# GBR NEWS 模板总结 与 跨区迁移设计（2026-11-03）

> 目的：①把 GBR 的 NEWS 挖掘沉淀成**可迁移的模板族**（不再依赖 GBR 具体字段）；②据此在**其它 region 的 NEWS category** 下挖 regular alpha。
> 本文两部分：**Part A = GBR 模板总结**（含 6 条结构性教训）；**Part B = 跨区迁移地图 + CHN 首波设计**。

---

# Part A · GBR NEWS 模板总结

## §A1 统一基底（GBR 现行档，唯一被固定的部分）

```
G(SIG) = ts_target_tvr_decay(
           group_neutralize(
             -ts_rank(ts_mean(SIG, 60), 252),
             densify(market)),
           target_tvr=0.05, lambda_max=5, lambda_min=0)
```

GBR 设置档：`region=GBR / universe=TOP700 / delay=1 / neutralization=FAST / decay=15 / truncation=0.05 / unitHandling=VERIFY / nanHandling=ON / maxTrade=OFF / pasteurization=ON / language=FASTEXPR`

**只有 `SIG` 的结构不同** ⇒ 归因干净，且不存在「换窗口/换常数当模板」的伪多样性。

## §A2 ★ 五条独立轴（NEWS 塔的容量上限 = 5，不是 6）

零成本互相关实测（阈值 0.7）证明：GBR NEWS 家族**只有 5 条信息轴**，其余全是同轴变体。

| 轴 | 语义 | 代表 alpha | 与其它轴最大相关 |
|---|---|---|---:|
| **A 新闻到达率** | level / 偏离 / ×广度 / 跨集门控 | `wpQwjWn6`（news17 level） | 0.8468（轴内） |
| **B news18 sse** | 事件级情绪强度 level / 比值 | `6XdPedNJ`（P1 裸 level） | 0.8346（轴内） |
| **C 事件强度求和** | `vec_sum(event_relevance)` | `leA6jmoe`（W4） | 0.6642 |
| **D 情绪分到达率** | `vec_count(event_sentiment_score)` | `9qxPX77V`（W1） | 0.6583 |
| **E 合成置信** | `ssc × 新颖度` 乘子 | `58E7jkaN`（S1） | 0.6642 |

**⇒ 换轴只有两条路**：① 换**语义不同**的字段；② 换数据集。
换结构（比值/门控/偏离/交互）**救不了相关性**——载体是字段本身的信息轴，不是结构，也不是来源数量。

## §A3 ★★ 六条可迁移的结构性教训（跨区复用时直接照用）

| # | 教训 | 证据 |
|---|---|---|
| L1 | **相关性的载体 = 字段的信息轴，不是结构** | S4 比值 vs P1 裸 level 同字段不同结构 ⇒ 0.8346；X1 跨集门控 vs W3 裸 level ⇒ 0.8294 |
| L2 | **强几何 ≠ 弱几何**：同一批字段在弱几何 `group_rank(ts_mean(x,22),subindustry)` 上 S 上限仅 0.91（N3），搬到强几何后 S 达 1.86–2.18 | news18 N1–N10 全灭 → news_strong_geometry S1–S10 两条全闸 |
| L3 | **`vec_count` 对完全填充的同事件字段是恒等变换**（统计记录条数，多字段取值逐位相同） | `vR1nAj6z`(nip) ↔ `wpQwjWn6`(relevance) 相关 **1.0000** |
| L4 | **量纲恒等变换要提前排除**：`winsorize` 接在 `ts_rank` 之前 = 恒等；`ts_zscore` 前置在 `ts_rank∘ts_mean` 前 ≈ 冗余 | S6/S8 撤回派发 |
| L5 | **二阶矩几何在「事件到达率」类字段上无信息**（自相关/残差/回归全灭） | S7 S 0.11、S9 残差恒 0 |
| L6 | **字段角色不同 ⇒ 同一字段当乘子有效、当信号本体无效** | `event_similarity_days` 作乘子 → 全闸 `58E7jkaN`；作信号本体 → S **−0.33** |
| L7 | **掩码类模板双杀**：遮掉半区 ⇒ TO 推高 + 广度被砍 ⇒ F 崩 | S2 `kqNkNQ7l` S 1.45 / F 0.78 |
| L8 | **裸 `rank(sentiment)` 禁用**；水平类情绪走慢平滑后截面排序，变化类情绪配 `ts_decay_linear`/`ts_target_tvr_decay` | forum `42659817284375` |

## §A4 平台侧硬约束（迁移时照搬）

1. **换手超标先归因三分类**（数据源高频翻转 / 信号构造放大噪声 / 权重集中），`decay` 只平滑值的抖动、平滑不了排名的翻转。
2. **`target_tvr` 必须与信号自然换手同量级**（0.7–1.2 倍）；压到 1/8 会把快信号抹平（S 1.81 → 0.04）。
3. **`ts_mean(·,5)` 对新闻字段是必选前置**，不是可选优化（news104 实证）。
4. **prod 是唯一真瓶颈**：闸是降 prod 的唯一有效手段；设置类杠杆（中性化/universe）对 prod 的极限收益约 0.06。
5. **浅钉（n=1，[0.7,0.8)）不判死**，破墙首选 = **同信号几何换面**（quantile↔zscore↔rank），窗口位移对 n=1 无效。

---

# Part B · 跨区迁移地图

## §B1 全平台 NEWS 数据集存量盘点（2026-11-03 实拉 get_datasets，14 region）

⚠ **universe 必须用各区 default_universe**（`src/wqb/config.py`）：传 TOP3000 给 EUR/ASI/CHN/IND/JPN/KOR/TWN/HKG/DEU/MEA/AMR/GBR 会**返回空**（不是没数据）。

| region | universe | NEWS 集数 | 备注 |
|---|---|---|---|
| USA | TOP3000 | 26 | news18 aC 60336（重饱和） |
| GLB | TOP3000 | 15 | |
| EUR | TOP2500 | 20 | |
| ASI | MINVOL1M | 22 | |
| IND | TOP500 | 22 | |
| KOR | TOP600 | 24 | **news 塔已全清点 24 集**（`tracking/KOR/reference/datasets/news_tower_inventory.md`），仅 news20 一条缝 |
| HKG | TOP800 | 24 | |
| DEU | TOP500 | 17 | **已做过 news20/17/104/29/38/50 模板池 + 剖面** |
| CHN | TOP2000U | 9 | **★★★★ 处女区：aC 3–7，valueScore 5–6** |
| AMR | TOP600 | 28 | news29 aC=5 / news84 aC=25 / news81 aC=31 |
| **JPN / TWN / MEA** | — | **0** | **平台无 NEWS 数据集** |

## §B2 ★ 跨区迁移的「机制×数据集」二维律（不能按集封杀）

GBR news17 波 1/2 + W7-neg + B1–B10 共 30+ 模板全灭后，DEU 的 news20（同构字段族、aC 33/27）**重开同机制**并被判为头号矿位。
⇒ **同一机制在不同数据集必须重测**；反之，**同一数据集的不同机制**（如 news46 的 `ens_elapsed` 时间链）也必须重测。

