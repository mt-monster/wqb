# USA · `shortinterest43`（Short Sell Dataset）字段画像 · asOf 2026-11-15

> **归档路径与命名规则（本文唯一权威口径）**
> - **权威位（tracking）**：`tracking/USA/reference/_usa-shortinterest43-field-profile-20261115.md` ← 本文件
> - **skills 镜像位**：`Claude/skills/wq-brain-ra-usa/references/_usa-shortinterest43-field-profile-20261115.md`（内容逐字同源；改一处必须同步另一处）
> - **命名规则**：`_usa-<dataset_id>-field-profile-<asOf>.md`
>   - `_` 前缀 = 专题档案（不是 `wqb.profiles render` 生成块，改它不影响 `SKILL.md` 渲染）；区域侧由 render 生成的组合卡是不带 `_` 的 `references/<类别>.md`。
>   - `<dataset_id>` = 平台 `dataset_id` 原文（`shortinterest43`），**不缩写**（历史上有 `_usa-fnd21-…` 这类缩写版本，本代统一用全 id，避免 S0 检索 miss）。
>   - `<asOf>` = 画像**基准日**（本轮用户指定 `20261115`；实际落盘 2026-11-16，平台字段实取时刻 2026-11-16）。
>   - 同族兄弟命名：类别级扫描 `_usa-<category>-dataset-scan-<asOf>.md`；模板库 `_usa-<dataset_id>-template-library-<asOf>.md`。
> - **本文件与旧档的关系**：`docs/reference/USA/shortinterest43_field_profile.md`（脚本生成，2026-10-29）与 `docs/reference/USA/shortinterest43_template_library.md`（2026-10-29）是**上一代产物**，其「判死」结论已被本轮 DB 实测推翻（见 §5/§6）。模板库的机制解释与禁区表仍有效，**结论层以本文件为准**。

> **口径声明（读前必看）**
> 1. 全程固定 **USA / TOP3000 / delay 1**，本轮未切换任何其它区域或宇宙。
> 2. **本轮是画像任务，不是开波任务**：未派发任何仿真，未提交任何 alpha（`WQB_ALLOW_ALPHA_SUBMIT=False` 口径不变，提交权归用户）。
> 3. **分布特征一列全部是「推断」**，不是实测：本仓没有「取原始面板值」的通道（`get_record_sets` 只接受 `alpha_id`、返回 alpha 级记录集，不给字段样本）。凡影响结论的分布判断，本文都用**已跑过的 alpha 读数**交叉验证（§5），并标注证据来源。
> 4. `alphaCount` / `userCount` 是**移动值**：本轮实取与 2026-10-29 快照相比，**14 / 32 字段**发生变化（§3.3），故所有拥挤度判断都带 asOf。

---

## 1. 规模与完整性（平台实取）

| 项 | 值 | 来源 |
|---|---|---|
| 实取字段数 | **32** | `get_datafields(region=USA, universe=TOP3000, delay=1, dataset_id="shortinterest43", filter_sharpe=false)`，`count=32`、`platform_count=32`、`complete=true`、`pages_fetched=1` |
| 类型分布 | **MATRIX × 32** | 同上（`type` 字段逐项确认；**无 VECTOR、无 GROUP**） |
| 平均 coverage | **0.999387** | 32 字段算术平均（30 × 1.0 + 2 × 0.9902） |
| coverage < 1 的字段 | **2 个**：`shrt43_edgash_sumsize_m_data1` / `_m_data2` = **0.9902** | 同上 |
| ΣalphaCount（字段级求和） | **2272** | 本轮实取；数据集级 `alphaCount=1571`（见 §3.3 口径差异） |
| ΣuserCount | **1244** | 本轮实取；数据集级 `userCount=509` |
| 数据集中位拥挤度 | alphaCount 中位数 **38** | 32 字段排序取中 |
| 敞口分档 | ≤10：4 个　11–50：16 个　51–200：10 个　>200：**2 个** | 同上 |

**数据集级元信息**（`get_datasets(region=USA, universe=TOP3000, delay=1, category="shortinterest")`，`count=6`）：

| dataset | name | cov | 字段 | user | alpha | valueScore | multiplier |
|---|---|---:|---:|---:|---:|---:|---:|
| **shortinterest43** | Short Sell Dataset | **0.9994** | **32** | 509 | **1571** | 3.0 | **1.1** |

同类别其余 5 集（用于定位，不在本轮范围）：`short_interest_pred`（10 字段/cov 0.9987/ac 518）、`shortinterest24`（1/0.2573/449）、`shortinterest29`（32/0.8838/276，已判死）、`shortinterest3`（31/1.0/4856）、`us_short_sale`（4/1.0/356）。

**塔位（本轮实查 `get_pyramid_alphas`）**：`USA / D1 / shortinterest = 0`（未点亮）⇒ 本数据集是**单塔 ATOM 可登记的处女塔**。同快照下 USA/D1 已点亮：analyst 6、model 4、other 3、risk 2、earnings 2、institutions 1。

---

## 2. 字段族划分（按经济机制归并，5 族）

> 归并依据 = **description 原文**（唯一语义来源）+ 字段名结构（`<venue>shvol_<svol|totalvolume|marketcenter>` / `<venue>sh_sumsize_<m|s>_data<1|2>`）。四所 = **Cboe 四个子交易所 BZX / BYX / EDGA / EDGX**（平台论坛帖 `35577573602455`，MY82844，15 票；见 `docs/reference/USA/shortinterest43_template_library.md` §2.1）。

