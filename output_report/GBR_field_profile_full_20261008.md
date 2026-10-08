# GBR 字段画像 · 完整情况

> 区域：**GBR / D1 / TOP700 / EQUITY**　｜　画像表：`data/wqb.db :: field_profile_perf`（本区视图 `field_profile_gbr`）
> 构建命令：`$WQ_PY tools/fields/field_profile.py --build --region GBR`
> 快照时间：**2026-10-08**（含当日修复：写入端补 `backtest_results` + 回填 1253 行后重建）
> 口径：**n_tests 来自 `backtest_results`（只读该表）**；`coverage`/`field_type` 来自 `fields` 表

---

## 一、总览

| 指标 | 值 |
|---|---|
| 画像总行数 | **15,522** |
| 有字段目录的 GBR 字段 | 15,522（**未入画像 = 0**） |
| 平台存在性缺口 | **0**（`get_datafields` 逐集反查，平台有而本地无目录的 = 0） |
| 已测字段数（n_tests ≥ 1） | 285 |
| 累计测试次数 | ≈ 1,700+ |

### verdict 分布（九类）

| verdict | 判据 | 行数 | 占比 |
|---|---|---:|---:|
| `UNUSABLE` | coverage < 0.6 | **10,967** | 70.7% |
| `UNTESTED` | 过前两关且 n_tests = 0 | **2,578** | 16.6% |
| `AXIS_ONLY` | field_type = GROUP | **1,390** | 9.0% |
| `DEAD` | 已测 S < 1.10 | **465** | 3.0% |
| **`ALIVE`** | 单信号 S ≥ 1.58 | **49** | 0.3% |
| `WEAK` | 1.10 ≤ S < 1.58 | **34** | 0.2% |
| `DEAD_STATIC` | to_med < 0.03 | 28 | 0.2% |
| `DEAD_TURNOVER` | to_med > 0.70 | 7 | <0.1% |
| `DEAD_COUNT` | 名字含 num/count 且 2Y≥1.3 且 S≤0.7 | 4 | <0.1% |

> **可行动空间** = `ALIVE` 49（直接可做） + `WEAK` 34（优先深挖） = **83 个字段**（其中**非 MODEL 仅 39 个**）；
> 另有 `UNTESTED` **2,578** 个（**定义本身即含 coverage ≥ 0.6**；其中**非 MODEL 1,491 个**）。

---

## 二、verdict × category 矩阵

| category | UNUSABLE | UNTESTED | AXIS_ONLY | DEAD | **ALIVE** | WEAK | DEAD_STATIC | DEAD_TURNOVER | DEAD_COUNT | 合计 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MODEL | 4032 | 1087 | 0 | 169 | **29** | 15 | 3 | 0 | 0 | 5,335 |
| OTHER | 1926 | 350 | **1200** | 36 | 0 | 2 | 1 | 0 | 0 | 3,515 |
| ANALYST | 1736 | 387 | 0 | 85 | **17** | 13 | 1 | 0 | 0 | 2,239 |
| PV | 1412 | 511 | 190 | 48 | **3** | 0 | 0 | 1 | 0 | 2,165 |
| FUNDAMENTAL | 1153 | 40 | 0 | 27 | 0 | 0 | 18 | 0 | 0 | 1,238 |
| NEWS | 279 | 180 | 0 | 25 | 0 | 1 | 0 | 6 | 0 | 491 |
| SENTIMENT | 258 | 5 | 0 | 12 | 0 | 1 | 0 | 0 | 0 | 276 |
| INSTITUTIONS | 37 | 3 | 0 | 16 | 0 | 2 | 4 | 0 | 4 | 66 |
| INSIDERS | 36 | 0 | 0 | 13 | 0 | 0 | 1 | 0 | 0 | 50 |
| RISK | 34 | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 40 |
| EARNINGS | 20 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 25 |
| SHORTINTEREST | 0 | 12 | 0 | 13 | 0 | 0 | 0 | 0 | 0 | 25 |
| OPTION | 14 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 22 |
| SOCIALMEDIA | 20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 |
| MACRO | 8 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 13 |
| IMBALANCE | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |

**读法**：
- **`ALIVE` 高度集中于 MODEL（29/49 = 59%）** —— 而 MODEL 塔已点亮 ⇒ 受「已点亮塔不作主数据集」锁定。
- **非 MODEL 的 ALIVE 仅 20 个**：ANALYST 17 / PV 3。
- **`AXIS_ONLY` 1,390 个几乎全在 OTHER(1200) 与 PV(190)** —— 这些是 GROUP 字段，**只能当分组轴，不进信号白名单**。
- `FUNDAMENTAL` 有 18 个 `DEAD_STATIC`（to_med<0.03，静态属性 ⇒ 任何骨架都无用）。

---

## 三、字段类型分布

| field_type | 字段数 | 占比 | 说明 |
|---|---:|---:|---|
| MATRIX | 9,160 | 59.0% | 可直接套 `ts_*` / 截面算子 |
| **VECTOR** | **4,782** | 30.8% | **必须先 `vec_*` 聚合**（7 种：`avg/sum/min/max/stddev/range/count`） |
| GROUP | 1,470 | 9.5% | 分组轴（`AXIS_ONLY`），不可作信号 |
| SYMBOL | 110 | 0.7% | 非数值 |

> ⚠ **VECTOR 占比 30.8%**：这是本区最大的「操作纪律风险点」——裸用 `ts_*` 会被平台整批判 `does not support event inputs`。

---

## 四、ALIVE 全表（49 个，单信号 S ≥ 1.58）

