# S0 塔位与数据集盘点 — DEU / TOP500 / D1（2026-11-16，修订 v2）

> 范围：region=DEU，universe=TOP500，delay=1，regular（无 ATOM 放松）。
> 本档零提交、零配额消耗；塔位与 alpha 读数为**平台实读**，历史臂数为**本地只读 SQL 读数**，
> 「未测」逐条标注通道与盲区（§11）。**v2 修订说明见 §14**（v1 的 5 处错误已更正，另列出未采信的复核条目）。

---

## §0 结论摘要（v2）

| 项 | 结论 |
|---|---|
| **目标塔** | **insiders**（差 2 颗，×1.6，1/3） |
| **配对塔** | **institutions**（差 2 颗，×1.6，1/3） |
| 主数据集 | `insiders1`（Global Insider Trading Data，8 字段，字段级 cov 0.5343） |
| 配对数据集 | `institutions6`（11 字段全 MATRIX，字段级 cov **1.0**） |
| **收割池（v2 更正）** | **非空**：`XgaGb3J1`（主）+ `0mPKr3bq`（备），两者均为 **[INSIDERS,MODEL] effective=2**、RA 全过、self 实测 PASS（0.6784 / 0.6714）、未提交 ⇒ **零仿真可把 insiders 1/3→2/3** |
| 开波时序 | ① 收割件（若 prod<0.70）→ insiders 2/3；② 新双塔件 → insiders **3/3 点亮** + institutions 1/3→2/3 |
| 偏离倍率次序 | 有。sentiment（×1.8）自相关锁死 + 主可用面被自己占满（§2.3） |

**v1 的两条硬错误（已更正）**：
1. v1 断言"第一格增量必须由新件产出，不能靠零配额收割"——**错**。v1 的池分类器把 `predicted_surprise_*` /
   `mean_estimate_change_*` 误判为 analyst（实际是 MODEL），导致漏掉 40 条 `[INSIDERS,MODEL]` 臂；
   补测后 `XgaGb3J1` self **0.6784 PASS**、`0mPKr3bq` self **0.6714 PASS**，零配额收割成立。
2. v1 把 `insider_agg_matrix` 整集排除——**错**。该集的 `significant_value_1..4` 与 `directional_indicator`
   正是上述 38 条全闸臂的核心腿，且 `directional_indicator` 被 ACTIVE 件 `Vk65zLzG` 使用（LC/SC 112/102）。

---

## §1 塔位实读（权威口径 = 平台 `get_pyramid_alphas` 当季）

**实读命令**：`mcp__wq-brain-http__get_pyramid_alphas()`（无参数 = 当前季度；返回体按 `region → delay → category` 分档）。

DEU **D1** 档实读（D0 档全 0，非本战役口径）：

| category | alphas | need(=3−alphas) | 是否点亮 |
|---|---:|---:|---|
| analyst | 6 | 0 | ✅ |
| shortinterest | 5 | 0 | ✅ |
| fundamental | 3 | 0 | ✅ |
| model | 3 | 0 | ✅ |
| other | 3 | 0 | ✅ |
| **sentiment** | **1** | **2** | ❌ |
| **insiders** | **1** | **2** | ❌ |
| **institutions** | **1** | **2** | ❌ |
| news / option / pv / earnings / macro / risk / socialmedia / imbalance | 0 | 3 | ❌ |

**与 ask 给定 CLI 表（`campaign_intel.py pyramid`）的差异**：**逐项一致，无差异**（16 类 alphas 值全等）。
故本档采用 MCP 读数，无需以 MCP 覆盖 CLI。

**抑制项**：`fundamental` 已 `lit=true`（3 颗），不再作目标塔——这与
`tracking/DEU/regular_tower/CAMPAIGN_REPORT_20261116.md` §1（当时记 fundamental 2 颗）相比已前进一格，该报告的优先级判断本轮失效。

**delay 归一口径**：只取 `DEU.D1`，不跨 delay 求和（历史盲区：`pull_pyramid()` 形态 B 曾跨 delay 求和，把 D1 点亮状态套到 D0）。

**★ 时效**：当季计数按自然季清零（`docs/time_bombs.json` TB-05 已登记）。本档全部 1/3→3/3 的推论**只在 2026Q4 成立**；
跨到 2027Q1 开波须按 need=3 重算。

---

## §2 目标塔选定与理由

### 2.1 排序依据（ask 给定）：need 升序 → 倍率 → 可挖面宽窄

三座未亮塔 need 全部 = 2（**不存在"差 1 颗即点亮"的塔**），第一键打平：

| 塔 | need | mult | 候选面 | 实测结论 |
|---|---:|---:|---|---|
| sentiment | 2 | **1.8** | 3 集 / 276 字段 | 主可用面（snt7×snl27）**被自己的 ACTIVE 件占满**，§2.3 |
| **insiders** | 2 | 1.6 | 2 集 / 42 字段 | **有 2 条零配额全闸收割件**（§9）+ 38 条 2 塔全闸臂 |
| **institutions** | 2 | 1.6 | 5 集 / 66 字段 | institutions6 腿有 6 条 |S|≥1.58 臂、字段级 cov=1.0，但塔归属用法未验证（§5.4） |

### 2.2 选定：insiders（主）+ institutions（配对）

1. **insiders 是唯一"零配额即可推进"的未亮塔**：`XgaGb3J1` / `0mPKr3bq` 均
   `pyramids.list = [DEU/D1/INSIDERS, DEU/D1/MODEL]`、`effective=2`、`failed_ra_count=0`、
   `status=UNSUBMITTED`、self 实测 PASS（§9.2），且 2014–2023 **十年逐年 pnl>0**（§9.3）。
2. **insiders + institutions 能一次推进两座未亮塔**：两塔都在 need=2，且两塔都不在 trio（PV/MODEL/OTHER）内
   ⇒ 不触禁混条款 ①②、也不触"≥3 塔归 0"。
3. **映射有平台实读支撑**（`get_alpha_details` 逐件，非推断）：
   `d5a2aO7v`=`[SHORTINTEREST,INSIDERS]` eff2；`d5a2K72E`=`[SHORTINTEREST,INSIDERS]` eff2；
   `Vk65zLzG`=`[INSIDERS,MODEL]` eff2；`XgaGb3J1`=`[INSIDERS,MODEL]` eff2；`0mPKr3bq`=`[INSIDERS,MODEL]` eff2；
   `1YWnZ9rK`=`[PV,INSIDERS,MODEL]` **eff0**；`vRA82ogA`=`[INSTITUTIONS,INSIDERS,ANALYST]` **eff0**；
   `E56AzejK`=`[INSTITUTIONS,OTHER]` eff2；`bl6OWZ2M`=`[SENTIMENT]` eff1。
   ⇒ `insd1_*`/`significant_value_*`/`directional_indicator` → INSIDERS；`count_institutional_*` → INSTITUTIONS；
     `predicted_surprise_*`/`mean_estimate_change_*` → **MODEL**（不是 analyst）；`cap` → **PV**（三塔陷阱）。
4. **insd1 腿不是瓶颈**：`XgaGb3J1` S 2.36 / 2Y 2.71 / sub 1.51；`1YWnZ9rK` S 2.64（3 塔不可派）。
   瓶颈在"配第二腿且不把塔数顶到 3"。

### 2.3 为什么不是 sentiment（倍率更高）

1. **主可用面只有一条结构**：类别参考 `Claude/skills/wq-brain-ra-deu/references/sentiment.md:84`
   "可用面仅 `sentiment27` 的 18 个（`snl27_*`，全 VECTOR）"；`DEU-SENTIMENT27-ATOM-DEAD` 的 rule
   "DEU 的 SENTIMENT 类唯一有效构造是 sentiment7×sentiment27 的 vector_neut 跨集正交"。
2. **那条结构已被 ACTIVE 占位**：`bl6OWZ2M`（`DEU_R_alpha_01`，ACTIVE 2026-11-04）S 2.03/F 1.61/2Y 2.54/sub 1.20，
   `pyramids=[DEU/D1/SENTIMENT]` eff1 —— 它就是 sentiment 塔的"1"。
3. **剩余最强者被 self 锁死**：`GrWVx2aO`（S 2.07/F 1.89/2Y 2.55/sub 1.29，prod 未测）
   self 实测 **0.8419 vs bl6OWZ2M → FAIL**；28 条 sentiment-only 池中 **27 条**同时引用 `snt7_*` 与 `snl27_*`。
4. **唯一"处女面"是弱面**：`sentiment33` 本地 118 条臂 max|S|=1.06；`sentiment7` 脉冲独立判死（48 探针天花板 0.71）。

⇒ sentiment 需要"全新结构"（当前零候选），insiders 已有"零配额可收割 + 38 条全闸臂"。
按 ask 的 ★收割优先于重挖 + 第三键"可挖面宽窄"应按**有证据的活面**衡量，本档取 insiders。

---

## §3 数据集分母（唯一合法来源 = 平台 `/data-sets`，按 region/universe/delay 实取）

**实取命令（逐字）**：
```
mcp__wq-brain-http__get_datasets(category="insiders",    region="DEU", delay=1, universe="TOP500")
mcp__wq-brain-http__get_datasets(category="institutions",region="DEU", delay=1, universe="TOP500")
mcp__wq-brain-http__get_datasets(category="sentiment",   region="DEU", delay=1, universe="TOP500")
```

### 3.1 insiders 塔分母 = **2 集**

| dataset | name | coverage(集级) | fieldCount | userCount | alphaCount |
|---|---|---:|---:|---:|---:|
| insider_agg_matrix | Smart Insider Transaction Aggregates | 0.5617 | 34 | 103 | 196 |
| **insiders1** | Global Insider Trading Data | 0.5343 | 8 | 22 | 35 |

`insider_agg_matrix` 逐字段实取（`count=34 / platform_count=34 / complete=true`，
`get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="insider_agg_matrix", filter_sharpe=true)`）：
- **`directional_indicator` cov=1.0**（alphaCount 52）、**`directional_indicator_2` cov=1.0**（alphaCount 23）
- `significant_value_1..4` / `top_significant_value_1..4` / `directional_significant_value_1..4` / `top_directional_significant_value_1..4`：cov 0.5342
- 8 个 `avg_*_shares` + 8 个 `total_*_shares`：cov 0.5344
⇒ **该集不是"无数据/零持仓"**，它有 2 个满覆盖字段与 26 个半覆盖字段。

`insiders1` 逐字段实取（`count=8 / platform_count=8 / complete=true`）：`insd1_gvkey`(ID)、
`insd1_holdings`、`insd1_price`、`insd1_shares`、`insd1_tradesignificance`、`insd1_value`、`insd1_valueeur`、
`transaction_currency_code`(ID)；字段级 cov 全 = 0.5343。⇒ 6 个可用数值字段。

### 3.2 institutions 塔分母 = **5 集**

| dataset | name | coverage(集级) | fieldCount | userCount | alphaCount |
|---|---|---:|---:|---:|---:|
| fund_holdings_panel | Global Institutional Fund Holdings | 0.9019 | 18 | 69 | 125 |
| institutions1 | Insider Trading for Europe | 0.2289 | 7 | 23 | 34 |
| institutions25 | Fund Short Selling Data | **0.0** | 24 | 7 | 11 |
| institutions4 | Institutional Ownership Data | 0.3413 | 6 | 14 | 20 |
| **institutions6** | Institutions and Beneficial Stake Ownership | **1.0** | 11 | 140 | 294 |

