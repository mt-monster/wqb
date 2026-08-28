# Wave 17 特征工程文档 - 降低 SELF_CORRELATION（multifactor_return_pred）

## 基础信息
- **Wave**: 17
- **Region**: USA
- **Dataset**: multifactor_return_pred
- **基础配方**: Wave 16 失败教训（SELF_CORRELATION FAIL）
- **优化目标**: 降低 SELF_CORRELATION，使用不同的字段组合和权重配置

## 失败教训分析

### Wave 16 失败原因
- **问题**: SELF_CORRELATION FAIL（0.72-0.79 > 0.7）
- **原因**: 
  1. 使用了相同的字段（long_term_quantile5_r120_pred）作为主导信号
  2. 权重配置相似（0.4-0.5 的权重给 long_term）
  3. 与已有的 alpha 信号过于相似

### 解决方向
1. **降低 long_term 权重**: 从 0.4-0.5 降低到 0.2-0.3
2. **增加其他字段权重**: 增加 short_term, event_5d 等字段的权重
3. **使用不同的字段组合**: 尝试不使用 long_term_quantile5_r120_pred
4. **使用不同的预处理**: 尝试不同的 ts_backfill 窗口（如 33, 99）
5. **使用不同的算子**: 尝试 ts_zscore, ts_rank 等

## 字段说明

基于 multifactor_return_pred 数据集，使用以下字段：
- `short_term_price_volume_based_return_5d`: 短期价格成交量动量（5 天）
- `short_hedge_quantile5_r60_pred`: 短期对冲预测（60 天）
- `event_5d_single_quantile_pred`: 事件驱动预测（5 天）
- `long_term_quantile5_r120_pred`: 长期趋势预测（120 天，降低权重）

## 特征工程策略

### 策略 1: 3腿组合（不使用 long_term）
使用 3 个字段，平衡权重（0.4/0.3/0.3）：
- 腿 1: short_term_price_volume_based_return_5d（权重 0.4）
- 腿 2: event_5d_single_quantile_pred（权重 0.3）
- 腿 3: short_hedge_quantile5_r60_pred（权重 0.3）

### 策略 2: 3腿组合（降低 long_term 权重）
使用 3 个字段，降低 long_term 权重（0.4/0.4/0.2）：
- 腿 1: short_term_price_volume_based_return_5d（权重 0.4）
- 腿 2: event_5d_single_quantile_pred（权重 0.4）
- 腿 3: long_term_quantile5_r120_pred（权重 0.2）

### 策略 3: 2腿组合（平衡权重）
使用 2 个字段，平衡权重（0.5/0.5）：
- 腿 1: short_term_price_volume_based_return_5d 或 short_hedge_quantile5_r60_pred（权重 0.5）
- 腿 2: event_5d_single_quantile_pred（权重 0.5）

### 策略 4: 单字段 + ts_zscore/ts_rank
使用单字段，加入 ts_zscore 或 ts_rank 算子：
- short_term_price_volume_based_return_5d + ts_zscore
- event_5d_single_quantile_pred + ts_rank
- short_hedge_quantile5_r60_pred + ts_zscore

## 建议

1. **字段选择**：使用 multifactor_return_pred 数据集的 short_term_price_volume_based_return_5d, short_hedge_quantile5_r60_pred, event_5d_single_quantile_pred 字段，避免过度依赖 long_term_quantile5_r120_pred。
2. **权重配置**：降低 long_term 权重（0.2-0.3），增加其他字段权重（0.3-0.4），避免信号过于集中在单一字段。
3. **预处理**：使用 ts_backfill（66 天窗口）处理缺失值，提高信号稳定性。
4. **多样性**：通过 3腿组合、2腿组合、单字段平滑等多种策略，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-3 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的字段组合和权重配置，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=17）。

## 预期改进

- 通过降低 SELF_CORRELATION，预期提高 Judge 评估通过率
- 通过使用不同的字段组合和权重配置，预期提高多样性
- 目标：挖掘更多候选 alpha（目标 10 个）