## §B3 各区 NEWS 已挖/未挖盘点（避免重复烧配额）

| region | 状态 | 证据 |
|---|---|---|
| **GBR** | 5 轴挖透（news17/18/20/38/50/104 全判死，仅 contrarian 聚合族活） | `docs/reference/template_library_gbr_news_strong_geometry.md` |
| **DEU** | news 6 集已做模板池+剖面 | `tracking/DEU/reference/dataset_landscape_2026-11-03.md` |
| **KOR** | 24 集全清点，只剩 news20 的 `nip`/`ber` 两条轴 | `tracking/KOR/reference/datasets/news_tower_inventory.md` |
| **CHN** | **只做过 `market_news_sent`/`news_sentiment_enriched`/`news29`（45 次回测、0 条过闸）**；**news46/news38/news50/news11/news79/news7 未开** | `tracking/CHN/config/cells.json` |
| AMR / HKG / ASI / IND | 无本地 NEWS 台账 | — |

---

# Part C · CHN 首波设计（★★★★ 处女区）

## §C0 选靶：CHN / news46（Relevant News Analytics Data）

| 项 | 值 | 依据 |
|---|---|---|
| 覆盖 | **cov = 1.0** | 全 CHN 最优（news38 0.938 / news29 0.966） |
| 拥挤度 | **数据集 aC=7；字段级 aC 0–4** | 几乎无人挖过 |
| valueScore | **6** | 全 CHN 最高档（平台：高分数据集 prod 相关更低） |
| 字段 | 37（全 VECTOR） | 机制面厚 |
| CHN 塔位 | **CHN/D1 全 14 塔 0/3**（含 news=0） | `get_pyramid_alphas` 实测 |

**★ 为什么是 CHN**：CHN/D1 全塔 0/3 = 处女地；NEWS 塔是 14 塔里最容易点亮的一个（单数据集单塔即可点亮，见 GBR `A1VPlR3l`+`58E7jkaN` 双数据集点亮先例）；且 `mws46_*` 字段族与 GBR news17/news18 **高度同构**（relevance / ens / g_ens / ess / ssc / nip / story_count / story_index）。

## §C1 CHN 严闸与设置（比 GBR 严，必须按 CHN 口径设计）

- **CHN 严闸 LOW_SHARPE = 2.07**（不是 GBR 的 1.58）——CHN 既往候选 S1.45 即判死。
- CHN 既有死路：**robust 子宇宙墙**（宽宇宙崩）+ 情绪-关注度价差族已判死 ⇒ **不要再用 `market_news_sent` 的价差结构**。
- **CHN 死路警告（`cells.json`）**：
  - `CHN-W4-NEGRANK-NOT-MIRROR-LESSON`：**禁止「rank(x) 负 Sharpe 则 -rank(x) 得正」的镜像假设** ⇒ 反向腿必须**换结构**（换窗/换预处理/换信号），不是取负号。
  - `CHN-NEWS-SENTIMENT-COST-ARTIFACT-DEAD`：**`ts_backfill` 会破坏事件条件性、把信号换掉而非平滑** ⇒ CHN **禁 `ts_backfill`**。
  - `CHN-MARKET-NEWS-SENT-COST-DEAD`：换手 <20% 硬要求。
- 设置档（`tracking/CHN/config/settings.json`）：**CHN/TOP2000U/D1/SUBINDUSTRY/decay4/truncation0.08/VERIFY/nanHandling OFF/pasteurization ON/maxTrade OFF/FASTEXPR**。
  - ⚠ GBR 用 FAST 中性化，CHN 既有档是 SUBINDUSTRY ⇒ 首波**按 CHN 既有档**（SUBINDUSTRY），FAST 留作 A/B 变体。
- CHN 分组字段可用：`industry` / `market` / `exchange` / `country` / `currency` + 大量 `china_*_pca_component*` / `method*_cluster*`。
  ⚠ `country` 是**单一国家**（A 股）⇒ `group_neutralize(·, densify(country))` 无效；用 `densify(market)` 或 `densify(industry)`。

## §C2 ★ 十二模板池（结构互异，来源标注；正反各测由结构本身承担，不靠取负）

统一基底同 GBR，但**换掉三个 GBR 特有元素**：
① 中性化 `SUBINDUSTRY`（CHN 既有档）② 保留 `densify(market)`（A 股唯一有效 market 轴）③ `nanHandling=OFF`（CHN 档）

| # | tag | 结构轴 | SIG | 来源 | GBR 对应 |
|---|---|---|---|---|---|
| **C1** | `C1_density_reversal` | 注意力密度反转（ts_rank 反向） | `ts_mean(vec_count(mws46_story_count), 60)` | forum `43541109631895`（78 赞，Da et al. 2011 ASVI 迁移，**已提交 S1.97**）+ GBR W3/P1 | A 轴 |
| **C2** | `C2_nip_corr` | **相关性算子 × nip** | `ts_corr(vec_avg(mws46_nip), returns, 22)` | forum `40847481080087`（94 赞）+ `35294898626711`（52 赞） | 新轴 |
| **C3** | `C3_nip_cov` | **协方差算子 × nip** | `ts_covariance(vec_avg(mws46_nip), returns, 22)` | 同上 + 双字段帖 EUR 版 | 新轴 |
| **C4** | `C4_dual_sent_cov` | 双通道协方差（情绪正/负） | `ts_covariance(vec_avg(mws46_ess), vec_avg(mws46_ssc), 126)` | forum `43211291823511`（96 赞，IND/EUR/GLB/USA 四地区法） | 新轴 |
| **C5** | `C5_novelty_relevance` | 新颖度 × 相关性 **乘性置信** | `multiply(vec_avg(mws46_ens), rank(vec_avg(mws46_relevance)))` | forum `42659817284375` 套路一（**已验证**）+ GBR S1 | E 轴 |
| **C6** | `C6_story_dilution` | 注意力稀释（故事实体数作分母） | `divide(vec_avg(mws46_ssc), vec_sum(mws46_story_count))` | forum `42659817284375` 进阶 Story Attention Dilution + GBR S4 | 新轴 |
| **C7** | `C7_ens_elapsed` | **时间链年龄**（elapsed ms） | `ts_mean(vec_avg(mws46_ens_elapsed), 22)` | news48 帖 `33566303033751` + **GBR 从未测过的轴** | 新轴 |
| **C8** | `C8_story_index` | **故事链位序**（index） | `ts_mean(vec_avg(mws46_story_index), 22)` | 同上，**GBR 从未测过** | 新轴 |
| **C9** | `C9_deviation` | **实体 vs 故事 偏离**（跨层级差） | `subtract(vec_avg(mws46_ess), vec_avg(mws46_storyid_ess))` | forum `42659817284375` Entity-Story Deviation | 新轴 |
| **C10** | `C10_g_ens_global` | **全球新颖度 vs 本地新颖度** | `subtract(vec_avg(mws46_g_ens), vec_avg(mws46_ens))` | 自建（跨供应商新颖度 = 全球注意力 vs 本地） | 新轴 |
| **C11** | `C11_mce_opinion` | **社论/评论分**（观点性内容） | `vec_avg(mws46_mce)` | 自建（mce = Editorials & commentary score，观点内容的独立轴） | 新轴 |
| **C12** | `C12_nip_relevance_spread` | **冲击 × 相关性 价差** | `subtract(vec_avg(mws46_nip), vec_avg(mws46_relevance))` | forum `43211291823511` 「当前值 − 平均值」结构 | 新轴 |

