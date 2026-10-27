# other296 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other296` |
| 名称 | Corporate Earnings Call Sentiment Data |
| 类别 | OTHER |
| 数据字段数(平台) | 19 |
| 覆盖率 | 0.5649 |
| 平台已有 alpha | 56 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Refinitiv Instrument Codes (RIC) and Bloomberg IDs, enabling users to cross-reference securities across two major financial data platforms. The mapping is essential for integrating, reconciling, and aggregating data from Bloomberg and Refinitiv sources, facilitating seamless data analysis and portfolio management. While not directly predictive of price movements, the dataset is crucial for ensuring data consistency and accuracy in multi-source financial research, allowing analysts and quants to link disparate datasets and enhance the reliability of their models and analytics.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **19** |
| 类型分布 | VECTOR×19 |
| 平均覆盖率 | **0.565** |
| 覆盖率区间 | 0.56 ~ 0.57 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 19 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 16 | 84.2% |
| DEAD | 3 | 15.8% |

- 已实测字段：**3** 个（16%），best_sharpe 最高 **0.79**，中位 0.68

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 9 | 0.56 | oth296_daily_prob_pos、oth296_sentiment、oth296_prob_pos |
| 其他 | 5 | 0.56 | oth296_daily_topic_count、oth296_daily_word_count、oth296_topic_count |
| 盈利与财务 | 2 | 0.56 | oth296_daily_call_time、oth296_call_time |
| 元数据与非信号 | 2 | 0.56 | oth296_daily_received_time、oth296_received_time |
| 风险与质量 | 1 | 0.57 | oth296_daily_confidence |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth296_daily_prob_pos` | VECTOR | 0.568 | 情绪与新闻 | 1 | 0.79 | — | — | DEAD | Probability that sentiment is positive; part of a three-class distribution summing to 1 |
| 2 | `oth296_sentiment` | VECTOR | 0.562 | 情绪与新闻 | 1 | 0.68 | — | — | DEAD | Trinary sentiment label for the section/topic based on highest probability: 1=positive, 0=neutral, -1=negative |
| 3 | `oth296_prob_pos` | VECTOR | 0.562 | 情绪与新闻 | 6 | 0.64 | — | — | DEAD | Raw probability that the topic sentiment is positive; POS/NTR/NEG probabilities sum to 1 |
| 4 | `oth296_daily_call_time` | VECTOR | 0.568 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The date and time of the earnings call in UTC |
| 5 | `oth296_daily_confidence` | VECTOR | 0.568 | 风险与质量 | 0 | — | — | — | UNUSABLE | Confidence score derived from Prob_ fields, scaled between 0 and 1 (approx. (max Prob − 0.333)/0.666) |
| 6 | `oth296_daily_prob_neg` | VECTOR | 0.568 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Probability that sentiment is negative; part of a three-class distribution summing to 1 |
| 7 | `oth296_daily_prob_ntr` | VECTOR | 0.568 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Probability that sentiment is neutral; part of a three-class distribution summing to 1 |
| 8 | `oth296_daily_received_time` | VECTOR | 0.568 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | UTC timestamp when Alexandria received the transcript text |
| 9 | `oth296_daily_sentiment` | VECTOR | 0.568 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Trinary sentiment label for the section/topic: 1 positive, 0 neutral, -1 negative, based on highest probability |
| 10 | `oth296_daily_topic_count` | VECTOR | 0.568 | 其他 | 0 | — | — | — | UNUSABLE | Count of times the identified topic is discussed in the section |
| 11 | `oth296_daily_word_count` | VECTOR | 0.568 | 其他 | 0 | — | — | — | UNUSABLE | Number of words in the transcript section |
| 12 | `oth296_call_time` | VECTOR | 0.562 | 盈利与财务 | 0 | — | — | — | UNUSABLE | UTC date and time of the earnings call |
| 13 | `oth296_confidence` | VECTOR | 0.562 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Normalized confidence of the sentiment classification derived from the Prob_ fields; ranges from 0 to 1 |
| 14 | `oth296_prob_neg` | VECTOR | 0.562 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Raw probability that the topic sentiment is negative; POS/NTR/NEG probabilities sum to 1 |
| 15 | `oth296_prob_ntr` | VECTOR | 0.562 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Raw probability that the topic sentiment is neutral; POS/NTR/NEG probabilities sum to 1 |
| 16 | `oth296_received_time` | VECTOR | 0.562 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | UTC timestamp when Alexandria received the transcript text |
| 17 | `oth296_topic_count` | VECTOR | 0.562 | 其他 | 0 | — | — | — | UNUSABLE | Number of times the identified topic is discussed within the section |
| 18 | `oth296_word_count` | VECTOR | 0.562 | 其他 | 0 | — | — | — | UNUSABLE | Number of words in the transcript section |
| 19 | `oth296_wqreceivetime` | VECTOR | 0.562 | 其他 | 0 | — | — | — | UNUSABLE | Epoch time added by WQ. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

