# Experiment Summary

Input: `runs/correlated_slip_sweep_results.csv`
Rows: 7200

## Policy Means

| Policy | n | Param error | Entropy | Final disturbance | Max disturbance | Cumulative disturbance | Recovery distance | Recovery gain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| constrained_fisher | 1800 | 0.0517 +/- 0.0028 | 0.8812 +/- 0.0293 | 0.0767 +/- 0.0021 | 0.1122 +/- 0.0012 | 1.8759 +/- 0.0624 | 0.0721 +/- 0.0031 | 0.0199 +/- 0.0022 |
| fisher_grid | 1800 | 0.0485 +/- 0.0024 | 0.9522 +/- 0.0314 | 0.3264 +/- 0.0085 | 0.3426 +/- 0.0079 | 4.8814 +/- 0.1968 | 0.0697 +/- 0.0030 | 0.0206 +/- 0.0022 |
| null_probe | 1800 | 0.0601 +/- 0.0029 | 1.2977 +/- 0.0325 | 0.0687 +/- 0.0037 | 0.1231 +/- 0.0035 | 1.7281 +/- 0.0822 | 0.0708 +/- 0.0032 | 0.0239 +/- 0.0022 |
| unpaired_null | 1800 | 0.0593 +/- 0.0029 | 1.2991 +/- 0.0329 | 0.0699 +/- 0.0035 | 0.2517 +/- 0.0032 | 3.3856 +/- 0.1094 | 0.0712 +/- 0.0030 | 0.0196 +/- 0.0020 |

## Paired Differences Against Null Probes

Reference policy: `null_probe`. Positive values mean the compared policy is larger than the reference.

| Compared policy | Param error diff | Final disturbance diff | Max disturbance diff | Cumulative disturbance diff | Recovery gain diff | Matched cases |
|---|---:|---:|---:|---:|---:|---:|
| constrained_fisher | -0.0084 +/- 0.0035 | 0.0080 +/- 0.0033 | -0.0109 +/- 0.0030 | 0.1479 +/- 0.0500 | -0.0040 +/- 0.0028 | 1800 |
| fisher_grid | -0.0115 +/- 0.0032 | 0.2577 +/- 0.0076 | 0.2196 +/- 0.0068 | 3.1534 +/- 0.1435 | -0.0033 +/- 0.0030 | 1800 |
| unpaired_null | -0.0008 +/- 0.0036 | 0.0012 +/- 0.0039 | 0.1286 +/- 0.0033 | 1.6576 +/- 0.0740 | -0.0043 +/- 0.0028 | 1800 |

## Budget-Conditioned Means

| Steps | Policy | Param error | Max disturbance | Cumulative disturbance | Recovery gain |
|---:|---|---:|---:|---:|---:|
| 8 | constrained_fisher | 0.0784 +/- 0.0064 | 0.1019 +/- 0.0020 | 0.4960 +/- 0.0148 | 0.0200 +/- 0.0039 |
| 8 | fisher_grid | 0.0684 +/- 0.0050 | 0.1541 +/- 0.0033 | 0.6605 +/- 0.0155 | 0.0201 +/- 0.0039 |
| 8 | null_probe | 0.0868 +/- 0.0061 | 0.0927 +/- 0.0020 | 0.3952 +/- 0.0115 | 0.0233 +/- 0.0038 |
| 8 | unpaired_null | 0.0886 +/- 0.0062 | 0.2346 +/- 0.0038 | 1.0019 +/- 0.0158 | 0.0196 +/- 0.0035 |
| 24 | constrained_fisher | 0.0409 +/- 0.0037 | 0.1139 +/- 0.0020 | 1.8073 +/- 0.0486 | 0.0195 +/- 0.0037 |
| 24 | fisher_grid | 0.0443 +/- 0.0038 | 0.3465 +/- 0.0057 | 3.7457 +/- 0.0811 | 0.0209 +/- 0.0038 |
| 24 | null_probe | 0.0529 +/- 0.0045 | 0.1225 +/- 0.0052 | 1.5652 +/- 0.0691 | 0.0247 +/- 0.0038 |
| 24 | unpaired_null | 0.0508 +/- 0.0042 | 0.2518 +/- 0.0051 | 3.2689 +/- 0.0719 | 0.0196 +/- 0.0035 |
| 40 | constrained_fisher | 0.0357 +/- 0.0029 | 0.1207 +/- 0.0019 | 3.3245 +/- 0.0827 | 0.0201 +/- 0.0036 |
| 40 | fisher_grid | 0.0329 +/- 0.0027 | 0.5272 +/- 0.0088 | 10.2381 +/- 0.1883 | 0.0209 +/- 0.0038 |
| 40 | null_probe | 0.0404 +/- 0.0033 | 0.1539 +/- 0.0082 | 3.2237 +/- 0.1734 | 0.0237 +/- 0.0037 |
| 40 | unpaired_null | 0.0384 +/- 0.0031 | 0.2685 +/- 0.0067 | 5.8861 +/- 0.1603 | 0.0195 +/- 0.0035 |

