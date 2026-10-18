# GBR 字段画像基线（Playbook 第 1 层落地快照）

> 跨区方法论主文：`docs/reference/field_profile_to_alpha_playbook.md`。
> 本文件只存 **GBR 的画像事实**（供选字段族时对照），机制/配方结论见 [`../mining_experience_by_category.md`](../../../../docs/reference/GBR/mining_experience_by_category.md)。
> 刷新：`$WQ_PY tools/fields/field_profile.py --build --region GBR`（画像随每波回归自动复利）。
> 快照时间：2026-10-08（**当日晚间修正版**）。
> ⚠ **2026-10-08 修正**：此前画像因 `harvest --persist` 未写 `backtest_results` 而**系统性失真**（写入端已修 + 回填 1253 行）。
> 修正后 **ALIVE 19 → 49、WEAK 9 → 34、DEAD 213 → 465、UNTESTED 2823 → 2578**。
> 阅读本文 §1/§2 时请以「修正后」列与 `$WQ_PY tools/fields/field_profile.py --query` 的实时输出为准。

## 0. 总览

```
GBR   1.55 万字段   285 已测   2578 未测   83 活弱(49 ALIVE + 34 WEAK)   465 判死
修正前(失真):  UNTESTED 2823 ｜ ALIVE 19 ｜ WEAK 9 ｜ DEAD 213
```

## 1. verdict 分布（按 category）

| category | UNUSABLE | UNTESTED | ALIVE | WEAK | DEAD | DEAD_STATIC | DEAD_TURNOVER | DEAD_COUNT | AXIS_ONLY |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ANALYST | 1742 | **474** | 3 | 1 | 17 | 2 | — | — | — |
| MODEL | 4071 | **1160** | **14** | 5 | 79 | 4 | 2 | — | — |
| PV | 1412 | **537** | 2 | — | 23 | — | 1 | — | 190 |
| OTHER | 1930 | **365** | — | 1 | 18 | 1 | — | — | 1200 |
| NEWS | 279 | **193** | — | — | 13 | — | 6 | — | — |
| FUNDAMENTAL | 1158 | **48** | — | — | 14 | 18 | — | — | — |
| INSTITUTIONS | 37 | **13** | — | 2 | 5 | 6 | — | 3 | — |
| SHORTINTEREST | — | **19** | — | — | 6 | — | — | — | — |
| SENTIMENT | 258 | **8** | — | — | 10 | — | — | — | — |
| RISK | 34 | **6** | — | — | — | — | — | — | — |
| EARNINGS / INSIDERS / MACRO / IMBALANCE / SOCIALMEDIA | — | — | — | — | 有 DEAD | — | — | — | — |

**读法**：`ALIVE` 集中在 MODEL（14）—— 而 MODEL 已点亮（本季度 4 颗）⇒ **按锁定项不作主数据集**。非 MODEL 的产出入口只有 **ANALYST（`analyst47`）/ PV（`pv47`）/ INSTITUTIONS（`fund_holdings_panel`）/ OTHER（`other335`）**，其余 category 只能走 `UNTESTED` 探针。

## 2. ALIVE 字段（19，单信号 S ≥ 1.58）