**结构互异性核验**：12 条落在 12 类骨架——时序分位反向 / ts_corr / ts_covariance(信号×收益) / ts_covariance(双情绪通道) / 乘性置信 / 同单位比值 / 时间链年龄 / 链位序 / 跨层级差 / 跨源新颖度差 / 观点分水平 / 冲击-相关价差。
**无两条共用同一骨架**；字段覆盖 `mws46_*` 的 12 个不同字段。

**合规声明**：
- 窗口只用 5 / 22 / 60 / 126 / 252（C2/C3 用 22 是 forum 帖的短窗建议；C4 用 126 来自 96 赞帖 EUR 版；60/252 来自 GBR 强几何与 78 赞帖）。
- **无 `add(A,B)` 混信号、无权重常数扫描**；唯一合成是 C5 的 `multiply(x, rank(C))`（已验证的最强杠杆）与 C9/C10/C12 的 `subtract`（同量纲差）。
- **单数据集单塔**（纯 news46）⇒ 不触 trio 禁混，NEWS 属非目标塔 category。
- **禁 `ts_backfill`**（CHN 死路）。
- C2/C3 引入 `returns`（PV 塔）⇒ 这是 **PV×NEWS 的 trio×非trio 组合**，**全波合计 ≤5 条**（C2/C3 仅占 2），且**不得再引入 MODEL/OTHER 腿**。
- 正反各测：因 CHN 禁「取负镜像」，反向腿**另写结构**（换 `ts_rank`→`ts_max`、换 `ts_corr`→`ts_covariance` 等），不靠乘 −1。

## §C3 波次结构与归因口径

- 首批 12 条（2 条/批，账号并发 2 槽）。
- 归因**按模板族**（C1–C12），不按单条 alpha。
- 判读顺序：① 五闸（CHN 严闸 S≥2.07 / F≥1.0 / 2Y≥1.6 / TO 5–30% / RA failed=0）② SUB/robust 墙（CHN 特有）③ prod <0.7 ④ self <0.7。
- 任一条达 S≥2.07 ⇒ 立即扩产同轴变体（换字段不换结构）；全灭 ⇒ 换集（news38 / news50 / news11）不换结构。


---

# Part D · 跨区迁移的首批实测（CHN/news46，2026-11-03 13:1x–13:2x）

## §D1 首批 12 条（CHN/TOP2000U/D1/SUBINDUSTRY/decay4/壳 target_tvr=0.05）实测账本

| tag | alpha | S | F | TO | 逐年覆盖 | 判读 |
|---|---|---:|---:|---:|---|---|
| C1 密度反转（`vec_count(mws46_story_count)`） | `YP1vNmg6` | **0.18** | 0.05 | 5.6% | **10/10 满**（longCount 15–40） | 弱；逐年 S 有 0.84/1.40/−0.85 正负摆动 ⇒ 机制有残响、被噪声压住 |
| C2 nip×returns 相关 | `LLMGn6d9` | −0.69 | −0.40 | 6.2% | 10/10 满 | 负；**方向相反**（forum 帖在 EUR 出 PPA 是正向） |
| C3 nip×returns 协方差 | `e753n2gp` | −0.51 | −0.25 | 5.7% | 10/10 满 | 负；与 C2 同向 ⇒ 同一机制面，非独立轴 |
| C4 双情绪通道协方差 | `npvNnzYz` | −0.46 | −0.25 | **4.1%** | — | 负；**TO 低于 CHN 闸下限 5%** |
| C5 新颖度×相关性乘性（**GBR S1 全闸结构直移植**） | `MPYGbpe9` | **0.03** | 0.00 | 6.8% | — | **几乎为零** ⇒ 关键证据：问题不在几何，**在档位/壳** |
| C6 注意力稀释比值 | `npvNnge3` | −0.30 | −0.11 | 5.8% | — | 弱负 |

**逐年覆盖核验**（`get_alpha_yearly_stats` 实测，3 条全 10/10 有 pnl+longCount）：⇒ **无 leading-gap / 无连续空窗**，数据供给没问题。

## §D2 ★ 归因判决：首批全灭的根因不是「模板错」，是「设置档 + 壳」

三条硬证据：

1. **C5 = GBR 全闸结构（`multiply(ssc, rank(relevance))`）直移植，S 仅 0.03** —— 同结构在 GBR 出过 S1.85 全闸。同字段语义（`mws46_ssc` 情绪分 / `mws46_relevance` 相关性）⇒ **几何与字段都没错**。
2. **TO 全部塌到 4–7%**（GBR 同几何是 7.8–8.0%）。CHN 既有档 `decay=4` + `nanHandling=OFF` ⇒ 信号被削平；且 `ts_target_tvr_decay(target_tvr=0.05)` 的目标换手与自然换手不同量级 ⇒ 壳把信号抹掉（与记忆里「目标换手压到自然换手 1/8 ⇒ S 1.81→0.04」同型）。
3. **C2/C3 同向为负** ⇒ 两者是同一机制面（nip×returns），不算两条独立轴。

⇒ **首批不能判模板死**。按记忆铁律「只跑单档得出的低 S 不足以判死」+「FAST/SLOW 档 A/B 必须做」，立即派 **2×6 因子 A/B 波**。

## §D3 A/B 波设计（12 条，2 因子正交）

| 因子 | 取值 | 依据 |
|---|---|---|
| **设置档** | FAST+decay15（GBR 出货档） vs SUBINDUSTRY+decay4（CHN 既有档） | GBR 全闸件全在 FAST+decay15 出（S1.85/S1.93）；EUR imbalance 实证 FAST 档 S 增益可达 +0.45 |
| **壳** | 带 `ts_target_tvr_decay(target_tvr=0.05)` vs **裸几何** | C4 TO 已塌到 4.1%（低于闸下限）；记忆铁律：`target_tvr` 须与自然换手同量级，否则壳毁灭信号 |

12 条 = C1–C6 各跑 {FAST15+壳, BASE+裸} 两格 ⇒ 一次跑出「档位贡献」与「壳贡献」的可分离归因。

## §D4 ★★★ 迁移总账：哪些 GBR 模板可迁移、哪些不可

