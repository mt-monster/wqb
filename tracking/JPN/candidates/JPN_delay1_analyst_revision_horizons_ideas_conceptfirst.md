# Concept-first ideas — JPN / TOP1600 / D1 / analyst_revision_horizons (2026-09-19)

**Dataset**: analyst_revision_horizons
**Region**: JPN
**Delay**: 1


> 手写 ideas（SOP 允许：source=手写/LLM 的 ideas 可注入 GEM）。背景：该集 GEM 模板展开 7538 条、w9 抽样 35 条 max|S| 0.62，
> 但样本全是 `add(sign,sign)` / `abs(subtract)` 类垃圾变体，分析师修正机制本身未被正确测试。
> 本文档按"机制 → 1-2 个具体字段 → 一条实现"给 GEM，只用标准窗口（5/22/66/252），字段覆盖 0.56-0.78 一律 `ts_backfill`。
> 纪律：禁 add(w·A, w·B) 加权混合；JPN 无 sector/subindustry/industry，分组只用 market 或 bucket(rank(x), range=...)。
> 设置：STATISTICAL（JPN 唯一可用的截面中性化）；decay 4。

## Concepts

**Concept**: Recommendation revision breadth (up-minus-down ratio, 30d)

- **Mechanism**: 分析师上调/下调评级家数之差占总修正家数的比例 = 修正广度。广度为正且持续 → 未来 1-3 月超额收益（Jegadeesh 2004 修正漂移；日本市场分析师覆盖集中在 TOP1600，信息扩散慢）。比值而非差值，剔除覆盖家数（大盘股）效应。
- **Fields**: `analyst_recommendation_upgrades_30d_medium_3`, `analyst_recommendation_downgrades_30d_medium_3`
- **Implementation Example**: `rank(ts_backfill(divide(subtract({analyst_recommendation_upgrades_30d_medium_3}, {analyst_recommendation_downgrades_30d_medium_3}), add(add({analyst_recommendation_upgrades_30d_medium_3}, {analyst_recommendation_downgrades_30d_medium_3}), 1)), 22))`

**Concept**: Revision score level, smoothed (5d score, 22d decay)

- **Mechanism**: 供应商已聚合的修正评分（5 日均）是修正方向的一手代理；线性衰减 22 日保留漂移期、压换手。中等持有期（medium horizon 版本）与 D1 提交口径匹配。
- **Fields**: `analyst_revision_score_5d_medium`
- **Implementation Example**: `rank(ts_decay_linear(ts_backfill({analyst_revision_score_5d_medium}, 22), 22))`

**Concept**: Revision score momentum (30d change of score, short horizon)

- **Mechanism**: 修正评分的变化（加速度）领先于水平：评分刚由负转正的公司还未被充分定价。用 30 日变化字段直接表达"修正动量"。
- **Fields**: `analyst_revision_score_change_30d_short`
- **Implementation Example**: `rank(ts_backfill({analyst_revision_score_change_30d_short}, 22))`

**Concept**: EPS estimate revision momentum (current-year EPS, 14d %chg, medium)

- **Mechanism**: 一致预期 EPS 的百分比变化是修正漂移最直接的度量；14 日窗兼顾及时性与噪声。低覆盖（0.76）先回填再排名。
- **Fields**: `avg_estimate_change_pct_current_year_eps_14d_short`
- **Implementation Example**: `rank(ts_backfill({avg_estimate_change_pct_current_year_eps_14d_short}, 22))`

**Concept**: Revision acceleration (7d vs 90d estimate change, long horizon)

- **Mechanism**: 近 7 日修正幅度减去 90 日修正幅度 = 修正加速度：正加速 = 新一轮上修刚开始（趋势延续），负加速 = 上修衰竭。排序差（rank-rank）避免量纲与加权混合。
- **Fields**: `avg_estimate_change_pct_current_year_eps_7d_medium`, `avg_estimate_change_pct_current_year_eps_90d_long`
- **Implementation Example**: `subtract(rank(ts_backfill({avg_estimate_change_pct_current_year_eps_7d_medium}, 22)), rank(ts_backfill({avg_estimate_change_pct_current_year_eps_90d_long}, 66)))`

**Concept**: Post-earnings-announcement drift via realized surprise (last quarter, 66d hold)

- **Mechanism**: 上季实际 EPS 惊喜百分比在公告后 1-3 月持续漂移（PEAD，日本市场文献支持）；66 日回填 + 22 日线性衰减近似"公告后持有一个季度并逐步减仓"。
- **Fields**: `actual_earnings_surprise_pct_lastq_medium`
- **Implementation Example**: `rank(ts_decay_linear(ts_backfill({actual_earnings_surprise_pct_lastq_medium}, 66), 22))`

**Concept**: Predicted surprise (model-forecast vs consensus, quarterly EPS)

