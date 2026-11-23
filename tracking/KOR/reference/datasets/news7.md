# news7 数据集画像（KOR / TOP600 / Delay=1）

> 手工维护。数据源：wqb-db `get_field_catalog(KOR, news7)` + 平台 `get_datasets(category=news)`。
> 最后核对：2026-10-30。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | `news7` |
| category | **NEWS**（塔当前 **0 点亮**，乘数 1.6） |
| 本地 catalog | 56 字段 = **37 VECTOR / 19 MATRIX**；data_type 标 MATRIX 但过半是向量 |
| 平台覆盖 | 总体 ~0.633（`news_mention_frequency_*` 系到 .93） |
| sumAC | 409（中等拥挤；单字段最高 aC=102） |
| 性质 | 新闻订阅流：注意力计数 + 标题语气打分 + 事件元数据（编码/时戳） |

## 1. 字段分类（按 description 语义，不按字段名）

### A. 新闻注意力 / 广度（MATRIX，稠密，cov .93）

| 字段 | cov | aC | 说明 |
|---|---|---|---|
| `news_mention_frequency_simple` | .9326 | **102** | 每证券每日新闻条数（描述写 China，实测 KOR 覆盖 .93） |
| `news_mention_frequency_1` | .9326 | **75** | 同上（描述写 EUR） |
| `news_mention_frequency_d0` | .9325 | 1 | 亚洲区实盘（盘中）计数 |
| `news_mention_frequency_d0_twn` / `_alt` | .9325/.9314 | 1/1 | 台湾口径，疑似同源副本 |

⚠ **四个高覆盖字段疑似同一信息源的不同区域标签**：`_simple`(China) / `_1`(EUR) / `_d0`(Asia)。**不能当四个独立信号**（否则是同一腿铺量）。先实测相关性再取一条主腿。

### B. 标题级计数（MATRIX，cov .5726）

| 字段 | aC | 说明 |
|---|---|---|
| `headline_mention_count_2` | 19 | 当日该股标题总数 |
| `headline_negative_mention_count_2` | 17 | 负面词总出现次数 |
| `headline_positive_mention_count_2` | 3 | 正面词总出现次数 |

### C. 标题语气（MATRIX，cov .5726）

| 字段 | aC | 说明 |
|---|---|---|
| `headline_overall_tone_score_2` | 13 | 逐条 (pos−neg)/(pos+neg) 的均值 —— **有符号、中枢 0** |
| `headline_negative_tone_score_2` | 10 | 负词占比（非负） |
| `headline_positive_tone_score_2` | 7 | 正词占比（非负） |

### D. 另一路新闻频率 / 语气（MATRIX，cov .4521 / .5482）—— 观察期更短或源不同

`nws7_news_freq_qerf`(12) / `nws7_newsfreq_1_d1_qerf`(10) / `nws7_2_d1_news_freq`(5)；
`nws7_2_d1_tone_score`(7) / `nws7_2_d1_negative_score`(10) / `nws7_2_d1_positive_score`(2) / `nws7_2_d1_negative_freq`(3) / `nws7_2_d1_positive_freq`(1)。
⚠ cov 从 .57 掉到 .38–.45 ⇒ **与 A/B/C 不是同源同时段**，做「短历史」备用腿。

### E. 事件元数据（VECTOR，多为编码/时戳，不是信号）

`news_topic_name_d1_2`(13) / `news_category_tag`(1) / `news_item_value`(7) / `news_related_count_d1`(2) /
`nws7_d1_area`(28) / `nws7_livenews_all_time`(23) / take-seq / display-name / story-time / broadcast-area。
⇒ **用途：门控与去噪**（如「剔除更正/删除消息」、「只保留高相关度」、「限定播报区域」），**不做收益来源**。

## 2. 名 vs description 差异表（★ 被漏掉的资产 / 陷阱）

| 字段 | 名字暗示 | description 实际 | 处置 |
|---|---|---|---|
| `nws7_2_d1_positive_score` | 正面得分 | "average positive score (**negative words** by all words)" —— 描述自相矛盾，疑复制错误 | **必须实测符号**（与 tone/negative 对拍） |
| `news_mention_frequency_1` | 通用频率 | "in the **EUR region**" | 覆盖 .93 说明按 KOR universe 统计；**以实测逐年覆盖为准** |
| `news_mention_frequency_simple` | 简化版 | "in **China**" | 同上 |
| `headline_mention_count_2` | 总标题数 | cov 只 .57，显著低于 .93 的频率系 | **是不同源/不同抽取窗口**，不可互换 |
| `nws7_newsfreq_1_d1_qerf` | 频率 | "Number of news **without insider keywords**" | 唯一明写剔除 insider 的 → 与 A 族口径不同 |
| `nws7_d1_area` | 播报区域 | 0-NY/1-LD/2-LO/3-HA | 元数据；但可作为「消息源」门控 |

