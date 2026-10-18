# 审核点④：3a 复活补测清单（WEAK 47 字段 × 各 2 族缺口骨架）

> 2026-10-09 ｜ 前置审核：①口径✅ ②v2映射✅ ③两级闸门阈值✅
> **本清单等你批准后才发批**（这是唯一烧回测配额的阶段）

## 一、规模与预算

```
字段 47 个（WEAK：1.10≤S<1.58，全部有骨架缺口）
表达式 89 条（每字段 2 族「它没见过的」骨架；缺口不足 2 族的按纪律从面板补次优未见过族）
波数 12 波 ｜ 预计 ≈1 小时（每波派发+收割约 5 分钟）
两级闸门：12/12 波 波级✓ + 字段级✓（装箱按「族签名轮转贪心」，已实测）
```

## 二、族与数据集分布

**骨架族**：level_rank 16 ｜ quantile 16 ｜ delta 14 ｜ gn_first 13 ｜ ts_rank 12 ｜ av_diff 8 ｜ ts_zscore 5 ｜ decay_linear 4 ｜ double_window 1

**数据集**：techindi_model 24 ｜ analyst7 22 ｜ model28 8 ｜ analyst_earnings_ibes 6 ｜ predictive_starmine 6 ｜ model53 6 ｜ sentiment27 3 ｜ dl_riskfree_returns 2 ｜ model250 2 ｜ analyst47 2 ｜ analyst_factor_signals 2 ｜ fund_holdings_panel 2 ｜ other335 2 ｜ news18 2

## 三、完整配对清单（47 字段，按现有 best_s 降序）