| 族 | 字段数 | 成员 | 经济机制 | 平台证据 |
|---|---:|---|---|---|
| **F1 交易所卖空流量比** | 8 | `shrt43_{batsshvol,byxxshvol,edgashvol,edgxshvol}_svol` + 同名 `_totalvolume` | 该票在**该所**当日「卖空股数 ÷ 该所总成交股数」= **该所卖空占比**。分子分母同单位（股）⇒ 天然无量纲、无需 ε。经济学上主体是**做市商库存对冲**，不是方向性空头 | 描述含 "sold short"/"shares traded" + "for the day"；`aC` 合计 **1371**（最大族） |
| **F2 场所成交规模/份额**（分母件独立可用） | 4 | `shrt43_<venue>shvol_totalvolume` | 该票在**该所**的总成交股数 ⇒ 可作为「场所流动性份额 / 场所竞争」量（`venue_i / Σ4venue`） | 描述 "Total shares traded … on <venue> for the day" |
| **F3 sumsize 聚合（语义不透明）** | 16 | `shrt43_<venue>sh_sumsize_{m,s}_data{1,2}` | **description 只有 `data1` / `data2`**，平台未披露口径。名字暗示「成交规模总和」；`m`/`s` 疑为 monthly / session，`data1`/`data2` 疑为两个统计口径 —— **全部为推断** | 描述 `data1`/`data2`（16/16 字段），`aC` 合计 799；其中 `edgxsh_sumsize_m_data2` = 74 用户/124 alpha，是**全数据集最拥挤单字段** |
| **F4 市场中心标识** | 4 | `shrt43_<venue>shvol_marketcenter` | 四所描述**逐字相同**："Bats operated stock exchanges" ⇒ 疑为**场所标识码**（元数据），不是信号 | 描述 = 8 个字的场所名；`aC` 合计 82（最低） |
| **F5 豁免卖空（Reg SHO 豁免）** | 4 | `count_shares_short_exempted`、`quantity_sold_short_exempted`、`total_short_exempted_shares`、`volume_short_exempted_trades` | Reg SHO **豁免条款（做市商豁免）**下的卖空股数 ⇒ 理论上可分离「做市对冲」与「方向性做空」 | 描述含 "short-exempt" / "exempt from certain trading regulations"；`aC` 合计仅 **10**（最低拥挤） |

### 2.1 每族一条可证伪假设（预注册，回测前写死）

| 族 | 假设（H） | 证伪条件（读到即推翻，不得事后改口径） |
|---|---|---|
| **F1** | **H1**：某票在某所的卖空占比越高，未来 1–3 个月相对同业**收益越高**（做市商承接卖压 → 库存 → 价格修复）。同族四所可聚合（Σsvol/Σtv）或取跨所离散。 | 反向长窗骨架 `multiply(group_rank(ts_rank(ts_mean(SVR,252),504), market), -1)` 的**全期 S < 1.0 或 2Y ≤ 0** ⇒ 推翻。**已测：S 1.78 / 2Y 2.35（不推翻）** |
| **F2** | **H2**：某票的成交在四所间的**份额漂移**（场所流动性迁移）含信息，且与 F1 的做空占比正交。 | 与 `value`/`volume` 类 PV 因子截面相关 > 0.9，或独立回测 \|S\| < 0.5 ⇒ 推翻。**本轮未测** |
| **F3** | **H3a**：`m` 后缀 = 月度聚合 ⇒ 该子族是**低频状态量**，可绕开日频流量比的高换手。 | 该子族的 TO 与日频 A 族同量级（>100%）⇒ 推翻。**已测：波 152 Y1 TO 140.99%、Y2 TO 100.31% ⇒ 推翻**（`m` 不是低频快照） |
| | **H3b**：`sumsize` 与 `totalvolume` 高度共线，去掉分母后**无增量信息**。 | 与 `totalvolume` 截面相关 < 0.9 且独立回测 \|S\| ≥ 1.0 ⇒ 推翻。**部分已测：波 308 T7 `S 0.27`；相关性未测** |
| **F4** | **H4**：`marketcenter` 是**离散场所编码**，对同一票同一日恒为常量 ⇒ 时序零方差，只能当分组轴。 | 若任取一票满足 `ts_std_dev(field,252) > 0`（即逐日变化）⇒ 推翻，可当信号。**未测**（见 §6 D2 缺口） |
| **F5** | **H5**：豁免卖空占卖空总量的比例 = 做市商参与度代理，可把「做市对冲」从「方向性做空」里剥出来。 | ①若该族在历史上**只有个别年份有值** ⇒ **数据层排除**（不是信号层死）；②若十年连续但 \|S\| < 0.5 ⇒ 信号层死。**已测：①成立（仅 2023 年有值）⇒ 数据层排除** |

---

## 3. 全量字段表（32/32，零抽样）

> `auc`=userCount，`aC`=alphaCount，均为 **2026-11-16 实取**。
> 更新频率一列：有 "for the day / during the reported day / for the given day / for the trading day" 字样的 = **日频（描述直证）**；`data1`/`data2` 与 `marketcenter` 无任何频率词 = **未知（平台 freq_hint 标"快照"，不可当证据）**。
> 分布一列：**全部为推断**（本仓无原始面板取值通道），推断依据写在括号里。

