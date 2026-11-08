# 取证笔记 · 2026-11-06

## 论文
- Antweiler & Frank (2004)：股吧消息板非纯噪声，情绪与波动/收益相关。
- Da, Engelberg, Gao (2011)：搜索量注意力 → 短期高估后反转。
- 韩国市场情绪化交易风险（新华社观察，制度背景，非因子定义）。

## 论坛
- 【Alpha Idea】net_buy 高换手驯服：日度散户计数先时序聚合，decay 治不了排名翻转。
- USA OTHER 穷尽复盘：equity_forum_data / stock_cluster_dl 作 virgin 靶仍死 ——「低竞争≠有信号」。KOR 不得未测照搬判死，但 Wave1 须小批探针、快判死。
- USA socialmedia 笔记：`vec_avg(scl39_top5_people_also_watch_ticker_ii)` 出现 PnL 异常字段记录 ⇒ ID 向量风险先验。

## 补充检索（Wave1 在飞期间）
- other553 论坛：[{"title":"【Data】怎么用 sentiment：类目叫情绪，最挤的字段没一个是情绪","votes":1,"snippet":"文体 · 不是情绪other553叫 FinancialOpinion Mining，最挤的却是句长、词数、数字个数：描述文本形态。 oth553_a_avgnumericpos 42； oth553_a_avgsentlen","date":"2026-09-23T06:11:42Z"},{"title":"【方法论】池塘有鱼，是没给 AI 装导航：用 archetype 分类法把 ACTIVE 池138 个信号挖出 90 个被忽视的非分析师另类信号","votes":0,"snippet":"类后， 90 个是非分析师信号 （被多数人忽略）；其中 文本舆情族 4 支是独立的第 3 生产安全族 （news/opinion/advertisement 另类数据）， zscore 基本面 31 支是待挖矿脉 。 这个方法直接催生了我前两篇的","date":"2026-10-30T15:41:08Z"},{"title":"挖掘 Token 黑洞 
- KOR sentiment：[{"title":"【sentiment模板】帮助点sentiment塔","votes":18,"snippet":"模板： group_neutralize(reverse(ts_max(【snt21_pos】 - 【snt21_neg】, 【days】)), 【group】) 以下是AI 解释： ### 核心内容摘要： 1"},{"title":"【Community Leader -因子构造 💎 】MCP七十二变模板之news-sentiment点塔","votes":36,"snippet":">, <sentiment/>, <days>), <group/>) 最近由于没有什么好的思路，于是决定使用MCP工具来进行辅助，在七十二变中找到了一个不错的模板。这个模板捕捉 新闻交易活跃度"},{"title":"【Alpha模板】情绪数据中用ts_covariance构建alpha模板","votes":52,"snippet":"3.个人对该模板的想法 其实一开始我在脑补跑这个模板的结果的时候，还以为这个模板跑出来alpha的会是turnover非常高的alpha(捕捉短

## 决议状态
- 主战场暂定 equity_forum_data（问卷超时自动选，**待用户显式确认后再发仿真**）。
## Wave1b 实测（socialmedia39，2026-11-06）
- Vkxm2zGY vec_count: S **-0.66** / 2Y -0.66 → REJECT
- leA5QGWA vec_avg: S **0.94** / 2Y **1.44** → REJECT（未达 REGULAR 1.58）
- 决策树「scl39 出奇强」未触发；ID 向量对照不计入主交付。

## 论坛再取证（Wave1 在飞期间）
- 【复盘】USA/D1/OTHER 穷尽：virgin 靶 `equity_forum_data` / stock_cluster_dl 复刻同样死法——低竞争≠有信号（已先验，KOR 仍须实测快判）。
- 【Alpha Idea】流程文把 equity_forum_data 与 socialmedia39/other100 并列作注意力计数替换候选。
- 直接搜 `equity_forum_data KOR` 几乎无专文；KOR 本集经验空白，以 Wave1 读数为准。
## 论坛精读 · news20 降噪（Wave2 在飞期间，2026-11-06）

### 「信息洪流里捞金：news20 网页舆情降噪体会」(votes 29)
- 裸多空情绪夏普差：通稿/复读机噪声多，只有业务突破/监管/重组才有持续驱动力。
- **decay 要大**：新闻情绪时效 3–5 天即被吸收。
- 冷门低频：长期无新闻标的偶发水文 → 需文章数量加权置信度。

### 「别再用裸 sentiment —— relevance 加权 + 新颖度过滤」(votes 31)
- 套路1：`ssc × relevance/100` 或 relevance>60 过滤。
- 套路2：`event_similarity_days × sentiment` 保新信息。
- 套路3：`nws20_ghc_lna` 情绪变化（高换手，配 decay）。
- 进阶：story_event_count 大 → 注意力稀释；实体相对故事偏离。
- Wave3 载荷已含 N02 relevance 加权、N05 novelty、N06 evt_cnt；ghc_lna 可作破闸加试。

## 论坛补证（2026-11-06 夜 · Wave3 在飞期间）

### news20 降噪帖（43554129390103）
- 裸正负买卖夏普惨；信噪比低。
- 时间衰减要迅速：情绪 3-5 天被吸收 => decay 必须调大（默认 decay=4 可能偏小）。
- 过滤冷门低频：结合文章数量加权置信度。

### MCP news-sentiment 模板帖（37140180319127）
- 骨架 group_zscore(-ts_corr(活跃度, 情感, W), group)。
- ATOM：两腿同属 news20（rp_story_event_count x ssc），禁跨集。

### 对决策的影响
- Wave3 若弱：先 Mode A 同骨架 decay=10，再判切 news66。
- 备胎：wave3b_news20_decay_payload.md

### KOR D1 塔点亮
- 已点亮：analyst3 / fundamental3 / model3 / shortinterest4
- 未点亮：news0 / socialmedia0 / sentiment0 / earnings0 / institutions0 / imbalance0 / macro0 / risk0 / insiders1 / other1 / pv2

## 注意力溢出论文（Wave3b 等待窗）
- Guo/Peng/Tao/Tu 2017 Joint News, Attention Spillover, and Stock Returns（SSRN/arXiv）：联合新闻覆盖触发注意力传染，短期估值膨胀；EDGAR IP 轨迹证伪溢出。
- 落地到 news66：单字段 `mws66_api_views` 作注意力代理；测水平/变化/波动/低关注倒数（冷门跳变）。
- news59 体检：仅 2 个日历字段 → **排除连续 alpha**。
- news54：40 字段中 ~27 为时间戳；其余 headline/flag/factor → 连续情绪轴弱，排 news66 之后。
