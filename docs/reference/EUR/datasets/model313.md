# model313 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model313` |
| 名称 | Intangible Asset Factors |
| 类别 | MODEL |
| 数据字段数(平台) | 8 |
| 覆盖率 | 0.6624 |
| 平台已有 alpha | 6 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBID) and Refinitiv Instrument Codes (RIC), enabling seamless cross-referencing of securities across two major financial data platforms. By facilitating the integration and reconciliation of data from Bloomberg and Refinitiv, it supports accurate security identification, data aggregation, and portfolio management. While not directly predictive of price movements, this mapping is essential for researchers and analysts who require reliable linkage of market data, corporate actions, and analytics from multiple sources, thereby improving the quality and consistency of downstream quantitative models and trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **8** |
| 类型分布 | MATRIX×8 |
| 平均覆盖率 | **0.662** |
| 覆盖率区间 | 0.47 ~ 0.78 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 5 | 62.5% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 3 | 37.5% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 5 | 62.5% |
| UNUSABLE | 3 | 37.5% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 5 / UNUSABLE 3 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 元数据与非信号 | 3 | 0.68 | mdl313_atlas_unit_name、mdl313_companyname、mdl313_mktcap_usd |
| 宏观与行业 | 2 | 0.78 | mdl313_sector、mdl313_sub_industry |
| 交易与微观结构 | 1 | 0.78 | mdl313_ticker |
| 盈利与财务 | 1 | 0.47 | mdl313_iai |
| 风险与质量 | 1 | 0.47 | mdl313_ico |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl313_atlas_unit_name` | MATRIX | 0.779 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Atlas unit name |
| 2 | `mdl313_companyname` | MATRIX | 0.779 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Company Name |
| 3 | `mdl313_sector` | MATRIX | 0.779 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector |
| 4 | `mdl313_sub_industry` | MATRIX | 0.779 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sub Industry |
| 5 | `mdl313_ticker` | MATRIX | 0.779 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Exchange Ticker |
| 6 | `mdl313_iai` | MATRIX | 0.468 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Intangible Asset Intensity Score (composite of KCI and OCI), normalized [0,1] |
| 7 | `mdl313_ico` | MATRIX | 0.468 | 风险与质量 | 0 | — | — | — | UNUSABLE | Organizational Capital Intensity Score, calculated from capitalized SG&A, normalized [0,1] |
| 8 | `mdl313_mktcap_usd` | MATRIX | 0.468 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Market capitalization of the company in US dollars as of the observation date |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

