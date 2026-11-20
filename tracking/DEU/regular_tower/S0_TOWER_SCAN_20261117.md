# S0 塔位与数据集盘点 — DEU / TOP500 / D1（2026-11-17）

> 范围：`region=DEU, universe=TOP500, delay=1`，regular（无 ATOM 放松）。
> 本档零提交、零仿真派发、零写库；塔位/数据集/字段/年度/相关性读数均为**本轮平台或本地只读实读**，
> 逐条注明命令；沿用他人读数的条目**单独标注**，不与本轮实读混写。
> 覆盖上一版 `S0_TOWER_SCAN_20261116.md`（该版 §0/§15/§16 的结论本节按新读数更新，§14 差异见本档 §13）。

---

## §0 结论摘要

| 项 | 结论 |
|---|---|
| **目标塔** | **insiders**（DEU/D1 当季 **1/3**，差 **2** 颗，`pyramidMultiplier=1.6`；平台实读） |
| 配对塔 / 配对数据集 | **留空**（理由见 §5：唯一实测合规 bucket 形 `[INSTITUTIONS,INSIDERS]` S 0.82 / sub 0.21；`risk60` 只登记为**保留备选**，本轮不作配对） |
| **主数据集** | **`insiders1`**（8 字段全 VECTOR，字段级 cov 0.5343；单集 ATOM 上限 ≈1.30 已由 3 波 30 臂收敛） |
| 同塔第二腿 | `insider_agg_matrix`（34 字段；`directional_indicator` / `_2` 字段级 **cov=1.0**，平台实读） |
| **收割池** | **非空，7 条**（RA 全过、prod 未测或已测<0.70、未提交）：第一梯队 **5 条 `[INSIDERS,ANALYST]`**（S 1.75–2.05，**本轮实测 self 0.30–0.48 + prod 0.45–0.52，全部过内部线**），第二梯队 2 条 `[INSIDERS,MODEL]`（S 2.36，但 self 0.67 撞内部 0.50 线） |
| **一次提交的塔位增量** | **insiders 1/3 → 2/3**（收割 5 条中任一提交；MODEL/ANALYST 已点亮，不计增量）。2/3→3/3 需新波，见 §12 |
| 偏离 need 次序 | 有：sentiment（×1.8，need 2）被**十年跨度**整体否掉（平台 yearly 实读，§2.2） |

---

## §1 塔位实读（权威 = 平台 `get_pyramid_alphas` 当季）

**实读命令**：`mcp__wq-brain-http__get_pyramid_alphas()`（无参数 = 当季；返回体按 `region → delay → category` 分档）。

DEU **D1** 实读（16 类）：

| category | alphas | need(=3−alphas) | 点亮 | 平台 `pyramidMultiplier`（`get_datasets` 实读） |
|---|---:|---:|:---:|---:|
| analyst | 6 | 0 | ✅ | 1.8 |
| shortinterest | 5 | 0 | ✅ | 1.3（ask 表同值） |
| fundamental | 3 | 0 | ✅ | 1.8 |
| model | 3 | 0 | ✅ | 1.8 |
| other | 3 | 0 | ✅ | 1.8 |
| **sentiment** | **1** | **2** | ❌ | **1.8** |
| **insiders** | **1** | **2** | ❌ | **1.6** |
| **institutions** | **1** | **2** | ❌ | **1.6** |
| news | 0 | 3 | ❌ | 1.8 |
| option | 0 | 3 | ❌ | 1.7 |
| pv | 0 | 3 | ❌ | 1.6 |
| earnings | 0 | 3 | ❌ | 1.5 |
| macro | 0 | 3 | ❌ | 1.5 |
| risk | 0 | 3 | ❌ | 1.5 |
| socialmedia | 0 | 3 | ❌ | 1.5 |
| imbalance | 0 | 3 | ❌ | 1.2 |

- **DEU D0 全 0**（非本战役口径；只取 `DEU.D1`，不跨 delay 求和——历史盲区 `pull_pyramid()` 形态 B 曾跨 delay 求和）。
- **与 ask 给定 CLI 表的差异：无**。16 类 `alphas` 值逐项一致；`campaign_intel.py pyramid` 的 1h sqlite 缓存本轮**未出现**漂移，故无需以 MCP 覆盖 CLI。
- **need 全表不存在 `need=1` 的塔**：5 座 `need=0`、3 座 `need=2`、8 座 `need=3`。
- **当季口径**：`get_pyramid_alphas()` 缺省取当前季度 ⇒ 本档全部「1/3→3/3」推论**只在 2026Q4 成立**（TB-05，`docs/time_bombs.json:75`，date=2026-12-31，owner=user，status=pending）。TB-05 自带的平台实测证据：`get_pyramid_alphas(2026-07-01~09-30)` DEU fundamental=**0** vs `(2026-10-01~11-15)` fundamental=**2** ⇒ **季度清零真实存在**。**Q3 提交件不计入**——例：`Vk65zLzG`（`[INSIDERS,MODEL]` eff2）`dateSubmitted=2026-09-13T01:32:32-04:00`（本轮 `get_alpha_details` 实读），不在当季计数内。
- **当前 insiders 的 1 最可能对应**：`d5a2aO7v`（`DEU_R_shrtinsd_02`，**ACTIVE**，`dateSubmitted=2026-11-12T23:54:47-05:00`，`pyramids=[DEU/D1/SHORTINTEREST, DEU/D1/INSIDERS]` eff2，S 1.66 / F 1.36 / 2Y 2.58 / sub 0.92，平台实读）。**当前 institutions 的 1 最可能对应**：`2rmGAPqN`（`DEU_R_insconviction_01`，ACTIVE，`dateSubmitted=2026-10-09`，`pyramids=[DEU/D1/INSTITUTIONS, DEU/D1/OTHER]` eff2，prod 0.6292 / self 0.0327，平台实读）。
  ⚠ **这是推断不是平台明示**：`get_user_alphas(stage="OS", region="DEU")` 本轮**30s 超时（工具故障，不作证据）**，无法穷举 Q4 全部提交件；只能确认这两件在 Q4 且各带一座未亮塔。

---

## §2 目标塔选定

### 2.1 排序键（按 ask）：need 升序 → 倍率 → 可挖面宽窄

三座未亮塔 need 全部 = 2 ⇒ 第一键打平。按倍率：sentiment 1.8 > insiders 1.6 = institutions 1.6。

### 2.2 为什么不是 sentiment（倍率最高）

**平台 `get_alpha_yearly_stats` 实读（本轮）**：

| 件 | 数据集 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 结论 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `bl6OWZ2M`（ACTIVE，`[SENTIMENT]` eff1） | sentiment7/27 | pnl 0 / LC 0 / SC 0 | 0 | 0 | 0 | 0 | 首次 996,227（LC 84 / SC 82） | **前 5 年零仓** |
| `O0Aw3Wkv`（前序实读，未复跑） | sentiment33 | pnl 0 / LC 0 | 0 | 0 | 0 | pnl 96.2 万但 LC/SC=0 | LC 6 / SC 9 | 2018 起才有数据（6 年样本） |

⇒ 按 ask「不足 10 年 ⇒ 记『结构受限：近十年闸不可达』，该塔整体不可作目标」，**sentiment 本轮不作目标**。
此结论是**可逆假设**（用户放宽十年约束即可重开）：平台曾接受 5 年空窗的 `bl6OWZ2M`，说明平台未执行十年硬闸；本档只按 ask 口径执行。另 sentiment 主面（`snt7`×`snl27`）已被 ACTIVE `bl6OWZ2M` 占位、次强 `GrWVx2aO` self 0.8419 FAIL（前序实读），本轮未复测。

### 2.3 为什么不是 institutions

- `insiders1` 之外的 institutions 数据面：`fund_holdings_panel` 本地 `get_mining_yield` 实读 **94 backtested / 0 ra_clean**；`institutions25` 集级+字段级 cov 全 0.0；`institutions4` 6 字段 / 集级 0.3413；`institutions6` 全宽度但**合规 bucket 形实测上限 S 0.82 / sub 0.21**（`1YWaRlJm`，本轮平台实读，见 §5）。
- `institutions1` 十年跨度不可达（`E56AzejK` 2014–2017 LC/SC/pnl 全 0，本轮平台实读），且其唯一有效族已被 ACTIVE `2rmGAPqN` 占位、后继 self 0.92+（台账）。
⇒ institutions **不作目标塔**，仅评估作配对（§5）。

### 2.4 为什么是 insiders

1. **唯一有「零仿真即可推进」的未亮塔**：7 条 RA 全过 / prod 未测或 <0.70 / 未提交件（§9），且第一梯队 5 条的 **self 与 prod 已在本轮前被刷成新鲜值且全部过线**（06:32–09:10，见 §9.2）。
2. **单集 ATOM 已证不可行 ⇒ 跨集兜底有据**：`insiders1` 单集 S 上限 ≈**1.30**（BE172/174/176 三波 30 臂收敛：1.22 / 1.30 / 1.19），`insider_agg_matrix` 单集 ≈**0.93**（22 模板），均 < 1.58 ⇒ 按 2026-11-17 ATOM 政策，**满足「ATOM 已穷尽」条件**，允许限定形态的跨集。
3. **有平台实读的最强臂**：现存 S 2.36 的两件核心腿正是 `insd1_holdings` + `significant_value_1..4`（§9）。
4. **十年跨度通过**：`3q0wVPgz` 2014–2023 逐年 `pnl>0`、LC 104–170 / SC 121–225（§9.3）。

