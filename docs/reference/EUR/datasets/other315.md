# other315 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other315` |
| 名称 | Equity Swap Data |
| 类别 | OTHER |
| 数据字段数(平台) | 32 |
| 覆盖率 | 0.5191 |
| 平台已有 alpha | 109 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RICs) and Bloomberg Identifiers (BBIDs), facilitating cross-platform security identification. By enabling seamless translation between two major financial data vendor codes, it supports data integration, reconciliation, and aggregation across trading, risk, and research systems. While not directly predictive of price movements, accurate identifier mapping is essential for merging datasets, tracking instruments across sources, and ensuring consistency in multi-vendor analytics, which indirectly enhances the reliability of price prediction models and market analysis.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **32** |
| 类型分布 | VECTOR×32 |
| 平均覆盖率 | **0.519** |
| 覆盖率区间 | 0.52 ~ 0.52 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 32 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 32 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 32 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 13 | 0.52 | active_notional_value_leg1、contract_notional_value_leg2、leg1_call_option_value |
| 价量与波动 | 10 | 0.52 | contract_trade_price、leg1_spread_expression_format、leg1_spread_value |
| 宏观与行业 | 5 | 0.52 | contract_notional_value_leg1、leg1_fixed_payment_period_count、leg1_floating_reset_period_count |
| 盈利与财务 | 2 | 0.52 | leg1_aggregate_notional_quantity、leg1_put_option_value |
| 搜索与替代数据 | 1 | 0.52 | option_premium_value |
| 交易与微观结构 | 1 | 0.52 | oth315_execution_timestamp |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `active_notional_value_leg1` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | Notional amount becoming effective on the associated unadjusted effective date for Leg 1 in a notional schedule |
| 2 | `contract_notional_value_leg1` | VECTOR | 0.519 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Notional amount for leg 1 (initial or current outstanding); rules for schedules, amendments, FX options, and CDS gross n |
| 3 | `contract_notional_value_leg2` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | For Leg 2, the contractual notional amount; initial notional at inception, updated for lifecycle events to the outstandi |
| 4 | `contract_trade_price` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price specified in the OTC derivative transaction (excluding fees, taxes, commissions); initial or forward price dependi |
| 5 | `leg1_aggregate_notional_quantity` | VECTOR | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Aggregate notional quantity of the underlying asset for Leg 1 over the term of the transaction, updated when available |
| 6 | `leg1_call_option_value` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | For foreign exchange options, the monetary amount that the option gives the right to buy. DMO expects this data element |
| 7 | `leg1_fixed_payment_period_count` | VECTOR | 0.519 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of time units determining payment frequency for the fixed rate on leg 1 (paired with payment period; special case |
| 8 | `leg1_floating_payment_period_count` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | Number of time units (per the payment frequency period) determining how often floating-leg payments occur for leg 1; spe |
| 9 | `leg1_floating_reset_period_count` | VECTOR | 0.519 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of time units determining reset frequency for the floating rate on leg 1 (paired with reset period; special cases |
| 10 | `leg1_notional_quantity_value` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | For Leg 1 negotiated in non-monetary amounts, the fixed notional quantity per schedule period; frequency reported in Qua |
| 11 | `leg1_put_option_value` | VECTOR | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | For FX options, the monetary amount that the option gives the right to sell for Leg 1; expected across asset classes alo |
| 12 | `leg1_quantity_frequency_count` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | Number of time units for the quantity frequency on Leg 1 |
| 13 | `leg1_spread_expression_format` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | For each leg of the transaction, where applicable: manner in which the spread is expressed. |
| 14 | `leg1_spread_value` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | For applicable swaps, the spread applied to leg 1’s floating index or the difference between reference prices; for equit |
| 15 | `leg2_aggregate_notional_quantity` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | Aggregate notional quantity of the underlying for leg 2 over the transaction’s term; updated when available |
| 16 | `leg2_call_option_value` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | For foreign exchange options, the monetary amount that the option gives the right to buy. DMO expects this data element |
| 17 | `leg2_fixed_payment_period_count` | VECTOR | 0.519 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of time units (as defined by the payment frequency period) that determines how often fixed-rate payments occur on |
| 18 | `leg2_floating_payment_period_count` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | Number of time units (as defined by the payment frequency period) that determines how often payments occur for the float |
| 19 | `leg2_floating_reset_period_count` | VECTOR | 0.519 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of time units (as defined by the floating rate reset frequency period) that determines how often resets occur on |
| 20 | `leg2_notional_quantity_value` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | For nonmonetary swaps, the fixed notional quantity per schedule period for leg 2; frequency and unit of measure are repo |
| 21 | `leg2_notional_value_on_effective_date` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | For monetary-amount schedules, the leg 2 notional that becomes effective on the associated unadjusted effective date in |
| 22 | `leg2_put_option_value` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | For foreign exchange options, the monetary amount that the option gives the right to sell. DMO expects this data element |
| 23 | `leg2_quantity_frequency_count` | VECTOR | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | Number of time units for the quantity frequency on Leg 2 |
| 24 | `leg2_spread_expression_format` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | For each leg of the transaction, where applicable: manner in which the spread is expressed. |
| 25 | `leg2_spread_value` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | Spread applied to the floating reference for leg 2 (or overall basket spread for equities/CFDs), expressed per product c |
| 26 | `option_premium_value` | VECTOR | 0.519 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Monetary amount paid by the option buyer for options/swaptions; not applicable if no optionality |
| 27 | `option_strike_expression_format` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | Manner in which the strike price is expressed |
| 28 | `option_strike_value` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | Strike price of the option (exchange rate for FX options); updated when available; also used for volatility/variance swa |
| 29 | `oth315_execution_timestamp` | VECTOR | 0.519 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Date and time the transaction was originally executed, creating the UTI; remains unchanged for the life of the UTI. For |
| 30 | `package_trade_price_format` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | Manner in which the package transaction price is expressed; not applicable if no package or if spread is used |
| 31 | `price_expression_format` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | Manner in which the price is expressed. |
| 32 | `transaction_currency_exchange_rate` | VECTOR | 0.519 | 价量与波动 | 0 | — | — | — | UNUSABLE | Exchange rate agreed at inception between unit and quoted currency, expressed as conversion from unit to quoted currency |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

