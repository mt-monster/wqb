# DEU / TOP500 / D1 — sentiment33 字段全画像

> 生成时间：2026-11-18｜数据源：`mcp__wq-brain-http__get_datafields`（region=DEU, universe=TOP500, delay=1, dataset_id=sentiment33, `filter_sharpe=false`）
> 分母对账：每次返回体都带 `platform_count=255`；`## 字段全表` 列出 **255** 行，去重后 255 个字段 id，缺口 0。
> 类型分布：VECTOR 255；`pyramidMultiplier` 全为 1.8；`dateCreated` 全为 2026-07-01。
> 取数方式：整集一次拉取时返回体约 182 KB，被工具结果预算截断（`[Tool output truncated by resultBudget: originalBytes=181900]`），
> 故改为 **14 个前缀分片逐片实读**。各分片 `count == returned`（44/39/39/41/44/3/5/2/13/5/5/5/5/5），
> 分片按前缀互斥，加总 255 = `platform_count`，无重复、无遗漏。
> 注：分片返回的 `truncated_reason="search_window_capped"` 是平台对 `search` 的 100 条搜索窗上限标记；
> 本集单片最多 44 条，远未触窗，故不构成截断。

## 0. 聚合统计

### 0.1 总量与类型

| 项 | 值 |
|---|---|
| 字段总数 | **255** |
| VECTOR / MATRIX / SYMBOL / GROUP / OTHER | 255 / 0 / 0 / 0 / 0 |
| 去重后字段 id 数 | 255（分片 `count` 加总一致：44+39+39+41+44+3+5+2+13+5+5+5+5+5 = 255） |
| `pyramidMultiplier` | 全为 **1.8**（255/255） |
| `dateCreated` 取值集合 | **{2026-07-01}**（255/255，单次 onboard） |

### 0.2 coverage 分布（整集只有 5 个取值，每个恰好 51 个字段）

| 区间 | 字段数 |
|---|---:|
| ≥ 0.9 | 0 |
| 0.8 – 0.9 | 0 |
| 0.5 – 0.8 | 0 |
| 0.3 – 0.5 | **255** |
| 0 < c < 0.3 | 0 |
| = 0 | 0 |

取值明细（实读计数）：`0.3258`→51、`0.3252`→51、`0.3227`→51、`0.3214`→51、`0.3152`→51。

均值 **0.3221**、中位 **0.3227**、最高 0.3258、最低 0.3152，极差 **0.0106**（3.4%）。
→ 全字段族 coverage 落在 3 个百分点内的窄带里，没有任何「高覆盖」字段。

### 0.3 alphaCount / userCount 分布

| 区间 | alphaCount | userCount |
|---|---:|---:|
| = 0 | **221** | **213** |
| 1 – 5 | 30 | 40 |
| 6 – 20 | 4 | 2 |
| > 20 | 0 | 0 |
| 最大值 | 12（`snt33_sefke1v1_fkw1_method_3_neg`） | 8（`snt33_sefke1v1_fkw1_method_3_neg`） |

- alphaCount 非零值清单（合计 **34** 个字段）：`1`×21、`2`×5、`3`×2、`4`×1、`5`×1、`6`×2、`8`×1、`12`×1 → Σ alphaCount = 78。
- userCount 非零值清单（合计 **42** 个字段）：`1`×30、`2`×4、`3`×3、`4`×2、`5`×1、`7`×1、`8`×1。
→ 86.7%（221/255）字段零 alphaCount，最高热度也只有 12 条 alpha；整个字段族处于**极早期冷启动**。

### 0.4 字段族拆解（按命名空间 / 前缀；实读计数）

| 族前缀 | 字段数 | coverage | 说明 |
|---|---:|---|---|
| `snt33_sefke1v1_fkw1_*` | 44 | 0.3258 | 文档槽 1 的 NLP 派生特征（最全，m9 缺 feature_4） |
| `snt33_sefke1v1_fkw2_*` | 39 | 0.3152 | 文档槽 2 |
| `snt33_sefke1v1_fkw3_*` | 39 | 0.3227 | 文档槽 3 |
| `snt33_sefke1v1_fkw4_*` | 41 | 0.3214 | 文档槽 4（层级计数用 level 2/4，其余槽用 level 3/5） |
| `snt33_sefke1v1_fkw5_*` | 44 | 0.3252 | 文档槽 5 |
| `sentiment_model6_*` | 3 | 0.3152 / 0.3214 / 0.3227 | 槽 2/3/4 的 Method 6 负向计数 |
| `sentiment_model7_*` | 5 | 0.3152 – 0.3258 | 槽 1–5 的 Method 7 feature-1 计数 |
| `sentiment_model8_*` | 2 | 0.3152 / 0.3227 | 槽 2/3 的 Method 8 计数 |
| `sentiment_model9_*` | 13 | 0.3152 – 0.3258 | 槽 1–5 的 Method 9 feature 2/3/4/5 补位 |
| `snt33_1_*` | 5 | 0.3258 | 槽 1 元数据（文本 / 时间戳） |
| `snt33_2_*` | 5 | 0.3152 | 槽 2 元数据 |
| `snt33_3_*` | 5 | 0.3227 | 槽 3 元数据 |
| `snt33_4_*` | 5 | 0.3214 | 槽 4 元数据 |
| `snt33_5_*` | 5 | 0.3252 | 槽 5 元数据 |
| **合计** | **255** | — | — |

### 0.5 结构骨架（对账恒等式，逐项实读校验）

`fkwN` 与 `snt33_N` 的 coverage **逐位相等**（0.3258 / 0.3152 / 0.3227 / 0.3214 / 0.3252），
且 `sentiment_model{6,7,8,9}_*` 的 coverage 恒等于其所属槽 —— 这不是「时间窗口副本」，而是
**5 个并列文档槽（document slot）**：每个槽 N = `snt33_N_*` 元数据 + `fkwN` 特征集 + 该槽在 `sentiment_model*` 命名空间下补出的长尾特征。

