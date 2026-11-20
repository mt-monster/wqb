# 字段画像 · news_sentiment_transfer（KOR / TOP600 / D1 / sentiment）

> 画像日期：2026-11-19。角色：字段画像员（只画像与归档，**未发任何仿真**，零配额）。
> 数据源（本轮实跑，逐条可复现）：
> - `mcp__wq-brain-http__get_datafields(region=KOR, dataset_id=news_sentiment_transfer, universe=TOP600, delay=1, filter_sharpe=false, max_fields=不传)`
>   → `count=23, platform_count=23, complete=true, pages_fetched=1, returned=23, ordering_scope=KOR/TOP600/D1` ⇒ **对账 23==23==23 通过**。
> - `mcp__wq-brain-http__get_datafields(region=USA, dataset_id=news_sentiment_transfer, universe=TOP3000, delay=1, filter_sharpe=false)`
>   → `count=23, platform_count=23, complete=true`，**同一 23 个字段 id**（仅 coverage 0.947、倍率 1.5）⇒ 跨区字段集一致，KOR 无缺字段。
> - `mcp__wq-brain-http__get_datasets(region=KOR, delay=1, universe=TOP600, search=transfer)`
>   → `news_sentiment_transfer`：name=`Transferred News Sentiment Analytics`，**category=sentiment**，coverage=**0.9654**，fieldCount=**23**，userCount=**142**，alphaCount=**263**，pyramidMultiplier=**1.6**，valueScore=4.0。
>   ⚠ 与候选理由的两处口径核对：直查值 **263/142** 本轮复现；候选理由提到的「category=sentiment 列表页读得 252/137」**本轮不可复现**（同 search 返回 263）⇒ 档案统一引用 **263**，并把 252 记为**未复现的旧读数**。
> - `mcp__wq-brain-http__get_pyramid_alphas()`（本轮实读）→ **KOR/D1 `sentiment` = 0**（news=0, earnings=0, institutions=0, macro=0, imbalance=0, socialmedia=0；analyst=4, fundamental=3, model=3, insiders=3, risk=3, shortinterest=4, other=2, pv=2）⇒ **0 < 3，塔未点亮，status=ok**（与候选理由逐项一致）。
> - `mcp__wqb-db__get_dead_datasets(region=KOR)` → **16 条**：acquisition_model / fundamental44 / institutions6 / model109 / model170 / model192 / model230 / model30 / model32 / model53 / multi_source_model / news79 / sentiment21 / shortinterest3 / smoke_ds / wave30_model252 —— **不含 news_sentiment_transfer**（数据集级未判死）。
> - 直读 `data/wqb.db`：`registry_empirical` id=**153**、`backtest_results`（dataset=`news_sentiment_transfer` 共 **103** 行；另 14 行 dataset=NULL 但表达式只含本集字段）、`wave_results` id=**1645**、`expressions`。
> - 平台复核：`get_alpha_details(RRE988kj / ZYQgpJqx)`（二者 `pyramids.list=[KOR/D1/SENTIMENT ×1.6]`、region=KOR/universe=TOP600/delay=1）；`get_alpha_yearly_stats(RRE988kj)` 十年逐年读数。
> - 既有档案（本轮复核，发现两处漂移，见 §0.4）：`tracking/KOR/reference/datasets/news_sentiment_transfer.md`（快照 2026-10-30）。

---

## 0. 结论先行（给编排器的诚实摘要）

1. **全字段探测完成（无抽样）**：23/23 字段逐 id 列于 §1，逐字段带数字读数于 §2；分母无通配占位。
2. **塔位属实且与候选理由一致**：KOR/D1 `sentiment` = **0/3**，倍率 **1.6**；本轮 `get_pyramid_alphas` 实读，非引用旧值。
3. **判死台账：命中，但定级是「族级」不是「数据集级」**（与候选理由一致，本轮机械复核通过）：
   - 权威行 `registry_empirical` id=153，`entry_id=KOR-NEWS-SENTIMENT-TRANSFER-DEAD`，`family='news_sentiment_transfer sentiment'`，**payload 无 `dataset` 键**，`rule='do not probe news/sentiment aggregate datasets in KOR again'`，`dead_at=2026-08-23`。
   - `get_dead_datasets(KOR)` 16 条**不含**本集 ⇒ 非数据集级。
   - 代码依据：`src/wqb/dead_datasets.py:135-143` —— `_family_of(payload)` 非空且 `fam != ds` ⇒ `level='family'`；payload 连 `dataset` 键都没有时 `_dataset_of()` 返回 None ⇒ 直接落 `_mk(None, "family")`（同文件 `:100-113`）。
4. **⚠ 但判死理由的一句话在本轮实测下不成立**：死因原文「day-frequency aggregated sentiment scores **carry no cross-sectional signal in KOR TOP600**」。KOR 实测有**真实截面**且有一条 **S=0.72 / 2Y=1.43 / TO=7.86% / CW PASS / subU PASS / 十年逐年多空均 >0** 的二阶矩腿（`RRE988kj`，平台实读 `pyramids=[KOR/D1/SENTIMENT]`）。准确表述应是：**本集在 KOR 达不到 S≥1.58 的闸线（KOR 全库最佳 |S|=0.72）**，而不是「无截面信号」。画像员无权撤销判死，按现状如实上报，请编排器/用户裁决是否走 REVOKED 流程。
5. **核心字段是「区间聚合情绪分」的横截面水平值（慢变量）**，但**不是**持股比例/治理评分/股本结构/市值余额那类会计存量。⚠ **本集真正的规模代理在 `*_total_2` / `total_sentiment_score` / `news_article_count` 的裸水平上**（sum 与 count 随媒体覆盖/市值单调增长）——§7 给替代写法（变化量 / 时序分位 / 离散度 / 比值归一），其中①③在 KOR 已有读数。
6. **推荐档**：`KOR/TOP600/D1/STATISTICAL（或实证档 REVERSION_AND_MOMENTUM）/decay4/trunc0.08/pasteurization ON/nanHandling OFF/maxTrade OFF + ts_backfill(22)`；先 2–3 条探针（二阶矩轴 × 分组轴）再决定是否投整波。

---

## 1. 字段全表（分母 = 23；平台 count=23 / platform_count=23 / complete=true；description 平台原文逐字）