## Budget-Conditioned Paired Differences

Reference policy: `null_probe`. Positive values mean the compared policy is larger than the reference.

| Steps | Compared policy | Param error diff | Max disturbance diff | Cumulative disturbance diff | Matched cases |
|---:|---|---:|---:|---:|---:|
| 8 | constrained_fisher | -0.0085 +/- 0.0085 | 0.0092 +/- 0.0015 | 0.1008 +/- 0.0096 | 600 |
| 8 | fisher_grid | -0.0185 +/- 0.0071 | 0.0614 +/- 0.0028 | 0.2653 +/- 0.0114 | 600 |
| 8 | unpaired_null | 0.0017 +/- 0.0085 | 0.1419 +/- 0.0033 | 0.6067 +/- 0.0135 | 600 |
| 24 | constrained_fisher | -0.0120 +/- 0.0052 | -0.0086 +/- 0.0043 | 0.2421 +/- 0.0522 | 600 |
| 24 | fisher_grid | -0.0086 +/- 0.0052 | 0.2240 +/- 0.0051 | 2.1805 +/- 0.0647 | 600 |
| 24 | unpaired_null | -0.0021 +/- 0.0054 | 0.1293 +/- 0.0055 | 1.7037 +/- 0.0740 | 600 |
| 40 | constrained_fisher | -0.0047 +/- 0.0036 | -0.0332 +/- 0.0072 | 0.1007 +/- 0.1402 | 600 |
| 40 | fisher_grid | -0.0075 +/- 0.0036 | 0.3733 +/- 0.0083 | 7.0144 +/- 0.1611 | 600 |
| 40 | unpaired_null | -0.0021 +/- 0.0038 | 0.1146 +/- 0.0076 | 2.6624 +/- 0.1737 | 600 |

## Pareto Check

Two-metric dominance is computed over mean parameter error and mean max diagnostic disturbance; lower is better for both.

| Steps | Two-metric Pareto policies | Two-metric dominated policies | Three-metric Pareto policies | Three-metric dominated policies |
|---:|---|---|---|---|
| 8 | constrained_fisher, fisher_grid, null_probe | unpaired_null | constrained_fisher, fisher_grid, null_probe | unpaired_null |
| 24 | constrained_fisher | fisher_grid, null_probe, unpaired_null | constrained_fisher, null_probe | fisher_grid, unpaired_null |
| 40 | constrained_fisher, fisher_grid | null_probe, unpaired_null | constrained_fisher, fisher_grid, null_probe | unpaired_null |

## Robustness Detail

Focused on `null_probe` and `constrained_fisher`; lower is better for parameter error and max disturbance.

| Steps | Obs noise | Disturbance limit | Policy | Param error | Max disturbance | Cumulative disturbance |
|---:|---:|---:|---|---:|---:|---:|
| 8 | 0.01 | 0.12 | constrained_fisher | 0.0784 +/- 0.0064 | 0.1019 +/- 0.0020 | 0.4960 +/- 0.0148 |
| 8 | 0.01 | 0.12 | null_probe | 0.0868 +/- 0.0061 | 0.0927 +/- 0.0020 | 0.3952 +/- 0.0115 |
| 24 | 0.01 | 0.12 | constrained_fisher | 0.0409 +/- 0.0037 | 0.1139 +/- 0.0020 | 1.8073 +/- 0.0486 |
| 24 | 0.01 | 0.12 | null_probe | 0.0529 +/- 0.0045 | 0.1225 +/- 0.0052 | 1.5652 +/- 0.0691 |
| 40 | 0.01 | 0.12 | constrained_fisher | 0.0357 +/- 0.0029 | 0.1207 +/- 0.0019 | 3.3245 +/- 0.0827 |
| 40 | 0.01 | 0.12 | null_probe | 0.0404 +/- 0.0033 | 0.1539 +/- 0.0082 | 3.2237 +/- 0.1734 |

## Slip-Correlation Detail

