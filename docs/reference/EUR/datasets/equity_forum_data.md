# equity_forum_data — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `equity_forum_data` |
| 名称 | International Equity Forum Activity |
| 类别 | OTHER |
| 数据字段数(平台) | 8 |
| 覆盖率 | 0.406 |
| 平台已有 alpha | 0 |
| valueScore | 6.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset compiles user engagement and sentiment metrics from a wide range of online forums dedicated to equity discussions across multiple countries and languages. It includes aggregated statistics such as active user counts, comment volumes, buy and sell ratings, and unique user participation for various financial instruments. By analyzing trends in forum activity and sentiment, the dataset provides valuable insights into retail investor behavior and crowd sentiment, which can serve as leading indicators for price movements. The inclusion of risk-adjusted performance metrics and benchmark correlations further enhances its utility for developing predictive models and alpha strategies based on social media-driven market signals.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **8** |
| 类型分布 | VECTOR×8 |
| 平均覆盖率 | **0.406** |
| 覆盖率区间 | 0.41 ~ 0.41 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 8 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 8 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 8 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 4 | 0.41 | aggregate_buy_opinion_score、aggregate_sell_opinion_score、platform_buy_sentiment_score |
| 价量与波动 | 2 | 0.41 | aggregate_comment_volume、comment_volume_per_platform |
| 其他 | 2 | 0.41 | distinct_user_count_per_platform、total_distinct_participants_count |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `aggregate_buy_opinion_score` | VECTOR | 0.406 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Combined buy sentiment score from all sources for an instrument. |
| 2 | `aggregate_comment_volume` | VECTOR | 0.406 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total number of comments posted across all sources for an instrument. |
| 3 | `aggregate_sell_opinion_score` | VECTOR | 0.406 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Combined sell sentiment score from all sources for an instrument. |
| 4 | `comment_volume_per_platform` | VECTOR | 0.406 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total number of comments posted on the source platform for an instrument. |
| 5 | `distinct_user_count_per_platform` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | Number of unique users participating on the source platform for an instrument. |
| 6 | `platform_buy_sentiment_score` | VECTOR | 0.406 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Buy sentiment score as reported by the source platform. |
| 7 | `platform_sell_sentiment_score` | VECTOR | 0.406 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Sell sentiment score as reported by the source platform. |
| 8 | `total_distinct_participants_count` | VECTOR | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | Number of unique users participating across all sources for an instrument. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

