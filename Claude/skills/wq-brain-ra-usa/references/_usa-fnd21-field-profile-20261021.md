# fnd21（ESG Scores）字段画像 — USA / TOP3000 / D1

- **as_of**：2026-10-21（平台 `get_datafields` 全量拉取，`filter_sharpe=false`，`complete=true`）
- **数据集**：`fundamental21` / `ESG Scores` / category=fundamental
- **规模**：平台声明 **142 字段**，实拉 **142**（未截断）；`userCount=61`，`alphaCount=154`
- **选定理由（换集说明）**：`analyst_consensus`（fa overlay）六个机制已全部走死（见 `_usa-analyst-consensus-fa-overlay-field-profile-20261021.md` §17.10），
  按目标约束第 2 条换集。候选逐一排除：
  - `other452` / `fundamental93`（Earnings Tax，46 字段）结构同源，fnd93 已判死（cov 0.3–0.4 使 `group_rank` 退化为覆盖度押注，max S 0.99）；
  - `fundamental69`（Quarterly Fundamental，11 个标量）经济内容 = 经营现金流 / 资本开支 / 债务 / 分红，落在 **USA 已饱和的 value-quality-book 族**（本区该类线性变体必死），且 cov 0.39–0.43 同样触发覆盖度押注；
  - `fundamental110`（Press Release）过滤后只剩 7 个 VECTOR 元数据字段（日历期 / 修订号 / 原始值），无标量经济内容；
  - `fundamental72`（1852 字段，aC 3082）覆盖最好但拥挤度最高，prod 风险最大，留作备选。
  - **fnd21 是本区 alphaCount 最低的可挖 fundamental 集（全库 154）**，且经济内容是 ESG 新闻情绪，**与已死的 value/quality/book 正交**。

### 0.5 与 2026-10-19 那轮 40 条穷举的对接（**重开本集的前提**）

⚠ 本集**不是新集**：`_usa-fnd21-field-profile-20261019.md` 已记 40 条实测，
结论是「S ↔ SUB 硬 Pareto 前沿，TOP3000 下结构性不可达」：

| 2026-10-19 前沿点 | S | F | 2Y | SUB | SUB/S |
|---|---:|---:|---:|---:|---:|
| 最大 S（`tail(combo,0,0.15,0)` #35） | 1.52 | 1.02 | 1.97 | 0.50 | 0.33 |
| 折中（#29 双背离） | 1.49 | 0.97 | 1.94 | 0.43 | 0.29 |
| 最大 SUB（#24 `ts_quantile(cauchy)` 单腿） | 1.17 | 0.69 | 1.83 | 0.72 | 0.62 |

外推：S=1.58 时 SUB/S≈0.30 ⇒ SUB≈0.47 ≪ 0.687。**那轮的根因判断是「ESG 覆盖偏大盘，子宇宙无 alpha」**。

**本波重开的依据是三条轴从未在 fnd21 上联合测过**（不是重复扫参）：

| 轴 | 2026-10-19 那轮 | 批次 18 |
|---|---|---|
| 时序变换 | `ts_rank` / `ts_zscore` / `ts_delta` / `ts_quantile` / `ts_corr` | **`ts_av_diff(core, 504\|252)`**（Change 桶；analyst 战役两颗 ACTIVE 的同款壳） |
| 中性化 | SUBINDUSTRY / INDUSTRY / market 轴 + 单腿 CROWDING 探针（#40） | **CROWDING + decay 10**（analyst 战役 SUB 比值 1.31–1.40×S 的那一档） |
| 平滑 | `hump=0.01` / 0.005 | **无 hump**（有界评分的量级与比率型核不同，0.01 有清零多数样本的风险） |

**为什么值得一测**：analyst 战役里 CROWDING + `ts_av_diff` 的 SUB 比值是 1.31–1.40×S，
是 fnd21 前沿（0.29–0.62）的 2–4 倍 ⇒ SUB 约束并非壳层内生的，**若壳层可迁移则 SUB 闸不是瓶颈**。

