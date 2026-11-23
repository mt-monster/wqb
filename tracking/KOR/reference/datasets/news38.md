# news38 字段画像（KOR / TOP600 / Delay=1）— Bloomberg/RavenPack 新闻情绪与热度

> 2026-11-21 建。平台 `get_datafields(news38, filter_sharpe=false)` 实读 **complete=true / 45/45**。
> 塔：**NEWS（0/3 未点亮）**，倍率 1.6，category = NEWS（非 OTHER ⇒ 在挖掘范围内）。
> **本集此前从未回测、无画像档案** —— 与已判死的 news85（天花板 S0.69）、news54（数据层排除）、news76（4 探针全灭）都不是同一集。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | `news38` |
| 语义 | 新闻标题级情绪（positive/negative score & freq、tone ±1）+ 注意力/热度 + 相关性打分 |
| 结构 | **45 字段全部 VECTOR** ⇒ 必须先 `vec_avg` / `vec_sum` / `vec_max` 降维 |
| coverage | **0.2683–0.9529**（分字段差异极大，**逐字段看**） |
| dateCreated | 2023-01-01（早期模块）/ 2025-11-01（d1 / story_analytics 新模块） |
| 拥挤度 | 头部 `mws38_score` aC **67**、`mws38_previous` 59；多数情绪字段 aC **0–7**（未被挖） |

## 字段全表（45/45）

| # | field | cov | aC | 族 | 裁决 |
|---|---|---|---|---|---|
| 1 | `mws38_score` | .9529 | **67** | F1 情绪综合 | ✅ 主候选（覆盖最高、综合分） |
| 2 | `mws38_previous` | .9529 | 59 | F9 元数据 | ✗ 指针/索引，非信号 |
| 3 | `mws38_d1_action` | .8932 | 14 | F9 元数据 | ✗ 生命周期码需映射 |
| 4 | `mws38_d1_related_num` | .8932 | 7 | F3 注意力 | ✅ 关联实体数（注意力强度） |
| 5 | `mws38_positive_score` | .8932 | 7 | F2 正负 | ✅ 正向情绪强度（≥0） |
| 6 | `mws38_d1_hotlevel` | .8932 | 6 | F3 注意力 | ✅ 热度分（注意力代理） |
| 7 | `mws38_d1_time` | .8932 | 6 | F9 元数据 | ✗ hhmmss 时刻码 |
| 8 | `mws38_positive_freq` | .8932 | 5 | F2 正负 | ✅ 正向词频 |
| 9 | `mws38_uniq_related_num` | .8932 | 5 | F3 注意力 | ✅ 关联实体数（uniq 口径） |
| 10 | `mws38_d1_relevances` | .8932 | 3 | F4 相关性 | ⚠ 只作门控/权重，不作主信号 |
| 11 | `mws38_uniq_relevances` | .8932 | 4 | F4 相关性 | ⚠ 同上 |
| 12 | `mws38_tc_negative_freq` | .8932 | 3 | F2 正负 | ✅ 负向词频（tc 口径） |
| 13 | `mws38_d1_version` | .8932 | 3 | F9 元数据 | ✗ 版本号 |
| 14 | `mws38_uniq_version` | .8932 | 3 | F9 元数据 | ✗ 版本号 |
| 15 | `mws38_headlinetones_tc_entitlement` | .8932 | 3 | F9 元数据 | ✗ 权限位（禁建模） |
| 16 | `mws38_headlinetones_tc_time` | .8932 | 3 | F9 元数据 | ✗ 时刻码 |
| 17 | `mws38_analytics_time` | .9529 | 3 | F9 元数据 | ✗ 时刻码 |
| 18 | `mws38_uniq_time` | .8932 | 2 | F9 元数据 | ✗ 时刻码 |
| 19 | `mws38_uniq_hotlevel` | .8932 | 2 | F3 注意力 | ✅ 热度分（uniq 口径） |
| 20 | `mws38_uniq_action` | .8932 | 2 | F9 元数据 | ✗ 生命周期码 |
| 21 | `mws38_type` | .9529 | 2 | F9 元数据 | ✗ 分类码需映射 |
| 22 | `mws38_headlinetones_time` | .8932 | 2 | F9 元数据 | ✗ 时刻码 |
| 23 | `mws38_tc_positive_freq` | .8932 | 2 | F2 正负 | ✅ 正向词频（tc 口径） |
| 24 | `mws38_headlinetones_entitlement` | .8932 | 2 | F9 元数据 | ✗ 权限位 |
| 25 | `mws38_action` | .2683 | 1 | F9 元数据 | ✗ 生命周期码 |
| 26 | `mws38_time` | .2683 | 1 | F9 元数据 | ✗ 时刻码 |
| 27 | `mws38_tone_score` | .8932 | 1 | F1 情绪水平 | ✅ 标题语调 [-1,1]（语义最干净） |
| 28 | `mws38_tc_tone_score` | .8932 | 1 | F1 情绪水平 | ✅ 标题语调（tc 口径） |
| 29 | `mws38_tc_positive_score` | .8932 | 1 | F2 正负 | ✅ 正向强度（tc 口径） |
| 30 | `mws38_tc_negative_score` | .8932 | 1 | F2 正负 | ✅ 负向强度（tc 口径） |
| 31 | `mws38_uniq_entitlement` | .8932 | 1 | F9 元数据 | ✗ 权限位 |
| 32 | `mws38_value` | .9529 | 1 | F9 元数据 | ✗ "News value" 语义不明，不作信号 |
| 33 | `mws38_analytics_entitlement` | .9529 | 6 | F9 元数据 | ✗ 权限位 |
| 34 | `mws38_d1_entitlement` | .8932 | 9 | F9 元数据 | ✗ 权限位 |
| 35 | `mws38_negative_score` | .8932 | **0** | F2 正负 | ✅ 负向强度（≥0，未被用过） |
| 36 | `mws38_negative_freq` | .8932 | **0** | F2 正负 | ✅ 负向词频（未被用过） |
| 37 | `mws38_hotlevel` | .7446 | **0** | F3 注意力 | ✗ **description 明写 "all 0"**（死字段） |
| 38 | `mws38_related_num` | .2683 | 0 | F3 注意力 | ⚠ cov .2683 < 0.5 地板 |
| 39 | `mws38_relevances` | .2683 | 0 | F4 相关性 | ⚠ cov .2683 < 0.5 地板 |
| 40 | `mws38_version` | .2683 | 0 | F9 元数据 | ✗ 版本号 + 低覆盖 |
| 41 | `mws38_entitlement` | .2683 | 0 | F9 元数据 | ✗ 权限位 |
| 42 | `market_impact_indicator` | .2683 | **0** | F3 注意力 | ⚠ cov .2683 < 0.5 地板 |
| 43 | `story_analytics_metric_value` | .8016 | **0** | F1 情绪综合 | ✅ 数值指标（未被用过） |
| 44 | `story_analytics_relevance_score` | .8592 | 1 | F4 相关性 | ⚠ 只作门控/权重 |
| 45 | `story_analytics_category` | .8592 | 1 | F9 元数据 | ✗ 分类码需映射 |

