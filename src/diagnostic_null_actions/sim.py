from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, sin, sqrt
from random import Random


@dataclass(frozen=True)
class Damage:
    name: str
    left_gain: float
    right_gain: float
    slip: float


@dataclass
class State:
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0
    slip_bias: float = 0.0


@dataclass(frozen=True)
class SimConfig:
    dt: float = 0.1
    wheel_base: float = 0.42
    process_noise: float = 0.003
    observation_noise: float = 0.01
    slip_correlation: float = 0.0


def step(state: State, action: tuple[float, float], damage: Damage, cfg: SimConfig, rng: Random) -> State:
    left_cmd, right_cmd = action
    left = left_cmd * damage.left_gain
    right = right_cmd * damage.right_gain
    v = 0.5 * (left + right)
    omega = (right - left) / cfg.wheel_base
    innovation = damage.slip * rng.uniform(-1.0, 1.0)
    innovation_scale = sqrt(max(0.0, 1.0 - cfg.slip_correlation * cfg.slip_correlation))
    slip_bias = cfg.slip_correlation * state.slip_bias + innovation_scale * innovation
    lateral_slip = slip_bias * abs(omega)

    dx = (v * cos(state.theta) - lateral_slip * sin(state.theta)) * cfg.dt
    dy = (v * sin(state.theta) + lateral_slip * cos(state.theta)) * cfg.dt
    dtheta = omega * cfg.dt
    return State(
        x=state.x + dx + rng.gauss(0.0, cfg.process_noise),
        y=state.y + dy + rng.gauss(0.0, cfg.process_noise),
        theta=state.theta + dtheta + rng.gauss(0.0, cfg.process_noise),
        slip_bias=slip_bias,
    )


def observe(state: State, cfg: SimConfig, rng: Random) -> State:
    return State(
        x=state.x + rng.gauss(0.0, cfg.observation_noise),
        y=state.y + rng.gauss(0.0, cfg.observation_noise),
        theta=state.theta + rng.gauss(0.0, cfg.observation_noise),
    )


def displacement(a: State, b: State) -> tuple[float, float, float]:
    return b.x - a.x, b.y - a.y, b.theta - a.theta


def distance_to_goal(state: State, goal: tuple[float, float]) -> float:
    return hypot(goal[0] - state.x, goal[1] - state.y)


def greedy_action(state: State, goal: tuple[float, float]) -> tuple[float, float]:
    desired = atan2(goal[1] - state.y, goal[0] - state.x)
    heading_error = (desired - state.theta + 3.141592653589793) % (2 * 3.141592653589793) - 3.141592653589793
    turn = max(-0.8, min(0.8, 1.8 * heading_error))
    speed = 0.7 if abs(heading_error) < 0.7 else 0.25
    return speed - turn, speed + turn
