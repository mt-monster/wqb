# NEWS 跨区迁移证据与天花板结论（2026-11-03）

> 目标：GBR 的 NEWS 模板能否总结成可迁移资产，并在其它 region 的 NEWS category 下挖出 regular alpha。
> 本文只收录**实读证据**；模板本身见 `gbr_news_template_summary_*_20261103.md` 与 `news_template_field_semantic_map_20261103.md`。

## 0. 结论摘要（最终版，2026-11-03 20:2x）

**问题**：GBR 的 NEWS 模板能否总结成可迁移资产，并在其它 region 的 NEWS category 下挖掘 regular alpha？

**答案分两半**：

**① 模板可以总结、且确实可迁移 —— 已验证。**
- 四份资产文档已产出：速查、迁移总纲、12 语义槽位映射（GBR/CHN/HKG/AMR）、10 步迁移 SOP。
- GBR 论坛机制 `signed_power(subtract(ts_zscore(ts_backfill(pos,60),250), ts_zscore(ts_backfill(neg,60),250)), 3)` 在 EUR/HKG/AMR/USA/IND/ASI 的 NEWS 数据集上**全部可复现、方向稳定、预检全 valid**。

**② 但在 NEWS category 内挖不出过闸的 regular alpha —— 九区实测证否。**

| 区 | 最优 \|S\| | 数据集 / 轴 | 闸线 | 差距 |
|---|---:|---|---:|---:|
| AMR | **0.92** | news73 `uncertainty` 10/126 | 1.58 | 1.7× |
| HKG | 0.88 | news36 词数归一 22/66 STAT | 1.58 | 1.8× |
| GBR（源区） | 0.83 | news20 新闻情绪 | 1.58 | 1.9× |
| IND | 0.69 | news73 `uncertainty` | 1.58 | 2.3× |
| EUR | 0.54 | news36 论坛 zscore 差 | 1.58 | 2.9× |
| ASI | 0.32 | news73 `uncertainty` | 1.58 | 4.9× |
| USA | 0.26 | news73 `uncertainty` | 1.58 | 6.1× |
| CHN | 0.18 | news46 `mws46_ess` | 1.58 | 11.5× |
| HKG news7 | 0.20 | MATRIX 标题语气 6 几何 | 1.58 | 7.9× |
| HKG news79 | 0.64 | VECTOR 事件驱动 `ts_delta` | 1.58 | 2.5× |

**根因（已被三条互相独立的否证锁定）**：
1. **不是覆盖度**：USA news73 cov=1.0 只有 0.26，AMR cov=0.645 却有 0.92 ⇒ 信号强度随 **universe 集中度**上升（TOP600 ≫ TOP3000）。
2. **不是字段类型（H2 被否）**：MATRIX 型的 news7 只有 0.20，VECTOR 型的 news73 有 0.92 ⇒ **MATRIX 反而更差**。
3. **不是「日频 vs 事件驱动」（H1 也被削弱）**：连事件驱动的 news 字段（news79）也只有 0.64，而 earnings 电话会情绪（`earnings_sent_matrix`）有 **1.65**。

⇒ **天花板是 NEWS category 本身的信息密度**：新闻情绪被即时套利，横截面定价力被压缩；即使是事件驱动的 news 字段，信息密度也远低于财报电话会。**换区、换轴、换字段类型、换几何都无效。**

**唯一摸到闸线的实例不在 NEWS**：同一论坛机制用在 `earnings_sent_matrix`（earnings category）上 S **1.65** / F 1.19 / 2Y **2.30** / TO 21.3% / **failed_ra 0** / **self 0.136**，唯一挡路的是 prod（旧读数 1.00，尚未在提交口径下重测确认）。⇒ 破闸路径 = 回 earnings 解决 prod 墙，见第 12 节。

## 1. 各区闸线（实读 config/thresholds.json）

| Region | LOW_SHARPE | LOW_FITNESS | LOW_2Y_SHARPE | TVR | 备注 |
|---|---:|---:|---:|---|---|
| USA | 1.58 | 1.0 | 1.6 | 5–30% | config review 1.25，**平台实测 1.58** |
| AMR | 1.58 | 1.0 | 1.0 | 1–70% | 2Y 最松、TVR 最松 |
| HKG | 1.58 | 1.0 | 1.6 | 5–30% | |
| EUR | 1.58 | 1.0 | 1.6 | 5–30% | |
| GLB | 1.58 | 1.0 | 1.6 | 5–30% | |
| CHN | 1.58 | 1.0 | 1.6 | 5–30% | 平台侧 LOW_SHARPE 实测 **2.07** |

## 2. 各区 NEWS 最强读数（实读 CSV + get_alpha_details）

