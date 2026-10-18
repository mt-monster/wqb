# analyst14 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst14_profile.json`（300 字段）
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
| 类型分布 | MATRIX 295 / VECTOR 5 |
| coverage ≥ 0.5 | 300 / 300 |
| 白空间（alphaCount ≤ 2） | 138 / 300 |
| 平均 coverage | 0.5000 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 179 | 179 | MATRIX174 / VECTOR5 | 68 |
| **共识均值** | 预期水平 | 74 | 74 | MATRIX74 | 38 |
| **已实现/实际值** | 事后真值 | 45 | 45 | MATRIX45 | 32 |
| **分散度/不确定度** | 观点分歧 | 2 | 2 | MATRIX2 | 0 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 300 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

## 四、类别 → 经济学骨架映射

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：74｜代表：`anl14_all_mean_eps_fy1`, `anl14_all_mean_eps_fy2`, `anl14_mean_bvps_fp1`

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：45｜代表：`anl14_high_epsrep_fp1`, `anl14_high_epsrep_fp2`, `anl14_high_epsrep_fp3`

### 分散度/不确定度 → 骨架：**分歧度 → 不确定性溢价**

- **收益来源**：分析师意见分歧大 = 信息环境差，风险溢价高
- **合规/工程注意**：离散评分型禁 winsorize/signed_power（无连续尾部）
- **字段数**：2｜代表：`anl14_all_stddev_eps_fy1`, `anl14_all_stddev_eps_fy2`

### ⚠ 未分类 179 条（须逐条人工判读）