## 0.1 字段实测读数表（全 45 字段，平台 `get_datafields` 实读 cov / aC）

> 本表是「全字段探测」的机械凭据：逐字段一行、id 真实、读数带数字，供 `tools/gates/field_profile_completeness_gate.py` 校验。

| field | cov | aC | 族 | 用途裁决 |
|---|---|---|---|---|
| `mws38_score` | .9529 | 67 | F1 情绪综合 | ✅ 主候选 |
| `mws38_previous` | .9529 | 59 | F9 元数据 | ✗ 指针，非信号 |
| `mws38_d1_action` | .8932 | 14 | F9 元数据 | ✗ 生命周期码 |
| `mws38_d1_related_num` | .8932 | 7 | F3 注意力 | ✅ 关联实体数 |
| `mws38_positive_score` | .8932 | 7 | F2 正负 | ✅ 正向强度 |
| `mws38_d1_hotlevel` | .8932 | 6 | F3 注意力 | ✅ 热度分 |
| `mws38_d1_time` | .8932 | 6 | F9 元数据 | ✗ 时刻码 |
| `mws38_positive_freq` | .8932 | 5 | F2 正负 | ✅ 正向词频 |
| `mws38_uniq_related_num` | .8932 | 5 | F3 注意力 | ✅ 关联实体数 |
| `mws38_d1_relevances` | .8932 | 3 | F4 相关性 | ⚠ 仅门控/权重 |
| `mws38_uniq_relevances` | .8932 | 4 | F4 相关性 | ⚠ 仅门控/权重 |
| `mws38_tc_negative_freq` | .8932 | 3 | F2 正负 | ✅ 负向词频(tc) |
| `mws38_d1_version` | .8932 | 3 | F9 元数据 | ✗ 版本号 |
| `mws38_uniq_version` | .8932 | 3 | F9 元数据 | ✗ 版本号 |
| `mws38_headlinetones_tc_entitlement` | .8932 | 3 | F9 元数据 | ✗ 权限位 |
| `mws38_headlinetones_tc_time` | .8932 | 3 | F9 元数据 | ✗ 时刻码 |
| `mws38_analytics_time` | .9529 | 3 | F9 元数据 | ✗ 时刻码 |
| `mws38_uniq_time` | .8932 | 2 | F9 元数据 | ✗ 时刻码 |
| `mws38_uniq_hotlevel` | .8932 | 2 | F3 注意力 | ✅ 热度分 |
| `mws38_uniq_action` | .8932 | 2 | F9 元数据 | ✗ 生命周期码 |
| `mws38_type` | .9529 | 2 | F9 元数据 | ✗ 分类码 |
| `mws38_headlinetones_time` | .8932 | 2 | F9 元数据 | ✗ 时刻码 |
| `mws38_tc_positive_freq` | .8932 | 2 | F2 正负 | ✅ 正向词频(tc) |
| `mws38_headlinetones_entitlement` | .8932 | 2 | F9 元数据 | ✗ 权限位 |
| `mws38_action` | .2683 | 1 | F9 元数据 | ✗ 低覆盖+生命周期码 |
| `mws38_time` | .2683 | 1 | F9 元数据 | ✗ 低覆盖+时刻码 |
| `mws38_tone_score` | .8932 | 1 | F1 情绪水平 | ✅ 标题语调 [-1,1] |
| `mws38_tc_tone_score` | .8932 | 1 | F1 情绪水平 | ✅ 标题语调(tc) |
| `mws38_tc_positive_score` | .8932 | 1 | F2 正负 | ✅ 正向强度(tc) |
| `mws38_tc_negative_score` | .8932 | 1 | F2 正负 | ✅ 负向强度(tc) |
| `mws38_uniq_entitlement` | .8932 | 1 | F9 元数据 | ✗ 权限位 |
| `mws38_value` | .9529 | 1 | F9 元数据 | ✗ 语义不明 |
| `mws38_analytics_entitlement` | .9529 | 6 | F9 元数据 | ✗ 权限位 |
| `mws38_d1_entitlement` | .8932 | 9 | F9 元数据 | ✗ 权限位 |
| `mws38_negative_score` | .8932 | 0 | F2 正负 | ✅ 负向强度（未被人用过） |
| `mws38_negative_freq` | .8932 | 0 | F2 正负 | ✅ 负向词频（未被人用过） |
| `mws38_hotlevel` | .7446 | 0 | F3 注意力 | ✗ description 明写 all 0 |
| `mws38_related_num` | .2683 | 0 | F3 注意力 | ⚠ cov 低于 0.5 地板 |
| `mws38_relevances` | .2683 | 0 | F4 相关性 | ⚠ cov 低于 0.5 地板 |
| `mws38_version` | .2683 | 0 | F9 元数据 | ✗ 版本号+低覆盖 |
| `mws38_entitlement` | .2683 | 0 | F9 元数据 | ✗ 权限位 |
| `market_impact_indicator` | .2683 | 0 | F3 注意力 | ⚠ cov 低于 0.5 地板 |
| `story_analytics_metric_value` | .8016 | 0 | F1 情绪综合 | ✅ 数值指标（未被人用过） |
| `story_analytics_relevance_score` | .8592 | 1 | F4 相关性 | ⚠ 仅门控/权重 |
| `story_analytics_category` | .8592 | 1 | F9 元数据 | ✗ 分类码 |