```
255 = 5 槽 × (46 信号位 + 5 元数据位)
230 信号字段 = 5 槽 × 46 位
 25 元数据   = 5 槽 × 5 位（headline / event_title / true_timestamp / true_timestamp_epoch / time_ingested_epoch）
```

每槽 46 个信号位构成（实读计数）：
Method 1 六位（pos/neg/neut + filtered 三兄弟）+ Method 2 六位 + Method 3 六位 + Method 4 六位 = 24；
Method 5 = 1；Method 6（pos/neg）= 2；Method 7（feature 1/2）= 2；Method 8 = 1；Method 9（feature 1–11）= 11；
层级计数 = 2；token 统计（valid_tokens_total / max / median）= 3。合计 **46**。

逐槽命名空间分配（实读，用于判「同一语义在哪个前缀」）：

| 槽 | `fkwN` 内 | `sentiment_model*` 补位 | 槽内信号合计 |
|---|---:|---:|---:|
| 1 | 44 | 2（model7 f1、model9 f4） | 46 |
| 2 | 39 | 7（model6 neg、model7 f1、model8、model9 f2/f3/f4/f5） | 46 |
| 3 | 39 | 7（同上） | 46 |
| 4 | 41 | 5（model6 neg、model7 f1、model9 f3/f4/f5） | 46 |
| 5 | 44 | 2（model7 f1、model9 f4） | 46 |
| **合计** | **207** | **23** | **230** |

⚠ 唯一非同构处：槽 4 的两个层级计数是 `group_level_2_count` / `group_level_4_count`，
其余四槽是 `group_level_3_count` / `group_level_5_count`。跨槽做同语义对齐时必须按「层级计数」位对齐，**不能按 level 编号对齐**。

## 字段全表

