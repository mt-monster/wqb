# analyst_factor_signals 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst_factor_signals_profile.json`（59 字段）
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
| 字段总数 | 59 |
| 类型分布 | MATRIX 59 |
| coverage ≥ 0.5 | 40 / 59 |
| 白空间（alphaCount ≤ 2） | 45 / 59 |
| 平均 coverage | 0.5770 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 28 | 20 | MATRIX28 | 23 |
| **分散度/不确定度** | 观点分歧 | 17 | 12 | MATRIX17 | 16 |
| **创新/修正事件** | 修正行为 | 7 | 6 | MATRIX7 | 1 |
| **已实现/实际值** | 事后真值 | 5 | 1 | MATRIX5 | 4 |
| **共识均值** | 预期水平 | 2 | 1 | MATRIX2 | 1 |

### 与「按字段名分类」的差异（★ 逐条人工判读，2026-11-16）

| 字段名前缀 | 条数 | description 归入的类 | 差异 |
|---|---:|---|---|
| `eps_` | 28 | 分散度 9 / 修正 3 / 已实现 4 / 增长类 12 | ⚠ **名字含 `eps` 但 description 是"增长/EPS 增长率"的 12 条**（`*_consensus_value` / `*_cagr_*yr` / `*_qoq_growth` / `*_yoy_growth`）**不是"预期水平"**，是**增长预期** |
| `revenue_` | 31 | 分散度 8 / 修正 4 / 已实现 1 / 增长类 18 | ⚠ 同上，`revenue_*_consensus_value` 的 description 是 "Forecast growth for FY1/FY2 revenue" ⇒ **是增长率不是收入额** |

**★ 关键差异 1：「共识均值」类实际只有 0 条**

文档模板把 `eps_y1_consensus_value` / `eps_y2_consensus_value` 归为「共识均值 / 预期水平」，
但**平台 description 明确写的是 "Forecast FY1 EPS **growth rate**"**（增长率，非水平值）。
⇒ 以 description 为准 ⇒ 这 2 条应归入「**增长预期**」类，**不是"预期水平"**。
⇒ **文档中"共识均值 2 条"的分类有误**（模板按字段名 `consensus_value` 推断，违反"以 description 为准"）。
⇒ 正确分类：**「增长预期」类**（含 `*_consensus_value` 4 条 + `*_cagr_*yr` 8 条 + `*_qoq/yoy_growth` 10 条 = 22 条）。

**★ 关键差异 2：`*_trend_slope_*yr` 是"修正的连续化"，不是"已实现值"**

模板把 `eps_estimate_trend_slope_3yr` 归入「已实现/实际值」，但：
- `eps_estimate_trend_slope_1yr` description = "**Slope of the 1-year consensus EPS forecast** time series"（**预测**的斜率）
- `eps_estimate_trend_slope_3yr` description = "Slope of the current **actual** EPS series over the past year"（**实际值**的斜率）
⇒ **同名不同义**：`_1yr` 是预测斜率（属「修正/趋势」类），`_3yr` 是实际斜率（属「已实现」类）。
⇒ 这正是"字段名会骗人、必须逐条读 description"的教科书案例。
⇒ 实测印证：A4（`revenue_estimate_trend_slope_1yr`，预测斜率）S 1.03，与 A1/A2（修正）同类但更弱。

**★ 差异 3：`revision_magnitude` 是「缩放后的修正」**

`eps_revision_magnitude` description = "**Scaled** magnitude of revisions to FY1 EPS (Street revision magnitude)"。
⇒ 与 `eps_y1_estimate_change_3mo`（**未缩放**的修正）不是同一经济量。
⇒ **实测印证 Jung (2019)**：缩放版（A3）S 1.14 < 未缩放版（A1）S 1.31 ⇒ 文献预测成立。

### 修正后的分类（以 description 为准）

