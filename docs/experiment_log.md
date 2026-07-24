# Experiment Log

## Loop 001: Repair Core Metrics

Date: 2026-07-24

Motivation: The initial scaffold could estimate damage, but its recovery metric evaluated the controller on the estimated damage itself. That cannot test whether diagnosis helps a true damaged robot. The diagnostic disturbance metric also measured only final displacement, which is vulnerable to globally cancelling probes that still cause large transient deviations.

Changes:

- Added diagnosis-conditioned compensation: greedy wheel commands are divided by the estimated left and right gains, clipped to command limits, and evaluated under the true damage.
- Added posterior entropy and posterior confidence from a grid likelihood estimator.
- Added action energy, maximum diagnostic disturbance, and cumulative diagnostic disturbance.
- Added `unpaired_null`, an ablation that uses the same action set as `null_probe` but breaks local pairwise cancellation.

Evidence:

- Base run: `runs/base_results.csv`
- Summary: `runs/base_summary.md`

Interpretation:

- `null_probe` has much lower maximum and cumulative diagnostic disturbance than `random_probe`, `task_greedy`, and `fisher_grid`.
- `fisher_grid` usually has lower parameter error, so null probing is not a best-estimator story.
- `unpaired_null` has similar parameter error to `null_probe`, but much higher maximum and cumulative disturbance. This supports the specific cancellation mechanism more than a generic action-distribution explanation.
- Recovery gain is small and noisy on the straight-goal task, so straight-goal recovery should not be used as a primary claim.

Decision: Preserve the main claim as a tradeoff between diagnostic information and task-state disturbance. Add budget sweeps before making any stronger statement.

## Loop 002: Diagnostic Budget Sweep

Date: 2026-07-24

Motivation: A single 24-step result could be an artifact of probe length. The next test asks whether the parameter-error/disturbance tradeoff persists across diagnostic horizons.

Configuration:

- Config: `configs/budget_sweep.json`
- Horizons: 4, 8, 16, 24, 40 diagnostic steps
- Trials: 60 per damage case, horizon, and policy
- Damage cases: left gain loss, right gain loss, symmetric low power, high slip
- Policies: `null_probe`, `unpaired_null`, `random_probe`, `task_greedy`, `fisher_grid`

Evidence:

- Raw results: `runs/budget_sweep_results.csv`
- Summary: `runs/budget_sweep_summary.md`
- Logged trials: 6,000

Main observations:

- `null_probe` remains Pareto non-dominated at every horizon when comparing mean parameter error and mean maximum diagnostic disturbance.
- `fisher_grid` is the other consistent Pareto policy: it estimates better, but at substantially higher disturbance.
- `unpaired_null` is dominated at every horizon in this sweep. It usually gives similar parameter error to `null_probe` with far higher max and cumulative disturbance.
- `random_probe` is dominated in the tested horizons, suggesting that the effect is not merely low action energy or generic exploration.

Interpretation:

The strongest current evidence is not that null probes estimate damage best. The evidence is that paired task-neutral probes expose a reproducible Pareto corner: less information than aggressive system identification, but substantially less task disruption.

Decision: Treat diagnostic null actions as an evaluation protocol and design principle, not as a performance-optimizing controller.

## Loop 003: Harder Recovery Task

Date: 2026-07-24

Motivation: The straight-goal task showed almost no useful recovery variation. A square waypoint task should make asymmetric wheel-gain estimates matter more because errors accumulate over turns.

Configuration:

- Config: `configs/recovery_waypoint_sweep.json`
- Recovery task: `square_waypoints`
- Horizons: 8, 16, 24, 40 diagnostic steps
- Trials: 60 per damage case, horizon, and policy
- Logged trials: 4,800

Evidence:

- Raw results: `runs/recovery_waypoint_sweep_results.csv`
- Summary: `runs/recovery_waypoint_sweep_summary.md`

Main observations:

- Recovery gain is more visible than in the straight-goal task, but it does not cleanly favor `null_probe`.
- `task_greedy` sometimes has higher recovery gain, but it causes much larger diagnostic disturbance and has worse parameter error.
- `fisher_grid` often improves recovery slightly more than `null_probe`, consistent with its lower parameter error, but at much higher disturbance.
- `null_probe` remains Pareto non-dominated for parameter error versus maximum diagnostic disturbance at every tested horizon.
- At 40 steps on the waypoint task, `unpaired_null` also appears on the Pareto set because its mean parameter error is nearly identical to `null_probe`, though its disturbance remains substantially higher.

Interpretation:

The downstream-controller result is mixed. The current simulator supports a paper claim about low-disturbance diagnosis, not a claim that null probes produce superior task recovery. This is still publishable if framed as an embodied negative-control evaluation protocol with a clear disturbance/information tradeoff.

Decision: Next experiments should test robustness of the Pareto claim under changes to observation noise, damage granularity, and non-cancelling terrain/contact effects. Do not tune the controller to manufacture a recovery win.

## Loop 004: Disturbance-Constrained Fisher Baseline

Date: 2026-07-24

Motivation: The strongest challenge to diagnostic null actions is not random exploration. It is an active system-identification policy that explicitly respects a task-disturbance budget. If such a baseline dominates null probes, the hand-designed null-action idea should be reported as a limited or failed intervention rather than promoted as a superior method.

Changes:

- Added `constrained_fisher`, a transparent adaptive baseline.
- At each diagnostic step it selects a command from a fixed wheel-command grid.
- Candidate actions are rejected if nominal one-step prediction exceeds `max_predicted_diagnostic_disturbance`.
- Remaining candidates are scored with a simple information proxy based on wheel-command magnitude and differential turn excitation.

Configuration:

- Budget sweep config: `configs/budget_sweep.json`
- Waypoint sweep config: `configs/recovery_waypoint_sweep.json`
- Disturbance threshold: `max_predicted_diagnostic_disturbance = 0.12`

Evidence:

- Updated budget sweep: `runs/budget_sweep_results.csv`
- Updated budget summary: `runs/budget_sweep_summary.md`
- Updated waypoint sweep: `runs/recovery_waypoint_sweep_results.csv`
- Updated waypoint summary: `runs/recovery_waypoint_sweep_summary.md`
- Logged trials after adding the baseline: 7,200 for the budget sweep and 5,760 for the waypoint sweep.

Main observations:

- `constrained_fisher` reduces parameter error relative to `null_probe` with only a small increase in maximum disturbance in most settings.
- In the budget sweep, `null_probe` remains Pareto non-dominated at 4, 8, 16, and 24 steps, but is dominated at 40 steps.
- In the waypoint sweep, `null_probe` remains Pareto non-dominated at 8 and 16 steps, but is dominated at 24 and 40 steps.
- `unpaired_null` remains a useful ablation: it does not consistently improve parameter error over `null_probe`, but it substantially increases transient disturbance.

Interpretation:

The central result is now sharper and more credible: diagnostic null actions appear useful as a short-horizon, hand-designed embodied negative-control probe, but a simple constrained active baseline can catch up or dominate as the diagnostic budget grows. This boundary condition is likely more publishable than a broad positive claim.

Decision:

- Reframe the paper around "when do embodied negative controls remain competitive with constrained active probing?"
- Treat long-horizon domination by `constrained_fisher` as a negative result to preserve.
- Next loop should vary the disturbance threshold and observation noise to see whether the crossover horizon is stable.

## Loop 005: Threshold And Observation-Noise Robustness

Date: 2026-07-24

Motivation: The `constrained_fisher` result might depend on one disturbance threshold and one observation-noise level. The robustness sweep tests whether the null-versus-constrained crossover remains visible across sensor quality and disturbance-budget assumptions.

Configuration:

- Config: `configs/threshold_noise_sweep.json`
- Horizons: 8, 24, 40 diagnostic steps
- Observation noise: 0.005, 0.01, 0.03
- Disturbance limits for `constrained_fisher`: 0.08, 0.12, 0.18
- Policies: `null_probe`, `unpaired_null`, `fisher_grid`, `constrained_fisher`
- Logged trials: 17,280

Evidence:

- Raw results: `runs/threshold_noise_sweep_results.csv`
- Summary: `runs/threshold_noise_sweep_summary.md`

Main observations:

- Across all robustness conditions, `constrained_fisher` has lower mean parameter error than `null_probe`.
- `constrained_fisher` can also match or beat `null_probe` on maximum disturbance, especially at tighter disturbance limits and longer horizons.
- `null_probe` consistently has lower cumulative disturbance than `constrained_fisher` in the robustness detail table.
- Two-metric Pareto analysis over parameter error and max disturbance makes `null_probe` non-dominated only at 8 steps.
- Three-metric Pareto analysis over parameter error, max disturbance, and cumulative disturbance keeps `null_probe` non-dominated at 8, 24, and 40 steps.
- `unpaired_null` remains dominated, strengthening the interpretation that local cancellation is the important ingredient.

Interpretation:

The current paper should not claim that null probes beat active low-disturbance system identification. The more accurate claim is that diagnostic null actions expose a different safety-relevant objective: they minimize accumulated task-state disturbance while preserving enough diagnostic signal to stay on the three-metric Pareto frontier. This is a narrower but more novel and falsifiable contribution.

Decision:

- Make cumulative diagnostic disturbance a first-class metric and not a secondary afterthought.
- Frame `constrained_fisher` as the main positive-control baseline.
- Next technical step should generate representative trajectory plots and add a second simulator perturbation where contact/slip is temporally correlated, because the current slip model is too simple.

## Loop 006: Temporally Correlated Slip Stress Test

Date: 2026-07-24

Motivation: The original slip process was independent at each step. Real contact disturbances can persist, so the estimator should be stress-tested under a misspecified temporal contact model.

Changes:

- Added `slip_correlation` to `SimConfig`.
- Preserved `slip_correlation = 0.0` as the default, matching the prior independent-slip process.
- Used variance-preserving autoregressive slip bias so higher correlation changes temporal structure rather than simply shrinking slip magnitude.

Configuration:

- Config: `configs/correlated_slip_sweep.json`
- Horizons: 8, 24, 40 diagnostic steps
- Slip correlations: 0.0, 0.5, 0.85
- Policies: `null_probe`, `unpaired_null`, `fisher_grid`, `constrained_fisher`
- Logged trials: 7,200

Evidence:

- Raw results: `runs/correlated_slip_sweep_results.csv`
- Summary: `runs/correlated_slip_sweep_summary.md`

Main observations:

- `constrained_fisher` retains lower mean parameter error than `null_probe` overall.
- `null_probe` has lower cumulative disturbance than `constrained_fisher` at 8 and 24 steps across tested slip correlations.
- At 40 steps with high slip correlation, the cumulative-disturbance advantage weakens and can reverse.
- Two-metric Pareto analysis favors `constrained_fisher` at 24 steps; three-metric Pareto analysis keeps `null_probe` non-dominated at 24 and 40 steps.
- `unpaired_null` remains dominated, preserving the evidence that local cancellation matters.

Interpretation:

The core phenomenon is robust enough to keep: pairwise cancellation reduces accumulated diagnostic disturbance relative to unpaired and aggressive baselines. The stronger claim that null probes are always best for cumulative disturbance is false under high temporal slip correlation and longer horizons.

Decision:

- Current contribution should be framed as a boundary-condition study: diagnostic null actions are a simple embodied negative-control baseline that reveals an information, max-disturbance, and cumulative-disturbance tradeoff.
- The next paper artifact should be trajectory visualizations and a formal methods section, not more broad sweeps.