`institutions6` 逐字段实取（`count=11 / platform_count=11 / complete=true`）：11 个 **MATRIX**，
**字段级 coverage 全 = 1.0**：`aggregate_equity_value_{all_owners,institutions}`、
`aggregate_share_count_{all_owners,institutions}`、`count_institutional_{buyers,holders,sellers}_security`、
`market_value_institutional_shares_{acquired,disposed}`、`quantity_institutional_shares_{acquired,disposed}`。
⚠ **只有 `count_institutional_buyers_security` 有平台塔归属实读**（`vRA82ogA` → INSTITUTIONS），其余 10 个未验（§5.4）。

### 3.3 sentiment 塔分母 = **3 集**（非本波目标，备查）

| dataset | coverage(集级) | fieldCount | 实测 |
|---|---:|---:|---|
| sentiment27 | 0.9038 | 18 | 14 个可用信号字段（全 VECTOR），字段级 cov 0.9022–0.9118 |
| sentiment33 | 0.3221 | 255 | 字段级 cov 0.3152–0.3258（全 255 个非零 ⇒ 数据存在，只是窄） |
| sentiment7 | 0.7418 | 3 | 脉冲面独立判死 0.71 |

---

## §4 逐集采用/排除理由（判死标记**均不单独作依据**）

### 4.1 insiders（分母 2）

| dataset | 处置 | 理由 |
|---|---|---|
| **insiders1** | **采用（主腿）** | 字段级 6 个可用数值字段、cov 0.5343。① 已登记的"单集上限 1.30"（`tracking/DEU/atom_orthogonal/BE176_INSIDERS1_CEILING_130_20261112.md`，3 波 30 臂）**只对单数据集 ATOM 成立**；② 我自己的 SQL 读数：池内 `insd1_` 臂 116 条，其中 **73 条 sub≥1.0**、最高 S 2.64；③ 已有 ACTIVE 先例 `d5a2aO7v`（S 1.66，2026-11-12）；④ **十年跨度实测通过**（`get_alpha_yearly_stats`：`XgaGb3J1` 2014–2023 逐年 pnl>0、LC 99–170/SC 107–187；`d5a2aO7v` 亦 2014–2023 逐年 pnl>0）。 |
| **insider_agg_matrix** | **采用（仅作共生腿）**（v2 更正） | ① 单集 ATOM 上限 **0.92**（`DEU-INSIDER-AGGMATRIX-DEAD`，22 模板）仍成立 ⇒ **不作主信号**；② 但其字段是现存最强臂的核心腿：`significant_value_1..4`（cov 0.5342）在 `XgaGb3J1`/`0mPKr3bq` 里作比值分母/分子，`directional_indicator`（cov **1.0**）被 **ACTIVE** `Vk65zLzG` 使用（LC/SC 112/102，S1.79/F1.69/2Y2.07/sub1.44，self/prod 0.64）；③ **死档"directional_indicator/_2 零持仓"与实测相反**（两字段 cov=1.0、alphaCount 52/23），该子句不采信。 |

### 4.2 institutions（分母 5）

| dataset | 处置 | 理由 |
|---|---|---|
| **institutions6** | **采用（仅作分组轴/残差轴）** | ① 11/11 字段 cov=1.0（全宽度，最适合分组轴）；② 类别参考 `references/institutions.md:56` "institutions6 作主信号判死；**作慢门控腿可用**（IND levk5JYN，prod 0.55）"；③ 我自己的臂数：以 institutional 系为腿的池内臂 **6 条 |S|≥1.58**，最高 `vRA82ogA` S2.07/F1.85/2Y2.59/sub1.43、RA 全过、self **0.265** PASS；④ 平台映射实读：`count_institutional_buyers_security` → `DEU/D1/INSTITUTIONS`。**⚠ 仅 bucket/分组轴用法未验（§5.4）**。 |
| fund_holdings_panel | 排除 | 三条独立判死（`DEU-FHP-ALLGATE-CLOSED` / `DEU-FHP-SCEILING-DEAD` / `DEU-INSTITUTIONS-fundholdings-SINGLEATOM-WEAK`）+ 跨集救援判死 `DEU-CROSSSET-RESCUE-DEAD`。**v2 更正**：v1 引用的"类别参考 102 回测 / 0 条 RA 全过"是 **2026-10-04 的快照**，已被 `E56AzejK`（institutions1+other455，`failed_ra_count=0`）打破 ⇒ **该快照不再作排除依据**，本节只以三条判死 + 94 臂 0 胜绩为据。 |
| institutions1 | 排除（作为主信号） | ① `DEU-INSTITUTIONS1-PROBE-DEAD-20260923`：方向为负、qp 预估 0.32–0.44 与实测一致；② 该族唯一有效构造（`inst1_valueeur/holdings × oth455 cluster`）已被 ACTIVE `2rmGAPqN`（S1.81/prod0.6292/self0.0327）占位，后继两条 `d5WwzRMY`/`E56AzejK` 实测 **self 0.9287 / 0.9184**（`DEU-INST1-OTH455-CLUSTER-DUP-DEAD`）⇒ **真实排除依据是 self 墙 + 占位，不是"RA 全过=0"**。本波刻意不用 `inst1_*` 以避开该墙。 |
| institutions25 | **待探针，不作可用** | 24 字段**字段级** coverage 全 = 0.0（`platform_count=24` 实取），集级亦 0.0。按纪律集级 cov=0 不是存在性判据，但字段级也全 0 是第二条同向读数；仍不能判"无数据"（GBR `techindi_model` 反例：cov=0 但真实 399 字段）。本地另有 33 条 `inst25_*` 臂 max|S|=1.22。**处置**：不判死、不入本波；要开先跑 `tools/probe/dataset_data_probe.py` 一条最小探针。 |
| institutions4 | 排除（本波） | 6 字段、cov 0.3413；无过闸证据、无判死记录 ⇒ **"未测"而非"已死"**；字段太少且与 institutions6 的持股轴高度同义，优先级更低。 |

### 4.3 need=3 的 8 座塔（登记依据，均不作目标）

| 塔 | 依据 |
|---|---|
| news | `news104` 6 探针 max0.74 且镜像 ±S 对称（`E56AVqkR +0.22 vs 9qxQE9Jr −0.22`、`O0AvAEJY +0.74 vs A1VdVMvQ −0.74`）= 噪声指纹；`news17` 8 臂 max0.41；`news81/38/48` 与 `analyst7` 字段 cov=0；`news50` 在死名单；`DEU-NEWS-SENTIMENT-DEAD`、`DEU-NEWS18-ALLDEAD` |
| pv | `pv106` S1.38/2Y0.94；`intraday_pv_feats` 13 模板 max0.64；`pv109`；`pattern_scores` 0.23；`continuation_score`；`pv20` 死名单 |
| risk | `risk72` 12/12 负、上限 0.76；`risk71`；`risk60/risk88` 死名单 |
| earnings | `earnings6` sub −0.82 判假强 |
| socialmedia | `sm12` S0.21/0.14；`socialmedia39` 单字段是 ID 不可用 |
| imbalance | `imbalance5` 唯一集，`imb5_score` 近静态 S0.24/2Y−0.55 |
| option | `option1` 在死名单；本档未找到活面证据（**"未找到证据"≠"已探明无解"**） |
| macro | **无任何判死条目**（我把 DEU 全部 70 条 `registry_empirical` dead_end 逐条列出核对，无 macro 命中），不在 19 条死名单 ⇒ **未测面**，但 need=3 |

---

## §5 配对塔合规检查 & 未验项

| 规则 | 本组合 |
|---|---|
| ① 禁 PV+MODEL / PV+OTHER / MODEL+OTHER / PV+PV / MODEL+MODEL / OTHER+OTHER | **不触**：INSIDERS + INSTITUTIONS 均不在 trio |
| ② trio 某类 + 非 trio 类累计 ≤5 | **对收割件适用**：`[INSIDERS,MODEL]` 属 trio(MODEL)×非trio(INSIDERS)。本地已提交件按 code 推论该组合 **1 条**（`Vk65zLzG` ACTIVE 2026-09-13）⇒ 余量 4。⚠ 该计数是**推论**：24 条已提交件里 3 条 `code` 为空（盲区），实际可能是 1–4，**开波前须按平台 `pyramids` 复核**。 |
| ③ 任何 ≥3 塔同现 ⇒ 归 0 | **红线**：本设计只许引用 `insd1_*` + institutions 系两类字段。反例已抓两条：`1YWnZ9rK`（含 `cap`）eff=0、`vRA82ogA`（含 `est_12m_ebi_*`）eff=0。**`cap` 是 PV 字段，本波禁用**；`predicted_surprise_*`/`mean_estimate_change_*` 是 MODEL 字段，**若只作第二塔则得 [INSIDERS,MODEL]，若再加 institutions 就三塔归零** ⇒ 收割件与配对件必须分开做，不可合并成一条。分组轴只用 GROUP 字段（`sector`/`industry`/`subindustry`/`market`）——`d5a2aO7v` 用 `sector` 仍只有 2 塔。 |
| ④ 塔归属以平台 `pyramids[].name` 为准 | 已办（§2.2 九条 `get_alpha_details` 实读） |
| ⑤ 单两塔组合 ≤3 | `[INSIDERS,MODEL]` 已 1 条（`Vk65zLzG`）；`[INSIDERS,INSTITUTIONS]` **0 条**（池内该类组合 0 臂，§9.1）⇒ 配额充足 |
| **⑥ 未验项（必须波内自证）** | `institutions6` 的其他 10 字段（`aggregate_*` / `market_value_*` / `quantity_*`）**塔归属未验证**；且"institutions6 只作 bucket/分组轴时是否仍计 INSTITUTIONS"**无任何已测件覆盖** —— `vRA82ogA` 里它是**信号腿**（不是分组轴）且整件三塔归零。**故波首臂必须先验证，不能假设**（见 §7.4 臂0）。 |

---

## §6 机制假设（驱动臂表）

> **内部人真实申买的信息只在"机构监督弱、套利约束大"的股票里被定价**——以 `insd1_holdings` 的自身变化
> 与信息比率（内部人持仓动量/稳定性）+ `insider_agg_matrix` 的 `significant_value_1..4` 比值作主腿，
> 用 `institutions6` 的机构持股**分位带**作分组轴（不相加、不缩持仓），只在低机构持股分位内做横截面排序。

可证伪点：
1. **分组轴有效性**：按机构持股分位分 5 带后，低分位带的内部人买入强度应显著高于高分位带；若各带 S 与裸跑逐位相同 ⇒ 该轴无信息。
2. **方向性**：内部人买入正向、卖出为负；若镜像对称（§7.2）⇒ 方向层无净信息。
3. **持仓水平 vs 家数**：用持股**水平/变化**（`aggregate_*` / `quantity_*`）优于**家数**（`count_institutional_*`），
   依据 = 类别参考"机构家数类整类静态"（换手 0.0146–0.0204）⇒ 家数类只可当分组值，不可当主信号。

---

## §7 判读基准

### 7.1 硬门槛（all must pass）

| 轴 | 线 | 来源 |
|---|---|---|
| Sharpe | ≥ **1.58** | `tracking/DEU/config/thresholds.json`（`sharpe_min`）。⚠ **内部严线**：平台 `LOW_SHARPE` 的 limit 值本轮**未读到**（`get_alpha_details` 只回 PASS 不回 limit），不得表述为"平台硬线" |
| Fitness | ≥ **1.0** | 同上 `fitness_min` |
| Two-year Sharpe | ≥ **1.58** | `thresholds.json:6` `_two_year_note`（平台实测：RREALzx0 `{name:LOW_2Y_SHARPE, value:1.43, limit:1.58}`） |
| sub_universe_sharpe | ≥ **1.0** | `thresholds.json` `sub_universe_sharpe_min`（与 ask 的 sub≥1 同值） |
| Turnover | 0.01–0.70 | `turnover_min/max` |
| Margin | ≥ 5 bp | `margin_min 0.0005` |
| CONCENTRATED_WEIGHT | ≤ 0.5 | 本地 review 线；平台 limit 实读 0.1，更严 |
| self / prod | 各 < **0.70** | `src/wqb/config.py:502 PRODCORR_CEILING = 0.70`；`thresholds.json hard_gates` 同值 |