---

## §3 数据集分母（唯一合法来源 = 平台 `/data-sets`，按 region/universe/delay 实取）

**实取命令（逐字）**：

```
mcp__wq-brain-http__get_datasets(category="insiders",     region="DEU", delay=1, universe="TOP500")  -> count=2
mcp__wq-brain-http__get_datasets(category="institutions", region="DEU", delay=1, universe="TOP500")  -> count=5
mcp__wq-brain-http__get_datasets(category="sentiment",    region="DEU", delay=1, universe="TOP500")  -> count=3
mcp__wq-brain-http__get_datasets(category="news",         region="DEU", delay=1, universe="TOP500")  -> count=17
mcp__wq-brain-http__get_datasets(category="option",       region="DEU", delay=1, universe="TOP500")  -> count=1
mcp__wq-brain-http__get_datasets(category="pv",           region="DEU", delay=1, universe="TOP500")  -> count=16
mcp__wq-brain-http__get_datasets(category="earnings",     region="DEU", delay=1, universe="TOP500")  -> count=2
mcp__wq-brain-http__get_datasets(category="macro",        region="DEU", delay=1, universe="TOP500")  -> count=1
mcp__wq-brain-http__get_datasets(category="risk",         region="DEU", delay=1, universe="TOP500")  -> count=5
mcp__wq-brain-http__get_datasets(category="socialmedia",  region="DEU", delay=1, universe="TOP500")  -> count=2
mcp__wq-brain-http__get_datasets(category="imbalance",    region="DEU", delay=1, universe="TOP500")  -> count=1
```

### 3.1 目标塔 insiders 分母 = **2 集**

| dataset | name | 集级 coverage | fieldCount | userCount | alphaCount | pyramidMultiplier |
|---|---|---:|---:|---:|---:|---:|
| insider_agg_matrix | Smart Insider Transaction Aggregates | 0.5617 | 34 | 103 | 196 | 1.6 |
| **insiders1** | Global Insider Trading Data | 0.5343 | 8 | 22 | 35 | 1.6 |

### 3.2 字段级实读（`get_datafields` dataset 全量 + `sort_by=dateCreated` + `min_coverage=0.8`）

> 注：`sort_by` / `sort_order` / `min_coverage` 在 `LocalToolSearch` 返回的 schema 里**未列出**，但服务端实现支持
> （`world-quant-brain-mcp/tools_data.py:108-164` 的 `_order_fields`），本轮实调**成功**并在返回体回显
> `sorted_by:"dateCreated", sort_order:"desc", min_coverage:0.8` ⇒ 读数有效。

| dataset | 全量字段 | dateCreated 范围 | cov≥0.8 字段数 | cov≥0.8 的字段 | 说明 |
|---|---:|---|---:|---|---|
| **insiders1** | 8 / `complete=true` | 全 **2026-07-01** | **0** | — | 8/8 VECTOR，字段级 cov 全 = 0.5343（**该列在本集是集级值复制，不携带字段级信息**）；6 个数值字段 + 2 个标识符 |
| **insider_agg_matrix** | 34 / `complete=true` | 全 **2026-07-01** | **2** | `directional_indicator`（cov **1.0**, aCnt 52）、`directional_indicator_2`（cov **1.0**, aCnt 23） | 其余 32 字段 cov 0.5342–0.5344 |

- **新鲜度结论**：DEU 全部相关数据集的 `dateCreated` 都是 **2026-07-01**（同一批 onboard）⇒ **本区不存在「老集里新 onboard 字段」的白空间线索**；`alphaCount` 极低 + dateCreated 旧的「死字段」判据在本区无从区分。
- `insider_agg_matrix` 的 `directional_significant_value_1..3` / `top_directional_significant_value_4` 的 `userCount=0, alphaCount=0`（平台实读）——**全平台无人用**，属高风险字段，不作首选。
- 15 个 `avg_*` / `total_*` shares 字段（cov 0.5344）与 `significant_value_1..4` / `top_*`（cov 0.5342）是同一记录的不同投影。

---

## §4 逐集采用/排除理由（判死标记一律不单独作依据）

### 4.1 insiders（分母 2）

| dataset | 处置 | 理由 |
|---|---|---|
| **insiders1** | **采用（主集）** | ① 字段级 6 个可用数值字段（holdings / valueeur / value / shares / price / tradesignificance），另 2 个是标识符；② 单集 ATOM 上限 ≈1.30（BE176 三波 30 臂），**但它是现存 S≥1.75 全部件的核心腿**；③ 原始 `vec_*` 换手 1.62–1.79（硬线 0.70），**必须 `ts_backfill(250)` 才降到 0.011–0.034**（`FIELD_insiders1_20261116.md` §0/§4.2）；④ 无买卖方向字段、数值符号不带方向 ⇒ 方向只能由 `insd1_holdings` 时间差分或双向对照臂确定；⑤ 十年跨度实测通过（§9.3）。 |
| insider_agg_matrix | **采用（同塔第二腿，不作 ATOM 主集）** | ① 单集 22 模板上限 0.92–0.93（`BE176` / `DEU-INSIDER-AGGMATRIX-DEAD`）；② 但 `directional_indicator` / `_2` 字段级 **cov=1.0**、alphaCount 52/23，且 `directional_indicator` 是 ACTIVE `Vk65zLzG` 的主腿（平台实读 code 首项）⇒ **「单集 ATOM 死」≠「字段不可用」**；③ `significant_value_1..4` 是 S≥2.3 臂的比值腿。死档「`directional_indicator` 零持仓」与实测（cov 1.0 / aCnt 52/23）相反，**不采信**。 |

### 4.2 sentiment（分母 3）— 整塔本轮不作目标

| dataset | 集级 cov | fieldCount | 处置 |
|---|---:|---:|---|
| sentiment27 | 0.9038 | 18 | 十年跨度（`bl6OWZ2M` 2014–2018 零仓，§2.2） |
| sentiment33 | 0.3221 | 255 | 十年跨度（`O0Aw3Wkv` 2014–2017 零仓 / 2018 LC-SC=0） |
| sentiment7 | 0.7418 | 3 | 十年跨度同上；且脉冲面独立判死（48 探针天花板 0.71，台账） |

### 4.3 institutions（分母 5）

| dataset | 集级 cov | 字段 | 处置 |
|---|---:|---:|---|
| **institutions6** | 1.0 | 11（全 MATRIX，字段级 cov **全 1.0**） | **保留为分组轴证据/配对备选**；`1YWaRlJm` 实测 S 0.82 / sub 0.21 / 4 项 RA fail ⇒ **不足以推进塔位**；**十年跨度实测通过**（`1YWaRlJm` 2014–2023 逐年有仓，本轮实读——更正上一版「未取」） |
| fund_holdings_panel | 0.9019 | 18 | 不投：`get_mining_yield` **94 backtested / 0 ra_clean**（conv 0.743） |
| institutions1 | 0.2289 | 7 | 不投：`E56AzejK` 2014–2017 LC/SC/pnl 全 0（十年跨度） |
| institutions4 | 0.3413 | 6 | 不投：本轮未取字段级、池内无过闸臂 ⇒ **弱面/未验证**，不判死 |
| institutions25 | **0.0** | 24 | 不投：集级 cov=0 + **字段级 24/24 cov=0.0**（`platform_count=24` 实读）⇒ 不可逆硬拦截；**未跑探针，不判「无数据」**，记可逆假设 |

### 4.4 其余未亮塔（本轮全部不投，逐集依据见 `excluded` 数组）

- **news（17 集）**：6 个 cov>0.6 的集（news104/17/18/20/38/50）本地 `get_mining_yield` 逐集 **0 ra_clean**；11 个集 cov=0 或未测。另 `references/news.md` §终局记录换手结构性冲突（TO 0.17–0.43）与 news104 max 0.05。
- **option（1 集）**：option1 集级 0.0 + 字段级 22/22 cov 0.0（`min_coverage=0.8` 返回 0/22）⇒ 硬拦截；未探针。
- **pv（16 集）**：pattern_scores / continuation_score / intraday_pv_feats / pv106 / pv109 均有实测上限（0.23–1.38，全部 <1.58）；pv1 核心价量 `alphaCount=15192`（全平台犁过）；PV 属 trio，不作本轮配对。
- **earnings（2 集）**：两集集级 cov 均 0.0；earnings6 覆盖放宽实测 best S≈0.6。
- **macro（1 集）**：macro27 集级 0.0 + 字段级 **13/13 cov 0.0**（0/13）；**无任何判死记录**，平台 `alphaCount=177 / userCount=82` ⇒ **未测盲区**，需探针才可动。
- **risk（5 集）**：risk60 单信号取反最好 S 0.62（12 臂探针）；risk68 beta 0.20；risk71 残差动量负；risk72 12/12 负、翻转上限 0.76；risk88 仅 1 个市值字段。
- **socialmedia（2 集）**：socialmedia12 集级 0.0；socialmedia39 仅 1 字段（共搜结构）。
- **imbalance（1 集）**：imbalance5 集级 0.0 / 2 字段；`imb5_score` 近静态 S 0.24 / 2Y −0.55。