| # | 字段 | 类型 | cov | auc | aC | 语义（description 直译） | 更新频率 | 分布形态（推断） | 潜在 alpha 适用性 |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | `shrt43_batsshvol_svol` | MATRIX | 1.0 | 118 | **183** | 该票当日**在 BZX(BATS)** 的**卖空股数** | 日频（"on that day"） | 非负股数流量，右偏重尾；跨票量级差 4–6 个数量级（大票 vs 微盘）（推断：股数计数量） | **F1 信号腿分子**。不可单用（量级主导），必须除以同所 `totalvolume` |
| 2 | `shrt43_batsshvol_totalvolume` | MATRIX | 1.0 | 164 | **302** | 该票当日**在 BZX(BATS)** 的**总成交股数** | 日频（"on that day"） | 同上，右偏重尾（推断） | **F1 分母**；亦可单作 **F2** 场所份额分子 |
| 3 | `shrt43_byxxshvol_svol` | MATRIX | 1.0 | 69 | 98 | 该票当日**在 BYX** 的**卖空股数** | 日频（"for the day"） | 同 #1（推断） | F1 分子 |
| 4 | `shrt43_byxxshvol_totalvolume` | MATRIX | 1.0 | 77 | 122 | 该票当日**在 BYX** 的**总成交股数** | 日频（"for the day"） | 同 #1（推断） | F1 分母 / F2 分子 |
| 5 | `shrt43_edgashvol_svol` | MATRIX | 1.0 | 43 | 62 | 该票当日**在 EDGA** 的**卖空股数** | 日频（"for the given day"） | 同 #1（推断）；EDGA 体量最小 ⇒ 零值/缺值比例最高（推断） | F1 分子（**最弱的分母支撑**：同所成交量小 ⇒ 比率噪声最大） |
| 6 | `shrt43_edgashvol_totalvolume` | MATRIX | 1.0 | 34 | 47 | 该票当日**在 EDGA** 的**总成交股数** | 日频（"for the given day"） | 同 #1（推断） | F1 分母 / F2 分子 |
| 7 | `shrt43_edgxshvol_svol` | MATRIX | 1.0 | 71 | **187** | 该票当日**在 EDGX** 的**卖空股数** | 日频（"during the reported day"） | 同 #1（推断） | F1 分子 |
| 8 | `shrt43_edgxshvol_totalvolume` | MATRIX | 1.0 | 118 | **370**（全数据集最拥挤） | 该票当日**在 EDGX** 的**总成交股数** | 日频（"during the reported day"） | 同 #1（推断） | F1 分母 / F2 分子。**aC 370 ⇒ prod 风险最高的一件** |
| 9 | `shrt43_batssh_sumsize_m_data1` | MATRIX | 1.0 | 45 | **115** | `data1`（平台未披露） | **未知**（描述仅 `data1`） | **未知**（推断：非负规模量，若为「成交规模总和」则与 #2 同量级、强右偏） | **F3 未知件**。可作 `divide(sumsize_m_data1, totalvolume)` 的同单位比值探针 |
| 10 | `shrt43_batssh_sumsize_m_data2` | MATRIX | 1.0 | 31 | 37 | `data2` | 未知 | 未知（推断同上，疑为与 data1 互补的第二个统计口径） | F3 未知件 |
| 11 | `shrt43_batssh_sumsize_s_data1` | MATRIX | 1.0 | 43 | 70 | `data1` | 未知 | 未知（推断同上） | F3 未知件；`s_data1 / m_data1` 曾用于「交易粒度」机制（波 244 T06，S −0.03） |
| 12 | `shrt43_batssh_sumsize_s_data2` | MATRIX | 1.0 | 29 | 46 | `data2` | 未知 | 未知 | F3 未知件 |
| 13 | `shrt43_byxxsh_sumsize_m_data1` | MATRIX | 1.0 | 26 | 53 | `data1` | 未知 | 未知 | F3 未知件 |
| 14 | `shrt43_byxxsh_sumsize_m_data2` | MATRIX | 1.0 | 15 | 22 | `data2` | 未知 | 未知 | F3 未知件 |
| 15 | `shrt43_byxxsh_sumsize_s_data1` | MATRIX | 1.0 | 32 | 78 | `data1` | 未知 | 未知 | F3 未知件（其 252 日 rank 是 `exprs_usa_prod24_shortint43.json` 里唯一点名的 sumsize 代表） |
| 16 | `shrt43_byxxsh_sumsize_s_data2` | MATRIX | 1.0 | 14 | 31 | `data2` | 未知 | 未知 | F3 未知件 |
| 17 | `shrt43_edgash_sumsize_m_data1` | MATRIX | **0.9902** | 29 | 38 | `data1` | 未知 | 未知（**唯一两个 cov<1 的字段之一** ⇒ 有 0.98% 的票/日无值，推断为该所当日无成交） | F3 未知件；cov 缺口本身是「EDGA 流动性薄」的旁证 |
| 18 | `shrt43_edgash_sumsize_m_data2` | MATRIX | **0.9902** | 18 | 32 | `data2` | 未知 | 未知（同 #17） | F3 未知件 |
| 19 | `shrt43_edgash_sumsize_s_data1` | MATRIX | 1.0 | 35 | 50 | `data1` | 未知 | 未知 | F3 未知件 |
| 20 | `shrt43_edgash_sumsize_s_data2` | MATRIX | 1.0 | 15 | 19 | `data2` | 未知 | 未知 | F3 未知件 |
| 21 | `shrt43_edgxsh_sumsize_m_data1` | MATRIX | 1.0 | 25 | 27 | `data1` | 未知 | 未知 | F3 未知件 |
| 22 | `shrt43_edgxsh_sumsize_m_data2` | MATRIX | 1.0 | **74**（F3 内最高用户数） | **124** | `data2` | 未知 | 未知 | F3 **最拥挤件** ⇒ 「有人挖到过东西」的旁证，但也是最容易撞 prod 的一件 |
| 23 | `shrt43_edgxsh_sumsize_s_data1` | MATRIX | 1.0 | 26 | 32 | `data1` | 未知 | 未知 | F3 未知件 |
| 24 | `shrt43_edgxsh_sumsize_s_data2` | MATRIX | 1.0 | 27 | 30 | `data2` | 未知 | 未知 | F3 未知件 |
| 25 | `shrt43_batsshvol_marketcenter` | MATRIX | 1.0 | 22 | 36 | "Bats operated stock exchanges"（= 场所名，**非数值语义**） | **未知/元数据** | **推断：离散场所编码（单票单日常量）** ⇒ 时序零方差、横截面零离散 | **F4 非信号**。只能当 venue 标识 / 数据完整性校验 / 分组轴（若真为常量则分组退化） |
| 26 | `shrt43_byxxshvol_marketcenter` | MATRIX | 1.0 | 13 | 22 | 同上 | 未知/元数据 | 同上（推断） | F4 非信号 |
| 27 | `shrt43_edgashvol_marketcenter` | MATRIX | 1.0 | 13 | 14 | 同上 | 未知/元数据 | 同上（推断） | F4 非信号 |
| 28 | `shrt43_edgxshvol_marketcenter` | MATRIX | 1.0 | 8 | 11 | 同上 | 未知/元数据 | 同上（推断） | F4 非信号 |
| 29 | `count_shares_short_exempted` | MATRIX | 1.0 | 4 | 4 | 该票当日**在 EDGX** 的**豁免条款下的卖空股数** | 日频（"during the reported day"） | 非负股数；**推断：2014–2022 全为 0，仅 2023 有值**（由同族实测反推，§5.3） | **F5 数据层排除**（见 §5.3） |
| 30 | `quantity_sold_short_exempted` | MATRIX | 1.0 | 3 | 6 | **豁免**监管条款的卖空总股数 | 未知（描述无频率词）→ 推断日频 | 同上（推断；与 #29/#31 疑同源） | F5 数据层排除 |
| 31 | `total_short_exempted_shares` | MATRIX | 1.0 | 2 | 2 | 该票当日**在 EDGA** 的**豁免卖空股数** | 日频（"for the given day"） | 同上（推断） | F5 数据层排除 |
| 32 | `volume_short_exempted_trades` | MATRIX | 1.0 | 1（全数据集最冷） | 2 | 交易日**豁免分类下的卖空股数合计** | 日频（"for the trading day"） | 同上（推断） | F5 数据层排除 |

