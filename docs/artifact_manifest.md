# Artifact Manifest

## Manuscript And Documentation

| Artifact | Purpose |
|---|---|
| `docs/paper_draft.md` | Full first manuscript draft. |
| `docs/references_and_novelty.md` | Prior-art positioning, novelty boundary, and search limitations. |
| `docs/experiment_log.md` | Chronological research loop record, including corrections and negative results. |
| `docs/preregistration.md` | Internal hypothesis, metrics, exclusions, amendments, and reporting rules. |
| `docs/paper_working_notes.md` | Current claim, planned figures, threats to validity, and next milestone. |
| `docs/figure_captions.md` | Publication-ready captions for the quantified figures. |
| `docs/github_release_checklist.md` | Repository naming, topics, release notes, and pre-publication checklist. |

## Code

| Artifact | Purpose |
|---|---|
| `src/diagnostic_null_actions/sim.py` | Differential-drive simulator with actuator gains, slip, noise, and correlated slip. |
| `src/diagnostic_null_actions/policies.py` | Fixed diagnostic policy definitions. |
| `src/diagnostic_null_actions/run_experiment.py` | Single-config experiment runner and estimator. |
| `src/diagnostic_null_actions/run_sweep.py` | Cartesian sweep runner over config fields. |
| `src/diagnostic_null_actions/analyze_results.py` | Summary tables, paired differences, Pareto checks. |
| `src/diagnostic_null_actions/make_figures.py` | Dependency-free SVG figure generation. |

## Configurations

| Config | Rows | Purpose |
|---|---:|---|
| `configs/base.json` | 960 | Small sanity run across all policies and damage cases. |
| `configs/budget_sweep.json` | 7,200 | Main diagnostic-horizon sweep. |
| `configs/recovery_waypoint_sweep.json` | 5,760 | Secondary recovery task with square waypoints. |
| `configs/threshold_noise_sweep.json` | 17,280 | Robustness over observation noise and constrained-Fisher disturbance threshold. |
| `configs/correlated_slip_sweep.json` | 7,200 | Stress test with temporally correlated contact/slip perturbations. |

Paper-scale evidence excludes the base sanity run and contains 37,440 rows. Including the base run, the repository contains 38,400 raw experiment rows.

## Raw Results And Summaries

| Raw log | Summary |
|---|---|
| `runs/base_results.csv` | `runs/base_summary.md` |
| `runs/budget_sweep_results.csv` | `runs/budget_sweep_summary.md` |
| `runs/recovery_waypoint_sweep_results.csv` | `runs/recovery_waypoint_sweep_summary.md` |
| `runs/threshold_noise_sweep_results.csv` | `runs/threshold_noise_sweep_summary.md` |
| `runs/correlated_slip_sweep_results.csv` | `runs/correlated_slip_sweep_summary.md` |

## Figures

| Figure | Purpose |
|---|---|
| `figures/fig1_budget_metrics.svg` | Horizon curves for parameter error, maximum disturbance, and cumulative disturbance with 95% CIs. |
| `figures/fig2_pareto_ci.svg` | Parameter-error vs maximum-disturbance Pareto plot with 95% CI bars. |
| `figures/fig3_cancellation_ablation.svg` | Paired vs unpaired null-probe ablation with cumulative disturbance ratios. |
| `figures/fig4_trajectory_quantified.svg` | Representative trajectory plot with numeric trajectory metrics. |
| `figures/fig5_robustness_quantified.svg` | Threshold/noise and correlated-slip robustness with 95% CIs. |

## Verification Commands

```bash
PYTHONPATH=src python -m compileall -q src tests
PYTHONPATH=src python -m diagnostic_null_actions.make_figures --runs runs --out figures
```

`pytest` is not required by the package and was not installed in the current environment. The smoke test was executed directly through the standard library.