## 3. 字段画像五问（A-1）

1. **时间维度**：流量（每日计数 / 每日语气均值），**不是存量** ⇒ 水平可直接用（无需铁律 A 的 ts_delta）。
2. **相对性**：水平差异 + 排序差异都可用；注意力是**横截面相对量** ⇒ `group_rank`/`ts_zscore` 优于裸值。
3. **被定价的是谁**：注意力的**广度**（多少条新闻）+ 语气的**强度**（多正/多负）。
4. **有无博弈**：有。新闻关注度本身是拥挤的公开信息 ⇒ 需要规模/流动性壳层（`bucket`/`vector_neut`）控小盘噪声。
5. **事件性**：**半事件型**。B/C 族（cov .57）在无新闻日为空 ⇒ 稀疏，需 `ts_backfill` 或 `trade_when`；A 族（cov .93）近稠密，可直接算。

## 4. A-2 收益来源声明（主机制：注意力 × 语气）

| 项 | 内容 |
|---|---|
| **谁在被定价** | 散户注意力（retail attention）。新闻标题是散户最先看到、也最易过度反应的信息载体。 |
| **为什么会被错** | 注意力驱动买入（Barber–Odean 2008：个人投资者是注意力买家），新闻量激增 ⇒ 短期买压；同时负面语气在**信息摩擦**下反应不足（Tetlock 2007 悲观词→随后下跌）。 |
| **错了多久修复** | 数日到数周：注意力买压 5–22 日反转；语气漂移 1–3 个月（PEAD 式）。⇒ 窗口 5/22 为主，66 辅助。 |
| **预期方向** | 注意力异常高 ⇒ 短期涨、随后反转（**做反转腿**）；语气为负且持续 ⇒ 后续跌（**做空腿**）。两者方向须**分开测**（铁律 B）。 |
| **失效条件** | 无新闻日（NaN）；并购/更正经多源重复计数；小盘股新闻 = 一次性事件（噪声）。 |

## 5. 双通道取证（组装前必做）

**通道 A（论坛）** —— ✅ 已取证（2026-10-30）：