|字段 id|type|coverage|userCount|alphaCount|dateCreated|描述|
|---|---|---:|---:|---:|---|---|
|`snt33_sefke1v1_fkw1_method_1_pos`|VECTOR|0.3258|0|0|2026-07-01|Method 1 positive token count, total positive tokens in document|
|`snt33_sefke1v1_fkw1_method_1_neg`|VECTOR|0.3258|0|0|2026-07-01|Method 1 negative token count, total negative tokens in document|
|`snt33_sefke1v1_fkw1_method_1_neut`|VECTOR|0.3258|0|0|2026-07-01|Method 1 neutral token count, total neutral tokens in document|
|`snt33_sefke1v1_fkw1_method_1_filtered_pos`|VECTOR|0.3258|0|0|2026-07-01|Method 1 positive count after additional NLP filtering|
|`snt33_sefke1v1_fkw1_method_1_filtered_neg`|VECTOR|0.3258|0|0|2026-07-01|Method 1 negative count after additional NLP filtering|
|`snt33_sefke1v1_fkw1_method_1_filtered_neut`|VECTOR|0.3258|0|0|2026-07-01|Method 1 neutral count after additional NLP filtering|
|`snt33_sefke1v1_fkw1_method_2_pos`|VECTOR|0.3258|2|2|2026-07-01|Method 2 positive weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_2_neg`|VECTOR|0.3258|1|0|2026-07-01|Method 2 negative weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_2_obj`|VECTOR|0.3258|1|1|2026-07-01|Method 2 objectivity weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_2_filtered_pos`|VECTOR|0.3258|3|3|2026-07-01|Method 2 positive score after additional NLP filtering|
|`snt33_sefke1v1_fkw1_method_2_filtered_neg`|VECTOR|0.3258|4|5|2026-07-01|Method 2 negative score after additional NLP filtering|
|`snt33_sefke1v1_fkw1_method_2_filtered_obj`|VECTOR|0.3258|5|6|2026-07-01|Method 2 objectivity score after extra NLP filtering, weighted average 0-1|
|`snt33_sefke1v1_fkw1_method_3_pos`|VECTOR|0.3258|4|4|2026-07-01|Method 3 positive weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_3_neg`|VECTOR|0.3258|8|12|2026-07-01|Method 3 negative weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_3_obj`|VECTOR|0.3258|1|0|2026-07-01|Method 3 objectivity weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_3_filtered_pos`|VECTOR|0.3258|1|0|2026-07-01|Method 3 positive score after extra NLP filtering, weighted average 0-1|
|`snt33_sefke1v1_fkw1_method_3_filtered_neg`|VECTOR|0.3258|7|8|2026-07-01|Method 3 negative score after extra NLP filtering, weighted average 0-1|
|`snt33_sefke1v1_fkw1_method_3_filtered_obj`|VECTOR|0.3258|0|0|2026-07-01|Method 3 objectivity score after extra NLP filtering, weighted average 0-1|
|`snt33_sefke1v1_fkw1_method_4_pos`|VECTOR|0.3258|2|2|2026-07-01|Method 4 positive weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_4_neg`|VECTOR|0.3258|1|0|2026-07-01|Method 4 negative weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_4_obj`|VECTOR|0.3258|0|0|2026-07-01|Method 4 objectivity weighted-average score for the document|
|`snt33_sefke1v1_fkw1_method_4_filtered_pos`|VECTOR|0.3258|2|2|2026-07-01|Method 4 positive score after extra NLP filtering, weighted average|
|`snt33_sefke1v1_fkw1_method_4_filtered_neg`|VECTOR|0.3258|0|0|2026-07-01|Method 4 negative score after extra NLP filtering, weighted average 0-1|
|`snt33_sefke1v1_fkw1_method_4_filtered_obj`|VECTOR|0.3258|0|0|2026-07-01|Method 4 objectivity score after extra NLP filtering, weighted average 0-1|
|`snt33_sefke1v1_fkw1_method_5`|VECTOR|0.3258|0|0|2026-07-01|Method 5 token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_6_pos`|VECTOR|0.3258|0|0|2026-07-01|Method 6 positivity token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_6_neg`|VECTOR|0.3258|0|0|2026-07-01|Method 6 negativity token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_7_feature_2`|VECTOR|0.3258|0|0|2026-07-01|Method 7 feature-2 token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_8`|VECTOR|0.3258|0|0|2026-07-01|Method 8 token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_1`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-1 token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_2`|VECTOR|0.3258|1|0|2026-07-01|Method 9 feature-2 token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_3`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-3 token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_5`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-5 token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_6`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-6 token count, no polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_7`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-7 token count, no polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_8`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-8 token count, no explicit polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_9`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-9 token count, no polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_10`|VECTOR|0.3258|1|0|2026-07-01|Method 9 feature-10 token count, no polarity|
|`snt33_sefke1v1_fkw1_method_9_feature_11`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-11 token count, no polarity|
|`snt33_sefke1v1_fkw1_group_level_3_count`|VECTOR|0.3258|1|1|2026-07-01|Tokens mapped to hierarchical keyword level 3|
|`snt33_sefke1v1_fkw1_group_level_5_count`|VECTOR|0.3258|1|1|2026-07-01|Tokens mapped to hierarchical keyword level 5|
|`snt33_sefke1v1_fkw1_valid_tokens_total`|VECTOR|0.3258|3|3|2026-07-01|Total number of tokens in a sentence|
|`snt33_sefke1v1_fkw1_max_token_length`|VECTOR|0.3258|0|0|2026-07-01|Max sentence token length, averaged per document|
|`snt33_sefke1v1_fkw1_median_token_length`|VECTOR|0.3258|0|0|2026-07-01|Median sentence token length, averaged per document|
|`snt33_sefke1v1_fkw2_method_1_pos`|VECTOR|0.3152|0|0|2026-07-01|Method 1 positive token count, total positive tokens in document|
|`snt33_sefke1v1_fkw2_method_1_neg`|VECTOR|0.3152|0|0|2026-07-01|Method 1 negative token count, total negative tokens in document|
|`snt33_sefke1v1_fkw2_method_1_neut`|VECTOR|0.3152|0|0|2026-07-01|Method 1 neutral token count, total neutral tokens in document|
|`snt33_sefke1v1_fkw2_method_1_filtered_pos`|VECTOR|0.3152|0|0|2026-07-01|Method 1 positive count after extra NLP filtering|
|`snt33_sefke1v1_fkw2_method_1_filtered_neg`|VECTOR|0.3152|0|0|2026-07-01|Method 1 negative count after extra NLP filtering|
|`snt33_sefke1v1_fkw2_method_1_filtered_neut`|VECTOR|0.3152|0|0|2026-07-01|Method 1 neutral count after extra NLP filtering|
|`snt33_sefke1v1_fkw2_method_2_pos`|VECTOR|0.3152|0|0|2026-07-01|Method 2 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_2_neg`|VECTOR|0.3152|0|0|2026-07-01|Method 2 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_2_obj`|VECTOR|0.3152|0|0|2026-07-01|Method 2 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_2_filtered_pos`|VECTOR|0.3152|0|0|2026-07-01|Method 2 positive score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_2_filtered_neg`|VECTOR|0.3152|0|0|2026-07-01|Method 2 negative score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_2_filtered_obj`|VECTOR|0.3152|0|0|2026-07-01|Method 2 objectivity score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_3_pos`|VECTOR|0.3152|0|0|2026-07-01|Method 3 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_3_neg`|VECTOR|0.3152|0|0|2026-07-01|Method 3 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_3_obj`|VECTOR|0.3152|0|0|2026-07-01|Method 3 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_3_filtered_pos`|VECTOR|0.3152|1|1|2026-07-01|Method 3 positive score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_3_filtered_neg`|VECTOR|0.3152|0|0|2026-07-01|Method 3 negative score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_3_filtered_obj`|VECTOR|0.3152|0|0|2026-07-01|Method 3 objectivity score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_4_pos`|VECTOR|0.3152|0|0|2026-07-01|Method 4 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_4_neg`|VECTOR|0.3152|0|0|2026-07-01|Method 4 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_4_obj`|VECTOR|0.3152|0|0|2026-07-01|Method 4 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw2_method_4_filtered_pos`|VECTOR|0.3152|0|0|2026-07-01|Method 4 positive score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_4_filtered_neg`|VECTOR|0.3152|0|0|2026-07-01|Method 4 negative score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_4_filtered_obj`|VECTOR|0.3152|0|0|2026-07-01|Method 4 objectivity score after extra NLP filtering, 0-1|
|`snt33_sefke1v1_fkw2_method_5`|VECTOR|0.3152|1|1|2026-07-01|Method 5 token count detected, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_6_pos`|VECTOR|0.3152|0|0|2026-07-01|Method 6 positivity token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_7_feature_2`|VECTOR|0.3152|0|0|2026-07-01|Method 7 feature-2 token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_9_feature_1`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-1 token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_9_feature_6`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-6 token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_9_feature_7`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-7 token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_9_feature_8`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-8 token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_9_feature_9`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-9 token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_9_feature_10`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-10 token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_method_9_feature_11`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-11 token count, no explicit polarity|
|`snt33_sefke1v1_fkw2_group_level_3_count`|VECTOR|0.3152|0|0|2026-07-01|Tokens or mentions at hierarchy keyword level 3|
|`snt33_sefke1v1_fkw2_group_level_5_count`|VECTOR|0.3152|0|0|2026-07-01|Tokens or mentions at hierarchy keyword level 5|
|`snt33_sefke1v1_fkw2_valid_tokens_total`|VECTOR|0.3152|0|0|2026-07-01|Total number of tokens in a sentence|
|`snt33_sefke1v1_fkw2_max_token_length`|VECTOR|0.3152|0|0|2026-07-01|Max sentence token length, averaged per document|
|`snt33_sefke1v1_fkw2_median_token_length`|VECTOR|0.3152|0|0|2026-07-01|Median sentence token length, averaged per document|
|`snt33_sefke1v1_fkw3_method_1_pos`|VECTOR|0.3227|0|0|2026-07-01|Method 1 positive token count in document|
|`snt33_sefke1v1_fkw3_method_1_neg`|VECTOR|0.3227|0|0|2026-07-01|Method 1 negative token count in document|
|`snt33_sefke1v1_fkw3_method_1_neut`|VECTOR|0.3227|1|1|2026-07-01|Method 1 neutral token count in document|
|`snt33_sefke1v1_fkw3_method_1_filtered_pos`|VECTOR|0.3227|0|0|2026-07-01|Method 1 positive tokens after additional NLP filtering|
|`snt33_sefke1v1_fkw3_method_1_filtered_neg`|VECTOR|0.3227|0|0|2026-07-01|Method 1 negative tokens after additional NLP filtering|
|`snt33_sefke1v1_fkw3_method_1_filtered_neut`|VECTOR|0.3227|0|0|2026-07-01|Method 1 neutral tokens after additional NLP filtering|
|`snt33_sefke1v1_fkw3_method_2_pos`|VECTOR|0.3227|0|0|2026-07-01|Method 2 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_2_neg`|VECTOR|0.3227|0|0|2026-07-01|Method 2 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_2_obj`|VECTOR|0.3227|0|0|2026-07-01|Method 2 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_2_filtered_pos`|VECTOR|0.3227|0|0|2026-07-01|Method 2 positive score after extra NLP filtering|
|`snt33_sefke1v1_fkw3_method_2_filtered_neg`|VECTOR|0.3227|0|0|2026-07-01|Method 2 negative score after extra NLP filtering|
|`snt33_sefke1v1_fkw3_method_2_filtered_obj`|VECTOR|0.3227|1|1|2026-07-01|Method 2 objectivity score after extra NLP filtering|
|`snt33_sefke1v1_fkw3_method_3_pos`|VECTOR|0.3227|0|0|2026-07-01|Method 3 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_3_neg`|VECTOR|0.3227|0|0|2026-07-01|Method 3 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_3_obj`|VECTOR|0.3227|0|0|2026-07-01|Method 3 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_3_filtered_pos`|VECTOR|0.3227|0|0|2026-07-01|Method 3 positive score after extra NLP filtering|
|`snt33_sefke1v1_fkw3_method_3_filtered_neg`|VECTOR|0.3227|0|0|2026-07-01|Method 3 negative score after extra NLP filtering|
|`snt33_sefke1v1_fkw3_method_3_filtered_obj`|VECTOR|0.3227|0|0|2026-07-01|Method 3 objectivity score after extra NLP filtering|
|`snt33_sefke1v1_fkw3_method_4_pos`|VECTOR|0.3227|1|1|2026-07-01|Method 4 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_4_neg`|VECTOR|0.3227|0|0|2026-07-01|Method 4 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_4_obj`|VECTOR|0.3227|0|0|2026-07-01|Method 4 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw3_method_4_filtered_pos`|VECTOR|0.3227|0|0|2026-07-01|Method 4 positive score after extra NLP filtering|
|`snt33_sefke1v1_fkw3_method_4_filtered_neg`|VECTOR|0.3227|0|0|2026-07-01|Method 4 negative score after extra NLP filtering, normalized 0-1|
|`snt33_sefke1v1_fkw3_method_4_filtered_obj`|VECTOR|0.3227|1|0|2026-07-01|Method 4 objectivity score after extra NLP filtering|
|`snt33_sefke1v1_fkw3_method_5`|VECTOR|0.3227|0|0|2026-07-01|Method 5 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_6_pos`|VECTOR|0.3227|1|1|2026-07-01|Method 6 positivity token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_7_feature_2`|VECTOR|0.3227|0|0|2026-07-01|Method 7 feature-2 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_9_feature_1`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-1 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_9_feature_6`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-6 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_9_feature_7`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-7 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_9_feature_8`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-8 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_9_feature_9`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-9 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_9_feature_10`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-10 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_method_9_feature_11`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-11 token count, no explicit polarity|
|`snt33_sefke1v1_fkw3_group_level_3_count`|VECTOR|0.3227|0|0|2026-07-01|Tokens mapped to hierarchy level 3|
|`snt33_sefke1v1_fkw3_group_level_5_count`|VECTOR|0.3227|0|0|2026-07-01|Tokens mapped to hierarchy level 5|
|`snt33_sefke1v1_fkw3_valid_tokens_total`|VECTOR|0.3227|0|0|2026-07-01|Valid tokens in the sentence after preprocessing|
|`snt33_sefke1v1_fkw3_max_token_length`|VECTOR|0.3227|0|0|2026-07-01|Max sentence token length, averaged per document|
|`snt33_sefke1v1_fkw3_median_token_length`|VECTOR|0.3227|0|0|2026-07-01|Median sentence token length, averaged per document|
|`snt33_sefke1v1_fkw4_method_1_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 1 positive token count in document|
|`snt33_sefke1v1_fkw4_method_1_neg`|VECTOR|0.3214|0|0|2026-07-01|Method 1 negative token count in document|
|`snt33_sefke1v1_fkw4_method_1_neut`|VECTOR|0.3214|0|0|2026-07-01|Method 1 neutral token count in document|
|`snt33_sefke1v1_fkw4_method_1_filtered_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 1 positive tokens after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_1_filtered_neg`|VECTOR|0.3214|0|0|2026-07-01|Method 1 negative tokens after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_1_filtered_neut`|VECTOR|0.3214|0|0|2026-07-01|Method 1 neutral tokens after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_2_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 2 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_2_neg`|VECTOR|0.3214|0|0|2026-07-01|Method 2 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_2_obj`|VECTOR|0.3214|0|0|2026-07-01|Method 2 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_2_filtered_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 2 positive score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_2_filtered_neg`|VECTOR|0.3214|0|0|2026-07-01|Method 2 negative score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_2_filtered_obj`|VECTOR|0.3214|0|0|2026-07-01|Method 2 objectivity score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_3_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 3 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_3_neg`|VECTOR|0.3214|0|0|2026-07-01|Method 3 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_3_obj`|VECTOR|0.3214|0|0|2026-07-01|Method 3 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_3_filtered_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 3 positive score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_3_filtered_neg`|VECTOR|0.3214|0|0|2026-07-01|Method 3 negative score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_3_filtered_obj`|VECTOR|0.3214|0|0|2026-07-01|Method 3 objectivity score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_4_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 4 positive weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_4_neg`|VECTOR|0.3214|1|1|2026-07-01|Method 4 negative weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_4_obj`|VECTOR|0.3214|0|0|2026-07-01|Method 4 objectivity weighted-average score, 0-1|
|`snt33_sefke1v1_fkw4_method_4_filtered_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 4 positive score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_4_filtered_neg`|VECTOR|0.3214|0|0|2026-07-01|Method 4 negative score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_4_filtered_obj`|VECTOR|0.3214|0|0|2026-07-01|Method 4 objectivity score after extra NLP filtering|
|`snt33_sefke1v1_fkw4_method_5`|VECTOR|0.3214|0|0|2026-07-01|Method 5 token count of this extraction type, no polarity|
|`snt33_sefke1v1_fkw4_method_6_pos`|VECTOR|0.3214|0|0|2026-07-01|Method 6 positivity token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_7_feature_2`|VECTOR|0.3214|0|0|2026-07-01|Method 7 feature-2 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_8`|VECTOR|0.3214|0|0|2026-07-01|Method 8 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_9_feature_1`|VECTOR|0.3214|0|0|2026-07-01|Method 9 feature-1 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_9_feature_2`|VECTOR|0.3214|2|2|2026-07-01|Method 9 feature-2 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_9_feature_6`|VECTOR|0.3214|1|1|2026-07-01|Method 9 feature-6 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_9_feature_7`|VECTOR|0.3214|0|0|2026-07-01|Method 9 feature-7 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_9_feature_8`|VECTOR|0.3214|0|0|2026-07-01|Method 9 feature-8 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_9_feature_9`|VECTOR|0.3214|0|0|2026-07-01|Method 9 feature-9 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_9_feature_10`|VECTOR|0.3214|0|0|2026-07-01|Method 9 feature-10 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_method_9_feature_11`|VECTOR|0.3214|0|0|2026-07-01|Method 9 feature-11 token count, no explicit polarity|
|`snt33_sefke1v1_fkw4_group_level_2_count`|VECTOR|0.3214|1|1|2026-07-01|Tokens mapped to hierarchical keyword level 2|
|`snt33_sefke1v1_fkw4_group_level_4_count`|VECTOR|0.3214|0|0|2026-07-01|Tokens mapped to hierarchical keyword level 4|
|`snt33_sefke1v1_fkw4_valid_tokens_total`|VECTOR|0.3214|0|0|2026-07-01|Total number of tokens in a sentence|
|`snt33_sefke1v1_fkw4_max_token_length`|VECTOR|0.3214|0|0|2026-07-01|Max sentence token length, averaged at document level|
|`snt33_sefke1v1_fkw4_median_token_length`|VECTOR|0.3214|0|0|2026-07-01|Median sentence token length, averaged at document level|
|`snt33_sefke1v1_fkw5_method_1_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 1 positive token count in document|
|`snt33_sefke1v1_fkw5_method_1_neg`|VECTOR|0.3252|0|0|2026-07-01|Method 1 negative token count in document|
|`snt33_sefke1v1_fkw5_method_1_neut`|VECTOR|0.3252|0|0|2026-07-01|Method 1 neutral token count in document|
|`snt33_sefke1v1_fkw5_method_1_filtered_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 1 positive tokens after extra NLP filtering|
|`snt33_sefke1v1_fkw5_method_1_filtered_neg`|VECTOR|0.3252|0|0|2026-07-01|Method 1 negative tokens after extra NLP filtering|
|`snt33_sefke1v1_fkw5_method_1_filtered_neut`|VECTOR|0.3252|0|0|2026-07-01|Method 1 neutral tokens after extra NLP filtering|
|`snt33_sefke1v1_fkw5_method_2_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 2 positive weighted-average score, 0-100 range 0-1|
|`snt33_sefke1v1_fkw5_method_2_neg`|VECTOR|0.3252|0|0|2026-07-01|Method 2 negative weighted-average score, range 0-1|
|`snt33_sefke1v1_fkw5_method_2_obj`|VECTOR|0.3252|0|0|2026-07-01|Method 2 objectivity weighted-average score, range 0-1|
|`snt33_sefke1v1_fkw5_method_2_filtered_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 2 positive score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_2_filtered_neg`|VECTOR|0.3252|0|0|2026-07-01|Method 2 negative score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_2_filtered_obj`|VECTOR|0.3252|0|0|2026-07-01|Method 2 objectivity score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_3_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 3 positive weighted-average score, range 0-1|
|`snt33_sefke1v1_fkw5_method_3_neg`|VECTOR|0.3252|0|0|2026-07-01|Method 3 negative weighted-average score, range 0-1|
|`snt33_sefke1v1_fkw5_method_3_obj`|VECTOR|0.3252|0|0|2026-07-01|Method 3 objectivity weighted-average score, range 0-1|
|`snt33_sefke1v1_fkw5_method_3_filtered_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 3 positive score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_3_filtered_neg`|VECTOR|0.3252|0|0|2026-07-01|Method 3 negative score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_3_filtered_obj`|VECTOR|0.3252|0|0|2026-07-01|Method 3 objectivity score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_4_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 4 positive weighted-average score, range 0-1|
|`snt33_sefke1v1_fkw5_method_4_neg`|VECTOR|0.3252|0|0|2026-07-01|Method 4 negative weighted-average score, range 0-1|
|`snt33_sefke1v1_fkw5_method_4_obj`|VECTOR|0.3252|0|0|2026-07-01|Method 4 objectivity weighted-average score, range 0-1|
|`snt33_sefke1v1_fkw5_method_4_filtered_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 4 positive score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_4_filtered_neg`|VECTOR|0.3252|0|0|2026-07-01|Method 4 negative score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_4_filtered_obj`|VECTOR|0.3252|0|0|2026-07-01|Method 4 objectivity score after extra NLP filtering, range 0-1|
|`snt33_sefke1v1_fkw5_method_5`|VECTOR|0.3252|0|0|2026-07-01|Method 5 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_6_pos`|VECTOR|0.3252|0|0|2026-07-01|Method 6 positivity token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_6_neg`|VECTOR|0.3252|1|1|2026-07-01|Method 6 negativity token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_7_feature_2`|VECTOR|0.3252|0|0|2026-07-01|Method 7 feature-2 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_8`|VECTOR|0.3252|0|0|2026-07-01|Method 8 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_1`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-1 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_2`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-2 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_3`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-3 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_5`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-5 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_6`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-6 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_7`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-7 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_8`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-8 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_9`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-9 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_10`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-10 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_method_9_feature_11`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-11 token count, no explicit polarity|
|`snt33_sefke1v1_fkw5_group_level_3_count`|VECTOR|0.3252|0|0|2026-07-01|Tokens extracted for the level-3 keyword group|
|`snt33_sefke1v1_fkw5_group_level_5_count`|VECTOR|0.3252|0|0|2026-07-01|Tokens extracted for the level-5 keyword group|
|`snt33_sefke1v1_fkw5_valid_tokens_total`|VECTOR|0.3252|0|0|2026-07-01|Total number of tokens in a sentence|
|`snt33_sefke1v1_fkw5_max_token_length`|VECTOR|0.3252|0|0|2026-07-01|Max sentence token length, averaged per document|
|`snt33_sefke1v1_fkw5_median_token_length`|VECTOR|0.3252|0|0|2026-07-01|Median sentence token length, averaged per document|
|`sentiment_model6_negative_score_fkw2`|VECTOR|0.3152|1|1|2026-07-01|Method 6 negativity token count, no explicit polarity (slot 2)|
|`sentiment_model6_negative_score_fkw3`|VECTOR|0.3227|0|0|2026-07-01|Method 6 negativity token count, no explicit polarity (slot 3)|
|`sentiment_model6_negative_score_fkw4`|VECTOR|0.3214|1|1|2026-07-01|Method 6 negativity token count, no explicit polarity (slot 4)|
|`sentiment_model7_score1_fkw1`|VECTOR|0.3258|1|1|2026-07-01|Method 7 feature-1 token count, no explicit polarity (slot 1)|
|`sentiment_model7_score1_fkw2`|VECTOR|0.3152|0|0|2026-07-01|Method 7 feature-1 token count, no explicit polarity (slot 2)|
|`sentiment_model7_score1_fkw3`|VECTOR|0.3227|1|1|2026-07-01|Method 7 feature-1 token count, no explicit polarity (slot 3)|
|`sentiment_model7_score1_fkw4`|VECTOR|0.3214|3|6|2026-07-01|Method 7 feature-1 token count, no explicit polarity (slot 4)|
|`sentiment_model7_score1`|VECTOR|0.3252|1|1|2026-07-01|Method 7 feature-1 token count, no explicit polarity (slot 5)|
|`sentiment_model8_score_fkw2`|VECTOR|0.3152|0|0|2026-07-01|Method 8 token count, no explicit polarity (slot 2)|
|`sentiment_model8_score_fkw3`|VECTOR|0.3227|1|1|2026-07-01|Method 8 token count, no explicit polarity (slot 3)|
|`sentiment_model9_score2_fkw2`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-2 token count (slot 2)|
|`sentiment_model9_score2_fkw3`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-2 token count (slot 3)|
|`sentiment_model9_score3_fkw2`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-3 token count (slot 2)|
|`sentiment_model9_score3_fkw3`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-3 token count (slot 3)|
|`sentiment_model9_score3_fkw4`|VECTOR|0.3214|1|0|2026-07-01|Method 9 feature-3 token count (slot 4)|
|`sentiment_model9_score4_fkw1`|VECTOR|0.3258|0|0|2026-07-01|Method 9 feature-4 token count (slot 1)|
|`sentiment_model9_score4_fkw2`|VECTOR|0.3152|0|0|2026-07-01|Method 9 feature-4 token count (slot 2)|
|`sentiment_model9_score4_fkw3`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-4 token count (slot 3)|
|`sentiment_model9_score4_fkw4`|VECTOR|0.3214|0|0|2026-07-01|Method 9 feature-4 token count (slot 4)|
|`sentiment_model9_score4`|VECTOR|0.3252|0|0|2026-07-01|Method 9 feature-4 token count (slot 5)|
|`sentiment_model9_score5_fkw2`|VECTOR|0.3152|1|1|2026-07-01|Method 9 feature-5 token count (slot 2)|
|`sentiment_model9_score5_fkw3`|VECTOR|0.3227|0|0|2026-07-01|Method 9 feature-5 token count (slot 3)|
|`sentiment_model9_score5_fkw4`|VECTOR|0.3214|0|0|2026-07-01|Method 9 feature-5 token count (slot 4)|
|`snt33_1_headline`|VECTOR|0.3258|1|2|2026-07-01|Event headline, raw text (slot 1)|
|`snt33_1_event_title`|VECTOR|0.3258|0|0|2026-07-01|Event title, raw text (slot 1)|
|`snt33_1_true_timestamp`|VECTOR|0.3258|0|0|2026-07-01|Document modified time, UTC ISO-8601 string (slot 1)|
|`snt33_1_true_timestamp_epoch`|VECTOR|0.3258|0|0|2026-07-01|true_timestamp as Unix epoch seconds UTC (slot 1)|
|`snt33_1_time_ingested_epoch`|VECTOR|0.3258|0|0|2026-07-01|Document ingestion time, Unix epoch seconds UTC (slot 1)|
|`snt33_2_headline`|VECTOR|0.3152|0|0|2026-07-01|Event headline, raw text (slot 2)|
|`snt33_2_event_title`|VECTOR|0.3152|0|0|2026-07-01|Event title, raw text (slot 2)|
|`snt33_2_true_timestamp`|VECTOR|0.3152|0|0|2026-07-01|Document modified time, UTC ISO-8601 string (slot 2)|
|`snt33_2_true_timestamp_epoch`|VECTOR|0.3152|1|1|2026-07-01|true_timestamp as Unix epoch seconds UTC (slot 2)|
|`snt33_2_time_ingested_epoch`|VECTOR|0.3152|0|0|2026-07-01|Document ingestion time, Unix epoch seconds UTC (slot 2)|
|`snt33_3_headline`|VECTOR|0.3227|0|0|2026-07-01|Event headline, raw text (slot 3)|
|`snt33_3_event_title`|VECTOR|0.3227|0|0|2026-07-01|Event title, raw text (slot 3)|
|`snt33_3_true_timestamp`|VECTOR|0.3227|0|0|2026-07-01|Document modified time, UTC ISO-8601 string (slot 3)|
|`snt33_3_true_timestamp_epoch`|VECTOR|0.3227|0|0|2026-07-01|true_timestamp as Unix epoch seconds UTC (slot 3)|
|`snt33_3_time_ingested_epoch`|VECTOR|0.3227|0|0|2026-07-01|Document ingestion time, Unix epoch seconds UTC (slot 3)|
|`snt33_4_headline`|VECTOR|0.3214|0|0|2026-07-01|Event headline, raw text (slot 4)|
|`snt33_4_event_title`|VECTOR|0.3214|0|0|2026-07-01|Event title, raw text (slot 4)|
|`snt33_4_true_timestamp`|VECTOR|0.3214|0|0|2026-07-01|Document modified time, UTC ISO-8601 string (slot 4)|
|`snt33_4_true_timestamp_epoch`|VECTOR|0.3214|0|0|2026-07-01|true_timestamp as Unix epoch seconds UTC (slot 4)|
|`snt33_4_time_ingested_epoch`|VECTOR|0.3214|0|0|2026-07-01|Document ingestion time, Unix epoch seconds UTC (slot 4)|
|`snt33_5_headline`|VECTOR|0.3252|0|0|2026-07-01|Event headline, raw text (slot 5)|
|`snt33_5_event_title`|VECTOR|0.3252|0|0|2026-07-01|Event title, raw text (slot 5)|
|`snt33_5_true_timestamp`|VECTOR|0.3252|0|0|2026-07-01|Document modified time, UTC ISO-8601 string (slot 5)|
|`snt33_5_true_timestamp_epoch`|VECTOR|0.3252|0|0|2026-07-01|true_timestamp as Unix epoch seconds UTC (slot 5)|
|`snt33_5_time_ingested_epoch`|VECTOR|0.3252|0|0|2026-07-01|Document ingestion time, Unix epoch seconds UTC (slot 5)|

