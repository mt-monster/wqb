# s1_news85 Wave1 · 模板池与画像（EUR / TOP2500 / D1）

> 数据集：`news85`（Deep Learning News Sentiment，22 字段 / 20 个 MATRIX）· category = **news**（NEWS 塔 1/3，未点亮，差 2 颗）
> 状态：**备料完成，待槽位派发**（在飞：第44批跨厂商合成、第46批 insider_feats 换档）

## 一、字段画像

| 族 | 字段 | 类型 | cov | aC | 语义 |
|---|---|---|---|---|---|
| 总量 | `aggregate_sentiment_total` | MATRIX | 0.8387 | 37 | 窗口内情绪得分**总量**（≈ 条数 × 平均强度） |
| 总量(通道) | `sentiment1_aggregate_total` / `sentiment2_aggregate_total` | MATRIX | 0.8387 | 11 / 9 | 两个独立情绪引擎各自的情绪总量 |
| 均值 | `sentiment_overall_average` / `sentiment1_average_value` / `sentiment2_average_value` / `sentiment2_central_tendency` | MATRIX | 0.8387 | 15 / 19 / 9 / 19 | 平均情绪强度 |
| 中位数 | `sentiment_overall_median` / `sentiment1_median_value` | MATRIX | 0.8387 | 10 / 9 | 中位情绪（抗极端值） |
| 极值 | `sentiment_overall_minimum` / `sentiment1_lowest_score` / `sentiment2_lowest_score` / `sentiment2_highest_score` / `peak_sentiment_value` | MATRIX | 0.8387 | 11 / 15 / 32 / 8 / 14 | 极值情绪 / 峰值 |
| **分布矩** | `sentiment_distribution_skewness` / `sentiment1_distribution_skewness` / `sentiment2_distribution_skewness` | MATRIX | 0.8387 | 11 / **6** / 8 | **情绪分布偏度（三阶矩）** |
| 覆盖强度 | `headline_item_count` / `normalized_headline_count` | MATRIX | 0.8387 | 120 / 21 | 新闻条数（关注度） |
| 原始分 | `sentiment1_raw_score` / `sentiment2_raw_score` / `mws85_sentiment` | VECTOR | 0.7182 | 9 / 9 / 50 | 事件级原始分（需 vec_*） |

**画像结论**：① **20/22 是 MATRIX** ⇒ 算子便宜（2–3 个），不踩 event 型算子禁令的坑；② **cov 0.8387** 高于论坛 0.7 死线；③ **aC 6–37**（分布矩族尤低）⇒ 几乎无人开采；④ 同时具备**五种互异几何**：水平量 / 均值 / 三阶矩 / 极值 / 条数。

## 二、为什么它与已判死的三个 NEWS 情绪面不同

| 已失败 | 形式 | S | 与 news85 的关键差异 |
|---|---|---:|---|
| news46 `mws46_ravenpack_mean_ess` | VECTOR 情绪**均值** | 0.70 | news85 有**总量**与**偏度**，且是 MATRIX（免聚合） |
| news46 `mws46_mcp` | **event 型**，`ts_mean`/`ts_backfill` 均报错 | — | news85 全部 MATRIX，无算子禁令风险 |
| news_sentiment_nlp vader | VECTOR 情绪水平 cov 0.9134 | −0.10 | 同上；且该集无分布矩字段 |
| news73 `uncertaintyscore` | VECTOR 单维情绪 | 0.22 | 未测 fear/certainty/hype 组合；news85 是双引擎 |
| news48 `nws48_ens` 新奇度 | VECTOR 新奇度 | −0.55 | 新奇度≠情绪 |

⇒ 共同点只是「情绪」这个词，**信息加工方式完全不同**（水平量 / 三阶矩 / 双引擎交互均未测过）⇒ 不构成「同一面 ≥6 全灭」。这是正当的新面，而非重复试错。

## 三、10 个结构互异模板

