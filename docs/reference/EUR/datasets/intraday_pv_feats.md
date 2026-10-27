# intraday_pv_feats — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `intraday_pv_feats` |
| 名称 | Daily Intraday Price Volume Features |
| 类别 | PV |
| 数据字段数(平台) | 585 |
| 覆盖率 | 0.9548 |
| 平台已有 alpha | 62 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides daily aggregated features derived from intraday price and volume data across global equity markets. By processing interval-level trading statistics—such as bid-ask spreads, order book depth, trade counts, volatility, and volume—into daily summaries, it enables consistent cross-regional analysis despite differences in exchange hours and data structures. These features are valuable for quantitative researchers and portfolio managers seeking to generate alpha signals, as they capture nuanced intraday market dynamics that can precede price movements. The dataset’s unified format and broad coverage make it a powerful tool for predicting short-term price changes and enhancing trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **585** |
| 类型分布 | MATRIX×585 |
| 平均覆盖率 | **0.955** |
| 覆盖率区间 | 0.41 ~ 1.00 |
| 更新频率（推断） | 日内（分钟/逐笔） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 553 | 94.5% |
| 中 (0.70–0.90) | 28 | 4.8% |
| 低 (0.50–0.70) | 1 | 0.2% |
| 稀疏 (<0.50) | 3 | 0.5% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 578 | 98.8% |
| DEAD | 4 | 0.7% |
| UNUSABLE | 3 | 0.5% |