### 7.2 符号指纹（判"机制在" vs "符号错"）

- **镜像对称检验**（决定性）：同式取反 `-expr` 重跑一条。
  - `S(-expr) ≈ −S(expr)`（差 <0.03）且 TO/DD/longCount 逐位相同 ⇒ **方向层无净信息、机制不在**，停
    （`news104`/`news17` 判死即此指纹：`E56AVqkR +0.22 vs 9qxQE9Jr −0.22`、`O0AvAEJY +0.74 vs A1VdVMvQ −0.74`）。
  - 两向不对称（|S+|−|S−| > 0.1）⇒ 机制在、取强侧。
- **衰减梯检验**：平滑窗 `ts_mean/ts_ir` 22 → 66 → 132 应呈**单峰**；单调或随机 ⇒ 结构未对上。
- **符号约定**：DEU 已有两处反转先例（`risk72` 残差是动量非反转；fnd1 CEO 任期"经验"为正）⇒ **内部人符号必须区内实测**。

### 7.3 真正的瓶颈轴（v2 更正）

v1 断言"sub≥1.0 是本族真正的墙"——**只在 `insd1+shrt3` 配对成立**，不能推广：

| 口径（本地 SQL，`region_id=10`，池 = S≥1.58 + RA 空 + prod<0.7/空 + 未提交 + stage IS） | 臂数 | sub≥1.0 条数 | 全闸条数 |
|---|---:|---:|---:|
| 池内 `insd1_` 臂（不限第二腿） | 116 | **73（63%）** | — |
| `[INSIDERS,MODEL]` 配对 | 40 | 38 | **38** |
| `[INSIDERS,ANALYST]` 配对 | 5 | 5 | **5** |
| `[INSIDERS,SHORTINTEREST]` 配对 | 32 | **0** | **0** |

⇒ **正确表述**：`insd1+shrt3` 这一配对把 sub 压到 [0.81, 0.98]（32/32 全部 <1.0）；
而 `[INSIDERS,MODEL]` 配对的 sub 是 **1.51–1.54**（`XgaGb3J1` 1.51 / `0mPKr3bq` 1.54）。
⇒ **开波第一设计目标不是"抬 sub"，而是"选对第二腿"**：把 sub 从 shrt3 配对的 0.81–0.98 换到 ≥1.0 的配对。

### 7.4 十年跨度（R5 已关闭）

`get_alpha_yearly_stats` 实读：
- `XgaGb3J1`：2014–2023 **逐年 pnl>0**（100 万–194 万），LC 99–170 / SC 107–187，年 S 1.52–3.43。
- `d5a2aO7v`：2014–2023 **逐年 pnl>0**，LC 109–198 / SC 105–199，年 S 0.61–2.71。
⇒ **insd1 族无 sentiment 那种前五年零持仓缺口**（对比：`bl6OWZ2M`/`kqNRX1ZP` 2014–2018 全零）。
`DEU-SENTIMENT-TOWER-DATASPAN-DEAD` 的"近十年硬闸"在本区实际未被执行（ACTIVE 件 `bl6OWZ2M` 同样五年空白），
故该条**不用于排除 sentiment**，insd1 族则本就满足。

---

## §8 settingsLine（本族存活配置行）与理由

```
DEU/TOP500/D1/decay0/SUBINDUSTRY/trunc0.08/nanHandling ON/maxTrade OFF/FASTEXPR
```

**依据（平台实读，逐件登记；⚠ 非单变量对照）**：

| 件 | 状态 | 主腿窗 | decay | neut | trunc | nan | S / F / 2Y / sub / TO / margin |
|---|---|---|---:|---|---|---|---|
| **XgaGb3J1** | UNSUBMITTED（收割主） | `ts_mean/ts_ir(insd1_holdings,66)` + `significant_value` 比值 66 | **0** | SUBINDUSTRY | 0.08 | ON | 2.36 / 2.02 / 2.71 / 1.51 / 17.38% / 14.66bp |
| **0mPKr3bq** | UNSUBMITTED（收割备） | 同上（外层 group_zscore×2） | **0** | SUBINDUSTRY | 0.08 | ON | 2.36 / 2.04 / 2.67 / 1.54 / 16.40% / 14.88bp |
| d5a2aO7v | **ACTIVE**（2026-11-12） | `ts_backfill(insd1_holdings,110)`+`ts_rank(...,252)`；`ts_delta(shrt3_bar,220)` | 8 | SUBINDUSTRY | 0.08 | ON | 1.66 / 1.36 / 2.58 / 0.92 / 9.47% / 17.86bp |
| d5a2K72E | UNSUBMITTED | `ts_backfill(insd1_holdings,66)`+`ts_rank(252)`；`ts_delta(ts_backfill(shrt3_bar,66),220)` | 4 | SUBINDUSTRY | 0.08 | ON | 1.78 / 1.42 / 2.28 / 0.88 / 14.65% / 12.73bp |
| Vk65zLzG | **ACTIVE**（2026-09-13） | `ts_sum(ts_backfill(directional_indicator,66),252)` + model 四腿 | 4 | SUBINDUSTRY | 0.08 | **OFF** | 1.79 / 1.69 / 2.07 / 1.44 / 12.03% / 18.46bp |

**为什么是这一行、以及不能声称什么**：
1. **decay 归因不干净（v1 错误更正）**：上表五件的 `decay` 与**主腿窗口/结构同时变化**
   （0 配 `ts_mean(…,66)`；4 配 `ts_backfill(,66)+ts_rank` 与 `directional_indicator`；8 配 `ts_backfill(,110)`），
   **不是单变量对照** ⇒ v1 的"decay 三档 → S-2Y 跷跷板"结论**撤回**，本档不据此断言 decay 效应。
2. **选 decay 0 的真实理由**：池内**唯一同时满足"全闸 + 2 塔 + self 实测 PASS"**的两件（`XgaGb3J1`/`0mPKr3bq`）
   都是 decay 0；而唯一被平台接受并 ACTIVE 的同族 2 塔件（`d5a2aO7v`）是 decay 8 ⇒ **两档都有存活证据**，
   故 decay **必须作波内对照臂**（0/4/8 各 1 臂），不得把任一档写成既定。
3. **中性化 SUBINDUSTRY 四件无例外**；`DEU-MODEL53-CREDIT-RISK-DEAD` 的 cross-dataset finding
   "SUBINDUSTRY 全仓中性化把绝对水平吃光，只留下相对自身历史的偏离残差" ⇒ 信号须为 `ts_rank`/`ts_delta`/`ts_ir` 形。
4. **nanHandling 分歧已知**：`Vk65zLzG` 是 **OFF**（且 ACTIVE），其余四件 ON。insd1 字段级 cov 仅 0.5343 ⇒
   本波取 ON（覆盖更宽），但把 OFF 列为对照臂（活跃 ACTIVE 件用的是 OFF，不能默认 ON 更优）。
5. **truncation 0.08 / maxTrade OFF / FASTEXPR 五件一致**。

---

## §9 收割池（v2：非空，零仿真 1 步）

### 9.1 池规模（只读 SQL）

口径：`alphas` join 每 alpha 最新 `backtest_results`；`region_id=10`、`S≥1.58`、`status∈{UNSUBMITTED,NULL}`、
`stage∈{IS,NULL}`、`ra_failed_checks∈{'[]',''}`、`prod_correlation IS NULL OR <0.70` ⇒ **313 行**。

**修正分类器（6/6 与平台 `pyramids` 集合一致）后的分布**（关键桶）：
```
('insiders','model') 40 | ('analyst',) 39 | ('model',) 36 | ('insiders','shortinterest') 32
('sentiment',) 28 | () 28 | ('insiders','model','pv') 22 | ('shortinterest',) 21
('analyst','model') 14 | ('fundamental',) 7 | ('pv',) 7 | ('insiders','other') 5 | ('analyst','insiders') 5
('insiders','institutions','other') 3 | ('analyst','insiders','institutions') 2 | … (其余 ≤2)
```
（`insiders` 单类 = 1；`insiders+institutions` 单列 = **0** ⇒ 本波配对是全新组合）

### 9.2 self 实测（`check_self_correlation`，本地增量缓存，**不消耗平台相关槽**）

| 候选 | 平台 pyramids | S / F / 2Y / sub / TO / margin | prod | self 实测 | 判决 |
|---|---|---|---|---|---|
| **`XgaGb3J1`** | `[INSIDERS,MODEL]` **eff2** | 2.36 / 2.02 / 2.71 / 1.51 / 17.38% / 14.66bp | **未测** | **0.6784** vs `Vk65zLzG` → **PASS** | ✅ **可收割（主）** |
| **`0mPKr3bq`** | `[INSIDERS,MODEL]` **eff2** | 2.36 / 2.04 / 2.67 / 1.54 / 16.40% / 14.88bp | **未测** | **0.6714** vs `Vk65zLzG` → **PASS** | ✅ **可收割（备）** |
| `vRA82ogA` | `[INSTITUTIONS,INSIDERS,ANALYST]` **eff0** | 2.07 / 1.85 / 2.59 / 1.43 | 未测 | 0.2650 vs `2rmGAPqN` → PASS | ❌ 3 塔归 0，不可派 |
| `1YWnZ9rK` | `[PV,INSIDERS,MODEL]` **eff0** | 2.64 / 2.17 / 2.86 / 1.72 | 未测 | 0.5487 vs `Vk65zLzG` → PASS | ❌ 3 塔归 0，不可派 |
| `d5a2K72E` | `[SHORTINTEREST,INSIDERS]` eff2 | 1.78 / 1.42 / 2.28 / 0.88 | 未测 | **0.9133** vs `d5a2aO7v` → FAIL | ❌ clone 墙 |
| `GrWVx2aO` | `[SENTIMENT]` eff1 | 2.07 / 1.89 / 2.55 / 1.29 | 未测 | **0.8419** vs `bl6OWZ2M` → FAIL | ❌ clone 墙 |

**⇒ 零配额收割 = 2 条**（`XgaGb3J1` 主 / `0mPKr3bq` 备），均为 `[INSIDERS,MODEL]` ⇒ **只推进 insiders 一颗**
（MODEL 已 3/5 点亮、无增量）。

**⚠ 余量告警**：两条的 self 余量只有 **0.0216 / 0.0286**（红线 0.70）。平台提交期 `SELF_CORRELATION` 若略高即挂，
故必须按 §7.5 五道闸的 self 终验（平台端点）复核，不能只信本地缓存。**且两条 prod 全未测** —— "零配额"成立，
"零风险"不成立。

### 9.3 十年跨度（收割件的硬前置，已实读）

`XgaGb3J1` 2014–2023 逐年 `pnl>0`、`LC 99–170 / SC 107–187`（无零持仓年）；`d5a2aO7v` 同。
⇒ 收割件不触发 AGENTS §7.5 第 3 道闸（近十年）。

### 9.4 `submit_ready` 不可当收割池（工具盲区实证）

`mcp__wqb-db__get_submit_ready(region="DEU", status="READY", limit=200)` 给 12 条，其中 `kqNRX1ZP` 的 `prod` = **null**
（`corr_stale_reason="missing"`），但 `alphas.prod_correlation` = **0.7706 > 0.70**（平台 `checks.pending` 含 `PROD_CORRELATION`）。
⇒ **`submit_ready.prod` 不是 prod 权威读数**。反过来，`submit_ready` 里也**没有** `XgaGb3J1`/`0mPKr3bq`
（它们从未入队）—— **两个方向都漏**，故收割必须走 `alphas` 表 + 平台实读。

