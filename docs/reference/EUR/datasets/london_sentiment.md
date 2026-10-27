# london_sentiment — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `london_sentiment` |
| 名称 | London Stock Sentiment Signals |
| 类别 | MODEL |
| 数据字段数(平台) | 7 |
| 覆盖率 | 0.1634 |
| 平台已有 alpha | 0 |
| valueScore | 6.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides daily sentiment scores for stocks listed on the London Stock Exchange, derived from the analysis of financial-relevant Twitter posts. Each stock's sentiment is quantified using normalized, weighted scores based on tweet content, volume, and changes over 1-day and 5-day periods. The dataset includes metrics such as sentiment volume, standard deviation, and z-scores, offering a comprehensive view of market sentiment trends. By tracking shifts in social media sentiment, analysts and traders can identify potential price movements, gauge investor mood, and enhance trading strategies with timely, alternative data signals.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **7** |
| 类型分布 | VECTOR×7 |
| 平均覆盖率 | **0.163** |
| 覆盖率区间 | 0.16 ~ 0.16 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 7 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 7 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 7 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 价量与波动 | 7 | 0.16 | five_day_sentiment_score_change、normalized_sentiment_volume_score、one_day_sentiment_score_change |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `five_day_sentiment_score_change` | VECTOR | 0.163 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-day change in sentiment z-score (today minus 5 trading days ago of sent_volume_z) |
| 2 | `normalized_sentiment_volume_score` | VECTOR | 0.163 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day z-score of sent_volume ((current minus 20D mean) divided by 20D std) |
| 3 | `one_day_sentiment_score_change` | VECTOR | 0.163 | 价量与波动 | 0 | — | — | — | UNUSABLE | 1-day change in sentiment z-score (today minus prior day of sent_volume_z) |
| 4 | `relative_tweet_volume_stddev` | VECTOR | 0.163 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day coefficient of variation of tweet volume (std divided by mean), indicating activity burstiness |
| 5 | `sentiment_volume_adjusted_score` | VECTOR | 0.163 | 价量与波动 | 0 | — | — | — | UNUSABLE | Daily volume-adjusted social sentiment score derived from relevant tweets |
| 6 | `sentiment_volume_score_stddev` | VECTOR | 0.163 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day rolling standard deviation of sent_volume |
| 7 | `twenty_day_avg_sentiment_volume_score` | VECTOR | 0.163 | 价量与波动 | 0 | — | — | — | UNUSABLE | 20-day rolling mean of sent_volume |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

