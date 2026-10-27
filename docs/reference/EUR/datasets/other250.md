# other250 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other250` |
| 名称 | details data |
| 类别 | OTHER |
| 数据字段数(平台) | 12 |
| 覆盖率 | 0.4899 |
| 平台已有 alpha | 22 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBID) and Refinitiv Instrument Codes (RIC), facilitating the cross-referencing of securities across two major financial data platforms. By enabling seamless integration and reconciliation of security identifiers, it supports accurate data aggregation, portfolio management, and multi-source analytics. While not directly predictive of price movements, this mapping is essential for researchers and analysts who need to merge datasets, track instruments across systems, and ensure consistency in security-level analysis, which can indirectly enhance the quality and reliability of quantitative models and trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **12** |
| 类型分布 | VECTOR×12 |
| 平均覆盖率 | **0.490** |
| 覆盖率区间 | 0.49 ~ 0.49 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 12 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 12 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 12 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 6 | 0.49 | oth250_item_display_price、oth250_price_range_max、oth250_price_range_min |
| 其他 | 3 | 0.49 | oth250_item_rating、oth250_item_review_count、total_review_number |
| 风险与质量 | 2 | 0.49 | average_star_score、oth250_rank |
| 持仓与资金流 | 1 | 0.49 | sales_position_rank |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `average_star_score` | VECTOR | 0.490 | 风险与质量 | 0 | — | — | — | UNUSABLE | Average customer star rating of the item at collection time, typically on a 0–5 scale |
| 2 | `oth250_item_display_price` | VECTOR | 0.490 | 价量与波动 | 0 | — | — | — | UNUSABLE | Displayed list price of the item at the parse date, in the local currency of the site |
| 3 | `oth250_item_rating` | VECTOR | 0.490 | 其他 | 0 | — | — | — | UNUSABLE | Average customer star rating at parse time, typically on a 0 to 5 scale |
| 4 | `oth250_item_review_count` | VECTOR | 0.490 | 其他 | 0 | — | — | — | UNUSABLE | Total number of customer reviews at parse time |
| 5 | `oth250_price_range_max` | VECTOR | 0.490 | 价量与波动 | 0 | — | — | — | UNUSABLE | Maximum listed price shown when a price range is displayed for the item, in USD |
| 6 | `oth250_price_range_min` | VECTOR | 0.490 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum listed price shown when a price range is displayed for the item, in USD |
| 7 | `oth250_rank` | VECTOR | 0.490 | 风险与质量 | 0 | — | — | — | UNUSABLE | Bestseller rank of the item within its category on that date, where 1 is best |
| 8 | `product_listed_price` | VECTOR | 0.490 | 价量与波动 | 0 | — | — | — | UNUSABLE | Displayed list price of the item at parse time (USD) |
| 9 | `product_price_lower_bound` | VECTOR | 0.490 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum listed price observed when a price range is shown, in the local currency |
| 10 | `product_price_upper_bound` | VECTOR | 0.490 | 价量与波动 | 0 | — | — | — | UNUSABLE | Maximum listed price shown for the item when a price range is displayed (USD) |
| 11 | `sales_position_rank` | VECTOR | 0.490 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Bestseller rank position of the item within its category on the parse date; lower values indicate higher popularity |
| 12 | `total_review_number` | VECTOR | 0.490 | 其他 | 0 | — | — | — | UNUSABLE | Total number of customer reviews the item had at the time of data collection |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

