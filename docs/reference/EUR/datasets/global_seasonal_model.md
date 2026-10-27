# global_seasonal_model — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `global_seasonal_model` |
| 名称 | Global Seasonal Regime Return Signals |
| 类别 | MODEL |
| 数据字段数(平台) | 449 |
| 覆盖率 | 0.9886 |
| 平台已有 alpha | 52 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides predictive return signals for global equities by modeling the impact of calendar seasonality, corporate event timing, market regime context, and key data sources such as price-volume, analyst forecasts, options, and fundamentals. Each module isolates a specific data aspect—like price-volume trends, analyst revisions, or option-implied signals—and overlays contextual features such as month/quarter effects, proximity to earnings or guidance events, and prevailing market regimes (e.g., risk-on/off, expansion/contraction). The dataset is strictly point-in-time and D1-lagged to avoid lookahead bias, making it robust for research and production use. By enabling detailed analysis of how individual features and market contexts drive return predictions, it supports advanced qu

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **449** |
| 类型分布 | MATRIX×449 |
| 平均覆盖率 | **0.989** |
| 覆盖率区间 | 0.72 ~ 1.00 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 435 | 96.9% |
| 中 (0.70–0.90) | 14 | 3.1% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 438 | 97.6% |
| DEAD | 11 | 2.4% |

