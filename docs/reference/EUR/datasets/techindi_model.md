# techindi_model — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `techindi_model` |
| 名称 | Deep Learning Technical Indicator Returns |
| 类别 | OTHER |
| 数据字段数(平台) | 798 |
| 覆盖率 | 0.9999 |
| 平台已有 alpha | 2263 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset leverages deep learning techniques to analyze images of technical indicator charts, mimicking the decision-making process of retail traders. By converting time series financial data into 2D images, pre-trained convolutional neural networks (CNNs) are used to predict future stock returns and their relative rankings across multiple time horizons. The dataset provides quantile-based return predictions, confidence scores, and cross-sectional rankings for a diversified universe of global equities. Its image-based approach captures complex market patterns and technical signals that may be missed by traditional time series analysis. This can be highly valuable for forecasting price movements, generating alpha signals, and constructing systematic trading strategies with improved predi

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **798** |
| 类型分布 | MATRIX×798 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 798 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 798 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 796 | 1.00 | predicted_first_quantile_five_day_return_13、predicted_first_quantile_five_day_return_14、predicted_first_quantile_five_day_return_141 |
| 修正与预期 | 2 | 1.00 | tm_15_r1_r5_r10_rh_glb_d1_r10_q1、tm_16_r1_r5_r10_rh_glb_d1_r5_q1 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `predicted_first_quantile_five_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the first quantile. |
| 2 | `predicted_first_quantile_five_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for a stock classified in the first quantile. |
| 3 | `predicted_first_quantile_five_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the first quantile group. |
| 4 | `predicted_first_quantile_five_day_return_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the first quantile. |
| 5 | `predicted_first_quantile_five_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, first group. |
| 6 | `predicted_first_quantile_five_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, first group. |
| 7 | `predicted_first_quantile_five_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the first quantile group. |
| 8 | `predicted_first_quantile_one_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the first quantile group. |
| 9 | `predicted_first_quantile_one_day_return_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the first quantile. |
| 10 | `predicted_first_quantile_one_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the first quantile group. |
| 11 | `predicted_first_quantile_one_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the first quantile. |
| 12 | `predicted_first_quantile_one_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, first group. |
| 13 | `predicted_first_quantile_one_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, first group. |
| 14 | `predicted_first_quantile_one_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the first quantile group. |
| 15 | `predicted_first_quantile_ten_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the first quantile group. |
| 16 | `predicted_first_quantile_ten_day_return_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the first quantile. |
| 17 | `predicted_first_quantile_ten_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the first quantile group. |
| 18 | `predicted_first_quantile_ten_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the first quantile. |
| 19 | `predicted_first_quantile_ten_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, first group. |
| 20 | `predicted_first_quantile_ten_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, first group. |
| 21 | `predicted_first_quantile_ten_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the first quantile group. |
| 22 | `probability_fifth_bucket_five_day_label_four_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, label four. |
| 23 | `probability_fifth_bucket_five_day_label_four_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, label four. |
| 24 | `probability_fifth_bucket_five_day_label_four_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth bucket of the fifth quantile. |
| 25 | `probability_fifth_bucket_five_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, label one. |
| 26 | `probability_fifth_bucket_five_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second bucket of the fifth quantile. |
| 27 | `probability_fifth_bucket_five_day_label_one_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second bucket of the fifth quantile. |
| 28 | `probability_fifth_bucket_five_day_label_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, label three. |
| 29 | `probability_fifth_bucket_five_day_label_three_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth bucket of the fifth quantile. |
| 30 | `probability_fifth_bucket_five_day_label_three_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth bucket of the fifth quantile. |
| 31 | `probability_fifth_bucket_five_day_label_three_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, label three. |
| 32 | `probability_fifth_bucket_five_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, label two. |
| 33 | `probability_fifth_bucket_five_day_label_two_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, label two. |
| 34 | `probability_fifth_bucket_five_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third bucket of the fifth quantile. |
| 35 | `probability_fifth_bucket_five_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the first bucket of the fifth quantile. |
| 36 | `probability_fifth_bucket_five_day_label_zero_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the first bucket of the fifth quantile. |
| 37 | `probability_fifth_bucket_five_day_label_zero_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, label zero. |
| 38 | `probability_fifth_bucket_one_day_label_four_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label four. |
| 39 | `probability_fifth_bucket_one_day_label_four_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label four. |
| 40 | `probability_fifth_bucket_one_day_label_four_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth bucket of the fifth quantile. |
| 41 | `probability_fifth_bucket_one_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label one. |
| 42 | `probability_fifth_bucket_one_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second bucket of the fifth quantile. |
| 43 | `probability_fifth_bucket_one_day_label_one_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second bucket of the fifth quantile. |
| 44 | `probability_fifth_bucket_one_day_label_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label three. |
| 45 | `probability_fifth_bucket_one_day_label_three_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label three. |
| 46 | `probability_fifth_bucket_one_day_label_three_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth bucket of the fifth quantile. |
| 47 | `probability_fifth_bucket_one_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label two. |
| 48 | `probability_fifth_bucket_one_day_label_two_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label two. |
| 49 | `probability_fifth_bucket_one_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third bucket of the fifth quantile. |
| 50 | `probability_fifth_bucket_one_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label zero. |
| 51 | `probability_fifth_bucket_one_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the first bucket of the fifth quantile. |
| 52 | `probability_fifth_bucket_one_day_label_zero_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the first bucket of the fifth quantile. |
| 53 | `probability_fifth_bucket_ten_day_label_four_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label four. |
| 54 | `probability_fifth_bucket_ten_day_label_four_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label four. |
| 55 | `probability_fifth_bucket_ten_day_label_four_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth bucket of the fifth quantile. |
| 56 | `probability_fifth_bucket_ten_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label one. |
| 57 | `probability_fifth_bucket_ten_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second bucket of the fifth quantile. |
| 58 | `probability_fifth_bucket_ten_day_label_one_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second bucket of the fifth quantile. |
| 59 | `probability_fifth_bucket_ten_day_label_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label three. |
| 60 | `probability_fifth_bucket_ten_day_label_three_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label three. |
| 61 | `probability_fifth_bucket_ten_day_label_three_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth bucket of the fifth quantile. |
| 62 | `probability_fifth_bucket_ten_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label two. |
| 63 | `probability_fifth_bucket_ten_day_label_two_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label two. |
| 64 | `probability_fifth_bucket_ten_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third bucket of the fifth quantile. |
| 65 | `probability_fifth_bucket_ten_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label zero. |
| 66 | `probability_fifth_bucket_ten_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the first bucket of the fifth quantile. |
| 67 | `probability_fifth_bucket_ten_day_label_zero_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the first bucket of the fifth quantile. |
| 68 | `probability_fifth_quantile_five_day_bucket_four_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket four. |
| 69 | `probability_fifth_quantile_five_day_bucket_four_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket four. |
| 70 | `probability_fifth_quantile_five_day_bucket_four_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket four. |
| 71 | `probability_fifth_quantile_five_day_bucket_four_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket four. |
| 72 | `probability_fifth_quantile_five_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket one. |
| 73 | `probability_fifth_quantile_five_day_bucket_one_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket one. |
| 74 | `probability_fifth_quantile_five_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket one. |
| 75 | `probability_fifth_quantile_five_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket one. |
| 76 | `probability_fifth_quantile_five_day_bucket_three_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket three. |
| 77 | `probability_fifth_quantile_five_day_bucket_three_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket three. |
| 78 | `probability_fifth_quantile_five_day_bucket_three_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket three. |
| 79 | `probability_fifth_quantile_five_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket two. |
| 80 | `probability_fifth_quantile_five_day_bucket_two_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket two. |
| 81 | `probability_fifth_quantile_five_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket two. |
| 82 | `probability_fifth_quantile_five_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket two. |
| 83 | `probability_fifth_quantile_five_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket zero. |
| 84 | `probability_fifth_quantile_five_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket zero. |
| 85 | `probability_fifth_quantile_five_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket zero. |
| 86 | `probability_fifth_quantile_five_day_bucket_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket zero. |
| 87 | `probability_fifth_quantile_one_day_bucket_four_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket four. |
| 88 | `probability_fifth_quantile_one_day_bucket_four_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket four. |
| 89 | `probability_fifth_quantile_one_day_bucket_four_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket four. |
| 90 | `probability_fifth_quantile_one_day_bucket_four_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket four. |
| 91 | `probability_fifth_quantile_one_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket one. |
| 92 | `probability_fifth_quantile_one_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket one. |
| 93 | `probability_fifth_quantile_one_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket one. |
| 94 | `probability_fifth_quantile_one_day_bucket_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket one. |
| 95 | `probability_fifth_quantile_one_day_bucket_three_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket three. |
| 96 | `probability_fifth_quantile_one_day_bucket_three_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket three. |
| 97 | `probability_fifth_quantile_one_day_bucket_three_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket three. |
| 98 | `probability_fifth_quantile_one_day_bucket_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket three. |
| 99 | `probability_fifth_quantile_one_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket two. |
| 100 | `probability_fifth_quantile_one_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket two. |
| 101 | `probability_fifth_quantile_one_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket two. |
| 102 | `probability_fifth_quantile_one_day_bucket_two_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket two. |
| 103 | `probability_fifth_quantile_one_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket zero. |
| 104 | `probability_fifth_quantile_one_day_bucket_zero_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket zero. |
| 105 | `probability_fifth_quantile_one_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket zero. |
| 106 | `probability_fifth_quantile_one_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket zero. |
| 107 | `probability_fifth_quantile_ten_day_bucket_four_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket four. |
| 108 | `probability_fifth_quantile_ten_day_bucket_four_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket four. |
| 109 | `probability_fifth_quantile_ten_day_bucket_four_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, bucket four. |
| 110 | `probability_fifth_quantile_ten_day_bucket_four_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket four. |
| 111 | `probability_fifth_quantile_ten_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, bucket one. |
| 112 | `probability_fifth_quantile_ten_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket one. |
| 113 | `probability_fifth_quantile_ten_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket one. |
| 114 | `probability_fifth_quantile_ten_day_bucket_one_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, bucket one. |
| 115 | `probability_fifth_quantile_ten_day_bucket_three_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket three. |
| 116 | `probability_fifth_quantile_ten_day_bucket_three_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, bucket three. |
| 117 | `probability_fifth_quantile_ten_day_bucket_three_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket three. |
| 118 | `probability_fifth_quantile_ten_day_bucket_three_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, bucket three. |
| 119 | `probability_fifth_quantile_ten_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket two. |
| 120 | `probability_fifth_quantile_ten_day_bucket_two_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, bucket two. |
| 121 | `probability_fifth_quantile_ten_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket two. |
| 122 | `probability_fifth_quantile_ten_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, bucket two. |
| 123 | `probability_fifth_quantile_ten_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket zero. |
| 124 | `probability_fifth_quantile_ten_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket zero. |
| 125 | `probability_fifth_quantile_ten_day_bucket_zero_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, bucket zero. |
| 126 | `probability_fifth_quantile_ten_day_bucket_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket zero. |
| 127 | `probability_fourth_bucket_five_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second bucket of the fourth quantile. |
| 128 | `probability_fourth_bucket_five_day_label_one_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second bucket of the fourth quantile. |
| 129 | `probability_fourth_bucket_five_day_label_one_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, label one. |
| 130 | `probability_fourth_bucket_five_day_label_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, label three. |
| 131 | `probability_fourth_bucket_five_day_label_three_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, label three. |
| 132 | `probability_fourth_bucket_five_day_label_three_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth bucket of the fourth quantile. |
| 133 | `probability_fourth_bucket_five_day_label_three_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, label three. |
| 134 | `probability_fourth_bucket_five_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, label two. |
| 135 | `probability_fourth_bucket_five_day_label_two_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, label two. |
| 136 | `probability_fourth_bucket_five_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third bucket of the fourth quantile. |
| 137 | `probability_fourth_bucket_five_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, label zero. |
| 138 | `probability_fourth_bucket_five_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the first bucket of the fourth quantile. |
| 139 | `probability_fourth_bucket_five_day_label_zero_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the first bucket of the fourth quantile. |
| 140 | `probability_fourth_bucket_one_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label one. |
| 141 | `probability_fourth_bucket_one_day_label_one_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label one. |
| 142 | `probability_fourth_bucket_one_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second bucket of the fourth quantile. |
| 143 | `probability_fourth_bucket_one_day_label_one_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label one. |
| 144 | `probability_fourth_bucket_one_day_label_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label three. |
| 145 | `probability_fourth_bucket_one_day_label_three_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label three. |
| 146 | `probability_fourth_bucket_one_day_label_three_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth bucket of the fourth quantile. |
| 147 | `probability_fourth_bucket_one_day_label_three_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label three. |
| 148 | `probability_fourth_bucket_one_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label two. |
| 149 | `probability_fourth_bucket_one_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third bucket of the fourth quantile. |
| 150 | `probability_fourth_bucket_one_day_label_two_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third bucket of the fourth quantile. |
| 151 | `probability_fourth_bucket_one_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label zero. |
| 152 | `probability_fourth_bucket_one_day_label_zero_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, label zero. |
| 153 | `probability_fourth_bucket_one_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the first bucket of the fourth quantile. |
| 154 | `probability_fourth_bucket_ten_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, label one. |
| 155 | `probability_fourth_bucket_ten_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second bucket of the fourth quantile. |
| 156 | `probability_fourth_bucket_ten_day_label_one_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second bucket of the fourth quantile. |
| 157 | `probability_fourth_bucket_ten_day_label_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, label three. |
| 158 | `probability_fourth_bucket_ten_day_label_three_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth bucket of the fourth quantile. |
| 159 | `probability_fourth_bucket_ten_day_label_three_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth bucket of the fourth quantile. |
| 160 | `probability_fourth_bucket_ten_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, label two. |
| 161 | `probability_fourth_bucket_ten_day_label_two_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, label two. |
| 162 | `probability_fourth_bucket_ten_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third bucket of the fourth quantile. |
| 163 | `probability_fourth_bucket_ten_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, label zero. |
| 164 | `probability_fourth_bucket_ten_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the first bucket of the fourth quantile. |
| 165 | `probability_fourth_bucket_ten_day_label_zero_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the first bucket of the fourth quantile. |
| 166 | `probability_fourth_quantile_five_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for five-day return, bucket one. |
| 167 | `probability_fourth_quantile_five_day_bucket_one_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket one. |
| 168 | `probability_fourth_quantile_five_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for five-day return, bucket one. |
| 169 | `probability_fourth_quantile_five_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket one. |
| 170 | `probability_fourth_quantile_five_day_bucket_three_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket three. |
| 171 | `probability_fourth_quantile_five_day_bucket_three_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for five-day return, bucket three. |
| 172 | `probability_fourth_quantile_five_day_bucket_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for five-day return, bucket three. |
| 173 | `probability_fourth_quantile_five_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for five-day return, bucket two. |
| 174 | `probability_fourth_quantile_five_day_bucket_two_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket two. |
| 175 | `probability_fourth_quantile_five_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for five-day return, bucket two. |
| 176 | `probability_fourth_quantile_five_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket two. |
| 177 | `probability_fourth_quantile_five_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket zero. |
| 178 | `probability_fourth_quantile_five_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for five-day return, bucket zero. |
| 179 | `probability_fourth_quantile_five_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket zero. |
| 180 | `probability_fourth_quantile_five_day_bucket_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for five-day return, bucket zero. |
| 181 | `probability_fourth_quantile_one_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, bucket one. |
| 182 | `probability_fourth_quantile_one_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket one. |
| 183 | `probability_fourth_quantile_one_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket one. |
| 184 | `probability_fourth_quantile_one_day_bucket_three_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket three. |
| 185 | `probability_fourth_quantile_one_day_bucket_three_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, bucket three. |
| 186 | `probability_fourth_quantile_one_day_bucket_three_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket three. |
| 187 | `probability_fourth_quantile_one_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket two. |
| 188 | `probability_fourth_quantile_one_day_bucket_two_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, bucket two. |
| 189 | `probability_fourth_quantile_one_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket two. |
| 190 | `probability_fourth_quantile_one_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, bucket two. |
| 191 | `probability_fourth_quantile_one_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket zero. |
| 192 | `probability_fourth_quantile_one_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket zero. |
| 193 | `probability_fourth_quantile_one_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, bucket zero. |
| 194 | `probability_fourth_quantile_one_day_bucket_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket zero. |
| 195 | `probability_fourth_quantile_ten_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket one. |
| 196 | `probability_fourth_quantile_ten_day_bucket_one_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket one. |
| 197 | `probability_fourth_quantile_ten_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket one. |
| 198 | `probability_fourth_quantile_ten_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket one. |
| 199 | `probability_fourth_quantile_ten_day_bucket_three_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket three. |
| 200 | `probability_fourth_quantile_ten_day_bucket_three_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket three. |
| 201 | `probability_fourth_quantile_ten_day_bucket_three_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket three. |
| 202 | `probability_fourth_quantile_ten_day_bucket_three_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket three. |
| 203 | `probability_fourth_quantile_ten_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket two. |
| 204 | `probability_fourth_quantile_ten_day_bucket_two_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket two. |
| 205 | `probability_fourth_quantile_ten_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket two. |
| 206 | `probability_fourth_quantile_ten_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket two. |
| 207 | `probability_fourth_quantile_ten_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock falls into the fourth quantile for ten-day return, bucket zero. |
| 208 | `probability_fourth_quantile_ten_day_bucket_zero_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket zero. |
| 209 | `probability_fourth_quantile_ten_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock falls into the fourth quantile for ten-day return, bucket zero. |
| 210 | `probability_fourth_quantile_ten_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket zero. |
| 211 | `probability_second_bucket_five_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second bucket of the second quantile. |
| 212 | `probability_second_bucket_five_day_label_one_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second bucket of the second quantile. |
| 213 | `probability_second_bucket_five_day_label_one_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second quantile, label one. |
| 214 | `probability_second_bucket_five_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second quantile, label zero. |
| 215 | `probability_second_bucket_five_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the first bucket of the second quantile. |
| 216 | `probability_second_bucket_five_day_label_zero_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the first bucket of the second quantile. |
| 217 | `probability_second_bucket_one_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second quantile, label one. |
| 218 | `probability_second_bucket_one_day_label_one_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second quantile, label one. |
| 219 | `probability_second_bucket_one_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second bucket of the second quantile. |
| 220 | `probability_second_bucket_one_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second quantile, label zero. |
| 221 | `probability_second_bucket_one_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the first bucket of the second quantile. |
| 222 | `probability_second_bucket_one_day_label_zero_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the first bucket of the second quantile. |
| 223 | `probability_second_bucket_ten_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, label one. |
| 224 | `probability_second_bucket_ten_day_label_one_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, label one. |
| 225 | `probability_second_bucket_ten_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second bucket of the second quantile. |
| 226 | `probability_second_bucket_ten_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, label zero. |
| 227 | `probability_second_bucket_ten_day_label_zero_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, label zero. |
| 228 | `probability_second_bucket_ten_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the first bucket of the second quantile. |
| 229 | `probability_second_quantile_five_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second quantile, bucket one. |
| 230 | `probability_second_quantile_five_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for five-day return, bucket one. |
| 231 | `probability_second_quantile_five_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for five-day return, bucket one. |
| 232 | `probability_second_quantile_five_day_bucket_one_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second quantile, bucket one. |
| 233 | `probability_second_quantile_five_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for five-day return, bucket zero. |
| 234 | `probability_second_quantile_five_day_bucket_zero_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second quantile, bucket zero. |
| 235 | `probability_second_quantile_five_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for five-day return, bucket zero. |
| 236 | `probability_second_quantile_five_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second quantile, bucket zero. |
| 237 | `probability_second_quantile_one_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Likelihood that a stock is in the second quantile for one-day return, bucket one. |
| 238 | `probability_second_quantile_one_day_bucket_one_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second quantile, bucket one. |
| 239 | `probability_second_quantile_one_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Likelihood that a stock is in the second quantile for one-day return, bucket one. |
| 240 | `probability_second_quantile_one_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second quantile, bucket one. |
| 241 | `probability_second_quantile_one_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for one-day return, bucket zero. |
| 242 | `probability_second_quantile_one_day_bucket_zero_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second quantile, bucket zero. |
| 243 | `probability_second_quantile_one_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for one-day return, bucket zero. |
| 244 | `probability_second_quantile_one_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second quantile, bucket zero. |
| 245 | `probability_second_quantile_ten_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Likelihood that a stock is in the second quantile for ten-day return, bucket one. |
| 246 | `probability_second_quantile_ten_day_bucket_one_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, bucket one. |
| 247 | `probability_second_quantile_ten_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Likelihood that a stock is in the second quantile for ten-day return, bucket one. |
| 248 | `probability_second_quantile_ten_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, bucket one. |
| 249 | `probability_second_quantile_ten_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, bucket zero. |
| 250 | `probability_second_quantile_ten_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for ten-day return, bucket zero. |
| 251 | `probability_second_quantile_ten_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, bucket zero. |
| 252 | `probability_second_quantile_ten_day_bucket_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for ten-day return, bucket zero. |
| 253 | `probability_third_bucket_five_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, label one. |
| 254 | `probability_third_bucket_five_day_label_one_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, label one. |
| 255 | `probability_third_bucket_five_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second bucket of the third quantile. |
| 256 | `probability_third_bucket_five_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, label two. |
| 257 | `probability_third_bucket_five_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third bucket of the third quantile. |
| 258 | `probability_third_bucket_five_day_label_two_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third bucket of the third quantile. |
| 259 | `probability_third_bucket_five_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, label zero. |
| 260 | `probability_third_bucket_five_day_label_zero_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, label zero. |
| 261 | `probability_third_bucket_five_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the first bucket of the third quantile. |
| 262 | `probability_third_bucket_one_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, label one. |
| 263 | `probability_third_bucket_one_day_label_one_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, label one. |
| 264 | `probability_third_bucket_one_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second bucket of the third quantile. |
| 265 | `probability_third_bucket_one_day_label_one_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, label one. |
| 266 | `probability_third_bucket_one_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, label two. |
| 267 | `probability_third_bucket_one_day_label_two_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, label two. |
| 268 | `probability_third_bucket_one_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third bucket of the third quantile. |
| 269 | `probability_third_bucket_one_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, label zero. |
| 270 | `probability_third_bucket_one_day_label_zero_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, label zero. |
| 271 | `probability_third_bucket_one_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the first bucket of the third quantile. |
| 272 | `probability_third_bucket_ten_day_label_one_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, label one. |
| 273 | `probability_third_bucket_ten_day_label_one_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second bucket of the third quantile. |
| 274 | `probability_third_bucket_ten_day_label_one_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second bucket of the third quantile. |
| 275 | `probability_third_bucket_ten_day_label_two_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, label two. |
| 276 | `probability_third_bucket_ten_day_label_two_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, label two. |
| 277 | `probability_third_bucket_ten_day_label_two_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third bucket of the third quantile. |
| 278 | `probability_third_bucket_ten_day_label_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, label zero. |
| 279 | `probability_third_bucket_ten_day_label_zero_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, label zero. |
| 280 | `probability_third_bucket_ten_day_label_zero_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the first bucket of the third quantile. |
| 281 | `probability_third_bucket_ten_day_label_zero_7` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, label zero. |
| 282 | `probability_third_quantile_five_bucket_label_two_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the predicted return falls into the second label of the third quantile in a five-bucket ranking. |
| 283 | `probability_third_quantile_five_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for five-day return, bucket one. |
| 284 | `probability_third_quantile_five_day_bucket_one_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, bucket one. |
| 285 | `probability_third_quantile_five_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for five-day return, bucket one. |
| 286 | `probability_third_quantile_five_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, bucket one. |
| 287 | `probability_third_quantile_five_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, bucket two. |
| 288 | `probability_third_quantile_five_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for five-day return, bucket two. |
| 289 | `probability_third_quantile_five_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, bucket two. |
| 290 | `probability_third_quantile_five_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for five-day return, bucket zero. |
| 291 | `probability_third_quantile_five_day_bucket_zero_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, bucket zero. |
| 292 | `probability_third_quantile_five_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for five-day return, bucket zero. |
| 293 | `probability_third_quantile_five_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, bucket zero. |
| 294 | `probability_third_quantile_one_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, bucket one. |
| 295 | `probability_third_quantile_one_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket one. |
| 296 | `probability_third_quantile_one_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket one. |
| 297 | `probability_third_quantile_one_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket two. |
| 298 | `probability_third_quantile_one_day_bucket_two_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, bucket two. |
| 299 | `probability_third_quantile_one_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket two. |
| 300 | `probability_third_quantile_one_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, bucket two. |
| 301 | `probability_third_quantile_one_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket zero. |
| 302 | `probability_third_quantile_one_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket zero. |
| 303 | `probability_third_quantile_one_day_bucket_zero_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, bucket zero. |
| 304 | `probability_third_quantile_one_day_bucket_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket zero. |
| 305 | `probability_third_quantile_ten_day_bucket_one_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for ten-day return, bucket one. |
| 306 | `probability_third_quantile_ten_day_bucket_one_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, bucket one. |
| 307 | `probability_third_quantile_ten_day_bucket_one_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for ten-day return, bucket one. |
| 308 | `probability_third_quantile_ten_day_bucket_one_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, bucket one. |
| 309 | `probability_third_quantile_ten_day_bucket_two_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for ten-day return, bucket two. |
| 310 | `probability_third_quantile_ten_day_bucket_two_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, bucket two. |
| 311 | `probability_third_quantile_ten_day_bucket_two_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for ten-day return, bucket two. |
| 312 | `probability_third_quantile_ten_day_bucket_two_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, bucket two. |
| 313 | `probability_third_quantile_ten_day_bucket_zero_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, bucket zero. |
| 314 | `probability_third_quantile_ten_day_bucket_zero_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for ten-day return, bucket zero. |
| 315 | `probability_third_quantile_ten_day_bucket_zero_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for ten-day return, bucket zero. |
| 316 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Continuous regression output for 10-day forward market-neutral return prediction, winsorization recommended, in the EUR universe |
| 317 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 0 (lowest bucket) out of 2 buckets (0 to 1) for the 10-day forward m |
| 318 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output for bucket 1 of 2 quantile buckets for 10-day forward market-neutral return prediction |
| 319 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 0 (lowest bucket) out of 3 buckets for the 10-day forward market-neu |
| 320 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 1 out of 3 buckets (0 to 2) for the 10-day forward market-neutral re |
| 321 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 2 out of 3 buckets for the 10-day forward market-neutral return prediction |
| 322 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 0 (lowest bucket) out of 4 buckets for the 10-day forward market-neutral return pr |
| 323 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 (second-lowest, bucket index 1 of 4) for 10-day forward marke |
| 324 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 2 out of 4 buckets for the 10-day forward market-neutral return prediction |
| 325 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 3 out of 4 buckets (0 to 3) for the 10-day forward market-neutral re |
| 326 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output that the stock belongs to the lowest bucket (bucket 0) among 5 quantile buckets for 10-day forward mark |
| 327 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 1 out of 5 buckets for the 10-day forward market-neutral return prediction |
| 328 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from model predicting the stock belongs to quantile bucket 2 out of 5 buckets for 10-day forward market-neutra |
| 329 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from model predicting the stock belongs to quantile bucket 3 out of 5 buckets for 10-day forward market-neutra |
| 330 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) for bucket 4 out of 5 quantile buckets at 10-day forward market-neutral return |
| 331 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output for 1-day forward market-neutral return prediction, must be winsorized before use |
| 332 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to the lowest quantile bucket (bucket 0 of 2) for 1-day forward market-neutral ret |
| 333 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from model predicting the stock belongs to quantile bucket 1 out of 2 buckets for 1-day forward market-neutral |
| 334 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from model predicting the stock belongs to quantile bucket 0 (lowest bucket) out of 3 buckets for 1-day forwar |
| 335 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output for bucket 1 of 3 quantile buckets for 1-day forward market-neutral return prediction |
| 336 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) for bucket 2 out of 3 quantile buckets at 1-day forward market-neutral return |
| 337 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output that the stock belongs to the lowest quantile bucket (bucket 0) among 4 quantile buckets for 1-day forw |
| 338 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 1 out of 4 buckets for the 1-day forward market-neutral return prediction |
| 339 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output for bucket 2 of 4 quantile buckets for 1-day forward market-neutral return prediction |
| 340 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from the model that the stock belongs to quantile bucket 3 out of 4 buckets (0 to 3) for the 1-day forward mar |
| 341 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to the lowest quantile bucket (bucket 0 of 5) for 1-day forward market-neutral ret |
| 342 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 1 out of 5 buckets (0 to 4) for the 1-day forward market-neutral ret |
| 343 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 2 (third quantile, bucket index 2 of 5) for 1-day forward marke |
| 344 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output for bucket 3 of 5 quantile buckets for 1-day forward market-neutral return prediction |
| 345 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to the highest quantile bucket (bucket 4 of 5) for 1-day forward market-neutral re |
| 346 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output predicting market-neutral cross-sectional 5-day forward stock return, winsorized before use |
| 347 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to the lowest quantile bucket (bucket 0 of 2) for 5-day forward market-neutral ret |
| 348 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 1 out of 2 buckets (0 to 1) for the 5-day forward market-neutral ret |
| 349 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) for bucket 0 out of 3 quantile buckets at 5-day forward market-neutral return |
| 350 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) for bucket 1 out of 3 quantile buckets at 5-day forward market-neutral return |
| 351 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from model predicting the stock belongs to quantile bucket 2 out of 3 buckets for 5-day forward market-neutral |
| 352 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to the lowest quantile bucket (bucket 0 of 4) for 5-day forward market-neutral ret |
| 353 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output for bucket 1 of 4 quantile buckets for 5-day forward market-neutral return prediction |
| 354 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 2 out of 4 buckets (0 to 3) for the 5-day forward market-neutral ret |
| 355 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 3 out of 4 buckets for the 5-day forward market-neutral return prediction |
| 356 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) for bucket 0 out of 5 quantile buckets at 5-day forward market-neutral return |
| 357 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 (second quantile, bucket index 1 of 5) for 5-day forward mark |
| 358 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 2 out of 5 buckets (0 to 4) for the 5-day forward market-neutral ret |
| 359 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from model predicting the stock belongs to quantile bucket 3 out of 5 buckets for 5-day forward market-neutral |
| 360 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from model predicting the stock belongs to quantile bucket 4 (highest bucket) out of 5 buckets for 5-day forwa |
| 361 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output for 10-day forward market-neutral return prediction in European universe using Techindi16 overlay |
| 362 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for ten-day return, bucket zero. |
| 363 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Likelihood that a stock is in the second quantile for ten-day return, bucket one. |
| 364 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence that the stock-date belongs to the lowest quantile bucket (bucket index 0) out of 3 buckets f |
| 365 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 1 out of 3 quantile buckets (0 to 2) for 10-day forward market-neutral return predicti |
| 366 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 10-day forward market-neutral return prediction belongs to quantile bucket 2 out of 3 buckets |
| 367 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock falls into the fourth quantile for ten-day return, bucket zero. |
| 368 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket one. |
| 369 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 2 out of 4 quantile buckets (0 to 3) for 10-day forward market-neutral return predicti |
| 370 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 3 out of 4 buckets for 10-day forward return prediction |
| 371 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket zero. |
| 372 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 10-day forward market-neutral return prediction belongs to quantile bucket 1 out of 5 buckets |
| 373 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence that the stock-date belongs to quantile bucket 2 (third bucket out of 5) for 10-day forward m |
| 374 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 3 out of 5 buckets for 10-day forward return prediction |
| 375 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket four. |
| 376 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output for 1-day forward market-neutral return prediction; represents cross-sectionally demeaned return prediction |
| 377 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for one-day return, bucket zero. |
| 378 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 1-day forward market-neutral return prediction belongs to quantile bucket 1 out of 2 buckets |
| 379 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket zero. |
| 380 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model probability that stock-date belongs to quantile bucket 1 of 3 for 1-day forward market-neutral return |
| 381 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 1-day forward market-neutral return prediction belongs to quantile bucket 2 out of 3 buckets |
| 382 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 1-day forward market-neutral return prediction belongs to quantile bucket 0 out of 4 buckets |
| 383 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 1 out of 4 buckets for 1-day forward return prediction |
| 384 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 1-day forward market-neutral return prediction belongs to quantile bucket 2 out of 4 buckets |
| 385 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 1-day forward market-neutral return prediction belongs to quantile bucket 3 out of 4 buckets |
| 386 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) for bucket 0 of 5 quantile buckets in 1-day forward market-neutral return prediction |
| 387 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 1-day forward market-neutral return prediction belongs to quantile bucket 1 out of 5 buckets |
| 388 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 2 out of 5 buckets for 1-day forward return prediction |
| 389 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) for bucket 3 of 5 quantile buckets in 1-day forward market-neutral return prediction |
| 390 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 4 out of 5 quantile buckets (0 to 4) for 1-day forward market-neutral return predictio |
| 391 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Continuous regression output for 5-day forward market-neutral return prediction; cross-sectionally demeaned return model estimate |
| 392 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence that the stock-date belongs to the lowest quantile bucket (bucket index 0) out of 2 buckets f |
| 393 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 1 out of 2 buckets for 5-day forward return prediction |
| 394 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for five-day return, bucket zero. |
| 395 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 5-day forward market-neutral return prediction belongs to quantile bucket 1 out of 3 buckets |
| 396 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the 5-day forward market-neutral return prediction belongs to quantile bucket 2 out of 3 buckets |
| 397 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence that the stock-date belongs to the lowest quantile bucket (bucket index 0) out of 4 buckets f |
| 398 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 1 out of 4 quantile buckets (0 to 3) for 5-day forward market-neutral return predictio |
| 399 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 2 out of 4 quantile buckets (0 to 3) for 5-day forward market-neutral return predictio |
| 400 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 3 out of 4 buckets for 5-day forward return prediction |
| 401 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 0 out of 5 quantile buckets (0 to 4) for 5-day forward market-neutral return predictio |
| 402 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 1 out of 5 quantile buckets (0 to 4) for 5-day forward market-neutral return predictio |
| 403 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) for bucket 2 of 5 quantile buckets in 5-day forward market-neutral return prediction |
| 404 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 3 out of 5 buckets for 5-day forward return prediction |
| 405 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket four. |
| 406 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output for 10-day forward market-neutral return prediction, unbounded float, strictly D1-lagged, to be winsorized befo |
| 407 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 0 out of 2 buckets for 10-day forward market-neutral return predicti |
| 408 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 1 out of 2 buckets for 10-day forward market-neutral return predicti |
| 409 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output of the model that the stock-date belongs to quantile bucket 0 of 3 for the 10-day forward market-neutra |
| 410 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for ten-day return, bucket one. |
| 411 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned to quantile bucket 2 out of 3 for 10-day forward market-neutral return prediction; exp(value) gives m |
| 412 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 0 out of 4 buckets for 10-day forward market-neutral return predicti |
| 413 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket one. |
| 414 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 2 out of 4 buckets for 10-day forward market-neutral return predicti |
| 415 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence for the 4th quantile bucket (bucket index 3) in EUR region, 10-day forward market-neutral ret |
| 416 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output of the model that the stock-date belongs to quantile bucket 0 of 5 for the 10-day forward market-neutra |
| 417 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence for the 2nd quantile bucket (bucket index 1) in EUR region, 10-day forward market-neutral ret |
| 418 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket two. |
| 419 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket three. |
| 420 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned to highest quantile bucket 4 out of 5 for 10-day forward market-neutral return prediction; exp(value) |
| 421 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output, 1-day forward market-neutral return prediction |
| 422 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for one-day return, bucket zero. |
| 423 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 1 out of 2 buckets for 1-day forward market-neutral return predictio |
| 424 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket zero. |
| 425 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence for the 2nd quantile bucket (bucket index 1) in EUR region, 1-day forward market-neutral retu |
| 426 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 2 out of 3 buckets for 1-day forward market-neutral return predictio |
| 427 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned to lowest quantile bucket 0 out of 4 for 1-day forward market-neutral return prediction; exp(value) g |
| 428 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence for the 2nd quantile bucket (bucket index 1) in EUR region, 1-day forward market-neutral retu |
| 429 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 2 out of 4 buckets for 1-day forward market-neutral return predictio |
| 430 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned to quantile bucket 3 out of 4 for 1-day forward market-neutral return prediction; exp(value) gives mo |
| 431 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket zero. |
| 432 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output of the model that the stock-date belongs to quantile bucket 1 of 5 for the 1-day forward market-neutral |
| 433 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output of the model that the stock-date belongs to quantile bucket 2 of 5 for the 1-day forward market-neutral |
| 434 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket three. |
| 435 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output of the model that the stock-date belongs to quantile bucket 4 of 5 for the 1-day forward market-neutral |
| 436 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output (market-neutral, winsorized) estimating the 5-day forward return for the stock-date |
| 437 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the second quantile for five-day return, bucket zero. |
| 438 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output that the stock-date belongs to quantile bucket 1 of 2 for the 5-day forward market-neutral return predi |
| 439 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for five-day return, bucket zero. |
| 440 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for five-day return, bucket one. |
| 441 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 2 out of 3 buckets for 5-day forward market-neutral return predictio |
| 442 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) output of the model that the stock-date belongs to quantile bucket 0 of 4 for the 5-day forward market-neutral |
| 443 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 1 out of 4 buckets for 5-day forward market-neutral return predictio |
| 444 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned to quantile bucket 2 out of 4 for 5-day forward market-neutral return prediction; exp(value) gives mo |
| 445 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence for the 4th quantile bucket (bucket index 3) in EUR region, 5-day forward market-neutral retu |
| 446 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence for the lowest quantile bucket (bucket index 0) in EUR region, 5-day forward market-neutral r |
| 447 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket one. |
| 448 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket two. |
| 449 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for five-day return, bucket three. |
| 450 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model confidence for the highest quantile bucket (bucket index 4) in EUR region, 5-day forward market-neutral  |
| 451 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output (winsorized) estimating 10-day forward market-neutral return |
| 452 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the lowest quantile bucket (index 0) out of 2 buckets for the 10-day forward market-neutr |
| 453 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for being in quantile bucket 1 out of 2 (buckets 0 and 1) for the 10-day forward market-neutral r |
| 454 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output that the stock-date belongs to quantile bucket 0 out of 3 buckets for the 10-day forward market-n |
| 455 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 1 out of 3 quantile buckets for 10-day forward market-neutral return prediction in Eur |
| 456 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for being in quantile bucket 2 out of 3 (buckets 0 to 2) for the 10-day forward market-neutral re |
| 457 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 0 out of 4 quantile buckets for 10-day forward market-neutral return prediction in Eur |
| 458 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 out of 4 buckets for the 10-day forward market-neutral return |
| 459 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the 3rd quantile bucket (index 2) out of 4 buckets for the 10-day forward market-neutral  |
| 460 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 3 out of 4 quantile buckets for 10-day forward market-neutral return prediction in Eur |
| 461 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 0 (lowest bucket) out of 5 for 10-day forward market-neutral return prediction |
| 462 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 out of 5 buckets for the 10-day forward market-neutral return |
| 463 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the 3rd quantile bucket (index 2) out of 5 buckets for the 10-day forward market-neutral  |
| 464 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for being in quantile bucket 3 out of 5 (buckets 0 to 4) for the 10-day forward market-neutral re |
| 465 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the highest quantile bucket (index 4) out of 5 buckets for the 10-day forward market-neut |
| 466 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output predicting the 1-day forward market-neutral return, as a float value (not a quantile) |
| 467 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 0 (lowest quantile) out of 2 quantile buckets for 1-day forward market-neutral return  |
| 468 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 1 out of 2 for 1-day forward market-neutral return prediction |
| 469 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the lowest quantile bucket (index 0) out of 3 buckets for the 1-day forward market-neutra |
| 470 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for being in quantile bucket 1 out of 3 (buckets 0 to 2) for the 1-day forward market-neutral ret |
| 471 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for being in quantile bucket 2 out of 3 (buckets 0 to 2) for the 1-day forward market-neutral ret |
| 472 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output that the stock-date belongs to quantile bucket 0 out of 4 buckets for the 1-day forward market-ne |
| 473 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output that the stock-date belongs to quantile bucket 1 out of 4 buckets for the 1-day forward market-ne |
| 474 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 2 out of 4 buckets for the 1-day forward market-neutral return  |
| 475 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the 4th quantile bucket (index 3) out of 4 buckets for the 1-day forward market-neutral r |
| 476 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 0 out of 5 quantile buckets for 1-day forward market-neutral return prediction in Euro |
| 477 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 out of 5 buckets for the 1-day forward market-neutral return  |
| 478 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the 3rd quantile bucket (index 2) out of 5 buckets for the 1-day forward market-neutral r |
| 479 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax output) that the stock belongs to quantile bucket 3 out of 5 for 1-day forward market-neutral return prediction |
| 480 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output that the stock-date belongs to quantile bucket 4 out of 5 buckets for the 1-day forward market-ne |
| 481 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output for the 5-day forward market-neutral return prediction, must be winsorized before use |
| 482 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 0 out of 3 buckets for the 5-day forward market-neutral return  |
| 483 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 out of 3 buckets for the 5-day forward market-neutral return  |
| 484 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output that the stock-date belongs to quantile bucket 0 out of 3 buckets for the 5-day forward market-ne |
| 485 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for being in quantile bucket 1 out of 3 (buckets 0 to 2) for the 5-day forward market-neutral ret |
| 486 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 2 out of 3 quantile buckets for 5-day forward market-neutral return prediction in Euro |
| 487 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 0 out of 4 buckets for the 5-day forward market-neutral return  |
| 488 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 1 out of 4 quantile buckets for 5-day forward market-neutral return prediction in Euro |
| 489 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the 3rd quantile bucket (index 2) out of 4 buckets for the 5-day forward market-neutral r |
| 490 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock is in the 4th quantile bucket (index 3) out of 4 buckets for the 5-day forward market-neutral r |
| 491 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 0 out of 5 for 5-day forward market-neutral return prediction |
| 492 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for bucket 1 out of 5 quantile buckets for 5-day forward market-neutral return prediction in Euro |
| 493 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 2 out of 5 for 5-day forward market-neutral return prediction |
| 494 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 3 out of 5 for 5-day forward market-neutral return prediction |
| 495 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output that the stock-date belongs to quantile bucket 4 out of 5 buckets for the 5-day forward market-ne |
| 496 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output predicting 10-day forward market-neutral (cross-sectionally demeaned) return; requires winsorization before use |
| 497 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 0 out of 2 for 10-day forward market-neutral return prediction in EU |
| 498 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 1 out of 2 quantile buckets for 10-day forward market-neutral return predictio |
| 499 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, label zero. |
| 500 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 out of 3 for 10-day forward market-neutral return prediction |
| 501 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 10-day forward return prediction is in quantile bucket 2 out of 3 buckets; exp(value) gives actual probability |
| 502 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, label zero. |
| 503 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 1 out of 4 for 10-day forward market-neutral return prediction in EU |
| 504 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 2 out of 4 quantile buckets for 10-day forward market-neutral return predictio |
| 505 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, label three. |
| 506 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to the lowest quantile bucket (bucket 0) out of 5 buckets fo |
| 507 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fifth quantile, label one. |
| 508 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 2 out of 5 for 10-day forward market-neutral return prediction |
| 509 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 3 out of 5 for 10-day forward market-neutral return prediction in EU |
| 510 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to highest quantile bucket 4 out of 5 for 10-day forward market-neutral return pre |
| 511 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output estimating 1-day forward market-neutral stock return; must be winsorized before use |
| 512 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the 1-day forward return prediction belongs to quantile bucket 0 out of 2 buckets; exp(value) gives the a |
| 513 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the second quantile, label one. |
| 514 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to quantile bucket 0 out of 3 for 1-day forward market-neutral return prediction in EUR |
| 515 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 1 out of 3 quantile buckets for 1-day forward market-neutral return prediction |
| 516 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 1-day forward return prediction is in quantile bucket 2 out of 3 buckets; exp(value) gives actual probability |
| 517 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to lowest quantile bucket 0 out of 4 for 1-day forward market-neutral return predi |
| 518 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 1 out of 4 quantile buckets for 1-day forward market-neutral return prediction |
| 519 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 2 out of 4 quantile buckets for 1-day forward market-neutral return prediction |
| 520 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 3 out of 4 for 1-day forward market-neutral return prediction |
| 521 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, label zero. |
| 522 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 out of 5 for 1-day forward market-neutral return prediction |
| 523 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 2 out of 5 for 1-day forward market-neutral return prediction |
| 524 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 3 out of 5 quantile buckets for 1-day forward market-neutral return prediction |
| 525 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to highest quantile bucket 4 out of 5 for 1-day forward market-neutral return pred |
| 526 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output for 5-day forward market-neutral return prediction in EUR universe |
| 527 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 0 out of 2 quantile buckets for 5-day forward market-neutral return prediction |
| 528 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 1 out of 2 buckets for 5-day forward mark |
| 529 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, label zero. |
| 530 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 out of 3 for 5-day forward market-neutral return prediction |
| 531 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 5-day forward return prediction is in quantile bucket 2 out of 3 buckets; exp(value) gives actual probability |
| 532 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 0 out of 4 quantile buckets for 5-day forward market-neutral return prediction |
| 533 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 1 out of 4 buckets for 5-day forward mark |
| 534 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 5-day forward return prediction is in quantile bucket 2 out of 4 buckets; exp(value) gives actual probability |
| 535 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model to bucket 3 out of 4 quantile buckets for 5-day forward market-neutral return prediction |
| 536 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to the lowest quantile bucket (bucket 0) out of 5 buckets fo |
| 537 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 1 out of 5 buckets for 5-day forward mark |
| 538 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 5-day forward return prediction is in quantile bucket 2 out of 5 buckets; exp(value) gives actual probability |
| 539 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 5-day forward return prediction is in quantile bucket 3 out of 5 buckets; exp(value) gives actual probability |
| 540 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the 5-day forward return prediction is in quantile bucket 4 out of 5 buckets; exp(value) gives actual probability |
| 541 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output predicting the 10-day forward market-neutral return; must be winsorized before use |
| 542 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 0 among 2 quantile buckets for the 10-day |
| 543 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 1 among 2 quantile buckets for the 10-day |
| 544 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for the lowest quantile bucket (index 0) out of 3 for the 10-day forward market-neutral return pr |
| 545 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) from the model that the stock-date belongs to quantile bucket 1 of 3 for 10-day forward market-neutral return  |
| 546 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 2 of 3 for 10-day forward market-neutral return prediction |
| 547 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to the lowest quantile bucket (bucket 0 of 4) for 10-day forward market-neutral return prediction |
| 548 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the second quantile bucket (bucket 1) for 10-day forward market-neutral return with  |
| 549 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the third quantile bucket (bucket 2) for 10-day forward market-neutral return with 4 |
| 550 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket three. |
| 551 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the lowest quantile bucket (bucket 0) for 10-day forward market-neutral return with  |
| 552 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 1 of 5 for 10-day forward market-neutral return prediction |
| 553 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the third quantile bucket (bucket 2) for 10-day forward market-neutral return with 5 |
| 554 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 3 of 5 for 10-day forward market-neutral return prediction |
| 555 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the highest quantile bucket (bucket 4) for 10-day forward market-neutral return with |
| 556 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output for 1-day forward market-neutral return prediction, needs winsorization before use |
| 557 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 0 among 2 quantile buckets for the 1-day  |
| 558 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 1 of 2 for 1-day forward market-neutral return prediction |
| 559 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 0 among 3 quantile buckets for the 1-day  |
| 560 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for the 2nd quantile bucket (index 1) out of 3 for the 1-day forward market-neutral return predic |
| 561 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 2 of 3 for 1-day forward market-neutral return prediction |
| 562 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, bucket zero. |
| 563 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for the 2nd quantile bucket (index 1) out of 4 for the 1-day forward market-neutral return predic |
| 564 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 2 of 4 for 1-day forward market-neutral return prediction |
| 565 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for the 4th quantile bucket (index 3) out of 4 for the 1-day forward market-neutral return predic |
| 566 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the lowest quantile bucket (bucket 0) for 1-day forward market-neutral return with 5 |
| 567 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the second quantile bucket (bucket 1) for 1-day forward market-neutral return with 5 |
| 568 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 2 among 5 quantile buckets for the 1-day  |
| 569 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 3 among 5 quantile buckets for the 1-day  |
| 570 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the highest quantile bucket (bucket 4 of 5) for 1-day forward market-neutral return  |
| 571 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output (winsorize before usage) predicting 5-day forward market-neutral return |
| 572 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 0 (lowest bucket) among 2 quantile bucket |
| 573 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second quantile, bucket one. |
| 574 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the lowest quantile bucket (bucket 0) for 5-day forward market-neutral return with 3 |
| 575 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 1 of 3 for 5-day forward market-neutral return prediction |
| 576 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock-date belongs to quantile bucket 2 among 3 quantile buckets for the 5-day  |
| 577 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to the lowest quantile bucket (bucket 0) out of 4 buckets for 5-day forward return |
| 578 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 1 of 4 for 5-day forward market-neutral return prediction |
| 579 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability that the stock belongs to quantile bucket 2 of 4 for 5-day forward market-neutral return prediction |
| 580 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for the 4th quantile bucket (index 3) out of 4 for the 5-day forward market-neutral return predic |
| 581 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fifth quantile, bucket zero. |
| 582 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock belongs to the second quantile bucket (bucket 1) for 5-day forward market-neutral return with 5 |
| 583 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 2 of 5 for 5-day forward market-neutral return prediction |
| 584 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for the 4th quantile bucket (index 3) out of 5 for the 5-day forward market-neutral return predic |
| 585 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) that the stock-date belongs to quantile bucket 4 of 5 for 5-day forward market-neutral return prediction |
| 586 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output of market-neutral 10-day forward return prediction |
| 587 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability of the stock being in quantile bucket 0 out of 2 (buckets 0 and 1) for 10-day forward market-neutral returns predicted by th |
| 588 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the second quantile, bucket one. |
| 589 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to lowest quantile bucket (bucket 0) out of 3 buckets for 10-day forward return prediction |
| 590 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the third quantile, bucket one. |
| 591 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 2 out of 3 buckets for 10-day forward return prediction |
| 592 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket zero. |
| 593 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the ten-day return falls into the fourth quantile, bucket one. |
| 594 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned to quantile bucket 2 of 4 buckets for the 10-day forward market-neutral return prediction |
| 595 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for ten-day return, bucket three. |
| 596 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket zero. |
| 597 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 1 out of 5 buckets for 10-day forward return prediction |
| 598 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 2 out of 5 buckets for 10-day forward return prediction |
| 599 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) model output for quantile bucket 3 out of 5 (buckets 0 to 4) for 10-day forward market-neutral return predicti |
| 600 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for ten-day return, bucket four. |
| 601 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output of 1-day forward market-neutral returns predicted by the EUR region model using tech indicator image variant 8, |
| 602 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) assigned by the model that the stock belongs to quantile bucket 0 out of 2 buckets for the 1-day forward marke |
| 603 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability of the stock being in quantile bucket 1 out of 2 (buckets 0 and 1) for 1-day forward market-neutral returns predicted by the |
| 604 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the third quantile for one-day return, bucket zero. |
| 605 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, bucket one. |
| 606 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the third quantile, bucket two. |
| 607 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fourth quantile for one-day return, bucket zero. |
| 608 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fourth quantile, bucket one. |
| 609 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability of the stock being in quantile bucket 2 out of 4 (buckets 0 to 3) for 1-day forward market-neutral returns predicted by the  |
| 610 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 3 out of 4 buckets for 1-day forward return prediction |
| 611 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket zero. |
| 612 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability of the stock being in quantile bucket 1 out of 5 (buckets 0 to 4) for 1-day forward market-neutral returns predicted by the  |
| 613 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket two. |
| 614 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that a stock is in the fifth quantile for one-day return, bucket three. |
| 615 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the one-day return falls into the fifth quantile, bucket four. |
| 616 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Continuous regression output of 5-day forward market-neutral returns predicted by the EUR region model using tech indicator image variant 8, |
| 617 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q2_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the second quantile, bucket zero. |
| 618 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q2_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 1 out of 2 buckets for 5-day forward return prediction |
| 619 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q3_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, bucket zero. |
| 620 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q3_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the third quantile, bucket one. |
| 621 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q3_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to quantile bucket 2 out of 3 buckets for 5-day forward return prediction |
| 622 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q4_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to the lowest quantile bucket (bucket 0 of 4) for the 5-day forward market-neutral return predict |
| 623 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q4_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket one. |
| 624 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q4_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the five-day return falls into the fourth quantile, bucket two. |
| 625 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q4_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability of the stock being in quantile bucket 3 out of 4 (buckets 0 to 3) for 5-day forward market-neutral returns predicted by the  |
| 626 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q5_p0` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to the lowest quantile bucket (bucket 0 of 5) for the 5-day forward market-neutral return predict |
| 627 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q5_p1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability of the stock being in quantile bucket 1 out of 5 (buckets 0 to 4) for 5-day forward market-neutral returns predicted by the  |
| 628 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q5_p2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability of the stock being in quantile bucket 2 out of 5 (buckets 0 to 4) for 5-day forward market-neutral returns predicted by the  |
| 629 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q5_p3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to bucket 3 of 5 quantile buckets for the 5-day forward market-neutral return prediction |
| 630 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q5_p4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Log-probability (log-softmax) of belonging to the highest quantile bucket (bucket 4 of 5) for the 5-day forward market-neutral return predic |
| 631 | `predicted_fifth_quantile_five_bucket_return_2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted return value for the fifth quantile in a five-bucket ranking system. |
| 632 | `predicted_fifth_quantile_five_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the fifth quantile group. |
| 633 | `predicted_fifth_quantile_five_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the fifth quantile. |
| 634 | `predicted_fifth_quantile_five_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the fifth quantile group. |
| 635 | `predicted_fifth_quantile_five_day_return_151` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, fifth group. |
| 636 | `predicted_fifth_quantile_five_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, fifth group. |
| 637 | `predicted_fifth_quantile_five_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the fifth quantile group. |
| 638 | `predicted_fifth_quantile_one_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the fifth quantile group. |
| 639 | `predicted_fifth_quantile_one_day_return_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the fifth quantile. |
| 640 | `predicted_fifth_quantile_one_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the fifth quantile group. |
| 641 | `predicted_fifth_quantile_one_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the fifth quantile. |
| 642 | `predicted_fifth_quantile_one_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, fifth group. |
| 643 | `predicted_fifth_quantile_one_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, fifth group. |
| 644 | `predicted_fifth_quantile_one_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the fifth quantile group. |
| 645 | `predicted_fifth_quantile_ten_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the fifth quantile group. |
| 646 | `predicted_fifth_quantile_ten_day_return_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the fifth quantile. |
| 647 | `predicted_fifth_quantile_ten_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the fifth quantile group. |
| 648 | `predicted_fifth_quantile_ten_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the fifth quantile. |
| 649 | `predicted_fifth_quantile_ten_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, fifth group. |
| 650 | `predicted_fifth_quantile_ten_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, fifth group. |
| 651 | `predicted_fifth_quantile_ten_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the fifth quantile group. |
| 652 | `predicted_fourth_quantile_five_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the fourth quantile. |
| 653 | `predicted_fourth_quantile_five_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for a stock classified in the fourth quantile. |
| 654 | `predicted_fourth_quantile_five_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the fourth quantile group. |
| 655 | `predicted_fourth_quantile_five_day_return_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the fourth quantile. |
| 656 | `predicted_fourth_quantile_five_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, fourth group. |
| 657 | `predicted_fourth_quantile_five_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the fourth quantile group. |
| 658 | `predicted_fourth_quantile_five_day_return_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the fourth quantile group. |
| 659 | `predicted_fourth_quantile_one_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the fourth quantile group. |
| 660 | `predicted_fourth_quantile_one_day_return_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the fourth quantile. |
| 661 | `predicted_fourth_quantile_one_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the fourth quantile group. |
| 662 | `predicted_fourth_quantile_one_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the fourth quantile. |
| 663 | `predicted_fourth_quantile_one_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, fourth group. |
| 664 | `predicted_fourth_quantile_one_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, fourth group. |
| 665 | `predicted_fourth_quantile_one_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the fourth quantile group. |
| 666 | `predicted_fourth_quantile_ten_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the fourth quantile group. |
| 667 | `predicted_fourth_quantile_ten_day_return_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the fourth quantile. |
| 668 | `predicted_fourth_quantile_ten_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the fourth quantile group. |
| 669 | `predicted_fourth_quantile_ten_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the fourth quantile. |
| 670 | `predicted_fourth_quantile_ten_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, fourth group. |
| 671 | `predicted_fourth_quantile_ten_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, fourth group. |
| 672 | `predicted_fourth_quantile_ten_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the fourth quantile group. |
| 673 | `predicted_second_quantile_five_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the second quantile. |
| 674 | `predicted_second_quantile_five_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for a stock classified in the second quantile. |
| 675 | `predicted_second_quantile_five_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the second quantile group. |
| 676 | `predicted_second_quantile_five_day_return_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the second quantile. |
| 677 | `predicted_second_quantile_five_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, second group. |
| 678 | `predicted_second_quantile_five_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, second group. |
| 679 | `predicted_second_quantile_five_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the second quantile group. |
| 680 | `predicted_second_quantile_one_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the second quantile. |
| 681 | `predicted_second_quantile_one_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for a stock classified in the second quantile. |
| 682 | `predicted_second_quantile_one_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the second quantile group. |
| 683 | `predicted_second_quantile_one_day_return_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the second quantile. |
| 684 | `predicted_second_quantile_one_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, second group. |
| 685 | `predicted_second_quantile_one_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, second group. |
| 686 | `predicted_second_quantile_one_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the second quantile group. |
| 687 | `predicted_second_quantile_ten_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the second quantile group. |
| 688 | `predicted_second_quantile_ten_day_return_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the second quantile. |
| 689 | `predicted_second_quantile_ten_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the second quantile group. |
| 690 | `predicted_second_quantile_ten_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the second quantile. |
| 691 | `predicted_second_quantile_ten_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, second group. |
| 692 | `predicted_second_quantile_ten_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, second group. |
| 693 | `predicted_second_quantile_ten_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the second quantile group. |
| 694 | `predicted_third_quantile_five_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the third quantile group. |
| 695 | `predicted_third_quantile_five_day_return_131` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the third quantile. |
| 696 | `predicted_third_quantile_five_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the third quantile group. |
| 697 | `predicted_third_quantile_five_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the third quantile. |
| 698 | `predicted_third_quantile_five_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, third group. |
| 699 | `predicted_third_quantile_five_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return quantile, third group. |
| 700 | `predicted_third_quantile_five_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the third quantile group. |
| 701 | `predicted_third_quantile_one_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the third quantile. |
| 702 | `predicted_third_quantile_one_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for a stock classified in the third quantile. |
| 703 | `predicted_third_quantile_one_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the third quantile group. |
| 704 | `predicted_third_quantile_one_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, third group. |
| 705 | `predicted_third_quantile_one_day_return_16` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, third group. |
| 706 | `predicted_third_quantile_one_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the third quantile group. |
| 707 | `predicted_third_quantile_one_day_return_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the third quantile group. |
| 708 | `predicted_third_quantile_ten_day_return_13` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the third quantile. |
| 709 | `predicted_third_quantile_ten_day_return_14` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for a stock classified in the third quantile. |
| 710 | `predicted_third_quantile_ten_day_return_141` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the third quantile group. |
| 711 | `predicted_third_quantile_ten_day_return_142` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the third quantile. |
| 712 | `predicted_third_quantile_ten_day_return_15` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, third group. |
| 713 | `predicted_third_quantile_ten_day_return_17` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the third quantile group. |
| 714 | `predicted_third_quantile_ten_day_return_18` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the third quantile group. |
| 715 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the second quantile group. |
| 716 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) for 10-day forward market-neutral return prediction using technical indicator chart images for the EUR  |
| 717 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based over 4 buckets) for market-neutral cross-sectional 10-day forward stock return prediction |
| 718 | `tm_15_r1_r5_r10_rh_glb_d1_r10_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return for stocks in the fifth quantile group. |
| 719 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return for stocks in the second quantile group. |
| 720 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) for 1-day forward market-neutral return prediction using technical indicator chart images for the EUR u |
| 721 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) out of 4 buckets for 1-day forward market-neutral return prediction in the EUR universe |
| 722 | `tm_15_r1_r5_r10_rh_glb_d1_r1_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) into one of 5 buckets (0 to 4) for the 1-day forward market-neutral return prediction |
| 723 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the second quantile group. |
| 724 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based over 3 buckets) for market-neutral cross-sectional 5-day forward stock return prediction |
| 725 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted five-day return for stocks in the fourth quantile group. |
| 726 | `tm_15_r1_r5_r10_rh_glb_d1_r5_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) into one of 5 buckets (0 to 4) for the 5-day forward market-neutral return prediction |
| 727 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 10-day forward market-neutral return prediction with 2 buckets (0-based indexing) |
| 728 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 10-day forward market-neutral return with 3 buckets (0-based indexing) |
| 729 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 10-day forward market-neutral return with 4 buckets (0-based indexing) |
| 730 | `tm_16_r1_r5_r10_rh_glb_d1_r10_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 10-day forward market-neutral return with 5 buckets (0-based indexing) |
| 731 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 1-day forward market-neutral return prediction with 2 buckets (0-based indexing) |
| 732 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 1-day forward market-neutral return with 3 buckets (0-based indexing) |
| 733 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) out of 4 buckets for 1-day forward market-neutral return prediction in EUR universe |
| 734 | `tm_16_r1_r5_r10_rh_glb_d1_r1_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) out of 5 buckets for 1-day forward market-neutral return prediction in EUR universe |
| 735 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) out of 2 buckets for 5-day forward market-neutral return prediction in EUR universe |
| 736 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 5-day forward market-neutral return prediction with 3 buckets (0-based indexing) |
| 737 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 5-day forward market-neutral return with 4 buckets (0-based indexing) |
| 738 | `tm_16_r1_r5_r10_rh_glb_d1_r5_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment into one of 5 buckets (0-based indices 0 to 4) for 5-day forward market-neutral return prediction |
| 739 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 10-day forward market-neutral return prediction with 3 quantile buckets (value 0 to 2) |
| 740 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) into 3 buckets for the 10-day forward market-neutral return prediction in EUR region |
| 741 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile assignment (bucket index 0 to 3) for 10-day forward return prediction with 4 buckets |
| 742 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) for 10-day forward market-neutral return prediction into 5 buckets in EUR universe using technical indi |
| 743 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) into 2 buckets for the 1-day forward market-neutral return prediction in EUR region |
| 744 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment of the stock-date into one of 3 buckets (0 to 2) for the 1-day forward market-neutral return prediction |
| 745 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile assignment (bucket index 0 to 3) for 1-day forward return prediction with 4 buckets |
| 746 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r1_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 1-day forward market-neutral return prediction with 5 quantile buckets (value 0 to 4) |
| 747 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment of the stock-date into one of 2 buckets (0 or 1) for the 5-day forward market-neutral return prediction |
| 748 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 0 to 2) for 5-day forward market-neutral return prediction for stocks in the EUR universe, using Techin |
| 749 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) into 4 buckets for the 5-day forward market-neutral return prediction in EUR region |
| 750 | `tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 0 to 4) for 5-day forward market-neutral return prediction for stocks in the EUR universe, using Techin |
| 751 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) to one of 2 buckets (0 and 1) for the 10-day forward market-neutral return prediction |
| 752 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 3 buckets) for 10-day forward market-neutral return prediction in European universe |
| 753 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) among 4 buckets for the 10-day forward market-neutral return prediction |
| 754 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r10_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) among 5 buckets for the 10-day forward market-neutral return prediction |
| 755 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) among 2 buckets for the 1-day forward market-neutral return prediction |
| 756 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 3 buckets) for 1-day forward market-neutral return prediction in European universe |
| 757 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) to one of 4 buckets (0 to 3) for the 1-day forward market-neutral return prediction |
| 758 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r1_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) of the stock into one of 5 buckets for 1-day forward market-neutral return prediction |
| 759 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) of the stock into one of 2 buckets for 5-day forward market-neutral return prediction |
| 760 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) to one of 3 buckets (0 to 2) for the 5-day forward market-neutral return prediction |
| 761 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) of the stock into one of 4 buckets for 5-day forward market-neutral return prediction |
| 762 | `tm_18_r1_r5_r10_rh_ah3_glb_d1_r5_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) to one of 5 buckets (0 to 4) for the 5-day forward market-neutral return prediction |
| 763 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted ten-day return quantile, second group. |
| 764 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) of the stock-date into one of 3 buckets for 10-day forward market-neutral return prediction |
| 765 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) of the stock-date into one of 4 buckets for 10-day forward market-neutral return prediction |
| 766 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r10_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, from 0 to 4) for 10-day forward market-neutral return prediction in EUR universe |
| 767 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) into 2 buckets for the 1-day forward market-neutral return prediction |
| 768 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) into 3 buckets for 1-day forward market-neutral return prediction in the EUR universe |
| 769 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) of the stock-date into one of 4 buckets for 1-day forward market-neutral return prediction |
| 770 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r1_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted one-day return quantile, fifth group. |
| 771 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, from 0 to 1) for 5-day forward market-neutral return prediction in EUR universe |
| 772 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) into 3 buckets for the 5-day forward market-neutral return prediction |
| 773 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) of the stock-date into one of 4 buckets for 5-day forward market-neutral return prediction |
| 774 | `tm_19_r1_r5_r10_rh_ah3_glb_d1_r5_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 5 buckets) for 5-day forward market-neutral return prediction |
| 775 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) among 2 buckets for 10-day forward market-neutral return prediction |
| 776 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) among 3 buckets for 10-day forward market-neutral return prediction |
| 777 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 4 buckets) of the stock-date for 10-day forward market-neutral return prediction |
| 778 | `tm_1_r1_r5_r10_rh_glb_d1_r10_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) among 5 buckets for 10-day forward market-neutral return prediction |
| 779 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0 or 1) indicating which of 2 quantile buckets the stock-date belongs to for the 1-day forward market-neutral re |
| 780 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile assignment to one of 3 buckets (0 to 2) for the 1-day forward market-neutral return prediction, strictly D1-lagged |
| 781 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) for 1-day forward market-neutral return with 4 quantile buckets |
| 782 | `tm_1_r1_r5_r10_rh_glb_d1_r1_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) among 5 buckets for 1-day forward market-neutral return prediction |
| 783 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) among 2 buckets for 5-day forward market-neutral return prediction |
| 784 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0, 1, or 2) indicating which of 3 quantile buckets the stock-date belongs to for the 5-day forward market-neutra |
| 785 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 4 buckets) of the stock-date for 5-day forward market-neutral return prediction |
| 786 | `tm_1_r1_r5_r10_rh_glb_d1_r5_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment for 5-day forward market-neutral return prediction, with 5 buckets indexed 0 to 4 |
| 787 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the second quantile. |
| 788 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the third quantile. |
| 789 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for ten-day return in the fourth quantile. |
| 790 | `tm_8_r1_r5_r10_rh_glb_d1_r10_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 5 buckets) for market-neutral 10-day forward return prediction |
| 791 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for one-day return in the second quantile. |
| 792 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) with 3 buckets (0,1,2) for 1-day forward market-neutral returns predicted by the EUR region model using |
| 793 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) assigning each stock to one of 4 buckets (0 to 3) based on the model's prediction for 1-day forward mar |
| 794 | `tm_8_r1_r5_r10_rh_glb_d1_r1_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0 based, 0 to 4) for 1-day forward market-neutral return prediction in EUR global universe |
| 795 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted label for five-day return in the second quantile. |
| 796 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) assigning the stock to one of 3 buckets (indices 0,1,2) for the 5-day forward market-neutral return pre |
| 797 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q4` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based, 4 buckets) for market-neutral 5-day forward return prediction |
| 798 | `tm_8_r1_r5_r10_rh_glb_d1_r5_q5` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Quantile bucket assignment (0-based) assigning each stock to one of 5 buckets (0 to 4) based on the model's prediction for 5-day forward mar |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-BUCKET-AXIS-NOT-A-DECORRELATOR`（2026-10-19）family=analyst_factor_signals：{"ablation_control": "KPmE8klx = signed_power(group_zscore(netprofit_y2_estimate_change_3mo, subindustry), 1.8) @ EUR/TOP2500/d1/decay10/FAST/trunc0.08/maxTrade ON/nanHandling ON. Batch J adds ONLY the outer bucket wrapper at identical settings => pure single-variable ablation.", "cost_table": {"double_bucket_25cell": {"alpha": "zqrROE1K", "d_fitness": -0.37, "d_sharpe": -0.26, "margin": 0.001671,

