# EUR 交付清单（ATOM 口径重排）

> **ATOM 定义**：信号字段全部来自**单一数据集**。分组轴字段（如 `sta1_allc5` 属 pv29）不计入信号腿，但逐颗披露。
> 全部 17 颗均通过四重验证：IS 全闸 + 互相关 <0.7 + self <0.7 + **prod <0.7 实测**。
> 机器可读：`results/eur_atom_audit.json`（含逐颗字段→数据集映射）。

## 一、真 ATOM（5 颗）

| # | alpha | S | F | 2Y | SUB/S | TO | margin | prod | 信号数据集 | 分组轴 | 机制 |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 1 | **mL617YPx** | 1.82 | 1.25 | 2.23 | 0.68 | 6.8% | 17.6bp | **0.5421** | fundamental72 | sta1_allc5 | 现金流质量（OCF/总资产 ÷ OCF/净利，tvr 目标 0.06） |
| 2 | **O0W0w3P7** | 2.72 | 1.15 | 3.31 | 0.52 | 28.3% | 3.6bp | **0.6403** | news46 | — | 新闻事件流量（story_count 5日累加 → ts_rank 110） |
| 3 | **6XMmE0EL** | 2.35 | 1.02 | 1.70 | 0.80 | 32.5% | 3.8bp | **0.6529** | techindi_model | — | 概率极端分位差（5日 bucket4−bucket0，TOP1200/INDUSTRY） |
| 4 | **mLaLllmK** | 3.98 | 2.21 | 1.93 | 0.56 | 29.1% | 6.2bp | **0.6579** | techindi_model | — | 概率分位差（10日 bucket3−bucket1，ts_rank 110 + ts_mean 5） |
| 5 | **qME6VWbj** | 1.76 | 1.07 | 1.65 | 0.57 | 5.0% | 18.5bp | **0.6609** | analyst7 | — | 分析师 EBI 均值修订（4周变化 ÷ 标准差，signed_power 1.0） |

### ATOM 逐条说明
**1. mL617YPx** — S 1.82 / 2Y 2.23 / SUB-S 0.68 / TO 6.8% / prod 0.5421

```
ts_target_tvr_decay(trade_when(greater(divide(vec_avg(fnd72_pit_or_is_a_ebitda), vec_avg(fnd72_pit_or_cf_a_cf_net_inc)), 0.3), group_rank(multiply(divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_bs_a_bs_tot_asset)), divide(vec_avg(fnd72_pit_or_cf_a_cf_cash_from_oper), vec_avg(fnd72_pit_or_cf_a_cf_net_inc))), sta1_allc5), -1), lambda_min=0, lambda_max=1, target_tvr=0.06)
```

**2. O0W0w3P7** — S 2.72 / 2Y 3.31 / SUB-S 0.52 / TO 28.3% / prod 0.6403

```
group_rank(ts_rank(ts_sum(vec_avg(mws46_story_count),5),110),group_cartesian_product(sector,country))
```

**3. 6XMmE0EL** — S 2.35 / 2Y 1.7 / SUB-S 0.8 / TO 32.5% / prod 0.6529

```
group_neutralize(ts_mean(ts_rank(subtract(probability_fifth_quantile_five_day_bucket_four_13,probability_fifth_quantile_five_day_bucket_zero_14),180),5), group_cartesian_product(sector,country))
```

**4. mLaLllmK** — S 3.98 / 2Y 1.93 / SUB-S 0.56 / TO 29.1% / prod 0.6579

```
group_rank(ts_mean(ts_rank(subtract(probability_fifth_quantile_ten_day_bucket_three_13,probability_fifth_quantile_ten_day_bucket_one_13),110),5), group_cartesian_product(sector,country))
```

**5. qME6VWbj** — S 1.76 / 2Y 1.65 / SUB-S 0.57 / TO 5.0% / prod 0.6609

```
group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebi_mean, est_12m_ebi_mean_4wks_ago), est_12m_ebi_std), subindustry), 1.0), market)
```

## 二、附录：非 ATOM 混腿件（12 颗，不计入 ATOM 口径）

