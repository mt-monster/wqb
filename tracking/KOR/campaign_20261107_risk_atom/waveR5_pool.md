# Wave R5 池（`akKQ7jkR` 主线提 S · 保 2Y · READY）

> 依据 key_insight_risk_volume.md：风险量族 S1.02/2Y1.08，反转族 S2.13/2Y0.10 ⇒ 互补。
> R5 只在**风险量族**内增强，禁入反转窗口谱。
> preflight valid=true

| # | 机制 | 算子 | 表达式 |
|---|---|---:|---|
| R5-01 | 收缩幅度 多窗乘积(5x22) | 7 | `subtract(0.5, group_rank(multiply(ts_mean(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 5), ts_mean(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 22)), sector))` |
| R5-02 | 收缩比率 srisku/srisk | 4 | `subtract(0.5, group_rank(ts_mean(divide(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 22), sector))` |
| R5-03 | 收缩幅度 ts_rank | 4 | `subtract(0.5, group_rank(ts_rank(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 66), sector))` |
| R5-04 | 收缩幅度 zscore252 | 4 | `subtract(0.5, group_rank(ts_zscore(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 252), sector))` |
| R5-05 | 收缩幅度 industry 轴 | 4 | `subtract(0.5, group_rank(ts_mean(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 22), industry))` |
| R5-06 | 低特异风险 66 窗 | 3 | `subtract(0.5, group_rank(ts_mean(rsk70_mfm2_asetrd_srisk, 66), sector))` |
| R5-07 | risk59 费率xDTC 反臂 | 7 | `subtract(group_rank(ts_mean(vec_avg(rsk59_daystocover10day), 22), sector), group_rank(ts_mean(vec_avg(rsk59_bid_rate), 22), sector))` |
| R5-08 | 收缩幅度 decay_linear | 4 | `subtract(0.5, group_rank(ts_decay_linear(subtract(rsk70_mfm2_asetrd_srisku, rsk70_mfm2_asetrd_srisk), 22), sector))` |

⚠ R5-01 multiply 两腿为同字段不同窗口 ⇒ 单信号结构化（合规）。
⚠ R5-07 是 `gJegjkkM`(S-0.71/2Y-1.85 双负) 的反臂，按铁律 B 必测。
