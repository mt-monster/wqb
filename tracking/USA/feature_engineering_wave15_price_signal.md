# Wave 15 特征工程文档 - 基于 Wave 14 成功配方（price_signal_dl）

## 基础信息
- **Wave**: 15
- **Region**: USA
- **Dataset**: price_signal_dl
- **基础配方**: Wave 14 成功配方（3腿组合，平衡权重）
- **优化目标**: 挖掘更多候选 alpha（目标 10 个）

## 成功配方分析

### Wave 14 成功配方
- **表达式**: `rank(add(multiply(0.4, rank(ts_backfill(long_term_quantile5_r120_pred, 66))), multiply(0.3, rank(ts_backfill(short_term_price_volume_based_return_5d, 66))), multiply(0.3, rank(ts_backfill(event_5d_single_quantile_pred, 66)))))`
- **骨架**: 3腿组合（long_term + short_term + event_5d）
- **权重**: 平衡权重（0.4/0.3/0.3）
- **预处理**: ts_backfill（66 天窗口）
- **结果**: Sharpe=2.100, Fitness=1.180, 所有平台硬闸通过

### 成功原因
1. **3腿组合**：避免信号过于集中在单一字段
2. **平衡权重**：避免过度依赖单一字段
3. **多信号源**：结合长期趋势、短期动量、事件驱动
4. **ts_backfill**：处理缺失值，提高信号稳定性

## 字段说明

基于 price_signal_dl 数据集，使用以下字段：
- `normalized_trend_indicator_3`: 归一化趋势指标 3
- `normalized_trend_indicator_4`: 归一化趋势指标 4
- `raw_trend_indicator_3`: 原始趋势指标 3
- `raw_trend_indicator_4`: 原始趋势指标 4

## 特征工程策略

### 策略 1: 3腿组合（基于 Wave 14 成功配方）
使用 3 个字段，平衡权重（0.4/0.3/0.3）：
- 腿 1: normalized_trend_indicator_3（权重 0.4）
- 腿 2: normalized_trend_indicator_4（权重 0.3）
- 腿 3: raw_trend_indicator_3（权重 0.3）

### 策略 2: 多信号源组合
结合归一化趋势指标和原始趋势指标：
- 归一化趋势指标捕捉标准化趋势
- 原始趋势指标捕捉原始趋势
- 多指标组合捕捉不同时间尺度的趋势

### 策略 3: 单字段平滑
使用 ts_mean 平滑单字段信号，提高信号稳定性：
- ts_mean(normalized_trend_indicator_3, 10)
- ts_mean(normalized_trend_indicator_4, 10)

## 建议

1. **字段选择**：使用 price_signal_dl 数据集的 normalized_trend_indicator_3/4 和 raw_trend_indicator_3/4 字段，这些字段已经在之前的回测中验证过。
2. **权重配置**：基于 Wave 14 成功配方，使用平衡权重（0.4/0.3/0.3），避免信号过于集中在单一字段。
3. **预处理**：使用 ts_backfill（66 天窗口）处理缺失值，提高信号稳定性。
4. **多样性**：通过 3腿组合、2腿组合、单字段平滑等多种策略，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-3 个字段），降低过拟合风险。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=15）。

## 预期改进

- 通过使用 price_signal_dl 数据集，预期挖掘更多候选 alpha
- 通过基于 Wave 14 成功配方，预期提高成功率
- 目标：挖掘更多候选 alpha（目标 10 个）
