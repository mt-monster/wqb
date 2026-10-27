# news17 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news17` |
| 名称 | PR Edition Data |
| 类别 | NEWS |
| 数据字段数(平台) | 88 |
| 覆盖率 | 0.7824 |
| 平台已有 alpha | 94 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset analyzes and structures news, press releases, and regulatory disclosures from over 22 global newswires and distribution networks, processing more than 100,000 items daily. It provides granular sentiment scores, event relevance, novelty metrics, and impact projections for entities such as companies, currencies, and commodities. The data includes detailed event taxonomy, entity mapping, and various sentiment indicators, enabling users to track market-moving news, measure the impact and novelty of events, and assess the relevance of information to specific securities. By quantifying news sentiment and event characteristics, the dataset helps investors and analysts anticipate price movements, identify alpha opportunities, and enhance risk management through timely, data-driven ins

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **88** |
| 类型分布 | VECTOR×88 |
| 平均覆盖率 | **0.782** |
| 覆盖率区间 | 0.26 ~ 0.98 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 31 | 35.2% |
| 中 (0.70–0.90) | 25 | 28.4% |
| 低 (0.50–0.70) | 26 | 29.5% |
| 稀疏 (<0.50) | 6 | 6.8% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 80 | 90.9% |
| UNUSABLE | 8 | 9.1% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 80 / UNUSABLE 8 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 47 | 0.78 | nws17_multiple_comp_d1_headline、nws17_multiple_comp_d1_rp_story_event_count、nws17_multiple_comp_d1_rp_story_event_index |
| 其他 | 24 | 0.78 | nws17_multiple_comp_d1_event_relevance、nws17_multiple_comp_d1_event_text、nws17_multiple_comp_d1_event_end_time_utc |
| 修正与预期 | 5 | 0.74 | analyst_recommendation_change_score、nws17_multiple_comp_ber、nws17_multiple_comp_d1_ber |
| 盈利与财务 | 5 | 0.76 | nws17_multiple_comp_acb、nws17_multiple_comp_bee、nws17_comp_d1_event_similarity_days |
| 宏观与行业 | 4 | 0.85 | nws17_multiple_comp_d1_country_code、nws17_multiple_comp_country_code、nws17_comp_d1_country_code |
| 风险与质量 | 2 | 0.78 | nws17_multiple_comp_relevance、nws17_relevance |
| 交易与微观结构 | 1 | 0.96 | nws17_multiple_comp_rp_story_event_index |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `nws17_multiple_comp_d1_country_code` | VECTOR | 0.981 | 宏观与行业 | 0 | — | — | — | UNTESTED | The two-character ISO-3166 country code associated with an entity. Companies and organizations are associated with the c |
| 2 | `nws17_multiple_comp_d1_event_relevance` | VECTOR | 0.981 | 其他 | 0 | — | — | — | UNTESTED | An integer between 0-100 that reflects the relevance of the event in the story |
| 3 | `nws17_multiple_comp_d1_event_text` | VECTOR | 0.981 | 其他 | 0 | — | — | — | UNTESTED | A short text summary of an event captured in a document |
| 4 | `nws17_multiple_comp_d1_headline` | VECTOR | 0.981 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The headline or summary text for the document |
| 5 | `nws17_multiple_comp_d1_rp_story_event_count` | VECTOR | 0.981 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the total entity records published by the vendor per news story |
| 6 | `nws17_multiple_comp_d1_rp_story_event_index` | VECTOR | 0.981 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the order in which entity records are published by vendor per news story. This integer can be equal to or les |
| 7 | `nws17_multiple_comp_d1_timestamp_utc_time` | VECTOR | 0.981 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Time of news arrival as received by WorldQuant |
| 8 | `nws17_multiple_comp_d1_event_end_time_utc` | VECTOR | 0.981 | 其他 | 0 | — | — | — | UNTESTED | The time when the event ends in UTC. |
| 9 | `nws17_multiple_comp_d1_event_start_time_utc` | VECTOR | 0.981 | 其他 | 0 | — | — | — | UNTESTED | The time when the event starts in UTC. |
| 10 | `nws17_multiple_comp_d1_reporting_end_time_utc` | VECTOR | 0.981 | 其他 | 0 | — | — | — | UNTESTED | The end time of the reporting period associated with the event. |
| 11 | `nws17_multiple_comp_d1_reporting_start_time_utc` | VECTOR | 0.981 | 其他 | 0 | — | — | — | UNTESTED | The start time of the reporting period associated with the event. |
| 12 | `nws17_multiple_comp_d1_nip` | VECTOR | 0.980 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and 1.00 with up to 2 decimal places that represents the degree of impact a news flash ha |
| 13 | `nws17_multiple_comp_d1_relevance` | VECTOR | 0.979 | 情绪与新闻 | 0 | — | — | — | UNTESTED | An integer score between 0-100 that indicates how strongly related the mention of an entity is to the underlying news st |
| 14 | `nws17_multiple_comp_rp_story_event_count` | VECTOR | 0.960 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total number of entity records published by the vendor for the news story |
| 15 | `nws17_multiple_comp_rp_story_event_index` | VECTOR | 0.960 | 交易与微观结构 | 0 | — | — | — | UNTESTED | Order index of this entity record within the vendor’s set of events for the story |
| 16 | `nws17_multiple_comp_d1_ssc` | VECTOR | 0.930 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and +1.00 with up to 2 decimal places that represents the news sentiment of a given story |
| 17 | `analyst_recommendation_change_score` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | A score representing changes in analyst recommendations, such as upgrade or downgrade. |
| 18 | `nws17_multiple_comp_acb` | VECTOR | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sentiment score for earnings release stories: -1 negative, 0 neutral, 1 positive |
| 19 | `nws17_multiple_comp_bam` | VECTOR | 0.905 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given news story according to the BCA classifier, which specializes in |
| 20 | `nws17_multiple_comp_bee` | VECTOR | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sentiment score for earnings evaluation stories: -1 negative, 0 neutral, 1 positive |
| 21 | `nws17_multiple_comp_ber` | VECTOR | 0.905 | 修正与预期 | 0 | — | — | — | UNTESTED | Score for analyst recommendation change: -1 downgrade, 0 no change, 1 upgrade |
| 22 | `nws17_multiple_comp_country_code` | VECTOR | 0.905 | 宏观与行业 | 0 | — | — | — | UNTESTED | Two-character ISO-3166 country code associated with the entity; ‘XX’ for global entities not tied to a specific country |
| 23 | `nws17_multiple_comp_nip` | VECTOR | 0.905 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Granular impact score from -1.00 to 1.00 estimating how the news affects the market over the next two hours |
| 24 | `nws17_multiple_comp_qcm` | VECTOR | 0.905 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Tone-based sentiment score applicable to the most relevant entities, derived from BMQ, BEE, BCA, and ANL-CHG analytics |
| 25 | `nws17_multiple_comp_qep` | VECTOR | 0.905 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment score based on positive and negative words or phrases in global equities articles |
| 26 | `nws17_multiple_comp_qmb` | VECTOR | 0.905 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given story according to the BAM classifier, which specializes in news |
| 27 | `nws17_multiple_comp_relevance` | VECTOR | 0.905 | 风险与质量 | 0 | — | — | — | UNTESTED | Integer score from 0 to 100 indicating how prominent the entity is in the story (higher means more relevant) |
| 28 | `nws17_multiple_comp_reporting_end_time_utc` | VECTOR | 0.905 | 其他 | 0 | — | — | — | UNTESTED | End time of the reporting period associated with the event in UTC |
| 29 | `nws17_multiple_comp_reporting_start_time_utc` | VECTOR | 0.905 | 其他 | 0 | — | — | — | UNTESTED | UTC start time of the reporting period associated with the event |
| 30 | `nws17_multiple_comp_ssc` | VECTOR | 0.905 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Continuous sentiment score from -1.00 to +1.00 (two decimals) summarizing story sentiment |
| 31 | `nws17_multiple_comp_timestamp_utc_time` | VECTOR | 0.905 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Time of news arrival as received by WorldQuant (UTC) |
| 32 | `nws17_multiple_comp_d1_qmb` | VECTOR | 0.884 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given story according to the BAM classifier, which specializes in news |
| 33 | `nws17_comp_d1_country_code` | VECTOR | 0.853 | 宏观与行业 | 0 | — | — | — | UNTESTED | The two-character ISO-3166 country code associated with an entity. Companies and organizations are associated with the c |
| 34 | `nws17_comp_d1_event_relevance` | VECTOR | 0.853 | 其他 | 0 | — | — | — | UNTESTED | An integer between 0-100 that reflects the relevance of the event in the story |
| 35 | `nws17_comp_d1_event_text` | VECTOR | 0.853 | 其他 | 0 | — | — | — | UNTESTED | A short text summary of an event captured in a document |
| 36 | `nws17_comp_d1_headline` | VECTOR | 0.853 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The headline or summary text for the document. |
| 37 | `nws17_comp_d1_rp_story_event_count` | VECTOR | 0.853 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the total entity records published by vendor per news story |
| 38 | `nws17_comp_d1_rp_story_event_index` | VECTOR | 0.853 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Represents the order in which entity records are published by the vendor per news story. This integer can be equal to or |
| 39 | `nws17_comp_d1_timestamp_utc_time` | VECTOR | 0.853 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Time of news arrival as received by WorldQuant |
| 40 | `nws17_comp_d1_event_end_time_utc` | VECTOR | 0.853 | 其他 | 0 | — | — | — | UNTESTED | The time when the event ends in UTC. |
| 41 | `nws17_comp_d1_event_start_time_utc` | VECTOR | 0.853 | 其他 | 0 | — | — | — | UNTESTED | The time when the event starts in UTC. |
| 42 | `nws17_comp_d1_reporting_end_time_utc` | VECTOR | 0.852 | 其他 | 0 | — | — | — | UNTESTED | The end time of the reporting period associated with the event. |
| 43 | `nws17_comp_d1_reporting_start_time_utc` | VECTOR | 0.852 | 其他 | 0 | — | — | — | UNTESTED | The start time of the reporting period associated with the event. |
| 44 | `nws17_comp_d1_nip` | VECTOR | 0.852 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and 1.00 with up to 2 decimal places that represents the degree of impact a news flash ha |
| 45 | `nws17_comp_d1_relevance` | VECTOR | 0.850 | 情绪与新闻 | 0 | — | — | — | UNTESTED | An integer score between 0-100 that indicates how strongly related the mention of an entity is to the underlying news st |
| 46 | `nws17_multiple_comp_event_relevance` | VECTOR | 0.833 | 其他 | 0 | — | — | — | UNTESTED | Integer 0–100 indicating how relevant the event is within the story |
| 47 | `nws17_multiple_comp_event_sentiment_score` | VECTOR | 0.833 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment polarity score between -1.00 and +1.00 measuring news sentiment for the entity |
| 48 | `nws17_multiple_comp_event_similarity_days` | VECTOR | 0.833 | 其他 | 0 | — | — | — | UNTESTED | Number of days (0 to 365, with decimals) since a similar event was last detected |
| 49 | `nws17_multiple_comp_d1_qep` | VECTOR | 0.818 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given news item according to the PEQ classifier, which specializes in |
| 50 | `nws17_comp_d1_ssc` | VECTOR | 0.804 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and +1.00 with up to 2 decimal places that represents the news sentiment of a given story |
| 51 | `nws17_multiple_comp_d1_event_similarity_days` | VECTOR | 0.801 | 其他 | 0 | — | — | — | UNTESTED | A granular number with up to 5 decimal places which indicates the number of days since a similar event was detected over |
| 52 | `nws17_multiple_comp_d1_event_sentiment_score` | VECTOR | 0.781 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and +1.00 with 2 decimal places that represents the news sentiment for a given entity by |
| 53 | `nws17_comp_d1_qmb` | VECTOR | 0.760 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given story according to the BAM classifier, which specializes in news |
| 54 | `nws17_rp_story_event_count` | VECTOR | 0.741 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total number of entity records published by RavenPack for the news story |
| 55 | `nws17_rp_story_event_index` | VECTOR | 0.741 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Order index of the entity record within the vendor’s sequence for a news story |
| 56 | `nws17_multiple_comp_d1_qcm` | VECTOR | 0.719 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment based on the tone; applicable only towards the most relevant entities mention |
| 57 | `nws17_comp_d1_qep` | VECTOR | 0.699 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given news item according to the PEQ classifier, which specializes in |
| 58 | `nws17_comp_d1_event_similarity_days` | VECTOR | 0.686 | 盈利与财务 | 0 | — | — | — | UNTESTED | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity fo |
| 59 | `nws17_event_sentiment_score` | VECTOR | 0.682 | 情绪与新闻 | 0 | — | — | — | UNTESTED | -1.00 to +1.00 sentiment score for the entity based on news analytics |
| 60 | `nws17_multiple_comp_d1_ber` | VECTOR | 0.667 | 修正与预期 | 0 | — | — | — | UNTESTED | A score that represents a change in recommendation by an analyst firm in the form of a numerical score. When the mention |
| 61 | `nws17_comp_d1_event_sentiment_score` | VECTOR | 0.667 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A granular score between -1.00 and +1.00 with 2 decimal places that represents the news sentiment for a given entity by |
| 62 | `nws17_acb` | VECTOR | 0.664 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings-focused sentiment classifier score: -1 negative, 0 neutral, 1 positive |
| 63 | `nws17_bam` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | BCA classifier sentiment score for corporate action reports: -1 negative, 0 neutral, 1 positive |
| 64 | `nws17_bee` | VECTOR | 0.664 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sentiment score from the earnings evaluations classifier, values -1 (negative), 0 (neutral), or 1 (positive) |
| 65 | `nws17_ber` | VECTOR | 0.664 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst recommendation change score for the company mention when an ANL-CHG event is detected: -1 downgrade, 0 neutral, |
| 66 | `nws17_country_code` | VECTOR | 0.664 | 宏观与行业 | 0 | — | — | — | UNTESTED | Two-letter ISO-3166 country code associated with the entity (XX for global entities) |
| 67 | `nws17_ghc_lna` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A sentiment score based on tone for the most relevant entities, derived from BMQ, BEE, BCA, and ANL-CHG classifiers |
| 68 | `nws17_nip` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | -1.00 to 1.00 score estimating market impact over the next two hours after the news flash |
| 69 | `nws17_qcm` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Composite tone-based sentiment score for the most relevant entities, derived from BMQ, BEE, BCA, and ANL-CHG |
| 70 | `nws17_qep` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment score from the PEQ classifier focused on equities-related positive/negative language |
| 71 | `nws17_qmb` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | M&A/takeover sentiment score: -1 negative, 0 neutral, 1 positive |
| 72 | `nws17_relevance` | VECTOR | 0.664 | 风险与质量 | 0 | — | — | — | UNTESTED | 0–100 score indicating how central the entity is to the story; higher means more relevant |
| 73 | `nws17_reporting_end_time_utc` | VECTOR | 0.664 | 其他 | 0 | — | — | — | UNTESTED | UTC time marking the end of the reporting period referenced by the event |
| 74 | `nws17_reporting_start_time_utc` | VECTOR | 0.664 | 其他 | 0 | — | — | — | UNTESTED | UTC start time of the reporting period associated with the event |
| 75 | `nws17_ssc` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Continuous sentiment score from -1.00 to +1.00 (two decimals) combining multiple techniques |
| 76 | `nws17_timestamp_utc_time` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | UTC time the news arrived as received by WorldQuant |
| 77 | `nws17_multiple_comp_d1_acb` | VECTOR | 0.652 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment of the given story according to the BER classifier, which specializes in news |
| 78 | `nws17_event_relevance` | VECTOR | 0.634 | 其他 | 0 | — | — | — | UNTESTED | Integer 0–100 indicating how relevant the event is within the story |
| 79 | `nws17_event_similarity_days` | VECTOR | 0.634 | 其他 | 0 | — | — | — | UNTESTED | Days since a similar event occurred within the last 365 days (0 to 365, up to 5 decimals) |
| 80 | `nws17_comp_d1_qcm` | VECTOR | 0.610 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A score that represents the news sentiment based on the tone; applicable only towards the most relevant entities mention |
| 81 | `nws17_comp_d1_ber` | VECTOR | 0.558 | 修正与预期 | 0 | — | — | — | UNUSABLE | A score that represents a change in recommendation by an analyst firm in the form of a numerical score. When the mention |
| 82 | `nws17_comp_d1_acb` | VECTOR | 0.544 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score that represents the news sentiment of the given story according to the BER classifier, which specializes in news |
| 83 | `nws17_multiple_comp_d1_bee` | VECTOR | 0.492 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score that represents the news sentiment of the given story according to the BEE classifier, which specializes in news |
| 84 | `nws17_comp_d1_bee` | VECTOR | 0.397 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score that represents the news sentiment of the given story according to the BEE classifier, which specializes in news |
| 85 | `nws17_multiple_comp_event_end_time_utc` | VECTOR | 0.317 | 其他 | 0 | — | — | — | UNUSABLE | Time when the event ends in UTC |
| 86 | `nws17_multiple_comp_event_start_time_utc` | VECTOR | 0.317 | 其他 | 0 | — | — | — | UNUSABLE | The time when the event starts in Coordinated Universal Time (UTC) |
| 87 | `nws17_event_start_time_utc` | VECTOR | 0.269 | 其他 | 0 | — | — | — | UNUSABLE | Time when the event starts, in UTC |
| 88 | `nws17_multiple_comp_d1_bam` | VECTOR | 0.259 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score that represents the news sentiment of the given news story according to the BCA classifier, which specializes in |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS17-INSPECT-GATE-WALL`（2026-09-23T18:56:06）family=news17 comp_d1 分数族：{"family": "news17 comp_d1 分数族", "reason": "news17 体检硬门系统性拦截（单边恒正 monthly/quarterly 分数 raw 水平+短窗错配+稀疏未 trade_when），GEM 池两轮收敛后仍违规，零配额判死。根因=GEM 生成侧未消费字段画像。NEWS 塔在 pregate 修复前无供给。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "sealed_at": "2026-09-23T18:56:06", "note": "seal_dead_end 沉降：供 Mode B 组合腿救援消费（get_salvage_pool）；动用仍守 mode_b_qualification 资格线"}}