行数核对：255 行 = 230 信号字段 + 25 元数据字段，与 `platform_count=255` 相等，缺口 0。
列含义：`coverage` / `userCount` / `alphaCount` / `dateCreated` 均为平台原值实读，未做任何估算或补值。

## 2. 字段族拆解（按经济含义，与 §0.4 的命名空间切法互补）

一个「文档槽」内的 46 个信号位，按抽取引擎可分为 9 个语义族：

| 语义族 | 每槽位数 | 全表位数 | 值域性质 | 说明 |
|---|---:|---:|---|---|
| Method 1（词典计数） | 6 | 30 | 无界非负计数 | pos / neg / neut 各带 filtered 版 |
| Method 2（加权平均分） | 6 | 30 | 有界 0–1 | pos / neg / obj，各带 filtered 版 |
| Method 3（加权平均分） | 6 | 30 | 有界 0–1 | 同上，全表热度最高族 |
| Method 4（加权平均分） | 6 | 30 | 有界 0–1 | 同上 |
| Method 5（无极性计数） | 1 | 5 | 无界非负计数 | 单一字段 |
| Method 6（正/负计数） | 2 | 10 | 无界非负计数 | pos 与 neg 分列 |
| Method 7（feature 1/2 计数） | 2 | 10 | 无界非负计数 | feature-1 在 model7 命名空间 |
| Method 8（无极性计数） | 1 | 5 | 无界非负计数 | 单一字段 |
| Method 9（feature 1–11 计数） | 11 | 55 | 无界非负计数 | 编号在 fkw 与 model9 两个命名空间交替 |
| 层级计数 | 2 | 10 | 无界非负计数 | 槽 1/2/3/5 用 level 3+5；槽 4 用 level 2+4 |
| token 统计 | 3 | 15 | 无界非负（长度） | valid_tokens_total / max / median token length |
| **单槽合计** | **46** | **230** | — | — |

