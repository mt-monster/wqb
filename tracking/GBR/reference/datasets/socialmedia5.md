# GBR / socialmedia5（Lexical Breakdown Data，社媒贴文词法拆解）

> 塔：**socialmedia**（GBR/D1，当前 **0/3 未点亮**；乘数 1.3）
> 画像日期 2026-11-24 · `get_datafields(GBR, socialmedia5, TOP700, D1, filter_sharpe=false)`
> 平台实拉：`count=13 / platform_count=13 / returned=13 / complete=true`
> ⚠ 本集在 GBR 无任何历史回测记录 ⇒ 全新机制面。全部 VECTOR（需 `vec_avg`/`vec_sum`），cov 元数据全 0（盲区）。

---

## 字段全表（平台实拉 13/13）

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `scl5_s_createdts_time` | VECTOR | 0.0 | 5 | 5 | 系统接收时间（元数据） |
| `scl5_s_d1_wqreceivetime` | VECTOR | 0.0 | 7 | 6 | UTC 系统入库时间（元数据） |
| `scl5_s_duplicatecount` | VECTOR | 0.0 | 23 | 11 | 重复贴计数（0=原创，>1=重复） |
| `scl5_s_hitscore_averagesentiment` | VECTOR | 0.0 | 41 | 19 | 贴文所有情绪片段均值 |
| `scl5_s_hitscore_highsentiment` | VECTOR | 0.0 | 13 | 11 | 贴文最高情绪分 |
| `scl5_s_hitscore_lowsentiment` | VECTOR | 0.0 | 7 | 6 | 贴文最低情绪分 |
| `scl5_s_hitscore_sentimentcount` | VECTOR | 0.0 | 16 | 12 | 命中情绪词典的词/短语数 |
| `scl5_s_hitscore_wordcount` | VECTOR | 0.0 | 29 | 22 | 贴文总词数 |
| `scl5_s_job` | VECTOR | 0.0 | 10 | 8 | 内部 job 标识（元数据） |
| `scl5_s_post_accountrating_value` | VECTOR | 0.0 | 6 | 6 | 发帖账号质量评分 |
| `scl5_s_postedts_time` | VECTOR | 0.0 | 3 | 3 | 发帖时间（元数据） |
| `scl5_s_publishedts_time` | VECTOR | 0.0 | 5 | 5 | 发布时间（元数据） |
| `sentiment_fragment_score_d1` | VECTOR | 0.0 | 23 | 20 | 贴文片段的 D1 回测安全情绪分 |

---

## 聚合统计

| 指标 | 值 |
|---|---|
| 字段总数 | 13（全部 VECTOR） |
| coverage 分布 | 13/13 = 0.0（GBR 元数据盲区） |
| alphaCount 合计 / 均值 | 189 / **14.5** |
| alphaCount 最大 / 最小 | 41（`scl5_s_hitscore_averagesentiment`）/ 3（`scl5_s_postedts_time`） |
| userCount 合计 / 均值 | 130 / **10** |
| dateCreated | 13/13 = `2026-07-01` |
| 数据集级 | `name=Lexical Breakdown Data` / `category=socialmedia` / `coverage=0.0` / `userCount=77` / `alphaCount=169` / `valueScore=3.0` / `pyramidMultiplier=1.3` |

---

## 字段族拆解

| 族 | 字段 | 机制 |
|---|---|---|
| **A 情绪极性** | `hitscore_averagesentiment`、`hitscore_highsentiment`、`hitscore_lowsentiment`、`sentiment_fragment_score_d1` | 贴文情绪水平/极值/片段分 |
| **B 情绪密度** | `hitscore_sentimentcount`、`hitscore_wordcount` | 情绪词占比（=强度/关注度） |
| **C 账号质量** | `post_accountrating_value` | 发帖者可信度 |
| **D 元数据** | 时间戳 ×3、`duplicatecount`、`job` | 不可作信号（重复数可作噪声门控） |

---

## 可用性三分

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可做信号** | 情绪极性 4 + 密度 2 + 账号质量 1 | VECTOR 折叠后 `ts_zscore`/`rank` |
| **② 门控** | `duplicatecount`（原创性）、`hitscore_wordcount`（长度） | 稀疏/噪声门控 |
| **③ 元数据** | 3 个时间戳、`scl5_s_job` | 不作信号 |

### 10.1 全字段实测（socialmedia5，`rank(ts_backfill(vec_avg(F),250))` @NONE/decay0/trunc0/nanOFF）

> 探针批次：`待发`（与 socialmedia12/insiders1 合并 10 臂）。

| 字段 | 类型 | longCount | shortCount | 有数据 | 备注 |
|---|---|---:|---:|---|---|
| `scl5_s_createdts_time` | VECTOR | 待填 | 待填 | 待填 | 元数据 |
| `scl5_s_d1_wqreceivetime` | VECTOR | 待填 | 待填 | 待填 | 元数据 |
| `scl5_s_duplicatecount` | VECTOR | 待填 | 待填 | 待填 | 门控 |
| `scl5_s_hitscore_averagesentiment` | VECTOR | 待填 | 待填 | 待填 | 情绪主信号 |
| `scl5_s_hitscore_highsentiment` | VECTOR | 待填 | 待填 | 待填 | |
| `scl5_s_hitscore_lowsentiment` | VECTOR | 待填 | 待填 | 待填 | |
| `scl5_s_hitscore_sentimentcount` | VECTOR | 待填 | 待填 | 待填 | |
| `scl5_s_hitscore_wordcount` | VECTOR | 待填 | 待填 | 待填 | |
| `scl5_s_job` | VECTOR | 待填 | 待填 | 待填 | 元数据 |
| `scl5_s_post_accountrating_value` | VECTOR | 待填 | 待填 | 待填 | |
| `scl5_s_postedts_time` | VECTOR | 待填 | 待填 | 待填 | 元数据 |
| `scl5_s_publishedts_time` | VECTOR | 待填 | 待填 | 待填 | 元数据 |
| `sentiment_fragment_score_d1` | VECTOR | 待填 | 待填 | 待填 | D1 情绪分 |

---

## 历史与先验

- 同塔 socialmedia12（buzz/sentiment）与本集同源（社媒帖），**机制不互异**；socialmedia5 是词法拆解，socialmedia12 是聚合情绪/注意力。
- GBR sentiment 塔判死不能直接外推到 socialmedia 塔（不同塔/不同数据集），但**情绪极性在 GBR 大盘多次失效**是强先验 ⇒ 优先测「密度/注意力/账号质量」而非纯极性。
- 论文：Tetlock (2007) 媒体悲观 → 反转；Da-Engelberg-Gao (2011) 注意力 → 短期动量。两者方向相反，**必须本区实测**。

## 适用性结论

- **模板数**：情绪极性/密度/账号质量 3 条；不构成 10 个互异模板，最多贡献 1–2 席。
- **优先级**：低于 risk（已有全闸件）；仅在 risk 第一批收批后仍有余量时开。
