# analyst44 数据集分析文档（KOR / TOP600 / D1）

> 字段分类**一律以平台 `description` 为准**，字段名仅作索引，禁作语义依据。
> 画像源：`reference/field_profile/kor_analyst44_profile.json`（300 字段）
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
| 类型分布 | VECTOR 252 / MATRIX 48 |
| coverage ≥ 0.5 | 268 / 300 |
| 白空间（alphaCount ≤ 2） | 159 / 300 |
| 平均 coverage | 0.7258 |

## 三、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 覆盖 | 类型 | 白空间 |
|---|---|---:|---:|---|---:|
| **未分类** | — | 164 | 144 | VECTOR138 / MATRIX26 | 84 |
| **币种/元信息** | 元数据 | 41 | 37 | VECTOR34 / MATRIX7 | 22 |
| **创新/修正事件** | 修正行为 | 35 | 29 | VECTOR35 | 21 |
| **年龄/时间戳** | 新鲜度 | 23 | 23 | MATRIX13 / VECTOR10 | 11 |
| **已实现/实际值** | 事后真值 | 14 | 13 | VECTOR13 / MATRIX1 | 9 |
| **家数/估计者数量** | 关注广度 | 11 | 11 | VECTOR11 | 4 |
| **标志/门控** | 状态位 | 7 | 6 | VECTOR7 | 4 |
| **分散度/不确定度** | 观点分歧 | 4 | 4 | VECTOR4 | 4 |
| **共识均值** | 预期水平 | 1 | 1 | MATRIX1 | 0 |

### 与「按字段名分类」的差异

| 字段名前缀 | 条数 |
|---|---:|
| `anl_` | 220 |
| `eps_` | 19 |
| `bps_` | 18 |
| `annual_` | 12 |
| `ebitda_` | 8 |
| `consensus_` | 5 |
| `current_` | 5 |
| `dps_` | 5 |
| `anticipated_` | 2 |
| `ebit_` | 2 |
| `actual_` | 1 |
| `bbo_` | 1 |

> ⚠ 字段名分类**仅供参考**。凡名与 description 冲突的，一律以 description 为准；
> 差异条目须在下方逐条记录，因为差异往往指向被漏掉的信号结构。

### ★ 家数类的时间窗结构（字段名看不见，description 才揭示）

| 时间窗 | 条数 | 语义 | 代表字段 |
|---|---:|---|---|
| `four_weeks_prior` | 8 | — | `anl44_best_dps_4wk_dn` (cov 1.000, αC 4) |
| `unspecified` | 3 | — | `anl44_best_dps_numest` (cov 1.000, αC 2) |

## 四、类别 → 经济学骨架映射

### 币种/元信息 → 骨架：**—**

- **收益来源**：元数据，无收益来源
- **合规/工程注意**：不进信号；仅可作 group 参数
- **字段数**：41｜代表：`anl44_eps_best_crncy_iso`, `bps_estimate_currency_iso`, `ebitda_latest_annual_currency`

### 创新/修正事件 → 骨架：**修正幅度 / 创新性修正**

- **收益来源**：市场对创新性修正反应不足 ⇒ 后续漂移；修正方向持续性强
- **合规/工程注意**：两字段相减须显式声明跨集经济含义
- **字段数**：35｜代表：`anl44_second_en_ebit_lastactvalue`, `anl44_second_en_netprofit_lastactccy`, `anl44_second_en_netprofit_lastactvalue`

### 年龄/时间戳 → 骨架：**预测新鲜度**

- **收益来源**：估计越旧信息越衰减；快照 vs 共识的差分刻画更新速度
- **合规/工程注意**：时间戳类字段（YYYYMMDD）禁作信号
- **字段数**：23｜代表：`anl44_cfps_latest_ann_dt_qtrly`, `anl44_cfps_most_recent_period_end_dt`, `anl44_dps_best_cur_fiscal_semi_year_period`

### 已实现/实际值 → 骨架：**盈余惊喜 SUE（须与共识配对）**

- **收益来源**：实际 − 预期 = 惊喜，市场对惊喜反应不足
- **合规/工程注意**：配对相减属跨字段价差，须声明经济含义
- **字段数**：14｜代表：`anl44_second_en_pretaxprofit_lastactccy`, `anl44_second_en_dps_lastactccy`, `ebitda_latest_annual_value`