| Slip corr | Steps | Policy | Param error | Max disturbance | Cumulative disturbance |
|---:|---:|---|---:|---:|---:|
| 0.0 | 8 | constrained_fisher | 0.0744 +/- 0.0110 | 0.1018 +/- 0.0037 | 0.4943 +/- 0.0260 |
| 0.0 | 8 | fisher_grid | 0.0659 +/- 0.0087 | 0.1520 +/- 0.0050 | 0.6452 +/- 0.0219 |
| 0.0 | 8 | null_probe | 0.0829 +/- 0.0105 | 0.0912 +/- 0.0029 | 0.3861 +/- 0.0167 |
| 0.0 | 8 | unpaired_null | 0.0848 +/- 0.0107 | 0.2344 +/- 0.0066 | 0.9962 +/- 0.0265 |
| 0.0 | 24 | constrained_fisher | 0.0362 +/- 0.0060 | 0.1127 +/- 0.0034 | 1.7767 +/- 0.0820 |
| 0.0 | 24 | fisher_grid | 0.0416 +/- 0.0066 | 0.3360 +/- 0.0070 | 3.5960 +/- 0.0972 |
| 0.0 | 24 | null_probe | 0.0502 +/- 0.0078 | 0.1129 +/- 0.0057 | 1.4379 +/- 0.0786 |
| 0.0 | 24 | unpaired_null | 0.0479 +/- 0.0068 | 0.2466 +/- 0.0073 | 3.1736 +/- 0.0975 |
| 0.0 | 40 | constrained_fisher | 0.0327 +/- 0.0049 | 0.1196 +/- 0.0034 | 3.2708 +/- 0.1398 |
| 0.0 | 40 | fisher_grid | 0.0321 +/- 0.0047 | 0.5116 +/- 0.0110 | 9.8667 +/- 0.2249 |
| 0.0 | 40 | null_probe | 0.0367 +/- 0.0056 | 0.1356 +/- 0.0078 | 2.8418 +/- 0.1740 |
| 0.0 | 40 | unpaired_null | 0.0379 +/- 0.0053 | 0.2581 +/- 0.0082 | 5.6095 +/- 0.1898 |
| 0.5 | 8 | constrained_fisher | 0.0731 +/- 0.0110 | 0.1026 +/- 0.0035 | 0.5060 +/- 0.0274 |
| 0.5 | 8 | fisher_grid | 0.0659 +/- 0.0084 | 0.1543 +/- 0.0057 | 0.6689 +/- 0.0291 |
| 0.5 | 8 | null_probe | 0.0856 +/- 0.0106 | 0.0932 +/- 0.0035 | 0.3988 +/- 0.0203 |
| 0.5 | 8 | unpaired_null | 0.0885 +/- 0.0107 | 0.2349 +/- 0.0066 | 1.0033 +/- 0.0277 |
| 0.5 | 24 | constrained_fisher | 0.0372 +/- 0.0061 | 0.1138 +/- 0.0034 | 1.8213 +/- 0.0887 |
| 0.5 | 24 | fisher_grid | 0.0430 +/- 0.0065 | 0.3431 +/- 0.0086 | 3.7263 +/- 0.1272 |
| 0.5 | 24 | null_probe | 0.0514 +/- 0.0076 | 0.1211 +/- 0.0080 | 1.5544 +/- 0.1090 |
| 0.5 | 24 | unpaired_null | 0.0500 +/- 0.0071 | 0.2504 +/- 0.0082 | 3.2485 +/- 0.1158 |
| 0.5 | 40 | constrained_fisher | 0.0318 +/- 0.0047 | 0.1210 +/- 0.0033 | 3.3256 +/- 0.1479 |
| 0.5 | 40 | fisher_grid | 0.0322 +/- 0.0046 | 0.5213 +/- 0.0128 | 10.1433 +/- 0.2816 |
| 0.5 | 40 | null_probe | 0.0396 +/- 0.0057 | 0.1487 +/- 0.0115 | 3.1477 +/- 0.2569 |
| 0.5 | 40 | unpaired_null | 0.0371 +/- 0.0054 | 0.2647 +/- 0.0100 | 5.7970 +/- 0.2368 |
| 0.85 | 8 | constrained_fisher | 0.0877 +/- 0.0111 | 0.1013 +/- 0.0032 | 0.4877 +/- 0.0234 |
| 0.85 | 8 | fisher_grid | 0.0734 +/- 0.0089 | 0.1559 +/- 0.0064 | 0.6674 +/- 0.0291 |
| 0.85 | 8 | null_probe | 0.0921 +/- 0.0107 | 0.0937 +/- 0.0039 | 0.4008 +/- 0.0221 |
| 0.85 | 8 | unpaired_null | 0.0925 +/- 0.0109 | 0.2347 +/- 0.0066 | 1.0062 +/- 0.0281 |
| 0.85 | 24 | constrained_fisher | 0.0492 +/- 0.0068 | 0.1151 +/- 0.0034 | 1.8239 +/- 0.0820 |
| 0.85 | 24 | fisher_grid | 0.0483 +/- 0.0066 | 0.3604 +/- 0.0129 | 3.9148 +/- 0.1809 |
| 0.85 | 24 | null_probe | 0.0571 +/- 0.0081 | 0.1336 +/- 0.0119 | 1.7033 +/- 0.1562 |
| 0.85 | 24 | unpaired_null | 0.0547 +/- 0.0077 | 0.2586 +/- 0.0106 | 3.3846 +/- 0.1529 |
| 0.85 | 40 | constrained_fisher | 0.0427 +/- 0.0054 | 0.1216 +/- 0.0033 | 3.3770 +/- 0.1423 |
| 0.85 | 40 | fisher_grid | 0.0345 +/- 0.0046 | 0.5488 +/- 0.0200 | 10.7044 +/- 0.4282 |
| 0.85 | 40 | null_probe | 0.0450 +/- 0.0060 | 0.1775 +/- 0.0199 | 3.6817 +/- 0.4103 |
| 0.85 | 40 | unpaired_null | 0.0402 +/- 0.0054 | 0.2829 +/- 0.0154 | 6.2518 +/- 0.3685 |

