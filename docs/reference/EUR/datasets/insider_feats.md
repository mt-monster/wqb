# insider_feats — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `insider_feats` |
| 名称 | Global Insider Transaction Features |
| 类别 | OTHER |
| 数据字段数(平台) | 118 |
| 覆盖率 | 0.5447 |
| 平台已有 alpha | 52 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive, structured features derived from global insider transactions, including purchases, sales, awards, and option exercises by company executives, directors, and major shareholders. It covers multiple regions and asset classes, with detailed metadata such as transaction type, insider role, ownership connection, trade significance, and post-transaction holdings. By aggregating and analyzing these transactions, the dataset enables the identification of potentially informative trades, such as opportunistic buying or selling, which can signal future price movements due to information asymmetry. Quantitative models and event studies built on this data can help forecast abnormal returns, enhance alpha generation, and improve risk-adjusted portfolio performance by 

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **118** |
| 类型分布 | MATRIX×118 |
| 平均覆盖率 | **0.545** |
| 覆盖率区间 | 0.16 ~ 0.92 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 31 | 26.3% |
| 中 (0.70–0.90) | 8 | 6.8% |
| 低 (0.50–0.70) | 17 | 14.4% |
| 稀疏 (<0.50) | 62 | 52.5% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 65 | 55.1% |
| UNTESTED | 43 | 36.4% |
| DEAD | 10 | 8.5% |