### 家数/估计者数量 → 骨架：**关注广度 / 覆盖变化**

- **收益来源**：分析师选择覆盖谁带信息，且覆盖存在羊群；水平含规模噪声，变化才干净
- **合规/工程注意**：VECTOR 必须 vec_avg；TO 低 ⇒ 禁扫窗口谱
- **字段数**：11｜代表：`anl44_best_dps_4wk_dn`, `anl44_best_dps_4wk_up`, `anl44_best_dps_numest`

### 标志/门控 → 骨架：**门控层**

- **收益来源**：不独立产出信号
- **合规/工程注意**：只作 if_else/trade_when 条件
- **字段数**：7｜代表：`bbo_ebitda_market_status`, `bps_market_status_flag`, `dps_market_session_status`

### 分散度/不确定度 → 骨架：**分歧度 → 不确定性溢价**

- **收益来源**：分析师意见分歧大 = 信息环境差，风险溢价高
- **合规/工程注意**：离散评分型禁 winsorize/signed_power（无连续尾部）
- **字段数**：4｜代表：`anl44_best_dps_stddev`, `anl44_best_eps_stddev`, `bps_estimate_standard_deviation`

### 共识均值 → 骨架：**预期水平 + 修正幅度**

- **收益来源**：共识的变化（非水平）是修正信号
- **合规/工程注意**：未缩放修正有效、缩放后失效（Jung 2019）
- **字段数**：1｜代表：`anl44_dps_best_crncy_iso`

### ⚠ 未分类 164 条（须逐条人工判读）

- `anl44_2_bps_coveredby` ｜ bps coveredby
- `anl44_2_bps_lastactvalue` ｜ Last known estimate value before this event, often the prior published value
- `anl44_2_bps_value` ｜ Current estimate value for Book Value Per Share from this event
- `anl44_2_cfps_coveredby` ｜ cfps coveredby
- `anl44_2_cfps_lastactvalue` ｜ Last known CFPS estimate value before the current event
- `anl44_2_cfps_value` ｜ Current analyst estimate value for Cash Flow Per Share
- `anl44_2_dps_coveredby` ｜ Identifier indicating which regime or policy covers the DPS estimate event
- `anl44_2_ebit_coveredby` ｜ String indicating regime or coverage regime; helps track which regime the event/estimate belongs to
- `anl44_2_ebit_lastactvalue` ｜ Most recent EBIT estimate before the current event, often prior published or final value
- `anl44_2_ebit_value` ｜ Current estimated value of EBIT
- `anl44_2_ebitda_value` ｜ Current value of the EBITDA estimate
- `anl44_2_ebitdaps_coveredby` ｜ ebitdaps coveredby
- `anl44_2_ebitdaps_lastactccy` ｜ ebitdaps lastactccy
- `anl44_2_ebitdaps_lastactvalue` ｜ ebitdaps lastactvalue
- `anl44_2_ebitdaps_prevalue` ｜ ebitdaps prevalue
- `anl44_2_ebitdaps_value` ｜ ebitdaps value
- `anl44_2_eps_coveredby` ｜ Regime or coverage identifier for the EPS event, helps regime linkage
- `anl44_2_eps_lastactvalue` ｜ Value of the most recent EPS estimate before the current event
- `anl44_2_eps_prevalue` ｜ Previous EPS estimate value before the current event
- `anl44_2_eps_value` ｜ Current EPS estimate value
- `anl44_2_epsr_coveredby` ｜ epsr coveredby
- `anl44_2_epsr_lastactvalue` ｜ Most recent EPSR estimate value before the current event
- `anl44_2_epsr_prevalue` ｜ Previous EPSR estimate value immediately before the current event
- `anl44_2_grossmargin_lastactvalue` ｜ Last known gross margin estimate value prior to the current event
- `anl44_2_grossmargin_value` ｜ Current gross margin estimate value for the event
- `anl44_2_nav_coveredby` ｜ nav coveredby
- `anl44_2_nav_lastactvalue` ｜ Value of NAV at the time of the most recent prior update before this event
- `anl44_2_nav_value` ｜ The current NAV estimate value
- `anl44_2_netprofit_lastactvalue` ｜ Value of the last known net profit estimate prior to the current event
- `anl44_2_netprofit_prevalue` ｜ Previous value of the net profit estimate prior to the current event
- … 另有 134 条