**⇒ 是否还有其他值得开的目标塔：有，但全部 need=3、优先级低于 insiders**。按证据强弱：
① `macro27`（DEU/D1 唯一 macro 集，13 字段，**无任何判死记录**，平台 alphaCount 177 / userCount 82；但字段级 13/13 cov 0.0 ⇒ 必须先跑 `tools/probe/dataset_data_probe.py` 一条最小探针）；
② `option1`（22 字段，字段级全 0.0，同样需探针；无判死记录）；
③ `risk68` 的 3 个未测字段（`rsk68_weight_volatility_short` / `rsk68_residual_return` / `rsk68_weight_edadv`，台账另记）；
④ `pv20` 流动性面（`average_daily_value_20d_usd` S 1.03 / `adv20_usd_capped_100m` S 0.95 / 2Y 1.28，`COVERAGE_RELAX_EARNINGS6_PV20_20261111.md` 台账；PV 属 trio，配额受限）。
以上均**未在本轮取得字段级可用证据**，不作采用。

---

## §5 配对塔评估（结论：partner 留空）

### 5.1 合规检查

| 规则 | 本组合 |
|---|---|
| ① 禁 PV+MODEL / PV+OTHER / MODEL+OTHER / PV+PV / MODEL+MODEL / OTHER+OTHER | INSIDERS × 任一未亮塔均不触（INSIDERS 不在 trio） |
| ② trio 某类 + 非 trio 类累计 ≤5 | 本档不涉 trio ⇒ 不消耗配额 |
| ③ 任何 ≥3 塔同现 ⇒ 归 0 | **红线**：收割件 `[INSIDERS,ANALYST]` / `[INSIDERS,MODEL]` 已是两塔；**任何在其上再加第三塔的改写一律不派**（历史实证：`1YWnZ9rK` 因 `bucket(rank(cap))` 变 `[PV,INSIDERS,MODEL]` eff0；`vRA82ogA` 因 `est_12m_ebi_*` 变三塔 eff0） |
| ④ 塔归属以平台 `pyramids[].name` 为准 | 是（§9.1 逐件实读） |
| ⑤ 单两塔组合 ≤3 | 本档未新增；`[INSIDERS,MODEL]` 的历史条数两套口径未对齐（前序 1–4 条），**开波前必须平台复核** |

### 5.2 候选配对逐条评估

| 配对候选 | 塔 | 平台证据 | 结论 |
|---|---|---|---|
| **institutions × institutions6（bucket 分组轴）** | institutions（1/3） | `1YWaRlJm`：`group_rank(ts_sum(divide(vec_max(insd1_valueeur), vec_sum(insd1_valueeur)),66), bucket(rank(ts_backfill(divide(aggregate_equity_value_institutions, aggregate_equity_value_all_owners),252)), range="0,0.5,1"))` → `pyramids=[DEU/D1/INSTITUTIONS, DEU/D1/INSIDERS]` **eff2**；S **0.82** / F 0.48 / 2Y 0.50 / sub **0.21** / TO 5.59%；**4 项 RA fail**（LOW_SHARPE / LOW_FITNESS / LOW_SUB_UNIVERSE / IS_LADDER）；十年逐年有仓（2014–2023）。**同时证明「bucket-only 第二数据集照计第二塔」** | **不配**：实测上限远低于 1.58，不可能推进塔位 |
| **risk × risk60（bucket/trade_when 分组轴）** | risk（0/3） | `kqarVldO`：`group_rank(ts_zscore(vec_avg(rsk60_offer),252),industry)` → `pyramids=[DEU/D1/RISK]` **eff1**、mult 1.5；LC **153**/SC **214**、TO 9.69% ⇒ 数据真实；但 S **−0.92**（取反后最好 +0.62，12 臂探针） | **保留备选，不配**：作为分组轴本身不需要 S，但「insd1-only + bucket」的**唯一实测类比就是 0.82**（上一行）⇒ 没有证据能到 1.58 |
| macro × macro27 | macro（0/3） | 13/13 字段 cov 0.0（`min_coverage=0.8` 返回 0/13） | 不配：全 NaN 字段无法作 bucket 轴 |
| option × option1 | option（0/3） | 22/22 字段 cov 0.0（0/22） | 不配：同上 |
| imbalance × imbalance5 | imbalance（0/3） | 2 字段 cov 0.0；`imb5_score` 近静态 | 不配：同上 |
| news × news104/17/18/20/38/50 | news（0/3） | cov 0.60–0.96 但 6 集 0 ra_clean；换手结构冲突 | 不配：无活面证据 |

### 5.3 ATOM 政策与配对的冲突及处置

ask §3 要求「本轮 ATOM 优先，跨集只在 ATOM 已穷尽时作兜底」；ask §4 要求评估配对（本质是跨集）。
**处置**：`insiders1` 的单集 ATOM 已由 **3 波 30 臂**收敛到 1.30（BE172/174/176），`insider_agg_matrix` 22 模板收敛到 0.93 ⇒ **ATOM 已穷尽成立**，允许跨集兜底。但兜底形态限定 `gating / grouping / residual / ratio`，**不含加法腿** ⇒ 现存 `[INSIDERS,ANALYST]` / `[INSIDERS,MODEL]` 的 `add(...)` 结构**只能作塔位件，不能作新波配方**（前序 §16 同结论）。

⇒ 新波第一优先应是 **同塔跨集**（`insiders1` × `insider_agg_matrix`，用 ratio / gating / grouping / residual），它只推进 insiders 一颗；**不把第二座塔写进 design**，故 partner 留空。

---

## §6 机制假设（驱动臂表）

> **内部人「增持路径」的持续性，只在「重要交易占比高」的截面里携带方向信息；且其信号强度受做空约束（借券费率）条件化。**
> `insd1_holdings` 的 66 日变化 / 信噪比 / 变更新鲜度刻画内部人信念的持续性（`ts_delta` / `ts_ir` / `reverse(days_from_last_change)`）；
> `significant_value_1..4` 的占比刻画「只有重要交易才有的方向信息」（同一记录族，属同一塔）；
> 两者按 `ratio` 或 `gating` 组合（**不做加法相加**），分组轴用 `sector` 或 `bucket(rank(insd1 侧派生))`。
> 可证伪点：
> 1. **去腿下探**：只留 `insd1_holdings` 单腿应回落到 ≈1.0–1.30（BE176 的 ATOM 区间）；若回落至 <0.6 ⇒ 第二腿只是方差。
> 2. **符号指纹**：整式取反；`S(−expr) ≈ −S(expr)`（差 <0.03）且 TO/DD/LC 逐位相同 ⇒ 方向层无净信息，停。
> 3. **换手是入场条件**：裸 `vec_*` TO 1.6–1.8 ⇒ 必须先 `ts_backfill(250)`；任何臂 TO >0.7 直接判表达层错误（不是信号死）。
> 4. **费率条件化（仅作备选探针）**：`bucket(rank(vec_avg(ts_backfill(rsk60_offer,66))))` 分组后，若两桶的 S 方向相反且单调 ⇒ 轴有信息；若各桶与裸跑逐位相同 ⇒ 轴无信息（参照前序 bucket 壳「S +0.01 / 2Y −0.33」的空壳指纹）。

**★ S 面怎么上 1.58（本轮必须回答的问题）**：DEU 历史上的 S 面弱（`fnd72` 三波 best 0.68、`insiders1` ATOM 1.30），而 **S≥1.75 的全部现存件都是「insd1 核心 + 第二个强腿」**（ANALYST 腿 1.75–2.05、MODEL 腿 2.36）。⇒ 新波的核心假设是：**把第二腿从「加法腿」换成合规的 `ratio` / `gating` 入口，同时保住 S 面**。如果合规形态无法保住 ≥1.58，则本塔 3/3 在本季度不可达，应记录为**配置层/表达层受限**，不得写成数据层判死。

---

## §7 判读基准（regular，无 ATOM 放松）

### 7.1 硬门槛（平台实读优先）

| 轴 | 线 | 来源（本轮实读） |
|---|---|---|
| Sharpe | ≥ **1.58** | `1YWaRlJm` `checks.fail`：`{name:LOW_SHARPE, value:0.82, limit:1.58}` |
| Fitness | ≥ **1.0** | 同上 `{LOW_FITNESS, 0.48, limit:1.0}` |
| Two-year Sharpe | ≥ **1.58** | 同上 `{IS_LADDER_SHARPE, value:0.5, limit:1.58, year:2}`；`kqarVldO` 另有 `{LOW_2Y_SHARPE, value:-1.14, limit:1.58}` |
| sub_universe_sharpe | 平台线 **0.39**（逐臂）；ask/内部线 **1.0** | `1YWaRlJm` `{LOW_SUB_UNIVERSE_SHARPE, 0.21, limit:0.39}` |
| Turnover | **0.01–0.70**（平台）；内部 **0.05–0.20** | `tracking/DEU/config/thresholds.json`；`src/wqb/config.py` `GATES_INTERNAL` |
| Margin | 平台 **5bp**（`0.0005`）；内部 **10bp** | `thresholds.json`；`config.py:524-534` |
| CONCENTRATED_WEIGHT | 本地 **0.5**；平台 limit **0.10** | `thresholds.json`；台账实测 |
| self / prod | 平台 **<0.70**；内部 **self<0.50 / prod<0.65** | `src/wqb/config.py:512` `PRODCORR_CEILING=0.70`；`config.py:524-534`（2026-11-16 用户指令） |
| RA 层 | `failed_ra_count=0` 且 `checks.fail=[]` | `src/wqb/config.py` `RA_CHECK_NAMES` |

