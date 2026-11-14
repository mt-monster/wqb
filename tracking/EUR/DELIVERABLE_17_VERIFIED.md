# EUR 交付：17 颗完全验证的 REGULAR Alpha（2026-11-12 22:30 定稿）

> 全部通过四重验证：IS 全闸 + 互相关 <0.7 + self <0.7 + **prod <0.7 实测**。
> 目标 20 颗，已确认 17 颗（16 REGULAR + 1 ACTIVE），缺口 3 颗原因见文末。
> 只挖不提交，提交权归用户。

## 逐颗明细（按 prod 从低到高 = 建议提交顺序）

| # | alpha | S | F | 2Y | SUB/S | TO | margin | prod | universe/中性化 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | mL617YPx | 1.82 | 1.25 | 2.23 | 0.68 | 6.8% | 17.6bp | 0.5421 | TOPCS1600/SUBINDUSTRY |
| 2 | E56GgqLL | 1.68 | 1.17 | 2.12 | 0.72 | 5.9% | 20.4bp | 0.5524 | TOPCS1600/SUBINDUSTRY |
| 3 | xArjE96W | 2.28 | 1.45 | 2.32 | 0.54 | 10.8% | 9.4bp | 0.5907 | TOP2500/FAST |
| 4 | N1P02YwL | 1.81 | 1.43 | 2.62 | 0.83 | 3.8% | 41.5bp | 0.6073 | TOPCS1600/INDUSTRY |
| 5 | O0W0w3P7 | 2.72 | 1.15 | 3.31 | 0.52 | 28.3% | 3.6bp | 0.6403 | TOP2500/MARKET |
| 6 | WjOeNE6O | 2.90 | 1.85 | 2.15 | 0.66 | 10.7% | 9.6bp | 0.6411 | TOP2500/FAST |
| 7 | 6XMmE0EL | 2.35 | 1.02 | 1.70 | 0.80 | 32.5% | 3.8bp | 0.6529 | TOP1200/INDUSTRY |
| 8 | mLaLllmK | 3.98 | 2.21 | 1.93 | 0.56 | 29.1% | 6.2bp | 0.6579 | TOP2500/MARKET |
| 9 | qME6VWbj | 1.76 | 1.07 | 1.65 | 0.57 | 5.0% | 18.5bp | 0.6609 | TOP2500/FAST |
| 10 | 78L5GaeZ | 3.02 | 2.35 | 2.55 | 0.57 | 13.8% | 12.1bp | 0.6662 | TOP2500/CROWDING |
| 11 | rKRx7v6m | 3.22 | 2.14 | 2.07 | 0.57 | 18.9% | 8.9bp | 0.6756 | TOP2500/CROWDING |
| 12 | VkxWmpYG | 2.15 | 1.49 | 2.33 | 0.67 | 14.0% | 9.5bp | 0.6800 | TOP2500/CROWDING |
| 13 | WjOAJWxd | 2.36 | 1.61 | 2.67 | 0.54 | 8.0% | 14.6bp | 0.6806 | TOP2500/FAST |
| 14 | JjeNJ00O | 2.60 | 1.35 | 2.31 | 0.61 | 19.9% | 5.4bp | 0.6813 | TOP2500/FAST |
| 15 | N1NGbddg | 1.69 | 1.05 | 2.17 | 0.53 | 5.1% | 18.7bp | 0.6872 | TOP2500/FAST |
| 16 | zq3Yrb3G | 2.87 | 1.65 | 2.10 | 0.52 | 18.4% | 6.6bp | 0.6872 | TOP2500/FAST |
| 17 | YP1baJrv | 2.23 | 1.19 | 2.00 | 0.70 | 19.7% | 5.7bp | 0.6999 | TOP1200/FAST |

## 表达式全文

### 1. mL617YPx（prod 0.5421，self 0.450）

    ts_target_tvr_decay(trade_when(greater(divide(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), 0.3), group_rank(multiply(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_cf_a_cf_net_inc))), sta1_allc5), -1), lambda_min=0, lambda_max=1, target_tvr=0.06)

### 2. E56GgqLL（prod 0.5524，self -1.000）

    ts_target_tvr_decay(quantile(signed_power(trade_when(multiply(greater(divide(vec_avg(fnd72_pit_or_is_a_ebitda),vec_avg(fnd72_pit_or_cf_a_cf_net_inc)),0.3),greater(group_rank(ts_mean(ts_backfill(buy_sell_ratio_all_250d_filled,22),5),subindustry),0.3)),group_rank(multiply(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper),vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)),divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper),vec_avg(fnd72_pit_or_cf_a_cf_net_inc))),bucket(rank(ts_backfill(buy_sell_ratio_all_250d_filled,22)),range="0,1,0.1")),-1),1.05),driver=gaussian),lambda_min=0,lambda_max=1,target_tvr=0.06)

### 3. xArjE96W（prod 0.5907，self -1.000）

    trade_when(less(group_rank(ts_mean(rsk68_beta,22),subindustry),0.9),vector_neut(group_neutralize(group_scale(signed_power(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks,est_12m_ebt_lowerednum_4wks),est_12m_ebt_num_4wks_ago),subindustry),1.5),industry),market),rank(ts_mean(vec_avg(oth553_est_estvalue),22))),-1)

