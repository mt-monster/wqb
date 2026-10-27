# analyst_consensus — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst_consensus` |
| 名称 | Standardized Analyst Consensus Forecasts |
| 类别 | ANALYST |
| 数据字段数(平台) | 1929 |
| 覆盖率 | 0.7027 |
| 平台已有 alpha | 95 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides standardized, cleaned, and event-aligned analyst consensus forecasts and actuals for global equities, enabling direct comparison across companies and time. It aggregates and harmonizes consensus data from multiple leading sources, including I/B/E/S, Capital IQ, and FactSet, and applies rigorous data cleaning to remove expired or irrelevant forecasts. The dataset supports flexible configuration for different forecast horizons (quarterly, annual, rolling) and includes both forecast and actual values, as well as surprise calculations. By offering time-series event data with consistent methodology, it allows users to track revisions, analyze forecast accuracy, and construct robust quantitative models. This makes it a valuable resource for predicting price movements, backt

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **1929** |
| 类型分布 | VECTOR×1911　MATRIX×18 |
| 平均覆盖率 | **0.703** |
| 覆盖率区间 | 0.18 ~ 0.95 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 320 | 16.6% |
| 中 (0.70–0.90) | 1156 | 59.9% |
| 低 (0.50–0.70) | 23 | 1.2% |
| 稀疏 (<0.50) | 430 | 22.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 1472 | 76.3% |
| UNUSABLE | 453 | 23.5% |
| DEAD | 4 | 0.2% |

