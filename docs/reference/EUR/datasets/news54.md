# news54 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news54` |
| 名称 | Key Developments Data |
| 类别 | NEWS |
| 数据字段数(平台) | 40 |
| 覆盖率 | 0.9002 |
| 平台已有 alpha | 3 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides concise, real-time summaries of significant, market-moving company news events, intelligently tagged by topic and significance. Covering a wide range of event types—such as mergers, acquisitions, earnings guidance, regulatory actions, product launches, and executive changes—it enables users to filter out noise and focus on impactful developments. Each event is classified by importance and topic, with detailed metadata for integration into quantitative models. By offering both current and historical trend analysis, this dataset is valuable for predicting price movements, supporting event-driven trading strategies, and enhancing alpha generation through timely identification of key corporate actions and news.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **40** |
| 类型分布 | VECTOR×40 |
| 平均覆盖率 | **0.900** |
| 覆盖率区间 | 0.87 ~ 0.98 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 18 | 45.0% |
| 中 (0.70–0.90) | 22 | 55.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 37 | 92.5% |
| DEAD | 2 | 5.0% |
| DEAD_STATIC | 1 | 2.5% |

- 已实测字段：**3** 个（8%），best_sharpe 最高 **0.40**，中位 -0.51

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 29 | 0.90 | mws54_eventcallbasicinfo_postponedflag、event_announcement_time、event_entry_time |
| 盈利与财务 | 8 | 0.88 | mws54_factor、mws54_eventerinfo_cancelledflag、daily_event_earnings_release_time |
| 情绪与新闻 | 3 | 0.92 | mws54_keydevelopments_headline、mws54_futureeventmkt_headline、mws54_eventsdaily_headline |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mws54_factor` | VECTOR | 0.913 | 盈利与财务 | 2 | 0.40 | — | — | DEAD_STATIC | Numeric amount/factor associated with the event, e.g., dividend amount or stock split ratio |
| 2 | `mws54_eventerinfo_cancelledflag` | VECTOR | 0.871 | 盈利与财务 | 2 | -0.51 | — | — | DEAD | Indicator that the earnings event was canceled |
| 3 | `mws54_eventcallbasicinfo_postponedflag` | VECTOR | 0.871 | 其他 | 1 | -0.96 | — | — | DEAD | Indicator whether the event call was postponed; 0=no, 1=yes |
| 4 | `event_announcement_time` | VECTOR | 0.983 | 其他 | 0 | — | — | — | UNTESTED | The UTC time at which the event was announced |
| 5 | `event_entry_time` | VECTOR | 0.983 | 其他 | 0 | — | — | — | UNTESTED | The time when the event record was entered into the system |
| 6 | `event_last_update_time` | VECTOR | 0.983 | 其他 | 0 | — | — | — | UNTESTED | The time when the event record was last modified |
| 7 | `event_relevant_time_utc` | VECTOR | 0.983 | 其他 | 0 | — | — | — | UNTESTED | UTC time of the key moment for the event (usually the announced time; for scheduled events, the event time) |
| 8 | `mws54_keydevelopments_headline` | VECTOR | 0.983 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Headline text describing the event |
| 9 | `mws54_keydevelopments_situation` | VECTOR | 0.983 | 其他 | 0 | — | — | — | UNTESTED | Additional descriptive narrative text about the event |
| 10 | `future_event_announcement_time` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Time the announcement is scheduled to be made, in UTC |
| 11 | `future_event_announcement_time_utc` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Time the announcement is scheduled/made in UTC |
| 12 | `future_event_entry_time` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Time when this Future Event was entered |
| 13 | `future_event_entry_time_utc` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Time the Future Event was entered, in UTC |
| 14 | `future_event_last_update_time` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Time of the last modification to the Future Event |
| 15 | `future_event_last_update_time_utc` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Time of the last modification in UTC |
| 16 | `future_event_record_end_time` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | End time of the S&P effective window during which this record is valid |
| 17 | `future_event_record_start_time` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Start time of the S&P effective window for this record |
| 18 | `future_event_relevant_time_utc` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Time the event occurs in UTC time zone |
| 19 | `mws54_futureeventmkt_headline` | VECTOR | 0.913 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Headline for the event |
| 20 | `mws54_futureeventmkt_situation` | VECTOR | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Additional descriptive text/details for the event |
| 21 | `daily_event_announcement_time` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Time of the announcement in the announcedDateTimeZoneId time zone |
| 22 | `daily_event_announcement_time_utc` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Time the event was announced (UTC) |
| 23 | `daily_event_earnings_release_time` | VECTOR | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time of the earnings release |
| 24 | `daily_event_entry_time` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | The time when the event was entered in the dataset. |
| 25 | `daily_event_entry_time_utc` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Time the record was first entered into the system (UTC) |
| 26 | `daily_event_last_update_time` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Time the event record was last modified |
| 27 | `daily_event_last_update_time_utc` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Time the record was last modified (UTC) |
| 28 | `daily_event_record_end_time` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | The time when the current record for the daily event ceased to be active. |
| 29 | `daily_event_record_start_time` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | The time when the current record for the daily event became active. |
| 30 | `daily_event_relevant_time_utc` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Time in UTC of the event’s key moment (often the event time; otherwise announcement time) |
| 31 | `mws54_eventcallbasicinfo_cancelledflag` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Flag indicating whether the event call was cancelled, 0=no, 1=yes |
| 32 | `mws54_eventcallbasicinfo_fiscalquarter` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Fiscal quarter associated with the event |
| 33 | `mws54_eventcallbasicinfo_fiscalyear` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Fiscal year pertaining to the event call |
| 34 | `mws54_eventerinfo_calendarmonth` | VECTOR | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | Calendar month of the earnings release |
| 35 | `mws54_eventerinfo_calendaryear` | VECTOR | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | Calendar year of the earnings release |
| 36 | `mws54_eventerinfo_fiscalquarter` | VECTOR | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fiscal quarter associated with the earnings release |
| 37 | `mws54_eventerinfo_fiscalyear` | VECTOR | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fiscal year of the earnings release |
| 38 | `mws54_eventerinfo_fullyearflag` | VECTOR | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flag indicating the earnings release covers a full fiscal year, 0=no, 1=yes |
| 39 | `mws54_eventsdaily_headline` | VECTOR | 0.871 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Headline text for the event |
| 40 | `mws54_eventsdaily_situation` | VECTOR | 0.871 | 其他 | 0 | — | — | — | UNTESTED | Additional descriptive text for the event |

## 六、本地回测证据

- 本地累计回测 **7** 条；其中 `ra_failed_checks` 为空的 **7** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `blR6V97p` | 0.40 | 0.15 | — | — | 0.02 | 0 | s2_news54_d1 | `trade_when(vec_count(mws54_factor) > 0, group_rank(ts_mean(vec_avg(mws54_factor), 66), sub` |
| `2rOAQpvZ` | 0.39 | 0.04 | — | — | 1.24 | 0 | s2_news54_d1 | `rank(vec_avg(headline_vader_positive_polarity) - vec_avg(headline_vader_negative_polarity)` |
| `MP1Yqxwr` | 0.31 | 0.11 | — | — | 0.02 | 0 | s2_news54_d1 | `trade_when(vec_count(mws54_factor) > 0, rank(ts_mean(vec_avg(mws54_factor), 22)), NaN)` |
| `e795g3nl` | 0.25 | 0.06 | — | — | 0.11 | 0 | s2_news54_d1 | `rank(ts_mean(vec_avg(headline_textblob_sentiment_score), 22))` |
| `9qVxbRgV` | -0.51 | -0.25 | — | — | 0.05 | 0 | s2_news54_d1 | `rank(ts_mean(ts_backfill(vec_avg(mws54_eventerinfo_cancelledflag), 66), 22))` |
| `LL9MqROm` | -0.54 | -0.27 | — | — | 0.03 | 0 | s2_news54_d1 | `group_rank(ts_mean(ts_backfill(vec_avg(mws54_eventerinfo_cancelledflag), 66), 66), subindu` |
| `vRk1xmad` | -0.96 | -0.97 | — | — | 0.05 | 0 | s2_news54_d1 | `ts_zscore(ts_backfill(vec_avg(mws54_eventcallbasicinfo_postponedflag), 66), 22)` |

## 七、判死记录（sealed dead_end）

- `EUR-NEWS38-CONCEPT-WEAK`（2026-08-25）family=news38 densified tone/polarity/relevance concepts：{"dataset": "news38", "id": "EUR-NEWS38-CONCEPT-WEAK", "reason": "Wave64 56 exprs / 7 concept slots (tone invert, pos-neg score/freq, relevance-gated tone, relevance-heat, related_num, analytics-score). Max S0.61 F0.20 (ak7dLe55). Heat slot max S0.53 F0.36. No cheap-gate. Slow-leg /S/<1 so do not mix PV.", "rule": "Leave news38 standalone densify concepts. Do not mix v_rev/wedge. Skip news54 times
- `EUR-NEWS36-NOVELTY-SENT-WEAK`（2026-08-25）family=news36 novelty/phrase/word/confidence concepts：{"dataset": "news36", "id": "EUR-NEWS36-NOVELTY-SENT-WEAK", "reason": "Wave65 56 exprs / 7 slots. Max S0.60 F0.19 (rKjodQr9 relevance-gated inverted neg phrases). Confidence S0.54, phrase S0.51. No cheap-gate. Slow /S/<1 so do not mix PV.", "rule": "Leave news36 standalone novelty/sentiment densify. NEWS whitelist concept track exhausted (news38/36/84/85). Skip news54 timestamps. Next unused non-N
- `EUR-M354-VALUATION-YIELD-WEAK`（2026-08-25）family=model354 group valuation yield concepts：{"dataset": "model354", "id": "EUR-M354-VALUATION-YIELD-WEAK", "reason": "Wave66 56 exprs / 7 slots (FY2/NTM EY, FCF/CFO/div yield, sales/EV, FY1-LTM disagreement). Max S0.26 F0.07 (KP7bgexN). Many TVR 2-4%. No cheap-gate. Do not mix PV.", "rule": "Leave model354 standalone valuation densify. Next unused whitelist: ml_factor_proj low-competition non-return MATRIX concepts (not NEWS, not news54, no
- `EUR-news54-TIMESTAMP-INVALID`（2026-09-04）family=news54 event timestamp fields：{"dataset": "news54", "evidence": "wave118 GEM 生成 8 条全部用 event_announcement_time 时间戳字段，ts_mean/ts_delta 对时间戳无意义；news54 可用数值字段极少（只有 mws54_factor），时间戳需转换", "id": "EUR-news54-TIMESTAMP-INVALID", "reason": "news54 时间戳字段（event_announcement_time/entry_time）是 UNIX 时间戳，ts_mean/ts_delta 无意义；需转换为'距今天数'但 GEM 不理解；可用数值字段极少", "region": "EUR", "rule": "Leave news54 timestamp fields in EUR. Do not use ts_mean/ts_
- `EUR-NONMODEL-TOWER-CEILING`（2026-09-11）family=non_model_tower_sparse_event_sentiment_analyst：{"datasets": [{"dataset": "news54", "max_sharpe": 0.4, "reason": "mws54_factor semi-annual+单边恒正+稀疏", "tower": "news"}, {"dataset": "news_sentiment_nlp", "max_sharpe": 0.39, "reason": "情绪信号弱,净极性turnover1.24高超手", "tower": "other"}, {"dataset": "analyst45", "max_sharpe": 0.32, "reason": "分析师想法表现弱,zscore/delta turnover1.5+", "tower": "analyst"}], "evidence": "三塔回测全灭,S0 calibrate预警与实测完全一致(news0.50→0.40

