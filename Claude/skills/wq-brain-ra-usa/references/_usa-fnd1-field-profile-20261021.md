# fundamental1（Management and Executive Data）字段画像 · 字段八问

> 命名：`_usa-<字段前缀>-field-profile-<asOf>.md`，前缀 = 平台字段前缀 **fnd1**
> **as_of**：2026-10-21 ｜ 状态：**Wave 1 探针进行中**
> 上游选区依据：`_usa-fnd21-field-profile-20261021.md` §0（23 个 USA Fundamental 数据集排序，本集列第 6 位「备选（cov 低）」）；
> fnd91 于 2026-10-21 封存后的下一个候选（fnd91 封存理由见该文件 §6）。

---

## §0 为什么是 fnd1

**一句话**：这是 USA Fundamental 里**唯一一个把「人」作为横截面维度**的数据集——董事会/高管的规模、任期、继任压力、流失率、兼职数、性别比、薪酬对齐。它与平台生产池的 value / quality / momentum / analyst 全部异源，且 **aC 合计只有 479**（fnd17 是 34771，fnd13 是 15273），是整个 Fundamental 类别里最不拥挤的一档。

三条硬理由：

1. **白空间实测**：`scan_fields` 的 `userCount==0` 清单里有 11 个 **cov ≥ 0.5** 的字段，其中 `fnd1_numberdirectors`（董事会人数）、`fnd1_director_characteristics_timeinco`、`fnd1_filtered_stdevtimebrd` 等 6 个是 **cov 0.798–0.800、longCount 2395–2399、uC=0、aC=0** —— 近全覆盖且**零人用过**。这在 USA 极罕见。
2. **覆盖率不是 0.41 那个数**：数据集级 avg cov 0.41 被 101 个低覆盖薪酬/期权字段拉低。按字段数看，**74 个字段落在 0.7–0.9 档，longCount 中位数 2395/3000**（80% 宇宙）——治理结构族本身是近全覆盖的，不需要为覆盖率做特殊处理（但仍按 fnd91 定律加 `ts_backfill` 兜住报告空窗）。
3. **机制自带经济学结论**：董事会规模（Yermack 1996）、兼职董事（Fich & Shivdasani 2006；Masulis-Wang-Xie 2012）、继任风险、薪酬-业绩敏感性（Core & Guay 1999）都是**已被文献定价过的方向**，不需要现编故事。

**与 fnd91 的关键差别**：fnd91 是**事件驱动**（8-K 落地），本集是**年度快照**（AnnualReportDate）。后者的换手天然更低、信号更慢——这既是优点（review 换手带 5%–30% 容易满足）也是风险（平台 LOW_TURNOVER 底线 1% 可能踩不到，见 §3.2 结构判据）。

---

## §1 字段全景（205 platform / 全部 VECTOR / 179 过 MCP sharpe 过滤）

### ① 是什么

董事会与高管履历数据：每位董事/高管的薪酬、期权、兼任董事席位、任职年限、退休时间、学历资格，以及公司层聚合（人数、性别比、年龄/任期标准差、继任压力、流失率）。数据按 **年度报告日（AnnualReportDate）** 刷新。

### ② 类型

**VECTOR 205/205**。⇒ 所有标量算子前必须先聚合。本集提供 7 个向量算子：
`vec_avg` / `vec_max` / `vec_min` / `vec_sum` / `vec_count` / `vec_stddev` / `vec_range`。
本批 Wave 1 用 `vec_avg`（董事均值）与 `vec_count`（董事人数），Wave 2 起按机制补 `vec_stddev`（董事会内部异质性）/ `vec_min`（最近退休者）。

### ③ 覆盖（按字段数，longCount = 有值股票数 / TOP3000）

| 覆盖档 | 字段数 | longCount 中位 | 代表字段 |
|---|---:|---:|---|
| 0.7–0.9 | **74** | **2395** | `fnd1_filtered_genderratio` .7984、`fnd1_filtered_succession` .7984、`fnd1_filtered_numberdirectors` .7984、`fnd1_filtered_stdevage` .7981、`fnd1_board_characteristics_filtered_timeinco` .7984、`fnd1_board_characteristics_filtered_totcurrnolstdbrd` .7984、`fnd1_numberdirectors` .7999、`board_nationality_diversity_ratio` .7621 |
| 0.5–0.7 | 8 | 1726 | `fnd1_filtered_attrition3yr` .6715、`director_attrition_ratio_3yr` .6828、`total_other_listed_boards_count` .5519、`director_total_other_listed_boards_count` .5469 |
| 0.3–0.5 | 22 | 949 | 薪酬总额/期权档案（`total_director_cash_comp` .2078 除外）、`director_current_other_listed_boards_count` .3041、`current_other_listed_boards_count_2` .3708 |
| 0.1–0.3 | 63 | 592 | 薪酬组件（`total_director_cash_comp` .2078、`aggregate_director_compensation` .2014、`compensation_change_percent_2` .1775）、持股价值（`total_shareholding_value` .193、`wealth_sensitivity_to_stock` .1952）、`equity_linked_compensation_ratio_2` .1784 |
| <0.1 | 38 | 29 | 期权计划碎片（`bonus_to_compensation_ratio` .0026、`incentive_expired_option_volume` .0003、`expected_*` 近零档） |

**口径注意（2026-10-21 实测）**：MCP `get_datafields` 缺省会套 sharpe 过滤（返回 `sharpe_filter_applied:true`、`sharpe_filter_removed:26`），只给 179 个；`tools/scan_fields.py` 的 `platform_count=205` 才是全量。两处差异 26 个字段**不是字段不存在**，是全量底表里的低 sharpe 档。做「全部字段梳理」必须用后者。

### ④ 更新频率

- 名义：**年度**（AnnualReportDate）；
- 实际：**按公司年报落地日错峰更新**，全市场集中在 2–4 月（10-K 季）；
- 董事进出会触发个别向量元素变化，但公司层聚合仍以年报节奏为主。

⇒ 后果：横截面排名只在「本公司换值 / 他人换值」时变化，**换手天然偏低**。本集的结构性风险不是覆盖率（fnd91 那种 NaN 块），而是 **LOW_TURNOVER（平台底线 1%）**。Wave 1 的 10 条里专门放了 2 条变化型（G10 `ts_delta`、G9 rank+group_backfill 结构对照）来测量这一维。

### ⑤ 量纲 / 分布（未做 Labs 直读，机制判读）

| 族 | 量纲 | 分布形态 | 处理 |
|---|---|---|---|
| 比率（gender ratio、equity-linked ratio、attrition、succession） | 0–1 有界 | 右偏/双峰 | `group_zscore` 足够 |
| 计数（numberdirectors、other boards） | 小整数 | 强右偏 | 先 `winsorize(std=3)` 再 z-score |
| 年限（timebrd/timeinco/timeretirement） | 年 | 右偏、长尾 | 同上 |
| 薪酬/期权金额 | 美元 | 极端右偏（跨 4 个数量级） | **不用水平值**；只作比率或 log 后的对齐度；且需按市值尺度化（本集无市值字段 ⇒ 金额类只做比率） |

**覆盖 < 0.4 的字段一律先 `ts_backfill(x,252)`，再做截面**（fnd91 定律：`group_rank` 把 NaN 排到组内最低档，不 backfill 就是在赌覆盖率，不是在测治理）。本批 10 条全部带 `ts_backfill`。

---

## §2 机制地图（9 个机制，不限于 8）

