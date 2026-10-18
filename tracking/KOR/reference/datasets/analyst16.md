# analyst16 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst16_profile.json`（109 字段）
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
| 字段总数 | 109 |
| 类型分布 | VECTOR 109 |
| coverage ≥ 0.5 | 102 / 109 |
| 白空间（alphaCount ≤ 2） | 64 / 109 |
| 平均 coverage | 0.6526 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 47 | 42 | VECTOR47 | 24 |
| **已实现/实际值** | 事后真值 | 34 | 32 | VECTOR34 | 28 |
| **共识均值** | 预期水平 | 10 | 10 | VECTOR10 | 3 |
| **币种/元信息** | 元数据 | 5 | 5 | VECTOR5 | 2 |
| **家数/估计者数量** | 关注广度 | 5 | 5 | VECTOR5 | 1 |
| **分散度/不确定度** | 观点分歧 | 4 | 4 | VECTOR4 | 3 |
| **标志/门控** | 状态位 | 2 | 2 | VECTOR2 | 2 |
| **创新/修正事件** | 修正行为 | 1 | 1 | VECTOR1 | 0 |
| **年龄/时间戳** | 新鲜度 | 1 | 1 | VECTOR1 | 1 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 71 |
| `actual_` | 17 |
| `estimate_` | 4 |
| `period_` | 4 |
| `surprise_` | 3 |
| `basedata_` | 2 |
| `mean_` | 2 |
| `premap_` | 2 |
| `relative_` | 2 |
| `fiscal_` | 1 |
| `no_` | 1 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `unspecified` | 5 | — | `anl16_numests` (cov 0.706, αC 9) |

## 四、类别 → 经济学骨架映射

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：34｜代表：`anl16_estunit_scale_ascontrib`, `anl16_estvalue`, `actual_currency_adjustment`

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：10｜代表：`anl16_meanest`, `anl16_meanest_normal`, `anl16_meanestnorm_estcomsplitadj`

### 币种/元信息 → 骨架：**—**

- **收益来源**：元数据，无收益来源
- **合规/工程注意**：不进信号；仅可作 group 参数
- **字段数**：5｜代表：`anl16_estnorm_estnormcuradj`, `anl16_estvalue_normal`, `estimate_currency_adjustment_factor`

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：5｜代表：`anl16_numests`, `anl16_numincests`, `mean_estimate_period_duration`

### 分散度/不确定度 → 骨架：**分歧度 → 不确定性溢价**

- **收益来源**：分析师意见分歧大 = 信息环境差，风险溢价高
- **合规/工程注意**：离散评分型禁 winsorize/signed_power（无连续尾部）
- **字段数**：4｜代表：`anl16_eststddev`, `anl16_eststddev_normal`, `anl16_aftercons_stddev`

### 标志/门控 → 骨架：**门控层**

- **收益来源**：不独立产出信号
- **合规/工程注意**：只作 if_else/trade_when 条件
- **字段数**：2｜代表：`period_advance_fiscal_year_end_month`, `period_advance_period_length`

### 创新/修正事件 → 骨架：**修正幅度 / 创新性修正**

- **收益来源**：市场对创新性修正反应不足 ⇒ 后续漂移；修正方向持续性强
- **合规/工程注意**：两字段相减须显式声明跨集经济含义
- **字段数**：1｜代表：`anl16_aftercons_percentage`

### 年龄/时间戳 → 骨架：**预测新鲜度**

- **收益来源**：估计越旧信息越衰减；快照 vs 共识的差分刻画更新速度
- **合规/工程注意**：时间戳类字段（YYYYMMDD）禁作信号
- **字段数**：1｜代表：`anl16_interimperiodend`

### ⚠ 未分类 47 条（须逐条人工判读）