- `anl14_all_high_eps_fy1` ｜ The highest estimation of earnings per share - upcoming year
- `anl14_all_high_eps_fy2` ｜ The highest estimation of earnings per share - upcoming 2 years
- `anl14_all_low_eps_fy1` ｜ The lowest estimation of earnings per share - upcoming year
- `anl14_all_low_eps_fy2` ｜ The Lowest Estimation of Earnings Per Share - upcoming 2 years
- `anl14_all_median_eps_fy1` ｜ Median of Estimations of Earnings Per Share - Upcoming Year
- `anl14_all_median_eps_fy2` ｜ Median of estimations of Earnings Per Share - upcoming 2 years
- `anl14_all_numofests_eps_fy1` ｜ Num of Estimations of Earnings Per Share - Upcoming Year
- `anl14_all_numofests_eps_fy2` ｜ Num of estimations of earnings per share - upcoming 2 years
- `anl14_curperiodtype` ｜ Type of Period -
- `anl14_cursharesoutstanding` ｜ Current Share Outstanding -
- `anl14_estq_broker` ｜ Broker name -
- `anl14_estvalue` ｜ Estimation Value -
- `anl14_estvalue_fp3` ｜ Estimation Value - upcoming 3 quarters
- `anl14_estvalue_fp4` ｜ Estimation value - upcoming 4 quarters
- `anl14_estvalue_fp5` ｜ Estimation value - upcoming 5 quarters
- `anl14_high_bvps_fp1` ｜ The Highest Estimation of Book Value Per Share - Upcoming Quarter
- `anl14_high_bvps_fp2` ｜ The Highest Estimation of Book Value Per Share - Upcoming 2 Quarters
- `anl14_high_bvps_fp3` ｜ The Highest Estimation of Book Value Per Share - upcoming 3 quarters
- `anl14_high_bvps_fp4` ｜ The highest estimation of book value per share - upcoming 4 quarters
- `anl14_high_bvps_fp5` ｜ The Highest Estimation of Book Value Per Share - Upcoming 5 Quarters
- `anl14_high_bvps_fy1` ｜ The highest estimation of Book Value Per Share - upcoming year
- `anl14_high_bvps_fy2` ｜ The highest estimation of Book Value Per Share - upcoming 2 years
- `anl14_high_capex_fy1` ｜ The highest estimation of Capital Expenditures - upcoming year
- `anl14_high_capex_fy2` ｜ The Highest Estimation of Capital Expenditures - upcoming 2 years
- `anl14_high_ebit_fp1` ｜ The highest estimation of earnings before interest & taxes - upcoming quarter
- `anl14_high_ebit_fp2` ｜ The Highest Estimation of Earnings Before Interest & Taxes - upcoming 2 quarters
- `anl14_high_ebit_fp3` ｜ The Highest Estimation of Earnings Before Interest & Taxes - upcoming 3 quarters
- `anl14_high_ebit_fp4` ｜ The highest estimation of earnings before interest & taxes - upcoming 4 quarters
- `anl14_high_ebit_fp5` ｜ The Highest Estimation of Earnings Before Interest & Taxes - upcoming 5 quarters
- `anl14_high_ebit_fy1` ｜ The Highest Estimation of Earnings Before Interest & Taxes - Upcoming Year
- … 另有 149 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 525 | 168 | 0.500 | `anl14_all_high_eps_fy1` | The highest estimation of earnings per share - upcoming year |
| 312 | 88 | 0.500 | `anl14_all_low_eps_fy1` | The lowest estimation of earnings per share - upcoming year |
| 265 | 81 | 0.500 | `anl14_all_mean_eps_fy1` | Mean of estimations of earnings per share - upcoming year |
| 212 | 58 | 0.500 | `anl14_cursharesoutstanding` | Current Share Outstanding - |
| 192 | 53 | 0.500 | `anl14_curperiodtype` | Type of Period - |
| 120 | 42 | 0.500 | `anl14_all_numofests_eps_fy1` | Num of Estimations of Earnings Per Share - Upcoming Year |
| 119 | 44 | 0.500 | `anl14_high_capex_fy1` | The highest estimation of Capital Expenditures - upcoming year |
| 118 | 43 | 0.500 | `anl14_all_median_eps_fy1` | Median of Estimations of Earnings Per Share - Upcoming Year |
| 110 | 39 | 0.500 | `anl14_all_numofests_eps_fy2` | Num of estimations of earnings per share - upcoming 2 years |
| 104 | 59 | 0.500 | `anl14_all_high_eps_fy2` | The highest estimation of earnings per share - upcoming 2 years |
| 92 | 32 | 0.500 | `anl14_all_median_eps_fy2` | Median of estimations of Earnings Per Share - upcoming 2 years |
| 84 | 41 | 0.500 | `anl14_all_mean_eps_fy2` | Mean of Estimations of Earnings Per Share - upcoming 2 years |
| 73 | 35 | 0.500 | `anl14_all_low_eps_fy2` | The Lowest Estimation of Earnings Per Share - upcoming 2 years |
| 65 | 12 | 0.500 | `anl14_high_ebitda_fp4` | The highest estimation of earnings before interest, taxes, depreciatio |
| 59 | 31 | 0.500 | `anl14_high_ebit_fy2` | The highest estimation of Earnings Before Interest & Taxes - upcoming  |
| 56 | 23 | 0.500 | `anl14_all_stddev_eps_fy1` | Standard Deviation of Estimations of Earnings Per Share - upcoming yea |
| 52 | 8 | 0.500 | `anl14_high_ebitda_fp1` | The highest estimation of earnings before interest, taxes, depreciatio |
| 45 | 24 | 0.500 | `anl14_high_capex_fy2` | The Highest Estimation of Capital Expenditures - upcoming 2 years |
| 41 | 24 | 0.500 | `anl14_high_ebit_fp1` | The highest estimation of earnings before interest & taxes - upcoming  |
| 40 | 18 | 0.500 | `anl14_estvalue` | Estimation Value - |
| 40 | 12 | 0.500 | `anl14_mean_ndebt_fy2` | Mean of Estimations of Net Debt - upcoming 2 years |
| 40 | 5 | 0.500 | `anl14_high_ebitda_fp2` | The Highest Estimation of Earnings Before Interest, Taxes, Depreciatio |
| 39 | 16 | 0.500 | `anl14_all_stddev_eps_fy2` | Standard Deviation of Estimations of Earnings Per Share - upcoming 2 y |
| 38 | 3 | 0.500 | `anl14_high_ebitda_fp3` | The highest estimation of Earnings Before Interest, Taxes, Depreciatio |
| 35 | 16 | 0.500 | `anl14_high_ntprep_fp1` | The Highest Estimation of Reported Net Profit - upcoming quarter |
| 34 | 12 | 0.500 | `anl14_high_bvps_fp1` | The Highest Estimation of Book Value Per Share - Upcoming Quarter |
| 33 | 17 | 0.500 | `anl14_estq_broker` | Broker name - |
| 32 | 12 | 0.500 | `anl14_mean_roe_fy2` | Mean of Estimations of Returns on Equity - upcoming 2 years |
| 30 | 23 | 0.500 | `anl14_high_ebit_fy1` | The Highest Estimation of Earnings Before Interest & Taxes - Upcoming  |
| 30 | 14 | 0.500 | `anl14_mean_capex_fy2` | Mean of Estimations of Capital Expenditures - upcoming 2 years |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl14_all_high_eps_fy1`(αC 525)；`anl14_all_low_eps_fy1`(αC 312)；`anl14_all_mean_eps_fy1`(αC 265)；`anl14_cursharesoutstanding`(αC 212)；`anl14_curperiodtype`(αC 192)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 共识均值 | — | — | — | — | cov≥0.5 74/74；类型 MATRIX |
| 已实现/实际值 | — | — | — | — | cov≥0.5 45/45；类型 MATRIX |
| 分散度/不确定度 | — | — | — | — | cov≥0.5 2/2；类型 MATRIX |

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