---

## §10 风险登记

| # | 风险 | 读数/依据 | 处置 |
|---|---|---|---|
| R1 | **收割件 self 余量薄** | `XgaGb3J1` 0.6784 / `0mPKr3bq` 0.6714，红线 0.70（余 0.0216 / 0.0286） | 提交前用平台 `SELF_CORRELATION` 端点终验；若不过，改用备件；两件都不过则回落到新件路线 |
| R2 | **收割件 prod 未测** | 两件 `prod_correlation` 均 null | 提交前 `check_correlation(production, refresh=True)`；prod≥0.70 则本路停手（参照 `kqNRX1ZP` 0.7706 反例） |
| R3 | **第 3 塔静默归零** | `1YWnZ9rK`（含 `cap`）、`vRA82ogA`（含 `est_12m_ebi_*`）均 `effective=0` | 禁 `cap`；禁 `predicted_surprise_*`/`mean_estimate_change_*` 与 institutions 同件；每臂派发后复核 `pyramids.effective==2` |
| R4 | **institutions6 作分组轴时塔归属未验** | 无任何已测件覆盖；`vRA82ogA` 里它是信号腿且三塔归零 | **臂0 先验证**（§12.1）；不成立则改条件/残差入场并复验 |
| R5 | **trio×非trio 累计余量不足 5** | `[INSIDERS,MODEL]` 已提交 **1 条**（`Vk65zLzG`，按 code 推论；24 件已提交里 3 件 code 为空 ⇒ 实际 1–4） | 开波前按平台 `pyramids` 复核真实条数；收割件占 1 格，剩余 ≥1 |
| R6 | **sentiment 被自己锁死** | `GrWVx2aO` self 0.8419 vs ACTIVE `bl6OWZ2M` | 本波不碰；将来须换机制（sentiment33 面）并先测 self |
| R7 | **insd1 与 inst1 同事件类** | `insiders1`=insd1_*（Global）；`institutions1`=inst1_*（Europe，归 institutions 塔） | 本波不用 `inst1_*`，只用 `aggregate_*`/`count_institutional_*` 持股类（不同信息） |
| R8 | **季度清零** | `docs/time_bombs.json` TB-05 | 本档 1/3→3/3 推论只在 2026Q4 成立 |
| R9 | **settingsLine 无单变量对照** | §8 五件的 decay 与主腿窗同时变 | 波内 decay 0/4/8、nanHandling ON/OFF 各作对照臂，不得把任一档当既定 |

---

## §11 证据通道与盲区

| 结论 | 通道 | 盲区 |
|---|---|---|
| 塔位 16 类计数 | 平台 `get_pyramid_alphas()`（当季 MCP 直读） | 只给计数不给是哪条；当季按自然季清零；pending 相关闸也计入 |
| 数据集分母 2/5/3 | 平台 `/data-sets`（`get_datasets` 按 region/universe/delay 实取） | 只给**集级** coverage/fieldCount，对字段级可用性盲视 |
| 字段可用性 | 平台 `/data-fields`（dataset-scoped 全量，`complete=true` 与 `platform_count` 一致） | 只给字段 coverage，不给 longCount/shortCount；拉不到≠没数据（需探针）；`filter_sharpe` 会过滤（本轮 `sharpe_filter_removed=0`） |
| 历史臂数（116/73/40/38/32/5…） | **本地 `data/wqb.db` 只读 SQL**（`alphas`×`backtest_results`） | ① 能看见 MCP 直连仿真的 `backtest_results` 行；② 仍盲视"既不写 expressions 也不入 backtest_results"的仿真；③ `dataset` 列大量 NULL ⇒ 按 **code 字段前缀**归类；④ 同式重复回测会多计行（本档按 distinct alpha_id 报） |
| 塔归属 / effective | 平台 `get_alpha_details().pyramids`（9 件实读） | 只能逐件查；其余 313 条用**已 6/6 校验**的前缀分类器推定，属"推定"非"实读" |
| self correlation | `check_self_correlation`（本地增量缓存，不占平台槽） | 池=已提交 OS 池（24 条，剔除 4 条 Power Pool）；对**未提交同批候选互相关盲视**（篮内互相关需另跑 `compute_mutual_correlation`）；首次调用可能 30s 超时（`GrWVx2aO`、`XgaGb3J1` 各超时一次，重试成功） |
| 判死/封盘 | `get_dead_datasets`(19) + `get_dead_ends`(70 全量) + `tracking/DEU/` 参考 | **死标记不得单独作判据**（本档已被实测推翻两处：`directional_indicator` 零持仓、institutions "0 RA 全过"）；MCP 返回曾因体量截断，本档改用 DB 全量枚举 |
| "未测"清单 | 上述全部 | **"未测"= 这些通道里没找到证据**，不等于没人跑过。`institutions4`/`institutions25`/`macro`/`institutions6` 其余 10 字段均属此类 |

---

## §12 下一步（给下游波次）

### 12.1 时序（v2 更正：先收割，再开波）

1. **第 0 步（零配额，先做）**：对 `XgaGb3J1` 跑 `check_correlation(production, refresh=True)` + 平台 self 终验。
   - **prod < 0.70 且 self < 0.70** ⇒ 提交（用户确认后）→ **insiders 1/3→2/3**；
   - prod ≥ 0.70 ⇒ 换 `0mPKr3bq` 同法；两件皆堵 ⇒ 只走新件路线。
2. **第 1 步（波首臂 = 塔归属验证件，必须最先跑）**：取 `vRA82ogA` 的**主腿**（去掉 `est_12m_ebi_*` 与 `oth455` 第三腿），
   把 `count_institutional_buyers_security` 从"信号腿"改为 **bucket/分组轴**（如
   `group_zscore(group_neutralize(core, bucket(rank(ts_delta(ts_mean(count_institutional_buyers_security,22),66)), range="0,1,0.2")), market)`）。
   跑完**立刻** `get_alpha_details` 验 `pyramids.effective==2` 且集合 = `{INSIDERS, INSTITUTIONS}`。
   - 成立 ⇒ 继续该形扩展臂；
   - 不成立（bucket-only 不计塔）⇒ 改 `trade_when` 条件入场或 `vector_neut` 残差入场，复验；仍不计塔则本配对放弃，回落 §12.3。
3. **第 2 步**：新双塔件过闸 ⇒ 提交（用户确认）→ **insiders 3/3 点亮 + institutions 1/3→2/3**。

### 12.2 臂表设计纪律

- **自相关前置筛**：每臂派发前先对 `2rmGAPqN` / `d5a2aO7v` / `Vk65zLzG` 三点做 self 预筛（`check_self_correlation`，零配额）；
  逐臂记录 `[两塔组合]` 计数（trio×非trio ≤5、单两塔 ≤3）。**这是 v1 的最大方法缺口**（v1 只测 4 条就下"收割池为空"的结论）。
- **禁字段**：`cap`（PV，三塔陷阱）；`predicted_surprise_*`/`mean_estimate_change_*`（MODEL，与 institutions 同件即三塔）；
  `inst1_*`（clone 墙）；`directional_significant_value_1`（毒，alphaCount 0）。
- **对照臂**：decay 0/4/8、nanHandling ON/OFF、分组轴 sector vs subindustry vs market（DEU 杠杆 H ⑤：sector ≫ subindustry 在 fnd72 族成立；本族 `d5a2aO7v` 用 sector 已 ACTIVE）。
- **近闸即探 prod**：任一臂 S≥1.2 或距任一硬闸 ≤0.4，先 `check_correlation(production, refresh=True)`（`_effective-levers.md` 通用纪律，用户 2026-11-14 明令）。

### 12.3 回落路线

若 §12.1-2 的 `[INSIDERS,INSTITUTIONS]` 配对验证失败：改走 `[INSIDERS,MODEL]`（38 条全闸臂的成熟形），
代价是只推进 insiders 一颗且吃 trio 配额（余量 ≥1）。**收益仍大于 0，因为它是唯一有 38 条全闸臂背书的组合。**

---

## §13 复现命令

```text
# 塔位（权威）
mcp__wq-brain-http__get_pyramid_alphas()

# 分母
mcp__wq-brain-http__get_datasets(category="insiders",     region="DEU", delay=1, universe="TOP500")
mcp__wq-brain-http__get_datasets(category="institutions", region="DEU", delay=1, universe="TOP500")
mcp__wq-brain-http__get_datasets(category="sentiment",    region="DEU", delay=1, universe="TOP500")

# 字段级（含 v2 新增的 insider_agg_matrix）
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="insiders1",         filter_sharpe=true)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="insider_agg_matrix", filter_sharpe=true)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="institutions6",     filter_sharpe=true)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="institutions25",    filter_sharpe=true)

# 塔归属 / 有效塔数（9 件）
mcp__wq-brain-http__get_alpha_details(alpha_id="XgaGb3J1")  # [INSIDERS,MODEL] eff2  S2.36/2Y2.71/sub1.51
mcp__wq-brain-http__get_alpha_details(alpha_id="0mPKr3bq")  # [INSIDERS,MODEL] eff2  S2.36/2Y2.67/sub1.54
mcp__wq-brain-http__get_alpha_details(alpha_id="Vk65zLzG")  # [INSIDERS,MODEL] eff2  ACTIVE 2026-09-13
mcp__wq-brain-http__get_alpha_details(alpha_id="d5a2aO7v")  # [SHORTINTEREST,INSIDERS] eff2 ACTIVE
mcp__wq-brain-http__get_alpha_details(alpha_id="d5a2K72E")  # [SHORTINTEREST,INSIDERS] eff2
mcp__wq-brain-http__get_alpha_details(alpha_id="1YWnZ9rK")  # [PV,INSIDERS,MODEL] eff0
mcp__wq-brain-http__get_alpha_details(alpha_id="vRA82ogA")  # [INSTITUTIONS,INSIDERS,ANALYST] eff0
mcp__wq-brain-http__get_alpha_details(alpha_id="E56AzejK")  # [INSTITUTIONS,OTHER] eff2 failed_ra=0
mcp__wq-brain-http__get_alpha_details(alpha_id="bl6OWZ2M")  # [SENTIMENT] eff1 ACTIVE

# 自相关（零配额）
mcp__wq-brain-http__check_self_correlation(alpha_id="XgaGb3J1", threshold=0.7)  # 0.6784 PASS
mcp__wq-brain-http__check_self_correlation(alpha_id="0mPKr3bq", threshold=0.7)  # 0.6714 PASS
mcp__wq-brain-http__check_self_correlation(alpha_id="d5a2K72E", threshold=0.7)  # 0.9133 FAIL
mcp__wq-brain-http__check_self_correlation(alpha_id="GrWVx2aO", threshold=0.7)  # 0.8419 FAIL
mcp__wq-brain-http__check_self_correlation(alpha_id="vRA82ogA", threshold=0.7)  # 0.2650 PASS（但 3 塔）
mcp__wq-brain-http__check_self_correlation(alpha_id="1YWnZ9rK", threshold=0.7)  # 0.5487 PASS（但 3 塔）

# 十年跨度
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="XgaGb3J1")   # 2014-2023 逐年 pnl>0
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="d5a2aO7v")   # 2014-2023 逐年 pnl>0
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="bl6OWZ2M")   # 2014-2018 全零（对照）
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="kqNRX1ZP")   # 2014-2018 全零（对照）
```

