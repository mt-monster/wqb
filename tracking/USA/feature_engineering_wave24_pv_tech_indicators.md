# Wave 24 特征工程文档 - 使用 pv_tech_indicators 数据集

## 基础信息
- **Wave**: 24
- **Region**: USA
- **Dataset**: pv_tech_indicators
- **基础配方**: Wave 21-23 失败教训（multifactor_return_pred SELF_CORRELATION 问题，analyst_consensus 信号质量差）
- **优化目标**: 使用技术指标相关的字段，避免 multifactor_return_pred 数据集的 SELF_CORRELATION 问题

## Wave 21-23 失败教训分析

### 失败原因
- **问题 1**: multifactor_return_pred 数据集的 SELF_CORRELATION 问题难以解决
  - 已验证的字段组合（short_term, event_5d, long_term）信号质量好，但 SELF_CORRELATION 过高（0.77-0.97）
  - 不同的字段组合（short_hedge, long_term_r60）信号质量差，无法通过硬闸（Sharpe < 1.58, Fitness < 1.0）
- **问题 2**: analyst_consensus 数据集的 MATRIX 字段信号质量非常差
  - 8 个候选全部失败（LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE）
  - Sharpe 范围: -0.02 到 0.28（远低于 1.58 阈值）
  - Fitness 范围: -0.00 到 0.09（远低于 1.0 阈值）

### 解决方向
1. **尝试其他数据集**: 避免 multifactor_return_pred 和 analyst_consensus 数据集，尝试 pv_tech_indicators 数据集
2. **使用技术指标相关的字段**: 使用 momentum, price, volume 相关的字段
3. **使用 2腿组合**: 比 3腿组合更容易通过 SELF_CORRELATION 检查
4. **使用 group_zscore 算子**: 满足多样性闸门要求

## 字段说明

基于 pv_tech_indicators 数据集，使用以下字段：
- `momentum_shift_indicator`: 动量转换指标 - **未验证**
- `price_reversal_signal`: 价格反转信号 - **未验证**
- `price_acceleration_factor`: 价格加速因子 - **未验证**
- `volume_spike_score`: 成交量突增分数 - **未验证**
- `price_trend_score`: 价格趋势分数 - **未验证**
- `price_volatility_score`: 价格波动分数 - **未验证**
- `price_change_indicator`: 价格变化指标 - **未验证**
- `volume_change_indicator`: 成交量变化指标 - **未验证**
- `momentum_strength_index`: 动量强度指数 - **未验证**
- `price_momentum_factor`: 价格动量因子 - **未验证**

## 特征工程策略

### 策略 1: 单字段 + rank
使用单字段，仅使用 rank(ts_backfill(...)) 预处理方法：
- momentum_shift_indicator + rank
- price_reversal_signal + rank
- price_acceleration_factor + rank

### 策略 2: 2腿组合（momentum + price/volume）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: momentum_shift_indicator（权重 0.5-0.6）
- 腿 2: price_acceleration_factor 或 volume_spike_score（权重 0.4-0.5）

### 策略 3: 单字段 + group_zscore
使用单字段，加入 group_zscore 算子：
- momentum_shift_indicator + group_zscore
- price_reversal_signal + group_zscore

### 策略 4: 2腿组合 + group_zscore
使用 2 个字段，加入 group_zscore 算子：
- momentum_shift_indicator + price_acceleration_factor + group_zscore

## 建议

1. **字段选择**：使用技术指标相关的字段（momentum, price, volume），避免使用 multifactor_return_pred 和 analyst_consensus 数据集的字段。
2. **权重配置**：使用 2腿组合，平衡权重（0.5/0.5 或 0.6/0.4）。
3. **预处理**：仅使用 rank(ts_backfill(...)) 预处理方法，避免添加额外的预处理方法和算子。
4. **多样性**：通过不同的字段组合和 group_zscore 算子，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-2 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的数据集和字段组合，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=24）。

## 预期改进

- 通过使用 pv_tech_indicators 数据集，预期降低 SELF_CORRELATION
- 通过使用技术指标相关的字段，预期保持信号质量
- 目标：挖掘更多候选 alpha（目标 10 个）