另加每槽 5 个元数据位（`snt33_N_*`）：25 个，合计 255。

## 3. 可用性三分（不是所有 255 个都能进表达式）

### 3.1 信号：有界无量纲评分——90 个字段（35.3%）

Method 2/3/4 的 `pos` / `neg` / `obj` 及对应 `filtered_*`，平台描述均为 "weighted average … (0–1)"。
3 个方法 × 6 位 × 5 槽 = **90**。

**结论：开箱可用**，直接 `rank` / `zscore` 即可（无需再除总量）。
这是本集唯一有界无量纲的族；历史热度也集中在这里：
`snt33_sefke1v1_fkw1_method_3_neg`（uC 8 / aC 12）与 `snt33_sefke1v1_fkw1_method_3_filtered_neg`（uC 7 / aC 8）
是全表最热的两个字段，说明既有用法集中在「Method 3 负向情绪」。

### 3.2 计数类：需归一化——140 个字段（54.9%）

Method 1 六位、Method 5、Method 6 pos/neg、Method 7 feature 1/2、Method 8、Method 9 feature 1–11、
`group_level_*_count`（2 位）、`valid_tokens_total`、`max_token_length` / `median_token_length`
= 28 位/槽 × 5 槽 = **140**。

**结论：不可直接横截面比较**——原值被「文档长度 / 事件条数」这个混淆因子主导，而 coverage 仅 0.32。
必须先归一化：`divide(计数, valid_tokens_total)` 得占比，或 `rank` / `zscore` / `ts_rank` 后再用。
⚠ `max_token_length` / `median_token_length` 反映的是文档排版，不是情绪，建议只作控制变量而非主信号。

