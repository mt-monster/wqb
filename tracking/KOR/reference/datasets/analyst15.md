# analyst15 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst15_profile.json`（300 字段）
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
| 类型分布 | MATRIX 300 |
| coverage ≥ 0.5 | 300 / 300 |
| 白空间（alphaCount ≤ 2） | 13 / 300 |
| 平均 coverage | 0.5192 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 139 | 139 | MATRIX139 | 11 |
| **共识均值** | 预期水平 | 87 | 87 | MATRIX87 | 0 |
| **家数/估计者数量** | 关注广度 | 53 | 53 | MATRIX53 | 2 |
| **分散度/不确定度** | 观点分歧 | 18 | 18 | MATRIX18 | 0 |
| **年龄/时间戳** | 新鲜度 | 3 | 3 | MATRIX3 | 0 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 288 |
| `group_` | 5 |
| `industry_` | 5 |
| `sector_` | 2 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `unspecified` | 53 | — | `anl15_gr_12_m_ests` (cov 0.500, αC 771) |

## 四、类别 → 经济学骨架映射

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：87｜代表：`anl15_gr_12_m_cos`, `anl15_gr_12_m_cos_dn`, `anl15_gr_12_m_cos_up`

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：53｜代表：`anl15_gr_12_m_ests`, `anl15_gr_12_m_ests_dn`, `anl15_gr_12_m_ests_up`

### 分散度/不确定度 → 骨架：**分歧度 → 不确定性溢价**

- **收益来源**：分析师意见分歧大 = 信息环境差，风险溢价高
- **合规/工程注意**：离散评分型禁 winsorize/signed_power（无连续尾部）
- **字段数**：18｜代表：`anl15_gr_12_m_st_dev`, `anl15_gr_18_m_st_dev`, `anl15_gr_cal_fy1_st_dev`

### 年龄/时间戳 → 骨架：**预测新鲜度**

- **收益来源**：估计越旧信息越衰减；快照 vs 共识的差分刻画更新速度
- **合规/工程注意**：时间戳类字段（YYYYMMDD）禁作信号
- **字段数**：3｜代表：`anl15_gr_18_m_ests_dn`, `anl15_gr_18_m_ests_up`, `anl15_s_fy3_ests_up`

### ⚠ 未分类 139 条（须逐条人工判读）

