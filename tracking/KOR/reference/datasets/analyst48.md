# analyst48 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst48_profile.json`（70 字段）
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
| 字段总数 | 70 |
| 类型分布 | VECTOR 70 |
| coverage ≥ 0.5 | 35 / 70 |
| 白空间（alphaCount ≤ 2） | 39 / 70 |
| 平均 coverage | 0.4411 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 44 | 19 | VECTOR44 | 27 |
| **年龄/时间戳** | 新鲜度 | 18 | 11 | VECTOR18 | 6 |
| **标志/门控** | 状态位 | 6 | 4 | VECTOR6 | 4 |
| **创新/修正事件** | 修正行为 | 1 | 1 | VECTOR1 | 1 |
| **已实现/实际值** | 事后真值 | 1 | 0 | VECTOR1 | 1 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 70 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

## 四、类别 → 经济学骨架映射

### 年龄/时间戳 → 骨架：**预测新鲜度**

- **收益来源**：估计越旧信息越衰减；快照 vs 共识的差分刻画更新速度
- **合规/工程注意**：时间戳类字段（YYYYMMDD）禁作信号
- **字段数**：18｜代表：`anl48_bnepd`, `anl48_bc_dvd_declared_dt`, `anl48_bdvd_next_est_ex_dt`

### 标志/门控 → 骨架：**门控层**

- **收益来源**：不独立产出信号
- **合规/工程注意**：只作 if_else/trade_when 条件
- **字段数**：6｜代表：`anl48_equity_return_code`, `anl48_bbt`, `anl48_equity_bulk_bdvd_all_projections_return_code`

### 创新/修正事件 → 骨架：**修正幅度 / 创新性修正**

- **收益来源**：市场对创新性修正反应不足 ⇒ 后续漂移；修正方向持续性强
- **合规/工程注意**：两字段相减须显式声明跨集经济含义
- **字段数**：1｜代表：`anl48_equity_bulk_eqy_dvd_hist_gross_return_code`

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：1｜代表：`anl48_equity_ldg`

### ⚠ 未分类 44 条（须逐条人工判读）

