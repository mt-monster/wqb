# model193 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model193` |
| 名称 | — |
| 类别 | MODEL |
| 数据字段数(平台) | 173 |
| 覆盖率 | 0.685 |
| 平台已有 alpha | 85 |
| valueScore | 6 |
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
| 字段总数 | **173** |
| 类型分布 | MATRIX×173 |
| 平均覆盖率 | **0.685** |
| 覆盖率区间 | 0.25 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 99 | 57.2% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 74 | 42.8% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 99 | 57.2% |
| UNUSABLE | 74 | 42.8% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 99 / UNUSABLE 74 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 64 | 0.68 | annual_cashflow_asset_change、book_leverage_ratio、cds_deep_value_comprehensive_debt |
| 价量与波动 | 55 | 0.64 | cds_1d_change_default_prob_5y、cds_1m_spread_volatility、cds_1y_spread_beta |
| 修正与预期 | 17 | 0.65 | analyst_consensus_rating、analyst_eps_estimate_dispersion、analyst_forecast_revision_count_fy1 |
| 风险与质量 | 15 | 0.75 | altman_z_score、cds_1d_change_default_prob_1y、cds_1m_change_default_prob_1y |
| 其他 | 14 | 0.79 | annual_percent_change_shares_outstanding、basic_defensive_interval_days、capital_gearing_ratio |
| 持仓与资金流 | 4 | 1.00 | cashflow_vs_eps_change、demand_supply_ratio_borrowed_to_lendable、short_interest_days_to_cover |
| 宏观与行业 | 2 | 1.00 | cash_burn_rate_ratio、reinvestment_rate_per_share |
| 元数据与非信号 | 1 | 0.27 | mdl193_cds_redcode |
| 交易与微观结构 | 1 | 0.27 | mdl193_ticker |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `altman_z_score` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Altman Z-score, a measure of company credit risk or bankruptcy risk |
| 2 | `analyst_consensus_rating` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus stock rating from market participants or analysts |
| 3 | `analyst_eps_estimate_dispersion` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Dispersion of analysts' FY1 EPS estimates (coefficient of variation) |
| 4 | `analyst_forecast_revision_count_fy1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Net number of analyst forecast revisions for fiscal year 1 |
| 5 | `analyst_rating_revision_6m` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of RatRev6M to maintain continuity when raw data are missing |
| 6 | `annual_cashflow_asset_change` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in assets-adjusted trailing twelve-month cash flow |
| 7 | `annual_percent_change_shares_outstanding` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Percent change in the number of shares outstanding compared to a specified previous period, typically one year ago |
| 8 | `basic_defensive_interval_days` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Imputed or backfilled value of BDI used when the raw BDI is missing to enhance continuity |
| 9 | `book_leverage_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book leverage ratio (likely debt to equity or related measure using book values) |
| 10 | `capital_gearing_ratio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of GEAR, used when raw data are missing |
| 11 | `cash_burn_rate_ratio` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CashBurnRate to maintain continuity when raw data are missing |
| 12 | `cash_conversion_cycle` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CashC to maintain continuity when raw data are missing |
| 13 | `cashflow_vs_eps_change` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of NCFEPS used when raw data are missing |
| 14 | `cds_1d_change_default_prob_1y` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in probability of default (implied from 1-year CDS) over a single day, measuring daily credit risk movement for t |
| 15 | `cds_1d_change_default_prob_5y` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-day change in probability of default using CDS spread at 5-year tenor |
| 16 | `cds_1m_change_default_prob_1y` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | 1-month change in probability of default for the 1-year tenor |
| 17 | `cds_1m_change_default_prob_5y` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | 1-month Change in Probability of Default (Tenor=5Y) |
| 18 | `cds_1m_spread_volatility` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-month CDS Spread Change Volatility (Tenor=5Y) |
| 19 | `cds_1y_spread_beta` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Imputed or backfilled value of CDS_1YBeta used when the raw beta is missing to enhance continuity |
| 20 | `cds_5d_change_default_prob_1y` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | 5-day change in the 1-year CDS-implied probability of default |
| 21 | `cds_5d_change_default_prob_5y` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | 5-day change in probability of default as implied by 5-year CDS, showing short-term movement in perceived credit risk fo |
| 22 | `cds_60m_spread_beta` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year (60 month) beta of CDS spread changes (measure of CDS spread sensitivity to market) |
| 23 | `cds_deep_value_comprehensive_debt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Comprehensive debt-to-assets ratio; total company debt as percentage of total assets for deep value analysis |
| 24 | `cds_deep_value_interest_coverage` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Difference between observed default probability and model fair value using interest coverage (deep value model). |
| 25 | `cds_default_probability_1y` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated probability of default over a one-year horizon, typically derived from the entity’s CDS data (Tenor=1Y) |
| 26 | `cds_default_probability_5y` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability of default over a 5-year horizon implied by CDS spread |
| 27 | `cds_distress_relative_value` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Imputed/backfilled value of CDS_DM used when raw data are missing to maintain series continuity |
| 28 | `cds_equity_price_sensitivity` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity price sensitivity (how the CDS spread responds to equity price movements) |
| 29 | `cds_fx_sensitivity_eurusd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Sensitivity of CDS spread to EUR/USD exchange rate movements |
| 30 | `cds_index_return_sensitivity_xover` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CDS_XO to maintain continuity when raw data are missing |
| 31 | `cds_interest_coverage_relative_value` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Interest coverage ratio: company's relative ability to cover interest expense (specific formula may vary, likely EBIT or |
| 32 | `cds_market_volatility_sensitivity` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Sensitivity of the entity’s CDS spread to changes in overall market volatility (typically measured by VIX), reflecting h |
| 33 | `cds_oil_price_sensitivity` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CDS_OilPrice, the ranked sensitivity of daily CDS spread changes to oil price changes, use |
| 34 | `cds_relative_value_1m_volatility` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Difference between observed default probability and model fair value using 1-month realized volatility. |
| 35 | `cds_relative_value_comprehensive_debt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Relative Value - Comprehensive Debt to Total Assets |
| 36 | `cds_sensitivity_to_canada_sovereign` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sovereign Sensitivity - Canada |
| 37 | `cds_sensitivity_to_france_sovereign` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Sensitivity of an entity's CDS spread changes to France sovereign CDS, representing how much the entity's CDS responds t |
| 38 | `cds_sensitivity_to_german_sovereign` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Sensitivity of an entity's CDS spread changes to German sovereign CDS, representing correlation to changes in Germany's |
| 39 | `cds_sensitivity_to_italy_sovereign` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Sensitivity of CDS spread changes to Italian sovereign movements |
| 40 | `cds_sensitivity_to_japan_sovereign` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sovereign Sensitivity - Japan |
| 41 | `cds_sensitivity_to_portugal_sovereign` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CDS_PorBeta, the ranked sensitivity of daily CDS spread changes to Portugal sovereign CDS |
| 42 | `cds_sensitivity_to_spain_sovereign` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CDS_SpaBeta, the ranked sensitivity of daily CDS spread changes to Spain sovereign CDS cha |
| 43 | `cds_sensitivity_to_uk_sovereign` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Sensitivity of CDS spread changes to UK sovereign movements |
| 44 | `cds_sensitivity_to_us_sovereign` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Sensitivity of CDS spread changes to US sovereign movements |
| 45 | `comprehensive_debt_to_assets_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CompDA to maintain continuity when raw data are missing |
| 46 | `cross_asset_value_divergence` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CDS_PS_Reg3, representing the same model-based value divergence when raw data are missing |
| 47 | `current_cashflow_debt_coverage` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Cash Flow Debt Coverage Ratio |
| 48 | `current_ratio_liquidity_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current ratio; company liquidity measured as current assets divided by current liabilities |
| 49 | `demand_supply_ratio_borrowed_to_lendable` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of Dmd_Supply, used when raw data are missing |
| 50 | `dtcc_gross_notional_1m_growth` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | One-month growth rate in DTCC (central clearinghouse) gross notional CDS volumes, reflecting liquidity/trading activity |
| 51 | `dtcc_gross_notional_1y_growth` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year growth in DTCC Gross Notional Volumes (open CDS positions for the company) |
| 52 | `dtcc_gross_notional_5w_avg` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Five-week moving average of weekly gross notional CDS transaction volumes from DTCC, measuring recent liquidity/activity |
| 53 | `dtcc_gross_notional_5w_change` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-week Change in DTCC Weekly Gross Notional Volumes |
| 54 | `dtcc_gross_notional_to_debt_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of DTCC gross notional CDS volumes to total company debt |
| 55 | `earnings_revision_magnitude_3m` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision magnitude (extent of analyst forecast EPS revisions for the company) |
| 56 | `earnings_surprise_std_adjusted` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Most recent quarterly earnings surprise (difference between actual and estimated EPS), normalized by the standard deviat |
| 57 | `earnings_vs_free_cashflow_shortfall` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Shortfall |
| 58 | `ebitda_to_debt_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA-to-Debt: ratio of TTM EBITDA divided by total debt |
| 59 | `ebitda_to_enterprise_value_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | TTM EBITDA-to-Enterprise Value ratio: measures earnings yield relative to valuation |
| 60 | `financial_distress_score` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of DM to maintain continuity when raw data are missing |
| 61 | `five_year_dividend_growth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-Year Dividend Growth Rate |
| 62 | `implied_loan_fee` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Imputed or backfilled value of Benchmark_fee used when the raw benchmark fee is missing to enhance continuity |
| 63 | `industry_relative_4w_return_zscore` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-week Industry Relative Return |
| 64 | `industry_relative_5d_return_zscore` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-day industry relative return (security return compared to industry average over 5 days) |
| 65 | `industry_relative_quarterly_roe_zscore` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-adjusted quarterly return on equity |
| 66 | `interest_coverage_ratio_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Interest coverage ratio (likely EBIT or similar over interest expense) |
| 67 | `leading_credit_risk_signal_indicator` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CDS_LRI, representing the same leading risk measure when raw data are missing |
| 68 | `liabilities_to_operating_cashflow_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CFLeverage to maintain continuity when raw data are missing |
| 69 | `liquidity_to_current_liabilities_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash and cash equivalents to current liabilities, indicating short-term liquidity position |
| 70 | `long_term_debt_to_equity_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of DE to maintain continuity when raw data are missing |
| 71 | `long_term_growth_projection_indicator` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of long-term growth rate for the company |
| 72 | `momentum_divergence_1m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-month Momentum Divergence |
| 73 | `momentum_divergence_5d` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of CDS_PS_Rank5D, the same 5-day momentum divergence measure used when raw data are missing |
| 74 | `net_debt_to_total_capital` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt ratio (net debt divided by a relevant base like equity or total assets) |
| 75 | `net_operating_profit_margin` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Operating Profit After Tax Margin; margin calculated as NOPAT divided by revenue |
| 76 | `ohlson_bankruptcy_risk_indicator` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Ohlson Bankruptcy Score; statistical measure of bankruptcy risk based on Ohlson's financial ratios |
| 77 | `one_month_realized_return_volatility` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of realized stock returns over the past 1 month (realized volatility) |
| 78 | `operating_cashflow_to_liabilities_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Cash Flow Ratio: ratio of operating cash flow to either current liabilities or total liabilities to assess liq |
| 79 | `operating_income_vs_long_term_debt_change` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in trailing twelve months operating income compared to long-term debt |
| 80 | `operating_leverage_ratio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Operating Leverage, likely percent change in operating income divided by percent change in sales |
| 81 | `operating_liability_leverage` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Imputed/backfilled Operating Liability Leverage used when raw data are missing |
| 82 | `profitability_to_assets_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Imputed/backfilled Profitability Ratio used when raw data are missing |
| 83 | `quick_ratio_liquidity_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio (Acid Test Ratio): measure of a company's short-term liquidity calculated as (Current Assets - Inventories) |
| 84 | `reinvestment_rate_per_share` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of ReInRate to maintain continuity when raw data are missing |
| 85 | `retained_earnings_to_assets_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings divided by total assets |
| 86 | `return_on_assets_ttm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets: net income or similar measure divided by total assets |
| 87 | `return_on_invested_capital_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Invested Capital (profitability relative to invested capital) |
| 88 | `short_interest_days_to_cover` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Days to cover short interest (days of average trading needed to buy back all shares sold short) |
| 89 | `short_interest_ratio` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Short interest (likely number or percentage of shares shorted for the security) |
| 90 | `three_month_eps_revision_dispersion` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Relative dispersion (standard deviation) of 3-month revisions in next-fiscal-year-2 EPS forecasts |
| 91 | `three_year_cashflow_asset_change` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of Chg3YCFAst to maintain continuity when raw data are missing |
| 92 | `total_coverage_ratio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of TotalCov to maintain continuity when raw data are missing |
| 93 | `total_debt_to_assets_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt to Total Assets ratio (leverage measure) |
| 94 | `trading_volume_visibility_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Imputed/backfilled version of VisiRatio to maintain continuity when raw data are missing |
| 95 | `twelve_month_total_debt_change` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in total debt over the past 12 months |
| 96 | `unexpected_profitability_score` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected Profitability |
| 97 | `yearly_change_current_ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Year-over-year change in current ratio (liquidity metric) |
| 98 | `yearly_change_debt_to_assets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in leverage, probably defined as change in total debt to assets ratio |
| 99 | `yoy_change_ebitda_to_debt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-Year Change in EBITDA-to-Debt |
| 100 | `mdl193_cds_1mvol` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the standard deviation of daily 5-year CDS spread change over the trailing one month |
| 101 | `mdl193_cds_probdefault5y` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the probability of default implied by the 5-year CDS spread. |
| 102 | `mdl193_cds_ps_rank1m` | MATRIX | 0.266 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The factor is the difference between the 1-month Active Return equity factor rank and the 1-month Change in Probability |
| 103 | `mdl193_cds_ps_rank5d` | MATRIX | 0.266 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The factor is the difference between the 5-day Industry Relative Return equity factor rank and the 5-day Change in Proba |
| 104 | `mdl193_cds_redcode` | MATRIX | 0.266 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | CDS RedCode |
| 105 | `mdl193_dtsm1_rd` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the standard deviation of stock's daily total return over the trailing one month. |
| 106 | `mdl193_dtsm1_rd_sdc` | MATRIX | 0.266 | 风险与质量 | 0 | — | — | — | UNUSABLE | The factor is the difference between the observed probability of default and the its fair value predicted by a proprieta |
| 107 | `mdl193_indrelrtn4w_` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as a stock's return in last 4-weeks minus the average of the comparable returns of all stocks in the same |
| 108 | `mdl193_indrelrtn5d_` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as a stock's return in the last 5 days minus the average of the comparable returns of all stocks in the sa |
| 109 | `mdl193_ticker` | MATRIX | 0.266 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Ticker |
| 110 | `mdl193_y5dpghcd1_sdc` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the change in the probability of default implied by the 5-year CDS spread from date t-1 to date t. |
| 111 | `mdl193_y5dpghcd5_sdc` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the change in the probability of default implied by the 5-year CDS spread from date t-5 to date t. |
| 112 | `mdl193_y5dpghcm1_sdc` | MATRIX | 0.266 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the change in the probability of default implied by the 5-year CDS spread from month t-1 to month t. |
| 113 | `mdl193_ad` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the most recently reported total debt divided by total assets. |
| 114 | `mdl193_aor` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the trailing 12-month income before extra items divided by the average of total assets in the same peri |
| 115 | `mdl193_booklev` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the most recently reported quarterly total assets divided by the book equity. |
| 116 | `mdl193_chg12mtotdebt` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the 12 month relative change in total debt, where total debt is the sum of long-term and short-term deb |
| 117 | `mdl193_chg3ycfast` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the most recently reported trailing 12-month operating cash flow minus 12-quarter ago comparable traili |
| 118 | `mdl193_chgshare` | MATRIX | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | It is defined as the percent change in a company's current number of outstanding shares as compared to the number of sha |
| 119 | `mdl193_earnshortfall` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the difference between reported accounting earnings and free cash flow, scaled by average assets. |
| 120 | `mdl193_ed` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the most recently reported total long-term debt divided by total book equity. |
| 121 | `mdl193_fcghc` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the the trailing 12-month cash flow minus comparable trailing 12-month cash flow from 4-quarters ago sc |
| 122 | `mdl193_gear` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the long-term debt divided by the difference between total assets and current liability. |
| 123 | `mdl193_ollev` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as 1 minus the ratio of (short-term debt + long-term debt + common equity + preferred equity - cash) to (t |
| 124 | `mdl193_rp` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the latest reported quarterly operating income divided by 12-Month lagged total assets. |
| 125 | `mdl193_yoychgda` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the difference between the most recent reported quarterly total liabilities as a percentage of the repo |
| 126 | `mdl193_2adpmoc_sdc` | MATRIX | 0.264 | 风险与质量 | 0 | — | — | — | UNUSABLE | The factor is the difference between the observed probability of default and the its fair value predicted by a proprieta |
| 127 | `mdl193_2vd_adpmoc_sdc` | MATRIX | 0.264 | 风险与质量 | 0 | — | — | — | UNUSABLE | The factor is the difference between the observed probability of default and the its fair value predicted by a proprieta |
| 128 | `mdl193_adpmoc` | MATRIX | 0.264 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the most recently reported sum of long-term debt, short-term debt, underfunded pension liabilities, ope |
| 129 | `mdl193_cds_1ybeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the average company in the Markit CDX North A |
| 130 | `mdl193_cds_canbeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the Canada sovereign CDS. The highest (lowest |
| 131 | `mdl193_cds_eurusd` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to the daily change in EUR/USD exchange rate. The highes |
| 132 | `mdl193_cds_frabeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the France sovereign CDS. The highest (lowest |
| 133 | `mdl193_cds_gerbeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the Germany sovereign CDS. The highest (lowes |
| 134 | `mdl193_cds_itabeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the Italy sovereign CDS. The highest (lowest) |
| 135 | `mdl193_cds_japbeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the Japan sovereign CDS. The highest (lowest) |
| 136 | `mdl193_cds_oilprice` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to the daily change in oil price. The highest (lowest) s |
| 137 | `mdl193_cds_porbeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the Portugal sovereign CDS. The highest (lowe |
| 138 | `mdl193_cds_probdefault1y` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the probability of default implied by the 1-year CDS spread. |
| 139 | `mdl193_cds_spabeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the Spain sovereign CDS. The highest (lowest) |
| 140 | `mdl193_cds_ukbeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the United Kingdom sovereign CDS. The highest |
| 141 | `mdl193_cds_usbeta` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to that of the United States sovereign CDS. The highest |
| 142 | `mdl193_ebitdaev` | MATRIX | 0.264 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the trailing 12-month earnings before interest,taxes,depreciation and amortization for a stock deflated |
| 143 | `mdl193_ox_sdc` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to the daily Markit iTraxx Crossover index return. The h |
| 144 | `mdl193_roic` | MATRIX | 0.264 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the trailing 12-month net income and interest expenses divided by the average reported invested capital |
| 145 | `mdl193_tqe_sdc` | MATRIX | 0.264 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread to the daily equity price. The highest (lowest) sensitivity nam |
| 146 | `mdl193_xiv_sdc` | MATRIX | 0.264 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the sensitivity of the daily CDS spread change to the daily change in market volatility (VIX). The high |
| 147 | `mdl193_2vd_voctni_sdc` | MATRIX | 0.263 | 风险与质量 | 0 | — | — | — | UNUSABLE | The factor is the difference between the observed probability of default and the its fair value predicted by a proprieta |
| 148 | `mdl193_2voctni_sdc` | MATRIX | 0.263 | 风险与质量 | 0 | — | — | — | UNUSABLE | The factor is the difference between the observed probability of default and the its fair value predicted by a proprieta |
| 149 | `mdl193_netdebt` | MATRIX | 0.263 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the net debt divided by the sum of the net debt, preferred stock and common stock, where net debt equal |
| 150 | `mdl193_nopatmargin` | MATRIX | 0.263 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as: (Net Income + Interest Expense*(1-Effective Tax Rate))/Net Sales.All items are for trailing 12-month. |
| 151 | `mdl193_visiratio` | MATRIX | 0.263 | 价量与波动 | 0 | — | — | — | UNUSABLE | It equals to a stock's most recent daily trading volume divided by the average daily trading volume in previous 50 tradi |
| 152 | `mdl193_voctni` | MATRIX | 0.263 | 其他 | 0 | — | — | — | UNUSABLE | It is defined as the most recently reported quarterly operating income before depreciation divided by the quarterly long |
| 153 | `mdl193_y1dpghcd1_sdc` | MATRIX | 0.263 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the change in the probability of default implied by the 1-year CDS spread from date t-1 to date t. |
| 154 | `mdl193_y1dpghcd5_sdc` | MATRIX | 0.263 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the change in the probability of default implied by the 1-year CDS spread from date t-5 to date t. |
| 155 | `mdl193_y1dpghcm1_sdc` | MATRIX | 0.263 | 价量与波动 | 0 | — | — | — | UNUSABLE | It is defined as the change in the probability of default implied by the 1-year CDS spread from month t-1 to month t. |
| 156 | `mdl193_aoer` | MATRIX | 0.263 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the reported cumulative retained earnings from the most recent quarter deflated by reported total asset |
| 157 | `mdl193_cds_ps_reg3` | MATRIX | 0.263 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The factor is based on a proprietary model that links equity price to CDS spread. The model residual value is adjusted b |
| 158 | `mdl193_fc_numrevy1` | MATRIX | 0.263 | 修正与预期 | 0 | — | — | — | UNUSABLE | It is defined as the weighted average of the number of FY1 analyst earnings forecasts raised less the number lowered wit |
| 159 | `mdl193_gtl` | MATRIX | 0.263 | 修正与预期 | 0 | — | — | — | UNUSABLE | It is defined as the consensus long term growth forecast.  It generally represents an expected annual increase in operat |
| 160 | `mdl193_ratrev6m` | MATRIX | 0.263 | 修正与预期 | 0 | — | — | — | UNUSABLE | It is defined as the 6-month average of the monthly change in the average analyst recommendation. |
| 161 | `mdl193_rev3my2std` | MATRIX | 0.263 | 修正与预期 | 0 | — | — | — | UNUSABLE | It is defined as the change in a stock's current analysts mean earnings estimate for fiscal year 2 less that of three mo |
| 162 | `mdl193_stockrating` | MATRIX | 0.263 | 修正与预期 | 0 | — | — | — | UNUSABLE | It is defined as the consensus recommendation for a company. |
| 163 | `mdl193_dcc` | MATRIX | 0.262 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the most recently reported quarterly cash flow from operations less the cash dividends divided by the c |
| 164 | `mdl193_div5yg` | MATRIX | 0.262 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the 5-year growth in dividends |
| 165 | `mdl193_indrelcroe_` | MATRIX | 0.262 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as a stock's lagged quarterly return on equity (ROE) minus the average of the ROEs of all stocks in the sa |
| 166 | `mdl193_opincltd` | MATRIX | 0.262 | 其他 | 0 | — | — | — | UNUSABLE | It is defined as the difference between the yearly percent change in operating income and the yearly percent change in l |
| 167 | `mdl193_reinrate` | MATRIX | 0.262 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the trailing 12-month earnings per share before extra items less the trailing 12-month dividends per sh |
| 168 | `mdl193_spe1yfvc_cf` | MATRIX | 0.261 | 修正与预期 | 0 | — | — | — | UNUSABLE | It is defined as the standard deviation of analyst earnings estimates for fiscal year 1 divided by the mean consensus fo |
| 169 | `mdl193_oplev` | MATRIX | 0.260 | 其他 | 0 | — | — | — | UNUSABLE | It is defined as the percent change in the trailing 12-month operating income from previous quarter divided by the perce |
| 170 | `mdl193_pu` | MATRIX | 0.260 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It is defined as the difference between realized profitability and expected one which is calculated from a regression mo |
| 171 | `mdl193_mrspe_cf` | MATRIX | 0.258 | 修正与预期 | 0 | — | — | — | UNUSABLE | It is defined as the 3-month change in the median FY1 consensus earnings forecast, scaled by the current mean earnings e |
| 172 | `mdl193_fc_fqsurstd` | MATRIX | 0.255 | 修正与预期 | 0 | — | — | — | UNUSABLE | It is defined as the most recent quarterly earnings surprise (actual fiscal quarter EPS less the consensus earnings esti |
| 173 | `mdl193_totalcov` | MATRIX | 0.253 | 盈利与财务 | 0 | — | — | — | UNUSABLE | It equals (Cash Flow from Operations + Interest Paid + Tax Paid)/ (Interest + Principal Paid). |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-M193-NAMED-SLOW-INERT`（2026-08-25）family=model193 named MATRIX residual x v_rev/wedge：{"best": {"alpha": "rKjobb71", "sharpe": 1.03, "fitness": 0.53}, "reason": "Wave60 seven named model193 slows (dispersion/cashflow/CCC/loan/industry z/revision/liquidity) x v_rev/wedge produced identical S1.03 F0.53 across all slots. Slow residual added no differentiation; signal is PV-only. Leave this recipe.", "rule": "Do not reuse model193 high-coverage named fields as 0.30 slow legs with v_rev
- `EUR-MODEL193-W129-CREDIT-AXIS-DEAD`（2026-09-06）family=model193 信用风险/CDS/困境轴：{"dataset": "model193", "waves": [129], "region": "EUR", "reason": "14 条候选（8 首批 + 6 修复）全 ra_failed。修复 CW 后信号普遍为负，最佳仅 sharpe 0.13。信用风险/CDS/困境轴在 EUR/D1 无预测力。", "rule": "Leave model193 的 CDS 利差波动/beta、破产风险(Altman Z / Ohlson)、违约概率、空头回补压力、现金流-稀释、ebitdaev-CDS 名义敷口全系。", "critical_lesson": "★ 高 returns 可能是 CONCENTRATED_WEIGHT 缺陷制造的假象，不是信号。gJQKrxJm returns 0.0885（全战役最高，是 ACTIVE 的 2 倍）伴 CW=0.500；加 ts_backfi

