# USA analyst45 字段画像（2026-10-22）

> 数据集：`analyst45`（类别 ANALYST）· USA / TOP3000 / D1 · 平台实测 **181 字段**（DB catalog 记 61，已陈旧）· 全部 **VECTOR**。
> 语义：**贡献者交易想法（trade idea）流水**——每条想法带进场价、目标价、已实现/未实现收益、存续天数、信念概率与相对基准收益。
> 与 `analyst_factor_signals`（一致预期修正）**机制不同**：这里是「谁在买、买了多久、赚没赚」，不是「分析师把 EPS 预期改成多少」。
> 数据来源：`get_datafields(dataset_id='analyst45', filter_sharpe=False)` 全量拉取，`complete=True`。

## 1. 家族分类（按字段 id/描述关键词，自上而下）

| 家族 | 字段数 | 覆盖中位数 | aC=0 字段 | 代表字段 |
|---|---:|---:|---:|---|
| idea_performance | 41 | 19.62% | 16 | `anl45_bias_weighted_ret`, `anl45_ad_ret_per`, `foreign_exchange_return_value` |
| price_target | 24 | 24.96% | 9 | `anl45_prc`, `anl45_prc_change_today`, `anl45_avg_initial_prc` |
| positioning | 25 | 24.91% | 12 | `anl45_current_inv`, `anl45_initial_inv`, `anl45_ang_inv` |
| timing | 7 | 24.99% | 1 | `anl45_time`, `anl45_avg_dur`, `anl45_days_since_inception` |
| risk | 11 | 22.99% | 2 | `anl45_risk_free_rate`, `anl45_beta`, `anl45_treynor_ratio` |
| benchmark | 31 | 21.40% | 14 | `benchmark_currency_code`, `anl45_bm_fx_ret`, `anl45_index_period_start_prc` |
| conviction | 3 | 13.26% | 2 | `anl45_probability`, `success_likelihood_score_2`, `trade_idea_success_probability` |
| fx | 21 | 24.98% | 12 | `anl45_transaction_charge`, `investment_currency_code`, `security_trading_currency_3` |
| classification | 4 | 24.96% | 3 | `previous_field_value`, `previous_field_value_2`, `updated_field_value` |
| other | 14 | 19.88% | 7 | `anl45_new_value`, `anl45_old_value`, `anl45_idea_count` |

**判读**：`idea_performance` / `price_target` / `positioning` 三族是信号面；`timing` 是确定性时间趋势（只宜作条件，不宜作主信号）；`benchmark` / `fx` / `classification` 是上下文与标识（免 ATOM 计入的是 market/sector 等分组，不含这些，故不作主腿）。

## 2. 全字段表（家族内按 coverage 降序）