| GBR 模板 | 可迁移性 | 跨区复用条件 |
|---|---|---|
| **S1 乘性置信**（情绪 × 置信） | ★★★★★ **强几何+强字段**（C5 虽弱但结构本身被 GBR 验证两次） | 目标区需有「情绪分 + 独立置信/相关度」双字段；先跑 A/B 定档 |
| **W3/P1 密度反转**（vec_count → ts_mean60 → ts_rank252 → 反向） | ★★★★ 机制普适（Da et al. 2011 ASVI 迁移，78 赞帖已提交 S1.97） | 目标区需**事件计数类字段**（不是情绪值）；GBR L3 提示：满填充同事件字段上 `vec_count` 恒等 |
| **W4 事件强度求和**（`vec_sum(event_relevance)`） | ★★★★ | 目标区需 relevance 类字段 |
| **nip×returns 相关/协方差**（forum 94 赞） | ★★★ **强依赖区域** | EUR 出 PPA，CHN 出负 ⇒ 方向先验**不跨区**，须正反各测且不可只测一向 |
| **双通道情绪协方差**（forum 96 赞） | ★★★ | 需正负双通道字段；CHN news46 的 `ess`/`ssc` **不是**正负双通道（是事件情绪 vs 综合情绪）⇒ 语义不匹配 |
| **S4 比值 / S3 分歧 / S7 自相关 / S9 残差** | ★★ | GBR 已证弱或退化，不建议迁移 |
| **掩码类（S2）** | ★ | GBR 已证双杀（TO↑广度↓） |
| **窗口谷破钉** | ★★ | 仅在 prod 卡浅钉时作辅助手段，非独立模板 |

## §D5 三条跨区通用铁律（本次实证固化）

1. **同字段语义 ≠ 同机制**：`mws46_ssc`（综合情绪）与 `mws46_ess`（事件情绪）是**事件层 vs 实体层**两个口径，不是「正/负双通道」⇒ 移植 forum 双通道模板前必须核字段 description，不能凭名字对号。
2. **档位贡献 ≥ 结构贡献**：同结构在 GBR（FAST+decay15）S1.85、在 CHN（SUBINDUSTRY+decay4）S0.03 ⇒ **换区必先 A/B 档位，再谈结构对错**。
3. **壳必须按目标区自然换手重标定**：GBR 目标 0.05 ≈ 自然换手 8%；CHN 换手塌到 4–7% ⇒ 壳要么去掉、要么 `target_tvr` 上调。


## §D6 ★★★★★ A/B 波决定性归因（CHN/news46，档位 × 壳 2×6 因子）

| SIG | FAST15+壳 S | BASE+裸 S | ΔS | FAST TO | BASE TO |
|---|---:|---:|---:|---:|---:|
| `ts_corr(vec_avg(mws46_nip), returns, 22)` | **−1.19** | −0.71 | **−0.48** | 9.6% | 6.9% |
| `vec_count(mws46_story_count)` | **−0.74** | +0.16 | **−0.90** | 9.4% | 9.4% |

### ★ 三条结论

1. **FAST 档是「信号放大器」，不是中性化开关**：同一结构换档，|S| 放大 3–5 倍（C1 从 0.16 → −0.74），TO 从 5.6% 升到 9.4%。
   ⇒ **GBR 全闸件（S1.85/S1.93）全在 FAST+decay15 出货，而 CHN 既有档 SUBINDUSTRY+decay4 把信号压到近零**——这解释了 C5（GBR S1 结构直移植）为何只有 0.03。**换区先换档，不是先换结构。**
2. **壳（`ts_target_tvr_decay(target_tvr=0.05)`）不是主因**：C1 两格 TO 完全相同（9.4% vs 9.4%），S 差异全部来自档位。
   ⇒ 「壳抹平信号」在 CHN news46 **不成立**（与 GBR EUR 的 target_tvr 事故不同源），**别把锅全甩给壳**。
3. ★★ **方向问题不能用「取负」解决，必须换几何**：
   C1 在 FAST 档是 **−0.74**（强负），BASE 档是 **+0.16**（弱正）——**换档翻了方向**。
   CHN 明文死路 `CHN-W4-NEGRANK-NOT-MIRROR-LESSON`：负 Sharpe 的反转腿必须**重做结构**（换窗 / 换预处理 / 换信号），不是乘 −1。
   ⇒ **下一波（wave1c）用「换几何」而非「取负」**：`-ts_rank` → `ts_rank` / `ts_zscore` / `ts_max_diff` / `ts_delta` / `ts_av_diff` / 短窗 ts_rank，六种几何换面各测。

### ★ wave1c 设计（12 条，FAST15 档 + 换几何）

| tag | 换面几何 | 针对的首批负向件 |
|---|---|---|
| G1 | `ts_rank`（正号） | C1 |
| G2 | `ts_zscore` | C1 |
| G3 | `ts_max_diff`（regime 突变） | C1 |
| G4 | `ts_delta`（变化面） | C1 |
| G5 | 短窗 `ts_rank(ts_mean(·,22),66)` | C1 |
| G6 | `ts_av_diff`（GBR S10 全闸结构） | C1 |
| G7 | nip-corr → `ts_zscore` 换面 | C2/C3 |
| G8 | nip-corr → 正号 `ts_rank` | C2/C3 |
| G9 | 社论分正向 | C11（首批最正 +0.25） |
| G10 | 冲击-相关价差正向 | C12（−0.84） |
| G11 | 链位序正向 | C8（−0.76，本批最强负） |
| G12 | 时间链年龄正向 | C7（−0.37） |

**塔混核算**：wave1c 仅 G7/G8 含 `returns`（PV 腿）⇒ PV×NEWS trio×非trio 累计 **2 条**（≤5 上限内）；其余 10 条纯 news46 单塔。

## §D7 ★ 跨区同波并行策略（本轮实证可行）

CHN 与 HKG 是**不同 region、不同塔位（news 均为 0/3）、不同设置档**，可并行派发互不抢槽；CHN 内部 wave1 / wave1b / wave1c 串行为主（同区同集要归因干净）。
⇒ **跨区并行 = 跨区同时开波；同区换波 = 串行。**

## §D8 ★★★★★ A/B 波 12/12 全收齐：FAST 档是「信号放大器」（完整配对表）

| SIG | FAST15+壳 S | BASE+裸 S | ΔS（FAST 贡献） | FAST TO | BASE TO |
|---|---:|---:|---:|---:|---:|
| `vec_count(mws46_story_count)`（密度） | −0.74 | **+0.16** | **−0.90** | 9.4% | 9.4% |
| `divide(ssc, story_count)`（稀释） | **−1.03** | −0.26 | **−0.77** | 9.6% | 9.0% |
| `ts_covariance(nip, returns, 22)` | **−1.19** | −0.53 | **−0.66** | 9.5% | 6.3% |
| `multiply(ens, rank(relevance))`（**GBR S1 全闸结构**） | −0.62 | **−0.01** | **−0.61** | 11.7% | 10.0% |
| `ts_corr(nip, returns, 22)` | **−1.19** | −0.71 | −0.48 | 9.6% | 6.9% |
| `ts_covariance(ess, ssc, 126)` | −0.82 | −0.46 | −0.36 | 9.7% | 4.0% |

### ★★★ 判决（这才是跨区迁移最值钱的一条）