⚠ 平台 `LOW_SHARPE` 的 limit 在 DEU/D1 实读为 **1.58**（不是 `config.PLATFORM_CHECK_LINES` 的 delay1 默认 1.25）——以**逐件 fail payload** 为准。

### 7.2 符号指纹（判「机制在」vs「符号错」）

| 检验 | 读法 |
|---|---|
| **镜像对称** | 同式取反重跑；`S(−expr) ≈ −S(expr)`（差 <0.03）且 TO/DD/LC 逐位相同 ⇒ 方向层无净信息、机制不在，停。两向不对称（\|S+\|−\|S−\| >0.1）⇒ 机制在、取强侧 |
| **去腿下探** | 去掉第二腿应回落 ≈1.0–1.30（BE176）；若全式 S 低于去腿版 ⇒ 第二腿在稀释 |
| **衰减梯** | 平滑窗 22 → 66 → 132 应单峰；单调/随机 ⇒ 结构没对上 |
| **decay 对称** | 本族存活件的 decay 横跨 0/4/8（`XgaGb3J1`/5 条 ANALYST=0、`Vk65zLzG`=4、`d5a2aO7v`=8）⇒ **decay 不是族特异常数**；若 decay4 相对 decay0 掉 >30% ⇒ 信号是快变分量，不得用 decay4 换稳定 |
| **宽度** | 存活件 LC/SC 99–182 / 107–214；<60/60 ⇒ backfill 假填充 |

---

## §8 settingsLine（本族存活配置行）与理由

```
DEU/TOP500/D1/decay0/SUBINDUSTRY/trunc0.08/nanHandling ON/maxTrade OFF/FASTEXPR
```

**依据（本轮平台实读的 7 件，设置逐项相同）**：

| 件 | 状态 | decay | 中性化 | trunc | nanHandling | S / F / 2Y / sub / TO / margin |
|---|---|---:|---|---|---|---|
| `3q0wVPgz` | UNSUBMITTED | **0** | SUBINDUSTRY | 0.08 | ON | 2.04 / 1.81 / 2.49 / 1.33 / 12.53% / 15.69bp |
| `VkNV0zqM` | UNSUBMITTED | 0 | SUBINDUSTRY | 0.08 | ON | 2.05 / 1.92 / 2.19 / 1.30 / 12.68% / 17.53bp |
| `O0WO8zqq` | UNSUBMITTED | 0 | SUBINDUSTRY | 0.08 | ON | 1.83 / 1.63 / 2.27 / 1.10 / 10.64% / 18.56bp |
| `GrmPOz05` | UNSUBMITTED | 0 | SUBINDUSTRY | 0.08 | ON | 1.79 / 1.41 / 2.66 / 1.02 / 14.09% / 12.40bp |
| `vRA82Ga3` | UNSUBMITTED | 0 | SUBINDUSTRY | 0.08 | ON | 1.75 / 1.44 / 2.59 / 1.22 / 10.17% / 16.71bp |
| `0mPKr3bq` | UNSUBMITTED | 0 | SUBINDUSTRY | 0.08 | ON | 2.36 / 2.04 / 2.67 / 1.54 / 16.40% / 14.88bp |
| `XgaGb3J1` | UNSUBMITTED | 0 | SUBINDUSTRY | 0.08 | ON | 2.36 / 2.02 / 2.71 / 1.51 / 17.38% / 14.66bp |

**为什么是这一行**：
1. 7 件都是 `decay0 + SUBINDUSTRY + trunc0.08 + nanHandling ON`（平台 `get_alpha_details` 实读）⇒ **本族的存活行**。
2. **不是族特异最优**：同族反例 `d5a2aO7v`（ACTIVE）是 **decay8**、`Vk65zLzG`（ACTIVE）是 **decay4 / nanHandling OFF**；区域生产档 `tracking/DEU/config/settings.json` 是 `decay4 / nanHandling OFF / 2013-01-01 起`。
⇒ **必须把 `decay 0/4/8 × nanHandling ON/OFF` 六格作对照臂**，不得把本行写成「最优」。
3. **可解释性**：insd1 字段级 cov 仅 0.5343、当日无申报时 `vec_*` 返回 NaN（不是 0）⇒ `nanHandling ON` 让「当期无申报」落 0 而不是丢样本；`decay0` 保住 66 日窗口后的快变分量（`ts_delta`/`ts_ir` 都是快变量）。
4. `trunc0.08 / maxTrade OFF / FASTEXPR` 7 件一致；`pasteurization ON / unitHandling VERIFY` 平台回显一致。

---

## §9 收割池（本轮实读；零仿真）

### 9.1 口径

- **来源**：ask 判据 + 本地 `alphas` 表（`mcp__wqb-db__get_alpha_by_id`，prod/self + `corr_checked_at`）+ 平台 `get_alpha_details`（`pyramids`/RA/metrics/settings）。
- **判据**：`failed_ra_count=0` 且 `checks.fail=[]`；`status=UNSUBMITTED`；`prod_correlation` **未测或已测 <0.70**（ask 原文写「prod 为 null」；本档按「未测或已测干净」执行，因已测干净严格优于未测，且本轮 5 条正是这种形态——**口径差异已在此声明**）。
- **塔归属**：逐件平台 `pyramids.list` 实读，不作推断。

### 9.2 候选逐条

| # | alphaId | 平台 pyramids | eff | S | F | 2Y | sub | TO | margin | RA | prod（本地） | self（本地/实测） | 内部线 | 梯队 |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| 1 | **`3q0wVPgz`** | `[INSIDERS, ANALYST]` | 2 | **2.04** | 1.81 | 2.49 | **1.33** | 12.53% | 15.69bp | `failed_ra_count=0`, `fail=[]` | **0.4531**（check_correlation, 09:10:57） | **0.305**（alphas 表；本轮 check_self 30s 超时） | **全过** | **第一（首选）** |
| 2 | `VkNV0zqM` | `[INSIDERS, ANALYST]` | 2 | **2.05** | 1.92 | 2.19 | 1.30 | 12.68% | 17.53bp | 0 / `[]` | **0.5013**（platform_sync, 07:36:57） | 0.4665 | 全过 | 第一 |
| 3 | `O0WO8zqq` | `[INSIDERS, ANALYST]` | 2 | 1.83 | 1.63 | 2.27 | 1.10 | 10.64% | 18.56bp | 0 / `[]`（CLUSTER_TEST warning 0.98<1） | 0.5153（platform_sync, 06:32:07） | 0.4758 | 全过 | 第一 |
| 4 | `GrmPOz05` | `[INSIDERS, ANALYST]` | 2 | 1.79 | 1.41 | 2.66 | 1.02 | 14.09% | 12.40bp | 0 / `[]` | 0.4923（platform_sync, 08:07:01） | 0.3136 | 全过 | 第一 |
| 5 | `vRA82Ga3` | `[INSIDERS, ANALYST]` | 2 | 1.75 | 1.44 | 2.59 | 1.22 | 10.17% | 16.71bp | 0 / `[]` | 0.5085（platform_sync, 07:06:58） | 0.3098 | 全过 | 第一 |
| 6 | `0mPKr3bq` | `[INSIDERS, MODEL]` | 2 | 2.36 | 2.04 | 2.67 | **1.54** | 16.40% | 14.88bp | 0 / `[]` | **null（未测）** | **0.6714**（本轮 `check_self_correlation` 实测，top `Vk65zLzG`） | **self 超内部 0.50** | 第二 |
| 7 | `XgaGb3J1` | `[INSIDERS, MODEL]` | 2 | 2.36 | 2.02 | 2.71 | 1.51 | 17.38% | 14.66bp | 0 / `[]` | 0.6784（check_correlation, 09:10:39；**与 self 逐位相同，疑同值写入**） | 0.6784（本轮实测） | **self + prod 双超内部线** | 末位（不作首选） |

**同族约束**：
- 1–5 互相 **0.83–0.97**（前序 2026-11-16 `compute_mutual_correlation`，4y/1021 点，max pair `GrmPOz05×vRA82Ga3`=0.969；**本轮未复跑**）⇒ **五条只能交一颗**，第二条会被 `SELF_CORRELATION` 拦。
- 6–7 同源（`predicted_surprise_*` / `mean_estimate_change_*`），彼此及与 1–5 的相关**未测**；其核心腿（insd1 + significant_value）与 1–5 相同 ⇒ 大概率同族。
- ⇒ **收割可得的塔位增量 = insiders 1→2，且只有一颗**。

### 9.3 十年跨度（首选的硬前置，本轮实读）

