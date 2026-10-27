# other384 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other384` |
| 名称 | NLP on conference conversation |
| 类别 | OTHER |
| 数据字段数(平台) | 66 |
| 覆盖率 | 0.2803 |
| 平台已有 alpha | 42 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset applies natural language processing to corporate event transcripts, primarily from earnings calls and other financial conferences, to extract and quantify sentiment. It includes detailed breakdowns by section (presentation, Q&A), speaker, and sentence, providing sentiment scores using dictionary-based matching. The data is cleaned and segmented for ease of use, with meta data and simple sentiment indicators for each event. By analyzing the tone and sentiment of management and analyst interactions, investors can gauge market expectations, management confidence, and potential red flags, making this dataset valuable for predicting short-term price movements and identifying alpha opportunities around key corporate events.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **66** |
| 类型分布 | VECTOR×66 |
| 平均覆盖率 | **0.280** |
| 覆盖率区间 | 0.27 ~ 0.30 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 66 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 66 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 66 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 36 | 0.28 | conference_company_attendees、oth384_oecsi、oth384_ofcsi |
| 情绪与新闻 | 19 | 0.28 | event_headline_text、oth384_presentation_negfreq、oth384_presentation_negnum |
| 价量与波动 | 4 | 0.28 | oth384_presentation_questions、oth384_qa_questions、presentation_question_total |
| 风险与质量 | 2 | 0.28 | company_name_match_score、company_name_match_score_v1 |
| 修正与预期 | 2 | 0.28 | conference_analyst_attendees、conference_analyst_attendees_v1 |
| 交易与微观结构 | 2 | 0.28 | qa_section_laughter_count、qa_content_item_total |
| 盈利与财务 | 1 | 0.30 | event_full_title |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `company_name_match_score` | VECTOR | 0.295 | 风险与质量 | 0 | — | — | — | UNUSABLE | Similarity score indicating confidence in entity mapping/match (0–1) |
| 2 | `conference_analyst_attendees` | VECTOR | 0.295 | 修正与预期 | 0 | — | — | — | UNUSABLE | List of analyst participants on the call |
| 3 | `conference_company_attendees` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | List of company participant names for the event |
| 4 | `event_full_title` | VECTOR | 0.295 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Official title of the event (e.g., “Q1 2018 Apple Inc Earnings Conference Call”) |
| 5 | `event_headline_text` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Headline or title text of the event or transcript |
| 6 | `oth384_oecsi` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Indicator flag showing whether a CEO is listed among the participants |
| 7 | `oth384_ofcsi` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Flag indicating if a CFO participant is present (1=yes, 0=no) |
| 8 | `oth384_presentation_count` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Number of content words in the presentation section, excluding annotations and speaker names |
| 9 | `oth384_presentation_negfreq` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Frequency (ratio) of negative sentiment in the presentation section |
| 10 | `oth384_presentation_negnum` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of negative sentiment word instances in the presentation |
| 11 | `oth384_presentation_paragraphcount` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Number of paragraphs in the presentation section |
| 12 | `oth384_presentation_posfreq` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Ratio of positive words to total content words in the presentation (Presentation_posNum / Presentation_count) |
| 13 | `oth384_presentation_posnum` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive sentiment instances in the presentation section |
| 14 | `oth384_presentation_questions` | VECTOR | 0.295 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of questions asked during the presentation if any |
| 15 | `oth384_presentation_sentcount` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Number of sentences in the presentation section |
| 16 | `oth384_presentation_tone` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment tone score for the presentation section |
| 17 | `oth384_presentation_wordcount` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Number of words in the presentation section including annotations and speaker names |
| 18 | `oth384_qa_count` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Number of content words in the Q&A section, excluding annotations and speaker names |
| 19 | `oth384_qa_negnum` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of negative sentiment instances in the Q&A section |
| 20 | `oth384_qa_paragraphcount` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Number of paragraphs in the Q&A section |
| 21 | `oth384_qa_posnum` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive sentiment instances in the Q&A section |
| 22 | `oth384_qa_questions` | VECTOR | 0.295 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total number of questions asked during the Q&A |
| 23 | `oth384_qa_sentcount` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Number of sentences in the Q&A section |
| 24 | `oth384_qa_tone` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment tone score for the Q&A section |
| 25 | `oth384_qa_wordcount` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Number of words in the Q&A section of the transcript, including annotations and speaker names |
| 26 | `oth384_qerfgen_aq` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Ratio of negative words to total content words in the Q&A section |
| 27 | `oth384_qerfsop_aq` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Frequency of positive words in the Q&A calculated as QA_posNum divided by QA_count |
| 28 | `presentation_laughter_count` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Count of laughter annotations during the presentation segment |
| 29 | `presentation_section_speaker_list` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | List of speakers during the presentation section including roles and counts |
| 30 | `qa_section_laughter_count` | VECTOR | 0.295 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Count of laughter annotations during the Q&A session |
| 31 | `qa_section_speaker_list` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | List of speakers in the Q&A section, possibly with roles and counts |
| 32 | `transcript_body_headline` | VECTOR | 0.295 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Headline extracted from the body of the transcript |
| 33 | `transcript_is_initial_version` | VECTOR | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Flag indicating whether the transcript is a preliminary version from the vendor |
| 34 | `company_name_match_score_v1` | VECTOR | 0.265 | 风险与质量 | 0 | — | — | — | UNUSABLE | Similarity score (0–1) indicating confidence in the transcript’s entity/name-to-identifier match |
| 35 | `conference_analyst_attendees_v1` | VECTOR | 0.265 | 修正与预期 | 0 | — | — | — | UNUSABLE | List of analyst participants in the event |
| 36 | `conference_company_attendees_v1` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | List of company-side participants in the event |
| 37 | `event_full_title_v1` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Official title of the event |
| 38 | `event_headline_text_v1` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Headline text of the event or transcript |
| 39 | `presentation_content_item_total` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Number of content words in the presentation section, excluding annotations and speaker names |
| 40 | `presentation_laughter_count_v1` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Count of laughter instances in the presentation section |
| 41 | `presentation_negative_word_count` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of negative sentiment word occurrences in the presentation section |
| 42 | `presentation_negative_word_frequency` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Frequency of negative words in the presentation (Presentation_negNum divided by Presentation_count) |
| 43 | `presentation_overall_sentiment_score` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment tone score for the presentation section (typically a float from negative to positive) |
| 44 | `presentation_paragraph_total` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Number of paragraphs in the presentation section |
| 45 | `presentation_positive_word_count` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive sentiment word occurrences in the presentation section |
| 46 | `presentation_positive_word_frequency` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Frequency of positive words in the presentation (Presentation_posNum divided by Presentation_count) |
| 47 | `presentation_question_total` | VECTOR | 0.265 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of questions asked during the presentation section |
| 48 | `presentation_section_speaker_list_v1` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | List of speakers in the presentation section (may include roles and counts) |
| 49 | `presentation_sentence_total` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Number of sentences in the presentation section |
| 50 | `presentation_word_total` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Total words in the presentation section, including annotations and speaker names |
| 51 | `qa_content_item_total` | VECTOR | 0.265 | 交易与微观结构 | 0 | — | — | — | UNUSABLE | Count of content words in the Q&A session, excluding annotations and speaker names |
| 52 | `qa_negative_word_count` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Number of negative sentiment words in the Q&A session |
| 53 | `qa_negative_word_frequency` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Frequency of negative sentiment words in the Q&A session, computed as QA_negNum / QA_count |
| 54 | `qa_overall_sentiment_score` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Overall sentiment tone score for the Q&A session (e.g., -1 to 1) |
| 55 | `qa_paragraph_total` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Number of paragraphs in the Q&A section |
| 56 | `qa_positive_word_count` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Count of positive sentiment word occurrences in the Q&A section |
| 57 | `qa_positive_word_frequency` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Frequency of positive sentiment words in the Q&A session, computed as QA_posNum / QA_count |
| 58 | `qa_question_total` | VECTOR | 0.265 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total number of questions asked in the Q&A section |
| 59 | `qa_section_laughter_count_v1` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Count of laughter instances in the Q&A section |
| 60 | `qa_section_speaker_list_v1` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | List of speakers in the Q&A section (may include roles and counts) |
| 61 | `qa_sentence_total` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Number of sentences in the Q&A section |
| 62 | `qa_word_total` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Total words in the Q&A section, including annotations and speaker names |
| 63 | `speaker_is_ceo_flag` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Flag indicating whether a CEO is listed among the event participants (1=yes, 0=no) |
| 64 | `speaker_is_cfo_flag` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Flag indicating whether a CFO is listed among the event participants (1=yes, 0=no) |
| 65 | `transcript_body_headline_v1` | VECTOR | 0.265 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Headline of he body |
| 66 | `transcript_is_initial_version_v1` | VECTOR | 0.265 | 其他 | 0 | — | — | — | UNUSABLE | Flag indicating the transcript is an initial/preliminary version; content is essentially as good as the final |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