| category | dataset | field | type | cov | n | to_med | **S** | 2Y | F |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| MODEL | model38 | star_val_region_rank | MATRIX | 0.00 | 3 | — | **2.61** | 2.06 | 2.31 |
| MODEL | model38 | region_relative_valuation_rank | MATRIX | 0.00 | 5 | — | 2.44 | 1.87 | 2.46 |
| MODEL | model38 | star_val_sector_rank | MATRIX | 0.00 | 3 | — | 2.41 | 2.05 | 2.14 |
| MODEL | model38 | star_val_piv_ratio | MATRIX | 0.00 | 1 | — | 2.15 | 2.22 | 1.52 |
| MODEL | analyst_earnings_ibes | five_day_total_return_dlr2 | MATRIX | 1.00 | **95** | 0.11 | **2.07** | 2.31 | 1.87 |
| MODEL | predictive_starmine | ep_yield_pct_smest_fy2_3 | MATRIX | 0.94 | 34 | 0.16 | 2.02 | 1.62 | 1.31 |
| MODEL | model38 | star_val_industry_rank | MATRIX | 0.00 | 2 | — | 2.01 | 2.00 | 1.69 |
| MODEL | model38 | star_val_ev_sales | MATRIX | 0.00 | 3 | — | 1.99 | 1.45 | 1.40 |
| MODEL | model38 | star_val_dividend_yield | MATRIX | 0.00 | 1 | — | 1.97 | 2.10 | 1.72 |
| MODEL | predictive_starmine | smest_price_ratio_fy1_revenue_4 | MATRIX | 0.93 | 1 | — | 1.97 | — | 1.25 |
| **ANALYST** | **analyst47** | **anl47_rawsentiment** | MATRIX | 0.64 | **60** | 0.17 | **1.96** | 1.84 | 0.97 |
| **ANALYST** | **analyst7** | **est_12m_pre_raisednum_4wks** | MATRIX | 1.00 | **75** | 0.11 | **1.96** | 2.05 | 1.31 |
| MODEL | model28 | mdl28_sm_structural_multiple_credit_structural_leverage | MATRIX | 0.59 | 27 | — | 1.94 | 1.85 | 1.37 |
| MODEL | predictive_starmine | forward_pe_mean_f12m_4 | MATRIX | 0.93 | 2 | — | 1.94 | 1.17 | 1.29 |
| MODEL | predictive_starmine | mean_estimate_price_ratio_f12m_earnings_5 | MATRIX | 0.93 | 2 | — | 1.94 | 1.17 | 1.29 |
| MODEL | model25 | value_momentum_industry_percentile | MATRIX | 1.00 | 1 | 0.05 | 1.91 | 1.36 | 1.61 |
| **ANALYST** | **analyst7** | **est_12m_pre_low** | MATRIX | 0.69 | **133** | 0.11 | **1.90** | **2.72** | 1.38 |
| MODEL | predictive_starmine | ep_yield_pct_smest_f12m | MATRIX | 0.94 | 52 | 0.13 | 1.88 | 2.09 | 1.27 |
| MODEL | model38 | ev_ebitda_relative_score | MATRIX | 0.00 | 4 | — | 1.87 | 2.08 | 1.63 |
| MODEL | model38 | star_val_pcf | MATRIX | 0.00 | 2 | — | 1.85 | 1.73 | 1.26 |
| **ANALYST** | **analyst7** | **est_12m_pre_raised_1wk** | MATRIX | 1.00 | 6 | 0.17 | **1.84** | **2.08** | **1.12** |
| **ANALYST** | **analyst7** | **est_12m_pre_raisednum_1mth** | MATRIX | 1.00 | 1 | 0.16 | **1.82** | 1.68 | **1.15** |
| ANALYST | analyst7 | est_12m_net_raisednum_4wks | MATRIX | 1.00 | 1 | — | 1.80 | 1.18 | 1.12 |
| MODEL | model28 | mdl28_sm_structural_credit_structural_pd_pct | MATRIX | 0.58 | 25 | — | 1.80 | 2.41 | 1.17 |
| MODEL | predictive_starmine | ep_yield_pct_smest_fy1_3 | MATRIX | 0.94 | 28 | 0.13 | 1.80 | 2.05 | 1.20 |
| ANALYST | analyst47 | anl47_indicator | MATRIX | 1.00 | 20 | 0.21 | 1.78 | 1.53 | 0.76 |
| MODEL | analyst_earnings_ibes | market_capitalization_dlr1 | MATRIX | 1.00 | 1 | — | 1.78 | 2.11 | 1.02 |
| ANALYST | analyst7 | est_12m_net_raised_1wk | MATRIX | 1.00 | 1 | — | 1.77 | 1.18 | 1.05 |
| MODEL | model28 | mdl28_sm_structural_credit_structural_asset_drift_pct | MATRIX | 0.58 | 23 | — | 1.77 | 2.20 | 1.21 |
| MODEL | predictive_starmine | smest_price_ratio_fy2_revenue_3 | MATRIX | 0.93 | 4 | — | 1.77 | — | 1.07 |
| **PV** | **pv47** | **pv47_spret** | MATRIX | 0.00 | **44** | 0.15 | **1.77** | **2.25** | 1.06 |
| ANALYST | analyst47 | anl47_totalrawsignal | MATRIX | 0.64 | 12 | 0.20 | 1.75 | 2.02 | 0.79 |
| ANALYST | analyst7 | est_12m_sal_raised_1wk | MATRIX | 1.00 | 1 | — | 1.74 | 1.43 | 0.98 |
| **PV** | **pv47** | **pv47_for_statssimple_only_spret** | MATRIX | 0.00 | 5 | 0.10 | **1.73** | **2.12** | **1.12** |
| ANALYST | analyst7 | est_12m_ebi_raisednum_4wks | MATRIX | 1.00 | 2 | — | 1.71 | 0.91 | 1.05 |
| MODEL | model53 | annualized_pd_2_year_jc7 | MATRIX | 0.80 | 75 | 0.11 | 1.70 | 2.14 | 1.04 |
| MODEL | predictive_starmine | smest_price_ratio_fy2_earnings_4 | MATRIX | 0.93 | 1 | — | 1.70 | — | 1.01 |
| **ANALYST** | **analyst9** | **anl9_s_numup** | **VECTOR** | 0.80 | 21 | — | **1.69** | 1.19 | **1.19** |
| MODEL | model109 | expected_dividend_yield | MATRIX | 0.48 | 11 | — | 1.69 | 2.10 | 1.07 |
| ANALYST | analyst7 | est_12m_ebt_raised_1wk | MATRIX | 1.00 | 2 | — | 1.68 | 1.88 | 0.97 |
| **ANALYST** | **analyst7** | **est_12m_pre_mean** | MATRIX | 0.69 | 37 | 0.12 | **1.66** | **2.15** | **1.20** |
| MODEL | analyst_earnings_ibes | highest_price_dlr1 | MATRIX | 1.00 | 5 | — | 1.65 | 2.22 | 0.92 |
| MODEL | predictive_starmine | smest_price_ratio_f12m_revenue_5 | MATRIX | 0.93 | 3 | — | 1.64 | — | 0.96 |
| **ANALYST** | analyst_factor_signals | revenue_y1_estimate_change_3mo | MATRIX | 0.87 | 14 | 0.16 | 1.62 | **0.76** | 1.02 |
| MODEL | model264 | mdl264_1l_m1d_1yf_spe_se | MATRIX | 0.97 | 1 | — | 1.62 | 1.70 | 1.10 |
| ANALYST | analyst_factor_signals | revenue_revision_magnitude | MATRIX | 0.87 | 9 | — | 1.61 | **0.99** | 1.01 |
| **PV** | **pattern_scores** | **breakaway_gap_up_mean_simscore_lookback60** | MATRIX | 1.00 | 1 | — | **1.61** | 1.64 | **1.13** |
| ANALYST | analyst7 | est_12m_net_low | MATRIX | 0.67 | 5 | — | 1.59 | 1.84 | 1.06 |
| MODEL | predictive_starmine | smest_price_ratio_fy1_ebitda_6 | MATRIX | 0.89 | 3 | — | 1.58 | — | 0.91 |