### 3.3 元数据：不可用作信号——25 个字段（9.8%）

`snt33_{1,2,3,4,5}_{headline, event_title, true_timestamp, true_timestamp_epoch, time_ingested_epoch}`。

- `headline` / `event_title` 是**原始文本**（VECTOR 承载的字符串）；
- `true_timestamp` 是 **ISO-8601 字符串**；`true_timestamp_epoch` / `time_ingested_epoch` 是 Unix 秒。

**结论：不可用于表达式**（平台算子对字符串/时间戳向量无定义）。仅可用于研究期的文档对齐、
事件去重、时效衰减窗口设定。
⚠ 两个坑：① `filter_sharpe=false` 下它们照样出现在目录里，极易被误当信号；
② `true_timestamp` 与 `true_timestamp_epoch` 是**同一值的两种编码**，属内部冗余。

### 3.4 三分一致性检查

- 90 + 140 + 25 = **255** ✓
- 全部字段 coverage 落在 0.3152–0.3258 的窄带内，**没有任何高覆盖字段**：任一股票日在任一时点大约只有
  1/3 的历史窗口内有该集数据。任何表达式都必须能处理「无文档 = NaN」，填充策略要显式写，不能依赖隐式填充。
- 5 个槽的 coverage 各自独立（0.3152 / 0.3214 / 0.3227 / 0.3252 / 0.3258），相差 ≤ 3.4%
  ⇒ **五个槽的股票覆盖几乎相同**，它们不是「覆盖互补的分片」，而是同一批股票的五份并列文档槽。

