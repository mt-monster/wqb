# BE93/94 未点亮塔角落探针（2026-11-12）

> 用户指令：已点亮塔不再投入，集中未点亮塔。本轮攻的是未点亮塔里最后 12 个从未测过的数据集角落。
> 依据：BE89/90 已证「画像 cov=0 不可信」（8/8 有数据），故这些 cov=0 角落必须实测。decay4/SUBINDUSTRY/nan ON，TOP500/D1，全部 ≤6 算子。

## BE93 · 三条真实经济机制（iWpF37Q45fMbEHi77EQGAr，10 臂）

### A. macro27 招聘数据（hiring 增长信号，DEU 从未测）
| 臂 | 构造 | 机制 |
|---|---|---|
| 1-2 | jobsactive 水平 / Δ66 | 招聘存量=扩张意愿 |
| 3 | jobscreated 水平 | 新增岗位=边际扩张 |
| 4 | jobsactive ts_zscore252 | 招聘强度分位 |

### B. pv47 特异收益（特质动量，DEU 从未测）
| 臂 | 构造 | 机制 |
|---|---|---|
| 5 | pv47_spret ts_zscore252 | 特质收益动量（剔市场/行业后） |
| 6 | pv47_spret Δ66 | 特质收益反转 |
| 7 | statssimple_spret ts_zscore252 | 另一口径特异收益 |

### C. news52 电话会议结构（管理层透明度）
| 臂 | 构造 | 机制 |
|---|---|---|
| 8 | chars_in_qa Σ66 | 问答长度=投资者质疑强度 |
| 9 | conference_call_participants Σ66 | 外部关注度 |
| 10 | corporate_participants Σ66 | 管理层出席度 |

## BE94 · 剩余角落（4uHXCM1g94Ft9TMOZnNlMBM，10 臂）

| 臂 | 数据集/字段 | 构造 |
|---|---|---|
| 1-2 | imbalance5 imb5_score | 水平 / Δ66（SHIELD-OIL 韧性分 0-1） |
| 3 | news7 earnings_news_mention_count | Σ66（财报提及热度） |
| 4 | news7 europe_buyback_news_count | Σ66（回购事件流，事件型计数） |
| 5 | news21 event_frequency_label | 水平（StreetEvents 提及计数） |
| 6 | news31 negative_sentiment_probability_2 | 均值22（负向概率，区别于情绪分） |
| 7 | pv71 pairwise_price_volume_corr_score | 水平（价量关系强度） |
| 8 | pv71 ibesest_score_float | 水平（关系网络方向分） |
| 9 | socialmedia12 backtest_hit_ratio | 水平（信号回测命中率） |
| 10 | news31 news_relevance_score | 均值22（新闻相关性） |

## 判读线（协议 v2 L1）

max |S| ≥1.2 ⇒ L2 定向补 / 满波；1.0-1.2 ⇒ 定向补 10 臂；<1.0 ⇒ 判死 + lc 证书（数据在不在一锤定音）。优先看 macro27（招聘）与 pv47（特异收益）——这两个是唯一带成熟学术机制的。