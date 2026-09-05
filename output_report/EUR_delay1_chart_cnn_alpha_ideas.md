# chart_cnn_alpha Feature Engineering Analysis Report

**Dataset**: chart_cnn_alpha
**Region**: EUR
**Delay**: 1


- **Dataset**: `chart_cnn_alpha`
- **Category**: `model`
- **Region**: `EUR`
- **Delay**: `1`
- **Universe**: `TOP2500`
- **Fields Analyzed**: 122
- **Generated**: 2026-09-04T01:24:27.296802

---

## Executive Summary

本数据集提供 122 个字段（MATRIX 122 / VECTOR 0 / GROUP 0），覆盖 `model` 类信号。以下为自动生成的特征工程思路，供 S2 GEM 阶段绑定字段池。

## 字段画像（Field Inventory）

| Field ID | Type | Coverage | Description |
|---|---|---|---|
| `eur_img_feature1_leapstar6_d1` | MATRIX | 98% | First extracted image-based feature for the EUR region, using the Leap Star6 model, daily frequency. |
| `eur_img_feature1_malta1_d1` | MATRIX | 58% | First extracted image-based feature for the EUR region, using the first Malta model, daily frequency. |
| `eur_img_feature1_malta2_d1` | MATRIX | 55% | First extracted image-based feature for the EUR region, using the second Malta model, daily frequency. |
| `eur_img_feature2_leapstar6_d1` | MATRIX | 97% | Second extracted image-based feature for the EUR region, using the Leap Star6 model, daily frequency. |
| `eur_img_feature2_malta1_d1` | MATRIX | 58% | Second extracted image-based feature for the EUR region, using the first Malta model, daily frequency. |
| `eur_img_feature2_malta2_d1` | MATRIX | 55% | Second extracted image-based feature for the EUR region, using the second Malta model, daily frequency. |
| `eur_img_feature3_malta1_d1` | MATRIX | 57% | Third extracted image-based feature for the EUR region, using the first Malta model, daily frequency. |
| `eur_img_feature3_malta2_d1` | MATRIX | 55% | Third extracted image-based feature for the EUR region, using the second Malta model, daily frequency. |
| `img_leapstar6_r30_q1_quantile_label` | MATRIX | 97% | Predicted quantile label (1-quantile, i.e., all-in-one) for 30-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r30_q2_prob_class0` | MATRIX | 97% | Predicted probability for class 0 in 2-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q2_prob_class1` | MATRIX | 97% | Predicted probability for class 1 in 2-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q2_quantile_label` | MATRIX | 97% | Predicted quantile label (1-2) for 30-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r30_q3_prob_class0` | MATRIX | 97% | Predicted probability for class 0 in 3-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q3_prob_class1` | MATRIX | 97% | Predicted probability for class 1 in 3-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q3_prob_class2` | MATRIX | 97% | Predicted probability for class 2 in 3-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q3_quantile_label` | MATRIX | 97% | Predicted quantile label (1-3) for 30-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r30_q4_prob_class0` | MATRIX | 97% | Predicted probability for class 0 in 4-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q4_prob_class1` | MATRIX | 97% | Predicted probability for class 1 in 4-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q4_prob_class2` | MATRIX | 97% | Predicted probability for class 2 in 4-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q4_prob_class3` | MATRIX | 97% | Predicted probability for class 3 in 4-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q4_quantile_label` | MATRIX | 97% | Predicted quantile label (1-4) for 30-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r30_q5_prob_class0` | MATRIX | 97% | Predicted probability for class 0 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q5_prob_class1` | MATRIX | 97% | Predicted probability for class 1 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q5_prob_class2` | MATRIX | 97% | Predicted probability for class 2 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q5_prob_class3` | MATRIX | 97% | Predicted probability for class 3 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q5_prob_class4` | MATRIX | 97% | Predicted probability for class 4 in 5-quantile return prediction for 30-day horizon using LeapStar6 image model. |
| `img_leapstar6_r30_q5_quantile_label` | MATRIX | 97% | Predicted quantile label (1-5) for 30-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r5_q1_quantile_label` | MATRIX | 97% | Predicted quantile label (1-quantile, i.e., all-in-one) for 5-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r5_q2_prob_class0` | MATRIX | 97% | Predicted probability for class 0 in 2-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q2_prob_class1` | MATRIX | 97% | Predicted probability for class 1 in 2-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q2_quantile_label` | MATRIX | 97% | Predicted quantile label (1-2) for 5-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r5_q3_prob_class0` | MATRIX | 97% | Predicted probability for class 0 in 3-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q3_prob_class1` | MATRIX | 97% | Predicted probability for class 1 in 3-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q3_prob_class2` | MATRIX | 97% | Predicted probability for class 2 in 3-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q3_quantile_label` | MATRIX | 97% | Predicted quantile label (1-3) for 5-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r5_q4_prob_class0` | MATRIX | 97% | Predicted probability for class 0 in 4-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q4_prob_class1` | MATRIX | 97% | Predicted probability for class 1 in 4-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q4_prob_class2` | MATRIX | 97% | Predicted probability for class 2 in 4-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q4_prob_class3` | MATRIX | 97% | Predicted probability for class 3 in 4-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q4_quantile_label` | MATRIX | 97% | Predicted quantile label (1-4) for 5-day horizon using LeapStar6 image-based model. |
| `img_leapstar6_r5_q5_prob_class0` | MATRIX | 97% | Predicted probability for class 0 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q5_prob_class1` | MATRIX | 97% | Predicted probability for class 1 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q5_prob_class2` | MATRIX | 97% | Predicted probability for class 2 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q5_prob_class3` | MATRIX | 97% | Predicted probability for class 3 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q5_prob_class4` | MATRIX | 97% | Predicted probability for class 4 in 5-quantile return prediction for 5-day horizon using LeapStar6 image model. |
| `img_leapstar6_r5_q5_quantile_label` | MATRIX | 97% | Predicted quantile label (1-5) for 5-day horizon using LeapStar6 image-based model. |
| `img_malta1_r180_q1_quantile_label` | MATRIX | 57% | Predicted quantile label (1-quantile, i.e., all-in-one) for 180-day horizon using Malta1 image-based model. |
| `img_malta1_r180_q2_prob_class0` | MATRIX | 57% | Predicted probability for class 0 in 2-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q2_quantile_label` | MATRIX | 57% | Predicted quantile label (1-2) for 180-day horizon using Malta1 image-based model. |
| `img_malta1_r180_q3_prob_class0` | MATRIX | 57% | Predicted probability for class 0 in 3-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q3_quantile_label` | MATRIX | 57% | Predicted quantile label (1-3) for 180-day horizon using Malta1 image-based model. |
| `img_malta1_r180_q4_prob_class0` | MATRIX | 57% | Predicted probability for class 0 in 4-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q4_prob_class1` | MATRIX | 57% | Predicted probability for class 1 in 4-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q4_prob_class2` | MATRIX | 57% | Predicted probability for class 2 in 4-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q4_prob_class3` | MATRIX | 57% | Predicted probability for class 3 in 4-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q4_quantile_label` | MATRIX | 57% | Predicted quantile label (1-4) for 180-day horizon using Malta1 image-based model. |
| `img_malta1_r180_q5_prob_class1` | MATRIX | 57% | Predicted probability for class 1 in 5-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q5_prob_class2` | MATRIX | 57% | Predicted probability for class 2 in 5-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q5_prob_class3` | MATRIX | 57% | Predicted probability for class 3 in 5-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r180_q5_prob_class4` | MATRIX | 57% | Predicted probability for class 4 in 5-quantile return prediction for 180-day horizon using Malta1 image model. |
| `img_malta1_r80_q2_prob_class1` | MATRIX | 57% | Predicted probability for class 1 in 2-quantile return prediction for 80-day horizon using Malta1 image model. |
| `img_malta1_r80_q2_quantile_label` | MATRIX | 57% | Predicted quantile label (1-2) for 80-day horizon using Malta1 image-based model. |
| `img_malta1_r80_q3_prob_class0` | MATRIX | 57% | Predicted probability for class 0 in 3-quantile return prediction for 80-day horizon using Malta1 image model. |
| `img_malta1_r80_q4_prob_class1` | MATRIX | 57% | Predicted probability for class 1 in 4-quantile return prediction for 80-day horizon using Malta1 image model. |
| `img_malta1_r80_q4_quantile_label` | MATRIX | 57% | Predicted quantile label (1-4) for 80-day horizon using Malta1 image-based model. |
| `img_malta1_r80_q5_prob_class1` | MATRIX | 57% | Predicted probability for class 1 in 5-quantile return prediction for 80-day horizon using Malta1 image model. |
| `img_malta1_r80_q5_prob_class3` | MATRIX | 57% | Predicted probability for class 3 in 5-quantile return prediction for 80-day horizon using Malta1 image model. |
| `img_malta2_r50_q1_quantile_label` | MATRIX | 54% | Predicted quantile label (1-quantile, i.e., all-in-one) for 50-day horizon using Malta2 image-based model. |
| `img_malta2_r50_q2_prob_class0` | MATRIX | 54% | Predicted probability for class 0 in 2-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q2_prob_class1` | MATRIX | 54% | Predicted probability for class 1 in 2-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q2_quantile_label` | MATRIX | 54% | Predicted quantile label (1-2) for 50-day horizon using Malta2 image-based model. |
| `img_malta2_r50_q3_prob_class0` | MATRIX | 54% | Predicted probability for class 0 in 3-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q3_prob_class1` | MATRIX | 54% | Predicted probability for class 1 in 3-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q3_prob_class2` | MATRIX | 54% | Predicted probability for class 2 in 3-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q3_quantile_label` | MATRIX | 54% | Predicted quantile label (1-3) for 50-day horizon using Malta2 image-based model. |
| `img_malta2_r50_q4_prob_class0` | MATRIX | 54% | Predicted probability for class 0 in 4-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q4_prob_class1` | MATRIX | 54% | Predicted probability for class 1 in 4-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q4_prob_class2` | MATRIX | 54% | Predicted probability for class 2 in 4-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q4_prob_class3` | MATRIX | 54% | Predicted probability for class 3 in 4-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q4_quantile_label` | MATRIX | 54% | Predicted quantile label (1-4) for 50-day horizon using Malta2 image-based model. |
| `img_malta2_r50_q5_prob_class0` | MATRIX | 54% | Predicted probability for class 0 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q5_prob_class1` | MATRIX | 54% | Predicted probability for class 1 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q5_prob_class2` | MATRIX | 54% | Predicted probability for class 2 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q5_prob_class3` | MATRIX | 54% | Predicted probability for class 3 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q5_prob_class4` | MATRIX | 54% | Predicted probability for class 4 in 5-quantile return prediction for 50-day horizon using Malta2 image model. |
| `img_malta2_r50_q5_quantile_label` | MATRIX | 54% | Predicted quantile label (1-5) for 50-day horizon using Malta2 image-based model. |
| `img_malta2_r80_q1_quantile_label` | MATRIX | 54% | Predicted quantile label (1-quantile, i.e., all-in-one) for 80-day horizon using Malta2 image-based model. |
| `img_malta2_r80_q2_prob_class0` | MATRIX | 54% | Predicted probability for class 0 in 2-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q2_prob_class1` | MATRIX | 54% | Predicted probability for class 1 in 2-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q2_quantile_label` | MATRIX | 54% | Predicted quantile label (1-2) for 80-day horizon using Malta2 image-based model. |
| `img_malta2_r80_q3_prob_class0` | MATRIX | 54% | Predicted probability for class 0 in 3-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q3_prob_class1` | MATRIX | 54% | Predicted probability for class 1 in 3-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q3_prob_class2` | MATRIX | 54% | Predicted probability for class 2 in 3-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q3_quantile_label` | MATRIX | 54% | Predicted quantile label (1-3) for 80-day horizon using Malta2 image-based model. |
| `img_malta2_r80_q4_prob_class0` | MATRIX | 54% | Predicted probability for class 0 in 4-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q4_prob_class1` | MATRIX | 54% | Predicted probability for class 1 in 4-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q4_prob_class2` | MATRIX | 54% | Predicted probability for class 2 in 4-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q4_prob_class3` | MATRIX | 54% | Predicted probability for class 3 in 4-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q4_quantile_label` | MATRIX | 54% | Predicted quantile label (1-4) for 80-day horizon using Malta2 image-based model. |
| `img_malta2_r80_q5_prob_class0` | MATRIX | 54% | Predicted probability for class 0 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q5_prob_class1` | MATRIX | 54% | Predicted probability for class 1 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q5_prob_class2` | MATRIX | 54% | Predicted probability for class 2 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q5_prob_class3` | MATRIX | 54% | Predicted probability for class 3 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q5_prob_class4` | MATRIX | 54% | Predicted probability for class 4 in 5-quantile return prediction for 80-day horizon using Malta2 image model. |
| `img_malta2_r80_q5_quantile_label` | MATRIX | 54% | Predicted quantile label (1-5) for 80-day horizon using Malta2 image-based model. |
| `probability_rank0_180d_5bucket_img_malta1` | MATRIX | 57% | Model probability that the 180-day return falls into the first of five ranked buckets, based on image-driven predictions |
| `probability_rank0_80d_2bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the first of two ranked buckets, based on image-driven predictions. |
| `probability_rank0_80d_4bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the first of four ranked buckets, based on image-driven predictions. |
| `probability_rank0_80d_5bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the first of five ranked buckets, based on image-driven predictions. |
| `probability_rank1_180d_2bucket_img_malta1` | MATRIX | 57% | Model probability that the 180-day return falls into the second of two ranked buckets, based on image-driven predictions |
| `probability_rank1_180d_3bucket_img_malta1` | MATRIX | 57% | Model probability that the 180-day return falls into the first of three ranked buckets, based on image-driven prediction |
| `probability_rank1_80d_3bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the second of three ranked buckets, based on image-driven prediction |
| `probability_rank2_180d_3bucket_img_malta1` | MATRIX | 57% | Model probability that the 180-day return falls into the third of three ranked buckets, based on image-driven prediction |
| `probability_rank2_80d_3bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the third of three ranked buckets, based on image-driven predictions |
| `probability_rank2_80d_4bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the third of four ranked buckets, based on image-driven predictions. |
| `probability_rank2_80d_5bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the third of five ranked buckets, based on image-driven predictions. |
| `probability_rank3_80d_4bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the fourth of four ranked buckets, based on image-driven predictions |
| `probability_rank4_80d_5bucket_img_malta1` | MATRIX | 57% | Model probability that the 80-day return falls into the fifth of five ranked buckets, based on image-driven predictions. |
| `quantile_rank_180d_5bucket_img_malta1` | MATRIX | 57% | Predicted quantile rank (0-4) for 180-day return among five buckets, using image-based model output. |
| `quantile_rank_80d_2bucket_img_malta1` | MATRIX | 57% | Predicted quantile rank (0-1) for 80-day return among two buckets, using image-based model output. |
| `quantile_rank_80d_3bucket_img_malta1` | MATRIX | 57% | Predicted quantile rank (0-2) for 80-day return among three buckets, using image-based model output. |
| `quantile_rank_80d_5bucket_img_malta1` | MATRIX | 57% | Predicted quantile rank (0-4) for 80-day return among five buckets, using image-based model output. |

## 字段解构（Field Deconstruction）

### `eur_img_feature1_leapstar6_d1`（MATRIX）
- **测什么**：First extracted image-based feature for the EUR region, using the Leap Star6 model, daily frequency.
- **覆盖率**：0.9809
- **字段名语义**：`eur_img_feature1_leapstar6_d1` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `eur_img_feature2_leapstar6_d1`（MATRIX）
- **测什么**：Second extracted image-based feature for the EUR region, using the Leap Star6 model, daily frequency.
- **覆盖率**：0.9683
- **字段名语义**：`eur_img_feature2_leapstar6_d1` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `img_leapstar6_r30_q1_quantile_label`（MATRIX）
- **测什么**：Predicted quantile label (1-quantile, i.e., all-in-one) for 30-day horizon using LeapStar6 image-based model.
- **覆盖率**：0.9675
- **字段名语义**：`img_leapstar6_r30_q1_quantile_label` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `img_leapstar6_r30_q2_prob_class0`（MATRIX）
- **测什么**：Predicted probability for class 0 in 2-quantile return prediction for 30-day horizon using LeapStar6 image model.
- **覆盖率**：0.9675
- **字段名语义**：`img_leapstar6_r30_q2_prob_class0` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `img_leapstar6_r30_q2_prob_class1`（MATRIX）
- **测什么**：Predicted probability for class 1 in 2-quantile return prediction for 30-day horizon using LeapStar6 image model.
- **覆盖率**：0.9675
- **字段名语义**：`img_leapstar6_r30_q2_prob_class1` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `img_leapstar6_r30_q2_quantile_label`（MATRIX）
- **测什么**：Predicted quantile label (1-2) for 30-day horizon using LeapStar6 image-based model.
- **覆盖率**：0.9675
- **字段名语义**：`img_leapstar6_r30_q2_quantile_label` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `img_leapstar6_r30_q3_prob_class0`（MATRIX）
- **测什么**：Predicted probability for class 0 in 3-quantile return prediction for 30-day horizon using LeapStar6 image model.
- **覆盖率**：0.9675
- **字段名语义**：`img_leapstar6_r30_q3_prob_class0` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `img_leapstar6_r30_q3_prob_class1`（MATRIX）
- **测什么**：Predicted probability for class 1 in 3-quantile return prediction for 30-day horizon using LeapStar6 image model.
- **覆盖率**：0.9675
- **字段名语义**：`img_leapstar6_r30_q3_prob_class1` 的命名前缀用于字段族聚类（S1 前缀扫描）

## 预处理决策（Preprocessing）

- group_zscore / group_rank：MATRIX 字段截面中性化（cross-sectional）

## 特征概念（8 问框架，模板化）

### Q1 稳定性/不变量
- **使用字段**：`eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **建议**：ts_mean / ts_std_dev 度量字段的长期水平与稳定性