| 字段 id | type | coverage | alphaCount | userCount | dateCreated | pyramidMultiplier | description（平台原文，唯一语义依据） |
|---|---|---:|---:|---:|---|---:|---|
| `news_article_count` | MATRIX | 0.9654 | 36 | 29 | 2026-03-01 | 1.6 | Total number of news articles considered for the entity. |
| `news_sentiment_score` | VECTOR | 0.9654 | 19 | 17 | 2026-03-01 | 1.6 | Overall sentiment value derived from news articles for an entity. |
| `normalized_news_article_count` | MATRIX | 0.9654 | 13 | 12 | 2026-03-01 | 1.6 | Number of news articles normalized for comparison across entities. |
| `primary_sentiment_average` | MATRIX | 0.9654 | 31 | 26 | 2026-03-01 | 1.6 | Mean value of the primary sentiment scores for the entity. |
| `primary_sentiment_maximum` | MATRIX | 0.9654 | 8 | 7 | 2026-03-01 | 1.6 | Maximum value observed in the primary sentiment scores. |
| `primary_sentiment_middle_value` | MATRIX | 0.9654 | 9 | 9 | 2026-03-01 | 1.6 | Median value of the primary sentiment scores for the entity. |
| `primary_sentiment_minimum` | MATRIX | 0.9654 | 9 | 8 | 2026-03-01 | 1.6 | Minimum value observed in the primary sentiment scores. |
| `primary_sentiment_skewness_2` | MATRIX | 0.9654 | 5 | 5 | 2026-03-01 | 1.6 | Skewness statistic of the primary sentiment values for the entity. |
| `primary_sentiment_total_2` | MATRIX | 0.9654 | 7 | 7 | 2026-03-01 | 1.6 | Sum of all primary sentiment values for the entity over the period. |
| `primary_sentiment_value` | VECTOR | 0.9654 | 11 | 9 | 2026-03-01 | 1.6 | Main sentiment score calculated for the entity from news data. |
| `secondary_sentiment_average` | MATRIX | 0.9654 | 20 | 20 | 2026-03-01 | 1.6 | Mean value of the secondary sentiment scores for the entity. |
| `secondary_sentiment_maximum` | MATRIX | 0.9654 | 5 | 5 | 2026-03-01 | 1.6 | Maximum value observed in the secondary sentiment scores. |
| `secondary_sentiment_middle_value` | MATRIX | 0.9654 | 23 | 20 | 2026-03-01 | 1.6 | Median value of the secondary sentiment scores for the entity. |
| `secondary_sentiment_minimum` | MATRIX | 0.9654 | 17 | 15 | 2026-03-01 | 1.6 | Minimum value observed in the secondary sentiment scores. |
| `secondary_sentiment_skewness_2` | MATRIX | 0.9654 | 4 | 4 | 2026-03-01 | 1.6 | Skewness statistic of the secondary sentiment values for the entity. |
| `secondary_sentiment_total_2` | MATRIX | 0.9654 | 2 | 2 | 2026-03-01 | 1.6 | Sum of all secondary sentiment values for the entity over the period. |
| `secondary_sentiment_value` | VECTOR | 0.9654 | 21 | 17 | 2026-03-01 | 1.6 | Secondary sentiment score calculated for the entity from news data. |
| `sentiment_distribution_skewness_2` | MATRIX | 0.9654 | 5 | 5 | 2026-03-01 | 1.6 | Skewness of the distribution of sentiment scores for the entity. |
| `sentiment_score_average` | MATRIX | 0.9654 | 17 | 14 | 2026-03-01 | 1.6 | Average sentiment score for the entity over the period. |
| `sentiment_score_maximum` | MATRIX | 0.9654 | 9 | 9 | 2026-03-01 | 1.6 | Highest sentiment score observed for the entity. |
| `sentiment_score_median` | MATRIX | 0.9654 | 13 | 12 | 2026-03-01 | 1.6 | Median sentiment score for the entity over the period. |
| `sentiment_score_minimum` | MATRIX | 0.9654 | 14 | 13 | 2026-03-01 | 1.6 | Lowest sentiment score observed for the entity. |
| `total_sentiment_score` | MATRIX | 0.9654 | 3 | 3 | 2026-03-01 | 1.6 | Sum of all sentiment values for the entity over the period. |

**类型构成实读**：MATRIX 20 + VECTOR 3（`news_sentiment_score` / `primary_sentiment_value` / `secondary_sentiment_value`）= 23。
**计数口径**：字段级 `alphaCount` 合计 = 301，数据集级 `alphaCount` = 263（平台按 alpha 去重，一条 alpha 可用多字段）⇒ 二者不同源、不矛盾。字段级 `userCount` 合计 268 vs 数据集级 142，同理。

---

## 2. 逐字段实测读数表（23 行 = 分母 23，逐字段带数字）

> 列口径：
> - **全区实测** = 直读 `data/wqb.db` `backtest_results`（`dataset='news_sentiment_transfer'`，共 **103** 行：IND 73 / USA 18 / ASI 8 / KOR 4），按**表达式里出现该字段名**（词边界匹配，防前缀串味）统计命中数 n，并取 `max|S|` 的那条。
> - **KOR 实测** = 同表 `region='KOR'` 且表达式含该字段的全部腿（含 14 条 `dataset` 列为 NULL 的探针，归属已由 `get_alpha_details` 平台复核：`pyramids=[KOR/D1/SENTIMENT]`，见 §4）。
> - **法1 有效覆盖** = 从 `long_count/short_count` 读到的真实截面宽度；`未入库` = 该行 `long_count` 为 NULL（本地入库缺口，不臆造）。
> - 元数据 `coverage=0.9654` 是**平台横截面覆盖率**，按 `docs/experience/07` §七 纪律**仅供排序**，不等于「当日非零」。

