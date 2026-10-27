# news85 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news85` |
| 名称 | News Sentiment Analysis using DNN |
| 类别 | NEWS |
| 数据字段数(平台) | 23 |
| 覆盖率 | 0.823 |
| 平台已有 alpha | 54 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset applies neural network techniques to transfer sentiment analytics from one news dataset to another, specifically mapping sentiment from tr_trna_eq headlines to ravenpack_web_v2 headlines. By leveraging machine learning to align sentiment scoring methodologies across datasets, it generates new sentiment signals for the target dataset, potentially enhancing alpha generation and predictive power. This approach allows for the creation of unified sentiment indicators, improving the consistency and robustness of trading models that rely on news-driven sentiment for forecasting price movements.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **23** |
| 类型分布 | MATRIX×20　VECTOR×3 |
| 平均覆盖率 | **0.823** |
| 覆盖率区间 | 0.72 ~ 0.84 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 23 | 100.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 23 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 23 | 0.82 | aggregate_sentiment_total、headline_item_count、normalized_headline_count |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `aggregate_sentiment_total` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sum of all sentiment values for the entity over the period. |
| 2 | `headline_item_count` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of news headlines associated with the entity in the period. |
| 3 | `normalized_headline_count` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | News headline count normalized by a reference or average value. |
| 4 | `peak_sentiment_value` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Highest sentiment score observed for the entity in the period. |
| 5 | `sentiment1_aggregate_total` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sum of all first sentiment values for the entity over the period. |
| 6 | `sentiment1_average_value` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of the first sentiment metric for the entity. |
| 7 | `sentiment1_distribution_skewness` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Skewness of the first sentiment value distribution for the entity. |
| 8 | `sentiment1_highest_score` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of the first sentiment measure for the entity. |
| 9 | `sentiment1_lowest_score` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of the first sentiment measure for the entity. |
| 10 | `sentiment1_median_value` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of the first sentiment metric for the entity. |
| 11 | `sentiment2_aggregate_total` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sum of all second sentiment values for the entity over the period. |
| 12 | `sentiment2_average_value` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Mean value of the second sentiment metric for the entity. |
| 13 | `sentiment2_central_tendency` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median value of the second sentiment measure for the entity. |
| 14 | `sentiment2_distribution_skewness` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Skewness of the second sentiment value distribution for the entity. |
| 15 | `sentiment2_highest_score` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Maximum value of the second sentiment measure for the entity. |
| 16 | `sentiment2_lowest_score` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Minimum value of the second sentiment measure for the entity. |
| 17 | `sentiment_distribution_skewness` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Skewness of the sentiment value distribution for the entity. |
| 18 | `sentiment_overall_average` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Average sentiment value for the entity across all news items. |
| 19 | `sentiment_overall_median` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Median sentiment value for the entity across all news items. |
| 20 | `sentiment_overall_minimum` | MATRIX | 0.839 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Lowest sentiment value for the entity across all news items. |
| 21 | `mws85_sentiment` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment based on news |
| 22 | `sentiment1_raw_score` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Raw value of the first sentiment metric for the entity. |
| 23 | `sentiment2_raw_score` | VECTOR | 0.718 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Raw value of the second sentiment metric for the entity. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS85-SENTIMENT-MATRIX-WEAK`（2026-08-24）family=news85 DNN sentiment MATRIX probe：{"dataset": "news85", "max_abs_sharpe": 0.32, "best": "rKjbdM2j", "mirror": "Vk7XdbG0", "wave": 39, "id": "EUR-NEWS85-SENTIMENT-MATRIX-WEAK", "reason": "Wave39 slot1 news85 DNN sentiment MATRIX max /S/0.32 with exact sign-flip mirror. No independent IS. Do not occupy another slot with news85 naked probes.", "rule": "Leave news85. Do not second-round probe.", "dead_at": "2026-08-24"}
- `EUR-NEWS84-SENTIMENT-MATRIX-WEAK`（2026-08-24）family=news84 migration sentiment MATRIX probe：{"dataset": "news84", "max_abs_sharpe": 0.35, "best": "KP7ngxpl", "mirror": "QP7n0moK", "wave": 40, "id": "EUR-NEWS84-SENTIMENT-MATRIX-WEAK", "reason": "Wave40 slot1 news84 migration sentiment MATRIX max /S/0.35 with sign-flip mirror. Same weak-probe outcome as news85. No independent IS.", "rule": "Leave news84/news85. Do not occupy another slot with EUR news sentiment MATRIX probes.", "dead_at": 