### Q2 变化
- **使用字段**：`eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **建议**：ts_delta / ts_scale 捕捉变化率与动量

### Q3 异常
- **使用字段**：`eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **建议**：zscore / ts_rank 识别截面与时间序列上的离群

### Q4 交互
- **使用字段**：`eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **建议**：两字段 add/multiply 合成新含义，注意先各自中性化

### Q5 结构
- **使用字段**：`eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **建议**：字段占比 / 比例关系（如 components 型字段）

### Q6 累积
- **使用字段**：`eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **建议**：ts_sum / ts_decay_linear 累积与衰减记忆

### Q7 相对
- **使用字段**：`eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **建议**：rank / group_rank 相对定位与归一化

### Q8 本质
- **使用字段**：`eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **建议**：第一性原理直取原始字段，剥离过拟合包装

## GEM 兼容模板（Concept Blocks）

> 以下 Concept 块供 S2 `brain-makeSomeGem` 直接消费（`--ideas-file` 注入）。
> 占位符 `{field_id}` 为字段白名单中的真实字段 id，run_pipeline 可解析绑定。

**Concept**: eur_img_feature1_leapstar6_d1 长期水平稳定（Q1）
- **Mechanism**: ts_mean 度量字段长期水平，rank 截面归一化
- **Fields Used**: `eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **Implementation Example**: `rank(ts_mean({eur_img_feature1_leapstar6_d1}, 66))`
- **Direction**: High → long

