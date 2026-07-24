from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from math import ceil, floor, log10, sqrt
from pathlib import Path
from random import Random
from statistics import mean
from xml.sax.saxutils import escape

from diagnostic_null_actions.run_experiment import select_action, state_disturbance
from diagnostic_null_actions.sim import Damage, SimConfig, State, step


COLORS = {
    "null_probe": "#0072b2",
    "unpaired_null": "#d55e00",
    "constrained_fisher": "#009e73",
    "fisher_grid": "#cc79a7",
    "random_probe": "#777777",
    "task_greedy": "#e69f00",
}

DISPLAY = {
    "null_probe": "paired null",
    "unpaired_null": "unpaired null",
    "constrained_fisher": "constrained Fisher",
    "fisher_grid": "Fisher grid",
    "random_probe": "random",
    "task_greedy": "task greedy",
}


@dataclass(frozen=True)
class Summary:
    mean: float
    ci95: float
    n: int


@dataclass(frozen=True)
class Panel:
    x: float
    y: float
    w: float
    h: float
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    xlabel: str
    ylabel: str
    title: str

    def sx(self, value: float) -> float:
        if self.xmax == self.xmin:
            return self.x + 0.5 * self.w
        return self.x + (value - self.xmin) * self.w / (self.xmax - self.xmin)

    def sy(self, value: float) -> float:
        if self.ymax == self.ymin:
            return self.y + 0.5 * self.h
        return self.y + self.h - (value - self.ymin) * self.h / (self.ymax - self.ymin)


def read_rows(path: Path) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def summarize(rows: list[dict[str, str]], keys: list[str], metric: str) -> dict[tuple[str, ...], Summary]:
    grouped: dict[tuple[str, ...], list[float]] = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(float(row[metric]))
    out = {}
    for key, values in grouped.items():
        m = mean(values)
        if len(values) < 2:
            ci = 0.0
        else:
            var = sum((v - m) ** 2 for v in values) / (len(values) - 1)
            ci = 1.96 * sqrt(var / len(values))
        out[key] = Summary(m, ci, len(values))
    return out


def nice_step(span: float, target_ticks: int = 5) -> float:
    if span <= 0:
        return 1.0
    raw = span / target_ticks
    mag = 10 ** floor(log10(raw))
    for mult in [1, 2, 2.5, 5, 10]:
        step = mult * mag
        if raw <= step:
            return step
    return 10 * mag


def ticks(lo: float, hi: float, target_ticks: int = 5) -> list[float]:
    step = nice_step(hi - lo, target_ticks)
    start = ceil(lo / step) * step
    values = []
    v = start
    while v <= hi + 1e-12:
        values.append(0.0 if abs(v) < 1e-12 else v)
        v += step
    return values


def pad_range(values: list[float], frac: float = 0.08) -> tuple[float, float]:
    lo = min(values)
    hi = max(values)
    if lo == hi:
        delta = 1.0 if lo == 0 else abs(lo) * 0.1
        return lo - delta, hi + delta
    delta = (hi - lo) * frac
    return lo - delta, hi + delta


def fmt(value: float) -> str:
    if abs(value) >= 10:
        return f"{value:.0f}"
    if abs(value) >= 1:
        return f"{value:.1f}"
    return f"{value:.2f}"


def svg_page(width: int, height: int, body: list[str]) -> str:
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text{font-family:Arial,Helvetica,sans-serif;fill:#202020}",
        ".title{font-size:18px;font-weight:700}",
        ".subtitle{font-size:13px;fill:#444}",
        ".label{font-size:13px}",
        ".tick{font-size:11px;fill:#444}",
        ".caption{font-size:12px;fill:#333}",
        ".axis{stroke:#202020;stroke-width:1.2}",
        ".grid{stroke:#dddddd;stroke-width:1}",
        ".ci{stroke-width:1.5;stroke-linecap:round}",
        "</style>",
        *body,
        "</svg>",
        "",
    ])


def write_svg(path: Path, width: int, height: int, body: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg_page(width, height, body), encoding="utf-8")