- `anl16_1scermun` ｜ Number of recommendations with a value of 1 in the summary
- `anl16_2scermun` ｜ Number of recommendations with a value of 2 in the summary
- `anl16_3scermun` ｜ Number of recommendations with a value of 3 in the summary
- `anl16_4scermun` ｜ Number of recommendations with a value of 4
- `anl16_5scermun` ｜ Number of recommendations with a value of 5 (typically "Sell" or lowest rating)
- `anl16_actnorm_estcomsplitadj` ｜ Adjustment factor for common stock split normalization applied to activity/estimate values
- `anl16_aftercons_difference` ｜ Difference between consensus values after and before the event (after change value minus before change value)
- `anl16_aftercons_high` ｜ Highest value in the consensus after the change
- `anl16_aftercons_low` ｜ Lowest value in the consensus after the event
- `anl16_aftercons_median` ｜ Median value in the consensus after the change
- `anl16_afterest_difference` ｜ Difference between estimate values after and before the event (after change value minus before change value)
- `anl16_afterest_percentage` ｜ Relative change in the earnings estimate: (after change value minus before change value) divided by before cha
- `anl16_afterest_value` ｜ Value of the earnings estimate after the change
- `anl16_beforecons_high` ｜ Highest value in the consensus before the change
- `anl16_beforecons_low` ｜ Lowest value in the consensus before the change
- `anl16_beforecons_median` ｜ Median value in the consensus before the change
- `anl16_beforecons_numitems` ｜ number of values included in the consensus multiply multiplier
- `anl16_beforeest_value` ｜ Value of the earnings estimate before the event
- `anl16_estnorm_estcomsplitadj` ｜ Split-adjusted normalized estimate value.
- `anl16_estunit_scale` ｜ Numeric scale factor applied to the estimate units (e.g., 1, 1e6)
- `anl16_estunit_scale_normal` ｜ Normalized unit scale indicating how the estimate value should be scaled for normalized data
- `anl16_estvalue_ascontrib` ｜ Raw estimate value as contributed by the analyst (unadjusted)
- `anl16_highest` ｜ Highest estimate among contributors
- `anl16_highest_normal` ｜ Highest contributor estimate after normalization
- `anl16_highrec` ｜ Highest recommendation value present in the summary
- `anl16_interimperiodnum` ｜ Number assigned to an interim period (e.g., 1=Q1, 2=Q2, 3=Q3, 4=Q4)
- `anl16_lowest` ｜ Lowest estimate value in the summary
- `anl16_lowest_normal` ｜ Lowest contributor estimate after normalization
- `anl16_lowrec` ｜ Lowest recommendation value present in the summary
- `anl16_medianest` ｜ Median value of the consensus estimate for the period
- … 另有 17 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 27 | 17 | 0.508 | `anl16_1scermun` | Number of recommendations with a value of 1 in the summary |
| 20 | 20 | 0.624 | `anl16_actsurprise` | The magnitude of the actual value surprise in the fiscal report, i.e., |
| 20 | 12 | 0.594 | `anl16_reccode` | The recommendation code indicating the type or category of the analyst |
| 19 | 11 | 0.508 | `anl16_3scermun` | Number of recommendations with a value of 3 in the summary |
| 18 | 10 | 0.508 | `anl16_highrec` | Highest recommendation value present in the summary |
| 16 | 14 | 0.508 | `anl16_2scermun` | Number of recommendations with a value of 2 in the summary |
| 15 | 10 | 0.576 | `anl16_afterest_difference` | Difference between estimate values after and before the event (after c |
| 12 | 7 | 0.697 | `anl16_actnorm_estcomsplitadj` | Adjustment factor for common stock split normalization applied to acti |
| 10 | 8 | 0.508 | `anl16_meanrec` | Mean (average) value of all recommendation scores in the summary |
| 9 | 8 | 0.576 | `anl16_afterest_percentage` | Relative change in the earnings estimate: (after change value minus be |
| 9 | 6 | 0.723 | `anl16_estunit_scale_normal` | Normalized unit scale indicating how the estimate value should be scal |
| 9 | 5 | 0.706 | `anl16_numests` | Number of contributing estimates included in the summary |
| 8 | 7 | 0.508 | `anl16_medianrec` | Median value of all recommendation scores in the summary |
| 8 | 5 | 0.504 | `anl16_actsuescore` | Sentiment score of the actual value surprise, quantifying the degree a |
| 8 | 5 | 0.723 | `anl16_estvalue_normal` | Fully normalized estimate value adjusted for currency, units, and corp |
| 7 | 7 | 0.508 | `anl16_lowrec` | Lowest recommendation value present in the summary |
| 7 | 5 | 0.640 | `anl16_beforecons_mean` | Mean value in the consensus before the event |
| 7 | 5 | 0.706 | `anl16_meanest` | Mean value of the consensus estimate for the period |
| 7 | 4 | 0.508 | `anl16_4scermun` | Number of recommendations with a value of 4 |
| 7 | 3 | 0.706 | `anl16_lowest_normal` | Lowest contributor estimate after normalization |
| 6 | 3 | 0.706 | `anl16_medianest` | Median value of the consensus estimate for the period |
| 6 | 2 | 0.706 | `anl16_eststddev_normal` | Normalized standard deviation of all estimates for the period (shows c |
| 5 | 5 | 0.617 | `anl16_aftercons_percentage` | Relative change in consensus value: (after change value minus before c |
| 5 | 5 | 0.508 | `anl16_scermun` | Total number of recommendations contributing to the summary |
| 5 | 4 | 0.659 | `anl16_afterest_value` | Value of the earnings estimate after the change |
| 5 | 4 | 0.669 | `anl16_beforecons_numitems_orig` | number of individual estimates included in the consensus before the ch |
| 5 | 4 | 0.706 | `anl16_lowest` | Lowest estimate value in the summary |
| 5 | 3 | 0.706 | `anl16_meanestunit_scale_normal` | Normalized scale factor applied to the mean estimate units after curre |
| 5 | 2 | 0.706 | `anl16_numincests` | the number of estimates used to generate the summary analytic values |
| 5 | 2 | 0.622 | `anl16_recvalue` | Recommendation value or score (e.g., numeric buy/hold/sell code) |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl16_1scermun`(αC 27)；`anl16_actsurprise`(αC 20)；`anl16_reccode`(αC 20)；`anl16_3scermun`(αC 19)；`anl16_highrec`(αC 18)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 已实现/实际值 | — | — | — | — | cov≥0.5 32/34；类型 VECTOR |
| 共识均值 | — | — | — | — | cov≥0.5 10/10；类型 VECTOR |
| 家数/估计者数量 | — | — | — | — | cov≥0.5 5/5；类型 VECTOR |
| 分散度/不确定度 | — | — | — | — | cov≥0.5 4/4；类型 VECTOR |
| 标志/门控 | — | — | — | — | cov≥0.5 2/2；类型 VECTOR |
| 创新/修正事件 | — | — | — | — | cov≥0.5 1/1；类型 VECTOR |
| 年龄/时间戳 | — | — | — | — | cov≥0.5 1/1；类型 VECTOR |

**预处理决策（由画像推导，不由拍脑袋）**：

| 画像读数 | 预处理决策 | 依据 |
|---|---|---|
| VECTOR 占比高 | **必须 `vec_avg`/`vec_sum` 降维** | 裸用 `rank`/`ts_*` 秒拒；一条错整批 CANCELLED |
| cov < 0.4 的字段 | 先 `ts_backfill`/`group_backfill` | 体检硬门检查 1 |
| 季频更新（报告日） | 窗口下限 ≥ 63d | 窗口低于更新周期 = 噪声 |
| 单边恒正 | 改变化率 | 体检读数映射 |
| 离散评分型 | 禁 `winsorize`/`signed_power` | 无连续尾部，零效果 |

## 五、本区实测与死因

> **待回填**：本数据集在 KOR/TOP600/D1 的实测读数（S / TO / RN_S / 2Y）与死因归因。
> 死因判据三条：① TO 是否 <0.10（近静态）；② 有效持仓占比；③ risk_neutralized_S vs raw_S。
> ⚠ 预筛更严版：**TO < 0.03 的候选连差分都不要做**（差分只会更低）。

## 六、双通道取证

- **通道 A（论坛）**：`search_forum_posts` 长中文 query 会炸，砍短关键词；`read_forum_post` 必传 `include_comments=false`（true 会 30s 超时）。
- **通道 B（论文）**：`domain_search`。
- **待回填**：本数据集相关的论坛模板与文献机制。

## 七、下一步

> **待回填**：本数据集尚未证伪的假设、下一波设计（须满足铁律 G：候选数 ≤ 上波 1/3，且写明继承/准入/收窄）。
