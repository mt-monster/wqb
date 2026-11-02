# GBR NEWS 第四波 `news_light3_4` — news18 字段 × 相关性矩几何（模板池 v1）

> 设计日期：2026-11-02。前置：news17 三波 36 条全 REJECT（`news_light3_1/2/3`，见各自模板库），
> news17 机制面穷尽；本波转 **相关性矩算子几何**（论坛 94 票先例）× news18 字段交付。
> 表达式：`news_light3_4_expressions.json`。

## §0.5 字段新颖度修正（派发后核查，影响归因口径）

⚠ `sentiment_*` 系列的 ac=0 **不是新数据**——是 RavenPack 已知 analytics 的 **D1 feed 别名**
（get_datafields description 逐一标注 `alias for X`）：

| 别名字段 | 原 analytics | 原字段 alphaCount | news17 波是否测过同 analytics |
|---|---|---|---|
| sentiment_news_impact_projection_d1 | NIP（新闻影响预测，**vol 影响**非方向） | nws18_nip 106 | 否（news17 无 nip） |
| sentiment_earnings_classifier_d1 | BEE 财报评估 | nws18_bee 13 | 否 |
| sentiment_m_and_a_classifier | BAM M&A | nws18_bam 4 | **是**（light3_3 V4 同 analytics，S 0.14 死） |
| sentiment_earnings_release_classifier | BER 财报发布 | nws18_ber 22 | **是**（light3_3 V1/V3 同 analytics，max 0.45 死） |
| sentiment_commentary_classifier | BMQ 评论 | nws18_qmb 202 | 否（但原字段拥挤度 202） |
| sentiment_composite_score_d1 | CSS 综合情绪 | — | 否 |
| sentiment_peq_score_d1 | PEQ 全球股票情绪 | nws18_qep 14 | **是**（light3_3 V6/V7 同 analytics 死） |
| story_entity_record_count_d1 | RP_STORY_EVENT_COUNT | story_event_record_count 62 | 否 |

**修正后的本波定位**：主假设从「未测数据轴」改为「**已知 analytics × 未测算子几何**」——
相关性矩（ts_corr/cov/reg 与 returns 的动态关系）提取的信息维度与 level/差分（light3_3 的
ts_rank∘ts_mean 慢矩）不同，forum 94 票先例正是「同一批 nip 字段在相关性几何下出 PPA」。
BAM/BER/PEQ 三字段在 level 几何下已判死，本波 W4/W5/W6 是**几何复活测试**（不是新字段测试）。
W1–W3（NIP×相关性矩）才是真新组合（nip + 几何都未测）。

## §0 统一基底（与前三波逐字一致，保证归因可比）

GBR / TOP700 / D1 / **neutralization=FAST** / decay 15 / truncation 0.05 / nanHandling ON /
maxTrade OFF / pasteurization ON / unitHandling VERIFY / FASTEXPR / IS 2014-01-01~2023-12-31。
闸线 S ≥ 1.58、F ≥ 1.0、2Y ≥ 1.58（含等号严格）、SUB ≈ 0.478×S；过闸判据 `ra_failed_checks == []`。

**设置反查**（get_alpha_details QPva2rwX）：neutralization=FAST 与 settings.json 的 SUBINDUSTRY
档案不同——本波次系列实用档是 FAST，且这正是论坛配方「相关性算子 + **FAST neutralization**」的核心。

## §1 十二模板（9 类骨架互异 + 字段轴对照 ×3 + 矩切换 ×2）

统一壳 `ts_target_tvr_decay(group_neutralize(内核, densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)`；
W12 用 `group_zscore(内核, densify(market))`（分组轴几何，点塔帖原壳）。