| # | 机制 | 经济逻辑 | 代表字段 | 预期方向 | 文献 |
|---|---|---|---|---|---|
| M1 | **董事会规模** | 大董事会 = 协调成本高、监督搭便车 | `fnd1_filtered_numberdirectors`、`vec_count(...)` | 规模↑ → 收益↓ | Yermack (1996) |
| M2 | **继任风险** | 董事年龄挤在退休区 ⇒ CEO/董事更替不确定性 | `fnd1_filtered_succession`、`timeretirement` | 风险↑ → 折价 | — |
| M3 | **管理层不稳定** | 3 年流失率高 ⇒ 战略不连续、执行风险 | `fnd1_filtered_attrition3yr` | 流失↑ → 收益↓ | — |
| M4 | **过度兼职** | 一人兼多家上市公司董事 ⇒ 注意力稀释、监督弱化 | `fnd1_board_characteristics_filtered_totcurrnolstdbrd` | 兼职↑ → 收益↓ | Fich & Shivdasani (2006)；Masulis et al. (2012) |
| M5 | **任期/堑壕** | 任期过长 ⇒ 管理层固化、外部监督弱 | `fnd1_board_characteristics_filtered_timeinco` | 任期↑ → 收益↓ | — |
| M6 | **董事会多样性** | 性别/国籍多样性 ⇒ 决策质量 | `fnd1_filtered_genderratio`（男比例）、`board_nationality_diversity_ratio` | 男比例↑ → 收益↓ | Adams & Ferreira (2009) |
| M7 | **薪酬-业绩对齐** | 权益型薪酬占比高 ⇒ 代理成本低 | `equity_linked_compensation_ratio_2` | 对齐↑ → 收益↑ | Core & Guay (1999) |
| M8 | **人力资本** | 学历资格数量/分散度 ⇒ 决策能力 | `fnd1_board_characteristics_filtered_noquals`、`stdevnoquals` | 资质↑ → 收益↑ | — |
| M9 | **董事会异质性** | 年龄标准差大 ⇒ 视角多元 vs 代际冲突 | `fnd1_filtered_stdevage`、`vec_stddev(timeinco)` | 方向待测 | — |

**未纳入本批的机制及理由**：董事持股/财富（`total_shareholding_value` / `wealth_sensitivity_to_stock`）—— 金额量纲且本集无市值字段，水平值等于市值代理，`rank` 后会变成 size beta；留到 Wave 2 用「占薪酬倍数」或「人均」间接构造。期权计划碎片（38 个 <0.1 覆盖字段）—— `longCount` 中位 29，截面不可用。

---

## §3 Wave 1 预注册（10 条 / 6 机制 + 1 结构对照 + 1 变化型）

### 3.1 表达式

| # | 机制 | 表达式 | 方向假设 |
|---|---|---|---|
| G1 | M6 多样性 | `-winsorize(group_zscore(ts_backfill(vec_avg(fnd1_filtered_genderratio),252),subindustry),std=3)` | 男比例高 → 差 |
| G2 | M2 继任风险 | `-winsorize(group_zscore(ts_backfill(vec_avg(fnd1_filtered_succession),252),subindustry),std=3)` | 风险高 → 差 |
| G3 | M3 流失 | `-winsorize(group_zscore(ts_backfill(vec_avg(fnd1_filtered_attrition3yr),252),subindustry),std=3)` | 流失高 → 差 |
| G4 | M4 兼职 | `-winsorize(group_zscore(ts_backfill(vec_avg(fnd1_board_characteristics_filtered_totcurrnolstdbrd),252),subindustry),std=3)` | 兼职多 → 差 |
| G5 | M5 任期 | `-winsorize(group_zscore(ts_backfill(vec_avg(fnd1_board_characteristics_filtered_timeinco),252),subindustry),std=3)` | 任期长 → 差 |
| G6 | M1 规模 | `-winsorize(group_zscore(ts_backfill(vec_count(fnd1_board_characteristics_filtered_timeinco),252),subindustry),std=3)` | 董事会大 → 差 |
| G7 | M9 异质性 | `winsorize(group_zscore(ts_backfill(vec_avg(fnd1_filtered_stdevage),252),subindustry),std=3)` | 年龄分散 → 好（待验） |
| G8 | M7 对齐 | `winsorize(group_zscore(ts_backfill(vec_avg(equity_linked_compensation_ratio_2),252),subindustry),std=3)` | 权益薪酬占比高 → 好（稀疏探针 cov .178） |
| G9 | M2 结构对照 | `-group_rank(group_backfill(ts_backfill(vec_avg(fnd1_filtered_succession),252),subindustry,252),subindustry)` | 同 G2，但 NaN 用组均值填 + rank |
| G10 | M3 变化型 | `-winsorize(group_zscore(ts_delta(ts_backfill(vec_avg(fnd1_filtered_attrition3yr),504),252),subindustry),std=3)` | 流失率同比抬升 → 差 |

**结构选择理由**：G1–G8/G10 用 `group_zscore`（**NaN 保留**，缺失股票不进组合，避免 fnd91 那种「缺失块 = 空头」的覆盖率赌注）；G9 用 `group_backfill` + `group_rank`（把 NaN 填成组内均值，全宇宙进组合），两者在**同一字段**上构成结构 A/B 对照。`winsorize(std=3)` 仅压 z-score 尾部（preflight 会把 `std` 误报成字段，属已知假阳性）。

### 3.2 结构判据（先于指标判定，避免再看错）

1. **换手地板**：若 10 条全部 TO < 1%，本集在年度快照下触不到平台底线 ⇒ 换手不是算子问题，是数据频率上限；此时只保留 `ts_delta` / 事件型结构，其余机制标记为「频率不可用」。
2. **覆盖率对称性**：G1–G8/G10 的 long/short 应大致对称（z-score 保留 NaN）；若出现 1:3 级别的偏斜，说明 `group_zscore` 并未保留 NaN（与预期不符），需改用 `group_backfill` 统一兜底。
3. **G2 vs G9**：同字段、同符号，若 S 差 > 0.3 或持仓结构显著不同，则结构（NaN 处理）比机制贡献更大 ⇒ 后续所有机制都要先做结构对照再判死。

### 3.3 判死线

- 单机制：G1–G7/G9/G10 中任一机制若 |S| < 0.5 且 TO 正常，记「机制弱，非结构问题」，不再为该机制扩变体；
- 数据集级：若 6 个机制里 ≥ 5 个 |S| < 0.5，且 G9 结构对照也无法把 G2 抬到 0.8 以上，则本集判「治理数据在 USA 无独立溢价」，转下一候选（fnd22 ESG / fnd110 Press Release / fnd14 董事变动）。

### 3.4 论坛取证（2026-10-21，两条直接约束本集设计）

| 来源 | 结论 | 对本集的用法 |
|---|---|---|
| `GLOBAL-TURNOVER-STRENGTH-FRONTIER-SHARP-EVENT`（DB registry） | 事件型信号一律优先 `group_rank`，`group_zscore` 会被离群/NaN 缺口破坏（-0.19 vs 0.94）；`ts_backfill` 是唯一三赢杠杆（TO、CW、S/2Y 同时改善）；轻量平滑把 |S| 腰斩 ⇒ 事件型不可平滑 | 本集是**慢变量横截面**，`group_zscore` 是文献认可的适用场景；G9 用 `group_rank` 作结构对照正是为了验证这一条在本集是否反号 |
| 论坛帖 `42065262268567`【换手治理】（45 赞 / 11 评） | `decay=0` 与 `decay=1` 输出逐位相同；decay 每加 1，时效性单调下降；`winsorize(std=3)` + `group_rank` 稳定截面排序比外层 `ts_mean` 平滑更自然 | 若 Wave 1 换手落进 5%–30% 带则**不要动 decay**；若 <1%，先试 decay 5→2（便宜杠杆），不要加 `ts_decay_linear`（会同时压掉年度跳变信息） |

---

## §4 实测结果

### 4.1 Wave 1 收批（2026-10-21 06:43，multisim `4F1pzocGf4NqaTruXeYpRRQ`，10/10 COMPLETE）

设置回读已核：`USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / maxTrade OFF / nanHandling ON / pasteurization ON / unitHandling VERIFY`。

| # | alpha | 机制 | 字段 | S | F | 2Y | SUB | TO | CW | 判定 |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| G1 | `YPxbRNJo` | M6 多样性 | `genderratio` | 0.16 | 0.03 | −0.56 | −0.16 | 2.82% | pass | 死 |
| G2 | `vROrW5Pz` | M2 继任 | `succession` | 0.67 | 0.32 | 1.04 | 0.33 | 2.83% | pass | 弱（风格 beta） |
| **G3** | **`58jzPLY5`** | **M3 流失** | **`attrition3yr`** | **1.12** | **0.60** | **2.26** | **0.59** | **2.57%** | pass | **最强** |
| G4 | `omoLxnkv` | M4 兼职 | `totcurrnolstdbrd` | −0.55 | −0.20 | −1.34 | −0.28 | 2.61% | pass | 反号可救 |
| G5 | `xA13JeEl` | M5 任期 | `timeinco` | −0.61 | −0.33 | −1.25 | −0.27 | 2.18% | pass | 反号可救 |
| G6 | `pwvR9nko` | M1 规模 | `vec_count(timeinco)` | −0.34 | −0.14 | −0.62 | −0.32 | 3.11% | pass | 死 |
| G7 | `d5KbNn6K` | M9 异质性 | `stdevage` | −0.60 | −0.21 | −0.76 | −0.33 | 2.61% | pass | 反号可救 |
| G8 | `e76bXnZp` | M7 对齐 | `equity_linked_comp_2` | −0.27 | −0.09 | −0.19 | −0.20 | 1.98% | **FAIL 0.50** | 死（cov .178） |
| G9 | `2rjw3voJ` | M2 结构对照 | `succession` group_rank | 0.53 | 0.21 | 0.96 | 0.14 | 2.47% | pass | 结构更差 |
| G10 | `omoLxn0k` | M3 变化型 | `ts_delta(attrition)` | 0.01 | 0.00 | 0.92 | −0.54 | 4.37% | pass | 死 |

