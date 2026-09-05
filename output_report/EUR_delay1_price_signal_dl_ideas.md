# price_signal_dl Feature Engineering Analysis Report

**Dataset**: price_signal_dl
**Region**: EUR
**Delay**: 1


- **Dataset**: `price_signal_dl`
- **Category**: `model`
- **Region**: `EUR`
- **Delay**: `1`
- **Universe**: `TOP2500`
- **Fields Analyzed**: 28
- **Generated**: 2026-09-04T01:06:46.843807

---

## Executive Summary

本数据集提供 28 个字段（MATRIX 28 / VECTOR 0 / GROUP 0），覆盖 `model` 类信号。以下为自动生成的特征工程思路，供 S2 GEM 阶段绑定字段池。

## 字段画像（Field Inventory）

| Field ID | Type | Coverage | Description |
|---|---|---|---|
| `normalized_trend_indicator_0` | MATRIX | 100% | Rescaled value of the first trend-based indicator for comparability. |
| `normalized_trend_indicator_1` | MATRIX | 100% | Rescaled value of the second trend-based indicator for comparability. |
| `normalized_trend_indicator_2` | MATRIX | 100% | Rescaled value of the third trend-based indicator for comparability. |
| `normalized_trend_indicator_3` | MATRIX | 100% | Rescaled value of the third trend-based indicator for comparability. |
| `normalized_trend_indicator_4` | MATRIX | 100% | Rescaled value of the fifth trend-based indicator for comparability. |
| `normalized_trend_indicator_5` | MATRIX | 100% | Rescaled value of the sixth trend-based indicator for comparability. |
| `normalized_trend_indicator_6` | MATRIX | 100% | Rescaled value of the seventh trend-based indicator for comparability. |
| `normalized_volume_indicator_0` | MATRIX | 90% | Rescaled value of the first volume-based indicator for comparability. |
| `normalized_volume_indicator_1` | MATRIX | 89% | Rescaled value of the second volume-based indicator for comparability. |
| `normalized_volume_indicator_2` | MATRIX | 89% | Rescaled value of the third volume-based indicator for comparability. |
| `normalized_volume_indicator_3` | MATRIX | 90% | Rescaled value of the fourth volume-based indicator for comparability. |
| `normalized_volume_indicator_4` | MATRIX | 90% | Rescaled value of the fifth volume-based indicator for comparability. |
| `normalized_volume_indicator_5` | MATRIX | 90% | Rescaled value of the sixth volume-based indicator for comparability. |
| `normalized_volume_indicator_6` | MATRIX | 87% | Rescaled value of the seventh volume-based indicator for comparability. |
| `raw_trend_indicator_0` | MATRIX | 100% | Unadjusted value of the first trend-based indicator. |
| `raw_trend_indicator_1` | MATRIX | 100% | Unadjusted value of the second trend-based indicator. |
| `raw_trend_indicator_2` | MATRIX | 100% | Unadjusted value of the second trend-based indicator. |
| `raw_trend_indicator_3` | MATRIX | 100% | Unadjusted value of the fourth trend-based indicator. |
| `raw_trend_indicator_4` | MATRIX | 100% | Unadjusted value of the fourth trend-based indicator. |
| `raw_trend_indicator_5` | MATRIX | 100% | Unadjusted value of the sixth trend-based indicator. |
| `raw_trend_indicator_6` | MATRIX | 100% | Unadjusted value of the seventh trend-based indicator. |
| `raw_volume_indicator_0` | MATRIX | 100% | Unadjusted value of the first volume-based indicator. |
| `raw_volume_indicator_1` | MATRIX | 100% | Unadjusted value of the second volume-based indicator. |
| `raw_volume_indicator_2` | MATRIX | 100% | Unadjusted value of the third volume-based indicator. |
| `raw_volume_indicator_3` | MATRIX | 100% | Unadjusted value of the fourth volume-based indicator. |
| `raw_volume_indicator_4` | MATRIX | 100% | Unadjusted value of the fifth volume-based indicator. |
| `raw_volume_indicator_5` | MATRIX | 100% | Unadjusted value of the sixth volume-based indicator. |
| `raw_volume_indicator_6` | MATRIX | 100% | Unadjusted value of the seventh volume-based indicator. |

## 字段解构（Field Deconstruction）

### `normalized_trend_indicator_0`（MATRIX）
- **测什么**：Rescaled value of the first trend-based indicator for comparability.
- **覆盖率**：1.0
- **字段名语义**：`normalized_trend_indicator_0` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `normalized_trend_indicator_1`（MATRIX）
- **测什么**：Rescaled value of the second trend-based indicator for comparability.
- **覆盖率**：1.0
- **字段名语义**：`normalized_trend_indicator_1` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `normalized_trend_indicator_2`（MATRIX）
- **测什么**：Rescaled value of the third trend-based indicator for comparability.
- **覆盖率**：1.0
- **字段名语义**：`normalized_trend_indicator_2` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `normalized_trend_indicator_3`（MATRIX）
- **测什么**：Rescaled value of the third trend-based indicator for comparability.
- **覆盖率**：1.0
- **字段名语义**：`normalized_trend_indicator_3` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `normalized_trend_indicator_4`（MATRIX）
- **测什么**：Rescaled value of the fifth trend-based indicator for comparability.
- **覆盖率**：1.0
- **字段名语义**：`normalized_trend_indicator_4` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `normalized_trend_indicator_5`（MATRIX）
- **测什么**：Rescaled value of the sixth trend-based indicator for comparability.
- **覆盖率**：1.0
- **字段名语义**：`normalized_trend_indicator_5` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `normalized_trend_indicator_6`（MATRIX）
- **测什么**：Rescaled value of the seventh trend-based indicator for comparability.
- **覆盖率**：1.0
- **字段名语义**：`normalized_trend_indicator_6` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `raw_trend_indicator_0`（MATRIX）
- **测什么**：Unadjusted value of the first trend-based indicator.
- **覆盖率**：1.0
- **字段名语义**：`raw_trend_indicator_0` 的命名前缀用于字段族聚类（S1 前缀扫描）