| 字段 id | type | cov(元数据) | aC | 全区实测（n / max\|S\| / 2Y / alpha / 区） | KOR 实测（最佳 \|S\| / 2Y / TO / alpha） | 法1 有效覆盖（LC/SC） | 角色 · 裁决 |
|---|---|---:|---:|---|---|---|---|
| `news_article_count` | MATRIX | 0.9654 | 36 | n=14 / 0.87 / −0.58 / `xA3MVQEN` / IND | 0.31 / −0.41 / 0.2467 / `N1NLrrg7`（水平）；0.25 / 1.01 / 0.5495 / `KPJvb1Yk`（Δ5） | 已实测 312–322 / 313–325 | 主信号（注意力计数；裸水平=规模代理，见 §7） |
| `news_sentiment_score` | VECTOR | 0.9654 | 19 | n=3 / 0.27 / −0.22 / `npvMqgLl` / USA | 无 KOR 独立腿 | **未实测**（VECTOR 元数据高估风险，07 §七） | 主信号（唯一可算文章级离散度的入口：`vec_stddev`） |
| `normalized_news_article_count` | MATRIX | 0.9654 | 13 | n=10 / 1.64 / −1.43 / `2rwEG506` / IND | 无 KOR 独立腿 | 未实测 | 对照（`news_article_count` 的归一化版本，勿双投） |
| `primary_sentiment_average` | MATRIX | 0.9654 | 31 | n=12 / 0.91 / +0.36 / `QPbeOMNX` / IND | 0.26 / 0.13 / 0.1872 / `omEEzRGE`；0.09 / −0.95 / `akKennWw` | 已实测 252–315 / 324–385 | 主信号（副口径最饱和的水平字段） |
| `primary_sentiment_maximum` | MATRIX | 0.9654 | 8 | n=8 / 0.91 / +0.36 / `QPbeOMNX` / IND | 无 KOR 独立腿 | 未实测 | 对照（极值，须配 `_minimum` 做价差） |
| `primary_sentiment_middle_value` | MATRIX | 0.9654 | 9 | n=2 / 0.22 / +1.12 / `d5bqYmvx` / IND | 无 KOR 独立腿 | 未实测 | 对照（中位，抗极值版水平） |
| `primary_sentiment_minimum` | MATRIX | 0.9654 | 9 | n=7 / 0.91 / +0.36 / `QPbeOMNX` / IND | 无 KOR 独立腿 | 未实测 | 对照（极值另一半） |
| `primary_sentiment_skewness_2` | MATRIX | 0.9654 | 5 | n=7 / 0.75 / −1.23 / `mLmOKQY2` / USA | 无 KOR 独立腿 | 未实测 | 对照（离散度族，方向为负） |
| `primary_sentiment_total_2` | MATRIX | 0.9654 | 7 | n=6 / 1.49 / −1.61 / `j2ALVaRo` / IND | 无 KOR 独立腿 | 未实测 | **排除**（裸 sum ⇒ 规模代理，只能作比值分子） |
| `primary_sentiment_value` | VECTOR | 0.9654 | 11 | n=2 / 0.31 / +0.56 / `e76VZRvp` / IND | 无 KOR 独立腿 | **未实测**（VECTOR） | 对照（`_average` 的向量版，同信息） |
| `secondary_sentiment_average` | MATRIX | 0.9654 | 20 | n=8 / 1.30 / −1.59 / `xA3MVq2q` / IND | 0.56 / −1.55 / 0.2866 / `6XdZ99YY`（primary−secondary 价差腿） | 已实测 272–315 / 323–363 | 对照（双通道价差的一侧） |
| `secondary_sentiment_maximum` | MATRIX | 0.9654 | 5 | n=6 / 0.78 / −1.16 / `e7bANmVN` / IND | 无 KOR 独立腿 | 未实测 | 对照 |
| `secondary_sentiment_middle_value` | MATRIX | 0.9654 | 23 | n=6 / 0.76 / −0.26 / `levxEdGN` / IND | 无 KOR 独立腿 | 未实测 | 对照 |
| `secondary_sentiment_minimum` | MATRIX | 0.9654 | 17 | n=6 / 0.78 / −1.16 / `e7bANmVN` / IND | 无 KOR 独立腿 | 未实测 | 对照 |
| `secondary_sentiment_skewness_2` | MATRIX | 0.9654 | 4 | n=4 / 1.49 / −1.61 / `j2ALVaRo` / IND | 无 KOR 独立腿 | 未实测 | 对照（离散度族） |
| `secondary_sentiment_total_2` | MATRIX | 0.9654 | 2 | n=10 / 1.30 / −1.59 / `xA3MVq2q` / IND | 无 KOR 独立腿 | 未实测 | **排除**（裸 sum ⇒ 规模代理） |
| `secondary_sentiment_value` | VECTOR | 0.9654 | 21 | n=2 / 0.42 / −0.51 / `d5K3rLGx` / USA | 无 KOR 独立腿 | **未实测**（VECTOR） | 对照（`_average` 的向量版） |
| `sentiment_distribution_skewness_2` | MATRIX | 0.9654 | 5 | n=7 / 0.62 / −0.72 / `QPvLN0Jw` / USA | 无 KOR 独立腿 | 未实测 | 主信号（综合通道唯一分布形态字段=分歧代理） |
| `sentiment_score_average` | MATRIX | 0.9654 | 17 | n=**29** / **2.38** / **2.47** / `2rjXKVKZ` / IND（慢×快价差几何） | **0.72 / 1.43 / 0.0786 / `RRE988kj`**（二阶矩）；0.84 / −1.45 / `e75NOjgz`；0.62 / −0.72 / `kqNv3Ak8`；wave203 三条 0.00 / 0.45 / 0.04 | 已实测 318–348 / 313–331（十年逐年 292–348、多空均 >0） | **主信号（本集最强轴）** |
| `sentiment_score_maximum` | MATRIX | 0.9654 | 9 | n=9 / 1.05 / +0.83 / `9qjo8Yd9` / IND | 0.57 / −0.59 / 1.0868 / `Jje0jadj`（max−min 价差腿） | 未入库（wave203 行 `long_count`=NULL） | 对照（极值，配 `_minimum`） |
| `sentiment_score_median` | MATRIX | 0.9654 | 13 | n=8 / 0.37 / +0.02 / `akbJelw5` / IND | 无 KOR 独立腿 | 未实测 | 主信号候选（抗极值版综合水平，KOR 未测） |
| `sentiment_score_minimum` | MATRIX | 0.9654 | 14 | n=8 / 1.05 / +0.83 / `9qjo8Yd9` / IND | 0.57 / −0.59 / 1.0868 / `Jje0jadj`（与 max 同腿） | 未入库 | 对照 |
| `total_sentiment_score` | MATRIX | 0.9654 | 3 | n=1 / 0.80 / −0.41 / `xA3Ml7MN` / IND | 0.29 / −0.78 / 0.2840 / `wpQ3RrO2`（÷count 比值） | 已实测 307–326 / 311–328 | **排除**（裸 sum ⇒ 规模代理；仅可作比值分子） |

