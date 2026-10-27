# news38 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news38` |
| 名称 | News Analytic Model Data |
| 类别 | NEWS |
| 数据字段数(平台) | 30 |
| 覆盖率 | 0.6821 |
| 平台已有 alpha | 79 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset delivers real-time and historical financial news, blogs, and sentiment analytics sourced from thousands of global websites and media outlets. It includes structured metadata such as headlines, story content, assigned and derived tickers/topics, market-moving potential indicators, sentiment scores, readership metrics, and corporate event details. Advanced natural language processing and machine learning models generate analytics like market-moving news probability, sentiment, and novelty scores for each story. By quantifying news impact and sentiment, this dataset enables users to identify market-moving events, gauge investor sentiment, and detect abnormal price movement risks, making it highly valuable for predicting short-term price reactions and supporting event-driven tradi

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **30** |
| 类型分布 | VECTOR×30 |
| 平均覆盖率 | **0.682** |
| 覆盖率区间 | 0.31 ~ 0.90 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 23 | 76.7% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 7 | 23.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 23 | 76.7% |
| UNUSABLE | 7 | 23.3% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 23 / UNUSABLE 7 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 18 | 0.72 | story_analytics_relevance_score、mws38_time、story_analytics_metric_value |
| 其他 | 4 | 0.53 | mws38_sg_negative_freq、mws38_sg_positive_freq、mws38_negative_freq |
| 风险与质量 | 4 | 0.53 | mws38_sg_negative_score、mws38_sg_positive_score、mws38_negative_score |
| 搜索与替代数据 | 3 | 0.85 | mws38_entitlement、story_analytics_category、mws38_action |
| 修正与预期 | 1 | 0.83 | mws38_version |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `story_analytics_relevance_score` | VECTOR | 0.899 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Composite or rolling analytics score (e.g., sentiment, attention, or relevance) for the news story at the given time poi |
| 2 | `mws38_entitlement` | VECTOR | 0.898 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | System/internal field indicating permissioning or logical gating for access; must not be used in research or modeling as |
| 3 | `mws38_time` | VECTOR | 0.898 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Integer representing the news publication time in hhmmss format (local market time zone) |
| 4 | `story_analytics_category` | VECTOR | 0.826 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Integer code representing the analytics type or classification for the story/event, which must be dynamically label-mapp |
| 5 | `story_analytics_metric_value` | VECTOR | 0.826 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Numeric value of the analytics metric for the news story. |
| 6 | `market_impact_indicator` | VECTOR | 0.825 | 情绪与新闻 | 0 | — | — | — | UNTESTED | A numeric measure of the level of attention, novelty, or “heat” associated with a news story; higher values indicate mor |
| 7 | `mws38_action` | VECTOR | 0.825 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Integer code describing the lifecycle event or state (e.g. add, update, cancel), requires label-mapping for precise mean |
| 8 | `mws38_related_num` | VECTOR | 0.825 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of stocks or entities related to or affected by the news |
| 9 | `mws38_relevances` | VECTOR | 0.825 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Numeric score(s) indicating how relevant the news is to the corresponding stock(s); higher values indicate stronger rele |
| 10 | `mws38_version` | VECTOR | 0.825 | 修正与预期 | 0 | — | — | — | UNTESTED | Numeric code representing the version or revision number of the news story or event instance |
| 11 | `mws38_sg_entitlement` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News entitlement ID (EID) |
| 12 | `mws38_sg_negative_freq` | VECTOR | 0.744 | 其他 | 0 | — | — | — | UNTESTED | Negative frequency |
| 13 | `mws38_sg_negative_score` | VECTOR | 0.744 | 风险与质量 | 0 | — | — | — | UNTESTED | Negative score |
| 14 | `mws38_sg_positive_freq` | VECTOR | 0.744 | 其他 | 0 | — | — | — | UNTESTED | Positive frequency |
| 15 | `mws38_sg_positive_score` | VECTOR | 0.744 | 风险与质量 | 0 | — | — | — | UNTESTED | Positive score |
| 16 | `mws38_sg_time` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News time |
| 17 | `mws38_sg_tone_score` | VECTOR | 0.744 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Tone score |
| 18 | `mws38_analytics_entitlement` | VECTOR | 0.740 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News entitlement ID (EID) |
| 19 | `mws38_analytics_time` | VECTOR | 0.740 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News time |
| 20 | `mws38_previous` | VECTOR | 0.740 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Previous news |
| 21 | `mws38_score` | VECTOR | 0.740 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News score |
| 22 | `mws38_type` | VECTOR | 0.740 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News type |
| 23 | `mws38_value` | VECTOR | 0.740 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News value |
| 24 | `mws38_headlinetones_sg_entitlement` | VECTOR | 0.381 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News entitlement ID (EID) |
| 25 | `mws38_headlinetones_sg_time` | VECTOR | 0.381 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | News time |
| 26 | `mws38_tone_score` | VECTOR | 0.338 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Tone score |
| 27 | `mws38_negative_freq` | VECTOR | 0.311 | 其他 | 0 | — | — | — | UNUSABLE | Negative frequency |
| 28 | `mws38_negative_score` | VECTOR | 0.311 | 风险与质量 | 0 | — | — | — | UNUSABLE | Negative score |
| 29 | `mws38_positive_freq` | VECTOR | 0.309 | 其他 | 0 | — | — | — | UNUSABLE | Positive frequency |
| 30 | `mws38_positive_score` | VECTOR | 0.309 | 风险与质量 | 0 | — | — | — | UNUSABLE | Positive score |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS38-CONCEPT-WEAK`（2026-08-25）family=news38 densified tone/polarity/relevance concepts：{"dataset": "news38", "id": "EUR-NEWS38-CONCEPT-WEAK", "reason": "Wave64 56 exprs / 7 concept slots (tone invert, pos-neg score/freq, relevance-gated tone, relevance-heat, related_num, analytics-score). Max S0.61 F0.20 (ak7dLe55). Heat slot max S0.53 F0.36. No cheap-gate. Slow-leg /S/<1 so do not mix PV.", "rule": "Leave news38 standalone densify concepts. Do not mix v_rev/wedge. Skip news54 times
- `EUR-NEWS36-NOVELTY-SENT-WEAK`（2026-08-25）family=news36 novelty/phrase/word/confidence concepts：{"dataset": "news36", "id": "EUR-NEWS36-NOVELTY-SENT-WEAK", "reason": "Wave65 56 exprs / 7 slots. Max S0.60 F0.19 (rKjodQr9 relevance-gated inverted neg phrases). Confidence S0.54, phrase S0.51. No cheap-gate. Slow /S/<1 so do not mix PV.", "rule": "Leave news36 standalone novelty/sentiment densify. NEWS whitelist concept track exhausted (news38/36/84/85). Skip news54 timestamps. Next unused non-N

