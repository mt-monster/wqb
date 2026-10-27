# other401 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other401` |
| 名称 | Governance, Accounting, Management, and Equality |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 65 |
| 覆盖率 | 0.707 |
| 平台已有 alpha | 244 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

Dataset relating to governance, accounting quality, management, and equality. The factors are chosen by a machine learning model which is trained to predict returns. The model is completely out-of-sample, trained at the end of each month, with only data prior to the date.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **65** |
| 类型分布 | MATRIX×65 |
| 平均覆盖率 | **0.707** |
| 覆盖率区间 | 0.25 ~ 0.88 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 41 | 63.1% |
| 低 (0.50–0.70) | 16 | 24.6% |
| 稀疏 (<0.50) | 8 | 12.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 44 | 67.7% |
| UNUSABLE | 12 | 18.5% |
| DEAD_STATIC | 5 | 7.7% |
| DEAD | 4 | 6.2% |

- 已实测字段：**9** 个（14%），best_sharpe 最高 **0.70**，中位 -0.05

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 29 | 0.72 | oth401_game_total_debt_chg、oth401_game_earning_smooth、oth401_qes_gamef_negative_earnings |
| 其他 | 20 | 0.72 | oth401_game_inc_cash_tax、oth401_game_pension_interest、oth401_game_sg_a_cost_ratio |
| 宏观与行业 | 5 | 0.56 | oth401_game_tax_rate、oth401_game_eff_interest_rate、oth401_game_depreciation_chg |
| 风险与质量 | 4 | 0.84 | oth401_qes_gamef_pscore、oth401_qes_gamef_score、oth401_qes_gamef_cscore |
| 修正与预期 | 4 | 0.64 | oth401_game_optimism_sale、oth401_game_eps_sur_vol、oth401_game_optimism_gma |
| 价量与波动 | 2 | 0.82 | oth401_game_relative_rtn_vol、oth401_game_sg_a_vol |
| 持仓与资金流 | 1 | 0.35 | oth401_game_esop_grant |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth401_game_inc_cash_tax` | MATRIX | 0.694 | 其他 | 1 | 0.70 | 1.07 | 0.62 | DEAD | Income Statement Tax to Cash Tax |
| 2 | `oth401_qes_gamef_pscore` | MATRIX | 0.873 | 风险与质量 | 1 | 0.30 | 0.74 | 0.34 | DEAD | Piotroski |
| 3 | `oth401_game_pension_interest` | MATRIX | 0.522 | 其他 | 1 | 0.10 | 0.14 | 0.00 | DEAD_STATIC | Pension Interest Cost |
| 4 | `oth401_game_sg_a_cost_ratio` | MATRIX | 0.817 | 其他 | 1 | -0.03 | -0.01 | 0.11 | DEAD_STATIC | SG&A Cost Ratio |
| 5 | `oth401_game_capex_dep` | MATRIX | 0.510 | 其他 | 1 | -0.05 | -0.17 | -0.09 | DEAD_STATIC | Capex to Depreciation |
| 6 | `oth401_game_receivable_chg` | MATRIX | 0.865 | 其他 | 1 | -0.25 | -1.15 | -0.17 | DEAD_STATIC | Change in Receivables |
| 7 | `oth401_qes_gamef_ohlson` | MATRIX | 0.855 | 其他 | 1 | -0.41 | 0.09 | -0.05 | DEAD | Ohlson |
| 8 | `oth401_game_total_debt_chg` | MATRIX | 0.770 | 盈利与财务 | 1 | -0.42 | -0.43 | -0.19 | DEAD | Change in Debt |
| 9 | `oth401_game_earning_smooth` | MATRIX | 0.758 | 盈利与财务 | 1 | -0.54 | -0.07 | -0.37 | DEAD_STATIC | Earnings Smoothness |
| 10 | `oth401_game_relative_rtn_vol` | MATRIX | 0.877 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative Volatility |
| 11 | `oth401_qes_gamef_mohanram` | MATRIX | 0.868 | 其他 | 0 | — | — | — | UNTESTED | Mohanram |
| 12 | `oth401_qes_gamef_negative_earnings` | MATRIX | 0.866 | 盈利与财务 | 0 | — | — | — | UNTESTED | Negative Earnings |
| 13 | `oth401_game_serial_special` | MATRIX | 0.866 | 其他 | 0 | — | — | — | UNTESTED | Serial Special Items to Sales |
| 14 | `oth401_game_receivable_days` | MATRIX | 0.865 | 其他 | 0 | — | — | — | UNTESTED | Receivable Days |
| 15 | `oth401_game_tax_rate` | MATRIX | 0.864 | 宏观与行业 | 0 | — | — | — | UNTESTED | Tax Rate |
| 16 | `oth401_game_equity_dilution` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity Dilution |
| 17 | `oth401_game_other_asset_gr` | MATRIX | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Asset Growth |
| 18 | `oth401_game_asset_turnover_chg` | MATRIX | 0.859 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Asset Turnover |
| 19 | `oth401_game_noa` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Operating Assets |
| 20 | `oth401_qes_gamef_score` | MATRIX | 0.854 | 风险与质量 | 0 | — | — | — | UNTESTED | Score |
| 21 | `oth401_qes_gamef_cscore` | MATRIX | 0.839 | 风险与质量 | 0 | — | — | — | UNTESTED | Montier's C Score |
| 22 | `oth401_game_optimism_sale` | MATRIX | 0.833 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Optimism Sales |
| 23 | `oth401_game_capex_sale` | MATRIX | 0.832 | 其他 | 0 | — | — | — | UNTESTED | Capex to Sales |
| 24 | `oth401_game_sg_a_inefficiency` | MATRIX | 0.829 | 其他 | 0 | — | — | — | UNTESTED | SG&A Inefficiency |
| 25 | `oth401_qes_gamef_earn_var` | MATRIX | 0.809 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Variability |
| 26 | `oth401_qes_gamef_grossprofit_asset` | MATRIX | 0.806 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Profit Over Asset |
| 27 | `oth401_qes_gamef_cashflow_var` | MATRIX | 0.803 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Variability |
| 28 | `oth401_qes_gamef_chs_default` | MATRIX | 0.798 | 风险与质量 | 0 | — | — | — | UNTESTED | CHS_DEFAULT |
| 29 | `oth401_game_gma_chg` | MATRIX | 0.797 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Gross Margin |
| 30 | `oth401_game_payble_days` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Payable Days |
| 31 | `oth401_game_cash_flow_coverage` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash Flow Coverage Ratio |
| 32 | `oth401_game_deferred_tax_liab_chg` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Deferred Tax Liabilities |
| 33 | `oth401_game_short_term_debt` | MATRIX | 0.785 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short Term Debt Ratio |
| 34 | `oth401_game_gross_margin_vol` | MATRIX | 0.784 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin Volatility |
| 35 | `oth401_qes_gamef_icfroe_1y` | MATRIX | 0.773 | 盈利与财务 | 0 | — | — | — | UNTESTED | Incremental Cash Flow Return Over Equity Over 1 Year |
| 36 | `oth401_game_sg_a_vol` | MATRIX | 0.760 | 价量与波动 | 0 | — | — | — | UNTESTED | SG&A Volatility |
| 37 | `oth401_game_interest_investment_inc` | MATRIX | 0.754 | 其他 | 0 | — | — | — | UNTESTED | Interest and Investment Income |
| 38 | `oth401_game_non_oper_inc` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Non-Operating Income to EBITDA |
| 39 | `oth401_game_pension_expense` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pension Expense to EBITDA |
| 40 | `oth401_game_eps_vol` | MATRIX | 0.731 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Volatility |
| 41 | `oth401_game_eff_interest_rate` | MATRIX | 0.721 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective Interest Rate |
| 42 | `oth401_qes_gamef_icfroe_3y` | MATRIX | 0.717 | 盈利与财务 | 0 | — | — | — | UNTESTED | Incremental Cash Flow Return over Equity over 3 Years |
| 43 | `oth401_game_deferred_tax_asset_chg` | MATRIX | 0.711 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Deferred Tax Assets |
| 44 | `oth401_game_eps_sur_vol` | MATRIX | 0.707 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Forecast Error |
| 45 | `oth401_game_non_production_asset` | MATRIX | 0.685 | 盈利与财务 | 0 | — | — | — | UNTESTED | Non-Production Assets |
| 46 | `oth401_game_inventory_chg` | MATRIX | 0.680 | 其他 | 0 | — | — | — | UNTESTED | Change in Inventory |
| 47 | `oth401_game_inventory_days` | MATRIX | 0.680 | 其他 | 0 | — | — | — | UNTESTED | Inventory Days |
| 48 | `oth401_game_pension_ev` | MATRIX | 0.667 | 其他 | 0 | — | — | — | UNTESTED | Pension and Other Benefit to TEV |
| 49 | `oth401_game_minority_interest` | MATRIX | 0.655 | 盈利与财务 | 0 | — | — | — | UNTESTED | Minority Interest to Equity |
| 50 | `oth401_game_optimism_gma` | MATRIX | 0.652 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Optimism Gross Margin |
| 51 | `oth401_qes_gamef_icfroe_5y` | MATRIX | 0.645 | 盈利与财务 | 0 | — | — | — | UNTESTED | Incremental Cash Flow Return Over Equity Over 5 Years |
| 52 | `oth401_game_labor_efficiency_chg` | MATRIX | 0.625 | 其他 | 0 | — | — | — | UNTESTED | Change in Labor Efficiency |
| 53 | `oth401_game_prepaid_expense` | MATRIX | 0.613 | 其他 | 0 | — | — | — | UNTESTED | Prepaid Expense to Sales |
| 54 | `oth401_game_pension_debt_equi_pbo` | MATRIX | 0.571 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt Equivalent Net PBO |
| 55 | `oth401_game_accruals_vol` | MATRIX | 0.561 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accrual Volatility |
| 56 | `oth401_game_pension_pbo` | MATRIX | 0.560 | 其他 | 0 | — | — | — | UNUSABLE | Projected Benefit Obligation to TEV |
| 57 | `oth401_game_depreciation_chg` | MATRIX | 0.505 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Change in Depreciation Rate |
| 58 | `oth401_game_finished_goods` | MATRIX | 0.486 | 其他 | 0 | — | — | — | UNUSABLE | Finished Goods to Inventory |
| 59 | `oth401_game_pension_discount_rate` | MATRIX | 0.443 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Pension Discount Rate |
| 60 | `oth401_game_deferred_sal_chg` | MATRIX | 0.421 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in Deferred Revenue |
| 61 | `oth401_qes_gamef_earnigs_timeliness` | MATRIX | 0.400 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Timeliness |
| 62 | `oth401_game_an_cov_chng` | MATRIX | 0.379 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst Coverage Change Over Time |
| 63 | `oth401_game_esop_grant` | MATRIX | 0.347 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Employee Stock Ownership Plan Grants |
| 64 | `oth401_game_contingent_liab` | MATRIX | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Contingent Liabilities to Equity |
| 65 | `oth401_game_amortization_rate` | MATRIX | 0.255 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Amortization Rate |

## 六、本地回测证据

- 本地累计回测 **9** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `0mXwM5Z6` | 0.70 | 0.34 | 1.07 | 0.62 | 0.04 | ["LOW_SHARPE | 235 | `group_neutralize(ts_delta(oth401_game_inc_cash_tax,126), bucket(rank(ts_backfill(oth401_ga` |
| `1YXwz03z` | 0.30 | 0.08 | 0.74 | 0.34 | 0.03 | ["LOW_SHARPE | 235 | `group_neutralize(subtract(oth401_qes_gamef_pscore, oth401_qes_gamef_mohanram), bucket(rank` |
| `wpZjapox` | 0.10 | 0.02 | 0.14 | 0.00 | 0.02 | ["LOW_SHARPE | 235 | `group_neutralize(subtract(rank(ts_backfill(oth401_game_pension_interest,22)), rank(ts_back` |
| `qMxjNM7v` | -0.03 | 0.00 | -0.01 | 0.11 | 0.02 | ["LOW_SHARPE | 235 | `group_neutralize(subtract(rank(ts_backfill(oth401_game_sg_a_cost_ratio,22)), rank(ts_backf` |
| `88jlp8RV` | -0.05 | -0.01 | -0.17 | -0.09 | 0.02 | ["LOW_SHARPE | 235 | `group_neutralize(subtract(rank(ts_backfill(oth401_game_capex_dep, 250)), rank(ts_backfill(` |
| `O0N7G0A7` | -0.25 | -0.07 | -1.15 | -0.17 | 0.02 | ["LOW_SHARPE | 235 | `group_neutralize(subtract(add(rank(ts_backfill(oth401_game_receivable_chg,22)), rank(ts_ba` |
| `kqojPqNd` | -0.41 | -0.25 | 0.09 | -0.05 | 0.19 | ["LOW_SHARPE | 235 | `group_count(oth401_qes_gamef_ohlson, sector)` |
| `omLqNmEn` | -0.42 | -0.17 | -0.43 | -0.19 | 0.06 | ["LOW_SHARPE | 235 | `divide(oth401_game_total_debt_chg, add(abs(oth401_qes_gamef_chs_default), 0.01))` |
| `0mXwpmY2` | -0.54 | -0.21 | -0.07 | -0.37 | 0.02 | ["LOW_SHARPE | 235 | `group_neutralize(subtract(normalize(ts_backfill(oth401_game_earning_smooth,22)), rank(ts_b` |

## 七、判死记录（sealed dead_end）

- `EUR-OTHER401-WEAK`（2026-09-23T18:27:10）family=other401 基本面矩阵族（oth401_* 65 字段 MATRIX）：{"family": "other401 基本面矩阵族（oth401_* 65 字段 MATRIX）", "reason": "wave235 9 探针全灭：best sharpe 0.70 / fit 0.34 / 2Y 1.07，CONCENTRATED_WEIGHT+LOW_ROBUST_UNIVERSE；D4 资格线 1.25 未达 → 判死。1 条 group_cartesian_product(sector,sector) 坏式被自动隔离。FUNDAMENTAL 塔候选 other401 出局；other452(cov0.37)/fundamental93(0.33) 均低于地板。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "seal