```sql
-- 臂数 / 池（只读，mode=ro）
with latest as (select alpha_id, max(id) mid from backtest_results where region='DEU' group by alpha_id)
select a.alpha_id,a.sharpe,a.fitness,a.two_year_sharpe,a.sub_universe_sharpe,a.turnover,a.prod_correlation,
       a.self_correlation,a.status,a.platform_status,b.ra_failed_checks,b.code,b.wave
from alphas a join latest l on l.alpha_id=a.alpha_id join backtest_results b on b.id=l.mid
where a.region_id=10 and a.sharpe>=1.58
  and (a.status='UNSUBMITTED' or a.status is null)
  and (a.stage is null or a.stage='IS')
  and (b.ra_failed_checks='[]' or b.ra_failed_checks='')
  and (a.prod_correlation is null or a.prod_correlation<0.70);
-- 313 行；分类器与分布见 §9.1
```

---

## §14 复核台账（v2：逐条采信/未采信 + 我的独立核验）

**复核意见共 7 条问题 + 10 条缺失证据 + 10 条必须修改。逐条处置如下。**

### 14.1 采信的 7 条问题（全部经我本人重跑核验）

| # | 复核意见 | 我的核验（本轮实跑） | 采信 |
|---|---|---|---|
| Q1 | 313 条池里有 38 条 `[INSIDERS,MODEL]` + 5 条 `[INSIDERS,ANALYST]` 全闸臂；`XgaGb3J1` self 0.6784 PASS、`0mPKr3bq` 0.6714 PASS ⇒ 零仿真即可 1/3→2/3 | ✅ 全部复现：`get_alpha_details("XgaGb3J1")` = S2.36/F2.02/2Y2.71/sub1.51/TO17.38%/margin14.66bp/`failed_ra_count=0`/`[INSIDERS,MODEL]` eff2/UNSUBMITTED；`check_self_correlation("XgaGb3J1")` = **0.6784242083598276** PASS；`("0mPKr3bq")` = **0.6713570156595247** PASS（top `Vk65zLzG`）。修正分类器后池内 `('insiders','model')` = **40 臂 / 38 全闸**、`('analyst','insiders')` = **5 / 5** | **采信** |
| Q2 | `insider_agg_matrix` 排除与实测相反：34 字段实读，`significant_value_1..4` 是该集且为 38 条全闸臂核心腿；`directional_indicator`（cov=1.0）被 ACTIVE `Vk65zLzG` 在用 | ✅ 复现：`get_datafields(dataset_id="insider_agg_matrix")` `count=34/complete=true`，含 `significant_value_1..4`(cov 0.5342)、`directional_indicator`(**cov 1.0**,alphaCount 52)、`directional_indicator_2`(**cov 1.0**,23)；`get_alpha_details("Vk65zLzG")` = ACTIVE，code 首项 `rank(ts_sum(ts_backfill(directional_indicator,66),252))`，LC/SC **112/102**，S1.79/F1.69/2Y2.07/sub1.44 | **采信（v1 该条错误）** |
| Q3 | "institutions 塔历史 0 条 RA 全过"与 `E56AzejK` 冲突；真实依据是 self 0.9184/0.9287 撞 `2rmGAPqN` | ✅ 复现：`get_alpha_details("E56AzejK")` `failed_ra_count=0`、`checks.fail=[]`、9 项 PASS、`[INSTITUTIONS,OTHER]`。v1 引用的"102 回测/0 RA 全过"确为**类别参考 2026-10-04 快照** | **采信（v1 该条错误）** |
| Q4 | "sub≥1.0 是本族真正的墙"只在 insd1+shrt3 成立；159 条 insd1 臂中 94 条 sub≥1.0 | ✅ 方向采信。**我的读数**：池内（非全量）`insd1_` 臂 **116**、sub≥1.0 **73（63%）**；`[INSIDERS,SHORTINTEREST]` 32 臂 **0** 条 sub≥1.0（区间修正为 [0.81,0.98]）；`[INSIDERS,MODEL]` sub 1.51–1.54。⚠ 分母不同（复核用全量 159，我用池口径 116），结论同向 | **采信（分母按我的读数更正）** |
| Q5 | 双塔映射是外推：`institutions6` 只作 bucket/分组轴时是否仍计 INSTITUTIONS，无已测件 | ✅ 成立。我复查 6 条 institutions6 过闸臂：`vRA82ogA`（+`est_12m_ebi_*`→ANALYST）eff0、`A1x9v2dQ` eff0、`KPg3r2jz` 带第三腿 ⇒ **无一条是"仅 bucket 用 institutions6"** | **采信，降级为未验项（§5⑥ / R4）** |
| Q6 | settingsLine 的 decay 归因不干净（`d5a2aO7v` bf110+shrt3 220 vs `d5a2K72E` bf66，两件不止差 decay） | ✅ 复现：两件 code 实读确为不同窗口；`Vk65zLzG` 又是 `directional_indicator` 不同结构 ⇒ **v1"decay 三档对照 → S-2Y 跷跷板"结论撤回** | **采信（§8 已重写）** |
| Q7 | 收割候选 self 余量仅 0.0216/0.0286，且 prod 全未测；towerGain 只在 2026Q4 成立（TB-05） | ✅ 成立。已列入 R1/R2/R8 | **采信** |

### 14.2 采信的缺失证据（已在本轮补齐）

| 缺失项 | 本轮补齐读数 | 落点 |
|---|---|---|
| 43 条两塔 insiders 全闸臂的 self 预筛 | 补测 2 条并 PASS（0.6784 / 0.6714）；仍未做全量 43 条 ⇒ **改为波内纪律**（§12.2 自相关前置筛） | §9.2 / §12.2 |
| `XgaGb3J1`/`0mPKr3bq` 的 prod 未测 | 仍未测（需平台相关槽，超出 S0 零配额边界）⇒ 列为 R2 与 §12.1 第 0 步 | R2 |
| `institutions6` bucket-only 塔归属未验 | 未验（需一条仿真）；已改为**波首臂验证件**，并写死不成立时的替代入场（trade_when / vector_neut） | §5⑥ / R4 / §12.1-2 |
| `aggregate_*`/`market_value_*`/`quantity_*` 塔归属未验 | 未验；仅 `count_institutional_buyers_security` 有 `vRA82ogA` 实读 | §3.2 注 / §5⑥ |
| 未复用 `vRA82ogA` 去第三腿的骨架 | 已改为波首臂的起点骨架（去掉 `est_12m_ebi_*` 与 `oth455` 腿） | §12.1-2 |
| trio×非trio 累计条数 | 本地推论 **1 条**（`Vk65zLzG`）；⚠ 24 条已提交件中 3 条 `code` 为空 ⇒ 实际 1–4，**须平台复核** | §5② / R5 |
| insd1 十年跨度未核 | **已核实并关闭**：`XgaGb3J1` 与 `d5a2aO7v` 均 2014–2023 逐年 pnl>0、LC 99–198/SC 105–199 | §7.4 / §9.3 / R5 已删 |
| 32 条与 38 条的计数口径混淆 | 已在 §7.3 给三档口径表（116 池 / 40 池 38 全闸 / 32 池 0 全闸） | §7.3 |
| 未复跑 `d5a2K72E` self 0.9133 与 `submit_ready` prod=null | `d5a2K72E` self 本轮**未重跑**（沿用 2026-11-16 早前同 session 读数 0.9133）；`submit_ready` prod=null 与 `alphas` 0.7706 的对照沿用同 session 读数 | §9.2 标注沿用 |
| DEU `LOW_SHARPE` 平台 limit 值 | 未读到（`get_alpha_details` 只回 PASS 不回 limit）⇒ 已把 S≥1.58 明确标注为**内部严线**，不提"平台硬线" | §7.1 |
| institutions4/25 字段级读数 | institutions25 字段级 24/24 cov=0.0 实读（v1 已有）；**institutions4 本轮仍未取字段级**，只用了集级 0.3413 | §4.2 标注 |

### 14.3 未采信的复核条目（附我的理由）

| 复核条目 | 未采信理由 |
|---|---|
| "159 条 insd1_ 臂中 94 条 sub≥1.0" 这一具体计数 | 我按**池口径**（S≥1.58 + RA 空 + prod<0.7/空 + 未提交 + stage IS）读到 116 臂 / 73 条 sub≥1.0。两个分母都可成立（复核的 159 应是"全部 |S|≥1.58 的 insd1 臂，未加池过滤"），但**我不能在档内写一个自己没跑出来的数**，故写我的读数并注明分母差异。结论（sub 不是全族墙）不受影响 |
| "把 harvestPool 改为非空并写入 `XgaGb3J1`" 中的"零仿真收割"表述可放宽为"零仿真 → 1/3→2/3" | **部分采信**：写入了，但**必须带 prod 未测的条件**。prod 是本区已知的硬墙（`kqNRX1ZP` 0.7706 堵、`1YWnZ9rK` 0.5485 净），不能把"prod 未测"当成"prod 净"⇒ 档内写成"若 prod<0.70 ⇒ 2/3；否则换备件/回落" |
| "删掉 §10 R1 的 0.86–0.98，改为 0.81–0.98" | **采信并已在 v1 修正过一次**（v1 正文 §7.3 已改 [0.81,0.98]，但 §10 R1 漏改）。v2 已把三档口径统一到 §7.3 一张表，并在 R1 引用该表，不再重复区间 |
| "towerGain 的 1/3→2/3 只在 2026Q4 成立" → 需按 need=3 重算 | 采信前半（已写 R8 + §1 ★）。但"按 need=3 重算"不是本轮动作：清零后**所有**未亮塔 need 变 3，insiders 仍是优先目标（它有 38 条全闸臂 + 2 条可收割件），故不改变选择，只改变增量数字 |

### 14.4 v1 中由我自查发现的另外两处错误（不在复核清单内）

1. **分类器错误的正向传播**：v1 §9.3 写"`1YWnZ9rK` 分类 (analyst, insiders, pv) vs 平台 [PV, INSIDERS, MODEL]
   **集合一致**"——这句本身就是错的（`analyst ≠ model`），却被我当成"分类器已校验"的证据。
   **根因**：我把 `predicted_surprise_*`/`mean_estimate_change_*` 当成 analyst（实际 MODEL，属 `predictive_starmine`），
   并把"集合大小相同"误读为"集合一致"。v2 已修正分类器并做到 **6/6 严格集合相等**（§14.1 Q1）。
2. **被自己排除的集正是池里最强臂的来源**：`insider_agg_matrix` 的 `significant_value_1..4` 是
   `XgaGb3J1`/`0mPKr3bq` 的比值腿、`directional_indicator` 是 ACTIVE `Vk65zLzG` 的主腿。
   v1 却把整集排除 ⇒ 与本档自己引用的"判死标记不得单独作依据"直接冲突。v2 已按"单集 ATOM 0.92 成立 / 共生腿可用"分层处置。

**方法教训（写入本档供后续复用）**：① 用自建分类器批量判塔数前，必须**逐字段**核对平台 `pyramids`，
不能只比对"集合大小"；② 排除一个数据集时，必须先查它是否作为**共生腿**出现在已过闸/已 ACTIVE 的件里——
"单集 ATOM 死"与"字段不可用"是两个不同结论。

---

## §15 独立复核（S0 重跑，2026-11-16 23:1x；本节由第二个会话追加，**不改动 v2 正文**）

> 触发：脚本派发的 S0 任务要求「塔位必须用 MCP 直读一次」「数据集分母只能来自平台 `/data-sets`」。
> 本节所有读数均由本会话**当场实读**，逐条注明命令；与 v2 不一致处显式标出。
> 结论与 v2 一致：**目标塔 insiders（1/3，差 2，×1.6）+ 配对塔 institutions（1/3，差 2，×1.6）**，
> 主数据集 `insiders1`，配对数据集 `institutions6`。

### 15.1 塔位实读（MCP 一次直读 vs ask 给的 CLI 表）

