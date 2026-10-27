# analyst_factor_signals — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst_factor_signals` |
| 名称 | Global Analyst Factor Signals |
| 类别 | ANALYST |
| 数据字段数(平台) | 108 |
| 覆盖率 | 0.5458 |
| 平台已有 alpha | 69 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive suite of analyst-derived quantitative factors and indicators for global equities, constructed using standardized methodologies. It leverages consensus estimates, actuals, and revision data from multiple sources to generate a wide range of predictive signals, such as estimate momentum, earnings surprise, and analyst recommendation trends. The dataset is designed to be comparable across regions and time, with rigorous data cleaning and normalization. By offering both raw and composite factors—similar to those used in established quantitative models—this resource enables users to systematically test and implement alpha strategies, enhance risk models, and improve the forecasting of price movements based on analyst behavior and expectations.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **108** |
| 类型分布 | MATRIX×108 |
| 平均覆盖率 | **0.546** |
| 覆盖率区间 | 0.18 ~ 0.94 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 18 | 16.7% |
| 中 (0.70–0.90) | 18 | 16.7% |
| 低 (0.50–0.70) | 8 | 7.4% |
| 稀疏 (<0.50) | 64 | 59.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 69 | 63.9% |
| UNTESTED | 33 | 30.6% |
| DEAD | 6 | 5.6% |

