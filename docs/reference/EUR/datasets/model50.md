# model50 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model50` |
| 名称 | International Scorings Data |
| 类别 | MODEL |
| 数据字段数(平台) | 168 |
| 覆盖率 | 0.8551 |
| 平台已有 alpha | 249 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive downside risk assessments for international equities, offering weekly scores that estimate the probability of a stock underperforming market averages over a 3 to 24 month horizon. It includes a wide array of quantitative metrics such as earnings valuation, free cash flow yield, shareholder yield, profitability, growth, leverage, analyst forecast revisions, price momentum, and volatility, both at the global and country levels. The data is organized by company, sector, and country, with decile rankings to facilitate relative comparisons. By aggregating these factors into a composite risk score, the dataset enables investors and quantitative researchers to identify stocks with elevated downside risk, making it a valuable tool for portfolio risk management, 

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **168** |
| 类型分布 | MATRIX×168 |
| 平均覆盖率 | **0.855** |
| 覆盖率区间 | 0.37 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 54 | 32.1% |
| 中 (0.70–0.90) | 110 | 65.5% |
| 低 (0.50–0.70) | 2 | 1.2% |
| 稀疏 (<0.50) | 2 | 1.2% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 155 | 92.3% |
| DEAD | 6 | 3.6% |
| DEAD_STATIC | 5 | 3.0% |
| UNUSABLE | 2 | 1.2% |

