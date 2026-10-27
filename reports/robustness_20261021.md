# 稳健性审计报告 · 2026-10-21

> 判定口径：`brain-alpha-robustness` Phase B（归因）+ Phase C（反过拟合闸）。
> 平台 RA 权威口径 = `ra.failed_ra_count == 0` 且 `checks.fail == []`。
> 阈值 = `PLATFORM_CHECK_LINES`（LOW_SHARPE 1.58 / LOW_FITNESS 1.0 / LOW_2Y_SHARPE 1.58）
> 与 EUR 比率闸 LOW_SUB_UNIVERSE_SHARPE = 0.53 × S。

---

## rKd5lAo8（EUR / fundamental72 / group_zscore @ industry）

**判定：CONDITIONAL**（failed_checks = 空 ⇒ 非 REJECT，可进提交前流程）

### Phase B 归因读数

| 项 | 值 | 来源 |
|---|---|---|
| 表达式 | `ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.06)` | `get_alpha_details` |
| 设置 | EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON | wave301 spec |
| Sharpe | **1.64** | 平台 IS |
| Fitness | **1.14** | 平台 IS（恒等式核对：1.64 × √(0.0603/0.125) = 1.139 ✔） |
| Returns | 0.0603 | 平台 IS |
| Turnover | 0.0685 | 平台 IS |
| Margin | 0.001762（**17.62 bp**） | 平台 IS |
| two_year_sharpe | **1.78** | 平台 IS |
| sub_universe_sharpe | 1.07（比 0.6524 vs 限 0.53×S = 0.8692 ⇒ **PASS**） | 平台 IS + EUR 比率闸 |
| robust_universe_sharpe | 1.12 | 平台 IS |
| investability_sharpe / fitness | 1.52 / 1.02 | 平台 IS |
| risk_neutralized_sharpe | 1.07 | 平台 IS |
| 塔位 | EUR / D1 / FUNDAMENTAL，multiplier 1.1；`pyramid_short = fundamental` | `get_alpha_details` |
| **prod 相关性** | **0.6747**（`passes_check=true`，直方图 [0.6,0.7) 仅 33、[0.7,0.8) **0**） | `check_correlation` |
| **self 相关性** | **0.5054**（最高 = JjQmx9nm；池 6 / OS 池 8） | `check_correlation` |
| RA 硬闸 | `failed_ra_count = 0`，`ra_failed = false`，`checks.fail = []` | 平台 |
| RA PASS 明细 | LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / LOW_ROBUST_UNIVERSE_SHARPE / LOW_2Y_SHARPE / MATCHES_PYRAMID | 平台 |
| RA WARNING | CLUSTER_TEST 0.97（限 1.58，不触发） | 平台 |
| 提交层 PENDING | SELF_CORRELATION / DATA_DIVERSITY / PROD_CORRELATION / REGULAR_SUBMISSION（后两项已由本次实测关闭） | 平台 |

### 逐年 Sharpe（`get_alpha_yearly_stats`，IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.09 | 1.86 | 1.31 | **0.05** | 2.15 | 2.74 | **−0.13** | 2.70 | 1.04 | 2.84 |
| Fitness | 1.57 | 1.27 | 0.76 | 0.01 | 1.63 | 2.24 | −0.03 | 2.56 | 0.68 | 2.68 |
| Returns | .0702 | .0583 | .0417 | .0014 | .0716 | .0832 | −.0054 | .1123 | .0537 | .1114 |
| Drawdown | .0196 | .0177 | .0210 | .0281 | .0178 | .0194 | .0435 | .0226 | .0320 | .0247 |
| Turnover | .0345 | .0819 | .0646 | .0534 | .0623 | .0676 | .0806 | .0805 | .0810 | .0796 |

### Phase C 反过拟合闸（Recent-3yr 口径：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| WebDataScope failed count | 0（PENDING 仅剩提交层相关性类，已实测关闭） | PASS |
| Recent-3yr 强度（主判定） | 平台 2Y **1.78** ≥ 1.58；近 3 年 2.70 / 1.04 / 2.84 全部 > 0.3 | PASS |
| Recent-3yr CV_Sharpe | **0.4565**（样本 std ddof=1；总体口径 0.3727） | **CONDITIONAL**（0.40–0.60 带） |
| 衰减比 | 2.84 / 1.64 = **1.732** ≥ 0.50 | PASS |
| 平年（仅近 3 年） | 0 | PASS |
| Recent-3yr max/min Sharpe 比 | 2.84 / 1.04 = **2.73** ≤ 3 | PASS |
| 全历史早年疲软 | 2017 平年（S 0.05）、2020 负年（S −0.13） | 软标记（**绝不据此 REJECT**） |
| Sub-universe | 平台 LOW_SUB_UNIVERSE_SHARPE = PASS；比率 0.6524 ≥ 0.53 | PASS |
| 算子数 | 9（REGULAR 无硬上限） | 软标记 |
| Margin @ turnover | 17.62 bp @ tvr 6.85% | PASS |
| Top-5 个股集中度 | `get_alpha_pnl` 只返回时间序列表（pnl / risk-neutralized-pnl / investability-constrained-pnl），**无逐股分解 ⇒ 不可测** | 不可得（不伪造、不计 FAIL） |
| 经济可解释性 | 行业中性下，现金转化能力（CFO/总资产）高、且 EBITDA 明显高于净利（盈利质量好）的公司组合长期跑赢 | PASS（一句话可写） |