- 已实测字段：**11** 个（2%），best_sharpe 最高 **0.78**，中位 0.49

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 427 | 0.99 | pv_12m_5d_forward_return、predicted_return_timeseries_5d、pv_12m_20d_forward_return |
| 宏观与行业 | 13 | 0.99 | trading_days_to_next_event、market_regime_2phase、market_regime_4phase_long |
| 其他 | 4 | 1.00 | iso_week_number、market_regime_4phase_short、quarter_end_start_flag |
| 元数据与非信号 | 3 | 1.00 | month_indicator_code、quarter_indicator_code、trading_weekday_code |
| 修正与预期 | 2 | 0.87 | analyst_metadata_feature1、analyst_metadata_feature2 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `pv_12m_5d_forward_return` | MATRIX | 0.997 | 价量与波动 | 5 | 0.78 | 0.39 | — | DEAD | Predicted 5-day forward return for a stock using 12-month price-volume features. |
| 2 | `predicted_return_timeseries_5d` | MATRIX | 0.997 | 价量与波动 | 1 | 0.64 | -0.03 | — | DEAD | Predicted 5-day forward return as a continuous value using time series features. |
| 3 | `pv_12m_20d_forward_return` | MATRIX | 0.997 | 价量与波动 | 1 | 0.56 | 0.73 | — | DEAD | Predicted 20-day forward return for a stock using 12-month price-volume features. |
| 4 | `pv_5d_forward_return` | MATRIX | 0.997 | 价量与波动 | 1 | 0.56 | 0.95 | — | DEAD | Predicted 5-day forward return for a stock using daily price-volume features. |
| 5 | `confidence_bucket0_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 2 | 0.53 | 0.05 | — | DEAD | Model confidence score for the 0th quantile bucket in 5-day return prediction using price-volume features. |
| 6 | `predicted_return_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 1 | 0.49 | 0.17 | — | DEAD | Predicted 5-day forward return as a continuous value using price-volume features. |
| 7 | `funda_event_60d_return_regression` | MATRIX | 0.997 | 价量与波动 | 1 | 0.45 | 1.17 | — | DEAD | Predicted 60-day forward return (regression output) using fundamental and event features. |
| 8 | `weekly_pricevol_calendar_r5_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 2 | 0.01 | -0.31 | — | DEAD | Model confidence score for the first quantile label in 5-day return prediction using weekly price-volume data with calen |
| 9 | `weekly_pricevol_calendar_r5_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 2 | 0.00 | 0.57 | — | DEAD | Model confidence score for the first quantile label in 5-day return prediction using weekly price-volume data with calen |
| 10 | `prob_bucket0_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 2 | -0.25 | -0.59 | — | DEAD | Probability assigned to the 0th quantile bucket for 5-day return prediction using price-volume features. |
| 11 | `trading_days_to_next_event` | MATRIX | 1.000 | 宏观与行业 | 1 | -0.51 | 0.25 | — | DEAD | Number of trading days until the next scheduled corporate event. |
| 12 | `iso_week_number` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | ISO-style week number within the year for the current trading day. |
| 13 | `market_regime_2phase` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Binary market regime label (e.g., risk-on/risk-off) for current macro context. |
| 14 | `market_regime_4phase_long` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long-horizon market regime label (0–3) indicating macroeconomic or market state. |
| 15 | `market_regime_4phase_medium` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Medium-horizon 4-phase market regime label (0–3) for macroeconomic context. |
| 16 | `market_regime_4phase_short` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Short-horizon 4-phase market regime label (0–3) for current market state. |
| 17 | `month_indicator_code` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Month code (1–12) as an indicator variable for the current month. |
| 18 | `quarter_end_start_flag` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating proximity to quarter-end or quarter-start for the current trading day. |
| 19 | `quarter_indicator_code` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Quarter code (1–4) as an indicator variable for the current quarter. |
| 20 | `trading_days_since_last_event` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Number of trading days since the most recent scheduled corporate event. |
| 21 | `trading_days_to_month_end` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Number of trading days remaining until the end of the current month. |
| 22 | `analyst_metadata_feature1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | First summary feature derived from analyst consensus or guidance metadata. |
| 23 | `trading_weekday_code` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Numeric code representing the trading day of the week (e.g., Monday=0). |
| 24 | `future_event_update_flag` | MATRIX | 0.998 | 宏观与行业 | 0 | — | — | — | UNTESTED | Indicator for whether the next scheduled corporate event has been updated, rescheduled, or cancelled. |
| 25 | `next_event_confirmation_level` | MATRIX | 0.998 | 宏观与行业 | 0 | — | — | — | UNTESTED | Confirmation or tentative status for the next scheduled corporate event. |
| 26 | `next_event_transcript_flag` | MATRIX | 0.998 | 宏观与行业 | 0 | — | — | — | UNTESTED | Indicator for whether a transcript is expected or available for the next scheduled corporate event. |
| 27 | `next_event_type_code` | MATRIX | 0.998 | 宏观与行业 | 0 | — | — | — | UNTESTED | Categorical code for the type of the next scheduled corporate event. |
| 28 | `confidence_bucket0_timeseries_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 0th quantile bucket in 5-day return prediction using time series and calendar features. |
| 29 | `confidence_bucket0_timeseries_event_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 0th quantile bucket in 5-day return prediction using time series and event features. |
| 30 | `confidence_bucket0_timeseries_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 0th quantile bucket in 5-day return prediction using time series and month/quarter featur |
| 31 | `confidence_bucket2_timeseries_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 5-day return prediction using time series and calendar features. |
| 32 | `confidence_bucket2_timeseries_regime_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 5-day return prediction using time series and regime features. |
| 33 | `confidence_bucket3_timeseries_event_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 3rd quantile bucket in 5-day return prediction using time series and event features. |
| 34 | `confidence_bucket4_timeseries_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 4th quantile bucket in 5-day return prediction using time series features. |
| 35 | `event_5d_return_regression_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 5-day forward return (regression output) using event-only features. |
| 36 | `funda_event_120d_return_regression` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 120-day forward return (regression output) using fundamental and event features. |
| 37 | `funda_regime_120d_return_regression` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 120-day forward return (regression output) using fundamental and regime features. |
| 38 | `funda_regime_20d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 20-day return (regression output) using fundamental data with regime context. |
| 39 | `funda_regime_5d_5bucket_confidence_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 5-day return using fundamental data with regim |
| 40 | `funda_regime_5d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 5-day return using fundamental data with regim |
| 41 | `funda_regime_5d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 5-day return using fundamental data with regim |
| 42 | `funda_regime_5d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 5-day return quantile using fundamental data with regime context. |
| 43 | `funda_regime_5d_5bucket_prob_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 0 in 5-bucket quantile classification of 5-day return using fundamental data with regime |
| 44 | `funda_regime_5d_5bucket_prob_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 2 in 5-bucket quantile classification of 5-day return using fundamental data with regime |
| 45 | `funda_regime_5d_5bucket_prob_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 3 in 5-bucket quantile classification of 5-day return using fundamental data with regime |
| 46 | `funda_regime_60d_return_regression` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 60-day forward return (regression output) using fundamental and regime features. |
| 47 | `predicted_bucket_timeseries_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 5-day forward return using time series features. |
| 48 | `predicted_bucket_timeseries_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 5-day forward return using time series and calendar features. |
| 49 | `predicted_return_timeseries_event_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 5-day forward return as a continuous value using time series and event features. |
| 50 | `prob_bucket1_regime_timeseries_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 1st quantile bucket for 5-day return prediction using time series and regime features. |
| 51 | `prob_bucket2_regime_timeseries_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 2nd quantile bucket for 5-day return prediction using time series and regime features. |
| 52 | `pv_weekly_60d_return_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the zeroth quantile for 60-day forward return prediction using weekly price-volume data. |
| 53 | `pv_weekly_60d_return_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile in 60-day forward return prediction using weekly price-volume data. |
| 54 | `pv_weekly_60d_return_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 60-day forward return prediction using weekly price-volume data. |
| 55 | `pv_weekly_60d_return_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile in 60-day forward return prediction using weekly price-volume data. |
| 56 | `pv_weekly_60d_return_quantile_probs` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Vector of probabilities for all quantiles in 60-day forward return prediction using weekly price-volume data. |
| 57 | `pv_weekly_cal_20d_return_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the zeroth quantile for 20-day forward return prediction using weekly price-volume data with cal |
| 58 | `pv_weekly_cal_20d_return_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 20-day forward return prediction using weekly price-volume data with cale |
| 59 | `pv_weekly_cal_20d_return_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 20-day forward return prediction using weekly price-volume data with cal |
| 60 | `pv_weekly_cal_20d_return_regression` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Regression output predicting 20-day forward return using weekly price-volume data with calendar context. |
| 61 | `pv_weekly_cal_60d_return_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the zeroth quantile in 60-day forward return prediction using weekly price-volume data with c |
| 62 | `pv_weekly_cal_60d_return_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 60-day forward return prediction using weekly price-volume data with cal |
| 63 | `pv_weekly_event_20d_return_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile in 20-day forward return prediction using weekly price-volume data with ev |
| 64 | `pv_weekly_event_20d_return_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 20-day forward return prediction using weekly price-volume data with even |
| 65 | `pv_weekly_event_20d_return_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile in 20-day forward return prediction using weekly price-volume data with e |
| 66 | `pv_weekly_event_20d_return_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 20-day forward return prediction using weekly price-volume data with even |
| 67 | `pv_weekly_event_20d_return_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile in 20-day forward return prediction using weekly price-volume data with e |
| 68 | `pv_weekly_event_20d_return_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 20-day forward return prediction using weekly price-volume data with eve |
| 69 | `pv_weekly_event_20d_return_quantile_probs` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Vector of probabilities for all quantiles in 20-day forward return prediction using weekly price-volume data with event |
| 70 | `pv_weekly_event_60d_return_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 60-day forward return prediction using weekly price-volume data with even |
| 71 | `pv_weekly_event_60d_return_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 60-day forward return prediction using weekly price-volume data with eve |
| 72 | `pv_weekly_monthqtr_20d_return_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the zeroth quantile for 20-day forward return prediction using weekly price-volume data with mon |
| 73 | `pv_weekly_monthqtr_20d_return_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile in 20-day forward return prediction using weekly price-volume data with mo |
| 74 | `pv_weekly_monthqtr_60d_return_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 60-day forward return prediction using weekly price-volume data with mont |
| 75 | `pv_weekly_monthqtr_60d_return_regression` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Regression output predicting 60-day forward return using weekly price-volume data with month/quarter context. |
| 76 | `pv_weekly_regime_20d_return_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile in 20-day forward return prediction using weekly price-volume data with re |
| 77 | `pv_weekly_regime_20d_return_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 20-day forward return prediction using weekly price-volume data with regi |
| 78 | `pv_weekly_regime_20d_return_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile in 20-day forward return prediction using weekly price-volume data with r |
| 79 | `pv_weekly_regime_20d_return_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 20-day forward return prediction using weekly price-volume data with reg |
| 80 | `pv_weekly_regime_60d_return_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the zeroth quantile for 60-day forward return prediction using weekly price-volume data with reg |
| 81 | `pv_weekly_regime_60d_return_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 60-day forward return prediction using weekly price-volume data with reg |
| 82 | `pv_weekly_regime_60d_return_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 60-day forward return prediction using weekly price-volume data with reg |
| 83 | `pvweekly_20d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 20-day return (regression output) using price-volume weekly data. |
| 84 | `pvweekly_60d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 60-day return (regression output) using price-volume weekly data. |
| 85 | `pvweekly_60d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 60-day return using price-volume weekly data. |
| 86 | `pvweekly_60d_5bucket_confidence_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data. |
| 87 | `pvweekly_60d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 60-day return using price-volume weekly data. |
| 88 | `pvweekly_60d_5bucket_prob_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data. |
| 89 | `pvweekly_60d_5bucket_prob_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 2 in 5-bucket quantile classification of 60-day return using price-volume weekly data. |
| 90 | `pvweekly_60d_5bucket_prob_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 4 in 5-bucket quantile classification of 60-day return using price-volume weekly data. |
| 91 | `pvweekly_calendar_20d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 92 | `pvweekly_calendar_20d_5bucket_confidence_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 93 | `pvweekly_calendar_20d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 94 | `pvweekly_calendar_20d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 95 | `pvweekly_calendar_20d_5bucket_confidence_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 96 | `pvweekly_calendar_20d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 20-day return quantile using price-volume weekly data with calendar context. |
| 97 | `pvweekly_calendar_20d_5bucket_prob_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 3 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 98 | `pvweekly_calendar_20d_5bucket_prob_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 4 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 99 | `pvweekly_calendar_60d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 60-day return (regression output) using price-volume weekly data with calendar context. |
| 100 | `pvweekly_calendar_60d_5bucket_confidence_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 101 | `pvweekly_calendar_60d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 102 | `pvweekly_calendar_60d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 103 | `pvweekly_calendar_60d_5bucket_confidence_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 104 | `pvweekly_calendar_60d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 60-day return quantile using price-volume weekly data with calendar context. |
| 105 | `pvweekly_calendar_60d_5bucket_prob_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 0 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 106 | `pvweekly_calendar_60d_5bucket_prob_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 107 | `pvweekly_calendar_60d_5bucket_prob_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 2 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 108 | `pvweekly_calendar_60d_5bucket_prob_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 3 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 109 | `pvweekly_event_20d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 20-day return (regression output) using price-volume weekly data with event context. |
| 110 | `pvweekly_event_20d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 111 | `pvweekly_event_20d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 112 | `pvweekly_event_20d_5bucket_prob_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 0 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 113 | `pvweekly_event_20d_5bucket_prob_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 2 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 114 | `pvweekly_event_60d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 60-day return (regression output) using price-volume weekly data with event context. |
| 115 | `pvweekly_event_60d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 116 | `pvweekly_event_60d_5bucket_confidence_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 117 | `pvweekly_event_60d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 118 | `pvweekly_event_60d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 119 | `pvweekly_event_60d_5bucket_confidence_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 120 | `pvweekly_event_60d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 60-day return quantile using price-volume weekly data with event context. |
| 121 | `pvweekly_event_60d_5bucket_prob_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 0 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 122 | `pvweekly_event_60d_5bucket_prob_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 3 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 123 | `pvweekly_event_60d_5bucket_prob_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 4 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 124 | `pvweekly_monthquarter_20d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 20-day return (regression output) using price-volume weekly data with month/quarter context. |
| 125 | `pvweekly_monthquarter_20d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 126 | `pvweekly_monthquarter_20d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 127 | `pvweekly_monthquarter_20d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 128 | `pvweekly_monthquarter_20d_5bucket_confidence_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 129 | `pvweekly_monthquarter_20d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 20-day return quantile using price-volume weekly data with month/quarter context. |
| 130 | `pvweekly_monthquarter_20d_5bucket_prob_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 1 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 131 | `pvweekly_monthquarter_20d_5bucket_prob_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 2 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 132 | `pvweekly_monthquarter_20d_5bucket_prob_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 3 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 133 | `pvweekly_monthquarter_20d_5bucket_prob_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 4 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 134 | `pvweekly_monthquarter_60d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 135 | `pvweekly_monthquarter_60d_5bucket_confidence_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 136 | `pvweekly_monthquarter_60d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 137 | `pvweekly_monthquarter_60d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 138 | `pvweekly_monthquarter_60d_5bucket_confidence_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 139 | `pvweekly_monthquarter_60d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 60-day return quantile using price-volume weekly data with month/quarter context. |
| 140 | `pvweekly_monthquarter_60d_5bucket_prob_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 0 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 141 | `pvweekly_monthquarter_60d_5bucket_prob_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 142 | `pvweekly_monthquarter_60d_5bucket_prob_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 2 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 143 | `pvweekly_monthquarter_60d_5bucket_prob_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 4 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 144 | `pvweekly_regime_20d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 20-day return (regression output) using price-volume weekly data with regime context. |
| 145 | `pvweekly_regime_20d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 146 | `pvweekly_regime_20d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 147 | `pvweekly_regime_20d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 20-day return using price-volume weekly data w |
| 148 | `pvweekly_regime_20d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 20-day return quantile using price-volume weekly data with regime context. |
| 149 | `pvweekly_regime_20d_5bucket_prob_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 0 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 150 | `pvweekly_regime_20d_5bucket_prob_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 1 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 151 | `pvweekly_regime_20d_5bucket_prob_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 2 in 5-bucket quantile classification of 20-day return using price-volume weekly data wi |
| 152 | `pvweekly_regime_5d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 5-day return (regression output) using price-volume weekly data with regime context. |
| 153 | `pvweekly_regime_60d_1bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 60-day return (regression output) using price-volume weekly data with regime context. |
| 154 | `pvweekly_regime_60d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 155 | `pvweekly_regime_60d_5bucket_confidence_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 156 | `pvweekly_regime_60d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 157 | `pvweekly_regime_60d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 158 | `pvweekly_regime_60d_5bucket_confidence_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-bucket quantile classification of 60-day return using price-volume weekly data w |
| 159 | `pvweekly_regime_60d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 60-day return quantile using price-volume weekly data with regime context. |
| 160 | `pvweekly_regime_60d_5bucket_prob_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 1 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 161 | `pvweekly_regime_60d_5bucket_prob_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 3 in 5-bucket quantile classification of 60-day return using price-volume weekly data wi |
| 162 | `regime_20d_return_regression` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Regression output predicting 20-day forward return using regime-based time series features. |
| 163 | `regime_5d_return_quantile5_prob1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 1 for 5-day forward return quantile (out of 5) using regime-only features. |
| 164 | `regime_5d_return_quantile5_prob4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 for 5-day forward return quantile (out of 5) using regime-only features. |
| 165 | `regime_5d_return_quantile5_score0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-day forward return quantile (out of 5) using regime-only features. |
| 166 | `regime_5d_return_quantile5_score4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-day forward return quantile (out of 5) using regime-only features. |
| 167 | `regime_5d_return_regression` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Regression output predicting 5-day forward return using regime-based time series features. |
| 168 | `ts_5d_q5_label0_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-quantile classification of 5-day return using time series features. |
| 169 | `ts_5d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 5-day return using time series features. |
| 170 | `ts_5d_q5_label1_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-quantile classification of 5-day return using time series features. |
| 171 | `ts_5d_q5_label1_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 1 in 5-quantile classification of 5-day return using time series features. |
| 172 | `ts_5d_q5_label2_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-quantile classification of 5-day return using time series features. |
| 173 | `ts_5d_q5_label2_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 2 in 5-quantile classification of 5-day return using time series features. |
| 174 | `ts_5d_q5_label3_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-quantile classification of 5-day return using time series features. |
| 175 | `ts_5d_q5_label3_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 3 in 5-quantile classification of 5-day return using time series features. |
| 176 | `ts_5d_q5_label4_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 in 5-quantile classification of 5-day return using time series features. |
| 177 | `ts_cal_5d_forward_return` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 5-day forward return for a stock using time series with calendar features. |
| 178 | `ts_cal_5d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 5-day return using time series with calendar features. |
| 179 | `ts_cal_5d_q5_label1_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-quantile classification of 5-day return using time series with calendar features |
| 180 | `ts_cal_5d_q5_label1_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 1 in 5-quantile classification of 5-day return using time series with calendar features. |
| 181 | `ts_cal_5d_q5_label2_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 2 in 5-quantile classification of 5-day return using time series with calendar features. |
| 182 | `ts_cal_5d_q5_label3_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-quantile classification of 5-day return using time series with calendar features |
| 183 | `ts_cal_5d_q5_label3_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 3 in 5-quantile classification of 5-day return using time series with calendar features. |
| 184 | `ts_cal_5d_q5_label4_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-quantile classification of 5-day return using time series with calendar features |
| 185 | `ts_cal_5d_q5_label4_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 in 5-quantile classification of 5-day return using time series with calendar features. |
| 186 | `ts_evt_5d_q5_label` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label (0–4) for 5-day return using time series with event features. |
| 187 | `ts_evt_5d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 5-day return using time series with event features. |
| 188 | `ts_evt_5d_q5_label1_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-quantile classification of 5-day return using time series with event features. |
| 189 | `ts_evt_5d_q5_label1_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 1 in 5-quantile classification of 5-day return using time series with event features. |
| 190 | `ts_evt_5d_q5_label2_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-quantile classification of 5-day return using time series with event features. |
| 191 | `ts_evt_5d_q5_label2_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 2 in 5-quantile classification of 5-day return using time series with event features. |
| 192 | `ts_evt_5d_q5_label3_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 3 in 5-quantile classification of 5-day return using time series with event features. |
| 193 | `ts_evt_5d_q5_label4_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-quantile classification of 5-day return using time series with event features. |
| 194 | `ts_evt_5d_q5_label4_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 in 5-quantile classification of 5-day return using time series with event features. |
| 195 | `ts_mq_5d_forward_return` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 5-day forward return for a stock using time series with month/quarter features. |
| 196 | `ts_mq_5d_q5_label` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label (0–4) for 5-day return using time series with month/quarter features. |
| 197 | `ts_mq_5d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 5-day return using time series with month/quarter featur |
| 198 | `ts_mq_5d_q5_label1_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-quantile classification of 5-day return using time series with month/quarter fea |
| 199 | `ts_mq_5d_q5_label1_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 1 in 5-quantile classification of 5-day return using time series with month/quarter featur |
| 200 | `ts_mq_5d_q5_label2_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-quantile classification of 5-day return using time series with month/quarter fea |
| 201 | `ts_mq_5d_q5_label2_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 2 in 5-quantile classification of 5-day return using time series with month/quarter featur |
| 202 | `ts_mq_5d_q5_label3_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-quantile classification of 5-day return using time series with month/quarter fea |
| 203 | `ts_mq_5d_q5_label3_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 3 in 5-quantile classification of 5-day return using time series with month/quarter featur |
| 204 | `ts_mq_5d_q5_label4_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-quantile classification of 5-day return using time series with month/quarter fea |
| 205 | `ts_mq_5d_q5_label4_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 in 5-quantile classification of 5-day return using time series with month/quarter featur |
| 206 | `ts_reg_5d_forward_return` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 5-day forward return for a stock using time series with regime features. |
| 207 | `ts_reg_5d_q5_label` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label (0–4) for 5-day return using time series with regime features. |
| 208 | `ts_reg_5d_q5_label0_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-quantile classification of 5-day return using time series with regime features. |
| 209 | `ts_reg_5d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 5-day return using time series with regime features. |
| 210 | `ts_reg_5d_q5_label1_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-quantile classification of 5-day return using time series with regime features. |
| 211 | `ts_reg_5d_q5_label3_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-quantile classification of 5-day return using time series with regime features. |
| 212 | `ts_reg_5d_q5_label3_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 3 in 5-quantile classification of 5-day return using time series with regime features. |
| 213 | `ts_reg_5d_q5_label4_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-quantile classification of 5-day return using time series with regime features. |
| 214 | `ts_reg_5d_q5_label4_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 in 5-quantile classification of 5-day return using time series with regime features. |
| 215 | `weekly_eventonly_r5_regression_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted continuous 5-day return using only event features in the weekly model (regression output). |
| 216 | `weekly_pricevol_calendar_r5_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 5-day return prediction using weekly price-volume data with calendar cont |
| 217 | `weekly_pricevol_calendar_r5_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using weekly price-volume data with calendar con |
| 218 | `weekly_pricevol_calendar_r5_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using weekly price-volume data with cale |
| 219 | `weekly_pricevol_calendar_r5_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using weekly price-volume data with calendar con |
| 220 | `weekly_pricevol_calendar_r5_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 5-day return prediction using weekly price-volume data with calen |
| 221 | `weekly_pricevol_calendar_r5_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 5-day return prediction using weekly price-volume data with calendar cont |
| 222 | `weekly_pricevol_calendar_r5_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile label in 5-day return prediction using weekly price-volume data with cale |
| 223 | `weekly_pricevol_calendar_r5_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 5-day return prediction using weekly price-volume data with calendar con |
| 224 | `weekly_pricevol_calendar_r5_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 5-day return using weekly price-volume data with calendar features. |
| 225 | `weekly_pricevol_calendar_r5_regression_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted continuous 5-day return using weekly price-volume data with calendar context (regression output). |
| 226 | `weekly_pricevol_event_r5_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 5-day return prediction using weekly price-volume data with event |
| 227 | `weekly_pricevol_event_r5_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 5-day return prediction using weekly price-volume data with event context |
| 228 | `weekly_pricevol_event_r5_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 5-day return prediction using weekly price-volume data with event |
| 229 | `weekly_pricevol_event_r5_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 5-day return prediction using weekly price-volume data with event context |
| 230 | `weekly_pricevol_event_r5_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using weekly price-volume data with even |
| 231 | `weekly_pricevol_event_r5_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using weekly price-volume data with event contex |
| 232 | `weekly_pricevol_event_r5_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 5-day return prediction using weekly price-volume data with event |
| 233 | `weekly_pricevol_event_r5_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 5-day return prediction using weekly price-volume data with event context |
| 234 | `weekly_pricevol_event_r5_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile label in 5-day return prediction using weekly price-volume data with even |
| 235 | `weekly_pricevol_event_r5_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 5-day return prediction using weekly price-volume data with event contex |
| 236 | `weekly_pricevol_event_r5_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 5-day return using weekly price-volume data with event context. |
| 237 | `weekly_pricevol_event_r5_regression_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted continuous 5-day return using weekly price-volume data with event context (regression output). |
| 238 | `weekly_pricevol_monthqtr_r5_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 5-day return prediction using weekly price-volume data with month |
| 239 | `weekly_pricevol_monthqtr_r5_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 5-day return prediction using weekly price-volume data with month/quarter |
| 240 | `weekly_pricevol_monthqtr_r5_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 5-day return prediction using weekly price-volume data with month |
| 241 | `weekly_pricevol_monthqtr_r5_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 5-day return prediction using weekly price-volume data with month/quarter |
| 242 | `weekly_pricevol_monthqtr_r5_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using weekly price-volume data with mont |
| 243 | `weekly_pricevol_monthqtr_r5_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using weekly price-volume data with month/quarte |
| 244 | `weekly_pricevol_monthqtr_r5_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 5-day return prediction using weekly price-volume data with month |
| 245 | `weekly_pricevol_monthqtr_r5_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 5-day return prediction using weekly price-volume data with month/quarter |
| 246 | `weekly_pricevol_monthqtr_r5_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile label in 5-day return prediction using weekly price-volume data with mont |
| 247 | `weekly_pricevol_monthqtr_r5_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 5-day return prediction using weekly price-volume data with month/quarte |
| 248 | `weekly_pricevol_monthqtr_r5_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 5-day return using weekly price-volume data with month/quarter features. |
| 249 | `weekly_pricevol_monthqtr_r5_regression_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted continuous 5-day return using weekly price-volume data with month/quarter context (regression output). |
| 250 | `weekly_pricevol_r20_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 20-day return prediction using weekly price-volume data. |
| 251 | `weekly_pricevol_r20_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 20-day return prediction using weekly price-volume data. |
| 252 | `weekly_pricevol_r20_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 20-day return prediction using weekly price-volume data. |
| 253 | `weekly_pricevol_r20_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 20-day return prediction using weekly price-volume data. |
| 254 | `weekly_pricevol_r20_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 20-day return prediction using weekly price-volume data. |
| 255 | `weekly_pricevol_r20_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 20-day return prediction using weekly price-volume data. |
| 256 | `weekly_pricevol_r20_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 20-day return prediction using weekly price-volume data. |
| 257 | `weekly_pricevol_r20_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 20-day return prediction using weekly price-volume data. |
| 258 | `weekly_pricevol_r20_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile label in 20-day return prediction using weekly price-volume data. |
| 259 | `weekly_pricevol_r20_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 20-day return prediction using weekly price-volume data. |
| 260 | `weekly_pricevol_r20_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 20-day return using weekly price-volume data. |
| 261 | `weekly_pricevol_r5_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 5-day return prediction using weekly price-volume data. |
| 262 | `weekly_pricevol_r5_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 5-day return prediction using weekly price-volume data. |
| 263 | `weekly_pricevol_r5_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using weekly price-volume data. |
| 264 | `weekly_pricevol_r5_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using weekly price-volume data. |
| 265 | `weekly_pricevol_r5_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using weekly price-volume data. |
| 266 | `weekly_pricevol_r5_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using weekly price-volume data. |
| 267 | `weekly_pricevol_r5_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 5-day return prediction using weekly price-volume data. |
| 268 | `weekly_pricevol_r5_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 5-day return prediction using weekly price-volume data. |
| 269 | `weekly_pricevol_r5_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile label in 5-day return prediction using weekly price-volume data. |
| 270 | `weekly_pricevol_r5_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 5-day return prediction using weekly price-volume data. |
| 271 | `weekly_pricevol_r5_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 5-day return using weekly price-volume data. |
| 272 | `weekly_pricevol_r5_regression_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted continuous 5-day return using weekly price-volume data (regression output). |
| 273 | `weekly_pricevol_regime_r5_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 5-day return prediction using weekly price-volume data with regim |
| 274 | `weekly_pricevol_regime_r5_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 5-day return prediction using weekly price-volume data with regime contex |
| 275 | `weekly_pricevol_regime_r5_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using weekly price-volume data with regi |
| 276 | `weekly_pricevol_regime_r5_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using weekly price-volume data with regime conte |
| 277 | `weekly_pricevol_regime_r5_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using weekly price-volume data with regi |
| 278 | `weekly_pricevol_regime_r5_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using weekly price-volume data with regime conte |
| 279 | `weekly_pricevol_regime_r5_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 5-day return prediction using weekly price-volume data with regim |
| 280 | `weekly_pricevol_regime_r5_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 5-day return prediction using weekly price-volume data with regime contex |
| 281 | `weekly_pricevol_regime_r5_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile label in 5-day return prediction using weekly price-volume data with regi |
| 282 | `weekly_pricevol_regime_r5_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fifth quantile for 5-day return prediction using weekly price-volume data with regime contex |
| 283 | `weekly_pricevol_regime_r5_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 5-day return using weekly price-volume data with regime context. |
| 284 | `weekly_pricevol_regime_r5_regression_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted continuous 5-day return using weekly price-volume data with regime context (regression output). |
| 285 | `weekly_regimeonly_r5_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 5-day return prediction using only regime features in the weekly |
| 286 | `weekly_regimeonly_r5_quantile0_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 5-day return prediction using only regime features in the weekly model. |
| 287 | `weekly_regimeonly_r5_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using only regime features in the weekly |
| 288 | `weekly_regimeonly_r5_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using only regime features in the weekly model. |
| 289 | `weekly_regimeonly_r5_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 5-day return prediction using only regime features in the weekly |
| 290 | `weekly_regimeonly_r5_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 5-day return prediction using only regime features in the weekly model. |
| 291 | `weekly_regimeonly_r5_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile label in 5-day return prediction using only regime features in the weekly |
| 292 | `weekly_regimeonly_r5_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 5-day return prediction using only regime features in the weekly model. |
| 293 | `weekly_regimeonly_r5_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fifth quantile label in 5-day return prediction using only regime features in the weekly |
| 294 | `weekly_regimeonly_r5_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fifth quantile for 5-day return prediction using only regime features in the weekly model. |
| 295 | `weekly_regimeonly_r5_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 5-day return using only market regime features in the weekly model. |
| 296 | `confidence_bucket0_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 0th quantile bucket in 20-day return prediction using price-volume features. |
| 297 | `confidence_bucket0_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 0th quantile bucket in 20-day return prediction using price-volume and calendar features. |
| 298 | `confidence_bucket0_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 0th quantile bucket in 5-day return prediction using price-volume and calendar features. |
| 299 | `confidence_bucket0_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 0th quantile bucket in 20-day return prediction using price-volume and month/quarter feat |
| 300 | `confidence_bucket0_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 0th quantile bucket in 60-day return prediction using price-volume and month/quarter feat |
| 301 | `confidence_bucket1_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 1st quantile bucket in 20-day return prediction using price-volume features. |
| 302 | `confidence_bucket1_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 1st quantile bucket in 5-day return prediction using price-volume features. |
| 303 | `confidence_bucket1_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 1st quantile bucket in 20-day return prediction using price-volume and calendar features. |
| 304 | `confidence_bucket1_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 1st quantile bucket in 5-day return prediction using price-volume and calendar features. |
| 305 | `confidence_bucket1_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 1st quantile bucket in 20-day return prediction using price-volume and month/quarter feat |
| 306 | `confidence_bucket1_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 1st quantile bucket in 5-day return prediction using price-volume and month/quarter featu |
| 307 | `confidence_bucket1_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 1st quantile bucket in 60-day return prediction using price-volume and month/quarter feat |
| 308 | `confidence_bucket2_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 20-day return prediction using price-volume features. |
| 309 | `confidence_bucket2_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 5-day return prediction using price-volume features. |
| 310 | `confidence_bucket2_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 20-day return prediction using price-volume and calendar features. |
| 311 | `confidence_bucket2_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 5-day return prediction using price-volume and calendar features. |
| 312 | `confidence_bucket2_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 20-day return prediction using price-volume and month/quarter feat |
| 313 | `confidence_bucket2_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 5-day return prediction using price-volume and month/quarter featu |
| 314 | `confidence_bucket2_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile bucket in 60-day return prediction using price-volume and month/quarter feat |
| 315 | `confidence_bucket3_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 3rd quantile bucket in 20-day return prediction using price-volume features. |
| 316 | `confidence_bucket3_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 3rd quantile bucket in 5-day return prediction using price-volume features. |
| 317 | `confidence_bucket3_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 3rd quantile bucket in 20-day return prediction using price-volume and calendar features. |
| 318 | `confidence_bucket3_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 3rd quantile bucket in 5-day return prediction using price-volume and calendar features. |
| 319 | `confidence_bucket3_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 3rd quantile bucket in 20-day return prediction using price-volume and month/quarter feat |
| 320 | `confidence_bucket3_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 3rd quantile bucket in 60-day return prediction using price-volume and month/quarter feat |
| 321 | `confidence_bucket4_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 4th quantile bucket in 20-day return prediction using price-volume features. |
| 322 | `confidence_bucket4_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 4th quantile bucket in 5-day return prediction using price-volume features. |
| 323 | `confidence_bucket4_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 4th quantile bucket in 20-day return prediction using price-volume and calendar features. |
| 324 | `confidence_bucket4_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 4th quantile bucket in 5-day return prediction using price-volume and calendar features. |
| 325 | `confidence_bucket4_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 4th quantile bucket in 20-day return prediction using price-volume and month/quarter feat |
| 326 | `confidence_bucket4_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 4th quantile bucket in 60-day return prediction using price-volume and month/quarter feat |
| 327 | `daily_pricevol_12m_r20_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the first quantile label in 20-day return prediction using daily price-volume data with 12-mo |
| 328 | `daily_pricevol_12m_r20_quantile1_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 20-day return prediction using daily price-volume data with 12-m |
| 329 | `daily_pricevol_12m_r20_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 20-day return prediction using daily price-volume data with 12-month emb |
| 330 | `daily_pricevol_12m_r20_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 20-day return prediction using daily price-volume data with 12-mo |
| 331 | `daily_pricevol_12m_r20_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 20-day return prediction using daily price-volume data with 12-month embe |
| 332 | `daily_pricevol_12m_r5_quantile2_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the second quantile label in 5-day return prediction using daily price-volume data with 12-mo |
| 333 | `daily_pricevol_12m_r5_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 5-day return prediction using daily price-volume data with 12-month embe |
| 334 | `daily_pricevol_12m_r5_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 5-day return prediction using daily price-volume data with 12-month embed |
| 335 | `daily_pricevol_12m_r5_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile label in 5-day return prediction using daily price-volume data with 12-mo |
| 336 | `daily_pricevol_r20_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 20-day return prediction using daily price-volume data. |
| 337 | `daily_pricevol_r20_quantile2_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the second quantile for 20-day return prediction using daily price-volume data. |
| 338 | `daily_pricevol_r20_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 20-day return prediction using daily price-volume data. |
| 339 | `daily_pricevol_r20_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 20-day return prediction using daily price-volume data. |
| 340 | `daily_pricevol_r20_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 20-day return using daily price-volume data. |
| 341 | `daily_pricevol_r5_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile label in 5-day return prediction using daily price-volume data. |
| 342 | `daily_pricevol_r5_quantile4_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the fourth quantile for 5-day return prediction using daily price-volume data. |
| 343 | `daily_pricevol_r5_quantile_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label for 5-day return using daily price-volume data. |
| 344 | `predicted_bucket_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 20-day forward return using price-volume features. |
| 345 | `predicted_bucket_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 5-day forward return using price-volume features. |
| 346 | `predicted_bucket_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 20-day forward return using price-volume and calendar features. |
| 347 | `predicted_bucket_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 5-day forward return using price-volume and calendar features. |
| 348 | `predicted_bucket_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 20-day forward return using price-volume and month/quarter features. |
| 349 | `predicted_bucket_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 5-day forward return using price-volume and month/quarter features. |
| 350 | `predicted_bucket_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket label for 60-day forward return using price-volume and month/quarter features. |
| 351 | `predicted_return_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 20-day forward return as a continuous value using price-volume and calendar features. |
| 352 | `predicted_return_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 5-day forward return as a continuous value using price-volume and calendar features. |
| 353 | `predicted_return_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 20-day forward return as a continuous value using price-volume and month/quarter features. |
| 354 | `predicted_return_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 5-day forward return as a continuous value using price-volume and month/quarter features. |
| 355 | `prob_bucket0_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 0th quantile bucket for 20-day return prediction using price-volume features. |
| 356 | `prob_bucket0_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 0th quantile bucket for 20-day return prediction using price-volume and calendar features. |
| 357 | `prob_bucket0_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 0th quantile bucket for 5-day return prediction using price-volume and calendar features. |
| 358 | `prob_bucket0_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 0th quantile bucket for 20-day return prediction using price-volume and month/quarter featur |
| 359 | `prob_bucket0_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 0th quantile bucket for 5-day return prediction using price-volume and month/quarter feature |
| 360 | `prob_bucket0_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 0th quantile bucket for 60-day return prediction using price-volume and month/quarter featur |
| 361 | `prob_bucket1_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 1st quantile bucket for 5-day return prediction using price-volume features. |
| 362 | `prob_bucket1_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 1st quantile bucket for 20-day return prediction using price-volume and calendar features. |
| 363 | `prob_bucket1_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 1st quantile bucket for 5-day return prediction using price-volume and calendar features. |
| 364 | `prob_bucket1_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 1st quantile bucket for 20-day return prediction using price-volume and month/quarter featur |
| 365 | `prob_bucket1_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 1st quantile bucket for 5-day return prediction using price-volume and month/quarter feature |
| 366 | `prob_bucket1_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 1st quantile bucket for 60-day return prediction using price-volume and month/quarter featur |
| 367 | `prob_bucket2_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 2nd quantile bucket for 20-day return prediction using price-volume features. |
| 368 | `prob_bucket2_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 2nd quantile bucket for 5-day return prediction using price-volume features. |
| 369 | `prob_bucket2_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 2nd quantile bucket for 20-day return prediction using price-volume and calendar features. |
| 370 | `prob_bucket2_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 2nd quantile bucket for 5-day return prediction using price-volume and calendar features. |
| 371 | `prob_bucket2_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 2nd quantile bucket for 20-day return prediction using price-volume and month/quarter featur |
| 372 | `prob_bucket2_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 2nd quantile bucket for 5-day return prediction using price-volume and month/quarter feature |
| 373 | `prob_bucket2_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 2nd quantile bucket for 60-day return prediction using price-volume and month/quarter featur |
| 374 | `prob_bucket3_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 3rd quantile bucket for 5-day return prediction using price-volume features. |
| 375 | `prob_bucket3_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 3rd quantile bucket for 20-day return prediction using price-volume and calendar features. |
| 376 | `prob_bucket3_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 3rd quantile bucket for 20-day return prediction using price-volume and month/quarter featur |
| 377 | `prob_bucket3_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 3rd quantile bucket for 5-day return prediction using price-volume and month/quarter feature |
| 378 | `prob_bucket3_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 3rd quantile bucket for 60-day return prediction using price-volume and month/quarter featur |
| 379 | `prob_bucket4_pricevol_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 4th quantile bucket for 20-day return prediction using price-volume features. |
| 380 | `prob_bucket4_pricevol_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 4th quantile bucket for 5-day return prediction using price-volume features. |
| 381 | `prob_bucket4_pricevol_calendar_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 4th quantile bucket for 20-day return prediction using price-volume and calendar features. |
| 382 | `prob_bucket4_pricevol_calendar_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 4th quantile bucket for 5-day return prediction using price-volume and calendar features. |
| 383 | `prob_bucket4_pricevol_monthquarter_20d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 4th quantile bucket for 20-day return prediction using price-volume and month/quarter featur |
| 384 | `prob_bucket4_pricevol_monthquarter_5d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 4th quantile bucket for 5-day return prediction using price-volume and month/quarter feature |
| 385 | `prob_bucket4_pricevol_monthquarter_60d` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the 4th quantile bucket for 60-day return prediction using price-volume and month/quarter featur |
| 386 | `pv_12m_20d_q5_label` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label (0–4) for 20-day return using 12-month price-volume features. |
| 387 | `pv_12m_20d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 20-day return using 12-month price-volume features. |
| 388 | `pv_12m_20d_q5_label2_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-quantile classification of 20-day return using 12-month price-volume features. |
| 389 | `pv_12m_20d_q5_label2_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 2 in 5-quantile classification of 20-day return using 12-month price-volume features. |
| 390 | `pv_12m_20d_q5_label4_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-quantile classification of 20-day return using 12-month price-volume features. |
| 391 | `pv_12m_20d_q5_label4_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 in 5-quantile classification of 20-day return using 12-month price-volume features. |
| 392 | `pv_12m_5d_q5_label` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile label (0–4) for 5-day return using 12-month price-volume features. |
| 393 | `pv_12m_5d_q5_label0_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-quantile classification of 5-day return using 12-month price-volume features. |
| 394 | `pv_12m_5d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 5-day return using 12-month price-volume features. |
| 395 | `pv_12m_5d_q5_label1_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-quantile classification of 5-day return using 12-month price-volume features. |
| 396 | `pv_12m_5d_q5_label1_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 1 in 5-quantile classification of 5-day return using 12-month price-volume features. |
| 397 | `pv_12m_5d_q5_label3_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-quantile classification of 5-day return using 12-month price-volume features. |
| 398 | `pv_12m_5d_q5_label4_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 in 5-quantile classification of 5-day return using 12-month price-volume features. |
| 399 | `pv_20d_forward_return` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 20-day forward return for a stock using daily price-volume features. |
| 400 | `pv_20d_q5_label0_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-quantile classification of 20-day return using daily price-volume features. |
| 401 | `pv_20d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 20-day return using daily price-volume features. |
| 402 | `pv_20d_q5_label1_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-quantile classification of 20-day return using daily price-volume features. |
| 403 | `pv_20d_q5_label2_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-quantile classification of 20-day return using daily price-volume features. |
| 404 | `pv_20d_q5_label3_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 3 in 5-quantile classification of 20-day return using daily price-volume features. |
| 405 | `pv_20d_q5_label4_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-quantile classification of 20-day return using daily price-volume features. |
| 406 | `pv_5d_q5_label0_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-quantile classification of 5-day return using daily price-volume features. |
| 407 | `pv_5d_q5_label0_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 in 5-quantile classification of 5-day return using daily price-volume features. |
| 408 | `pv_5d_q5_label1_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-quantile classification of 5-day return using daily price-volume features. |
| 409 | `pv_5d_q5_label1_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 1 in 5-quantile classification of 5-day return using daily price-volume features. |
| 410 | `pv_5d_q5_label2_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-quantile classification of 5-day return using daily price-volume features. |
| 411 | `pv_5d_q5_label2_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 2 in 5-quantile classification of 5-day return using daily price-volume features. |
| 412 | `pv_5d_q5_label3_probability` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 3 in 5-quantile classification of 5-day return using daily price-volume features. |
| 413 | `pv_5d_q5_label4_confidence` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-quantile classification of 5-day return using daily price-volume features. |
| 414 | `pv_daily_20d_return_quantile1_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the first quantile for 20-day forward return prediction using daily price-volume data. |
| 415 | `pv_daily_20d_return_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 20-day forward return prediction using daily price-volume data. |
| 416 | `pv_daily_20d_return_regression` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Regression output predicting 20-day forward return using daily price-volume data. |
| 417 | `pv_dailycal_5d_return_quantile3_prob` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to the third quantile for 5-day forward return prediction using daily price-volume data with calend |
| 418 | `pv_mq_5d_return_quantile0_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the zeroth quantile in 5-day forward return prediction using daily price-volume data with mon |
| 419 | `pv_mq_5d_return_quantile3_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the third quantile in 5-day forward return prediction using daily price-volume data with mont |
| 420 | `pv_mq_5d_return_quantile4_confscore` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the fourth quantile in 5-day forward return prediction using daily price-volume data with mon |
| 421 | `pvdaily12m_60d_5bucket_confidence_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 60-day return using price-volume daily data wi |
| 422 | `pvdaily12m_60d_5bucket_confidence_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 60-day return using price-volume daily data wi |
| 423 | `pvdaily12m_60d_5bucket_confidence_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 5-bucket quantile classification of 60-day return using price-volume daily data wi |
| 424 | `pvdaily12m_60d_5bucket_confidence_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 5-bucket quantile classification of 60-day return using price-volume daily data wi |
| 425 | `pvdaily12m_60d_5bucket_confidence_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 5-bucket quantile classification of 60-day return using price-volume daily data wi |
| 426 | `pvdaily12m_60d_5bucket_pred` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label (0–4) for 60-day return quantile using price-volume daily data with 12-month embedding. |
| 427 | `pvdaily12m_60d_5bucket_prob_0` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 0 in 5-bucket quantile classification of 60-day return using price-volume daily data wit |
| 428 | `pvdaily12m_60d_5bucket_prob_1` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 1 in 5-bucket quantile classification of 60-day return using price-volume daily data wit |
| 429 | `pvdaily12m_60d_5bucket_prob_2` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 2 in 5-bucket quantile classification of 60-day return using price-volume daily data wit |
| 430 | `pvdaily12m_60d_5bucket_prob_3` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 3 in 5-bucket quantile classification of 60-day return using price-volume daily data wit |
| 431 | `pvdaily12m_60d_5bucket_prob_4` | MATRIX | 0.997 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for label 4 in 5-bucket quantile classification of 60-day return using price-volume daily data wit |
| 432 | `last_event_confirmation_level` | MATRIX | 0.985 | 宏观与行业 | 0 | — | — | — | UNTESTED | Confirmation or tentative status for the most recent past corporate event. |
| 433 | `last_event_transcript_flag` | MATRIX | 0.985 | 宏观与行业 | 0 | — | — | — | UNTESTED | Indicator for whether a transcript is available for the most recent past corporate event. |
| 434 | `last_event_type_code` | MATRIX | 0.985 | 宏观与行业 | 0 | — | — | — | UNTESTED | Categorical code for the type of the most recent past corporate event. |
| 435 | `last_event_update_flag` | MATRIX | 0.985 | 宏观与行业 | 0 | — | — | — | UNTESTED | Indicator for whether the most recent past corporate event was updated, rescheduled, or cancelled. |
| 436 | `analyst_metadata_feature2` | MATRIX | 0.746 | 修正与预期 | 0 | — | — | — | UNTESTED | Second summary feature derived from analyst consensus or guidance metadata. |
| 437 | `funda_120d_5bucket_confidence_0` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 0 in 5-bucket quantile classification of 120-day return using fundamental data. |
| 438 | `funda_120d_5bucket_confidence_1` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 1 in 5-bucket quantile classification of 120-day return using fundamental data. |
| 439 | `funda_120d_return_quantile5` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted quantile bucket (out of 5) for 120-day forward return using fundamental data. |
| 440 | `funda_120d_return_quantile5_prob0` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 0 for 120-day forward return quantile (out of 5) using fundamental data. |
| 441 | `funda_120d_return_quantile5_prob1` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 1 for 120-day forward return quantile (out of 5) using fundamental data. |
| 442 | `funda_120d_return_quantile5_prob2` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 2 for 120-day forward return quantile (out of 5) using fundamental data. |
| 443 | `funda_120d_return_quantile5_prob3` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 3 for 120-day forward return quantile (out of 5) using fundamental data. |
| 444 | `funda_120d_return_quantile5_prob4` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability assigned to label 4 for 120-day forward return quantile (out of 5) using fundamental data. |
| 445 | `funda_120d_return_quantile5_score2` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 2 in 120-day forward return quantile (out of 5) using fundamental data. |
| 446 | `funda_120d_return_quantile5_score3` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 3 in 120-day forward return quantile (out of 5) using fundamental data. |
| 447 | `funda_120d_return_quantile5_score4` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for label 4 in 120-day forward return quantile (out of 5) using fundamental data. |
| 448 | `funda_120d_return_regression` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 120-day forward return (regression output) using fundamental data. |
| 449 | `funda_60d_return_regression` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted 60-day forward return (regression output) using fundamental data. |