## 预处理决策（Preprocessing）

- group_zscore / group_rank：MATRIX 字段截面中性化（cross-sectional）

## 特征概念（8 问框架，模板化）

### Q1 稳定性/不变量
- **使用字段**：`normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **建议**：ts_mean / ts_std_dev 度量字段的长期水平与稳定性

### Q2 变化
- **使用字段**：`normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **建议**：ts_delta / ts_scale 捕捉变化率与动量

### Q3 异常
- **使用字段**：`normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **建议**：zscore / ts_rank 识别截面与时间序列上的离群

### Q4 交互
- **使用字段**：`normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **建议**：两字段 add/multiply 合成新含义，注意先各自中性化

### Q5 结构
- **使用字段**：`normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **建议**：字段占比 / 比例关系（如 components 型字段）

### Q6 累积
- **使用字段**：`normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **建议**：ts_sum / ts_decay_linear 累积与衰减记忆

### Q7 相对
- **使用字段**：`normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **建议**：rank / group_rank 相对定位与归一化

### Q8 本质
- **使用字段**：`normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **建议**：第一性原理直取原始字段，剥离过拟合包装

## GEM 兼容模板（Concept Blocks）

> 以下 Concept 块供 S2 `brain-makeSomeGem` 直接消费（`--ideas-file` 注入）。
> 占位符 `{field_id}` 为字段白名单中的真实字段 id，run_pipeline 可解析绑定。

**Concept**: normalized_trend_indicator_0 长期水平稳定（Q1）
- **Mechanism**: ts_mean 度量字段长期水平，rank 截面归一化
- **Fields Used**: `normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **Implementation Example**: `rank(ts_mean({normalized_trend_indicator_0}, 66))`
- **Direction**: High → long

**Concept**: normalized_trend_indicator_0 变化动量（Q2）
- **Mechanism**: ts_delta 捕捉 21 日变化率，rank 截面归一化
- **Fields Used**: `normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **Implementation Example**: `rank(ts_delta({normalized_trend_indicator_0}, 21))`
- **Direction**: High → long

**Concept**: normalized_trend_indicator_0 截面离群（Q3）
- **Mechanism**: zscore 识别截面离群，rank 归一化
- **Fields Used**: `normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **Implementation Example**: `rank(zscore({normalized_trend_indicator_0}))`
- **Direction**: High → long

**Concept**: normalized_trend_indicator_0 × normalized_trend_indicator_1 交互（Q4）
- **Mechanism**: 两字段各自 ts_zscore 中性化后 multiply 合成
- **Fields Used**: `normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **Implementation Example**: `rank(multiply(ts_zscore({normalized_trend_indicator_0}, 66), ts_zscore({normalized_trend_indicator_1}, 66)))`
- **Direction**: High → long

**Concept**: normalized_trend_indicator_0 结构占比（Q5）
- **Mechanism**: divide 构造比例关系，rank 截面归一化
- **Fields Used**: `normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **Implementation Example**: `rank(divide({normalized_trend_indicator_0}, {normalized_trend_indicator_1}))`
- **Direction**: High → long

**Concept**: normalized_trend_indicator_0 累积衰减（Q6）
- **Mechanism**: ts_decay_linear 累积记忆衰减，rank 归一化
- **Fields Used**: `normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **Implementation Example**: `rank(ts_decay_linear({normalized_trend_indicator_0}, 21))`
- **Direction**: High → long

**Concept**: normalized_trend_indicator_0 截面相对定位（Q7）
- **Mechanism**: ts_backfill 稀疏回填 + group_rank 行业内相对定位
- **Fields Used**: `normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **Implementation Example**: `group_rank(ts_backfill({normalized_trend_indicator_0}, 66), industry)`
- **Direction**: High → long

**Concept**: normalized_trend_indicator_0 本质直取（Q8）
- **Mechanism**: 第一性原理直取原始字段，rank 截面归一化
- **Fields Used**: `normalized_trend_indicator_0`, `normalized_trend_indicator_1`
- **Implementation Example**: `rank({normalized_trend_indicator_0})`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
normalized_trend_indicator_0
normalized_trend_indicator_1
normalized_trend_indicator_2
normalized_trend_indicator_3
normalized_trend_indicator_4
normalized_trend_indicator_5
normalized_trend_indicator_6
normalized_volume_indicator_0
normalized_volume_indicator_1
normalized_volume_indicator_2
normalized_volume_indicator_3
normalized_volume_indicator_4
normalized_volume_indicator_5
normalized_volume_indicator_6
raw_trend_indicator_0
raw_trend_indicator_1
raw_trend_indicator_2
raw_trend_indicator_3
raw_trend_indicator_4
raw_trend_indicator_5
raw_trend_indicator_6
raw_volume_indicator_0
raw_volume_indicator_1
raw_volume_indicator_2
raw_volume_indicator_3
raw_volume_indicator_4
raw_volume_indicator_5
raw_volume_indicator_6
```

*Report generated: 2026-09-04T01:06:46.843807*