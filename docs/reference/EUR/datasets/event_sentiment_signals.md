# event_sentiment_signals — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `event_sentiment_signals` |
| 名称 | Corporate Event Sentiment Signals |
| 类别 | OTHER |
| 数据字段数(平台) | 26 |
| 覆盖率 | 0.3567 |
| 平台已有 alpha | 22 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides structured sentiment analysis and key driver metrics derived from corporate event transcripts, including earnings calls, company presentations, analyst/investor days, and guidance calls. It covers a global universe of public companies, with detailed metadata such as industry classification, identifiers, event timestamps, and document sections. The dataset quantifies sentiment at multiple granularities—overall, by section, and by key topic—using scores based on positive and negative event counts, polarity, and word counts. By capturing management and analyst tone, margin and pricing power sentiment, and deception signals, it enables investors and researchers to assess market expectations, information asymmetry, and the impact of qualitative disclosures on price movemen

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **26** |
| 类型分布 | VECTOR×26 |
| 平均覆盖率 | **0.357** |
| 覆盖率区间 | 0.36 ~ 0.36 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 26 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 26 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 26 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 13 | 0.36 | event_count_in_section_aggregation、event_count_in_section_aggregation_2、event_weight_aggregation |
| 情绪与新闻 | 8 | 0.36 | event_weight_aggregation_2、key_factor_negative_score_section、key_factor_score_section |
| 风险与质量 | 3 | 0.36 | key_factor_negative_score_section_2、key_factor_positive_score_section、key_factor_positive_score_section_2 |
| 持仓与资金流 | 2 | 0.36 | section_negative_score_2、section_positive_score_2 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `event_count_in_section_aggregation` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Weighted count of events within the specified section context |
| 2 | `event_count_in_section_aggregation_2` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Weighted count of events in the given section context |
| 3 | `event_weight_aggregation` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | The numerical weight/magnitude assigned to the event occurrence |
| 4 | `event_weight_aggregation_2` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | The numeric weight assigned to an aggregated event, indicating its contribution or importance in the event aggregation and sentiment calcula |
| 5 | `key_factor_negative_event_count_section` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Count of negative events associated with the key driver in the section |
| 6 | `key_factor_negative_event_count_section_2` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Count of negative events for the key driver within the section |
| 7 | `key_factor_negative_score_section` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Weighted aggregate negative sentiment score for the given key driver within the section |
| 8 | `key_factor_negative_score_section_2` | VECTOR | 0.357 | 风险与质量 | 0 | — | — | — | UNUSABLE | Weighted aggregate of negative events for the specified key driver within the section |
| 9 | `key_factor_positive_event_count_section` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Count of positive events associated with the key driver in the section |
| 10 | `key_factor_positive_event_count_section_2` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Count of positive events for the key driver within the section |
| 11 | `key_factor_positive_score_section` | VECTOR | 0.357 | 风险与质量 | 0 | — | — | — | UNUSABLE | Weighted sum of positive events for the key driver within the section |
| 12 | `key_factor_positive_score_section_2` | VECTOR | 0.357 | 风险与质量 | 0 | — | — | — | UNUSABLE | Weighted aggregate of positive events for the specified key driver within the section |
| 13 | `key_factor_score_section` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment score for the key driver within the section, computed as (P−N)/(P+N+1) where P and N are weighted sums of positive and negative ev |
| 14 | `key_factor_score_section_2` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment score for the key driver within the section computed as (P−N)/(P+N+1) where P and N are weighted sums of positive and negative eve |
| 15 | `positive_event_count_section` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Count of positive events in the section |
| 16 | `positive_event_count_section_2` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Number of positive events identified in a document section. |
| 17 | `section_negative_event_count` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Count of negative events in the specified section |
| 18 | `section_negative_event_count_2` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Count of negative events in a document section. |
| 19 | `section_negative_score` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Weighted aggregate negative sentiment score for the section |
| 20 | `section_negative_score_2` | VECTOR | 0.357 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Weighted sum of negative events for the Fundamental-KD key driver in the section |
| 21 | `section_positive_score` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Weighted aggregate positive sentiment score for the section |
| 22 | `section_positive_score_2` | VECTOR | 0.357 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Weighted sum of positive events for the Fundamental-KD key driver in the section |
| 23 | `section_sentiment_score_2` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment score for events tagged with the Fundamental-KD key driver in this section, computed as (P−N)/(P+N+1) |
| 24 | `section_sentiment_score_3` | VECTOR | 0.357 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sentiment score for the section, computed as (P−N)/(P+N+1) where P and N are weighted sums of positive and negative events |
| 25 | `word_count_section` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Word count of the content in the specified transcript section |
| 26 | `word_count_section_2` | VECTOR | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Total number of words in a document section. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

