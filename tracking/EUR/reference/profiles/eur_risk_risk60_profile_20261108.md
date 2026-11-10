# EUR × risk60 字段画像（2026-11-08）

> 平台目录：5/5 字段全量（complete=true，全部 VECTOR，需 vec_* 聚合）
> 塔位：RISK(×1.0，本季 2/3 未点亮，差 1 颗点亮)；拥挤度：rsk60_last/offer uC 222–252（热），crowding uC 71（中）

## 一、字段清单

| 字段 | cov | 语义 | 适用性 |
|---|---|---|---|
| rsk60_offer | 0.8168 | 复合借券费率（年化，空头支付） | **主读数候选**：高费率=高做空需求=负信号（reverse） |
| rsk60_last | 0.8168 | 快照时点最新借券费率 | 与 offer 高重叠，备选 |
| lending_fee_bid_rate | 0.8168 | 多头出借收益率的复合费率 | 出借供给端，备选 |
| rsk60_crowding | 0.8168 | 做空拥挤日度符号指标（正=加空/负=回补） | **事件型读数**：做空动量，j2eRn9KQ 已用作卫星腿 |
| rsk60_datatime | 0.8168 | 快照时间戳 | 元数据，不作信号 |

## 二、实证与风险

- **sub 闸风险**：cov 0.8168 < 0.85 ⇒ 按覆盖判死口径"sub 闸结构性不可达"的边界线上；但 0.82 vs fundamental28 的 0.50 不同——借贷数据在大票覆盖更好，sub 宇宙（更小宇宙）内覆盖可能高于全宇宙，**必须实测 sub 闸而非直接判死**。
- j2eRn9KQ（qfl 主腿 + 0.5×rank(ts_mean(vec_avg(rsk60_crowding),5)) 卫星，TOP700/STATISTICAL）S2.14/F1.63/2Y2.13/sub1.8 全过 ⇒ **crowding 读数与强主腿组合后不破坏闸**。
- 文献先验：借券费率/做空兴趣 = 负收益预测（Rapach & Lou 2018 "Under-Performance of Short Sellers"；Diether, Lee, Werner 2009 借贷约束）。

## 三、结论

1. ATOM 主攻方向：reverse(rank(ts_mean(vec_avg(rsk60_offer), 22)))——高费率做空。**注意平台无 reverse(x) 的等价写法用 multiply(-1, x) 或 rank 逆序**。
2. 备选：crowding 动量读数 ts_sum(vec_avg(rsk60_crowding), 22)。
3. cov 0.8168 的 sub 闸是第一道生死闸，探针波先测 sub 比例。
