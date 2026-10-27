# news7 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news7` |
| 名称 | Real Time News Feed Data |
| 类别 | NEWS |
| 数据字段数(平台) | 118 |
| 覆盖率 | 0.715 |
| 平台已有 alpha | 300 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive, point-in-time financial statement data for a global universe of public companies, including both active and inactive firms. It offers daily historical snapshots of income statements, balance sheets, and cash flow statements, capturing both originally reported and restated values as they were known on each reporting date. The data is standardized for cross-company comparability and includes detailed metadata such as auditor opinions, industry classifications, and currency conversions. By eliminating forward-looking and survivorship biases, this dataset enables accurate backtesting and robust factor research, making it highly valuable for predicting price movements based on fundamental signals and historical financial trends.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **118** |
| 类型分布 | MATRIX×62　VECTOR×56 |
| 平均覆盖率 | **0.715** |
| 覆盖率区间 | 0.28 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 52 | 44.1% |
| 中 (0.70–0.90) | 7 | 5.9% |
| 低 (0.50–0.70) | 29 | 24.6% |
| 稀疏 (<0.50) | 30 | 25.4% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 64 | 54.2% |
| UNUSABLE | 54 | 45.8% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 64 / UNUSABLE 54 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 80 | 0.72 | news_item_value、news_related_count、news_signal_alt_dmgrhchendtn |
| 修正与预期 | 12 | 0.58 | news_mention_frequency_1_simple、news_mention_frequency_1_all、news_sales_mention_count_1 |
| 盈利与财务 | 11 | 0.60 | news_category_tag、news_subject_code、news_category_tag_livenews_all |
| 其他 | 10 | 0.86 | nws7_d1_comp_count、nws7_sl_d1_comp_count、nws7_all_story_time |
| 元数据与非信号 | 3 | 0.96 | nws7_d1_timestamp、nws7_sl_d1_timestamp、nws7_tname |
| 价量与波动 | 2 | 0.96 | nws7_all_area、nws7_area |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `news_category_tag` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Integer code representing a classification tag for the news headline (e.g., M&A, Earnings, Regulatory), decoded via the PIT codebook |
| 2 | `news_item_value` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | news type value |
| 3 | `news_related_count` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of financial instruments affected or mentioned in the news event |
| 4 | `news_signal_alt_dmgrhchendtn` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A computed signal or indicator derived from news data in the alternative DmgrHchenDtn module. |
| 5 | `news_topic_name_2` | VECTOR | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | index to type name |
| 6 | `nws7_d1_comp_count` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | the number of different companies in the story |
| 7 | `nws7_d1_timestamp` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | timestamp of the story |
| 8 | `nws7_sl_d1_comp_count` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | the number of different companies in the story |
| 9 | `nws7_sl_d1_timestamp` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | timestamp of the story |
| 10 | `news_story_company_count` | VECTOR | 0.988 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of distinct companies or entities mentioned in the story |
| 11 | `news_story_full_text` | VECTOR | 0.988 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Full text content of the news story/article |
| 12 | `livenews_story_company_count_sl` | VECTOR | 0.976 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of companies or entities mentioned or involved in the story |
| 13 | `livenews_story_full_text_sl` | VECTOR | 0.976 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Full text content of the news story |
| 14 | `nws7_all_story_time` | VECTOR | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Time (in GMT, to the second) the first alert/take for this story was issued |
| 15 | `nws7_all_take_seqno` | VECTOR | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Number of alerts/takes in the story. Set to 1 for the first and incremented by 1 for each subsequent alert/take in that story |
| 16 | `nws7_livenews_all_tag` | VECTOR | 0.975 | 情绪与新闻 | 0 | — | — | — | UNTESTED | news headline tag |
| 17 | `nws7_livenews_all_time` | VECTOR | 0.975 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Time (in GMT, to the second) this alert/take was issued |
| 18 | `nws7_all_area` | VECTOR | 0.974 | 价量与波动 | 0 | — | — | — | UNTESTED | Returns News Service Data Centre where the news was first broadcast (0 - NY, 1 - LD, 2 - LO, 3 - HA) |
| 19 | `nws7_all_display_name` | VECTOR | 0.973 | 其他 | 0 | — | — | — | UNTESTED | Message subtype (0: alert, 1: first_take, 2: subsequent_take, 3: correction, 4: corrected, 5: delete) |
| 20 | `nws7_eur_news_freq_2_qerf` | MATRIX | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | number of news |
| 21 | `nws7_newsfreq_qerf` | MATRIX | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news without imbalance" key words" |
| 22 | `nws7_nf_qerf` | MATRIX | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | number of news |
| 23 | `nws7_news_d1_tag` | VECTOR | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | news headline tag |
| 24 | `nws7_news_d1_time` | VECTOR | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | news time |
| 25 | `nws7_related_num` | VECTOR | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | news affected instruments number |
| 26 | `nws7_tvalue` | VECTOR | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | news type value |
| 27 | `nws7_eur_news_freq_pzeng_qerf` | MATRIX | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | number of news |
| 28 | `nws7_eur_newsfreq_qerf` | MATRIX | 0.957 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news without insider" keywords" |
| 29 | `nws7_eur_newsfreq_all_delay_qerf` | MATRIX | 0.956 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news without insider" key words (extra delay)" |
| 30 | `nws7_livenews_time` | VECTOR | 0.948 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Time (in GMT, to the second) this alert/take was issued |
| 31 | `nws7_story_time` | VECTOR | 0.948 | 其他 | 0 | — | — | — | UNTESTED | time (in GMT, to the second) the first alert/take for this story was issued |
| 32 | `nws7_take_seqno` | VECTOR | 0.948 | 其他 | 0 | — | — | — | UNTESTED | Number of alerts/takes in the story. Set to 1 for the first and incremented by 1 for each subsequent alert/take in that story |
| 33 | `nws7_livenews_tag` | VECTOR | 0.947 | 情绪与新闻 | 0 | — | — | — | UNTESTED | news headline tag |
| 34 | `nws7_eur_headlinetone2_d1_news_freq` | MATRIX | 0.947 | 情绪与新闻 | 0 | — | — | — | UNTESTED | number of news |
| 35 | `nws7_area` | VECTOR | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Returns News Service Data Centre where the news was first broadcast (0 - NY, 1 - LD, 2 - LO, 3 - HA) |
| 36 | `nws7_display_name` | VECTOR | 0.944 | 其他 | 0 | — | — | — | UNTESTED | Message subtype (0: alert, 1: first_take, 2: subsequent_take, 3: correction, 4: corrected, 5: delete) |
| 37 | `news_product_code_all` | VECTOR | 0.934 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Product code specifying the news product or audience for all news items in the feed. |
| 38 | `news_subject_code_all` | VECTOR | 0.934 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Subject or topic code for all news items, indicating the main theme or category. |
| 39 | `news_mention_frequency_alt_newsfreq` | MATRIX | 0.931 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count of news stories linked to the security on each date, excluding stories containing "imbalance" keywords |
| 40 | `news_mention_frequency_alt_nf` | MATRIX | 0.931 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news articles/events associated with the security on a given date |
| 41 | `news_mention_frequency_2` | MATRIX | 0.931 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count of news articles per US security and date, excluding stories containing insider-related keywords (real-time D0 delay) |
| 42 | `news_mention_frequency_alt_xtangnfgdata` | MATRIX | 0.931 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The number of news items or mentions within a specified period in the alternative XtangNfgData module. |
| 43 | `news_mention_frequency_v11_0_0` | MATRIX | 0.931 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Daily count of news events associated with a security or entity in the Europe (EUR) region, excluding stories containing the keyword "inside |
| 44 | `news_mention_frequency_pzeng` | MATRIX | 0.931 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news events or stories related to European securities, counted per security and date in the djnews dataset |
| 45 | `news_product_code` | VECTOR | 0.926 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Code indicating the news product or audience group to which a news item is published. |
| 46 | `news_subject_code` | VECTOR | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Code representing the subject or topic of a news item, such as asset class, geography, or industry. |
| 47 | `headline_mention_count_2` | MATRIX | 0.926 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news headlines for the given security and date |
| 48 | `headline_negative_mention_count_2` | MATRIX | 0.926 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total count of negative words appearing in all news headlines for the day |
| 49 | `headline_negative_tone_score_2` | MATRIX | 0.926 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The average ratio of negative words to all words in all news headlines for the day |
| 50 | `headline_overall_tone_score_2` | MATRIX | 0.926 | 情绪与新闻 | 0 | — | — | — | UNTESTED | average normalized headline tone score across all news, calculated as (positive words - negative words) divided by (positive words + negativ |
| 51 | `headline_positive_mention_count_2` | MATRIX | 0.926 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Total count of positive words appearing in all news headlines for the day |
| 52 | `headline_positive_tone_score_2` | MATRIX | 0.926 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The average ratio of positive words to all words in all news headlines for the day |
| 53 | `nws7_tname` | VECTOR | 0.884 | 元数据与非信号 | 0 | — | — | — | UNTESTED | index to type name |
| 54 | `news_category_tag_livenews_all` | VECTOR | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | Integer code for fine-grained classification tag (e.g., "M&A", "Earnings"), resolved via codebook |
| 55 | `news_display_name_livenews_all` | VECTOR | 0.758 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Code indicating message subtype (e.g., 0-alert, 1-first take, 2-subsequent take, etc.) |
| 56 | `news_geographic_area_livenews_all` | VECTOR | 0.758 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Code for Data Centre where news was first broadcast (e.g., 0-NY, 1-LD, 2-LO, 3-HA) |
| 57 | `live_news_area_identifier` | VECTOR | 0.749 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Identifier for the geographic area or data center associated with the live news item. |
| 58 | `live_news_display_label` | VECTOR | 0.749 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Display label or name for the live news item or source. |
| 59 | `live_news_headline_tag` | VECTOR | 0.749 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Tag indicating the type or status of the live news headline. |
| 60 | `news_mention_frequency_1_simple` | MATRIX | 0.632 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of news articles per security and date in Europe that contain keywords related to sales, earnings, analyst, and EPS |
| 61 | `news_mention_frequency_1_all` | MATRIX | 0.632 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of news articles per security and date within the Europe region, with an additional delay, containing keywords related to sales, earn |
| 62 | `news_sales_mention_count_1` | MATRIX | 0.624 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of Europe news articles per security and date with one-day delay that contain earnings or sales-related keywords (e.g., earning, earni |
| 63 | `news_sales_mention_count_1_all_delay_1` | MATRIX | 0.624 | 修正与预期 | 0 | — | — | — | UNTESTED | Count of news articles related to earnings, EPS, sales, or estimates, mentioning keywords such as "earning", "earnings", "EPS", "sale", "sal |
| 64 | `news_sales_mention_count_1_d0` | MATRIX | 0.623 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of news articles per security and date in the EUR region (real-time/daily) containing keywords related to earnings, EPS, sales, or es |
| 65 | `headline_mention_count` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Total number of news items for the security/date in the dataset |
| 66 | `headline_negative_mention_count` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of negative words in headlines across all news for a security/date |
| 67 | `headline_negative_tone_score` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average proportion of negative words in news headlines, calculated as negative words divided by total words, across all news for the securit |
| 68 | `headline_overall_tone_score` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | average tone score calculated as (positive word count - negative word count) divided by (positive word count + negative word count) for head |
| 69 | `headline_positive_mention_count` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive words in headlines across all news for a security/date |
| 70 | `headline_positive_tone_score` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average proportion of positive words in news headlines, calculated as positive words divided by total words, across all news for the securit |
| 71 | `news_mention_frequency_alt_livenewsfreq` | MATRIX | 0.594 | 修正与预期 | 0 | — | — | — | UNUSABLE | The count of news articles per security and date containing the keywords "sale", "earning", "analyst", "sales", "earnings", or "EPS" as dete |
| 72 | `news_negative_mention_count_alt_storytone` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | date |
| 73 | `news_negative_tone_score_alt_storytone` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Total count of negative words in the story |
| 74 | `news_overall_tone_score_alt_storytone` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Normalized sentiment score calculated as (positive word count minus negative word count) divided by total positive and negative word count |
| 75 | `news_positive_mention_count_alt_storytone` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Total count of positive words in the story |
| 76 | `news_positive_tone_score_alt_storytone` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Proportion of positive words relative to all words in the story |
| 77 | `news_story_mention_count_alt_storytone` | MATRIX | 0.594 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Proportion of negative words relative to all words in the story |
| 78 | `news_sales_mention_count` | MATRIX | 0.589 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Daily count of news articles for European securities that mention sales-related keywords (e.g., sale, sales) or earnings, aggregated per sec |
| 79 | `news_sales_mention_count_all` | MATRIX | 0.589 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Delayed next-day (D1) count of news stories for European securities containing the keywords "sale", "sales", or "earnings" |
| 80 | `nws7_eur_newsfreq_1_d1_sales_qerf` | MATRIX | 0.572 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of news with earning/earnings/EPS/sale/sales/estimate" keywords" |
| 81 | `nws7_eur_newsfreq_1_d1_sales_all_delay_1_qerf` | MATRIX | 0.572 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of news with earning/earnings/EPS/sale/sales/estimate" key words (extra delay)" |
| 82 | `nws7_eur_news_freq_1_qerf` | MATRIX | 0.569 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of news with sale/earning/analyst/sales/earnings/EPS" keywords" |
| 83 | `nws7_eur_news_freq_1_all_delay_1_qerf` | MATRIX | 0.569 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of news with sale/earning/analyst/sales/earnings/EPS" key words (extra delay)" |
| 84 | `nws7_eur_news_freq_sales_qerf` | MATRIX | 0.549 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of news with sale/sales/earnings" keywords" |
| 85 | `nws7_eur_news_freq_sales_all_delay_1_qerf` | MATRIX | 0.549 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of news with sale/sales/earnings" key words" |
| 86 | `nws7_eur_headlinetone_d1_news_freq` | MATRIX | 0.541 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | number of news |
| 87 | `nws7_storytone_news_freq` | MATRIX | 0.540 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | negative words divided by all words |
| 88 | `nws7_livenewsfreq_qerf` | MATRIX | 0.540 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of news with sale/earning/analyst/sales/earnings/EPS" keywords" |
| 89 | `nws7_storytone_tone_score` | MATRIX | 0.451 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | ((pos - neg) / (pos + neg)) |
| 90 | `nws7_storytone_positive_freq` | MATRIX | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | how many positive words in story |
| 91 | `nws7_storytone_positive_score` | MATRIX | 0.441 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | positive words divided by all words |
| 92 | `nws7_storytone_negative_freq` | MATRIX | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | date |
| 93 | `nws7_storytone_negative_score` | MATRIX | 0.430 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | how many negative words in story |
| 94 | `earnings_news_mention_count` | MATRIX | 0.428 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of news items per security and date that mention "earnings," "earning," or "EPS" in the text, representing earnings-related news freq |
| 95 | `news_earnings_mention_count_all` | MATRIX | 0.427 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of news articles mentioning earnings-related keywords (such as "earning", "earnings", "EPS") for each security on each date, aggregat |
| 96 | `headline_negative_sentiment_score` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Ratio of negative words to total words in the story headline |
| 97 | `headline_negative_sentiment_score_story` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Ratio of negative words to total words in the headline |
| 98 | `headline_negative_word_count` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of negative words in the story headline |
| 99 | `headline_negative_word_count_story` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of negative words in the headline across all news articles |
| 100 | `headline_positive_sentiment_score` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Ratio of positive words to total words in the story headline |
| 101 | `headline_positive_sentiment_score_story` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Ratio of positive words to total words in the headline |
| 102 | `headline_positive_word_count` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of positive words in the story headline |
| 103 | `headline_positive_word_count_story` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of positive words in the headline across all news articles |
| 104 | `headline_sentiment_score_2` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment score for the headline, calculated as (positive words minus negative words) divided by (positive plus negative words) |
| 105 | `headline_sentiment_score_story` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Net sentiment score for the headline, calculated as (positive words - negative words) divided by (positive words + negative words) |
| 106 | `story_body_negative_sentiment_score` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Ratio of negative words to total words in the story text |
| 107 | `story_body_negative_word_count` | VECTOR | 0.421 | 其他 | 0 | — | — | — | UNUSABLE | Number of negative words in the story text |
| 108 | `story_body_positive_sentiment_score` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Ratio of positive words to total words in the story |
| 109 | `story_body_positive_word_count` | VECTOR | 0.421 | 其他 | 0 | — | — | — | UNUSABLE | Number of positive words in the story text |
| 110 | `story_body_sentiment_score` | VECTOR | 0.421 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of alerts/takes in the story. Starts at 1 for first alert/take and increases by 1 for each additional alert/take in that story |
| 111 | `nws7_eur_headlinetone2_d1_tone_score` | MATRIX | 0.418 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Average tone_score ((pos - neg) / (pos + neg)) |
| 112 | `nws7_eur_news_earning_qerf` | MATRIX | 0.400 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of news with earning/earnings/EPS" keywords" |
| 113 | `nws7_eur_news_earning_all_delay_1_qerf` | MATRIX | 0.400 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of news with earning/earnings/EPS" key words (extra delay)" |
| 114 | `nws7_news_revisions_d1_time` | VECTOR | 0.379 | 修正与预期 | 0 | — | — | — | UNUSABLE | when the event was published |
| 115 | `nws7_eur_headlinetone2_d1_negative_freq` | MATRIX | 0.286 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | How many negative words in the headline of all news |
| 116 | `nws7_eur_headlinetone2_d1_negative_score` | MATRIX | 0.286 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | average negative score (negative words by all words) of all news |
| 117 | `nws7_eur_headlinetone2_d1_positive_freq` | MATRIX | 0.285 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | How many positive words in the headline of all news |
| 118 | `nws7_eur_headlinetone2_d1_positive_score` | MATRIX | 0.285 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | average positive score (negative words by all words) of all news |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-predictive_starmine-NEWS-MIX-WEAK`（2026-09-04）family=predictive_starmine × news73 sentiment mix：{"best_2y": 1.26, "best_alpha": "9qVLwrOK", "best_fitness": 0.52, "best_sharpe": 1.21, "dataset": "predictive_starmine × news73", "evidence": "wave113 11 条全灭：MODEL×NEWS 配方（surprise 慢腿 × nws73 情绪快腿）整体弱信号，最强候选 S1.21/F0.52/2Y1.26 未达 Mode B 资格线；news73 字段在 EUR TOP2500 覆盖不足或信号弱", "id": "EUR-predictive_starmine-NEWS-MIX-WEAK", "reason": "MODEL×NEWS 跨集混合弱信号：surprise 与 news73 sentiment 相关性不足，组合后 IS 衰减；11 条
- `EUR-news_sentiment_dl-SENTIMENT-WEAK`（2026-09-04）family=news_sentiment_dl sentiment word stats：{"best_2y": 1.36, "best_alpha": "zqY1knoO", "best_fitness": 0.04, "best_sharpe": 0.21, "dataset": "news_sentiment_dl", "evidence": "wave114 9 条全灭：情绪词统计（mean/max/min positive/negative sentiment）在 EUR TOP2500 整体弱信号，最强 S0.38/F0.07/2Y0.63 远低于 Mode B 线；text_complexity 交互项全负；ts_std_dev/ts_delta 快腿全负", "id": "EUR-news_sentiment_dl-SENTIMENT-WEAK", "reason": "news_sentiment_dl 情绪词统计与文本复杂度在 EUR D1 无正向预测力；p

