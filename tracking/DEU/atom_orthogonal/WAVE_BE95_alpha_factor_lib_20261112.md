# BE95 设计档：alpha_factor_lib 行业专属基本面（未点亮 FUNDAMENTAL 塔最后机制面，2026-11-12）

> 背景：65 字段全 VECTOR，此前仅以「cov=0」先验排除，从未实测（BE89/90 已证 cov 先验不可信）。
> 机制：跨行业通用价值/质量动量 7 条 + DEU 权重行业专属 3 条（银行=德银/商银，保险=安联/慕再）。
> 设置：DEU/TOP500/D1，decay4，SUBINDUSTRY，nan ON，全部 ≤5 算子。

| 臂 | 字段 | 构造 | 机制 |
|---|---|---|---|
| 1 | change_free_cash_flow_to_market_cap | 水平 | 估值动量（FCF 收益率改善=便宜化） |
| 2 | change_free_cash_flow_to_total_assets | 水平 | 资产效率改善 |
| 3 | free_cash_flow_per_share_change | 水平 | 每股现金创造变化 |
| 4 | fundamental_one_year_unweighted_profit_growth | 水平 | 利润增长（质量） |
| 5 | change_dcf_implied_market_cap | 水平 | DCF 隐含市值变化（内在价值动量） |
| 6 | fundamental_retention_ratio | 水平 | 留存比率（再投资能力） |
| 7 | industry_one_year_growth_net_profit_estimate | 水平 | 行业净利预期增长（预期修正） |
| 8 | bank_tier1_capital_ratio | 水平 | 银行资本充足率（质量） |
| 9 | bank_modified_texas_ratio_1y_change | 负号（比率上升=信用恶化） | 银行信用质量变化 |
| 10 | insurance_combined_ratio | 负号（综合成本率越低越好） | 保险承保盈利 |

表达式模板：`group_zscore(group_rank(ts_backfill(vec_avg(<field>),66),sector),market)`（臂 9/10 外层加负号）。

## 判读线（协议 v2 L1）

max |S| ≥1.2 满波 / 1.0-1.2 定向补 / <1.0 判死 + lc 证书。
注意：行业专属字段（臂 8-10）coverage 天然低（仅该行业股票有值），lc 会小；若 lc <30 则该臂数据不足，不算信号否证。
