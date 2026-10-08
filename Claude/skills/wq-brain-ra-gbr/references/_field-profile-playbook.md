# GBR 字段画像基线（Playbook 第 1 层落地快照）

> 跨区方法论主文：`docs/reference/field_profile_to_alpha_playbook.md`。
> 本文件只存 **GBR 的画像事实**（供选字段族时对照），机制/配方结论见 [`../mining_experience_by_category.md`](../../../../docs/reference/GBR/mining_experience_by_category.md)。
> 刷新：`$WQ_PY tools/fields/field_profile.py --build --region GBR`（画像随每波回归自动复利）。
> 快照时间：2026-10-08（**当日晚间修正版**）。
> ⚠ **2026-10-08 修正**：此前画像因 `harvest --persist` 未写 `backtest_results` 而**系统性失真**（写入端已修 + 回填 1253 行）。
> 修正后 **ALIVE 19 → 49、WEAK 9 → 34、DEAD 213 → 465、UNTESTED 2823 → 2578**。
> 阅读本文 §1/§2 时请以「修正后」列与 `$WQ_PY tools/fields/field_profile.py --query` 的实时输出为准。

## 0. 总览

```
GBR   1.55 万字段   285 已测   2578 未测   83 活弱(49 ALIVE + 34 WEAK)   465 判死
修正前(失真):  UNTESTED 2823 ｜ ALIVE 19 ｜ WEAK 9 ｜ DEAD 213
```

## 1. verdict 分布（按 category）

| category | UNUSABLE | UNTESTED | ALIVE | WEAK | DEAD | DEAD_STATIC | DEAD_TURNOVER | DEAD_COUNT | AXIS_ONLY |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ANALYST | 1742 | **474** | 3 | 1 | 17 | 2 | — | — | — |
| MODEL | 4071 | **1160** | **14** | 5 | 79 | 4 | 2 | — | — |
| PV | 1412 | **537** | 2 | — | 23 | — | 1 | — | 190 |
| OTHER | 1930 | **365** | — | 1 | 18 | 1 | — | — | 1200 |
| NEWS | 279 | **193** | — | — | 13 | — | 6 | — | — |
| FUNDAMENTAL | 1158 | **48** | — | — | 14 | 18 | — | — | — |
| INSTITUTIONS | 37 | **13** | — | 2 | 5 | 6 | — | 3 | — |
| SHORTINTEREST | — | **19** | — | — | 6 | — | — | — | — |
| SENTIMENT | 258 | **8** | — | — | 10 | — | — | — | — |
| RISK | 34 | **6** | — | — | — | — | — | — | — |
| EARNINGS / INSIDERS / MACRO / IMBALANCE / SOCIALMEDIA | — | — | — | — | 有 DEAD | — | — | — | — |

**读法**：`ALIVE` 集中在 MODEL（14）—— 而 MODEL 已点亮（本季度 4 颗）⇒ **按锁定项不作主数据集**。非 MODEL 的产出入口只有 **ANALYST（`analyst47`）/ PV（`pv47`）/ INSTITUTIONS（`fund_holdings_panel`）/ OTHER（`other335`）**，其余 category 只能走 `UNTESTED` 探针。

## 2. ALIVE 字段（19，单信号 S ≥ 1.58）

