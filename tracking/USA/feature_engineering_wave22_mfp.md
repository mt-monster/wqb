# Wave 22 特征工程文档 - 使用完全不同的字段组合（multifactor_return_pred）

## 基础信息
- **Wave**: 22
- **Region**: USA
- **Dataset**: multifactor_return_pred
- **基础配方**: Wave 21 失败教训（SELF_CORRELATION FAIL）
- **优化目标**: 使用完全不同的字段组合，避免 SELF_CORRELATION 过高

## Wave 21 失败教训分析

### 失败原因
- **问题**: 所有 4 个 Fitness >= 1.0 的候选都因为 SELF_CORRELATION 过高而被 BLOCK
  - RR7bM59j: SELF_CORRELATION = 0.9638 > 0.7
  - 9qXVeWX1: SELF_CORRELATION = 0.9702 > 0.7
  - P072NPxw: SELF_CORRELATION = 0.781 > 0.7
  - 3qlXwG1g: SELF_CORRELATION = 0.7664 > 0.7
- **原因**: 
  1. 这些候选使用了相同的字段组合（short_term + event_5d 或 short_term + long_term），仅权重不同
  2. 即使使用 2腿组合，如果字段组合与已有 alpha 相似，SELF_CORRELATION 仍然会很高
  3. 平台判定这些 alpha 高度相关（0.77-0.97），因为它们本质上使用了相同的信号源

### 解决方向
1. **使用完全不同的字段组合**: 避免使用 short_term, event_5d, long_term 这些已验证的字段
2. **尝试其他字段**: 从 multifactor_return_pred 数据集中选择其他字段（short_hedge, event_10d, long_term_r60）
3. **使用 2腿组合**: 比 3腿组合更容易通过 SELF_CORRELATION 检查
4. **使用 group_zscore 算子**: 满足多样性闸门要求

## 字段说明

基于 multifactor_return_pred 数据集，使用以下字段：
- `short_hedge_quantile5_r60_pred`: 短期对冲预测（60 天）- **未验证**
- `event_10d_single_quantile_pred`: 事件驱动预测（10 天）- **未验证**
- `long_term_quantile5_r60_pred`: 长期趋势预测（60 天）- **未验证**

## 特征工程策略

### 策略 1: 2腿组合（short_hedge + event_10d）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: short_hedge_quantile5_r60_pred（权重 0.5-0.6）
- 腿 2: event_10d_single_quantile_pred（权重 0.4-0.5）

### 策略 2: 2腿组合（short_hedge + long_term_r60）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: short_hedge_quantile5_r60_pred（权重 0.5-0.6）
- 腿 2: long_term_quantile5_r60_pred（权重 0.4-0.5）

### 策略 3: 2腿组合（event_10d + long_term_r60）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: event_10d_single_quantile_pred（权重 0.5-0.6）
- 腿 2: long_term_quantile5_r60_pred（权重 0.4-0.5）

### 策略 4: 单字段 + group_zscore
使用单字段，加入 group_zscore 算子：
- short_hedge_quantile5_r60_pred + group_zscore
- event_10d_single_quantile_pred + group_zscore

## 建议

1. **字段选择**：使用完全不同的字段（short_hedge, event_10d, long_term_r60），避免使用已验证的字段（short_term, event_5d, long_term）。
2. **权重配置**：使用 2腿组合，平衡权重（0.5/0.5 或 0.6/0.4）。
3. **预处理**：仅使用 rank(ts_backfill(...)) 预处理方法，避免添加额外的预处理方法和算子。
4. **多样性**：通过不同的 2腿组合和 group_zscore 算子，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-2 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用完全不同的字段组合，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=22）。

## 预期改进

- 通过使用完全不同的字段组合，预期降低 SELF_CORRELATION
- 通过使用 2腿组合 + 简单预处理方法，预期保持信号质量
- 目标：挖掘更多候选 alpha（目标 10 个）
