# Experiment Summary

Input: `runs/base_results.csv`
Rows: 960

## Policy Means

| Policy | n | Param error | Entropy | Final disturbance | Max disturbance | Cumulative disturbance | Recovery distance | Recovery gain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| constrained_fisher | 160 | 0.0408 +/- 0.0076 | 0.6047 +/- 0.0629 | 0.0830 +/- 0.0062 | 0.1159 +/- 0.0042 | 1.8256 +/- 0.0981 | 0.0571 +/- 0.0073 | 0.0099 +/- 0.0067 |
| fisher_grid | 160 | 0.0368 +/- 0.0064 | 0.6794 +/- 0.0530 | 0.3441 +/- 0.0094 | 0.3451 +/- 0.0092 | 3.7255 +/- 0.1316 | 0.0554 +/- 0.0074 | 0.0090 +/- 0.0058 |
| null_probe | 160 | 0.0499 +/- 0.0088 | 1.1706 +/- 0.0628 | 0.0616 +/- 0.0064 | 0.1162 +/- 0.0064 | 1.4767 +/- 0.0856 | 0.0528 +/- 0.0067 | 0.0110 +/- 0.0064 |
| random_probe | 160 | 0.0672 +/- 0.0100 | 1.5602 +/- 0.0672 | 0.2532 +/- 0.0218 | 0.3090 +/- 0.0190 | 4.1380 +/- 0.2659 | 0.0580 +/- 0.0079 | 0.0207 +/- 0.0079 |
| task_greedy | 160 | 0.1225 +/- 0.0164 | 1.7172 +/- 0.0395 | 1.3686 +/- 0.0288 | 1.3660 +/- 0.0288 | 17.2394 +/- 0.3511 | 0.0524 +/- 0.0078 | 0.0162 +/- 0.0062 |
| unpaired_null | 160 | 0.0499 +/- 0.0078 | 1.1014 +/- 0.0573 | 0.0562 +/- 0.0059 | 0.2468 +/- 0.0082 | 3.1677 +/- 0.1081 | 0.0575 +/- 0.0081 | 0.0100 +/- 0.0061 |

## Paired Differences Against Null Probes

Reference policy: `null_probe`. Positive values mean the compared policy is larger than the reference.

| Compared policy | Param error diff | Final disturbance diff | Max disturbance diff | Cumulative disturbance diff | Recovery gain diff | Matched cases |
|---|---:|---:|---:|---:|---:|---:|
| constrained_fisher | -0.0091 +/- 0.0109 | 0.0214 +/- 0.0065 | -0.0003 +/- 0.0040 | 0.3489 +/- 0.0662 | -0.0011 +/- 0.0074 | 160 |
| fisher_grid | -0.0131 +/- 0.0097 | 0.2826 +/- 0.0079 | 0.2290 +/- 0.0071 | 2.2489 +/- 0.0960 | -0.0019 +/- 0.0090 | 160 |
| random_probe | 0.0173 +/- 0.0115 | 0.1917 +/- 0.0221 | 0.1928 +/- 0.0182 | 2.6613 +/- 0.2535 | 0.0098 +/- 0.0102 | 160 |
| task_greedy | 0.0726 +/- 0.0174 | 1.3071 +/- 0.0251 | 1.2498 +/- 0.0238 | 15.7627 +/- 0.2853 | 0.0052 +/- 0.0092 | 160 |
| unpaired_null | 0.0000 +/- 0.0112 | -0.0054 +/- 0.0076 | 0.1306 +/- 0.0068 | 1.6910 +/- 0.0885 | -0.0010 +/- 0.0083 | 160 |

## Budget-Conditioned Means

| Steps | Policy | Param error | Max disturbance | Cumulative disturbance | Recovery gain |
|---:|---|---:|---:|---:|---:|
| 24 | constrained_fisher | 0.0408 +/- 0.0076 | 0.1159 +/- 0.0042 | 1.8256 +/- 0.0981 | 0.0099 +/- 0.0067 |
| 24 | fisher_grid | 0.0368 +/- 0.0064 | 0.3451 +/- 0.0092 | 3.7255 +/- 0.1316 | 0.0090 +/- 0.0058 |
| 24 | null_probe | 0.0499 +/- 0.0088 | 0.1162 +/- 0.0064 | 1.4767 +/- 0.0856 | 0.0110 +/- 0.0064 |
| 24 | random_probe | 0.0672 +/- 0.0100 | 0.3090 +/- 0.0190 | 4.1380 +/- 0.2659 | 0.0207 +/- 0.0079 |
| 24 | task_greedy | 0.1225 +/- 0.0164 | 1.3660 +/- 0.0288 | 17.2394 +/- 0.3511 | 0.0162 +/- 0.0062 |
| 24 | unpaired_null | 0.0499 +/- 0.0078 | 0.2468 +/- 0.0082 | 3.1677 +/- 0.1081 | 0.0100 +/- 0.0061 |

