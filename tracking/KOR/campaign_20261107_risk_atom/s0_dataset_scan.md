# S0 · KOR Risk 数据集扫描（2026-11-07）

> 目标变更：Social Media → **Risk**。KOR risk 塔 **0/3 未点亮**，可挖。
> 禁区核对：禁混集合 = {PV, MODEL, OTHER, FUNDAMENTAL}；**RISK 在集合外**，可与任意集组两塔（限 5 个）。单集 ATOM 不占配额。

## 全部 7 个 risk 数据集
| id | 名称 | 字段 | cov | aC | uC | 判读 |
|---|---|---:|---:|---:|---:|---|
| risk59 | Securities Lending & Short Market Dynamics | 16 | 0.981 | 564 | 222 | **首选**：利用率/费率/DTC/挤压，经济轴最厚 |
| risk70 | Multi-Factor Model（MFM2） | 96 | 0.980 | 8018 | 1230 | **并列首选**：特异收益/特异风险/风格载荷 |
| risk68 | Forecast Data | 5 | 0.991 | 770 | 347 | 高价值：特异收益 + beta + 短波动 |
| risk88 | Other Multi-Factor Risk Models | 64 | 0.973 | 1418 | 495 | 次选：ASI 前缀，KOR 覆盖 0.967 |
| risk71 | Daily Specific Return Profiling | 7 | 0.666 | 349 | 152 | 低覆盖，备选 |
| risk72 | Specific return of extended factors | 5 | 0.625 | 402 | 164 | 低覆盖，备选 |
| risk60 | Securities Lending Insight | 5 | 1.000 | 211 | 83 | 与 risk59 同轴，跨集组合时用 |

## 机制优先序（A-2 收益来源声明见 s1 文件）
1. **特异收益反转**（risk68.residual_return / risk70.dsrt）：流动性提供者吸收特质性订单流，价格压力数日回吐
2. **融券约束溢价**（risk59.bid_rate / s3utilization）：借券成本高 = 卖空受限 = 高估持续 ⇒ 未来负收益
3. **空头挤压**（risk59.squeeze_risk）：拥挤空头被逼平 ⇒ 短期正收益
4. **特异波动异象**（risk70.resvol / srisk）：Ang et al. 2006 idio vol puzzle
5. **低 beta 异象**（risk68.beta）：Frazzini-Pedersen BAB

## C 位判据（初筛）
- 十一年覆盖：risk59/60/68/70/88 常年有数据；risk71/72 cov 0.62–0.67 需逐年复核
- 拥挤度：risk70 aC 8018 最挤 ⇒ 优先取 `dsrt`/`srisk`/`resvol`（风险量），避开纯风格载荷
