# Embodied Null Probes: Embodied Negative Controls for Low-Disturbance Robot Self-Diagnosis

Status: first complete research draft  
Date: 2026-07-24

## Abstract

Robots often need to identify hidden changes in their embodiment, such as actuator degradation or contact shifts, without first disrupting the task they are trying to preserve. Active system-identification methods deliberately excite the system to collect informative data, but this can move the robot far from its task state. We study an alternative intervention: diagnostic null actions, paired physical actions predicted by a nominal self-model to cancel locally. The intended contribution is not higher identification accuracy, but a test of whether embodied negative controls expose a distinct information-disturbance tradeoff. In a minimal differential-drive simulator with hidden wheel-gain and slip changes, we compare paired null probes against unpaired action ablations, random exploration, task-greedy behavior, Fisher-grid excitation, and a disturbance-constrained Fisher baseline. Across 37,440 logged trials, null probes are not the best estimators; Fisher-style baselines usually achieve lower parameter error. However, paired null probes consistently reduce cumulative diagnostic disturbance relative to unpaired and aggressive probes, and remain on the three-metric Pareto frontier when parameter error, maximum disturbance, and cumulative disturbance are jointly considered. Stress tests with observation noise and temporally correlated slip identify boundary conditions: constrained active probing can dominate on parameter error and maximum disturbance, and high slip correlation weakens null-probe advantages at long horizons. These results support diagnostic null actions as a reproducible embodied negative-control protocol and a useful negative-space benchmark for low-disturbance robot self-diagnosis.

## 1. Introduction

Robots deployed outside tightly controlled settings must adapt when their bodies or contacts change. A wheel may lose torque, terrain may become slippery, a manipulator joint may drift, or a leg may be damaged. Existing recovery approaches often ask how a robot can find a new behavior after damage, or how it can actively collect data for system identification. Those questions are important, but they leave a smaller measurement question underexplored: can the robot test whether its embodiment has changed without substantially disturbing the task state it is trying to protect?

This draft proposes and evaluates diagnostic null actions. A diagnostic null action is a short sequence of physical commands whose net task effect should be near zero under a nominal self-model. If the robot is intact, executing a forward command followed immediately by the inverse command should nearly return it to the same task state. If a hidden actuator or contact parameter has changed, the residual motion contains diagnostic information. In this sense, the paired action functions as an embodied negative control: it is designed not to change the task-relevant state, and deviations from that expected null effect become evidence of hidden physical change.

The goal is deliberately not to beat active system identification on parameter estimation. A strong active baseline should often estimate better, because it is free to excite informative directions. The scientific question is whether pairwise cancellation defines a different safety-relevant Pareto point: less information, but less accumulated diagnostic disturbance.

## 2. Related Work

Damage recovery work shows that robots can adapt after body changes. Cully et al. introduced intelligent trial-and-error adaptation for damaged robots, using behavior-performance maps to recover in minutes without explicit damage diagnosis [Cully2015]. Chatzilygeroudis et al. extended this line with reset-free trial-and-error learning for damage recovery [Chatzilygeroudis2016]. This project differs by making diagnosis itself the object of study and by measuring how much the diagnostic intervention perturbs task state.

Active system-identification methods collect informative real-world data to refine simulators and improve transfer. ASID is a recent example that plans real exploration policies to identify physical parameters for manipulation [Memmel2024]. We use a deliberately simple constrained-Fisher baseline as the main positive control. The key comparison is not against weak random exploration but against a baseline that explicitly tries to obtain information under a disturbance limit.

Causal and interventional robotics benchmarks such as CausalWorld provide controlled environments for causal structure and transfer learning [Ahmed2020]. Recent interventional RL work uses probing phases to identify controllable observation dimensions [IBD2026]. Diagnostic null actions are adjacent to this tradition but use the robot body itself as the negative-control instrument: nominally cancelling actions are expected to have no task effect, so residual effects reveal hidden embodiment mismatch.

Failure discovery and safe exploration research studies where robot policies fail and how exploration can be constrained. RoboFail/RoboMD-style work searches for failure modes in learned manipulation policies [RoboFail2024], while safe RL surveys formalize risk-aware exploration [Garcia2015]. This project focuses on a narrower axis: diagnostic information per unit of task-state disturbance.

The term negative control comes from causal inference and experimental design. Lipsitch, Tchetgen Tchetgen, and Cohen describe negative controls as tools for detecting confounding and bias using variables or outcomes that should not be affected in the target way [Lipsitch2010]. Here the analogy is embodied: the "should not change" object is the robot's task state under a nominal physical model.

## 3. Research Question And Hypotheses