## Budget-Conditioned Paired Differences

Reference policy: `null_probe`. Positive values mean the compared policy is larger than the reference.

| Steps | Compared policy | Param error diff | Max disturbance diff | Cumulative disturbance diff | Matched cases |
|---:|---|---:|---:|---:|---:|
| 24 | constrained_fisher | -0.0091 +/- 0.0109 | -0.0003 +/- 0.0040 | 0.3489 +/- 0.0662 | 160 |
| 24 | fisher_grid | -0.0131 +/- 0.0097 | 0.2290 +/- 0.0071 | 2.2489 +/- 0.0960 | 160 |
| 24 | random_probe | 0.0173 +/- 0.0115 | 0.1928 +/- 0.0182 | 2.6613 +/- 0.2535 | 160 |
| 24 | task_greedy | 0.0726 +/- 0.0174 | 1.2498 +/- 0.0238 | 15.7627 +/- 0.2853 | 160 |
| 24 | unpaired_null | 0.0000 +/- 0.0112 | 0.1306 +/- 0.0068 | 1.6910 +/- 0.0885 | 160 |

## Pareto Check

Two-metric dominance is computed over mean parameter error and mean max diagnostic disturbance; lower is better for both.

| Steps | Two-metric Pareto policies | Two-metric dominated policies | Three-metric Pareto policies | Three-metric dominated policies |
|---:|---|---|---|---|
| 24 | constrained_fisher, fisher_grid | null_probe, random_probe, task_greedy, unpaired_null | constrained_fisher, fisher_grid, null_probe | random_probe, task_greedy, unpaired_null |

## Robustness Detail

Focused on `null_probe` and `constrained_fisher`; lower is better for parameter error and max disturbance.

| Steps | Obs noise | Disturbance limit | Policy | Param error | Max disturbance | Cumulative disturbance |
|---:|---:|---:|---|---:|---:|---:|
| 24 | 0.01 | 0.12 | constrained_fisher | 0.0408 +/- 0.0076 | 0.1159 +/- 0.0042 | 1.8256 +/- 0.0981 |
| 24 | 0.01 | 0.12 | null_probe | 0.0499 +/- 0.0088 | 0.1162 +/- 0.0064 | 1.4767 +/- 0.0856 |

## Slip-Correlation Detail

| Slip corr | Steps | Policy | Param error | Max disturbance | Cumulative disturbance |
|---:|---:|---|---:|---:|---:|
| 0.0 | 24 | constrained_fisher | 0.0408 +/- 0.0076 | 0.1159 +/- 0.0042 | 1.8256 +/- 0.0981 |
| 0.0 | 24 | fisher_grid | 0.0368 +/- 0.0064 | 0.3451 +/- 0.0092 | 3.7255 +/- 0.1316 |
| 0.0 | 24 | null_probe | 0.0499 +/- 0.0088 | 0.1162 +/- 0.0064 | 1.4767 +/- 0.0856 |
| 0.0 | 24 | random_probe | 0.0672 +/- 0.0100 | 0.3090 +/- 0.0190 | 4.1380 +/- 0.2659 |
| 0.0 | 24 | task_greedy | 0.1225 +/- 0.0164 | 1.3660 +/- 0.0288 | 17.2394 +/- 0.3511 |
| 0.0 | 24 | unpaired_null | 0.0499 +/- 0.0078 | 0.2468 +/- 0.0082 | 3.1677 +/- 0.1081 |

## By Damage Case