**Concept**: eur_img_feature1_leapstar6_d1 变化动量（Q2）
- **Mechanism**: ts_delta 捕捉 21 日变化率，rank 截面归一化
- **Fields Used**: `eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **Implementation Example**: `rank(ts_delta({eur_img_feature1_leapstar6_d1}, 21))`
- **Direction**: High → long

**Concept**: eur_img_feature1_leapstar6_d1 截面离群（Q3）
- **Mechanism**: zscore 识别截面离群，rank 归一化
- **Fields Used**: `eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **Implementation Example**: `rank(zscore({eur_img_feature1_leapstar6_d1}))`
- **Direction**: High → long

**Concept**: eur_img_feature1_leapstar6_d1 × eur_img_feature2_leapstar6_d1 交互（Q4）
- **Mechanism**: 两字段各自 ts_zscore 中性化后 multiply 合成
- **Fields Used**: `eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **Implementation Example**: `rank(multiply(ts_zscore({eur_img_feature1_leapstar6_d1}, 66), ts_zscore({eur_img_feature2_leapstar6_d1}, 66)))`
- **Direction**: High → long

**Concept**: eur_img_feature1_leapstar6_d1 结构占比（Q5）
- **Mechanism**: divide 构造比例关系，rank 截面归一化
- **Fields Used**: `eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **Implementation Example**: `rank(divide({eur_img_feature1_leapstar6_d1}, {eur_img_feature2_leapstar6_d1}))`
- **Direction**: High → long