- 已实测字段：**4** 个（1%），best_sharpe 最高 **1.07**，中位 0.23

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 565 | 0.95 | mean_trade_volume_30m_pre_close_2、corr_bid_with_ask_price_last_half、corr_interval_vwap_with_interval_twap_2 |
| 其他 | 16 | 0.98 | max_slippage_30m_pre_close_2、max_slippage_60m_pre_close_2、mean_slippage_30m_pre_close |
| 交易与微观结构 | 4 | 0.97 | min_slippage_interval_2、std_slippage_interval、slippage_first_interval |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mean_trade_volume_30m_pre_close_2` | MATRIX | 0.992 | 价量与波动 | 4 | 1.07 | — | 0.55 | DEAD | Average trading volume in the last 30 minutes before market close. |
| 2 | `corr_bid_with_ask_price_last_half` | MATRIX | 0.938 | 价量与波动 | 1 | 0.23 | — | — | DEAD | Correlation between bid price and ask price in the last 50% of the session. |
| 3 | `corr_interval_vwap_with_interval_twap_2` | MATRIX | 0.964 | 价量与波动 | 1 | -0.54 | — | — | DEAD | Pearson correlation across intraday intervals between interval VWAP and interval TWAP for the day (D1) |
| 4 | `corr_high_with_low_price_last_half` | MATRIX | 0.873 | 价量与波动 | 1 | -0.69 | — | — | DEAD | Correlation between high price and low price in the last 50% of the session. |
| 5 | `last_trade_price_30m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Last trade price at the 30-minute mark before market close. |
| 6 | `last_trade_price_60m_post_open` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Last trade price recorded 60 minutes after market open. |
| 7 | `last_trade_price_60m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Last trade price at the 60-minute mark before market close. |
| 8 | `last_trade_price_last_interval` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Last intraday observation of the last trade price at the end of the trading session |
| 9 | `max_last_trade_price_30m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum last traded price observed within the last 30 minutes before the exchange close |
| 10 | `max_last_trade_price_60m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum last-traded price during the 60 minutes before close |
| 11 | `mean_last_trade_price_30m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average last-traded price over the 30 minutes before close |
| 12 | `mean_last_trade_price_60m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average last-traded price over the 60 minutes before close |
| 13 | `mean_last_trade_price_return_30m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the last trade price in the last 30 minutes before market close. |
| 14 | `mean_last_trade_price_return_60m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the last trade price in the last 60 minutes before market close. |
| 15 | `mean_price_modulo_100_ratio_30m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 100 in the last 30 minutes before market close. |
| 16 | `mean_price_modulo_100_ratio_60m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 100 in the last 60 minutes before market close. |
| 17 | `mean_price_modulo_10_ratio_30m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 10 in the last 30 minutes before market close. |
| 18 | `mean_price_modulo_10_ratio_60m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 10 in the last 60 minutes before market close. |
| 19 | `mean_price_modulo_1_ratio_30m_pre_close` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 1 over the last 30 minutes before market close. |
| 20 | `mean_price_modulo_1_ratio_60m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 1 in the last 60 minutes before market close. |
| 21 | `min_last_trade_price_30m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum last-traded price during the last 30 minutes before the close |
| 22 | `min_last_trade_price_60m_pre_close_2` | MATRIX | 0.999 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum last trade price during the last 60 minutes before the market close |
| 23 | `max_slippage_30m_pre_close_2` | MATRIX | 0.992 | 其他 | 0 | — | — | — | UNTESTED | Maximum observed slippage in the last 30 minutes before market close. |
| 24 | `max_slippage_60m_pre_close_2` | MATRIX | 0.992 | 其他 | 0 | — | — | — | UNTESTED | Maximum observed slippage in the last 60 minutes before market close. |
| 25 | `max_trade_volume_30m_pre_close_2` | MATRIX | 0.992 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum trading volume in the last 30 minutes before market close. |
| 26 | `max_trade_volume_60m_pre_close_2` | MATRIX | 0.992 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum interval trading volume observed in the 60 minutes before the close |
| 27 | `mean_slippage_30m_pre_close` | MATRIX | 0.992 | 其他 | 0 | — | — | — | UNTESTED | Average slippage over the last 30 minutes before market close. |
| 28 | `mean_slippage_60m_pre_close_2` | MATRIX | 0.992 | 其他 | 0 | — | — | — | UNTESTED | Average observed slippage in the last 60 minutes before market close. |
| 29 | `mean_trade_volume_60m_pre_close` | MATRIX | 0.992 | 价量与波动 | 0 | — | — | — | UNTESTED | Average trade volume over the last 60 minutes before market close. |
| 30 | `min_slippage_30m_pre_close_2` | MATRIX | 0.992 | 其他 | 0 | — | — | — | UNTESTED | Minimum observed slippage in the last 30 minutes before market close. |
| 31 | `min_slippage_60m_pre_close_2` | MATRIX | 0.992 | 其他 | 0 | — | — | — | UNTESTED | Minimum observed slippage in the last 60 minutes before market close. |
| 32 | `min_trade_volume_30m_pre_close_2` | MATRIX | 0.992 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum trading volume in the last 30 minutes before market close. |
| 33 | `min_trade_volume_60m_pre_close_2` | MATRIX | 0.992 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum interval trading volume within the 60 minutes before the close |
| 34 | `slippage_last_interval` | MATRIX | 0.992 | 其他 | 0 | — | — | — | UNTESTED | Slippage value in the last interval of the day. |
| 35 | `trade_volume_last_interval` | MATRIX | 0.992 | 价量与波动 | 0 | — | — | — | UNTESTED | Trade volume in the last interval of the day. |
| 36 | `last_trade_price_30m_post_open` | MATRIX | 0.992 | 价量与波动 | 0 | — | — | — | UNTESTED | Last trade price recorded 30 minutes after market open. |
| 37 | `high_price_last_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Last observed intraday high (final interval's high) of the session |
| 38 | `low_price_last_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Low price in the last interval of the day. |
| 39 | `max_high_price_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest high price reached during the last 30 minutes before the close |
| 40 | `max_high_price_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum of the high price series within the last 60 minutes before the exchange close |
| 41 | `max_low_price_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum low price in the last 30 minutes before market close. |
| 42 | `max_low_price_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum low price in the last 60 minutes before market close. |
| 43 | `mean_high_price_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average high price in the last 30 minutes before market close. |
| 44 | `mean_high_price_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average high price in the last 60 minutes before market close. |
| 45 | `mean_high_price_return_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the high price in the last 30 minutes before market close. |
| 46 | `mean_high_price_return_60m_pre_close` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of high price in the last 60 minutes before market close. |
| 47 | `mean_low_price_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average low price in the last 30 minutes before market close. |
| 48 | `mean_low_price_60m_pre_close` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average low price over the last 60 minutes before market close. |
| 49 | `mean_low_price_return_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the low price in the last 30 minutes before market close. |
| 50 | `mean_low_price_return_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the low price in the last 60 minutes before market close. |
| 51 | `min_high_price_30m_pre_close` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum high price observed in the last 30 minutes before market close. |
| 52 | `min_high_price_60m_pre_close` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum high price observed in the last 60 minutes before market close. |
| 53 | `min_low_price_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the low price series within the last 30 minutes before the exchange close |
| 54 | `min_low_price_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum intraday low price observed during the last 60 minutes before the local market close |
| 55 | `high_price_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | High price at the 30-minute mark before market close. |
| 56 | `low_price_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Low price at the 30-minute mark before market close. |
| 57 | `high_price_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | High price at the 60-minute mark before market close. |
| 58 | `low_price_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Low price at the 60-minute mark before market close. |
| 59 | `max_vwap_30m_pre_close` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum volume-weighted average price in the last 30 minutes before market close. |
| 60 | `max_vwap_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum volume-weighted average price in the last 60 minutes before market close. |
| 61 | `mean_vwap_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of intraday VWAP values over the last 30 minutes before the exchange close |
| 62 | `mean_vwap_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average VWAP over the last 60 minutes before the market close |
| 63 | `mean_vwap_return_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the volume-weighted average price in the last 30 minutes before market close. |
| 64 | `mean_vwap_return_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the volume-weighted average price in the last 60 minutes before market close. |
| 65 | `min_vwap_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum volume-weighted average price in the last 30 minutes before market close. |
| 66 | `min_vwap_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum volume-weighted average price in the last 60 minutes before market close. |
| 67 | `vwap_last_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Last value of the intraday VWAP series (final interval) on the prior trading day |
| 68 | `vwap_30m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume-weighted average price in the last 30 minutes before market close. |
| 69 | `kurtosis_last_trade_price_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Kurtosis of the intraday last-traded price series over the session |
| 70 | `last_trade_price_first_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | First intraday observation of the last trade price at the start of the trading session |
| 71 | `max_last_trade_price_30m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum last traded price during the first 30 minutes after the exchange open |
| 72 | `max_last_trade_price_60m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum last-traded price observed during the first 60 minutes after the exchange opens |
| 73 | `max_last_trade_price_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum of the intraday last-traded price during the session |
| 74 | `mean_last_trade_price_30m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | arithmetic mean of the last traded price over the first 30 minutes since market open |
| 75 | `mean_last_trade_price_60m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | arithmetic mean of the last traded price over the first 60 minutes since market open |
| 76 | `mean_last_trade_price_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of the intraday last trade price across all intervals during the trading session, computed from the prior day’s int |
| 77 | `mean_last_trade_price_return_30m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean intraday return of the last-trade price computed over intervals within the first 30 minutes after market open |
| 78 | `mean_last_trade_price_return_60m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean intraday return of the last-trade price computed over intervals within the first 60 minutes after market open |
| 79 | `mean_price_modulo_100_ratio_30m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 100 over the first 30 minutes after market open. |
| 80 | `mean_price_modulo_100_ratio_60m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 100 over the first 60 minutes after market open. |
| 81 | `mean_price_modulo_100_ratio_daily` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 100 for the day. |
| 82 | `mean_price_modulo_10_ratio_30m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 10 over the first 30 minutes after market open. |
| 83 | `mean_price_modulo_10_ratio_60m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 10 over the first 60 minutes after market open. |
| 84 | `mean_price_modulo_10_ratio_daily` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 10 for the day. |
| 85 | `mean_price_modulo_1_ratio_30m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 1 over the first 30 minutes after market open. |
| 86 | `mean_price_modulo_1_ratio_60m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 1 over the first 60 minutes after market open. |
| 87 | `mean_price_modulo_1_ratio_daily` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 1 for the day. |
| 88 | `mean_return_last_trade_price_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean intraday return of the last trade price series computed across intervals during the session |
| 89 | `min_last_trade_price_30m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum last-trade price observed during the first 30 minutes after market open |
| 90 | `min_last_trade_price_60m_post_open` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum last-traded price observed during the first 60 minutes after the exchange opens |
| 91 | `min_last_trade_price_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the intraday last-traded price across the session |
| 92 | `momentum2_last_trade_price_daily` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of last trade price for the day. |
| 93 | `skew_last_trade_price_interval` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the intraday last-traded price series over the session |
| 94 | `vwap_60m_pre_close_2` | MATRIX | 0.985 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume-weighted average price in the last 60 minutes before market close. |
| 95 | `std_last_trade_price_interval` | MATRIX | 0.983 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the intraday last trade price across intervals during the session |
| 96 | `max_bid_price_60m_pre_close` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum bid price within the last 60 minutes before the exchange close |
| 97 | `mean_bid_price_60m_pre_close` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean bid price over the last 60 minutes before the exchange close |
| 98 | `mean_bid_price_return_60m_pre_close_2` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the bid price in the last 60 minutes before market close. |
| 99 | `min_bid_price_60m_pre_close` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum bid price within the last 60 minutes before the exchange close |
| 100 | `bid_price_60m_pre_close_2` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Bid price at the 60-minute mark before market close. |
| 101 | `max_ask_price_60m_pre_close` | MATRIX | 0.981 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ask price observed during the last 60 minutes before the exchange close |
| 102 | `mean_ask_price_60m_pre_close_2` | MATRIX | 0.981 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ask price over the 60 minutes before close |
| 103 | `mean_ask_price_return_60m_pre_close_2` | MATRIX | 0.981 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the ask price in the last 60 minutes before market close. |
| 104 | `min_ask_price_60m_pre_close_2` | MATRIX | 0.981 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ask price within the last 60 minutes before the exchange close |
| 105 | `ask_price_60m_pre_close_2` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | Ask price at the 60-minute mark before market close. |
| 106 | `max_bid_price_30m_pre_close_2` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum bid price in the last 30 minutes before market close. |
| 107 | `mean_bid_price_30m_pre_close_2` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | Average bid price in the last 30 minutes before market close. |
| 108 | `min_bid_price_30m_pre_close_2` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum bid price during the 30 minutes before close |
| 109 | `bid_price_30m_pre_close_2` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | Bid price at the 30-minute mark before market close. |
| 110 | `mean_bid_ask_size_ratio_60m_pre_close_2` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to ask size in the last 60 minutes before market close. |
| 111 | `max_slippage_interval_2` | MATRIX | 0.978 | 其他 | 0 | — | — | — | UNTESTED | Maximum slippage value observed across intervals. |
| 112 | `max_trade_volume_interval` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum intraday interval volume observed during the trading session |
| 113 | `min_slippage_interval_2` | MATRIX | 0.978 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Minimum intraday slippage observed during the session |
| 114 | `min_trade_volume_interval` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum intraday interval volume observed during the trading session |
| 115 | `momentum2_slippage_daily` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of slippage for the day. |
| 116 | `momentum2_trade_volume_daily` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of trade volume for the day. |
| 117 | `skew_slippage_interval` | MATRIX | 0.978 | 其他 | 0 | — | — | — | UNTESTED | Skewness of slippage values across intervals. |
| 118 | `skew_trade_volume_interval` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of intraday traded volume across intervals during the session |
| 119 | `std_trade_volume_interval` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of intraday volume across intervals during the session |
| 120 | `kurtosis_slippage_interval` | MATRIX | 0.978 | 其他 | 0 | — | — | — | UNTESTED | Kurtosis of slippage values across intervals. |
| 121 | `kurtosis_trade_volume_interval` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Kurtosis of the intraday volume series across intervals over the prior trading day’s session |
| 122 | `max_ask_price_30m_pre_close` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ask price within the last 30 minutes before the exchange close |
| 123 | `mean_ask_price_30m_pre_close` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ask price over the last 30 minutes before the exchange close |
| 124 | `min_ask_price_30m_pre_close_2` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ask price within the last 30 minutes before the exchange close |
| 125 | `std_slippage_interval` | MATRIX | 0.978 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Standard deviation of the intraday slippage series over the trading session (from interval data) |
| 126 | `ask_price_30m_pre_close_2` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Ask price at the 30-minute mark before market close. |
| 127 | `bid_price_60m_post_open` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | Bid price recorded 60 minutes after market open. |
| 128 | `mean_bid_ask_size_ratio_30m_pre_close_2` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to ask size in the last 30 minutes before market close. |
| 129 | `bid_price_30m_post_open` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | Bid price recorded 30 minutes after market open. |
| 130 | `ask_price_60m_post_open` | MATRIX | 0.976 | 价量与波动 | 0 | — | — | — | UNTESTED | Ask price recorded 60 minutes after market open. |
| 131 | `ask_price_30m_post_open` | MATRIX | 0.976 | 价量与波动 | 0 | — | — | — | UNTESTED | Ask price recorded 30 minutes after market open. |
| 132 | `mean_bid_vwap_ratio_60m_pre_close_2` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to VWAP in the last 60 minutes before market close. |
| 133 | `max_slippage_60m_post_open` | MATRIX | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Maximum slippage observed in the first 60 minutes after market open. |
| 134 | `max_trade_volume_60m_post_open` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum interval trading volume observed in the first 60 minutes after market open |
| 135 | `mean_ask_vwap_ratio_60m_pre_close_2` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of ask price to VWAP over the last 60 minutes before the exchange close |
| 136 | `mean_slippage_60m_post_open` | MATRIX | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Average slippage over the first 60 minutes after market open. |
| 137 | `mean_trade_volume_60m_post_open` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | Average trade volume over the first 60 minutes after market open. |
| 138 | `min_slippage_60m_post_open` | MATRIX | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Minimum slippage observed in the first 60 minutes after market open. |
| 139 | `min_trade_volume_60m_post_open` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum trade volume observed in the first 60 minutes after market open. |
| 140 | `max_slippage_30m_post_open` | MATRIX | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Maximum slippage observed in the first 30 minutes after market open. |
| 141 | `max_trade_volume_30m_post_open` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum trade volume observed in the first 30 minutes after market open. |
| 142 | `mean_slippage_30m_post_open` | MATRIX | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Average slippage over the first 30 minutes after market open. |
| 143 | `mean_trade_volume_30m_post_open` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | Average trade volume over the first 30 minutes after market open. |
| 144 | `min_slippage_30m_post_open` | MATRIX | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Minimum slippage observed in the first 30 minutes after market open. |
| 145 | `min_trade_volume_30m_post_open` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum trade volume observed in the first 30 minutes after market open. |
| 146 | `slippage_first_interval` | MATRIX | 0.974 | 交易与微观结构 | 0 | — | — | — | UNTESTED | First intraday slippage value observed at session start |
| 147 | `trade_volume_first_interval` | MATRIX | 0.974 | 价量与波动 | 0 | — | — | — | UNTESTED | Traded volume in the first intraday interval after market open |
| 148 | `corr_last_trade_price_with_slippage` | MATRIX | 0.973 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between last trade price per interval and interval |
| 149 | `momentum_slippage_daily` | MATRIX | 0.973 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of slippage for the day. |
| 150 | `mean_bid_vwap_ratio_30m_pre_close_2` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of bid price to VWAP over the last 30 minutes before the exchange close |
| 151 | `mean_ask_vwap_ratio_30m_pre_close_2` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of ask price to VWAP in the last 30 minutes before market close. |
| 152 | `max_bid_price_interval_2` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum intraday bid quote during the trading session |
| 153 | `max_bid_size_to_volume_ratio` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of bid size to traded volume observed in intervals. |
| 154 | `mean_bid_price_interval` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of the intraday bid price across intervals during the prior trading day (D1) |
| 155 | `min_bid_price_interval_2` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the best bid price across intraday intervals during the session |
| 156 | `min_bid_size_to_volume_ratio` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of bid size to traded volume in intervals. |
| 157 | `momentum2_bid_price_daily` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of bid price for the day. |
| 158 | `mean_return_bid_price_interval` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean return based on bid prices across intervals. |
| 159 | `momentum3_slippage_daily` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Third-order momentum of slippage for the day. |
| 160 | `skew_bid_price_interval` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the intraday bid price series across the session |
| 161 | `kurtosis_bid_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Kurtosis of the intraday bid price series across the session |
| 162 | `std_bid_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the intraday bid price series |
| 163 | `kurtosis_high_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Kurtosis of the intraday high price series over the session |
| 164 | `kurtosis_low_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Kurtosis of the intraday low price series across the session |
| 165 | `max_high_interval_last_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of high price to last price across intervals for the day. |
| 166 | `max_high_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum of the intraday high series across the session, the session’s highest high |
| 167 | `max_low_interval_last_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of low price to last price across intervals for the day. |
| 168 | `max_low_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum of the intraday low price across all intervals during the trading session (the highest interval low), computed f |
| 169 | `mean_high_interval_last_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of high price to last price across intervals for the day. |
| 170 | `mean_high_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of the intraday high series across intervals during the session |
| 171 | `mean_low_interval_last_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of low price to last price across intervals for the day. |
| 172 | `mean_low_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Time-averaged intraday low price over the session |
| 173 | `mean_return_high_price` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean return based on high prices across intervals. |
| 174 | `mean_return_low_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean return based on low prices across intervals. |
| 175 | `min_high_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the intraday high series across the session (lowest of highs) |
| 176 | `min_high_to_last_price_ratio` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of interval high price to last trade price. |
| 177 | `min_low_interval_last_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of low price to last price across intervals for the day. |
| 178 | `min_low_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the intraday low series across the session (session low) |
| 179 | `momentum2_high_price_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of high price for the day. |
| 180 | `momentum2_low_price_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of low price for the day. |
| 181 | `skew_high_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the intraday interval high series over the session |
| 182 | `skew_low_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the intraday low price series across the trading session |
| 183 | `momentum3_last_trade_price_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Third-order momentum of last trade price for the day. |
| 184 | `momentum_last_trade_price_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of last trade price for the day. |
| 185 | `std_high_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the intraday high price across intervals during the session (daily aggregated, D1) |
| 186 | `std_low_price_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the intraday low series over the session |
| 187 | `avg_volume_to_last_trade_ratio` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of traded volume to last trade size over intervals. |
| 188 | `avg_vwap_to_last_price_ratio` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of volume-weighted average price to last trade price over intervals. |
| 189 | `max_twap_vwap_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of time-weighted average price to VWAP for the day. |
| 190 | `max_volume_interval_last_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of trading volume to last price across intervals for the day. |
| 191 | `max_vwap_interval_2` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum value of intraday VWAP across intervals during the session |
| 192 | `max_vwap_interval_last_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of VWAP to last price across intervals for the day. |
| 193 | `mean_twap_vwap_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of time-weighted average price to VWAP for the day. |
| 194 | `mean_vwap_interval_2` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of intraday VWAP values across intervals during the session |
| 195 | `min_twap_vwap_ratio_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of time-weighted average price to VWAP for the day. |
| 196 | `min_volume_to_last_trade_ratio` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of traded volume to last trade size in intervals. |
| 197 | `min_vwap_interval_2` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum value of intraday VWAP across the session |
| 198 | `min_vwap_to_last_price_ratio` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of volume-weighted average price to last trade price in intervals. |
| 199 | `momentum2_vwap_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of VWAP for the day. |
| 200 | `momentum3_trade_volume_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Third-order momentum of trade volume for the day. |
| 201 | `momentum_trade_volume_daily` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of trade volume for the day. |
| 202 | `kurtosis_vwap_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Kurtosis of the intraday VWAP series across the trading session |
| 203 | `mean_return_vwap_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean return based on volume-weighted average prices across intervals. |
| 204 | `skew_twap_to_vwap_ratio` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio between time-weighted and volume-weighted average prices. |
| 205 | `skew_vwap_interval` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the intraday VWAP series over the session |
| 206 | `skew_vwap_to_last_price_ratio` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio between volume-weighted average price and last trade price. |
| 207 | `std_vwap_interval_2` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the intraday VWAP series across all intervals during the trading session, computed from the prior |
| 208 | `max_bid_price_60m_post_open` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum bid price observed during the first 60 minutes after market open |
| 209 | `mean_bid_price_60m_post_open` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | arithmetic mean of the best bid price over the first 60 minutes since market open |
| 210 | `min_bid_price_60m_post_open` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum bid price observed during the first 60 minutes after the exchange open |
| 211 | `mean_bid_price_return_60m_post_open` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of bid price over the first 60 minutes after market open. |
| 212 | `max_bid_price_30m_post_open` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum bid price during the first 30 minutes after the exchange open |
| 213 | `mean_bid_price_30m_post_open` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | arithmetic mean of the best bid price over the first 30 minutes since market open |
| 214 | `min_bid_price_30m_post_open` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | minimum best bid price observed in the first 30 minutes since market open |
| 215 | `corr_last_trade_price_with_volume` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between last trade price per interval and interval |
| 216 | `max_ask_price_interval` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum of the intraday ask price across all intervals during the trading session, computed from the prior day’s intrada |
| 217 | `max_ask_size_to_volume_ratio` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of ask size to traded volume observed in intervals. |
| 218 | `mean_ask_price_interval` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of the intraday ask quote across the trading session |
| 219 | `mean_bid_price_return_30m_post_open` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of bid price in the first 30 minutes after market open. |
| 220 | `min_ask_price_interval` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ask price observed across intraday intervals during the trading session |
| 221 | `min_ask_size_volume_ratio_daily` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of ask size to trading volume for the day. |
| 222 | `momentum2_ask_price_daily` | MATRIX | 0.970 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of ask price for the day. |
| 223 | `kurtosis_ask_price_interval` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Kurtosis of the best ask price series across intraday intervals during the session |
| 224 | `mean_return_ask_price_interval` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean intraday return of the ask price series computed across intervals during the session |
| 225 | `skew_ask_price_interval` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the intraday ask price series across intervals during the session |
| 226 | `bid_price_first_interval` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | First intraday value of the bid quote after market open |
| 227 | `momentum_bid_price_daily` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of bid price for the day. |
| 228 | `std_ask_price_interval` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the ask price across intraday intervals during the trading session |
| 229 | `mean_bid_price_return_30m_pre_close_2` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the bid price in the last 30 minutes before market close. |
| 230 | `momentum3_bid_price_daily` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Third-order momentum of bid price for the day. |
| 231 | `avg_bid_to_ask_price_ratio` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to ask price across intervals. |
| 232 | `max_bid_ask_price_ratio_daily` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Intraday maximum across intervals of the ratio of bid to ask price |
| 233 | `max_bid_ask_size_ratio_daily` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of bid size to ask size for the day. |
| 234 | `max_bid_ask_size_volume_ratio_daily` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of combined bid and ask size to trading volume for the day. |
| 235 | `mean_bid_ask_size_ratio_daily` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to ask size for the day. |
| 236 | `min_bid_ask_price_ratio_daily` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Intraday minimum across intervals of the ratio of bid to ask price |
| 237 | `min_bid_ask_size_to_volume_ratio` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of combined bid and ask sizes to traded volume. |
| 238 | `min_bid_size_to_ask_size_ratio` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum across intraday intervals of top-of-book bid size divided by top-of-book ask size |
| 239 | `max_ask_price_60m_post_open` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ask price observed during the first 60 minutes after the market open |
| 240 | `mean_ask_price_60m_post_open` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | arithmetic mean of the best ask price over the first 60 minutes since market open |
| 241 | `min_ask_price_60m_post_open` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ask price during the first 60 minutes after the market open |
| 242 | `skew_bid_size_to_ask_size_ratio` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio between bid size and ask size across intervals. |
| 243 | `skew_bid_to_ask_price_ratio` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio between bid and ask prices across intervals. |
| 244 | `mean_ask_price_return_60m_post_open` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of ask price over the first 60 minutes after market open. |
| 245 | `max_ask_price_30m_post_open` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | max best ask price observed within the first 30 minutes since market open |
| 246 | `mean_ask_price_30m_post_open` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | arithmetic mean of the best ask price over the first 30 minutes since market open |
| 247 | `mean_ask_price_return_30m_post_open` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of ask price in the first 30 minutes after market open. |
| 248 | `min_ask_price_30m_post_open` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ask price during the first 30 minutes after the market open |
| 249 | `ask_price_first_interval` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | First intraday value of the ask quote after market open |
| 250 | `mean_bid_ask_size_ratio_60m_post_open` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to ask size in the first 60 minutes after market open. |
| 251 | `momentum_ask_price_daily` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of ask price for the day. |
| 252 | `corr_bid_price_with_slippage` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation computed over intraday intervals during the trading session between interval bid price and inte |
| 253 | `mean_bid_ask_size_ratio_30m_post_open` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to ask size in the first 30 minutes after market open. |
| 254 | `momentum3_ask_price_daily` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Third-order momentum of ask price for the day. |
| 255 | `corr_ask_price_with_slippage` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation computed over intraday intervals during the trading session between interval ask price and inte |
| 256 | `corr_interval_bid_with_interval_ask` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily Pearson correlation across intraday intervals between the interval bid quote and the interval ask quote for the st |
| 257 | `corr_last_trade_price_with_interval_bid` | MATRIX | 0.967 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last trade price and interval bid price. |
| 258 | `mean_ask_price_return_30m_pre_close_2` | MATRIX | 0.967 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of the ask price in the last 30 minutes before market close. |
| 259 | `corr_last_trade_price_with_interval_ask` | MATRIX | 0.967 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last trade price and interval ask price. |
| 260 | `bid_price_last_interval` | MATRIX | 0.967 | 价量与波动 | 0 | — | — | — | UNTESTED | Last intraday value of the bid quote during the trading session |
| 261 | `high_price_60m_post_open` | MATRIX | 0.967 | 价量与波动 | 0 | — | — | — | UNTESTED | High price recorded 60 minutes after market open. |
| 262 | `low_price_60m_post_open` | MATRIX | 0.967 | 价量与波动 | 0 | — | — | — | UNTESTED | Low price recorded 60 minutes after market open. |
| 263 | `vwap_60m_post_open` | MATRIX | 0.966 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume-weighted average price recorded 60 minutes after market open. |
| 264 | `corr_twap_with_slippage` | MATRIX | 0.966 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval TWAP and interval slippage, aggreg |
| 265 | `corr_last_vwap_with_slippage` | MATRIX | 0.965 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation computed over intraday intervals during the trading session between end-of-interval VWAP and in |
| 266 | `ask_price_last_interval` | MATRIX | 0.965 | 价量与波动 | 0 | — | — | — | UNTESTED | Last intraday observation of the ask price at the end of the trading session |
| 267 | `corr_vwap_with_slippage` | MATRIX | 0.965 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval VWAP and interval slippage, aggreg |
| 268 | `corr_last_trade_price_with_interval_twap` | MATRIX | 0.965 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last trade price and interval time-weighted average price. |
| 269 | `corr_twap_with_volume` | MATRIX | 0.965 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval TWAP and interval traded volume, a |
| 270 | `skew_high_to_last_price_ratio` | MATRIX | 0.965 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio between interval high price and last trade price. |
| 271 | `skew_low_to_last_price_ratio` | MATRIX | 0.965 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio between interval low price and last trade price. |
| 272 | `max_bid_vwap_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Intraday maximum across intervals of the ratio of bid price to VWAP |
| 273 | `mean_bid_vwap_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Intraday mean across intervals of the ratio of bid price to VWAP |
| 274 | `min_bid_vwap_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Intraday minimum across intervals of the ratio of bid price to VWAP |
| 275 | `mean_bid_size_volume_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to trading volume for the day. |
| 276 | `corr_last_vwap_with_interval_twap_2` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last volume-weighted average price and the interval time-weighted average price. |
| 277 | `corr_last_vwap_with_last_price_2` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last volume-weighted average price and the last trade price. |
| 278 | `corr_last_vwap_with_volume` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation computed over intraday intervals during the trading session between end-of-interval VWAP and in |
| 279 | `max_ask_price_to_vwap_ratio` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum ratio of ask price to volume-weighted average price in intervals. |
| 280 | `mean_ask_size_volume_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of ask size to trading volume for the day. |
| 281 | `mean_ask_vwap_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of ask price to VWAP for the day. |
| 282 | `min_ask_price_to_vwap_ratio` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum ratio of ask price to volume-weighted average price in intervals. |
| 283 | `skew_bid_vwap_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio of bid price to VWAP for the day. |
| 284 | `corr_last_vwap_with_interval_vwap` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation coefficient across intraday intervals between the last-sampled VWAP (last_vwap) and the interval VWA |
| 285 | `corr_vwap_with_volume` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval VWAP and interval traded volume, a |
| 286 | `corr_last_trade_price_with_interval_vwap` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation coefficient across intraday intervals between the last trade price and the interval VWAP for the tra |
| 287 | `skew_ask_vwap_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio of ask price to VWAP for the day. |
| 288 | `avg_bid_ask_size_to_volume_ratio` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of combined bid and ask sizes to traded volume over intervals. |
| 289 | `skew_volume_interval_last_ratio_daily` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio of trading volume to last price across intervals for the day. |
| 290 | `high_price_30m_post_open` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | High price recorded 30 minutes after market open. |
| 291 | `low_price_30m_post_open` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Low price recorded 30 minutes after market open. |
| 292 | `corr_interval_twap_with_interval_high` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation coefficient across intraday intervals between the interval TWAP and the interval high price for the |
| 293 | `corr_interval_twap_with_interval_low` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval time-weighted average price and interval low price. |
| 294 | `corr_last_price_with_interval_high` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last trade price and the interval high price. |
| 295 | `corr_last_trade_price_with_interval_low` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last trade price and interval low price. |
| 296 | `corr_high_price_with_slippage` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval high price and interval slippage, |
| 297 | `corr_interval_low_with_interval_high` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals between each interval’s low and high prices for the trading day (D1) |
| 298 | `corr_low_price_with_slippage` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation computed over intraday intervals during the trading session between interval low price and inte |
| 299 | `corr_ask_price_with_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval best ask price and interval traded |
| 300 | `corr_bid_price_with_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval best bid price and interval traded |
| 301 | `corr_high_price_with_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval high price and interval traded vol |
| 302 | `corr_low_price_with_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval low price and interval traded volu |
| 303 | `corr_interval_vwap_with_interval_high` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval VWAP and interval high price. |
| 304 | `corr_interval_vwap_with_interval_low_2` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals between interval VWAP and interval low price for the day (D1) |
| 305 | `corr_last_vwap_with_interval_high_2` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last volume-weighted average price and the interval high price. |
| 306 | `corr_last_vwap_with_interval_low` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last VWAP and interval low price. |
| 307 | `momentum3_vwap_daily` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Third-order momentum of VWAP for the day. |
| 308 | `momentum_vwap_daily` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of VWAP for the day. |
| 309 | `avg_price_modulo_10_ratio_first_half` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of price modulo 10 during the first half of volume clock. |
| 310 | `corr_last_low_with_interval_twap_2` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last low price and the interval time-weighted average price. |
| 311 | `corr_last_trade_price_with_last_low` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last trade price and last low price. |
| 312 | `mean_high_price_first_half_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Average high price during the first half of volume clock. |
| 313 | `mean_last_trade_price_first_half` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Average last-trade price over the first 50% of cumulative intraday volume (D1 lag) |
| 314 | `mean_low_price_first_half_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Average low price during the first half of volume clock. |
| 315 | `mean_volume_first_half` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Average interval volume within the first 50% of cumulative intraday volume (D1 lag) |
| 316 | `mean_vwap_first_half_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Average VWAP within the first 50% of cumulative intraday volume |
| 317 | `num_intervals_first_half_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of intraday intervals included in the first 50% cumulative volume slice |
| 318 | `vwap_30m_post_open` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume-weighted average price recorded 30 minutes after market open. |
| 319 | `corr_last_high_with_interval_twap` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last high price and interval time-weighted average price. |
| 320 | `momentum1_volume_first_half` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | First order momentum of traded volume in the first half of volume clock. |
| 321 | `momentum2_high_price_first_half_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Second order momentum of high price in the first half of volume clock. |
| 322 | `momentum2_last_trade_price_first_half` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Second order momentum of last trade price in the first half of volume clock. |
| 323 | `momentum2_low_price_first_half_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Second order momentum of low price in the first half of volume clock. |
| 324 | `momentum2_volume_first_half` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Second order momentum of traded volume in the first half of volume clock. |
| 325 | `momentum2_vwap_first_half_volume` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Second order momentum of VWAP in the first half of volume clock. |
| 326 | `std_volume_first_half` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of traded volume in the first half of volume clock. |
| 327 | `corr_last_trade_price_with_last_high` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last trade price and last high price. |
| 328 | `std_last_trade_price_first_half` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the last trade price across intervals within the first 50% of cumulative intraday volume (prior da |
| 329 | `std_vwap_first_half_volume` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of VWAP during the first half of volume clock. |
| 330 | `corr_last_vwap_with_last_low_2` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last volume-weighted average price and the last low price. |
| 331 | `mean_high_price_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean high price in the first quarter of volume clock. |
| 332 | `mean_last_trade_price_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean last trade price in the first quarter of volume clock. |
| 333 | `mean_low_price_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean low price in the first quarter of volume clock. |
| 334 | `mean_price_modulo_10_ratio_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of price modulo 10 in the first quarter of volume clock. |
| 335 | `mean_trade_volume_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean traded volume per interval within the first 25% volume slice |
| 336 | `mean_vwap_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of interval VWAP values across the first 25% cumulative volume slice |
| 337 | `num_intervals_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of time intervals contained in the first 25% volume slice |
| 338 | `corr_last_low_with_interval_vwap_2` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last low price and the interval volume-weighted average price. |
| 339 | `std_high_price_first_half_volume` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the intraday high price across intervals within the first 50% volume slice (prior day) |
| 340 | `std_low_price_first_half_volume` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the intraday low price across intervals within the first 50% volume slice (prior day) |
| 341 | `corr_last_vwap_with_last_high_2` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last volume-weighted average price and the last high price. |
| 342 | `corr_last_high_with_interval_vwap` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last high price and interval VWAP. |
| 343 | `momentum2_high_price_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of high price in the first quarter of volume clock. |
| 344 | `momentum2_last_trade_price_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of last trade price in the first quarter of volume clock. |
| 345 | `momentum2_low_price_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of low price in the first quarter of volume clock. |
| 346 | `std_trade_volume_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of traded volume per interval within the first 25% volume slice |
| 347 | `momentum2_trade_volume_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of trade volume in the first quarter of volume clock. |
| 348 | `momentum2_vwap_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of VWAP in the first quarter of volume clock. |
| 349 | `momentum_trade_volume_first_quarter_volumeclock` | MATRIX | 0.962 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of trade volume in the first quarter of volume clock. |
| 350 | `std_last_trade_price_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the last trade price across intervals within the first 25% of the day's cumulative traded volume |
| 351 | `std_vwap_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of interval VWAP values across the first 25% cumulative volume slice |
| 352 | `avg_bid_price_to_vwap_ratio_first_half` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to VWAP in the first half of volume clock. |
| 353 | `avg_bid_size_to_volume_ratio_first_half` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to traded volume in the first half of volume clock. |
| 354 | `mean_bid_price_first_half_volume` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Average bid price over the first 50% of cumulative intraday volume (D1 lag) |
| 355 | `avg_ask_price_to_vwap_ratio_first_half` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of ask price to VWAP in the first half of volume clock. |
| 356 | `avg_ask_size_to_volume_ratio_first_half` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of ask size to traded volume in the first half of volume clock. |
| 357 | `avg_bid_to_ask_price_ratio_first_half` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to ask price in the first half of volume clock. |
| 358 | `mean_ask_price_first_half_volume` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ask price across intervals within the first 50% of cumulative intraday volume (prior day) |
| 359 | `std_high_price_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of high price in the first quarter of volume clock. |
| 360 | `std_low_price_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the low price across intervals within the first 25% cumulative volume slice |
| 361 | `momentum2_ask_price_first_half_volume` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Second order momentum of ask price in the first half of volume clock. |
| 362 | `momentum2_bid_price_first_half_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of bid price during the first half of volume clock. |
| 363 | `std_ask_price_first_half_volume` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of ask price during the first half of volume clock. |
| 364 | `std_bid_price_first_half_volume` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of bid price during the first half of volume clock. |
| 365 | `corr_last_low_with_interval_low` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last low price and interval low price. |
| 366 | `momentum3_low_price_daily` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Third-order momentum of low price for the day. |
| 367 | `corr_last_low_with_interval_high` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last low price and interval high price. |
| 368 | `mean_ask_price_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ask price across intervals within the first 25% of the day's cumulative traded volume |
| 369 | `mean_ask_size_to_volume_ratio_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of ask size to volume in the first quarter of volume clock. |
| 370 | `mean_ask_to_vwap_ratio_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of ask price to VWAP in the first quarter of volume clock. |
| 371 | `mean_bid_price_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Average of the bid price across intervals within the first 25% cumulative volume slice |
| 372 | `mean_bid_size_to_volume_ratio_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of bid size to volume in the first quarter of volume clock. |
| 373 | `mean_bid_to_vwap_ratio_first_quarter_volumeclock` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to VWAP across intervals within the first 25% cumulative volume slice |
| 374 | `mean_bid_to_ask_price_ratio_first_quarter_volumeclock` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of bid price to ask price in the first quarter of volume clock. |
| 375 | `corr_last_high_with_interval_high_2` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last high price and the interval high price. |
| 376 | `momentum3_high_price_daily` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Third-order momentum of high price for the day. |
| 377 | `momentum_high_price_daily` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of high price for the day. |
| 378 | `corr_last_high_with_interval_low` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last high price and interval low price. |
| 379 | `momentum2_bid_price_first_quarter_volumeclock` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of bid price in the first quarter of volume clock. |
| 380 | `momentum2_ask_price_first_quarter_volumeclock` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of ask price in the first quarter of volume clock. |
| 381 | `std_ask_price_first_quarter_volumeclock` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the ask price across intervals within the first 25% cumulative volume slice |
| 382 | `std_bid_price_first_quarter_volumeclock` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of bid price in the first quarter of volume clock. |
| 383 | `vwap_last_half` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume-weighted average price in the last 50% of the session. |
| 384 | `max_high_price_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | max of the per-interval high prices within the first 60 minutes since open (highest high) |
| 385 | `max_low_price_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum low price observed in the first 60 minutes after market open. |
| 386 | `mean_high_price_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Average high price over the first 60 minutes after market open. |
| 387 | `mean_low_price_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Average low price over the first 60 minutes after market open. |
| 388 | `min_high_price_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the high price series during the first 60 minutes after the exchange open |
| 389 | `min_low_price_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the low price series (i.e., the lowest low) during the first 60 minutes after the market open |
| 390 | `momentum_bid_to_vwap_ratio_first_half_volumeclock` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of the ratio between bid price and VWAP in the first half of volume clock. |
| 391 | `momentum_ask_price_to_vwap_ratio_first_half` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of ask price to VWAP ratio in the first half of volume clock. |
| 392 | `mean_high_price_return_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of high price in the first 60 minutes after market open. |
| 393 | `mean_low_price_return_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of low price in the first 60 minutes after market open. |
| 394 | `max_vwap_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum volume-weighted average price in the first 60 minutes after market open. |
| 395 | `mean_vwap_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Average VWAP over the first 60 minutes after the exchange opens, computed from intraday intervals |
| 396 | `min_vwap_60m_post_open` | MATRIX | 0.959 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum volume-weighted average price in the first 60 minutes after market open. |
| 397 | `mean_vwap_return_60m_post_open` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of volume-weighted average price in the first 60 minutes after market open. |
| 398 | `corr_interval_twap_with_interval_ask` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval time-weighted average price and interval ask price. |
| 399 | `momentum_ask_to_vwap_ratio_first_quarter_volumeclock` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of the ratio between ask price and VWAP in the first quarter of volume clock. |
| 400 | `momentum_bid_to_vwap_ratio_first_quarter_volumeclock_2` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of the ratio between bid price and VWAP in the first quarter of volume clock (alternate). |
| 401 | `skew_bid_size_volume_ratio_daily` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio of bid size to trading volume for the day. |
| 402 | `corr_interval_twap_with_interval_bid_2` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval time-weighted average price and interval bid price. |
| 403 | `skew_ask_size_volume_ratio_daily` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio of ask size to trading volume for the day. |
| 404 | `skew_bid_ask_size_to_volume_ratio` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of the ratio of combined bid and ask sizes to traded volume. |
| 405 | `corr_interval_vwap_with_interval_ask` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval VWAP and interval ask price. |
| 406 | `corr_last_vwap_with_interval_ask` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last VWAP and interval ask price. |
| 407 | `corr_interval_vwap_with_interval_bid_2` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals between interval VWAP and interval bid quote price for the day (D1) |
| 408 | `corr_last_low_with_last_high` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last low price and last high price. |
| 409 | `corr_last_vwap_with_interval_bid` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last VWAP and interval bid price. |
| 410 | `corr_volume_with_bid_price_first_half` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between traded volume and bid price in the first half of volume clock. |
| 411 | `corr_volume_with_ask_price_first_half` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between traded volume and ask price in the first half of volume clock. |
| 412 | `momentum_bid_to_ask_price_ratio_first_half` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of bid price to ask price ratio in the first half of volume clock. |
| 413 | `corr_bid_with_ask_price_first_half` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation between bid price and ask price within the first 50% cumulative-volume slice |
| 414 | `momentum1_bid_price_first_half_volume` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | First order momentum of bid price in the first half of volume clock. |
| 415 | `momentum1_ask_price_first_half_volume` | MATRIX | 0.957 | 价量与波动 | 0 | — | — | — | UNTESTED | First order momentum of ask price in the first half of volume clock. |
| 416 | `corr_last_low_with_interval_ask` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last low price and interval ask price. |
| 417 | `corr_last_low_with_interval_bid` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last low price and interval bid price. |
| 418 | `corr_last_high_with_interval_ask_2` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between the last high price and the interval ask price. |
| 419 | `corr_volume_with_ask_price_first_quarter_volumeclock` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between volume and ask price in the first quarter of volume clock. |
| 420 | `corr_volume_with_bid_price_first_quarter_volumeclock` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between volume and bid price in the first quarter of volume clock. |
| 421 | `max_high_price_30m_post_open` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum of the high price series (highest high) in the first 30 minutes after the exchange opens |
| 422 | `max_low_price_30m_post_open` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum of the low price series during the first 30 minutes after the exchange open |
| 423 | `mean_high_price_30m_post_open` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Average high price over the first 30 minutes after market open. |
| 424 | `mean_low_price_30m_post_open` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Average low price over the first 30 minutes after market open. |
| 425 | `min_high_price_30m_post_open` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the high price series during the first 30 minutes after the exchange open |
| 426 | `min_low_price_30m_post_open` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum of the low price series (lowest low) in the first 30 minutes after the exchange opens |
| 427 | `momentum_bid_to_ask_price_ratio_first_quarter_volumeclock` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of the ratio between bid and ask price in the first quarter of volume clock. |
| 428 | `corr_last_high_with_interval_bid` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between last high price and interval bid price. |
| 429 | `corr_bid_with_ask_price_first_quarter_volumeclock` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between bid price and ask price in the first quarter of volume clock. |
| 430 | `momentum_ask_price_first_quarter_volumeclock` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of ask price in the first quarter of volume clock. |
| 431 | `momentum_bid_price_first_quarter_volumeclock` | MATRIX | 0.956 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of bid price in the first quarter of volume clock. |
| 432 | `max_vwap_30m_post_open` | MATRIX | 0.955 | 价量与波动 | 0 | — | — | — | UNTESTED | Maximum volume-weighted average price in the first 30 minutes after market open. |
| 433 | `mean_vwap_30m_post_open` | MATRIX | 0.955 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean VWAP over the first 30 minutes after the exchange open |
| 434 | `min_vwap_30m_post_open` | MATRIX | 0.955 | 价量与波动 | 0 | — | — | — | UNTESTED | Minimum VWAP observed during the first 30 minutes after the exchange open |
| 435 | `corr_volume_with_last_trade_price_first_half` | MATRIX | 0.955 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation between intraday volume and last trade price within the first 50% cumulative-volume slice |
| 436 | `mean_high_price_return_30m_post_open` | MATRIX | 0.955 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of high price in the first 30 minutes after market open. |
| 437 | `mean_low_price_return_30m_post_open` | MATRIX | 0.955 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of low price in the first 30 minutes after market open. |
| 438 | `mean_vwap_return_30m_post_open` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | Average return of volume-weighted average price in the first 30 minutes after market open. |
| 439 | `momentum1_last_trade_price_first_half` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | First order momentum of last trade price in the first half of volume clock. |
| 440 | `corr_interval_high_with_interval_bid` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval high price and interval bid price. |
| 441 | `corr_interval_high_with_interval_ask` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval high price and interval ask price. |
| 442 | `corr_interval_low_with_interval_ask` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval low price and interval ask price. |
| 443 | `corr_interval_low_with_interval_bid` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval low price and interval bid price. |
| 444 | `mean_ask_vwap_ratio_60m_post_open` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of ask price to VWAP in the first 60 minutes after market open. |
| 445 | `mean_bid_vwap_ratio_60m_post_open` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to VWAP in the first 60 minutes after market open. |
| 446 | `momentum1_vwap_first_half_volume` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | First order momentum of VWAP in the first half of volume clock. |
| 447 | `corr_volume_with_last_trade_price_first_quarter_volumeclock` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between volume and last trade price in the first quarter of volume clock. |
| 448 | `momentum_ask_size_to_volume_ratio_first_half` | MATRIX | 0.953 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of ask size to traded volume ratio in the first half of volume clock. |
| 449 | `momentum_bid_size_to_volume_ratio_first_half` | MATRIX | 0.953 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of bid size to volume ratio in the first half of volume clock. |
| 450 | `momentum_last_trade_price_first_quarter_volumeclock` | MATRIX | 0.953 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of last trade price in the first quarter of volume clock. |
| 451 | `momentum_price_modulo_10_ratio_first_half` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of price modulo 10 ratio in the first half of volume clock. |
| 452 | `momentum_vwap_first_quarter_volumeclock` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of VWAP in the first quarter of volume clock. |
| 453 | `corr_volume_with_low_price_first_half` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between traded volume and low price in the first half of volume clock. |
| 454 | `momentum_bid_size_to_volume_ratio_first_quarter_volumeclock` | MATRIX | 0.952 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of the ratio between bid size and volume in the first quarter of volume clock. |
| 455 | `corr_volume_with_high_price_first_half` | MATRIX | 0.951 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between traded volume and high price in the first half of volume clock. |
| 456 | `mean_bid_vwap_ratio_30m_post_open` | MATRIX | 0.951 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to VWAP in the first 30 minutes after market open. |
| 457 | `mean_ask_vwap_ratio_30m_post_open` | MATRIX | 0.951 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of the ask-to-VWAP ratio over the first 30 minutes after the market open |
| 458 | `momentum_price_modulo_10_ratio_first_quarter_volumeclock` | MATRIX | 0.951 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of price modulo 10 ratio in the first quarter of volume clock. |
| 459 | `corr_volume_with_low_price_first_quarter_volumeclock` | MATRIX | 0.949 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between volume and low price in the first quarter of volume clock. |
| 460 | `corr_volume_with_high_price_first_quarter_volumeclock` | MATRIX | 0.949 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between volume and high price in the first quarter of volume clock. |
| 461 | `avg_high_price_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of high prices in the last 50% of the trading period. |
| 462 | `avg_last_trade_price_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean last trade price computed over the last 50% of the day's cumulative volume |
| 463 | `avg_low_price_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of the low price across intraday intervals within the last 50% of the day's cumulative traded volume |
| 464 | `avg_price_modulo_10_ratio_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of price modulo 10 in the last 50% of the session. |
| 465 | `avg_trade_volume_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean traded volume in the last 50% of the session. |
| 466 | `num_intervals_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of intraday intervals included in the last 50% cumulative volume slice, D1 |
| 467 | `avg_vwap_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean volume-weighted average price (VWAP) across intraday intervals within the last 50% of the day's cumulative traded v |
| 468 | `momentum2_high_price_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of high price in the last 50% of the session. |
| 469 | `momentum2_last_trade_price_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of last trade price in the last 50% of the session. |
| 470 | `momentum2_low_price_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of low price in the last 50% of the session. |
| 471 | `momentum2_trade_volume_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of traded volume in the last 50% of the session. |
| 472 | `momentum2_vwap_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of volume-weighted average price in the last 50% of the session. |
| 473 | `momentum_trade_volume_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of traded volume in the last 50% of the session. |
| 474 | `std_trade_volume_last_half` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of traded volume in the last 50% of the session. |
| 475 | `std_last_trade_price_last_half` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the last traded price across intraday intervals within the last 50% of the day's cumulative traded |
| 476 | `std_vwap_last_half` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of volume-weighted average price in the last 50% of the session. |
| 477 | `std_high_price_last_half` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of high prices in the last 50% of the trading period. |
| 478 | `std_low_price_last_half` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of low prices in the last 50% of the trading period. |
| 479 | `high_price_first_interval` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | First intraday interval high observed at session start |
| 480 | `low_price_first_interval` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Low price in the first interval of the day. |
| 481 | `avg_bid_price_last_half` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean bid price computed over the last 50% of the day's cumulative volume |
| 482 | `avg_ask_price_last_half` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ask price across intraday intervals within the last 50% of the day's cumulative traded volume |
| 483 | `avg_ask_size_to_volume_ratio_last_half` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of ask size to traded volume in the last 50% of the session. |
| 484 | `avg_ask_to_vwap_ratio_last_half` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of ask price to VWAP across intraday intervals within the last 50% of the day's cumulative traded volume |
| 485 | `avg_bid_size_to_volume_ratio_last_half` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to traded volume in the last 50% of the session. |
| 486 | `avg_bid_to_vwap_ratio_last_half` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to VWAP in the last 50% of the session. |
| 487 | `avg_bid_to_ask_price_ratio_last_half` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to ask price in the last 50% of the session. |
| 488 | `momentum2_bid_price_last_half` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of bid price in the last 50% of the session. |
| 489 | `momentum2_ask_price_last_half` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of ask price in the last 50% of the session. |
| 490 | `std_bid_price_last_half` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the bid price across intraday intervals within the last 50% of the day's cumulative traded volume |
| 491 | `std_ask_price_last_half` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the ask price across intraday intervals within the last 50% of the day's cumulative traded volume |
| 492 | `vwap_first_interval` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | First intraday VWAP observed at session start |
| 493 | `corr_high_with_low_price_first_half` | MATRIX | 0.943 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between high and low prices in the first half of volume clock. |
| 494 | `ask_price_last_half` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | Ask price in the last 50% of the session. |
| 495 | `bid_price_last_half` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | Bid price in the last 50% of the session. |
| 496 | `momentum_ask_to_vwap_ratio_last_half` | MATRIX | 0.941 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of ask price to VWAP during the last 50% of the session. |
| 497 | `momentum_bid_to_vwap_ratio_last_half` | MATRIX | 0.941 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of bid price to VWAP during the last 50% of the session. |
| 498 | `corr_volume_with_last_price_last_half` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation between intraday interval volume and the last traded price computed over the last 50% of the day's c |
| 499 | `corr_volume_with_ask_price_last_half` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between traded volume and ask price in the last 50% of the session. |
| 500 | `corr_volume_with_bid_price_last_half` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between traded volume and bid price in the last 50% of the session. |
| 501 | `momentum_bid_to_ask_price_ratio_last_half` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of bid price to ask price during the last 50% of the session. |
| 502 | `momentum_last_trade_price_last_half` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of last trade price in the last 50% of the session. |
| 503 | `momentum_vwap_last_half` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of volume-weighted average price in the last 50% of the session. |
| 504 | `momentum_ask_price_last_half` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of ask price in the last 50% of the session. |
| 505 | `momentum_bid_price_last_half` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of bid price in the last 50% of the session. |
| 506 | `momentum_ask_size_to_volume_ratio_last_half` | MATRIX | 0.937 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of ask size to volume during the last 50% of the session. |
| 507 | `momentum_bid_size_to_volume_ratio_last_half` | MATRIX | 0.937 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of bid size to volume during the last 50% of the session. |
| 508 | `corr_high_with_low_price_first_quarter_volumeclock` | MATRIX | 0.937 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between high and low prices across intervals within the first 25% of the day's cumulative traded volume |
| 509 | `momentum_price_modulo_10_ratio_last_half` | MATRIX | 0.936 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of price modulo 10 during the last 50% of the session. |
| 510 | `corr_volume_with_high_price_last_half` | MATRIX | 0.927 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between traded volume and high price in the last 50% of the session. |
| 511 | `corr_volume_with_low_price_last_half` | MATRIX | 0.926 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between traded volume and low price in the last 50% of the session. |
| 512 | `vwap_last_quarter` | MATRIX | 0.925 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume-weighted average price in the last 25% of the session. |
| 513 | `corr_bid_price_with_bid_size` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval best bid price and interval bid si |
| 514 | `avg_high_price_last_quarter` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Average high price within the last 25% of intraday volume |
| 515 | `avg_trade_volume_last_quarter` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Average intraday volume across intervals within the last 25% of cumulative volume of the prior trading day |
| 516 | `avg_vwap_last_quarter` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Average VWAP across intraday intervals within the last 25% volume slice |
| 517 | `corr_ask_price_with_ask_size` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval best ask price and interval ask si |
| 518 | `mean_last_trade_price_last_quarter_volumeclock` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Average last trade price across intervals within the last 25% volume slice |
| 519 | `mean_low_price_last_quarter_volumeclock` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Average low price within the last 25% of intraday volume |
| 520 | `mean_price_modulo_10_ratio_last_quarter_volumeclock` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of price modulo 10 in the last quarter of volume clock. |
| 521 | `num_intervals_last_quarter_volumeclock` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of intraday intervals included in the last 25% of intraday volume |
| 522 | `corr_bid_price_with_ask_size` | MATRIX | 0.911 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval best bid price and interval ask si |
| 523 | `corr_ask_price_with_bid_size` | MATRIX | 0.911 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval best ask price and interval bid si |
| 524 | `avg_ask_price_last_quarter` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ask price within the last 25% of intraday volume |
| 525 | `avg_bid_to_vwap_ratio_last_quarter` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid price to VWAP in the last 25% of the session. |
| 526 | `mean_ask_to_vwap_ratio_last_quarter_volumeclock` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of ask price to VWAP in the last quarter of volume clock. |
| 527 | `mean_bid_price_last_quarter_volumeclock` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | Average bid price across intervals within the last 25% volume slice |
| 528 | `avg_ask_size_to_volume_ratio_last_quarter` | MATRIX | 0.909 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of ask size to traded volume in the last 25% of the session. |
| 529 | `mean_bid_to_ask_price_ratio_last_quarter_volumeclock` | MATRIX | 0.909 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean ratio of bid price to ask price in the last quarter of volume clock. |
| 530 | `avg_bid_size_to_volume_ratio_last_quarter` | MATRIX | 0.909 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ratio of bid size to traded volume in the last 25% of the session. |
| 531 | `ask_price_last_quarter` | MATRIX | 0.908 | 价量与波动 | 0 | — | — | — | UNTESTED | Ask price in the last 25% of the session. |
| 532 | `bid_price_last_quarter` | MATRIX | 0.908 | 价量与波动 | 0 | — | — | — | UNTESTED | Bid price in the last 25% of the session. |
| 533 | `corr_interval_asksize_with_interval_bidsize` | MATRIX | 0.907 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation coefficient across intraday intervals between the interval ask size and the interval bid size for th |
| 534 | `momentum2_high_price_last_quarter_volumeclock` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of high price in the last quarter of volume clock. |
| 535 | `momentum2_last_trade_price_last_quarter_volumeclock` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of last trade price in the last quarter of volume clock. |
| 536 | `momentum2_low_price_last_quarter_volumeclock` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of low price in the last quarter of volume clock. |
| 537 | `momentum2_trade_volume_last_quarter_volumeclock` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of trade volume in the last quarter of volume clock. |
| 538 | `momentum2_vwap_last_quarter_volumeclock` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of VWAP in the last quarter of volume clock. |
| 539 | `momentum_trade_volume_last_quarter_volumeclock` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of trade volume in the last quarter of volume clock. |
| 540 | `std_trade_volume_last_quarter_volumeclock` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of traded volume within the last 25% of cumulative intraday volume |
| 541 | `std_last_trade_price_last_quarter_volumeclock` | MATRIX | 0.905 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of last trade price within the last 25% of cumulative intraday volume |
| 542 | `std_vwap_last_quarter` | MATRIX | 0.905 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of volume-weighted average price in the last 25% of the session. |
| 543 | `std_low_price_last_quarter` | MATRIX | 0.905 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of low prices in the last 25% of the trading period. |
| 544 | `std_high_price_last_quarter_volumeclock` | MATRIX | 0.905 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of high price in the last quarter of volume clock. |
| 545 | `corr_last_trade_price_with_ask_size` | MATRIX | 0.904 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between last trade price per interval and interval |
| 546 | `momentum2_ask_price_last_quarter` | MATRIX | 0.904 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of ask price in the last 25% of the session. |
| 547 | `momentum2_bid_price_last_quarter` | MATRIX | 0.904 | 价量与波动 | 0 | — | — | — | UNTESTED | Second-order momentum of bid price in the last 25% of the session. |
| 548 | `std_ask_price_last_quarter` | MATRIX | 0.904 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of ask prices in the last 25% of the trading period. |
| 549 | `std_bid_price_last_quarter_volumeclock` | MATRIX | 0.904 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of bid price in the last quarter of volume clock. |
| 550 | `corr_last_trade_price_with_bid_size` | MATRIX | 0.904 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between last trade price per interval and interval |
| 551 | `corr_interval_volume_with_interval_asksize` | MATRIX | 0.903 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between interval trade volume and interval ask size. |
| 552 | `corr_interval_volume_with_interval_bid_size` | MATRIX | 0.902 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation coefficient across intraday intervals between the interval traded volume and the interval bid size f |
| 553 | `momentum_ask_to_vwap_ratio_last_quarter` | MATRIX | 0.902 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of ask price to VWAP during the last 25% of the session. |
| 554 | `momentum_bid_to_vwap_ratio_last_quarter` | MATRIX | 0.901 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of bid price to VWAP during the last 25% of the session. |
| 555 | `corr_volume_with_ask_price_last_quarter_volumeclock` | MATRIX | 0.899 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation between intraday volume and ask price within the last 25% cumulative volume slice of the prior |
| 556 | `momentum_bid_to_ask_price_ratio_last_quarter_volumeclock` | MATRIX | 0.899 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of the ratio between bid and ask price in the last quarter of volume clock. |
| 557 | `corr_volume_with_bid_price_last_quarter_volumeclock` | MATRIX | 0.899 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation between intraday volume and bid price within the last 25% cumulative volume slice of the prior |
| 558 | `momentum_ask_price_last_quarter_volumeclock` | MATRIX | 0.898 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of ask price in the last quarter of volume clock. |
| 559 | `momentum_bid_price_last_quarter_volumeclock` | MATRIX | 0.898 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of bid price in the last quarter of volume clock. |
| 560 | `corr_bid_with_ask_price_last_quarter_volumeclock` | MATRIX | 0.898 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation between bid price and ask price within the last 25% cumulative volume slice of the prior tradin |
| 561 | `momentum_vwap_last_quarter_volumeclock` | MATRIX | 0.895 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of VWAP in the last quarter of volume clock. |
| 562 | `corr_volume_with_last_price_last_quarter` | MATRIX | 0.895 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation between intraday volume and last-traded price within the last 25% cumulative volume slice of th |
| 563 | `momentum_ask_size_to_volume_ratio_last_quarter` | MATRIX | 0.894 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of ask size to volume during the last 25% of the session. |
| 564 | `momentum_bid_size_to_volume_ratio_last_quarter_volumeclock` | MATRIX | 0.894 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of the ratio between bid size and volume in the last quarter of volume clock. |
| 565 | `momentum_last_trade_price_last_quarter` | MATRIX | 0.894 | 价量与波动 | 0 | — | — | — | UNTESTED | First-order momentum of last trade price in the last 25% of the session. |
| 566 | `momentum_price_modulo_10_ratio_last_quarter_volumeclock` | MATRIX | 0.892 | 价量与波动 | 0 | — | — | — | UNTESTED | Momentum of price modulo 10 ratio in the last quarter of volume clock. |
| 567 | `corr_twap_with_ask_size` | MATRIX | 0.890 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval TWAP and interval ask size (best a |
| 568 | `corr_last_vwap_with_ask_size` | MATRIX | 0.890 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation computed over intraday intervals during the trading session between end-of-interval VWAP and in |
| 569 | `corr_vwap_with_ask_size` | MATRIX | 0.890 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval VWAP and interval ask size (best a |
| 570 | `corr_twap_with_bid_size` | MATRIX | 0.890 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval TWAP and interval bid size (best b |
| 571 | `corr_last_vwap_with_bid_size` | MATRIX | 0.890 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson-type correlation computed over intraday intervals during the trading session between end-of-interval VWAP and in |
| 572 | `corr_vwap_with_bid_size` | MATRIX | 0.889 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval VWAP and interval bid size (best b |
| 573 | `corr_high_price_with_ask_size` | MATRIX | 0.883 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval high price and interval ask size ( |
| 574 | `corr_low_price_with_ask_size` | MATRIX | 0.883 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval low price and interval ask size (b |
| 575 | `corr_high_price_with_bid_size` | MATRIX | 0.883 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval high price and interval bid size ( |
| 576 | `corr_low_price_with_bid_size` | MATRIX | 0.883 | 价量与波动 | 0 | — | — | — | UNTESTED | Pearson correlation across intraday intervals during the trading day between interval low price and interval bid size (b |
| 577 | `corr_volume_with_high_price_last_quarter_volumeclock` | MATRIX | 0.801 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between volume and high price in the last quarter of volume clock. |
| 578 | `corr_volume_with_low_price_last_quarter_volumeclock` | MATRIX | 0.793 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between volume and low price in the last quarter of volume clock. |
| 579 | `vwap_first_half_volume` | MATRIX | 0.742 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume-weighted average price in the first half of volume clock. |
| 580 | `avg_ask_price_first_half_volume` | MATRIX | 0.725 | 价量与波动 | 0 | — | — | — | UNTESTED | Average ask price during the first half of volume clock. |
| 581 | `avg_bid_price_first_half_volume` | MATRIX | 0.725 | 价量与波动 | 0 | — | — | — | UNTESTED | Average bid price during the first half of volume clock. |
| 582 | `corr_high_with_low_last_quarter_volume` | MATRIX | 0.639 | 价量与波动 | 0 | — | — | — | UNTESTED | Correlation between high and low prices during the last 25% of cumulative daily volume. |
| 583 | `vwap_first_quarter_volume` | MATRIX | 0.427 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average price during the first 25% of cumulative daily volume. |
| 584 | `ask_price_first_quarter_volume` | MATRIX | 0.410 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ask price during the first 25% of cumulative daily volume. |
| 585 | `bid_price_first_quarter_volume` | MATRIX | 0.410 | 价量与波动 | 0 | — | — | — | UNUSABLE | Bid price during the first 25% of cumulative daily volume. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-W169-FASTPV-SPREAD-REVERSED-DEAD`（None）family=None：{"evidence": "wave169 8/8 全负 Sharpe(-0.27~-1.11)：le89bMrx(median_upward_gap-ebitda4)S-1.11、le89bM0x(group_zscore纯快腿)S-0.91、zqY01rWR(vwap_twap)S-0.71、0mR60j8q(corr_high_low)S-0.67+turnover1.88撞HIGH_TURNOVER、npKQMAWz(ascending_channel)S-0.44、LL9rA5RM(形态价差)S-0.51、883YdvnW(corr_bid_ask)S-0.27+CW、9qVmLEJd(cup_handle)S-0.37", "family": "continuation_score/intraday_pv_feats 快腿 - predicted_surprise 慢腿 价差骨
- `EUR-W170-FASTPV-NEGATED-WEAK-DEAD`（None）family=None：{"evidence": "wave170 8/8 全 failed_ra：ZY0MGkpx(median_upward_gap取负)S1.11/fit0.42/SUB0.58/LADDER0.67、YP5JqXpM(cup_handle)S0.37、kqVOle38(ascending)S0.44、akLwvXd9(形态价差)S0.51、d5OoLe0X(dead_cat_recovery)S0.58、A10mKqPY(dynamic_cup)S0.0、1YxPE6dz(bearish_flag)S0.17、58QeWNO5(dead_cat_bounce)S0.1", "family": "predicted_surprise 慢 - continuation_score 快(取负同向) 价差", "finding": "方向修正生效(wave169 -1.11→wave170 +1.
- `EUR-INTRADAY-PV-W126-128-NEAR-MISS`（2026-09-06）family=intraday_pv_feats 事件门控 × 成交量厚尾分位：{"dataset": "intraday_pv_feats", "waves": [126, 127, 128], "region": "EUR", "reason": "机制真实但强度封顶：最强 pwPoekzg sharpe 1.20 / fitness 0.51，未达 D4 资格线(1.25/0.8)。fitness 为束缚约束且已证明不能从 deferred 分支解决。", "rule": "Leave intraday_pv_feats 的下列已试机制：挂单深度倾斜(group_zscore)、宽价差买盘偏离(if_else)、量价确认度(ts_corr/ts_covariance)、VWAP 积压、报价厚尾不对称、T-KB-01 日内版、整数价位聚集全族、成交量时钟不对称。数据集本身不判死——585 字段中仅约 80 个被触及。", "salvage": "★ pwPoekz