**预登记判死线（事后不得放宽）**：批次 18 八条里若**无一**满足
`S ≥ 1.52 且 SUB/S ≥ 0.43`（即至少追平 #35 的 S、且比值高于前沿外推 0.30），
则判定 **fnd21 壳层救援失败**，本集关闭，不再发第三波，转 `fundamental72`（aC 3082，拥挤度最高但覆盖 0.745、字段 1852）或 `other416`（aC 1711）。

## 1. 全量字段分类（142/142 已归类）

**全部字段类型均为 `VECTOR`，零 `MATRIX`、零 `GROUP`** ⇒ 任何表达式都必须先做 `vec_*` 聚合，再进标量算子。

| 族 | 计数 | 命名形态 | 语义 |
|---|---:|---|---|
| `…_insight` | 42 | `fnd21_allcategories_insight_<主题>_insight` + `…industrypercentile_insight` | 长周期「洞察分」：新闻中该 ESG 主题的深度评分（21 主题 × {原始, 行业分位}） |
| `…_momentum` | 48 | `fnd21_allcategories_momentum_<主题>_momentum` + `…industrypercentile_momentum` | 趋势度量：该主题新闻语调/关注度的中期走向（24 主题 × 2） |
| `…_pulse` | 21 | `fnd21_allcategories_pulse_<主题>_pulse` | **短周期实时**表现分（无行业分位变体） |
| `datasecurity`（独立小族） | 5 | `fnd21_datasecurity_{insight,momentum,pulse,…}` | 单一主题（数据安全）的三种分数 + 2 个行业分位 |
| `volume_ttmdaily_*` | 15 | `…_articlevolumettm` / `…_categoryvolumettm` | 过去 12 个月新闻条数（**关注度 / 曝光量**，非评分） |
| `*_impactpercentagettm` | 11 | `fnd21_<主题>_impactpercentagettm` | 相关新闻的「影响占比」 |
| **合计** | **142** | | 42+48+21+5+15+11 |

分子族结构：每个主题都有 `{insight, momentum, pulse}` 三条**不同时间尺度**的评分 + 若干 `industrypercentile` 版本（**已在同业内做过横截面归一**）+ 可选 `volume` / `impact%`。

## 2. 覆盖率画像

覆盖 ≥0.6 的字段共 **16 个**（其余 126 个 <0.6）。按族看，覆盖天花板集中在**聚合主题**：

| 字段 | cov | aC | uC | 桶位 |
|---|---:|---:|---:|---|
| `fnd21_allcategories_momentum_allcategories_momentum` | **0.8768** | 3 | 3 | 主核（趋势） |
| `fnd21_allcategories_momentum_allcategoriesindustrypercentile_momentum` | 0.8766 | 1 | 1 | 同业内相对版本 |
| `fnd21_allcategories_pulse_allcategories_pulse` | **0.8431** | 10 | 3 | 主核（短周期） |
| `fnd21_allcategories_insight_allcategories_insight` | **0.8419** | 7 | 5 | 主核（长周期） |
| `fnd21_allcategories_insight_allcategoriesindustrypercentile_insight` | 0.8415 | 9 | 6 | 同业内相对版本 |
| `fnd21_allcategories_momentum_materiality_momentum` | 0.8071 | 0 | 0 | 主核（重要性加权） |
| `fnd21_allcategories_momentum_materialityindustrypercentile_momentum` | 0.8068 | 2 | 2 | 同上相对版 |
| `fnd21_allcategories_pulse_materiality_pulse` | 0.7715 | 5 | 2 | 短周期重要性 |
| `fnd21_allcategories_insight_materiality_insight` | 0.7703 | 1 | 1 | 长周期重要性 |
| `fnd21_allcategories_insight_materialityindustrypercentile_insight` | 0.7695 | 3 | 3 | 同上相对版 |
| `fnd21_volume_ttmdaily_allcategories_articlevolumettm` | 0.7671 | 3 | 3 | **关注度** |
| `fnd21_volume_ttmdaily_allcategories_categoryvolumettm` | 0.7671 | 1 | 1 | 关注度（口径二） |
| `fnd21_materiality_categoryvolumettm` | 0.6644 | 2 | 2 | 重要性关注度 |
| `fnd21_volume_ttmdaily_materiality_articlevolumettm` | 0.6644 | 0 | 0 | 同上 |
| `fnd21_allcategories_momentum_businessethics…_momentum` | 0.6308 | 0 | 0 | 单主题（商业伦理） |
| `fnd21_allcategories_momentum_businessethics…industrypercentile_momentum` | 0.6304 | 0 | 0 | 同上相对版 |

