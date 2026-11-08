# news36 · EUR / TOPCS1600 / D1 字段画像

> 类型 VECTOR · 15 字段 · cov 0.7713 · category = **news**（×1.3）· αC 15
> 采集：2026-11-07

## 0. 字段

| 族 | 字段 |
|---|---|
| 新颖度 | `mws36_novelty`（100=全新/50=部分/0=旧闻）、`_newest_span` / `_oldest_span`（毫秒间隔） |
| 相关性 | `mws36_relevance`（0–100） |
| 短语计数 | `mws36_sentiment_phrase_positive/negative`（bigram 分类器） |
| 词计数 | `mws36_sentiment_words_positive/negative`、`mws36_total_words` |
| 置信度 | `mws36_sentiment_positive/negative_confidence`、`mws36_key_event_confidence` |
| 元数据 | `mws36_title`（文本）、`mws36_timestamp_time`、`event_effect_magnitude`（未填充） |

## 实测（已终态,multisim `2iWWiE1xN4k28OSatM2QzFM`,密度模板 66/252,FAST/decay15）

| 变体 | alpha id | S | F | 2Y |
|---|---|---|---|---|
| −密度(正短语) | `9qxdxAKx` | −0.30 | −0.07 | −0.09 |
| −密度(正短语×novelty) | `P0oYoXlE` | −0.34 | −0.08 | 0.01 |
| +密度(负短语) | `npvevOz8` | 0.30 | 0.07 | 0.09 |
| +密度(总词数) | `A1VrVOae` | 0.30 | 0.07 | 0.09（与负短语逐位相同——字段冗余） |
| reverse 总词数 | `ZYQdQWWY` | −0.30 | | |

**归因**：① 全族 |S|≤0.34——短语级事件密度不含注意力信息（Ravenpack 的 sse 才有）。② novelty 加权无增益（−0.30→−0.34），论坛「新颖度过滤」对本集无增量。③ 负短语数与总词数读数逐位相同——**负短语在该供应商数据里近似常数占比，计数不携带独立信息**。④ 5 探针快判死归档。