**命令**：`mcp__wq-brain-http__get_pyramid_alphas()`（无参数 = 当季；返回体按 `region → delay → category` 分档）。

DEU **D1** 实读：`analyst 6 / shortinterest 5 / fundamental 3 / model 3 / other 3 / sentiment 1 / insiders 1 /
institutions 1 / news 0 / option 0 / pv 0 / earnings 0 / macro 0 / risk 0 / socialmedia 0 / imbalance 0`。
DEU **D0** 全 0（非本战役口径，按 delay 过滤，不做跨 delay 求和）。

**与 ask 给定 CLI 表（`campaign_intel.py pyramid`）逐项对照：16 类 alphas 值全等，无差异** ⇒ 本档采用 MCP 读数；
本次**未出现**任务提示里「同 turn CLI 读 2 / MCP 读 3」的那种缓存漂移，故无需覆盖，也无差异可记。
`fundamental/analyst/model/other/shortinterest` 五类 need=0 = 已点亮，**不再作目标**。

### 15.2 本次新增/独立取得的平台读数（不是沿用台账）

| # | 读数 | 命令 | 结果 |
|---|---|---|---|
| A | insiders1 字段级 | `get_datafields(dataset_id="insiders1", region="DEU", universe="TOP500", delay=1)` | `count=8 / platform_count=8 / complete=true`，8 字段全 VECTOR、cov 全 0.5343 |
| B | insider_agg_matrix 字段级 | 同上 `dataset_id="insider_agg_matrix"` | `count=34 / platform_count=34 / complete=true`；`directional_indicator` **cov=1.0**（aCnt 52）、`directional_indicator_2` cov=1.0（23）、`significant_value_1..4` cov=0.5342 |
| C | institutions6 字段级 | 同上 `dataset_id="institutions6"` | `count=11 / platform_count=11 / complete=true`，11 字段全 MATRIX、cov **1.0** |
| D | insiders1 十年跨度 | `get_alpha_yearly_stats("XgaGb3J1")` | **2014–2023 十年逐年 pnl>0**，LC 99–170 / SC 107–187 ⇒ 十年闸可达 |
| E | institutions6 十年跨度 | `get_alpha_yearly_stats("vRA82ogA")` | **2014–2023 十年逐年 pnl>0**，LC 108–182 / SC 121–214 ⇒ 十年闸可达（该件同时含 insd1 与 institutions6 腿） |
| F | sentiment 跨度（**排除依据**） | `get_alpha_yearly_stats("bl6OWZ2M")` | **2014–2018 五年 LC/SC=0、pnl=0**，2019 才有仓 ⇒ sentiment 全家族结构受限（与 `DEU-SENTIMENT-TOWER-DATASPAN-DEAD` 台账一致，本条是我自己实读） |
| G | institutions1 跨度 | `get_alpha_yearly_stats("E56AzejK")` | **2014–2017 四年为零**，2018 起才有仓 ⇒ institutions1 十年闸不可达（非「判死标记」依据，是平台 yearly 实读） |
| H | 预算塔位/RA/设置 | `get_alpha_details("XgaGb3J1" / "0mPKr3bq" / "wpoqZd9l" / "58JxER76" / "vRA82ogA" / "A1x9v2dQ")` | 见 §15.4 与 §15.5 |

### 15.3 数据集分母（唯一合法来源；实取命令逐字）

```
mcp__wq-brain-http__get_datasets(category="insiders",    region="DEU", delay=1, universe="TOP500")  -> count=2
mcp__wq-brain-http__get_datasets(category="institutions",region="DEU", delay=1, universe="TOP500")  -> count=5
mcp__wq-brain-http__get_datasets(category="sentiment",   region="DEU", delay=1, universe="TOP500")  -> count=3
```

| 塔 | 数据集 | 集级 coverage | fieldCount | alphaCount | 本轮处置 |
|---|---|---:|---:|---:|---|
| insiders | **insiders1** | 0.5343 | 8 | 35 | **采用（主）** |
| insiders | insider_agg_matrix | 0.5617 | 34 | 196 | **采用（同族共生腿，不作主）** |
| institutions | **institutions6** | 1.0000 | 11 | 294 | **采用（配对）** |
| institutions | fund_holdings_panel | 0.9019 | 18 | 125 | 不采用（见 15.3.1） |
| institutions | institutions1 | 0.2289 | 7 | 34 | 排除：十年跨度不可达（§15.2-G） |
| institutions | institutions4 | 0.3413 | 6 | 20 | 不采用（6 字段 / cov 0.34 / 无过闸件；**字段级本轮未取**） |
| institutions | institutions25 | **0.0** | 24 | 11 | 不采用：集级 cov=0 是**不可逆硬拦截**；**未做字段级/探针** ⇒ 记「可逆假设」，**不写判死** |
| sentiment | sentiment7 / 27 / 33 | 0.7418 / 0.9038 / 0.3221 | 3 / 18 / 255 | 114 / 390 / 67 | **整塔结构受限，不作目标**（§15.2-F） |

#### 15.3.1 逐集排除理由（判死标记一律不单独作依据）

- **fund_holdings_panel**：台账两条 dead_end（`DEU-FHP-ALLGATE-CLOSED`、`DEU-FHP-SCEILING-DEAD`）**不作依据**；
  本轮的正面依据是——我的只读池扫描（口径：S≥1.58 + 最新回测 `ra_failed_checks` 空 + prod 空或 <0.70 + 未提交，共 313 行）
  里，**含 FHP 字段（`aggregate_*` / `market_value_*` / `quantity_*`）的臂 = 0 条**；且类别参考
  `references/institutions.md` 的 2026-10-04 快照记 94 回测 / 0 条 RA 全过。⇒「有证据的活面」为零，本轮不投。
- **institutions1**：`DEU-INSTITUTIONS1-PROBE-DEAD-20260923` 不作依据；依据是 §15.2-G——它的平台十年曲线 2014–2017 全零。
- **institutions4**：只取到集级 cov 0.3413（平台 `/data-sets`），**字段级未取**，池内零过闸臂 ⇒ 记「未验证的弱面」。
- **institutions25**：集级 cov=0 ⇒ 按纪律这是**不可逆硬拦截**，本轮不采用；但**它不是「没数据」的判据**（反面实证：
  GBR `techindi_model` 集级 cov=0 而真实字段 399 个）。未做字段级/探针 ⇒ 只记 `untested_blind`，不判死。
- **insider_agg_matrix**：`DEU-INSIDER-AGGMATRIX-DEAD`（22 模板、单集上限 0.92）**不作排除依据**——它的
  `significant_value_1..4` 是所有 S≥2.3 臂的核心比值腿、`directional_indicator`(cov=1.0) 是 ACTIVE `Vk65zLzG` 的主腿。
  「单集 ATOM 死」≠「字段不可用」，本轮按共生腿保留。

### 15.4 收割池（RA 全过 / prod 未测或干净 / 未提交；均为平台实读）

**池规模（只读 SQL，`logs/_tmp_s0_harvest_pool.py`，mode=ro）**：全 DEU 313 行；其中含 `insd1_` 116 行、
含 `significant_value_` 87 行、含 `count_institutional_` 6 行。

| alphaId | S / F | 2Y / sub | TO | 塔（平台 `pyramids`） | eff | RA | prod（本地） | 设置 |
|---|---|---|---|---:|---|---|---|---|
| **`XgaGb3J1`** | **2.36 / 2.02** | 2.71 / 1.51 | 17.38% | `[INSIDERS, MODEL]` | **2** | `failed_ra_count=0`、`checks.fail=[]` | **0.6784**（缓存，未 refresh） | decay0/SUBINDUSTRY/trunc0.08/nan ON |
| **`0mPKr3bq`** | 2.36 / 2.04 | 2.67 / 1.54 | 16.40% | `[INSIDERS, MODEL]` | 2 | 同上（RA 全过） | 未测 | 同上 |
| `wpoqZd9l` | 2.36 / 2.04 | 2.67 / 1.54 | 16.40% | `[INSIDERS, MODEL]` | 2 | 同上 | 未测 | 同上 |
| `58JxER76` | 2.36 / 2.02 | 2.71 / 1.51 | 17.38% | `[INSIDERS, MODEL]` | 2 | 同上 | 未测 | 同上 |

- 四条**同源**（`insd1_holdings` + `significant_value_1..4` 比值 + `predicted_surprise_*`/`mean_estimate_change_*`），
  后三条是 `XgaGb3J1` 的几何微调 ⇒ **同族只可能交一颗**（`HARVEST_AUDIT_20261116.md` §二已记 0.906–0.983 的两两相关）。
- **self 本轮未重跑**（v2 记 `XgaGb3J1` self 0.6784242083598276、`0mPKr3bq` 0.6713570156595247）；
  `HARVEST_AUDIT` §五 指出「篮内互相关 0.9936」**复现不出来**、且 `XgaGb3J1` 的篮内相关仍无可信读数 ⇒ 这两项列为本档未验项。
- **塔位增量**：任一条被平台计入 ⇒ **insiders 1/3 → 2/3**（MODEL 已亮，不增值）。
- **不可入池者**：`1YWnZ9rK`(2.64) / `2r5MO67Z`(2.63) / `O0W5JdMg` 等 10 条是 `PV+INSIDERS+MODEL` = **3 塔 eff0**
  （根因 `bucket(rank(cap))` 把 `cap` 挂成 PV），**点塔计数归 0，一律不派**（平台实读 2 条 + code 判 8 条，见 HARVEST_AUDIT §二）。

### 15.5 目标塔 + 配对塔的合规检查（本会话复核）

1. **need 升序第一键打平**：insiders / institutions / sentiment 三座 need 全是 2；不存在「差 1 颗」的塔。
2. **sentiment 被十年闸整体否掉**（§15.2-F：2014–2018 全零）⇒ 倍率 ×1.8 不救它；按任务书「不足 10 年 ⇒ 该塔整体不可作目标」处置。
3. **insiders + institutions 是唯一能「一次提交推两座未亮塔」的组合**，且两类都不在 trio（PV/MODEL/OTHER）内
   ⇒ 不触禁混①②、不占「trio×非 trio ≤5 条」配额。
4. **实现路径有平台实证**：`vRA82ogA` = `[INSTITUTIONS, INSIDERS, ANALYST]` **eff0**（RA 全过、S 2.07/F 1.85/2Y 2.59/sub 1.43、十年全仓）。
   **去掉 `est_12m_ebi_*`（ANALYST）腿 + 不顺带引入 `oth455_*`(OTHER)/`cap`(PV)/MODEL 腿 ⇒ 恰好两塔 `[INSIDERS, INSTITUTIONS]` ⇒ eff2**。
   旁证：`E56AzejK` = `[INSTITUTIONS, OTHER]` eff2 证明两塔生效口径；`A1x9v2dQ` = `[INSTITUTIONS, INSIDERS, OTHER]` eff0 证明多一条腿就归零。
5. **塔归属只认平台 `pyramids[].name`**：`predicted_surprise_*`/`mean_estimate_change_*` → **MODEL**（不是 analyst）；
   `count_institutional_*` → **INSTITUTIONS**；`insd1_*`/`significant_value_*` → **INSIDERS**；`cap` → **PV**（隐形陷阱）。

### 15.6 机制假设（驱动臂表）

**内部人「增持路径」的持续性 × 重要交易的多空构成 × 机构参与广度净扩散**：
`insd1_holdings` 的 66 日变化/信噪比/变更新鲜度刻画内部人信念的持续性，`significant_value_1..4` 的占比刻画
只有「重要交易」才有的方向性信息，`(buyers−sellers)/(buyers+sellers)` 的 22→66 日变化刻画机构参与广度的净迁移；
三者是**不同持仓主体对同一标的的『增持确认』**，同向才有信号，单侧崩塌即失效。

