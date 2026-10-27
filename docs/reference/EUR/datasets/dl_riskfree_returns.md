# dl_riskfree_returns — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `dl_riskfree_returns` |
| 名称 | Deep Learning Risk Free Returns |
| 类别 | OTHER |
| 数据字段数(平台) | 133 |
| 覆盖率 | 0.9429 |
| 平台已有 alpha | 177 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset leverages deep learning techniques to predict risk-free returns by transforming time series price and volume data into 2D chart images, which are then analyzed using pre-trained convolutional neural networks (CNNs). The dataset includes predictions for multiple time horizons (such as 5, 10, 20, and 50 days) and provides both raw and relative return forecasts, along with quantile rankings and associated probabilities. By simulating a retail trader’s perspective through chart-based analysis, this dataset offers a unique, high-dimensional approach to forecasting future returns with minimal risk. It is particularly useful for identifying low-risk trading opportunities and enhancing portfolio construction by providing robust, model-driven signals that can help anticipate price move

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **133** |
| 类型分布 | MATRIX×133 |
| 平均覆盖率 | **0.943** |
| 覆盖率区间 | 0.53 ~ 1.00 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 117 | 88.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 16 | 12.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 115 | 86.5% |
| UNUSABLE | 16 | 12.0% |
| WEAK | 1 | 0.8% |
| DEAD | 1 | 0.8% |