- 已实测字段：**11** 个（7%），best_sharpe 最高 **0.80**，中位 0.14

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 57 | 0.85 | mdl50_bk_cn_fcf_valu、mdl50_bk_cn_profitabil_cons、mdl50_bk_profitabil_cons |
| 宏观与行业 | 29 | 0.87 | country_capital_investment_score、beta_relative_to_country_backfill、country_capital_investment_score_backfill |
| 价量与波动 | 25 | 0.86 | mdl50_bk_price_change_6m、closing_stock_price、country_level_price_volatility_score |
| 修正与预期 | 17 | 0.82 | mdl50_bk_cn_analyst_revisn、mdl50_bk_analyst_revisn、analyst_count_fy1_forecasts_backfill |
| 风险与质量 | 16 | 0.88 | mdl50_bk_drai_score_chg_1w、aggregate_downside_risk_score_backfill、beta_relative_to_global_index |
| 其他 | 13 | 0.82 | five_year_eps_growth_forecast_backfill、forward_pe_ratio_trailing、latest_quarterly_eps_surprise_backfill |
| 持仓与资金流 | 8 | 0.89 | mdl50_bk_fcf_valu、country_level_fundamental_stability_score、free_cash_flow_yield_score_backfill |
| 交易与微观结构 | 2 | 0.81 | mdl50_bk_adr_ticker、mdl50_bk_ticker |
| 元数据与非信号 | 1 | 0.81 | mdl50_bk_company_name |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl50_bk_cn_fcf_valu` | MATRIX | 0.799 | 盈利与财务 | 3 | 0.80 | 0.57 | 0.62 | DEAD_STATIC | Country-normalized free cash flow valuation |
| 2 | `mdl50_bk_cn_profitabil_cons` | MATRIX | 0.754 | 盈利与财务 | 3 | 0.49 | 1.22 | 0.65 | DEAD | Profitability consistency score relative to the country |
| 3 | `mdl50_bk_drai_score_chg_1w` | MATRIX | 0.817 | 风险与质量 | 3 | 0.46 | 0.92 | 0.48 | DEAD | One-week change in the downside-risk score |
| 4 | `mdl50_bk_price_change_6m` | MATRIX | 0.817 | 价量与波动 | 2 | 0.25 | 0.11 | 0.38 | DEAD | Stock price change over the past 6 months |
| 5 | `mdl50_bk_cn_analyst_revisn` | MATRIX | 0.792 | 修正与预期 | 1 | 0.15 | 0.18 | 0.33 | DEAD_STATIC | Country-normalized analyst estimate revisions indicator |
| 6 | `country_capital_investment_score` | MATRIX | 0.783 | 宏观与行业 | 2 | 0.14 | -0.52 | -0.03 | DEAD | Country-normalized capital investment measure for the company |
| 7 | `mdl50_bk_fcf_valu` | MATRIX | 0.799 | 持仓与资金流 | 1 | 0.11 | 0.08 | 0.11 | DEAD | Free-cash-flow valuation metric (e.g., FCF yield) |
| 8 | `mdl50_bk_analyst_revisn` | MATRIX | 0.792 | 修正与预期 | 1 | 0.09 | 0.19 | 0.25 | DEAD_STATIC | Indicator of analyst estimate revisions momentum |
| 9 | `mdl50_bk_profitabil_cons` | MATRIX | 0.755 | 盈利与财务 | 3 | 0.08 | 0.33 | 0.33 | DEAD | Measure of profitability consistency or persistence over time |
| 10 | `mdl50_bk_cn_earn_valu` | MATRIX | 0.796 | 盈利与财务 | 2 | -0.41 | -0.56 | -0.39 | DEAD_STATIC | Country-normalized earnings-based valuation measure |
| 11 | `mdl50_bk_earn_valu` | MATRIX | 0.797 | 盈利与财务 | 2 | -0.42 | -0.47 | -0.46 | DEAD_STATIC | Earnings-based valuation metric (e.g., earnings yield) |
| 12 | `aggregate_downside_risk_score_backfill` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Backfill duplicate of the composite downside-risk score |
| 13 | `analyst_count_fy1_forecasts_backfill` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the number of FY1 analyst forecasts value became valid |
| 14 | `analyst_forecast_dispersion_score` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Score indicating the level of disagreement among analyst forecasts. |
| 15 | `analyst_forecast_revision_score_4` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Score ranking stocks by changes in analyst forecasts relative to the universe. |
| 16 | `beta_relative_to_country_backfill` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Beta value of the stock compared to its country index (backfill data). |
| 17 | `beta_relative_to_global_index` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the beta relative to MSCI ACWI ex-US became valid |
| 18 | `capital_investment_score_2` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the capital investment measure became valid |
| 19 | `closing_stock_price` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the stock price value became valid in backfill |
| 20 | `country_capital_investment_score_backfill` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score for recent capital and R&D expenditures within the country (backfill data). |
| 21 | `country_fundamental_growth_score_backfill` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score for earnings and dividend growth within the country (backfill data). |
| 22 | `country_level_analyst_forecast_dispersion_score` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Score indicating analyst forecast dispersion compared to country peers. |
| 23 | `country_level_analyst_forecast_revision_score` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the country-normalized analyst revisions metric became valid |
| 24 | `country_level_earnings_quality_score` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the country-normalized earnings quality metric became valid |
| 25 | `country_level_earnings_valuation_score` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the country-normalized earnings valuation metric became valid |
| 26 | `country_level_enterprise_valuation_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score ranking stocks by operating income yield compared to country peers. |
| 27 | `country_level_external_financing_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the country-neutralized external financing metric became valid |
| 28 | `country_level_financial_leverage_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score indicating the financial leverage of a company relative to country peers. |
| 29 | `country_level_free_cash_flow_valuation_score` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score ranking stocks by free cash flow yield compared to country peers. |
| 30 | `country_level_fundamental_stability_score` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Score measuring the stability of a company's fundamentals compared to country peers. |
| 31 | `country_level_price_volatility_score` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the country-neutralized stock price volatility rank became valid |
| 32 | `country_level_profitability_score` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the country-normalized profitability metric became valid |
| 33 | `country_level_shareholder_yield_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the country-normalized shareholder yield metric became valid |
| 34 | `country_level_stock_price_momentum_score` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the country-neutralized stock price momentum value became valid |
| 35 | `country_profitability_consistency_score_backfill` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score for stability of cash flow return on assets within the country (backfill data). |
| 36 | `debt_equity_ratio_backfill` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the debt-to-equity ratio became valid |
| 37 | `dividend_yield_ratio_4` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backfill module duplicate of dividend_yield |
| 38 | `downside_risk_decile_rank` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Decile ranking of downside risk scores across the entire universe. |
| 39 | `downside_risk_score_change_13w_2` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Backfill duplicate of drai_score_chg_13w (13-week change in downside-risk score) |
| 40 | `earnings_quality_score_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backfill duplicate of earn_qual |
| 41 | `earnings_valuation_score_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the earnings-based valuation metric became valid |
| 42 | `enterprise_valuation_score` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Score ranking stocks by operating income yield relative to the universe. |
| 43 | `external_financing_score_backfill` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score based on recent issuance of debt or equity (backfill data). |
| 44 | `financial_leverage_score_3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score ranking stocks by changes in debt levels relative to the universe. |
| 45 | `five_year_eps_growth_forecast_backfill` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the 5-year EPS growth forecast value became valid |
| 46 | `forward_dividend_yield_ratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the forward dividend yield value became valid |
| 47 | `forward_pe_ratio_trailing` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the float trailing P/E value became valid |
| 48 | `free_cash_flow_yield_score_backfill` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the free-cash-flow valuation metric became valid |
| 49 | `fundamental_growth_score_backfill` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Backfill duplicate of the fundamental growth metric |
| 50 | `fundamental_stability_score_backfill` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the fundamental stability measure became valid |
| 51 | `latest_quarterly_eps_surprise_backfill` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the most recent quarterly EPS surprise value became valid |
| 52 | `mean_daily_trading_volume` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average number of shares traded per day over a specified period. |
| 53 | `pe_ratio_trailing` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the trailing price-to-earnings rank/value became valid (backfill companion) |
| 54 | `price_volatility_score_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the price volatility metric became valid in backfill |
| 55 | `price_volatility_score_backfill` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) for the stock price volatility rank (backfill companion) |
| 56 | `profitability_consistency_score_backfill` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backfill duplicate of the profitability consistency measure |
| 57 | `profitability_level_score_2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backfill duplicate of profitability |
| 58 | `risk_decile_country_rank_backfill` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Backfill duplicate of the downside-risk decile within the country |
| 59 | `risk_decile_sector_rank_backfill` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) for the within-sector DRA decile value (backfill companion) |
| 60 | `risk_score_change_1w_backfill` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Effective date (yyyymmdd) when the 1-week change in downside-risk score became valid |
| 61 | `roe_ratio_backfill` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backfill duplicate of return_on_equity |
| 62 | `shareholder_yield_score_backfill` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Backfill duplicate of shrhldr_yld |
| 63 | `six_month_price_change_backfill` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentage change in stock price over the last six months (backfill data). |
| 64 | `stock_price_momentum_score` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Score ranking stocks by recent price momentum relative to the universe. |
| 65 | `total_market_capitalization_backfill` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Market cap backfill duplicate |
| 66 | `mdl50_bk_average_vol` | MATRIX | 0.819 | 价量与波动 | 0 | — | — | — | UNTESTED | Average daily trading volume |
| 67 | `mdl50_bk_beta_vs_acwi_ex_us` | MATRIX | 0.819 | 风险与质量 | 0 | — | — | — | UNTESTED | Beta relative to the MSCI ACWI ex-US index |
| 68 | `mdl50_bk_dividend_yield_f` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward dividend yield as a continuous float metric |
| 69 | `mdl50_bk_market_cap` | MATRIX | 0.819 | 价量与波动 | 0 | — | — | — | UNTESTED | Market capitalization of the company (price times shares outstanding) |
| 70 | `mdl50_bk_msci_acwi_member` | MATRIX | 0.819 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating MSCI ACWI index membership (1=member, 0=non-member) |
| 71 | `mdl50_bk_msci_eafe_member` | MATRIX | 0.819 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating MSCI EAFE index membership (1=member, 0=non-member) |
| 72 | `mdl50_bk_stock_price` | MATRIX | 0.819 | 价量与波动 | 0 | — | — | — | UNTESTED | Current stock price |
| 73 | `mdl50_bk_pric_volatil` | MATRIX | 0.819 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous stock price volatility measure |
| 74 | `mdl50_bk_debt_to_equity` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Debt-to-equity ratio |
| 75 | `mdl50_bk_trailing_price__f` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing price-to-earnings ratio (floating point) |
| 76 | `mdl50_bk_beta_vs_country` | MATRIX | 0.818 | 宏观与行业 | 0 | — | — | — | UNTESTED | Beta of the stock relative to its country’s market index (higher implies greater sensitivity/risk) |
| 77 | `avg_daily_volume` | MATRIX | 0.816 | 价量与波动 | 0 | — | — | — | UNTESTED | Average daily trading volume in shares |
| 78 | `beta_vs_global_ex_us` | MATRIX | 0.816 | 风险与质量 | 0 | — | — | — | UNTESTED | Stock’s beta relative to the MSCI ACWI ex-US index |
| 79 | `closing_share_price` | MATRIX | 0.816 | 价量与波动 | 0 | — | — | — | UNTESTED | Current share price |
| 80 | `dividend_yield_forecast` | MATRIX | 0.816 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward dividend yield provided as a continuous float |
| 81 | `total_market_capitalization` | MATRIX | 0.816 | 其他 | 0 | — | — | — | UNTESTED | Total market capitalization of the company |
| 82 | `price_volatility_metric` | MATRIX | 0.816 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous measure of the stock’s realized price volatility |
| 83 | `debt_equity_ratio_2` | MATRIX | 0.816 | 盈利与财务 | 0 | — | — | — | UNTESTED | Debt-to-equity ratio |
| 84 | `trailing_pe_ratio_forecast` | MATRIX | 0.815 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted trailing price-to-earnings ratio. |
| 85 | `beta_relative_to_country` | MATRIX | 0.815 | 宏观与行业 | 0 | — | — | — | UNTESTED | Market beta relative to the stock’s country benchmark |
| 86 | `mdl50_bk_num_of_analysts_fy1` | MATRIX | 0.815 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst forecasts for next fiscal year (FY1) |
| 87 | `risk_score_change_1w` | MATRIX | 0.814 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the downside-risk score over the past 1 week |
| 88 | `six_month_price_change` | MATRIX | 0.814 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock price change over the past six months |
| 89 | `analyst_count_fy1_forecasts` | MATRIX | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts providing fiscal year 1 earnings forecasts |
| 90 | `mdl50_bk_drai_score_chg_13w` | MATRIX | 0.809 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the downside-risk score over the past 13 weeks |
| 91 | `mdl50_bk_adr_ticker` | MATRIX | 0.808 | 交易与微观结构 | 0 | — | — | — | UNTESTED | American Depositary Receipt ticker symbol for the stock |
| 92 | `mdl50_bk_company_name` | MATRIX | 0.808 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Company name |
| 93 | `mdl50_bk_dividend_yield` | MATRIX | 0.808 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend yield (dividends per share as a proportion of share price) |
| 94 | `mdl50_bk_exchange_country` | MATRIX | 0.808 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country of the exchange where the security is listed |
| 95 | `mdl50_bk_geographic_region` | MATRIX | 0.808 | 宏观与行业 | 0 | — | — | — | UNTESTED | Geographic region of the issuer |
| 96 | `mdl50_bk_periods` | MATRIX | 0.808 | 其他 | 0 | — | — | — | UNTESTED | period |
| 97 | `mdl50_bk_ticker` | MATRIX | 0.808 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Ticker |
| 98 | `mdl50_bk_trailing_price` | MATRIX | 0.808 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing price-to-earnings ratio (P/E) |
| 99 | `risk_score_change_13w` | MATRIX | 0.807 | 风险与质量 | 0 | — | — | — | UNTESTED | Change in the downside-risk score over the past 13 weeks |
| 100 | `mdl50_bk_analyst_uncertainty` | MATRIX | 0.805 | 修正与预期 | 0 | — | — | — | UNTESTED | High score indicates low forecast dispersion |
| 101 | `mdl50_bk_cn_analyst_uncertainty` | MATRIX | 0.804 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst uncertainty score relative to the country |
| 102 | `mdl50_bk_return_on_equity` | MATRIX | 0.804 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity (ROE) |
| 103 | `mdl50_bk_drai_decile` | MATRIX | 0.801 | 风险与质量 | 0 | — | — | — | UNTESTED | Decile rank of the downside-risk score across the global universe (1=lowest risk, 10=highest) |
| 104 | `mdl50_bk_drai_decile_sector` | MATRIX | 0.801 | 宏观与行业 | 0 | — | — | — | UNTESTED | Decile rank of drai_score within the sector (1=lowest, 10=highest) |
| 105 | `mdl50_bk_drai_score` | MATRIX | 0.801 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite downside-risk score for the security |
| 106 | `mdl50_bk_stk_pric_volatil` | MATRIX | 0.801 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock price volatility measure (typically a ranked/discretized metric) |
| 107 | `mdl50_bk_entrpris_valu` | MATRIX | 0.801 | 宏观与行业 | 0 | — | — | — | UNTESTED | Higher value indicates higher operating income yield |
| 108 | `mdl50_bk_cn_stk_pric_volatil` | MATRIX | 0.801 | 价量与波动 | 0 | — | — | — | UNTESTED | Country-normalized stock price volatility metric |
| 109 | `roe_ratio` | MATRIX | 0.801 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity (ROE) |
| 110 | `mdl50_bk_drai_decile_country` | MATRIX | 0.801 | 宏观与行业 | 0 | — | — | — | UNTESTED | Decile rank of downside-risk score within the country (1=lowest, 10=highest) |
| 111 | `mdl50_bk_cn_entrpris_valu` | MATRIX | 0.801 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-normalized enterprise value metric |
| 112 | `mdl50_bk_leverage` | MATRIX | 0.800 | 其他 | 0 | — | — | — | UNTESTED | Financial leverage ratio |
| 113 | `mdl50_bk_profitability` | MATRIX | 0.800 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability measure where a higher value indicates higher cash flow ROI |
| 114 | `mdl50_bk_earn_qual` | MATRIX | 0.800 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings quality score where higher values indicate higher earnings quality |
| 115 | `mdl50_bk_ext_finance` | MATRIX | 0.800 | 其他 | 0 | — | — | — | UNTESTED | External financing indicator (dependence on or use of outside capital) |
| 116 | `mdl50_bk_cn_profitability` | MATRIX | 0.799 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability score relative to the country |
| 117 | `mdl50_bk_cn_leverage` | MATRIX | 0.799 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-normalized leverage ratio |
| 118 | `mdl50_bk_cn_earn_qual` | MATRIX | 0.799 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings quality score relative to the country |
| 119 | `mdl50_bk_cn_ext_finance` | MATRIX | 0.799 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-normalized external financing dependence metric |
| 120 | `mdl50_bk_dly_rdlhrhs` | MATRIX | 0.799 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shareholder yield (net payout to shareholders via dividends/buybacks minus issuance) |
| 121 | `forecast_dispersion_score` | MATRIX | 0.799 | 修正与预期 | 0 | — | — | — | UNTESTED | Measure of dispersion or uncertainty in analysts’ estimates for the stock |
| 122 | `mdl50_bk_dly_rdlhrhs_nc` | MATRIX | 0.799 | 盈利与财务 | 0 | — | — | — | UNTESTED | Country-normalized shareholder yield (net payout minus issuance, normalized within country) |
| 123 | `country_forecast_dispersion_score` | MATRIX | 0.798 | 修正与预期 | 0 | — | — | — | UNTESTED | Country-normalized measure of analyst estimate uncertainty/dispersion |
| 124 | `price_volatility_score` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Ranked measure of the stock’s realized price volatility |
| 125 | `aggregate_downside_risk_score_2` | MATRIX | 0.795 | 风险与质量 | 0 | — | — | — | UNTESTED | Composite downside-risk score indicating likelihood of underperforming over the next 3–24 months |
| 126 | `risk_decile_sector_rank` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | Decile rank of the downside-risk score within the company’s sector (1=lowest, 10=highest) |
| 127 | `risk_decile_universe_rank` | MATRIX | 0.795 | 风险与质量 | 0 | — | — | — | UNTESTED | Decile rank of overall downside risk across all covered stocks, 1=lowest and 10=highest risk |
| 128 | `operating_income_yield_score` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | Enterprise value–based valuation metric (e.g., EV ratios) |
| 129 | `country_price_volatility_score` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Country-normalized rank of the stock’s realized price volatility |
| 130 | `risk_decile_country_rank` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | Decile rank of the downside-risk score within the country (1=lowest, 10=highest) |
| 131 | `country_operating_income_yield_score` | MATRIX | 0.795 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-normalized enterprise value-based valuation metric |
| 132 | `profitability_level_score` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | Composite profitability metric (e.g., margins or return measures) used in the risk model |
| 133 | `financial_leverage_score_2` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financial leverage measure (e.g., debt burden) |
| 134 | `earnings_quality_score` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings quality indicator (e.g., accruals/quality diagnostics) |
| 135 | `external_financing_score` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | External financing indicator measuring reliance on net equity or debt issuance |
| 136 | `country_profitability_level_score` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability measure normalized within country |
| 137 | `country_financial_leverage_score` | MATRIX | 0.793 | 宏观与行业 | 0 | — | — | — | UNTESTED | Leverage ratio normalized within country |
| 138 | `country_earnings_quality_score` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Country-normalized earnings quality measure |
| 139 | `country_external_financing_score` | MATRIX | 0.793 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-normalized external financing indicator |
| 140 | `free_cash_flow_yield_score` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow valuation metric (e.g., FCF yield) |
| 141 | `shareholder_yield_score` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shareholder yield (net payout to shareholders, e.g., dividends plus buybacks minus issuance) |
| 142 | `country_free_cash_flow_yield_score` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Country-normalized free cash flow valuation metric |
| 143 | `country_shareholder_yield_score` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Country-normalized shareholder yield (dividends and buybacks minus issuance) |
| 144 | `earnings_valuation_score` | MATRIX | 0.791 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings-based valuation factor (e.g., earnings yield), indicating how cheap or expensive the stock is |
| 145 | `country_earnings_valuation_score` | MATRIX | 0.790 | 盈利与财务 | 0 | — | — | — | UNTESTED | Country-normalized earnings-based valuation measure |
| 146 | `mdl50_bk_capital_inv` | MATRIX | 0.790 | 其他 | 0 | — | — | — | UNTESTED | Higher value indicates lower recent capital and R&D expenses |
| 147 | `mdl50_bk_cn_capital_inv` | MATRIX | 0.789 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country-normalized capital investment metric |
| 148 | `analyst_forecast_revision_score_3` | MATRIX | 0.786 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator of analyst estimate revisions momentum |
| 149 | `country_analyst_forecast_revision_score` | MATRIX | 0.785 | 修正与预期 | 0 | — | — | — | UNTESTED | Country-normalized indicator of analyst estimate revisions momentum for the stock |
| 150 | `capital_investment_score` | MATRIX | 0.783 | 宏观与行业 | 0 | — | — | — | UNTESTED | Capital investment metric (e.g., investment rate or capex intensity) |
| 151 | `mdl50_bk_fund_gth` | MATRIX | 0.779 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fundamental growth metric (e.g., EPS or dividend growth) |
| 152 | `mdl50_bk_cn_fund_gth` | MATRIX | 0.778 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Country-normalized fundamental growth |
| 153 | `mdl50_bk_fund_stab` | MATRIX | 0.778 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fundamental stability metric (variability of revenues/cash flows) |
| 154 | `mdl50_bk_cn_fund_stab` | MATRIX | 0.777 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Country-normalized fundamental stability indicator for the company’s financials |
| 155 | `fundamental_growth_score_3` | MATRIX | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fundamental growth metric (e.g., EPS or dividend growth) |
| 156 | `fundamental_stability_score` | MATRIX | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fundamental stability measure (variability of revenues, earnings, or cash flows) |
| 157 | `country_fundamental_growth_score` | MATRIX | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fundamental growth measure (e.g., EPS or dividend growth) normalized within country (country-neutralized) |
| 158 | `country_fundamental_stability_score` | MATRIX | 0.772 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Country-normalized fundamental stability indicator |
| 159 | `mdl50_bk_stk_pric_mom` | MATRIX | 0.755 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock price momentum indicator (scaled metric, e.g., -5 to 5) |
| 160 | `mdl50_bk_cn_stk_pric_mom` | MATRIX | 0.754 | 价量与波动 | 0 | — | — | — | UNTESTED | Country-normalized stock price momentum metric |
| 161 | `price_momentum_score` | MATRIX | 0.750 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock price momentum score (range typically -5 to 5) |
| 162 | `country_price_momentum_score` | MATRIX | 0.749 | 价量与波动 | 0 | — | — | — | UNTESTED | Country-normalized stock price momentum measure |
| 163 | `profitability_consistency_score` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Measure of profitability consistency/persistence across time |
| 164 | `country_profitability_consistency_score` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability consistency measure normalized within country |
| 165 | `mdl50_bk_eps_growth_f_5year` | MATRIX | 0.609 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst forecast for EPS growth over the next five years |
| 166 | `five_year_eps_growth_forecast` | MATRIX | 0.606 | 其他 | 0 | — | — | — | UNTESTED | Forecasted EPS growth over the next five years for the company |
| 167 | `mdl50_bk_recent_eps_sur` | MATRIX | 0.373 | 修正与预期 | 0 | — | — | — | UNUSABLE | Most recent quarterly EPS surprise versus consensus (reported minus expected) |
| 168 | `latest_quarterly_eps_surprise` | MATRIX | 0.370 | 其他 | 0 | — | — | — | UNUSABLE | Most recent quarterly EPS surprise |

## 六、本地回测证据

- 本地累计回测 **23** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `Wjem8dON` | 0.80 | 0.38 | 0.57 | 0.60 | 0.03 | ["LOW_SHARPE | s2_model50_d1 | `quantile(subtract(rank(mdl50_bk_cn_fcf_valu), rank(mdl50_bk_cn_earn_valu)))` |
| `GrOvJ6WQ` | 0.77 | 0.37 | 0.37 | 0.62 | 0.02 | ["LOW_SHARPE | s2_model50_d1 | `quantile(subtract(rank(mdl50_bk_cn_fcf_valu), rank(mdl50_bk_earn_valu)))` |
| `LLZxAYoe` | 0.49 | 0.24 | 1.22 | 0.65 | 0.52 | ["LOW_SHARPE | s2_model50_d1 | `group_zscore(subtract(ts_zscore(mdl50_bk_cn_profitabil_cons, 252), ts_zscore(country_finan` |
| `58gVWZEJ` | 0.46 | 0.18 | 0.92 | 0.48 | 0.73 | ["LOW_SHARPE | s2_model50_d1 | `group_rank(ts_corr(mdl50_bk_drai_score_chg_1w, mean_daily_trading_volume, 22), bucket(rank` |
| `58gVod16` | 0.25 | 0.08 | 0.11 | 0.38 | 0.09 | ["LOW_SHARPE | s2_model50_d1 | `group_zscore(divide(ts_backfill(mdl50_bk_price_change_6m, 22), add(ts_backfill(mdl50_bk_dr` |
| `1YZ5EqNJ` | 0.24 | 0.06 | 0.09 | 0.08 | 0.10 | ["LOW_SHARPE | s2_model50_d1 | `group_rank(ts_corr(mdl50_bk_drai_score_chg_1w, mean_daily_trading_volume, 22), bucket(rank` |
| `zqbzpv31` | 0.15 | 0.03 | 0.18 | 0.33 | 0.01 | ["LOW_SHARPE | s2_model50_d1 | `group_rank(subtract(rank(mdl50_bk_cn_analyst_revisn), rank(analyst_forecast_dispersion_sco` |
| `pw5gOEav` | 0.14 | 0.03 | -0.52 | -0.03 | 0.54 | ["LOW_SHARPE | s2_model50_d1 | `winsorize(subtract(rank(country_capital_investment_score), rank(mdl50_bk_ext_finance)))` |
| `1YZ5ELWQ` | 0.11 | 0.02 | 0.08 | 0.11 | 0.05 | ["LOW_SHARPE | s2_model50_d1 | `rank(group_neutralize(subtract(rank(mdl50_bk_fcf_valu), rank(mdl50_bk_drai_score_chg_13w))` |
| `kqg5lxJ6` | 0.09 | 0.02 | 0.19 | 0.25 | 0.01 | ["LOW_SHARPE | s2_model50_d1 | `group_rank(subtract(rank(mdl50_bk_analyst_revisn), rank(analyst_forecast_dispersion_score)` |
| `YPMdGo3l` | 0.08 | 0.01 | -0.43 | 0.25 | 0.03 | ["LOW_SHARPE | s2_model50_d1 | `group_zscore(subtract(ts_zscore(mdl50_bk_profitabil_cons, 252), ts_zscore(mdl50_bk_cn_leve` |
| `vR2Vg91Q` | 0.04 | 0.00 | 0.01 | 0.05 | 0.05 | ["LOW_SHARPE | s2_model50_d1 | `rank(group_neutralize(subtract(rank(mdl50_bk_cn_fcf_valu), rank(mdl50_bk_drai_score_chg_13` |
| `9qWQ0KE2` | -0.03 | 0.00 | 0.33 | 0.33 | 0.50 | ["LOW_SHARPE | s2_model50_d1 | `group_zscore(subtract(ts_zscore(mdl50_bk_profitabil_cons, 252), ts_zscore(country_financia` |
| `RR6LnwO0` | -0.06 | -0.01 | -0.75 | 0.12 | 0.03 | ["LOW_SHARPE | s2_model50_d1 | `group_zscore(subtract(ts_zscore(mdl50_bk_profitabil_cons, 252), ts_zscore(mdl50_bk_leverag` |
| `omWeM005` | -0.11 | -0.02 | 0.04 | 0.00 | 0.03 | ["LOW_SHARPE | s2_model50_d1 | `group_zscore(subtract(ts_zscore(mdl50_bk_cn_profitabil_cons, 252), ts_zscore(mdl50_bk_cn_l` |

## 七、判死记录（sealed dead_end）

- `EUR-UNTESTED-CHANNEL-FIRSTPROBE-DEAD`（2026-10-02）family=EUR 未测数据集通道（pv106 PV价差 / model50 MODEL估值）：{"id": "EUR-UNTESTED-CHANNEL-FIRSTPROBE-DEAD", "family": "EUR 未测数据集通道（pv106 PV价差 / model50 MODEL估值）", "reason": "2026-10-02 实测：经 S0-tier ∩ TRI ∩ 未测 ∩ 非判死 四重筛选后，EUR 仅剩 pv106 与 model50 两个真空白候选。首波 pv106 11 式 max/S/=0.70、model50 23 式 max/S/=0.80（骨架含 group_rank/group_zscore/ts_zscore/价差对/门控），全 LOW_SHARPE+LOW_FITNESS，candidates=0。与 eur_unlit_tower_strategic_closure 的 Fitness_upper=Sharpe×sqrt(returns/0.