## 四·补、字段质量先验（alphaCount TOP30 看轴）

> 依据 `brain-alpha-research-field-quality` §1：**高使用量字段揭示该数据集最强的经济轴**。
> 按 `alphaCount` 降序（同分按 `userCount`）取前 ~30 名看轴。**此步不可跳**。

| αC | users | cov | 字段 | description 摘要 |
|---:|---:|---:|---|---|
| 96 | 62 | 0.758 | `anl44_second_en_eps_value` | Current EPS estimate value (numeric, float) |
| 50 | 7 | 0.752 | `bps_estimated_eps_next_year` | Bloomberg Estimates projected earnings per share for the next fiscal y |
| 45 | 22 | 1.000 | `eps_gaap_estimate_4wk_down_count` | Number of analysts who decreased their GAAP EPS estimates for the spec |
| 42 | 13 | 0.726 | `anl44_second_en_bps_prevalue` | Prior estimate value before the current revision |
| 37 | 12 | 0.752 | `anl44_eps_best_eeps_nxt_yr` | Consensus estimated EPS for the next fiscal year |
| 37 | 5 | 0.767 | `anl44_second_en_ebit_prevalue` | Previous EBIT estimate value before this update |
| 29 | 5 | 0.713 | `anl44_second_en_dps_prevalue` | Previous DPS estimate value prior to the current event |
| 28 | 11 | 0.752 | `anl44_dps_best_eeps_nxt_yr` | Estimated Earnings Per Share (EPS) for the next fiscal year as provide |
| 28 | 10 | 0.759 | `current_year_eps_estimate_2` | Consensus estimate for earnings per share for the current fiscal year. |
| 27 | 1 | 0.995 | `current_fiscal_year_period_code_2` | Current fiscal year end date for which BEst content is provided |
| 24 | 20 | 0.721 | `anl44_eps_analyst` | eps analyst |
| 24 | 4 | 0.995 | `anl44_dps_best_cur_fiscal_qtr_period` | Current fiscal quarter end date for which Bloomberg Earnings Estimates |
| 22 | 10 | 0.769 | `anl44_second_en_sales_prevalue` | Previous value for the sales estimate, before current event |
| 22 | 9 | 0.745 | `anl44_second_en_pretaxprofit_coveredby` | pretaxprofit coveredby |
| 22 | 8 | 0.702 | `anl44_second_en_ebitda_coveredby` | ebitda coveredby |
| 22 | 6 | 0.752 | `eps_estimate_next_fiscal_year` | Bloomberg Estimates projected earnings per share for the next fiscal y |
| 20 | 10 | 0.769 | `anl44_second_en_sales_coveredby` | sales coveredby |
| 19 | 3 | 0.838 | `annual_update_net_income_currency` | netprofit rep lastupdatedannccy |
| 18 | 10 | 0.759 | `anl44_dps_best_eeps_cur_yr` | Estimated Earnings Per Share (EPS) for the current fiscal year as prov |
| 18 | 3 | 0.621 | `anl44_second_en_cfps_prevalue` | Previous CFPS estimate value prior to current event |
| 18 | 1 | 0.995 | `bps_current_fiscal_year_period` | Current fiscal year end date or period for which the BEst BPS estimate |
| 17 | 4 | 0.759 | `eps_estimate_current_year_2` | Estimated EPS for the current fiscal year from Bloomberg Estimates |
| 17 | 2 | 0.995 | `bps_current_fiscal_quarter_period` | Current fiscal quarter end date used for Bloomberg Estimates content |
| 17 | 1 | 0.995 | `anl44_eps_best_cur_fiscal_year_period` | Current fiscal year end date for which Bloomberg Earnings Estimates co |
| 17 | 1 | 0.629 | `annual_update_ebitda_per_share_currency` | ebitdaps lastupdatedannccy |
| 16 | 15 | 1.000 | `anl44_best_eps_4wk_dn` | Number of analysts who lowered their EPS estimates in the last 4 weeks |
| 16 | 10 | 0.759 | `anl44_eps_best_eeps_cur_yr` | Estimated earnings per share for the current fiscal year from Bloomber |
| 16 | 9 | 0.758 | `anl44_second_en_eps_coveredby` | eps coveredby |
| 16 | 3 | 0.769 | `anl44_second_en_sales_lastactvalue` | Most recent known sales estimate value prior to the current event; typ |
| 15 | 11 | 0.726 | `anl44_second_en_bps_value` | Current estimate value |

