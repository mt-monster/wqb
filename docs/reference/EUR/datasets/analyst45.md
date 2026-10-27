# analyst45 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst45` |
| 名称 | Analyst Trade Ideas |
| 类别 | ANALYST |
| 数据字段数(平台) | 61 |
| 覆盖率 | 1.0 |
| 平台已有 alpha | 244 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Bloomberg IDs (BBIDs) and Refinitiv Instrument Codes (RICs), facilitating cross-platform identification of securities. It is sourced from both Bloomberg and Refinitiv, ensuring high coverage and accuracy. While not intended for general research or direct price prediction, this mapping is essential for data integration, enabling analysts and portfolio managers to link and synchronize datasets from different vendors. By ensuring consistent instrument identification, it supports robust multi-source analytics, backtesting, and the construction of unified trading universes, which are foundational for any quantitative or fundamental price movement analysis.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **61** |
| 类型分布 | VECTOR×61 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 61 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 53 | 86.9% |
| DEAD | 3 | 4.9% |
| DEAD_TURNOVER | 3 | 4.9% |
| DEAD_STATIC | 2 | 3.3% |

- 已实测字段：**8** 个（13%），best_sharpe 最高 **0.38**，中位 0.07

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 41 | 1.00 | anl45_ad_ret_per、anl45_rel_index_ret_per、anl45_jensensalpha |
| 其他 | 11 | 1.00 | anl45_ang_inv、anl45_avg_dur、anl45_bias_weighted_ret |
| 宏观与行业 | 6 | 1.00 | benchmark_currency_code、conversion_rate_summary、anl45_bm_exchange_rate |
| 修正与预期 | 2 | 1.00 | anl45_new_value、anl45_old_value |
| 搜索与替代数据 | 1 | 1.00 | anl45_time |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl45_ad_ret_per` | VECTOR | 1.000 | 价量与波动 | 1 | 0.38 | 0.43 | — | DEAD | Average daily percent return over the idea’s lifetime |
| 2 | `anl45_rel_index_ret_per` | VECTOR | 1.000 | 价量与波动 | 2 | 0.32 | — | — | DEAD_TURNOVER | Difference in return percentage between the idea and the comparative index |
| 3 | `anl45_jensensalpha` | VECTOR | 1.000 | 价量与波动 | 3 | 0.21 | -0.85 | — | DEAD | Risk-adjusted performance measure representing return over market |
| 4 | `benchmark_currency_code` | VECTOR | 1.000 | 宏观与行业 | 1 | 0.07 | -0.58 | — | DEAD_STATIC | Currency of the benchmark |
| 5 | `anl45_ad_rel_ret_per` | VECTOR | 1.000 | 价量与波动 | 4 | 0.02 | -0.05 | — | DEAD_TURNOVER | Average daily index relative return percentage |
| 6 | `conversion_rate_summary` | VECTOR | 1.000 | 宏观与行业 | 1 | 0.00 | 0.00 | — | DEAD_STATIC | Exchange rate between investment and performance currencies |
| 7 | `anl45_beta` | VECTOR | 1.000 | 价量与波动 | 1 | -0.14 | -0.07 | — | DEAD | A measure of the volatility or systematic risk of a security compared to the market, updated monthly based on last 20 mo |
| 8 | `anl45_tot_ret` | VECTOR | 1.000 | 价量与波动 | 1 | -0.47 | -0.66 | — | DEAD_TURNOVER | Sum of realised and unrealised returns |
| 9 | `anl45_ang_inv` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Time-weighted average investment |
| 10 | `anl45_avg_dur` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Average age of the idea limited to the selected period |
| 11 | `anl45_avg_initial_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average share price weighted by volume of each share purchase |
| 12 | `anl45_avg_initial_prc_wfee` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The avg initial price adjusted to include fee payment when fees are applied |
| 13 | `anl45_bias_weighted_ret` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Non-Functional |
| 14 | `anl45_bm_exchange_rate` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate by which the benchmark will be measured |
| 15 | `anl45_bm_fx_ret` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | FX return made by the benchmark due to currency movements |
| 16 | `anl45_bm_ret` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Return of the benchmark index |
| 17 | `anl45_bm_ret_wo_fx` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Benchmark’s return excluding foreign exchange effects (raw benchmark return) |
| 18 | `anl45_closed_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price at which the idea was closed |
| 19 | `anl45_current_inv` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Current investment amount, including increases and partial closures |
| 20 | `anl45_days_since_inception` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Number of trading days since the idea was submitted |
| 21 | `anl45_idea_count` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Number of ideas in a group, useful when grouping ideas |
| 22 | `anl45_index_period_end_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Benchmark or index end price for the selected performance period |
| 23 | `anl45_index_period_start_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Benchmark or index start price for the selected performance period |
| 24 | `anl45_index_ret_per` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Return percentage had the investment been made in the selected index |
| 25 | `anl45_initial_inv` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Initial investment amount allocated to the idea |
| 26 | `anl45_inv_exchange_rate` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Exchange rate between stock and investment currencies, typically the FX rate on the period end date |
| 27 | `anl45_latest_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The current price of the stock in the idea |
| 28 | `anl45_net_market_exposure` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Difference in fractional total value between long and short ideas (net market exposure) |
| 29 | `anl45_new_value` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | New value set for the stop-loss percent, target price, or capital allocation |
| 30 | `anl45_old_value` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Previous value of the stop-loss percent, target price, or capital allocation before the latest change |
| 31 | `anl45_period_end_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Close price on day at end of selected period |
| 32 | `anl45_period_start_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Close price on day before start of selected period |
| 33 | `anl45_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The price given to the investment change |
| 34 | `anl45_prc_change_per_today` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent change in stock price since previous close of day price |
| 35 | `anl45_prc_change_today` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in stock price since previous day close |
| 36 | `anl45_prev_close_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Last available close price for the stock |
| 37 | `anl45_probability` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Tag giving a quantitative measure of conviction |
| 38 | `anl45_real_ret` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Realized return from closed portions of the idea since inception |
| 39 | `anl45_real_ret_today` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Increase in realized return since the previous market close |
| 40 | `anl45_real_value` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Monetary value of the realized (closed) portion of the idea |
| 41 | `anl45_rel_index_ret` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Difference in return percentage between the idea and the comparative index |
| 42 | `anl45_rel_ret_per_today` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative return percentage today |
| 43 | `anl45_rel_ret_today` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Increase in realised return since last market close |
| 44 | `anl45_ret_per_today` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentage return since last market close |
| 45 | `anl45_ret_today` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Increase in realised return since last market close |
| 46 | `anl45_risk_free_rate` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The unrealised return on an open idea |
| 47 | `anl45_stock_ret_per` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Net total return from all ideas since the previous market close |
| 48 | `anl45_stock_ret_per_relative` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average daily return percentage had the investment been made in the relative benchmark index |
| 49 | `anl45_target_prc` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Author’s stated likely exit price for the idea |
| 50 | `anl45_time` | VECTOR | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Approximate time horizon for the idea |
| 51 | `anl45_tot_ret_per` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Total return as a percentage of average investment |
| 52 | `anl45_tot_ret_wo_fx` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Total return excluding any foreign exchange effects |
| 53 | `anl45_transaction_charge` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Transaction fee charged for the idea (in calculation currency) |
| 54 | `anl45_treynor_ratio` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | A ratio that measures returns earned in excess of that which could have been earned on a riskless investment (such as th |
| 55 | `anl45_unreal_ret` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Unrealized return on the open idea (mark-to-market) |
| 56 | `anl45_unreal_ret_today` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Increase in unrealised return since the last market close |
| 57 | `anl45_unreal_value` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Unrealised value of an open idea |
| 58 | `currency_gain_percentage` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | FX-driven return expressed as a percentage of the invested amount |
| 59 | `currency_gain_value` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Return generated from variations in foreign exchange |
| 60 | `investment_currency_code` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency of the investment |
| 61 | `security_trading_currency_3` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Currency in which the security is traded |

## 六、本地回测证据

- 本地累计回测 **14** 条；其中 `ra_failed_checks` 为空的 **14** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `RRVn5GV1` | 0.38 | 0.16 | 0.43 | — | 0.07 | 0 | 117 | `rank(ts_mean(vec_avg(anl45_ad_ret_per), 66))` |
| `Vk6xE1pM` | 0.32 | 0.11 | — | — | 0.06 | 0 | s2_analyst45_d1 | `rank(ts_mean(vec_avg(anl45_rel_index_ret_per), 66))` |
| `A10Vbjwg` | 0.21 | 0.05 | — | — | 0.06 | 0 | s2_analyst45_d1 | `rank(ts_mean(vec_avg(anl45_jensensalpha), 66))` |
| `pwPAWLeo` | 0.07 | 0.01 | -0.58 | — | 0.02 | 0 | 117 | `rank(ts_mean(vec_avg(benchmark_currency_code), 66))` |
| `P0ZdPVmJ` | 0.02 | 0.00 | -0.05 | — | 1.66 | 0 | 117 | `if_else(ts_delta(vec_avg(anl45_ad_rel_ret_per), 5) > 0, rank(vec_avg(anl45_ad_rel_ret_per)` |
| `9qVxKZwV` | 0.02 | 0.00 | — | — | 0.15 | 0 | s2_analyst45_d1 | `group_rank(ts_mean(vec_avg(anl45_jensensalpha), 22), subindustry)` |
| `9qVLGNVK` | 0.00 | 0.00 | 0.00 | — | 0.00 | 0 | 117 | `group_rank(ts_backfill(vec_avg(conversion_rate_summary), 66), industry)` |
| `blR5xw1N` | -0.14 | -0.04 | -0.07 | — | 0.09 | 0 | 117 | `trade_when(ts_count_nans(vec_avg(anl45_beta), 22) < 5, rank(vec_avg(anl45_beta)), NaN)` |
| `MP1ogrNo` | -0.31 | -0.04 | -0.85 | — | 1.46 | 0 | 117 | `rank(ts_decay_linear(vec_avg(anl45_jensensalpha), 21))` |
| `0mRYdO72` | -0.43 | -0.05 | — | — | 1.58 | 0 | s2_analyst45_d1 | `rank(zscore(vec_avg(anl45_rel_index_ret_per)))` |
| `A10MLA8l` | -0.47 | -0.06 | -0.66 | — | 1.56 | 0 | 117 | `rank(subtract(vec_avg(anl45_tot_ret), vec_avg(anl45_bm_ret)))` |
| `O0rE63jR` | -0.53 | -0.09 | -0.65 | — | 1.61 | 0 | 117 | `ts_zscore(ts_delta(vec_avg(anl45_ad_rel_ret_per), 21), 22)` |
| `XgW9Lmnm` | -0.54 | -0.10 | — | — | 1.64 | 0 | s2_analyst45_d1 | `rank(ts_delta(vec_avg(anl45_ad_rel_ret_per), 22))` |
| `ZY0eXJ91` | -1.24 | -0.26 | -1.59 | — | 1.56 | 0 | 117 | `rank(multiply(ts_zscore(vec_avg(anl45_ad_rel_ret_per), 66), ts_zscore(vec_avg(anl45_ad_ret` |

## 七、判死记录（sealed dead_end）

- `EUR-ANL11-ESG-SLOWVAR-LONGCOUNT`（None）family=analyst11 ESG 评分体系（三支柱 + 行业排名 + 改善动量）：{"critical_lesson": "★ coverage 元数据虚报（缺陷#3 第4次坐实）：catalog 报 cov=0.9123/0.9087，实际回测 longCount 仅 51-52（占 TOP2500 的 2%）。选数据集时不能信 catalog coverage，必须用 1-2 条探针实测 longCount。", "dataset": "analyst11", "evidence": {"1YxzzPmQ": "ESG 绝对水平 rank(overall_sustainability_score_2)：S-0.68/F-0.13/TVR0.0985/longCount 52/CW FAIL", "A1077x7l": "行业内排名 rank(reverse(anl11_esgreg_industryrnk))：S-0.25/F-0.03/longCount 51/C
- `EUR-ANL45-TRADE-IDEAS-WEAK`（2026-08-25）family=analyst45 VECTOR trade-idea residual x v_rev/wedge：{"best": {"alpha": "78jwwme2", "fitness": 0.31, "sharpe": 0.71}, "reason": "Wave61 seven analyst45 trade-idea slows (probability/jensen/exposure/age/count/rel-return/PnL) x v_rev/wedge. Max S0.71. Differentiated but far from cheap gate. Do not Mode A. Do not reuse leftover anl45 price/FX/time fields.", "rule": "Do not reuse analyst45 trade-idea vec_avg residuals as 0.30 slow legs with v_rev/fallin
- `EUR-analyst45-RET-WEAK`（2026-09-04）family=analyst45 return/benchmark fields：{"best_2y": 0.43, "best_alpha": "RRVn5GV1", "best_fitness": 0.16, "best_sharpe": 0.38, "dataset": "analyst45", "evidence": "wave117 9 条全灭：收益类字段（ad_rel_ret/jensensalpha/tot_ret）全负，ad_ret_per S0.38 弱；conversion_rate_summary 无数据；benchmark_currency_code 弱信号；if_else/trade_when 条件逻辑无效", "id": "EUR-analyst45-RET-WEAK", "reason": "analyst45 收益/基准类字段在 EUR TOP2500 无正向预测力；收益类字段全负或弱，条件逻辑无效", "region": "EUR", 
- `EUR-NONMODEL-TOWER-CEILING`（2026-09-11）family=non_model_tower_sparse_event_sentiment_analyst：{"datasets": [{"dataset": "news54", "max_sharpe": 0.4, "reason": "mws54_factor semi-annual+单边恒正+稀疏", "tower": "news"}, {"dataset": "news_sentiment_nlp", "max_sharpe": 0.39, "reason": "情绪信号弱,净极性turnover1.24高超手", "tower": "other"}, {"dataset": "analyst45", "max_sharpe": 0.32, "reason": "分析师想法表现弱,zscore/delta turnover1.5+", "tower": "analyst"}], "evidence": "三塔回测全灭,S0 calibrate预警与实测完全一致(news0.50→0.40