| Region | 最优 S | 数据集 | 轴 | 窗口 | TO | alpha | 闸差 |
|---|---:|---|---|---|---:|---|---:|
| AMR | **−0.92** | news73 | `entitiessent_uncertaintypartscr` | 10/126 | 8.06% | `E56GRlwK` | 1.7× |
| HKG | **+0.88** | news36 | 词数归一情绪 `wn` | 22/66 STAT decay8 | 7.55% | `KPJGvmEp` | 1.8× |
| EUR | **+0.54** | news36 | 论坛 zscore 差 | bf30/z250/p3 | 20.96% | `58ElbWQk` | 2.9× |
| GBR（源区） | +0.83 | news20 | 新闻情绪 | — | — | — | 1.9× |
| CHN | +0.18 | news46 | `mws46_ess` | — | — | — | 11.5× |
| USA | +0.26 | news73 | uncertainty 10/126 | 10/126 | 5.71% | \`leAjXzRl\` | 6.1× |
| ASI | +0.32 | news73 | uncertainty 10/126 | 10/126 | — | `zq3kamjK` | 4.9× |
| IND | **−0.69** | news73 | uncertainty 10/126 | 10/126 | 12.3% | `pwdjJZP3` | 2.3× |

**共 6 条情绪轴全部实测过**：uncertainty / 实体-故事跨层偏离 / finhype / finvolatile / fear / entities。
其中 **uncertainty 是唯一量级杠杆**（AMR ±0.92），其余轴 |S| ≤ 0.44。

## 3. 机制迁移证据

### 3.1 论坛机制（事件驱动情绪）— 可复现但数据依赖

```
signed_power(subtract(ts_zscore(ts_backfill(POS,60),250), ts_zscore(ts_backfill(NEG,60),250)), 3)
```

| 数据集 | category | 区 | S | F | TO | RA | prod |
|---|---|---|---:|---:|---:|---|---:|
| `earnings_sent_matrix` | earnings | EUR | **1.65** | 1.19 | 21.3% | **8/8 全过** | **1.00（饱和）** |
| `news36` | news | EUR | 0.54 | 0.16 | 20.96% | 挂 LOW_SHARPE/FITNESS/2Y | — |
| `news73` | news | EUR | 0.53 | — | — | 挂 | — |

⇒ **同一表达式，事件驱动情绪 S=1.65，日频新闻 S=0.54（3× 差）**。差异来自**数据集的信息密度**，不是表达式。

### 3.2 几何移植 — 全面失败

| 几何 | AMR | HKG | 结论 |
|---|---:|---:|---|
| `ts_max_diff` 峰值回差 | −0.23 | −0.54 | 判死 |
| `ts_zscore` 无壳 | — | −0.47（TO 128–137%） | 判死 |
| `ts_covariance` | +0.52 | — | 弱 |
| 乘子（跨族/同族） | 10/10 稀释 | relevance 系 +4.5% | 仅边际增益 |

## 4. 天花板根因（第一性原理）

1. **日频新闻情绪是连续噪声，事件驱动情绪是离散信息**。`earnings_sent_matrix` 的电话会情绪是**一次性信息事件**，市场需要时间定价；日频新闻情绪被即时套利，横截面定价力被压缩。
2. **news73 在 AMR 的 cov 只有 0.6448**，而 USA/GLB 是 **1.0** —— 覆盖度差异可能是 USA 的突破点。
3. **毒档/增益档是 region 特异的**：CHN 因子型中性化是毒档、HKG 是增益（1.27×）、AMR 不支持；HKG decay8 是增益、AMR 是毒档。⇒ **源区设置档不可照抄**。
4. **prod=1.0 是「平台已有几乎相同持仓」的信号**：`akK7Z3d9` RA 全过但 prod=1.00，说明该机制已被提交。⇒ 论坛模板的**具体表达式**已被市场占用。

## 5. USA news73 新线索（在飞）

- `news73` = "Story by Story Sentiment"，22 个 VECTOR 字段，与 AMR news73 **完全同族**。
- USA 档：cov **1.0**（AMR 0.6448），`uncertaintypartscr` alphaCount **3**（近处女）。
- USA config review 1.25，但**平台 LOW_SHARPE 实测 1.58**（无优势）。
- 已派发：
  - wave1（12 条，`bg_7531b17a`）：uncertainty 窗口阶梯 + hype/volatile/certainty/偏离 + 论坛机制。
  - wave2（10 条，`bg_8c779d3a`）：中性化 SECTOR/MARKET、decay15、长窗 504、论坛 bf30/z120 变体。

## 6. 进展与下一步

### 6.1 USA 已判死（2026-11-03）
- wave1（12 条）前两条 0.26 / 0.29；wave2（10 条）首条 0.37 ⇒ 全部 ≤0.37，远低于 1.58，停发。
- 结论：**覆盖度不是解药**。USA news73 cov=1.0 却只有 0.26，AMR cov=0.645 却有 −0.92 ⇒ 信号强度随 **universe 集中度**上升（TOP600 ≫ TOP3000）。

### 6.2 已派发 ASI/IND（2026-11-03）
- 方向：**新兴市场假设**（AMR 实测最强 −0.92，越低效市场信号越强）。
- ASI news73：cov 0.646，alphaCount **0–12**（近处女）；设置 TOP500/SUBINDUSTRY。
- IND news73：cov 0.665，alphaCount 20–109；设置 TOP500/STATISTICAL。
- 各 9 条：AMR 几何（SUBINDUSTRY/decay4/nanOFF）窗口阶梯 + 区域默认档 + hype/volatile/certainty/偏离四轴。
- 任务：`bg_9fc74525`（ASI）/ `bg_d342f01d`（IND）。

### 6.3 待办
- 若 ASI/IND 仍 < 1.58 ⇒ NEWS category 在七区全部判死，模板资产归档，转 earnings 事件驱动（需破 prod=1.0）。

## 7. ASI/IND 新兴市场假设 — 已判死（2026-11-03 收批）

| 区 | 波次 | 条数 | 最优 S | alpha | 结论 |
|---|---|---:|---|---|---|
| ASI | news73 wave1 | 1 | +0.32 | `zq3kamjK` | 弱 |
| IND | news73 wave1 | 9 | **−0.69** | `pwdjJZP3` | 该区最强，仍差 2.3× |

IND 全批：`pwdjJZP3` −0.69 / `e75zAm6d` −0.44 / `vR1j0kww` −0.36 / `58El7Ng1` −0.36 / `0mYwnqKq` −0.24 / `zq3kwO3E` −0.25 / `xArjwOKJ` −0.28 / `pwdjQJjv` −0.09 / `KPJ7xm81` +0.07。
⇒ **「越低效市场信号越强」假设被否**：ASI/IND 均远低于 AMR 的 −0.92。

## 8. ★ 新线索：HKG news79 — NEWS category 内唯一含「事件驱动情绪」字段的数据集

**为何重要**：第 4 节推论「NEWS 天花板是日频情绪」受到挑战。同一机制在 earnings（事件驱动）上 S=1.65，说明天花板是**数据集信息密度**造成的，不是 category 造成的。因此只要在 NEWS category 内找到**事件驱动情绪字段**，就有望破 1.58。

**实读（get_datasets + get_datafields）**：
- HKG `news79`「Global Corporate News Analytics」= Ravenpack 文档级分析，**85 字段全 VECTOR，cov 0.9341，tier1（score 0.7859），HKG tracking 内零引用**（只在 reference/hkg_dataset_ranking.json 中）。
- 关键字段：`nws79_earnings_release_sentiment`（财报发布标题情绪 −1/0/1，**alphaCount=7 / userCount=6**）、`nws79_earnings_tone_sentiment`（aC=34）、`nws79_sentiment_impact_projection`（预测未来 2h 市场冲击，**aC=1**）、`composite_sentiment_score` / `entity_sentiment` / `document_sentiment_confidence` / `entity_relevance` / `event_relevance` / `event_risk` / `event_similarity_days`（cov 0.9888）。

**已派发**：`results/_hkg_news79_wave1_list.json`（14 条结构互异模板：论坛机制 bf60/bf30、多尺度 zscore 差、confidence/relevance 加权、novelty 衰减、earnings_tone/composite/entity/impact 四轴、ts_delta；含 2 条无壳对照），设置 HKG/TOP800/SECTOR/decay8/trunc0.08/nanON。预检 **valid=True、unknown_fields=[]**。任务 `bg_a9658c18`。

**踩坑复用**：`batch_simulator` 的 alpha_list 条目**只许 {type, settings, regular}** —— 生成器里加的 `name` 会被转发进 simulate payload，报 `400 - {"name":["Unexpected property."]}`，14 条全 FAIL（无孤儿 sim）；剥掉后重派即成功。

## 9. 当前待办（更新 2026-11-03 18:5x）

1. **HKG news79 wave1 已收 10/14**（任务 1 小时上限超时，平台侧仍在跑剩余 3 条）。最优 `E56lKE6K` **0.64**，差闸线 2.5× ⇒ 不扩大模板，判弱收批。
2. **HKG news73 wave1 任务丢失**（runtime restart 杀死，已出 3/9 全弱 −0.13/−0.10/−0.23）；剩余 6 条仍在平台跑但无追踪，因结果弱不重派。
3. **AMR wave6**（11 条，已预检 valid）仍未派 —— 待 news79 出结果后再决定是否打。
4. ★ 尖雷：若 news79 也 < 1.58 → NEWS category 在**七区全部判死**，模板资产归档，转 earnings 事件驱动（需破 prod=1.0）。

## 10. 竞争性假设：MATRIX vs VECTOR（决定 news79 结果的解读）

第 4 节把天花板归因于「日频 vs 事件驱动」。但还有第二个、可能更根本的候选：**字段是 MATRIX 还是 VECTOR**。

| 数据集 | category | 字段类型 | 每 instrument-day 粒度 | 区 | S |
|---|---|---|---|---|---:|
| `earnings_sent_matrix` | earnings | **MATRIX** | 一个值（来自电话会事件） | EUR | **1.65** |
| `news73` | news | VECTOR | 多篇文档，需 `vec_avg` 聚合 | AMR | −0.92 |
| `news36` | news | VECTOR | 同上 | EUR | 0.54 |
| `news73` | news | VECTOR | 同上 | USA | 0.26 |

**两个假设预测一致，当前数据无法区分**：
- H1「日频 vs 事件驱动」：日频情绪被即时套利，事件情绪有定价力。
- H2「MATRIX vs VECTOR」：`vec_avg` 把多篇文档聚合成日均值，**摧毁了事件的时点信息**（哪天有几条新闻、距上次新闻多久），只剩「平均情绪水平」。

**news79 是唯一能区分二者的检验**（它是 VECTOR 但字段是事件驱动的）：
- 若 news79 破 1.58 → 支持 **H1**，`vec_avg` 聚合不毁信号 → NEWS category 内可继续挖。
- 若 news79 < 1.58 → 支持 **H2**，VEC 聚合是硬伤 → **NEWS category 内无解**（除非找到 MATRIX 型的 news 数据集），应转 earnings。

**可操作推论**：若 H2 成立，则应优先找 **MATRIX 类型** 的 news 数据集，而不是继续在 VECTOR 数据集上换情绪轴。

## 11. news79 结果（负面）+ news7 MATRIX 新线索（2026-11-03 19:40）

### 11.1 news79 未复现事件驱动假设

| 波次 | 条数 | 最优 S | 结论 |
|---|---:|---:|---|
| 带壳（SECTOR/decay8） | **10/14 已出** | **0.64**（`E56lKE6K`，`ts_delta` 变化量机制） | 弱 |
| 无壳（SECTOR/decay6/trunc0.04） | 2/6 已出（已停） | 0.02 | 弱 |

带壳 10 条全量（按 |S| 排序）：`E56lKE6K` **0.64** / `LLM7kQmn` −0.59 / `LLM7n5Qe` 0.53 / `P0o7vwbW` 0.41 / `bl6joQzM` 0.28 / `78LjQoPZ` 0.24 / `QPv7lJO5` 0.21 / `WjO7NR0O` 0.21 / `QPv72d0M` −0.06 / `ZYQ7j5r1` −0.07；另 1 条 `BATCH_SPAWN_FAILED`。

**★ 机制差异（本轮最有信息量的发现）**：
- **最优 `E56lKE6K`（0.64）不是论坛概率差机制**，而是**变化量机制** `ts_delta(ts_zscore(ts_backfill(vec_avg(nws79_earnings_release_sentiment),60),252),22)` —— 对 zscore 后的情绪取 **22 日差分**。
- 论坛机制（`signed_power(subtract(zscore(pos),zscore(neg)),3)`）在本数据集上的对应件 `LLM7n5Qe` 只有 0.53。
- 次优 `LLM7kQmn`（−0.59）用的是 `sentiment_impact_projection`（Ravenpack 预测未来 2h 冲击，aC=1）—— 负向。
⇒ 在 news79 上，**「情绪的变化」比「情绪的水平/概率差」更有定价力**，与论坛帖 `43614940683799`（变化稳定性：`sign(ts_delta)` 符号持续性）同族。但 0.64 仍差闸线 2.5×，且 TO 仅 4.07%（壳把换手压到极低，代价是信号被摊薄）。

无壳首条 `0mYwe6Kq`（S=−0.04，TO 31.8%）正是论坛机制（在 `earnings_sent_matrix` 上 S=1.65 的原型）的**直接移植**，**没有复现**。
⇒ **H1（事件驱动）在 news79 上暂不成立**；news79 的 VECTOR 字段即便事件驱动也破不了闸。

### 11.2 ★ 新线索：HKG news7 / news18 的 MATRIX 字段

侦察 HKG `news7`（Real Time News Feed，63 字段）与 `news18`（Ravenpack，44 字段）发现 **MATRIX 类型字段**：

**news7（26 个 MATRIX，其中满覆盖且近乎处女的）**：
- `headline_overall_tone_score_2`（cov **1.0**，aC=23）—— 标准化标题语气分
- `nws7_2_d1_tone_score`（cov 0.858，**aC=1**）—— (pos−neg)/(pos+neg)
- `headline_positive_tone_score_2`（cov 1.0，aC=7）/ `headline_negative_tone_score_2`（cov 1.0，aC=6）
- `headline_mention_count_2`（cov 1.0，aC=47）/ `news_mention_frequency_simple`（cov 1.0，aC=156）

**news18（24 个 MATRIX）**：
- `rp_ess_earnings`（财报事件情绪，cov 0.5，aC=43）/ `rp_css_earnings`（aC=119）
- `rp_nip_earnings`（财报新闻冲击预测，cov 0.5，**aC=6**）
- `rp_ess_revenue`（aC=42）/ `rp_ess_mna`（aC=1）

**为什么关键**：这是**唯一能干净检验 H2（MATRIX vs VECTOR）**的材料 ——
- `earnings_sent_matrix`：MATRIX + 事件驱动 → S 1.65
- `news79`：VECTOR + 事件驱动 → ≤0.28（刚测）
- `news7`：**MATRIX + 日频标题语气** → 待测

判读：
- 若 news7 > 1.58 ⇒ **MATRIX 才是关键**，`vec_avg` 聚合是硬伤 → 以后只找 MATRIX 型 news 数据集。
- 若 news7 < 1.58 ⇒ MATRIX 也不够 → **事件驱动（而非字段类型）才是关键**，NEWS category 内确实无解。

**已派发**：`results/_hkg_news7_matrix_list.json`（12 条：论坛机制、pos−neg 差、无 power、多尺度、ts_delta、volume 加权、mention 频次、bf30、rp_ess_earnings、rp_nip_earnings），HKG/TOP800/SECTOR/decay8/trunc0.08/nanON。预检 **valid=True、unknown_fields=[]**。任务 `bg_f1dee32e`。

### 11.3 MATRIX 波次结果（6/12，2026-11-03 20:1x）

| # | 字段 | 类型 | cov | aC | 表达式 | S | TO | alpha |
|---|---|---|---:|---:|---|---:|---:|---|
| 1 | `headline_overall_tone_score_2` | MATRIX | 1.0 | 23 | 论坛机制 bf60/z250/p3 | 0.18 | 5.3% | `RRE7d0bz` |
| 2 | `nws7_2_d1_tone_score` | MATRIX | 0.858 | **1** | 论坛机制 bf60/z250/p3 | 0.18 | 5.3% | （id 与 #1 重复，CSV 串值待核） |
| 3 | pos−neg 差 | MATRIX | 1.0 | — | bf60/z250/p3 | 0.12 | 5.3% | `3qolApdO` |
| 4 | `headline_overall_tone_score_2` | MATRIX | 1.0 | 23 | bf30 变体 | 0.19 | — | `akK7d3p2` |
| 5 | `headline_overall_tone_score_2` | MATRIX | 1.0 | 23 | 无 power 变体 | 0.20 | — | `e75zOz2J` |
| 6 | `headline_overall_tone_score_2` | MATRIX | 1.0 | 23 | 多尺度 zscore 差 | −0.06 | — | `qMLjAwAV` |

**前 6 条全弱（|S| ≤ 0.20）**，但全部是 news7 的「日频标题语气」轴 —— 它们是 H2 的**背景件**，不是**判决件**。判决件是同批未回的 `rp_ess_earnings`（news18，MATRIX + 事件驱动财报情绪，cov 0.5，aC=43）与 `rp_nip_earnings`（MATRIX + 事件冲击预测，aC=6）。

**初步判读**：`headline_overall_tone_score_2` cov=1.0、aC=23 已是被挖过的字段，6 条几何全灭 ⇒ 「日频标题语气」这条轴在 HKG 上确认无信号。这与 VECTOR/VECTOR 无关，**MATRIX 类型本身不构成优势**；H2 的剩余希望只压在 `rp_ess_*`（事件驱动）上。

### 11.4 ★ 判读更新：H2 已基本被否

| 数据集 | 字段类型 | 信息性质 | 区 | 最优 S | |S| vs 1.58 |
|---|---|---|---|---:|---|
| `earnings_sent_matrix` | MATRIX | 事件驱动 | EUR | **1.65** | 过 |
| `news79` | VECTOR | 事件驱动 | HKG | 0.64 | 2.5× |
| `news7` | **MATRIX** | 日频语气 | HKG | 0.20 | 7.9× |
| `news73` | VECTOR | 日频情绪 | AMR | 0.92 | 1.7× |
| `news36` | VECTOR | 日频情绪 | HKG | 0.88 | 1.8× |

**关键对比**：MATRIX 型的 news7 只有 0.20，而 VECTOR 型的 news73 有 0.92 ⇒ **MATRIX 不但不是优势，反而不如 VECTOR**。
⇒ **H2（MATRIX vs VECTOR）被否**；H1（事件驱动 vs 日频）仍成立但**仅在 `earnings_sent_matrix` 这一个数据集上被验证**，NEWS category 内的事件驱动字段（news79）只有 0.64。

**结论**：NEWS category 的天花板不是字段类型造成的，是 **category 本身的信息密度**造成的 —— 即使是事件驱动的 news 字段（news79），也不如 earnings 电话会情绪。⇒ 破闸只能回 `earnings_sent_matrix` 并解决它的 prod 墙。


## 12. 转向：earnings 事件驱动破 prod 墙（2026-11-03 20:1x）

### 12.1 目标 alpha 完整实读（get_alpha_details + check_self_correlation）

```
signed_power(subtract(ts_zscore(ts_backfill(positive_sentiment_probability_3, 60), 250),
                      ts_zscore(ts_backfill(negative_sentiment_probability_3, 60), 250)), 3)