| dataset | field | type | cov | n | to_med | S_sg | 2Y_sg | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| model38 | region_relative_valuation_rank | MATRIX | 0.00 | 5 | 0.053 | **2.44** | 1.87 | 1.25 |
| model38 | star_val_region_rank | MATRIX | 0.00 | 1 | 0.123 | 2.37 | 2.06 | 1.19 |
| model38 | star_val_sector_rank | MATRIX | 0.00 | 1 | 0.129 | 2.31 | 1.93 | 1.13 |
| **analyst_earnings_ibes** | **five_day_total_return_dlr2** | MATRIX | **1.00** | **94** | 0.111 | **2.07** | **2.31** | 1.05 |
| predictive_starmine | ep_yield_pct_smest_fy2_3 | MATRIX | 0.94 | 11 | 0.158 | 2.02 | 1.51 | — |
| model38 | star_val_industry_rank | MATRIX | 0.00 | 2 | 0.129 | 2.01 | 2.00 | 0.99 |
| model38 | star_val_dividend_yield | MATRIX | 0.00 | 1 | 0.111 | 1.97 | 2.10 | — |
| **analyst47** | **anl47_rawsentiment** | MATRIX | 0.64 | **29** | 0.168 | **1.95** | **1.75** | **1.30** |
| predictive_starmine | forward_pe_mean_f12m_4 | MATRIX | 0.93 | 2 | 0.125 | 1.94 | 1.17 | 0.95 |
| predictive_starmine | mean_estimate_price_ratio_f12m_earnings_5 | MATRIX | 0.93 | 2 | 0.125 | 1.94 | 1.17 | 0.95 |
| model25 | value_momentum_industry_percentile | MATRIX | 1.00 | 1 | 0.054 | 1.91 | 1.36 | 0.82 |
| predictive_starmine | ep_yield_pct_smest_f12m | MATRIX | 0.94 | 46 | 0.130 | 1.88 | 1.89 | 1.23 |
| model38 | ev_ebitda_relative_score | MATRIX | 0.00 | 4 | — | 1.87 | 2.08 | 0.98 |
| **analyst47** | **anl47_indicator** | MATRIX | 1.00 | 4 | 0.214 | 1.78 | 1.41 | 1.07 |
| **analyst47** | **anl47_totalrawsignal** | MATRIX | 0.64 | 4 | 0.203 | 1.74 | 1.63 | 1.28 |
| **pv47** | **pv47_spret** | MATRIX | 0.00 | 16 | 0.147 | **1.69** | **2.07** | 1.20 |
| predictive_starmine | ep_yield_pct_smest_fy1_3 | MATRIX | 0.94 | 14 | 0.126 | 1.68 | 1.89 | 0.81 |
| model53 | annualized_pd_2_year_jc7 | MATRIX | 0.80 | 41 | 0.108 | 1.62 | 2.04 | 1.16 |
| **pv47** | **pv47_for_statssimple_only_spret** | MATRIX | 0.00 | 2 | 0.101 | 1.62 | 1.89 | — |

**⚠ 两处需复核**：① `model38` / `pv47` 的 `cov=0.00` 与高 S 并存 —— 覆盖率列疑似口径差异（真覆盖须以平台 `get_datafields` 复核，不要据 0.00 直接剔除）；② `predictive_starmine` 属 profile 写明的 **PROD 饱和族**（「starmine 四向」不生成新变体）⇒ 只作对照，不作首选。

## 3. WEAK 字段（9，1.10 ≤ S < 1.58）

| dataset | field | type | cov | n | to_med | S_sg | 2Y_sg |
|---|---|---|---:|---:|---:|---:|---:|
| model38 | star_val_ev_sales | MATRIX | 0.00 | 1 | 0.114 | 1.54 | 1.00 |
| predictive_starmine | eq_vr_dlra2_score | MATRIX | 0.67 | 2 | 0.037 | 1.51 | 1.70 |
| model250 | mdl250_maltahc_eq_score | MATRIX | 0.49 | 6 | 0.102 | 1.41 | 1.22 |
| analyst47 | anl47_rawalphadecay | MATRIX | 0.64 | 7 | 0.172 | 1.39 | 0.17 |
| model53 | annualized_pd_1_year_jc7 | MATRIX | 0.80 | 5 | 0.144 | 1.36 | 1.86 |
| **fund_holdings_panel** | **boundary_transaction_total** | **VECTOR** | 0.93 | 1 | 0.528 | 1.26 | 1.38 |
| **fund_holdings_panel** | **stable_boundary_trade_count_21d** | **VECTOR** | 0.93 | 2 | 0.539 | 1.24 | 1.49 |
| model53 | annualized_pd_3_year_jc7 | MATRIX | 0.80 | 3 | 0.084 | 1.16 | 1.26 |
| other335 | oth335_combined_all_region_mind | MATRIX | 0.00 | 5 | 0.116 | 1.13 | 0.96 |

