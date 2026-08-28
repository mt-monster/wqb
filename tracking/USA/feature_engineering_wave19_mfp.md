# Wave 19 特征工程文档 - 使用完全不同的字段组合（multifactor_return_pred）

## 基础信息
- **Wave**: 19
- **Region**: USA
- **Dataset**: multifactor_return_pred
- **基础配方**: Wave 18 失败教训（SELF_CORRELATION FAIL）
- **优化目标**: 使用完全不同的字段组合，降低 SELF_CORRELATION

## Wave 18 失败教训分析

### 失败原因
- **问题**: SELF_CORRELATION FAIL（0.9941 > 0.7）
- **原因**: 
  1. 使用了相同的字段组合（short_term + event_5d + long_term）
  2. 仅权重不同（0.45/0.35/0.2 vs 0.4/0.4/0.2）
  3. 与已有的 alpha（1Ywx8ZpR）信号过于相似

### 解决方向
1. **使用完全不同的字段组合**: 避免使用 short_term_price_volume_based_return_5d
2. **使用不同的字段**: 重点使用 short_hedge_quantile5_r60_pred
3. **使用不同的预处理方法**: 尝试 ts_zscore, ts_rank, ts_arg_max, ts_arg_min
4. **使用不同的算子**: 尝试 group_zscore, group_mean

## 字段说明

基于 multifactor_return_pred 数据集，使用以下字段：
- `short_hedge_quantile5_r60_pred`: 短期对冲预测（60 天）- **重点使用**
- `event_5d_single_quantile_pred`: 事件驱动预测（5 天）
- `long_term_quantile5_r120_pred`: 长期趋势预测（120 天）
- ~~`short_term_price_volume_based_return_5d`~~: **避免使用**（与已有 alpha 重复）

## 特征工程策略

### 策略 1: 2腿组合（short_hedge + event_5d）
使用 2 个字段，平衡权重（0.6/0.4 或 0.7/0.3）：
- 腿 1: short_hedge_quantile5_r60_pred（权重 0.6-0.7）
- 腿 2: event_5d_single_quantile_pred（权重 0.3-0.4）

### 策略 2: 2腿组合（short_hedge + long_term）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: short_hedge_quantile5_r60_pred（权重 0.5-0.6）
- 腿 2: long_term_quantile5_r120_pred（权重 0.4-0.5）

### 策略 3: 单字段 + 不同预处理方法
使用单字段，尝试不同的预处理方法：
- short_hedge_quantile5_r60_pred + ts_zscore/ts_arg_max
- event_5d_single_quantile_pred + ts_rank/ts_arg_min

### 策略 4: 加入 group_* 算子
使用 2 个字段，加入 group_zscore 或 group_mean 算子：
- short_hedge_quantile5_r60_pred + event_5d_single_quantile_pred + group_zscore
- short_hedge_quantile5_r60_pred + long_term_quantile5_r120_pred + group_mean

## 建议

1. **字段选择**：重点使用 short_hedge_quantile5_r60_pred，避免使用 short_term_price_volume_based_return_5d。
2. **权重配置**：使用 2腿组合，平衡权重（0.5/0.5 或 0.6/0.4 或 0.7/0.3）。
3. **预处理**：使用 ts_backfill（66 天窗口）处理缺失值，提高信号稳定性。
4. **多样性**：通过 2腿组合、单字段、不同预处理方法等多种策略，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-2 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用完全不同的字段组合，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=19）。

## 预期改进

- 通过使用完全不同的字段组合，预期降低 SELF_CORRELATION
- 通过使用不同的预处理方法，预期找到更优的信号处理方式
- 目标：挖掘更多候选 alpha（目标 10 个）