def draw_panel(body: list[str], panel: Panel) -> None:
    body.append(f'<text class="title" x="{panel.x}" y="{panel.y - 28}">{escape(panel.title)}</text>')
    body.append(f'<rect x="{panel.x}" y="{panel.y}" width="{panel.w}" height="{panel.h}" fill="#fff" stroke="#cfcfcf"/>')
    for x_tick in ticks(panel.xmin, panel.xmax):
        x = panel.sx(x_tick)
        body.append(f'<line class="grid" x1="{x:.1f}" y1="{panel.y}" x2="{x:.1f}" y2="{panel.y + panel.h}"/>')
        body.append(f'<line class="axis" x1="{x:.1f}" y1="{panel.y + panel.h}" x2="{x:.1f}" y2="{panel.y + panel.h + 5}"/>')
        body.append(f'<text class="tick" x="{x:.1f}" y="{panel.y + panel.h + 19}" text-anchor="middle">{fmt(x_tick)}</text>')
    for y_tick in ticks(panel.ymin, panel.ymax):
        y = panel.sy(y_tick)
        body.append(f'<line class="grid" x1="{panel.x}" y1="{y:.1f}" x2="{panel.x + panel.w}" y2="{y:.1f}"/>')
        body.append(f'<line class="axis" x1="{panel.x - 5}" y1="{y:.1f}" x2="{panel.x}" y2="{y:.1f}"/>')
        body.append(f'<text class="tick" x="{panel.x - 9}" y="{y + 4:.1f}" text-anchor="end">{fmt(y_tick)}</text>')
    body.append(f'<line class="axis" x1="{panel.x}" y1="{panel.y + panel.h}" x2="{panel.x + panel.w}" y2="{panel.y + panel.h}"/>')
    body.append(f'<line class="axis" x1="{panel.x}" y1="{panel.y}" x2="{panel.x}" y2="{panel.y + panel.h}"/>')
    body.append(f'<text class="label" x="{panel.x + panel.w / 2}" y="{panel.y + panel.h + 45}" text-anchor="middle">{escape(panel.xlabel)}</text>')
    body.append(
        f'<text class="label" x="{panel.x - 52}" y="{panel.y + panel.h / 2}" '
        f'transform="rotate(-90 {panel.x - 52} {panel.y + panel.h / 2})" text-anchor="middle">{escape(panel.ylabel)}</text>'
    )