| # | 模板 | 内核 | 骨架/矩 | 字段轴 | 来源 |
|---|---|---|---|---|---|
| W1 | nip-收益相关性 | `ts_corr(vec_avg(sentiment_news_impact_projection_d1), returns, 22)` | corr 几何 | 影响预测 ac=0 | **forum 40847481080087（94 票，EUR nip→PPA 先例）** |
| W2 | nip-收益协方差 | `ts_covariance(vec_avg(sentiment_news_impact_projection_d1), returns, 22)` | cov 矩 | 同 W1 | 同帖（三模板之二） |
| W3 | nip-收益回归 β | `ts_regression(returns, vec_avg(sentiment_news_impact_projection_d1), 60, lag=0, rettype=2)` | reg 矩 | 同 W1 | 同帖（三模板之三） |
| W4 | 财报情绪-收益相关性 | `ts_corr(vec_sum(sentiment_earnings_classifier_d1), returns, 22)` | corr 几何 | 财报分类器 ac=0 | forum 帖 × PEAD（Bernard-Thomas 1989） |
| W5 | M&A 情绪-收益相关性 | `ts_corr(vec_sum(sentiment_m_and_a_classifier), returns, 60)` | corr 几何 | M&A 分类器 ac=0 | forum 帖 × 并购事件（Mitchell-Netter 1994） |
| W6 | 财报发布情绪慢矩 | `-ts_rank(ts_mean(vec_sum(sentiment_earnings_release_classifier), 60), 252)` | rank∘mean 慢矩 | 财报发布 ac=1 | 自建（PEAD 漂移水平对照） |
| W7 | 实体广度 | `-ts_rank(ts_mean(vec_avg(story_entity_record_count_d1), 22), 252)` | rank∘mean 慢矩 | 实体广度 ac=2 | 自建（institutions6「广度>深度」实证平移） |
| W8 | 事件广度动量 | `-ts_rank(ts_delta(ts_mean(vec_avg(multi_entity_story_event_count), 22), 60), 252)` | 一阶差分 | 事件广度 ac=41 | 自建（广度矩切换） |
| W9 | 悲观主导（min 几何） | `-ts_rank(ts_mean(vec_min(sentiment_composite_score_d1), 22), 252)` | **min 非线性** | 综合情绪 ac=17 | Tetlock 2007（不确定性/悲观不对称） |
| W10 | 水平−分歧 | `subtract(rank(ts_mean(vec_avg(sentiment_commentary_classifier), 60)), rank(ts_mean(vec_stddev(sentiment_commentary_classifier), 60)))` | **双 rank 差几何** | 评论分类器 ac=1 | Harvey 2017（分析师分歧类比） |
| W11 | 预测−情绪缺口 | `-ts_rank(ts_mean(subtract(rank(vec_avg(sentiment_news_impact_projection_d1)), rank(vec_avg(sentiment_composite_score_d1))), 60), 252)` | 预期差缺口 | nip×综合情绪 | 自建（供应商预测 vs 实际情绪的期望差） |
| W12 | 活跃度×情绪相关性（点塔帖平移） | `group_zscore(-ts_corr(vec_avg(nws18_nip), vec_avg(sentiment_composite_score_d1), 22), densify(market))` | **group_zscore∘ts_corr** | nip×综合情绪 | **forum 37140180319127（36 票，news-sentiment 点塔模板）** |

**字段轴对照设计**：W1/W4/W5 同 corr 几何 × 三个事件类型字段（影响预测/财报/M&A）——判字段效应固定结构。
**矩切换对照**：W1(corr) vs W2(cov) vs W3(reg) 同 nip 字段 × 三种相关性矩；W7(水平) vs W8(一阶差分) 同广度族。
**非线性对照**：W9 min 几何 vs W6/W7 mean 几何。

## §2 合规声明

- 单数据集（news18）+ 内置 `returns` ⇒ **ATOM**；不占两塔配额；塔位=NEWS。
- 无 `add(A,B)` 混信号；W10/W11 的 `subtract(rank,rank)` 是差几何（强库 §6 允许的几何重构），非权重调参。
- 时间窗 22/60/252（月/季/年）；`lag=0/rettype=2` 为函数参数（帖原文）。
- W1–W5 相关性族**不加负号**（忠实 nip 帖原文符号）；W6–W12 取 `-ts_rank`（Tetlock 2007 悲观方向，news_light3_3 V1/V3 正 S 验证 GBR 成立）。
  收批若相关性族出 |S|≥0.8 大幅负号 ⇒ 单条烧翻向探针；两头弱判死。
- 全部字段 VECTOR（64/70）已手工包 `vec_*`（vec_avg/vec_sum/vec_min/vec_stddev），无裸 VECTOR。
- 量纲纪律：无 `add(带量纲, 裸常数)`；ts_covariance 量纲输出直接进 group_neutralize 不加常数。
- **工具语法**：`ts_regression` 第 4/5 参数必须命名（`lag=`/`rettype=`）——静态闸实证（批 1 首发被拒）。

## §3 收批账本（2026-11-02 收批，0/12 全 REJECT）

批 1（W1–W6）`14F8cq3JQ4QkcaUP4AzJ2f5` / 批 2（W7–W12）`34ZOC26qV55mabr12ubKYMwE`，无连坐。

| # | 模板 | alpha | S | F | 2Y | SUB | TO | failed_ra | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| W1 | nip corr 22 | 0mY7zzeG | **0.26** | 0.07 | **0.63** | 0.56 | 0.093 | 3 | REJECT（corr 族最优） |
| W2 | nip cov 22 | npvg33ZE | −0.17 | −0.04 | −0.41 | 0.47 | 0.129 | 3 | REJECT |
| W3 | nip reg 60 | mLo8ZZq9 | −0.01 | −0.00 | −0.93 | −0.04 | 0.130 | 5 | REJECT |
| W4 | BEE corr 22 | xArxRRem | 0.21 | 0.05 | −0.01 | 0.26 | 0.100 | 3 | REJECT |
| W5 | BAM corr 60 | d5Wxddnj | 0.13 | 0.03 | **0.89** | −0.14 | 0.110 | 4 | REJECT（2Y 次高） |
| W6 | BER 慢矩 | VkxpOOX5 | −0.15 | −0.03 | −0.06 | −0.40 | 0.080 | 4 | REJECT |
| W7 | 实体广度 | QPvaEXMW | −0.25 | −0.06 | −0.90 | −0.24 | 0.086 | 4 | REJECT |
| W8 | 广度动量 | 1YN7JEeM | 0.07 | 0.01 | 0.41 | −0.06 | 0.079 | 4 | REJECT |
| W9 | min 悲观 | 0mY7zvlk | −0.16 | −0.03 | −0.24 | 0.04 | 0.086 | 3 | REJECT |
| W10 | 水平−分歧 | GrWwkJaG | **0.42** | 0.13 | **1.09** | −0.00 | 0.080 | 4 | REJECT（全波双最高） |
| W11 | 预期差缺口 | 9qxwJ0ve | 0.18 | 0.04 | −0.06 | 0.03 | 0.079 | 4 | REJECT |
| W12 | 点塔帖 group_zscore∘ts_corr | 3qo7zLrQ | −0.02 | −0.00 | 0.19 | 0.06 | 0.084 | 3 | REJECT |