`mcp__wq-brain-http__get_alpha_yearly_stats("3q0wVPgz")`：**2014–2023 十年逐年 `pnl>0`**（42.2 万–159.9 万），LC 104–170 / SC 121–225，年 S 0.89–2.98。
⇒ 十年闸可达，不触发 `DEU-SENTIMENT-TOWER-DATASPAN-DEAD` 那类前段空窗。

### 9.4 已排除的「伪收割」

| 件 | 原因 |
|---|---|
| `1YWnZ9rK`（S 2.64 / 2Y 2.86 / sub 1.72） | `[PV, INSIDERS, MODEL]` **eff0（3 塔）**，点塔计数归 0；prod 0.5485 |
| `2r5MO67Z`（S 2.63） | 同上（`bucket(rank(cap))` 引入 PV），eff0 |
| `O0W5JdMg` / `58JqE0kk` / `oma9apvk` 等 | 同一 3 塔族，eff0 |
| `d5a2K72E`（S 1.78） | self **0.9133** vs `d5a2aO7v` FAIL（前序实测） |
| `YPaja5n6` | self **0.9160** vs `d5a2aO7v` FAIL（前序实测） |
| `GrWVx2aO`（S 2.07） | `[SENTIMENT]`，self **0.8419** vs `bl6OWZ2M` FAIL；且 sentiment 十年跨度不可达 |

---

## §10 风险登记

| # | 风险 | 读数/依据 | 处置 |
|---|---|---|---|
| R1 | 收割件同族只能交一颗 | 1–5 互相关 0.83–0.97 | 只交首选；第二颗必须换机制 |
| R2 | prod/self 值非本会话发起 | 5 条 prod 来自 `platform_sync`/`check_correlation`（06:32–09:10）；`get_alpha_details` 的 checks 仍显示 `PROD_CORRELATION` / `SELF_CORRELATION` pending | 提交前必须 `check_correlation(refresh=True)` + 平台 self 终验；**不能只信本地缓存** |
| R3 | `3q0wVPgz` self 本轮未测到 | `check_self_correlation` **30s 超时**（工具故障，不作证据）；本地表 0.305 | 提交前重测 |
| R4 | `XgaGb3J1` prod 值可疑 | prod=0.6784 与 self 逐位相同；且 >内部 0.65 | 不作首选；若动用先 `refresh=True` 重测 |
| R5 | 塔位当季清零 | TB-05 | 本档 1/3→2/3 只在 2026Q4 成立 |
| R6 | 双塔新件第三塔归零 | `1YWnZ9rK` / `vRA82ogA` 教训 | 每臂派发后复核 `pyramids.effective==2` |
| R7 | 十年跨度只核了 insd1 族 | `3q0wVPgz` / `XgaGb3J1` / `d5a2aO7v` / `bl6OWZ2M` / `E56AzejK` / `1YWaRlJm` 已读；其余未读 | 新臂若换数据集必须先读 yearly |
| R8 | ATOM 上限 1.30 的适用范围 | 只对 `insiders1` **单集** ATOM；跨集件不受此限（`0mPKr3bq` 2.36） | 不得用 1.30 否定跨集，也不得用跨集反证 1.30 |

---

## §11 证据通道与盲区（逐条声明）

| 结论 | 通道（本轮实跑） | 该通道对什么盲视 |
|---|---|---|
| 塔位 16 类计数 / need | `mcp__wq-brain-http__get_pyramid_alphas()`（当季 MCP 直读） | 只给**计数**，不给「是哪些 alpha」；按自然季清零；不区分 universe；`pending` 相关闸不影响计数但影响可提交性 |
| 数据集分母（insiders=2 等 11 塔） | `mcp__wq-brain-http__get_datasets(category=…, region="DEU", delay=1, universe="TOP500")` | **只给集级** coverage / fieldCount / alphaCount；对字段级可用性盲视；集级 cov=0 **不能**推出无数据（反例：GBR `techindi_model` cov=0 但 399 字段） |
| 字段可用性 / 新鲜度 / 覆盖率 | `mcp__wq-brain-http__get_datafields(dataset_id=…, filter_sharpe=true, sort_by="dateCreated", min_coverage=0.8)`；返回 `complete=true` 与 `platform_count` 一致 | 只给字段 `coverage`，**不给 longCount/shortCount**；拉不到 ≠ 没数据（需 `tools/probe/dataset_data_probe.py` 一条探针）；`filter_sharpe` 默认会滤负 Sharpe 字段（本轮 `sharpe_filter_removed=0`） |
| 塔归属 / effective / RA / 年度 | `mcp__wq-brain-http__get_alpha_details` / `get_alpha_yearly_stats` | 只能逐件查；`checks.pass` 不回 limit；`pending` 项不能当通过；只覆盖平台上已存在的 alpha |
| 历史臂数 / 池规模 | `mcp__wqb-db__get_mining_yield(region="DEU", by_dataset=true, strict=true)` + `get_alpha_by_id` | ⚠ **MCP 直连仿真不写 `expressions`** ⇒ 本轮 7 条收割件只有在被 upsert 后才有行；`insiders1` 本地 40 行恰是 4 波 upsert 件；`alphas.dataset_id` 大量为 **1902（伪 id）** ⇒ 数据集归属只能靠 code 字段前缀；`passed` 用 **|S|** ⇒ 负向强臂会抬高 passed，不能当 ra_clean |
| 数据集画像 | `mcp__wqb-db__query_dataset_profile(region="DEU")` | **返回 0 行**（本区无画像）⇒ 本条通道对 DEU 全盲 |
| prod / self | 本地 `alphas.prod_correlation` / `self_correlation` + `check_self_correlation`（本地池，不占平台槽） | 本地值可能是**旧缓存**（`corr_checked_at` 逐件看）；`platform_sync` 与 `check_correlation` 两种来源混用；**篮内互相关（未提交同批候选之间）不在 self 池里** |
| 判死 / 封盘 | `get_dead_datasets(DEU)`=19 集 + `get_dead_ends(DEU)` 全量 + `tracking/DEU/**` 档案 | **死标记不得单独作依据**（本轮推翻两处：`directional_indicator` 实为 cov 1.0/aCnt 52；institutions「0 RA 全过」已被 `E56AzejK` 打破）；死档不覆盖 MCP 直连仿真 |
| 「未测」清单 | 上述全部通道 | **「未测」= 这些通道里没找到证据，不等于没人跑过**；`macro27` / `option1` / `institutions4` / `institutions25` 均属此类 |

---

## §12 下一步（给下游波次）

### 12.1 第 0 步（零仿真，先做）

1. 对 **`3q0wVPgz`**（首选）跑平台 `check_self_correlation` + `check_correlation(production, refresh=True)` 终验；`VkNV0zqM` 作备。
2. 两项均 < 内部线（self 0.50 / prod 0.65）且用户确认 ⇒ 提交 ⇒ **insiders 1/3 → 2/3**（`[INSIDERS,ANALYST]` eff2；ANALYST 已亮无增量）。
3. 若首选被平台 self 终验否掉（本地 0.305，余量充足），按 1→5 顺序换件；五条为同族，**只能成一颗**。

### 12.2 第 1 步（新波，ATOM 已穷尽后的跨集兜底）

- **主腿（同塔）**：`insd1_holdings` / `insd1_valueeur` / `insd1_shares` 的 `ts_backfill(250)` → `ts_delta` / `ts_ir` / `reverse(days_from_last_change)`；
  `insider_agg_matrix` 的 `significant_value_1..4` 比值经 **`ratio` 入口**（`divide(..., add(...,1e-4))`）或 **`gating` 入口**（`trade_when(...)`），**禁止加法腿**。
- **分组轴**：`sector`（存活件已用）→ 对照 `subindustry` / `market`；第三档才试 `bucket(rank(vec_avg(ts_backfill(rsk60_offer,66))))`（**一旦启用即为 `[INSIDERS,RISK]` eff2，可同时推进 risk 0/3→1/3；先跑 1 臂验证 `pyramids.effective==2` 与 S**）。
- **对照臂（必带）**：`decay 0/4/8` × `nanHandling ON/OFF` 六格；`ts_backfill 66/250` 两档；双向符号臂各 1 条。
- **止损线**：首臂 S < 1.58 **或** sub < 0.39（平台 limit）即停，不派第二批；TO >0.7 判表达层错误（先修 backfill，不判信号死）。

### 12.3 第 2 步（塔位）

- 若新波过闸 ⇒ **insiders 2/3→3/3**（点亮）；若同时启用 risk60 分组轴并过闸 ⇒ **risk 0/3→1/3**。
- 若无过闸件 ⇒ insiders 停在 2/3，本轮结束；不得把「无过闸」写成数据集判死（D2 仍有 3 字段未测、D6 只有单配置）。

---

## §13 与 2026-11-16 S0 的差异（更新台账）

