# analyst_earnings_ibes — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst_earnings_ibes` |
| 名称 | Global Analyst Earnings Forecasts |
| 类别 | MODEL |
| 数据字段数(平台) | 42 |
| 覆盖率 | 0.9976 |
| 平台已有 alpha | 22 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive global analyst earnings forecasts, consensus estimates, and actuals for over 60,000 companies, sourced from broker and sell-side analyst submissions. It includes detailed and summary-level data on key financial metrics such as earnings per share (EPS), revenue, cash flow, and segment-level results, as well as analyst recommendations and price targets. The dataset tracks both current and historical estimates, revisions, and company-issued guidance, with extensive metadata on contributors, accounting standards, and industry classifications. By aggregating and updating analyst expectations in near real-time, this dataset enables users to monitor market sentiment, identify earnings momentum, and anticipate potential surprises—making it a valuable tool for pr

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **42** |
| 类型分布 | MATRIX×42 |
| 平均覆盖率 | **0.998** |
| 覆盖率区间 | 0.98 ~ 1.00 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 42 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 42 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 42 | 1.00 | closing_price_dlr1、closing_price_dlr2、closing_price_dlr3 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `closing_price_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily closing price for the security, D1-delayed, point-in-time, event-masked, split- and FX-adjusted |
| 2 | `closing_price_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Closing price for the trading day, split- and FX-adjusted, point-in-time and D1-delayed, event-masked |
| 3 | `closing_price_dlr3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Closing price for the day (split/FX-adjusted, PIT, D1-delayed, event-masked) |
| 4 | `five_day_total_return_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 5 trading days for Americas-region equities, D1-delayed, point-in-time, split/FX-adjusted and |
| 5 | `five_day_total_return_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 5 trading days for Europe, D1-delayed and point-in-time, split/FX-adjusted and event-masked ( |
| 6 | `five_day_total_return_dlra1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Rolling stock return over the last 5 trading days for Europe; D1-delayed, point-in-time, split/FX-adjusted, masked if an |
| 7 | `highest_price_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily highest traded price (session high) for the security, D1-delayed, point-in-time, event-masked, split- and FX-adjus |
| 8 | `highest_price_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest traded price of the day, split- and FX-adjusted, point-in-time and D1-delayed, event-masked |
| 9 | `highest_price_dlr3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest trade price of the day (split/FX-adjusted, PIT, D1-delayed, event-masked) |
| 10 | `lowest_price_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily lowest traded price (session low) for the security, D1-delayed, point-in-time, event-masked, split- and FX-adjuste |
| 11 | `lowest_price_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Lowest traded price of the day, split- and FX-adjusted, point-in-time and D1-delayed, event-masked |
| 12 | `lowest_price_dlr3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Lowest trade price of the day (split/FX-adjusted, PIT, D1-delayed, event-masked) |
| 13 | `one_day_total_return_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily (1-day) stock return for Americas-region equities, D1-delayed, point-in-time, split/FX-adjusted and event-masked |
| 14 | `one_day_total_return_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily stock return (1 trading day) for Europe, D1-delayed and point-in-time, split/FX-adjusted and event-masked |
| 15 | `one_day_total_return_dlra1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Total return for the most recent trading day. |
| 16 | `opening_price_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily opening price for the stock in the Europe region (D1-delayed, point-in-time, split- and FX-adjusted, event-masked) |
| 17 | `opening_price_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Opening price for the trading day, split- and FX-adjusted, point-in-time and D1-delayed, event-masked |
| 18 | `opening_price_dlr3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Opening price for the day (split/FX-adjusted, PIT, D1-delayed, event-masked) |
| 19 | `trading_volume_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Total traded volume for the day, D1-delayed, point-in-time, event-masked per calendar and events |
| 20 | `trading_volume_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Europe region daily traded volume, D1-delayed, point-in-time, with event and calendar masking |
| 21 | `trading_volume_dlr3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily traded share volume for the security (PIT, D1-delayed, event-masked) |
| 22 | `twenty_day_total_return_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 20 trading days for Americas-region equities, D1-delayed, point-in-time, split/FX-adjusted an |
| 23 | `twenty_day_total_return_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 20 trading days for Europe, D1-delayed and point-in-time, split/FX-adjusted and event-masked |
| 24 | `twenty_day_total_return_dlra1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Rolling stock return over the last 20 trading days for Europe; D1-delayed, point-in-time, split/FX-adjusted, masked if a |
| 25 | `sixty_day_total_return_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 60 trading days for Americas-region equities, D1-delayed, point-in-time, split/FX-adjusted an |
| 26 | `sixty_day_total_return_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 60 trading days for Europe, D1-delayed and point-in-time, split/FX-adjusted and event-masked |
| 27 | `market_capitalization_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Market capitalization as of the as-of-date close (price × shares outstanding), D1-delayed, point-in-time, event-masked |
| 28 | `market_capitalization_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Europe region market capitalization as of close (price times shares outstanding), D1-delayed, point-in-time, currency- a |
| 29 | `shares_outstanding_dlr1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Shares outstanding for the stock as of the as-of-date in the Europe region (D1-delayed, point-in-time, masked if unavail |
| 30 | `shares_outstanding_dlr2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Shares outstanding as of the as-of-date, point-in-time and D1-delayed, masked when unavailable or invalid |
| 31 | `market_capitalization_dlr3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Market capitalization as of the as-of-date close, computed as price × shares outstanding (PIT, D1-delayed, event-masked) |
| 32 | `shares_outstanding_dlr3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Shares outstanding as of the as-of-date (PIT, D1-delayed, event-masked) |
| 33 | `sixty_day_total_return_dlra1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Rolling stock return over the last 60 trading days for Europe; D1-delayed, point-in-time, split/FX-adjusted, masked if a |
| 34 | `volume_weighted_avg_price_dlr2` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Europe region daily volume-weighted average price, D1-delayed, point-in-time, split- and currency-adjusted, event-masked |
| 35 | `volume_weighted_avg_price_dlr1` | MATRIX | 0.998 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily volume-weighted average price, D1-delayed, point-in-time, event-masked, split- and FX-adjusted |
| 36 | `one_twenty_day_total_return_dlr2` | MATRIX | 0.995 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 120 trading days for Europe, D1-delayed and point-in-time, split/FX-adjusted and event-masked |
| 37 | `one_twenty_day_total_return_dlr1` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 120 trading days for Americas-region equities, D1-delayed, point-in-time, split/FX-adjusted a |
| 38 | `one_twenty_day_total_return_dlra1` | MATRIX | 0.994 | 价量与波动 | 0 | — | — | — | UNTESTED | Rolling stock return over the last 120 trading days for Europe; D1-delayed, point-in-time, split/FX-adjusted, masked if |
| 39 | `volume_weighted_avg_price_dlr3` | MATRIX | 0.983 | 价量与波动 | 0 | — | — | — | UNTESTED | Volume-weighted average price for the day (split/FX-adjusted, PIT, D1-delayed, event-masked) |
| 40 | `two_fifty_day_total_return_dlr2` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 250 trading days for Europe, D1-delayed and point-in-time, split/FX-adjusted and event-masked |
| 41 | `two_fifty_day_total_return_dlra1` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | Rolling stock return over the last 250 trading days for Europe; D1-delayed, point-in-time, split/FX-adjusted, masked if |
| 42 | `two_fifty_day_total_return_dlr1` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the last 250 trading days for Americas-region equities, D1-delayed, point-in-time, split/FX-adjusted a |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-AEIBES-W125-OPERATOR-LEVERAGE-WEAK`（2026-09-06）family=analyst_earnings_ibes event-masked OHLCV × 未用算子族：{"dataset": "analyst_earnings_ibes", "wave": 125, "region": "EUR", "reason": "8 个互异机制全 ra_failed；整波最强 /S/=0.88、正向最强 0.42，fitness 峰值仅 0.11——远低于 D4 资格线(1.25/0.8)。event-masked OHLCV 在 EUR/D1 的横截面区分度不足。", "rule": "Leave analyst_earnings_ibes 这 8 个机制（规模桶内漂移残差/日内分歧/加速度门控翻转/量价确认度/执行压力残差/彩票需求/T-KB-01 单集跨周期）。不判死整个数据集——换手率方向有存活线索见 salvage。", "salvage": "★ ts_quantile(divide(trading_volume_dlr2, shares_outst

