# chart_cnn_alpha — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `chart_cnn_alpha` |
| 名称 | Deep Learning Chart-Based Alpha |
| 类别 | MODEL |
| 数据字段数(平台) | 122 |
| 覆盖率 | 0.6916 |
| 平台已有 alpha | 27 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset leverages deep learning to predict future stock returns by mimicking the decision-making process of retail traders who analyze price charts. It transforms time series financial data into images (such as OHLC or other chart types) and applies pre-trained convolutional neural networks (CNNs) to these images to generate return forecasts. The output includes both raw return predictions and quantile-based relative return rankings, along with associated probabilities. By capturing complex visual patterns and technical signals that may be overlooked by traditional quantitative models, this approach can identify non-linear relationships and subtle chart features that are predictive of price movements. The dataset is particularly useful for developing and testing alpha models that seek

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **122** |
| 类型分布 | MATRIX×122 |
| 平均覆盖率 | **0.692** |
| 覆盖率区间 | 0.54 ~ 0.98 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 40 | 32.8% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 82 | 67.2% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 79 | 64.8% |
| UNTESTED | 39 | 32.0% |
| DEAD | 3 | 2.5% |
| WEAK | 1 | 0.8% |

- 已实测字段：**4** 个（3%），best_sharpe 最高 **1.36**，中位 1.06

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 88 | 0.69 | img_leapstar6_r30_q2_prob_class0、img_leapstar6_r30_q2_prob_class1、img_leapstar6_r30_q3_prob_class0 |
| 其他 | 26 | 0.71 | img_malta2_r50_q3_quantile_label、img_malta2_r50_q4_quantile_label、img_malta2_r50_q5_quantile_label |
| 宏观与行业 | 8 | 0.67 | eur_img_feature1_leapstar6_d1、eur_img_feature2_leapstar6_d1、eur_img_feature1_malta1_d1 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `eur_img_feature1_leapstar6_d1` | MATRIX | 0.981 | 宏观与行业 | 4 | 1.36 | 0.70 | — | WEAK | First extracted image-based feature for the EUR region, using the Leap Star6 model, daily frequency. |
| 2 | `img_malta2_r50_q3_quantile_label` | MATRIX | 0.541 | 其他 | 1 | 1.06 | 1.59 | — | DEAD | Predicted quantile label (1-3) for 50-day horizon using Malta2 image-based model. |
| 3 | `img_malta2_r50_q4_quantile_label` | MATRIX | 0.541 | 其他 | 1 | 0.89 | 1.63 | — | DEAD | Predicted quantile label (1-4) for 50-day horizon using Malta2 image-based model. |
| 4 | `img_malta2_r50_q5_quantile_label` | MATRIX | 0.541 | 其他 | 3 | 0.88 | 1.78 | — | DEAD | Predicted quantile label (1-5) for 50-day horizon using Malta2 image-based model. |
| 5 | `eur_img_feature2_leapstar6_d1` | MATRIX | 0.968 | 宏观与行业 | 0 | — | — | — | UNTESTED | Second extracted image-based feature for the EUR region, using the Leap Star6 model, daily frequency. |
| 6 | `img_leapstar6_r30_q1_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-quantile, i.e., all-in-one) for 30-day horizon using LeapStar6 image-based model. |
| 7 | `img_leapstar6_r30_q2_prob_class0` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 0 in 2-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 8 | `img_leapstar6_r30_q2_prob_class1` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 1 in 2-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 9 | `img_leapstar6_r30_q2_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-2) for 30-day horizon using LeapStar6 image-based model. |
| 10 | `img_leapstar6_r30_q3_prob_class0` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 0 in 3-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 11 | `img_leapstar6_r30_q3_prob_class1` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 1 in 3-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 12 | `img_leapstar6_r30_q3_prob_class2` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 2 in 3-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 13 | `img_leapstar6_r30_q3_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-3) for 30-day horizon using LeapStar6 image-based model. |
| 14 | `img_leapstar6_r30_q4_prob_class0` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 0 in 4-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 15 | `img_leapstar6_r30_q4_prob_class1` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 1 in 4-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 16 | `img_leapstar6_r30_q4_prob_class2` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 2 in 4-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 17 | `img_leapstar6_r30_q4_prob_class3` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 3 in 4-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 18 | `img_leapstar6_r30_q4_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-4) for 30-day horizon using LeapStar6 image-based model. |
| 19 | `img_leapstar6_r30_q5_prob_class0` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 0 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 20 | `img_leapstar6_r30_q5_prob_class1` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 1 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 21 | `img_leapstar6_r30_q5_prob_class2` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 2 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 22 | `img_leapstar6_r30_q5_prob_class3` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 3 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 23 | `img_leapstar6_r30_q5_prob_class4` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 4 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| 24 | `img_leapstar6_r30_q5_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-5) for 30-day horizon using LeapStar6 image-based model. |
| 25 | `img_leapstar6_r5_q1_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-quantile, i.e., all-in-one) for 5-day horizon using LeapStar6 image-based model. |
| 26 | `img_leapstar6_r5_q2_prob_class0` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 0 in 2-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 27 | `img_leapstar6_r5_q2_prob_class1` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 1 in 2-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 28 | `img_leapstar6_r5_q2_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-2) for 5-day horizon using LeapStar6 image-based model. |
| 29 | `img_leapstar6_r5_q3_prob_class0` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 0 in 3-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 30 | `img_leapstar6_r5_q3_prob_class1` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 1 in 3-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 31 | `img_leapstar6_r5_q3_prob_class2` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 2 in 3-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 32 | `img_leapstar6_r5_q3_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-3) for 5-day horizon using LeapStar6 image-based model. |
| 33 | `img_leapstar6_r5_q4_prob_class0` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 0 in 4-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 34 | `img_leapstar6_r5_q4_prob_class1` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 1 in 4-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 35 | `img_leapstar6_r5_q4_prob_class2` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 2 in 4-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 36 | `img_leapstar6_r5_q4_prob_class3` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 3 in 4-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 37 | `img_leapstar6_r5_q4_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-4) for 5-day horizon using LeapStar6 image-based model. |
| 38 | `img_leapstar6_r5_q5_prob_class0` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 0 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 39 | `img_leapstar6_r5_q5_prob_class1` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 1 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 40 | `img_leapstar6_r5_q5_prob_class2` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 2 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 41 | `img_leapstar6_r5_q5_prob_class3` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 3 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 42 | `img_leapstar6_r5_q5_prob_class4` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted probability for class 4 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| 43 | `img_leapstar6_r5_q5_quantile_label` | MATRIX | 0.968 | 其他 | 0 | — | — | — | UNTESTED | Predicted quantile label (1-5) for 5-day horizon using LeapStar6 image-based model. |
| 44 | `eur_img_feature1_malta1_d1` | MATRIX | 0.579 | 宏观与行业 | 0 | — | — | — | UNUSABLE | First extracted image-based feature for the EUR region, using the first Malta model, daily frequency. |
| 45 | `eur_img_feature2_malta1_d1` | MATRIX | 0.579 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Second extracted image-based feature for the EUR region, using the first Malta model, daily frequency. |
| 46 | `img_malta1_r180_q1_quantile_label` | MATRIX | 0.572 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-quantile, i.e., all-in-one) for 180-day horizon using Malta1 image-based model. |
| 47 | `img_malta1_r180_q2_prob_class0` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 2-quantile return prediction for 180-day horizon using Malta1 image model. |
| 48 | `img_malta1_r180_q2_quantile_label` | MATRIX | 0.572 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-2) for 180-day horizon using Malta1 image-based model. |
| 49 | `img_malta1_r180_q3_prob_class0` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 3-quantile return prediction for 180-day horizon using Malta1 image model. |
| 50 | `img_malta1_r180_q3_quantile_label` | MATRIX | 0.572 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-3) for 180-day horizon using Malta1 image-based model. |
| 51 | `img_malta1_r180_q4_prob_class0` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 4-quantile return prediction for 180-day horizon using Malta1 image model. |
| 52 | `img_malta1_r180_q4_prob_class1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 4-quantile return prediction for 180-day horizon using Malta1 image model. |
| 53 | `img_malta1_r180_q4_prob_class2` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 2 in 4-quantile return prediction for 180-day horizon using Malta1 image model. |
| 54 | `img_malta1_r180_q4_prob_class3` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 3 in 4-quantile return prediction for 180-day horizon using Malta1 image model. |
| 55 | `img_malta1_r180_q4_quantile_label` | MATRIX | 0.572 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-4) for 180-day horizon using Malta1 image-based model. |
| 56 | `img_malta1_r180_q5_prob_class1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 5-quantile return prediction for 180-day horizon using Malta1 image model. |
| 57 | `img_malta1_r180_q5_prob_class2` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 2 in 5-quantile return prediction for 180-day horizon using Malta1 image model. |
| 58 | `img_malta1_r180_q5_prob_class3` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 3 in 5-quantile return prediction for 180-day horizon using Malta1 image model. |
| 59 | `img_malta1_r180_q5_prob_class4` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 4 in 5-quantile return prediction for 180-day horizon using Malta1 image model. |
| 60 | `img_malta1_r80_q2_prob_class1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 2-quantile return prediction for 80-day horizon using Malta1 image model. |
| 61 | `img_malta1_r80_q2_quantile_label` | MATRIX | 0.572 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-2) for 80-day horizon using Malta1 image-based model. |
| 62 | `img_malta1_r80_q3_prob_class0` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 3-quantile return prediction for 80-day horizon using Malta1 image model. |
| 63 | `img_malta1_r80_q4_prob_class1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 4-quantile return prediction for 80-day horizon using Malta1 image model. |
| 64 | `img_malta1_r80_q4_quantile_label` | MATRIX | 0.572 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-4) for 80-day horizon using Malta1 image-based model. |
| 65 | `img_malta1_r80_q5_prob_class1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 5-quantile return prediction for 80-day horizon using Malta1 image model. |
| 66 | `img_malta1_r80_q5_prob_class3` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 3 in 5-quantile return prediction for 80-day horizon using Malta1 image model. |
| 67 | `probability_rank0_180d_5bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 180-day return falls into the first of five ranked buckets, based on image-driven predictions |
| 68 | `probability_rank0_80d_2bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the first of two ranked buckets, based on image-driven predictions. |
| 69 | `probability_rank0_80d_4bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the first of four ranked buckets, based on image-driven predictions. |
| 70 | `probability_rank0_80d_5bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the first of five ranked buckets, based on image-driven predictions. |
| 71 | `probability_rank1_180d_2bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 180-day return falls into the second of two ranked buckets, based on image-driven predictions |
| 72 | `probability_rank1_180d_3bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 180-day return falls into the first of three ranked buckets, based on image-driven prediction |
| 73 | `probability_rank1_80d_3bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the second of three ranked buckets, based on image-driven prediction |
| 74 | `probability_rank2_180d_3bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 180-day return falls into the third of three ranked buckets, based on image-driven prediction |
| 75 | `probability_rank2_80d_3bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the third of three ranked buckets, based on image-driven predictions |
| 76 | `probability_rank2_80d_4bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the third of four ranked buckets, based on image-driven predictions. |
| 77 | `probability_rank2_80d_5bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the third of five ranked buckets, based on image-driven predictions. |
| 78 | `probability_rank3_80d_4bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the fourth of four ranked buckets, based on image-driven predictions |
| 79 | `probability_rank4_80d_5bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Model probability that the 80-day return falls into the fifth of five ranked buckets, based on image-driven predictions. |
| 80 | `quantile_rank_180d_5bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted quantile rank (0-4) for 180-day return among five buckets, using image-based model output. |
| 81 | `quantile_rank_80d_2bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted quantile rank (0-1) for 80-day return among two buckets, using image-based model output. |
| 82 | `quantile_rank_80d_3bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted quantile rank (0-2) for 80-day return among three buckets, using image-based model output. |
| 83 | `quantile_rank_80d_5bucket_img_malta1` | MATRIX | 0.572 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted quantile rank (0-4) for 80-day return among five buckets, using image-based model output. |
| 84 | `eur_img_feature3_malta1_d1` | MATRIX | 0.570 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Third extracted image-based feature for the EUR region, using the first Malta model, daily frequency. |
| 85 | `eur_img_feature2_malta2_d1` | MATRIX | 0.550 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Second extracted image-based feature for the EUR region, using the second Malta model, daily frequency. |
| 86 | `eur_img_feature3_malta2_d1` | MATRIX | 0.550 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Third extracted image-based feature for the EUR region, using the second Malta model, daily frequency. |
| 87 | `eur_img_feature1_malta2_d1` | MATRIX | 0.550 | 宏观与行业 | 0 | — | — | — | UNUSABLE | First extracted image-based feature for the EUR region, using the second Malta model, daily frequency. |
| 88 | `img_malta2_r50_q1_quantile_label` | MATRIX | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-quantile, i.e., all-in-one) for 50-day horizon using Malta2 image-based model. |
| 89 | `img_malta2_r50_q2_prob_class0` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 2-quantile return prediction for 50-day horizon using Malta2 image model. |
| 90 | `img_malta2_r50_q2_prob_class1` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 2-quantile return prediction for 50-day horizon using Malta2 image model. |
| 91 | `img_malta2_r50_q2_quantile_label` | MATRIX | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-2) for 50-day horizon using Malta2 image-based model. |
| 92 | `img_malta2_r50_q3_prob_class0` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 3-quantile return prediction for 50-day horizon using Malta2 image model. |
| 93 | `img_malta2_r50_q3_prob_class1` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 3-quantile return prediction for 50-day horizon using Malta2 image model. |
| 94 | `img_malta2_r50_q3_prob_class2` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 2 in 3-quantile return prediction for 50-day horizon using Malta2 image model. |
| 95 | `img_malta2_r50_q4_prob_class0` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 4-quantile return prediction for 50-day horizon using Malta2 image model. |
| 96 | `img_malta2_r50_q4_prob_class1` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 4-quantile return prediction for 50-day horizon using Malta2 image model. |
| 97 | `img_malta2_r50_q4_prob_class2` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 2 in 4-quantile return prediction for 50-day horizon using Malta2 image model. |
| 98 | `img_malta2_r50_q4_prob_class3` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 3 in 4-quantile return prediction for 50-day horizon using Malta2 image model. |
| 99 | `img_malta2_r50_q5_prob_class0` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| 100 | `img_malta2_r50_q5_prob_class1` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| 101 | `img_malta2_r50_q5_prob_class2` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 2 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| 102 | `img_malta2_r50_q5_prob_class3` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 3 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| 103 | `img_malta2_r50_q5_prob_class4` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 4 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| 104 | `img_malta2_r80_q1_quantile_label` | MATRIX | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-quantile, i.e., all-in-one) for 80-day horizon using Malta2 image-based model. |
| 105 | `img_malta2_r80_q2_prob_class0` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 2-quantile return prediction for 80-day horizon using Malta2 image model. |
| 106 | `img_malta2_r80_q2_prob_class1` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 2-quantile return prediction for 80-day horizon using Malta2 image model. |
| 107 | `img_malta2_r80_q2_quantile_label` | MATRIX | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-2) for 80-day horizon using Malta2 image-based model. |
| 108 | `img_malta2_r80_q3_prob_class0` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 3-quantile return prediction for 80-day horizon using Malta2 image model. |
| 109 | `img_malta2_r80_q3_prob_class1` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 3-quantile return prediction for 80-day horizon using Malta2 image model. |
| 110 | `img_malta2_r80_q3_prob_class2` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 2 in 3-quantile return prediction for 80-day horizon using Malta2 image model. |
| 111 | `img_malta2_r80_q3_quantile_label` | MATRIX | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-3) for 80-day horizon using Malta2 image-based model. |
| 112 | `img_malta2_r80_q4_prob_class0` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 4-quantile return prediction for 80-day horizon using Malta2 image model. |
| 113 | `img_malta2_r80_q4_prob_class1` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 4-quantile return prediction for 80-day horizon using Malta2 image model. |
| 114 | `img_malta2_r80_q4_prob_class2` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 2 in 4-quantile return prediction for 80-day horizon using Malta2 image model. |
| 115 | `img_malta2_r80_q4_prob_class3` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 3 in 4-quantile return prediction for 80-day horizon using Malta2 image model. |
| 116 | `img_malta2_r80_q4_quantile_label` | MATRIX | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-4) for 80-day horizon using Malta2 image-based model. |
| 117 | `img_malta2_r80_q5_prob_class0` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 0 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| 118 | `img_malta2_r80_q5_prob_class1` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 1 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| 119 | `img_malta2_r80_q5_prob_class2` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 2 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| 120 | `img_malta2_r80_q5_prob_class3` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 3 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| 121 | `img_malta2_r80_q5_prob_class4` | MATRIX | 0.541 | 价量与波动 | 0 | — | — | — | UNUSABLE | Predicted probability for class 4 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| 122 | `img_malta2_r80_q5_quantile_label` | MATRIX | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | Predicted quantile label (1-5) for 80-day horizon using Malta2 image-based model. |

