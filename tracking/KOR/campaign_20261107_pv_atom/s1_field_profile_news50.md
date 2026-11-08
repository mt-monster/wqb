# 字段画像 · news50（KOR/TOP600/D1）

- 字段数: 71
- 类型: 全部 VECTOR（须 vec_* 聚合后才能进标量算子）
- 覆盖率: 绝大多数 0.6528
- 拥挤度: alphaCount 0-1（几乎无人使用）

| 字段 | 类型 | 覆盖 | alphaCount | 描述 |
|---|---|---:|---:|---|
| analyst_recommendation_change_score_d0 | VECTOR | 0.6528 | 0 | A score representing changes in analyst recommendations for an entity (D0 multicutoff variant). |
| analyst_recommendation_change_score_twn | VECTOR | 0.6528 | 1 | A score representing changes in analyst recommendations for an entity (TWN multicutoff variant). |
| composite_story_sentiment_score_d0 | VECTOR | 0.6528 | 0 | Composite Sentiment Score for the news item, typically 0–100 where higher values indicate more positive overal |
| composite_story_sentiment_score_twn | VECTOR | 0.6528 | 0 | Combined sentiment score for a news story using multiple analysis techniques (TWN multicutoff variant). |
| corporate_action_report_sentiment_score_d0 | VECTOR | 0.6528 | 0 | Sentiment score for news about corporate action announcements (D0 multicutoff variant). |
| corporate_action_report_sentiment_score_twn | VECTOR | 0.6528 | 1 | Sentiment score for news about corporate action announcements (TWN multicutoff variant). |
| earnings_evaluation_sentiment_score_d0 | VECTOR | 0.6528 | 1 | Sentiment score for news about earnings evaluations (D0 multicutoff variant). |
| earnings_evaluation_sentiment_score_twn | VECTOR | 0.6528 | 0 | Sentiment score for news about earnings evaluations (TWN multicutoff variant). |
| earnings_release_sentiment_score_d0 | VECTOR | 0.6528 | 0 | Sentiment score for news about earnings releases (D0 multicutoff variant). |
| earnings_release_sentiment_score_twn | VECTOR | 0.6528 | 0 | Sentiment score for news about earnings releases (TWN multicutoff variant). |
| editorial_commentary_sentiment_score_d0 | VECTOR | 0.6528 | 0 | Sentiment score for short commentary and editorials on equity markets (D0 multicutoff variant). |
| editorial_commentary_sentiment_score_twn | VECTOR | 0.6528 | 0 | Sentiment score for short commentary and editorials on equity markets (TWN multicutoff variant). |
| entity_record_count_per_story_d0 | VECTOR | 0.6528 | 0 | Total number of events in the story or event chain |
| entity_record_count_per_story_twn | VECTOR | 0.6528 | 0 | Total number of entity records published for a news story (TWN multicutoff variant). |
| entity_relevance_score_d0 | VECTOR | 0.6528 | 1 | Score from 0 to 100 indicating how central the entity is to the news story; higher means more relevant |
| entity_relevance_score_twn | VECTOR | 0.6528 | 0 | Relevance score (0–100) indicating how strongly the story relates to the entity; higher means more central |
| event_novelty_score_d0 | VECTOR | 0.6528 | 0 | Event Novelty Score (0–100) measuring how new the event is for the entity over a 24-hour window; higher means  |
| event_novelty_score_twn | VECTOR | 0.6528 | 0 | Event Novelty Score (0–100) measuring how new the story is within a 24-hour window |
| event_sentiment_score_d0 | VECTOR | 0.6528 | 1 | Event Sentiment Score from 0 to 100 measuring sentiment of the specific event; higher is more positive |
| event_sentiment_score_twn | VECTOR | 0.6528 | 0 | Event Sentiment Score (0–100) indicating the news sentiment for the entity; higher is more positive |
| global_equities_sentiment_score_d0 | VECTOR | 0.6528 | 1 | Sentiment score for global equities news based on positive, neutral, or negative tone (D0 multicutoff variant) |
| global_equities_sentiment_score_twn | VECTOR | 0.6528 | 0 | Sentiment score for global equities news based on positive, neutral, or negative tone (TWN multicutoff variant |
| global_event_novelty_score_d0 | VECTOR | 0.6528 | 0 | Global Event Novelty Score (0–100) measuring how new the event is in a global context over a 24-hour window |
| global_event_novelty_score_twn | VECTOR | 0.6528 | 0 | Global Event Novelty score (0–100) measuring how new the event is in a global context, typically over a 24-hou |
| global_novelty_elapsed_milliseconds_d0 | VECTOR | 0.6528 | 0 | Milliseconds between the first and current story in a global novelty chain (D0 multicutoff variant). |
| global_novelty_elapsed_milliseconds_twn | VECTOR | 0.6528 | 0 | Milliseconds between the first and current story in a global novelty chain (TWN multicutoff variant). |
| global_novelty_similarity_gap_days_d0 | VECTOR | 0.6528 | 1 | Number of days since a similar story was detected across all sources (D0 multicutoff variant). |
| global_novelty_similarity_gap_days_twn | VECTOR | 0.6528 | 0 | Number of days since a similar story was detected across all sources (TWN multicutoff variant). |
| merger_acquisition_sentiment_score_d0 | VECTOR | 0.6528 | 0 | Sentiment score for news about mergers, acquisitions, and takeovers (D0 multicutoff variant). |
| merger_acquisition_sentiment_score_twn | VECTOR | 0.6528 | 0 | Sentiment score for news about mergers, acquisitions, and takeovers (TWN multicutoff variant). |
| multi_classifier_equity_sentiment_score_d0 | VECTOR | 0.6528 | 0 | Sentiment score based on the tone for the most relevant companies in a story (D0 multicutoff variant). |
| multi_classifier_equity_sentiment_score_twn | VECTOR | 0.6528 | 0 | Sentiment score based on the tone for the most relevant companies in a story (TWN multicutoff variant). |
| mws50_acb | VECTOR | 0.6812 | 2 | Score representing sentiment according to the corporate actions classifier |
| mws50_bam | VECTOR | 0.6812 | 1 | Score representing sentiment according to the mergers and acquisitions classifier |
| mws50_bee | VECTOR | 0.6812 | 0 | Earnings evaluations sentiment score from the BEE classifier |
| mws50_ber | VECTOR | 0.6812 | 15 | Earnings releases sentiment score from the BER classifier specialized in earnings release news |
| mws50_category | VECTOR | 0.5389 | 12 | A unique tag to label, identify, and recognize a particular type and property of an entity-specific news event |
| mws50_country_code | VECTOR | 0.6812 | 1 | Two-character ISO-3166 country code associated with the entity (companies by incorporation, currencies by cent |
| mws50_ens_elapsed | VECTOR | 0.3484 | 0 | Milliseconds elapsed between the first story and the current story within the event novelty chain for this pac |
| mws50_ens_key | VECTOR | 0.5389 | 0 | An alphanumeric identifier that provides a way to chain or relate stories about the same categorized event for |
| mws50_ess | VECTOR | 0.3484 | 2 | Granular sentiment score from 0 to 100 for the entity in the story; higher values indicate more positive short |
| mws50_g_ens | VECTOR | 0.3484 | 1 | Global event novelty score from 0 to 100 indicating how new the story is within a 24 hour window across provid |
| mws50_g_ens_elapsed | VECTOR | 0.3484 | 4 | Milliseconds elapsed between the first and current story in the global event novelty chain across all news pro |
| mws50_g_ens_key | VECTOR | 0.5389 | 0 | An alphanumeric identifier that provides a way to chain or relate stories about the same categorized event for |
| mws50_ghc_lna | VECTOR | 0.6812 | 1 | Score representing changes in analyst recommendations |
| mws50_group | VECTOR | 0.5389 | 0 | A collection of related events. |
| mws50_maturity | VECTOR | 0.7855 | 2 | For events related to debt, this named attribute indicates the period of time for which a financial instrument |
| mws50_news_type | VECTOR | 0.6812 | 2 | Code classifying the type of news story or document (e.g., news, press release), per module codebook |
| mws50_nip | VECTOR | 0.6812 | 5 | News Impact Projections score (0–100) estimating market impact over the following two hours, conditional on ti |
| mws50_product_key | VECTOR | 0.5389 | 8 | Identifies which subscription package contains the record |
| mws50_property | VECTOR | 0.5389 | 0 | A named attribute of an event such as an entity, role, or string extracted from a matched event type. When app |
| mws50_qcm | VECTOR | 0.6812 | 1 | Multi-classifier for equities sentiment score combining outputs from BMQ, BEE, BCA, and ANL-CHG, applied to th |
| mws50_qmb | VECTOR | 0.6812 | 0 | Editorials & Commentary classifier score for the story (equities package) |
| mws50_relevance | VECTOR | 0.6812 | 1 | Score from 0 to 100 indicating how strongly the entity is related to the news story, with 100 meaning the enti |
| mws50_rp_story_event_count | VECTOR | 0.6812 | 1 | Total number of entity records (events) published by RavenPack for the given news story |
| mws50_rp_story_event_index | VECTOR | 0.6812 | 0 | Ordinal position of the entity record within a story, less than or equal to RP_STORY_EVENT_COUNT |
| mws50_ssc | VECTOR | 0.6812 | 10 | Composite sentiment score from 0 to 100 representing overall story sentiment |
| mws50_topic | VECTOR | 0.5389 | 3 | A subject or theme of events detected |
| mws50_vea | VECTOR | 0.6812 | 2 | Aggregate Event Volume over the past 91 days for an entity, counting non-neutral events (ESS ≠ 50) from qualif |
| news_story_classification_2 | VECTOR | 0.6528 | 0 | Classification of a news story, such as breaking news, full article, or press release. |
| news_story_classification_d0 | VECTOR | 0.6528 | 0 | Classification of a news story, such as breaking news, full article, or press release (D0 multicutoff variant) |
| news_volatility_projection_score_d0 | VECTOR | 0.6528 | 0 | News Impact Projection score estimating the expected market impact of the news |
| news_volatility_projection_score_twn | VECTOR | 0.6528 | 0 | A score estimating the impact of a news flash on short-term market volatility (TWN multicutoff variant). |
| non_neutral_event_count_rolling_window_d0 | VECTOR | 0.6528 | 0 | Count of non-neutral events for an entity over a rolling 91-day window (D0 multicutoff variant). |
| non_neutral_event_count_rolling_window_twn | VECTOR | 0.6528 | 0 | Count of non-neutral events for an entity over a rolling 91-day window (TWN multicutoff variant). |
| novelty_elapsed_milliseconds_d0 | VECTOR | 0.6528 | 0 | Milliseconds between the first and current story in an event novelty chain (D0 multicutoff variant). |
| novelty_elapsed_milliseconds_twn | VECTOR | 0.6528 | 1 | Milliseconds between the first and current story in an event novelty chain (TWN multicutoff variant). |
| novelty_similarity_gap_days_d0 | VECTOR | 0.6528 | 0 | Event-level novelty similarity gap between 0 and 1 indicating similarity to prior events; lower values suggest |
| novelty_similarity_gap_days_twn | VECTOR | 0.6528 | 1 | Number of days since a similar story was detected in a specific data package (TWN multicutoff variant). |
| positive_event_ratio_score_d0 | VECTOR | 0.6528 | 0 | Ratio of positive to total non-neutral events for an entity over a rolling window (D0 multicutoff variant). |
| positive_event_ratio_score_twn | VECTOR | 0.6528 | 0 | Ratio of positive to total non-neutral events for an entity over a rolling window (TWN multicutoff variant). |