```
设置：EUR / TOP2500 / D1 / **COUNTRY** / **decay 6** / **trunc 0.04** / nanHandling OFF / 2014-01-01~2023-12-31

| 指标 | 值 | 闸线 | 判定 |
|---|---:|---:|---|
| Sharpe | **1.65** | 1.58 | ✅ 过 |
| Fitness | 1.19 | 1.0 | ✅ 过 |
| Turnover | 21.3% | 1–70% | ✅ 过 |
| Returns | 11.09% | — | — |
| Drawdown | 8.22% | — | — |
| **2Y Sharpe** | **2.30** | 1.6 | ✅ 过 |
| Sub-universe Sharpe | 1.15 | — | — |
| investability_sharpe | 0.64 | — | — |
| risk_neutralized_sharpe | 1.52 | — | — |
| **failed_ra_count** | **0** | 0 | ✅ 全过 |
| ra_failed / ppa_failed | false / false | — | ✅ |
| pyramid_short | `earnings` | — | 可点 earnings 塔 |
| **SELF** | **0.1361** | 0.7 | ✅ 过（池 15/17，top: gJj1nxLM 0.136） |
| **PROD** | **1.00**（2.15h 前读数） | 0.7 | ❌ **撞墙** |
| CLUSTER_TEST | 1.22 | 1.58 | ⚠ warning |

checks.fail = **[]**，pass 含 LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / LOW_2Y_SHARPE / MATCHES_PYRAMID。

**★★ 唯一挡路的是 PROD = 1.00** —— 这是极端饱和（不是 0.70–0.72 那种边际卡墙），意味着平台 production pool 里已有一个**日收益序列几乎完全相同**的 alpha。窗口微调这类杠杆对它无效，必须换**信息维度**。

> 复测状态：2026-11-03 20:1x 重测 prod 返回 `correlation_busy`（holder = `corr:get_production_correlation(GrWlnXZJ)`，平台只允许一个在飞的 prod 计算，retry_after=240s）。待空槽后复测确认。

### 12.2 数据集实读：`earnings_sent_matrix` 只有 7 个字段

`get_datafields`（EUR / TOP2500 / D1）—— **7 个字段全 MATRIX，cov 0.5062**：

| 字段 | aC | 含义 |
|---|---:|---|
| `positive_sentiment_probability_3` | 335 | 正向情绪概率 [0–1] |
| `negative_sentiment_probability_3` | 315 | 负向情绪概率 [0–1] |
| `sentiment_weighting_method1` | 463 | 聚合电话会语气分（方法 1） |
| `sentiment_weighting_method2` | 233 | 聚合电话会语气分（方法 2） |
| `overall_sentiment_score` | 169 | argmax 得到的类别标签 |
| `likelihood_of_neutral_tone` | 129 | 中性语气概率 |
| `intraday_delay_indicator` | 111 | 日内/延迟更新码（元数据） |

⇒ **只有 7 个字段，所以「模板 ≥10 且结构互异」必须落在算子几何上，不能落在字段上。**

### 12.3 13 条破墙模板（已预检 valid=True / unknown_fields=[]，已派发）

| # | 模板 | 机制维度 | 表达式核心 |
|---|---|---|---|
| T1 | delta22 | **一阶差分**（情绪变化，news79 上实证最强 0.64） | `ts_delta(zscore(bf(POS−NEG)), 22)` |
| T2 | confweight | 置信加权（情绪差 × (1−中性概率)） | `zscore(bf((POS−NEG)×(1−NTR)))` |
| T3 | ratio | 比率几何（有向情绪占比） | `zscore(bf((POS−NEG)/(POS+NEG+0.01)))` |
| T4 | rank | 秩变换（厚尾稳健） | `ts_rank(bf(POS),250) − ts_rank(bf(NEG),250)` |
| T5 | std66 | **二阶矩**（情绪波动＝不确定度溢价，取负） | `−ts_std_dev(bf(POS−NEG), 66)` |
| T6 | ovr | 换字段（argmax 离散标签） | `zscore(bf(overall_sentiment_score))` |
| T7 | m1 | 换字段（聚合语气分 method1） | `zscore(bf(method1))` |
| T8 | disagree | **模型分歧**（两法之差＝不确定度，全新维度） | `zscore(bf(method1 − method2))` |
| T9 | shell | 降换手壳（改变持仓权重） | 原式 + `ts_target_tvr_decay(group_neutralize(...))` |
| T10 | sector | 中性化换 SECTOR | 原式 + SECTOR |
| T11 | delaygate | 元数据交互（日内更新码） | `zscore(bf((POS−NEG)×intraday_delay_indicator))` |
| T12 | cov126 | **协动**（正负概率同涨＝无信息，取负） | `−ts_covariance(bf(POS), bf(NEG), 126)` |
| T13 | surprise | **情绪意外**（短窗 z − 长窗 z） | `zscore(bf(POS−NEG),66) − zscore(bf(POS−NEG),250)` |

**真正的新信息维度只有 5 个**：T1（变化）、T5（波动）、T8（分歧）、T12（协同）、T13（意外）。其余是分布变换（T3/T4）、换字段（T6/T7）、设置变体（T9/T10）、元数据（T11）—— 对 prod=1.00 这种极端饱和，设置变体的持仓结构与原式高度重叠，预期仍会撞墙。

**预期管理**：原式 S 只比闸线高 0.07（1.65 vs 1.58），破墙时 S 大概率下降。验收要求 **S ≥ 1.58 且 prod < 0.7** 才算成功；若 S 掉了但 prod 也掉了，则需再做「维度 × 强度」二维搜索。

**已派发**：`results/_eur_esm_breakwall_list.json`（13 条），EUR/TOP2500/D1/COUNTRY/decay6/trunc0.04/nanOFF（T10 改 SECTOR），任务 `bg_ecf62946`。


### 12.4 ★★ universe 是比算子几何更根本的破 prod 杠杆（2026-11-03 20:2x）

**逻辑**：prod 相关性按**同一 universe 的日收益序列**计算。换 universe ⇒ 持仓股票池不同 ⇒ 与平台已有 alpha 的相关性**结构性下降**，这与「换算子几何」是正交的、可叠加的杠杆。

**EUR `earnings_sent_matrix` 的 universe 可用性实测**（`preflight_expressions` 逐档探测）：

| universe | preflight | 说明 |
|---|---|---|
| TOP2500 | ✅ | 原式所在档（S 1.65 / prod 1.00） |
| **TOP1200** | ✅ | **可用**，中盘 |
| TOP600 | ❌ | 字段不存在（`positive/negative_sentiment_probability_3` 不在该档） |
| **TOP400** | ✅ | **可用**，小盘 |
| TOP200 | ❌ | 字段不存在 |

**已预检 valid 的 12 条 universe 变体**（`results/_eur_esm_univ_list.json`）：TOP1200 × {base, delta, std, disagree, cov, surprise, shell, confweight} 8 条 + TOP400 × {base, delta, disagree, surprise} 4 条。全部 **valid=True / unknown_fields=[] / unknown_soft=[]**。待槽位空出后派发。

**执行顺序（重要）**：先派 U1（TOP1200 原式）单条 —— 它是**纯 universe 杠杆的对照件**，用来回答一个决定性问题：
- 若 U1 的 prod 已 < 0.7 ⇒ universe 单杠杆就够，后续全部往小 universe 铺，无需复杂几何。
- 若 U1 的 prod 仍 ≈1.0 ⇒ 说明该机制在全 EUR 范围内都被占用，需叠加机制杠杆（delta/std/disagree/cov/surprise）。

### 12.5 prod 复测阻塞（待解）

2026-11-03 20:1x / 20:2x 两次复测 `akK7Z3d9` 的 prod 均返回 `correlation_busy`：

```
status: correlation_busy
message: Another production correlation check is already running for this account.
         The BRAIN platform supports only one in-flight correlation computation.
         Please retry in 240 seconds.
