# Wave 23 特征工程文档 - 使用 analyst_consensus 数据集

## 基础信息
- **Wave**: 23
- **Region**: USA
- **Dataset**: analyst_consensus
- **基础配方**: Wave 21-22 失败教训（multifactor_return_pred 数据集 SELF_CORRELATION 问题）
- **优化目标**: 使用分析师预期相关的字段，避免 multifactor_return_pred 数据集的 SELF_CORRELATION 问题

## Wave 21-22 失败教训分析

### 失败原因
- **问题**: multifactor_return_pred 数据集的 SELF_CORRELATION 问题难以解决
  - 已验证的字段组合（short_term, event_5d, long_term）信号质量好，但 SELF_CORRELATION 过高（0.77-0.97）
  - 不同的字段组合（short_hedge, long_term_r60）信号质量差，无法通过硬闸（Sharpe < 1.58, Fitness < 1.0）
- **原因**: 
  1. 已验证的字段组合与已有 alpha 相似，导致 SELF_CORRELATION 过高
  2. 不同的字段组合信号质量差，无法通过硬闸
  3. 需要找到一个平衡点：既能通过 SELF_CORRELATION 检查，又能保持信号质量

### 解决方向
1. **尝试其他数据集**: 避免 multifactor_return_pred 数据集，尝试其他数据集（analyst_consensus）
2. **使用分析师预期相关的字段**: 使用 mean_estimate_eps 相关的字段
3. **使用 2腿组合**: 比 3腿组合更容易通过 SELF_CORRELATION 检查
4. **使用 group_zscore 算子**: 满足多样性闸门要求

## 字段说明

基于 analyst_consensus 数据集，使用以下字段：
- `mean_estimate_eps_quarterly16`: 分析师预期 EPS 季度数据 - **未验证**
- `mean_estimate_eps_annual12`: 分析师预期 EPS 年度数据 - **未验证**
- `mean_estimate_fxadj_eps_quarterly16`: 分析师预期 EPS 季度数据（汇率调整）- **未验证**

## 特征工程策略

### 策略 1: 单字段 + rank
使用单字段，仅使用 rank(ts_backfill(...)) 预处理方法：
- mean_estimate_eps_quarterly16 + rank
- mean_estimate_eps_annual12 + rank
- mean_estimate_fxadj_eps_quarterly16 + rank

### 策略 2: 2腿组合（mean_estimate_eps_quarterly16 + mean_estimate_eps_annual12）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: mean_estimate_eps_quarterly16（权重 0.5-0.6）
- 腿 2: mean_estimate_eps_annual12（权重 0.4-0.5）

### 策略 3: 单字段 + group_zscore
使用单字段，加入 group_zscore 算子：
- mean_estimate_eps_quarterly16 + group_zscore
- mean_estimate_eps_annual12 + group_zscore

### 策略 4: 2腿组合 + group_zscore
使用 2 个字段，加入 group_zscore 算子：
- mean_estimate_eps_quarterly16 + mean_estimate_eps_annual12 + group_zscore

## 建议

1. **字段选择**：使用分析师预期相关的字段（mean_estimate_eps），避免使用 multifactor_return_pred 数据集的字段。
2. **权重配置**：使用 2腿组合，平衡权重（0.5/0.5 或 0.6/0.4）。
3. **预处理**：仅使用 rank(ts_backfill(...)) 预处理方法，避免添加额外的预处理方法和算子。
4. **多样性**：通过不同的字段组合和 group_zscore 算子，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-2 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的数据集和字段组合，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=23）。

## 预期改进

- 通过使用 analyst_consensus 数据集，预期降低 SELF_CORRELATION
- 通过使用分析师预期相关的字段，预期保持信号质量
- 目标：挖掘更多候选 alpha（目标 10 个）