**★ 轴判读**（头部字段指向的经济轴，供人工确认 / 修正）：

- 头部字段集中于：`anl44_second_en_eps_value`(αC 96)；`bps_estimated_eps_next_year`(αC 50)；`eps_gaap_estimate_4wk_down_count`(αC 45)；`anl44_second_en_bps_prevalue`(αC 42)；`anl44_eps_best_eeps_nxt_yr`(αC 37)
- ⇒ **开波前须先确认本集「最强轴」是否与拟挖方向一致**；
  若头部字段指向的轴与拟挖方向不同，**方向本身可能已偏**（见 analyst_consensus 打样实例）。

## 四·补二、字段画像五问与预处理决策

> 五问 = 测的是什么？怎么测的？时间维度（瞬时/累计/变化率）？为何存在？可靠性如何？

| 类 | 测什么 | 怎么测 | 时间维度 | 为何存在 | 可靠性 |
|---|---|---|---|---|---|
| 创新/修正事件 | — | — | — | — | cov≥0.5 29/35；类型 VECTOR |
| 年龄/时间戳 | — | — | — | — | cov≥0.5 23/23；类型 MATRIX / VECTOR |
| 已实现/实际值 | — | — | — | — | cov≥0.5 13/14；类型 MATRIX / VECTOR |
| 家数/估计者数量 | — | — | — | — | cov≥0.5 11/11；类型 VECTOR |
| 标志/门控 | — | — | — | — | cov≥0.5 6/7；类型 VECTOR |
| 分散度/不确定度 | — | — | — | — | cov≥0.5 4/4；类型 VECTOR |
| 共识均值 | — | — | — | — | cov≥0.5 1/1；类型 MATRIX |

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

---

## 八、prod 归因与「针对性降 prod」全表（2026-10-24，wave kor_w86_prod_attrib）

> 方法论：**降 prod 前必先做归因，禁结构试错**。归因第一轴 = `neutralization` 因子剥离谱
> （此前长期锁死 INDUSTRY 单档，属已知错误模式）。

### 8.1 归因轴一：neutralization 全扫（A 腿 = `vec_avg(eps_estimate_4wk_change)` 同壳）

统一壳层：`ts_target_tvr_decay(ts_decay_linear(signed_power(group_rank(winsorize(rank(ts_backfill(F,55)), std=0.26), sector), 4.0), 22), target_tvr=0.15)`

| neutralization | S | F | 2Y | TO | **prod** | Δprod vs INDUSTRY | alpha |
|---|---:|---:|---:|---:|---:|---:|---|
| INDUSTRY（长期基线） | **1.40** | 1.09 ✅ | 2.44 | 0.0800 | **0.8073** | — | `leMlwg2N` |
| REVERSION_AND_MOMENTUM | 1.08 | 0.77 | 1.83 | 0.075 | 0.7957 | −0.0116 | `1Yjd8weX` |
| CROWDING | 1.11 | 0.80 | 1.86 | 0.075 | 0.7700 | −0.0373 | `vROlEoXa` |
| **SUBINDUSTRY** | 1.11 | 0.78 | **2.68** | 0.0856 | **0.7179** | **−0.0894** | `E5VE9ZNR` |
| STATISTICAL | 0.85 | 0.45 | 2.25 | 0.1026 | （S 已废，未测） | — | `KPmpQdmz` |

**读法**：prod 单调随中性化粒度变细而下降（INDUSTRY → SUBINDUSTRY −0.089），
但 S 同向塌（1.40 → 1.11）。R&M / CROWDING 是「掉 0.3 S 换 0.01–0.04 prod」的亏本交易。
**⇒ prod 的来源是「行业层共同暴露」，不是动量/反转/拥挤因子暴露。**

### 8.2 归因轴二：加腿（跨信息通道）—— 结果与直觉相反

