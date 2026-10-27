# news31 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news31` |
| 名称 | News Analytics on Equities |
| 类别 | NEWS |
| 数据字段数(平台) | 53 |
| 覆盖率 | 0.7991 |
| 平台已有 alpha | 105 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive analytics on news items related to equities, including sentiment, relevance, novelty, and volume scores for each asset mentioned in a news article. It covers over 80 fields, such as headline classification, asset identifiers, sentiment probabilities, and volume counts, enabling granular analysis of how news impacts individual companies and commodities. By quantifying the tone and relevance of news, as well as tracking the frequency and uniqueness of coverage, the dataset allows researchers and portfolio managers to assess the potential influence of news flow on price movements, identify momentum or reversal signals, and enhance predictive models for asset returns.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **53** |
| 类型分布 | VECTOR×53 |
| 平均覆盖率 | **0.799** |
| 覆盖率区间 | 0.74 ~ 0.91 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 16 | 30.2% |
| 中 (0.70–0.90) | 37 | 69.8% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 53 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 22 | 0.80 | nws31_d1_noveltycounts、nws31_d1_relevance、nws31_d1_sentimentnegative |
| 情绪与新闻 | 21 | 0.79 | nws31_d1_companycount、nws31_d1_sentencecount、nws31_d1_sentimentwordcount |
| 元数据与非信号 | 5 | 0.81 | nws31_d1_feedtimestamp_time、nws31_d1_firstcreated_time、nws31_audiences |
| 其他 | 4 | 0.79 | nws31_d1_bodysize、nws31_bodysize、nws31_linkedidvalues |
| 持仓与资金流 | 1 | 0.75 | nws31_linkedidpositions |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `nws31_d1_companycount` | VECTOR | 0.909 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of companies explicitly listed in the news item in the subjects field |
| 2 | `nws31_d1_feedtimestamp_time` | VECTOR | 0.909 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The time when the data was available on the feed |
| 3 | `nws31_d1_firstcreated_time` | VECTOR | 0.909 | 元数据与非信号 | 0 | — | — | — | UNTESTED | UTC timestamp for the first version of the story (time) |
| 4 | `nws31_d1_noveltycounts` | VECTOR | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | The number of similar items on a particular asset within 5 time windows. The periods are 12 hours, 24 hours, 3 days, 5 d |
| 5 | `nws31_d1_relevance` | VECTOR | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | The number indicating the relevance of the news item to the asset. It ranges from 0 to 1. |
| 6 | `nws31_d1_sentencecount` | VECTOR | 0.909 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The total number of sentences in the news item |
| 7 | `nws31_d1_sentimentnegative` | VECTOR | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the sentiment of the news item was negative for the asset |
| 8 | `nws31_d1_sentimentneutral` | VECTOR | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the sentiment of the news item was neutral for the asset |
| 9 | `nws31_d1_sentimentpositive` | VECTOR | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the sentiment of the news item was positive for the asset |
| 10 | `nws31_d1_sentimentwordcount` | VECTOR | 0.909 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of lexical tokens (words and punctuation) in the sections of the item text that are deemed relevant to the as |
| 11 | `nws31_d1_sourcetimestamp_time` | VECTOR | 0.909 | 情绪与新闻 | 0 | — | — | — | UNTESTED | UTC timestamp of this news item (time) |
| 12 | `nws31_d1_urgency` | VECTOR | 0.909 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Differentiates story types: 1: alert, 3: article |
| 13 | `nws31_d1_volumecounts` | VECTOR | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | The number of items on a particular asset within 5 time windows. The periods are 12 hours, 24 hours, 3 days, 5 days, and |
| 14 | `nws31_d1_wordcount` | VECTOR | 0.909 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The total number of lexical tokens (words and punctuation) in the news item. Can be used in conjunction with sentimentWo |
| 15 | `nws31_d1_bodysize` | VECTOR | 0.907 | 其他 | 0 | — | — | — | UNTESTED | The size of the current version of the story body in characters |
| 16 | `nws31_d1_firstmentionsentence` | VECTOR | 0.902 | 盈利与财务 | 0 | — | — | — | UNTESTED | The first sentence, starting with the headline, in which the scored asset is mentioned. Thus, a value of 1 denotes the h |
| 17 | `nws31_d1_sentimentclass` | VECTOR | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | This field indicates the predominant sentiment class for this news item with respect to this asset |
| 18 | `nws31_amertimestamp_time` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The time when the news arrived(American time) |
| 19 | `nws31_apactimestamp_time` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The time when the news arrived(Asian time) |
| 20 | `nws31_audiences` | VECTOR | 0.750 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Audience code |
| 21 | `nws31_bodysize` | VECTOR | 0.750 | 其他 | 0 | — | — | — | UNTESTED | The size of the current version of the story body in characters |
| 22 | `nws31_companycount` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of companies explicitly listed in the news item in the subjects field |
| 23 | `nws31_emeatimestamp_time` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The time when the news arrived(European time) |
| 24 | `nws31_feedtimestamp_time` | VECTOR | 0.750 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The time when the data was available on the feed |
| 25 | `nws31_firstcreated_time` | VECTOR | 0.750 | 元数据与非信号 | 0 | — | — | — | UNTESTED | UTC timestamp for the first version of the story(time) |
| 26 | `nws31_firstmentionsentence` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | The first sentence, starting with the headline, in which the scored asset is mentioned Thus, a value of 1 denotes the he |
| 27 | `nws31_linkedidpositions` | VECTOR | 0.750 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Position of the linkedId in the complete list of linked Ids 0 is the first/oldest, and the largest/most recent is the 7- |
| 28 | `nws31_linkedidvalues` | VECTOR | 0.750 | 其他 | 0 | — | — | — | UNTESTED | id of the item |
| 29 | `nws31_noveltycounts` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | The number of similar items on a particular asset within 5 time windows The periods are 12 hours, 24 hours, 3 days, 5 da |
| 30 | `nws31_relevance` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | The number indicating the relevance of the news item to the asset It ranges from 0 to 1 |
| 31 | `nws31_sentencecount` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The total number of sentences in the news item |
| 32 | `nws31_sentimentnegative` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the sentiment of the news item was negative for the asset |
| 33 | `nws31_sentimentneutral` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the sentiment of the news item was neutral for the asset |
| 34 | `nws31_sentimentpositive` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the sentiment of the news item was positive for the asset |
| 35 | `nws31_sentimentwordcount` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of lexical tokens (words and punctuation) in the sections of the item text that are deemed relevant to the as |
| 36 | `nws31_sourcetimestamp_time` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | UTC timestamp of this news item(time) |
| 37 | `nws31_subjects` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Topic codes and company identifiers that relate to this news item |
| 38 | `nws31_urgency` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Differentiates story types1: alert, 3: article |
| 39 | `nws31_volumecounts` | VECTOR | 0.750 | 盈利与财务 | 0 | — | — | — | UNTESTED | The number of items on a particular asset within 5 time windows The periods are 12 hours, 24 hours, 3 days, 5 days and 7 |
| 40 | `nws31_windows` | VECTOR | 0.750 | 其他 | 0 | — | — | — | UNTESTED | The windowed count group is used to associate a count with the window of time it relates to It is used for the noveltyCo |
| 41 | `nws31_wordcount` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The total number of lexical tokens (words and punctuation) in the news itemCan be used in conjunction with sentimentWord |
| 42 | `explicit_company_mention_count` | VECTOR | 0.742 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of companies specifically listed or scored in the subjects field of the news item |
| 43 | `first_appearance_sentence_number` | VECTOR | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Index of the first sentence (starting with headline as 1) in which the scored asset is mentioned in the news item |
| 44 | `negative_sentiment_probability_2` | VECTOR | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability (0-1) that the sentiment expressed in the news item is negative towards the asset |
| 45 | `neutral_sentiment_probability_2` | VECTOR | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability (0-1) that the sentiment expressed is neutral towards the asset |
| 46 | `news_relevance_score` | VECTOR | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | A value between 0 and 1 quantifying how relevant the news item is to the asset |
| 47 | `news_urgency_level` | VECTOR | 0.742 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Integer indicating news urgency (1 = alert/breaking, 3 = full article) |
| 48 | `positive_sentiment_probability_2` | VECTOR | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability (0-1) that the sentiment expressed is positive towards the asset |
| 49 | `predominant_sentiment_class` | VECTOR | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Primary sentiment classification for the news item regarding the asset (-1: negative, 0: neutral, 1: positive) |
| 50 | `sentiment_analysis_word_count` | VECTOR | 0.742 | 盈利与财务 | 0 | — | — | — | UNTESTED | Number of words and punctuation in text deemed relevant for sentiment scoring for the asset |
| 51 | `story_body_character_count` | VECTOR | 0.742 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of characters in the body of the current news story version |
| 52 | `total_sentence_count` | VECTOR | 0.742 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total number of sentences in the news item's body text |
| 53 | `total_word_token_count` | VECTOR | 0.742 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total number of lexical tokens (words, punctuation) in the news item |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS31-INSPECT-GATE-WALL`（2026-09-23T18:56:06）family=news31 事件/相似度分族：{"family": "news31 事件/相似度分族", "reason": "news31 体检硬门系统性拦截（单边恒正 monthly/quarterly 分数 raw 水平+短窗错配+稀疏未 trade_when），GEM 池两轮收敛后仍违规，零配额判死。根因=GEM 生成侧未消费字段画像。NEWS 塔在 pregate 修复前无供给。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-23T18:56:06", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；动用仍守 mode_b_qualification 资格线"}}

