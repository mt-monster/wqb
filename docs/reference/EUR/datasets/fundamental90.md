# fundamental90 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental90` |
| 名称 | Governance, Accounting, Management, and Equality |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 66 |
| 覆盖率 | 0.4825 |
| 平台已有 alpha | 81 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides quantitative model outputs for global equities, leveraging a model ensemble meta-algorithm that combines robust linear regression and a modified xgBoost classification approach. It includes a wide array of fundamental, accounting, governance, and management quality signals, as well as risk and event indicators such as bankruptcy, fraud, and executive turnover. The model is designed to predict three-month ahead stock returns and the likelihood of negative corporate events, offering daily cross-sectional scores and risk metrics. By integrating these diverse factors, the dataset enables users to identify stocks with superior governance, accounting quality, and management efficiency, as well as to anticipate adverse events, making it a powerful tool for forecasting price 

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **66** |
| 类型分布 | MATRIX×66 |
| 平均覆盖率 | **0.483** |
| 覆盖率区间 | 0.19 ~ 0.58 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 41 | 62.1% |
| 稀疏 (<0.50) | 25 | 37.9% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 66 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 66 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 43 | 0.48 | fnd90_qes_gamef_mohanram、fnd90_qes_gamef_negative_earnings、fnd90_game_serial_special |
| 风险与质量 | 7 | 0.46 | fnd90_qes_gamef_cscore、fnd90_qes_gamef_ohlson、fnd90_qes_gamef_score |
| 修正与预期 | 6 | 0.44 | fnd90_game_optimism_sale、fnd90_game_deferred_tax_liab_chg、fnd90_game_eps_sur_vol |
| 价量与波动 | 4 | 0.53 | fnd90_game_relative_rtn_vol、fnd90_qes_gamef_cashflow_var、fnd90_game_sg_a_vol |
| 其他 | 3 | 0.57 | fnd90_game_receivable_chg、fnd90_game_receivable_days、fnd90_game_sg_a_inefficiency |
| 宏观与行业 | 2 | 0.41 | fnd90_game_tax_rate、fnd90_game_amortization_rate |
| 持仓与资金流 | 1 | 0.58 | fnd90_qes_gamef_pscore |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `fnd90_qes_gamef_cscore` | MATRIX | 0.579 | 风险与质量 | 0 | — | — | — | UNUSABLE | Montier’s C-score, an integer-based composite designed to flag accounting manipulation or fraud risk (higher is more risk) |
| 2 | `fnd90_qes_gamef_mohanram` | MATRIX | 0.579 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mohanram “G-score” assessing risk of earnings manipulation in growth stocks (higher indicates greater fraud or earnings risk) |
| 3 | `fnd90_qes_gamef_pscore` | MATRIX | 0.579 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Piotroski F-score (0–9), a composite accounting quality score based on fundamental signals; higher values indicate better accounting quality |
| 4 | `fnd90_game_relative_rtn_vol` | MATRIX | 0.579 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volatility of a security’s returns relative to a benchmark or peers, representing relative risk or instability of stock returns |
| 5 | `fnd90_qes_gamef_negative_earnings` | MATRIX | 0.577 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Frequency or indicator of negative earnings occurrences for the entity; higher numbers suggest more frequent negative earnings results |
| 6 | `fnd90_game_receivable_chg` | MATRIX | 0.574 | 其他 | 0 | — | — | — | UNUSABLE | Change in receivables (typically quarter-over-quarter or year-over-year), showing how much accounts receivable increased or decreased, refle |
| 7 | `fnd90_game_receivable_days` | MATRIX | 0.574 | 其他 | 0 | — | — | — | UNUSABLE | Number of days, on average, it takes a company to collect receivables from customers; a measure of working capital efficiency |
| 8 | `fnd90_game_serial_special` | MATRIX | 0.574 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total of special (non-recurring/one-off) accounting items as a proportion of sales, highlighting the prevalence of such adjustments and pote |
| 9 | `nonliquid_asset_ratio` | MATRIX | 0.573 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of illiquid assets (such as plant, equipment, intangibles, or other hard-to-sell assets) to total assets, indicating potential capital |
| 10 | `fnd90_game_other_asset_gr` | MATRIX | 0.573 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other Asset Growth [ Descending] - [Quality.Capital utilization] |
| 11 | `fnd90_game_equity_dilution` | MATRIX | 0.572 | 盈利与财务 | 0 | — | — | — | UNUSABLE | An indicator of new equity issuance or dilution, such as through new share issuance or conversion of convertibles, reflecting risk of owners |
| 12 | `fnd90_qes_gamef_ohlson` | MATRIX | 0.571 | 风险与质量 | 0 | — | — | — | UNUSABLE | Ohlson O-score, a bankruptcy prediction model score; higher scores indicate higher risk of bankruptcy for a company |
| 13 | `fnd90_game_asset_turnover_chg` | MATRIX | 0.570 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The change in asset turnover ratio (typically sales/assets), reflecting improvement or deterioration in capital utilization over time |
| 14 | `fnd90_game_tax_rate` | MATRIX | 0.569 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Effective tax rate, with lower rates possibly indicating aggressive accounting or tax minimization strategies |
| 15 | `fnd90_game_noa` | MATRIX | 0.569 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Operating Assets; represents the company's operating assets minus operating liabilities, indicating capital employed in operations |
| 16 | `fnd90_qes_gamef_score` | MATRIX | 0.567 | 风险与质量 | 0 | — | — | — | UNUSABLE | SCORE |
| 17 | `fnd90_qes_gamef_cashflow_var` | MATRIX | 0.566 | 价量与波动 | 0 | — | — | — | UNUSABLE | Variability (volatility) of operating cashflows; higher values indicate more unpredictable or volatile cashflow generation, which means high |
| 18 | `fnd90_game_optimism_sale` | MATRIX | 0.558 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst Optimism Sales [ Descending] - [Quality.Profitability] |
| 19 | `fnd90_game_sg_a_inefficiency` | MATRIX | 0.558 | 其他 | 0 | — | — | — | UNUSABLE | Level of inefficiency in SG&A (Selling, General & Administrative) expenses; higher values suggest less efficient management of overhead cost |
| 20 | `fnd90_game_sg_a_cost_ratio` | MATRIX | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Selling, General, & Administrative (SG&A) expenses as a ratio to a base (likely sales or revenue), measuring company efficiency in overhead  |
| 21 | `fnd90_game_capex_sale` | MATRIX | 0.552 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of capital expenditures to sales, indicating investment intensity compared to revenue generation |
| 22 | `fnd90_qes_gamef_chs_default` | MATRIX | 0.547 | 风险与质量 | 0 | — | — | — | UNUSABLE | Standardized probability of bankruptcy/default (z-score) based on the Campbell, Hilscher, Szilagyi model; higher values = greater default ri |
| 23 | `fnd90_qes_gamef_earn_var` | MATRIX | 0.543 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings variability, typically representing the standard deviation or volatility of a company's earnings over a period; higher values indic |
| 24 | `fnd90_game_inc_cash_tax` | MATRIX | 0.541 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of tax expense per income statement to actual cash taxes paid, designed to highlight aggressive tax recognition or earnings quality re |
| 25 | `fnd90_game_pension_expense` | MATRIX | 0.541 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Pension-related expense scaled by EBITDA, where higher values indicate greater pension-related liability risk |
| 26 | `fnd90_qes_gamef_grossprofit_asset` | MATRIX | 0.536 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross profit divided by total assets, a quality/profitability metric where higher values indicate better profitability |
| 27 | `fnd90_game_cash_flow_coverage` | MATRIX | 0.535 | 盈利与财务 | 0 | — | — | — | UNUSABLE | A ratio measuring how well a company's operating cash flow covers its obligations (likely total debt or interest); higher values signal stro |
| 28 | `fnd90_game_payble_days` | MATRIX | 0.533 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average number of days the company takes to pay its suppliers (accounts payable days); a higher value means slower payments, which could ind |
| 29 | `fnd90_game_gma_chg` | MATRIX | 0.532 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in gross margin (as a percentage or ratio) from one period to the next, capturing improvement or deterioration in efficiency |
| 30 | `fnd90_game_gross_margin_vol` | MATRIX | 0.532 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Volatility in gross margin over time; high volatility signals instability or unpredictability in profitability, indicating potential busines |
| 31 | `fnd90_game_earning_smooth` | MATRIX | 0.532 | 盈利与财务 | 0 | — | — | — | UNUSABLE | A measure of how stable or "smooth" reported earnings are over time, potentially capturing both persistent profitability or possible earning |
| 32 | `fnd90_game_sg_a_vol` | MATRIX | 0.529 | 价量与波动 | 0 | — | — | — | UNUSABLE | Volatility or variability in SG&A expenses over time, with higher values indicating instability or unpredictability in overhead costs, which |
| 33 | `fnd90_qes_gamef_icfroe_1y` | MATRIX | 0.528 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Incremental Cash Flow Return on Equity over the past 1 year; higher values indicate stronger cash generation relative to equity for the rece |
| 34 | `fnd90_game_deferred_tax_liab_chg` | MATRIX | 0.524 | 修正与预期 | 0 | — | — | — | UNUSABLE | The period-over-period change in deferred tax liabilities, indicating shifts in future tax obligations possibly due to accounting policies o |
| 35 | `fnd90_game_eps_vol` | MATRIX | 0.516 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Volatility (standard deviation) of earnings per share over a period, with higher values indicating unstable profitability |
| 36 | `fnd90_game_labor_efficiency_chg` | MATRIX | 0.516 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Period-to-period change in labor efficiency (e.g., revenue or profit per employee), with increases reflecting greater efficiency |
| 37 | `fnd90_game_short_term_debt` | MATRIX | 0.516 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of short-term (due within one year) debt to a base (likely total assets or capitalization), indicating near-term financial leverage or |
| 38 | `fnd90_game_total_debt_chg` | MATRIX | 0.510 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in total debt balance (period-over-period), measuring increases or decreases in company leverage |
| 39 | `fnd90_game_deferred_tax_asset_chg` | MATRIX | 0.505 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The period-over-period change in the amount of deferred tax assets on the balance sheet, reflecting adjustments or aggressive accounting in  |
| 40 | `fnd90_qes_gamef_icfroe_3y` | MATRIX | 0.503 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Incremental Cash Flow Return on Equity over the past 3 years; higher values indicate stronger multi-year cash flow returns relative to equit |
| 41 | `fnd90_game_non_oper_inc` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Non-operating income as a share of EBITDA, highlighting the proportion of earnings derived from sources outside the core business; higher ra |
| 42 | `fnd90_game_interest_investment_inc` | MATRIX | 0.496 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The amount of income earned from interest and investments, as opposed to operating earnings, which might distort quality of earnings if high |
| 43 | `fnd90_game_eps_sur_vol` | MATRIX | 0.487 | 修正与预期 | 0 | — | — | — | UNUSABLE | Volatility of analyst EPS (earnings per share) forecast errors, reflecting the unpredictability or low quality of reported earnings versus m |
| 44 | `fnd90_game_eff_interest_rate` | MATRIX | 0.480 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The effective interest rate experienced by the company, representing the cost of debt factoring in all forms of financing; higher rates sign |
| 45 | `fnd90_qes_gamef_icfroe_5y` | MATRIX | 0.480 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Incremental Cash Flow Return on Equity over the past 5 years; higher values indicate sustained cash flow return performance relative to equi |
| 46 | `fnd90_game_optimism_gma` | MATRIX | 0.477 | 修正与预期 | 0 | — | — | — | UNUSABLE | Analyst Optimism Gross Margin [ Descending] - [Quality.Profitability] |
| 47 | `fnd90_game_non_production_asset` | MATRIX | 0.451 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Amount or ratio of company assets not directly tied to production or core operations (such as investments, property held for sale); higher v |
| 48 | `fnd90_game_inventory_chg` | MATRIX | 0.448 | 风险与质量 | 0 | — | — | — | UNUSABLE | Change in company inventory levels over a specific period, typically quarter-over-quarter or year-over-year, reflecting working capital chan |
| 49 | `fnd90_game_inventory_days` | MATRIX | 0.448 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of days inventory remains on hand before being sold, calculated as inventory divided by average daily sales; a higher value suggests  |
| 50 | `fnd90_game_accruals_vol` | MATRIX | 0.422 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The volatility of accounting accruals, measuring variability in accruals over time; higher values indicate greater manipulation or lower ear |
| 51 | `fnd90_game_pension_ev` | MATRIX | 0.412 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of pension and other post-employment benefit obligations to total enterprise value; higher values mean greater pension-related liabili |
| 52 | `fnd90_game_minority_interest` | MATRIX | 0.391 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The ratio of minority interest (equity attributable to non-controlling shareholders in subsidiaries) to total equity; higher values may refl |
| 53 | `fnd90_game_prepaid_expense` | MATRIX | 0.388 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of prepaid expenses to sales, indicating the extent of accounting items paid in advance relative to revenue, which may signal aggressi |
| 54 | `fnd90_game_pension_debt_equi_pbo` | MATRIX | 0.380 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of the company's net pension benefit obligation (PBO) expressed as debt equivalent; a higher value indicates greater pension-related f |
| 55 | `fnd90_game_pension_pbo` | MATRIX | 0.378 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of projected pension benefit obligations (pension liabilities) to total enterprise value, indicating pension-related financial risk |
| 56 | `fnd90_game_deferred_sal_chg` | MATRIX | 0.345 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The period-over-period change in deferred revenue (sales received but not yet recognized), which may reflect aggressive revenue recognition  |
| 57 | `fnd90_game_finished_goods` | MATRIX | 0.341 | 风险与质量 | 0 | — | — | — | UNUSABLE | Ratio of finished goods to total inventory, indicating the proportion of inventory in final form; higher values may signal slow sales, overp |
| 58 | `fnd90_game_depreciation_chg` | MATRIX | 0.336 | 修正与预期 | 0 | — | — | — | UNUSABLE | The change in the depreciation rate (either method or level), which can indicate changes in accounting estimate or potential earnings manage |
| 59 | `fnd90_game_pension_interest` | MATRIX | 0.336 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest cost component of pension expense, representing the increase in projected pension liability due to the passage of time |
| 60 | `fnd90_game_capex_dep` | MATRIX | 0.335 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of capital expenditures to depreciation, with higher values indicating more aggressive reinvestment relative to asset aging |
| 61 | `fnd90_game_pension_discount_rate` | MATRIX | 0.306 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The discount rate used to calculate the present value of pension obligations; higher values may indicate more aggressive accounting practice |
| 62 | `fnd90_game_an_cov_chng` | MATRIX | 0.282 | 修正与预期 | 0 | — | — | — | UNUSABLE | Period-over-period change in the number of financial analysts covering the company, positive values indicate increasing analyst attention |
| 63 | `fnd90_qes_gamef_earnigs_timeliness` | MATRIX | 0.274 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Z-score measuring the timeliness of a company's earnings releases, where higher values typically indicate quicker (more timely) earnings rep |
| 64 | `fnd90_game_amortization_rate` | MATRIX | 0.255 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Amortization Rate |
| 65 | `fnd90_game_contingent_liab` | MATRIX | 0.226 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The ratio of contingent liabilities (potential future obligations) to equity, indicating off-balance-sheet or unrecognized risk; higher valu |
| 66 | `fnd90_game_esop_grant` | MATRIX | 0.185 | 风险与质量 | 0 | — | — | — | UNUSABLE | ESOP grants [ ] - [Quality.Capital structure] |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

