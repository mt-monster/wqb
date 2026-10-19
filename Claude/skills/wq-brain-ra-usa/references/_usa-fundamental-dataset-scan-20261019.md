# USA Fundamental 数据集扫描（2026-10-19）

> **命名规范**：类别级扫描 = `_usa-<category>-dataset-scan-<asOf>.md`；
> 单数据集档案 = `_usa-<字段前缀>-field-profile-<asOf>.md`（前缀 = 平台字段前缀，如 `fnd93`）。
> **正文规范**：数据集档案一律按「字段八问」组织（见 `MEMORY.md` §7）。

## 1. 全部 23 个 fundamental 数据集（按 alphaCount 升序）

**筛选纪律**：`alphaCount < 200` 才有 prod 空间（2026-10-18 实证：prod 与拥挤度单调）。

| # | 数据集 | 名称 | 字段 | cov | **aC** | 机制 | 裁定 |
|---:|---|---|---:|---:|---:|---|---|
| 1 | **fundamental67** | Predictive Sales | 12 | 0.50 | **52** | 分类模型：5 类概率 + 应计质量 | ✗ 判死（档案 `_usa-fnd67-…`） |
| 2 | fundamental35 | US 金融机构 | 1 | 1.00 | 71 | 单字段 | 跳过（字段不足） |
| 3 | fundamental25 | Company Operating Metrics | 8 | 0.38 | 72 | 运营 KPI | 跳过（元数据为主） |
| 4 | fundamental22 | ESG Data | 14 | 0.72 | 81 | ESG | 备选 |
| 5 | **fundamental93** | **Earnings Tax Data** | 46 | 0.63 | **85** | **税务应计 / 递延税 / 盈余管理** | **★ 主攻** |
| 6 | fundamental21 | ESG Scores | 142 | 0.43 | 154 | ESG 评分 | 备选 |
| 7 | other452 | Earnings Tax Data | 46 | 0.53 | 165 | 同上（另一版本） | 备选 |
| 8 | fundamental69 | Quarterly Fundamental | 12 | 0.61 | 231 | 季频基本面 | 备选 |
| 9 | fundamental1 | Management & Executive | 205 | 0.41 | 359 | 高管/董事履历 | 备选 |
| 10 | fundamental91 | Quantitative Filings | 407 | 0.61 | 475 | 10-K/10-Q XBRL | 备选 |
| 11 | fundamental110 | Press Release | 26 | 0.82 | 773 | 财报前新闻稿 | 备选（元数据为主） |
| 12 | other416 | Quantitative Filings | 371 | 0.56 | 1711 | 10Q/8K NLP | 备选 |
| 13 | fundamental72 | Comprehensive Fundamental | 1852 | 0.75 | 3082 | 宽表 | 拥挤 |
| 14 | other466 | Aggregated Fundamental | 565 | 0.83 | 3781 | 多源聚合 | 拥挤 |
| 15 | fundamental14 | Audit Analytics Directors | 248 | 0.89 | 7574 | 董事变动 | 拥挤（编码字段） |
| 16 | fundamental13 | Comprehensive Fundamentals | 87 | 0.76 | 15273 | 三表 | 拥挤 |
| 17 | fundamental3 | US Equities 10-K/10-Q | 788 | 0.64 | 16603 | 三表 | 拥挤 |
| 18 | fundamental7 | Comprehensive Fundamentals | 311 | 0.74 | 20980 | 宽表 | 拥挤 |
| 19 | fundamental23 | Point in Time | 1637 | 0.77 | 28238 | PIT 基本面 | 拥挤 |
| 20 | fundamental17 | Direct Fundamental (FactSet) | 402 | 0.83 | 34771 | 三表+比率 | 拥挤 |
| 21 | fundamental28 | Global Fundamental | 2209 | 0.50 | 38879 | 全球宽表 | 拥挤 |
| 22 | fundamental2 | Report Footnotes | 766 | 0.44 | 141883 | 报表附注 | 极拥挤 |
| 23 | fundamental6 | Company Fundamental | 886 | 0.50 | **860417** | 宽表 | **极度过饱和，禁用** |

## 2. 主攻序（拥挤度 × 机制新颖度）

1. **fundamental93**（税务应计/递延税，aC 85）← 当前主攻
2. fundamental22（ESG，aC 81）
3. fundamental21（ESG 评分，aC 154）
4. fundamental69（季频基本面，aC 231）
5. fundamental1（高管/董事履历，aC 359）

## 3. 档案索引