| 家族 | 字段 | 类型 | 覆盖 | userCount | alphaCount | 描述 |
|---|---|---|---:|---:|---:|---|
| idea_performance | `anl45_bias_weighted_ret` | VECTOR | 66.32% | 4 | 9 | Non-Functional |
| idea_performance | `anl45_ad_ret_per` | VECTOR | 55.30% | 3 | 3 | Average daily percent return over the idea’s lifetime |
| idea_performance | `foreign_exchange_return_value` | VECTOR | 54.63% | 0 | 0 | Return generated from variations in foreign exchange rates affecting the idea's PnL |
| idea_performance | `anl45_ret_today` | VECTOR | 54.48% | 1 | 1 | Increase in realised return since last market close |
| idea_performance | `anl45_real_ret` | VECTOR | 54.26% | 4 | 4 | Realized return from closed portions of the idea since inception |
| idea_performance | `anl45_tot_ret` | VECTOR | 54.19% | 1 | 4 | Sum of realised and unrealised returns |
| idea_performance | `anl45_unreal_ret` | VECTOR | 54.19% | 4 | 7 | Unrealized return on the open idea (mark-to-market) |
| idea_performance | `anl45_stock_ret_per` | VECTOR | 54.18% | 2 | 3 | Net total return from all ideas since the previous market close |
| idea_performance | `anl45_ad_rel_ret_per` | VECTOR | 54.09% | 6 | 6 | Average daily index relative return percentage |
| idea_performance | `anl45_ret_per_today` | VECTOR | 53.24% | 1 | 2 | Percentage return since last market close |
| idea_performance | `anl45_real_ret_today` | VECTOR | 52.25% | 4 | 4 | Increase in realized return since the previous market close |
| idea_performance | `anl45_rel_ret_per_today` | VECTOR | 52.01% | 1 | 2 | Relative return percentage today |
| idea_performance | `anl45_unreal_ret_today` | VECTOR | 51.97% | 2 | 3 | Increase in unrealised return since the last market close |
| idea_performance | `anl45_rel_ret_today` | VECTOR | 50.70% | 1 | 1 | Increase in realised return since last market close |
| idea_performance | `bias_adjusted_return_value` | VECTOR | 24.91% | 0 | 0 | Non functional field retained for compatibility not used in calculations |
| idea_performance | `adjusted_return_for_bias` | VECTOR | 24.76% | 11 | 20 | The return on the idea adjusted for contributor or model bias. |
| idea_performance | `average_daily_return_percent` | VECTOR | 20.03% | 1 | 1 | Average daily percent return over the lifetime of the idea |
| idea_performance | `mean_daily_return_percent` | VECTOR | 19.91% | 0 | 0 | The average daily percent return over the idea’s lifetime. |
| idea_performance | `return_percentage_today` | VECTOR | 19.88% | 1 | 1 | Percentage return since last market close |
| idea_performance | `total_return_today_value` | VECTOR | 19.63% | 1 | 1 | Increase in realised return since last market close |
| idea_performance | `realized_trade_return` | VECTOR | 19.62% | 1 | 3 | Realised return on the idea since inception or closure |
| idea_performance | `total_gain_today` | VECTOR | 19.62% | 0 | 0 | The total increase in return for the idea since the last market close. |
| idea_performance | `realized_idea_gain` | VECTOR | 19.59% | 0 | 0 | The realized return on the idea from closed positions. |
| idea_performance | `aggregate_trade_return` | VECTOR | 19.58% | 1 | 1 | Sum of realised and unrealised returns |
| idea_performance | `security_return_percent` | VECTOR | 19.58% | 1 | 1 | Net total return from all ideas since the previous market close |
| idea_performance | `unrealized_trade_return` | VECTOR | 19.58% | 0 | 0 | The unrealised return on an open idea |
| idea_performance | `aggregate_idea_return` | VECTOR | 19.47% | 1 | 7 | The sum of realized and unrealized returns for the trade idea. |
| idea_performance | `net_stock_return_percent` | VECTOR | 19.47% | 0 | 0 | The net total return from all ideas since the previous market close. |
| idea_performance | `open_position_return` | VECTOR | 19.47% | 0 | 0 | The return on open (unrealized) positions in the trade idea. |
| idea_performance | `average_daily_relative_return_percent` | VECTOR | 19.46% | 0 | 0 | Average daily index relative return percentage |
| idea_performance | `realized_return_today_value` | VECTOR | 19.46% | 1 | 1 | Increase in realized return since the last market close |
| idea_performance | `relative_return_percent_today` | VECTOR | 19.43% | 1 | 1 | Relative return percentage for today |
| idea_performance | `unrealized_return_today_value` | VECTOR | 19.39% | 0 | 0 | Increase in unrealised return since the last market close |
| idea_performance | `gain_percent_today` | VECTOR | 19.22% | 0 | 0 | The percentage return for the idea since the last market close. |
| idea_performance | `realized_gain_today` | VECTOR | 18.90% | 1 | 1 | The increase in realized return since the last market close. |
| idea_performance | `relative_return_today_value` | VECTOR | 18.90% | 0 | 0 | Increase in realised return since the last market close |
| idea_performance | `daily_unrealized_gain` | VECTOR | 18.72% | 0 | 0 | The increase in unrealized return since the last market close. |
| idea_performance | `mean_daily_relative_return_percent` | VECTOR | 18.56% | 0 | 0 | The average daily index-relative return percentage over the idea’s lifetime. |
| idea_performance | `relative_gain_percent_today` | VECTOR | 17.91% | 1 | 1 | The relative return percentage for the idea for today. |
| idea_performance | `relative_gain_today` | VECTOR | 17.34% | 0 | 0 | The change in relative return for the idea since the last market close. |
| idea_performance | `foreign_exchange_gain` | VECTOR | 0.00% | 0 | 0 | The return generated from foreign exchange rate changes. |
| price_target | `anl45_prc` | VECTOR | 66.61% | 2 | 2 | The price given to the investment change |
| price_target | `anl45_prc_change_today` | VECTOR | 54.48% | 4 | 4 | Change in stock price since previous day close |
| price_target | `anl45_avg_initial_prc` | VECTOR | 54.27% | 0 | 0 | Average share price weighted by volume of each share purchase |
| price_target | `anl45_avg_initial_prc_wfee` | VECTOR | 54.27% | 7 | 9 | The avg initial price adjusted to include fee payment when fees are applied |
| price_target | `anl45_period_start_prc` | VECTOR | 54.27% | 2 | 2 | Close price on day before start of selected period |
| price_target | `anl45_period_end_prc` | VECTOR | 54.19% | 2 | 2 | Close price on day at end of selected period |
| price_target | `anl45_prc_change_per_today` | VECTOR | 53.24% | 1 | 1 | Percent change in stock price since previous close of day price |
| price_target | `anl45_prev_close_prc` | VECTOR | 52.14% | 2 | 3 | Last available close price for the stock |
| price_target | `anl45_target_prc` | VECTOR | 51.60% | 6 | 8 | Author’s stated likely exit price for the idea |
| price_target | `anl45_closed_prc` | VECTOR | 50.96% | 0 | 0 | Price at which the idea was closed |
| price_target | `anl45_latest_prc` | VECTOR | 48.45% | 4 | 9 | The current price of the stock in the idea |
| price_target | `security_trade_price` | VECTOR | 24.96% | 0 | 0 | Price used for the investment change at the event time |
| price_target | `average_initial_trade_price` | VECTOR | 19.62% | 0 | 0 | Average share price weighted by volume of each share purchase |
| price_target | `period_starting_security_price` | VECTOR | 19.62% | 1 | 1 | Close price on day before start of selected period |
| price_target | `entry_price_inclusive_fees` | VECTOR | 19.59% | 0 | 0 | The average initial price adjusted for transaction fees. |
| price_target | `volume_weighted_entry_price` | VECTOR | 19.59% | 0 | 0 | The average share price weighted by purchase volume at entry. |
| price_target | `period_ending_security_price` | VECTOR | 19.58% | 0 | 0 | Close price on day at end of selected period |
| price_target | `period_closing_price` | VECTOR | 19.47% | 1 | 1 | The closing price at the end of the selected period. |
| price_target | `previous_closing_security_price` | VECTOR | 19.42% | 0 | 0 | Last available closing price for the stock |
| price_target | `final_closing_price` | VECTOR | 16.62% | 1 | 1 | The price at which the trade idea was closed or exited. |
| price_target | `most_recent_security_price` | VECTOR | 15.56% | 0 | 0 | The current price of the stock in the idea |
| price_target | `most_recent_market_price` | VECTOR | 15.27% | 1 | 2 | The most recent price of the security in the trade idea. |
| price_target | `expected_exit_price_2` | VECTOR | 5.89% | 1 | 1 | The projected price at which the contributor expects to close the position. |
| price_target | `expected_exit_price_3` | VECTOR | 5.89% | 1 | 1 | Author’s likely exit price for the idea |
| positioning | `anl45_current_inv` | VECTOR | 66.41% | 2 | 2 | Current investment amount, including increases and partial closures |
| positioning | `anl45_initial_inv` | VECTOR | 66.41% | 3 | 3 | Initial investment amount allocated to the idea |
| positioning | `anl45_ang_inv` | VECTOR | 66.40% | 5 | 7 | Time-weighted average investment |
| positioning | `anl45_net_market_exposure` | VECTOR | 66.39% | 23 | 34 | Difference in fractional total value between long and short ideas (net market exposure) |
| positioning | `anl45_tot_ret_per` | VECTOR | 55.30% | 0 | 0 | Total return as a percentage of average investment |
| positioning | `anl45_real_value` | VECTOR | 54.26% | 1 | 1 | Monetary value of the realized (closed) portion of the idea |
| positioning | `anl45_unreal_value` | VECTOR | 54.19% | 5 | 11 | Unrealised value of an open idea |
| positioning | `theoretical_zero_risk_rate` | VECTOR | 24.97% | 1 | 1 | The theoretical rate of return of a risk-free investment. |
| positioning | `event_associated_price` | VECTOR | 24.93% | 1 | 1 | The price associated with an investment change or event. |
| positioning | `average_investment_amount` | VECTOR | 24.91% | 0 | 0 | Time-weighted average investment |
| positioning | `current_investment_amount` | VECTOR | 24.91% | 0 | 0 | Current investment amount of the idea, including all increases and partial closures |
| positioning | `present_invested_amount` | VECTOR | 24.91% | 0 | 0 | The current total amount allocated to the trade idea. |
| positioning | `starting_invested_amount` | VECTOR | 24.91% | 1 | 1 | The initial amount allocated to the trade idea. |
| positioning | `starting_investment_amount` | VECTOR | 24.91% | 0 | 0 | Initial investment amount for the idea |
| positioning | `mean_invested_amount` | VECTOR | 24.90% | 1 | 1 | The time-weighted average amount allocated to the trade idea. |
| positioning | `net_market_exposure_value` | VECTOR | 24.90% | 0 | 0 | Difference in fractional total value between long and short ideas |
| positioning | `net_exposure_to_market` | VECTOR | 24.89% | 0 | 0 | The net exposure to market movements, calculated as long minus short positions. |
| positioning | `index_return_percentage` | VECTOR | 21.42% | 0 | 0 | Return percentage had the investment been made in the comparative index |
| positioning | `total_return_percentage` | VECTOR | 20.03% | 0 | 0 | Total return as a percentage of average investment |
| positioning | `aggregate_return_percent` | VECTOR | 19.91% | 3 | 3 | The total return as a percentage of average investment. |
| positioning | `realized_position_value_2` | VECTOR | 19.62% | 0 | 0 | Value of the realised (closed) portions of the idea |
| positioning | `realized_position_value` | VECTOR | 19.59% | 0 | 0 | The value of closed (realized) parts of the trade idea. |
| positioning | `unrealized_position_value` | VECTOR | 19.58% | 1 | 1 | Unrealised value of an open idea |
| positioning | `open_position_value` | VECTOR | 19.47% | 4 | 8 | The value of unrealized (open) parts of the trade idea. |
| positioning | `security_relative_return_percent` | VECTOR | 18.95% | 0 | 0 | Average daily return percentage had all investments been in the relative index |
| timing | `anl45_time` | VECTOR | 66.70% | 1 | 1 | Approximate time horizon for the idea |
| timing | `anl45_avg_dur` | VECTOR | 66.41% | 3 | 4 | Average age of the idea limited to the selected period |
| timing | `anl45_days_since_inception` | VECTOR | 66.41% | 2 | 2 | Number of trading days since the idea was submitted |
| timing | `days_since_idea_start` | VECTOR | 24.99% | 2 | 6 | Number of trading days since the idea was submitted |
| timing | `trading_days_since_submission` | VECTOR | 24.98% | 2 | 3 | The number of trading days since the idea was submitted. |
| timing | `average_idea_duration` | VECTOR | 24.91% | 0 | 0 | Average age of the idea (limited to the period selected) |
| timing | `mean_idea_age_period` | VECTOR | 24.91% | 1 | 1 | The average age of the idea within the selected period. |
| risk | `anl45_risk_free_rate` | VECTOR | 66.53% | 1 | 1 | The unrealised return on an open idea |
| risk | `anl45_beta` | VECTOR | 61.20% | 7 | 9 | A measure of the volatility or systematic risk of a security compared to the market, updat |
| risk | `anl45_treynor_ratio` | VECTOR | 60.99% | 3 | 3 | A ratio that measures returns earned in excess of that which could have been earned on a r |
| risk | `anl45_jensensalpha` | VECTOR | 60.25% | 3 | 8 | Risk-adjusted performance measure representing return over market |
| risk | `riskless_investment_rate` | VECTOR | 24.99% | 2 | 3 | The unrealised return on an open idea |
| risk | `systematic_risk_beta` | VECTOR | 22.99% | 0 | 0 | A measure of the security’s systematic risk versus the market, updated monthly based on th |
| risk | `systematic_risk_measure` | VECTOR | 22.98% | 1 | 1 | A measure of the idea's volatility relative to the overall market. |
| risk | `treynor_performance_ratio` | VECTOR | 22.92% | 1 | 1 | Risk-adjusted return ratio measuring excess return per unit of systematic risk relative to |
| risk | `risk_adjusted_return_per_beta` | VECTOR | 22.78% | 0 | 0 | A risk-adjusted return measure relative to the risk-free rate and beta. |
| risk | `jensens_alpha_value` | VECTOR | 22.12% | 2 | 2 | Risk-adjusted performance measure representing return above the market (Jensen’s Alpha) |
| risk | `risk_adjusted_excess_return` | VECTOR | 22.12% | 1 | 2 | The performance of the idea above market return, adjusted for risk. |
| benchmark | `benchmark_currency_code` | VECTOR | 66.70% | 1 | 1 | Currency of the benchmark |
| benchmark | `anl45_bm_fx_ret` | VECTOR | 59.86% | 1 | 1 | FX return made by the benchmark due to currency movements |
| benchmark | `anl45_index_period_start_prc` | VECTOR | 59.25% | 2 | 2 | Benchmark or index start price for the selected performance period |
| benchmark | `anl45_index_period_end_prc` | VECTOR | 58.70% | 4 | 4 | Benchmark or index end price for the selected performance period |
| benchmark | `anl45_index_ret_per` | VECTOR | 58.68% | 0 | 0 | Return percentage had the investment been made in the selected index |
| benchmark | `anl45_bm_ret` | VECTOR | 57.93% | 1 | 1 | Return of the benchmark index |
| benchmark | `anl45_bm_ret_wo_fx` | VECTOR | 57.93% | 3 | 8 | Benchmark’s return excluding foreign exchange effects (raw benchmark return) |
| benchmark | `anl45_rel_index_ret_per` | VECTOR | 54.09% | 1 | 1 | Difference in return percentage between the idea and the comparative index |
| benchmark | `anl45_stock_ret_per_relative` | VECTOR | 52.87% | 1 | 1 | Average daily return percentage had the investment been made in the relative benchmark ind |
| benchmark | `anl45_rel_index_ret` | VECTOR | 52.86% | 1 | 1 | Difference in return percentage between the idea and the comparative index |
| benchmark | `benchmark_currency_abbreviation` | VECTOR | 24.99% | 0 | 0 | Currency of the benchmark |
| benchmark | `reference_index_currency` | VECTOR | 24.98% | 0 | 0 | The currency in which the benchmark index is denominated. |
| benchmark | `benchmark_fx_return_value` | VECTOR | 21.91% | 0 | 0 | Foreign exchange return attributable to the benchmark (movement due to currency difference |
| benchmark | `reference_index_fx_gain` | VECTOR | 21.90% | 0 | 0 | Return generated from foreign exchange movements in the benchmark. |
| benchmark | `index_period_starting_price` | VECTOR | 21.69% | 1 | 1 | Benchmark/Index start price based on the performance period you chose |
| benchmark | `benchmark_period_opening_price` | VECTOR | 21.40% | 2 | 2 | The index price at the start of the selected period. |
| benchmark | `index_period_ending_price` | VECTOR | 21.31% | 1 | 1 | Benchmark/Index end price based on the performance period you chose |
| benchmark | `benchmark_return_ex_fx` | VECTOR | 21.05% | 0 | 0 | Basically tracking the raw returns of the benchmark |
| benchmark | `benchmark_total_return` | VECTOR | 21.05% | 1 | 1 | Return of the benchmark over the measurement period |
| benchmark | `benchmark_period_closing_price` | VECTOR | 20.84% | 0 | 0 | The index price at the end of the selected period. |
| benchmark | `benchmark_index_return_percent` | VECTOR | 20.44% | 0 | 0 | The return percentage of the index over the selected period. |
| benchmark | `reference_index_return` | VECTOR | 20.04% | 1 | 1 | The return of the benchmark index over the selected period. |
| benchmark | `reference_index_return_ex_fx` | VECTOR | 20.04% | 2 | 2 | Benchmark return excluding foreign exchange effects. |
| benchmark | `relative_index_return_percentage` | VECTOR | 19.46% | 0 | 0 | Percentage difference in return between the idea and the comparative index |
| benchmark | `relative_index_return_value` | VECTOR | 18.95% | 0 | 0 | Difference in return percentage between investing in the idea and the chosen benchmark ind |
| benchmark | `relative_index_return_percent` | VECTOR | 18.56% | 1 | 1 | The difference in return percentage between the idea and the benchmark index. |
| benchmark | `relative_stock_return_percent` | VECTOR | 18.04% | 0 | 0 | The average daily return percentage if all investments were in the index. |
| benchmark | `relative_index_gain` | VECTOR | 18.02% | 0 | 0 | The return if all investments had been made in the benchmark index. |
| benchmark | `anl45_bm_exchange_rate` | VECTOR | 0.42% | 0 | 0 | Exchange Rate by which the Benchmark will be measured |
| benchmark | `benchmark_conversion_rate` | VECTOR | 0.03% | 0 | 0 | Exchange rate used to measure/convert the benchmark |
| benchmark | `reference_fx_rate` | VECTOR | 0.03% | 1 | 1 | The exchange rate used to convert benchmark returns to the reporting currency. |
| conviction | `anl45_probability` | VECTOR | 13.47% | 0 | 0 | Tag giving a quantative measure of conviction |
| conviction | `success_likelihood_score_2` | VECTOR | 13.26% | 1 | 1 | A quantitative measure of the likelihood of the idea’s success. |
| conviction | `trade_idea_success_probability` | VECTOR | 13.26% | 0 | 0 | Quantitative measure of conviction for the idea |
| fx | `anl45_transaction_charge` | VECTOR | 66.70% | 2 | 2 | Transaction fee charged for the idea (in calculation currency) |
| fx | `investment_currency_code` | VECTOR | 66.70% | 0 | 0 | Currency of the investment |
| fx | `security_trading_currency_3` | VECTOR | 66.70% | 1 | 1 | Currency in which the security is traded |
| fx | `fx_return_percentage` | VECTOR | 54.63% | 0 | 0 | Return from FX movements expressed as a percentage of the investment |
| fx | `summary_conversion_rate` | VECTOR | 54.63% | 0 | 0 | Exchange rate between investment and performance currencies |
| fx | `anl45_tot_ret_wo_fx` | VECTOR | 54.18% | 1 | 1 | Total return excluding any foreign exchange effects |
| fx | `investment_currency_abbreviation` | VECTOR | 24.99% | 0 | 0 | Currency of the idea investment |
| fx | `security_currency_code_8` | VECTOR | 24.99% | 1 | 1 | Currency in which the security is traded |
| fx | `trade_transaction_fee` | VECTOR | 24.99% | 0 | 0 | Transaction fee charged for the idea in the calculation currency |
| fx | `allocated_funds_currency` | VECTOR | 24.98% | 3 | 6 | The currency used for the investment in the trade idea. |
| fx | `security_trading_currency_2` | VECTOR | 24.98% | 1 | 1 | The currency in which the security is traded. |
| fx | `total_return_excluding_fx` | VECTOR | 19.58% | 0 | 0 | Return excluding any foreign exchange effects |
| fx | `aggregate_return_ex_fx` | VECTOR | 19.47% | 2 | 2 | The total return for the idea excluding foreign exchange effects. |
| fx | `anl45_inv_exchange_rate` | VECTOR | 0.43% | 1 | 1 | Exchange rate between stock and investment currencies / FX Rate on the period End date |
| fx | `investment_conversion_rate` | VECTOR | 0.03% | 0 | 0 | Exchange rate between stock and investment currencies, i.e., FX rate on the period end dat |
| fx | `investment_fx_conversion_rate` | VECTOR | 0.03% | 0 | 0 | The exchange rate between stock and investment currencies. |
| fx | `conversion_rate_summary` | VECTOR | 0.00% | 0 | 0 | Exchange rate between investment and performance currencies. |
| fx | `currency_gain_percentage` | VECTOR | 0.00% | 0 | 0 | The percentage return generated from currency movements. |
| fx | `currency_gain_value` | VECTOR | 0.00% | 0 | 0 | The return generated from currency movements. |
| fx | `fx_gain_percentage` | VECTOR | 0.00% | 1 | 3 | The percentage return generated from foreign exchange rate movements. |
| fx | `investment_performance_fx_rate` | VECTOR | 0.00% | 0 | 0 | The exchange rate between investment and performance currencies. |
| classification | `previous_field_value` | VECTOR | 24.96% | 0 | 0 | The value before a change in stop loss, target price, or capital. |
| classification | `previous_field_value_2` | VECTOR | 24.96% | 0 | 0 | Previous value of a stop-loss percent, target price, or capital change |
| classification | `updated_field_value` | VECTOR | 24.96% | 2 | 2 | The new value after a change in stop loss, target price, or capital. |
| classification | `updated_field_value_2` | VECTOR | 24.96% | 0 | 0 | New value of a stop-loss percent, target price, or capital change |
| other | `anl45_new_value` | VECTOR | 66.68% | 6 | 6 | New value set for the stop-loss percent, target price, or capital allocation |
| other | `anl45_old_value` | VECTOR | 66.68% | 2 | 2 | Previous value of the stop-loss percent, target price, or capital allocation before the la |
| other | `anl45_idea_count` | VECTOR | 66.41% | 0 | 0 | Number of ideas in a group, useful when grouping ideas |
| other | `trade_execution_fee` | VECTOR | 24.98% | 4 | 4 | The transaction fee charged for executing the trade idea. |
| other | `grouped_idea_total` | VECTOR | 24.91% | 0 | 0 | The number of ideas in a group or view. |
| other | `trade_idea_count` | VECTOR | 24.91% | 1 | 1 | Number of ideas in the group/context, useful for grouping |
| other | `price_change_percent_today` | VECTOR | 19.88% | 0 | 0 | Percentage change in stock price since previous day's close |
| other | `absolute_price_change_today` | VECTOR | 19.63% | 12 | 13 | Change in stock price since previous day close |
| other | `average_initial_price_with_fee` | VECTOR | 19.62% | 0 | 0 | The avg initial price adjusted to include fee payment when fees are applied |
| other | `daily_price_delta` | VECTOR | 19.62% | 0 | 0 | The change in the security's price since the previous market close. |
| other | `period_opening_price` | VECTOR | 19.59% | 0 | 0 | The closing price before the start of the selected period. |
| other | `daily_price_change_percent` | VECTOR | 19.22% | 1 | 1 | The percentage change in price since the previous day's close. |
| other | `previous_market_close_price` | VECTOR | 18.85% | 0 | 0 | The last available closing price for the security. |
| other | `trade_idea_closed_price` | VECTOR | 16.62% | 3 | 3 | The price at which the idea was closed |

## 3. 可用性判据（S1 结论）

| 检查 | 结论 |
|---|---|
| 类型 | 全 VECTOR ⇒ 必须先 `vec_avg` 聚合再进标量算子（类别卡硬规则） |
| 覆盖率 | 主信号族 0.48–0.67；< 0.40 的字段一律 `ts_backfill` 或弃用 |
| 拥挤度 | 字段 aC 中位数 0–9，最高 `anl45_net_market_exposure` 34 ⇒ **极低拥挤**，prod 先验优于 analyst_factor_signals（aC 297） |
| 更新频率 | 想法 PnL 类日更；`anl45_beta` 月更（描述明示 last ~20 months） |
| 时间趋势 | `anl45_days_since_inception` 单调递增 ⇒ 只能做条件/分组，不能当信号 |
| 单位 | 价格族与收益族混用时用比值（`target/latest`），比值再 z-score |

## 4. 批次 45A（8 臂探针，2026-10-22）

统一壳（T5，proven）：`quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(vec_avg(F), 504), std=4), 756), hump=0.01), sector))`；设置 USA/TOP3000/D1/REVERSION_AND_MOMENTUM/decay 20/trunc 0.08/VERIFY/nan ON。

| 臂 | 字段 | 机制假设 |
|---|---|---|
| A1 | `anl45_unreal_ret` | 想法的浮动盈亏异常度 ⇒ 聪明钱动量 |
| A2 | `anl45_tot_ret` | 想法总收益（浮盈+已实现）⇒ 完整业绩 |
| A3 | `anl45_rel_index_ret` | 想法相对基准的超额 ⇒ 剔除 beta 的选股能力 |
| A4 | `anl45_jensensalpha` | 风险调整后超额 ⇒ 高质量想法 |
| A5 | `anl45_target_prc / anl45_latest_prc` | 隐含上行空间（目标价/现价） |
| A6 | `anl45_real_ret` | 已实现收益 ⇒ 兑现过的正确性 |
| A7 | `anl45_net_market_exposure` | 想法组合净敞口 ⇒ 方向性拥挤 |
| A8 | `anl45_beta` | 想法标的的系统风险 ⇒ 低 beta 偏好 |

## 5. 批次 45B / 45C 与判死（2026-10-22 收盘）

**45B（8 臂，流量 / 差分壳）**：在 45A 的 T5 壳上换 `ts_av_diff` / `ts_delta` / 条件门控。
最高 S **1.06**；唯一有独立信息的臂是 **22 日指数相对收益的反号**（`-ts_zscore(ts_delta(anl45_rel_index_ret,22),252)`，
S ≈ +0.97）⇒ 本集的「聪明钱」含量低于其自身近期跑输，均值回复才是主效应。

**45C（9 臂，三类机制）**

| 臂 | alpha | 机制 | S | F | 2Y | SUB(下限) | TO | 归因 |
|---|---|---|---:|---:|---:|---:|---:|---|
| C1 | `pwvarxd6` | `vec_stddev` 裸分散度 | 0.30 | 0.08 | 0.08 | −0.16(0.13) | 4.35% | VECTOR 是「单人多想法」，不是市场分歧 |
| C2 | `9qEl18xe` | 分散度条件反转 | 0.74 | 0.41 | 0.10 | 0.45 PASS | 4.99% | 反向也弱 |
| C3 | `gJWaOXam` | C2 + 强壳 | **0.96** | 0.53 | 1.14 | 0.28(0.42) | 5.10% | 用全期强度换近期强度 |
| D1 | `wp9ox3o2` | 22d 新鲜度门控 | 0.74 | 0.29 | 0.53 | −0.08 | 4.15% | 稀疏 |
| D2 | `d5KaVY9X` | 66d 新鲜度门控 | 0.91 | 0.43 | **1.71** | 0.12(0.39) | 4.57% | 少交易假 2Y |
| E1 | `3qj0r1G6` | 贡献者技能加权 | 0.84 | 0.35 | 0.73 | 0.16(0.36) | 4.11% | 技能系数平 |
| E2 | `kqJarv88` | 贡献者技能差分 | 0.85 | 0.35 | 0.46 | −0.01 | 4.06% | 同上 |
| F1 | `mLYaRdKE` | 多头集中度条件 | 0.83 | 0.34 | 0.27 | 0.27(0.36) | 3.44% | 无增益 |
| G2 | `vROAMZZz` | 反号 × 长窗 | 0.60 | 0.20 | **1.99** | −0.11(0.26) | 3.55% | 样本稀疏伪强 |

**判死**：三批 25 臂、三种机制（水平 / 差分 / 条件），S 天花板 **1.10**，距 USA 闸 1.58 缺口 0.48 且无机制解释的余量。
**另加规则约束**：analyst 塔本季已提交 6 颗（≥3 ⇒ 点亮），按用户裁定本塔数据集停测 ⇒ 本集不再投入。
完整裁决与外部取证见交付日志附录 AG。

## 6. 存档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-analyst45-field-profile-20261022.md`
- 交付日志：`_usa-atom-delivery-log-20261020.md` 附录 AG
- 数据集总览：`_usa-fundamental-dataset-scan-20261019.md` §6（本集此前未展开）
