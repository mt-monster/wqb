# analyst_consensus · FA overlay 全族字段画像清单（2026-10-21 生成）

> 归档文件：本表由 `logs/_tmp_facat.py`（全量分页拉取 `GET /data-fields`，无 search）机械生成，读数部分来自同壳批次 1–2 实测。**别手改字段清单**，要更新就重跑生成器。

## §1 拉取口径与规模

| 项 | 值 |
|---|---|
| region / delay / universe | USA / 1 / TOP3000 |
| dataset | `analyst_consensus` |
| 平台声明字段总数 | **3424**（实拉 3424，`complete=true`） |
| `mean_forecast_actual_combined_*` 全族 | **147 条**（fxadj + 非 fxadj 成对） |
| 去重后不同经济指标 | **92** |
| 已回测指标 | **21** |
| 未测且 cov ≥ 0.70 | **50** |

⚠ 旧版「analyst_consensus 只有 300 字段」是 MCP `max_fields=300` 截断造成的假象；任何 `search=` 查询都被平台截在前 100 条，**不能用来建目录**。

## §2 已测 21 条的完整读数（同壳：`quantile(group_rank(hump(ts_backfill(winsorize(ts_zscore(ts_av_diff(vec_avg(<F>),63),252),std=4),252),hump=0.01),industry))`，decay 20 / RAM / TRUNC 0.08）

闸线：S ≥ 1.58 / F ≥ 1.0 / 2Y ≥ 1.58 / `LOW_SUB_UNIVERSE_SHARPE` ≥ **0.43 × S**。

| 指标 | alpha | S | F | TO% | 2Y | SUB | SUB/S | 结论 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `eps_annual12` (cov 0.95) | `e76xgXkM` | 1.89 | 1.12 | 3.29 | 1.76 | 1.05 | 0.56 | **全闸通过·已提交 ACTIVE**（prod 0.5532） |
| `netprofit_annual12` (cov 0.95) | `mLYYpKaW` | 1.82 | 1.05 | 3.40 | 1.20 | 0.51 | 0.28 | 近失（SUB 硬伤 + 2Y） |
| `eps_reported_quarterly16` (cov 0.91) | `gJWWAWKe` | 1.80 | 1.11 | 4.18 | 1.35 | 0.68 | 0.38 | 近失（SUB+2Y） |
| `netprofitreported_annual12` (cov 0.94) | `9qEEvE6d` | 1.54 | 0.83 | 3.51 | 1.43 | 0.39 | 0.25 | 近失但 SUB 硬伤 |
| `interest_expense_annual12` (cov 0.90) | `N1eewe5o` | 1.53 | 0.86 | 3.61 | 1.13 | 0.48 | 0.31 | 近失（融资成本通道，非盈利机制也起效） |
| `netprofit_reported_quarterly16` (cov 0.89) | `pwvvXvzq` | 1.52 | 0.87 | 4.37 | 1.16 | 0.65 | 0.43 | 近失（全项差 4%，SUB 差 0.01） |
| `total_assets_annual12` (cov 0.89) | `N1ee0KL8` | 1.47 | 0.78 | 3.45 | 0.84 | 0.71 | 0.48 | SUB 过；缺 S/F/2Y（2Y 最难） |
| `roe_annual12_tribes` (cov 0.86) | `zqrRjeLd` | 1.45 | 0.91 | 4.13 | 1.35 | 0.80 | 0.55 | **三项同时近失（S−0.13/F−0.09/2Y−0.23），最接近全闸** |
| `ebit_annual12_2` (cov 0.96) | `2rjjMGG6` | 1.16 | 0.56 | 4.83 | 1.21 | 0.76 | 0.66 | **SUB 比值全族最高**，缺 S/F/2Y |
| `gps2` (cov 0.97) | `vROO8YGa` | 1.06 | 0.50 | 5.07 | 1.88 | 0.55 | 0.52 | 死（S/F）；2Y 1.88 是亮点 |
| `revenue_annual12` (cov 0.98) | `akVElGGx` | 0.99 | 0.45 | 5.19 | -0.10 | 0.41 | 0.41 | 死（S/F/SUB/2Y 四项） |
| `nav_annual12` (cov 0.92) | `9qEEYGMx` | 0.97 | 0.44 | 5.10 | 1.48 | 0.13 | 0.13 | 死（SUB 结构性） |
| `net2` (cov 0.97) | `d5KKXK7E` | 0.97 | 0.44 | 4.95 | 0.71 | 0.35 | 0.36 | 死 |
| `eps_quarterly16` (cov 0.95) | `Vkdd9dq0` | 0.95 | 0.44 | 5.55 | 1.30 | 0.19 | 0.20 | 死（S/SUB） |
| `ebit_quarterly16_2` (cov 0.92) | `zqrrMrjX` | 0.94 | 0.45 | 5.89 | 1.12 | 0.40 | 0.43 | 死（S/F/2Y） |
| `bvps_annual12` (cov 0.83) | `rKdd3dr8` | 0.92 | 0.45 | 5.37 | 0.66 | 0.17 | 0.18 | 死（否证「每股即可」） |
| `cfo_annual12` (cov 0.80) | `9qEEYG89` | 0.90 | 0.48 | 3.96 | 0.86 | 0.48 | 0.53 | 死（S/F/2Y） |
| `reportednet_annual12_2` (cov 0.96) | `0mjMd5ak` | 0.80 | 0.33 | 4.89 | 1.39 | -0.02 | -0.03 | 死（SUB 为负） |
| `pretax_reported_annual12` (cov 0.94) | `GrggPQx0` | 0.66 | 0.25 | 5.00 | 0.45 | 0.02 | 0.03 | 死（SUB≈0） |
| `capex_annual12_2` (cov 0.83) | `MP00Ogez` | 0.64 | 0.29 | 4.94 | 0.99 | 0.38 | 0.59 | 死（S/F/2Y） |
| `dividend_annual12` (cov 0.86) | `YPxxrx2q` | 0.34 | 0.16 | 5.47 | 1.34 | 0.10 | 0.29 | 死（DD 42.9%） |