- 已实测字段：**6** 个（6%），best_sharpe 最高 **0.31**，中位 -0.18

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 85 | 0.54 | revenue_y1_estimate_asymmetry、eps_y2_consensus_value、eps_y1_estimate_asymmetry |
| 盈利与财务 | 15 | 0.56 | revenue_y1_cagr_2yr、netprofit_y1_cagr_2yr_alt、revenue_y1_cagr_3yr |
| 其他 | 8 | 0.55 | eps_y1_cagr_2yr、eps_y1_cagr_3yr、eps_y1_cagr_4yr |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `revenue_y1_estimate_asymmetry` | MATRIX | 0.861 | 修正与预期 | 1 | 0.31 | -0.59 | 0.08 | DEAD | Asymmetry measure of the forecast FY1 revenue estimate distribution from analysts |
| 2 | `eps_y2_consensus_value` | MATRIX | 0.936 | 修正与预期 | 2 | -0.04 | 0.80 | -0.15 | DEAD | Forecast FY2 EPS growth rate |
| 3 | `eps_y1_estimate_asymmetry` | MATRIX | 0.870 | 修正与预期 | 1 | -0.18 | 0.03 | 0.08 | DEAD | Asymmetry measure of the distribution of FY1 EPS forecasts |
| 4 | `eps_y2_estimate_change_3mo` | MATRIX | 0.931 | 修正与预期 | 3 | -0.23 | 0.05 | 0.16 | DEAD | Change in consensus FY2 EPS forecast over the past 3 months |
| 5 | `netprofit_y1_estimate_asymmetry` | MATRIX | 0.848 | 修正与预期 | 1 | -0.38 | 0.18 | -0.41 | DEAD | Asymmetry of forecast FY1 net profit estimate distribution |
| 6 | `netprofit_y2_estimate_change_3mo` | MATRIX | 0.927 | 修正与预期 | 1 | -0.46 | -0.87 | -0.14 | DEAD | Three-month change in the consensus forecast for FY2 net profit |
| 7 | `eps_y1_estimate_skewness` | MATRIX | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Pearson skewness of the FY1 EPS forecast distribution |
| 8 | `revenue_y1_estimate_skewness` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Pearson's skewness of the FY1 revenue forecast distribution |
| 9 | `revenue_y2_consensus_value` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast growth for FY2 revenue |
| 10 | `netprofit_y1_estimate_skewness_alt` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Pearson’s skewness of forecast FY1 net profit estimates |
| 11 | `netprofit_y2_consensus_value` | MATRIX | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast FY2 net profit growth |
| 12 | `eps_revision_magnitude` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Scaled magnitude of revisions to FY1 EPS (Street revision magnitude) |
| 13 | `eps_y1_estimate_change_3mo` | MATRIX | 0.931 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in consensus FY1 EPS forecast over the past 3 months |
| 14 | `revenue_y2_estimate_change_3mo` | MATRIX | 0.928 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in consensus forecast for FY2 revenue over the past 3 months |
| 15 | `revenue_revision_magnitude` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Scaled revision magnitude of the median FY1 revenue estimate (Street Revision Magnitude) |
| 16 | `revenue_y1_estimate_change_3mo` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in FY1 revenue consensus forecast over the past 3 months |
| 17 | `netprofit_revision_magnitude` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Revision magnitude of median FY1 net profit estimates (Street revision magnitude) |
| 18 | `netprofit_y1_estimate_change_3mo` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month change in the FY1 consensus net profit forecast |
| 19 | `eps_y1_consensus_value` | MATRIX | 0.911 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast FY1 EPS growth rate |
| 20 | `revenue_y1_consensus_value` | MATRIX | 0.908 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast growth for FY1 revenue |
| 21 | `netprofit_y1_consensus_value` | MATRIX | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast FY1 net profit growth |
| 22 | `eps_y1_estimate_coeff_var` | MATRIX | 0.870 | 修正与预期 | 0 | — | — | — | UNTESTED | Coefficient of variation (std/mean) of consensus FY1 EPS estimates |
| 23 | `eps_y2_estimate_coeff_var` | MATRIX | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Coefficient of variation (std/mean) of FY2 EPS estimates |
| 24 | `revenue_y1_estimate_coeff_var` | MATRIX | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Coefficient of variation (std/mean) of FY1 revenue estimates |
| 25 | `revenue_y2_estimate_coeff_var` | MATRIX | 0.861 | 修正与预期 | 0 | — | — | — | UNTESTED | Coefficient of variation (std/mean) of FY2 revenue estimates |
| 26 | `netprofit_y2_estimate_coeff_var` | MATRIX | 0.848 | 修正与预期 | 0 | — | — | — | UNTESTED | Coefficient of variation of FY2 net profit estimates from analysts |
| 27 | `netprofit_y1_estimate_volatility_adj_1yr` | MATRIX | 0.848 | 修正与预期 | 0 | — | — | — | UNTESTED | Coefficient of variation (standard deviation divided by mean) of analyst FY1 net profit estimates |
| 28 | `eps_y1_cagr_2yr` | MATRIX | 0.847 | 其他 | 0 | — | — | — | UNTESTED | Forecast FY1 EPS growth CAGR over 2 years |
| 29 | `revenue_y1_cagr_2yr` | MATRIX | 0.842 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast compound annual growth rate to FY1 revenue measured over a 2-year horizon |
| 30 | `netprofit_y1_cagr_2yr_alt` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast FY1 net profit growth CAGR measured over 2 years |
| 31 | `eps_y1_cagr_3yr` | MATRIX | 0.778 | 其他 | 0 | — | — | — | UNTESTED | Forecast FY1 EPS growth CAGR over 3 years |
| 32 | `revenue_y1_cagr_3yr` | MATRIX | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast compound annual growth rate to FY1 revenue measured over a 3-year horizon |
| 33 | `netprofit_y1_cagr_3yr` | MATRIX | 0.770 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast FY1 net profit growth CAGR measured over 3 years |
| 34 | `eps_y1_cagr_4yr` | MATRIX | 0.714 | 其他 | 0 | — | — | — | UNTESTED | Forecast FY1 EPS growth CAGR over 4 years |
| 35 | `revenue_y1_cagr_4yr` | MATRIX | 0.706 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast compound annual growth rate to FY1 revenue measured over a 4-year horizon |
| 36 | `netprofit_y1_cagr_4yr` | MATRIX | 0.704 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast FY1 net profit growth CAGR measured over 4 years |
| 37 | `eps_y1_cagr_5yr` | MATRIX | 0.655 | 其他 | 0 | — | — | — | UNTESTED | Forecast FY1 EPS growth CAGR over 5 years |
| 38 | `revenue_y1_cagr_5yr` | MATRIX | 0.646 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast compound annual growth rate to FY1 revenue measured over a 5-year horizon |
| 39 | `netprofit_y1_cagr_5yr` | MATRIX | 0.643 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast FY1 net profit growth CAGR measured over 5 years |
| 40 | `revenue_estimate_trend_slope_1yr` | MATRIX | 0.560 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the 1-year consensus revenue forecast (quarterly), indicating trend |
| 41 | `revenue_q1_estimate_skewness` | MATRIX | 0.560 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pearson's skewness of the analyst forecast distribution for fiscal Q1 revenue |
| 42 | `revenue_q2_estimate_qoq_growth` | MATRIX | 0.560 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast Q2 revenue growth quarter-over-quarter |
| 43 | `revenue_q2_estimate_skewness` | MATRIX | 0.560 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pearson's skewness of the analyst forecast distribution for fiscal Q2 revenue |
| 44 | `revenue_q1_estimate_change_1mo` | MATRIX | 0.524 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in consensus forecast for fiscal Q1 revenue over the past 1 month |
| 45 | `revenue_trailing_4q_estimate` | MATRIX | 0.480 | 修正与预期 | 0 | — | — | — | UNUSABLE | Trailing-twelve-month forecast revenue growth |
| 46 | `revenue_q1_estimate_qoq_growth` | MATRIX | 0.479 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast Q1 revenue growth quarter-over-quarter |
| 47 | `eps_estimate_trend_slope_1yr` | MATRIX | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the 1-year consensus EPS forecast time series (quarterly) |
| 48 | `eps_q1_estimate_skewness` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pearson skewness of the Q1 EPS forecast distribution |
| 49 | `eps_q2_estimate_qoq_growth` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast Q2 EPS growth quarter over quarter |
| 50 | `eps_q2_estimate_skewness` | MATRIX | 0.475 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pearson's skewness of the forecast Q2 EPS estimate distribution |
| 51 | `netprofit_estimate_trend_slope_1yr` | MATRIX | 0.466 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the 1-year consensus net profit forecast series (quarterly) |
| 52 | `netprofit_q1_estimate_skewness` | MATRIX | 0.466 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pearson’s skewness of forecast Q1 net profit estimates |
| 53 | `netprofit_q2_estimate_qoq_growth` | MATRIX | 0.466 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast quarter-over-quarter growth for Q2 net profit |
| 54 | `netprofit_q2_estimate_skewness` | MATRIX | 0.465 | 修正与预期 | 0 | — | — | — | UNUSABLE | Pearson’s skewness of forecast Q2 net profit estimates |
| 55 | `eps_q1_estimate_change_1mo` | MATRIX | 0.461 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in consensus EPS forecast for fiscal Q1 over the past 1 month |
| 56 | `revenue_actual_q1_qoq_growth` | MATRIX | 0.441 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual Q1 revenue growth quarter over quarter |
| 57 | `netprofit_q1_estimate_change_1mo` | MATRIX | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | 1-month change in the Q1 consensus net profit forecast |
| 58 | `eps_trailing_4q_estimate` | MATRIX | 0.425 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast trailing-twelve-month EPS growth |
| 59 | `eps_q1_estimate_qoq_growth` | MATRIX | 0.425 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast Q1 EPS growth quarter over quarter |
| 60 | `revenue_q1_estimate_asymmetry` | MATRIX | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Asymmetry measure of the analyst forecast distribution for fiscal Q1 revenue |
| 61 | `revenue_q1_estimate_coeff_var` | MATRIX | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Coefficient of variation (std/mean) of Q1 revenue estimates |
| 62 | `eps_actual_q1_qoq_growth` | MATRIX | 0.398 | 其他 | 0 | — | — | — | UNUSABLE | Actual reported Q1 EPS growth quarter over quarter |
| 63 | `revenue_surprise_stddev` | MATRIX | 0.397 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of revenue surprise |
| 64 | `netprofit_trailing_4q_estimate_alt` | MATRIX | 0.396 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast trailing-twelve-month growth in net profit |
| 65 | `netprofit_q1_estimate_qoq_growth_alt` | MATRIX | 0.396 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast quarter-over-quarter growth for Q1 net profit |
| 66 | `revenue_surprise_mean_diff` | MATRIX | 0.389 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Difference between Q1 and Q2 revenue surprise metrics (Q1 minus Q2) |
| 67 | `revenue_q2_estimate_asymmetry` | MATRIX | 0.380 | 修正与预期 | 0 | — | — | — | UNUSABLE | Asymmetry measure of the forecast Q2 revenue estimate distribution from analysts |
| 68 | `revenue_q2_estimate_coeff_var` | MATRIX | 0.380 | 修正与预期 | 0 | — | — | — | UNUSABLE | Coefficient of variation (std/mean) of Q2 revenue estimates |
| 69 | `revenue_estimate_zscore` | MATRIX | 0.368 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standardized z-score of the fiscal Q1 revenue surprise |
| 70 | `revenue_estimate_trend_slope_2yr` | MATRIX | 0.364 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the linear trend in consensus revenue estimates over the past 2 years. |
| 71 | `eps_surprise_stddev` | MATRIX | 0.364 | 其他 | 0 | — | — | — | UNUSABLE | Standard deviation of EPS surprises |
| 72 | `revenue_estimate_trend_slope_3yr` | MATRIX | 0.364 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the linear trend in consensus revenue estimates over the past 3 years. |
| 73 | `revenue_q1_estimate_yoy_growth` | MATRIX | 0.364 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast year-over-year growth for fiscal Q1 revenue |
| 74 | `netprofit_actual_q1_qoq_growth` | MATRIX | 0.362 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual quarter-over-quarter growth for Q1 net profit |
| 75 | `eps_surprise_mean_diff` | MATRIX | 0.355 | 其他 | 0 | — | — | — | UNUSABLE | Difference in EPS surprise between Q1 and Q2 (Q1 minus Q2) |
| 76 | `revenue_actual_q1_yoy_growth` | MATRIX | 0.343 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual Q1 revenue growth year over year |
| 77 | `revenue_q1_estimate_sequential` | MATRIX | 0.343 | 修正与预期 | 0 | — | — | — | UNUSABLE | Difference between sequential forecast and actual revenue growth for Q1 |
| 78 | `netprofit_surprise_stddev` | MATRIX | 0.342 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of historical net profit surprises (actual minus consensus). |
| 79 | `netprofit_q1_estimate_asymmetry` | MATRIX | 0.340 | 修正与预期 | 0 | — | — | — | UNUSABLE | Asymmetry of forecast Q1 net profit estimate distribution |
| 80 | `netprofit_q1_estimate_coeff_var` | MATRIX | 0.340 | 修正与预期 | 0 | — | — | — | UNUSABLE | Coefficient of variation (std/mean) of Q1 consensus net profit estimates |
| 81 | `netprofit_surprise_mean_diff` | MATRIX | 0.336 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Difference in net profit surprise between Q1 and Q2 (Q1 minus Q2) |
| 82 | `eps_q1_estimate_asymmetry` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Asymmetry of the distribution of consensus Q1 EPS estimates |
| 83 | `eps_q1_estimate_coeff_var` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | Coefficient of variation of Q1 EPS consensus estimates |
| 84 | `eps_estimate_trend_slope_2yr` | MATRIX | 0.334 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the combined consensus forecast and actual EPS series (quarterly) |
| 85 | `eps_estimate_trend_slope_3yr` | MATRIX | 0.334 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the current actual EPS series over the past year (quarterly) |
| 86 | `eps_q1_estimate_yoy_growth` | MATRIX | 0.334 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast Q1 EPS growth year over year |
| 87 | `eps_estimate_zscore` | MATRIX | 0.320 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standardized EPS surprise z-score for Q1 |
| 88 | `netprofit_estimate_zscore` | MATRIX | 0.318 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standardized surprise (z-score) for Q1 net profit versus consensus |
| 89 | `eps_actual_q1_yoy_growth` | MATRIX | 0.317 | 其他 | 0 | — | — | — | UNUSABLE | Actual EPS growth for fiscal Q1, year-over-year |
| 90 | `eps_q2_estimate_asymmetry` | MATRIX | 0.317 | 修正与预期 | 0 | — | — | — | UNUSABLE | Asymmetry measure of the distribution of Q2 EPS forecasts |
| 91 | `eps_q2_estimate_coeff_var` | MATRIX | 0.317 | 修正与预期 | 0 | — | — | — | UNUSABLE | Coefficient of variation (std/mean) of Q2 EPS estimates |
| 92 | `eps_q1_estimate_sequential` | MATRIX | 0.316 | 修正与预期 | 0 | — | — | — | UNUSABLE | Difference between sequentially forecast and actual EPS growth for Q1 |
| 93 | `netprofit_q2_estimate_asymmetry` | MATRIX | 0.304 | 修正与预期 | 0 | — | — | — | UNUSABLE | Asymmetry (difference between mean and median) of second quarter net profit consensus estimates. |
| 94 | `netprofit_q2_estimate_coeff_var` | MATRIX | 0.304 | 修正与预期 | 0 | — | — | — | UNUSABLE | Coefficient of variation of Q2 net profit estimates from analysts |
| 95 | `netprofit_estimate_trend_slope_2yr` | MATRIX | 0.288 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the combined series of consensus net profit forecasts and actuals (quarterly) |
| 96 | `netprofit_estimate_trend_slope_3yr` | MATRIX | 0.288 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the current actual 1-year quarterly net profit series |
| 97 | `netprofit_q1_estimate_yoy_growth` | MATRIX | 0.288 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast year-over-year growth for Q1 net profit |
| 98 | `revenue_estimate_trend_slope_4yr` | MATRIX | 0.286 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the current actual 2-year revenue series (quarterly), indicating longer-term trend |
| 99 | `revenue_estimate_volatility_adj_2yr` | MATRIX | 0.285 | 修正与预期 | 0 | — | — | — | UNUSABLE | Volatility-adjusted 2-year projected revenue growth |
| 100 | `netprofit_actual_q1_yoy_growth` | MATRIX | 0.272 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual year-over-year growth for Q1 net profit |
| 101 | `netprofit_q1_estimate_sequential` | MATRIX | 0.272 | 修正与预期 | 0 | — | — | — | UNUSABLE | Sequential value of first quarter net profit consensus estimate (for time series analysis). |
| 102 | `eps_estimate_trend_slope_4yr` | MATRIX | 0.268 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the current actual 2-year EPS series (quarterly) |
| 103 | `eps_estimate_volatility_adj_2yr` | MATRIX | 0.268 | 修正与预期 | 0 | — | — | — | UNUSABLE | Volatility-adjusted 2-year projected EPS growth |
| 104 | `revenue_estimate_volatility_adj_3yr` | MATRIX | 0.230 | 修正与预期 | 0 | — | — | — | UNUSABLE | Volatility-adjusted 3-year projected revenue growth |
| 105 | `netprofit_estimate_trend_slope_4yr_alt` | MATRIX | 0.222 | 修正与预期 | 0 | — | — | — | UNUSABLE | Slope of the current actual 2-year quarterly net profit series |
| 106 | `netprofit_estimate_volatility_adj_2yr` | MATRIX | 0.222 | 修正与预期 | 0 | — | — | — | UNUSABLE | Volatility-adjusted projected 2-year growth in net profit |
| 107 | `eps_estimate_volatility_adj_3yr` | MATRIX | 0.219 | 修正与预期 | 0 | — | — | — | UNUSABLE | Volatility of consensus EPS estimates over the past 3 years, adjusted for scale. |
| 108 | `netprofit_estimate_volatility_adj_3yr` | MATRIX | 0.178 | 修正与预期 | 0 | — | — | — | UNUSABLE | Volatility-adjusted projected 3-year growth in net profit |