1. **FAST 档一致放大信号：6/6 条 ΔS 全为负且幅度 0.36–0.90**。
   ⇒ **GBR 全闸件（S1.85/S1.93）全在 FAST+decay15 出货，而 CHN 既有档 SUBINDUSTRY+decay4 把信号压到 ~0**。
   ⇒ **跨区迁移第一动作 = 换档，不是换结构**。GBR S1 结构在 CHN BASE 档是 −0.01（完全无效），FAST 档是 −0.62（信号现形）。
2. **壳不是主因**：密度一格两档 TO 完全相同（9.4% vs 9.4%），S 差 0.90 全来自档位；双情绪协方差 TO 9.7% vs 4.0% 差最大，S 差反而最小（0.36）。
   ⇒ **别把锅甩给 `target_tvr`**（与 GBR EUR 那次 target_tvr 事故不同源）。
3. ★★★ **方向是真实的：四种换面几何一致给出负暴露**

| 换面几何（均为正向、FAST15 档） | alpha | S | TO |
|---|---|---:|---:|
| `ts_rank(ts_mean(count,60),252)` | `YP1vQWwl` | **−1.24** | 9.4% |
| `ts_zscore(ts_mean(count,60),252)` | `vR1NdJx3` | **−1.17** | 10.0% |
| `ts_max_diff(ts_mean(count,22),5)` | `9qxpJpA2` | **−1.09** | 10.1% |
| `ts_delta(ts_mean(count,22),5)` | `E56GkGr9` | **−1.06** | 10.7% |

**四种几何（时序分位 / 标准化 / 极值突变 / 一阶差分）一致给出 −1.06 ~ −1.24，returns 与 margin 同为负** ⇒
**这不是成本伪影，是「新闻事件密度高 ⇒ 未来收益低」的真实负暴露**（Da, Engelberg & Gao 2011 注意力反转机制在 CHN 成立）。

⇒ **下一波 wave1d 的正确做法：在『正向几何』上取负**（`-ts_zscore(...)` / `-ts_rank(...)`），而不是在负向几何上换正——
这既满足 CHN 死路「反转型信号必须重做结构、不是取负」，又能让几何保持已验证的面。

### ⚠ CHN 严闸仍有一道墙（必须提前知道）

CHN 严闸 = **LOW_SHARPE 2.07**；而本波最强正暴露是 −1.24（取负后约 +1.2）⇒ **即便方向修对，首波也只到 S≈1.2，达不到 2.07**。
⇒ CHN news46 的出货路径必须是「**强几何 + 高强度字段组合**」，单字段单结构在 CHN 达不到严闸。下一波需在 S≈1.2 的基础上再叠一层增益（窗口/字段组合/中性化），而不是继续在同一强度上打转。

### ★ 并行策略的槽位教训（本轮实测）

三波并行（CHN AB + CHN 1C + HKG）⇒ **HKG 波被 `CONCURRENT_SIMULATION_LIMIT_EXCEEDED` 连续退避到 4/8 次**（账号只有 2 个并发槽）。
⇒ **跨区并行也受账号槽约束**，不是「不同 region 就能同时跑」。**正确做法：同一时刻只让 1–2 波在飞**，其余备好待发。
## §D9 ★★★★★★ 【重大纠偏】两极同负 = 不是方向信号，是设置在制造系统性拖累

### 正负两极配对实测（同一 SIG、同一档，只改符号）

| SIG | 正极 S | 负极 S | 判读 |
|---|---:|---:|---|
| 密度 `ts_rank` | **−1.24** | **−0.74** | ⛔ 同负 |
| 密度 `ts_zscore` | **−1.17** | **−0.76** | ⛔ 同负 |
| nip-corr（ts_rank / ts_zscore） | −0.80 / −0.88 | −1.07 | ⛔ 同负 |
| nip-cov | — | −1.28 | ⛔ 同负 |

### ★ 判决（推翻 §D6/D8 的乐观读法）

1. **六组成对全部同号且同负** ⇒ 不是「方向反了、换符号就能出货」的真信号，而是 **成本/结构伪影**（CHN 台账 `CHN-PV27` 同款判词「both-negative = cost artifact」）。
2. **真信号特征应是「两极符号相反且 |S| 接近」**（S_pos ≈ −S_neg）；两极同号 ⇒ 立即停手查设置。
3. **§D6/D8「FAST 档是放大器」需打折**：FAST 让 |S| 变大，但**变大的是系统性负漂**（6/6 条 ΔS 全负），不是可取负的真信号。
   ⇒ **铁律修正：单看 |S| 变大/变小无法区分「信号放大」与「伪影放大」，必须成对跑正负两极。**
4. **§D8「四种几何一致负暴露 ⇒ 注意力反转机制成立」作废**：正确读法是「一致负暴露 ⇒ 该几何族在 CHN 有系统性负拖累」，机制归属**未证**。

### ⇒ wave1f 单因子隔离波（12 条，逐项剥离设置）

| tag | 隔离因子 | 目的 |
|---|---|---|
| F1 | 基准复现（SUBINDUSTRY/decay4/壳/带 group） | 确认可复现（wave1 C1 = +0.18） |
| F2 | 去壳（裸几何） | 壳是否拖累源 |
| F3 | 去 `group_neutralize(market)` | 分组轴是否拖累源 |
| F4 | 去壳 + 去组 | 双重剥离 |
| F5 | decay 4→22 | decay 档是否拖累源 |
| F6 | 中性化 SUB→FAST（decay 保持 4） | **隔离 FAST 独立贡献**（此前 FAST 与 decay15 混在一起） |
| F7 | FAST + 去壳 | FAST 与壳交互 |
| F8 | 中性化 → STATISTICAL | 中性化横向对照 |
| F9 | 中性化 → SLOW | 中性化横向对照 |
| F10 | 中性化 → MARKET | 中性化横向对照 |
| F11 | 分组轴 market → industry | 换分组轴 |
| F12 | target_tvr 0.05→0.15 | 壳目标换手是否压过头 |

**判读口径**：找**能让 S 翻正且 |S| 明显大于基准**的那一格 ⇒ 该因子是拖累源，反向利用它。
若全 12 格仍全负 ⇒ news46 密度轴在 CHN 无横截面定价力（判死该轴），转 news38 / news73 / 其它区。

### 战略信息：CHN 严闸最苛刻，HKG/AMR 更容易出货

| region | S 闸 | 2Y 闸 | 来源 |
|---|---:|---:|---|
| **CHN** | **2.07** | **2.07** | `get_alpha_details` 实读 |
| HKG | 1.58 | 1.6 | `tracking/HKG/config/thresholds.json` |
| AMR | 1.58 | 1.0 | `tracking/AMR/config/thresholds.json` |
| GBR | 1.58 | 分档制 | 既有台账 |

⇒ **CHN 双线 2.07 是最苛刻目标区**；即便方向修对，S≈1.2 也过不了闸。
⇒ 迁移**出货优先级按闸线松紧排**：HKG（1.58/1.6）与 AMR（1.58/1.0）现实得多。
⇒ 三区 NEWS 塔均 **0/3**（`get_pyramid_alphas` 实测 CHN/HKG/AMR D1 news=0）⇒ 迁移价值等价，**但出货概率不同**。
## §D10 ★★★★★★ CHN 终局判定 + 跨区战略转向（2026-11-03 14:0x）

