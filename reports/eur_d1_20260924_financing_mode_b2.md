# EUR D1 融资依赖 Mode B2：收益来源剥离

## 字段
total_financing_cash_flow、operating_cashflow、assets_total_2；均为已核实 MATRIX，users分别1、4、7。冷门字段预算100%。252日回填保留；不增加窗口网格。

## 特征
合格主信号2rwj1kWY S1.42/F.85，production .7879。第一轮6个概念完成：正经营现金流门控S.38/F.12淘汰；资产分母wpZ9mr9Q改善至S1.51/F.96，但子宇宙.76/稳健宇宙.69不足。现金储备组内主信号S1.41/F.85，prod .7762，仍不合格。投资现金支出分母S1.38/F.80，prod尚待平台结果。

## 建议
第二周期只测试四个可证伪问题：盈利暴露、规模暴露、季度会计时点、自身融资状态。每个机制独立；不做加权混合，不救援弱候选，不改变EUR/D1/TOPCS1600/SUBINDUSTRY/decay4。来源沿用第一轮理论文献 https://arxiv.org/abs/1411.7670 对外部融资成本和流动性管理的经济解释；下列欧股可预测性是待检验推论，不是论文结论。数据诊断仅为模拟计数代理，完整形状包仍缺失，必须显式warn。

**Dataset**: fundamental23
**Region**: EUR
**Delay**: 1

**Concept**: Financing intensity independent of operating profitability
**Mechanism**: Remove cross-sectional operating cash return on assets exposure from low external financing intensity. Surviving returns would support an independent financing effect rather than a profitability proxy.
**Fields**: total_financing_cash_flow, assets_total_2, operating_cashflow.
**Implementation Example**: `vector_neut(reverse(rank(divide(ts_backfill({total_financing_cash_flow},252),ts_backfill({assets_total_2},252)))),rank(divide(ts_backfill({operating_cashflow},252),ts_backfill({assets_total_2},252))))`

**Concept**: Cash financing dependence independent of company scale
**Mechanism**: Remove asset size exposure from financing relative to internal cash, isolating financing dependence from large mature firm structure.
**Fields**: total_financing_cash_flow, operating_cashflow, assets_total_2.
**Implementation Example**: `vector_neut(reverse(rank(divide(ts_backfill({total_financing_cash_flow},252),abs(ts_backfill({operating_cashflow},252))))),rank(ts_backfill({assets_total_2},252)))`

**Concept**: Annual persistent financing intensity
**Mechanism**: Annual mean financing intensity aggregates the quarterly financing cycle. Improvement would indicate reporting timing noise in a persistent financing policy signal, rather than a short term event.
**Fields**: total_financing_cash_flow, assets_total_2.
**Implementation Example**: `reverse(rank(ts_mean(divide(ts_backfill({total_financing_cash_flow},252),ts_backfill({assets_total_2},252)),252)))`

**Concept**: Financing intensity relative to own historical state
**Mechanism**: Compare financing intensity to its own annual distribution before cross-sectional ranking. This removes stable payer/issuer identity and tests whether unusually low financing needs contain information.
**Fields**: total_financing_cash_flow, assets_total_2.
**Implementation Example**: `reverse(rank(ts_zscore(divide(ts_backfill({total_financing_cash_flow},252),ts_backfill({assets_total_2},252)),252)))`