- 已实测字段：**2** 个（2%），best_sharpe 最高 **1.40**，中位 1.40

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 129 | 0.94 | quantile_label_1bucket_20day_ohlcv、probability_label0_2quantile_10day_eur_ohlc_ma、probability_label0_2quantile_20day_eur_ohlcma |
| 修正与预期 | 4 | 1.00 | single_bucket_20day_return_estimate_eur_ohlc_ma、single_bucket_10day_return_estimate_eur_ohlc_ma、single_bucket_50day_return_estimate_eur_ohlc_ma |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `quantile_label_1bucket_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 1 | 1.40 | 0.82 | 0.87 | WEAK | Continuous regression forecast of 20-day forward market-neutral return as a float; must be winsorized before use |
| 2 | `single_bucket_20day_return_estimate_eur_ohlc_ma` | MATRIX | 1.000 | 修正与预期 | 1 | 0.03 | 0.23 | 0.07 | DEAD | Continuous regression prediction of 20-day forward market-neutral return (float, must be winsorized before use) |
| 3 | `probability_label0_2quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the first quantile group out of two using EUR OHLC moving average |
| 4 | `probability_label0_2quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 0 in 2-quantile classification of 20-day return using European price chart features. |
| 5 | `probability_label0_2quantile_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 0 (0-based) out of 2 buckets of the 20-day forward risk-free market-neutral return f |
| 6 | `probability_label0_2quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the first quantile group out of two using EUR OHLC moving average |
| 7 | `probability_label0_2quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the first quantile group out of two using EUR OHLC moving average f |
| 8 | `probability_label0_2quantile_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 5-day forward market-neutral return falls in quantile bucket 0 of 2 (0-based); ex |
| 9 | `probability_label0_2quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 60-day forward market-neutral return falls in quantile bucket index 0 of 2 bucket |
| 10 | `probability_label0_3quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the first quantile group using EUR OHLC moving average features. |
| 11 | `probability_label0_3quantile_20day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 0 (zero-based) out of 3 buckets for 20-day forward market-neutral return |
| 12 | `probability_label0_3quantile_20day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 20-day forward return falls in quantile bucket index 0 out of 3 buckets (0-based); exp(value) g |
| 13 | `probability_label0_3quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the first quantile group using EUR OHLC moving average features. |
| 14 | `probability_label0_3quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the first quantile group using EUR OHLC moving average features. |
| 15 | `probability_label0_3quantile_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 0 (0-based) out of 3 buckets for 5-day forward risk-free return prediction; exp(valu |
| 16 | `probability_label0_3quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 60-day forward market-neutral return falls in quantile bucket index 0 of 3 bucket |
| 17 | `probability_label0_4quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that 10-day forward return is in bucket index 0 of 4 buckets for European ohlc_ma MFM2 model; exponentia |
| 18 | `probability_label0_4quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 0 in 4-quantile classification of 20-day return using European price chart features. |
| 19 | `probability_label0_4quantile_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 0 (zero-based) of 5 for 20-day forward return; exponentiate for probability |
| 20 | `probability_label0_4quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the first quantile group out of four using EUR OHLC moving average |
| 21 | `probability_label0_4quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the first quantile group out of four using EUR OHLC moving average |
| 22 | `probability_label0_4quantile_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 5-day forward market-neutral return falls in quantile bucket index 0 of 4 buckets |
| 23 | `probability_label0_4quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 60-day forward market-neutral return falls in quantile bucket 0 of 4 (0-based); e |
| 24 | `probability_label0_5quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the first quantile group out of five using EUR OHLC moving average |
| 25 | `probability_label0_5quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 0 in 5-quantile classification of 20-day return using European price chart features. |
| 26 | `probability_label0_5quantile_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 20-day forward market-neutral return falls in quantile bucket 0 of 5 (zero-based); exp(value) g |
| 27 | `probability_label0_5quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the first quantile group out of five using EUR OHLC moving average |
| 28 | `probability_label0_5quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the first quantile group out of five using EUR OHLC moving average |
| 29 | `probability_label0_5quantile_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 5-day forward market-neutral return falls in quantile bucket 0 of 5 (zero-based); exp(value) gi |
| 30 | `probability_label0_5quantile_60day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that 60-day forward return is in bucket index 0 of 5 buckets (zero-based), exp(value) gives probability |
| 31 | `probability_label1_2quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the second quantile group out of two using EUR OHLC moving average |
| 32 | `probability_label1_2quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 1 in 2-quantile classification of 20-day return using European price chart features. |
| 33 | `probability_label1_2quantile_20day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 1 (0-based) of 2 for 20-day forward market-neutral return; exp(value) yields actiona |
| 34 | `probability_label1_2quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the second quantile group out of two using EUR OHLC moving average |
| 35 | `probability_label1_2quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the second quantile group out of two using EUR OHLC moving average |
| 36 | `probability_label1_2quantile_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 5-day forward market-neutral return falls in quantile bucket 1 of 2 (0-based); ex |
| 37 | `probability_label1_2quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 60-day forward market-neutral return is in quantile bucket 1 of 2 buckets, zero-based; exp(valu |
| 38 | `probability_label1_3quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that 10-day forward return is in bucket index 1 of 3 buckets for European ohlc_ma MFM2 model; exponentia |
| 39 | `probability_label1_3quantile_20day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 1 (zero-based) out of 3 buckets for 20-day forward market-neutral return |
| 40 | `probability_label1_3quantile_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 1 (0-based) of 3 for 20-day forward market-neutral return; exp(value) yields actiona |
| 41 | `probability_label1_3quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the second quantile group using EUR OHLC moving average features. |
| 42 | `probability_label1_3quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the second quantile group using EUR OHLC moving average features. |
| 43 | `probability_label1_3quantile_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 5-day forward market-neutral return falls in quantile bucket 1 of 3 (0-based); ex |
| 44 | `probability_label1_3quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 60-day forward market-neutral return falls in quantile bucket index 1 of 3 bucket |
| 45 | `probability_label1_4quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the second quantile group out of four using EUR OHLC moving averag |
| 46 | `probability_label1_4quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 1 in 4-quantile classification of 20-day return using European price chart features. |
| 47 | `probability_label1_4quantile_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 20-day forward market-neutral return falls in quantile bucket index 1 of 4 bucket |
| 48 | `probability_label1_4quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the second quantile group out of four using EUR OHLC moving averag |
| 49 | `probability_label1_4quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the second quantile group out of four using EUR OHLC moving average |
| 50 | `probability_label1_4quantile_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 5-day forward market-neutral return falls in quantile bucket 1 of 4 (zero-based); exp(value) gi |
| 51 | `probability_label1_4quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 60-day forward market-neutral return falls in quantile bucket 1 of 4 (zero-based); exp(value) g |
| 52 | `probability_label1_5quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the second quantile group out of five using EUR OHLC moving averag |
| 53 | `probability_label1_5quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 1 (zero-based) out of 5 buckets for 20-day forward market-neutral return |
| 54 | `probability_label1_5quantile_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that 20-day forward return is in bucket index 1 of 5 buckets (zero-based), exp(value) gives probability |
| 55 | `probability_label1_5quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the second quantile group out of five using EUR OHLC moving averag |
| 56 | `probability_label1_5quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the second quantile group out of five using EUR OHLC moving average |
| 57 | `probability_label1_5quantile_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 5-day forward market-neutral return falls in quantile bucket 1 of 5 (0-based); ex |
| 58 | `probability_label1_5quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 60-day forward market-neutral return is in quantile bucket index 1 out of 5; exponentiate to ge |
| 59 | `probability_label2_3quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that 10-day forward return is in bucket index 2 of 3 buckets for European ohlc_ma MFM2 model; exponentia |
| 60 | `probability_label2_3quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 2 (zero-based) out of 3 buckets for 20-day forward market-neutral return |
| 61 | `probability_label2_3quantile_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 20-day forward market-neutral return falls in quantile bucket 2 of 3 (0-based); e |
| 62 | `probability_label2_3quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 50-day forward market-neutral return falls in quantile bucket index 2 of 3; exp(value) converts |
| 63 | `probability_label2_3quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the third quantile group using EUR OHLC moving average features. |
| 64 | `probability_label2_3quantile_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 5-day forward market-neutral return is in quantile bucket 2 of 3 buckets, zero-based; exp(value |
| 65 | `probability_label2_3quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 2 (0-based) out of 3 buckets of the 60-day forward risk-free market-neutral return f |
| 66 | `probability_label2_4quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that 10-day forward return is in bucket index 2 of 4 buckets for European ohlc_ma MFM2 model; exponentia |
| 67 | `probability_label2_4quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 2 in 4-quantile classification of 20-day return using European price chart features. |
| 68 | `probability_label2_4quantile_20day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 20-day forward market-neutral return falls in quantile bucket 2 of 4 (zero-based); exp(value) g |
| 69 | `probability_label2_4quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the third quantile group out of four using EUR OHLC moving average |
| 70 | `probability_label2_4quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the third quantile group out of four using EUR OHLC moving average |
| 71 | `probability_label2_4quantile_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 5-day forward market-neutral return falls in quantile bucket 2 of 4 (0-based); ex |
| 72 | `probability_label2_4quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 60-day forward market-neutral return will fall in quantile bucket index 2 of 4 (z |
| 73 | `probability_label2_5quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of the 10-day forward return being in bucket index 2 (third bucket) out of 5 buckets for E |
| 74 | `probability_label2_5quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 2 in 5-quantile classification of 20-day return using European price chart features. |
| 75 | `probability_label2_5quantile_20day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 2 (0-based) out of 5 buckets for 20-day forward risk-free return prediction; exp(val |
| 76 | `probability_label2_5quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the third quantile group out of five using EUR OHLC moving average |
| 77 | `probability_label2_5quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the third quantile group out of five using EUR OHLC moving average |
| 78 | `probability_label2_5quantile_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 5-day forward market-neutral return falls in quantile bucket 2 of 5 (zero-based); |
| 79 | `probability_label2_5quantile_60day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 60-day forward market-neutral return falls in quantile bucket 2 of 5 (zero-based); exp(value) g |
| 80 | `probability_label3_4quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the fourth quantile group out of four using EUR OHLC moving averag |
| 81 | `probability_label3_4quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 3 in 4-quantile classification of 20-day return using European price chart features. |
| 82 | `probability_label3_4quantile_20day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 20-day forward market-neutral return falls in quantile bucket index 3 of 4 bucket |
| 83 | `probability_label3_4quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the fourth quantile group out of four using EUR OHLC moving averag |
| 84 | `probability_label3_4quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the fourth quantile group out of four using EUR OHLC moving average |
| 85 | `probability_label3_4quantile_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 3 (zero-based) of 5 for 5-day forward return; exponentiate for probability |
| 86 | `probability_label3_4quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 3 (0-based) out of 4 buckets for 60-day forward risk-free return prediction; exp(val |
| 87 | `probability_label3_5quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the fourth quantile group out of five using EUR OHLC moving averag |
| 88 | `probability_label3_5quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 3 in 5-quantile classification of 20-day return using European price chart features. |
| 89 | `probability_label3_5quantile_20day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 3 (0-based) out of 5 buckets of the 20-day forward risk-free market-neutral return f |
| 90 | `probability_label3_5quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the fourth quantile group out of five using EUR OHLC moving averag |
| 91 | `probability_label3_5quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the fourth quantile group out of five using EUR OHLC moving average |
| 92 | `probability_label3_5quantile_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 3 (0-based) out of 5 buckets for 5-day forward risk-free return prediction; exp(valu |
| 93 | `probability_label3_5quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 60-day forward market-neutral return falls in quantile bucket 3 of 5 (zero-based); exp(value) g |
| 94 | `probability_label4_5quantile_10day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 10-day forward return falls into the fifth quantile group using EUR OHLC moving average features. |
| 95 | `probability_label4_5quantile_20day_eur_ohlcma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Model probability for label 4 in 5-quantile classification of 20-day return using European price chart features. |
| 96 | `probability_label4_5quantile_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 20-day forward market-neutral return falls in quantile bucket index 4 of 5 bucket |
| 97 | `probability_label4_5quantile_50day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 50-day forward return falls into the fifth quantile group using EUR OHLC moving average features. |
| 98 | `probability_label4_5quantile_5day_eur_ohlc_ma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the 5-day forward return falls into the fifth quantile group using EUR OHLC moving average features. |
| 99 | `probability_label4_5quantile_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability for quantile bucket 4 (0-based) out of 5 buckets of the 5-day forward risk-free market-neutral return fo |
| 100 | `probability_label4_5quantile_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that 60-day forward return is in bucket index 4 of 5 buckets (zero-based), exp(value) gives probability |
| 101 | `quantile_label_1bucket_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression prediction (float) of the 5-day forward market-neutral return; requires winsorization before use |
| 102 | `quantile_label_1bucket_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression prediction of 60-day forward risk-free return (float); requires winsorization before use |
| 103 | `single_bucket_10day_return_estimate_eur_ohlc_ma` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted 10-day forward return value for the single quantile group using EUR OHLC moving average features. |
| 104 | `single_bucket_50day_return_estimate_eur_ohlc_ma` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Continuous regression prediction (float) of 50-day forward market-neutral return; requires winsorization before use |
| 105 | `single_bucket_5day_return_estimate_eur_ohlc_ma` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Continuous regression prediction of the 5-day forward market-neutral return; must be winsorized before use |
| 106 | `quantile_label_2bucket_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket (integer 0 or 1) of 2 buckets for the 20-day forward risk-free market-neutral return forecast |
| 107 | `quantile_label_2bucket_5day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket (0-based) index of 2 buckets for 5-day forward risk-free return prediction (integer) |
| 108 | `quantile_label_2bucket_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket index (0 or 1) for the 60-day forward market-neutral return divided into 2 buckets, zero-based |
| 109 | `quantile_label_3bucket_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket (integer 0 to 2) for the 20-day forward market-neutral return, zero-based indexing |
| 110 | `quantile_label_3bucket_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket index (0 to 2) for the 5-day forward market-neutral return divided into 3 buckets, zero-based |
| 111 | `quantile_label_3bucket_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket (0-based) index of 3 buckets for 60-day forward risk-free return prediction (integer) |
| 112 | `quantile_label_4bucket_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket (integer, 0-based) index in 4 buckets for the 20-day forward market-neutral return from the ASI |
| 113 | `quantile_label_4bucket_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket index (integer 0 to 3) for the 5-day forward market-neutral return divided into 4 buckets |
| 114 | `quantile_label_4bucket_60day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket index (0-based) indicating which of 4 buckets the 60-day forward market-neutral return falls in |
| 115 | `quantile_label_5bucket_20day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket (integer 0 to 4) for the 20-day forward market-neutral return, zero-based indexing |
| 116 | `quantile_label_5bucket_5day_ohlcv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket index (integer 0 to 4) for the 5-day forward market-neutral return divided into 5 buckets |
| 117 | `quantile_label_5bucket_60day_ohlcv_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Assigned quantile bucket index (integer between 0 and 4) for the 60-day forward market-neutral return, divided into 5 bu |
| 118 | `quantile_label_2bucket_10day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket (integer 0 or 1) for the 10-day forward market-neutral return, divided into 2 buckets (0-based |
| 119 | `quantile_label_2bucket_20day_eur_ohlcma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0 to 1) for 20-day forward market-neutral return divided into 2 buckets |
| 120 | `quantile_label_2bucket_50day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0-based) out of 2 buckets indicating predicted 50-day forward market-neutral return |
| 121 | `quantile_label_2bucket_5day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted quantile label (out of 2) for 5-day forward return using EUR OHLC moving average features. |
| 122 | `quantile_label_3bucket_10day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket (0-based, 0 to 2) for 10-day forward market-neutral return divided into 3 buckets for European |
| 123 | `quantile_label_3bucket_20day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0 to 2) for 20-day forward market-neutral return divided into 3 buckets |
| 124 | `quantile_label_3bucket_50day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0-based) for the 50-day forward market-neutral return divided into 3 buckets |
| 125 | `quantile_label_3bucket_5day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted quantile label (out of 3) for 5-day forward return using EUR OHLC moving average features. |
| 126 | `quantile_label_4bucket_10day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket (0-based, 0 to 3) for 10-day forward market-neutral return divided into 4 buckets for the Europ |
| 127 | `quantile_label_4bucket_20day_eur_ohlcma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0 to 3) for 20-day forward market-neutral return divided into 4 buckets |
| 128 | `quantile_label_4bucket_50day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0-based) out of 4 buckets indicating predicted 50-day forward market-neutral return |
| 129 | `quantile_label_4bucket_5day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0-based) for the 5-day forward market-neutral return divided into 4 buckets (values 0 to |
| 130 | `quantile_label_5bucket_10day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket (0-based, 0 to 4) for 10-day forward market-neutral return divided into 5 buckets for European |
| 131 | `quantile_label_5bucket_20day_eur_ohlcma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0 to 4) for 20-day forward market-neutral return divided into 5 buckets |
| 132 | `quantile_label_5bucket_50day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Assigned quantile bucket index (0-based) out of 5 buckets indicating predicted 50-day forward market-neutral return |
| 133 | `quantile_label_5bucket_5day_eur_ohlc_ma` | MATRIX | 0.526 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted quantile label (out of 5) for 5-day forward return using EUR OHLC moving average features. |

## 六、本地回测证据

- 本地累计回测 **6** 条；其中 `ra_failed_checks` 为空的 **1** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `0mXAwnYq` | 1.40 | 0.75 | 0.82 | 0.87 | 0.06 | 0 | probe_dl_eur_20260921 | `signed_power(subtract(rank(quantile_label_1bucket_20day_ohlcv), 0.5), 0.5)` |
| `qMxnjeLA` | 1.07 | 0.54 | — | 0.55 | 0.09 | ["LOW_SHARPE | probe_dl_eur_20260921 | `trade_when(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5, sig` |
| `xA3ejXvJ` | 1.07 | 0.53 | — | 0.54 | 0.09 | ["LOW_SHARPE | probe_dl_eur_20260921 | `trade_when(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5, sig` |
| `omLnqQEk` | 0.64 | 0.25 | — | 0.41 | 0.09 | ["LOW_SHARPE | probe_dl_eur_20260921 | `trade_when(and(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5,` |
| `gJbmj7av` | 0.03 | 0.00 | 0.23 | 0.07 | 0.12 | ["LOW_SHARPE | probe_dl_eur_20260921 | `signed_power(subtract(rank(single_bucket_20day_return_estimate_eur_ohlc_ma), 0.5), 0.5)` |
| `GrbnlEmO` | -0.23 | -0.06 | — | -0.20 | 0.12 | ["LOW_SHARPE | probe_dl_eur_20260921 | `trade_when(rank(divide(mean_trade_volume_30m_pre_close_2, ts_mean(volume, 22))) > 0.5, sig` |

## 七、判死记录（sealed dead_end）

- `EUR-DLRF-PROD-WALL-080`（None）family=None：{"dataset": "dl_riskfree_returns", "evidence": "wave132 14 条完成回测，4 颗全硬闸 PASS（O0rZ3Qr7 S2.51/F1.23、1YxdMw6Q S2.43/F1.17、P0Z3k5dK S2.75/F1.40、E5veOZ81 S2.64/F1.29）但 prod_corr 全部 0.80-0.81 超 0.7 硬闸。变体尝试：换窗口（20d/60d/5d）、换权重（0.4/0.6 vs 0.3/0.4/0.3）、行业残差化（group_mean subtract）、EUR 专用模型（eur_ohlc_ma 信号弱 S0.84）均无法破墙。", "reason": "dl_riskfree_returns DL 分位数概率信号在 EUR D1 有真实预测力（Sharpe 2.4-2.75），但信号方向（做多高预测收益-做
- `EUR-DLRF-OHLCV-PRODWALL-FIELD-LEVEL`（None）family=dl_riskfree_returns ohlcv 通用模型字段族 × 四种算子几何：{"dataset": "dl_riskfree_returns", "evidence": {"E5veOZ81_行业残差rank几何": "S2.64/F1.29 prod 0.8035", "group_mean行业残差加group_rank几何": "RRV1kJPo S2.44/F1.08/2Y1.86 prod 0.8212", "group_rank加subindustry几何": "xAYdm0Ag S2.32/F1.03 prod 0.8115；QP395LMG S2.57/F1.20", "group_zscore加subindustry几何": "blRdWoWN S2.71/F1.34/2Y2.04 prod 0.8100", "rank几何": "P0Z3k5dK S2.75/F1.40 prod 0.8118；O0rZ3Qr7 S2.51/F1.23 prod 
- `EUR-DLRF-EUROHLCMA-TURNOVER-FITNESS-WALL`（None）family=dl_riskfree_returns eur_ohlc_ma EUR 专用模型族 × 跨期分位数差：{"d4_verdict": "未达资格线（最强 Sharpe 1.48>=1.25 但 Fitness 0.36<0.8）→ 判死，不进 near_pool、不发 Mode B 增强波", "dataset": "dl_riskfree_returns", "evidence": {"78ZnxblZ": "L4-L0@50d-5d tsv22 S0.82/F0.17/2Y0.03 3FAIL（拉长窗口反而更差）", "E5veaQKm": "L3-L0@50d-5d S1.13/F0.27/2Y0.87 fail=[]", "O0rxnea7": "L4-L0@50d-5d S0.84/F0.16/2Y-0.03 3FAIL", "ZY0Klv83": "L3-L1@50d-5d S1.30/F0.30/2Y1.22 prod0.3751 fail=[]", "akLENZa5": "
- `EUR-DLRF-BOTH-FAMILIES-DEAD-MATH-PROOF`（None）family=dl_riskfree_returns 全数据集（ohlcv 通用族 + eur_ohlc_ma 专用族）：{"conclusion": "dl_riskfree_returns 在 EUR D1 全数据集判死：两个字段族各缺一半且缺口互不兼容，无法通过任何合规手段（换几何/换字段组合/Mode A 参数层优化）凑齐可提交四要件。", "dataset": "dl_riskfree_returns", "family_comparison": {"eur_ohlc_ma_专用族": {"best_alpha": "MP1LxrAr / xAYdnZPm / akLENZa5", "field_count": 76, "fitness": "0.31-0.39 FAIL", "prod_corr": "0.3234-0.3751 PASS（战役最低）", "returns_ceiling": 0.0438, "self_corr": "0.0205-0.0500 PASS", "sharpe": 
- `EUR-DLRFR-OHLCV-GEOM-WALL`（2026-09-09）family=dl_riskfree_returns：{"blocked_by": "prod_corr only（TOP2500/TOPCS1600）；IS 崩（TOP1200/800/400）；after-cost 闸（ILLIQUID）", "conclusion": "dl_riskfree_returns 在 EUR D1 全部 6 个 universe 结构性闭合。prod 墙由信号内容驱动（MAX 统计量），换几何/换 universe/换分组轴均无效；换 universe 反而推高 max prod_corr。本数据集在 EUR D1 判死，任何继续在本数据集本区域刷壳的行为都是烧配额。", "dataset": "dl_riskfree_returns", "evidence_waves": [145, 147, 152, 153, 154], "prod_by_universe": {"ILLIQUID_MINVOL1M"