### 一、CHN/news46 判死（证据链完整）

| 证据 | 读数 | 指向 |
|---|---|---|
| 12 模板首波（BASE 档 + 壳） | S −0.84 ~ +0.25，TO 塌到 4–7% | 全弱 |
| 逐年覆盖（3 条实测） | 10/10 年有 pnl + longCount 15–40 | 数据无问题 |
| 4 种换面几何（FAST 档） | −1.06 ~ −1.44 | 看似强信号 |
| ★ 正负两极配对（6 组） | **全部同号同负** | ⛔ 非方向信号 = 伪影 |
| ★ 单因子隔离（12 格） | 分组型中性化 +0.08…+0.18；**因子型 −0.67…−0.76** | ⛔ 负漂 = 中性化族造成 |
| 最优档（SUBINDUSTRY/decay4） | **S = +0.18** | 离严闸 2.07 差一个数量级 |

**⇒ 判决：news46 密度轴在 CHN 无横截面定价力，判死。**

### 二、CHN/news38 首批（真·正负双通道）同样两极同负

| SIG | 负极 S | 正极 S | 判读 |
|---|---:|---:|---|
| 正负情绪价差 | −0.54 | −0.58 | ⛔ 同负且 |S| 几乎相等 = 纯伪影 |
| 负面情绪热度 | −0.97 | −0.67 | ⛔ 同负 |

⇒ **CHN 的两个最高质量 NEWS 集（news46 cov1.0 / news38 正负双通道）在安全档下都无方向信号。**

### 三、CHN 严闸是全平台最难（放大器效应）

| region | S 闸 | 2Y 闸 | 本轮可达性 |
|---|---:|---:|---|
| **CHN** | **2.07** | **2.07** | 实测最优 S +0.18 ⇒ 差 11 倍 |
| HKG | 1.58 | 1.6 | 概率高得多 |
| AMR | 1.58 | 1.0 | 概率最高 |
| GBR | 1.58 | 分档制 | 已挖透 |

⇒ **战略转向：CHN 的 NEWS 塔（倍率 1.7）本轮判为「结构不可达」，主力转向 HKG / AMR。**
理由：① CHN 双线 2.07 是全平台最苛刻；② 两个最高质量 NEWS 集已证无方向信号；③ CHN news 塔历史死路（market_news_sent 价差族、news_sentiment_enriched 语调族）已覆盖情绪-关注度与语调两大族；④ 连续多波 max|S| < 0.5 触发 diversity signal_floor（floor 0.5 / min_batches 2，fail-closed）。

### 四、本轮跨区迁移的净收获（虽未出货，但方法论与资产齐全）

1. **GBR NEWS 模板总结**：5 轴 + 8 教训 + 12 语义槽位（速查版 / 完整版 / 语义映射表 三份文档）；
2. **跨区迁移 SOP**：10 步流程 + 单因子隔离波设计 + 正负两极判据 + 槽位纪律；
3. **全平台 NEWS 数据集存量地图**：14 region 实拉（含 JPN/TWN/MEA 无 NEWS 数据的结论）；
4. **三个区的模板池全部预检通过**：CHN news46/news38、HKG news36、AMR news73（各 12 条，preflight `valid=true`）；
5. **三条新方法论（已入 Agent 记忆）**：中性化族隔离、正负两极判伪影、单因子隔离优先于换档 A/B。
## §D11 ★★★★★★ 双极判据：真信号 vs 伪影的对照实证（本轮最有复用价值的一张表）

同一套 GBR NEWS 模板骨架 `-ts_rank(ts_mean(SIG,60),252)` + 壳 + `group_neutralize(densify(market))`，只变 region/字段/SIG；每组跑正负两极。

| # | region / 集 | SIG | 负极 S | 正极 S | 判读 |
|---|---|---|---:|---:|---|
| 1 | CHN news46 | 密度 `vec_count(story_count)` | −0.74 | −1.24 | ⛔ 同负 |
| 2 | CHN news46 | 密度 zscore 版 | −0.76 | −1.17 | ⛔ 同负 |
| 3 | CHN news46 | nip×corr | −1.07 | −0.80 / −0.88 | ⛔ 同负 |
| 4 | CHN news38 | 正负情绪价差 | −0.54 | −0.58 | ⛔ 同负且 \|S\| 相等 = 纯伪影 |
| 5 | CHN news38 | 负面情绪热度 | −0.97 | −0.67 | ⛔ 同负 |
| 6 | **HKG news36** | **词数归一情绪** | **+0.27** | **−0.27** | ✅ **严格对称 = 真信号** |
| 7 | **HKG news36** | **正负置信价差** | **+0.15** | **−0.15** | ✅ **严格对称 = 真信号** |

### 判据（机械可执行）

- **真信号**：S_neg ≈ −S_pos，|S| 接近，符号相反。
- **伪影**：两极同号（尤其同负）⇒ 该结构**没有横截面定价力**，问题在**设置 / 成本 / 中性化**，不在方向。
- **判伪影的第二判据**：`returns` 与 `margin` 是否同号（同负 = 真实拖累；margin 负而 returns 正 = 纯成本）。

### ★ 为什么这条判据比「多跑变体」值钱

成本 = **1 条回测**就能区分「值得深化」与「该换设置」；
而 CHN 本轮若没有双极判据，会把 wave1c 的 −1.06…−1.44 当成「强信号，取负即得 +1.4」，
从而沿伪影方向烧掉 wave1d + wave1e + wave1f 三波共 36 条配额。

### ★ 两个区的问题性质完全不同

| region | 现象 | 性质 | 出路 |
|---|---|---|---|
| **CHN** | 两极同负、最优档 +0.18 | **无横截面定价力**（且闸线 2.07/2.07 最苛刻） | 换集 / 换区 |
| **HKG** | 两极严格对称（+0.27/−0.27、+0.15/−0.15） | **信号真实但强度弱** | **增益波**（换窗 / 换中性化族 / 换分母口径 / 去壳） |

⇒ 「真但弱」比「伪但强」好办得多：前者是工程问题，后者是机制问题。
## §D12 ★ 本轮跨区迁移的产出清单（2026-11-03 完整盘点）

### 交付文档（5 份）

| 文档 | 内容 |
|---|---|
| `docs/reference/gbr_news_template_summary_quickref_20261103.md` | **GBR NEWS 模板总结速查**：强几何 + 5 轴 + 8 教训 + 跨区三查 + 中性化族隔离 + 双极判据 |
| `docs/reference/gbr_news_template_summary_and_cross_region_migration_20261103.md` | **完整版**：Part A 模板总结 / Part B 迁移地图 / Part C CHN 设计 / Part D 实测归因与纠偏 |
| `docs/reference/news_template_field_semantic_map_20261103.md` | **字段语义映射表**：12 语义槽位 × 5 个区/集的字段对照 + 槽位填充优先级 + 3 个语义陷阱 |
| `docs/reference/cross_region_template_migration_sop_20261103.md` | **迁移 SOP**：10 步流程（盘点→查台账→字段画像→取证→模板池→A/B→方向判决→增益→终验→回写）+ 槽位纪律 |
| `tracking/CHN/reference/chn_news46_cross_region_campaign_20261103.md` / `tracking/HKG/reference/hkg_news36_cross_region_campaign_20261103.md` | 两个区的战役记录（含全部实测账本与判死登记） |

