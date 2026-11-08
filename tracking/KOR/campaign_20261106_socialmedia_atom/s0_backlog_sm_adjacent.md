# 后备数据集短表（Social / Sentiment / News 向）

刷新：2026-11-06 夜（Wave3b 在飞期间）

## 已试
| id | 结果 |
|---|---|
| equity_forum_data | Wave1 全灭 maxS0.38 |
| socialmedia39 | REJECT（ID 向量） |
| other553 | Wave2 全灭 max|S|0.71 |
| news20 decay4 | Wave3 弱灭 max|S|0.49 |
| news20 decay10 | Wave3b 在飞 |

## 下一刀队列
| id | cat | 角色 | 备注 |
|---|---|---|---|
| news66 | news | **下一刀** | 注意力浏览量；模板≥12 已扩；payload 就绪 |
| news54 | news | 备选弱 | 多为 headline/time/flag；连续定价字段稀缺；末选 |
| sentiment27 | sentiment | 拥挤末选 | aC1879 |
| news48 | news | cov偏低 | 0.27 |

## 本回合排除
| id | 原因 |
|---|---|
| news59 | 仅 fiscal_year + event_time_value 日历元数据，无可连续定价字段 |
| sentiment21 / news79 / news_sentiment_transfer / sentiment26 | dead |
| institutions6 | dead ledger |