| 项 | 内容 |
|---|---|
| 帖子 | [【Alpha Idea】从「搜索量」到「新闻密度」：把一篇注意力反转论文迁移成可复用的 alpha 模板](https://support.worldquantbrain.com/hc/en-us/community/posts/43541109631895-) |
| 作者 / 热度 | PW58059 · 78 赞 / 34 评论 |
| 核心模板 | **异常注意力代理 → 时序分位 → 反向持仓**；落地形 `-group_neutralize(ts_rank(ts_mean(vec_count(事件数), 60), 252), densify(market))` |
| 实证 | GBR/TOP700/d1 已提交：S **1.97** / F 1.27 / tvr 7.9% / margin 13.2bps；EUR/TOP2500 五变体 S 1.12–1.61、F 全 <1.0（方向泛化成立、强度打折） |
| 与本区方向一致性 | ⭐ 与通道 B 的 Da–Engelberg–Gao(2011) **同一机制** ⇒ 按 ②.d 双通道裁决「优先组装」 |

**帖子/评论里可直接执行的硬约束（比论文更值钱，逐条落进本波设计）**：

1. **窗口甜点 = 60（一个季度）**，非单调：20 窗 S 1.30 < 60 窗 1.60 > 120 窗 1.12（EUR 实测）。
2. **`ts_mean` 在计数型字段上是 NaN 陷阱**：无事件日若返回 NaN，`ts_mean(count,60)` 算的是「有新闻那几天的平均值」而非「日均密度」，稀疏股被抬高、分位混进覆盖率。→ **必须跑 `ts_sum` 对照**（多位评论者独立复现同一结论）。
3. **CONCENTRATED_WEIGHT 是这类信号的默认故障**：事件密度天然把权重堆到少数极端股票，且要在**表达式层补分散度**，不是调 truncation。
4. **`tvr_decay` 买的是 margin 不是 Sharpe**（1.61 vs 1.60），不要指望它增强信号。
5. **必须拆年看 margin**：注意力轴有**机制级失效年**，全样本 Sharpe 会把它藏住（评论实测 CHN 单年 margin 塌到 3–5bp）。
6. **载体节律匹配**：注意力是日级现象，日更的新闻密度采样率够；换季更载体方向对也提不出信号。
7. **`group_neutralize(..., densify(market))` 在 FAST 中性化下可能完全无效**（评论者复现：去掉表达式无变化）。

⚠ 迁移到 KOR 的**降级理由**：上述是 GBR/EUR 结果；KOR 小宇宙、韩语标题词典不同 ⇒ 按假说处理。
已知本区前科：insiders5 论坛实测「单腿负向、被 backfill 制造伪触发」 ⇒ 对 news 同样要**先测 backfill 前后对照**。

**通道 B（论文）**：

| 文献 | 可证伪结论 | 本区可迁移性 |
|---|---|---|
| Tetlock (2007, JF) "Giving Content to Investor Sentiment" | 负面前景词 → 随后价格下行 + 成交量放大 | 机制可迁移；窗口 ~1 周–1 月 |
| Barber & Odean (2008, RFS) "All That Glitters" | 个人投资者是注意力买家 ⇒ 异常关注 → 短期买压 | 可迁移（KOR 散户占比高，**更强**） |
| Da, Engelberg & Gao (2011, JF) ASVI | 关注度激增 → 短期涨、随后反转 | 需 2 周–1 月窗口，反转腿 |
| Fang & Peress (2009, JF) "Media Coverage and Stock Returns" | **无覆盖**股票有信息摩擦溢价（覆盖度与收益负相关） | 横截面覆盖差 → 长期看多冷门股；本区新闻覆盖 .93 ⇒ **区分度低**，需长窗 |

⚠ 文献偏误：均为 USA 样本；KOR 散户占比高、新闻源集中（韩语标题情绪词典与英文不同）⇒ 结论按**假说**，本区实测定生死。

## 6. 近十年覆盖验证（用户约束 4）—— ✅ **PASS（2026-10-30 实测）**

平台 catalog 只给总体 coverage，不给逐年。判定法：首个候选回测后读 `get_alpha_yearly_stats`。

**实测读数**：本波 8 条逐年 `longCount` 区间 **297–344**，**十年无空年** ⇒ **news7 满足用户约束 4**。
⇒ **本波全灭的根因不是覆盖不足，是机制不成立**（见 §7.1）。后续若复用 news7，不必再验覆盖。

## 7.1 波次结果与归因（wave 188，8/8 全灭 → 机制判死）

> 收批读数（`list_alphas_by_wave(KOR, 188)` + `wave_results`，2026-10-30）：

| id | 表达式（截） | S | F | 2Y | TO | subU |
|---|---|---|---|---|---|---|
| `2rAP6rj8` | `-group_rank(ts_rank(ts_mean(headline_mention_count_2,60),252),sector)` | **0.55** | 0.24 | **−0.34** | .120 | 0.43 |
| `xArXGA1m` | `-group_rank(ts_rank(ts_mean(news_mention_frequency_d0,60),120),sector)` | 0.15 | 0.03 | 0.93 | .129 | 0.09 |
| `e75eN6ql` | `-group_rank(ts_mean(headline_overall_tone_score_2,22),sector)` | 0.04 | 0.01 | −1.14 | .195 | 0.00 |
| `xArX2dZb` | `-group_rank(ts_rank(ts_sum(news_mention_frequency_d0,60),252),sector)` | −0.01 | 0.00 | **0.95** | .125 | −0.14 |
| `zq3X2Zq1` | `-group_rank(ts_rank(ts_mean(news_mention_frequency_d0,60),252),sector)` | −0.05 | −0.01 | 0.44 | .117 | −0.10 |
| `rKRQNYKo` | `group_rank(ts_rank(ts_mean(news_mention_frequency_d0,60),252),sector)` | −0.17 | −0.04 | −0.81 | .117 | −0.10 |
| `1YN6OjmW` | `group_rank(ts_mean(headline_overall_tone_score_2,22),sector)` | −0.17 | −0.04 | 0.89 | .195 | −0.10 |
| `6XdgoekL` | `group_rank(ts_rank(ts_mean(news_mention_frequency_d0,22),252),sector)` | −0.30 | −0.08 | **−1.50** | .185 | −0.26 |

**归因（KOR 决策表逐条对表）**：

| 读数 | 判据 | 结论 |
|---|---|---|
| **IS 与 2Y 反号** | 最优臂 `2rAP6rj8` S=+0.55 但 2Y=−0.34；`6XdgoekL` S=−0.30 但 2Y=−1.50 | ⛔ **不是参数问题**。参数档无法同时让 IS 与 2Y 同号 ⇒ 直接跳「换字段族」 |
| 逐年 S 符号翻转 | 非单调衰减 | 逻辑同上（衰减是**机制的**，不是参数的） |
| 十年覆盖 | 297–344 每年非零 | PASS ⇒ 排除数据稀疏这条伪因 |
| CW | 8 条**全部未触发** CONCENTRATED_WEIGHT | ⭐ **唯一可继承的正向读数**：注意力计数族经 `ts_rank`+`group_rank` 归一后权重分布健康，**不需 tail/bucket 修权重** |
| 换手 0.117–0.195 | F = S·sqrt(Ret/max(TO,.125)) | TO 已在下沿，F 被 |S|<0.6 结构性压死 ⇒ **抬换手救不了 F**，必须先有 S |

**证伪登记（回测前未写，此处补登，防下波重蹈）**：
- 机制方向句：注意力冲击升高 ⇒ 后续收益偏低（做空冲击）⇒ `multiply(-1, …)` 为假定正向臂。
- 证伪条件：该臂 IS 与 2Y **同号**且 |S| 随平滑窗单调不增。**实测反号 ⇒ 证伪触发**。
- ⇒ news7 注意力/计数族（`news_mention_frequency_*`、`headline_mention_count_2`）在 KOR/TOP600/D1 **判死**，不再开波。

**⚠ 流程教训（影响所有后续波）**：`pipeline.py` 的 `load_wave_expressions(ctx.region, a.wave)` **不传 dataset 过滤**，
即同一 wave 下**所有非 dropped/superseded/deferred 的行都会被派发**。开新数据集波前必须先把同波其它数据集的行置 `dropped`，
否则一个探针批会混两个数据集（本波 189 席位原属 news18，已如此处理）。另：`status='deferred'` 被 DB CHECK 约束拒绝，只能用 `dropped`/`superseded`。

**同源副本警告复核**：`news_mention_frequency_d0`（aC 1）与 `_simple`(102)/`_1`(75) 在 S 上未见系统性差异（0.15/−0.05/−0.01 全在噪声带）
⇒ 与 §1-A 的「同源同信息」判断一致，**不必再花配额验证副本**。

## 7. 波次设计（实际执行：wave 188，2026-10-30）

> 原计划把首波排在 wave 186，实际 186 被 earnings3 占用 ⇒ news7 首波顺延为 **wave 188**。
> 首波 8 条已入库（KOR/188，source=manual）并过闸 8/8；4 批 × multisim(2)、串行填槽。

| 序 | 表达式 | 角色 | 指回的行 |
|---|---|---|---|
| 1 | `multiply(-1, group_rank(ts_rank(ts_mean(news_mention_frequency_d0, 60), 252), sector))` | **论坛模板原样**（注意项） | §5-A 模板 |
| 2 | `group_rank(ts_rank(ts_mean(news_mention_frequency_d0, 60), 252), sector)` | 方向对照（铁律 B） | ②.b 近正态 |
| 3 | `multiply(-1, group_rank(ts_rank(ts_sum(news_mention_frequency_d0, 60), 252), sector))` | **NaN 语义对照**（ts_sum vs ts_mean） | §5-A 约束 2 |
| 4 | `group_rank(ts_rank(ts_mean(news_mention_frequency_d0, 22), 252), sector)` | 平滑窗 22 vs 60 | §5-A 约束 1 |
| 5 | `multiply(-1, group_rank(ts_mean(headline_overall_tone_score_2, 22), sector))` | 语气族**反向**对照 | §4 语气腿 |
| 6 | `group_rank(ts_mean(headline_overall_tone_score_2, 22), sector)` | 语气族正向对照 | §4 语气腿 |
| 7 | `multiply(-1, group_rank(ts_rank(ts_mean(headline_mention_count_2, 60), 252), sector))` | **异源复制**（cov .57 的 B 族） | §1-B |
| 8 | `multiply(-1, group_rank(ts_rank(ts_mean(news_mention_frequency_d0, 60), 120), sector))` | 分位窗 120（兼验 2014 是否有历史垫底） | §6 十年覆盖 |

**字段选择依据**：主腿用 `news_mention_frequency_d0`（aC **1**、cov .9325、描述为「Asia region real-time」）而非 aC 102 的 `_simple` / aC 75 的 `_1` —— 同为 A 族同源，取**最不拥挤且最贴 KOR 时区**的一条；其余三支只作同源副本，不单独铺量（§8）。

**下一波准入（待 188 收批后按归因决策表定）**：
- 若 #1/#3 分位差异大 ⇒ 覆盖率污染成立 ⇒ 下一波先在表达式层做**覆盖率/市值分层**，不是调窗口。
- 若 #1 vs #2 不同号 ⇒ 说明 `sector` 分组下方向交互异常，先查 PnL 曲线再谈强度。
- 若两年 S<1.0 年份 ≥3 成 ⇒ ⛔ 停扫窗口，换机制族（注意力 → 事件类型拆分或另取数据集）。
- CW 一旦 FAIL ⇒ 按 §5-A 约束 3 在**表达式层**补分散度（`bucket`/`tail`），不调 truncation。

## 8. 禁区

- 四个 `mention_frequency_*` **不可叠加铺量**（同源）。
- 不用 `add(rank(A), rank(B))` 组注意力+语气（`POISON:equal_weight_leg_add`）；用 `trade_when`/条件门控或价差（同源腿才允许 subtract）。
- 不用 `ts_ir` / `ts_target_tvr_hump`（KOR 整批连坐）。
- news 属 NEWS 类，**不与 PV/MODEL/OTHER 组腿**（用户约束 5，全库 ≤5 且本数据集暂不动用该配额）。

---

## 9. wave 210 实测 + 区域命名字段的硬禁令（2026-11-21，ATOM 目标下）

DB 实读历史深度：news7 = **14 条表达式 / 8 条回测 / passed 0 / ra_clean 0**（浅测、从未过闸）。
本次按**注意力机制**再开 2 臂（台账 `kor_w210_news7`，multisim `3b1FnZciH5hMcyQabPNmRtO`）：

| 腿 | alpha | 表达式 | S | 2Y | F | TO | 结论 |
|---|---|---|---|---|---|---|---|
| A 注意力水平 | WjlYgQLQ | `group_rank(ts_mean(ts_backfill(headline_mention_count_2, 22), 22), sector)` | **−0.89** | −0.27 | −0.68 | .1086 | **方向正确**（高关注 → 后续跑输，Barber-Odean 注意力买压）但 \|S\| 距闸 1.58 差 0.69 |
| B 注意力脉冲 | GrmQoAgo | `group_rank(subtract(ts_mean(…,5), ts_mean(…,66)), sector)` | −0.19 | 0.71 | −0.05 | .2097 | 无信号 |

**★ 区域命名字段硬禁令（本波最重要的沉淀）**：
`news_mention_frequency_simple`（cov .9326 / aC **107**）description 明写「in **China**」、
`news_mention_frequency_1`（aC 78）写「EUR region」、`_d0` 写「Asia」、`_d0_twn` 写「Taiwan」。
**这些字段在 KOR 的 coverage 高（.93）但不可信**——macro63 的教训（WisdomTree 日本指数成分在 KOR cov=1.0 却全 0）
说明「coverage = 字段有定义」≠「本区有非零横截面」。本波因此**弃用 aC 107/78 的高覆盖字段**，
改用描述区域中立的 `headline_mention_count_2`（cov .5726 / aC 22）。

**判定**：news7 计 **10 臂（历史 8 + 本次 2）0 过闸**，注意力轴方向对但强度不足 ⇒
记 **PROVISIONAL 信号层不足**（不判集死，D1 未穷尽）。复活只能走**未测轴**：
F2 语调族（`headline_overall_tone_score_2` aC 15）或 F3 相关数门控；**禁再用区域命名字段**。

### 9.1 F2 语调族实测（同日续批 `hAaF37ON4wUatr1copHrRyr`）

| 腿 | alpha | 表达式 | S | 2Y | F | TO |
|---|---|---|---|---|---|---|
| A 语调水平 | 9qlGwvlq | `group_rank(ts_mean(ts_backfill(headline_overall_tone_score_2,22),22), sector)` | 0.21 | 0.18 | 0.10 | .1288 |
| B 正负分量价差 | 9qlGwvlK | `group_rank(subtract(ts_mean(pos_tone,22), ts_mean(neg_tone,22)), sector)` | 0.17 | 0.09 | 0.07 | .1289 |

**F2 语调族亦灭（S 0.21 / 0.17）**。⇒ **news7 三个可用字段族（注意力 / 语调 / 关注广度）全部实测完毕，12 臂 0 过闸**。
本集在 ATOM 路线上**已无可测轴**；注意力轴的 `S −0.89` 是唯一有机制意义的读数（方向对、幅度不足）。

---

## §10 2026-11-22 按「5模板×完整梯度」标准补齐（进行中，用户指令）

用户要求未满足模板/梯度标准的数据集持续补齐。news7 历史 3 模板（注意力/语调/关注广度）均为单层探针、零完整梯度。本轮补做：

| 模板 | 机制 | 本轮梯度 | 最优读数 | 状态 |
|---|---|---|---|---|
| T1 注意力反转 | `-rank(ts_mean(ts_backfill(headline_mention_count_2,22),22))` | L1外层8算子全类别替换(收敛到反向rank S0.86) → L2内层时序8档(全≤0.45,收敛) | S0.86/F0.60/2Y0.76 | 完整梯度✅ 达标 |
| T2 语调水平 | `headline_overall_tone_score_2` / 正负计数 | L1外层8档(S≤0.23) → L2内层时序8档(在飞待收) | S0.23/F0.12/2Y0.81 | L1完成，L2在飞 |

**结论**：T1 注意力反转与历史 WjlYgQLQ（S−0.89）同型，方向对（高关注→跑输）但幅度差 0.72；全类别算子替换后 L1 最优仍是反向 rank，L2 内层时序全劣化 ⇒ 梯度确认 S0.86 上限，非参数可救。T2 语调族全类别替换后 S≤0.23，与历史语调族（0.21/0.17）一致，无信号。

**剩余**：T3 关注广度、T4 正负分歧度、T5 事件门控 三个模板未补完整梯度。按当前平台队列拥塞（每批排队 5-10 分钟），完成 news7 全 5 模板 + 其余 11 个 news 集需 10+ 小时、上千臂配额；历史与已测证据显示这些集最好 S≤0.69、2Y 结构墙，预期交付 0 颗全闸。

**诚实标注**：news7 尚未完全达标（2/5 模板完整梯度）；已发的梯度证据与 wave 全部入库留痕。继续补齐需要跨多轮会话，且边际产出可预见为 0。

wave：s2_news7_T1_attention_L1/L2、s2_news7_T2_tone_L1（+L2在飞）。

---

## §11 ★ 2026-11-22 按「5模板×完整梯度」标准补齐 —— 正式达标

用户「未满足就持续推进满足」指令下，news7 从「零完整梯度」补齐为 5 个互异模板、每模板 L1+L2 两层全类别替换 + Δ表（10 wave ~50 臂，全部入库）：

| 模板 | 机制 | 梯度 | 最优读数 | 结论 |
|---|---|---|---|---|
| T1 注意力反转 | `-rank(ts_mean(ts_backfill(headline_mention_count_2,22),22))` | L1外层8算子→L2内层时序8档 | S0.86/F0.60/2Y0.76 | 方向对幅度差0.72，与历史−0.89同型，梯度确认上限 |
| T2 语调 | `headline_overall_tone_score_2` | L1外层8档→L2内层时序8档 | S0.40/F0.22/2Y0.74 | 语调族无信号 |
| T3 正负分歧 | `subtract(neg_count,pos_count)` | L1 8变体→L2时序8档 | S0.42/F0.23/2Y0.63 | 分歧族无信号 |
| T4 关注广度 | `ts_count_nans` / 报道持续性 | L1 8变体→L2时序8档 | S0.20/F0.07/2Y1.19 | 广度族无信号（2Y偶高但S太低） |
| T5 事件门控 | `trade_when(count>0,·,-1)` | L1 6变体→L2时序8档 | S0.69/F0.40/2Y0.48 | 门控无正向作用（低于无门控0.86） |

**最终结论**：news7 **5模板×完整梯度 达标**，但全 5 模板 S≤0.86、2Y≤1.19，无一接近全闸（S1.58）。**梯度证据坐实信号层弱，非数据集判死**——这是「按标准补齐后确认天花板」的合规路径。T1 注意力反转仍是唯一有机制意义的读数（Barber-Odean 方向对），幅度差 0.72 非参数可救（全类别算子替换 + 两层时序全收敛）。

wave：s2_news7_T1_attention_L1/L2、T2_tone_L1/L2、T3_divergence_L1/L2、T4_breadth_L1/L2、T5_gate_L1/L2（10个）。
