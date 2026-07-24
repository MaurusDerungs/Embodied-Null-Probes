from __future__ import annotations

from random import Random

NULL_SEQUENCE = [
    (0.8, 0.8), (-0.8, -0.8),
    (0.7, -0.7), (-0.7, 0.7),
    (0.45, 0.9), (-0.45, -0.9),
    (0.9, 0.45), (-0.9, -0.45),
]

UNPAIRED_NULL_SEQUENCE = [
    (0.8, 0.8), (0.7, -0.7), (0.45, 0.9), (0.9, 0.45),
    (-0.8, -0.8), (-0.7, 0.7), (-0.45, -0.9), (-0.9, -0.45),
]


def action_for(policy: str, t: int, rng: Random, state=None, goal=(2.0, 0.0)) -> tuple[float, float]:
    if policy == "null_probe":
        return NULL_SEQUENCE[t % len(NULL_SEQUENCE)]
    if policy == "unpaired_null":
        return UNPAIRED_NULL_SEQUENCE[t % len(UNPAIRED_NULL_SEQUENCE)]
    if policy == "random_probe":
        return rng.uniform(-0.9, 0.9), rng.uniform(-0.9, 0.9)
    if policy == "fisher_grid":
        grid = [(-0.9, -0.9), (-0.9, 0.9), (0.9, -0.9), (0.9, 0.9), (0.0, 0.9), (0.9, 0.0)]
        return grid[t % len(grid)]
    if policy == "task_greedy":
        from diagnostic_null_actions.sim import greedy_action

        return greedy_action(state, goal)
    raise ValueError(f"unknown policy: {policy}")