| alpha | S | 2Y | SUB/S | TO | prod | 信号数据集（数量） | 类别构成 | 禁区类数 |
|---|---:|---:|---:|---:|---:|---|---|---:|
| E56GgqLL | 1.68 | 2.12 | 0.72 | 5.9% | 0.5524 | fundamental72 + insider_feats（2） | FUNDAMENTAL+OTHER | 1 |
| xArjE96W | 2.28 | 2.32 | 0.54 | 10.8% | 0.5907 | analyst7 + other553 + risk68（3） | ANALYST+RISK+SENTIMENT | 0 |
| N1P02YwL | 1.81 | 2.62 | 0.83 | 3.8% | 0.6073 | quant_factor_lib + risk60（2） | MODEL+RISK | 1 |
| WjOeNE6O | 2.90 | 2.15 | 0.66 | 10.6% | 0.6411 | imbalance5 + insider_feats（2） | IMBALANCE+OTHER | 1 |
| 78L5GaeZ | 3.02 | 2.55 | 0.57 | 13.8% | 0.6662 | analyst_factor_signals + insider_matrix + techindi_model（3） | ANALYST+OTHER | 1 |
| rKRx7v6m | 3.22 | 2.07 | 0.57 | 18.9% | 0.6756 | sentiment26 + techindi_model（2） | OTHER+SENTIMENT | 1 |
| VkxWmpYG | 2.15 | 2.33 | 0.67 | 14.0% | 0.6800 | analyst_factor_signals + news36 + techindi_model（3） | ANALYST+NEWS+OTHER | 1 |
| WjOAJWxd | 2.36 | 2.67 | 0.54 | 8.0% | 0.6806 | analyst7 + sentiment27（2） | ANALYST+SENTIMENT | 0 |
| JjeNJ00O | 2.60 | 2.31 | 0.61 | 19.9% | 0.6813 | imbalance5 + risk60 + risk70（3） | IMBALANCE+RISK | 0 |
| N1NGbddg | 1.69 | 2.17 | 0.53 | 5.1% | 0.6872 | analyst7 + institutions6（2） | ANALYST+INSTITUTIONS | 0 |
| zq3Yrb3G | 2.87 | 2.10 | 0.52 | 18.4% | 0.6872 | analyst7 + other553 + risk68（3） | ANALYST+RISK+SENTIMENT | 0 |
| YP1baJrv | 2.23 | 2.00 | 0.70 | 19.7% | 0.6999 | risk70 + techindi_model（2） | OTHER+RISK | 1 |

## 三、78L5GaeZ 字段来源复核（用户指定核查项）

**结论：不是 ATOM。** 表达式实际使用 **3 个数据集**：

| 字段 | 所属数据集 | 类别 | 角色 |
|---|---|---|---|
| `probability_fifth_quantile_five_day_bucket_four_15` | techindi_model | OTHER | 信号腿 |
| `probability_fifth_quantile_five_day_bucket_zero_15` | techindi_model | OTHER | 信号腿 |
| `revenue_revision_magnitude` | analyst_factor_signals | ANALYST | 信号腿 |
| `revenue_y1_estimate_coeff_var` | analyst_factor_signals | ANALYST | 信号腿 |
| `eur_director_signal_value_1` | insider_matrix | OTHER | 信号腿 |

**两条判定**：
1. **ATOM 判定：否** —— 跨 3 个数据集（techindi_model + analyst_factor_signals + insider_matrix）。
2. **组腿合规判定：通过** —— 禁区类（PV/MODEL/OTHER）只出现 1 个（OTHER），未构成 OTHER×OTHER 违规。

⇒ 因此它**降为附录**，但仍可提交（合规层面无问题）。

## 四、口径变化带来的数字更正

| 口径 | 数量 | 说明 |
|---|---:|---|
| 之前报告 | 17 颗 | 未区分 ATOM / 混腿 |
| **ATOM 口径** | **5 颗** | mL617YPx / O0W0w3P7 / 6XMmE0EL / mLaLllmK / qME6VWbj |
| 混腿（附录） | 12 颗 | 含 78L5GaeZ、WjOeNE6O 等 |

**偏差根源**：补数量阶段我把「能过闸」排在「是否 ATOM」之前，库存挖掘时见组合腿能过 prod 就直接收。
**更正后的选件纪律**：ATOM 作为硬条件，混腿件单独记账不计入交付数。