注：`primary_sentiment_maximum` / `_minimum` / `_average` 共用 `QPbeOMNX`、`secondary_sentiment_skewness_2` 与 `primary_sentiment_total_2` 共用 `j2ALVaRo`、`secondary_sentiment_total_2` 与 `secondary_sentiment_average` 共用 `xA3MVq2q` —— 同一条 alpha 含多字段，故「最佳读数」可重复出现，n 为该字段的独立命中数。

---

## 3. 语义族与角色划分（以 description 为唯一依据）

| 族 | 字段 | 经济含义（来自 description） | 存量/流量 | 角色 |
|---|---|---|---|---|
| **F1 综合情绪水平** | `sentiment_score_average` / `sentiment_score_median` / `news_sentiment_score`(V) / `total_sentiment_score` | 实体区间内的平均 / 中位 / 总体 / **总和**情绪值 | **存量型**（区间聚合的慢变量；其中 `total` 是 sum ⇒ 兼规模代理） | 主信号（average/median/VECTOR）、排除（total） |
| **F2 双通道水平** | `primary_sentiment_average` / `primary_sentiment_value`(V) / `primary_sentiment_middle_value` / `secondary_*` 同构 4 个 | 主 / 副两条 NLP 通道的情绪分（description 只说 main / secondary，**无质量梯度含义**） | **存量型** | 主信号（primary_average）、对照（其余） |
| **F3 极值** | `sentiment_score_maximum` / `_minimum`、`primary_sentiment_maximum` / `_minimum`、`secondary_sentiment_maximum` / `_minimum` | 区间内最高 / 最低情绪 | **存量型** | 对照（只作 max−min 价差，见 M2） |
| **F4 分布形态 / 分歧** | `sentiment_distribution_skewness_2` / `primary_sentiment_skewness_2` / `secondary_sentiment_skewness_2` | 情绪分布的偏度统计量（**纯形态，不带方向**） | **存量型** | 主信号（综合通道一条）、对照（两通道） |
| **F5 注意力计数** | `news_article_count` / `normalized_news_article_count` | 覆盖该实体的新闻条数（原值 / 跨实体归一） | **流量型**（逐日事件计数） | 主信号（原值）、对照（归一化版） |
| **F6 通道总量** | `primary_sentiment_total_2` / `secondary_sentiment_total_2` | 区间内情绪值的**和** | **存量型 ∧ 规模代理** | 排除（只能作比值分子） |

**本集无 GROUP 类型字段**（23 字段全为 MATRIX/VECTOR）⇒ 「分组轴」角色不可由本集字段承担，必须外借平台内置 `sector` / `industry` / `subindustry` / `market`。⛔ 不要因为 `primary` / `secondary` 有「主/副」字样就把它当分组轴——description 明确只是两套通道。

---

## 4. 本仓历史实测（KOR 逐条，来源 `backtest_results` + 平台复核）

### 4.1 归属已由平台确认的 14 条探针（`backtest_results.dataset` 列为 NULL，本地入库缺口）

> 复核方式：`get_alpha_details(RRE988kj)` 与 `get_alpha_details(ZYQgpJqx)` 均返回 `region=KOR, universe=TOP600, delay=1`、`pyramids.effective=1`、`pyramids.list=[{name:'KOR/D1/SENTIMENT', multiplier:1.6}]`、`ra.pyramid_short='sentiment'` ⇒ **确属本集、确计入 sentiment 塔**，不是仅凭字段名推断。

| alpha_id | wave | 表达式（截断） | S | 2Y | F | TO | LC/SC | RA 失败项 |
|---|---|---|---:|---:|---:|---:|---|---|
| **`RRE988kj`** | mcp-20261106 | `group_rank(ts_mean(ts_std_dev(ts_backfill(sentiment_score_average,22),22),55),sector)` | **+0.72** | **+1.43** | 0.47 | **0.0786** | 322/313 | LOW_SHARPE / LOW_FITNESS / LOW_2Y（**CW、TO、subU 全 PASS**） |
| `e75NOjgz` | mcp-20261106 | `subtract(0.5, group_rank(ts_std_dev(ts_backfill(sentiment_score_average,22),22),sector))` | −0.84 | −1.45 | −0.43 | 0.1393 | 314/324 | LOW_* |
| `kqNv3Ak8` | mcp-20261106 | `subtract(0.5, group_rank(ts_delta(ts_backfill(sentiment_score_average,22),22),sector))` | −0.62 | −0.72 | −0.17 | 0.3562 | 319/319 | LOW_* |
| `6XdZ99YY` | mcp-20261106 | `multiply(group_rank(subtract(ts_backfill(primary_sentiment_average,22),ts_backfill(secondary_sentiment_average,22)),sector), …)` | −0.56 | −1.55 | −0.19 | 0.2866 | 272/363 | LOW_* |
| `omERKdAm` | mcp-20261106 | `subtract(0.5, group_rank(subtract(ts_backfill(primary_sentiment_average,22),ts_backfill(secondary_sentiment_average,22)),sector))` | −0.12 | **+1.70** | −0.02 | 0.2925 | 315/323 | LOW_* |
| `ZYQgpJqx` | mcp-20261106 | `subtract(0.5, group_rank(ts_zscore(ts_backfill(sentiment_score_average,22),66),sector))` | −0.32 | −0.15 | −0.07 | 0.2883 | 318/319 | LOW_*（CW PASS） |
| `N1NLrrg7` | mcp-20261106 | `group_rank(ts_backfill(news_article_count,22),sector)` | −0.31 | −0.41 | −0.08 | 0.2467 | 322/313 | LOW_* |
| `KPJvb1Yk` | mcp-20261106 | `subtract(0.5, group_rank(ts_delta(ts_backfill(news_article_count,22),5),sector))` | +0.25 | +1.01 | 0.04 | 0.5495 | 312/325 | LOW_* |
| `e75N002J` | mcp-20261106 | `multiply(group_rank(ts_std_dev(...),sector), group_rank(ts_backfill(news_article_count,22),sector))` | +0.10 | +0.01 | 0.02 | 0.2210 | 287/348 | LOW_* |
| `akKennWw` | mcp-20261106 | `group_rank(ts_backfill(primary_sentiment_average,22),sector)` | +0.09 | −0.95 | 0.01 | 0.2686 | 308/327 | LOW_* |
| `QPvOVV2X` | mcp-20261106 | `group_rank(divide(ts_backfill(total_sentiment_score,22),ts_backfill(news_article_count,22)),sector)` | +0.23 | +0.06 | 0.05 | 0.2697 | 307/328 | LOW_* |
| `wpQ3RrO2` | mcp-20261106 | `subtract(0.5, group_rank(divide(ts_backfill(total_sentiment_score,22),ts_backfill(news_article_count,22)),sector))` | −0.29 | −0.78 | −0.06 | 0.2840 | 326/311 | LOW_* |
| `KPJzAmqj` | mcp-20261107 | `group_rank(ts_av_diff(sentiment_score_average,250),sector)` | +0.04 | +0.53 | 0.00 | 0.4229 | **186/449** | LOW_* |
| `xArG71wp` | mcp-20261107 | `group_rank(ts_av_diff(sentiment_score_average,66),sector)` | +0.09 | +0.54 | 0.01 | 0.4259 | **187/448** | LOW_* |
| `omEEzRGE` | mcp-20261105 | `ts_target_tvr_decay(signed_power(group_rank(winsorize(rank(ts_backfill(primary_s…` | +0.26 | +0.13 | 0.06 | 0.1872 | 252/385 | LOW_* |

