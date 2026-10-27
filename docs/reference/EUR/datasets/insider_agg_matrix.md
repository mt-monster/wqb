# insider_agg_matrix — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `insider_agg_matrix` |
| 名称 | Smart Insider Transaction Aggregates |
| 类别 | INSIDERS |
| 数据字段数(平台) | 34 |
| 覆盖率 | 0.6116 |
| 平台已有 alpha | 156 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a structured, matrix-format view of insider trading activity, where individual transactions by company insiders are aggregated and filtered using advanced methodologies. By summarizing key metrics such as average shares bought or sold, and applying smart filters to highlight the most relevant transactions, the dataset enables researchers and investors to efficiently identify patterns of insider behavior across companies and regions. Such aggregated insider activity is a valuable signal for predicting future price movements, as it can reveal informed trading ahead of significant corporate events or shifts in company fundamentals. The matrix structure makes it easier to incorporate these insights into quantitative models and backtesting frameworks, supporting the develo

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **34** |
| 类型分布 | MATRIX×34 |
| 平均覆盖率 | **0.612** |
| 覆盖率区间 | 0.61 ~ 0.61 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 34 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 28 | 82.4% |
| DEAD | 5 | 14.7% |
| DEAD_STATIC | 1 | 2.9% |

- 已实测字段：**6** 个（18%），best_sharpe 最高 **0.40**，中位 0.06

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 18 | 0.61 | significant_value_1、directional_indicator_2、directional_significant_value_1 |
| 其他 | 16 | 0.61 | avg_buy_shares、avg_secondary_top_buy_shares、total_top_buy_shares |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `avg_buy_shares` | MATRIX | 0.608 | 其他 | 4 | 0.40 | 0.50 | 0.41 | DEAD | Mean shares bought by all directors |
| 2 | `avg_secondary_top_buy_shares` | MATRIX | 0.608 | 其他 | 4 | 0.36 | -0.12 | 0.40 | DEAD_STATIC | Mean shares bought directly by executives |
| 3 | `total_top_buy_shares` | MATRIX | 0.608 | 其他 | 2 | 0.06 | 1.04 | 0.46 | DEAD | Sum shares bought by all executives |
| 4 | `total_secondary_top_buy_shares` | MATRIX | 0.608 | 其他 | 2 | -0.02 | -0.60 | -0.08 | DEAD | Sum shares bought directly by executives |
| 5 | `avg_top_buy_shares` | MATRIX | 0.608 | 其他 | 2 | -0.06 | -0.32 | 0.00 | DEAD | Mean shares bought by all executives |
| 6 | `significant_value_1` | MATRIX | 0.615 | 持仓与资金流 | 1 | -0.13 | -0.05 | -0.05 | DEAD | Value of the most significant insider transaction. |
| 7 | `directional_indicator_2` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | A metric indicating the overall direction or bias of enhanced insider activity. |
| 8 | `directional_significant_value_1` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Highest value among directional significant insider transactions. |
| 9 | `directional_significant_value_2` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Second highest value among directional significant insider transactions. |
| 10 | `directional_significant_value_3` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Third highest value among directional significant insider transactions. |
| 11 | `directional_significant_value_4` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Fourth highest value among directional significant insider transactions. |
| 12 | `significant_value_2` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Value of the second most significant insider transaction. |
| 13 | `significant_value_3` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Value of the third most significant insider transaction. |
| 14 | `significant_value_4` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Value of the fourth most significant insider transaction. |
| 15 | `top_directional_significant_value_1` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Highest value among top directional significant insider transactions. |
| 16 | `top_directional_significant_value_2` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Second highest value among top directional significant insider transactions. |
| 17 | `top_directional_significant_value_3` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Third highest value among top directional significant insider transactions. |
| 18 | `top_directional_significant_value_4` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Fourth highest value among top directional significant insider transactions. |
| 19 | `top_significant_value_1` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Highest value among top significant insider transactions. |
| 20 | `top_significant_value_2` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Second highest value among top significant insider transactions. |
| 21 | `top_significant_value_3` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Third highest value among top significant insider transactions. |
| 22 | `top_significant_value_4` | MATRIX | 0.615 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Fourth highest value among top significant insider transactions. |
| 23 | `avg_secondary_buy_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Mean shares bought directly by directors |
| 24 | `avg_secondary_sell_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Mean shares sold directly by directors |
| 25 | `avg_secondary_top_sell_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Mean shares sold directly by executives |
| 26 | `avg_sell_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Mean shares sold by all directors |
| 27 | `avg_top_sell_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Mean shares sold by all executives |
| 28 | `directional_indicator` | MATRIX | 0.608 | 持仓与资金流 | 0 | — | — | — | UNTESTED | A metric indicating the overall direction or bias of insider activity. |
| 29 | `total_buy_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Sum shares bought by all directors |
| 30 | `total_secondary_buy_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Sum shares bought directly by directors |
| 31 | `total_secondary_sell_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Sum shares sold directly by directors |
| 32 | `total_secondary_top_sell_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Sum shares sold directly by executives |
| 33 | `total_sell_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Sum shares sold by all directors |
| 34 | `total_top_sell_shares` | MATRIX | 0.608 | 其他 | 0 | — | — | — | UNTESTED | Sum shares sold by all executives |

