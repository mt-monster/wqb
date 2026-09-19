# Concept-first ideas — IND / TOP500 / D1 / analyst_consensus (2026-09-19)

**Dataset**: analyst_consensus
**Region**: IND
**Delay**: 1


> 手写 ideas（SOP 允许 source=手写 的 ideas 注入 GEM）。背景：IND 未点亮塔 7 集 197 条 0 候选（robust/换手结构墙）；
> 用户规则"已点亮塔不再优先"= 优先级而非禁令 —— 未点亮塔已实证穷尽后，转向 IND 唯一被证明既过 robust 又能 prod-clean 的信号面：
> 分析师一致预期（vRje2ZGd ACTIVE，STATISTICAL 过 robust 1.03）。避开已饱和的 revision-magnitude 族，只用 analyst_consensus 的
> **冷字段（users 1-8）**：年度 EPS 一致预期的惊喜/离散度/4 周修正/覆盖变化。全部 VECTOR（vec_avg），cov 0.91 → ts_backfill。
> 纪律：标准窗口 22/66/252；禁 add(w·A, w·B)；组合只用比值/排序差/trade_when 门控。设置 STATISTICAL / decay 4。

## Concepts

**Concept**: Standardized earnings surprise (SUE, annual EPS)

- **Mechanism**: 实际 EPS 减一致预期（surprise）除以预期离散度 = 标准化惊喜；PEAD 在印度市场持续 1-3 月。66 日回填覆盖年报节奏，22 日线性衰减控换手。
- **Fields**: `mean_surprise_value_eps_annual12_3`, `stddev_estimate_eps_annual12_3`
- **Implementation Example**: `rank(ts_decay_linear(ts_backfill(divide(vec_avg({mean_surprise_value_eps_annual12_3}), add(vec_avg({stddev_estimate_eps_annual12_3}), 0.01)), 66), 22))`

**Concept**: Analyst estimate dispersion (Diether-Malloy-Scherbina)

- **Mechanism**: 预期离散度高 = 意见分歧大 + 卖空约束 → 价格偏乐观 → 未来低收益；做多低离散度。离散度用 |mean| 标准化去量纲。
- **Fields**: `stddev_estimate_eps_annual12_3`, `mean_estimate_eps_annual12_3`
- **Implementation Example**: `rank(ts_backfill(multiply(-1, divide(vec_avg({stddev_estimate_eps_annual12_3}), add(abs(vec_avg({mean_estimate_eps_annual12_3})), 0.01))), 22))`

**Concept**: Consensus revision momentum (mean vs 4 weeks prior)

- **Mechanism**: 一致预期相对 4 周前的百分比变化 = 修正动量；修正漂移是 IND 最强的分析师效应（vRje2ZGd 同机制不同字段族，冷字段规避 prod 撞墙）。
- **Fields**: `mean_estimate_eps_annual12_3`, `mean_estimate_four_weeks_prior_eps_annual12_3`
- **Implementation Example**: `rank(ts_backfill(divide(subtract(vec_avg({mean_estimate_eps_annual12_3}), vec_avg({mean_estimate_four_weeks_prior_eps_annual12_3})), add(abs(vec_avg({mean_estimate_four_weeks_prior_eps_annual12_3})), 0.01)), 22))`

**Concept**: Analyst coverage change (attention inflow)

- **Mechanism**: 贡献一致预期的分析师家数 66 日变化：覆盖增加 = 机构关注流入、信息环境改善 → 正向；覆盖减少 = 被放弃。
- **Fields**: `estimate_count_current_period_eps_annual12_3`
- **Implementation Example**: `rank(ts_delta(ts_backfill(vec_avg({estimate_count_current_period_eps_annual12_3}), 22), 66))`

**Concept**: Estimate skew (optimism asymmetry)

- **Mechanism**: (最高预期 − 中位数) / (中位数 − 最低预期)：右偏 = 少数极端乐观者拉高均值 → 一致预期偏高 → 负向；比值形态无量纲。
- **Fields**: `max_estimate_eps_annual12_3`, `median_estimate_eps_annual12_3`, `min_estimate_eps_annual12_3`
- **Implementation Example**: `rank(ts_backfill(multiply(-1, divide(subtract(vec_avg({max_estimate_eps_annual12_3}), vec_avg({median_estimate_eps_annual12_3})), add(subtract(vec_avg({median_estimate_eps_annual12_3}), vec_avg({min_estimate_eps_annual12_3})), 0.01))), 22))`