**Concept**: eur_img_feature1_leapstar6_d1 累积衰减（Q6）
- **Mechanism**: ts_decay_linear 累积记忆衰减，rank 归一化
- **Fields Used**: `eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **Implementation Example**: `rank(ts_decay_linear({eur_img_feature1_leapstar6_d1}, 21))`
- **Direction**: High → long

**Concept**: eur_img_feature1_leapstar6_d1 截面相对定位（Q7）
- **Mechanism**: ts_backfill 稀疏回填 + group_rank 行业内相对定位
- **Fields Used**: `eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **Implementation Example**: `group_rank(ts_backfill({eur_img_feature1_leapstar6_d1}, 66), industry)`
- **Direction**: High → long

**Concept**: eur_img_feature1_leapstar6_d1 本质直取（Q8）
- **Mechanism**: 第一性原理直取原始字段，rank 截面归一化
- **Fields Used**: `eur_img_feature1_leapstar6_d1`, `eur_img_feature2_leapstar6_d1`
- **Implementation Example**: `rank({eur_img_feature1_leapstar6_d1})`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
eur_img_feature1_leapstar6_d1
eur_img_feature1_malta1_d1
eur_img_feature1_malta2_d1
eur_img_feature2_leapstar6_d1
eur_img_feature2_malta1_d1
eur_img_feature2_malta2_d1
eur_img_feature3_malta1_d1
eur_img_feature3_malta2_d1
img_leapstar6_r30_q1_quantile_label
img_leapstar6_r30_q2_prob_class0
img_leapstar6_r30_q2_prob_class1
img_leapstar6_r30_q2_quantile_label
img_leapstar6_r30_q3_prob_class0
img_leapstar6_r30_q3_prob_class1
img_leapstar6_r30_q3_prob_class2
img_leapstar6_r30_q3_quantile_label
img_leapstar6_r30_q4_prob_class0
img_leapstar6_r30_q4_prob_class1
img_leapstar6_r30_q4_prob_class2
img_leapstar6_r30_q4_prob_class3
img_leapstar6_r30_q4_quantile_label
img_leapstar6_r30_q5_prob_class0
img_leapstar6_r30_q5_prob_class1
img_leapstar6_r30_q5_prob_class2
img_leapstar6_r30_q5_prob_class3
img_leapstar6_r30_q5_prob_class4
img_leapstar6_r30_q5_quantile_label
img_leapstar6_r5_q1_quantile_label
img_leapstar6_r5_q2_prob_class0
img_leapstar6_r5_q2_prob_class1
img_leapstar6_r5_q2_quantile_label
img_leapstar6_r5_q3_prob_class0
img_leapstar6_r5_q3_prob_class1
img_leapstar6_r5_q3_prob_class2
img_leapstar6_r5_q3_quantile_label
img_leapstar6_r5_q4_prob_class0
img_leapstar6_r5_q4_prob_class1
img_leapstar6_r5_q4_prob_class2
img_leapstar6_r5_q4_prob_class3
img_leapstar6_r5_q4_quantile_label
img_leapstar6_r5_q5_prob_class0
img_leapstar6_r5_q5_prob_class1
img_leapstar6_r5_q5_prob_class2
img_leapstar6_r5_q5_prob_class3
img_leapstar6_r5_q5_prob_class4
img_leapstar6_r5_q5_quantile_label
img_malta1_r180_q1_quantile_label
img_malta1_r180_q2_prob_class0
img_malta1_r180_q2_quantile_label
img_malta1_r180_q3_prob_class0
img_malta1_r180_q3_quantile_label
img_malta1_r180_q4_prob_class0
img_malta1_r180_q4_prob_class1
img_malta1_r180_q4_prob_class2
img_malta1_r180_q4_prob_class3
img_malta1_r180_q4_quantile_label
img_malta1_r180_q5_prob_class1
img_malta1_r180_q5_prob_class2
img_malta1_r180_q5_prob_class3
img_malta1_r180_q5_prob_class4
img_malta1_r80_q2_prob_class1
img_malta1_r80_q2_quantile_label
img_malta1_r80_q3_prob_class0
img_malta1_r80_q4_prob_class1
img_malta1_r80_q4_quantile_label
img_malta1_r80_q5_prob_class1
img_malta1_r80_q5_prob_class3
img_malta2_r50_q1_quantile_label
img_malta2_r50_q2_prob_class0
img_malta2_r50_q2_prob_class1
img_malta2_r50_q2_quantile_label
img_malta2_r50_q3_prob_class0
img_malta2_r50_q3_prob_class1
img_malta2_r50_q3_prob_class2
img_malta2_r50_q3_quantile_label
img_malta2_r50_q4_prob_class0
img_malta2_r50_q4_prob_class1
img_malta2_r50_q4_prob_class2
img_malta2_r50_q4_prob_class3
img_malta2_r50_q4_quantile_label
img_malta2_r50_q5_prob_class0
img_malta2_r50_q5_prob_class1
img_malta2_r50_q5_prob_class2
img_malta2_r50_q5_prob_class3
img_malta2_r50_q5_prob_class4
img_malta2_r50_q5_quantile_label
img_malta2_r80_q1_quantile_label
img_malta2_r80_q2_prob_class0
img_malta2_r80_q2_prob_class1
img_malta2_r80_q2_quantile_label
img_malta2_r80_q3_prob_class0
img_malta2_r80_q3_prob_class1
img_malta2_r80_q3_prob_class2
img_malta2_r80_q3_quantile_label
img_malta2_r80_q4_prob_class0
img_malta2_r80_q4_prob_class1
img_malta2_r80_q4_prob_class2
img_malta2_r80_q4_prob_class3
img_malta2_r80_q4_quantile_label
img_malta2_r80_q5_prob_class0
img_malta2_r80_q5_prob_class1
img_malta2_r80_q5_prob_class2
img_malta2_r80_q5_prob_class3
img_malta2_r80_q5_prob_class4
img_malta2_r80_q5_quantile_label
probability_rank0_180d_5bucket_img_malta1
probability_rank0_80d_2bucket_img_malta1
probability_rank0_80d_4bucket_img_malta1
probability_rank0_80d_5bucket_img_malta1
probability_rank1_180d_2bucket_img_malta1
probability_rank1_180d_3bucket_img_malta1
probability_rank1_80d_3bucket_img_malta1
probability_rank2_180d_3bucket_img_malta1
probability_rank2_80d_3bucket_img_malta1
probability_rank2_80d_4bucket_img_malta1
probability_rank2_80d_5bucket_img_malta1
probability_rank3_80d_4bucket_img_malta1
probability_rank4_80d_5bucket_img_malta1
quantile_rank_180d_5bucket_img_malta1
quantile_rank_80d_2bucket_img_malta1
quantile_rank_80d_3bucket_img_malta1
quantile_rank_80d_5bucket_img_malta1
```

*Report generated: 2026-09-04T01:24:27.296802*