**读法**：`ts_av_diff` 两条（66/250 日）的 `long/short` = 186/449、187/448 ⇒ **严重偏空**，说明长窗「相对自身历史偏离」在 KOR 是方向性下注而非多空中性，需警惕；其余腿多空接近 1:1。

### 4.2 `dataset` 列已标注的 4 条（wave 203，`wave_results` id=1645 verdict=FAIL）

| alpha_id | 表达式（截断） | S | 2Y | F | TO | RA 失败项 |
|---|---|---:|---:|---:|---:|---|
| `npvkpGWw` | `hump(subtract(rank(ts_decay_linear(ts_delta(sentiment_score_average,5),10)),0.5),hump=0.003)` | +0.04 | +0.54 | 0.00 | 1.1527 | LOW_SHARPE / LOW_FITNESS / **HIGH_TURNOVER** / **CW** / LOW_2Y |
| `YP1wPrmA` | `hump(subtract(rank(ts_decay_linear(sentiment_score_average,22)),0.5),hump=0.003)` | +0.00 | −0.27 | 0.00 | 1.0935 | LOW_SHARPE / LOW_FITNESS / **HIGH_TURNOVER** / **CW** / LOW_2Y |
| `j2Yl2EXe` | `hump(subtract(0.5, rank(ts_decay_linear(sentiment_score_average,22))),hump=0.003)` | −0.45 | −0.26 | −0.07 | 1.0935 | … / **CW** / LOW_SUB_U / LOW_INVEST / LOW_2Y |
| `Jje0jadj` | `hump(subtract(0.5, rank(subtract(sentiment_score_maximum,sentiment_score_minimum))),hump=0.003)` | −0.57 | −0.59 | −0.10 | 1.0868 | … / **CW** / LOW_SUB_U / LOW_2Y |

**wave 203 归因**：4/4 **HIGH_TURNOVER（TO 1.09–1.15）** + 4/4 **CONCENTRATED_WEIGHT**，max|S| = 0.57。⚠ **结构性对照**：wave 203 四条**未加 `ts_backfill`**；而 §4.1 加了 `ts_backfill(…,22)` 的 14 条 **CW 全部 PASS**（`RRE988kj` 平台 checks 明确 `CONCENTRATED_WEIGHT` 在 pass 列表）⇒ **CW 的根因是覆盖/缺失造成的权重塌缩，`ts_backfill` 是解**（对齐 `docs/experience/07` §六「CW FAIL ⇒ 补覆盖，非调 decay/truncation」）。

### 4.3 十年覆盖（`get_alpha_yearly_stats(RRE988kj)` 实读，2014–2023）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | −0.14 | 1.02 | 1.83 | 0.48 | 0.69 | **−0.97** | **−0.27** | 1.29 | 1.51 | 1.36 |
| TO | .0778 | .0766 | .0798 | .0785 | .0862 | .0766 | .0789 | .0747 | .0784 | .0780 |
| LC/SC | 292/286 | 309/301 | 310/309 | 314/305 | 326/324 | 324/321 | 329/315 | 348/331 | 335/318 | 335/318 |

⇒ **十年逐年 `longCount>0 ∧ shortCount>0 ∧ pnl` 有正有负但无空年**（十年覆盖 PASS，非「数据不满十年」型死法）；**冷段集中在 2019–2020 两年**（−0.97 / −0.27），2021–2023 连续三年 S≥1.29 ⇒ 2Y=1.43 是**近年结构性存在**而非单年脉冲。⚠ 但 2Y 与 IS 的裂口（1.43 vs 0.72）说明**长样本被 2019–2020 稀释**，是「分段失效」而非「全程无效」。

---

## 5. 判死台账核对（族级 vs 数据集级，逐条取证）