## 4. 同构冗余与去重

### 4.1 冗余规模（实读计数，非估算）

- 230 个信号字段 → **只有 48 个不同语义位**。算法：一个槽的 46 位里，44 位是五槽共有的非层级位；
  层级计数位跨槽并不同名 —— 槽 1/2/3/5 是 `level_3` + `level_5`，槽 4 是 `level_2` + `level_4`，
  并集共 4 个 → 44 + 4 = **48**。
  ⇒ **182 个字段是同语义跨槽副本，冗余率 79.1%**（182/230）。
- `fkw1..fkw5` 五族合计 207 字段；`sentiment_model6/7/8/9_*` 的 23 字段**不是新语义**，而是同一语义在其他槽上的命名空间补位
  （逐槽分配见 §0.5 表）。
  → **不能把 `sentiment_model*` 当作独立信号族**，必须与 `fkwN` 按槽位对齐后再去重。

### 4.2 命名空间陷阱（实读确认，必须按槽对齐）

| 字段名前缀形态 | 实际所属槽 | 依据 |
|---|---|---|
| `sentiment_model7_score1`（无后缀） | **槽 5** | coverage 0.3252 = fkw5 |
| `sentiment_model9_score4`（无后缀） | **槽 5** | coverage 0.3252 = fkw5 |
| `sentiment_model6_negative_score_fkw{2,3,4}` | 槽 2/3/4 | coverage 0.3152/0.3227/0.3214 |
| `sentiment_model8_score_fkw{2,3}` | 槽 2/3 | coverage 0.3152/0.3227 |
| `sentiment_model7_score1_fkw{1,2,3,4}` | 槽 1/2/3/4 | coverage 逐槽一致 |
| `sentiment_model9_score{2,3,4,5}_fkwN` | 槽 N | coverage 逐槽一致 |