| 数据集 | 档案 | 状态 |
|---|---|---|
| fundamental67 | [`_usa-fnd67-field-profile-20261019.md`](_usa-fnd67-field-profile-20261019.md) | ✗ 判死（8 条实测，S ≤0.64） |
| fundamental93 | [`_usa-fnd93-field-profile-20261019.md`](_usa-fnd93-field-profile-20261019.md) | 进行中 |

---

## 4. 进展与首批读数（2026-10-19 12:00）

| 数据集 | 条数 | 最高 S | 判定 | 关键读数 |
|---|---:|---:|---|---|
| fundamental67 | 8 | 0.64 | **判死** | 分类概率/标签：CW 0.44–0.48；ts_rank 后 S→0.05 |
| fundamental93 | 12 | 0.99 | **判死** | 5 维度×3 结构；backfill 把 TO 压到 0.0095 撞 LOW_TURNOVER；最高分来自"资产变化"（规模代理） |
| fundamental21 | 4 | **1.25** | **SUB 卡死** | pulse 水平 S1.25/F0.71/2Y1.12，但 **SUB 0.17（限 0.54）**；momentum Δ63 S1.23/SUB 0.43 |

### 三条结构性结论（本战役新增）

1. **低 alphaCount ≠ 有信号**（第三次验证）：f67(aC52) 最高 S 0.64、f93(aC85) 最高 S 0.99。
2. **季频低覆盖字段的「覆盖率 ↔ 换手地板」不可兼得**：`ts_backfill` 救覆盖（1:6 失衡 → 1:1），
   但 TO 从 0.17 掉到 0.0095，直接撞 `LOW_TURNOVER(0.01)`。
3. **ESG 类（f21）的瓶颈是 SUB 而非 S**：`SUB/S ≈ 0.14`（需 0.435）⇒ 信号只在大盘有效，
   与「ESG 覆盖天然偏大盘」一致；这类数据在 TOP3000 的子宇宙里没有 alpha。

---

## 5. 追记：`fundamental91`（8-K 披露 NLP，407 字段 / aC 475）判死

**字段结构**（cov≥0.55 共 341 个）：`cat#` 273 个（8-K 分类 NLP）、`sentiment1/2` 15、`topic` 20、
`readability` 3、`measure` 5、`numeric_count` 1 —— 全 **VECTOR**（需 `vec_avg`）。

| 机制（文献依据） | 字段 | S | F | 2Y | SUB | 判定 |
|---|---|---:|---:|---:|---:|---|
| 披露可读性（低可读=坏消息掩饰） | `readability_0` | 0.02 | 0.00 | −0.46 | −0.03 | ✗ |
| 披露可读性（第二维） | `readability_1` | 0.58 | 0.27 | 0.33 | 0.14 | ✗ |
| 数字密度（信息量代理） | `numeric_count` | 0.23 | 0.07 | −0.05 | 0.21 | ✗ |
| 8-K 情绪 | `sentiment1_0` | 0.18 | 0.04 | −0.40 | 0.30 | ✗ |

**判死理由**：4 类机制（可读性/信息密度/情绪/第二可读性维）S 全 ≤0.58，且 2Y 多为负
⇒ 8-K 披露的 NLP 特征在 TOP3000 **无截面预测力**（8-K 事件稀疏 + 已被快讯消化）。

---

## 6. ★ 类别级最终结论（2026-10-19 全日 50 条实测）

| 类别 | 测试数据集 | 条数 | 最高 S | 最优读数 | 结论 |
|---|---|---:|---:|---|---|
| **Fundamental** | fundamental67 / 93 / 21 / 17 / 91 | 32 | **1.43**（f21 ESG） | SUB 0.52（限 0.62） | **无法产出 ATOM** |
| **ShortInterest** | short_interest_pred / us_short_sale / shortinterest3 / shortinterest29 | 17 | **1.07**（借券反向） | SUB 0.13–0.24 | **无法产出 ATOM** |

**五条硬结论（可直接用于未来选类别）**：

1. **在 USA/TOP3000，Fundamental 与 ShortInterest 两个类别都过不了 S 闸**：
   低 aC 集（f67 52 / f93 85 / f21 154 / 借券 81）信号强度天花板 **S 0.6–1.4**；
   高 aC 集（f6 86万 / f2 14万 / f17 3.5万）有强度但 prod 必爆。
2. **「低拥挤」与「有信号」在本市场是负相关的**（第 4 次验证）：aC 52 的 f67 最高 S 0.64，
   aC 81 的借券反向 S 1.07；而能出货的 analyst_factor_signals 是 aC 6 的字段 + **特定机制（增长率）**。
