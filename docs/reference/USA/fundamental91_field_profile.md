# USA · `fundamental91` 字段画像

> 由 `tools/fields/profile_dataset_fields.py` 生成，输入为 `get_datafields` 原始返回。零平台配额。

## 1 规模与完整性

| 项 | 值 |
|---|---|
| 本次返回字段数 | 407 |
| 平台声明数 `platform_count` | 407 |
| 返回 `count` | 407 |
| 是否完整 `complete` | True |
| 类型分布 | {'VECTOR': 407} |
| 平均 coverage | 0.6051 |
| 判定 | ✅ 完整 |

## 2 可用性分档

### 2.1 coverage

| 档 | 字段数 |
|---|---|
| 0.40–0.70（稀疏，慎用） | 314 |
| <0.40（枯竭） | 54 |
| 0.70–0.90（sub/robust 需关注） | 39 |

### 2.2 拥挤度（决定 prod 相关性风险）

| 档 | 字段数 |
|---|---|
| 零竞争 | 270 |
| 低拥挤（≤50 alpha） | 136 |
| 中拥挤（51–500） | 1 |

零竞争字段（`userCount==0`）：**270** / 407；描述带单位标注：0

## 3 语义结构

| 语义族 | 字段数 | 示例字段 |
|---|---|---|
| 未归类 | 407 | `cat10_primary_sentiment_score2`, `cat10_primary_sentiment_score5`, `cat10_primary_sentiment_score8`, `cat10_secondary_sentiment_score0` |

**时间朝向**（`forecast`=前瞻/预测，`realized`=已实现/事后，`mixed`=差值构造）：

| 朝向 | 字段数 |
|---|---|
| unknown | 407 |

## 4 名字前缀聚类（前 15）

| 前缀 | 字段数 |
|---|---|
| `fnd91_cat0` | 27 |
| `fnd91_cat12` | 27 |
| `fnd91_cat2` | 27 |
| `fnd91_cat3` | 27 |
| `fnd91_cat1` | 26 |
| `fnd91_cat4` | 26 |
| `fnd91_cat13` | 25 |
| `fnd91_cat5` | 25 |
| `fnd91_cat8` | 25 |
| `fnd91_cat11` | 24 |
| `fnd91_cat7` | 20 |
| `fnd91_topic` | 20 |
| `fnd91_cat10` | 19 |
| `fnd91_cat6` | 18 |
| `fnd91_sentiment1` | 10 |

## 5 候选短名单（Top 25，按打分排序）

打分 = 覆盖 40 + 低拥挤 25 + 语义可解释 20 + 前瞻 5（非信号 −30）。**只做排序参考**，仍须过单位闸与机制假设。

| # | 字段 | 类型 | cov | user | alpha | 语义族 | 朝向 | 分 | 描述（截断） |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `fnd91_8k_kic` | VECTOR | 0.866 | 13 | 16 | 未归类 | - | 56.5 | SEC Central Index Key identifying the company |
| 2 | `fnd91_measure_0` | VECTOR | 0.866 | 6 | 7 | 未归类 | - | 56.5 | Count of sentences in the 8-K item text |
| 3 | `fnd91_measure_1` | VECTOR | 0.866 | 7 | 8 | 未归类 | - | 56.5 | Count of syllables in the 8-K item text |
| 4 | `fnd91_measure_2` | VECTOR | 0.866 | 3 | 6 | 未归类 | - | 56.5 | Count of complex words in the item text |
| 5 | `fnd91_measure_3` | VECTOR | 0.866 | 19 | 23 | 未归类 | - | 56.5 | Count of long words in the 8-K item text |
| 6 | `fnd91_measure_4` | VECTOR | 0.866 | 4 | 7 | 未归类 | - | 56.5 | Total word count in the item text |
| 7 | `fnd91_numeric_count` | VECTOR | 0.866 | 3 | 3 | 未归类 | - | 56.5 | Count of numeric figures in the item text |
| 8 | `fnd91_readability_0` | VECTOR | 0.866 | 14 | 15 | 未归类 | - | 56.5 | readability_<0,1,2> : readability measures of text |
| 9 | `fnd91_readability_1` | VECTOR | 0.866 | 2 | 2 | 未归类 | - | 56.5 | readability_<0,1,2> : readability measures of text |
| 10 | `fnd91_readability_2` | VECTOR | 0.866 | 11 | 15 | 未归类 | - | 56.5 | readability_<0,1,2> : readability measures of text |
| 11 | `fnd91_sentiment1_0` | VECTOR | 0.866 | 1 | 2 | 未归类 | - | 56.5 | Word count after filtering by the sentiment1 method |
| 12 | `fnd91_sentiment1_1` | VECTOR | 0.866 | 7 | 7 | 未归类 | - | 56.5 | Positive sentiment score from sentiment model #1 |
| 13 | `fnd91_sentiment1_2` | VECTOR | 0.866 | 3 | 3 | 未归类 | - | 56.5 | Negative sentiment score from sentiment model #1 |
| 14 | `fnd91_sentiment1_3` | VECTOR | 0.866 | 2 | 2 | 未归类 | - | 56.5 | Objective/neutral sentiment score from sentiment model #1 |
| 15 | `fnd91_sentiment1_4` | VECTOR | 0.866 | 5 | 5 | 未归类 | - | 56.5 | Positive sentiment score from sentiment model #2 |
| 16 | `fnd91_sentiment1_5` | VECTOR | 0.866 | 2 | 2 | 未归类 | - | 56.5 | Negative sentiment score from sentiment model #2 |
| 17 | `fnd91_sentiment1_6` | VECTOR | 0.866 | 8 | 13 | 未归类 | - | 56.5 | Objective or neutral sentiment score from sentiment model #2 |
| 18 | `fnd91_sentiment1_7` | VECTOR | 0.866 | 1 | 3 | 未归类 | - | 56.5 | Positive sentiment score from sentiment model #3 |
| 19 | `fnd91_sentiment1_8` | VECTOR | 0.866 | 1 | 1 | 未归类 | - | 56.5 | Negative sentiment score from sentiment model #3 |
| 20 | `fnd91_sentiment1_9` | VECTOR | 0.866 | 4 | 7 | 未归类 | - | 56.5 | Objective or neutral sentiment score from sentiment model #3 |
| 21 | `fnd91_sentiment2_0` | VECTOR | 0.866 | 20 | 23 | 未归类 | - | 56.5 | Positive sentiment score from sentiment family 2 |
| 22 | `fnd91_sentiment2_1` | VECTOR | 0.866 | 6 | 6 | 未归类 | - | 56.5 | Negative sentiment score from the alternate sentiment family (sentiment2) |
| 23 | `fnd91_sentiment2_2` | VECTOR | 0.866 | 3 | 3 | 未归类 | - | 56.5 | Word count from sentiment family 2 |
| 24 | `fnd91_sentiment2_3` | VECTOR | 0.866 | 3 | 4 | 未归类 | - | 56.5 | sentiment2_<3,4> : 2 complexity measures of text |
| 25 | `fnd91_sentiment2_4` | VECTOR | 0.866 | 8 | 10 | 未归类 | - | 56.5 | sentiment2_<3,4> : 2 complexity measures of text |
