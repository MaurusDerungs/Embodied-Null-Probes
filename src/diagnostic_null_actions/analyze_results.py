from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from math import sqrt
from pathlib import Path
from statistics import mean


METRICS = [
    "param_error",
    "posterior_entropy",
    "diagnostic_disturbance",
    "max_diagnostic_disturbance",
    "cumulative_diagnostic_disturbance",
    "recovery_distance",
    "recovery_gain",
]


CONDITION_KEYS = [
    "diagnostic_steps",
    "recovery_task",
    "observation_noise",
    "process_noise",
    "slip_correlation",
    "max_predicted_diagnostic_disturbance",
]


def load_rows(path: Path) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def mean_ci(values: list[float]) -> tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    if len(values) == 1:
        return values[0], 0.0
    m = mean(values)
    var = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return m, 1.96 * sqrt(var / len(values))


def group(rows: list[dict[str, str]], *keys: str) -> dict[tuple[str, ...], list[dict[str, str]]]:
    out: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        out[tuple(row[k] for k in keys)].append(row)
    return dict(out)


def available_condition_keys(rows: list[dict[str, str]]) -> list[str]:
    return [key for key in CONDITION_KEYS if key in rows[0]]


def policy_summary(rows: list[dict[str, str]]) -> list[str]:
    lines = [
        "| Policy | n | Param error | Entropy | Final disturbance | Max disturbance | Cumulative disturbance | Recovery distance | Recovery gain |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for (policy,), items in sorted(group(rows, "policy").items()):
        cells = [policy, str(len(items))]
        for metric in METRICS:
            m, ci = mean_ci([float(row[metric]) for row in items])
            cells.append(f"{m:.4f} +/- {ci:.4f}")
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def damage_summary(rows: list[dict[str, str]]) -> list[str]:
    lines = [
        "| Damage | Policy | Param error | Final disturbance | Max disturbance | Recovery gain |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for (damage, policy), items in sorted(group(rows, "damage", "policy").items()):
        cells = [damage, policy]
        for metric in ["param_error", "diagnostic_disturbance", "max_diagnostic_disturbance", "recovery_gain"]:
            m, ci = mean_ci([float(row[metric]) for row in items])
            cells.append(f"{m:.4f} +/- {ci:.4f}")
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def budget_summary(rows: list[dict[str, str]]) -> list[str]:
    if "diagnostic_steps" not in rows[0]:
        return []
    lines = [
        "| Steps | Policy | Param error | Max disturbance | Cumulative disturbance | Recovery gain |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    keys = sorted(group(rows, "diagnostic_steps", "policy").items(), key=lambda item: (int(item[0][0]), item[0][1]))
    for (steps, policy), items in keys:
        cells = [steps, policy]
        for metric in ["param_error", "max_diagnostic_disturbance", "cumulative_diagnostic_disturbance", "recovery_gain"]:
            m, ci = mean_ci([float(row[metric]) for row in items])
            cells.append(f"{m:.4f} +/- {ci:.4f}")
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def budget_paired_differences(rows: list[dict[str, str]], reference: str = "null_probe") -> list[str]:
    if "diagnostic_steps" not in rows[0]:
        return []
    lines = [
        f"Reference policy: `{reference}`. Positive values mean the compared policy is larger than the reference.",
        "",
        "| Steps | Compared policy | Param error diff | Max disturbance diff | Cumulative disturbance diff | Matched cases |",
        "|---:|---|---:|---:|---:|---:|",
    ]
    policies = sorted({row["policy"] for row in rows if row["policy"] != reference})
    steps_values = sorted({row["diagnostic_steps"] for row in rows}, key=int)
    for steps in steps_values:
        step_rows = [row for row in rows if row["diagnostic_steps"] == steps]
        pair_keys = [key for key in available_condition_keys(step_rows) if key != "diagnostic_steps"]
        by_case = group(step_rows, *pair_keys, "trial", "damage")
        for policy in policies:
            diffs = {metric: [] for metric in ["param_error", "max_diagnostic_disturbance", "cumulative_diagnostic_disturbance"]}
            matched = 0
            for items in by_case.values():
                by_policy = {row["policy"]: row for row in items}
                if reference not in by_policy or policy not in by_policy:
                    continue
                matched += 1
                for metric in diffs:
                    diffs[metric].append(float(by_policy[policy][metric]) - float(by_policy[reference][metric]))
            cells = [steps, policy]
            for metric in ["param_error", "max_diagnostic_disturbance", "cumulative_diagnostic_disturbance"]:
                m, ci = mean_ci(diffs[metric])
                cells.append(f"{m:.4f} +/- {ci:.4f}")
            cells.append(str(matched))
            lines.append("| " + " | ".join(cells) + " |")
    return lines


def pareto_summary(rows: list[dict[str, str]]) -> list[str]:
    if "diagnostic_steps" not in rows[0]:
        return []
    by_step_policy = group(rows, "diagnostic_steps", "policy")
    points = []
    for (steps, policy), items in by_step_policy.items():
        param_error, _ = mean_ci([float(row["param_error"]) for row in items])
        max_disturbance, _ = mean_ci([float(row["max_diagnostic_disturbance"]) for row in items])
        cumulative_disturbance, _ = mean_ci([float(row["cumulative_diagnostic_disturbance"]) for row in items])
        recovery_distance, _ = mean_ci([float(row["recovery_distance"]) for row in items])
        points.append({
            "steps": steps,
            "policy": policy,
            "param_error": param_error,
            "max_disturbance": max_disturbance,
            "cumulative_disturbance": cumulative_disturbance,
            "recovery_distance": recovery_distance,
        })

    lines = [
        "Two-metric dominance is computed over mean parameter error and mean max diagnostic disturbance; lower is better for both.",
        "",
        "| Steps | Two-metric Pareto policies | Two-metric dominated policies | Three-metric Pareto policies | Three-metric dominated policies |",
        "|---:|---|---|---|---|",
    ]
    for steps in sorted({point["steps"] for point in points}, key=int):
        step_points = [point for point in points if point["steps"] == steps]
        pareto_2d = []
        dominated_2d = []
        pareto_3d = []
        dominated_3d = []
        for point in step_points:
            is_dominated_2d = any(
                other["policy"] != point["policy"]
                and other["param_error"] <= point["param_error"]
                and other["max_disturbance"] <= point["max_disturbance"]
                and (
                    other["param_error"] < point["param_error"]
                    or other["max_disturbance"] < point["max_disturbance"]
                )
                for other in step_points
            )
            is_dominated_3d = any(
                other["policy"] != point["policy"]
                and other["param_error"] <= point["param_error"]
                and other["max_disturbance"] <= point["max_disturbance"]
                and other["cumulative_disturbance"] <= point["cumulative_disturbance"]
                and (
                    other["param_error"] < point["param_error"]
                    or other["max_disturbance"] < point["max_disturbance"]
                    or other["cumulative_disturbance"] < point["cumulative_disturbance"]
                )
                for other in step_points
            )
            (dominated_2d if is_dominated_2d else pareto_2d).append(point["policy"])
            (dominated_3d if is_dominated_3d else pareto_3d).append(point["policy"])
        lines.append(
            f"| {steps} | {', '.join(sorted(pareto_2d))} | {', '.join(sorted(dominated_2d))} | "
            f"{', '.join(sorted(pareto_3d))} | {', '.join(sorted(dominated_3d))} |"
        )
    return lines


def robustness_summary(rows: list[dict[str, str]]) -> list[str]:
    required = {"diagnostic_steps", "observation_noise", "max_predicted_diagnostic_disturbance"}
    if not required.issubset(rows[0]):
        return []
    selected = {"null_probe", "constrained_fisher"}
    filtered = [row for row in rows if row["policy"] in selected]
    lines = [
        "Focused on `null_probe` and `constrained_fisher`; lower is better for parameter error and max disturbance.",
        "",
        "| Steps | Obs noise | Disturbance limit | Policy | Param error | Max disturbance | Cumulative disturbance |",
        "|---:|---:|---:|---|---:|---:|---:|",
    ]
    keys = sorted(
        group(filtered, "diagnostic_steps", "observation_noise", "max_predicted_diagnostic_disturbance", "policy").items(),
        key=lambda item: (int(item[0][0]), float(item[0][1]), float(item[0][2]), item[0][3]),
    )
    for (steps, noise, limit, policy), items in keys:
        cells = [steps, noise, limit, policy]
        for metric in ["param_error", "max_diagnostic_disturbance", "cumulative_diagnostic_disturbance"]:
            m, ci = mean_ci([float(row[metric]) for row in items])
            cells.append(f"{m:.4f} +/- {ci:.4f}")
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def slip_correlation_summary(rows: list[dict[str, str]]) -> list[str]:
    if "slip_correlation" not in rows[0]:
        return []
    lines = [
        "| Slip corr | Steps | Policy | Param error | Max disturbance | Cumulative disturbance |",
        "|---:|---:|---|---:|---:|---:|",
    ]
    keys = sorted(
        group(rows, "slip_correlation", "diagnostic_steps", "policy").items(),
        key=lambda item: (float(item[0][0]), int(item[0][1]), item[0][2]),
    )
    for (corr, steps, policy), items in keys:
        cells = [corr, steps, policy]
        for metric in ["param_error", "max_diagnostic_disturbance", "cumulative_diagnostic_disturbance"]:
            m, ci = mean_ci([float(row[metric]) for row in items])
            cells.append(f"{m:.4f} +/- {ci:.4f}")
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def paired_policy_differences(rows: list[dict[str, str]], reference: str = "null_probe") -> list[str]:
    by_case = group(rows, *available_condition_keys(rows), "trial", "damage")
    policies = sorted({row["policy"] for row in rows if row["policy"] != reference})
    lines = [
        f"Reference policy: `{reference}`. Positive values mean the compared policy is larger than the reference.",
        "",
        "| Compared policy | Param error diff | Final disturbance diff | Max disturbance diff | Cumulative disturbance diff | Recovery gain diff | Matched cases |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for policy in policies:
        diffs = {metric: [] for metric in ["param_error", "diagnostic_disturbance", "max_diagnostic_disturbance", "cumulative_diagnostic_disturbance", "recovery_gain"]}
        matched = 0
        for items in by_case.values():
            by_policy = {row["policy"]: row for row in items}
            if reference not in by_policy or policy not in by_policy:
                continue
            matched += 1
            for metric in diffs:
                diffs[metric].append(float(by_policy[policy][metric]) - float(by_policy[reference][metric]))
        cells = [policy]
        for metric in ["param_error", "diagnostic_disturbance", "max_diagnostic_disturbance", "cumulative_diagnostic_disturbance", "recovery_gain"]:
            m, ci = mean_ci(diffs[metric])
            cells.append(f"{m:.4f} +/- {ci:.4f}")
        cells.append(str(matched))
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)

    rows = load_rows(args.input)
    lines = [
        "# Experiment Summary",
        "",
        f"Input: `{args.input}`",
        f"Rows: {len(rows)}",
        "",
        "## Policy Means",
        "",
        *policy_summary(rows),
        "",
        "## Paired Differences Against Null Probes",
        "",
        *paired_policy_differences(rows),
        "",
        "## Budget-Conditioned Means",
        "",
        *budget_summary(rows),
        "",
        "## Budget-Conditioned Paired Differences",
        "",
        *budget_paired_differences(rows),
        "",
        "## Pareto Check",
        "",
        *pareto_summary(rows),
        "",
        "## Robustness Detail",
        "",
        *robustness_summary(rows),
        "",
        "## Slip-Correlation Detail",
        "",
        *slip_correlation_summary(rows),
        "",
        "## By Damage Case",
        "",
        *damage_summary(rows),
        "",
    ]
    text = "\n".join(lines)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