- `anl48_bbpdiip` ｜ Amount of projected dividends expressed in index points, indicating the expected dividend impact within a spec
- `anl48_bbpsa` ｜ The amount of dividend projected or paid per share
- `anl48_bdha` ｜ Amount of dividend historically announced for the security
- `anl48_bdvd_curr_dir_therm` ｜ Type of security (equity, ADR, ETF, etc.), likely using numeric or floating-point codes
- `anl48_bdvd_curr_dvd_health` ｜ Current metric indicating the strength or sustainability of the dividend
- `anl48_bedhga` ｜ Historical gross dividend amount per share
- `anl48_bp12m_dip` ｜ Projected total dividend for the next 12 months, expressed in index points for the index
- `anl48_bp12m_yld` ｜ Projected dividend yield over the next 12 months
- `anl48_bp3y_dg` ｜ Projected growth rate of dividends over the next 3 years
- `anl48_bpda` ｜ The next projected dividend per share amount according to Bloomberg's forecasts
- `anl48_bulk_bdvd_all_projections_ibs` ｜ Bloomberg security identifier; unique code for the specific security as listed in Bloomberg
- `anl48_bulk_bdvd_all_projections_par_amt` ｜ Par amount, i.e., the face value of the security issued
- `anl48_bulk_count_index_members` ｜ The number of constituent stocks in the index
- `anl48_bulk_dvd_hist_ibs` ｜ Bloomberg security identifier, uniquely identifies individual security
- `anl48_bulk_dvd_hist_par_amt` ｜ Par amount or face value of the security issued
- `anl48_bulk_eqy_dvd_hist_gross_ibs` ｜ Bloomberg unique identifier for the security (e.g., specific share class or instrument)
- `anl48_bulk_eqy_dvd_hist_gross_par_amt` ｜ Face value or principal amount of the security issued
- `anl48_bulk_idivisor` ｜ The divisor used in index calculations to maintain continuity following changes such as corporate actions
- `anl48_bulk_indx_typ` ｜ Numeric code representing the type of index (e.g., price, total return, sector-based, etc.)
- `anl48_count_index_members` ｜ The total number of stocks that are members of the index
- `anl48_dvd_xe` ｜ Ex-dividend amount or relevant value indicating the period when securities are traded without dividend entitle
- `anl48_edg3yr_g` ｜ Growth rate of gross dividends per share over the past 3 years
- `anl48_equity_bulk_bdvd_all_projections_ibc` ｜ Bloomberg company identifier; unique code for the issuing company of the security
- `anl48_equity_bulk_bdvd_all_projections_nfields` ｜ The number of fields present in the record or data row
- `anl48_equity_bulk_dvd_hist_ibc` ｜ Bloomberg Company Identifier, a unique code used by Bloomberg to identify the company
- `anl48_equity_bulk_dvd_hist_nfields` ｜ Number of fields present in the data record or dataset
- `anl48_equity_bulk_eqy_dvd_hist_gross_ibc` ｜ Bloomberg unique identifier for the company
- `anl48_equity_bulk_eqy_dvd_hist_gross_nfields` ｜ Number of fields included in the record or dataset
- `anl48_equity_dvd_sh_last` ｜ The most recent net dividend amount paid per share
- `anl48_equity_ibc` ｜ Bloomberg unique identifier for the company associated with the security
- … 另有 14 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 42 | 12 | 0.504 | `anl48_bdhad` | Date when the dividend was announced for the security in question |
| 42 | 5 | 0.515 | `anl48_bdvd_curr_dvd_health` | Current metric indicating the strength or sustainability of the divide |
| 31 | 10 | 0.537 | `anl48_bnepd` | Next estimated dividend payment date (expected when the dividend will  |
| 25 | 7 | 0.507 | `anl48_bedhgad` | Date when dividend was historically announced |
| 21 | 2 | 0.507 | `anl48_equity_bulk_eqy_dvd_hist_gross_ibc` | Bloomberg unique identifier for the company |
| 16 | 1 | 0.324 | `anl48_bp12m_dip` | Projected total dividend for the next 12 months, expressed in index po |
| 13 | 2 | 0.515 | `anl48_bnedd` | Next estimated date when the dividend will be officially declared |
| 13 | 2 | 0.515 | `anl48_dvd_declared_dt` | The official date when the dividend was formally declared by the compa |
| 13 | 2 | 0.325 | `anl48_index_bulk_ibc` | Unique Bloomberg identifier for the company associated with the index  |
| 12 | 5 | 0.515 | `anl48_bbpsa` | The amount of dividend projected or paid per share |
| 10 | 4 | 0.488 | `anl48_bedhgrd` | Date recording ownership entitlement for the dividend payout (record d |
| 10 | 3 | 0.298 | `anl48_bulk_indx_typ` | Numeric code representing the type of index (e.g., price, total return |
| 9 | 8 | 0.478 | `anl48_equity_m21_dly_dvd_yqe` | Gross dividend yield for the past 12 months, often calculated as divid |
| 9 | 3 | 0.325 | `anl48_index_bulk_return_code` | Code indicating the result or status of a data retrieval or event, suc |
| 9 | 1 | 0.515 | `anl48_bbt` | Indicator or metric showing the trend or direction of dividend project |
| 9 | 1 | 0.314 | `anl48_index_td_xe_dvd` | The last or most recent ex-dividend date, i.e., the date when new buye |
| 8 | 2 | 0.325 | `anl48_index_bulk_nfields` | Number of fields present within this dataset record |
| 7 | 3 | 0.325 | `anl48_bbpdiip` | Amount of projected dividends expressed in index points, indicating th |
| 7 | 3 | 0.507 | `anl48_bedhged` | Historical ex-dividend date for dividend event |
| 6 | 4 | 0.515 | `anl48_bdvd_next_est_ex_dt` | Estimated date when shares will go ex-dividend for the next dividend e |
| 5 | 1 | 0.515 | `anl48_equity_bulk_bdvd_all_projections_ibc` | Bloomberg company identifier; unique code for the issuing company of t |
| 4 | 2 | 0.515 | `anl48_bc_dvd_declared_dt` | The date on which the dividend was formally declared by the company |
| 4 | 2 | 0.436 | `anl48_edg3yr_g` | Growth rate of gross dividends per share over the past 3 years |
| 4 | 2 | 0.504 | `anl48_equity_bulk_dvd_hist_nfields` | Number of fields present in the data record or dataset |
| 4 | 1 | 0.475 | `anl48_dvd_pay_dt` | Date on which the dividend payment is made to eligible shareholders |
| 3 | 3 | 0.513 | `anl48_bp12m_yld` | Projected dividend yield over the next 12 months |
| 3 | 2 | 0.515 | `anl48_bulk_bdvd_all_projections_par_amt` | Par amount, i.e., the face value of the security issued |
| 3 | 2 | 0.515 | `anl48_equity_td_xe_dvd` | Date on which the equity goes ex-dividend, i.e., after which buyers ar |
| 3 | 2 | 0.311 | `anl48_m21_hs_dvd` | Total gross dividend per share distributed over the last 12 months |
| 3 | 1 | 0.349 | `anl48_index_ibc` | Unique Bloomberg identifier assigned to the company used in this index |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl48_bdhad`(αC 42)；`anl48_bdvd_curr_dvd_health`(αC 42)；`anl48_bnepd`(αC 31)；`anl48_bedhgad`(αC 25)；`anl48_equity_bulk_eqy_dvd_hist_gross_ibc`(αC 21)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 年龄/时间戳 | — | — | — | — | cov≥0.5 11/18；类型 VECTOR |
| 标志/门控 | — | — | — | — | cov≥0.5 4/6；类型 VECTOR |
| 创新/修正事件 | — | — | — | — | cov≥0.5 1/1；类型 VECTOR |
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