- **Mechanism**: 供应商"预测惊喜"= 更聪明的分析师子集 vs 一致预期的差，是尚未发布的惊喜的领先指标；直接排名，66 日回填覆盖季度频率。
- **Fields**: `predicted_surprise_pct_quarterly_eps_medium`
- **Implementation Example**: `rank(ts_backfill({predicted_surprise_pct_quarterly_eps_medium}, 66))`

**Concept**: Revision breadth conditioned on distance from 52-week high (attention gate)

- **Mechanism**: 结构交互（允许形态④ 条件门控）：修正广度只在股价离 52 周高点较远（未被追捧）时定价不足；接近高点的上修已被动量交易者消化。用 trade_when 门控而非加权。
- **Fields**: `analyst_recommendation_upgrades_30d_medium_3`, `analyst_recommendation_downgrades_30d_medium_3`, `pct_change_from_52week_high_medium_term`
- **Implementation Example**: `trade_when(less(rank(ts_backfill({pct_change_from_52week_high_medium_term}, 22)), 0.7), rank(ts_backfill(divide(subtract({analyst_recommendation_upgrades_30d_medium_3}, {analyst_recommendation_downgrades_30d_medium_3}), add(add({analyst_recommendation_upgrades_30d_medium_3}, {analyst_recommendation_downgrades_30d_medium_3}), 1)), 22)), -1)`

## 字段（Fields）

| Field ID | Type | Coverage | Role |
|---|---|---|---|
| analyst_recommendation_upgrades_30d_medium_3 | MATRIX | 0.78 | 主信号（广度分子） |
| analyst_recommendation_downgrades_30d_medium_3 | MATRIX | 0.78 | 主信号（广度分子/分母） |
| analyst_revision_score_5d_medium | MATRIX | 0.76 | 主信号 |
| analyst_revision_score_change_30d_short | MATRIX | 0.75 | 主信号 |
| avg_estimate_change_pct_current_year_eps_14d_short | MATRIX | 0.76 | 主信号 |
| avg_estimate_change_pct_current_year_eps_7d_medium | MATRIX | 0.76 | 主信号（加速度短腿） |
| avg_estimate_change_pct_current_year_eps_90d_long | MATRIX | 0.74 | 辅助（加速度长腿） |
| actual_earnings_surprise_pct_lastq_medium | MATRIX | 0.57 | 主信号（PEAD） |
| predicted_surprise_pct_quarterly_eps_medium | MATRIX | 0.56 | 主信号 |
| pct_change_from_52week_high_medium_term | MATRIX | 0.78 | 条件腿（bucket/trade_when） |

## 特征（Features）

- ts_backfill 22/66：覆盖 0.56-0.78 的季度/事件字段先回填
- rank / subtract(rank, rank)：截面排序与排序差，不做加权混合
- ts_decay_linear 22：压换手，保留漂移期
- trade_when：条件门控（结构交互），不用 add(w·A, w·B)

## 建议（Implementation Examples）

- concept_1: `rank(ts_backfill(divide(subtract({analyst_recommendation_upgrades_30d_medium_3}, {analyst_recommendation_downgrades_30d_medium_3}), add(add({analyst_recommendation_upgrades_30d_medium_3}, {analyst_recommendation_downgrades_30d_medium_3}), 1)), 22))`
- concept_2: `rank(ts_decay_linear(ts_backfill({analyst_revision_score_5d_medium}, 22), 22))`
- concept_3: `rank(ts_backfill({analyst_revision_score_change_30d_short}, 22))`
- concept_4: `rank(ts_backfill({avg_estimate_change_pct_current_year_eps_14d_short}, 22))`
- concept_5: `subtract(rank(ts_backfill({avg_estimate_change_pct_current_year_eps_7d_medium}, 22)), rank(ts_backfill({avg_estimate_change_pct_current_year_eps_90d_long}, 66)))`
- concept_6: `rank(ts_decay_linear(ts_backfill({actual_earnings_surprise_pct_lastq_medium}, 66), 22))`
- concept_7: `rank(ts_backfill({predicted_surprise_pct_quarterly_eps_medium}, 66))`
- concept_8: `trade_when(less(rank(ts_backfill({pct_change_from_52week_high_medium_term}, 22)), 0.7), rank(ts_backfill(divide(subtract({analyst_recommendation_upgrades_30d_medium_3}, {analyst_recommendation_downgrades_30d_medium_3}), add(add({analyst_recommendation_upgrades_30d_medium_3}, {analyst_recommendation_downgrades_30d_medium_3}), 1)), 22)), -1)`

## 字段白名单（Field Whitelist）

```
analyst_recommendation_upgrades_30d_medium_3
analyst_recommendation_downgrades_30d_medium_3
analyst_revision_score_5d_medium
analyst_revision_score_change_30d_short
avg_estimate_change_pct_current_year_eps_14d_short
avg_estimate_change_pct_current_year_eps_7d_medium
avg_estimate_change_pct_current_year_eps_90d_long
actual_earnings_surprise_pct_lastq_medium
predicted_surprise_pct_quarterly_eps_medium
pct_change_from_52week_high_medium_term
```