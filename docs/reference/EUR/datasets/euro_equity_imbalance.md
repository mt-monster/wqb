# euro_equity_imbalance — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `euro_equity_imbalance` |
| 名称 | European Equity Trading Imbalance Indicators |
| 类别 | OTHER |
| 数据字段数(平台) | 31 |
| 覆盖率 | 0.3089 |
| 平台已有 alpha | 133 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive suite of daily trading imbalance indicators for stocks and ETFs listed on major European exchanges. It includes metrics such as buying and selling turnover, net turnover, participant counts, and aggressive trading activity, all segmented by participant type and order aggressiveness. By capturing the flow of buy and sell orders, as well as the concentration and behavior of different market participants, the dataset enables analysts and quantitative researchers to identify shifts in supply and demand, detect short-term market sentiment, and anticipate potential price movements. The granularity and breadth of these indicators make the dataset particularly valuable for developing and backtesting trading strategies that seek to exploit order flow imbalances

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **31** |
| 类型分布 | VECTOR×31 |
| 平均覆盖率 | **0.309** |
| 覆盖率区间 | 0.25 ~ 0.32 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 31 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 31 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 31 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 14 | 0.32 | aggressive_buying_participant_count、aggressive_net_net_participant_count、aggressive_net_selling_participant_count |
| 价量与波动 | 12 | 0.32 | aggressive_buy_trade_value、aggressive_buy_turnover_concentration_index、aggressive_sell_trade_value |
| 交易与微观结构 | 4 | 0.25 | bucketed_net_order_imbalance_quantile、bucketed_net_order_imbalance_uniform、bucketed_sign_imbalance_quantile |
| 持仓与资金流 | 1 | 0.32 | aggressive_net_buying_participant_count |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `aggressive_buy_trade_value` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | ≥0 or Null. Aggressive buying turnover in euro. |
| 2 | `aggressive_buy_turnover_concentration_index` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | ≥0 and ≤1. The sum of square of aggressive buy market share (measured by aggressive turnover) across all trading members active in this buck |
| 3 | `aggressive_buying_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Count of participants that executed aggressive buys (taker) over the day |
| 4 | `aggressive_net_buying_participant_count` | VECTOR | 0.318 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Count of aggressive net buyers (participants who were net buyers on taker-only flow) over the day |
| 5 | `aggressive_net_net_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | AGG_NB_NET_BUYER – AGG_NB_NET_SELLER |
| 6 | `aggressive_net_selling_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | ≥0 or Null. Number of aggressive net selling participants |
| 7 | `aggressive_participant_net_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Net aggressive participants = AGG_NB_BUYER − AGG_NB_SELLER for the day |
| 8 | `aggressive_sell_trade_value` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Sell-side traded value for aggressive (taker-only) executions, converted to EUR, per instrument-day |
| 9 | `aggressive_sell_turnover_concentration_index` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | ≥0 and ≤1. The sum of square of aggressive sell market share (measured by aggressive turnover) across all trading members active in this buc |
| 10 | `aggressive_selling_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Count of participants that executed aggressive sells (taker) over the day |
| 11 | `buy_market_share_std_rescaled` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | The sum of buying market share rescaled by its standard deviation of last month across all trading members active in this bucket. |
| 12 | `buy_turnover_concentration_index` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Concentration (HHI-like) of buy-side turnover across participants, per day |
| 13 | `buying_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Count of participants that bought at least once over the day |
| 14 | `net_aggressive_trade_value` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | AGG_BUY_TURNOVER – AGG_SELL_TURNOVER |
| 15 | `net_buying_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Count of participants that were net buyers over the day |
| 16 | `net_market_share_std_rescaled` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | BUY_MS_STD-SELL_MS_STD |
| 17 | `net_net_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | NB_NET_BUYER – NB_NET_SELLER |
| 18 | `net_selling_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Count of participants that were net sellers over the day |
| 19 | `net_trade_value` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Net traded value = BUY_TURNOVER − SELL_TURNOVER (EUR) for the day |
| 20 | `participant_net_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Net participant count (number of buyers minus number of sellers) for the instrument/day |
| 21 | `sell_market_share_std_rescaled` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | The sum of selling market share rescaled by its standard deviation of last month across all trading members active in this bucket. |
| 22 | `sell_turnover_concentration_index` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Concentration (HHI-like) of sell-side turnover across participants, per day |
| 23 | `selling_participant_count` | VECTOR | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Count of participants that sold at least once over the day |
| 24 | `session_close_price` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Closing price of the instrument in trading currency for the day |
| 25 | `session_open_price` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Opening price of the instrument in trading currency for the day |
| 26 | `total_buy_trade_value` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total buy-side traded value, converted to EUR, per instrument-day |
| 27 | `total_sell_trade_value` | VECTOR | 0.318 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total sell-side traded value, converted to EUR, per instrument-day |
| 28 | `bucketed_net_order_imbalance_quantile` | VECTOR | 0.251 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Compute for each participant the sign of its net underlying data on each bucket created with quantile method, then sum over buckets for ea |
| 29 | `bucketed_net_order_imbalance_uniform` | VECTOR | 0.251 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Compute for each participant the sign of its net underlying data on each bucket created with uniform method, then sum over buckets for eac |
| 30 | `bucketed_sign_imbalance_quantile` | VECTOR | 0.251 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Compute for each participant the sign of its net underlying data on each bucket created with quantile method, then sum over buckets for ea |
| 31 | `bucketed_sign_imbalance_uniform` | VECTOR | 0.251 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Compute for each participant the sign of its net underlying data on each bucket created with uniform method, then sum over buckets for eac |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

