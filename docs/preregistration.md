# Internal Preregistration Draft

## Main Hypothesis

Task-neutral diagnostic null probes will identify latent actuator or contact changes with lower task-state disturbance than random probing or task-greedy behavior, while preserving comparable or better post-diagnosis task recovery.

## Primary Metrics

- Parameter error: absolute error over left wheel gain, right wheel gain, and slip.
- Final diagnostic disturbance: Euclidean displacement plus weighted heading drift at the end of the diagnostic phase.
- Maximum diagnostic disturbance: maximum Euclidean displacement plus weighted heading drift reached during diagnosis.
- Cumulative diagnostic disturbance: sum of per-step disturbance from the task start state during diagnosis.
- Recovery distance: final task error after using the diagnosed model for compensation on the true damaged robot.
- Recovery gain: recovery distance of a nominal uncompensated controller minus recovery distance of the diagnosis-conditioned controller.

Maximum and cumulative diagnostic disturbance are the primary task-preservation metrics. Final diagnostic disturbance is retained as a secondary metric because globally cancelling action sequences can hide large transient disruptions.

## Exclusions

Exclude only runs with invalid configuration files, simulator numerical errors, or missing logs. Do not exclude poor-performing trials.

## Stopping Criteria

Run the preregistered number of seeds and damage cases before inspecting aggregate results. Additional exploratory runs must be logged under a separate config and labelled post hoc.

## Reporting Rules

Report null, negative, unstable, and implementation-failure outcomes. Preserve raw CSV logs, configs, code commit hash, and random seeds.

## Amendments

- 2026-07-24: The initial scaffold incorrectly evaluated recovery on the estimated damage model rather than the true damaged robot. The metric was amended before interpreting recovery results.
- 2026-07-24: The initial disturbance metric measured only final displacement. Maximum and cumulative disturbance were added after the `unpaired_null` ablation revealed that final displacement can miss transient task disruption.
- 2026-07-24: An analysis bug in aggregate paired differences for multi-budget sweeps grouped by trial and damage without diagnostic horizon. The raw logs were unaffected; summaries were regenerated after adding `diagnostic_steps` to the pairing key.
