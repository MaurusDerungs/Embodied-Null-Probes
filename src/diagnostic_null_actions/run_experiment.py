from __future__ import annotations

import csv
import json
import os
import sys
from itertools import product
from math import cos, exp, log, pi, sin
from pathlib import Path
from random import Random

from diagnostic_null_actions.policies import action_for
from diagnostic_null_actions.sim import Damage, SimConfig, State, displacement, distance_to_goal, greedy_action, observe, step


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def candidate_grid() -> list[Damage]:
    gains = [0.6, 0.75, 0.9, 1.0]
    slips = [0.02, 0.10, 0.20]
    return [Damage(f"g{lg:.2f}_{rg:.2f}_s{s:.2f}", lg, rg, s) for lg, rg, s in product(gains, gains, slips)]


def action_energy(action: tuple[float, float]) -> float:
    return 0.5 * (action[0] * action[0] + action[1] * action[1])


def state_disturbance(state: State) -> float:
    return (state.x * state.x + state.y * state.y) ** 0.5 + 0.2 * abs(angle_delta(state.theta, 0.0))


def mean_step(state: State, action: tuple[float, float], damage: Damage, cfg: SimConfig) -> State:
    left_cmd, right_cmd = action
    left = left_cmd * damage.left_gain
    right = right_cmd * damage.right_gain
    v = 0.5 * (left + right)
    omega = (right - left) / cfg.wheel_base
    return State(
        x=state.x + v * cos(state.theta) * cfg.dt,
        y=state.y + v * sin(state.theta) * cfg.dt,
        theta=state.theta + omega * cfg.dt,
    )


def constrained_fisher_action(state: State, cfg: SimConfig, max_disturbance: float) -> tuple[float, float]:
    nominal = Damage("nominal", 1.0, 1.0, 0.02)
    commands = [-0.9, -0.45, 0.0, 0.45, 0.9]
    best_action = None
    best_score = -float("inf")
    fallback_action = None
    fallback_disturbance = float("inf")
    for left in commands:
        for right in commands:
            if left == 0.0 and right == 0.0:
                continue
            action = (left, right)
            predicted = mean_step(state, action, nominal, cfg)
            disturbance = state_disturbance(predicted)
            info_proxy = left * left + right * right + 0.5 * (right - left) * (right - left)
            if disturbance < fallback_disturbance:
                fallback_disturbance = disturbance
                fallback_action = action
            if disturbance > max_disturbance:
                continue
            score = info_proxy - 0.25 * disturbance
            if score > best_score:
                best_score = score
                best_action = action
    assert fallback_action is not None
    return best_action if best_action is not None else fallback_action


def select_action(policy: str, t: int, rng: Random, state: State, cfg: SimConfig, max_disturbance: float) -> tuple[float, float]:
    if policy == "constrained_fisher":
        return constrained_fisher_action(state, cfg, max_disturbance)
    return action_for(policy, t, rng, state=state)


def rollout(policy: str, damage: Damage, cfg: SimConfig, seed: int, steps: int, max_predicted_disturbance: float = 0.12) -> tuple[list[tuple[State, tuple[float, float], State]], float, float, float, float]:
    rng = Random(seed)
    state = State()
    obs0 = observe(state, cfg, rng)
    trace = []
    energy = 0.0
    cumulative_disturbance = 0.0
    max_disturbance = 0.0
    for t in range(steps):
        action = select_action(policy, t, rng, state, cfg, max_predicted_disturbance)
        energy += action_energy(action)
        nxt = step(state, action, damage, cfg, rng)
        trace.append((observe(state, cfg, rng), action, observe(nxt, cfg, rng)))
        state = nxt
        current_disturbance = state_disturbance(state)
        cumulative_disturbance += current_disturbance
        max_disturbance = max(max_disturbance, current_disturbance)
    obs1 = observe(state, cfg, rng)
    dx, dy, dtheta = displacement(obs0, obs1)
    disturbance = (dx * dx + dy * dy) ** 0.5 + 0.2 * abs(dtheta)
    return trace, disturbance, max_disturbance, cumulative_disturbance, energy


def angle_delta(a: float, b: float) -> float:
    return (a - b + pi) % (2 * pi) - pi


def transition_loss(obs: State, action: tuple[float, float], nxt: State, cand: Damage, cfg: SimConfig) -> float:
    left_cmd, right_cmd = action
    left = left_cmd * cand.left_gain
    right = right_cmd * cand.right_gain
    v = 0.5 * (left + right)
    omega = (right - left) / cfg.wheel_base

    expected_dx = v * cos(obs.theta) * cfg.dt
    expected_dy = v * sin(obs.theta) * cfg.dt
    expected_dtheta = omega * cfg.dt
    dx = nxt.x - obs.x
    dy = nxt.y - obs.y
    dtheta = angle_delta(nxt.theta, obs.theta)

    forward_resid = (dx - expected_dx) * cos(obs.theta) + (dy - expected_dy) * sin(obs.theta)
    lateral_resid = -(dx - expected_dx) * sin(obs.theta) + (dy - expected_dy) * cos(obs.theta)
    theta_resid = angle_delta(dtheta, expected_dtheta)

    obs_var = max(1e-6, 2.0 * cfg.observation_noise * cfg.observation_noise + cfg.process_noise * cfg.process_noise)
    lateral_var = obs_var + ((cand.slip * abs(omega) * cfg.dt) ** 2) / 3.0
    theta_var = obs_var

    return (
        (forward_resid * forward_resid) / obs_var
        + (lateral_resid * lateral_resid) / lateral_var
        + 0.1 * (theta_resid * theta_resid) / theta_var
        + log(obs_var)
        + log(lateral_var)
        + log(theta_var)
    )