**★ 非 MODEL 的 ALIVE 20 个**（战役可用）：
- **ANALYST 17**：`analyst7` 11 个（修正家数族 `_4wks`/`_1wk`/`_1mth`、`pre_low`/`net_low`/`pre_mean` 等）｜`analyst47` 3 个（`rawsentiment`/`indicator`/`totalrawsignal`）｜`analyst9` 1 个（`anl9_s_numup`，VECTOR）｜`analyst_factor_signals` 2 个（2Y 塌）
- **PV 3**：`pv47` 2 个（`spret` / `for_statssimple_only_spret`）｜`pattern_scores` 1 个
- **注意**：`analyst47` 的 3 个 ALIVE **F 均 < 1.0**（0.76–0.97）⇒ IS 层实际卡 `LOW_FITNESS`；`analyst9`（2Y 1.19）与 `analyst_factor_signals`（2Y 0.76/0.99）卡 2Y。

---

## 五、WEAK 全表（34 个，1.10 ≤ S < 1.58）

| category | dataset | field | type | cov | n | to_med | S | 2Y | F |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| MODEL | analyst_earnings_ibes | closing_price_dlr1 | MATRIX | 1.00 | 1 | 0.13 | 1.57 | 1.86 | 0.84 |
| MODEL | analyst_earnings_ibes | lowest_price_dlr1 | MATRIX | 1.00 | 1 | 0.12 | 1.57 | 2.01 | 0.87 |
| MODEL | model28 | mdl28_..._pd_percent | MATRIX | 0.58 | 3 | 0.13 | 1.57 | — | 0.95 |
| MODEL | analyst_earnings_ibes | volume_weighted_avg_price_dlr1 | MATRIX | 0.99 | 2 | 0.10 | 1.56 | 1.81 | 0.87 |
| MODEL | model28 | mdl28_..._asset_drift_percent | MATRIX | 0.58 | 5 | 0.13 | 1.55 | — | 0.97 |
| ANALYST | analyst7 | est_12m_sal_raisednum_4wks | MATRIX | 1.00 | 1 | 0.08 | 1.54 | 0.82 | 0.91 |
| MODEL | model28 | mdl28_..._leverage | MATRIX | 0.59 | 2 | 0.08 | 1.54 | 0.04 | 0.95 |
| MODEL | predictive_starmine | eq_vr_dlra2_score | MATRIX | 0.67 | 2 | 0.04 | 1.51 | 1.70 | **1.07** |
| MODEL | model53 | annualized_pd_3_year_jc7 | MATRIX | 0.80 | 5 | 0.12 | 1.50 | 1.26 | 0.86 |
| MODEL | model53 | annualized_pd_1_year_jc7 | MATRIX | 0.80 | 6 | 0.14 | 1.47 | 1.86 | 0.83 |
| **ANALYST** | **analyst7** | **est_12m_pre_median** | MATRIX | 0.69 | 3 | 0.12 | **1.45** | **2.03** | 0.97 |
| OTHER | dl_riskfree_returns | probability_label1_2quantile_5day_ohlcv | MATRIX | 1.00 | 8 | 0.10 | 1.41 | 0.18 | 0.69 |
| MODEL | model250 | mdl250_maltahc_eq_score | MATRIX | 0.49 | 6 | 0.10 | 1.41 | 1.22 | 1.00 |
| ANALYST | analyst7 | est_12m_gps_raisednum_4wks | MATRIX | 1.00 | 1 | 0.08 | 1.40 | 1.01 | 0.77 |
| ANALYST | analyst47 | anl47_rawalphadecay | MATRIX | 0.64 | 8 | 0.17 | 1.39 | 0.17 | 0.60 |
| ANALYST | analyst7 | est_12m_ebt_mean | MATRIX | 0.68 | 4 | 0.12 | 1.38 | 1.34 | 0.78 |
| MODEL | predictive_starmine | smest_price_ratio_fy2_ebitda_6 | MATRIX | 0.90 | 2 | 0.09 | 1.36 | — | 0.73 |
| ANALYST | analyst7 | est_12m_dps_low | MATRIX | 0.69 | 3 | 0.11 | 1.35 | 0.71 | 0.79 |
| ANALYST | analyst7 | est_12m_ebt_raisednum_4wks | MATRIX | 1.00 | 4 | 0.08 | 1.35 | 0.79 | 0.79 |
| MODEL | model28 | mdl28_..._distance_to_default | MATRIX | 0.58 | 13 | 0.11 | 1.35 | 0.88 | 0.77 |
| ANALYST | analyst7 | est_12m_ebi_low | MATRIX | 0.67 | 5 | 0.12 | 1.34 | 1.77 | 0.82 |
| MODEL | model28 | mdl28_..._distance_to_default | MATRIX | 0.58 | 5 | 0.12 | 1.32 | 0.71 | 0.74 |
| ANALYST | analyst7 | est_12m_ebt_low | MATRIX | 0.68 | 5 | 0.11 | 1.31 | 1.52 | 0.78 |
| ANALYST | analyst_factor_signals | netprofit_y2_estimate_change_3mo | MATRIX | 0.85 | 2 | 0.16 | 1.27 | 1.18 | 0.68 |
| **INSTITUTIONS** | **fund_holdings_panel** | boundary_transaction_total | **VECTOR** | 0.93 | 4 | 0.09 | **1.26** | 1.38 | 0.32 |
| MODEL | predictive_starmine | smest_price_ratio_f12m_ebitda_4 | MATRIX | 0.90 | 1 | 0.12 | 1.26 | — | 0.65 |
| **INSTITUTIONS** | **fund_holdings_panel** | stable_boundary_trade_count_21d | **VECTOR** | 0.93 | 3 | **0.54** | **1.24** | 1.49 | 0.31 |
| ANALYST | analyst7 | est_12m_gps_low | MATRIX | 0.63 | 1 | 0.11 | 1.20 | 0.68 | 0.67 |
| ANALYST | analyst7 | rec_raisednum_4wks | MATRIX | 1.00 | 5 | 0.13 | 1.16 | 0.70 | 0.61 |
| MODEL | model53 | annualized_pd_5_year_jc7 | MATRIX | 0.80 | 3 | 0.12 | 1.15 | 1.48 | 0.57 |
| ANALYST | analyst7 | est_12m_cps_low | MATRIX | 0.61 | 3 | 0.11 | 1.14 | 0.44 | 0.61 |
| OTHER | other335 | oth335_combined_all_region_mind | MATRIX | 0.00 | 5 | 0.12 | 1.13 | 0.96 | 0.71 |
| **SENTIMENT** | **sentiment27** | **snl27_totaldomains** | **VECTOR** | 0.80 | 2 | 0.10 | **1.12** | **2.00** | 0.62 |
| **NEWS** | **news18** | **nws18_multiple_comp_ssc** | **VECTOR** | 0.97 | 13 | 0.09 | **1.10** | **1.65** | 0.49 |