**字段级完整性核对**：编号 1–32 与 `get_datafields` 返回逐项一致，`count=32 = platform_count=32`，无截断（`pages_fetched=1`，`complete=true`）。**未抽样**。

### 3.1 四族（F1/F3/F4/F5）+ 一支（F2）的规模对照

| 族 | 字段数 | Σauc | ΣaC | 中位 aC | 语义可解释性 | 已有实测 |
|---|---:|---:|---:|---:|---|---|
| F1（svol + totalvolume 组合） | 8 | 694 | **1371** | 152.5 | **高**（描述直述） | 多波（§5） |
| F2（totalvolume 单用） | （4，与 F1 共用字段） | — | — | — | 高 | **未测** |
| F3（sumsize） | 16 | 484 | 804 | 37.5 | **低（16/16 描述只有 `dataN`）** | 波 152（2 条）+ 波 244（1 条）+ 波 308（1 条） |
| F4（marketcenter） | 4 | 56 | 83 | 18 | **非信号**（描述 = 场所名） | **未测** |
| F5（豁免卖空） | 4 | 10 | **14** | 3 | 中（描述重叠度高） | 波 152（1 条）+ 波 244（1 条） |

（ΣaC / Σauc 均为 2026-11-16 实取口径，四族合计 1371+804+83+14 = **2272** = §1 的 ΣalphaCount；Σauc 694+484+56+10 = **1244**，闭合。）

### 3.2 语义质量分级（description 是唯一语义来源 ⇒ 必须先给它打分）

| 档 | 判定 | 字段数 | 说明 |
|---|---|---:|---|
| **S 可直算** | 描述含明确计量单位与口径（shares / for the day / on `<venue>`） | **8**（F1 八件） | 可直接构造 `divide(svol, totalvolume)`，无需猜 |
| **A 可猜** | 描述说明「是什么」但缺单位/口径细节 | **4**（F5 四件） | 「exempt」三字段描述高度重叠，疑同源，必须先验共线性 |
| **C 不可解释** | 描述只有 `data1` / `data2` | **16**（F3 全部） | **不得**据字段名推断口径后直接写模板；只能先跑「同单位比值」探针 |
| **X 非信号** | 描述是场所名，非数值语义 | **4**（F4 全部） | 只能当标识/分组轴 |

⇒ **结构性事实：32 个字段里只有 8 个（25%）的语义达到「可直算」**；一半（16 个）的语义是平台**未履行披露义务**。这决定了本数据集只能走「F1 起步 → F3 靠比值探针试」的路径，不能靠读描述铺开。

### 3.3 三方取值漂移核对（2026-10-29 快照 vs 2026-11-16 实取）

| 项 | 2026-10-29 快照 | 2026-11-16 实取 | 变化 |
|---|---:|---:|---|
| 字段数 / 完整性 | 32 / complete | 32 / complete | 无 |
| 类型分布 | MATRIX × 32 | MATRIX × 32 | 无 |
| **coverage（逐字段）** | 30×1.0 + 2×0.9902 | 30×1.0 + 2×0.9902 | **零变化** |
| **userCount / alphaCount** | ΣaC **2194** / Σuc 1208 | ΣaC **2272** / Σuc 1244 | **14 / 32 字段变化**，ΣaC **+78**（约 +3.6% / 18 天） |
| 漂移最大的字段 | `batsshvol_totalvolume` 285 / 157 | **302 / 164** | +17 alpha / +7 user |
| | `edgxshvol_totalvolume` 364 / 112 | **370 / 118** | +6 / +6 |
| **数据集级 alphaCount** | 1527（模板库）/ 1492（扫描表）/ 1384（波 244 context） | **1571** | 三份旧档彼此就差 143，全部过期 |

**结论**：`coverage`/`type` 是稳定量，可跨月引用；`alphaCount`/`userCount` **不可跨月引用**（本轮 18 天就 +3.6%）。旧档之间 `alphaCount` 自相矛盾（1384 / 1492 / 1527）⇒ 任何「低拥挤 / 高拥挤」判断都必须带 asOf，且以当日实取为准。

---

## 4. 类型 / 覆盖 / 语义 三方对账

| 维度 | 平台 `get_datafields` | 本地 `data/wqb.db::field_profile` | 描述语义 | 结论 |
|---|---|---|---|---|
| **类型** | 32/32 = MATRIX | 32/32 = MATRIX | 全部为「股数 / 成交量 / 比例 / 标识」标量 | ✅ **三方一致**（无 VECTOR、无 GROUP、无 STRING）。⇒ **不需要 `vec_*` 聚合**；本轮 `preflight_expressions(auto_fix_vector=true)` 实测 `vector_fields=[]`、`any_changed=false`，与之一致 |
| **覆盖** | 30 × 1.0 + 2 × 0.9902（均值 0.999387） | 32 行，逐字段 coverage 与平台**逐项相同**（0.9902 正确落在 `edgash_sumsize_m_data1/_m_data2`） | 描述未提覆盖 | ✅ **一致**。⚠ 但**覆盖 ≠ 历史纵深**：`count_shares_short_exempted` 等 F5 四件 cov=1.0，实测却**只有 2023 年有值**（§5.3）。`cov=1.0` 只描述**横截面**覆盖，**不能**用来推断「十年都有数」 |
| **语义** | description 唯一来源 | `semantic_family` 自动分类 | — | ❌ **不一致，3 处硬矛盾**（下表） |

### 4.1 语义列的三处硬矛盾（本地自动分类 vs 描述）

| 字段 | 本地 `semantic_family` | 平台 description | 矛盾点 |
|---|---|---|---|
| `shrt43_*shvol_marketcenter`（×4） | **宏观与行业** | "Bats operated stock exchanges" | 场所标识被归成「宏观行业」⇒ **语义错误**，会导致分组/条件误用 |
| `shrt43_edgxshvol_svol` / `_edgashvol_svol` / `_byxxshvol_svol` / `_batsshvol_svol` | **风险与质量** | "Number of shares sold short …" | 日频**流量**被归成「风险质量（状态量）」⇒ 恰好会诱导写出「用 decay 平滑当状态量」的错误配方（波 151 的 TO 灾难就是这样来的） |
| `quantity_sold_short_exempted`（=其他） vs `volume_short_exempted_trades`（=价量与波动） | 两个不同族 | 两者描述都是「exempt 卖空股数合计」 | **同一语义被分到两个族** ⇒ 自动分类不可作族划分依据 |

