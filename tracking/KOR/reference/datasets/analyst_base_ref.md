# analyst_base_ref 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst_base_ref_profile.json`（14 字段）
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
| 字段总数 | 14 |
| 类型分布 | VECTOR 10 / MATRIX 4 |
| coverage ≥ 0.5 | 14 / 14 |
| 白空间（alphaCount ≤ 2） | 6 / 14 |
| 平均 coverage | 0.7322 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 6 | 6 | MATRIX4 / VECTOR2 | 2 |
| **已实现/实际值** | 事后真值 | 4 | 4 | VECTOR4 | 1 |
| **共识均值** | 预期水平 | 1 | 1 | VECTOR1 | 1 |
| **标志/门控** | 状态位 | 1 | 1 | VECTOR1 | 0 |
| **分散度/不确定度** | 观点分歧 | 1 | 1 | VECTOR1 | 1 |
| **家数/估计者数量** | 关注广度 | 1 | 1 | VECTOR1 | 1 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `consensus_` | 7 |
| `actual_` | 1 |
| `dilution_` | 1 |
| `last_` | 1 |
| `num_` | 1 |
| `number_` | 1 |
| `reported_` | 1 |
| `split_` | 1 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `unspecified` | 1 | — | `num_estimates_consensus` (cov 0.668, αC 0) |

## 四、类别 → 经济学骨架映射

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：4｜代表：`actual_category`, `consensus_surprise_percentage`, `consensus_vs_actual_diff`

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：1｜代表：`consensus_mean_estimate`

### 标志/门控 → 骨架：**门控层**

- **收益来源**：不独立产出信号
- **合规/工程注意**：只作 if_else/trade_when 条件
- **字段数**：1｜代表：`consensus_median_estimate`

### 分散度/不确定度 → 骨架：**分歧度 → 不确定性溢价**

- **收益来源**：分析师意见分歧大 = 信息环境差，风险溢价高
- **合规/工程注意**：离散评分型禁 winsorize/signed_power（无连续尾部）
- **字段数**：1｜代表：`consensus_stddev_estimate`

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：1｜代表：`num_estimates_consensus`

### ⚠ 未分类 6 条（须逐条人工判读）

- `consensus_high_estimate` ｜ Highest analyst estimate in the consensus snapshot for that metric and period
- `consensus_low_estimate` ｜ Lowest analyst estimate in the consensus snapshot for that metric and period
- `dilution_adjustment_ratio` ｜ Dilution adjustment factor applied to convert/normalize per-share metrics for the chosen dilution regime
- `last_close_price` ｜ Point-in-time corporate-action–adjusted price overlay for the security used in ratios and analytics (not a ful
- `number_of_issued_shares` ｜ Point-in-time shares outstanding for the security, without forward or backfill adjustments
- `split_adjustment_factor` ｜ Stock split adjustment ratio effective on splDate

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 20 | 15 | 0.668 | `consensus_surprise_percentage` | Percentage difference between consensus estimate and actual value for  |
| 11 | 11 | 0.568 | `split_adjustment_factor` | Stock split adjustment ratio effective on splDate |
| 9 | 7 | 1.000 | `last_close_price` | Point-in-time corporate-action–adjusted price overlay for the security |
| 9 | 6 | 1.000 | `number_of_issued_shares` | Point-in-time shares outstanding for the security, without forward or  |
| 6 | 5 | 0.668 | `consensus_median_estimate` | The median of all analysts’ consensus estimates for the indicator or d |
| 4 | 4 | 0.668 | `consensus_vs_actual_diff` | Difference between consensus estimate and actual value for the period. |
| 4 | 3 | 1.000 | `dilution_adjustment_ratio` | Dilution adjustment factor applied to convert/normalize per-share metr |
| 3 | 3 | 0.668 | `actual_category` | Classification of the actual value (e.g., earnings, revenue). |
| 2 | 2 | 0.668 | `consensus_high_estimate` | Highest analyst estimate in the consensus snapshot for that metric and |
| 2 | 2 | 0.668 | `consensus_low_estimate` | Lowest analyst estimate in the consensus snapshot for that metric and  |
| 1 | 1 | 0.668 | `consensus_mean_estimate` | The mean (average) of all analysts’ consensus estimates for the indica |
| 0 | 0 | 0.668 | `consensus_stddev_estimate` | The standard deviation of the analysts’ consensus estimates, indicatin |
| 0 | 0 | 0.668 | `num_estimates_consensus` | The number of analyst estimates contributing to the consensus for this |
| 0 | 0 | 0.668 | `reported_actual_value` | The actual reported value for the indicator or data item for the speci |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`consensus_surprise_percentage`(αC 20)；`split_adjustment_factor`(αC 11)；`last_close_price`(αC 9)；`number_of_issued_shares`(αC 9)；`consensus_median_estimate`(αC 6)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 已实现/实际值 | — | — | — | — | cov≥0.5 4/4；类型 VECTOR |
| 共识均值 | — | — | — | — | cov≥0.5 1/1；类型 VECTOR |
| 标志/门控 | — | — | — | — | cov≥0.5 1/1；类型 VECTOR |
| 分散度/不确定度 | — | — | — | — | cov≥0.5 1/1；类型 VECTOR |
| 家数/估计者数量 | — | — | — | — | cov≥0.5 1/1；类型 VECTOR |

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