## 六、本地回测证据

- 本地累计回测 **9** 条；其中 `ra_failed_checks` 为空的 **9** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `rK5vRkmE` | 1.36 | 0.49 | 0.70 | — | 0.16 | 0 | 116 | `rank(ts_decay_linear(eur_img_feature1_leapstar6_d1, 21))` |
| `P0ZdoeEp` | 1.26 | 0.27 | -0.41 | — | 0.43 | 0 | 116 | `rank(zscore(eur_img_feature1_leapstar6_d1))` |
| `YP5G1ZdM` | 1.06 | 0.60 | 1.59 | — | 0.03 | 0 | 116 | `rank(ts_mean(ts_backfill(img_malta2_r50_q3_quantile_label, 66), 66))` |
| `XgW5aVGx` | 0.89 | 0.48 | 1.63 | — | 0.03 | 0 | 116 | `rank(ts_mean(ts_backfill(img_malta2_r50_q4_quantile_label, 66), 66))` |
| `wpYMQ6V2` | 0.88 | 0.49 | 1.78 | — | 0.03 | 0 | 116 | `rank(ts_mean(ts_backfill(img_malta2_r50_q5_quantile_label, 66), 66))` |
| `E5vX63A1` | 0.46 | 0.06 | -0.63 | — | 0.44 | 0 | 116 | `ts_zscore(ts_delta(eur_img_feature1_leapstar6_d1, 21), 22)` |
| `e79o5AJz` | 0.42 | 0.11 | -0.75 | — | 0.14 | 0 | 116 | `ts_quantile(ts_mean(ts_backfill(img_malta2_r50_q5_quantile_label, 66), 66), 22, driver="ga` |
| `O0rEAevv` | -0.05 | 0.00 | 0.32 | — | 0.72 | 0 | 116 | `rank(multiply(ts_zscore(eur_img_feature1_leapstar6_d1, 66), ts_zscore(eur_img_feature2_lea` |
| `gJQEaX6Q` | -0.35 | -0.12 | -0.40 | — | 0.93 | 0 | 116 | `group_sum(ts_backfill(img_malta2_r50_q5_quantile_label, 66), subindustry)` |