⇒ **判定**：`field_profile.semantic_family` **不可用**（本仓 `sem_type` 全 NULL 的已知缺口，见 `Claude/skills/wq-brain-ra-usa/SKILL.md` S0 选集条目）。本文 §2 的族划分**只依据 description**，与自动分类无关。

### 4.2 口径差异（不是矛盾，但必须知道）

| 现象 | 数值 | 解释 |
|---|---|---|
| Σ字段 alphaCount > 数据集 alphaCount | 2272 vs 1571 | 一条 alpha 可同时引用多字段，**字段级 alphaCount 不可相加当数据集总量** |
| Σ字段 userCount > 数据集 userCount | 1244 vs 509 | 同上（一个用户用多字段） |
| `field_profile.n_tests = 0`（32/32 全 UNTESTED） vs DB `backtest_results` 有 **30 行** | 0 vs 30 | **已知证据通道盲区**：`field_profile` 不收录 MCP 直连仿真（`docs/operations` 口径见 `AGENTS.md` §8.11⑦）。⇒ **不得**用 `n_tests=0` 推断「本数据集从未被挖过」 |

---

## 5. 已有实测证据（全部来自本地 DB，可复算）

> 证据通道：`data/wqb.db` 的 `backtest_results`（30 行，`dataset='shortinterest43'`）+ `expressions`（30 行）+ `wave_results`（波 151/152/244 结论）+ `alphas`（平台指标）。**本轮未重跑任何一条**，也未重测 prod。

### 5.1 六波 38 条的时间线（这是「判死」口径混乱的根源）

| 波 | 日期 | 条数 | 最高 S | 结论（`wave_results.verdict`） |
|---|---:|---:|---:|---|
| **151** | 2026-10-29 | 6 | 1.51（跨所差） | FAIL —— 「换手灾难，5/6 条 TO > 100%」 |
| **152** | 2026-10-29 | ≥6 | 1.57（Y6 跨所差 group_zscore） | FAIL —— 「B 族判死 / D 族判死 / A 族是纯流量不是状态量 / eff 低一个数量级」 |
| **244** | 2026-10-29 | 10 | **0.74** | FAIL —— 「10 个结构互异模板全 FAIL；★ 找到 **regime break**；★ F5 只有 2023 年有数据」 |
| **308** | 2026-10-31 | 10 | **1.47** | （无 `wave_results` 行）—— 换到 `group_rank` + `market`/`industry` 轴后强度翻倍 |
| **309** | 2026-10-31 | 10 | **1.78** | （无 `wave_results` 行）—— TVR 消融，**TO 从 43% 压到 0.67–4.43%** |
| **311/312** | 2026-10-31 | 10+10 | 1.20 / 0.52 | PARTIAL / FAIL（收批级联结论） |

**⇒ 关键事实：波 152 的「全族判死 / 字段无收益承载能力」写于 2026-10-29，两天后被波 308/309 的实测推翻，但 `wave_results` 里没有任何一行记录这个反转**（308/309 无 `wave_results` 行）。这就是为什么 2026-11-14 的台账还在按「日频做空量=噪声」跳过本数据集。

### 5.2 最强证据：`88RKbpGl`（波 309）——**RA 全闸 + 可投资性全过**

表达式（10 个算子调用点，单数据集 ATOM）：

```
multiply(group_rank(ts_rank(ts_mean(divide(
    add(add(shrt43_batsshvol_svol, shrt43_byxxshvol_svol), add(shrt43_edgashvol_svol, shrt43_edgxshvol_svol)),
    add(add(shrt43_batsshvol_totalvolume, shrt43_byxxshvol_totalvolume), add(shrt43_edgashvol_totalvolume, shrt43_edgxshvol_totalvolume))
), 252), 504), market), -1)
```

`get_alpha_details("88RKbpGl")` 本轮实读：

| 项 | 值 |
|---|---|
| settings | USA / TOP3000 / **D1** / neutralization **SUBINDUSTRY** / **decay 4** / truncation 0.08 / nanHandling ON / maxTrade OFF / **2014-01-01 ~ 2023-12-31** |
| S / F / TO / margin | **1.78 / 1.12 / 0.0443 / 0.002248** |
| 2Y / SUB / **investability** | **2.35** / **1.31** / **invest_sharpe 1.75**（⇒ invest_S/S = **0.983**，远过 USA 0.70 闸） |
| **risk_neutralized_sharpe** | **1.30**（>1.0 ⇒ 真 alpha，不是纯风格 beta） |
| `checks.fail` | **[]**（空 ⇒ 平台 RA 硬闸全过） |
| `checks.pass` | LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / CLUSTER_TEST / LOW_2Y_SHARPE / MATCHES_PYRAMID |
| `checks.pending` | SELF_CORRELATION / DATA_DIVERSITY / **PROD_CORRELATION** / REGULAR_SUBMISSION |
| `pyramids` | `[USA/D1/SHORTINTEREST ×1.1]`，`effective=1` ⇒ **单塔 ATOM 合规** |
| long / short | 1530 / 1530（**多空对称**，非单边） |
| **prod（本地 `alphas` 列）** | **0.7908**，`prod_corr_source=check_correlation`，`corr_checked_at=2026-10-31T16:22:34` ⇒ **≥ 0.7 红线，不可提交** |

**近十年闸（`get_alpha_yearly_stats("88RKbpGl")`，本轮实跑）**：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| sharpe | 1.41 | 0.70 | 1.29 | 0.69 | 0.81 | **0.40** | 2.14 | **3.92** | **3.33** | 1.18 |
| pnl（$） | 369,977 | 129,414 | 261,310 | 166,919 | 186,063 | 80,685 | 641,842 | 1,494,318 | 1,216,352 | 385,339 |
| longCount | 1520 | 1537 | 1527 | 1518 | 1522 | 1514 | 1514 | 1535 | 1553 | 1553 |
| shortCount | 1517 | 1534 | 1535 | 1513 | 1526 | 1520 | 1519 | 1553 | 1535 | 1551 |