## 六、本地回测证据

- 本地累计回测 **21** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `qMWj6lgE` | 0.78 | 0.32 | 0.10 | — | 0.18 | ["LOW_SHARPE | 158 | `rank(pv_12m_5d_forward_return)` |
| `vRkjNY9v` | 0.78 | 0.32 | 0.11 | — | 0.18 | ["LOW_SHARPE | 159 | `group_neutralize(rank(pv_12m_5d_forward_return), industry)` |
| `WjP7Pw7k` | 0.64 | 0.20 | -0.03 | — | 0.22 | ["LOW_SHARPE | 160 | `rank(ts_cal_5d_forward_return)` |
| `3q9l9Y9Q` | 0.64 | 0.20 | -0.03 | — | 0.22 | ["LOW_SHARPE | 160 | `rank(predicted_return_timeseries_5d)` |
| `N1Q7bKjw` | 0.61 | 0.17 | -0.10 | — | 0.21 | ["LOW_SHARPE | 159 | `rank(ts_zscore(pv_12m_5d_forward_return, 22))` |
| `YP57vlnJ` | 0.58 | 0.23 | 0.24 | — | 0.13 | ["LOW_SHARPE | 159 | `rank(ts_mean(pv_12m_5d_forward_return, 5))` |
| `A10lGLbd` | 0.58 | 0.23 | 0.39 | — | 0.11 | ["LOW_SHARPE | 159 | `rank(ts_decay_linear(pv_12m_5d_forward_return, 10))` |
| `Jjx7x0xm` | 0.57 | 0.27 | 0.26 | — | 0.11 | ["LOW_SHARPE | 160 | `rank(ts_reg_5d_forward_return)` |
| `Vk67GME5` | 0.56 | 0.21 | 0.73 | — | 0.14 | ["LOW_SHARPE | 159 | `rank(pv_12m_20d_forward_return)` |
| `blRjR2jR` | 0.56 | 0.18 | 0.95 | — | 0.18 | ["LOW_SHARPE | 160 | `rank(pv_5d_forward_return)` |
| `RRV7dzj0` | 0.53 | 0.12 | 0.05 | — | 0.22 | ["LOW_SHARPE | s2_global_seasonal_model_d1 | `rank(divide(confidence_bucket0_pricevol_5d, confidence_bucket0_pricevol_calendar_5d))` |
| `LL979b72` | 0.49 | 0.14 | 0.17 | — | 0.18 | ["LOW_SHARPE | 160 | `rank(predicted_return_pricevol_5d)` |
| `RRV718do` | 0.45 | 0.11 | 1.17 | — | 0.06 | ["LOW_SHARPE | 158 | `rank(funda_event_60d_return_regression)` |
| `E5vlkz1K` | 0.01 | 0.00 | -0.31 | — | 0.21 | ["LOW_SHARPE | s2_global_seasonal_model_d1 | `rank(multiply(ts_zscore(weekly_pricevol_calendar_r5_quantile0_confscore, 66), ts_zscore(co` |
| `KPO7kz3z` | 0.00 | 0.00 | 0.57 | — | 0.21 | ["LOW_SHARPE | s2_global_seasonal_model_d1 | `rank(multiply(ts_zscore(weekly_pricevol_calendar_r5_quantile1_confscore, 66), ts_zscore(co` |

## 七、判死记录（sealed dead_end）

- `EUR-AFT-OSC2-WEAK`（2026-08-25）family=ai_factor_transfer _2 oscillators/money-flow：{"dataset": "ai_factor_transfer", "id": "EUR-AFT-OSC2-WEAK", "reason": "Wave70 56 exprs on unused _2 fields (anomaly/DPO/liq_2/PVO/ADL/CCI/BPO_2). Max S0.58 F0.16. Wave18 already killed base oscillators. Do not mix PV.", "rule": "Leave ai_factor_transfer. Next unused whitelist: global_seasonal_model non-return seasonal features. Do not deepen RelVal EV/EBITDA or v_rev/wedge.", "salvage": "none", "
- `EUR-GSM-EVENT-WEAK`（2026-08-25）family=global_seasonal_model event flags：{"dataset": "global_seasonal_model", "id": "EUR-GSM-EVENT-WEAK", "reason": "Wave71 56 exprs on stock-specific event flags (confirmation/update/transcript/days-since). Max S0.68 F0.29. Wave20 already RED on to-next + return-quantile. Calendar constants have no cross-section. Leave GSM.", "rule": "Leave global_seasonal_model. Do not mix PV. Do not use calendar constants or return-quantile fields. Ne
- `EUR-GSM-SAME-SRC-BUCKET-RATIO`（2026-09-09）family=None：{"dataset": "global_seasonal_model", "delay": 1, "evidence": "wave157 8/8 COMPLETE Sharpe≤0.53 Fitness≤0.12；multiply 交互 4 条 -0.13~0.01", "fields": ["confidence_bucket0_pricevol_5d", "confidence_bucket0_pricevol_calendar_5d", "prob_bucket0_pricevol_5d"], "mechanism": "same-source-bucket-ratio", "reason": "confidence/prob 同源分桶置信度 divide 比值近乎常数零区分度；5d vs calendar_5d 变体同源相关；multiply(ts_zscore) 交互同源高相关

