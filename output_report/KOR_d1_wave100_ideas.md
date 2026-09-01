# KOR wave100 特征工程 ideas — pv106 + risk88

> S2 合规文档（source=skill）。wave97-99 analyst10 revise_value 族三波判死（KOR-ANL10-REVISE-VALUE-CEILING），wave100 转向未点亮 PriceVolume（pv106 交易成本/滑点）+ Risk（risk88 风险因子载荷）双数据集，经济机制正交。

## 1. 数据集理解

### pv106（交易成本/滑点，29 字段 MATRIX，cov 1.0，29 alpha 极低拥挤）
- **滑点指标**：`korean_market_slippage`（KOR 本地化滑点，3 alpha）、`transaction_cost_estimate`（综合成本，0 alpha）、`group_order_slippage`（组单滑点，2 alpha）
- **买卖成本**：`asia_trade_cost_buy/sell`（亚洲买卖成本，17/9 alpha）、`asia_trade_rate_buy/sell`（买卖费率，9/13 alpha）
- **spread 指标**：`pv106_wli_spread/bp`（198/153 alpha 高拥挤，排除）、`pv106_lastspreadbp`（30 分钟 spread bp，4 alpha 极低）
- **交易成本分布**：`transaction_cost_maximum/median/percentile_10`（34/25/20 alpha）
- **KOR 实证**：wave96 intraday_pv_feats 判死的是盘口流动性比率族（bid/ask/vwap），pv106 是交易成本/滑点族——经济机制不同（交易成本=执行摩擦，非盘口形态）

### risk88（多因子模型风险载荷，64 字段 MATRIX，cov 0.97，64 alpha 低拥挤）
- **风格因子载荷**：`ri_beta`（35 alpha）、`ri_leverage`（25 alpha）、`ri_nonlsize`（22 alpha）、`ri_size`（48 alpha）、`ri_growth`（61 alpha）、`ri_momentum`（39 alpha）、`ri_divyield`（52 alpha）、`ri_volatility`（77 alpha）
- **特质风险**：`srisk`（78 alpha）、`dsrt`（241 alpha 高拥挤，排除）
- **行业因子载荷**：`ind_*`（3-37 alpha 极低拥挤，40+ 行业）
- **KOR 实证**：risk59 判死的是 squeeze_risk/short_momentum 借贷卖空族，risk88 是多因子模型风险载荷族——经济机制不同（因子敞口 vs 借贷压力）

## 2. 字段解构

| 字段 | 测什么 | 为什么有意义 | 方向 |
|---|---|---|---|
| korean_market_slippage | KOR 本地化滑点 | 低流动性股票滑点高=交易摩擦大 | 高=看空 |
| transaction_cost_estimate | 综合交易成本 | 成本高=流动性差+市场影响大 | 高=看空 |
| asia_trade_cost_buy | 亚洲买入成本 | 买方压力大=需求旺盛 | 高=看多 |
| pv106_lastspreadbp | 30 分钟 spread(bp) | 盘口流动性，窄 spread=流动性好 | 低=看多 |
| rsk88_mfm_ase1_ri_beta | Beta 因子载荷 | 低 beta 异象（低风险溢价） | 低=看多 |
| rsk88_mfm_ase1_ri_leverage | 杠杆因子载荷 | 高杠杆=财务风险 | 低=看多 |
| rsk88_mfm_ase1_ri_nonlsize | 非线性市值因子 | 小市值溢价非线性部分 | 高=看多 |
| rsk88_mfm_ase1_srisk | 特质风险 | 低特质风险=质量溢价 | 低=看多 |

## 3. 候选池（8 条，1-2 字段/条，骨架多样性满足闸6）

| # | 表达式 | 数据集 | 骨架 | 经济机制 |
|---|---|---|---|---|
| 1 | multiply(rank(korean_market_slippage), -1) | pv106 | multiply 取反 | KOR 滑点反向（低滑点=流动性好看多） |
| 2 | multiply(rank(transaction_cost_estimate), -1) | pv106 | multiply 取反 | 交易成本反向（低成本=流动性好看多） |
| 3 | rank(asia_trade_cost_buy) | pv106 | rank | 买入成本（买方需求旺盛看多） |
| 4 | multiply(rank(pv106_lastspreadbp), -1) | pv106 | multiply 取反 | 窄 spread 反向（流动性好看多） |
| 5 | multiply(rank(rsk88_mfm_ase1_ri_beta), -1) | risk88 | multiply 取反 | 低 beta 异象（低风险溢价看多） |
| 6 | multiply(rank(rsk88_mfm_ase1_ri_leverage), -1) | risk88 | multiply 取反 | 低杠杆（财务稳健看多） |
| 7 | rank(rsk88_mfm_ase1_ri_nonlsize) | risk88 | rank | 非线性市值（小市值溢价看多） |
| 8 | multiply(rank(rsk88_mfm_ase1_srisk), -1) | risk88 | multiply 取反 | 低特质风险（质量溢价看多） |

## 4. 实现考量
- 全部 MATRIX 字段：直接 rank/multiply，无 VECTOR 包裹需求
- 滑点/成本类信号：慢变（交易成本日间变化小），decay=4 天然低换手
- 风险因子载荷：日频更新，截面 rank 消除量纲
- 多样性：rank/multiply 2 种骨架；2 数据集；字段互异；pv106 4 条 + risk88 4 条均衡

## 5. 风险与后续
- **pv106 高拥挤字段排除**：pv106_wli_spread/bp（198/153 alpha）已排除，选低拥挤变体
- **risk88 高拥挤字段排除**：dsrt（241 alpha）/ri_value（209 alpha）已排除
- **KOR 动量判死**：ri_momentum 不用（KOR-MOMENTUM-DEAD）
- 若 pv106 滑点族有效：Mode B 组合 asia_trade_cost 买卖双侧
- 若 risk88 因子载荷有效：Mode B 组合多因子（beta+leverage+size）

## 6. 建议
- **pv106 与 wave96 intraday_pv_feats 区别**：pv106 是交易成本/滑点（执行摩擦），intraday_pv_feats 是盘口流动性比率（bid/ask/vwap 形态）——经济机制不同，不构成同族重复
- **risk88 与 wave96 risk59 区别**：risk88 是多因子模型风险载荷（因子敞口），risk59 是借贷卖空压力（squeeze_risk/short_momentum）——经济机制不同
- **PROD 检查**：S4 必须查 prod_correlation，pv106/risk88 为新族无已知饱和风险
- **辅助信号配比**：pv106 4 条（交易成本主信号）+ risk88 4 条（风险因子辅助信号），跨数据集相关性 < 0.4（交易成本 vs 风险敞口正交）