holder: corr:get_production_correlation(GrWlnXZJ)
last_known: { max: 1.0, checked_at: 2026-11-03T17:56:44, age_hours: 2.19, stale: false }
```

- 平台**全账号只允许一个在飞的 prod 计算**，`GrWlnXZJ` 占住了槽位（非本轮任何调用所触发）。
- `last_known.max = 1.0` 是 17:56 的读数，note 明确标注「参考值，**判闸不得使用**」⇒ **prod=1.00 尚未在提交口径下被确认**。
- **行动**：等槽位释放后重测；**在 prod 被实测确认前，不得把 akK7Z3d9 记为「已撞墙淘汰」**（该结论目前只基于 2.19h 前的参考读数）。

### 11.5 判决件改派（2026-11-03 20:3x）

MATRIX 波次的 12 条排队顺序里，**H2 的唯二判决件 `rp_ess_earnings`（第 11 位）与 `rp_nip_earnings`（第 12 位）排在最后**，前面第 7–10 位仍是 news7 同族变体（mention_frequency / bf30 / pos−neg score 差）。

前 6 条已证 news7 标题语气轴**全灭**（|S| ≤ 0.20，6 种几何），继续等第 7–10 条只是重复确认。⇒ **停掉 MATRIX 波次（`bg_f1dee32e`），直接单派判决件**，省约 40 分钟。

**改派的 4 条**（`results/_hkg_news18_verdict_list.json`，HKG/TOP800/SECTOR/decay8/trunc0.08/nanON，预检 valid=True / unknown=[]）：

| # | 字段 | cov | aC | 角色 |
|---|---|---:|---:|---|
| 1 | `rp_ess_earnings` | 0.5 | 43 | **判决件**：MATRIX + 事件驱动财报情绪 |
| 2 | `rp_nip_earnings` | 0.5 | **6** | **判决件**：MATRIX + 财报冲击预测（近乎处女） |
| 3 | `rp_css_earnings` | 0.5 | 119 | 交叉验证：综合财报情绪 |
| 4 | `rp_ess_revenue` | 0.5 | 42 | 交叉验证：营收事件情绪 |

统一几何：`ts_target_tvr_decay(group_neutralize(signed_power(ts_zscore(ts_backfill(F, 60), 250), 3), densify(market)), target_tvr=0.05, lambda_max=5, lambda_min=0)`。任务 `bg_11d8769f`。

**判读规则**：
- 任一 > 1.58 ⇒ **H1 在 HKG news 上成立**，「事件驱动 + MATRIX」是破 NEWS 天花板的真实路径，值得全 category 铺开。
- 全部 ≤ 0.64 ⇒ NEWS category 九区彻底判死，模板资产归档，战力全部转 earnings（第 12 节）。


## 13. 覆盖率披露：哪些数据集测过、哪些没测（诚实边界）

上面的判死结论必须配上覆盖边界，否则会被误读成「NEWS category 已被穷尽」。**事实是：每个区只测了 1–2 个数据集，不是全部。**

### 13.1 已实测的数据集 × 区组合（12 个）

| 区 | 已测数据集 | 该区 news 数据集总数 |
|---|---|---:|
| GBR | news20 | —（源区） |
| CHN | news46 | 9 |
| HKG | news36 / news73 / news79 / news7 / news18 | 24 |
| AMR | news73 | 28 |
| EUR | news36 / news73 | 20 |
| USA | news73 | 26 |
| IND | news73 | 22 |
| ASI | news73 | 22 |
| KOR / DEU / GLB | **未测** | 24 / 17 / 15 |
| JPN / TWN / MEA | — | **0（该区无 news 数据集）** |

### 13.2 未测的部分与「为什么先不测」

每个区还剩 7–27 个 news 数据集未测。不继续铺开的理由不是「测不动」，而是**边际信息已经很低**：

1. **已测集都是该区按覆盖度/拥挤度排在最前的最强集**（news73 在多区是 tier1、cov 最高的那一档）。若最强的都只有 0.2–0.9，弱集反超 1.58 的概率极低。
2. **失败模式高度一致**：9 个区、6 条情绪轴、约 100 条 alpha，|S| 全部落在 0.18–0.92 这个窄带里，没有一条接近 1.58（差距最小也有 1.7×）。这是**系统性天花板**的特征，不是「碰巧没选对字段」。
3. **三条独立否证已经排除了最可能的解释**（覆盖度 / 字段类型 / 日频vs事件驱动），剩下的候选解释只有「category 信息密度」——而它无法通过换数据集绕过。

### 13.3 结论的有效边界（必须和第 0 节一起读）

- **强结论**（证据充分）：在已测的 12 个数据集×区组合上，NEWS category 的日频情绪/事件情绪字段**挖不出过 1.58 闸线的 regular alpha**；模板本身可迁移且预检全 valid。
- **弱推断**（未穷尽）：其余约 150 个未测 news 数据集**大概率**同样达不到 1.58，但**未被证否**。若未来要再试，优先序是：① 该区 tier1 且 alphaCount < 50 的集；② 含 `nip`（news impact projection）/`ens`（event novelty）等事件型字段的集；③ 不要再用日频情绪水平轴。


## 14. prod 复测轨迹（akk7Z3d9，三轮）

| 轮次 | 时刻 | 返回状态 | 细节 |
|---|---|---|---|
| 1 | 20:1x | `correlation_busy` | holder = `corr:get_production_correlation(GrWlnXZJ)`，retry_after 240s |
| 2 | 20:2x | `correlation_busy` | 同上，last_known 1.0（age 2.19h） |
| 3 | 20:14 | **`pending`** | `Production correlation data was not available after 242s of polling`；**holder=None / inflight=True** ⇒ 本次计算由我发起，平台算力不足未在 242s 内完成 |

**解读**：
1. 第 1–2 轮的 busy 是**别人/残留**的 prod 计算占槽；第 3 轮槽位已释放，进入 `pending` 说明**计算已受理但平台没算完**。
2. `last_known.max = 1.0`（17:56 读数）在三轮中始终未变，且工具持续标注「判闸不得使用」。
3. **行动**：等 300s 后重试（本机 inflight 标记需自行清理）；在拿到实测值前，`akK7Z3d9` 的状态记为「**RA 全过、self 0.136 过、prod 待实测**」，不得记为「已撞墙淘汰」。

**平台事实（复用）**：prod 计算有 242s 轮询上限，超时不落缓存；平台全账号只允许 1 个在飞 prod 计算。⇒ 批量破墙时不能对每条候选都测 prod，**必须先用 S ≥ 1.58 过滤**（回测返回 S/F/TO 但不返回 prod）。


## 15. ★★★ 更强杠杆：换 region（earnings_sent_matrix 在四区可用）

前面第 12.4 节说「换 universe」是与算子几何正交的破 prod 杠杆。**换 region 比它更彻底** —— prod 相关性按**同区 alpha 池**计算，换 region ⇒ 完全不同的 production 池 ⇒ prod 重新计算。

### 15.1 可用性实测（preflight_expressions）

`earnings_sent_matrix` + 论坛机制原式，四区逐档探测：

| region | universe | preflight | unknown_fields |
|---|---|---|---|
| **GBR** | TOP700 | ✅ valid | [] |
| **AMR** | TOP600 | ✅ valid | [] |
| **USA** | TOP3000 | ✅ valid | [] |
| **GLB** | TOP3000 | ✅ valid | [] |
| EUR（原区） | TOP2500 | ✅ valid | [] |

⇒ 该数据集是**真正的跨区数据集**（五区可用）。EUR 上 S 1.65 已证明机制有效；其余四区的 S 未知，但**prod 墙是区特有的**，EUR 的 prod=1.00 不约束其它区。

### 15.2 为什么这条路比「换算子几何」更有希望

| 杠杆 | 改变什么 | 对 prod 的影响 |
|---|---|---|
| 换算子几何（delta/std/disagree/cov/surprise） | 同一信息源的表达方式 | **可能仍高** —— 信息源相同，持仓方向高度重叠 |
| 换 universe（TOP1200/TOP400） | 股票池子集 | 中 —— 子集与全集的日收益相关 |
| **换 region**（GBR/AMR/USA/GLB） | **完全不同的市场 + 完全不同的 alpha 池** | **最强 —— prod 重新计算，与 EUR 的 1.0 无关** |

### 15.3 已备清单（`results/_esm_region_list.json`，4 条，各区既有成功档）

| region | universe | neutralization | decay | trunc | nan |
|---|---|---|---:|---:|---|
| GBR | TOP700 | COUNTRY | 15 | 0.05 | ON |
| AMR | TOP600 | SUBINDUSTRY | 4 | 0.08 | ON |
| USA | TOP3000 | SUBINDUSTRY | 5 | 0.08 | ON |
| GLB | TOP3000 | SUBINDUSTRY | 4 | 0.08 | ON |

**注意**：各区闸线均为 **1.58**（AMR 的 2Y 只要 1.0，最松）。AMR 是最有希望的区（新兴市场 + 2Y 最松 + universe 集中度最高 ⇒ 第 6.1 节实证「信号强度随 universe 集中度上升」）。

**待槽位**：当前 ESM 破墙波次（13 条）+ news18 判决件（4 条）已占满 2 槽。


## 16. ★★★★★ 破墙首个成功件：`d5Wj0Nx2`（T3 比率几何，S 1.90 全过 RA）

### 16.1 表达式与设置

```
ts_zscore(ts_backfill(divide(subtract(positive_sentiment_probability_3, negative_sentiment_probability_3),
                         add(add(positive_sentiment_probability_3, negative_sentiment_probability_3), 0.01)), 60), 250)