## §4.8 归因定稿（全灭后）

1. **相关性矩族 GBR 不复现**（W1–W5 全灭，max 0.26）：forum 94 票 EUR 先例（nip×corr→PPA）
   在 GBR TOP700 连 near 线 1.2 都不到。EUR 出的是 **PPA**（Power Pool 线松），与 RA 闸线 1.58
   不可比——**论坛「出 PPA 容易」≠「过 RA 闸」**。地域差异 + 门槛差异双重原因。
2. **几何复活测试失败**：BAM（W5 0.13 vs light3_3 V4 0.14）、BER（W6 −0.15 vs V1 0.38/V3 0.45）
   ——corr 几何没有救活 level 几何下死掉的 analytics，BER 在 level 几何下反而更强。
   相关性矩提取的「字段-收益动态关系」维度在 GBR 新闻数据上无截面区分度。
3. **W10（水平−分歧）全波唯一亮点**：S 0.42 / 2Y 1.09 / margin 30bp——Harvey 分歧折价方向正确
   但幅度仅闸线 26%。S≥0.8 翻向线不到，不烧探针。
4. **NIP 判死**（GBR）：三矩 0.26/−0.17/−0.01，论坛最强先例不成立。
5. **按 §4.6 预设判读：news18 在 GBR 真判死**。四波总账 news_light3_1/2/3/4 = 48 条全 REJECT，
   GBR NEWS 线 IS 天花板 0.91（light3_2）。GBR NEWS 挖掘空间彻底关闭（存量仅 58E7jkaN 已提交
   + MPYq0819 篮内，NEWS 塔 2/3）。**缺口 2 条必须走 B 路线（其它塔）或 C（先提交 8 条）**。

## §4 归因口径

1. **相关性矩族（W1–W5）**：若出信号（S≥1.2）⇒ 论坛配方在 GBR 复现成功，立即查 prod（EUR 出的是 PPA，PPA 的 prod 线更松，RA 需 prod<0.7）。
2. **字段轴对照（W1/W4/W5）**：同 corr 几何三字段 ⇒ 判事件类型字段效应。
3. **矩切换（W1/W2/W3）**：同 nip 字段三矩 ⇒ 判 corr/cov/reg 几何效应。
4. **广度族（W7/W8）**：对照 institutions6「广度>深度」——若 W7 出信号 ⇒ 广度机制跨数据集成立。
5. **W9 min 几何**：悲观不对称检验；W10 差几何；W11 预期差。三者互为非线性骨架对照。
6. **全灭判读**：若相关性矩族（有 94 票 EUR 先例）都全灭 ⇒ news18 在 GBR 真判死（EUR 正面先验 + GBR 三波负面），NEWS 线补塔改走 B 路线（其它塔凑 10 条）。
7. **EUR 负面先验对照**（forum 38878004433815，30 票）：EUR_TOPCS1600 news18 2400+ 一阶表达式 sharpe 均值 0.05——
   但浅结构 + 2026-03 时 `sentiment_*_d1` 新字段族（ac=0）尚未上架；本波是深结构 + 新字段，先验不直接适用。

## §5 论坛与文献先验（模板来源汇总）

| 来源 | 内容 | 落点 |
|---|---|---|
| forum 40847481080087（94 票） | 「相关性算子 + FAST neutralization + nip 字段」EUR D0/D1 出 PPA 容易；三模板 ts_corr/ts_covariance/ts_regression；nip 在 news18（Ravenpack） | W1–W5 设计核心 |
| forum 37140180319127（36 票） | `group_zscore(-ts_corr(<news>, <sentiment>, <days>), <group>)` 点塔模板；注意力驱动/信息扩散/过度反应 | W12 |
| forum 38878004433815（30 票） | EUR news18 2400+ 浅结构全灭（均值 0.05）；「勤换中性化 + 处理 turn」 | §4.7 负面先验对照 |
| forum 33554030316183 | news54 Data Idea：事件情绪/重要性指数特征工程思路 | 机制概念参考 |
| Bernard-Thomas 1989 | PEAD 财报后漂移 | W4/W6 |
| Tetlock 2007 | 媒体悲观→收益高、不确定性不对称 | W9、全波符号方向 |
| Harvey 2017 | 分析师分歧折价 | W10 |
| institutions6 本库实证（2026-11-02） | 广度>深度一个量级 | W7/W8 |