**★ 非 MODEL 的 WEAK 9 个**：`analyst7` 6 个（`pre_median` S1.45/2Y2.03 最有希望）｜`analyst47` 1（`rawalphadecay`，2Y 0.17 死）｜`fund_holdings_panel` 2（VECTOR，to_med 0.09/0.54，F 0.31–0.32 极低）｜`other335` 1｜`sentiment27` 1（2Y 2.00 但 F 0.62）｜`news18` 1（2Y 1.65 但 F 0.49）。

---

## 六、UNTESTED 池（2,578 个；定义即 coverage ≥ 0.6，其中非 MODEL 1,491 个）— top 20 数据集

| category | dataset | 未测字段数 | 备注 |
|---|---|---:|---|
| PV | `pattern_scores` | **471** | K线形态相似度（前序已探 33 字段，最强 S1.61） |
| MODEL | `predictive_starmine` | 419 | **profile 写明 PROD 饱和族（starmine 四向）** |
| MODEL | `model264` | 359 | — |
| OTHER | `other455` | 300 | 图嵌入 PCA（前序已探弱，\|S\|≤0.48） |
| ANALYST | `analyst7` | **296** | 本区最强族；已测 78 字段，剩余多为 `est_12m_*` 同族变体 |
| MODEL | `model26` | 161 | — |
| MODEL | `model25` | 75 | — |
| NEWS | `news18` / `news17` / `news20` / `news50` | 56 / 45 / 39 / 32 | 多为 event_time/headline 等文本元数据（非信号） |
| ANALYST | `analyst9` | 44 | VECTOR（51 总，已测 7） |
| OTHER | `dl_riskfree_returns` | 43 | profile 记「实为分位数桶标签」，慎用 |
| PV | `pv29` | 40 | **实为 GROUP 聚类标签 ⇒ 只能当轴** |
| FUNDAMENTAL | `fundamental6` | 39 | aCnt 1947 极拥挤 |
| ANALYST | `analyst93` / `analyst_factor_signals` | 23 / 17 | — |
| SHORTINTEREST | `shortinterest3` | 12 | 本轮 `vec_*` 5 种聚合全弱 |