### 结论与软标记

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记（提交描述须如实带一行）：① Recent-3yr CV_Sharpe 0.457 落在 0.40–0.60 条件带，源于 2022 弱年（S 1.04）；
  ② 全史含 2017 平年与 2020 负年（2020 疫情期波动）；③ Top-5 集中度不可测；④ 算子数 9。
- 下一步：CONDITIONAL 允许升级前最多 2 轮修复轮换（`brain-alpha-repair` / `wq-brain-alpha-optimization-v1`）后重跑本表；
  **提交仍需用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

### 归因要点（可复用的机制结论）

1. **归一化位是本族最强杠杆**：同轴同载荷同 tvr，只把 `group_rank` 换成 `group_zscore`
   ⇒ S 1.74→1.75、F 1.20→1.34、2Y 1.37→1.68、sub/S 0.632→0.652，四个闸门同时上台阶。
2. **换分组轴 = 换持仓组合 = 破 prod 密墙**：sector 轴 zscore 配方两次实测 prod = 0.7571（tvr0.06）/ 0.7553（tvr0.09）
   ⇒ D0-P 判 ≥0.75 = dead_end，且直方图 [0.7,0.8) 桶 n=16 / n=14 ⇒ **密墙**（非单颗钉子）；
   同族换成 **industry 轴**后 prod 落到 **0.6747**（[0.7,0.8) 桶 = 0）⇒ 假设成立。
3. **EUR LOW_SUB_UNIVERSE_SHARPE 是比率闸**（limit = 0.53 × S）⇒ 压 S 不能解，只能抬 sub/S 比；
   `group_zscore` 是目前唯一同时抬 S 与 sub/S 的算子。

---

## leM88RN5（wave302 / industry 轴）

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebit), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.06)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.59 ｜ F 1.09 ｜ 2Y 1.68 ｜ returns 0.0584 ｜ margin 17.25 bp ｜ tvr 0.0677 ｜ sub 1.06（比率 0.6667）
- **相关性**：prod **0.6701**（余量 0.0299）｜ self **0.5294** ｜ 平台 RA failed = 0

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.43 | 1.82 | 1.24 | **-0.05** | 2.47 | 2.82 | **-0.67** | 2.54 | 0.95 | 2.70 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.68, 'line': 1.58, 'years': {'2021': 2.54, '2022': 0.95, '2023': 2.7}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.4689 |
| decay_ratio | PASS | 1.6981 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | PASS | 2.8421 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.05, '2020': -0.67} |
| sub_universe_sharpe | PASS | {'sub': 1.06, 'S': 1.59, 'ratio': 0.6667, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 17.25, 'turnover': 0.0677} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBIT 明显高于现金流口径净利润（利润有现金支撑、盈利质量好）且经营现金流/总资产高的公司组合长期跑赢；ts_target_tvr_decay 把换手锚在 6%。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.469（0.40–0.60 带；总体口径 0.383）；驱动 = 2022 Sharpe 0.95 vs 2021 2.54 / 2023 2.70
- 全史疲软：2017 平年 S-0.05、2020 负年 S-0.67 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 算子数 6（调用点 9，闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6701 余量 0.0299（贴线）
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

---

## KPmOOwZx（wave302 / industry 轴）

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.09)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.61 ｜ F 1.10 ｜ 2Y 1.80 ｜ returns 0.0583 ｜ margin 14.15 bp ｜ tvr 0.0824 ｜ sub 1.05（比率 0.6522）
- **相关性**：prod **0.6624**（余量 0.0376）｜ self **0.5023** ｜ 平台 RA failed = 0

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.09 | 1.90 | 1.11 | **-0.03** | 2.05 | 2.66 | **-0.14** | 2.69 | 0.94 | 2.99 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.8, 'line': 1.58, 'years': {'2021': 2.69, '2022': 0.94, '2023': 2.99}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.5017 |
| decay_ratio | PASS | 1.8571 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | CONDITIONAL | 3.1809 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.03, '2020': -0.14} |
| sub_universe_sharpe | PASS | {'sub': 1.05, 'S': 1.61, 'ratio': 0.6522, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 14.15, 'turnover': 0.0824} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBITDA 明显高于现金流口径净利润（盈利质量好）且经营现金流/总资产高的公司组合长期跑赢；tvr 锚在 9% 以提高信号时效。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.502（0.40–0.60 带；总体口径 0.410）；驱动 = 2022 Sharpe 0.94 vs 2021 2.69 / 2023 2.99
- ★ Recent-3yr max/min Sharpe 比 3.18 落 3–5 条件带
- 全史疲软：2017 平年 S-0.03、2020 负年 S-0.14 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 算子数 6（调用点 9，闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6624 余量 0.0376（贴线）
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