- 已实测字段：**10** 个（8%），best_sharpe 最高 **0.47**，中位 0.03

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 111 | 0.54 | top5_buy_tx_count_60d、top5_buy_tx_count_60d_2、top20_sale_tx_count_60d |
| 价量与波动 | 7 | 0.64 | top5_insider_sale_volume_lookback_250、top20_buy_to_sell_volume_ratio_lookback_10_filled、top5_buy_to_sell_volume_ratio_lookback_5_filled |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `top5_buy_tx_count_60d` | MATRIX | 0.272 | 持仓与资金流 | 1 | 0.47 | 0.13 | 0.41 | DEAD | Number of purchase transactions by the top 5 insiders over the last 60 days. |
| 2 | `top5_buy_tx_count_60d_2` | MATRIX | 0.272 | 持仓与资金流 | 1 | 0.28 | 0.40 | 0.57 | DEAD | Number of purchase transactions by the top 5 insiders over the last 60 days (alternate calculation). |
| 3 | `top20_sale_tx_count_60d` | MATRIX | 0.418 | 持仓与资金流 | 1 | 0.27 | -0.91 | 0.14 | DEAD | Number of sale transactions by the top 20 insiders over the last 60 days. |
| 4 | `top5_insider_sale_volume_lookback_250` | MATRIX | 0.514 | 价量与波动 | 1 | 0.05 | 0.15 | -0.13 | DEAD | Total shares sold by top 5 insiders over a 250-day period. |
| 5 | `top20_buy_to_sell_txn_ratio_lookback_20_filled` | MATRIX | 0.916 | 持仓与资金流 | 1 | 0.03 | -0.28 | 0.18 | DEAD | Ratio of purchase to sale transactions by top 20 insiders over 20 days, with missing data filled. |
| 6 | `top5_buy_to_sell_txn_ratio_lookback_20_filled` | MATRIX | 0.916 | 持仓与资金流 | 1 | 0.02 | 0.21 | 0.11 | DEAD | Ratio of purchase to sale transactions by top 5 insiders over 20 days, with missing data filled. |
| 7 | `top5_insider_sale_transaction_count_lookback_60` | MATRIX | 0.323 | 持仓与资金流 | 1 | 0.02 | 0.05 | -0.07 | DEAD | Number of sale transactions by top 5 insiders over a 60-day period. |
| 8 | `insider_buy_to_sell_transaction_ratio_lookback_60` | MATRIX | 0.726 | 持仓与资金流 | 1 | -0.14 | -0.79 | -0.06 | DEAD | Ratio of insider purchase to sale transactions over a 60-day period. |
| 9 | `total_insider_purchase_count_lookback_60` | MATRIX | 0.483 | 持仓与资金流 | 1 | -0.38 | -0.72 | -0.12 | DEAD | Total number of insider purchase transactions over a 60-day period. |
| 10 | `buy_sell_tx_count_ratio_top5_60d_filled` | MATRIX | 0.916 | 持仓与资金流 | 1 | -0.53 | -0.02 | 0.05 | DEAD | Ratio of purchase to sale transaction counts for the top 5 insiders over 60 days, with missing data filled. |
| 11 | `buy_sell_ratio_all_10d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for all insiders over 10 days, with missing data filled. |
| 12 | `buy_sell_ratio_all_20d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for all insiders over 20 days, with missing data filled. |
| 13 | `buy_sell_ratio_all_250d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for all insiders over 250 days, with missing data filled. |
| 14 | `buy_sell_ratio_all_5d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for all insiders over 5 days, with missing data filled. |
| 15 | `buy_sell_ratio_all_60d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for all insiders over 60 days, with missing data filled. |
| 16 | `buy_sell_ratio_top20_20d_filled_2` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 20 insiders over 20 days, with missing data filled (alternate calculation). |
| 17 | `buy_sell_ratio_top20_250d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 20 insiders over 250 days, with missing data filled. |
| 18 | `buy_sell_ratio_top20_5d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 20 insiders over 5 days, with missing data filled. |
| 19 | `buy_sell_ratio_top20_60d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 20 insiders over 60 days, with missing data filled. |
| 20 | `buy_sell_ratio_top5_20d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 5 insiders over 20 days, with missing data filled. |
| 21 | `buy_sell_ratio_top5_250d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 5 insiders over 250 days, with missing data filled. |
| 22 | `buy_sell_ratio_top5_60d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 5 insiders over 60 days, with missing data filled. |
| 23 | `buy_sell_tx_count_ratio_all_20d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for all insiders over 20 days, with missing data filled. |
| 24 | `buy_sell_tx_count_ratio_all_250d` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for all insiders over 250 days. |
| 25 | `buy_sell_tx_count_ratio_all_250d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for all insiders over 250 days, with missing data filled. |
| 26 | `buy_sell_tx_count_ratio_all_5d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for all insiders over 5 days, with missing data filled. |
| 27 | `buy_sell_tx_count_ratio_all_60d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for all insiders over 60 days, with missing data filled. |
| 28 | `buy_sell_tx_count_ratio_top20_10d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for the top 20 insiders over 10 days, with missing data filled. |
| 29 | `buy_sell_tx_count_ratio_top20_250d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for the top 20 insiders over 250 days, with missing data filled. |
| 30 | `buy_sell_tx_count_ratio_top20_5d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for the top 20 insiders over 5 days, with missing data filled. |
| 31 | `buy_sell_tx_count_ratio_top5_250d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for the top 5 insiders over 250 days, with missing data filled. |
| 32 | `buy_sell_tx_count_ratio_top5_5d_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for the top 5 insiders over 5 days, with missing data filled. |
| 33 | `buy_to_sell_ratio_all_250d` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of insider purchases to sales for all insiders over the last 250 days. |
| 34 | `buy_to_sell_txn_ratio_lookback_10_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transactions by all insiders over 10 days, with missing data filled. |
| 35 | `top20_buy_to_sell_txn_ratio_lookback_60_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transactions by top 20 insiders over 60 days, with missing data filled. |
| 36 | `top20_buy_to_sell_volume_ratio_lookback_10_filled` | MATRIX | 0.916 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of shares purchased to sold by top 20 insiders over 10 days, with missing data filled. |
| 37 | `top5_buy_to_sell_txn_ratio_lookback_10_filled` | MATRIX | 0.916 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transactions by top 5 insiders over 10 days, with missing data filled. |
| 38 | `top5_buy_to_sell_volume_ratio_lookback_5_filled` | MATRIX | 0.916 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of shares purchased to sold by top 5 insiders over 5 days, with missing data filled. |
| 39 | `buy_sell_tx_count_ratio_top20_250d` | MATRIX | 0.825 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for the top 20 insiders over 250 days. |
| 40 | `top20_buy_to_sell_volume_ratio_lookback_250` | MATRIX | 0.825 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of shares purchased to sold by top 20 insiders over a 250-day period. |
| 41 | `buy_sell_tx_count_ratio_top5_250d` | MATRIX | 0.755 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for the top 5 insiders over 250 days. |
| 42 | `buy_to_sell_ratio_top5_250d` | MATRIX | 0.755 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 5 insiders over the past 250 days. |
| 43 | `buy_to_sell_ratio_all_60d` | MATRIX | 0.726 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of insider purchases to sales for all insiders over the last 60 days. |
| 44 | `total_buy_tx_count_250d` | MATRIX | 0.723 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total number of insider purchase transactions over the past 250 days. |
| 45 | `total_buy_tx_count_250d_2` | MATRIX | 0.723 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total number of insider purchase transactions over the past 250 days (alternate calculation). |
| 46 | `total_sale_tx_count_250d` | MATRIX | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total number of insider sale transactions over the past 250 days. |
| 47 | `total_sale_tx_count_250d_2` | MATRIX | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total number of insider sale transactions over the past 250 days (alternate calculation). |
| 48 | `top20_sale_tx_count_250d` | MATRIX | 0.609 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of sale transactions by the top 20 insiders over the last 250 days. |
| 49 | `top20_sale_tx_count_250d_2` | MATRIX | 0.609 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Number of sale transactions by the top 20 insiders over the last 250 days (alternate calculation). |
| 50 | `buy_sell_tx_count_ratio_all_20d` | MATRIX | 0.609 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for all insiders over 20 days. |
| 51 | `buy_to_sell_ratio_all_20d` | MATRIX | 0.609 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of insider purchases to sales for all insiders over the last 20 days. |
| 52 | `buy_sell_tx_count_ratio_top20_60d` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchase to sale transaction counts for the top 20 insiders over 60 days. |
| 53 | `buy_to_sell_ratio_top20_60d` | MATRIX | 0.607 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of purchases to sales for the top 20 insiders over the past 60 days. |
| 54 | `buy_to_sell_ratio_10d` | MATRIX | 0.568 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of insider purchases to sales for all insiders over the last 10 days. |
| 55 | `buy_sell_tx_count_ratio_all_10d` | MATRIX | 0.567 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchase to sale transaction counts for all insiders over 10 days. |
| 56 | `buy_to_sell_volume_ratio_lookback_5` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ratio of shares purchased to sold by all insiders over a 5-day period. |
| 57 | `top20_buy_tx_count_250d` | MATRIX | 0.525 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 250 days. |
| 58 | `top20_buy_tx_count_250d_2` | MATRIX | 0.525 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 250 days (alternate calculation). |
| 59 | `buy_sell_tx_count_ratio_top5_60d` | MATRIX | 0.514 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchase to sale transaction counts for the top 5 insiders over 60 days. |
| 60 | `buy_to_sell_ratio_top5_60d` | MATRIX | 0.514 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchases to sales for the top 5 insiders over the past 60 days. |
| 61 | `top5_insider_sale_transaction_count_lookback_250` | MATRIX | 0.514 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by top 5 insiders over a 250-day period. |
| 62 | `buy_sell_tx_count_ratio_top20_20d` | MATRIX | 0.493 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchase to sale transaction counts for the top 20 insiders over 20 days. |
| 63 | `buy_to_sell_ratio_top20_20d` | MATRIX | 0.493 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchases to sales for the top 20 insiders over the past 20 days. |
| 64 | `total_insider_sale_transaction_count_lookback_60` | MATRIX | 0.488 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider sale transactions over a 60-day period. |
| 65 | `total_sale_tx_count_60d` | MATRIX | 0.488 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider sale transactions over the past 60 days. |
| 66 | `total_buy_tx_count_60d` | MATRIX | 0.483 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider purchase transactions over the past 60 days. |
| 67 | `top5_buy_tx_count_250d` | MATRIX | 0.466 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 5 insiders over the last 250 days. |
| 68 | `top5_insider_buy_count_250d` | MATRIX | 0.466 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 5 insiders over the last 250 days. |
| 69 | `buy_sell_tx_count_ratio_top20_10d` | MATRIX | 0.455 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchase to sale transaction counts for the top 20 insiders over 10 days. |
| 70 | `buy_to_sell_ratio_top20_10d` | MATRIX | 0.455 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchases to sales for the top 20 insiders over the past 10 days. |
| 71 | `buy_sell_tx_count_ratio_top20_5d` | MATRIX | 0.431 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchase to sale transaction counts for the top 20 insiders over 5 days. |
| 72 | `buy_to_sell_ratio_top20_5d` | MATRIX | 0.431 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchases to sales for the top 20 insiders over the past 5 days. |
| 73 | `top20_insider_sale_count_60d` | MATRIX | 0.418 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 20 insiders over the last 60 days. |
| 74 | `buy_sell_tx_count_ratio_top5_20d` | MATRIX | 0.402 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchase to sale transaction counts for the top 5 insiders over 20 days. |
| 75 | `buy_to_sell_ratio_top5_20d` | MATRIX | 0.402 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchases to sales for the top 5 insiders over the past 20 days. |
| 76 | `total_insider_sale_count_20d` | MATRIX | 0.391 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider sale transactions over the past 20 days. |
| 77 | `total_insider_sale_volume_lookback_20` | MATRIX | 0.391 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total shares sold by all insiders over a 20-day period. |
| 78 | `total_buy_tx_count_20d_2` | MATRIX | 0.379 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider purchase transactions over the past 20 days (alternate calculation). |
| 79 | `total_insider_buy_count_20d` | MATRIX | 0.379 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider purchase transactions over the past 20 days. |
| 80 | `buy_sell_tx_count_ratio_top5_10d` | MATRIX | 0.366 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchase to sale transaction counts for the top 5 insiders over 10 days. |
| 81 | `buy_to_sell_ratio_top5_10d` | MATRIX | 0.366 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchases to sales for the top 5 insiders over the past 10 days. |
| 82 | `total_insider_sale_volume_lookback_10` | MATRIX | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total shares sold by all insiders over a 10-day period. |
| 83 | `total_sale_tx_count_10d` | MATRIX | 0.359 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider sale transactions over the past 10 days. |
| 84 | `total_buy_tx_count_10d` | MATRIX | 0.346 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider purchase transactions over the past 10 days. |
| 85 | `total_insider_purchase_count_lookback_10` | MATRIX | 0.346 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider purchase transactions over a 10-day period. |
| 86 | `buy_sell_tx_count_ratio_top5_5d` | MATRIX | 0.344 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchase to sale transaction counts for the top 5 insiders over 5 days. |
| 87 | `buy_to_sell_ratio_top5_5d` | MATRIX | 0.344 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Ratio of purchases to sales for the top 5 insiders over the past 5 days. |
| 88 | `total_insider_sale_transaction_count_lookback_5` | MATRIX | 0.340 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider sale transactions over a 5-day period. |
| 89 | `total_sale_tx_count_5d` | MATRIX | 0.340 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider sale transactions over the past 5 days. |
| 90 | `top20_sale_tx_count_20d` | MATRIX | 0.332 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 20 insiders over the last 20 days. |
| 91 | `top20_sale_tx_count_20d_2` | MATRIX | 0.332 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 20 insiders over the last 20 days (alternate calculation). |
| 92 | `total_buy_tx_count_5d` | MATRIX | 0.326 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider purchase transactions over the past 5 days. |
| 93 | `total_buy_tx_count_5d_2` | MATRIX | 0.326 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total number of insider purchase transactions over the past 5 days (alternate calculation). |
| 94 | `top5_sale_tx_count_60d` | MATRIX | 0.323 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 5 insiders over the last 60 days. |
| 95 | `top20_buy_tx_count_60d` | MATRIX | 0.318 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 60 days. |
| 96 | `top20_buy_tx_count_60d_2` | MATRIX | 0.318 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 60 days (alternate calculation). |
| 97 | `top20_sale_tx_count_10d` | MATRIX | 0.305 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 20 insiders over the last 10 days. |
| 98 | `top20_sale_tx_count_10d_2` | MATRIX | 0.305 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 20 insiders over the last 10 days (alternate calculation). |
| 99 | `top20_sale_tx_count_5d` | MATRIX | 0.288 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 20 insiders over the last 5 days. |
| 100 | `top20_sale_tx_count_5d_2` | MATRIX | 0.288 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 20 insiders over the last 5 days (alternate calculation). |
| 101 | `top20_buy_tx_count_20d` | MATRIX | 0.214 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 20 days. |
| 102 | `top20_buy_tx_count_20d_2` | MATRIX | 0.214 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 20 days (alternate calculation). |
| 103 | `top5_insider_sale_transaction_count_lookback_20` | MATRIX | 0.207 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by top 5 insiders over a 20-day period. |
| 104 | `top5_sale_tx_count_20d` | MATRIX | 0.207 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 5 insiders over the last 20 days. |
| 105 | `top20_buy_tx_count_10d` | MATRIX | 0.196 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 10 days. |
| 106 | `top20_buy_tx_count_10d_2` | MATRIX | 0.196 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 10 days (alternate calculation). |
| 107 | `top5_sale_tx_count_10d` | MATRIX | 0.190 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 5 insiders over the last 10 days. |
| 108 | `top5_sale_tx_count_10d_2` | MATRIX | 0.190 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 5 insiders over the last 10 days (alternate calculation). |
| 109 | `top20_buy_tx_count_5d` | MATRIX | 0.187 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 5 days. |
| 110 | `top20_buy_tx_count_5d_2` | MATRIX | 0.187 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 20 insiders over the last 5 days (alternate calculation). |
| 111 | `top5_buy_tx_count_20d` | MATRIX | 0.183 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 5 insiders over the last 20 days. |
| 112 | `top5_buy_tx_count_20d_2` | MATRIX | 0.183 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 5 insiders over the last 20 days (alternate calculation). |
| 113 | `top5_sale_tx_count_5d` | MATRIX | 0.181 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 5 insiders over the last 5 days. |
| 114 | `top5_sale_tx_count_5d_2` | MATRIX | 0.181 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of sale transactions by the top 5 insiders over the last 5 days (alternate calculation). |
| 115 | `top5_buy_tx_count_10d` | MATRIX | 0.167 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 5 insiders over the last 10 days. |
| 116 | `top5_buy_tx_count_10d_2` | MATRIX | 0.167 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 5 insiders over the last 10 days (alternate calculation). |
| 117 | `top5_buy_tx_count_5d` | MATRIX | 0.159 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 5 insiders over the last 5 days. |
| 118 | `top5_buy_tx_count_5d_2` | MATRIX | 0.159 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of purchase transactions by the top 5 insiders over the last 5 days (alternate calculation). |