### 4.2 三条预注册判据的裁决

1. **换手地板：未触发。** 10/10 TO ∈ [1.98%, 4.37%]，全部高于平台 1% 底线 ⇒ 年度快照**不是**「频率不可用」。但全部低于 USA review band 的 5% 下限，属本集固有低频特征（年更 + 日内无新信息），后续不再把换手当求解目标。
2. **覆盖率对称性：通过。** G3 long/short = 1352/1006（57/43），G1 1330/1503，G2 1608/1217，G9 1543/1512 ⇒ `group_zscore` 确实保留了 NaN，**没有 fnd91 那种「NaN 块被压到单侧」的伪信号**。G8 的 350/290 是真稀疏（cov .178），不是结构问题。
3. **G2 vs G9：结构不是主因。** S 0.67 vs 0.53，Δ=0.14 < 0.3 判据；持仓 2825 vs 3055 亦同量级 ⇒ 机制贡献为主。且**慢变量上 `group_zscore` 优于 `group_rank`**，与库内「事件型用 rank」法则方向相反（该法则适用事件型，本集是横截面慢变量，用 zscore 正确）。

### 4.3 逐年归因（决定性发现）

| 年度 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | **2020** | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| G3 attrition | 0.99 | 2.11 | 0.54 | 0.17 | 2.14 | 0.74 | **−2.46** | 1.54 | 2.68 | 1.68 |
| G2 succession | 1.00 | 1.59 | 0.81 | −1.67 | 0.71 | 0.68 | **−2.77** | 2.28 | 1.91 | −0.61 |
| G5 tenure（负号） | −0.66 | −1.19 | −0.67 | 0.25 | −0.92 | −0.32 | **+3.76** | −1.81 | −1.85 | −0.22 |

- **2020 是唯一大负年，且三条信号同时翻号**。这不是三个机制同时失效，而是**同一个「治理质量 vs 困境/投机」风格轴在 2020 被整体反向定价**（高流失、高更替、任期短的困境股在流动性行情中暴涨）。
- 因此 G3 的全期 S=1.12 被单年压低：其余 9 年多数为正（2.11 / 2.14 / 1.54 / 2.68 / 1.68）。
- `risk_neutralized_sharpe` 给出同一结论：G3 **0.93**（保留 83%，真实特质）、G5(−) **0.60**（保留 98%）、G2 **0.09**（保留 13% ⇒ **G2 主要是风格 beta，降级不作主力**）。
- **推论**：本集所有机制共享同一条风格轴，**多机制组合不会带来分散化**；能治 2020 的只有「削减极值暴露」与「改中性化域」，不是继续换字段。这直接决定 Wave 2 的设计。

### 4.4 机制排序与判死线复核

|S| 排序：M3 流失 **1.12** ≫ M2 继任 0.67 > M5 任期 0.61 > M9 异质性 0.60 > M4 兼职 0.55 > M1 规模 0.34 > M7 对齐 0.27 ≈ M6 多样性 0.16 > M3-变化型 0.01。

**判死线未命中**：|S| ≥ 0.5 的机制有 5 个（M3/M2/M5/M9/M4），远多于「≥5 个 <0.5」的判死条件 ⇒ 本集保留，继续在 fnd1 内推进。

### 4.5 Wave 2 的因果依据（不是盲扫）

Wave 1 只留下三个可推进的问题，每个对应一组表达式：

| 问题 | 依据 | Wave 2 动作 |
|---|---|---|
| Q1 2020 的伤害是否集中在空头极值？ | 2020 单一负年，高流失股暴涨 | M3 的尾部压到 `std=2` 与 `group_rank`（有界）两种压尾法对照 |
| Q2 流失率的最优时间窗是哪个？ | `attrition3yr` cov .6715；兄弟字段 `director_attrition_ratio_2` cov .6931 / `_3yr` cov .6828 | 2yr vs 3yr 同期对照（同机制不同窗，不是换概念） |
| Q3 M5 反号是否稳健？ | G5 逐年 9/10 年同号，RN 保留 98% | 正号 tenure 用 zscore 与 rank 各一 |
| Q4 剩余未测的高覆盖机制（M2 备选 / M8 / M9 离散度） | 三者在 0.798 覆盖档且 aC ≤ 15，从未被本集测过 | 各一条，各带独立经济含义 |
| Q5 SUBINDUSTRY 是否过碎？ | 3000 只股票 ÷ 约 200 个 subindustry ≈ 15 只/组，组内 z-score 噪声大；治理质量是行业内公司特质 | 同结构在 `industry`（约 70 组 ≈ 43 只/组）重跑 5 条 |

Q5 是**设置层**问题，用独立 multisim（同字段同结构，只换中性化域），不混进 Q1–Q4 的批。

### 4.6 Wave 2 收批（2026-10-21，15 条 / 两个 multisim）

设置与 Wave 1 完全相同（USA/TOP3000/D1、decay 5、trunc 0.08、nanHandling ON、maxTrade OFF、2014-01-01→2023-12-31），
唯一变量是中性化域。两批均 10/10、5/5 COMPLETE，设置已回读确认。

**Wave 2A（SUBINDUSTRY，multisim `9fJgU9xt5ee8G6cfxhLaMg`，10 条）**

| # | 对应问题 | 表达式要点 | alpha | S | F | 2Y | SUB | TO | rns |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Q1 压尾 | attrition3yr zscore `std=2` | `e76Ql7xl` | 1.08 | 0.56 | 2.20 | 0.59 | 2.54% | 0.90 |
| 2 | Q1 有界压尾 | attrition3yr `group_rank` | `qME0KM6P` | **0.06** | 0.01 | 0.54 | 0.16 | 2.07% | 0.64 |
| 3 | Q2 2 年窗 | `director_attrition_ratio_2` | `RRA6JR1b` | 1.04 | 0.58 | 1.61 | 0.49 | 2.92% | 0.84 |
| 4 | Q2 3 年窗 | `director_attrition_ratio_3yr` | `P0MgJ0OL` | 0.91 | 0.45 | 1.56 | 0.43 | 2.68% | 0.79 |
| 5 | Q1 聚合对照 | `vec_max`(attrition3yr) | `kqJgxqPl` | 1.06 | 0.53 | 2.16 | 0.57 | 2.46% | 0.88 |
| 6 | Q3 任期正号 | timeinco zscore | `E5VRZ5GG` | 0.61 | 0.33 | 1.25 | 0.27 | 2.18% | 0.60 |
| 7 | Q3 任期 rank | timeinco `group_rank` | `vRO2KRjG` | 0.77 | 0.45 | 1.44 | **0.21 ✗** | 2.16% | 0.74 |
| 8 | Q4 未测机制 | timeretirement 正号 | `gJWZYJQO` | −0.32 | −0.12 | −0.79 | 0.08 | 2.62% | 0.59 |
| 9 | Q4 未测机制 | noquals 正号 | `pwv5qwP6` | 0.37 | 0.09 | 0.19 | 0.31 | 2.59% | 0.22 |
| 10 | Q4 未测机制 | stdevtimeincompany 正号 | `RRA6JRVo` | 0.50 | 0.25 | 1.12 | 0.28 | 2.24% | 0.35 |

**Wave 2B（INDUSTRY，multisim `26GMULeRH5bM8K116s6OrJoz`，5 条）**

| # | 对应问题 | 表达式要点 | alpha | S | F | 2Y | SUB | TO | rns |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Q5 域对照 | attrition3yr zscore | `rKde1pWd` | 1.10 | **0.63** | 2.09 | 0.48 | 2.41% | 0.84 |
| 2 | Q5 域对照 | attrition3yr `group_rank` | `XgRJjmpm` | −0.04 | 0.00 | 0.40 | 0.08 | 1.87% | 0.57 |
| 3 | Q5 域对照 | timeinco 正号 | `LL5ZPVp1` | 0.61 | 0.36 | 1.20 | 0.28 | 1.93% | 0.69 |
| 4 | Q5 域对照 | succession 负号 | `E5VRZOem` | 0.65 | 0.35 | 0.90 | 0.28 | 2.62% | **0.07** |
| 5 | Q5 域对照 | director_attrition_ratio_2 | `omoW18gb` | 1.07 | **0.68** | 1.68 | 0.50 | 2.78% | 0.82 |