## §3 未测指标 × 经济通道（批次 5 候选池）

机制律（§8.1 / §8.2 实测）：活跃共性是 **earnings-based 兑现意外**，不是「每股」形式；`reported` 口径 > `adjusted`；年度 > 季度（仅在 adjusted 内成立）；顶线与慢存量（revenue / nav / bvps / dividend）是死区。

- **盈利兑现**：`eps_annual12_3`(cov 0.98, ac=0, 未测) · `epsreported_annual12`(cov 0.94, ac=2, 未测) · `eps_quarterly16_tribes`(cov 0.93, ac=0, 未测) · `ebt_annual12`(cov 0.88, ac=0, 未测) · `pretax_annual12`(cov 0.97, ac=1, 未测) · `pretax_annual12_2`(cov 0.94, ac=0, 未测) · `pretax_quarterly16`(cov 0.89, ac=0, 未测) · `ebitda_annual12`(cov 0.86, ac=1, 未测) · `ebit_quarterly16_tribes`(cov 0.90, ac=1, 未测) · `gps`(cov 0.97, ac=0, 未测) · `fullyreported`(cov 0.93, ac=1, 未测) · `gps_fq16`(cov 0.93, ac=0, 未测)
- **利润率/成本**：`grossmargin_annual12`(cov 0.76, ac=0, 未测) · `grossmargin_annual12_tribes`(cov 0.75, ac=0, 未测) · `operatingexpense_annual12`(cov 0.84, ac=0, 未测) · `interest_expense_annual12`(cov 0.90, ac=0, 已测) · `taxrate_annual12`(cov 0.86, ac=0, 未测) · `taxprovision_annual12_tribes`(cov 0.93, ac=1, 未测) · `depreciation_annual12`(cov 0.63, ac=1, 未测)
- **资本结构/稀释**：`sharesoutstanding_annual12`(cov 0.94, ac=0, 未测) · `netdebt_annual12`(cov 0.75, ac=0, 未测) · `netdebt_annual12_2`(cov 0.74, ac=1, 未测) · `totalliab_annual12_tribes`(cov 0.78, ac=0, 未测) · `cashflowfinancing_annual12`(cov 0.74, ac=0, 未测) · `cashflowinvesting_annual12`(cov 0.75, ac=0, 未测) · `currentassets_annual12`(cov 0.72, ac=0, 未测) · `currentliabilities_annual12`(cov 0.72, ac=0, 未测)
- **现金转化**：`cfps_annual12`(cov 0.73, ac=0, 未测) · `cfps_annual12_2`(cov 0.73, ac=1, 未测) · `fcf_annual12`(cov 0.79, ac=3, 未测) · `cfo_annual12`(cov 0.80, ac=3, 已测)
- **口径变体（低优先）**：`revenue_annual12_tribes`(cov 0.95, ac=1, 死区) · `revenue_quarterly16`(cov 0.95, ac=0, 死区) · `revenue_quarterly16_3`(cov 0.95, ac=0, 死区) · `nav_annual12_tribes`(cov 0.90, ac=0, 死区) · `bvps_annual12_tribes`(cov 0.81, ac=0, 死区) · `tangbookvalue_annual12_tribes`(cov 0.90, ac=1, 未测) · `dividend_annual12_2`(cov 0.86, ac=0, 死区) · `dps_annual12_3`(cov 0.85, ac=0, 死区) · `dps_quarterly16`(cov 0.60, ac=0, 死区) · `dps_quarterly16_2`(cov 0.63, ac=0, 死区) · `capex_quarterly16`(cov 0.64, ac=0, 未测) · `capex_annual12_3`(cov 0.81, ac=0, 未测) · `inventory_annual12_2`(cov 0.60, ac=0, 未测) · `goodwill_annual12`(cov 0.66, ac=0, 未测) · `enterprisevalue_annual12`(cov 0.70, ac=0, 未测) · `ebitdarep_annual12`(cov 0.68, ac=0, 未测)

## §4 未测全量（cov ≥ 0.70，按覆盖降序）