- **近十年闸：10/10 年 `pnl > 0` 且 `longCount > 0`、`shortCount > 0`** ⇒ **通过**（数据自 2014 起连续，回测窗 `2014-01-01 ~ 2023-12-31` 即平台为该 alpha 设定的起点）。
- ⚠ **但年际方差 = 1.268（总体）/ 1.408（样本）> 1.0** ⇒ 命中 `docs/experience/02_signal_patterns.md` 的**过拟合四信号之一「年际方差 > 1.0」**；`S < 1` 有 4 年（2015/2017/2018/2019）。强度真实但**高度集中在 2020–2022**（S 2.14 / 3.92 / 3.33）。这**不是**「全期与 2Y 反号」那种 regime artifact（全期 1.78 与 2Y 2.35 同号），但**不是均匀十年的稳定因子**。

### 5.3 F5（豁免卖空）——数据层排除，不是信号层死

`wave_results` 波 244 第 3 条（`GrW0AkgO`）：`get_alpha_yearly_stats` 显示 **2014–2022 九年 `pnl` / `longCount` / `shortCount` 全为 0，只有 2023 年有数据**（S −2.08）。
⇒ **`*_short_exempted` 四字段整族「数据层排除」**：`coverage=1.0` 只描述横截面覆盖，**不代表历史纵深**。这是本数据集最容易误判的一处——cov 满格 + 零竞争（1–4 用户），单看平台元信息会把它当成「处女地金矿」。
（另一条独立证据：波 152 `Y3 (E563OeRP)` `divide(volume_short_exempted_trades, quantity_sold_short_exempted)` S −0.97 / TO 147.13% / fRA 4 —— 两个字段相除得到的是**纯规模量**而非行为比率。）

### 5.4 F3（sumsize）——已测三次，均无信号

| 波 | 表达式骨架 | S | TO | 判读 |
|---|---|---:|---:|---|
| 152 | `Y1 (2rAE87LP)` sumsize 份额 | −0.38 | **140.99%** | 「m = 月度」假设被证伪：`m` 粒度 TO 与日频同量级 |
| 152 | `Y2 (leAxpVNn)` sumsize 份额 | −0.19 | **100.31%** | 同上 |
| 244 | `T06 (kqNkrQJP)` `ts_rank(batssh_sumsize_s_data1 / batssh_sumsize_m_data1, 252)` | −0.03 | 25.38% | 交易粒度机制无信号 |
| 308 | `T7 (2rAn8N0P)` 跨所 sumsize 比值 | 0.27 | 29.73% | 无信号 + CONCENTRATED_WEIGHT |

⇒ F3 已测 4 条、4 个不同几何，**均 |S| ≤ 0.38**。但 **`edgxsh_sumsize_m_data2`（74 用户/124 aC）从未被单字段测过**，且 16 个字段的描述仍是 `data1/data2` ⇒ 该族仍属「**语义未披露 + 强度未出现**」，按六维闸是**未穷尽**（§6 D2）。

### 5.5 F1 的「换手灾难」是怎么被解掉的（最重要的配方结论）

| 波 | 骨架 | S | TO | 结论 |
|---|---|---:|---:|---|
| 151 X1/X2 | `ts_rank(单所占比, 66)` | ∓1.32 | **102.97%** | 裸日频比率 = 换手爆炸 |
| 151 X5 | + `ts_decay_linear(·,66)` | 0.34 | 15.35% | **平滑抹掉 71% 信号** |
| 152 Y4/Y5 | `group_zscore(ts_mean(·,252), industry)` | ∓0.23 / +0.80 | 7.15% / 8.00% | 长窗均值把方向都打反 ⇒ 「水平项零信息」判读 |
| 244 T02 | `ts_rank(SVR4, 252)` | −0.45 | 18.34% | 中等窗口仍不够 |
| 244 T04 | `signed_power(ts_zscore(SVR4,504), 0.5)` | **−0.74**（全波最高） | 17.91% | 长窗 z + 饱和 = 方向对、强度不够 |
| 244 T10 | `group_rank(ts_rank(SVR4,252), subindustry)` | −0.06 | 17.19% | **「group_rank 抹信号」** ⇒ 当时判定此路不通 |
| **308 T10** | `ts_rank(…,504)` + `market` 合成 | **1.47** | 43.80% | 换 `market` 轴 + 504 窗 ⇒ 强度翻倍 |
| **309 A8** | `group_rank(ts_rank(ts_mean(SVR,252),504), market)` | **1.78** | **4.43%** | **`ts_mean(252)` 内层 + `ts_rank(504)` 外层 + `market` 轴 + `-1`** |

**★ 配方与旧结论的三处硬冲突，逐条给证据：**

1. **「group_rank 抹信号」是轴选错，不是算子问题。** 波 244 T10 用 `subindustry` 得 −0.06（相对 T02 −0.45 缩 87%），据此写进「group_rank 再次抹掉信号」；波 309 换 `market` 轴得 **+1.78**。⇒ 结论应改为：**本数据集的有效截面轴是 `market`（全市场），不是 subindustry**（做空占比的横截面分布被行业结构主导，行业内比较会把信号当噪声抹掉）。
2. **「eff 低一个数量级 ⇒ 字段没有收益承载能力」是 TO 的伪影，不是字段属性。** 波 152 用 `eff = F/S = sqrt(|R| / max(TO,0.125))` 判「全族 eff 0.05–0.41，USA 成功 band 0.587–0.622 ⇒ 字段无承载能力」。但 `88RKbpGl` 的 eff = **1.12 / 1.78 = 0.629**，**正好落在成功 band 内**——因为 TO 从 100%+ 压到 **4.43%**。公式里 TO 在分母，**用高 TO 的骨架反推「字段」属性，是把骨架缺陷记到字段账上**。
3. **「近两年失效」只在裸比率骨架上成立。** 波 151 报 X3 2Y −0.24、X6 2Y −1.27；`88RKbpGl` 2Y = **2.35**。⇒ 2Y 失效是裸比率的性质，不是字段的性质。

---

## 6. 判死六维穷尽闸核验（`AGENTS.md` §7.6）

