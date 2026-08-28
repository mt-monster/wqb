# Wave 18 特征工程文档 - 基于 Wave 17 成功配方（multifactor_return_pred）

## 基础信息
- **Wave**: 18
- **Region**: USA
- **Dataset**: multifactor_return_pred
- **基础配方**: Wave 17 成功配方（1Ywx8ZpR）
- **优化目标**: 继续挖掘更多候选，尝试不同的字段组合和权重配置

## Wave 17 成功配方分析

### 1Ywx8ZpR 成功原因
- **表达式**: `rank(add(multiply(0.4, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.4, rank(ts_backfill(event_5d_single_quantile_pred, 66))), multiply(0.2, rank(ts_backfill(long_term_quantile5_r120_pred, 66)))))`
- **SELF_CORRELATION**: 0.5906 < 0.7 (PASS)
- **Platform Submit OK**: True
- **成功原因**: 降低 long_term 权重（0.2），增加 short_term 和 event_5d 权重（0.4/0.4）

## 字段说明

基于 multifactor_return_pred 数据集，使用以下字段：
- `short_term_price_volume_based_return_5d`: 短期价格成交量动量（5 天）
- `short_hedge_quantile5_r60_pred`: 短期对冲预测（60 天）
- `event_5d_single_quantile_pred`: 事件驱动预测（5 天）
- `long_term_quantile5_r120_pred`: 长期趋势预测（120 天，降低权重）

## 特征工程策略

### 策略 1: 微调权重（基于 1Ywx8ZpR）
使用 3 个字段，微调权重（0.35/0.45/0.20 或 0.45/0.35/0.20）：
- 腿 1: short_term_price_volume_based_return_5d（权重 0.35-0.45）
- 腿 2: event_5d_single_quantile_pred（权重 0.35-0.45）
- 腿 3: long_term_quantile5_r120_pred（权重 0.20）

### 策略 2: 不使用 long_term（降低 SELF_CORRELATION）
使用 3 个字段，不使用 long_term（0.35/0.35/0.30 或 0.40/0.30/0.30）：
- 腿 1: short_term_price_volume_based_return_5d（权重 0.35-0.40）
- 腿 2: event_5d_single_quantile_pred（权重 0.30-0.35）
- 腿 3: short_hedge_quantile5_r60_pred（权重 0.30）

### 策略 3: 2腿组合（简化策略）
使用 2 个字段，平衡权重（0.50/0.50 或 0.60/0.40）：
- 腿 1: short_term_price_volume_based_return_5d（权重 0.50-0.60）
- 腿 2: event_5d_single_quantile_pred（权重 0.40-0.50）

### 策略 4: 不同预处理方法
使用 3 个字段，尝试不同的预处理方法（ts_zscore 或 ts_rank）：
- 腿 1: short_term_price_volume_based_return_5d + ts_zscore/ts_rank（权重 0.40）
- 腿 2: event_5d_single_quantile_pred + ts_zscore/ts_rank（权重 0.40）
- 腿 3: long_term_quantile5_r120_pred + ts_zscore/ts_rank（权重 0.20）

## 建议

1. **字段选择**：使用 multifactor_return_pred 数据集的 short_term_price_volume_based_return_5d, short_hedge_quantile5_r60_pred, event_5d_single_quantile_pred 字段，避免过度依赖 long_term_quantile5_r120_pred。
2. **权重配置**：降低 long_term 权重（0.2），增加其他字段权重（0.3-0.45），避免信号过于集中在单一字段。
3. **预处理**：使用 ts_backfill（66 天窗口）处理缺失值，提高信号稳定性。
4. **多样性**：通过 3腿组合、2腿组合、不同预处理方法等多种策略，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-3 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的字段组合和权重配置，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=18）。

## 预期改进

- 通过微调权重和尝试不同字段组合，预期提高多样性
- 通过尝试不同预处理方法，预期找到更优的信号处理方式
- 目标：挖掘更多候选 alpha（目标 10 个）
