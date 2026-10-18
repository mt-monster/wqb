# analyst11 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst11_profile.json`（210 字段）
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
| 字段总数 | 210 |
| 类型分布 | MATRIX 210 |
| coverage ≥ 0.5 | 126 / 210 |
| 白空间（alphaCount ≤ 2） | 202 / 210 |
| 平均 coverage | 0.5831 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **排名/分位** | 相对位置 | 183 | 108 | MATRIX183 | 178 |
| **未分类** | — | 21 | 12 | MATRIX21 | 19 |
| **共识均值** | 预期水平 | 6 | 6 | MATRIX6 | 5 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `community_` | 28 |
| `environmental_` | 21 |
| `governance_` | 21 |
| `social_` | 21 |
| `workforce_` | 21 |
| `sustainability_` | 20 |
| `employee_` | 14 |
| `anti_` | 7 |
| `board_` | 7 |
| `disclosure_` | 7 |
| `human_` | 7 |
| `management_` | 7 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

## 四、类别 → 经济学骨架映射

### 排名/分位 → 骨架：**横截面相对位置**

- **收益来源**：同业内相对位置，剥离行业共性
- **合规/工程注意**：⚠ 可能与本数据集已有的 rank 字段重复
- **字段数**：183｜代表：`sustainability_industry_rank`, `sustainability_sector_rank`, `sustainability_subsector_rank`

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：6｜代表：`overall_sustainability_score`, `environmental_pillar_composite_score`, `community_pillar_composite_score`

### ⚠ 未分类 21 条（须逐条人工判读）