| 维 | 合格线 | 本数据集实测 | 判定 |
|---|---|---|---|
| **D1 结构互异模板** | ≥10 | 波 244 有 10 个**明确不同的经济机制**（term structure / squeeze regime `trade_when` / Jensen gap / trade granularity / industry neutral level / acceleration / cross-venue dispersion / svr level / saturation `signed_power` / exempt composition）；波 308 另有 10 个（含 `ts_av_diff`、`ts_delta`、`ts_std_dev`、跨所 spread）；波 151 6 个 | ✅ **满足**（≥10，且有 DB 行可核） |
| **D2 每字段族 ≥1 条实测** | 5 族全覆盖 | F1 ✅ / F2 ❌**未测** / F3 ✅（4 条）/ F4 ❌**未测** / F5 ✅ | ❌ **不满足**（**F2 场所份额、F4 marketcenter 从未测**） |
| **D3 矩全家** | 水平 / 一阶差 / 二阶波动 / 比值 各 ≥1 | 水平 ✅（T02 占比水平）/ 一阶差 ✅（波 308 `T3 ts_delta22`、波 244 加速度 `ts_delta(ts_delta)`）/ 二阶波动 ✅（波 308 `T8 ts_std_dev66`）/ 比值 ✅（全部主体） | ✅ **满足** |
| **D4 分组轴** | ≥2 | `subindustry` ✅（波 244 T10）/ `industry` ✅（波 308 T2/T9）/ `market` ✅（波 309 A8）/ `sector` ❌ | ✅ **满足**（3 个） |
| **D5 非线性** | ≥1 | `signed_power` ✅（波 244 T04）/ `trade_when` ✅（波 244 T02）/ `ts_rank`（秩变换）✅；`bucket` / `ts_quantile` ❌ | ✅ **满足** |
| **D6 配置** | ≥2 套（宇宙/中性化/decay 至少变一维） | 波 244：`decay 22 / neutralization SLOW_AND_FAST`；波 309：`decay 4 / SUBINDUSTRY` | ✅ **满足**（decay + 中性化双变） |

**⇒ 判死档案结论：缺 D2（F2、F4 未测）⇒ 只能记 `PROVISIONAL`，不得记终判死，不得作为邻接数据集/族的判死先验，不得据此宣布 SHORTINTEREST 塔关闭。**

### 6.1 与各份旧档的口径对账（谁说了什么、哪条被推翻）

| 文档 | 说法 | 与 DB 事实 | 处置 |
|---|---|---|---|
| `docs/reference/USA/shortinterest3_template_library.md:271` | 「`shortinterest43` 判死（波 151+152，12 条）」 | 波 151/152 确为 FAIL，但**波 244/308/309 各 10 条**未计入；且波 309 有 RA 全闸 | **作废**（漏计 30 条） |
| `docs/reference/USA/shortinterest43_template_library.md` §4.1–4.4 | 「换手灾难 / 平滑即抹信号 / 近两年失效 / 四所聚合不提升」 | 波 151 实测成立；但 §5.5 显示换 `market` 轴 + `ts_mean252` 后 TO 4.43%、2Y 2.35 | **降级为「裸比率骨架的结论」**，不得外推到全族 |
| `docs/reference/USA/shortinterest43_template_library.md` §3.1 P7–P16「波 152 在飞 / 待发」 | 波 152 已跑（Y1–Y6） | 实际跑了 Y1–Y6，但 P7–P16 的读数未落盘 | **P7–P16 视为未测**（DB 无对应行） |
| `docs/reference/USA/shortinterest43_field_profile.md` §4.5.2 | 首波三条读数、结论「下一步补 group_zscore」 | 读数与波 151 一致 | **保留为历史证据**，结论已被 §5.5 覆盖 |
| `tracking/USA/reference/usa_s0_dataset_scan_20261114.md:14` | 「shortinterest43 … 未测（可造跨 venue 背离）」 | 已跑 38 条 | **作废**（"未测"不成立） |
| `tracking/USA/runs/usa_campaign_ledger_20261114.md:139,164` | 「32 字段全为按交易所日频做空量 + sumsize data1/2 无语义 ⇒ 按字段规则跳过（日频做空量=噪声 prior 复证）」 | 该 prior 已被波 309 推翻；且**跳过就永远看不到 88RKbpGl** | **作废**，改为「prod 已封（0.7908），非信号死」 |
| `output_report/USA_regular_alpha_delivery_20261114.md:107` | 「shortinterest 塔月频口径（shortinterest43 未测）」 | 同上 | **作废** |
| `tracking/USA/reference/usa_dead_datasets.md` | **不含** `shortinterest43`（JSON 与表格均无） | 与本文一致 | ✅ **保留**（区域判死清单本来就没收录它，这是对的） |
| `tracking/USA/reference/usa_dataset_mechanisms.md` | **无** shortinterest 条目 | 本数据集无 `classic_anomaly` 登记 ⇒ S0 排序里落到「未标注」层 | ⚠ **缺口**：应补一条（见 §8 待办） |

---

## 7. 可用性与潜在 alpha 适用性（按族给结论）

| 族 | 可用性 | 一句话结论 | 下一步唯一值得做的 |
|---|---|---|---|
| **F1 交易所卖空流量比** | **可用（信号层活）/ prod 已封 0.7908** | 反向、`market` 轴、`ts_mean252` 内层 + `ts_rank504` 外层是已知最优；S 1.78 / F 1.12 / 2Y 2.35 / invest 0.983 / rn 1.30，**唯一卡点是 prod 0.7908 ≥ 0.7** | **不重挖，先重测 prod**（记录已超 48h 保鲜期，`check_correlation(refresh=True)` 需占平台单并发槽）；若仍 ≥0.7 ⇒ 按决策表 D0-P 换轴/换窗降 prod |
| **F2 场所成交份额** | **未测，理论可用** | 描述清楚、同单位可算（`venue_i / Σ4venue`），且与 F1 的做空占比**机制正交**（一个讲「在哪交易」，一个讲「做空多少」） | 一臂探针（≤2 条）：`group_rank(ts_zscore(ts_mean(divide(tv_venue, Σtv), 66), 252), market)` |
| **F3 sumsize** | **语义未披露；4 条 \|S\|≤0.38** | 16 字段全部 `data1/data2`，口径靠猜；四次实测无信号 | 只值一条「同单位比值」探针（`sumsize_m_data1 / totalvolume`），**不再扫骨架** |
| **F4 marketcenter** | **非信号（推断）/ 未测** | 描述 = 场所名，若真为常量则时序零方差 ⇒ 只能当分组轴 | 一条 `ts_std_dev(field,252)` 判常量即可，**不占正式回测槽** |
| **F5 豁免卖空** | **数据层排除** | 只有 2023 年有值（波 244 T07 直证）+ 波 152 Y3 判死 | **不再投**（数据层排除，写明"排除"而非"信号死"） |