**覆盖率分档**：≥0.8 = 7 个；0.6–0.8 = 9 个；<0.6 = 126 个（单主题大多 0.26–0.55）。

**单主题覆盖矩阵（momentum / insight / pulse，节选）**

| 主题 | momentum | insight | pulse |
|---|---:|---:|---:|
| allcategories | 0.8768 | 0.8419 | 0.8431 |
| materiality | 0.8071 | 0.7703 | 0.7715 |
| businessethics | 0.6308 | 0.5959 | 0.5976 |
| fairlaborpractices | 0.5458 | 0.5165 | 0.5178 |
| supplychainmanagement | 0.5082 | 0.4789 | 0.4801 |
| energymanagement | 0.4827 | 0.4549 | 0.4559 |
| productqualityandsafety | 0.4807 | 0.4541 | 0.4552 |
| diversityandinclusion | 0.4737 | 0.4462 | 0.4475 |
| ghgemissions | 0.4735 | 0.4477 | 0.4486 |
| employeehealthsafety | 0.4520 | 0.4256 | 0.4270 |
| regulatorycapture / lifecycle / productpackaging | 0.42–0.43 | 0.40 | 0.40 |
| datasecurityandcustomerprivacy | 0.4207 | 0.3967 | 0.3979 |
| competitivebehavior | 0.4150 | 0.3926 | 0.3938 |
| accessandaffordability | 0.3882 | 0.3658 | 0.3668 |
| biodiversityimpacts | 0.3628 | 0.3412 | 0.3421 |
| fairdisclosure / fairmarketing | 0.3430 | 0.3229 | 0.3239 |
| waterandwastewater | 0.3351 | 0.3150 | 0.3158 |
| accidentandsafetymanagement | 0.3004 | 0.2822 | 0.2830 |
| customerwelfare / materialssourcing / waste | 0.262 | — | — |

> 读数：**单主题字段一律落在 0.26–0.55**，低于 0.4 的按本 skill 硬纪律必须显式 `ts_backfill` / `group_backfill` 或弃用；
> 本画像的主核全部取 **≥0.77 的聚合主题**，**不依赖 backfill**。

## 3. 更新频率与分布（推断 + 待实测）

- **更新频率（按字段名与语义推断，未做 Labs 实测）**：`pulse` = 短周期实时（事件驱动，日级变动）；`momentum` = 中期趋势（周–月级平滑）；`insight` = 长周期评分（月级）；`volume_ttmdaily_*` = 滚动 12 个月计数（日级增量、缓慢变化）。**实测口径**应由 Labs 的字段频率脚本确认，属未验证项。
- **分布**：未做原始分布实测。设计上已用 `quantile()` 包住最终输出 ⇒ 进 PnL 前已转成横截面均匀分布，原始量纲不影响结果；但 `hump` 阈值会受**原始值量纲**影响（评分类字段与比率类字段量级不同，见 §5 禁区）。
- **VECTOR 语义（未在 Labs 验证）**：字段命名含 `allcategories_*_allcategories`，向量维度最可能是**时间快照序列**（而非主题维度），因此 `vec_stddev` 读作「该股 ESG 分数的时序离散度」而不是「跨主题分歧」。若后续实测证明维数是主题，则 `vec_stddev` 应改读作跨主题分歧 —— **两读法都指向 dispersion 机制，方向一致，故不阻塞首波**。