Research question: Can paired, nominally cancelling physical actions act as embodied negative controls for diagnosing hidden actuator and contact changes, and what tradeoff do they expose relative to random probing, task-greedy behavior, unpaired actions, Fisher-grid excitation, and disturbance-constrained active probing?

Hypotheses:

- H1: Paired null probes will produce lower maximum and cumulative diagnostic disturbance than unpaired, random, task-greedy, and Fisher-grid baselines.
- H2: Paired null probes will remain Pareto non-dominated when evaluated jointly on parameter error, maximum diagnostic disturbance, and cumulative diagnostic disturbance.
- H3: Breaking local pairwise cancellation while preserving the same action set will increase maximum and cumulative disturbance without a commensurate improvement in parameter error.
- H4: Diagnosis-conditioned recovery may improve over nominal control in turn-heavy tasks, but recovery is secondary because the current controller may underuse diagnostic estimates.

Falsification criteria:

- H1 fails if another comparable policy has no larger max or cumulative disturbance while matching or improving parameter error.
- H2 fails if constrained active probing dominates null probes on all three metrics across horizons and noise/contact conditions.
- H3 fails if `unpaired_null` matches `null_probe` on cumulative disturbance or consistently improves parameter error enough to justify the added disturbance.
- H4 remains exploratory unless the recovery controller and task suite are strengthened.

## 4. Method

### 4.1 Simulator

The simulator is intentionally minimal: a differential-drive robot with state `(x, y, theta)`, wheel commands `(left, right)`, hidden left and right gain parameters, and a slip parameter. The simulator supports process noise, observation noise, and an optional variance-preserving autoregressive slip-bias process.

Hidden damage cases:

- `left_gain_loss`: left wheel gain 0.62, right wheel gain 1.0, slip 0.02.
- `right_gain_loss`: left wheel gain 1.0, right wheel gain 0.62, slip 0.02.
- `symmetric_low_power`: both gains 0.72, slip 0.02.
- `high_slip`: both gains 1.0, slip 0.20.

This simulator is not presented as a high-fidelity physical model. Its purpose is to isolate the diagnostic intervention and produce a falsifiable first study.

### 4.2 Diagnostic Policies

`null_probe`: repeated paired commands that should locally cancel under nominal dynamics:

- forward, backward;
- clockwise turn, counterclockwise turn;
- asymmetric arc, inverse asymmetric arc.

`unpaired_null`: the same action multiset as `null_probe`, but reordered so local cancellation is broken. This is the key mechanism ablation.

`random_probe`: random wheel commands sampled uniformly from a matched command range.

`task_greedy`: normal goal-directed behavior during the diagnostic phase.

`fisher_grid`: repeated high-excitation wheel commands selected from a fixed grid.

`constrained_fisher`: an adaptive positive-control baseline. At each step, it evaluates a wheel-command grid under the nominal model, rejects commands whose predicted one-step disturbance exceeds a configurable threshold, and selects the remaining command with a simple Fisher-like excitation proxy.

### 4.3 Estimator

The estimator is a grid likelihood over candidate left gain, right gain, and slip values. Candidate transition losses compare observed one-step changes with mean differential-drive predictions and a slip-dependent lateral variance term. The estimator reports:

- best grid-cell estimate;
- parameter error: absolute error over left gain, right gain, and slip;
- posterior entropy;
- posterior confidence.

The estimator is intentionally simple. The experiments are about the probing protocol, not about maximizing estimator sophistication.

### 4.4 Metrics

Primary metrics:

- Parameter error: `|estimated_left - true_left| + |estimated_right - true_right| + |estimated_slip - true_slip|`.
- Final diagnostic disturbance: displacement plus weighted heading drift after the diagnostic phase.
- Maximum diagnostic disturbance: largest task-state deviation reached during the diagnostic phase.
- Cumulative diagnostic disturbance: sum of per-step task-state deviations during the diagnostic phase.

Secondary metrics:

- Recovery distance: final task error after compensating a greedy controller with the diagnosed gain estimate and evaluating under true damage.
- Recovery gain: nominal-controller recovery distance minus diagnosis-conditioned recovery distance.

The distinction among final, maximum, and cumulative disturbance is central. Final disturbance can hide a large excursion that later cancels. Maximum disturbance captures peak excursion. Cumulative disturbance measures integrated task disruption.

## 5. Experiments

### 5.1 Main Budget Sweep

Config: `configs/budget_sweep.json`  
Raw log: `runs/budget_sweep_results.csv`  
Summary: `runs/budget_sweep_summary.md`  
Trials: 7,200 rows.

