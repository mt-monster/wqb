# news20 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news20` |
| 名称 | Web Sources News Sentiment Data |
| 类别 | NEWS |
| 数据字段数(平台) | 68 |
| 覆盖率 | 0.8079 |
| 平台已有 alpha | 55 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping and reference framework for entities and events detected in financial news and analytics. It includes unique identifiers for entities (such as companies, currencies, commodities, places, and people), their relationships, roles, and associated metadata like country codes and security identifiers. The dataset also covers event taxonomy, sentiment scores, relevance, novelty, and aggregation functions, enabling users to link news events to specific entities and analyze their impact. By offering granular mapping and classification, this dataset is essential for integrating news analytics with other financial datasets, supporting event-driven research, and enhancing predictive models for price movements through improved entity resolution and event ca

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **68** |
| 类型分布 | VECTOR×68 |
| 平均覆盖率 | **0.808** |
| 覆盖率区间 | 0.26 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 20 | 29.4% |
| 中 (0.70–0.90) | 42 | 61.8% |
| 低 (0.50–0.70) | 3 | 4.4% |
| 稀疏 (<0.50) | 3 | 4.4% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 63 | 92.6% |
| UNUSABLE | 5 | 7.4% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 63 / UNUSABLE 5 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 35 | 0.81 | nws20_multiple_comp_rp_story_event_index、nws20_multiple_comp_bam、nws20_multiple_comp_ghc_lna |
| 其他 | 22 | 0.80 | nws20_multiple_comp_rp_story_event_count、nws20_multiple_comp_reporting_end_time_utc、nws20_multiple_comp_reporting_start_time_utc |
| 盈利与财务 | 5 | 0.83 | nws20_multiple_comp_acb、nws20_multiple_comp_bee、nws20_multiple_comp_d1_event_similarity_days |
| 修正与预期 | 3 | 0.81 | nws20_multiple_comp_ber、nws20_multiple_comp_d1_ber、nws20_ber |
| 宏观与行业 | 3 | 0.84 | nws20_multiple_comp_country_code、nws20_multiple_comp_d1_country_code、nws20_country_code |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `nws20_multiple_comp_rp_story_event_index` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count or index indicating the total number of entity records published within a news story (position in story chain) |
| 2 | `nws20_multiple_comp_rp_story_event_count` | VECTOR | 0.999 | 其他 | 0 | — | — | — | UNTESTED | Identifies which content set the record came from |
| 3 | `nws20_multiple_comp_acb` | VECTOR | 0.963 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sentiment score from a classifier specialized in earnings release news |
| 4 | `nws20_multiple_comp_bam` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment score from a classifier focused on corporate action announcements |
| 5 | `nws20_multiple_comp_bee` | VECTOR | 0.963 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sentiment score from a classifier specialized in earnings evaluations and related news stories |
| 6 | `nws20_multiple_comp_ber` | VECTOR | 0.963 | 修正与预期 | 0 | — | — | — | UNTESTED | Numerical score representing the magnitude of a change in analyst recommendation |
| 7 | `nws20_multiple_comp_country_code` | VECTOR | 0.963 | 宏观与行业 | 0 | — | — | — | UNTESTED | The two character ISO-3166 country code associated with the entity referenced in the event |
| 8 | `nws20_multiple_comp_ghc_lna` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment based on the tone; applicable only towards the most relevant entities mention |
| 9 | `nws20_multiple_comp_nip` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score between -1.00 and 1.00 representing degree of impact the news has on the market over the next two hours |
| 10 | `nws20_multiple_comp_qcm` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the order in which entity records are published per news story |
| 11 | `nws20_multiple_comp_qep` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that specializes in identifying positive and negative words and phrases in articles |
| 12 | `nws20_multiple_comp_qmb` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment score from a classifier specializing in news about mergers, acquisitions, and takeovers |
| 13 | `nws20_multiple_comp_relevance` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | An integer score between 0-100 that indicates how strongly related the mention of an entity is to the underlying news st |
| 14 | `nws20_multiple_comp_reporting_end_time_utc` | VECTOR | 0.963 | 其他 | 0 | — | — | — | UNTESTED | End time of the reporting period associated with the event in UTC |
| 15 | `nws20_multiple_comp_reporting_start_time_utc` | VECTOR | 0.963 | 其他 | 0 | — | — | — | UNTESTED | Beginning time in UTC of the reporting period pertinent to the event (e.g., fiscal period start) |
| 16 | `nws20_multiple_comp_ssc` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Granular sentiment score between -1.00 and +1.00 representing the combined news sentiment of the story |
| 17 | `nws20_multiple_comp_timestamp_utc_time` | VECTOR | 0.963 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Time when the news item was received in UTC |
| 18 | `nws20_multiple_comp_event_relevance` | VECTOR | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Integer between 0-100 reflecting the relevance of the event in the story |
| 19 | `nws20_multiple_comp_event_sentiment_score` | VECTOR | 0.960 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Granular sentiment score between -1.00 and +1.00 (net positive/negative sentiment) reflecting the tone of news regarding |
| 20 | `nws20_multiple_comp_event_similarity_days` | VECTOR | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Number of days (up to 5 decimals) since a similar event was last observed within the past 365 days; reflects novelty or |
| 21 | `nws20_multiple_comp_d1_country_code` | VECTOR | 0.844 | 宏观与行业 | 0 | — | — | — | UNTESTED | The two-character ISO-3166 country code associated with an entity |
| 22 | `nws20_multiple_comp_d1_event_text` | VECTOR | 0.844 | 其他 | 0 | — | — | — | UNTESTED | A short text summary of an event captured in a document |
| 23 | `nws20_multiple_comp_d1_headline` | VECTOR | 0.844 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The headline or summary text for the document |
| 24 | `nws20_multiple_comp_d1_rp_story_event_count` | VECTOR | 0.844 | 其他 | 0 | — | — | — | UNTESTED | Identifies which content set the record came from |
| 25 | `nws20_multiple_comp_d1_rp_story_event_index` | VECTOR | 0.844 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the total entity records published per news story |
| 26 | `nws20_multiple_comp_d1_timestamp_utc_time` | VECTOR | 0.844 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The time at which the news item was received |
| 27 | `nws20_multiple_comp_d1_event_end_time_utc` | VECTOR | 0.844 | 其他 | 0 | — | — | — | UNTESTED | The time when the event ends in UTC |
| 28 | `nws20_multiple_comp_d1_event_relevance` | VECTOR | 0.844 | 其他 | 0 | — | — | — | UNTESTED | An integer between 0-100 that reflects the relevance of the event in the story |
| 29 | `nws20_multiple_comp_d1_event_start_time_utc` | VECTOR | 0.844 | 其他 | 0 | — | — | — | UNTESTED | The time when the event starts in UTC |
| 30 | `nws20_multiple_comp_d1_relevance` | VECTOR | 0.843 | 情绪与新闻 | 0 | — | — | — | UNTESTED | An integer score between 0-100 that indicates how strongly related the mention of an entity is to the underlying news st |
| 31 | `nws20_multiple_comp_d1_nip` | VECTOR | 0.843 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and 1.00 with up to 2 decimal places that represents the degree of impact a news flash ha |
| 32 | `nws20_multiple_comp_d1_reporting_end_time_utc` | VECTOR | 0.842 | 其他 | 0 | — | — | — | UNTESTED | The end time of the reporting period associated with the event |
| 33 | `nws20_multiple_comp_d1_reporting_start_time_utc` | VECTOR | 0.842 | 其他 | 0 | — | — | — | UNTESTED | The start time of the reporting period associated with the event |
| 34 | `nws20_rp_story_event_index` | VECTOR | 0.838 | 其他 | 0 | — | — | — | UNTESTED | Sequential index of this entity event within the provider story’s set of entity events |
| 35 | `nws20_multiple_comp_d1_ssc` | VECTOR | 0.822 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and +1.00 with up to 2 decimal places that represents the news sentiment of a given story |
| 36 | `nws20_multiple_comp_d1_qmb` | VECTOR | 0.809 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment about mergers, acquisitions, and takeovers |
| 37 | `nws20_event_relevance` | VECTOR | 0.801 | 其他 | 0 | — | — | — | UNTESTED | An integer between 0-100 reflecting how relevant the event is in the context of the story, with higher values showing gr |
| 38 | `nws20_event_sentiment_score` | VECTOR | 0.801 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score from -1.00 to +1.00 quantifying the sentiment of the news event for the entity (negative to positive) |
| 39 | `nws20_event_similarity_days` | VECTOR | 0.801 | 其他 | 0 | — | — | — | UNTESTED | Number of days since a similar event occurred, used to measure event novelty |
| 40 | `nws20_rp_story_event_count` | VECTOR | 0.777 | 其他 | 0 | — | — | — | UNTESTED | Total number of entity events or records associated with the provider story |
| 41 | `nws20_multiple_comp_d1_qep` | VECTOR | 0.769 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that specializes in identifying positive and negative words and phrases in articles |
| 42 | `nws20_multiple_comp_d1_event_similarity_days` | VECTOR | 0.765 | 盈利与财务 | 0 | — | — | — | UNTESTED | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity fo |
| 43 | `nws20_multiple_comp_d1_acb` | VECTOR | 0.762 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given story according to a classifier, which specializes in news stori |
| 44 | `nws20_multiple_comp_d1_qcm` | VECTOR | 0.757 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the order in which entity records are published per news story |
| 45 | `nws20_multiple_comp_d1_ber` | VECTOR | 0.752 | 修正与预期 | 0 | — | — | — | UNTESTED | A score that represents a change in recommendation by an analyst firm in the form of a numerical score |
| 46 | `nws20_multiple_comp_d1_event_sentiment_score` | VECTOR | 0.749 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and +1.00 with 2 decimal places that represents the news sentiment for a given entity by |
| 47 | `nws20_acb` | VECTOR | 0.718 | 盈利与财务 | 0 | — | — | — | UNTESTED | A sentiment score for news about earnings releases via the BER classifier; values: -1 = negative, 0 = neutral, 1 = posit |
| 48 | `nws20_bam` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Score for news sentiment of the story, based on a classifier specializing in corporate action announcements |
| 49 | `nws20_bee` | VECTOR | 0.718 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score (-1, 0, or 1) representing sentiment for earnings-related news, assigned by the BEE classifier |
| 50 | `nws20_ber` | VECTOR | 0.718 | 修正与预期 | 0 | — | — | — | UNTESTED | Numeric score representing a change in recommendation by an analyst firm |
| 51 | `nws20_country_code` | VECTOR | 0.718 | 宏观与行业 | 0 | — | — | — | UNTESTED | Two character ISO-3166 country code associated with the entity |
| 52 | `nws20_ghc_lna` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score representing the change in news sentiment, based on tone analysis, particularly relevant to the most important e |
| 53 | `nws20_nip` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score ranging from -1.00 to 1.00 estimating the degree of market impact a news flash will have in the next tw |
| 54 | `nws20_qcm` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the order in which entity records are published per news story, likely used for indexing of entities across a |
| 55 | `nws20_qep` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score specializing in identifying positive and negative wording in news articles, reflecting overall sentiment of lang |
| 56 | `nws20_qmb` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A sentiment score for news about M&A activity, based on the BAM classifier; values: -1 = negative, 0 = neutral, 1 = posi |
| 57 | `nws20_relevance` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Integer score (0-100) showing how strongly the entity mention is related to the news story, higher means more relevant |
| 58 | `nws20_reporting_end_time_utc` | VECTOR | 0.718 | 其他 | 0 | — | — | — | UNTESTED | End time of the reporting period associated with the event (in UTC) |
| 59 | `nws20_reporting_start_time_utc` | VECTOR | 0.718 | 其他 | 0 | — | — | — | UNTESTED | Start time of the reporting period associated with the event, in UTC |
| 60 | `nws20_ssc` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A detailed sentiment score between -1.00 and +1.00 (two decimal places), combining multiple sentiment analysis methods t |
| 61 | `nws20_timestamp_utc_time` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Time at which the news item was received, in UTC |
| 62 | `nws20_multiple_comp_d1_bee` | VECTOR | 0.710 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given story according to a classifier, which specializes in news stori |
| 63 | `nws20_multiple_comp_d1_bam` | VECTOR | 0.604 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given news story according to a classifier, which specializes in repor |
| 64 | `nws20_multiple_comp_event_end_time_utc` | VECTOR | 0.568 | 其他 | 0 | — | — | — | UNUSABLE | The specific time in UTC when the event concluded or finished |
| 65 | `nws20_multiple_comp_event_start_time_utc` | VECTOR | 0.568 | 其他 | 0 | — | — | — | UNUSABLE | Time in UTC when the event starts |
| 66 | `nws20_event_end_time_utc` | VECTOR | 0.480 | 其他 | 0 | — | — | — | UNUSABLE | Time when the event ends, in UTC |
| 67 | `nws20_event_start_time_utc` | VECTOR | 0.480 | 其他 | 0 | — | — | — | UNUSABLE | Time when the event starts, in UTC |
| 68 | `nws20_multiple_comp_d1_ghc_lna` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score that represents the news sentiment based on the tone; applicable only towards the most relevant entities mention |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS20-INSPECT-GATE-WALL`（2026-09-23T18:56:06）family=news20 multiple_comp 事件分族：{"family": "news20 multiple_comp 事件分族", "reason": "news20 体检硬门系统性拦截（单边恒正 monthly/quarterly 分数 raw 水平+短窗错配+稀疏未 trade_when），GEM 池两轮收敛后仍违规，零配额判死。根因=GEM 生成侧未消费字段画像。NEWS 塔在 pregate 修复前无供给。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-23T18:56:06", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；动用仍守 mode_b_qualification