## 4. 机制映射（6 桶，本集可覆盖 6/6）

| 桶 | 本集实现 | 核心字段 | 经济含义 |
|---|---|---|---|
| **Change** | `ts_av_diff(vec_avg(x), 252\|504)` | momentum / insight | ESG 新闻语调相对自身长期均值的偏离 |
| **Surprise** | `vec_avg(pulse) − vec_avg(momentum)` | pulse × momentum | 短周期表现 vs 中期趋势的意外差 |
| **Attention / Event-conditioned** | `trade_when(ts_zscore(vol)>t, …, -1)` | volume_ttmdaily | 只在曝光异常日交易 ESG 信号 |
| **Dispersion** | `vec_stddev(momentum)`；`原始分 − 行业分位分` | momentum | 评分的时序/跨主题离散度 |
| **Propagation** | `group_rank(x, industry)` 或直接用 `industrypercentile` 版本 | *industrypercentile_* | 同业内扩散 / 相对领先 |
| **Level** | 原始评分水平（`quantile(vec_avg(x))`） | insight | 静态 ESG 质量（拥挤时失效） |

**跨家族红线**：本集可用字段全部来自 fnd21 一个数据集，满足 ATOM；不与其它数据集字段相加。

## 5. 可用性与禁区

- **必须 `vec_*` 聚合**：直接用 VECTOR 字段进 `ts_*` / `rank` 会报类型错。首波统一 `vec_avg`，第二波轮换 `vec_max` / `vec_stddev`（本 skill 要求含 VECTOR 时 ≥2 种聚合）。
- **`hump` 阈值必须按量纲重设**：本会话已验证的 `hump=0.01` 是给**比率型**核（analyst 修正率，量级 ~0.1–1）用的；ESG 评分是**有界分数**，`ts_av_diff` 的输出量级远小于比率，`hump=0.01` 可能把大部分样本清零 ⇒ 首波**不挂 hump**，先读裸信号的 TO，再在第二波按实测 TO 定量级。
- **不要用 `exchange` / `market` / `sector` 当字段**（本集本来也没有）：它们是豁免字段；`market` 只作为 `group_rank` 的分组参数出现。
- **不要信 `industrypercentile` 与原始分同时入式**：两者高度共线（同一底层分数的两种归一），同时入式等于重复计权；只能二选一，或做**差值**（`原始 − 行业分位`）作为「行业内定位」机制。
- **低覆盖单主题（<0.4）不用**：`customerwelfare` / `materialssourcing` / `waste` / `accidentandsafety` / `waterandwastewater` / `biodiversity` / `fairdisclosure` / `fairmarketing`。

## 6. 首波预登记（batch 18）

壳层：`quantile(group_rank(ts_av_diff(vec_avg(core), W), market))`（**不挂 hump，不挂 winsorize/backfill**，先读裸信号）
设置：USA / TOP3000 / D1 / truncation 0.08 / decay 10 / neutralization **CROWDING** / 其余同区域 settings。

| 臂 | 核 | W | 符号 |
|---|---|---:|---|
| P1 | momentum_allcategories | 504 | 正 |
| P2 | pulse_allcategories | 504 | 正 |
| P3 | insight_allcategories | 252 | 正 |
| P4 | momentum_materiality | 252 | 正 |
| P5–P8 | 同 P1–P4 | 同 | **反号**（`-1 *`） |

**判据（预登记，事后不得放宽）**：S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / TO ≥ 1.0% / SUB ≥ 0.43×S；
**全过后才测 prod**（D0-P：<0.60 正常 / 0.60–0.70 不出变体 / 0.70–0.75 一次定因尝试 / ≥0.75 判死）。