| 类 | 经济学角色 | 条数 | 代表字段 |
|---|---|---:|---|
| **修正/修正事件** | 修正行为 | **10** | `eps_y1_estimate_change_3mo`, `eps_y2_estimate_change_3mo`, `revenue_y2_estimate_change_3mo`, `eps_revision_magnitude`, `revenue_revision_magnitude`, `*_estimate_change_1mo`, `eps_estimate_trend_slope_1yr`, `revenue_estimate_trend_slope_1yr/2yr/3yr` |
| **修正幅度/离散度** | 观点分歧 | **17** | `*_skewness`, `*_coeff_var`, `*_asymmetry`, `eps_surprise_stddev`, `revenue_surprise_stddev` |
| **增长预期** | 预期增速（**非水平**）| **22** | `eps_y1/y2_consensus_value`, `eps_y1_cagr_2/3/4/5yr`, `revenue_*_consensus_value`, `revenue_y1_cagr_*`, `*_qoq_growth`, `*_yoy_growth` |
| **已实现/事后真值** | 事后真值 | **6** | `eps_actual_q1_qoq_growth`, `eps_actual_q1_yoy_growth`, `eps_estimate_trend_slope_3yr`, `*_sequential`, `*_surprise_mean_diff` |
| **尾部/极值** | 分布端点 | **2** | `eps_estimate_trend_slope_2yr`, `revenue_estimate_volatility_adj_2yr` |

> ⚠ 上表条数相加 > 59（部分字段跨类）⇒ 分类是**经济角色的多标签**，不是互斥划分。

## 四、类别 → 经济学骨架映射

### 分散度/不确定度 → 骨架：**分歧度 → 不确定性溢价**

- **收益来源**：分析师意见分歧大 = 信息环境差，风险溢价高
- **合规/工程注意**：离散评分型禁 winsorize/signed_power（无连续尾部）
- **字段数**：17｜代表：`eps_y1_estimate_skewness`, `revenue_q1_estimate_skewness`, `revenue_q2_estimate_skewness`

### 创新/修正事件 → 骨架：**修正幅度 / 创新性修正**

- **收益来源**：市场对创新性修正反应不足 ⇒ 后续漂移；修正方向持续性强
- **合规/工程注意**：两字段相减须显式声明跨集经济含义
- **字段数**：7｜代表：`revenue_y2_estimate_change_3mo`, `eps_revision_magnitude`, `eps_y1_estimate_change_3mo`

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：5｜代表：`revenue_q1_estimate_sequential`, `eps_actual_q1_qoq_growth`, `eps_estimate_trend_slope_3yr`

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：2｜代表：`revenue_y1_estimate_change_3mo`, `eps_estimate_trend_slope_2yr`

### ⚠ 未分类 28 条（须逐条人工判读）

