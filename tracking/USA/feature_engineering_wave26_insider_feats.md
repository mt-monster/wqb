# Wave 26 特征工程文档 - 使用 insider_feats 数据集

## 基础信息
- **Wave**: 26
- **Region**: USA
- **Dataset**: insider_feats
- **基础配方**: Wave 21-25 失败教训（multifactor_return_pred SELF_CORRELATION 问题，analyst_consensus、pv_tech_indicators 和 pattern_scores 信号质量差）
- **优化目标**: 使用内部人交易相关的字段，避免 multifactor_return_pred 数据集的 SELF_CORRELATION 问题

## Wave 21-25 失败教训分析

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

### 解决方向
1. **尝试其他数据集**: 避免 multifactor_return_pred、analyst_consensus、pv_tech_indicators 和 pattern_scores 数据集，尝试 insider_feats 数据集
2. **使用内部人交易相关的字段**: 使用内部人买卖比例、交易次数等字段
3. **使用 vec_avg 聚合**: 对于 VECTOR 字段，必须使用 vec_* 聚合
4. **使用 2腿组合**: 比 3腿组合更容易通过 SELF_CORRELATION 检查

## 字段说明

基于 insider_feats 数据集，使用以下字段：
- `buy_sell_ratio_all_20d_filled`: 所有内部人 20 天买卖比例（填充）- **未验证**
- `buy_sell_ratio_all_60d_filled`: 所有内部人 60 天买卖比例（填充）- **未验证**
- `buy_sell_ratio_all_250d_filled`: 所有内部人 250 天买卖比例（填充）- **未验证**
- `buy_to_sell_ratio_all_20d`: 所有内部人 20 天买卖比例 - **未验证**
- `top20_buy_to_sell_txn_ratio_lookback_20_filled`: 前 20 内部人 20 天买卖交易比例（填充）- **未验证**
- `top20_buy_tx_count_20d`: 前 20 内部人 20 天买入交易次数 - **未验证**
- `top20_sale_tx_count_20d`: 前 20 内部人 20 天卖出交易次数 - **未验证**
- `top5_buy_to_sell_txn_ratio_lookback_20_filled`: 前 5 内部人 20 天买卖交易比例（填充）- **未验证**
- `top5_buy_tx_count_20d`: 前 5 内部人 20 天买入交易次数 - **未验证**
- `top5_insider_sale_volume_lookback_250`: 前 5 内部人 250 天卖出交易量 - **未验证**
- `top5_sale_tx_count_20d`: 前 5 内部人 20 天卖出交易次数 - **未验证**
- `total_sale_tx_count_250d`: 所有内部人 250 天卖出交易次数 - **未验证**

## 特征工程策略

### 策略 1: 单字段 + rank
使用单字段，仅使用 rank 预处理方法：
- buy_sell_ratio_all_20d_filled + rank
- buy_sell_ratio_all_60d_filled + rank
- top20_buy_to_sell_txn_ratio_lookback_20_filled + rank

### 策略 2: 2腿组合（buy_sell_ratio + top20/top5）
使用 2 个字段，平衡权重（0.5/0.5 或 0.6/0.4）：
- 腿 1: buy_sell_ratio_all_20d_filled（权重 0.5-0.6）
- 腿 2: top20_buy_to_sell_txn_ratio_lookback_20_filled 或 top5_buy_to_sell_txn_ratio_lookback_20_filled（权重 0.4-0.5）

### 策略 3: 使用 vec_avg 聚合
对于 VECTOR 字段，使用 vec_avg 聚合：
- vec_avg(top5_insider_sale_volume_lookback_250)
- vec_avg(top20_buy_tx_count_20d)

### 策略 4: 使用 reverse 和 divide 算子
使用 reverse 和 divide 算子，计算反向比例：
- reverse(divide(vec_avg(top5_insider_sale_volume_lookback_250), vec_avg(top20_buy_tx_count_20d)))

## 建议

1. **字段选择**：使用内部人交易相关的字段（buy_sell_ratio, top20/top5 交易次数），避免使用 multifactor_return_pred、analyst_consensus、pv_tech_indicators 和 pattern_scores 数据集的字段。
2. **算子选择**：使用 rank, reverse, divide, vec_avg 等算子，提高信号质量。
3. **预处理**：对于 VECTOR 字段，必须使用 vec_* 聚合；对于 MATRIX 字段，使用 rank 预处理方法。
4. **多样性**：通过不同的字段组合和算子，提高候选 alpha 的多样性。
5. **风险控制**：避免使用过多字段（每条表达式尽量只用 1-2 个字段），降低过拟合风险。
6. **SELF_CORRELATION 控制**：通过使用不同的数据集和字段组合，降低与已有 alpha 的自相关性。

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=26）。

## 预期改进

- 通过使用 insider_feats 数据集，预期降低 SELF_CORRELATION
- 通过使用内部人交易相关的字段，预期保持信号质量
- 通过使用 vec_avg, reverse, divide 等算子，预期提高信号质量
- 目标：挖掘更多候选 alpha（目标 10 个）