| Damage | Policy | Param error | Final disturbance | Max disturbance | Recovery gain |
|---|---|---:|---:|---:|---:|
| high_slip | constrained_fisher | 0.0200 +/- 0.0144 | 0.1175 +/- 0.0083 | 0.1544 +/- 0.0055 | 0.0010 +/- 0.0024 |
| high_slip | fisher_grid | 0.0050 +/- 0.0068 | 0.3992 +/- 0.0166 | 0.4012 +/- 0.0169 | 0.0014 +/- 0.0027 |
| high_slip | null_probe | 0.0370 +/- 0.0191 | 0.1079 +/- 0.0163 | 0.1730 +/- 0.0129 | -0.0034 +/- 0.0108 |
| high_slip | random_probe | 0.0300 +/- 0.0160 | 0.3139 +/- 0.0465 | 0.3781 +/- 0.0354 | -0.0038 +/- 0.0045 |
| high_slip | task_greedy | 0.1335 +/- 0.0320 | 1.6839 +/- 0.0071 | 1.6818 +/- 0.0051 | 0.0011 +/- 0.0041 |
| high_slip | unpaired_null | 0.0225 +/- 0.0164 | 0.0821 +/- 0.0177 | 0.3049 +/- 0.0072 | -0.0001 +/- 0.0008 |
| left_gain_loss | constrained_fisher | 0.0365 +/- 0.0154 | 0.0919 +/- 0.0090 | 0.1125 +/- 0.0024 | 0.0151 +/- 0.0196 |
| left_gain_loss | fisher_grid | 0.0350 +/- 0.0121 | 0.3553 +/- 0.0077 | 0.3561 +/- 0.0055 | 0.0167 +/- 0.0165 |
| left_gain_loss | null_probe | 0.0307 +/- 0.0090 | 0.0549 +/- 0.0048 | 0.1046 +/- 0.0029 | 0.0095 +/- 0.0152 |
| left_gain_loss | random_probe | 0.0553 +/- 0.0151 | 0.2380 +/- 0.0504 | 0.3066 +/- 0.0444 | 0.0221 +/- 0.0196 |
| left_gain_loss | task_greedy | 0.0932 +/- 0.0288 | 1.2866 +/- 0.0059 | 1.2845 +/- 0.0039 | 0.0178 +/- 0.0151 |
| left_gain_loss | unpaired_null | 0.0480 +/- 0.0142 | 0.0626 +/- 0.0070 | 0.1867 +/- 0.0035 | 0.0085 +/- 0.0144 |
| right_gain_loss | constrained_fisher | 0.0272 +/- 0.0109 | 0.0874 +/- 0.0096 | 0.1106 +/- 0.0025 | 0.0005 +/- 0.0140 |
| right_gain_loss | fisher_grid | 0.0307 +/- 0.0090 | 0.3620 +/- 0.0053 | 0.3606 +/- 0.0043 | -0.0062 +/- 0.0117 |
| right_gain_loss | null_probe | 0.0400 +/- 0.0118 | 0.0538 +/- 0.0066 | 0.1076 +/- 0.0040 | 0.0063 +/- 0.0138 |
| right_gain_loss | random_probe | 0.0690 +/- 0.0168 | 0.2367 +/- 0.0380 | 0.2879 +/- 0.0331 | 0.0319 +/- 0.0220 |
| right_gain_loss | task_greedy | 0.0968 +/- 0.0313 | 1.2889 +/- 0.0059 | 1.2831 +/- 0.0048 | 0.0199 +/- 0.0169 |
| right_gain_loss | unpaired_null | 0.0470 +/- 0.0147 | 0.0505 +/- 0.0061 | 0.2878 +/- 0.0043 | 0.0057 +/- 0.0174 |
| symmetric_low_power | constrained_fisher | 0.0793 +/- 0.0127 | 0.0352 +/- 0.0060 | 0.0860 +/- 0.0026 | 0.0229 +/- 0.0107 |
| symmetric_low_power | fisher_grid | 0.0765 +/- 0.0120 | 0.2600 +/- 0.0058 | 0.2626 +/- 0.0047 | 0.0243 +/- 0.0086 |
| symmetric_low_power | null_probe | 0.0917 +/- 0.0211 | 0.0298 +/- 0.0050 | 0.0794 +/- 0.0032 | 0.0314 +/- 0.0085 |
| symmetric_low_power | random_probe | 0.1145 +/- 0.0223 | 0.2243 +/- 0.0333 | 0.2634 +/- 0.0291 | 0.0326 +/- 0.0071 |
| symmetric_low_power | task_greedy | 0.1665 +/- 0.0343 | 1.2152 +/- 0.0063 | 1.2144 +/- 0.0037 | 0.0259 +/- 0.0080 |
| symmetric_low_power | unpaired_null | 0.0820 +/- 0.0112 | 0.0296 +/- 0.0046 | 0.2076 +/- 0.0029 | 0.0257 +/- 0.0077 |

