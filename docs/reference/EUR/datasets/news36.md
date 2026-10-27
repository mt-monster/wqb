# news36 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news36` |
| 名称 | News Analytics Data |
| 类别 | NEWS |
| 数据字段数(平台) | 15 |
| 覆盖率 | 0.7713 |
| 平台已有 alpha | 20 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RIC) and Bloomberg IDs, facilitating the cross-referencing of securities across two major financial data platforms. The mapping is essential for integrating and reconciling data from Bloomberg and Refinitiv sources, enabling seamless data aggregation, analysis, and reporting. While not directly predictive of price movements, this dataset is crucial for ensuring data consistency and accuracy in multi-source quantitative research, portfolio management, and trading systems that rely on identifiers from both platforms.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **15** |
| 类型分布 | VECTOR×15 |
| 平均覆盖率 | **0.771** |
| 覆盖率区间 | 0.77 ~ 0.77 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 15 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 15 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 8 | 0.77 | mws36_relevance、mws36_sentiment_negative_confidence、mws36_sentiment_phrase_negative |
| 其他 | 3 | 0.77 | mws36_novelty_newest_span、mws36_novelty_oldest_span、mws36_total_words |
| 风险与质量 | 2 | 0.77 | mws36_key_event_confidence、mws36_novelty |
| 宏观与行业 | 1 | 0.77 | event_effect_magnitude |
| 元数据与非信号 | 1 | 0.77 | mws36_timestamp_time |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `event_effect_magnitude` | VECTOR | 0.771 | 宏观与行业 | 0 | — | — | — | UNTESTED | Planned impact magnitude on affected entities; not yet populated (<0.1 minor, 0.1–0.9 moderate, >0.9 high) |
| 2 | `mws36_key_event_confidence` | VECTOR | 0.771 | 风险与质量 | 0 | — | — | — | UNTESTED | Confidence score of the key event classification for this story |
| 3 | `mws36_novelty` | VECTOR | 0.771 | 风险与质量 | 0 | — | — | — | UNTESTED | Novelty score within subscribed content sets (100 novel, 50 partially novel, 0 not novel) |
| 4 | `mws36_novelty_newest_span` | VECTOR | 0.771 | 其他 | 0 | — | — | — | UNTESTED | Milliseconds between this story and the most recent older similar story; empty if first |
| 5 | `mws36_novelty_oldest_span` | VECTOR | 0.771 | 其他 | 0 | — | — | — | UNTESTED | Milliseconds between this story and the oldest known similar story starting the novelty sequence; empty if first |
| 6 | `mws36_relevance` | VECTOR | 0.771 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Overall relevance score of the news story to the referenced entity/entities, on a 0–100 scale where higher means more re |
| 7 | `mws36_sentiment_negative_confidence` | VECTOR | 0.771 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Confidence score that the story is negative; higher means more confident negative classification |
| 8 | `mws36_sentiment_phrase_negative` | VECTOR | 0.771 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count of negative sentiment phrases detected by the bigram classifier |
| 9 | `mws36_sentiment_phrase_positive` | VECTOR | 0.771 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count of positive sentiment phrases detected by the bigram classifier |
| 10 | `mws36_sentiment_positive_confidence` | VECTOR | 0.771 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Confidence score that the story is positive; higher means more confident positive classification |
| 11 | `mws36_sentiment_words_negative` | VECTOR | 0.771 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count of negative sentiment tokens detected by the unigram classifier |
| 12 | `mws36_sentiment_words_positive` | VECTOR | 0.771 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Count of positive sentiment tokens detected by the unigram classifier |
| 13 | `mws36_timestamp_time` | VECTOR | 0.771 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Time component of the story’s publication timestamp as an integer (e.g., HHMMSS or milliseconds) |
| 14 | `mws36_title` | VECTOR | 0.771 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The article title text |
| 15 | `mws36_total_words` | VECTOR | 0.771 | 其他 | 0 | — | — | — | UNTESTED | Total tokens examined by the unigram classifier |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS38-CONCEPT-WEAK`（2026-08-25）family=news38 densified tone/polarity/relevance concepts：{"dataset": "news38", "id": "EUR-NEWS38-CONCEPT-WEAK", "reason": "Wave64 56 exprs / 7 concept slots (tone invert, pos-neg score/freq, relevance-gated tone, relevance-heat, related_num, analytics-score). Max S0.61 F0.20 (ak7dLe55). Heat slot max S0.53 F0.36. No cheap-gate. Slow-leg /S/<1 so do not mix PV.", "rule": "Leave news38 standalone densify concepts. Do not mix v_rev/wedge. Skip news54 times
- `EUR-NEWS36-NOVELTY-SENT-WEAK`（2026-08-25）family=news36 novelty/phrase/word/confidence concepts：{"dataset": "news36", "id": "EUR-NEWS36-NOVELTY-SENT-WEAK", "reason": "Wave65 56 exprs / 7 slots. Max S0.60 F0.19 (rKjodQr9 relevance-gated inverted neg phrases). Confidence S0.54, phrase S0.51. No cheap-gate. Slow /S/<1 so do not mix PV.", "rule": "Leave news36 standalone novelty/sentiment densify. NEWS whitelist concept track exhausted (news38/36/84/85). Skip news54 timestamps. Next unused non-N