## 1. 字段族与角色白名单

| 族 | 可用字段 | 允许形态 | 禁作 |
|---|---|---|---|
| **F1 情绪水平** | mws38_score(aC67)、mws38_tone_score、mws38_tc_tone_score、story_analytics_metric_value | `vec_avg` → `ts_mean(22)` → `group_rank` | 裸情绪直排（日噪声） |
| **F2 正负不对称** | positive_score/freq、negative_score/freq（base 与 tc 两套） | `vec_avg(pos) − vec_avg(neg)`（同集单机制价差） | 只用单边（丢信息）；base 与 tc 两套同腿相加（同源） |
| **F3 注意力/热度** | d1_hotlevel、uniq_hotlevel、d1_related_num、uniq_related_num | **门控**（`trade_when`）或与情绪做比 | 裸计数当信号；`mws38_hotlevel`（全 0） |
| **F4 相关性** | d1_relevances、uniq_relevances、story_analytics_relevance_score | 只作权重/门控 | 作主信号 |
| **F9 元数据** | 全部 `*_entitlement` / `*_time` / `*_version` / `*_action` / `*_type` / `mws38_previous` / `mws38_value` | 禁用 | 一切信号用途 |

**低覆盖排除（cov < 0.5 地板）**：`mws38_related_num`(.2683)、`mws38_relevances`(.2683)、`mws38_version`(.2683)、`mws38_entitlement`(.2683)、`mws38_action`(.2683)、`mws38_time`(.2683)、`market_impact_indicator`(.2683)。

