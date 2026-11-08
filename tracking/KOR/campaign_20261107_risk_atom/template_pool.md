# 模板池 · KOR Risk ATOM（16 个结构互异）

> 结构维度：水平 / 短窗 / 变化率 / zscore / ts_rank / group_zscore / 倒数 / std / 行业轴 / 反臂方向。
> 机制：M1 特异反转 / M2 融券约束 / M3 挤压 / M4 特异波动 / M5 低 beta。

| # | 机制 | 表达式 |
|---|---|---|
| R01 | M1 特异反转 risk68 | `subtract(0.5, group_rank(ts_mean(rsk68_residual_return, 5), sector))` |
| R02 | M1 特异反转 risk70 | `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_dsrt, 22), sector))` |
| R03 | M2 融券费率 | `subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_bid_rate), 22), sector))` |
| R04 | M2 利用率 zscore | `subtract(0.5, group_rank(ts_zscore(vec_avg(rsk59_s3utilization), 66), sector))` |
| R05 | M3 挤压（做多） | `subtract(group_rank(ts_mean(vec_avg(rsk59_squeeze_risk), 22), sector), 0.5)` |
| R06 | M4 特异波动 | `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_resvol, 22), sector))` |
| R07 | M2 DTC 变化率 | `subtract(0.5, group_rank(ts_delta(vec_avg(rsk59_daystocover10day), 22), sector))` |
| R08 | M5 低 beta | `subtract(0.5, group_rank(ts_mean(rsk68_beta, 22), sector))` |
| R09 | M1 ts_rank 形态 | `subtract(0.5, group_rank(ts_rank(rsk70_mfm2_asetrd_dsrt, 66), sector))` |
| R10 | M4 最终特异风险 | `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_srisk, 22), sector))` |
| R11 | M2 空头占流通比 | `subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_shortinterestpct), 22), sector))` |
| R12 | M3 拥挤度 group_zscore | `group_zscore(ts_mean(vec_avg(rsk59_crowded_score), 22), sector)` |
| R13 | M2 供给倒数 | `subtract(0.5, group_rank(ts_mean(divide(1, add(vec_avg(rsk59_indicativeavailability), 1)), 22), sector))` |
| R14 | M1 industry 轴 | `subtract(0.5, group_rank(ts_mean(rsk68_residual_return, 5), industry))` |
| R15 | M1 特异反转波动 std | `subtract(0.5, group_rank(ts_mean(vec_stddev(rsk59_short_momentum), 22), sector))` |
| R16 | M2 DTC30 水平 | `subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_daystocover30day), 22), sector))` |

## R1 首派（8 条）
- R01 M1 特异反转 risk68 — `subtract(0.5, group_rank(ts_mean(rsk68_residual_return, 5), sector))`
- R02 M1 特异反转 risk70 — `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_dsrt, 22), sector))`
- R03 M2 融券费率 — `subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_bid_rate), 22), sector))`
- R04 M2 利用率 zscore — `subtract(0.5, group_rank(ts_zscore(vec_avg(rsk59_s3utilization), 66), sector))`
- R05 M3 挤压（做多） — `subtract(group_rank(ts_mean(vec_avg(rsk59_squeeze_risk), 22), sector), 0.5)`
- R06 M4 特异波动 — `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_resvol, 22), sector))`
- R07 M2 DTC 变化率 — `subtract(0.5, group_rank(ts_delta(vec_avg(rsk59_daystocover10day), 22), sector))`
- R08 M5 低 beta — `subtract(0.5, group_rank(ts_mean(rsk68_beta, 22), sector))`