Diagnostic horizons: 4, 8, 16, 24, and 40 steps.  
Policies: all six policies.  
Damage cases: all four hidden damage cases.

### 5.2 Waypoint Recovery Sweep

Config: `configs/recovery_waypoint_sweep.json`  
Raw log: `runs/recovery_waypoint_sweep_results.csv`  
Summary: `runs/recovery_waypoint_sweep_summary.md`  
Trials: 5,760 rows.

The recovery task is a square waypoint route. This task was added after straight-line recovery proved too insensitive.

### 5.3 Threshold And Noise Robustness

Config: `configs/threshold_noise_sweep.json`  
Raw log: `runs/threshold_noise_sweep_results.csv`  
Summary: `runs/threshold_noise_sweep_summary.md`  
Trials: 17,280 rows.

Swept variables:

- diagnostic steps: 8, 24, 40;
- observation noise: 0.005, 0.01, 0.03;
- constrained-Fisher disturbance limit: 0.08, 0.12, 0.18.

### 5.4 Correlated Slip Stress Test

Config: `configs/correlated_slip_sweep.json`  
Raw log: `runs/correlated_slip_sweep_results.csv`  
Summary: `runs/correlated_slip_sweep_summary.md`  
Trials: 7,200 rows.

Swept variables:

- diagnostic steps: 8, 24, 40;
- slip correlation: 0.0, 0.5, 0.85.

This test intentionally makes the simulator less aligned with the estimator, because the estimator does not explicitly model temporally correlated slip.

## 6. Results

### 6.1 Aggregate Main Sweep

In the main budget sweep, `null_probe` is not the most accurate estimator. Mean parameter error is lower for `fisher_grid` (0.0542 +/- 0.0033) and `constrained_fisher` (0.0591 +/- 0.0043) than for `null_probe` (0.0709 +/- 0.0042).

However, null probes produce substantially lower disturbance. Mean cumulative disturbance is:

| Policy | Parameter error | Max disturbance | Cumulative disturbance |
|---|---:|---:|---:|
| `null_probe` | 0.0709 +/- 0.0042 | 0.1039 +/- 0.0022 | 1.1416 +/- 0.0636 |
| `constrained_fisher` | 0.0591 +/- 0.0043 | 0.1091 +/- 0.0015 | 1.3756 +/- 0.0683 |
| `fisher_grid` | 0.0542 +/- 0.0033 | 0.2679 +/- 0.0085 | 3.2469 +/- 0.2070 |
| `unpaired_null` | 0.0728 +/- 0.0043 | 0.2423 +/- 0.0029 | 2.4555 +/- 0.1063 |
| `random_probe` | 0.0936 +/- 0.0053 | 0.2531 +/- 0.0079 | 3.3121 +/- 0.2000 |

The `unpaired_null` ablation is especially important: it has similar parameter error but much higher max and cumulative disturbance. This supports H3 and isolates local cancellation as the relevant mechanism.

### 6.2 Budget Dependence

At 8 diagnostic steps, `null_probe` has higher parameter error than `constrained_fisher` but lower max and cumulative disturbance:

| Policy | Parameter error | Max disturbance | Cumulative disturbance |
|---|---:|---:|---:|
| `null_probe` | 0.0939 +/- 0.0106 | 0.0903 +/- 0.0027 | 0.3826 +/- 0.0156 |
| `constrained_fisher` | 0.0710 +/- 0.0105 | 0.1036 +/- 0.0034 | 0.4997 +/- 0.0247 |

At 24 steps, `constrained_fisher` nearly matches max disturbance and estimates better, but null probes still accumulate less disturbance:

| Policy | Parameter error | Max disturbance | Cumulative disturbance |
|---|---:|---:|---:|
| `null_probe` | 0.0502 +/- 0.0061 | 0.1132 +/- 0.0049 | 1.4465 +/- 0.0707 |
| `constrained_fisher` | 0.0455 +/- 0.0073 | 0.1141 +/- 0.0032 | 1.7794 +/- 0.0724 |

At 40 steps, `constrained_fisher` beats `null_probe` on parameter error and maximum disturbance, but `null_probe` remains lower on cumulative disturbance:

| Policy | Parameter error | Max disturbance | Cumulative disturbance |
|---|---:|---:|---:|
| `null_probe` | 0.0377 +/- 0.0050 | 0.1351 +/- 0.0064 | 2.8338 +/- 0.1465 |
| `constrained_fisher` | 0.0348 +/- 0.0055 | 0.1204 +/- 0.0030 | 3.2607 +/- 0.1200 |

This supports a three-metric version of H2, but not a two-metric version using only parameter error and maximum disturbance.

### 6.3 Recovery Is Secondary And Mixed