def draw_error_bar(body: list[str], panel: Panel, x: float, y: Summary, color: str, vertical: bool = True) -> None:
    if vertical:
        x0 = panel.sx(x)
        y0 = panel.sy(y.mean)
        y_low = panel.sy(y.mean - y.ci95)
        y_high = panel.sy(y.mean + y.ci95)
        body.append(f'<line class="ci" x1="{x0:.1f}" y1="{y_low:.1f}" x2="{x0:.1f}" y2="{y_high:.1f}" stroke="{color}"/>')
        body.append(f'<line class="ci" x1="{x0 - 4:.1f}" y1="{y_low:.1f}" x2="{x0 + 4:.1f}" y2="{y_low:.1f}" stroke="{color}"/>')
        body.append(f'<line class="ci" x1="{x0 - 4:.1f}" y1="{y_high:.1f}" x2="{x0 + 4:.1f}" y2="{y_high:.1f}" stroke="{color}"/>')
        body.append(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="4.5" fill="{color}"/>')


def draw_xy_error(
    body: list[str],
    panel: Panel,
    x: Summary,
    y: Summary,
    color: str,
    label: str,
    dx_label: float = 6,
    dy_label: float = -7,
) -> None:
    px = panel.sx(x.mean)
    py = panel.sy(y.mean)
    xl = panel.sx(x.mean - x.ci95)
    xh = panel.sx(x.mean + x.ci95)
    yl = panel.sy(y.mean - y.ci95)
    yh = panel.sy(y.mean + y.ci95)
    body.append(f'<line class="ci" x1="{xl:.1f}" y1="{py:.1f}" x2="{xh:.1f}" y2="{py:.1f}" stroke="{color}"/>')
    body.append(f'<line class="ci" x1="{px:.1f}" y1="{yl:.1f}" x2="{px:.1f}" y2="{yh:.1f}" stroke="{color}"/>')
    body.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{color}" stroke="#fff" stroke-width="1"/>')
    body.append(f'<text class="tick" x="{px + dx_label:.1f}" y="{py + dy_label:.1f}">{escape(label)}</text>')


def legend(body: list[str], x: float, y: float, policies: list[str]) -> None:
    for i, policy in enumerate(policies):
        yy = y + i * 20
        body.append(f'<circle cx="{x}" cy="{yy}" r="5" fill="{COLORS[policy]}"/>')
        body.append(f'<text class="tick" x="{x + 12}" y="{yy + 4}">{escape(DISPLAY[policy])}</text>')


def caption(body: list[str], x: float, y: float, lines: list[str]) -> None:
    for i, line in enumerate(lines):
        body.append(f'<text class="caption" x="{x}" y="{y + i * 17}">{escape(line)}</text>')


def fig1_budget_metrics(budget_rows: list[dict[str, str]], out: Path) -> None:
    policies = ["null_probe", "constrained_fisher", "fisher_grid", "unpaired_null", "random_probe", "task_greedy"]
    steps = sorted({int(row["diagnostic_steps"]) for row in budget_rows})
    metrics = {
        "param_error": summarize(budget_rows, ["diagnostic_steps", "policy"], "param_error"),
        "max_diagnostic_disturbance": summarize(budget_rows, ["diagnostic_steps", "policy"], "max_diagnostic_disturbance"),
        "cumulative_diagnostic_disturbance": summarize(budget_rows, ["diagnostic_steps", "policy"], "cumulative_diagnostic_disturbance"),
    }
    body: list[str] = ['<rect x="0" y="0" width="1320" height="520" fill="#ffffff"/>']
    panels = [
        ("param_error", Panel(80, 90, 340, 270, min(steps), max(steps), *pad_range([s.mean + s.ci95 for s in metrics["param_error"].values()] + [s.mean - s.ci95 for s in metrics["param_error"].values()]), "diagnostic horizon (steps)", "parameter error (L1)", "A. Identification error")),
        ("max_diagnostic_disturbance", Panel(510, 90, 340, 270, min(steps), max(steps), *pad_range([s.mean + s.ci95 for s in metrics["max_diagnostic_disturbance"].values()] + [s.mean - s.ci95 for s in metrics["max_diagnostic_disturbance"].values()]), "diagnostic horizon (steps)", "max disturbance", "B. Peak task-state disturbance")),
        ("cumulative_diagnostic_disturbance", Panel(940, 90, 340, 270, min(steps), max(steps), *pad_range([s.mean + s.ci95 for s in metrics["cumulative_diagnostic_disturbance"].values()] + [s.mean - s.ci95 for s in metrics["cumulative_diagnostic_disturbance"].values()]), "diagnostic horizon (steps)", "cumulative disturbance", "C. Integrated task-state disturbance")),
    ]
    for metric, panel in panels:
        draw_panel(body, panel)
        for policy in policies:
            pts = []
            for step_count in steps:
                summary = metrics[metric][(str(step_count), policy)]
                px = panel.sx(step_count)
                py = panel.sy(summary.mean)
                pts.append((px, py))
                draw_error_bar(body, panel, step_count, summary, COLORS[policy])
            body.append('<polyline fill="none" stroke="{}" stroke-width="2" points="{}"/>'.format(
                COLORS[policy],
                " ".join(f"{x:.1f},{y:.1f}" for x, y in pts),
            ))
    legend(body, 82, 440, policies)
    caption(body, 500, 430, [
        "Means with 95% CIs over 60 trials x 4 damage cases per policy/horizon (n=240 per point).",
        "Source: runs/budget_sweep_results.csv. Lower is better for all three metrics.",
    ])
    write_svg(out / "fig1_budget_metrics.svg", 1320, 520, body)


def fig2_pareto(budget_rows: list[dict[str, str]], out: Path) -> None:
    policies = ["null_probe", "constrained_fisher", "fisher_grid", "unpaired_null"]
    selected_steps = [8, 24, 40]
    param = summarize(budget_rows, ["diagnostic_steps", "policy"], "param_error")
    maxdist = summarize(budget_rows, ["diagnostic_steps", "policy"], "max_diagnostic_disturbance")
    xs = [param[(str(s), p)].mean + param[(str(s), p)].ci95 for s in selected_steps for p in policies]
    xs += [param[(str(s), p)].mean - param[(str(s), p)].ci95 for s in selected_steps for p in policies]
    ys = [maxdist[(str(s), p)].mean + maxdist[(str(s), p)].ci95 for s in selected_steps for p in policies]
    ys += [maxdist[(str(s), p)].mean - maxdist[(str(s), p)].ci95 for s in selected_steps for p in policies]
    xmin, xmax = pad_range(xs, 0.12)
    ymin, ymax = pad_range(ys, 0.12)
    body: list[str] = ['<rect x="0" y="0" width="980" height="660" fill="#ffffff"/>']
    panel = Panel(95, 85, 650, 420, xmin, xmax, ymin, ymax, "parameter error (L1)", "maximum diagnostic disturbance", "Pareto comparison with 95% CI bars")
    draw_panel(body, panel)
    offsets = {"null_probe": (-25, -9), "constrained_fisher": (7, -8), "fisher_grid": (7, 13), "unpaired_null": (7, -8)}
    for step_count in selected_steps:
        for policy in policies:
            dx, dy = offsets[policy]
            draw_xy_error(
                body,
                panel,
                param[(str(step_count), policy)],
                maxdist[(str(step_count), policy)],
                COLORS[policy],
                f"{DISPLAY[policy]}, {step_count}",
                dx,
                dy,
            )
    legend(body, 785, 100, policies)
    caption(body, 95, 560, [
        "Each point is a policy-horizon mean; horizontal and vertical bars show 95% CIs.",
        "Two-metric dominance uses x and y only. The paper also reports cumulative disturbance as a third safety metric.",
        "Source: runs/budget_sweep_results.csv.",
    ])
    write_svg(out / "fig2_pareto_ci.svg", 980, 660, body)


def fig3_ablation(budget_rows: list[dict[str, str]], out: Path) -> None:
    policies = ["null_probe", "unpaired_null"]
    steps = sorted({int(row["diagnostic_steps"]) for row in budget_rows})
    metrics = {
        "max_diagnostic_disturbance": summarize(budget_rows, ["diagnostic_steps", "policy"], "max_diagnostic_disturbance"),
        "cumulative_diagnostic_disturbance": summarize(budget_rows, ["diagnostic_steps", "policy"], "cumulative_diagnostic_disturbance"),
    }
    ratios = []
    for s in steps:
        ratios.append(metrics["cumulative_diagnostic_disturbance"][(str(s), "unpaired_null")].mean / metrics["cumulative_diagnostic_disturbance"][(str(s), "null_probe")].mean)
    body: list[str] = ['<rect x="0" y="0" width="1050" height="540" fill="#ffffff"/>']
    panel1 = Panel(80, 85, 405, 285, min(steps), max(steps), *pad_range([v.mean + v.ci95 for v in metrics["cumulative_diagnostic_disturbance"].values()]), "diagnostic horizon (steps)", "cumulative disturbance", "A. Local cancellation ablation")
    draw_panel(body, panel1)
    for policy in policies:
        pts = []
        for s in steps:
            summary = metrics["cumulative_diagnostic_disturbance"][(str(s), policy)]
            pts.append((panel1.sx(s), panel1.sy(summary.mean)))
            draw_error_bar(body, panel1, s, summary, COLORS[policy])
        body.append('<polyline fill="none" stroke="{}" stroke-width="2.5" points="{}"/>'.format(COLORS[policy], " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
    panel2 = Panel(600, 85, 330, 285, min(steps), max(steps), *pad_range(ratios), "diagnostic horizon (steps)", "unpaired / paired ratio", "B. Disturbance ratio")
    draw_panel(body, panel2)
    pts = []
    for s, ratio in zip(steps, ratios):
        x = panel2.sx(s)
        y = panel2.sy(ratio)
        pts.append((x, y))
        body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#202020"/>')
        body.append(f'<text class="tick" x="{x + 7:.1f}" y="{y - 7:.1f}">{ratio:.2f}x</text>')
    body.append('<polyline fill="none" stroke="#202020" stroke-width="2.5" points="{}"/>'.format(" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
    legend(body, 80, 435, policies)
    caption(body, 315, 430, [
        "Same action multiset, different ordering. Error bars are 95% CIs.",
        "The unpaired sequence accumulates about 1.9x-3.4x more disturbance across tested horizons.",
        "Source: runs/budget_sweep_results.csv.",
    ])
    write_svg(out / "fig3_cancellation_ablation.svg", 1050, 540, body)


def trajectory(policy: str, damage: Damage, cfg: SimConfig, seed: int, steps: int) -> list[State]:
    rng = Random(seed)
    state = State()
    states = [state]
    for t in range(steps):
        action = select_action(policy, t, rng, state, cfg, 0.12)
        state = step(state, action, damage, cfg, rng)
        states.append(state)
    return states


def fig4_trajectory_quant(out: Path) -> None:
    policies = ["null_probe", "unpaired_null", "constrained_fisher", "fisher_grid"]
    damage = Damage("left_gain_loss", 0.62, 1.0, 0.02)
    cfg = SimConfig(dt=0.1, wheel_base=0.42, process_noise=0.003, observation_noise=0.01)
    traces = {policy: trajectory(policy, damage, cfg, 37011, 40) for policy in policies}
    all_x = [state.x for trace in traces.values() for state in trace]
    all_y = [state.y for trace in traces.values() for state in trace]
    xmin, xmax = pad_range(all_x, 0.15)
    ymin, ymax = pad_range(all_y, 0.15)
    max_abs = max(abs(xmin), abs(xmax), abs(ymin), abs(ymax))
    xmin = ymin = -max_abs
    xmax = ymax = max_abs
    body: list[str] = ['<rect x="0" y="0" width="1120" height="600" fill="#ffffff"/>']
    panel = Panel(90, 80, 520, 420, xmin, xmax, ymin, ymax, "x position", "y position", "Representative 40-step diagnostic trajectories")
    draw_panel(body, panel)
    body.append(f'<line class="axis" x1="{panel.sx(0):.1f}" y1="{panel.y}" x2="{panel.sx(0):.1f}" y2="{panel.y + panel.h}" stroke="#777" stroke-dasharray="4 4"/>')
    body.append(f'<line class="axis" x1="{panel.x}" y1="{panel.sy(0):.1f}" x2="{panel.x + panel.w}" y2="{panel.sy(0):.1f}" stroke="#777" stroke-dasharray="4 4"/>')
    table_rows = []
    for policy, states in traces.items():
        pts = [(panel.sx(state.x), panel.sy(state.y)) for state in states]
        body.append('<polyline fill="none" stroke="{}" stroke-width="2.5" points="{}"/>'.format(COLORS[policy], " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
        body.append(f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5" fill="#202020"/>')
        body.append(f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="5" fill="{COLORS[policy]}"/>')
        disturbances = [state_disturbance(state) for state in states[1:]]
        table_rows.append((policy, max(disturbances), sum(disturbances), disturbances[-1]))
    legend(body, 665, 88, policies)
    body.append('<text class="title" x="665" y="210">Trajectory metrics for shown seed</text>')
    body.append('<text class="tick" x="665" y="238">policy</text><text class="tick" x="790" y="238">max</text><text class="tick" x="855" y="238">cum.</text><text class="tick" x="930" y="238">final</text>')
    for i, (policy, max_d, cum_d, final_d) in enumerate(table_rows):
        y = 262 + i * 24
        body.append(f'<circle cx="671" cy="{y - 4}" r="4" fill="{COLORS[policy]}"/>')
        body.append(f'<text class="tick" x="682" y="{y}">{escape(DISPLAY[policy])}</text>')
        body.append(f'<text class="tick" x="790" y="{y}">{max_d:.3f}</text>')
        body.append(f'<text class="tick" x="855" y="{y}">{cum_d:.3f}</text>')
        body.append(f'<text class="tick" x="930" y="{y}">{final_d:.3f}</text>')
    caption(body, 90, 545, [
        "Single representative seed, left wheel gain = 0.62, horizon = 40. Axes use simulator state units.",
        "The table quantifies the plotted trajectory; aggregate statistics are in Figures 1-3.",
    ])
    write_svg(out / "fig4_trajectory_quantified.svg", 1120, 600, body)


def fig5_robustness(threshold_rows: list[dict[str, str]], slip_rows: list[dict[str, str]], out: Path) -> None:
    policies = ["null_probe", "constrained_fisher"]
    body: list[str] = ['<rect x="0" y="0" width="1220" height="560" fill="#ffffff"/>']

    filtered = [
        row for row in threshold_rows
        if row["policy"] in policies and row["observation_noise"] == "0.01"
    ]
    td = summarize(filtered, ["diagnostic_steps", "max_predicted_diagnostic_disturbance", "policy"], "cumulative_diagnostic_disturbance")
    steps = sorted({int(row["diagnostic_steps"]) for row in filtered})
    limits = sorted({float(row["max_predicted_diagnostic_disturbance"]) for row in filtered})
    vals = [s.mean + s.ci95 for s in td.values()] + [s.mean - s.ci95 for s in td.values()]
    p1 = Panel(80, 90, 460, 310, min(steps), max(steps), *pad_range(vals), "diagnostic horizon (steps)", "cumulative disturbance", "A. Threshold sweep at observation noise = 0.01")
    draw_panel(body, p1)
    dash = {0.08: "2 2", 0.12: "6 2", 0.18: "10 3"}
    for policy in policies:
        for limit in limits:
            pts = []
            for s in steps:
                summary = td[(str(s), str(limit), policy)]
                x = p1.sx(s)
                y = p1.sy(summary.mean)
                pts.append((x, y))
                if policy == "constrained_fisher":
                    body.append(f'<line class="ci" x1="{x:.1f}" y1="{p1.sy(summary.mean - summary.ci95):.1f}" x2="{x:.1f}" y2="{p1.sy(summary.mean + summary.ci95):.1f}" stroke="{COLORS[policy]}" stroke-dasharray="{dash[limit]}"/>')
                else:
                    body.append(f'<line class="ci" x1="{x:.1f}" y1="{p1.sy(summary.mean - summary.ci95):.1f}" x2="{x:.1f}" y2="{p1.sy(summary.mean + summary.ci95):.1f}" stroke="{COLORS[policy]}"/>')
                body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{COLORS[policy]}"/>')
            body.append('<polyline fill="none" stroke="{}" stroke-width="2" stroke-dasharray="{}" points="{}"/>'.format(COLORS[policy], dash[limit] if policy == "constrained_fisher" else "none", " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))

    slip_filtered = [row for row in slip_rows if row["policy"] in policies and row["diagnostic_steps"] == "40"]
    sd = summarize(slip_filtered, ["slip_correlation", "policy"], "cumulative_diagnostic_disturbance")
    corrs = sorted({float(row["slip_correlation"]) for row in slip_filtered})
    vals2 = [s.mean + s.ci95 for s in sd.values()] + [s.mean - s.ci95 for s in sd.values()]
    p2 = Panel(690, 90, 370, 310, min(corrs), max(corrs), *pad_range(vals2), "slip correlation", "cumulative disturbance", "B. Correlated slip stress test at 40 steps")
    draw_panel(body, p2)
    for policy in policies:
        pts = []
        for corr in corrs:
            summary = sd[(str(corr), policy)]
            x = p2.sx(corr)
            y = p2.sy(summary.mean)
            pts.append((x, y))
            draw_error_bar(body, p2, corr, summary, COLORS[policy])
        body.append('<polyline fill="none" stroke="{}" stroke-width="2.5" points="{}"/>'.format(COLORS[policy], " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)))
    legend(body, 80, 470, policies)
    caption(body, 350, 455, [
        "Error bars are 95% CIs. Left panel: constrained-Fisher line dash encodes disturbance limit 0.08/0.12/0.18.",
        "Right panel: high slip correlation weakens the paired-null cumulative-disturbance advantage.",
        "Sources: threshold_noise_sweep_results.csv and correlated_slip_sweep_results.csv.",
    ])
    write_svg(out / "fig5_robustness_quantified.svg", 1220, 560, body)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=Path("runs"))
    parser.add_argument("--out", type=Path, default=Path("figures"))
    args = parser.parse_args(argv)

    budget_rows = read_rows(args.runs / "budget_sweep_results.csv")
    threshold_rows = read_rows(args.runs / "threshold_noise_sweep_results.csv")
    slip_rows = read_rows(args.runs / "correlated_slip_sweep_results.csv")

    fig1_budget_metrics(budget_rows, args.out)
    fig2_pareto(budget_rows, args.out)
    fig3_ablation(budget_rows, args.out)
    fig4_trajectory_quant(args.out)
    fig5_robustness(threshold_rows, slip_rows, args.out)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