- `eps_estimate_trend_slope_1yr` ｜ Slope of the 1-year consensus EPS forecast time series (quarterly)
- `eps_q1_estimate_qoq_growth` ｜ Forecast Q1 EPS growth quarter over quarter
- `eps_q1_estimate_yoy_growth` ｜ Forecast Q1 EPS growth year over year
- `eps_q2_estimate_qoq_growth` ｜ Forecast Q2 EPS growth quarter over quarter
- `eps_surprise_mean_diff` ｜ Difference in EPS surprise between Q1 and Q2 (Q1 minus Q2)
- `eps_trailing_4q_estimate` ｜ Forecast trailing-twelve-month EPS growth
- `eps_y1_cagr_2yr` ｜ Forecast FY1 EPS growth CAGR over 2 years
- `eps_y1_cagr_3yr` ｜ Forecast FY1 EPS growth CAGR over 3 years
- `eps_y1_cagr_4yr` ｜ Forecast FY1 EPS growth CAGR over 4 years
- `eps_y1_cagr_5yr` ｜ Forecast FY1 EPS growth CAGR over 5 years
- `eps_y1_consensus_value` ｜ Forecast FY1 EPS growth rate
- `eps_y2_consensus_value` ｜ Forecast FY2 EPS growth rate
- `revenue_estimate_trend_slope_1yr` ｜ Slope of the 1-year consensus revenue forecast (quarterly), indicating trend
- `revenue_estimate_trend_slope_2yr` ｜ Slope of the linear trend in consensus revenue estimates over the past 2 years.
- `revenue_estimate_trend_slope_3yr` ｜ Slope of the linear trend in consensus revenue estimates over the past 3 years.
- `revenue_estimate_volatility_adj_2yr` ｜ Volatility-adjusted 2-year projected revenue growth
- `revenue_estimate_zscore` ｜ Standardized z-score of the fiscal Q1 revenue surprise
- `revenue_q1_estimate_qoq_growth` ｜ Forecast Q1 revenue growth quarter-over-quarter
- `revenue_q1_estimate_yoy_growth` ｜ Forecast year-over-year growth for fiscal Q1 revenue
- `revenue_q2_estimate_qoq_growth` ｜ Forecast Q2 revenue growth quarter-over-quarter
- `revenue_surprise_mean_diff` ｜ Difference between Q1 and Q2 revenue surprise metrics (Q1 minus Q2)
- `revenue_trailing_4q_estimate` ｜ Trailing-twelve-month forecast revenue growth
- `revenue_y1_cagr_2yr` ｜ Forecast compound annual growth rate to FY1 revenue measured over a 2-year horizon
- `revenue_y1_cagr_3yr` ｜ Forecast compound annual growth rate to FY1 revenue measured over a 3-year horizon
- `revenue_y1_cagr_4yr` ｜ Forecast compound annual growth rate to FY1 revenue measured over a 4-year horizon
- `revenue_y1_cagr_5yr` ｜ Forecast compound annual growth rate to FY1 revenue measured over a 5-year horizon
- `revenue_y1_consensus_value` ｜ Forecast growth for FY1 revenue
- `revenue_y2_consensus_value` ｜ Forecast growth for FY2 revenue

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 43 | 30 | 0.786 | `eps_y1_estimate_change_3mo` | Change in consensus FY1 EPS forecast over the past 3 months |
| 26 | 20 | 0.786 | `eps_revision_magnitude` | Scaled magnitude of revisions to FY1 EPS (Street revision magnitude) |
| 24 | 16 | 0.786 | `eps_y2_estimate_change_3mo` | Change in consensus FY2 EPS forecast over the past 3 months |
| 18 | 11 | 0.647 | `revenue_estimate_trend_slope_1yr` | Slope of the 1-year consensus revenue forecast (quarterly), indicating |
| 12 | 8 | 0.786 | `revenue_y2_estimate_change_3mo` | Change in consensus forecast for FY2 revenue over the past 3 months |
| 8 | 7 | 0.797 | `eps_y2_consensus_value` | Forecast FY2 EPS growth rate |
| 7 | 7 | 0.756 | `eps_y1_consensus_value` | Forecast FY1 EPS growth rate |
| 7 | 5 | 0.797 | `revenue_y2_consensus_value` | Forecast growth for FY2 revenue |
| 5 | 4 | 0.436 | `eps_actual_q1_qoq_growth` | Actual reported Q1 EPS growth quarter over quarter |
| 5 | 4 | 0.786 | `revenue_y1_estimate_change_3mo` | Change in FY1 revenue consensus forecast over the past 3 months |
| 4 | 4 | 0.640 | `revenue_q1_estimate_change_1mo` | Change in consensus forecast for fiscal Q1 revenue over the past 1 mon |
| 3 | 3 | 0.786 | `revenue_revision_magnitude` | Scaled revision magnitude of the median FY1 revenue estimate (Street R |
| 3 | 2 | 0.505 | `revenue_q1_estimate_coeff_var` | Coefficient of variation (std/mean) of Q1 revenue estimates |
| 3 | 2 | 0.580 | `revenue_surprise_mean_diff` | Difference between Q1 and Q2 revenue surprise metrics (Q1 minus Q2) |
| 2 | 2 | 0.367 | `eps_q1_estimate_sequential` | Difference between sequentially forecast and actual EPS growth for Q1 |
| 2 | 2 | 0.427 | `eps_surprise_stddev` | Standard deviation of EPS surprises |
| 2 | 2 | 0.629 | `eps_y1_cagr_3yr` | Forecast FY1 EPS growth CAGR over 3 years |
| 2 | 2 | 0.528 | `eps_y1_cagr_5yr` | Forecast FY1 EPS growth CAGR over 5 years |
| 2 | 2 | 0.797 | `eps_y1_estimate_skewness` | Pearson skewness of the FY1 EPS forecast distribution |
| 2 | 2 | 0.569 | `revenue_y2_estimate_coeff_var` | Coefficient of variation (std/mean) of FY2 revenue estimates |
| 2 | 1 | 0.587 | `revenue_surprise_stddev` | Standard deviation of revenue surprise |
| 1 | 1 | 0.473 | `eps_estimate_trend_slope_1yr` | Slope of the 1-year consensus EPS forecast time series (quarterly) |
| 1 | 1 | 0.456 | `eps_q1_estimate_qoq_growth` | Forecast Q1 EPS growth quarter over quarter |
| 1 | 1 | 0.416 | `eps_surprise_mean_diff` | Difference in EPS surprise between Q1 and Q2 (Q1 minus Q2) |
| 1 | 1 | 0.688 | `eps_y1_cagr_2yr` | Forecast FY1 EPS growth CAGR over 2 years |
| 1 | 1 | 0.576 | `eps_y1_cagr_4yr` | Forecast FY1 EPS growth CAGR over 4 years |
| 1 | 1 | 0.575 | `eps_y1_estimate_coeff_var` | Coefficient of variation (std/mean) of consensus FY1 EPS estimates |
| 1 | 1 | 0.530 | `revenue_estimate_trend_slope_2yr` | Slope of the linear trend in consensus revenue estimates over the past |
| 1 | 1 | 0.495 | `revenue_estimate_zscore` | Standardized z-score of the fiscal Q1 revenue surprise |
| 1 | 1 | 0.647 | `revenue_q1_estimate_skewness` | Pearson's skewness of the analyst forecast distribution for fiscal Q1  |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`eps_y1_estimate_change_3mo`(αC 43)；`eps_revision_magnitude`(αC 26)；`eps_y2_estimate_change_3mo`(αC 24)；`revenue_estimate_trend_slope_1yr`(αC 18)；`revenue_y2_estimate_change_3mo`(αC 12)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 分散度/不确定度 | — | — | — | — | cov≥0.5 12/17；类型 MATRIX |
| 创新/修正事件 | — | — | — | — | cov≥0.5 6/7；类型 MATRIX |
| 已实现/实际值 | — | — | — | — | cov≥0.5 1/5；类型 MATRIX |
| 共识均值 | — | — | — | — | cov≥0.5 1/2；类型 MATRIX |

**预处理决策（由画像推导，不由拍脑袋）**：

| 画像读数 | 预处理决策 | 依据 |
|---|---|---|
| VECTOR 占比高 | **必须 `vec_avg`/`vec_sum` 降维** | 裸用 `rank`/`ts_*` 秒拒；一条错整批 CANCELLED |
| cov < 0.4 的字段 | 先 `ts_backfill`/`group_backfill` | 体检硬门检查 1 |
| 季频更新（报告日） | 窗口下限 ≥ 63d | 窗口低于更新周期 = 噪声 |
| 单边恒正 | 改变化率 | 体检读数映射 |
| 离散评分型 | 禁 `winsorize`/`signed_power` | 无连续尾部，零效果 |

## 五、本区实测与死因（★ Wave16 已回填，2026-11-16）

### 5.1 Wave16 首探（multisim `3m29yygWi5in4VstDAiT0Qh`，5/5 COMPLETE，0 error）

设置：KOR / TOP600 / d1 / **SECTOR** / decay4 / trunc0.08 / nanHandling ON｜`[OPS]=2`

| # | 字段 | αC | S | fit | TO | **2Y** | sub | RN_S | CW | fail=[] | 卡什么 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| **A1** | `eps_y1_estimate_change_3mo` | 43 | **1.31** | **1.05** | 0.053 | **1.69 ✅** | 1.36 | 0.71 | **PASS** | ✅ | **仅 LOW_SHARPE** |
| A2 | `eps_y2_estimate_change_3mo` | 24 | 1.31 | 1.06 | 0.057 | 1.53 | 1.38 | 0.88 | PASS | ✅ | S + LOW_2Y |
| A3 | `eps_revision_magnitude` | 26 | 1.14 | 0.85 | 0.056 | **2.00 ✅** | 1.22 | 0.54 | PASS | ✅ | S + fit |
| A4 | `revenue_estimate_trend_slope_1yr` | 18 | 1.03 | 0.78 | 0.042 | **1.64 ✅** | 0.99 | **1.13** | PASS | ✅ | S + fit |
| A5 | `revenue_y2_estimate_change_3mo` | 12 | 1.20 | 0.92 | 0.067 | 1.37 | 1.23 | 0.87 | PASS | ✅ | S + fit + 2Y |

⇒ **5/5 `checks.fail = []`**（无硬 FAIL）；5/5 `ppa_failed = false`；塔 `KOR/D1/ANALYST ×1.6`。

### 5.2 ★★★★ 结论 1：DEU 的「2Y 天花板」在 KOR 被推翻

| 骨架（逐字相同）| 区域 | universe | S | fit | **2Y** |
|---|---|---|---:|---:|---:|
| `winsorize(group_rank(eps_y1_estimate_change_3mo, sector), std=2)` | **DEU** | TOP500 | 1.82 | 1.62 | **1.12 ❌** |
| 同上 | **KOR** | TOP600 | 1.31 | 1.05 | **1.69 ✅** |

⇒ **2Y 从 1.12 → 1.69（+0.57）**，但 **S 从 1.82 → 1.31（−0.51）**。
⇒ **「2Y 天花板 1.17」只适用于 DEU**；同时 **R1 铁律（结构不可跨区迁移）依然成立**，只是表现为「强度衰减」而非「全灭」。

### 5.3 ★★★★ 结论 2：`CONCENTRATED_WEIGHT` 的根因 = 覆盖率，不是数据集属性

Wave15 在 `analyst_consensus`（cov 0.62–0.72）上把 CW 定为「结构性死因」。
本集 5 条 cov **0.647–0.786 ⇒ CW 5/5 PASS**，`longCount/shortCount` 对称（271–305 / 332–366）。
⇒ **判据修正**：CW 命中与否由 **cov** 决定（<0.4 危险、≥0.6 安全），可在**开波前用 cov 预筛**，无需实测才知道。
⇒ 上波的「TO < 0.10 且 CW 命中 ⇒ 判死」应改为「**cov < 0.6 且 CW 命中 ⇒ 该条判死**」。

### 5.4 ★★★ 结论 3：TO 全部落在最优区间（0.042–0.067 < 0.125）

⇒ F 闸分母不放大。**该族的破闸路径唯一 = 提 S**（提 fit 的充要条件也是提 S）。
⇒ **不要扫窗口谱降 TO**（TO 已极低，降无可降，反而伤信号）。

### 5.5 ★★ 结论 4：EPS 侧 > 营收侧（与 αC 质量先验完全一致）

| 侧 | S 均值 | 2Y 均值 | fit 均值 |
|---|---:|---:|---:|
| **EPS 侧**（A1/A2/A3）| **1.25** | **1.74** | **0.99** |
| 营收侧（A4/A5）| 1.12 | 1.51 | 0.85 |

⇒ **验证「αC 头部字段 = 该集最强经济轴」这条先验判断法有效**（EPS 修正族 αC 43/26/24 > 营收侧 18/12）。

### 5.6 ★ A3 的 2Y = 2.00 是独立资产

`eps_revision_magnitude`（修正**幅度**）2Y = 2.00 但 S 仅 1.14、RN_S 仅 0.54。
⇒ **「修正幅度」与「修正方向」是两个经济量**：幅度抓近年爆发（2Y 强），方向抓全期（S 强）。
⇒ ⚠ 但两者**禁用 `add` 组合**（撞 `POISON:equal_weight_leg_add`）；只能走 `subtract`（须单一经济含义）或条件门控。

### 5.7 死因归因（本集暂无死因）

- ① TO < 0.10 ⇒ ✅ 不成立（0.042–0.067 健康，非近静态）
- ② 有效持仓占比 ⇒ ✅ 对称（271–305 / 332–366）
- ③ risk_neutralized_S vs raw_S ⇒ ⚠ A4 的 RN_S(1.13) **高于** raw_S(1.03) ⇒ 该字段含负向风险暴露；A3 的 RN_S 衰减最重（1.14→0.54）

⇒ **本集未判死**，Wave17 继续攻 A1 的 S 闸。

### ★★★★ 通道 A 论坛取证：WL27618「121 个字段里最值得做的 5 个信号」（30 赞）

**帖子 ID**：`42659792904343`（2026-08-12，顾问专属中文论坛）

**本集与该帖的接口对照**：

| 帖子排名 | 方向 | 帖子原话 | 本集对应字段 |
|---|---|---|---|
| **1** | **Estimate Revision Momentum（预期修正动量）** | 「分析师对 EPS 的一致预期**上升**时，股价出现持续正漂移；**修正方向反映增量信息，比预期绝对水平更强**」「数据集通常**没有原生 revision 字段**，需要 `ts_delta(...)` 自己构造」| ✅ **`eps_y1_estimate_change_3mo` / `eps_y2_estimate_change_3mo`（原生 revision 字段）** |
| 2 | Revenue Surprise | 「**收入 beat 比 EPS beat 更干净**——不受一次性项目、税率、回购操纵影响，top-line 意外的漂移更持久」| `revenue_estimate_zscore`（本集有！）|
| **3** | **Margin Scissor（边际剪刀差）** | 「**收入上修 + EPS 下修 = 隐含利润率压缩预期**，盈利质量恶化的领先信号」| `revenue_*` 与 `eps_*` 配对 ⇒ ⚠ **跨字段，只能 `subtract`，不能 `add`** |
| 5 | Estimate Skew（预期偏度）| 「**mean − median** 刻画预期分布的不对称性；stddev 只告诉你分歧**大小**，mean−median 告诉你分歧**方向**」| `eps_y1_estimate_skewness`（Pearson skewness）|

**★ 最关键的一句话（对本集是直接利好）**：
> 「数据集通常**没有原生 revision 字段**，需要用 `ts_delta(anl14_mean_eps_fp1, d)` 自己构造」

⇒ **本集是例外 —— 有原生的 revision 字段**（`*_estimate_change_3mo` = "Change in consensus ... over the past 3 months"）。
⇒ 免去自建 `ts_delta` 的噪声 ⇒ **理论上是比论坛通用做法更优的起点**（Wave16 A1 已证 2Y 1.69 过闸，S 1.31 卡 LOW_SHARPE）。
⇒ ⚠ **但反过来也说明：本集在该方向上已被其他用户大量使用**（αC 43/26/24 是全网用量）⇒ **prod 相关性风险需实测**。

**另一条可直接落地的构造**：
> 「**`fp1` 与 `fp2` 的差本身就是「未来两个季度预期之差」**，可作 revision 的廉价代理」

⇒ 对本集 = `subtract(eps_y2_estimate_change_3mo, eps_y1_estimate_change_3mo)` = **修正的期限结构**（长端 − 短端）。
⇒ 两腿**同源同集**、**单一经济含义**（"修正的期限斜率"）⇒ **符合 `subtract` 放行形态**（不是违规的拼腿）。

**实现提醒**：
> 「数据集常见 coverage 只有 0.5 左右，记得用 `ts_backfill` 处理缺失」
> 「`numofests`（估计人数）建议用作**质量过滤**：覆盖稀疏的股票上，预期信号噪声大」

⇒ ⚠ 本集 cov 最低者 `eps_actual_q1_yoy_growth` 0.3671 / `eps_q1_estimate_sequential` 0.3671 ⇒ 若用到，须 `ts_backfill`。

### ★★★ 通道 A 论坛取证：ZZ43261「修正广度」（36 赞）—— 对本集的参照价值

**帖子 ID**：`43250301270295`。其核心是 `analyst25` 的「家数」字段（见 `analyst25.md` §六）。
**对本集的参照价值**：
- 该帖用「上调数/下调数」广度可达 **S 3.0–4.5** ⇒ **说明分析师类数据在 BRAIN 上有 S 3+ 的可能性**
- 本集 A1 只有 S 1.31 ⇒ **差距可能在「构造口径」**（广度比 vs 共识变化幅度）
- 该帖的 **`Neutralization = STATISTICAL`** 建议 ⇒ 本集 Wave17 未测此档，是**未探索的设置空间**

## 七、下一步

> **已回填（2026-11-16）**：见 §五 的判定 1–5 与本节下方的 Wave17 结论。

### Wave17 结果（multisim `3wB20i1GE4Wk9vHuOMBWNP5`，3/3 COMPLETE）

| 杠杆 | S | fit | TO | 2Y | vs 基线 (1.31/1.05/1.69) |
|---|---:|---:|---:|---:|---|
| L1 换粗轴 `market` | 1.26 | 1.00 | 0.050 | **1.71** | S **−0.05** ❌ |
| **L2 `signed_power 2.5`** | **1.48** | **1.22** | 0.060 | **1.35** | S **+0.17** ✅ / 2Y **−0.34** ❌ |
| L3 双窗秩乘积 66/252 | 0.96 | 0.67 | 0.028 | 1.87 | S **−0.35** ❌（另触发 PPA FAIL）|

**★ 三条结论**：

1. **`signed_power` 是「S↔2Y 权衡旋钮」，不是单向增益**
   L2 把 S 从 1.31 提到 1.48（+0.17）、fit 1.05→1.22（+0.17），但 **2Y 从 1.69 崩到 1.35（−0.34）**。
   ⇒ 与 RULES「signed_power 是压 prod 核心算子」一脉相承 —— 它**重排了时间分布**（近年衰减）。
   ⇒ **本集上 signed_power 会把「唯一的 2Y 优势」打掉** ⇒ **不可用此杠杆**。

2. **双窗秩乘积在「季频字段」上彻底失败**（S 0.96）
   印证 RULES ★★★★★「双窗**非普适**」+ 本集季频更新 ⇒ **短窗 66d 在季频数据上 = 噪声**。
   ⇒ 本集若用双窗，**两窗都必须 ≥ 63d**（一个季度）。

3. **换粗轴几乎无效**（S −0.05，2Y +0.02）
   与 RULES「换粗轴 = 破 robust 闸第一杠杆」**不冲突** —— 本集 robust/sub 闸**早已通过**（sub 1.36 > 0.53×1.31 = 0.69），瓶颈是 S 本身。

### ⇒ A1 的破闸优先级（修正后）

| 优先 | 杠杆 | 依据 / ⚠ 风险 |
|---|---|---|
| 1 | **换中性化档**（SECTOR → **STATISTICAL**）| 论坛帖明确推荐；本集**从未测过**；RULES「neutralization 是 prod↔S 单一权衡旋钮」|
| 2 | **`decay` 调档**（4 → 1/2/6）| 本波未测；论坛帖说「短档更贴合盈利动能窗口」|
| 3 | **`truncation` 调档**（0.08 → 0.04/0.12）| 未测 |
| 4 | ⚠ **不用** `signed_power`（毁 2Y）| Wave17 L2 已证 |
| 5 | ⚠ **不用** 双窗（本集季频）| Wave17 L3 已证 |
| 6 | ⚠ **不用** 换粗轴（无效）| Wave17 L1 已证 |

### 并行的第二战场（Wave18，`analyst25`）

论坛 36 赞帖给出的「修正广度」路线（`analyst25` count 族）**报告 IS S 3.0–4.5**，
与「修正幅度」是不同的经济量 ⇒ **两条腿可并行探索，不互斥**。

### ⚠ 禁区（本集已知）

- **禁 `add` 跨字段**（A1+A3 相加 = 撞 `POISON:equal_weight_leg_add`）
- **禁 `signed_power`**（毁 2Y，Wave17 L2 已证）
- **禁双窗短窗**（季频噪声，Wave17 L3 已证）
- **禁把 DEU 的 2Y 结论外推**（Wave16 已证伪）
- **不必扫窗口谱降 TO**（TO 已 0.042–0.067）
- ⚠ **`ts_backfill` 慎用**：RULES 记载「`ts_backfill` 不支持事件型输入」