## By Damage Case

| Damage | Policy | Param error | Final disturbance | Max disturbance | Recovery gain |
|---|---|---:|---:|---:|---:|
| high_slip | constrained_fisher | 0.0408 +/- 0.0054 | 0.1172 +/- 0.0030 | 0.1434 +/- 0.0022 | -0.0001 +/- 0.0019 |
| high_slip | fisher_grid | 0.0276 +/- 0.0046 | 0.4033 +/- 0.0195 | 0.4214 +/- 0.0186 | 0.0009 +/- 0.0010 |
| high_slip | null_probe | 0.0443 +/- 0.0062 | 0.1363 +/- 0.0119 | 0.1978 +/- 0.0108 | 0.0029 +/- 0.0021 |
| high_slip | unpaired_null | 0.0403 +/- 0.0060 | 0.1272 +/- 0.0115 | 0.3242 +/- 0.0069 | 0.0002 +/- 0.0015 |
| left_gain_loss | constrained_fisher | 0.0383 +/- 0.0050 | 0.0728 +/- 0.0038 | 0.1096 +/- 0.0011 | 0.0220 +/- 0.0057 |
| left_gain_loss | fisher_grid | 0.0416 +/- 0.0043 | 0.3251 +/- 0.0166 | 0.3322 +/- 0.0161 | 0.0160 +/- 0.0053 |
| left_gain_loss | null_probe | 0.0490 +/- 0.0049 | 0.0526 +/- 0.0027 | 0.1097 +/- 0.0019 | 0.0251 +/- 0.0056 |
| left_gain_loss | unpaired_null | 0.0516 +/- 0.0055 | 0.0651 +/- 0.0032 | 0.1857 +/- 0.0014 | 0.0212 +/- 0.0053 |
| right_gain_loss | constrained_fisher | 0.0408 +/- 0.0055 | 0.0785 +/- 0.0037 | 0.1096 +/- 0.0012 | 0.0193 +/- 0.0051 |
| right_gain_loss | fisher_grid | 0.0362 +/- 0.0032 | 0.3325 +/- 0.0165 | 0.3551 +/- 0.0137 | 0.0252 +/- 0.0058 |
| right_gain_loss | null_probe | 0.0482 +/- 0.0048 | 0.0553 +/- 0.0028 | 0.1088 +/- 0.0020 | 0.0201 +/- 0.0052 |
| right_gain_loss | unpaired_null | 0.0499 +/- 0.0045 | 0.0553 +/- 0.0030 | 0.2866 +/- 0.0013 | 0.0175 +/- 0.0049 |
| symmetric_low_power | constrained_fisher | 0.0868 +/- 0.0051 | 0.0384 +/- 0.0022 | 0.0861 +/- 0.0010 | 0.0383 +/- 0.0024 |
| symmetric_low_power | fisher_grid | 0.0887 +/- 0.0046 | 0.2444 +/- 0.0116 | 0.2618 +/- 0.0102 | 0.0403 +/- 0.0026 |
| symmetric_low_power | null_probe | 0.0988 +/- 0.0058 | 0.0305 +/- 0.0015 | 0.0760 +/- 0.0010 | 0.0475 +/- 0.0021 |
| symmetric_low_power | unpaired_null | 0.0954 +/- 0.0055 | 0.0318 +/- 0.0015 | 0.2101 +/- 0.0011 | 0.0393 +/- 0.0020 |

