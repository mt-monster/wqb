# news18 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news18` |
| 名称 | Ravenpack News Data |
| 类别 | NEWS |
| 数据字段数(平台) | 124 |
| 覆盖率 | 0.61 |
| 平台已有 alpha | 636 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides structured analytics derived from global news sources, focusing on sentiment, event detection, and entity relevance for financial markets. It includes granular sentiment scores for specific events and entities, measures of event novelty and relevance, and a comprehensive taxonomy for classifying news events. The data covers a wide range of entities such as companies, products, people, and macroeconomic factors, and is enriched with metadata like event timing, fact level, and source trustworthiness. By quantifying the tone and impact of news stories, this dataset enables investors and researchers to systematically monitor market sentiment, identify significant events, and generate predictive signals for price movements, making it a valuable tool for quantitative tradin

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **124** |
| 类型分布 | VECTOR×65　MATRIX×59 |
| 平均覆盖率 | **0.610** |
| 覆盖率区间 | 0.33 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 20 | 16.1% |
| 中 (0.70–0.90) | 20 | 16.1% |
| 低 (0.50–0.70) | 63 | 50.8% |
| 稀疏 (<0.50) | 21 | 16.9% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 81 | 65.3% |
| UNTESTED | 43 | 34.7% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 43 / UNUSABLE 81 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 63 | 0.59 | nws18_multiple_comp_acb、nws18_multiple_comp_qep、nws18_multiple_comp_qmb |
| 盈利与财务 | 23 | 0.54 | nws18_multiple_comp_bee、nws18_multiple_comp_ber、nws18_bee |
| 其他 | 11 | 0.72 | nws18_mltpl_cmp_event_simildays、multi_entity_reporting_end_date_utc、multi_entity_reporting_start_date_utc |
| 元数据与非信号 | 8 | 0.72 | multi_entity_reporting_end_time_utc、multi_entity_reporting_start_time_utc、reporting_period_end_time_utc |
| 修正与预期 | 6 | 0.61 | nws18_multiple_comp_ghc_lna、nws18_ghc_lna、rp_css_ratings |
| 价量与波动 | 6 | 0.50 | rp_css_price、rp_css_ptg、rp_ess_price |
| 风险与质量 | 4 | 0.87 | nws18_multiple_comp_relevance、nws18_mltpl_cmp_event_relevance、nws18_relevance |
| 宏观与行业 | 2 | 0.89 | multi_entity_country_iso_code、entity_country_iso_code_4 |
| 搜索与替代数据 | 1 | 0.33 | mapping_reporting_end_date_utc |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `multi_entity_country_iso_code` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The ISO country code for each entity in a multi-entity event. |
| 2 | `multi_entity_reporting_end_time_utc` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The UTC timestamp marking the end of the reporting period for multiple entities. |
| 3 | `multi_entity_reporting_start_time_utc` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The UTC timestamp marking the start of the reporting period for multiple entities. |
| 4 | `nws18_mltpl_cmp_event_simildays` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Days since a similar event was detected |
| 5 | `nws18_multiple_comp_acb` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News sentiment specializing in corporate action announcements |
| 6 | `nws18_multiple_comp_bee` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings evaluations score with values -1, 0, or +1 |
| 7 | `nws18_multiple_comp_ber` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | News sentiment specializing in earnings result |
| 8 | `nws18_multiple_comp_ghc_lna` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in analyst recommendation |
| 9 | `nws18_multiple_comp_qep` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Global equities sentiment score taking values -1, 0, or +1 |
| 10 | `nws18_multiple_comp_qmb` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News sentiment specializing in editorials on global markets |
| 11 | `multi_entity_story_event_count` | VECTOR | 0.991 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The total number of event records for a news story involving multiple entities. |
| 12 | `nws18_multiple_comp_bam` | VECTOR | 0.991 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News sentiment specializing in mergers and acquisitions |
| 13 | `nws18_multiple_comp_nip` | VECTOR | 0.991 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Degree of impact of the news |
| 14 | `nws18_multiple_comp_qcm` | VECTOR | 0.991 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News sentiment of relevant news with high confidence |
| 15 | `nws18_multiple_comp_relevance` | VECTOR | 0.991 | 风险与质量 | 0 | — | — | — | UNTESTED | Relevance score indicating the significance of the entity in the story (typically 0–100) |
| 16 | `nws18_multiple_comp_ssc` | VECTOR | 0.991 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment of the news calculated using multiple techniques |
| 17 | `nws18_mltpl_cmp_event_relevance` | VECTOR | 0.976 | 风险与质量 | 0 | — | — | — | UNTESTED | Overall event relevance score (e.g., 0–100) measuring importance of the event |
| 18 | `nws18_multiple_comp_sse` | VECTOR | 0.976 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment polarity score of the event, typically from -1 (negative) to +1 (positive) |
| 19 | `multi_entity_reporting_end_date_utc` | VECTOR | 0.927 | 其他 | 0 | — | — | — | UNTESTED | The UTC date marking the end of the reporting period for multiple entities. |
| 20 | `multi_entity_reporting_start_date_utc` | VECTOR | 0.927 | 其他 | 0 | — | — | — | UNTESTED | The UTC date marking the start of the reporting period for multiple entities. |
| 21 | `nws18_acb` | VECTOR | 0.833 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News sentiment specializing in corporate action announcements |
| 22 | `nws18_bam` | VECTOR | 0.833 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mergers and acquisitions sentiment indicator (e.g., -1 negative, 0 neutral, +1 positive) |
| 23 | `nws18_nip` | VECTOR | 0.833 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Narrative impact score in [-1, 1] estimating the news item’s short-term market impact (e.g., next two hours) |
| 24 | `nws18_qmb` | VECTOR | 0.833 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Editorials and commentary score indicating stance or sentiment (-1, 0, +1) |
| 25 | `nws18_relevance` | VECTOR | 0.833 | 风险与质量 | 0 | — | — | — | UNTESTED | Score from 0 to 100 indicating how strongly the entity is related to the story higher is more relevant |
| 26 | `nws18_ssc` | VECTOR | 0.833 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Granular sentiment score from -1.00 to +1.00 for the story, combining multiple sentiment analysis techniques |
| 27 | `nws18_event_relevance` | VECTOR | 0.817 | 其他 | 0 | — | — | — | UNTESTED | Integer from 0 to 100 indicating the event’s relevance within the story |
| 28 | `nws18_event_similarity_days` | VECTOR | 0.817 | 其他 | 0 | — | — | — | UNTESTED | Number of days since a similar event was last detected within the past 365 days, up to 5 decimals |
| 29 | `reporting_period_end_time_utc` | VECTOR | 0.778 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The UTC timestamp marking the end of the reporting period for the event. |
| 30 | `entity_country_iso_code_4` | VECTOR | 0.772 | 宏观与行业 | 0 | — | — | — | UNTESTED | The two-letter ISO code representing the country associated with the entity. |
| 31 | `nws18_bee` | VECTOR | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings evaluation score indicating positive, neutral, or negative assessment (-1, 0, +1) |
| 32 | `nws18_ber` | VECTOR | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Release Indicator flag for earnings release events |
| 33 | `nws18_ghc_lna` | VECTOR | 0.772 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in analyst recommendation |
| 34 | `nws18_qcm` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News sentiment of relevant news with high confidence |
| 35 | `nws18_qep` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Equities sentiment polarity score derived from positive/negative words in news (typically -1, 0, +1) |
| 36 | `story_event_record_count` | VECTOR | 0.772 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The total number of event records published for a news story. |
| 37 | `nws18_sse` | VECTOR | 0.757 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Continuous sentiment score between -1.00 and +1.00 for the entity-event |
| 38 | `reporting_period_end_date_utc` | VECTOR | 0.719 | 其他 | 0 | — | — | — | UNTESTED | The UTC date marking the end of the reporting period for the event. |
| 39 | `reporting_period_start_date_utc` | VECTOR | 0.719 | 其他 | 0 | — | — | — | UNTESTED | The UTC date marking the beginning of the reporting period for the event. |
| 40 | `reporting_period_start_time_utc` | VECTOR | 0.719 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The UTC timestamp marking the beginning of the reporting period for the event. |
| 41 | `multi_entity_event_end_date_utc` | VECTOR | 0.675 | 其他 | 0 | — | — | — | UNTESTED | The UTC date when a multi-entity event concludes. |
| 42 | `multi_entity_event_end_time_utc` | VECTOR | 0.675 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The UTC timestamp when a multi-entity event concludes. |
| 43 | `multi_entity_event_start_date_utc` | VECTOR | 0.675 | 风险与质量 | 0 | — | — | — | UNTESTED | The UTC date when an event involving multiple entities begins. |
| 44 | `multi_entity_event_start_time_utc` | VECTOR | 0.590 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | The UTC timestamp when a multi-entity event begins. |
| 45 | `rp_css_assets` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Composite sentiment score of assets news |
| 46 | `rp_css_business` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of business-related news |
| 47 | `rp_css_credit` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of credit news |
| 48 | `rp_css_credit_ratings` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of credit ratings news |
| 49 | `rp_css_dividends` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Composite sentiment score of dividends news |
| 50 | `rp_css_earnings` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Composite sentiment score of earnings news |
| 51 | `rp_css_equity` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Composite sentiment score of equity action news |
| 52 | `rp_css_insider` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of insider trading news |
| 53 | `rp_css_inverstor` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of investor relations news |
| 54 | `rp_css_labor` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of labor issues news |
| 55 | `rp_css_legal` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of legal news |
| 56 | `rp_css_marketing` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of marketing news |
| 57 | `rp_css_mna` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of mergers and acquisitions-related news |
| 58 | `rp_css_partner` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of partnership news |
| 59 | `rp_css_price` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Composite sentiment score of stock price news |
| 60 | `rp_css_product` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of product and service-related news |
| 61 | `rp_css_ptg` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Composite sentiment score of price target news |
| 62 | `rp_css_ratings` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Composite sentiment score of analyst ratings-related news |
| 63 | `rp_css_revenue` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Composite sentiment score of revenue news |
| 64 | `rp_css_society` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score of society-related news |
| 65 | `rp_css_technical` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Composite sentiment score based on technical analysis |
| 66 | `rp_ess_assets` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Event sentiment score of assets news |
| 67 | `rp_ess_business` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of business-related news |
| 68 | `rp_ess_credit` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of credit news |
| 69 | `rp_ess_credit_ratings` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of credit ratings news |
| 70 | `rp_ess_dividends` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Event sentiment score of dividends news |
| 71 | `rp_ess_earnings` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Event sentiment score of earnings news |
| 72 | `rp_ess_equity` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Event sentiment score of equity action news |
| 73 | `rp_ess_insider` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of insider trading news |
| 74 | `rp_ess_labor` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of labor issues news |
| 75 | `rp_ess_legal` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of legal news |
| 76 | `rp_ess_mna` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of mergers and acquisitions-related news |
| 77 | `rp_ess_partner` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of partnership news |
| 78 | `rp_ess_price` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Event sentiment score of stock price news |
| 79 | `rp_ess_product` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of product and service-related news |
| 80 | `rp_ess_ptg` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Event sentiment score of price target news |
| 81 | `rp_ess_ratings` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Event sentiment score of analyst ratings-related news |
| 82 | `rp_ess_revenue` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Event sentiment score of revenue news |
| 83 | `rp_ess_society` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score of society-related news |
| 84 | `rp_ess_technical` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Event sentiment score based on technical analysis |
| 85 | `rp_nip_assets` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | News impact projection of assets news |
| 86 | `rp_nip_business` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of business-related news |
| 87 | `rp_nip_credit` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of credit news |
| 88 | `rp_nip_credit_ratings` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of credit ratings news |
| 89 | `rp_nip_dividends` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | News impact projection of dividends news |
| 90 | `rp_nip_earnings` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | News impact projection of earnings news |
| 91 | `rp_nip_equity` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | News impact projection of equity action news |
| 92 | `rp_nip_inverstor` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of investor relations news |
| 93 | `rp_nip_labor` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of labor issues news |
| 94 | `rp_nip_legal` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of legal news |
| 95 | `rp_nip_mna` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of mergers and acquisitions-related news |
| 96 | `rp_nip_partner` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of partnership news |
| 97 | `rp_nip_price` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | News impact projection of stock price news |
| 98 | `rp_nip_product` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of product and service-related news |
| 99 | `rp_nip_ptg` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | News impact projection of price target news |
| 100 | `rp_nip_ratings` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | News impact projection of analyst ratings-related news |
| 101 | `rp_nip_revenue` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | News impact projection of revenue news |
| 102 | `rp_nip_society` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection of society-related news |
| 103 | `rp_nip_technical` | MATRIX | 0.500 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News impact projection based on technical analysis |
| 104 | `event_end_date_utc` | VECTOR | 0.496 | 其他 | 0 | — | — | — | UNUSABLE | The UTC date when the event concludes. |
| 105 | `event_end_time_utc` | VECTOR | 0.496 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | The UTC timestamp when the event concludes. |
| 106 | `event_start_time_utc` | VECTOR | 0.496 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | The UTC timestamp when the event begins. |
| 107 | `event_start_date_utc` | VECTOR | 0.438 | 其他 | 0 | — | — | — | UNUSABLE | The UTC date when the event begins. |
| 108 | `analyst_recommendation_change` | VECTOR | 0.362 | 修正与预期 | 0 | — | — | — | UNUSABLE | A score representing a change in analyst recommendation, such as upgrade or downgrade. |
| 109 | `composite_news_sentiment_score` | VECTOR | 0.362 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A sentiment score representing the overall news sentiment for a story by combining multiple techniques. |
| 110 | `corporate_action_sentiment_2` | VECTOR | 0.362 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A sentiment score for news stories about corporate action announcements. |
| 111 | `earnings_evaluation_sentiment_2` | VECTOR | 0.362 | 盈利与财务 | 0 | — | — | — | UNUSABLE | A sentiment score for news stories about earnings evaluations. |
| 112 | `earnings_release_sentiment` | VECTOR | 0.362 | 盈利与财务 | 0 | — | — | — | UNUSABLE | A sentiment score for news stories about earnings releases. |
| 113 | `editorial_commentary_sentiment_3` | VECTOR | 0.362 | 盈利与财务 | 0 | — | — | — | UNUSABLE | A sentiment score for short commentary and editorials on equity markets. |
| 114 | `entity_relevance_score_3` | VECTOR | 0.362 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score indicating how strongly an entity is related to the news story. |
| 115 | `mapping_equity_sentiment_score` | VECTOR | 0.362 | 盈利与财务 | 0 | — | — | — | UNUSABLE | A sentiment score for equities as found in the mapping file. |
| 116 | `merger_acquisition_sentiment_2` | VECTOR | 0.362 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A sentiment score for news stories about mergers, acquisitions, and takeovers. |
| 117 | `multi_classifier_sentiment` | VECTOR | 0.362 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A sentiment score derived from multiple analytics methods for relevant entities in a story. |
| 118 | `news_impact_projection_score_2` | VECTOR | 0.362 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score estimating the market impact of a news flash over the next two hours. |
| 119 | `story_event_total_count` | VECTOR | 0.362 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | The total number of entity records published for a news story. |
| 120 | `story_headline_text` | VECTOR | 0.362 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | The main title or summary text of the news story. |
| 121 | `days_since_similar_event_2` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | The number of days since a similar event was last detected for the entity. |
| 122 | `event_prominence_score` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score reflecting the prominence of an event within a news story. |
| 123 | `event_sentiment_value` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | A score between -1 and 1 representing the sentiment of the event for the entity. |
| 124 | `mapping_reporting_end_date_utc` | VECTOR | 0.334 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | The UTC date marking the end of the reporting period in the mapping file. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

