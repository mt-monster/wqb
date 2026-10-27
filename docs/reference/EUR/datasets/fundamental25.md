# fundamental25 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental25` |
| 名称 | Company Operating Metrics |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 8 |
| 覆盖率 | 0.2596 |
| 平台已有 alpha | 13 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive, standardized financial statement data and key operating metrics for companies covering 96% of global market capitalization. It includes annual and quarterly financials, per share data, calculated ratios, pricing, and textual information, enabling deep peer comparability across industries and regions. The dataset features over 1,500 data items such as income statement, balance sheet, cash flow, segment data, and supplemental metrics, with point-in-time history, restatements, and amendments. Analysts can use this rich dataset to assess company performance, financial health, and valuation, making it highly valuable for predicting price movements, screening for investment opportunities, and building quantitative models.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **8** |
| 类型分布 | VECTOR×8 |
| 平均覆盖率 | **0.260** |
| 覆盖率区间 | 0.25 ~ 0.30 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 8 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 8 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 8 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 4 | 0.26 | fnd25_updatetype、fnd25_interimnumber、fnd25_metricvalue |
| 元数据与非信号 | 3 | 0.26 | fnd25_metriccode、fnd25_fiscalyear、fnd25_periodtypecode |
| 盈利与财务 | 1 | 0.25 | fnd25_statementtypecode |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `fnd25_metriccode` | VECTOR | 0.300 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Metric code as an integer |
| 2 | `fnd25_updatetype` | VECTOR | 0.300 | 其他 | 0 | — | — | — | UNUSABLE | Update type provides information on how statements were formulated. Options include: UPD - Update Normal, UCA - Update Calculated, USP - Upd |
| 3 | `fnd25_fiscalyear` | VECTOR | 0.246 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Fiscal year identifier (numeric) |
| 4 | `fnd25_interimnumber` | VECTOR | 0.246 | 其他 | 0 | — | — | — | UNUSABLE | Sequence number within the fiscal year/period (e.g., 1 for Q1) |
| 5 | `fnd25_metricvalue` | VECTOR | 0.246 | 其他 | 0 | — | — | — | UNUSABLE | Numeric value of the operating metric |
| 6 | `fnd25_periodlength` | VECTOR | 0.246 | 其他 | 0 | — | — | — | UNUSABLE | Number of months or weeks covered by the reporting period, depending on reporting practices |
| 7 | `fnd25_periodtypecode` | VECTOR | 0.246 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Numeric code for reporting frequency; 1=annual, 2=quarterly, 3=semi-annual, 4=trimester |
| 8 | `fnd25_statementtypecode` | VECTOR | 0.246 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Code for statement context: 1=Profit & Loss, 3=Balance Sheet |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