3. **借券利用率是本类别里唯一有方向的信号**（反向 S 1.0–1.07、2Y 1.7–2.0），
   但差 S 0.5 / SUB 0.3，**且尾部门控（挤空假说）实测更差** ⇒ 无杠杆可用。
4. **8-K / ESG / 税务应计 / 分类模型输出**四类 alt-data 在 TOP3000 均无截面 alpha（S ≤1.43）。
5. **破 ATOM 的配方不普适**：`winsorize+ts_backfill+hump+decay1` 在 analyst 增长族上是四赢，
   在 ESG 上把 TO 压到 0.0089 撞地板、2Y 从 1.45 掉到 1.39 ⇒ **换集必重测**。

⇒ 当日唯一 ATOM：`omoK1A5m`（analyst_factor_signals，已 ACTIVE/OS）。
⇒ 若继续追 10 颗目标，**建议回到 analyst_factor_signals 的其它增长/修正族**
（900+ 字段，仅"增长率"一族已验证出货），而不是在 Fundamental/ShortInterest 上继续投入。

---

## 7. 追记（三轮）：用「按形态选模板」+「内层 GN」重测 Fundamental —— 结论：**过度加工**

**动机**：analytic 侧靠 `ts_zscore 归一 + 内层 group_neutralize + winsorize/backfill` 出了两颗 ATOM，
用同一套重测此前失败的 Fundamental 集。

### 7.1 新模板在 Fundamental **全面变差**

| 数据集 | 字段/机制 | 旧最佳 | 新模板（zscore+GN+winsorize+backfill） | 变化 |
|---|---|---:|---:|---|
| f21 | pulse−insight 背离 | **1.43** | 1.01 | **−0.42** |
| f21 | pulse 水平 | 1.25 | 1.14 | −0.11 |
| f93 | accruals z 分 | 0.99 | 0.66 | −0.33 |
| f93 | tax_accruals_11 | 0.87 | 0.59 | −0.28 |

⇒ **根因：过度加工**。Fundamental 字段本身已是**比率 / z 分 / 评分 / 率**
（`fnd93_accruals_d1_current_t` 本身就是 z 分、`fnd21_*` 本身是 0–100 评分），
再叠 `ts_zscore + winsorize + backfill + GN` 等于重复归一化 ⇒ 抹掉原始信息。
**analyst 的成长率是"裸率"，才需要归一化**。

### 7.2 内层 GN 在 f21 上只抬 2Y、不救 SUB

| 结构 | S | F | 2Y | SUB | 需要 |
|---|---:|---:|---:|---:|---|
| 无 GN（对照 `9qERxn91`） | **1.43** | 0.94 | 1.52 | **0.52** | — |
| GN(industry) + market 轴 | 1.42 | 0.93 | **1.57** | 0.50 | — |
| GN(sector) + market 轴 | 1.38 | 0.90 | 1.47 | 0.51 | — |
| GN(sector) + industry 轴 | 1.35 | 0.83 | 1.50 | 0.40 | — |

**2Y 只能抬到 1.57（闸 1.58）而 SUB 反降到 0.50（闸 0.61）** —— 与 2026-10-19 上午的
「hump 保 S 但杀 SUB/S 比值」是同一现象的延续。

### 7.3 Fundamental 类目最终判定（累计 40 条 / 5 数据集 / 2 套模板）

| 判据 | 结论 |
|---|---|
| S 上限 | **1.43**（f21 ESG 背离，`9qERxn91`）距闸 0.15 |
| SUB 上限 | **0.52**（需 0.62）；且所有能抬 S 的杠杆都会**同时压低 SUB/S 比值** |
| 新模板 | **有害**（−0.11 ~ −0.42） |
| 内层 GN | 只抬 2Y（+0.05），不救 SUB |
| ⇒ | **Fundamental 在 USA/TOP3000 结构性无法产出 ATOM**（除非换 universe，纪律禁止） |

**★ 可迁移纪律（新增）**：
> **同一套叠加算子不能跨"字段加工深度"复用**：
> - **裸率/原始量**（analyst 成长率）→ 可叠 `zscore + winsorize + backfill + GN`（越叠越强）；
> - **已加工量**（比率 / z 分 / 评分 / 斜率）→ **只能做轻加工**（`hump + group_rank`），
>   再叠归一层 = 过度加工，S 掉 0.1–0.4。
> 判别方法：看字段定义里有没有 "z-score / ratio / percent / score / slope" —— 有就不叠。
