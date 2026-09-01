# IND Wave 131 特征工程决策文档（S1/S2）

- 波次: IND / TOP500 / D1 / neutralization=STATISTICAL
- 日期: 2026-08-31
- 候选池来源: skill（brain-makeSomeGem headless_runner + trailSomeAlphas，priors=tracking/IND/priors/ind_priors.json wins=6/dead_ends=12）
- S0 白名单: model16, model50, pv106, behavioral_signals（other323/pv13 经 S1 判定降级排除）

## 数据集与字段预算

| 数据集 | 类型/覆盖 | 入池字段 | 剔除字段（IND 已饱和/死族实证） |
|---|---|---|---|
| model16 | MATRIX×8, cov=1.0 | composite_factor_score, earnings_certainty_rank, multi_factor_acceleration_score, multi_factor_static_score, cashflow_efficiency_rank | analyst_revision_rank（prod 0.82-0.96）、relative_valuation（估值死）、growth_potential（增长死） |
| model50 | MATRIX×58 | risk_score_change_13w, aggregate_downside_risk_score_2, forecast_dispersion, profitability_level, avg_daily_volume, total_market_capitalization, external_financing, financial_leverage, free_cash_flow_yield, capital_investment, fundamental_growth, price_momentum, beta_relative_to_country, analyst_forecast_revision(+country) | 估值类（IND 估值死） |
| pv106 | MATRIX×23 | pv106_wli_spread/-bp/-lastspread, bid_ask_price_gap, transaction_cost_max/median/percentile, asia_trade_cost_buy/sell, aggregated_slippage, group_order_slippage | reverse() 骨架 2 条（SCALE-NEG-RANK 铁律） |
| behavioral_signals | VECTOR×7 | visual_price_path_shape_score, chronological_return_sequence_correlation, salience_weighted_return_score, price_path_curvature_measure, consecutive_return_streak_length（全部 vec_avg 包裹） | reverse() 骨架 1 条 |

## 预处理决策

1. MATRIX 字段：ts_backfill(x,66) 兜底 → rank/quantile/ts_delta/ts_mean/ts_corr。
2. VECTOR 字段（behavioral_signals）：必须 vec_avg 聚合后再进常规算子（IND event 类硬约束）。
3. 稀疏事件防护：swap/事件流不直接裸排；本波 other315 未入生成池（S1 判定探针级，暂缓）。
4. 反向统一写法：subtract(0, x) 或 -rank(x)，禁用 reverse(...)。
5. quantile 单参硬约束：GEM 生成的 driver="gaussian" 参数已全部剥离（8 条修复）。
6. 骨架配给：补 trade_when 事件门控（model16 加速度>0 才进 composite 评分）与 ts_corr 流动性体制（pv106 spreadbp × transaction_cost_median）各 1 条。

## 主信号 / 辅助信号分配（组合类表达式）

- model50 双腿：analyst_forecast_revision（快变量 0.6）× profitability_level（慢锚 0.4）——复用 SLOW-X-FAST-MIX 配方压 prod_corr（win 实证 0.81→0.66）。
- pv106 双腿：aggregated_slippage（水平 0.4）× group_order_slippage delta（变化 0.6）。
- model16 双腿：cashflow_efficiency × earnings_certainty（质量协同，无权重调参）。

## GEM ideas 报告索引

- model16: output_report/IND_d1_model16_ideas_v2.md
- model50: brain-makeSomeGem/skills/brain-data-feature-engineering/output_report/IND_delay1_model50_ideas.md
- pv106: brain-makeSomeGem/skills/brain-data-feature-engineering/output_report/IND_delay1_pv106_ideas.md
- behavioral_signals: brain-makeSomeGem/skills/brain-data-feature-engineering/output_report/IND_delay1_behavioral_signals_ideas.md

## 建议

1. model16 多因子加速度/静态分 delta 是本波最优先行指标，若 IS 突破可优先 Mode B 扩骨架（勿同信号调权重）。
2. model50 risk_score_change 族为正交风险恶化机制，预估器标注 HARD 仅作参考，以实测为准；若 IS 强但 prod 撞墙，走 prod_wall_dilution_v1（找 |corr|<0.3 分量梯度稀释）。
3. pv106 买卖成本不对称（asia_trade_cost_buy-sell）是新机制，与 win（cost-max/median 比）同族但骨架不同，注意 self_corr 对照。
4. behavioral_signals 延续既有三角困境认知：优先低换手字段（chronological_return_sequence_correlation），STATISTICAL 中性化。
5. other315（全 VECTOR 稀疏事件）仅在上述方向判死后作探针批，先 ts_backfill+trade_when 结构化。

## 门禁结论（wave_gate Wave 131）

语法 29/29 PASS；5 闸 all_pass=True（29/29）；六维多样性 PASS（算子熵 3.091，同质 5.7%）；
质量预估 D/C/W/B/H=0/0/28/0/1（#16 risk_score_change 预估器 HARD 标注仅参考——该预估器擅长拦截不擅长优选，机制保留实测）。