| # | 上一版 | 本版（2026-11-17 实读） |
|---|---|---|
| 1 | 5 条 `[INSIDERS,ANALYST]` 的 prod「未取（correlation_busy）」 | **5 条 prod 全部已测且 0.4531–0.5153 < 内部 0.65**；self 0.305–0.4758 < 内部 0.50 ⇒ **全部过内部线**（来源：`alphas` 表 06:32–09:10 刷写 + 本轮 `get_alpha_by_id` 读） |
| 2 | `XgaGb3J1` prod 0.6784 > 内部 0.65，列「备选」 | prod/self **同值 0.6784**（疑同值写入），来源 `check_correlation` ⇒ 降为**末位**，动用前必须重测 |
| 3 | 配对塔留空（institutions6 合规形 0.82） | **结论不变**；新增「bucket-only 第二数据集照计第二塔」的直接实证（`1YWaRlJm` eff2），并把 `risk60` 登记为唯一保留备选（平台 `kqarVldO` → `DEU/D1/RISK` eff1 实读） |
| 4 | `institutions6` 的十年跨度「未取」 | **已取**：`1YWaRlJm` 2014–2023 逐年 LC/SC>0 ⇒ **跨度不是问题，强度 0.82 才是** |
| 5 | ATOM 政策未纳入 | 按 2026-11-17 政策补齐：`insiders1` 30 臂 / `insider_agg_matrix` 22 模板 ⇒ **ATOM 已穷尽成立**，跨集兜底合法 |
| 6 | 收割「只推进一颗」 | 结论不变，但依据升级：五条互相关 0.83–0.97（前序未复跑）+ self/prod 全部实测 |
| 7 | 塔位 16 类 | 逐项不变（MCP 直读 = CLI 表） |

---

## §14 复现命令

```text
# 塔位（权威）
mcp__wq-brain-http__get_pyramid_alphas()

# 分母（唯一合法来源；本轮实取 11 塔）
mcp__wq-brain-http__get_datasets(category="insiders",     region="DEU", delay=1, universe="TOP500")
mcp__wq-brain-http__get_datasets(category="institutions", region="DEU", delay=1, universe="TOP500")
mcp__wq-brain-http__get_datasets(category="sentiment",    region="DEU", delay=1, universe="TOP500")
mcp__wq-brain-http__get_datasets(category="macro",        region="DEU", delay=1, universe="TOP500")
mcp__wq-brain-http__get_datasets(category="option",       region="DEU", delay=1, universe="TOP500")

# 字段级 + 新鲜度 + 覆盖率
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="insiders1",         sort_by="dateCreated", min_coverage=0.8)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="insider_agg_matrix", sort_by="dateCreated", min_coverage=0.8)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="institutions6",     sort_by="dateCreated", min_coverage=0.8)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="risk60",           sort_by="dateCreated", min_coverage=0.8)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="macro27",          sort_by="dateCreated", min_coverage=0.8)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="option1",          sort_by="dateCreated", min_coverage=0.8)
mcp__wq-brain-http__get_datafields(region="DEU", universe="TOP500", delay=1, dataset_id="institutions25")

# 塔归属 / RA / 设置 / 指标（逐件实读）
mcp__wq-brain-http__get_alpha_details(alpha_id="3q0wVPgz")   # [INSIDERS,ANALYST] eff2 S2.04
mcp__wq-brain-http__get_alpha_details(alpha_id="VkNV0zqM")   # [INSIDERS,ANALYST] eff2 S2.05
mcp__wq-brain-http__get_alpha_details(alpha_id="O0WO8zqq")   # [INSIDERS,ANALYST] eff2 S1.83
mcp__wq-brain-http__get_alpha_details(alpha_id="GrmPOz05")   # [INSIDERS,ANALYST] eff2 S1.79
mcp__wq-brain-http__get_alpha_details(alpha_id="vRA82Ga3")   # [INSIDERS,ANALYST] eff2 S1.75
mcp__wq-brain-http__get_alpha_details(alpha_id="0mPKr3bq")   # [INSIDERS,MODEL] eff2 S2.36
mcp__wq-brain-http__get_alpha_details(alpha_id="XgaGb3J1")   # [INSIDERS,MODEL] eff2 S2.36
mcp__wq-brain-http__get_alpha_details(alpha_id="d5a2aO7v")   # ACTIVE 2026-11-12 [SHORTINTEREST,INSIDERS] eff2
mcp__wq-brain-http__get_alpha_details(alpha_id="2rmGAPqN")   # ACTIVE 2026-10-09 [INSTITUTIONS,OTHER] eff2
mcp__wq-brain-http__get_alpha_details(alpha_id="1YWaRlJm")   # [INSTITUTIONS,INSIDERS] eff2 S0.82/sub0.21; LOW_SHARPE limit=1.58
mcp__wq-brain-http__get_alpha_details(alpha_id="kqarVldO")   # [RISK] eff1 S-0.92; LC153/SC214

# 十年跨度
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="3q0wVPgz")  # 2014-2023 逐年 pnl>0
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="bl6OWZ2M")  # 2014-2018 全零 ⇒ sentiment 跨度
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="E56AzejK")  # 2014-2017 全零 ⇒ institutions1 跨度
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="1YWaRlJm")  # 2014-2023 逐年有仓 ⇒ institutions6 跨度 OK

# self（本地池，不占平台槽）
mcp__wq-brain-http__check_self_correlation(alpha_id="0mPKr3bq", threshold=0.7)  # 0.6714 PASS
mcp__wq-brain-http__check_self_correlation(alpha_id="XgaGb3J1", threshold=0.7)  # 0.6784 PASS
# 3q0wVPgz：本轮 30s 超时（工具故障）

# 历史臂数 / 产出率
mcp__wqb-db__get_mining_yield(region="DEU", by_dataset=true, strict=true)
mcp__wqb-db__get_alpha_by_id(alpha_id="3q0wVPgz")   # prod 0.4531 / self 0.305
mcp__wqb-db__query_dataset_profile(region="DEU")    # 0 行 ⇒ 本区无画像
```

---

## §15 本档对 ask 指令冲突的显式登记

1. **ask §3「ATOM 优先」 vs ask §4「配对」**：本档按「ATOM 已穷尽 ⇒ 允许跨集兜底」处理（依据 = insiders1 3 波 30 臂收敛 1.30、insider_agg_matrix 22 模板收敛 0.93）；跨集兜底限定 `gating/grouping/residual/ratio`，**不含加法腿**；因此现存 `[INSIDERS,ANALYST]` / `[INSIDERS,MODEL]` 只能作**塔位件**、不作**配方**。
2. **`harvestPool` 判据「prod 为 null」**：本档按「未测或已测 <0.70」执行（已测干净优于未测）；5 条第一梯队正是「已测干净」形态，已在 §9.1 声明。
3. **`partnerTower` 留空**：并非未评估（§5 逐条评估），而是**没有合规且可达标**的第二个未亮塔；`risk60` 已登记为保留备选，需用户授权才作单臂探针。

---

## §16 独立复核修订（v2，2026-11-17；本节**覆盖** §0/§9/§12 的「可提交性」结论）

> 复核共 10 条问题 + 9 条缺失证据 + 11 条必须修改。本节逐条处置，并补跑复核要求的核验。
> **本节新增读数均为本会话实跑**；沿用前序读数的条目逐条标注。
> 命令留档：`python -X utf8 logs/_tmp_s0_add_gate.py`、`logs/_tmp_s0_add_gate2.py`、`logs/_tmp_s0_subtract_gate.py`。

### 16.1 修订后的结论（替换 §0/§9/§12 对应项）

| 项 | 修订前 | **修订后** |
|---|---|---|
| 目标塔 | insiders（need 2） | **insiders（need 2）— 不变**（仍唯一满足十年闸的未亮塔；§16.3-3/8 见 institutions/sentiment 的十年阻断） |
| 配对塔 / 配对数据集 | 留空 | **留空 — 不变**（§5 结论未被复核推翻） |
| 主数据集 | insiders1 | **insiders1 — 不变**；`insider_agg_matrix` 仅作同塔第二腿 |
| **可提交收割件** | 7 条 | **0 条**：7 条 add 型全部闸 5 `block=True`（§16.2-1），32 条 subtract 型 **6/6 self FAIL**（§16.3-1） |
| towerGain | insiders 1/3→2/3 | **条件式**：仅在用户显式裁定 add 型存量件可提交 + 3q0wVPgz 平台 self 终验 <0.50 时成立；合规零仿真路径 = 无（§16.5） |
| 新波 | ratio/gating 跨集 | **降级为 1 臂探针**，首臂 S<1.58 即停（§16.2-8 / §16.4） |

### 16.2 复核问题逐条处置（10 条）