## 六、本地回测证据

- 本地累计回测 **10** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `xA3jjqMq` | 0.47 | 0.32 | 0.13 | 0.41 | 0.04 | ["LOW_SHARPE | 238 | `divide(subtract(ts_backfill(top5_buy_tx_count_60d,66), ts_backfill(top20_sale_tx_count_60d` |
| `1YXwwe5R` | 0.28 | 0.17 | 0.40 | 0.57 | 0.04 | ["LOW_SHARPE | 238 | `divide(subtract(ts_backfill(top5_buy_tx_count_60d_2,66), ts_backfill(top20_sale_tx_count_6` |
| `O0N77OEg` | 0.27 | 0.13 | -0.91 | 0.14 | 0.04 | ["LOW_SHARPE | 238 | `divide(subtract(ts_backfill(top20_sale_tx_count_60d,66), ts_backfill(top5_sale_tx_count_60` |
| `blbjQAAm` | 0.05 | 0.01 | 0.15 | -0.13 | 0.03 | ["LOW_SHARPE | 238 | `group_neutralize(divide(top5_insider_sale_volume_lookback_250, add(multiply(top5_insider_s` |
| `ZYb776kZ` | 0.03 | 0.00 | -0.28 | 0.18 | 0.06 | ["LOW_SHARPE | 238 | `divide(ts_backfill(top20_buy_to_sell_txn_ratio_lookback_20_filled,44), ts_backfill(top20_b` |
| `RRb7mPP0` | 0.02 | 0.00 | 0.21 | 0.11 | 0.06 | ["LOW_SHARPE | 238 | `divide(ts_backfill(top5_buy_to_sell_txn_ratio_lookback_20_filled,44), ts_backfill(top20_bu` |
| `0mXwwqo8` | 0.02 | 0.00 | 0.05 | -0.07 | 0.05 | ["LOW_SHARPE | 238 | `divide(ts_av_diff(ts_backfill(top5_insider_sale_transaction_count_lookback_60,22), 252), a` |
| `pwRjjm0v` | -0.14 | -0.03 | -0.79 | -0.06 | 0.05 | ["LOW_SHARPE | 238 | `divide(ts_av_diff(ts_backfill(insider_buy_to_sell_transaction_ratio_lookback_60,22), 252),` |
| `akb776Jw` | -0.38 | -0.26 | -0.72 | -0.12 | 0.06 | ["LOW_SHARPE | 238 | `divide(ts_av_diff(ts_backfill(total_insider_purchase_count_lookback_60,22), 252), add(ts_s` |
| `MPa7GVV6` | -0.53 | -0.36 | -0.02 | 0.05 | 0.18 | ["LOW_SHARPE | 238 | `group_mean(buy_sell_tx_count_ratio_top5_60d_filled, top20_buy_tx_count_250d_2, sector)` |

## 七、判死记录（sealed dead_end）

- `EUR-EVENT-RELATION-WEAK`（2026-09-23T18:22:52）family=event_relation 实体关系强度族（relation_strength_rank/score × merger/partner/financial/general）：{"family": "event_relation 实体关系强度族（relation_strength_rank/score × merger/partner/financial/general）", "reason": "wave233 8 探针全灭 max/sharpe/=0.43 < 0.5 → 达 EUR fast_kill 判死线。字段全冷门（users<=1）理论 prod≈0，纯信号缺席。OTHER 塔已连续三集判死（acquisition_model 0.16 / insider_feats 多样性墙 / event_relation 0.43）。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-
- `EUR-INSIDER-FEATS-WEAK`（2026-09-23T18:35:49）family=insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback）：{"family": "insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback）", "reason": "wave238 10 探针全灭 best /sharpe/=0.47 < 0.5 → 达 fast_kill 判死线。此前 w232 多样性闸（flow 单 exposure）+ 字段名拼接幻觉 + 低覆盖无 backfill 三轮门禁墙已记录。OTHER 塔 4 候选全灭（acquisition_model/insider_feats/event_relation + ml_factor_proj 平台无字段）。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at

