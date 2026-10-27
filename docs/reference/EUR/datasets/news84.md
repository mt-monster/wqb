# news84 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news84` |
| 名称 | Headline Sentiment Analysis using DNN |
| 类别 | NEWS |
| 数据字段数(平台) | 23 |
| 覆盖率 | 0.7811 |
| 平台已有 alpha | 63 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset leverages advanced machine learning techniques to transfer sentiment signals from one news analytics dataset to another, specifically mapping sentiment derived from one set of financial news headlines onto a different set of press release headlines. By using neural network models to learn how sentiment is constructed in the source dataset and applying this understanding to the target dataset, it generates a new, alternative sentiment score for each press release. This approach enables the creation of a unique sentiment signal that may capture market-relevant nuances missed by traditional sentiment models. Such a dataset can be valuable for predicting price movements, as it provides a differentiated view of market sentiment that can be used to enhance alpha generation, inform t

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **23** |
| 类型分布 | MATRIX×20　VECTOR×3 |
| 平均覆盖率 | **0.781** |
| 覆盖率区间 | 0.66 ~ 0.80 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 20 | 87.0% |
| 低 (0.50–0.70) | 3 | 13.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 23 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 23 | 0.78 | max_primary_sentiment_score_transfer、max_secondary_sentiment_score_transfer、max_sentiment_score_transfer |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `max_primary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The highest value of the primary transferred sentiment score for the period. |
| 2 | `max_secondary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The highest value of the secondary transferred sentiment score for the period. |
| 3 | `max_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The maximum sentiment score derived from transferred news sentiment for the period. |
| 4 | `mean_primary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The average value of the primary transferred sentiment score for the period. |
| 5 | `mean_secondary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The average value of the secondary transferred sentiment score for the period. |
| 6 | `mean_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The average of all transferred sentiment scores for the period. |
| 7 | `median_primary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The median value of the primary transferred sentiment score for the period. |
| 8 | `median_secondary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The median value of the secondary transferred sentiment score for the period. |
| 9 | `median_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The median value of transferred sentiment scores for the period. |
| 10 | `min_primary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The lowest value of the primary transferred sentiment score for the period. |
| 11 | `min_secondary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The lowest value of the secondary transferred sentiment score for the period. |
| 12 | `min_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The minimum sentiment score derived from transferred news sentiment for the period. |
| 13 | `news_item_count_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The total number of news items used for transferred sentiment calculation. |
| 14 | `normalized_news_item_count_transfer_2` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The count of news items used for sentiment transfer, normalized for comparability. |
| 15 | `skew_primary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The skewness of the primary transferred sentiment score distribution for the period. |
| 16 | `skew_secondary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The skewness of the secondary transferred sentiment score distribution for the period. |
| 17 | `skew_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The skewness of the transferred sentiment score distribution for the period. |
| 18 | `sum_primary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The sum of all primary transferred sentiment scores for the period. |
| 19 | `sum_secondary_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The sum of all secondary transferred sentiment scores for the period. |
| 20 | `sum_sentiment_score_transfer` | MATRIX | 0.799 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The sum of all transferred sentiment scores for the period. |
| 21 | `mws84_sentiment` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Sentiment of headlines |
| 22 | `primary_sentiment_score_transfer` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The primary transferred sentiment score for the period. |
| 23 | `secondary_sentiment_score_transfer` | VECTOR | 0.664 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The secondary transferred sentiment score for the period. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-NEWS84-SENTIMENT-MATRIX-WEAK`（2026-08-24）family=news84 migration sentiment MATRIX probe：{"dataset": "news84", "max_abs_sharpe": 0.35, "best": "KP7ngxpl", "mirror": "QP7n0moK", "wave": 40, "id": "EUR-NEWS84-SENTIMENT-MATRIX-WEAK", "reason": "Wave40 slot1 news84 migration sentiment MATRIX max /S/0.35 with sign-flip mirror. Same weak-probe outcome as news85. No independent IS.", "rule": "Leave news84/news85. Do not occupy another slot with EUR news sentiment MATRIX probes.", "dead_at": 

