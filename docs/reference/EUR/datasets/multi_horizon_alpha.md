# multi_horizon_alpha — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `multi_horizon_alpha` |
| 名称 | — |
| 类别 | MODEL |
| 数据字段数(平台) | 158 |
| 覆盖率 | 0.8257 |
| 平台已有 alpha | 309 |
| valueScore | 5 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

（平台目录未返回描述）

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **158** |
| 类型分布 | MATRIX×158 |
| 平均覆盖率 | **0.826** |
| 覆盖率区间 | 0.75 ~ 0.86 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 158 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 158 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 44 | 0.84 | long_term_estimate_revision_europe_rank、long_term_growth_analyst_europe_rank、long_term_momentum_analyst_europe_rank |
| 盈利与财务 | 40 | 0.84 | long_term_inverse_dividend_adjusted_peg、mid_term_inverse_dividend_adjusted_peg_2、short_term_inverse_dividend_adjusted_peg |
| 风险与质量 | 36 | 0.80 | long_term_balance_sheet_rank_europe、long_term_deep_value_europe_rank、long_term_enterprise_value_europe_rank |
| 价量与波动 | 34 | 0.81 | long_term_price_momentum_europe_rank、mid_term_price_momentum_europe_rank、short_term_price_momentum_europe_rank |
| 其他 | 4 | 0.86 | mid_term_enterprise_value_europe、short_term_enterprise_value_europe、short_term_management_efficiency_europe |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `long_term_balance_sheet_rank_europe` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-term ranking of companies based on balance sheet strength in the European universe. |
| 2 | `long_term_deep_value_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon composite rank for deep value model in European equities. |
| 3 | `long_term_enterprise_value_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for enterprise value-based valuation in European stocks. |
| 4 | `long_term_estimate_revision_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-horizon rank for analyst earnings estimate revisions in European stocks. |
| 5 | `long_term_financial_statement_rank_europe` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-term ranking of companies based on overall financial statement strength in the European universe. |
| 6 | `long_term_growth_analyst_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-horizon rank for growth-focused analyst model in European equities. |
| 7 | `long_term_income_statement_rank_europe` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-term ranking of companies based on income statement strength in the European universe. |
| 8 | `long_term_management_efficiency_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for management efficiency in European companies. |
| 9 | `long_term_management_leverage_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for management leverage in European companies. |
| 10 | `long_term_momentum_analyst_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-horizon composite rank for momentum-focused analyst model in European equities. |
| 11 | `long_term_price_momentum_europe_rank` | MATRIX | 0.863 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon rank for price momentum in European equities. |
| 12 | `long_term_value_analyst_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-horizon composite rank for value-focused analyst model in European equities. |
| 13 | `mid_term_balance_sheet_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for balance sheet strength in European companies. |
| 14 | `mid_term_deep_value_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon composite rank for deep value model in European equities. |
| 15 | `mid_term_enterprise_value_europe` | MATRIX | 0.863 | 其他 | 0 | — | — | — | UNTESTED | Medium-term enterprise value metric for companies in the European universe. |
| 16 | `mid_term_estimate_revision_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-horizon rank for analyst earnings estimate revisions in European stocks. |
| 17 | `mid_term_financial_statement_rank_europe` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-term ranking of companies based on overall financial statement strength in the European universe. |
| 18 | `mid_term_growth_analyst_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-horizon rank for growth-focused analyst model in European equities. |
| 19 | `mid_term_income_statement_rank_europe` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-term ranking of companies based on income statement strength in the European universe. |
| 20 | `mid_term_management_efficiency_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for management efficiency in European companies. |
| 21 | `mid_term_management_leverage_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for management leverage in European companies. |
| 22 | `mid_term_momentum_analyst_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-horizon composite rank for momentum-focused analyst model in European equities. |
| 23 | `mid_term_price_momentum_europe_rank` | MATRIX | 0.863 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-horizon rank for price momentum in European equities. |
| 24 | `mid_term_value_analyst_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-horizon composite rank for value-focused analyst model in European equities. |
| 25 | `short_term_balance_sheet_rank_europe` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-term ranking of companies based on balance sheet strength in the European universe. |
| 26 | `short_term_deep_value_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-horizon composite rank for deep value model in European equities. |
| 27 | `short_term_enterprise_value_europe` | MATRIX | 0.863 | 其他 | 0 | — | — | — | UNTESTED | Short-term enterprise value metric for companies in the European universe. |
| 28 | `short_term_estimate_revision_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-horizon rank for analyst earnings estimate revisions in European stocks. |
| 29 | `short_term_financial_statement_europe_rank` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-horizon rank for financial statement strength in European companies. |
| 30 | `short_term_growth_rank_europe` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-term ranking of companies based on growth metrics in the European universe. |
| 31 | `short_term_income_statement_rank_europe` | MATRIX | 0.863 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-term ranking of companies based on income statement strength in the European universe. |
| 32 | `short_term_management_efficiency_europe` | MATRIX | 0.863 | 其他 | 0 | — | — | — | UNTESTED | Short-term measure of management efficiency for companies in the European universe. |
| 33 | `short_term_management_leverage_europe` | MATRIX | 0.863 | 其他 | 0 | — | — | — | UNTESTED | Short-term measure of management leverage for companies in the European universe. |
| 34 | `short_term_momentum_analyst_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-horizon composite rank for momentum-focused analyst model in European equities. |
| 35 | `short_term_price_momentum_europe_rank` | MATRIX | 0.863 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon rank for price momentum in European equities. |
| 36 | `short_term_value_analyst_europe_rank` | MATRIX | 0.863 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-horizon composite rank for value-focused analyst model in European equities. |
| 37 | `long_term_change_in_price_adj_eps` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-term change in trailing 12-month EPS compared to four quarters ago, deflated by month-end trading price. |
| 38 | `long_term_inverse_dividend_adjusted_peg` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term reciprocal of the forward P/E ratio divided by total growth rate and adjusted for dividend yield. |
| 39 | `long_term_net_number_revisions_fy1` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term net number of analyst forecast revisions for FY1 within a month, weighted by total forecasts. |
| 40 | `long_term_stddev_fy1_eps_estimates_to_price` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term standard deviation of FY1 earnings forecasts scaled by month-end price. |
| 41 | `long_term_street_revision_magnitude` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term 3-month change in median earnings forecast for FY1 scaled by current mean estimate. |
| 42 | `long_term_three_month_revision_fy2_eps` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 43 | `long_term_three_month_revision_fy2_eps2` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 44 | `long_term_three_year_change_in_price_adj_eps` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-term difference between trailing 12-month EPS and 12-quarters ago, divided by month-end trading price. |
| 45 | `mid_term_change_in_price_adj_eps` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term change in trailing 12-month EPS compared to four quarters ago, deflated by month-end trading price. |
| 46 | `mid_term_inverse_dividend_adjusted_peg_2` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-term reciprocal of the forward P/E ratio divided by total growth rate and adjusted for dividend yield. |
| 47 | `mid_term_net_number_revisions_fy1` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-term net number of analyst forecast revisions for FY1 within a month, weighted by total forecasts. |
| 48 | `mid_term_stddev_fy1_eps_estimates_to_price` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-term standard deviation of FY1 earnings forecasts scaled by month-end price. |
| 49 | `mid_term_street_revision_magnitude` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-term 3-month change in median earnings forecast for FY1 scaled by current mean estimate. |
| 50 | `mid_term_three_month_revision_fy2_eps` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 51 | `mid_term_three_month_revision_fy2_eps2` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 52 | `mid_term_three_year_change_in_price_adj_eps` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term difference between trailing 12-month EPS and 12-quarters ago, divided by month-end trading price. |
| 53 | `short_term_change_in_price_adj_eps` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term change in trailing 12-month EPS compared to four quarters ago, deflated by month-end trading price. |
| 54 | `short_term_inverse_dividend_adjusted_peg` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term reciprocal of the forward P/E ratio divided by total growth rate and adjusted for dividend yield. |
| 55 | `short_term_net_number_revisions_fy1` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term net number of analyst forecast revisions for FY1 within a month, weighted by total forecasts. |
| 56 | `short_term_stddev_fy1_eps_estimates_to_price` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term standard deviation of FY1 earnings forecasts scaled by month-end price. |
| 57 | `short_term_street_revision_magnitude` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term 3-month change in median earnings forecast for FY1 scaled by current mean estimate. |
| 58 | `short_term_three_month_revision_fy2_eps` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 59 | `short_term_three_month_revision_fy2_eps2` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 60 | `short_term_three_year_change_in_price_adj_eps` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term difference between trailing 12-month EPS and 12-quarters ago, divided by month-end trading price. |
| 61 | `long_term_capital_acquisition_ratio_3` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term ratio of operating cash flow after dividends to total capital expenditures, measuring sustained ability to fun |
| 62 | `long_term_ebitda_to_enterprise_value_ratio` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Enterprise value divided by EBITDA (EV/EBITDA) ratio |
| 63 | `long_term_ebitda_to_enterprise_value_ratio_2` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of earnings before interest, taxes, depreciation, and amortization to enterprise value, measured over a long-term |
| 64 | `long_term_free_cash_flow_to_price_2` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term ratio of trailing 12-month free cash flow per share to month-end trading price. |
| 65 | `long_term_growth_flow_to_price_2` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-term sum of trailing 12-month growth flow value per share divided by month-end trading price. |
| 66 | `long_term_operating_liability_leverage_change` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-horizon change in operating liability leverage, indicating shifts in non-debt financing. |
| 67 | `long_term_operating_liability_leverage_change2` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-horizon change in operating liability leverage, indicating shifts in non-debt financing. |
| 68 | `long_term_price_to_total_assets_ratio` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-horizon ratio of price to total assets per share. |
| 69 | `long_term_return_on_equity` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-horizon return on equity, measuring profitability relative to shareholder equity. |
| 70 | `long_term_return_on_equity1` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term return on equity, calculated as net income divided by average common equity over a long-term period. |
| 71 | `long_term_sales_to_price` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-term ratio of trailing 12-month sales per share to month-end trading price. |
| 72 | `long_term_time_weighted_earnings_yield` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term time-weighted sum of reported EPS and next year's consensus estimate divided by price. |
| 73 | `long_term_time_weighted_earnings_yield1` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term time-weighted sum of reported EPS and next year's consensus estimate divided by price. |
| 74 | `long_term_time_weighted_earnings_yield_3` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-horizon time-weighted earnings yield, combining current and forward earnings estimates. |
| 75 | `long_term_trailing_free_cash_flow_to_price` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-horizon ratio of trailing twelve-month free cash flow to price. |
| 76 | `long_term_trailing_growth_flow_to_price` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon ratio of trailing twelve-month growth flow to price. |
| 77 | `mid_term_capital_acquisition_ratio` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-term ratio of operating cash flow less cash dividends to total expenditures over the trailing 12 months. |
| 78 | `mid_term_capital_acquisition_ratio2` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-term ratio of operating cash flow less cash dividends to total expenditures over the trailing 12 months. |
| 79 | `mid_term_ebitda_to_enterprise_value_3` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Enterprise value divided by EBITDA (EV/EBITDA) ratio |
| 80 | `mid_term_ebitda_to_enterprise_value_ratio` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of earnings before interest, taxes, depreciation, and amortization to enterprise value, measured over a medium-ter |
| 81 | `mid_term_growth_flow_to_price_ratio` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term ratio of trailing twelve-month growth flow per share to stock price, reflecting intermediate horizon value f |
| 82 | `mid_term_growth_flow_to_price_ratio_2` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term ratio of trailing twelve-month growth flow per share to stock price, reflecting intermediate horizon value f |
| 83 | `mid_term_operating_liability_leverage_change_4` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-term change in a company's operating liability leverage, measuring the difference in operating liability leverage |
| 84 | `mid_term_price_to_total_assets_ratio` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-horizon ratio of price to total assets per share. |
| 85 | `mid_term_return_on_equity` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-horizon return on equity, measuring profitability relative to shareholder equity. |
| 86 | `mid_term_return_on_equity1` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-term return on equity, calculated as net income divided by average common equity over a medium-term period. |
| 87 | `mid_term_sales_to_price` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term ratio of trailing 12-month sales per share to month-end trading price. |
| 88 | `mid_term_time_weighted_earnings_yield` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-horizon time-weighted earnings yield, combining current and forward earnings estimates. |
| 89 | `mid_term_time_weighted_earnings_yield1` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-term time-weighted sum of reported EPS and next year's consensus estimate divided by price. |
| 90 | `mid_term_time_weighted_earnings_yield_3` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-horizon time-weighted earnings yield, combining current and forward earnings estimates. |
| 91 | `mid_term_trailing_free_cash_flow_to_price` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-horizon ratio of trailing twelve-month free cash flow to price. |
| 92 | `mid_term_trailing_free_cash_flow_to_price1` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-term ratio of trailing twelve-month free cash flow per share to stock price, reflecting intermediate cash generat |
| 93 | `mid_term_trailing_growth_flow_to_price` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-horizon ratio of trailing twelve-month growth flow to price. |
| 94 | `short_term_capital_acquisition_ratio` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term ratio of operating cash flow less cash dividends to total expenditures over the trailing 12 months. |
| 95 | `short_term_capital_acquisition_ratio2` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term ratio of operating cash flow less cash dividends to total expenditures over the trailing 12 months. |
| 96 | `short_term_ebitda_to_enterprise_value_3` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Enterprise value divided by EBITDA (EV/EBITDA) ratio |
| 97 | `short_term_ebitda_to_enterprise_value_ratio` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of earnings before interest, taxes, depreciation, and amortization to enterprise value, measured over a short-term |
| 98 | `short_term_growth_flow_to_price_2` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term sum of trailing 12-month growth flow value per share divided by month-end trading price. |
| 99 | `short_term_operating_liability_leverage_change` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-horizon change in operating liability leverage, indicating shifts in non-debt financing. |
| 100 | `short_term_operating_liability_leverage_change3` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-horizon change in operating liability leverage, indicating shifts in non-debt financing. |
| 101 | `short_term_price_to_total_assets_ratio` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-horizon ratio of price to total assets per share. |
| 102 | `short_term_return_on_equity` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-horizon return on equity, measuring profitability relative to shareholder equity. |
| 103 | `short_term_return_on_equity1` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term return on equity, calculated as net income divided by average common equity over a short-term period. |
| 104 | `short_term_sales_to_price` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term ratio of trailing 12-month sales per share to month-end trading price. |
| 105 | `short_term_time_weighted_earnings_yield` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term time-weighted sum of reported EPS and next year's consensus estimate divided by price. |
| 106 | `short_term_time_weighted_earnings_yield1` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term time-weighted sum of reported EPS and next year's consensus estimate divided by price. |
| 107 | `short_term_time_weighted_earnings_yield_3` | MATRIX | 0.860 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-horizon time-weighted earnings yield, combining current and forward earnings estimates. |
| 108 | `short_term_trailing_free_cash_flow_to_price` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-horizon ratio of trailing twelve-month free cash flow to price. |
| 109 | `short_term_trailing_free_cash_flow_to_price1` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term ratio of trailing twelve-month free cash flow per share to stock price, indicating recent cash generation rel |
| 110 | `short_term_trailing_growth_flow_to_price` | MATRIX | 0.860 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon ratio of trailing twelve-month growth flow to price. |
| 111 | `long_term_change_in_net_operating_assets` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term year-over-year change of net operating assets to total assets. |
| 112 | `long_term_change_in_price_adj_eps_2` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-term change in trailing 12-month EPS compared to four quarters ago, deflated by month-end trading price. |
| 113 | `long_term_five_day_industry_relative_return` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-term difference between a stock's 5-day return and industry average, deflated by standard deviation. |
| 114 | `long_term_free_cash_flow_to_price_3` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term ratio of trailing 12-month free cash flow per share to month-end trading price. |
| 115 | `long_term_growth_flow_to_price_3` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-term sum of trailing 12-month growth flow value per share divided by month-end trading price. |
| 116 | `long_term_rational_decay_alpha` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-term market-adjusted excess return using a decay function for weighting past returns. |
| 117 | `long_term_three_month_revision_fy2_eps_2` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 118 | `long_term_time_weighted_earnings_yield_2` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term time-weighted sum of reported EPS and next year's consensus estimate divided by price. |
| 119 | `mid_term_change_in_net_operating_assets` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-term year-over-year change of net operating assets to total assets. |
| 120 | `mid_term_change_in_price_adj_eps_2` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term change in trailing 12-month EPS compared to four quarters ago, deflated by month-end trading price. |
| 121 | `mid_term_five_day_industry_relative_return` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term difference between a stock's 5-day return and industry average, deflated by standard deviation. |
| 122 | `mid_term_free_cash_flow_to_price_2` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Medium-term ratio of trailing 12-month free cash flow per share to month-end trading price. |
| 123 | `mid_term_growth_flow_to_price_2` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term sum of trailing 12-month growth flow value per share divided by month-end trading price. |
| 124 | `mid_term_rational_decay_alpha` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-term market-adjusted excess return using a decay function for weighting past returns. |
| 125 | `mid_term_three_month_revision_fy2_eps_2` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 126 | `mid_term_time_weighted_earnings_yield_2` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-term time-weighted sum of reported EPS and next year's consensus estimate divided by price. |
| 127 | `short_term_change_in_net_operating_assets` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term year-over-year change of net operating assets to total assets. |
| 128 | `short_term_change_in_price_adj_eps_2` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term change in trailing 12-month EPS compared to four quarters ago, deflated by month-end trading price. |
| 129 | `short_term_five_day_industry_relative_return` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term difference between a stock's 5-day return and industry average, deflated by standard deviation. |
| 130 | `short_term_free_cash_flow_to_price_2` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term ratio of trailing 12-month free cash flow per share to month-end trading price. |
| 131 | `short_term_growth_flow_to_price_3` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term sum of trailing 12-month growth flow value per share divided by month-end trading price. |
| 132 | `short_term_rational_decay_alpha` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term market-adjusted excess return using a decay function for weighting past returns. |
| 133 | `short_term_three_month_revision_fy2_eps_2` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term change in current FY2 mean earnings estimate less three months ago, deflated by month-end price. |
| 134 | `short_term_time_weighted_earnings_yield_2` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-term time-weighted sum of reported EPS and next year's consensus estimate divided by price. |
| 135 | `long_term_balance_sheet_strength_europe_rank` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for balance sheet strength in European companies. |
| 136 | `long_term_enterprise_value_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for enterprise value-based valuation in European stocks. |
| 137 | `long_term_financial_statement_strength_europe_rank` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for financial statement strength in European companies. |
| 138 | `long_term_income_statement_europe_rank` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for income statement strength in European companies. |
| 139 | `long_term_management_efficiency_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for management efficiency in European companies. |
| 140 | `long_term_management_leverage_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Long-horizon rank for management leverage in European companies. |
| 141 | `long_term_value_analyst_europe_composite` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-horizon composite score for value analyst model in European equities. |
| 142 | `long_term_value_momentum_europe_composite` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon composite score for value and momentum model in European equities. |
| 143 | `mid_term_balance_sheet_strength_europe_rank` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for balance sheet strength in European companies. |
| 144 | `mid_term_enterprise_value_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for enterprise value-based valuation in European stocks. |
| 145 | `mid_term_financial_statement_strength_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for financial statement strength in European companies. |
| 146 | `mid_term_income_statement_europe_rank` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for income statement strength in European companies. |
| 147 | `mid_term_management_efficiency_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for management efficiency in European companies. |
| 148 | `mid_term_management_leverage_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Medium-horizon rank for management leverage in European companies. |
| 149 | `mid_term_value_analyst_europe_composite` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Medium-horizon composite score for value analyst model in European equities. |
| 150 | `mid_term_value_momentum_europe_composite` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Medium-horizon composite score for value and momentum model in European equities. |
| 151 | `short_term_balance_sheet_strength_europe_rank` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-horizon rank for balance sheet strength in European companies. |
| 152 | `short_term_enterprise_value_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-horizon rank for enterprise value-based valuation in European stocks. |
| 153 | `short_term_financial_statement_strength_europe_rank` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-horizon rank for financial statement strength in European companies. |
| 154 | `short_term_income_statement_europe_rank` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-horizon rank for income statement strength in European companies. |
| 155 | `short_term_management_efficiency_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-horizon rank for management efficiency in European companies. |
| 156 | `short_term_management_leverage_rank_europe` | MATRIX | 0.746 | 风险与质量 | 0 | — | — | — | UNTESTED | Short-horizon rank for management leverage in European companies. |
| 157 | `short_term_value_analyst_europe_composite` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Short-horizon composite score for value analyst model in European equities. |
| 158 | `short_term_value_momentum_europe_composite` | MATRIX | 0.746 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon composite score for value and momentum model in European equities. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-FCF-PURE-INVERT-RESID-PROD`（2026-08-23）family=multi_horizon FCF invert industry residual dominant：{"dataset": "multi_horizon_alpha", "example_id": "88lOQrdm", "expr_pattern": "subtract(0, rank(subtract(long_term_free_cash_flow_to_price_2, group_mean(..., industry))))", "fitness": 1.06, "prod_corr": 0.9381, "reason": "IS S/F/2Y pass but prod 0.94 because pure FCF without heterogeneous dilution. Self vs Wj71Q12o 0.45 so not a clone of the submitted mix, but FCF-to-price dominant is crowded. Do n
- `EUR-FCF-MINORITY-VALUE-MIX-PROD`（2026-08-24）family=multi_horizon FCF invert residual mixed with to-price value：{"dataset": "multi_horizon_alpha", "example_id": "np7n8Mgd", "expr_pattern": "0.35-0.45 invert FCF industry residual + 0.55-0.65 ebitda/EV or deep_value", "fitness": 0.69, "prod_corr": 0.8693, "reason": "FCF as minority mixed with other to-price/value fields does not break prod 0.7. np7n8Mgd S1.17 F0.69 2Y2.03 prod 0.8693 vs pure FCF 88lOQrdm prod 0.9381. Three-way FCF 0.30 killed IS (max +S 0.49)
- `EUR-MH-ESTREV-RESID-INVERT-CROWD`（2026-08-24）family=multi_horizon long_term estimate_revision industry residual full invert：{"dataset": "multi_horizon_alpha", "example_id": "1YwozEAW", "expr_pattern": "rank(subtract(long_term_estimate_revision_europe_rank, group_mean(..., industry))) and its full invert as dominant", "fitness": -0.99, "mutual_vs_m238": -0.74, "prod_corr": 0.7748, "prod_min": -0.9477, "reason": "Has independent IS (/S/1.48, self vs Wj71Q12o 0.17) but the profitable invert aligns with model238 institutio
- `EUR-MH-MIDTERM-ESTREV-WEAK`（2026-08-24）family=multi_horizon mid_term estimate_revision：{"dataset": "multi_horizon_alpha", "example_id": "88lOpzjm", "expr_pattern": "mid_term_estimate_revision_europe_rank residual/gzscore/growth mix", "max_abs_sharpe": 0.52, "reason": "Horizon shift from long_term estrev residual (/S/1.48) to mid_term (alphaCount=0) failed. Best 88lOpzjm invert residual+growth S0.52 F0.19 2Y-0.03. Not independent of the long_term estrev residual prod wall because the
- `EUR-MH-ESTREV-INVERT-DILUTE-PROD`（2026-08-24）family=multi_horizon long_term estrev invert residual as minority：{"dataset": "multi_horizon_alpha", "example_id": "O07nGp8Y", "expr_pattern": "0.30-0.40 invert long_term estrev industry residual + growth/FS/mid_term", "fitness": 0.51, "prod_corr": 0.7057, "reason": "Salvage of EUR-MH-ESTREV-RESID-INVERT-CROWD failed. 0.30 invert x growth/FS killed IS (S~-0.08). 0.40 invert + 0.60 mid_term O07nGp8Y S1.08 F0.51 2Y0.88 prod=0.7057 (still >=0.7) though self vs Wj71
- `EUR-MH-CAPACQ-INVERT-RESID-PROD`（2026-08-24）family=multi_horizon capital_acquisition invert residual dominant：{"dataset": "multi_horizon_alpha", "example_id": "omqnqr3m", "expr_pattern": "subtract(0, rank(subtract(long_term_capital_acquisition_ratio_3, group_mean(..., industry))))", "settings": "EUR TOP2500 COUNTRY decay6", "sharpe": 1.28, "fitness": 0.69, "two_year_sharpe": 1.8, "sub_universe_sharpe": 0.59, "prod_corr": 0.8851, "wave": 38, "id": "EUR-MH-CAPACQ-INVERT-RESID-PROD", "family": "multi_horizon
- `EUR-MH-QUALITY-BS-EPS-WEAK`（2026-08-24）family=multi_horizon balance_sheet and price_adj_eps residual：{"dataset": "multi_horizon_alpha", "fields": ["long_term_balance_sheet_rank_europe", "long_term_change_in_price_adj_eps"], "max_abs_sharpe": 0.28, "wave": 38, "id": "EUR-MH-QUALITY-BS-EPS-WEAK", "family": "multi_horizon balance_sheet and price_adj_eps residual", "reason": "Unused quality legs BS residual max /S/0.06 and price_adj_eps residual max /S/0.28. Not independent signal. Capacq invert is a
- `EUR-MH-MGEFF-INVERT-GZ-PROD`（2026-08-24）family=multi_horizon invert management_efficiency gzscore：{"dataset": "multi_horizon_alpha", "example_id": "vRj5O7kG", "sharpe": 1, "fitness": 0.53, "prod_corr": 0.8178, "wave": 39, "reason": "invert long_term_management_efficiency_europe_rank industry gz S1.0 F0.53 TVR1.7% prod 0.8178. EUR/D1/MODEL wall. Do not Mode A. Do not use invert mgeff as dominant.", "rule": "Do not use invert management_efficiency gzscore as dominant.", "dead_at": "2026-08-24"}
- `EUR-MH-FY2-INVERT-CROWD`（2026-08-24）family=multi_horizon invert FY2 three-month revision：{"dataset": "multi_horizon_alpha", "example_id": "78jxLkAO", "sharpe": 0.95, "fitness": 0.69, "prod_corr": 0.945, "sibling": "LL7nMPjn", "wave": 39, "reason": "invert FY2 3m revision S0.95 F0.69 prod 0.945. Same analyst-revision crowding as long_term estrev invert. Residual /S/1.11 is the uninverted side. Do not invert-dominant or dilute.", "rule": "Do not use invert FY2 revision as dominant. Same
- `EUR-MH-NOA-PEG-WEAK`（2026-08-24）family=multi_horizon NOA change and PEG：{"dataset": "multi_horizon_alpha", "max_abs_sharpe": 0.27, "fields": ["long_term_change_in_net_operating_assets", "long_term_inverse_dividend_adjusted_peg"], "wave": 39, "reason": "NOA max /S/0.27 PEG /S/0.15. Not independent. IS rank /S/0.6 only. Do not occupy another slot with NOA/PEG probes.", "rule": "Do not occupy slots with NOA or PEG probes.", "dead_at": "2026-08-24"}
- `EUR-MH-VALUE-COUNTRY-SALES-WEAK`（2026-08-24）family=multi_horizon country gz value and sales_to_price：{"dataset": "multi_horizon_alpha", "example_id": "rKjbdxn1", "max_sharpe": 0.89, "wave": 39, "reason": "country gz / neutralize invert deep_value max S0.89; sales_to_price /S/0.22. Not independent of Wave38 value residual path. Do not occupy another slot.", "rule": "Do not occupy slots with country-gz deep_value or sales_to_price.", "dead_at": "2026-08-24"}
- `EUR-MH-LEVERAGE-RESID-DOMINANT`（2026-08-24）family=multi_horizon leverage industry residual as dominant：{"dataset": "multi_horizon_alpha", "example_id": "88lONkOV", "expr_pattern": "rank(subtract(long_term_management_leverage_europe_rank, group_mean(..., industry)))", "settings": "EUR TOP2500 COUNTRY decay6", "sharpe": -1.58, "fitness": -0.87, "two_year_sharpe": -2.68, "sibling": "1YwoWVoX invert naked rank S0.87 F0.46 2Y2.26", "wave": 40, "id": "EUR-MH-LEVERAGE-RESID-DOMINANT", "reason": "Leverage 
- `EUR-MH-LEVERAGE-3LEG-VREV-WEDGE-PROD`（2026-08-24）family=multi_horizon leverage residual x v_reversal x falling_wedge：{"dataset": "multi_horizon_alpha", "example_id": "P071A7zL", "prod_corr": 0.7644, "reason": "Wave46 leverage 3-leg passes IS/ladder (P071A7zL S1.80 F1.13 2Y2.27 RN1.02 RA=0) but prod 0.7644. Lower MODEL weight made prod worse (E5lK2l80 0.30 -> 0.7867; d5jQPj3j 0.28 -> 0.7958). Do not Mode A. Leave this 3-leg.", "rule": "Do not grind leverage x v_reversal x falling_wedge weights. Mode B must change
- `EUR-MH-GROWTH-FLOW-3LEG-PROD`（2026-08-24）family=multi_horizon growth_flow_to_price residual x v_rev x wedge：{"dataset": "multi_horizon_alpha", "example_id": "Grlo2az5", "fitness": 1.25, "prod_corr": 0.8136, "reason": "Wave48 0.30 growth_flow_to_price_2 residual x 0.40 v_rev x 0.30 wedge S1.91 F1.25 ladder 2.20 RN0.87 but prod 0.8136. Do not Mode A.", "rule": "Do not grind growth_flow_to_price x v_rev x wedge weights. Mode B must change slow field.", "sharpe": 1.91, "two_year_sharpe": 2.2, "wave": 48}
- `EUR-MH-VALUE-ANALYST-3LEG-PROD`（2026-08-24）family=multi_horizon value_analyst residual x v_rev x wedge：{"dataset": "multi_horizon_alpha", "example_id": "lej0ne0e", "fitness": 1.33, "prod_corr": 0.9101, "reason": "Wave48 0.30 value_analyst residual x v_rev x wedge S1.99 F1.33 ladder 2.14 RN0.90 prod 0.9101. Do not Mode A.", "rule": "Do not grind value_analyst x v_rev x wedge. Mode B must change slow field.", "sharpe": 1.99, "two_year_sharpe": 2.14, "wave": 48}
- `EUR-MH-FS-RANK-3LEG-PROD`（2026-08-24）family=multi_horizon FS rank residual x v_rev x wedge：{"dataset": "multi_horizon_alpha", "example_id": "9qXReZ11", "fitness": 1.13, "prod_corr": 0.9029, "reason": "Wave48 FS_rank 0.30 3leg S1.75 F1.13 ladder 2.13 RN0.92 prod 0.9029. FS strength max S1.21 missed cheap gate. Do not Mode A.", "rule": "Do not grind FS rank/strength x v_rev x wedge. Leave FS family as slow leg.", "sharpe": 1.75, "two_year_sharpe": 2.13, "wave": 48}
- `EUR-MH-INCOME-STMT-3LEG-PROD`（2026-08-24）family=multi_horizon income_statement_rank residual x v_rev x wedge：{"dataset": "multi_horizon_alpha", "example_id": "gJj3lp50", "fitness": 1.22, "prod_corr": 0.8538, "reason": "Wave48 income_statement_rank 0.30 3leg S1.90 F1.22 ladder 2.05 but RN 0.74 and prod 0.8538. OLL change max S1.21. Do not Mode A.", "rn": 0.74, "rule": "Do not grind income_statement_rank x v_rev x wedge. Leave OLL/income as slow leg.", "sharpe": 1.9, "two_year_sharpe": 2.05, "wave": 48}
- `EUR-MH-ROE-3LEG-WEAK`（2026-08-24）family=multi_horizon ROE residual x v_rev x wedge：{"dataset": "multi_horizon_alpha", "max_sharpe": 1.47, "reason": "Wave48 ROE/ROE1 3leg max S1.47 F0.93 missed cheap gate. Horizon/weight variants will not jump 1.58. Do not occupy another slot.", "rule": "Do not occupy slots with ROE residual x v_rev x wedge.", "wave": 48}
- `EUR-MH-W49-UNUSED-3LEG-WEAK`（2026-08-24）family=multi_horizon PTA/street/nrev/pmom/rational_decay x v_rev x wedge：{"best": {"xAjnJdqq": {"fit": 0.97, "sharpe": 1.54, "slot": "mid nrev fy1"}}, "dataset": "multi_horizon_alpha", "max_sharpe": {"decay": 0.46, "nrev": 1.54, "pmom": 1.28, "pta": 1, "street": 1.27}, "reason": "Wave49 unused MH slow legs all missed cheap gate. PTA 1.00 street 1.27 nrev 1.54/0.97 pmom 1.28 decay 0.46. Do not Mode A grind these families.", "rule": "Do not occupy slots with PTA, street_
- `EUR-MH-NREV-LADDER-WALL`（2026-08-24）family=multi_horizon_nrev：{"concepts": ["PTA", "street", "nrev", "pmom", "decay", "MH_pure_legs"], "dataset": "multi_horizon_alpha", "evidence": {"modeA_best_S_F": "omqK2zxb S1.63 F1.13 ladder~1.00 INDUSTRY", "modeA_best_ladder": "6Xlwbo2p S1.58 F1.01 ladder1.14", "modeB_best": "58lw7RpN S1.55 F0.92 2Y1.28", "modeB_note": "dropping avg_similarity legs collapsed S/F; ladder still <<1.58"}, "limit": {"sharpe": 1.58, "fitness
- `EUR-MH-EV-EBITDA-3LEG-RN-PROD`（2026-08-24）family=multi_horizon EV rank / ebitda-to-EV x v_rev x wedge：{"dataset": "multi_horizon_alpha", "example_id": "P071R0vK", "prod_corr": 0.9285, "reason": "Wave58 EV rank 3leg P071R0vK S1.75 F1.08 ladder 2.10 RN0.81 prod 0.9285. EBITDA/EV d5jQPR5X S1.69 F1.03 ladder 2.03 RN0.66 prod 0.8461. Both fail RN>1 and prod>=0.7. Do not Mode A grind weights.", "rn": 0.81, "rule": "Do not grind long_term_enterprise_value_europe_rank or ebitda_to_enterprise_value x v_rev
- `EUR-MH-DEEPVALUE-INVERT-PROD`（2026-08-25）family=multi_horizon deep_value invert x common_gap_up：{"best": {"alpha": "j2j0R5Zo", "fitness": 1, "prod": 0.7121, "sharpe": 1.61}, "dataset": "multi_horizon_alpha", "id": "EUR-MH-DEEPVALUE-INVERT-PROD", "reason": "Wave80 invert long_term_deep_value_europe_rank x winning PV passed cheap gate but prod 0.712. Do not Mode A this field.", "rule": "Do not Mode A deep_value invert. Do not submit prod>=0.7.", "wave": 80}
- `EUR-MH-LEVERAGE-INVERT-RN`（2026-08-25）family=multi_horizon mgmt leverage invert x common_gap_up：{"best": {"alpha": "3qlRb8xg", "fitness": 1, "prod": 0.592, "rn": 0.41, "sharpe": 1.68}, "dataset": "multi_horizon_alpha", "id": "EUR-MH-LEVERAGE-INVERT-RN", "reason": "Wave80 invert mgmt leverage passed cheap gate (S1.68 F1.0 2Y2.56) but RN 0.41 vs gJj1nxLM 0.66. Invert recipe is valid; do not Mode A this field.", "rule": "Do not Mode A leverage invert. Keep invert recipe on unused MH fields. Kee
- `EUR-MH-FCF-INVERT-PROD`（2026-08-25）family=multi_horizon trailing FCF-to-price invert x common_gap_up：{"best": {"alpha": "6Xl9vj9O", "fitness": 1.46, "prod": 0.7342, "rn": 0.67, "sharpe": 2.15}, "dataset": "multi_horizon_alpha", "id": "EUR-MH-FCF-INVERT-PROD", "reason": "Wave81 invert trailing_free_cash_flow_to_price passed cheap+ladder+2Y (S2.15 F1.46 RN0.67) but prod 0.734. Sibling E5lEXpwL prod 0.731. Mutual 0.85 vs 3qlRb8xg. Do not Mode A this field vs prod.", "rule": "Do not Mode A FCF invert