**注**：`fund_holdings_panel` 两条是 **VECTOR** ⇒ 必须 `vec_*` 聚合（`vec_avg` 等），且 `to_med` 高达 0.53 —— 逼近 GBR `turnover_max 0.3` 的评审线（平台线 0.70），**开批前先降换手**。

## 4. 本区战役目标（按产出概率排序）

| 优先 | category / 数据集 | 依据 | 距点亮 |
|---|---|---|---|
| **1** | **ANALYST**（`analyst47` raw sentiment 族 + 474 UNTESTED） | 塔 **2/3**，`anl47_rawsentiment` ALIVE S1.95/2Y1.75/sub1.30；已有 `wpbJ2gm2` F 差 0.04 | **差 1 颗** |
| **2** | **PV**（`pv47`，537 UNTESTED + 190 AXIS_ONLY） | `pv47_spret` ALIVE S1.69/**2Y2.07**；PV 塔 0/3 | 差 3 |
| **3** | **INSTITUTIONS**（`fund_holdings_panel` + 13 UNTESTED） | 2 WEAK（VECTOR），塔 0/3；需先降换手 | 差 3 |
| 4 | **NEWS**（193 UNTESTED） | 池最大但 6 条 DEAD_TURNOVER 警告换手结构性偏高 | 差 3 |
| 5 | **OTHER**（`other335` + 365 UNTESTED / 1200 AXIS_ONLY） | 仅 1 WEAK（S1.13） | 差 3 |
| — | ~~MODEL~~ | **已点亮（4 颗）⇒ 锁定项不作主数据集**，仅可作复合从腿 | — |

## 5. 纪律（与主文一致）

1. **改持仓才是真降 prod**：换残差轴 / 字段 / 概念 / `trade_when` 分层；只改时序（`hump` / `decay` / 慢化 `ts_mean`）会**爆 self**。
2. **一条腿只产 1 颗**：同族提交一颗后，同持仓变体 prod/self 会被推爆（`gJZQZkZe` → `rKe5L9q3` 0.6737→0.9933）。
3. **框架与机制耦合，不可跨机制外推**：同框架对 estimate 族 +0.31、对 anl93 族 −0.38。
4. **画像只是「存在性证明」，不是「可复现证明」**：命中后必须本框架实测。
5. **高 S 陷阱**：`*_label*` / `*_bucket*` / `dl_riskfree_returns` 类分位桶标签不是信号，开批前核 `description`。


## 6. ★ 算子对账必须单列 `genius` 子集（2026-10-08 新增）

判「方向 / 算子穷尽」时，只对 `get_operators` 做差集**不够** —— API 的 `category` 只有 9 类（无 Genius），
`level` 字段恒为 `ALL`/`None`，**不暴露平台 UI 的 `base`/`genius` 分级**。

**权威表**：`docs/reference/operators_notes.md`（Category / Definition / Count / Scope / **Level**）。
**genius 级共 17 个**：`pasteurize`｜`ts_returns`｜`ts_kurtosis`｜`ts_ir`｜`ts_max_diff`｜
`ts_target_tvr_decay`｜`ts_target_tvr_hump`｜`vec_min`｜`vec_max`｜`vec_stddev`｜`vec_range`｜`vec_count`｜
`tail`｜`group_count`｜`group_std_dev`｜`group_sum`｜`group_cartesian_product`。

**★ VECTOR 聚合有 7 种**（`vec_min/max/stddev/range/count/avg/sum`）—— **勿只用 `vec_avg`/`vec_sum`**。

**GBR 实测（2026-10-08）**：唯一产出的 genius 算子是 **`ts_target_tvr_hump`**
（新候选 S1.62/F1.03/2Y1.89，`Failed RA=0`）；`vec_*` 另 5 种、`group_std_dev/count/sum`、`pasteurize`
在本区已试家族上均无产出；`group_cartesian_product` 语法可用但劣于 `sector`；
`tail` 语义为「区间内置 newval」⇒ 销毁信息，判为非合理尝试。


## 7. ★ 判字段以 `description` 为准，名字只是线索（2026-10-08 新增）

**用户指正**：「判断字段时通过读 description 而不是光看字段名」。据此审计发现 **`field_profile.py` 里 `DEAD_COUNT`
是唯一的名字驱动规则**，且它有三类错误（均已在 2026-10-08 修正为**纯 description 驱动**）：

| 类型 | 实例 |
|---|---|
| 名字误匹配 | `count` 无词边界 ⇒ 命中 `**count**ry_percentile_*`（实为 Percentile）、`**accounts**_receivable_turnover_ratio`（实为 ratio） |
| 语义混淆 | `*_surprisenum` 描述 "Number of **estimates used for** surprise calculation" = **参与家数/覆盖度**，非方向性修正家数 |
| 漏杀 | `oth47_organic_keywords` 描述 "**Count of** unique keywords … unit: count"，名字无 count/num 而逃过 |
| 反例 | `mdl307_sales_pct_gb` 描述含 "expressed as a **number**" 但实为 **Fraction（比例）** |

**纪律**：
1. 类型/机制归类**必须读 `description`**；名字正则只用于**缩小候选**，不得单独作判死依据。
2. **关键词出现 ≠ 语义成立**：描述里的 `number` 可能指「数值范围」。
3. **反向也要查**：名字不像但描述是（`*_keywords` = "Count of…"）⇒ 会漏杀。
4. **正向价值**（用 description 扫未测池的直接产出）：`news17.analyst_recommendation_change_score`
   （实为**分析师评级变动分**，非新闻情绪）、`news104.nws104_prob_*`（情绪三分类概率）、
   `analyst7.est_12m_bps_*_4wks_ago/_3mth_ago`（**vintage 快照** ⇒ 可做长周期修正）、
   `institutions6.aggregate_equity_value_all_owners` —— 这四类**从名字上完全看不出来**。


## 8. 语义类型层：`tools/fields/field_semantic_type.py`（2026-10-08 新增）

**两层分工**：`field_profile.py` 判「**强不强**」（verdict，S 驱动）；本工具判「**是什么量**」（sem_type，**description 驱动**）。
**骨架选择完全取决于后者** ⇒ 两层必须交叉使用。

```bash
$WQ_PY tools/fields/field_semantic_type.py --build  --region GBR      # 建表 field_semantic_type
$WQ_PY tools/fields/field_semantic_type.py --report --region GBR      # 语义 × category 报告
```

**19 类语义**（5 类非信号）：`count`｜`ratio`｜`level_amount`｜`percentile`｜`probability`｜`score`｜
`revision_change`｜`sentiment`｜`estimate_level`｜`dispersion`｜`indicator_name`｜`direction`｜`correlation`｜
`novelty_time`｜`unknown`（须人工读描述）‖ **非信号**：`cluster_label`（只作轴）｜`identifier`｜`temporal_meta`｜`text`（禁用）。

**GBR 实测结论**：
- 15,522 字段中**名字与 description 语义冲突 = 1,470（9.5%）**；
- **83 个活/弱字段只落在 10 类语义上，前三类（`count`19 / `ratio`10 / `level_amount`14）占 62%**；
- **能出东西的量类型收敛为：计数型 / 比率型 / 水平型**；
- 未测池里 **PV `score` 329 个**（形态相似度分）是本区最大未被系统开采的语义块；
  **FUNDAMENTAL/OTHER 以 `unknown` 为主（587/1375，领域专有复合量）** ⇒ 必须先解决「读描述定骨架」；
- **非信号 754 个**（cluster 322 / identifier 255 / temporal 148 / text 29）应从候选池硬排除。

**规则设计的三个坑（我实际踩过，务必避免）**：
1. 不能按**固定规则优先级**：应按「description 中**最靠前的主量词**」（"Number of … per share" 主量是家数）；
2. **复合名词**要单独处理："price-to-revenue **ratio**" 的主量词在**词尾**，`price` 会抢先误判；
3. 泛化词要收紧（`expected` ⇒ `expect(ed)?\s+(annual|forward|fiscal|\d)`，否则 "Expected annualized percent change" 被判估计水平）。


## 9. ★★★★ 硬纪律：已测字段的命中率**不能**预测未测字段（2026-10-08 实测确立）

**同日内两次栽在同一坑，固化为此纪律**：
- §十二 被 **`score` 的未测数量**（533 个）误导 ⇒ 建议扫 score ⇒ 实测命中率仅 1.3%；
- §十四 被 **`count` 的已测命中率**（10.6%）误导 ⇒ 建议优先 count ⇒ 实测未测 count 中位 S 仅 **0.08**。

**根因**：**已测集合不是随机样本** —— 字段是历史上被**刻意挑选**（如已看到信号迹象）才去测的，
因此「已测字段的命中率」同时包含「语义能力」与「挑选偏差」，**外推到未测池必然失效**。

> **⇒ 要估计未测池的产出率，唯一可靠做法 = 直接测未测字段（配匹配骨架）** —— 即「语义抽样扫测」。

### 语义抽样扫测（新区域第 0 步，建议固化）

```bash
$WQ_PY <repo 外>/wqb-scripts/semtype_scan.py gen --region <R> --per-type 4   # 生成波文件+manifest
$WQ_PY <repo 外>/wqb-scripts/semtype_scan.py run --region <R> --waves 1-N   # 逐波派发+收割
```
- 每类取 **UNTESTED** 字段（非 MODEL 优先、类内按 coverage 降序、每数据集至多 1 个）；
- 套该 sem_type 的**匹配骨架**（见 §7/§8 的 `SKELETON_HINT`）；8 条一波；
- `manifest.json` 保留 `expr → (sem_type, field)` 映射，供事后归因。

### GBR 实测结论（62 条 / 8 波 / 17 类，2026-10-08）

| 判读 | sem_type | 中位 S |
|---|---|---|
| **有效语义（有序号语义）** | **`ratio` 0.50 > `percentile` 0.23 > `revision_change` 0.11 > `estimate_level` 0.10 > `count` 0.08 > `sentiment` 0.05** | — |
| **spurious（无序号语义，分数无意义）** | `identifier` 0.65 ｜ `text` 0.45 ｜ `cluster_label` 0.30 ｜ `temporal_meta` 0.06 | — |
| **反效** | `dispersion` −0.41 ｜ `probability` −0.51 ｜ `level_amount` −0.59 | — |

**62 条中 S≥1.58 = 0**。⇒ 用 8 波（而非盲挖的 ≈322 波）证明了「GBR 非 MODEL 未测池不值得挖」。

**★ 附带的判读纪律**：`identifier`/`text`/`cluster_label`/`temporal_meta` 的高 S 是 **spurious**
（对 ISO 国家代码按字母序 rank、对 cluster id 按数字序 rank ⇒ 排序无经济含义）。
**判定「能不能当信号」必须靠 description 判断它是否有 ordinal 语义** —— 这是「读 description」纪律的又一个落点。


## 10. ★★★★ 硬纪律：判据只允许建立在「字段本质」之上（2026-10-09）

**代理量（coverage / turnover / 字段名正则）只能作线索或降权，不得单独作判死依据。** 同日已踩三次同类坑：

| # | 判据 | 错在哪 | 铁证 | 处置 |
|---|---|---|---|---|
| 1 | `DEAD_COUNT`：字段名正则 | 名字会骗人 | `country`/`accounts` 误匹配；`*_surprisenum` 语义实为覆盖度 | ✅ 改为 description 驱动 |
| 2 | `DEAD_TURNOVER`：`to_med > 0.70` | **换手是骨架属性**（`ts_decay_linear`/`ts_target_tvr_decay` 可压低），且该判据下 7 个字段 `n_tests` 全为 1 | — | ⏳ **待修**（建议降级为提示） |
| 3 | **`UNUSABLE`：`coverage < 0.6`** | **coverage 是 `区域×universe×delay` 属性**；且 `cov == 0.00` 实为**未采集** | ★ **`model38` 全部字段 cov=0.0，其中 9 个 ALIVE（S1.87–2.44）、另 57 个仅因同一个 0.0 被判 UNUSABLE**；`pv47` cov=0.0 而 2 字段全 ALIVE；真低覆盖的 `model28` 族 cov 0.5837–0.5862 出 **4 个 ALIVE（S1.77–1.94）** | ✅ **已修**：`cov==0/None → UNKNOWN_COVERAGE`（回平台复核） |

### 修正效果（GBR 15,522）

```
修正前：UNUSABLE 10,967（70.7%）｜UNTESTED 2,578
修正后：UNUSABLE  3,409（22.0%）｜UNKNOWN_COVERAGE 7,558（48.7%）｜UNTESTED 2,508
⇒ 可探池上限 2,578 → 10,066（+290%）
```

**★ 附带纪律**：**低覆盖由平台的 `LOW_SUB_UNIVERSE_SHARPE` 闸判**，不应在字段画像层预判死亡。


## 11. ★★★ 骨架多样性（2026-10-09 用户明令，v2 已审）

**纪律**：**字段画像决定骨架** —— 不同 sem_type/field_type 的字段必须配不同骨架族；禁止一套 house 骨架打所有字段。

**工具**：`tools/fields/skeleton_panel.py`
- `list`：12 族骨架面板与语义映射；
- `gap-report --region R`：每字段「应配（SEM_PREFERRED）→ 已见（skeleton_fams 列）→ 缺口」；
- `gen`：按字段画像生成多族初筛波（count 自动配对对偶字段差）；
- `audit`：发批第 7 闸，**两级** —— 波级（模板 ≥3 族、单模板 ≤60%）+ 字段级（`--region`，每字段 ≥2 族）；
  深挖/参数扫用 `--param-sweep` 显式豁免。

**SEM_PREFERRED v2（实测校准，证据见 GBR_skeleton_mapping_review_20261009.md）**：
```
count           → subtract_pair（对偶差 1.96）→ quantile → gn_first → decay_linear
ratio           → delta（2.15）→ av_diff（2.02）→ quantile → level_rank
percentile      → delta（2.61）→ gn_first → double_window → gate → level_rank
estimate_level  → delta（1.90）→ ts_rank（1.79）→ level_rank
probability     → delta（1.80）→ level_rank → av_diff
score           → level_rank（1.61 唯一 ALIVE 族）→ ts_rank → quantile（待证）
level_amount    → delta（1.78）→ level_rank ｜ ⚠ ts_zscore 实测 0.65 弱，降为对照
sentiment       → quantile（1.75 唯一 ALIVE 族）→ level_rank
revision_change → level_rank → decay_linear（1.50）→ ts_rank
dispersion      → delta → divide（全族低置信待证）
unknown         → level_rank → delta → decay_linear → gate（2.07）
```
**反模式（实测推翻，勿再用）**：ts_rank/ts_zscore 对 ratio/level_amount/sentiment 当首选（实测 0.3~0.9 弱）；
`count` 只用单字段 level_rank（1.36）而丢对偶差（1.96）。

**画像列**：`field_profile_perf.n_skeletons` / `skeleton_fams`（Phase 0 已建）；
`n_skeletons==1` 的 DEAD = 低置信，进复活候选池，禁当终局结论。

  **v3 回归结论（2026-10-09，3a 复活补测 89 条）**：v2 映射在合并新数据后**全部站住**；
  GBR WEAK 池复活率仅 **2.1%**（1/47，ΔS 中位 −0.88）⇒ **「单骨架判死=假死」在 GBR 不成立，
  原骨架通常已是该字段最强形态**；DEAD 池大规模复活（3b/3d）已取消（期望更低）。
  骨架多样性的价值在「**置信度分级 + 排除嫌疑**」，不在「大量复活」。