## 七、判死记录（sealed dead_end）

- `EUR-chart_cnn_alpha-LEAPSTAR-WEAK`（2026-09-04）family=chart_cnn_alpha leapstar6/malta2 image features：{"best_2y": 1.59, "best_alpha": "rK5vRkmE", "best_fitness": 0.49, "best_sharpe": 1.36, "dataset": "chart_cnn_alpha", "evidence": "wave116 9 条：3 条近闸（rK5vRkmE S1.36/F0.49、P0ZdoeEp S1.26/F0.27、YP5G1ZdM S1.06/F0.60/2Y1.59）但 F<0.8 未达 Mode B 线；leapstar6 特征有效但强度不足；malta2 q3/q4 有效但 q5 弱；group_sum 契约算子全负", "id": "EUR-chart_cnn_alpha-LEAPSTAR-WEAK", "reason": "chart_cnn_alpha leapstar6/malta2 图像特征在 EUR TOP2
- `EUR-chart_cnn_alpha-MODEB-CEILING`（2026-09-04）family=chart_cnn_alpha malta2 q3 × leapstar6 Mode B ceiling：{"best_2y": 1.68, "best_alpha": "e79ovXnl", "best_fitness": 0.91, "best_sharpe": 1.44, "dataset": "chart_cnn_alpha", "evidence": "wave120 Mode B 优化 9 条近闸候选（S1.22-1.44/F0.71-0.91），F0.91 最接近 1.0 线但未达；malta2 q3 × leapstar6 组合在 EUR 的天花板 S1.44/F0.91 已是极限；所有近闸候选 S<1.58 且 F<1.0 无法通过提交硬闸", "id": "EUR-chart_cnn_alpha-MODEB-CEILING", "reason": "chart_cnn_alpha malta2 q3 × leapstar6 Mode B 优化在 EUR 已达天花板（S1.4