| 项 | 实读内容 | 判定 |
|---|---|---|
| `get_dead_datasets(KOR)` | **16 条**（列表见文首），**无 news_sentiment_transfer** | ⇒ **非数据集级**，硬闸 `dead_dataset_guard` 不拦 |
| `registry_empirical` id=153 | `entry_id=KOR-NEWS-SENTIMENT-TRANSFER-DEAD`；`layer=dead_end`；`family='news_sentiment_transfer sentiment'`；**payload 无 `dataset` 键**；`reason='wave132 8/8 RED max abs sh 0.52; day-frequency aggregated sentiment scores carry no cross-sectional signal in KOR TOP600; tvr 111-122% structural wall'`；`rule='do not probe news/sentiment aggregate datasets in KOR again'`；`dead_at=2026-08-23` | payload 带 `family` 且无 `dataset` |
| 代码定级依据 | `src/wqb/dead_datasets.py:100-113` `_dataset_of()` 无 `dataset` 键 ⇒ None；`:135-143` `_family_of()` 非空或 ds 为空 ⇒ `level='family'` | ⇒ **level = family（机制族）**，与候选理由一致 |
| 路线图 | `tracking/KOR/reference/unlit_towers_roadmap_20261030.md:51`（news 塔「已死」栏点名本集为 `KOR-NEWS-SENTIMENT-TRANSFER-DEAD`）；`:96`（wave 208 开波前 kill、0 配额、4 式 dropped、并记 `dead_dataset_guard` 不查 `get_dead_ends` 机制族记录）；`:114`（列入「战役级判死数据集（`get_dead_ends` 点名）」） | 三处命中，逐字核对一致 |
| **门禁结论**（机械口径） | ① `get_pyramid_alphas` 实读 KOR/D1 sentiment=**0** < 3 ⇒ 未亮塔；② 不在 16 死集名单 ⇒ 数据集级未死；③ 但**命中毒性明确写死的机制族** `news_sentiment_transfer sentiment`，`rule` 原文点名「do not probe news/sentiment aggregate datasets in KOR again」 | **塔未亮 + 机制族判死 = 冲突**。按 `AGENTS.md` §7.5「判死标记不得单独作为依据」与 §7.6「判死是例外不是默认」，本档案**只如实上报，不判定可投**；开波前须由用户/战役负责人裁决是否 REVOKED（同 wave124→fhp 的处理路径） |

### 5.1 ⚠ 判死理由与实测的两处冲突（必须上报，不得静默）

| 死因原文 | 本轮实测 | 差异定性 |
|---|---|---|
| 「carry **no cross-sectional signal** in KOR TOP600」 | `RRE988kj` 真实截面 322/313、十年逐年 292–348、S=**+0.72** / 2Y=**+1.43** / CW PASS / TO 7.86% | **表述过强**。准确说法应是「达不到 S≥1.58 闸线」（KOR 全库最佳 \|S\|=0.72，距闸 54%），不是「无截面」 |
| 「tvr **111-122%** structural wall」 | wave 203 实测 TO = **1.0868–1.1527**（108.7%–115.3%）；但加 `ts_backfill` 的 14 条探针 TO = **0.0786–0.5495**，其中 `RRE988kj` 7.86% 落在获胜带 | **换手墙不是本集的结构墙，是「未补覆盖 + 裸水平」的形态墙**；补覆盖后 TO 可下降一个数量级 |
| 「wave132 8/8 RED max abs sh **0.52**」 | 本地 `backtest_results` **无 wave 132 行**（KOR 仅有 wave 203 + mcp-20261105/06/07），`wave_results` 亦无 wave132 记录 | **wave132 原始读数不可复现**（本地入库缺口）；本档案以**可复现的 wave 203 与 14 条探针**为准，不引用 0.52 |

---

## 6. 机制假设（5 条；格式＝机制名｜存量型/流量型｜经济叙事｜适用统计族｜证伪条件）

> 全部字段的存量/流量定性见 §3。**存量型走长窗需慎**（区间聚合本身已平滑）；**流量型（F5 计数）宜短窗 5/22**。

