# ml_factor_proj — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `ml_factor_proj` |
| 名称 | — |
| 类别 | OTHER |
| 数据字段数(平台) | 0 |
| 覆盖率 | 1 |
| 平台已有 alpha | 293 |
| valueScore | 5 |
| 金字塔倍率 | 1.5 |
| 数据类型 | UNKNOWN |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

（平台目录未返回描述）

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **333** |
| 类型分布 | MATRIX×333 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 333 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 333 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 135 | 1.00 | change_1y_cashflow_to_price、change_1y_eps_growth、change_1y_eps_to_price |
| 其他 | 98 | 1.00 | change_1y_accounts_receivable_to_sales、change_1y_inventory_to_sales、change_5y_relative_book_to_market |
| 价量与波动 | 68 | 1.00 | change_12m_alpha、change_1m_active_return、change_20d_volume_to_price_volatility |
| 修正与预期 | 21 | 1.00 | change_3m_revision_fy2_eps、change_6m_rating_revision、change_analyst_consensus_rating |
| 宏观与行业 | 7 | 1.00 | change_3y_compound_sales_growth、change_five_year_sales_growth、change_industry_relative_book_to_market |
| 持仓与资金流 | 2 | 1.00 | change_cash_conversion_cycle_2、change_operating_cash_burn_rate |
| 风险与质量 | 1 | 1.00 | change_market_beta |
| 搜索与替代数据 | 1 | 1.00 | change_rd_expense_to_sales |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `change_12m_alpha` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in 12-month alpha, measuring the difference in excess return over a benchmark between two periods. |
| 2 | `change_1m_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in one-month active return, reflecting the difference in price performance over one month. |
| 3 | `change_1y_accounts_receivable_to_sales` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in accounts receivable as a percentage of sales compared to four quarters ago. |
| 4 | `change_1y_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in one-year growth of cash flow per share relative to price. |
| 5 | `change_1y_eps_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in one-year growth rate of trailing twelve-month earnings per share. |
| 6 | `change_1y_eps_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in one-year growth of earnings per share relative to price. |
| 7 | `change_1y_inventory_to_sales` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in inventory as a percentage of sales compared to four quarters ago. |
| 8 | `change_1y_operating_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in one-year growth of operating cash flow per share relative to price. |
| 9 | `change_1y_quarterly_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the most recent quarterly total assets per share compared to four quarters ago. |
| 10 | `change_20d_volume_to_price_volatility` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the coefficient of variation of last 20 days closing prices divided by coefficient of variation of trading vol |
| 11 | `change_24m_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in 24-month active return, measuring the difference in price performance over two years. |
| 12 | `change_24m_value_at_risk` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in 24-month value at risk, measuring shifts in the minimum monthly price return over a 20-month period. |
| 13 | `change_2m_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the percent change in stock price from month t-2 to t, relative to a benchmark. |
| 14 | `change_30_75w_price_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of 30-week to 75-week moving average prices, indicating long-term price momentum shifts. |
| 15 | `change_36m_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the 36-month active return, measuring long-term performance relative to a benchmark. |
| 16 | `change_3m_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the 3-month active return, measuring recent performance relative to a benchmark. |
| 17 | `change_3m_revision_fy2_eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 18 | `change_3y_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the difference between trailing twelve-month cash flow per share and 12-quarters ago, divided by month-end tra |
| 19 | `change_3y_compound_sales_growth` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change in the geometric growth rate of trailing twelve-month sales per share over last 12 quarters. |
| 20 | `change_3y_eps_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in three-year growth rate of trailing twelve-month earnings per share. |
| 21 | `change_3y_eps_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in trailing twelve-month EPS before extra items minus EPS 12-quarters ago, deflated by average total assets per s |
| 22 | `change_3y_eps_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in three-year growth of earnings per share relative to price. |
| 23 | `change_3y_fcf_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in trailing twelve-month free cash flow per share compared to twelve quarters ago. |
| 24 | `change_3y_fcf_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in trailing twelve-month free cash flow minus 12-quarters ago, divided by average total assets. |
| 25 | `change_3y_operating_cashflow_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in trailing twelve-month operating cash flow per share compared to twelve quarters ago. |
| 26 | `change_3y_operating_cashflow_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the trailing twelve-month operating cash flow minus OCF 12-quarters ago, deflated by average total assets. |
| 27 | `change_3y_operating_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the three-year growth of operating cash flow per share relative to price. |
| 28 | `change_3y_price_adj_fcf_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the 3-year growth of free cash flow per share adjusted for price, indicating long-term cash flow trends. |
| 29 | `change_4y_avg_trading_volume` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the average trading volume over a four-year period, reflecting shifts in liquidity. |
| 30 | `change_50_200d_price_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the moving average of last 50 days prices divided by moving average of last 200 days prices. |
| 31 | `change_52w_high_price_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of current price to the highest price over the past 52 weeks. |
| 32 | `change_5y_dividend_growth_rate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in five-year dividend growth rate, indicating shifts in dividend policy over time. |
| 33 | `change_5y_relative_book_to_market` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the 5-year relative book-to-market ratio, indicating shifts in long-term valuation relative to peers. |
| 34 | `change_5y_relative_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the current cash flow-to-price ratio minus 5-year average, scaled by standard deviation. |
| 35 | `change_5y_relative_earnings_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in five-year relative earnings-to-price ratio, comparing current to historical values. |
| 36 | `change_5y_relative_fcf_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in five-year relative free cash flow-to-price ratio, comparing current to historical values. |
| 37 | `change_5y_relative_forward_earnings_yield` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in five-year relative forward earnings yield, comparing current to historical values. |
| 38 | `change_5y_relative_operating_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the five-year relative operating cash flow-to-price ratio, comparing current to historical values. |
| 39 | `change_5y_relative_sales_to_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the five-year relative sales-to-price ratio, comparing current value to historical average. |
| 40 | `change_60m_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the percent change in stock price from month t-61 to t-1, relative to a benchmark. |
| 41 | `change_60m_alpha` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in 60-month alpha, measuring the difference in excess return over a benchmark over five years. |
| 42 | `change_60m_regression_error` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the standard error of the slope of the 60-month CAPM regression. |
| 43 | `change_6m_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the percent change in stock price from month t-7 to t-1, relative to a benchmark. |
| 44 | `change_6m_alpha_18m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in a stock's 18-month alpha from regression of monthly returns against a benchmark over the last 6 months. |
| 45 | `change_6m_rating_revision` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in six-month average of analyst rating revisions, indicating shifts in consensus sentiment. |
| 46 | `change_9m_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in 9-month active return, reflecting the difference in price performance over nine months. |
| 47 | `change_abnormal_capital_investment_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in abnormal capital investment, measuring the difference in recent capital investment intensity compared to histo |
| 48 | `change_acquisition_valuation_multiple` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of invested capital to trailing twelve-month EBITDA, reflecting acquisition valuation shifts. |
| 49 | `change_analyst_consensus_rating` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the average analyst recommendation tracked by standardized rating systems. |
| 50 | `change_analyst_coverage_count` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the number of analysts providing earnings estimates for the current fiscal year. |
| 51 | `change_asset_composition_ratio_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of total current assets to total assets, indicating shifts in asset structure. |
| 52 | `change_asset_quality_index` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the asset quality index, measuring year-over-year change in the ratio of current assets plus PP&E to total ass |
| 53 | `change_asset_turnover_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the percent growth of the asset turnover ratio compared to the previous year. |
| 54 | `change_asset_turnover_ratio_3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event-aligned change in asset turnover |
| 55 | `change_attention_span_ratio_3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of quarterly operating assets minus operating liabilities, deflated by lagged total assets. |
| 56 | `change_average_collection_period_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the average number of days it takes a company to collect payments from customers, reflecting trends in receiva |
| 57 | `change_avg_payable_period` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the average payable period, indicating shifts in the time taken to pay suppliers. |
| 58 | `change_basic_defensive_interval` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in basic defensive interval, indicating shifts in the number of days a company can cover expenses with cash and r |
| 59 | `change_beta_times_sigma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the product of adjusted 60-month Beta and 60-month Sigma (standard deviation of monthly returns). |
| 60 | `change_book_leverage_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of total assets to book equity, indicating shifts in financial leverage. |
| 61 | `change_book_to_market_ratio_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of book value per share divided by month-end trading price. |
| 62 | `change_capex_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of capital expenditures to total assets, indicating shifts in investment intensity. |
| 63 | `change_capex_to_price_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month capital expenditures per share to price. |
| 64 | `change_capex_to_sales_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of capital expenditures to sales, indicating shifts in investment intensity relative to revenue. |
| 65 | `change_capital_acquisition_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the capital acquisition ratio, measuring the ability to finance capital spending without new debt or equity. |
| 66 | `change_capital_gearing_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of long-term debt divided by total assets minus current liability. |
| 67 | `change_cash_conversion_cycle_2` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Change in the cash conversion cycle, measuring shifts in the time between cash outflows for purchases and inflows from s |
| 68 | `change_cash_flow_debt_coverage` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of cash flow from operations less dividends to current interest-bearing debt, measuring debt coverag |
| 69 | `change_cash_to_current_liabilities_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of cash and equivalents to current liabilities, indicating shifts in liquidity. |
| 70 | `change_cash_to_enterprise_value_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of total cash and equivalents to market value of equity plus long-term debt. |
| 71 | `change_cash_to_liabilities_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | change in cash ratio (cash and equivalents/current liabilities) |
| 72 | `change_cash_to_price_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of most recent cash and equivalents per share divided by month-end trading price. |
| 73 | `change_cash_to_sales_ratio_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the ratio of average cash and equivalents in trailing twelve months divided by trailing twelve-month sales. |
| 74 | `change_cashflow_growth_rate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in trailing twelve-month cash flow per share compared to four quarters ago. |
| 75 | `change_cashflow_investment_to_assets_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of cash flow from investment to total assets, indicating shifts in investment activity. |
| 76 | `change_cashflow_leverage` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow leverage, calculated as total liabilities divided by trailing twelve-month operating cash flow. |
| 77 | `change_cashflow_return_on_invested_capital_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow return on invested capital, measuring shifts in profitability from capital employed. |
| 78 | `change_cogs_vs_inventory_level_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the absolute difference between yearly percent change in cost of goods sold and inventory level. |
| 79 | `change_current_liabilities_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of current liabilities per share to closing price. |
| 80 | `change_current_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event-aligned change in the current ratio (current assets divided by current liabilities) |
| 81 | `change_cv_prior_90_day_prices` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the coefficient of variation of prior 90-day closing prices, measuring shifts in price volatility. |
| 82 | `change_debt_to_cashflow_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of long-term debt to cash flow, indicating shifts in debt service ability. |
| 83 | `change_depreciation_vs_capex_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the absolute difference between yearly percent change in depreciation and capital expenditure. |
| 84 | `change_dispersion_fy2_eps_estimates` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the coefficient of variation of FY2 earnings per share estimates, measuring forecast uncertainty. |
| 85 | `change_dividend_coverage_ratio_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in dividend coverage ratio, indicating shifts in the ability to pay dividends from earnings. |
| 86 | `change_dividend_yield_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in trailing twelve-month dividend yield, indicating shifts in income generation. |
| 87 | `change_dividends_to_cashflow_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of dividends paid to cash flow, indicating shifts in payout sustainability. |
| 88 | `change_ebitda_to_enterprise_value` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event-aligned change in EBITDA to enterprise value ratio |
| 89 | `change_ebitda_to_price_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month EBITDA to price. |
| 90 | `change_ebo_value_to_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the Edwards-Bell-Ohlson value-to-price ratio, indicating shifts in intrinsic value relative to price. |
| 91 | `change_eighteen_month_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in 18-month active return, representing the difference in stock price performance over an 18-month period compare |
| 92 | `change_eps_from_tax_rate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share attributed to changes in effective tax rate over four quarters. |
| 93 | `change_eps_growth_rate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in trailing twelve-month earnings per share before extra items compared to four quarters ago. |
| 94 | `change_eps_vs_operating_cashflow` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the absolute difference between yearly percent change in operating cash flow per share and diluted EPS. |
| 95 | `change_equity_turnover_ratio_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month sales divided by average trailing twelve-month book equity. |
| 96 | `change_fama_french_momentum` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in Fama-French momentum, measuring the difference in price return over a specified period. |
| 97 | `change_fcf_yield_forward_roe_product` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the product of trailing free cash flow yield and forward return on equity, reflecting profitability and cash g |
| 98 | `change_fifteen_thirtysix_week_price_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of the 15-week to 36-week moving average of stock prices. |
| 99 | `change_financial_leverage_ratio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in financial leverage, measuring shifts in the ratio of pretax income and interest expense to pretax income. |
| 100 | `change_five_year_relative_dividend_yield` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the five-year relative trailing twelve-month dividend yield compared to its historical average. |
| 101 | `change_five_year_relative_ebitda_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the five-year relative trailing twelve-month EBITDA-to-price ratio compared to its historical average. |
| 102 | `change_five_year_sales_growth` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change in the five-year sales growth rate, measuring the difference in sales per share over five years. |
| 103 | `change_fixed_assets_turnover` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month sales to average total fixed assets. |
| 104 | `change_flow_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the flow ratio, calculated as the difference between current assets and cash divided by the difference between |
| 105 | `change_forward_2y_eps_growth` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the most recent FY2 consensus earnings forecast minus FY1 forecast divided by month-end price. |
| 106 | `change_forward_earnings_yield` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the leading 12-month mean earnings yield, calculated as next four quarters' mean earnings estimates divided by |
| 107 | `change_forward_eps_to_enterprise_value` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of forward 12-month earnings per share to enterprise value, indicating shifts in forward-looking val |
| 108 | `change_forward_estimated_earnings_yield` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the most recent next 4-quarter median earnings estimates divided by month-end price. |
| 109 | `change_forward_fcf_to_price` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the ratio of next four-quarter mean earnings estimates plus depreciation minus capex divided by month-end pric |
| 110 | `change_forward_return_on_equity_2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the forward-looking return on equity, based on analyst earnings forecasts. |
| 111 | `change_free_cashflow_return_on_invested_capital_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in free cash flow return on invested capital, measuring trends in capital efficiency. |
| 112 | `change_free_cashflow_to_equity` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month free cash flow to equity. |
| 113 | `change_free_cashflow_to_sales_ratio_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month free cash flow to sales, indicating shifts in a company's cash generation e |
| 114 | `change_fy1_eps_estimate_dispersion` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the standard deviation of FY1 earnings estimates divided by mean, measuring forecast uncertainty. |
| 115 | `change_industry_adjusted_12m_price_strength` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in industry-adjusted 12-month relative price strength, comparing stock performance to industry peers. |
| 116 | `change_industry_adjusted_quarterly_roe` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the industry-adjusted quarterly return on equity, calculated as lagged quarterly ROE minus industry average. |
| 117 | `change_industry_relative_book_to_market` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change in book-to-market ratio relative to the industry, indicating shifts in valuation compared to peers. |
| 118 | `change_industry_relative_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the cash flow-to-price ratio relative to the industry average. |
| 119 | `change_industry_relative_dividend_yield` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the dividend yield relative to the industry average, adjusted for industry standard deviation. |
| 120 | `change_industry_relative_doubtful_receivables` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in industry-adjusted doubtful account receivables, measuring shifts in asset quality relative to peers. |
| 121 | `change_industry_relative_ebitda_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the stock's EBITDA-to-price ratio less industry average, deflated by industry standard deviation. |
| 122 | `change_industry_relative_eps_to_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the stock's EPS-to-price ratio less industry average, deflated by industry standard deviation. |
| 123 | `change_industry_relative_fcf_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the stock's free cash flow-to-price ratio less industry average, deflated by industry standard deviation. |
| 124 | `change_industry_relative_five_day_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the five-day return of a stock relative to its industry average. |
| 125 | `change_industry_relative_forward_ep` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the stock's next 4-quarter earnings estimates-to-price ratio less industry average, deflated by standard devia |
| 126 | `change_industry_relative_four_week_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the four-week return of a stock relative to its industry average. |
| 127 | `change_industry_relative_oper_cashflow_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating cash flow to total assets ratio relative to the industry average. |
| 128 | `change_industry_relative_oper_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the operating cash flow-to-price ratio relative to the industry average. |
| 129 | `change_industry_relative_sales_to_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the sales-to-price ratio relative to the industry average. |
| 130 | `change_interest_coverage_ratio_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in interest coverage ratio, indicating the difference in a company's ability to meet interest payments over time. |
| 131 | `change_inventory_to_assets_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of inventory to total assets, indicating shifts in asset composition. |
| 132 | `change_inventory_turnover_ratio_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month cost of goods sold divided by average inventory. |
| 133 | `change_inverse_peg_ratio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the inverse of the PEG ratio, indicating shifts in valuation relative to growth. |
| 134 | `change_lagged_inverse_peg_ratio` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change in the lagged inverse PEG ratio, calculated as trailing twelve-month EPS times change in sales growth rate divide |
| 135 | `change_liquidity_coefficient` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the liquidity coefficient, measuring the relationship between trading turnover and price returns. |
| 136 | `change_log_closing_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the natural logarithm of the closing price, indicating shifts in price level on a log scale. |
| 137 | `change_log_market_capitalization` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the natural logarithm of market capitalization, reflecting shifts in company size. |
| 138 | `change_log_sales` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the natural logarithm of trailing twelve-month sales, reflecting shifts in company revenue size. |
| 139 | `change_log_total_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the natural logarithm of most recent quarterly total assets. |
| 140 | `change_log_trading_volume_to_market_cap` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the natural logarithm of average monthly trading volume divided by average monthly market capitalization. |
| 141 | `change_long_term_debt_to_equity_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of long-term debt to equity, indicating shifts in financial leverage. |
| 142 | `change_long_term_growth_estimate` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the long-term growth rate estimate, reflecting shifts in analyst expectations. |
| 143 | `change_market_beta` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | change in market beta |
| 144 | `change_market_cap_per_analyst` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in market capitalization per analyst, reflecting shifts in analyst coverage relative to company size. |
| 145 | `change_market_leverage_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of month-end total market value plus most recent quarterly book debt divided by market value. |
| 146 | `change_nav_to_price_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of net asset value per share to month-end closing price. |
| 147 | `change_net_cash_to_equity` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of net cash (cash and equivalents less debt) to market value of equity. |
| 148 | `change_net_debt_ratio_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event-aligned change in net debt |
| 149 | `change_net_fixed_assets_to_longterm_debt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of net fixed assets to total long-term debt. |
| 150 | `change_net_income_per_employee_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in net income per employee, measuring trends in workforce profitability. |
| 151 | `change_net_net_assets_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of current assets per share minus total liabilities per share divided by month-end price. |
| 152 | `change_net_number_fy1_eps_revisions` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the net number of analyst forecast revisions for fiscal year 1. |
| 153 | `change_net_operating_asset_turnover_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in net operating asset turnover, indicating changes in efficiency of asset utilization. |
| 154 | `change_net_operating_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net operating assets, measuring the year-over-year difference as a percentage of total assets. |
| 155 | `change_net_profit_margin_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net profit margin, measuring the difference in profitability as a percentage of sales between two periods. |
| 156 | `change_nopat_profit_margin` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net operating profit after tax margin over time. |
| 157 | `change_one_year_cashflow_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the percent growth of trailing twelve-month cash flow per share compared to one year ago. |
| 158 | `change_one_year_free_cashflow_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the percent growth of trailing twelve-month free cash flow per share compared to one year ago. |
| 159 | `change_one_year_free_cashflow_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the one-year difference in assets-adjusted trailing twelve-month free cash flow. |
| 160 | `change_one_year_free_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the one-year difference in price-adjusted trailing twelve-month free cash flow per share. |
| 161 | `change_one_year_price_momentum_indicator` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the one-year price momentum indicator, based on correlation of price over the last 260 days. |
| 162 | `change_operating_cash_burn_rate` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Change in the rate at which a company uses cash from operations and investments relative to cash holdings. |
| 163 | `change_operating_cashflow_assets_adj` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in assets-adjusted trailing twelve-month operating cash flow compared to the previous year. |
| 164 | `change_operating_cashflow_growth_rate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in trailing twelve-month operating cash flow per share compared to four quarters ago. |
| 165 | `change_operating_cashflow_margin_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in the operating cash flow margin, measuring shifts in cash profitability relative to sales. |
| 166 | `change_operating_cashflow_ratio_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of quarterly cash flow from operations to current liabilities. |
| 167 | `change_operating_cashflow_return_on_invested_capital` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month operating cash flow divided by average invested capital. |
| 168 | `change_operating_cashflow_to_assets_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month net cash flow from operations divided by average total assets. |
| 169 | `change_operating_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month operating cash flow per share to price. |
| 170 | `change_operating_income_vs_long_term_debt_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the difference between operating income growth and long-term debt growth, reflecting leverage impact on profit |
| 171 | `change_operating_leverage` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in operating leverage, calculated as the percent change in operating income divided by percent change in sales fr |
| 172 | `change_operating_liability_leverage_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating liability leverage, measuring shifts in the use of non-debt financing. |
| 173 | `change_operating_liability_leverage_ratio_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in the ratio of operating liabilities to operating assets, indicating shifts in non-debt financing |
| 174 | `change_operating_profit_margin_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in operating profit margin, indicating trends in operational efficiency and profitability. |
| 175 | `change_operating_profit_margin_21` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating profit margin, calculated as the difference in quarterly operating income to sales ratio. |
| 176 | `change_percent_shares_outstanding` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the percentage of shares outstanding, reflecting share issuance or buybacks. |
| 177 | `change_predicted_dividend_yield` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in predicted dividend yield, reflecting shifts in expected payout relative to price. |
| 178 | `change_pretax_return_on_operating_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in pretax return on net operating assets, measuring shifts in operational profitability. |
| 179 | `change_price_above_260d_low` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of current closing price to the lowest daily low price in the last 260 trading days. |
| 180 | `change_price_to_total_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trading price to most recent total assets per share. |
| 181 | `change_quarterly_sales_growth` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change in the growth rate of quarterly sales per share compared to four quarters ago. |
| 182 | `change_quick_ratio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | change in quick ratio |
| 183 | `change_rational_decay_alpha` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the market-adjusted excess return using a decay function for weighting historical returns. |
| 184 | `change_rd_expense_to_sales` | MATRIX | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Change in the ratio of average research and development expenses divided by total sales over trailing twelve months. |
| 185 | `change_real_earnings_surprise` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the real earnings surprise, calculated as the difference between actual EPS and consensus forecast scaled by p |
| 186 | `change_reciprocal_dividend_yield_adjusted_peg` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the reciprocal of the dividend yield-adjusted PEG ratio, indicating shifts in valuation adjusted for growth an |
| 187 | `change_reinvestment_rate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of EPS before extra items less dividends per share divided by average book equity per share. |
| 188 | `change_residual_return_variance` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the variance of monthly residual returns over the last 24 months. |
| 189 | `change_retained_earnings_to_assets_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in the ratio of retained earnings to total assets, reflecting shifts in earnings reinvestment. |
| 190 | `change_return_on_assets_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in return on assets, measuring the difference in profitability relative to total assets over time. |
| 191 | `change_return_on_equity_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event-aligned change in Return on Equity (ROE) |
| 192 | `change_return_on_invested_capital_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in return on invested capital, measuring the difference in profitability from capital employed over time. |
| 193 | `change_revenue_per_employee_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in revenue generated per employee, reflecting trends in workforce productivity. |
| 194 | `change_risk_adjusted_peg_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the risk-adjusted price/earnings-to-growth ratio, indicating shifts in valuation relative to growth and risk. |
| 195 | `change_sales_vs_eps_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Absolute difference between the yearly percent change in sales per share and diluted earnings per share. |
| 196 | `change_sales_vs_gross_margin_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the difference between sales growth and gross profit margin, reflecting profitability trends. |
| 197 | `change_sales_vs_receivables` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the difference between yearly percent change in sales and accounts receivable, indicating shifts in revenue qu |
| 198 | `change_second_preceding_six_month_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the return from the second preceding six-month period, measuring price performance from 12 to 7 months ago. |
| 199 | `change_sga_expense_vs_sales_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the difference between yearly change in quarterly SG&A expenses and yearly change in quarterly sales. |
| 200 | `change_sga_to_sales_ratio_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the ratio of selling, general, and administrative expenses to sales. |
| 201 | `change_six_month_alpha_36m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the six-month nominal change in 36-month alpha from regression of monthly returns against a benchmark. |
| 202 | `change_six_month_average_trading_volume` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the six-month moving average of trading volume, indicating shifts in liquidity. |
| 203 | `change_six_month_eps_revision` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the average of the last six months' EPS revisions for the current fiscal year. |
| 204 | `change_six_month_long_term_growth_estimate` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the long-term growth rate estimate over the past six months. |
| 205 | `change_skewness_90_day_excess_returns` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the skewness of 90-day stock daily excess returns, indicating shifts in the asymmetry of return distribution. |
| 206 | `change_skewness_90_day_returns` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the skewness of 90-day stock daily returns, indicating shifts in the asymmetry of return distribution. |
| 207 | `change_slope_52w_price_trend` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the slope of the 52-week price trend line, indicating shifts in long-term price momentum. |
| 208 | `change_slope_66_week_price_trend` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the slope coefficient of the 66-week price trend line, indicating shifts in long-term price momentum. |
| 209 | `change_stddev_fy1_eps_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the standard deviation of FY1 earnings forecasts scaled by month-end price. |
| 210 | `change_stddev_fy2_eps_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the standard deviation of FY2 earnings forecasts scaled by price, indicating shifts in forecast dispersion. |
| 211 | `change_stock_illiquidity` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the stock illiquidity measure, reflecting shifts in trading volume relative to price movements. |
| 212 | `change_stock_return_volatility` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the standard deviation of monthly returns, indicating shifts in stock return volatility. |
| 213 | `change_street_revision_confidence` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in street revision confidence, calculated as the sum of 3-month change in highest and lowest earnings forecasts f |
| 214 | `change_street_revision_magnitude` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the magnitude of analyst earnings forecast revisions over three months. |
| 215 | `change_sustainable_growth_rate` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change in the maximum growth rate a firm can sustain without increasing leverage. |
| 216 | `change_thirty_nine_week_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in 39-week return, measuring the difference in stock price over a 39-week period. |
| 217 | `change_three_month_revision_fy1_eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in the three-month revision of current fiscal year earnings per share estimates. |
| 218 | `change_three_year_cashflow_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the percent growth of trailing twelve-month cash flow per share compared to three years ago. |
| 219 | `change_three_year_cashflow_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the three-year difference in assets-adjusted trailing twelve-month cash flow. |
| 220 | `change_time_weighted_earnings_yield` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the time-weighted earnings yield, which combines reported and forecasted earnings relative to price. |
| 221 | `change_tobins_q_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Tobin's Q, measuring the difference in market value to asset replacement cost over time. |
| 222 | `change_total_coverage_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in total coverage ratio, measuring shifts in the ability to cover interest and principal payments from cash flow. |
| 223 | `change_total_sales_growth_rate` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change in the yearly growth rate of total sales over the trailing twelve months. |
| 224 | `change_trading_turnover_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the trading turnover ratio, calculated as monthly trading volume divided by shares outstanding. |
| 225 | `change_trading_volume_trend` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the trend of trading volume over a specified period, indicating shifts in market activity. |
| 226 | `change_trailing_fcf_to_price_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in trailing twelve-month free cash flow to price ratio, reflecting shifts in cash flow valuation. |
| 227 | `change_ttm_accounting_accruals` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the difference between trailing twelve-month net income and operating cash flow scaled by beginning total asse |
| 228 | `change_ttm_cashflow_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month cash flows per share divided by month-end trading price. |
| 229 | `change_ttm_eps_after_items_to_price` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in trailing twelve-month earnings per share after extraordinary items divided by price. |
| 230 | `change_ttm_eps_before_items_to_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month EPS before extraordinary items to price. |
| 231 | `change_ttm_fcf_to_enterprise_value` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month free cash flow divided by month-end enterprise value. |
| 232 | `change_ttm_growth_flow_to_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the sum of trailing twelve-month growth flow value per share divided by month-end trading price. |
| 233 | `change_ttm_pretax_income_to_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in trailing twelve-month pretax income per share divided by price. |
| 234 | `change_ttm_sales_to_enterprise_value` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing twelve-month sales divided by enterprise value, indicating shifts in valuation. |
| 235 | `change_ttm_sales_to_price_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of trailing twelve-month sales per share to price. |
| 236 | `change_twelve_month_active_return` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in 12-month active return, representing the difference in stock price performance over a 12-month period compared |
| 237 | `change_twenty_six_week_relative_strength` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Event-aligned change in the 26-week Relative Strength Index |
| 238 | `change_unexpected_accounts_payable` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in unexpected accounts payable, measuring the difference between actual and expected payables as a percentage of |
| 239 | `change_unexpected_accounts_receivable` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the difference between current accounts receivable and expected level, scaled by total assets. |
| 240 | `change_unexpected_depreciation` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in unexpected depreciation, calculated as the difference between actual and expected depreciation scaled by total |
| 241 | `change_unexpected_inventory_level` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in unexpected inventory level, measuring the difference between actual and expected inventory as a percentage of |
| 242 | `change_visibility_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the ratio of recent daily trading volume to average daily volume over the previous 50 days. |
| 243 | `change_working_capital_accruals_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in working capital accruals, measuring shifts in non-cash current asset and liability adjustments. |
| 244 | `change_working_capital_to_assets_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of working capital to total assets, indicating shifts in liquidity position. |
| 245 | `change_working_capital_to_inventory_ratio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the ratio of most recent working capital to inventory. |
| 246 | `change_working_capital_to_sales_ratio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in the ratio of working capital to trailing twelve-month sales. |
| 247 | `change_yearly_current_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Year-over-year change in the current ratio, reflecting shifts in short-term liquidity. |
| 248 | `change_yearly_gross_profit_margin_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the yearly gross profit margin, calculated as the difference between the most recent and prior year's margin. |
| 249 | `change_yearly_leverage` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in leverage, calculated as the difference in total liabilities as a percentage of assets compared |
| 250 | `change_yearly_net_profit_margin` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in net profit margin, indicating shifts in profitability. |
| 251 | `change_yearly_return_on_assets_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on assets, indicating shifts in profitability relative to assets. |
| 252 | `change_yoy_accruals_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in year-over-year accruals to assets, measuring the difference in operating cash flow and income before extra ite |
| 253 | `change_yoy_receivables_to_current_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the percent of accounts receivable to current assets ratio from same quarter one year ago. |
| 254 | `log_variance_global_feature_0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 0th global model feature, typically used to assess feature volatility. |
| 255 | `log_variance_global_feature_1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 1st global feature, typically a model-derived or latent variable. |
| 256 | `log_variance_global_feature_10` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 10th global feature, representing dispersion in the metric. |
| 257 | `log_variance_global_feature_11` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 11th global feature, typically a model-derived or latent variable. |
| 258 | `log_variance_global_feature_12` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 12th global feature, typically a model-derived or latent variable. |
| 259 | `log_variance_global_feature_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 13th global model feature, typically used to assess feature volatility. |
| 260 | `log_variance_global_feature_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 14th global model feature, typically used to assess feature volatility. |
| 261 | `log_variance_global_feature_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 15th global model feature, typically used to assess feature volatility. |
| 262 | `log_variance_global_feature_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 16th global model feature, typically used to assess feature volatility. |
| 263 | `log_variance_global_feature_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 17th global model feature, typically used to assess feature volatility. |
| 264 | `log_variance_global_feature_18` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 18th global feature, representing variability in the metric. |
| 265 | `log_variance_global_feature_19` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 19th global feature, representing variability in the metric. |
| 266 | `log_variance_global_feature_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 2nd global feature, typically a model-derived or latent variable. |
| 267 | `log_variance_global_feature_20` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 20th global latent feature, typically from a model's latent space. |
| 268 | `log_variance_global_feature_21` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 21st global feature, typically a model-derived or latent variable. |
| 269 | `log_variance_global_feature_22` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 22nd global latent feature, typically from a model's latent space. |
| 270 | `log_variance_global_feature_23` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 23rd global feature, typically a model-derived or latent variable. |
| 271 | `log_variance_global_feature_24` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 24th global feature, representing dispersion in the metric. |
| 272 | `log_variance_global_feature_25` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 25th global feature, typically a model-derived or latent variable. |
| 273 | `log_variance_global_feature_26` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 26th global feature, typically a model-derived or latent variable. |
| 274 | `log_variance_global_feature_27` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 27th global feature, typically a model-derived or latent variable. |
| 275 | `log_variance_global_feature_28` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 28th global feature, representing variability in the metric. |
| 276 | `log_variance_global_feature_29` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 29th global feature, typically a model-derived or latent variable. |
| 277 | `log_variance_global_feature_3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 3rd global feature, representing variability in the metric. |
| 278 | `log_variance_global_feature_30` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 30th global feature, indicating variability in the metric. |
| 279 | `log_variance_global_feature_31` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 31st global feature, representing variability in the metric. |
| 280 | `log_variance_global_feature_32` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 32nd global model feature, typically used to assess feature volatility. |
| 281 | `log_variance_global_feature_33` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 33rd global feature, typically a model-derived or latent variable. |
| 282 | `log_variance_global_feature_34` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 34th global model feature, typically used to assess feature volatility. |
| 283 | `log_variance_global_feature_35` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 35th global feature, typically a model-derived or latent variable. |
| 284 | `log_variance_global_feature_36_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 36th global feature, measuring its volatility. |
| 285 | `log_variance_global_feature_37` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 37th global feature, typically a model-derived or latent variable. |
| 286 | `log_variance_global_feature_38` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 38th global latent feature, typically from a model's latent space. |
| 287 | `log_variance_global_feature_39` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 39th global feature, indicating variability in the metric. |
| 288 | `log_variance_global_feature_4` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 4th global feature, typically a model-derived or latent variable. |
| 289 | `log_variance_global_feature_5` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 5th global feature, representing variability in the metric. |
| 290 | `log_variance_global_feature_6` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 6th global feature, indicating variability in the metric. |
| 291 | `log_variance_global_feature_7` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance of the 7th global feature, typically a model-derived or latent variable. |
| 292 | `log_variance_global_feature_8` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 8th global feature, representing dispersion in the metric. |
| 293 | `log_variance_global_feature_9` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Logarithm of the variance for the 9th global latent feature, typically from a model's latent space. |
| 294 | `mean_global_feature_0` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 0th global feature, representing a summary statistic for a specific metric. |
| 295 | `mean_global_feature_1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 1st global feature, typically a model-derived or latent variable. |
| 296 | `mean_global_feature_10` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 10th global model feature, typically a latent or model-derived metric. |
| 297 | `mean_global_feature_11` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 11th global feature, summarizing a specific metric across the dataset. |
| 298 | `mean_global_feature_12` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 12th global feature, typically a model-derived or latent variable. |
| 299 | `mean_global_feature_13` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 13th global model feature, typically a latent or model-derived metric. |
| 300 | `mean_global_feature_14` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 14th global feature, typically a model-derived or latent variable. |
| 301 | `mean_global_feature_15` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 15th global model feature, typically a latent or model-derived metric. |
| 302 | `mean_global_feature_16` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 16th global feature, summarizing a specific metric across the dataset. |
| 303 | `mean_global_feature_17` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 17th global feature, typically a model-derived or latent variable. |
| 304 | `mean_global_feature_18` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 18th global feature, typically a model-derived or latent variable. |
| 305 | `mean_global_feature_19` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 19th global feature, representing an aggregated metric across the dataset. |
| 306 | `mean_global_feature_2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 2nd global latent feature, typically from a model's latent space. |
| 307 | `mean_global_feature_20` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 20th global feature, summarizing a specific metric across the dataset. |
| 308 | `mean_global_feature_21` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 21st global latent feature, typically from a model's latent space. |
| 309 | `mean_global_feature_22` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 22nd global feature, typically a model-derived or latent variable. |
| 310 | `mean_global_feature_23` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 23rd global feature, summarizing a specific metric across the dataset. |
| 311 | `mean_global_feature_24` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 24th global model feature, typically a latent or model-derived metric. |
| 312 | `mean_global_feature_25` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 25th global model feature, typically a latent or model-derived metric. |
| 313 | `mean_global_feature_26` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 26th global model feature, typically a latent or model-derived metric. |
| 314 | `mean_global_feature_27` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 27th global feature, typically a model-derived or latent variable. |
| 315 | `mean_global_feature_28` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 28th global model feature, typically a latent or model-derived metric. |
| 316 | `mean_global_feature_29` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 29th global feature, typically a model-derived or latent variable. |
| 317 | `mean_global_feature_3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 3rd global model feature, typically a latent or model-derived metric. |
| 318 | `mean_global_feature_30` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 30th global feature, typically a model-derived or latent variable. |
| 319 | `mean_global_feature_31` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 31st global model feature, typically a latent or model-derived metric. |
| 320 | `mean_global_feature_32` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 32nd global feature, typically a model-derived or latent variable. |
| 321 | `mean_global_feature_33` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 33rd global model feature, typically a latent or model-derived metric. |
| 322 | `mean_global_feature_34` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 34th global model feature, typically a latent or model-derived metric. |
| 323 | `mean_global_feature_35` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 35th global feature, typically a model-derived or latent variable. |
| 324 | `mean_global_feature_36` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 36th global latent feature, typically from a model's latent space. |
| 325 | `mean_global_feature_37` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 37th global model feature, typically a latent or model-derived metric. |
| 326 | `mean_global_feature_38` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 38th global feature, typically a model-derived or latent variable. |
| 327 | `mean_global_feature_39` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 39th global model feature, typically a latent or model-derived metric. |
| 328 | `mean_global_feature_4` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 4th global model feature, typically a latent or model-derived metric. |
| 329 | `mean_global_feature_5` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 5th global feature, summarizing a specific metric across the dataset. |
| 330 | `mean_global_feature_6` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 6th global feature, summarizing a specific metric across the dataset. |
| 331 | `mean_global_feature_7` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 7th global model feature, typically a latent or model-derived metric. |
| 332 | `mean_global_feature_8` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 8th global feature, summarizing a specific metric across the dataset. |
| 333 | `mean_global_feature_9` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Mean value of the 9th global model feature, typically a latent or model-derived metric. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-M354-VALUATION-YIELD-WEAK`（2026-08-25）family=model354 group valuation yield concepts：{"dataset": "model354", "id": "EUR-M354-VALUATION-YIELD-WEAK", "reason": "Wave66 56 exprs / 7 slots (FY2/NTM EY, FCF/CFO/div yield, sales/EV, FY1-LTM disagreement). Max S0.26 F0.07 (KP7bgexN). Many TVR 2-4%. No cheap-gate. Do not mix PV.", "rule": "Leave model354 standalone valuation densify. Next unused whitelist: ml_factor_proj low-competition non-return MATRIX concepts (not NEWS, not news54, no
- `EUR-MLFP-0ALPHA-OPS-WEAK`（2026-08-25）family=ml_factor_proj 0-alpha coverage/rating/CCC/capex：{"dataset": "ml_factor_proj", "id": "EUR-MLFP-0ALPHA-OPS-WEAK", "reason": "Wave67 56 exprs / 7 slots. Max S0.70 F0.23 (E5lwN5WJ abnormal capex ts_delta). Rating 0.47, CCC 0.41. No cheap-gate. Do not mix PV.", "rule": "Leave this ml_factor_proj ops/coverage family. Do not replay Wave9 EPS/price/FCF ranks. Next: predictive_starmine high-coverage fields unused in Wave21 ARM/RelVal/surprise ranks.", "
- `EUR-INSIDER-FEATS-WEAK`（2026-09-23T18:35:49）family=insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback）：{"family": "insider_feats 内部人买卖比率族（buy/sell ratio × tx count × lookback）", "reason": "wave238 10 探针全灭 best /sharpe/=0.47 < 0.5 → 达 fast_kill 判死线。此前 w232 多样性闸（flow 单 exposure）+ 字段名拼接幻觉 + 低覆盖无 backfill 三轮门禁墙已记录。OTHER 塔 4 候选全灭（acquisition_model/insider_feats/event_relation + ml_factor_proj 平台无字段）。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at