- `anti_pollution_policy_score` ｜ Aggregated environmental transparency KPI reflecting company policies, reporting, and dedication to environmen
- `board_independence_diversity_score` ｜ KPI for Board Effectiveness, aggregating data on Board independence, diversity, and effectiveness in meeting f
- `community_corr_weighted_score` ｜ Score for Capital Investment KPIs (CIT1, CIT2, CIT3) weighted by strongest (positive and negative) correlation
- `community_engagement_score` ｜ KPI measuring company performance in community and charitable activities, public health, and local social/envi
- `community_positive_corr_score` ｜ Score for Capital Investment KPIs (CIT1, CIT2, CIT3) weighted by positive correlations with financial metrics 
- `disclosure_transparency_accountability_score` ｜ A composite KPI measuring Disclosure & Accountability: assesses the quality of financial and sustainability re
- `employee_compensation_satisfaction_score` ｜ Employment KPI 1 measures how well the company fosters employee satisfaction through fair pay, benefits, and p
- `employee_training_safety_score` ｜ KPI measuring company performance on education, work conditions, workplace safety, training, and health
- `environmental_corr_weighted_score` ｜ A composite Environmental (E) score built by weighting E1, E2, and E3 KPIs according to the strength of both p
- `environmental_positive_corr_score` ｜ A composite Environmental (E) score built by weighting E1, E2, and E3 KPIs according to their positive correla
- `human_rights_supply_chain_score` ｜ KPI for Human Rights, aggregating data on a company's policies and performance regarding human rights issues s
- `management_ethics_standards_score` ｜ KPI for Management Ethics, measuring management's stakeholder relations, ethical decision-making, equitable sh
- `pollution_prevention_score` ｜ Aggregated pollution prevention KPI reflecting how well a company is reducing pollution and transitioning to l
- `resource_efficiency_score` ｜ Aggregated resource efficiency KPI reflecting how well a company reduces resource use and implements recycling
- `social_corr_weighted_score` ｜ Composite score for social KPIs (EMP1, EMP2, EMP3, CIT1, CIT2, CIT3) weighted by their absolute correlation (p
- `social_positive_corr_score` ｜ A composite Social (S) score created by weighting EMP1, EMP2, EMP3, CIT1, CIT2, and CIT3 according to their po
- `sustainability_max_correlation_score` ｜ A composite ESG score where each underlying KPI is weighted according to its strongest (positive or negative) 
- `sustainable_product_business_model_score` ｜ KPI for Sustainability Integration, measuring how well a company transitions its products and operations towar
- `workforce_corr_weighted_score` ｜ Score for Employment KPIs (EMP1, EMP2, EMP3) weighted by their strongest correlations (positive and negative) 
- `workforce_positive_corr_score` ｜ Score for Employment KPIs (EMP1, EMP2, EMP3) weighted by their positive correlations with financial metrics li
- `workplace_diversity_labor_rights_score` ｜ KPI measuring company performance on workplace diversity, labor-management relations, and workforce rights

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 5 | 5 | 0.671 | `anti_pollution_policy_score` | Aggregated environmental transparency KPI reflecting company policies, |
| 5 | 3 | 0.681 | `pollution_prevention_industry_rank` | Rank of the company within its industry peer group based on the OWL E1 |
| 5 | 2 | 0.656 | `board_independence_diversity_score` | KPI for Board Effectiveness, aggregating data on Board independence, d |
| 4 | 4 | 0.682 | `environmental_industry_position` | Rank of company’s E score within its industry peer group, with 1 being |
| 4 | 4 | 0.697 | `social_pillar_composite_score` | Composite Social (S) Score calculated as the average of the CIT (Citiz |
| 3 | 3 | 0.656 | `anti_pollution_policy_industry_rank` | Rank of the company within its industry peer group based on the OWL E2 |
| 3 | 3 | 0.682 | `sustainability_sector_rank` | Rank of company within its sector based on its overall ESG score, with |
| 3 | 2 | 0.652 | `anti_pollution_policy_industry_percentile` | Percentile ranking of the company within its industry peer group on th |
| 2 | 2 | 0.694 | `community_engagement_score` | KPI measuring company performance in community and charitable activiti |
| 2 | 2 | 0.455 | `community_hybrid_sector_percentile` | Percentile ranking of the Citizenship hybrid score for the company wit |
| 2 | 2 | 0.651 | `employee_compensation_satisfaction_score` | Employment KPI 1 measures how well the company fosters employee satisf |
| 2 | 2 | 0.648 | `employee_training_industry_rank` | Rank of company within its industry peer group on the EMP3 KPI (educat |
| 1 | 1 | 0.652 | `anti_pollution_policy_sector_percentile` | Percentile ranking of the company within its sector peer group on the  |
| 1 | 1 | 0.656 | `anti_pollution_policy_sector_rank` | Rank of the company within its sector peer group based on the OWL E2 K |
| 1 | 1 | 0.641 | `board_independence_industry_rank` | Rank of the company's Board Effectiveness KPI (G1) within its industry |
| 1 | 1 | 0.679 | `community_engagement_industry_rank` | Rank of company within its industry peer group on the CIT1 KPI (commun |
| 1 | 1 | 0.455 | `community_hybrid_industry_percentile` | Percentile ranking of a company's CIT Hybrid score within its industry |
| 1 | 1 | 0.682 | `community_score_subsector_position` | Rank of the company within its subsector peer group based on the overa |
| 1 | 1 | 0.682 | `community_sector_position` | Rank of the company within its sector peer group based on the overall  |
| 1 | 1 | 0.647 | `disclosure_transparency_industry_rank` | Rank of a company within its industry peer group on the G3 governance  |
| 1 | 1 | 0.643 | `disclosure_transparency_sector_percentile` | Percentile of company within its sector for the OWL G3 Disclosure & Ac |
| 1 | 1 | 0.647 | `disclosure_transparency_sector_rank` | Rank of company within its sector based on the OWL G3 Disclosure & Acc |
| 1 | 1 | 0.632 | `employee_compensation_subsector_percentile` | Percentile ranking of Employment KPI 1 for the company within its subs |
| 1 | 1 | 0.648 | `employee_training_sector_rank` | Rank of company within its sector peer group on the EMP3 KPI (educatio |
| 1 | 1 | 0.439 | `environmental_positive_corr_industry_percentile` | Percentile of company’s E Hybrid score within industry peer group (100 |
| 1 | 1 | 0.467 | `governance_corr_weighted_score` | Governance Max Correlation Score, calculated by weighting G1, G2, and  |
| 1 | 1 | 0.657 | `governance_industry_position` | Rank of a company within its industry peer group based on the Governan |
| 1 | 1 | 0.440 | `governance_positive_corr_score` | Governance Hybrid Score, calculated by weighting G1, G2, and G3 based  |
| 1 | 1 | 0.440 | `governance_positive_corr_sector_position` | Rank of a company within its sector peer group based on the Governance |
| 1 | 1 | 0.653 | `governance_sector_percentile` | Percentile of a company within its sector peer group based on the Gove |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anti_pollution_policy_score`(αC 5)；`board_independence_diversity_score`(αC 5)；`pollution_prevention_industry_rank`(αC 5)；`environmental_industry_position`(αC 4)；`social_pillar_composite_score`(αC 4)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 排名/分位 | — | — | — | — | cov≥0.5 108/183；类型 MATRIX |
| 共识均值 | — | — | — | — | cov≥0.5 6/6；类型 MATRIX |

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