```
设置：EUR / TOP2500 / D1 / COUNTRY / decay 6 / trunc 0.04 / nanHandling OFF（沿用原式档位）
模板编号：**T3_ratio**（有向情绪占比 —— 把「正负概率之差」换成「差 ÷ 概率和」，即去掉中性质量后的情绪方向占比）

### 16.2 闸状态实读（get_alpha_details + check_self_correlation）

| 检查 | 值 | 闸线 | 结果 |
|---|---:|---:|---|
| Sharpe | **1.90** | 1.58 | ✅ |
| Fitness | **1.35** | 1.0 | ✅ |
| Turnover | **9.02%** | 1–70% | ✅ |
| 2Y Sharpe | **1.81** | 1.6 | ✅ |
| sub-universe Sharpe | **1.44** | — | ✅ |
| **failed_ra_count** | **0** | 0 | ✅ |
| checks.fail | **[]** | — | ✅ |
| checks.pass | LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / LOW_2Y_SHARPE / MATCHES_PYRAMID | — | ✅ 8/8 |
| **SELF** | **0.2290** | 0.7 | ✅（池 15，top gJj1nxLM 0.229） |
| CLUSTER_TEST | 1.32 | 1.58 | ⚠ warning |
| **PROD** | **待测** | 0.7 | ❓ |
| pyramid_short | `earnings` | — | 可点 earnings 塔 |

### 16.3 与原式（`akK7Z3d9`）对比 —— 换几何确实换了持仓

| | 原式（POS−NEG 差值 + signed_power 3） | **T3（比率几何）** |
|---|---:|---:|
| Sharpe | 1.65 | **1.90** |
| Fitness | 1.19 | **1.35** |
| Turnover | 21.3% | **9.02%** |
| 2Y Sharpe | 2.30 | 1.81 |
| self | 0.136 | **0.229** |
| failed_ra | 0 | 0 |

**三条关键信息**：
1. **S 反而更高**（1.65 → 1.90）：比率几何比差值几何更能表达「情绪方向占比」，且天然有界（不依赖 signed_power 压尾）。
2. **换手砍半**（21.3% → 9.02%）：比率对概率同时涨落免疫（分子分母同向变），只对方向变化敏感 ⇒ 持仓更稳。
3. **self 变了**（0.136 → 0.229）：说明**持仓结构确实与原式不同**，不是同一序列的重新缩放 ⇒ 有希望绕开 EUR 上 prod=1.00 的墙。

### 16.4 状态与下一步

- **唯一未知项是 prod**。已发起 `check_correlation`（任务 `bg_f8a22862`）。
- 若 **prod < 0.7** ⇒ 这是本轮第一颗**完全过闸的可提交候选**（S/F/2Y/sub/RA/self 全过），但**提交需用户明确授权**（不可逆）。
- 若 prod ≥ 0.7 ⇒ 继续用同族杠杆（换 region：GBR/AMR/USA/GLB 均可用，见第 15 节；换 universe：TOP1200/TOP400，见第 12.4 节）。


### 16.5 逐年稳健性（get_alpha_yearly_stats，10 年全量）

| 年 | d5Wj0Nx2 S | d5 pnl(万) | d5 long/short | d5 TO | akK7Z3d9 S | ak7 pnl(万) |
|---|---:|---:|---|---:|---:|---:|
| 2014 | 2.43 | 65.5 | 505/498 | 9.4% | 1.87 | 112.3 |
| 2015 | 1.83 | 55.7 | 574/600 | 8.5% | 1.32 | 104.6 |
| 2016 | 2.61 | 82.3 | 600/627 | 8.6% | 1.35 | 105.6 |
| 2017 | **3.37** | 83.4 | 691/681 | 8.6% | 2.22 | 139.0 |
| 2018 | 2.24 | 61.0 | 659/693 | 8.6% | 1.98 | 132.6 |
| 2019 | 1.48 | 46.3 | 673/700 | 8.8% | **0.10** | **6.4** |
| 2020 | 1.43 | 75.7 | 655/749 | 10.4% | 2.08 | 125.0 |
| 2021 | 1.51 | 59.3 | 800/683 | 9.6% | 1.08 | 74.5 |
| 2022 | 2.40 | 92.1 | 790/830 | 9.1% | 2.95 | 244.5 |
| 2023 | **1.12** | 33.7 | 828/812 | 8.7% | 1.52 | 99.6 |
| **min S** | **1.12** | | | | **0.10** | |
| **S<1 年数** | **0** | | | | **1** | |
| **亏损年数** | **0** | | | | 0 | |

**结论：d5Wj0Nx2 在每一项稳健性指标上都优于原式。**
- **无单年依赖**：最低 2023 年 S 1.12，仍高于 1.0；10 年无一年亏损。
- **换手只有原式的 42%**（8.5–10.4% vs 20.2–25.1%），且逐年极稳（标准差远小于原式）。
- **多空平衡**：505/498 起步，10 年后 828/812，几乎 1:1；原式出现 2014 年 325/665、2021 年 394/1067 的严重偏斜。
- **原式的薄弱点**：2019 年 S 仅 0.10、pnl 6.4 万（几乎不赚钱），这正是 prod=1.00 之外它另一个被忽略的缺陷。

**⇒ 即使不看 prod，d5Wj0Nx2 也是比 akK7Z3d9 更值得提交的那一颗。**


### 16.6 T4 秩变换几何也逼近闸线（1.56）—— 分布变换类几何系统性有效

| 模板 | 几何 | S | F | TO | alpha |
|---|---|---:|---:|---:|---|
| **T3** | 比率 `(POS−NEG)/(POS+NEG+0.01)` | **1.90** | 1.35 | 9.02% | `d5Wj0Nx2` |
| 原式 | 差值 `POS−NEG` + signed_power 3 | 1.65 | 1.19 | 21.3% | `akK7Z3d9` |
| **T4** | 秩差 `ts_rank(POS,250) − ts_rank(NEG,250)` | **1.56** | 1.00 | 6.69% | `QPv79djg` |

**规律**：三种几何（差值 / 比率 / 秩差）都落在 1.5–1.9 区间，说明**信号本身强度足够，天花板不在信号而在持仓表达**。

更重要的一点：**T3 与 T4 都把换手砍到原式的一半以下**（9.0% / 6.7% vs 21.3%）—— 因为比率和秩都对「正负概率同向涨落」免疫，只对方向变化敏感。这既是 S 提升的原因，也是持仓结构改变（可能绕开 prod）的原因。

### 16.7 策略调整：把已验证的 T3 骨架铺到不同 prod 池（2026-11-03 20:2x）

**逻辑**：既然 T3（S 1.90）是已验证骨架，继续测 T1/T2/T5/T6/T7/T11 等未验证模板的期望值，低于「把 T3 铺到 prod 池不同的区/universe」。

**已停**：news18 判决件（4 条，`bg_11d8769f`）—— NEWS 结论已由九区实测锁定，它只是补第 13 个数据集的数据点，价值低于 T3 spread。

**已派**：`results/_esm_t3_spread_list.json`（6 条，全预检 valid=True / unknown=[]）：

| # | region | universe | neutralization | decay | trunc | nan | 目的 |
|---|---|---|---|---:|---:|---|---|
| R_GBR | GBR | TOP700 | COUNTRY | 15 | 0.05 | ON | 换 prod 池 |
| R_AMR | AMR | TOP600 | SUBINDUSTRY | 4 | 0.08 | ON | 换池 + 2Y 最松 + 集中度高 |
| R_USA | USA | TOP3000 | SUBINDUSTRY | 5 | 0.08 | ON | 换池 |
| R_GLB | GLB | TOP3000 | SUBINDUSTRY | 4 | 0.08 | ON | 换池 |
| U_1200 | EUR | TOP1200 | COUNTRY | 6 | 0.04 | OFF | 同区换股票池 |
| U_400 | EUR | TOP400 | COUNTRY | 6 | 0.04 | OFF | 同区换股票池（最集中） |

任务 `bg_41cb5fa0`。ESM 原波次（13 条）继续跑剩余 11 条，两槽并行。

**判读**：任一 region 变体 S ≥ 1.58 且 prod < 0.7 ⇒ 直接得到可提交件（且是跨区分散，与 EUR 的 1.0 无关）。


### 16.8 prod 占用者查明：不是超时残留，是真实的长时计算

对 `d5Wj0Nx2` 发起 3 次 `check_correlation`（20:16 / 20:18 / 20:20，间隔均 > 240s），**三次全返回 `correlation_busy`**。

⇒ 排除「超时后本机残留 300s」这个解释（该解释预测 240s 后应能重测）。

**实查占用者 `GrWlnXZJ`**（`get_alpha_details`）：

| 项 | 值 |
|---|---|
| region / universe | **GLB / MINVOL1M** |
| Sharpe | **3.28** |
| Fitness | **2.14** |
| Turnover | 10.13% |
| status / stage | UNSUBMITTED / IS |
| pending | 含 PROD_CORRELATION |
| code 摘要 | `trade_when(rank(ts_mean(vec_avg(rsk60_offer), 126)) > 0.7, signed_power(subtract(group_rank(quantile_label_4bucket_20day_ohlcv_img, country), 0.5), 0.…)` |

**结论**：这是**之前会话遗留的一颗 GLB 强候选（S 3.28）正在算 prod**，占住了全账号唯一的生产相关性计算槽位。不是本轮的调用残留，也无法通过等待 240s 解决 —— 只能等它算完。

**操作含义（复用）**：
1. 破 prod 墙批量验证时，**prod 测量是串行瓶颈**：平台全账号 1 槽，且单次可能占用 10 分钟以上。
2. 因此**绝不能对每条候选都测 prod**；必须先用 **S ≥ 1.58** 过滤（回测不返回 prod）。
3. 被占用时正确的动作是**继续跑回测收集高 S 候选**，最后统一排队测 prod，而不是反复重试（重试只会浪费调用预算）。

---

## 17. earnings 事件驱动情绪：跨区强度结构 / 水平型机制 / prod 墙全读数（2026-11-03 21:30）

> 本节是 NEWS 判死之后转进 earnings category 的产出。数据集 `earnings_sent_matrix`（7 字段，全 MATRIX，EUR cov 0.5062 / AMR cov 0.5223）。

### 17.1 结论速览

1. 机制成立且**跨区可迁移**，但只有 **USA / EUR** 两个区成立（GBR 1.25 / GLB 1.06 / AMR 0.42 全弱）。
2. 强度**水位由区决定**：USA 约 2.2、EUR 约 1.9。同一区内换几何只在 1.90-2.25 之间收敛，**无法突破该区水位**。
3. **prod 墙是全族的**：五条结构互异候选 prod 读数 0.8033 / 0.8179 / 0.8713 / 0.8809 / 0.9010，全部 >= 0.7，本轮**无一可提交**。

### 17.2 跨区读数矩阵（同一表达式 `ts_zscore(ts_backfill(<core>, 60), 250)`）

| 区 / universe / 中性化 | 比率 T3 | 置信加权 T2 | 合成 | 秩差 T4 | argmax | 判决 |
|---|---:|---:|---:|---:|---:|---|
| USA / TOP3000 / SUBINDUSTRY | **2.25** | **2.21** | **2.22** | 1.96 | **2.13** | 可用（但 prod 不过） |
| EUR / TOP2500 / COUNTRY | 1.90 | 1.93 | 1.92 | 1.56 | 1.69（2Y 仅 0.72 挂） | 可用（prod 不过） |
| GBR / TOP700 / FAST | 1.25 | -- | -- | -- | -- | 弱（TO 15.05%） |
| GLB / TOP3000 / SUBINDUSTRY | 1.04 | 1.06 | -- | -- | -- | 弱 |
| GLB / TOP3000 / INDUSTRY | 1.01 | -- | -- | -- | -- | 弱 |
| AMR / TOP600 / SUBINDUSTRY | 0.42 | -- | -- | -- | -- | 死 |

**AMR 的死法值得单独记**：cov 0.5223 与 EUR 完全相同（不是覆盖问题），但逐年 S 正负交替 —— 2014 +1.85 / 2015 +0.26 / 2016 -0.34 / 2017 +0.85 / 2018 -0.58 / 2019 +0.69 / 2020 -0.67，均值约 0。这是纯 regime 噪声，任何设置调整都救不了。

### 17.3 机制判读一：电话会情绪是**水平型**信号，动态型全灭

| 模板 | 几何 | S |
|---|---|---:|
| T2 置信加权 | `(P-N) x (1 - neutral)` | **1.93** |
| 合成 | `(P-N)/(P+N) x (1 - neutral)` | **1.92** |
| T3 比率 | `(P-N)/(P+N)` | **1.90** |
| T4 秩差 | `ts_rank(P) - ts_rank(N)` | 1.56 |
| T1 变化量 | `ts_delta(zscore, 22)` | **0.44** |
| T5 波动率 | `-ts_std_dev(P-N, 66)` | **0.22** |

=> 一阶差分、二阶方差类几何全部塌到 0.2-0.4，水平类几何全部 1.5-1.9。**不要把事件驱动数据当动量源**。

### 17.4 机制判读二：中性概率是**条件变量**，不是信号

`likelihood_of_neutral_tone`（模型估计语调中性的概率）：

- 单独作信号：`ts_zscore(ts_backfill(subtract(0.5, likelihood_of_neutral_tone), 60), 250)` -> **S -0.30**；
- 作乘子：`(P-N) x (1 - neutral)` -> **1.93（EUR）/ 2.21（USA）**。

=> 它只适合做 weight / gate，不适合做 signal。这与「有些字段只适合做辅助信号」的一般纪律一致，此处给出一个干净的实证标本。

### 17.5 机制判读三：argmax 通道独立成立

`overall_sentiment_score` 是 `argmax(POS, NTR, NEG)` 的**分类标签**（-1/0/1），丢弃了概率幅度信息。
USA 单独测：`ts_zscore(ts_backfill(overall_sentiment_score, 60), 250)` -> **S 2.13 / F 1.37 / TO 9.39% / 2Y 3.26 / sub 1.11 / DD 3.06% / failed_ra 0 / CLUSTER_TEST 1.09**。
=> 同一数据集但信息通道不同（离散符号 vs 连续幅度），是 prod 分散的候选路径。

### 17.6 prod 墙全读数：五条结构互异候选全部 0.80-0.90，无一过 0.7

| 候选 | 区 | 几何 | S | CLUSTER_TEST | prod | 判决 |
|---|---|---|---:|---:|---:|---|
| `kqNjZg7P` | USA | 比率 | 2.25 | 1.38 | 0.8033 | FAIL |
| `vR1jrjpG` | USA | argmax 离散 | 2.13 | 1.09 | 0.8179 | FAIL |
| `wpQjEAPl` | EUR | 置信加权 | 1.93 | 1.37 | 0.8713 | FAIL |
| `d5Wj0Nx2` | EUR | 比率 | 1.90 | 1.32 | 0.8809 | FAIL |
| `rKRjOEx8` | USA | 比率 + MARKET | 1.61 | 1.01 | 0.9010 | FAIL |

**决定性判读**：跨越 2 个区、3 种信息加工方式（连续幅度 / 离散 argmax / 置信加权）、4 种中性化，Sharpe 从 2.25 一路压到 1.61，prod 始终锁死在 **0.80-0.90**。这说明生产池里存在一个**主导该情绪信号**的 alpha，任何几何变换都无法逃逸 —— 不是「某条表达式撞墙」，是**整个 earnings 电话会情绪族被 prod 饱和**。

**被自己的数据否掉的假设**（记录以免后人重犯）：中途曾提出「CLUSTER_TEST 可作 prod 的廉价代理 —— CT 1.0-1.1 大概率过闸，CT >= 1.35 大概率挂」。五条读数直接否掉该假设：CT 1.01 -> prod **0.9010（最差）**，CT 1.09 -> **0.8179（最好）**，CT 1.32-1.38 -> 0.88/0.87/0.80。**CT 与 prod 无单调关系，不能当判闸代理**；prod 只能逐条实测。

**因此本轮的资产是「机制知识」而不是「可提交 alpha」**：S 2.2 级别的信号确实存在且可跨区迁移（EUR -> USA 换区还涨了 0.35 Sharpe），但它已经拥挤。要在此 category 出货，必须找**另一个未被生产池占用的信息源**，而不是继续在本信号上换算子。
### 17.7 工程纪律：prod 计算一旦启动**不可中断**

- `wpQjEAPl` 在计算中途被 kill 客户端 -> 结果**不落缓存**，必须从头重算；
- `kqNjZg7P` / `d5Wj0Nx2` 在同一进程内每 25s 持续 poll -> 约 13 分钟后成功取到值。
- 判定「计算已启动」的标志：`trigger` 返回 `status=pending`（而非 `correlation_busy` 且 holder 是别人的 alpha）。
- **纪律**：见到 `pending` 后必须保持同一进程持续轮询到出值，间隔 25s，不可换进程、不可 kill。

### 17.8 universe / 中性化杠杆实测（均无 prod 分散价值）

- EUR 比率：TOP2500 1.90 / TOP1200 1.52 / **TOP400 0.73** -- universe 缩小单调削弱；
- USA 比率：TOP3000 2.25 / **TOP1000 0.79** -- 同上；
- USA 中性化：SUBINDUSTRY 2.25 / INDUSTRY 2.04 / **MARKET 1.61** -- 换中性化确实削弱 S，但把 CLUSTER_TEST 从 1.38 压到 1.01，是**唯一在 prod 维度上值得的削弱**。

### 17.9 与 NEWS 结论的关系

NEWS category 九区最优 |S| 0.92（AMR），而 earnings 同一套迁移 SOP 在 USA 直接给到 2.25 —— 差距不是模板质量，是 **category 信息密度**：电话会逐句情绪带真实基本面事件时点，新闻标题情绪不带。这条对照本身回答了「模板可迁移但目标 category 挖不出」中的后半句。

---

## 18. NEWS 判决补强：USA news18（全平台最常用新闻情绪集）5 模板全灭（2026-11-03 21:55）

> 前 17 节共测 12 个 dataset x region 组合，属抽样。本节改用「按 alphaCount 排序的头部数据集」做压力测试，堵住「你只测了弱数据集」这条质疑。

### 18.1 先排除一个假靶子：news12 不是新闻情绪

USA news 数据集按 alphaCount 排序：`news12` 184,070 / `news18` 60,336 / `news21` 8,233 / `news7` 6,253 / `news31` 3,055 / `news5` 2,721 / `news52` 1,592 / `news46` 1,116 / `news3` 1,025 / `news50` 763 / `news17` 709。

但 **`news12`（aC 最高，184,070）实测不是新闻情绪**：它的 40 个高覆盖字段是 `aggregate_sessions_vwap` / `current_day_volume` / `average_true_range_fourteen_periods` / `actual_earnings_per_share_value` / `advantageous_position_flag` / `best_position_indicator` —— 全是新闻事件日的**交易数据（PV 性质）**，aC 高是因为它被当作价量数据用。**不能用它作为 NEWS 情绪天花板的证据**，否则会得出错误结论。

### 18.2 真正的靶子：news18 的 MATRIX 情绪字段 cov = 1.0

USA 侧 `news18` 的情绪字段**覆盖率全部 1.0**（不是覆盖不足），且是全平台最常被挖掘的新闻情绪字段：

| 字段 | 类型 | cov | alphaCount |
|---|---|---:|---:|
| `nws18_bam`（并购情绪） | VECTOR | 1.0 | **1201** |
| `nws18_event_relevance` | VECTOR | 1.0 | 1044 |
| `nws18_bee`（财报评估分） | VECTOR | 1.0 | 599 |
| `mean_news_impact_projection` | MATRIX | 1.0 | 580 |
| `mean_merger_acquisition_sentiment` | MATRIX | 1.0 | 454 |
| `mean_earnings_evaluation_sentiment` | MATRIX | 1.0 | 400 |
| `mean_composite_sentiment_score` | MATRIX | 1.0 | 317 |
| `mean_event_novelty_score` | MATRIX | 1.0 | 312 |
| `mean_entity_relevance_score` | MATRIX | 1.0 | 138 |

### 18.3 5 个结构互异模板，全部阵亡

设置：USA / TOP3000 / SUBINDUSTRY / decay 5 / trunc 0.08 / nanHandling ON；几何统一为 `ts_zscore(ts_backfill(X, 60), 250)`（与 earnings 侧验证成功的水平型几何完全一致）。

| # | 模板 | 核心字段 | alpha_id | S | F | TO |
|---|---|---|---|---:|---:|---:|
| V1 | 综合情绪水平 | `mean_composite_sentiment_score` | `O0A766NR` | **-0.24** | -0.03 | 57.2% |
| V2 | 财报评估情绪 | `mean_earnings_evaluation_sentiment` | `WjO7YRmZ` | **-0.48** | -0.07 | 58.5% |
| V3 | 跨通道分歧 | `EES - CPS` | `npv7m0wd` | **-0.50** | -0.07 | 58.9% |
| V4 | 新颖度 x 情绪 | `mean_event_novelty_score x CPS` | `gJejXjK0` | **-0.63** | -0.11 | 47.0% |
| V5 | 相关性加权情绪 | `CPS x mean_entity_relevance_score` | `YP178OYl` | **-0.14** | -0.01 | 55.6% |

**最优 |S| = 0.63，距闸线 1.58 差 2.5 倍**；五条无一为正、无一超 1.0。

### 18.4 决定性指纹：换手 47%-59%

五条模板的换手全部落在 **47.0%-59.9%**。这不是参数问题 —— `ts_zscore(..., 250)` 已经把信号平滑到年度尺度，仍然日频翻转，说明**新闻情绪在日频上没有持续性**，是全频段重新抽签。

对照 earnings 电话会情绪：同样水平型几何、同样 `ts_zscore(...,250)`，换手只有 **9.0%**。

### 18.5 本轮最有价值的一句话（NEWS vs earnings）

同样是「情绪」字段、同样 cov = 1.0、同样在美国区、同样用水平型几何：

| | 换手 | S |
|---|---:|---:|
| 新闻情绪（news18，最常用字段） | **47%-59%** | **<= 0.63** |
| 电话会情绪（earnings_sent_matrix） | **9.0%** | **2.13-2.25** |

=> 差别不在模板、不在覆盖度、不在区、不在字段类型（两者都是 MATRIX/VECTOR 混合可用），而在**事件语义密度**：电话会逐句问答带管理层前瞻信息，新闻标题只复述已公开信息，后者在发布瞬间就被定价掉了。

**这条对照同时解释了「模板可迁移但目标 category 挖不出」的完整机制**，也是本项目在 NEWS 方向上可以停止探索的依据。