**Q1–Q5 逐条裁决**

1. **Q1 压尾：不是极端空头的问题。** `std=2`（1.08）低于 `std=3`（1.12），`group_rank` 直接崩到 0.06 / −0.04。
   ⇒ 2020 的伤害来自**整条截面的同向翻转**，不是少数极值股；压尾或改秩只会抹掉信号本身。
   附带确认：`group_rank` 在此类慢变量上不可用（两域一致），与论坛「事件型优先 rank」正好相反——**这不是事件型信号**。
2. **Q2 窗口：2 年优于 3 年但都不如原字段。** `director_attrition_ratio_2` 1.04 > `_3yr` 0.91，均低于 `attrition3yr` 的 1.12。
   ⇒ 已含 3 年率的信息，无需再拆窗。
3. **Q3 任期维度上限 0.77。** 正号 tenure 在两域都是 0.61；rank 版 0.77 但 SUB 0.21 破线（`LOW_SUB_UNIVERSE_SHARPE`）。
   ⇒ 任期不是可交付维度，与 `board_gov_stats` 的「reverse CEO tenure S −0.37」一致。
4. **Q4 未测机制全灭。** timeretirement −0.32、noquals 0.37、stdevtimeincompany 0.50（rns 仅 0.35 = 风格）。
   ⇒ M8/M9 离散度/退休条款均无独立溢价。
5. **Q5 中性化域不是瓶颈。** INDUSTRY 换来更高的 F 与 returns（attrition 0.63 vs 0.60；`director_attrition_ratio_2`
   0.68 vs 0.58，returns 5.01% vs 3.87%），但 S 持平（1.10 vs 1.12、1.07 vs 1.04），SUB 反而更低（0.48/0.50）。
   ⇒ **域只能改 F 分配，改不了 S 高度**；且 SUB|<0.43 的余量变薄。

**强度天花板（25 条实测，14 个字段，9 个机制）**：max S **1.12**、max F **0.68**。从 1.12 到交付线 1.58 需 +41%，
而结构（zscore/rank/backfill/`std`2·3/`vec_avg`·`vec_max`）、窗口（2y/3y）、域（subindustry/industry）**全部已试且无杠杆**。

## §5 数据集裁定：可交付性判死（prod 轴，2026-10-21）

### 5.1 决定性读数

| 证据 | 读数 | 含义 |
|---|---|---|
| 本集最强候选 `58jzPLY5`（G3，S1.12/F0.60/2Y2.26）跑 `check_correlation(refresh=True)` | **prod 0.7817**，`passes_check=false`（线 0.7）；直方图 `[0.7,0.8)` n=483，max 0.7817 / min −0.7911 | **在 S 还没到线时就已破 prod 红线** |
| 跨数据集同轴 `board_gov_stats`（3 个月管理层离任率，反向） | S **1.56** / F 1.02 / 2Y **2.55** / rns 1.12 ⇒ prod **0.8508**（`[0.8,0.9]` n=1） | 同经济轴、比本集强得多的形态，同样死在 prod |
| 同轴平行战役 `3qjezndX`（S1.54） | prod **0.9137**（`[0.9,1]` n=5，`[0.8,0.9)` n=1482） | 该轴在平台上的拥挤度天花板已就位 |
| 本集 rns 保留率 | M3 0.90 / M5 0.60 / M2 0.07 | 信号**确实存在**且是特质的（M3），不是纯风格 |

### 5.2 裁定：`dead_end`（可交付性，不是「无信号」）

**判死理由（三条，按优先级）**：

1. **prod 轴先死**：最强形态 S1.12 时 prod 已 0.7817 > 0.70。prod 与 S 无关，且 PC 只向上漂
   （`rules/gate-and-submit-discipline.md` 三·3）——**抬 S 不会降 prod**，所以 Wave 3 的任何「把 S 做上去」的努力都不可能变成可提交。
2. **同一经济轴已被两区实证定价**：`USA-BOARD-GOV-STABILITY-PROD-WALL`（S1.56 → 0.8508）与 `3qjezndX`（S1.54 → 0.9137）
   覆盖了「董事会离任率 / 治理稳定性」这条轴。本集 M3 就是这条轴的另一种度量（3 年董事流失率），**不是新机制**。
3. **天花板与交付线差 41%**：25 条 / 9 机制 / 14 字段穷举后 max S 1.12。即使 prod 不是问题，本集也拿不出 S≥1.58 的形态。

**与 §3.3 判死线的关系**：§3.3 那条（「6 机制里 ≥5 个 |S|<0.5」）是**无信号判死**，本文**未命中**——
本集确有信号。但判死有两条独立通道，**prod 通道优先**：信号存在 ≠ 可交付。
按「先归因再推进」的要求，这里不再开 Wave 3，理由不是「懒得试」，而是**可证明的收益上限为零**。

### 5.3 可复用结论（已入 registry `USA-FND1-GOVERNANCE-STYLE-AXIS`）

- **低 S 不等于可以晚点再测 prod**：一个机制在 S≈1.1 时就必须跑一次 prod。若已 >0.7，**抬 S 是白工**。
  本次若先做 Wave 2 再测 prod，会白烧 15 条仿真。
- **`group_rank` 在慢变量上会把信号打死**（0.06 / −0.04），与「事件型优先 rank」是两条互斥规则；
  判据是**变量是否年度快照**，不是「是否横截面」。
- **中性化域改的是 F 与 SUB，不是 S 的高度**：同一结构换域后 S 最多变动 ±0.03。
- **同一数据集内多个机制可能共享一条风格轴**（本集 2020 三机制同年翻号），逐年翻号是比相关性更快的分散化体检。

---

## 附录 · 全 205 字段底表（按 cov 降序；uC=userCount，aC=alphaCount，lc=longCount）