---

## 七、已测密度 top 15（画像可信度）

| dataset | 已测字段 | 累计测试 | 最强 S |
|---|---:|---:|---:|
| `analyst7` | **78** | **391** | 1.96 |
| `predictive_starmine` | 47 | 181 | 2.02 |
| `pattern_scores` | 33 | 42 | 1.61 |
| `model109` | 28 | 53 | 1.69 |
| `fundamental72` | 25 | 38 | 0.61 |
| `model264` | 21 | 32 | 1.62 |
| `intraday_pv_feats` | 17 | 23 | 0.94 |
| `model28` | 17 | 113 | 1.94 |
| `analyst_earnings_ibes` | 16 | **119** | 2.07 |
| `fund_holdings_panel` | 16 | 28 | 1.26 |
| `analyst_factor_signals` | 15 | 38 | 1.62 |
| `model53` | 15 | 114 | 1.70 |
| `dl_riskfree_returns` | 14 | 33 | 1.41 |
| `insider_agg_matrix` | 14 | 28 | 0.81 |
| `model38` | 14 | 31 | 2.61 |

> 密度集中：前 15 个数据集占了绝大部分已测字段；**其余 ~160 个数据集几乎零测试**。

---

## 八、⚠ 数据质量提示（务必先读）

1. **`coverage = 0.00` 的字段并非无覆盖**：`model38` / `pv47` / `pattern_scores` / `other335` 的字段画像 cov 全为 0.00，但平台实测可用（`pv47_spret` 已产出 S1.77/2Y2.25 的候选）。
   ⇒ **cov=0.00 是本区这些数据集的属性缺失，不是「不可用」信号**；判定可用性须用 `get_datafields`。
2. **`get_datasets` 不是存在性权威**：它只返回 149 条且**漏掉** `pv47`/`pattern_scores`/`fundamental6`/`pv30` 等。
   ⇒ **存在性只信 `get_datafields(dataset_id=...)`**（逐集反查）。
3. **画像只从 `backtest_results` 读实测**：`harvest --persist` 若漏写该表，画像会**系统性失真**（2026-10-08 曾因此把 ALIVE 少报 30 个：19 vs 49）。**写入端已修**。
4. **`ALIVE` 不等于「可提交」**：本区 20 个非 MODEL 的 ALIVE 中，`analyst47` 3 个卡 `LOW_FITNESS`（F 0.76–0.97）、`analyst9`/`analyst_factor_signals` 卡 2Y；`pv47` 2 个 prod 实测 0.81（>0.70）。
5. **真空数据集 5 个**：`news48` / `model219` / `model242` / `model50` / `other532`（`fields` 表 0 行）；其中 `news48`、`other532` 经平台反查返回 0 字段 ⇒ **真空而非缺口**。