---

## vROkA5nw（wave305 / industry 轴（EBIT>NI 闸，tvr 0.06））

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebit), vec_avg(fnd72_pit_or_is_a_net_income)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.06)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.58 ｜ F 1.08 ｜ 2Y 1.68 ｜ returns 0.0582 ｜ margin 17.18 bp ｜ tvr 0.0677 ｜ sub 1.07（比率 0.6772）
- **相关性**：prod **0.6663**（余量 0.0337）｜ self **0.5270** ｜ 平台 RA failed = 0

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.38 | 1.88 | 1.32 | **-0.09** | 2.21 | 2.80 | **-0.49** | 2.44 | 0.93 | 2.74 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.68, 'line': 1.58, 'years': {'2021': 2.44, '2022': 0.93, '2023': 2.74}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.4763 |
| decay_ratio | PASS | 1.7342 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | PASS | 2.9462 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.09, '2020': -0.49} |
| sub_universe_sharpe | PASS | {'sub': 1.07, 'S': 1.58, 'ratio': 0.6772, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 17.18, 'turnover': 0.0677} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBIT 明显高于净利润（利润有现金支撑、盈利质量好）且经营现金流/总资产高的公司组合长期跑赢；ts_target_tvr_decay 把换手锚在 6%。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.476（0.40–0.60 带；总体口径 0.389）；驱动 = 2022 Sharpe 0.93 vs 2021 2.44 / 2023 2.74
- 全史疲软：2017 平年 S-0.09、2020 负年 S-0.49 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 算子数 6（调用点 9，闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6663 余量 0.0337（贴线）
- self 0.5270 余量 0.1730（本地快算，口径 = OS 池排除 PPA）
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

---

## P0MZ5nrp（wave305 / industry 轴（EBIT>CFNI 闸，tvr 0.09））

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebit), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.09)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.58 ｜ F 1.07 ｜ 2Y 1.70 ｜ returns 0.0574 ｜ margin 14.34 bp ｜ tvr 0.0801 ｜ sub 1.05（比率 0.6646）
- **相关性**：prod **0.6653**（余量 0.0347）｜ self **0.5267** ｜ 平台 RA failed = 0

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.47 | 1.88 | 1.04 | **-0.11** | 2.40 | 2.78 | **-0.65** | 2.60 | 0.86 | 2.84 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.7, 'line': 1.58, 'years': {'2021': 2.6, '2022': 0.86, '2023': 2.84}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.5146 |
| decay_ratio | PASS | 1.7975 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | CONDITIONAL | 3.3023 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.11, '2020': -0.65} |
| sub_universe_sharpe | PASS | {'sub': 1.05, 'S': 1.58, 'ratio': 0.6646, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 14.34, 'turnover': 0.0801} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBIT 明显高于现金流口径净利润（利润有现金支撑、盈利质量好）且经营现金流/总资产高的公司组合长期跑赢；tvr 锚在 9% 以提高信号时效。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.515（0.40–0.60 带；总体口径 0.420）；驱动 = 2022 Sharpe 0.86 vs 2021 2.60 / 2023 2.84
- ★ Recent-3yr max/min Sharpe 比 3.30 落 3–5 条件带
- 全史疲软：2017 平年 S-0.11、2020 负年 S-0.65 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 算子数 6（调用点 9，闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6653 余量 0.0347（贴线）
- self 0.5267 余量 0.1733（本地快算，口径 = OS 池排除 PPA）
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

---

