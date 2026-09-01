# KOR Wave 1 候选池设计
## 目标: 20 个可提交 REGULAR alpha
## 白名单数据集: analyst_base_ref, analyst_consensus, other78, fundamental93

### 设计原则
1. 慢变量(分析师共识) × 短周期(价格/成交量) 混合
2. 规避死路: 不用 value/quality 风格、不用评级修正族、不用图表形态
3. 每条表达式 1-2 个 catalog 字段
4. 重点方向: 分析师离散度、盈余意外、估计修正动量

### 候选表达式 (Wave 1 - 8条)

#### A. 分析师离散度族 (analyst_base_ref)
# A1: 离散度排名 + 价格反转 (慢×快混合)
rank(ts_mean(consensus_stddev_estimate, 22)) + scale(-rank(returns, 42)) * 0.35

# A2: 离散度变化率 (动量)
ts_zscore(consensus_stddev_estimate, 63) + scale(-rank(returns, 21)) * 0.3

# A3: 离散度/估计数量比值 (质量调整离散度)
rank(divide(consensus_stddev_estimate, add(num_estimates_consensus, 1))) + scale(-rank(returns, 42)) * 0.35

#### B. 盈余意外族 (analyst_base_ref)
# B1: 意外百分比动量 + 成交量确认
ts_zscore(consensus_surprise_percentage, 42) * rank(ts_mean(volume, 5))

# B2: 意外百分比 × 离散度交互 (高意外+低离散=强信号)
multiply(rank(consensus_surprise_percentage), subtract(1, rank(consensus_stddev_estimate)))

#### C. 估计修正族 (analyst_consensus)
# C1: EPS 估计数量变化 (关注度代理)
ts_zscore(estimate_count_current_period_eps_annual12_3, 63) + scale(-rank(returns, 21)) * 0.3

# C2: 实际/预期比值 (盈余质量)
rank(divide(actual_eps_value_annual12_3, consensus_mean_estimate)) + scale(-rank(returns, 42)) * 0.35

#### D. 事件标记族 (other78)
# D1: 初步结果标记 × 价格动量 (事件驱动)
multiply(oth78_preliminaryresultsflag, rank(ts_mean(returns, 5)))

### 设置参数
- region: KOR
- universe: TOP600
- delay: 1
- neutralization: STATISTICAL (默认) / SECTOR (备选)
- decay: 4-6
- truncation: 0.08
- testPeriod: P6Y