### 实测回测量

| 波 | 区/集 | 条数 | 状态 | 结论 |
|---|---|---:|---|---|
| wave1 | CHN news46 | 12 | 12/12 COMPLETE | 全弱（S −0.84…+0.25） |
| wave1b | CHN news46 A/B | 12 | 12/12 COMPLETE | 档位差 ≠ 放大器（伪影假象） |
| wave1c | CHN news46 换面几何 | 12 | 12/12 COMPLETE | 四几何一致负（实为中性化毒档） |
| wave1d | CHN news46 正向取负 | 12 | 12/12 COMPLETE | 两极同负 ⇒ 伪影确认 |
| wave1f | CHN news46 单因子隔离 | 12 | 12/12 COMPLETE | **毒档 = 因子型中性化** |
| wave3 | CHN news38 双通道 | 12 | 4/12 后停 | 两极同负 ⇒ 判死 |
| wave2 | HKG news36 双极 | 12 | 4/12 后停 | **四条严格对称 ⇒ 真信号** |
| wave4 | HKG news36 强度放大 | 12 | 在飞 | — |
| 待发 | AMR news73 双极 | 12 | preflight 过 | 模板池就绪 |

**合计 84 条已派发 + 12 条待发 = 96 条跨区回测**（另有 GBR 既有 10 席篮，与本目标无关）。

### 新增方法论（已入 Agent 记忆，跨区通用）

1. **中性化族隔离**：分组型（SUBINDUSTRY/MARKET/SECTOR/INDUSTRY）vs 因子型（FAST/STATISTICAL/SLOW/CROWDING/SLOW_AND_FAST）—— 后者剥离的因子暴露若与信号同源，会留下反向残差 ⇒ 系统性负漂。**源区出货设置档不可跨区照抄。**
2. **双极判据**：真信号 S_pos ≈ −S_neg；两极同号 = 伪影。成本 1 条回测即可区分「值得深化」与「该换设置」。
3. **单因子隔离优先于换档 A/B**：设置项有交互，S 差不能归因给单方；每格只动一项才能定位真毒档。
4. **正向几何读方向**：先在正向几何（ts_rank/ts_zscore/ts_max_diff/ts_delta/ts_av_diff）上读方向；负号加在已验证几何上，而非「把 `-ts_rank` 改成 `ts_rank`」。

### 区域画像增量

- **CHN**：NEWS 塔（倍率 1.7）双线严闸 2.07/2.07；因子型中性化有毒；news46/news38 均无方向信号 ⇒ 本轮判死。
- **HKG**：闸线 1.58/1.6（较松）；news36 词数归一情绪 + 正负置信价差两轴**信号真实但弱**（±0.27 / ±0.15）⇒ 走增益波。
- **AMR**：闸线 1.58/1.0（最松）；news73 双层情绪 + fear/uncertainty 新轴待测。
- **全平台 NEWS 存量地图**：USA 26 / GLB 15 / EUR 20 / ASI 22 / IND 22 / KOR 24 / HKG 24 / AMR 28 / DEU 17 / CHN 9；**JPN / TWN / MEA = 0**。
- **已被占的区**：GBR（5 轴挖透）、DEU（news 6 集已做）、KOR（news 塔 24 集全清点）⇒ 迁移不要去这三区。
## §D13 ★★★ 三区横向对比（跨区迁移的最终洞察）

| 维度 | CHN | HKG | AMR |
|---|---|---|---|
| 靶位 | news46（cov 1.0） | news36（cov 0.81） | news73（cov 0.79） |
| 数据集 aC / valueScore | 7 / **6** | 50 / 5 | 27 / 5 |
| 字段级 aC | 0–4 | 0–14 | 0–5 |
| S 闸 / 2Y 闸 | **2.07 / 2.07** | 1.58 / 1.6 | **1.58 / 1.0** |
| 塔位 | news 0/3（倍率 1.7） | news 0/3 | news 0/3 |
| 强几何下的双极结果 | **6 组全部同负**（伪影） | **2 组严格对称**（真信号） | 待测 |
| 最优档读数 | +0.18 | +0.27 / +0.15 | — |
| 问题性质 | **机制问题**（无定价力） | **工程问题**（真但弱） | 待定 |
| 单因子隔离结论 | 因子型中性化 = 毒档 | 待 wave4 验证 | — |
| 本轮判定 | **判死** | **走增益波** | **待发** |

### ★★ 三条跨区通用结论

1. **「同字段族」不等于「同可挖性」**：news46（cov 1.0、aC 7、vs 6，平台评分最高）在 CHN 完全无定价力，
   而 news36（cov 0.81、aC 50）在 HKG 挖到真信号。⇒ **数据集质量分不预测可挖性**；
   **决定性变量是「该轴在该区是否有横截面定价力」，而这只能靠双极实测。**

2. **闸线松紧决定机会成本**：CHN 双线 2.07 是全平台最苛刻。即便方向修对，S≈1.2 也过不了；
   HKG/AMR 的 1.58/1.0 才是能出货的靶子。⇒ **跨区迁移的第一筛选维度应是「目标区闸线」，而不是「数据集质量」。**

3. **同骨架的强度上限是区属性**：HKG 两条不同语义轴（词数归一情绪 / novelty 时间链）在**同一骨架同一档位**下 |S| 只有 0.27 / 0.15；
   CHN 同骨架在最优档只有 0.18。⇒ **骨架在某个区的强度天花板是区属性**；
   「换字段」在同一区内换不出量级差异（0.27 vs 0.15 差不到 2 倍），**要换量级只能换区或换档族**。

### ⇒ 对「在其它 region 的 NEWS category 挖 alpha」这个问题的直接回答

**可以做，但要按区排序、按判据推进：**

| 优先级 | region | 理由 | 本轮状态 |
|---|---|---|---|
| 1 | **AMR** | 闸线最松（1.58/1.0）+ news73 有 GBR 五轴完全没有的 fear/uncertainty/finhype 轴 + 双层结构 | 波在飞 |
| 2 | **HKG** | news36 有「词数归一分母」这个 GBR 没有的结构（情绪密度） | 增益波在飞 |
| 3 | **EUR / ASI / IND** | 闸线 1.58/1.6，但 NEWS 集饱和度不一（EUR news18 aC 11355 重饱和） | 未开 |
| 4 | CHN | 严闸 + 两集均证伪影 | 判死 |
| — | GBR / DEU / KOR | 已被占（GBR 5 轴挖透 / DEU news 6 集已做 / KOR news 塔 24 集全清点） | 避让 |
| — | JPN / TWN / MEA | 平台无 NEWS 数据集 | 不可行 |

### ★ 迁移资产（可直接复用的三件套）

