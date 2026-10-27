# news21 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news21` |
| 名称 | Macro Economic Event Data |
| 类别 | NEWS |
| 数据字段数(平台) | 47 |
| 覆盖率 | 0.5266 |
| 平台已有 alpha | 1282 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides concise, real-time summaries of major company news events, focusing on developments that are likely to move markets. Each event is tagged by topic (such as M&A, earnings guidance, product launches, regulatory actions, and more) and assigned a significance level, allowing users to filter for the most impactful news. The data includes detailed headlines, descriptions, event categorization, and metadata such as timing, company identifiers, and industry classification. By offering structured, noise-filtered news with intelligent tagging, this dataset enables quantitative models and event-driven strategies to quickly identify and react to market-moving information, making it a valuable resource for predicting short-term price movements and volatility.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **47** |
| 类型分布 | MATRIX×24　VECTOR×23 |
| 平均覆盖率 | **0.527** |
| 覆盖率区间 | 0.16 ~ 0.77 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 2 | 4.3% |
| 低 (0.50–0.70) | 32 | 68.1% |
| 稀疏 (<0.50) | 13 | 27.7% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 25 | 53.2% |
| UNTESTED | 17 | 36.2% |
| DEAD | 5 | 10.6% |

- 已实测字段：**5** 个（11%），best_sharpe 最高 **0.64**，中位 0.47

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 16 | 0.49 | nws21_pos_sc、nws21_neg_sc、event_end_time |
| 盈利与财务 | 10 | 0.60 | previous_earnings_call_date、earning_calendar_quarter_end、earning_fiscal_quarter_number |
| 修正与预期 | 9 | 0.62 | estimated_next_shareholder_meeting_date、earning_broker_count、earning_event_type_label |
| 情绪与新闻 | 5 | 0.45 | nws21_tone_tone_sc、event_transcript_sentiment_score、negative_sentiment_score_1 |
| 元数据与非信号 | 3 | 0.48 | event_frequency_label、event_quarter_label、event_category_label_1 |
| 风险与质量 | 2 | 0.51 | event_transcript_negative_score、event_transcript_positive_score |
| 宏观与行业 | 2 | 0.27 | previous_corporate_presentation_date、next_corporate_presentation_date |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `previous_earnings_call_date` | MATRIX | 0.769 | 盈利与财务 | 2 | 0.64 | 0.50 | 0.50 | DEAD | Most recent past earnings conference call date prior to today for the US region module, encoded as an integer date (typi |
| 2 | `nws21_pos_sc` | MATRIX | 0.510 | 其他 | 1 | 0.64 | -0.31 | 0.48 | DEAD | Positive word count divided by total word count |
| 3 | `event_frequency_label` | MATRIX | 0.415 | 元数据与非信号 | 1 | 0.47 | 0.64 | 0.38 | DEAD | Integer count of StreetEvents mentions or hits for the company during the represented period or date |
| 4 | `nws21_tone_tone_sc` | MATRIX | 0.510 | 情绪与新闻 | 2 | 0.22 | 0.48 | 0.09 | DEAD | Normalized tone: (positive word count minus negative word count) divided by (positive word count plus negative word coun |
| 5 | `nws21_neg_sc` | MATRIX | 0.510 | 其他 | 1 | -0.21 | 0.86 | -0.35 | DEAD | Negative word count divided by total word count |
| 6 | `estimated_next_shareholder_meeting_date` | MATRIX | 0.708 | 修正与预期 | 0 | — | — | — | UNTESTED | Tentative or estimated date (as an integer date, e.g., YYYYMMDD) for the next shareholder annual meeting, provided with |
| 7 | `earning_broker_count` | VECTOR | 0.619 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of brokers contributing to the earnings consensus for the event. |
| 8 | `earning_calendar_quarter_end` | VECTOR | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | The end date of the calendar quarter associated with the earnings event. |
| 9 | `earning_event_type_label` | VECTOR | 0.619 | 修正与预期 | 0 | — | — | — | UNTESTED | Descriptive label for the type of earnings event (e.g., actual, estimate). |
| 10 | `earning_fiscal_quarter_number` | VECTOR | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fiscal quarter number that the earnings relate to (1–4) |
| 11 | `earning_fiscal_year` | VECTOR | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fiscal year number that the earnings relate to |
| 12 | `earning_fiscal_year_end` | VECTOR | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | The company’s fiscal year end date (month/day for fiscal year closing) |
| 13 | `earning_number_value` | VECTOR | 0.619 | 修正与预期 | 0 | — | — | — | UNTESTED | The reported or estimated earnings number (e.g., EPS) for the event. |
| 14 | `earning_time_type` | VECTOR | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Classification of the time associated with the earnings event (e.g., before open, after close). |
| 15 | `event_end_date_is_estimated` | VECTOR | 0.619 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating whether the event end date is estimated rather than confirmed |
| 16 | `event_end_date_type` | VECTOR | 0.619 | 修正与预期 | 0 | — | — | — | UNTESTED | Type or classification of the event's end date (e.g., actual, estimated). |
| 17 | `event_end_time` | VECTOR | 0.619 | 其他 | 0 | — | — | — | UNTESTED | Local time at which the event ends |
| 18 | `event_fiscal_year` | VECTOR | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | The fiscal year associated with the earnings event. |
| 19 | `event_quarter_label` | VECTOR | 0.619 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Label or code indicating the quarter associated with the event (e.g., Q1, Q2). |
| 20 | `event_start_date_is_estimated` | VECTOR | 0.619 | 修正与预期 | 0 | — | — | — | UNTESTED | Flag indicating whether the event start date is estimated rather than confirmed |
| 21 | `event_start_date_type` | VECTOR | 0.619 | 修正与预期 | 0 | — | — | — | UNTESTED | Type or classification of the event's start date (e.g., actual, estimated). |
| 22 | `event_start_time_2` | VECTOR | 0.619 | 其他 | 0 | — | — | — | UNTESTED | Local time at which the event starts |
| 23 | `previous_ex_dividend_event_date` | MATRIX | 0.565 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The most recent past ex-dividend date before today for the company in the USA module, encoded as an integer date |
| 24 | `next_earnings_call_date` | MATRIX | 0.541 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Next scheduled or confirmed earnings conference call date for the US region module, encoded as an integer date (typicall |
| 25 | `next_earnings_estimate_date` | MATRIX | 0.540 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated next earnings release date when the actual date is not yet confirmed (D1 module; next-day availability), store |
| 26 | `event_transcript_negative_score` | MATRIX | 0.510 | 风险与质量 | 0 | — | — | — | UNUSABLE | number of negative words divided by number of all words |
| 27 | `event_transcript_negative_word_count` | MATRIX | 0.510 | 其他 | 0 | — | — | — | UNUSABLE | number of negative words |
| 28 | `event_transcript_positive_score` | MATRIX | 0.510 | 风险与质量 | 0 | — | — | — | UNUSABLE | number of positive words divided by number of all words |
| 29 | `event_transcript_positive_word_count` | MATRIX | 0.510 | 其他 | 0 | — | — | — | UNUSABLE | number of positive words |
| 30 | `event_transcript_sentiment_score` | MATRIX | 0.510 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | (number of positive words - number of negative words) divided by (number of positive words + number of negative words) |
| 31 | `event_transcript_total_word_count` | MATRIX | 0.510 | 其他 | 0 | — | — | — | UNUSABLE | number of events |
| 32 | `nws21_event_freq` | MATRIX | 0.510 | 其他 | 0 | — | — | — | UNUSABLE | Count of events |
| 33 | `nws21_qerf_gen` | MATRIX | 0.510 | 其他 | 0 | — | — | — | UNUSABLE | Count of negative words |
| 34 | `nws21_qerf_sop` | MATRIX | 0.510 | 其他 | 0 | — | — | — | UNUSABLE | Count of positive words |
| 35 | `previous_shareholder_meeting_date` | MATRIX | 0.508 | 其他 | 0 | — | — | — | UNUSABLE | Most recent past date (as an integer date, e.g., YYYYMMDD) when the shareholder annual meeting last occurred before toda |
| 36 | `next_shareholder_meeting_date` | MATRIX | 0.490 | 其他 | 0 | — | — | — | UNUSABLE | Confirmed next scheduled date (as an integer date, e.g., YYYYMMDD) for the upcoming shareholder annual meeting as of tod |
| 37 | `next_ex_dividend_event_date` | MATRIX | 0.423 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The next confirmed ex-dividend date for the company in the USA module, delivered with next-day (D1) timeliness and encod |
| 38 | `event_category_label_1` | VECTOR | 0.417 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Numeric code indicating the type of event (decoded via event type codebook) |
| 39 | `negative_sentiment_score_1` | VECTOR | 0.417 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Negative sentiment score (negative words divided by total words) |
| 40 | `negative_word_count_1` | VECTOR | 0.417 | 其他 | 0 | — | — | — | UNUSABLE | Count of negative words detected in the transcript/segment |
| 41 | `overall_tone_score_1` | VECTOR | 0.417 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Overall sentiment/tone score for the event/transcript |
| 42 | `positive_sentiment_score_1` | VECTOR | 0.417 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Positive sentiment score for the event/transcript (positive words divided by total words) |
| 43 | `positive_word_count_1` | VECTOR | 0.417 | 其他 | 0 | — | — | — | UNUSABLE | Count of positive words detected in the transcript/segment |
| 44 | `transcript_version_label_1` | VECTOR | 0.417 | 其他 | 0 | — | — | — | UNUSABLE | Version of the transcript/brief (e.g., Preliminary, Edited, Audited, Redlined) |
| 45 | `previous_corporate_presentation_date` | MATRIX | 0.379 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Most recent past corporate presentation date before today (for a China-listed company), available on a next-trading-day |
| 46 | `previous_sales_statement_date` | MATRIX | 0.298 | 其他 | 0 | — | — | — | UNUSABLE | The most recent past occurrence date (as an integer date) of a company's sales/trading statement release event before th |
| 47 | `next_corporate_presentation_date` | MATRIX | 0.162 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Next scheduled or confirmed corporate presentation date (for a China-listed company) as of today, available on a next-tr |

## 六、本地回测证据

- 本地累计回测 **8** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `P02rmlRJ` | 0.64 | 0.63 | 0.50 | 0.50 | 0.08 | ["LOW_SHARPE | 208 | `trade_when(greater(abs(ts_delta(previous_earnings_call_date, 1)), 0), rank(event_transcrip` |
| `j2AlKw79` | 0.64 | 0.34 | -0.31 | 0.48 | 0.03 | ["LOW_SHARPE | 208 | `rank(ts_backfill(nws21_pos_sc, 66))` |
| `LLNbYXoM` | 0.59 | 0.56 | 0.46 | 0.35 | 0.08 | ["LOW_SHARPE | 208 | `trade_when(greater(abs(ts_delta(previous_earnings_call_date, 1)), 0), rank(nws21_tone_tone` |
| `JjN0JX9E` | 0.47 | 0.31 | 0.64 | 0.38 | 0.07 | ["LOW_SHARPE | 208 | `rank(multiply(-1, ts_zscore(ts_backfill(event_frequency_label, 22), 252)))` |
| `omLw0zb6` | 0.22 | 0.07 | 0.48 | -0.02 | 0.03 | ["LOW_SHARPE | 208 | `rank(ts_backfill(nws21_tone_tone_sc, 66))` |
| `kqok6mwk` | 0.12 | 0.02 | 0.43 | 0.43 | 0.03 | ["LOW_SHARPE | 208 | `rank(days_from_last_change(previous_earnings_call_date))` |
| `ZYbwvl81` | -0.05 | -0.01 | 0.45 | 0.09 | 0.04 | ["LOW_SHARPE | 208 | `rank(ts_delta(ts_backfill(nws21_tone_tone_sc, 66), 66))` |
| `omLw0zd6` | -0.21 | -0.06 | 0.86 | -0.35 | 0.03 | ["LOW_SHARPE | 208 | `rank(multiply(-1, ts_backfill(nws21_neg_sc, 66)))` |

## 七、判死记录（sealed dead_end）

- `EUR-NEWS21-EVENT-CALENDAR-DEAD`（2026-09-19）family=news21 event calendar / transcript tone (post-call drift, pre-call premium, tone level/change, attention)：{"id": "EUR-NEWS21-EVENT-CALENDAR-DEAD", "dataset": "news21", "wave": 208, "universe": "TOPCS1600", "evidence": "8 event/level probes /S/<=0.64 (post-call tone drift 0.59-0.64 with CW; tone level 0.22; pre-call calendar rank 0.12; attention z 0.47)", "verdict": "no RA-grade signal; transcript coverage 0.51 + CW", "rule": "EUR news tower: event-calendar family closed"}

