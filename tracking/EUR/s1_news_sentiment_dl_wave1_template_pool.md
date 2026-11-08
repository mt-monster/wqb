# s1_news_sentiment_dl_wave1 模板池（EUR / TOP2500 / D1 / industry）

> 数据集：`news_sentiment_dl`（category **news**，NEWS 塔当前 **1/3**）。66 个字段**全 VECTOR**，coverage 0.7443 / 0.7508 / 0.7723（三来源），**alphaCount 0–7 ⇒ 全平台近乎零开采**，是本区当前最干净的白地。
> 单数据集 ATOM 合法，不占两塔组合配额，不触碰「禁混集合 {PV, MODEL, OTHER, FUNDAMENTAL}」。
> 开波日 2026-11-06。批次 `Unvy6fIq4ra95BvSKoABAE`（T01 / T03）。

## 一、字段画像（66 VECTOR = 3 来源 × 22 指标）

三来源（**同一篇文章被三家独立文本分析厂商打分**）：
| 后缀 | coverage | 含义 |
|---|---:|---|
| `_bbgnews_enhanced` | 0.7443 | Bloomberg News 增强文本管线 |
| `_inferess` | 0.7723 | Inferess 情感引擎 |
| `_trna` / `_trna_enhanced` | 0.7508 | TRNA 新闻分析 |

22 指标分五族：
1. **可读性/句法族**：`avg_syllables_per_word`(aC 2–4)、`avg_words_per_sentence`(aC 0–1)、`sentence_count`(aC 0–1)、`text_complexity_score`(aC 0–1)、`text_perplexity`(aC 1–3)、`vocab_coverage_ratio`(aC 0–1)
2. **词计数族**：`positive_word_count` / `negative_word_count`（aC 0–1）
3. **词情绪水平族**：`max/mean/min_{positive,negative}_word_sentiment`（aC 0–7）
4. **情绪离散族**：`{positive,negative}_word_sentiment_entropy` / `_stddev`（aC 0–1）
5. **未知族**：`output_metric_1..4`（描述仅「custom output metric」）⇒ **语义不明，按纪律禁止盲挖**，仅作最后备选。

★ **本集的结构性独特之处**：三来源对**同一指标**独立打分 ⇒ ①可直接做**跨厂商分歧**（同指标三厂商之差的截面排序），这是 prod 相关性天然最低的形态（没有任何生产 alpha 会这么构造）；②也可三来源取均值降噪。

## 二、机制先验（文献）

| 机制 | 结论 | 出处 |
|---|---|---|
| 披露复杂度（obfuscation vs information） | 加工成本高的披露 ⇒ 价格反应不足/延迟 ⇒ 复杂度可预测后续收益 | Bushee, Gow & Taylor (2018, *JAE*)；Bloomfield (2002, *JBFA*) incomplete revelation hypothesis |
| 词表情绪计数 | 领域词表（正/负词数）优于通用词典；净情绪占比有预测力 | Loughran & McDonald (2011, *JF*) |
| 媒体悲观与反转 | 媒体悲观度短期制造下行压力、随后反转 | Tetlock (2007, *JF*) |
| 文本情绪 ML | 10-K 文本情绪预测异象 | Li (2010, *JF*) |
| 意见分歧 | 分歧 + 卖空约束 ⇒ 高估；熵/标准差是分歧代理 | Miller (1977)；分歧度文献 |
| 媒体内容横截面 | 媒体语调对横截面收益有独立解释力 | Hillert, Jacobs & Müller (2014, *JFE*) |
| ★跨厂商打分分歧 | **自建机制**（无直接文献）：同指标多厂商打分差 ⇒ 信息不确定性 / 文本本身模糊 | 自建 |

## 三、模板池（12 个结构互异；差异落在机制 / 算子几何 / 矩 / 归一方式）

