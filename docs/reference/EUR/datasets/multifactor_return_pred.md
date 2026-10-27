# multifactor_return_pred — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `multifactor_return_pred` |
| 名称 | Multi Factor Market Return Predictions |
| 类别 | MODEL |
| 数据字段数(平台) | 648 |
| 覆盖率 | 0.568 |
| 平台已有 alpha | 18 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides predictive signals for global financial market returns by integrating a diverse set of data sources, including price-volume trends, fundamental financial indicators, analyst forecasts, options market data, event-driven information, and contextual factors such as market regimes and seasonal effects. The dataset delivers both short-term and long-term return forecasts, as well as specialized hedge signals designed to be uncorrelated with the main predictions, supporting risk management and portfolio diversification. By combining multiple data modalities and applying contextual adjustments, the dataset aims to enhance the accuracy and robustness of return predictions, making it a valuable tool for quantitative strategies, asset allocation, and risk-controlled investment d

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **648** |
| 类型分布 | MATRIX×648 |
| 平均覆盖率 | **0.568** |
| 覆盖率区间 | 0.42 ~ 0.59 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 612 | 94.4% |
| 稀疏 (<0.50) | 36 | 5.6% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 643 | 99.2% |
| DEAD | 5 | 0.8% |

- 已实测字段：**5** 个（1%），best_sharpe 最高 **0.57**，中位 0.12

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 270 | 0.56 | long_term_60d_quantile1_pred_mfml、long_term_60d_quantile5_pred_mfml、long_term_predicted_return_quantile5_120d |
| 其他 | 215 | 0.59 | long_hedge2_quantile1_r60_pred、long_hedge2_120d_quantile5_pred_mfml、event_embedding_5d_quantile1_pred_mfml |
| 风险与质量 | 66 | 0.59 | long_horizon_hedge2_120d_quantile5_confidence、long_horizon_hedge2_60d_quantile5_confidence、long_term_120d_quantile5_confidence_score_mfml |
| 修正与预期 | 48 | 0.53 | analyst_120d_quantile1_pred、analyst_120d_5bucket_class_confidence、analyst_120d_5bucket_class_pred_solar |
| 搜索与替代数据 | 31 | 0.59 | alt3_short_term_hedge_signal_5d_q5、alt_short_hedge_5d_bin5_confidence、alt_short_term_hedge_signal_5d_bin1 |
| 持仓与资金流 | 18 | 0.42 | alt_fundamental_60d_bin5_confidence、alt_fundamental_pred_120d_q5、alt_fundamental_pred_60d_q1 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `alt_fundamental_60d_bin5_confidence` | MATRIX | 0.423 | 持仓与资金流 | 1 | 0.57 | -0.07 | — | DEAD | Model confidence for alternative fundamental-based signal over 60 days, quantile 5. |
| 2 | `analyst_120d_quantile1_pred` | MATRIX | 0.526 | 修正与预期 | 1 | 0.24 | 0.48 | — | DEAD | 120-day prediction using analyst-derived features, quantile 1. |
| 3 | `alt3_short_term_hedge_signal_5d_q5` | MATRIX | 0.587 | 搜索与替代数据 | 1 | 0.12 | -0.29 | — | DEAD | Third alternative short-term hedge signal for 5-day horizon, quantile 5. |
| 4 | `long_hedge2_quantile1_r60_pred` | MATRIX | 0.587 | 其他 | 1 | -0.57 | -0.72 | — | DEAD | Alternate long-term, 60-day, quantile 1 hedge signal prediction. |
| 5 | `long_hedge2_120d_quantile5_pred_mfml` | MATRIX | 0.587 | 其他 | 1 | -0.74 | -1.30 | — | DEAD | 120-day long horizon alternate hedge prediction, quantile 5 (multi-model variant, low correlation). |
| 6 | `alt_short_hedge_5d_bin5_confidence` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Model confidence for alternative short-term hedge signal over 5 days, quantile 5. |
| 7 | `alt_short_term_hedge_signal_5d_bin1` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal over 5 days, quantile 1. |
| 8 | `alt_short_term_hedge_signal_5d_bin5` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal over 5 days, quantile 5. |
| 9 | `alt_short_term_hedge_signal_60d_bin5` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal over 60 days, quantile 5. |
| 10 | `event_embedding_5d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day prediction using event-driven features, quantile 1 (multi-model variant). |
| 11 | `long_hedge2_120d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 120-day long horizon alternate hedge prediction, quantile 1 (multi-model variant). |
| 12 | `long_hedge2_60d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day long horizon alternate hedge prediction, quantile 1 (multi-model variant, low correlation). |
| 13 | `long_hedge2_60d_quantile5_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day long horizon alternate hedge prediction, quantile 5 (multi-model variant, low correlation). |
| 14 | `long_horizon_hedge2_120d_quantile5_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for the second long-horizon hedge signal (120-day), quantile 5. |
| 15 | `long_horizon_hedge2_60d_quantile5_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for the second long-horizon hedge signal (60-day), quantile 5. |
| 16 | `long_term_120d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day long horizon quantile 5 prediction (multi-model variant). |
| 17 | `long_term_60d_quantile1_pred_mfml` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day long horizon return prediction, quantile 1 (multi-model variant). |
| 18 | `long_term_60d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day long horizon quantile 5 prediction (multi-model variant). |
| 19 | `long_term_60d_quantile5_pred_mfml` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day long horizon return prediction, quantile 5 (multi-model variant). |
| 20 | `long_term_pred_120d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 120 days, quantile 1. |
| 21 | `long_term_predicted_return_quantile5_120d` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (120-day) return prediction, quantile 5. |
| 22 | `long_term_regime2_phase_120d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 120-day long horizon prediction adjusted for regime 2, quantile 1 (multi-model variant). |
| 23 | `long_term_regime2_phase_60d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day long horizon prediction adjusted for regime 2, quantile 1 (multi-model variant). |
| 24 | `long_term_regime4_adjusted_pred_q1_60d` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon (60-day) prediction adjusted for 4-phase regime, quantile 1. |
| 25 | `long_term_regime4_phase_120d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 120-day long horizon prediction adjusted for regime 4, quantile 1 (multi-model variant). |
| 26 | `long_term_seasonal_adj_pred_60d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 60 days, seasonally adjusted, quantile 1. |
| 27 | `long_term_seasonal_adjusted_pred_q1_120d` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon (120-day) prediction adjusted for seasonal effects, quantile 1. |
| 28 | `regime2_phase_20d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day prediction adjusted for regime 2 phase, quantile 1 (multi-model variant). |
| 29 | `regime2_phase_signal_5d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Signal based on 2-phase regime embedding over 5 days, quantile 1. |
| 30 | `regime4_phase_5d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day regime 4 phase quantile 5 prediction (multi-model variant). |
| 31 | `regime4_phase_adjusted_pred_q1_20d` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day prediction adjusted for 4-phase market regime, quantile 1. |
| 32 | `regime4_phase_adjusted_pred_q5_5d` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day prediction adjusted for 4-phase market regime, quantile 5. |
| 33 | `regime4_phase_signal_5d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Signal based on 4-phase regime embedding over 5 days, quantile 1. |
| 34 | `short_hedge3_20d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day third variant hedge prediction, quantile 1 (multi-model variant, low correlation). |
| 35 | `short_hedge3_20d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day third variant hedge quantile 5 prediction (multi-model variant). |
| 36 | `short_hedge3_20d_quantile5_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day third variant hedge prediction, quantile 5 (multi-model variant, low correlation). |
| 37 | `short_hedge3_60d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day third variant hedge prediction, quantile 1 (multi-model variant, low correlation). |
| 38 | `short_hedge3_60d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day third variant hedge quantile 5 prediction (multi-model variant). |
| 39 | `short_hedge_20d_quantile5_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon hedge prediction, quantile 5 (multi-model variant, low correlation). |
| 40 | `short_hedge_5d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day short horizon hedge quantile 5 prediction (multi-model variant). |
| 41 | `short_hedge_5d_quantile5_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day short horizon hedge prediction, quantile 5 (multi-model variant, low correlation). |
| 42 | `short_hedge_60d_quantile5_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon hedge prediction, quantile 5 (multi-model variant, low correlation). |
| 43 | `short_term_20d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day short horizon quantile 5 prediction (multi-model variant). |
| 44 | `short_term_5d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day short horizon quantile 5 prediction (multi-model variant). |
| 45 | `short_term_60d_quantile5_confidence_score_mfml` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day short horizon quantile 5 prediction (multi-model variant). |
| 46 | `short_term_60d_quantile5_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon prediction, quantile 5 (multi-model variant). |
| 47 | `short_term_hedge_signal_20d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term hedge signal over 20 days, quantile 1. |
| 48 | `short_term_hedge_signal_5d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term hedge signal over 5 days, quantile 1. |
| 49 | `short_term_hedge_signal_60d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term hedge signal over 60 days, quantile 1. |
| 50 | `short_term_hedge_signal_confidence_20d_q5` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for short-horizon (20-day) hedge signal, quantile 5. |
| 51 | `short_term_hedge_signal_confidence_60d_q5` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for short-horizon (60-day) hedge signal, quantile 5. |
| 52 | `short_term_pred_5d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 5 days, quantile 1. |
| 53 | `short_term_pred_5d_bin5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 5 days, quantile 5. |
| 54 | `short_term_predicted_return_quantile1_20d_v2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (20-day) return prediction, quantile 1 (alternate version). |
| 55 | `short_term_predicted_return_quantile1_60d` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (60-day) return prediction, quantile 1. |
| 56 | `short_term_predicted_return_quantile5_20d` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (20-day) return prediction, quantile 5. |
| 57 | `short_term_regime2_adj_pred_20d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 20 days, adjusted for 2-phase regime, quantile 1. |
| 58 | `short_term_regime2_adj_pred_60d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 60 days, adjusted for 2-phase regime, quantile 1. |
| 59 | `short_term_regime2_phase_5d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day short horizon prediction adjusted for regime 2, quantile 1 (multi-model variant). |
| 60 | `short_term_regime4_adj_pred_20d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 20 days, adjusted for 4-phase regime, quantile 1. |
| 61 | `short_term_regime4_adjusted_pred_q1_5d` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-horizon (5-day) prediction adjusted for 4-phase regime, quantile 1. |
| 62 | `short_term_regime4_phase_60d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon prediction adjusted for regime 4, quantile 1 (multi-model variant). |
| 63 | `short_term_seasonal_20d_quantile1_pred_mfml` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon prediction adjusted for seasonal effects, quantile 1 (multi-model variant). |
| 64 | `short_term_seasonal_adj_pred_60d_bin1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 60 days, seasonally adjusted, quantile 1. |
| 65 | `short_term_seasonal_adjusted_pred_q1_5d` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-horizon (5-day) prediction adjusted for seasonal effects, quantile 1. |
| 66 | `alt2_short_hedge_5d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for second alternative short-term hedge, 5-day horizon, quantile 5. |
| 67 | `alt2_short_hedge_60d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for second alternative short-term hedge, 60-day horizon, quantile 5. |
| 68 | `alt2_short_term_hedge_signal_20d_q1` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Second alternative short-term hedge signal for 20-day horizon, quantile 1. |
| 69 | `alt2_short_term_hedge_signal_20d_q5` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Second alternative short-term hedge signal for 20-day horizon, quantile 5. |
| 70 | `alt2_short_term_hedge_signal_5d_q1` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Second alternative short-term hedge signal for 5-day horizon, quantile 1. |
| 71 | `alt2_short_term_hedge_signal_5d_q5` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Second alternative short-term hedge signal for 5-day horizon, quantile 5. |
| 72 | `alt2_short_term_hedge_signal_60d_q1` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Second alternative short-term hedge signal for 60-day horizon, quantile 1. |
| 73 | `alt2_short_term_hedge_signal_60d_q5` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Second alternative short-term hedge signal for 60-day horizon, quantile 5. |
| 74 | `alt3_short_hedge_20d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for third alternative short-term hedge, 20-day horizon, quantile 5. |
| 75 | `alt3_short_hedge_5d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for third alternative short-term hedge, 5-day horizon, quantile 5. |
| 76 | `alt3_short_hedge_60d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for third alternative short-term hedge, 60-day horizon, quantile 5. |
| 77 | `alt3_short_term_hedge_signal_20d_q1` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Third alternative short-term hedge signal for 20-day horizon, quantile 1. |
| 78 | `alt3_short_term_hedge_signal_20d_q5` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Third alternative short-term hedge signal for 20-day horizon, quantile 5. |
| 79 | `alt3_short_term_hedge_signal_5d_q1` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Third alternative short-term hedge signal for 5-day horizon, quantile 1. |
| 80 | `alt3_short_term_hedge_signal_60d_q1` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Third alternative short-term hedge signal for 60-day horizon, quantile 1. |
| 81 | `alt_long_hedge_120d_bin5_confidence_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Model confidence for alternative long-term hedge signal over 120 days, quantile 5, Mfmcr module. |
| 82 | `alt_long_hedge_60d_bin5_confidence_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Model confidence for alternative long-term hedge signal over 60 days, quantile 5, Mfmcr module. |
| 83 | `alt_long_term_hedge_signal_120d_bin1_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative long-term hedge signal over 120 days, quantile 1, Mfmcr module. |
| 84 | `alt_long_term_hedge_signal_120d_bin5_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative long-term hedge signal over 120 days, quantile 5, Mfmcr module. |
| 85 | `alt_long_term_hedge_signal_60d_bin1_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative long-term hedge signal over 60 days, quantile 1, Mfmcr module. |
| 86 | `alt_short_hedge_20d_bin5_confidence_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Model confidence for alternative short-term hedge signal over 20 days, quantile 5, Mfmcr module. |
| 87 | `alt_short_hedge_5d_bin5_confidence_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Model confidence for alternative short-term hedge signal over 5 days, quantile 5, Mfmcr module. |
| 88 | `alt_short_hedge_60d_bin5_confidence_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Model confidence for alternative short-term hedge signal over 60 days, quantile 5, Mfmcr module. |
| 89 | `alt_short_term_hedge_signal_20d_bin1_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal over 20 days, quantile 1, Mfmcr module. |
| 90 | `alt_short_term_hedge_signal_5d_bin1_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal over 5 days, quantile 1, Mfmcr module. |
| 91 | `alt_short_term_hedge_signal_5d_bin5_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal over 5 days, quantile 5, Mfmcr module. |
| 92 | `alt_short_term_hedge_signal_60d_bin1_mcr` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal over 60 days, quantile 1, Mfmcr module. |
| 93 | `alt_short_term_hedge_signal_60d_q5` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal for 60-day horizon, quantile 5. |
| 94 | `event_5d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, single-quantile return prediction using event-driven features. |
| 95 | `event_5d_single_quantile_pred_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, single-quantile return prediction using event-driven features (alternate model version). |
| 96 | `event_embedded_pred_5d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Prediction using event-based features for 5-day horizon, quantile 1. |
| 97 | `event_embedding_5d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day prediction using event-driven features, quantile 1. |
| 98 | `event_embedding_5d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day forward return forecast based on event-driven model inputs. |
| 99 | `event_embedding_quantile1_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 5-day, quantile 1 return using event-driven data embedding. |
| 100 | `event_embedding_signal_5d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Signal from event embedding over 5 days, quantile 1, Mfmcr module. |
| 101 | `long_hedge2_quantile1_r120_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate long-term, 120-day, quantile 1 hedge signal prediction. |
| 102 | `long_hedge2_quantile5_confidence_r120` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for alternate long-term, 120-day, quantile 5 hedge signal. |
| 103 | `long_hedge2_quantile5_confidence_r60` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for alternate long-term, 60-day, quantile 5 hedge signal. |
| 104 | `long_hedge2_quantile5_r120_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate long-term, 120-day, quantile 5 hedge signal prediction. |
| 105 | `long_hedge2_quantile5_r60_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate long-term, 60-day, quantile 5 hedge signal prediction. |
| 106 | `long_hedge3_120d_5bucket_class_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of long-horizon 120-day hedge signal classified into five quantile buckets (SolarEquiNox variant). |
| 107 | `long_hedge3_120d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of long-horizon 120-day hedge signal (regression output). |
| 108 | `long_hedge3_120d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of long-horizon 120-day hedge signal (regression output, SolarEquiNox variant). |
| 109 | `long_hedge3_60d_5bucket_class_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for third variant of long-term 60-day hedge signal (5-bucket classification). |
| 110 | `long_hedge3_60d_5bucket_class_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of long-term 60-day hedge signal classified into five quantile buckets (SolarEquiNox variant). |
| 111 | `long_hedge3_quantile5_pred_r60` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of long-term hedge signal, 60-day, 5-quantile classification prediction. |
| 112 | `long_hedge_120d_5quantile_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day, 5-quantile long-horizon hedge signal. |
| 113 | `long_hedge_120d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for long-horizon hedge signal, 120-day period, quantile 5. |
| 114 | `long_hedge_120d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 120-day long horizon hedge prediction, quantile 1 (low correlation signal). |
| 115 | `long_hedge_120d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day long horizon hedge quantile 5 prediction. |
| 116 | `long_hedge_120d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon 120-day hedge signal with low correlation to main predictions (regression output). |
| 117 | `long_hedge_60d_5bucket_class_confidence_solar` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for long-term 60-day hedge signal (5-bucket classification, SolarEquiNox variant). |
| 118 | `long_hedge_60d_5quantile_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day, 5-quantile long-horizon hedge signal. |
| 119 | `long_hedge_60d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for long-horizon hedge signal, 60-day period, quantile 5. |
| 120 | `long_hedge_60d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon 60-day hedge signal (regression output, SolarEquiNox variant). |
| 121 | `long_hedge_quantile1_r120_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term, 120-day, quantile 1 hedge signal prediction. |
| 122 | `long_hedge_quantile1_r60_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 1 hedge signal prediction. |
| 123 | `long_hedge_quantile1_r60_pred_mfm2` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 1 hedge signal prediction from Mfm2 module. |
| 124 | `long_hedge_quantile5_confidence_r120` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for long-term, 120-day, quantile 5 hedge signal. |
| 125 | `long_hedge_quantile5_confidence_r60` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for long-term, 60-day, quantile 5 hedge signal. |
| 126 | `long_hedge_quantile5_confidence_r60_mfm2` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for long-term, 60-day, quantile 5 hedge signal from Mfm2 module. |
| 127 | `long_hedge_quantile5_r120_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term, 120-day, quantile 5 hedge signal prediction. |
| 128 | `long_hedge_quantile5_r120_pred_mfm2` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term, 120-day, quantile 5 hedge signal prediction from Mfm2 module. |
| 129 | `long_hedge_quantile5_r60_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 5 hedge signal prediction. |
| 130 | `long_hedge_quantile5_r60_pred_mfm2` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 5 hedge signal prediction from Mfm2 module. |
| 131 | `long_pred_120d_regression_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon 120-day regression-based return prediction. |
| 132 | `long_pred_60d_5bucket_class_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for long-horizon 60-day 5-bucket classification prediction. |
| 133 | `long_pred_60d_5bucket_class_confidence_solar` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for long-horizon 60-day 5-bucket classification prediction (SolarEquiNox variant). |
| 134 | `long_pred_60d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for long-horizon prediction, 60-day period, quantile 5. |
| 135 | `long_pred_regime2_120d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon prediction adjusted for 2-phase regime, 120-day period, quantile 1. |
| 136 | `long_pred_regime2_120d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon 120-day regression prediction adjusted for two-phase market regime. |
| 137 | `long_pred_regime2_60d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon prediction adjusted for 2-phase regime, 60-day period, quantile 1. |
| 138 | `long_pred_regime2_60d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon 60-day regression prediction adjusted for two-phase market regime (SolarEquiNox variant). |
| 139 | `long_pred_regime4_120d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon prediction adjusted for 4-phase regime, 120-day period, quantile 1. |
| 140 | `long_pred_regime4_120d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon 120-day regression prediction adjusted for four-phase market regime. |
| 141 | `long_pred_regime4_60d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon prediction adjusted for 4-phase regime, 60-day period, quantile 1. |
| 142 | `long_pred_regime4_60d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon 60-day regression prediction adjusted for four-phase market regime. |
| 143 | `long_pred_seasonal_120d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon prediction adjusted for seasonal effects, 120-day period, quantile 1. |
| 144 | `long_pred_seasonal_60d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon prediction adjusted for seasonal effects, 60-day period, quantile 1. |
| 145 | `long_term_120d_5quantile_confidence_score` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day, 5-quantile long-horizon return prediction. |
| 146 | `long_term_120d_5quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (120-day) 5-quantile return prediction. |
| 147 | `long_term_120d_5quantile_pred_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (120-day) 5-quantile return prediction (alternate model version). |
| 148 | `long_term_120d_quantile1_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day long horizon return prediction, quantile 1. |
| 149 | `long_term_120d_quantile5_classification` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 120-day long-horizon return into one of five quantile buckets. |
| 150 | `long_term_120d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day long horizon quantile 5 prediction. |
| 151 | `long_term_120d_quantile5_confidence_score_2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 120-day long-term return. |
| 152 | `long_term_120d_quantile5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day long horizon return prediction, quantile 5. |
| 153 | `long_term_120d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted 120-day forward return using all available features. |
| 154 | `long_term_120d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day long-horizon regression-based return forecast. |
| 155 | `long_term_60d_5quantile_confidence_score` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day, 5-quantile long-horizon return prediction. |
| 156 | `long_term_60d_5quantile_pred_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (60-day) 5-quantile return prediction (alternate model version). |
| 157 | `long_term_60d_qtile5_class_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 60-day return into quantile 5 using long-horizon prediction model. |
| 158 | `long_term_60d_quantile1_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day long horizon return prediction, quantile 1. |
| 159 | `long_term_60d_quantile5_classification` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 60-day forward return into one of five quantile buckets for long-term prediction. |
| 160 | `long_term_60d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day long horizon quantile 5 prediction. |
| 161 | `long_term_60d_quantile5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day long horizon return prediction, quantile 5. |
| 162 | `long_term_60d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (60-day) regression-based return forecast. |
| 163 | `long_term_60d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (60-day) single-quantile return prediction. |
| 164 | `long_term_alternate_hedge3_quantile_120d` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative long-horizon (120-day) hedge signal variant 3, quantile bucket 5. |
| 165 | `long_term_forecast_regime2_120d_single_quantile` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon return prediction adjusted for 2-phase market regime over 120 days, single quantile output. |
| 166 | `long_term_hedge3_120d_quantile5_confidence` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for long-horizon (120-day) hedge signal variant 3 in quantile 5. |
| 167 | `long_term_hedge3_120d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 120-day long-horizon hedge3 signal. |
| 168 | `long_term_hedge3_60d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 60-day long-horizon hedge3 signal. |
| 169 | `long_term_hedge3_60d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day forward return forecast from the third variant of long-horizon hedge signal. |
| 170 | `long_term_hedge_120d_quantile5_classification` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Classification of 120-day long-horizon hedge signal into one of five quantile buckets. |
| 171 | `long_term_hedge_120d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 120-day long-horizon hedge signal. |
| 172 | `long_term_hedge_120d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day forward return forecast from the primary long-horizon hedge signal. |
| 173 | `long_term_hedge_60d_qtile5_class_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon 60-day hedge signal predicting membership in quantile 5, designed for low correlation with main signals. |
| 174 | `long_term_hedge_60d_quantile5_classification` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Classification of 60-day long-horizon hedge signal into one of five quantile buckets. |
| 175 | `long_term_hedge_pred_r60_q5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term hedge signal for 60-day horizon, 5-quantile classification prediction, designed for low correlation with main signal. |
| 176 | `long_term_hedge_signal_120d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon hedge signal for 120-day period, quantile 1. |
| 177 | `long_term_hedge_signal_120d_q5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon hedge signal for 120-day period, quantile 5. |
| 178 | `long_term_hedge_signal_60d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon hedge signal for 60-day period, quantile 1. |
| 179 | `long_term_hedge_signal_quantile_120d` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-horizon (120-day) hedge signal assigned to quantile bucket 5, designed for low correlation with main signals. |
| 180 | `long_term_hedge_variant3_quantile5_r60` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of long-horizon hedge signal, 5-quantile, over 60 days. |
| 181 | `long_term_pred_120d_bin5_confidence_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for long-term prediction over 120 days, quantile 5, Mfmcr module. |
| 182 | `long_term_pred_120d_bin5_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 120 days, quantile 5, Mfmcr module. |
| 183 | `long_term_pred_120d_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon return prediction for 120-day period, quantile 1. |
| 184 | `long_term_pred_120d_q5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon return prediction for 120-day period, quantile 5. |
| 185 | `long_term_pred_60d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 60 days, quantile 1, Mfmcr module. |
| 186 | `long_term_pred_60d_bin5_confidence_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for long-term prediction over 60 days, quantile 5, Mfmcr module. |
| 187 | `long_term_pred_60d_bin5_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 60 days, quantile 5, Mfmcr module. |
| 188 | `long_term_pred_60d_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon return prediction for 60-day period, quantile 1. |
| 189 | `long_term_pred_60d_q5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon return prediction for 60-day period, quantile 5. |
| 190 | `long_term_quantile1_r120_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 120-day, quantile 1 return prediction. |
| 191 | `long_term_quantile1_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 1 return prediction. |
| 192 | `long_term_quantile5_confidence_r120` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for long-term, 120-day, quantile 5 return prediction. |
| 193 | `long_term_quantile5_confidence_r120_2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-quantile long-horizon return prediction over 120 days. |
| 194 | `long_term_quantile5_confidence_r120_3` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for long-term 120-day, 5-quantile classification prediction. |
| 195 | `long_term_quantile5_confidence_r60` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for long-term, 60-day, quantile 5 return prediction. |
| 196 | `long_term_quantile5_r120_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 120-day, quantile 5 return prediction. |
| 197 | `long_term_quantile5_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 5 return prediction. |
| 198 | `long_term_regime2_120d_return_forecast` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (120-day) return prediction adjusted for 2-phase market regime. |
| 199 | `long_term_regime2_60d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day long-horizon return prediction with two-phase regime adjustment. |
| 200 | `long_term_regime2_adj_pred_120d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 120 days, adjusted for 2-phase regime, quantile 1, Mfmcr module. |
| 201 | `long_term_regime2_adj_pred_r60_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term return prediction for 60-day horizon, adjusted for 2-phase market regime, regression output. |
| 202 | `long_term_regime2_adjusted_return_pred_r60` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon return prediction over 60 days, adjusted for 2-phase market regime. |
| 203 | `long_term_regime2_phase_120d_quantile1_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day long horizon return prediction adjusted for regime 2, quantile 1. |
| 204 | `long_term_regime2_quantile1_r120_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 120-day, quantile 1 return forecast adjusted for 2-phase market regime. |
| 205 | `long_term_regime2_quantile1_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 1 return forecast adjusted for 2-phase market regime. |
| 206 | `long_term_regime2_quantile1_r60_pred_mfm2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 1 return forecast adjusted for 2-phase market regime from Mfm2 module. |
| 207 | `long_term_regime4_120d_return_forecast` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day long-horizon return prediction adjusted for 4-phase market regime. |
| 208 | `long_term_regime4_120d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (120-day) single-quantile return prediction adjusted for 4-phase market regime. |
| 209 | `long_term_regime4_60d_return_forecast` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day long-horizon return prediction adjusted for 4-phase market regime. |
| 210 | `long_term_regime4_60d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (60-day) single-quantile return prediction adjusted for 4-phase market regime. |
| 211 | `long_term_regime4_adj_pred_120d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 120 days, adjusted for 4-phase regime, quantile 1, Mfmcr module. |
| 212 | `long_term_regime4_adj_pred_60d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 60 days, adjusted for 4-phase regime, quantile 1, Mfmcr module. |
| 213 | `long_term_regime4_phase_120d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 120-day long horizon prediction adjusted for regime 4, quantile 1. |
| 214 | `long_term_regime4_phase_60d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day long horizon prediction adjusted for regime 4, quantile 1. |
| 215 | `long_term_regime4_quantile1_r120_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 120-day, quantile 1 return forecast adjusted for 4-phase market regime. |
| 216 | `long_term_regime4_quantile1_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 1 return forecast adjusted for 4-phase market regime. |
| 217 | `long_term_return_forecast_r120` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon single-quantile return prediction over 120 days. |
| 218 | `long_term_return_pred_r60_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term return prediction for a 60-day horizon, regression output. |
| 219 | `long_term_seasonal_120d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 120-day long horizon prediction adjusted for seasonal effects, quantile 1. |
| 220 | `long_term_seasonal_120d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day long-horizon return forecast incorporating seasonal or calendar effects. |
| 221 | `long_term_seasonal_120d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day long-horizon return forecast adjusted for seasonal and calendar effects. |
| 222 | `long_term_seasonal_60d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day long-horizon return forecast adjusted for seasonal and calendar effects. |
| 223 | `long_term_seasonal_60d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon (60-day) single-quantile return prediction adjusted for seasonal effects. |
| 224 | `long_term_seasonal_adj_pred_60d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Long-term prediction over 60 days, seasonally adjusted, quantile 1, Mfmcr module. |
| 225 | `long_term_seasonal_adjusted_return_forecast_120d` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon return prediction over 120 days, adjusted for seasonal effects. |
| 226 | `long_term_seasonal_adjusted_return_pred_r120` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-horizon return prediction adjusted for seasonal effects over 120 days. |
| 227 | `long_term_seasonal_quantile1_r120_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 120-day, quantile 1 return prediction adjusted for seasonal effects. |
| 228 | `long_term_seasonal_quantile1_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 1 return prediction adjusted for seasonal effects. |
| 229 | `long_term_seasonal_quantile1_r60_pred_mfm2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Long-term, 60-day, quantile 1 return prediction adjusted for seasonal effects from Mfm2 module. |
| 230 | `mid_term_hedge3_signal_60d_quantile1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Medium-term (60-day) hedge signal variant 3, quantile bucket 1. |
| 231 | `mid_term_hedge_signal_60d_quantile1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Medium-term (60-day) hedge signal, quantile bucket 1, designed for low correlation with main signals. |
| 232 | `mid_term_seasonal_adjusted_return_forecast_60d` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Medium-term (60-day) return forecast with seasonal effect adjustment. |
| 233 | `regime2_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day forward return forecast adjusted for 2-phase market regime effects. |
| 234 | `regime2_20d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day, single-quantile return prediction adjusted for 2-phase market regime. |
| 235 | `regime2_5d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day return prediction using two-phase market regime adjustment. |
| 236 | `regime2_5d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day regression prediction adjusted for two-phase market regime (SolarEquiNox variant). |
| 237 | `regime2_adj_pred_20d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Prediction adjusted for 2-phase market regime, 20-day horizon, quantile 1. |
| 238 | `regime2_adj_pred_5d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Prediction adjusted for 2-phase regime, 5-day horizon, quantile 1. |
| 239 | `regime2_adj_pred_r20_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Return prediction for 20-day horizon, adjusted for 2-phase market regime, regression output. |
| 240 | `regime2_adjusted_5d_return_quantile1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day return prediction in quantile 1, adjusted for 2-phase market regime. |
| 241 | `regime2_phase_20d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day prediction adjusted for regime 2 phase, quantile 1. |
| 242 | `regime2_phase_5d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day prediction adjusted for regime 2 phase, quantile 1. |
| 243 | `regime2_phase_signal_20d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Signal based on 2-phase regime embedding over 20 days, quantile 1, Mfmcr module. |
| 244 | `regime2_phase_signal_5d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Signal based on 2-phase regime embedding over 5 days, quantile 1, Mfmcr module. |
| 245 | `regime2_quantile1_r20_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 20-day, quantile 1 return using 2-phase market regime adjustment. |
| 246 | `regime2_quantile1_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 5-day, quantile 1 return using 2-phase market regime adjustment. |
| 247 | `regime4_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day forward return forecast adjusted for 4-phase market regime effects. |
| 248 | `regime4_20d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day, single-quantile return prediction adjusted for 4-phase market regime embedding. |
| 249 | `regime4_5d_5bucket_class_confidence_solar` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day four-phase regime adjusted 5-bucket classification (SolarEquiNox variant). |
| 250 | `regime4_5d_5quantile_confidence_score` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day, 5-quantile return prediction with 4-phase regime adjustment. |
| 251 | `regime4_5d_5quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, 5-quantile return prediction adjusted for 4-phase market regime embedding. |
| 252 | `regime4_5d_quantile5_classification` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 5-day return adjusted for 4-phase regime into one of five quantile buckets. |
| 253 | `regime4_5d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day forward return forecast adjusted for 4-phase market regime effects. |
| 254 | `regime4_5d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, single-quantile return prediction adjusted for 4-phase market regime embedding. |
| 255 | `regime4_5d_single_quantile_pred_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, single-quantile return prediction adjusted for 4-phase market regime embedding (alternate model version). |
| 256 | `regime4_adj_pred_20d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Prediction adjusted for 4-phase regime, 20-day horizon, quantile 1. |
| 257 | `regime4_adj_pred_5d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Prediction adjusted for 4-phase regime, 5-day horizon, quantile 1. |
| 258 | `regime4_adj_pred_5d_q5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Prediction adjusted for 4-phase regime, 5-day horizon, quantile 5. |
| 259 | `regime4_adj_pred_5d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 4-phase regime adjusted prediction, 5-day horizon, quantile 5. |
| 260 | `regime4_adj_pred_r20_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Return prediction for 20-day horizon, adjusted for 4-phase market regime, regression output. |
| 261 | `regime4_adjusted_5d_quantile5_confidence` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Confidence score for 5-day return prediction in quantile 5, adjusted for 4-phase market regime. |
| 262 | `regime4_adjusted_5d_return_quantile5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day return prediction in quantile 5, adjusted for 4-phase market regime. |
| 263 | `regime4_phase_5d_bin5_confidence_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for 4-phase regime signal over 5 days, quantile 5, Mfmcr module. |
| 264 | `regime4_phase_5d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day regime 4 phase quantile 5 prediction. |
| 265 | `regime4_phase_5d_quantile5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day prediction adjusted for regime 4 phase, quantile 5. |
| 266 | `regime4_phase_quantile5_pred_r5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-quantile return prediction adjusted for 4-phase market regime over 5 days. |
| 267 | `regime4_phase_return_pred_r20` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Return prediction adjusted for 4-phase market regime over 20 days. |
| 268 | `regime4_phase_signal_5d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Signal based on 4-phase regime embedding over 5 days, quantile 1, Mfmcr module. |
| 269 | `regime4_quantile1_r20_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 20-day, quantile 1 return using 4-phase market regime adjustment. |
| 270 | `regime4_quantile1_r20_pred_mfm2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 20-day, quantile 1 return using 4-phase market regime adjustment from Mfm2 module. |
| 271 | `regime4_quantile1_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 5-day, quantile 1 return using 4-phase market regime adjustment. |
| 272 | `regime4_quantile1_r5_pred_mfm2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 5-day, quantile 1 return using 4-phase market regime adjustment from Mfm2 module. |
| 273 | `regime4_quantile5_confidence_r5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for 5-day, quantile 5 return prediction using 4-phase market regime adjustment. |
| 274 | `regime4_quantile5_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 5-day, quantile 5 return using 4-phase market regime adjustment. |
| 275 | `seasonal_quantile1_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 5-day, quantile 1 return using seasonal effects. |
| 276 | `short_hedge2_20d_5bucket_class_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second variant of short-term 20-day hedge signal classified into five quantile buckets (SolarEquiNox variant). |
| 277 | `short_hedge2_20d_qtile5_confidence_score` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for secondary short-term hedge signal classifying 20-day return into quantile 5. |
| 278 | `short_hedge2_20d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second variant of short-term 20-day hedge signal (regression output). |
| 279 | `short_hedge2_5d_5bucket_class_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second variant of short-term 5-day hedge signal classified into five quantile buckets. |
| 280 | `short_hedge2_5d_5bucket_class_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second variant of short-term 5-day hedge signal classified into five quantile buckets (SolarEquiNox variant). |
| 281 | `short_hedge2_5d_5quantile_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for second variant of 5-day, 5-quantile short-term hedge signal. |
| 282 | `short_hedge2_5d_single_quantile_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second variant of short-term hedge signal for 5-day, single-quantile prediction. |
| 283 | `short_hedge2_60d_5bucket_class_confidence_solar` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for second variant of short-term 60-day hedge signal (5-bucket classification, SolarEquiNox variant). |
| 284 | `short_hedge2_60d_5bucket_class_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second variant of short-term 60-day hedge signal classified into five quantile buckets. |
| 285 | `short_hedge2_60d_5bucket_class_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second variant of short-term 60-day hedge signal classified into five quantile buckets (SolarEquiNox variant). |
| 286 | `short_hedge2_60d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second variant of short-term 60-day hedge signal (regression output, SolarEquiNox variant). |
| 287 | `short_hedge2_quantile1_r20_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate short-term, 20-day, quantile 1 hedge signal prediction. |
| 288 | `short_hedge2_quantile1_r5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate short-term, 5-day, quantile 1 hedge signal prediction. |
| 289 | `short_hedge2_quantile1_r60_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate short-term, 60-day, quantile 1 hedge signal prediction. |
| 290 | `short_hedge2_quantile5_confidence_r20` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for alternate short-term, 20-day, quantile 5 hedge signal. |
| 291 | `short_hedge2_quantile5_confidence_r5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for alternate short-term, 5-day, quantile 5 hedge signal. |
| 292 | `short_hedge2_quantile5_confidence_r60` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for alternate short-term, 60-day, quantile 5 hedge signal. |
| 293 | `short_hedge2_quantile5_confidence_r60_2` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for the second short-term hedge signal, 60-day, 5-quantile classification. |
| 294 | `short_hedge2_quantile5_pred_r20` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Second short-term hedge signal, 20-day, 5-quantile classification prediction. |
| 295 | `short_hedge2_quantile5_r20_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate short-term, 20-day, quantile 5 hedge signal prediction. |
| 296 | `short_hedge2_quantile5_r5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate short-term, 5-day, quantile 5 hedge signal prediction. |
| 297 | `short_hedge2_quantile5_r60_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Alternate short-term, 60-day, quantile 5 hedge signal prediction. |
| 298 | `short_hedge3_20d_5bucket_class_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for third variant of short-term 20-day hedge signal (5-bucket classification). |
| 299 | `short_hedge3_20d_5bucket_class_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term 20-day hedge signal classified into five quantile buckets. |
| 300 | `short_hedge3_20d_5quantile_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for third variant of 20-day short-term hedge signal (5-quantile). |
| 301 | `short_hedge3_20d_5quantile_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal for 20-day, 5-quantile prediction. |
| 302 | `short_hedge3_20d_single_quantile_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal for 20-day, single-quantile prediction. |
| 303 | `short_hedge3_5d_5quantile_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for the third variant of short-term hedge signal (5-day, 5-quantile). |
| 304 | `short_hedge3_5d_5quantile_confidence_score_m1` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for third variant of 5-day, 5-quantile short-term hedge signal (alternate model version). |
| 305 | `short_hedge3_5d_5quantile_pred_m1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal for 5-day, 5-quantile prediction (alternate model version). |
| 306 | `short_hedge3_5d_single_quantile_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal for 5-day, single-quantile prediction. |
| 307 | `short_hedge3_5d_single_quantile_pred_m1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal for 5-day, single-quantile prediction (alternate model version). |
| 308 | `short_hedge3_60d_5quantile_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for third variant of 60-day short-term hedge signal (5-quantile). |
| 309 | `short_hedge3_60d_5quantile_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal for 60-day, 5-quantile prediction. |
| 310 | `short_hedge3_60d_single_quantile_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal for 60-day, single-quantile prediction. |
| 311 | `short_hedge3_pred_r20_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal, 20-day horizon, regression output. |
| 312 | `short_hedge3_quantile5_pred_r60` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-term hedge signal, 60-day, 5-quantile classification prediction. |
| 313 | `short_hedge_20d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for short-term hedge signal, 20-day horizon, quantile 5. |
| 314 | `short_hedge_20d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon hedge prediction, quantile 1 (low correlation signal). |
| 315 | `short_hedge_20d_quantile5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon hedge prediction, quantile 5 (low correlation signal). |
| 316 | `short_hedge_5d_5bucket_class_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 5-day hedge signal classified into five quantile buckets (SolarEquiNox variant). |
| 317 | `short_hedge_5d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for short-term hedge signal, 5-day horizon, quantile 5. |
| 318 | `short_hedge_5d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day short horizon hedge quantile 5 prediction. |
| 319 | `short_hedge_5d_quantile5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day short horizon hedge prediction, quantile 5 (low correlation signal). |
| 320 | `short_hedge_5d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 5-day hedge signal (regression output, SolarEquiNox variant). |
| 321 | `short_hedge_60d_5bucket_class_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 60-day hedge signal classified into five quantile buckets (SolarEquiNox variant). |
| 322 | `short_hedge_60d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for short-term hedge signal, 60-day horizon, quantile 5. |
| 323 | `short_hedge_60d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon hedge prediction, quantile 1 (low correlation signal). |
| 324 | `short_hedge_60d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day short horizon hedge quantile 5 prediction. |
| 325 | `short_hedge_60d_quantile5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon hedge prediction, quantile 5 (low correlation signal). |
| 326 | `short_hedge_quantile1_r20_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term, 20-day, quantile 1 hedge signal prediction. |
| 327 | `short_hedge_quantile1_r5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 1 hedge signal prediction. |
| 328 | `short_hedge_quantile1_r5_pred_mfm2` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 1 hedge signal prediction from Mfm2 module. |
| 329 | `short_hedge_quantile1_r60_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term, 60-day, quantile 1 hedge signal prediction. |
| 330 | `short_hedge_quantile5_confidence_r20` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for short-term, 20-day, quantile 5 hedge signal. |
| 331 | `short_hedge_quantile5_confidence_r20_mfm2` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for short-term, 20-day, quantile 5 hedge signal from Mfm2 module. |
| 332 | `short_hedge_quantile5_confidence_r5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for short-term, 5-day, quantile 5 hedge signal. |
| 333 | `short_hedge_quantile5_confidence_r60` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for short-term, 60-day, quantile 5 hedge signal. |
| 334 | `short_hedge_quantile5_r20_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term, 20-day, quantile 5 hedge signal prediction. |
| 335 | `short_hedge_quantile5_r5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 5 hedge signal prediction. |
| 336 | `short_hedge_quantile5_r60_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term, 60-day, quantile 5 hedge signal prediction. |
| 337 | `short_horizon_hedge2_20d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 20-day short-horizon hedge2 signal. |
| 338 | `short_horizon_hedge2_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day forward return forecast from the second variant of short-horizon hedge signal. |
| 339 | `short_horizon_hedge2_5d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 5-day short-horizon hedge2 signal. |
| 340 | `short_horizon_hedge2_5d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day forward return forecast from the second variant of short-horizon hedge signal. |
| 341 | `short_horizon_hedge3_20d_quantile5_classification` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Classification of 20-day short-horizon hedge3 signal into one of five quantile buckets. |
| 342 | `short_horizon_hedge3_20d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 20-day short-horizon hedge3 signal. |
| 343 | `short_horizon_hedge3_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day forward return forecast from the third variant of short-horizon hedge signal. |
| 344 | `short_horizon_hedge3_5d_5quantile_signal` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal (third variant) for 5-day, 5-quantile classification. |
| 345 | `short_horizon_hedge3_5d_quantile5_classification` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Classification of 5-day hedge3 signal into one of five quantile buckets for short-term horizon. |
| 346 | `short_horizon_hedge3_5d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 5-day short-horizon hedge3 signal. |
| 347 | `short_horizon_hedge3_5d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day forward return forecast from the third variant of short-horizon hedge signal. |
| 348 | `short_horizon_hedge3_60d_quantile5_classification` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Classification of 60-day short-horizon hedge3 signal into one of five quantile buckets. |
| 349 | `short_horizon_hedge3_60d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 60-day short-horizon hedge3 signal. |
| 350 | `short_horizon_hedge3_60d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day forward return forecast from the third variant of short-horizon hedge signal. |
| 351 | `short_horizon_hedge_20d_quantile5_classification` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Classification of 20-day short-horizon hedge signal into one of five quantile buckets. |
| 352 | `short_horizon_hedge_20d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 20-day short-horizon hedge signal. |
| 353 | `short_horizon_hedge_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day forward return forecast from the primary short-horizon hedge signal. |
| 354 | `short_horizon_hedge_5d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 5-day short-horizon hedge signal. |
| 355 | `short_horizon_hedge_60d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 60-day short-horizon hedge signal. |
| 356 | `short_horizon_hedge_60d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day forward return forecast from the primary short-horizon hedge signal. |
| 357 | `short_pred_20d_5bucket_class_pred_solar` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term 20-day return classification into five quantile buckets (SolarEquiNox variant). |
| 358 | `short_pred_20d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for short-term prediction, 20-day horizon, quantile 5. |
| 359 | `short_pred_5d_5bucket_class_confidence` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day short-term 5-bucket classification prediction. |
| 360 | `short_pred_5d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for short-term prediction, 5-day horizon, quantile 5. |
| 361 | `short_pred_60d_5bucket_class_confidence_solar` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day short-term 5-bucket classification prediction (SolarEquiNox variant). |
| 362 | `short_pred_60d_q5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for short-term prediction, 60-day period, quantile 5. |
| 363 | `short_pred_60d_regression_pred_solar` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term 60-day regression-based return prediction (SolarEquiNox variant). |
| 364 | `short_pred_regime2_20d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction adjusted for 2-phase regime, 20-day horizon, quantile 1. |
| 365 | `short_pred_regime2_20d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 20-day regression prediction adjusted for two-phase market regime. |
| 366 | `short_pred_regime2_5d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction adjusted for 2-phase regime, 5-day horizon, quantile 1. |
| 367 | `short_pred_regime2_5d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 5-day regression prediction adjusted for two-phase market regime (SolarEquiNox variant). |
| 368 | `short_pred_regime2_60d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction adjusted for 2-phase regime, 60-day horizon, quantile 1. |
| 369 | `short_pred_regime2_60d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 60-day regression prediction adjusted for two-phase market regime (SolarEquiNox variant). |
| 370 | `short_pred_regime4_20d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 20-day regression prediction adjusted for four-phase market regime. |
| 371 | `short_pred_regime4_5d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction adjusted for 4-phase regime, 5-day horizon, quantile 1. |
| 372 | `short_pred_regime4_5d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 5-day regression prediction adjusted for four-phase market regime. |
| 373 | `short_pred_regime4_60d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction adjusted for 4-phase regime, 60-day horizon, quantile 1. |
| 374 | `short_pred_seasonal_20d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction adjusted for seasonal effects, 20-day horizon, quantile 1. |
| 375 | `short_pred_seasonal_5d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 5-day regression prediction adjusted for seasonal effects (SolarEquiNox variant). |
| 376 | `short_pred_seasonal_60d_regression_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 60-day regression prediction adjusted for seasonal effects. |
| 377 | `short_pred_seasonal_60d_regression_pred_solar` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term 60-day regression prediction adjusted for seasonal effects (SolarEquiNox variant). |
| 378 | `short_term_20d_5quantile_confidence_score` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day, 5-quantile short-term return prediction. |
| 379 | `short_term_20d_5quantile_confidence_score_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day, 5-quantile short-term return prediction (alternate model version). |
| 380 | `short_term_20d_5quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (20-day) 5-quantile return prediction. |
| 381 | `short_term_20d_5quantile_pred_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (20-day) 5-quantile return prediction (alternate model version). |
| 382 | `short_term_20d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon prediction, quantile 1. |
| 383 | `short_term_20d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day short horizon quantile 5 prediction. |
| 384 | `short_term_20d_quantile5_confidence_score_2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 20-day short-term return. |
| 385 | `short_term_20d_quantile5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon prediction, quantile 5. |
| 386 | `short_term_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (20-day) regression-based return forecast. |
| 387 | `short_term_20d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (20-day) single-quantile return prediction. |
| 388 | `short_term_5d_5bucket_class_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 5-day short-term return into one of five quantile buckets. |
| 389 | `short_term_5d_5quantile_confidence_score` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day short-term return prediction in 5 quantile classification. |
| 390 | `short_term_5d_qtile5_class_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 5-day return into quantile 5 using short-term prediction model. |
| 391 | `short_term_5d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day short horizon prediction, quantile 1. |
| 392 | `short_term_5d_quantile5_classification` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 5-day short-horizon return into one of five quantile buckets. |
| 393 | `short_term_5d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day short horizon quantile 5 prediction. |
| 394 | `short_term_5d_quantile5_confidence_score_2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 5-day short-term return. |
| 395 | `short_term_5d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (5-day) regression-based return forecast. |
| 396 | `short_term_5d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (5-day) single-quantile return prediction. |
| 397 | `short_term_5d_single_quantile_pred_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (5-day) single-quantile return prediction (alternate model version). |
| 398 | `short_term_60d_5bucket_class_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 60-day short-term return into one of five quantile buckets. |
| 399 | `short_term_60d_5quantile_confidence_score` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day, 5-quantile short-term return prediction. |
| 400 | `short_term_60d_qtile5_class_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 60-day return into quantile 5 using short-term prediction model. |
| 401 | `short_term_60d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon prediction, quantile 1. |
| 402 | `short_term_60d_quantile5_classification` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 60-day short-horizon return into one of five quantile buckets. |
| 403 | `short_term_60d_quantile5_confidence_score` | MATRIX | 0.587 | 风险与质量 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day short horizon quantile 5 prediction. |
| 404 | `short_term_60d_quantile5_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon prediction, quantile 5. |
| 405 | `short_term_60d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (60-day) single-quantile return prediction. |
| 406 | `short_term_60d_single_quantile_pred_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (60-day) single-quantile return prediction (alternate model version). |
| 407 | `short_term_hedge2_20d_quantile5_confidence` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for short-term (20-day) hedge signal variant 2 in quantile 5. |
| 408 | `short_term_hedge2_pred_r60_q1` | MATRIX | 0.587 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Alternative short-term hedge signal for 60-day horizon, regression output, designed for low correlation with main signal. |
| 409 | `short_term_hedge3_60d_quantile5_confidence` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for short-term (60-day) hedge signal variant 3 in quantile 5. |
| 410 | `short_term_hedge3_signal_60d_quantile1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term (60-day) hedge signal variant 3, assigned to quantile bucket 1. |
| 411 | `short_term_hedge_60d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term 60-day return forecast designed to be uncorrelated with main signals. |
| 412 | `short_term_hedge_signal_20d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term hedge signal for 20-day horizon, quantile 1. |
| 413 | `short_term_hedge_signal_20d_q5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term hedge signal for 20-day horizon, quantile 5. |
| 414 | `short_term_hedge_signal_5d_q1` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term hedge signal for 5-day horizon, quantile 1. |
| 415 | `short_term_hedge_signal_5d_q5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term hedge signal for 5-day horizon, quantile 5. |
| 416 | `short_term_hedge_signal_60d_q5` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term hedge signal for 60-day horizon, quantile 5. |
| 417 | `short_term_hedge_variant3_quantile5_r20` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-horizon hedge signal, 5-quantile, over 20 days. |
| 418 | `short_term_hedge_variant3_quantile5_r60` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Third variant of short-horizon hedge signal, 5-quantile, over 60 days. |
| 419 | `short_term_pred_20d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 20 days, quantile 1, Mfmcr module. |
| 420 | `short_term_pred_20d_bin5_confidence_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for short-term prediction over 20 days, quantile 5, Mfmcr module. |
| 421 | `short_term_pred_20d_bin5_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 20 days, quantile 5, Mfmcr module. |
| 422 | `short_term_pred_20d_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction for 20-day period, quantile 1. |
| 423 | `short_term_pred_20d_q5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction for 20-day period, quantile 5. |
| 424 | `short_term_pred_5d_bin5_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 5 days, quantile 5, Mfmcr module. |
| 425 | `short_term_pred_5d_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction for 5-day period, quantile 1. |
| 426 | `short_term_pred_5d_q5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction for 5-day period, quantile 5. |
| 427 | `short_term_pred_60d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 60 days, quantile 1, Mfmcr module. |
| 428 | `short_term_pred_60d_bin5_confidence_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Model confidence for short-term prediction over 60 days, quantile 5, Mfmcr module. |
| 429 | `short_term_pred_60d_bin5_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 60 days, quantile 5, Mfmcr module. |
| 430 | `short_term_pred_60d_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction for 60-day period, quantile 1. |
| 431 | `short_term_pred_60d_q5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction for 60-day period, quantile 5. |
| 432 | `short_term_quantile1_r20_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 20-day, quantile 1 return prediction. |
| 433 | `short_term_quantile1_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 1 return prediction. |
| 434 | `short_term_quantile1_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 60-day, quantile 1 return prediction. |
| 435 | `short_term_quantile5_confidence_r20` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for short-term, 20-day, quantile 5 return prediction. |
| 436 | `short_term_quantile5_confidence_r5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for short-term, 5-day, quantile 5 return prediction. |
| 437 | `short_term_quantile5_confidence_r60` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for short-term, 60-day, quantile 5 return prediction. |
| 438 | `short_term_quantile5_r20_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 20-day, quantile 5 return prediction. |
| 439 | `short_term_quantile5_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 5 return prediction. |
| 440 | `short_term_quantile5_r5_pred_mfm2` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 5 return prediction from Mfm2 module. |
| 441 | `short_term_quantile5_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 60-day, quantile 5 return prediction. |
| 442 | `short_term_regime2_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day short-horizon return forecast adjusted for 2-phase market regime. |
| 443 | `short_term_regime2_20d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day, single-quantile short-term return prediction adjusted for 2-phase market regime. |
| 444 | `short_term_regime2_5d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, single-quantile short-term return prediction adjusted for 2-phase market regime. |
| 445 | `short_term_regime2_5d_single_quantile_pred_m1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, single-quantile short-term return prediction adjusted for 2-phase market regime (alternate model version). |
| 446 | `short_term_regime2_60d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (60-day) single-quantile return prediction adjusted for 2-phase market regime. |
| 447 | `short_term_regime2_adj_pred_20d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 20 days, adjusted for 2-phase regime, quantile 1, Mfmcr module. |
| 448 | `short_term_regime2_adj_pred_60d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 60 days, adjusted for 2-phase regime, quantile 1, Mfmcr module. |
| 449 | `short_term_regime2_adj_return_pred_r60_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term return prediction over 60 days, adjusted for 2-phase market regime, regression output. |
| 450 | `short_term_regime2_adjusted_return_pred_r5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction over 5 days, adjusted for 2-phase market regime. |
| 451 | `short_term_regime2_phase_20d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon prediction adjusted for regime 2, quantile 1. |
| 452 | `short_term_regime2_phase_5d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day short horizon prediction adjusted for regime 2, quantile 1. |
| 453 | `short_term_regime2_phase_60d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon prediction adjusted for regime 2, quantile 1. |
| 454 | `short_term_regime2_quantile1_r20_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 20-day, quantile 1 return forecast adjusted for 2-phase market regime. |
| 455 | `short_term_regime2_quantile1_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 1 return forecast adjusted for 2-phase market regime. |
| 456 | `short_term_regime2_quantile1_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 60-day, quantile 1 return forecast adjusted for 2-phase market regime. |
| 457 | `short_term_regime4_20d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day short-term return prediction adjusted for four-phase market regime. |
| 458 | `short_term_regime4_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day short-horizon return forecast adjusted for 4-phase market regime. |
| 459 | `short_term_regime4_20d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day, single-quantile short-term return prediction adjusted for 4-phase market regime. |
| 460 | `short_term_regime4_5d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day short-horizon return forecast adjusted for 4-phase market regime. |
| 461 | `short_term_regime4_5d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, single-quantile short-term return prediction adjusted for 4-phase market regime. |
| 462 | `short_term_regime4_60d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day short-term return prediction adjusted for four-phase market regime. |
| 463 | `short_term_regime4_60d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day short-horizon return forecast adjusted for 4-phase market regime. |
| 464 | `short_term_regime4_adj_pred_20d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 20 days, adjusted for 4-phase regime, quantile 1, Mfmcr module. |
| 465 | `short_term_regime4_adj_pred_5d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 5 days, adjusted for 4-phase regime, quantile 1, Mfmcr module. |
| 466 | `short_term_regime4_adjusted_return_60d` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term (60-day) return prediction adjusted for 4-phase market regime. |
| 467 | `short_term_regime4_adjusted_return_pred_r60` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction over 60 days, adjusted for 4-phase market regime. |
| 468 | `short_term_regime4_phase_20d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon prediction adjusted for regime 4, quantile 1. |
| 469 | `short_term_regime4_phase_5d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day short horizon prediction adjusted for regime 4, quantile 1. |
| 470 | `short_term_regime4_phase_60d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon prediction adjusted for regime 4, quantile 1. |
| 471 | `short_term_regime4_quantile1_r20_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 20-day, quantile 1 return forecast adjusted for 4-phase market regime. |
| 472 | `short_term_regime4_quantile1_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 1 return forecast adjusted for 4-phase market regime. |
| 473 | `short_term_regime4_quantile1_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 60-day, quantile 1 return forecast adjusted for 4-phase market regime. |
| 474 | `short_term_return_60d_quantile5_confidence` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for short-term (60-day) return prediction in quantile 5. |
| 475 | `short_term_return_forecast_r5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon single-quantile return prediction over 5 days. |
| 476 | `short_term_return_pred_r20_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term return prediction for a 20-day horizon, regression output. |
| 477 | `short_term_return_quantile5_confidence_r5` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-quantile short-term return prediction over 5 days. |
| 478 | `short_term_seasonal_20d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 20-day short horizon prediction adjusted for seasonal effects, quantile 1. |
| 479 | `short_term_seasonal_20d_regression_prediction` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day short-horizon return forecast adjusted for seasonal and calendar effects. |
| 480 | `short_term_seasonal_20d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day, single-quantile short-term return prediction adjusted for seasonal effects. |
| 481 | `short_term_seasonal_5d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 5-day short horizon prediction adjusted for seasonal effects, quantile 1. |
| 482 | `short_term_seasonal_5d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day short-term return forecast incorporating seasonal or calendar effects. |
| 483 | `short_term_seasonal_5d_single_quantile_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, single-quantile short-term return prediction adjusted for seasonal effects. |
| 484 | `short_term_seasonal_60d_quantile1_pred` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | 60-day short horizon prediction adjusted for seasonal effects, quantile 1. |
| 485 | `short_term_seasonal_60d_regress_return_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day short-term return forecast incorporating seasonal or calendar effects. |
| 486 | `short_term_seasonal_adj_pred_20d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 20 days, seasonally adjusted, quantile 1, Mfmcr module. |
| 487 | `short_term_seasonal_adj_pred_5d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 5 days, seasonally adjusted, quantile 1, Mfmcr module. |
| 488 | `short_term_seasonal_adj_pred_60d_bin1_mcr` | MATRIX | 0.587 | 其他 | 0 | — | — | — | UNUSABLE | Short-term prediction over 60 days, seasonally adjusted, quantile 1, Mfmcr module. |
| 489 | `short_term_seasonal_adj_pred_r5_q1` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term return prediction for 5-day horizon, adjusted for seasonal effects, regression output. |
| 490 | `short_term_seasonal_adjusted_return_20d` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon (20-day) return prediction incorporating seasonal adjustments. |
| 491 | `short_term_seasonal_adjusted_return_pred_r60` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-horizon return prediction adjusted for seasonal effects over 60 days. |
| 492 | `short_term_seasonal_quantile1_r20_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 20-day, quantile 1 return prediction adjusted for seasonal effects. |
| 493 | `short_term_seasonal_quantile1_r5_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 5-day, quantile 1 return prediction adjusted for seasonal effects. |
| 494 | `short_term_seasonal_quantile1_r60_pred` | MATRIX | 0.587 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term, 60-day, quantile 1 return prediction adjusted for seasonal effects. |
| 495 | `mid_term_price_volume_quantile5_confidence_60d` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for price-volume based prediction over 60 days, quantile 5. |
| 496 | `price_volume_20d_5quantile_confidence_score` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day, 5-quantile return prediction using price-volume features. |
| 497 | `price_volume_20d_5quantile_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day, 5-quantile return prediction using price-volume features. |
| 498 | `price_volume_20d_bin5_confidence_mcr` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for price-volume signal over 20 days, quantile 5, Mfmcr module. |
| 499 | `price_volume_20d_quantile5_classification` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 20-day price-volume based return into one of five quantile buckets. |
| 500 | `price_volume_20d_regression_prediction` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day forward return forecast using price and volume features. |
| 501 | `price_volume_20d_single_quantile_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day, single-quantile return prediction using price-volume features. |
| 502 | `price_volume_5d_5quantile_confidence_score` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day, 5-quantile return prediction using price-volume features. |
| 503 | `price_volume_5d_5quantile_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, 5-quantile return prediction using price-volume features. |
| 504 | `price_volume_5d_5quantile_pred_m1` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day, 5-quantile return prediction using price-volume features (alternate model version). |
| 505 | `price_volume_5d_bin5_confidence_mcr` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for price-volume signal over 5 days, quantile 5, Mfmcr module. |
| 506 | `price_volume_5d_quantile5_classification` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 5-day price-volume based return into one of five quantile buckets. |
| 507 | `price_volume_5d_quantile5_confidence_score` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 5-day price-volume based return. |
| 508 | `price_volume_5d_regression_prediction` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day forward return forecast using price and volume features. |
| 509 | `price_volume_5d_single_quantile_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day single-quantile return prediction using price-volume features. |
| 510 | `price_volume_60d_5quantile_confidence_score` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day, 5-quantile return prediction using price-volume features. |
| 511 | `price_volume_60d_5quantile_pred_m1` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day, 5-quantile return prediction using price-volume features (alternate model version). |
| 512 | `price_volume_60d_bin5_confidence_mcr` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for price-volume signal over 60 days, quantile 5, Mfmcr module. |
| 513 | `price_volume_60d_qtile5_class_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 60-day return into quantile 5 using price-volume features. |
| 514 | `price_volume_60d_qtile5_confidence_score` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for classifying 60-day return into quantile 5 using price-volume features. |
| 515 | `price_volume_60d_quantile5_classification` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 60-day price-volume based return into one of five quantile buckets. |
| 516 | `price_volume_60d_regress_return_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted 60-day forward return using price and volume data. |
| 517 | `price_volume_60d_regression_prediction` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day forward return forecast based on price-volume model inputs. |
| 518 | `price_volume_based_return_pred_r20` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term return prediction using price-volume data over 20 days. |
| 519 | `price_volume_based_return_pred_r5` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term return prediction using price-volume data over 5 days. |
| 520 | `price_volume_pred_r20_q1` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Return prediction for 20-day horizon using price-volume data, regression output. |
| 521 | `price_volume_pred_r60_q1` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Return prediction for 60-day horizon using price-volume data, regression output. |
| 522 | `price_volume_quantile1_r20_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 20-day, quantile 1 return using price-volume data. |
| 523 | `price_volume_quantile1_r5_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 5-day, quantile 1 return using price-volume data. |
| 524 | `price_volume_quantile1_r60_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 60-day, quantile 1 return using price-volume data. |
| 525 | `price_volume_quantile5_confidence_r20` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for 20-day, quantile 5 return prediction using price-volume data. |
| 526 | `price_volume_quantile5_confidence_r20_mfm2` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for 20-day, quantile 5 return prediction using price-volume data from Mfm2 module. |
| 527 | `price_volume_quantile5_confidence_r5` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for 5-day, quantile 5 return prediction using price-volume data. |
| 528 | `price_volume_quantile5_confidence_r60` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for 60-day, quantile 5 return prediction using price-volume data. |
| 529 | `price_volume_quantile5_confidence_r60_mfm2` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for 60-day, quantile 5 return prediction using price-volume data from Mfm2 module. |
| 530 | `price_volume_quantile5_pred_r20` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-volume based 20-day, 5-quantile classification prediction. |
| 531 | `price_volume_quantile5_r20_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 20-day, quantile 5 return using price-volume data. |
| 532 | `price_volume_quantile5_r5_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 5-day, quantile 5 return using price-volume data. |
| 533 | `price_volume_quantile5_r60_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prediction for 60-day, quantile 5 return using price-volume data. |
| 534 | `price_volume_quantile5_return_pred_r20` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-quantile return prediction using price-volume data over 20 days. |
| 535 | `price_volume_signal_5d_bin5` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Signal from price-volume data over 5 days, quantile 5. |
| 536 | `price_volume_signal_5d_bin5_mcr` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Signal from price-volume data over 5 days, quantile 5, Mfmcr module. |
| 537 | `price_volume_signal_60d_bin1_mcr` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Signal from price-volume data over 60 days, quantile 1, Mfmcr module. |
| 538 | `price_volume_signal_60d_bin5_mcr` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Signal from price-volume data over 60 days, quantile 5, Mfmcr module. |
| 539 | `pv_20d_5bucket_class_confidence` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day price-volume based 5-bucket classification. |
| 540 | `pv_20d_5bucket_class_confidence_solar` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day price-volume based 5-bucket classification (SolarEquiNox variant). |
| 541 | `pv_20d_q1` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-volume based prediction for 20-day horizon, quantile 1. |
| 542 | `pv_20d_q5` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-volume based prediction for 20-day horizon, quantile 5. |
| 543 | `pv_20d_q5_confidence_score` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for price-volume based prediction, 20-day horizon, quantile 5. |
| 544 | `pv_20d_quantile1_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day prediction using price-volume features, quantile 1. |
| 545 | `pv_20d_quantile5_confidence_score_mfml` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 20-day price-volume quantile 5 prediction (multi-model variant). |
| 546 | `pv_20d_quantile5_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day prediction using price-volume features, quantile 5. |
| 547 | `pv_20d_quantile5_pred_mfml` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day prediction using price-volume features, quantile 5 (multi-model variant). |
| 548 | `pv_5d_5bucket_class_confidence` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day price-volume based 5-bucket classification. |
| 549 | `pv_5d_q1` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-volume based prediction for 5-day horizon, quantile 1. |
| 550 | `pv_5d_q5` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-volume based prediction for 5-day horizon, quantile 5. |
| 551 | `pv_5d_q5_confidence_score` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for price-volume based prediction, 5-day horizon, quantile 5. |
| 552 | `pv_5d_quantile1_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day prediction using price-volume features, quantile 1. |
| 553 | `pv_5d_quantile5_confidence_score` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day price-volume quantile 5 prediction. |
| 554 | `pv_5d_quantile5_confidence_score_mfml` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 5-day price-volume quantile 5 prediction (multi-model variant). |
| 555 | `pv_5d_quantile5_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day prediction using price-volume features, quantile 5. |
| 556 | `pv_60d_5bucket_class_confidence` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day price-volume based 5-bucket classification. |
| 557 | `pv_60d_5bucket_class_confidence_solar` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day price-volume based 5-bucket classification (SolarEquiNox variant). |
| 558 | `pv_60d_q1` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-volume based prediction for 60-day horizon, quantile 1. |
| 559 | `pv_60d_q5` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-volume based prediction for 60-day horizon, quantile 5. |
| 560 | `pv_60d_quantile1_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day prediction using price-volume features, quantile 1. |
| 561 | `pv_60d_quantile1_pred_mfml` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day prediction using price-volume features, quantile 1 (multi-model variant). |
| 562 | `pv_60d_quantile5_pred` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day prediction using price-volume features, quantile 5. |
| 563 | `pv_60d_quantile5_pred_mfml` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day prediction using price-volume features, quantile 5 (multi-model variant). |
| 564 | `short_term_price_volume_based_return_5d` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term (5-day) return forecast using price and volume data. |
| 565 | `short_term_price_volume_return_quantile1_20d` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term (20-day) return prediction based on price-volume data, quantile 1. |
| 566 | `short_term_price_volume_return_quantile1_5d` | MATRIX | 0.539 | 价量与波动 | 0 | — | — | — | UNUSABLE | Short-term (5-day) return prediction based on price-volume data, quantile 1. |
| 567 | `analyst_120d_5bucket_class_confidence` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day analyst-based 5-bucket classification. |
| 568 | `analyst_120d_5bucket_class_pred_solar` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 120-day forward return classification into five buckets using analyst-derived features (SolarEquiNox variant). |
| 569 | `analyst_120d_5quantile_confidence_score` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day, 5-quantile return prediction using analyst data. |
| 570 | `analyst_120d_5quantile_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 120-day, 5-quantile return prediction using analyst data. |
| 571 | `analyst_120d_5quantile_pred_m1` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 120-day, 5-quantile return prediction using analyst data (alternate model version). |
| 572 | `analyst_120d_bin5_confidence_mcr` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence for analyst-based signal over 120 days, quantile 5, Mfmcr module. |
| 573 | `analyst_120d_quantile5_confidence_score` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day analyst-based quantile 5 prediction. |
| 574 | `analyst_120d_quantile5_confidence_score_mfml` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day analyst-based quantile 5 prediction (multi-model variant). |
| 575 | `analyst_120d_regression_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regression-based 120-day forward return prediction using analyst data. |
| 576 | `analyst_120d_single_quantile_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 120-day, single-quantile return prediction using analyst data. |
| 577 | `analyst_60d_5bucket_class_pred_solar` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 60-day forward return classification into five buckets using analyst-derived features (SolarEquiNox variant). |
| 578 | `analyst_60d_5quantile_confidence_score` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day, 5-quantile return prediction using analyst data. |
| 579 | `analyst_60d_5quantile_confidence_score_m1` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day, 5-quantile return prediction using analyst data (alternate model version). |
| 580 | `analyst_60d_5quantile_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 60-day, 5-quantile return prediction using analyst data. |
| 581 | `analyst_60d_bin5_confidence_mcr` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence for analyst-based signal over 60 days, quantile 5, Mfmcr module. |
| 582 | `analyst_60d_qtile5_class_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Classification of 60-day return into quantile 5 using analyst-based features. |
| 583 | `analyst_60d_quantile1_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 60-day prediction using analyst-derived features, quantile 1. |
| 584 | `analyst_60d_quantile1_pred_mfml` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 60-day prediction using analyst-derived features, quantile 1 (multi-model variant). |
| 585 | `analyst_60d_quantile5_confidence_score` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day analyst-based quantile 5 prediction. |
| 586 | `analyst_60d_quantile5_confidence_score_mfml` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day analyst-based quantile 5 prediction (multi-model variant). |
| 587 | `analyst_60d_quantile5_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 60-day prediction using analyst-derived features, quantile 5. |
| 588 | `analyst_60d_regression_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Regression-based 60-day forward return prediction using analyst-derived features. |
| 589 | `analyst_60d_single_quantile_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 60-day, single-quantile return prediction using analyst data. |
| 590 | `analyst_based_120d_quantile5_confidence_score` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 120-day analyst-based return. |
| 591 | `analyst_based_120d_regression_prediction` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 120-day forward return forecast derived from analyst data inputs. |
| 592 | `analyst_based_60d_quantile5_confidence_score` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 60-day analyst-based return. |
| 593 | `analyst_based_60d_regression_prediction` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | 60-day forward return forecast derived from analyst data. |
| 594 | `analyst_based_pred_120d_q1` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-derived prediction for 120-day horizon, quantile 1. |
| 595 | `analyst_based_pred_120d_q5` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-derived prediction for 120-day horizon, quantile 5. |
| 596 | `analyst_based_pred_60d_q1` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-derived prediction for 60-day horizon, quantile 1. |
| 597 | `analyst_based_pred_60d_q5` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-derived prediction for 60-day horizon, quantile 5. |
| 598 | `analyst_pred_120d_q5_confidence_score` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for analyst-based prediction, 120-day horizon, quantile 5. |
| 599 | `analyst_pred_60d_q5_confidence_score` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for analyst-based prediction, 60-day horizon, quantile 5. |
| 600 | `analyst_quantile1_r120_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Prediction for 120-day, quantile 1 return using analyst data. |
| 601 | `analyst_quantile1_r60_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Prediction for 60-day, quantile 1 return using analyst data. |
| 602 | `analyst_quantile5_confidence_r120` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence for 120-day, quantile 5 return prediction from analyst data. |
| 603 | `analyst_quantile5_confidence_r60` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence for 60-day, quantile 5 return prediction from analyst data. |
| 604 | `analyst_quantile5_r120_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Prediction for 120-day, quantile 5 return using analyst data. |
| 605 | `analyst_quantile5_r120_pred_mfm2` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Prediction for 120-day, quantile 5 return using analyst data from Mfm2 module. |
| 606 | `analyst_quantile5_r60_pred` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Prediction for 60-day, quantile 5 return using analyst data. |
| 607 | `analyst_signal_120d_bin1_mcr` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based signal over 120 days, quantile 1, Mfmcr module. |
| 608 | `analyst_signal_120d_bin5_mcr` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based signal over 120 days, quantile 5, Mfmcr module. |
| 609 | `analyst_signal_120d_quantile1` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based return prediction for 120-day horizon, quantile 1. |
| 610 | `analyst_signal_120d_quantile5` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based return prediction for 120-day horizon, quantile 5. |
| 611 | `analyst_signal_60d_bin1_mcr` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based signal over 60 days, quantile 1, Mfmcr module. |
| 612 | `analyst_signal_60d_bin5_mcr` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based signal over 60 days, quantile 5, Mfmcr module. |
| 613 | `analyst_signal_60d_quantile5` | MATRIX | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based return prediction for 60-day horizon, quantile 5. |
| 614 | `alt_fundamental_pred_120d_q5` | MATRIX | 0.424 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Alternative fundamental-based prediction for 120-day horizon, quantile 5. |
| 615 | `alt_fundamental_pred_60d_q1` | MATRIX | 0.424 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Alternative fundamental-based prediction for 60-day horizon, quantile 1. |
| 616 | `alt_fundamental_pred_60d_q5` | MATRIX | 0.424 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Alternative fundamental-based prediction for 60-day horizon, quantile 5. |
| 617 | `alt_fundamental_pred_60d_q5_confidence_score` | MATRIX | 0.424 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Model confidence score for alternative fundamental-based prediction, 60-day horizon, quantile 5. |
| 618 | `fundamental2_120d_5quantile_pred_m1` | MATRIX | 0.424 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day, 5-quantile return prediction using secondary set of fundamental features (alternate model version). |
| 619 | `fundamental2_based_return_60d_quantile1` | MATRIX | 0.424 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day return prediction using alternate fundamental data fields, quantile 1. |
| 620 | `fundamental2_quantile5_pred_r60` | MATRIX | 0.424 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Second set of fundamental data-based 60-day, 5-quantile classification prediction. |
| 621 | `fundamental_alt_120d_5bucket_class_confidence` | MATRIX | 0.424 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day alternative fundamental-based 5-bucket classification. |
| 622 | `fundamental_alt_120d_qtile5_confidence_score` | MATRIX | 0.424 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence for classifying 120-day return into quantile 5 using alternative fundamental data. |
| 623 | `fundamental_alt_120d_regress_return_pred` | MATRIX | 0.424 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted 120-day forward return using alternative fundamental features. |
| 624 | `fundamental_alt_120d_regression_pred` | MATRIX | 0.424 | 价量与波动 | 0 | — | — | — | UNUSABLE | Regression-based 120-day forward return prediction using alternative fundamental features. |
| 625 | `fundamental_alt_60d_5bucket_class_confidence` | MATRIX | 0.424 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day alternative fundamental-based 5-bucket classification. |
| 626 | `alt_fundamental_120d_bin5_confidence` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Model confidence for alternative fundamental-based signal over 120 days, quantile 5. |
| 627 | `alt_fundamental_120d_bin5_confidence_mcr` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Model confidence for alternative fundamental-based signal over 120 days, quantile 5, Mfmcr module. |
| 628 | `alt_fundamental_60d_bin5_confidence_mcr` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Model confidence for alternative fundamental-based signal over 60 days, quantile 5, Mfmcr module. |
| 629 | `alt_fundamental_signal_120d_bin1_mcr` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Alternative fundamental-based signal over 120 days, quantile 1, Mfmcr module. |
| 630 | `alt_fundamental_signal_120d_bin5` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Alternative fundamental-based signal over 120 days, quantile 5. |
| 631 | `alt_fundamental_signal_120d_bin5_mcr` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Alternative fundamental-based signal over 120 days, quantile 5, Mfmcr module. |
| 632 | `alt_fundamental_signal_60d_bin5_mcr` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Alternative fundamental-based signal over 60 days, quantile 5, Mfmcr module. |
| 633 | `fundamental2_120d_5quantile_confidence_score` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 120-day, 5-quantile return prediction using secondary fundamental features. |
| 634 | `fundamental2_120d_5quantile_pred` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day, 5-quantile return prediction using secondary set of fundamental features. |
| 635 | `fundamental2_120d_quantile1_pred_mfml` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | 120-day prediction using alternate fundamental features, quantile 1 (multi-model variant). |
| 636 | `fundamental2_120d_quantile5_confidence_score` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 120-day return using secondary fundamental features. |
| 637 | `fundamental2_120d_single_quantile_forecast` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day single-quantile return prediction using secondary set of fundamental features. |
| 638 | `fundamental2_60d_5quantile_confidence_score` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model confidence score for 60-day, 5-quantile return prediction using secondary fundamental features. |
| 639 | `fundamental2_60d_5quantile_pred` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day, 5-quantile return prediction using secondary set of fundamental features. |
| 640 | `fundamental2_60d_quantile1_pred_mfml` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | 60-day prediction using alternate fundamental features, quantile 1 (multi-model variant). |
| 641 | `fundamental2_60d_quantile5_classification` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | Classification of 60-day return using secondary fundamental features into one of five quantile buckets. |
| 642 | `fundamental2_60d_quantile5_confidence_score` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model's confidence in the 5-bucket quantile prediction for 60-day return using secondary fundamental features. |
| 643 | `fundamental2_60d_quantile5_pred_mfml` | MATRIX | 0.423 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | 60-day prediction using alternate fundamental features, quantile 5 (multi-model variant). |
| 644 | `fundamental2_60d_regression_prediction` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day forward return prediction using secondary set of fundamental features. |
| 645 | `fundamental2_60d_single_quantile_pred` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day, single-quantile return prediction using secondary set of fundamental features. |
| 646 | `fundamental2_based_return_pred_r60` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | Return prediction using secondary fundamental data over 60 days. |
| 647 | `fundamental_alt_120d_5bucket_class_pred_solar` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day forward return classification into five buckets using alternative fundamental features (SolarEquiNox variant). |
| 648 | `fundamental_alt_120d_regression_pred_solar` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | Regression-based 120-day forward return prediction using alternative fundamental features (SolarEquiNox variant). |

## 六、本地回测证据

- 本地累计回测 **5** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `78ZjLEd2` | 0.57 | 0.19 | -0.07 | — | 0.08 | ["LOW_SHARPE | 162 | `rank(alt_fundamental_60d_bin5_confidence)` |
| `XgW795Kb` | 0.24 | 0.06 | 0.48 | — | 0.13 | ["LOW_SHARPE | 162 | `rank(analyst_120d_quantile1_pred)` |
| `0mRwY088` | 0.12 | 0.02 | -0.29 | — | 0.10 | ["LOW_SHARPE | 162 | `rank(alt3_short_term_hedge_signal_5d_q5)` |
| `d5OjWAx2` | -0.57 | -0.22 | -0.72 | — | 0.10 | ["LOW_SHARPE | 162 | `rank(long_hedge2_quantile1_r60_pred)` |
| `rK5jRvWm` | -0.74 | -0.32 | -1.30 | — | 0.10 | ["LOW_SHARPE | 162 | `rank(long_hedge2_120d_quantile5_pred_mfml)` |

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

