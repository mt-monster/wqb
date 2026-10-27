# fundamental72 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental72` |
| 名称 | Comprehensive Fundamental Data |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 876 |
| 覆盖率 | 0.4976 |
| 平台已有 alpha | 2202 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a comprehensive mapping between Reuters Instrument Codes (RICs) and Bloomberg IDs for global securities. It enables users to cross-reference and link securities across two major financial data platforms, facilitating seamless integration of datasets from different sources. The mapping covers a wide range of asset classes and regions, supporting data normalization and consolidation for research, analytics, and operational workflows. By ensuring accurate identifier matching, this dataset is essential for portfolio management, risk analysis, and multi-source data aggregation, ultimately improving the reliability of price movement predictions and historical backtesting.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **876** |
| 类型分布 | MATRIX×449　VECTOR×427 |
| 平均覆盖率 | **0.498** |
| 覆盖率区间 | 0.15 ~ 0.91 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 1 | 0.1% |
| 中 (0.70–0.90) | 189 | 21.6% |
| 低 (0.50–0.70) | 188 | 21.5% |
| 稀疏 (<0.50) | 498 | 56.8% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 596 | 68.0% |
| UNTESTED | 280 | 32.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 280 / UNUSABLE 596 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 386 | 0.50 | fnd72_pit_or_is_a_spe_si、fnd72_s_pit_or_bs_a2_announcement_dt、fnd72_s_pit_or_bs_a_announcement_dt |
| 其他 | 378 | 0.49 | fnd72_pit_or_cf_a_cf_form_of_statement、fnd72_s_pit_or_bs_a2_latest_period_end_dt_full_record、fnd72_s_pit_or_bs_a_latest_period_end_dt_full_record |
| 持仓与资金流 | 59 | 0.56 | fnd72_pit_or_cf_a_cf_def_of_fund、fnd72_s_pit_or_bs_a2_fundamental_entry_dt、fnd72_s_pit_or_bs_a_fundamental_entry_dt |
| 价量与波动 | 22 | 0.48 | fnd72_is_a_fiscal_year_period、fnd72_bs_a_fiscal_year_period、fnd72_cf_a_fiscal_year_period |
| 宏观与行业 | 13 | 0.47 | reporting_currency_code_41、fnd72_s_pit_or_is_a_is_foreign_crncy_trans_adj、fnd72_pit_or_is_a_is_foreign_crncy_trans_adj |
| 风险与质量 | 7 | 0.50 | fnd72_s_pit_or_is_a_min_noncontrol_interest_credits、fnd72_pit_or_is_a_min_noncontrol_interest_credits、fnd72_pit_or_is_q_min_noncontrol_interest_credits |
| 元数据与非信号 | 6 | 0.62 | fnd72_s_pit_or_is_a_is_sga_other_op_depr_op_maint、fnd72_pit_or_is_a_id_bb_global、fnd72_pit_or_cf_a_id_bb_global |
| 搜索与替代数据 | 4 | 0.43 | fnd72_s_pit_or_is_a_is_rd_expend、fnd72_pit_or_is_a_is_rd_expend、fnd72_pit_or_is_q_is_rd_expend |
| 修正与预期 | 1 | 0.28 | fnd72_pit_or_is_a_is_expected_return_plan_assets |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `fnd72_pit_or_cf_a_cf_def_of_fund` | VECTOR | 0.906 | 持仓与资金流 | 0 | — | — | — | UNTESTED | No longer supported |
| 2 | `fnd72_pit_or_cf_a_cf_form_of_statement` | VECTOR | 0.883 | 其他 | 0 | — | — | — | UNTESTED | No longer supported |
| 3 | `fnd72_is_a_fiscal_year_period` | VECTOR | 0.881 | 价量与波动 | 0 | — | — | — | UNTESTED | This field, used for the History Wizard, will return the Fiscal year and period that coincides with the period end date |
| 4 | `fnd72_bs_a_fiscal_year_period` | VECTOR | 0.881 | 价量与波动 | 0 | — | — | — | UNTESTED | This field, used for the History Wizard, will return the Fiscal year and period that coincides with the period end date |
| 5 | `fnd72_cf_a_fiscal_year_period` | VECTOR | 0.879 | 价量与波动 | 0 | — | — | — | UNTESTED | This field, used for the History Wizard, will return the Fiscal year and period that coincides with the period end date |
| 6 | `fnd72_pit_or_is_a_spe_si` | VECTOR | 0.870 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Per Share |
| 7 | `fnd72_s_pit_or_bs_a2_announcement_dt` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Date of the latest earnings announcement with a full annual fundamental record available |
| 8 | `fnd72_s_pit_or_bs_a2_fundamental_entry_dt` | MATRIX | 0.834 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Date the fundamental record was entered into the database |
| 9 | `fnd72_s_pit_or_bs_a2_latest_period_end_dt_full_record` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Latest available period end date from full financial records |
| 10 | `fnd72_s_pit_or_bs_a_announcement_dt` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Latest full earnings report announcement date (annual) |
| 11 | `fnd72_s_pit_or_bs_a_fundamental_entry_dt` | MATRIX | 0.834 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Point in time timestamp when the fundamental data was entered |
| 12 | `fnd72_s_pit_or_bs_a_latest_period_end_dt_full_record` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Latest available period end date from full financial records |
| 13 | `fnd72_s_pit_or_is_a2_announcement_dt` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual latest full earnings report date |
| 14 | `fnd72_s_pit_or_is_a2_fundamental_entry_dt` | MATRIX | 0.834 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Fundamental data entry date |
| 15 | `fnd72_s_pit_or_is_a2_latest_period_end_dt_full_record` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Latest available period end date from the full financial records |
| 16 | `fnd72_s_pit_or_is_a3_announcement_dt` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual latest full earnings report date |
| 17 | `fnd72_s_pit_or_is_a3_fundamental_entry_dt` | MATRIX | 0.834 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Date the annual fundamental data record was entered |
| 18 | `fnd72_s_pit_or_is_a3_latest_period_end_dt_full_record` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Latest available period-end date from full financial records |
| 19 | `fnd72_s_pit_or_is_a_announcement_dt` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Date of the latest full annual earnings report for which complete fundamentals are available |
| 20 | `fnd72_s_pit_or_is_a_fundamental_entry_dt` | MATRIX | 0.834 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Fundamental data entry date |
| 21 | `fnd72_s_pit_or_is_a_latest_period_end_dt_full_record` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Latest available period-end date from full financial records (annual) |
| 22 | `reporting_currency_code_41` | MATRIX | 0.834 | 宏观与行业 | 0 | — | — | — | UNTESTED | The currency in which the financial statement values are reported. |
| 23 | `fnd72_s_pit_or_bs_a_bs_tot_asset` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets |
| 24 | `fnd72_s_pit_or_bs_a_bs_cash_near_cash_item` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Cash and cash equivalents and near-cash items |
| 25 | `fnd72_s_pit_or_bs_a_bs_retain_earn` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained Earnings (Balance Sheet) |
| 26 | `fnd72_s_pit_or_cf_a_announcement_dt` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Latest full earnings report date for which complete fundamentals are available (annual) |
| 27 | `fnd72_s_pit_or_cf_a_fundamental_entry_dt` | MATRIX | 0.834 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Annual fundamental data entry date when the record was entered into the system |
| 28 | `fnd72_s_pit_or_cf_a_latest_period_end_dt_full_record` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | Latest available period end date from full financial records |
| 29 | `fnd72_s_pit_or_bs_a_bs_other_asset_def_chng_other` | MATRIX | 0.833 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other long-term assets |
| 30 | `fnd72_s_pit_or_is_a3_net_income_bef_mi` | MATRIX | 0.833 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual net income before minority interests |
| 31 | `fnd72_s_pit_or_is_a_earn_for_common` | MATRIX | 0.833 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual net income available to common shareholders (after preferred dividends) |
| 32 | `fnd72_s_pit_or_is_a_net_income` | MATRIX | 0.833 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual net income (net profit or loss) |
| 33 | `fnd72_s_pit_or_is_a_is_oper_inc` | MATRIX | 0.833 | 其他 | 0 | — | — | — | UNTESTED | Operating income or loss from core operations (annual) |
| 34 | `fnd72_s_pit_or_is_a3_pretax_inc` | MATRIX | 0.833 | 其他 | 0 | — | — | — | UNTESTED | Annual pre-tax income |
| 35 | `fnd72_s_pit_or_cf_a_cf_net_inc` | MATRIX | 0.833 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income as reported in the cash flow statement (starting point for operating cash flow) |
| 36 | `fnd72_s_pit_or_is_a_is_inc_bef_xo_item` | MATRIX | 0.833 | 其他 | 0 | — | — | — | UNTESTED | Annual income (loss) from continuing operations (before extraordinary items) |
| 37 | `fnd72_s_pit_or_is_a2_inc_bef_xo_less_min_int_pref_dvd` | MATRIX | 0.833 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual income before extraordinary items, less minority interest and preferred dividends |
| 38 | `fnd72_s_pit_or_bs_a2_bs_disclosed_intangibles` | MATRIX | 0.833 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total intangible assets as reported (typically net) |
| 39 | `fnd72_s_pit_or_bs_a_bs_lt_borrow` | MATRIX | 0.832 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt obligations due beyond one year (bonds, long-term loans) |
| 40 | `fnd72_s_pit_or_is_a_is_inc_tax_exp` | MATRIX | 0.832 | 其他 | 0 | — | — | — | UNTESTED | Annual income tax expense or benefit |
| 41 | `fnd72_s_pit_or_is_a_sales_rev_turn` | MATRIX | 0.832 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual revenue (sales/turnover) |
| 42 | `fnd72_s_pit_or_cf_a_cf_cash_from_oper` | MATRIX | 0.831 | 其他 | 0 | — | — | — | UNTESTED | Annual net cash provided by operating activities |
| 43 | `fnd72_s_pit_or_bs_a_bs_other_st_liab` | MATRIX | 0.831 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other short-term liabilities not separately classified |
| 44 | `fnd72_s_pit_or_cf_a_cf_cash_from_fnc_act` | MATRIX | 0.831 | 其他 | 0 | — | — | — | UNTESTED | Annual net cash from financing activities |
| 45 | `fnd72_s_pit_or_cf_a_cf_net_chng_cash` | MATRIX | 0.831 | 其他 | 0 | — | — | — | UNTESTED | Annual net change in cash and cash equivalents |
| 46 | `fnd72_s_pit_or_bs_a_bs_sh_cap_and_apic` | MATRIX | 0.831 | 其他 | 0 | — | — | — | UNTESTED | Share capital plus additional paid in capital, annual |
| 47 | `fnd72_s_pit_or_cf_a_cf_cash_from_inv_act` | MATRIX | 0.831 | 其他 | 0 | — | — | — | UNTESTED | Annual net cash from investing activities |
| 48 | `fnd72_s_pit_or_is_a_is_net_non_oper_loss` | MATRIX | 0.831 | 其他 | 0 | — | — | — | UNTESTED | Annual net non-operating losses or gains |
| 49 | `fnd72_s_pit_or_is_a_is_tot_cash_pfd_dvd` | MATRIX | 0.831 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual total cash preferred dividends |
| 50 | `fnd72_s_pit_or_bs_a_bs_other_lt_liabilities` | MATRIX | 0.830 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other long-term liabilities |
| 51 | `fnd72_s_pit_or_is_a3_xo_gl_net_of_tax` | MATRIX | 0.830 | 其他 | 0 | — | — | — | UNTESTED | Annual extraordinary gains or losses net of tax |
| 52 | `fnd72_s_pit_or_bs_a_minority_noncontrolling_interest` | MATRIX | 0.830 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual balance sheet amount of minority (non‑controlling) interest in equity |
| 53 | `fnd72_a_bs_net_fix_asset` | MATRIX | 0.830 | 盈利与财务 | 0 | — | — | — | UNTESTED | Property, plant and equipment, net of accumulated depreciation |
| 54 | `fnd72_s_pit_or_is_a_is_sga_other_op_depr_op_maint` | MATRIX | 0.829 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Operating expenses comprising SG&A and other operating depreciation and maintenance for the year |
| 55 | `fnd72_s_pit_or_bs_a_yqe_dfp_sb` | MATRIX | 0.827 | 盈利与财务 | 0 | — | — | — | UNTESTED | Preferred equity (preferred stock) |
| 56 | `fnd72_s_pit_or_bs_a2_bs_goodwill` | MATRIX | 0.826 | 其他 | 0 | — | — | — | UNTESTED | Goodwill (Balance Sheet) |
| 57 | `fnd72_s_pit_or_is_a_min_noncontrol_interest_credits` | MATRIX | 0.826 | 风险与质量 | 0 | — | — | — | UNTESTED | Annual minority/noncontrolling interest credits |
| 58 | `fnd72_s_pit_or_bs_a_bs_def_tax_liab` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | Deferred tax liabilities |
| 59 | `fnd72_s_pit_or_cf_a_cf_cap_expend_prpty_add` | MATRIX | 0.825 | 其他 | 0 | — | — | — | UNTESTED | Annual capital expenditures / property additions |
| 60 | `fnd72_s_pit_or_bs_a_bs_st_borrow` | MATRIX | 0.825 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term borrowings and debt due within one year |
| 61 | `fnd72_s_pit_or_cf_a_cf_other_non_cash_adjust` | MATRIX | 0.825 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other non-cash adjustments impacting cash flow (sector-specific items such as gains/losses, deferred taxes, etc.) (annual) |
| 62 | `fnd72_s_pit_or_is_a_is_abnormal_item` | MATRIX | 0.824 | 其他 | 0 | — | — | — | UNTESTED | Annual abnormal or exceptional items (gains or losses) |
| 63 | `fnd72_s_pit_or_bs_a_bs_sh_out` | MATRIX | 0.823 | 其他 | 0 | — | — | — | UNTESTED | Total number of shares outstanding excluding treasury shares |
| 64 | `dividends_paid_cashflow_2` | MATRIX | 0.823 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total cash dividends paid during the reporting period. |
| 65 | `fnd72_s_pit_or_is_a_spe_si` | MATRIX | 0.822 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share (annual) |
| 66 | `fnd72_s_pit_or_is_a_is_diluted_eps` | MATRIX | 0.822 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual diluted earnings per share |
| 67 | `fnd72_s_pit_or_is_a_is_earn_bef_xo_items_per_sh` | MATRIX | 0.822 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share from continuing operations excluding extraordinary items |
| 68 | `fnd72_s_pit_or_is_a_is_avg_num_sh_for_eps` | MATRIX | 0.822 | 其他 | 0 | — | — | — | UNTESTED | Annual basic weighted average number of shares used for EPS |
| 69 | `fnd72_s_pit_or_is_a_is_sh_for_diluted_eps` | MATRIX | 0.822 | 其他 | 0 | — | — | — | UNTESTED | Diluted weighted average shares used to compute diluted EPS (annual) |
| 70 | `fnd72_s_pit_or_is_a_is_basic_eps_cont_ops` | MATRIX | 0.822 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual basic earnings per share from continuing operations, adjusted |
| 71 | `fnd72_s_pit_or_is_a_is_tax_eff_on_abnormal_item` | MATRIX | 0.821 | 其他 | 0 | — | — | — | UNTESTED | Tax effects on abnormal items (annual) |
| 72 | `fnd72_s_pit_or_cf_a_cf_other_inv_act` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual other investing activities (cash flow) |
| 73 | `fnd72_s_pit_or_is_a_is_dil_eps_cont_ops` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual diluted earnings per share from continuing operations, adjusted |
| 74 | `fnd72_s_pit_or_is_a_is_net_inc_avail_com_shrhldrs` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual net income available to common shareholders |
| 75 | `fnd72_s_pit_or_is_a_ox_feb_spe_lid_si` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted earnings per share before extraordinary items |
| 76 | `fnd72_s_pit_or_cf_a_cf_other_fnc_act` | MATRIX | 0.815 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other financing activities (cash flow) |
| 77 | `fnd72_s_pit_or_cf_a_cf_incr_cap_stock` | MATRIX | 0.814 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Annual cash inflow from issuance of capital stock |
| 78 | `fnd72_s_pit_or_is_a_is_xo_loss_bef_tax_eff` | MATRIX | 0.814 | 其他 | 0 | — | — | — | UNTESTED | Extraordinary loss before tax effect |
| 79 | `fnd72_s_pit_or_cf_a_cf_depr_amort` | MATRIX | 0.812 | 其他 | 0 | — | — | — | UNTESTED | Annual depreciation and amortization expense (non-cash add-back) |
| 80 | `fnd72_s_pit_or_is_a3_tot_int_exp` | MATRIX | 0.811 | 其他 | 0 | — | — | — | UNTESTED | Annual total interest expense incurred |
| 81 | `fnd72_s_pit_or_cf_a_cf_decr_cap_stock` | MATRIX | 0.811 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Cash outflow from reduction of capital stock, such as share repurchases or redemptions |
| 82 | `fnd72_s_pit_or_is_a_is_div_per_shr` | MATRIX | 0.810 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual dividend per share |
| 83 | `fnd72_s_pit_or_is_a_is_comprehensive_income` | MATRIX | 0.808 | 其他 | 0 | — | — | — | UNTESTED | Annual comprehensive income including other comprehensive income |
| 84 | `fnd72_s_pit_or_cf_a_cf_chng_non_cash_work_cap` | MATRIX | 0.806 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in non-cash working capital (operating cash flow adjustment) |
| 85 | `fnd72_s_pit_or_bs_a2_bs_pure_retained_earnings` | MATRIX | 0.805 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings (accumulated deficit) |
| 86 | `fnd72_s_pit_or_is_a_is_tot_cash_com_dvd` | MATRIX | 0.803 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual total cash dividends paid to common shareholders |
| 87 | `fnd72_s_pit_or_is_a2_is_comprehensive_income_per_shr` | MATRIX | 0.798 | 其他 | 0 | — | — | — | UNTESTED | Comprehensive income per share |
| 88 | `fnd72_s_pit_or_is_a_is_other_adj_comp_inc` | MATRIX | 0.790 | 其他 | 0 | — | — | — | UNTESTED | Other adjustments to other comprehensive income |
| 89 | `fnd72_pit_or_is_a_pxe_rped_si` | VECTOR | 0.788 | 其他 | 0 | — | — | — | UNTESTED | Depreciation Expense |
| 90 | `fnd72_s_pit_or_is_a3_net_non_oper_loss` | MATRIX | 0.782 | 其他 | 0 | — | — | — | UNTESTED | Net non-operating loss or gain |
| 91 | `fnd72_s_pit_or_bs_a_bs_lt_invest` | MATRIX | 0.774 | 其他 | 0 | — | — | — | UNTESTED | Long-term investments and receivables (balance sheet, annual) |
| 92 | `fnd72_s_pit_or_cf_a_cf_cash_paid_for_tax` | MATRIX | 0.771 | 其他 | 0 | — | — | — | UNTESTED | Annual actual cash paid for income taxes |
| 93 | `fnd72_s_pit_or_cf_a_cf_decr_invest` | MATRIX | 0.765 | 其他 | 0 | — | — | — | UNTESTED | Annual decrease in investments (proceeds from sales/maturities) |
| 94 | `fnd72_s_pit_or_cf_a_cf_reimb_lt_borrow` | MATRIX | 0.765 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Annual cash outflow for repayment of long-term borrowings |
| 95 | `fnd72_s_pit_or_bs_a_bs_mkt_sec_other_st_invest` | MATRIX | 0.760 | 其他 | 0 | — | — | — | UNTESTED | Marketable securities and other short-term investments |
| 96 | `fnd72_s_pit_or_is_a_is_personnel_exp` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | Annual personnel expenses (staff costs) |
| 97 | `fnd72_s_pit_or_is_a2_is_expense_stock_based_comp` | MATRIX | 0.756 | 其他 | 0 | — | — | — | UNTESTED | Expense for stock-based compensation |
| 98 | `fnd72_s_pit_or_is_a_pxe_rped_si` | MATRIX | 0.755 | 其他 | 0 | — | — | — | UNTESTED | Annual depreciation expenses |
| 99 | `fnd72_s_pit_or_is_a3_is_interest_inc` | MATRIX | 0.754 | 其他 | 0 | — | — | — | UNTESTED | Annual interest income |
| 100 | `fnd72_s_pit_or_is_a_cni_tni_si` | MATRIX | 0.754 | 其他 | 0 | — | — | — | UNTESTED | Interest income earned during the period (income statement) |
| 101 | `fnd72_s_pit_or_is_a_ebit` | MATRIX | 0.754 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual earnings before interest and taxes |
| 102 | `fnd72_s_pit_or_is_a_is_foreign_crncy_trans_adj` | MATRIX | 0.749 | 宏观与行业 | 0 | — | — | — | UNTESTED | Annual foreign currency translation adjustment recorded in other comprehensive income |
| 103 | `fnd72_s_pit_or_cf_a_cf_incr_invest` | MATRIX | 0.748 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Annual increase in investments (cash outflow for purchases) |
| 104 | `fnd72_s_pit_or_is_a_ebitda` | MATRIX | 0.747 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual earnings before interest, taxes, depreciation, and amortization |
| 105 | `fnd72_a_cf_disp_fix_asset` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual cash proceeds from disposal of fixed assets |
| 106 | `fnd72_s_pit_or_bs_a_hs_yst_fo_mun_sb` | MATRIX | 0.743 | 其他 | 0 | — | — | — | UNTESTED | Number of treasury shares |
| 107 | `fnd72_s_pit_or_bs_a_bs_invest_in_assoc_co` | MATRIX | 0.741 | 其他 | 0 | — | — | — | UNTESTED | Investment in associate companies |
| 108 | `fnd72_s_pit_or_bs_a_bs_acct_note_rcv` | MATRIX | 0.732 | 其他 | 0 | — | — | — | UNTESTED | Accounts and notes receivable |
| 109 | `fnd72_s_pit_or_is_a2_other_adjustments` | MATRIX | 0.732 | 其他 | 0 | — | — | — | UNTESTED | Annual other adjustments reported on the income statement |
| 110 | `fnd72_s_pit_or_is_a_is_tax_eff_on_xo_item` | MATRIX | 0.730 | 其他 | 0 | — | — | — | UNTESTED | Annual tax effect associated with extraordinary items |
| 111 | `fnd72_s_pit_or_bs_a_bs_cur_asset_report` | MATRIX | 0.730 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current assets |
| 112 | `fnd72_s_pit_or_bs_a_bs_cur_liab` | MATRIX | 0.730 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current liabilities |
| 113 | `fnd72_s_pit_or_is_a_is_int_expense` | MATRIX | 0.725 | 其他 | 0 | — | — | — | UNTESTED | Annual interest expense |
| 114 | `fnd72_s_pit_or_bs_a_bs_pension_rsrv` | MATRIX | 0.725 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pension and postretirement liabilities |
| 115 | `fnd72_s_pit_or_is_a_is_invest_income` | MATRIX | 0.715 | 其他 | 0 | — | — | — | UNTESTED | Annual net investment income |
| 116 | `fnd72_pit_or_bs_a_announcement_dt` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Latest full earnings report date for which complete fundamentals are available |
| 117 | `fnd72_pit_or_bs_a_fundamental_entry_dt` | VECTOR | 0.714 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Date when the fundamental data point was entered |
| 118 | `fnd72_pit_or_bs_a_latest_period_end_dt_full_record` | VECTOR | 0.714 | 其他 | 0 | — | — | — | UNTESTED | Latest available period end date from full financial records |
| 119 | `fnd72_pit_or_bs_a_bs_cash_near_cash_item` | VECTOR | 0.714 | 其他 | 0 | — | — | — | UNTESTED | Cash and cash equivalents |
| 120 | `fnd72_pit_or_bs_a_bs_tot_asset` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets on the balance sheet |
| 121 | `fnd72_pit_or_is_a_announcement_dt` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quarterly latest full earnings report date |
| 122 | `fnd72_pit_or_is_a_fundamental_entry_dt` | VECTOR | 0.714 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Date when the fundamental data point was entered into the system |
| 123 | `fnd72_pit_or_is_a_id_bb_global` | VECTOR | 0.714 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Bloomberg Financial Instrument Global Identifier |
| 124 | `fnd72_pit_or_is_a_latest_period_end_dt_full_record` | VECTOR | 0.714 | 其他 | 0 | — | — | — | UNTESTED | Latest available period end date from full financial records |
| 125 | `fnd72_pit_or_bs_a_bs_retain_earn` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings and other equity components |
| 126 | `fnd72_pit_or_cf_a_announcement_dt` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Date of the latest earnings announcement for which full fundamental information is available |
| 127 | `fnd72_pit_or_cf_a_fundamental_entry_dt` | VECTOR | 0.714 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Date the fundamental data was entered into the system |
| 128 | `fnd72_pit_or_cf_a_id_bb_global` | VECTOR | 0.714 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Financial Instrument Global Identifier (Bloomberg global ID linking the record across systems) |
| 129 | `fnd72_pit_or_cf_a_latest_period_end_dt_full_record` | VECTOR | 0.714 | 其他 | 0 | — | — | — | UNTESTED | Latest available period end date from the full financial records |
| 130 | `fnd72_pit_or_bs_a_bs_other_asset_def_chng_other` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other long-term assets |
| 131 | `fnd72_pit_or_is_a_is_oper_inc` | VECTOR | 0.714 | 其他 | 0 | — | — | — | UNTESTED | Operating income (or loss) |
| 132 | `fnd72_pit_or_is_a_net_income` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income (net profit or loss) for the period |
| 133 | `fnd72_pit_or_cf_a_cf_net_inc` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income as presented on the cash flow statement, the starting point for operating cash flows |
| 134 | `fnd72_pit_or_is_a_earn_for_common` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income available to common shareholders for the quarter |
| 135 | `fnd72_pit_or_is_a_inc_bef_xo_less_min_int_pref_dvd` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income before extraordinary items after minority interest and preferred dividends |
| 136 | `fnd72_pit_or_is_a_is_inc_bef_xo_item` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings from continuing operations before extraordinary items and discontinued operations |
| 137 | `fnd72_pit_or_is_a_net_income_bef_mi` | VECTOR | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income before minority interest |
| 138 | `fnd72_pit_or_is_a_pretax_inc` | VECTOR | 0.714 | 其他 | 0 | — | — | — | UNTESTED | Income before income taxes for the period |
| 139 | `fnd72_pit_or_is_a_is_inc_tax_exp` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Income tax expense or benefit for the quarter |
| 140 | `fnd72_pit_or_bs_a_bs_disclosed_intangibles` | VECTOR | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net carrying value of disclosed intangible assets |
| 141 | `fnd72_pit_or_bs_a_bs_lt_borrow` | VECTOR | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total long-term debt obligations due beyond one year |
| 142 | `fnd72_pit_or_is_a_sales_rev_turn` | VECTOR | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sales or revenue for the period |
| 143 | `fnd72_pit_or_cf_a_cf_cash_from_oper` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Net cash provided by (used in) operating activities |
| 144 | `fnd72_pit_or_bs_a_bs_sh_cap_and_apic` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Share capital at par plus additional paid-in capital |
| 145 | `fnd72_pit_or_cf_a_cf_cash_from_fnc_act` | VECTOR | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quarterly total cash flows from financing activities |
| 146 | `fnd72_pit_or_cf_a_cf_cash_from_inv_act` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Net cash provided by (used in) investing activities |
| 147 | `fnd72_pit_or_cf_a_cf_net_chng_cash` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Net change in cash and cash equivalents for the period |
| 148 | `fnd72_pit_or_is_a_is_tot_cash_pfd_dvd` | VECTOR | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total cash preferred dividends |
| 149 | `fnd72_pit_or_is_a_xo_gl_net_of_tax` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Net extraordinary gains or losses after tax |
| 150 | `fnd72_pit_or_bs_a_bs_other_st_liab` | VECTOR | 0.713 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other current liabilities not otherwise classified, due within one year |
| 151 | `fnd72_pit_or_is_a_is_net_non_oper_loss` | VECTOR | 0.713 | 其他 | 0 | — | — | — | UNTESTED | Net non-operating losses or gains for the period |
| 152 | `fnd72_pit_or_bs_a_bs_other_lt_liabilities` | VECTOR | 0.712 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other long-term liabilities |
| 153 | `fnd72_pit_or_is_a_min_noncontrol_interest_credits` | VECTOR | 0.712 | 风险与质量 | 0 | — | — | — | UNTESTED | Minority/noncontrolling interest credits (share of income attributable to minority interests) |
| 154 | `fnd72_pit_or_bs_a_minority_noncontrolling_interest` | VECTOR | 0.712 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity attributable to non-controlling interests in subsidiaries |
| 155 | `fnd72_pit_or_is_a_is_sga_other_op_depr_op_maint` | VECTOR | 0.712 | 其他 | 0 | — | — | — | UNTESTED | Operating expenses including selling, general and administrative, other operating depreciation, and maintenance |
| 156 | `fnd72_pit_or_bs_a_bs_net_fix_asset` | VECTOR | 0.711 | 盈利与财务 | 0 | — | — | — | UNTESTED | Property, plant and equipment net of accumulated depreciation |
| 157 | `fnd72_pit_or_cf_a_cf_other_non_cash_adjust` | VECTOR | 0.711 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other non-cash adjustments included in operating cash flow (e.g., gains/losses, deferred taxes) |
| 158 | `fnd72_pit_or_bs_a_bs_def_tax_liab` | VECTOR | 0.711 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term net deferred tax liabilities |
| 159 | `fnd72_pit_or_bs_a_bs_pfd_eqy` | VECTOR | 0.711 | 盈利与财务 | 0 | — | — | — | UNTESTED | Preferred equity (preferred stock) outstanding |
| 160 | `fnd72_pit_or_bs_a_bs_goodwill` | VECTOR | 0.711 | 盈利与财务 | 0 | — | — | — | UNTESTED | Goodwill intangible asset from acquisitions |
| 161 | `fnd72_pit_or_cf_a_cf_cap_expend_prpty_add` | VECTOR | 0.710 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Capital expenditures or property additions (cash outflows for PP&E) |
| 162 | `fnd72_s_pit_or_bs_a_bs_tot_liab_eqy` | MATRIX | 0.710 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total liabilities and equity |
| 163 | `total_noncurrent_assets_value_2` | MATRIX | 0.710 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value of noncurrent assets. |
| 164 | `fnd72_pit_or_cf_a_cf_other_inv_act` | VECTOR | 0.710 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other investing cash flows not classified elsewhere |
| 165 | `dividends_paid_cash_flow` | VECTOR | 0.710 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash outflow for dividends paid to shareholders. |
| 166 | `fnd72_pit_or_bs_a_bs_sh_out` | VECTOR | 0.709 | 其他 | 0 | — | — | — | UNTESTED | Shares outstanding at period end |
| 167 | `fnd72_pit_or_is_a_is_xo_loss_bef_tax_eff` | VECTOR | 0.709 | 其他 | 0 | — | — | — | UNTESTED | Extraordinary gains or losses before tax effects |
| 168 | `fnd72_pit_or_is_a_is_eps` | VECTOR | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share for the quarter |
| 169 | `fnd72_pit_or_is_a_is_avg_num_sh_for_eps` | VECTOR | 0.709 | 其他 | 0 | — | — | — | UNTESTED | Quarterly basic weighted average number of shares used for EPS calculation |
| 170 | `fnd72_pit_or_is_a_is_earn_bef_xo_items_per_sh` | VECTOR | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share from continuing operations (before extraordinary items) |
| 171 | `fnd72_pit_or_is_a_is_abnormal_item` | VECTOR | 0.709 | 其他 | 0 | — | — | — | UNTESTED | Gross amount of abnormal or exceptional gains or losses recognized during the period |
| 172 | `fnd72_pit_or_is_a_is_diluted_eps` | VECTOR | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted earnings per share |
| 173 | `fnd72_pit_or_is_a_is_sh_for_diluted_eps` | VECTOR | 0.709 | 其他 | 0 | — | — | — | UNTESTED | Diluted weighted average shares used in EPS calculation |
| 174 | `fnd72_pit_or_is_a_is_basic_eps_cont_ops` | VECTOR | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic earnings per share from continuing operations, adjusted |
| 175 | `fnd72_pit_or_bs_a_bs_st_borrow` | VECTOR | 0.708 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term borrowings and debt due within one year |
| 176 | `fnd72_pit_or_cf_a_cf_other_fnc_act` | VECTOR | 0.708 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other cash flows from financing activities not captured in specific financing line items |
| 177 | `fnd72_s_pit_or_cf_a_cf_incr_lt_borrow` | MATRIX | 0.707 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Annual cash proceeds from increases in long-term borrowings |
| 178 | `fnd72_pit_or_is_a_is_dil_eps_cont_ops` | VECTOR | 0.707 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted earnings per share from continuing operations, adjusted |
| 179 | `fnd72_pit_or_is_a_is_tax_eff_on_abnormal_item` | VECTOR | 0.707 | 其他 | 0 | — | — | — | UNTESTED | Tax effects related to abnormal or extraordinary items |
| 180 | `fnd72_s_pit_or_bs_a_bs_tot_eqy` | MATRIX | 0.706 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total equity |
| 181 | `fnd72_pit_or_cf_a_cf_incr_cap_stock` | VECTOR | 0.706 | 其他 | 0 | — | — | — | UNTESTED | Proceeds from issuing share capital |
| 182 | `fnd72_pit_or_is_a_is_dil_eps_bef_xo` | VECTOR | 0.705 | 其他 | 0 | — | — | — | UNTESTED | Diluted EPS before extraordinary items (from continuing operations) |
| 183 | `fnd72_pit_or_is_a_is_div_per_shr` | VECTOR | 0.704 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share for the period |
| 184 | `fnd72_pit_or_cf_a_cf_decr_cap_stock` | VECTOR | 0.704 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Cash outflows from reductions in share capital, including share repurchases |
| 185 | `fnd72_pit_or_bs_a_bs_pure_retained_earnings` | VECTOR | 0.702 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings (accumulated profits/losses) |
| 186 | `fnd72_pit_or_is_a_tot_int_exp` | VECTOR | 0.701 | 其他 | 0 | — | — | — | UNTESTED | Quarterly total interest expense incurred |
| 187 | `fnd72_pit_or_cf_a_cf_depr_amort` | VECTOR | 0.701 | 盈利与财务 | 0 | — | — | — | UNTESTED | Depreciation and amortization addback on the cash flow statement |
| 188 | `total_assets_amt` | VECTOR | 0.701 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sum of all assets owned by the company. |
| 189 | `fnd72_pit_or_cf_a_cf_chng_non_cash_work_cap` | VECTOR | 0.700 | 其他 | 0 | — | — | — | UNTESTED | Change in non-cash working capital (e.g., receivables, inventory, payables) |
| 190 | `fnd72_pit_or_is_a_is_tot_cash_com_dvd` | VECTOR | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total cash common dividends |
| 191 | `fnd72_pit_or_is_a_is_net_inc_avail_com_shrhldrs` | VECTOR | 0.700 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income attributable to common shareholders (after preferred dividends) |
| 192 | `fnd72_pit_or_is_a_is_comprehensive_income` | VECTOR | 0.698 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total comprehensive income including net income and other comprehensive income |
| 193 | `fnd72_s_pit_or_bs_a_bs_acct_payable` | MATRIX | 0.697 | 价量与波动 | 0 | — | — | — | UNTESTED | Accounts payable (trade and other payables) |
| 194 | `fnd72_s_pit_or_is_a_eff_int_rate` | MATRIX | 0.697 | 盈利与财务 | 0 | — | — | — | UNTESTED | Effective interest rate percentage calculated as total interest incurred divided by average short and long-term debt |
| 195 | `fnd72_s_pit_or_bs_a_bs_amt_of_tsy_stock` | MATRIX | 0.694 | 其他 | 0 | — | — | — | UNTESTED | Amount of treasury stock |
| 196 | `fnd72_pit_or_is_a_is_comprehensive_income_per_shr` | VECTOR | 0.693 | 其他 | 0 | — | — | — | UNTESTED | Quarterly comprehensive income per share |
| 197 | `fnd72_s_pit_or_cf_a_cf_act_cash_paid_for_int_debt` | MATRIX | 0.693 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual actual cash paid for interest on debt |
| 198 | `fnd72_pit_or_cf_a_cf_reimb_lt_borrow` | VECTOR | 0.691 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Repayments of long-term borrowings |
| 199 | `fnd72_is_a_eqy_fund_crncy` | VECTOR | 0.690 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Currency in which the fundamental data is reported |
| 200 | `fnd72_bs_a_eqy_fund_crncy` | VECTOR | 0.690 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Currency in which the fundamental data is reported |
| 201 | `fnd72_s_pit_or_bs_a_bs_accum_depr` | MATRIX | 0.690 | 其他 | 0 | — | — | — | UNTESTED | Accumulated depreciation (balance sheet, annual) |
| 202 | `fnd72_pit_or_is_a_is_other_adj_comp_inc` | VECTOR | 0.689 | 其他 | 0 | — | — | — | UNTESTED | Other adjustments to other comprehensive income for the period |
| 203 | `fnd72_pit_or_is_a_is_tax_eff_on_xo_item` | VECTOR | 0.688 | 其他 | 0 | — | — | — | UNTESTED | Tax effect related to extraordinary items |
| 204 | `property_plant_equipment_net_annual` | VECTOR | 0.688 | 其他 | 0 | — | — | — | UNTESTED | Net value of property, plant, and equipment after depreciation, as reported in annual statements. |
| 205 | `fnd72_cf_a_eqy_fund_crncy` | VECTOR | 0.687 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Currency in which the fundamental data is reported |
| 206 | `fnd72_pit_or_is_a_cni_tni_si` | VECTOR | 0.687 | 其他 | 0 | — | — | — | UNTESTED | Interest Income |
| 207 | `fnd72_s_pit_or_bs_a_bs_other_cur_asset` | MATRIX | 0.685 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual balance sheet value of other current assets |
| 208 | `fnd72_pit_or_cf_a_cf_decr_invest` | VECTOR | 0.684 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Proceeds from sales or maturities of investments (decrease in investment holdings) |
| 209 | `fnd72_pit_or_cf_a_cf_disp_fix_asset` | VECTOR | 0.684 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash proceeds from disposal of fixed assets |
| 210 | `fnd72_s_pit_or_is_a_is_min_pension_liab_adj` | MATRIX | 0.683 | 其他 | 0 | — | — | — | UNTESTED | Annual pension-related adjustment to other comprehensive income |
| 211 | `fnd72_s_pit_or_bs_a_bs_inventories` | MATRIX | 0.680 | 其他 | 0 | — | — | — | UNTESTED | Inventories of raw materials, work-in-progress, and finished goods |
| 212 | `fnd72_s_pit_or_is_a_is_other_oper_inc` | MATRIX | 0.680 | 其他 | 0 | — | — | — | UNTESTED | Annual other operating income |
| 213 | `fnd72_s_pit_or_is_a_is_unrealized_gain_loss_comp_inc` | MATRIX | 0.680 | 其他 | 0 | — | — | — | UNTESTED | Unrealized gains/losses recorded in other comprehensive income (annual) |
| 214 | `fnd72_pit_or_bs_a_bs_lt_invest` | VECTOR | 0.679 | 其他 | 0 | — | — | — | UNTESTED | Long-term investments and receivables reported on the balance sheet |
| 215 | `fnd72_pit_or_cf_a_cf_cash_paid_for_tax` | VECTOR | 0.679 | 其他 | 0 | — | — | — | UNTESTED | Cash taxes paid during the period |
| 216 | `shareholders_equity_total_amt` | VECTOR | 0.678 | 盈利与财务 | 0 | — | — | — | UNTESTED | Aggregate value of shareholders' equity. |
| 217 | `fnd72_pit_or_bs_a_bs_invest_in_assoc_co` | VECTOR | 0.678 | 盈利与财务 | 0 | — | — | — | UNTESTED | Investments in associate or affiliate companies (equity method) |
| 218 | `fnd72_s_pit_or_bs_a2_bs_capital_reserve` | MATRIX | 0.676 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital reserves or other equity reserves (e.g., capital surplus or additional paid-in capital) |
| 219 | `fnd72_s_pit_or_bs_a_bs_par_val` | MATRIX | 0.676 | 其他 | 0 | — | — | — | UNTESTED | Par value of issued shares |
| 220 | `fnd72_pit_or_cf_a_cf_incr_lt_borrow` | VECTOR | 0.675 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Proceeds from issuance of long-term borrowings |
| 221 | `total_liabilities_and_equity_value` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value of liabilities and shareholders' equity. |
| 222 | `fnd72_pit_or_is_a_is_expense_stock_based_comp` | VECTOR | 0.673 | 其他 | 0 | — | — | — | UNTESTED | Total stock-based compensation expense recognized in the period |
| 223 | `fnd72_pit_or_is_a_net_non_oper_loss` | VECTOR | 0.672 | 其他 | 0 | — | — | — | UNTESTED | Quarterly net non-operating loss or gain for the period |
| 224 | `fnd72_pit_or_bs_a_bs_mkt_sec_other_st_invest` | VECTOR | 0.671 | 其他 | 0 | — | — | — | UNTESTED | Marketable securities and other short-term investments |
| 225 | `fnd72_pit_or_cf_a_cf_incr_invest` | VECTOR | 0.670 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Increase in investments (purchases of investments), cash outflow |
| 226 | `fnd72_s_pit_or_is_a2_is_net_interest_expense` | MATRIX | 0.669 | 其他 | 0 | — | — | — | UNTESTED | Net interest expense after offsetting interest income |
| 227 | `fnd72_s_pit_or_cf_a_cf_other_non_cash_adj_less` | MATRIX | 0.668 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other non-cash adjustments, excluding specified items (cash flow statement) |
| 228 | `fnd72_pit_or_is_a_is_personnel_exp` | VECTOR | 0.668 | 其他 | 0 | — | — | — | UNTESTED | Personnel expenses such as wages and benefits for the period |
| 229 | `fnd72_pit_or_is_a_is_depr_exp` | VECTOR | 0.668 | 其他 | 0 | — | — | — | UNTESTED | Quarterly depreciation expense |
| 230 | `fnd72_a_bs_gross_fix_asset` | MATRIX | 0.667 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross property, plant and equipment, annual |
| 231 | `fnd72_pit_or_bs_a_bs_num_of_tsy_sh` | VECTOR | 0.667 | 其他 | 0 | — | — | — | UNTESTED | Number of shares held in treasury by the company |
| 232 | `fnd72_pit_or_is_a_is_foreign_crncy_trans_adj` | VECTOR | 0.665 | 宏观与行业 | 0 | — | — | — | UNTESTED | Quarterly foreign currency translation adjustment recognized in other comprehensive income |
| 233 | `fnd72_pit_or_is_a_is_int_inc` | VECTOR | 0.662 | 其他 | 0 | — | — | — | UNTESTED | Interest income earned during the period |
| 234 | `fnd72_pit_or_is_a_is_interest_inc` | VECTOR | 0.662 | 其他 | 0 | — | — | — | UNTESTED | Interest income for the quarter |
| 235 | `fnd72_s_pit_or_bs_a2_bs_accts_rec_excl_notes_rec` | MATRIX | 0.655 | 其他 | 0 | — | — | — | UNTESTED | Accounts receivable, net (excluding notes receivable) |
| 236 | `fnd72_pit_or_is_a_is_invest_income` | VECTOR | 0.654 | 其他 | 0 | — | — | — | UNTESTED | Investment income for the period |
| 237 | `fnd72_pit_or_bs_a_bs_pension_rsrv` | VECTOR | 0.646 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pension and post-retirement benefit obligations (liability) |
| 238 | `fnd72_s_pit_or_cf_a_cf_form_of_statement` | MATRIX | 0.644 | 其他 | 0 | — | — | — | UNTESTED | No longer supported |
| 239 | `cash_and_equivalents_amt` | VECTOR | 0.644 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash and highly liquid assets held by the company. |
| 240 | `fnd72_pit_or_bs_a_bs_amt_of_tsy_stock` | VECTOR | 0.644 | 其他 | 0 | — | — | — | UNTESTED | Carrying amount of treasury stock (repurchased shares) |
| 241 | `fnd72_pit_or_bs_a_bs_acct_note_rcv` | VECTOR | 0.644 | 其他 | 0 | — | — | — | UNTESTED | Accounts and notes receivable |
| 242 | `fnd72_s_pit_or_is_a_is_foreign_exch_loss` | MATRIX | 0.643 | 其他 | 0 | — | — | — | UNTESTED | Annual foreign exchange losses or gains recognized in the income statement |
| 243 | `fnd72_pit_or_is_a_ebit` | VECTOR | 0.642 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes for the period |
| 244 | `fnd72_pit_or_is_a_is_int_expense` | VECTOR | 0.640 | 其他 | 0 | — | — | — | UNTESTED | Interest expense for the period |
| 245 | `fnd72_pit_or_is_a_is_unrealized_gain_loss_comp_inc` | VECTOR | 0.640 | 其他 | 0 | — | — | — | UNTESTED | Unrealized gains or losses recognized in other comprehensive income |
| 246 | `fnd72_pit_or_is_a_ebitda` | VECTOR | 0.638 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation, and amortization for the period |
| 247 | `fnd72_pit_or_bs_a_bs_future_min_oper_lease_oblig` | VECTOR | 0.637 | 其他 | 0 | — | — | — | UNTESTED | Future minimum payments due under operating lease obligations |
| 248 | `fnd72_pit_or_is_a_is_min_pension_liab_adj` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pension-related adjustment recorded in other comprehensive income for the period (minimum pension liability adjustment) |
| 249 | `fnd72_s_pit_or_bs_a_notes_receivable` | MATRIX | 0.637 | 其他 | 0 | — | — | — | UNTESTED | Notes receivable (balance sheet, annual) |
| 250 | `property_plant_equipment_net_a` | VECTOR | 0.635 | 其他 | 0 | — | — | — | UNTESTED | Net value of property, plant, and equipment after depreciation, as reported in annual statements. |
| 251 | `fnd72_s_pit_or_is_a_is_eqy_earn_from_invest_assoc` | MATRIX | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annual share of earnings (losses) from equity-accounted associates/affiliates |
| 252 | `fnd72_s_pit_or_is_a_ebitdar` | MATRIX | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation, amortization, and rent (annual) |
| 253 | `fnd72_pit_or_is_a_other_adjustments` | VECTOR | 0.633 | 其他 | 0 | — | — | — | UNTESTED | Other Adjustments |
| 254 | `ard_retained_earnings_accum_deficit_annual` | MATRIX | 0.630 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings or accumulated deficit in standardized ARD format (annual, duplicate field). |
| 255 | `fnd72_s_pit_or_is_a2_is_pension_expense_income` | MATRIX | 0.630 | 其他 | 0 | — | — | — | UNTESTED | Annual pension expense or income |
| 256 | `fnd72_pit_or_cf_a_cf_act_cash_paid_for_int_debt` | VECTOR | 0.628 | 盈利与财务 | 0 | — | — | — | UNTESTED | Actual cash paid for interest on debt |
| 257 | `fnd72_pit_or_is_a_is_eqy_earn_from_invest_assoc` | VECTOR | 0.626 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity income or loss from investments in associates for the quarter |
| 258 | `fnd72_s_pit_or_is_a_is_rd_expend` | MATRIX | 0.626 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Annual research and development expense |
| 259 | `other_intangible_assets_value` | MATRIX | 0.625 | 盈利与财务 | 0 | — | — | — | UNTESTED | Value of intangible assets other than goodwill. |
| 260 | `total_current_assets_amt` | VECTOR | 0.625 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value of assets expected to be converted to cash within a year. |
| 261 | `total_current_liabilities_amt` | VECTOR | 0.624 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total obligations due within one year. |
| 262 | `fnd72_pit_or_bs_a_bs_cur_asset_report` | VECTOR | 0.622 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current assets |
| 263 | `fnd72_pit_or_bs_a_bs_cur_liab` | VECTOR | 0.622 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current liabilities at the reporting date |
| 264 | `fnd72_pit_or_bs_a_bs_tot_liab_eqy` | VECTOR | 0.621 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total liabilities plus equity as presented for REITs, typically equal to total assets |
| 265 | `fnd72_pit_or_bs_a_bs_par_val` | VECTOR | 0.619 | 其他 | 0 | — | — | — | UNTESTED | Par value of issued shares |
| 266 | `gross_property_plant_equipment_2` | MATRIX | 0.619 | 其他 | 0 | — | — | — | UNTESTED | Total gross value of property, plant, and equipment before depreciation. |
| 267 | `total_noncurrent_liabilities_amt` | VECTOR | 0.617 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sum of all liabilities due beyond one year. |
| 268 | `fnd72_s_pit_or_bs_a_bs_st_debt` | MATRIX | 0.616 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term debt (balance sheet, annual) |
| 269 | `fnd72_s_pit_or_bs_a2_contingent_liabilities` | MATRIX | 0.616 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total contingent liabilities |
| 270 | `fnd72_s_pit_or_bs_a_bs_other_cur_asset_less_prepay` | MATRIX | 0.614 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other current assets excluding prepayments |
| 271 | `fnd72_pit_or_bs_a_bs_accum_depr` | VECTOR | 0.611 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accumulated depreciation on fixed assets |
| 272 | `fnd72_s_pit_or_bs_a2_bs_accrual` | MATRIX | 0.611 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other accounts payable and accrued liabilities reported on the balance sheet |
| 273 | `fnd72_pit_or_bs_a_bs_tot_eqy` | VECTOR | 0.611 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total shareholders’ equity or partnership capital |
| 274 | `goodwill_balance` | VECTOR | 0.610 | 其他 | 0 | — | — | — | UNTESTED | Value of goodwill recognized on the balance sheet. |
| 275 | `fnd72_pit_or_bs_a_bs_acct_payable` | VECTOR | 0.607 | 价量与波动 | 0 | — | — | — | UNTESTED | Accounts payable (trade payables) |
| 276 | `fnd72_pit_or_is_a_eff_int_rate` | VECTOR | 0.607 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective interest rate |
| 277 | `inventory_value_total_3` | MATRIX | 0.607 | 其他 | 0 | — | — | — | UNTESTED | Total value of inventory reported on the balance sheet. |
| 278 | `total_noncurrent_assets_2` | VECTOR | 0.606 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sum of all assets expected to provide value beyond one year. |
| 279 | `fnd72_pit_or_is_a_is_other_oper_inc` | VECTOR | 0.603 | 其他 | 0 | — | — | — | UNTESTED | Other operating income |
| 280 | `fnd72_pit_or_is_a_is_pension_expense_income` | VECTOR | 0.602 | 其他 | 0 | — | — | — | UNTESTED | Pension expense or income recognized for the period |
| 281 | `fnd72_s_pit_or_is_a_is_special_eps` | MATRIX | 0.599 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Annual special earnings per share |
| 282 | `shareholders_equity_total_value` | MATRIX | 0.598 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total value of shareholders' equity. |
| 283 | `fnd72_s_pit_or_is_a_is_inc_tax_exp_other_comp_inc` | MATRIX | 0.598 | 其他 | 0 | — | — | — | UNUSABLE | Annual income tax expense related to other comprehensive income |
| 284 | `fnd72_s_pit_or_bs_a2_num_outlets_branches` | MATRIX | 0.595 | 其他 | 0 | — | — | — | UNUSABLE | Number of outlets and branches |
| 285 | `fnd72_pit_or_bs_a_contingent_liabilities` | VECTOR | 0.595 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total contingent liabilities and commitments dependent on future events |
| 286 | `fnd72_pit_or_bs_a_bs_total_capital_leases` | VECTOR | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Total capital lease obligations |
| 287 | `fnd72_s_pit_or_bs_a2_invtry_finished_goods` | MATRIX | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Finished goods inventory |
| 288 | `fnd72_s_pit_or_bs_a2_invtry_raw_materials` | MATRIX | 0.590 | 其他 | 0 | — | — | — | UNUSABLE | Value of raw materials inventory |
| 289 | `fnd72_pit_or_is_a_is_net_interest_expense` | VECTOR | 0.589 | 其他 | 0 | — | — | — | UNUSABLE | Net interest expense (interest expense minus interest income) |
| 290 | `fnd72_s_pit_or_bs_a2_bs_other_cur_liab` | MATRIX | 0.588 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current liabilities (Balance Sheet) |
| 291 | `fnd72_pit_or_bs_a_bs_gross_fix_asset` | VECTOR | 0.587 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross property, plant, and equipment before accumulated depreciation |
| 292 | `fnd72_pit_or_bs_a_bs_capital_reserve` | VECTOR | 0.584 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Capital reserve within equity (other equity reserves such as share premium or legal reserves) |
| 293 | `fnd72_pit_or_bs_a_bs_other_cur_asset` | VECTOR | 0.584 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current assets |
| 294 | `total_liabilities_and_equity_8` | VECTOR | 0.583 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total of all liabilities and shareholders' equity. |
| 295 | `fnd72_s_pit_or_bs_a2_bs_other_inv` | MATRIX | 0.582 | 其他 | 0 | — | — | — | UNUSABLE | Other inventory and allowances |
| 296 | `other_intangibles_other_amt` | VECTOR | 0.582 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other intangible assets as reported in alternate statement formats. |
| 297 | `fnd72_pit_or_cf_a_cf_other_non_cash_adj_less` | VECTOR | 0.582 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other non-cash adjustments (reductions) used to reconcile net income to cash from operations, excluding specified items |
| 298 | `fnd72_pit_or_is_a_is_inc_tax_exp_other_comp_inc` | VECTOR | 0.582 | 其他 | 0 | — | — | — | UNUSABLE | Income tax expense on other comprehensive income |
| 299 | `fnd72_s_pit_or_bs_a2_invtry_in_progress` | MATRIX | 0.581 | 其他 | 0 | — | — | — | UNUSABLE | Work-in-process inventory |
| 300 | `fnd72_pit_or_bs_a_bs_inventories` | VECTOR | 0.581 | 其他 | 0 | — | — | — | UNUSABLE | Inventory balances held by the company |
| 301 | `trade_accounts_receivable_value` | MATRIX | 0.579 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of trade accounts receivable. |
| 302 | `fnd72_pit_or_cf_a_cf_issue_com_stock` | VECTOR | 0.578 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Cash inflow from issuance of common stock |
| 303 | `retained_earnings_or_accum_deficit` | VECTOR | 0.576 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cumulative net income retained or deficit accumulated by the company. |
| 304 | `fnd72_pit_or_bs_a_bs_lifo_reserve` | VECTOR | 0.575 | 其他 | 0 | — | — | — | UNUSABLE | LIFO reserve |
| 305 | `plant_and_equipment_net` | VECTOR | 0.575 | 其他 | 0 | — | — | — | UNUSABLE | Net value of plant and equipment after depreciation. |
| 306 | `property_plant_equipment_gross_amt` | VECTOR | 0.574 | 其他 | 0 | — | — | — | UNUSABLE | Gross value of property, plant, and equipment before depreciation. |
| 307 | `par_value_annual` | VECTOR | 0.572 | 其他 | 0 | — | — | — | UNUSABLE | Nominal value assigned to each share of stock, as reported in annual statements. |
| 308 | `common_stock_annual` | VECTOR | 0.571 | 其他 | 0 | — | — | — | UNUSABLE | Value of common stock issued and outstanding, as reported in annual statements. |
| 309 | `fnd72_s_pit_or_is_q_fundamental_entry_dt` | MATRIX | 0.570 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Fundamental data entry date for the quarter |
| 310 | `fnd72_s_pit_or_is_q_latest_period_end_dt_full_record` | MATRIX | 0.570 | 其他 | 0 | — | — | — | UNUSABLE | Latest available period end date from full financial records |
| 311 | `fnd72_s_pit_or_is_q_announcement_dt` | MATRIX | 0.569 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Latest full earnings report announcement date (quarterly) |
| 312 | `fnd72_pit_or_bs_a_lt_capital_lease_obligations` | VECTOR | 0.569 | 其他 | 0 | — | — | — | UNUSABLE | Noncurrent portion of obligations under capital/finance leases |
| 313 | `fnd72_s_pit_or_cf_a_cf_issue_com_stock` | MATRIX | 0.567 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Cash inflow from issuance of common stock |
| 314 | `fnd72_pit_or_bs_a_bs_rental_exp_year_1` | VECTOR | 0.566 | 其他 | 0 | — | — | — | UNUSABLE | Rental expense for Year 1 |
| 315 | `fnd72_pit_or_is_a_is_foreign_exch_loss` | VECTOR | 0.564 | 其他 | 0 | — | — | — | UNUSABLE | Foreign exchange losses or gains recognized in the period |
| 316 | `fnd72_pit_or_bs_a_bs_accts_rec_excl_notes_rec` | VECTOR | 0.562 | 价量与波动 | 0 | — | — | — | UNUSABLE | Trade accounts receivable excluding notes receivable, net of allowances |
| 317 | `fnd72_pit_or_is_a_ebitdar` | VECTOR | 0.562 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation, amortization, and rent |
| 318 | `fnd72_pit_or_bs_a_st_capital_lease_obligations` | VECTOR | 0.561 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current portion of capital lease liabilities due within one year |
| 319 | `fnd72_pit_or_cf_a_cf_net_cash_paid_for_aquis` | VECTOR | 0.560 | 其他 | 0 | — | — | — | UNUSABLE | Net cash paid for acquisitions |
| 320 | `fnd72_s_pit_or_cf_q_announcement_dt` | MATRIX | 0.557 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Latest full earnings report announcement date associated with the fundamental snapshot |
| 321 | `fnd72_s_pit_or_cf_q_fundamental_entry_dt` | MATRIX | 0.557 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Date the fundamental data was entered into the system |
| 322 | `fnd72_s_pit_or_cf_q_latest_period_end_dt_full_record` | MATRIX | 0.557 | 其他 | 0 | — | — | — | UNUSABLE | Latest available period end date from full financial records |
| 323 | `fnd72_pit_or_is_a_is_rd_expend` | VECTOR | 0.554 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Quarterly research and development expense |
| 324 | `fnd72_pit_or_bs_a_bs_rental_exp_beyond_year_5` | VECTOR | 0.551 | 其他 | 0 | — | — | — | UNUSABLE | Contracted rental payments due beyond Year 5 under operating lease commitments |
| 325 | `fnd72_pit_or_bs_a_bs_st_debt` | VECTOR | 0.548 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term debt |
| 326 | `fnd72_s_pit_or_is_a2_is_over_underfund_pension_exp` | MATRIX | 0.547 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Annual pension funded status amount (overfunded or underfunded) |
| 327 | `fnd72_pit_or_bs_a_bs_curr_rental_expense` | VECTOR | 0.547 | 其他 | 0 | — | — | — | UNUSABLE | Rental expense for the current reporting period (typically operating lease expense) |
| 328 | `total_shareholders_equity_amt` | VECTOR | 0.546 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total equity attributable to shareholders. |
| 329 | `fnd72_pit_or_is_a_ox_feb_spe_lid_si` | VECTOR | 0.546 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS Before Extraordinary Items |
| 330 | `fnd72_pit_or_bs_a_notes_receivable` | VECTOR | 0.545 | 其他 | 0 | — | — | — | UNUSABLE | Amounts owed to the company via promissory notes (notes receivable) |
| 331 | `non_equity_reserves_3` | VECTOR | 0.544 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reserves not related to equity, such as for liabilities or contingencies. |
| 332 | `fnd72_s_pit_or_is_q_sales_rev_turn` | MATRIX | 0.544 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly revenue (sales/turnover recognized) |
| 333 | `fnd72_pit_or_is_a_is_special_eps` | VECTOR | 0.543 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Special earnings per share as reported |
| 334 | `total_liabilities_amt` | VECTOR | 0.542 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sum of all liabilities reported on the balance sheet. |
| 335 | `fnd72_s_pit_or_is_a2_is_projected_benefit_obligation` | MATRIX | 0.542 | 其他 | 0 | — | — | — | UNUSABLE | Projected benefit obligation for defined benefit pension plans |
| 336 | `other_current_liabilities_annual` | VECTOR | 0.540 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current liabilities not classified elsewhere, as reported in annual statements. |
| 337 | `fnd72_s_pit_or_bs_a2_bs_curr_rental_expense` | MATRIX | 0.540 | 其他 | 0 | — | — | — | UNUSABLE | Rental/operating lease expense |
| 338 | `issued_shares_annual` | VECTOR | 0.537 | 其他 | 0 | — | — | — | UNUSABLE | Total number of shares issued and outstanding, as reported in annual statements. |
| 339 | `fnd72_s_pit_or_bs_q_1_announcement_dt` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Latest full earnings report or announcement date used for fundamentals (quarterly) |
| 340 | `fnd72_s_pit_or_bs_q_1_fundamental_entry_dt` | MATRIX | 0.537 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Date the fundamental data point was entered into the database |
| 341 | `fnd72_s_pit_or_bs_q_1_latest_period_end_dt_full_record` | MATRIX | 0.537 | 其他 | 0 | — | — | — | UNUSABLE | Latest available period-end date from the entity’s full financial records |
| 342 | `fnd72_s_pit_or_bs_q_2_announcement_dt` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Latest full earnings report announcement date |
| 343 | `fnd72_s_pit_or_bs_q_2_fundamental_entry_dt` | MATRIX | 0.537 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Date the fundamental data record was entered into the system |
| 344 | `fnd72_s_pit_or_bs_q_2_latest_period_end_dt_full_record` | MATRIX | 0.537 | 其他 | 0 | — | — | — | UNUSABLE | Latest available period end date from full financial records |
| 345 | `fnd72_s_pit_or_bs_q_announcement_dt` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Latest earnings announcement date for which full fundamental information is available for the quarter |
| 346 | `fnd72_s_pit_or_bs_q_fundamental_entry_dt` | MATRIX | 0.537 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Date the fundamental data record was entered into the database |
| 347 | `fnd72_s_pit_or_bs_q_latest_period_end_dt_full_record` | MATRIX | 0.537 | 其他 | 0 | — | — | — | UNUSABLE | Latest available period end date from the full financial records |
| 348 | `deferred_tax_liabilities_long_term_a` | VECTOR | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liabilities due beyond one year, as reported in annual statements. |
| 349 | `income_tax_accrued_payable_a` | VECTOR | 0.536 | 其他 | 0 | — | — | — | UNUSABLE | Income taxes accrued but not yet paid, as reported in annual statements. |
| 350 | `fnd72_pit_or_bs_a_bs_options_outstanding` | VECTOR | 0.536 | 其他 | 0 | — | — | — | UNUSABLE | Number of stock options outstanding at period end |
| 351 | `deferred_tax_assets_long_term_amt` | VECTOR | 0.535 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-term deferred tax assets reported on the balance sheet. |
| 352 | `fnd72_s_pit_or_cf_a_cf_net_cash_paid_for_aquis` | MATRIX | 0.535 | 其他 | 0 | — | — | — | UNUSABLE | Annual net cash paid for acquisitions |
| 353 | `number_of_outlets_branches` | VECTOR | 0.532 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total number of company-operated outlets or branches. |
| 354 | `fnd72_s_pit_or_is_a2_is_oprb_expense_income` | MATRIX | 0.529 | 其他 | 0 | — | — | — | UNUSABLE | Other post-retirement benefits expense or income |
| 355 | `fnd72_pit_or_bs_a_bs_other_cur_asset_less_prepay` | VECTOR | 0.528 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current assets excluding prepaid expenses |
| 356 | `fnd72_pit_or_bs_a_invtry_finished_goods` | VECTOR | 0.527 | 其他 | 0 | — | — | — | UNUSABLE | Finished goods component of inventory |
| 357 | `fnd72_pit_or_bs_a_invtry_raw_materials` | VECTOR | 0.527 | 其他 | 0 | — | — | — | UNUSABLE | Raw materials component of inventory |
| 358 | `fnd72_s_pit_or_bs_a2_bs_future_min_oper_lease_oblig` | MATRIX | 0.526 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Total future minimum operating lease payments committed as of the reporting date |
| 359 | `fnd72_pit_or_bs_a_bs_other_inv` | VECTOR | 0.526 | 其他 | 0 | — | — | — | UNUSABLE | Other inventories and related allowances |
| 360 | `furniture_machinery_equipment_amt` | VECTOR | 0.525 | 其他 | 0 | — | — | — | UNUSABLE | Value of furniture, machinery, and equipment owned. |
| 361 | `other_noncurrent_liabilities_amt` | VECTOR | 0.524 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other liabilities due beyond one year not classified elsewhere. |
| 362 | `fnd72_s_pit_or_is_a2_is_interest_cost_pension` | MATRIX | 0.523 | 其他 | 0 | — | — | — | UNUSABLE | Annual interest cost on pension obligations |
| 363 | `fnd72_pit_or_bs_a_invtry_in_progress` | VECTOR | 0.522 | 其他 | 0 | — | — | — | UNUSABLE | Work-in-progress inventory |
| 364 | `fnd72_s_pit_or_bs_a_bs_common_stock` | MATRIX | 0.517 | 其他 | 0 | — | — | — | UNUSABLE | Common stock (share capital, balance sheet, annual) |
| 365 | `fnd72_s_pit_or_is_a2_is_service_cost` | MATRIX | 0.516 | 其他 | 0 | — | — | — | UNUSABLE | Service cost component of pension/postretirement benefit expense |
| 366 | `fnd72_pit_or_bs_a_bs_accrual` | VECTOR | 0.515 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other accounts payable and accruals |
| 367 | `fnd72_pit_or_is_a_is_over_underfund_pension_exp` | VECTOR | 0.515 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Quarterly expense impact related to overfunded/underfunded pension plans recognized in the income statement |
| 368 | `fnd72_pit_or_is_a_is_projected_benefit_obligation` | VECTOR | 0.514 | 其他 | 0 | — | — | — | UNUSABLE | Projected benefit obligation (PBO) for pension plans as of the reporting period |
| 369 | `common_stock_amt` | VECTOR | 0.512 | 其他 | 0 | — | — | — | UNUSABLE | Value of common stock issued by the company. |
| 370 | `additional_paid_in_capital_amt` | VECTOR | 0.509 | 其他 | 0 | — | — | — | UNUSABLE | Capital contributed by shareholders in excess of par value. |
| 371 | `other_current_liabilities_value_3` | MATRIX | 0.508 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of other current liabilities not separately disclosed. |
| 372 | `fnd72_pit_or_bs_a_bs_other_cur_liab` | VECTOR | 0.506 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current (short-term) liabilities |
| 373 | `fnd72_pit_or_bs_a_bs_st_portion_of_lt_debt` | VECTOR | 0.506 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current maturities of long-term debt due within one year |
| 374 | `short_term_borrowings_a` | VECTOR | 0.505 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Borrowings due within one year, as reported in annual statements. |
| 375 | `fnd72_s_pit_or_cf_a_cf_interest_received` | MATRIX | 0.504 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Cash inflow from interest received |
| 376 | `fnd72_pit_or_is_a_is_interest_cost_pension` | VECTOR | 0.503 | 其他 | 0 | — | — | — | UNUSABLE | Interest cost on pension obligations (increase in benefit obligation due to passage of time) |
| 377 | `fnd72_s_pit_or_bs_a_bs_st_portion_of_lt_debt` | MATRIX | 0.501 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term portion of long-term debt due within one year |
| 378 | `long_term_debt_annual_2` | VECTOR | 0.501 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Outstanding balance of debt obligations due beyond one year, as reported in annual statements. |
| 379 | `fnd72_pit_or_is_a_is_service_cost` | VECTOR | 0.499 | 其他 | 0 | — | — | — | UNUSABLE | Service cost component of pension expense for the period |
| 380 | `short_term_borrowings_total_6` | MATRIX | 0.498 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total short-term borrowings outstanding. |
| 381 | `fnd72_pit_or_is_q_fundamental_entry_dt` | VECTOR | 0.496 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Fundamental data entry date |
| 382 | `fnd72_pit_or_is_q_id_bb_global` | VECTOR | 0.496 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Financial Instrument Global Identifier linking the instrument across Bloomberg systems |
| 383 | `fnd72_pit_or_is_q_latest_period_end_dt_full_record` | VECTOR | 0.496 | 其他 | 0 | — | — | — | UNUSABLE | Latest available period end date from the full financial records |
| 384 | `fnd72_pit_or_is_q_announcement_dt` | VECTOR | 0.495 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the latest full quarterly earnings report |
| 385 | `fnd72_s_pit_or_cf_a_cf_change_in_inventories` | MATRIX | 0.493 | 其他 | 0 | — | — | — | UNUSABLE | Annual change in inventories (working capital adjustment) |
| 386 | `fnd72_is_q_fiscal_year_period` | VECTOR | 0.491 | 价量与波动 | 0 | — | — | — | UNUSABLE | This field, used for the History Wizard, will return the Fiscal year and period that coincides with the period end date |
| 387 | `inventory_total_a2` | MATRIX | 0.491 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Total value of inventory for region A2. |
| 388 | `fnd72_pit_or_bs_a_bs_options_granted` | VECTOR | 0.490 | 其他 | 0 | — | — | — | UNUSABLE | Number of stock options granted during the period |
| 389 | `additional_paid_in_capital_3` | VECTOR | 0.488 | 其他 | 0 | — | — | — | UNUSABLE | Capital contributed by shareholders in excess of par value. |
| 390 | `fnd72_s_pit_or_is_a2_is_fair_value_plan_assets` | MATRIX | 0.487 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fair value of pension plan assets |
| 391 | `fnd72_pit_or_is_q_sales_rev_turn` | VECTOR | 0.487 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total revenue (sales) for the quarter |
| 392 | `fnd72_s_pit_or_bs_a_bs_add_paid_in_cap` | MATRIX | 0.485 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Additional paid in capital of common equity, annual |
| 393 | `fnd72_pit_or_is_a_is_oprb_expense_income` | VECTOR | 0.485 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly other post-retirement benefits expense or income (income statement) |
| 394 | `fnd72_pit_or_bs_a_bs_common_stock` | VECTOR | 0.480 | 其他 | 0 | — | — | — | UNUSABLE | Common stock |
| 395 | `fnd72_s_pit_or_bs_q_1_bs_sh_out` | MATRIX | 0.479 | 其他 | 0 | — | — | — | UNUSABLE | Shares outstanding |
| 396 | `fnd72_s_pit_or_bs_q_bs_sh_out` | MATRIX | 0.479 | 其他 | 0 | — | — | — | UNUSABLE | Total number of shares outstanding at period end (excluding treasury shares) |
| 397 | `fnd72_s_pit_or_bs_q_1_bs_tot_asset` | MATRIX | 0.477 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total assets |
| 398 | `fnd72_s_pit_or_bs_q_bs_tot_asset` | MATRIX | 0.477 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total assets reported on the balance sheet for the quarter |
| 399 | `fnd72_s_pit_or_bs_q_1_bs_other_asset_def_chng_other` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other long-term assets |
| 400 | `fnd72_s_pit_or_bs_q_bs_other_asset_def_chng_other` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Miscellaneous long-term (non-current) assets not otherwise classified |
| 401 | `fnd72_s_pit_or_bs_q_1_bs_cash_near_cash_item` | MATRIX | 0.475 | 其他 | 0 | — | — | — | UNUSABLE | Cash and cash equivalents (cash and near-cash items) |
| 402 | `fnd72_s_pit_or_bs_q_bs_cash_near_cash_item` | MATRIX | 0.475 | 其他 | 0 | — | — | — | UNUSABLE | Cash and cash equivalents |
| 403 | `fnd72_s_pit_or_bs_q_1_bs_other_lt_liabilities` | MATRIX | 0.474 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other long-term liabilities |
| 404 | `fnd72_s_pit_or_bs_q_bs_other_lt_liabilities` | MATRIX | 0.474 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other long-term liabilities not classified elsewhere |
| 405 | `fnd72_s_pit_or_bs_q_1_bs_lt_borrow` | MATRIX | 0.472 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-term borrowings and debt obligations due beyond one year |
| 406 | `fnd72_s_pit_or_bs_q_bs_lt_borrow` | MATRIX | 0.472 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt obligations due beyond one year |
| 407 | `fnd72_s_pit_or_bs_q_1_bs_retain_earn` | MATRIX | 0.472 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Retained earnings balance |
| 408 | `fnd72_s_pit_or_bs_q_bs_retain_earn` | MATRIX | 0.472 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The cumulative undistributed earnings and comprehensive equity accumulated by the company |
| 409 | `fnd72_s_pit_or_bs_q_1_bs_other_st_liab` | MATRIX | 0.471 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other short-term liabilities due within one year not separately categorized |
| 410 | `fnd72_s_pit_or_bs_q_bs_other_st_liab` | MATRIX | 0.471 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other short-term liabilities |
| 411 | `fnd72_is_q_eqy_fund_crncy` | VECTOR | 0.470 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Currency in which the fundamental data is reported |
| 412 | `fnd72_s_pit_or_bs_q_1_yqe_dfp_sb` | MATRIX | 0.470 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Preferred equity, including preferred stock |
| 413 | `fnd72_s_pit_or_bs_q_yqe_dfp_sb` | MATRIX | 0.470 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Preferred equity (preferred stock) component of shareholders’ equity |
| 414 | `fnd72_s_pit_or_bs_q_1_minority_noncontrolling_interest` | MATRIX | 0.469 | 其他 | 0 | — | — | — | UNUSABLE | Minority/non-controlling interest in subsidiaries |
| 415 | `fnd72_s_pit_or_bs_q_minority_noncontrolling_interest` | MATRIX | 0.469 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly value of minority (non-controlling) interests, the portion of subsidiaries’ equity not attributable to the parent company |
| 416 | `non_equity_reserves_bs` | MATRIX | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reserves not related to equity, as reported on the balance sheet. |
| 417 | `fnd72_q_1_bs_net_fix_asset` | MATRIX | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net property plant and equipment after accumulated depreciation |
| 418 | `fnd72_q_bs_net_fix_asset` | MATRIX | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net property plant and equipment after accumulated depreciation |
| 419 | `fnd72_pit_or_is_a_is_fair_value_plan_assets` | VECTOR | 0.467 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fair value of pension plan assets |
| 420 | `fnd72_bs_q_fiscal_year_period` | VECTOR | 0.466 | 价量与波动 | 0 | — | — | — | UNUSABLE | This field, used for the History Wizard, will return the Fiscal year and period that coincides with the period end date |
| 421 | `total_intangible_assets_net_amt` | VECTOR | 0.466 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net value of all intangible assets owned by the company. |
| 422 | `fnd72_pit_or_cf_a_cf_interest_received` | VECTOR | 0.465 | 其他 | 0 | — | — | — | UNUSABLE | Interest received |
| 423 | `inventory_annual_2` | VECTOR | 0.463 | 其他 | 0 | — | — | — | UNUSABLE | Value of goods held for sale or production, as reported in annual statements. |
| 424 | `fnd72_s_pit_or_bs_q_1_bs_st_borrow` | MATRIX | 0.463 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term debt |
| 425 | `fnd72_s_pit_or_bs_q_bs_st_borrow` | MATRIX | 0.463 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term borrowings/debt for the quarter |
| 426 | `short_term_provisions_amt` | VECTOR | 0.463 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Provisions due within one year, such as short-term liabilities. |
| 427 | `fnd72_pit_or_bs_a_hs_yst_fo_mun_sb` | VECTOR | 0.462 | 其他 | 0 | — | — | — | UNUSABLE | Number of treasury shares in primary equivalents at period end |
| 428 | `fnd72_s_pit_or_bs_q_2_bs_disclosed_intangibles` | MATRIX | 0.461 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total intangible assets net of amortization and impairments |
| 429 | `fnd72_s_pit_or_bs_q_bs_disclosed_intangibles` | MATRIX | 0.461 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total amount of disclosed intangible assets (e.g., goodwill, patents, copyrights) reported in the balance sheet |
| 430 | `trade_accounts_payable_value` | MATRIX | 0.460 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of trade accounts payable. |
| 431 | `fnd72_pit_or_bs_q_announcement_dt` | VECTOR | 0.457 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the latest full earnings report available |
| 432 | `fnd72_pit_or_bs_q_fundamental_entry_dt` | VECTOR | 0.457 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Fundamental data entry date (timestamp of entry) |
| 433 | `fnd72_pit_or_bs_q_latest_period_end_dt_full_record` | VECTOR | 0.457 | 其他 | 0 | — | — | — | UNUSABLE | Latest available period end date from full financial records |
| 434 | `fnd72_pit_or_cf_a_cf_change_in_inventories` | VECTOR | 0.456 | 其他 | 0 | — | — | — | UNUSABLE | Change in inventories |
| 435 | `fnd72_cf_q_fiscal_year_period` | VECTOR | 0.456 | 价量与波动 | 0 | — | — | — | UNUSABLE | This field, used for the History Wizard, will return the Fiscal year and period that coincides with the period end date |
| 436 | `fnd72_s_pit_or_bs_a2_bs_options_outstanding` | MATRIX | 0.455 | 其他 | 0 | — | — | — | UNUSABLE | Options outstanding at period end |
| 437 | `fnd72_s_pit_or_cf_q_cf_net_inc` | MATRIX | 0.455 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly net income as used in the cash flow statement starting point |
| 438 | `fnd72_s_pit_or_bs_a2_bs_rental_exp_year_1` | MATRIX | 0.452 | 其他 | 0 | — | — | — | UNUSABLE | Operating lease payments due in year 1 (annual disclosure) |
| 439 | `fnd72_s_pit_or_bs_a2_bs_total_capital_leases` | MATRIX | 0.452 | 其他 | 0 | — | — | — | UNUSABLE | Total capital lease obligations outstanding |
| 440 | `fnd72_pit_or_is_q_spe_si` | VECTOR | 0.451 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Per Share |
| 441 | `fnd72_bs_q_eqy_fund_crncy` | VECTOR | 0.450 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Currency in which the fundamental data is reported |
| 442 | `fnd72_pit_or_bs_a_bs_add_paid_in_cap` | VECTOR | 0.450 | 其他 | 0 | — | — | — | UNUSABLE | Additional paid-in capital (capital contributed over par value) |
| 443 | `fnd72_s_pit_or_is_q_earn_for_common` | MATRIX | 0.449 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly net income available to common shareholders (after preferred dividends) |
| 444 | `fnd72_s_pit_or_is_q_net_income_bef_mi` | MATRIX | 0.449 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income before minority noncontrolling interest |
| 445 | `fnd72_s_pit_or_is_q_net_income` | MATRIX | 0.449 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly net income (net profit or loss) |
| 446 | `fnd72_pit_or_is_a_is_benefits_paid_pension` | VECTOR | 0.449 | 其他 | 0 | — | — | — | UNUSABLE | Pension benefits paid during the period |
| 447 | `fnd72_s_pit_or_is_a2_is_benefits_paid_pension` | MATRIX | 0.448 | 其他 | 0 | — | — | — | UNUSABLE | Annual benefits paid from the pension plan |
| 448 | `fnd72_s_pit_or_is_q_xo_gl_net_of_tax` | MATRIX | 0.447 | 其他 | 0 | — | — | — | UNUSABLE | Extraordinary gains or losses net of tax |
| 449 | `fnd72_s_pit_or_is_q_pretax_inc` | MATRIX | 0.447 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly pre-tax income |
| 450 | `fnd72_s_pit_or_is_q_is_avg_num_sh_for_eps` | MATRIX | 0.446 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly basic weighted average number of shares outstanding (for EPS) |
| 451 | `fnd72_s_pit_or_is_q_is_oper_inc` | MATRIX | 0.444 | 其他 | 0 | — | — | — | UNUSABLE | Operating income or loss |
| 452 | `fnd72_s_pit_or_is_q_is_inc_bef_xo_item` | MATRIX | 0.444 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly income (loss) from continuing operations, i.e., income before extraordinary items and discontinued operations |
| 453 | `fnd72_s_pit_or_is_q_is_net_non_oper_loss` | MATRIX | 0.443 | 其他 | 0 | — | — | — | UNUSABLE | Net non-operating losses (gains) |
| 454 | `ard_total_shareholders_equity` | MATRIX | 0.443 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total shareholders' equity in standardized ARD format. |
| 455 | `fnd72_s_pit_or_is_q_is_sh_for_diluted_eps` | MATRIX | 0.443 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly diluted weighted average shares outstanding |
| 456 | `fnd72_s_pit_or_is_q_spe_si` | MATRIX | 0.442 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly basic earnings per share |
| 457 | `fnd72_s_pit_or_is_q_is_earn_bef_xo_items_per_sh` | MATRIX | 0.442 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly basic EPS from continuing operations (before extraordinary items) |
| 458 | `fnd72_s_pit_or_bs_a_bs_non_depr_decomm_fund` | MATRIX | 0.441 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Portion of the decommissioning fund classified as non-depreciable |
| 459 | `fnd72_cf_q_eqy_fund_crncy` | VECTOR | 0.441 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Currency in which the fundamental data is reported |
| 460 | `fnd72_s_pit_or_is_q_inc_bef_xo_less_min_int_pref_dvd` | MATRIX | 0.441 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Income before extraordinary items less minority interest and preferred dividends |
| 461 | `fnd72_pit_or_cf_q_announcement_dt` | VECTOR | 0.439 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Latest earnings announcement date corresponding to a full fundamental report |
| 462 | `fnd72_pit_or_cf_q_fundamental_entry_dt` | VECTOR | 0.439 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Date the fundamental data point was entered into the system |
| 463 | `fnd72_pit_or_cf_q_id_bb_global` | VECTOR | 0.439 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Financial Instrument Global Identifier used to link entities across Bloomberg datasets |
| 464 | `fnd72_pit_or_cf_q_latest_period_end_dt_full_record` | VECTOR | 0.439 | 其他 | 0 | — | — | — | UNUSABLE | Latest available period end date from full financial records |
| 465 | `fnd72_s_pit_or_is_q_is_diluted_eps` | MATRIX | 0.439 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly diluted earnings per share |
| 466 | `fnd72_s_pit_or_is_q_is_net_inc_avail_com_shrhldrs` | MATRIX | 0.439 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly net income available to common shareholders (after preferred dividends) |
| 467 | `trade_accounts_receivable_annual` | VECTOR | 0.438 | 价量与波动 | 0 | — | — | — | UNUSABLE | Amounts owed to the company by customers for sales made on credit, as reported in annual statements. |
| 468 | `fnd72_s_pit_or_is_q_is_inc_tax_exp` | MATRIX | 0.438 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly income tax expense or benefit |
| 469 | `fnd72_pit_or_cf_q_cf_def_of_fund` | VECTOR | 0.438 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | No longer supported |
| 470 | `fnd72_s_pit_or_is_a_is_cogs_to_fe_and_pp_and_g` | MATRIX | 0.437 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Annual cost of revenue (cost of goods sold) |
| 471 | `fnd72_s_pit_or_is_q_min_noncontrol_interest_credits` | MATRIX | 0.437 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly minority/noncontrolling interest (credits) in earnings |
| 472 | `fnd72_s_pit_or_is_q_is_sga_other_op_depr_op_maint` | MATRIX | 0.437 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly operating expenses (including SG&A, other operating depreciation and maintenance) |
| 473 | `fnd72_s_pit_or_bs_a_bs_prepay` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Prepaid expenses recorded as current assets (amounts paid in advance for goods/services) |
| 474 | `fnd72_s_pit_or_is_q_is_basic_eps_cont_ops` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Basic earnings per share from continuing operations |
| 475 | `fnd72_s_pit_or_is_q_ox_feb_spe_lid_si` | MATRIX | 0.436 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Diluted earnings per share before extraordinary items |
| 476 | `fnd72_s_pit_or_is_q_is_dil_eps_cont_ops` | MATRIX | 0.435 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Diluted earnings per share from continuing operations |
| 477 | `fnd72_s_pit_or_bs_q_1_bs_def_tax_liab` | MATRIX | 0.435 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net long-term deferred tax liabilities |
| 478 | `fnd72_s_pit_or_bs_q_bs_def_tax_liab` | MATRIX | 0.435 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net deferred tax liabilities, long-term portion |
| 479 | `fnd72_s_pit_or_is_q_is_tax_eff_on_abnormal_item` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Tax effects on abnormal items |
| 480 | `fnd72_s_pit_or_is_q_is_abnormal_item` | MATRIX | 0.434 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly abnormal/exceptional items (losses or gains) |
| 481 | `fnd72_pit_or_bs_a_bs_non_depr_decomm_fund` | VECTOR | 0.434 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Non-Depreciable Real Estate |
| 482 | `fnd72_s_pit_or_bs_a2_bs_rental_exp_beyond_year_5` | MATRIX | 0.434 | 其他 | 0 | — | — | — | UNUSABLE | Annual operating lease payments due in year 6 and beyond |
| 483 | `fnd72_s_pit_or_is_q_is_tot_cash_pfd_dvd` | MATRIX | 0.434 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly total cash preferred dividends paid |
| 484 | `fnd72_s_pit_or_bs_q_1_bs_sh_cap_and_apic` | MATRIX | 0.433 | 其他 | 0 | — | — | — | UNUSABLE | Common share capital at par value plus additional paid-in capital (APIC) |
| 485 | `fnd72_s_pit_or_bs_q_bs_sh_cap_and_apic` | MATRIX | 0.433 | 其他 | 0 | — | — | — | UNUSABLE | Total share capital and additional paid-in-capital reported on the balance sheet |
| 486 | `fnd72_pit_or_bs_q_bs_sh_out` | VECTOR | 0.432 | 其他 | 0 | — | — | — | UNUSABLE | Shares outstanding at period end |
| 487 | `fnd72_pit_or_bs_q_bs_tot_asset` | VECTOR | 0.432 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total assets at period end |
| 488 | `raw_material_inventory_value` | MATRIX | 0.431 | 其他 | 0 | — | — | — | UNUSABLE | Value of raw materials held in inventory. |
| 489 | `fnd72_pit_or_bs_q_bs_other_asset_def_chng_other` | VECTOR | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other long-term (noncurrent) assets not classified elsewhere |
| 490 | `fnd72_pit_or_bs_q_bs_cash_near_cash_item` | VECTOR | 0.431 | 其他 | 0 | — | — | — | UNUSABLE | Cash and cash equivalents |
| 491 | `fnd72_pit_or_bs_q_bs_other_lt_liabilities` | VECTOR | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other long-term liabilities not otherwise classified |
| 492 | `fnd72_pit_or_bs_q_bs_retain_earn` | VECTOR | 0.430 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Retained earnings (and other equity reserves where applicable) |
| 493 | `fnd72_pit_or_bs_q_bs_lt_borrow` | VECTOR | 0.430 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-term debt |
| 494 | `fnd72_pit_or_bs_q_bs_other_st_liab` | VECTOR | 0.430 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other short-term liabilities |
| 495 | `fnd72_s_pit_or_is_q_is_xo_loss_bef_tax_eff` | MATRIX | 0.430 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly extraordinary gains/losses before related tax effects |
| 496 | `fnd72_s_pit_or_bs_a2_lt_capital_lease_obligations` | MATRIX | 0.430 | 其他 | 0 | — | — | — | UNUSABLE | Noncurrent portion of capital lease obligations due after one year |
| 497 | `fnd72_pit_or_is_q_xo_gl_net_of_tax` | VECTOR | 0.429 | 其他 | 0 | — | — | — | UNUSABLE | Net extraordinary gains or losses after tax |
| 498 | `fnd72_pit_or_bs_q_bs_pfd_eqy` | VECTOR | 0.429 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Preferred equity |
| 499 | `fnd72_pit_or_bs_q_minority_noncontrolling_interest` | VECTOR | 0.429 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity attributable to noncontrolling interests in subsidiaries |
| 500 | `fnd72_pit_or_bs_q_bs_net_fix_asset` | VECTOR | 0.428 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Property, plant and equipment, net of accumulated depreciation |
| 501 | `fnd72_pit_or_bs_q_bs_disclosed_intangibles` | VECTOR | 0.427 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total intangible assets, net |
| 502 | `fnd72_pit_or_bs_q_bs_st_borrow` | VECTOR | 0.426 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term borrowings or debt due within one year |
| 503 | `fnd72_s_pit_or_bs_q_1_bs_lt_invest` | MATRIX | 0.426 | 其他 | 0 | — | — | — | UNUSABLE | Long-Term Investments |
| 504 | `fnd72_s_pit_or_bs_q_bs_lt_invest` | MATRIX | 0.426 | 其他 | 0 | — | — | — | UNUSABLE | Long-term investments and receivables reported on the balance sheet for the quarter |
| 505 | `fnd72_pit_or_cf_q_cf_form_of_statement` | VECTOR | 0.424 | 其他 | 0 | — | — | — | UNUSABLE | No longer supported |
| 506 | `fnd72_pit_or_bs_q_bs_sh_cap_and_apic` | VECTOR | 0.422 | 其他 | 0 | — | — | — | UNUSABLE | Share capital at par plus additional paid-in capital (APIC) |
| 507 | `fnd72_pit_or_is_q_earn_for_common` | VECTOR | 0.422 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income available to common shareholders |
| 508 | `fnd72_pit_or_is_q_is_net_non_oper_loss` | VECTOR | 0.422 | 其他 | 0 | — | — | — | UNUSABLE | Net non-operating losses (gains) |
| 509 | `fnd72_pit_or_is_q_net_income` | VECTOR | 0.422 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income/net profit (loss) |
| 510 | `fnd72_pit_or_is_q_net_income_bef_mi` | VECTOR | 0.422 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income before minority interests |
| 511 | `net_fixed_assets_2` | MATRIX | 0.422 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net value of property, plant, and equipment after depreciation. |
| 512 | `fnd72_pit_or_is_q_min_noncontrol_interest_credits` | VECTOR | 0.422 | 风险与质量 | 0 | — | — | — | UNUSABLE | Credits attributable to minority or noncontrolling interests for the quarter |
| 513 | `fnd72_pit_or_is_q_is_abnormal_item` | VECTOR | 0.422 | 其他 | 0 | — | — | — | UNUSABLE | Total abnormal/exceptional items (gains or losses) recognized for the period |
| 514 | `fnd72_pit_or_is_q_pretax_inc` | VECTOR | 0.422 | 其他 | 0 | — | — | — | UNUSABLE | Income before income taxes for the period |
| 515 | `fnd72_pit_or_is_q_is_tax_eff_on_abnormal_item` | VECTOR | 0.422 | 其他 | 0 | — | — | — | UNUSABLE | Tax effect related to abnormal or extraordinary items for the quarter |
| 516 | `fnd72_pit_or_is_q_is_xo_loss_bef_tax_eff` | VECTOR | 0.422 | 其他 | 0 | — | — | — | UNUSABLE | Extraordinary loss before tax effects |
| 517 | `fnd72_pit_or_is_q_is_oper_inc` | VECTOR | 0.421 | 其他 | 0 | — | — | — | UNUSABLE | Operating income (loss) for the quarter |
| 518 | `fnd72_pit_or_bs_q_bs_def_tax_liab` | VECTOR | 0.420 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-term net deferred tax liabilities |
| 519 | `fnd72_pit_or_is_q_is_inc_bef_xo_item` | VECTOR | 0.420 | 其他 | 0 | — | — | — | UNUSABLE | Income (loss) from continuing operations before extraordinary items |
| 520 | `fnd72_s_pit_or_bs_q_1_bs_mkt_sec_other_st_invest` | MATRIX | 0.419 | 其他 | 0 | — | — | — | UNUSABLE | Marketable securities and other short-term investments |
| 521 | `fnd72_s_pit_or_bs_q_bs_mkt_sec_other_st_invest` | MATRIX | 0.419 | 其他 | 0 | — | — | — | UNUSABLE | Balance sheet value of marketable securities and other short-term investments |
| 522 | `fnd72_pit_or_is_q_is_avg_num_sh_for_eps` | VECTOR | 0.419 | 其他 | 0 | — | — | — | UNUSABLE | Basic weighted average number of shares for EPS calculation |
| 523 | `fnd72_s_pit_or_bs_a2_st_capital_lease_obligations` | MATRIX | 0.419 | 其他 | 0 | — | — | — | UNUSABLE | Current portion of capital lease obligations due within one year |
| 524 | `fnd72_pit_or_is_a_is_disc_rate_pension_plan_liabs` | VECTOR | 0.418 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Discount rate used to measure pension plan liabilities |
| 525 | `fnd72_pit_or_cf_q_cf_net_inc` | VECTOR | 0.418 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income as presented in the cash flow statement (starting point for operating cash flow) |
| 526 | `fnd72_pit_or_is_q_is_eps` | VECTOR | 0.417 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Basic earnings per share for the quarter |
| 527 | `fnd72_pit_or_is_q_is_sga_other_op_depr_op_maint` | VECTOR | 0.417 | 其他 | 0 | — | — | — | UNUSABLE | Operating expenses including SG&A, other operating depreciation, and maintenance for the quarter |
| 528 | `fnd72_pit_or_is_q_is_earn_bef_xo_items_per_sh` | VECTOR | 0.417 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Before Extraordinary Items Per Share (Basic EPS) |
| 529 | `fnd72_pit_or_is_q_is_sh_for_diluted_eps` | VECTOR | 0.417 | 其他 | 0 | — | — | — | UNUSABLE | Weighted average diluted shares outstanding used to compute diluted EPS for the quarter |
| 530 | `fnd72_pit_or_is_q_is_inc_tax_exp` | VECTOR | 0.416 | 其他 | 0 | — | — | — | UNUSABLE | Income tax expense or benefit recognized for the quarter |
| 531 | `fnd72_pit_or_is_q_is_tot_cash_pfd_dvd` | VECTOR | 0.416 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total cash preferred dividends for the quarter |
| 532 | `fnd72_pit_or_is_q_inc_bef_xo_less_min_int_pref_dvd` | VECTOR | 0.416 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Income before extraordinary items after deducting minority interest and preferred dividends for the quarter |
| 533 | `fnd72_s_pit_or_is_q_net_non_oper_loss` | MATRIX | 0.415 | 其他 | 0 | — | — | — | UNUSABLE | Net non-operating loss for the period |
| 534 | `fnd72_s_pit_or_bs_q_1_bs_cur_asset_report` | MATRIX | 0.414 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total current assets |
| 535 | `fnd72_s_pit_or_bs_q_bs_cur_asset_report` | MATRIX | 0.414 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total current assets |
| 536 | `fnd72_pit_or_is_q_is_diluted_eps` | VECTOR | 0.414 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Diluted earnings per share for the period |
| 537 | `fnd72_pit_or_is_q_is_net_inc_avail_com_shrhldrs` | VECTOR | 0.414 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income available to common shareholders for the quarter |
| 538 | `fnd72_pit_or_is_q_is_basic_eps_cont_ops` | VECTOR | 0.413 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Basic earnings per share from continuing operations (Income Statement) |
| 539 | `ard_cash_and_equivalents` | MATRIX | 0.413 | 其他 | 0 | — | — | — | UNUSABLE | Cash and cash equivalents in standardized ARD format. |
| 540 | `fnd72_pit_or_is_q_is_dil_eps_cont_ops` | VECTOR | 0.412 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted diluted earnings per share from continuing operations |
| 541 | `fnd72_pit_or_bs_q_bs_pure_retained_earnings` | VECTOR | 0.412 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pure retained earnings balance |
| 542 | `fnd72_pit_or_is_q_is_dil_eps_bef_xo` | VECTOR | 0.412 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Diluted earnings per share from continuing operations for the period |
| 543 | `fnd72_s_pit_or_bs_q_1_bs_cur_liab` | MATRIX | 0.412 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total current liabilities |
| 544 | `fnd72_s_pit_or_bs_q_bs_cur_liab` | MATRIX | 0.412 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total current liabilities |
| 545 | `fnd72_s_pit_or_bs_q_2_bs_pure_retained_earnings` | MATRIX | 0.410 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Retained earnings (accumulated deficit) |
| 546 | `fnd72_s_pit_or_bs_q_bs_pure_retained_earnings` | MATRIX | 0.410 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Retained earnings: accumulated earnings retained in the company after dividends, possibly including legal reserves and current year profit |
| 547 | `other_reserve_value` | MATRIX | 0.408 | 其他 | 0 | — | — | — | UNUSABLE | Value of other reserves reported on the balance sheet. |
| 548 | `goodwill_amt` | VECTOR | 0.407 | 其他 | 0 | — | — | — | UNUSABLE | Value of goodwill reported on the balance sheet. |
| 549 | `fnd72_pit_or_bs_q_bs_lt_invest` | VECTOR | 0.405 | 其他 | 0 | — | — | — | UNUSABLE | Long-term investments and long-term receivables |
| 550 | `fnd72_s_pit_or_bs_a2_bs_allow_doubtful_acc_rec` | MATRIX | 0.405 | 其他 | 0 | — | — | — | UNUSABLE | Allowance for doubtful accounts (contra receivables) |
| 551 | `fnd72_s_pit_or_bs_a2_bs_total_avail_line_of_credit` | MATRIX | 0.404 | 风险与质量 | 0 | — | — | — | UNUSABLE | Unused portion of committed lines of credit currently available |
| 552 | `other_intangible_assets_amt` | VECTOR | 0.403 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of intangible assets not classified elsewhere. |
| 553 | `fnd72_pit_or_bs_a_bs_total_avail_line_of_credit` | VECTOR | 0.403 | 风险与质量 | 0 | — | — | — | UNUSABLE | Total available lines of credit |
| 554 | `accounts_payable_trade_amt` | VECTOR | 0.403 | 价量与波动 | 0 | — | — | — | UNUSABLE | Amount owed to suppliers for goods and services received. |
| 555 | `other_noncurrent_assets_amt` | VECTOR | 0.400 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other assets not expected to be converted to cash within a year. |
| 556 | `raw_material_inventory` | VECTOR | 0.400 | 其他 | 0 | — | — | — | UNUSABLE | Value of raw materials held in inventory. |
| 557 | `fnd72_pit_or_bs_q_bs_goodwill` | VECTOR | 0.400 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Carrying value of goodwill (intangible asset arising from acquisitions) |
| 558 | `fnd72_pit_or_is_q_is_tax_eff_on_xo_item` | VECTOR | 0.400 | 其他 | 0 | — | — | — | UNUSABLE | Tax effect on extraordinary items for the quarter |
| 559 | `other_reserves_amt` | VECTOR | 0.400 | 其他 | 0 | — | — | — | UNUSABLE | Other reserves not classified elsewhere on the balance sheet. |
| 560 | `fnd72_pit_or_bs_q_bs_num_of_tsy_sh` | VECTOR | 0.399 | 其他 | 0 | — | — | — | UNUSABLE | Number of treasury shares |
| 561 | `fnd72_s_pit_or_bs_q_1_bs_tot_eqy` | MATRIX | 0.399 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total shareholders’ equity |
| 562 | `fnd72_s_pit_or_bs_q_bs_tot_eqy` | MATRIX | 0.399 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total equity or partnership capital; calculated as assets minus liabilities and includes all equity components and minority interests |
| 563 | `fnd72_pit_or_bs_q_bs_mkt_sec_other_st_invest` | VECTOR | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | Marketable securities and other short-term investments |
| 564 | `fnd72_s_pit_or_bs_q_2_num_outlets_branches` | MATRIX | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | Number of outlets and branches |
| 565 | `fnd72_s_pit_or_bs_q_num_outlets_branches` | MATRIX | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | Number of outlets and branches |
| 566 | `fnd72_pit_or_is_q_net_non_oper_loss` | VECTOR | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | Net non-operating loss (Income Statement) |
| 567 | `fnd72_pit_or_bs_a_bs_prepay` | VECTOR | 0.396 | 其他 | 0 | — | — | — | UNUSABLE | Prepaid expenses |
| 568 | `fnd72_s_pit_or_is_q_ebit` | MATRIX | 0.394 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest and taxes (EBIT) |
| 569 | `fnd72_s_pit_or_bs_q_1_bs_tot_liab_eqy` | MATRIX | 0.393 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Liabilities and Equity (Balance Sheet) |
| 570 | `fnd72_s_pit_or_bs_q_bs_tot_liab_eqy` | MATRIX | 0.393 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total liabilities plus shareholders’ equity |
| 571 | `total_shareholders_equity_4` | VECTOR | 0.393 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total equity attributable to shareholders. |
| 572 | `reserve_charge_income_statement` | VECTOR | 0.393 | 其他 | 0 | — | — | — | UNUSABLE | Expense recognized for changes in reserves during the period. |
| 573 | `fnd72_s_pit_or_cf_q_cf_depr_amort` | MATRIX | 0.393 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly depreciation and amortization expense recorded as a non cash adjustment in cash flows |
| 574 | `fnd72_pit_or_is_a_is_cogs_to_fe_and_pp_and_g` | VECTOR | 0.392 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cost of revenue |
| 575 | `total_current_assets_value_4` | MATRIX | 0.391 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total value of current assets. |
| 576 | `ard_total_current_liabilities` | MATRIX | 0.390 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total current liabilities in standardized ARD format. |
| 577 | `total_current_liabilities_value_2` | MATRIX | 0.390 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total value of current liabilities. |
| 578 | `liabilities_and_equity_total_4` | VECTOR | 0.390 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total of all liabilities and shareholders' equity. |
| 579 | `ard_total_noncurrent_assets` | MATRIX | 0.389 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total noncurrent assets in standardized ARD format. |
| 580 | `fnd72_s_pit_or_is_q_other_adjustments` | MATRIX | 0.389 | 其他 | 0 | — | — | — | UNUSABLE | Other adjustments reported in the income statement for the quarter |
| 581 | `inventory_finished_goods_amt` | VECTOR | 0.389 | 其他 | 0 | — | — | — | UNUSABLE | Value of finished goods inventory held by the company. |
| 582 | `fnd72_s_pit_or_cf_q_cf_cash_from_oper` | MATRIX | 0.388 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total cash flows from operating activities |
| 583 | `fnd72_s_pit_or_cf_q_cf_net_chng_cash` | MATRIX | 0.388 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly net change in cash and cash equivalents from all activities |
| 584 | `fnd72_s_pit_or_bs_q_1_bs_other_cur_asset` | MATRIX | 0.388 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current assets |
| 585 | `fnd72_s_pit_or_bs_q_bs_other_cur_asset` | MATRIX | 0.388 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current assets not separately itemized |
| 586 | `fnd72_pit_or_is_a_is_employer_contrib_pension` | VECTOR | 0.388 | 其他 | 0 | — | — | — | UNUSABLE | Employer contributions to pension plans during the quarter (income statement) |
| 587 | `fnd72_s_pit_or_is_q_is_tax_eff_on_xo_item` | MATRIX | 0.387 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly tax impact attributable to extraordinary items |
| 588 | `fnd72_s_pit_or_bs_q_1_hs_yst_fo_mun_sb` | MATRIX | 0.386 | 其他 | 0 | — | — | — | UNUSABLE | Number of treasury shares held by the company |
| 589 | `fnd72_s_pit_or_bs_q_hs_yst_fo_mun_sb` | MATRIX | 0.386 | 其他 | 0 | — | — | — | UNUSABLE | Number of treasury shares held by the company |
| 590 | `fnd72_s_pit_or_cf_q_cf_cash_from_inv_act` | MATRIX | 0.385 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total cash flows from investing activities |
| 591 | `fnd72_pit_or_cf_a_cf_incr_st_borrow` | VECTOR | 0.384 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net increase or decrease in short-term borrowings (financing cash flow) |
| 592 | `fnd72_pit_or_bs_q_bs_pension_rsrv` | VECTOR | 0.384 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pension and postretirement benefit obligations (liability) |
| 593 | `fnd72_s_pit_or_cf_q_cf_cash_from_fnc_act` | MATRIX | 0.384 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly net cash provided by or used in financing activities |
| 594 | `stock_option_expense_pre_tax` | VECTOR | 0.384 | 其他 | 0 | — | — | — | UNUSABLE | Stock-based compensation expense before tax effects. |
| 595 | `fnd72_pit_or_bs_q_bs_invest_in_assoc_co` | VECTOR | 0.383 | 其他 | 0 | — | — | — | UNUSABLE | Investment in associate/affiliated companies |
| 596 | `ard_total_noncurrent_liabilities` | MATRIX | 0.383 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total noncurrent liabilities in standardized ARD format. |
| 597 | `fnd72_s_pit_or_bs_q_2_bs_capital_reserve` | MATRIX | 0.383 | 其他 | 0 | — | — | — | UNUSABLE | Capital Reserve |
| 598 | `fnd72_s_pit_or_bs_q_bs_capital_reserve` | MATRIX | 0.383 | 其他 | 0 | — | — | — | UNUSABLE | Capital reserve (e.g., share premium or other paid-in capital) |
| 599 | `other_current_assets_12` | VECTOR | 0.383 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current assets not classified elsewhere. |
| 600 | `fnd72_pit_or_is_a_is_rate_of_comp_increase_pension` | VECTOR | 0.383 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Assumed rate of compensation increase used in pension actuarial calculations |
| 601 | `net_property_plant_equipment_3` | VECTOR | 0.382 | 其他 | 0 | — | — | — | UNUSABLE | Net value of property, plant, and equipment after depreciation. |
| 602 | `fnd72_s_pit_or_bs_q_1_bs_inventories` | MATRIX | 0.381 | 其他 | 0 | — | — | — | UNUSABLE | Inventories |
| 603 | `fnd72_s_pit_or_bs_q_bs_inventories` | MATRIX | 0.381 | 其他 | 0 | — | — | — | UNUSABLE | Value of inventories on the balance sheet |
| 604 | `fnd72_pit_or_bs_a_bs_total_line_of_credit` | VECTOR | 0.379 | 风险与质量 | 0 | — | — | — | UNUSABLE | Total committed lines of credit facilities |
| 605 | `fnd72_s_pit_or_bs_q_1_bs_pension_rsrv` | MATRIX | 0.378 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pension and post-retirement obligations/liabilities |
| 606 | `fnd72_s_pit_or_bs_q_bs_pension_rsrv` | MATRIX | 0.378 | 其他 | 0 | — | — | — | UNUSABLE | Balance of pension and post-retirement obligations and reserves (long-term provisions and severance payments) |
| 607 | `fnd72_pit_or_cf_q_cf_net_chng_cash` | VECTOR | 0.377 | 其他 | 0 | — | — | — | UNUSABLE | Net change in cash and cash equivalents for the period |
| 608 | `fnd72_pit_or_cf_q_cf_depr_amort` | VECTOR | 0.377 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation and amortization (cash flow) |
| 609 | `fnd72_pit_or_cf_q_cf_cash_from_oper` | VECTOR | 0.377 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total cash flows from operations |
| 610 | `cash_equivalents_other_amt` | VECTOR | 0.375 | 其他 | 0 | — | — | — | UNUSABLE | Cash and equivalents as reported in other statement formats. |
| 611 | `fnd72_s_pit_or_cf_q_cf_other_non_cash_adjust` | MATRIX | 0.375 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other non-cash adjustments to reconcile net income to cash |
| 612 | `fnd72_s_pit_or_bs_a2_bs_accrued_income_taxes` | MATRIX | 0.374 | 其他 | 0 | — | — | — | UNUSABLE | Income taxes accrued and payable but not yet paid |
| 613 | `fnd72_pit_or_bs_a_bs_allow_doubtful_acc_rec` | VECTOR | 0.374 | 其他 | 0 | — | — | — | UNUSABLE | Allowance for doubtful accounts against receivables |
| 614 | `fnd72_pit_or_is_q_ebit` | VECTOR | 0.373 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest and taxes |
| 615 | `fnd72_pit_or_bs_q_bs_cur_asset_report` | VECTOR | 0.372 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total current assets |
| 616 | `fnd72_s_pit_or_is_a2_is_disc_rate_pension_plan_liabs` | MATRIX | 0.372 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Discount rate used to value pension plan liabilities |
| 617 | `fnd72_s_pit_or_cf_q_cf_other_fnc_act` | MATRIX | 0.372 | 其他 | 0 | — | — | — | UNUSABLE | Other financing activities |
| 618 | `fnd72_s_pit_or_cf_q_cf_other_inv_act` | MATRIX | 0.371 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly net cash flows from other investing activities not otherwise classified |
| 619 | `fnd72_pit_or_bs_q_bs_amt_of_tsy_stock` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Amount of treasury stock |
| 620 | `fnd72_pit_or_cf_q_cf_cash_from_fnc_act` | VECTOR | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly net cash provided by financing activities |
| 621 | `fnd72_pit_or_cf_q_cf_cash_from_inv_act` | VECTOR | 0.371 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total cash flows from investing activities |
| 622 | `fnd72_pit_or_bs_q_bs_cur_liab` | VECTOR | 0.371 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total current liabilities due within one year |
| 623 | `fnd72_pit_or_is_q_other_adjustments` | VECTOR | 0.370 | 其他 | 0 | — | — | — | UNUSABLE | Other adjustments reported on the income statement for the quarter |
| 624 | `fnd72_pit_or_bs_q_bs_acct_note_rcv` | VECTOR | 0.370 | 其他 | 0 | — | — | — | UNUSABLE | Accounts and notes receivable |
| 625 | `fnd72_s_pit_or_bs_a2_bs_total_line_of_credit` | MATRIX | 0.370 | 风险与质量 | 0 | — | — | — | UNUSABLE | Total committed lines of credit including used and unused amounts |
| 626 | `fnd72_pit_or_cf_q_cf_other_non_cash_adjust` | VECTOR | 0.370 | 其他 | 0 | — | — | — | UNUSABLE | Other non-cash adjustments |
| 627 | `fnd72_pit_or_bs_q_bs_tot_liab_eqy` | VECTOR | 0.369 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total liabilities and equity for REITs (balance sheet total) |
| 628 | `fnd72_s_pit_or_is_a2_is_employer_contrib_pension` | MATRIX | 0.368 | 其他 | 0 | — | — | — | UNUSABLE | Annual employer contributions to pension plans |
| 629 | `fnd72_pit_or_cf_q_cf_other_inv_act` | VECTOR | 0.366 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other investing activities cash flows not otherwise classified |
| 630 | `fnd72_pit_or_cf_q_cf_other_fnc_act` | VECTOR | 0.366 | 其他 | 0 | — | — | — | UNUSABLE | Other financing activities |
| 631 | `fnd72_pit_or_bs_q_bs_tot_eqy` | VECTOR | 0.366 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total equity or partnership capital on the balance sheet |
| 632 | `fnd72_pit_or_is_q_is_comprehensive_income` | VECTOR | 0.366 | 其他 | 0 | — | — | — | UNUSABLE | Comprehensive income |
| 633 | `fnd72_s_pit_or_bs_a2_bs_options_granted` | MATRIX | 0.366 | 其他 | 0 | — | — | — | UNUSABLE | Options granted during the period |
| 634 | `cash_and_equivalents_7` | VECTOR | 0.366 | 其他 | 0 | — | — | — | UNUSABLE | Cash and short-term investments readily available for use. |
| 635 | `dividends_paid_total_2` | MATRIX | 0.365 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total dividends paid during the period. |
| 636 | `other_gross_fixed_assets_amt` | VECTOR | 0.362 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross value of fixed assets not classified elsewhere. |
| 637 | `fnd72_s_pit_or_bs_q_1_bs_acct_note_rcv` | MATRIX | 0.362 | 其他 | 0 | — | — | — | UNUSABLE | Accounts receivable plus notes receivable |
| 638 | `fnd72_s_pit_or_bs_q_bs_acct_note_rcv` | MATRIX | 0.362 | 其他 | 0 | — | — | — | UNUSABLE | Accounts and notes receivable reported on the balance sheet for the quarter |
| 639 | `fnd72_pit_or_is_q_is_comprehensive_income_per_shr` | VECTOR | 0.361 | 其他 | 0 | — | — | — | UNUSABLE | Comprehensive income per share for the quarter |
| 640 | `fnd72_s_pit_or_cf_q_cf_decr_cap_stock` | MATRIX | 0.361 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Quarterly cash outflow for share repurchases or reductions of capital stock |
| 641 | `fnd72_pit_or_bs_q_bs_par_val` | VECTOR | 0.360 | 其他 | 0 | — | — | — | UNUSABLE | Par value of issued share capital |
| 642 | `fnd72_s_pit_or_bs_q_1_bs_amt_of_tsy_stock` | MATRIX | 0.360 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Carrying amount of the company’s own shares repurchased and held in treasury, recorded as a reduction of equity |
| 643 | `fnd72_s_pit_or_bs_q_bs_amt_of_tsy_stock` | MATRIX | 0.360 | 其他 | 0 | — | — | — | UNUSABLE | Monetary amount/carrying value of treasury stock |
| 644 | `dividends_paid_cash_flow_q` | VECTOR | 0.360 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash outflow for dividends paid to shareholders in the quarter. |
| 645 | `fnd72_s_pit_or_is_q_ebitda` | MATRIX | 0.359 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly earnings before interest, taxes, depreciation, and amortization (EBITDA) |
| 646 | `fnd72_pit_or_is_q_is_other_adj_comp_inc` | VECTOR | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Other Adjustments to Comprehensive Income (Income Statement) |
| 647 | `fnd72_s_pit_or_cf_q_cf_chng_non_cash_work_cap` | MATRIX | 0.359 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly net change in non cash working capital items as an operating cash flow adjustment |
| 648 | `fnd72_s_pit_or_cf_q_cf_incr_cap_stock` | MATRIX | 0.359 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly cash inflow from issuing capital stock (equity) |
| 649 | `fnd72_s_pit_or_bs_q_1_bs_par_val` | MATRIX | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Par Value (Balance Sheet) |
| 650 | `fnd72_s_pit_or_bs_q_bs_par_val` | MATRIX | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Par value of issued share capital |
| 651 | `fnd72_s_pit_or_is_q_is_comprehensive_income` | MATRIX | 0.356 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total comprehensive income for the quarter (net income plus other comprehensive income) |
| 652 | `fnd72_pit_or_cf_q_cf_chng_non_cash_work_cap` | VECTOR | 0.356 | 其他 | 0 | — | — | — | UNUSABLE | Change in non-cash working capital |
| 653 | `fnd72_s_pit_or_cf_q_cf_cap_expend_prpty_add` | MATRIX | 0.354 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Quarterly capital expenditures/property additions (cash outflows for PP&E purchases and additions) |
| 654 | `fnd72_pit_or_cf_q_cf_incr_cap_stock` | VECTOR | 0.353 | 其他 | 0 | — | — | — | UNUSABLE | Increase in capital stock |
| 655 | `fnd72_pit_or_cf_q_cf_decr_cap_stock` | VECTOR | 0.353 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Cash outflow from decreases in capital stock (share repurchases or retirements) |
| 656 | `fnd72_pit_or_cf_q_cf_cap_expend_prpty_add` | VECTOR | 0.352 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Capital Expenditures (Cash Flow) |
| 657 | `fnd72_pit_or_bs_q_bs_capital_reserve` | VECTOR | 0.352 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Capital reserves within equity reported quarterly |
| 658 | `fnd72_s_pit_or_bs_q_2_bs_st_debt` | MATRIX | 0.351 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term debt and current portion of borrowings due within one year |
| 659 | `fnd72_s_pit_or_bs_q_bs_st_debt` | MATRIX | 0.351 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term borrowings and current portion of long-term debt |
| 660 | `fnd72_s_pit_or_cf_q_cf_def_of_fund` | MATRIX | 0.351 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | No longer supported |
| 661 | `fnd72_pit_or_bs_q_bs_other_cur_asset` | VECTOR | 0.350 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current assets not separately classified |
| 662 | `fnd72_pit_or_bs_q_num_outlets_branches` | VECTOR | 0.350 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Count of physical outlets or branches operated |
| 663 | `fnd72_s_pit_or_bs_q_2_bs_goodwill` | MATRIX | 0.350 | 其他 | 0 | — | — | — | UNUSABLE | Carrying amount of goodwill |
| 664 | `fnd72_s_pit_or_bs_q_bs_goodwill` | MATRIX | 0.350 | 其他 | 0 | — | — | — | UNUSABLE | Goodwill |
| 665 | `fnd72_s_pit_or_is_q_is_comprehensive_income_per_shr` | MATRIX | 0.350 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Comprehensive income per share for the quarter, including net income and other comprehensive income |
| 666 | `fnd72_pit_or_bs_q_bs_lifo_reserve` | VECTOR | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | LIFO reserve (difference between FIFO and LIFO inventory valuation) |
| 667 | `fnd72_pit_or_bs_q_bs_acct_payable` | VECTOR | 0.347 | 价量与波动 | 0 | — | — | — | UNUSABLE | Accounts payable/trade payables owed to suppliers |
| 668 | `fnd72_pit_or_is_q_ebitda` | VECTOR | 0.347 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation, and amortization for the period |
| 669 | `fnd72_pit_or_bs_q_bs_inventories` | VECTOR | 0.347 | 其他 | 0 | — | — | — | UNUSABLE | Inventories |
| 670 | `fnd72_pit_or_bs_a_bs_accrued_income_taxes` | VECTOR | 0.346 | 其他 | 0 | — | — | — | UNUSABLE | Accrued income taxes payable |
| 671 | `other_noncurrent_assets_value_3` | MATRIX | 0.346 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of other noncurrent assets. |
| 672 | `total_current_liabilities_9` | VECTOR | 0.346 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sum of all liabilities due within one year. |
| 673 | `total_current_assets_10` | VECTOR | 0.346 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sum of all assets expected to be converted to cash within one year. |
| 674 | `fnd72_s_pit_or_bs_q_2_bs_other_cur_asset_less_prepay` | MATRIX | 0.344 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current assets excluding prepayments |
| 675 | `fnd72_s_pit_or_bs_q_bs_other_cur_asset_less_prepay` | MATRIX | 0.344 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current assets excluding prepayments |
| 676 | `fnd72_s_pit_or_is_a_is_gnrl_and_admin_exp` | MATRIX | 0.344 | 其他 | 0 | — | — | — | UNUSABLE | General and Administrative Expenses (Income Statement) |
| 677 | `fnd72_s_pit_or_is_q_is_other_adj_comp_inc` | MATRIX | 0.342 | 其他 | 0 | — | — | — | UNUSABLE | Other adjustments to Other Comprehensive Income for the quarter |
| 678 | `total_noncurrent_liabilities_3` | VECTOR | 0.342 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sum of all liabilities due beyond one year. |
| 679 | `stock_option_cost_before_tax` | MATRIX | 0.341 | 其他 | 0 | — | — | — | UNUSABLE | Cost of stock-based compensation before tax effects. |
| 680 | `fnd72_s_pit_or_bs_q_1_bs_invest_in_assoc_co` | MATRIX | 0.341 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Investments in affiliated/associate companies (equity method) |
| 681 | `fnd72_s_pit_or_bs_q_bs_invest_in_assoc_co` | MATRIX | 0.341 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly investments in associated or affiliated companies (equity method) |
| 682 | `fnd72_pit_or_is_q_tot_int_exp` | VECTOR | 0.340 | 其他 | 0 | — | — | — | UNUSABLE | Total interest expense incurred during the quarter |
| 683 | `fnd72_s_pit_or_cf_q_cf_form_of_statement` | MATRIX | 0.340 | 其他 | 0 | — | — | — | UNUSABLE | No longer supported |
| 684 | `fnd72_pit_or_is_q_is_oprb_expense_income` | VECTOR | 0.340 | 其他 | 0 | — | — | — | UNUSABLE | Other post-retirement benefits (OPRB) expense or income recognized for the quarter |
| 685 | `other_receivables_amt` | VECTOR | 0.339 | 价量与波动 | 0 | — | — | — | UNUSABLE | Amount of receivables not classified as trade accounts. |
| 686 | `fnd72_pit_or_cf_q_cf_decr_invest` | VECTOR | 0.338 | 其他 | 0 | — | — | — | UNUSABLE | Proceeds from investments (decrease in investments) |
| 687 | `fnd72_s_pit_or_is_q_is_oprb_expense_income` | MATRIX | 0.336 | 其他 | 0 | — | — | — | UNUSABLE | Other postretirement benefits expense or income recognized in the period |
| 688 | `fnd72_pit_or_is_a_is_pension_category_equities` | VECTOR | 0.335 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage of pension plan assets allocated to equities |
| 689 | `stock_option_expense_post_tax` | VECTOR | 0.334 | 其他 | 0 | — | — | — | UNUSABLE | Stock-based compensation expense after tax effects. |
| 690 | `accounts_receivable_other` | MATRIX | 0.333 | 其他 | 0 | — | — | — | UNUSABLE | Value of other accounts receivable. |
| 691 | `fnd72_pit_or_cf_q_cf_reimb_lt_borrow` | VECTOR | 0.333 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Quarterly cash outflow for reimbursement/repayment of long-term borrowings |
| 692 | `fnd72_pit_or_cf_q_cf_incr_invest` | VECTOR | 0.331 | 其他 | 0 | — | — | — | UNUSABLE | Purchases of investments (increase in investments) |
| 693 | `fnd72_s_pit_or_bs_q_1_bs_acct_payable` | MATRIX | 0.331 | 其他 | 0 | — | — | — | UNUSABLE | Accounts payable |
| 694 | `fnd72_s_pit_or_bs_q_bs_acct_payable` | MATRIX | 0.331 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Amounts owed to suppliers or vendors for goods and services received; standard accounts payable liability |
| 695 | `fnd72_pit_or_bs_q_bs_st_debt` | VECTOR | 0.331 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term debt (due within one year) |
| 696 | `fnd72_pit_or_is_a_is_pension_category_debt` | VECTOR | 0.331 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage of pension plan assets allocated to debt instruments |
| 697 | `inventory_total_value_3` | MATRIX | 0.331 | 其他 | 0 | — | — | — | UNUSABLE | Total value of inventory held by the company. |
| 698 | `fnd72_pit_or_is_a_is_expected_return_pension` | VECTOR | 0.330 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected return on pension plan assets |
| 699 | `other_equity_amt` | VECTOR | 0.330 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other equity components not classified elsewhere. |
| 700 | `fnd72_s_pit_or_bs_q_2_bs_other_cur_liab` | MATRIX | 0.329 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Miscellaneous short-term liabilities not separately classified |
| 701 | `fnd72_s_pit_or_bs_q_bs_other_cur_liab` | MATRIX | 0.329 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Miscellaneous short-term liabilities on the balance sheet, including customer deposits, deferred taxes, refunds, or other current obligation |
| 702 | `fnd72_pit_or_is_q_is_foreign_crncy_trans_adj` | VECTOR | 0.327 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Foreign currency translation adjustment (Income Statement) |
| 703 | `other_current_liabilities_11` | VECTOR | 0.326 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current liabilities not classified elsewhere. |
| 704 | `fnd72_s_pit_or_is_a2_is_pension_category_equities` | MATRIX | 0.326 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage of pension plan assets allocated to equities |
| 705 | `fnd72_pit_or_bs_q_bs_accts_rec_excl_notes_rec` | VECTOR | 0.326 | 价量与波动 | 0 | — | — | — | UNUSABLE | Trade accounts receivable excluding notes receivable, net of allowances |
| 706 | `fnd72_s_pit_or_cf_q_cf_decr_invest` | MATRIX | 0.325 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly proceeds from sale or maturity of investments (decrease in investments) |
| 707 | `other_current_liabilities_bs` | MATRIX | 0.325 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current liabilities not classified elsewhere, as reported on the balance sheet. |
| 708 | `other_current_liabilities_total_3` | MATRIX | 0.325 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total value of other current liabilities. |
| 709 | `fnd72_s_pit_or_is_q_tot_int_exp` | MATRIX | 0.325 | 其他 | 0 | — | — | — | UNUSABLE | Total interest expense incurred during the period |
| 710 | `fnd72_s_pit_or_is_a2_is_pension_category_debt` | MATRIX | 0.325 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage of pension plan assets invested in debt instruments |
| 711 | `fnd72_pit_or_cf_q_cf_disp_fix_asset` | VECTOR | 0.324 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash proceeds from disposal of fixed assets |
| 712 | `assets_held_for_sale_2` | VECTOR | 0.324 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets classified as held for sale. |
| 713 | `fnd72_s_pit_or_bs_q_2_bs_accts_rec_excl_notes_rec` | MATRIX | 0.322 | 价量与波动 | 0 | — | — | — | UNUSABLE | Trade accounts receivable excluding notes receivable |
| 714 | `fnd72_s_pit_or_bs_q_bs_accts_rec_excl_notes_rec` | MATRIX | 0.322 | 价量与波动 | 0 | — | — | — | UNUSABLE | Trade accounts receivable excluding notes, net of allowances |
| 715 | `fnd72_pit_or_is_a_is_impairment_goodwill_intangibl` | VECTOR | 0.321 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Impairment charges for goodwill and intangible assets recognized in the quarter |
| 716 | `fnd72_pit_or_cf_q_cf_incr_lt_borrow` | VECTOR | 0.321 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Quarterly cash inflow from increases in long-term borrowings |
| 717 | `fnd72_s_pit_or_cf_q_cf_reimb_lt_borrow` | MATRIX | 0.320 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Quarterly cash outflow for repayment of long-term borrowings |
| 718 | `fnd72_s_pit_or_cf_q_cf_incr_invest` | MATRIX | 0.319 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Quarterly cash outflows for increases or purchases of investments |
| 719 | `fnd72_pit_or_bs_q_bs_accum_depr` | VECTOR | 0.319 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accumulated depreciation on fixed assets |
| 720 | `fnd72_s_pit_or_is_a2_is_rate_of_comp_increase_pension` | MATRIX | 0.318 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Annual assumed rate of employee compensation increase used in pension calculations |
| 721 | `fnd72_pit_or_is_q_is_other_oper_inc` | VECTOR | 0.317 | 其他 | 0 | — | — | — | UNUSABLE | Other operating income recognized during the quarter |
| 722 | `ard_other_noncurrent_liabilities` | MATRIX | 0.317 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other noncurrent liabilities in standardized ARD format. |
| 723 | `other_noncurrent_liabilities_value_2` | MATRIX | 0.317 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of other noncurrent liabilities. |
| 724 | `fnd72_pit_or_bs_q_bs_other_cur_asset_less_prepay` | VECTOR | 0.314 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current assets excluding prepayments (miscellaneous short-term assets) |
| 725 | `fnd72_pit_or_is_a_is_gnrl_and_admin_exp` | VECTOR | 0.313 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly general and administrative expense, adjusted (income statement) |
| 726 | `fnd72_s_pit_or_bs_q_1_notes_receivable` | MATRIX | 0.312 | 其他 | 0 | — | — | — | UNUSABLE | Notes Receivable (Long Term) |
| 727 | `fnd72_s_pit_or_bs_q_notes_receivable` | MATRIX | 0.312 | 其他 | 0 | — | — | — | UNUSABLE | Total notes receivable |
| 728 | `fnd72_pit_or_cf_a_cf_acct_rcv_unbilled_rev` | VECTOR | 0.311 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in accounts receivable, notes receivable, and unbilled revenue used in operating cash flow |
| 729 | `fnd72_s_pit_or_is_a_is_adjusted_eps_as_reported` | MATRIX | 0.310 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Annual adjusted earnings per share as reported by the company |
| 730 | `fnd72_s_pit_or_is_a2_is_adjusted_net_inc_as_reported` | MATRIX | 0.310 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjusted net income as reported by the company |
| 731 | `operating_profit_discontinued_ops` | VECTOR | 0.309 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating profit derived from discontinued operations. |
| 732 | `fnd72_pit_or_bs_q_bs_gross_fix_asset` | VECTOR | 0.308 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross property, plant and equipment (before accumulated depreciation) |
| 733 | `fnd72_s_pit_or_is_q_is_foreign_crncy_trans_adj` | MATRIX | 0.308 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Quarterly foreign currency translation adjustment recognized in other comprehensive income |
| 734 | `fnd72_pit_or_is_q_is_unrealized_gain_loss_comp_inc` | VECTOR | 0.308 | 其他 | 0 | — | — | — | UNUSABLE | Unrealized gains or losses recognized in comprehensive income for the quarter |
| 735 | `fnd72_pit_or_is_q_ox_feb_spe_lid_si` | VECTOR | 0.307 | 其他 | 0 | — | — | — | UNUSABLE | Diluted EPS Before Extraordinary Items |
| 736 | `fnd72_pit_or_bs_q_contingent_liabilities` | VECTOR | 0.306 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Contingent liabilities and commitments |
| 737 | `total_liabilities_value_9` | MATRIX | 0.306 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total value of liabilities reported on the balance sheet. |
| 738 | `fnd72_pit_or_cf_q_cf_cash_paid_for_tax` | VECTOR | 0.306 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Paid for Tax (Cash Flow) |
| 739 | `deferred_tax_liabilities_long_term_2` | MATRIX | 0.306 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liabilities due beyond one year. |
| 740 | `fnd72_pit_or_is_a_is_pension_category_other` | VECTOR | 0.305 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentage of pension plan assets classified as “Other” category, reported quarterly |
| 741 | `fnd72_s_pit_or_cf_q_cf_other_non_cash_adj_less` | MATRIX | 0.305 | 其他 | 0 | — | — | — | UNUSABLE | Other non-cash adjustments excluding specific items |
| 742 | `fnd72_pit_or_bs_q_bs_future_min_oper_lease_oblig` | VECTOR | 0.305 | 其他 | 0 | — | — | — | UNUSABLE | Total future minimum payments under operating lease obligations |
| 743 | `deferred_tax_assets_long_term` | MATRIX | 0.304 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax assets expected to be realized after one year. |
| 744 | `fnd72_pit_or_bs_q_notes_receivable` | VECTOR | 0.304 | 其他 | 0 | — | — | — | UNUSABLE | Promissory notes owed to the company (notes receivable) |
| 745 | `stock_option_cost_after_tax` | MATRIX | 0.302 | 其他 | 0 | — | — | — | UNUSABLE | Cost of stock-based compensation after tax effects. |
| 746 | `fnd72_s_pit_or_is_q_is_other_oper_inc` | MATRIX | 0.301 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly other operating income |
| 747 | `fnd72_pit_or_bs_q_bs_other_cur_liab` | VECTOR | 0.301 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other current liabilities (miscellaneous short-term liabilities) |
| 748 | `fnd72_pit_or_cf_q_cf_other_non_cash_adj_less` | VECTOR | 0.301 | 其他 | 0 | — | — | — | UNUSABLE | Other non-cash adjustments excluding specific items |
| 749 | `inventory_balance_5` | VECTOR | 0.300 | 其他 | 0 | — | — | — | UNUSABLE | Value of goods held for sale or production. |
| 750 | `fnd72_pit_or_bs_a_bs_auth_capital` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Authorized Capital |
| 751 | `fnd72_s_pit_or_cf_q_cf_cash_paid_for_tax` | MATRIX | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly cash paid for taxes |
| 752 | `other_pension_category_income` | MATRIX | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Income or expense from other pension categories. |
| 753 | `fnd72_pit_or_is_q_is_min_pension_liab_adj` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Pension Related Adjust Other Comprehensive Inc |
| 754 | `fnd72_pit_or_is_a_is_adjusted_eps_as_reported` | VECTOR | 0.297 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Company-reported adjusted earnings per share for the period |
| 755 | `fnd72_pit_or_is_a_is_adjusted_net_inc_as_reported` | VECTOR | 0.294 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Company-reported adjusted net income for the quarter |
| 756 | `long_term_deferred_tax_assets` | VECTOR | 0.294 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax assets expected to be realized after one year. |
| 757 | `aggregate_shareholders_equity_4` | VECTOR | 0.294 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Aggregate value of shareholders' equity. |
| 758 | `fnd72_pit_or_is_q_is_over_underfund_pension_exp` | VECTOR | 0.292 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Expense impact related to overfunded or underfunded pension plans recognized on the income statement |
| 759 | `long_term_deferred_tax_liabilities` | VECTOR | 0.292 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liabilities due beyond one year. |
| 760 | `total_liabilities_9` | VECTOR | 0.291 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Sum of all company liabilities, both current and noncurrent. |
| 761 | `fnd72_pit_or_is_q_is_projected_benefit_obligation` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Projected pension benefit obligation (actuarial present value of benefits earned) |
| 762 | `fnd72_q_cf_disp_fix_asset` | MATRIX | 0.289 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash proceeds from the disposal of fixed assets during the quarter |
| 763 | `fnd72_pit_or_bs_q_bs_accrual` | VECTOR | 0.289 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other accounts payable and accrued expenses |
| 764 | `net_nonoperating_income_jv_associates` | VECTOR | 0.289 | 其他 | 0 | — | — | — | UNUSABLE | Net non-operating income from joint ventures and associates. |
| 765 | `income_tax_payable_4` | VECTOR | 0.288 | 其他 | 0 | — | — | — | UNUSABLE | Income taxes accrued but not yet paid. |
| 766 | `trade_accounts_receivable` | VECTOR | 0.286 | 价量与波动 | 0 | — | — | — | UNUSABLE | Amounts owed to the company by customers for sales made on credit. |
| 767 | `fnd72_pit_or_is_q_is_eqy_earn_from_invest_assoc` | VECTOR | 0.285 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity in earnings (loss) from investments in associates for the quarter |
| 768 | `fnd72_pit_or_bs_q_bs_total_capital_leases` | VECTOR | 0.285 | 其他 | 0 | — | — | — | UNUSABLE | Total obligations under capital/finance leases recognized on the balance sheet |
| 769 | `fnd72_s_pit_or_cf_q_cf_incr_lt_borrow` | MATRIX | 0.284 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Increase in long-term borrowings |
| 770 | `ard_accounts_receivable_trade` | MATRIX | 0.284 | 价量与波动 | 0 | — | — | — | UNUSABLE | Trade accounts receivable in standardized ARD format. |
| 771 | `short_term_borrowings_6` | VECTOR | 0.282 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Borrowings due within one year. |
| 772 | `fnd72_pit_or_bs_q_bs_other_inv` | VECTOR | 0.281 | 其他 | 0 | — | — | — | UNUSABLE | Other inventory items and allowances |
| 773 | `shareholders_equity_aggregate_3` | MATRIX | 0.281 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Aggregate value of shareholders' equity. |
| 774 | `total_shareholders_equity_value` | MATRIX | 0.281 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total value of shareholders' equity. |
| 775 | `fnd72_pit_or_bs_q_invtry_finished_goods` | VECTOR | 0.281 | 其他 | 0 | — | — | — | UNUSABLE | Finished goods inventory |
| 776 | `fnd72_pit_or_bs_q_invtry_raw_materials` | VECTOR | 0.280 | 其他 | 0 | — | — | — | UNUSABLE | Raw materials component of inventory |
| 777 | `short_term_borrowings_bs` | MATRIX | 0.279 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Borrowings due within one year as reported on the balance sheet. |
| 778 | `fnd72_s_pit_or_cf_a_cf_incr_st_borrow` | MATRIX | 0.279 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Annual increase/(decrease) in short-term borrowings |
| 779 | `non_equity_reserves_q` | VECTOR | 0.277 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reserves not related to equity, as reported on the quarterly balance sheet. |
| 780 | `fnd72_s_pit_or_cf_a_cf_acct_rcv_unbilled_rev` | MATRIX | 0.277 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in accounts receivable and unbilled revenue affecting operating cash flow |
| 781 | `fnd72_pit_or_is_a_is_expected_return_plan_assets` | VECTOR | 0.276 | 修正与预期 | 0 | — | — | — | UNUSABLE | The estimated expected long-term rate of return on pension plan assets expressed as a percent |
| 782 | `retained_earnings_accumulated_deficit_2` | VECTOR | 0.276 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cumulative net income retained or deficit accumulated by the company. |
| 783 | `fnd72_pit_or_bs_q_invtry_in_progress` | VECTOR | 0.276 | 其他 | 0 | — | — | — | UNUSABLE | Work-in-progress inventory |
| 784 | `fnd72_pit_or_bs_q_bs_st_portion_of_lt_debt` | VECTOR | 0.275 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current (short-term) portion of long-term debt due within one year |
| 785 | `intangible_assets_net_5` | MATRIX | 0.275 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net value of intangible assets such as patents and trademarks. |
| 786 | `total_intangible_assets_net_value` | MATRIX | 0.275 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net value of all intangible assets. |
| 787 | `fnd72_pit_or_is_q_is_rd_expend` | VECTOR | 0.274 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development expense |
| 788 | `fnd72_pit_or_is_a_is_act_ret_loss_pension_plan_ast` | VECTOR | 0.273 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual return or loss on pension plan assets during the period |
| 789 | `trade_accounts_payable_2` | VECTOR | 0.273 | 价量与波动 | 0 | — | — | — | UNUSABLE | Amounts owed to suppliers for goods and services received. |
| 790 | `fnd72_s_pit_or_is_a2_is_expected_return_pension` | MATRIX | 0.272 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The component of net pension expense that pertains to the expected return on pension plan assets |
| 791 | `fnd72_pit_or_is_a_is_cost_of_matl` | VECTOR | 0.272 | 其他 | 0 | — | — | — | UNUSABLE | Cost of materials expense for the quarter |
| 792 | `fnd72_pit_or_is_q_eff_int_rate` | VECTOR | 0.271 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Effective interest rate for the reporting period |
| 793 | `derivative_assets_short_term_amt` | VECTOR | 0.271 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term derivative assets reported on the balance sheet. |
| 794 | `net_intangible_assets` | VECTOR | 0.271 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net value of intangible assets such as patents and trademarks. |
| 795 | `income_tax_accrued_payable` | MATRIX | 0.271 | 其他 | 0 | — | — | — | UNUSABLE | Income taxes accrued but not yet paid. |
| 796 | `ard_retained_earnings_accum_deficit_dup` | MATRIX | 0.271 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Retained earnings or accumulated deficit in standardized ARD format (duplicate field). |
| 797 | `common_stock_balance` | VECTOR | 0.270 | 其他 | 0 | — | — | — | UNUSABLE | Value of common stock issued and outstanding. |
| 798 | `fnd72_s_pit_or_is_q_is_rd_expend` | MATRIX | 0.270 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development expenses for the period |
| 799 | `joint_venture_associate_net_non_operating` | MATRIX | 0.270 | 其他 | 0 | — | — | — | UNUSABLE | Net non-operating income or loss from joint ventures and associates. |
| 800 | `long_term_debt_bs` | MATRIX | 0.270 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Outstanding balance of debt obligations due beyond one year, as reported on the balance sheet. |
| 801 | `fnd72_pit_or_is_a_amort_of_goodwill` | VECTOR | 0.270 | 其他 | 0 | — | — | — | UNUSABLE | Amortization Of Goodwill |
| 802 | `fnd72_s_pit_or_is_q_is_unrealized_gain_loss_comp_inc` | MATRIX | 0.270 | 其他 | 0 | — | — | — | UNUSABLE | Unrealized gain or loss in comprehensive income for the quarter |
| 803 | `fnd72_pit_or_bs_q_bs_common_stock` | VECTOR | 0.269 | 其他 | 0 | — | — | — | UNUSABLE | Common stock (par value of issued common shares) |
| 804 | `fnd72_pit_or_bs_q_lt_capital_lease_obligations` | VECTOR | 0.269 | 其他 | 0 | — | — | — | UNUSABLE | Long-term portion of capital/finance lease obligations |
| 805 | `trade_accounts_payable_bs` | MATRIX | 0.268 | 价量与波动 | 0 | — | — | — | UNUSABLE | Amounts owed to suppliers for goods and services received, as reported on the balance sheet. |
| 806 | `fnd72_pit_or_bs_q_bs_rental_exp_year_1` | VECTOR | 0.268 | 其他 | 0 | — | — | — | UNUSABLE | Rental expense year 1 |
| 807 | `fnd72_pit_or_bs_q_bs_options_outstanding` | VECTOR | 0.267 | 其他 | 0 | — | — | — | UNUSABLE | Options outstanding at end of period |
| 808 | `long_term_debt_balance_2` | VECTOR | 0.267 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Outstanding balance of debt obligations due beyond one year. |
| 809 | `fnd72_pit_or_is_q_is_inc_tax_exp_other_comp_inc` | VECTOR | 0.266 | 其他 | 0 | — | — | — | UNUSABLE | Income tax related to items recorded in other comprehensive income for the quarter |
| 810 | `fnd72_pit_or_bs_q_st_capital_lease_obligations` | VECTOR | 0.264 | 其他 | 0 | — | — | — | UNUSABLE | Short-term capital lease obligations due within one year |
| 811 | `fnd72_pit_or_is_q_is_special_eps` | VECTOR | 0.263 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Special earnings per share |
| 812 | `fnd72_s_pit_or_is_q_is_special_eps` | MATRIX | 0.263 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Special earnings per share |
| 813 | `fnd72_pit_or_bs_q_bs_rental_exp_beyond_year_5` | VECTOR | 0.261 | 其他 | 0 | — | — | — | UNUSABLE | Rental/lease expense commitments scheduled beyond year five |
| 814 | `added_value_income` | VECTOR | 0.260 | 其他 | 0 | — | — | — | UNUSABLE | Value created by the company after deducting input costs from output. |
| 815 | `fnd72_s_pit_or_is_q_is_eqy_earn_from_invest_assoc` | MATRIX | 0.259 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity in earnings or losses from investments in associates accounted for under the equity method |
| 816 | `total_shares_issued_8` | VECTOR | 0.258 | 其他 | 0 | — | — | — | UNUSABLE | Total number of shares issued and outstanding. |
| 817 | `fnd72_s_pit_or_is_q_eff_int_rate` | MATRIX | 0.257 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Effective interest rate |
| 818 | `fnd72_pit_or_is_q_is_fair_value_plan_assets` | VECTOR | 0.255 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fair value of pension plan assets |
| 819 | `fnd72_s_pit_or_is_a_is_cost_of_matl` | MATRIX | 0.255 | 其他 | 0 | — | — | — | UNUSABLE | Cost of materials |
| 820 | `value_added_income` | MATRIX | 0.254 | 其他 | 0 | — | — | — | UNUSABLE | Value created by the company after deducting input costs from output. |
| 821 | `pension_expense_real_estate` | VECTOR | 0.254 | 其他 | 0 | — | — | — | UNUSABLE | Pension-related expense for real estate activities. |
| 822 | `fnd72_pit_or_cf_q_cf_net_cash_paid_for_aquis` | VECTOR | 0.252 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Cash Paid for Acquisitions (Cash Flow Statement) |
| 823 | `fnd72_s_pit_or_bs_q_2_bs_common_stock` | MATRIX | 0.215 | 其他 | 0 | — | — | — | UNUSABLE | Par or stated value of common stock issued |
| 824 | `fnd72_s_pit_or_bs_q_bs_common_stock` | MATRIX | 0.215 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly value of common stock, generally calculated as par or stated value times shares issued |
| 825 | `ardr_retained_earnings_accum_deficit` | MATRIX | 0.213 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Retained earnings or accumulated deficit in standardized ARD format. |
| 826 | `retained_earnings_or_deficit_value` | MATRIX | 0.213 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of retained earnings or accumulated deficit. |
| 827 | `ard_common_stock` | MATRIX | 0.202 | 其他 | 0 | — | — | — | UNUSABLE | Common stock value in standardized ARD format. |
| 828 | `common_stock_value` | MATRIX | 0.202 | 其他 | 0 | — | — | — | UNUSABLE | Value of common stock reported on the balance sheet. |
| 829 | `fnd72_s_pit_or_bs_q_1_bs_st_portion_of_lt_debt` | MATRIX | 0.200 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current portion of long-term debt due within one year |
| 830 | `fnd72_s_pit_or_bs_q_bs_st_portion_of_lt_debt` | MATRIX | 0.200 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Short-term portion of long-term debt due within one year |
| 831 | `fnd72_s_pit_or_bs_q_2_bs_accrual` | MATRIX | 0.200 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other accounts payable and accrued liabilities within current liabilities |
| 832 | `fnd72_s_pit_or_bs_q_bs_accrual` | MATRIX | 0.200 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other accounts payable and accrued liabilities for the quarter |
| 833 | `fnd72_s_pit_or_is_q_is_personnel_exp` | MATRIX | 0.198 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly personnel expenses (wages, salaries, benefits, and related costs) |
| 834 | `fnd72_s_pit_or_cf_q_cf_issue_com_stock` | MATRIX | 0.197 | 其他 | 0 | — | — | — | UNUSABLE | Cash from issuance of common stock |
| 835 | `fnd72_s_pit_or_cf_q_cf_act_cash_paid_for_int_debt` | MATRIX | 0.194 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual cash paid for interest on debt |
| 836 | `short_term_provisions_3` | MATRIX | 0.192 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Provisions for liabilities expected to be settled within one year. |
| 837 | `short_term_provisions_value` | MATRIX | 0.192 | 其他 | 0 | — | — | — | UNUSABLE | Value of short-term provisions reported on the balance sheet. |
| 838 | `fnd72_s_pit_or_bs_q_2_bs_add_paid_in_cap` | MATRIX | 0.191 | 其他 | 0 | — | — | — | UNUSABLE | Additional paid-in capital (share premium) |
| 839 | `fnd72_s_pit_or_bs_q_bs_add_paid_in_cap` | MATRIX | 0.191 | 其他 | 0 | — | — | — | UNUSABLE | Additional paid-in capital (share premium over par value) |
| 840 | `investments_in_affiliates_joint_ventures` | MATRIX | 0.191 | 其他 | 0 | — | — | — | UNUSABLE | Investments held in affiliated companies and joint ventures. |
| 841 | `cumulative_translation_adjustment_value` | MATRIX | 0.189 | 其他 | 0 | — | — | — | UNUSABLE | Value of cumulative translation adjustment on the balance sheet. |
| 842 | `other_intangible_assets_3` | MATRIX | 0.188 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Intangible assets not classified elsewhere, such as licenses or copyrights. |
| 843 | `other_long_term_assets_3` | MATRIX | 0.187 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets not classified elsewhere that are expected to provide value beyond one year. |
| 844 | `other_noncurrent_assets_3` | MATRIX | 0.187 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets not classified elsewhere that are expected to provide value beyond one year. |
| 845 | `minimum_pension_liability_adjustment_5` | MATRIX | 0.183 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Adjustment for minimum pension liability in the income statement. |
| 846 | `ebitda_rental_adjusted` | MATRIX | 0.180 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings before interest, taxes, depreciation, amortization, and rent. |
| 847 | `pension_postretirement_liabilities` | MATRIX | 0.176 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liabilities related to pension and post-retirement benefits. |
| 848 | `fnd72_s_pit_or_is_q_is_inc_tax_exp_other_comp_inc` | MATRIX | 0.171 | 其他 | 0 | — | — | — | UNUSABLE | Income tax expense related to items in Other Comprehensive Income |
| 849 | `fnd72_s_pit_or_bs_q_2_invtry_finished_goods` | MATRIX | 0.169 | 其他 | 0 | — | — | — | UNUSABLE | Value of finished goods component of inventory |
| 850 | `fnd72_s_pit_or_bs_q_invtry_finished_goods` | MATRIX | 0.169 | 其他 | 0 | — | — | — | UNUSABLE | Value of finished goods inventory |
| 851 | `fnd72_s_pit_or_bs_q_2_bs_accrued_income_taxes` | MATRIX | 0.168 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Income taxes accrued but not yet paid (current liability) |
| 852 | `fnd72_s_pit_or_bs_q_bs_accrued_income_taxes` | MATRIX | 0.168 | 其他 | 0 | — | — | — | UNUSABLE | Accrued income taxes payable |
| 853 | `common_stock_issued` | MATRIX | 0.168 | 其他 | 0 | — | — | — | UNUSABLE | Value of common stock issued by the company. |
| 854 | `fnd72_s_pit_or_bs_q_2_invtry_raw_materials` | MATRIX | 0.168 | 其他 | 0 | — | — | — | UNUSABLE | Value of raw materials component of inventory |
| 855 | `fnd72_s_pit_or_bs_q_invtry_raw_materials` | MATRIX | 0.168 | 其他 | 0 | — | — | — | UNUSABLE | Inventory of raw materials |
| 856 | `fnd72_s_pit_or_bs_q_2_bs_other_inv` | MATRIX | 0.168 | 其他 | 0 | — | — | — | UNUSABLE | Other inventory |
| 857 | `fnd72_s_pit_or_bs_q_bs_other_inv` | MATRIX | 0.168 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly value of other inventory/allowances not otherwise classified |
| 858 | `fnd72_s_pit_or_bs_q_2_invtry_in_progress` | MATRIX | 0.166 | 其他 | 0 | — | — | — | UNUSABLE | Inventory work in progress |
| 859 | `fnd72_s_pit_or_bs_q_invtry_in_progress` | MATRIX | 0.166 | 其他 | 0 | — | — | — | UNUSABLE | Inventory in progress (work in process) for the quarter |
| 860 | `ard_additional_paid_in_capital` | MATRIX | 0.165 | 其他 | 0 | — | — | — | UNUSABLE | Additional paid-in capital in standardized ARD format. |
| 861 | `fnd72_s_pit_or_is_q_is_cogs_to_fe_and_pp_and_g` | MATRIX | 0.165 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly cost of revenue (cost of goods sold and related) |
| 862 | `fnd72_s_pit_or_bs_q_2_contingent_liabilities` | MATRIX | 0.156 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Contingent Liabilities and Commitments |
| 863 | `fnd72_s_pit_or_bs_q_contingent_liabilities` | MATRIX | 0.156 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quarterly disclosed liabilities dependent on uncertain future events (e.g., guarantees, legal disputes, commitments) |
| 864 | `fnd72_s_pit_or_bs_q_1_bs_accum_depr` | MATRIX | 0.156 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accumulated depreciation on fixed assets |
| 865 | `fnd72_s_pit_or_bs_q_bs_accum_depr` | MATRIX | 0.156 | 其他 | 0 | — | — | — | UNUSABLE | Cumulative depreciation on property, plant and equipment |
| 866 | `miscellaneous_reserves` | MATRIX | 0.156 | 其他 | 0 | — | — | — | UNUSABLE | Reserves set aside for various unspecified purposes on the balance sheet. |
| 867 | `other_reserves_bs` | MATRIX | 0.156 | 其他 | 0 | — | — | — | UNUSABLE | Reserves set aside for various unspecified purposes, as reported on the balance sheet. |
| 868 | `fnd72_s_pit_or_is_q_cni_tni_si` | MATRIX | 0.154 | 其他 | 0 | — | — | — | UNUSABLE | Quarterly interest income |
| 869 | `fnd72_s_pit_or_is_q_is_interest_inc` | MATRIX | 0.154 | 其他 | 0 | — | — | — | UNUSABLE | Interest income for the period |
| 870 | `ardr_additional_paid_in_capital` | MATRIX | 0.153 | 其他 | 0 | — | — | — | UNUSABLE | Additional paid-in capital in standardized ARD format. |
| 871 | `fnd72_s_pit_or_cf_q_cf_net_cash_paid_for_aquis` | MATRIX | 0.153 | 其他 | 0 | — | — | — | UNUSABLE | Net cash paid for acquisitions |
| 872 | `fnd72_q_1_bs_gross_fix_asset` | MATRIX | 0.152 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross carrying amount of property, plant and equipment before accumulated depreciation |
| 873 | `fnd72_q_bs_gross_fix_asset` | MATRIX | 0.152 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross carrying amount of property, plant and equipment before depreciation |
| 874 | `fnd72_s_pit_or_cf_a_cf_def_of_fund` | MATRIX | 0.152 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Not found in the BBO Field Dictionary |
| 875 | `real_estate_pension_category_income` | MATRIX | 0.151 | 其他 | 0 | — | — | — | UNUSABLE | Income or expense from real estate pension category. |
| 876 | `par_value_of_shares` | MATRIX | 0.151 | 其他 | 0 | — | — | — | UNUSABLE | Nominal value assigned to each share of stock. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