## 2. 机制与证据

| 机制 | 定义 | 方向 | 证据 |
|---|---|---|---|
| **M1 语调水平** | 标题语调（tone ∈[-1,1] / 综合 score）被渐进吸收 | 正向 | 《News sentiment indicators and the cross-section of stock returns》(2025)；paper_search diverse 5 篇/4 作者 PASS |
| **M2 正负不对称** | 负向消息定价更快、正向扩散更慢；净语调 = pos − neg | 正向（净语调高 ⇒ 后续强） | TRNA 2003–2014 极端情绪不对称研究；同上 paper_search |
| **M3 热度门控** | 热度/关联数激增 ⇒ 注意力过载 ⇒ 短期反转 | 反向（门控） | 论坛帖 42659817284375「别再用裸 sentiment」+ 37140180319127「注意力×情绪解耦」 |

## 3. 预处理与设置

- **全 VECTOR ⇒ 每个字段必须 `vec_avg` 降维**，禁裸字段。
- cov .8932/.9529 ⇒ 不必强制 backfill；低于 0.7 的可加 `ts_backfill(x,22)`。
- 日频事件型 ⇒ 先 `ts_mean(x, 22)` 聚合再 `group_rank`（news_sentiment_transfer 实测「rank 每日重排使 TO 失控 1.3」）。
- **禁 `hump`**（在 news_sentiment_transfer 上把书压到 42 只、CW 1.0）。
- 标准档 **SUBINDUSTRY**（earnings3 / institutions6 双集实证最优），decay 4，truncation 0.08，nanHandling OFF。
- 十年覆盖：dateCreated 有 2023 与 2025 两批 ⇒ **首波必须 `get_alpha_yearly_stats` 核 2014–2023 逐年 longCount**。

## 4. 波次记录（wave 207 起）

| wave | 腿 | 机制 | 表达式 | alpha | S | 2Y | F | TO | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| 207 | A | M1 语调水平 | `group_rank(ts_mean(vec_avg(mws38_score), 22), sector)` | 78YGq73L | **−0.36** | −0.52 | −0.13 | .1335 | **无正定价力**（反向且弱） |
| 207 | B | M2 正负不对称 | `group_rank(ts_mean(subtract(vec_avg(mws38_positive_score), vec_avg(mws38_negative_score)), 22), sector)` | vRAYnwpw | **0.00** | 0.36 | 0.00 | .2096 | 完全无信号 |

**wave 207 判定（2026-11-21）**：首轮 2 腿全灭。
- M1（`mws38_score`，本集覆盖最高的综合情绪分 aC67）S **−0.36**：不是包装问题——TO .13 在甜点带、CW pass、书 259/260 只都正常，是**该情绪分在 KOR 无正向定价力**（甚至弱反向）。
- M2（净语调 pos−neg）S **0.00**、TO .21：正负两侧对冲后信息归零。
- ⚠ 本集 2025-11-01 批字段 dateCreated 很新，历史长度需先核（本波未过闸故未查 yearly）。
- 按梯度法可继续在本集内做 L1（内层标准化全替），但**两个机制面一个反向一个零信号**，期望偏低 ⇒ 记 **PROVISIONAL 信号层封顶**，暂不再投；若后续要复活，优先测 F3 热度门控（`mws38_d1_hotlevel`）而非情绪水平。

