# multi_source_model — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `multi_source_model` |
| 名称 | Multi-Source Market Return Prediction |
| 类别 | MODEL |
| 数据字段数(平台) | 60 |
| 覆盖率 | 0.5785 |
| 平台已有 alpha | 1 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides predictive signals for global financial markets by integrating a diverse set of data sources, including price-volume trends, fundamental financial indicators, analyst forecasts, options market data, event-driven information, and contextual factors such as market regimes and calendar effects. The model generates both short-term and long-term return forecasts, as well as specialized hedge signals designed to be uncorrelated with the main predictions for enhanced risk management. By combining these varied inputs and applying contextual adjustments, the dataset aims to deliver robust, risk-aware return predictions that can be used to inform trading strategies, asset allocation, and portfolio risk control. Its comprehensive, multi-factor approach makes it a valuable tool f

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **60** |
| 类型分布 | MATRIX×60 |
| 平均覆盖率 | **0.579** |
| 覆盖率区间 | 0.45 ~ 0.60 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 58 | 96.7% |
| 稀疏 (<0.50) | 2 | 3.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 43 | 71.7% |
| UNUSABLE | 17 | 28.3% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 43 / UNUSABLE 17 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 45 | 0.58 | event_embedding_quantile2_60d_pred、event_embedding_quantile2_confidence_60d_pred、long_term_quantile1_120d_pred |
| 其他 | 6 | 0.60 | long_horizon_hedge3_quantile1_120d_pred、long_horizon_hedge3_quantile1_60d_pred、long_horizon_hedge_quantile2_60d_pred |
| 修正与预期 | 6 | 0.53 | analyst_quantile1_120d_pred、analyst_quantile1_60d_pred、analyst_quantile5_120d_pred |
| 风险与质量 | 3 | 0.60 | long_horizon_hedge_quantile2_confidence_60d_pred、short_horizon_hedge3_quantile4_confidence_20d_pred、short_horizon_hedge3_quantile5_confidence_5d_pred |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `event_embedding_quantile2_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-day forward return prediction for the 2nd quantile using event embedding features. |
| 2 | `event_embedding_quantile2_confidence_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile of 60-day event embedding-based return prediction. |
| 3 | `long_horizon_hedge3_quantile1_120d_pred` | MATRIX | 0.600 | 其他 | 0 | — | — | — | UNTESTED | Long-term hedge signal for the top quantile over 120 days, designed for low correlation with main signals. |
| 4 | `long_horizon_hedge3_quantile1_60d_pred` | MATRIX | 0.600 | 其他 | 0 | — | — | — | UNTESTED | Long-term hedge signal for the top quantile over 60 days, designed for low correlation with main signals. |
| 5 | `long_horizon_hedge_quantile2_60d_pred` | MATRIX | 0.600 | 其他 | 0 | — | — | — | UNTESTED | Long-term hedge signal for the 2nd quantile over 60 days, designed for low correlation with main signals. |
| 6 | `long_horizon_hedge_quantile2_confidence_60d_pred` | MATRIX | 0.600 | 风险与质量 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile of 60-day long-term hedge signal. |
| 7 | `long_term_quantile1_120d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the top quantile over a 120-day period. |
| 8 | `long_term_quantile1_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the top quantile over a 60-day period. |
| 9 | `long_term_quantile5_120d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the 5th quantile over a 120-day period. |
| 10 | `long_term_quantile5_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the 5th quantile over a 60-day period. |
| 11 | `long_term_quantile5_confidence_120d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 5th quantile bucket of 120-day long-term return prediction. |
| 12 | `long_term_quantile5_confidence_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 5th quantile bucket of 60-day long-term return prediction. |
| 13 | `long_term_regime2_quantile1_120d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the top quantile over 120 days, adjusted for two-phase market regime. |
| 14 | `long_term_regime2_quantile1_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the top quantile over 60 days, adjusted for two-phase market regime. |
| 15 | `long_term_regime4_quantile1_120d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the top quantile over 120 days, adjusted for four-phase market regime. |
| 16 | `long_term_regime4_quantile1_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the top quantile over 60 days, adjusted for four-phase market regime. |
| 17 | `long_term_seasonal_quantile1_120d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the top quantile over 120 days, adjusted for seasonal effects. |
| 18 | `long_term_seasonal_quantile1_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Long-horizon return prediction for the top quantile over 60 days, adjusted for seasonal effects. |
| 19 | `regime4_embedding_quantile1_20d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | 20-day forward return prediction for the top quantile using four-phase regime embedding features. |
| 20 | `short_horizon_hedge3_quantile1_5d_pred` | MATRIX | 0.600 | 其他 | 0 | — | — | — | UNTESTED | Short-term hedge signal for the top quantile over 5 days, designed for low correlation with main signals. |
| 21 | `short_horizon_hedge3_quantile4_20d_pred` | MATRIX | 0.600 | 其他 | 0 | — | — | — | UNTESTED | Short-term hedge signal for the 4th quantile over 20 days, designed for low correlation with main signals. |
| 22 | `short_horizon_hedge3_quantile4_confidence_20d_pred` | MATRIX | 0.600 | 风险与质量 | 0 | — | — | — | UNTESTED | Model confidence score for the 4th quantile of 20-day short-term hedge signal (third variant). |
| 23 | `short_horizon_hedge3_quantile5_5d_pred` | MATRIX | 0.600 | 其他 | 0 | — | — | — | UNTESTED | Short-term hedge signal for the 5th quantile over 5 days, designed for low correlation with main signals. |
| 24 | `short_horizon_hedge3_quantile5_confidence_5d_pred` | MATRIX | 0.600 | 风险与质量 | 0 | — | — | — | UNTESTED | Model confidence score for the 5th quantile of 5-day short-term hedge signal (third variant). |
| 25 | `short_term_quantile1_20d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon return prediction for the top quantile over a 20-day period. |
| 26 | `short_term_quantile1_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon return prediction for the top quantile over a 60-day period. |
| 27 | `short_term_quantile2_5d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon return prediction for the 2nd quantile over a 5-day period. |
| 28 | `short_term_quantile2_confidence_5d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 2nd quantile of 5-day short-term return prediction. |
| 29 | `short_term_quantile5_20d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon return prediction for the 5th quantile over a 20-day period. |
| 30 | `short_term_quantile5_5d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon return prediction for the 5th quantile over a 5-day period. |
| 31 | `short_term_quantile5_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-horizon return prediction for the 5th quantile over a 60-day period. |
| 32 | `short_term_quantile5_confidence_20d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 5th quantile bucket of 20-day short-term return prediction. |
| 33 | `short_term_quantile5_confidence_5d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 5th quantile bucket of 5-day short-term return prediction. |
| 34 | `short_term_quantile5_confidence_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Model confidence score for the 5th quantile bucket of 60-day short-term return prediction. |
| 35 | `short_term_regime2_quantile1_20d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 20 days, adjusted for two-phase market regime. |
| 36 | `short_term_regime2_quantile1_5d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 5 days, adjusted for two-phase market regime. |
| 37 | `short_term_regime2_quantile1_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 60 days, adjusted for two-phase market regime. |
| 38 | `short_term_regime4_quantile1_20d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 20 days, adjusted for four-phase market regime. |
| 39 | `short_term_regime4_quantile1_5d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 5 days, adjusted for four-phase market regime. |
| 40 | `short_term_regime4_quantile1_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 60 days, adjusted for four-phase market regime. |
| 41 | `short_term_seasonal_quantile1_20d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 20 days, adjusted for seasonal effects. |
| 42 | `short_term_seasonal_quantile1_5d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 5 days, adjusted for seasonal effects. |
| 43 | `short_term_seasonal_quantile1_60d_pred` | MATRIX | 0.600 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term return prediction for the top quantile over 60 days, adjusted for seasonal effects. |
| 44 | `price_volume_quantile1_20d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day forward return prediction for the top quantile using price-volume features. |
| 45 | `price_volume_quantile1_5d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day forward return prediction for the top quantile using price-volume features. |
| 46 | `price_volume_quantile1_60d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day forward return prediction for the top quantile using price-volume features. |
| 47 | `price_volume_quantile5_20d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day forward return prediction for the 5th quantile using price-volume features. |
| 48 | `price_volume_quantile5_5d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day forward return prediction for the 5th quantile using price-volume features. |
| 49 | `price_volume_quantile5_60d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day forward return prediction for the 5th quantile using price-volume features. |
| 50 | `price_volume_quantile5_confidence_20d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | Confidence score for the 5th quantile of 20-day return prediction using price-volume data. |
| 51 | `price_volume_quantile5_confidence_5d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | Confidence score for the 5th quantile of 5-day return prediction using price-volume data. |
| 52 | `price_volume_quantile5_confidence_60d_pred` | MATRIX | 0.538 | 价量与波动 | 0 | — | — | — | UNUSABLE | Confidence score for the 5th quantile of 60-day return prediction based on price-volume data. |
| 53 | `analyst_quantile1_120d_pred` | MATRIX | 0.525 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based prediction for the top quantile of 120-day forward returns. |
| 54 | `analyst_quantile1_60d_pred` | MATRIX | 0.525 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based prediction for the top quantile of 60-day forward returns. |
| 55 | `analyst_quantile5_120d_pred` | MATRIX | 0.525 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based prediction for the 5th quantile of 120-day forward returns. |
| 56 | `analyst_quantile5_60d_pred` | MATRIX | 0.525 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst-based prediction for the 5th quantile of 60-day forward returns. |
| 57 | `analyst_quantile5_confidence_120d_pred` | MATRIX | 0.525 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for the 5th quantile of 120-day analyst-based return prediction. |
| 58 | `analyst_quantile5_confidence_60d_pred` | MATRIX | 0.525 | 修正与预期 | 0 | — | — | — | UNUSABLE | Model confidence score for the 5th quantile of 60-day analyst-based return prediction. |
| 59 | `fundamental_quantile1_120d_pred` | MATRIX | 0.449 | 价量与波动 | 0 | — | — | — | UNUSABLE | 120-day forward return prediction for the top quantile using fundamental data. |
| 60 | `fundamental_quantile1_60d_pred` | MATRIX | 0.449 | 价量与波动 | 0 | — | — | — | UNUSABLE | 60-day forward return prediction for the top quantile using fundamental data. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