| 腿 | 定义 | 单独 S | 单独 F | 单独 2Y | 单独 prod | ρ 与 A 腿 |
|---|---|---:|---:|---:|---:|---:|
| **A（修正幅度）** | `vec_avg(eps_estimate_4wk_change)` | 1.40 | 1.09 | 2.44 | 0.8073 | 1.00 |
| **B（修正广度）** | `up − down` 家数净额 | 1.21 | 0.87 | 1.86 | 0.7912 | **0.7609** |
| **C（分歧度）** | `vec_avg(anl44_best_eps_stddev)` | 0.58 ❌ | 0.32 | 0.70 | — | — |
| **D（SUE，analyst16）** | `vec_avg(anl16_actsuescore)` | 1.09 | 0.82 | 1.36 | 0.7796 | **0.6515** |

| 合成 | S | F | 2Y | TO | **prod** | 观察 |
|---|---:|---:|---:|---:|---:|---|
| A + B（同集） | 1.36 | **1.19 ✅** | 2.08 | 0.052 | **0.8953** | ⚠ **比两条腿都高** |
| A + D（跨集） | 1.18 | 1.03 | 1.49 | 0.0557 | **0.8859** | ⚠ 同样升高 |

**★★ 决定性反直觉结论**：加腿不是稀释 prod，而是**「提纯」拥挤暴露** ——
A 0.807 / B 0.791 → 合成 0.895；A 0.807 / D 0.780 → 合成 0.886。
噪音相消使共同分量占比上升 ⇒ 与生产池的相关系数反而更高。
**⇒ 在 prod 这一关上，「加腿」是反向杠杆，与 F 闸的结论正好相反。**

### 8.3 归因轴三：跨数据集加腿会取消 Single Dataset 身份（硬约束）

| alpha | 数据集构成 | `failed_ra_checks` 实际下发 | 判定 |
|---|---|---|---|
| `P0Mb82xW` | 仅 analyst16 | `LOW_SHARPE`, `LOW_FITNESS`, **`LOW_2Y_SHARPE`** | ✅ 判为 Single Dataset |
| `6XAQJQWG` | analyst44 + analyst16 | `LOW_SHARPE`, **`IS_LADDER_SHARPE`(year 6)** | ❌ **NOT Single Dataset** |

⇒ 「同类别跨集并腿合法」这条此前记录的口径**被平台实测否证**：
跨集即触发 `IS_LADDER_SHARPE`、`LOW_2Y_SHARPE` 消失 ⇒ **点不亮任何塔**。
**任何用于点塔的 alpha 必须严格单数据集。**

### 8.4 闭式判决（三重，全部指向不可达）

**(1) prod–S 前沿拟合**（4 个可比单腿点）：
```
prod = 0.6116 + 0.1371 · S
  prod @ S=1.45  →  0.8104
  prod @ S=1.58  →  0.8283   （门槛 0.70，超 0.128）
  反解 prod=0.70 →  S = 0.645   （必须把 S 砍到 0.65 才可能过 prod）
```
⇒ **要过 prod 就必须放弃 S，要过 S 就必须放弃 prod。前沿斜率正向，剪刀差不可达。**

**(2) 加腿合成下界**（两条腿共享同一生产 alpha 分量 ⇒ ρ ≥ c_A·c_B）：
```
A+B  : ρ_min=0.6387 → prod 下界 0.8830   （实测 0.8953）
A+SUE: ρ_min=0.6294 → prod 下界 0.8791   （实测 0.8859）
```
⇒ 只要两条腿自身 prod 都 ≥0.78，**50:50 合成的 prod 数学上不可能低于 0.87**。

**(3) S 天花板**：本集历史最高 S = **1.45**（`wp9l3J51`）< 门槛 1.58。
即便 prod 归零，S 这一关也过不去。

### 8.5 终局判定

**analyst44 在 KOR/TOP600/D1 结构性不可产出。** 三重封死：
1. prod 与 S 前沿严格对立（闭式：prod@1.58 = 0.83）；
2. 加腿在 prod 轴上是反向杠杆（+0.08~0.09）；
3. 跨集加腿取消 Single Dataset 身份，点塔收益归零。

剩余可动轴（`std` 0.20–0.32 / 幂次 3.0–5.0 / `ts_rank` 替代 `rank`）**只能动 S 或 F，
不可能把 prod 从 0.83 压到 0.70 以下**，且沿前沿提 S 会同步抬高 prod。
⇒ **继续投入的期望值为负。本数据集判死，不再派批。**