### 15.7 判读基准（regular，无 ATOM 放松）

- **硬线**：S≥1.58、F≥1.0、2Y≥1.58、sub≥1.0、TO 0.01–0.70、margin≥5bp、CW≤0.5；RA `checks.fail` 必须为空。
- **符号指纹（判「机制在」而不是「拟合到」）**：
  ① **单侧取负对称**：把 institutions 腿取负后，|S| 应大体保持、符号翻转（两腿方向都是"增持=好"）；若 |S| 崩到 <0.5×原值 ⇒
  该腿只是方差不是信号，删腿回退到收割路线。
  ② **去腿下探**：只留 insd1 腿应回落到 **≈1.30 上限**（`BE176` 三波 30 臂：insiders1 单集上限 1.30）——回落即证明第二腿真在贡献；
  若两腿都留 S 仍 <1.58 ⇒ 组合几何失效，不是数据没数据。
  ③ **衰减对称**：本族存活件全在 `decay=0`；若 `decay=4` 下 S 掉 >30% ⇒ 信号是快变分量，不得用 decay 4 换稳定。
- **多空宽度**：本族历史 LC/SC 99–182 / 107–214（XgaGb3J1/vRA82ogA 实读）；新臂若宽度掉到 <60/60 ⇒ 覆盖率被 backfill 假填充撑开，不可信。

### 15.8 settingsLine（本族存活配置行）与理由

**`DEU/TOP500/D1/decay0/SUBINDUSTRY/trunc0.08/nanHandling ON/maxTrade OFF/FASTEXPR`**

- 依据 = **平台实读的 6 条存活件设置全同**（`XgaGb3J1`、`0mPKr3bq`、`wpoqZd9l`、`58JxER76`、`vRA82ogA`、`A1x9v2dQ`）：
  `delay 1 / decay 0 / neutralization SUBINDUSTRY / truncation 0.08 / pasteurization ON / unitHandling VERIFY /
  nanHandling ON / maxTrade OFF / language FASTEXPR / 2014-01-01–2023-12-31 / simulationMode FULL`。
- **与区域缺省不同（族特异，不是抄缺省）**：`references/insiders.md` 的区域表是 `decay 4 / nanHandling OFF`，
  但**全部存活臂都是 `decay 0 + nanHandling ON`** ⇒ 本族必须按这条走。原因可解释：insd1 是 VECTOR 事件流、
  coverage 仅 0.5343，`nanHandling ON` 让"当期无申报"落 0 而不是丢样本；`decay 0` 保住 66 日窗口后的快变分量。
- **未做设置扫描**：本轮零配额，`decay 1/2/4` 与 `SUBINDUSTRY→SECTOR/INDUSTRY` 未实测 ⇒ 若要换档，必须先跑一条对照臂。

### 15.9 证据通道与盲区（本档新增部分的通道声明）

| 通道 | 用途 | 盲区 |
|---|---|---|
| `mcp__wq-brain-http__get_pyramid_alphas()` | 塔位/need | 只给当季计数（自然季首日清零）；不分 region 内的 universe；只回 alphas 数，不回是哪些 alpha |
| `mcp__wq-brain-http__get_datasets(...)` | 数据集分母 | 只回**集级** coverage / fieldCount；集级 cov=0 **不能**推出无数据（反面实证 GBR `techindi_model`） |
| `mcp__wq-brain-http__get_datafields(...)` | 字段级可用性 | `search` 只回前 100 命中；本档全部用 `dataset_id` 全量拉取并校验 `complete=true/platform_count` |
| `get_alpha_details` / `get_alpha_yearly_stats` | 塔归属 / RA / 十年跨度 | 只覆盖**平台上存在的 alpha**；`checks.pass` 不回 limit 值；pending 的 SELF/PROD_CORRELATION 不参与判定 |
| 本地 `data/wqb.db` 只读 SQL（`logs/_tmp_s0_harvest_pool.py`） | 历史臂数 / 收割池 | **MCP 直连仿真不写 `expressions` 表**；`alphas.dataset_id` 不可信（本区大量行为 1902）；池只含 S≥1.58 的臂，低于闸的臂在其中不可见 |
| `get_submit_ready` | 提交队列 | 该队列 `prod/self` 多为 null、`towers` 恒为 `[]` ⇒ **不能**判塔、不能判 prod 干净 |

### 15.10 本轮未做 / 未验（不填猜测值）

1. `XgaGb3J1`/`0mPKr3bq` 的 **self 与 prod 未在本会话重跑**（沿用 v2/HARVEST_AUDIT 读数）；prod 缓存值必须 `refresh=True` 终验。
2. `institutions25` 字段级 / 探针、`institutions4` 字段级、`fund_holdings_panel` 字段级：**均未取**。
3. 新双塔臂 `[INSIDERS, INSTITUTIONS]` 的 S 未测——`vRA82ogA` 是 3 塔件（含 ANALYST 腿），去掉该腿后 S 的走向是**未知**，不得当成必然 ≥1.58。
4. 「trio×非 trio ≤5 条」本战役已用条数**未在平台复核**（本地推论 1–4 条，24 条已提交件里 3 条 code 为空）。
5. 设置扫描（decay / 中性化换档）未做；本档 settingsLine 是「存活行」不是「最优行」。

---

## §16 按独立复核意见修订（2026-11-16 23:5x；本节覆盖 §0/§15 的选择结论，§15 保留为过程记录）

> 复核共 12 条问题 + 14 条缺失证据 + 13 条必须修改。逐条处置见 §16.3（采信/未采信/补证）。
> **本节所有新读数都是本会话当场实读**；沿用他人读数的条目逐条标注。

### 16.1 修订后的结论（结构同前）

| 项 | 修订前（§0/§15） | **修订后（本节）** |
|---|---|---|
| 目标塔 | insiders（need 2） | **insiders（need 2）— 不变** |
| 配对塔 | institutions | **留空**（原因见 §16.2-B） |
| 主数据集 | insiders1 | **insiders1**（不变）；`insider_agg_matrix` 仍作同族共腿 |
| 配对数据集 | institutions6 | **留空** |
| 收割池 | 2 条 `[INSIDERS,MODEL]` | **5 条 `[INSIDERS,ANALYST]` 为第一梯队**（self 0.30–0.48 全过），`XgaGb3J1` 降为备选（内部 prod 严线不过） |
| towerGain | 「收割+双塔一次推两座」 | **只承诺第 1 步：insiders 1/3→2/3**；第 2 步（2/3→3/3）**无现存正证据**，列为需新做的工作 |
| 10 条 PV+INSIDERS+MODEL | 全部写「塔位实读」 | **只有 2 条是平台实读，其余 8 条是 code 推断**（§16.3-M8） |

### 16.2 三处必须改选的判断与依据

#### A. 配对塔从 institutions 改为「留空」

| 证据（本会话实读） | 读数 |
|---|---|
| `get_alpha_details("1YWaRlJm")` —— **唯一」合规形"双塔件**（institutions6 只作 `bucket(...)` 分组轴，insd1 作唯一信号腿） | `S 0.82 / F 0.48 / 2Y 0.50 / sub 0.21 / TO 5.59%`；`failed_ra_count=4`（LOW_SHARPE / LOW_FITNESS / LOW_SUB_UNIVERSE / IS_LADDER）；`pyramids=[INSTITUTIONS, INSIDERS] eff2` |
| 本地只读 SQL（`logs/_tmp_s0_pool_v3.py`）全量扫 `institutions6 字段 × insd1 字段` 的 DEU 臂 | **34 条**，S ∈ **[−0.44, 2.07]**、sub ∈ **[−0.12, 1.43]**；其中 **S≥1.58 只有 6 条**，而这 6 条按 code 全是「insd1 + institutions6 + analyst/oth455」**三塔 add 件（eff0）**；两条平台实读确认（`vRA82ogA`=[INST,INS,ANL] eff0、`A1x9v2dQ`=[INST,INS,OTHER] eff0） |
| 平台 `LOW_SUB_UNIVERSE_SHARPE` 限值（1YWaRlJm `checks.fail` 实读） | **0.39**（1YWaRlJm 0.21 未过） |

⇒ 在**合规几何**下 institutions6 作为第二腿的实测上限是 **S 0.82 / sub 0.21**；能过 S 闸的 6 条全是 eff0 三塔。
**且「一条双塔 alpha 是否同时计入两塔的 alphas 计数」未经验证**（`CAMPAIGN_REPORT_INSIDERS_20261116.md:95` 原文）。
两个前提都没站住 ⇒ 本轮不配塔。institutions 的重开条件写死在 §16.4。

#### B. 收割池从 `[INSIDERS,MODEL]` 换成 `[INSIDERS,ANALYST]`

复核要求的 5 条 `[INSIDERS,ANALYST]` 全闸臂，本会话逐条平台实读 + self 实测：

| alpha | S / F / 2Y / sub / TO / margin | 塔（平台） | RA | **self（本会话）** | prod |
|---|---|---|---|---|---|
| **`3q0wVPgz`** | 2.04 / 1.81 / 2.49 / **1.33** / 12.53% / 15.69bp | `[INSIDERS, ANALYST]` eff2 | 0 | **0.3047 PASS** | 未取（槽忙） |
| `VkNV0zqM` | **2.05** / 1.92 / 2.19 / 1.30 / 12.68% / 17.53bp | 同上 | 0 | 0.4665 PASS | 未取（槽忙） |
| `O0WO8zqq` | 1.83 / 1.63 / 2.27 / 1.10 / 10.64% / 18.56bp | 同上 | 0 | 0.4758 PASS | 未取 |
| `GrmPOz05` | 1.79 / 1.41 / 2.66 / 1.02 / 14.09% / 12.40bp | 同上 | 0 | 0.3134 PASS | 未取 |
| `vRA82Ga3` | 1.75 / 1.44 / 2.59 / 1.22 / 10.17% / 16.71bp | 同上 | 0 | 0.3095 PASS | 未取 |

- **五条互相 0.83–0.97**（`compute_mutual_correlation`，4y/1021 点，max_pair `GrmPOz05×vRA82Ga3`=0.969，`max_mutually_below_subset` size=1）⇒ **同族只能交一颗**，首选 `3q0wVPgz`（self 余量最大、sub 最高）。
- **`Vk6eodeb` 实读 self 0.9523 FAIL**（vs `JjxrYjre`）——复核引用的「记录 self 0.6262」是它 vs `Vk65zLzG` 的单点值，**不能**作为入池依据 ⇒ 本轮排除。
- **`[INSIDERS,SHORTINTEREST]` 整族（34 条 S≥1.58 池内臂）self 撞死**：`YPaja5n6` self **0.9160**、`d5a2K72E` self **0.9133**（都撞 ACTIVE `d5a2aO7v`）⇒ 该族不能作为第一步。
- `XgaGb3J1` self **0.6784 PASS**（复跑确认），但 **prod 0.6784 > 内部严线 0.65**（`src/wqb/config.py:532-534` 写明 2026-11-16 用户指令；平台硬线 `PRODCORR_CEILING=0.70` 在 `config.py:512`）⇒ 只能当备选，且动用前须用户 waiver 或改走 0.65 以下件。
- ⚠ **合规警示**：上述 5 条与 `XgaGb3J1` 都是**跨数据集 `add` 型信号腿**（`est_12m_ebi_*` / `predicted_surprise_*` 作为**整腿**累加），与 `insiders.md:55` / `institutions.md:57` 的全局锁定（「禁止两条独立信号腿相加；第二个数据集只以条件/分组/残差入场」）冲突。
  战例：`CAMPAIGN_REPORT_INSIDERS_20261116.md:95` 已用同一纪律把 `Vk6eodeb` 判为「可作塔位备选，但不是可复用配方」。
  ⇒ 本档把它**只当塔位件用**（一次提交、不产配方），并把合规改写列为波内第一条对照（§16.4）。