| # | field id | 指标 | cov | ac | uc |
|---:|---|---|---:|---:|---:|
| 1 | `mean_forecast_actual_combined_fxadj_eps_annual12_3` | eps_annual12_3 | 0.9779 | 0 | 0 |
| 2 | `mean_forecast_actual_combined_pretax_annual12` | pretax_annual12 | 0.9665 | 1 | 1 |
| 3 | `mean_forecast_actual_combined_gps` | gps | 0.9659 | 0 | 0 |
| 4 | `mean_forecast_actual_combined_revenue_annual12_tribes` | revenue_annual12_tribes | 0.9497 | 1 | 1 |
| 5 | `mean_forecast_actual_combined_fxadj_revenue_quarterly16` | revenue_quarterly16 | 0.9465 | 0 | 0 |
| 6 | `mean_forecast_actual_combined_revenue_quarterly16_3` | revenue_quarterly16_3 | 0.9465 | 0 | 0 |
| 7 | `mean_forecast_actual_combined_fxadj_epsreported_annual12` | epsreported_annual12 | 0.9433 | 2 | 2 |
| 8 | `mean_forecast_actual_combined_pretax_annual12_2` | pretax_annual12_2 | 0.9431 | 0 | 0 |
| 9 | `mean_forecast_actual_combined_ebit_annual12` | ebit_annual12 | 0.9396 | 0 | 0 |
| 10 | `mean_forecast_actual_combined_sharesoutstanding_annual12` | sharesoutstanding_annual12 | 0.9374 | 0 | 0 |
| 11 | `mean_forecast_actual_combined_fullyreported` | fullyreported | 0.9305 | 1 | 1 |
| 12 | `mean_forecast_actual_combined_fxadj_gps_fq16` | gps_fq16 | 0.9305 | 0 | 0 |
| 13 | `mean_forecast_actual_combined_eps_quarterly16_tribes` | eps_quarterly16_tribes | 0.9303 | 0 | 0 |
| 14 | `mean_forecast_actual_combined_taxprovision_annual12_tribes` | taxprovision_annual12_tribes | 0.9279 | 1 | 1 |
| 15 | `mean_forecast_actual_combined_pretax_reported_annual12_tribes` | pretax_reported_annual12_tribes | 0.9227 | 1 | 1 |
| 16 | `mean_forecast_actual_combined_ebit_quarterly16` | ebit_quarterly16 | 0.9191 | 0 | 0 |
| 17 | `mean_forecast_actual_combined_netprofit_quarterly16` | netprofit_quarterly16 | 0.9179 | 0 | 0 |
| 18 | `mean_forecast_actual_combined_reportednet` | reportednet | 0.9179 | 0 | 0 |
| 19 | `mean_forecast_actual_combined_pretax` | pretax | 0.9098 | 0 | 0 |
| 20 | `mean_forecast_actual_combined_tangbookvalue_annual12_tribes` | tangbookvalue_annual12_tribes | 0.9015 | 1 | 1 |
| 21 | `mean_forecast_actual_combined_nav_annual12_tribes` | nav_annual12_tribes | 0.8993 | 0 | 0 |
| 22 | `mean_forecast_actual_combined_ebit_quarterly16_tribes` | ebit_quarterly16_tribes | 0.8967 | 1 | 1 |
| 23 | `mean_forecast_actual_combined_pretax_quarterly16` | pretax_quarterly16 | 0.8901 | 0 | 0 |
| 24 | `mean_forecast_actual_combined_fxadj_ebt_annual12` | ebt_annual12 | 0.8808 | 0 | 0 |
| 25 | `mean_forecast_actual_combined_roe_annual12` | roe_annual12 | 0.8705 | 0 | 0 |
| 26 | `mean_forecast_actual_combined_pretax_reported_quarterly16` | pretax_reported_quarterly16 | 0.8662 | 0 | 0 |
| 27 | `mean_forecast_actual_combined_taxrate_annual12` | taxrate_annual12 | 0.8650 | 0 | 0 |
| 28 | `mean_forecast_actual_combined_ebitda_annual12` | ebitda_annual12 | 0.8636 | 1 | 1 |
| 29 | `mean_forecast_actual_combined_fxadj_marketable_securities_annual12_2` | marketable_securities_annual12_2 | 0.8634 | 0 | 0 |
| 30 | `mean_forecast_actual_combined_marketable_securities_annual12` | marketable_securities_annual12 | 0.8634 | 0 | 0 |
| 31 | `mean_forecast_actual_combined_dividend_annual12_2` | dividend_annual12_2 | 0.8591 | 0 | 0 |
| 32 | `mean_forecast_actual_combined_dps_annual12_3` | dps_annual12_3 | 0.8485 | 0 | 0 |
| 33 | `mean_forecast_actual_combined_operatingexpense_annual12` | operatingexpense_annual12 | 0.8405 | 0 | 0 |
| 34 | `mean_forecast_actual_combined_capex_annual12_3` | capex_annual12_3 | 0.8128 | 0 | 0 |
| 35 | `mean_forecast_actual_combined_fxadj_bvps_annual12_tribes` | bvps_annual12_tribes | 0.8126 | 0 | 0 |
| 36 | `mean_forecast_actual_combined_pretax_quarterly16_2` | pretax_quarterly16_2 | 0.8019 | 0 | 0 |
| 37 | `mean_forecast_actual_combined_fxadj_ebitda_quarterly16` | ebitda_quarterly16 | 0.7905 | 0 | 0 |
| 38 | `mean_forecast_actual_combined_fxadj_fcf_annual12` | fcf_annual12 | 0.7902 | 3 | 2 |
| 39 | `mean_forecast_actual_combined_totalliab_annual12_tribes` | totalliab_annual12_tribes | 0.7780 | 0 | 0 |
| 40 | `mean_forecast_actual_combined_grossmargin_annual12` | grossmargin_annual12 | 0.7607 | 0 | 0 |
| 41 | `mean_forecast_actual_combined_netdebt_annual12` | netdebt_annual12 | 0.7528 | 0 | 0 |
| 42 | `mean_forecast_actual_combined_fxadj_cashflowinvesting_annual12` | cashflowinvesting_annual12 | 0.7495 | 0 | 0 |
| 43 | `mean_forecast_actual_combined_grossmargin_annual12_tribes` | grossmargin_annual12_tribes | 0.7458 | 0 | 0 |
| 44 | `mean_forecast_actual_combined_cashflowfinancing_annual12` | cashflowfinancing_annual12 | 0.7429 | 0 | 0 |
| 45 | `mean_forecast_actual_combined_fxadj` | fxadj | 0.7405 | 0 | 0 |
| 46 | `mean_forecast_actual_combined_netdebt_annual12_2` | netdebt_annual12_2 | 0.7400 | 1 | 1 |
| 47 | `mean_forecast_actual_combined_fxadj_cfps_annual12` | cfps_annual12 | 0.7331 | 0 | 0 |
| 48 | `mean_forecast_actual_combined_fxadj_cfps_annual12_2` | cfps_annual12_2 | 0.7282 | 1 | 1 |
| 49 | `mean_forecast_actual_combined_currentassets_annual12` | currentassets_annual12 | 0.7212 | 0 | 0 |
| 50 | `mean_forecast_actual_combined_fxadj_currentliabilities_annual12` | currentliabilities_annual12 | 0.7200 | 0 | 0 |

