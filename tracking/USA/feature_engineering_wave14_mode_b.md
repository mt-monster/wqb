# Wave 14 特征工程文档 - Mode B 想法层优化（提高子宇宙 Sharpe）

## 基础信息
- **Wave**: 14
- **Region**: USA
- **Dataset**: analyst_earnings_ibes
- **问题**: LOW_SUB_UNIVERSE_SHARPE FAIL（0.78-0.82 < 0.87）
- **优化目标**: 提高子宇宙 Sharpe >= 0.87

## 问题分析

### LOW_SUB_UNIVERSE_SHARPE 失败原因
当前候选表达式（Jj7GMK5E, ZY7EPGx0）的子宇宙 Sharpe 只有 0.78-0.82，低于阈值 0.87。

**可能原因**：
1. **信号在某些子宇宙中表现不佳**：当前表达式主要依赖 long_term_quantile5_r120_pred，可能在某些行业或市值范围内表现不稳定
2. **权重分配不合理**：0.5 权重集中在 long_term，可能导致信号过于单一
3. **缺乏多样性**：虽然使用了多个字段，但核心信号仍然集中在长期预测

### 改进策略

**Mode B 想法层优化**：
1. **增加信号多样性**：引入更多不同类型的字段（如基本面、情绪、技术指标）
2. **平衡权重分配**：避免过度依赖单一字段，使用更均衡的权重
3. **使用 ts_zscore 替代 rank**：ts_zscore 可能在某些子宇宙中表现更稳定
4. **引入 ts_mean 平滑**：减少噪声，提高信号稳定性

## 字段说明

基于 analyst_earnings_ibes 数据集，使用以下字段：
- `est_q_eps_mean`: 季度 EPS 预测均值
- `est_q_eps_mean_3mth_ago`: 3 个月前季度 EPS 预测均值
- `est_q_net_mean`: 季度净利润预测均值
- `est_q_net_mean_3mth_ago`: 3 个月前季度净利润预测均值
- `est_q_eps_med`: 季度 EPS 预测中位数
- `est_q_eps_std`: 季度 EPS 预测标准差

## 特征工程策略

### 策略 1: 变化率信号（基于 MEA 成功案例）
使用 EPS 和净利润的变化率，捕捉分析师预期的变化：
- `divide(est_q_eps_mean, est_q_eps_mean_3mth_ago)`: EPS 变化率
- `divide(est_q_net_mean, est_q_net_mean_3mth_ago)`: 净利润变化率

### 策略 2: 预测分散度信号
使用预测标准差，捕捉分析师预期的不确定性：
- `divide(est_q_eps_std, est_q_eps_mean)`: EPS 预测变异系数
- `subtract(est_q_eps_mean, est_q_eps_med)`: EPS 预测均值与中位数差异

### 策略 3: 组合信号
结合变化率和分散度，构建更稳健的信号：
- 变化率信号捕捉趋势
- 分散度信号捕捉不确定性
- 组合使用可以提高在不同子宇宙中的表现

## 表达式列表

共生成 8 个优化表达式，详见 expressions 表（wave=14）。

## 预期改进

- 通过引入变化率和分散度信号，预期提高在不同子宇宙中的表现
- 通过平衡权重分配，预期减少对单一字段的依赖
- 目标：子宇宙 Sharpe >= 0.87
