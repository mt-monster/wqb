# news_sentiment_nlp · EUR / TOPCS1600 / D1 字段画像

> 类型 **VECTOR（全部 23 字段）** · cov **0.9134** · category = **other**（×1.5）
> 采集：2026-11-06 · αC 合计 11（最高单字段 `headline_sentence_sentiment_maximum` αC=6）
> 前序：`news_sentiment_dl` 关注度反向天花板 S=0.91 且 sub/robust 结构性 FAIL 已归档；`news54` 时间戳/文本不可用已跳过

## 0. 字段目录（按语义）

| 族 | 字段 | αC | 经济含义 |
|---|---|---|---|
| **关注度** | `headline_word_count_total` / `headline_unique_word_count` / `headline_total_sentence_count` | 0/0/1 | 标题长度=注意力代理 |
| **VADER 情绪** | `headline_sentiment_vader_score` + pos/neg/neu polarity | 0 | 复合情绪 −1..1 |
| **TextBlob** | `headline_textblob_sentiment_score` / `headline_subjectivity_score` | 0/1 | 极性 + 主观性 |
| **句级情绪** | `headline_sentence_sentiment_{average,maximum,median,minimum,variance}` | 2/6/0/1/0 | 句级最值/均值——最大句情绪可能是冲击强度 |
| **SentiWordNet** | pos/neg/neu polarity | 0 | 另一套极性 |
| **可读性** | flesch / gunning / smog / stopword / avg_sentence_length | 0 | 元数据，作辅助 |

## 1. 五问

| # | 问 | 答 |
|---|---|---|
| 1 | 时间 | 事件流量 VECTOR，须 `vec_*` 归约 |
| 2 | 相对性 | 情绪分已标准化，可直接截面排序 |
| 3 | 被定价谁 | 优先测**关注度（词数）反向**（承接 dl 集结论）+ **句级最大情绪**（冲击强度）+ VADER 水平 |
| 4 | 拥挤 | αC≤6，低竞争 |
| 5 | 事件 | 稀疏，窗口 5/22；禁 `ts_decay_linear` |

## 2. 第一批探针（5 条）

1. reverse 词数关注度 22d（承接 dl 集）
2. 句级最大情绪 22d（冲击强度，正向）
3. VADER 复合情绪 22d
4. 主观性 22d
5. reverse 句级最大情绪 22d（对照）

骨架：`rank(group_scale(tail(winsorize(group_zscore(ts_sum(vec_*(·), 22), industry), std=2), lower=0.25, upper=0.75, newval=0.5), industry))` @ SLOW_AND_FAST

## 3. 实测

**第一批探针（已终态,multisim `1AA3Po5r35bMcap19yfJMxVI`）——全部噪声**：

| # | 机制 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|---|
| 1 | reverse 词数关注度 | `gJego13Q` | 0.12 | 0.02 | −0.26 | 0.16 | 0.26 |
| 2 | 句级最大情绪 | `Xg9vYpKx` | 0.19 | 0.03 | 0.44 | 0.23 | 0.36 |
| 3 | VADER 复合 | `bl6rWLLl` | 0.15 | 0.02 | 0.29 | 0.19 | 0.24 |
| 4 | 主观性 | `zq32J991` | 0.05 | 0 | 0.74 | −0.14 | −0.17 |
| 5 | reverse 句级最大 | `LLMmlpp6` | −0.19 | −0.03 | −0.44 | −0.23 | −0.36 |

**归因**：本集标题级 NLP 特征在截面 zscore 骨架下无信号（|S|≤0.19）。与 `news_sentiment_dl` 对比，词数反向在 dl 集还能到 0.91，本集只到 0.12——标题词数的注意力代理弱于全文词数。**两集均归档**（dl 集反向天花板 0.91 结构性 FAIL；本集全噪声）。

**论坛新模板（帖 `43541109631895`，PW58059，78 票）——EUR 已验证的注意力密度骨架**：
```
-ts_rank(ts_mean(vec_count(<VECTOR>), 60), 252)  // 自身历史分位异常高 → 反转
@ FAST / decay 15
```
EUR TOP2500 原样迁移 S=1.60（GBR 1.97）。关键差异：用 `vec_count`（事件个数）而非 `vec_sum`（数值加总）；用 `ts_rank` 自身基线而非截面 `group_zscore`；中性化用 **FAST** 而非 SLOW_AND_FAST。

**密度模板迁移实测（已终态,multisim `2ojhrg7z35cEcqGDsiqFZAL`,FAST/decay15）——本集字段不携带事件密度信息**：

| 字段 | alpha id | S | F | 2Y | sub | robust |
|---|---|---|---|---|---|---|
| `headline_word_count_total` | `pwdMVAnX` | 0.07 | 0.01 | 0.70 | 0.56 | 0.55 |
| `headline_sentiment_vader_score` | `akKQAqN2` | 0.07 | 0.01 | 0.70 | 0.56 | 0.55 |
| `positive_word_count_trna`（dl 集） | `d5W3EAnx` | 0.40 | 0.10 | 0.06 | 0.38 | 0.39 |
| `output_metric_1_trna`（dl 集） | `rKRNJvbd` | 0.40 | 0.10 | 0.06 | 0.38 | 0.39 |

**归因**：① NLP/DL 集的 `vec_count` ≈「当天有无标题/有无词」的 0/1 密度，不是 Ravenpack 式「一天 N 条独立新闻事件」——注意力代理被压成稀疏二元，模板失效。② 前两字段读数逐位相同（同一天有标题则两字段都非空）。③ **本集 + dl 集按「无可用注意力密度源」归档**；模板正确性改由 `news18` 验证（已提交）。