The recovery task did not produce a clean null-probe advantage. The waypoint sweep shows `fisher_grid` and `constrained_fisher` often obtain comparable or higher recovery gains, but at higher diagnostic disturbance. This is a negative result and should be preserved. The current controller is too simple to support a strong claim that diagnostic null actions improve downstream control.

### 6.4 Robustness To Noise And Thresholds

The threshold/noise sweep confirms that `constrained_fisher` is a strong competitor. Across all robustness conditions, it has lower mean parameter error than `null_probe`:

| Policy | Parameter error | Max disturbance | Cumulative disturbance |
|---|---:|---:|---:|
| `null_probe` | 0.0857 +/- 0.0031 | 0.1157 +/- 0.0015 | 1.5759 +/- 0.0390 |
| `constrained_fisher` | 0.0754 +/- 0.0031 | 0.1107 +/- 0.0012 | 1.8702 +/- 0.0432 |

Two-metric Pareto analysis over parameter error and max disturbance keeps `null_probe` non-dominated only at 8 steps. Three-metric Pareto analysis over parameter error, maximum disturbance, and cumulative disturbance keeps `null_probe` non-dominated at 8, 24, and 40 steps.

This result is central: diagnostic null actions look useful only if cumulative task disturbance is treated as a primary safety-relevant metric.

### 6.5 Correlated Slip Boundary Condition

The correlated slip stress test shows that the result is not unconditional. At slip correlation 0.85 and 40 diagnostic steps:

| Policy | Parameter error | Max disturbance | Cumulative disturbance |
|---|---:|---:|---:|
| `null_probe` | 0.0450 +/- 0.0060 | 0.1775 +/- 0.0199 | 3.6817 +/- 0.4103 |
| `constrained_fisher` | 0.0427 +/- 0.0054 | 0.1216 +/- 0.0033 | 3.3770 +/- 0.1423 |

Here `constrained_fisher` is better on all three means. This falsifies any broad claim that null probes always minimize cumulative disturbance. The more defensible conclusion is that pairwise cancellation is useful under nominal and moderate contact-memory settings, but persistent contact errors can break the advantage at long horizons.

## 7. Figures

Generated figures:

- Figure 1: `figures/fig1_budget_metrics.svg`. Horizon curves for parameter error, maximum diagnostic disturbance, and cumulative diagnostic disturbance. Points are means; error bars are 95% CIs over 60 trials x 4 damage cases per policy/horizon.
- Figure 2: `figures/fig2_pareto_ci.svg`. Parameter-error versus maximum-disturbance Pareto plot with horizontal and vertical 95% CI bars.
- Figure 3: `figures/fig3_cancellation_ablation.svg`. Paired-null versus unpaired-null ablation. The ratio panel quantifies how much additional cumulative disturbance is caused by breaking local cancellation.
- Figure 4: `figures/fig4_trajectory_quantified.svg`. Representative 40-step diagnostic trajectories with a table of max, cumulative, and final disturbance for the shown seed.
- Figure 5: `figures/fig5_robustness_quantified.svg`. Robustness to constrained-Fisher disturbance threshold, observation noise, and temporally correlated slip. Error bars are 95% CIs.

The figures are generated directly from raw CSV logs by `src/diagnostic_null_actions/make_figures.py`.

## 8. Discussion

The initial intuition was that paired null actions might provide diagnostic information with little task disruption. The experiments support a narrower version of that intuition. Pairing matters: using the same actions without local cancellation greatly increases transient and cumulative disturbance. Null probes are also substantially less disruptive than random, task-greedy, and unconstrained Fisher-grid probing.

The stronger baseline changes the story. Once an active system-identification policy is constrained by predicted disturbance, it can match or beat null probes on parameter error and maximum disturbance. This prevents a simplistic "null probes are best" conclusion. Instead, the contribution is an evaluation protocol and boundary-condition result: final displacement, maximum displacement, and cumulative displacement produce different conclusions about diagnostic safety.

The most scientifically useful result may be the failure mode. If reviewers expect active system identification to dominate hand-designed probes, the results partially agree. It dominates on estimation and often on maximum disturbance. But it accumulates more disturbance in many conditions, while unpaired null actions reveal that local cancellation is not merely aesthetic; it changes the disturbance profile.

## 9. Limitations

The simulator is low dimensional. It does not model wheel inertia, saturation dynamics beyond command clipping, actuator heating, terrain geometry, perception failures, or closed-loop obstacle avoidance.

The estimator assumes a fixed candidate family. It is not open-ended self-model discovery.

The constrained-Fisher baseline is simple. A stronger model-predictive information-gain baseline may reduce cumulative disturbance and dominate null probes more often.

