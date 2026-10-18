# analyst9 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst9_profile.json`（48 字段）
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
| 字段总数 | 48 |
| 类型分布 | VECTOR 47 / MATRIX 1 |
| coverage ≥ 0.5 | 33 / 48 |
| 白空间（alphaCount ≤ 2） | 26 / 48 |
| 平均 coverage | 0.5672 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 24 | 21 | VECTOR23 / MATRIX1 | 17 |
| **创新/修正事件** | 修正行为 | 11 | 7 | VECTOR11 | 0 |
| **家数/估计者数量** | 关注广度 | 7 | 2 | VECTOR7 | 4 |
| **标志/门控** | 状态位 | 5 | 3 | VECTOR5 | 4 |
| **已实现/实际值** | 事后真值 | 1 | 0 | VECTOR1 | 1 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 39 |
| `consensus_` | 2 |
| `revision_` | 2 |
| `eps_` | 1 |
| `estimate_` | 1 |
| `estimated_` | 1 |
| `income_` | 1 |
| `parent_` | 1 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `unspecified` | 7 | — | `anl9_s_numanalystall` (cov 0.711, αC 1) |

## 四、类别 → 经济学骨架映射

### 创新/修正事件 → 骨架：**修正幅度 / 创新性修正**

- **收益来源**：市场对创新性修正反应不足 ⇒ 后续漂移；修正方向持续性强
- **合规/工程注意**：两字段相减须显式声明跨集经济含义
- **字段数**：11｜代表：`anl9_revisions_effectivetime`, `anl9_s_numdn`, `anl9_s_numdownunfiltered`

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：7｜代表：`anl9_s_numanalystall`, `anl9_s_numanalysts`, `anl9_daily_numanalystall`

### 标志/门控 → 骨架：**门控层**

- **收益来源**：不独立产出信号
- **合规/工程注意**：只作 if_else/trade_when 条件
- **字段数**：5｜代表：`anl9_isnmflag`, `anl9_isexcluded`, `anl9_parentflag`

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：1｜代表：`estimate_currency_code_2`

### ⚠ 未分类 24 条（须逐条人工判读）

