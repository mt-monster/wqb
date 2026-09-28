# EUR D1 news46：聚合新闻的预期与语气差异

## 字段
字段均来自本轮 EUR / TOPCS1600 / D1 的平台字段扫描，具体绑定列于各 Concept 的 Fields 行；字段白名单及类型记录在 s1_news46_d1。

## 特征
按可证伪经济机制设计；主信号、分母和事件门控的角色由各 Mechanism 描述限定。只保留 GEM 实现的概念原式，自动添加的同字段模板变体不纳入本轮回测。

## 建议
以下 Implementation Example 是概念实现契约。先经过 GEM 生成、语法/类型/画像预检，再进行有限首批验证；未达到资格线不得开展参数优化。


**Dataset**: news46
**Region**: EUR
**Delay**: 1

范围 EUR TOPCS1600 D1，REGULAR。来自实时 S1 30 字段与现有 WebDataScope 包；本次只用已匹配的 MATRIX 聚合字段。禁止 VECTOR、编号、时间、PV/MODEL、加权相加。
先验仅继承 win 的“两个经济量的排序差和条件分组”，不复用饱和字段。低频画像统一用 252 日回填/变化窗口；这是体检约束，不做参数寻优。sum 字段必须事件门控。每项绑定下述具体字段，禁止模糊后缀替换。

**Concept**: Novel information with restrained tone
**Mechanism**: New information that has not yet generated strong positive tone may diffuse slowly; novel stories with already euphoric tone have less surprise left.
**Fields**: mws46_ravenpack_mean_ens, mws46_ravenpack_mean_ess.
**Implementation Example**: `subtract(rank(ts_backfill({mws46_ravenpack_mean_ens},252)),rank(ts_backfill({mws46_ravenpack_mean_ess},252)))`

**Concept**: Attention-adjusted composite tone
**Mechanism**: Compare composite sentiment against how central the entity is; tone that exceeds prominence is an entity-specific surprise instead of generic coverage.
**Fields**: mws46_ravenpack_mean_ssc, mws46_ravenpack_mean_relevance.
**Implementation Example**: `subtract(rank(ts_backfill({mws46_ravenpack_mean_ssc},252)),rank(ts_backfill({mws46_ravenpack_mean_relevance},252)))`

**Concept**: Projected impact versus realized language
**Mechanism**: Impact projection minus composite tone is a disagreement between importance and direction, translating the historical surprise-residual mechanism to new news fields.
**Fields**: mws46_ravenpack_mean_nip, mws46_ravenpack_mean_ssc.
**Implementation Example**: `subtract(rank(ts_backfill({mws46_ravenpack_mean_nip},252)),rank(ts_backfill({mws46_ravenpack_mean_ssc},252)))`

**Concept**: Novelty revision
**Mechanism**: A persistent rise in novelty against its own prior year identifies a new information regime; use one signal source and no weighted blend.
**Fields**: mws46_ravenpack_mean_ens.
**Implementation Example**: `rank(ts_delta(ts_backfill({mws46_ravenpack_mean_ens},252),252))`

**Concept**: Composite tone regime revision
**Mechanism**: The annual change in composite tone tests slow incorporation of corporate news; the direction is a predeclared continuation hypothesis.
**Fields**: mws46_ravenpack_mean_ssc.
**Implementation Example**: `rank(ts_delta(ts_backfill({mws46_ravenpack_mean_ssc},252),252))`

**Concept**: Sentiment intensity per relevant coverage
**Mechanism**: Normalize aggregate sentiment by aggregate relevance only when relevant coverage exists, separating information tone from amount of attention.
**Fields**: mws46_ravenpack_sum_ess, mws46_ravenpack_sum_relevance.
**Implementation Example**: `trade_when(greater({mws46_ravenpack_sum_relevance},0),rank(divide({mws46_ravenpack_sum_ess},{mws46_ravenpack_sum_relevance})),-1)`

**Concept**: Novelty intensity per relevant coverage
**Mechanism**: Newly arriving information per unit of entity-relevant coverage detects underrecognized corporate events; update positions only on observed relevant events.
**Fields**: mws46_ravenpack_sum_ens, mws46_ravenpack_sum_relevance.
**Implementation Example**: `trade_when(greater({mws46_ravenpack_sum_relevance},0),rank(divide({mws46_ravenpack_sum_ens},{mws46_ravenpack_sum_relevance})),-1)`

**Concept**: Composite directional intensity per projected impact
**Mechanism**: Composite tone scaled by projected impact distinguishes direction from event magnitude. Positive impact guards the ratio and event updates.
**Fields**: mws46_ravenpack_sum_ssc, mws46_ravenpack_sum_nip.
**Implementation Example**: `trade_when(greater({mws46_ravenpack_sum_nip},0),rank(divide({mws46_ravenpack_sum_ssc},{mws46_ravenpack_sum_nip})),-1)`
