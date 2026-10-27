# other635 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other635` |
| 名称 | Thomson Reuters News Analytics Equities |
| 类别 | OTHER |
| 数据字段数(平台) | 6 |
| 覆盖率 | 0.6216 |
| 平台已有 alpha | 15 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive news analytics for equities, including over 80 fields across five key categories: relevance, sentiment, novelty, volume, and headline classification. Each news item is scored for every asset it materially mentions, with separate linguistic processing for each asset, such as companies or commodities. The dataset includes granular metadata like timestamps, source, headline tags, and asset identifiers (RIC, PermID), enabling detailed analysis of how news impacts specific securities. By quantifying sentiment, relevance, and novelty, and tracking news volume, this dataset is highly valuable for predicting price movements, identifying market-moving events, and generating alpha signals through systematic news-based strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **6** |
| 类型分布 | VECTOR×6 |
| 平均覆盖率 | **0.622** |
| 覆盖率区间 | 0.49 ~ 0.75 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 3 | 50.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 3 | 50.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 3 | 50.0% |
| UNUSABLE | 3 | 50.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 3 / UNUSABLE 3 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 情绪与新闻 | 4 | 0.69 | headline_character_count、headline_sentiment_score、headline_word_count |
| 元数据与非信号 | 1 | 0.49 | oth635_char_count |
| 宏观与行业 | 1 | 0.49 | oth635_words_count |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `headline_character_count` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of characters in the news headline, excluding spaces. |
| 2 | `headline_sentiment_score` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Numerical sentiment score for the news headline, typically ranging from negative to positive. |
| 3 | `headline_word_count` | VECTOR | 0.750 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Number of words in the news headline or title. |
| 4 | `oth635_char_count` | VECTOR | 0.493 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Count of Unicode characters in decode_title, including whitespace |
| 5 | `oth635_sentiment` | VECTOR | 0.493 | 情绪与新闻 | 0 | — | — | — | UNUSABLE | Neural-derived sentiment score for the event/title in [-1, 1] (negative to positive, 0 neutral) |
| 6 | `oth635_words_count` | VECTOR | 0.493 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Number of tokens/words in the normalized title (purify_title), whitespace-separated |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