| dataset | field | type | cov | n | to_med | S_sg | 2Y_sg | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| model38 | region_relative_valuation_rank | MATRIX | 0.00 | 5 | 0.053 | **2.44** | 1.87 | 1.25 |
| model38 | star_val_region_rank | MATRIX | 0.00 | 1 | 0.123 | 2.37 | 2.06 | 1.19 |
| model38 | star_val_sector_rank | MATRIX | 0.00 | 1 | 0.129 | 2.31 | 1.93 | 1.13 |
| **analyst_earnings_ibes** | **five_day_total_return_dlr2** | MATRIX | **1.00** | **94** | 0.111 | **2.07** | **2.31** | 1.05 |
| predictive_starmine | ep_yield_pct_smest_fy2_3 | MATRIX | 0.94 | 11 | 0.158 | 2.02 | 1.51 | — |
| model38 | star_val_industry_rank | MATRIX | 0.00 | 2 | 0.129 | 2.01 | 2.00 | 0.99 |
| model38 | star_val_dividend_yield | MATRIX | 0.00 | 1 | 0.111 | 1.97 | 2.10 | — |
| **analyst47** | **anl47_rawsentiment** | MATRIX | 0.64 | **29** | 0.168 | **1.95** | **1.75** | **1.30** |
| predictive_starmine | forward_pe_mean_f12m_4 | MATRIX | 0.93 | 2 | 0.125 | 1.94 | 1.17 | 0.95 |
| predictive_starmine | mean_estimate_price_ratio_f12m_earnings_5 | MATRIX | 0.93 | 2 | 0.125 | 1.94 | 1.17 | 0.95 |
| model25 | value_momentum_industry_percentile | MATRIX | 1.00 | 1 | 0.054 | 1.91 | 1.36 | 0.82 |
| predictive_starmine | ep_yield_pct_smest_f12m | MATRIX | 0.94 | 46 | 0.130 | 1.88 | 1.89 | 1.23 |
| model38 | ev_ebitda_relative_score | MATRIX | 0.00 | 4 | — | 1.87 | 2.08 | 0.98 |
| **analyst47** | **anl47_indicator** | MATRIX | 1.00 | 4 | 0.214 | 1.78 | 1.41 | 1.07 |
| **analyst47** | **anl47_totalrawsignal** | MATRIX | 0.64 | 4 | 0.203 | 1.74 | 1.63 | 1.28 |
| **pv47** | **pv47_spret** | MATRIX | 0.00 | 16 | 0.147 | **1.69** | **2.07** | 1.20 |
| predictive_starmine | ep_yield_pct_smest_fy1_3 | MATRIX | 0.94 | 14 | 0.126 | 1.68 | 1.89 | 0.81 |
| model53 | annualized_pd_2_year_jc7 | MATRIX | 0.80 | 41 | 0.108 | 1.62 | 2.04 | 1.16 |
| **pv47** | **pv47_for_statssimple_only_spret** | MATRIX | 0.00 | 2 | 0.101 | 1.62 | 1.89 | — |

**⚠ 两处需复核**：① `model38` / `pv47` 的 `cov=0.00` 与高 S 并存 —— 覆盖率列疑似口径差异（真覆盖须以平台 `get_datafields` 复核，不要据 0.00 直接剔除）；② `predictive_starmine` 属 profile 写明的 **PROD 饱和族**（「starmine 四向」不生成新变体）⇒ 只作对照，不作首选。

## 3. WEAK 字段（9，1.10 ≤ S < 1.58）

| dataset | field | type | cov | n | to_med | S_sg | 2Y_sg |
|---|---|---|---:|---:|---:|---:|---:|
| model38 | star_val_ev_sales | MATRIX | 0.00 | 1 | 0.114 | 1.54 | 1.00 |
| predictive_starmine | eq_vr_dlra2_score | MATRIX | 0.67 | 2 | 0.037 | 1.51 | 1.70 |
| model250 | mdl250_maltahc_eq_score | MATRIX | 0.49 | 6 | 0.102 | 1.41 | 1.22 |
| analyst47 | anl47_rawalphadecay | MATRIX | 0.64 | 7 | 0.172 | 1.39 | 0.17 |
| model53 | annualized_pd_1_year_jc7 | MATRIX | 0.80 | 5 | 0.144 | 1.36 | 1.86 |
| **fund_holdings_panel** | **boundary_transaction_total** | **VECTOR** | 0.93 | 1 | 0.528 | 1.26 | 1.38 |
| **fund_holdings_panel** | **stable_boundary_trade_count_21d** | **VECTOR** | 0.93 | 2 | 0.539 | 1.24 | 1.49 |
| model53 | annualized_pd_3_year_jc7 | MATRIX | 0.80 | 3 | 0.084 | 1.16 | 1.26 |
| other335 | oth335_combined_all_region_mind | MATRIX | 0.00 | 5 | 0.116 | 1.13 | 0.96 |