1. **M1 语调水平慢扩散（慢×快价差）｜存量型｜正向新闻语调被市场渐进吸收、负向被更快定价，故「情绪分相对自身历史的分位 减去 收益相对自身历史的 z-score」应抓未被吸收的那部分（IND 实测 `2rjXKVKZ` S=2.38 / 2Y=2.47 是全库唯一强几何）｜统计族：`rank(subtract(ts_zscore(ts_backfill(sentiment_score_average,22),20), ts_zscore(returns,20)))` 慢×快价差 + `group_rank` 分组轴｜证伪：若 KOR 上慢×快价差与裸水平族（wave 203 已在 S=0.00 / −0.45）**在 ≥2 个分组轴上 \|S\| 均 <0.5 且 2Y<1.0** ⇒ 语调水平轴在 KOR 无截面信息（现有 KOR 读数已临界）。
2. **M2 双通道背离（不确定性折价）｜存量型｜primary 与 secondary 是两条独立 NLP 通道，二者背离＝信息矛盾，市场高估确定性（Miller 1977 路径）｜统计族：**单一经济含义价差** `subtract(rank(ts_backfill(primary_sentiment_average,22)), rank(ts_backfill(secondary_sentiment_average,22)))`（⛔ 禁 `add` 等权拼腿）｜证伪：KOR 已有 `6XdZ99YY` S=−0.56/2Y=−1.55 与 `omERKdAm` S=−0.12/**2Y=+1.70** 两条方向相反的读数 ⇒ **若在 ≥2 分组轴上价差腿 \|S\|<0.5 或 2Y 符号不稳定**，判背离轴死；先做一次两通道相关性体检（相关≈1 则退化为噪声）。
3. **M3 舆情不确定性（情绪二阶矩）｜存量型（区间聚合的时序二阶统计）｜情绪分自身的时序波动＝舆情分歧/不确定性，比水平更适合当风险溢价代理；KOR 全库**唯一有生存读数**的轴（`RRE988kj` S=0.72 / 2Y=1.43 / TO 7.86% / CW PASS / 十年无空年）｜统计族：`group_rank(ts_mean(ts_std_dev(ts_backfill(sentiment_score_average,22),22),55), sector)` 双层平滑（短窗算波动、长窗平滑）｜证伪：若换分组轴（sector→industry→market）与平滑窗（22/55/66）后 **\|S\| 无一超过 0.72 且 2Y 全部 <1.4** ⇒ 二阶矩轴无增量；⚠ 若出现「IS 抬到 1.0+ 而 2Y 断崖 <1.0」⇒ 按决策表判**存量型结构墙**（对齐 `AGENTS.md` KOR 配置平移律：先换 1 档确认 S 天花板，2Y 仍 <1.0 即确认机制死，别再扫窗口）。
4. **M4 注意力冲击反转 + 新鲜度门｜流量型｜新闻条数激增＝散户注意力过载 ⇒ 短期高估后反转；`ts_arg_max` **只当门控条件**（论坛 LC97552 冠军用法），不当信号｜统计族：`ts_delta(ts_backfill(news_article_count,22),5)` 变化量 + `trade_when(ts_arg_max(news_article_count,G) < T, <M1/M3 持仓腿>, -1)` 门控｜证伪：KOR 已有 Δ5 S=+0.25/2Y=1.01、水平 S=−0.31、std×count S=+0.10 ⇒ **若 Δ 与门控腿在 ≥2 个分组轴上 \|S\| 均 <0.5** ⇒ 注意力轴在 KOR 无截面信息（与 wave132 判死原文方向一致）；⚠ 门控只修 prod/robust **不造强度**，强度不足时不应投。
5. **M5 单位语调强度（去规模代理归一）｜流量型归一（比值）｜把情绪总和除以报道条数＝每则新闻的平均语调；这是**唯一能把 `total_sentiment_score` / `*_total_2` 这类 sum 字段合法用起来**的写法，同时消掉媒体覆盖/市值代理｜统计族：`divide(ts_backfill(total_sentiment_score,22), ts_backfill(news_article_count,22))` 或直接用已单位化的 `sentiment_score_average` / `_median`｜证伪：KOR 已有比值腿 S=−0.29 / +0.23（两个方向都试过）⇒ **若比值化后 \|S\| 仍 <0.5**，判「归一不产生信息」，且**不得回退到裸 sum 水平**（那是规模代理，违 §7 铁律）。

---

## 7. 规模代理判定（任务特指：核心字段是否为慢变量横截面水平值）

**结论分三层，必须分开读**：

1. **不是会计存量型规模代理**：本集**没有**持股比例、治理评分、股本结构、市值余额类字段。F1–F4 是**区间聚合的情绪分与其分布统计**，量纲有界（情绪 0–1 或对称分），**不随市值单调增长**。
2. **但 F6 与 F5 的裸水平确实是规模代理**（诚实标注，这是本集真正的坑）：
   - `total_sentiment_score` = "Sum of all sentiment values…"、`primary_sentiment_total_2` / `secondary_sentiment_total_2` = "Sum of all … values" ⇒ **sum 随报道条数线性增长**；
   - `news_article_count` = "Total number of news articles" ⇒ **媒体覆盖量与市值/机构关注度强正相关**（KOR TOP600 内大票新闻多）。
   - ⇒ 任何以这三者**裸水平**入信号的腿，本质是市值/媒体覆盖代理 ⇒ **角色判为「排除」**，只允许作比值分子（M5）。
3. **可替代的合规写法（任务要求的变化量/时序分位/离散度）**，本集已各有一条 KOR 读数：

| 写法 | 具体表达式形态 | KOR 已有读数 |
|---|---|---|
| ① 变化量 | `ts_delta(ts_backfill(sentiment_score_average,22),5/22)` | `kqNv3Ak8` −0.62 / −0.72；`npvkpGWw` +0.04 |
| ② 相对自身历史偏离 | `ts_zscore(…,66)` / `ts_av_diff(…,66/250)` / `ts_rank(…,252)` | `ZYQgpJqx` −0.32；`xArG71wp` +0.09（偏空 187/448）；`KPJzAmqj` +0.04 |
| ③ 离散度/分歧 | `ts_std_dev(…,22)` 双层平滑 / 偏度字段 / `vec_stddev(news_sentiment_score)` | **`RRE988kj` +0.72 / 2Y 1.43 ★ 本集最佳** |
| ④ 比值归一 | `divide(total_sentiment_score, news_article_count)` | `QPvOVV2X` +0.23；`wpQ3RrO2` −0.29 |

**预注册声明**：本集任何后续波次**不得**出现裸 `total_sentiment_score` / `*_total_2` / `news_article_count` 水平作为主信号腿；出现即按规模代理违规处理（可在 wave gate 前人工拦截）。

---

## 8. 模板匹配（症状 → 查表 → 动作，依据 `docs/experience/07_field_profile_template_mapping.md` §六/§七）

| 本集症状 | 查表动作 | 依据 |
|---|---|---|
| 覆盖率 0.9654（元数据高），但 wave 203 **CW FAIL 4/4** | **先 `ts_backfill(F,22)` 补覆盖**（不调 decay/truncation/中性化）；本仓实证：补齐后 14 条探针 CW 全 PASS | 07 §六「CONCENTRATED_WEIGHT FAIL」 |
| VECTOR 3 个（`news_sentiment_score` / `primary_sentiment_value` / `secondary_sentiment_value`） | 必须先 `vec_avg` / `vec_stddev` 降标量 + `ts_backfill`；**元数据 cov 0.9654 不可信**，须先 Long Count（本档案未跑） | 07 §七；09 §14.2 |
| 换手 1.09–1.15（wave 203） | 换形态（二阶矩 + 长窗平滑 → TO 7.86% 实证）+ 补覆盖；**不是调 truncation** | 本档案 §4.1 vs §4.2 对照 |
| 2Y 与 IS 裂口（IS 0.72 / 2Y 1.43；冷段 2019–2020） | 按「IS_LADDER / 2Y」查表：`trade_when` 流动性门控或双层平滑；⚠ 不叠多个门 | 07 §六 |
| 信号弱（KOR 最佳 0.72，距闸 1.58 差 54%） | 换**分组轴**（sector→industry→subindustry 逐档）或换**算子几何**；⛔ 不扫窗口/常数 | 07 §六；KOR 配置平移律 |
| 想合成 primary + secondary / max + min | 只走**单一经济含义价差** `subtract(rank(A),rank(B))`；⛔ 禁 `add` 等权拼腿 | 02 §1 组合形态铁律 |
| 想用 `ts_arg_max` 造新鲜度 | **只作 `trade_when` 门控条件**（冠军），作信号=摧毁器 | 07 §六 LC97552 |
| 想用裸 sum / 裸 count 水平 | **禁止**（规模代理，§7）；改比值 `divide` 或时序分位 | 本档案 §7 |

**量纲坑**：`add(带单位字段, 裸常数)` 报 UNITS 错（preflight 查不出）；中心化用 `ts_av_diff` / `ts_ratio`，⛔ 别写 `add(x, ts_std_dev(x,252))`（触发 `POISON:equal_weight_leg_add`）。本集价差/比值一律用 `subtract` / `divide`，安全。

---

## 9. 推荐回测设置与理由

| 设置 | 值 | 理由 |
|---|---|---|
| region / universe / delay | **KOR / TOP600 / 1** | 本集 KOR 实读档；`get_alpha_details` 两条平台复核件均为此档 |
| neutralization | **STATISTICAL**（首发）；**REVERSION_AND_MOMENTUM** 作第 2 档 | `RRE988kj`（本集最佳腿）的平台 settings 实读是 `REVERSION_AND_MOMENTUM`，`ZYQgpJqx` 是 `STATISTICAL`；按 KOR 配置平移律，**只换这 1 档**确认 S 天花板，2Y 仍 <1.0 即判机制死，别扩扫 |
| decay | **4** | KOR 默认；两条平台复核件均为 decay=4，且二阶矩腿 TO 仅 7.86% 说明 decay 不是瓶颈 |
| truncation | **0.08** | KOR 默认；CW FAIL **不靠调 truncation 修**（走 `ts_backfill`） |
| pasteurization | **ON** | `get_alpha_details` 实读档 |
| nanHandling | **OFF** | `get_alpha_details` 实读档；但**必须靠显式 `ts_backfill` 补覆盖**，不靠平台 nan 填充 |
| maxTrade / maxPosition | **OFF / OFF** | 实读档 |
| **backfill** | **必要**：`ts_backfill(F, 22)`（必要时 66） | 唯一有对照证据的开关：wave 203 不补 ⇒ CW 4/4 FAIL、TO 1.09–1.15；14 条补覆盖探针 ⇒ CW 全 PASS、TO 0.079–0.550 |
| VECTOR 降维 | **必要**（仅 3 个 VECTOR）：`vec_avg` / `vec_stddev` | 平台不接受裸 VECTOR 入信号 |
| 窗口 | 短窗 **22** 为主，平滑 **55/66**；长窗 250 慎用 | 流量/情绪日频；`ts_av_diff(250)` 实测多空 187/448 严重偏空 |
| 波次规模 | **先 2–3 条探针**（二阶矩 × 分组轴；慢×快价差 ×1），再决定整波 | 本集命中**族级判死**（§5），且 KOR 最佳 |S|=0.72 距闸 54%；未获 REVOKED 前不得开大波 |

**一句话推荐档**：`KOR/TOP600/D1/STATISTICAL(第2档 REVERSION_AND_MOMENTUM)/decay4/trunc0.08/pasteurization ON/nanHandling OFF/maxTrade OFF + ts_backfill(22) + 二阶矩/慢×快价差几何`，**先探针后整波**。

---

## 10. 自查（无抽样、无凭名推断）

- ✅ **分母完整**：23/23 字段逐 id 列于 §1，无 `*_active` / 「同构孪生」/「代表字段」类通配；平台对账 `count=23 == platform_count=23 == complete=true`。
- ✅ **每字段有带数字读数**：§2 实测表 **23 行**，每行含 cov=0.9654、aC、全区 n 与 max\|S\|/2Y/alpha/区；KOR 无独立腿的字段已**诚实标注「无 KOR 独立腿」并用跨区数字 + 元数据数字**满足「带数字」，未编造 KOR S 值。
- ✅ **计数一致**：§1 分母 23 = §2 实测行 23。
- ✅ **语义全部来自平台 description 原文**（§1 逐字），未凭字段名推断；`primary`/`secondary` 的「主/副」已明确按 description 只当两条通道，不当质量梯度或分组轴。
- ✅ **塔位与判死均为本轮实读**：`get_pyramid_alphas`（KOR/D1 sentiment=0）、`get_dead_datasets(KOR)`（16 条不含本集）、`registry_empirical` id=153 逐字段。
- ✅ **判死定级有代码依据**（`src/wqb/dead_datasets.py:100-113, 135-143`），非印象。
- ✅ **归属不靠猜**：14 条 `dataset=NULL` 的 KOR 探针经 `get_alpha_details` 平台复核 `pyramids=[KOR/D1/SENTIMENT]` 后才计入本集。
- ⚠ **未做的事（如实标注，不臆造）**：
  - **法1 Long Count 未跑**（本任务零仿真约束）⇒ VECTOR 3 个字段与 12 个无 KOR 腿的字段，**有效覆盖标「未实测」**，只引用元数据 0.9654（仅供排序）。
  - **wave132 原始读数不可复现**（本地库无该波记录），已在 §5.1 列明并改用可复现证据。
  - 一批 KOR 探针（`mean_sentiment_score_transfer` / `skew_sentiment_score_transfer` / `primary_sentiment_score_transfer` 等，wave mcp-20261109，7 条）**未计入本集**：这些字段名**不在本集 23 字段内**（KOR/TOP600 与 USA/TOP3000 两区实读均无），也已排除 `news85`（其 23 字段名不同）与 `ai_factor_transfer`（20 个价量字段）；**归属数据集本轮未定位**，如实登记为「疑似他集，待查」，不挪用其读数（那些腿 S 最高 0.76 / TO 0.027，若误归本集会显著抬高本集观感）。
- 🚩 **既有档案两处漂移（本轮发现，建议维护者修正）**：`tracking/KOR/reference/datasets/news_sentiment_transfer.md`
  ① 文首写「23 字段（**18 MATRIX + 5 VECTOR**）」，本轮平台实读为 **20 MATRIX + 3 VECTOR**；其 §0.3「VECTOR 5 个必须先 `vec_avg`」应改为 3 个；
  ② 其 §3「待测表达式与实测记录」表仍只有 `| 203 | 待填 |` 一行，**wave 203 的 4 条实测与 14 条探针均未回写**（本档案 §4 已补齐读数）。
- **机械闸**（本轮已执行，非转述）：`python tools/gates/field_profile_completeness_gate.py --profile tracking/KOR/campaign_wf/wf_profile_news_sentiment_transfer.md`
  → 输出 `字段全表 id 数: 23` / `带实测读数的字段: 23` / `✅ PASS：全字段均有实测读数，且分母无通配占位`，**exit 0**。