## pwvPanJx（wave305 / industry 轴（EBITDA>CFNI 闸，tvr 0.12））

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.12)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.60 ｜ F 1.09 ｜ 2Y 1.80 ｜ returns 0.0577 ｜ margin 13.29 bp ｜ tvr 0.0869 ｜ sub 1.04（比率 0.6500）
- **相关性**：prod **0.6595**（余量 0.0405）｜ self **0.5012** ｜ 平台 RA failed = 0

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.09 | 1.90 | 1.07 | **-0.04** | 2.00 | 2.63 | **-0.14** | 2.70 | 0.89 | 3.05 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.8, 'line': 1.58, 'years': {'2021': 2.7, '2022': 0.89, '2023': 3.05}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.5238 |
| decay_ratio | PASS | 1.9062 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | CONDITIONAL | 3.427 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.04, '2020': -0.14} |
| sub_universe_sharpe | PASS | {'sub': 1.04, 'S': 1.6, 'ratio': 0.65, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 13.29, 'turnover': 0.0869} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBITDA 明显高于现金流口径净利润（盈利质量好）且经营现金流/总资产高的公司组合长期跑赢；tvr 锚在 12% 以提高信号时效。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.524（0.40–0.60 带；总体口径 0.428）；驱动 = 2022 Sharpe 0.89 vs 2021 2.70 / 2023 3.05
- ★ Recent-3yr max/min Sharpe 比 3.43 落 3–5 条件带
- 全史疲软：2017 平年 S-0.04、2020 负年 S-0.14 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 算子数 6（调用点 9，闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6595 余量 0.0405（贴线）
- self 0.5012 余量 0.1988（本地快算，口径 = OS 池排除 PPA）
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

---

## akVLzLV1（wave306 / industry 轴（EBITDA>CFNI 闸，tvr 0.15））

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.15)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.60 ｜ F 1.09 ｜ 2Y 1.83 ｜ returns 0.0578 ｜ margin 13.07 bp ｜ tvr 0.0885 ｜ sub 1.04（比率 0.6500）
- **相关性**：prod **0.6585**（余量 0.0415）｜ self **0.5005** ｜ 平台 RA failed = 0

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.10 | 1.88 | 1.04 | **-0.04** | 2.00 | 2.61 | **-0.14** | 2.71 | 0.92 | 3.08 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.83, 'line': 1.58, 'years': {'2021': 2.71, '2022': 0.92, '2023': 3.08}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.5165 |
| decay_ratio | PASS | 1.925 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | CONDITIONAL | 3.3478 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.04, '2020': -0.14} |
| sub_universe_sharpe | PASS | {'sub': 1.04, 'S': 1.6, 'ratio': 0.65, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 13.07, 'turnover': 0.0885} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBITDA 明显高于现金流口径净利润（盈利质量好）且经营现金流/总资产高的公司组合长期跑赢；tvr 锚在 15% 以提高信号时效（换手略抬、prod 仍 < 0.7）。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.516（0.40–0.60 带；总体口径 0.422）；驱动 = 2022 Sharpe 0.92 vs 2021 2.71 / 2023 3.08
- ★ Recent-3yr max/min Sharpe 比 3.35 落 3–5 条件带
- 全史疲软：2017 平年 S-0.04、2020 负年 S-0.14 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 算子数 6（调用点 9，闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6585 余量 0.0415（贴线）
- self 0.5005 余量 0.1995（本地快算，口径 = OS 池排除 PPA）
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

---

## omoL2Od2（wave307 / industry 轴（EBITDA>CFNI 闸，tvr 0.18 — 实际饱和于 0.089））

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.18)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.60 ｜ F 1.09 ｜ 2Y 1.84 ｜ returns 0.0579 ｜ margin 12.98 bp ｜ tvr 0.0892 ｜ sub 1.04（比率 0.6500）
- **相关性**：prod **0.6582**（余量 0.0418）｜ self **0.5001** ｜ 平台 RA failed = 0

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.09 | 1.88 | 1.03 | **-0.03** | 2.01 | 2.61 | **-0.15** | 2.71 | 0.94 | 3.09 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.84, 'line': 1.58, 'years': {'2021': 2.71, '2022': 0.94, '2023': 3.09}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.5107 |
| decay_ratio | PASS | 1.9312 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | CONDITIONAL | 3.2872 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.03, '2020': -0.15} |
| sub_universe_sharpe | PASS | {'sub': 1.04, 'S': 1.6, 'ratio': 0.65, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 12.98, 'turnover': 0.0892} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBITDA 明显高于现金流口径净利润（利润有现金支撑、盈利质量好）且经营现金流/总资产高的公司组合长期跑赢；tvr 目标 18% 已饱和（实际 8.9%），信号时效与 0.15 档等价。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.511（0.40–0.60 带；总体口径 0.417）；驱动 = 2022 Sharpe 0.94 vs 2021 2.71 / 2023 3.09
- ★ Recent-3yr max/min Sharpe 比 3.29 落 3–5 条件带
- 全史疲软：2017 平年 S-0.03、2020 负年 S-0.15 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 调用点 9（闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6582 余量 0.0418（贴线）
- self 0.5001 余量 0.1999（本地快算，口径 = OS 池排除 PPA）
- ★ 同族注意：本颗与 wave301-307 的 CFO/TA 冠军族互相关 ~0.99，提交其中一颗会令同族其余颗的 self 超 0.7 ⇒ 每族实际只能提交 1 颗
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

