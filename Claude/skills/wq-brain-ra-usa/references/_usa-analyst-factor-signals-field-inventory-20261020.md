# analyst_factor_signals 全字段清单（USA / TOP3000 / D1）

> 自动生成。数据源 = 平台 `GET /data-fields?dataset.id=analyst_factor_signals&region=USA&delay=1&universe=TOP3000`，
> 按 `limit=50` 翻页至 `count` 耗尽；拉取日 2026-10-20（UTC 2026-10-19）。
> `cov` = coverage，`uc` = userCount，`ac` = alphaCount（平台累计使用度，越低越不拥挤）。
> 机制判读与骨架适配见 `_usa-analyst-factor-signals-field-profile-20261019.md`。

## ⚠ 更正记录（2026-10-20）

首版清单只含 **300** 条，**缺整族 `revenue_*` / `netprofit_*` 与大量科目线**，且首版头部的
「字段总数：300」是错的。根因不是平台上限，而是 MCP `get_datafields` 的**未限定数据集 dump 硬截断**：
`world-quant-brain-mcp/brain_mixin_simulation.py:475` 的 `max_fields = 300`（`capped=True` 提前 break）。
本次改用 `BrainApiClient` 直接翻页（`dataset.id` 限定 + `limit=50`）拿到 **922** 条。
教训：**字段清单的完备性必须核对 `count` 字段**（本次平台返回 `total=922`，旧清单 300 条即 `count != len(rows)`）。

**字段总数：922**（全部 MATRIX 型；按覆盖率降序）

## 家族计数（按 id 前缀粗分）

| 家族 | 字段数 | 家族 | 字段数 |
|---|---:|---|---:|
| `estimate_*` | 322 | `est_q2_*` | 13 |
| `eps_*` | 36 | `quarter2_estimate_*` | 10 |
| `netprofit_*` | 36 | `est_slope_*` | 10 |
| `revenue_*` | 36 | `current_assets_*` | 9 |
| `nav_*` | 36 | `est_y2_*` | 8 |
| `ebitda_*` | 36 | `est_volatility_*` | 7 |
| `ebitdarep_*` | 36 | `est_surprise_*` | 6 |
| `dividend_*` | 33 | `actual_quarter1_*` | 6 |
| `interest_*` | 32 | `forward_*` | 5 |
| `est_y1_*` | 30 | `est_revision_*` | 3 |
| `op_*` | 30 | `est_qttm_*` | 3 |
| `capex_*` | 30 | `est_zscore_*` | 3 |
| `fwd_*` | 29 | `consensus_*` | 2 |
| `est_q1_*` | 23 | `second_fiscal_*` | 2 |
| `cf_operating_*` | 22 | `next_fiscal_*` | 2 |
| `cogs_*` | 22 | `est_trend_*` | 1 |
| `quarter1_estimate_*` | 21 | `act_*` | 1 |
| `actual_q1_*` | 21 |  | |

> `estimate`(322) 与 `est_*` 命名族高度重叠，多为同一底层量的命名变体；做 ATOM 时同数据集不受限，
> 但机制族计数应合并（如 `netprofit_y1_estimate_change_3mo` 与 `fwd_year1_estimate_change_3mo_nprofit` 同族）。

## 机制桶（coverage ≥ 0.85 的可用字段数）

| 机制 | 全部 n | cov≥0.85 n | 备注 |
|---|---:|---:|---|
| skewness | 78 | 29 | 三阶矩；`eps_y1_estimate_skewness` 已交付（S1.83/SUB0.95） |
| asymmetry | 74 | 9 | 与 skewness 近似；批 11 在 EPS 族 SUB 指纹 0.005–0.01，已封 |
| coeff_var | 75 | 12 | 二阶离散；批 11 SUB 指纹 0.24–0.40，已封 |
| qoq_growth | 38 | 11 | 季环比预期增速；`eps_q1_estimate_qoq_growth` 已交付（S2.05） |
| yoy_growth | 24 | 3 | 同比预期增速；未系统挖 |
| revision_magnitude | 26 | 13 | 修正幅度绝对值；与方向性修正不同机制，未系统挖 |
| change_1mo | 22 | 8 | 1 月修正（短窗）；`est_q1_change_1mo_profit` 批 13 三闸 |
| change_3mo | 45 | 24 | 3 月修正（主窗）；`revenue_y1_estimate_change_3mo` 已过 RA、prod 0.7565 |
| surprise | 52 | 12 | 实际−预期；平台 prod 已占满（批 10） |
| zscore | 23 | 2 | 标准化水平；SUB 指纹 0.37–0.40，不达标 |
| trend_slope | 94 | 13 | 趋势斜率；未系统挖 |
| slope | 104 | 14 | 趋势斜率（含 est_slope_*）；未系统挖 |
| sequential | 26 | 1 | 相邻期变化；未系统挖 |
| volatility | 50 | 1 | 预期波动；未系统挖 |
| cagr | 104 | 7 | 复合增速；未系统挖 |
| consensus | 18 | 9 | 一致预期水平；水平类，SUB 弱 |

## 低拥挤候选（cov ≥ 0.85 且 ac ≤ 5），按 cov 降序

| # | 字段 | cov | uc | ac | 描述 |
|---:|---|---:|---:|---:|---|
| 1 | `netprofit_y1_estimate_skewness_alt` | 0.9498 | 1 | 1 | Pearson’s skewness of forecast FY1 net profit estimates |
| 2 | `netprofit_y2_consensus_value` | 0.9498 | 4 | 4 | Forecast FY2 net profit growth |
| 3 | `netprofit_y1_estimate_change_3mo` | 0.9452 | 1 | 1 | 3-month change in the FY1 consensus net profit forecast |
| 4 | `netprofit_y2_estimate_change_3mo` | 0.9452 | 3 | 3 | Three-month change in the consensus forecast for FY2 net profit |
| 5 | `est_y1_skewness_eps` | 0.9432 | 2 | 2 | Skewness of year 1 EPS estimates, indicating asymmetry in forecast distribution. |
| 6 | `est_y2_eps` | 0.9432 | 1 | 3 | Consensus EPS estimate for the second fiscal year ahead. |
| 7 | `forward_year2_estimate_pprofit` | 0.9431 | 2 | 2 | Consensus pretax profit estimate for the second forward year. |
| 8 | `fwd_year1_estimate_skewness_pprofit` | 0.9431 | 3 | 3 | Skewness of the forward year 1 pretax profit estimate distribution. |
| 9 | `estimate_y2_value_ebit` | 0.9396 | 1 | 1 | Analyst consensus estimate for EBIT in year 2. |
| 10 | `fwd_year1_estimate_change_3mo_pprofit` | 0.9381 | 3 | 3 | Change in the forward year 1 pretax profit estimate over the past 3 months. |
| 11 | `fwd_year2_estimate_change_3mo_pprofit` | 0.9381 | 2 | 2 | Change in the forward year 2 pretax profit estimate over the past 3 months. |
| 12 | `est_y2_change_3mo_eps` | 0.9378 | 2 | 2 | Change in year 2 EPS estimate over the past 3 months. |
| 13 | `forward_year2_estimate_nprofit` | 0.9369 | 2 | 2 | Consensus net profit estimate for the second forward year. |
| 14 | `fwd_year1_estimate_skewness_nprofit` | 0.9369 | 2 | 2 | Skewness of the forward year 1 net profit estimate distribution. |
| 15 | `estimate_y1_change_3mo_ebit` | 0.9346 | 2 | 2 | Three-month change in year 1 EBIT estimate. |
| 16 | `estimate_y2_change_3mo_ebit` | 0.9346 | 1 | 1 | Three-month change in year 2 EBIT estimate. |
| 17 | `fwd_year1_estimate_change_3mo_nprofit` | 0.9311 | 0 | 0 | Change in the forward year 1 net profit estimate over the past 3 months. |
| 18 | `fwd_year2_estimate_change_3mo_nprofit` | 0.9311 | 1 | 1 | Change in the forward year 2 net profit estimate over the past 3 months. |
| 19 | `eps_q2_estimate_skewness` | 0.93 | 2 | 2 | Pearson's skewness of the forecast Q2 EPS estimate distribution |
| 20 | `netprofit_y1_consensus_value` | 0.9282 | 4 | 4 | Forecast FY1 net profit growth |
| 21 | `eps_trailing_4q_estimate` | 0.925 | 4 | 5 | Forecast trailing-twelve-month EPS growth |
| 22 | `est_y1_skewness_profit` | 0.9226 | 2 | 2 | Skewness of year 1 profit estimates, indicating asymmetry in forecast distribution. |
| 23 | `est_y2_profit` | 0.9226 | 1 | 1 | Consensus profit estimate for the second fiscal year ahead. |
| 24 | `est_y1_eps` | 0.9191 | 1 | 1 | Consensus EPS estimate for the next fiscal year. |
| 25 | `netprofit_estimate_trend_slope_1yr` | 0.9178 | 2 | 2 | Slope of the 1-year consensus net profit forecast series (quarterly) |
| 26 | `netprofit_q2_estimate_skewness` | 0.9178 | 0 | 0 | Pearson’s skewness of forecast Q2 net profit estimates |
| 27 | `forward_year1_estimate_pprofit` | 0.9177 | 2 | 4 | Consensus pretax profit estimate for the first forward year. |
| 28 | `netprofit_q1_estimate_skewness` | 0.9177 | 2 | 2 | Pearson’s skewness of forecast Q1 net profit estimates |
| 29 | `estimate_y1_value_ebit` | 0.9163 | 0 | 0 | Analyst consensus estimate for EBIT in year 1. |
| 30 | `est_revision_magnitude_profit` | 0.9158 | 4 | 5 | Magnitude of recent revisions in profit estimates. |
| 31 | `est_y1_change_3mo_profit` | 0.9158 | 4 | 4 | Change in year 1 profit estimate over the past 3 months. |
| 32 | `est_y2_change_3mo_profit` | 0.9158 | 2 | 2 | Change in year 2 profit estimate over the past 3 months. |
| 33 | `netprofit_q1_estimate_change_1mo` | 0.9149 | 3 | 4 | 1-month change in the Q1 consensus net profit forecast |
| 34 | `forward_year1_estimate_nprofit` | 0.9129 | 0 | 0 | Consensus net profit estimate for the first forward year. |
| 35 | `netprofit_trailing_4q_estimate_alt` | 0.9108 | 3 | 3 | Forecast trailing-twelve-month growth in net profit |
| 36 | `est_q1_skewness_eps` | 0.9099 | 2 | 2 | Skewness of EPS estimates for the most recent quarter, indicating asymmetry in forecast distribution. |
| 37 | `estimate_q2_skewness_eps_reported` | 0.9098 | 0 | 0 | Skewness of the Q2 reported EPS estimate distribution. |
| 38 | `revenue_y1_consensus_value` | 0.9082 | 4 | 4 | Forecast growth for FY1 revenue |
| 39 | `estimate_q1_change_1mo_eps_reported` | 0.9073 | 3 | 5 | Change in Q1 reported EPS estimate over the past month. |
| 40 | `revenue_q2_estimate_skewness` | 0.906 | 1 | 1 | Pearson's skewness of the analyst forecast distribution for fiscal Q2 revenue |
| 41 | `revenue_q1_estimate_skewness` | 0.9052 | 1 | 1 | Pearson's skewness of the analyst forecast distribution for fiscal Q1 revenue |
| 42 | `revenue_trailing_4q_estimate` | 0.9049 | 1 | 1 | Trailing-twelve-month forecast revenue growth |
| 43 | `est_qttm_eps` | 0.9041 | 2 | 2 | Trailing twelve month EPS estimate based on quarterly data. |
| 44 | `revenue_surprise_stddev` | 0.9031 | 4 | 5 | Standard deviation of revenue surprise |
| 45 | `nav_estimate_year1_skewness` | 0.8992 | 1 | 1 | Skewness of analyst net asset value estimates for the next fiscal year. |
| 46 | `nav_estimate_year2_consensus` | 0.8992 | 0 | 0 | Consensus analyst estimate for net asset value in the second forecast year. |
| 47 | `netprofit_y2_estimate_coeff_var` | 0.8981 | 2 | 2 | Coefficient of variation of FY2 net profit estimates from analysts |
| 48 | `netprofit_actual_q1_qoq_growth` | 0.8967 | 3 | 3 | Actual quarter-over-quarter growth for Q1 net profit |
| 49 | `estimate_trend_slope1_ebit` | 0.8965 | 2 | 2 | First slope coefficient from trend analysis of EBIT estimates. |
| 50 | `estimate_q1_skewness_ebit` | 0.8964 | 2 | 2 | Skewness of analyst estimates for EBIT in the first quarter forecast. |
| 51 | `estimate_q2_skewness_ebit` | 0.8964 | 0 | 0 | Skewness of analyst estimates for EBIT in the second quarter forecast. |
| 52 | `revenue_q1_estimate_qoq_growth` | 0.8961 | 4 | 4 | Forecast Q1 revenue growth quarter-over-quarter |
| 53 | `est_y1_profit` | 0.8954 | 0 | 0 | Consensus profit estimate for the next fiscal year. |
| 54 | `netprofit_y1_estimate_asymmetry` | 0.8954 | 2 | 2 | Asymmetry of forecast FY1 net profit estimate distribution |
| 55 | `netprofit_y1_estimate_volatility_adj_1yr` | 0.8954 | 0 | 0 | Coefficient of variation (standard deviation divided by mean) of analyst FY1 net profit estimates |
| 56 | `estimate_trend_slope_1yr_nprofit` | 0.8945 | 1 | 1 | Slope of the net profit estimate trend over the past year. |
| 57 | `quarter1_estimate_skewness_nprofit` | 0.8945 | 0 | 0 | Skewness of the consensus estimate distribution for next quarter's net profit. |
| 58 | `quarter2_estimate_skewness_nprofit` | 0.8944 | 1 | 1 | Skewness of the consensus estimate distribution for the second upcoming quarter's net profit. |
| 59 | `estimate_q1_change_1mo_ebit` | 0.8934 | 1 | 1 | One-month change in first quarter EBIT estimate. |
| 60 | `netprofit_surprise_stddev` | 0.8923 | 2 | 2 | Standard deviation of historical net profit surprises (actual minus consensus). |
| 61 | `revenue_y1_estimate_asymmetry` | 0.8923 | 2 | 3 | Asymmetry measure of the forecast FY1 revenue estimate distribution from analysts |
| 62 | `revenue_y1_estimate_coeff_var` | 0.8923 | 1 | 1 | Coefficient of variation (std/mean) of FY1 revenue estimates |
| 63 | `quarter1_estimate_change_1mo_nprofit` | 0.8908 | 2 | 2 | Change in the consensus net profit estimate for the next quarter over the past month. |
| 64 | `nav_estimate_revision_magnitude` | 0.8901 | 0 | 0 | Magnitude of recent analyst revisions to net asset value estimates. |
| 65 | `nav_estimate_year1_change_3mo` | 0.8901 | 0 | 0 | Change in the next fiscal year's net asset value estimate over the past 3 months. |
| 66 | `nav_estimate_year2_change_3mo` | 0.8901 | 0 | 0 | Change in the second forecast year's net asset value estimate over the past 3 months. |
| 67 | `estimate_trailing_12mo_ebit` | 0.8877 | 0 | 0 | Trailing twelve-month EBIT estimate. |
| 68 | `estimate_q1_qoq_change_ebit` | 0.8876 | 0 | 0 | Quarter-over-quarter change in EBIT estimate for the first quarter. |
| 69 | `estimate_trend_slope_1yr_pprofit` | 0.8875 | 0 | 0 | Slope of the pretax profit estimate trend over the past year. |
| 70 | `quarter1_estimate_skewness_pprofit` | 0.8875 | 0 | 0 | Skewness of the consensus pretax profit estimate distribution for the next quarter. |
| 71 | `quarter2_estimate_qoq_change_pprofit` | 0.8875 | 1 | 1 | Quarter-over-quarter change in the consensus pretax profit estimate for the second upcoming quarter. |
| 72 | `quarter2_estimate_skewness_pprofit` | 0.8875 | 0 | 0 | Skewness of the consensus pretax profit estimate distribution for the second upcoming quarter. |
| 73 | `netprofit_surprise_mean_diff` | 0.887 | 1 | 1 | Difference in net profit surprise between Q1 and Q2 (Q1 minus Q2) |
| 74 | `estimate_trailing_twelve_months` | 0.8859 | 0 | 0 | Consensus estimate for the trailing twelve month period. |
| 75 | `quarter1_estimate_qoq_change_nprofit` | 0.8859 | 0 | 0 | Quarter-over-quarter change in the consensus net profit estimate for the next quarter. |
| 76 | `est_surprise_stddev_eps` | 0.8852 | 1 | 1 | Standard deviation of EPS estimate surprises, indicating variability in forecast errors. |
| 77 | `consensus_next_fiscal_year_interest_expense` | 0.885 | 1 | 1 | Consensus mean estimate for interest expense in the next fiscal year. |
| 78 | `interest_expense_y1_skewness` | 0.885 | 0 | 0 | Skewness of analyst estimates for interest expense in the current fiscal year. |
| 79 | `quarter1_estimate_change_1mo_pprofit` | 0.8847 | 0 | 0 | Change in the consensus pretax profit estimate for the next quarter over the past month. |
| 80 | `revenue_actual_q1_qoq_growth` | 0.8847 | 1 | 1 | Actual Q1 revenue growth quarter over quarter |
| 81 | `eps_q1_estimate_asymmetry` | 0.8833 | 4 | 4 | Asymmetry of the distribution of consensus Q1 EPS estimates |
| 82 | `est_surprise_diff_eps` | 0.8812 | 1 | 1 | Difference between actual and estimated EPS, representing the forecast error. |
| 83 | `eps_estimate_trend_slope_2yr` | 0.878 | 3 | 3 | Slope of the combined consensus forecast and actual EPS series (quarterly) |
| 84 | `interest_expense_revision_magnitude` | 0.878 | 0 | 0 | Magnitude of recent analyst estimate revisions for interest expense. |
| 85 | `eps_q2_estimate_asymmetry` | 0.8779 | 0 | 0 | Asymmetry measure of the distribution of Q2 EPS forecasts |
| 86 | `eps_q2_estimate_coeff_var` | 0.8779 | 1 | 1 | Coefficient of variation (std/mean) of Q2 EPS estimates |
| 87 | `eps_estimate_zscore` | 0.8775 | 2 | 2 | Standardized EPS surprise z-score for Q1 |
| 88 | `estimate_trailing_twelve_months_pprofit` | 0.8774 | 1 | 1 | Consensus pretax profit estimate for the trailing twelve month period. |
| 89 | `quarter1_estimate_qoq_change_pprofit` | 0.8773 | 0 | 0 | Quarter-over-quarter change in the consensus pretax profit estimate for the next quarter. |
| 90 | `interest_expense_y1_change_3mo` | 0.877 | 2 | 2 | Change in current fiscal year interest expense estimate over the past three months. |
| 91 | `interest_expense_y2_change_3mo` | 0.8732 | 2 | 2 | Change in next fiscal year interest expense estimate over the past three months. |
| 92 | `estimate_y2_coeffvar_eps_reported` | 0.8714 | 0 | 0 | Coefficient of variation for year 2 reported EPS estimates. |
| 93 | `netprofit_y1_cagr_2yr_alt` | 0.8695 | 1 | 1 | Forecast FY1 net profit growth CAGR measured over 2 years |
| 94 | `actual_quarter1_qoq_growth_nprofit` | 0.8679 | 5 | 5 | Quarter-over-quarter growth in actual reported net profit for the most recent quarter. |
| 95 | `est_y1_asymmetry_eps` | 0.8676 | 0 | 0 | Asymmetry measure of year 1 EPS estimates. |
| 96 | `estimate_y1_coeffvar_eps_reported` | 0.8676 | 0 | 0 | Coefficient of variation for year 1 reported EPS estimates. |
| 97 | `est_q1_skewness_profit` | 0.8661 | 2 | 3 | Skewness of profit estimates for the most recent quarter, indicating asymmetry in forecast distribution. |
| 98 | `est_q2_qoq_profit` | 0.8661 | 4 | 5 | Quarter-over-quarter change in profit estimate for the second quarter. |
| 99 | `est_q2_skewness_profit` | 0.8661 | 0 | 0 | Skewness of profit estimates for the second quarter, indicating asymmetry in forecast distribution. |
| 100 | `est_slope_1yr_profit` | 0.8661 | 1 | 1 | Slope of profit estimates over the last year, indicating short-term trend direction. |
| 101 | `nav_estimate_year1_consensus` | 0.8661 | 1 | 1 | Consensus analyst estimate for net asset value in the next fiscal year. |
| 102 | `estimate_y1_skewness_depr_amort` | 0.8651 | 0 | 0 | Skewness of the year 1 depreciation and amortization estimate distribution. |
| 103 | `estimate_y2_depr_amort` | 0.8651 | 0 | 0 | Consensus estimate for year 2 depreciation and amortization. |
| 104 | `estimate_surprise_stddev_ebit` | 0.8644 | 0 | 0 | Standard deviation of the difference between actual and forecasted EBIT. |
| 105 | `estimate_surprise_standard_deviation` | 0.8638 | 1 | 1 | Standard deviation of the difference between actuals and consensus estimates. |
| 106 | `fwd_year2_estimate_coeff_var_pprofit` | 0.8638 | 1 | 1 | Coefficient of variation for the forward year 2 pretax profit estimate. |
| 107 | `ebitda_estimate_year2` | 0.8633 | 1 | 1 | Consensus EBITDA estimate for the second forecast year. |
| 108 | `ebitda_y1_estimate_skewness` | 0.8633 | 0 | 0 | Skewness of the distribution of consensus EBITDA estimates for year one. |
| 109 | `estimate_y1_skewness_mktblsec` | 0.8629 | 0 | 0 | Skewness of year 1 marketable securities analyst estimates. |
| 110 | `estimate_y2_value_mktblsec` | 0.8629 | 0 | 0 | Analyst consensus estimate for marketable securities in year 2. |
| 111 | `est_q1_change_1mo_profit` | 0.8621 | 0 | 0 | Change in profit estimate for the most recent quarter over the past month. |
| 112 | `eps_actual_q1_yoy_growth` | 0.8605 | 1 | 2 | Actual EPS growth for fiscal Q1, year-over-year |
| 113 | `estimate_surprise_difference_nprofit` | 0.8596 | 2 | 3 | Difference between actual net profit and consensus estimate for the period. |
| 114 | `revenue_estimate_trend_slope_2yr` | 0.8588 | 3 | 3 | Slope of the linear trend in consensus revenue estimates over the past 2 years. |
| 115 | `fwd_year1_estimate_cagr_2yr_pprofit` | 0.8581 | 0 | 0 | Compound annual growth rate of the forward year 1 pretax profit estimate over the last 2 years. |
| 116 | `estimate_revision_magnitude_depr_amort` | 0.8576 | 0 | 0 | Magnitude of recent revisions in depreciation and amortization estimates. |
| 117 | `ebitda_y1_estimate_change_3m` | 0.8572 | 1 | 1 | Change in consensus EBITDA estimate for year one over the past three months. |
| 118 | `ebitda_y2_estimate_change_3m` | 0.8572 | 1 | 1 | Change in consensus EBITDA estimate for year two over the past three months. |
| 119 | `estimate_y1_change_3mo_depr_amort` | 0.8572 | 0 | 0 | Change in year 1 depreciation and amortization estimate over the past three months. |
| 120 | `estimate_y2_change_3mo_depr_amort` | 0.8568 | 0 | 0 | Change in year 2 depreciation and amortization estimate over the past three months. |
| 121 | `eps_q1_estimate_sequential` | 0.8564 | 2 | 2 | Difference between sequentially forecast and actual EPS growth for Q1 |
| 122 | `fwd_year1_estimate_asymmetry_pprofit` | 0.8561 | 0 | 0 | Asymmetry (third moment) of the forward year 1 pretax profit estimate distribution. |
| 123 | `fwd_year1_estimate_coeff_var_pprofit` | 0.8561 | 1 | 1 | Coefficient of variation for the forward year 1 pretax profit estimate. |
| 124 | `estimate_revision_magnitude_mktblsec` | 0.856 | 1 | 1 | Magnitude of recent revisions in marketable securities estimates. |
| 125 | `estimate_y1_cagr2_ebit` | 0.856 | 0 | 0 | Two-year compound annual growth rate for year 1 EBIT estimate. |
| 126 | `estimate_y1_change_3mo_mktblsec` | 0.856 | 0 | 0 | Three-month change in year 1 marketable securities estimate. |
| 127 | `revenue_q1_estimate_asymmetry` | 0.856 | 3 | 3 | Asymmetry measure of the analyst forecast distribution for fiscal Q1 revenue |
| 128 | `revenue_q1_estimate_coeff_var` | 0.856 | 1 | 1 | Coefficient of variation (std/mean) of Q1 revenue estimates |
| 129 | `est_q1_qoq_profit` | 0.8559 | 2 | 2 | Quarter-over-quarter change in profit estimate for the most recent quarter. |
| 130 | `est_qttm_profit` | 0.8559 | 2 | 2 | Trailing twelve month profit estimate based on quarterly data. |
| 131 | `estimate_y2_change_3mo_mktblsec` | 0.8559 | 0 | 0 | Three-month change in year 2 marketable securities estimate. |
| 132 | `revenue_estimate_trend_slope_3yr` | 0.8537 | 4 | 5 | Slope of the linear trend in consensus revenue estimates over the past 3 years. |
| 133 | `revenue_y1_cagr_2yr` | 0.8533 | 1 | 1 | Forecast compound annual growth rate to FY1 revenue measured over a 2-year horizon |
| 134 | `netprofit_estimate_trend_slope_2yr` | 0.8532 | 1 | 1 | Slope of the combined series of consensus net profit forecasts and actuals (quarterly) |
| 135 | `netprofit_estimate_trend_slope_3yr` | 0.8532 | 0 | 0 | Slope of the current actual 1-year quarterly net profit series |
| 136 | `estimate_y2_coeffvar_ebit` | 0.8528 | 0 | 0 | Coefficient of variation for year 2 EBIT estimate. |
| 137 | `fwd_year1_estimate_cagr_2yr` | 0.8525 | 1 | 1 | Compound annual growth rate of the forward year 1 estimate over the last 2 years. |
| 138 | `estimate_surprise_standard_deviation_pprofit` | 0.8517 | 1 | 1 | Standard deviation of the difference between actuals and consensus pretax profit estimates. |
| 139 | `fwd_year2_estimate_coeff_var_nprofit` | 0.8517 | 0 | 0 | Coefficient of variation for the forward year 2 net profit estimate. |
| 140 | `fwd_year1_estimate_asymmetry_nprofit` | 0.8504 | 0 | 0 | Asymmetry (third moment) of the forward year 1 net profit estimate distribution. |
| 141 | `fwd_year1_estimate_coeff_var_nprofit` | 0.8504 | 3 | 3 | Coefficient of variation for the forward year 1 net profit estimate. |