**注**：`fund_holdings_panel` 两条是 **VECTOR** ⇒ 必须 `vec_*` 聚合（`vec_avg` 等），且 `to_med` 高达 0.53 —— 逼近 GBR `turnover_max 0.3` 的评审线（平台线 0.70），**开批前先降换手**。

## 4. 本区战役目标（按产出概率排序）

| 优先 | category / 数据集 | 依据 | 距点亮 |
|---|---|---|---|
| **1** | **ANALYST**（`analyst47` raw sentiment 族 + 474 UNTESTED） | 塔 **2/3**，`anl47_rawsentiment` ALIVE S1.95/2Y1.75/sub1.30；已有 `wpbJ2gm2` F 差 0.04 | **差 1 颗** |
| **2** | **PV**（`pv47`，537 UNTESTED + 190 AXIS_ONLY） | `pv47_spret` ALIVE S1.69/**2Y2.07**；PV 塔 0/3 | 差 3 |
| **3** | **INSTITUTIONS**（`fund_holdings_panel` + 13 UNTESTED） | 2 WEAK（VECTOR），塔 0/3；需先降换手 | 差 3 |
| 4 | **NEWS**（193 UNTESTED） | 池最大但 6 条 DEAD_TURNOVER 警告换手结构性偏高 | 差 3 |
| 5 | **OTHER**（`other335` + 365 UNTESTED / 1200 AXIS_ONLY） | 仅 1 WEAK（S1.13） | 差 3 |
| — | ~~MODEL~~ | **已点亮（4 颗）⇒ 锁定项不作主数据集**，仅可作复合从腿 | — |

## 5. 纪律（与主文一致）

1. **改持仓才是真降 prod**：换残差轴 / 字段 / 概念 / `trade_when` 分层；只改时序（`hump` / `decay` / 慢化 `ts_mean`）会**爆 self**。
2. **一条腿只产 1 颗**：同族提交一颗后，同持仓变体 prod/self 会被推爆（`gJZQZkZe` → `rKe5L9q3` 0.6737→0.9933）。
3. **框架与机制耦合，不可跨机制外推**：同框架对 estimate 族 +0.31、对 anl93 族 −0.38。
4. **画像只是「存在性证明」，不是「可复现证明」**：命中后必须本框架实测。
5. **高 S 陷阱**：`*_label*` / `*_bucket*` / `dl_riskfree_returns` 类分位桶标签不是信号，开批前核 `description`。


## 6. ★ 算子对账必须单列 `genius` 子集（2026-10-08 新增）

判「方向 / 算子穷尽」时，只对 `get_operators` 做差集**不够** —— API 的 `category` 只有 9 类（无 Genius），
`level` 字段恒为 `ALL`/`None`，**不暴露平台 UI 的 `base`/`genius` 分级**。

**权威表**：`docs/reference/operators_notes.md`（Category / Definition / Count / Scope / **Level**）。
**genius 级共 17 个**：`pasteurize`｜`ts_returns`｜`ts_kurtosis`｜`ts_ir`｜`ts_max_diff`｜
`ts_target_tvr_decay`｜`ts_target_tvr_hump`｜`vec_min`｜`vec_max`｜`vec_stddev`｜`vec_range`｜`vec_count`｜
`tail`｜`group_count`｜`group_std_dev`｜`group_sum`｜`group_cartesian_product`。

**★ VECTOR 聚合有 7 种**（`vec_min/max/stddev/range/count/avg/sum`）—— **勿只用 `vec_avg`/`vec_sum`**。

**GBR 实测（2026-10-08）**：唯一产出的 genius 算子是 **`ts_target_tvr_hump`**
（新候选 S1.62/F1.03/2Y1.89，`Failed RA=0`）；`vec_*` 另 5 种、`group_std_dev/count/sum`、`pasteurize`
在本区已试家族上均无产出；`group_cartesian_product` 语法可用但劣于 `sector`；
`tail` 语义为「区间内置 newval」⇒ 销毁信息，判为非合理尝试。