#### C. FHP 的排除依据整条写错了（复核 M7，已实读更正）

`get_datafields(dataset_id="fund_holdings_panel", region="DEU", universe="TOP500", delay=1)` 实读：**18 个 VECTOR 字段**，是
`boundary_transaction_*` / `herfindahl_index_transactions*` / `large_trade_count_50bps*` / `security_transaction_usd_value*` /
`stable_boundary_trade_count_21d*` / `top_weighted_transaction_number*` / `transaction_account_total*` / `transaction_value_distribution_score*`；
**`aggregate_*` / `market_value_*` / `quantity_*` 是 institutions6 的字段，不是 FHP 的**（§15 归因错误，本节更正）。

FHP 的真实读数（本地只读 SQL，`logs/_tmp_s0_pool_v2.py`）：DEU 全量 **299 条 FHP 臂**，`max S = 1.43`、**S≥1.58 = 0 条**、
`S≥1.0 = 28 条`、`min S = −0.62` ⇒ **「已测弱面」**（不是「0 条臂」）。

### 16.3 复核条目逐条处置

| # | 复核条目 | 处置 |
|---|---|---|
| M1 | 双塔会崩（16 条同配对 S≤0.82/sub≤0.21/全 RA fail） | **采信**：§16.2-A；1YWaRlJm 实读与之逐项吻合 |
| M2 | XgaGb3J1 撞内部 prod 0.65 | **采信**：`config.py:526-534` 实读；改列备选并写明「平台 0.70 可过 / 内部 0.65 不过」 |
| M3 | add 型腿违反全局锁定 | **采信**：`insiders.md:55`/`institutions.md:57` 实读；收割件标注「塔位件、非配方」 |
| M4 | 机制逐腿对应现成腿，不是新机制 | **采信**：§16.5 改写为「单一主信号 + 第二数据集仅分组/条件」的合规形 |
| M5 | towerGain 三步算术崩 | **采信**：改为两步表（§16.4），删掉「再补一颗」的既得能力表述 |
| M6 | 「再补一颗 insiders+MODEL」无来源 | **采信**：五条 ANALYST 件同源 0.83–0.97、SHORTINTER 族 self 0.91 撞死 ⇒ 第二颗无现存来源 |
| M7 | FHP 排除理由错杀 | **采信并更正**：§16.2-C |
| M8 | 10 条 PV 件里 8 条是 code 推断 | **采信**：按 `HARVEST_AUDIT:49` 原话标注 |
| M9 | vRA82ogA 十年不能证明 institutions6 腿 2014–2018 有仓 | **未采信（部分）**：`1YWaRlJm` 是**纯 institutions6 分组 + insd1**，其 `get_alpha_yearly_stats` 未取；但 vRA82ogA 的 `vra82ogA pnl>0 十年`只能证明合并件。**改为待验项**（§16.7-3） |
| M10 | sentiment 排除口径自相矛盾 | **采信并改写**：见 §16.6，并补 `O0Aw3Wkv` 实读 |
| M11 | TB-05 到期条件未写 | **采信**：§16.4 加「仅 2026Q4 成立」 |
| M12 | settingsLine 被选择性样本误导 | **采信**：§16.5 重写为「无单一族特异行 + 必须先跑对照臂」 |
| M13 | 漏掉 5+1 条零仿真候选 | **采信**：已入池并实测（§16.2-B） |

**缺失证据补齐**：5 条 `[INSIDERS,ANALYST]` self ✅（0.30–0.48 全过）；`Vk6eodeb` self ✅（0.9523 FAIL ⇒ 排除）；
`3q0wVPgz` 等 prod ❌（平台单并发槽被 `corr:prod_backfill(xAvMdaOl)` 占用，`check_correlation` 返回 `correlation_busy` retry 240s —— **可用性故障，不是闸门结论**）。

### 16.4 towerGain（修订：只承诺可由既有证据支撑的那一步）

| 步 | 动作 | 前提 | 塔位增量 | 到期 |
|---|---|---|---|---|
| **0** | 对 `3q0wVPgz`（备 `VkNV0zqM`）跑 `check_correlation(refresh=True)` + 用户确认 | prod < 0.65（内部严线）/ 平台 0.70；self 0.3047 已过；篮内互相关未测 | — | 2026Q4 |
| **1** | 提交该件（`[INSIDERS,ANALYST]` eff2，RA 全过，UNSUBMITTED） | — | **insiders 1/3→2/3**；ANALYST 已亮不增值；**不占 trio 配额**（ANALYST/INSIDERS 均非 trio） | 2026Q4 |
| **2** | 再交一颗 insiders 件 → 3/3 点亮 | **无现存正证据**：单集上限 1.30（BE176，ATOM 口径）；`[INSIDERS,SHORTINTEREST]` self 0.91 撞死；`[INSIDERS,MODEL]` 最好 0.6784（内部 prod 不过）；合规双塔 `[INSTITUTIONS,INSIDERS]` ≤0.82 | 2/3→3/3 **未保证** | 2026Q4 |

**★ 时效**：当季计数按自然季清零（TB-05）。以上 1/3→3/3 的推论**只在 2026Q4 成立**；跨到 2027Q1 须按 need=3 重算。
**institutions 重开条件（不配对，但留一条可执行的门）**：只在「设计出一条**非 add** 的新几何」时才值得花臂；首臂止损线 = **S<1.58 或 sub<0.39（平台限值）即停，不派第二批**；派前先跑 `get_alpha_yearly_stats` 确认 2014–2018 有仓。

### 16.5 机制假设 / 判读基准 / settingsLine（修订）

**机制假设（合规形）**：内部人「增持路径」的持续性（`insd1_holdings` 的 66 日变化 / 信噪比 / 变更新鲜度）与重要交易的方向构成（`significant_value_1..4` 占比）合成**同族单一主信号**；
第二数据集**不以信号腿入场**——`institutions6` 只作 `bucket` / `group_rank` 分组轴，`count_institutional_*` 只作**分组值**（家数类在 DEU 是静态结构属性，换手 0.015–0.020，`institutions.md:94-95` 明令不可当主信号）。

**判读基准（口径更正）**：
- 平台实读限值（`1YWaRlJm` 的 `checks.fail` 原文）：`LOW_SHARPE limit 1.58`、`LOW_FITNESS limit 1.0`、`LOW_SUB_UNIVERSE_SHARPE limit 0.39`、`IS_LADDER_SHARPE limit 1.58`。
- 内部严线（`config.py:526-534`）：S 1.58 / F 1.0 / TO 0.05–0.20 / margin 10bp / self 0.50 / **prod 0.65**。ask 给的 sub≥1.0 是**内部线**，平台线是 0.39。
- `CONCENTRATED_WEIGHT` 平台 limit = **0.10**（HARVEST_AUDIT §二/§四）。
- **pending 必须终验**：`SELF_CORRELATION` / `DATA_DIVERSITY` / `PROD_CORRELATION` / `REGULAR_SUBMISSION` 在平台 checks 里全是 pending，提交前必须逐项拿到终值。
- 符号指纹：①第二腿取负后 |S| 保持、符号翻转，崩到 <0.5×原值 ⇒ 该腿是方差不是信号；②只留 insd1 腿应回落至 **≈1.30（BE176 的 ATOM 单集上限，不作 regular 单腿基准）**；③**decay 不是族特异常量**——存活件横跨 decay 0/2/4/8（XgaGb3J1=0、gJaYeV9g=2、GrmqgQK5/Vk6eodeb=4、YPaja5n6=8），必须做对照而不是锁定；④LC/SC 宽度应维持 99–182 / 107–214，<60/60 即 backfill 假填充。

**settingsLine（修订：不给"唯一存活行"）**：
`DEU/TOP500/D1/decay{0|2|4|8}/SUBINDUSTRY/trunc0.08/nanHandling{ON|OFF}/maxTrade OFF/FASTEXPR`
—— 理由：平台实读的 6 条我读过的件（XgaGb3J1/0mPKr3bq/wpoqZd9l/58JxER76/vRA82ogA/A1x9v2dQ）确实逐项同为 `decay0+SUBINDUSTRY+trunc0.08+nanHandling ON`，
但**同族同闸的另外三条是反例**：`Vk6eodeb` decay4/**nanHandling OFF**、`d5a2aO7v`(ACTIVE) decay8、`Vk65zLzG`(ACTIVE) decay4/nanHandling OFF（S0 §8 表实读）。
⇒ 这 6 条是**选择性样本**，不能支持"族特异设置"。开波必须先跑 `decay 0/4/8 × nanHandling ON/OFF` 六格对照（6 条仿真），再谈设置。

### 16.6 sentiment 与 institutions25：改判为「可逆假设」（不写"整塔结构受限"）

| 集 | 平台 yearly 实读 | 结论口径 |
|---|---|---|
| sentiment7/27 | `bl6OWZ2M`（ACTIVE）：2014–2018 LC/SC=0、pnl=0；2019 起有仓；2020 pnl −7823 | 该件 5 年零仓 |
| sentiment33 | `O0Aw3Wkv`（本会话实读）：2014–2017 pnl=0 且 LC/SC=0；**2018 pnl 96.2 万但 LC/SC=0**；2019 LC 6/SC 9 | 2018 起才有数据 |
| 反向证据 | **ACTIVE `bl6OWZ2M` 同样五年空白却被平台接受**（S0 §7.4:265 原文：「该条不用于排除 sentiment」） | 平台未执行"近十年"硬闸 |

⇒ 修订为：**「按 ask 的十年硬规则，sentiment 本轮不作目标塔；但这是可逆假设，不是结构死。」** 若用户放宽该规则或愿意接受 5–6 年样本，sentiment 可重开（其 `kqNRX1ZP` S 2.06 另被 self 0.7936 撞 `bl6OWZ2M` 否掉）。

institutions25 同理：**字段级 24/24 cov=0.0（`platform_count=24`，S0:175 实读）+ 集级 0.0 + 本地 33 条 `inst25_*` 臂 max|S|=1.22** ⇒ 仍**不判死**；处置 = 「待 `tools/probe/dataset_data_probe.py` 一条最小探针」，本轮不采用。
institutions4：字段级 6/6 VECTOR cov 0.3413（S0 §4.2 实读，本节未重跑）。

### 16.7 仍未验 / 仍缺（不填猜测值）

1. `3q0wVPgz` / `VkNV0zqM` 的 **prod 未取**（`correlation_busy`，持有者 `corr:prod_backfill(xAvMdaOl)`）——不是闸门结论。
2. 五条 `[INSIDERS,ANALYST]` 与已提交篮的**篮内互相关**未测（只知道它们彼此 0.83–0.97）。
3. `1YWaRlJm`（纯 institutions6 分组形）的 `get_alpha_yearly_stats` 未取 ⇒ institutions6 腿 2014–2018 是否有仓**仍未知**。
4. `institutions6` 的 `aggregate_*` 作为**非 bucket** 的分组/条件用法未测（只在 1YWaRlJm 见过 bucket 形）。
5. 10 条 PV+INSIDERS+MODEL 中 8 条的 `pyramids` 未逐条实读（code 推断）。
6. `trio×非 trio ≤5 条` 本战役累计未在平台复核；本修订已**改用 ANALYST 腿绕开该配额**，但若后续回到 MODEL 腿仍需先核。
7. 设置六格对照未跑（§16.5）。
8. 「一条双塔 alpha 是否同时计入两塔计数」未验证（`CAMPAIGN_REPORT_INSIDERS_20261116.md:95`）。
