# analyst10 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst10_profile.json`（300 字段）
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
| 类型分布 | MATRIX 152 / VECTOR 148 |
| coverage ≥ 0.5 | 272 / 300 |
| 白空间（alphaCount ≤ 2） | 256 / 300 |
| 平均 coverage | 0.6578 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 78 | 67 | VECTOR40 / MATRIX38 | 66 |
| **创新/修正事件** | 修正行为 | 77 | 64 | MATRIX65 / VECTOR12 | 70 |
| **家数/估计者数量** | 关注广度 | 56 | 52 | MATRIX45 / VECTOR11 | 51 |
| **标志/门控** | 状态位 | 42 | 42 | VECTOR42 | 39 |
| **年龄/时间戳** | 新鲜度 | 33 | 33 | VECTOR33 | 23 |
| **币种/元信息** | 元数据 | 10 | 10 | VECTOR10 | 7 |
| **已实现/实际值** | 事后真值 | 4 | 4 | MATRIX4 | 0 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 296 |
| `actual_` | 4 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `unspecified` | 56 | — | `anl10_det_full_ebi_past_det_estage` (cov 0.792, αC 0) |

## 四、类别 → 经济学骨架映射

### 创新/修正事件 → 骨架：**修正幅度 / 创新性修正**

- **收益来源**：市场对创新性修正反应不足 ⇒ 后续漂移；修正方向持续性强
- **合规/工程注意**：两字段相减须显式声明跨集经济含义
- **字段数**：77｜代表：`anl10_det_full_ebi_past_det_indicator`, `anl10_det_full_sal_past_det_indicator`, `anl10_det_full_gps_past_det_indicator`

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：56｜代表：`anl10_det_full_ebi_past_det_estage`, `anl10_det_full_sal_past_det_estage`, `anl10_det_full_gps_past_det_estage`

### 标志/门控 → 骨架：**门控层**

- **收益来源**：不独立产出信号
- **合规/工程注意**：只作 if_else/trade_when 条件
- **字段数**：42｜代表：`anl10_ebipast_det_estflag_7388`, `anl10_ebipast_det_excflag_7393`, `anl10_netpast_det_estflag_7295`

### 年龄/时间戳 → 骨架：**预测新鲜度**

- **收益来源**：估计越旧信息越衰减；快照 vs 共识的差分刻画更新速度
- **合规/工程注意**：时间戳类字段（YYYYMMDD）禁作信号
- **字段数**：33｜代表：`anl10_ebipast_det_anntime_7395`, `anl10_ebipast_det_estage_7392`, `anl10_netpast_det_anntime_7296`

### 币种/元信息 → 骨架：**—**

- **收益来源**：元数据，无收益来源
- **合规/工程注意**：不进信号；仅可作 group 参数
- **字段数**：10｜代表：`anl10_ebipast_det_indicator_7386`, `anl10_netpast_det_indicator_7303`, `anl10_gpspast_det_indicator_6499`

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：4｜代表：`actual_update_flag_bps`, `actual_update_flag_ebi`, `actual_update_flag_nav`

### ⚠ 未分类 78 条（须逐条人工判读）