- `anl15_gr_12_m_1m_chg` ｜ Weighted one-month percent change in 12-month forward earnings forecasts at the group level (constant sample)
- `anl15_gr_12_m_3m_chg` ｜ Weighted three-month percent change in 12-month forward earnings forecasts for the group
- `anl15_gr_12_m_6m_chg` ｜ Weighted six-month percent change in 12-month forward earnings forecasts for the group
- `anl15_gr_12_m_gro` ｜ Weighted 12-month forward year-over-year EPS growth at the group level
- `anl15_gr_12_m_total` ｜ The total of 12-month forward earnings estimation aggregated within GICS group grouping.
- `anl15_gr_18_m_1m_chg` ｜ Weighted one-month percent change in 18-month forward earnings forecasts, using a constant sample, aggregated 
- `anl15_gr_18_m_3m_chg` ｜ Weighted three-month percent change in the 18-month forward earnings forecasts at the group level, using a con
- `anl15_gr_18_m_6m_chg` ｜ Weighted six‑month percent change in the forward 18‑month earnings forecast, constant sample, at the group lev
- `anl15_gr_18_m_gro` ｜ The weighted 18-month forward year-over-year growth of EPS estimation aggregated within GICS group grouping.
- `anl15_gr_18_m_total` ｜ Total earnings for the forward 18 months for companies in the group
- `anl15_gr_cal_fy0_gro` ｜ The weighted year-over-year growth of EPS estimation for the current calendarized fiscal year aggregated withi
- `anl15_gr_cal_fy0_total` ｜ The total of earnings estimation for the current calendarized fiscal year aggregated within GICS group groupin
- `anl15_gr_cal_fy1_1m_chg` ｜ Weighted one-month percent change in calendarized FY1 earnings forecasts for the group, using a constant sampl
- `anl15_gr_cal_fy1_3m_chg` ｜ Weighted three-month percent change in calendarized FY1 earnings forecasts at the group level (constant sample
- `anl15_gr_cal_fy1_6m_chg` ｜ Weighted six-month percent change in calendarized FY1 earnings forecasts for the group, using a constant sampl
- `anl15_gr_cal_fy1_cos` ｜ The number of companies with a calendarized 1 fiscal year EPS estimation within GICS group grouping.
- `anl15_gr_cal_fy1_gro` ｜ Weighted year-over-year growth in earnings for calendarized Fiscal Year 1 at the group level
- `anl15_gr_cal_fy1_total` ｜ The total of earnings estimation for the calendarized 1 fiscal year aggregated within GICS group grouping.
- `anl15_gr_cal_fy2_1m_chg` ｜ Weighted one-month percent change in calendarized FY2 earnings forecasts at the group level (constant sample)
- `anl15_gr_cal_fy2_3m_chg` ｜ Weighted three-month percent change in the calendarized FY2 earnings forecast for the industry group, using a 
- `anl15_gr_cal_fy2_6m_chg` ｜ Weighted six-month percent change in calendarized Fiscal Year 2 earnings forecasts using a constant sample, ag
- `anl15_gr_cal_fy2_cos` ｜ The number of companies with a calendarized 2 fiscal year EPS estimation within GICS group grouping.
- `anl15_gr_cal_fy2_gro` ｜ Weighted year-over-year earnings growth for calendarized FY2 at the group level
- `anl15_gr_cal_fy2_total` ｜ Total earnings for the calendarized Fiscal Year 2 period for the group
- `anl15_gr_cal_fy3_1m_chg` ｜ Group-level weighted one-month percent change in calendarized FY3 earnings forecasts using a constant sample
- `anl15_gr_cal_fy3_3m_chg` ｜ Weighted three-month percent change in calendarized FY3 earnings forecasts at the group level (constant sample
- `anl15_gr_cal_fy3_6m_chg` ｜ Weighted six-month percent change in calendarized FY3 earnings forecasts for the group, using a constant sampl
- `anl15_gr_cal_fy3_cos` ｜ The number of companies with a calendarized 3 fiscal year EPS estimation within GICS group grouping.
- `anl15_gr_cal_fy3_gro` ｜ Weighted year-over-year earnings growth for calendarized Fiscal Year 3 at the group level
- `anl15_gr_cal_fy3_total` ｜ Total sum of calendarized Fiscal Year 3 earnings/estimates aggregated at the group level
- … 另有 109 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 2920 | 140 | 0.500 | `anl15_gr_ltg_cos_up` | Number of companies in the group whose long-term growth median was rai |
| 2773 | 165 | 0.500 | `anl15_s_cal_fy3_ests` | Number of estimates for calendarized Fiscal Year 3 at the sector level |
| 2321 | 142 | 0.500 | `anl15_s_18_m_ests` | Number of analyst estimates for the 18-month forward period in the sec |
| 2225 | 109 | 0.500 | `anl15_s_ltg_cos` | The number of companies with a long-term growth EPS estimation within  |
| 2143 | 108 | 0.500 | `anl15_s_18_m_gro` | Weighted 18‑month forward earnings growth for the sector |
| 1960 | 105 | 0.500 | `anl15_ind_ltg_cos_up` | Number of companies for which the long-term growth consensus was raise |
| 1905 | 112 | 0.500 | `anl15_s_fy1_ests_up` | Number of Fiscal Year 1 analyst estimates raised since last month in t |
| 1898 | 193 | 0.500 | `anl15_s_cal_fy2_ests` | Number of estimates for calendarized Fiscal Year 2 at the sector level |
| 1779 | 120 | 0.500 | `anl15_ind_prc` | Weighted average share price of companies in the industry |
| 1700 | 124 | 0.500 | `anl15_s_18_m_ests_dn` | Number of estimates with negative revisions for the sector’s 18‑month  |
| 1632 | 125 | 0.500 | `anl15_s_12_m_ests_dn` | Number of 12-month forward estimates lowered since last month at the s |
| 1625 | 107 | 0.500 | `anl15_s_18_m_6m_chg` | Weighted six-month percent change in 18-month forward earnings forecas |
| 1623 | 114 | 0.500 | `anl15_s_fy2_ests_up` | Number of FY2 earnings estimates raised since last month for the secto |
| 1572 | 139 | 0.500 | `anl15_s_12_m_ests` | Number of analyst estimates contributing to the 12-month forward perio |
| 1564 | 131 | 0.500 | `anl15_s_12_m_ests_up` | Pro-rated number of forward 12-month earnings estimates raised since l |
| 1489 | 109 | 0.500 | `anl15_ind_fy1_cos_dn` | Number of companies for which the calendarized Fiscal Year 1 mean was  |
| 1388 | 136 | 0.500 | `anl15_s_fy1_ests_dn` | Number of Fiscal Year 1 earnings estimates lowered since last month, a |
| 1352 | 104 | 0.500 | `anl15_ind_fy2_cos_dn` | Number of companies in the industry whose calendarized Fiscal Year 2 m |
| 1339 | 149 | 0.500 | `anl15_s_fy3_cos_dn` | The number of companies for which EPS estimation for the calendarized  |
| 1323 | 109 | 0.500 | `anl15_s_cal_fy1_cos` | The number of companies with a calendarized 1 fiscal year EPS estimati |
| 1309 | 121 | 0.500 | `anl15_s_18_m_ests_up` | Sector-level number of estimates with positive revision over the trail |
| 1288 | 109 | 0.500 | `anl15_ind_12_m_tr_mean` | Weighted average trailing 12-month EPS for the industry |
| 1280 | 104 | 0.500 | `anl15_s_18_m_cos` | The number of companies with an 18-month forward mean EPS estimation w |
| 1263 | 107 | 0.500 | `anl15_gr_ltg_mdn` | Weighted median long-term growth forecast for the group |
| 1259 | 105 | 0.500 | `anl15_ind_cal_fy3_ests` | Number of analyst estimates for calendarized Fiscal Year 3 at the indu |
| 1255 | 111 | 0.500 | `anl15_s_cal_fy2_total` | The total of earnings estimation for the calendarized 2 fiscal year ag |
| 1237 | 107 | 0.500 | `anl15_s_cal_fy3_cos` | The number of companies with a calendarized 3 fiscal year EPS estimati |
| 1236 | 97 | 0.500 | `anl15_s_fy3_cos_up` | Number of companies in the sector whose calendarized FY3 mean EPS was  |
| 1214 | 129 | 0.500 | `anl15_gr_cal_fy3_ests` | Number of analyst estimates contributing to the calendarized FY3 conse |
| 1214 | 106 | 0.500 | `anl15_s_fy2_ests_dn` | Number of Fiscal Year 2 estimates lowered since last month, aggregated |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl15_gr_ltg_cos_up`(αC 2920)；`anl15_s_cal_fy3_ests`(αC 2773)；`anl15_s_18_m_ests`(αC 2321)；`anl15_s_ltg_cos`(αC 2225)；`anl15_s_18_m_gro`(αC 2143)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 共识均值 | — | — | — | — | cov≥0.5 87/87；类型 MATRIX |
| 家数/估计者数量 | — | — | — | — | cov≥0.5 53/53；类型 MATRIX |
| 分散度/不确定度 | — | — | — | — | cov≥0.5 18/18；类型 MATRIX |
| 年龄/时间戳 | — | — | — | — | cov≥0.5 3/3；类型 MATRIX |

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