1. **语义槽位表**（`news_template_field_semantic_map_20261103.md`）—— 12 槽位 × 5 个区/集；
2. **迁移 SOP**（`cross_region_template_migration_sop_20261103.md`）—— 隔离 → 双极 → 增益 的正确顺序；
3. **三个区的现成模板池**（preflight 全过，各 12 条）—— AMR news73 / HKG news36 / CHN news38，换区即用。
## §D14 ★★★ AMR 并行波实测（第三区，跨层偏离轴）

| tag | 轴 | 负极 alpha / S | 正极 alpha / S | 判读 |
|---|---|---|---|---|
| A_ent_vs_glob_pos | **实体分 vs 故事全局分（正情绪偏离）** | `JjeGOdPe` **−0.40** | `kqNP0KJO` **+0.40** | ✅ 严格对称 |
| A_fear_axis | 恐惧部分分（水平） | `O0AGZZGY` −0.02 | `3qopRRpe` +0.02 | ✅ 对称但近零 |

### ★★★ 本轮跨区迁移挖出的最强新结构：「实体层 vs 故事层」跨层偏离

- 构造：`subtract(vec_avg(nws73_entitiessent_positivepartscr), vec_avg(nws73_globalsent_positivescore))`
  （实体级正情绪部分分 − 故事级全局正情绪分）
- 读数：**±0.40 严格对称**，是本轮三个区、六个数据集里**最强**的读数。
- **GBR 五轴里完全没有这个结构** —— GBR 的 news17/news18 是**单层聚合族**（`multiple_comp_*`），没有 entity↔story 两层可比。
- ⇒ **跨区迁移的正收益不在「复制源区模板」，而在「用目标区的数据结构造源区没有的新轴」**。

### ★★ 三区强度阶梯（同一骨架、同一档位族）

| region | 集 | 最强轴 | |S| | S 闸 | 差距 |
|---|---|---|---:|---:|---:|
| CHN | news46 | 密度 | 0.18（最优档） | 2.07 | **11.5×** |
| HKG | news36 | 词数归一情绪 | 0.27 | 1.58 | **5.9×** |
| **AMR** | **news73** | **实体-故事跨层偏离** | **0.40** | 1.58 | **4.0×** |

⇒ 三区**都是「真但弱」**（双极严格对称 = 真信号），差别只在强度与闸线距离；
⇒ **AMR 是三区里最有希望到达闸线的靶子**（差距 4.0× vs CHN 11.5×），且 AMR 2Y 闸线最松（1.0）。

### ⇒ 对用户问题的直接回答

> 「GBR 的 NEWS 模板可以总结一下，在其它 region 的 NEWS 的 category 下挖掘 regular alpha 吗」

**可以，且已经在三个区跑起来了。** 但实测给出的答案是**更精确的版本**：

1. **模板要总结成「语义槽位」而不是「表达式」** —— 已产出 12 槽位映射表，跨区可直接落位。
2. **跨区迁移的第一决定项是「目标区闸线」，不是「数据集质量」** —— CHN news46 是全平台评分最高的数据集（cov 1.0 / aC 7 / vs 6）却是三区里最弱的。
3. **设置档不可跨区照抄** —— GBR 出货档 FAST+decay15 在 CHN 是毒档（因子型中性化负漂 −0.67…−0.76）。
4. **必须成对跑正负两极** —— 成本 1 条回测就能把「伪影」与「真信号」分开，避免像本轮早期那样沿伪影方向烧 24 条配额。
5. **最有价值的产出不是复制的模板，是目标区独有的新轴** —— AMR 的「实体层 vs 故事层」跨层偏离（±0.40）是 GBR 完全没有的结构。

**当前状态**：AMR wave2（双层轴增益 11 条）与 HKG wave4（强度放大 12 条）在飞；EUR news36 双极波（12 条）模板池 + preflight 已就绪。
**未达标**：三个区目前**都还没有一条过闸线的 alpha**（最强 0.40 vs 闸线 1.58）；下一波增益波若无法把强度抬到 1.0 以上，需按「机制×数据集二维律」继续换集（ASI news104 / IND news79 / EUR news29 等低拥挤集均未开）。
## §D15 ★★★ 最终三区结果总表（2026-11-03 15:0x）

| region | 集 | 回测条数 | 双极对称组数 | 最强轴 | 最强 \|S\| | S 闸 | 距闸线 | 性质 | 状态 |
|---|---|---:|---:|---|---:|---:|---:|---|---|
| CHN | news46 | **60** | 6/6 同负（伪影） | 密度 | 0.18（最优档） | 2.07 | 11.5× | 无定价力 | **判死** |
| CHN | news38 | 4 | 2/2 同负（伪影） | 正负情绪价差 | 0.58（同负） | 2.07 | — | 无定价力 | **判死** |
| HKG | news36 | 4+ | 2/2 **对称** | 词数归一情绪 | **0.64**（短窗 22/66） | 1.58 | 2.5× | 真但弱 | 增益波在飞 |
| AMR | news73 | 12 | **6/6 对称** | **不确定度** | **0.44**（长窗 60/252） | 1.58 | 3.6× | 真但弱 | 窗口阶梯波在飞 |

### ★★ 两条决定性结论

1. **双极判据在四个集上给出完全可区分的结论**（CHN 8 组全伪影 / HKG+AMR 8 组全真信号），
   ⇒ 判据本身有效，且**成本仅 1 条回测/组**。

2. **「窗口是主杠杆」在 HKG 已实测到 2.4×**（0.27 → 0.64）；
   AMR 首波用的正是长窗 60/252（uncertainty 0.44），其窗口阶梯波（wave3）已在飞，预期同样有 2× 级提升空间。
   ⇒ **AMR 若按 HKG 的短窗结论走，uncertainty 轴有望到 0.9–1.1**，逼近 AMR 闸线 1.58 / 2Y 1.0。

### ★★★ 最优执行序（本轮总结）

```
跨区迁移：
  1) 查闸线（决定目标区）→ 2) 查既有台账（避重复）→ 3) 字段画像 + 语义槽位映射
  4) 模板池 ≥10 结构互异 + preflight
  5) 单因子隔离波（找毒档：中性化族/壳/decay/分组轴）
  6) 双极波（判真伪：S_pos ≈ −S_neg ?）
  7) 窗口阶梯波（最高性价比增益：短窗 5/22 × 分位 66/126）
  8) 换轴波（目标区独有的新结构优先，如 AMR 的 entity↔story 跨层偏离）
  9) 终验四审 → 10) 回写台账 + 封存 dead_end
```

**跳过的错误序（本轮踩过）**：换档 A/B → 看到 |S| 变大 → 沿负方向取负 → 烧两波 → 最后才隔离波。

### 本轮跨区回测总量

| 类别 | 条数 |
|---|---:|
| CHN news46（wave1 + wave1b + wave1c + wave1d + wave1f） | 60 |
| CHN news38（wave3） | 4（另 8 条主动停） |
| HKG news36（wave2 + wave4） | 4 + 2（在飞 10） |
| AMR news73（wave1 + wave3） | 12 + 12（在飞） |
| **合计已派发** | **80+ 条，另有 26 条在飞/待发** |