| # | 模板 | 表达式骨架 | 几何族 | 算子 | 来源 |
|---|---|---|---|---:|---|
| N-01 | 情绪总量水平 | `group_rank(ts_backfill(aggregate_sentiment_total,66), industry)` | 累计水平量 | 2 | 本区铁律（EUR 信号活在水平量） |
| N-02 | 平均情绪水平 | `group_rank(ts_backfill(sentiment_overall_average,66), industry)` | 水平（均值） | 2 | 论坛/文献基线 |
| N-03 | **情绪分布偏度** | `group_rank(ts_backfill(sentiment_distribution_skewness,66), industry)` | **三阶矩** | 2 | 文献（sentiment skewness） |
| N-04 | 均值−中位数差 | `group_rank(subtract(ts_backfill(sentiment_overall_average,66), ts_backfill(sentiment_overall_median,66)), industry)` | 偏度代理（右尾依赖） | 3 | 自建 |
| N-05 | 双引擎同向确认 | `group_rank(multiply(rank(ts_backfill(sentiment1_average_value,66)), rank(ts_backfill(sentiment2_average_value,66))), industry)` | 交互项 | 4 | 自建（共识强度） |
| N-06 | 双引擎分歧 | `group_rank(subtract(ts_backfill(sentiment1_average_value,66), ts_backfill(sentiment2_average_value,66)), industry)` | 差（不确定性） | 3 | 自建 |
| N-07 | 峰值回落 | `group_rank(subtract(ts_backfill(peak_sentiment_value,66), ts_backfill(sentiment_overall_average,66)), industry)` | 极值−均值 | 3 | 自建 |
| N-08 | 单条新闻情绪强度 | `group_rank(divide(ts_backfill(aggregate_sentiment_total,66), ts_backfill(headline_item_count,66)), industry)` | 比率（去覆盖） | 3 | 自建；⚠ 需防零条数 |
| N-09 | 下行极值情绪 | `multiply(-1, group_rank(ts_backfill(sentiment_overall_minimum,66), industry))` | 极值（负向） | 3 | 自建 |
| N-10 | 情绪动量 | `group_rank(ts_delta(ts_backfill(sentiment_overall_average,66),22), industry)` | 一阶差分 | 3 | 文献（trend） |
| N-11 | 关注度（对照臂） | `group_rank(ts_backfill(headline_item_count,66), industry)` | 覆盖强度 | 2 | 关注度面已衰减，作**对照**判「情绪是否只是覆盖度代理」 |

**结构差异落点**：水平量(N-01) / 均值(N-02) / 三阶矩(N-03/N-04) / 双引擎交互与分歧(N-05/N-06) / 极值(N-07/N-09) / 比率(N-08) / 差分(N-10) / 覆盖度(N-11) —— **7 个互异几何族**。

## 四、派发计划与判读

- 第 1 批：**N-01（水平量）+ N-03（偏度）** —— 两个先验最强、算子最少（各 2 个）的骨架，用最小成本判断「news85 到底有没有信号」。
- 判据：任一 S ≥ 1.2 ⇒ 面成立，继续 N-04…N-10；两条均 < 0.8 ⇒ 该数据集情绪面亦死，转 `news20`（64 字段 cov 0.72–0.96，event 型需先探针）。
- 与 insider 波并行时注意：**NEWS 与 OTHER 同为集合外 category** ⇒ NEWS+OTHER 组合**不受 5 条配额限制**，若后续需要合成降 prod 可直接组腿。

## 五、外部溯源

- 论坛《新闻情绪因子：别再用裸 sentiment 了 —— relevance 加权 + 新颖度过滤》（31 票）：裸 sentiment 排序 Sharpe 波动大 ⇒ 必须加权/过滤。本库的 N-08（去覆盖）与 N-05（双引擎确认）即该思路的两种实现。
- 文献先验（未联网核对）：情绪**分布偏度**（skewness of sentiment）比情绪均值更能预测尾部收益；均值−中位数差是偏度的稳健代理；多引擎分歧度（disagreement）在新闻密集期升高，与未来波动正相关、与未来收益负相关。
