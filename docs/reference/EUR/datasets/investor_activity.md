# investor_activity — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `investor_activity` |
| 名称 | Nordic Baltic Investor Activity Trends |
| 类别 | PV |
| 数据字段数(平台) | 47 |
| 覆盖率 | 0.1644 |
| 平台已有 alpha | 9 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides detailed indicators and statistics on the trading behavior of retail and professional investors across Nordic and Baltic equity markets. It includes metrics such as trading volume, turnover, net buying/selling, and confidence/activity scores at the security level, segmented by investor type. By analyzing the split between retail and professional investor activity, as well as their net positions and order flows, users can gain insights into market sentiment, liquidity, and potential price movements. The dataset is particularly useful for identifying shifts in market dynamics, understanding the impact of different investor groups, and predicting short-term price trends based on changes in investor confidence and activity.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **47** |
| 类型分布 | VECTOR×47 |
| 平均覆盖率 | **0.164** |
| 覆盖率区间 | 0.16 ~ 0.16 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 47 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 47 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 47 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 31 | 0.16 | average_trade_price、average_trade_price_eur、average_trade_price_professional |
| 其他 | 10 | 0.16 | market_capitalization_eur、net_professional_buying_selling_value_eur、net_retail_buying_selling_value_eur |
| 交易与微观结构 | 3 | 0.16 | orders_placed_professional_investors_daily、orders_placed_retail_investors_daily、total_orders_placed_daily |
| 宏观与行业 | 2 | 0.16 | net_professional_buying_selling_value、net_retail_buying_selling_value |
| 盈利与财务 | 1 | 0.16 | company_equity_valuation_amount |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `average_trade_price` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average executed price for the day in local currency across all participants |
| 2 | `average_trade_price_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average executed price for the day in EUR across all participants |
| 3 | `average_trade_price_professional` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average executed price for professional trades in local currency |
| 4 | `average_trade_price_professional_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average executed price for professional activity during the day in EUR |
| 5 | `average_trade_price_retail` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average executed price for retail activity during the day in local currency |
| 6 | `average_trade_price_retail_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volume-weighted average executed price for retail trades, expressed in EUR |
| 7 | `closing_trade_price` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Last executed price of the session in local currency |
| 8 | `closing_trade_price_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Last executed price of the session expressed in EUR |
| 9 | `company_equity_valuation_amount` | VECTOR | 0.164 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Market capitalization of the instrument in local currency |
| 10 | `highest_executed_price_professional` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest executed price during the day within professional trades in local currency |
| 11 | `highest_executed_price_professional_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest executed price within professional activity during the session, in EUR |
| 12 | `highest_executed_price_retail` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest executed price within retail activity during the session in local currency |
| 13 | `highest_executed_price_retail_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest executed price within retail activity during the session, in EUR |
| 14 | `highest_executed_trade_price` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest executed price during the day in local currency across all activity |
| 15 | `highest_executed_trade_price_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Highest executed price during the session, expressed in EUR |
| 16 | `lowest_executed_price_professional` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest executed price during the day within professional trades in local currency |
| 17 | `lowest_executed_price_professional_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest executed price during the day within professional trades, expressed in EUR |
| 18 | `lowest_executed_price_retail` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest executed price during the day within retail trades in local currency |
| 19 | `lowest_executed_price_retail_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest executed price during the day within retail trades, expressed in EUR |
| 20 | `lowest_executed_trade_price` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest executed price during the day in local currency across all activity |
| 21 | `lowest_executed_trade_price_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Lowest executed price during the session, expressed in EUR |
| 22 | `market_capitalization_eur` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Market capitalization of the instrument expressed in EUR |
| 23 | `net_professional_buying_selling_value` | VECTOR | 0.164 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Net buying or selling value by professional participants for the day in local currency, positive for net buying and negative for net selling |
| 24 | `net_professional_buying_selling_value_eur` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Net buying or selling value aggregated across professional participants for the day in EUR |
| 25 | `net_retail_buying_selling_value` | VECTOR | 0.164 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Net buying or selling value by retail participants for the day in local currency, positive for net buying and negative for net selling |
| 26 | `net_retail_buying_selling_value_eur` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Net buying or selling value by retail participants for the day in EUR; positive means net buying, negative net selling |
| 27 | `opening_trade_price` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | First executed price of the session in local currency |
| 28 | `opening_trade_price_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | First executed price of the day expressed in EUR |
| 29 | `orders_placed_professional_investors_daily` | VECTOR | 0.164 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Number of orders placed by professional participants during the day |
| 30 | `orders_placed_retail_investors_daily` | VECTOR | 0.164 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Number of orders placed by retail participants during the day |
| 31 | `professional_investor_trading_turnover` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily traded value attributable to professional participants in local currency |
| 32 | `professional_investor_trading_turnover_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total traded value by professional participants during the day in EUR |
| 33 | `retail_investor_trading_turnover` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily traded value attributable to retail participants in local currency |
| 34 | `retail_investor_trading_turnover_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total traded value by retail participants during the day in EUR |
| 35 | `shares_purchased_professional_investors_daily` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Number of shares bought during the day by professional participants |
| 36 | `shares_purchased_retail_investors_daily` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Number of shares bought during the day by retail participants |
| 37 | `shares_sold_professional_investors_daily` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Number of shares sold by professional participants during the day |
| 38 | `shares_sold_retail_investors_daily` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Number of shares sold during the day by retail participants |
| 39 | `shares_traded_professional_investors_daily` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of shares traded by professional participants during the day |
| 40 | `shares_traded_retail_investors_daily` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total number of shares traded by retail participants during the day |
| 41 | `total_orders_placed_daily` | VECTOR | 0.164 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Total number of orders during the day across all participants |
| 42 | `total_shares_listed` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Number of shares outstanding or listed for the instrument |
| 43 | `total_shares_purchased_daily` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Total number of shares bought during the day across all participants |
| 44 | `total_shares_sold_daily` | VECTOR | 0.164 | 其他 | 0 | — | — | — | UNUSABLE | Total number of shares sold during the day across all participants |
| 45 | `total_shares_traded_daily` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total number of shares traded during the day across all participants |
| 46 | `total_trading_turnover_eur` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total traded value for the day in EUR across all participants |
| 47 | `total_trading_turnover_value` | VECTOR | 0.164 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total daily traded value for the instrument across all participants in local currency |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