| # | 名称 | 骨架 | 机制 | 来源 | 算子 |
|---|---|---|---|---|:-:|
| T01 | 披露复杂度水平 | `-group_rank(ts_backfill(vec_avg(text_complexity_score_trna_enhanced),250),industry)` | 加工成本高⇒反应不足 | Bushee 2018 | 3 |
| T02 | 句法冗长度 | `-group_rank(ts_backfill(vec_avg(avg_words_per_sentence_inferess),250),industry)` | 句长=冗长，独立于复杂度评分 | Li 2010 | 3 |
| T03 | 净情绪密度（每句） | `group_rank(ts_backfill(divide(subtract(vec_avg(positive_word_count_inferess),vec_avg(negative_word_count_inferess)),vec_avg(sentence_count_inferess)),250),industry)` | 词表净情绪 / 信息量归一 | LM 2011 | 7 |
| T04 | 极端负面词强度 | `-group_rank(ts_backfill(vec_avg(max_negative_word_sentiment_inferess),250),industry)` | 尾部负面词定调（最坏词主导） | Tetlock 2007 | 3 |
| T05 | 负面情绪熵 | `group_rank(ts_backfill(vec_avg(negative_word_sentiment_entropy_trna),250),industry)` | 分歧 + 卖空约束⇒高估 | Miller 1977 | 3 |
| T06 | 情绪强度标准差 | `-group_rank(ts_backfill(vec_avg(positive_word_sentiment_stddev_inferess),250),industry)` | 情绪一致性 vs 发散 | 分歧度 | 3 |
| T07 | 词汇覆盖率 | `group_rank(ts_backfill(vec_avg(vocab_coverage_ratio_trna_enhanced),250),industry)` | 高覆盖=信息已被熟悉/定价 | 自建 | 3 |
| T08 | 困惑度 | `-group_rank(ts_backfill(vec_avg(text_perplexity_inferess),250),industry)` | 高困惑度=新颖信息⇒漂移 | Bloomfield 2002 | 3 |
| T09 | ★跨来源复杂度分歧 | `group_rank(subtract(ts_backfill(vec_avg(text_complexity_score_trna_enhanced),250),ts_backfill(vec_avg(text_complexity_score_bbgnews_enhanced),250)),industry)` | 同指标跨厂商打分差=不确定性 | **自建（跨厂商）** | 6 |
| T10 | ★复杂度一阶变化 | `-group_rank(ts_delta(ts_backfill(vec_avg(text_complexity_score_trna_enhanced),250),63),industry)` | 披露变难=坏消息被掩盖（一阶矩，非水平） | Bushee 2018 | 4 |
| T11 | ★情绪×复杂度交互 | `multiply(group_rank(ts_backfill(net_tone_S,250),industry),group_rank(subtract(0,ts_backfill(vec_avg(text_complexity_score_trna_enhanced),250)),industry))` | 坏消息被写复杂⇒反应更慢（条件机制，非加性） | 自建（交互） | 8 |
| T12 | 冗长校正后的净情绪 | `group_rank(divide(ts_backfill(net_tone_S,250),ts_backfill(vec_avg(avg_words_per_sentence_inferess),250)),industry)` | 每词情绪强度（分母换量纲） | 自建 | 7 |

**模板互异性核对**：T01/T02 同属复杂度但一个用厂商复杂度评分、一个用句法统计（相关性低）；T03/T12 同为情绪但归一量纲不同（句子数 vs 句长）；T04/T05/T06 分别测**尾部 / 离散度 / 二阶**；T09 跨厂商；T10 一阶差分；T11 交互。**无「同骨架换窗口」的伪多样**。

## 四、执行进度

| 批 | 模板 | 表达式（简） | 状态 | S | F | 2Y | TO |
|---|---|---|---|---|---:|---:|---:|---:|
| 1 | T01 复杂度水平 | `-group_rank(ts_backfill(vec_avg(text_complexity_score_trna_enhanced),250),industry)` | 在飞 `Unvy6fIq4ra95BvSKoABAE` | | | | |
| 1 | T03 净情绪密度 | `group_rank(ts_backfill(divide(subtract(vec_avg(pos_cnt),vec_avg(neg_cnt)),vec_avg(sentence_count)),250),industry)` | 在飞 `Unvy6fIq4ra95BvSKoABAE` | | | | |

- 批级设置：decay 8 / SLOW_AND_FAST / trunc 0.08 / unitHandling VERIFY / nanHandling ON / pasteurization ON / maxTrade ON；区间 2014-01-01~2023-12-31。
- 选 `SLOW_AND_FAST` 依据：新闻文本类为慢信号（预期 TO < 8%），Memory「慢信号先试 SLOW_AND_FAST」。
- 预检：`validate_expressions` `valid=true` / `unknown_fields=[]` / `platform_field_count=4`；算子 3 与 7（上限 12）。

## 五、纪律

- **判死口径**：同一面 ≥6 个结构互异骨架全灭才判死；不足 6 个只降级不封盘。
- **新族合格硬判据**：出炉后先跑 `compute_mutual_correlation([ZYQmolVx, e76kv2xE, xArjE96W, 新件], threshold 0.7)`（免费），与三颗存量合格件都不超 0.7 才继续投资源。
- `output_metric_1..4` 语义不明 ⇒ 不盲挖。
- 覆盖率 0.744–0.772 ⇒ 所有表达式必须带 `ts_backfill(·,250)`。
- VECTOR 字段必须先 `vec_avg` 变 MATRIX 才能进 `ts_*`。