| # | 复核问题 | 我的核验（本轮实跑） | 处置 |
|---:|---|---|---|
| 1 | 7 条收割件均命中 add 多腿禁令 | **采信**。`logs/_tmp_s0_add_gate.py` 实跑 `_find_equal_weight_leg_add`：`3q0wVPgz` **4 命中 / 全 same_dataset=False**、`VkNV0zqM` 5、`O0WO8zqq` 5、`GrmPOz05` 4、`vRA82Ga3` 4、`XgaGb3J1` 4；`0mPKr3bq` 3 命中（`logs/_tmp_s0_add_gate2.py` 带 field_dataset：2 条同源豁免 + **1 条跨集 BLOCK**）。规范：`AGENTS.md:447` §7.7「**仍然无条件禁止** add(独立信号腿A,独立信号腿B)」；`src/wqb/profiles/locked.py:16-18` `mixed_signal_ban`；`Claude/skills/wq-brain-campaign-toolkit/config/methodology_rules.json` `mixed_signal_leg_ban_v1`（poisons 含 `equal_weight_leg_add`）；`docs/experience/02_signal_patterns.md:310-325` §11（DEU 91 颗存量多腿 S2.17 **违规不可提交**，拆单腿峰值 **1.36**，82 臂 **0 条 ≥1.58**）。**「只作塔位件」在 locked.py / methodology_rules 里无豁免条款** | **7 条全部移出可提交池**（§16.4），不作 towerGain 的既得增量 |
| 2 | 0mPKr3bq / XgaGb3J1 内部线不过 | **采信**：0mPKr3bq self **0.6714**（本轮 `check_self_correlation` 实测，top `Vk65zLzG`）> 内部 0.50、prod null；XgaGb3J1 self **0.6784**（本轮实测）> 0.50，本地 prod 同为 0.6784（与 self 逐位相同，疑同值写入）> 内部 0.65 | 移出可提交池，仅留档 |
| 3 | trio 配额漏算 | **采信并更正**：`MODEL ∈ TOWER_TRIO`（`locked.py:64-65`），`[INSIDERS,MODEL]` = trio×非trio，吃 `TOWER_TRIO_CROSS_QUOTA=5`（`locked.py:68`）。原文「本档不涉 trio」只对 `[INSIDERS,ANALYST]` 成立 ⇒ 已改 |
| 4 | 两塔组合配额 | **采信**：`TOWER_PAIR_QUOTA=3`（`locked.py:51-52`）；池内 `[INSIDERS,ANALYST]` **5 条** > 3 ⇒ **该组合超配封盘（既有候选仍可提交，不得新增）**；计划不得再生成同组合新件 |
| 5 | 唯一 +1 可能被 self 终验否掉 | **采信**：`3q0wVPgz` 本轮 `check_self_correlation` **30s 超时**（工具故障，不作证据）；平台 `checks.pending` 含 `SELF_CORRELATION`/`PROD_CORRELATION`；本地 0.305 不能当平台已测 | 写入 R3/§16.6，提交前必须平台终验 |
| 6 | CW 操作线应为 0.10 | **采信**：平台 `CONCENTRATED_WEIGHT` limit=**0.10**（台账/实测）；0.5 只是本地 review 线 | §7.1 与新臂预筛改 0.10 |
| 7 | settingsLine 缺起止日期、2013 生产档会崩对照 | **采信**：7 件平台回显 `2014-01-01→2023-12-31`；区域生产档 `tracking/DEU/config/settings.json` 与 `references/_dataset-scan-method.md:271` 是 **2013-01-01** | settingsLine 补起止日期，并把 2013 生产档列为**禁止混用的对照项** |
| 8 | 2/3→3/3 机制假设无 ≥1.58 读数 | **采信**：`DEU-INSIDER-AGGMATRIX-DEAD`（22 模板上限 0.92–0.93）与 `02_signal_patterns.md:317-325`（DEU 单腿峰值 **1.36**、82 臂 0 条 ≥1.58）⇒ 同塔 ratio/gating 无任何 ≥1.58 证据 | §12.2 降级为 **1 臂探针 + 止损** |
| 9 | 「N backtested / 0 ra_clean」口径盲区 | **采信**：本轮实查 `backtest_results`（region=DEU）**total=12635 / dataset NULL=10203 = 80.75%**；`get_mining_yield` 对这批无归属行盲视 | 全文所有此类表述改标「本地库口径（81% 无 dataset 归属；MCP 直连仿真不写该表）」 |
| 10 | pv20 死档与台账冲突 | **采信**：`tracking/DEU/reports/deu_campaign_20261030.md:12743` 「pv20 \| 681 \| 0.0 \| 619 \| 判死 `pv20_dead`」；`COVERAGE_RELAX_EARNINGS6_PV20_20261111.md` 写 S 1.03/0.95、2Y 1.28 | **登记为待判**（§16.7），**不作** moreTowersRemain 的既定证据 |

### 16.3 缺失证据补齐（9 条）

#### 16.3-1 `[INSIDERS,SHORTINTEREST]` 32 条 subtract 池（复核核心缺口）

**池口径**（本轮只读 SQL，`logs/_tmp_s0_subtract_gate.py`）：DEU / S≥1.58 / status∈{UNSUBMITTED,NULL} / stage∈{IS,NULL} / 最新回测 `ra_failed_checks∈{'[]',''}` / prod 空或 <0.70 ⇒ **319 行**；其中 `insd1_` × `shrt3_` 共 **32 条**（29 条 subtract-only，3 条 add 型：`wpo8ZQN6` / `zqdvbLzo` / `KPgKr2Rz`）。
闸 5 全家判定：32/32 触发 `spread_cross_dataset`（`_spread_findings` 返回 2 条 cross；**未声明经济含义即阻断**；按 `_gate_expr_checks.py:1009-1046` 的 2026-10-01 用户口径，跨集价差**声明后可放行**，add 则永不放行）。

**self 抽样（本轮实测 + 前序）：**

| alpha | S | self | top correlated | 结论 |
|---|---:|---:|---|---|
| `1YWqZ25X` | 1.72 | **0.9346** | `d5a2aO7v` | **FAIL（本轮）** |
| `88NmPYj7` | 1.69 | **0.9293** | `d5a2aO7v` | **FAIL（本轮）** |
| `ZYaRmXzj` | 1.76 | **0.9520** | `d5a2aO7v` | **FAIL（本轮）** |
| `gJaYeV9g` | 1.74 | **0.9263** | `d5a2aO7v` | **FAIL（本轮）** |
| `d5a2K72E` | 1.78 | 0.9133 | `d5a2aO7v` | FAIL（前序实测） |
| `YPaja5n6` | 1.78 | 0.9160 | `d5a2aO7v` | FAIL（前序实测） |

⇒ **6/6 抽样全部 0.91–0.95，全部撞 ACTIVE `d5a2aO7v`**（`[SHORTINTEREST,INSIDERS]`，2026-11-12 提交）⇒ **整族克隆墙成立，不再作零仿真池**。剩余 26 条未逐条测，但同一骨架（insd1 的 `ts_rank(ts_backfill(...,W),252)` 减 shrt3 的 `ts_delta(...,220)`，仅 W 与外壳不同）与 6 条已测件同族，**按族级判据不重复消耗调用**（这是推断，不是逐条实读）。

#### 16.3-2 `submit_ready` 队列（DEC-33）

**未核对**：`mcp__wqb-db__get_submit_ready(region="DEU", status="READY", limit=50)` 连续两次返回
`Error POSTing to endpoint: {"code":-32600,"message":"Session not found"}`（**工具故障，不作证据**）。
复核称「11 条 READY / 0 条 insiders」——本档**不采信为实读**，只登记为待补。

#### 16.3-3 institutions1 的 RA-clean 行与 `58gGQmlN`

本轮只读 SQL：`inst1_` 且 `ra_failed_checks='[]'` 共 **34 行**（其中 S≥1.58 的 **24 行**；24 行里 5 条 prod≥0.70 ⇒ 19 条 prod 净/未测）。复核称「12 条」，口径不同，**结论同向**：不能用「0 条 RA 全过」排除。
新增平台实读（本轮）：
- `58gGQmlN`：`[DEU/D1/INSTITUTIONS, DEU/D1/OTHER]` **eff2**、RA 全过（`failed_ra_count=0`, `fail=[]`）、S 1.62 / F 1.26 / 2Y 2.58 / sub 1.15 / TO 13.11% / margin 12.10bp、prod **0.683**（>内部 0.65、<平台 0.70）；`get_alpha_yearly_stats`：**2014–2017 逐年 LC/SC/pnl 全 0**，2018 起才有仓。
⇒ institutions1 的排除依据升级为**两件平台年度实读**（`E56AzejK` + `58gGQmlN` 均 2014–2017 零仓），不再是「0 RA 全过」。

#### 16.3-4 harvestPool 五列

已在 §9.2 表内给全（pyramids / eff / self / prod / RA）；本修订新增「闸 5 判定」列，见 §16.4。

#### 16.3-5 trio×非trio 累计

| 组合 | 件 | 状态 | 计入配额？ |
|---|---|---|---|
| `[INSIDERS,MODEL]` | `Vk65zLzG` | **ACTIVE 2026-09-13（Q3）** | 是（1 条已确认） |
| `[INSIDERS,MODEL]` | `0mPKr3bq` / `XgaGb3J1` | IS 候选 | 若动用 → +2 |
| `[INSTITUTIONS,OTHER]` | `2rmGAPqN` | **ACTIVE 2026-10-09（Q4）** | 是（1 条已确认） |
| `[INSTITUTIONS,OTHER]` | `58gGQmlN` / `E56AzejK` | IS 候选 | 若动用 → +2 |
| `[INSIDERS,ANALYST]` | 5 条 | IS 候选 | 该两塔组合 **5 > TOWER_PAIR_QUOTA=3 ⇒ 封盘（不得新增）** |

⇒ 按最保守口径（只算 ACTIVE），trio×非trio 已用 **2/5**；动用 `0mPKr3bq` 或 `XgaGb3J1` 会推到 3/5。

