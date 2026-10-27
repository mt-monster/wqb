# insider_matrix — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `insider_matrix` |
| 名称 | Aggregated Insider Transaction Matrix |
| 类别 | OTHER |
| 数据字段数(平台) | 33 |
| 覆盖率 | 0.6107 |
| 平台已有 alpha | 82 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a structured matrix of insider transaction data, organized by company, region, and time delay. It aggregates and filters insider buying and selling activities, capturing key metrics such as average buy and sell values, transaction counts, and ratios over configurable time windows. By summarizing insider trades from individuals with privileged access to non-public information, the dataset enables analysts to identify patterns of opportunistic or routine trading, cluster buying, and other signals that may precede significant price movements. The smart aggregation and filtering enhance signal quality, making it a valuable resource for predicting future stock performance, detecting market anomalies, and constructing alpha-generating investment strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **33** |
| 类型分布 | MATRIX×33 |
| 平均覆盖率 | **0.611** |
| 覆盖率区间 | 0.61 ~ 0.61 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 33 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 32 | 97.0% |
| DEAD | 1 | 3.0% |

- 已实测字段：**1** 个（3%），best_sharpe 最高 **0.93**，中位 0.93

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 16 | 0.61 | eur_director_signal_value_1、eur_director_signal_value_2、eur_director_signal_value_3 |
| 宏观与行业 | 16 | 0.61 | eur_aggregated_value_1、eur_aggregated_value_2、eur_aggregated_value_3 |
| 风险与质量 | 1 | 0.61 | director_intensity_score |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `eur_director_signal_value_1` | MATRIX | 0.615 | 价量与波动 | 8 | 0.93 | 0.76 | — | DEAD | Mean value of shares bought directly in Euro currency by directors with significant trades |
| 2 | `eur_director_signal_value_2` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum value of shares bought directly in Euro currency by directors with significant trades |
| 3 | `eur_director_signal_value_3` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean value of shares sold directly in Euro currency by directors with significant trades |
| 4 | `eur_director_signal_value_4` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum value of shares sold directly in Euro currency by directors with significant trades |
| 5 | `eur_signal_value_1` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean value of shares bought in Euro currency by directors with significant trades |
| 6 | `eur_signal_value_2` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum value of shares bought in Euro currency by directors with significant trades |
| 7 | `eur_signal_value_3` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean value of shares sold in Euro currency by directors with significant trades |
| 8 | `eur_signal_value_4` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum value of shares sold in Euro currency by directors with significant trades |
| 9 | `eur_top_director_signal_value_1` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean value of shares bought directly in Euro currency by executives with significant trades |
| 10 | `eur_top_director_signal_value_2` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum value of shares bought directly in Euro currency by executives with significant trades |
| 11 | `eur_top_director_signal_value_3` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean value of shares sold directly in Euro currency by executives with significant trades |
| 12 | `eur_top_director_signal_value_4` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum value of shares sold directly in Euro currency by executives with significant trades |
| 13 | `eur_top_signal_value_1` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean value of shares bought in Euro currency by executives with significant trades |
| 14 | `eur_top_signal_value_2` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum value of shares bought in Euro currency by executives with significant trades |
| 15 | `eur_top_signal_value_3` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean value of shares sold in Euro currency by executives with significant trades |
| 16 | `eur_top_signal_value_4` | MATRIX | 0.615 | 价量与波动 | 0 | — | — | — | UNTESTED | Sum value of shares sold in Euro currency by executives with significant trades |
| 17 | `director_intensity_score` | MATRIX | 0.607 | 风险与质量 | 0 | — | — | — | UNTESTED | Dataset-specific timing/bookkeeping indicator used for internal sequence logging; not a trading signal |
| 18 | `eur_aggregated_value_1` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Mean value of shares bought in Euro currency |
| 19 | `eur_aggregated_value_2` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sum value of shares bought in Euro currency |
| 20 | `eur_aggregated_value_3` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Mean value of shares sold in Euro currency |
| 21 | `eur_aggregated_value_4` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sum value of shares sold in Euro currency |
| 22 | `eur_director_value_1` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Mean value of shares bought in Euro currency by all directors |
| 23 | `eur_director_value_2` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sum value of shares bought in Euro currency by all directors |
| 24 | `eur_director_value_3` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Mean value of shares sold in Euro currency by all directors |
| 25 | `eur_director_value_4` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sum value of shares sold in Euro currency by all directors |
| 26 | `eur_top_director_value_1` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Mean value of shares bought in Euro currency by specific directors |
| 27 | `eur_top_director_value_2` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sum value of shares bought in Euro currency by specific directors |
| 28 | `eur_top_director_value_3` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Mean value of shares sold in Euro currency by specific directors |
| 29 | `eur_top_director_value_4` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sum value of shares sold in Euro currency by specific directors |
| 30 | `eur_top_value_1` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Mean value of shares bought in Euro currency by executives |
| 31 | `eur_top_value_2` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sum value of shares bought in Euro currency by executives |
| 32 | `eur_top_value_3` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Mean value of shares sold in Euro currency by executives |
| 33 | `eur_top_value_4` | MATRIX | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sum value of shares sold in Euro currency by executives |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `npKdXP0M` | 0.93 | 0.39 | 0.71 | — | 0.04 | ["LOW_SHARPE | s2_insider_matrix_d1 | `group_rank(ts_backfill(eur_director_signal_value_1, 66), industry)` |
| `LL9N2ZO1` | 0.58 | 0.34 | -0.05 | — | 0.28 | ["LOW_SHARPE | s2_insider_matrix_d1 | `rank(zscore(eur_director_signal_value_1))` |
| `E5vp2Rom` | 0.58 | 0.34 | -0.05 | — | 0.28 | ["LOW_SHARPE | s2_insider_matrix_d1 | `rank(eur_director_signal_value_1)` |
| `P0Z2AgeK` | 0.48 | 0.25 | -0.30 | — | 0.28 | ["LOW_SHARPE | s2_insider_matrix_d1 | `rank(ts_decay_linear(eur_director_signal_value_1, 21))` |
| `Grdb7OEJ` | 0.38 | 0.11 | 0.76 | — | 0.04 | ["LOW_SHARPE | s2_insider_matrix_d1 | `rank(ts_mean(eur_director_signal_value_1, 66))` |
| `3q9X2Vd0` | -0.01 | 0.00 | -1.06 | — | 0.31 | ["LOW_SHARPE | s2_insider_matrix_d1 | `rank(multiply(ts_zscore(eur_director_signal_value_1, 66), ts_zscore(eur_aggregated_value_2` |
| `LL9N2Ze1` | -0.13 | -0.04 | -0.64 | — | 0.23 | ["LOW_SHARPE | s2_insider_matrix_d1 | `rank(divide(eur_director_signal_value_1, eur_aggregated_value_2))` |
| `YP5b9MZR` | -0.25 | -0.14 | -0.46 | — | 0.04 | ["LOW_SHARPE | s2_insider_matrix_d1 | `ts_zscore(ts_delta(eur_director_signal_value_1, 21), 22)` |

## 七、判死记录（sealed dead_end）

- `EUR-INSIDER-AGG-MATRIX-COLD-ZERO-YIELD`（2026-09-22）family=内部人买入股数比例与二级买入广度：{"dataset": "insider_agg_matrix", "evidence": {"alpha_count": 114, "best_abs_sharpe": 0.53, "best_positive_sharpe": 0.3}, "failure_mode": "LOW_SHARPE / LOW_FITNESS / LOW_ROBUST_UNIVERSE_SHARPE / LOW_2Y_SHARPE + 多数 CONCENTRATED_WEIGHT", "mechanism": "内部人买入股数比例与二级买入广度（avg_secondary_top_buy_shares / total_top_buy_shares，126 长窗）", "rule": "命中 EUR profile fast_kill（新集 8 探针无 /S/>=0.5）；INSIDERS 塔另一集 insi

