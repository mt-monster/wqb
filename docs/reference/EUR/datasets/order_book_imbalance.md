# order_book_imbalance — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `order_book_imbalance` |
| 名称 | Order Book Liquidity and Imbalance Analytics |
| 类别 | OTHER |
| 数据字段数(平台) | 256 |
| 覆盖率 | 0.2122 |
| 平台已有 alpha | 2 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset offers comprehensive analytics derived from Level 1 to Level 3 order books for US and EU equities, focusing on liquidity, order flow, and trade imbalances. It includes metrics such as auction dislocation, order imbalance, liquidity around best bid and offer, trade aggressiveness, and spread measurements. The data also covers order placement, modification, execution behaviors, and venue price quality, providing insights into market microstructure and trading dynamics. By analyzing these metrics, users can identify periods of liquidity stress, anticipate price movements driven by order imbalances, and assess the impact of aggressive trading activity. This information is valuable for predicting short-term price changes, optimizing execution strategies, and understanding the drive

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **256** |
| 类型分布 | VECTOR×256 |
| 平均覆盖率 | **0.212** |
| 覆盖率区间 | 0.19 ~ 0.30 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 256 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 256 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 256 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 242 | 0.21 | bilateral_trade_count、bilateral_trade_notional_value、bilateral_trade_volume |
| 交易与微观结构 | 13 | 0.20 | ebbo_cancelled_order_count、ebbo_filled_order_avg_rest_time、ebbo_filled_order_percentage |
| 修正与预期 | 1 | 0.23 | intraday_price_volatility |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `bilateral_trade_count` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of executions classified as bilateral addressable. This corresponds to the liquidity that is part of the price forming  |
| 2 | `bilateral_trade_notional_value` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the notional value traded classified as bilateral addressable. This corresponds to the liquidity that is part of the price forming |
| 3 | `bilateral_trade_volume` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of shares trades classified as bilateral addressable. This corresponds to the liquidity that is part of the price formi |
| 4 | `dark_trade_count` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of trades executed on dark venues/non-displayed books during the day |
| 5 | `dark_trade_notional_value` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the notional value traded classified as dark addressable. This corresponds to the liquidity that is open to all market participant |
| 6 | `dark_trade_volume` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of shares trades classified as dark addressable. This corresponds to the liquidity that is open to all market participa |
| 7 | `lit_trade_count` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of trades executed on lit/transparent order books during the day |
| 8 | `lit_trade_notional_value` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the notional value traded classified as lit addressable. This corresponds to liquidity open to all market participants, has full p |
| 9 | `lit_trade_volume` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total share volume traded on lit/transparent order books during the day |
| 10 | `nonaddressable_trade_count` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of executions classified as non-addressable. This corresponds to the liquidity that is not part of the price forming pr |
| 11 | `nonaddressable_trade_notional_value` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the notional value traded classified as non-addressable. This corresponds to the liquidity that is not part of the price forming p |
| 12 | `nonaddressable_trade_volume` | VECTOR | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of shares trades classified as non-addressable. This corresponds to the liquidity that is not part of the price forming |
| 13 | `intraday_price_volatility` | VECTOR | 0.230 | 修正与预期 | 0 | — | — | — | UNUSABLE | Realized intraday volatility estimate for the instrument on the given date |
| 14 | `auction_order_imbalance_absolute` | VECTOR | 0.230 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the excess volume after the closing auction that stays on the book after the auction execution. This is the volume of bid orders a |
| 15 | `auction_order_imbalance_notional` | VECTOR | 0.230 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the excess notional volume after the closing auction that stays on the book after the auction execution. This is the notional volu |
| 16 | `auction_order_imbalance_pct_adv` | VECTOR | 0.230 | 价量与波动 | 0 | — | — | — | UNUSABLE | Closing auction order imbalance expressed as a percentage of the stock’s Average Daily Volume |
| 17 | `auction_order_imbalance_pct_auction` | VECTOR | 0.230 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the excess volume after the closing auction that stays on the book after the auction execution as a percentage of volume traded du |
| 18 | `closing_auction_dislocation_1min` | VECTOR | 0.230 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the change (in basis points) between the mid-point price 1 minute prior to the end of continuous trading and the closing price of  |
| 19 | `closing_auction_dislocation_5min` | VECTOR | 0.230 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the change (in basis points) between the mid-point price 5 minutes prior to the end of continuous trading and the closing price of |
| 20 | `closing_auction_dislocation_last` | VECTOR | 0.230 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the change (in basis points) between the last mid-point price during continuous trading and the closing price of the auction on th |
| 21 | `quote_to_trade_ratio` | VECTOR | 0.230 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ratio of quote volume to trade volume away from the EBBO (off-best), used as a proxy for execution quality |
| 22 | `twa_notional_ask_10bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed sell-side liquidity within 10 basis points of the best ask price |
| 23 | `twa_notional_ask_1_level` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed sell-side liquidity at the top (best) ask level |
| 24 | `twa_notional_ask_2_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed sell-side liquidity within the top 2 ask order book levels near the best |
| 25 | `twa_notional_ask_30bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional available on the ask within 30 basis points of the best ask price, in the local trading currency |
| 26 | `twa_notional_ask_3_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed sell-side liquidity within the top 3 ask order book levels near the best |
| 27 | `twa_notional_ask_4_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed sell-side liquidity within the top 4 ask order book levels near the best |
| 28 | `twa_notional_ask_50bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed sell-side liquidity within 50 basis points of the best ask price |
| 29 | `twa_notional_ask_5_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency) available on the ask side within the top 5 order book levels |
| 30 | `twa_notional_bid_10bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed buy-side liquidity within 10 basis points of the best bid price |
| 31 | `twa_notional_bid_1_level` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency) available at the best bid (level 1) |
| 32 | `twa_notional_bid_2_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional available on the bid within the top 2 order book levels near the best bid, in the local trading currency |
| 33 | `twa_notional_bid_30bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency) available on the bid side within 30 bps of the best bid price |
| 34 | `twa_notional_bid_3_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed buy-side liquidity within the top 3 bid order book levels near the best  |
| 35 | `twa_notional_bid_4_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed buy-side liquidity within the top 4 bid order book levels near the best  |
| 36 | `twa_notional_bid_50bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency) available on the bid side within 50 bps of the best bid price |
| 37 | `twa_notional_bid_5_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average notional (local currency amount) of displayed buy-side liquidity within the top 5 bid order book levels near the best  |
| 38 | `twa_order_count_ask_10bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of resting limit orders on the ask side within 10 basis points of the best ask price during the day |
| 39 | `twa_order_count_ask_1_level` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of resting orders at the best ask (level 1) |
| 40 | `twa_order_count_ask_2_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of displayed sell-side limit orders within the top 2 ask order book levels near the best ask price |
| 41 | `twa_order_count_ask_30bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of displayed sell-side limit orders within 30 basis points of the best ask price |
| 42 | `twa_order_count_ask_3_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of displayed sell-side limit orders within the top 3 ask order book levels near the best ask price |
| 43 | `twa_order_count_ask_4_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of displayed sell-side limit orders within the top 4 ask order book levels near the best ask price |
| 44 | `twa_order_count_ask_50bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of displayed sell-side limit orders within 50 basis points of the best ask price |
| 45 | `twa_order_count_ask_5_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average count of limit orders on the ask side across the first 5 price levels from the best ask |
| 46 | `twa_order_count_bid_10bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of displayed buy-side limit orders within 10 basis points of the best bid price |
| 47 | `twa_order_count_bid_1_level` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of displayed buy-side limit orders at the top (best) bid level |
| 48 | `twa_order_count_bid_2_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average count of limit orders on the bid side across the first 2 price levels from the best bid |
| 49 | `twa_order_count_bid_30bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average count of limit orders on the bid side within 30 bps of the best bid price |
| 50 | `twa_order_count_bid_3_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average count of limit orders on the bid side across the first 3 price levels from the best bid |
| 51 | `twa_order_count_bid_4_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average count of limit orders on the bid side across the first 4 price levels from the best bid |
| 52 | `twa_order_count_bid_50bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average count of resting limit orders on the bid within 50 basis points of the best bid price |
| 53 | `twa_order_count_bid_5_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of displayed buy-side limit orders within the top 5 bid order book levels near the best bid price |
| 54 | `twa_share_count_ask_10bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of shares resting on the ask side within 10 bps of the best ask price |
| 55 | `twa_share_count_ask_1_level` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of shares on the ask side at the first price level (best ask) |
| 56 | `twa_share_count_ask_2_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average shares available on the ask side within the top 2 order book levels near the best ask price over the trading day |
| 57 | `twa_share_count_ask_30bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average share count of displayed sell-side liquidity within 30 basis points of the best ask price |
| 58 | `twa_share_count_ask_3_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average share count of displayed sell-side liquidity within the top 3 ask order book levels near the best ask price |
| 59 | `twa_share_count_ask_4_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of shares on the ask side across the first 4 price levels from the best ask |
| 60 | `twa_share_count_ask_50bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average shares available on the ask side within 50 bps of the best ask price |
| 61 | `twa_share_count_ask_5_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average shares available on the ask side within the top 5 order book levels |
| 62 | `twa_share_count_bid_10bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of shares available on the bid within 10 basis points of the best bid price |
| 63 | `twa_share_count_bid_1_level` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of shares on the bid side at the first price level (best bid) |
| 64 | `twa_share_count_bid_2_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of shares on the bid side across the first 2 price levels from the best bid |
| 65 | `twa_share_count_bid_30bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of shares resting on the bid side within 30 bps of the best bid price |
| 66 | `twa_share_count_bid_3_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average share count of displayed buy-side liquidity within the top 3 bid order book levels near the best bid price |
| 67 | `twa_share_count_bid_4_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average share count of displayed buy-side liquidity within the top 4 bid order book levels near the best bid price |
| 68 | `twa_share_count_bid_50bps` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average number of shares resting on the bid side within 50 bps of the best bid price |
| 69 | `twa_share_count_bid_5_levels` | VECTOR | 0.215 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average share count of displayed buy-side liquidity within the top 5 bid order book levels near the best bid price |
| 70 | `final_executed_trade_price` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Last executed trade price of the trading day |
| 71 | `final_midpoint_price` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | End-of-day midpoint of the best bid and ask price |
| 72 | `lowest_executed_price` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest executed trade price observed during the trading day |
| 73 | `lowest_midpoint_price` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest midpoint of the best bid and ask observed during the trading day |
| 74 | `max_executed_trade_price` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest executed trade price observed during the trading day |
| 75 | `max_midpoint_price_daily` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest midpoint of the best bid and ask observed during the trading day |
| 76 | `opening_executed_price` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | First executed trade price of the trading day |
| 77 | `opening_midpoint_price` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Opening midpoint of the best bid and ask price |
| 78 | `final_bid_ask_spread_bps` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Last observed relative bid-ask spread of the day |
| 79 | `last_absolute_bid_ask_spread` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Last observed absolute bid-ask spread of the day in price units |
| 80 | `last_bid_ask_spread_ticks` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Last observed absolute bid-ask spread of the day measured in tick increments |
| 81 | `mean_absolute_bid_ask_spread` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Arithmetic mean absolute bid-ask spread over the day in price units |
| 82 | `mean_bid_ask_spread_ticks` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Arithmetic mean absolute bid-ask spread over the day expressed in tick units |
| 83 | `mean_relative_bid_ask_spread` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Arithmetic mean of the relative bid-ask spread over the day |
| 84 | `time_weighted_spread_bps` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average relative bid-ask spread over the trading day (normalized by price) |
| 85 | `time_weighted_spread_price_units` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average absolute bid-ask spread over the day in price units |
| 86 | `time_weighted_spread_ticks` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average absolute bid-ask spread over the day in tick units |
| 87 | `volume_weighted_relative_spread` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average relative bid-ask spread over the trading day |
| 88 | `volume_weighted_spread_price_units` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average absolute bid-ask spread in price units |
| 89 | `volume_weighted_spread_ticks` | VECTOR | 0.213 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average absolute bid-ask spread over the day in tick units |
| 90 | `time_weighted_avg_trade_price` | VECTOR | 0.212 | 价量与波动 | 0 | — | — | — | UNUSABLE | Time-weighted average trade price over the trading day |
| 91 | `volume_weighted_avg_trade_price` | VECTOR | 0.212 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average trade price over the trading day |
| 92 | `trade_market_impact_coefficient` | VECTOR | 0.211 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the immediate impact of making a trade on the next price that is traded |
| 93 | `duration_best_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time during the continuous trading period where there is at least one order equal to the ask price of the ebbo |
| 94 | `duration_best_bid_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time during the continuous trading period where there is at least one order equal to the bid price and simulta |
| 95 | `duration_best_bid_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time during the continuous trading period where there is at least one order equal to the bid price of the ebbo |
| 96 | `exclusive_duration_best_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time during the continuous trading period where there is exactly one venue with an order equal to the ask pric |
| 97 | `exclusive_duration_best_bid_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time during the continuous trading period where there is exactly one venue with an order equal to the bid pric |
| 98 | `exclusive_duration_best_bid_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time during the continuous trading period where there is exactly one venue with an order equal to the bid pric |
| 99 | `exclusive_ref_duration_best_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time in the continuous trading period where exactly one venue was at the consolidated best ask price. |
| 100 | `exclusive_ref_duration_best_bid_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time in the continuous trading period where exactly one venue was simultaneously at the consolidated best bid  |
| 101 | `exclusive_ref_duration_best_bid_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time in the continuous trading period where exactly one venue was at the consolidated best bid price. |
| 102 | `mean_notional_ask_price_improvement` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean notional amount added to the ask side of the book when this venue sets an improved consolidated ask price. |
| 103 | `mean_notional_ask_price_joiner` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean notional amount added to the ask side of the book when this venue joins an improved consolidated ask price. |
| 104 | `mean_notional_ask_price_worsening` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean notional amount at the first level of the ask side of the book when this venue is the last venue at the consolidated ask  |
| 105 | `mean_notional_bid_price_improvement` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean notional amount added to the bid side of the book when this venue sets an improved consolidated bid price. |
| 106 | `mean_notional_bid_price_joiner` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean notional amount added to the bid side of the book when this venue joins an improved consolidated bid price. |
| 107 | `mean_notional_bid_price_worsening` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean notional amount at the first level of the bid side of the book when this venue is the last venue at the consolidated bid  |
| 108 | `mean_percentage_ask_price_improvement` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of events where this venue improved the consolidated best ask price |
| 109 | `mean_percentage_ask_price_joiner` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of events where this venue was the second venue at an improved consolidated best ask price |
| 110 | `mean_percentage_ask_price_worsening` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of events where this venue was the last venue at the consolidated best ask price before the consolidated price subseque |
| 111 | `mean_percentage_bid_price_improvement` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of events where this venue improved the consolidated best bid price |
| 112 | `mean_percentage_bid_price_joiner` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of events where this venue was the second venue at an improved consolidated best bid price |
| 113 | `mean_percentage_bid_price_worsening` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the number of events where this venue was the last venue at the consolidated best bid price before the consolidated price subseque |
| 114 | `percentage_exclusive_time_best_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time during the continuous trading period where there is exactly one venue with an order equal to the ask price  |
| 115 | `percentage_exclusive_time_best_bid_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time during the continuous trading period where there is exactly one venue with an order equal to the bid price  |
| 116 | `percentage_exclusive_time_best_bid_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time during the continuous trading period where there is exactly one venue with an order equal to the bid price  |
| 117 | `percentage_time_best_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time during the continuous trading period where there is at least one order equal to the ask price of the ebbo. |
| 118 | `percentage_time_best_bid_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time during the continuous trading period where there is at least one order equal to the bid price and simultane |
| 119 | `percentage_time_best_bid_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time during the continuous trading period where there is at least one order equal to the bid price of the ebbo. |
| 120 | `ref_duration_best_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time in the continuous trading period where there was an ask side of the consolidated book. |
| 121 | `ref_duration_best_bid_ask_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time in the continuous trading period. |
| 122 | `ref_duration_best_bid_venue` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total amount of time in the continuous trading period where there was a bid side of the consolidated book. |
| 123 | `twa_notional_ask_price_improvement` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the time-weighted average notional amount added to the ask side of the book when this venue sets an improved consolidated ask pric |
| 124 | `twa_notional_ask_price_joiner` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the time-weighted average notional amount added to the ask side of the book when this venue joins an improved consolidated ask pri |
| 125 | `twa_notional_ask_price_worsening` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the time-weighted average notional amount at the first level of the ask side of the book when this venue is the last venue at the  |
| 126 | `twa_notional_bid_price_improvement` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the time-weighted average notional amount added to the bid side of the book when this venue sets an improved consolidated bid pric |
| 127 | `twa_notional_bid_price_joiner` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the time-weighted average notional amount added to the bid side of the book when this venue joins an improved consolidated bid pri |
| 128 | `twa_notional_bid_price_worsening` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the time-weighted average notional amount at the first level of the bid side of the book when this venue is the last venue at the  |
| 129 | `twa_percentage_ask_price_improvement` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time where this venue improved the consolidated best ask price |
| 130 | `twa_percentage_ask_price_joiner` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time where this venue was the second venue at an improved consolidated best ask price |
| 131 | `twa_percentage_ask_price_worsening` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time where this venue was the last venue at the consolidated best ask price before the consolidated price subseq |
| 132 | `twa_percentage_bid_price_improvement` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time where this venue improved the consolidated best bid price |
| 133 | `twa_percentage_bid_price_joiner` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time where this venue was the second venue at an improved consolidated best bid price |
| 134 | `twa_percentage_bid_price_worsening` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the percentage of time where this venue was the last venue at the consolidated best bid price before the consolidated price subseq |
| 135 | `ebbo_executed_order_count` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total traded volume executed at the European Best Bid and Offer over the day |
| 136 | `ebbo_execution_to_order_ratio` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Ratio of traded volume to quote volume at the EBBO, indicating execution quality |
| 137 | `ebbo_placed_order_count` | VECTOR | 0.207 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total displayed quote volume at the European Best Bid and Offer over the day |
| 138 | `ask_order_deletion_count` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of ask-side order deletions/cancellations during the day |
| 139 | `ask_order_execution_count` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of execution events that filled resting ask-side orders during the day |
| 140 | `ask_order_insertion_count_2` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of new limit order insert events on the ask side during the day |
| 141 | `ask_order_modification_count` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of modification events (e.g., size changes) on the ask side during the day |
| 142 | `ask_order_replacement_count` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of order replacement events on the ask side during the day |
| 143 | `ask_order_volume_after_modification_2` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total volume of modified ask orders |
| 144 | `ask_order_volume_after_replacement` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total volume of replaced ask orders |
| 145 | `ask_order_volume_before_modification` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total volume of modified ask orders |
| 146 | `ask_order_volume_change_modification` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total change in volume of ask orders due to orders being modified. |
| 147 | `ask_order_volume_change_replacement` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the total change in volume of ask orders due to orders being replaced. |
| 148 | `ask_order_volume_deleted` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total share volume removed via cancellations on the ask side during the day |
| 149 | `ask_order_volume_executed` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total share volume executed from resting ask-side orders during the day |
| 150 | `bid_order_deletion_count` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of deletion/cancellation events on the bid side during the day |
| 151 | `bid_order_execution_count` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of execution events that filled resting bid-side orders during the day |
| 152 | `bid_order_insertion_count` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of new limit order insert events on the bid side during the day |
| 153 | `bid_order_modification_count` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of modification events (e.g., size changes) on the bid side during the day |
| 154 | `bid_order_replacement_count_2` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of order replacement events on the bid side during the day |
| 155 | `bid_order_volume_after_modification` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Cumulative new volume (shares) set by modify events on the bid side during the day |
| 156 | `bid_order_volume_after_replacement` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Cumulative new volume (shares) set by replace events on the bid side during the day |
| 157 | `bid_order_volume_before_modification` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Sum of original volumes (before modification) for bid-side orders that were modified |
| 158 | `bid_order_volume_change_modification_2` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Cumulative change in volume (new minus old, in shares) caused by bid-side modify events during the day |
| 159 | `bid_order_volume_change_replacement_2` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Cumulative change in volume (shares) caused by bid-side replace events during the day |
| 160 | `bid_order_volume_deleted` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total share volume removed via cancellations on the bid side during the day |
| 161 | `bid_order_volume_executed` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total share volume executed from resting bid-side orders during the day |
| 162 | `inserted_ask_order_volume` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total volume (shares) of orders inserted on the ask side during the day |
| 163 | `inserted_bid_order_volume` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total share volume added via new limit orders on the bid side during the day |
| 164 | `replaced_ask_order_volume_before` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Sum of original volumes (before replacement) for ask-side orders that were replaced |
| 165 | `replaced_bid_order_volume_before` | VECTOR | 0.205 | 价量与波动 | 0 | — | — | — | UNUSABLE | Sum of original volumes (before replacement) for bid-side orders that were replaced |
| 166 | `avg_rest_time_ask_cancelled_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of ask orders placed at the 1st level of the book which were subsequently cancelled. |
| 167 | `avg_rest_time_ask_cancelled_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for ask-side orders at depth level 2 away from the EBBO that were cancelled |
| 168 | `avg_rest_time_ask_cancelled_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average time in seconds that ask-side limit orders resting 3 levels away from the EBBO remained on the book before being cancelled |
| 169 | `avg_rest_time_ask_cancelled_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of ask orders placed at the 4th level of the book which were subsequently cancelled. |
| 170 | `avg_rest_time_ask_cancelled_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of ask orders placed at the 5th level of the book which were subsequently cancelled. |
| 171 | `avg_rest_time_ask_filled_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of ask orders placed at the 1st level of the book which were subsequently completely filled. |
| 172 | `avg_rest_time_ask_filled_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for ask-side orders at depth level 2 away from the EBBO that were fully filled |
| 173 | `avg_rest_time_ask_filled_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for ask-side orders at depth level 3 away from the EBBO that were fully filled |
| 174 | `avg_rest_time_ask_filled_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of ask orders placed at the 4th level of the book which were subsequently completely filled. |
| 175 | `avg_rest_time_ask_filled_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of ask orders placed at the 5th level of the book which were subsequently completely filled. |
| 176 | `avg_rest_time_ask_partial_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of ask orders placed at the 1st level of the book which were subsequently partially filled. |
| 177 | `avg_rest_time_ask_partial_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for ask-side orders at depth level 2 away from the EBBO that were partially filled |
| 178 | `avg_rest_time_ask_partial_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for ask-side orders at depth level 3 away from the EBBO that were partially filled |
| 179 | `avg_rest_time_ask_partial_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average time in seconds that ask-side limit orders resting 4 levels away from the EBBO remained on the book before being partially filled |
| 180 | `avg_rest_time_ask_partial_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average time in seconds that ask-side limit orders resting 5 levels away from the EBBO remained on the book before being partially filled |
| 181 | `avg_rest_time_bid_cancelled_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average time in seconds that bid-side limit orders resting 1 level away from the EBBO remained on the book before being cancelled |
| 182 | `avg_rest_time_bid_cancelled_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for bid-side orders at depth level 2 away from the EBBO that were cancelled |
| 183 | `avg_rest_time_bid_cancelled_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of bid orders placed at the 3rd level of the book which were subsequently cancelled. |
| 184 | `avg_rest_time_bid_cancelled_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of bid orders placed at the 4th level of the book which were subsequently cancelled. |
| 185 | `avg_rest_time_bid_cancelled_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of bid orders placed at the 5th level of the book which were subsequently cancelled. |
| 186 | `avg_rest_time_bid_filled_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average time in seconds that bid-side limit orders resting 1 level away from the EBBO remained on the book before being fully filled |
| 187 | `avg_rest_time_bid_filled_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for bid-side orders at depth level 2 away from the EBBO that were fully filled |
| 188 | `avg_rest_time_bid_filled_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for bid-side orders at depth level 3 away from the EBBO that were fully filled |
| 189 | `avg_rest_time_bid_filled_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of bid orders placed at the 4th level of the book which were subsequently completely filled. |
| 190 | `avg_rest_time_bid_filled_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average time in seconds that bid-side limit orders resting 5 levels away from the EBBO remained on the book before being fully filled |
| 191 | `avg_rest_time_bid_partial_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of bid orders placed at the 1st level of the book which were subsequently partially filled. |
| 192 | `avg_rest_time_bid_partial_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average resting time in seconds for bid-side orders at depth level 2 away from the EBBO that were partially filled |
| 193 | `avg_rest_time_bid_partial_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Average time in seconds that bid-side limit orders resting 3 levels away from the EBBO remained on the book before being partially filled |
| 194 | `avg_rest_time_bid_partial_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of bid orders placed at the 4th level of the book which were subsequently partially filled. |
| 195 | `avg_rest_time_bid_partial_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the mean resting time (in seconds) of bid orders placed at the 5th level of the book which were subsequently partially filled. |
| 196 | `fill_prob_ask_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that an ask order placed at the 1st level of the book will be filled within 60 seconds. |
| 197 | `fill_prob_ask_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that an ask order placed at the 2nd level of the book will be filled within 60 seconds. |
| 198 | `fill_prob_ask_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that an ask order placed at the 3rd level of the book will be filled within 60 seconds. |
| 199 | `fill_prob_ask_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that an ask order placed at the 4th level of the book will be filled within 60 seconds. |
| 200 | `fill_prob_ask_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that an ask order placed at the 5th level of the book will be filled within 60 seconds. |
| 201 | `fill_prob_bid_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that a bid order placed at the 1st level of the book will be filled within 60 seconds. |
| 202 | `fill_prob_bid_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that a bid order placed at the 2nd level of the book will be filled within 60 seconds. |
| 203 | `fill_prob_bid_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that a bid order placed at the 3rd level of the book will be filled within 60 seconds. |
| 204 | `fill_prob_bid_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that a bid order placed at the 4th level of the book will be filled within 60 seconds. |
| 205 | `fill_prob_bid_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the probability that a bid order placed at the 5th level of the book will be filled within 60 seconds. |
| 206 | `min_rest_time_ask_cancelled_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that ask-side limit orders resting 1 level away from the EBBO remained on the book before being cancelled |
| 207 | `min_rest_time_ask_cancelled_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of ask orders placed at the 2nd level of the book which were subsequently cancelled. |
| 208 | `min_rest_time_ask_cancelled_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that ask-side limit orders resting 3 levels away from the EBBO remained on the book before being cancelled |
| 209 | `min_rest_time_ask_cancelled_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that ask-side limit orders resting 4 levels away from the EBBO remained on the book before being cancelled |
| 210 | `min_rest_time_ask_cancelled_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum resting time in seconds for ask-side orders at depth level 5 away from the EBBO that were cancelled |
| 211 | `min_rest_time_ask_filled_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of ask orders placed at the 1st level of the book which were subsequently completely fi |
| 212 | `min_rest_time_ask_filled_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that ask-side limit orders resting 2 levels away from the EBBO remained on the book before being fully fill |
| 213 | `min_rest_time_ask_filled_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of ask orders placed at the 3rd level of the book which were subsequently completely fi |
| 214 | `min_rest_time_ask_filled_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum resting time in seconds for ask-side orders at depth level 4 away from the EBBO that were fully filled |
| 215 | `min_rest_time_ask_filled_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of ask orders placed at the 5th level of the book which were subsequently completely fi |
| 216 | `min_rest_time_ask_partial_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum resting time in seconds for ask-side orders at depth level 1 away from the EBBO that were partially filled |
| 217 | `min_rest_time_ask_partial_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of ask orders placed at the 2nd level of the book which were subsequently partially fil |
| 218 | `min_rest_time_ask_partial_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that ask-side limit orders resting 3 levels away from the EBBO remained on the book before being partially  |
| 219 | `min_rest_time_ask_partial_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of ask orders placed at the 4th level of the book which were subsequently partially fil |
| 220 | `min_rest_time_ask_partial_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that ask-side limit orders resting 5 levels away from the EBBO remained on the book before being partially  |
| 221 | `min_rest_time_bid_cancelled_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that bid-side limit orders resting 1 level away from the EBBO remained on the book before being cancelled |
| 222 | `min_rest_time_bid_cancelled_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that bid-side limit orders resting 2 levels away from the EBBO remained on the book before being cancelled |
| 223 | `min_rest_time_bid_cancelled_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that bid-side limit orders resting 3 levels away from the EBBO remained on the book before being cancelled |
| 224 | `min_rest_time_bid_cancelled_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that bid-side limit orders resting 4 levels away from the EBBO remained on the book before being cancelled |
| 225 | `min_rest_time_bid_cancelled_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum resting time in seconds for bid-side orders at depth level 5 away from the EBBO that were cancelled |
| 226 | `min_rest_time_bid_filled_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum resting time in seconds for bid-side orders at depth level 1 away from the EBBO that were fully filled |
| 227 | `min_rest_time_bid_filled_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum resting time in seconds for bid-side orders at depth level 2 away from the EBBO that were fully filled |
| 228 | `min_rest_time_bid_filled_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum resting time in seconds for bid-side orders at depth level 3 away from the EBBO that were fully filled |
| 229 | `min_rest_time_bid_filled_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of bid orders placed at the 4th level of the book which were subsequently completely fi |
| 230 | `min_rest_time_bid_filled_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of bid orders placed at the 5th level of the book which were subsequently completely fi |
| 231 | `min_rest_time_bid_partial_lvl1` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of bid orders placed at the 1st level of the book which were subsequently partially fil |
| 232 | `min_rest_time_bid_partial_lvl2` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that bid-side limit orders resting 2 levels away from the EBBO remained on the book before being partially  |
| 233 | `min_rest_time_bid_partial_lvl3` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of bid orders placed at the 3rd level of the book which were subsequently partially fil |
| 234 | `min_rest_time_bid_partial_lvl4` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the minimum resting time (in microseconds) of bid orders placed at the 4th level of the book which were subsequently partially fil |
| 235 | `min_rest_time_bid_partial_lvl5` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Minimum observed time in seconds that bid-side limit orders resting 5 levels away from the EBBO remained on the book before being partially  |
| 236 | `ebbo_cancelled_order_count` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Number of EBBO orders that were cancelled |
| 237 | `ebbo_filled_order_avg_rest_time` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Mean resting time (seconds) for EBBO orders that were fully filled |
| 238 | `ebbo_filled_order_percentage` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Percentage of EBBO orders that were fully filled |
| 239 | `filled_ebbo_order_count` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Number of EBBO orders that were fully filled |
| 240 | `mean_resting_time_cancelled_ebbo_orders` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Mean resting time (seconds) for EBBO orders that were cancelled |
| 241 | `mean_resting_time_partial_fill_ebbo_orders` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Mean resting time (seconds) for EBBO orders that were partially filled |
| 242 | `partial_fill_ebbo_order_count` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Number of EBBO orders that were partially filled |
| 243 | `percentage_cancelled_ebbo_orders` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Percentage of EBBO orders that ended cancelled |
| 244 | `percentage_partial_fill_ebbo_orders` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Percentage of EBBO orders that were partially filled at the EBBO |
| 245 | `total_ebbo_order_count` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Refers to the total number of orders placed at EBBO. |
| 246 | `total_time_cancelled_ebbo_orders` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Total cumulative resting time (seconds) of orders at the EBBO that were cancelled during the day |
| 247 | `total_time_filled_ebbo_orders` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Total cumulative resting time (seconds) of EBBO orders that were fully filled |
| 248 | `total_time_partial_fill_ebbo_orders` | VECTOR | 0.197 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Total cumulative resting time (seconds) of EBBO orders that were partially filled |
| 249 | `ask_trade_imbalance_1_level` | VECTOR | 0.195 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the volume of aggressive asks executed 1 level or more away from the best offer, as a percentage of the total volume traded in tha |
| 250 | `ask_trade_imbalance_2_levels` | VECTOR | 0.195 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the volume of aggressive asks executed 2 levels or more away from the best offer, as a percentage of the total volume traded in th |
| 251 | `ask_trade_imbalance_3_levels` | VECTOR | 0.195 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the volume of aggressive asks executed 3 levels or more away from the best offer, as a percentage of the total volume traded in th |
| 252 | `ask_trade_imbalance_all_levels` | VECTOR | 0.195 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the volume of aggressive asks executed as a percentage of the total volume traded in that period. |
| 253 | `bid_trade_imbalance_1_level` | VECTOR | 0.195 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the volume of aggressive bids executed 1 level or more away from the best bid, as a percentage of the total volume traded in that  |
| 254 | `bid_trade_imbalance_2_levels` | VECTOR | 0.195 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the volume of aggressive bids executed 2 levels or more away from the best bid, as a percentage of the total volume traded in that |
| 255 | `bid_trade_imbalance_3_levels` | VECTOR | 0.195 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the volume of aggressive bids executed 3 levels or more away from the best bid, as a percentage of the total volume traded in that |
| 256 | `bid_trade_imbalance_all_levels` | VECTOR | 0.195 | 价量与波动 | 0 | — | — | — | UNUSABLE | Refers to the volume of aggressive bids executed as a percentage of the total volume traded in that period. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