---

## LL5NeJQ9（wave307 / industry 轴（**EBITDA>NI 新闸**，tvr 0.12））

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_is_a_net_income)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.12)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.59 ｜ F 1.08 ｜ 2Y 1.80 ｜ returns 0.0575 ｜ margin 13.22 bp ｜ tvr 0.0869 ｜ sub 1.04（比率 0.6541）
- **相关性**：prod **0.6599**（余量 0.0401）｜ self **0.5017** ｜ 平台 RA failed = 0

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.10 | 1.89 | 1.08 | **-0.03** | 1.88 | 2.66 | **-0.12** | 2.70 | 0.89 | 3.05 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.8, 'line': 1.58, 'years': {'2021': 2.7, '2022': 0.89, '2023': 3.05}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.5238 |
| decay_ratio | PASS | 1.9182 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | CONDITIONAL | 3.427 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.03, '2020': -0.12} |
| sub_universe_sharpe | PASS | {'sub': 1.04, 'S': 1.59, 'ratio': 0.6541, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 13.22, 'turnover': 0.0869} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBITDA 明显高于**净利润**（盈利质量好、非现金项目少）且经营现金流/总资产高的公司组合长期跑赢；该闸是本族新变体，2Y 1.80 优于同 tvr 的 EBIT>NI 闸（1.71）。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.524（0.40–0.60 带；总体口径 0.428）；驱动 = 2022 Sharpe 0.89 vs 2021 2.70 / 2023 3.05
- ★ Recent-3yr max/min Sharpe 比 3.43 落 3–5 条件带
- 全史疲软：2017 平年 S-0.03、2020 负年 S-0.12 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 调用点 9（闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6599 余量 0.0401（贴线）
- self 0.5017 余量 0.1983（本地快算，口径 = OS 池排除 PPA）
- ★ 同族注意：本颗与 wave301-307 的 CFO/TA 冠军族互相关 ~0.99，提交其中一颗会令同族其余颗的 self 超 0.7 ⇒ 每族实际只能提交 1 颗
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

---

## 1YjXvEMJ（wave307 / industry 轴，EBITDA>CFNI 闸，**tvr 0.21 档**）

- **表达式**：`ts_target_tvr_decay(trade_when(greater(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), group_zscore(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), industry), -1), lambda_min=0, lambda_max=1, target_tvr=0.21)`
- **设置**：EUR / TOPCS1600 / SUBINDUSTRY / delay 1 / decay 1 / maxTrade OFF / trunc 0.08 / nanHandling ON
- **平台指标**：S 1.60 ｜ F 1.09 ｜ 2Y 1.85 ｜ returns 0.0579 ｜ margin 12.91 bp ｜ tvr 0.0896 ｜ dd 0.0676 ｜ sub 1.04（比率 0.6500）｜ robust 1.15
- **相关性**：prod **0.6581**（余量 0.0419）｜ self **0.5000**（余量 0.2000）｜ 平台 RA failed = 0
- **来源**：本颗不是 wave313 的新概念，而是冠军族 tvr 阶梯的最高档（0.18 → 0.21 实际饱和于 0.0896）；由「EUR 全闸库存 + 无 prod 读数」筛查后实测 prod 捞回

### 逐年 Sharpe（IS）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| Sharpe | 2.10 | 1.87 | 1.02 | **-0.04** | 2.01 | 2.62 | **-0.16** | 2.70 | 0.95 | 3.10 |

### Phase C 反过拟合闸（Recent-3yr：2021 / 2022 / 2023）

| 检查项 | 读数 | 判定 |
|---|---|---|
| recent3yr_strength | PASS | {'two_year_sharpe': 1.85, 'line': 1.58, 'years': {'2021': 2.7, '2022': 0.95, '2023': 3.1}} |
| recent3yr_cv_sharpe | CONDITIONAL | 0.5082（样本口径）/ 0.4149（总体口径） |
| decay_ratio | PASS | 1.9375 |
| flat_years_recent3 | PASS | [] |
| recent3yr_max_min_ratio | CONDITIONAL | 3.2632 |
| full_history_weakness | SOFT_ONLY | {'2017': -0.04, '2020': -0.16} |
| sub_universe_sharpe | PASS | {'sub': 1.04, 'S': 1.6, 'ratio': 0.65, 'limit_ratio': 0.53} |
| operator_count | SOFT_ONLY | 9 |
| margin_at_turnover | PASS | {'margin_bp': 12.91, 'turnover': 0.0896} |
| top5_concentration | UNAVAILABLE | None |
| economic_explainability | PASS | 行业中性下，EBITDA 明显高于现金流口径净利润（利润有现金支撑、盈利质量好）且经营现金流/总资产高的公司组合长期跑赢；tvr 目标 21% 已饱和（实际 9.0%），信号时效与 0.15–0.18 档等价。 |