### 4.3 去重结论

1. **去重后 48 个语义位**（230 → 48，降 79.1%）。单槽建模取任一槽的 46 位即可，无需跨槽拼接。
2. **跨槽不可当独立信号腿**：5 个槽 coverage 几乎相同、语义完全对齐，`add(槽1信号, 槽2信号)` 属同源混腿
   （违反仓库 `mixed_signal_leg_ban_v1`）。合理用法是**选一个槽 + 组内语义去重**，
   或把 5 槽做横截面合并（`group_rank` / 取均值）**当作单一信号**，而不是并行加腿。
3. **同槽内仍有近似重复**：`method_N_*` 与 `method_N_filtered_*` 是同一引擎过滤前后两版，通常高度相关；
   `_pos` / `_neg` / `_obj` 在一篇文档上近似互补共线。单条表达式建议每槽最多取 1–2 个语义位。
4. **零热度噪声**：alphaCount 与 userCount 全为 0 的字段有 **221 / 213** 个，这批字段没有任何历史验证，
   仅凭语义不可信。按用户热度排序，全表只有 34 个字段有 alphaCount，其中 21 个只有 1。

## 5. 引用本档案前的强制校验

```bash
python tools/gates/field_profile_completeness_gate.py \
    --profile tracking/DEU/reference/datasets/sentiment33.md
```

该闸三判据：① `## 字段全表` 逐字段真实 id、无通配占位；② 每个字段在档案内均有带数字读数的行；
③ 字段全表行数 == 实测行数。本档案需 exit 0 才可作为选区/建族依据。

## 6. 遗留说明（本轮未复跑，仅作线索）

上一版本档案曾记录过一组单字段探针读数（`NONE / decay0 / P0Y0M0D` 下对
`snt33_sefke1v1_fkw1_method_3_neg` / `method_3_pos` 的覆盖率、非零率、N 放大与比值四项读数），
以及据此推出的「必须长窗口聚合」模板白名单。

**本轮（2026-11-18）未复跑这批探针**（本轮任务范围是全字段静态画像，未派发仿真），
故不在此重述具体数字。引用前须用 `create_multi_simulation` 重新实测；
静态画像层面能确认的只有一条：**全字段 coverage 0.3152–0.3258、无高覆盖字段**，
因此任何表达式都必须显式处理缺失，不能假设逐日满截面。
