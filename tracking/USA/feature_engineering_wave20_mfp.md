# Wave 20 特征工程文档 - 使用已验证字段组合 + 不同预处理方法/算子（multifactor_return_pred）

## 基础信息
- **Wave**: 20
- **Region**: USA
- **Dataset**: multifactor_return_pred
- **基础配方**: Wave 17 成功配方（1Ywx8ZpR）+ Wave 19 失败教训
- **优化目标**: 使用已验证字段组合 + 不同预处理方法/算子

## Wave 19 失败教训分析

### 失败原因
- **问题**: LOW_SHARPE（0.98-0.99 < 1.58）, LOW_FITNESS（0.39-0.40 < 1.0）
- **原因**: 
  1. 使用了完全不同的字段组合（short_hedge + event_5d 或 short_hedge + long_term）
  2. 这些字段组合的信号质量不如已验证的字段组合（short_term + event_5d + long_term）
  3. 导致 Sharpe 和 Fitness 都远低于阈值

### 解决方向
1. **继续使用已验证的字段组合**: short_term + event_5d + long_term（权重 0.4/0.4/0.2）
2. **尝试不同的预处理方法**: ts_zscore, ts_rank, ts_arg_max, ts_arg_min, ts_av_diff, ts_delta
3. **尝试不同的算子**: group_zscore, group_std_dev
4. **避免仅调整权重**: 会导致 SELF_CORRELATION 过高

## 字段说明

基于 multifactor_return_pred 数据集，使用以下字段：
- `short_term_price_volume_based_return_5d`: 短期价格成交量动量（5 天）- **已验证有效**
- `event_5d_single_quantile_pred`: 事件驱动预测（5 天）- **已验证有效**
- `long_term_quantile5_r120_pred`: 长期趋势预测（120 天）- **已验证有效**

## 特征工程策略

### 策略 1: 已验证字段组合 + ts_zscore
使用已验证的字段组合和权重（0.4/0.4/0.2），加入 ts_zscore 预处理方法：
- 腿 1: short_term_price_volume_based_return_5d + ts_zscore（权重 0.4）
- 腿 2: event_5d_single_quantile_pred + ts_zscore（权重 0.4）
- 腿 3: long_term_quantile5_r120_pred + ts_zscore（权重 0.2）

### 策略 2: 已验证字段组合 + ts_rank
使用已验证的字段组合和权重（0.4/0.4/0.2），加入 ts_rank 预处理方法：
- 腿 1: short_term_price_volume_based_return_5d + ts_rank（权重 0.4）
- 腿 2: event_5d_single_quantile_pred + ts_rank（权重 0.4）
- 腿 3: long_term_quantile5_r120_pred + ts_rank（权重 0.2）

### 策略 3: 已验证字段组合 + group_zscore/group_std_dev
使用已验证的字段组合和权重（0.4/0.4/0.2），加入 group_zscore 或 group_std_dev 算子：
- 腿 1: short_term_price_volume_based_return_5d + group_zscore/group_std_dev（权重 0.4）
- 腿 2: event_5d_single_quantile_pred + group_zscore/group_std_dev（权重 0.4）
- 腿 3: long_term_quantile5_r120_pred + group_zscore/group_std_dev（权重 0.2）

### 策略 4: 已验证字段组合 + ts_arg_max/ts_arg_min/ts_av_diff/ts_delta
使用已验证的字段组合和权重（0.4/0.4/0.2），加入 ts_arg_max, ts_arg_min, ts_av_diff 或 ts_delta 算子：
- 腿 1: short_term_price_volume_based_return_5d + ts_arg_max/ts_arg_min/ts_av_diff/ts_delta（权重 0.4）
- 腿 2: event_5d_single_quantile_pred + ts_arg_max/ts_arg_min/ts_av_diff/ts_delta（权重 0.4）
- 腿 3: long_term_quantile5_r120_pred + ts_arg_max/ts_arg_min/ts_av_diff/ts_delta（权重 0.2）

## 建议

1. **字段选择**：继续使用已验证的字段组合（short_term + event_5d + long_term），避免使用完全不同的字段组合。
2. **权重配置**：使用已验证的权重配置（0.4/0.4/0.2），避免仅调整权重。
3. **预处理**：使用 ts_backfill（66 天窗口）处理缺失值，提高信号稳定性。
4. **多样性**：通过不同的预处理方法和算子，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-3 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的预处理方法和算子，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=20）。

## 预期改进

- 通过使用已验证的字段组合，预期提高信号质量
- 通过使用不同的预处理方法和算子，预期降低 SELF_CORRELATION
- 目标：挖掘更多候选 alpha（目标 10 个）