### 结论

- **verdict = CONDITIONAL**，`failed_checks = []` ⇒ 按 `submit_verdict` 口径**不构成 BLOCKED**。
- 软标记：
- ★ CONDITIONAL 来源：Recent-3yr CV_Sharpe 样本 0.508（0.40–0.60 带；总体口径 0.415）；驱动 = 2022 Sharpe 0.95 vs 2021 2.70 / 2023 3.10
- ★ Recent-3yr max/min Sharpe 比 3.26 落 3–5 条件带
- 全史疲软：2017 平年 S-0.04、2020 负年 S-0.16 ⇒ 仅软标记，绝不据此 REJECT
- Top-5 个股集中度不可测：get_alpha_pnl 仅返回时间序列 ⇒ 以平台 CONCENTRATED_WEIGHT ∈ pass 替代
- 调用点 9（闸1b-2 上限 <10）⇒ REGULAR 仅软标记
- prod 0.6581 余量 0.0419（贴线）
- self 0.5000 余量 0.2000（本地快算，口径 = OS 池排除 PPA；最相关 JjQmx9nm 0.5000）
- ★ 同族注意：本颗与 wave301-307 的 CFO/TA 冠军族互相关 ~0.99，提交其中一颗会令同族其余颗的 self 超 0.7 ⇒ 每族实际只能提交 1 颗；tvr 档阶梯**不构成新经济概念**
- 提交仍需**用户明确确认**（红线，`submit_verdict` 只能否决不能放行）。

# 稳健性归因报告 — 2026-10-21

## KPmmw3Oz（IND / D1 / FUNDAMENTAL）

**表达式**
```
group_rank(quantile(ts_rank(ts_delta(ts_backfill(fnd17_ebitda2ev, 22), 11), 300)), sector)
```
settings: region=IND universe=TOP500 delay=1 decay=20 neutralization=STATISTICAL truncation=0.15 nanHandling=OFF maxTrade=OFF

### 一、平台闸（B.0 硬前置）
| 项 | 值 |
|---|---|
| `ra.failed_ra_count` | **0** |
| `ra.failed_ppa_count` | **0** |
| `checks.fail` | `[]` |
| 硬闸 warning | 无（仅 MATCHES_THEMES / OSMOSIS_ALLOCATION） |
| `submit_verdict` | UNVERIFIABLE_404（死端点，预期），failed_ra=0 / failed_ppa=0 / sim_fails=[] |

### 二、核心指标
S 2.45 ｜ F 1.93 ｜ TO 0.170 ｜ returns 10.54% ｜ 2Y 2.12 ｜ sub 1.40 ｜ rob 1.03 ｜ margin 12.4 bp
prod 0.6342（<0.70 ✓）｜ self 0.4349（<0.70 ✓）｜ inv_S 1.28（保留率 52.2%）

### 三、逐年 Sharpe
| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| S | 2.08 | 2.01 | 1.62 | 1.06 | 4.99 | 4.39 | 2.54 | 1.71 | 2.94 | 1.21 |

### 四、Phase C 判据
| 检查项 | 结果 | 判定 |
|---|---|---|
| WebDataScope failed count | 0，无名单内 PENDING | **PASS** |
| Recent-3yr Sharpe（主判定） | 1.71 / 2.94 / 1.21，均值 1.95 ≥ 1.58，每年 >0.3 | **PASS** |
| Recent-3yr CV_Sharpe | 0.372 | **PASS**（<0.40） |
| 衰减比（2023/全期） | 1.21/2.45 = **0.494** | **CONDITIONAL**（0.30–0.50，差 0.006） |
| 平年（近3年） | 0 | **PASS** |
| Recent-3yr max/min | 2.43 | **PASS**（≤3） |
| Sub-universe | 平台 LOW_SUB_UNIVERSE_SHARPE = PASS（1.40） | **PASS** |
| 算子数 | 5（group_rank/quantile/ts_rank/ts_delta/ts_backfill） | PASS（阈值 >5 才软标记） |
| Margin @ turnover | 12.4 bp @ TO 0.170 | **PASS**（≥5 bp） |
| Top-5 个股集中度 | 平台未提供逐股分解 | 未测 |
| 经济可解释性 | EBITDA/EV 的 11 日变化：盈利收益率动量 —— 估值相对盈利改善的股票未来 1–2 周继续跑赢 | PASS（一句可写） |