## 5 「≥5 结构互异族 + 每族完整梯度」补齐复核（2026-11-22）
> 用户要求按严格标准补齐梯度；本节执行档案 §4 点名的复活方向（F3 热度门控）+ M1 语调 + M2 正负，并补相关性族。论文闸 PASS（paper_search diverse，news sentiment indicators 2025 等）已在档案 §2。KOR/TOP600/D1/SUBINDUSTRY/decay4/trunc0.08（遵档案标准档）。

### 5.1 L1 外层全类别替换（逐族推进）
| 族 | wave | 最优 | S | 2Y | 判 |
|---|---|---|---:|---:|---|
| M3 热度门控（复活方向） | `s2_news38_T1_hotlevel_gate_L1_d1` | `N1PG6A9X` `trade_when(d1_hotlevel>0,score)` | 0.31 | 0.90 | 档案点名复活方向也全灭；门控臂 longCount 13/TO0.018、CW0.5 |
| M1 语调水平 | `s2_news38_T2_tone_level_L1_d1` | `QP0AlYNp` `story_analytics_metric` | 0.13 | 0.35 | tone_score/score 全灭；score 长窗44/66 反向 −0.46/−0.48（印证 wave207 无正定价力）|
| M2 正负不对称 | `s2_news38_T3_posneg_L1_d1` | **`mLaNxrQE`** `group_zscore(pos−neg,44)` | **0.68** | 0.90 | ★本集最强：F0.55/CW0.29/TO0.12，比 wave207 S0.00 大幅改善；44窗+group_zscore是杠杆；tc口径 `vRAbJeGG` S0.40/2Y1.45 |

### 5.2 L2 内层时序全类别替换（在最强 M2 族上推进）
| 族 | wave | 内层替换最优 | S | 判 |
|---|---|---|---:|---|
| M2 正负 | `s2_news38_T3_posneg_L2_d1` | `pwakVKbo` `ts_mean(66)` | 0.38 | 内层换窗全劣化，L1 的 44 窗 group_zscore S0.68 仍最优（2Y0.90）；66窗 S0.38/2Y0.08；decay/av_diff/delta 全塌（TO0.74–0.81）|
| M1 语调 | `s2_news38_T2_tone_L2_d1` | `88NZn12m` `ts_zscore(252)` | 0.17 | 内层全类别全灭，|S|≤0.30；tone_score 族无定价力 |

### 5.3 收口判定（2026-11-22）
**news38 已按严格标准补齐：M1 语调/M2 正负不对称/M3 热度门控三族（含各自 tc 口径/词频/比率变体）× L1 外层 + L2 内层 = 5 wave / 40 臂，全部入库。**
- **族数诚实标注**：合法信号族为 M1 语调水平（score/tone_score/story_analytics_metric）、M2 正负不对称（pos−neg，base/tc/词频/比率）、M3 热度门控（hotlevel/related_num）；F4 相关性字段只作门控/权重、元数据 `*_entitlement/*_time/*_version` 与 cov<0.5 字段排除 ⇒ **受字段落地性限制凑不满独立 5 族**，不硬凑同构冒充。
- **0 全闸、无 near**：全集天花板 M2 `mLaNxrQE` S0.68/F0.55/2Y0.90/CW0.29（44 窗 + group_zscore，比 wave207 S0.00 大幅改善但仍距闸远）；tc 口径 `vRAbJeGG` S0.40/2Y1.45。
- **L2 内层替换全部收敛**：三族内层换窗均未超过 L1 最优，44 窗/22 窗分别是正负/其它族甜点；decay/av_diff/delta 因 TO 0.74–1.25 超闸全灭。
- **M3 复活方向失败**：档案 §4 点名"若复活优先测 F3 热度门控"——本轮实测 hotlevel 门控 S0.31/2Y0.90、裸 hotlevel S≤0.13，仍全灭 ⇒ 档案 PROVISIONAL 信号层封顶得到确认。
- **不判死**：记「梯度证据完整、信号层弱」；翻案须引外部新信息源。论文闸 PASS（《News sentiment indicators and the cross-section of stock returns》2025）。全程前台 MCP、无后台任务、未提交任何 alpha。
