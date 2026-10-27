# equity_conc_metrics — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `equity_conc_metrics` |
| 名称 | Equity Market Concentration Metrics |
| 类别 | OTHER |
| 数据字段数(平台) | 18 |
| 覆盖率 | 0.1965 |
| 平台已有 alpha | 1 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides detailed metrics on equity market concentration for Nordic and Baltic exchanges, utilizing the Herfindahl–Hirschman Index (HHI) methodology. It includes measures of overall market concentration, as well as breakdowns by trade type (aggressive, passive, buy, sell) and participant category (financial intermediaries, non-financial entities). By tracking the dominance of key entities and shifts in trading activity, the dataset helps identify periods of reduced competition or increased market control. These insights can be valuable for predicting price movements, as changes in concentration often precede volatility, liquidity shifts, or directional trends in equity prices.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **18** |
| 类型分布 | VECTOR×18 |
| 平均覆盖率 | **0.197** |
| 覆盖率区间 | 0.20 ~ 0.20 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 18 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 18 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 18 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 13 | 0.20 | aggressive_order_concentration_score、buy_side_trade_concentration_index、daily_total_shares_traded |
| 其他 | 4 | 0.20 | daily_market_participant_count、listed_shares_count、market_participant_concentration_index |
| 宏观与行业 | 1 | 0.20 | market_value_local_currency |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `aggressive_order_concentration_score` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) for aggressive (liquidity-taking) trades |
| 2 | `buy_side_trade_concentration_index` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) for buy-side trades overall |
| 3 | `daily_market_participant_count` | VECTOR | 0.197 | 其他 | 0 | — | — | — | UNUSABLE | Number of active market participants (unique legal entities) trading the stock on that day and venue |
| 4 | `daily_total_shares_traded` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total number of shares traded on the venue (MIC) during the day |
| 5 | `daily_trading_value_eur` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total traded value during the day in EUR |
| 6 | `daily_trading_value_local_currency` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total traded value during the day in local currency |
| 7 | `intermediary_buy_order_concentration` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) among intermediary/professional participants on buy-side trades |
| 8 | `intermediary_sell_order_concentration` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) among intermediary/professional participants on sell-side trades |
| 9 | `intermediary_trade_concentration_index` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) among intermediary/professional participants overall |
| 10 | `listed_shares_count` | VECTOR | 0.197 | 其他 | 0 | — | — | — | UNUSABLE | Number of shares outstanding/listed for the company |
| 11 | `market_participant_concentration_index` | VECTOR | 0.197 | 其他 | 0 | — | — | — | UNUSABLE | Overall participant concentration for the stock-day-venue using HHI (0–1) |
| 12 | `market_value_eur` | VECTOR | 0.197 | 其他 | 0 | — | — | — | UNUSABLE | Market capitalization in EUR |
| 13 | `market_value_local_currency` | VECTOR | 0.197 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Market capitalization in local currency |
| 14 | `natural_entity_sell_order_concentration` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) among natural person (retail) participants on sell-side trades |
| 15 | `natural_entity_trade_concentration` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) among natural person (retail) participants overall |
| 16 | `ownership_concentration_natural_buy_orders` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) among natural person (retail) participants on buy-side trades |
| 17 | `passive_order_concentration_score` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) for passive (liquidity-providing) trades |
| 18 | `sell_side_trade_concentration_index` | VECTOR | 0.197 | 价量与波动 | 0 | — | — | — | UNUSABLE | HHI concentration metric (0–1) for sell-side trades overall |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

