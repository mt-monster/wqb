# DEU Analyst ATOM 战役 · 波 1 设计（2026-11-06）

> 目标：10 颗 ATOM（单数据集）regular alpha，DEU/TOP500/D1，ANALYST 塔。
> 本波：A 批 analyst7（608 字段仅 61 测，最大未挖矿脉）+ B 批 analyst_factor_signals 分歧度族（94 测全押 estimate_change 族，分歧度/偏度/斜率族零测）。
> 设置：decay4 / SUBINDUSTRY / trunc0.08 / nanOFF / pasteurize ON / VERIFY / maxTrade OFF。
> 硬约束：算子 ≤12（越少越好）；窗口白名单 22/66/252/504；ATOM 单数据集不占两塔配额；self 避雷——两颗已提交 analyst alpha（2rjrMZ25 / LLM93nGa）都基于 eps_y1_estimate_change_3mo ⇒ **estimate_change_3mo 族整族禁用**，本波全部走非修正机制。

## 机制取证（论坛+论文，派发前）

1. 论坛《分析师数据的正确打开方式:预期差与修正》(WL27618, 30 赞)：修正>水平；收入意外比 EPS 干净；**分歧度低=正溢价**；覆盖人数做质量过滤；winsorize 后排序；**收入上修+利润下修=利润率压缩预警**（评论区 LL46807 评价"全文最值钱的构造"）。
2. 论坛《分析师预期修正，怎样分离方向与参与广度》(XH93773, 29 赞)：方向 × 广度分离假设。
3. 论坛《分析师预测分歧度》(ZW71478, 14 赞, 引东方证券研报)：DISP 分歧度因子负方向；**分歧类构造对分组敏感，industry 粒度优于全局排序**。
4. 论坛《分析师盈利预期修正广度》(17 票) + DEU 实战帖：「同一行业里谁比同行被上调得狠」= group_rank 组内归一。
5. 论文先验：Diether-Malloy-Scherbina (2002 JF) 分歧度高→收益低；Zhang (2006) 信息不确定性；Finexus (1995-2024) 修正得分欧洲 4.6%/年（方向：上调→正）。
6. 负先验（DEU 已证）：model26 的 avg_change_analyst_recommendation（推荐变化）S −0.33/−0.37 ⇒ 推荐变化臂方向存疑，只留 1 臂试探。

## A 批 · analyst7 模板池（10 结构互异）

| # | 机制 | 表达式 | 方向 | ops |
|---|---|---|---|---|
| T1 | 修正广度净额（EBITDA 4周） | group_rank(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), industry) | + | 2 |
| T2 | 广度占比（除法归一） | group_rank(divide(est_12m_ebi_raisednum_4wks, add(est_12m_ebi_raisednum_4wks, add(est_12m_ebi_lowerednum_4wks, 1))), industry) | + | 5 |
| T3 | 广度动量 ts_delta 22 | group_rank(ts_delta(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), 22), industry) | + | 4 |
| T4 | 周频广度累积 zscore 66 | group_zscore(ts_sum(subtract(est_12m_ebi_raised_1wk, est_12m_ebi_lowered_1wk), 66), industry) | + | 4 |
| T5 | **利润率压缩交叉**（利润广度−销售广度） | group_rank(subtract(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), subtract(est_12m_sal_raisednum_4wks, est_12m_sal_lowerednum_4wks)), industry) | + | 7 |
| T6 | 推荐变化广度（负先验存疑臂） | group_rank(subtract(rec_raisednum_4wks, rec_lowerednum_4wks), industry) | +? | 2 |
| T7 | 共识区间分歧度（std/|mean| 反向） | -group_rank(divide(est_12m_ebi_std, abs(est_12m_ebi_mean)), industry) | − | 3 |
| T8 | PEAD（EBITDA 惊喜均值回填） | group_rank(ts_backfill(act_q_ebi_surprisemean, 66), industry) | + | 3 |
| T9 | 覆盖度门控广度 | trade_when(greater(est_12m_ebi_num, 5), group_rank(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), subindustry), -1) | + | 6 |
| T10 | 共识水平变化 ts_av_diff 66（self 风险标注） | group_rank(ts_av_diff(est_12m_ebi_mean, 66), industry) | + | 3 |

## B 批 · analyst_factor_signals 分歧度模板池（10 结构互异）

| # | 机制 | 表达式 | 方向 | ops |
|---|---|---|---|---|
| D1 | FY1 CV 分歧度反向 | -group_rank(ts_backfill(eps_y1_estimate_coeff_var, 66), industry) | − | 3 |
| D2 | FY1 偏度反向（右尾乐观→高估） | -group_rank(ts_backfill(eps_y1_estimate_skewness, 66), industry) | − | 3 |
| D3 | FY2 CV 分歧度反向（horizon gap 载体） | -group_rank(ts_backfill(eps_y2_estimate_coeff_var, 66), industry) | − | 3 |
| D4 | 分歧收敛（CV 落差为正） | group_rank(-ts_delta(ts_backfill(eps_y1_estimate_coeff_var, 252), 66), industry) | −Δ | 4 |
| D5 | 营收偏度反向 | -group_rank(ts_backfill(revenue_y1_estimate_skewness, 66), industry) | − | 3 |
| D6 | 净利润 CV（volatility_adj_1yr 实为 CV）反向 | -group_rank(ts_backfill(netprofit_y1_estimate_volatility_adj_1yr, 66), industry) | − | 3 |
| D7 | 分布不对称性探针（方向未知） | group_rank(ts_backfill(netprofit_y1_estimate_asymmetry, 66), industry) | ± | 3 |
| D8 | 分歧度时序分位（高估体制检测） | -group_rank(ts_rank(ts_backfill(eps_y1_estimate_coeff_var, 66), 252), industry) | − | 4 |
| D9 | 趋势斜率（平滑修正，self 风险标注） | group_rank(ts_backfill(eps_estimate_trend_slope_1yr, 66), industry) | + | 3 |
| D10 | winsorize 稳健分歧度 | -group_rank(winsorize(ts_backfill(eps_y1_estimate_coeff_var, 66), std=4), industry) | − | 4 |

## 判读预案（三分法）
- S≥1.58 且 2Y>1.58 → 全闸验证 + MCP prod/self + 逐年覆盖（get_alpha_yearly_stats，连续空窗判死口径）。
- S 1.0-1.58 → 不判死，归因后升窗口/换轴/换算子。
- 双结构皆 <0.5 → 该字段族判死，同族免测。

## 字段画像存档
- tracking/DEU/atom_analyst/fields/<ds>_fields.json（15 个数据集全量字段目录）
- tracking/DEU/atom_analyst/field_profiles_20261106.md（汇总画像，见单独文件）