## §5 全族 147 条原始清单

| # | field id | 指标 | cov | ac | uc | fxadj |
|---:|---|---|---:|---:|---:|---|
| 1 | `mean_forecast_actual_combined_eps_annual12_3` | eps_annual12_3 | 0.9779 | 0 | 0 |  |
| 2 | `mean_forecast_actual_combined_fxadj_eps_annual12_3` | eps_annual12_3 | 0.9779 | 0 | 0 | Y |
| 3 | `mean_forecast_actual_combined_fxadj_revenue_annual12` | revenue_annual12 | 0.9751 | 0 | 0 | Y |
| 4 | `mean_forecast_actual_combined_revenue_annual12` | revenue_annual12 | 0.9751 | 0 | 0 |  |
| 5 | `mean_forecast_actual_combined_fxadj_net2` | net2 | 0.9742 | 1 | 1 | Y |
| 6 | `mean_forecast_actual_combined_net2` | net2 | 0.9742 | 0 | 0 |  |
| 7 | `mean_forecast_actual_combined_fxadj_pretax_annual12` | pretax_annual12 | 0.9665 | 0 | 0 | Y |
| 8 | `mean_forecast_actual_combined_pretax_annual12` | pretax_annual12 | 0.9665 | 1 | 1 |  |
| 9 | `mean_forecast_actual_combined_fxadj_gps2` | gps2 | 0.9659 | 0 | 0 | Y |
| 10 | `mean_forecast_actual_combined_gps` | gps | 0.9659 | 0 | 0 |  |
| 11 | `mean_forecast_actual_combined_ebit_annual12_2` | ebit_annual12_2 | 0.9632 | 0 | 0 |  |
| 12 | `mean_forecast_actual_combined_fxadj_ebit_annual12_2` | ebit_annual12_2 | 0.9632 | 0 | 0 | Y |
| 13 | `mean_forecast_actual_combined_fxadj_reportednet_annual12_2` | reportednet_annual12_2 | 0.9589 | 0 | 0 | Y |
| 14 | `mean_forecast_actual_combined_reportednet_annual12_2` | reportednet_annual12_2 | 0.9589 | 0 | 0 |  |
| 15 | `mean_forecast_actual_combined_eps_annual12` | eps_annual12 | 0.9521 | 1 | 1 |  |
| 16 | `mean_forecast_actual_combined_fxadj_eps_annual12` | eps_annual12 | 0.9521 | 1 | 1 | Y |
| 17 | `mean_forecast_actual_combined_eps_quarterly16` | eps_quarterly16 | 0.9514 | 0 | 0 |  |
| 18 | `mean_forecast_actual_combined_fxadj_eps_quarterly16` | eps_quarterly16 | 0.9514 | 0 | 0 | Y |
| 19 | `mean_forecast_actual_combined_fxadj_netprofit_annual12` | netprofit_annual12 | 0.9498 | 2 | 2 | Y |
| 20 | `mean_forecast_actual_combined_netprofit_annual12` | netprofit_annual12 | 0.9498 | 0 | 0 |  |
| 21 | `mean_forecast_actual_combined_fxadj_revenue_annual12_tribes` | revenue_annual12_tribes | 0.9497 | 0 | 0 | Y |
| 22 | `mean_forecast_actual_combined_revenue_annual12_tribes` | revenue_annual12_tribes | 0.9497 | 1 | 1 |  |
| 23 | `mean_forecast_actual_combined_fxadj_revenue_quarterly16` | revenue_quarterly16 | 0.9465 | 0 | 0 | Y |
| 24 | `mean_forecast_actual_combined_revenue_quarterly16_3` | revenue_quarterly16_3 | 0.9465 | 0 | 0 |  |
| 25 | `mean_forecast_actual_combined_epsreported_annual12` | epsreported_annual12 | 0.9433 | 2 | 1 |  |
| 26 | `mean_forecast_actual_combined_fxadj_epsreported_annual12` | epsreported_annual12 | 0.9433 | 2 | 2 | Y |
| 27 | `mean_forecast_actual_combined_fxadj_pretax_reported_annual12` | pretax_reported_annual12 | 0.9432 | 0 | 0 | Y |
| 28 | `mean_forecast_actual_combined_pretax_reported_annual12` | pretax_reported_annual12 | 0.9432 | 0 | 0 |  |
| 29 | `mean_forecast_actual_combined_fxadj_pretax_annual12_2` | pretax_annual12_2 | 0.9431 | 0 | 0 | Y |
| 30 | `mean_forecast_actual_combined_pretax_annual12_2` | pretax_annual12_2 | 0.9431 | 0 | 0 |  |
| 31 | `mean_forecast_actual_combined_ebit_annual12` | ebit_annual12 | 0.9396 | 0 | 0 |  |
| 32 | `mean_forecast_actual_combined_sharesoutstanding_annual12` | sharesoutstanding_annual12 | 0.9374 | 0 | 0 |  |
| 33 | `mean_forecast_actual_combined_fxadj_netprofitreported_annual12` | netprofitreported_annual12 | 0.9369 | 0 | 0 | Y |
| 34 | `mean_forecast_actual_combined_netprofitreported_annual12` | netprofitreported_annual12 | 0.9369 | 0 | 0 |  |
| 35 | `mean_forecast_actual_combined_fullyreported` | fullyreported | 0.9305 | 1 | 1 |  |
| 36 | `mean_forecast_actual_combined_fxadj_gps_fq16` | gps_fq16 | 0.9305 | 0 | 0 | Y |
| 37 | `mean_forecast_actual_combined_eps_quarterly16_tribes` | eps_quarterly16_tribes | 0.9303 | 0 | 0 |  |
| 38 | `mean_forecast_actual_combined_fxadj_taxprovision_annual12_tribes` | taxprovision_annual12_tribes | 0.9279 | 0 | 0 | Y |
| 39 | `mean_forecast_actual_combined_taxprovision_annual12_tribes` | taxprovision_annual12_tribes | 0.9279 | 1 | 1 |  |
| 40 | `mean_forecast_actual_combined_revenue_quarterly16` | revenue_quarterly16 | 0.9248 | 0 | 0 |  |
| 41 | `mean_forecast_actual_combined_fxadj_pretax_reported_annual12_tribes` | pretax_reported_annual12_tribes | 0.9227 | 1 | 1 | Y |
| 42 | `mean_forecast_actual_combined_pretax_reported_annual12_tribes` | pretax_reported_annual12_tribes | 0.9227 | 1 | 1 |  |
| 43 | `mean_forecast_actual_combined_ebit_quarterly16` | ebit_quarterly16 | 0.9191 | 0 | 0 |  |
| 44 | `mean_forecast_actual_combined_fxadj_ebit_quarterly16_2` | ebit_quarterly16_2 | 0.9191 | 0 | 0 | Y |
| 45 | `mean_forecast_actual_combined_fxadj_nav_annual12` | nav_annual12 | 0.9184 | 0 | 0 | Y |
| 46 | `mean_forecast_actual_combined_nav_annual12` | nav_annual12 | 0.9184 | 0 | 0 |  |
| 47 | `mean_forecast_actual_combined_fxadj_netprofit_quarterly16` | netprofit_quarterly16 | 0.9179 | 0 | 0 | Y |
| 48 | `mean_forecast_actual_combined_fxadj_reportednet` | reportednet | 0.9179 | 0 | 0 | Y |
| 49 | `mean_forecast_actual_combined_netprofit_quarterly16` | netprofit_quarterly16 | 0.9179 | 0 | 0 |  |
| 50 | `mean_forecast_actual_combined_reportednet` | reportednet | 0.9179 | 0 | 0 |  |
| 51 | `mean_forecast_actual_combined_eps_reported_quarterly16` | eps_reported_quarterly16 | 0.9102 | 0 | 0 |  |
| 52 | `mean_forecast_actual_combined_fxadj_eps_reported_quarterly16` | eps_reported_quarterly16 | 0.9102 | 0 | 0 | Y |
| 53 | `mean_forecast_actual_combined_fxadj_pretax` | pretax | 0.9098 | 1 | 1 | Y |
| 54 | `mean_forecast_actual_combined_pretax` | pretax | 0.9098 | 0 | 0 |  |
| 55 | `mean_forecast_actual_combined_fxadj_tangbookvalue_annual12_tribes` | tangbookvalue_annual12_tribes | 0.9015 | 0 | 0 | Y |
| 56 | `mean_forecast_actual_combined_tangbookvalue_annual12_tribes` | tangbookvalue_annual12_tribes | 0.9015 | 1 | 1 |  |
| 57 | `mean_forecast_actual_combined_fxadj_nav_annual12_tribes` | nav_annual12_tribes | 0.8993 | 0 | 0 | Y |
| 58 | `mean_forecast_actual_combined_nav_annual12_tribes` | nav_annual12_tribes | 0.8993 | 0 | 0 |  |
| 59 | `mean_forecast_actual_combined_fxadj_interest_expense_annual12` | interest_expense_annual12 | 0.8976 | 1 | 1 | Y |
| 60 | `mean_forecast_actual_combined_interest_expense_annual12` | interest_expense_annual12 | 0.8976 | 0 | 0 |  |
| 61 | `mean_forecast_actual_combined_ebit_quarterly16_tribes` | ebit_quarterly16_tribes | 0.8967 | 1 | 1 |  |
| 62 | `mean_forecast_actual_combined_fxadj_ebit_quarterly16` | ebit_quarterly16 | 0.8967 | 0 | 0 | Y |
| 63 | `mean_forecast_actual_combined_fxadj_netprofit_reported_quarterly16` | netprofit_reported_quarterly16 | 0.8945 | 0 | 0 | Y |
| 64 | `mean_forecast_actual_combined_netprofit_reported_quarterly16` | netprofit_reported_quarterly16 | 0.8945 | 0 | 0 |  |
| 65 | `mean_forecast_actual_combined_fxadj_total_assets_annual12` | total_assets_annual12 | 0.8937 | 0 | 0 | Y |
| 66 | `mean_forecast_actual_combined_total_assets_annual12` | total_assets_annual12 | 0.8937 | 3 | 2 |  |
| 67 | `mean_forecast_actual_combined_fxadj_pretax_quarterly16` | pretax_quarterly16 | 0.8901 | 0 | 0 | Y |
| 68 | `mean_forecast_actual_combined_pretax_quarterly16` | pretax_quarterly16 | 0.8901 | 0 | 0 |  |
| 69 | `mean_forecast_actual_combined_ebt_annual12` | ebt_annual12 | 0.8808 | 0 | 0 |  |
| 70 | `mean_forecast_actual_combined_fxadj_ebt_annual12` | ebt_annual12 | 0.8808 | 0 | 0 | Y |
| 71 | `mean_forecast_actual_combined_roe_annual12` | roe_annual12 | 0.8705 | 0 | 0 |  |
| 72 | `mean_forecast_actual_combined_fxadj_pretax_reported_quarterly16` | pretax_reported_quarterly16 | 0.8662 | 0 | 0 | Y |
| 73 | `mean_forecast_actual_combined_pretax_reported_quarterly16` | pretax_reported_quarterly16 | 0.8662 | 0 | 0 |  |
| 74 | `mean_forecast_actual_combined_taxrate_annual12` | taxrate_annual12 | 0.8650 | 0 | 0 |  |
| 75 | `mean_forecast_actual_combined_ebitda_annual12` | ebitda_annual12 | 0.8636 | 1 | 1 |  |
| 76 | `mean_forecast_actual_combined_fxadj_marketable_securities_annual12_2` | marketable_securities_annual12_2 | 0.8634 | 0 | 0 | Y |
| 77 | `mean_forecast_actual_combined_marketable_securities_annual12` | marketable_securities_annual12 | 0.8634 | 0 | 0 |  |
| 78 | `mean_forecast_actual_combined_roe_annual12_tribes` | roe_annual12_tribes | 0.8592 | 2 | 2 |  |
| 79 | `mean_forecast_actual_combined_dividend_annual12_2` | dividend_annual12_2 | 0.8591 | 0 | 0 |  |
| 80 | `mean_forecast_actual_combined_fxadj_dividend_annual12` | dividend_annual12 | 0.8591 | 0 | 0 | Y |
| 81 | `mean_forecast_actual_combined_dps_annual12_3` | dps_annual12_3 | 0.8485 | 0 | 0 |  |
| 82 | `mean_forecast_actual_combined_fxadj_dividend_annual12_2` | dividend_annual12_2 | 0.8485 | 0 | 0 | Y |
| 83 | `mean_forecast_actual_combined_fxadj_operatingexpense_annual12` | operatingexpense_annual12 | 0.8405 | 0 | 0 | Y |
| 84 | `mean_forecast_actual_combined_operatingexpense_annual12` | operatingexpense_annual12 | 0.8405 | 0 | 0 |  |
| 85 | `mean_forecast_actual_combined_capex_annual12_2` | capex_annual12_2 | 0.8334 | 0 | 0 |  |
| 86 | `mean_forecast_actual_combined_fxadj_capex_annual12_2` | capex_annual12_2 | 0.8334 | 0 | 0 | Y |
| 87 | `mean_forecast_actual_combined_bvps_annual12` | bvps_annual12 | 0.8278 | 0 | 0 |  |
| 88 | `mean_forecast_actual_combined_fxadj_bvps_annual12` | bvps_annual12 | 0.8278 | 0 | 0 | Y |
| 89 | `mean_forecast_actual_combined_capex_annual12_3` | capex_annual12_3 | 0.8128 | 0 | 0 |  |
| 90 | `mean_forecast_actual_combined_bvps_annual12_tribes` | bvps_annual12_tribes | 0.8126 | 0 | 0 |  |
| 91 | `mean_forecast_actual_combined_fxadj_bvps_annual12_tribes` | bvps_annual12_tribes | 0.8126 | 0 | 0 | Y |
| 92 | `mean_forecast_actual_combined_fxadj_pretax_quarterly16_2` | pretax_quarterly16_2 | 0.8019 | 0 | 0 | Y |
| 93 | `mean_forecast_actual_combined_pretax_quarterly16_2` | pretax_quarterly16_2 | 0.8019 | 0 | 0 |  |
| 94 | `mean_forecast_actual_combined_cfo_annual12` | cfo_annual12 | 0.7956 | 2 | 2 |  |
| 95 | `mean_forecast_actual_combined_fxadj_cfo_annual12` | cfo_annual12 | 0.7956 | 3 | 2 | Y |
| 96 | `mean_forecast_actual_combined_ebitda_quarterly16` | ebitda_quarterly16 | 0.7905 | 0 | 0 |  |
| 97 | `mean_forecast_actual_combined_fxadj_ebitda_quarterly16` | ebitda_quarterly16 | 0.7905 | 0 | 0 | Y |
| 98 | `mean_forecast_actual_combined_fcf_annual12` | fcf_annual12 | 0.7902 | 1 | 1 |  |
| 99 | `mean_forecast_actual_combined_fxadj_fcf_annual12` | fcf_annual12 | 0.7902 | 3 | 2 | Y |
| 100 | `mean_forecast_actual_combined_fxadj_totalliab_annual12_tribes` | totalliab_annual12_tribes | 0.7780 | 0 | 0 | Y |
| 101 | `mean_forecast_actual_combined_totalliab_annual12_tribes` | totalliab_annual12_tribes | 0.7780 | 0 | 0 |  |
| 102 | `mean_forecast_actual_combined_grossmargin_annual12` | grossmargin_annual12 | 0.7607 | 0 | 0 |  |
| 103 | `mean_forecast_actual_combined_fxadj_netdebt_annual12` | netdebt_annual12 | 0.7528 | 0 | 0 | Y |
| 104 | `mean_forecast_actual_combined_netdebt_annual12` | netdebt_annual12 | 0.7528 | 0 | 0 |  |
| 105 | `mean_forecast_actual_combined_cashflowinvesting_annual12` | cashflowinvesting_annual12 | 0.7495 | 0 | 0 |  |
| 106 | `mean_forecast_actual_combined_fxadj_cashflowinvesting_annual12` | cashflowinvesting_annual12 | 0.7495 | 0 | 0 | Y |
| 107 | `mean_forecast_actual_combined_grossmargin_annual12_tribes` | grossmargin_annual12_tribes | 0.7458 | 0 | 0 |  |
| 108 | `mean_forecast_actual_combined_cashflowfinancing_annual12` | cashflowfinancing_annual12 | 0.7429 | 0 | 0 |  |
| 109 | `mean_forecast_actual_combined_fxadj` | fxadj | 0.7405 | 0 | 0 | Y |
| 110 | `mean_forecast_actual_combined_netdebt_annual12_2` | netdebt_annual12_2 | 0.7400 | 1 | 1 |  |
| 111 | `mean_forecast_actual_combined_cfps_annual12` | cfps_annual12 | 0.7331 | 0 | 0 |  |
| 112 | `mean_forecast_actual_combined_fxadj_cfps_annual12` | cfps_annual12 | 0.7331 | 0 | 0 | Y |
| 113 | `mean_forecast_actual_combined_cfps_annual12_2` | cfps_annual12_2 | 0.7282 | 0 | 0 |  |
| 114 | `mean_forecast_actual_combined_fxadj_cfps_annual12_2` | cfps_annual12_2 | 0.7282 | 1 | 1 | Y |
| 115 | `mean_forecast_actual_combined_currentassets_annual12` | currentassets_annual12 | 0.7212 | 0 | 0 |  |
| 116 | `mean_forecast_actual_combined_currentliabilities_annual12` | currentliabilities_annual12 | 0.7200 | 0 | 0 |  |
| 117 | `mean_forecast_actual_combined_fxadj_currentliabilities_annual12` | currentliabilities_annual12 | 0.7200 | 0 | 0 | Y |
| 118 | `mean_forecast_actual_combined_enterprisevalue_annual12` | enterprisevalue_annual12 | 0.6969 | 0 | 0 |  |
| 119 | `mean_forecast_actual_combined_ebitdarep_annual12` | ebitdarep_annual12 | 0.6756 | 0 | 0 |  |
| 120 | `mean_forecast_actual_combined_fxadj_goodwill_annual12` | goodwill_annual12 | 0.6615 | 0 | 0 | Y |
| 121 | `mean_forecast_actual_combined_goodwill_annual12` | goodwill_annual12 | 0.6615 | 0 | 0 |  |
| 122 | `mean_forecast_actual_combined_grossmargin_quarterly16_2` | grossmargin_quarterly16_2 | 0.6503 | 0 | 0 |  |
| 123 | `mean_forecast_actual_combined_capex_quarterly16` | capex_quarterly16 | 0.6422 | 0 | 0 |  |
| 124 | `mean_forecast_actual_combined_fxadj_capex_quarterly16` | capex_quarterly16 | 0.6422 | 0 | 0 | Y |
| 125 | `mean_forecast_actual_combined_dps_quarterly16_2` | dps_quarterly16_2 | 0.6328 | 0 | 0 |  |
| 126 | `mean_forecast_actual_combined_fxadj_dps_quarterly16_2` | dps_quarterly16_2 | 0.6328 | 0 | 0 | Y |
| 127 | `mean_forecast_actual_combined_depreciation_annual12` | depreciation_annual12 | 0.6300 | 0 | 0 |  |
| 128 | `mean_forecast_actual_combined_fxadj_depreciation_annual12` | depreciation_annual12 | 0.6300 | 1 | 1 | Y |
| 129 | `mean_forecast_actual_combined_dps_quarterly16` | dps_quarterly16 | 0.6035 | 0 | 0 |  |
| 130 | `mean_forecast_actual_combined_fxadj_dps_quarterly16` | dps_quarterly16 | 0.6035 | 0 | 0 | Y |
| 131 | `mean_forecast_actual_combined_fxadj_inventory_annual12_2` | inventory_annual12_2 | 0.5966 | 0 | 0 | Y |
| 132 | `mean_forecast_actual_combined_inventory_annual12` | inventory_annual12 | 0.5966 | 0 | 0 |  |
| 133 | `mean_forecast_actual_combined_fcfps_annual12` | fcfps_annual12 | 0.5922 | 1 | 1 |  |
| 134 | `mean_forecast_actual_combined_fxadj_fcfps_annual12` | fcfps_annual12 | 0.5922 | 0 | 0 | Y |
| 135 | `mean_forecast_actual_combined_cfps_quarterly16` | cfps_quarterly16 | 0.5690 | 0 | 0 |  |
| 136 | `mean_forecast_actual_combined_fxadj_cfps_quarterly16` | cfps_quarterly16 | 0.5690 | 0 | 0 | Y |
| 137 | `mean_forecast_actual_combined_bvps_quarterly16_2` | bvps_quarterly16_2 | 0.5641 | 0 | 0 |  |
| 138 | `mean_forecast_actual_combined_fxadj_bvps_quarterly16_2` | bvps_quarterly16_2 | 0.5641 | 0 | 0 | Y |
| 139 | `mean_forecast_actual_combined_return_on_equity_quarterly16` | return_on_equity_quarterly16 | 0.5283 | 0 | 0 |  |
| 140 | `mean_forecast_actual_combined_roe_quarterly16` | roe_quarterly16 | 0.5149 | 0 | 0 |  |
| 141 | `mean_forecast_actual_combined_fcf_quarterly16` | fcf_quarterly16 | 0.5144 | 0 | 0 |  |
| 142 | `mean_forecast_actual_combined_fxadj_fcf_quarterly16_tribes` | fcf_quarterly16_tribes | 0.5144 | 1 | 1 | Y |
| 143 | `mean_forecast_actual_combined_fxadj_netdebt_quarterly16` | netdebt_quarterly16 | 0.4847 | 1 | 1 | Y |
| 144 | `mean_forecast_actual_combined_netdebt_quarterly16_2` | netdebt_quarterly16_2 | 0.4847 | 0 | 0 |  |
| 145 | `mean_forecast_actual_combined_return_on_capital_annual12` | return_on_capital_annual12 | 0.4708 | 0 | 0 |  |
| 146 | `mean_forecast_actual_combined_fcf_fq16` | fcf_fq16 | 0.3887 | 0 | 0 |  |
| 147 | `mean_forecast_actual_combined_fxadj_fcf_quarterly16` | fcf_quarterly16 | 0.3887 | 0 | 0 | Y |