#### 16.3-6 S≥1.58 三处口径冲突（登记）

| 来源 | LOW_SHARPE 线（Delay-1） | 性质 |
|---|---:|---|
| `src/wqb/config.py:539-543` `PLATFORM_CHECK_LINES["low_sharpe_min"]["delay1"]` | **1.25** | 平台通用缺省 |
| `tracking/DEU/config/thresholds.json` `sharpe_min` | **1.58** | 区域战役线 |
| `1YWaRlJm` 平台 `checks.fail`：`{LOW_SHARPE, value:0.82, limit:1.58}` | **1.58** | **DEU/D1 逐件实读，本档操作线** |

⇒ 本档按 **1.58** 执行（DEU 实读）；`config` 的 1.25 与 DEU 实读不一致，**登记为待治理口径冲突**，不在本档裁定。

#### 16.3-7 `directional_significant_value_1`「毒字段」指控：**未采信（字段名不同）**

复核称「`3q0wVPgz` 正用它作主腿」。实读 `3q0wVPgz` code：用的是 **`significant_value_1`**（无 `directional_` 前缀），`directional_` 前缀字段在该表达式里**零出现**。
`DEU-INSIDER-AGGMATRIX-DEAD` 的禁试清单针对的是 **`directional_significant_value_1`**（平台 `userCount=0 / alphaCount=0`）。本档**从未推荐**该字段。⇒ 该条**不成立**；但「毒字段不可用」的结论本身与本档不冲突。

#### 16.3-8 sentiment 30 条本地 strict-pool 候选

本轮只读 SQL：池内含 `snt7_` **28 条**、含 `snl27_` **29 条**，两者**同时出现 29 条**（仅 `Jje0J2rx` 为 snl27-only、`d5WqmExJ` 为 snt7-only）；S 1.59–2.07、2Y 2.02–2.55，prod 多数 null（`QPveY7Kg` 0.6671）。
⇒ 与 `bl6OWZ2M` 的 2014–2018 零仓一致：**整池建立在 snt7/snl27 十年跨度不足的面之上**，不作目标塔（可逆假设）。

#### 16.3-9 XgaGb3J1 / 0mPKr3bq 的 prod refresh

**未跑**：平台 prod 计算占单并发槽（1–5 分钟），S0 零配额边界内不做。`0mPKr3bq` prod 仍 null；`XgaGb3J1` 本地 prod=0.6784 与 self 同值可疑 ⇒ 列 R2，提交前 `refresh=True`。

### 16.4 修订后的可提交池（替换 §9）

**可提交：0 条。**

| 层 | 件 | 闸 5 | self | prod | 处置 |
|---|---|---:|---|---|---|
| add 型（待用户裁定） | `3q0wVPgz` 4 命中 / `VkNV0zqM` 5 / `O0WO8zqq` 5 / `GrmPOz05` 4 / `vRA82Ga3` 4 | **block** | 0.305 / 0.4665 / 0.4758 / 0.3136 / 0.3098 | 0.4531 / 0.5013 / 0.5153 / 0.4923 / 0.5085 | **不提交**；若用户显式裁定 add 型存量件可提交，首选 `3q0wVPgz`（内部线全过） |
| add 型（内部线不过） | `0mPKr3bq`（1 跨集 BLOCK） / `XgaGb3J1`（4 BLOCK） | block | 0.6714 / 0.6784 | null / 0.6784 | **不提交**（self 撞内部 0.50；Xga prod 撞 0.65） |
| 跨集价差（已证伪） | 32 条 `insd1×shrt3` | 需声明；未声明即 block | **6/6 抽样 0.9133–0.9520 FAIL** | 多数 null | **移出可提交池**（整族克隆墙） |

### 16.5 修订后的 towerGain（替换 §0/§9 的承诺）

> **insiders 1/3→2/3 目前没有可执行的合规路径。**
> ① 7 条 add 型是唯一有平台实证强度（S 1.75–2.36）的件，但闸 5 `equal_weight_leg_add` **全部 block**
> （命中数：`3q0wVPgz` 4 / `VkNV0zqM` 5 / `O0WO8zqq` 5 / `GrmPOz05` 4 / `vRA82Ga3` 4 / `0mPKr3bq` 1 跨集 / `XgaGb3J1` 4），
> 且 `AGENTS.md:447` §7.7 明写「仍然无条件禁止」、`locked.py` 无「塔位件」豁免 ⇒ **须用户显式裁定**。
> ② 合规零仿真池（32 条跨集价差）**6/6 self FAIL（0.91–0.95 撞 ACTIVE `d5a2aO7v`）** ⇒ 整族不可用。
> ③ 因此 +1 只在此条件下成立：**用户裁定 add 型可提交** 且 `3q0wVPgz` 平台 self 终验 <0.50 / prod <0.65。
> 否则只能走新波探针（§16.6），且不承诺点亮。

### 16.6 修订后的新波（替换 §12.2）

**第 1 步 = 1 臂探针（不是整波）**：`insiders1` 主信号 × `insider_agg_matrix` 的**单一**合规形态（`ratio` 或 `gating` 二选一，**禁 add / 禁 multiply 复合腿**），`ts_backfill(250)`、`sector` 轴。
- **止损**：首臂 S < 1.58 **或** sub < 0.39 ⇒ **停，不派第二批**。
- **先验**：`insider_agg_matrix` 单集 22 模板上限 **0.92–0.93**；DEU 存量单腿峰值 **1.36**（82 臂 0 条 ≥1.58，`02_signal_patterns.md:317-325`）⇒ 本探针是**低先验**验证，不是既定路径。
- **禁止**：把 `[INSIDERS,ANALYST]` 的 add 结构改写成新波（组合形态铁律）；把 `insd1×shrt3` 换窗口当新族（克隆墙）。

### 16.7 pv20 冲突登记（待判）

| 来源 | 读数 |
|---|---|
| `tracking/DEU/reports/deu_campaign_20261030.md:12743` | pv20：681 字段、cov 0.0、aCnt 619、**判死 `pv20_dead`** |
| `tracking/DEU/atom_orthogonal/COVERAGE_RELAX_EARNINGS6_PV20_20261111.md` §三 | `average_daily_value_20d_usd` S 1.03 / F 0.68 / TO 0.102；`adv20_usd_capped_100m` S 0.95 / 2Y 1.28 |
| 本轮 `get_datasets(category="pv")` | pv20 cov 0.0 / 681 字段 / alphaCount 670 |

⇒ **两者必有一错，登记为待判**（可能差异：判死针对 pv20 的汇率/价差面，台账针对流动性字段；或 cov 口径不同），**不作为** moreTowersRemain 的既定证据。

### 16.8 settingsLine（修订：补起止日期）

```
DEU/TOP500/D1/decay0/SUBINDUSTRY/trunc0.08/nanHandling ON/maxTrade OFF/FASTEXPR/startDate 2014-01-01/endDate 2023-12-31
```
- 7 件收割件平台回显逐项一致（含起止日期）。
- **禁止混用**：区域生产档 `decay4 + nanHandling OFF + startDate 2013-01-01`（`tracking/DEU/config/settings.json`；`references/_dataset-scan-method.md:271`）——起止日期差一年会让十年闸与 ATOM 上限不可比。
- decay / nanHandling 仍须六格对照（§8 理由不变）。

### 16.9 复核未采信清单（附理由）

| 复核条目 | 未采信理由 |
|---|---|
| 「`0mPKr3bq` 7 处命中」 | 我实跑得 **3 处**（带 field_dataset：2 同源豁免 + 1 跨集 block）。口径可能含嵌套重复计数；**结论同向**（仍 block），故按我方读数登记 |
| 「institutions1 12 条 ra=[]」 | 我读到 **34 条 ra='[]'（其中 S≥1.58 共 24 条）**。口径不同；**结论同向**（不能用 0 条估计排除），已按我的读数登记 |
| 「`3q0wVPgz` 用 `directional_significant_value_1`」 | 字段名不同：实读 code 用 `significant_value_1`（无 `directional_` 前缀），该前缀在表达式中零出现（§16.3-7） |
| 「submit_ready 11 READY / 0 insiders」 | 工具连续两次 `Session not found`（故障），无法复现；不采信为实读，只列待补 |

### 16.10 本轮新增风险

| # | 风险 | 依据 | 处置 |
|---|---|---|---|
| R9 | add 型 7 件需用户显式裁定 | 闸 5 block；§7.7 无条件禁止 | 未经裁定不提交；裁定后先 3q0wVPgz 平台 self/prod 终验 |
| R10 | `[INSIDERS,SHORTINTEREST]` 整族克隆墙 | 6/6 self 0.9133–0.9520 vs `d5a2aO7v` | 不再投入；不再换窗口重试 |
| R11 | submit_ready 队列不可读 | MCP `Session not found` ×2 | 重连后补核；不据队列下结论 |
| R12 | S 线三口径冲突 | config 1.25 / thresholds 1.58 / 平台 fail payload 1.58 | 本档按 1.58；待治理 |
| R13 | pv20 死档 vs 活体读数冲突 | §16.7 | 待判；不作目标依据 |