### 4. N1P02YwL（prod 0.6073，self -1.000）

    subtract(hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)),hump=0.001), multiply(rank(ts_mean(vec_avg(rsk60_offer),5)), 0.5))

### 5. O0W0w3P7（prod 0.6403，self 0.098）

    group_rank(ts_rank(ts_sum(vec_avg(mws46_story_count),5),110),group_cartesian_product(sector,country))

### 6. WjOeNE6O（prod 0.6411，self 0.641）

    add(group_zscore(group_backfill(imb5_score, industry, 66), industry), group_zscore(group_backfill(buy_sell_ratio_all_250d_filled, industry, 66), industry))

### 7. 6XMmE0EL（prod 0.6529，self 0.249）

    group_neutralize(ts_mean(ts_rank(subtract(probability_fifth_quantile_five_day_bucket_four_13,probability_fifth_quantile_five_day_bucket_zero_14),180),5), group_cartesian_product(sector,country))

### 8. mLaLllmK（prod 0.6579，self 0.301）

    group_rank(ts_mean(ts_rank(subtract(probability_fifth_quantile_ten_day_bucket_three_13,probability_fifth_quantile_ten_day_bucket_one_13),110),5), group_cartesian_product(sector,country))

### 9. qME6VWbj（prod 0.6609，self -1.000）

    group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebi_mean, est_12m_ebi_mean_4wks_ago), est_12m_ebi_std), subindustry), 1.0), market)

### 10. 78L5GaeZ（prod 0.6662，self -1.000）

    group_rank(add(add(group_rank(subtract(probability_fifth_quantile_five_day_bucket_four_15,probability_fifth_quantile_five_day_bucket_zero_15),industry),group_rank(divide(revenue_revision_magnitude,ts_mean(revenue_y1_estimate_coeff_var,55)),industry)),group_rank(ts_backfill(eur_director_signal_value_1,66),industry)),industry)

### 11. rKRx7v6m（prod 0.6756，self 0.428）

    group_rank(add(group_rank(subtract(probability_fifth_quantile_ten_day_bucket_four_15,probability_fifth_quantile_ten_day_bucket_zero_15),industry),group_rank(ts_backfill(vec_avg(snt26_avgranking),66),industry)),industry)

### 12. VkxWmpYG（prod 0.6800，self -1.000）

    group_rank(add(add(group_rank(subtract(probability_fifth_quantile_ten_day_bucket_four_15,probability_fifth_quantile_ten_day_bucket_zero_15),industry),group_rank(divide(eps_revision_magnitude,ts_mean(eps_y1_estimate_coeff_var,55)),industry)),group_rank(ts_backfill(vec_avg(mws36_novelty),66),industry)),industry)

### 13. WjOAJWxd（prod 0.6806，self 0.645）

    vector_neut(group_neutralize(group_scale(signed_power(group_zscore(divide(subtract(est_12m_ebt_raisednum_4wks,est_12m_ebt_lowerednum_4wks),est_12m_ebt_num_4wks_ago),market),1.5),industry),market),group_rank(ts_mean(vec_avg(snt27_relpopularity1),66),subindustry))

### 14. JjeNJ00O（prod 0.6813，self -1.000）

    add(add(group_rank(imb5_score,industry),group_rank(multiply(-1,ts_zscore(vec_avg(rsk60_offer),252)),industry)),group_rank(multiply(-1,ts_mean(rsk70_mfm2_euetrd_shortint,22)),industry))

### 15. N1NGbddg（prod 0.6872，self 0.660）

    group_neutralize(add(signed_power(group_zscore(divide(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), est_12m_ebi_num_4wks_ago), subindustry), 2.1), subtract(group_rank(ts_zscore(ts_backfill(divide(subtract(count_institutional_buyers_security, count_institutional_sellers_security), count_institutional_holders_security), 120), 35), subindustry), 0.5)), market)

### 16. zq3Yrb3G（prod 0.6872，self -1.000）

    ts_target_tvr_decay(trade_when(less(group_rank(ts_mean(rsk68_beta,22),subindustry),0.6),vector_neut(group_neutralize(group_scale(signed_power(group_zscore(divide(est_12m_ebt_raisednum_4wks,add(est_12m_ebt_raisednum_4wks,est_12m_ebt_lowerednum_4wks)),subindustry),1.5),sector),market),rank(ts_mean(vec_avg(oth553_est_estvalue),66))),-1),target_tvr=0.30)

### 17. YP1baJrv（prod 0.6999，self -1.000）

    add(group_rank(ts_mean(vector_neut(vector_neut(tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q1,momentum_factor_exposure),rsk70_mfm2_euetrd_strevrsl),5),sector),group_rank(ts_mean(vector_neut(vector_neut(tm_17_r1_r5_r10_rh_ah3_glb_d1_r5_q1,momentum_factor_exposure),rsk70_mfm2_euetrd_strevrsl),22),sector))
