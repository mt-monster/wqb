# analyst_consensus 数据集分析文档（KOR / TOP600 / D1）

> ★ **打样文档**（用户指定首个打样数据集，2026-11-16）。其余 15 份文档以本文档为格式与深度基准。
> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst_consensus_profile.json`（300 字段）
> 区域 KOR（不换）｜universe TOP600（本区唯一合法）｜delay 1

---

## 一、分析思路

1. **先用 description 做零假设重分类**，不看字段名 —— 字段名会骗人（description 是唯一语义依据）。
2. 与「按字段名分类」对照，**记录差异**（差异往往就是被漏掉的资产）。
3. 每类映射到经济学机制：说清「收益从哪来」，说不出的不进骨架。
4. 机制 → 骨架 → 候选；**骨架形态由体检体征决定，壳层由经济机制决定**。
5. 双通道取证（论坛 + 论文）后本区实测，结论回写本文档。

## 二、数据集总览

| 指标 | 值 |
|---|---|
| 字段总数 | 300 |
| 类型分布 | VECTOR 298 / MATRIX 2 |
| coverage ≥ 0.5 | 264 / 300 |
| 白空间（alphaCount ≤ 2） | 299 / 300 |
| 平均 coverage | 0.6859 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **已实现/实际值** | 事后真值 | 144 | 126 | VECTOR144 | 144 |
| **家数/估计者数量** | 关注广度 | 136 | 118 | VECTOR134 / MATRIX2 | 135 |
| **共识均值** | 预期水平 | 12 | 12 | VECTOR12 | 12 |
| **币种/元信息** | 元数据 | 8 | 8 | VECTOR8 | 8 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `actual_` | 143 |
| `estimate_` | 132 |
| `avg_` | 12 |
| `currency_` | 9 |
| `count_` | 4 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准。

**★ 逐条记录差异（这是本文档最重要的产出之一）**：

| # | 字段名（会骗人） | description（真相） | 字段名分类会错成 | 正确分类 |
|---|---|---|---|---|
| 1 | `estimate_count_net2` | Number of analyst estimates contributing to the current NET consensus | 名里无 `annual12` 等窗标记，易被当"杂项"丢弃 | **家数类 · current** |
| 2 | `estimate_count_pre2` | Number of analyst estimates contributing to the current PRE consensus | 同上 | **家数类 · current** |
| 3 | `estimate_count_recent_net2` | Number of analyst estimates in the NET **flash snapshot** | 名字看不出 flash | **家数类 · flash** |
| 4 | `estimate_count_recent_pre2` | Number of analyst estimates in the PRE flash snapshot | 同上 | **家数类 · flash** |
| 5 | `estimate_count_current_period_targetprice_annual12_tribes` | Number of analyst **target price** estimates | 名字像普通盈利家数 | **家数类**，但标的物是**目标价**非盈利 ⇒ 语义独立，慎与盈利家数混用 |
| 6 | `count_net_income_estimates` | Current number of analyst estimates in the quarterly NET consensus | 前缀是 `count_` 不是 `estimate_count_`，按名前缀会被切成另一族 | **家数类 · current** |
| 7 | `count_net_income_4wks_prior` | Number of contributing quarterly Net Income estimates as of four weeks ago | 同上 | **家数类 · four_weeks_prior** |
| 8 | `count_net_income_3mth_prior` | Number of analyst estimates in the NET consensus 3 months ago | 同上 | **家数类 · three_months_prior** |

> **教训**：若按字段名前缀分类，家数类会被拆成 `estimate_count_*`(132) 与 `count_*`(4) **两个互不相认的族**（共 136），
> 而**窗口信息（flash/current/4wk/3mth）也完全丢失** —— 因为字段名里窗标记的写法不统一
> （`four_weeks_prior_` vs `_3mth_prior` vs `recent_` vs `flash_period_`）。
> **只有读 description 才能把它们还原成同一个四窗梯度族。这是本轮最重要的发现。**


### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `unspecified` | 58 | — | `estimate_count_current_period_targetprice_annual12_tribes` (cov 0.804, αC 2) |
| `four_weeks_prior` | 26 | — | `estimate_count_four_weeks_prior_net2` (cov 0.803, αC 0) |
| `flash_period` | 25 | — | `estimate_count_recent_net2` (cov 0.803, αC 0) |
| `current_period` | 20 | — | `estimate_count_ebit_annual12_2` (cov 0.803, αC 0) |
| `three_months_prior` | 7 | — | `estimate_count_three_months_prior_ebit_annual12_2` (cov 0.803, αC 0) |

## 三·补、★ 字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**，
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| **4** | 3 | 0.620 | `estimate_count_currentliabilities_annual12` | Number of individual analyst estimates…annual current liabilities |
| 2 | 2 | 0.786 | `actual_bvps_value_annual12` | Reported actual annual Book Value per Share |
| 2 | 2 | 0.638 | `count_recent_net_income_estimates` | Number of estimates in the vendor **flash snapshot** for NET |
| 2 | 2 | 0.804 | `estimate_count_current_period_targetprice_annual12_tribes` | Number of analyst **target price** estimates |
| 2 | 1 | 0.800 | `estimate_count_current_period_eps_annual12_3` | Current number of analyst estimates…consensus |
| 1 | 1 | 0.727 | `estimate_count_fcf_annual12` | Number of analyst estimates…annual FCF |
| 1 | 1 | 0.622 | `estimate_count_currentassets_annual12` | Number of analyst estimates…Current Assets |

**★ 轴判读**：头部字段**既不是盈利轴、也不是 EPS 修正轴**，而是
① **资产负债表科目家数**（currentliabilities αC=4、currentassets）、② **BVPS 实际值**、
③ **flash 快照家数**。

⇒ **该数据集最强的经济轴 = 资产负债表口径的覆盖广度**，不是我一直做的盈利口径。
前三波（Wave11–13）全部打在 net/eps/revenue 上，**方向本身就偏了**。这是本轮最重要的纠错。

## 三·补二、字段画像五问（第 2 步要求）

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 家数类 | 有几个分析师在估该标的 | 计数 | **状态量**（非变化率） | 覆盖决策本身带信息 | cov 0.62–0.80；**VECTOR 需 vec_avg** |
| 已实现类 | 该标的的**事后真值** | 报告值采集 | 事件驱动（报告日阶跃） | 用于算惊喜/误差 | cov 0.47–0.80，季频 |
| 共识均值类 | 分析师估值的**均值** | 算术平均 | 状态量 | 预期水平 | 仅 12 条，全 net_income 标的物 |
| 币种类 | 币种/汇率元信息 | 元数据 | — | 跨币种可比 | 不产出信号 |

**预处理决策（由画像推导）**：

| 画像读数 | 预处理决策 | 依据 |
|---|---|---|
| 全部 VECTOR（132/134） | **必须 `vec_avg` 降维** | 裸用 `rank`/`ts_*` 秒拒，且一条错整批 CANCELLED |
| cov 0.62–0.80（不满） | 可裸用；<0.4 才需 `ts_backfill` | 体检硬门检查 1 |
| 更新频率 = 季频（报告日） | **窗口下限 ≥ 63d** | 铁律 A：窗口低于更新周期 = 噪声 |
| **TO 实测 0.027–0.094** | ⚠ **禁扫窗口谱** | 见 §五判据 |
| 离散评分型（N/A 本集） | — | 无连续尾部字段 |

## 三·补三、★★ 真正的结构：「30 标的物 × 4 时间窗」矩阵

家数类按 description 的标的物细分（缩写按受控词表还原，unknown 降至 12%）：

| 标的物 | 条数 | 均 cov | 标的物 | 条数 | 均 cov |
|---|---:|---:|---|---:|---:|
| pretax | 16 | 0.719 | roe | 5 | 0.791 |
| eps | 10 | 0.637 | net income | 4 | 0.638 |
| ebit | 10 | 0.728 | capex | 4 | 0.753 |
| revenue | 8 | 0.727 | netdebt | 4 | 0.724 |
| grossmargin | 7 | 0.541 | netprofit | 4 | 0.708 |
| dividend | 6 | 0.766 | nav | 3 | 0.777 |
| gps | 6 | 0.621 | depreciation | 2 | 0.654 |
| reportednet | 6 | 0.715 | ebitda | 2 | 0.750 |
| bvps | 5 | 0.785 | 其余 + unknown | 16+12 | — |
| cfps | 5 | 0.761 | | | |

**★ 结构判读**：家数类 **134 条 = 30 个标的物 × 4 个时间窗**，是一个**矩阵**不是一条轴。
标的物分布**极分散**（最大 pretax 仅 16 条，占 12%）。

⇒ **正确的骨架不是「单标的物做深」，而是「跨标的物做广度一致性」** ——
例：当 30 个标的物的覆盖家数**同时**下降 = 系统性关注撤离（强信号）；
若只有 1–2 个标的物变动 = 个股特例（噪声）。
这解释了为什么前三波单轴打法全灭：**我把一个 30×4 的矩阵当成了 1 条轴在打。**


### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：144｜代表：`actual_net_value`, `actual_net_value_fxadj`, `actual_revenue_value_annual12`

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：136｜代表：`estimate_count_current_period_targetprice_annual12_tribes`, `estimate_count_four_weeks_prior_net2`, `estimate_count_net2`

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：12｜代表：`avg_net_income_3mth_prior`, `avg_net_income_3mth_prior_fxadj`, `avg_net_income_4wks_prior`

### 币种/元信息 → 骨架：**—**

- **收益来源**：元数据，无收益来源
- **合规/工程注意**：不进信号；仅可作 group 参数
- **字段数**：8｜代表：`currency_type_eps_annual12`, `currency_code_epsreported_annual12`, `currency_type_parent_profit_annual12`

## 五、本区实测与死因

### 5.1 Wave11 实测（一阶变化路线，2026-11-16）

| 候选 | S | TO | RN_S | 判断 |
|---|---:|---:|---:|---|
| 变化裸差 `log(cur+1)-log(4wk+1)` | **0.47** | 0.060 | 0.59 | 本类最佳，仍 << 1.58 |
| +`group_zscore(...,sector)` z(20) | 0.30 | 0.045 | 0.44 | 平滑降强度 |
| +`group_zscore` 3m 窗 z(60) | 0.06 | 0.027 | 0.24 | 长窗更差 |
| 水平（论坛 USA 原式） | **-0.11** | 0.048 | -0.45 | **符号翻转** |
| `ts_rank(Δ,250)` | 0.32 | 0.094 | 0.34 | 救不回 |
| `group_zscore(ts_zscore(cur,252),subindustry)` | 0.14 | 0.068 | 0.49 | 救不回 |

### 5.3 Wave14 实测（flash−current 窗口差分，2026-11-16）

| 候选 | S | TO | RN_S | 判断 |
|---|---:|---:|---:|---|
| `flash−current` revenue 差分 | -0.06 | **0.0239** | 0.35 | 更静态 |
| `flash−current` eps 差分 | 0.03 | **0.0242** | 0.45 | 更静态 |

**判读**：TO 进一步降到 **0.024**（比 Wave11 的 0.047–0.094 还低）。
⇒ **flash 与 current 几乎同步，两者差分无信息** —— 反向证实 §三·补三 的结构判读：
家数类整体是**同步更新的状态量矩阵**，任何窗口间差分都会把信号差没。

### 5.4 死因指纹（三条，Wave11–14 共 10 条一致）

1. **TO 锁死 0.0239–0.094** —— 信号近乎静态，横截面重排产生不了收益
2. 有效持仓仅 **274–341 / 600**（cov ≈0.78 上限的必然后果）
3. **risk_neutralized_S ≥ raw_S** —— 中性化/因子暴露不背锅，是**信号自身无信息**

### 5.5 预筛判据（下次开波前先跑）

> 候选族在 KOR 的 TO 上限 < 0.10 ⇒ **不要扫窗口谱** —— 窗口只改幅度，改不了「静态」。
> 更严的版本：**TO < 0.03 的候选连差分都不要做**（见 5.3，差分只会更低）。

### 5.6 ★ Wave15 实测（跨标的物广度一致性，2026-11-16）—— 数据集判死

> 详见 `tracking/KOR/candidates/wave15_results.md`；multisim `2zb19Y4Pd4oNbQC92Jz5Ppp`。

| 组 | 机制 | 5 条 S | 最高 |
|---|---|---|---|
| **A** | 跨科目广度背离 `subtract(rank(资产负债口径), rank(盈利口径))` | -0.54 / -0.17 / -0.06 / -0.04 / -0.02 | **-0.02** |
| **B** | 头部轴 `currentliabilities`(αC=4) 五种新形态 | 0.54 / 0.51 / 0.36 / 0.21 / -0.13 | **0.54** |

**四条结论**：

1. **组 A 全灭（S 全负）** ⇒ 「跨标的物广度一致性/背离」机制在 KOR **不存在**。
2. **矩阵结构假设证伪**：§三·补三 的字段结构还原**正确**（数据确实是 30×4 矩阵），
   但**该结构没有可交易信号**。⇒ **★ 方法论教训：「结构还原正确」≠「结构有信号」**。
3. **组 B（0.21–0.54）仅比 Wave11–13（0.47）好 +0.07** ⇒ **不是「选错科目」，而是「家数类整体无信号」**。
4. **★ 新增死因指纹：`CONCENTRATED_WEIGHT`**（组 A 多条 + 组 B **全部**触发，value 0.30–0.50 / limit 0.1）
   —— 根因是**覆盖度仅 0.62–0.72 ⇒ 少数股票有值 ⇒ 权重强制集中**，
   属**低覆盖字段的结构性问题**，与信号强度无关，**任何算子形态都救不了**。

**⇒ 判定：`analyst_consensus` 数据集级判死，转其余 15 个数据集。**

**5.7 判据升级（Wave15 贡献）**：

> **TO < 0.10 且 `CONCENTRATED_WEIGHT` 命中 ⇒ 该族可直接判死，不必再试形态谱。**
> （Wave15 实测：换 5 种算子几何，TO 无一被提振、CW 无一被解除。）




## 六、双通道取证

- **通道 A（论坛）**：`search_forum_posts` 长中文 query 会炸，砍短关键词；`read_forum_post` 必传 `include_comments=false`（true 会 30s 超时）。

### 通道 A 实证（本数据集相关）

- 帖 `34506025416087`（LZ70706，2025-08-28）**分析师覆盖度因子**，USA/TOP3000 骨架：
  `group_zscore(ts_mean(log(anl4_epsr_number+1),120),densify(bucket(rank(cap),range='0.1,1,0.1')))`
  → USA 下 S=1.48，窗口加大到 120、十分组分桶、中性化改 Sector 后**提交成功**。
  **KOR 实测 S=-0.11（符号翻转）** ⇒ 论坛模板必须本区实测，禁跨区照搬。
  破 sub-universe 手法：`base - group_mean(base,1,industry)` 取残差 + 中性化改 Sector。
- 帖 `35417197662615`（DW88214，2025-10-05）**规避覆盖中的羊群效应**，来源广发金工：
  覆盖度只数数量不看质量，羊群过度推高热门股覆盖。有效修正 = 用成交额/换手率**过去半年分位**识别过热股：
  `if_else` 硬剔除 >95% 分位个股的覆盖度（S 1.63→1.85、F 1.09→1.34）；
  或温和惩罚 `×(1-分位)/0.05`（回撤进一步降至 5.56%）。
  ⚠ **回归取残差法实测不理想**，别走那条。

### 通道 B 实证（论文）

- **Gleason & Lee (2003, TAR)**：修正分「创新性」（新预测同时高于自身旧预测**与**一致预期）vs「羊群性」（向共识靠拢）。
  市场对**创新性修正反应不足** ⇒ 后续漂移更大；羊群性几乎无漂移。低覆盖股漂移更强。
- **华泰金工 (2024)**：高创新性修正 + 剔 3 个月动量残差 ⇒ RankIC 3.99%、TOP 组合年化超额 9.55%。
- **Mill Street**：修正**方向**一个月后仍维持约 83%（收益本身仅 50%）⇒ 修正有持续性。
  breadth（上调占比）比 magnitude（修正幅度）更稳健，窗口约 100 天。
- **Jung, Keeley & Ronen (2019, JAAF)**：**未缩放**的 EPS 修正有效，缩放后失效；低覆盖股更强。
- **Clement & Tse (2005)**：herded 预测**更不准**、含更少分析师私有信息。
- ⚠ **反方证据**：聚簇预测可能是「共享信息」而非羊群（Bernhardt 等）；共同基金追风会导致**反转**而非漂移 ⇒ 方向须本区实测。


## 七、下一步（打样重跑，已按新流程修正）

### 7.1 流程纠错（本轮教训）

初版流程 = **分类 → 骨架**，**跳过了三步**，已补齐：

| 漏掉的步骤 | 本应产出 | 已补 |
|---|---|---|
| **字段质量先验** | alphaCount TOP30 看轴 | ✅ §三·补（**结果直接纠正了方向**） |
| **字段画像五问** | 测什么/怎么测/时间维度/为何存在/可靠性 | ✅ §三·补二 |
| **预处理决策** | 由画像推导的算子与窗口 | ✅ §三·补二 |
| **8 问法** | — | ⚪ **本集按 skill 口径跳过**（见下） |

**关于 8 问法**：`brain-data-feature-engineering` 第 0 步规定 —— analyst 类且字段名含标准财务词汇、
描述覆盖率 ≥ 80% ⇒ 判为**透明集，跳过 8 问**，走「字段画像 → 预处理决策 → 白名单」。
本集实测描述覆盖率 **300/300 = 100%**、描述均值 > 5 词，**确认属透明集**。
⇒ 跳过 8 问是合规的；但**画像五问 / 质量先验 / 预处理决策不能跳**（它们不在豁免范围内）。

### 7.2 Wave14 假设修正

§五 已证伪「盈利口径 + 水平/一阶变化」路线。结合 §三·补 的轴判读，修正为：

> **新假设**：该数据集是「30 标的物 × 4 时间窗」矩阵。
> 真实信号应来自**跨标的物的覆盖广度一致性**（系统性关注变动），
> 而非单标的物（pretax/eps）的强度。单标的物 = 噪声，跨标的物共识 = 信号。

同时 §三·补 显示 **flash 快照家数**（αC=2）与**资产负债表家数**（αC=4）是头部轴，
上一轮完全未触碰。

### 7.3 Wave14 三问（铁律 G）

| 问 | 答 |
|---|---|
| **继承** | Wave11–13 证明「单标的物 + 水平/一阶变化」在 TO<0.10 下已死；继承结论 = 不碰单标的物水平 |
| **准入** | 只测**跨标的物广度一致性**与 **flash−current 窗口差分**；不碰单标的物强度、不扫窗口谱 |
| **收窄** | 候选数 **2**（≤ 上一波 6 的 1/3），先证机制是否存在 |

> 若 Wave14 仍 <0.6，则 `analyst_consensus` **数据集级判死**，转入其余 15 个数据集文档。


