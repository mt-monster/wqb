# USA / order_book_imbalance / D1 / TOP3000 机制优先 ideas（wave84 重生成 v2）

**Dataset**: order_book_imbalance
**Region**: USA
**Delay**: 1


背景：历史 27 条过 S/F 候选全卡 LOW_SUB_UNIVERSE_SHARPE + LOW_2Y_SHARPE 双墙。救法 = 慢快结构交互（提 2Y）+ 行业/分桶内比较（提 sub）。禁止 count 占比型 ratio 骨架（上轮 8/8 超配已 FAIL）。所有字段 VECTOR，示例已 vec_avg 包裹；占位符已替换为真实字段名（validator 要求真实字段占位）。

> v2.1（2026-09-28）：概念 3/7 原用 `add(A,B)` 分母占比被闸5 `POISON:equal_weight_leg_add` 结构判定拦截（2/13），改为 `divide` 比率形态（占比的单调等价，不引入加权拼腿）并经 GEM 重生成。

**Concept**: 收盘竞价失衡过度反应反转：竞价 order imbalance 过大 → 隔日过度反应 → 反向修正
- **Implementation Example**: `scale(-rank(group_rank(ts_decay_linear(vec_avg({auction_order_imbalance_pct_adv}), 5), subindustry)))`
- **Rationale**: 收盘竞价失衡反映被动方被迫成交，隔日价格过度延伸后回归（auction imbalance 过度反应机制）；候选主字段 auction_order_imbalance_pct_adv

**Concept**: 耐心溢价价差：耐心挂单者（挂单久后成交）知情 vs 急躁撤单者噪声，两者差是耐心溢价
- **Implementation Example**: `group_rank(subtract(rank(ts_mean(vec_avg({avg_rest_time_bid_filled_lvl1}), 22)), rank(ts_mean(vec_avg(avg_rest_time_bid_cancelled_lvl1), 22))), subindustry)`
- **Rationale**: 挂单耐心度是知情程度代理（耐心订单信息含量高）；22 日慢窗提 2Y 稳健性；候选主字段 avg_rest_time_bid_filled_lvl1

**Concept**: 暗池知情迁移：暗池/显示成交相对占比趋势上升 → 知情流聚集 → 中期延续
- **Implementation Example**: `group_rank(ts_mean(divide(vec_avg({dark_trade_volume}), vec_avg(lit_trade_volume)), 22), subindustry)`
- **Rationale**: 知情交易者倾向非显示场所执行以减冲击；dark/lit 相对占比（22 日均）是 dark_share=dark/(dark+lit) 的单调等价、中期知情流代理，慢结构救 2Y；候选主字段 dark_trade_volume

**Concept**: 深度斜率：五档深度/一档深度比 → 订单簿形状（薄顶厚尾=做市让价意愿高）→ 冲击成本低
- **Implementation Example**: `group_rank(ts_mean(divide(vec_avg({twa_notional_bid_5_levels}), vec_avg(twa_notional_bid_1_level)), 22), bucket(rank(vec_avg(twa_share_count_bid_1_level)), range="0,1,0.2"))`
- **Rationale**: 深度形状刻画流动性供给弹性；流动性分桶内比较（bucket）使信号在小票内也可比，救 sub-universe；候选主字段 twa_notional_bid_5_levels

**Concept**: 冲击系数反转：高价格冲击系数股短期被过度定价 → 反向回归
- **Implementation Example**: `scale(-rank(ts_mean(vec_avg({trade_market_impact_coefficient}), 22)))`
- **Rationale**: 价格冲击大的股票短期定价含流动性溢价泡沫，均值回归（microstructure 冲击回归）；候选主字段 trade_market_impact_coefficient

**Concept**: 买卖成交概率差：买盘成交概率显著高于卖盘 → 单边买入压力未消化 → 短期延续
- **Implementation Example**: `group_rank(ts_mean(subtract(vec_avg({fill_prob_bid_lvl1}), vec_avg(fill_prob_ask_lvl1)), 22), subindustry)`
- **Rationale**: 两侧 60 秒成交概率差度量单边压力强度；候选主字段 fill_prob_bid_lvl1

**Concept**: 失衡极值日的耐心价差门控：仅在竞价失衡极值日启用耐心信号（事件条件化降噪）
- **Implementation Example**: `trade_when(greater(rank(vec_avg(auction_order_imbalance_pct_adv)), 0.7), group_rank(subtract(rank(vec_avg({avg_rest_time_bid_filled_lvl1})), rank(ts_mean(vec_avg(avg_rest_time_bid_cancelled_lvl1), 22))), subindustry), less(rank(vec_avg(auction_order_imbalance_pct_adv)), 0.3))`
- **Rationale**: 条件腿（auction 失衡极值）是辅助事件轴，主信号是耐心价差；门控去噪提升 2Y；候选主字段 avg_rest_time_bid_filled_lvl1

**Concept**: 可寻址流动性占比趋势：bilateral/nonaddressable 相对占比上升 → 做市参与加深 → alpha 稳定性提升
- **Implementation Example**: `group_rank(ts_delta(ts_mean(divide(vec_avg({bilateral_trade_volume}), vec_avg(nonaddressable_trade_volume)), 22), 66), subindustry)`
- **Rationale**: 流动性构成变化（bilateral vs nonaddressable）反映做市行为 regime；相对占比（share 的单调等价）的 66 日趋势变化捕获慢信号救 2Y；候选主字段 bilateral_trade_volume

**Concept**: 失衡趋势反转（ts_corr 共振腿）：盘口失衡水平与失衡变化共振过高 → 均值回归
- **Implementation Example**: `scale(-rank(ts_corr(vec_avg({ask_trade_imbalance_all_levels}), ts_delta(vec_avg({ask_trade_imbalance_all_levels}), 5), 22)))`
- **Rationale**: 失衡水平与其自身变化高度共振时是拥挤失衡，回归概率高（共振腿=单一价差信号，非加权拼腿）；候选主字段 ask_trade_imbalance_all_levels

**Concept**: 深度不对称：ask 侧深度远大于 bid 侧 → 卖压堆积 → 反向（供给侧过量）
- **Implementation Example**: `scale(-rank(group_rank(subtract(rank(ts_mean(vec_avg(twa_notional_ask_30bps), 22)), rank(ts_mean(vec_avg({twa_notional_bid_30bps}), 22))), subindustry)))`
- **Rationale**: 订单簿供给侧不对称预示价格向下消化；候选主字段 twa_notional_bid_30bps

生成约束：窗口只用 5/22/66/252/504；反向 scale(-rank())；禁止加权混合（权重参数/0.4+0.6 式）；禁用幽灵算子（sigmoid/ts_entropy/ts_skewness/ts_decay_exp_window/ts_percentage/group_median 等）；骨架覆盖比值/价差/条件/趋势/共振/分桶多链；≥3 条含 22+ 慢腿、≥2 条含 group/bucket。