## 六、本地回测证据

- 本地累计回测 **9** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `npd7KAAw` | 0.31 | 0.08 | -0.59 | 0.08 | 0.05 | ["LOW_SHARPE | 243 | `divide(revenue_y1_estimate_asymmetry, add(abs(netprofit_y1_estimate_skewness_alt), 0.01))` |
| `xA3jYlYg` | -0.04 | -0.01 | 0.80 | -0.15 | 0.06 | ["LOW_SHARPE | 243 | `divide(ts_delta(subtract(eps_y2_consensus_value, eps_y1_consensus_value), 66), ts_mean(eps` |
| `Wjb7PYPG` | -0.04 | -0.01 | 0.78 | -0.23 | 0.06 | ["LOW_SHARPE | 243 | `divide(ts_delta(subtract(eps_y2_consensus_value, netprofit_y1_consensus_value), 66), ts_me` |
| `QPb73YKW` | -0.18 | -0.03 | 0.03 | 0.08 | 0.05 | ["LOW_SHARPE | 243 | `divide(eps_y1_estimate_asymmetry, add(abs(netprofit_y1_estimate_skewness_alt), 0.01))` |
| `ZYb70mmd` | -0.23 | -0.11 | -0.20 | 0.16 | 0.06 | ["LOW_SHARPE | 243 | `divide(subtract(ts_backfill(eps_y2_estimate_change_3mo,66), ts_backfill(netprofit_y1_estim` |
| `npd7KAvw` | -0.31 | -0.17 | 0.05 | -0.12 | 0.05 | ["LOW_SHARPE | 243 | `divide(subtract(ts_backfill(eps_y2_estimate_change_3mo,66), ts_backfill(revenue_y1_estimat` |
| `LLN795Z6` | -0.38 | -0.10 | 0.18 | -0.41 | 0.05 | ["LOW_SHARPE | 243 | `divide(netprofit_y1_estimate_asymmetry, add(abs(netprofit_y1_estimate_skewness_alt), 0.01)` |
| `58zlQjzJ` | -0.46 | -0.30 | -0.87 | -0.14 | 0.18 | ["LOW_SHARPE | 243 | `group_count(netprofit_y2_estimate_change_3mo, sector)` |
| `1YXwxjNW` | -0.54 | -0.44 | -0.57 | 0.00 | 0.06 | ["LOW_SHARPE | 243 | `divide(subtract(ts_backfill(eps_y2_estimate_change_3mo,66), ts_backfill(eps_y1_estimate_ch` |

## 七、判死记录（sealed dead_end）

- `EUR-ANALYST-FACTOR-SIGNALS-WEAK`（2026-09-23T18:49:12）family=analyst_factor_signals 分析师因子信号族（EPS/revenue revision magnitude × coeff_var）：{"family": "analyst_factor_signals 分析师因子信号族（EPS/revenue revision magnitude × coeff_var）", "reason": "wave243 9 探针全灭 best /sharpe/=0.31 → 达 fast_kill 判死线。ANALYST 塔候选出局。今日 7 集回测探针全灭（max/S/ 0.16-0.91），与 2026-09-22 零竞争轴证伪结论互证。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-23T18:49:12", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_
- `EUR-COUNTRY-EXCHANGE-SECTOR-GROUPING-DEAD`（2026-10-19）family=analyst_revision：{"contradicts": {"item": "EUR region panel states 'country axis neutralization/grouping is meaningful' because the universe spans multiple countries", "resolution": "That panel statement is a REGION-LEVEL PRIOR, not a family-level measurement. It is falsified for the analyst_revision family. Do not spend slots on country grouping for revision fields without new evidence.", "where": "wq-brain-ra-eu
- `EUR-ANALYST39-FAST-RECIPE-DEAD`（2026-10-19）family=analyst39：{"acceleration_leg": "ts_delta(anl39_ghcspemtt, 60) → S 0.09（全批最差）⇒ 「变动」再取变动在 EUR 是纯噪声。", "batch": "1e3zWtfA64HqcFSOP51tcOH", "best": {"alpha": "9qE7arG1", "failed_ra": 3, "field": "anl39_rygnhcspe", "fitness": 0.73, "sharpe": 1.21, "sub": 0.44, "sub_limit": 0.63, "two_year_sharpe": 1.8}, "coverage": 0.8755, "dataset": "analyst39", "date": "2026-10-19", "decision_table": "D15", "family": "analyst3
- `EUR-BUCKET-AXIS-NOT-A-DECORRELATOR`（2026-10-19）family=analyst_factor_signals：{"ablation_control": "KPmE8klx = signed_power(group_zscore(netprofit_y2_estimate_change_3mo, subindustry), 1.8) @ EUR/TOP2500/d1/decay10/FAST/trunc0.08/maxTrade ON/nanHandling ON. Batch J adds ONLY the outer bucket wrapper at identical settings => pure single-variable ablation.", "cost_table": {"double_bucket_25cell": {"alpha": "zqrROE1K", "d_fitness": -0.37, "d_sharpe": -0.26, "margin": 0.001671,

