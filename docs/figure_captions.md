# Figure Captions

## Figure 1: Budget Metrics

File: `figures/fig1_budget_metrics.svg`

Mean parameter error, maximum diagnostic disturbance, and cumulative diagnostic disturbance as a function of diagnostic horizon. Error bars show 95% confidence intervals over 60 trials and 4 damage cases per policy/horizon (`n = 240` per plotted point). Lower is better on all three axes. Source data: `runs/budget_sweep_results.csv`.

## Figure 2: Pareto Comparison

File: `figures/fig2_pareto_ci.svg`

Parameter-error versus maximum-disturbance Pareto comparison for horizons 8, 24, and 40. Horizontal and vertical bars show 95% confidence intervals. This two-metric view shows why constrained active probing is a strong baseline; cumulative disturbance is reported separately because it changes the interpretation. Source data: `runs/budget_sweep_results.csv`.

## Figure 3: Cancellation Ablation

File: `figures/fig3_cancellation_ablation.svg`

Comparison between locally paired null probes and an unpaired ablation using the same action multiset. Error bars show 95% confidence intervals. The ratio panel reports `unpaired_null / null_probe` cumulative disturbance, quantifying the effect of local cancellation. Source data: `runs/budget_sweep_results.csv`.

## Figure 4: Representative Trajectory

File: `figures/fig4_trajectory_quantified.svg`

Representative 40-step diagnostic trajectories for one fixed seed under left wheel gain loss. The embedded table reports maximum, cumulative, and final disturbance for the plotted trajectories. This figure is illustrative only; aggregate statistics are reported in Figures 1-3. Generated directly from simulator rollouts.

## Figure 5: Robustness

File: `figures/fig5_robustness_quantified.svg`

Robustness of cumulative disturbance under constrained-Fisher disturbance thresholds, observation noise, and temporally correlated slip. Error bars show 95% confidence intervals. The left panel fixes observation noise at 0.01 and varies the constrained-Fisher threshold. The right panel fixes horizon at 40 and varies slip correlation. Source data: `runs/threshold_noise_sweep_results.csv` and `runs/correlated_slip_sweep_results.csv`.
