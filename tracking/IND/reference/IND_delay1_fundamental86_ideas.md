# IND fundamental86 特征工程 Ideas

**Dataset**: fundamental86 (Stock Reports Plus)
**Region**: IND
**Delay**: 1
**Universe**: TOP500

## 数据集理解

fundamental86 为 Stock Reports Plus 综合评分数据集，7 个 MATRIX 字段全为 1-10 decile 评分：
- `fnd86_average_score`: 综合评分 (cov=0.97, alphas=2409 拥挤)
- `fnd86_earnings_score`: 盈利质量/修订/成长 (cov=0.76, alphas=1254)
- `fnd86_fundamental_score`: 基本面质量 (cov=0.97, alphas=793)
- `fnd86_insider_trading_score`: 内部人交易 (cov=0.00 无数据，排除)
- `fnd86_price_momentum_score`: 价格动量 (cov=0.97, alphas=1089)
- `fnd86_relative_valuation_score`: 相对估值 (cov=0.95, alphas=1029)
- `fnd86_risk_score`: 风险 profile (cov=0.98, alphas=825)

## 字段解构

- **评分本质**: 1-10 decile 整数评分，非连续值，天然适合 rank/quantile 处理
- **更新频率**: 月频/季频（分析师报告驱动），适合 ts_backfill(66) 填充
- **信号特性**: 高 persistent，低 turnover，但 decile 离散化可能损失信息

## 特征概念

### 1. 盈利-动量分歧 (Earnings-Momentum Disagreement)
- **机制**: 市场追逐价格动量，盈利评分反映基本面修订； gap 识别盈利支撑但价格未反应的股票
- **字段**: earnings_score, price_momentum_score
- **实现**: quantile(subtract(ts_backfill(earnings_score, 66), ts_backfill(price_momentum_score, 66)))
- **暴露**: quality
- **turnover**: medium (0.15-0.30)

### 2. 基本面变化-水平 (Fundamental Change-vs-Level)
- **机制**: 低水平基本面改善比高水平更有 runway；变化-水平差捕捉 recovery 信号
- **字段**: fundamental_score
- **实现**: ts_zscore(ts_delta(ts_backfill(fundamental_score, 66), 66), 126)
- **暴露**: growth
- **turnover**: medium

### 3. 廉价+安全 (Cheap-and-Safe)
- **机制**: 低估值需低风险 profile 配合，避免 value trap
- **字段**: relative_valuation_score, risk_score
- **实现**: quantile(multiply(ts_backfill(relative_valuation_score, 66), ts_backfill(risk_score, 66)))
- **暴露**: value
- **turnover**: low (<0.15)

### 4. 盈利质量残差 (Earnings Quality Residual)
- **机制**: 盈利评分与基本面评分差， isolates 盈利特定组件
- **字段**: earnings_score, fundamental_score
- **实现**: quantile(subtract(ts_backfill(earnings_score, 66), ts_backfill(fundamental_score, 66)))
- **暴露**: profitability
- **turnover**: medium

### 5. 动量稳定性 (Momentum Stability)
- **机制**: 动量评分变化的一致性（ts_ir）， stable positive drift 优于 spike
- **字段**: price_momentum_score
- **实现**: rank(ts_ir(ts_delta(ts_backfill(price_momentum_score, 66), 21), 66))
- **暴露**: momentum
- **turnover**: medium

### 6. 风险改善 (Risk Improvement)
- **机制**: 风险评分改善趋势， lowvol 暴露
- **字段**: risk_score
- **实现**: ts_zscore(ts_ir(ts_delta(ts_backfill(risk_score, 66), 66), 66), 126)
- **暴露**: lowvol
- **turnover**: low

### 7. 综合-价格分歧 (Composite-Price Divergence)
- **机制**: 综合评分 vs 价格动量， sentiment gap mean-reversion
- **字段**: average_score, price_momentum_score
- **实现**: quantile(subtract(ts_backfill(average_score, 66), ts_backfill(price_momentum_score, 66)))
- **暴露**: sentiment
- **turnover**: medium

### 8. 综合加速度 (Composite Acceleration)
- **机制**: 综合评分二阶差分， acceleration 优于 level/first difference
- **字段**: average_score
- **实现**: ts_zscore(ts_delta(ts_delta(ts_backfill(average_score, 66), 21), 21), 126)
- **暴露**: growth
- **turnover**: medium-high

## 预处理决策

- **ts_backfill(66)**: 所有字段月频更新， 66 天填充防断点
- **quantile/rank**: decile 评分天然适合截面 rank 处理
- **ts_zscore(126)**: 时间序列标准化窗口 126（半年）
- **ts_delta(21/66)**: 变化窗口 21（月）/66（季）

## 多样性评估

- **算子**: quantile(4), ts_zscore(2), rank(1), ts_ir(2), ts_delta(4), ts_backfill(7), subtract(3), multiply(1)
- **字段**: 6/7 字段使用（insider_trading_score 排除）
- **骨架**: single_field(3), dual_field(4), acceleration(1)
- **暴露**: quality, growth, value, profitability, momentum, lowvol, sentiment (7 类)

## 失败风险

- **decile 离散化**: 1-10 评分信息损失， 可能信号离散度不足
- **拥挤**: average_score alphas=2409 已高度拥挤， 需避开直接使用
- **turnover**: 月频更新天然低 turnover, 但 decile 跳变可能引发集中交易

## 建议

1. **优先测试概念 1/4/7**（earnings_score 相关）：历史 robust=1.12 突破， 但 IS 失败需修复
2. **避开 average_score 直接使用**：alphas=2409 高度拥挤， 仅用于加速度/分歧组合
3. **关注 turnover**：decile 评分月频更新， 天然低 turnover, 但需监控 CONCENTRATED_WEIGHT
4. **组合策略**：若单信号 IS 不足， 考虑 earnings_score × price_momentum_score 跨周期组合（KOR 成功模式）
