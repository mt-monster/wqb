# Wave R3 模板池（论坛进阶结构 · READY · 已排除幽灵算子）

> ⛔ **`regression_neut` 不是平台算子名**（`references/*.md` 全局锁定条目明示）⇒ 已替换为 `ts_regression(..., rettype=0)` 残差形式。
> ✅ `winsorize` 平台可用（算子矩阵标 ⭐ 且是 prod 承重件）。
> 依据：risk70 帖「ts_zscore(dsrt,60)」「loading 先 winsorize」；risk88 帖「纯残差均值回归」。

| # | 机制 | 算子数 | 表达式 |
|---|---|---:|---|
| R3-01 | 论坛原式 ts_zscore60 反转 | 3 | `subtract(0.5, group_rank(ts_zscore(rsk70_mfm2_asetrd_dsrt, 60), sector))` |
| R3-02 | winsorize 后 zscore 反转 | 4 | `subtract(0.5, group_rank(winsorize(ts_zscore(rsk70_mfm2_asetrd_dsrt, 60), std=4), sector))` |
| R3-03 | ts_regression 残差(行业载荷) | 4 | `subtract(0.5, group_rank(ts_regression(ts_zscore(rsk70_mfm2_asetrd_dsrt, 60), rsk70_mfm2_asetrd_srtindcnt, 252, lag=0, rettype=0), sector))` |
| R3-04 | ts_regression 残差(韩国因子) | 4 | `subtract(0.5, group_rank(ts_regression(ts_zscore(rsk70_mfm2_asetrd_dsrt, 60), rsk70_mfm2_asetrd_cnt_kor, 252, lag=0, rettype=0), sector))` |
| R3-05 | risk71 特异收益反转 | 3 | `subtract(0.5, group_rank(ts_mean(rsk71_eqy_asi_supported_minvol1m_dsrt, 5), sector))` |
| R3-06 | risk72 特异收益反转 | 3 | `subtract(0.5, group_rank(ts_mean(rsk72_asi_top2000_eqy_dsrt, 5), sector))` |
| R3-07 | 空头占流通比 | 4 | `subtract(0.5, group_rank(ts_mean(vec_avg(rsk59_shortinterestpct), 22), sector))` |
| R3-08 | 空头动量×费率相关 | 5 | `subtract(0.5, group_rank(ts_corr(vec_avg(rsk59_short_momentum), vec_avg(rsk59_bid_rate), 22), sector))` |
| R3-09 | risk88 残差 22 日反转 | 3 | `subtract(0.5, group_rank(ts_mean(rsk88_mfm_ase1_dsrt, 22), sector))` |
| R3-10 | risk88 残差 zscore60 | 3 | `subtract(0.5, group_rank(ts_zscore(rsk88_mfm_ase1_dsrt, 60), sector))` |
| R3-11 | 特异收益÷特异风险 水平 | 4 | `subtract(0.5, group_rank(divide(rsk70_mfm2_asetrd_dsrt, sqrt(rsk70_mfm2_asetrd_srisk)), sector))` |
| R3-12 | 残差反转 反臂 | 3 | `subtract(group_rank(ts_mean(rsk88_mfm_ase1_dsrt, 5), sector), 0.5)` |

覆盖：risk70(dsrt/srisk/srtindcnt/cnt_kor) · risk88(dsrt) · risk59(shortinterestpct/short_momentum/bid_rate) · risk71 · risk72
