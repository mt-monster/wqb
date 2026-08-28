# Wave 21 特征工程文档 - 使用 2腿组合 + 简单预处理方法（multifactor_return_pred）

## 基础信息
- **Wave**: 21
- **Region**: USA
- **Dataset**: multifactor_return_pred
- **基础配方**: Wave 17 成功配方（1Ywx8ZpR）+ Wave 20 失败教训
- **优化目标**: 使用 2腿组合 + 简单预处理方法

## Wave 20 失败教训分析

### 失败原因
- **问题**: LOW_SHARPE（1.41 < 1.58）, LOW_FITNESS（0.51 < 1.0）, LOW_2Y_SHARPE（1.15-1.22 < 1.58）
- **原因**: 
  1. 添加额外的预处理方法和算子（ts_zscore, ts_rank 等）反而降低了信号质量
  2. 这些预处理方法和算子改变了信号的分布，导致 Sharpe 和 Fitness 都远低于阈值

### 解决方向
1. **仅使用简单预处理方法**: rank(ts_backfill(...))，避免添加额外的预处理方法和算子
2. **尝试不同的 2腿组合**: short_term + event_5d, short_term + long_term, event_5d + long_term
3. **使用 group_zscore 算子**: 满足多样性闸门要求
4. **避免仅调整权重**: 会导致 SELF_CORRELATION 过高

## 字段说明

基于 multifactor_return_pred 数据集，使用以下字段：
- `short_term_price_volume_based_return_5d`: 短期价格成交量动量（5 天）- **已验证有效**
- `event_5d_single_quantile_pred`: 事件驱动预测（5 天）- **已验证有效**
- `long_term_quantile5_r120_pred`: 长期趋势预测（120 天）- **已验证有效**

## 特征工程策略

### 策略 1: 2腿组合（short_term + event_5d）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: short_term_price_volume_based_return_5d（权重 0.5-0.6）
- 腿 2: event_5d_single_quantile_pred（权重 0.4-0.5）

### 策略 2: 2腿组合（short_term + long_term）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: short_term_price_volume_based_return_5d（权重 0.5-0.6）
- 腿 2: long_term_quantile5_r120_pred（权重 0.4-0.5）

### 策略 3: 2腿组合（event_5d + long_term）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: event_5d_single_quantile_pred（权重 0.5-0.6）
- 腿 2: long_term_quantile5_r120_pred（权重 0.4-0.5）

### 策略 4: 单字段 + group_zscore
使用单字段，加入 group_zscore 算子：
- short_term_price_volume_based_return_5d + group_zscore
- event_5d_single_quantile_pred + group_zscore

## 建议

1. **字段选择**：继续使用已验证的字段（short_term, event_5d, long_term），避免使用完全不同的字段。
2. **权重配置**：使用 2腿组合，平衡权重（0.5/0.5 或 0.6/0.4）。
3. **预处理**：仅使用 rank(ts_backfill(...)) 预处理方法，避免添加额外的预处理方法和算子。
4. **多样性**：通过不同的 2腿组合和 group_zscore 算子，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-2 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的 2腿组合，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=21）。

## 预期改进

- 通过使用 2腿组合 + 简单预处理方法，预期提高信号质量
- 通过使用不同的 2腿组合，预期降低 SELF_CORRELATION
- 目标：挖掘更多候选 alpha（目标 10 个）