- `anl10_analyst_innovation_dps_normal_decrease_fy1` ｜ Normal decrease in data for fiscal year 1 for dividend per share (DPS) forecasts
- `anl10_analyst_innovation_dps_normal_decrease_fy2` ｜ Normal decrease in data for fiscal year 2 for dividend per share (DPS) forecasts
- `anl10_analyst_innovation_dps_normal_increase_fy1` ｜ Normal increase forecast for fiscal year 1 for dividend per share (DPS) forecasts
- `anl10_analyst_innovation_dps_normal_increase_fy2` ｜ Normal increase forecast for fiscal year 2 for dividend per share (DPS) forecasts
- `anl10_analyst_innovation_pre_normal_decrease_fq1` ｜ Normal decrease in data for quarter 1
- `anl10_analyst_innovation_pre_normal_decrease_fq2` ｜ Normal decrease in data for quarter 2
- `anl10_analyst_innovation_pre_normal_decrease_fy1` ｜ Normal decrease in data for fiscal year 1
- `anl10_analyst_innovation_pre_normal_decrease_fy2` ｜ Normal decrease in data for fiscal year 2
- `anl10_analyst_innovation_pre_normal_increase_fq1` ｜ Normal increase forecast for quarter 1
- `anl10_analyst_innovation_pre_normal_increase_fq2` ｜ Normal increase in data for quarter 2
- `anl10_analyst_innovation_pre_normal_increase_fy1` ｜ Normal increase forecast for fiscal year 1
- `anl10_analyst_innovation_pre_normal_increase_fy2` ｜ Normal increase forecast for fiscal year 2
- `anl10_analyst_innovation_sal_normal_decrease_fq1` ｜ Normal decrease in data for quarter 1
- `anl10_analyst_innovation_sal_normal_decrease_fq2` ｜ Normal decrease in data for quarter 2
- `anl10_analyst_innovation_sal_normal_decrease_fy1` ｜ Normal decrease in data for fiscal year 1
- `anl10_analyst_innovation_sal_normal_decrease_fy2` ｜ Normal decrease in sales estimates for FY2
- `anl10_analyst_innovation_sal_normal_increase_fq1` ｜ Normal increase forecast for fq1 period
- `anl10_analyst_innovation_sal_normal_increase_fq2` ｜ Normal increase in data for quarter 2
- `anl10_analyst_innovation_sal_normal_increase_fy1` ｜ Normal increase in sales estimates for FY1
- `anl10_analyst_innovation_sal_normal_increase_fy2` ｜ Normal increase forecast for fiscal year 2
- `anl10_bpspast_det_analyst_7306` ｜ Analyst ID for book value per share estimates
- `anl10_bpspast_det_estvalue_7305` ｜ Estimate value for book value per share
- `anl10_cpxpast_det_analyst_6548` ｜ Analyst ID for capital expenditures estimates
- `anl10_cpxpast_det_estvalue_6553` ｜ Estimate value for capital expenditures
- `anl10_det_full_bps_past_det_analyst` ｜ Unique identifier for the analyst who issued the estimate/event in the detailed IBES chain
- `anl10_det_full_bps_past_det_anntime` ｜ Time of day when the analyst issued the estimate
- `anl10_det_full_cpx_past_det_analyst` ｜ Unique identifier of the analyst who issued the estimate
- `anl10_det_full_dps_past_det_analyst` ｜ Unique identifier for the analyst providing the estimate
- `anl10_det_full_dps_past_det_anntime` ｜ Time of day when the analyst issued the DPS forecast
- `anl10_det_full_ebi_past_det_analyst` ｜ Unique identifier for the analyst who issued the estimate
- … 另有 48 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 37 | 26 | 0.728 | `anl10_cpxpast_det_estage_6549` | Age of capital expenditures estimates in days |
| 20 | 14 | 1.000 | `actual_update_flag_bps` | Flag indicating if book value per share smart estimate was updated bas |
| 18 | 13 | 0.642 | `anl10_preinnovation_score_fy1_7809` | Innovation score for pre-tax or preliminary FY1 (innovate_increase - i |
| 12 | 9 | 0.673 | `anl10_prerevise_ratio_to_consensus_fy1_7803` | Consensus estimate value for pre-tax or preliminary FY1 |
| 11 | 11 | 0.797 | `anl10_netpast_det_indicator_7303` | Indicator for fiscal periods in ASCII values (54=fq1, 55=fq2, 49=fy1,  |
| 11 | 9 | 0.655 | `anl10_analyst_innovation_pre_innovation_score_fy1` | Innovation score for fiscal year 1 (FY1) |
| 10 | 9 | 1.000 | `actual_update_flag_ebi` | Flag indicating if EBIT smart estimate was updated based on actual res |
| 7 | 6 | 0.798 | `anl10_ebipast_det_estvalue_7389` | Estimate value for earnings before interest |
| 7 | 5 | 0.792 | `anl10_det_full_ebi_past_det_estvalue` | Numeric estimate value provided by the analyst at that event |
| 6 | 5 | 1.000 | `actual_update_flag_ndt` | Flag indicating if net debt smart estimate was updated based on actual |
| 6 | 5 | 0.500 | `anl10_det_full_net_past_det_indicator` | Code indicating the event type in the estimate chain (e.g., initiation |
| 6 | 5 | 0.673 | `anl10_preinnovate_decrease_fy1_7823` | Number of analysts with innovative negative revisions for pre-tax or p |
| 6 | 4 | 0.778 | `anl10_bpspast_det_estage_7310` | Age of book value per share estimates in days |
| 5 | 5 | 1.000 | `actual_update_flag_nav` | Flag indicating if net asset value smart estimate was updated based on |
| 5 | 5 | 0.590 | `anl10_analyst_innovation_sal_normal_decrease_fq1` | Normal decrease in data for quarter 1 |
| 5 | 5 | 0.798 | `anl10_ebipast_det_analyst_7394` | Analyst ID for earnings before interest estimates |
| 5 | 5 | 0.673 | `anl10_prerevise_value_fy1_7821` | Delta consensus for pre-tax or preliminary FY1 (difference between old |
| 5 | 5 | 0.613 | `anl10_salinnovation_score_fq1_7866` | Innovation score for sales Q1 (innovate_increase - innovate_decrease) |
| 5 | 4 | 0.798 | `anl10_ebipast_det_anntime_7395` | Announce time for earnings before interest estimates |
| 4 | 4 | 0.468 | `anl10_analyst_innovation_pre_innovate_decrease_fq2` | Decrease forecast of innovation estimate for the second quarter |
| 4 | 4 | 0.655 | `anl10_analyst_innovation_pre_innovate_decrease_fy1` | Number of analysts with innovative negative revisions for pre-tax or p |
| 4 | 4 | 0.728 | `anl10_cpxpast_det_anntime_6554` | Announce time for capital expenditures estimates |
| 4 | 4 | 0.798 | `anl10_ebipast_det_estflag_7388` | Estimate flag for earnings before interest |
| 4 | 4 | 0.795 | `anl10_gpspast_det_anntime_6506` | Announce time for gross profit per share estimates |
| 4 | 4 | 0.795 | `anl10_gpspast_det_estage_6500` | Age of gross profit per share estimates in days |
| 4 | 4 | 0.797 | `anl10_netpast_det_estvalue_7301` | Estimate value for net income |
| 4 | 4 | 0.673 | `anl10_preinnovate_increase_fy1_7820` | Number of analysts with innovative positive revisions for pre-tax or p |
| 4 | 4 | 0.798 | `anl10_salpast_det_analyst_6647` | Analyst ID for sales estimates |
| 4 | 3 | 0.778 | `anl10_bpspast_det_analyst_7306` | Analyst ID for book value per share estimates |
| 4 | 2 | 0.745 | `anl10_det_full_ebt_past_det_estvalue` | Analyst’s EBT forecast value recorded at the event date (as-of snapsho |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl10_cpxpast_det_estage_6549`(αC 37)；`actual_update_flag_bps`(αC 20)；`anl10_preinnovation_score_fy1_7809`(αC 18)；`anl10_prerevise_ratio_to_consensus_fy1_7803`(αC 12)；`anl10_analyst_innovation_pre_innovation_score_fy1`(αC 11)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 创新/修正事件 | — | — | — | — | cov≥0.5 64/77；类型 MATRIX / VECTOR |
| 家数/估计者数量 | — | — | — | — | cov≥0.5 52/56；类型 MATRIX / VECTOR |
| 标志/门控 | — | — | — | — | cov≥0.5 42/42；类型 VECTOR |
| 年龄/时间戳 | — | — | — | — | cov≥0.5 33/33；类型 VECTOR |
| 已实现/实际值 | — | — | — | — | cov≥0.5 4/4；类型 MATRIX |

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