Recovery control is underdeveloped. Recovery results should not be used as the main contribution.

The novelty claim is provisional. Similar ideas may exist under terms such as reversible probes, undo actions, safe excitation, null-space exploration, self-test maneuvers, or low-impact probing.

## 10. Ethics And Safety

All current experiments are simulated. No physical robot was operated.

A future hardware validation should include:

- low-speed differential-drive platform;
- bounded diagnostic area;
- mechanical emergency stop;
- software stop on position or heading limit;
- maximum wheel command and acceleration limits;
- human supervision;
- no operation near people, animals, public infrastructure, or fragile equipment;
- logging of all commands and states;
- predeclared abort thresholds for maximum displacement and cumulative disturbance.

The method is intended for diagnosis and safety evaluation. It should not be deployed as an autonomous self-modification system without hardware-specific hazard analysis.

## 11. Reproducibility

Run from repository root:

```bash
PYTHONPATH=src python -m diagnostic_null_actions.run_experiment configs/base.json
PYTHONPATH=src python -m diagnostic_null_actions.run_sweep configs/budget_sweep.json
PYTHONPATH=src python -m diagnostic_null_actions.run_sweep configs/recovery_waypoint_sweep.json
PYTHONPATH=src python -m diagnostic_null_actions.run_sweep configs/threshold_noise_sweep.json
PYTHONPATH=src python -m diagnostic_null_actions.run_sweep configs/correlated_slip_sweep.json
PYTHONPATH=src python -m diagnostic_null_actions.analyze_results runs/budget_sweep_results.csv --out runs/budget_sweep_summary.md
PYTHONPATH=src python -m diagnostic_null_actions.make_figures --runs runs --out figures
```

Primary source files:

- `src/diagnostic_null_actions/sim.py`
- `src/diagnostic_null_actions/policies.py`
- `src/diagnostic_null_actions/run_experiment.py`
- `src/diagnostic_null_actions/run_sweep.py`
- `src/diagnostic_null_actions/analyze_results.py`
- `src/diagnostic_null_actions/make_figures.py`

Primary documentation:

- `docs/preregistration.md`
- `docs/experiment_log.md`
- `docs/references_and_novelty.md`
- `docs/paper_working_notes.md`

## 12. Conclusion

Diagnostic null actions are not a replacement for active system identification. They are a simple embodied negative-control protocol that makes a different safety question measurable: how much task-state disturbance must a robot accumulate to obtain useful diagnostic evidence?

The current evidence supports three conclusions:

1. Pairwise cancellation reduces accumulated diagnostic disturbance relative to unpaired use of the same actions.
2. Constrained active probing is a strong baseline and can dominate null probes on parameter error and maximum disturbance.
3. Cumulative disturbance changes the interpretation and keeps null probes scientifically relevant as a Pareto baseline under several conditions.

The publishable contribution is therefore not a new high-performing controller. It is a reproducible feasibility study and boundary-condition analysis for embodied negative controls in robot self-diagnosis.

## References

[Ahmed2020] Ahmed et al. "CausalWorld: A Robotic Manipulation Benchmark for Causal Structure and Transfer Learning." arXiv 2020. https://arxiv.org/abs/2010.04296

[Chatzilygeroudis2016] Chatzilygeroudis et al. "Reset-free Trial-and-Error Learning for Robot Damage Recovery." arXiv 2016. https://arxiv.org/abs/1610.04213

[Cully2015] Cully, Clune, Tarapore, and Mouret. "Robots that can adapt like animals." Nature 2015 / arXiv 2014. https://arxiv.org/abs/1407.3501

[Garcia2015] Garcia and Fernandez. "A Comprehensive Survey on Safe Reinforcement Learning." JMLR 2015. https://www.jmlr.org/papers/volume16/garcia15a/garcia15a.pdf

[IBD2026] "Interventional Boundary Discovery for Reinforcement Learning." arXiv 2026. https://arxiv.org/html/2603.18257

[Lipsitch2010] Lipsitch, Tchetgen Tchetgen, and Cohen. "Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies." Epidemiology 2010. https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/

[Memmel2024] Memmel et al. "ASID: Active Exploration for System Identification in Robotic Manipulation." arXiv 2024. https://arxiv.org/abs/2404.12308

[OpenX2023] Open X-Embodiment Collaboration. "Open X-Embodiment: Robotic Learning Datasets and RT-X Models." arXiv 2023. https://arxiv.org/abs/2310.08864

[RoboFail2024] "RoboFail: Analyzing Failures in Robot Learning Policies." arXiv 2024. https://arxiv.org/html/2412.02818v1