## 六、本地回测证据

- 本地累计回测 **9** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `N1ardQbp` | 0.30 | 0.10 | -0.15 | 0.40 | 0.02 | ["LOW_SHARPE | 215 | `divide(divide(ts_sum(avg_secondary_top_buy_shares,126), add(ts_sum(avg_top_buy_shares,126)` |
| `mLmbGg51` | 0.24 | 0.07 | -0.50 | 0.37 | 0.02 | ["LOW_SHARPE | 215 | `divide(divide(ts_sum(avg_secondary_top_buy_shares,126), add(ts_sum(total_secondary_top_buy` |
| `0mXEVRMK` | 0.06 | 0.01 | 1.04 | -0.03 | 0.19 | ["LOW_SHARPE | 215 | `group_count(total_top_buy_shares, sector)` |
| `mLmbGdYX` | 0.05 | 0.01 | -0.01 | 0.12 | 0.06 | ["LOW_SHARPE | 215 | `divide(ts_av_diff(ts_sum(subtract(avg_buy_shares,avg_secondary_sell_shares),22), 252), add` |
| `N1ardLew` | -0.03 | 0.00 | -0.23 | -0.02 | 0.06 | ["LOW_SHARPE | 215 | `divide(ts_av_diff(ts_sum(subtract(avg_buy_shares,avg_sell_shares),22), 252), add(ts_std_de` |
| `vRrlEkj3` | -0.06 | -0.02 | -0.38 | 0.00 | 0.07 | ["LOW_SHARPE | 215 | `divide(subtract(ts_backfill(avg_top_buy_shares,22), ts_backfill(avg_secondary_buy_shares,2` |
| `mLmbGgV1` | -0.13 | -0.06 | -0.05 | -0.05 | 0.16 | ["LOW_SHARPE | 215 | `divide(significant_value_1, add(add(significant_value_2, significant_value_3), significant` |
| `gJbMlQjM` | -0.16 | -0.08 | -0.67 | -0.08 | 0.06 | ["LOW_SHARPE | 215 | `divide(subtract(ts_backfill(total_secondary_top_buy_shares,22), ts_backfill(avg_secondary_` |
| `rKOlq523` | -0.53 | -0.21 | -0.63 | -0.51 | 0.08 | ["LOW_SHARPE | 215 | `divide(days_from_last_change(significant_value_1), add(days_from_last_change(significant_v` |

## 七、判死记录（sealed dead_end）

- `EUR-INSIDER-AGG-MATRIX-COLD-ZERO-YIELD`（2026-09-22）family=内部人买入股数比例与二级买入广度：{"dataset": "insider_agg_matrix", "evidence": {"alpha_count": 114, "best_abs_sharpe": 0.53, "best_positive_sharpe": 0.3}, "failure_mode": "LOW_SHARPE / LOW_FITNESS / LOW_ROBUST_UNIVERSE_SHARPE / LOW_2Y_SHARPE + 多数 CONCENTRATED_WEIGHT", "mechanism": "内部人买入股数比例与二级买入广度（avg_secondary_top_buy_shares / total_top_buy_shares，126 长窗）", "rule": "命中 EUR profile fast_kill（新集 8 探针无 /S/>=0.5）；INSIDERS 塔另一集 insi