- `anl9_confirmtime` ｜ Intraday time of the most recent confirmation of the current estimate
- `anl9_consensusanalysis_dataitemvalue` ｜ Numeric consensus estimate value for the specified data item
- `anl9_consensusanalysis_effectivetime` ｜ Intra-day time when the consensus estimate calculation became effective
- `anl9_consensusv2span_incomeeps_dataitemvalue` ｜ Numeric consensus estimate value for the specified data item
- `anl9_consensusv2span_incomeeps_effectivetime` ｜ Intra-day time when the estimate becomes effective or is calculated
- `anl9_consensusv2span_incomeeps_splitfactor` ｜ Ratio used to unadjust per-share EPS estimates for stock splits that occur after the estimate’s EffectiveDate
- `anl9_consensusv2span_incomeeps_totime` ｜ End time when the estimate’s validity window ends
- `anl9_consensusv2span_incomeothers_dataitemvalue` ｜ Numeric consensus estimate value for the specified data item
- `anl9_consensusv2span_incomeothers_effectivetime` ｜ Intra-day time when the consensus estimate became effective (time of calculation)
- `anl9_consensusv2span_incomeothers_splitfactor` ｜ Adjustment factor for corporate actions (e.g., stock splits) applied to maintain comparability of estimates
- `anl9_consensusv2span_incomeothers_totime` ｜ Intra-day time when the estimate’s validity period ends
- `anl9_detail_dataitemvalue` ｜ Numeric value of the estimated metric
- `anl9_detail_effectivetime` ｜ Time of day when the estimate became effective (start time of validity)
- `anl9_detail_totime` ｜ End time of the estimate’s validity period (intraday)
- `anl9_eps_splitfactor` ｜ Split factor
- `anl9_estanalystmap` ｜ Human-readable name/description of the analyst corresponding to estimateAnalystIx
- `anl9_estimatetime` ｜ Intra-day time at which the estimate was recorded/issued
- `anl9_others_splitfactor` ｜ Split factor
- `consensus_analysis_value` ｜ <baseModule>.ConsensusIdIx idx
- `eps_consensus_estimate_value` ｜ Lookup index identifying the consensus category/type for the estimate
- `estimated_metric_value` ｜ Numeric value of the estimate for the specified metric
- `income_other_consensus_value` ｜ <baseModule>.ConsensusIdIx idx
- `revision_consensus_value` ｜ Index key referencing the consensus estimate category in the ConsensusId lookup
- `revision_consensus_value_revisions` ｜ Integer code identifying the consensus estimate category for the metric/period, joinable to a consensus lookup

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 14 | 7 | 0.711 | `anl9_s_numanalysts` | Number of analysts whose estimates are included in the consensus for t |
| 12 | 6 | 0.711 | `anl9_s_numupunfiltered` | Total analysts with upward revisions, including those excluded from th |
| 11 | 7 | 0.711 | `anl9_s_numdn` | Count of downward revisions included in the consensus during the speci |
| 10 | 10 | 0.443 | `anl9_daily_numup` | Count of upward revisions among analysts included in the consensus |
| 10 | 6 | 0.711 | `anl9_s_numup` | Count of upward revisions included in the consensus during the specifi |
| 9 | 5 | 0.443 | `anl9_daily_numdownunfiltered` | Total number of analysts whose estimates were revised downward, includ |
| 7 | 7 | 0.443 | `anl9_daily_numupunfiltered` | Total number of analysts whose estimates were revised upward, includin |
| 7 | 6 | 0.443 | `anl9_daily_numdn` | Count of downward revisions among analysts included in the consensus |
| 6 | 6 | 0.602 | `anl9_consensusv2span_incomeothers_dataitemvalue` | Numeric consensus estimate value for the specified data item |
| 6 | 3 | 0.711 | `anl9_revisions_effectivetime` | Time when the revision snapshot/estimate was calculated |
| 6 | 1 | 0.443 | `anl9_daily_numnochg` | Count of revisions with no change among analysts included in the conse |
| 6 | 1 | 0.606 | `consensus_analysis_value` | <baseModule>.ConsensusIdIx idx |
| 5 | 4 | 0.602 | `anl9_consensusv2span_incomeothers_totime` | Intra-day time when the estimate’s validity period ends |
| 5 | 3 | 0.528 | `anl9_detail_totime` | End time of the estimate’s validity period (intraday) |
| 4 | 4 | 0.606 | `anl9_consensusanalysis_dataitemvalue` | Numeric consensus estimate value for the specified data item |
| 4 | 3 | 0.579 | `anl9_consensusv2span_incomeeps_splitfactor` | Ratio used to unadjust per-share EPS estimates for stock splits that o |
| 4 | 2 | 0.711 | `anl9_s_numnochg` | Number of revisions with no change in the consensus (included analysts |
| 4 | 1 | 0.443 | `anl9_revisiondaily_effectivetime` | Time when the revision metrics were calculated or became effective |
| 3 | 3 | 0.579 | `anl9_consensusv2span_incomeeps_dataitemvalue` | Numeric consensus estimate value for the specified data item |
| 3 | 3 | 0.528 | `anl9_isexcluded` | Flag indicating the estimate is excluded from consensus/analysis due t |
| 3 | 2 | 0.711 | `anl9_s_numdownunfiltered` | Total analysts with downward revisions, including those excluded from  |
| 3 | 2 | 0.711 | `anl9_s_numnochangeunfiltered` | Total number of no-change revisions, without exclusions |
| 2 | 2 | 0.606 | `anl9_consensusanalysis_effectivetime` | Intra-day time when the consensus estimate calculation became effectiv |
| 2 | 2 | 0.579 | `anl9_consensusv2span_incomeeps_effectivetime` | Intra-day time when the estimate becomes effective or is calculated |
| 2 | 2 | 0.528 | `anl9_detail_effectivetime` | Time of day when the estimate became effective (start time of validity |
| 2 | 2 | 0.839 | `anl9_estanalystmap` | Human-readable name/description of the analyst corresponding to estima |
| 2 | 2 | 0.528 | `anl9_estimatetime` | Intra-day time at which the estimate was recorded/issued |
| 2 | 2 | 0.606 | `anl9_isnmflag` | Flag indicating the estimate is not meaningful (NM) |
| 2 | 2 | 0.711 | `revision_consensus_value_revisions` | Integer code identifying the consensus estimate category for the metri |
| 1 | 1 | 0.466 | `anl9_confirmtime` | Intraday time of the most recent confirmation of the current estimate |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl9_s_numanalysts`(αC 14)；`anl9_s_numupunfiltered`(αC 12)；`anl9_s_numdn`(αC 11)；`anl9_daily_numup`(αC 10)；`anl9_s_numup`(αC 10)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 创新/修正事件 | — | — | — | — | cov≥0.5 7/11；类型 VECTOR |
| 家数/估计者数量 | — | — | — | — | cov≥0.5 2/7；类型 VECTOR |
| 标志/门控 | — | — | — | — | cov≥0.5 3/5；类型 VECTOR |
| 已实现/实际值 | — | — | — | — | cov≥0.5 0/1；类型 VECTOR |

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