| # | dataset.field | 语义 | 现 best_s | 现 2Y | 补测的 2 族（波） |
|---|---|---|---:|---:|---|
| 1 | `analyst_earnings_ibes.closing_price_dlr1` | level_amount | 1.57 | 1.86 | level_rank(w01) ts_rank(w01) |
| 2 | `analyst_earnings_ibes.lowest_price_dlr1` | level_amount | 1.57 | 2.01 | level_rank(w02) ts_rank(w02) |
| 3 | `model28.mdl28_sm_structural_multiple_credit_struct` | probability | 1.57 | - | av_diff(w08) level_rank(w08) |
| 4 | `analyst_earnings_ibes.volume_weighted_avg_price_dlr1` | level_amount | 1.56 | 1.81 | level_rank(w03) ts_rank(w03) |
| 5 | `model28.mdl28_sm_structural_multiple_credit_struct` | estimate_level | 1.55 | - | level_rank(w04) ts_rank(w04) |
| 6 | `analyst7.est_12m_sal_raisednum_4wks` | count | 1.54 | 0.82 | gn_first(w01) quantile(w01) |
| 7 | `model28.mdl28_sm_structural__credit_structural_lev` | ratio | 1.54 | 0.04 | av_diff(w04) quantile(w04) |
| 8 | `predictive_starmine.eq_vr_dlra2_score` | unknown | 1.51 | 1.70 | decay_linear(w06) level_rank(w06) |
| 9 | `model53.annualized_pd_3_year_jc7` | probability | 1.50 | 1.26 | level_rank(w05) ts_rank(w05) |
| 10 | `model53.annualized_pd_1_year_jc7` | probability | 1.47 | 1.86 | level_rank(w06) ts_rank(w06) |
| 11 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r5_q1` | unknown | 1.47 | 1.69 | decay_linear(w09) delta(w09) |
| 12 | `analyst7.est_12m_pre_median` | estimate_level | 1.45 | 2.03 | level_rank(w07) ts_rank(w07) |
| 13 | `dl_riskfree_returns.probability_label1_2quantile_5day_ohlcv` | probability | 1.41 | 0.18 | av_diff(w02) delta(w02) |
| 14 | `model250.mdl250_maltahc_eq_score` | score | 1.41 | 1.22 | quantile(w07) ts_zscore(w07) |
| 15 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r5_q2_p1` | probability | 1.41 | 1.80 | av_diff(w05) delta(w05) |
| 16 | `analyst7.est_12m_gps_raisednum_4wks` | count | 1.40 | 1.01 | gn_first(w02) quantile(w02) |
| 17 | `analyst47.anl47_rawalphadecay` | unknown | 1.39 | 0.17 | decay_linear(w09) level_rank(w09) |
| 18 | `analyst7.est_12m_ebt_mean` | estimate_level | 1.38 | 1.34 | level_rank(w08) ts_rank(w08) |
| 19 | `predictive_starmine.smest_price_ratio_fy2_ebitda_6` | ratio | 1.36 | - | av_diff(w06) quantile(w06) |
| 20 | `analyst7.est_12m_dps_low` | estimate_level | 1.35 | 0.71 | level_rank(w09) ts_rank(w09) |
| 21 | `analyst7.est_12m_ebt_raisednum_4wks` | count | 1.35 | 0.79 | gn_first(w03) quantile(w03) |
| 22 | `model28.mdl28_sm_structural_credit_structural_dist` | count | 1.35 | 0.88 | quantile(w01) |
| 23 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r10_q2` | percentile | 1.35 | 1.53 | delta(w01) gn_first(w01) |
| 24 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r1_q3` | percentile | 1.35 | 1.12 | delta(w02) gn_first(w02) |
| 25 | `analyst7.est_12m_ebi_low` | estimate_level | 1.34 | 1.77 | level_rank(w11) ts_zscore(w11) |
| 26 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r10_q5` | percentile | 1.33 | 1.75 | delta(w11) double_window(w11) |
| 27 | `model28.mdl28_sm_structural_multiple_credit_struct` | count | 1.32 | 0.71 | quantile(w03) |
| 28 | `analyst7.est_12m_ebt_low` | estimate_level | 1.31 | 1.52 | decay_linear(w12) ts_zscore(w12) |
| 29 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r10_q4` | percentile | 1.29 | 1.54 | delta(w03) gn_first(w03) |
| 30 | `analyst_factor_signals.netprofit_y2_estimate_change_3mo` | revision_change | 1.27 | 1.18 | delta(w12) ts_zscore(w12) |
| 31 | `sentiment27.snl27_totalcountrydomains` | count | 1.27 | 1.01 | quantile(w05) |
| 32 | `fund_holdings_panel.boundary_transaction_total` | count | 1.26 | 1.52 | quantile(w07) |
| 33 | `predictive_starmine.smest_price_ratio_f12m_ebitda_4` | ratio | 1.26 | - | av_diff(w09) quantile(w09) |
| 34 | `fund_holdings_panel.stable_boundary_trade_count_21d` | count | 1.24 | 1.49 | quantile(w10) |
| 35 | `techindi_model.tm_15_r1_r5_r10_rh_glb_d1_r10_q2_p1` | probability | 1.24 | 1.07 | av_diff(w07) delta(w07) |
| 36 | `techindi_model.tm_15_r1_r5_r10_rh_glb_d1_r1_q3` | percentile | 1.24 | 1.38 | delta(w04) gn_first(w04) |
| 37 | `analyst7.est_12m_gps_low` | estimate_level | 1.20 | 0.68 | level_rank(w10) ts_rank(w10) |
| 38 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r1_q2_p1` | probability | 1.20 | 1.80 | av_diff(w10) delta(w10) |
| 39 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r5_q2` | percentile | 1.19 | 1.42 | delta(w05) gn_first(w05) |
| 40 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r5_q3` | percentile | 1.19 | 2.08 | delta(w08) gn_first(w08) |
| 41 | `techindi_model.tm_16_r1_r5_r10_rh_glb_d1_r10_q3` | percentile | 1.17 | 2.04 | delta(w11) gn_first(w11) |
| 42 | `analyst7.rec_raisednum_4wks` | count | 1.16 | 0.70 | gn_first(w04) quantile(w04) |
| 43 | `model53.annualized_pd_5_year_jc7` | probability | 1.15 | 1.48 | level_rank(w11) ts_rank(w11) |
| 44 | `analyst7.est_12m_cps_low` | estimate_level | 1.14 | 0.44 | level_rank(w12) ts_rank(w12) |
| 45 | `other335.oth335_combined_all_region_mind` | score | 1.13 | 0.96 | quantile(w10) ts_zscore(w10) |
| 46 | `sentiment27.snl27_totaldomains` | count | 1.12 | 2.00 | gn_first(w06) quantile(w06) |
| 47 | `news18.nws18_multiple_comp_ssc` | sentiment | 1.10 | 1.65 | gn_first(w08) quantile(w08) |

## 四、判读规则（收割后统一执行）

- **复活**：任一新骨架 S≥1.58 ⇒ 该字段 WEAK→ALIVE，且证明「单骨架判死」是假死；
- **加固**：新骨架全 <1.10 ⇒ 该字段置信度升级（低置信→高置信 WEAK/DEAD）；
- **Phase 4 回归**：用本批 89 条重估「sem_type × 骨架族」矩阵，校正 SEM_PREFERRED v2 → v3。

**🔍 请你裁决：① 清单是否批准发批；② 是否调整优先级（如只看 best_s≥1.3 的前 20 个字段，成本减半至 6 波）。**