## 全字段表（922 条，按覆盖率降序）

| # | 字段 | cov | uc | ac | 描述 |
|---:|---|---:|---:|---:|---|
| 1 | `eps_y1_estimate_skewness` | 0.9521 | 12 | 13 | Pearson skewness of the FY1 EPS forecast distribution |
| 2 | `eps_y2_consensus_value` | 0.9521 | 4 | 9 | Forecast FY2 EPS growth rate |
| 3 | `netprofit_y1_estimate_skewness_alt` | 0.9498 | 1 | 1 | Pearson’s skewness of forecast FY1 net profit estimates |
| 4 | `netprofit_y2_consensus_value` | 0.9498 | 4 | 4 | Forecast FY2 net profit growth |
| 5 | `eps_revision_magnitude` | 0.9477 | 52 | 79 | Scaled magnitude of revisions to FY1 EPS (Street revision magnitude) |
| 6 | `eps_y1_estimate_change_3mo` | 0.9477 | 28 | 43 | Change in consensus FY1 EPS forecast over the past 3 months |
| 7 | `eps_y2_estimate_change_3mo` | 0.9477 | 12 | 23 | Change in consensus FY2 EPS forecast over the past 3 months |
| 8 | `netprofit_revision_magnitude` | 0.9452 | 29 | 42 | Revision magnitude of median FY1 net profit estimates (Street revision magnitude) |
| 9 | `netprofit_y1_estimate_change_3mo` | 0.9452 | 1 | 1 | 3-month change in the FY1 consensus net profit forecast |
| 10 | `netprofit_y2_estimate_change_3mo` | 0.9452 | 3 | 3 | Three-month change in the consensus forecast for FY2 net profit |
| 11 | `est_y1_skewness_eps` | 0.9432 | 2 | 2 | Skewness of year 1 EPS estimates, indicating asymmetry in forecast distribution. |
| 12 | `est_y2_eps` | 0.9432 | 1 | 3 | Consensus EPS estimate for the second fiscal year ahead. |
| 13 | `forward_year2_estimate_pprofit` | 0.9431 | 2 | 2 | Consensus pretax profit estimate for the second forward year. |
| 14 | `fwd_year1_estimate_skewness_pprofit` | 0.9431 | 3 | 3 | Skewness of the forward year 1 pretax profit estimate distribution. |
| 15 | `estimate_y1_skewness_ebit` | 0.9396 | 6 | 7 | Skewness of year 1 EBIT analyst estimates. |
| 16 | `estimate_y2_value_ebit` | 0.9396 | 1 | 1 | Analyst consensus estimate for EBIT in year 2. |
| 17 | `estimate_revision_magnitude_pprofit` | 0.9381 | 7 | 17 | Magnitude of recent revisions in the consensus pretax profit estimate. |
| 18 | `fwd_year1_estimate_change_3mo_pprofit` | 0.9381 | 3 | 3 | Change in the forward year 1 pretax profit estimate over the past 3 months. |
| 19 | `fwd_year2_estimate_change_3mo_pprofit` | 0.9381 | 2 | 2 | Change in the forward year 2 pretax profit estimate over the past 3 months. |
| 20 | `est_revision_magnitude_eps` | 0.9378 | 13 | 13 | Magnitude of recent revisions in EPS estimates. |
| 21 | `est_y1_change_3mo_eps` | 0.9378 | 7 | 8 | Change in year 1 EPS estimate over the past 3 months. |
| 22 | `est_y2_change_3mo_eps` | 0.9378 | 2 | 2 | Change in year 2 EPS estimate over the past 3 months. |
| 23 | `forward_year2_estimate_nprofit` | 0.9369 | 2 | 2 | Consensus net profit estimate for the second forward year. |
| 24 | `fwd_year1_estimate_skewness_nprofit` | 0.9369 | 2 | 2 | Skewness of the forward year 1 net profit estimate distribution. |
| 25 | `revenue_y2_estimate_change_3mo` | 0.9354 | 8 | 8 | Change in consensus forecast for FY2 revenue over the past 3 months |
| 26 | `estimate_revision_magnitude_ebit` | 0.9346 | 5 | 7 | Magnitude of recent revisions in EBIT estimates. |
| 27 | `estimate_y1_change_3mo_ebit` | 0.9346 | 2 | 2 | Three-month change in year 1 EBIT estimate. |
| 28 | `estimate_y2_change_3mo_ebit` | 0.9346 | 1 | 1 | Three-month change in year 2 EBIT estimate. |
| 29 | `revenue_y1_estimate_skewness` | 0.9335 | 6 | 6 | Pearson's skewness of the FY1 revenue forecast distribution |
| 30 | `revenue_y2_consensus_value` | 0.9335 | 6 | 6 | Forecast growth for FY2 revenue |
| 31 | `estimate_revision_magnitude_nprofit` | 0.9311 | 12 | 19 | Magnitude of recent revisions in the consensus net profit estimate. |
| 32 | `fwd_year1_estimate_change_3mo_nprofit` | 0.9311 | 0 | 0 | Change in the forward year 1 net profit estimate over the past 3 months. |
| 33 | `fwd_year2_estimate_change_3mo_nprofit` | 0.9311 | 1 | 1 | Change in the forward year 2 net profit estimate over the past 3 months. |
| 34 | `eps_y1_consensus_value` | 0.9307 | 14 | 16 | Forecast FY1 EPS growth rate |
| 35 | `eps_estimate_trend_slope_1yr` | 0.9302 | 8 | 8 | Slope of the 1-year consensus EPS forecast time series (quarterly) |
| 36 | `eps_q1_estimate_skewness` | 0.9301 | 7 | 8 | Pearson skewness of the Q1 EPS forecast distribution |
| 37 | `revenue_y1_estimate_change_3mo` | 0.9301 | 9 | 10 | Change in FY1 revenue consensus forecast over the past 3 months |
| 38 | `eps_q2_estimate_qoq_growth` | 0.93 | 52 | 81 | Forecast Q2 EPS growth quarter over quarter |
| 39 | `eps_q2_estimate_skewness` | 0.93 | 2 | 2 | Pearson's skewness of the forecast Q2 EPS estimate distribution |
| 40 | `revenue_revision_magnitude` | 0.9292 | 20 | 29 | Scaled revision magnitude of the median FY1 revenue estimate (Street Revision Magnitude) |
| 41 | `eps_q1_estimate_change_1mo` | 0.9283 | 15 | 19 | Change in consensus EPS forecast for fiscal Q1 over the past 1 month |
| 42 | `netprofit_y1_consensus_value` | 0.9282 | 4 | 4 | Forecast FY1 net profit growth |
| 43 | `eps_trailing_4q_estimate` | 0.925 | 4 | 5 | Forecast trailing-twelve-month EPS growth |
| 44 | `eps_q1_estimate_qoq_growth` | 0.9243 | 7 | 10 | Forecast Q1 EPS growth quarter over quarter |
| 45 | `est_y1_skewness_profit` | 0.9226 | 2 | 2 | Skewness of year 1 profit estimates, indicating asymmetry in forecast distribution. |
| 46 | `est_y2_profit` | 0.9226 | 1 | 1 | Consensus profit estimate for the second fiscal year ahead. |
| 47 | `est_y1_eps` | 0.9191 | 1 | 1 | Consensus EPS estimate for the next fiscal year. |
| 48 | `netprofit_estimate_trend_slope_1yr` | 0.9178 | 2 | 2 | Slope of the 1-year consensus net profit forecast series (quarterly) |
| 49 | `netprofit_q2_estimate_skewness` | 0.9178 | 0 | 0 | Pearson’s skewness of forecast Q2 net profit estimates |
| 50 | `forward_year1_estimate_pprofit` | 0.9177 | 2 | 4 | Consensus pretax profit estimate for the first forward year. |
| 51 | `netprofit_q1_estimate_skewness` | 0.9177 | 2 | 2 | Pearson’s skewness of forecast Q1 net profit estimates |
| 52 | `netprofit_q2_estimate_qoq_growth` | 0.9177 | 19 | 27 | Forecast quarter-over-quarter growth for Q2 net profit |
| 53 | `estimate_y1_value_ebit` | 0.9163 | 0 | 0 | Analyst consensus estimate for EBIT in year 1. |
| 54 | `est_revision_magnitude_profit` | 0.9158 | 4 | 5 | Magnitude of recent revisions in profit estimates. |
| 55 | `est_y1_change_3mo_profit` | 0.9158 | 4 | 4 | Change in year 1 profit estimate over the past 3 months. |
| 56 | `est_y2_change_3mo_profit` | 0.9158 | 2 | 2 | Change in year 2 profit estimate over the past 3 months. |
| 57 | `netprofit_q1_estimate_change_1mo` | 0.9149 | 3 | 4 | 1-month change in the Q1 consensus net profit forecast |
| 58 | `eps_actual_q1_qoq_growth` | 0.9131 | 9 | 22 | Actual reported Q1 EPS growth quarter over quarter |
| 59 | `forward_year1_estimate_nprofit` | 0.9129 | 0 | 0 | Consensus net profit estimate for the first forward year. |
| 60 | `netprofit_trailing_4q_estimate_alt` | 0.9108 | 3 | 3 | Forecast trailing-twelve-month growth in net profit |
| 61 | `netprofit_q1_estimate_qoq_growth_alt` | 0.9107 | 5 | 6 | Forecast quarter-over-quarter growth for Q1 net profit |
| 62 | `estimate_trend_slope1_eps_reported` | 0.91 | 7 | 8 | First-order slope of the reported EPS estimate trend, indicating direction of change. |
| 63 | `est_q1_skewness_eps` | 0.9099 | 2 | 2 | Skewness of EPS estimates for the most recent quarter, indicating asymmetry in forecast distribution. |
| 64 | `eps_surprise_stddev` | 0.9098 | 7 | 14 | Standard deviation of EPS surprises |
| 65 | `eps_y2_estimate_coeff_var` | 0.9098 | 12 | 17 | Coefficient of variation (std/mean) of FY2 EPS estimates |
| 66 | `est_q2_qoq_eps` | 0.9098 | 28 | 37 | Quarter-over-quarter change in EPS estimate for the second quarter. |
| 67 | `estimate_q2_skewness_eps_reported` | 0.9098 | 0 | 0 | Skewness of the Q2 reported EPS estimate distribution. |
| 68 | `revenue_estimate_trend_slope_1yr` | 0.909 | 13 | 20 | Slope of the 1-year consensus revenue forecast (quarterly), indicating trend |
| 69 | `eps_y1_estimate_asymmetry` | 0.9087 | 5 | 9 | Asymmetry measure of the distribution of FY1 EPS forecasts |
| 70 | `eps_y1_estimate_coeff_var` | 0.9087 | 14 | 21 | Coefficient of variation (std/mean) of consensus FY1 EPS estimates |
| 71 | `revenue_y1_consensus_value` | 0.9082 | 4 | 4 | Forecast growth for FY1 revenue |
| 72 | `estimate_q1_change_1mo_eps_reported` | 0.9073 | 3 | 5 | Change in Q1 reported EPS estimate over the past month. |
| 73 | `revenue_q2_estimate_skewness` | 0.906 | 1 | 1 | Pearson's skewness of the analyst forecast distribution for fiscal Q2 revenue |
| 74 | `eps_surprise_mean_diff` | 0.9058 | 17 | 28 | Difference in EPS surprise between Q1 and Q2 (Q1 minus Q2) |
| 75 | `revenue_q1_estimate_skewness` | 0.9052 | 1 | 1 | Pearson's skewness of the analyst forecast distribution for fiscal Q1 revenue |
| 76 | `revenue_q2_estimate_qoq_growth` | 0.9052 | 122 | 231 | Forecast Q2 revenue growth quarter-over-quarter |
| 77 | `revenue_trailing_4q_estimate` | 0.9049 | 1 | 1 | Trailing-twelve-month forecast revenue growth |
| 78 | `est_qttm_eps` | 0.9041 | 2 | 2 | Trailing twelve month EPS estimate based on quarterly data. |
| 79 | `est_q1_qoq_eps` | 0.9033 | 7 | 12 | Quarter-over-quarter change in EPS estimate for the most recent quarter. |
| 80 | `revenue_q1_estimate_change_1mo` | 0.9032 | 8 | 11 | Change in consensus forecast for fiscal Q1 revenue over the past 1 month |
| 81 | `revenue_surprise_stddev` | 0.9031 | 4 | 5 | Standard deviation of revenue surprise |
| 82 | `revenue_surprise_mean_diff` | 0.8996 | 4 | 6 | Difference between Q1 and Q2 revenue surprise metrics (Q1 minus Q2) |
| 83 | `nav_estimate_year1_skewness` | 0.8992 | 1 | 1 | Skewness of analyst net asset value estimates for the next fiscal year. |
| 84 | `nav_estimate_year2_consensus` | 0.8992 | 0 | 0 | Consensus analyst estimate for net asset value in the second forecast year. |
| 85 | `netprofit_y2_estimate_coeff_var` | 0.8981 | 2 | 2 | Coefficient of variation of FY2 net profit estimates from analysts |
| 86 | `revenue_y2_estimate_coeff_var` | 0.8974 | 6 | 8 | Coefficient of variation (std/mean) of FY2 revenue estimates |
| 87 | `netprofit_actual_q1_qoq_growth` | 0.8967 | 3 | 3 | Actual quarter-over-quarter growth for Q1 net profit |
| 88 | `estimate_trend_slope1_ebit` | 0.8965 | 2 | 2 | First slope coefficient from trend analysis of EBIT estimates. |
| 89 | `estimate_q1_skewness_ebit` | 0.8964 | 2 | 2 | Skewness of analyst estimates for EBIT in the first quarter forecast. |
| 90 | `estimate_q2_qoq_change_ebit` | 0.8964 | 5 | 6 | Quarter-over-quarter change in EBIT estimate for the second quarter. |
| 91 | `estimate_q2_skewness_ebit` | 0.8964 | 0 | 0 | Skewness of analyst estimates for EBIT in the second quarter forecast. |
| 92 | `revenue_q1_estimate_qoq_growth` | 0.8961 | 4 | 4 | Forecast Q1 revenue growth quarter-over-quarter |
| 93 | `est_y1_profit` | 0.8954 | 0 | 0 | Consensus profit estimate for the next fiscal year. |
| 94 | `netprofit_y1_estimate_asymmetry` | 0.8954 | 2 | 2 | Asymmetry of forecast FY1 net profit estimate distribution |
| 95 | `netprofit_y1_estimate_volatility_adj_1yr` | 0.8954 | 0 | 0 | Coefficient of variation (standard deviation divided by mean) of analyst FY1 net profit estimates |
| 96 | `estimate_trend_slope_1yr_nprofit` | 0.8945 | 1 | 1 | Slope of the net profit estimate trend over the past year. |
| 97 | `quarter1_estimate_skewness_nprofit` | 0.8945 | 0 | 0 | Skewness of the consensus estimate distribution for next quarter's net profit. |
| 98 | `quarter2_estimate_qoq_change_nprofit` | 0.8945 | 14 | 22 | Quarter-over-quarter change in the consensus net profit estimate for the second upcoming quarter. |
| 99 | `quarter2_estimate_skewness_nprofit` | 0.8944 | 1 | 1 | Skewness of the consensus estimate distribution for the second upcoming quarter's net profit. |
| 100 | `estimate_q1_change_1mo_ebit` | 0.8934 | 1 | 1 | One-month change in first quarter EBIT estimate. |
| 101 | `netprofit_surprise_stddev` | 0.8923 | 2 | 2 | Standard deviation of historical net profit surprises (actual minus consensus). |
| 102 | `revenue_y1_estimate_asymmetry` | 0.8923 | 2 | 3 | Asymmetry measure of the forecast FY1 revenue estimate distribution from analysts |
| 103 | `revenue_y1_estimate_coeff_var` | 0.8923 | 1 | 1 | Coefficient of variation (std/mean) of FY1 revenue estimates |
| 104 | `quarter1_estimate_change_1mo_nprofit` | 0.8908 | 2 | 2 | Change in the consensus net profit estimate for the next quarter over the past month. |
| 105 | `nav_estimate_revision_magnitude` | 0.8901 | 0 | 0 | Magnitude of recent analyst revisions to net asset value estimates. |
| 106 | `nav_estimate_year1_change_3mo` | 0.8901 | 0 | 0 | Change in the next fiscal year's net asset value estimate over the past 3 months. |
| 107 | `nav_estimate_year2_change_3mo` | 0.8901 | 0 | 0 | Change in the second forecast year's net asset value estimate over the past 3 months. |
| 108 | `actual_q1_qoq_eps_growth` | 0.8887 | 11 | 11 | Quarter-over-quarter growth rate for actual EPS in the most recent quarter. |
| 109 | `estimate_trailing_12mo_ebit` | 0.8877 | 0 | 0 | Trailing twelve-month EBIT estimate. |
| 110 | `estimate_q1_qoq_change_ebit` | 0.8876 | 0 | 0 | Quarter-over-quarter change in EBIT estimate for the first quarter. |
| 111 | `estimate_trend_slope_1yr_pprofit` | 0.8875 | 0 | 0 | Slope of the pretax profit estimate trend over the past year. |
| 112 | `quarter1_estimate_skewness_pprofit` | 0.8875 | 0 | 0 | Skewness of the consensus pretax profit estimate distribution for the next quarter. |
| 113 | `quarter2_estimate_qoq_change_pprofit` | 0.8875 | 1 | 1 | Quarter-over-quarter change in the consensus pretax profit estimate for the second upcoming quarter. |
| 114 | `quarter2_estimate_skewness_pprofit` | 0.8875 | 0 | 0 | Skewness of the consensus pretax profit estimate distribution for the second upcoming quarter. |
| 115 | `netprofit_surprise_mean_diff` | 0.887 | 1 | 1 | Difference in net profit surprise between Q1 and Q2 (Q1 minus Q2) |
| 116 | `estimate_trailing_twelve_months` | 0.8859 | 0 | 0 | Consensus estimate for the trailing twelve month period. |
| 117 | `quarter1_estimate_qoq_change_nprofit` | 0.8859 | 0 | 0 | Quarter-over-quarter change in the consensus net profit estimate for the next quarter. |
| 118 | `est_surprise_stddev_eps` | 0.8852 | 1 | 1 | Standard deviation of EPS estimate surprises, indicating variability in forecast errors. |
| 119 | `consensus_next_fiscal_year_interest_expense` | 0.885 | 1 | 1 | Consensus mean estimate for interest expense in the next fiscal year. |
| 120 | `interest_expense_y1_skewness` | 0.885 | 0 | 0 | Skewness of analyst estimates for interest expense in the current fiscal year. |
| 121 | `quarter1_estimate_change_1mo_pprofit` | 0.8847 | 0 | 0 | Change in the consensus pretax profit estimate for the next quarter over the past month. |
| 122 | `revenue_actual_q1_qoq_growth` | 0.8847 | 1 | 1 | Actual Q1 revenue growth quarter over quarter |
| 123 | `eps_q1_estimate_asymmetry` | 0.8833 | 4 | 4 | Asymmetry of the distribution of consensus Q1 EPS estimates |
| 124 | `eps_q1_estimate_coeff_var` | 0.8833 | 43 | 56 | Coefficient of variation of Q1 EPS consensus estimates |
| 125 | `est_surprise_diff_eps` | 0.8812 | 1 | 1 | Difference between actual and estimated EPS, representing the forecast error. |
| 126 | `eps_estimate_trend_slope_2yr` | 0.878 | 3 | 3 | Slope of the combined consensus forecast and actual EPS series (quarterly) |
| 127 | `eps_estimate_trend_slope_3yr` | 0.878 | 8 | 15 | Slope of the current actual EPS series over the past year (quarterly) |
| 128 | `interest_expense_revision_magnitude` | 0.878 | 0 | 0 | Magnitude of recent analyst estimate revisions for interest expense. |
| 129 | `eps_q2_estimate_asymmetry` | 0.8779 | 0 | 0 | Asymmetry measure of the distribution of Q2 EPS forecasts |
| 130 | `eps_q2_estimate_coeff_var` | 0.8779 | 1 | 1 | Coefficient of variation (std/mean) of Q2 EPS estimates |
| 131 | `eps_estimate_zscore` | 0.8775 | 2 | 2 | Standardized EPS surprise z-score for Q1 |
| 132 | `estimate_trailing_twelve_months_pprofit` | 0.8774 | 1 | 1 | Consensus pretax profit estimate for the trailing twelve month period. |
| 133 | `quarter1_estimate_qoq_change_pprofit` | 0.8773 | 0 | 0 | Quarter-over-quarter change in the consensus pretax profit estimate for the next quarter. |
| 134 | `eps_q1_estimate_yoy_growth` | 0.8772 | 16 | 21 | Forecast Q1 EPS growth year over year |
| 135 | `interest_expense_y1_change_3mo` | 0.877 | 2 | 2 | Change in current fiscal year interest expense estimate over the past three months. |
| 136 | `eps_y1_cagr_2yr` | 0.8735 | 6 | 7 | Forecast FY1 EPS growth CAGR over 2 years |
| 137 | `interest_expense_y2_change_3mo` | 0.8732 | 2 | 2 | Change in next fiscal year interest expense estimate over the past three months. |
| 138 | `actual_q1_qoq_change_ebit` | 0.8725 | 11 | 15 | Quarter-over-quarter change in actual EBIT for the first quarter. |
| 139 | `estimate_y2_coeffvar_eps_reported` | 0.8714 | 0 | 0 | Coefficient of variation for year 2 reported EPS estimates. |
| 140 | `netprofit_y1_cagr_2yr_alt` | 0.8695 | 1 | 1 | Forecast FY1 net profit growth CAGR measured over 2 years |
| 141 | `actual_quarter1_qoq_growth_nprofit` | 0.8679 | 5 | 5 | Quarter-over-quarter growth in actual reported net profit for the most recent quarter. |
| 142 | `est_y1_asymmetry_eps` | 0.8676 | 0 | 0 | Asymmetry measure of year 1 EPS estimates. |
| 143 | `estimate_y1_coeffvar_eps_reported` | 0.8676 | 0 | 0 | Coefficient of variation for year 1 reported EPS estimates. |
| 144 | `est_q1_skewness_profit` | 0.8661 | 2 | 3 | Skewness of profit estimates for the most recent quarter, indicating asymmetry in forecast distribution. |
| 145 | `est_q2_qoq_profit` | 0.8661 | 4 | 5 | Quarter-over-quarter change in profit estimate for the second quarter. |
| 146 | `est_q2_skewness_profit` | 0.8661 | 0 | 0 | Skewness of profit estimates for the second quarter, indicating asymmetry in forecast distribution. |
| 147 | `est_slope_1yr_profit` | 0.8661 | 1 | 1 | Slope of profit estimates over the last year, indicating short-term trend direction. |
| 148 | `nav_estimate_year1_consensus` | 0.8661 | 1 | 1 | Consensus analyst estimate for net asset value in the next fiscal year. |
| 149 | `estimate_y1_skewness_depr_amort` | 0.8651 | 0 | 0 | Skewness of the year 1 depreciation and amortization estimate distribution. |
| 150 | `estimate_y2_depr_amort` | 0.8651 | 0 | 0 | Consensus estimate for year 2 depreciation and amortization. |
| 151 | `estimate_surprise_stddev_ebit` | 0.8644 | 0 | 0 | Standard deviation of the difference between actual and forecasted EBIT. |
| 152 | `estimate_surprise_standard_deviation` | 0.8638 | 1 | 1 | Standard deviation of the difference between actuals and consensus estimates. |
| 153 | `fwd_year2_estimate_coeff_var_pprofit` | 0.8638 | 1 | 1 | Coefficient of variation for the forward year 2 pretax profit estimate. |
| 154 | `ebitda_estimate_year2` | 0.8633 | 1 | 1 | Consensus EBITDA estimate for the second forecast year. |
| 155 | `ebitda_y1_estimate_skewness` | 0.8633 | 0 | 0 | Skewness of the distribution of consensus EBITDA estimates for year one. |
| 156 | `estimate_y1_skewness_mktblsec` | 0.8629 | 0 | 0 | Skewness of year 1 marketable securities analyst estimates. |
| 157 | `estimate_y2_value_mktblsec` | 0.8629 | 0 | 0 | Analyst consensus estimate for marketable securities in year 2. |
| 158 | `est_q1_change_1mo_profit` | 0.8621 | 0 | 0 | Change in profit estimate for the most recent quarter over the past month. |
| 159 | `eps_actual_q1_yoy_growth` | 0.8605 | 1 | 2 | Actual EPS growth for fiscal Q1, year-over-year |
| 160 | `actual_quarter1_qoq_growth_pprofit` | 0.8603 | 7 | 11 | Quarter-over-quarter growth in actual reported pretax profit for the most recent quarter. |
| 161 | `estimate_surprise_difference_nprofit` | 0.8596 | 2 | 3 | Difference between actual net profit and consensus estimate for the period. |
| 162 | `est_y1_cagr_2yr_eps` | 0.8595 | 6 | 12 | Compound annual growth rate of year 1 EPS estimate over the last 2 years. |
| 163 | `revenue_estimate_trend_slope_2yr` | 0.8588 | 3 | 3 | Slope of the linear trend in consensus revenue estimates over the past 2 years. |
| 164 | `fwd_year1_estimate_cagr_2yr_pprofit` | 0.8581 | 0 | 0 | Compound annual growth rate of the forward year 1 pretax profit estimate over the last 2 years. |
| 165 | `estimate_revision_magnitude_depr_amort` | 0.8576 | 0 | 0 | Magnitude of recent revisions in depreciation and amortization estimates. |
| 166 | `ebitda_estimate_revision_magnitude` | 0.8572 | 7 | 15 | Magnitude of recent revisions in consensus EBITDA estimates. |
| 167 | `ebitda_y1_estimate_change_3m` | 0.8572 | 1 | 1 | Change in consensus EBITDA estimate for year one over the past three months. |
| 168 | `ebitda_y2_estimate_change_3m` | 0.8572 | 1 | 1 | Change in consensus EBITDA estimate for year two over the past three months. |
| 169 | `estimate_y1_change_3mo_depr_amort` | 0.8572 | 0 | 0 | Change in year 1 depreciation and amortization estimate over the past three months. |
| 170 | `estimate_y2_change_3mo_depr_amort` | 0.8568 | 0 | 0 | Change in year 2 depreciation and amortization estimate over the past three months. |
| 171 | `eps_q1_estimate_sequential` | 0.8564 | 2 | 2 | Difference between sequentially forecast and actual EPS growth for Q1 |
| 172 | `fwd_year1_estimate_asymmetry_pprofit` | 0.8561 | 0 | 0 | Asymmetry (third moment) of the forward year 1 pretax profit estimate distribution. |
| 173 | `fwd_year1_estimate_coeff_var_pprofit` | 0.8561 | 1 | 1 | Coefficient of variation for the forward year 1 pretax profit estimate. |
| 174 | `estimate_revision_magnitude_mktblsec` | 0.856 | 1 | 1 | Magnitude of recent revisions in marketable securities estimates. |
| 175 | `estimate_y1_cagr2_ebit` | 0.856 | 0 | 0 | Two-year compound annual growth rate for year 1 EBIT estimate. |
| 176 | `estimate_y1_change_3mo_mktblsec` | 0.856 | 0 | 0 | Three-month change in year 1 marketable securities estimate. |
| 177 | `revenue_q1_estimate_asymmetry` | 0.856 | 3 | 3 | Asymmetry measure of the analyst forecast distribution for fiscal Q1 revenue |
| 178 | `revenue_q1_estimate_coeff_var` | 0.856 | 1 | 1 | Coefficient of variation (std/mean) of Q1 revenue estimates |
| 179 | `est_q1_qoq_profit` | 0.8559 | 2 | 2 | Quarter-over-quarter change in profit estimate for the most recent quarter. |
| 180 | `est_qttm_profit` | 0.8559 | 2 | 2 | Trailing twelve month profit estimate based on quarterly data. |
| 181 | `estimate_y2_change_3mo_mktblsec` | 0.8559 | 0 | 0 | Three-month change in year 2 marketable securities estimate. |
| 182 | `revenue_estimate_trend_slope_3yr` | 0.8537 | 4 | 5 | Slope of the linear trend in consensus revenue estimates over the past 3 years. |
| 183 | `revenue_y1_cagr_2yr` | 0.8533 | 1 | 1 | Forecast compound annual growth rate to FY1 revenue measured over a 2-year horizon |
| 184 | `netprofit_estimate_trend_slope_2yr` | 0.8532 | 1 | 1 | Slope of the combined series of consensus net profit forecasts and actuals (quarterly) |
| 185 | `netprofit_estimate_trend_slope_3yr` | 0.8532 | 0 | 0 | Slope of the current actual 1-year quarterly net profit series |
| 186 | `netprofit_q1_estimate_yoy_growth` | 0.8531 | 5 | 6 | Forecast year-over-year growth for Q1 net profit |
| 187 | `estimate_y2_coeffvar_ebit` | 0.8528 | 0 | 0 | Coefficient of variation for year 2 EBIT estimate. |
| 188 | `fwd_year1_estimate_cagr_2yr` | 0.8525 | 1 | 1 | Compound annual growth rate of the forward year 1 estimate over the last 2 years. |
| 189 | `estimate_surprise_standard_deviation_pprofit` | 0.8517 | 1 | 1 | Standard deviation of the difference between actuals and consensus pretax profit estimates. |
| 190 | `fwd_year2_estimate_coeff_var_nprofit` | 0.8517 | 0 | 0 | Coefficient of variation for the forward year 2 net profit estimate. |
| 191 | `revenue_estimate_zscore` | 0.8506 | 5 | 18 | Standardized z-score of the fiscal Q1 revenue surprise |
| 192 | `fwd_year1_estimate_asymmetry_nprofit` | 0.8504 | 0 | 0 | Asymmetry (third moment) of the forward year 1 net profit estimate distribution. |
| 193 | `fwd_year1_estimate_coeff_var_nprofit` | 0.8504 | 3 | 3 | Coefficient of variation for the forward year 1 net profit estimate. |
| 194 | `revenue_q2_estimate_asymmetry` | 0.8499 | 0 | 0 | Asymmetry measure of the forecast Q2 revenue estimate distribution from analysts |
| 195 | `revenue_q2_estimate_coeff_var` | 0.8499 | 1 | 1 | Coefficient of variation (std/mean) of Q2 revenue estimates |
| 196 | `revenue_q1_estimate_yoy_growth` | 0.8493 | 4 | 4 | Forecast year-over-year growth for fiscal Q1 revenue |
| 197 | `netprofit_q1_estimate_asymmetry` | 0.8492 | 0 | 0 | Asymmetry of forecast Q1 net profit estimate distribution |
| 198 | `netprofit_q1_estimate_coeff_var` | 0.8492 | 1 | 1 | Coefficient of variation (std/mean) of Q1 consensus net profit estimates |
| 199 | `estimate_surprise_diff_ebit` | 0.8472 | 1 | 1 | Difference between actual and forecasted EBIT values. |
| 200 | `estimate_y1_asymmetry_ebit` | 0.8472 | 6 | 7 | Asymmetry measure of year 1 EBIT analyst estimates. |
| 201 | `estimate_y1_coeffvar_ebit` | 0.8472 | 3 | 3 | Coefficient of variation for year 1 EBIT estimate. |
| 202 | `estimate_y1_depr_amort` | 0.8465 | 0 | 0 | Consensus estimate for year 1 depreciation and amortization. |
| 203 | `est_slope_3yr_eps` | 0.8453 | 1 | 1 | Slope of EPS estimates over the last 3 years, showing medium-term trend direction. |
| 204 | `estimate_trend_slope2_eps_reported` | 0.8453 | 2 | 2 | Second-order slope of the reported EPS estimate trend, indicating acceleration or deceleration. |
| 205 | `est_q1_yoy_eps_growth` | 0.8446 | 18 | 21 | Year-over-year growth rate in EPS estimate for the most recent quarter. |
| 206 | `netprofit_estimate_zscore` | 0.8444 | 0 | 0 | Standardized surprise (z-score) for Q1 net profit versus consensus |
| 207 | `consensus_current_fiscal_year_interest_expense` | 0.8425 | 0 | 0 | Consensus mean estimate for interest expense in the current fiscal year. |
| 208 | `netprofit_q2_estimate_asymmetry` | 0.8397 | 0 | 0 | Asymmetry (difference between mean and median) of second quarter net profit consensus estimates. |
| 209 | `netprofit_q2_estimate_coeff_var` | 0.8397 | 0 | 0 | Coefficient of variation of Q2 net profit estimates from analysts |
| 210 | `op_expense_estimate_y1_skewness` | 0.8397 | 1 | 1 | Skewness of the distribution of next fiscal year operating expense estimates. |
| 211 | `second_fiscal_year_op_expense_consensus` | 0.8397 | 0 | 0 | Consensus operating expense estimate for the second fiscal year ahead. |
| 212 | `ebitda_estimate_year1` | 0.8354 | 3 | 3 | Consensus EBITDA estimate for the first forecast year. |
| 213 | `actual_q1_qoq_profit_growth` | 0.8352 | 5 | 10 | Quarter-over-quarter growth rate for actual profit in the most recent quarter. |
| 214 | `netprofit_actual_q1_yoy_growth` | 0.835 | 1 | 1 | Actual year-over-year growth for Q1 net profit |
| 215 | `netprofit_q1_estimate_sequential` | 0.8349 | 2 | 2 | Sequential value of first quarter net profit consensus estimate (for time series analysis). |
| 216 | `revenue_actual_q1_yoy_growth` | 0.8333 | 1 | 1 | Actual Q1 revenue growth year over year |
| 217 | `est_y1_cagr_2yr_profit` | 0.8314 | 1 | 2 | Compound annual growth rate of year 1 profit estimate over the last 2 years. |
| 218 | `revenue_q1_estimate_sequential` | 0.8313 | 0 | 0 | Difference between sequential forecast and actual revenue growth for Q1 |
| 219 | `op_expense_estimate_revision_magnitude` | 0.8306 | 0 | 0 | Magnitude of recent revisions in operating expense estimates. |
| 220 | `op_expense_estimate_y1_change_3mo` | 0.8306 | 0 | 0 | Change in next fiscal year operating expense estimate over the past 3 months. |
| 221 | `op_expense_estimate_y2_change_3mo` | 0.8304 | 1 | 1 | Change in second fiscal year operating expense estimate over the past 3 months. |
| 222 | `est_q1_asymmetry_eps` | 0.8301 | 2 | 3 | Asymmetry measure of EPS estimates for the most recent quarter. |
| 223 | `estimate_q1_coeffvar_eps_reported` | 0.8301 | 5 | 5 | Coefficient of variation for Q1 reported EPS estimates, measuring relative dispersion. |
| 224 | `est_surprise_stddev_profit` | 0.8294 | 0 | 0 | Standard deviation of profit estimate surprises, indicating variability in forecast errors. |
| 225 | `estimate_trend_slope2_ebit` | 0.8281 | 0 | 0 | Second slope coefficient from trend analysis of EBIT estimates. |
| 226 | `estimate_trend_slope3_ebit` | 0.8281 | 0 | 0 | Third slope coefficient from trend analysis of EBIT estimates. |
| 227 | `estimate_q1_yoy_change_ebit` | 0.828 | 0 | 0 | Year-over-year change in EBIT estimate for the first quarter. |
| 228 | `estimate_surprise_difference_pprofit` | 0.8265 | 0 | 0 | Difference between actual pretax profit and consensus estimate for the period. |
| 229 | `actual_q1_yoy_eps_growth` | 0.8263 | 3 | 3 | Year-over-year growth rate for actual EPS in the most recent quarter. |
| 230 | `est_surprise_diff_profit` | 0.8224 | 1 | 1 | Difference between actual and estimated profit, representing the forecast error. |
| 231 | `estimate_zscore_eps_reported` | 0.8221 | 1 | 1 | Z-score of the consensus reported EPS estimate, measuring deviation from the mean. |
| 232 | `est_q1_sequential_eps` | 0.8217 | 5 | 7 | Sequential change in EPS estimate for the most recent quarter. |
| 233 | `est_q2_asymmetry_eps` | 0.821 | 1 | 1 | Asymmetry measure of EPS estimates for the second quarter. |
| 234 | `est_q2_coeff_var_eps` | 0.821 | 0 | 0 | Coefficient of variation for EPS estimates in the second quarter. |
| 235 | `interest_expense_trend_slope_1yr` | 0.8207 | 0 | 0 | Slope of the linear trend in interest expense estimates over the past year. |
| 236 | `estimate_q2_qoq_change_interestexp` | 0.8186 | 1 | 1 | Quarter-over-quarter change in interest expense estimate for the second quarter. |
| 237 | `interest_expense_q1_skewness` | 0.8186 | 0 | 0 | Skewness of analyst estimates for interest expense in the current quarter. |
| 238 | `interest_expense_q2_skewness` | 0.8179 | 0 | 0 | Skewness of analyst estimates for interest expense in the next quarter. |
| 239 | `estimate_trend_slope_2yr_nprofit` | 0.8164 | 0 | 0 | Slope of the net profit estimate trend over the past 2 years. |
| 240 | `estimate_trend_slope_3yr_nprofit` | 0.8164 | 0 | 0 | Slope of the net profit estimate trend over the past 3 years. |
| 241 | `quarter1_estimate_yoy_change_nprofit` | 0.8164 | 3 | 5 | Year-over-year change in the consensus net profit estimate for the next quarter. |
| 242 | `estimate_trend_slope_2yr_pprofit` | 0.8155 | 0 | 0 | Slope of the pretax profit estimate trend over the past 2 years. |
| 243 | `estimate_trend_slope_3yr_pprofit` | 0.8155 | 0 | 0 | Slope of the pretax profit estimate trend over the past 3 years. |
| 244 | `quarter1_estimate_yoy_change_pprofit` | 0.8155 | 2 | 3 | Year-over-year change in the consensus pretax profit estimate for the next quarter. |
| 245 | `eps_y1_cagr_3yr` | 0.815 | 2 | 2 | Forecast FY1 EPS growth CAGR over 3 years |
| 246 | `interest_expense_trailing_twelve_months_est` | 0.8149 | 1 | 1 | Estimate of interest expense for the trailing twelve months. |
| 247 | `interest_expense_q1_change_1mo` | 0.8142 | 1 | 1 | Change in current quarter interest expense estimate over the past month. |
| 248 | `eps_estimate_trend_slope_4yr` | 0.8122 | 1 | 1 | Slope of the current actual 2-year EPS series (quarterly) |
| 249 | `eps_estimate_volatility_adj_2yr` | 0.8121 | 1 | 3 | Volatility-adjusted 2-year projected EPS growth |
| 250 | `estimate_y1_skewness_book_value_ps` | 0.8121 | 0 | 0 | Skewness of the year 1 book value per share estimate distribution. |
| 251 | `estimate_y2_book_value_ps` | 0.8121 | 0 | 0 | Consensus estimate for year 2 book value per share. |
| 252 | `netprofit_y1_cagr_3yr` | 0.8099 | 1 | 1 | Forecast FY1 net profit growth CAGR measured over 3 years |
| 253 | `actual_q1_yoy_change_ebit` | 0.8091 | 2 | 2 | Year-over-year change in actual EBIT for the first quarter. |
| 254 | `estimate_q1_sequential_ebit` | 0.809 | 1 | 1 | Sequential change in EBIT estimate for the first quarter. |
| 255 | `next_fiscal_year_op_expense_consensus` | 0.8088 | 0 | 0 | Consensus operating expense estimate for the next fiscal year. |
| 256 | `estimate_y1_value_mktblsec` | 0.8066 | 0 | 0 | Analyst consensus estimate for marketable securities in year 1. |
| 257 | `capex_estimate_y1_skewness` | 0.8057 | 2 | 2 | Skewness of the distribution of next fiscal year capital expenditure estimates. |
| 258 | `second_fiscal_year_capex_consensus` | 0.8057 | 1 | 1 | Consensus capital expenditure estimate for the second fiscal year ahead. |
| 259 | `quarter1_estimate_asymmetry_nprofit` | 0.805 | 0 | 0 | Asymmetry (third moment) of the consensus net profit estimate distribution for the next quarter. |
| 260 | `quarter1_estimate_coeff_var_nprofit` | 0.805 | 1 | 1 | Coefficient of variation for the consensus net profit estimate for the next quarter. |
| 261 | `estimate_revision_magnitude_book_value_ps` | 0.8022 | 1 | 1 | Magnitude of recent revisions in book value per share estimates. |
| 262 | `fwd_year1_estimate_change_3mo` | 0.8022 | 1 | 2 | Change in the forward year 1 consensus estimate over the past 3 months. |
| 263 | `estimate_y2_change_3mo_book_value_ps` | 0.8019 | 0 | 0 | Change in year 2 book value per share estimate over the past three months. |
| 264 | `est_y1_cagr_3yr_eps` | 0.7991 | 2 | 4 | Compound annual growth rate of year 1 EPS estimate over the last 3 years. |
| 265 | `estimate_zscore_nprofit` | 0.7988 | 1 | 1 | Z-score of the current net profit estimate relative to its historical mean and standard deviation. |
| 266 | `capex_estimate_revision_magnitude` | 0.7984 | 2 | 2 | Magnitude of recent revisions in capital expenditure estimates. |
| 267 | `capex_estimate_y1_change_3mo` | 0.798 | 2 | 2 | Change in next fiscal year capital expenditure estimate over the past 3 months. |
| 268 | `fwd_year1_estimate_cagr_3yr_pprofit` | 0.7979 | 0 | 0 | Compound annual growth rate of the forward year 1 pretax profit estimate over the last 3 years. |
| 269 | `nav_estimate_cagr2y_year1` | 0.7973 | 0 | 0 | Compound annual growth rate of net asset value estimates over the last 2 years to the next year. |
| 270 | `actual_quarter1_year_on_year_growth` | 0.7971 | 5 | 6 | Year-over-year growth in actual reported value for the most recent quarter. |
| 271 | `capex_y2_estimate_change_3m` | 0.7969 | 1 | 1 | Change in consensus capital expenditure estimate for year two over the past three months. |
| 272 | `quarter1_estimate_sequential_change_nprofit` | 0.7969 | 3 | 6 | Sequential change in the consensus net profit estimate for the next quarter. |
| 273 | `interest_expense_q1_qoq_growth_est` | 0.7967 | 0 | 0 | Quarter-over-quarter growth estimate for interest expense in the current quarter. |
| 274 | `revenue_y1_cagr_3yr` | 0.7967 | 0 | 0 | Forecast compound annual growth rate to FY1 revenue measured over a 3-year horizon |
| 275 | `actual_quarter1_year_on_year_growth_pprofit` | 0.7965 | 2 | 2 | Year-over-year growth in actual reported pretax profit for the most recent quarter. |
| 276 | `quarter1_estimate_sequential_change_pprofit` | 0.7965 | 0 | 0 | Sequential change in the consensus pretax profit estimate for the next quarter. |
| 277 | `cf_operating_estimate_year2_consensus` | 0.7954 | 0 | 0 | Consensus analyst estimate for operating cash flow in the second forecast year. |
| 278 | `estimate_year1_skewness_operating_cashflow` | 0.7954 | 1 | 2 | Skewness of operating cash flow estimates for the first forecast year. |
| 279 | `quarter2_estimate_asymmetry_nprofit` | 0.7939 | 0 | 0 | Asymmetry (third moment) of the consensus net profit estimate distribution for the second upcoming quarter. |
| 280 | `quarter2_estimate_coeff_var_nprofit` | 0.7939 | 0 | 0 | Coefficient of variation for the consensus net profit estimate for the second upcoming quarter. |
| 281 | `estimate_y1_cagr3_ebit` | 0.7938 | 0 | 0 | Three-year compound annual growth rate for year 1 EBIT estimate. |
| 282 | `est_y2_coeff_var_profit` | 0.7936 | 0 | 0 | Coefficient of variation for year 2 profit estimates, measuring relative dispersion. |
| 283 | `revenue_estimate_trend_slope_4yr` | 0.7918 | 1 | 3 | Slope of the current actual 2-year revenue series (quarterly), indicating longer-term trend |
| 284 | `revenue_estimate_volatility_adj_2yr` | 0.7916 | 0 | 0 | Volatility-adjusted 2-year projected revenue growth |
| 285 | `fwd_year1_estimate_cagr_3yr_nprofit` | 0.7911 | 0 | 0 | Compound annual growth rate of the forward year 1 net profit estimate over the last 3 years. |
| 286 | `ebitda_estimate_trend_slope1` | 0.7904 | 2 | 2 | Slope of the trend line for consensus EBITDA estimates over the last period. |
| 287 | `ebitda_q1_estimate_skewness` | 0.7903 | 3 | 3 | Skewness of the distribution of consensus EBITDA estimates for the first quarter. |
| 288 | `ebitda_q2_estimate_qoq_growth` | 0.7903 | 15 | 15 | Quarter-over-quarter growth in consensus EBITDA estimate for the second quarter. |
| 289 | `ebitda_q2_estimate_skewness` | 0.7903 | 0 | 0 | Skewness of the distribution of consensus EBITDA estimates for the second quarter. |
| 290 | `est_y1_asymmetry_profit` | 0.7903 | 1 | 1 | Asymmetry measure of year 1 profit estimates. |
| 291 | `est_y1_coeff_var_profit` | 0.7903 | 1 | 1 | Coefficient of variation for year 1 profit estimates, measuring relative dispersion. |
| 292 | `estimate_year1_skewness_free_cash_flow` | 0.7897 | 0 | 0 | Skewness of free cash flow estimates for the first forecast year. |
| 293 | `estimate_year2_free_cash_flow` | 0.7897 | 1 | 1 | Consensus free cash flow estimate for the second forecast year. |
| 294 | `estimate_q1_asymmetry_ebit` | 0.7868 | 1 | 2 | Asymmetry measure of analyst estimates for EBIT in the first quarter. |
| 295 | `estimate_q1_coeffvar_ebit` | 0.7868 | 3 | 6 | Coefficient of variation for first quarter EBIT estimate. |
| 296 | `ebitda_q1_estimate_change_1m` | 0.7867 | 3 | 3 | Change in consensus EBITDA estimate for the first quarter over the past month. |
| 297 | `cf_operating_estimate_year1_change_3mo` | 0.7864 | 6 | 9 | Change in the next fiscal year's operating cash flow estimate over the past 3 months. |
| 298 | `cf_operating_estimate_year2_change_3mo` | 0.7864 | 0 | 0 | Change in the second forecast year's operating cash flow estimate over the past 3 months. |
| 299 | `estimate_revision_magnitude_operating_cashflow` | 0.7863 | 3 | 8 | Magnitude of recent revisions in operating cash flow estimates. |
| 300 | `netprofit_estimate_trend_slope_4yr_alt` | 0.7812 | 0 | 0 | Slope of the current actual 2-year quarterly net profit series |
| 301 | `netprofit_estimate_volatility_adj_2yr` | 0.7812 | 1 | 1 | Volatility-adjusted projected 2-year growth in net profit |
| 302 | `estimate_revision_magnitude_free_cash_flow` | 0.7802 | 2 | 2 | Magnitude of recent revisions in free cash flow estimates. |
| 303 | `estimate_year1_change_3mo_free_cash_flow` | 0.7802 | 2 | 2 | Change in first forecast year free cash flow estimate over the past three months. |
| 304 | `estimate_year2_change_3mo_free_cash_flow` | 0.7799 | 0 | 0 | Change in second forecast year free cash flow estimate over the past three months. |
| 305 | `estimate_zscore_ebit` | 0.7797 | 0 | 0 | Z-score of EBIT estimate relative to historical mean and standard deviation. |
| 306 | `estimate_q2_asymmetry_ebit` | 0.7796 | 0 | 0 | Asymmetry measure of analyst estimates for EBIT in the second quarter. |
| 307 | `estimate_q2_coeffvar_ebit` | 0.7796 | 1 | 1 | Coefficient of variation for second quarter EBIT estimate. |
| 308 | `est_q1_yoy_profit_growth` | 0.7788 | 1 | 1 | Year-over-year growth rate in profit estimate for the most recent quarter. |
| 309 | `est_slope_2yr_profit` | 0.7788 | 0 | 0 | Slope of profit estimates over the last 2 years, indicating recent trend direction. |
| 310 | `est_slope_3yr_profit` | 0.7788 | 0 | 0 | Slope of profit estimates over the last 3 years, showing medium-term trend direction. |
| 311 | `next_fiscal_year_capex_consensus` | 0.7779 | 0 | 0 | Consensus capital expenditure estimate for the next fiscal year. |
| 312 | `ebitda_estimate_trailing_twelve_months` | 0.7765 | 0 | 0 | Consensus EBITDA estimate for the trailing twelve months period. |
| 313 | `ebitda_q1_estimate_qoq_growth` | 0.7764 | 2 | 2 | Quarter-over-quarter growth in consensus EBITDA estimate for the first quarter. |
| 314 | `estimate_y1_book_value_ps` | 0.7763 | 0 | 0 | Consensus estimate for year 1 book value per share. |
| 315 | `interest_expense_actual_q1_qoq_growth` | 0.7761 | 0 | 0 | Quarter-over-quarter growth in actual reported interest expense for the most recent quarter. |
| 316 | `ebitda_y1_estimate_cagr2` | 0.7759 | 2 | 2 | Two-year compound annual growth rate for consensus EBITDA estimate in year one. |
| 317 | `quarter1_estimate_asymmetry_pprofit` | 0.7729 | 0 | 0 | Asymmetry (third moment) of the consensus pretax profit estimate distribution for the next quarter. |
| 318 | `quarter1_estimate_coeff_var_pprofit` | 0.7729 | 0 | 0 | Coefficient of variation for the consensus pretax profit estimate for the next quarter. |
| 319 | `est_slope_4yr_eps` | 0.7723 | 0 | 0 | Slope of EPS estimates over the last 4 years, showing long-term trend direction. |
| 320 | `est_volatility_adj_2yr_eps` | 0.7723 | 0 | 0 | Volatility of EPS estimates adjusted over a 2-year period. |
| 321 | `interest_expense_surprise_stddev` | 0.7689 | 0 | 0 | Standard deviation of historical surprises for interest expense versus consensus. |
| 322 | `quarter2_estimate_asymmetry_pprofit` | 0.7684 | 0 | 0 | Asymmetry (third moment) of the consensus pretax profit estimate distribution for the second upcoming quarter. |
| 323 | `quarter2_estimate_coeff_var_pprofit` | 0.7684 | 0 | 0 | Coefficient of variation for the consensus pretax profit estimate for the second upcoming quarter. |
| 324 | `est_y1_cagr_3yr_profit` | 0.7667 | 2 | 6 | Compound annual growth rate of year 1 profit estimate over the last 3 years. |
| 325 | `estimate_trend_slope1_depr_amort` | 0.7663 | 1 | 1 | First-order slope of the depreciation and amortization estimate trend. |
| 326 | `estimate_q1_skewness_depr_amort` | 0.7658 | 0 | 0 | Skewness of the Q1 depreciation and amortization estimate distribution. |
| 327 | `estimate_q2_qoq_depr_amort` | 0.7658 | 0 | 0 | Quarter-over-quarter change in Q2 depreciation and amortization estimate. |
| 328 | `estimate_q2_skewness_depr_amort` | 0.7653 | 0 | 0 | Skewness of the Q2 depreciation and amortization estimate distribution. |
| 329 | `estimate_zscore_pprofit` | 0.7628 | 0 | 0 | Z-score of the current pretax profit estimate relative to its historical mean and standard deviation. |
| 330 | `cf_operating_estimate_year1_consensus` | 0.7625 | 1 | 1 | Consensus analyst estimate for operating cash flow in the next fiscal year. |
| 331 | `estimate_qtr_trail12mo_depr_amort` | 0.7615 | 0 | 0 | Trailing twelve-month quarterly depreciation and amortization estimate. |
| 332 | `estimate_q1_qoq_depr_amort` | 0.7607 | 0 | 0 | Quarter-over-quarter change in Q1 depreciation and amortization estimate. |
| 333 | `interest_expense_2yr_cagr_estimate` | 0.7604 | 0 | 0 | Compound annual growth rate of interest expense over the past two years based on estimates. |
| 334 | `estimate_q1_change_1mo_depr_amort` | 0.7603 | 0 | 0 | Change in Q1 depreciation and amortization estimate over the past month. |
| 335 | `ebitda_actual_q1_qoq_growth` | 0.7596 | 2 | 3 | Quarter-over-quarter growth in reported EBITDA for the first quarter. |
| 336 | `estimate_y1_cagr2_depr_amort` | 0.759 | 0 | 0 | Two-year compound annual growth rate for year 1 depreciation and amortization estimate. |
| 337 | `estimate_trend_slope_recent_op_expense` | 0.7588 | 1 | 1 | Slope of the most recent trend line for operating expense estimates. |
| 338 | `op_expense_estimate_q1_skewness` | 0.7587 | 0 | 0 | Skewness of the distribution of current quarter operating expense estimates. |
| 339 | `op_expense_estimate_q2_qoq_growth` | 0.7587 | 3 | 4 | Quarter-over-quarter growth rate in second quarter operating expense estimate. |
| 340 | `op_expense_estimate_q2_skewness` | 0.7587 | 0 | 0 | Skewness of the distribution of second quarter operating expense estimates. |
| 341 | `eps_y1_cagr_4yr` | 0.7582 | 2 | 2 | Forecast FY1 EPS growth CAGR over 4 years |
| 342 | `actual_q1_yoy_profit_growth` | 0.7576 | 3 | 3 | Year-over-year growth rate for actual profit in the most recent quarter. |
| 343 | `est_q1_sequential_profit` | 0.7575 | 0 | 0 | Sequential change in profit estimate for the most recent quarter. |
| 344 | `estimate_year1_free_cash_flow` | 0.7557 | 0 | 0 | Consensus free cash flow estimate for the first forecast year. |
| 345 | `interest_expense_y1_asymmetry` | 0.7548 | 1 | 1 | Asymmetry (difference between mean and median) of interest expense estimates for the current fiscal year. |
| 346 | `interest_expense_y1_coeff_variation` | 0.7548 | 0 | 0 | Coefficient of variation for interest expense estimates in the current fiscal year. |
| 347 | `ebitda_y2_estimate_coeff_var` | 0.7535 | 1 | 1 | Coefficient of variation for consensus EBITDA estimate in year two. |
| 348 | `estimate_trend_slope4_ebit` | 0.7533 | 0 | 0 | Fourth slope coefficient from trend analysis of EBIT estimates. |
| 349 | `estimate_volatility_adj2yr_ebit` | 0.7533 | 0 | 0 | Volatility of EBIT estimates adjusted over a two-year period. |
| 350 | `op_expense_estimate_q1_change_1mo` | 0.7527 | 1 | 3 | Change in current quarter operating expense estimate over the past month. |
| 351 | `netprofit_y1_cagr_4yr` | 0.752 | 0 | 0 | Forecast FY1 net profit growth CAGR measured over 4 years |
| 352 | `eps_estimate_volatility_adj_3yr` | 0.7508 | 0 | 0 | Volatility of consensus EPS estimates over the past 3 years, adjusted for scale. |
| 353 | `ebitda_y1_estimate_asymmetry` | 0.7503 | 0 | 0 | Asymmetry measure of consensus EBITDA estimates for year one. |
| 354 | `ebitda_y1_estimate_coeff_var` | 0.7503 | 0 | 0 | Coefficient of variation for consensus EBITDA estimate in year one. |
| 355 | `interest_expense_y2_coeff_variation` | 0.7499 | 0 | 0 | Coefficient of variation for interest expense estimates in the next fiscal year. |
| 356 | `estimate_y1_skewness_cash_invest` | 0.7463 | 0 | 0 | Skewness of the year 1 cash flow from investing activities estimate distribution. |
| 357 | `estimate_y2_cash_invest` | 0.7463 | 0 | 0 | Consensus estimate for year 2 cash flow from investing activities. |
| 358 | `ebitda_estimate_surprise_stdev` | 0.7455 | 0 | 0 | Standard deviation of the difference between actual and forecasted EBITDA. |
| 359 | `op_expense_estimate_trailing_12mo` | 0.7446 | 1 | 1 | Trailing twelve month operating expense estimate. |
| 360 | `op_expense_estimate_q1_qoq_growth` | 0.7445 | 1 | 1 | Quarter-over-quarter growth rate in current quarter operating expense estimate. |
| 361 | `revenue_y1_cagr_4yr` | 0.7417 | 2 | 2 | Forecast compound annual growth rate to FY1 revenue measured over a 4-year horizon |
| 362 | `est_y1_cagr_4yr_eps` | 0.7411 | 1 | 1 | Compound annual growth rate of year 1 EPS estimate over the last 4 years. |
| 363 | `estimate_trend_slope_4yr_pprofit` | 0.7398 | 0 | 0 | Slope of the pretax profit estimate trend over the past 4 years. |
| 364 | `estimate_volatility_adjusted_2yr_pprofit` | 0.7398 | 0 | 0 | Two-year volatility-adjusted measure of consensus pretax profit estimate changes. |
| 365 | `fwd_year1_estimate_cagr_4yr_pprofit` | 0.7398 | 1 | 1 | Compound annual growth rate of the forward year 1 pretax profit estimate over the last 4 years. |
| 366 | `estimate_trend_slope_4yr_nprofit` | 0.7396 | 0 | 0 | Slope of the net profit estimate trend over the past 4 years. |
| 367 | `estimate_volatility_adjusted_2yr` | 0.7396 | 0 | 0 | Two-year volatility-adjusted measure of consensus estimate changes. |
| 368 | `estimate_year1_skewness_gross_margin` | 0.7383 | 0 | 0 | Skewness of analyst gross margin estimates for the first forecast year. |
| 369 | `estimate_year2_gross_margin` | 0.7383 | 0 | 0 | Consensus gross margin estimate for the second forecast year. |
| 370 | `estimate_revision_magnitude_cash_invest` | 0.7363 | 1 | 1 | Magnitude of recent revisions in cash flow from investing activities estimates. |
| 371 | `estimate_y1_change_3mo_cash_invest` | 0.7359 | 0 | 0 | Change in year 1 cash flow from investing activities estimate over the past three months. |
| 372 | `estimate_y2_change_3mo_cash_invest` | 0.7341 | 0 | 0 | Change in year 2 cash flow from investing activities estimate over the past three months. |
| 373 | `interest_expense_trend_slope_2yr` | 0.7338 | 0 | 0 | Slope of the linear trend in interest expense estimates over the past two years. |
| 374 | `estimate_year2_change_3mo_gross_margin` | 0.7336 | 5 | 5 | Change in the second-year gross margin estimate over the past three months. |
| 375 | `est_q1_asymmetry_profit` | 0.7334 | 1 | 3 | Asymmetry measure of profit estimates for the most recent quarter. |
| 376 | `est_q1_coeff_var_profit` | 0.7334 | 1 | 1 | Coefficient of variation for profit estimates in the most recent quarter. |
| 377 | `interest_expense_surprise_difference` | 0.7331 | 0 | 0 | Difference between actual and consensus interest expense for the most recent period. |
| 378 | `actual_q1_qoq_depr_amort` | 0.733 | 2 | 2 | Quarter-over-quarter change in actual Q1 depreciation and amortization. |
| 379 | `revenue_estimate_volatility_adj_3yr` | 0.7322 | 0 | 0 | Volatility-adjusted 3-year projected revenue growth |
| 380 | `fwd_year1_estimate_cagr_4yr_nprofit` | 0.7319 | 0 | 0 | Compound annual growth rate of the forward year 1 net profit estimate over the last 4 years. |
| 381 | `nav_estimate_cagr3y_year1` | 0.7316 | 0 | 0 | Compound annual growth rate of net asset value estimates over the last 3 years to the next year. |
| 382 | `fwd_year1_estimate_change_3mo_gpm` | 0.7312 | 2 | 2 | Change in the forward year 1 gross profit margin estimate over the past 3 months. |
| 383 | `estimate_revision_magnitude_gpm` | 0.7308 | 5 | 7 | Magnitude of recent revisions in the consensus gross profit margin estimate. |
| 384 | `estimate_y1_cagr4_ebit` | 0.7296 | 0 | 0 | Four-year compound annual growth rate for year 1 EBIT estimate. |
| 385 | `interest_expense_trend_slope_3yr` | 0.7293 | 0 | 0 | Slope of the linear trend in interest expense estimates over the past three years. |
| 386 | `ebitda_estimate_surprise_diff` | 0.7286 | 0 | 0 | Difference between actual and consensus EBITDA estimate for a given period. |
| 387 | `estimate_year1_skewness_cashflow_per_share` | 0.726 | 0 | 0 | Skewness of cash flow per share estimates for the first forecast year. |
| 388 | `estimate_year2_cashflow_per_share` | 0.726 | 0 | 0 | Consensus cash flow per share estimate for the second forecast year. |
| 389 | `est_zscore_profit` | 0.7245 | 0 | 0 | Z-score of profit estimate, showing how far the estimate is from the mean in standard deviations. |
| 390 | `est_q2_asymmetry_profit` | 0.7229 | 0 | 0 | Asymmetry measure of profit estimates for the second quarter. |
| 391 | `est_q2_coeff_var_profit` | 0.7229 | 0 | 0 | Coefficient of variation for profit estimates in the second quarter. |
| 392 | `op_expense_actual_q1_qoq_growth` | 0.7217 | 4 | 4 | Quarter-over-quarter growth rate in actual operating expense for the most recent quarter. |
| 393 | `estimate_surprise_stddev_depr_amort` | 0.7215 | 0 | 0 | Standard deviation of the surprise (actual minus estimate) for depreciation and amortization. |
| 394 | `current_assets_estimate_year1_skewness` | 0.7212 | 1 | 1 | Skewness of analyst current assets estimates for the next fiscal year. |
| 395 | `estimate_y2_value_currassets` | 0.7212 | 0 | 0 | Analyst consensus estimate for current assets in year 2. |
| 396 | `est_y1_skewness_gross_income` | 0.721 | 0 | 0 | Skewness of year 1 gross income estimates, indicating asymmetry in forecast distribution. |
| 397 | `est_y2_gross_income` | 0.721 | 1 | 1 | Consensus gross income estimate for the second fiscal year ahead. |
| 398 | `op_expense_estimate_y1_cagr_2yr` | 0.7198 | 0 | 0 | Two-year compound annual growth rate for next fiscal year operating expense estimate. |
| 399 | `est_y2_change_3mo_gross_income` | 0.7188 | 1 | 1 | Change in year 2 gross income estimate over the past 3 months. |
| 400 | `interest_expense_q1_yoy_growth_est` | 0.7188 | 0 | 0 | Year-over-year growth estimate for interest expense in the current quarter. |
| 401 | `ebitda_y1_estimate_cagr3` | 0.7172 | 2 | 2 | Three-year compound annual growth rate for consensus EBITDA estimate in year one. |
| 402 | `estimate_revision_magnitude_cashflow_per_share` | 0.7168 | 2 | 2 | Magnitude of recent revisions in cash flow per share estimates. |
| 403 | `estimate_year1_change_3mo_cashflow_per_share` | 0.7168 | 0 | 0 | Change in first forecast year cash flow per share estimate over the past three months. |
| 404 | `estimate_year2_change_3mo_cashflow_per_share` | 0.7167 | 0 | 0 | Change in second forecast year cash flow per share estimate over the past three months. |
| 405 | `netprofit_estimate_volatility_adj_3yr` | 0.7162 | 1 | 1 | Volatility-adjusted projected 3-year growth in net profit |
| 406 | `ebitda_estimate_trend_slope2` | 0.7153 | 0 | 0 | Slope of the trend line for consensus EBITDA estimates over the last two periods. |
| 407 | `ebitda_estimate_trend_slope3` | 0.7153 | 1 | 1 | Slope of the trend line for consensus EBITDA estimates over the last three periods. |
| 408 | `ebitda_q1_estimate_yoy_growth` | 0.7152 | 6 | 7 | Year-over-year growth in consensus EBITDA estimate for the first quarter. |
| 409 | `est_y1_change_3mo_gross_income` | 0.715 | 1 | 1 | Change in year 1 gross income estimate over the past 3 months. |
| 410 | `capex_estimate_y1_cagr_2yr` | 0.7147 | 0 | 0 | Two-year compound annual growth rate for next fiscal year capital expenditure estimate. |
| 411 | `est_revision_magnitude_gross_income` | 0.7144 | 0 | 0 | Magnitude of recent revisions in gross income estimates. |
| 412 | `op_expense_surprise_stddev` | 0.7142 | 0 | 0 | Standard deviation of operating expense surprises over a defined period. |
| 413 | `current_assets_estimate_revision_magnitude` | 0.714 | 0 | 0 | Magnitude of recent analyst revisions to current assets estimates. |
| 414 | `current_assets_estimate_year1_change_3mo` | 0.714 | 2 | 3 | Change in the next fiscal year's current assets estimate over the past 3 months. |
| 415 | `estimate_y2_change_3mo_currassets` | 0.7139 | 0 | 0 | Three-month change in year 2 current assets estimate. |
| 416 | `cogs_y2_estimate_change_3m` | 0.7134 | 0 | 0 | Change in consensus cost of goods sold estimate for year two over the past three months. |
| 417 | `estimate_y1_cash_invest` | 0.7134 | 1 | 1 | Consensus estimate for year 1 cash flow from investing activities. |
| 418 | `estimate_surprise_diff_depr_amort` | 0.7112 | 0 | 0 | Difference between actual and estimated depreciation and amortization values (surprise). |
| 419 | `nav_estimate_q1_skewness` | 0.7109 | 1 | 1 | Skewness of analyst net asset value estimates for the first quarter. |
| 420 | `nav_estimate_q2_qoq_growth` | 0.7109 | 0 | 0 | Quarter-over-quarter growth in net asset value estimate for the second quarter. |
| 421 | `nav_estimate_q2_skewness` | 0.7109 | 0 | 0 | Skewness of analyst net asset value estimates for the second quarter. |
| 422 | `nav_estimate_trend_slope_1yr` | 0.7109 | 0 | 0 | Slope of analyst consensus net asset value estimates over the last year. |
| 423 | `estimate_y1_cagr2_book_value_ps` | 0.7095 | 1 | 1 | Two-year compound annual growth rate for year 1 book value per share estimate. |
| 424 | `estimate_y1_asymmetry_depr_amort` | 0.7092 | 0 | 0 | Asymmetry measure for year 1 depreciation and amortization estimate distribution. |
| 425 | `estimate_y1_coeffvar_depr_amort` | 0.7092 | 0 | 0 | Coefficient of variation for year 1 depreciation and amortization estimates. |
| 426 | `estimate_y1_cagr2_mktblsec` | 0.7079 | 0 | 0 | Two-year compound annual growth rate for year 1 marketable securities estimate. |
| 427 | `est_volatility_adj_3yr_eps` | 0.7068 | 0 | 0 | Volatility of EPS estimates adjusted over a 3-year period. |
| 428 | `cogs_estimate_year2` | 0.7062 | 0 | 0 | Consensus cost of goods sold estimate for the second forecast year. |
| 429 | `est_y1_skewness_cogs` | 0.7062 | 1 | 2 | Skewness of next fiscal year cost of goods sold estimates, reflecting asymmetry in analyst forecasts. |
| 430 | `op_expense_surprise_difference` | 0.7051 | 0 | 0 | Difference between actual and estimated operating expense for a given period. |
| 431 | `estimate_y2_coeffvar_depr_amort` | 0.705 | 0 | 0 | Coefficient of variation for year 2 depreciation and amortization estimates. |
| 432 | `est_y1_cagr_4yr_profit` | 0.7045 | 0 | 0 | Compound annual growth rate of year 1 profit estimate over the last 4 years. |
| 433 | `eps_y1_cagr_5yr` | 0.7036 | 0 | 0 | Forecast FY1 EPS growth CAGR over 5 years |
| 434 | `cogs_y1_estimate_change_3m` | 0.7021 | 0 | 0 | Change in consensus cost of goods sold estimate for year one over the past three months. |
| 435 | `nav_estimate_q1_change_1mo` | 0.702 | 0 | 0 | Change in the first quarter's net asset value estimate over the past month. |
| 436 | `cogs_estimate_revision_magnitude` | 0.7 | 1 | 1 | Magnitude of recent revisions in consensus cost of goods sold estimates. |
| 437 | `ebitda_actual_q1_yoy_growth` | 0.6973 | 0 | 0 | Year-over-year growth in reported EBITDA for the first quarter. |
| 438 | `ebitda_q1_estimate_sequential_growth` | 0.6972 | 0 | 0 | Sequential growth in consensus EBITDA estimate for the first quarter. |
| 439 | `est_slope_4yr_profit` | 0.6962 | 0 | 0 | Slope of profit estimates over the last 4 years, showing long-term trend direction. |
| 440 | `est_volatility_adj_2yr_profit` | 0.6962 | 0 | 0 | Volatility of profit estimates adjusted over a 2-year period. |
| 441 | `forward_year1_estimate_gpm` | 0.696 | 0 | 0 | Consensus gross profit margin estimate for the first forward year. |
| 442 | `netprofit_y1_cagr_5yr` | 0.6959 | 0 | 0 | Forecast FY1 net profit growth CAGR measured over 5 years |
| 443 | `interest_expense_actual_q1_yoy_growth` | 0.6943 | 0 | 0 | Year-over-year growth in actual reported interest expense for the most recent quarter. |
| 444 | `estimate_year1_cashflow_per_share` | 0.6922 | 0 | 0 | Consensus cash flow per share estimate for the first forecast year. |
| 445 | `est_y1_gross_income` | 0.6919 | 1 | 1 | Consensus gross income estimate for the next fiscal year. |
| 446 | `interest_expense_q1_asymmetry` | 0.6892 | 0 | 0 | Asymmetry (difference between mean and median) of interest expense estimates for the current quarter. |
| 447 | `interest_expense_q1_coeff_variation` | 0.6892 | 0 | 0 | Coefficient of variation for interest expense estimates in the current quarter. |
| 448 | `revenue_y1_cagr_5yr` | 0.6888 | 1 | 1 | Forecast compound annual growth rate to FY1 revenue measured over a 5-year horizon |
| 449 | `nav_estimate_q1_qoq_growth` | 0.6873 | 0 | 0 | Quarter-over-quarter growth in net asset value estimate for the first quarter. |
| 450 | `nav_estimate_trailing_4q_sum` | 0.6873 | 0 | 0 | Sum of the most recent four quarters of net asset value estimates (trailing twelve months). |
| 451 | `estimate_q1_sequential_interestexp` | 0.6859 | 0 | 0 | Sequential change in interest expense estimate for the first quarter. |
| 452 | `est_y1_cagr_5yr_eps` | 0.6855 | 1 | 1 | Compound annual growth rate of year 1 EPS estimate over the last 5 years. |
| 453 | `estimate_q1_skewness_mktblsec` | 0.6847 | 1 | 1 | Skewness of analyst estimates for marketable securities in the first quarter forecast. |
| 454 | `estimate_q2_qoq_change_mktblsec` | 0.6847 | 0 | 0 | Quarter-over-quarter change in marketable securities estimate for the second quarter. |
| 455 | `estimate_trend_slope1_mktblsec` | 0.6847 | 0 | 0 | First slope coefficient from trend analysis of marketable securities estimates. |
| 456 | `estimate_q2_skewness_mktblsec` | 0.6846 | 0 | 0 | Skewness of analyst estimates for marketable securities in the second quarter forecast. |
| 457 | `fwd_year1_estimate_cagr_5yr_pprofit` | 0.6841 | 0 | 0 | Compound annual growth rate of the forward year 1 pretax profit estimate over the last 5 years. |
| 458 | `estimate_volatility_adj3yr_ebit` | 0.6826 | 0 | 0 | Volatility of EBIT estimates adjusted over a three-year period. |
| 459 | `interest_expense_q2_asymmetry` | 0.6818 | 0 | 0 | Asymmetry (difference between mean and median) of interest expense estimates for the next quarter. |
| 460 | `interest_expense_q2_coeff_variation` | 0.6818 | 0 | 0 | Coefficient of variation for interest expense estimates in the next quarter. |
| 461 | `estimate_q1_change_1mo_mktblsec` | 0.6771 | 0 | 0 | One-month change in first quarter marketable securities estimate. |
| 462 | `ebitda_q1_estimate_asymmetry` | 0.677 | 1 | 1 | Asymmetry measure of consensus EBITDA estimates for the first quarter. |
| 463 | `ebitda_q1_estimate_coeff_var` | 0.677 | 2 | 2 | Coefficient of variation for consensus EBITDA estimate in the first quarter. |
| 464 | `nav_estimate_year1_asymmetry` | 0.6758 | 0 | 0 | Asymmetry (skewness) of analyst net asset value estimates for the next fiscal year. |
| 465 | `nav_estimate_year1_coeff_var` | 0.6758 | 1 | 1 | Coefficient of variation for analyst net asset value estimates for the next fiscal year. |
| 466 | `ebitdarep_estimate_year2` | 0.6752 | 0 | 0 | Consensus reported EBITDA estimate for the second forecast year. |
| 467 | `ebitdarep_y1_estimate_skewness` | 0.6752 | 0 | 0 | Skewness of the distribution of consensus reported EBITDA estimates for year one. |
| 468 | `fwd_year1_estimate_cagr_5yr_nprofit` | 0.674 | 0 | 0 | Compound annual growth rate of the forward year 1 net profit estimate over the last 5 years. |
| 469 | `estimate_volatility_adjusted_3yr_pprofit` | 0.6727 | 0 | 0 | Three-year volatility-adjusted measure of consensus pretax profit estimate changes. |
| 470 | `estimate_volatility_adjusted_3yr` | 0.6721 | 0 | 0 | Three-year volatility-adjusted measure of consensus estimate changes. |
| 471 | `estimate_year1_cagr2_operating_cashflow` | 0.6709 | 0 | 0 | Two-year compound annual growth rate for operating cash flow estimates starting from the first forecast year. |
| 472 | `cogs_estimate_year1` | 0.6705 | 0 | 0 | Consensus cost of goods sold estimate for the first forecast year. |
| 473 | `ebitda_q2_estimate_asymmetry` | 0.6704 | 0 | 0 | Asymmetry measure of consensus EBITDA estimates for the second quarter. |
| 474 | `ebitda_q2_estimate_coeff_var` | 0.6704 | 0 | 0 | Coefficient of variation for consensus EBITDA estimate in the second quarter. |
| 475 | `estimate_y1_value_currassets` | 0.6696 | 0 | 0 | Analyst consensus estimate for current assets in year 1. |
| 476 | `nav_estimate_cagr4y_year1` | 0.6695 | 1 | 1 | Compound annual growth rate of net asset value estimates over the last 4 years to the next year. |
| 477 | `estimate_year1_cagr2_free_cash_flow` | 0.6675 | 0 | 0 | Two-year compound annual growth rate for free cash flow estimates starting from the first forecast year. |
| 478 | `ebitda_estimate_zscore` | 0.6671 | 1 | 1 | Z-score of the consensus EBITDA estimate relative to its historical mean and standard deviation. |
| 479 | `estimate_trailing_12mo_mktblsec` | 0.664 | 0 | 0 | Trailing twelve-month estimate for marketable securities. |
| 480 | `estimate_y1_cagr5_ebit` | 0.664 | 0 | 0 | Five-year compound annual growth rate for year 1 EBIT estimate. |
| 481 | `ebitdarep_estimate_revision_magnitude` | 0.6639 | 0 | 0 | Magnitude of recent revisions in consensus reported EBITDA estimates. |
| 482 | `ebitdarep_y1_estimate_change_3m` | 0.6639 | 0 | 0 | Change in consensus reported EBITDA estimate for year one over the past three months. |
| 483 | `ebitdarep_y2_estimate_change_3m` | 0.6638 | 0 | 0 | Change in consensus reported EBITDA estimate for year two over the past three months. |
| 484 | `estimate_q1_qoq_change_mktblsec` | 0.6637 | 0 | 0 | Quarter-over-quarter change in marketable securities estimate for the first quarter. |
| 485 | `nav_estimate_year2_coeff_var` | 0.6637 | 0 | 0 | Coefficient of variation for analyst net asset value estimates for the second forecast year. |
| 486 | `estimate_trend_slope2_depr_amort` | 0.6631 | 0 | 0 | Second-order slope of the depreciation and amortization estimate trend. |
| 487 | `estimate_trend_slope3_depr_amort` | 0.663 | 0 | 0 | Third-order slope of the depreciation and amortization estimate trend. |
| 488 | `estimate_q1_yoy_depr_amort` | 0.6625 | 0 | 0 | Year-over-year change in Q1 depreciation and amortization estimate. |
| 489 | `ebitda_y1_estimate_cagr4` | 0.6616 | 0 | 0 | Four-year compound annual growth rate for consensus EBITDA estimate in year one. |
| 490 | `estimate_y1_cagr3_depr_amort` | 0.6611 | 0 | 0 | Three-year compound annual growth rate for year 1 depreciation and amortization estimate. |
| 491 | `estimate_trend_slope_intermediate_op_expense` | 0.6605 | 0 | 0 | Slope of the intermediate-term trend line for operating expense estimates. |
| 492 | `estimate_trend_slope_mid_op_expense` | 0.6605 | 0 | 0 | Slope of the mid-term trend line for operating expense estimates. |
| 493 | `op_expense_estimate_q1_yoy_growth` | 0.6604 | 0 | 0 | Year-over-year growth rate in current quarter operating expense estimate. |
| 494 | `estimate_y1_asymmetry_mktblsec` | 0.6569 | 0 | 0 | Asymmetry measure of year 1 marketable securities analyst estimates. |
| 495 | `estimate_y1_coeffvar_mktblsec` | 0.6569 | 1 | 1 | Coefficient of variation for year 1 marketable securities estimate. |
| 496 | `capex_estimate_y1_cagr_3yr` | 0.6543 | 2 | 2 | Three-year compound annual growth rate for next fiscal year capital expenditure estimate. |
| 497 | `interest_expense_zscore_estimate` | 0.6528 | 0 | 0 | Z-score of the current interest expense estimate relative to historical mean and standard deviation. |
| 498 | `interest_expense_3yr_cagr_estimate` | 0.6479 | 0 | 0 | Compound annual growth rate of interest expense over the past three years based on estimates. |
| 499 | `nav_actual_q1_qoq_growth` | 0.6476 | 0 | 0 | Quarter-over-quarter growth in actual reported net asset value for the first quarter. |
| 500 | `estimate_y1_cagr3_book_value_ps` | 0.6464 | 0 | 0 | Three-year compound annual growth rate for year 1 book value per share estimate. |
| 501 | `estimate_y2_coeffvar_mktblsec` | 0.6461 | 0 | 0 | Coefficient of variation for year 2 marketable securities estimate. |
| 502 | `estimate_y1_cagr3_mktblsec` | 0.6449 | 0 | 0 | Three-year compound annual growth rate for year 1 marketable securities estimate. |
| 503 | `ebitda_estimate_trend_slope4` | 0.6443 | 0 | 0 | Slope of the trend line for consensus EBITDA estimates over the last four periods. |
| 504 | `ebitda_estimate_volatility_adj_2yr` | 0.6443 | 0 | 0 | Volatility-adjusted measure of consensus EBITDA estimates over the past two years. |
| 505 | `est_y1_cagr_5yr_profit` | 0.6439 | 0 | 0 | Compound annual growth rate of year 1 profit estimate over the last 5 years. |
| 506 | `fwd_year1_estimate_cagr_2yr_gpm` | 0.638 | 0 | 0 | Compound annual growth rate of the forward year 1 gross profit margin estimate over the last 2 years. |
| 507 | `ebitdarep_estimate_year1` | 0.6378 | 1 | 1 | Consensus reported EBITDA estimate for the first forecast year. |
| 508 | `capex_estimate_y1_asymmetry` | 0.6369 | 0 | 0 | Asymmetry (skewness) of the distribution of next fiscal year capital expenditure estimates. |
| 509 | `capex_estimate_y1_coeff_var` | 0.6369 | 0 | 0 | Coefficient of variation for next fiscal year capital expenditure estimate. |
| 510 | `actual_q1_yoy_depr_amort` | 0.6356 | 3 | 3 | Year-over-year change in actual Q1 depreciation and amortization. |
| 511 | `estimate_q1_sequential_depr_amort` | 0.635 | 0 | 0 | Sequential change in Q1 depreciation and amortization estimate. |
| 512 | `op_expense_actual_q1_yoy_growth` | 0.6346 | 1 | 1 | Year-over-year growth rate in actual operating expense for the most recent quarter. |
| 513 | `op_expense_estimate_q1_sequential` | 0.6346 | 0 | 0 | Sequential value or change in current quarter operating expense estimate. |
| 514 | `nav_estimate_surprise_stddev` | 0.6325 | 0 | 0 | Standard deviation of the difference between actual and consensus net asset value estimates (surprise). |
| 515 | `capex_y2_estimate_coeff_var` | 0.6305 | 1 | 1 | Coefficient of variation for consensus capital expenditure estimate in year two. |
| 516 | `estimate_trend_slope_primary_gross_margin` | 0.629 | 0 | 0 | First-order slope of analyst gross margin estimates over time, indicating trend direction. |
| 517 | `cogs_estimate_trend_slope1` | 0.6288 | 1 | 1 | Slope of the trend line for consensus cost of goods sold estimates over the last period. |
| 518 | `quarter2_estimate_skewness_gpm` | 0.6286 | 0 | 0 | Skewness of the consensus gross profit margin estimate distribution for the second upcoming quarter. |
| 519 | `estimate_q2_quarterly_change_gross_margin` | 0.6285 | 3 | 3 | Quarter-over-quarter change in gross margin estimate for the second quarter. |
| 520 | `quarter1_estimate_skewness_gpm` | 0.6285 | 0 | 0 | Skewness of the consensus gross profit margin estimate distribution for the next quarter. |
| 521 | `cogs_estimate_surprise_stdev` | 0.6277 | 0 | 0 | Standard deviation of the difference between actual and forecasted cost of goods sold. |
| 522 | `cogs_q2_estimate_skewness` | 0.6257 | 0 | 0 | Skewness of the distribution of consensus cost of goods sold estimates for the second quarter. |
| 523 | `estimate_year1_cagr2_cashflow_per_share` | 0.6256 | 0 | 0 | Two-year compound annual growth rate for cash flow per share estimates starting from the first forecast year. |
| 524 | `est_volatility_adj_3yr_profit` | 0.6246 | 1 | 1 | Volatility of profit estimates adjusted over a 3-year period. |
| 525 | `quarter1_estimate_change_1mo_gpm` | 0.6244 | 0 | 0 | Change in the consensus gross profit margin estimate for the next quarter over the past month. |
| 526 | `cogs_q2_estimate_qoq_growth` | 0.6242 | 15 | 22 | Quarter-over-quarter growth in consensus cost of goods sold estimate for the second quarter. |
| 527 | `est_q1_skewness_cogs` | 0.6242 | 0 | 0 | Skewness of first quarter cost of goods sold estimates, reflecting asymmetry in analyst forecasts. |
| 528 | `actual_q1_qoq_change_mktblsec` | 0.6225 | 3 | 3 | Quarter-over-quarter change in actual marketable securities for the first quarter. |
| 529 | `estimate_y1_cagr2_cash_invest` | 0.6216 | 0 | 0 | Two-year compound annual growth rate for year 1 cash flow from investing activities estimate. |
| 530 | `cogs_estimate_trailing_twelve_months` | 0.6214 | 0 | 0 | Consensus cost of goods sold estimate for the trailing twelve months period. |
| 531 | `cogs_estimate_surprise_diff` | 0.6213 | 0 | 0 | Difference between actual and consensus cost of goods sold estimate for a given period. |
| 532 | `cogs_q1_estimate_change_1m` | 0.6213 | 0 | 0 | Change in consensus cost of goods sold estimate for the first quarter over the past month. |
| 533 | `nav_estimate_surprise_difference` | 0.6213 | 0 | 0 | Difference between actual and consensus net asset value estimate (surprise). |
| 534 | `est_y1_cagr_2yr_gross_income` | 0.6194 | 1 | 1 | Compound annual growth rate of year 1 gross income estimate over the last 2 years. |
| 535 | `estimate_surprise_stddev_mktblsec` | 0.6191 | 0 | 0 | Standard deviation of the difference between actual and forecasted marketable securities. |
| 536 | `est_slope_1yr_gross_income` | 0.6159 | 0 | 0 | Slope of gross income estimates over the last year, indicating short-term trend direction. |
| 537 | `op_expense_estimate_y1_asymmetry` | 0.615 | 1 | 2 | Asymmetry (skewness) of the distribution of next fiscal year operating expense estimates. |
| 538 | `op_expense_estimate_y1_coeff_var` | 0.615 | 0 | 0 | Coefficient of variation for next fiscal year operating expense estimate. |
| 539 | `estimate_trend_slope_recent_capex` | 0.6141 | 0 | 0 | Slope of the most recent trend line for capital expenditure estimates. |
| 540 | `est_q2_skewness_gross_income` | 0.614 | 0 | 0 | Skewness of gross income estimates for the second quarter, indicating asymmetry in forecast distribution. |
| 541 | `capex_estimate_q1_skewness` | 0.6134 | 0 | 0 | Skewness of the distribution of current quarter capital expenditure estimates. |
| 542 | `capex_q2_estimate_qoq_growth` | 0.6134 | 0 | 0 | Quarter-over-quarter growth in consensus capital expenditure estimate for the second quarter. |
| 543 | `est_q1_skewness_gross_income` | 0.6134 | 0 | 0 | Skewness of gross income estimates for the most recent quarter, indicating asymmetry in forecast distribution. |
| 544 | `est_q2_qoq_gross_income` | 0.6134 | 22 | 28 | Quarter-over-quarter change in gross income estimate for the second quarter. |
| 545 | `capex_estimate_q2_skewness` | 0.613 | 1 | 1 | Skewness of the distribution of second quarter capital expenditure estimates. |
| 546 | `interest_expense_trend_slope_4yr` | 0.6126 | 0 | 0 | Slope of the linear trend in interest expense estimates over the past four years. |
| 547 | `interest_expense_volatility_adjusted_2yr` | 0.6125 | 0 | 0 | Two-year volatility-adjusted measure of interest expense estimates. |
| 548 | `op_expense_estimate_y2_coeff_var` | 0.6119 | 3 | 4 | Coefficient of variation for the second fiscal year operating expense estimate. |
| 549 | `cogs_q1_estimate_qoq_growth` | 0.6111 | 0 | 0 | Quarter-over-quarter growth in consensus cost of goods sold estimate for the first quarter. |
| 550 | `estimate_surprise_diff_mktblsec` | 0.6104 | 0 | 0 | Difference between actual and forecasted marketable securities values. |
| 551 | `est_q1_change_1mo_gross_income` | 0.6102 | 0 | 0 | Change in gross income estimate for the most recent quarter over the past month. |
| 552 | `estimate_trailing_twelve_months_gpm` | 0.6098 | 0 | 0 | Consensus gross profit margin estimate for the trailing twelve month period. |
| 553 | `ebitda_y1_estimate_cagr5` | 0.6088 | 0 | 0 | Five-year compound annual growth rate for consensus EBITDA estimate in year one. |
| 554 | `est_qttm_gross_income` | 0.6085 | 0 | 0 | Trailing twelve month gross income estimate based on quarterly data. |
| 555 | `quarter1_estimate_qoq_change_gpm` | 0.6085 | 0 | 0 | Quarter-over-quarter change in the consensus gross profit margin estimate for the next quarter. |
| 556 | `capex_q1_estimate_change_1m` | 0.6053 | 1 | 1 | Change in consensus capital expenditure estimate for the first quarter over the past month. |
| 557 | `op_expense_estimate_y1_cagr_3yr` | 0.6042 | 0 | 0 | Three-year compound annual growth rate for next fiscal year operating expense estimate. |
| 558 | `est_q1_qoq_gross_income` | 0.6033 | 1 | 1 | Quarter-over-quarter change in gross income estimate for the most recent quarter. |
| 559 | `nav_estimate_cagr5y_year1` | 0.6029 | 0 | 0 | Compound annual growth rate of net asset value estimates over the last 5 years to the next year. |
| 560 | `cf_operating_estimate_q2_qoq_growth` | 0.5987 | 0 | 0 | Quarter-over-quarter growth rate in operating cash flow estimate for the second quarter. |
| 561 | `estimate_q1_skewness_operating_cashflow` | 0.5987 | 0 | 0 | Skewness of operating cash flow estimates for the first quarter. |
| 562 | `estimate_trend_slope_primary_operating_cashflow` | 0.5987 | 0 | 0 | First-order slope of analyst operating cash flow estimates over time, indicating trend direction. |
| 563 | `cf_operating_estimate_q2_skewness` | 0.5986 | 0 | 0 | Skewness of analyst operating cash flow estimates for the second quarter. |
| 564 | `capex_estimate_trailing_12mo` | 0.5983 | 0 | 0 | Trailing twelve month capital expenditure estimate. |
| 565 | `capex_estimate_y1_cagr_4yr` | 0.5983 | 0 | 0 | Four-year compound annual growth rate for next fiscal year capital expenditure estimate. |
| 566 | `estimate_q1_asymmetry_depr_amort` | 0.5975 | 0 | 0 | Asymmetry measure for Q1 depreciation and amortization estimate distribution. |
| 567 | `estimate_q1_coeffvar_depr_amort` | 0.5975 | 0 | 0 | Coefficient of variation for Q1 depreciation and amortization estimates. |
| 568 | `capex_estimate_q1_qoq_growth` | 0.5957 | 0 | 0 | Quarter-over-quarter growth rate in current quarter capital expenditure estimate. |
| 569 | `cogs_y2_estimate_coeff_var` | 0.5943 | 0 | 0 | Coefficient of variation for consensus cost of goods sold estimate in year two. |
| 570 | `est_surprise_stddev_gross_income` | 0.594 | 1 | 1 | Standard deviation of gross income estimate surprises, indicating variability in forecast errors. |
| 571 | `cogs_actual_q1_qoq_growth` | 0.5934 | 0 | 0 | Quarter-over-quarter growth in reported cost of goods sold for the first quarter. |
| 572 | `cogs_y1_estimate_cagr2` | 0.5915 | 0 | 0 | Two-year compound annual growth rate for consensus cost of goods sold estimate in year one. |
| 573 | `actual_quarter1_qoq_growth_gpm` | 0.5909 | 1 | 1 | Quarter-over-quarter growth in actual reported gross profit margin for the most recent quarter. |
| 574 | `estimate_q1_change_1mo_operating_cashflow` | 0.5907 | 1 | 1 | Change in first quarter operating cash flow estimate over the past month. |
| 575 | `fwd_year1_estimate_cagr_4yr` | 0.5888 | 1 | 1 | Compound annual growth rate of the forward year 1 estimate over the last 4 years. |
| 576 | `est_surprise_diff_gross_income` | 0.5884 | 0 | 0 | Difference between actual and estimated gross income, representing the forecast error. |
| 577 | `estimate_q2_asymmetry_depr_amort` | 0.5873 | 0 | 0 | Asymmetry measure for Q2 depreciation and amortization estimate distribution. |
| 578 | `estimate_q2_coeffvar_depr_amort` | 0.5873 | 0 | 0 | Coefficient of variation for Q2 depreciation and amortization estimates. |
| 579 | `actual_q1_qoq_gross_income_growth` | 0.5864 | 3 | 3 | Quarter-over-quarter growth rate for actual gross income in the most recent quarter. |
| 580 | `estimate_zscore_depr_amort` | 0.586 | 0 | 0 | Z-score of the consensus depreciation and amortization estimate. |
| 581 | `cogs_y1_estimate_asymmetry` | 0.5851 | 0 | 0 | Asymmetry measure of consensus cost of goods sold estimates for year one. |
| 582 | `est_y1_coeff_var_cogs` | 0.5851 | 0 | 0 | Coefficient of variation for next fiscal year cost of goods sold estimates, measuring relative dispersion. |
| 583 | `cf_operating_estimate_year1_asymmetry` | 0.585 | 1 | 1 | Asymmetry (skewness) of analyst operating cash flow estimates for the next fiscal year. |
| 584 | `cf_operating_estimate_year1_coeff_var` | 0.585 | 1 | 1 | Coefficient of variation for analyst operating cash flow estimates for the next fiscal year. |
| 585 | `fwd_year1_estimate_cagr_3yr_gpm` | 0.5835 | 0 | 0 | Compound annual growth rate of the forward year 1 gross profit margin estimate over the last 3 years. |
| 586 | `ebitda_estimate_volatility_adj_3yr` | 0.5833 | 1 | 1 | Volatility-adjusted measure of consensus EBITDA estimates over the past three years. |
| 587 | `estimate_y1_cagr2_currassets` | 0.5804 | 0 | 0 | Two-year compound annual growth rate for year 1 current assets estimate. |
| 588 | `cf_operating_estimate_trailing_4q_sum` | 0.5797 | 0 | 0 | Sum of the most recent four quarters of operating cash flow estimates (trailing twelve months). |
| 589 | `estimate_q1_quarterly_change_operating_cashflow` | 0.5796 | 0 | 0 | Quarter-over-quarter change in operating cash flow estimate for the first quarter. |
| 590 | `cf_operating_estimate_year2_coeff_var` | 0.5787 | 0 | 0 | Coefficient of variation for analyst operating cash flow estimates for the second forecast year. |
| 591 | `cf_operating_estimate_cagr3y_year1` | 0.5749 | 0 | 0 | Compound annual growth rate of operating cash flow estimates over the last 3 years to the next year. |
| 592 | `estimate_surprise_standard_deviation_gpm` | 0.5743 | 0 | 0 | Standard deviation of the difference between actuals and consensus gross profit margin estimates. |
| 593 | `estimate_year1_cagr3_free_cash_flow` | 0.5736 | 0 | 0 | Three-year compound annual growth rate for free cash flow estimates starting from the first forecast year. |
| 594 | `estimate_year1_asymmetry_free_cash_flow` | 0.5703 | 0 | 0 | Asymmetry (skewness) of free cash flow estimates for the first forecast year. |
| 595 | `estimate_year1_coeff_var_free_cash_flow` | 0.5703 | 0 | 0 | Coefficient of variation for free cash flow estimates in the first forecast year. |
| 596 | `est_y2_coeff_var_gross_income` | 0.5694 | 1 | 1 | Coefficient of variation for year 2 gross income estimates, measuring relative dispersion. |
| 597 | `estimate_year2_coeff_var_free_cash_flow` | 0.5679 | 0 | 0 | Coefficient of variation for free cash flow estimates in the second forecast year. |
| 598 | `est_y1_asymmetry_gross_income` | 0.5678 | 1 | 1 | Asymmetry measure of year 1 gross income estimates. |
| 599 | `est_y1_coeff_var_gross_income` | 0.5678 | 0 | 0 | Coefficient of variation for year 1 gross income estimates, measuring relative dispersion. |
| 600 | `fwd_year2_estimate_coeff_var_gpm` | 0.5647 | 0 | 0 | Coefficient of variation for the forward year 2 gross profit margin estimate. |
| 601 | `estimate_year1_cagr3_cashflow_per_share` | 0.5637 | 0 | 0 | Three-year compound annual growth rate for cash flow per share estimates starting from the first forecast year. |
| 602 | `op_expense_estimate_q1_asymmetry` | 0.5628 | 1 | 1 | Asymmetry (skewness) of the distribution of current quarter operating expense estimates. |
| 603 | `op_expense_estimate_q1_coeff_var` | 0.5628 | 1 | 1 | Coefficient of variation for current quarter operating expense estimate. |
| 604 | `capex_actual_q1_qoq_growth` | 0.5616 | 0 | 0 | Quarter-over-quarter growth rate in actual capital expenditure for the most recent quarter. |
| 605 | `nav_estimate_q1_yoy_growth` | 0.5612 | 0 | 0 | Year-over-year growth rate in net asset value estimate for the first quarter. |
| 606 | `nav_estimate_trend_slope_2yr` | 0.5612 | 1 | 2 | Slope of analyst consensus net asset value estimates over the last 2 years. |
| 607 | `nav_estimate_trend_slope_3yr` | 0.5612 | 0 | 0 | Slope of analyst consensus net asset value estimates over the last 3 years. |
| 608 | `estimate_y1_asymmetry_book_value_ps` | 0.5599 | 0 | 0 | Asymmetry measure for year 1 book value per share estimate distribution. |
| 609 | `estimate_y1_coeffvar_book_value_ps` | 0.5599 | 0 | 0 | Coefficient of variation for year 1 book value per share estimates. |
| 610 | `estimate_year1_coeff_var_gross_margin` | 0.5588 | 0 | 0 | Coefficient of variation for gross margin estimates in the first forecast year. |
| 611 | `fwd_year1_estimate_asymmetry_gpm` | 0.5588 | 0 | 0 | Asymmetry (third moment) of the forward year 1 gross profit margin estimate distribution. |
| 612 | `op_expense_estimate_zscore` | 0.5573 | 1 | 1 | Z-score of the current operating expense estimate relative to its historical mean and standard deviation. |
| 613 | `interest_expense_4yr_cagr_estimate` | 0.5566 | 0 | 0 | Compound annual growth rate of interest expense over the past four years based on estimates. |
| 614 | `estimate_y1_cagr4_depr_amort` | 0.5548 | 0 | 0 | Four-year compound annual growth rate for year 1 depreciation and amortization estimate. |
| 615 | `estimate_q2_skewness_book_value_ps` | 0.5543 | 0 | 0 | Skewness of the Q2 book value per share estimate distribution. |
| 616 | `estimate_trend_slope1_book_value_ps` | 0.5543 | 0 | 0 | First-order slope of the book value per share estimate trend. |
| 617 | `estimate_q2_qoq_book_value_ps` | 0.5542 | 0 | 0 | Quarter-over-quarter change in Q2 book value per share estimate. |
| 618 | `quarter1_estimate_skewness` | 0.5542 | 0 | 0 | Skewness of the distribution of consensus estimates for the upcoming quarter. |
| 619 | `op_expense_estimate_q2_asymmetry` | 0.5535 | 1 | 1 | Asymmetry (skewness) of the distribution of second quarter operating expense estimates. |
| 620 | `op_expense_estimate_q2_coeff_var` | 0.5535 | 0 | 0 | Coefficient of variation for the second quarter operating expense estimate. |
| 621 | `estimate_y2_coeffvar_book_value_ps` | 0.553 | 0 | 0 | Coefficient of variation for year 2 book value per share estimates. |
| 622 | `ebitdarep_y1_estimate_cagr2` | 0.5523 | 0 | 0 | Two-year compound annual growth rate for consensus reported EBITDA estimate in year one. |
| 623 | `estimate_trend_slope_primary_cashflow_per_share` | 0.5521 | 0 | 0 | First-order slope of analyst cash flow per share estimates over time, indicating trend direction. |
| 624 | `estimate_trailing_twelve_months_cashflow_per_share` | 0.5516 | 0 | 0 | Trailing twelve months cash flow per share estimate based on analyst consensus. |
| 625 | `est_trend_slope2_cogs` | 0.5515 | 0 | 0 | Slope of the linear trend over two periods for cost of goods sold estimates, indicating direction of change. |
| 626 | `estimate_surprise_difference_gpm` | 0.5511 | 0 | 0 | Difference between actual gross profit margin and consensus estimate for the period. |
| 627 | `estimate_trend_slope_secondary_gross_margin` | 0.5509 | 0 | 0 | Second-order slope of gross margin estimates, capturing acceleration or deceleration in trend. |
| 628 | `estimate_trend_slope_3yr_gpm` | 0.5507 | 0 | 0 | Slope of the gross profit margin estimate trend over the past 3 years. |
| 629 | `estimate_q1_skewness_cashflow_per_share` | 0.5503 | 0 | 0 | Skewness of cash flow per share estimates for the first quarter. |
| 630 | `estimate_q2_quarterly_change_cashflow_per_share` | 0.5503 | 0 | 0 | Quarter-over-quarter change in cash flow per share estimate for the second quarter. |
| 631 | `estimate_q1_yearly_growth_gross_margin` | 0.5499 | 1 | 1 | Year-over-year growth in gross margin estimate for the first quarter. |
| 632 | `estimate_q1_quarterly_change_cashflow_per_share` | 0.5498 | 0 | 0 | Quarter-over-quarter change in cash flow per share estimate for the first quarter. |
| 633 | `capex_estimate_surprise_stdev` | 0.5491 | 1 | 1 | Standard deviation of the difference between actual and forecasted capital expenditure. |
| 634 | `estimate_q2_skewness_cashflow_per_share` | 0.5491 | 0 | 0 | Skewness of cash flow per share estimates for the second quarter. |
| 635 | `quarter1_estimate_change_1mo` | 0.5472 | 0 | 0 | Change in the consensus estimate for the next quarter over the past month. |
| 636 | `estimate_q1_change_1mo_cashflow_per_share` | 0.546 | 0 | 0 | Change in first quarter cash flow per share estimate over the past month. |
| 637 | `capex_estimate_y1_cagr_5yr` | 0.5452 | 1 | 1 | Five-year compound annual growth rate for next fiscal year capital expenditure estimate. |
| 638 | `cf_operating_actual_q1_qoq_growth` | 0.5452 | 2 | 2 | Quarter-over-quarter growth in actual reported operating cash flow for the first quarter. |
| 639 | `cogs_estimate_trend_slope3` | 0.5443 | 0 | 0 | Slope of the trend line for consensus cost of goods sold estimates over the last three periods. |
| 640 | `estimate_trend_slope_long_op_expense` | 0.544 | 0 | 0 | Slope of the long-term trend line for operating expense estimates. |
| 641 | `op_expense_estimate_volatility_2yr_adj` | 0.5439 | 0 | 0 | Two-year volatility of operating expense estimates, adjusted for outliers or structural breaks. |
| 642 | `estimate_trend_slope4_depr_amort` | 0.5434 | 0 | 0 | Fourth-order slope of the depreciation and amortization estimate trend. |
| 643 | `estimate_volatility_adj2yr_depr_amort` | 0.5434 | 0 | 0 | Two-year volatility-adjusted value for depreciation and amortization estimates. |
| 644 | `est_slope_2yr_gross_income` | 0.543 | 0 | 0 | Slope of gross income estimates over the last 2 years, indicating recent trend direction. |
| 645 | `estimate_trend_slope2_mktblsec` | 0.5425 | 0 | 0 | Second slope coefficient from trend analysis of marketable securities estimates. |
| 646 | `estimate_trend_slope3_mktblsec` | 0.5424 | 0 | 0 | Third slope coefficient from trend analysis of marketable securities estimates. |
| 647 | `estimate_q1_yoy_change_mktblsec` | 0.5422 | 0 | 0 | Year-over-year change in marketable securities estimate for the first quarter. |
| 648 | `est_slope_3yr_gross_income` | 0.5409 | 0 | 0 | Slope of gross income estimates over the last 3 years, showing medium-term trend direction. |
| 649 | `est_q1_yoy_growth_cogs` | 0.5402 | 0 | 0 | Year-over-year growth rate in first quarter cost of goods sold estimates. |
| 650 | `est_q1_yoy_gross_income_growth` | 0.538 | 0 | 0 | Year-over-year growth rate in gross income estimate for the most recent quarter. |
| 651 | `est_y1_cagr_3yr_gross_income` | 0.5369 | 0 | 0 | Compound annual growth rate of year 1 gross income estimate over the last 3 years. |
| 652 | `estimate_surprise_stddev_operating_cashflow` | 0.536 | 0 | 0 | Standard deviation of operating cash flow surprises (actual minus estimate). |
| 653 | `estimate_qtr_trail12mo_book_value_ps` | 0.5358 | 0 | 0 | Trailing twelve-month quarterly book value per share estimate. |
| 654 | `estimate_q1_qoq_book_value_ps` | 0.5357 | 0 | 0 | Quarter-over-quarter change in Q1 book value per share estimate. |
| 655 | `fwd_year1_estimate_cagr_5yr` | 0.5357 | 0 | 0 | Compound annual growth rate of the forward year 1 estimate over the last 5 years. |
| 656 | `nav_actual_q1_yoy_growth` | 0.535 | 0 | 0 | Year-over-year growth in actual reported net asset value for the first quarter. |
| 657 | `nav_estimate_q1_sequential_growth` | 0.535 | 0 | 0 | Sequential quarter-over-quarter growth in net asset value estimate for the first quarter. |
| 658 | `actual_quarter1_year_on_year_growth_gpm` | 0.5339 | 2 | 2 | Year-over-year growth in actual reported gross profit margin for the most recent quarter. |
| 659 | `capex_surprise_difference` | 0.5339 | 0 | 0 | Difference between actual and estimated capital expenditure for a given period. |
| 660 | `estimate_q1_sequential_change_gross_margin` | 0.5336 | 0 | 0 | Sequential change in gross margin estimate for the first quarter compared to the previous quarter. |
| 661 | `estimate_year1_cagr4_gross_margin` | 0.5333 | 0 | 0 | Four-year compound annual growth rate for gross margin estimates starting from the first forecast year. |
| 662 | `estimate_y1_cagr3_cash_invest` | 0.5285 | 0 | 0 | Three-year compound annual growth rate for year 1 cash flow from investing activities estimate. |
| 663 | `ebitdarep_estimate_trend_slope1` | 0.5282 | 0 | 0 | Slope of the trend line for consensus reported EBITDA estimates over the last period. |
| 664 | `ebitdarep_q1_estimate_skewness` | 0.5282 | 0 | 0 | Skewness of the distribution of consensus reported EBITDA estimates for the first quarter. |
| 665 | `ebitdarep_q2_estimate_qoq_growth` | 0.5282 | 0 | 0 | Quarter-over-quarter growth in consensus reported EBITDA estimate for the second quarter. |
| 666 | `ebitdarep_q2_estimate_skewness` | 0.5282 | 0 | 0 | Skewness of the distribution of consensus reported EBITDA estimates for the second quarter. |
| 667 | `estimate_surprise_difference_operating_cashflow` | 0.5275 | 0 | 0 | Difference between actual and estimated operating cash flow, representing earnings surprise. |
| 668 | `actual_q1_quarterly_change_cashflow_per_share` | 0.5265 | 1 | 1 | Quarter-over-quarter change in actual cash flow per share for the first quarter. |
| 669 | `cogs_q1_estimate_asymmetry` | 0.5252 | 0 | 0 | Asymmetry measure of consensus cost of goods sold estimates for the first quarter. |
| 670 | `est_q1_coeff_var_cogs` | 0.5252 | 0 | 0 | Coefficient of variation for first quarter cost of goods sold estimates, measuring forecast dispersion. |
| 671 | `interest_expense_volatility_adjusted_3yr` | 0.5248 | 0 | 0 | Three-year volatility-adjusted measure of interest expense estimates. |
| 672 | `estimate_trend_slope1_cash_invest` | 0.5243 | 0 | 0 | First-order slope of the cash flow from investing activities estimate trend. |
| 673 | `estimate_q1_skewness_cash_invest` | 0.5238 | 0 | 0 | Skewness of the Q1 cash flow from investing activities estimate distribution. |
| 674 | `estimate_q2_qoq_cash_invest` | 0.5238 | 0 | 0 | Quarter-over-quarter change in Q2 cash flow from investing activities estimate. |
| 675 | `est_y1_cagr3yr_cogs` | 0.5237 | 0 | 0 | Three-year compound annual growth rate for next fiscal year cost of goods sold estimates. |
| 676 | `estimate_q2_skewness_cash_invest` | 0.5235 | 0 | 0 | Skewness of the Q2 cash flow from investing activities estimate distribution. |
| 677 | `estimate_y1_cagr3_currassets` | 0.5221 | 0 | 0 | Three-year compound annual growth rate for year 1 current assets estimate. |
| 678 | `est_q2_asymmetry_cogs` | 0.52 | 0 | 0 | Asymmetry measure for second quarter cost of goods sold estimates, indicating distribution skew. |
| 679 | `est_q2_coeff_var_cogs` | 0.52 | 2 | 3 | Coefficient of variation for second quarter cost of goods sold estimates, indicating forecast uncertainty. |
| 680 | `actual_q1_yoy_gross_income_growth` | 0.5193 | 1 | 1 | Year-over-year growth rate for actual gross income in the most recent quarter. |
| 681 | `est_zscore_cogs` | 0.5191 | 1 | 1 | Z-score of cost of goods sold estimate, indicating how far the value is from the mean in standard deviations. |
| 682 | `ebitdarep_q1_estimate_change_1m` | 0.5187 | 0 | 0 | Change in consensus reported EBITDA estimate for the first quarter over the past month. |
| 683 | `est_q1_sequential_gross_income` | 0.5181 | 0 | 0 | Sequential change in gross income estimate for the most recent quarter. |
| 684 | `estimate_q1_skewness_currassets` | 0.5179 | 0 | 0 | Skewness of analyst estimates for current assets in the first quarter forecast. |
| 685 | `estimate_q2_qoq_change_currassets` | 0.5179 | 0 | 0 | Quarter-over-quarter change in current assets estimate for the second quarter. |
| 686 | `estimate_q2_skewness_currassets` | 0.5179 | 0 | 0 | Skewness of analyst estimates for current assets in the second quarter forecast. |
| 687 | `estimate_trend_slope1_currassets` | 0.5179 | 0 | 0 | First slope coefficient from trend analysis of current assets estimates. |
| 688 | `actual_q1_yoy_change_mktblsec` | 0.5155 | 2 | 2 | Year-over-year change in actual marketable securities for the first quarter. |
| 689 | `estimate_q1_change_1mo_cash_invest` | 0.5152 | 0 | 0 | Change in Q1 cash flow from investing activities estimate over the past month. |
| 690 | `estimate_q1_sequential_mktblsec` | 0.5152 | 0 | 0 | Sequential change in marketable securities estimate for the first quarter. |
| 691 | `estimate_trend_slope_primary_free_cash_flow` | 0.5142 | 0 | 0 | First-order slope of analyst free cash flow estimates over time, indicating trend direction. |
| 692 | `estimate_q1_skewness_free_cash_flow` | 0.5141 | 0 | 0 | Skewness of free cash flow estimates for the first quarter. |
| 693 | `estimate_q2_quarterly_change_free_cash_flow` | 0.5141 | 0 | 0 | Quarter-over-quarter change in free cash flow estimate for the second quarter. |
| 694 | `estimate_q2_skewness_free_cash_flow` | 0.514 | 0 | 0 | Skewness of free cash flow estimates for the second quarter. |
| 695 | `estimate_y1_cagr4_mktblsec` | 0.5136 | 0 | 0 | Four-year compound annual growth rate for year 1 marketable securities estimate. |
| 696 | `act_q1_yoy_growth_cogs` | 0.5125 | 1 | 1 | Year-over-year growth rate in actual reported cost of goods sold for the first quarter. |
| 697 | `estimate_surprise_stddev_cashflow_per_share` | 0.5124 | 0 | 0 | Standard deviation of cash flow per share surprises (actual minus estimate). |
| 698 | `op_expense_estimate_y1_cagr_4yr` | 0.5115 | 0 | 0 | Four-year compound annual growth rate for next fiscal year operating expense estimate. |
| 699 | `current_assets_estimate_q1_change_1mo` | 0.5114 | 0 | 0 | Change in the first quarter's current assets estimate over the past month. |
| 700 | `est_q1_sequential_cogs` | 0.5113 | 0 | 0 | Sequential quarter-over-quarter change in cost of goods sold estimates for the first quarter. |
| 701 | `actual_q1_qoq_book_value_ps` | 0.5081 | 1 | 1 | Quarter-over-quarter change in actual Q1 book value per share. |
| 702 | `estimate_year1_cagr4_cashflow_per_share` | 0.5075 | 0 | 0 | Four-year compound annual growth rate for cash flow per share estimates starting from the first forecast year. |
| 703 | `ebitdarep_estimate_trailing_twelve_months` | 0.5074 | 0 | 0 | Consensus reported EBITDA estimate for the trailing twelve months period. |
| 704 | `est_q1_asymmetry_gross_income` | 0.5074 | 0 | 0 | Asymmetry measure of gross income estimates for the most recent quarter. |
| 705 | `est_q1_coeff_var_gross_income` | 0.5074 | 1 | 1 | Coefficient of variation for gross income estimates in the most recent quarter. |
| 706 | `ebitdarep_q1_estimate_qoq_growth` | 0.5073 | 0 | 0 | Quarter-over-quarter growth in consensus reported EBITDA estimate for the first quarter. |
| 707 | `estimate_qtr_trail12mo_cash_invest` | 0.5063 | 0 | 0 | Trailing twelve-month quarterly cash flow from investing activities estimate. |
| 708 | `estimate_q1_change_1mo_free_cash_flow` | 0.506 | 0 | 0 | Change in first quarter free cash flow estimate over the past month. |
| 709 | `estimate_q1_qoq_cash_invest` | 0.5054 | 0 | 0 | Quarter-over-quarter change in Q1 cash flow from investing activities estimate. |
| 710 | `est_zscore_gross_income` | 0.5024 | 0 | 0 | Z-score of gross income estimate, showing how far the estimate is from the mean in standard deviations. |
| 711 | `est_q2_asymmetry_gross_income` | 0.5019 | 0 | 0 | Asymmetry measure of gross income estimates for the second quarter. |
| 712 | `est_q2_coeff_var_gross_income` | 0.5019 | 1 | 1 | Coefficient of variation for gross income estimates in the second quarter. |
| 713 | `estimate_y1_cagr5_depr_amort` | 0.5013 | 0 | 0 | Five-year compound annual growth rate for year 1 depreciation and amortization estimate. |
| 714 | `current_assets_estimate_year1_asymmetry` | 0.4984 | 0 | 0 | Asymmetry (skewness) of analyst current assets estimates for the next fiscal year. |
| 715 | `estimate_y1_coeffvar_currassets` | 0.4984 | 0 | 0 | Coefficient of variation for year 1 current assets estimate. |
| 716 | `estimate_q1_qoq_change_currassets` | 0.4965 | 0 | 0 | Quarter-over-quarter change in current assets estimate for the first quarter. |
| 717 | `estimate_trailing_12mo_currassets` | 0.4965 | 0 | 0 | Trailing twelve-month estimate for current assets. |
| 718 | `dividend_estimate_surprise_stddev` | 0.4955 | 0 | 0 | Standard deviation of the difference between actual and consensus dividend per share estimates (surprise). |
| 719 | `estimate_q1_quarterly_change_free_cash_flow` | 0.4946 | 0 | 0 | Quarter-over-quarter change in free cash flow estimate for the first quarter. |
| 720 | `estimate_trailing_twelve_months_free_cash_flow` | 0.4946 | 0 | 0 | Trailing twelve months free cash flow estimate based on analyst consensus. |
| 721 | `estimate_surprise_stddev_book_value_ps` | 0.4941 | 0 | 0 | Standard deviation of the surprise (actual minus estimate) for book value per share. |
| 722 | `dividend_estimate_year1_skewness` | 0.4939 | 0 | 0 | Skewness of analyst dividend per share estimates for the next fiscal year. |
| 723 | `dividend_estimate_year2_consensus` | 0.4939 | 0 | 0 | Consensus analyst estimate for dividend per share in the second forecast year. |
| 724 | `dividend_estimate_year2_change_3mo` | 0.4938 | 0 | 0 | Change in the second forecast year's dividend per share estimate over the past 3 months. |
| 725 | `estimate_y1_asymmetry_cash_invest` | 0.4934 | 0 | 0 | Asymmetry measure for year 1 cash flow from investing activities estimate distribution. |
| 726 | `estimate_y1_coeffvar_cash_invest` | 0.4934 | 0 | 0 | Coefficient of variation for year 1 cash flow from investing activities estimates. |
| 727 | `dividend_estimate_year1_change_3mo` | 0.4913 | 0 | 0 | Change in the next fiscal year's dividend per share estimate over the past 3 months. |
| 728 | `dividend_estimate_revision_magnitude` | 0.4912 | 0 | 0 | Magnitude of recent analyst revisions to dividend per share estimates. |
| 729 | `estimate_trend_slope_quaternary_gross_margin` | 0.4904 | 0 | 0 | Fourth-order slope of gross margin estimates, reflecting higher-order trend changes. |
| 730 | `estimate_volatility_adjusted_2yr_gross_margin` | 0.4895 | 0 | 0 | Gross margin estimate adjusted for volatility over a two-year period. |
| 731 | `quarter1_estimate_asymmetry_gpm` | 0.4886 | 0 | 0 | Asymmetry (third moment) of the consensus gross profit margin estimate distribution for the next quarter. |
| 732 | `quarter1_estimate_coeff_var_gpm` | 0.4886 | 0 | 0 | Coefficient of variation for the consensus gross profit margin estimate for the next quarter. |
| 733 | `estimate_y2_coeffvar_currassets` | 0.4878 | 0 | 0 | Coefficient of variation for year 2 current assets estimate. |
| 734 | `fwd_year1_estimate_cagr_5yr_gpm` | 0.4867 | 0 | 0 | Compound annual growth rate of the forward year 1 gross profit margin estimate over the last 5 years. |
| 735 | `estimate_q2_coeff_var_gross_margin` | 0.4864 | 0 | 0 | Coefficient of variation for gross margin estimates in the second quarter. |
| 736 | `estimate_year1_cagr4_free_cash_flow` | 0.4864 | 0 | 0 | Four-year compound annual growth rate for free cash flow estimates starting from the first forecast year. |
| 737 | `quarter2_estimate_asymmetry_gpm` | 0.4864 | 0 | 0 | Asymmetry (third moment) of the consensus gross profit margin estimate distribution for the second upcoming quarter. |
| 738 | `estimate_y2_coeffvar_cash_invest` | 0.4835 | 0 | 0 | Coefficient of variation for year 2 cash flow from investing activities estimates. |
| 739 | `estimate_surprise_difference_cashflow_per_share` | 0.4832 | 0 | 0 | Difference between actual and estimated cash flow per share, representing earnings surprise. |
| 740 | `estimate_trend_slope_mid_capex` | 0.4827 | 0 | 0 | Slope of the mid-term trend line for capital expenditure estimates. |
| 741 | `estimate_trend_slope_intermediate_capex` | 0.4825 | 0 | 0 | Slope of the intermediate-term trend line for capital expenditure estimates. |
| 742 | `estimate_volatility_adj3yr_depr_amort` | 0.4818 | 0 | 0 | Three-year volatility-adjusted value for depreciation and amortization estimates. |
| 743 | `capex_estimate_q1_yoy_growth` | 0.4812 | 0 | 0 | Year-over-year growth rate in current quarter capital expenditure estimate. |
| 744 | `estimate_surprise_difference` | 0.4812 | 0 | 0 | Difference between actual reported value and consensus estimate for the period. |
| 745 | `estimate_zscore_gross_margin` | 0.4792 | 0 | 0 | Z-score of the gross margin estimate relative to its historical distribution. |
| 746 | `ebitdarep_actual_q1_qoq_growth` | 0.479 | 0 | 0 | Quarter-over-quarter growth in reported EBITDA for the first quarter. |
| 747 | `estimate_year1_cagr4_operating_cashflow` | 0.4762 | 0 | 0 | Four-year compound annual growth rate for operating cash flow estimates starting from the first forecast year. |
| 748 | `estimate_trend_slope_secondary_cashflow_per_share` | 0.475 | 0 | 0 | Second-order slope of cash flow per share estimates, capturing acceleration or deceleration in trend. |
| 749 | `estimate_trend_slope_tertiary_cashflow_per_share` | 0.475 | 0 | 0 | Third-order slope of cash flow per share estimates, indicating curvature in the trend. |
| 750 | `dividend_estimate_surprise_difference` | 0.4743 | 1 | 1 | Difference between actual and consensus dividend per share estimate (surprise). |
| 751 | `estimate_q1_yearly_growth_cashflow_per_share` | 0.4736 | 1 | 1 | Year-over-year growth in cash flow per share estimate for the first quarter. |
| 752 | `dividend_estimate_year1_consensus` | 0.469 | 0 | 0 | Consensus analyst estimate for dividend per share in the next fiscal year. |
| 753 | `ebitdarep_estimate_surprise_stdev` | 0.4687 | 0 | 0 | Standard deviation of the difference between actual and forecasted reported EBITDA. |
| 754 | `ebitdarep_y1_estimate_cagr3` | 0.4683 | 0 | 0 | Three-year compound annual growth rate for consensus reported EBITDA estimate in year one. |
| 755 | `estimate_year1_asymmetry_cashflow_per_share` | 0.4673 | 0 | 0 | Asymmetry (skewness) of cash flow per share estimates for the first forecast year. |
| 756 | `estimate_year1_coeff_var_cashflow_per_share` | 0.4673 | 1 | 1 | Coefficient of variation for cash flow per share estimates in the first forecast year. |
| 757 | `nav_estimate_trend_slope_4yr` | 0.4671 | 0 | 0 | Slope of analyst consensus net asset value estimates over the last 4 years. |
| 758 | `nav_estimate_volatility_adj_2yr` | 0.467 | 0 | 0 | Volatility of net asset value estimates over the past 2 years, adjusted for scale or outliers. |
| 759 | `actual_q1_qoq_cash_invest` | 0.4669 | 1 | 1 | Quarter-over-quarter change in actual Q1 cash flow from investing activities. |
| 760 | `cogs_estimate_trend_slope4` | 0.4659 | 0 | 0 | Slope of the trend line for consensus cost of goods sold estimates over the last four periods. |
| 761 | `est_volatility_adj2yr_cogs` | 0.4659 | 0 | 0 | Two-year volatility-adjusted measure for cost of goods sold estimates, reflecting normalized forecast variability. |
| 762 | `estimate_year2_coeff_var_cashflow_per_share` | 0.4657 | 0 | 0 | Coefficient of variation for cash flow per share estimates in the second forecast year. |
| 763 | `actual_q1_quarterly_change_free_cash_flow` | 0.465 | 2 | 2 | Quarter-over-quarter change in actual free cash flow for the first quarter. |
| 764 | `cf_operating_estimate_q1_yoy_growth` | 0.4622 | 1 | 1 | Year-over-year growth rate in operating cash flow estimate for the first quarter. |
| 765 | `cf_operating_estimate_trend_slope_2yr` | 0.4622 | 1 | 1 | Slope of analyst consensus operating cash flow estimates over the last 2 years. |
| 766 | `cf_operating_estimate_trend_slope_3yr` | 0.4622 | 1 | 1 | Slope of analyst consensus operating cash flow estimates over the last 3 years. |
| 767 | `current_assets_actual_q1_qoq_growth` | 0.4606 | 2 | 2 | Quarter-over-quarter growth in actual reported current assets for the first quarter. |
| 768 | `interest_expense_5yr_cagr_estimate` | 0.4598 | 0 | 0 | Compound annual growth rate of interest expense over the past five years based on estimates. |
| 769 | `ebitdarep_estimate_surprise_diff` | 0.4595 | 0 | 0 | Difference between actual and consensus reported EBITDA estimate for a given period. |
| 770 | `estimate_y1_cagr4_cash_invest` | 0.4595 | 0 | 0 | Four-year compound annual growth rate for year 1 cash flow from investing activities estimate. |
| 771 | `estimate_surprise_stddev_currassets` | 0.4576 | 0 | 0 | Standard deviation of the difference between actual and forecasted current assets. |
| 772 | `estimate_surprise_stddev_free_cash_flow` | 0.4569 | 0 | 0 | Standard deviation of free cash flow surprises (actual minus estimate). |
| 773 | `estimate_year1_cagr5_cashflow_per_share` | 0.4564 | 0 | 0 | Five-year compound annual growth rate for cash flow per share estimates starting from the first forecast year. |
| 774 | `estimate_surprise_stddev_cash_invest` | 0.456 | 0 | 0 | Standard deviation of the surprise (actual minus estimate) for cash flow from investing activities. |
| 775 | `est_slope_4yr_gross_income` | 0.4547 | 0 | 0 | Slope of gross income estimates over the last 4 years, showing long-term trend direction. |
| 776 | `est_volatility_adj_2yr_gross_income` | 0.4547 | 0 | 0 | Volatility of gross income estimates adjusted over a 2-year period. |
| 777 | `capex_actual_q1_yoy_growth` | 0.454 | 0 | 0 | Year-over-year growth rate in actual capital expenditure for the most recent quarter. |
| 778 | `actual_q1_yearly_growth_cashflow_per_share` | 0.4536 | 1 | 1 | Year-over-year growth in actual cash flow per share for the first quarter. |
| 779 | `capex_estimate_q1_sequential` | 0.4525 | 0 | 0 | Sequential value or change in current quarter capital expenditure estimate. |
| 780 | `estimate_q1_yoy_book_value_ps` | 0.4521 | 0 | 0 | Year-over-year change in Q1 book value per share estimate. |
| 781 | `estimate_trend_slope3_book_value_ps` | 0.4521 | 0 | 0 | Third-order slope of the book value per share estimate trend. |
| 782 | `estimate_trend_slope_2yr` | 0.4521 | 1 | 1 | Slope of the consensus estimate trend over the past 2 years. |
| 783 | `estimate_q1_sequential_change_cashflow_per_share` | 0.452 | 0 | 0 | Sequential change in cash flow per share estimate for the first quarter compared to the previous quarter. |
| 784 | `current_assets_estimate_surprise_difference` | 0.4506 | 1 | 1 | Difference between actual and consensus current assets estimate (surprise). |
| 785 | `op_expense_estimate_volatility_3yr_adj` | 0.4506 | 0 | 0 | Three-year volatility of operating expense estimates, adjusted for outliers or structural breaks. |
| 786 | `estimate_surprise_difference_free_cash_flow` | 0.4492 | 0 | 0 | Difference between actual and estimated free cash flow, representing earnings surprise. |
| 787 | `est_y1_cagr_4yr_gross_income` | 0.449 | 0 | 0 | Compound annual growth rate of year 1 gross income estimate over the last 4 years. |
| 788 | `estimate_y1_cagr5_mktblsec` | 0.4471 | 0 | 0 | Five-year compound annual growth rate for year 1 marketable securities estimate. |
| 789 | `dividend_estimate_cagr2y_year1` | 0.4464 | 0 | 0 | Compound annual growth rate of dividend per share estimates over the last 2 years to the next year. |
| 790 | `estimate_surprise_diff_cash_invest` | 0.4455 | 0 | 0 | Difference between actual and estimated cash flow from investing activities (surprise). |
| 791 | `estimate_trend_slope4_mktblsec` | 0.4454 | 0 | 0 | Fourth slope coefficient from trend analysis of marketable securities estimates. |
| 792 | `estimate_volatility_adj2yr_mktblsec` | 0.4453 | 0 | 0 | Volatility of marketable securities estimates adjusted over a two-year period. |
| 793 | `estimate_volatility_adjusted_3yr_gross_margin` | 0.4396 | 0 | 0 | Gross margin estimate adjusted for volatility over a three-year period. |
| 794 | `cogs_y1_estimate_cagr4` | 0.4381 | 0 | 0 | Four-year compound annual growth rate for consensus cost of goods sold estimate in year one. |
| 795 | `actual_q1_yearly_growth_operating_cashflow` | 0.4338 | 2 | 2 | Year-over-year growth in actual operating cash flow for the first quarter. |
| 796 | `estimate_q1_sequential_change_operating_cashflow` | 0.4337 | 0 | 0 | Sequential change in operating cash flow estimate for the first quarter compared to the previous quarter. |
| 797 | `actual_q1_yoy_book_value_ps` | 0.4327 | 1 | 1 | Year-over-year change in actual Q1 book value per share. |
| 798 | `estimate_q1_sequential_book_value_ps` | 0.4327 | 1 | 1 | Sequential change in Q1 book value per share estimate. |
| 799 | `cf_operating_estimate_cagr5y_year1` | 0.4258 | 1 | 1 | Compound annual growth rate of operating cash flow estimates over the last 5 years to the next year. |
| 800 | `estimate_year1_cagr5_free_cash_flow` | 0.4251 | 0 | 0 | Five-year compound annual growth rate for free cash flow estimates starting from the first forecast year. |
| 801 | `dividend_estimate_cagr3y_year1` | 0.4224 | 0 | 0 | Compound annual growth rate of dividend per share estimates over the last 3 years to the next year. |
| 802 | `nav_estimate_q1_asymmetry` | 0.4193 | 1 | 1 | Asymmetry (skewness) of analyst net asset value estimates for the first quarter. |
| 803 | `nav_estimate_q1_coeff_var` | 0.4193 | 0 | 0 | Coefficient of variation for analyst net asset value estimates for the first quarter. |
| 804 | `dividend_estimate_trend_slope_1yr` | 0.419 | 0 | 0 | Slope of analyst consensus dividend per share estimates over the last year. |
| 805 | `cogs_estimate_volatility_adj_3yr` | 0.4171 | 0 | 0 | Volatility-adjusted measure of consensus cost of goods sold estimates over the past three years. |
| 806 | `op_expense_estimate_y1_cagr_5yr` | 0.417 | 0 | 0 | Five-year compound annual growth rate for next fiscal year operating expense estimate. |
| 807 | `dividend_estimate_trailing_4q_sum` | 0.4144 | 0 | 0 | Sum of the most recent four quarters of dividend per share estimates (trailing twelve months). |
| 808 | `dividend_estimate_q2_skewness` | 0.4129 | 0 | 0 | Skewness of analyst dividend per share estimates for the second quarter. |
| 809 | `dividend_estimate_q1_skewness` | 0.4124 | 0 | 0 | Skewness of analyst dividend per share estimates for the first quarter. |
| 810 | `dividend_estimate_q2_qoq_growth` | 0.4124 | 0 | 0 | Quarter-over-quarter growth in dividend per share estimate for the second quarter. |
| 811 | `ebitdarep_estimate_trend_slope2` | 0.4118 | 0 | 0 | Slope of the trend line for consensus reported EBITDA estimates over the last two periods. |
| 812 | `ebitdarep_estimate_trend_slope3` | 0.4118 | 0 | 0 | Slope of the trend line for consensus reported EBITDA estimates over the last three periods. |
| 813 | `ebitdarep_q1_estimate_yoy_growth` | 0.4118 | 0 | 0 | Year-over-year growth in consensus reported EBITDA estimate for the first quarter. |
| 814 | `ebitdarep_y2_estimate_coeff_var` | 0.4113 | 0 | 0 | Coefficient of variation for consensus reported EBITDA estimate in year two. |
| 815 | `ebitdarep_y1_estimate_asymmetry` | 0.4111 | 0 | 0 | Asymmetry measure of consensus reported EBITDA estimates for year one. |
| 816 | `ebitdarep_y1_estimate_coeff_var` | 0.4111 | 0 | 0 | Coefficient of variation for consensus reported EBITDA estimate in year one. |
| 817 | `current_assets_estimate_cagr4y_year1` | 0.411 | 0 | 0 | Compound annual growth rate of current assets estimates over the last 4 years to the next year. |
| 818 | `dividend_estimate_q1_change_1mo` | 0.4094 | 0 | 0 | Change in the first quarter's dividend per share estimate over the past month. |
| 819 | `est_volatility_adj_3yr_gross_income` | 0.409 | 0 | 0 | Volatility of gross income estimates adjusted over a 3-year period. |
| 820 | `estimate_q1_asymmetry_mktblsec` | 0.4089 | 0 | 0 | Asymmetry measure of analyst estimates for marketable securities in the first quarter. |
| 821 | `estimate_q1_coeffvar_mktblsec` | 0.4089 | 0 | 0 | Coefficient of variation for first quarter marketable securities estimate. |
| 822 | `nav_estimate_year1_zscore` | 0.4084 | 0 | 0 | Z-score of the next fiscal year's net asset value estimate relative to historical mean and standard deviation. |
| 823 | `dividend_estimate_year2_coeff_var` | 0.4072 | 0 | 0 | Coefficient of variation for analyst dividend per share estimates for the second forecast year. |
| 824 | `ebitdarep_y1_estimate_cagr4` | 0.4062 | 0 | 0 | Four-year compound annual growth rate for consensus reported EBITDA estimate in year one. |
| 825 | `nav_estimate_q2_asymmetry` | 0.4053 | 0 | 0 | Asymmetry (skewness) of analyst net asset value estimates for the second quarter. |
| 826 | `nav_estimate_q2_coeff_var` | 0.4053 | 0 | 0 | Coefficient of variation for analyst net asset value estimates for the second quarter. |
| 827 | `est_y1_cagr_5yr_gross_income` | 0.4048 | 0 | 0 | Compound annual growth rate of year 1 gross income estimate over the last 5 years. |
| 828 | `nav_estimate_volatility_adj_3yr` | 0.4017 | 0 | 0 | Volatility of net asset value estimates over the past 3 years, adjusted for outliers. |
| 829 | `estimate_trend_slope_quaternary_cashflow_per_share` | 0.3993 | 0 | 0 | Fourth-order slope of cash flow per share estimates, reflecting higher-order trend changes. |
| 830 | `estimate_volatility_adjusted_2yr_cashflow_per_share` | 0.3992 | 0 | 0 | Cash flow per share estimate adjusted for volatility over a two-year period. |
| 831 | `dividend_estimate_cagr4y_year1` | 0.399 | 0 | 0 | Compound annual growth rate of dividend per share estimates over the last 4 years to the next year. |
| 832 | `estimate_q2_asymmetry_mktblsec` | 0.3955 | 0 | 0 | Asymmetry measure of analyst estimates for marketable securities in the second quarter. |
| 833 | `estimate_q2_coeffvar_mktblsec` | 0.3955 | 0 | 0 | Coefficient of variation for second quarter marketable securities estimate. |
| 834 | `estimate_zscore_mktblsec` | 0.3949 | 0 | 0 | Z-score of marketable securities estimate relative to historical mean and standard deviation. |
| 835 | `dividend_estimate_q1_qoq_growth` | 0.3945 | 0 | 0 | Quarter-over-quarter growth in dividend per share estimate for the first quarter. |
| 836 | `estimate_q1_yearly_growth_free_cash_flow` | 0.3938 | 0 | 0 | Year-over-year growth in free cash flow estimate for the first quarter. |
| 837 | `estimate_trend_slope_secondary_free_cash_flow` | 0.3938 | 0 | 0 | Second-order slope of free cash flow estimates, capturing acceleration or deceleration in trend. |
| 838 | `estimate_trend_slope_tertiary_free_cash_flow` | 0.3938 | 0 | 0 | Third-order slope of free cash flow estimates, indicating curvature in the trend. |
| 839 | `est_y1_cagr5yr_cogs` | 0.3932 | 0 | 0 | Five-year compound annual growth rate for next fiscal year cost of goods sold estimates. |
| 840 | `estimate_q1_yoy_change_currassets` | 0.3891 | 0 | 0 | Year-over-year change in current assets estimate for the first quarter. |
| 841 | `estimate_trend_slope2_currassets` | 0.3891 | 0 | 0 | Second slope coefficient from trend analysis of current assets estimates. |
| 842 | `estimate_trend_slope3_currassets` | 0.3891 | 0 | 0 | Third slope coefficient from trend analysis of current assets estimates. |
| 843 | `capex_estimate_volatility_2yr_adj` | 0.3883 | 0 | 0 | Two-year volatility of capital expenditure estimates, adjusted for outliers or structural breaks. |
| 844 | `estimate_trend_slope_long_capex` | 0.3883 | 0 | 0 | Slope of the long-term trend line for capital expenditure estimates. |
| 845 | `capex_estimate_q1_asymmetry` | 0.3868 | 1 | 1 | Asymmetry (skewness) of the distribution of current quarter capital expenditure estimates. |
| 846 | `capex_estimate_q1_coeff_var` | 0.3868 | 1 | 1 | Coefficient of variation for current quarter capital expenditure estimate. |
| 847 | `estimate_y1_cagr5_cash_invest` | 0.3868 | 0 | 0 | Five-year compound annual growth rate for year 1 cash flow from investing activities estimate. |
| 848 | `dividend_estimate_year1_asymmetry` | 0.3858 | 0 | 0 | Asymmetry (skewness) of analyst dividend per share estimates for the next fiscal year. |
| 849 | `dividend_estimate_year1_coeff_var` | 0.3858 | 0 | 0 | Coefficient of variation for analyst dividend per share estimates for the next fiscal year. |
| 850 | `ebitdarep_actual_q1_yoy_growth` | 0.3843 | 0 | 0 | Year-over-year growth in reported EBITDA for the first quarter. |
| 851 | `ebitdarep_q1_estimate_sequential_growth` | 0.3843 | 0 | 0 | Sequential growth in consensus reported EBITDA estimate for the first quarter. |
| 852 | `estimate_trend_slope4_book_value_ps` | 0.3825 | 0 | 0 | Fourth-order slope of the book value per share estimate trend. |
| 853 | `estimate_volatility_adj2yr_book_value_ps` | 0.3825 | 0 | 0 | Two-year volatility-adjusted value for book value per share estimates. |
| 854 | `dividend_actual_q1_qoq_growth` | 0.3799 | 0 | 0 | Quarter-over-quarter growth in actual reported dividend per share for the first quarter. |
| 855 | `dividend_estimate_cagr5y_year1` | 0.3763 | 0 | 0 | Compound annual growth rate of dividend per share estimates over the last 5 years to the next year. |
| 856 | `capex_estimate_zscore` | 0.3759 | 1 | 1 | Z-score of the current capital expenditure estimate relative to its historical mean and standard deviation. |
| 857 | `estimate_trend_slope2_cash_invest` | 0.3759 | 0 | 0 | Second-order slope of the cash flow from investing activities estimate trend. |
| 858 | `estimate_trend_slope3_cash_invest` | 0.3759 | 0 | 0 | Third-order slope of the cash flow from investing activities estimate trend. |
| 859 | `estimate_q1_yoy_cash_invest` | 0.3755 | 0 | 0 | Year-over-year change in Q1 cash flow from investing activities estimate. |
| 860 | `capex_estimate_q2_asymmetry` | 0.3749 | 1 | 1 | Asymmetry (skewness) of the distribution of second quarter capital expenditure estimates. |
| 861 | `capex_q2_estimate_coeff_var` | 0.3749 | 0 | 0 | Coefficient of variation for consensus capital expenditure estimate in the second quarter. |
| 862 | `estimate_volatility_adj3yr_mktblsec` | 0.3692 | 0 | 0 | Volatility of marketable securities estimates adjusted over a three-year period. |
| 863 | `actual_q1_yearly_growth_free_cash_flow` | 0.369 | 4 | 4 | Year-over-year growth in actual free cash flow for the first quarter. |
| 864 | `estimate_q1_sequential_change_free_cash_flow` | 0.3689 | 0 | 0 | Sequential change in free cash flow estimate for the first quarter compared to the previous quarter. |
| 865 | `current_assets_actual_q1_yoy_growth` | 0.3651 | 0 | 0 | Year-over-year growth in actual reported current assets for the first quarter. |
| 866 | `estimate_q1_sequential_currassets` | 0.3651 | 0 | 0 | Sequential change in current assets estimate for the first quarter. |
| 867 | `dividend_estimate_trend_slope_2yr` | 0.3604 | 0 | 0 | Slope of analyst consensus dividend per share estimates over the last 2 years. |
| 868 | `dividend_estimate_trend_slope_3yr` | 0.3554 | 0 | 0 | Slope of analyst consensus dividend per share estimates over the last 3 years. |
| 869 | `estimate_y1_cagr5_currassets` | 0.355 | 0 | 0 | Five-year compound annual growth rate for year 1 current assets estimate. |
| 870 | `cf_operating_estimate_trend_slope_4yr` | 0.3511 | 0 | 0 | Slope of analyst consensus operating cash flow estimates over the last 4 years, indicating long-term trend. |
| 871 | `cf_operating_estimate_volatility_adj_2yr` | 0.3511 | 0 | 0 | Volatility of operating cash flow estimates over the past 2 years, adjusted for scale or outliers. |
| 872 | `actual_q1_yoy_cash_invest` | 0.3456 | 2 | 2 | Year-over-year change in actual Q1 cash flow from investing activities. |
| 873 | `estimate_q1_sequential_cash_invest` | 0.3452 | 0 | 0 | Sequential change in Q1 cash flow from investing activities estimate. |
| 874 | `dividend_estimate_q1_yoy_growth` | 0.3448 | 0 | 0 | Year-over-year growth rate in dividend per share estimate for the first quarter. |
| 875 | `cf_operating_estimate_q1_asymmetry` | 0.3422 | 2 | 9 | Asymmetry (skewness) of analyst operating cash flow estimates for the first quarter. |
| 876 | `cf_operating_estimate_q1_coeff_var` | 0.3422 | 2 | 3 | Coefficient of variation for analyst operating cash flow estimates for the first quarter. |
| 877 | `estimate_volatility_adjusted_3yr_cashflow_per_share` | 0.3411 | 0 | 0 | Cash flow per share estimate adjusted for volatility over a three-year period. |
| 878 | `ebitdarep_y1_estimate_cagr5` | 0.3409 | 0 | 0 | Five-year compound annual growth rate for consensus reported EBITDA estimate in year one. |
| 879 | `estimate_zscore_operating_cashflow` | 0.335 | 1 | 1 | Z-score of the operating cash flow estimate relative to its historical distribution. |
| 880 | `dividend_actual_q1_yoy_growth` | 0.3314 | 0 | 0 | Year-over-year growth in actual reported dividend per share for the first quarter. |
| 881 | `estimate_volatility_adj3yr_book_value_ps` | 0.3302 | 0 | 0 | Three-year volatility-adjusted value for book value per share estimates. |
| 882 | `cf_operating_estimate_q2_asymmetry` | 0.3298 | 0 | 0 | Asymmetry (skewness) of analyst operating cash flow estimates for the second quarter. |
| 883 | `estimate_q2_coeff_var_operating_cashflow` | 0.3298 | 0 | 0 | Coefficient of variation for operating cash flow estimates in the second quarter. |
| 884 | `capex_estimate_volatility_3yr_adj` | 0.325 | 0 | 0 | Three-year volatility of capital expenditure estimates, adjusted for outliers or structural breaks. |
| 885 | `dividend_estimate_q1_sequential_growth` | 0.3243 | 0 | 0 | Sequential quarter-over-quarter growth in dividend per share estimate for the first quarter. |
| 886 | `ebitdarep_estimate_trend_slope4` | 0.3172 | 0 | 0 | Slope of the trend line for consensus reported EBITDA estimates over the last four periods. |
| 887 | `ebitdarep_estimate_volatility_adj_2yr` | 0.3171 | 0 | 0 | Volatility-adjusted measure of consensus reported EBITDA estimates over the past two years. |
| 888 | `dividend_estimate_trend_slope_4yr` | 0.3105 | 0 | 0 | Slope of analyst consensus dividend per share estimates over the last 4 years. |
| 889 | `estimate_trend_slope4_currassets` | 0.306 | 0 | 0 | Fourth slope coefficient from trend analysis of current assets estimates. |
| 890 | `estimate_volatility_adj2yr_currassets` | 0.306 | 0 | 0 | Volatility of current assets estimates adjusted over a two-year period. |
| 891 | `estimate_trend_slope_quaternary_free_cash_flow` | 0.296 | 0 | 0 | Fourth-order slope of free cash flow estimates, reflecting higher-order trend changes. |
| 892 | `estimate_volatility_adjusted_2yr_free_cash_flow` | 0.2959 | 0 | 0 | Free cash flow estimate adjusted for volatility over a two-year period. |
| 893 | `cf_operating_estimate_volatility_adj_3yr` | 0.2947 | 0 | 0 | Volatility of operating cash flow estimates over the past 3 years, adjusted for outliers or scale. |
| 894 | `estimate_q1_asymmetry_free_cash_flow` | 0.2937 | 0 | 0 | Asymmetry (skewness) of free cash flow estimates for the first quarter. |
| 895 | `estimate_q1_coeff_var_free_cash_flow` | 0.2937 | 1 | 1 | Coefficient of variation for free cash flow estimates in the first quarter. |
| 896 | `estimate_q1_asymmetry_cashflow_per_share` | 0.2931 | 0 | 0 | Asymmetry (skewness) of cash flow per share estimates for the first quarter. |
| 897 | `estimate_q1_coeff_var_cashflow_per_share` | 0.2931 | 0 | 0 | Coefficient of variation for cash flow per share estimates in the first quarter. |
| 898 | `estimate_zscore_cashflow_per_share` | 0.287 | 0 | 0 | Z-score of the cash flow per share estimate relative to its historical distribution. |
| 899 | `estimate_q2_asymmetry_cashflow_per_share` | 0.2864 | 0 | 0 | Asymmetry (skewness) of cash flow per share estimates for the second quarter. |
| 900 | `estimate_q2_coeff_var_cashflow_per_share` | 0.2864 | 0 | 0 | Coefficient of variation for cash flow per share estimates in the second quarter. |
| 901 | `estimate_zscore_free_cash_flow` | 0.2862 | 0 | 0 | Z-score of the free cash flow estimate relative to its historical distribution. |
| 902 | `estimate_q2_asymmetry_free_cash_flow` | 0.2819 | 0 | 0 | Asymmetry (skewness) of free cash flow estimates for the second quarter. |
| 903 | `estimate_q2_coeff_var_free_cash_flow` | 0.2819 | 0 | 0 | Coefficient of variation for free cash flow estimates in the second quarter. |
| 904 | `dividend_estimate_volatility_adj_2yr` | 0.2785 | 0 | 0 | Volatility of dividend per share estimates over the past 2 years, adjusted for scale or outliers. |
| 905 | `ebitdarep_q1_estimate_asymmetry` | 0.278 | 0 | 0 | Asymmetry measure of consensus reported EBITDA estimates for the first quarter. |
| 906 | `ebitdarep_q1_estimate_coeff_var` | 0.278 | 0 | 0 | Coefficient of variation for consensus reported EBITDA estimate in the first quarter. |
| 907 | `estimate_q1_asymmetry_currassets` | 0.2681 | 1 | 1 | Asymmetry measure of analyst estimates for current assets in the first quarter. |
| 908 | `estimate_q1_coeffvar_currassets` | 0.2681 | 0 | 0 | Coefficient of variation for first quarter current assets estimate. |
| 909 | `ebitdarep_q2_estimate_asymmetry` | 0.2677 | 0 | 0 | Asymmetry measure of consensus reported EBITDA estimates for the second quarter. |
| 910 | `ebitdarep_q2_estimate_coeff_var` | 0.2677 | 0 | 0 | Coefficient of variation for consensus reported EBITDA estimate in the second quarter. |
| 911 | `estimate_trend_slope4_cash_invest` | 0.2661 | 1 | 1 | Fourth-order slope of the cash flow from investing activities estimate trend. |
| 912 | `estimate_volatility_adj2yr_cash_invest` | 0.266 | 0 | 0 | Two-year volatility-adjusted value for cash flow from investing activities estimates. |
| 913 | `ebitdarep_estimate_zscore` | 0.2641 | 0 | 0 | Z-score of the consensus reported EBITDA estimate relative to its historical mean and standard deviation. |
| 914 | `dividend_estimate_volatility_adj_3yr` | 0.2599 | 0 | 0 | Volatility of dividend per share estimates over the past 3 years, adjusted for outliers. |
| 915 | `estimate_zscore_currassets` | 0.2589 | 0 | 0 | Z-score of current assets estimate relative to historical mean and standard deviation. |
| 916 | `estimate_q2_asymmetry_currassets` | 0.2582 | 1 | 1 | Asymmetry measure of analyst estimates for current assets in the second quarter. |
| 917 | `estimate_q2_coeffvar_currassets` | 0.2582 | 0 | 0 | Coefficient of variation for second quarter current assets estimate. |
| 918 | `ebitdarep_estimate_volatility_adj_3yr` | 0.2567 | 0 | 0 | Volatility-adjusted measure of consensus reported EBITDA estimates over the past three years. |
| 919 | `dividend_estimate_q2_asymmetry` | 0.256 | 0 | 0 | Asymmetry (skewness) of analyst dividend per share estimates for the second quarter. |
| 920 | `dividend_estimate_q2_coeff_var` | 0.256 | 0 | 0 | Coefficient of variation for analyst dividend per share estimates for the second quarter. |
| 921 | `estimate_q1_asymmetry_cash_invest` | 0.2558 | 0 | 0 | Asymmetry measure for Q1 cash flow from investing activities estimate distribution. |
| 922 | `estimate_q1_coeffvar_cash_invest` | 0.2558 | 0 | 0 | Coefficient of variation for Q1 cash flow from investing activities estimates. |
