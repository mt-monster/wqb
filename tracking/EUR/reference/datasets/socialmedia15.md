# socialmedia15 · EUR / TOP2500 / D1 字段画像（2026-11-22 全字段普查）

> 类型 VECTOR · 45/45 字段全量拉取（complete=true）· category = **socialmedia**（×1.2，塔位 0/3）
> 采集：2026-11-22 · 两代字段：d1_ 系（2022-07 onboard）+ 2026-03 新系

## 0. 可用性分层（全字段）

| 层 | 字段 | αC | cov | 语义 |
|---|---|---:|---:|---|
| **d1 主力（唯一有历史量的层）** | d1_buzz(128)、d1_conflict(140)、d1_emotionvsfact(94)、d1_fundamentalstrength(87)、d1_timeurgency(77)、d1_sentiment(56)、d1_volatility(57)、d1_stress(65)、d1_trust(64)、d1_optimism(68)、d1_longshort(49)、d1_risk_score(51)、d1_pricedirection(34) | ≤140 | **0.256–0.299** | 财经媒体/社媒情绪 13 维 |
| 2026-03 新系（同语义去 d1_ 前缀） | sentiment(2)、buzz(9)、anger(1)、fear(2)、joy(1)、gloom(2)、innovation(1)、litigation(0)、violence(1)、mergers(6)、dividend_trend(8)、attrition(4)、debt(4)、earn(1)、analystrating(3)、conflict(6)、fundamentalstrength(8)、lovehate(2)、longshort(1)、longshortforecast(0)、managementchange(0)、managementtrust(1)、optimism(2)、price_score(1)、pricedirection(1)、risk_score(0)、stress(2)、timeurgency(1)、trust(1)、uncertainty(0)、volatility(1) | ≤9 | 0.371 | αC 全 ≤9，蓝海但无先验 |
| 事件类新字段 | mergers(6)、litigation(0)、managementchange(0) | ≤6 | 0.371 | M&A/诉讼/管理层变动强度 |

**画像结论**：socialmedia15 = 双层结构。d1_ 系 13 维有量（aC 34–140）但 cov 仅 0.26–0.30；新系 32 维 αC≤9 全蓝海、cov 0.371 略高。**cov <0.5 ⇒ 全字段先过覆盖闸再说**。与 socialmedia12（6 字段、aC2579 拥挤）互补。

## 1. 机制假设（按 04 编号）

- M1 情绪水平反转：`-ts_rank(d1_sentiment/buzz, 66)`（高关注→反转；与 news 关注度机制同源）
- M2 情绪异常：`ts_zscore(d1_emotionvsfact, 252)` 净情绪 z 值
- M3 分歧定价：`d1_conflict` 高分歧 → 期权式不确定性溢价（正向持有波动卖出方）
- M4 基本面信心：`d1_fundamentalstrength` 慢化 `ts_mean(66)`（会计信心是慢变量）
- M5 泡沫风险：`-d1_risk_score`（气泡风险高→做空倾向）
- M6 新系蓝海扫：mergers/dividend_trend/attrition 各 1 探针

## 2. 实测记录

### 批8（2026-11-22，新系 10 字段蓝海探针，multisim `4CewjQ2Do4ml8ZR6lfcGzf1`）

骨架：`group_rank(ts_zscore(ts_backfill(vec_avg(F), 252), 756), industry)`，TOP2500/SUBINDUSTRY/decay8

| 字段 | S | 2Y | sub | 判定 |
|---|---:|---:|---:|---|
| scl15_litigation | **0.38** | 0.86 | 0.36 | 唯一正向，弱 |
| dividend_trend_score | −0.19 | 0.28 | −0.04 | 负 |
| scl15_managementchange | −0.09 | 0.73 | 0.06 | 负 |
| scl15_analystrating | −0.25 | 0.16 | −0.19 | 负 |
| scl15_attrition_score | −0.28 | 0.16 | −0.19 | 负 |
| scl15_debt_score | −0.34 | −0.07 | −0.35 | 负 |
| scl15_earn_score | −0.35 | −0.00 | −0.32 | 负 |
| scl15_innovation | −0.42 | 0.10 | −0.41 | 负 |
| scl15_managementtrust | −0.43 | 0.22 | −0.52 | 负 |
| scl15_mergers | −0.54 | −0.67 | −0.52 | 负（最强反向） |

**结论**：新系 10 字段全灭（|S| ≤ 0.54，9/10 为负）。叠加 11-18 会话对 **d1_ 系**的十臂全灭（|S| ≤ 0.21）⇒ **socialmedia15 两代字段（13 + 32 = 45 字段）全部实测过 ⇒ SOCIALMEDIA 塔纯 ATOM 判死**。

**★ 归因（可迁移）**：这批字段的共同特征是 **cov 0.37 + 「事件计数/打分」语义稀疏** ⇒
① 覆盖率低 ⇒ 有效样本小、截面噪声大；
② 社媒/新闻类打分在 EUR 的定价效率高（已被生产池消化）。
⇒ **socialmedia 类在 EUR 应作「门控腿」（presence gating）而非「信号腿」**——这与 11-20 会话「门控优先」结论一致（scl12_buzz 作为弱腿反而出全闸件 `2r5NgWvY` prod 0.6785）。

## 3. 风险先验

- cov 0.26–0.37 在 sub-universe 闸上是结构性弱点（TOP800 有效股票更少）
- d1_conflict aC140 = 该集最高拥挤度字段，prod 先验中等
- 新系 αC≤9 ⇒ prod 友好，但无任何历史信号证据（纯 ATOM 蓝海）
