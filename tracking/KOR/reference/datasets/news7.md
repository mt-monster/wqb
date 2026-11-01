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