### 五、软标记（不进 REJECT）
1. **衰减比 0.494**：2023 Sharpe 1.21 vs 全期 2.45；但近 3 年均值 1.95 仍强。
2. **全历史 CV 0.51**：2018/2019 两年 4.99/4.39 拉高均值（厂字形）。
3. **2017 = 1.06**：全历史最弱年，仍 >1。
4. **inv_S 保留率 52.2%**（用户级闸 ≥70% 不达标）；五条杠杆（backfill 22/66/252、ts_rank 300/375、decay 20/30、delta 5/11/22/66、f86 式多成分 add）全部无法改善 ⇒ 判为该字段族固有属性。

### 六、判定
**CONDITIONAL** —— 唯一触发项是衰减比 0.494（差 0.006）。平台闸全过、prod/self 全过、近 3 年强度与稳定性均达标。
待用户决策项：inv_S 保留率 52.2% 是否接受（IND 平台层不设此检查）。

---

## 9qEEwRnV（KPmmw3Oz 的修复版）— 判定 PASS

**修复动作**：在 `ts_rank(...,300)` 外层加一层 `ts_scale(...,300)`
```
group_rank(quantile(ts_scale(ts_rank(ts_delta(ts_backfill(fnd17_ebitda2ev, 22), 11), 300), 300)), sector)
```
settings 不变：IND / TOP500 / delay1 / decay20 / STATISTICAL / truncation 0.15

### 修复前后对比
| 指标 | KPmmw3Oz（原） | 9qEEwRnV（修复） | 变化 |
|---|---:|---:|---|
| 2023 Sharpe | 1.21 | **1.36** | +0.15 |
| 衰减比 | 0.494（COND） | **0.555（PASS）** | +0.061 |
| S / F | 2.45 / 1.93 | 2.45 / 1.92 | — |
| 2Y | 2.12 | 2.04 | −0.08（仍 ≥1.58） |
| rob | 1.03 | **1.05** | +0.02 |
| inv_S / 保留率 | 1.28 / 52.2% | **1.32 / 53.9%** | +1.7pp |
| prod / self | 0.6342 / 0.4349 | 0.6286 / 0.4350 | 均过 |
| RA failed | 0 | 0 | — |

### Phase C 逐项
| 检查项 | 结果 | 判定 |
|---|---|---|
| WebDataScope failed | 0，无名单内 PENDING | PASS |
| Recent-3yr Sharpe | 1.59 / 2.62 / 1.36，均值 1.86 ≥1.58，每年>0.3 | PASS |
| Recent-3yr CV | 0.295 | PASS |
| 衰减比 | 1.36/2.45 = **0.555** | **PASS** |
| 平年 / max-min | 0 / 1.93 | PASS |
| Sub-universe | 1.40 | PASS |
| 算子数 | 6 | PASS |
| Margin @ turnover | 12.2 bp @ 0.173 | PASS |
| 经济可解释性 | 盈利收益率动量的尺度归一版 | PASS |

**软标记**：全历史 CV 0.51（2018/2019 尖峰形）、2017 = 1.10、inv_S 保留率 53.9%（用户级闸 70% 未达）。

**判定 = PASS**（台账 `robustness_9qEEwRnV`）

---

## 分组轴全枚举结果（同批 w481，delta11 / decay20 / trunc0.15）
| 轴 | S | rob | 结论 |
|---|---:|---:|---|
| **sector** | 2.45 | **1.03** | 最优 |
| densify(sector) | 2.45 | 1.03 | 与 sector 完全等价 |
| **exchange** | 2.42 | 0.95 | 不优于 sector |
| densify(exchange) | 2.42 | 0.95 | 同上 |
| country | 2.41 | 0.96 | 同上 |
| group_zscore(exchange) | 2.26 | 0.86 | — |
| industry（同 settings） | 2.60 | 0.99 | S 最高但 rob 差 0.01 |
| subindustry（decay5） | 2.44 | 0.72 | rob 崩 |
⇒ **分组轴全集已扫：{market, sector, industry, subindustry, exchange, country} × {raw, densify}。sector 仍最优。**

---

## A1QQ0q8d（当前最优）— 判定 PASS

```
group_rank(quantile(ts_scale(ts_rank(ts_delta(ts_backfill(fnd17_ebitda2ev, 22), 11), 300), 252)), sector)
decay 15 | truncation 0.16 | STATISTICAL | IND/TOP500
```

| 闸/指标 | 值 | 说明 |
|---|---:|---|
| S / F | 2.59 / 1.98 | 闸 1.58 / 1.0 |
| TO | 0.190 | 闸 0.01–0.4 |
| 2Y | 2.18 | 闸 1.58 |
| sub | 1.49 | 闸 0.71 |
| rob | **1.10** | 闸 1.00 |
| CW / CLUSTER | pass | — |
| prod / self | **0.6612 / 0.4681** | 均 <0.70（prod 余量仅 0.039，偏薄） |
| inv_S / **IS/SH** | 1.44 / **55.6%** | 用户闸 70% 未达；社区带「一般」 |
| RA failed | **0** | 平台全过 |

