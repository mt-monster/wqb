# KOR delay1 other553 分析师预期修正事件流特征工程

## 数据集理解

**数据集**：other553（分析师预期/评级/目标价事件流）
**字段数**：21（全 VECTOR）
**覆盖率**：0.48-0.75（中等）
**竞争度**：alphaCount 0-11（低竞争）

**核心字段**：
- `oth553_est_estvalue` / `oth553_est_preestvalue`：当前/之前盈利预期值
- `oth553_recvalue` / `oth553_prerecvalue`：当前/之前评级值
- `oth553_ptgvalue` / `oth553_preptgvalue`：当前/之前目标价值
- `oth553_sal_estvalue` / `oth553_sal_preestvalue`：当前/之前销售预期值

**数据结构**：VECTOR 事件流，每个字段包含多个分析师的预期/评级/目标价，需 `vec_avg` 聚合为 MATRIX。

## 字段解构分析

**预期修正方向**（est_estvalue - est_preestvalue）：
- 测的是：分析师对公司盈利预期的变化方向与幅度
- 逻辑含义：预期上调 → 公司基本面改善 → 未来收益正
- 方向性：正值（预期上调）→ 做多；负值（预期下调）→ 做空

**评级修正方向**（recvalue - prerecvalue）：
- 测的是：分析师评级的变化方向（1-5 分，1=买入，5=卖出）
- 逻辑含义：评级下调（分数减小）→ 公司基本面改善 → 未来收益正
- 方向性：负值（评级下调，分数减小）→ 做多；正值（评级上调，分数增大）→ 做空

**目标价修正方向**（ptgvalue - preptgvalue）：
- 测的是：分析师目标价的变化方向与幅度
- 逻辑含义：目标价上调 → 公司估值提升 → 未来收益正
- 方向性：正值（目标价上调）→ 做多；负值（目标价下调）→ 做空

## 特征工程建议

### 3.1 变化特征（主信号）

**F1 预期修正方向**：
- 定义：`rank(ts_mean(subtract(vec_avg(oth553_est_estvalue), vec_avg(oth553_est_preestvalue)), 5))`
- 逻辑：5 日平均预期修正方向，平滑事件流噪声
- 预处理：vec_avg 聚合 VECTOR → ts_mean(5) 平滑 → rank 标准化

**F2 评级修正方向**：
- 定义：`rank(ts_mean(subtract(vec_avg(oth553_recvalue), vec_avg(oth553_prerecvalue)), 5))`
- 逻辑：5 日平均评级修正方向
- 预处理：同上

**F3 目标价修正方向**：
- 定义：`rank(ts_mean(subtract(vec_avg(oth553_ptgvalue), vec_avg(oth553_preptgvalue)), 5))`
- 逻辑：5 日平均目标价修正方向
- 预处理：同上

### 3.4 交互特征（组合信号）

**F4 预期+评级双修正**：
- 定义：`rank(add(rank(F1), rank(F2)))`
- 逻辑：预期修正与评级修正同向时信号增强
- 收益来源：分析师预期变化（基本面预期改善）

**F5 预期修正×sales 修正**：
- 定义：`rank(add(rank(F1), rank(ts_mean(subtract(vec_avg(oth553_sal_estvalue), vec_avg(oth553_sal_preestvalue)), 5))))`
- 逻辑：盈利预期与销售预期同向时信号增强（盈利质量）
- 收益来源：分析师预期变化（盈利质量改善）

### 3.7 相对特征（归一化）

**F6 预期修正强度（zscore）**：
- 定义：`rank(ts_zscore(ts_mean(subtract(vec_avg(oth553_est_estvalue), vec_avg(oth553_est_preestvalue)), 5), 20))`
- 逻辑：20 日 zscore 归一化，捕捉预期修正的相对强度
- 预处理：ts_zscore(20) 归一化

### 3.8 本质特征（事件门控）

**F7 预期修正×returns 相关性**：
- 定义：`rank(ts_corr(ts_mean(subtract(vec_avg(oth553_est_estvalue), vec_avg(oth553_est_preestvalue)), 5), returns, 20))`
- 逻辑：预期修正与价格的相关性，捕捉市场对预期修正的反应强度
- 收益来源：分析师预期变化×市场反应

**F8 预期修正 sector 中性化**：
- 定义：`rank(group_neutralize(ts_mean(subtract(vec_avg(oth553_est_estvalue), vec_avg(oth553_est_preestvalue)), 5), sector))`
- 逻辑：sector 内中性化，去除行业beta，捕捉纯 alpha
- 收益来源：分析师预期变化（sector 内相对强弱）

**F9 预期修正事件门控**：
- 定义：`rank(if_else(greater(ts_mean(subtract(vec_avg(oth553_est_estvalue), vec_avg(oth553_est_preestvalue)), 5), 0), ts_mean(subtract(vec_avg(oth553_est_estvalue), vec_avg(oth553_est_preestvalue)), 5), 0))`
- 逻辑：只保留预期修正为正的持仓（事件门控）
- 收益来源：分析师预期上调（单向做多）

## 实现考量

**数据质量**：
- VECTOR 事件流覆盖率 0.48-0.75（中等），需 `vec_avg` 聚合
- 事件流稀疏性：部分股票可能长期无分析师覆盖，需 `ts_backfill(66)` 填洞

**CW 风险**：
- VECTOR 事件流天然有事件日集中风险（某天大量分析师同时修正预期）
- 防护：`rank()` 标准化 + `group_neutralize()` sector 中性化 + `if_else()` 事件门控

**与已有 ACTIVE alpha 的正交性**：
- 已有 ACTIVE：88lr21xo/A1lb2KpR（评级修正×SH 混合，ml_factor_proj + model170）
- other553 是不同数据集（分析师预期事件流 vs 评级修正+短周期对冲），预期 SELF 相关性 <0.4

## 进一步探索的关键问题

1. other553 与 analyst_consensus（300 字段 VECTOR）的差异：other553 是事件流，analyst_consensus 是快照，哪个更有效？
2. 预期修正方向在 KOR 是否有效（与 analyst10 revise_value 族天花板 0.67 对比）？
3. 事件门控（if_else）是否能有效防 CW 集中？
