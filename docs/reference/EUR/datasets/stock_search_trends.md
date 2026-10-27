# stock_search_trends — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `stock_search_trends` |
| 名称 | US Stock Search Trend Matrix |
| 类别 | OTHER |
| 数据字段数(平台) | 6 |
| 覆盖率 | 0.5401 |
| 平台已有 alpha | 2 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset transforms web search trend data for the top 3000 US stocks into structured fields suitable for financial analysis. By leveraging daily and hourly search popularity scores for company names and ticker symbols, it provides a time series of public interest in individual stocks, including coverage on weekends and holidays. The data is normalized and decomposed to facilitate robust comparisons and feature generation, making it easier for researchers to extract meaningful signals. Increased search activity can reflect shifts in investor attention or sentiment, which may precede price movements, making this dataset valuable for predicting short-term and long-term stock returns.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **6** |
| 类型分布 | MATRIX×6 |
| 平均覆盖率 | **0.540** |
| 覆盖率区间 | 0.52 ~ 0.55 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 6 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 6 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 6 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 宏观与行业 | 6 | 0.54 | search_interest_7d_corporate_name、search_interest_14d_corporate_name、search_interest_28d_corporate_name |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `search_interest_7d_corporate_name` | MATRIX | 0.546 | 宏观与行业 | 0 | — | — | — | UNUSABLE | 7-day rolling average of daily Google Trends search-interest for company-name queries in the USA; 0–100 scale (D1) |
| 2 | `search_interest_14d_corporate_name` | MATRIX | 0.546 | 宏观与行业 | 0 | — | — | — | UNUSABLE | 14-day rolling average of daily Google Trends search-interest for company-name queries in the USA; 0–100 scale (D1) |
| 3 | `search_interest_28d_corporate_name` | MATRIX | 0.545 | 宏观与行业 | 0 | — | — | — | UNUSABLE | 28-day rolling average of daily Google Trends search-interest for company-name queries in the USA; 0–100 scale (D1) |
| 4 | `search_interest_84d_corporate_name` | MATRIX | 0.544 | 宏观与行业 | 0 | — | — | — | UNUSABLE | 84-day rolling average of daily Google Trends search-interest for company-name queries in the USA; 0–100 scale (D1) |
| 5 | `search_interest_today_corporate_name` | MATRIX | 0.539 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Latest complete calendar day Google Trends search-interest value for company-name queries in the USA; daily point-in-time value on Google’s  |
| 6 | `search_interest_1y_corporate_name` | MATRIX | 0.520 | 宏观与行业 | 0 | — | — | — | UNUSABLE | 364-day rolling average of daily Google Trends search-interest for company-name queries in the USA; 0–100 scale (D1) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