**首波要回答的三个问题**：
1. 方向（正/反号）—— ESG 新闻语调是动量还是反转；
2. 时标（pulse vs momentum vs insight）—— 哪条时间尺度携带 S/2Y；
3. 壳层可迁移性 —— analyst 上的 `ts_av_diff` 承重壳在 VECTOR 评分上是否仍承重（若三条核全部 S<1，说明壳层不可迁移，须换 `ts_zscore` / `group_rank` 级别壳）。

## 7. 复现与索引

- 字段全量：`get_datafields(dataset_id="fundamental21", region="USA", delay=1, universe="TOP3000", filter_sharpe=false)` → `count=142, platform_count=142, complete=true`
- 同源统计：`get_datasets(category="fundamental", region="USA", delay=1, universe="TOP3000")` → 23 集
- 本画像字段族计数（42/48/21/5/15/11）与 `count=142` 对账一致，无遗漏。
- 本文件只做画像与预登记；读数与归因在本文后续章节追加。

## 8. 论坛取证（2026-10-21，三条，按正文核实）

| # | 帖子 | 关键事实 | 对本集的含义 |
|---|---|---|---|
| 1 | 《当 ESG 评分变成每日更新的实时数据（ESG Scores Data）》`article_id=43691553444247`，2026-09-23，24 票 | **就是 fundamental21 本集**：为 8000+ 公司提供实时 ESG 评分，AI/NLP 从新闻报告持续聚合，产出 **每日 / Pulse（短期）/ Insight（长期）/ 动量** 四类分数，覆盖 **30 个 SASB 类别**，含行业百分位与事件量。作者判断：**「相对变化可能比绝对分数更有研究意义」**；评分是模型产物、口径不透明，**绝对水平跨行业不可比**；使用时应**把「说了什么」（情绪）与「发生了多少次」（频率）分开** | ① 证实本集是**动态事件流**而非静态评级 ⇒ Change / Surprise 桶优先于 Level 桶（与 §4 一致）；② 证实「情绪 × 频率」是两个独立维度 ⇒ `momentum/pulse` 与 `volume_ttmdaily` 的交叉是**设计内**的正交配对，不是混信号；③ 证实跨行业绝对分不可比 ⇒ **中性化必须按行业**，`group_rank(…, market)` 只解决全市场、不解决行业内口径差 |
| 2 | 《一个基于 ESG 评分与熵指标的 Alpha 思路》`article_id=34421736616855`，2025-08-25，33 票 | 可复现模板：`ts_entropy(group_rank(ts_backfill(<ESG字段>,90), sector), 20)` —— **行业内相对排名的时序熵** = 「该公司在行业内 ESG 相对地位的不稳定性」；作者经济解释：高熵 ⇒ 市场对它的 ESG 定价存在分歧 ⇒ 潜在风险/预期差。作者建议的改进方向：换分组（sector/subindustry/industry/market/country）、换熵窗口（20/60/120）、加 rank/zscore 平滑 | 提供一条**本会话从未用过的壳**（`ts_entropy` 包排名），与 `ts_av_diff` 壳机理不同（前者测「相对地位波动」，后者测「自身水平偏离」）。列为下一波候选壳，**不替换**首波（首波要回答壳层可迁移性，变量越少越好）。注意其用 `ts_backfill(...,90)` 是因 analyst11 覆盖低；本集主核 cov ≥0.77，**不需要 backfill** |
| 3 | 《数据集子分类分析与中性化策略匹配方法》`article_id=36224596669335`，2025-11-10，12 票 | 官方推荐：**Fundamental → INDUSTRY**；子分类级：**Analyst-ESG → SECTOR / INDUSTRY**；Analyst-Crowdsourced → CROWDING/STATISTICAL；Analyst-Estimates → SECTOR/FAST。作者主张「同一大分类下不同 subcategory 数据特征差异大，不能一律用同一种中性化」 | **直接挑战首波选用的 CROWDING**。本集属 fundamental 下的 ESG（= Analyst-ESG 同族特征），社区口径指向 **INDUSTRY / SECTOR**。首波已在途不改（保证可归因），**批次 19 必测 INDUSTRY / SECTOR / SUBINDUSTRY**，与 CROWDING 并列比较 |
| 4 | 《无脑用 ts_backfill 不是一个好主意…》`article_id=43273417454487`，2025-09-05 | 截面覆盖不均的卖方预期 / **ESG 评分**类数据在大中盘覆盖高（可达 95%），小盘稀疏；应区分 `ts_backfill` / `group_backfill` / `to_nan(x, value=0, reverse=true)` 三种补法 | 本集主核 cov 0.77–0.88（缺口来自小盘）⇒ 若后续要提高覆盖，**优先 `group_backfill`（按行业补）而不是 `ts_backfill`**（后者会把停更僵尸股一起补活） |