---

## 九、机会评估（按「可行动性」排序）

| 优先 | 入口 | 依据 | 现实约束 |
|---|---|---|---|
| 1 | **ANALYST `analyst7` 修正家数族**（11 个 ALIVE，`_1wk`/`_1mth`/`_4wks` 三个时间尺度） | 本区最密、最强（S 1.59–1.96，F 1.05–1.38） | **prod 实测 0.76–0.86 ⇒ 已拥挤**（我方已提交 2 颗同族） |
| 2 | **PV `pv47`**（2 个 ALIVE，S1.73–1.77/2Y2.12–2.25） | 全闸候选可批量产生 | **prod 0.80–0.81 ⇒ 已拥挤**；且本区无 universe 杠杆 |
| 3 | `analyst47`（3 ALIVE） | S1.75–1.96 | F 0.76–0.97 卡 `LOW_FITNESS`，已穷尽降 TO 手段 |
| 4 | `analyst7/pre_median`（WEAK S1.45/**2Y2.03**） | 2Y 健康，S 缺口 0.13 | 值得 1 波 |
| 5 | 未测池：`pattern_scores` 471 / `analyst7` 296 / `analyst9` 44 | 白空间 | 前序探针显示多弱；盲探成本高 |
| — | MODEL（29 ALIVE + 48 颗全闸 alpha） | 本区最强 | **已点亮塔，受锁定项约束** |

**结论**：本区**可行动字段已基本探明**（285 已测字段 / 83 个活弱）；剩余 2,578 个未测字段中，除 `pattern_scores`(471)、`analyst7`(296)、`analyst9`(44) 外，多为文本元数据或已知弱族。
**真正的瓶颈不在画像覆盖，而在 prod 饱和**（两条活腿 `analyst7`、`pv47` 实测 prod 0.76–0.86）。


---

## 十、★ 修正：`DEAD_COUNT` 由「名字驱动」改为「description 驱动」（2026-10-08）

**用户指正**：「判断字段时通过读 description 而不是光看字段名」。

审计确认：本画像的 9 类 verdict 中，**只有 `DEAD_COUNT` 是名字驱动的** ——
旧实现 `COUNT_PAT = re.compile(r"(raisednum|lowerednum|surprisenum|_num|count)", re.I)` 直接对**字段名**跑正则。

### 审计出的三类错误（均有实例）

| 类型 | 实例 | description 揭示的真相 |
|---|---|---|
| **名字误匹配** | `acquisition_model.**count**ry_percentile_acquisition_likelihood` | 实为 **Percentile score**（`count` 无词边界命中 `country`） |
| | `model109.**accounts**_receivable_turnover_ratio` | 实为 turnover **ratio** |
| **语义混淆** | `analyst7.act_q_roe_surprisenum` | 描述 "Number of **estimates used for** surprise calculation" = **参与家数/覆盖度**，与 `raisednum/lowerednum`（**方向性**修正家数）不是同一机制 |
| | `insider_trx_matrix.mean_buy_transaction_count` | 描述 "**Average** per event" ⇒ 已是均值 |
| **漏杀** | `other47.oth47_organic_keywords` | 描述 "**Count of** unique keywords … **unit: count**"，S0.51/2Y1.61 ⇒ 完全符合形态，却因名字无 count/num 逃过 |
| **反例警示** | `model307.mdl307_sales_pct_gb` | 描述含 "expressed as a **number**"，但实为 **Fraction（比例）** ⇒ **描述出现 number ≠ 计数** |

### 修法（两次迭代；第一次我修错了）

1. ❌ **只加词边界** `count` ⇒ **过度修正**：`count_50bps`（`_` 属 `\w`）与 `_numup` 全部失配，**DEAD_COUNT 4→0 是假象**。
2. ✅ **最终：以 description 为准，名字只作注释** ——
   `COUNT_DESC_PAT`（"number of ｜ count of ｜ counts ｜ how many ｜ breadth ｜ …"）**且非** `COUNT_DESC_NEG`（ratio ｜ percentage ｜ percentile ｜ fraction ｜ average ｜ per event ｜ rank ｜ weighted ｜ …»）。
   实测该版比「名字+描述双确认」**多捕获 1 例漏杀**，且不引入假阳性。

**结果**：`DEAD_COUNT` 4 → **5**；`--all-regions` 重建通过（USA 亦为 4）⇒ 规则跨区可用。

### 对画像数字的影响

| verdict | 修正前 | 修正后 |
|---|---:|---:|
| DEAD | 465 | **464** |
| DEAD_COUNT | 4 | **5** |
| 其余（ALIVE 49 / WEAK 34 / UNTESTED 2578 / AXIS_ONLY 1390 / DEAD_STATIC 28 / DEAD_TURNOVER 7） | — | **不变** |

### 顺便的纪律（已写入 skill 的 `_field-profile-playbook.md §7`）

1. 类型/机制归类**必须读 `description`**；名字正则只能用于**缩小候选**，不得单独作判死依据。
2. **关键词出现 ≠ 语义成立**（描述里的 `number` 可能指「数值范围」）。
3. **反向也要查**（名字不像但描述是）⇒ 否则漏杀。

---

## 十一、★ 用 description 正向扫未测池：挖出「名字完全看不出」的新目标

非 MODEL 的 UNTESTED 1,491 个（有描述）分类：**疑似真信号 1,196 ｜ 中性 181 ｜ 元数据/非信号 114**。
其中名字完全无法揭示机制的高价值目标：

| 字段 | description 揭示 | 为何名字视角会漏 |
|---|---|---|
| **`news17.analyst_recommendation_change_score`**（cov 0.97，VECTOR） | "score representing **changes in analyst recommendations**, such as **upgrade or downgrade**" | 带 `news17_` 前缀 ⇒ 误以为只是新闻情绪；**实为评级变动分**（NEWS 塔 0/3，全新机制） |
| **`news104.nws104_prob_neg` / `_prob_ntr` / `_confidence`**（cov 0.97，VECTOR） | **正/负/中三分类概率 + 置信度** | 此前只探过 `nws20_*`，**完全没碰 news104** |
| **`analyst7.est_12m_bps_high_4wks_ago` / `_3mth_ago`** | "…made in the **past 3 months / past 4 weeks**" | 判为「同族变体」；描述揭示是 **vintage 快照** ⇒ 可做**长周期修正** |
| `institutions6.aggregate_equity_value_all_owners`（cov 1.00） | 机构持股聚合市值 | 此前只看 `fund_holdings_panel` |

### Wave 18 实测（标准水平型骨架）—— 全弱

| 目标 | S | 2Y |
|---|---:|---:|
| `analyst_recommendation_change_score` | 0.05 | −0.23 |
| `nws104_prob_neg` / `_prob_ntr` / `_confidence` | 0.06 / −0.39 / −0.12 | 0.98 / −1.12 / −0.85 |
| `est_12m_bps_low` | −0.26 | −0.52 |
| `divide(est_12m_bps_high, _4wks_ago)` | −0.00 | 0.25 |
| `aggregate_equity_value_all_owners` | 0.03 | **1.74** |
| `ts_delta(est_12m_bps_low, 66)` | −0.04 | 0.53 |

**★ 判读（不要把负结果误读为「描述方法无效」）**：
- **描述方法的有效性已由「修正 DEAD_COUNT 三类错误 + 挖出名字看不到的字段」证明**；Wave18 的负结果只说明**这些字段配「水平型 group_rank 骨架」无信号**。
- 存在明显的**骨架-量类型错配**：
  · `analyst_recommendation_change_score` 是**事件型**（升级/降级）⇒ 应用**变化型**（`ts_delta` / `ts_rank`），不是水平型；
  · 两个水平相除 ≈ 1 ⇒ **比值近似常量**（实测 S = −0.00）；vintage 用法应是**差值**或**分位**，不是 `divide`；
  · `aggregate_equity_value_all_owners` **2Y 1.74 健康、S 弱** ⇒ 与 `oth47_organic_traffic` 同型，值得换量纲再试。
- **⇒ 建议下一步**：对这 3 类「骨架错配/待换量纲」目标再发一波（变化型 / 分位型骨架）。
