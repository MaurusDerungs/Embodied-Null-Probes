# Paper Working Notes

## Provisional Title

Embodied Null Probes: Embodied Negative Controls for Low-Disturbance Robot Self-Diagnosis

## Current Claim

Paired actions that are predicted to cancel under a nominal robot model can diagnose hidden embodiment changes while occupying a distinct short-horizon Pareto region: less accurate than aggressive system-identification probes, but much less disruptive to task state.

This is a feasibility, boundary-condition, and evaluation-protocol claim, not a performance-superiority claim. A simple disturbance-constrained Fisher baseline often improves parameter error and maximum disturbance, but null probes remain competitive when cumulative disturbance is treated as a primary safety-relevant objective. Under high temporal slip correlation and long horizons, even the cumulative-disturbance advantage can weaken.

## Research Question

Can task-neutral physical action pairs act as embodied negative controls for diagnosing latent actuator and contact changes, and what information-versus-disturbance tradeoff do they expose relative to random probing, task-directed behavior, unpaired actions, and aggressive system-identification probes?

## Hypotheses

- H1: `null_probe` will produce lower maximum and cumulative diagnostic disturbance than action-energy-comparable or stronger exploration baselines.
- H2: `null_probe` will remain Pareto non-dominated when evaluated on parameter error, maximum diagnostic disturbance, and cumulative diagnostic disturbance.
- H3: Breaking local pairwise cancellation while preserving the action set will increase maximum and cumulative disturbance without a commensurate reduction in parameter error.
- H4: Diagnosis-conditioned recovery may improve on nominal control in turn-heavy tasks, but this is exploratory until the recovery controller and task suite are strengthened.

## Current Evidence

- `runs/budget_sweep_summary.md`: `null_probe` and `fisher_grid` are the consistent Pareto policies across 4, 8, 16, 24, and 40 diagnostic steps.
- `runs/budget_sweep_summary.md` after adding `constrained_fisher`: `null_probe` remains Pareto non-dominated at 4, 8, 16, and 24 steps, but is dominated at 40 steps.
- `runs/budget_sweep_summary.md` with three-metric Pareto analysis: `null_probe` remains non-dominated at every tested horizon because constrained Fisher accumulates more disturbance.
- `runs/recovery_waypoint_sweep_summary.md` with three-metric Pareto analysis: `null_probe` remains non-dominated at every tested horizon.
- `runs/threshold_noise_sweep_summary.md`: two-metric analysis keeps `null_probe` non-dominated only at 8 steps, while three-metric analysis keeps it non-dominated at 8, 24, and 40 steps.
- `runs/correlated_slip_sweep_summary.md`: correlated slip preserves the local-cancellation result, but shows that high correlation can erode null-probe cumulative-disturbance advantages at long horizons.
- `unpaired_null` is important: it is close in parameter error but much worse in transient disturbance, supporting local cancellation as the relevant mechanism.

## Negative Or Mixed Results To Preserve

- `fisher_grid` usually estimates hidden parameters better than `null_probe`.
- Straight-goal recovery was too insensitive to diagnose downstream utility.
- Waypoint recovery did not show a clean null-probe advantage.
- Final displacement alone is an inadequate disturbance metric because it misses transient disruption.
- A transparent disturbance-constrained Fisher baseline can outperform null probes once the diagnostic budget is long enough.
- Whether null probes look useful depends strongly on whether cumulative disturbance is considered a primary outcome.
- High temporal slip correlation is a boundary condition where the null-probe advantage is weaker.

## Planned Figures

- Figure 1: Quantified budget curves for parameter error, maximum disturbance, and cumulative disturbance with 95% CIs.
- Figure 2: Parameter error versus maximum diagnostic disturbance Pareto plot with 95% CI bars.
- Figure 3: `null_probe` versus `unpaired_null` cancellation ablation with cumulative-disturbance ratios.
- Figure 4: Representative diagnostic trajectories with numeric trajectory metrics.
- Figure 5: Threshold/noise and correlated-slip robustness with 95% CIs.

## Threats To Validity

- The simulator is intentionally low-dimensional and may overstate the ease of detecting actuator gains.
- Slip is represented as a simple stochastic lateral process; real contact changes have structured temporal correlation.
- The estimator uses a known damage-family grid, so results are about probing protocols, not open-ended model discovery.
- The compensation controller is basic and may underuse the diagnosis.
- Current baselines are simple; a stronger constrained active-system-identification baseline is needed before submission.

## Next Publishable Milestone

Add representative trajectory plots and a formal methods section. The next paper-level question is how to explain the different safety meanings of final, maximum, and cumulative diagnostic disturbance.