**可复用结论（写入本 skill 证据池）**：
- **ESG 类字段的第一性特征是「事件流」，不是「评级」** ⇒ 用 Change / Surprise / Attention-gate 三桶，别堆 Level。
- **行业口径不可比是结构性的**（评分来自不同行业的新闻密度），所以 **industry 维度的归一/中性化是承重件**，不是可选装饰。
- **`ts_std_dev(group_rank(x, sector), W)` 是一条独立壳**（原拟用 `ts_entropy`，但该算子是已登记幽灵算子、平台不存在 ⇒ 改用同义的 `ts_std_dev` 作波动量）：它把「行业内相对地位的波动」当信号，与 `ts_av_diff`（自身水平偏离）正交，值得作为新壳候选。
- **情绪与频率要分开建模**（`momentum/pulse` vs `volume`），二者相乘/门控是设计内配对。

---

## 9. 批次 18 收批（2026-10-21）：冠军壳 `ts_av_diff` 迁移测试

**设置**：USA/TOP3000/D1，decay 10，**CROWDING**，trunc 0.08，**无 hump**。
**壳**：`quantile(group_rank(ts_av_diff(vec_avg(<core>), W), market))`；B 组 = `-1 * (…)`。
**multisim**：A `1l2LG67ar50faHPpUEizELh` / B `2l82Yd3dP4JKaO51ayARJkKM`（8/8 COMPLETE，无 ERROR）。

| # | 核 | W | S | F | 2Y | SUB | **SUB/S** | TO | 过闸情况 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| P1 | momentum allcat | 504 | 1.09 | 0.60 | 1.25 | 0.67 | **0.61** | 1.54% | S−0.49 / F−0.40 / 2Y−0.33 |
| P2 | pulse allcat | 504 | 0.99 | 0.54 | 0.87 | 0.63 | **0.64** | 3.54% | 三闸全缺（最差） |
| P3 | insight allcat | 252 | 1.19 | 0.71 | 0.96 | 0.80 | **0.67** | 1.62% | S−0.39 / F−0.29 / 2Y−0.62 |
| P4 | momentum **materiality** | 252 | **1.23** | **0.75** | **1.45** | 0.45 | 0.37 | 1.60% | S−0.35 / F−0.25 / 2Y−0.13 / **SUB 0.45 < 0.53** |
| P5–P8 | 四条 `-1 *` | — | 逐位镜像 | | | | 同比值 | | 全负 S（无反向结构） |

`alpha_id`：P1 `88vvLXZX` / P2 `P0MM1KmL` / P3 `akVVOGmW` / P4 `d5KKQvJv`；P5 `JjPPd3bE` / P6 `A1QQ3Lkl` / P7 `ZYmmoXr1` / P8 `YPxxAlAq`。
**镜像已抽验 2/4**（P5 vs P1、P6 vs P2 逐位取负：S −1.09 / −0.99，TO / SUB / DD 完全同值）；
P7 / P8 按 `-1 *` 构造必然镜像，未单列。

### 9.1 三个预登记问题的答案

