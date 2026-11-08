# Wave R2 模板池（论坛组合结构 · READY）

> 依据：risk70 帖「单字段直用最高 S0.41，价值在组合」+ risk88 帖「纯残差更适合均值回归、时序衰减、剔薄流动性」。
> preflight valid=true unknown=[]
> 算子数：R2-01=5, R2-02=4, R2-03=3, R2-04=3, R2-05=5, R2-06=6, R2-07=7, R2-08=3, R2-09=3, R2-10=4, R2-11=7, R2-12=3

| # | 机制 | 表达式 |
|---|---|---|
| R2-01 | 风险调整特异收益反转 | `subtract(0.5, group_rank(ts_mean(divide(rsk70_mfm2_asetrd_dsrt, sqrt(rsk70_mfm2_asetrd_srisk)), 22), sector))` |
| R2-02 | 风险收缩幅度 | `subtract(0.5, group_rank(ts_mean(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 22), sector))` |
| R2-03 | risk88 纯残差衰减反转 | `subtract(0.5, group_rank(ts_decay_linear(rsk88_mfm_ase1_dsrt, 5), sector))` |
| R2-04 | 纯残差5日反转 | `subtract(0.5, group_rank(ts_mean(rsk88_mfm_ase1_dsrt, 5), sector))` |
| R2-05 | 残差 zscore 反转 | `subtract(0.5, group_rank(ts_zscore(divide(rsk70_mfm2_asetrd_dsrt, sqrt(rsk70_mfm2_asetrd_srisk)), 66), sector))` |
| R2-06 | 流动性门控残差反转 | `trade_when(greater(rank(rsk68_weight_edadv), 0.3), subtract(0.5, group_rank(ts_mean(rsk88_mfm_ase1_dsrt, 5), sector)), -1)` |
| R2-07 | 借券约束强度价差 | `subtract(group_rank(ts_mean(vec_avg(rsk59_bid_rate), 22), sector), group_rank(ts_mean(vec_avg(rsk59_daystocover10day), 22), sector))` |
| R2-08 | 特殊风险低波 | `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_srisk, 22), sector))` |
| R2-09 | 残差反转 industry 轴 | `subtract(0.5, group_rank(ts_mean(rsk88_mfm_ase1_dsrt, 5), industry))` |
| R2-10 | 风险调整反转 std | `subtract(0.5, group_rank(ts_mean(vec_stddev(rsk70_mfm2_asetrd_dsrt), 22), sector))` |
| R2-11 | DTC÷费率背离 | `subtract(group_rank(ts_mean(vec_avg(rsk59_daystocover10day), 22), sector), group_rank(ts_mean(vec_avg(rsk59_bid_rate), 22), sector))` |
| R2-12 | 残差反转 ts_rank | `subtract(0.5, group_rank(ts_rank(rsk88_mfm_ase1_dsrt, 22), sector))` |