def fit_damage(trace: list[tuple[State, tuple[float, float], State]], cfg: SimConfig) -> tuple[Damage, float, float]:
    best = None
    best_loss = float("inf")
    losses = []
    for cand in candidate_grid():
        loss = 0.0
        for obs, action, nxt in trace:
            loss += transition_loss(obs, action, nxt, cand, cfg)
        losses.append((cand, loss))
        if loss < best_loss:
            best = cand
            best_loss = loss
    assert best is not None
    min_loss = min(loss for _, loss in losses)
    weights = [exp(-0.5 * (loss - min_loss)) for _, loss in losses]
    total = sum(weights)
    probs = [w / total for w in weights]
    entropy = -sum(p * log(max(p, 1e-12)) for p in probs)
    confidence = max(probs)
    return best, entropy, confidence


def compensate_action(action: tuple[float, float], model: Damage) -> tuple[float, float]:
    left = max(-1.0, min(1.0, action[0] / max(model.left_gain, 0.1)))
    right = max(-1.0, min(1.0, action[1] / max(model.right_gain, 0.1)))
    return left, right


def task_score(true_damage: Damage, model: Damage, cfg: SimConfig, seed: int, task_steps: int, task: str = "straight_goal") -> float:
    rng = Random(seed)
    state = State()
    if task == "straight_goal":
        goals = [(2.0, 0.0)]
    elif task == "square_waypoints":
        goals = [(0.7, 0.0), (0.7, 0.7), (0.0, 0.7), (0.0, 0.0)]
    else:
        raise ValueError(f"unknown recovery task: {task}")

    goal_index = 0
    for _ in range(task_steps):
        goal = goals[goal_index]
        action = compensate_action(greedy_action(state, goal), model)
        state = step(state, action, true_damage, cfg, rng)
        if distance_to_goal(state, goal) < 0.08 and goal_index < len(goals) - 1:
            goal_index += 1
    final_goal = goals[goal_index]
    remaining_waypoints = len(goals) - goal_index - 1
    return distance_to_goal(state, final_goal) + float(remaining_waypoints)


def run_config(config: dict) -> list[dict[str, object]]:
    cfg = SimConfig(
        dt=config["dt"],
        wheel_base=config["wheel_base"],
        process_noise=config["process_noise"],
        observation_noise=config["observation_noise"],
        slip_correlation=config.get("slip_correlation", 0.0),
    )
    rows = []
    for trial in range(config["trials"]):
        for d in config["damage_cases"]:
            damage = Damage(d["name"], d["left_gain"], d["right_gain"], d["slip"])
            for policy in config["policies"]:
                seed = config["seed"] + trial * 1000 + len(rows)
                trace, disturbance, max_disturbance, cumulative_disturbance, energy = rollout(
                    policy,
                    damage,
                    cfg,
                    seed,
                    config["diagnostic_steps"],
                    config.get("max_predicted_diagnostic_disturbance", 0.12),
                )
                estimate, entropy, confidence = fit_damage(trace, cfg)
                param_error = abs(estimate.left_gain - damage.left_gain) + abs(estimate.right_gain - damage.right_gain) + abs(estimate.slip - damage.slip)
                nominal = Damage("nominal", 1.0, 1.0, 0.02)
                recovery_task = config.get("recovery_task", "straight_goal")
                recovery_distance = task_score(damage, estimate, cfg, seed + 99, config["task_steps"], recovery_task)
                nominal_recovery_distance = task_score(damage, nominal, cfg, seed + 99, config["task_steps"], recovery_task)
                rows.append({
                    "trial": trial,
                    "diagnostic_steps": config["diagnostic_steps"],
                    "recovery_task": recovery_task,
                    "observation_noise": config["observation_noise"],
                    "process_noise": config["process_noise"],
                    "slip_correlation": config.get("slip_correlation", 0.0),
                    "max_predicted_diagnostic_disturbance": config.get("max_predicted_diagnostic_disturbance", 0.12),
                    "damage": damage.name,
                    "policy": policy,
                    "estimate": estimate.name,
                    "param_error": f"{param_error:.4f}",
                    "posterior_entropy": f"{entropy:.4f}",
                    "posterior_confidence": f"{confidence:.4f}",
                    "action_energy": f"{energy:.4f}",
                    "diagnostic_disturbance": f"{disturbance:.4f}",
                    "max_diagnostic_disturbance": f"{max_disturbance:.4f}",
                    "cumulative_diagnostic_disturbance": f"{cumulative_disturbance:.4f}",
                    "recovery_distance": f"{recovery_distance:.4f}",
                    "nominal_recovery_distance": f"{nominal_recovery_distance:.4f}",
                    "recovery_gain": f"{nominal_recovery_distance - recovery_distance:.4f}",
                    "seed": seed,
                })
    return rows


def write_rows(rows: list[dict[str, object]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    config_path = argv[0] if argv else "configs/base.json"
    config = load_config(config_path)
    out = Path(config["output"])
    rows = run_config(config)
    write_rows(rows, out)
    print(os.fspath(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