**塔位与配额视角**：`USA/D1/SHORTINTEREST` 现 **0/3**。F1 的 `88RKbpGl` 若能解决 prod，就是**该塔第 1 颗**；按纪律「一族一席」，本数据集最多贡献 **1 席**（F1），F2 若成立可再算一族但要先证明与 F1 不相关。

---

## 8. 开波前预注册（预注册判据，禁止事后挑选口径）

若本数据集重启（**须先经用户同意**，本轮不派发）：

| 项 | 内容 | 判据 |
|---|---|---|
| 裸强度探针 | F2 单条 + F3 单条（≤2 条，`create_multi_simulation` 一批 2 条） | \|S\| < 0.5 ⇒ 该族 kill |
| prod 探针 | 先对 `88RKbpGl` 重测 prod（`check_correlation(refresh=True)`） | 仍 ≥0.7 ⇒ F1 换轴/换窗降 prod，而不是重挖新骨架 |
| 机制归属 | 补 `usa_dataset_mechanisms.md` 一条：`classic_anomaly: true`，evidence = 做市商库存对冲（`docs/experience/02_signal_patterns.md` 的注意力/流动性族同源） | 说不出机制 ⇒ 不投槽 |
| 证伪条件 | F1：反向长窗骨架 2Y ≤ 0 或全期 S < 1.0；F2：与 PV volume 族相关 > 0.9 或 \|S\| < 0.5 | 回测后按此写归因 |
| 判死上限 | 缺 D2（F2/F4）⇒ 最高只到 `PROVISIONAL` | 不得写「SHORTINTEREST 塔关闭」 |

**待办（写给下一个会话）**：
1. 把 `shortinterest43` 从「日频做空量=噪声」的口径里摘出来（`usa_s0_dataset_scan_20261114.md`、`usa_campaign_ledger_20261114.md`、`output_report/USA_regular_alpha_delivery_20261114.md` 三处）。
2. 给 `88RKbpGl` 补 `upsert_wave_result`/`set_alpha_properties` 的归属（波 308/309 在 `wave_results` 里**没有行**，这是本次反转没被记录的直接原因）。
3. `usa_dataset_mechanisms.md` 补 shortinterest43 的机制条。

---

## 9. 复现与预检命令（本轮实际执行过的）

```text
# 全量字段（零截断）
mcp__wq-brain-http__get_datafields(region="USA", universe="TOP3000", delay=1,
    dataset_id="shortinterest43", filter_sharpe=false)          # count=32 = platform_count=32, complete=true

# 类别全景（定位用）
mcp__wq-brain-http__get_datasets(region="USA", universe="TOP3000", delay=1, category="shortinterest")   # count=6

# 塔位快照
mcp__wq-brain-http__get_pyramid_alphas()                        # USA.D1.shortinterest = 0

# 派发前预检（本轮用于验证字段存在性 + VECTOR 修复，结果 valid=true / unknown_fields=[] / vector_fields=[] / any_changed=false）
mcp__wq-brain-http__preflight_expressions(
    alpha_expressions=[
      "group_rank(ts_rank(ts_backfill(divide(shrt43_batsshvol_svol, shrt43_batsshvol_totalvolume), 252), 252), subindustry)",
      "group_rank(ts_zscore(ts_backfill(shrt43_edgxsh_sumsize_m_data2, 252), 252), subindustry)",
      "group_rank(ts_zscore(ts_backfill(divide(quantity_sold_short_exempted, volume_short_exempted_trades), 252), 252), subindustry)",
      "group_rank(ts_zscore(ts_backfill(total_short_exempted_shares, 252), 252), subindustry)"],
    region="USA", universe="TOP3000", delay=1, dataset_id="shortinterest43", auto_fix_vector=true)

# 最强候选的逐年（近十年闸）
mcp__wq-brain-http__get_alpha_yearly_stats(alpha_id="88RKbpGl")   # 2014–2023，10/10 年 pnl>0 且多空皆在仓
mcp__wq-brain-http__get_alpha_details(alpha_id="88RKbpGl")        # checks.fail=[]，invest_sharpe 1.75，rn 1.30
```

**平台回测设置（本数据集已有实测所用，非缺省）**：`USA / TOP3000 / D1 / neutralization SUBINDUSTRY / decay 4 / truncation 0.08 / pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade OFF / FASTEXPR / 2014-01-01 ~ 2023-12-31`。
⚠ 波 244 用的是 `decay 22 / SLOW_AND_FAST`，**与波 309 不同档 ⇒ 两组读数不可直接对比**（设置是强度闸，`docs/experience/02_signal_patterns.md` 已有同类实证）。

---

## 10. 结论（一段话）

`shortinterest43` 是 **32 字段全 MATRIX、覆盖 0.9994、语义只有 8/32 达「可直算」** 的 Cboe 四所日频做空流量数据集；它的 **F1 卖空占比族已经产出 RA 全闸候选 `88RKbpGl`（S 1.78 / F 1.12 / 2Y 2.35 / SUB 1.31 / invest 0.983 / risk-neut 1.30 / 失闸 0），十年逐年 pnl 全正**——即**信号层是活的**；唯一死因是 **prod 0.7908 ≥ 0.7 红线**（记录 2026-10-31，已过 48h 保鲜期未重测）。**F5 豁免卖空是数据层排除（只有 2023 年有值），F3 sumsize 语义未披露且四次实测 |S| ≤ 0.38，F2/F4 从未测 ⇒ 按六维穷尽闸只能记 `PROVISIONAL`**。所有把它写成「日频做空量=噪声判死」的旧档（2026-10-19 扫描 / 2026-10-29 模板库 / 2026-11-14 台账与交付报告）**均已被本文件 §5/§6.1 逐条对账作废**。
