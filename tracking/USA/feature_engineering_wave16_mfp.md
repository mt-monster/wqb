# Wave 16 特征工程文档 - 基于 Wave 14 成功配方（multifactor_return_pred）

## 基础信息
- **Wave**: 16
- **Region**: USA
- **Dataset**: multifactor_return_pred
- **基础配方**: Wave 14 成功配方（3腿组合，平衡权重）
- **优化目标**: 尝试不同的字段组合，提高多样性，挖掘更多候选 alpha（目标 10 个）

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

基于 multifactor_return_pred 数据集，使用以下字段：
- `long_term_quantile5_r120_pred`: 长期趋势预测（120 天）
- `short_term_price_volume_based_return_5d`: 短期价格成交量动量（5 天）
- `short_hedge_quantile5_r60_pred`: 短期对冲预测（60 天）
- `event_5d_single_quantile_pred`: 事件驱动预测（5 天）
- `event_10d_single_quantile_pred`: 事件驱动预测（10 天）

## 特征工程策略

### 策略 1: 3腿组合（基于 Wave 14 成功配方）
使用 3 个字段，平衡权重（0.4/0.3/0.3）：
- 腿 1: long_term_quantile5_r120_pred（权重 0.4）
- 腿 2: short_term_price_volume_based_return_5d 或 short_hedge_quantile5_r60_pred（权重 0.3）
- 腿 3: event_5d_single_quantile_pred 或 event_10d_single_quantile_pred（权重 0.3）

### 策略 2: 多信号源组合
结合长期趋势、短期动量、事件驱动：
- 长期趋势捕捉长期趋势
- 短期动量捕捉短期价格成交量动量
- 事件驱动捕捉事件驱动机会

### 策略 3: 2腿组合 + group_zscore
使用 2 个字段，平衡权重（0.5/0.5），加入 group_zscore 算子：
- 腿 1: long_term_quantile5_r120_pred（权重 0.5）
- 腿 2: short_term_price_volume_based_return_5d 或 event_5d_single_quantile_pred（权重 0.5）

### 策略 4: 单字段 + ts_arg_max
使用单字段，加入 ts_arg_max 算子：
- long_term_quantile5_r120_pred

## 建议

1. **字段选择**：使用 multifactor_return_pred 数据集的 long_term_quantile5_r120_pred, short_term_price_volume_based_return_5d, short_hedge_quantile5_r60_pred, event_5d_single_quantile_pred, event_10d_single_quantile_pred 字段，这些字段已经在 Wave 14 验证过。
2. **权重配置**：基于 Wave 14 成功配方，使用平衡权重（0.4/0.3/0.3），避免信号过于集中在单一字段。
3. **预处理**：使用 ts_backfill（66 天窗口）处理缺失值，提高信号稳定性。
4. **多样性**：通过 3腿组合、2腿组合、单字段平滑等多种策略，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-3 个字段），降低过拟合风险。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=16）。

## 预期改进

- 通过使用 multifactor_return_pred 数据集，预期挖掘更多候选 alpha
- 通过基于 Wave 14 成功配方，预期提高成功率
- 通过尝试不同的字段组合，预期提高多样性
- 目标：挖掘更多候选 alpha（目标 10 个）
