# digital_ad_spend — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `digital_ad_spend` |
| 名称 | Digital Advertising Spend Intelligence |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 6 |
| 覆盖率 | 0.1725 |
| 平台已有 alpha | 1 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive estimates of digital advertising spend and related metadata across a wide range of websites and social media platforms, including details on brands, categories, channels, creatives, and purchase paths. It tracks ad impressions, spend, creative types, and the route each ad takes from advertiser to publisher, offering granular insights into advertising strategies and market presence. By analyzing trends in ad spend, creative deployment, and targeting strategies, researchers can gauge shifts in marketing intensity, brand competition, and consumer engagement, which may serve as leading indicators for price movements in related equities or sectors. The dataset is particularly valuable for identifying changes in digital marketing activity that could signal upc

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **6** |
| 类型分布 | VECTOR×6 |
| 平均覆盖率 | **0.172** |
| 覆盖率区间 | 0.17 ~ 0.17 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 6 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 6 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 6 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 3 | 0.17 | ad_display_count、estimated_ad_spend、estimated_local_ad_spend |
| 宏观与行业 | 2 | 0.17 | ad_purchase_channel、ad_sales_channel |
| 其他 | 1 | 0.17 | ad_content_format |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `ad_content_format` | VECTOR | 0.172 | 其他 | 0 | — | — | — | UNUSABLE | Format/type of the ad creative |
| 2 | `ad_display_count` | VECTOR | 0.172 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated number of ad exposures (impressions count) |
| 3 | `ad_purchase_channel` | VECTOR | 0.172 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Enumerated code indicating the channel through which media was purchased (e.g., direct, DSP, ad network) |
| 4 | `ad_sales_channel` | VECTOR | 0.172 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Enumerated code indicating the channel through which the ad inventory was sold or distributed (e.g., direct, SSP, exchange) |
| 5 | `estimated_ad_spend` | VECTOR | 0.172 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total advertising spend for the record in USD (normalized amount) |
| 6 | `estimated_local_ad_spend` | VECTOR | 0.172 | 修正与预期 | 0 | — | — | — | UNUSABLE | Advertising spend in original/local currency (pre-normalization; unconverted) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