| # | 字段 id | 类型 | cov | longCount | uC | aC | 描述 |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `compensation_currency_code_2` | VECTOR | 0.8010 | 2403 | 3 | 3 | ISO code of the currency in which all reported values are displayed |
| 2 | `fnd1_board_characteristics_noquals` | VECTOR | 0.7999 | 2399 | 1 | 1 | Total number of educational qualifications at undergraduate level or above as of the annual report date |
| 3 | `fnd1_board_characteristics_timebrd` | VECTOR | 0.7999 | 2399 | 7 | 15 | Average time spent on the board by executive directors as of the selected annual report date |
| 4 | `fnd1_board_characteristics_timeinco` | VECTOR | 0.7999 | 2399 | 1 | 2 | Average time spent at the company by executive directors as of the selected annual report date |
| 5 | `fnd1_board_characteristics_timerole` | VECTOR | 0.7999 | 2399 | 6 | 8 | The average length of time executive directors have served in their current role |
| 6 | `fnd1_board_characteristics_totcurrnolstdbrd` | VECTOR | 0.7999 | 2399 | 1 | 1 | The average number of quoted (public) boards currently served on by executive directors in the company |
| 7 | `fnd1_board_characteristics_totnolstdbrd` | VECTOR | 0.7999 | 2399 | 2 | 2 | The average cumulative number of quoted (public) boards served on over time by executive directors |
| 8 | `fnd1_director_characteristics_avgtimeothco` | VECTOR | 0.7999 | 2399 | 3 | 3 | Average time the director sits on boards of quoted (public) companies |
| 9 | `fnd1_director_characteristics_noquals` | VECTOR | 0.7999 | 2399 | 2 | 2 | Total number of educational qualifications (undergraduate and above) for the director as of the selected annua |
| 10 | `fnd1_director_characteristics_timebrd` | VECTOR | 0.7999 | 2399 | 5 | 6 | Time spent by the director on the board as of the selected annual report date |
| 11 | `fnd1_director_characteristics_timeinco` | VECTOR | 0.7999 | 2399 | 0 | 0 | Time spent by the director in the company as of the selected annual report date |
| 12 | `fnd1_director_characteristics_timerole` | VECTOR | 0.7999 | 2399 | 1 | 1 | Time spent by the director in their current role as of the selected annual report date |
| 13 | `fnd1_director_characteristics_totcurrnolstdbrd` | VECTOR | 0.7999 | 2399 | 0 | 0 | Number of quoted (public) boards the director serves on as of the selected annual report date |
| 14 | `fnd1_director_characteristics_totnolstdbrd` | VECTOR | 0.7999 | 2399 | 3 | 3 | Total number of quoted (publicly-listed) boards the director has served on historically up to the selected ann |
| 15 | `fnd1_numberdirectors` | VECTOR | 0.7999 | 2399 | 0 | 0 | Number of Executive Directors on the board |
| 16 | `fnd1_stdevnoquals` | VECTOR | 0.7999 | 2399 | 1 | 1 | The standard deviation of the number of educational qualifications (undergraduate and above) for executive dir |
| 17 | `fnd1_stdevtimebrd` | VECTOR | 0.7999 | 2399 | 0 | 0 | Standard deviation of “time on board” for executive directors (i.e., how long they have sat on boards) |
| 18 | `fnd1_stdevtimeincompany` | VECTOR | 0.7999 | 2399 | 1 | 1 | Standard deviation of time in company among executive directors |
| 19 | `fnd1_stdevtotcurrnolstdbrd` | VECTOR | 0.7999 | 2399 | 1 | 1 | Standard deviation of the number of quoted boards currently served on by executive directors |
| 20 | `fnd1_stdevtotnolstdbrd` | VECTOR | 0.7999 | 2399 | 0 | 0 | Standard deviation of total number of quoted boards served on over time among executive directors |
| 21 | `fnd1_director_characteristics_timeretirement` | VECTOR | 0.7998 | 2399 | 3 | 3 | Number of years or time until the director's retirement at the annual report date |
| 22 | `compensation_currency_code` | VECTOR | 0.7997 | 2399 | 2 | 2 | ISO currency code representing the currency in which all values in the row are displayed |
| 23 | `fnd1_board_characteristics_avgtimeothco` | VECTOR | 0.7997 | 2399 | 2 | 2 | Average time executive directors serve on other quoted boards (excluding the one analyzed) |
| 24 | `fnd1_board_characteristics_timeretirement` | VECTOR | 0.7997 | 2399 | 2 | 2 | Average time to retirement for executive directors as of the selected annual report date |
| 25 | `fnd1_director_characteristics_totnounlstdbrd` | VECTOR | 0.7997 | 2399 | 1 | 1 | Total number of private (unlisted) boards served by the director up to the selected annual report date |
| 26 | `fnd1_stdevage` | VECTOR | 0.7997 | 2399 | 4 | 4 | Standard deviation of ages of Executive Directors |
| 27 | `fnd1_genderratio` | VECTOR | 0.7995 | 2398 | 1 | 1 | Proportion of male directors among executive directors |
| 28 | `fnd1_succession` | VECTOR | 0.7991 | 2397 | 4 | 5 | Degree to which Executive Directors’ ages are clustered near retirement age, indicating succession risk |
| 29 | `fnd1_board_characteristics_filtered_avgtimeothco` | VECTOR | 0.7984 | 2395 | 5 | 10 | Average time executive directors sit on the boards of quoted companies (excluding current organization) |
| 30 | `fnd1_board_characteristics_filtered_noquals` | VECTOR | 0.7984 | 2395 | 1 | 1 | Total number of educational qualifications undergraduate and above held by the individual |
| 31 | `fnd1_board_characteristics_filtered_timebrd` | VECTOR | 0.7984 | 2395 | 6 | 8 | Length of time the individual has served on the board up to the annual report date |
| 32 | `fnd1_board_characteristics_filtered_timeinco` | VECTOR | 0.7984 | 2395 | 3 | 3 | Tenure of the individual at the company as of the annual report date |
| 33 | `fnd1_board_characteristics_filtered_timerole` | VECTOR | 0.7984 | 2395 | 2 | 2 | Time in current role for the individual at the chosen AnnualReportDate |
| 34 | `fnd1_board_characteristics_filtered_totcurrnolstdbrd` | VECTOR | 0.7984 | 2395 | 1 | 1 | Number of quoted (publicly listed) boards an executive director serves on as of the annual report date |
| 35 | `fnd1_board_characteristics_filtered_totnolstdbrd` | VECTOR | 0.7984 | 2395 | 0 | 0 | Total number of quoted (public) boards an individual has served up to the AnnualReportDate |
| 36 | `fnd1_director_characteristics_filtered_avgtimeothco` | VECTOR | 0.7984 | 2395 | 1 | 1 | Average time the director sits on the boards of other quoted companies |
| 37 | `fnd1_director_characteristics_filtered_noquals` | VECTOR | 0.7984 | 2395 | 3 | 3 | Total number of educational qualifications (undergraduate and above) held by the individual |
| 38 | `fnd1_director_characteristics_filtered_timebrd` | VECTOR | 0.7984 | 2395 | 6 | 6 | Length of time the individual has served on the board at the selected annual report date |
| 39 | `fnd1_director_characteristics_filtered_timeinco` | VECTOR | 0.7984 | 2395 | 2 | 2 | Total time the individual has been with the company at the selected annual report date |
| 40 | `fnd1_director_characteristics_filtered_timerole` | VECTOR | 0.7984 | 2395 | 2 | 4 | Length of time the individual has served in the current role at the selected annual report date |
| 41 | `fnd1_director_characteristics_filtered_totcurrnolstdbrd` | VECTOR | 0.7984 | 2395 | 1 | 1 | Number of quoted boards the individual currently serves on at the selected date |
| 42 | `fnd1_director_characteristics_filtered_totnolstdbrd` | VECTOR | 0.7984 | 2395 | 1 | 1 | Total number of quoted (public) boards the individual has served on up to the selected date |
| 43 | `fnd1_filtered_genderratio` | VECTOR | 0.7984 | 2395 | 8 | 14 | Proportion of male executive directors on the board |
| 44 | `fnd1_filtered_numberdirectors` | VECTOR | 0.7984 | 2395 | 3 | 12 | Total number of executive directors as of the annual report date |
| 45 | `fnd1_filtered_stdevnoquals` | VECTOR | 0.7984 | 2395 | 1 | 3 | Standard deviation across the executive directors on the board for the number of educational or professional q |
| 46 | `fnd1_filtered_stdevtimebrd` | VECTOR | 0.7984 | 2395 | 0 | 0 | Standard deviation of time served on board among executive directors |
| 47 | `fnd1_filtered_stdevtimeincompany` | VECTOR | 0.7984 | 2395 | 0 | 0 | Standard deviation of time in company among executive directors |
| 48 | `fnd1_filtered_stdevtotcurrnolstdbrd` | VECTOR | 0.7984 | 2395 | 0 | 0 | Standard deviation of the number of quoted boards currently served on by executive directors in the board |
| 49 | `fnd1_filtered_stdevtotnolstdbrd` | VECTOR | 0.7984 | 2395 | 2 | 2 | Standard deviation of total quoted boards served among executive directors |
| 50 | `fnd1_filtered_succession` | VECTOR | 0.7984 | 2395 | 6 | 8 | Measure of how many directors are clustered near retirement age (succession risk) |
| 51 | `fnd1_board_characteristics_filtered_timeretirement` | VECTOR | 0.7981 | 2394 | 6 | 15 | Time to retirement for the individual at the chosen AnnualReportDate |
| 52 | `fnd1_director_characteristics_filtered_timeretirement` | VECTOR | 0.7981 | 2394 | 0 | 0 | Time to retirement for the individual at the selected annual report date |
| 53 | `fnd1_filtered_stdevage` | VECTOR | 0.7981 | 2394 | 6 | 10 | Standard deviation across the executive directors on the board for their ages (how spread out the ages are amo |
| 54 | `fnd1_board_characteristics_filtered_totnounlstdbrd` | VECTOR | 0.7980 | 2394 | 8 | 17 | Total number of private (non-quoted) boards an executive director has ever served on to date |
| 55 | `fnd1_director_characteristics_filtered_totnounlstdbrd` | VECTOR | 0.7980 | 2394 | 3 | 3 | Total number of private boards the individual has served on up to the selected date |
| 56 | `fnd1_director_characteristics_totcurrnounlstdbrd` | VECTOR | 0.7957 | 2387 | 13 | 21 | Number of private (unlisted) boards the director serves on as of the selected annual report date |
| 57 | `fnd1_board_characteristics_filtered_totcurrnounlstdbrd` | VECTOR | 0.7893 | 2367 | 1 | 1 | Number of private (non-quoted) boards an executive director serves on as of the annual report date |
| 58 | `fnd1_director_characteristics_filtered_totcurrnounlstdbrd` | VECTOR | 0.7891 | 2367 | 4 | 4 | Number of private boards the individual currently serves on at the selected date |
| 59 | `fnd1_board_characteristics_totnounlstdbrd` | VECTOR | 0.7890 | 2367 | 2 | 2 | Average number of private boards served on over time by Executive Directors |
| 60 | `average_other_board_tenure` | VECTOR | 0.7683 | 2304 | 13 | 22 | The Average Time that a Director sits on the Board of Quoted Companies |
| 61 | `board_service_duration` | VECTOR | 0.7683 | 2304 | 7 | 10 | Years served on the current board as of the selected annual report date |
| 62 | `current_other_board_count` | VECTOR | 0.7683 | 2304 | 2 | 2 | The number of Other Boards that an individual serves on at the AnnualReportDate selected. |
| 63 | `current_private_board_count` | VECTOR | 0.7683 | 2304 | 6 | 8 | Current number of unlisted or private boards the director serves on at the report date |
| 64 | `current_quoted_board_count` | VECTOR | 0.7683 | 2304 | 3 | 5 | The total number of quoted/listed boards the individual currently serves on at the given report date |
| 65 | `qualification_count` | VECTOR | 0.7683 | 2304 | 1 | 3 | Total number of educational qualifications (undergraduate level and above) held by the director |
| 66 | `retirement_time_remaining` | VECTOR | 0.7683 | 2304 | 2 | 3 | Estimated time to retirement for the individual at the selected annual report date (years) |
| 67 | `role_tenure_duration` | VECTOR | 0.7683 | 2304 | 3 | 4 | Years in the current role as of the selected annual report date |
| 68 | `tenure_in_organization` | VECTOR | 0.7683 | 2304 | 2 | 3 | Years the individual has been at the company as of the selected annual report date |
| 69 | `total_other_board_count` | VECTOR | 0.7683 | 2304 | 2 | 2 | The total number of Other Boards that an individual has served to the AnnualReportDate selected. |
| 70 | `total_private_board_count` | VECTOR | 0.7683 | 2304 | 2 | 3 | Total lifetime number of unlisted/private boards the individual has served on |
| 71 | `total_quoted_board_count` | VECTOR | 0.7683 | 2304 | 3 | 4 | Total lifetime number of quoted/listed boards the individual has served on |
| 72 | `board_nationality_diversity_ratio` | VECTOR | 0.7621 | 2286 | 0 | 0 | Proportion of executive directors from different countries on the board |
| 73 | `fnd1_board_characteristics_totcurrnounlstdbrd` | VECTOR | 0.7544 | 2263 | 1 | 1 | The average number of private (unlisted) boards currently served on by executive directors in the company |
| 74 | `board_nationality_diversity_ratio_2` | VECTOR | 0.7405 | 2221 | 1 | 4 | Proportion of directors from different countries among executive directors (board nationality diversity) |
| 75 | `director_attrition_ratio_2` | VECTOR | 0.6931 | 2079 | 5 | 22 | Proportion of executive directors who have left roles relative to average number for the preceding reporting p |
| 76 | `director_attrition_ratio_3yr` | VECTOR | 0.6828 | 2048 | 6 | 14 | Proportion of executive directors who have left roles relative to average number for the preceding 3 years |
| 77 | `fnd1_filtered_attrition3yr` | VECTOR | 0.6715 | 2014 | 18 | 30 | Proportion of executive directors who left over the preceding 3 years compared to average number of directors  |
| 78 | `other_board_total_count` | VECTOR | 0.5992 | 1797 | 3 | 3 | Total number of other boards the director has served on up to the selected annual report date |
| 79 | `total_other_listed_boards_count` | VECTOR | 0.5519 | 1655 | 1 | 1 | Total number of other boards (neither quoted nor private) an executive director has served on to date |
| 80 | `director_total_other_listed_boards_count` | VECTOR | 0.5469 | 1640 | 3 | 3 | Total number of other types of boards the individual has served on up to the selected date |
| 81 | `total_other_listed_boards_count_2` | VECTOR | 0.5162 | 1548 | 0 | 0 | Total number of other (non-quoted, non-private) boards an individual has served on as of the annual report dat |
| 82 | `director_attrition_ratio` | VECTOR | 0.5019 | 1505 | 2 | 2 | Proportion of executive directors who left since previous period to average number of directors in previous pe |
| 83 | `current_other_board_total` | VECTOR | 0.4061 | 1218 | 1 | 1 | Number of other boards the director serves on as of the selected annual report date |
| 84 | `current_other_listed_boards_count_2` | VECTOR | 0.3708 | 1112 | 2 | 2 | Number of other boards the individual currently serves on as of the annual report date |
| 85 | `incentive_currency_code` | VECTOR | 0.3187 | 956 | 0 | 0 | ISO code representing the currency in which all monetary values are reported |
| 86 | `incentive_plan_stock_price` | VECTOR | 0.3187 | 956 | 0 | 0 | Price of the stock for the incentive plan at the annual report date |
| 87 | `option_plan_currency_code` | VECTOR | 0.3173 | 951 | 2 | 2 | ISO code of the currency in which financial values are expressed |
| 88 | `option_plan_stock_price` | VECTOR | 0.3173 | 951 | 0 | 0 | Closing price of the stock at the time of the annual report or the relevant award date |
| 89 | `option_exercise_price` | VECTOR | 0.3172 | 951 | 0 | 0 | Price at which options can be exercised by the director |
| 90 | `fnd1_board_characteristics_boardid` | VECTOR | 0.3170 | 951 | 2 | 2 | A unique identifier allocated to each company |
| 91 | `fnd1_director_characteristics_boardid` | VECTOR | 0.3170 | 951 | 0 | 0 | A unique identifier allocated to each company |
| 92 | `fnd1_director_characteristics_directorid` | VECTOR | 0.3170 | 951 | 1 | 1 | A unique identifier allocated to each director |
| 93 | `ltip_wealth_stock_price` | VECTOR | 0.3166 | 949 | 0 | 0 | Stock price for the awarded security on the annual report date |
| 94 | `monetary_unit_code` | VECTOR | 0.3166 | 949 | 0 | 0 | ISO code of the currency in which all monetary values are reported |
| 95 | `current_other_listed_boards_count` | VECTOR | 0.3103 | 930 | 3 | 3 | Number of other types of boards (neither quoted nor private) an executive director serves on as of the annual  |
| 96 | `exercisable_option_volume` | VECTOR | 0.3093 | 927 | 3 | 3 | Number of exercisable options awarded in the incentive plan |
| 97 | `exercisable_option_estimated_value` | VECTOR | 0.3092 | 927 | 1 | 1 | Estimated value of exercisable options awarded, valued at the closing stock price |
| 98 | `director_current_other_listed_boards_count` | VECTOR | 0.3041 | 912 | 4 | 4 | Number of other types of boards the individual currently serves on at the selected date |
| 99 | `option_award_stock_price` | VECTOR | 0.3032 | 909 | 1 | 1 | Market price of the stock at the annual report date relevant to the option plan |
| 100 | `option_currency_code` | VECTOR | 0.3032 | 909 | 0 | 0 | Numeric ISO code of the currency in which all plan values in the record are displayed |
| 101 | `option_exercise_price_2` | VECTOR | 0.3032 | 909 | 0 | 0 | Specified price at which the option holder can purchase shares under the option plan |
| 102 | `exercisable_option_intrinsic_value` | VECTOR | 0.3031 | 909 | 0 | 0 | Valuation of exercisable options, usually at the period's closing stock price |
| 103 | `share_award_quantity` | VECTOR | 0.3029 | 908 | 1 | 1 | Maximum number of shares awarded during the period for the specified incentive plan |
| 104 | `share_award_value_3` | VECTOR | 0.3029 | 908 | 0 | 0 | Total value of shares awarded for a given incentive plan |
| 105 | `cash_incentive_plan_value_2` | VECTOR | 0.2955 | 886 | 1 | 1 | Value of any cash-based incentive plan held by the director. |
| 106 | `currency_iso_code_8` | VECTOR | 0.2955 | 886 | 1 | 1 | Three-letter ISO code representing the currency for monetary values. |
| 107 | `equity_award_monetary_value` | VECTOR | 0.2955 | 886 | 0 | 0 | Value of shares awarded under a specific incentive plan. |
| 108 | `equity_award_share_count` | VECTOR | 0.2955 | 886 | 0 | 0 | Number of shares awarded in a given incentive plan. |
| 109 | `exercisable_option_estimated_value_2` | VECTOR | 0.2955 | 886 | 0 | 0 | Estimated value of options that can currently be exercised. |
| 110 | `exercisable_option_intrinsic_value_3` | VECTOR | 0.2955 | 886 | 0 | 0 | Intrinsic value of options that can currently be exercised. |
| 111 | `exercisable_option_volume_2` | VECTOR | 0.2955 | 886 | 0 | 0 | Number of options awarded that can currently be exercised. |
| 112 | `expired_option_count` | VECTOR | 0.2955 | 886 | 0 | 0 | Number of options in the incentive plan that have expired. |
| 113 | `matched_equity_award_value` | VECTOR | 0.2955 | 886 | 0 | 0 | Value of shares awarded including any matched portion in an incentive plan. |
| 114 | `matched_equity_award_volume` | VECTOR | 0.2955 | 886 | 1 | 1 | Number of shares awarded including any matched portion in an incentive plan. |
| 115 | `option_exercise_price_5` | VECTOR | 0.2955 | 886 | 0 | 0 | Price at which awarded options can be exercised. |
| 116 | `reference_stock_price` | VECTOR | 0.2955 | 886 | 0 | 0 | Stock price at the relevant report or award date. |
| 117 | `unexercisable_option_estimated_value_2` | VECTOR | 0.2955 | 886 | 0 | 0 | Estimated value of options that cannot currently be exercised. |
| 118 | `unexercisable_option_intrinsic_value_3` | VECTOR | 0.2955 | 886 | 0 | 0 | Intrinsic value of options that are not yet exercisable. |
| 119 | `unexercisable_option_volume_2` | VECTOR | 0.2955 | 886 | 2 | 2 | Number of options awarded that are not yet exercisable. |
| 120 | `incentive_share_award_value` | VECTOR | 0.2885 | 865 | 0 | 0 | Value of shares awarded for a given incentive plan |
| 121 | `incentive_share_award_volume` | VECTOR | 0.2885 | 865 | 0 | 0 | Maximum number of shares awarded in the period for a conditional incentive plan |
| 122 | `fnd1_attrition3yr` | VECTOR | 0.2772 | 831 | 6 | 9 | Number of directors that have left a role as a proportion of the average number of directors for the preceding |
| 123 | `option_unexercisable_estimate_value` | VECTOR | 0.2690 | 807 | 0 | 0 | Valuation of unexercisable options awarded, using closing stock price at annual report date |
| 124 | `option_unexercisable_volume` | VECTOR | 0.2690 | 807 | 2 | 2 | Number of unexercisable options currently awarded for that plan |
| 125 | `fnd1_attrition` | VECTOR | 0.2459 | 737 | 9 | 23 | Number of directors that have left a role as a proportion of the average number of directors for the preceding |
| 126 | `fnd1_board_characteristics_totnoothlstdbrd` | VECTOR | 0.2439 | 731 | 1 | 1 | The average number of Other Boards that have been sat on over time for the Executive Directors |
| 127 | `fnd1_director_characteristics_totnoothlstdbrd` | VECTOR | 0.2439 | 731 | 1 | 1 | The total number of Other Boards that an individual has served to the AnnualReportDate selected. |
| 128 | `option_unexercisable_intrinsic_value` | VECTOR | 0.2336 | 700 | 0 | 0 | Valuation of unexercisable options awarded, using closing stock price at annual report date |
| 129 | `aggregate_director_compensation_2` | VECTOR | 0.2078 | 623 | 1 | 1 | Sum of the director's salary and bonus for the report period |
| 130 | `total_director_cash_comp` | VECTOR | 0.2078 | 623 | 2 | 2 | Total direct compensation: sum of salary, bonus, other cash, and pension employer contributions for the direct |
| 131 | `annual_base_salary` | VECTOR | 0.2046 | 613 | 1 | 1 | Base annual cash salary for the director in the report period |
| 132 | `aggregate_director_compensation` | VECTOR | 0.2014 | 604 | 3 | 3 | Sum of salary and bonus received by the director for the report period |
| 133 | `total_director_cash_compensation` | VECTOR | 0.2014 | 604 | 0 | 0 | Total direct compensation received by the director, calculated as Salary plus Bonus plus Other plus PenEmpCont |
| 134 | `total_equity_linked_wealth_2` | VECTOR | 0.1992 | 597 | 0 | 0 | Total valuation of director’s equity-linked wealth at period end, calculated at closing stock price of the ann |
| 135 | `total_remuneration_period` | VECTOR | 0.1990 | 597 | 0 | 0 | Total remuneration or awards received by the director during the period |
| 136 | `total_shareholding_value_2` | VECTOR | 0.1974 | 592 | 0 | 0 | Value of shares held by the director at the end of the reporting period, calculated using the annual report da |
| 137 | `total_equity_linked_wealth` | VECTOR | 0.1952 | 585 | 0 | 0 | Total value of equity-linked wealth (e.g., shares, options) held by the director at the end of the period, val |
| 138 | `wealth_sensitivity_to_stock` | VECTOR | 0.1952 | 585 | 0 | 0 | Change in the director's wealth in the company for a 1% change in share price at the annual report date; calcu |
| 139 | `wealth_sensitivity_to_stock_2` | VECTOR | 0.1951 | 585 | 0 | 0 | Change in the director's company-specific wealth for a 1% change in stock price at the annual report date, as  |
| 140 | `total_shareholding_value` | VECTOR | 0.1930 | 579 | 0 | 0 | Value of shares held by the individual director at the end of the reporting period, measured at the closing st |
| 141 | `other_cash_payments_2` | VECTOR | 0.1860 | 558 | 0 | 0 | Annual value of ad hoc cash payments such as relocation allowances |
| 142 | `total_equity_at_risk_2` | VECTOR | 0.1833 | 549 | 1 | 1 | Total stock |
| 143 | `equity_linked_compensation_ratio_2` | VECTOR | 0.1784 | 535 | 0 | 0 | Equity-linked compensation (such as shares/options/LTIPs) as a proportion of total compensation, based on annu |
| 144 | `compensation_change_percent_2` | VECTOR | 0.1775 | 532 | 1 | 1 | Percentage change in total compensation from previous report period for the director |
| 145 | `ltip_plan_value_held` | VECTOR | 0.1733 | 519 | 0 | 0 | Value of long-term incentive plans (LTIPs) held by the director at the end of the period, at closing stock pri |
| 146 | `annual_bonus_payment` | VECTOR | 0.1712 | 513 | 1 | 2 | Bonus payment received by the director during the report period |
| 147 | `fnd1_board_characteristics_totcurrnoothlstdbrd` | VECTOR | 0.1712 | 513 | 0 | 0 | The average number of Other Boards that are sat on today for the Executive Directors |
| 148 | `fnd1_director_characteristics_totcurrnoothlstdbrd` | VECTOR | 0.1712 | 513 | 2 | 3 | The number of other boards that an individual serves on at the Annual Report Date selected. |
| 149 | `estimated_value_options_held` | VECTOR | 0.1706 | 511 | 0 | 0 | Estimated value of options held at end of period by the director, valued at annual report closing price |
| 150 | `intrinsic_value_options_held_2` | VECTOR | 0.1656 | 496 | 0 | 0 | Value of stock options held by the director at period end, using closing stock price from the annual report da |
| 151 | `bonus_proportion_total_comp` | VECTOR | 0.1655 | 496 | 0 | 0 | Bonus amount as a proportion of total direct compensation excluding defined contribution pension |
| 152 | `cash_incentive_plan_value` | VECTOR | 0.1640 | 492 | 1 | 1 | Value of any cash-based incentive plan awarded |
| 153 | `ltip_plan_value_held_2` | VECTOR | 0.1627 | 488 | 2 | 2 | Value of LTIPs held at period end, valued at closing stock price on annual report date |
| 154 | `ltip_award_value_2` | VECTOR | 0.1617 | 485 | 0 | 0 | Value of Long-Term Incentive Plans (LTIPs) awarded during the period, valued at closing stock price on the ann |
| 155 | `option_exercisable_volume` | VECTOR | 0.1616 | 484 | 0 | 0 | Number of options in the plan that are exercisable as of the report date |
| 156 | `option_exercisable_estimate_value` | VECTOR | 0.1615 | 484 | 0 | 0 | Valuation of exercisable options awarded, based on closing stock price at annual report date |
| 157 | `estimated_value_options_awarded_2` | VECTOR | 0.1560 | 468 | 0 | 0 | Estimated value of options awarded to the director during the period, based on closing stock price from the an |
| 158 | `ltip_to_total_remuneration_ratio_2` | VECTOR | 0.1552 | 465 | 1 | 1 | Ratio of LTIP value to total awards for the period (LTIPValue/TotRemPeriod) |
| 159 | `employer_pension_contribution_2` | VECTOR | 0.1481 | 444 | 2 | 2 | Employer’s defined pension contribution for each director during the reporting period |
| 160 | `incentive_cash_plan_value` | VECTOR | 0.1437 | 431 | 1 | 1 | The value of any cash-based incentive plan awarded |
| 161 | `intrinsic_value_options_awarded_2` | VECTOR | 0.1405 | 421 | 0 | 0 | Intrinsic value of options awarded during the period, valued at annual report date closing stock price |
| 162 | `option_exercisable_intrinsic_value` | VECTOR | 0.1383 | 414 | 0 | 0 | Valuation of exercisable options awarded, using closing stock price at annual report date |
| 163 | `estimated_option_value_held` | VECTOR | 0.1228 | 368 | 0 | 0 | Estimated value of options held by the director at the end of the reporting period, calculated at the closing  |
| 164 | `fnd1_nationalitymix` | VECTOR | 0.1220 | 366 | 0 | 0 | Proportion of directors from different countries whether for the executive directors. |
| 165 | `unexercisable_option_estimated_value` | VECTOR | 0.1137 | 341 | 1 | 1 | Estimated value of unexercisable options awarded, valued at the closing stock price |
| 166 | `unexercisable_option_volume` | VECTOR | 0.1137 | 341 | 0 | 0 | Number of unexercisable options awarded in the incentive plan |
| 167 | `intrinsic_value_options_held` | VECTOR | 0.1100 | 330 | 0 | 0 | Valuation of stock options held by the director at period end, using the closing share price on the annual rep |
| 168 | `unexercisable_option_intrinsic_value` | VECTOR | 0.0920 | 276 | 2 | 2 | Valuation of unexercisable options, usually at the closing stock price for the period |
| 169 | `incentive_option_exercise_price` | VECTOR | 0.0557 | 167 | 1 | 1 | Price at which the options under the incentive plan can be exercised |
| 170 | `option_strike_price` | VECTOR | 0.0500 | 150 | 0 | 0 | Price at which awarded options can be exercised |
| 171 | `share_award_value_2` | VECTOR | 0.0418 | 125 | 0 | 0 | Value of shares awarded during the period, using closing stock price on the annual report date |
| 172 | `director_base_salary` | VECTOR | 0.0301 | 90 | 0 | 0 | Base annual cash salary paid to the director during the reported period |
| 173 | `total_awards_period` | VECTOR | 0.0301 | 90 | 0 | 0 | Total compensation or awards received by the director for the reporting period |
| 174 | `estimated_value_exercisable_options` | VECTOR | 0.0273 | 81 | 1 | 1 | Estimated value of exercisable options awarded in the period, valued at closing stock price on annual report d |
| 175 | `exercisable_option_quantity` | VECTOR | 0.0273 | 81 | 0 | 0 | Maximum number of exercisable options awarded for that incentive plan in the period |
| 176 | `estimated_value_unexercisable_options` | VECTOR | 0.0252 | 75 | 0 | 0 | Estimated value of unexercisable options awarded in the period, valued at closing stock price on annual report |
| 177 | `unexercisable_option_quantity` | VECTOR | 0.0252 | 75 | 0 | 0 | Maximum number of unexercisable options awarded for the incentive plan in the period |
| 178 | `incentive_unexercisable_option_volume` | VECTOR | 0.0248 | 74 | 0 | 0 | Number of unexercisable options awarded for the plan |
| 179 | `unexercisable_option_estimate_value` | VECTOR | 0.0248 | 74 | 0 | 0 | Valuation of unexercisable options awarded in the period, valued at closing stock price for the annual report  |
| 180 | `intrinsic_value_exercisable_options` | VECTOR | 0.0224 | 67 | 1 | 1 | Exercise price at which the exercisable options can be exercised |
| 181 | `intrinsic_value_unexercisable_options` | VECTOR | 0.0206 | 61 | 1 | 1 | Valuation of unexercisable options awarded in the period, using the closing stock price at the annual report d |
| 182 | `unexercisable_option_intrinsic_value_2` | VECTOR | 0.0197 | 59 | 0 | 0 | Valuation of unexercisable options awarded in the period, based on closing stock price at the annual report da |
| 183 | `exercisable_option_estimate_value` | VECTOR | 0.0133 | 39 | 1 | 1 | Valuation of exercisable options awarded in the period, based on the closing stock price at the annual report  |
| 184 | `incentive_exercisable_option_volume` | VECTOR | 0.0133 | 39 | 0 | 0 | The number of options awarded that are currently exercisable under the specified conditional incentive plan |
| 185 | `other_cash_payments` | VECTOR | 0.0121 | 36 | 1 | 1 | Annual ad hoc cash payments made to the director, such as relocation allowances or similar items |
| 186 | `exercisable_option_intrinsic_value_2` | VECTOR | 0.0099 | 29 | 3 | 3 | Valuation of exercisable options awarded in the period, based on closing stock price at the annual report date |
| 187 | `compensation_change_percent` | VECTOR | 0.0095 | 28 | 0 | 0 | Percentage change in the director's total compensation compared to the previous reporting period |
| 188 | `equity_linked_compensation_ratio` | VECTOR | 0.0089 | 26 | 1 | 1 | Ratio of equity-linked compensation to total compensation for the director, calculated at closing stock price |
| 189 | `total_equity_at_risk` | VECTOR | 0.0089 | 26 | 0 | 0 | Total value or volume of equity at risk (held or awarded shares and options) |
| 190 | `ltip_award_value` | VECTOR | 0.0087 | 26 | 0 | 0 | Value of long-term incentive plan (LTIP) awards granted during the period, measured at the closing stock price |
| 191 | `ltip_to_total_remuneration_ratio` | VECTOR | 0.0087 | 26 | 0 | 0 | Ratio of LTIP value to total compensation for the director during the report period |
| 192 | `employer_pension_contribution` | VECTOR | 0.0076 | 22 | 0 | 0 | Employer's defined contribution to the director's pension for each report period |
| 193 | `incentive_equity_matched_value` | VECTOR | 0.0053 | 15 | 1 | 1 | The value of shares awarded plus any matched percentage for a given incentive plan |
| 194 | `incentive_equity_matched_volume` | VECTOR | 0.0053 | 15 | 1 | 1 | Maximum number of shares awarded plus matched percentage in the period for a conditional incentive plan |
| 195 | `matched_share_award_quantity` | VECTOR | 0.0053 | 15 | 3 | 3 | Maximum number of shares awarded plus the matched percentage in the period under a specific incentive plan |
| 196 | `matched_share_award_value` | VECTOR | 0.0053 | 15 | 0 | 0 | Value of shares awarded plus matched percentage for the given incentive plan |
| 197 | `estimated_value_options_awarded` | VECTOR | 0.0048 | 14 | 0 | 0 | Estimated valuation of options awarded to the director during the period, calculated at the closing stock pric |
| 198 | `expired_option_volume` | VECTOR | 0.0040 | 12 | 1 | 1 | Number of expired options in the director's incentive plan |
| 199 | `option_expired_volume` | VECTOR | 0.0040 | 12 | 0 | 0 | Number of expired options in the relevant incentive plan |
| 200 | `intrinsic_value_options_awarded` | VECTOR | 0.0029 | 8 | 0 | 0 | Intrinsic value of options awarded to the director during the period, valued at closing stock price on the rep |
| 201 | `bonus_to_compensation_ratio` | VECTOR | 0.0026 | 7 | 0 | 0 | Bonus as a proportion of total direct compensation less defined contribution pension for the director |
| 202 | `director_bonus_payment` | VECTOR | 0.0026 | 7 | 0 | 0 | Bonus payments received by the director during the report period |
| 203 | `expired_option_quantity` | VECTOR | 0.0018 | 5 | 2 | 2 | Number of expired options in the incentive plan |
| 204 | `share_award_value` | VECTOR | 0.0008 | 2 | 1 | 1 | Value of shares awarded to the director during the reporting period, measured at closing stock price |
| 205 | `incentive_expired_option_volume` | VECTOR | 0.0003 | 0 | 0 | 0 | Number of options that have expired in the incentive plan |