**逐年**：2.81 / 2.16 / 1.58 / 1.02 / 5.07 / 4.68 / 2.45 / 1.85 / 2.78 / **1.49**
**Phase C**：近3年均值 2.04、CV 0.266、衰减比 **0.575**、max/min 1.87、平年 0、margin 11.7bp → **全 PASS**

---

## 保留率实测全表（平台 investability_sharpe / sharpe）
| alpha | 结构 | S | inv_S | **IS/SH** |
|---|---|---:|---:|---:|
| ZYmmxv9Q | delta5 / decay5 / trunc.15 | 3.36 | 1.50 | 44.6% |
| vROOd0zv | backfill66 / decay20 | 2.42 | 1.21 | 50.0% |
| wp99L6Jl | ts_rank375 / decay20 | 2.31 | 1.17 | 50.6% |
| P0MM16wK | decay30 | 2.19 | 1.12 | 51.1% |
| E5VVbXbJ | delta22 / decay5 | 2.39 | 1.24 | 51.9% |
| KPmmw3Oz | decay20 / trunc.15 | 2.45 | 1.28 | 52.2% |
| rKde6Q1m | delta66 / decay5 / trunc.08 | 1.41 | 0.75 | 53.2% |
| pwvvPQkv | decay15 / trunc.16 | 2.57 | 1.38 | 53.7% |
| 9qEEwRnV | decay20 + ts_scale300 | 2.45 | 1.32 | 53.9% |
| **A1QQ0q8d** | **decay15 + ts_scale252 / trunc.16** | **2.59** | **1.44** | **55.6%** |
| xA137wbb（f86 参照） | — | 2.12 | 1.57 | **74.1%** |

**规律**：保留率对 decay 呈单峰（decay5 44–53%｜**decay15 55.6%**｜decay20 52–54%｜decay30 51%），**decay 15 + trunc 0.16 是 IND f17 的保留率甜点**（与 HKG 论坛「decay 7 + trunc 0.16」结论方向一致）。

---

## 论坛经验（2026-10-21 检索）
1. **IS Sharpe 是 APAC 强制项**（ASI / JPN / HKG / TWN / KOR），**IND 不在此列** ⇒ 平台 `checks` 从不出现该闸，实测吻合。
2. **社区判读带**：<0.50 极差｜**0.50–0.65 一般**｜0.65–0.80 良好｜>0.80 优秀。我们 55.6% 落在「一般」段，非「极差」。Osmosis 帖的剔除线是「约束后掉 >60%」（即保留率 <40%）。
3. **limit 是动态的**（实测 1.65 / 1.92），必须读 `checks[].limit`，不能用 0.7×S 的固定公式。
4. **提 IS/SH 的正道是降 TV**（HKG：decay 5→7 使 TV −58%、IS/SH +23%）；但 **decay 已高时失效**（我们 decay 20→30 反而 0.539→0.511）。

---

## 提交记录 — A1QQ0q8d（用户 2026-10-21 明确授权）

| 项 | 值 |
|---|---|
| status / stage | **ACTIVE / OS**（os.startDate 2024-01-01） |
| dateSubmitted | **2026-10-21T11:55:30-04:00** |
| name / color | `IND_R_F17_EBITDAEV_01` / BLUE |
| tags | `CH_REG` / `SRC_fundamental17` / `EXPRFAM_EBITDAEV` |
| 提交时指标 | S 2.59｜F 1.98｜TO 0.1897｜2Y 2.18｜sub 1.49｜rob 1.10｜inv_S 1.44（IS/SH 55.6%）｜margin 11.7bp |
| 相关性（refresh 复核） | prod **0.6612**｜self **0.4693** |
| RA | failed_ra=0｜failed_ppa=0｜checks.fail=[] |
| 稳健性台账 | `robustness_A1QQ0q8d = PASS`（衰减比 0.575） |
| classifications | DATA_USAGE:SINGLE_DATA_SET｜POWER_POOL:POWER_POOL_ELIGIBLE｜**REGULAR:REGULAR**｜CLUSTER:CLUSTER |

**过程记录**
1. MCP 提交通道报 `fetch failed`，经核对 `name/tags/dateSubmitted` 全为空 ⇒ 实际未发出（不是"报错但已提交"）。
2. 改用本地唯一放行路径（`WQB_ALLOW_ALPHA_SUBMIT=1` + submit_alpha 节点），一次成功。
3. 平台提交时自动追加 `PowerPoolSelected` 标签；已按政策清除（PPA 通道不接受），现为 3 个纯 REGULAR 标签。