- 已实测字段：**4** 个（0%），best_sharpe 最高 **0.96**，中位 0.22

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 1580 | 0.70 | mean_flash_estimate_pretax_annual12、median_estimate_return_on_capital_annual12、estimate_count_current_period_targetprice_annual12_tribes |
| 盈利与财务 | 180 | 0.71 | actual_ebit_value_annual12、actual_fcf_value_annual12、actual_dividend_value_annual12_2 |
| 其他 | 83 | 0.69 | actual_value_eps_annual12、forecast_actual_indicator_pretax_annual12_2、actual_epsreported_value_annual12 |
| 宏观与行业 | 72 | 0.70 | actual_value_fxadj_eps_annual12、currency_type_eps_annual12、actual_epsreported_value_fxadj_annual12 |
| 持仓与资金流 | 7 | 0.75 | actual_goodwill_value_annual12、forecast_actual_indicator_totalliab_annual12_tribes、actual_cashflowinvesting_value_annual12 |
| 价量与波动 | 5 | 0.80 | actual_return_on_capital_value_annual12、forecast_actual_flag_return_on_capital_annual12、forecast_actual_indicator_return_on_capital_annual12 |
| 风险与质量 | 1 | 0.87 | forecast_actual_flag_capex_annual12_2 |
| 元数据与非信号 | 1 | 0.32 | forecast_actual_indicator_dps_quarterly16 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mean_flash_estimate_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 3 | 0.96 | 0.66 | 0.50 | DEAD | Mean of flash consensus estimates for the PRE metric (vendor snapshot) |
| 2 | `actual_ebit_value_annual12` | VECTOR | 0.932 | 盈利与财务 | 3 | 0.22 | -0.02 | — | DEAD | Reported actual annual EBIT value as released by the company |
| 3 | `actual_fcf_value_annual12` | VECTOR | 0.849 | 盈利与财务 | 1 | 0.02 | 0.46 | — | DEAD | Actual reported annual Free Cash Flow value for the company, point-in-time and regime-aware |
| 4 | `median_estimate_return_on_capital_annual12` | VECTOR | 0.799 | 修正与预期 | 1 | -0.04 | -0.37 | — | DEAD | Median of analyst ROC estimates (consensus median) |
| 5 | `estimate_count_current_period_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst target price estimates used in the consensus |
| 6 | `estimate_currency_code_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency code/identifier associated with the target price estimates |
| 7 | `max_estimate_fxadj_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst target price estimate after currency and split adjustment |
| 8 | `max_estimate_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst target price estimate in the consensus set |
| 9 | `mean_estimate_fxadj_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) target price estimate after currency and split adjustment |
| 10 | `mean_estimate_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus average) of analyst target price estimates |
| 11 | `median_estimate_fxadj_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst target price estimate after currency and split adjustment |
| 12 | `median_estimate_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst target price estimates |
| 13 | `min_estimate_fxadj_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst target price estimate after currency and split adjustment |
| 14 | `min_estimate_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst target price estimate in the consensus set |
| 15 | `stddev_estimate_fxadj_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted standard deviation of target price estimates |
| 16 | `stddev_estimate_targetprice_annual12_tribes` | MATRIX | 0.948 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst target price estimates |
| 17 | `actual_value_eps_annual12` | VECTOR | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Actual reported annual EPS values vector; forecast periods are null/NaN |
| 18 | `actual_value_fxadj_eps_annual12` | VECTOR | 0.936 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/split-adjusted actual reported annual EPS values |
| 19 | `currency_type_eps_annual12` | VECTOR | 0.936 | 宏观与行业 | 0 | — | — | — | UNTESTED | Integer code for the report/measure currency, to be decoded via currency table |
| 20 | `estimate_count_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to form the EPS consensus |
| 21 | `max_estimate_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst EPS estimate |
| 22 | `max_estimate_fxadj_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | FX-adjusted highest individual analyst EPS estimate for the annual period |
| 23 | `mean_estimate_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) EPS estimate |
| 24 | `mean_estimate_fxadj_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean of analyst annual EPS forecasts |
| 25 | `mean_forecast_actual_combined_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate combined with subsequent actuals for annual EPS (forecast + actual overlay) |
| 26 | `mean_forecast_actual_combined_fxadj_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean estimate combined with actuals (FA overlay) for annual EPS |
| 27 | `mean_surprise_value_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus mean EPS estimate (Actual minus mean consensus) |
| 28 | `mean_surprise_value_fxadj_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus mean EPS estimate (Actual minus mean consensus) |
| 29 | `median_estimate_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst EPS estimates |
| 30 | `median_estimate_fxadj_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median of analyst EPS estimates |
| 31 | `median_forecast_actual_combined_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual composite: median consensus for forecast periods combined with reported actuals for actual periods |
| 32 | `median_forecast_actual_fxadj_eps_annual12_tribes` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median estimate combined with actuals (FA overlay) |
| 33 | `median_surprise_value_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus median EPS estimate (Actual minus median consensus) |
| 34 | `median_surprise_value_fxadj_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus median EPS estimate (Actual minus median consensus) |
| 35 | `min_estimate_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst EPS estimate |
| 36 | `min_estimate_fxadj_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | FX-adjusted lowest individual analyst EPS estimate |
| 37 | `stddev_estimate_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst EPS estimates |
| 38 | `stddev_estimate_fxadj_eps_annual12` | VECTOR | 0.936 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/currency-adjusted standard deviation of analyst EPS estimates |
| 39 | `actual_dividend_value_annual12_2` | VECTOR | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual dividends-per-share (DPS) value for the period |
| 40 | `actual_dividend_value_fxadj_annual12_3` | VECTOR | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual annual DPS value adjusted for currency/splits/regime effects |
| 41 | `estimate_count_current_period_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the DPS consensus |
| 42 | `forecast_actual_flag_dividend_annual12_2` | VECTOR | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for dividends per share in the annual period. |
| 43 | `forecast_actual_indicator_dividend_annual12_2` | VECTOR | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for dividends per share in the annual period. |
| 44 | `max_estimate_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual DPS estimate (forecast) |
| 45 | `max_estimate_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst forecast for annual DPS |
| 46 | `mean_estimate_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) analyst estimate for annual DPS |
| 47 | `mean_estimate_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean (consensus) analyst estimate for annual DPS |
| 48 | `mean_forecast_actual_combined_dps_annual12_3` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus for annual DPS combined with actuals (Forecast+Actual overlay) |
| 49 | `mean_forecast_actual_combined_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean consensus for annual DPS combined with actuals (Forecast+Actual overlay) |
| 50 | `mean_surprise_value_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus the mean DPS estimate (Actual minus mean consensus) |
| 51 | `mean_surprise_value_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the mean DPS estimate (Actual minus mean consensus) |
| 52 | `median_estimate_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate for annual DPS |
| 53 | `median_estimate_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median analyst estimate for annual DPS |
| 54 | `median_forecast_actual_combined_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus for annual DPS combined with actuals (Forecast+Actual overlay) |
| 55 | `median_forecast_actual_combined_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median consensus for annual DPS combined with actuals (Forecast+Actual overlay) |
| 56 | `median_surprise_value_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus the median DPS estimate (Actual minus median consensus) |
| 57 | `median_surprise_value_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the median DPS estimate (Actual minus median consensus) |
| 58 | `min_estimate_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst annual DPS estimate (forecast) |
| 59 | `min_estimate_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst forecast for annual DPS |
| 60 | `stddev_estimate_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation (dispersion) of analyst annual DPS estimates |
| 61 | `stddev_estimate_fxadj_dividend_annual12_2` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation (dispersion) of analyst annual DPS estimates |
| 62 | `actual_revenue_value_annual12_tribes` | VECTOR | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual revenue (vendor-reported) |
| 63 | `actual_value_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted actual reported annual revenue |
| 64 | `estimate_count_revenue_annual12` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the annual revenue consensus |
| 65 | `estimate_currency_code_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer code for the reporting currency of the measure (decoded by date) |
| 66 | `forecast_actual_flag_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating status/provenance of FA data (e.g., 0 backfilled, 1 consensus forecast, 2 actual) |
| 67 | `forecast_actual_indicator_revenue_annual12_tribes` | VECTOR | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for revenue. |
| 68 | `max_estimate_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted highest analyst annual revenue estimate (forecast only) |
| 69 | `max_estimate_revenue_annual12` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual revenue estimate (forecast only) |
| 70 | `mean_estimate_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted consensus mean of analyst annual revenue estimates |
| 71 | `mean_estimate_revenue_annual12` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst annual revenue estimates |
| 72 | `mean_forecast_actual_combined_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted mean estimate combined with actuals (forecast+actual) for annual revenue |
| 73 | `mean_forecast_actual_combined_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-actual overlay: mean estimate combined with subsequent actuals for annual revenue |
| 74 | `mean_surprise_value_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the mean analyst consensus for annual revenue (actual minus mean estimate) |
| 75 | `mean_surprise_value_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise based on mean estimate (actual minus mean consensus) for annual revenue |
| 76 | `median_estimate_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median of analyst annual revenue estimates |
| 77 | `median_estimate_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst annual revenue estimates for the specified period/window |
| 78 | `median_forecast_actual_combined_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-actual overlay: median estimate combined with subsequent actuals for annual revenue |
| 79 | `median_forecast_actual_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted median estimate combined with actuals (forecast+actual) for annual revenue |
| 80 | `median_surprise_value_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the median analyst consensus for annual revenue |
| 81 | `median_surprise_value_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus the consensus median annual revenue estimate, computed as Actual minus MedianEst, regime-aware |
| 82 | `min_estimate_fxadj_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted lowest analyst annual revenue estimate (forecast only) |
| 83 | `min_estimate_revenue_annual12` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst annual revenue estimate (forecast only) |
| 84 | `stddev_estimate_fxadj_revenue_annual12` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted standard deviation of analyst annual revenue estimates |
| 85 | `stddev_estimate_revenue_annual12_tribes` | VECTOR | 0.935 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst annual revenue estimates |
| 86 | `actual_ebit_value_fxadj_annual12` | VECTOR | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency/split-adjusted actual reported annual EBIT values |
| 87 | `estimate_count_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the annual EBIT consensus |
| 88 | `forecast_actual_flag_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Provenance/status flag for FA data (0 backfilled, 1 forecast consensus, 2 actual report) |
| 89 | `forecast_actual_indicator_ebit_annual12` | VECTOR | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event indicator identifying forecast versus actual periods (M..1 for forecasts, 0 and negative values for actual/outdate |
| 90 | `max_estimate_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual EBIT estimate (forecast-only) |
| 91 | `max_estimate_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst estimate of annual EBIT |
| 92 | `mean_estimate_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) of analyst annual EBIT estimates (forecast-only) |
| 93 | `mean_estimate_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted mean annual EBIT estimate |
| 94 | `mean_forecast_actual_combined_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst EBIT estimate combined with subsequent actuals (forecast plus actual), regime-aware overlay |
| 95 | `mean_forecast_actual_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean estimate combined with actuals (forecast plus actual) |
| 96 | `mean_surprise_value_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise: deviation between actual EBIT and the mean consensus estimate |
| 97 | `mean_surprise_value_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/FX-adjusted mean estimate surprise |
| 98 | `median_estimate_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst annual EBIT estimates (consensus, forecast-only) under regime-aware processing |
| 99 | `median_estimate_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted median annual EBIT estimate |
| 100 | `median_forecast_actual_combined_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst EBIT estimate combined with subsequent actuals (forecast plus actual), regime-aware overlay |
| 101 | `median_forecast_actual_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median estimate combined with actuals (forecast plus actual) |
| 102 | `median_surprise_value_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise: deviation between actual EBIT and the median consensus estimate |
| 103 | `median_surprise_value_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median estimate surprise (actual minus adjusted median) |
| 104 | `min_estimate_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst annual EBIT estimate (forecast-only) |
| 105 | `min_estimate_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst estimate of annual EBIT |
| 106 | `stddev_estimate_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation (dispersion) of analyst EBIT estimates |
| 107 | `stddev_estimate_fxadj_ebit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst EBIT estimates, adjusted for currency, annual period. |
| 108 | `actual_netprofit_value_annual12` | VECTOR | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual Net Profit values aligned to the event periods (forecast slots empty) |
| 109 | `actual_netprofit_value_fxadj_annual12` | VECTOR | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted actual reported annual net profit values |
| 110 | `estimate_count_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the annual Net Profit consensus for the period |
| 111 | `forecast_actual_flag_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Provenance/quality flag for Forecast+Actual (FA) data: 0 backfilled, 1 forecast consensus, 2 actual report |
| 112 | `forecast_actual_indicator_netprofit_annual12` | VECTOR | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of forecast vs actual periods for each point (positive codes for forecasts; 0/-1/-2 for actuals/outdated forec |
| 113 | `max_estimate_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst estimate for annual Net Profit |
| 114 | `max_estimate_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual Net Profit |
| 115 | `mean_estimate_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean consensus estimate for annual Net Profit |
| 116 | `mean_estimate_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) of analysts’ annual Net Profit estimates for the period |
| 117 | `mean_forecast_actual_combined_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean consensus estimate for annual net profit, combined with actuals under the FA overlay |
| 118 | `mean_forecast_actual_combined_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus estimate for annual net profit combined with actuals under the FA overlay |
| 119 | `mean_surprise_value_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise: actual minus mean estimate for annual net profit |
| 120 | `mean_surprise_value_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise: actual minus mean estimate for annual net profit (unadjusted) |
| 121 | `median_estimate_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median consensus estimate for annual Net Profit |
| 122 | `median_estimate_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus estimate for annual Net Profit |
| 123 | `median_forecast_actual_combined_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median consensus estimate for annual net profit, combined with actuals under the FA overlay |
| 124 | `median_forecast_actual_combined_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast+Actual composite median consensus estimate for annual Net Profit |
| 125 | `median_surprise_value_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise: actual minus median estimate for annual net profit |
| 126 | `median_surprise_value_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise: actual minus median estimate for annual net profit (unadjusted) |
| 127 | `min_estimate_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst estimate for annual Net Profit |
| 128 | `min_estimate_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual Net Profit |
| 129 | `stddev_estimate_fxadj_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted standard deviation of analyst estimates for annual Net Profit |
| 130 | `stddev_estimate_netprofit_annual12` | VECTOR | 0.932 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual Net Profit |
| 131 | `actual_pretax_value_annual12_2` | VECTOR | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual PPROFIT value |
| 132 | `actual_pretax_value_fxadj_annual12_2` | VECTOR | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency-adjusted actual annual pre-tax profit value |
| 133 | `currency_type_parent_profit_annual12` | VECTOR | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Integer currency code for the measure, decoded to the reporting currency by date |
| 134 | `estimate_count_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to form the consensus |
| 135 | `forecast_actual_flag_pretax_annual12_2` | VECTOR | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator flag showing if the value is a forecast or actual for annual pretax profit. |
| 136 | `forecast_actual_indicator_pretax_annual12_2` | VECTOR | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Indicator of forecast versus actual periods within the series (M..1 = forecasts; 0, -1, -2 = actual/outdated) |
| 137 | `max_estimate_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for Parent Profit, adjusted for currency/splits/regime |
| 138 | `max_estimate_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate |
| 139 | `mean_estimate_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean (consensus) analyst estimate |
| 140 | `mean_estimate_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) estimate for annual PPROFIT |
| 141 | `mean_forecast_actual_combined_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast-plus-Actual combined mean consensus for annual pre-tax profit |
| 142 | `mean_forecast_actual_combined_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual combined mean consensus series for annual pre-tax profit (unadjusted) |
| 143 | `mean_surprise_value_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted vendor-reported surprise for annual pre-tax profit equal to actual minus mean estimate |
| 144 | `mean_surprise_value_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise for annual pre-tax profit equal to actual minus mean estimate (unadjusted) |
| 145 | `median_estimate_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted median of analyst estimates for annual pre-tax profit |
| 146 | `median_estimate_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analysts’ annual PPROFIT estimates |
| 147 | `median_forecast_actual_combined_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast-plus-Actual combined median consensus for annual pre-tax profit |
| 148 | `median_forecast_actual_combined_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual combined median consensus series for annual pre-tax profit (unadjusted) |
| 149 | `median_surprise_value_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise for annual pre-tax profit equal to actual minus median estimate, currency-adjusted |
| 150 | `median_surprise_value_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise for annual pre-tax profit equal to actual minus median estimate (unadjusted) |
| 151 | `min_estimate_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for Parent Profit, adjusted for currency/splits/regime |
| 152 | `min_estimate_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate |
| 153 | `stddev_estimate_fxadj_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual pretax profit, adjusted for currency. |
| 154 | `stddev_estimate_pretax_annual12_2` | VECTOR | 0.929 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual pre-tax profit (forecast only) |
| 155 | `actual_epsreported_value_annual12` | VECTOR | 0.922 | 其他 | 0 | — | — | — | UNTESTED | Actual reported EPS value (EPSREP) |
| 156 | `actual_epsreported_value_fxadj_annual12` | VECTOR | 0.922 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted actual reported EPS value |
| 157 | `currency_code_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code referencing decode table for the measure’s reporting/estimate currency |
| 158 | `estimate_count_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to compute the consensus for EPSREP |
| 159 | `forecast_actual_flag_epsreported_annual12` | VECTOR | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast, actual, or combined for reported earnings per share in the annual perio |
| 160 | `forecast_actual_indicator_epsreported_annual12` | VECTOR | 0.922 | 其他 | 0 | — | — | — | UNTESTED | Forecast/Actual period indicator per event: M..1 denote forecast periods; 0, -1, -2 denote actual or outdated forecasts |
| 161 | `max_estimate_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate (forecast only) for annual reported EPS (EPSREP) |
| 162 | `max_estimate_fxadj_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/currency-adjusted highest analyst estimate for EPSREP |
| 163 | `mean_estimate_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean analyst estimate for EPSREP |
| 164 | `mean_estimate_fxadj_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted consensus mean analyst estimate for EPSREP |
| 165 | `mean_forecast_actual_combined_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-actual regime-aware mean for EPSREP (consensus mean blended with actuals when available) |
| 166 | `mean_forecast_actual_combined_fxadj_epsreported_annual12` | VECTOR | 0.922 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted forecast-plus-actual mean for EPSREP |
| 167 | `mean_surprise_value_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus mean consensus (Actual minus mean estimate) for EPSREP |
| 168 | `mean_surprise_value_fxadj_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the consensus mean (Actual minus mean estimate) for EPSREP |
| 169 | `median_estimate_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for EPSREP |
| 170 | `median_estimate_fxadj_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median analyst estimate for EPSREP |
| 171 | `median_forecast_actual_combined_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-actual median estimate for EPSREP |
| 172 | `median_forecast_actual_combined_fxadj_epsreported_annual12` | VECTOR | 0.922 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted forecast-plus-actual median for EPSREP |
| 173 | `median_surprise_value_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus median consensus (Actual minus median estimate) for EPSREP |
| 174 | `median_surprise_value_fxadj_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus median consensus for EPSREP |
| 175 | `min_estimate_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate (forecast only) for EPSREP |
| 176 | `min_estimate_fxadj_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/currency-adjusted lowest analyst estimate for annual reported EPS (EPSREP) |
| 177 | `stddev_estimate_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst EPSREP estimates (unadjusted) |
| 178 | `stddev_estimate_fxadj_epsreported_annual12` | VECTOR | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for reported earnings per share, adjusted for currency, for the annual period. |
| 179 | `actual_nav_value_annual12_tribes` | VECTOR | 0.918 | 其他 | 0 | — | — | — | UNTESTED | Actual reported NAV value |
| 180 | `actual_value_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reported actual values adjusted for currency, splits, and regime effects |
| 181 | `currency_code_nav_annual12_tribes` | VECTOR | 0.918 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency code in which the net asset value is reported for the annual period. |
| 182 | `estimate_count_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the consensus |
| 183 | `forecast_actual_flag_nav_annual12_tribes` | VECTOR | 0.918 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing if the value is a forecast or an actual for net asset value. |
| 184 | `forecast_actual_indicator_nav_annual12_tribes` | VECTOR | 0.918 | 其他 | 0 | — | — | — | UNTESTED | Event/period indicator: M..1 denote forecast periods, 0, -1, -2... denote actual/reporting periods, locating each NAV va |
| 185 | `max_estimate_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst NAV estimate after currency/split adjustment |
| 186 | `max_estimate_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for NAV |
| 187 | `mean_estimate_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean NAV consensus |
| 188 | `mean_estimate_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus average) of analyst estimates for NAV |
| 189 | `mean_forecast_actual_combined_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast+Actual combined mean value for NAV |
| 190 | `mean_forecast_actual_combined_nav_annual12_tribes` | VECTOR | 0.918 | 其他 | 0 | — | — | — | UNTESTED | Forecast+Actual combined mean value (regime-aware) for NAV |
| 191 | `mean_surprise_value_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise: Actual NAV minus consensus mean NAV estimate at the time of reporting |
| 192 | `mean_surprise_value_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise of the mean estimate versus the actual (actual minus mean consensus) |
| 193 | `median_estimate_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median NAV consensus |
| 194 | `median_estimate_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Median (consensus) of analyst estimates for NAV |
| 195 | `median_forecast_actual_combined_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast+Actual combined median value for NAV |
| 196 | `median_forecast_actual_combined_nav_annual12_tribes` | VECTOR | 0.918 | 其他 | 0 | — | — | — | UNTESTED | Forecast+Actual combined median value (regime-aware) for NAV |
| 197 | `median_surprise_value_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise: Actual NAV minus consensus median NAV estimate |
| 198 | `median_surprise_value_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise of the median estimate versus the actual (actual minus median consensus) |
| 199 | `min_estimate_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted lowest analyst NAV estimate |
| 200 | `min_estimate_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for NAV |
| 201 | `stddev_estimate_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for NAV |
| 202 | `stddev_fxadj_nav_annual12_tribes` | VECTOR | 0.918 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation of analyst NAV estimates |
| 203 | `actual_netprofitreported_value_annual12` | VECTOR | 0.916 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual Net Profit (NPROFITREP) values aligned to events; forecast periods are blank or NaN |
| 204 | `actual_netprofitreported_value_fxadj_annual12` | VECTOR | 0.916 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency- and split-adjusted actual reported annual Net Profit values |
| 205 | `estimate_count_current_period_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the consensus for each period |
| 206 | `forecast_actual_flag_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag for Forecast-plus-Actual provenance/status (e.g., 0 backfilled, 1 consensus forecast, 2 actual report) |
| 207 | `forecast_actual_indicator_netprofitreported_annual12` | VECTOR | 0.916 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for reported net profit in the annual period. |
| 208 | `max_estimate_fxadj_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted highest individual analyst estimate for annual Net Profit (Reported) |
| 209 | `max_estimate_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate in the consensus for annual Net Profit Reported |
| 210 | `mean_estimate_fxadj_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted consensus mean estimate for annual Net Profit (Reported) |
| 211 | `mean_estimate_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst estimates for Net Profit Reported |
| 212 | `mean_forecast_actual_combined_fxadj_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean consensus estimate combined with actuals (FA overlay) for the measure |
| 213 | `mean_forecast_actual_combined_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus estimate combined with subsequent actuals (FA overlay), regime-aware |
| 214 | `mean_surprise_value_fxadj_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise for the mean estimate (actual minus mean consensus, expressed in default currency) |
| 215 | `mean_surprise_value_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for annual Net Profit (Reported) computed as Actual minus mean estimate, regime-aware |
| 216 | `median_estimate_fxadj_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted median consensus estimate for annual Net Profit (Reported) |
| 217 | `median_estimate_netprofitreported_annual12_2` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for Net Profit Reported |
| 218 | `median_forecast_actual_combined_fxadj_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median estimate combined with actuals (FA overlay) |
| 219 | `median_forecast_actual_combined_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Median estimate combined with subsequent actuals (FA overlay), regime-aware |
| 220 | `median_surprise_value_fxadj_netprofitreported_annual12_2` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise for the median estimate (actual minus median consensus, expressed in default currency) |
| 221 | `median_surprise_value_netprofitreported_annual12_2` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise overlay for Net Profit Reported: actual minus the median consensus estimate at the time of the |
| 222 | `min_estimate_fxadj_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted lowest individual analyst estimate for annual Net Profit (Reported) |
| 223 | `min_estimate_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for Net Profit Reported in original vendor currency |
| 224 | `stddev_estimate_fxadj_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted standard deviation of estimates |
| 225 | `stddev_estimate_netprofitreported_annual12` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for Net Profit Reported |
| 226 | `actual_taxprovision_value_annual12_tribes` | VECTOR | 0.915 | 其他 | 0 | — | — | — | UNTESTED | Actual reported TAXPROV values |
| 227 | `actual_value_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 宏观与行业 | 0 | — | — | — | UNTESTED | Actual reported Tax Provision figures adjusted for currency/splits |
| 228 | `estimate_count_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the consensus for annual Tax Provision |
| 229 | `estimate_currency_code_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code for the tax provision measure, decoded by date to the report currency |
| 230 | `forecast_actual_flag_taxprovision_annual12_tribes` | VECTOR | 0.915 | 其他 | 0 | — | — | — | UNTESTED | Indicator showing if the value is a forecast or an actual for tax provision. |
| 231 | `forecast_actual_indicator_taxprovision_annual12_tribes` | VECTOR | 0.915 | 其他 | 0 | — | — | — | UNTESTED | Indicator vector for period type: M...1 = forecast periods; 0, -1, -2... = actual/outdated forecasts |
| 232 | `max_estimate_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for Tax Provision adjusted for currency/splits |
| 233 | `max_estimate_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for Tax Provision for the period (unadjusted) |
| 234 | `mean_estimate_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and regime adjusted consensus mean estimate for annual Tax Provision |
| 235 | `mean_estimate_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean analyst estimate for annual Tax Provision |
| 236 | `mean_forecast_actual_combined_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency adjusted forecast-plus-actual mean for annual Tax Provision |
| 237 | `mean_forecast_actual_combined_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast plus actual overlay: consensus mean estimate combined with subsequent actuals for annual Tax Provision |
| 238 | `mean_surprise_value_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean estimate surprise for TAXPROV |
| 239 | `mean_surprise_value_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for TAXPROV computed as Actual minus mean consensus estimate |
| 240 | `median_estimate_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median analyst estimate for Tax Provision adjusted for currency/splits |
| 241 | `median_estimate_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Median (consensus) analyst estimate for TAXPROV |
| 242 | `median_forecast_actual_combined_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency adjusted median estimate combined with actuals under the FA overlay for annual tax provision |
| 243 | `median_forecast_actual_combined_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast plus actual overlay: consensus median estimate combined with subsequent actuals for annual Tax Provision |
| 244 | `median_surprise_value_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and regime adjusted surprise versus median estimate for annual Tax Provision |
| 245 | `median_surprise_value_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise overlay for Tax Provision: vendor-reported Actual minus consensus median estimate (unadjusted) |
| 246 | `min_estimate_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for Tax Provision adjusted for currency/splits |
| 247 | `min_estimate_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for annual Tax Provision |
| 248 | `stddev_estimate_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for the TAXPROV metric |
| 249 | `stddev_fxadj_taxprovision_annual12_tribes` | VECTOR | 0.915 | 修正与预期 | 0 | — | — | — | UNTESTED | FX and regime adjusted standard deviation of analyst estimates for annual Tax Provision |
| 250 | `actual_roe_value_annual12_tribes_2` | VECTOR | 0.910 | 其他 | 0 | — | — | — | UNTESTED | Company-reported actual annual ROE value as captured point-in-time under the dataset’s regime rules |
| 251 | `estimate_count_current_period_roe_annual12_tribes` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst ROE estimates used to compute the consensus |
| 252 | `forecast_actual_flag_roe_annual12_2` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Status flag for the forecast-plus-actual series (e.g., 0 backfilled, 1 consensus forecast, 2 actual report) |
| 253 | `forecast_actual_indicator_roe_annual12_2` | VECTOR | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | A code or flag indicating whether the value is a forecast or an actual for return on equity in the annual period. |
| 254 | `max_estimate_roe_annual12_tribes_2` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for annual ROE |
| 255 | `mean_estimate_roe_annual12_tribes_2` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) of analyst ROE estimates (forecast-only) |
| 256 | `mean_forecast_actual_combined_roe_annual12_tribes` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst consensus estimate for annual ROE combined with subsequent actuals (Forecast + Actual), regime-aware |
| 257 | `mean_surprise_value_roe_annual12_tribes_2` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus mean: actual annual ROE minus the mean ROE estimate (regime-aware) |
| 258 | `median_estimate_roe_annual12_tribes_2` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median analyst forecast for annual ROE |
| 259 | `median_forecast_actual_combined_roe_annual12_tribes` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst consensus estimate for annual ROE combined with subsequent actuals (Forecast + Actual), regime-aware |
| 260 | `median_surprise_value_roe_annual12_tribes_2` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus median: actual annual ROE minus the median ROE estimate |
| 261 | `min_estimate_roe_annual12_tribes_2` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for annual ROE |
| 262 | `stddev_estimate_roe_annual12_tribes_2` | VECTOR | 0.910 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst ROE estimates within the consensus |
| 263 | `actual_tangbookvalue_value_annual12_tribes` | VECTOR | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported values for the SEQUITY measure (vector; forecast positions are NaN) |
| 264 | `actual_tangbookvalue_value_fxadj_annual12_tribes` | VECTOR | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency-adjusted actual reported value(s) for the SEquity measure |
| 265 | `estimate_count_current_period_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to compute the consensus for the SEQUITY measure |
| 266 | `estimate_currency_code_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code for the reporting currency, decoded by report date |
| 267 | `forecast_actual_flag_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 其他 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for tangible book value per share. |
| 268 | `forecast_actual_indicator_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for tangible book value per share. |
| 269 | `max_estimate_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted highest analyst estimate for the SEQUITY measure |
| 270 | `max_estimate_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for the SEQUITY measure for the period |
| 271 | `mean_estimate_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean (consensus) analyst estimate for the SEquity measure |
| 272 | `mean_estimate_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst estimates (consensus) for the SEQUITY measure |
| 273 | `mean_forecast_actual_combined_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean consensus estimate combined with subsequent actuals (FA overlay) for the SEquity measure |
| 274 | `mean_forecast_actual_combined_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus estimate combined with subsequent actuals (FA overlay) for the SEquity measure |
| 275 | `mean_surprise_value_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the mean estimate (Actual minus mean consensus) for the SEquity measure |
| 276 | `mean_surprise_value_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise overlay: Actual minus mean consensus estimate for the SEQUITY measure |
| 277 | `median_estimate_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median (consensus) analyst estimate for the SEquity measure |
| 278 | `median_estimate_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates (consensus) for the SEQUITY measure |
| 279 | `median_forecast_actual_combined_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median consensus estimate combined with subsequent actuals (FA overlay) for the SEquity measure |
| 280 | `median_forecast_actual_combined_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus value in the Forecast+Actual (FA) composite for the SEQUITY measure |
| 281 | `median_surprise_value_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the median estimate (Actual minus median consensus) for the SEquity measure |
| 282 | `median_surprise_value_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise overlay: Actual minus median consensus estimate for the SEQUITY measure |
| 283 | `min_estimate_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted lowest analyst estimate for the SEQUITY measure |
| 284 | `min_estimate_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for the SEQUITY measure for the period |
| 285 | `stddev_estimate_fxadj_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation of analyst estimates for the SEquity measure |
| 286 | `stddev_estimate_tangbookvalue_annual12_tribes` | VECTOR | 0.907 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for the SEQUITY measure |
| 287 | `actual_pretax_reported_value_annual12_tribes` | VECTOR | 0.906 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported pre-tax profit values aligned to event dates (forecast lead periods are NaN) |
| 288 | `actual_value_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reported actual values for the measure adjusted for currency/splits/regime |
| 289 | `estimate_count_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to form the consensus |
| 290 | `estimate_currency_code_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code for the measure/report, decoded per date |
| 291 | `forecast_actual_flag_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag for Forecast-plus-Actual provenance/status: 0 backfilled, 1 consensus forecast, 2 actual |
| 292 | `forecast_actual_indicator_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 其他 | 0 | — | — | — | UNTESTED | Forecast/actual period indicator (M..1 = forecast periods; 0, -1, -2 = actual/reporting periods) |
| 293 | `max_estimate_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst estimate for pre-tax profit |
| 294 | `max_estimate_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate among the contributing forecasts for the measure |
| 295 | `mean_estimate_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus estimate adjusted for currency/splits/regime |
| 296 | `mean_estimate_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (average) analyst consensus estimate for the measure (forecast) |
| 297 | `mean_forecast_actual_combined_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted Forecast+Actual series using mean consensus |
| 298 | `mean_forecast_actual_combined_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast+Actual series using mean consensus (mean forecasts prior to release, actuals afterward) |
| 299 | `mean_surprise_value_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted surprise versus mean estimate (actual minus mean estimate) |
| 300 | `mean_surprise_value_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise for mean consensus: actual minus mean estimate |
| 301 | `median_estimate_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus estimate adjusted for currency/splits/regime |
| 302 | `median_estimate_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates (consensus) for pre-tax profit |
| 303 | `median_forecast_actual_combined_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted Forecast+Actual series using median consensus |
| 304 | `median_forecast_actual_combined_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast+Actual median consensus series for pre-tax profit (unadjusted) |
| 305 | `median_surprise_value_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted surprise versus median estimate (actual minus median estimate) |
| 306 | `median_surprise_value_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus the median estimate for Profit (Reported): actual minus median estimate |
| 307 | `min_estimate_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate adjusted for currency/splits/regime |
| 308 | `min_estimate_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for pre-tax profit (forecast only) |
| 309 | `stddev_estimate_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for pre-tax profit |
| 310 | `stddev_fxadj_pretax_reported_annual12_tribes` | VECTOR | 0.906 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of estimates adjusted for currency/splits/regime |
| 311 | `actual_sharesoutstanding_value_annual12` | VECTOR | 0.905 | 其他 | 0 | — | — | — | UNTESTED | Actual reported Number of Shares Outstanding for the period (vector aligned to events; forecasts filled with nulls befor |
| 312 | `estimate_count_current_period_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the consensus for shares outstanding |
| 313 | `forecast_actual_flag_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating provenance/status of FA values (0 backfilled, 1 forecast consensus, 2 actual report) |
| 314 | `forecast_actual_indicator_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Event-period indicator: codes M..1 for forecast periods and 0,-1,-2.. for actual/reporting periods, aligning estimates/a |
| 315 | `max_estimate_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for the annual number of shares outstanding for the given period |
| 316 | `mean_estimate_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus average) of analysts’ forecasts for the annual number of shares outstanding |
| 317 | `mean_forecast_actual_combined_sharesoutstanding_annual12` | VECTOR | 0.905 | 其他 | 0 | — | — | — | UNTESTED | Forecast-plus-actual (regime-aware) mean for the annual number of shares outstanding |
| 318 | `mean_surprise_value_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for the annual number of shares outstanding based on mean consensus (Actual minus mean estimate) |
| 319 | `median_estimate_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analysts’ forecasts for the annual number of shares outstanding |
| 320 | `median_forecast_actual_combined_sharesoutstanding_annual12` | VECTOR | 0.905 | 其他 | 0 | — | — | — | UNTESTED | Forecast-plus-actual (regime-aware) median for the annual number of shares outstanding |
| 321 | `median_surprise_value_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for the annual number of shares outstanding based on median consensus (Actual minus median estimate) |
| 322 | `min_estimate_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for the annual number of shares outstanding for the given period |
| 323 | `stddev_estimate_sharesoutstanding_annual12` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analysts’ estimates for the annual number of shares outstanding |
| 324 | `actual_value_ebitda_annual12` | VECTOR | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported actual EBITDA value for the corresponding fiscal period |
| 325 | `actual_value_fxadj_ebitda_annual12` | VECTOR | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted actual EBITDA value |
| 326 | `estimate_count_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to compute the EBITDA consensus |
| 327 | `forecast_actual_flag_ebitda_annual12` | VECTOR | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for annual EBITDA. |
| 328 | `forecast_actual_indicator_ebitda_annual12` | VECTOR | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event indicator marking forecast vs actual periods (positive values for forecasts, 0/negative for actual/outdated) |
| 329 | `max_estimate_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst EBITDA estimate (forecast only) |
| 330 | `max_estimate_fxadj_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst EBITDA estimate |
| 331 | `mean_estimate_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (average) of analyst EBITDA estimates (consensus) |
| 332 | `mean_estimate_fxadj_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean analyst estimate for annual EBITDA |
| 333 | `mean_forecast_actual_combined_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-actual composite mean consensus estimate for annual EBITDA across the p12 window |
| 334 | `mean_forecast_actual_fxadj_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted forecast-plus-actual composite mean consensus estimate for annual EBITDA across the p12 window |
| 335 | `mean_surprise_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus the mean consensus EBITDA estimate (Actual minus mean estimate), regime-aware |
| 336 | `mean_surprise_fxadj_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise relative to the mean EBITDA estimate |
| 337 | `median_estimate_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst EBITDA estimates for the specified annual period |
| 338 | `median_estimate_fxadj_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median EBITDA estimate |
| 339 | `median_forecast_actual_combined_ebitda_annual12` | VECTOR | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median forecast-plus-actual value for annual EBITDA (FA overlay) |
| 340 | `median_forecast_actual_fxadj_ebitda_annual12` | VECTOR | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency-adjusted median forecast-plus-actual value for annual EBITDA |
| 341 | `median_surprise_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus the median consensus EBITDA estimate, typically calculated as Actual minus median estimate, regime-aware |
| 342 | `median_surprise_fxadj_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise relative to the median EBITDA estimate |
| 343 | `min_estimate_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst EBITDA estimate (forecast only) |
| 344 | `min_estimate_fxadj_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst EBITDA estimate |
| 345 | `stddev_estimate_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst EBITDA estimates |
| 346 | `stddev_estimate_fxadj_ebitda_annual12` | VECTOR | 0.899 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation of analyst EBITDA estimates |
| 347 | `actual_value_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 宏观与行业 | 0 | — | — | — | UNTESTED | Reported actual annual Interest Expense adjusted for currency/splits |
| 348 | `actual_value_interest_expense_annual12` | VECTOR | 0.891 | 其他 | 0 | — | — | — | UNTESTED | Reported actual annual Interest Expense |
| 349 | `currency_type_interest_expense_annual12` | VECTOR | 0.891 | 宏观与行业 | 0 | — | — | — | UNTESTED | Integer currency code for the measure, decoded to reporting currency by date |
| 350 | `estimate_count_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to compute the consensus for annual Interest Expense |
| 351 | `max_estimate_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for annual Interest Expense adjusted for currency/splits/regime effects |
| 352 | `max_estimate_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual Interest Expense (forecast only) |
| 353 | `mean_estimate_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean forecast for annual Interest Expense adjusted for currency/splits/regime effects |
| 354 | `mean_estimate_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) analyst estimate for annual Interest Expense |
| 355 | `mean_forecast_actual_combined_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast+Actual mean for annual Interest Expense (vendor FA overlay) |
| 356 | `mean_forecast_actual_combined_interest_expense_annual12` | VECTOR | 0.891 | 其他 | 0 | — | — | — | UNTESTED | Regime-aware Forecast+Actual overlay combining the mean forecast and the subsequent actual for annual Interest Expense |
| 357 | `mean_surprise_value_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/splits/regime-adjusted mean estimate surprise for annual Interest Expense |
| 358 | `mean_surprise_value_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the actual reported annual Interest Expense and the consensus mean estimate (surprise) |
| 359 | `median_estimate_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median forecast for annual Interest Expense adjusted for currency/splits/regime effects |
| 360 | `median_estimate_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus analyst estimate for annual Interest Expense |
| 361 | `median_forecast_actual_combined_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 宏观与行业 | 0 | — | — | — | UNTESTED | Forecast+Actual overlay for annual Interest Expense, adjusted for currency/splits/regime effects on the median |
| 362 | `median_forecast_actual_combined_interest_expense_annual12` | VECTOR | 0.891 | 其他 | 0 | — | — | — | UNTESTED | Forecast+Actual median for annual Interest Expense (vendor FA overlay), unadjusted |
| 363 | `median_surprise_value_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/splits/regime-adjusted median estimate surprise for annual Interest Expense |
| 364 | `median_surprise_value_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between the actual reported annual Interest Expense and the consensus median estimate (surprise) |
| 365 | `min_estimate_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for annual Interest Expense adjusted for currency/splits/regime effects |
| 366 | `min_estimate_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual Interest Expense (forecast only) |
| 367 | `stddev_estimate_fxadj_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for annual Interest Expense adjusted for currency/splits/regime effects |
| 368 | `stddev_estimate_interest_expense_annual12` | VECTOR | 0.891 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual Interest Expense, unadjusted |
| 369 | `actual_bvps_value_annual12_tribes` | VECTOR | 0.889 | 其他 | 0 | — | — | — | UNTESTED | Reported actual BVPS values for the periods (forecast periods may be empty) |
| 370 | `actual_bvps_value_fxadj_annual12_2` | VECTOR | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime and currency-adjusted actual reported BVPS value |
| 371 | `estimate_count_current_period_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst BVPS estimates used in the consensus |
| 372 | `estimate_currency_code_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code for the reporting or estimate units |
| 373 | `forecast_actual_flag_bvps_annual12_tribes` | VECTOR | 0.889 | 其他 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for book value per share. |
| 374 | `forecast_actual_indicator_bvps_annual12_tribes` | VECTOR | 0.889 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for book value per share. |
| 375 | `max_estimate_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst BVPS estimate in the current consensus period (forecast only) |
| 376 | `max_estimate_fxadj_bvps_annual12_2` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | FX and regime-adjusted highest analyst BVPS forecast within the window |
| 377 | `mean_estimate_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) analyst BVPS estimate for the fiscal period |
| 378 | `mean_estimate_fxadj_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean analyst BVPS estimate |
| 379 | `mean_forecast_actual_combined_bvps_annual12_tribes` | VECTOR | 0.889 | 其他 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual overlay of the mean BVPS value (uses forecast until actual arrives, then actual) |
| 380 | `mean_forecast_actual_combined_fxadj_bvps_annual12_tribes` | VECTOR | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast-plus-Actual mean BVPS value |
| 381 | `mean_surprise_value_bvps_annual12_tribes_2` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise based on mean BVPS estimate, typically actual minus mean estimate |
| 382 | `mean_surprise_value_fxadj_bvps_annual12_tribes_2` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise for mean BVPS estimate, typically actual minus mean estimate |
| 383 | `median_estimate_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Median (consensus) analyst BVPS estimate for the fiscal period |
| 384 | `median_estimate_fxadj_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median (consensus) analyst BVPS estimate |
| 385 | `median_forecast_actual_combined_bvps_annual12_2` | VECTOR | 0.889 | 其他 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual overlay of the median BVPS value |
| 386 | `median_forecast_actual_combined_fxadj_bvps_annual12_tribes` | VECTOR | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast-plus-Actual median BVPS value |
| 387 | `median_surprise_value_bvps_annual12_2` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise: Actual BVPS minus median consensus BVPS at time of report |
| 388 | `median_surprise_value_fxadj_bvps_annual12_tribes` | VECTOR | 0.889 | 宏观与行业 | 0 | — | — | — | UNTESTED | Median of the differences between actual and currency-adjusted forecasts for book value per share for the annual period. |
| 389 | `min_estimate_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst BVPS estimate (forecast) |
| 390 | `min_estimate_fxadj_bvps_annual12_tribes` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | FX and regime-adjusted lowest analyst BVPS estimate |
| 391 | `stddev_estimate_bvps_annual12_2` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst BVPS estimates (forecast only) |
| 392 | `stddev_fxadj_bvps_annual12_2` | VECTOR | 0.889 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation of BVPS analyst estimates |
| 393 | `actual_total_assets_value_annual12` | VECTOR | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported actual values vector (NaN in forecast periods) |
| 394 | `actual_total_assets_value_fxadj_annual12` | VECTOR | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted actual reported value for the measure |
| 395 | `estimate_count_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the consensus |
| 396 | `estimate_currency_code_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency code in which annual total assets are reported. |
| 397 | `forecast_actual_flag_total_assets_annual12` | VECTOR | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for annual total assets. |
| 398 | `forecast_actual_indicator_total_assets_annual12` | VECTOR | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event-type indicator: positive/M..1 for forecast periods, 0/-1/-2 for actual or outdated forecast periods |
| 399 | `max_estimate_fxadj_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate after currency/split adjustment |
| 400 | `max_estimate_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate among contributing forecasts for the measure |
| 401 | `mean_estimate_fxadj_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted mean consensus estimate for the TA metric (currency/split/regime adjusted) |
| 402 | `mean_estimate_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean average of analyst estimates consensus for the measure |
| 403 | `mean_forecast_actual_combined_fxadj_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime- and currency-adjusted Forecast-plus-Actual (FA) overlay for the mean estimate of Total Assets |
| 404 | `mean_forecast_actual_combined_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate combined with actuals (forecast + actual) for the measure |
| 405 | `mean_surprise_value_fxadj_total_assets_annual12_2` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted surprise for Total Assets using mean consensus (Actual minus MeanEst) |
| 406 | `mean_surprise_value_total_assets_annual12` | VECTOR | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Mean of the surprise values (actual minus forecast) for annual total assets. |
| 407 | `median_estimate_fxadj_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime- and currency-adjusted median analyst estimate for Total Assets |
| 408 | `median_estimate_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for the TA metric |
| 409 | `median_forecast_actual_combined_fxadj_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime- and currency-adjusted Forecast-plus-Actual (FA) overlay for the median estimate of Total Assets |
| 410 | `median_forecast_actual_combined_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus combining forecasts and actuals for the TA metric (FA overlay) |
| 411 | `median_surprise_value_fxadj_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted vendor surprise overlay: the difference between the reported actual and the median consensus estimate, |
| 412 | `median_surprise_value_total_assets_annual12` | VECTOR | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of the surprise values (actual minus forecast) for annual total assets. |
| 413 | `min_estimate_fxadj_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate after currency/split adjustment |
| 414 | `min_estimate_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate among contributing forecasts for the measure |
| 415 | `stddev_estimate_fxadj_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of currency-adjusted analyst estimates for annual total assets. |
| 416 | `stddev_estimate_total_assets_annual12` | VECTOR | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for the measure |
| 417 | `actual_dividend_value_annual12_tribes` | VECTOR | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported total dividend value |
| 418 | `actual_dividend_value_fxadj_annual12_tribes` | VECTOR | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Regime-adjusted actual total dividend value (currency/splits adjustments) |
| 419 | `estimate_count_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to compute the total dividend consensus |
| 420 | `estimate_currency_code_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code for the measure units, decoded by date |
| 421 | `forecast_actual_flag_dividend_annual12_tribes` | VECTOR | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast, actual, or combined for annual total dividends. |
| 422 | `forecast_actual_indicator_dividend_annual12_tribes` | VECTOR | 0.878 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event indicator identifying forecast vs actual periods (M..1 for forecast periods; 0, -1, -2 for actual/outdated) |
| 423 | `max_estimate_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for total dividend |
| 424 | `max_estimate_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted highest analyst estimate for total dividend |
| 425 | `mean_estimate_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) analyst estimate for total dividend |
| 426 | `mean_estimate_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted consensus mean (average) estimate for annual total dividends per share |
| 427 | `mean_forecast_actual_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Average of analyst forecasts and actuals for annual total dividends. |
| 428 | `mean_forecast_actual_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Average of analyst forecasts and actuals for annual total dividends, adjusted for currency. |
| 429 | `mean_surprise_value_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for total dividend (actual minus consensus mean estimate), regime-aware |
| 430 | `mean_surprise_value_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/currency-adjusted surprise for TOTDIV based on mean estimate (Actual minus MeanEst) |
| 431 | `median_estimate_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for total dividend |
| 432 | `median_estimate_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median analyst estimate for total dividend |
| 433 | `median_forecast_actual_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecasts and actuals for annual total dividends. |
| 434 | `median_forecast_actual_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecasts and actuals for annual total dividends, adjusted for currency. |
| 435 | `median_surprise_value_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Median surprise between actual and consensus annual total dividends. |
| 436 | `median_surprise_value_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/currency-adjusted surprise for TOTDIV based on median estimate (Actual minus MedianEst) |
| 437 | `min_estimate_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for total dividend |
| 438 | `min_estimate_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted lowest analyst estimate for total dividend |
| 439 | `stddev_estimate_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for total dividend |
| 440 | `stddev_estimate_fxadj_dividend_annual12_tribes` | VECTOR | 0.878 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/currency-adjusted standard deviation of analyst estimates for annual total dividend (TOTDIV) |
| 441 | `actual_taxrate_value_annual12` | VECTOR | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Actual reported TAXRATE value |
| 442 | `actual_taxrate_value_fxadj_annual12` | VECTOR | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Actual reported effective tax rate for the annual period, adjusted for currency. |
| 443 | `estimate_count_current_period_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to TAXRATE consensus |
| 444 | `forecast_actual_flag_taxrate_annual12` | VECTOR | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for effective tax rate in the annual period. |
| 445 | `forecast_actual_indicator_taxrate_annual12` | VECTOR | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for effective tax rate in the annual period. |
| 446 | `max_estimate_fxadj_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for effective tax rate in the annual period, adjusted for currency. |
| 447 | `max_estimate_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for TAXRATE |
| 448 | `mean_estimate_fxadj_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime adjusted mean estimate for TAXRATE |
| 449 | `mean_estimate_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) analyst estimate for TAXRATE |
| 450 | `mean_forecast_actual_combined_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-aware overlay combining the mean analyst estimate for TAXRATE with subsequent actuals (Forecast plus Actual) |
| 451 | `mean_forecast_actual_fxadj_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime/currency-adjusted mean estimate combined with actuals for TAXRATE |
| 452 | `mean_surprise_value_fxadj_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Average difference between actual and consensus effective tax rate, adjusted for currency, for the annual period. |
| 453 | `mean_surprise_value_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Average difference between actual and consensus effective tax rate for the annual period. |
| 454 | `median_estimate_fxadj_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime/currency-adjusted median of analyst TAXRATE estimates |
| 455 | `median_estimate_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate for TAXRATE |
| 456 | `median_forecast_actual_combined_fxadj_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime/currency-adjusted median estimate combined with actuals for TAXRATE |
| 457 | `median_forecast_actual_combined_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-aware overlay combining the median analyst estimate for TAXRATE with subsequent actuals (Forecast plus Actual) |
| 458 | `median_surprise_value_fxadj_taxrate_annual12` | VECTOR | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Median difference between actual and forecasted effective tax rate, adjusted for currency, for the annual period. |
| 459 | `median_surprise_value_taxrate_annual12` | VECTOR | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | Median difference between actual and forecasted effective tax rate for the annual period. |
| 460 | `min_estimate_fxadj_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for effective tax rate in the annual period, adjusted for currency. |
| 461 | `min_estimate_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for TAXRATE |
| 462 | `stddev_estimate_fxadj_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for effective tax rate in the annual period, adjusted for currency. |
| 463 | `stddev_estimate_taxrate_annual12` | VECTOR | 0.875 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for the annual TAXRATE consensus within the p12 window |
| 464 | `actual_capex_value_annual12_3` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Actual reported CAPEX value (as reported, unadjusted) |
| 465 | `actual_capex_value_fxadj_annual12_3` | VECTOR | 0.871 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted actual reported CAPEX value |
| 466 | `estimate_count_current_period_capex_annual12` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst CAPEX forecasts contributing to the consensus in the current window |
| 467 | `forecast_actual_flag_capex_annual12_2` | VECTOR | 0.871 | 风险与质量 | 0 | — | — | — | UNTESTED | Forecast-plus-actual provenance/quality flag (e.g., 0 backfilled, 1 forecast, 2 actual) |
| 468 | `forecast_actual_indicator_capex_annual12_2` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Event indicator marking forecast vs actual periods (M..1 forecast, 0,-1,-2 actual/outdated) for CAPEX |
| 469 | `max_estimate_capex_annual12` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest raw analyst CAPEX forecast (forecast-only, unadjusted) |
| 470 | `max_estimate_fxadj_capex_annual12` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest CAPEX forecast after currency/split/regime adjustment |
| 471 | `mean_estimate_capex_annual12_2` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean CAPEX estimate |
| 472 | `mean_estimate_fxadj_capex_annual12_3` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted consensus mean CAPEX estimate |
| 473 | `mean_forecast_actual_combined_capex_annual12_3` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Regime-aware overlay combining mean CAPEX forecast with subsequent actuals |
| 474 | `mean_forecast_actual_fxadj_capex_annual12_3` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted FA overlay: mean CAPEX estimate combined with actuals |
| 475 | `mean_surprise_value_capex_annual12_2` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise value: actual CAPEX minus consensus mean CAPEX estimate |
| 476 | `mean_surprise_value_fxadj_capex_annual12_3` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean CAPEX surprise (actual minus mean estimate) |
| 477 | `median_estimate_capex_annual12_2` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median CAPEX estimate |
| 478 | `median_estimate_fxadj_capex_annual12_3` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted consensus median CAPEX estimate |
| 479 | `median_forecast_actual_combined_capex_annual12_2` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | FA overlay: median CAPEX estimate combined with actuals |
| 480 | `median_forecast_actual_combined_fxadj_capex_annual12_2` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted FA overlay: median CAPEX estimate combined with actuals |
| 481 | `median_surprise_value_capex_annual12_3` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Median CAPEX surprise (actual minus median estimate), unadjusted |
| 482 | `median_surprise_value_fxadj_capex_annual12_2` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median CAPEX surprise (actual minus median estimate) |
| 483 | `min_estimate_capex_annual12_3` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest raw analyst CAPEX forecast (forecast-only, unadjusted) |
| 484 | `min_estimate_fxadj_capex_annual12` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest CAPEX forecast after currency/split/regime adjustment |
| 485 | `stddev_estimate_capex_annual12_2` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst CAPEX estimates |
| 486 | `stddev_estimate_fxadj_capex_annual12` | VECTOR | 0.871 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of CAPEX estimates after currency/regime adjustments |
| 487 | `actual_cfo_value_annual12` | VECTOR | 0.869 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported actual operating cash flow values; forecast periods are typically NaN |
| 488 | `actual_cfo_value_fxadj_annual12` | VECTOR | 0.869 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported actual operating cash flow values adjusted for currency and splits |
| 489 | `estimate_count_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to compute the consensus for the period |
| 490 | `forecast_actual_flag_cfo_annual12` | VECTOR | 0.869 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator flag showing if the value is a forecast or actual for annual cash flow from operations. |
| 491 | `forecast_actual_indicator_cfo_annual12` | VECTOR | 0.869 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing if the value is a forecast or actual for annual cash flow from operations. |
| 492 | `max_estimate_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual operating cash flow (forecast-only) |
| 493 | `max_estimate_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual operating cash flow, adjusted for currency and splits |
| 494 | `mean_estimate_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst forecasts for annual operating cash flow |
| 495 | `mean_estimate_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted consensus mean analyst estimate for annual operating cash flow |
| 496 | `mean_forecast_actual_combined_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst estimate combined with subsequent actuals for operating cash flow |
| 497 | `mean_forecast_actual_combined_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted forecast-plus-actual consensus mean for annual operating cash flow, regime-aware |
| 498 | `mean_surprise_value_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus the consensus mean estimate for annual operating cash flow (Actual minus mean estimate), regime-aware |
| 499 | `mean_surprise_value_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the consensus mean estimate for annual operating cash flow (Actual minus mean estimate |
| 500 | `median_estimate_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecasts for annual operating cash flow |
| 501 | `median_estimate_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted consensus median analyst estimate for annual operating cash flow |
| 502 | `median_forecast_actual_combined_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate combined with subsequent actuals for operating cash flow |
| 503 | `median_forecast_actual_combined_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted forecast-plus-actual consensus median for annual operating cash flow, regime-aware |
| 504 | `median_surprise_value_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus the consensus median estimate for annual operating cash flow (Actual minus median estimate), regime-awar |
| 505 | `median_surprise_value_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus the consensus median estimate for annual operating cash flow (Actual minus median esti |
| 506 | `min_estimate_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual operating cash flow (forecast-only) |
| 507 | `min_estimate_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for operating cash flow adjusted for currency |
| 508 | `stddev_estimate_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for annual operating cash flow |
| 509 | `stddev_estimate_fxadj_cfo_annual12` | VECTOR | 0.869 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/FX-adjusted standard deviation of analyst estimates for annual operating cash flow |
| 510 | `estimate_count_depreciation_amortization_annual12` | VECTOR | 0.853 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the DEPAMORT consensus |
| 511 | `max_estimate_depreciation_amortization_annual12` | VECTOR | 0.853 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for annual depreciation and amortization (DEPAMORT) within the p12 regime window |
| 512 | `stddev_estimate_depreciation_amortization_annual12` | VECTOR | 0.853 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for DEPAMORT |
| 513 | `stddev_fxadj_depreciation_amortization_annual12` | VECTOR | 0.853 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted standard deviation of analyst estimates for DEPAMORT |
| 514 | `actual_fcf_value_fxadj_annual12` | VECTOR | 0.849 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime-adjusted actual annual FCF value (currency/split adjusted) |
| 515 | `estimate_count_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the consensus for annual FCF |
| 516 | `forecast_actual_flag_fcf_annual12` | VECTOR | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating whether the free cash flow value is a forecast, actual, or combined for the annual period. |
| 517 | `forecast_actual_indicator_fcf_annual12` | VECTOR | 0.849 | 其他 | 0 | — | — | — | UNTESTED | Event/period indicator vector where positive values (M…1) denote forecast periods and 0, -1, -2… denote actual or post-a |
| 518 | `max_estimate_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual FCF |
| 519 | `max_estimate_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | FX-adjusted highest analyst estimate of annual free cash flow (consensus) |
| 520 | `mean_estimate_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) analyst annual FCF estimate |
| 521 | `mean_estimate_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted consensus mean analyst estimate for annual Free Cash Flow (FCF) for each period in the p12 series |
| 522 | `mean_forecast_actual_combined_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus analyst estimate of annual free cash flow combined with subsequent actuals (Forecast + Actual) |
| 523 | `mean_forecast_actual_combined_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean estimate of FCF combined with actuals (Forecast + Actual) |
| 524 | `mean_surprise_value_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise using mean: Actual minus mean annual FCF estimate |
| 525 | `mean_surprise_value_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted surprise: Actual minus mean annual FCF estimate |
| 526 | `median_estimate_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median of analysts’ annual FCF estimates |
| 527 | `median_estimate_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted median annual FCF estimate |
| 528 | `median_forecast_actual_combined_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus analyst estimate of annual free cash flow combined with subsequent actuals |
| 529 | `median_forecast_actual_combined_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median estimate of FCF combined with actuals (Forecast + Actual) |
| 530 | `median_surprise_value_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise using median: Actual minus median annual FCF estimate |
| 531 | `median_surprise_value_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted surprise: Actual minus median annual FCF estimate |
| 532 | `min_estimate_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual FCF |
| 533 | `min_estimate_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | FX-adjusted lowest analyst estimate of annual free cash flow |
| 534 | `stddev_estimate_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst annual FCF estimates in the consensus set |
| 535 | `stddev_fxadj_fcf_annual12` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | FX-adjusted standard deviation of analyst FCF estimates |
| 536 | `actual_netdebt_value_annual12_tribes_2` | VECTOR | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual Net Debt (NDEBT) value |
| 537 | `actual_netdebt_value_fxadj_annual12_2` | VECTOR | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted actual annual Net Debt value (currency/split/regime adjusted) |
| 538 | `estimate_count_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the consensus |
| 539 | `forecast_actual_flag_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag for forecast/actual combined data provenance or status (e.g., 0=backfilled, 1=consensus forecast, 2=actual) |
| 540 | `forecast_actual_flag_netdebt_annual12_tribes_2` | VECTOR | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator marking forecast vs actual periods (e.g., M..1 = forecasts; 0, -1, -2 = actuals/posted periods) |
| 541 | `max_estimate_fxadj_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted highest analyst estimate for annual Net Debt |
| 542 | `max_estimate_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual Net Debt |
| 543 | `mean_estimate_fxadj_netdebt_annual12_tribes_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean (consensus) estimate for annual Net Debt |
| 544 | `mean_estimate_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) analyst estimate for annual Net Debt |
| 545 | `mean_forecast_actual_combined_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate combined with actuals (Forecast+Actual) for annual Net Debt |
| 546 | `mean_forecast_actual_fxadj_netdebt_annual12_tribes_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean estimate combined with actuals (Forecast+Actual) for annual Net Debt |
| 547 | `mean_surprise_value_fxadj_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted surprise for annual Net Debt (Actual minus mean consensus estimate) |
| 548 | `mean_surprise_value_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate surprise for annual Net Debt (actual minus mean consensus) |
| 549 | `median_estimate_fxadj_netdebt_annual12_tribes_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median (consensus) estimate for annual Net Debt |
| 550 | `median_estimate_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate for annual Net Debt |
| 551 | `median_forecast_actual_combined_fxadj_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median estimate combined with actuals (Forecast+Actual) for annual Net Debt |
| 552 | `median_forecast_actual_combined_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Median estimate combined with actuals (Forecast+Actual) for annual Net Debt |
| 553 | `median_surprise_fxadj_netdebt_annual12_tribes_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted surprise for annual Net Debt (Actual minus median consensus estimate) |
| 554 | `median_surprise_netdebt_annual12_tribes_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for annual Net Debt (Actual minus median consensus estimate), unadjusted |
| 555 | `min_estimate_fxadj_netdebt_annual12_tribes_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted lowest analyst estimate for annual Net Debt |
| 556 | `min_estimate_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual Net Debt |
| 557 | `stddev_estimate_fxadj_netdebt_annual12_tribes_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted standard deviation of analyst estimates for annual Net Debt |
| 558 | `stddev_estimate_netdebt_annual12_2` | VECTOR | 0.849 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual Net Debt |
| 559 | `actual_cfps_value_annual12_2` | VECTOR | 0.844 | 其他 | 0 | — | — | — | UNTESTED | Reported actual annual CFPS value |
| 560 | `actual_cfps_value_fxadj_annual12_2` | VECTOR | 0.844 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/split-adjusted actual CFPS values |
| 561 | `estimate_count_current_period_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst CFPS estimates used to compute the consensus for the period |
| 562 | `estimate_currency_code_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code for the CFPS measure/estimates (decode to report currency by date) |
| 563 | `forecast_actual_flag_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating Forecast+Actual data status/provenance (0 backfilled, 1 forecast consensus, 2 actual) |
| 564 | `forecast_actual_indicator_cfps_annual12_2` | VECTOR | 0.844 | 其他 | 0 | — | — | — | UNTESTED | Forecast/Actual period indicator for each data point (M..1 = forecasts; 0, -1, -2 = actuals/past) |
| 565 | `max_estimate_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst CFPS estimate for the period (forecast) |
| 566 | `max_estimate_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/currency-adjusted highest analyst annual CFPS forecast |
| 567 | `mean_estimate_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean CFPS estimate for the period |
| 568 | `mean_estimate_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted consensus mean CFPS estimate |
| 569 | `mean_forecast_actual_combined_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-aware composite of the consensus mean CFPS estimate combined with actuals (Forecast+Actual overlay) |
| 570 | `mean_forecast_actual_combined_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted forecast-plus-actual mean CFPS value |
| 571 | `mean_surprise_value_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-provided surprise: actual CFPS minus mean consensus estimate at time of reporting |
| 572 | `mean_surprise_value_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus mean CFPS estimate |
| 573 | `median_estimate_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median CFPS estimate for the period |
| 574 | `median_estimate_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median consensus CFPS estimate |
| 575 | `median_forecast_actual_combined_cfps_annual12_2` | VECTOR | 0.844 | 其他 | 0 | — | — | — | UNTESTED | Forecast-plus-actual median CFPS value |
| 576 | `median_forecast_actual_combined_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency-adjusted forecast-plus-actual median CFPS value |
| 577 | `median_surprise_value_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-provided surprise: actual reported CFPS minus the contemporaneous median consensus estimate (embargo-aware snapsh |
| 578 | `median_surprise_value_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus median CFPS estimate |
| 579 | `min_estimate_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst CFPS estimate for the period (forecast) |
| 580 | `min_estimate_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/currency-adjusted lowest analyst annual CFPS forecast within the p12 window |
| 581 | `stddev_estimate_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation (dispersion) of analyst CFPS estimates |
| 582 | `stddev_estimate_fxadj_cfps_annual12_2` | VECTOR | 0.844 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/FX-adjusted standard deviation of analyst CFPS estimates |
| 583 | `actual_depreciation_value_annual12` | VECTOR | 0.812 | 其他 | 0 | — | — | — | UNTESTED | Actual reported annual depreciation values aligned to events (NaN for pure forecast periods) |
| 584 | `actual_depreciation_value_fxadj_annual12` | VECTOR | 0.812 | 宏观与行业 | 0 | — | — | — | UNTESTED | Adjusted actual annual depreciation values vector (currency/split/regime adjusted) |
| 585 | `estimate_count_current_period_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used in the consensus |
| 586 | `estimate_currency_code_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code for the reporting/estimate units |
| 587 | `forecast_actual_flag_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating provenance/status of the Forecast-plus-Actual overlay (e.g., 0 backfilled, 1 forecast consensus, 2 actua |
| 588 | `forecast_actual_indicator_depreciation_annual12` | VECTOR | 0.812 | 其他 | 0 | — | — | — | UNTESTED | Event indicator showing forecast vs actual periods (M..1 = forecast periods; 0,-1,-2.. = actual/outdated) |
| 589 | `max_estimate_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual depreciation |
| 590 | `max_estimate_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst forecast estimate for annual depreciation |
| 591 | `mean_estimate_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst estimates for annual depreciation |
| 592 | `mean_estimate_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted consensus mean of analyst annual depreciation estimates |
| 593 | `mean_forecast_actual_combined_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean estimate combined with subsequent actuals (FA overlay) for annual depreciation |
| 594 | `mean_forecast_actual_combined_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted consensus mean estimate for annual depreciation, combined with subsequent actuals (FA overlay) |
| 595 | `mean_surprise_value_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise value: actual minus consensus mean estimate for annual depreciation |
| 596 | `mean_surprise_value_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean estimate surprise (actual minus adjusted mean) for annual depreciation |
| 597 | `median_estimate_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for annual depreciation |
| 598 | `median_estimate_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted consensus median of analyst annual depreciation estimates |
| 599 | `median_forecast_actual_combined_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median estimate combined with subsequent actuals (FA overlay) for annual depreciation |
| 600 | `median_forecast_actual_combined_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted consensus median estimate combined with subsequent actuals (FA overlay) for annual depreciation |
| 601 | `median_surprise_value_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise value: actual minus consensus median estimate for annual depreciation |
| 602 | `median_surprise_value_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median estimate surprise (actual minus adjusted median) for annual depreciation |
| 603 | `min_estimate_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual depreciation |
| 604 | `min_estimate_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual depreciation, adjusted for currency/splits/regime effects |
| 605 | `stddev_estimate_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst annual depreciation estimates (forecast only) |
| 606 | `stddev_estimate_fxadj_depreciation_annual12` | VECTOR | 0.812 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for depreciation and amortization, adjusted for currency, for the annual period. |
| 607 | `actual_marketable_securities_value_annual12` | VECTOR | 0.802 | 其他 | 0 | — | — | — | UNTESTED | Reported actual value for Marketable Securities |
| 608 | `actual_marketable_securities_value_fxadj_annual12` | VECTOR | 0.802 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/split-adjusted actual reported values |
| 609 | `estimate_count_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the consensus |
| 610 | `estimate_currency_code_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency code in which annual marketable securities are reported. |
| 611 | `forecast_actual_flag_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating provenance/status of Forecast+Actual data (e.g., 0 backfilled, 1 consensus forecast, 2 actual report) |
| 612 | `forecast_actual_indicator_marketable_securities_annual12` | VECTOR | 0.802 | 其他 | 0 | — | — | — | UNTESTED | Event period indicator for the series (forecast vs actual periods; M…1 = forecast, 0, -1… = actual/outdated) for MKTBLSE |
| 613 | `max_estimate_fxadj_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted highest analyst estimate for Marketable Securities |
| 614 | `max_estimate_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate among forecasts for the measure |
| 615 | `mean_estimate_fxadj_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean consensus estimate |
| 616 | `mean_estimate_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (arithmetic average) of analyst estimates for the measure |
| 617 | `mean_forecast_actual_combined_fxadj_marketable_securities_annual12_2` | VECTOR | 0.802 | 宏观与行业 | 0 | — | — | — | UNTESTED | FX/split/regime-adjusted combined mean forecast plus actuals for annual Marketable Securities |
| 618 | `mean_forecast_actual_combined_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-aware combined series of consensus mean forecasts and subsequent actuals for annual Marketable Securities |
| 619 | `mean_surprise_value_fxadj_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted surprise: actual minus consensus mean estimate |
| 620 | `mean_surprise_value_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise metric: actual minus consensus mean estimate for Marketable Securities, regime-aware |
| 621 | `median_estimate_fxadj_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median estimate adjusted for currency/splits/regime |
| 622 | `median_estimate_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Median (50th percentile) of analyst estimates for the MKTBLSEC annual measure |
| 623 | `median_forecast_actual_combined_fxadj_marketable_securities_annual12` | VECTOR | 0.802 | 宏观与行业 | 0 | — | — | — | UNTESTED | FX/split/regime-adjusted combined median forecast plus actuals |
| 624 | `median_forecast_actual_combined_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-aware combined series of consensus median forecasts and subsequent actuals for Marketable Securities |
| 625 | `median_surprise_value_fxadj_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted surprise: actual minus consensus median estimate |
| 626 | `median_surprise_value_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise metric: actual minus consensus median estimate for Marketable Securities, regime-aware |
| 627 | `min_estimate_fxadj_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted lowest analyst estimate for Marketable Securities |
| 628 | `min_estimate_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate among forecasts for the measure |
| 629 | `stddev_estimate_fxadj_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted standard deviation of analyst estimates for Marketable Securities |
| 630 | `stddev_estimate_marketable_securities_annual12` | VECTOR | 0.802 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates used in the consensus |
| 631 | `actual_value_enterprisevalue_annual12` | VECTOR | 0.800 | 其他 | 0 | — | — | — | UNTESTED | Actual reported EV values vector, with forecast periods filled with nulls/NaNs |
| 632 | `actual_value_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted actual reported value for the EV metric |
| 633 | `estimate_count_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the EV consensus |
| 634 | `forecast_actual_flag_enterprisevalue_annual12` | VECTOR | 0.800 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating provenance/status of Forecast + Actual data (e.g., backfilled/forecast/actual) for EV |
| 635 | `forecast_actual_indicator_enterprisevalue_annual12` | VECTOR | 0.800 | 其他 | 0 | — | — | — | UNTESTED | Event indicator showing forecast vs actual periods (M..1 for forecasts, 0 for current actual, negatives for prior actual |
| 636 | `max_estimate_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst EV estimate (consensus window) |
| 637 | `max_estimate_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted highest analyst estimate for EV |
| 638 | `mean_estimate_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) of analyst estimates for the EV metric |
| 639 | `mean_estimate_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean consensus estimate for EV |
| 640 | `mean_forecast_actual_combined_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate combined with actuals (Forecast + Actual) for EV |
| 641 | `mean_forecast_actual_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted mean estimate combined with actuals (Forecast + Actual) for EV |
| 642 | `mean_surprise_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise: actual minus mean consensus estimate for EV |
| 643 | `mean_surprise_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted surprise based on mean estimate for EV |
| 644 | `median_estimate_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for the EV metric |
| 645 | `median_estimate_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted median analyst estimate for EV |
| 646 | `median_forecast_actual_combined_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Median estimate combined with actuals (Forecast + Actual) for EV |
| 647 | `median_forecast_actual_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted median estimate combined with actuals (Forecast + Actual) for EV |
| 648 | `median_surprise_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise: actual minus median consensus estimate for EV |
| 649 | `median_surprise_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted surprise based on median estimate for EV |
| 650 | `min_estimate_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst EV estimate (consensus window) |
| 651 | `min_estimate_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted lowest analyst estimate for EV |
| 652 | `stddev_estimate_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for the EV metric within the window |
| 653 | `stddev_estimate_fxadj_enterprisevalue_annual12` | VECTOR | 0.800 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted standard deviation of analyst estimates for EV |
| 654 | `actual_return_on_capital_value_annual12` | VECTOR | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual reported value of return on capital for the annual period. |
| 655 | `estimate_count_return_on_capital_annual12` | VECTOR | 0.799 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the ROC consensus |
| 656 | `forecast_actual_flag_return_on_capital_annual12` | VECTOR | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | Flag indicating whether the return on capital value is a forecast, actual, or combined for the annual period. |
| 657 | `forecast_actual_indicator_return_on_capital_annual12` | VECTOR | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | Forecast/actual period indicator per point: M..1 denote forecast horizons; 0, -1, -2 denote actual/reporting periods per |
| 658 | `max_estimate_return_on_capital_annual12` | VECTOR | 0.799 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for ROC |
| 659 | `mean_estimate_return_on_capital_annual12` | VECTOR | 0.799 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus average) of analyst ROC estimates |
| 660 | `mean_forecast_actual_combined_return_on_capital_annual12` | VECTOR | 0.799 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual composite mean consensus for the ROC measure, aligned across forecast and actual periods |
| 661 | `mean_surprise_value_return_on_capital_annual12` | VECTOR | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | Mean of return on capital surprise values (actual minus forecast) for the annual period. |
| 662 | `median_forecast_actual_combined_return_on_capital_annual12` | VECTOR | 0.799 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual composite median estimate for the ROC measure across forecast and actual periods |
| 663 | `median_surprise_value_return_on_capital_annual12` | VECTOR | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | Median of return on capital surprise values (actual minus forecast) for the annual period. |
| 664 | `min_estimate_return_on_capital_annual12` | VECTOR | 0.799 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for ROC |
| 665 | `stddev_estimate_return_on_capital_annual12` | VECTOR | 0.799 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for ROC in the consensus at that time |
| 666 | `actual_goodwill_value_annual12` | VECTOR | 0.793 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Vector of company-reported actual goodwill values for annual periods aligned to the event calendar; forecast positions a |
| 667 | `actual_goodwill_value_fxadj_annual12` | VECTOR | 0.793 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime- and currency/split-adjusted actual reported goodwill value |
| 668 | `estimate_count_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the consensus |
| 669 | `forecast_actual_flag_goodwill_annual12` | VECTOR | 0.793 | 其他 | 0 | — | — | — | UNTESTED | Indicator flag showing if the value is a forecast or actual for annual goodwill. |
| 670 | `forecast_actual_indicator_goodwill_annual12` | VECTOR | 0.793 | 其他 | 0 | — | — | — | UNTESTED | Event indicator marking forecast versus actual periods (M..1 for forecasts; 0, -1, -2 for actuals/outdated) for the good |
| 671 | `max_estimate_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate adjusted for currency (and splits where applicable) |
| 672 | `max_estimate_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for goodwill (forecast only) |
| 673 | `mean_estimate_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted consensus mean estimate for goodwill |
| 674 | `mean_estimate_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean estimate for goodwill |
| 675 | `mean_forecast_actual_combined_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean estimate combined with actuals for goodwill |
| 676 | `mean_forecast_actual_combined_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate combined with actuals (Forecast+Actual vector) for goodwill |
| 677 | `mean_surprise_value_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise based on the mean estimate (Actual minus mean estimate), vendor overlay |
| 678 | `mean_surprise_value_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise based on the mean estimate (Actual minus mean estimate), vendor overlay |
| 679 | `median_estimate_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median estimate for goodwill |
| 680 | `median_estimate_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for goodwill |
| 681 | `median_forecast_actual_combined_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast-plus-Actual composite of the consensus median estimate |
| 682 | `median_forecast_actual_combined_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual composite of the consensus median estimate for goodwill |
| 683 | `median_surprise_value_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise based on the median estimate (Actual minus median estimate), vendor overlay |
| 684 | `median_surprise_value_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise based on the median estimate (Actual minus median estimate), vendor overlay |
| 685 | `min_estimate_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/split/regime-adjusted lowest analyst estimate for goodwill |
| 686 | `min_estimate_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for goodwill (forecast only) |
| 687 | `stddev_estimate_fxadj_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/split/regime-adjusted standard deviation of analyst estimates |
| 688 | `stddev_estimate_goodwill_annual12` | VECTOR | 0.793 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for goodwill |
| 689 | `estimate_count_eps_longterm` | MATRIX | 0.781 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst EPS estimates used to form the consensus |
| 690 | `max_estimate_eps_longterm` | MATRIX | 0.781 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst EPS estimate in the current forecast consensus (forecast-only) |
| 691 | `mean_estimate_eps_longterm` | MATRIX | 0.781 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (average) of analyst EPS estimates within the consensus |
| 692 | `median_estimate_eps_longterm` | MATRIX | 0.781 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst EPS estimates within the consensus |
| 693 | `min_estimate_eps_longterm` | MATRIX | 0.781 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst EPS estimate in the current forecast consensus (forecast-only) |
| 694 | `stddev_estimate_eps_longterm` | MATRIX | 0.781 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst EPS estimates within the consensus |
| 695 | `actual_dividend_value_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual DPS value(s) |
| 696 | `actual_dividend_value_fxadj_annual12_2` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Regime-adjusted actual annual DPS (currency/split adjusted) |
| 697 | `estimate_count_current_period_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Current number of DPS estimates in the consensus |
| 698 | `estimate_count_flash_period_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of flash DPS estimates used in consensus |
| 699 | `estimate_count_four_weeks_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for annual DPS as of 4 weeks ago |
| 700 | `estimate_count_three_months_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of DPS estimates three months ago (vendor overlay) |
| 701 | `forecast_actual_flag_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating Forecast+Actual status/provenance (0 backfilled, 1 consensus forecast, 2 actual) |
| 702 | `forecast_actual_indicator_dividend_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or actual for annual dividend per share. |
| 703 | `max_estimate_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current annual DPS consensus estimate |
| 704 | `max_estimate_four_weeks_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest annual DPS consensus estimate recorded four weeks ago |
| 705 | `max_estimate_four_weeks_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst annual DPS estimate as of four weeks ago, adjusted for currency and stock splits (vendor snapshot) |
| 706 | `max_estimate_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted highest current consensus annual DPS estimate |
| 707 | `max_estimate_three_months_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest annual DPS consensus estimate 3 months ago (historical snapshot) |
| 708 | `max_estimate_three_months_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst dividend per share estimate from three months prior, adjusted for currency, for the annual period. |
| 709 | `mean_estimate_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst consensus estimates for annual Dividend Per Share (DPS) |
| 710 | `mean_estimate_four_weeks_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean annual DPS consensus 4 weeks ago (historical snapshot) |
| 711 | `mean_estimate_four_weeks_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean consensus annual DPS estimate four weeks ago (vendor snapshot) |
| 712 | `mean_estimate_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted current mean consensus annual DPS estimate |
| 713 | `mean_estimate_three_months_prior_dividend_annual12_2` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean annual DPS consensus 3 months ago (historical snapshot) |
| 714 | `mean_estimate_three_months_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean consensus annual DPS estimate three months ago (vendor snapshot) |
| 715 | `mean_flash_estimate_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of flash DPS consensus estimates |
| 716 | `mean_flash_estimate_fxadj_dividend_annual12_2` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted mean annual DPS using flash estimates |
| 717 | `mean_forecast_actual_combined_dividend_annual12_2` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-actual overlay mean for DPS, combining consensus forecasts with subsequent actuals in a regime-aware manne |
| 718 | `mean_forecast_actual_combined_fxadj_dividend_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual composite mean for annual DPS, adjusted for currency and splits |
| 719 | `mean_surprise_value_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean value of the difference between actual and consensus dividend per share for the annual period. |
| 720 | `mean_surprise_value_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor surprise overlay: adjusted difference between actual reported DPS and the consensus mean estimate |
| 721 | `median_estimate_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of current annual DPS consensus estimates |
| 722 | `median_estimate_four_weeks_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median annual DPS consensus estimate recorded four weeks ago |
| 723 | `median_estimate_four_weeks_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median consensus annual DPS estimate four weeks ago (vendor snapshot) |
| 724 | `median_estimate_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted current median consensus annual DPS estimate |
| 725 | `median_estimate_three_months_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median annual DPS consensus 3 months ago (historical snapshot) |
| 726 | `median_estimate_three_months_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median consensus annual DPS estimate three months ago (vendor snapshot) |
| 727 | `median_forecast_actual_combined_dividend_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median annual DPS under the forecast-plus-actual (FA) overlay |
| 728 | `median_forecast_actual_combined_fxadj_dividend_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of combined forecast and actual dividend per share, adjusted for currency, for the annual period. |
| 729 | `median_surprise_value_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median value of the difference between actual and consensus dividend per share for the annual period. |
| 730 | `median_surprise_value_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor surprise overlay: adjusted median difference between actual DPS and consensus estimates |
| 731 | `min_estimate_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest current annual DPS consensus estimate |
| 732 | `min_estimate_four_weeks_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest annual DPS consensus estimate 4 weeks ago (historical snapshot) |
| 733 | `min_estimate_four_weeks_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted lowest consensus annual DPS estimate four weeks ago (vendor snapshot) |
| 734 | `min_estimate_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted lowest current annual DPS estimate in the consensus |
| 735 | `min_estimate_three_months_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest annual DPS consensus estimate recorded three months ago |
| 736 | `min_estimate_three_months_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst dividend per share estimate from three months prior, adjusted for currency, for the annual period. |
| 737 | `stddev_estimate_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Current standard deviation of DPS consensus estimates |
| 738 | `stddev_estimate_four_weeks_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of annual dividend per share (DPS) consensus 4 weeks ago (historical snapshot) |
| 739 | `stddev_estimate_four_weeks_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted standard deviation of annual DPS consensus as of 4 weeks ago |
| 740 | `stddev_estimate_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted current standard deviation of annual DPS consensus |
| 741 | `stddev_estimate_three_months_prior_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of DPS consensus estimates three months ago |
| 742 | `stddev_estimate_three_months_prior_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted standard deviation of annual DPS consensus as of 3 months ago |
| 743 | `stddev_flash_estimate_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of flash DPS consensus estimates |
| 744 | `stddev_flash_estimate_fxadj_dividend_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted standard deviation of annual DPS flash estimates |
| 745 | `actual_revenue_value_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual sales value |
| 746 | `actual_revenue_value_fxadj_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted actual reported sales values (currency/splits/regime adjusted) |
| 747 | `estimate_count_current_period_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the current annual sales consensus |
| 748 | `estimate_count_flash_period_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst Sales flash estimates in the flash snapshot |
| 749 | `estimate_count_four_weeks_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of Sales estimates in the consensus four weeks ago |
| 750 | `estimate_count_three_months_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of Sales estimates in the consensus three months ago |
| 751 | `estimate_currency_code_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer code for the reporting currency of the sales measure (decoded by a lookup table) |
| 752 | `forecast_actual_flag_revenue_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating status of Forecast/Actual combined data or provenance (e.g., 0=backfill, 1=forecast, 2=actual) |
| 753 | `forecast_actual_indicator_revenue_annual12_2` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator flag showing if the value is a forecast or an actual for annual revenue. |
| 754 | `max_estimate_current_period_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current annual sales consensus estimate |
| 755 | `max_estimate_four_weeks_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted highest annual sales consensus estimate from four weeks ago |
| 756 | `max_estimate_four_weeks_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest sales estimate in the consensus four weeks ago |
| 757 | `max_estimate_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current sales estimate adjusted for currency/splits/regime |
| 758 | `max_estimate_three_months_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency- and split-adjusted highest annual sales consensus estimate as of three months ago |
| 759 | `max_estimate_three_months_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest sales estimate in the consensus three months ago |
| 760 | `mean_estimate_current_period_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (average) sales consensus estimate (current) |
| 761 | `mean_estimate_four_weeks_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean sales estimate four weeks ago, adjusted for currency/splits/regime |
| 762 | `mean_estimate_four_weeks_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean sales consensus estimate four weeks ago |
| 763 | `mean_estimate_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency- and split-adjusted current mean of annual sales consensus estimates |
| 764 | `mean_estimate_three_months_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean sales consensus estimate three months ago, adjusted for currency/splits/regime |
| 765 | `mean_estimate_three_months_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean sales consensus estimate three months ago |
| 766 | `mean_flash_estimate_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted mean from flash (snapshot) sales estimates |
| 767 | `mean_flash_estimate_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean from flash (snapshot) sales estimates |
| 768 | `mean_forecast_actual_combined_fxadj_revenue_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted mean of the Forecast-plus-Actual (FA) sales series |
| 769 | `mean_forecast_actual_combined_revenue_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Mean of combined forecast and actual values for annual revenue. |
| 770 | `mean_surprise_value_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted mean sales surprise (actual minus consensus) |
| 771 | `mean_surprise_value_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean sales surprise (actual minus consensus), regime-aware and embargo-sensitive |
| 772 | `median_estimate_current_period_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Current median of analyst annual sales consensus estimates |
| 773 | `median_estimate_four_weeks_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median sales estimate four weeks ago, adjusted for currency/splits/regime |
| 774 | `median_estimate_four_weeks_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median sales consensus estimate four weeks ago |
| 775 | `median_estimate_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted current median sales consensus estimate |
| 776 | `median_estimate_three_months_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median annual sales consensus estimate from three months ago |
| 777 | `median_estimate_three_months_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median Sales estimate at the vendor snapshot three months ago |
| 778 | `median_forecast_actual_combined_fxadj_revenue_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjusted median of the Forecast-plus-Actual (FA) sales series |
| 779 | `median_forecast_actual_combined_revenue_annual12` | VECTOR | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of the Forecast-plus-Actual (FA) sales series (regime-aware) |
| 780 | `median_surprise_value_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median surprise (actual minus median estimate) for annual revenue, adjusted for currency. |
| 781 | `median_surprise_value_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Median surprise (actual minus median estimate) for annual revenue. |
| 782 | `min_estimate_current_period_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest current analyst estimate in the Sales consensus |
| 783 | `min_estimate_four_weeks_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted lowest annual sales consensus estimate from four weeks ago |
| 784 | `min_estimate_four_weeks_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest sales estimate in the consensus four weeks ago |
| 785 | `min_estimate_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted lowest current annual sales consensus estimate |
| 786 | `min_estimate_three_months_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted lowest annual sales consensus estimate from three months ago |
| 787 | `min_estimate_three_months_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest sales estimate in the consensus as of three months ago |
| 788 | `stddev_estimate_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Current standard deviation of annual sales consensus estimates |
| 789 | `stddev_flash_estimate_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted standard deviation of the vendor “flash” consensus Sales estimates |
| 790 | `stddev_flash_estimate_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of flash annual sales consensus estimates |
| 791 | `stddev_four_weeks_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted standard deviation of annual sales consensus estimates from four weeks ago |
| 792 | `stddev_four_weeks_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of sales estimates four weeks ago |
| 793 | `stddev_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted standard deviation of current Sales estimates |
| 794 | `stddev_three_months_prior_fxadj_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency- and split-adjusted standard deviation of annual sales consensus estimates as of three months ago (vendor snaps |
| 795 | `stddev_three_months_prior_revenue_annual12` | VECTOR | 0.762 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of sales estimates three months ago |
| 796 | `actual_currentassets_value_annual12` | VECTOR | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual current assets amount as disclosed by the company |
| 797 | `actual_currentassets_value_fxadj_annual12` | VECTOR | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted actual reported annual current assets amount |
| 798 | `estimate_count_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to compute the consensus for Current Assets |
| 799 | `forecast_actual_flag_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating provenance/status of the forecast-plus-actual (FA) data point (e.g., 0 backfilled, 1 consensus forecast, |
| 800 | `forecast_actual_indicator_currentassets_annual12` | VECTOR | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator specifying if the value is a forecast or actual for current assets, annual period. |
| 801 | `max_estimate_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for Current Assets |
| 802 | `max_estimate_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted highest analyst estimate for Current Assets |
| 803 | `mean_estimate_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) analyst estimate for Current Assets |
| 804 | `mean_estimate_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted mean (consensus) analyst estimate for Current Assets |
| 805 | `mean_forecast_actual_combined_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus estimate for annual current assets combined with subsequent actuals (FA overlay) |
| 806 | `mean_forecast_actual_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean consensus estimate for annual current assets, combined with subsequent actuals (FA o |
| 807 | `mean_surprise_value_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise value: actual minus mean consensus estimate for current assets, regime-aware |
| 808 | `mean_surprise_value_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted surprise for annual current assets based on Actual minus mean estimate |
| 809 | `median_estimate_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate for Current Assets |
| 810 | `median_estimate_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted median analyst estimate for Current Assets |
| 811 | `median_forecast_actual_combined_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus estimate for annual current assets combined with subsequent actuals (FA overlay) |
| 812 | `median_forecast_actual_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median consensus estimate for annual current assets, combined with subsequent actuals (FA |
| 813 | `median_surprise_value_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for annual current assets defined as Actual minus median consensus estimate |
| 814 | `median_surprise_value_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted surprise for annual current assets based on Actual minus median estimate |
| 815 | `min_estimate_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for Current Assets |
| 816 | `min_estimate_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted lowest analyst estimate for Current Assets |
| 817 | `stddev_estimate_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for Current Assets |
| 818 | `stddev_estimate_fxadj_currentassets_annual12` | VECTOR | 0.760 | 修正与预期 | 0 | — | — | — | UNTESTED | FX/regime-adjusted standard deviation of analyst estimates for Current Assets |
| 819 | `actual_ebit_value_annual12_2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual EBI value, unadjusted |
| 820 | `actual_ebit_value_fxadj_annual12_2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency/split adjusted actual reported EBI figures |
| 821 | `estimate_count_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current number of contributing analyst estimates for EBI |
| 822 | `estimate_count_flash_period_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates in the flash snapshot for annual EBI |
| 823 | `estimate_count_four_weeks_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to EBI consensus four weeks ago |
| 824 | `estimate_count_three_months_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to EBI consensus three months ago |
| 825 | `max_estimate_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current highest EBI consensus estimate |
| 826 | `max_estimate_four_weeks_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest EBI consensus estimate as of four weeks ago |
| 827 | `max_estimate_four_weeks_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted highest analyst consensus estimate for annual EBI as of four weeks ago |
| 828 | `max_estimate_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted highest individual EBI estimate in the consensus |
| 829 | `max_estimate_three_months_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest EBI consensus estimate as of three months ago |
| 830 | `max_estimate_three_months_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual Earnings Before Interest (EBI) as of three months ago, adjusted for currency, splits |
| 831 | `mean_estimate_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current mean consensus estimate for annual EBI |
| 832 | `mean_estimate_four_weeks_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus estimate for EBI as of four weeks ago |
| 833 | `mean_estimate_four_weeks_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst estimate for annual EBI as of four weeks ago, adjusted for currency, splits, and regime effects |
| 834 | `mean_estimate_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted consensus mean estimate for annual EBI |
| 835 | `mean_estimate_three_months_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean EBI consensus estimate as of 3 months ago |
| 836 | `mean_estimate_three_months_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst estimate for annual EBI as of three months ago, adjusted for currency, splits, and regime effects |
| 837 | `mean_flash_estimate_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of the flash snapshot analyst estimates for annual EBI |
| 838 | `mean_flash_estimate_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted mean of flash consensus estimates for EBI |
| 839 | `mean_forecast_actual_combined_ebit_annual12_2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast-plus-actual mean overlay for EBI, reflecting regime-aware combination of forecasts and subsequent actuals |
| 840 | `mean_forecast_actual_combined_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency and split adjusted mean of the forecast-plus-actual composite for EBI |
| 841 | `mean_surprise_value_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise based on the mean consensus (actual EBI minus mean estimate) |
| 842 | `mean_surprise_value_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted surprise overlay: actual minus consensus mean for EBI, currency/split adjusted |
| 843 | `median_estimate_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current median of EBI consensus estimates |
| 844 | `median_estimate_four_weeks_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Median EBI consensus estimate as of four weeks ago |
| 845 | `median_estimate_four_weeks_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate for annual EBI as of four weeks ago, adjusted for currency, splits, and regime effects |
| 846 | `median_estimate_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted current median EBI consensus estimate |
| 847 | `median_estimate_three_months_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus estimate for EBI as of three months ago |
| 848 | `median_estimate_three_months_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate for annual EBI as of three months ago, adjusted for currency, splits, and regime effects |
| 849 | `median_forecast_actual_combined_ebit_annual12_2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast-plus-actual median overlay for EBI |
| 850 | `median_forecast_actual_combined_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency and split adjusted median of the forecast-plus-actual composite for EBI |
| 851 | `median_surprise_value_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of the difference between actual and consensus EBIT for the annual period. |
| 852 | `median_surprise_value_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of the currency-adjusted surprise between actual and consensus EBIT for the annual period. |
| 853 | `min_estimate_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current lowest EBI consensus estimate |
| 854 | `min_estimate_four_weeks_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest EBI consensus estimate as of four weeks ago |
| 855 | `min_estimate_four_weeks_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted lowest EBI consensus estimate as of four weeks ago |
| 856 | `min_estimate_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted current lowest EBI consensus estimate |
| 857 | `min_estimate_three_months_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest EBI estimate recorded three months ago |
| 858 | `min_estimate_three_months_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual EBI as of three months ago, adjusted for currency, splits, and regime effects |
| 859 | `stddev_estimate_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current standard deviation of EBI consensus estimates |
| 860 | `stddev_flash_estimate_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of flash EBI consensus estimates |
| 861 | `stddev_flash_estimate_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted standard deviation of flash EBI estimates |
| 862 | `stddev_four_weeks_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of EBI consensus estimates as of four weeks ago |
| 863 | `stddev_four_weeks_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted standard deviation of EBI estimates as of four weeks ago |
| 864 | `stddev_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted standard deviation of EBI consensus estimates |
| 865 | `stddev_three_months_prior_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of EBI estimates three months ago |
| 866 | `stddev_three_months_prior_fxadj_ebit_annual12_2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted standard deviation of EBI consensus estimates as of three months ago |
| 867 | `actual_net_value` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual Net Income (NET) values |
| 868 | `actual_net_value_fxadj` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Regime- and currency-adjusted actual reported annual Net Income (NET) values |
| 869 | `estimate_count_four_weeks_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates in the NET consensus four weeks ago |
| 870 | `estimate_count_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the current NET consensus |
| 871 | `estimate_count_recent_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates in the NET flash snapshot |
| 872 | `estimate_count_three_months_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates in the NET consensus three months ago |
| 873 | `forecast_actual_flag_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating status/provenance of Forecast-plus-Actual data for NET (0 backfilled, 1 forecast consensus, 2 actual) |
| 874 | `forecast_actual_indicator_net2` | VECTOR | 0.759 | 其他 | 0 | — | — | — | UNTESTED | Event indicator vector marking forecast versus actual periods (M..1=forecast, 0,-1,-2=actual/outdated) |
| 875 | `max_estimate_four_weeks_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for net income from four weeks ago, adjusted for currency. |
| 876 | `max_estimate_four_weeks_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest contributor estimate 4 weeks ago for annual Net Income |
| 877 | `max_estimate_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current highest analyst estimate for annual Net Income, currency/split-adjusted |
| 878 | `max_estimate_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current analyst consensus estimate for annual Net Income (unadjusted) |
| 879 | `max_estimate_three_months_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for net income from three months ago, adjusted for currency. |
| 880 | `max_estimate_three_months_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest contributor estimate 3 months ago for annual Net Income |
| 881 | `mean_estimate_four_weeks_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted mean consensus estimate 4 weeks ago for annual Net Income |
| 882 | `mean_estimate_four_weeks_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean NET consensus value from the vendor snapshot four weeks ago |
| 883 | `mean_estimate_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted mean of the current annual Net Income (NET) consensus estimates |
| 884 | `mean_estimate_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current mean NET consensus estimate |
| 885 | `mean_estimate_three_months_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Average analyst estimate for net income from three months ago, adjusted for currency. |
| 886 | `mean_estimate_three_months_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean annual Net Income (NET) consensus value as of three months ago |
| 887 | `mean_forecast_actual_combined_fxadj_net2` | VECTOR | 0.759 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean of the Forecast+Actual composite for NET (regime-aware combination of forecasts and actuals |
| 888 | `mean_forecast_actual_combined_net2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average of combined forecast and actual net income values. |
| 889 | `mean_recent_estimates_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted mean of flash consensus estimates for annual Net Income |
| 890 | `mean_recent_estimates_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of the NET flash estimates overlay |
| 891 | `mean_surprise_value_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Average difference between actual and consensus net income, adjusted for currency. |
| 892 | `mean_surprise_value_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Average difference between actual and consensus net income. |
| 893 | `median_estimate_four_weeks_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median NET consensus value from the vendor snapshot four weeks ago |
| 894 | `median_estimate_four_weeks_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor snapshot of the median consensus estimate for annual Net Income taken 4 weeks ago |
| 895 | `median_estimate_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted current median analyst consensus estimate for annual Net Income |
| 896 | `median_estimate_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Current consensus median estimate for annual Net Income |
| 897 | `median_estimate_three_months_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median NET consensus value from three months ago |
| 898 | `median_estimate_three_months_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor snapshot of the median consensus estimate 3 months ago for annual Net Income |
| 899 | `median_forecast_actual_combined_fxadj_net2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of combined forecast and actual net income values, adjusted for currency. |
| 900 | `median_forecast_actual_combined_net2` | VECTOR | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of combined forecast and actual net income values. |
| 901 | `median_surprise_value_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Median difference between actual and consensus net income, adjusted for currency. |
| 902 | `median_surprise_value_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Median difference between actual and consensus net income. |
| 903 | `min_estimate_four_weeks_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted lowest contributor estimate 4 weeks ago for annual Net Income |
| 904 | `min_estimate_four_weeks_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest NET consensus estimate as of four weeks ago |
| 905 | `min_estimate_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest contributor estimate for annual Net Income, currency/split adjusted |
| 906 | `min_estimate_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest current annual Net Income (NET) consensus estimate |
| 907 | `min_estimate_three_months_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted lowest contributor estimate 3 months ago for annual Net Income |
| 908 | `min_estimate_three_months_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest annual Net Income (NET) estimate as of three months ago |
| 909 | `stddev_estimate_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of current estimates for annual Net Income, currency/split adjusted |
| 910 | `stddev_estimate_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of current analyst consensus estimates for annual Net Income (unadjusted) |
| 911 | `stddev_four_weeks_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for net income from four weeks ago, adjusted for currency. |
| 912 | `stddev_four_weeks_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of annual Net Income (NET) estimates as of four weeks ago |
| 913 | `stddev_recent_estimates_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted standard deviation of the NET flash estimates |
| 914 | `stddev_recent_estimates_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of the NET flash estimates |
| 915 | `stddev_three_months_prior_fxadj_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted standard deviation of estimates 3 months ago for annual Net Income |
| 916 | `stddev_three_months_prior_net2` | VECTOR | 0.759 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of NET consensus estimates from three months ago |
| 917 | `actual_currentliabilities_value_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported actual value for annual current liabilities (unadjusted) |
| 918 | `actual_currentliabilities_value_fxadj_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual current liabilities adjusted for currency/regime effects |
| 919 | `currency_code_currentliabilities_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Integer code identifying the reporting currency for the values |
| 920 | `estimate_count_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of individual analyst estimates contributing to the consensus for annual current liabilities |
| 921 | `forecast_actual_flag_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag for forecast/actual combined data status or provenance (e.g., backfilled, forecast consensus, actual) |
| 922 | `forecast_actual_indicator_currentliabilities_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for current liabilities in the annual period. |
| 923 | `max_estimate_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast (forecast-only consensus high) for annual current liabilities |
| 924 | `max_estimate_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual current liabilities adjusted for currency/splits/regime effects |
| 925 | `mean_estimate_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean analyst forecast for annual current liabilities |
| 926 | `mean_estimate_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean analyst forecast for annual current liabilities adjusted for currency/splits/regime effects |
| 927 | `mean_forecast_actual_combined_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual overlay: regime-aware series combining the consensus mean forecast for annual current liabilities w |
| 928 | `mean_forecast_actual_combined_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean consensus value combining forecasts and actuals for current liabilities |
| 929 | `mean_surprise_value_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for annual current liabilities, calculated as Actual minus mean consensus estimate |
| 930 | `mean_surprise_value_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise for annual current liabilities, calculated as Actual minus mean consensus estimate |
| 931 | `median_estimate_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus analyst forecast for annual current liabilities |
| 932 | `median_estimate_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median analyst forecast for annual current liabilities adjusted for currency/splits/regime effects |
| 933 | `median_forecast_actual_combined_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Combined series of median consensus forecast and subsequent actuals for annual current liabilities |
| 934 | `median_forecast_actual_combined_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency-adjusted median value combining forecasts and actuals for current liabilities |
| 935 | `median_surprise_value_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for annual current liabilities, calculated as Actual minus median consensus estimate |
| 936 | `median_surprise_value_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise based on the median consensus estimate (Actual minus median) for annual current liabilities |
| 937 | `min_estimate_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual current liabilities (forecast-only consensus low) for the period |
| 938 | `min_estimate_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst forecast for annual current liabilities |
| 939 | `stddev_estimate_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual current liabilities |
| 940 | `stddev_estimate_fxadj_currentliabilities_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation of analyst estimates for annual current liabilities |
| 941 | `actual_pretax_value_annual12` | VECTOR | 0.755 | 其他 | 0 | — | — | — | UNTESTED | Actual reported value for the PRE measure (annual); vector aligned to events with NaN for forecast periods |
| 942 | `actual_pretax_value_fxadj_annual12` | VECTOR | 0.755 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime-adjusted actual reported values for the PRE metric (currency/split adjusted) |
| 943 | `estimate_count_current_period_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Current number of analyst estimates contributing to the annual PRE consensus |
| 944 | `estimate_count_flash_period_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of flash (intra-day) analyst estimates contributing to the annual PRE consensus |
| 945 | `estimate_count_four_weeks_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the PRE consensus four weeks ago |
| 946 | `estimate_count_three_months_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates in the PRE consensus three months ago |
| 947 | `forecast_actual_flag_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for annual pre-tax profit. |
| 948 | `forecast_actual_indicator_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for annual pre-tax profit. |
| 949 | `max_estimate_current_period_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current PRE consensus estimate |
| 950 | `max_estimate_four_weeks_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted highest PRE consensus estimate from four weeks ago |
| 951 | `max_estimate_four_weeks_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest consensus estimate for the PRE measure recorded four weeks ago |
| 952 | `max_estimate_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted highest current PRE consensus estimate |
| 953 | `max_estimate_three_months_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted highest PRE consensus estimate from three months ago |
| 954 | `max_estimate_three_months_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst consensus estimate for the PRE measure from 3 months ago |
| 955 | `mean_estimate_current_period_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Current mean PRE consensus estimate |
| 956 | `mean_estimate_four_weeks_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted mean PRE consensus estimate from four weeks ago |
| 957 | `mean_estimate_four_weeks_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean PRE consensus estimate four weeks ago |
| 958 | `mean_estimate_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime/currency/split-adjusted mean analyst consensus estimate for the PRE measure |
| 959 | `mean_estimate_three_months_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted mean PRE consensus estimate from three months ago |
| 960 | `mean_estimate_three_months_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst consensus estimate for the PRE measure from 3 months ago |
| 961 | `mean_flash_estimate_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split-adjusted mean of the flash consensus estimates for annual pre-tax profit (PRE) |
| 962 | `mean_forecast_actual_combined_fxadj_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Mean of combined forecast and actual values for annual pre-tax profit, adjusted for currency. |
| 963 | `mean_forecast_actual_combined_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Mean of combined forecast and actual values for annual pre-tax profit. |
| 964 | `mean_surprise_value_fxadj_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Mean value of the difference between actual and forecasted annual pre-tax profit, currency-adjusted. |
| 965 | `mean_surprise_value_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Mean value of the difference between actual and forecasted annual pre-tax profit. |
| 966 | `median_estimate_current_period_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Current median analyst consensus estimate for the PRE metric |
| 967 | `median_estimate_four_weeks_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median PRE consensus estimate from four weeks ago |
| 968 | `median_estimate_four_weeks_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst consensus for the PRE metric as captured four weeks ago |
| 969 | `median_estimate_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median consensus estimate for the PRE measure (adjusted for currency, splits, and regime effects) |
| 970 | `median_estimate_three_months_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median PRE consensus estimate from three months ago |
| 971 | `median_estimate_three_months_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst consensus estimate for the PRE measure from 3 months ago |
| 972 | `median_forecast_actual_combined_fxadj_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of combined forecast and actual values for annual pre-tax profit, adjusted for currency. |
| 973 | `median_forecast_actual_combined_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of combined forecast and actual values for annual pre-tax profit. |
| 974 | `median_surprise_value_fxadj_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median value of the difference between actual and forecasted annual pre-tax profit, currency-adjusted. |
| 975 | `median_surprise_value_pretax_annual12` | VECTOR | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median value of the difference between actual and forecasted annual pre-tax profit. |
| 976 | `min_estimate_current_period_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Current lowest analyst consensus estimate for the PRE measure |
| 977 | `min_estimate_four_weeks_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest currency-adjusted analyst forecast for annual pre-tax profit as of four weeks ago. |
| 978 | `min_estimate_four_weeks_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst consensus value for the PRE metric as of four weeks ago |
| 979 | `min_estimate_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest currency-adjusted analyst forecast for annual pre-tax profit for the current period. |
| 980 | `min_estimate_three_months_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest currency-adjusted analyst forecast for annual pre-tax profit from three months ago. |
| 981 | `min_estimate_three_months_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst consensus estimate for the PRE measure from 3 months ago |
| 982 | `stddev_current_period_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Current standard deviation of PRE consensus estimates |
| 983 | `stddev_estimate_four_weeks_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of PRE consensus estimates four weeks ago |
| 984 | `stddev_estimate_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime/currency/split-adjusted standard deviation of analyst estimates for the PRE measure |
| 985 | `stddev_flash_estimate_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of the most recent currency-adjusted analyst forecasts for annual pre-tax profit. |
| 986 | `stddev_flash_estimate_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of flash consensus estimates for the PRE measure |
| 987 | `stddev_four_weeks_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of currency-adjusted analyst forecasts for annual pre-tax profit as of four weeks ago. |
| 988 | `stddev_three_months_prior_fxadj_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of currency-adjusted analyst forecasts for annual pre-tax profit from three months ago. |
| 989 | `stddev_three_months_prior_pretax_annual12` | VECTOR | 0.755 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of the PRE consensus three months ago |
| 990 | `actual_totalliab_value_annual12_tribes` | VECTOR | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported Total Liabilities value |
| 991 | `actual_totalliab_value_fxadj_annual12_tribes` | VECTOR | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted actual reported Total Liabilities value |
| 992 | `estimate_count_current_period_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the consensus for annual total liabilities |
| 993 | `estimate_currency_code_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency code in which total liabilities is reported for the annual period. |
| 994 | `forecast_actual_flag_totalliab_annual12_tribes` | VECTOR | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for total liabilities. |
| 995 | `forecast_actual_indicator_totalliab_annual12_tribes` | VECTOR | 0.751 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Event indicator per element: M..1 denote forecast periods ahead, 0, -1, -2… denote actuals or post-actual positions |
| 996 | `max_estimate_fxadj_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted highest analyst forecast estimate for annual total liabilities |
| 997 | `max_estimate_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for annual total liabilities within the consensus set |
| 998 | `mean_estimate_fxadj_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted consensus mean estimate for annual total liabilities |
| 999 | `mean_estimate_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst forecasts for annual total liabilities |
| 1000 | `mean_forecast_actual_combined_fxadj_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted forecast-plus-actual mean estimate for annual total liabilities |
| 1001 | `mean_forecast_actual_combined_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-actual overlay of the consensus mean estimate for annual total liabilities, with forecasts replaced by act |
| 1002 | `mean_surprise_value_fxadj_totalliab_annual12_tribes_2` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise for annual total liabilities based on the mean estimate (actual minus mean) |
| 1003 | `mean_surprise_value_totalliab_annual12_tribes_2` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for annual total liabilities based on the mean consensus (actual minus mean estimate), regime-aware |
| 1004 | `median_estimate_fxadj_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted consensus median estimate for annual total liabilities |
| 1005 | `median_estimate_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median of analyst forecasts for annual total liabilities |
| 1006 | `median_forecast_actual_combined_fxadj_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted forecast-plus-actual median estimate for annual total liabilities |
| 1007 | `median_forecast_actual_combined_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-actual overlay of the consensus median estimate for annual total liabilities |
| 1008 | `median_surprise_value_fxadj_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise for annual total liabilities based on the median estimate (actual minus median) |
| 1009 | `median_surprise_value_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for annual total liabilities based on the median consensus (actual minus median estimate), regime-aware |
| 1010 | `min_estimate_fxadj_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted lowest analyst forecast estimate for annual total liabilities |
| 1011 | `min_estimate_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for annual total liabilities |
| 1012 | `stddev_estimate_fxadj_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation of analyst estimates for annual Total Liabilities |
| 1013 | `stddev_estimate_totalliab_annual12_tribes` | VECTOR | 0.751 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for annual total liabilities |
| 1014 | `actual_ebitdarep_value_annual12` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported annual EBITDA values |
| 1015 | `actual_ebitdarep_value_fxadj_annual12` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency-adjusted actual values for annual Reported EBITDA aligned to event periods |
| 1016 | `estimate_count_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to form the consensus for annual Reported EBITDA |
| 1017 | `forecast_actual_flag_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating data provenance/status within the Forecast+Actual overlay (e.g., 0 backfilled, 1 forecast consensus, 2 a |
| 1018 | `forecast_actual_indicator_ebitdarep_annual12` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event-type indicator for each point: positive values denote forecast periods (e.g., M..1), non-positive denote actual/ou |
| 1019 | `max_estimate_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual Reported EBITDA for the period (forecast only) |
| 1020 | `max_estimate_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual Reported EBITDA, adjusted for currency/splits |
| 1021 | `mean_estimate_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst estimates for annual Reported EBITDA for each period |
| 1022 | `mean_estimate_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus estimate for annual Reported EBITDA adjusted for currency/splits |
| 1023 | `mean_forecast_actual_combined_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast+Actual composite for mean: mean estimates during forecast periods, switching to actuals when reported for annua |
| 1024 | `mean_forecast_actual_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast+Actual composite for mean: mean estimates for forecast periods, switching to actuals when rep |
| 1025 | `mean_surprise_value_ebitda_reported_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor surprise overlay: Actual minus mean consensus estimate at time of reporting for annual Reported EBITDA |
| 1026 | `mean_surprise_value_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise overlay: Actual minus mean consensus estimate for annual Reported EBITDA |
| 1027 | `median_estimate_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for annual Reported EBITDA for each period |
| 1028 | `median_estimate_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate for annual Reported EBITDA, adjusted for currency/splits |
| 1029 | `median_forecast_actual_combined_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecasts for annual reported EBITDA combined with subsequent actuals in the regime-aware Forecast+Act |
| 1030 | `median_forecast_actual_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast+Actual composite for median: median estimates for forecast periods, switching to actuals when |
| 1031 | `median_surprise_value_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor surprise overlay: Actual minus median consensus estimate at time of reporting for annual Reported EBITDA |
| 1032 | `median_surprise_value_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise overlay: Actual minus median consensus estimate for annual Reported EBITDA |
| 1033 | `min_estimate_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual Reported EBITDA for the period (forecast only) |
| 1034 | `min_estimate_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual Reported EBITDA, adjusted for currency/splits |
| 1035 | `stddev_estimate_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual Reported EBITDA |
| 1036 | `stddev_estimate_fxadj_ebitdarep_annual12` | VECTOR | 0.750 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual Reported EBITDA, adjusted for currency/splits |
| 1037 | `actual_gps_value` | VECTOR | 0.749 | 其他 | 0 | — | — | — | UNTESTED | Actual reported value for the GPS measure (as reported, unadjusted) |
| 1038 | `actual_gps_value_fxadj` | VECTOR | 0.749 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/split-adjusted actual reported values for the GPS measure |
| 1039 | `estimate_count_current_period_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Current number of contributing analyst estimates for the GPS measure |
| 1040 | `estimate_count_four_weeks_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates for the GPS measure as of 4 weeks ago |
| 1041 | `estimate_count_recent_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of flash analyst estimates for the GPS measure |
| 1042 | `estimate_count_three_months_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates for the GPS measure as of 3 months ago |
| 1043 | `forecast_actual_flag_gps` | VECTOR | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator flag specifying whether the value is a forecast or an actual fully reported earnings per share. |
| 1044 | `forecast_actual_indicator_gps` | VECTOR | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator specifying whether the value is a forecast or an actual for fully reported earnings per share. |
| 1045 | `max_estimate_current_period_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current consensus estimate for the GPS metric |
| 1046 | `max_estimate_four_weeks_prior_fxadj_gps2` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for fully reported EPS from four weeks ago, adjusted for currency. |
| 1047 | `max_estimate_four_weeks_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest individual estimate in the consensus as of the vendor's 4 weeks ago snapshot for GPS |
| 1048 | `max_estimate_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted highest current consensus estimate for the GPS measure |
| 1049 | `max_estimate_three_months_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted highest consensus estimate from the vendor snapshot three months ago |
| 1050 | `max_estimate_three_months_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest consensus estimate from the vendor snapshot three months ago |
| 1051 | `mean_estimate_current_period_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Current mean consensus estimate for the GPS measure |
| 1052 | `mean_estimate_four_weeks_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted consensus mean estimate for the GPS metric as of four weeks prior |
| 1053 | `mean_estimate_four_weeks_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean estimate for the GPS metric as of four weeks prior |
| 1054 | `mean_estimate_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted current mean consensus estimate for the GPS measure |
| 1055 | `mean_estimate_three_months_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted consensus mean estimate for the GPS metric as of three months prior |
| 1056 | `mean_estimate_three_months_prior_gps2` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean estimate for the GPS metric as of three months prior |
| 1057 | `mean_forecast_actual_combined_fxadj_gps2` | VECTOR | 0.749 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency and split-adjusted mean of the Forecast-plus-Actual composite for the annual GPS measure |
| 1058 | `mean_forecast_actual_combined_gps` | VECTOR | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average of both forecasted and actual fully reported earnings per share for the period. |
| 1059 | `mean_recent_estimates_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted mean of the flash (vendor quick-update) consensus estimates |
| 1060 | `mean_recent_estimates_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of flash estimates for the GPS measure |
| 1061 | `mean_surprise_value_fxadj_gps` | VECTOR | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average difference between actual and forecasted fully reported earnings per share, adjusted for currency effects. |
| 1062 | `mean_surprise_value_gps2` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Average difference between actual and consensus fully reported EPS. |
| 1063 | `median_estimate_four_weeks_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median consensus estimate for the GPS measure four weeks ago (vendor snapshot) |
| 1064 | `median_estimate_four_weeks_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus estimate four weeks ago for GPS (vendor historical snapshot, unadjusted) |
| 1065 | `median_estimate_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted current median consensus estimate for the GPS measure |
| 1066 | `median_estimate_gps2` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Current median consensus estimate for the annual GPS measure |
| 1067 | `median_estimate_three_months_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted median consensus estimate from the vendor snapshot three months ago |
| 1068 | `median_estimate_three_months_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus estimate for the GPS metric as of three months prior |
| 1069 | `median_forecast_actual_combined_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted median of the Forecast+Actual (FA) composite for the GPS measure, combining consensus forecasts with actuals in |
| 1070 | `median_forecast_actual_combined_gps2` | VECTOR | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of both forecasted and actual fully reported earnings per share for the period. |
| 1071 | `median_surprise_value_fxadj_gps` | VECTOR | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median difference between actual and forecasted fully reported earnings per share, adjusted for currency effects. |
| 1072 | `median_surprise_value_gps` | VECTOR | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median difference between actual and forecasted fully reported earnings per share (surprise) for the period. |
| 1073 | `min_estimate_four_weeks_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted lowest consensus estimate for the GPS measure as of four weeks ago (vendor snapshot) |
| 1074 | `min_estimate_four_weeks_prior_gps2` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest consensus estimate for the GPS metric as of four weeks prior |
| 1075 | `min_estimate_fxadj_gps2` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted current lowest consensus estimate for the GPS measure |
| 1076 | `min_estimate_gps2` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Current lowest consensus estimate for the GPS measure |
| 1077 | `min_estimate_three_months_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted lowest consensus estimate from the vendor snapshot three months ago |
| 1078 | `min_estimate_three_months_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest consensus estimate from the vendor snapshot three months ago |
| 1079 | `stddev_estimate_gps2` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Current standard deviation of analyst estimates for the GPS consensus |
| 1080 | `stddev_four_weeks_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted standard deviation of analyst estimates for the GPS measure as of 4 weeks ago |
| 1081 | `stddev_four_weeks_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of consensus estimates from the vendor snapshot four weeks ago |
| 1082 | `stddev_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted standard deviation of current analyst estimates for the GPS measure |
| 1083 | `stddev_recent_estimates_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted standard deviation of the flash (vendor quick-update) consensus estimates |
| 1084 | `stddev_recent_estimates_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of the flash (vendor quick-update) consensus estimates |
| 1085 | `stddev_three_months_prior_fxadj_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted standard deviation of consensus estimates for the GPS metric as of three months prior |
| 1086 | `stddev_three_months_prior_gps` | VECTOR | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of consensus estimates for the GPS metric as of three months prior |
| 1087 | `actual_operatingexpense_value_annual12` | VECTOR | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Actual reported annual operating expenses |
| 1088 | `actual_operatingexpense_value_fxadj_annual12` | VECTOR | 0.746 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted actual reported annual operating expenses |
| 1089 | `estimate_count_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the annual operating expenses consensus |
| 1090 | `estimate_currency_code_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency code in which the operating expense estimate or actual is reported for the annual period. |
| 1091 | `forecast_actual_flag_operatingexpense_annual12` | VECTOR | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for operating expense in the annual period. |
| 1092 | `forecast_actual_indicator_operatingexpense_annual12` | VECTOR | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating whether the value is a forecast or actual for operating expense in the annual period. |
| 1093 | `max_estimate_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst forecast estimate for annual operating expenses |
| 1094 | `max_estimate_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual operating expenses (forecast-only) |
| 1095 | `mean_estimate_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean (consensus) of analyst estimates for OPREXP |
| 1096 | `mean_estimate_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst consensus estimate for annual operating expenses |
| 1097 | `mean_forecast_actual_combined_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean analyst consensus combined with actuals (Forecast+Actual) for annual operating expenses |
| 1098 | `mean_forecast_actual_combined_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst consensus for annual operating expenses in the Forecast+Actual overlay |
| 1099 | `mean_surprise_value_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Average difference between actual and adjusted consensus operating expense for the annual period. |
| 1100 | `mean_surprise_value_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Average difference between actual and consensus operating expense for the annual period. |
| 1101 | `median_estimate_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median analyst consensus estimate for annual operating expenses |
| 1102 | `median_estimate_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst consensus estimate for annual operating expenses |
| 1103 | `median_forecast_actual_combined_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median analyst consensus for annual operating expenses, combined with actuals in the Forecast+Actual o |
| 1104 | `median_forecast_actual_combined_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst consensus for annual operating expenses in the Forecast+Actual overlay |
| 1105 | `median_surprise_value_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 宏观与行业 | 0 | — | — | — | UNTESTED | Median of the difference between actual and forecasted operating expense, adjusted for currency, for the annual period. |
| 1106 | `median_surprise_value_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of the difference between actual and consensus operating expense for the annual period. |
| 1107 | `min_estimate_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst forecast estimate for annual operating expenses |
| 1108 | `min_estimate_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual operating expenses (forecast-only) |
| 1109 | `stddev_estimate_fxadj_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of adjusted operating expense estimates for the annual period. |
| 1110 | `stddev_estimate_operatingexpense_annual12` | VECTOR | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual operating expenses |
| 1111 | `actual_cashflowinvesting_value_annual12` | VECTOR | 0.744 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Actual reported annual CFINVEST values, with forecast periods typically filled with NaN |
| 1112 | `actual_cashflowinvesting_value_fxadj_annual12` | VECTOR | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency-adjusted actual reported Cash Flow from Investing (converted to default currency and split-adjusted as applicab |
| 1113 | `estimate_count_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used in the consensus for annual CFINVEST |
| 1114 | `estimate_currency_code_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer code for the report currency of the measure values |
| 1115 | `forecast_actual_flag_cashflowinvesting_annual12` | VECTOR | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for annual cash flow from investing. |
| 1116 | `forecast_actual_indicator_cashflowinvesting_annual12` | VECTOR | 0.744 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Forecast or actual period indicator for each event in the series, with M..1 for forecast periods and 0, -1, -2 for actua |
| 1117 | `max_estimate_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for cash flow from investing |
| 1118 | `max_estimate_fxadj_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst estimate |
| 1119 | `mean_estimate_cfinvest_annual12_tribes` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst estimates for cash flow from investing |
| 1120 | `mean_estimate_fxadj_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted mean consensus estimate for annual CFINVEST |
| 1121 | `mean_forecast_actual_combined_cashflowinvesting_annual12` | VECTOR | 0.744 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Forecast-plus-actual mean for annual CFINVEST |
| 1122 | `mean_forecast_actual_combined_fxadj_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency adjusted forecast-plus-actual composite: mean consensus for annual CFINVEST aligned with actuals |
| 1123 | `mean_surprise_value_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean estimate surprise for cash flow from investing (actual minus mean consensus) |
| 1124 | `mean_surprise_value_fxadj_cfinvest_annual12_tribes` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted mean estimate surprise for cash flow from investing (actual minus mean consensus) |
| 1125 | `median_estimate_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst estimates for annual CFINVEST |
| 1126 | `median_estimate_fxadj_cfinvest_annual12_tribes` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted median consensus estimate for annual CFINVEST |
| 1127 | `median_forecast_actual_combined_cfinvest_annual12_tribes` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-provided forecast-plus-actual composite series: the median consensus estimate for annual Cash Flow from Investing |
| 1128 | `median_forecast_actual_combined_fxadj_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency adjusted forecast-plus-actual composite: median consensus for annual CFINVEST aligned with actuals |
| 1129 | `median_surprise_value_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Median estimate surprise for cash flow from investing (actual minus median consensus) |
| 1130 | `median_surprise_value_fxadj_cfinvest_annual12_tribes` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted median estimate surprise for cash flow from investing (actual minus median consensus) |
| 1131 | `min_estimate_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for cash flow from investing |
| 1132 | `min_estimate_fxadj_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst estimate for cash flow from investing |
| 1133 | `stddev_estimate_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for cash flow from investing |
| 1134 | `stddev_estimate_fxadj_cashflowinvesting_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of currency-adjusted analyst estimates for annual cash flow from investing. |
| 1135 | `actual_nav_value_annual12` | VECTOR | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported net asset value for the annual period. |
| 1136 | `actual_nav_value_fxadj_annual12` | VECTOR | 0.744 | 宏观与行业 | 0 | — | — | — | UNTESTED | Actual reported annual NAV value adjusted for currency/splits/regime |
| 1137 | `estimate_count_current_period_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts contributing to the current annual NAV consensus |
| 1138 | `estimate_count_flash_period_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of flash annual NAV estimates |
| 1139 | `estimate_count_four_weeks_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of annual NAV estimates in the consensus four weeks ago |
| 1140 | `estimate_count_three_months_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of annual NAV estimates in the consensus three months ago |
| 1141 | `forecast_actual_flag_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating status/provenance of forecast-plus-actual data (e.g., backfilled, consensus forecast, actual) |
| 1142 | `forecast_actual_indicator_nav_annual12` | VECTOR | 0.744 | 其他 | 0 | — | — | — | UNTESTED | Forecast/Actual period indicator marking forecast periods (M..1) and actual periods (0, -1, …) for the NAV series |
| 1143 | `max_estimate_current_period_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current analyst estimate in the annual NAV consensus |
| 1144 | `max_estimate_four_weeks_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split-adjusted highest annual NAV estimate four weeks ago |
| 1145 | `max_estimate_four_weeks_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest net asset value estimate from four weeks prior for the annual period. |
| 1146 | `max_estimate_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Current highest annual NAV estimate, adjusted for currency/splits/regime |
| 1147 | `max_estimate_three_months_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest annual NAV estimate from three months ago, adjusted for currency/splits/regime |
| 1148 | `max_estimate_three_months_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest annual NAV estimate three months ago |
| 1149 | `mean_estimate_current_period_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Current consensus mean estimate for annual NAV |
| 1150 | `mean_estimate_four_weeks_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split-adjusted mean annual NAV consensus four weeks ago |
| 1151 | `mean_estimate_four_weeks_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus annual NAV estimate as of four weeks ago |
| 1152 | `mean_estimate_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split-adjusted current consensus mean for annual NAV |
| 1153 | `mean_estimate_three_months_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of currency-adjusted net asset value estimates from three months prior for the annual period. |
| 1154 | `mean_estimate_three_months_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of annual NAV consensus estimates three months ago |
| 1155 | `mean_flash_estimate_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of currency-adjusted flash net asset value estimates for the annual period. |
| 1156 | `mean_flash_estimate_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of flash annual NAV estimates |
| 1157 | `mean_forecast_actual_combined_fxadj_nav_annual12` | VECTOR | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average of currency-adjusted forecast and actual net asset value for the annual period. |
| 1158 | `mean_forecast_actual_combined_nav_annual12` | VECTOR | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average of forecast and actual net asset value for the annual period. |
| 1159 | `mean_surprise_value_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Average surprise (actual minus mean estimate) for net asset value, adjusted for currency, in the annual period. |
| 1160 | `mean_surprise_value_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Average surprise (actual minus mean estimate) for net asset value in the annual period. |
| 1161 | `median_estimate_four_weeks_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of currency-adjusted net asset value estimates from four weeks prior for the annual period. |
| 1162 | `median_estimate_four_weeks_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of annual NAV consensus estimates four weeks ago |
| 1163 | `median_estimate_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split-adjusted median estimate for annual NAV |
| 1164 | `median_estimate_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Current median consensus annual NAV estimate |
| 1165 | `median_estimate_three_months_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Median annual NAV estimate from three months ago, adjusted for currency/splits/regime |
| 1166 | `median_estimate_three_months_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Median NAV consensus estimate three months ago |
| 1167 | `median_forecast_actual_combined_fxadj_nav_annual12` | VECTOR | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of currency-adjusted forecast and actual net asset value for the annual period. |
| 1168 | `median_forecast_actual_combined_nav_annual12` | VECTOR | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of forecast and actual net asset value for the annual period. |
| 1169 | `median_surprise_value_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Median surprise (actual minus estimate) for net asset value, adjusted for currency, in the annual period. |
| 1170 | `median_surprise_value_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Median surprise (actual minus estimate) for net asset value in the annual period. |
| 1171 | `min_estimate_current_period_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest current analyst estimate in the annual NAV consensus |
| 1172 | `min_estimate_four_weeks_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest currency-adjusted net asset value estimate from four weeks prior for the annual period. |
| 1173 | `min_estimate_four_weeks_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest annual NAV estimate four weeks ago |
| 1174 | `min_estimate_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest currency-adjusted net asset value estimate for the annual period. |
| 1175 | `min_estimate_three_months_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest annual NAV estimate from three months ago, adjusted for currency/splits/regime |
| 1176 | `min_estimate_three_months_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest annual NAV estimate three months ago |
| 1177 | `stddev_estimate_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Current standard deviation of annual NAV estimates, adjusted for currency/splits/regime |
| 1178 | `stddev_estimate_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of current consensus annual NAV estimates |
| 1179 | `stddev_flash_estimate_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of currency-adjusted flash net asset value estimates for the annual period. |
| 1180 | `stddev_flash_estimate_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of flash annual NAV estimates |
| 1181 | `stddev_four_weeks_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split-adjusted standard deviation of annual NAV estimates four weeks ago |
| 1182 | `stddev_four_weeks_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of annual NAV estimates four weeks ago |
| 1183 | `stddev_three_months_prior_fxadj_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split-adjusted standard deviation of annual NAV estimates three months ago |
| 1184 | `stddev_three_months_prior_nav_annual12` | VECTOR | 0.744 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of annual NAV estimates three months ago |
| 1185 | `actual_grossmargin_value_annual12_tribes` | VECTOR | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported actual GPM value for the relevant fiscal period |
| 1186 | `actual_reportednet_value_annual12_2` | VECTOR | 0.743 | 其他 | 0 | — | — | — | UNTESTED | Actual reported NER value |
| 1187 | `actual_reportednet_value_fxadj_annual12_2` | VECTOR | 0.743 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime-adjusted actual NER value (currency/splits adjusted) |
| 1188 | `estimate_count_flash_period_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of flash (intra-period) analyst estimates for the NER measure |
| 1189 | `estimate_count_four_weeks_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the consensus 4 weeks ago for the NER measure |
| 1190 | `estimate_count_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the consensus for the period |
| 1191 | `estimate_count_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Current number of analyst estimates in the consensus for the annual NER measure |
| 1192 | `estimate_count_three_months_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the consensus 3 months ago for the NER measure |
| 1193 | `forecast_actual_flag_grossmargin_annual12_tribes` | VECTOR | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing if the value is a forecast or an actual for gross margin. |
| 1194 | `forecast_actual_indicator_grossmargin_annual12_tribes` | VECTOR | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Event indicator marking forecast versus actual periods for the series (M…1 for forecasts, 0, -1, -2… for actual/outdated |
| 1195 | `max_estimate_four_weeks_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual reported net income four weeks ago, adjusted for currency and splits. |
| 1196 | `max_estimate_four_weeks_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual reported net income as of four weeks ago. |
| 1197 | `max_estimate_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual reported net income, adjusted for currency and splits. |
| 1198 | `max_estimate_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for the GPM measure |
| 1199 | `max_estimate_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current consensus NER estimate |
| 1200 | `max_estimate_three_months_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast for annual reported net income three months ago, adjusted for currency and splits. |
| 1201 | `max_estimate_three_months_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest consensus NER estimate as of three months ago |
| 1202 | `mean_estimate_four_weeks_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Average analyst forecast for annual reported net income as of four weeks ago, adjusted for currency and splits. |
| 1203 | `mean_estimate_four_weeks_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus NER estimate four weeks ago |
| 1204 | `mean_estimate_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted current consensus mean for NER |
| 1205 | `mean_estimate_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst forecast estimates for the GPM measure |
| 1206 | `mean_estimate_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Current consensus mean NER estimate |
| 1207 | `mean_estimate_three_months_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Average analyst forecast for annual reported net income three months ago, adjusted for currency and splits. |
| 1208 | `mean_estimate_three_months_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus NER estimate three months ago |
| 1209 | `mean_flash_estimate_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Average analyst forecast for annual reported net income in the flash period, adjusted for currency and splits. |
| 1210 | `mean_flash_estimate_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of flash consensus NER estimates |
| 1211 | `mean_forecast_actual_combined_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Average of both analyst forecasts and actuals for annual reported net income, adjusted for currency and splits. |
| 1212 | `mean_forecast_actual_combined_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual composite: mean estimate combined with actuals in a regime-aware vector |
| 1213 | `mean_forecast_actual_combined_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-aware forecast-plus-actual mean for the NER measure, combining consensus forecasts with subsequently reported act |
| 1214 | `mean_surprise_value_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average surprise (actual minus forecast) for annual reported net income, adjusted for currency and splits. |
| 1215 | `mean_surprise_value_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise: actual minus mean consensus estimate for Gross Profit Margin |
| 1216 | `mean_surprise_value_reportednet_annual12_2` | VECTOR | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average surprise (actual minus forecast) for annual reported net income. |
| 1217 | `median_estimate_four_weeks_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst forecast for annual reported net income four weeks ago, adjusted for currency and splits. |
| 1218 | `median_estimate_four_weeks_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst forecast for annual reported net income as of four weeks ago. |
| 1219 | `median_estimate_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median current consensus NER estimate |
| 1220 | `median_estimate_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median of analysts’ Gross Profit Margin estimates for the period |
| 1221 | `median_estimate_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Current median of NER consensus estimates |
| 1222 | `median_estimate_three_months_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst forecast for annual reported net income three months ago, adjusted for currency and splits. |
| 1223 | `median_estimate_three_months_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus NER estimate three months ago |
| 1224 | `median_forecast_actual_combined_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of both analyst forecasts and actuals for annual reported net income, adjusted for currency and splits. |
| 1225 | `median_forecast_actual_combined_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual composite: median estimate combined with actuals in a regime-aware vector |
| 1226 | `median_forecast_actual_combined_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of both analyst forecasts and actuals for annual reported net income. |
| 1227 | `median_surprise_value_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median surprise (actual minus forecast) for annual reported net income, adjusted for currency and splits. |
| 1228 | `median_surprise_value_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor-reported surprise: actual minus median consensus estimate for Gross Profit Margin |
| 1229 | `median_surprise_value_reportednet_annual12_2` | VECTOR | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median surprise (actual minus forecast) for annual reported net income. |
| 1230 | `min_estimate_four_weeks_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual reported net income four weeks ago, adjusted for currency and splits. |
| 1231 | `min_estimate_four_weeks_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual reported net income as of four weeks ago. |
| 1232 | `min_estimate_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted lowest current consensus NER estimate |
| 1233 | `min_estimate_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for the GPM measure within the consensus window |
| 1234 | `min_estimate_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest current consensus NER estimate |
| 1235 | `min_estimate_three_months_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast for annual reported net income three months ago, adjusted for currency and splits. |
| 1236 | `min_estimate_three_months_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest consensus NER estimate three months ago |
| 1237 | `stddev_estimate_grossmargin_annual12_tribes` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecast estimates for the GPM consensus |
| 1238 | `stddev_flash_estimate_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for annual reported net income in the flash period, adjusted for currency and sp |
| 1239 | `stddev_flash_estimate_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of flash consensus NER estimates |
| 1240 | `stddev_four_weeks_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for annual reported net income four weeks ago, adjusted for currency and splits. |
| 1241 | `stddev_four_weeks_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for annual reported net income four weeks ago. |
| 1242 | `stddev_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted standard deviation of current NER consensus estimates |
| 1243 | `stddev_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of current consensus NER estimates |
| 1244 | `stddev_three_months_prior_fxadj_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for annual reported net income three months ago, adjusted for currency and split |
| 1245 | `stddev_three_months_prior_reportednet_annual12_2` | VECTOR | 0.743 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of consensus NER estimates three months ago |
| 1246 | `actual_inventory_value_annual12` | VECTOR | 0.740 | 其他 | 0 | — | — | — | UNTESTED | Actual reported annual Inventory value |
| 1247 | `actual_inventory_value_fxadj_annual12` | VECTOR | 0.740 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted actual annual inventory value |
| 1248 | `estimate_count_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used in the INVENTORY consensus for the period |
| 1249 | `estimate_currency_code_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer currency code for the inventory measure, decoded by date to the reporting currency |
| 1250 | `forecast_actual_flag_inventory_annual12_2` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating status/provenance of forecast-plus-actual data (0 backfilled, 1 consensus forecast, 2 actual) |
| 1251 | `forecast_actual_indicator_inventory_annual12` | VECTOR | 0.740 | 其他 | 0 | — | — | — | UNTESTED | Period indicator for each data point: positive values represent forecast periods (M..1), 0 and negatives represent actua |
| 1252 | `max_estimate_fxadj_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted highest analyst estimate for INVENTORY |
| 1253 | `max_estimate_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for the INVENTORY measure for the given annual period (forecast only) |
| 1254 | `mean_estimate_fxadj_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted mean (consensus) estimate for INVENTORY |
| 1255 | `mean_estimate_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) of analyst estimates for the INVENTORY measure (forecast only) |
| 1256 | `mean_forecast_actual_combined_fxadj_inventory_annual12_2` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted Forecast+Actual composite mean for INVENTORY, using consensus in forecast periods and actual |
| 1257 | `mean_forecast_actual_combined_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast+Actual composite mean for INVENTORY, regime-aware combination of consensus forecasts and actuals |
| 1258 | `mean_surprise_value_fxadj_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/regime-adjusted surprise versus mean consensus (actual minus mean estimate) for annual inventory |
| 1259 | `mean_surprise_value_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise relative to consensus mean: actual Inventory minus the mean estimate |
| 1260 | `median_estimate_fxadj_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted median analyst estimate for INVENTORY |
| 1261 | `median_estimate_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median of analyst forecasts for annual inventory |
| 1262 | `median_forecast_actual_combined_fxadj_inventory_annual12` | VECTOR | 0.740 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency and split adjusted Forecast+Actual composite median for INVENTORY, regime-aware |
| 1263 | `median_forecast_actual_combined_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast+Actual composite median for INVENTORY, using consensus during forecast periods and actuals once reported |
| 1264 | `median_surprise_value_fxadj_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus median consensus for annual inventory |
| 1265 | `median_surprise_value_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus median consensus (actual minus median estimate) for annual inventory, regime-aware |
| 1266 | `min_estimate_fxadj_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency and split adjusted lowest analyst estimate for INVENTORY |
| 1267 | `min_estimate_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for the INVENTORY measure for the given annual period within the consensus window (forecast only |
| 1268 | `stddev_estimate_fxadj_inventory_annual12_2` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation of analyst Inventory estimates |
| 1269 | `stddev_estimate_inventory_annual12` | VECTOR | 0.740 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for the INVENTORY consensus (forecast only) |
| 1270 | `actual_roe_value_annual12` | VECTOR | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported value for annual return on equity. |
| 1271 | `estimate_count_current_period_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Current number of analyst estimates contributing to ROE consensus |
| 1272 | `estimate_count_flash_period_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst flash estimates contributing to ROE consensus |
| 1273 | `estimate_count_four_weeks_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for annual ROE as of four weeks ago |
| 1274 | `estimate_count_three_months_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates for annual ROE as of three months ago |
| 1275 | `forecast_actual_flag_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating status/provenance of Forecast+Actual combined data for ROE (0=backfilled, 1=consensus forecast, 2=actual |
| 1276 | `forecast_actual_indicator_roe_annual12` | VECTOR | 0.737 | 其他 | 0 | — | — | — | UNTESTED | Event indicator marking forecast vs actual periods (M..1 = forecast, 0,-1.. = actual) for ROE |
| 1277 | `max_estimate_current_period_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current consensus estimate for annual ROE |
| 1278 | `max_estimate_four_weeks_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor snapshot of the highest annual ROE estimate 4 weeks prior |
| 1279 | `max_estimate_three_months_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest annual ROE estimate 3 months prior |
| 1280 | `mean_estimate_current_period_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean ROE consensus estimate |
| 1281 | `mean_estimate_four_weeks_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean annual ROE consensus 4 weeks prior |
| 1282 | `mean_estimate_three_months_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean annual ROE consensus 3 months prior |
| 1283 | `mean_flash_estimate_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean ROE consensus including flash updates |
| 1284 | `mean_forecast_actual_combined_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of the Forecast+Actual overlay for ROE, combining consensus forecasts with subsequent actuals |
| 1285 | `mean_surprise_value_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean surprise for annual ROE (actual minus consensus), regime-aware and masked during blackout periods |
| 1286 | `median_estimate_current_period_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Median ROE consensus estimate |
| 1287 | `median_estimate_four_weeks_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor snapshot of the median consensus estimate for annual ROE taken 4 weeks prior |
| 1288 | `median_estimate_three_months_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Median annual ROE consensus 3 months prior |
| 1289 | `median_forecast_actual_combined_roe_annual12` | VECTOR | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of combined forecast and actual values for annual return on equity. |
| 1290 | `median_surprise_value_roe_annual12` | VECTOR | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median value of the difference between actual and forecasted annual return on equity. |
| 1291 | `min_estimate_current_period_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest current ROE consensus estimate |
| 1292 | `min_estimate_four_weeks_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest annual ROE estimate 4 weeks prior |
| 1293 | `min_estimate_three_months_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest annual ROE estimate 3 months prior |
| 1294 | `stddev_current_period_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of ROE consensus estimates |
| 1295 | `stddev_flash_estimate_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of ROE consensus estimates including flash updates |
| 1296 | `stddev_four_weeks_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Vendor snapshot of the standard deviation of annual ROE estimates 4 weeks prior |
| 1297 | `stddev_three_months_prior_roe_annual12` | VECTOR | 0.737 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of annual ROE estimates 3 months prior |
| 1298 | `actual_value_fcfps_annual12` | VECTOR | 0.736 | 其他 | 0 | — | — | — | UNTESTED | Reported actual annual FCFPS values aligned to the event timeline (forecast periods empty) |
| 1299 | `actual_value_fxadj_fcfps_annual12` | VECTOR | 0.736 | 宏观与行业 | 0 | — | — | — | UNTESTED | Actual annual FCFPS values adjusted for currency and corporate actions (e.g., splits) |
| 1300 | `currency_type_fcfps_annual12` | VECTOR | 0.736 | 宏观与行业 | 0 | — | — | — | UNTESTED | Integer currency code per data point, referencing a decode table for report currency |
| 1301 | `estimate_count_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of contributing analyst estimates used to compute the FCFPS consensus |
| 1302 | `max_estimate_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for annual FCFPS |
| 1303 | `max_estimate_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for FCFPS after currency/split adjustments |
| 1304 | `mean_estimate_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of analyst forecast estimates for annual FCFPS |
| 1305 | `mean_estimate_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean consensus estimate for annual FCFPS |
| 1306 | `mean_forecast_actual_combined_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean consensus for FCFPS combined with actuals in a single forecast-plus-actual (FA) series (vendor overlay) |
| 1307 | `mean_forecast_actual_combined_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted mean consensus for FCFPS in the FA (forecast-plus-actual) series |
| 1308 | `mean_surprise_value_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise based on mean consensus for FCFPS (Actual minus MeanEst), vendor-provided overlay |
| 1309 | `mean_surprise_value_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted surprise based on mean consensus for FCFPS (Actual minus MeanEst), vendor-provided overlay |
| 1310 | `median_estimate_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of analyst forecast estimates for annual FCFPS |
| 1311 | `median_estimate_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median consensus estimate for annual FCFPS |
| 1312 | `median_forecast_actual_combined_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Median consensus for FCFPS combined with actuals in a single forecast-plus-actual (FA) series (vendor overlay) |
| 1313 | `median_forecast_actual_combined_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median consensus for FCFPS in the FA (forecast-plus-actual) series |
| 1314 | `median_surprise_value_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise based on median consensus for FCFPS (Actual minus MedianEst), vendor-provided overlay |
| 1315 | `median_surprise_value_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted surprise based on median consensus for FCFPS (Actual minus MedianEst), vendor-provided overlay |
| 1316 | `min_estimate_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for annual FCFPS |
| 1317 | `min_estimate_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for FCFPS after currency/split adjustments |
| 1318 | `stddev_estimate_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecast estimates for annual FCFPS |
| 1319 | `stddev_estimate_fxadj_fcfps_annual12` | VECTOR | 0.736 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst FCFPS estimates after currency/split adjustment |
| 1320 | `actual_pretax_reported_value_annual12` | VECTOR | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual reported pre-tax profit for the annual period. |
| 1321 | `actual_pretax_reported_value_fxadj_annual12` | VECTOR | 0.733 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime-adjusted actual reported PRR values vector |
| 1322 | `estimate_count_flash_period_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of flash PRR estimates currently in the consensus window |
| 1323 | `estimate_count_four_weeks_prior_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of PRR estimates (analyst contributions) four weeks ago |
| 1324 | `estimate_count_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Current number of analyst estimates contributing to the PRR consensus |
| 1325 | `estimate_count_three_months_prior_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of PRR estimates (analyst contributions) three months ago |
| 1326 | `max_estimate_four_weeks_prior_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest pre-tax profit (reported) estimate from four weeks ago for the annual period, adjusted for currency effects. |
| 1327 | `max_estimate_four_weeks_prior_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest PRR estimate four weeks ago |
| 1328 | `max_estimate_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted current highest PRR consensus estimate |
| 1329 | `max_estimate_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Current highest PRR consensus estimate |
| 1330 | `max_estimate_three_months_prior_fxadj_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest currency-adjusted pre-tax reported profit estimate from three months ago for the annual period. |
| 1331 | `max_estimate_three_months_prior_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest PRR consensus value from three months ago |
| 1332 | `mean_estimate_four_weeks_prior_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean pre-tax profit (reported) estimate from four weeks ago for the annual period, adjusted for currency effects. |
| 1333 | `mean_estimate_four_weeks_prior_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of PRR consensus estimates four weeks ago |
| 1334 | `mean_estimate_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted current mean PRR consensus |
| 1335 | `mean_estimate_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of the current PRR consensus estimates |
| 1336 | `mean_estimate_three_months_prior_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean pre-tax profit (reported) estimate from three months ago for the annual period, adjusted for currency effects. |
| 1337 | `mean_estimate_three_months_prior_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of PRR consensus estimates three months ago |
| 1338 | `mean_flash_estimate_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of the most recent pre-tax profit (reported) estimates for the annual period, adjusted for currency effects. |
| 1339 | `mean_flash_estimate_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of the flash PRR consensus estimates |
| 1340 | `mean_forecast_actual_combined_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | Mean of combined forecast and actual pre-tax profit (reported) values for the annual period, adjusted for currency effec |
| 1341 | `mean_forecast_actual_combined_pretax_reported_annual12` | VECTOR | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | Mean of combined forecast and actual pre-tax profit (reported) values for the annual period. |
| 1342 | `mean_surprise_value_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Average surprise (actual minus consensus) for pre-tax profit (reported), adjusted for currency effects, for the annual p |
| 1343 | `mean_surprise_value_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of the difference between actual and consensus pre-tax reported profit for the annual period. |
| 1344 | `median_estimate_four_weeks_prior_fxadj_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of currency-adjusted pre-tax reported profit estimates from four weeks ago for the annual period. |
| 1345 | `median_estimate_four_weeks_prior_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of PRR consensus estimates four weeks ago |
| 1346 | `median_estimate_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split-adjusted median of the current consensus estimates for the PRR measure |
| 1347 | `median_estimate_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Current median of PRR consensus estimates |
| 1348 | `median_estimate_three_months_prior_fxadj_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median PRR consensus from three months ago |
| 1349 | `median_estimate_three_months_prior_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Median PRR consensus from three months ago |
| 1350 | `median_forecast_actual_combined_pretax_reported_annual12_2` | VECTOR | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median value combining both forecast and actual pre-tax reported profit for the annual period. |
| 1351 | `median_forecast_actual_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 盈利与财务 | 0 | — | — | — | UNTESTED | Median of combined forecast and actual pre-tax profit (reported) values for the annual period, adjusted for currency eff |
| 1352 | `median_surprise_value_fxadj_pretax_reported_annual12_3` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of the currency-adjusted surprise between actual and consensus pre-tax reported profit for the annual period. |
| 1353 | `median_surprise_value_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Median of the difference between actual and consensus pre-tax reported profit for the annual period. |
| 1354 | `min_estimate_four_weeks_prior_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest pre-tax profit (reported) estimate from four weeks ago for the annual period, adjusted for currency effects. |
| 1355 | `min_estimate_four_weeks_prior_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest PRR consensus value from four weeks ago |
| 1356 | `min_estimate_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted current lowest PRR consensus estimate |
| 1357 | `min_estimate_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Current lowest PRR consensus estimate |
| 1358 | `min_estimate_three_months_prior_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest pre-tax profit (reported) estimate from three months ago for the annual period, adjusted for currency effects. |
| 1359 | `min_estimate_three_months_prior_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest PRR consensus estimate from three months ago |
| 1360 | `stddev_estimate_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Adjusted standard deviation of the current PRR consensus estimates |
| 1361 | `stddev_estimate_pretax_reported_annual12_3` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of the current PRR consensus estimates |
| 1362 | `stddev_flash_estimate_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of the most recent pre-tax profit (reported) estimates for the annual period, adjusted for currency e |
| 1363 | `stddev_flash_estimate_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of flash PRR estimates |
| 1364 | `stddev_four_weeks_prior_fxadj_pretax_reported_annual12_3` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of currency-adjusted pre-tax reported profit estimates from four weeks ago for the annual period. |
| 1365 | `stddev_four_weeks_prior_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of PRR consensus estimates as of four weeks ago |
| 1366 | `stddev_three_months_prior_fxadj_pretax_reported_annual12` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of pre-tax profit (reported) estimates from three months ago for the annual period, adjusted for curr |
| 1367 | `stddev_three_months_prior_pretax_reported_annual12_2` | VECTOR | 0.733 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of PRR consensus estimates from three months ago |
| 1368 | `actual_ebt_value_annual12` | VECTOR | 0.732 | 其他 | 0 | — | — | — | UNTESTED | Actual reported EBT value (regime-aware) |
| 1369 | `actual_ebt_value_fxadj_annual12` | VECTOR | 0.732 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime- and currency-adjusted actual reported annual EBT |
| 1370 | `estimate_count_current_period_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Current number of analyst EBT estimates contributing to the consensus |
| 1371 | `estimate_count_flash_period_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of flash analyst estimates for annual Earnings Before Taxes (EBT) |
| 1372 | `estimate_count_four_weeks_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst EBT estimates four weeks ago |
| 1373 | `estimate_count_three_months_prior_ebt_annual12_2` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst EBT estimates three months ago |
| 1374 | `max_estimate_current_period_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest current EBT consensus estimate |
| 1375 | `max_estimate_four_weeks_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest EBT consensus estimate four weeks ago |
| 1376 | `max_estimate_four_weeks_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted highest EBT consensus estimate four weeks ago |
| 1377 | `max_estimate_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted highest current EBT consensus estimate |
| 1378 | `max_estimate_three_months_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest EBT consensus estimate three months ago |
| 1379 | `max_estimate_three_months_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted highest EBT consensus estimate three months ago |
| 1380 | `mean_estimate_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of current EBT consensus estimates |
| 1381 | `mean_estimate_four_weeks_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst EBT consensus as of four weeks ago |
| 1382 | `mean_estimate_four_weeks_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted mean EBT consensus estimate four weeks ago |
| 1383 | `mean_estimate_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted mean EBT consensus estimate |
| 1384 | `mean_estimate_three_months_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst EBT consensus as of three months ago |
| 1385 | `mean_estimate_three_months_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted mean EBT consensus estimate three months ago |
| 1386 | `mean_flash_estimate_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean of EBT flash consensus estimates |
| 1387 | `mean_flash_estimate_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted mean of EBT flash consensus estimates |
| 1388 | `mean_forecast_actual_combined_ebt_annual12` | VECTOR | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average value combining both forecast and actual pre-tax profit for the annual period. |
| 1389 | `mean_forecast_actual_combined_fxadj_ebt_annual12` | VECTOR | 0.732 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime-adjusted mean of the forecast-plus-actual overlay for EBT |
| 1390 | `mean_surprise_value_ebt_annual12_2` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean earnings surprise for EBT (actual minus consensus estimate) |
| 1391 | `mean_surprise_value_fxadj_ebt_annual12_2` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Average surprise (actual minus consensus) for pre-tax profit, adjusted for currency effects, for the annual period. |
| 1392 | `median_estimate_current_period_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Current median of analyst consensus annual EBT estimates |
| 1393 | `median_estimate_four_weeks_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Median EBT consensus estimate four weeks ago |
| 1394 | `median_estimate_four_weeks_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median EBT consensus estimate four weeks ago |
| 1395 | `median_estimate_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Median pre-tax profit estimate for the annual period, adjusted for currency effects. |
| 1396 | `median_estimate_three_months_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst consensus for Earnings Before Taxes (EBT) as of three months ago (historical snapshot) |
| 1397 | `median_estimate_three_months_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median EBT consensus estimate three months ago |
| 1398 | `median_forecast_actual_ebt_annual12` | VECTOR | 0.732 | 其他 | 0 | — | — | — | UNTESTED | Median of the forecast-plus-actual overlay for EBT |
| 1399 | `median_forecast_actual_fxadj_ebt_annual12` | VECTOR | 0.732 | 宏观与行业 | 0 | — | — | — | UNTESTED | Regime-adjusted median of the forecast-plus-actual overlay for EBT |
| 1400 | `median_surprise_value_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Median earnings surprise for EBT (actual minus consensus estimate) |
| 1401 | `median_surprise_value_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted median earnings surprise for EBT (actual minus consensus estimate) |
| 1402 | `min_estimate_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest current EBT consensus estimate |
| 1403 | `min_estimate_four_weeks_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest Earnings Before Taxes (EBT) consensus estimate four weeks ago |
| 1404 | `min_estimate_four_weeks_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest pre-tax profit estimate from four weeks ago for the annual period, adjusted for currency effects. |
| 1405 | `min_estimate_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest current analyst consensus annual EBT estimate, adjusted for currency, splits, and regime effects |
| 1406 | `min_estimate_three_months_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest EBT consensus estimate three months ago |
| 1407 | `min_estimate_three_months_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Regime-adjusted lowest EBT consensus estimate three months ago |
| 1408 | `stddev_estimate_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of current EBT consensus estimates |
| 1409 | `stddev_estimate_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of pre-tax profit estimates for the annual period, adjusted for currency effects. |
| 1410 | `stddev_flash_estimate_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of EBT flash consensus estimates |
| 1411 | `stddev_flash_estimate_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of the most recent short-term pre-tax profit estimates for the annual period, adjusted for currency e |
| 1412 | `stddev_four_weeks_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of EBT consensus estimates four weeks ago |
| 1413 | `stddev_four_weeks_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of pre-tax profit estimates from four weeks ago for the annual period, adjusted for currency effects. |
| 1414 | `stddev_three_months_prior_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst consensus annual EBT estimates as of three months ago |
| 1415 | `stddev_three_months_prior_fxadj_ebt_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of pre-tax profit estimates from three months ago, adjusted for currency effects. |
| 1416 | `actual_cashflowfinancing_value_annual12` | VECTOR | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported actual annual Cash Flow from Financing (CFFINANCE) |
| 1417 | `actual_cashflowfinancing_value_fxadj_annual12` | VECTOR | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual annual Cash Flow from Financing adjusted for currency/splits/regime |
| 1418 | `currency_code_cashflowfinancing_annual12` | VECTOR | 0.732 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Integer code for the reporting currency associated with the values (decode via currency table) |
| 1419 | `estimate_count_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates used to form the consensus for Cash Flow from Financing |
| 1420 | `forecast_actual_flag_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag for Forecast-plus-Actual status/provenance (e.g., 0 backfilled, 1 consensus forecast, 2 actual report) |
| 1421 | `forecast_actual_indicator_cashflowfinancing_annual12` | VECTOR | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for cash flow from financing activities in the annual per |
| 1422 | `max_estimate_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate (forecast only) for annual Cash Flow from Financing, unadjusted |
| 1423 | `max_estimate_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst estimate for annual Cash Flow from Financing |
| 1424 | `mean_estimate_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean (consensus) of analyst estimates for the fiscal period |
| 1425 | `mean_estimate_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted mean analyst estimate for annual Cash Flow from Financing |
| 1426 | `mean_forecast_actual_combined_cashflowfinancing_annual12` | VECTOR | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecast-plus-Actual overlay using the mean for annual Cash Flow from Financing (regime-aware) |
| 1427 | `mean_forecast_actual_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast-plus-Actual mean for annual Cash Flow from Financing |
| 1428 | `mean_surprise_cashflowfinancing_annual12_tribes` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise versus consensus mean for Cash Flow from Financing (Actual minus mean estimate), regime-aware |
| 1429 | `mean_surprise_value_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus consensus mean for Cash Flow from Financing (Actual minus mean estimate) |
| 1430 | `median_estimate_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate (forecast) for annual Cash Flow from Financing, unadjusted |
| 1431 | `median_estimate_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted median analyst estimate for annual Cash Flow from Financing |
| 1432 | `median_forecast_actual_combined_cashflowfinancing_annual12` | VECTOR | 0.732 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Regime-aware overlay combining median forecast with subsequent actuals for CFFINANCE |
| 1433 | `median_forecast_actual_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Currency-adjusted Forecast-plus-Actual median for annual Cash Flow from Financing |
| 1434 | `median_surprise_value_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise = Actual minus median estimate for CFFINANCE (unadjusted) |
| 1435 | `median_surprise_value_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted surprise versus consensus median for Cash Flow from Financing |
| 1436 | `min_estimate_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate (forecast only) for annual Cash Flow from Financing, unadjusted |
| 1437 | `min_estimate_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst estimate for annual Cash Flow from Financing |
| 1438 | `stddev_estimate_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual Cash Flow from Financing |
| 1439 | `stddev_estimate_fxadj_cashflowfinancing_annual12` | VECTOR | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted standard deviation of analyst estimates for annual Cash Flow from Financing |
| 1440 | `actual_roe_value_annual12_tribes` | VECTOR | 0.731 | 其他 | 0 | — | — | — | UNTESTED | Reported actual annual ROA value for the period |
| 1441 | `estimate_count_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the ROA consensus |
| 1442 | `forecast_actual_flag_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecast/Actual provenance or quality flag (0 backfilled, 1 forecast consensus, 2 actual) |
| 1443 | `forecast_actual_indicator_roe_annual12_tribes` | VECTOR | 0.731 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator showing whether the value is a forecast or an actual for annual return on assets. |
| 1444 | `max_estimate_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst forecast estimate for annual ROA within the window |
| 1445 | `mean_estimate_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean analyst estimate for annual ROA |
| 1446 | `mean_forecast_actual_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Mean analyst estimate combined with subsequent actuals for annual ROA (Forecast+Actual FA overlay) |
| 1447 | `mean_surprise_value_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise relative to the mean consensus (actual ROA minus mean estimate), regime-aware |
| 1448 | `median_estimate_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median analyst estimate for annual ROA |
| 1449 | `median_forecast_actual_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Median analyst estimate combined with subsequent actuals for annual ROA (Forecast+Actual FA overlay) |
| 1450 | `median_surprise_value_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise metric for ROA: actual reported ROA minus the consensus median estimate (regime-aware) |
| 1451 | `min_estimate_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst forecast estimate for annual ROA within the window |
| 1452 | `stddev_estimate_roe_annual12_tribes` | VECTOR | 0.731 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst ROA estimates (consensus dispersion) |
| 1453 | `actual_cogs_value_annual12_tribes` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Actual reported annual Cost of Goods Sold |
| 1454 | `actual_cogs_value_fxadj_annual12_tribes` | VECTOR | 0.713 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency/split adjusted actual annual COGS value |
| 1455 | `estimate_count_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates contributing to the annual COGS consensus |
| 1456 | `estimate_currency_code_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Integer code identifying the reporting currency for the COGS measure |
| 1457 | `forecast_actual_flag_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating provenance/status of Forecast+Actual data points (e.g., 0 backfilled, 1 consensus forecast, 2 actual) |
| 1458 | `forecast_actual_indicator_cogs_annual12_tribes` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Period indicator marking forecast vs actual windows (M..1 forecast, 0 and negatives actual/back history) |
| 1459 | `max_estimate_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Highest analyst estimate for annual Cost of Goods Sold |
| 1460 | `max_estimate_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted highest analyst forecast estimate for annual COGS |
| 1461 | `mean_estimate_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean of analyst annual COGS estimates |
| 1462 | `mean_estimate_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted consensus mean of analyst annual COGS estimates |
| 1463 | `mean_forecast_actual_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus mean estimate for annual COGS combined with subsequent actuals (Forecast + Actual overlay) |
| 1464 | `mean_forecast_actual_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted consensus mean estimate for annual COGS combined with subsequent actuals (Forecast + Actu |
| 1465 | `mean_surprise_value_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Surprise for COGS based on the mean analyst consensus (actual minus mean estimate) |
| 1466 | `mean_surprise_value_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted surprise for COGS based on the mean analyst consensus (actual minus mean estimate) |
| 1467 | `median_estimate_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median of analyst annual COGS estimates |
| 1468 | `median_estimate_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted median analyst estimate for annual COGS |
| 1469 | `median_forecast_actual_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Consensus median estimate for annual COGS combined with subsequent actuals (Forecast + Actual overlay) |
| 1470 | `median_forecast_actual_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split/regime-adjusted consensus median estimate for annual COGS combined with actuals (Forecast + Actual overla |
| 1471 | `median_surprise_value_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Difference between actual reported COGS and the median analyst consensus estimate (surprise) |
| 1472 | `median_surprise_value_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency/split adjusted surprise for COGS based on the median analyst consensus |
| 1473 | `min_estimate_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Lowest analyst estimate for annual Cost of Goods Sold |
| 1474 | `min_estimate_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Currency-adjusted lowest analyst forecast estimate for annual COGS |
| 1475 | `stddev_estimate_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst estimates for annual Cost of Goods Sold |
| 1476 | `stddev_estimate_fxadj_cogs_annual12_tribes` | VECTOR | 0.713 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of analyst forecasts for annual cost of goods sold, adjusted for currency. |
| 1477 | `actual_revenue_value_fxadj_quarterly16` | VECTOR | 0.562 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency-adjusted actual reported quarterly revenue |
| 1478 | `actual_revenue_value_quarterly16` | VECTOR | 0.562 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reported quarterly revenue actuals (NaN during forecast periods) |
| 1479 | `estimate_count_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates used to compute the consensus for quarterly revenue |
| 1480 | `forecast_actual_flag_revenue_quarterly16` | VECTOR | 0.562 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Indicator showing if the value is a forecast, actual, or combined for revenue in the quarter. |
| 1481 | `forecast_actual_indicator_revenue_quarterly16` | VECTOR | 0.562 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Event indicator for forecast/actual regime (M..1 = forecast periods; 0, -1, -2 = actual or post-actual periods) |
| 1482 | `max_estimate_fxadj_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted highest analysts’ quarterly revenue estimate |
| 1483 | `max_estimate_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate for quarterly revenue (forecast only) |
| 1484 | `mean_estimate_fxadj_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted consensus mean quarterly revenue estimate |
| 1485 | `mean_estimate_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean (consensus) analyst estimate for quarterly revenue |
| 1486 | `mean_forecast_actual_combined_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regime-aware overlay combining consensus mean quarterly revenue forecasts with subsequent actuals |
| 1487 | `mean_forecast_actual_fxadj_revenue_quarterly16_tribes` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency and split adjusted Forecast plus Actual composite of the mean revenue value (consensus in forecast periods, act |
| 1488 | `mean_surprise_value_fxadj_revenue_quarterly16_tribes` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise: actual quarterly revenue minus consensus mean estimate |
| 1489 | `mean_surprise_value_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise versus the mean quarterly revenue estimate (actual minus mean estimate) |
| 1490 | `median_estimate_fxadj_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted median of analysts’ quarterly revenue estimates |
| 1491 | `median_estimate_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median consensus estimate for quarterly revenue |
| 1492 | `median_forecast_actual_combined_fxadj_revenue_quarterly16` | VECTOR | 0.562 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency and split adjusted Forecast plus Actual composite of the median revenue value |
| 1493 | `median_forecast_actual_revenue_quarterly16_tribes` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate combined with subsequent actuals for quarterly revenue (Forecast+Actual) |
| 1494 | `median_surprise_value_fxadj_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency adjusted vendor surprise overlay for revenue, computed as actual minus median consensus at time of report |
| 1495 | `median_surprise_value_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise using the median estimate: actual quarterly revenue minus consensus median |
| 1496 | `min_estimate_fxadj_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted lowest analysts’ quarterly revenue estimate |
| 1497 | `min_estimate_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analysts’ quarterly revenue estimate |
| 1498 | `stddev_estimate_fxadj_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted standard deviation of analysts’ quarterly revenue estimates |
| 1499 | `stddev_estimate_revenue_quarterly16` | VECTOR | 0.562 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst revenue estimates (unadjusted) |
| 1500 | `actual_ebit_value_fxadj_quarterly16_tribes` | VECTOR | 0.477 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency-adjusted actual reported quarterly EBIT value |
| 1501 | `actual_value_ebit_quarterly16` | VECTOR | 0.477 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual reported value for quarterly EBIT |
| 1502 | `currency_type_ebit_quarterly16` | VECTOR | 0.477 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Integer currency code for the measure’s units, mapped via a decode table by report date |
| 1503 | `estimate_count_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst EBIT estimates used to compute consensus |
| 1504 | `max_estimate_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst forecast estimate for quarterly EBIT |
| 1505 | `max_estimate_fxadj_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime adjusted highest analyst EBIT estimate |
| 1506 | `mean_estimate_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst EBIT estimate (consensus) |
| 1507 | `mean_estimate_fxadj_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime adjusted mean analyst EBIT estimate |
| 1508 | `mean_forecast_actual_combined_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean EBIT estimate combined with actuals (Forecast+Actual overlay) |
| 1509 | `mean_forecast_actual_combined_fxadj_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted mean consensus estimate combined with actuals (FA overlay) for quarterly EBIT |
| 1510 | `mean_surprise_value_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise overlay: actual reported quarterly EBIT minus the mean analyst consensus estimate |
| 1511 | `mean_surprise_value_fxadj_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise relative to the consensus mean estimate for quarterly EBIT (Actual minus MeanEst), regime-awa |
| 1512 | `median_estimate_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst EBIT estimates (consensus) |
| 1513 | `median_estimate_fxadj_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime adjusted median analyst EBIT estimate |
| 1514 | `median_forecast_actual_combined_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median EBIT estimate combined with actuals (FA overlay) |
| 1515 | `median_forecast_actual_combined_fxadj_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted median consensus estimate combined with actuals for quarterly EBIT |
| 1516 | `median_surprise_value_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise overlay: actual reported quarterly EBIT minus the median analyst consensus estimate |
| 1517 | `median_surprise_value_fxadj_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise relative to the median estimate for quarterly EBIT (Actual minus MedianEst) |
| 1518 | `min_estimate_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst forecast estimate for quarterly EBIT |
| 1519 | `min_estimate_fxadj_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime adjusted lowest analyst EBIT estimate |
| 1520 | `stddev_estimate_ebit_quarterly16_tribes` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst EBIT estimates |
| 1521 | `stddev_estimate_fxadj_ebit_quarterly16` | VECTOR | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted standard deviation of analyst estimates for quarterly EBIT |
| 1522 | `actual_value_eps_quarterly16_tribes` | VECTOR | 0.476 | 其他 | 0 | — | — | — | UNUSABLE | Actual reported quarterly EPS (unadjusted) |
| 1523 | `actual_value_fxadj_eps_quarterly16_tribes` | VECTOR | 0.476 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted actual reported quarterly EPS |
| 1524 | `estimate_count_current_period_eps_quarterly16` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates used to compute the consensus |
| 1525 | `max_estimate_current_period_eps_quarterly16` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst quarterly EPS estimate (forecast only) |
| 1526 | `max_estimate_fxadj_eps_quarterly16_tribes` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted highest analyst quarterly EPS estimate |
| 1527 | `mean_estimate_eps_quarterly16_tribes` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of analyst quarterly EPS estimates (consensus) |
| 1528 | `mean_estimate_fxadj_eps_quarterly16_tribes` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted mean of analyst quarterly EPS estimates |
| 1529 | `mean_forecast_actual_combined_eps_quarterly16_tribes` | VECTOR | 0.476 | 其他 | 0 | — | — | — | UNUSABLE | Forecast-plus-Actual overlay for the mean quarterly EPS (combines forecasts with actuals) |
| 1530 | `mean_forecast_actual_fxadj_eps_quarterly16` | VECTOR | 0.476 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Currency-adjusted forecast-plus-actual overlay for the mean quarterly EPS |
| 1531 | `mean_surprise_value_eps_quarterly16_2` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise versus the mean consensus estimate for quarterly EPS (actual minus mean estimate) |
| 1532 | `mean_surprise_value_fxadj_eps_quarterly16_2` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise versus the mean quarterly EPS consensus (Actual_adj minus MeanEst_adj) |
| 1533 | `median_estimate_eps_quarterly16_tribes` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst quarterly EPS estimates (consensus forecast) |
| 1534 | `median_estimate_fxadj_eps_quarterly16_tribes` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted median of analyst quarterly EPS estimates |
| 1535 | `median_forecast_actual_combined_eps_quarterly16` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast-plus-Actual overlay for the median quarterly EPS (combines consensus forecasts with subsequent actuals) |
| 1536 | `median_forecast_actual_combined_fxadj_eps_quarterly16` | VECTOR | 0.476 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Currency-adjusted forecast-plus-actual overlay for the median quarterly EPS |
| 1537 | `median_surprise_value_eps_quarterly16_2` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise versus the median quarterly EPS consensus (Actual minus MedianEst), regime-aware and embargo-compliant |
| 1538 | `median_surprise_value_fxadj_eps_quarterly16_tribes` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise versus the median quarterly EPS consensus (Actual_adj minus MedianEst_adj) |
| 1539 | `min_estimate_current_period_eps_quarterly16` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst quarterly EPS estimate (forecast only) |
| 1540 | `min_estimate_fxadj_eps_quarterly16_tribes` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted lowest analyst quarterly EPS estimate |
| 1541 | `stddev_estimate_eps_quarterly16_tribes` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst quarterly EPS estimates |
| 1542 | `stddev_fxadj_eps_quarterly16` | VECTOR | 0.476 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted standard deviation of analyst quarterly EPS estimates |
| 1543 | `actual_netprofit_value_fxadj_quarterly16` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual reported quarterly net profit adjusted for currency, splits, and regime effects |
| 1544 | `actual_netprofit_value_quarterly16` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual reported quarterly net profit |
| 1545 | `currency_code_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Integer currency code indicating the reporting/estimate currency for the net profit values |
| 1546 | `estimate_count_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates included in the consensus for quarterly net profit |
| 1547 | `forecast_actual_flag_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Flag indicating provenance/status of Forecast+Actual data (e.g., 0 backfilled, 1 consensus forecast, 2 actual) |
| 1548 | `forecast_actual_indicator_netprofit_quarterly16` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Indicator showing whether the value is a forecast or an actual for net profit in the quarterly period. |
| 1549 | `max_estimate_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest estimate adjusted for currency, splits, and regime effects |
| 1550 | `max_estimate_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest individual analyst estimate for quarterly net profit (forecast only) |
| 1551 | `mean_estimate_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate adjusted for currency, splits, and regime effects |
| 1552 | `mean_estimate_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus mean analyst estimate for quarterly net profit |
| 1553 | `mean_forecast_actual_combined_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted Forecast+Actual mean series for quarterly net profit |
| 1554 | `mean_forecast_actual_combined_netprofit_quarterly16` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Forecast+Actual mean series for quarterly net profit |
| 1555 | `mean_surprise_value_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise relative to the mean estimate (actual minus mean) |
| 1556 | `mean_surprise_value_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise metric: actual reported net profit minus mean estimate |
| 1557 | `median_estimate_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate adjusted for currency, splits, and regime effects |
| 1558 | `median_estimate_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus median analyst estimate for quarterly net profit |
| 1559 | `median_forecast_actual_combined_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted Forecast+Actual median series for quarterly net profit |
| 1560 | `median_forecast_actual_combined_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast+Actual overlay using the median consensus for quarterly net profit |
| 1561 | `median_surprise_value_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise relative to the median estimate (actual minus median) |
| 1562 | `median_surprise_value_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise metric: actual minus median estimate for quarterly net profit |
| 1563 | `min_estimate_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest estimate adjusted for currency, splits, and regime effects |
| 1564 | `min_estimate_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest individual analyst estimate for quarterly net profit (forecast only) |
| 1565 | `stddev_estimate_fxadj_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates adjusted for currency/regime |
| 1566 | `stddev_estimate_netprofit_quarterly16` | VECTOR | 0.467 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for quarterly net profit |
| 1567 | `actual_netprofit_reported_value_fxadj_quarterly16` | VECTOR | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted reported actual value for quarterly Net Profit (Reported) |
| 1568 | `actual_netprofit_reported_value_quarterly16` | VECTOR | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reported actual net profit for the period |
| 1569 | `estimate_count_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates used to compute the consensus for reported net profit |
| 1570 | `forecast_actual_flag_netprofit_reported_quarterly16` | VECTOR | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Indicator showing if the value is a forecast, actual, or combined for reported net profit in the quarter. |
| 1571 | `forecast_actual_indicator_netprofit_reported_quarterly16` | VECTOR | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Forecast/actual period indicator where positive values (M..1) denote forecast periods and 0, -1, -2 denote actual or pos |
| 1572 | `max_estimate_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted highest analyst estimate for reported net profit |
| 1573 | `max_estimate_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate for reported net profit (unadjusted) |
| 1574 | `mean_estimate_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted mean (consensus) analyst estimate of reported net profit |
| 1575 | `mean_estimate_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean (consensus) of analyst estimates for quarterly Net Profit (Reported) |
| 1576 | `mean_forecast_actual_combined_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted version of the combined mean forecast plus actual series for quarterly Net Profit (Report |
| 1577 | `mean_forecast_actual_combined_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regime-aware series combining mean consensus forecasts with subsequent actuals for quarterly Net Profit (Reported) |
| 1578 | `mean_surprise_value_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise based on mean consensus (Actual minus mean estimate), vendor overlay |
| 1579 | `mean_surprise_value_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise versus the mean consensus for quarterly Net Profit (Reported), calculated as Actual minus mean estimate |
| 1580 | `median_estimate_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted median analyst estimate of reported net profit |
| 1581 | `median_estimate_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst estimates for quarterly Net Profit (Reported) |
| 1582 | `median_forecast_actual_combined_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted overlay combining median forecast estimates with subsequent actuals |
| 1583 | `median_forecast_actual_combined_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regime-aware series combining median consensus forecasts with subsequent actuals for quarterly Net Profit (Reported) |
| 1584 | `median_surprise_value_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise based on median consensus (Actual minus median estimate), vendor overlay |
| 1585 | `median_surprise_value_netprofit_reported_quarterly16` | VECTOR | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median surprise value (actual minus forecast) for reported net profit in the quarter. |
| 1586 | `min_estimate_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted lowest analyst estimate for reported net profit |
| 1587 | `min_estimate_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate for reported net profit (unadjusted) |
| 1588 | `stddev_estimate_fxadj_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted standard deviation of analyst estimates for reported net profit |
| 1589 | `stddev_estimate_netprofit_reported_quarterly16` | VECTOR | 0.431 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for reported net profit (unadjusted) |
| 1590 | `actual_pretax_value_fxadj_quarterly16_tribes` | VECTOR | 0.430 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Regime and currency adjusted actual reported quarterly PPROFIT |
| 1591 | `actual_pretax_value_quarterly16_tribes` | VECTOR | 0.430 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual reported value for the PPROFIT quarterly metric |
| 1592 | `estimate_count_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of contributing analyst estimates used to compute the pre-tax profit consensus for the period |
| 1593 | `estimate_currency_code_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Integer currency code referencing the reporting currency for the PPROFIT measure |
| 1594 | `forecast_actual_flag_pretax_quarterly16_tribes` | VECTOR | 0.430 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Flag indicating whether the value is a forecast, actual, or combined for pre-tax profit in the quarter. |
| 1595 | `forecast_actual_indicator_pretax_quarterly16_tribes` | VECTOR | 0.430 | 其他 | 0 | — | — | — | UNUSABLE | Indicator of period type within the series: positive M..1 for forecast periods, 0 and negatives for actual/outdated peri |
| 1596 | `max_estimate_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted highest analyst forecast estimate for the PPROFIT quarterly metric |
| 1597 | `max_estimate_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst forecast estimate for the PPROFIT quarterly metric |
| 1598 | `mean_estimate_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted consensus mean analyst estimate for quarterly pre-tax profit over the p16 rolling window |
| 1599 | `mean_estimate_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst consensus estimate for the PPROFIT quarterly metric |
| 1600 | `mean_forecast_actual_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted forecast plus actual overlay of the mean estimate for the PPROFIT quarterly metric |
| 1601 | `mean_forecast_actual_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast plus actual overlay of the mean estimate for the PPROFIT quarterly metric |
| 1602 | `mean_surprise_value_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise for the PPROFIT quarterly metric, computed as Actual minus the mean consensus estimate |
| 1603 | `mean_surprise_value_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise for the PPROFIT quarterly metric, computed as Actual minus the mean consensus estimate |
| 1604 | `median_estimate_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted median analyst estimate for quarterly pre-tax profit |
| 1605 | `median_estimate_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst consensus estimate for the PPROFIT quarterly metric |
| 1606 | `median_forecast_actual_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted forecast plus actual overlay of the median estimate for the PPROFIT quarterly metric |
| 1607 | `median_forecast_actual_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast plus actual overlay of the median estimate for the PPROFIT quarterly metric |
| 1608 | `median_surprise_value_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise for the PPROFIT quarterly metric, computed as Actual minus the median consensus estimate |
| 1609 | `median_surprise_value_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise for the PPROFIT quarterly metric, computed as Actual minus the median consensus estimate |
| 1610 | `min_estimate_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted lowest analyst forecast estimate for the PPROFIT quarterly metric |
| 1611 | `min_estimate_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst forecast estimate for the PPROFIT quarterly metric |
| 1612 | `stddev_estimate_fxadj_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted standard deviation of analyst estimates for the PPROFIT quarterly metric |
| 1613 | `stddev_estimate_pretax_quarterly16_tribes` | VECTOR | 0.430 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for the PPROFIT quarterly metric |
| 1614 | `actual_ebitda_value_fxadj_quarterly16` | VECTOR | 0.420 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted actual reported EBITDA values for each period |
| 1615 | `actual_ebitda_value_quarterly16` | VECTOR | 0.420 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual reported quarterly EBITDA |
| 1616 | `estimate_count_current_period_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates used to compute the consensus for the quarterly EBITDA measure |
| 1617 | `estimate_currency_code_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency code in which the EBITDA estimate or actual is reported for the quarterly period. |
| 1618 | `forecast_actual_flag_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast/Actual flag indicating data provenance/status (0 backfilled, 1 consensus forecast, 2 actual) |
| 1619 | `forecast_actual_indicator_ebitda_quarterly16` | VECTOR | 0.420 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Forecast/Actual phase indicator for each point (positive values = forecast periods; 0 or negative = actual/outdated) |
| 1620 | `max_estimate_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst EBITDA estimate for the forecast period |
| 1621 | `max_estimate_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted highest analyst quarterly EBITDA estimate |
| 1622 | `mean_estimate_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean (consensus) analyst quarterly EBITDA estimate |
| 1623 | `mean_estimate_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted mean consensus quarterly EBITDA estimate (currency/splits/regime adjusted) |
| 1624 | `mean_forecast_actual_combined_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast+Actual composite: mean (consensus) EBITDA where forecasts are replaced by actuals once reported |
| 1625 | `mean_forecast_actual_combined_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted version of the Forecast+Actual mean EBITDA |
| 1626 | `mean_surprise_value_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate surprise for EBITDA (actual minus mean consensus) |
| 1627 | `mean_surprise_value_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise versus mean consensus (Actual − Mean estimate) |
| 1628 | `median_estimate_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst quarterly EBITDA estimates |
| 1629 | `median_estimate_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted median consensus quarterly EBITDA estimate (currency/splits/regime adjusted) |
| 1630 | `median_forecast_actual_combined_ebitda_quarterly16` | VECTOR | 0.420 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Forecast+Actual composite: median EBITDA where forecasts are replaced by actuals once reported |
| 1631 | `median_forecast_actual_combined_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted version of the Forecast+Actual median EBITDA |
| 1632 | `median_surprise_value_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise versus median consensus (Actual − Median estimate) at report time |
| 1633 | `median_surprise_value_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise versus median consensus (Actual − Median estimate) at report time |
| 1634 | `min_estimate_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst EBITDA estimate for the forecast period |
| 1635 | `min_estimate_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted lowest analyst quarterly EBITDA estimate |
| 1636 | `stddev_estimate_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst EBITDA estimates for the period |
| 1637 | `stddev_estimate_fxadj_ebitda_quarterly16` | VECTOR | 0.420 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted standard deviation of analyst EBITDA estimates |
| 1638 | `actual_eps_reported_value_fxadj_quarterly16` | VECTOR | 0.399 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Reported actual EPS value adjusted for currency/splits/regime |
| 1639 | `actual_eps_reported_value_quarterly16` | VECTOR | 0.399 | 其他 | 0 | — | — | — | UNUSABLE | Reported actual EPS value |
| 1640 | `estimate_count_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates used to compute the consensus |
| 1641 | `forecast_actual_flag_eps_reported_quarterly16` | VECTOR | 0.399 | 其他 | 0 | — | — | — | UNUSABLE | Indicator showing if the value is a forecast, actual, or combined for reported EPS in the quarter. |
| 1642 | `forecast_actual_indicator_eps_reported_quarterly16` | VECTOR | 0.399 | 其他 | 0 | — | — | — | UNUSABLE | Event indicator for period type where positive values denote forecast periods and 0 or negative values denote actual-rep |
| 1643 | `max_estimate_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst EPSREP estimate |
| 1644 | `max_estimate_fxadj_eps_reported_quarterly16` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst EPSREP estimate adjusted for currency/splits/regime |
| 1645 | `mean_estimate_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean (consensus) analyst estimate for quarterly reported EPS |
| 1646 | `mean_estimate_fxadj_eps_reported_quarterly16` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst EPSREP estimate adjusted for currency/splits/regime |
| 1647 | `mean_forecast_actual_combined_eps_reported_quarterly16` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast-plus-actual overlay for the mean EPSREP estimate |
| 1648 | `mean_forecast_actual_combined_fxadj_eps_reported_quarterly16` | VECTOR | 0.399 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Currency-adjusted forecast-plus-actual mean EPSREP overlay |
| 1649 | `mean_surprise_value_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise relative to the mean EPSREP estimate (Actual minus mean estimate) |
| 1650 | `mean_surprise_value_fxadj_eps_reported_quarterly16` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise of the mean EPSREP estimate (Actual minus mean estimate) |
| 1651 | `median_estimate_eps_reported_quarterly16` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst EPSREP estimates |
| 1652 | `median_estimate_fxadj_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst EPSREP estimate adjusted for currency/splits/regime |
| 1653 | `median_forecast_actual_combined_eps_reported_quarterly16` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast-plus-actual overlay for the median EPSREP estimate |
| 1654 | `median_forecast_actual_combined_fxadj_eps_reported_quarterly16` | VECTOR | 0.399 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Currency-adjusted forecast-plus-actual median EPSREP overlay |
| 1655 | `median_surprise_value_eps_reported_quarterly16` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise relative to the median EPSREP estimate (Actual minus median estimate) |
| 1656 | `median_surprise_value_fxadj_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted surprise of the median EPSREP estimate (Actual minus median estimate) |
| 1657 | `min_estimate_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst EPSREP estimate |
| 1658 | `min_estimate_fxadj_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate for EPSREP, adjusted for currency/splits/regime |
| 1659 | `stddev_estimate_fullyreported_quarterly16_tribes` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for quarterly reported EPS |
| 1660 | `stddev_estimate_fxadj_eps_reported_quarterly16` | VECTOR | 0.399 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted standard deviation of analyst EPSREP estimates |
| 1661 | `actual_tax_provision_value_quarterly16` | VECTOR | 0.389 | 其他 | 0 | — | — | — | UNUSABLE | Actual reported quarterly tax provision values as reported (unadjusted) |
| 1662 | `actual_value_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted actual tax provision value |
| 1663 | `estimate_count_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of contributing analyst estimates used to compute the consensus for the period |
| 1664 | `forecast_actual_flag_tax_provision_quarterly16` | VECTOR | 0.389 | 其他 | 0 | — | — | — | UNUSABLE | Indicator showing whether the value is a forecast or an actual for quarterly tax provision. |
| 1665 | `forecast_actual_indicator_tax_provision_quarterly16` | VECTOR | 0.389 | 其他 | 0 | — | — | — | UNUSABLE | Indicator showing whether the value is a forecast or an actual for tax provision in the current quarter. |
| 1666 | `max_estimate_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted highest analyst estimate for tax provision |
| 1667 | `max_estimate_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate (forecast only) for quarterly tax provision for the period |
| 1668 | `mean_estimate_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted mean analyst estimate for tax provision |
| 1669 | `mean_estimate_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean (arithmetic average) of analyst consensus estimates for quarterly tax provision for each period, unadjusted |
| 1670 | `mean_forecast_actual_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted mean estimate combined with actuals |
| 1671 | `mean_forecast_actual_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate combined with actuals (Forecast plus Actual) for tax provision |
| 1672 | `mean_surprise_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted surprise using mean estimate (Actual minus mean estimate) |
| 1673 | `mean_surprise_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate surprise, typically Actual minus mean estimate |
| 1674 | `median_estimate_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted median analyst estimate |
| 1675 | `median_estimate_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst consensus estimates for quarterly tax provision (income tax expense) for each period, unadjusted |
| 1676 | `median_forecast_actual_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted median estimate combined with actuals |
| 1677 | `median_forecast_actual_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate combined with actuals (Forecast plus Actual) for tax provision |
| 1678 | `median_surprise_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted surprise using median estimate (Actual minus median estimate) |
| 1679 | `median_surprise_value_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate surprise, typically Actual minus median estimate |
| 1680 | `min_estimate_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted lowest analyst estimate for tax provision |
| 1681 | `min_estimate_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate (forecast only) for quarterly tax provision for the period |
| 1682 | `stddev_estimate_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for quarterly tax provision (forecast only) |
| 1683 | `stddev_fxadj_tax_provision_quarterly16` | VECTOR | 0.389 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted standard deviation of analyst estimates |
| 1684 | `actual_pretax_reported_value_fxadj_quarterly16` | VECTOR | 0.378 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted actual value for the PPROFITREP measure |
| 1685 | `actual_pretax_reported_value_quarterly16` | VECTOR | 0.378 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual reported value for PPROFITREP |
| 1686 | `estimate_count_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the consensus for PPROFITREP |
| 1687 | `forecast_actual_flag_pretax_reported_quarterly16` | VECTOR | 0.378 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Flag indicating whether the pre-tax profit (reported) value is a forecast, actual, or combined for the quarterly period. |
| 1688 | `forecast_actual_indicator_pretax_reported_quarterly16` | VECTOR | 0.378 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Indicator showing whether the value is a forecast or an actual for pre-tax profit (reported) in the quarterly period. |
| 1689 | `max_estimate_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted highest analyst estimate for the PPROFITREP metric |
| 1690 | `max_estimate_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest individual analyst estimate for PPROFITREP |
| 1691 | `mean_estimate_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted mean analyst estimate for the PPROFITREP metric |
| 1692 | `mean_estimate_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean (consensus) analyst estimate for the PPROFITREP metric |
| 1693 | `mean_forecast_actual_combined_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted mean estimate combined with actuals (FA overlay) for the PPROFITREP metric |
| 1694 | `mean_forecast_actual_combined_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate combined with actuals (FA overlay) for the PPROFITREP metric |
| 1695 | `mean_surprise_value_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted surprise based on the mean estimate (actual − mean estimate) for PPROFITREP |
| 1696 | `mean_surprise_value_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean estimate surprise for the PPROFITREP metric (actual minus mean consensus) |
| 1697 | `median_estimate_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted median analyst estimate for the PPROFITREP metric |
| 1698 | `median_estimate_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst estimates for PPROFITREP |
| 1699 | `median_forecast_actual_combined_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted median estimate combined with actuals (FA overlay) |
| 1700 | `median_forecast_actual_combined_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast-plus-Actual overlay: median estimate combined with subsequent actuals for PPROFITREP |
| 1701 | `median_surprise_value_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted median estimate surprise for the PPROFITREP metric |
| 1702 | `median_surprise_value_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median estimate surprise for the PPROFITREP metric (actual minus median consensus) |
| 1703 | `min_estimate_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency-adjusted lowest analyst estimate for the PPROFITREP metric |
| 1704 | `min_estimate_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest individual analyst estimate for PPROFITREP |
| 1705 | `stddev_estimate_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation (dispersion) of analyst estimates for PPROFITREP |
| 1706 | `stddev_fxadj_pretax_reported_quarterly16` | VECTOR | 0.378 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted standard deviation of analyst estimates for PPROFITREP |
| 1707 | `actual_dps_value_fxadj_quarterly16` | VECTOR | 0.315 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Currency and split adjusted vector of reported quarterly DPS actuals aligned to event periods |
| 1708 | `actual_dps_value_quarterly16` | VECTOR | 0.315 | 其他 | 0 | — | — | — | UNUSABLE | Actual reported DPS value |
| 1709 | `estimate_count_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the consensus |
| 1710 | `forecast_actual_flag_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Flag indicating status/provenance of Forecast-plus-Actual data for DPS (e.g., 0 backfilled, 1 consensus forecast, 2 actu |
| 1711 | `forecast_actual_indicator_dps_quarterly16` | VECTOR | 0.315 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Event/period indicator: codes marking forecast periods (M…1) and actual-reporting periods (0, -1, -2, …) |
| 1712 | `max_estimate_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate (forecast only) |
| 1713 | `max_estimate_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate adjusted for currency/splits/regime |
| 1714 | `mean_estimate_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean (consensus) of analyst estimates |
| 1715 | `mean_estimate_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted mean consensus DPS estimate for the quarter |
| 1716 | `mean_forecast_actual_combined_dps_quarterly16` | VECTOR | 0.315 | 其他 | 0 | — | — | — | UNUSABLE | Forecast-plus-Actual mean series for DPS |
| 1717 | `mean_forecast_actual_combined_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean FA estimate adjusted for currency/splits/regime |
| 1718 | `mean_surprise_value_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise versus mean DPS estimate (actual minus mean consensus) |
| 1719 | `mean_surprise_value_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted surprise versus mean estimate |
| 1720 | `median_estimate_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst estimates (consensus) for the measure |
| 1721 | `median_estimate_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split/regime-adjusted median consensus DPS estimate |
| 1722 | `median_forecast_actual_combined_dps_quarterly16` | VECTOR | 0.315 | 其他 | 0 | — | — | — | UNUSABLE | Forecast-plus-Actual median series for DPS |
| 1723 | `median_forecast_actual_combined_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median FA estimate adjusted for currency/splits/regime |
| 1724 | `median_surprise_value_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Surprise versus the median estimate (actual minus median) |
| 1725 | `median_surprise_value_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/regime-adjusted surprise versus the median estimate |
| 1726 | `min_estimate_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate (forecast only) |
| 1727 | `min_estimate_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate adjusted for currency/splits/regime |
| 1728 | `stddev_estimate_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates |
| 1729 | `stddev_estimate_fxadj_dps_quarterly16` | VECTOR | 0.315 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates adjusted for currency/regime |
| 1730 | `actual_eps_value_fxadj_quarterly16` | VECTOR | 0.294 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Regime-adjusted reported quarterly EPS actual value |
| 1731 | `actual_eps_value_quarterly16` | VECTOR | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Reported quarterly EPS actual value |
| 1732 | `estimate_count_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current number of EPS estimates contributing to the consensus |
| 1733 | `estimate_count_flash_period_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of flash analyst EPS estimates in the snapshot |
| 1734 | `estimate_count_four_weeks_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst EPS estimates in the consensus four weeks ago |
| 1735 | `estimate_count_three_months_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst EPS estimates in the consensus three months ago |
| 1736 | `max_estimate_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest current quarterly EPS consensus estimate |
| 1737 | `max_estimate_four_weeks_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest quarterly EPS consensus estimate from four weeks ago |
| 1738 | `max_estimate_four_weeks_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest consensus quarterly EPS estimate from four weeks ago, adjusted for currency, splits, and regime effects |
| 1739 | `max_estimate_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest adjusted current quarterly EPS estimate in the consensus |
| 1740 | `max_estimate_three_months_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest quarterly EPS estimate in the consensus three months ago |
| 1741 | `max_estimate_three_months_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest adjusted quarterly EPS estimate in the consensus three months ago |
| 1742 | `mean_estimate_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current mean of the quarterly EPS consensus estimates |
| 1743 | `mean_estimate_four_weeks_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean quarterly EPS consensus value from four weeks ago |
| 1744 | `mean_estimate_four_weeks_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted mean EPS estimate as of the 4-weeks-ago vendor snapshot |
| 1745 | `mean_estimate_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current currency/split-adjusted mean of analyst consensus EPS estimates for the quarter |
| 1746 | `mean_estimate_three_months_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean quarterly EPS consensus value from three months ago |
| 1747 | `mean_estimate_three_months_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted mean quarterly EPS consensus value from three months ago |
| 1748 | `mean_flash_estimate_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of flash quarterly EPS estimates |
| 1749 | `mean_flash_estimate_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted mean of flash quarterly EPS estimates |
| 1750 | `mean_forecast_actual_combined_eps_quarterly16` | VECTOR | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Mean of the forecast-plus-actual overlay for quarterly EPS |
| 1751 | `mean_forecast_actual_combined_fxadj_eps_quarterly16` | VECTOR | 0.294 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Regime-adjusted forecast-plus-actual combined mean for quarterly EPS |
| 1752 | `mean_surprise_value_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor surprise overlay: actual EPS minus the consensus mean estimate recorded prior to the announcement |
| 1753 | `mean_surprise_value_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted surprise: actual EPS minus consensus mean estimate prior to announcement |
| 1754 | `median_estimate_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of current quarterly EPS consensus estimates |
| 1755 | `median_estimate_four_weeks_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median quarterly EPS consensus estimate from four weeks ago |
| 1756 | `median_estimate_four_weeks_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted median quarterly EPS consensus value from four weeks ago |
| 1757 | `median_estimate_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current currency/split-adjusted median of analyst consensus EPS estimates for the quarter |
| 1758 | `median_estimate_three_months_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median EPS consensus three months ago |
| 1759 | `median_estimate_three_months_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted median quarterly EPS consensus value from three months ago |
| 1760 | `median_forecast_actual_eps_quarterly16` | VECTOR | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Forecast-plus-actual combined median for quarterly EPS under the regime-aware FA overlay |
| 1761 | `median_forecast_actual_fxadj_eps_quarterly16` | VECTOR | 0.294 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of combined forecast and actual earnings per share values for the quarterly period, adjusted for currency effects |
| 1762 | `median_surprise_value_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median quarterly EPS surprise (actual minus consensus), respecting embargo rules |
| 1763 | `median_surprise_value_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median surprise (actual minus consensus) for earnings per share in the quarterly period, adjusted for currency effects. |
| 1764 | `min_estimate_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest current consensus quarterly EPS estimate |
| 1765 | `min_estimate_four_weeks_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest quarterly EPS consensus estimate from four weeks ago |
| 1766 | `min_estimate_four_weeks_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted lowest quarterly EPS estimate from four weeks ago |
| 1767 | `min_estimate_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency and split-adjusted lowest current consensus EPS estimate |
| 1768 | `min_estimate_three_months_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest EPS consensus estimate three months ago |
| 1769 | `min_estimate_three_months_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest adjusted quarterly EPS estimate in the consensus three months ago |
| 1770 | `stddev_estimate_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the current quarterly EPS consensus estimates |
| 1771 | `stddev_estimate_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted standard deviation of current quarterly EPS estimates |
| 1772 | `stddev_flash_estimate_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of flash quarterly EPS estimates |
| 1773 | `stddev_flash_estimate_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of flash quarterly EPS estimates, adjusted for currency, splits, and regime effects |
| 1774 | `stddev_four_weeks_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of EPS estimates four weeks ago |
| 1775 | `stddev_four_weeks_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of earnings per share estimates from four weeks ago for the quarterly period, adjusted for currency e |
| 1776 | `stddev_three_months_prior_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of EPS estimates three months ago |
| 1777 | `stddev_three_months_prior_fxadj_eps_quarterly16` | VECTOR | 0.294 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of earnings per share estimates from three months ago for the quarterly period, adjusted for currency |
| 1778 | `actual_fullyreported_value` | VECTOR | 0.259 | 其他 | 0 | — | — | — | UNUSABLE | Actual reported value for the GPS metric (latest quarterly report) |
| 1779 | `actual_fullyreported_value_fxadj` | VECTOR | 0.259 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Regime- and currency-adjusted actual reported values for the GPS metric |
| 1780 | `estimate_count_current_period_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current number of analyst estimates contributing to the GPS consensus |
| 1781 | `estimate_count_flash_period_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of flash estimates for the GPS measure |
| 1782 | `estimate_count_four_weeks_prior_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to GPS consensus four weeks ago |
| 1783 | `estimate_count_three_months_prior_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to GPS consensus three months ago |
| 1784 | `estimate_currency_code_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency code identifier for the GPS measure (integer mapped to currency) |
| 1785 | `forecast_actual_flag_gps_fq16` | VECTOR | 0.259 | 其他 | 0 | — | — | — | UNUSABLE | Flag indicating whether the GPS data point is forecast (1), actual (2), or backfilled (0) within the Forecast+Actual ove |
| 1786 | `forecast_actual_indicator_gps_fq16` | VECTOR | 0.259 | 其他 | 0 | — | — | — | UNUSABLE | Indicator showing if the value is a forecast or actual for fully reported EPS in the quarter. |
| 1787 | `max_estimate_current_period_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest current GPS consensus estimate |
| 1788 | `max_estimate_four_weeks_prior_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest GPS consensus estimate four weeks ago |
| 1789 | `max_estimate_four_weeks_prior_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regime-adjusted highest GPS consensus estimate four weeks ago |
| 1790 | `max_estimate_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted highest current consensus estimate for GPS |
| 1791 | `max_estimate_three_months_prior_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest GPS consensus estimate three months ago |
| 1792 | `max_estimate_three_months_prior_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest adjusted analyst estimate for the GPS metric as of three months ago (vendor snapshot, currency and split adjuste |
| 1793 | `mean_estimate_current_period_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current mean consensus estimate for the GPS metric |
| 1794 | `mean_estimate_four_weeks_prior_fxadj_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted mean GPS consensus four weeks ago |
| 1795 | `mean_estimate_four_weeks_prior_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus mean estimate for the GPS measure as of four weeks ago |
| 1796 | `mean_estimate_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regime-adjusted current mean GPS consensus estimate (adjusted for currency, splits, etc.) |
| 1797 | `mean_estimate_three_months_prior_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean GPS consensus estimate three months ago |
| 1798 | `mean_estimate_three_months_prior_fxadj_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted mean GPS consensus three months ago |
| 1799 | `mean_flash_estimate_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of flash GPS consensus estimates |
| 1800 | `mean_flash_estimate_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted mean of flash analyst estimates for the GPS metric (currency and split adjusted) |
| 1801 | `mean_forecast_actual_combined_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast-plus-actual overlay: mean combining consensus forecasts and subsequent actuals for the GPS metric |
| 1802 | `mean_forecast_actual_combined_fxadj_gps_fq16` | VECTOR | 0.259 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Average of forecast and actual fully reported EPS values, adjusted for currency, for the quarter. |
| 1803 | `mean_surprise_value_fullyreported` | VECTOR | 0.259 | 其他 | 0 | — | — | — | UNUSABLE | Mean of the surprise values (actual minus forecast) for fully reported EPS. |
| 1804 | `mean_surprise_value_fxadj_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average surprise (actual minus mean estimate) for fully reported EPS, adjusted for currency, for the quarter. |
| 1805 | `median_estimate_four_weeks_prior_fxadj_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted median GPS consensus four weeks ago |
| 1806 | `median_estimate_four_weeks_prior_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median GPS consensus four weeks ago (unadjusted) |
| 1807 | `median_estimate_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current adjusted median consensus estimate for the GPS metric (currency and split adjusted) |
| 1808 | `median_estimate_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current median GPS consensus estimate |
| 1809 | `median_estimate_three_months_prior_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median GPS consensus value as of three months ago |
| 1810 | `median_estimate_three_months_prior_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted median GPS consensus estimate three months ago |
| 1811 | `median_forecast_actual_combined_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast-plus-actual overlay: median combining consensus forecasts and subsequent actuals for the GPS metric |
| 1812 | `median_forecast_actual_combined_fxadj_fullyreported` | VECTOR | 0.259 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Regime-adjusted forecast-plus-actual median for the GPS metric |
| 1813 | `median_surprise_value_fullyreported` | VECTOR | 0.259 | 其他 | 0 | — | — | — | UNUSABLE | Median of the surprise values (actual minus forecast) for fully reported EPS. |
| 1814 | `median_surprise_value_fxadj_fullyreported` | VECTOR | 0.259 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Median of the surprise values (actual minus forecast) for fully reported EPS, adjusted for currency. |
| 1815 | `min_estimate_current_period_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest current GPS consensus estimate |
| 1816 | `min_estimate_four_weeks_prior_fxadj_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted lowest GPS consensus value four weeks ago |
| 1817 | `min_estimate_four_weeks_prior_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest consensus estimate for the GPS measure as of four weeks ago |
| 1818 | `min_estimate_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current adjusted lowest analyst estimate for the GPS metric (currency and split adjusted) |
| 1819 | `min_estimate_three_months_prior_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest GPS consensus estimate three months ago |
| 1820 | `min_estimate_three_months_prior_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted lowest consensus estimate for GPS three months ago |
| 1821 | `stddev_estimate_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current standard deviation of the adjusted analyst estimates for the GPS metric (currency and split adjusted) |
| 1822 | `stddev_estimate_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of current GPS consensus estimates |
| 1823 | `stddev_flash_estimate_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of flash GPS consensus estimates |
| 1824 | `stddev_flash_estimate_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of regime-adjusted flash GPS consensus estimates |
| 1825 | `stddev_four_weeks_prior_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for the GPS metric as of four weeks ago (vendor snapshot, unadjusted) |
| 1826 | `stddev_four_weeks_prior_fxadj_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the adjusted analyst estimates for the GPS metric as of four weeks ago (vendor snapshot, currency |
| 1827 | `stddev_three_months_prior_fullyreported` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of consensus estimates for the GPS measure three months ago |
| 1828 | `stddev_three_months_prior_fxadj_gps_fq16` | VECTOR | 0.259 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regime-adjusted standard deviation of GPS consensus estimates three months ago |
| 1829 | `actual_pretax_value_fxadj_quarterly16` | VECTOR | 0.250 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Adjusted actual reported figure for the PRR measure (currency and split corrected) |
| 1830 | `actual_pretax_value_quarterly16` | VECTOR | 0.250 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual reported pretax profit for the quarterly period. |
| 1831 | `estimate_count_current_period_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current number of analyst estimates contributing to the PRR consensus |
| 1832 | `estimate_count_flash_period_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of flash estimates contributing to the PRR consensus |
| 1833 | `estimate_count_four_weeks_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for the PRR consensus recorded four weeks ago |
| 1834 | `estimate_count_three_months_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for the PRR consensus recorded three months ago |
| 1835 | `forecast_actual_flag_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Flag indicating provenance/status of FA data (e.g., 0 backfilled, 1 consensus forecast, 2 actual report) |
| 1836 | `forecast_actual_indicator_pretax_quarterly16` | VECTOR | 0.250 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Indicator showing whether the value is a forecast or actual for quarterly pretax profit. |
| 1837 | `max_estimate_four_weeks_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor snapshot of the highest consensus estimate four weeks ago, adjusted for currency and splits |
| 1838 | `max_estimate_four_weeks_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor snapshot of the highest consensus estimate four weeks ago |
| 1839 | `max_estimate_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest current individual analyst estimate for PRR, adjusted for currency/splits |
| 1840 | `max_estimate_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest current individual analyst estimate for PRR |
| 1841 | `max_estimate_three_months_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest individual analyst estimate for PRR as of three months ago, adjusted for currency/splits (vendor snapshot) |
| 1842 | `max_estimate_three_months_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest individual analyst estimate for the PRR measure as of three months ago (vendor snapshot for the quarterly IBES U |
| 1843 | `mean_estimate_four_weeks_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor snapshot of the mean consensus estimate four weeks ago, adjusted for currency and splits |
| 1844 | `mean_estimate_four_weeks_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean consensus estimate for PRR from four weeks ago (vendor snapshot) |
| 1845 | `mean_estimate_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current adjusted mean consensus estimate for the PRR measure (currency and split corrected) |
| 1846 | `mean_estimate_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current mean consensus estimate for the PRR measure |
| 1847 | `mean_estimate_three_months_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean analyst pretax profit estimate from three months prior, adjusted for currency, for the quarterly period. |
| 1848 | `mean_estimate_three_months_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean PRR consensus calculated three months ago |
| 1849 | `mean_flash_estimate_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of flash consensus estimates for the PRR measure, adjusted for currency and splits |
| 1850 | `mean_flash_estimate_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of flash consensus estimates for the PRR measure |
| 1851 | `mean_forecast_actual_combined_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Regime-adjusted mean of the forecast-plus-actual (FA) series for PRR |
| 1852 | `mean_forecast_actual_combined_pretax_quarterly16` | VECTOR | 0.250 | 其他 | 0 | — | — | — | UNUSABLE | Mean of the Forecast-plus-Actual composite series for the PRR measure |
| 1853 | `mean_surprise_value_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean value of the difference between actual and consensus pretax profit, adjusted for currency, for the quarterly period |
| 1854 | `mean_surprise_value_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean value of the difference between actual and consensus pretax profit for the quarterly period. |
| 1855 | `median_estimate_four_weeks_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median consensus estimate for PRR from four weeks ago, adjusted for currency/splits (vendor snapshot) |
| 1856 | `median_estimate_four_weeks_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median consensus estimate for PRR from four weeks ago (vendor snapshot) |
| 1857 | `median_estimate_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted median consensus estimate for the PRR measure |
| 1858 | `median_estimate_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current median consensus estimate for PRR |
| 1859 | `median_estimate_three_months_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median consensus estimate for PRR from three months ago, adjusted for currency/splits (vendor snapshot) |
| 1860 | `median_estimate_three_months_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median consensus estimate for PRR from three months ago (vendor snapshot) |
| 1861 | `median_forecast_actual_combined_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median of combined forecast and actual pretax profit, adjusted for currency, for the quarterly period. |
| 1862 | `median_forecast_actual_combined_pretax_quarterly16` | VECTOR | 0.250 | 其他 | 0 | — | — | — | UNUSABLE | Median of the forecast-plus-actual (FA) series for the PRR measure |
| 1863 | `median_surprise_value_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of the difference between actual and consensus pretax profit, adjusted for currency, for the quarterly peri |
| 1864 | `median_surprise_value_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of the difference between actual and consensus pretax profit for the quarterly period. |
| 1865 | `min_estimate_four_weeks_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor snapshot of the lowest consensus estimate four weeks ago, adjusted for currency and splits |
| 1866 | `min_estimate_four_weeks_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest PRR estimate in the consensus four weeks ago |
| 1867 | `min_estimate_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst pretax profit estimate for the quarterly period, adjusted for currency. |
| 1868 | `min_estimate_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest current individual analyst estimate for PRR |
| 1869 | `min_estimate_three_months_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor snapshot of the lowest consensus estimate for the PRR measure from three months ago, adjusted for currency and sp |
| 1870 | `min_estimate_three_months_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest PRR estimate in the consensus three months ago |
| 1871 | `stddev_estimate_four_weeks_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor snapshot of the standard deviation of consensus estimates four weeks ago, adjusted for currency and splits |
| 1872 | `stddev_estimate_four_weeks_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor snapshot of the standard deviation of consensus estimates four weeks ago |
| 1873 | `stddev_estimate_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current adjusted standard deviation of consensus estimates for the PRR measure |
| 1874 | `stddev_estimate_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of current PRR consensus estimates |
| 1875 | `stddev_estimate_three_months_prior_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Vendor snapshot of the standard deviation of consensus estimates three months ago, adjusted for currency and splits |
| 1876 | `stddev_estimate_three_months_prior_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of PRR consensus estimates as of three months ago (vendor snapshot) |
| 1877 | `stddev_flash_estimate_fxadj_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of flash consensus estimates for the PRR measure, adjusted for currency and splits |
| 1878 | `stddev_flash_estimate_pretax_quarterly16` | VECTOR | 0.250 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of flash consensus estimates for the PRR measure |
| 1879 | `actual_value_dps_quarterly16_2` | VECTOR | 0.180 | 其他 | 0 | — | — | — | UNUSABLE | Actual reported quarterly DPS value |
| 1880 | `actual_value_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted actual reported quarterly DPS values vector |
| 1881 | `estimate_count_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of current analyst estimates used in the quarterly DPS consensus |
| 1882 | `estimate_count_flash_period_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of DPS flash estimates |
| 1883 | `estimate_count_four_weeks_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of contributing DPS estimates 4 weeks ago |
| 1884 | `estimate_count_three_months_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of contributing DPS estimates 3 months ago |
| 1885 | `estimate_currency_code_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency code (integer) mapping to the reporting currency for DPS, decoded by date |
| 1886 | `forecast_actual_flag_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Flag indicating provenance/status of FA data: 0 backfilled, 1 consensus forecast, 2 actual report |
| 1887 | `forecast_actual_indicator_dps_quarterly16_2` | VECTOR | 0.180 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Indicator showing whether the value is a forecast or an actual for dividend per share. |
| 1888 | `max_estimate_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest current quarterly DPS estimate |
| 1889 | `max_estimate_four_weeks_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest quarterly DPS estimate four weeks ago |
| 1890 | `max_estimate_four_weeks_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest DPS consensus estimate from 4 weeks ago, adjusted for currency, splits, and regime effects |
| 1891 | `max_estimate_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted highest analyst estimate in the current quarterly DPS consensus |
| 1892 | `max_estimate_three_months_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest consensus estimate for quarterly Dividends Per Share three months ago |
| 1893 | `max_estimate_three_months_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest DPS consensus estimate from 3 months ago, adjusted for currency, splits, and regime effects |
| 1894 | `mean_estimate_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current mean of the quarterly DPS consensus |
| 1895 | `mean_estimate_four_weeks_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of the quarterly DPS consensus 4 weeks ago (vendor snapshot) |
| 1896 | `mean_estimate_four_weeks_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regime-adjusted mean consensus quarterly DPS as of 4 weeks ago |
| 1897 | `mean_estimate_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted current mean of the quarterly DPS consensus |
| 1898 | `mean_estimate_three_months_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean consensus estimate for quarterly Dividends Per Share three months ago |
| 1899 | `mean_estimate_three_months_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted mean of the quarterly DPS consensus 3 months ago |
| 1900 | `mean_flash_estimate_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Mean of flash quarterly DPS estimates |
| 1901 | `mean_flash_estimate_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Average broker estimate for dividend per share, adjusted for currency, in the flash (recent) period. |
| 1902 | `mean_forecast_actual_combined_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Forecast-plus-actual mean for DPS, combining consensus forecasts with subsequent actuals |
| 1903 | `mean_forecast_actual_combined_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Forecast-plus-actual mean for DPS adjusted for currency, splits, and regime effects |
| 1904 | `mean_surprise_value_dps_quarterly16_2` | VECTOR | 0.180 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average surprise value (actual minus forecast) for dividend per share for the current period. |
| 1905 | `mean_surprise_value_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average surprise value (actual minus forecast), adjusted for currency, for dividend per share. |
| 1906 | `median_estimate_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current median of the quarterly DPS consensus |
| 1907 | `median_estimate_four_weeks_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median quarterly DPS consensus as of four weeks ago (unadjusted) |
| 1908 | `median_estimate_four_weeks_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted median quarterly DPS consensus as of four weeks ago |
| 1909 | `median_estimate_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current median DPS consensus estimate adjusted for currency, splits, and regime effects |
| 1910 | `median_estimate_three_months_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median consensus estimate for quarterly Dividends Per Share three months ago |
| 1911 | `median_estimate_three_months_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Currency/split-adjusted median quarterly DPS consensus as of three months ago |
| 1912 | `median_forecast_actual_combined_dps_quarterly16_2` | VECTOR | 0.180 | 其他 | 0 | — | — | — | UNUSABLE | Median of forecast-plus-actual (FA) quarterly DPS overlay (regime-aware) |
| 1913 | `median_forecast_actual_combined_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Forecast-plus-actual median for DPS adjusted for currency, splits, and regime effects |
| 1914 | `median_surprise_value_dps_quarterly16_2` | VECTOR | 0.180 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median surprise value (actual minus forecast) for dividend per share for the current period. |
| 1915 | `median_surprise_value_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Median surprise value (actual minus forecast), adjusted for currency, for dividend per share. |
| 1916 | `min_estimate_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest current quarterly DPS estimate in the analyst consensus |
| 1917 | `min_estimate_four_weeks_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest quarterly DPS consensus estimate as of four weeks ago |
| 1918 | `min_estimate_four_weeks_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted lowest quarterly DPS estimate four weeks ago |
| 1919 | `min_estimate_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate in the current quarterly DPS consensus, currency/split-adjusted |
| 1920 | `min_estimate_three_months_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest consensus estimate for quarterly Dividends Per Share three months ago |
| 1921 | `min_estimate_three_months_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest DPS consensus estimate from 3 months ago, adjusted for currency, splits, and regime effects |
| 1922 | `stddev_estimate_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of the current quarterly DPS consensus estimates |
| 1923 | `stddev_flash_estimate_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of flash snapshot DPS consensus estimates |
| 1924 | `stddev_flash_estimate_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted standard deviation of flash quarterly DPS estimates |
| 1925 | `stddev_four_weeks_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of quarterly DPS estimates as of four weeks ago |
| 1926 | `stddev_four_weeks_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of DPS consensus estimates from 4 weeks ago, adjusted for currency, splits, and regime effects |
| 1927 | `stddev_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regime-adjusted current standard deviation of consensus quarterly DPS |
| 1928 | `stddev_three_months_prior_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of quarterly DPS estimates three months ago |
| 1929 | `stddev_three_months_prior_fxadj_dps_quarterly16_2` | VECTOR | 0.180 | 修正与预期 | 0 | — | — | — | UNUSABLE | Adjusted standard deviation of quarterly DPS estimates three months ago |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `P02rW1r7` | 0.96 | 0.53 | 0.66 | 0.50 | 0.03 | "[\"LOW_SHAR | probe_pretax_20260919 | `rank(ts_zscore(ts_backfill(vec_avg(mean_flash_estimate_pretax_annual12), 22), 252))` |
| `YPbwrAwl` | 0.50 | 0.19 | 0.32 | 0.34 | 0.05 | "[\"LOW_SHAR | probe_pretax_20260919 | `rank(ts_delta(ts_backfill(vec_avg(mean_flash_estimate_pretax_annual12), 22), 66))` |
| `O0NwY9wq` | 0.40 | 0.14 | -0.67 | 0.12 | 0.03 | "[\"LOW_SHAR | probe_pretax_20260919 | `group_rank(divide(subtract(ts_backfill(vec_avg(mean_flash_estimate_pretax_annual12), 22), ` |
| `ZY07MWdn` | 0.22 | 0.06 | -0.02 | — | 0.36 | ["LOW_SHARPE | s2_analyst_consensus_d1 | `group_mean(vec_avg(actual_ebit_value_annual12), vec_avg(actual_depreciation_value_fxadj_an` |
| `wpYjPJ2d` | 0.14 | 0.04 | -0.19 | — | 0.10 | ["LOW_SHARPE | s2_analyst_consensus_d1 | `ts_arg_min(vec_avg(actual_ebit_value_annual12), 20)` |
| `A10lmOzd` | 0.02 | 0.00 | 0.46 | — | 0.11 | ["LOW_SHARPE | s2_analyst_consensus_d1 | `ts_covariance(vec_avg(actual_fcf_value_annual12), vec_avg(actual_currentassets_value_annua` |
| `WjP70WzO` | -0.04 | -0.01 | -0.37 | — | 0.13 | ["LOW_SHARPE | s2_analyst_consensus_d1 | `ts_kurtosis(vec_avg(median_estimate_return_on_capital_annual12), 20)` |
| `Jjx715WW` | -0.18 | -0.05 | -0.11 | — | 0.37 | ["LOW_SHARPE | s2_analyst_consensus_d1 | `group_sum(vec_avg(actual_ebit_value_annual12), sector)` |

## 七、判死记录（sealed dead_end）

- `EUR-ANL11-ESG-SLOWVAR-LONGCOUNT`（None）family=analyst11 ESG 评分体系（三支柱 + 行业排名 + 改善动量）：{"critical_lesson": "★ coverage 元数据虚报（缺陷#3 第4次坐实）：catalog 报 cov=0.9123/0.9087，实际回测 longCount 仅 51-52（占 TOP2500 的 2%）。选数据集时不能信 catalog coverage，必须用 1-2 条探针实测 longCount。", "dataset": "analyst11", "evidence": {"1YxzzPmQ": "ESG 绝对水平 rank(overall_sustainability_score_2)：S-0.68/F-0.13/TVR0.0985/longCount 52/CW FAIL", "A1077x7l": "行业内排名 rank(reverse(anl11_esgreg_industryrnk))：S-0.25/F-0.03/longCount 51/C
- `EUR-CONSENSUS-SURPRISE-TP-WEAK`（2026-08-25）family=analyst_consensus surprise/estimate/target x v_rev/wedge：{"best": {"alpha": "Xg7pogXl", "fitness": 0.48, "sharpe": 0.97}, "reason": "Wave63 seven consensus slows (EPS mean/std, EPS surprise, estimate count, rev/FCF/EBIT surprise, MATRIX target price) x v_rev/wedge. Max S0.97. Stop resid x PV template grinding.", "rule": "Do not reuse analyst_consensus surprise/target residuals as 0.30 slow legs with v_rev/falling_wedge. Prefer GEM concept generation on 
- `EUR-ANALYST-CONSENSUS-TARGETPRICE-DEAD`（2026-10-19）family=analyst_consensus：{"contradicts_archive": "档案 §4.1 曾把该数据集评为「机制价值最高：mean/stddev 成对 ⇒ 可直接构造 targetprice 修正 ÷ 分歧度，且拥挤度 aCnt 仅 0–6，与已锁死的 eps_revision_magnitude 机制完全正交」。实测：正交性成立，但信号强度为零——正交于一个不存在的东西没有价值。", "evidence": {"best_reading": "RRA1L0ge (estimate_count 覆盖广度) S 0.41 / 2Y -0.95；xA1daXLl S 0.11 / F 0.11；XgR8EXA0 与 88veqgwW S -0.07；9qE7Qg5r S -0.11；j2erQNpE 与 wp9EVXr1 S -0.14；RRA1L0Od S -0.34；e76xJeME S 0.29 但 2Y 1.

