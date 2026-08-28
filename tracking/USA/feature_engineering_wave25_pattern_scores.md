# Wave 25 特征工程文档 - 使用 pattern_scores 数据集

## 基础信息
- **Wave**: 25
- **Region**: USA
- **Dataset**: pattern_scores
- **基础配方**: Wave 21-24 失败教训（multifactor_return_pred SELF_CORRELATION 问题，analyst_consensus 和 pv_tech_indicators 信号质量差）
- **优化目标**: 使用图表模式相关的字段，避免 multifactor_return_pred 数据集的 SELF_CORRELATION 问题

## Wave 21-24 失败教训分析

### 失败原因
- **问题 1**: multifactor_return_pred 数据集的 SELF_CORRELATION 问题难以解决
  - 已验证的字段组合（short_term, event_5d, long_term）信号质量好，但 SELF_CORRELATION 过高（0.77-0.97）
  - 不同的字段组合（short_hedge, long_term_r60）信号质量差，无法通过硬闸（Sharpe < 1.58, Fitness < 1.0）
- **问题 2**: analyst_consensus 数据集的 MATRIX 字段信号质量非常差
  - 8 个候选全部失败（LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE）
  - Sharpe 范围: -0.02 到 0.28（远低于 1.58 阈值）
  - Fitness 范围: -0.00 到 0.09（远低于 1.0 阈值）
- **问题 3**: pv_tech_indicators 数据集的技术指标字段信号质量非常差
  - 8 个候选全部失败（LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE, LOW_SUB_UNIVERSE_SHARPE）
  - Sharpe 范围: -0.30 到 0.07（远低于 1.58 阈值）
  - Fitness 范围: -0.08 到 0.01（远低于 1.0 阈值）

### 解决方向
1. **尝试其他数据集**: 避免 multifactor_return_pred、analyst_consensus 和 pv_tech_indicators 数据集，尝试 pattern_scores 数据集
2. **使用图表模式相关的字段**: 使用图表模式相似度分数相关的字段
3. **使用复杂算子**: 使用 quantile, subtract, ts_av_diff 等算子，提高信号质量
4. **使用 2腿组合**: 比 3腿组合更容易通过 SELF_CORRELATION 检查

## 字段说明

基于 pattern_scores 数据集，使用以下字段：
- `dynamic_similarity_breakaway_gap_downward`: 动态相似度突破缺口向下 - **未验证**
- `dynamic_similarity_common_gap_downward`: 动态相似度普通缺口向下 - **未验证**
- `max_similarity_common_gap_downward`: 最大相似度普通缺口向下 - **未验证**
- `mean_similarity_common_gap_downward`: 平均相似度普通缺口向下 - **未验证**
- `median_similarity_breakaway_gap_downward`: 中位数相似度突破缺口向下 - **未验证**
- `median_similarity_common_gap_downward`: 中位数相似度普通缺口向下 - **未验证**
- `min_similarity_breakaway_gap_downward`: 最小相似度突破缺口向下 - **未验证**
- `min_similarity_common_gap_downward`: 最小相似度普通缺口向下 - **未验证**

## 特征工程策略

### 策略 1: 2腿组合（breakaway_gap_downward - common_gap_downward）
使用 2 个字段，计算它们的差异：
- 腿 1: dynamic_similarity_breakaway_gap_downward（权重 1.0）
- 腿 2: dynamic_similarity_common_gap_downward（权重 -1.0）

### 策略 2: 使用 quantile 算子
使用 quantile 算子，提高信号质量：
- quantile(subtract(ts_av_diff(dynamic_similarity_breakaway_gap_downward, 66), ts_av_diff(dynamic_similarity_common_gap_downward, 66)))

### 策略 3: 使用 ts_av_diff 算子
使用 ts_av_diff 算子，计算时间序列平均差异：
- ts_av_diff(dynamic_similarity_breakaway_gap_downward, 66)

## 建议

1. **字段选择**：使用图表模式相似度分数相关的字段（breakaway_gap_downward, common_gap_downward），避免使用 multifactor_return_pred、analyst_consensus 和 pv_tech_indicators 数据集的字段。
2. **算子选择**：使用 quantile, subtract, ts_av_diff 等算子，提高信号质量。
3. **预处理**：使用 ts_av_diff 计算时间序列平均差异，使用 quantile 计算分位数。
4. **多样性**：通过不同的字段组合和算子，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-2 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的数据集和字段组合，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=25）。

## 预期改进

- 通过使用 pattern_scores 数据集，预期降低 SELF_CORRELATION
- 通过使用图表模式相似度分数相关的字段，预期保持信号质量
- 通过使用 quantile, subtract, ts_av_diff 等算子，预期提高信号质量
- 目标：挖掘更多候选 alpha（目标 10 个）