**Concept**: SUE gated by low dispersion (conviction filter)

- **Mechanism**: 结构交互（条件门控）：惊喜只在分歧小（离散度低半区）时可信，分歧大时惊喜可能是预期本身失真。trade_when 门控而非加权。
- **Fields**: `mean_surprise_value_eps_annual12_3`, `stddev_estimate_eps_annual12_3`, `mean_estimate_eps_annual12_3`
- **Implementation Example**: `trade_when(less(rank(ts_backfill(divide(vec_avg({stddev_estimate_eps_annual12_3}), add(abs(vec_avg({mean_estimate_eps_annual12_3})), 0.01)), 22)), 0.5), rank(ts_backfill(vec_avg({mean_surprise_value_eps_annual12_3}), 66)), -1)`

## 字段（Fields）

| Field ID | Type | Coverage | Role |
|---|---|---|---|
| mean_surprise_value_eps_annual12_3 | VECTOR | 0.91 | 主信号（惊喜） |
| stddev_estimate_eps_annual12_3 | VECTOR | 0.91 | 主信号（离散度）/ 标准化分母 |
| mean_estimate_eps_annual12_3 | VECTOR | 0.91 | 主信号（修正分子）/ 标准化分母 |
| mean_estimate_four_weeks_prior_eps_annual12_3 | VECTOR | 0.91 | 辅助（修正基准） |
| estimate_count_current_period_eps_annual12_3 | VECTOR | 0.91 | 主信号（覆盖变化） |
| max_estimate_eps_annual12_3 | VECTOR | 0.91 | 辅助（偏度） |
| median_estimate_eps_annual12_3 | VECTOR | 0.91 | 辅助（偏度） |
| min_estimate_eps_annual12_3 | VECTOR | 0.91 | 辅助（偏度） |

## 特征（Features）

- vec_avg：VECTOR 字段聚合
- ts_backfill 22/66：年报节奏字段回填
- divide / subtract(rank, rank) / trade_when：比值、排序差、条件门控，不做加权混合
- ts_decay_linear 22：压换手

## 建议（Implementation Examples）

- concept_1: `rank(ts_decay_linear(ts_backfill(divide(vec_avg({mean_surprise_value_eps_annual12_3}), add(vec_avg({stddev_estimate_eps_annual12_3}), 0.01)), 66), 22))`
- concept_2: `rank(ts_backfill(multiply(-1, divide(vec_avg({stddev_estimate_eps_annual12_3}), add(abs(vec_avg({mean_estimate_eps_annual12_3})), 0.01))), 22))`
- concept_3: `rank(ts_backfill(divide(subtract(vec_avg({mean_estimate_eps_annual12_3}), vec_avg({mean_estimate_four_weeks_prior_eps_annual12_3})), add(abs(vec_avg({mean_estimate_four_weeks_prior_eps_annual12_3})), 0.01)), 22))`
- concept_4: `rank(ts_delta(ts_backfill(vec_avg({estimate_count_current_period_eps_annual12_3}), 22), 66))`
- concept_5: `rank(ts_backfill(multiply(-1, divide(subtract(vec_avg({max_estimate_eps_annual12_3}), vec_avg({median_estimate_eps_annual12_3})), add(subtract(vec_avg({median_estimate_eps_annual12_3}), vec_avg({min_estimate_eps_annual12_3})), 0.01))), 22))`
- concept_6: `trade_when(less(rank(ts_backfill(divide(vec_avg({stddev_estimate_eps_annual12_3}), add(abs(vec_avg({mean_estimate_eps_annual12_3})), 0.01)), 22)), 0.5), rank(ts_backfill(vec_avg({mean_surprise_value_eps_annual12_3}), 66)), -1)`

## 字段白名单（Field Whitelist）

```
mean_surprise_value_eps_annual12_3
stddev_estimate_eps_annual12_3
mean_estimate_eps_annual12_3
mean_estimate_four_weeks_prior_eps_annual12_3
estimate_count_current_period_eps_annual12_3
max_estimate_eps_annual12_3
median_estimate_eps_annual12_3
min_estimate_eps_annual12_3
```