| 问题 | 答案 | 证据 |
|---|---|---|
| **1. 方向** | **只有正号有信息**。反向 = 精确镜像（S 取负），不是独立信号 | P5/P6 与 P1/P2 逐位取负 |
| **2. 时标** | **materiality-momentum(252) 最强 S/2Y，insight(252) 最强 SUB 比值，pulse(504) 最差** | P4 S1.23/2Y1.45 vs P3 SUB/S 0.67 vs P2 S0.99/2Y0.87 |
| **3. 壳层可迁移性** | **半迁移**：SUB 比值迁移成功（0.61–0.67，远超 0.43 闸），**S 强度不迁移**（analyst 1.6–2.0 → fnd21 1.09–1.23，掉 0.4–0.9） | 见 §9.2 |

### 9.2 归因：为什么 SUB 过了、S 上不去

1. **壳层的失败模式被彻底改变**：2026-10-19 那轮的主病症是 `SUB/S 0.29–0.62 且 S↑⇒比值↓`；
   本壳把三臂的比值稳定在 **0.61–0.67**（P4 除外），**SUB 闸从"结构性不可达"变成"默认通过"**
   ⇒ 此前"ESG 覆盖偏大盘、子宇宙无 alpha"的诊断**只对 `hump + group_rank` 壳成立，不是数据集属性**。这是本轮最重要的更正。
2. **但 S 的天花板跟着壳走不动**：同样的 `ts_av_diff` 壳在 analyst 上给 1.6–2.0，
   在 fnd21 只给 1.09–1.23。差别在**信号本身的动态范围**：
   ESG 分数有界（0–100）+ 慢变，504 日变化量的截面离散度被压缩，
   `quantile(group_rank())` 之后可交易的秩差很小 ⇒ **壳不是瓶颈，核的 IC 是瓶颈**。
3. **S ↔ SUB 的交换仍在**（只是位置抬高了）：独占 S 最优的 P4（materiality）SUB 比值掉到 0.37，
   独占 SUB 最优的 P3 2Y 掉到 0.96 ⇒ **两条腿不能在同一核上同时满足**，与 2026-10-19 的结论同向。

### 9.3 判决：fnd21 关闭（按 §0.5 预登记线执行）

预登记线 = **S ≥ 1.52 且 SUB/S ≥ 0.43**。本波最高 S = **1.23**（缺 0.29），
最高 SUB/S = 0.67（S 1.19）。**无一命中 ⇒ fnd21 壳层救援失败，本集关闭，不发第三波。**

累计口径：fnd21 共 **48 条**实测（2026-10-19 的 40 条 + 本轮 8 条），
两套壳、6 机制、8 算子族、5 种中性化，**S 上限 1.52（D0 前峰）/ 1.23（本壳），均低于 1.58**。
⇒ **fnd21（ESG Scores）在 USA/TOP3000/D1 不具备交付能力**，与 universe 无关的判死理由成立（覆盖率结构性偏大盘）。

### 9.4 三条可迁移结论（与本集无关也成立）

1. **`CROWDING + ts_av_diff` 是"SUB 保险"**：三臂把 SUB/S 稳在 0.61–0.67，
   而 `hump + group_rank + SUBINDUSTRY` 在同一个集上只有 0.29–0.52 ⇒
   **在 SUB 卡死的集上，先换壳（`ts_av_diff` + CROWDING）再谈换字段**。
2. **有界评分（0–100）上不要用 `ts_av_diff` 长窗求强度**：它能救 SUB 比值，
   但变化量的动态范围被有界性压死，S 天花板落回 1.2 附近。有界评分应走**背离 / 相对占比**（2026-10-19 #29/#35 给到 1.49/1.52）。
3. **反向是镜像 ⇒ 无独立信息**：`-1 * quantile(group_rank(...))` 的八条里两条抽验逐位取负。
   这与 analyst 的"反向另有一套结构"不同 —— 判据是**核是否含符号含义**（ESG 分数取反 = 纯反转，analyst 修正取反 = 下修动量）。
