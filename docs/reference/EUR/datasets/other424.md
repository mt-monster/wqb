# other424 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other424` |
| 名称 | Dividend prediction model |
| 类别 | OTHER |
| 数据字段数(平台) | 3 |
| 覆盖率 | 0.6935 |
| 平台已有 alpha | 176 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a mapping between Bloomberg IDs (BBID) and Reuters Instrument Codes (RIC), serving as a cross-reference for security identifiers across two major financial data vendors. The data is sourced from both Bloomberg and Refinitiv, ensuring comprehensive coverage and accuracy. While primarily intended for operational and data management purposes rather than direct research or trading signal generation, this mapping is essential for integrating datasets, reconciling positions, and ensuring consistency in multi-vendor environments. Accurate identifier mapping can indirectly support price prediction by enabling seamless merging of disparate datasets, thus improving the quality and breadth of input data for quantitative models and research workflows.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **3** |
| 类型分布 | MATRIX×3 |
| 平均覆盖率 | **0.694** |
| 覆盖率区间 | 0.67 ~ 0.70 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 2 | 66.7% |
| 低 (0.50–0.70) | 1 | 33.3% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 3 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 2 | 0.69 | dividend_growth_factor_score、oth424_divyld |
| 宏观与行业 | 1 | 0.70 | oth424_mktcap |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `dividend_growth_factor_score` | MATRIX | 0.704 | 盈利与财务 | 0 | — | — | — | UNTESTED | GRID signal: predicted likelihood or strength of imminent dividend increase (range [0,1]), based on Wolfe's ML model |
| 2 | `oth424_mktcap` | MATRIX | 0.704 | 宏观与行业 | 0 | — | — | — | UNTESTED | Market capitalization of the company (currency/unit unspecified; treat as relative size) |
| 3 | `oth424_divyld` | MATRIX | 0.672 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend yield of the company (method of calculation unspecified) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

