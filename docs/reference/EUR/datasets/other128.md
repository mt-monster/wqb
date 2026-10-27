# other128 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other128` |
| 名称 | Global Executive Performance Factors |
| 类别 | OTHER |
| 数据字段数(平台) | 18 |
| 覆盖率 | 0.4607 |
| 平台已有 alpha | 20 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg Global Identifiers (BBGID) and Reuters Instrument Codes (RIC), two widely used security identifiers in financial markets. By linking these identifiers, the dataset enables seamless cross-referencing of securities across Bloomberg and Refinitiv platforms, facilitating data integration, portfolio management, and research workflows. While not directly predictive of price movements, accurate identifier mapping is essential for consolidating data from multiple sources, ensuring data integrity, and supporting robust quantitative analysis and trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **18** |
| 类型分布 | VECTOR×18 |
| 平均覆盖率 | **0.461** |
| 覆盖率区间 | 0.39 ~ 0.71 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 4 | 22.2% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 14 | 77.8% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| DEAD | 6 | 33.3% |
| DEAD_STATIC | 4 | 22.2% |
| UNTESTED | 4 | 22.2% |
| UNUSABLE | 4 | 22.2% |

- 已实测字段：**10** 个（56%），best_sharpe 最高 **0.41**，中位 -0.04

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 风险与质量 | 10 | 0.39 | oth128_dmexusexecutiveefficiencyinput、oth128_dmexusscore、oth128_dmexusexecutiveefficiencyoutput |
| 情绪与新闻 | 2 | 0.39 | chief_exec_investor_sentiment_score_dmexus、finance_exec_investor_sentiment_score_dmexus |
| 宏观与行业 | 2 | 0.71 | oth128_dmexuscountry、oth128_dmexusgicssector |
| 盈利与财务 | 1 | 0.39 | oth128_dmexusceononcashcompensation |
| 元数据与非信号 | 1 | 0.71 | oth128_dmexuscompanyname |
| 交易与微观结构 | 1 | 0.71 | oth128_dmexusticker |
| 其他 | 1 | 0.39 | oth128_dmexusmarketcap |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth128_dmexusceononcashcompensation` | VECTOR | 0.389 | 盈利与财务 | 3 | 0.41 | 0.46 | 0.56 | DEAD | z-score of CEO non-cash compensation (e.g., equity/options awards) for the firm |
| 2 | `oth128_dmexusexecutiveefficiencyinput` | VECTOR | 0.389 | 风险与质量 | 1 | 0.09 | 0.43 | 0.04 | DEAD | z-score of Executive Input Efficiency |
| 3 | `chief_exec_investor_sentiment_score_dmexus` | VECTOR | 0.389 | 情绪与新闻 | 3 | 0.06 | 0.05 | -0.10 | DEAD | z-score of CEO Investor Confidence |
| 4 | `oth128_dmexusscore` | VECTOR | 0.389 | 风险与质量 | 5 | -0.03 | 0.49 | 0.22 | DEAD | Final Capri composite management quality score (unitless, normalized) for the company/date in DM ex-US |
| 5 | `oth128_dmexusexecutiveefficiencyoutput` | VECTOR | 0.389 | 风险与质量 | 3 | -0.04 | -0.33 | 0.19 | DEAD | z-score of Executive Output Efficiency |
| 6 | `oth128_dmexusceotenure` | VECTOR | 0.389 | 风险与质量 | 1 | -0.19 | 0.41 | 0.14 | DEAD_STATIC | z-score of CEO tenure |
| 7 | `oth128_dmexusceocashcompensation` | VECTOR | 0.389 | 风险与质量 | 2 | -0.22 | 0.26 | 0.01 | DEAD | z-score of CEO cash compensation |
| 8 | `oth128_dmexuskeyexecutiveice` | VECTOR | 0.389 | 风险与质量 | 2 | -0.24 | -0.47 | -0.15 | DEAD_STATIC | z-score of Investor Confidence for key executives (all C-suite) |
| 9 | `finance_exec_investor_sentiment_score_dmexus` | VECTOR | 0.389 | 情绪与新闻 | 1 | -0.29 | -1.03 | -0.14 | DEAD_STATIC | z-score of CFO Investor Confidence |
| 10 | `oth128_dmexuskeyexecutivetenure` | VECTOR | 0.389 | 风险与质量 | 1 | -0.53 | -0.93 | -0.34 | DEAD_STATIC | z-score of tenure across key executives (C-suite) |
| 11 | `oth128_dmexuscompanyname` | VECTOR | 0.711 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Company Name |
| 12 | `oth128_dmexuscountry` | VECTOR | 0.711 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country |
| 13 | `oth128_dmexusgicssector` | VECTOR | 0.711 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector |
| 14 | `oth128_dmexusticker` | VECTOR | 0.711 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Point in Time Ticker |
| 15 | `oth128_dmexuscfocashcompensation` | VECTOR | 0.389 | 风险与质量 | 0 | — | — | — | UNUSABLE | z-score of CFO cash compensation |
| 16 | `oth128_dmexuscfononcashcompensation` | VECTOR | 0.389 | 风险与质量 | 0 | — | — | — | UNUSABLE | z-score of CFO non-cash compensation |
| 17 | `oth128_dmexuscfotenure` | VECTOR | 0.389 | 风险与质量 | 0 | — | — | — | UNUSABLE | z-score of CFO tenure |
| 18 | `oth128_dmexusmarketcap` | VECTOR | 0.389 | 其他 | 0 | — | — | — | UNUSABLE | market cap in developed markets |

## 六、本地回测证据

- 本地累计回测 **22** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `QPKmj7mp` | 0.41 | 0.22 | 0.46 | 0.56 | 0.22 | ["LOW_SHARPE | s2_other128_d1 | `divide(vec_avg(oth128_dmexusceononcashcompensation), vec_avg(oth128_dmexusceocashcompensat` |
| `leKJzQp8` | 0.20 | 0.06 | 0.21 | 0.22 | 0.03 | ["LOW_SHARPE | s2_other128_d1_r2 | `divide(ts_backfill(vec_avg(oth128_dmexusceononcashcompensation), 66), abs(ts_backfill(vec_` |
| `kqgem1dg` | 0.09 | 0.02 | 0.43 | 0.04 | 0.27 | ["LOW_SHARPE | s2_other128_d1_r2 | `group_zscore(subtract(vec_avg(oth128_dmexusexecutiveefficiencyinput), vec_avg(oth128_dmexu` |
| `zqbXjY6X` | 0.06 | 0.02 | 0.05 | -0.10 | 0.12 | ["LOW_SHARPE | s2_other128_d1 | `if_else(greater(vec_avg(chief_exec_investor_sentiment_score_dmexus), 0), group_rank(ts_bac` |
| `P0gj67jW` | -0.03 | 0.00 | 0.43 | 0.20 | 0.02 | ["LOW_SHARPE | s2_other128_d1 | `group_rank(ts_delta(ts_backfill(vec_avg(oth128_dmexusscore), 252), 252), industry)` |
| `mL6eAje6` | -0.04 | 0.00 | -0.64 | 0.19 | 0.28 | ["LOW_SHARPE | s2_other128_d1 | `divide(vec_avg(oth128_dmexusexecutiveefficiencyoutput), abs(vec_avg(oth128_dmexusexecutive` |
| `blO7Mj7q` | -0.07 | -0.01 | -1.29 | -0.15 | 0.25 | ["LOW_SHARPE | s2_other128_d1 | `group_zscore(subtract(vec_avg(oth128_dmexusexecutiveefficiencyoutput), vec_avg(oth128_dmex` |
| `kqgeXjeL` | -0.09 | -0.01 | 0.20 | 0.17 | 0.02 | ["LOW_SHARPE | s2_other128_d1 | `add(group_rank(ts_backfill(vec_avg(oth128_dmexusscore), 66), subindustry), group_rank(ts_b` |
| `1YZ6Lxbz` | -0.09 | -0.02 | 0.49 | 0.12 | 0.30 | ["LOW_SHARPE | s2_other128_d1 | `group_zscore(subtract(vec_avg(oth128_dmexusscore), vec_avg(oth128_dmexusmarketcap)), subin` |
| `QPKmj3kg` | -0.13 | -0.03 | -0.58 | 0.03 | 0.22 | ["LOW_SHARPE | s2_other128_d1 | `group_rank(ts_backfill(vec_avg(oth128_dmexusscore), 252), bucket(rank(vec_avg(oth128_dmexu` |
| `akxXPAjw` | -0.16 | -0.03 | -0.33 | -0.06 | 0.01 | ["LOW_SHARPE | s2_other128_d1_r2 | `group_rank(ts_backfill(vec_avg(oth128_dmexusexecutiveefficiencyoutput), 66), subindustry)` |
| `58gN9l7M` | -0.19 | -0.04 | 0.41 | 0.14 | 0.01 | ["LOW_SHARPE | s2_other128_d1 | `group_rank(ts_backfill(vec_avg(oth128_dmexusceotenure), 252), industry)` |
| `d51emOVK` | -0.22 | -0.05 | 0.26 | -0.27 | 0.02 | ["LOW_SHARPE | s2_other128_d1 | `group_rank(ts_delta(ts_backfill(vec_avg(oth128_dmexusceocashcompensation), 252), 66), subi` |
| `blO7MRZZ` | -0.24 | -0.07 | -0.69 | -0.15 | 0.01 | ["LOW_SHARPE | s2_other128_d1 | `trade_when(greater(vec_avg(oth128_dmexuskeyexecutiveice), 0), group_rank(ts_backfill(vec_a` |
| `d51emjeY` | -0.27 | -0.11 | -0.40 | 0.01 | 0.17 | ["LOW_SHARPE | s2_other128_d1 | `group_rank(subtract(vec_avg(oth128_dmexusceocashcompensation), vec_avg(oth128_dmexuscfocas` |

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

