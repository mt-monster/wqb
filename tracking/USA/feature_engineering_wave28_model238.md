# Wave 28 特征工程文档 - 使用 model238 数据集

## 基础信息
- **Wave**: 28
- **Region**: USA
- **Dataset**: model238
- **基础配方**: Wave 21-27 失败教训（multifactor_return_pred SELF_CORRELATION 问题，analyst_consensus、pv_tech_indicators、pattern_scores、insider_feats 信号质量差）
- **优化目标**: 使用 model238 数据集的 mdl238_global_rank 字段，基于 IND 区域的成功经验（Sharpe=2.59, Fitness=2.88）

## Wave 21-27 失败教训分析

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
- **问题 4**: pattern_scores 数据集的图表模式相似度分数字段信号质量非常差
  - 8 个候选全部失败（LOW_SHARPE, LOW_FITNESS, LOW_2Y_SHARPE）
  - Sharpe 范围: 0.16 到 0.41（远低于 1.58 阈值）
  - Fitness 范围: 0.02 到 0.10（远低于 1.0 阈值）
- **问题 5**: insider_feats 数据集网络超时，无法完成回测
- **问题 6**: event_return_model 数据集网络超时，无法完成回测

### 解决方向
1. **尝试其他数据集**: 避免 multifactor_return_pred、analyst_consensus、pv_tech_indicators、pattern_scores、insider_feats 和 event_return_model 数据集，尝试 model238 数据集
2. **使用 mdl238_global_rank 字段**: 基于 IND 区域的成功经验（Sharpe=2.59, Fitness=2.88）
3. **使用简单的预处理方法**: rank, ts_backfill, ts_zscore, ts_mean, group_zscore, ts_decay_linear
4. **使用 2腿组合**: 比 3腿组合更容易通过 SELF_CORRELATION 检查

## 字段说明

基于 model238 数据集，使用以下字段：
- `mdl238_global_rank`: 模型238全局排名 - **已验证**（在 IND 区域 Sharpe=2.59, Fitness=2.88）
- `mdl238_sector_rank`: 模型238行业排名 - **未验证**
- `mdl238_industry_rank`: 模型238子行业排名 - **未验证**
- `mdl238_global_rank_change`: 模型238全局排名变化 - **未验证**

## 特征工程策略

### 策略 1: 单字段 + rank
使用单字段，仅使用 rank 预处理方法：
- mdl238_global_rank + rank

### 策略 2: 单字段 + ts_zscore/ts_mean/ts_decay_linear
使用单字段，使用时间序列预处理方法：
- mdl238_global_rank + ts_zscore(60)
- mdl238_global_rank + ts_mean(20)
- mdl238_global_rank + ts_decay_linear(10)

### 策略 3: 2腿组合（global_rank + sector/industry_rank）
使用 2 个字段，平衡权重（0.6/0.4 或 0.7/0.3）：
- 腿 1: mdl238_global_rank（权重 0.6-0.7）
- 腿 2: mdl238_sector_rank 或 mdl238_industry_rank（权重 0.3-0.4）

### 策略 4: 使用 group_zscore 算子
使用 group_zscore 算子，满足多样性闸门要求：
- group_zscore(mdl238_global_rank, subindustry)

## 建议

1. **字段选择**：使用 model238 数据集的 mdl238_global_rank 字段，避免使用 multifactor_return_pred、analyst_consensus、pv_tech_indicators、pattern_scores、insider_feats 和 event_return_model 数据集的字段。
2. **算子选择**：使用 rank, ts_backfill, ts_zscore, ts_mean, group_zscore, ts_decay_linear 等算子，提高信号质量。
3. **预处理**：使用 ts_backfill 计算时间序列回填，使用 rank 计算排名。
4. **多样性**：通过不同的字段组合和算子，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-2 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的数据集和字段组合，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=28）。

## 预期改进

- 通过使用 model238 数据集，预期降低 SELF_CORRELATION
- 通过使用 mdl238_global_rank 字段，预期保持信号质量（基于 IND 区域的成功经验）
- 通过使用简单的预处理方法，预期提高信号质量
- 目标：挖掘更多候选 alpha（目标 10 个）
