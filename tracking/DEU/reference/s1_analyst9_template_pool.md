# analyst9 模板池（修正广度分歧）—— DEU/TOP500/D1 —— 2026-11-03

**数据集**：analyst9（anl9_*，51 VECTOR 字段，consensus + 修正广度 numup/numdn/numanalysts 双口径 daily_*/s_* + unfiltered 过滤族）。
**塔**：ANALYST 单塔（单数据集 ATOM）；不触 PV/MODEL/OTHER 禁令，trio×非trio 配额不占用。
**画像**：s1_analyst44_analyst9_profile.md。

## 机制取证（模板前查，硬约束）
- **论文1**（Finexus，1995–2024 跨市场）：EPS 预测修正 3 个月滚动加权「revision score」多空价差 欧洲 4.6%/年、美国 5.2%、日本 3.1%（1% 显著，30bp 成本后仍存）；机制=低反应+扩散；**方向先验：上调→正**。
- **论文2**（values-project）：**成簇同向修正**移动共识；「修正比财报本身更重要」；加/减速是动量算法猎物；**高分歧→财报后波动大**（分歧=负向条件先验）。
- **论坛3 帖**：① 上调预期次数计数因子（anl4_basicconafv110_pu，vec 聚合）；② **DEU 实战帖**：「别问谁被上调最多，要问同一行业里谁比同行被上调得狠」= group_rank 组内归一直接印证；③ 修正广度=盈利动能横截面代理（17 票机构分歧因子同向）。

## 模板池（12 条，结构互异：水平/一阶/二阶/比率/乘积/门控/事件计数/反向六轴打散）

| # | 名称 | 骨架 | 机制箱 | 表达式 | 先验方向 |
|---|---|---|---|---|---|
| T1 | 净额水平 | group_rank(subtract) | 净广度 | `group_rank(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), industry)` | +（上调→正） |
| T2 | 净额动量 22 | ts_delta | 净广度 | `group_rank(ts_delta(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), 22), industry)` | + |
| T3 | 上调占比 | 比率（除零保护 x+0.01x） | 比率 | `group_rank(divide(vec_sum(anl9_s_numup), add(add(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), multiply(0.01, add(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn))))), industry)` | + |
| T4 | 有效覆盖占比 | 比率 | 覆盖 | `group_rank(divide(vec_sum(anl9_s_numanalysts), add(vec_sum(anl9_s_numanalystall), multiply(0.01, vec_sum(anl9_s_numanalystall)))), industry)` | +（覆盖广度） |
| T5 | 高覆盖日净额动量 | trade_when 门控 | 覆盖×净广度 | `trade_when(greater(vec_sum(anl9_s_numanalysts), ts_mean(vec_sum(anl9_s_numanalysts), 252)), group_rank(ts_delta(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), 22), industry), 0)` | + |
| T6 | 双窗一致性 | multiply(rank,rank) | 净广度 | `group_rank(multiply(rank(ts_delta(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), 252)), rank(ts_delta(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), 66))), industry)` | +（other47 T3 骨架迁移） |
| T7 | 上调过滤缺口 | 比率 | 噪声/过滤 | `group_rank(divide(subtract(vec_sum(anl9_daily_numupunfiltered), vec_sum(anl9_daily_numup)), add(vec_sum(anl9_daily_numupunfiltered), multiply(0.01, vec_sum(anl9_daily_numupunfiltered)))), industry)` | ±探针 |
| T8 | 僵持占比反向 | subtract(0,·) 反向 | 比率 | `subtract(0, group_rank(divide(vec_sum(anl9_s_numnochg), add(vec_sum(anl9_s_numanalystall), multiply(0.01, vec_sum(anl9_s_numanalystall)))), industry))` | +（分歧→负，论文2） |
| T9 | EPS 共识值动量 | ts_delta(值) | 共识值 | `group_rank(ts_delta(vec_avg(eps_consensus_estimate_value), 66), industry)` | + |
| T10 | 上调胜出日数 | ts_sum(greater) 事件计数 | 事件计数 | `group_rank(ts_sum(greater(vec_sum(anl9_daily_numup), vec_sum(anl9_daily_numdn)), 22), industry)` | +（成簇持续，论文2） |
| T11 | 净额波动率反向 | ts_std_dev 二阶矩反向 | 净广度不稳定 | `subtract(0, group_rank(ts_std_dev(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), 66), industry))` | +（波动=分歧→负） |
| T12 | 净额加速度 | 二阶差分（同字段双周期价差合规） | 净广度 | `group_rank(subtract(ts_delta(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), 22), ts_delta(subtract(vec_sum(anl9_s_numup), vec_sum(anl9_s_numdn)), 66)), industry)` | ±（other47 教训：突刺=负则此为−） |

**多样性审计**：骨架 8 种（水平/一阶差分/二阶差分/比率×3/乘积/门控/事件计数/波动率）；机制箱 5 个（净广度 6、比率 2、覆盖 2、噪声 1、共识值 1）；聚合 vec_sum/vec_avg 2 种；反号件 T8/T11 已内置。12 条同数据集同塔，无 add 混信号（subtract 均为同机制净额/同字段价差，合规）。
**量纲**：numup/numdn 同为计数 → subtract 安全；比率分母一律 x+0.01x 除零保护（单字段安全型）；eps_consensus_estimate_value 为 VECTOR 已 vec_avg。
**水平型纪律**：numup/numdn/numnochg 是水平/事件型 → 一律 group_rank(raw,g)，无逐股 ts_rank/ts_zscore 归一（insider 灭活教训）。
**克隆预警**：与 shrt3 提交篮（pwdl6ov6 估计修正 change-ratio 家族）**不同形态**（广度计数 vs change-ratio），prod 家族撞车风险低；anl44 的 change-ratio 形态禁用。

## 收批判据（预锁）
任一 |S|≥1.58 ⇒ 破闸流程（2Y/prod/self/fRA+逐年覆盖）；最高 ∈[0.8,1.58) ⇒ 赢单杠杆一轮（含反号变体）；最高 <0.8 ⇒ 判「广度机制弱」收口。逐年覆盖必查（leading-gap 口径待裁定）。反号变体：主候选 |S|≥0.6 时随批补 subtract(0,·)。
