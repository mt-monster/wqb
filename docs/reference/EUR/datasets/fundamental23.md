# fundamental23 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental23` |
| 名称 | Fundamental Point in Time Data |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 2332 |
| 覆盖率 | 0.6641 |
| 平台已有 alpha | 1585 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides point-in-time, globally standardized fundamental financial data for over 60,000 companies, including both active and inactive firms, with daily granularity. It includes original and restated values for income statements, balance sheets, and cash flow statements, as well as business and geographic segment data, ratios, and company metadata. The point-in-time structure eliminates forward-looking and survivorship biases, enabling accurate historical backtesting and model development. With coverage dating back to 1989 for US companies and 1997 for non-US, this dataset is essential for constructing robust factor models, event studies, and alpha signals based on true historical financials, supporting reliable prediction of price movements and risk assessment.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **2332** |
| 类型分布 | MATRIX×2318　VECTOR×14 |
| 平均覆盖率 | **0.664** |
| 覆盖率区间 | 0.15 ~ 1.00 |
| 更新频率（推断） | 低频（季/年） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 407 | 17.5% |
| 中 (0.70–0.90) | 818 | 35.1% |
| 低 (0.50–0.70) | 446 | 19.1% |
| 稀疏 (<0.50) | 661 | 28.3% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 1468 | 63.0% |
| UNUSABLE | 855 | 36.7% |
| DEAD_STATIC | 9 | 0.4% |

- 已实测字段：**9** 个（0%），best_sharpe 最高 **1.61**，中位 -0.28

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 1086 | 0.64 | accounts_receivable_total_5、fnd23_tot_inventory、accrued_interest_payable |
| 盈利与财务 | 1027 | 0.71 | fnd23_debt_issuance、fnd23_net_income、fnd23_tot_assets |
| 宏观与行业 | 69 | 0.59 | currency_of_converted_financials、converted_financial_currency、annual_reporting_currency_code |
| 持仓与资金流 | 52 | 0.57 | total_financing_cash_flow、operating_cashflow、bank_borrowings_total |
| 价量与波动 | 44 | 0.51 | accrued_accounts_receivable、trade_payables_short_term、fnd23_intfvalld1_eote |
| 搜索与替代数据 | 24 | 0.47 | fnd23_intfvm_tnoe、fnd23_annfv1a_tnoe、environmental_social_governance_expense |
| 元数据与非信号 | 15 | 0.35 | fnd23_topic1、fnd23_intfvm_saie、fnd23_intfvm_vdav |
| 风险与质量 | 7 | 0.76 | extraordinary_net_income_credits、fnd23_annfv1a_atda、fnd23_intfvm_atda |
| 修正与预期 | 5 | 0.81 | fnd23_annfv1a_tdbl、fnd23_intfvm_tdbl、fnd23_annfvalld1_tdbl |
| 情绪与新闻 | 2 | 0.64 | fnd23_headline、fnd23_headlinefull |
| 交易与微观结构 | 1 | 1.00 | fnd23_repnotickermap |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `total_financing_cash_flow` | MATRIX | 0.932 | 持仓与资金流 | 7 | 1.61 | 2.25 | 0.93 | DEAD_STATIC | [Quarterly] Cash from Financing Activities |
| 2 | `fnd23_debt_issuance` | MATRIX | 0.835 | 盈利与财务 | 1 | 0.75 | 1.36 | 0.64 | DEAD_STATIC | debt issuance |
| 3 | `operating_cashflow` | MATRIX | 0.755 | 持仓与资金流 | 2 | 0.55 | 0.98 | 0.17 | DEAD_STATIC | Net cash generated from operating activities during the period. |
| 4 | `accounts_receivable_total_5` | MATRIX | 0.873 | 其他 | 1 | 0.46 | -0.20 | 0.50 | DEAD_STATIC | Total accounts receivable as of the reporting date. |
| 5 | `fnd23_tot_inventory` | MATRIX | 0.899 | 其他 | 1 | -0.28 | -0.11 | -0.15 | DEAD_STATIC | total inventory. |
| 6 | `accrued_interest_payable` | MATRIX | 0.891 | 其他 | 1 | -0.29 | 0.19 | -0.31 | DEAD_STATIC | Interest expense that has been accrued but not yet paid. |
| 7 | `accounts_payable_4` | MATRIX | 0.843 | 其他 | 1 | -0.49 | -0.75 | -0.52 | DEAD_STATIC | [Quarterly] Accounts Payable |
| 8 | `accrued_accounts_receivable` | MATRIX | 0.828 | 价量与波动 | 1 | -0.76 | -1.19 | -0.54 | DEAD_STATIC | [Quarterly] Accounts Receivable - Trade, Net |
| 9 | `accrued_cash_equivalents` | MATRIX | 0.867 | 其他 | 1 | -0.87 | -0.86 | -0.70 | DEAD_STATIC | [Quarterly] Cash & Equivalents |
| 10 | `fnd23_repnotickermap` | MATRIX | 1.000 | 交易与微观结构 | 0 | — | — | — | UNTESTED | maps each rep to a ticker on a given day. |
| 11 | `fnd23_net_income` | MATRIX | 0.985 | 盈利与财务 | 0 | — | — | — | UNTESTED | net income |
| 12 | `fnd23_tot_assets` | MATRIX | 0.982 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets. |
| 13 | `fnd23_roe` | MATRIX | 0.982 | 盈利与财务 | 0 | — | — | — | UNTESTED | return on equity |
| 14 | `fnd23_aor` | MATRIX | 0.981 | 盈利与财务 | 0 | — | — | — | UNTESTED | return on assets |
| 15 | `fnd23_intfvalld1_tbie` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents a company's total revenues reduced by total expenses, before taxes on net income and all after-tax adjustment |
| 16 | `fnd23_intfvalld1_cnin` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes, adjusted by minority interest, equity in affiliates, the U.S. GAAP adjustment and extraordinary |
| 17 | `fnd23_intfvalld1_swds` | MATRIX | 0.964 | 其他 | 0 | — | — | — | UNTESTED | Diluted Weighted Average Shares represents the number of shares for Diluted EPS computation. |
| 18 | `fnd23_intfvalld1_tait` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income After Taxes |
| 19 | `fnd23_intfvalld1_sabs` | MATRIX | 0.964 | 其他 | 0 | — | — | — | UNTESTED | represents the weighted average common shares outstanding less the dilution of stock options for a given period. These s |
| 20 | `fnd23_intfvalld1_fbbs` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents the bottom-line earnings per share available to common stockholders, excluding the effects of extraordinary i |
| 21 | `fnd23_intfvalld1_fbds` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS excluding extraordinary items represents the bottom-line earnings per share available to common stockholders |
| 22 | `fnd23_intfvalld1_iabs` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, including the effects of extraordinary i |
| 23 | `fnd23_intfvalld1_iads` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Including Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 24 | `fnd23_intfvalld1_xbin` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents net income after taxes, adjusted by minority interest, equity in affiliates and the U.S. GAAP adjustment, bef |
| 25 | `fnd23_intfvalld1_caic` | MATRIX | 0.964 | 其他 | 0 | — | — | — | UNTESTED | Income Available to Common Excl. Extraordinary Items |
| 26 | `fnd23_intfvalld1_cinx` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income available to common stocks incl. extraordinary items represents the bottom-line net income available to common st |
| 27 | `fnd23_intfvalld1_itpv` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Before Taxes represents net income before taxes, excluding the effects of all non-recurring/unusual/on |
| 28 | `fnd23_intfvalld1_inds` | MATRIX | 0.963 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 29 | `fnd23_intfvalld1_sebv` | MATRIX | 0.963 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic normalized EPS represents the bottom-line earnings per share available to common stockholders, excluding the effec |
| 30 | `fnd23_intfvalld1_sedv` | MATRIX | 0.963 | 其他 | 0 | — | — | — | UNTESTED | Diluted Normalized EPS |
| 31 | `fnd23_intfvalld1_caiv` | MATRIX | 0.963 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Available to Common represents the bottom-line net income available to common shareholders, excluding |
| 32 | `fnd23_intfvalld1_taiv` | MATRIX | 0.963 | 其他 | 0 | — | — | — | UNTESTED | Normalized Income After Taxes. |
| 33 | `fnd23_intfvalld1_eltq` | MATRIX | 0.960 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 34 | `fnd23_intfvalld1_letq` | MATRIX | 0.960 | 盈利与财务 | 0 | — | — | — | UNTESTED | sum of total liabilities and total equity. |
| 35 | `fnd23_intfvalld1_tota` | MATRIX | 0.960 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 36 | `fnd23_intfvalld1_lltl` | MATRIX | 0.960 | 盈利与财务 | 0 | — | — | — | UNTESTED | total liabilities. |
| 37 | `fnd23_intfvalld1_1oscq` | MATRIX | 0.960 | 其他 | 0 | — | — | — | UNTESTED | Represents the number of common shares outstanding in a company. When a company has 2 or more different types of common |
| 38 | `fnd23_intfvalld1_octq` | MATRIX | 0.960 | 其他 | 0 | — | — | — | UNTESTED | represents the number of primary common shares equivalent outstanding. |
| 39 | `fnd23_intfvalld1_pbts` | MATRIX | 0.959 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value per Share, Common Equity. |
| 40 | `fnd23_intfvalld1_vbts` | MATRIX | 0.959 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value, Common Equity. |
| 41 | `fnd23_intfvalld1_mtps` | MATRIX | 0.959 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Margin. |
| 42 | `fnd23_annfvalld1_letq` | MATRIX | 0.959 | 盈利与财务 | 0 | — | — | — | UNTESTED | sum of total liabilities and total equity. |
| 43 | `fnd23_annfvalld1_tota` | MATRIX | 0.959 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 44 | `fnd23_annfvalld1_eltq` | MATRIX | 0.959 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 45 | `fnd23_annfvalld1_lltl` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | total liabilities. |
| 46 | `fnd23_intfvalld1_mpns` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin represents Income Available to Common Excluding Extraordinary Items divided by Total Revenue. |
| 47 | `fnd23_annfvalld1_cinx` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Available to Common Stocks Incl. Extraordinary Items represents the bottom-line net income available to common st |
| 48 | `fnd23_annfvalld1_iabs` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, including the effects of extraordinary i |
| 49 | `fnd23_annfvalld1_cnin` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes, adjusted by minority interest, equity in affiliates, the U.S. GAAP adjustment and extraordinary |
| 50 | `fnd23_annfvalld1_sedv` | MATRIX | 0.958 | 其他 | 0 | — | — | — | UNTESTED | Diluted Normalized EPS |
| 51 | `fnd23_annfvalld1_caiv` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Available to Common represents the bottom-line net income available to common shareholders, excluding |
| 52 | `fnd23_annfvalld1_fbbs` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents the bottom-line earnings per share available to common stockholders, excluding the effects of extraordinary i |
| 53 | `fnd23_annfvalld1_sebv` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic normalized EPS represents the bottom-line earnings per share available to common stockholders, excluding the effec |
| 54 | `fnd23_annfvalld1_tait` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income After Taxes |
| 55 | `fnd23_annfvalld1_taiv` | MATRIX | 0.958 | 其他 | 0 | — | — | — | UNTESTED | Normalized Income After Taxes. |
| 56 | `fnd23_annfvalld1_tbie` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents a company's total revenues reduced by total expenses, before taxes on net income and all after-tax adjustment |
| 57 | `fnd23_annfvalld1_iads` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Including Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 58 | `fnd23_annfvalld1_sabs` | MATRIX | 0.957 | 其他 | 0 | — | — | — | UNTESTED | represents the weighted average common shares outstanding less the dilution of stock options for a given period. These s |
| 59 | `fnd23_annfvalld1_swds` | MATRIX | 0.957 | 其他 | 0 | — | — | — | UNTESTED | Diluted Weighted Average Shares represents the number of shares for Diluted EPS computation. |
| 60 | `fnd23_annfvalld1_caic` | MATRIX | 0.957 | 其他 | 0 | — | — | — | UNTESTED | Income Available to Common Excl. Extraordinary Items |
| 61 | `fnd23_annfvalld1_xbin` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents net income after taxes, adjusted by minority interest, equity in affiliates and the U.S. GAAP adjustment, bef |
| 62 | `fnd23_annfvalld1_fbds` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Excluding Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 63 | `fnd23_annfvalld1_itpv` | MATRIX | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Before Taxes represents net income before taxes, excluding the effects of all non-recurring/unusual/on |
| 64 | `fnd23_annfvalld1_1oscq` | MATRIX | 0.956 | 其他 | 0 | — | — | — | UNTESTED | represents the number of common shares outstanding in a company. When a company has two or more different types of commo |
| 65 | `fnd23_annfvalld1_inds` | MATRIX | 0.956 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 66 | `fnd23_annfvalld1_octq` | MATRIX | 0.956 | 其他 | 0 | — | — | — | UNTESTED | represents the number of primary common shares equivalent outstanding. |
| 67 | `fnd23_annfvalld1_vbts` | MATRIX | 0.956 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value, Common Equity. |
| 68 | `fnd23_annfvalld1_pbts` | MATRIX | 0.956 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value per Share, Common Equity. |
| 69 | `fnd23_ofc` | MATRIX | 0.950 | 盈利与财务 | 0 | — | — | — | UNTESTED | cash flow from operating activities. |
| 70 | `fnd23_annfvalld1_mtps` | MATRIX | 0.947 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Margin |
| 71 | `fnd23_annfvalld1_mpns` | MATRIX | 0.947 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin represents Income Available to Common Excluding Extraordinary Items divided by Total Revenue. |
| 72 | `fnd23_annfvalld1_nppa` | MATRIX | 0.946 | 其他 | 0 | — | — | — | UNTESTED | net property, plant and equipment. |
| 73 | `fnd23_annfvalld1_olto` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Includes diverse cash flows that are reported outside of the operating, investing, and financing sections of the cash fl |
| 74 | `fnd23_intfvalld1_xatt` | MATRIX | 0.944 | 其他 | 0 | — | — | — | UNTESTED | Provision for Income Taxes. |
| 75 | `fnd23_annfvalld1_ilti` | MATRIX | 0.944 | 其他 | 0 | — | — | — | UNTESTED | Cash from Investing Activities. |
| 76 | `fnd23_annfvalld1_xatt` | MATRIX | 0.943 | 其他 | 0 | — | — | — | UNTESTED | Provision for Income Taxes. |
| 77 | `fnd23_annfvalld1_fltf` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | cash from financing activities that is the sum of financing cash flow items, cash dividends paid, issuance of stock, net |
| 78 | `fnd23_intfvalld1_ntiv` | MATRIX | 0.943 | 其他 | 0 | — | — | — | UNTESTED | Income Taxes Excluding Impact of Special Items represents total income taxes, adjusted by the tax impact of adding back |
| 79 | `fnd23_annfvalld1_ccns` | MATRIX | 0.942 | 其他 | 0 | — | — | — | UNTESTED | Net Change in Cash |
| 80 | `fnd23_annfvalld1_fcos` | MATRIX | 0.942 | 其他 | 0 | — | — | — | UNTESTED | Changes in Working Capital |
| 81 | `fnd23_annfvalld1_ntiv` | MATRIX | 0.942 | 其他 | 0 | — | — | — | UNTESTED | Income Taxes Excluding Impact of Special Items represents total income taxes, adjusted by the tax impact of adding back |
| 82 | `fnd23_annfvalld1_pedv` | MATRIX | 0.940 | 其他 | 0 | — | — | — | UNTESTED | Depreciation |
| 83 | `deferred_income_noncurrent` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Deferred income classified as non-current. |
| 84 | `extraordinary_items_total_2` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Total extraordinary items reported for the period. |
| 85 | `fnd23_intfvm_cinx` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Income Available to Common Stocks Incl. Extraordinary Items represents the bottom-line net income available to common s |
| 86 | `fnd23_intfvm_inds` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 87 | `fnd23_intfvmfm2_inds` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 88 | `fnd23_intfvmfm_inds` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 89 | `bank_borrowings_total` | MATRIX | 0.936 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total bank borrowings outstanding. |
| 90 | `benefit_expense_total` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Total benefit expense for the period. |
| 91 | `capital_invested_accumulated_cost` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Capital invested at accumulated cost for the interim period. |
| 92 | `dividends_withheld_settled` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends withheld and settled during the period. |
| 93 | `earnings_before_tax` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before tax expenses are deducted. |
| 94 | `extraordinary_net_income_credits` | MATRIX | 0.936 | 风险与质量 | 0 | — | — | — | UNTESTED | [Quarterly] Income Available to Com Incl ExtraOrd |
| 95 | `fnd23_intfvm_caic` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Income Available to Common Excl. Extraordinary Items |
| 96 | `fnd23_intfvm_caiv` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Available to Common represents the bottom-line net income available to common shareholders, excluding |
| 97 | `fnd23_intfvm_cnin` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes, adjusted by minority interest, equity in affiliates, the U.S. GAAP adjustment and extraordinary |
| 98 | `fnd23_intfvm_fbbs` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, excluding the effects of extraordinary |
| 99 | `fnd23_intfvm_fbds` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Excluding Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 100 | `fnd23_intfvm_iabs` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, including the effects of extraordinary i |
| 101 | `fnd23_intfvm_iads` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Including Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 102 | `fnd23_intfvm_sabs` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | represents the weighted average common shares outstanding less the dilution of stock options for a given period. These s |
| 103 | `fnd23_intfvm_sebv` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic Normalized EPS  represents the bottom-line earnings per share available to common stockholders, excluding the eff |
| 104 | `fnd23_intfvm_sedv` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Diluted Normalized EPS |
| 105 | `fnd23_intfvm_swds` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Diluted Weighted Average Shares represents the number of shares for Diluted EPS computation. |
| 106 | `fnd23_intfvm_tait` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Net Income After Taxes |
| 107 | `fnd23_intfvm_taiv` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Normalized Income After Taxes. |
| 108 | `fnd23_intfvm_tbie` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents a company’s total revenues reduced by total expenses, before taxes on net income and all after-tax adjustment |
| 109 | `fnd23_intfvm_xbin` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents net income after taxes, adjusted by minority interest, equity in affiliates and the U.S. GAAP adjustment, bef |
| 110 | `net_income_before_tax` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income before tax for the period. |
| 111 | `net_income_current` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income for the current period. |
| 112 | `net_interest_income_value` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted Net Income |
| 113 | `share_based_awards` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Value of share-based awards granted to employees or management. |
| 114 | `short_term_bank_acceptances_issued` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Short-term bank acceptances issued during the period. |
| 115 | `short_term_debt_amortization_incurred` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Amortization expense incurred on short-term debt. |
| 116 | `short_term_debt_bonds_face_value` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Face value of short-term debt bonds outstanding. |
| 117 | `total_income_after_taxes` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Total income after all taxes have been deducted. |
| 118 | `value_debt_equity_securities` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Value of debt and equity securities held. |
| 119 | `value_investment_assets_total` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value of investment assets held. |
| 120 | `voting_interest_acquired` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Percentage or value of voting interest acquired in subsidiaries or investments. |
| 121 | `bank_assets_investment` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Basic EPS Including Extraordinary Items |
| 122 | `bank_assets_securities` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Basic Weighted Average Shares |
| 123 | `bank_borrowed_funds` | MATRIX | 0.936 | 持仓与资金流 | 0 | — | — | — | UNTESTED | [Quarterly] Basic EPS Excluding Extraordinary Items |
| 124 | `dividend_per_share_declared` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share declared for the period. |
| 125 | `eps` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, including the effects of extraordinary i |
| 126 | `fnd23_intfvm_1spdd` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | common dividends per share for common stock primary issues. |
| 127 | `fnd23_intfvm_dlts` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt represents total interest-bearing debt outstanding. |
| 128 | `fnd23_intfvm_dttl` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 129 | `fnd23_intfvm_itpv` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Before Taxes represents net income before taxes, excluding the effects of all non-recurring/unusual/on |
| 130 | `fnd23_intfvmfm2_dlts` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt represents total interest-bearing debt outstanding. |
| 131 | `fnd23_intfvmfm2_dttl` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 132 | `fnd23_intfvmfm_dttl` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 133 | `income` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes, adjusted by minority interest, equity in affiliates, the U.S. GAAP adjustment and extraordinary |
| 134 | `income_before_tax_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Income Before Taxes |
| 135 | `income_before_tax_3` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Income Before Extra. Items |
| 136 | `income_beforeextra` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents net income after taxes, adjusted by minority interest, equity in affiliates and the U.S. GAAP adjustment, bef |
| 137 | `investments_associates_companies` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Available to Com Excl ExtraOrd |
| 138 | `long_term_debt_total_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total long-term debt outstanding. |
| 139 | `net_income_continuing_ops` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Incl Extra Before Distributions |
| 140 | `pretax_income` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents a company’s total revenues reduced by total expenses, before taxes on net income and all after-tax adjustment |
| 141 | `property_plant_equipment_investment` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Investment in property, plant, and equipment. |
| 142 | `shareholders_equity_value` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted EPS Excluding ExtraOrd Items |
| 143 | `short_term_loans_debt` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term loans and debt reported for the interim period. |
| 144 | `taxes_incurred_after_tax_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Income After Taxes |
| 145 | `total_assets_value_5` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted EPS Including ExtraOrd Items |
| 146 | `valuation_benefit_employee_stock` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Basic Normalized EPS |
| 147 | `valuation_deferred_expense` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted Normalized EPS |
| 148 | `valuation_investment_account_2` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized Inc. Avail to Com. |
| 149 | `valuation_investment_assets_total_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized Income After Taxes |
| 150 | `weighted_shares_outstanding` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted Weighted Average Shares |
| 151 | `assets_total_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets held by the company. |
| 152 | `debt_lt` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 153 | `dividends_payable_short_term` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] DPS - Common Stock Primary Issue |
| 154 | `fnd23_intfvm_eltq` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 155 | `fnd23_intfvm_letq` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | sum of total liabilities and total equity. |
| 156 | `fnd23_intfvm_lltl` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total liabilities. |
| 157 | `fnd23_intfvm_octq` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | represents the number of primary common shares equivalent outstanding. |
| 158 | `fnd23_intfvm_pbts` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value per Share, Common Equity. |
| 159 | `fnd23_intfvm_tota` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 160 | `fnd23_intfvm_vbts` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value, Common Equity. |
| 161 | `fnd23_intfvmfm2_eltq` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 162 | `fnd23_intfvmfm2_tota` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 163 | `fnd23_intfvmfm_eltq` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 164 | `fnd23_intfvmfm_tota` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 165 | `interim_quasi_equity_contracts` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quasi-equity contracts reported for the interim period. |
| 166 | `long_term_liabilities_total_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total long-term liabilities as of the reporting date. |
| 167 | `quarterly_total_liabilities_equity` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total liabilities and equity for the quarter. |
| 168 | `short_term_borrowings_value_2` | MATRIX | 0.936 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Value of short-term borrowings outstanding. |
| 169 | `short_term_loans_drawn_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Debt |
| 170 | `total_debt_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Long Term Debt |
| 171 | `total_equity_liabilities` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total equity and liabilities combined. |
| 172 | `trade_payables_short_term` | MATRIX | 0.936 | 价量与波动 | 0 | — | — | — | UNTESTED | Short-term trade payables owed by the company. |
| 173 | `valuation_post_tax_income` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized Income Before Taxes |
| 174 | `assets` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 175 | `bookvalue_ps` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value per Share, Common Equity. |
| 176 | `equity` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 177 | `fnd23_intfv_octq` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Total Common Shares Outstanding |
| 178 | `fnd23_intfvm_ntiv` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Income Taxes Excluding Impact of Special Items represents total income taxes, adjusted by the tax impact of adding back |
| 179 | `liabilities` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | total liabilities. |
| 180 | `short_term_bank_payables` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Tangible Book Value per Share, Common Eq |
| 181 | `short_term_bonds_value` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Tangible Book Value, Common Equity |
| 182 | `total_assets_7` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Assets |
| 183 | `total_current_obligations_2` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Total Common Shares Outstanding |
| 184 | `total_equity_liabilities_3` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Liabilities & Shareholders' Equity |
| 185 | `total_liabilities_4` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Liabilities |
| 186 | `total_liabilities_equity_3` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Equity |
| 187 | `voting_interest_total` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Total voting interest held by the company in subsidiaries or investments. |
| 188 | `common_shares_outstanding_quarter_2` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Number of common shares outstanding at quarter end. |
| 189 | `fnd23_intfvm_1oscq` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | represents the number of common shares outstanding in a company. When a company has two or more different types of commo |
| 190 | `fnd23_intfvm_lltq` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Total Equity and Equity Non-Controlling Interests. |
| 191 | `fnd23_intfvm_xatt` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Provision for Income Taxes. |
| 192 | `total_liabilities_long_term` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total long-term liabilities outstanding. |
| 193 | `total_tax_expense` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Total tax expense for the period. |
| 194 | `valuation_investment_tangible_net` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Taxes Excluding Impact of Special Items |
| 195 | `common_stock_outstanding_primary` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Shares Outstanding - Common Stock Primary Issue |
| 196 | `income_tax` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Provision for Income Taxes. |
| 197 | `total_liabilities_long_term_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Equity & Minority Interest |
| 198 | `total_tax_expense_3` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Provision for Income Taxes |
| 199 | `fnd23_annfv1a_iabs` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, including the effects of extraordinary i |
| 200 | `fnd23_annfv1a_sebv` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic Normalized EPS  represents the bottom-line earnings per share available to common stockholders, excluding the eff |
| 201 | `fnd23_annfv1a_sedv` | MATRIX | 0.936 | 其他 | 0 | — | — | — | UNTESTED | Diluted Normalized EPS |
| 202 | `fnd23_annfv1a_pbts` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value per Share, Common Equity. |
| 203 | `fnd23_annfv1a_iads` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Including Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 204 | `fnd23_annfvmfm2_octq` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | represents the number of primary common shares equivalent outstanding. |
| 205 | `fnd23_intfvalld1_nppa` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | net property, plant and equipment. |
| 206 | `fnd23_intfvm_mtps` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Margin. |
| 207 | `return_assets` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | return on assets. |
| 208 | `return_equity` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | return on equity. |
| 209 | `special_premium_trust_monetary` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Special premium trust monetary value for the interim period. |
| 210 | `fnd23_annfv1a_fbbs` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, excluding the effects of extraordinary |
| 211 | `fnd23_annfv1a_fbds` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Excluding Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 212 | `fnd23_annfv1a_lltq` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Total Equity and Equity Non-Controlling Interests. |
| 213 | `fnd23_annfvmfm2_eltq` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 214 | `fnd23_annfvmfm2_fcos` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Changes in Working Capital |
| 215 | `fnd23_annfvmfm2_inds` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 216 | `fnd23_annfvmfm_inds` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 217 | `fnd23_intfvm_mpns` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin represents Income Available to Common Excluding Extraordinary Items divided by Total Revenue. |
| 218 | `net_premiums_written` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Net premiums written during the period. |
| 219 | `short_term_prepaid_misc` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Pretax Margin |
| 220 | `fnd23_annfv1a_caiv` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Available to Common represents the bottom-line net income available to common shareholders, excluding |
| 221 | `fnd23_annfv1a_ntiv` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Income Taxes Excluding Impact of Special Items represents total income taxes, adjusted by the tax impact of adding back |
| 222 | `fnd23_annfv1a_sabs` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | represents the weighted average common shares outstanding less the dilution of stock options for a given period. These s |
| 223 | `fnd23_annfv1a_swds` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Diluted Weighted Average Shares represents the number of shares for Diluted EPS computation. |
| 224 | `fnd23_annfv1a_taiv` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Normalized Income After Taxes. |
| 225 | `fnd23_annfvalld1_smcq` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Common Stock represents the value of the most frequently issued class of stock; usually it provides a voting right, but |
| 226 | `fnd23_annfvalld1_smcs` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Total common stock represents the combined value of common stock and limited partner. |
| 227 | `fnd23_annfvmfm2_dttl` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 228 | `fnd23_annfvmfm2_lltl` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | total liabilities. |
| 229 | `fnd23_annfvmfm2_tota` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 230 | `fnd23_annfvmfm_tota` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 231 | `payroll_liabilities_current` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Profit Margin |
| 232 | `fnd23_annfv1a_dlts` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt represents total interest-bearing debt outstanding. |
| 233 | `fnd23_annfv1a_itpv` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Before Taxes represents net income before taxes, excluding the effects of all non-recurring/unusual/on |
| 234 | `fnd23_annfv1a_octq` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | represents the number of primary common shares equivalent outstanding. |
| 235 | `fnd23_annfvmfm2_cnin` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes, adjusted by minority interest, equity in affiliates, the U.S. GAAP adjustment and extraordinary |
| 236 | `fnd23_annfv1a_eltq` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 237 | `fnd23_annfv1a_inds` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 238 | `fnd23_annfvmfm2_olto` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 239 | `fnd23_annfvmfm_olto` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 240 | `fnd23_intfvm_1nstq` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Treasury Shares - Common Stock Primary Issue |
| 241 | `quarterly_treasury_securities` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Value of treasury securities for the quarter. |
| 242 | `fnd23_annfv1a_1oscq` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | represents the number of common shares outstanding in a company. When a company has two or more different types of commo |
| 243 | `fnd23_annfv1a_cinx` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Income Available to Common Stocks Incl. Extraordinary Items represents the bottom-line net income available to common s |
| 244 | `fnd23_annfv1a_dttl` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 245 | `fnd23_annfv1a_fcos` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Changes in Working Capital |
| 246 | `fnd23_annfv1a_letq` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | sum of total liabilities and total equity. |
| 247 | `fnd23_annfv1a_lltl` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | total liabilities. |
| 248 | `fnd23_annfv1a_tota` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 249 | `fnd23_annfv1a_vbts` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value, Common Equity. |
| 250 | `total_shares_number_primary` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Treasury Shares - Common Stock Primary Issue |
| 251 | `fnd23_annfv1a_caic` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Income Available to Common Excl. Extraordinary Items |
| 252 | `fnd23_annfv1a_tait` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Net Income After Taxes |
| 253 | `fnd23_annfv1a_xbin` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents net income after taxes, adjusted by minority interest, equity in affiliates and the U.S. GAAP adjustment, bef |
| 254 | `fnd23_annfv1a_cnin` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes, adjusted by minority interest, equity in affiliates, the U.S. GAAP adjustment and extraordinary |
| 255 | `fnd23_annfv1a_olto` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 256 | `fnd23_annfv1a_tbie` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents a company’s total revenues reduced by total expenses, before taxes on net income and all after-tax adjustment |
| 257 | `fnd23_annfv1a_ccns` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Net Change in Cash |
| 258 | `fnd23_annfv1a_fltf` | MATRIX | 0.934 | 盈利与财务 | 0 | — | — | — | UNTESTED | cash from financing activities that is the sum of financing cash flow items, cash dividends paid, issuance of stock, net |
| 259 | `fnd23_annfv1a_ilti` | MATRIX | 0.934 | 其他 | 0 | — | — | — | UNTESTED | Cash from Investing Activities. |
| 260 | `fnd23_annfv1a_xatt` | MATRIX | 0.934 | 其他 | 0 | — | — | — | UNTESTED | Provision for Income Taxes. |
| 261 | `fnd23_annfvalld1_derq` | MATRIX | 0.934 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents residual earnings from operations, not distributed to shareholders. It may represent accumulated deficit when |
| 262 | `fnd23_annfv1a_1nstq` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | Treasury Shares - Common Stock Primary Issue |
| 263 | `fnd23_annfv1a_mpns` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin represents Income Available to Common Excluding Extraordinary Items divided by Total Revenue. |
| 264 | `fnd23_annfv1a_mtps` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Margin. |
| 265 | `currency_of_converted_financials` | MATRIX | 0.933 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency in which the financial values have been converted for reporting. |
| 266 | `fnd23_annfv1a_derq` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents residual earnings from operations, not distributed to shareholders. It may represent accumulated deficit when |
| 267 | `interim_fiscal_month` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | The fiscal month corresponding to the interim reporting period. |
| 268 | `interim_fiscal_year` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | The fiscal year corresponding to the interim reporting period. |
| 269 | `interim_period_sequence_number_2` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | Sequence number of the interim period within the fiscal year. |
| 270 | `converted_financial_currency` | MATRIX | 0.933 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency to which the financial values have been converted. |
| 271 | `fiscal_period_month` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | Month corresponding to the end of the fiscal period. |
| 272 | `fiscal_period_year` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | Year corresponding to the fiscal period. |
| 273 | `fnd23_annfv1a_smcq` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | Common Stock represents the value of the most frequently issued class of stock; usually it provides a voting right, but |
| 274 | `fnd23_annfv1a_smcs` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | total common stock represets the combined value of common stock and limited partner. |
| 275 | `interim_period_number` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | Sequence number of the interim period within the fiscal year. |
| 276 | `fnd23_annfv1a_fcis` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Investing Cash Flow Items, Total represents all items reported within the investing activities in the cash flow st |
| 277 | `interim_period_type_2` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | Type of interim period (e.g., quarterly, semi-annual) for the financial report. |
| 278 | `fnd23_intfvm_ccns` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Net Change in Cash |
| 279 | `fnd23_intfvm_olto` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 280 | `fnd23_intfvmfm2_olto` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 281 | `fnd23_intfvmfm_olto` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 282 | `other_long_term_obligations_2` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Other long-term obligations not classified elsewhere. |
| 283 | `short_term_non_current_cash` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Short-term cash classified as non-current. |
| 284 | `cashflow_op` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 285 | `commercial_paper_current` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Net Change in Cash |
| 286 | `fnd23_intfvm_fcos` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Changes in Working Capital |
| 287 | `fnd23_intfvm_fltf` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | cash from financing activities that is the sum of financing cash flow items, cash dividends paid, issuance of stock, net |
| 288 | `fnd23_intfvmfm2_fcos` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Changes in Working Capital |
| 289 | `future_tax_liabilities_fund` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Future tax liabilities fund for the interim period. |
| 290 | `other_current_financial_assets` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other financial assets classified as current. |
| 291 | `total_liabilities_other` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Cash from Operating Activities |
| 292 | `cashflow_fin` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | cash from financing activities that is the sum of financing cash flow items, cash dividends paid, issuance of stock, net |
| 293 | `customer_deposits_current` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Changes in Working Capital |
| 294 | `fnd23_annfv1a_bcns` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Net Cash – Beginning Balance represents the beginning balance of cash and cash equivalents, as defined by a company. |
| 295 | `fnd23_annfv1a_ecns` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Net Cash – Ending Balance represents the sum of Net Change in Cash and Net Cash –Beginning Balance. |
| 296 | `fnd23_intfvm_ilti` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Cash from Investing Activities. |
| 297 | `intangible_liabilities_total` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total intangible liabilities outstanding. |
| 298 | `cashflow_invst` | MATRIX | 0.932 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Cash from Investing Activities. |
| 299 | `interest_paid` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash from Investing Activities |
| 300 | `fnd23_intfvm_bcns` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Net Cash – Beginning Balance represents the beginning balance of cash and cash equivalents, as defined by a company. |
| 301 | `fnd23_intfvm_ecns` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Net Cash – Ending Balance represents the sum of Net Change in Cash and Net Cash –Beginning Balance. |
| 302 | `net_cash_equivalents` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | Net cash and cash equivalents held by the company. |
| 303 | `net_current_borrowings` | MATRIX | 0.932 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Net current borrowings outstanding. |
| 304 | `bank_loans_current` | MATRIX | 0.932 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Net Cash - Beginning Balance |
| 305 | `current_portion_long_term_debt` | MATRIX | 0.932 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Cash - Ending Balance |
| 306 | `fnd23_intfvm_fcis` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Investing Cash Flow Items, Total represents all items reported within the investing activities in the cash flow st |
| 307 | `short_term_investment_cashflow` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow from short-term investment activities. |
| 308 | `cash_flow_from_investing_value` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Investing Cash Flow Items, Total |
| 309 | `annual_reporting_currency_code` | MATRIX | 0.930 | 宏观与行业 | 0 | — | — | — | UNTESTED | The currency code in which annual financial values are presented after conversion. |
| 310 | `annual_fiscal_month_number` | MATRIX | 0.930 | 其他 | 0 | — | — | — | UNTESTED | The fiscal month number corresponding to the end of the annual period. |
| 311 | `annual_fiscal_year_number` | MATRIX | 0.930 | 其他 | 0 | — | — | — | UNTESTED | The fiscal year associated with the annual reporting period. |
| 312 | `fnd23_annfv1a_lcos` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Liabilities, Total. |
| 313 | `fnd23_annfvalld1_fcis` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Investing Cash Flow Items, Total represents all items reported within the investing activities in the cash flow st |
| 314 | `fnd23_annfvalld1_ltem` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Full-Time Employees |
| 315 | `fnd23_intfvm_ltls` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Liabilities, Total |
| 316 | `short_term_long_term_liabilities` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term portion of long-term liabilities. |
| 317 | `liabilities_oth` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Liabilities, Total |
| 318 | `long_term_debt_liabilities` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Liabilities, Total |
| 319 | `fnd23_annfv1a_nppa` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | net property, plant and equipment. |
| 320 | `fnd23_annfv1a_pedv` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Deprecation |
| 321 | `fnd23_annfvmfm2_xecs` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | capital expenditures. |
| 322 | `fnd23_intfvm_lcos` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Liabilities, Total. |
| 323 | `other_current_liabilities_3` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other liabilities classified as current. |
| 324 | `current_liabilities_total_4` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Current liabilities, Total |
| 325 | `fnd23_annfv1a_xecs` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | capital expenditures. |
| 326 | `liabilities_cur_oth` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Liabilities, Total. |
| 327 | `fnd23_intfvm_fcoo` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the impact of other operating cash flow items that cannot be classified as an adjustment item to net income, |
| 328 | `other_operating_cash_flows` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other operating cash flows reported in interim financials. |
| 329 | `accounts_payable_notes` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | Notes payable included in accounts payable. |
| 330 | `fnd23_intfvm_nppa` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | net property, plant and equipment. |
| 331 | `operating_cash_flow_2` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Operating Cash Flow |
| 332 | `ppent_net` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | net property, plant and equipment. |
| 333 | `prepaid_pension_assets` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Property/Plant/Equipment,Total - Net |
| 334 | `fnd23_annfv1a_xeci` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | purchase of fixed assets. |
| 335 | `fnd23_annfv1a_ltls` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Liabilities, Total |
| 336 | `fnd23_annfv1a_fcoo` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the impact of other operating cash flow items that cannot be classified as an adjustment item to net income, |
| 337 | `fnd23_annfvalld1_lcos` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Liabilities, Total. |
| 338 | `fnd23_intfvalld1_olto` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 339 | `fnd23_intfvm2_nppv` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Other Property/Plant/Equipment - Net |
| 340 | `equity_total_reported` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total equity as reported in the financial statements. |
| 341 | `fnd23_intfvm_rtes` | MATRIX | 0.924 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective Tax Rate represents Provision for Income Taxes divided by Income Before Tax. |
| 342 | `total_expenses_value` | MATRIX | 0.924 | 宏观与行业 | 0 | — | — | — | UNTESTED | [Quarterly] Effective Tax Rate |
| 343 | `fnd23_intfvalld1_ilti` | MATRIX | 0.923 | 其他 | 0 | — | — | — | UNTESTED | Cash from Investing Activities. |
| 344 | `fnd23_intfvalld1_rtes` | MATRIX | 0.923 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective Tax Rate represents Provision for Income Taxes divided by Income Before Tax. |
| 345 | `fnd23_intfvalld1_ccns` | MATRIX | 0.923 | 其他 | 0 | — | — | — | UNTESTED | Net Change in Cash |
| 346 | `fnd23_annfv1a_1spdd` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | common dividends per share for common stock primary issues. |
| 347 | `fnd23_intfvalld1_fcos` | MATRIX | 0.922 | 其他 | 0 | — | — | — | UNTESTED | Changes in Working Capital |
| 348 | `fnd23_intfvm_alos` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Long-Term Assets, Total. |
| 349 | `short_term_loans_advances` | MATRIX | 0.922 | 其他 | 0 | — | — | — | UNTESTED | Short-term loans and advances provided by the company. |
| 350 | `total_noncurrent_liabilities` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Long Term Assets, Total |
| 351 | `fnd23_tot_revenue` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue. |
| 352 | `fnd23_intfvalld1_fltf` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash from financing activities that is the sum of financing cash flow items, cash dividends paid, issuance of stock, net |
| 353 | `financing_cash_flow_2` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net cash flow from financing activities. |
| 354 | `fnd23_intfvm_fcff` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | other financing cash flow |
| 355 | `fnd23_intfvm_fcfs` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | financing cash flow items represents sum of increase/decrease ind eposits, increase/decrease in federal funds sold or RE |
| 356 | `free_cash_flow_firm` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow available to all capital providers of the firm. |
| 357 | `free_cash_flow` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Financing Cash Flow |
| 358 | `free_cash_flow_value` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Financing Cash Flow Items |
| 359 | `fnd23_annfv1a_alos` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Long-Term Assets, Total. |
| 360 | `deposits_total_value` | MATRIX | 0.917 | 其他 | 0 | — | — | — | UNTESTED | Total value of deposits held by the company. |
| 361 | `fnd23_intfvm_pedv` | MATRIX | 0.917 | 其他 | 0 | — | — | — | UNTESTED | Deprecation |
| 362 | `valuation_depreciation` | MATRIX | 0.917 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Depreciation, Supplemental |
| 363 | `fnd23_annfv1a_ists` | MATRIX | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Total Special Items represents the sum of all non-recurring/unusual/extraordinary/one-off/special gains and losses that |
| 364 | `fnd23_annfv1a_cets` | MATRIX | 0.913 | 其他 | 0 | — | — | — | UNTESTED | Effect of Special Items on Income Taxes. |
| 365 | `fnd23_annfv1a_fcff` | MATRIX | 0.913 | 盈利与财务 | 0 | — | — | — | UNTESTED | other financing cash flow |
| 366 | `fnd23_annfv1a_fcfs` | MATRIX | 0.913 | 盈利与财务 | 0 | — | — | — | UNTESTED | financing cash flow items represents sum of increase/decrease ind eposits, increase/decrease in federal funds sold or RE |
| 367 | `fnd23_annfv1a_rtes` | MATRIX | 0.912 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective Tax Rate represents Provision for Income Taxes divided by Income Before Tax. |
| 368 | `fnd23_annfvalld1_ltls` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Liabilities, Total |
| 369 | `fnd23_intfvm_xecs` | MATRIX | 0.912 | 其他 | 0 | — | — | — | UNTESTED | capital expenditures. |
| 370 | `short_term_contract_expenses` | MATRIX | 0.912 | 其他 | 0 | — | — | — | UNTESTED | Expenses related to short-term contracts. |
| 371 | `capex` | MATRIX | 0.912 | 其他 | 0 | — | — | — | UNTESTED | capital expenditures. |
| 372 | `cash_equivalents_total` | MATRIX | 0.912 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Capital Expenditures |
| 373 | `deferred_charge_goodwill` | MATRIX | 0.912 | 其他 | 0 | — | — | — | UNTESTED | Amount of deferred charges related to goodwill. |
| 374 | `fnd23_intfvm_dgcd` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | gross dividends on common stock. |
| 375 | `deferred_compensation_grants` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Gross Dividends - Common Stock |
| 376 | `fnd23_intfvm_xeci` | MATRIX | 0.911 | 盈利与财务 | 0 | — | — | — | UNTESTED | purchase of fixed assets. |
| 377 | `investment_contracts_total` | MATRIX | 0.911 | 其他 | 0 | — | — | — | UNTESTED | Total value of investment contracts held. |
| 378 | `capital_expenditures` | MATRIX | 0.911 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Capital Expenditures |
| 379 | `fnd23_annfvalld1_xecs` | MATRIX | 0.911 | 其他 | 0 | — | — | — | UNTESTED | capital expenditures. |
| 380 | `fnd23_annfv1a_ctpa` | MATRIX | 0.910 | 其他 | 0 | — | — | — | UNTESTED | gross property, plant & equipment. |
| 381 | `fnd23_intfvalld1_ltls` | MATRIX | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Liabilities, Total |
| 382 | `fnd23_annfv1a_drpf` | MATRIX | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | If debt issuances and reductions are not delineated separately, the total is classified as Issuance (Retirement) of Debt |
| 383 | `fnd23_annfv1a_peda` | MATRIX | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | aggregate of accumulated depreciation for each fixed asset. |
| 384 | `fnd23_intfvm_derq` | MATRIX | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents residual earnings from operations, not distributed to shareholders. It may represent accumulated deficit when |
| 385 | `redeemable_equity_debt` | MATRIX | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | Redeemable equity and debt instruments outstanding. |
| 386 | `redeemable_equity_debt_3` | MATRIX | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Retained Earnings (Accumulated Deficit) |
| 387 | `retained_earnings` | MATRIX | 0.909 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents residual earnings from operations, not distributed to shareholders. It may represent accumulated deficit when |
| 388 | `fnd23_annfv1a_icns` | MATRIX | 0.908 | 其他 | 0 | — | — | — | UNTESTED | non-cash items. |
| 389 | `fnd23_intfvm_dtll` | MATRIX | 0.908 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 390 | `long_term_loans_total_debt` | MATRIX | 0.908 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total long-term loans and debt reported for the interim period. |
| 391 | `long_term_debt_2` | MATRIX | 0.908 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Long Term Debt |
| 392 | `fnd23_annfv1a_dtll` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 393 | `fnd23_annfvalld1_rtes` | MATRIX | 0.907 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective Tax Rate represents Provision for Income Taxes divided by Income Before Tax. |
| 394 | `fnd23_annfvmfm2_teno` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | is the first line of a cash flow statement when a company employs the Indirect Method in the operating cash flow section |
| 395 | `fnd23_annfv1a_teno` | MATRIX | 0.906 | 盈利与财务 | 0 | — | — | — | UNTESTED | is the first line of a cash flow statement when a company employs the Indirect Method in the operating cash flow section |
| 396 | `fnd23_intfvalld1_ipos` | MATRIX | 0.906 | 其他 | 0 | — | — | — | UNTESTED | Operating Income. |
| 397 | `fnd23_annfvalld1_xeci` | MATRIX | 0.906 | 盈利与财务 | 0 | — | — | — | UNTESTED | purchase of fixed assets. |
| 398 | `fnd23_intfvalld1_eote` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | represents total expenses that are operating in nature, including variable costs directly related to the volume of sales |
| 399 | `fnd23_annfvmfm2_peds` | MATRIX | 0.905 | 其他 | 0 | — | — | — | UNTESTED | depreciation. |
| 400 | `fnd23_annfv1a_peds` | MATRIX | 0.904 | 其他 | 0 | — | — | — | UNTESTED | depreciation. |
| 401 | `fnd23_intfvm_etos` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Equity, Total. |
| 402 | `shareholders_other_equity` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other equity items attributable to shareholders for the interim period. |
| 403 | `short_term_other_equity` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Equity, Total |
| 404 | `current_maturities_long_term_debt` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current maturities of long-term debt obligations. |
| 405 | `current_maturities_short_term` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current maturities of short-term debt obligations. |
| 406 | `fnd23_intfvm_smcq` | MATRIX | 0.904 | 其他 | 0 | — | — | — | UNTESTED | Common Stock represents the value of the most frequently issued class of stock; usually it provides a voting right, but |
| 407 | `fnd23_intfvm_smcs` | MATRIX | 0.904 | 其他 | 0 | — | — | — | UNTESTED | total common stock represets the combined value of common stock and limited partner. |
| 408 | `cash_market_securities` | MATRIX | 0.904 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Common Stock, Total |
| 409 | `current_maturities_short_term_debt` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Common Stock |
| 410 | `fnd23_intfvalld1_fcis` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Investing Cash Flow Items, Total represents all items reported within the investing activities in the cash flow st |
| 411 | `fnd23_annfvalld1_dlts` | MATRIX | 0.903 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt represents total interest-bearing debt outstanding. |
| 412 | `fnd23_annfv1a_icno` | MATRIX | 0.903 | 其他 | 0 | — | — | — | UNTESTED | other non cash items. |
| 413 | `fnd23_intfvalld1_rltr` | MATRIX | 0.902 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 414 | `fnd23_annfv1a_dgcd` | MATRIX | 0.901 | 盈利与财务 | 0 | — | — | — | UNTESTED | gross dividends on common stock. |
| 415 | `fnd23_annfv1a_etos` | MATRIX | 0.901 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Equity, Total. |
| 416 | `fnd23_annfvalld1_eote` | MATRIX | 0.899 | 价量与波动 | 0 | — | — | — | UNTESTED | Represents total expenses that are operating in nature, including variable costs directly related to the volume of sales |
| 417 | `fnd23_annfvalld1_ipos` | MATRIX | 0.899 | 其他 | 0 | — | — | — | UNTESTED | Operating Income. |
| 418 | `fnd23_tangible_bvps` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | tangible book value per share. |
| 419 | `fnd23_annfv1a_ttiv` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Income Tax – Total reflects the sum of Domestic Tax - Other, Foreign Tax – Other, Local Tax – Other and Other Tax. |
| 420 | `fnd23_intfvm_cets` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | Effect of Special Items on Income Taxes. |
| 421 | `fnd23_intfvm_ists` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | Total Special Items represents the sum of all non-recurring/unusual/extraordinary/one-off/special gains and losses that |
| 422 | `short_term_securities_investments` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | Short-term securities investments reported for the interim period. |
| 423 | `special_items_effect_on_income_taxes` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | Effect of special items on income taxes for the interim period. |
| 424 | `fnd23_annfv1a_sspf` | MATRIX | 0.897 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance or repurchase of common and preferred stock is not separately delineated, then the total is classi |
| 425 | `short_term_securities_investments_4` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Total Special Items |
| 426 | `special_items_effect_on_tax` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Effect of Special Items on Income Taxes |
| 427 | `fnd23_annfv1a_tnia` | MATRIX | 0.896 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the net value of assets that lack physical existence, reduced by accumulated impairment and intangible amorti |
| 428 | `fnd23_annfv1a_ctcv` | MATRIX | 0.896 | 其他 | 0 | — | — | — | UNTESTED | Current Tax – Total reflects the sum of Current Tax – Domestic, Current Tax – Foreign, Current Tax – Local, Current Tax |
| 429 | `fnd23_annfv1a_bpal` | MATRIX | 0.896 | 其他 | 0 | — | — | — | UNTESTED | Accrued interest expenses, interest payable in commercial banks. |
| 430 | `fnd23_annfvalld1_rltr` | MATRIX | 0.895 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 431 | `fnd23_intfvalld1_dlts` | MATRIX | 0.895 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt represents total interest-bearing debt outstanding. |
| 432 | `fnd23_annfv1a_vnis` | MATRIX | 0.894 | 其他 | 0 | — | — | — | UNTESTED | Long-Term Investments represents the sum of LT Investments – Affiliate Companies and LT Investments – Other. |
| 433 | `fnd23_intfvm_fcii` | MATRIX | 0.894 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash used for discontinued operations classified as Other Investing Cash Flow |
| 434 | `interest_income_cashflow` | MATRIX | 0.894 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow from interest income activities. |
| 435 | `fnd23_annfvalld1_crta` | MATRIX | 0.894 | 其他 | 0 | — | — | — | UNTESTED | total net receivables. |
| 436 | `investing_cash_flow` | MATRIX | 0.894 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Investing Cash Flow |
| 437 | `fnd23_intfvm_vnis` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Long-Term Investments represents the sum of LT Investments – Affiliate Companies and LT Investments – Other. |
| 438 | `short_term_investments_7` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Short-term investments reported in interim financials. |
| 439 | `inventory_value` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Long Term Investments |
| 440 | `fixed_production_assets` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Value of fixed assets used in production. |
| 441 | `fnd23_intfvm_drpf` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | If debt issuances and reductions are not delineated separately, the total is classified as Issuance (Retirement) of Debt |
| 442 | `fnd23_annfv1a_pxtl` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Taxes Payable represents income taxes payable to the government, where such tax liability is already confirmed i |
| 443 | `fnd23_annfvalld1_teno` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | is the first line of a cash flow statement when a company employs the Indirect Method in the operating cash flow section |
| 444 | `preferred_dividends_paid` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Issuance (Retirement) of Debt, Net |
| 445 | `fnd23_net_reveivables` | MATRIX | 0.891 | 其他 | 0 | — | — | — | UNTESTED | net receivables. |
| 446 | `fnd23_intfvm_tnia` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the net value of assets that lack physical existence, reduced by accumulated impairment and intangible amorti |
| 447 | `intangible_assets_total_3` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Intangibles, Net |
| 448 | `fnd23_annfvalld1_bpal` | MATRIX | 0.889 | 其他 | 0 | — | — | — | UNTESTED | Accrued interest expenses, interest payable in commercial banks. |
| 449 | `fnd23_annfv1a_tdbl` | MATRIX | 0.888 | 修正与预期 | 0 | — | — | — | UNTESTED | represents income taxes estimated and expected to be paid within one year or an operating cycle, whichever is longer. |
| 450 | `fnd23_annfv1a_tdbs` | MATRIX | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Deferred Income Tax – Long Term Liability and Deferred Investment Tax Credit |
| 451 | `fnd23_intfvm_rltr` | MATRIX | 0.887 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 452 | `fnd23_intfvmfm2_rltr` | MATRIX | 0.887 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 453 | `fnd23_intfvmfm_rltr` | MATRIX | 0.887 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 454 | `retained_earnings_3` | MATRIX | 0.887 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cumulative net income retained in the business after dividends. |
| 455 | `revenue` | MATRIX | 0.887 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 456 | `total_loans_receivable` | MATRIX | 0.887 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Revenue |
| 457 | `fnd23_intfvm_ipos` | MATRIX | 0.887 | 其他 | 0 | — | — | — | UNTESTED | Operating Income. |
| 458 | `operating_income_2` | MATRIX | 0.887 | 宏观与行业 | 0 | — | — | — | UNTESTED | Income generated from regular business operations. |
| 459 | `equity_to_equityholders` | MATRIX | 0.887 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity attributable to equity holders of the parent. |
| 460 | `fnd23_intfvm_eote` | MATRIX | 0.887 | 价量与波动 | 0 | — | — | — | UNTESTED | represents total expenses that are operating in nature, including variable costs directly related to the volume of sales |
| 461 | `operating_income` | MATRIX | 0.887 | 其他 | 0 | — | — | — | UNTESTED | Operating Income. |
| 462 | `preferred_shares_issued_2` | MATRIX | 0.887 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Operating Income |
| 463 | `operating_expense` | MATRIX | 0.886 | 价量与波动 | 0 | — | — | — | UNTESTED | represents total expenses that are operating in nature, including variable costs directly related to the volume of sales |
| 464 | `total_equity_to_total_equity` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Operating Expenses |
| 465 | `fnd23_intfvm_dtsl` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | notes payable/short term debt. |
| 466 | `long_term_debt` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value of long-term debt obligations outstanding. |
| 467 | `debt_st` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | notes payable/short term debt. |
| 468 | `short_term_debt_2` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Notes Payable/Short Term Debt |
| 469 | `debt` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | total long term plus short term debt. |
| 470 | `fnd23_annfv1a_ipos` | MATRIX | 0.886 | 其他 | 0 | — | — | — | UNTESTED | Operating Income. |
| 471 | `fnd23_annfvmfm2_dtsl` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | notes payable/short term debt. |
| 472 | `fnd23_annfvmfm2_rltr` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 473 | `fnd23_annfvmfm_rltr` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 474 | `fnd23_annfv1a_nscf` | MATRIX | 0.886 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance or repurchase of common stock is not separately delineated, then the total is classified as Common |
| 475 | `fnd23_annfvmfm2_deds` | MATRIX | 0.886 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/Depletion represents the sum of Depreciation and Depletion. |
| 476 | `fnd23_annfv1a_dtsl` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | notes payable/short term debt. |
| 477 | `fnd23_annfv1a_eote` | MATRIX | 0.886 | 价量与波动 | 0 | — | — | — | UNTESTED | represents total expenses that are operating in nature, including variable costs directly related to the volume of sales |
| 478 | `fnd23_annfv1a_rltr` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 479 | `fnd23_annfv1a_deds` | MATRIX | 0.885 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/Depletion represents the sum of Depreciation and Depletion. |
| 480 | `fnd23_intfvalld1_lcos` | MATRIX | 0.885 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Liabilities, Total. |
| 481 | `fnd23_intfvm_icns` | MATRIX | 0.885 | 其他 | 0 | — | — | — | UNTESTED | non-cash items. |
| 482 | `short_term_non_current_investments` | MATRIX | 0.885 | 其他 | 0 | — | — | — | UNTESTED | Short-term investments that are classified as non-current. |
| 483 | `current_income_tax_payable` | MATRIX | 0.885 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Non-Cash Items |
| 484 | `fnd23_intfvalld1_cets` | MATRIX | 0.885 | 其他 | 0 | — | — | — | UNTESTED | Effect of Special Items on Income Taxes. |
| 485 | `fnd23_intfvalld1_ists` | MATRIX | 0.884 | 其他 | 0 | — | — | — | UNTESTED | Total Special Items represents the sum of all non-recurring/unusual/extraordinary/one-off/special gains and losses that |
| 486 | `fnd23_intfvalld1_vnis` | MATRIX | 0.884 | 其他 | 0 | — | — | — | UNTESTED | Long-Term Investments represents the sum of LT Investments - Affiliate Companies and LT Investments - Other. |
| 487 | `fnd23_ebit` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT - Earnings before interest & tax |
| 488 | `fnd23_ebitda` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA - Interest before interest, taxes, depreciation & amortization |
| 489 | `fnd23_annfv1a_ptcs` | MATRIX | 0.883 | 持仓与资金流 | 0 | — | — | — | UNTESTED | cash taxes paid represents taxes paid in cash, net of tax refunds received, as reported by the company. |
| 490 | `fnd23_annfvalld1_jads` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dilution Adjustment represents the adding back to reported net income the interest expense of debentures when assumed co |
| 491 | `fnd23_net_debt` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | net debt |
| 492 | `fnd23_annfvalld1_deds` | MATRIX | 0.882 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/Depletion represents the sum of Depreciation and Depletion. |
| 493 | `fnd23_annfv1a_crta` | MATRIX | 0.881 | 其他 | 0 | — | — | — | UNTESTED | total net receivables. |
| 494 | `fnd23_annfvalld1_icns` | MATRIX | 0.881 | 其他 | 0 | — | — | — | UNTESTED | non-cash items. |
| 495 | `fnd23_ve` | MATRIX | 0.881 | 其他 | 0 | — | — | — | UNTESTED | enterprise value |
| 496 | `fnd23_intfvalld1_fcoo` | MATRIX | 0.880 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the impact of other operating cash flow items that cannot be classified as an adjustment item to net income, |
| 497 | `fnd23_annfvalld1_fcoo` | MATRIX | 0.880 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the impact of other operating cash flow items that cannot be classified as an adjustment item to net income, |
| 498 | `fnd23_annfv1a_xeal` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents operational expenses accrued, but not yet paid. As current liabilities, such expenses are expected to be paid |
| 499 | `fnd23_annfvalld1_ecns` | MATRIX | 0.879 | 其他 | 0 | — | — | — | UNTESTED | Net Cash - Ending Balance represents the sum of Net Change in Cash and Net Cash - Beginning Balance. |
| 500 | `fnd23_intfvalld1_pedv` | MATRIX | 0.879 | 其他 | 0 | — | — | — | UNTESTED | Depreciation |
| 501 | `fnd23_annfvalld1_bcns` | MATRIX | 0.879 | 其他 | 0 | — | — | — | UNTESTED | Net Cash - Beginning Balance represents the beginning balance of cash and cash equivalents, as defined by a company. |
| 502 | `fnd23_annfvalld1_icno` | MATRIX | 0.879 | 其他 | 0 | — | — | — | UNTESTED | Other non-cash items. |
| 503 | `fnd23_intfvm_nins` | MATRIX | 0.878 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense (Income), Net- Non-Operating, Total |
| 504 | `short_term_notes_issued_net` | MATRIX | 0.878 | 其他 | 0 | — | — | — | UNTESTED | Net amount of short-term notes issued during the period. |
| 505 | `interest_payable_current` | MATRIX | 0.878 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Income (Exp), Net- Non-Operating, Total |
| 506 | `fnd23_annfvmfm2_imav` | MATRIX | 0.877 | 其他 | 0 | — | — | — | UNTESTED | Amortization. |
| 507 | `fnd23_intfvm_tdbl` | MATRIX | 0.877 | 修正与预期 | 0 | — | — | — | UNTESTED | represents income taxes estimated and expected to be paid within one year or an operating cycle, whichever is longer. |
| 508 | `fnd23_intfvm_tdbs` | MATRIX | 0.877 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Deferred Income Tax – Long Term Liability and Deferred Investment Tax Credit |
| 509 | `long_term_bond_debt` | MATRIX | 0.877 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term bond debt reported in interim financials. |
| 510 | `short_term_bond_debt` | MATRIX | 0.877 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term bond debt reported in interim financials. |
| 511 | `bank_debt` | MATRIX | 0.877 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] NOT_SELECTED Deferred Income Tax - LT Liability |
| 512 | `bank_deposits_total` | MATRIX | 0.877 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Deferred Income Tax |
| 513 | `fnd23_annfv1a_imav` | MATRIX | 0.877 | 其他 | 0 | — | — | — | UNTESTED | Amortization. |
| 514 | `fnd23_annfv1a_fcii` | MATRIX | 0.877 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash used for discontinued operations classified as Other Investing Cash Flow |
| 515 | `fnd23_intfvm_icno` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | other non cash items. |
| 516 | `other_non_current_investments` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | Other non-current investments held by the company. |
| 517 | `fnd23_annfv1a_nins` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense (Income), Net- Non-Operating, Total |
| 518 | `noncontrolling_interests` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other Non-Cash Items |
| 519 | `fnd23_intfvm_sspf` | MATRIX | 0.876 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance or repurchase of common and preferred stock is not separately delineated, then the total is classi |
| 520 | `fully_paid_share_capital` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | Total value of fully paid share capital issued by the company. |
| 521 | `proceeds_from_preferred_stock_sale` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Issuance (Retirement) of Stock, Net |
| 522 | `current_tax_payable` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | Current tax payable as of the reporting date. |
| 523 | `fnd23_annfv1a_xeiv` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Supplemental. |
| 524 | `fnd23_annfvalld1_agss` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expenses, Total. |
| 525 | `fnd23_intfvm_ptcs` | MATRIX | 0.876 | 持仓与资金流 | 0 | — | — | — | UNTESTED | cash taxes paid represents taxes paid in cash, net of tax refunds received, as reported by the company. |
| 526 | `capitalized_technology_property` | MATRIX | 0.876 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash Taxes Paid |
| 527 | `fnd23_annfv1a_agss` | MATRIX | 0.875 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expenses, Total. |
| 528 | `fnd23_annfvalld1_sspf` | MATRIX | 0.875 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance, or repurchase of common and preferred stock is not separately delineated, then the total is class |
| 529 | `fnd23_curr_assets` | MATRIX | 0.875 | 盈利与财务 | 0 | — | — | — | UNTESTED | current assets |
| 530 | `fnd23_curr_liabilities` | MATRIX | 0.874 | 盈利与财务 | 0 | — | — | — | UNTESTED | current liabilities |
| 531 | `fnd23_lt_debt` | MATRIX | 0.874 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt. |
| 532 | `fnd23_intfvm_crta` | MATRIX | 0.873 | 其他 | 0 | — | — | — | UNTESTED | total net receivables. |
| 533 | `fnd23_intfvm_niis` | MATRIX | 0.873 | 其他 | 0 | — | — | — | UNTESTED | Interest/Investment Income, Non-Operating |
| 534 | `interest_income_total_2` | MATRIX | 0.873 | 其他 | 0 | — | — | — | UNTESTED | Total interest income earned by the company. |
| 535 | `insurance_income_value` | MATRIX | 0.873 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest/Invest Income - Non-Operating |
| 536 | `receivable` | MATRIX | 0.873 | 其他 | 0 | — | — | — | UNTESTED | total net receivables. |
| 537 | `trade_receivables_current` | MATRIX | 0.873 | 价量与波动 | 0 | — | — | — | UNTESTED | [Quarterly] Total Receivables, Net |
| 538 | `fnd23_annfvalld1_xeiv` | MATRIX | 0.873 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Supplemental. |
| 539 | `fnd23_annfvalld1_peds` | MATRIX | 0.872 | 其他 | 0 | — | — | — | UNTESTED | depreciation. |
| 540 | `fnd23_intfvm_teno` | MATRIX | 0.872 | 盈利与财务 | 0 | — | — | — | UNTESTED | is the first line of a cash flow statement when a company employs the Indirect Method in the operating cash flow section |
| 541 | `fnd23_intfvmfm2_teno` | MATRIX | 0.872 | 盈利与财务 | 0 | — | — | — | UNTESTED | is the first line of a cash flow statement when a company employs the Indirect Method in the operating cash flow section |
| 542 | `other_net_income_total` | MATRIX | 0.872 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total other net income for the period. |
| 543 | `net_equity_total` | MATRIX | 0.872 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Income/Starting Line |
| 544 | `fnd23_annfv1a_atda` | MATRIX | 0.872 | 风险与质量 | 0 | — | — | — | UNTESTED | deferred income taxes - long term. These are credits being applied to income taxes that will be paid in future years. |
| 545 | `fnd23_annfvalld1_cema` | MATRIX | 0.871 | 其他 | 0 | — | — | — | UNTESTED | represents the acquisition cost of machinery and other equipment (including delivery equipment, office equipment, machin |
| 546 | `fnd23_annfv1a_croa` | MATRIX | 0.869 | 其他 | 0 | — | — | — | UNTESTED | other receivables. |
| 547 | `fnd23_intfvalld1_crta` | MATRIX | 0.869 | 其他 | 0 | — | — | — | UNTESTED | total net receivables. |
| 548 | `fnd23_annfvalld1_nins` | MATRIX | 0.869 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense (Income), Net- Non-Operating, Total |
| 549 | `fnd23_annfv1a_niis` | MATRIX | 0.869 | 其他 | 0 | — | — | — | UNTESTED | Interest/Investment Income, Non-Operating |
| 550 | `fnd23_intfvalld1_vers` | MATRIX | 0.867 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue represents revenues from the sale of merchandise goods, manufactured products and services, and the distribution |
| 551 | `accounts_current_assets_equity` | MATRIX | 0.867 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current assets related to equity accounts. |
| 552 | `fnd23_intfvm_eaca` | MATRIX | 0.867 | 其他 | 0 | — | — | — | UNTESTED | cash & equivalents. |
| 553 | `financing_cashflow_net` | MATRIX | 0.866 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net cash flow from financing activities. |
| 554 | `fnd23_annfv1a_eaca` | MATRIX | 0.866 | 其他 | 0 | — | — | — | UNTESTED | cash & equivalents. |
| 555 | `fnd23_intfvm_nscf` | MATRIX | 0.866 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance or repurchase of common stock is not separately delineated, then the total is classified as Common |
| 556 | `cash_and_short_term_investments` | MATRIX | 0.866 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Common Stock, Net |
| 557 | `fnd23_intfvalld1_tibs` | MATRIX | 0.866 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest and Taxes. |
| 558 | `fnd23_intfvalld1_adbs` | MATRIX | 0.865 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest, Taxes, Depreciation and Amortization |
| 559 | `fnd23_intfvalld1_bcns` | MATRIX | 0.865 | 其他 | 0 | — | — | — | UNTESTED | Net cash - beginning balance represents the beginning balance of cash and cash equivalents, as defined by a company. |
| 560 | `fnd23_intfvalld1_ecns` | MATRIX | 0.865 | 其他 | 0 | — | — | — | UNTESTED | Net Cash - Ending Balance represents the sum of Net Change in Cash and Net Cash - Beginning Balance. |
| 561 | `fnd23_intfvm_vnin` | MATRIX | 0.865 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents income or losses, other than interest, from investment securities. Such income may include dividend income, g |
| 562 | `net_investments` | MATRIX | 0.865 | 其他 | 0 | — | — | — | UNTESTED | Net investments reported in interim financials. |
| 563 | `fnd23_annfvalld1_ctpa` | MATRIX | 0.865 | 其他 | 0 | — | — | — | UNTESTED | gross property, plant & equipment. |
| 564 | `net_investment_income_2` | MATRIX | 0.865 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Investment Income - Non-Operating |
| 565 | `fnd23_annfvalld1_dttl` | MATRIX | 0.864 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents interest-bearing debt with maturities beyond 1 year. Long-term debt may consist of long-term bank borrowings, |
| 566 | `fnd23_annfvalld1_ttiv` | MATRIX | 0.864 | 其他 | 0 | — | — | — | UNTESTED | Income Tax - Total reflects the sum of Domestic Tax - Other, Foreign Tax - Other, Local Tax - Other and Other Tax. |
| 567 | `fnd23_annfv1a_ndlf` | MATRIX | 0.864 | 盈利与财务 | 0 | — | — | — | UNTESTED | If long-term debt issuances and reductions are not delineated separately, the total is classified as Long Term Debt, Net |
| 568 | `fnd23_intfvalld1_fcff` | MATRIX | 0.864 | 盈利与财务 | 0 | — | — | — | UNTESTED | other financing cash flow |
| 569 | `fnd23_intfvalld1_fcfs` | MATRIX | 0.864 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financing cash flow items represent the sum of increase/decrease in deposits, increase/decrease in federal funds sold or |
| 570 | `fnd23_intfvalld1_ppos` | MATRIX | 0.864 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin. |
| 571 | `fnd23_annfvalld1_tnia` | MATRIX | 0.863 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the net value of assets that lack physical existence, reduced by accumulated impairment and intangible amorti |
| 572 | `fnd23_intfvm_jads` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dilution Adjustment represents the adding back to reported net income the interest expense of debentures when assumed co |
| 573 | `shareholder_dividends_adjustments` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjustments made to dividends attributable to shareholders. |
| 574 | `total_liabilities_value_3` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Dilution Adjustment |
| 575 | `fnd23_annfvmfm2_dlcl` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Port. of LT Debt/Capital Leases. |
| 576 | `fnd23_intfvalld1_derq` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents residual earnings from operations, not distributed to shareholders. It may represent accumulated deficit when |
| 577 | `fnd23_annfv1a_dlcl` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Port. of LT Debt/Capital Leases. |
| 578 | `fnd23_intfvalld1_dtns` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Debt Including Preferred Stock & Minority Interest. |
| 579 | `fnd23_annfvalld1_dtns` | MATRIX | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Debt Including Preferred Stock & Minority Interest. |
| 580 | `fnd23_annfvalld1_tibs` | MATRIX | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest and Taxes. |
| 581 | `fnd23_annfvalld1_adbs` | MATRIX | 0.861 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest, Taxes, Depreciation and Amortization |
| 582 | `fnd23_annfvalld1_niis` | MATRIX | 0.861 | 其他 | 0 | — | — | — | UNTESTED | Interest/Investment Income, Non-Operating |
| 583 | `fnd23_capex` | MATRIX | 0.861 | 其他 | 0 | — | — | — | UNTESTED | capital expenditure |
| 584 | `fnd23_annfvalld1_vers` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue represents revenues from the sale of merchandise goods, manufactured products and services, and the distribution |
| 585 | `fnd23_annfvalld1_peda` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | aggregate of accumulated depreciation for each fixed asset. |
| 586 | `fnd23_annfvalld1_ctcv` | MATRIX | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Current Tax - Total reflects the sum of Current Tax - Domestic, Current Tax - Foreign, Current Tax - Local, Current Tax |
| 587 | `fnd23_intfvm_eoos` | MATRIX | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Other Operating Expenses, Total. |
| 588 | `short_term_other_operating_expenses` | MATRIX | 0.860 | 其他 | 0 | — | — | — | UNTESTED | Short-term other operating expenses reported in interim financials. |
| 589 | `other_operating_expenses_current` | MATRIX | 0.859 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other Operating Expenses, Total |
| 590 | `fnd23_annfvalld1_eaca` | MATRIX | 0.859 | 其他 | 0 | — | — | — | UNTESTED | cash & equivalents. |
| 591 | `fnd23_annfvalld1_iscs` | MATRIX | 0.859 | 其他 | 0 | — | — | — | UNTESTED | cash and short-term investments. |
| 592 | `accumulated_depreciation_total_assets` | MATRIX | 0.859 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total accumulated depreciation on assets reported in interim financials. |
| 593 | `fnd23_intfvm_atda` | MATRIX | 0.859 | 风险与质量 | 0 | — | — | — | UNTESTED | deferred income taxes - long term. These are credits being applied to income taxes that will be paid in future years. |
| 594 | `accumulated_depreciation_total_assets_matrix` | MATRIX | 0.859 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Deferred Income Tax - Long Term Asset |
| 595 | `fnd23_intfvalld1_fcii` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash used for discontinued operations classified as Other Investing Cash Flow |
| 596 | `fnd23_intfvalld1_smcq` | MATRIX | 0.858 | 其他 | 0 | — | — | — | UNTESTED | Common Stock represents the value of the most frequently issued class of stock; usually it provides a voting right, but |
| 597 | `fnd23_intfvalld1_smcs` | MATRIX | 0.858 | 其他 | 0 | — | — | — | UNTESTED | Total common stock represents the combined value of common stock and limited partner. |
| 598 | `fnd23_intfvalld1_eaca` | MATRIX | 0.858 | 其他 | 0 | — | — | — | UNTESTED | cash & equivalents. |
| 599 | `fnd23_annfvalld1_ppos` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin. |
| 600 | `fnd23_annfvalld1_ndlf` | MATRIX | 0.857 | 盈利与财务 | 0 | — | — | — | UNTESTED | If long-term debt issuances and reductions are not delineated separately, the total is classified as Long Term Debt, Net |
| 601 | `fnd23_annfvalld1_nscf` | MATRIX | 0.857 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance or repurchase of common stock is not separately delineated, then the total is classified as Common |
| 602 | `fnd23_annfv1a_vnin` | MATRIX | 0.857 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents income or losses, other than interest, from investment securities. Such income may include dividend income, g |
| 603 | `fnd23_intfvalld1_acta` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current assets. Sum of cash and short-term investments, total receivables (net), total inventory, prepaid expenses |
| 604 | `fnd23_intfvalld1_iucs` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Current Assets less Inventory represents Total Current Assets minus Total Inventory. |
| 605 | `fnd23_intfvalld1_kcqs` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio represents Total Current Assets less Inventory divided by Total Current Liabilities. |
| 606 | `fnd23_intfvalld1_rucs` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Ratio represents Total Current Assets divided by Total Current Liabilities |
| 607 | `fnd23_annfv1a_aiav` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accumulated Intangible Amortization represents accumulated amortization against intangible fixed assets. |
| 608 | `fnd23_annfvalld1_alos` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Long-Term Assets, Total. |
| 609 | `fnd23_intfvalld1_lctl` | MATRIX | 0.855 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 610 | `fnd23_annfvalld1_kcqs` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio represents Total Current Assets less Inventory divided by Total Current Liabilities. |
| 611 | `fnd23_annfvalld1_rucs` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Ratio represents Total Current Assets divided by Total Current Liabilities. |
| 612 | `fnd23_annfvalld1_iucs` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Current Assets less Inventory represents Total Current Assets minus Total Inventory. |
| 613 | `fnd23_annfvalld1_acta` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current assets. Sum of cash and short-term investments, total receivables (net), total inventory, prepaid expenses |
| 614 | `fnd23_annfvalld1_lctl` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 615 | `fnd23_intfvalld1_dttl` | MATRIX | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents interest-bearing debt with maturities beyond 1 year. Long-term debt may consist of long-term bank borrowings, |
| 616 | `fnd23_intfvalld1_iscs` | MATRIX | 0.853 | 其他 | 0 | — | — | — | UNTESTED | cash and short-term investments. |
| 617 | `fnd23_intfvalld1_dtll` | MATRIX | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents interest-bearing debt with maturities beyond 1 year. Long-term debt may consist of long-term bank borrowings, |
| 618 | `fnd23_annfvalld1_fcfs` | MATRIX | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | Financing cash flow items represent sum of increase/decrease in deposits, increase/decrease in federal funds sold or REP |
| 619 | `fnd23_annfv1a_tmaa` | MATRIX | 0.853 | 其他 | 0 | — | — | — | UNTESTED | accumulated intangible amortization. |
| 620 | `fnd23_annfvalld1_fcff` | MATRIX | 0.852 | 盈利与财务 | 0 | — | — | — | UNTESTED | other financing cash flow |
| 621 | `fnd23_annfvalld1_ctdv` | MATRIX | 0.852 | 其他 | 0 | — | — | — | UNTESTED | Deferred Tax - Total |
| 622 | `fnd23_annfv1a_gnia` | MATRIX | 0.852 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the gross purchase value of assets that lack physical existence, before being reduced by accumulated impairm |
| 623 | `fnd23_annfvalld1_iwga` | MATRIX | 0.852 | 其他 | 0 | — | — | — | UNTESTED | net goodwill. |
| 624 | `fnd23_annfv1a_neis` | MATRIX | 0.852 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Net Non-Operating represents Interest Expense, Non-Operating, reduced by Interest Capitalized, Non-Ope |
| 625 | `fnd23_annfv1a_nein` | MATRIX | 0.852 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest expense on debt of non-financial service companies, including insurance companies. |
| 626 | `fnd23_annfvalld1_croa` | MATRIX | 0.850 | 其他 | 0 | — | — | — | UNTESTED | other receivables. |
| 627 | `fnd23_annfvalld1_rcaa` | MATRIX | 0.850 | 其他 | 0 | — | — | — | UNTESTED | accounts receivable value. |
| 628 | `bank_interest_total` | MATRIX | 0.849 | 其他 | 0 | — | — | — | UNTESTED | Total interest expense related to banking operations. |
| 629 | `fnd23_intfvm_tibs` | MATRIX | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest and Taxes. |
| 630 | `fnd23_intfvmfm2_tibs` | MATRIX | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest and Taxes. |
| 631 | `bank_interest_total_2` | MATRIX | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized EBIT |
| 632 | `ebit` | MATRIX | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest and Taxes. |
| 633 | `fnd23_annfv1a_afsi` | MATRIX | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sale of assets to be leased out under operating lease contracts. |
| 634 | `fnd23_annfv1a_iwga` | MATRIX | 0.849 | 其他 | 0 | — | — | — | UNTESTED | net goodwill. |
| 635 | `fnd23_intfvm_dtns` | MATRIX | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Debt Including Preferred Stock & Minority Interest. |
| 636 | `shareholders_net_total_dividends` | MATRIX | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total net dividends to shareholders for the interim period. |
| 637 | `dividends_payable_current` | MATRIX | 0.849 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Debt Including Preferred Stock & Minority Interest |
| 638 | `fnd23_intfvm_vers` | MATRIX | 0.848 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue represents revenues from the sale of merchandise goods, manufactured products and services, and the distributio |
| 639 | `sales_revenue_total` | MATRIX | 0.848 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total revenue from sales for the period. |
| 640 | `fnd23_annfv1a_dtns` | MATRIX | 0.848 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Debt Including Preferred Stock & Minority Interest. |
| 641 | `short_term_receivables` | MATRIX | 0.848 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Revenue |
| 642 | `fnd23_annfv1a_tibs` | MATRIX | 0.848 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest and Taxes. |
| 643 | `fnd23_intfvalld1_prgs` | MATRIX | 0.848 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Profit represents a measure of a company's operating performance. Gross Profit states the profits earned from a co |
| 644 | `fnd23_annfv1a_iscs` | MATRIX | 0.848 | 其他 | 0 | — | — | — | UNTESTED | cash and short-term investments. |
| 645 | `fnd23_annfvmfm2_iscs` | MATRIX | 0.848 | 其他 | 0 | — | — | — | UNTESTED | cash and short-term investments. |
| 646 | `fnd23_annfvalld1_dtll` | MATRIX | 0.847 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents interest-bearing debt with maturities beyond 1 year. Long-term debt may consist of long-term bank borrowings, |
| 647 | `fnd23_intfvm_ppos` | MATRIX | 0.847 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin. |
| 648 | `operating_profit_3` | MATRIX | 0.847 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profit from core business operations before interest and taxes. |
| 649 | `operating_margin` | MATRIX | 0.847 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin. |
| 650 | `prepaid_expenses_current` | MATRIX | 0.847 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Operating Margin |
| 651 | `customer_securities_investment` | MATRIX | 0.847 | 其他 | 0 | — | — | — | UNTESTED | Customer securities held for investment purposes. |
| 652 | `fnd23_annfv1a_vers` | MATRIX | 0.847 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue represents revenues from the sale of merchandise goods, manufactured products and services, and the distributio |
| 653 | `fnd23_intfvm_iscs` | MATRIX | 0.847 | 其他 | 0 | — | — | — | UNTESTED | cash and short-term investments. |
| 654 | `capital_stock_issued` | MATRIX | 0.847 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash and Short Term Investments |
| 655 | `cash_st` | MATRIX | 0.847 | 其他 | 0 | — | — | — | UNTESTED | cash and short-term investments. |
| 656 | `finance_lease_debt_total` | MATRIX | 0.846 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total finance lease debt outstanding. |
| 657 | `fnd23_intfvm_ndlf` | MATRIX | 0.846 | 盈利与财务 | 0 | — | — | — | UNTESTED | If long-term debt issuances and reductions are not delineated separately, the total is classified as Long Term Debt, Net |
| 658 | `long_term_debt_net` | MATRIX | 0.846 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Long Term Debt, Net |
| 659 | `fnd23_annfv1a_eoos` | MATRIX | 0.846 | 其他 | 0 | — | — | — | UNTESTED | Other Operating Expenses, Total. |
| 660 | `fnd23_annfv1a_ppos` | MATRIX | 0.846 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin. |
| 661 | `fnd23_intfvalld1_stnr` | MATRIX | 0.846 | 其他 | 0 | — | — | — | UNTESTED | net sales. |
| 662 | `fnd23_intfvalld1_ppgs` | MATRIX | 0.846 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross margin represents gross profit divided by revenue. Gross margin is not available if either gross profit or revenue |
| 663 | `fnd23_intfvalld1_nins` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense (Income), Net - Non-Operating, Total |
| 664 | `fnd23_intfvm_pxtl` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Taxes Payable represents income taxes payable to the government, where such tax liability is already confirmed i |
| 665 | `long_term_tax_payable_4` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | Long-term tax payable reported in interim financials. |
| 666 | `fnd23_annfvalld1_tdbl` | MATRIX | 0.845 | 修正与预期 | 0 | — | — | — | UNTESTED | Represents income taxes estimated and expected to be paid within 1 year or an operating cycle, whichever is longer. |
| 667 | `fnd23_annfvalld1_tdbs` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Deferred Income Tax - Long Term Liability and Deferred Investment Tax Credit |
| 668 | `income_tax_payable` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Taxes Payable represents income taxes payable to the government, where such tax liability is already confirmed i |
| 669 | `tax_payable` | MATRIX | 0.845 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Taxes Payable |
| 670 | `fnd23_intfvalld1_alos` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Long-Term Assets, Total |
| 671 | `fnd23_annfvalld1_ptcs` | MATRIX | 0.845 | 持仓与资金流 | 0 | — | — | — | UNTESTED | cash taxes paid represents taxes paid in cash, net of tax refunds received, as reported by the company. |
| 672 | `fnd23_annfv1a_adbs` | MATRIX | 0.844 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest, Taxes, Depreciation and Amortization |
| 673 | `bank_deposits_assets` | MATRIX | 0.844 | 盈利与财务 | 0 | — | — | — | UNTESTED | Assets held as deposits in banks. |
| 674 | `fnd23_intfvm_adbs` | MATRIX | 0.844 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest, Taxes, Depreciation and Amortization |
| 675 | `bank_deposits_assets_3` | MATRIX | 0.844 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized EBITDA |
| 676 | `ebitda` | MATRIX | 0.844 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest, Taxes, Depreciation and Amortization |
| 677 | `fnd23_annfvalld1_fcii` | MATRIX | 0.844 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash used for discontinued operations classified as Other Investing Cash Flow |
| 678 | `fnd23_annfvalld1_rocs` | MATRIX | 0.843 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue represents total costs that can be directly attributed to the goods and services produced/purchased and |
| 679 | `fnd23_annfvalld1_drpf` | MATRIX | 0.843 | 盈利与财务 | 0 | — | — | — | UNTESTED | If debt issuances and reductions are not delineated separately, the total is classified as Issuance (Retirement) of Debt |
| 680 | `fnd23_annfv1a_pics` | MATRIX | 0.843 | 其他 | 0 | — | — | — | UNTESTED | cash interest paid represents interest paid in cash during the period Cash Interest. |
| 681 | `fnd23_annfvalld1_roce` | MATRIX | 0.843 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cost of revenue including labor costs reported within cost of goods sold & that are not clearly labeled as cost of goods |
| 682 | `fnd23_intfvm_bpal` | MATRIX | 0.843 | 其他 | 0 | — | — | — | UNTESTED | Accrued interest expenses, interest payable in commercial banks. |
| 683 | `loans_advances_to_public_banks` | MATRIX | 0.843 | 宏观与行业 | 0 | — | — | — | UNTESTED | Loans and advances made to public sector banks. |
| 684 | `accounts_payable` | MATRIX | 0.843 | 其他 | 0 | — | — | — | UNTESTED | Accrued interest expenses, interest payable in commercial banks. |
| 685 | `fnd23_annfvalld1_prgs` | MATRIX | 0.843 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Profit represents a measure of a company's operating performance. Gross Profit states the profits earned from a co |
| 686 | `fnd23_annfv1a_eius` | MATRIX | 0.842 | 其他 | 0 | — | — | — | UNTESTED | Unusual Expense (Income). |
| 687 | `fnd23_annfvalld1_afsi` | MATRIX | 0.842 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sale of assets to be leased out under operating lease contracts. |
| 688 | `fnd23_annfv1a_cema` | MATRIX | 0.842 | 其他 | 0 | — | — | — | UNTESTED | represents the acquisition cost of machinery and other equipment (including delivery equipment, office equipment, machin |
| 689 | `fnd23_annfv1a_pdcf` | MATRIX | 0.841 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Cash Dividends Paid. |
| 690 | `fnd23_annfvalld1_ppgs` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin represents Gross Profit divided by Revenue. Gross Margin is not available if either Gross Profit or Revenue |
| 691 | `fnd23_annfv1a_rcaa` | MATRIX | 0.840 | 其他 | 0 | — | — | — | UNTESTED | accounts receivable value. |
| 692 | `fnd23_annfvalld1_cipq` | MATRIX | 0.840 | 价量与波动 | 0 | — | — | — | UNTESTED | represents capital contributed by shareholders in excess of par value of common stock in return for shares issued to the |
| 693 | `fnd23_intfvm_agss` | MATRIX | 0.840 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expenses, Total. |
| 694 | `short_term_securities_gain_adjustment` | MATRIX | 0.840 | 其他 | 0 | — | — | — | UNTESTED | Adjustment for gains on short-term securities. |
| 695 | `selling_general_admin_expense_4` | MATRIX | 0.840 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Selling/General/Admin. Expenses, Total |
| 696 | `accounts_total_current_assets` | MATRIX | 0.839 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current assets as reported in accounts. |
| 697 | `fnd23_annfvmfm2_acta` | MATRIX | 0.839 | 盈利与财务 | 0 | — | — | — | UNTESTED | total current assets. Sum of cash and short term investments, total receivables (net), total inventory, prepaid expenses |
| 698 | `fnd23_annfvmfm2_lctl` | MATRIX | 0.839 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 699 | `fnd23_intfvm_acta` | MATRIX | 0.839 | 盈利与财务 | 0 | — | — | — | UNTESTED | total current assets. Sum of cash and short term investments, total receivables (net), total inventory, prepaid expenses |
| 700 | `assets_curr` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | total current assets. Sum of cash and short term investments, total receivables (net), total inventory, prepaid expenses |
| 701 | `fnd23_intfvalld1_xecs` | MATRIX | 0.838 | 其他 | 0 | — | — | — | UNTESTED | capital expenditures. |
| 702 | `fnd23_intfvm_lctl` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 703 | `fnd23_intfvmfm2_lctl` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 704 | `fnd23_intfvmfm_lctl` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 705 | `interim_long_term_contract_liabilities` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term contract liabilities reported for the interim period. |
| 706 | `total_current_assets_7` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Current Assets |
| 707 | `liabilities_curr` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 708 | `total_current_liabilities_4` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Current Liabilities |
| 709 | `fnd23_annfv1a_acta` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | total current assets. Sum of cash and short term investments, total receivables (net), total inventory, prepaid expenses |
| 710 | `fnd23_annfv1a_lctl` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 711 | `currency_in_circulation` | MATRIX | 0.838 | 宏观与行业 | 0 | — | — | — | UNTESTED | Total currency in circulation for the company. |
| 712 | `fnd23_intfvm_iucs` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Current Assets less Inventory represents Total Current Assets minus Total Inventory. |
| 713 | `fnd23_intfvm_kcqs` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio represents Total Current Assets less Inventory divided by Total Current Liabilities. |
| 714 | `fnd23_intfvm_rucs` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Ratio represents Total Current Assets divided by Total Current Liabilities. |
| 715 | `quick_assets_total` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value of quick assets, typically cash and equivalents. |
| 716 | `short_term_currency_instruments` | MATRIX | 0.838 | 宏观与行业 | 0 | — | — | — | UNTESTED | Short-term currency instruments held by the company. |
| 717 | `financial_reporting_currency_2` | MATRIX | 0.838 | 宏观与行业 | 0 | — | — | — | UNTESTED | [Quarterly] Current Ratio |
| 718 | `fnd23_intfv_rucs` | MATRIX | 0.838 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Current Ratio |
| 719 | `quick_ratio` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio represents Total Current Assets less Inventory divided by Total Current Liabilities. |
| 720 | `short_term_quick_assets` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Quick Ratio |
| 721 | `fnd23_annfv1a_eiuo` | MATRIX | 0.837 | 盈利与财务 | 0 | — | — | — | UNTESTED | is applicable only if Net Income/Starting Line [ONET] is income after gains/losses from unusual activities. Because the |
| 722 | `depreciation_expense_total` | MATRIX | 0.837 | 其他 | 0 | — | — | — | UNTESTED | Total depreciation expense for the period. |
| 723 | `fnd23_annfv1a_kcqs` | MATRIX | 0.837 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio represents Total Current Assets less Inventory divided by Total Current Liabilities. |
| 724 | `fnd23_intfvm_peds` | MATRIX | 0.837 | 其他 | 0 | — | — | — | UNTESTED | depreciation. |
| 725 | `depre_amort` | MATRIX | 0.837 | 其他 | 0 | — | — | — | UNTESTED | depreciation. |
| 726 | `fnd23_annfv1a_iucs` | MATRIX | 0.837 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Current Assets less Inventory represents Total Current Assets minus Total Inventory. |
| 727 | `fnd23_annfv1a_rucs` | MATRIX | 0.837 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Ratio represents Total Current Assets divided by Total Current Liabilities. |
| 728 | `total_revenue_value_2` | MATRIX | 0.837 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Depreciation |
| 729 | `fnd23_cash_n_equivalents` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | cash equivalents |
| 730 | `fnd23_annfv1a_cipq` | MATRIX | 0.836 | 价量与波动 | 0 | — | — | — | UNTESTED | represents capital contributed by shareholders in excess of par value of common stock in return for shares issued to the |
| 731 | `fnd23_annfvalld1_stnr` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | net sales. |
| 732 | `fnd23_intfvm_stnr` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | net sales. |
| 733 | `rental_expense` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | Total rental expense incurred during the period. |
| 734 | `net_sales_total` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Net Sales |
| 735 | `sales` | MATRIX | 0.836 | 其他 | 0 | — | — | — | UNTESTED | net sales. |
| 736 | `fnd23_intfvalld1_xeci` | MATRIX | 0.835 | 盈利与财务 | 0 | — | — | — | UNTESTED | purchase of fixed assets. |
| 737 | `fnd23_annfvalld1_vnis` | MATRIX | 0.835 | 其他 | 0 | — | — | — | UNTESTED | Long-Term Investments represents the sum of LT Investments - Affiliate Companies and LT Investments - Other. |
| 738 | `fnd23_intfvm_xeiv` | MATRIX | 0.835 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Supplemental. |
| 739 | `value_investment_expenditures` | MATRIX | 0.835 | 其他 | 0 | — | — | — | UNTESTED | Total value of investment expenditures made during the period. |
| 740 | `fnd23_annfv1a_tnon` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | represents any non-operating income or expense item that a company reports before income taxes |
| 741 | `fnd23_annfv1a_tnos` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | other net income. |
| 742 | `valuation_investment_expense` | MATRIX | 0.834 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Expense, Supplemental |
| 743 | `fnd23_intfvm_dlcl` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Port. of LT Debt/Capital Leases. |
| 744 | `long_term_current_liabilities_4` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term current liabilities reported in interim financials. |
| 745 | `current_liabilities` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Current Portion of LT Debt/Capital Leases |
| 746 | `debt_lt_curr` | MATRIX | 0.834 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Port. of LT Debt/Capital Leases. |
| 747 | `fnd23_annfv1a_stnr` | MATRIX | 0.833 | 其他 | 0 | — | — | — | UNTESTED | net sales. |
| 748 | `current_ratio` | MATRIX | 0.832 | 盈利与财务 | 0 | — | — | — | UNTESTED | total current assets/total current liabilities. |
| 749 | `finance_costs_deferred_payment` | MATRIX | 0.832 | 其他 | 0 | — | — | — | UNTESTED | Finance costs related to deferred payment reported in interim financials. |
| 750 | `fnd23_intfvm_pdcf` | MATRIX | 0.832 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Cash Dividends Paid. |
| 751 | `cash_dividends_paid` | MATRIX | 0.832 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Cash Dividends Paid |
| 752 | `fnd23_annfvalld1_pdcf` | MATRIX | 0.830 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Cash Dividends Paid. |
| 753 | `fnd23_intfvalld1_eoos` | MATRIX | 0.830 | 其他 | 0 | — | — | — | UNTESTED | Other Operating Expenses, Total. |
| 754 | `fnd23_annfv1a_agse` | MATRIX | 0.829 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expense. |
| 755 | `accrued_assets_total` | MATRIX | 0.828 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total accrued assets as of the reporting date. |
| 756 | `fnd23_intfvm_rcaa` | MATRIX | 0.828 | 其他 | 0 | — | — | — | UNTESTED | accounts receivable value. |
| 757 | `fnd23_annfvalld1_neis` | MATRIX | 0.828 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Net Non-Operating represents Interest Expense, Non-Operating, reduced by Interest Capitalized, Non-Ope |
| 758 | `fnd23_annfvalld1_nein` | MATRIX | 0.827 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest expense on debt of non-financial service companies, including insurance companies. |
| 759 | `fnd23_intfvm_pics` | MATRIX | 0.827 | 其他 | 0 | — | — | — | UNTESTED | cash interest paid represents interest paid in cash during the period Cash Interest. |
| 760 | `share_capital_in_preference` | MATRIX | 0.827 | 其他 | 0 | — | — | — | UNTESTED | Share capital in preference reported for the interim period. |
| 761 | `capital_investment_property` | MATRIX | 0.827 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash Interest Paid |
| 762 | `fnd23_intfvm_afsi` | MATRIX | 0.827 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sale of assets to be leased out under operating lease contracts. |
| 763 | `intangible_software_assets` | MATRIX | 0.827 | 盈利与财务 | 0 | — | — | — | UNTESTED | Intangible software assets reported in interim financials. |
| 764 | `sale_of_fixed_assets` | MATRIX | 0.827 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Sale of Fixed Assets |
| 765 | `fnd23_annfvmfm2_rocs` | MATRIX | 0.827 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue represents total costs that can be directly attributed to the goods and services produced/purchased and |
| 766 | `fnd23_annfv1a_roce` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue including labor coasts reported within cost of goods sold & that are not clearly labeled as cost of good |
| 767 | `fnd23_annfv1a_rocs` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue represents total costs that can be directly attributed to the goods and services produced/purchased and |
| 768 | `fnd23_intfvalld1_ptcs` | MATRIX | 0.826 | 持仓与资金流 | 0 | — | — | — | UNTESTED | cash taxes paid represents taxes paid in cash, net of tax refunds received, as reported by the company. |
| 769 | `fnd23_annfvalld1_pxtl` | MATRIX | 0.826 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Taxes Payable represents income taxes payable to the government, where such tax liability is already confirmed in |
| 770 | `fnd23_annfv1a_cpdf` | MATRIX | 0.825 | 盈利与财务 | 0 | — | — | — | UNTESTED | common cash dividends paid |
| 771 | `fnd23_intfvm_eius` | MATRIX | 0.825 | 其他 | 0 | — | — | — | UNTESTED | Unusual Expense (Income). |
| 772 | `unrealized_investment_expense` | MATRIX | 0.825 | 其他 | 0 | — | — | — | UNTESTED | Unrealized expense related to investments. |
| 773 | `short_term_unearned_income` | MATRIX | 0.825 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Unusual Expense (Income) |
| 774 | `fnd23_intfvalld1_icns` | MATRIX | 0.822 | 其他 | 0 | — | — | — | UNTESTED | non-cash items. |
| 775 | `fnd23_acc_payable` | MATRIX | 0.821 | 其他 | 0 | — | — | — | UNTESTED | accounts payable |
| 776 | `fnd23_annfv1a_lcol` | MATRIX | 0.821 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current liabilities. |
| 777 | `fnd23_intfvm_prgs` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Profit represents a measure of a company’s operating performance. Gross Profit states the profits earned from a co |
| 778 | `fnd23_intfvm_tnos` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | other net income. |
| 779 | `goodwill_and_intangibles` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value of goodwill and intangible assets on the balance sheet. |
| 780 | `shares_outstanding_total` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | Total number of shares currently issued and outstanding for the company. |
| 781 | `gross_receipts_value` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Gross Profit |
| 782 | `notes_payable_current` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other, Net |
| 783 | `fnd23_annfv1a_prgs` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Profit represents a measure of a company’s operating performance. Gross Profit states the profits earned from a co |
| 784 | `fnd23_intfvm_ppgs` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin  represents Gross Profit  divided by Revenue. Gross Margin is not available if either Gross Profit or Reven |
| 785 | `gross_profit_total` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total gross profit for the period. |
| 786 | `fnd23_intfvm_tnon` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | represents any non-operating income or expense item that a company reports before income taxes |
| 787 | `gross_profit_value_2` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Gross Margin |
| 788 | `non_operating_income_total` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | Total non-operating income for the period. |
| 789 | `non_operating_income_total_3` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other Non-Operating Income (Expense) |
| 790 | `fnd23_annfvalld1_eoos` | MATRIX | 0.820 | 其他 | 0 | — | — | — | UNTESTED | Other Operating Expenses, Total. |
| 791 | `fnd23_annfv1a_ppgs` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin  represents Gross Profit  divided by Revenue. Gross Margin is not available if either Gross Profit or Reven |
| 792 | `equity_corrections` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | Adjustments or corrections made to equity. |
| 793 | `fnd23_intfvm_roce` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue including labor coasts reported within cost of goods sold & that are not clearly labeled as cost of good |
| 794 | `fnd23_intfvm_rocs` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue represents total costs that can be directly attributed to the goods and services produced/purchased and |
| 795 | `other_current_receivables` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other receivables classified as current assets. |
| 796 | `cogs` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue represents total costs that can be directly attributed to the goods and services produced/purchased and |
| 797 | `cost_of_revenue` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue including labor coasts reported within cost of goods sold & that are not clearly labeled as cost of good |
| 798 | `cost_of_revenue_3` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Cost of Revenue |
| 799 | `cost_of_revenue_total` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Cost of Revenue, Total |
| 800 | `fnd23_intfvm_lcol` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current liabilities. |
| 801 | `long_term_other_current_liabilities_2` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term other current liabilities reported in interim financials. |
| 802 | `other_current_liabilities_4` | MATRIX | 0.819 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Current Liabilities |
| 803 | `fnd23_intfvalld1_rocs` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue represents total costs that can be directly attributed to the goods and services produced/purchased and |
| 804 | `fnd23_intfvalld1_roce` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cost of revenue including labor costs reported within cost of goods sold & that are not clearly labeled as cost of goods |
| 805 | `fnd23_intfvm_deds` | MATRIX | 0.818 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/Depletion represents the sum of Depreciation and Depletion. |
| 806 | `short_term_debt_ending_balance` | MATRIX | 0.818 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ending balance of short-term debt for the period. |
| 807 | `net_income_value_4` | MATRIX | 0.818 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Depreciation/Depletion |
| 808 | `finance_deferred_payment_costs` | MATRIX | 0.816 | 其他 | 0 | — | — | — | UNTESTED | Finance deferred payment costs reported in interim financials. |
| 809 | `fnd23_intfvm_cpdf` | MATRIX | 0.816 | 盈利与财务 | 0 | — | — | — | UNTESTED | common cash dividends paid |
| 810 | `depreciation_and_amortization_expense_3` | MATRIX | 0.816 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Cash Dividends Paid - Common |
| 811 | `fnd23_annfvalld1_xeal` | MATRIX | 0.815 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents operational expenses accrued, but not yet paid. As current liabilities, such expenses are expected to be paid |
| 812 | `fnd23_intfvalld1_nimc` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity fo |
| 813 | `fnd23_intfvalld1_tnia` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the net value of assets that lack physical existence, reduced by accumulated impairment and intangible amorti |
| 814 | `fnd23_intfvm_ltll` | MATRIX | 0.814 | 其他 | 0 | — | — | — | UNTESTED | Long-term obligations from right-of-use contracts related to operating leases. |
| 815 | `long_term_liabilities_total_4` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total long-term liabilities reported in interim financials. |
| 816 | `long_term_liabilities_3` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Long Term Liabilities |
| 817 | `fnd23_intfvalld1_nimv` | MATRIX | 0.813 | 盈利与财务 | 0 | — | — | — | UNTESTED | Minority interest, supplemental represents the share of earnings/losses in subsidiaries that belongs to shareholders oth |
| 818 | `fnd23_intfvalld1_teno` | MATRIX | 0.812 | 盈利与财务 | 0 | — | — | — | UNTESTED | is the first line of a cash flow statement when a company employs the Indirect Method in the operating cash flow section |
| 819 | `fnd23_annfv1a_jads` | MATRIX | 0.811 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dilution Adjustment represents the adding back to reported net income the interest expense of debentures when assumed co |
| 820 | `extraordinary_other_operating_expenses` | MATRIX | 0.810 | 其他 | 0 | — | — | — | UNTESTED | Extraordinary other operating expenses reported in interim financials. |
| 821 | `fnd23_intfvm_eooe` | MATRIX | 0.810 | 其他 | 0 | — | — | — | UNTESTED | Depreciation of investment properties disclosed outside of the cost of goods sold, for companies reporting in the IFRS o |
| 822 | `other_operating_expenses_2` | MATRIX | 0.810 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other Operating Expense |
| 823 | `fnd23_annfvalld1_cpdf` | MATRIX | 0.810 | 盈利与财务 | 0 | — | — | — | UNTESTED | common cash dividends paid |
| 824 | `current_minority_interest` | MATRIX | 0.809 | 其他 | 0 | — | — | — | UNTESTED | Current minority interest reported in interim financials. |
| 825 | `fnd23_intfvm_nimc` | MATRIX | 0.809 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the share of earnings/losses in subsidiaries that belongs to shareholders other than the parent company when |
| 826 | `minority_interest_2` | MATRIX | 0.809 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Minority Interest |
| 827 | `fnd23_annfv1a_ltll` | MATRIX | 0.809 | 其他 | 0 | — | — | — | UNTESTED | Long-term obligations from right-of-use contracts related to operating leases. |
| 828 | `fnd23_annfv1a_itla` | MATRIX | 0.809 | 其他 | 0 | — | — | — | UNTESTED | represents long-term investments with maturities of one year or longer. |
| 829 | `fnd23_intfvm_nimv` | MATRIX | 0.809 | 盈利与财务 | 0 | — | — | — | UNTESTED | Minority Interest, Supplemental represents the share of earnings/losses in subsidiaries that belongs to shareholders ot |
| 830 | `valuation_minority_interest` | MATRIX | 0.809 | 其他 | 0 | — | — | — | UNTESTED | Minority interest amount used for valuation in interim financials. |
| 831 | `valuation_miscellaneous_items` | MATRIX | 0.809 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Minority Interest, Supplemental |
| 832 | `allowance_for_loans_total_interim` | MATRIX | 0.808 | 其他 | 0 | — | — | — | UNTESTED | Total allowance for loan losses reported in interim financials. |
| 833 | `fnd23_intfvm_itla` | MATRIX | 0.808 | 其他 | 0 | — | — | — | UNTESTED | represents long-term investments with maturities of one year or longer. |
| 834 | `loans_to_insiders_2` | MATRIX | 0.808 | 持仓与资金流 | 0 | — | — | — | UNTESTED | [Quarterly] Long-Term Investments - Other |
| 835 | `fnd23_annfv1a_b6los` | MATRIX | 0.808 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Year 6 and Beyond represents Total Operating Leases, Supplemental  less St |
| 836 | `fnd23_annfv1a_lotv` | MATRIX | 0.808 | 其他 | 0 | — | — | — | UNTESTED | Total Operating Leases, Supplemental reflects the sum of Operating Leases Maturing within 1 through 10 Years, Operating |
| 837 | `fnd23_intfvalld1_drpf` | MATRIX | 0.807 | 盈利与财务 | 0 | — | — | — | UNTESTED | If debt issuances and reductions are not delineated separately, the total is classified as Issuance (Retirement) of Debt |
| 838 | `fnd23_annfv1a_1los` | MATRIX | 0.807 | 其他 | 0 | — | — | — | UNTESTED | Operating Lease Payments Due in Year 1 |
| 839 | `fnd23_annfv1a_qabi` | MATRIX | 0.807 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash outflow for acquiring new businesses. Reporting the cash flow for acquiring new businesses is not consis |
| 840 | `fnd23_annfvalld1_dlcl` | MATRIX | 0.807 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Port. of LT Debt/Capital Leases. |
| 841 | `fnd23_intfvm_etoq` | MATRIX | 0.805 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents any residual value of shareholders’ equity that belongs to shareholders. |
| 842 | `quasi_other_total_equity` | MATRIX | 0.805 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quasi other total equity reported in interim financials. |
| 843 | `other_equity_total` | MATRIX | 0.805 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Equity |
| 844 | `fnd23_annfv1a_2los` | MATRIX | 0.802 | 其他 | 0 | — | — | — | UNTESTED | Operating Lease Payments Due in Year 2 |
| 845 | `fnd23_annfv1a_32los` | MATRIX | 0.802 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Years 2 and 3 represents the summation of Standardized Operating Lease Paym |
| 846 | `fnd23_intfvm_eefs` | MATRIX | 0.801 | 宏观与行业 | 0 | — | — | — | UNTESTED | Foreign Exchange Effects represents the increase/decrease in cash and cash equivalents due to changes in exchange rates. |
| 847 | `short_term_fees_expense` | MATRIX | 0.801 | 其他 | 0 | — | — | — | UNTESTED | Short-term fees expense reported in interim financials. |
| 848 | `fee_income_value` | MATRIX | 0.801 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Foreign Exchange Effects |
| 849 | `fnd23_annfv1a_acos` | MATRIX | 0.799 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Assets, Total. |
| 850 | `fnd23_intfvalld1_niis` | MATRIX | 0.799 | 其他 | 0 | — | — | — | UNTESTED | Interest/Investment Income, Non-Operating |
| 851 | `fnd23_annfvalld1_imav` | MATRIX | 0.799 | 其他 | 0 | — | — | — | UNTESTED | Amortization. |
| 852 | `fnd23_intfvalld1_bpal` | MATRIX | 0.799 | 其他 | 0 | — | — | — | UNTESTED | Accrued interest expenses, interest payable in commercial banks. |
| 853 | `fnd23_annfvalld1_eius` | MATRIX | 0.798 | 其他 | 0 | — | — | — | UNTESTED | Unusual Expense (Income). |
| 854 | `fnd23_intfvm_cipq` | MATRIX | 0.797 | 价量与波动 | 0 | — | — | — | UNTESTED | represents capital contributed by shareholders in excess of par value of common stock in return for shares issued to the |
| 855 | `preferred_investment_capital` | MATRIX | 0.797 | 其他 | 0 | — | — | — | UNTESTED | Preferred investment capital outstanding. |
| 856 | `preferred_investment_capital_2` | MATRIX | 0.797 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Additional Paid-In Capital |
| 857 | `fnd23_annfv1a_3los` | MATRIX | 0.796 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Year 3. |
| 858 | `fnd23_annfvalld1_eiuo` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | is applicable only if Net Income/Starting Line [ONET] is income after gains/losses from unusual activities. Because the |
| 859 | `fnd23_annfvalld1_itla` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Represents long-term investments with maturities of 1 year or longer. |
| 860 | `fnd23_annfvalld1_aiav` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accumulated Intangible Amortization represents accumulated amortization against intangible fixed assets. |
| 861 | `fnd23_annfv1a_niin` | MATRIX | 0.793 | 宏观与行业 | 0 | — | — | — | UNTESTED | represents non-operating interest income, which is generated from non-operating investment securities such as certificat |
| 862 | `fnd23_annfvalld1_lcol` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current liabilities. |
| 863 | `fnd23_annfv1a_4los` | MATRIX | 0.793 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Year 4. |
| 864 | `fnd23_annfv1a_54los` | MATRIX | 0.793 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Years 4 and 5 represents the summation of Standardized Operating Lease Paym |
| 865 | `fnd23_annfv1a_eefs` | MATRIX | 0.792 | 宏观与行业 | 0 | — | — | — | UNTESTED | Foreign Exchange Effects represents the increase/decrease in cash and cash equivalents due to changes in exchange rates. |
| 866 | `fnd23_intfvm_acos` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Assets, Total. |
| 867 | `short_term_other_current_assets_2` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term other current assets reported in interim financials. |
| 868 | `accrued_expenses_current` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Current Assets, Total |
| 869 | `assets_curr_oth` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Assets, Total. |
| 870 | `fnd23_intfvalld1_icno` | MATRIX | 0.790 | 其他 | 0 | — | — | — | UNTESTED | Other non-cash items. |
| 871 | `fnd23_annfv1a_rpds` | MATRIX | 0.790 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/amortization represents sum of depreciation, amortization of intangibles and amortization of acquisition co |
| 872 | `fnd23_annfvalld1_1spdd` | MATRIX | 0.790 | 盈利与财务 | 0 | — | — | — | UNTESTED | common dividends per share for common stock primary issues. |
| 873 | `fnd23_annfv1a_5los` | MATRIX | 0.788 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Year 5. |
| 874 | `fnd23_intfvalld1_agss` | MATRIX | 0.788 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expenses, Total. |
| 875 | `fnd23_intfvalld1_sspf` | MATRIX | 0.787 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance, or repurchase of common and preferred stock is not separately delineated, then the total is class |
| 876 | `fnd23_annfv1a_rdlf` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash outflow on the repayment of long-term debt in a company. Long-term debt obligations may be repaid upon m |
| 877 | `fnd23_annfv1a_pxrv` | MATRIX | 0.786 | 其他 | 0 | — | — | — | UNTESTED | Rental Expense, Supplemental represents the total value of rental expenses paid for offices, factories, machinery and eq |
| 878 | `fnd23_intfvalld1_etos` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Equity, Total |
| 879 | `fnd23_intfvm_croa` | MATRIX | 0.785 | 其他 | 0 | — | — | — | UNTESTED | other receivables. |
| 880 | `other_receivables_current` | MATRIX | 0.785 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Receivables - Other |
| 881 | `fnd23_annfvalld1_niml` | MATRIX | 0.785 | 其他 | 0 | — | — | — | UNTESTED | Represents accumulated interest for minority shareholders in subsidiaries that are less than 100% owned by the reporting |
| 882 | `fnd23_intfvm_neis` | MATRIX | 0.784 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Net Non-Operating represents Interest Expense, Non-Operating, reduced by Interest Capitalized, Non-Ope |
| 883 | `interest_expense_net` | MATRIX | 0.784 | 其他 | 0 | — | — | — | UNTESTED | Net interest expense for the period. |
| 884 | `interest_expense_value` | MATRIX | 0.784 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Expense, Net Non-Operating |
| 885 | `fnd23_intfvm_nein` | MATRIX | 0.783 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest expense on debt of non-financial service companies, including insurance companies. |
| 886 | `net_interest_earned` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | Net interest earned during the period. |
| 887 | `interest_expense_net_3` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Expense - Non-Operating |
| 888 | `fnd23_efcf` | MATRIX | 0.783 | 盈利与财务 | 0 | — | — | — | UNTESTED | free cash flow to equity. |
| 889 | `fnd23_annfvalld1_ists` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | Total Special Items represents the sum of all non-recurring/unusual/extraordinary/one-off/special gains and losses that |
| 890 | `fnd23_intfvm_niml` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | represents accumulated interest for minority shareholders in subsidiaries that are less than 100 percent owned by the re |
| 891 | `fnd23_intfvmfm2_niml` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | represents accumulated interest for minority shareholders in subsidiaries that are less than 100 percent owned by the re |
| 892 | `long_term_minority_interest_3` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | Long-term minority interest reported in interim financials. |
| 893 | `minority_interest_3` | MATRIX | 0.782 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Minority Interest |
| 894 | `fnd23_intfvm_qabi` | MATRIX | 0.781 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash outflow for acquiring new businesses. Reporting the cash flow for acquiring new businesses is not consis |
| 895 | `acquisition_of_businesses` | MATRIX | 0.781 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Acquisition of Business |
| 896 | `fnd23_annfv1a_yppa` | MATRIX | 0.781 | 其他 | 0 | — | — | — | UNTESTED | prepaid expenses. |
| 897 | `fnd23_intfvalld1_niml` | MATRIX | 0.780 | 其他 | 0 | — | — | — | UNTESTED | Represents accumulated interest for minority shareholders in subsidiaries that are less than 100% owned by the reporting |
| 898 | `fnd23_intfvalld1_peds` | MATRIX | 0.780 | 其他 | 0 | — | — | — | UNTESTED | depreciation. |
| 899 | `fnd23_intfvalld1_eius` | MATRIX | 0.779 | 其他 | 0 | — | — | — | UNTESTED | Unusual Expense (Income). |
| 900 | `fnd23_annfvalld1_nimv` | MATRIX | 0.779 | 盈利与财务 | 0 | — | — | — | UNTESTED | Minority Interest, Supplemental represents the share of earnings/losses in subsidiaries that belongs to shareholders oth |
| 901 | `fnd23_annfvalld1_nimc` | MATRIX | 0.778 | 盈利与财务 | 0 | — | — | — | UNTESTED | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity fo |
| 902 | `fnd23_annfv1a_niml` | MATRIX | 0.778 | 其他 | 0 | — | — | — | UNTESTED | represents accumulated interest for minority shareholders in subsidiaries that are less than 100 percent owned by the re |
| 903 | `fnd23_annfv1a_cisf` | MATRIX | 0.778 | 持仓与资金流 | 0 | — | — | — | UNTESTED | represents cash inflow from the issuance of common stock. It also includes cash inflow from the sale of treasury shares. |
| 904 | `fnd23_intfvm_aiev` | MATRIX | 0.776 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity in Affiliates, Supplemental represents the total share of earnings/losses, net of taxes, that the company is ent |
| 905 | `valuation_equity_investments_amount` | MATRIX | 0.776 | 盈利与财务 | 0 | — | — | — | UNTESTED | Amount of equity investments reported for valuation purposes in interim financials. |
| 906 | `valuation_equity_intangible_assets` | MATRIX | 0.776 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Equity in Affiliates, Supplemental |
| 907 | `fnd23_annfvalld1_niin` | MATRIX | 0.776 | 宏观与行业 | 0 | — | — | — | UNTESTED | represents non-operating interest income, which is generated from non-operating investment securities such as certificat |
| 908 | `fnd23_intfvm_imav` | MATRIX | 0.776 | 其他 | 0 | — | — | — | UNTESTED | Amortization. |
| 909 | `valuation_allowance_misc_items` | MATRIX | 0.776 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Amortization of Intangibles, Supplemental |
| 910 | `fnd23_annfvalld1_vnin` | MATRIX | 0.775 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents income or losses, other than interest, from investment securities. Such income may include dividend income, g |
| 911 | `fnd23_annfv1a_iqea` | MATRIX | 0.774 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents long-term investment in securities (loans, bonds, and equity) of affiliate companies, where the affiliation |
| 912 | `fnd23_annfvalld1_lotv` | MATRIX | 0.774 | 其他 | 0 | — | — | — | UNTESTED | Total Operating Leases, Supplemental reflects the sum of Operating Leases Maturing within 1 through 10 Years, Operating |
| 913 | `fnd23_annfvalld1_b6los` | MATRIX | 0.774 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Year 6 and Beyond represents total operating leases, supplemental less stan |
| 914 | `fnd23_annfvalld1_1los` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Operating Lease Payments Due in Year 1 |
| 915 | `fnd23_annfv1a_dltv` | MATRIX | 0.773 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Long Term Debt, Supplemental reflects the sum of Long Term Debt Maturing within 1 through 10 Years and Long Term |
| 916 | `fnd23_intfvalld1_itla` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Represents long-term investments with maturities of 1 year or longer. |
| 917 | `fnd23_annfvalld1_gnia` | MATRIX | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents the gross purchase value of assets that lack physical existence, before being reduced by accumulated impairme |
| 918 | `fnd23_annfv1a_eooe` | MATRIX | 0.772 | 其他 | 0 | — | — | — | UNTESTED | Depreciation of investment properties disclosed outside of the cost of goods sold, for companies reporting in the IFRS o |
| 919 | `fnd23_annfv1a_1dls` | MATRIX | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long Term Debt Maturing within 1 Year |
| 920 | `fnd23_annfv1a_acoa` | MATRIX | 0.771 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current assets. |
| 921 | `fnd23_annfv1a_nimv` | MATRIX | 0.771 | 盈利与财务 | 0 | — | — | — | UNTESTED | Minority Interest, Supplemental represents the share of earnings/losses in subsidiaries that belongs to shareholders ot |
| 922 | `fnd23_intfvalld1_tdbs` | MATRIX | 0.770 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Deferred Income Tax - Long Term Liability and Deferred Investment Tax Credit |
| 923 | `fnd23_intfvalld1_tdbl` | MATRIX | 0.770 | 修正与预期 | 0 | — | — | — | UNTESTED | Represents income taxes estimated and expected to be paid within 1 year or an operating cycle, whichever is longer. |
| 924 | `fnd23_annfvalld1_tmaa` | MATRIX | 0.770 | 其他 | 0 | — | — | — | UNTESTED | accumulated intangible amortization. |
| 925 | `fnd23_intfvm_agse` | MATRIX | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expense. |
| 926 | `fnd23_annfv1a_etoq` | MATRIX | 0.770 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents any residual value of shareholders’ equity that belongs to shareholders. |
| 927 | `sga_expense` | MATRIX | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expense. |
| 928 | `sga_expense_2` | MATRIX | 0.770 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Selling/General/Administrative Expense |
| 929 | `fnd23_annfv1a_nimc` | MATRIX | 0.768 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the share of earnings/losses in subsidiaries that belongs to shareholders other than the parent company when |
| 930 | `fnd23_intfvalld1_nscf` | MATRIX | 0.768 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance or repurchase of common stock is not separately delineated, then the total is classified as Common |
| 931 | `fnd23_annfvalld1_dltv` | MATRIX | 0.767 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Long Term Debt, Supplemental reflects the sum of Long Term Debt Maturing within 1 through 10 Years and Long Term D |
| 932 | `fnd23_annfvalld1_b6dls` | MATRIX | 0.767 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standardized Long Term Debt Maturing in Year 6 & Beyond |
| 933 | `fnd23_annfvalld1_1dls` | MATRIX | 0.767 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long Term Debt Maturing within 1 Year |
| 934 | `fnd23_intfvalld1_pdcf` | MATRIX | 0.766 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Cash Dividends Paid. |
| 935 | `fnd23_cogs` | MATRIX | 0.765 | 其他 | 0 | — | — | — | UNTESTED | cost of goods sold |
| 936 | `fnd23_annfvalld1_ltia` | MATRIX | 0.764 | 其他 | 0 | — | — | — | UNTESTED | total inventory. |
| 937 | `fnd23_intfvm_rdlf` | MATRIX | 0.764 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash outflow on the repayment of long-term debt in a company. Long-term debt obligations may be repaid upon m |
| 938 | `long_term_debt_repaid` | MATRIX | 0.764 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Long Term Debt Reduction |
| 939 | `fnd23_annfvalld1_vsrl` | MATRIX | 0.763 | 其他 | 0 | — | — | — | UNTESTED | Reserves |
| 940 | `total_assets_4` | MATRIX | 0.763 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sum of all assets owned by the company. |
| 941 | `total_liabilities_equity` | MATRIX | 0.763 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sum of total liabilities and equity as reported on the balance sheet. |
| 942 | `dividends_noncontrolling_interest` | MATRIX | 0.763 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends paid to noncontrolling interest holders during the period. |
| 943 | `long_term_debt_value` | MATRIX | 0.763 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total amount of long-term debt obligations for the period. |
| 944 | `short_term_loans_debt_2` | MATRIX | 0.763 | 盈利与财务 | 0 | — | — | — | UNTESTED | Short-term loans and debt obligations due within one year. |
| 945 | `total_equity_book_value` | MATRIX | 0.763 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value of total equity as reported on the balance sheet. |
| 946 | `voting_beneficial_equity_shares` | MATRIX | 0.762 | 盈利与财务 | 0 | — | — | — | UNTESTED | Voting beneficial equity shares reported for the annual period. |
| 947 | `fnd23_intfvm_rpds` | MATRIX | 0.762 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/amortization represents sum of depreciation, amortization of intangibles and amortization of acquisition co |
| 948 | `pretax_profit_value` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] epreciation/Amortization |
| 949 | `securities_deferred_net_income` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Deferred net income related to securities for the annual period. |
| 950 | `quasi_equity_contracts` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quasi-equity contracts reported for the annual period. |
| 951 | `annual_net_income_value` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income reported for the annual period. |
| 952 | `long_term_trade_debt` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term trade debt reported for the annual period. |
| 953 | `total_assets_annual_atot` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets reported for the annual period. |
| 954 | `long_term_loans_liabilities` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term loans and liabilities reported for the annual period. |
| 955 | `quasi_equity_liabilities` | MATRIX | 0.761 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quasi-equity liabilities reported for the annual period. |
| 956 | `fnd23_annfvalld1_pics` | MATRIX | 0.760 | 其他 | 0 | — | — | — | UNTESTED | cash interest paid represents interest paid in cash during the period Cash Interest. |
| 957 | `statement_of_cash_flows` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Statement of cash flows for the annual period. |
| 958 | `other_long_term_obligations` | MATRIX | 0.760 | 其他 | 0 | — | — | — | UNTESTED | Other long-term obligations reported for the annual period. |
| 959 | `fnd23_annfvalld1_2los` | MATRIX | 0.760 | 其他 | 0 | — | — | — | UNTESTED | Operating Lease Payments Due in Year 2 |
| 960 | `fnd23_annfvalld1_32los` | MATRIX | 0.760 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Years 2 and 3 represents the summation of Standardized Operating Lease Paym |
| 961 | `fnd23_intfvalld1_ndlf` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | If long-term debt issuances and reductions are not delineated separately, the total is classified as Long-Term Debt, Net |
| 962 | `fnd23_annfvalld1_cila` | MATRIX | 0.760 | 其他 | 0 | — | — | — | UNTESTED | represents land and improvements on land at acquisition cost. Land is not depreciated, but land improvements are normall |
| 963 | `fnd23_blsm_pbts` | MATRIX | 0.760 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Tangible Book Value per Share, Common Eq |
| 964 | `fnd23_blsmalld1_pbts` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value per Share, Common Equity. |
| 965 | `fnd23_intfvalld1_lcol` | MATRIX | 0.760 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current liabilities. |
| 966 | `fnd23_icsm_m_sebv` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Basic Normalized EPS |
| 967 | `fnd23_icsm_m_sedv` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted Normalized EPS |
| 968 | `fnd23_icsm_malld1_sebv` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Basic Normalized EPS  represents the bottom-line earnings per share available to common stockholders, excluding the eff |
| 969 | `fnd23_icsm_malld1_sedv` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | Diluted Normalized EPS |
| 970 | `fnd23_blsm_dlts` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Debt |
| 971 | `fnd23_icsm_m_iabs` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Basic EPS Including Extraordinary Items |
| 972 | `fnd23_icsm_m_iads` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted EPS Including ExtraOrd Items |
| 973 | `discontinued_operations_net_income` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Net Income represents the bottom-line net income available to common shareholders, including extraordinary items |
| 974 | `fnd23_blsm_octq` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Total Common Shares Outstanding |
| 975 | `fnd23_blsmalld1_dlts` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Debt represents total interest-bearing debt outstanding. |
| 976 | `fnd23_icsm_m_caiv` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized Inc. Avail to Com. |
| 977 | `fnd23_icsm_m_fbbs` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Basic EPS Excluding Extraordinary Items |
| 978 | `fnd23_icsm_m_fbds` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted EPS Excluding ExtraOrd Items |
| 979 | `fnd23_icsm_m_inds` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted Net Income |
| 980 | `fnd23_icsm_m_taiv` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized Income After Taxes |
| 981 | `fnd23_icsm_malld1_caiv` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Available to Common represents the bottom-line net income available to common shareholders, excluding |
| 982 | `fnd23_icsm_malld1_iabs` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, including the effects of extraordinary i |
| 983 | `fnd23_icsm_malld1_iads` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Including Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 984 | `fnd23_blsm_dttl` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Long Term Debt |
| 985 | `fnd23_blsm_eltq` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Equity |
| 986 | `fnd23_blsm_letq` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Liabilities & Shareholders' Equity |
| 987 | `fnd23_blsm_tota` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Assets |
| 988 | `fnd23_icsm_m_itpv` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized Income Before Taxes |
| 989 | `fnd23_icsm_malld1_fbbs` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the bottom-line earnings per share available to common stockholders, excluding the effects of extraordinary |
| 990 | `fnd23_icsm_malld1_fbds` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted EPS Excluding Extraordinary Items represents the bottom-line earnings per share available to common stockholders |
| 991 | `fnd23_icsm_malld1_taiv` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | Normalized Income After Taxes. |
| 992 | `total_assets_6` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | total assets of the company. |
| 993 | `treasury_stock_other` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | represents the number of primary common shares equivalent outstanding. |
| 994 | `basic_earnings_per_share` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the weighted average common shares outstanding less the dilution of stock options for a given period. These s |
| 995 | `debt_writeoff_sum` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Diluted Weighted Average Shares represents the number of shares for Diluted EPS computation. |
| 996 | `extraordinary_net_income_component_2` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | Income Available to Common Stocks Incl. Extraordinary Items represents the bottom-line net income available to common s |
| 997 | `fnd23_blsm_lltl` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Liabilities |
| 998 | `fnd23_blsm_vbts` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Tangible Book Value, Common Equity |
| 999 | `fnd23_icsm_m_cinx` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Available to Com Incl ExtraOrd |
| 1000 | `fnd23_icsm_m_sabs` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Basic Weighted Average Shares |
| 1001 | `fnd23_icsm_m_swds` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Diluted Weighted Average Shares |
| 1002 | `fnd23_icsm_m_tait` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Income After Taxes |
| 1003 | `fnd23_icsm_malld1_itpv` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Income Before Taxes represents net income before taxes, excluding the effects of all non-recurring/unusual/on |
| 1004 | `fnd23_intfvm_eiue` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | Acquisition costs/expenses. |
| 1005 | `long_term_trade_debt_3` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 1006 | `total_liabilities_equity_2` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | total equity. |
| 1007 | `treasury_stock_preferred` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | sum of total liabilities and total equity. |
| 1008 | `fnd23_blsmalld1_lltl` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | total liabilities. |
| 1009 | `fnd23_blsmalld1_vbts` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tangible Book Value, Common Equity. |
| 1010 | `fnd23_icsm_m_caic` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Available to Com Excl ExtraOrd |
| 1011 | `fnd23_icsm_m_cnin` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Incl Extra Before Distributions |
| 1012 | `fnd23_icsm_m_tbie` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Income Before Taxes |
| 1013 | `fnd23_icsm_m_xbin` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Income Before Extra. Items |
| 1014 | `income_after_corporate_actions` | MATRIX | 0.759 | 宏观与行业 | 0 | — | — | — | UNTESTED | Income Available to Common Excl. Extraordinary Items |
| 1015 | `income_after_tax` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | Net Income After Taxes |
| 1016 | `unrealized_investment_equity` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Unusual Income/Expense |
| 1017 | `earnings_before_tax_3` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents a company’s total revenues reduced by total expenses, before taxes on net income and all after-tax adjustment |
| 1018 | `fnd23_annfvmfm2_rcao` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | represents changes in accounts receivable during the period. An increase in accounts receivable has a negative impact on |
| 1019 | `net_income_before_extraordinary_2` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents net income after taxes, adjusted by minority interest, equity in affiliates and the U.S. GAAP adjustment, bef |
| 1020 | `net_income_total_4` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income after taxes, adjusted by minority interest, equity in affiliates, the U.S. GAAP adjustment and extraordinary |
| 1021 | `fnd23_annfv1a_rcao` | MATRIX | 0.759 | 其他 | 0 | — | — | — | UNTESTED | represents changes in accounts receivable during the period. An increase in accounts receivable has a negative impact on |
| 1022 | `fnd23_annfvalld1_iqea` | MATRIX | 0.758 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents long-term investment in securities (loans, bonds, and equity) of affiliate companies, where the affiliation m |
| 1023 | `fnd23_icsm_m_ntiv` | MATRIX | 0.758 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Taxes Excluding Impact of Special Items |
| 1024 | `fnd23_icsm_malld1_ntiv` | MATRIX | 0.758 | 其他 | 0 | — | — | — | UNTESTED | Income Taxes Excluding Impact of Special Items represents total income taxes, adjusted by the tax impact of adding back |
| 1025 | `fnd23_icsm_m_xatt` | MATRIX | 0.758 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Provision for Income Taxes |
| 1026 | `total_income_tax_expense` | MATRIX | 0.758 | 其他 | 0 | — | — | — | UNTESTED | Provision for Income Taxes. |
| 1027 | `fnd23_intfvalld1_deds` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/Depletion represents the sum of Depreciation and Depletion. |
| 1028 | `fnd23_cf_m_fcos` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Changes in Working Capital |
| 1029 | `fnd23_cf_malld1_fcos` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | Changes in Working Capital |
| 1030 | `fnd23_cf_m_olto` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash from Operating Activities |
| 1031 | `other_long_term_obligations_7` | MATRIX | 0.757 | 盈利与财务 | 0 | — | — | — | UNTESTED | includes diverse cash flows that are reported outside of the operating, investing and financing sections of the cash flo |
| 1032 | `fnd23_cf_m_ccns` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Net Change in Cash |
| 1033 | `fnd23_blsm_smcs` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Common Stock, Total |
| 1034 | `short_term_net_cash_change` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | Net Change in Cash |
| 1035 | `fnd23_cf_m_fltf` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash from Financing Activities |
| 1036 | `funds_transfer_loan_facility` | MATRIX | 0.757 | 盈利与财务 | 0 | — | — | — | UNTESTED | cash from financing activities that is the sum of financing cash flow items, cash dividends paid, issuance of stock, net |
| 1037 | `short_term_commercial_paper` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | total common stock represets the combined value of common stock and limited partner. |
| 1038 | `fnd23_blsm_smcq` | MATRIX | 0.757 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Common Stock |
| 1039 | `common_stock_shares` | MATRIX | 0.756 | 其他 | 0 | — | — | — | UNTESTED | Common Stock represents the value of the most frequently issued class of stock; usually it provides a voting right, but |
| 1040 | `fnd23_intfvalld1_rcaa` | MATRIX | 0.756 | 其他 | 0 | — | — | — | UNTESTED | accounts receivable value. |
| 1041 | `other_long_term_obligations_6` | MATRIX | 0.756 | 其他 | 0 | — | — | — | UNTESTED | Other obligations due beyond one year not classified elsewhere. |
| 1042 | `fnd23_blsm_derq` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Retained Earnings (Accumulated Deficit) |
| 1043 | `fnd23_intfvm_acoa` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current assets. |
| 1044 | `fnd23_blsmalld1_derq` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents residual earnings from operations, not distributed to shareholders. It may represent accumulated deficit when |
| 1045 | `other_current_assets_5` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Current Assets |
| 1046 | `fnd23_cf_m_ilti` | MATRIX | 0.756 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash from Investing Activities |
| 1047 | `fnd23_icsm_m_mpns` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Profit Margin |
| 1048 | `fnd23_icsm_m_mtps` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Pretax Margin |
| 1049 | `fnd23_icsm_malld1_mpns` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Profit Margin represents Income Available to Common Excluding Extraordinary Items divided by Total Revenue. |
| 1050 | `fnd23_icsm_malld1_mtps` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax Margin. |
| 1051 | `interest_liabilities` | MATRIX | 0.756 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash from Investing Activities. |
| 1052 | `fnd23_annfvalld1_ltll` | MATRIX | 0.755 | 其他 | 0 | — | — | — | UNTESTED | Long-term obligations from right-of-use contracts related to operating leases. |
| 1053 | `fnd23_ffcf` | MATRIX | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | free cash flow to the firm |
| 1054 | `fnd23_annfvalld1_agse` | MATRIX | 0.754 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expense. |
| 1055 | `fnd23_annfvalld1_rpds` | MATRIX | 0.753 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/amortization represents the sum of depreciation, amortization of intangibles, and amortization of acquisiti |
| 1056 | `fnd23_intfvm_eiuo` | MATRIX | 0.753 | 盈利与财务 | 0 | — | — | — | UNTESTED | is applicable only if Net Income/Starting Line [ONET] is income after gains/losses from unusual activities. Because the |
| 1057 | `unrealized_investment_equity_2` | MATRIX | 0.753 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Unusual Items |
| 1058 | `fnd23_annfvalld1_acos` | MATRIX | 0.753 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Assets, Total. |
| 1059 | `fnd23_cf_m_fcis` | MATRIX | 0.752 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Investing Cash Flow Items, Total |
| 1060 | `fnd23_intfvm_saoa` | MATRIX | 0.752 | 盈利与财务 | 0 | — | — | — | UNTESTED | non operational fixed assets that are long term. |
| 1061 | `short_term_investment_cash_flow` | MATRIX | 0.752 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Investing Cash Flow Items, Total represents all items reported within the investing activities in the cash flow st |
| 1062 | `other_assets_short_term` | MATRIX | 0.752 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Long Term Assets |
| 1063 | `fnd23_intfvalld1_eooe` | MATRIX | 0.752 | 其他 | 0 | — | — | — | UNTESTED | Depreciation of investment properties disclosed outside of the cost of goods sold, for companies reporting in the IFRS o |
| 1064 | `fnd23_blsm_lcos` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Current liabilities, Total |
| 1065 | `fnd23_cf_m_bcns` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Net Cash - Beginning Balance |
| 1066 | `fnd23_cf_m_ecns` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Net Cash - Ending Balance |
| 1067 | `short_term_net_cash_balance` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Net Cash – Beginning Balance represents the beginning balance of cash and cash equivalents, as defined by a company. |
| 1068 | `short_term_net_cash_expense` | MATRIX | 0.751 | 其他 | 0 | — | — | — | UNTESTED | Net Cash – Ending Balance represents the sum of Net Change in Cash and Net Cash –Beginning Balance. |
| 1069 | `fnd23_blsmalld1_lcos` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Liabilities, Total. |
| 1070 | `fnd23_annfv1a_pnii` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Acquisition of investment securities of a company (rather than the whole business unit) classified as Purchase of Invest |
| 1071 | `share_capital_extraordinary` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Extraordinary share capital reported for the annual period. |
| 1072 | `fnd23_blsm_nppa` | MATRIX | 0.749 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Property/Plant/Equipment,Total - Net |
| 1073 | `prepaid_insurance` | MATRIX | 0.749 | 其他 | 0 | — | — | — | UNTESTED | net property, plant and equipment. |
| 1074 | `fnd23_intfvalld1_nnin` | MATRIX | 0.749 | 其他 | 0 | — | — | — | UNTESTED | Interest expense that is reduced by interest income. |
| 1075 | `fnd23_intfvalld1_vnin` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents income or losses, other than interest, from investment securities. Such income may include dividend income, g |
| 1076 | `fnd23_icsm_m_pedv` | MATRIX | 0.748 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Depreciation, Supplemental |
| 1077 | `fnd23_intfvalld1_cpdf` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | common cash dividends paid |
| 1078 | `fnd23_icsm_malld1_pedv` | MATRIX | 0.748 | 其他 | 0 | — | — | — | UNTESTED | Deprecation |
| 1079 | `fnd23_annfvalld1_atda` | MATRIX | 0.747 | 风险与质量 | 0 | — | — | — | UNTESTED | deferred income taxes - long term. These are credits being applied to income taxes that will be paid in future years. |
| 1080 | `fnd23_annfvalld1_3los` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Year 3. |
| 1081 | `fnd23_intfvalld1_xeiv` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Supplemental. |
| 1082 | `fnd23_cf_m_xecs` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Capital Expenditures |
| 1083 | `short_term_contracts_executed` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | capital expenditures. |
| 1084 | `fnd23_annfv1a_cila` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | represents land and improvements on land at acquisition cost. Land is not depreciated, but land improvements are normall |
| 1085 | `fnd23_intfvm_iqea` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents long-term investment in securities (loans, bonds, and equity) of affiliate companies, where the affiliation |
| 1086 | `accrued_equity_investments` | MATRIX | 0.746 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] LT Investment - Affiliate Companies |
| 1087 | `fnd23_intfvalld1_ltia` | MATRIX | 0.746 | 其他 | 0 | — | — | — | UNTESTED | total inventory. |
| 1088 | `fnd23_intfvm_tnoe` | MATRIX | 0.746 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Income from external grants received to cover research and development expenses. |
| 1089 | `other_nonoperating_income_2` | MATRIX | 0.745 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other, Net |
| 1090 | `fnd23_annfv1a_ltia` | MATRIX | 0.745 | 其他 | 0 | — | — | — | UNTESTED | total inventory. |
| 1091 | `fnd23_ltem` | MATRIX | 0.745 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Number of Employees |
| 1092 | `minority_interest_liabilities` | MATRIX | 0.745 | 盈利与财务 | 0 | — | — | — | UNTESTED | Full-Time Employees |
| 1093 | `fnd23_intfvalld1_vsrl` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | Reserves |
| 1094 | `fnd23_annfvalld1_etos` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Equity, Total. |
| 1095 | `fnd23_cf_m_xeci` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Capital Expenditures |
| 1096 | `investment_cash_expenditures` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | purchase of fixed assets. |
| 1097 | `fnd23_intfvm_cisf` | MATRIX | 0.744 | 持仓与资金流 | 0 | — | — | — | UNTESTED | represents cash inflow from the issuance of common stock. It also includes cash inflow from the sale of treasury shares. |
| 1098 | `sale_of_investments` | MATRIX | 0.744 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Sale/Issuance of Common |
| 1099 | `fnd23_blsm_ltls` | MATRIX | 0.744 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Liabilities, Total |
| 1100 | `fnd23_blsmalld1_ltls` | MATRIX | 0.743 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Liabilities, Total |
| 1101 | `fnd23_intfvalld1_pics` | MATRIX | 0.743 | 其他 | 0 | — | — | — | UNTESTED | cash interest paid represents interest paid in cash during the period Cash Interest. |
| 1102 | `fnd23_intfvalld1_ltll` | MATRIX | 0.742 | 其他 | 0 | — | — | — | UNTESTED | Long-term obligations from right-of-use contracts related to operating leases. |
| 1103 | `fnd23_annfvalld1_4los` | MATRIX | 0.742 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Year 4. |
| 1104 | `fnd23_annfvalld1_54los` | MATRIX | 0.742 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Years 4 and 5 represents the summation of Standardized Operating Lease Paym |
| 1105 | `fnd23_annfvalld1_dgcd` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | gross dividends on common stock. |
| 1106 | `fnd23_intfvm_ltia` | MATRIX | 0.741 | 其他 | 0 | — | — | — | UNTESTED | total inventory. |
| 1107 | `intangible_assets_licenses` | MATRIX | 0.741 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Inventory |
| 1108 | `inventory` | MATRIX | 0.741 | 其他 | 0 | — | — | — | UNTESTED | total inventory. |
| 1109 | `fnd23_intfvm_iwga` | MATRIX | 0.740 | 其他 | 0 | — | — | — | UNTESTED | net goodwill. |
| 1110 | `accrued_goodwill_intangible` | MATRIX | 0.740 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Goodwill, Net |
| 1111 | `goodwill` | MATRIX | 0.740 | 其他 | 0 | — | — | — | UNTESTED | net goodwill. |
| 1112 | `fnd23_annfvalld1_cisf` | MATRIX | 0.740 | 持仓与资金流 | 0 | — | — | — | UNTESTED | represents cash inflow from the issuance of common stock. It also includes cash inflow from the sale of treasury shares. |
| 1113 | `fnd23_annfv1a_saoa` | MATRIX | 0.738 | 盈利与财务 | 0 | — | — | — | UNTESTED | non operational fixed assets that are long term. |
| 1114 | `fnd23_annfvalld1_pxrv` | MATRIX | 0.738 | 其他 | 0 | — | — | — | UNTESTED | Rental Expense, Supplemental represents the total value of rental expenses paid for offices, factories, machinery, and e |
| 1115 | `cash` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | total current assets - total net receivables. |
| 1116 | `other_net_equity_total` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total of other net equity items for the annual period. |
| 1117 | `enterprise_value` | MATRIX | 0.737 | 其他 | 0 | — | — | — | UNTESTED | enterprise value. |
| 1118 | `fnd23_annfv1a_32dls` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standardized Long Term Debt Maturing in Years 2 and 3 represents the summation of Standardized Long Term Debt Maturing i |
| 1119 | `fnd23_annfvalld1_tnos` | MATRIX | 0.737 | 盈利与财务 | 0 | — | — | — | UNTESTED | other net income. |
| 1120 | `fnd23_annfv1a_2dls` | MATRIX | 0.736 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standardized Long Term Debt Maturing in Year 2 |
| 1121 | `fnd23_intfvalld1_rpds` | MATRIX | 0.736 | 其他 | 0 | — | — | — | UNTESTED | Depreciation/amortization represents the sum of depreciation, amortization of intangibles, and amortization of acquisiti |
| 1122 | `fnd23_annfvalld1_cets` | MATRIX | 0.736 | 其他 | 0 | — | — | — | UNTESTED | Effect of Special Items on Income Taxes. |
| 1123 | `fnd23_annfvalld1_5los` | MATRIX | 0.735 | 其他 | 0 | — | — | — | UNTESTED | Standardized Operating Lease Payments Due in Year 5. |
| 1124 | `fnd23_annfvalld1_tnon` | MATRIX | 0.734 | 其他 | 0 | — | — | — | UNTESTED | represents any non-operating income or expense item that a company reports before income taxes |
| 1125 | `fnd23_annfv1a_aiev` | MATRIX | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity in Affiliates, Supplemental represents the total share of earnings/losses, net of taxes, that the company is ent |
| 1126 | `fnd23_intfvm_nnin` | MATRIX | 0.732 | 其他 | 0 | — | — | — | UNTESTED | Interest expense that is reduced by interest income. |
| 1127 | `net_income_noncontrolling_interest` | MATRIX | 0.732 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Income (Expense), Net |
| 1128 | `fnd23_intfvalld1_iwga` | MATRIX | 0.731 | 其他 | 0 | — | — | — | UNTESTED | net goodwill. |
| 1129 | `fnd23_icsm_m_rtes` | MATRIX | 0.731 | 宏观与行业 | 0 | — | — | — | UNTESTED | [Quarterly] Effective Tax Rate |
| 1130 | `extraordinary_items_total_4` | MATRIX | 0.731 | 宏观与行业 | 0 | — | — | — | UNTESTED | Effective Tax Rate represents Provision for Income Taxes divided by Income Before Tax. |
| 1131 | `fnd23_annfv1a_tnoe` | MATRIX | 0.731 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Income from external grants received to cover research and development expenses. |
| 1132 | `fnd23_cf_m_icns` | MATRIX | 0.731 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Non-Cash Items |
| 1133 | `fnd23_intfvalld1_cipq` | MATRIX | 0.731 | 价量与波动 | 0 | — | — | — | UNTESTED | represents capital contributed by shareholders in excess of par value of common stock in return for shares issued to the |
| 1134 | `short_term_net_cash_inflow` | MATRIX | 0.731 | 持仓与资金流 | 0 | — | — | — | UNTESTED | non-cash items. |
| 1135 | `share_deposit_equity` | MATRIX | 0.730 | 盈利与财务 | 0 | — | — | — | UNTESTED | Share deposit equity reported for the annual period. |
| 1136 | `fnd23_blsm_alos` | MATRIX | 0.730 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Long Term Assets, Total |
| 1137 | `other_long_term_assets_2` | MATRIX | 0.730 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Long-Term Assets, Total. |
| 1138 | `fnd23_intfvalld1_tnos` | MATRIX | 0.729 | 盈利与财务 | 0 | — | — | — | UNTESTED | other net income. |
| 1139 | `fnd23_cf_m_teno` | MATRIX | 0.728 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Income/Starting Line |
| 1140 | `fnd23_annfvalld1_rcao` | MATRIX | 0.728 | 其他 | 0 | — | — | — | UNTESTED | represents changes in accounts receivable during the period. An increase in accounts receivable has a negative impact on |
| 1141 | `other_net_earnings_total_2` | MATRIX | 0.728 | 盈利与财务 | 0 | — | — | — | UNTESTED | is the first line of a cash flow statement when a company employs the Indirect Method in the operating cash flow section |
| 1142 | `fnd23_intfvalld1_afsi` | MATRIX | 0.728 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sale of assets to be leased out under operating lease contracts |
| 1143 | `fnd23_icsm_m_uatv` | MATRIX | 0.728 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Audit Fees |
| 1144 | `tax_allowance_utilized` | MATRIX | 0.728 | 其他 | 0 | — | — | — | UNTESTED | Audit Fees |
| 1145 | `financing_proceeds_redeemable_debt` | MATRIX | 0.727 | 盈利与财务 | 0 | — | — | — | UNTESTED | If debt issuances and reductions are not delineated separately, the total is classified as Issuance (Retirement) of Debt |
| 1146 | `fnd23_cf_m_drpf` | MATRIX | 0.727 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Issuance (Retirement) of Debt, Net |
| 1147 | `fnd23_intfvalld1_tnon` | MATRIX | 0.727 | 其他 | 0 | — | — | — | UNTESTED | represents any non-operating income or expense item that a company reports before income taxes |
| 1148 | `fnd23_cf_m_icno` | MATRIX | 0.726 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other Non-Cash Items |
| 1149 | `fnd23_intfvm_pnii` | MATRIX | 0.726 | 其他 | 0 | — | — | — | UNTESTED | Acquisition of investment securities of a company (rather than the whole business unit) classified as Purchase of Invest |
| 1150 | `increase_in_investments` | MATRIX | 0.726 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Purchase of Investments |
| 1151 | `other_net_cash_inflows` | MATRIX | 0.726 | 持仓与资金流 | 0 | — | — | — | UNTESTED | other non cash items. |
| 1152 | `fnd23_annfv1a_idlf` | MATRIX | 0.726 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash inflow on the issuance of long-term debt instruments in a company. Long-term debt may include long-term |
| 1153 | `fnd23_annfv1a_eiue` | MATRIX | 0.726 | 其他 | 0 | — | — | — | UNTESTED | Acquisition costs/expenses. |
| 1154 | `retained_earnings_5` | MATRIX | 0.725 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cumulative net income retained in the business after dividends. |
| 1155 | `fnd23_annfvalld1_yppa` | MATRIX | 0.724 | 其他 | 0 | — | — | — | UNTESTED | prepaid expenses. |
| 1156 | `fnd23_blsm_ctpa` | MATRIX | 0.724 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Property/Plant/Equipment, Total - Gross |
| 1157 | `property_plant_and_equipment` | MATRIX | 0.724 | 其他 | 0 | — | — | — | UNTESTED | gross property, plant & equipment. |
| 1158 | `fnd23_annfvalld1_qabi` | MATRIX | 0.724 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash outflow for acquiring new businesses. Reporting the cash flow for acquiring new businesses is not consis |
| 1159 | `fnd23_blsm_peda` | MATRIX | 0.723 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Accumulated Depreciation, Total |
| 1160 | `accumulated_depreciation_3` | MATRIX | 0.723 | 盈利与财务 | 0 | — | — | — | UNTESTED | aggregate of accumulated depreciation for each fixed asset. |
| 1161 | `fnd23_blsm_bpal` | MATRIX | 0.723 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Accounts Payable |
| 1162 | `long_term_policyholder_liabilities` | MATRIX | 0.723 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accrued interest expenses, interest payable in commercial banks. |
| 1163 | `retained_earnings_liabilities` | MATRIX | 0.723 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings classified as liabilities for the annual period. |
| 1164 | `long_term_debt_total` | MATRIX | 0.722 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total long-term debt reported for the annual period. |
| 1165 | `fnd23_icsm_m_rltr` | MATRIX | 0.721 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Revenue |
| 1166 | `fnd23_intfvm_niin` | MATRIX | 0.721 | 宏观与行业 | 0 | — | — | — | UNTESTED | represents non-operating interest income, which is generated from non-operating investment securities such as certificat |
| 1167 | `total_rental_income` | MATRIX | 0.721 | 盈利与财务 | 0 | — | — | — | UNTESTED | total revenue represents all items clearly presented as revenues, before the cost of goods sold and the gross profit. |
| 1168 | `interest_income_net_2` | MATRIX | 0.720 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest/Investment Income |
| 1169 | `fnd23_icsm_m_ipos` | MATRIX | 0.720 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Operating Income |
| 1170 | `operating_income_4` | MATRIX | 0.720 | 其他 | 0 | — | — | — | UNTESTED | Operating Income. |
| 1171 | `fnd23_icsm_m_eote` | MATRIX | 0.720 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Total Operating Expenses |
| 1172 | `total_other_expense` | MATRIX | 0.720 | 价量与波动 | 0 | — | — | — | UNTESTED | represents total expenses that are operating in nature, including variable costs directly related to the volume of sales |
| 1173 | `fnd23_blsm_dtsl` | MATRIX | 0.720 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Notes Payable/Short Term Debt |
| 1174 | `long_term_securities_debt` | MATRIX | 0.720 | 盈利与财务 | 0 | — | — | — | UNTESTED | notes payable/short term debt. |
| 1175 | `fnd23_icsm_m_ists` | MATRIX | 0.719 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Total Special Items |
| 1176 | `fnd23_icsm_m_cets` | MATRIX | 0.719 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Effect of Special Items on Income Taxes |
| 1177 | `special_items_tax_effect` | MATRIX | 0.719 | 其他 | 0 | — | — | — | UNTESTED | Effect of Special Items on Income Taxes. |
| 1178 | `total_special_items` | MATRIX | 0.719 | 其他 | 0 | — | — | — | UNTESTED | Total Special Items represents the sum of all non-recurring/unusual/extraordinary/one-off/special gains and losses that |
| 1179 | `fnd23_cf_m_peds` | MATRIX | 0.718 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Depreciation |
| 1180 | `short_term_deposits` | MATRIX | 0.718 | 其他 | 0 | — | — | — | UNTESTED | depreciation. |
| 1181 | `fnd23_intfv_item` | VECTOR | 0.717 | 其他 | 0 | — | — | — | UNTESTED | integer index of the item description field. You can use this index to find out what the value is from itemIx. |
| 1182 | `fnd23_intfvalld1_1nstq` | MATRIX | 0.716 | 其他 | 0 | — | — | — | UNTESTED | Treasury Shares - Common Stock Primary Issue |
| 1183 | `share_dividend_equity` | MATRIX | 0.716 | 盈利与财务 | 0 | — | — | — | UNTESTED | Share dividend equity reported for the annual period. |
| 1184 | `fnd23_blsm_crta` | MATRIX | 0.716 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Total Receivables, Net |
| 1185 | `fnd23_blsmalld1_crta` | MATRIX | 0.715 | 其他 | 0 | — | — | — | UNTESTED | total net receivables. |
| 1186 | `fnd23_blsm_dtll` | MATRIX | 0.715 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Long Term Debt |
| 1187 | `long_term_liabilities_other` | MATRIX | 0.715 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest-bearing debt with maturities beyond one year. Long-term debt may consist of long-term bank borrowing |
| 1188 | `fnd23_cf_m_fcff` | MATRIX | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Financing Cash Flow |
| 1189 | `fnd23_cf_m_fcfs` | MATRIX | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Financing Cash Flow Items |
| 1190 | `free_firm_cash_flow` | MATRIX | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | other financing cash flow |
| 1191 | `short_term_financing_cash_flow` | MATRIX | 0.714 | 盈利与财务 | 0 | — | — | — | UNTESTED | financing cash flow items represents sum of increase/decrease ind eposits, increase/decrease in federal funds sold or RE |
| 1192 | `fnd23_intfvalld1_atda` | MATRIX | 0.713 | 风险与质量 | 0 | — | — | — | UNTESTED | deferred income taxes - long term. These are credits being applied to income taxes that will be paid in future years. |
| 1193 | `fnd23_blsm_tnia` | MATRIX | 0.713 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Intangibles, Net |
| 1194 | `interest_receivable` | MATRIX | 0.713 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Intangibles, Net |
| 1195 | `fnd23_icsm_m_ttiv` | MATRIX | 0.712 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Tax - Total |
| 1196 | `income_tax_total` | MATRIX | 0.712 | 其他 | 0 | — | — | — | UNTESTED | Income Tax – Total reflects the sum of Domestic Tax - Other, Foreign Tax – Other, Local Tax – Other and Other Tax. |
| 1197 | `fnd23_icsm_m_nins` | MATRIX | 0.711 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Income (Exp), Net- Non-Operating, Total |
| 1198 | `net_income_including_nonrecurring` | MATRIX | 0.710 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense (Income), Net- Non-Operating, Total |
| 1199 | `fnd23_annfvalld1_eooe` | MATRIX | 0.710 | 其他 | 0 | — | — | — | UNTESTED | Depreciation of investment properties disclosed outside of the cost of goods sold, for companies reporting in the IFRS o |
| 1200 | `fnd23_icsm_m_dgcd` | MATRIX | 0.710 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Gross Dividends - Common Stock |
| 1201 | `goodwill_depreciation_charge` | MATRIX | 0.710 | 盈利与财务 | 0 | — | — | — | UNTESTED | gross dividends on common stock. |
| 1202 | `fnd23_annfvalld1_ralv` | MATRIX | 0.710 | 其他 | 0 | — | — | — | UNTESTED | Total labor costs: Labor & Related Expense, Supplemental |
| 1203 | `fnd23_icsm_m_agss` | MATRIX | 0.709 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Selling/General/Admin. Expenses, Total |
| 1204 | `selling_general_admin_expense_3` | MATRIX | 0.709 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expenses, Total. |
| 1205 | `fnd23_icsm_m_ctcv` | MATRIX | 0.709 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Current Tax - Total |
| 1206 | `contract_costs_expense` | MATRIX | 0.709 | 其他 | 0 | — | — | — | UNTESTED | Current Tax – Total reflects the sum of Current Tax – Domestic, Current Tax – Foreign, Current Tax – Local, Current Tax |
| 1207 | `fnd23_blsm_etos` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Equity, Total |
| 1208 | `net_income_value_3` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total profit after all expenses, taxes, and costs for the period. |
| 1209 | `other_equity` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Equity, Total. |
| 1210 | `fnd23_annfv1a_itsa` | MATRIX | 0.708 | 其他 | 0 | — | — | — | UNTESTED | Short-Term Investments |
| 1211 | `fnd23_intfvalld1_dlcl` | MATRIX | 0.707 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Port. of LT Debt/Capital Leases. |
| 1212 | `fnd23_intfvalld1_eefs` | MATRIX | 0.706 | 宏观与行业 | 0 | — | — | — | UNTESTED | Foreign Exchange Effects represents the increase/decrease in cash and cash equivalents due to changes in exchange rates. |
| 1213 | `fnd23_intfvm2_pcsv` | MATRIX | 0.705 | 其他 | 0 | — | — | — | UNTESTED | Stock-Based Compensation, Supplemental |
| 1214 | `fnd23_icsm_m_niis` | MATRIX | 0.705 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest/Invest Income - Non-Operating |
| 1215 | `fnd23_intfvalld1_acos` | MATRIX | 0.705 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Assets, Total. |
| 1216 | `interest_income_net` | MATRIX | 0.704 | 其他 | 0 | — | — | — | UNTESTED | Interest/Investment Income, Non-Operating |
| 1217 | `fnd23_cf_m_deds` | MATRIX | 0.704 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Depreciation/Depletion |
| 1218 | `short_term_debt_issued` | MATRIX | 0.704 | 盈利与财务 | 0 | — | — | — | UNTESTED | Depreciation/Depletion represents the sum of Depreciation and Depletion. |
| 1219 | `fnd23_annfvalld1_1nstq` | MATRIX | 0.703 | 其他 | 0 | — | — | — | UNTESTED | Treasury Shares - Common Stock Primary Issue |
| 1220 | `fnd23_annfvalld1_32dls` | MATRIX | 0.703 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standardized Long-Term Debt Maturing in Years 2 and 3 represents the summation of Standardized Long-Term Debt Maturing i |
| 1221 | `income_before_tax_value` | MATRIX | 0.703 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before provision for income taxes for the period. |
| 1222 | `fnd23_annfvalld1_2dls` | MATRIX | 0.703 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standardized Long-Term Debt Maturing in Year 7 |
| 1223 | `share_capital_subscribed` | MATRIX | 0.701 | 其他 | 0 | — | — | — | UNTESTED | Share capital subscribed reported for the annual period. |
| 1224 | `fnd23_blsm_croa` | MATRIX | 0.700 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Receivables - Other |
| 1225 | `other_receivables_2` | MATRIX | 0.700 | 其他 | 0 | — | — | — | UNTESTED | other receivables. |
| 1226 | `fnd23_icsm_m_xeiv` | MATRIX | 0.700 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Expense, Supplemental |
| 1227 | `investment_expense` | MATRIX | 0.700 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Supplemental. |
| 1228 | `fnd23_annfvalld1_eefs` | MATRIX | 0.699 | 宏观与行业 | 0 | — | — | — | UNTESTED | Foreign Exchange Effects represents the increase/decrease in cash and cash equivalents due to changes in exchange rates. |
| 1229 | `fnd23_icsm_m_ctdv` | MATRIX | 0.699 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Deferred Tax - Total |
| 1230 | `depreciation_total` | MATRIX | 0.699 | 其他 | 0 | — | — | — | UNTESTED | Deferred Tax – Total |
| 1231 | `voting_amortized_investments` | MATRIX | 0.699 | 其他 | 0 | — | — | — | UNTESTED | Voting amortized investments reported for the annual period. |
| 1232 | `fnd23_icsm_m_tibs` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized EBIT |
| 1233 | `fnd23_blsm_dtns` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Net Debt Including Preferred Stock & Minority Interest |
| 1234 | `fnd23_icsm_malld1_tibs` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest and Taxes. |
| 1235 | `short_term_notes_payable_2` | MATRIX | 0.699 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Debt Including Preferred Stock & Minority Interest. |
| 1236 | `fnd23_blsm_iscs` | MATRIX | 0.698 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash and Short Term Investments |
| 1237 | `long_term_collateral_debt` | MATRIX | 0.698 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term collateralized debt reported for the annual period. |
| 1238 | `short_term_customer_securities` | MATRIX | 0.698 | 其他 | 0 | — | — | — | UNTESTED | cash and short-term investments. |
| 1239 | `fnd23_cf_m_sspf` | MATRIX | 0.698 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Issuance (Retirement) of Stock, Net |
| 1240 | `financing_proceeds_share_sale` | MATRIX | 0.698 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance or repurchase of common and preferred stock is not separately delineated, then the total is classi |
| 1241 | `fnd23_icsm_m_vers` | MATRIX | 0.698 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Revenue |
| 1242 | `total_revenue_3` | MATRIX | 0.698 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue represents revenues from the sale of merchandise goods, manufactured products and services, and the distributio |
| 1243 | `fnd23_annfvalld1_nnin` | MATRIX | 0.697 | 其他 | 0 | — | — | — | UNTESTED | Interest expense that is reduced by interest income. |
| 1244 | `fnd23_annfvalld1_acoa` | MATRIX | 0.697 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current assets. |
| 1245 | `fnd23_annfv1a_atcq` | MATRIX | 0.696 | 其他 | 0 | — | — | — | UNTESTED | represents translation gains (losses) on financial statements of foreign subsidiaries. Such adjustments may be required |
| 1246 | `fnd23_intfvm_idlf` | MATRIX | 0.695 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash inflow on the issuance of long-term debt instruments in a company. Long-term debt may include long-term |
| 1247 | `fnd23_icsm_m_ppos` | MATRIX | 0.695 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Operating Margin |
| 1248 | `long_term_debt_issued` | MATRIX | 0.695 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Long Term Debt Issued |
| 1249 | `operating_profit_percentage` | MATRIX | 0.695 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin. |
| 1250 | `long_term_current_liabilities_3` | MATRIX | 0.695 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current portion of long-term liabilities due within one year. |
| 1251 | `fnd23_blsm_xeal` | MATRIX | 0.695 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Accrued Expenses |
| 1252 | `long_term_accrued_expenses` | MATRIX | 0.695 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents operational expenses accrued, but not yet paid. As current liabilities, such expenses are expected to be paid |
| 1253 | `inventory_turnover` | MATRIX | 0.694 | 价量与波动 | 0 | — | — | — | UNTESTED | inventory turnover. |
| 1254 | `fnd23_blsm_pxtl` | MATRIX | 0.694 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Taxes Payable |
| 1255 | `fnd23_intfvalld1_agse` | MATRIX | 0.694 | 其他 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expense. |
| 1256 | `long_term_tax_payable_3` | MATRIX | 0.694 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Taxes Payable represents income taxes payable to the government, where such tax liability is already confirmed i |
| 1257 | `total_current_assets_4` | MATRIX | 0.694 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total current assets reported for the annual period. |
| 1258 | `long_term_contract_liabilities` | MATRIX | 0.693 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term contract liabilities reported for the annual period. |
| 1259 | `fnd23_blsm_vnis` | MATRIX | 0.693 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Long Term Investments |
| 1260 | `short_term_investments_6` | MATRIX | 0.693 | 其他 | 0 | — | — | — | UNTESTED | Long-Term Investments represents the sum of LT Investments – Affiliate Companies and LT Investments – Other. |
| 1261 | `fnd23_blsm_eaca` | MATRIX | 0.693 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash & Equivalents |
| 1262 | `accrued_expenses_2` | MATRIX | 0.693 | 其他 | 0 | — | — | — | UNTESTED | cash & equivalents. |
| 1263 | `fnd23_blsm_tdbl` | MATRIX | 0.693 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] NOT_SELECTED Deferred Income Tax - LT Liability |
| 1264 | `fnd23_blsm_tdbs` | MATRIX | 0.693 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Deferred Income Tax |
| 1265 | `long_term_bank_debt` | MATRIX | 0.693 | 修正与预期 | 0 | — | — | — | UNTESTED | represents income taxes estimated and expected to be paid within one year or an operating cycle, whichever is longer. |
| 1266 | `short_term_bank_debt` | MATRIX | 0.693 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Deferred Income Tax – Long Term Liability and Deferred Investment Tax Credit |
| 1267 | `fnd23_annfvalld1_itsa` | MATRIX | 0.692 | 其他 | 0 | — | — | — | UNTESTED | Short-Term Investments |
| 1268 | `fnd23_icsm_m_adbs` | MATRIX | 0.692 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Normalized EBITDA |
| 1269 | `fnd23_icsm_malld1_adbs` | MATRIX | 0.692 | 盈利与财务 | 0 | — | — | — | UNTESTED | Normalized Earnings before Interest, Taxes, Depreciation and Amortization |
| 1270 | `fnd23_annfv1a_pede` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | Depreciation of fixed assets reported outside of the cost of goods and services sold. |
| 1271 | `fnd23_blsm_acta` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Current Assets |
| 1272 | `total_current_assets_6` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | total current assets. Sum of cash and short term investments, total receivables (net), total inventory, prepaid expenses |
| 1273 | `fnd23_blsm_lctl` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Current Liabilities |
| 1274 | `fnd23_icsm_m_imav` | MATRIX | 0.691 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Amortization of Intangibles, Supplemental |
| 1275 | `long_term_capital_lease_obligation` | MATRIX | 0.691 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents current liabilities for industrial and utility companies. Current liabilities are liabilities that are incurr |
| 1276 | `amortization_of_intangibles` | MATRIX | 0.691 | 其他 | 0 | — | — | — | UNTESTED | Amortization. |
| 1277 | `fnd23_cf_m_ptcs` | MATRIX | 0.690 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash Taxes Paid |
| 1278 | `short_term_cash_transaction_proceeds` | MATRIX | 0.690 | 持仓与资金流 | 0 | — | — | — | UNTESTED | cash taxes paid represents taxes paid in cash, net of tax refunds received, as reported by the company. |
| 1279 | `fnd23_blsm_iucs` | MATRIX | 0.690 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Current Assets less Inventory |
| 1280 | `fnd23_blsm_kcqs` | MATRIX | 0.690 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Quick Ratio |
| 1281 | `fnd23_blsm_rucs` | MATRIX | 0.690 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Current Ratio |
| 1282 | `short_term_currency_assets` | MATRIX | 0.690 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Ratio represents Total Current Assets divided by Total Current Liabilities. |
| 1283 | `short_term_quick_liabilities` | MATRIX | 0.690 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick Ratio represents Total Current Assets less Inventory divided by Total Current Liabilities. |
| 1284 | `short_term_customer_investments` | MATRIX | 0.690 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Current Assets less Inventory represents Total Current Assets minus Total Inventory. |
| 1285 | `fnd23_annfvalld1_pnii` | MATRIX | 0.690 | 其他 | 0 | — | — | — | UNTESTED | Acquisition of investment securities of a company (rather than the whole business unit) classified as Purchase of Invest |
| 1286 | `accrued_revenue` | MATRIX | 0.688 | 盈利与财务 | 0 | — | — | — | UNTESTED | accounts receivable value. |
| 1287 | `fnd23_annfv1a_snii` | MATRIX | 0.688 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Deconsolidation of subsidiaries if ownership interest in a subsidiary is reduced classified as Sale/Maturity of Investme |
| 1288 | `fnd23_blsm_rcaa` | MATRIX | 0.688 | 价量与波动 | 0 | — | — | — | UNTESTED | [Quarterly] Accounts Receivable - Trade, Net |
| 1289 | `fnd23_icsm_m_stnr` | MATRIX | 0.688 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Net Sales |
| 1290 | `fnd23_blsm_dlcl` | MATRIX | 0.688 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Current Portion of LT Debt/Capital Leases |
| 1291 | `rental_expense_total` | MATRIX | 0.688 | 其他 | 0 | — | — | — | UNTESTED | net sales. |
| 1292 | `long_term_collateralized_debt_2` | MATRIX | 0.688 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current Port. of LT Debt/Capital Leases. |
| 1293 | `fnd23_icsm_m_vnin` | MATRIX | 0.687 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Investment Income - Non-Operating |
| 1294 | `net_investment_income` | MATRIX | 0.686 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents income or losses, other than interest, from investment securities. Such income may include dividend income, g |
| 1295 | `fnd23_annfvalld1_agav` | MATRIX | 0.686 | 其他 | 0 | — | — | — | UNTESTED | Accumulated Goodwill Amortization, Supplemental |
| 1296 | `fnd23_annfv1a_graa` | MATRIX | 0.685 | 盈利与财务 | 0 | — | — | — | UNTESTED | gross accounts receivable from sales of trading assets such as inventories or from services provided. |
| 1297 | `fnd23_intfvalld1_pxtl` | MATRIX | 0.684 | 盈利与财务 | 0 | — | — | — | UNTESTED | Income Taxes Payable represents income taxes payable to the government, where such tax liability is already confirmed in |
| 1298 | `fnd23_intfvalld1_neis` | MATRIX | 0.683 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Net Non-Operating represents Interest Expense, Non-Operating, reduced by Interest Capitalized, Non-Ope |
| 1299 | `fnd23_annfvalld1_uatv` | MATRIX | 0.683 | 其他 | 0 | — | — | — | UNTESTED | Audit Fees |
| 1300 | `fnd23_intfvalld1_eiue` | MATRIX | 0.683 | 其他 | 0 | — | — | — | UNTESTED | Acquisition costs/expenses. |
| 1301 | `fnd23_intfvalld1_nein` | MATRIX | 0.683 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest expense on debt of non-financial service companies, including insurance companies. |
| 1302 | `fnd23_cf_m_nscf` | MATRIX | 0.682 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Common Stock, Net |
| 1303 | `financing_cash_senior_notes` | MATRIX | 0.682 | 宏观与行业 | 0 | — | — | — | UNTESTED | If the sale, issuance or repurchase of common stock is not separately delineated, then the total is classified as Common |
| 1304 | `fnd23_annfvalld1_eptv` | MATRIX | 0.682 | 其他 | 0 | — | — | — | UNTESTED | Total Pension Expense |
| 1305 | `fnd23_intfvm_snii` | MATRIX | 0.681 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Deconsolidation of subsidiaries if ownership interest in a subsidiary is reduced classified as Sale/Maturity of Investme |
| 1306 | `investment_in_subsidiaries` | MATRIX | 0.681 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Sale/Maturity of Investment |
| 1307 | `fnd23_icsm_m_neis` | MATRIX | 0.681 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Expense, Net Non-Operating |
| 1308 | `interest_expense_net_2` | MATRIX | 0.681 | 其他 | 0 | — | — | — | UNTESTED | Interest Expense, Net Non-Operating represents Interest Expense, Non-Operating, reduced by Interest Capitalized, Non-Ope |
| 1309 | `fnd23_icsm_m_nein` | MATRIX | 0.681 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Expense - Non-Operating |
| 1310 | `net_interest_expense` | MATRIX | 0.681 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents interest expense on debt of non-financial service companies, including insurance companies. |
| 1311 | `fnd23_annfv1a_rtla` | MATRIX | 0.680 | 其他 | 0 | — | — | — | UNTESTED | represents long-term notes receivable, excluding the current portion of the long-term receivables. It also represents al |
| 1312 | `fnd23_intfvm2_tius` | MATRIX | 0.680 | 其他 | 0 | — | — | — | UNTESTED | Non-Recurring Items, Total |
| 1313 | `fnd23_intfvalld1_iqea` | MATRIX | 0.680 | 盈利与财务 | 0 | — | — | — | UNTESTED | Represents long-term investment in securities (loans, bonds, and equity) of affiliate companies, where the affiliation m |
| 1314 | `fnd23_annfvalld1_rdlf` | MATRIX | 0.679 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash outflow on the repayment of long-term debt in a company. Long-term debt obligations may be repaid upon m |
| 1315 | `share_capital_ordinary` | MATRIX | 0.678 | 其他 | 0 | — | — | — | UNTESTED | Ordinary share capital reported for the annual period. |
| 1316 | `fnd23_annfv1a_uaie` | MATRIX | 0.674 | 盈利与财务 | 0 | — | — | — | UNTESTED | form of an unusual item related to the impairment of longlived assets, certain identifiable intangibles, and goodwill re |
| 1317 | `fnd23_cf_m_fcii` | MATRIX | 0.674 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Investing Cash Flow |
| 1318 | `investment_income_cash_flow` | MATRIX | 0.674 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash used for discontinued operations classified as Other Investing Cash Flow |
| 1319 | `fnd23_annfvmfm2_bpao` | MATRIX | 0.673 | 其他 | 0 | — | — | — | UNTESTED | represents changes in accounts payable during the period. An increase inaccounts payable has a positive impact on cash f |
| 1320 | `fnd23_annfv1a_bpao` | MATRIX | 0.673 | 其他 | 0 | — | — | — | UNTESTED | represents changes in accounts payable during the period. An increase inaccounts payable has a positive impact on cash f |
| 1321 | `fnd23_annfvalld1_gwga` | MATRIX | 0.673 | 其他 | 0 | — | — | — | UNTESTED | Goodwill, Gross |
| 1322 | `fnd23_icsm_m_prgs` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Gross Profit |
| 1323 | `gross_profit_2` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Profit represents a measure of a company’s operating performance. Gross Profit states the profits earned from a co |
| 1324 | `fnd23_annfvalld1_3dls` | MATRIX | 0.672 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long Term Debt Maturing in Year 3 |
| 1325 | `fnd23_annfvalld1_lbpl` | MATRIX | 0.672 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Pension Benefits - Underfunded |
| 1326 | `fnd23_annfv1a_bosi` | MATRIX | 0.672 | 其他 | 0 | — | — | — | UNTESTED | Deconsolidation of a subsidiary classified as Sale of Business. |
| 1327 | `fnd23_intfvm_rcao` | MATRIX | 0.672 | 其他 | 0 | — | — | — | UNTESTED | represents changes in accounts receivable during the period. An increase in accounts receivable has a negative impact on |
| 1328 | `fnd23_icsm_m_ppgs` | MATRIX | 0.671 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Gross Margin |
| 1329 | `other_assets_current_2` | MATRIX | 0.671 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Accounts Receivable |
| 1330 | `gross_profit_percentage` | MATRIX | 0.671 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross Margin  represents Gross Profit  divided by Revenue. Gross Margin is not available if either Gross Profit or Reven |
| 1331 | `fnd23_annfv1a_rtcv` | MATRIX | 0.670 | 其他 | 0 | — | — | — | UNTESTED | Current Tax – Total |
| 1332 | `fnd23_blsm_atda` | MATRIX | 0.670 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Deferred Income Tax - Long Term Asset |
| 1333 | `deferred_tax_assets` | MATRIX | 0.670 | 盈利与财务 | 0 | — | — | — | UNTESTED | deferred income taxes - long term. These are credits being applied to income taxes that will be paid in future years. |
| 1334 | `fnd23_cf_m_ndlf` | MATRIX | 0.669 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Long Term Debt, Net |
| 1335 | `financing_loan_drawdown_net` | MATRIX | 0.669 | 盈利与财务 | 0 | — | — | — | UNTESTED | If long-term debt issuances and reductions are not delineated separately, the total is classified as Long Term Debt, Net |
| 1336 | `fnd23_annfvalld1_agaa` | MATRIX | 0.669 | 其他 | 0 | — | — | — | UNTESTED | Accumulated Goodwill Amortization represents the accumulated amortization of goodwill acquired through mergers according |
| 1337 | `fnd23_blsm_aiav` | MATRIX | 0.668 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Accumulated Intangible Amort, Supplemental |
| 1338 | `fnd23_icsm_m_roce` | MATRIX | 0.668 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Cost of Revenue |
| 1339 | `fnd23_icsm_m_rocs` | MATRIX | 0.668 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Cost of Revenue, Total |
| 1340 | `cost_of_revenue_2` | MATRIX | 0.667 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue represents total costs that can be directly attributed to the goods and services produced/purchased and |
| 1341 | `cost_of_revenue_expense` | MATRIX | 0.667 | 盈利与财务 | 0 | — | — | — | UNTESTED | cost of revenue including labor coasts reported within cost of goods sold & that are not clearly labeled as cost of good |
| 1342 | `valuation_allowance_intangible_assets_2` | MATRIX | 0.667 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accumulated Intangible Amortization represents accumulated amortization against intangible fixed assets. |
| 1343 | `fnd23_intfvm_bosi` | MATRIX | 0.667 | 其他 | 0 | — | — | — | UNTESTED | Deconsolidation of a subsidiary classified as Sale of Business. |
| 1344 | `sale_of_businesses` | MATRIX | 0.667 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Sale of Business |
| 1345 | `fnd23_blsm_tmaa` | MATRIX | 0.667 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Accumulated Intangible Amortization |
| 1346 | `amortization_of_intangibles_2` | MATRIX | 0.667 | 其他 | 0 | — | — | — | UNTESTED | accumulated intangible amortization. |
| 1347 | `fnd23_intfvm_uaie` | MATRIX | 0.667 | 盈利与财务 | 0 | — | — | — | UNTESTED | form of an unusual item related to the impairment of longlived assets, certain identifiable intangibles, and goodwill re |
| 1348 | `income_attributable_to_unitholders` | MATRIX | 0.667 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Impairment-Assets Held for Use |
| 1349 | `fnd23_blsm_gnia` | MATRIX | 0.666 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Intangibles - Gross |
| 1350 | `interest_and_dividends_receivable` | MATRIX | 0.666 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the gross purchase value of assets that lack physical existence, before being reduced by accumulated impairm |
| 1351 | `fnd23_annfvalld1_4dls` | MATRIX | 0.665 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt maturing in year 4 |
| 1352 | `fnd23_annfvalld1_54dls` | MATRIX | 0.665 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standardized Long-Term Debt Maturing in Years 4 and 5 |
| 1353 | `fnd23_intfvalld1_acoa` | MATRIX | 0.665 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current assets. |
| 1354 | `fnd23_annfv1a_cdav` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | Deferred Revenue - Current |
| 1355 | `fnd23_icsm_m_eoos` | MATRIX | 0.662 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other Operating Expenses, Total |
| 1356 | `other_operating_expense` | MATRIX | 0.662 | 其他 | 0 | — | — | — | UNTESTED | Other Operating Expenses, Total. |
| 1357 | `fnd23_blsm_lcol` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Current Liabilities |
| 1358 | `long_term_operating_lease_liabilities` | MATRIX | 0.662 | 盈利与财务 | 0 | — | — | — | UNTESTED | other current liabilities. |
| 1359 | `fnd23_annfv1a_adpa` | MATRIX | 0.660 | 其他 | 0 | — | — | — | UNTESTED | represents provisions established for doubtful accounts receivable. Provision for doubtful accounts is usually establish |
| 1360 | `employee` | MATRIX | 0.660 | 其他 | 0 | — | — | — | UNTESTED | Full-Time Employees |
| 1361 | `fnd23_intfvm2_lbpl` | MATRIX | 0.659 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Pension Benefits - Underfunded |
| 1362 | `fnd23_intfvalld1_eiuo` | MATRIX | 0.659 | 盈利与财务 | 0 | — | — | — | UNTESTED | is applicable only if Net Income/Starting Line [ONET] is income after gains/losses from unusual activities. Because the |
| 1363 | `fnd23_intfvalld1_saoa` | MATRIX | 0.659 | 盈利与财务 | 0 | — | — | — | UNTESTED | Non-operational fixed assets that are long-term. |
| 1364 | `fnd23_intfvm2_iwgv` | MATRIX | 0.658 | 其他 | 0 | — | — | — | UNTESTED | Goodwill - Net |
| 1365 | `fnd23_icsm_m_tnos` | MATRIX | 0.657 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other, Net |
| 1366 | `fnd23_icsm_m_tnon` | MATRIX | 0.657 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Other Non-Operating Income (Expense) |
| 1367 | `other_nonoperating_income` | MATRIX | 0.657 | 盈利与财务 | 0 | — | — | — | UNTESTED | other net income. |
| 1368 | `non_operating_income_total_2` | MATRIX | 0.657 | 其他 | 0 | — | — | — | UNTESTED | represents any non-operating income or expense item that a company reports before income taxes |
| 1369 | `fnd23_icsm_m_agse` | MATRIX | 0.656 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Selling/General/Administrative Expense |
| 1370 | `environmental_social_governance_expense` | MATRIX | 0.656 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Selling/General/Administrative Expense. |
| 1371 | `fnd23_annfvalld1_saoa` | MATRIX | 0.655 | 盈利与财务 | 0 | — | — | — | UNTESTED | Non-operational fixed assets that are long-term. |
| 1372 | `fnd23_intfvm_itsa` | MATRIX | 0.655 | 其他 | 0 | — | — | — | UNTESTED | Short-Term Investments |
| 1373 | `short_term_investments_8` | MATRIX | 0.655 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Short Term Investments |
| 1374 | `fnd23_intfvm_ixts` | MATRIX | 0.654 | 其他 | 0 | — | — | — | UNTESTED | Total Extraordinary Items |
| 1375 | `short_term_tax_incentives_2` | MATRIX | 0.654 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Total Extraordinary Items |
| 1376 | `fnd23_cf_m_afsi` | MATRIX | 0.653 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Sale of Fixed Assets |
| 1377 | `investment_securities_financial_assets` | MATRIX | 0.653 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sale of assets to be leased out under operating lease contracts. |
| 1378 | `fnd23_icsm_m_eius` | MATRIX | 0.653 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Unusual Expense (Income) |
| 1379 | `unusual_income_expense` | MATRIX | 0.653 | 其他 | 0 | — | — | — | UNTESTED | Unusual Expense (Income). |
| 1380 | `fnd23_intfvalld1_aiev` | MATRIX | 0.653 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity in affiliates, supplemental represents the total share of earnings/losses, net of taxes, that the company is enti |
| 1381 | `fnd23_cf_m_pics` | MATRIX | 0.651 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Cash Interest Paid |
| 1382 | `short_term_cash_investment_proceeds` | MATRIX | 0.651 | 其他 | 0 | — | — | — | UNTESTED | cash interest paid represents interest paid in cash during the period Cash Interest. |
| 1383 | `fnd23_cf_m_pdcf` | MATRIX | 0.651 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Cash Dividends Paid |
| 1384 | `financing_cash_dividend_paid` | MATRIX | 0.651 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total Cash Dividends Paid. |
| 1385 | `rad` | MATRIX | 0.650 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Research and Development |
| 1386 | `fnd23_intfvalld1_cisf` | MATRIX | 0.648 | 持仓与资金流 | 0 | — | — | — | UNTESTED | represents cash inflow from the issuance of common stock. It also includes cash inflow from the sale of treasury shares. |
| 1387 | `fnd23_cf_m_eiuo` | MATRIX | 0.647 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Unusual Items |
| 1388 | `fnd23_annfv1a_nnin` | MATRIX | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Interest expense that is reduced by interest income. |
| 1389 | `other_unusual_income_expense_2` | MATRIX | 0.647 | 盈利与财务 | 0 | — | — | — | UNTESTED | is applicable only if Net Income/Starting Line [ONET] is income after gains/losses from unusual activities. Because the |
| 1390 | `fnd23_blsm_cema` | MATRIX | 0.647 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Machinery/Equipment - Gross |
| 1391 | `marketable_equity_securities` | MATRIX | 0.647 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the acquisition cost of machinery and other equipment (including delivery equipment, office equipment, machin |
| 1392 | `fnd23_intfvm_ttiv` | MATRIX | 0.646 | 其他 | 0 | — | — | — | UNTESTED | Income Tax – Total reflects the sum of Domestic Tax - Other, Foreign Tax – Other, Local Tax – Other and Other Tax. |
| 1393 | `fnd23_intfvalld1_etoq` | MATRIX | 0.646 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents any residual value of shareholders' equity that belongs to shareholders. |
| 1394 | `valuation_investment_total` | MATRIX | 0.646 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Income Tax - Total |
| 1395 | `fnd23_annfvalld1_lltq` | MATRIX | 0.645 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Total Equity and Equity Non-Controlling Interests. |
| 1396 | `fnd23_annfvalld1_idlf` | MATRIX | 0.645 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash inflow on the issuance of long-term debt instruments in a company. Long-term debt may include long-term |
| 1397 | `fnd23_blsm_cipq` | MATRIX | 0.645 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Additional Paid-In Capital |
| 1398 | `policyholder_interest_crediting` | MATRIX | 0.645 | 价量与波动 | 0 | — | — | — | UNTESTED | represents capital contributed by shareholders in excess of par value of common stock in return for shares issued to the |
| 1399 | `fnd23_intfvalld1_lltq` | MATRIX | 0.645 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the sum of Total Equity and Equity Non-Controlling Interests. |
| 1400 | `fnd23_blsm_iwga` | MATRIX | 0.644 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Goodwill, Net |
| 1401 | `goodwill_intangible_assets` | MATRIX | 0.644 | 盈利与财务 | 0 | — | — | — | UNTESTED | net goodwill. |
| 1402 | `fnd23_annfvalld1_bpao` | MATRIX | 0.643 | 其他 | 0 | — | — | — | UNTESTED | Represents changes in accounts payable during the period. An increase in accounts payable has a positive impact on cash |
| 1403 | `fnd23_intfvalld1_qabi` | MATRIX | 0.642 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents cash outflow for acquiring new businesses. Reporting the cash flow for acquiring new businesses is not consis |
| 1404 | `fnd23_annfvalld1_5dls` | MATRIX | 0.642 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standardized Long Term Debt Maturing in Year 5 |
| 1405 | `fnd23_annfv1a_bloo` | MATRIX | 0.641 | 盈利与财务 | 0 | — | — | — | UNTESTED | other liabilities |
| 1406 | `fnd23_annfvmfm2_bloo` | MATRIX | 0.641 | 盈利与财务 | 0 | — | — | — | UNTESTED | other liabilities |
| 1407 | `depre` | MATRIX | 0.640 | 盈利与财务 | 0 | — | — | — | UNTESTED | Depreciation of fixed assets reported outside of the cost of goods and services sold. |
| 1408 | `depreciation_expense_3` | MATRIX | 0.640 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Depreciation/Amortization |
| 1409 | `fnd23_description` | VECTOR | 0.640 | 其他 | 0 | — | — | — | UNTESTED | description index |
| 1410 | `fnd23_descriptionfull` | VECTOR | 0.640 | 其他 | 0 | — | — | — | UNTESTED | full description index |
| 1411 | `fnd23_fieldfull` | VECTOR | 0.640 | 其他 | 0 | — | — | — | UNTESTED | Full field which is string value's starting index in fieldfull_str |
| 1412 | `fnd23_frontpage` | VECTOR | 0.640 | 其他 | 0 | — | — | — | UNTESTED | Indicates whether a given development is coming from a front page story |
| 1413 | `fnd23_headline` | VECTOR | 0.640 | 情绪与新闻 | 0 | — | — | — | UNTESTED | story headline index |
| 1414 | `fnd23_headlinefull` | VECTOR | 0.640 | 情绪与新闻 | 0 | — | — | — | UNTESTED | full story headline index |
| 1415 | `fnd23_intfvm_pede` | MATRIX | 0.640 | 盈利与财务 | 0 | — | — | — | UNTESTED | Depreciation of fixed assets reported outside of the cost of goods and services sold. |
| 1416 | `fnd23_significance` | VECTOR | 0.640 | 其他 | 0 | — | — | — | UNTESTED | Indicates the level of importance for the given development (1 = High, 2 = Medium, 3 = Low) |
| 1417 | `fnd23_topic1` | VECTOR | 0.640 | 元数据与非信号 | 0 | — | — | — | UNTESTED | parent topic code. |
| 1418 | `fnd23_topic2` | VECTOR | 0.640 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | second-tier topic mapped to parent topic. |
| 1419 | `fnd23_topic3` | VECTOR | 0.640 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | third tier topic mapped to parent topic. |
| 1420 | `fnd23_annfv1a_crrf` | MATRIX | 0.639 | 盈利与财务 | 0 | — | — | — | UNTESTED | Treasury Stock, when reported in the financing section of the cash flow statement, is henceforth classified as Sale/Issu |
| 1421 | `fnd23_annfvmfm2_ltio` | MATRIX | 0.639 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents changes in inventories during the period. An increase in inventories has a negative impact on cash flow from |
| 1422 | `fnd23_annfv1a_ltio` | MATRIX | 0.639 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents changes in inventories during the period. An increase in inventories has a negative impact on cash flow from |
| 1423 | `fnd23_intfvm_crrf` | MATRIX | 0.639 | 盈利与财务 | 0 | — | — | — | UNTESTED | Treasury Stock, when reported in the financing section of the cash flow statement, is henceforth classified as Sale/Issu |
| 1424 | `repurchase_of_common_stock` | MATRIX | 0.639 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Repurchase/Retirement of Common |
| 1425 | `fnd23_intfv_value` | VECTOR | 0.638 | 其他 | 0 | — | — | — | UNTESTED | value. |
| 1426 | `fnd23_annfv1a_vacl` | MATRIX | 0.638 | 其他 | 0 | — | — | — | UNTESTED | Advances/deposits from customers for the products to be sold or services to be rendered classified as Customer Advances. |
| 1427 | `extraordinary_income_disposal_operations` | MATRIX | 0.636 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Discontinued Operations |
| 1428 | `fnd23_intfvm_odix` | MATRIX | 0.636 | 其他 | 0 | — | — | — | UNTESTED | Discontinued Operations. |
| 1429 | `fnd23_intfvm_rale` | MATRIX | 0.636 | 其他 | 0 | — | — | — | UNTESTED | Labor costs reported outside of the cost of goods sold, or not clearly labeled as part of the cost of goods sold, for bu |
| 1430 | `legal_and_regulatory_expenses` | MATRIX | 0.636 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Labor & Related Expense |
| 1431 | `fnd23_intfvm_ctcv` | MATRIX | 0.636 | 其他 | 0 | — | — | — | UNTESTED | Current Tax – Total reflects the sum of Current Tax – Domestic, Current Tax – Foreign, Current Tax – Local, Current Tax |
| 1432 | `valuation_credit_tax_carryforward` | MATRIX | 0.636 | 风险与质量 | 0 | — | — | — | UNTESTED | [Quarterly] Current Tax - Total |
| 1433 | `fnd23_blsm_ltll` | MATRIX | 0.635 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Long Term Liabilities |
| 1434 | `long_term_loans_3` | MATRIX | 0.635 | 其他 | 0 | — | — | — | UNTESTED | Long-term obligations from right-of-use contracts related to operating leases. |
| 1435 | `fnd23_fotv` | MATRIX | 0.634 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] All Other Fees Paid to Auditor |
| 1436 | `other_financing_expense` | MATRIX | 0.634 | 其他 | 0 | — | — | — | UNTESTED | All Other Fees Paid to Auditor |
| 1437 | `fnd23_intfvm_nnis` | MATRIX | 0.633 | 其他 | 0 | — | — | — | UNTESTED | Net - Net Operating, Total |
| 1438 | `net_noninterest_income_value` | MATRIX | 0.633 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest Expense (Income), Net - Operating, Total |
| 1439 | `fnd23_annfvalld1_ltio` | MATRIX | 0.631 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents changes in inventories during the period. An increase in inventories has a negative impact on cash flow from |
| 1440 | `fnd23_intfvalld1_imav` | MATRIX | 0.630 | 其他 | 0 | — | — | — | UNTESTED | Amortization. |
| 1441 | `fnd23_annfvalld1_bpol` | MATRIX | 0.630 | 其他 | 0 | — | — | — | UNTESTED | Other Payables |
| 1442 | `fnd23_intfvm2_ctdv` | MATRIX | 0.627 | 其他 | 0 | — | — | — | UNTESTED | Deferred Tax – Total |
| 1443 | `fnd23_intfvm_inas` | MATRIX | 0.627 | 盈利与财务 | 0 | — | — | — | UNTESTED | total adjustments to net income represents sum of preferred dividend, general partners distributions, misc. earnings adj |
| 1444 | `amortization_intangible_total` | MATRIX | 0.627 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Total Adjustments to Net Income |
| 1445 | `fnd23_annfvalld1_aiev` | MATRIX | 0.627 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity in affiliates, supplemental represents the total share of earnings/losses, net of taxes, that the company is enti |
| 1446 | `fnd23_blsm_acos` | MATRIX | 0.626 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Current Assets, Total |
| 1447 | `other_current_assets_4` | MATRIX | 0.625 | 盈利与财务 | 0 | — | — | — | UNTESTED | Other Current Assets, Total. |
| 1448 | `fnd23_intfvalld1_niin` | MATRIX | 0.625 | 宏观与行业 | 0 | — | — | — | UNTESTED | represents non-operating interest income, which is generated from non-operating investment securities such as certificat |
| 1449 | `fnd23_annfvalld1_amav` | MATRIX | 0.625 | 其他 | 0 | — | — | — | UNTESTED | Amortization of Acquisition Costs, Supplemental |
| 1450 | `fnd23_annfvalld1_eiue` | MATRIX | 0.625 | 其他 | 0 | — | — | — | UNTESTED | Acquisition costs/expenses. |
| 1451 | `fnd23_intfvalld1_amav` | MATRIX | 0.625 | 其他 | 0 | — | — | — | UNTESTED | Amortization of Acquisition Costs, Supplemental |
| 1452 | `fnd23_intfvm_laoo` | MATRIX | 0.621 | 盈利与财务 | 0 | — | — | — | UNTESTED | represents the changes in the combined sum of assets and liabilities when a company reports these totals as a single lin |
| 1453 | `fnd23_icsm_m_niin` | MATRIX | 0.621 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest/Investment Income |
| 1454 | `net_income_including_interest` | MATRIX | 0.621 | 宏观与行业 | 0 | — | — | — | UNTESTED | represents non-operating interest income, which is generated from non-operating investment securities such as certificat |
| 1455 | `other_assets_long_term` | MATRIX | 0.621 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Other Assets & Liabilities, Net |
| 1456 | `fnd23_intfvalld1_itsa` | MATRIX | 0.620 | 其他 | 0 | — | — | — | UNTESTED | Short-Term Investments |
| 1457 | `fnd23_annfvalld1_pede` | MATRIX | 0.619 | 盈利与财务 | 0 | — | — | — | UNTESTED | Depreciation of fixed assets reported outside of the cost of goods and services sold. |
| 1458 | `fnd23_annfv1a_rale` | MATRIX | 0.618 | 其他 | 0 | — | — | — | UNTESTED | Labor costs reported outside of the cost of goods sold, or not clearly labeled as part of the cost of goods sold, for bu |
| 1459 | `other_accumulated_reserves` | MATRIX | 0.618 | 其他 | 0 | — | — | — | UNTESTED | Other accumulated reserves reported for the annual period. |
| 1460 | `fnd23_intfvalld1_nppv` | MATRIX | 0.617 | 其他 | 0 | — | — | — | UNTESTED | Other Property/Plant/Equipment - Net |
| 1461 | `fnd23_blsm_itla` | MATRIX | 0.613 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Long-Term Investments - Other |
| 1462 | `long_term_investments` | MATRIX | 0.613 | 其他 | 0 | — | — | — | UNTESTED | represents long-term investments with maturities of one year or longer. |
| 1463 | `fnd23_intfvalld1_tnoe` | MATRIX | 0.612 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Income from external grants received to cover research and development expenses. |
| 1464 | `fnd23_intfvalld1_croa` | MATRIX | 0.612 | 其他 | 0 | — | — | — | UNTESTED | other receivables. |
| 1465 | `fnd23_annfvalld1_rtdv` | MATRIX | 0.611 | 其他 | 0 | — | — | — | UNTESTED | Deferred Tax - Total |
| 1466 | `fnd23_annfvalld1_tnoe` | MATRIX | 0.608 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Income from external grants received to cover research and development expenses. |
| 1467 | `fnd23_blsm_yppa` | MATRIX | 0.605 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Prepaid Expenses |
| 1468 | `prepaid_expenses_2` | MATRIX | 0.605 | 其他 | 0 | — | — | — | UNTESTED | prepaid expenses. |
| 1469 | `fnd23_intfvm_oiis` | MATRIX | 0.605 | 其他 | 0 | — | — | — | UNTESTED | Interest/Investment Income – Operating |
| 1470 | `insurance_operating_income_value` | MATRIX | 0.605 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Interest/Investment Income - Operating |
| 1471 | `fnd23_intfvm_atcq` | MATRIX | 0.604 | 其他 | 0 | — | — | — | UNTESTED | represents translation gains (losses) on financial statements of foreign subsidiaries. Such adjustments may be required |
| 1472 | `current_total_assets` | MATRIX | 0.604 | 盈利与财务 | 0 | — | — | — | UNTESTED | [Quarterly] Cumulative Translation Adjustment |
| 1473 | `fnd23_intfvm_vnie` | MATRIX | 0.603 | 其他 | 0 | — | — | — | UNTESTED | investing income from operating section. |
| 1474 | `fnd23_intfvm2_eiuv` | MATRIX | 0.603 | 其他 | 0 | — | — | — | UNTESTED | Other Unusual Expense (Income), Supplemental |
| 1475 | `investment_income_4` | MATRIX | 0.603 | 其他 | 0 | — | — | — | UNTESTED | [Quarterly] Investment Income - Operating |
| 1476 | `fnd23_annfvalld1_fotv` | MATRIX | 0.602 | 其他 | 0 | — | — | — | UNTESTED | All Other Fees Paid to Auditor |
| 1477 | `fnd23_annfvalld1_snii` | MATRIX | 0.602 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Deconsolidation of subsidiaries if ownership interest in a subsidiary is reduced classified as Sale/Maturity of Investme |
| 1478 | `fnd23_blsm_lotv` | MATRIX | 0.599 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Operating Leases, Supplemental |
| 1479 | `fnd23_intfvm_bpao` | MATRIX | 0.599 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in accounts payable during the period. An increase inaccounts payable has a positive impact on cash f |
| 1480 | `valuation_allowance_total_loans` | MATRIX | 0.599 | 其他 | 0 | — | — | — | UNUSABLE | Total Operating Leases, Supplemental reflects the sum of Operating Leases Maturing within 1 through 10 Years, Operating |
| 1481 | `accounts_payable_balance_2` | MATRIX | 0.599 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Accounts Payable |
| 1482 | `fnd23_annfv1a_qaii` | MATRIX | 0.598 | 其他 | 0 | — | — | — | UNUSABLE | Franchise acquired (classified as Purchase/Acquisition of Intangibles). |
| 1483 | `depreciation_and_amortization_expense_2` | MATRIX | 0.597 | 其他 | 0 | — | — | — | UNUSABLE | Depreciation/amortization represents sum of depreciation, amortization of intangibles and amortization of acquisition co |
| 1484 | `fnd23_icsm_m_rpds` | MATRIX | 0.597 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] epreciation/Amortization |
| 1485 | `fnd23_intfvm_aemc` | MATRIX | 0.597 | 盈利与财务 | 0 | — | — | — | UNUSABLE | miscellaneous earnings adjustment. |
| 1486 | `marketable_equity_assets` | MATRIX | 0.596 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Miscellaneous Earnings Adjustment |
| 1487 | `fnd23_blsm_1los` | MATRIX | 0.596 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 1 |
| 1488 | `other_long_term_liabilities_1` | MATRIX | 0.596 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Lease Payments Due in Year 1 |
| 1489 | `minority_interest_value` | MATRIX | 0.596 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Portion of net assets or earnings attributable to minority shareholders for the period. |
| 1490 | `fnd23_cf_m_rcao` | MATRIX | 0.595 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Accounts Receivable |
| 1491 | `fnd23_icsm_m_eptv` | MATRIX | 0.595 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Pension Expense |
| 1492 | `total_premiums_earned` | MATRIX | 0.595 | 其他 | 0 | — | — | — | UNUSABLE | Total Pension Expense |
| 1493 | `fnd23_blsm_2los` | MATRIX | 0.594 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 2 |
| 1494 | `other_assets_cash_receipts` | MATRIX | 0.594 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents changes in accounts receivable during the period. An increase in accounts receivable has a negative impact on |
| 1495 | `other_long_term_liabilities_2` | MATRIX | 0.594 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Lease Payments Due in Year 2 |
| 1496 | `fnd23_intfvalld1_rdlf` | MATRIX | 0.593 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents cash outflow on the repayment of long-term debt in a company. Long-term debt obligations may be repaid upon m |
| 1497 | `fnd23_intfvalld1_pnii` | MATRIX | 0.593 | 其他 | 0 | — | — | — | UNUSABLE | Acquisition of investment securities of a company (rather than the whole business unit) classified as Purchase of Invest |
| 1498 | `fnd23_icsm_m_pxrv` | MATRIX | 0.591 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Rental Expense, Supplemental |
| 1499 | `foreign_exchange_gain_loss` | MATRIX | 0.591 | 其他 | 0 | — | — | — | UNUSABLE | Rental Expense, Supplemental represents the total value of rental expenses paid for offices, factories, machinery and eq |
| 1500 | `fnd23_blsm_acoa` | MATRIX | 0.589 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Current Assets |
| 1501 | `fnd23_blsm_3los` | MATRIX | 0.589 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 3 |
| 1502 | `other_current_assets_additional` | MATRIX | 0.589 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other current assets. |
| 1503 | `other_long_term_liabilities_3` | MATRIX | 0.589 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Year 3. |
| 1504 | `fnd23_cf_m_rdlf` | MATRIX | 0.587 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Reduction |
| 1505 | `financing_loan_drawdown_receipts` | MATRIX | 0.587 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents cash outflow on the repayment of long-term debt in a company. Long-term debt obligations may be repaid upon m |
| 1506 | `fnd23_intfvm_qaii` | MATRIX | 0.586 | 其他 | 0 | — | — | — | UNUSABLE | Franchise acquired (classified as Purchase/Acquisition of Intangibles). |
| 1507 | `acquisition_of_intangibles` | MATRIX | 0.586 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Purchase/Acquisition of Intangibles |
| 1508 | `fnd23_annfv1a_alge` | MATRIX | 0.586 | 盈利与财务 | 0 | — | — | — | UNUSABLE | loss/gain on sale of assets listed in the operating section. |
| 1509 | `fnd23_blsm_4los` | MATRIX | 0.585 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 4 |
| 1510 | `other_long_term_liabilities_4` | MATRIX | 0.585 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Year 4. |
| 1511 | `fnd23_intfvm_rtla` | MATRIX | 0.584 | 其他 | 0 | — | — | — | UNUSABLE | represents long-term notes receivable, excluding the current portion of the long-term receivables. It also represents al |
| 1512 | `loans_to_related_parties` | MATRIX | 0.584 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Note Receivable - Long Term |
| 1513 | `fnd23_intfvm_xeal` | MATRIX | 0.584 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents operational expenses accrued, but not yet paid. As current liabilities, such expenses are expected to be paid |
| 1514 | `accrued_expenses_3` | MATRIX | 0.584 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Accrued Expenses |
| 1515 | `fnd23_annfv1a_imae` | MATRIX | 0.584 | 盈利与财务 | 0 | — | — | — | UNUSABLE | amortization of intangible assets reported outside the cost of goods and services sold |
| 1516 | `fnd23_annfv1a_laoo` | MATRIX | 0.581 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents the changes in the combined sum of assets and liabilities when a company reports these totals as a single lin |
| 1517 | `fnd23_blsm_ltia` | MATRIX | 0.580 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Inventory |
| 1518 | `income_taxes_receivable` | MATRIX | 0.580 | 其他 | 0 | — | — | — | UNUSABLE | total inventory. |
| 1519 | `fnd23_annfvalld1_opts` | MATRIX | 0.580 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Obligations |
| 1520 | `fnd23_annfvalld1_ssfv` | MATRIX | 0.579 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total Funded Status |
| 1521 | `fnd23_blsm_5los` | MATRIX | 0.579 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 5 |
| 1522 | `other_long_term_liabilities_5` | MATRIX | 0.579 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Year 5. |
| 1523 | `fnd23_annfv1a_nnis` | MATRIX | 0.579 | 其他 | 0 | — | — | — | UNUSABLE | Net - Net Operating, Total |
| 1524 | `fnd23_intfvalld1_pede` | MATRIX | 0.579 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation of fixed assets reported outside of the cost of goods and services sold. |
| 1525 | `fnd23_intfvm_imae` | MATRIX | 0.578 | 盈利与财务 | 0 | — | — | — | UNUSABLE | amortization of intangible assets reported outside the cost of goods and services sold |
| 1526 | `amortization_intangible_assets_2` | MATRIX | 0.578 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Amortization of Intangibles |
| 1527 | `fnd23_intfvalld1_ralv` | MATRIX | 0.578 | 其他 | 0 | — | — | — | UNUSABLE | Total labor costs: Labor & Related Expense, Supplemental |
| 1528 | `fnd23_intfvm2_amav` | MATRIX | 0.576 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of Acquisition Costs, Supplemental |
| 1529 | `fnd23_intfvm_alge` | MATRIX | 0.574 | 盈利与财务 | 0 | — | — | — | UNUSABLE | loss/gain on sale of assets listed in the operating section. |
| 1530 | `gain_loss_asset_sales` | MATRIX | 0.574 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Loss(Gain) on Sale of Assets - Operating |
| 1531 | `fnd23_intfvm_sere` | MATRIX | 0.571 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Restructuring Charge is an unusual or non-recurring item related to a significant rearrangement of a company’s assets an |
| 1532 | `restructuring_expense` | MATRIX | 0.571 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Restructuring Charge |
| 1533 | `fnd23_blsm_dltv` | MATRIX | 0.570 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Long Term Debt, Supplemental |
| 1534 | `valuation_allowance_trade_loans` | MATRIX | 0.570 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Long Term Debt, Supplemental reflects the sum of Long Term Debt Maturing within 1 through 10 Years and Long Term |
| 1535 | `fnd23_intfvm2_rtdv` | MATRIX | 0.570 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax – Total |
| 1536 | `fnd23_intfvm_bloo` | MATRIX | 0.570 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other liabilities |
| 1537 | `other_liabilities_long_term` | MATRIX | 0.570 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Liabilities |
| 1538 | `fnd23_blsm_1dls` | MATRIX | 0.569 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Maturing within 1 Year |
| 1539 | `short_term_loans_1` | MATRIX | 0.569 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long Term Debt Maturing within 1 Year |
| 1540 | `fnd23_intfvm_nvii` | MATRIX | 0.567 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in investments in securities and other investments. Investment, Net is utilized when a company does n |
| 1541 | `investment_in_joint_ventures` | MATRIX | 0.567 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Investment, Net |
| 1542 | `fnd23_intfvm_ltio` | MATRIX | 0.567 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents changes in inventories during the period. An increase in inventories has a negative impact on cash flow from |
| 1543 | `fnd23_intfvalld1_tniv` | MATRIX | 0.567 | 其他 | 0 | — | — | — | UNUSABLE | Intangibles - Net |
| 1544 | `income_tax_liabilities_2` | MATRIX | 0.567 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories |
| 1545 | `fnd23_annfv1a_gfia` | MATRIX | 0.563 | 其他 | 0 | — | — | — | UNUSABLE | represents inventories of unsold finished goods on hand. These goods may have been produced internally or purchased for |
| 1546 | `fnd23_annfvalld1_cdav` | MATRIX | 0.561 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred Revenue - Current |
| 1547 | `fnd23_intfvalld1_rcao` | MATRIX | 0.560 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in accounts receivable during the period. An increase in accounts receivable has a negative impact on |
| 1548 | `fnd23_annfv1a_nvii` | MATRIX | 0.560 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in investments in securities and other investments. Investment, Net is utilized when a company does n |
| 1549 | `fnd23_annfvalld1_gfia` | MATRIX | 0.560 | 其他 | 0 | — | — | — | UNUSABLE | represents inventories of unsold finished goods on hand. These goods may have been produced internally or purchased for |
| 1550 | `fnd23_annfvalld1_etoq` | MATRIX | 0.558 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents any residual value of shareholders' equity that belongs to shareholders. |
| 1551 | `fnd23_annfvalld1_mria` | MATRIX | 0.558 | 其他 | 0 | — | — | — | UNUSABLE | annual inventories - raw material. |
| 1552 | `fnd23_annfvalld1_ppdv` | MATRIX | 0.557 | 其他 | 0 | — | — | — | UNUSABLE | Domestic Pension Plan Expense |
| 1553 | `fnd23_annfvalld1_bloo` | MATRIX | 0.557 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other liabilities |
| 1554 | `fnd23_intfvm_rtcv` | MATRIX | 0.557 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax – Total |
| 1555 | `valuation_credit_tax_reserve` | MATRIX | 0.557 | 风险与质量 | 0 | — | — | — | UNUSABLE | [Quarterly] Current Tax - Total |
| 1556 | `fnd23_icsm_m_nimv` | MATRIX | 0.556 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Minority Interest, Supplemental |
| 1557 | `minority_interest_income` | MATRIX | 0.556 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Minority Interest, Supplemental represents the share of earnings/losses in subsidiaries that belongs to shareholders ot |
| 1558 | `fnd23_icsm_m_nimc` | MATRIX | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Minority Interest |
| 1559 | `minority_interest_expense` | MATRIX | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents the share of earnings/losses in subsidiaries that belongs to shareholders other than the parent company when |
| 1560 | `fnd23_annfvalld1_cpoa` | MATRIX | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Other Properties/Plant/Equipment - Gross |
| 1561 | `long_term_capital_commitments` | MATRIX | 0.553 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Current Portion of Long-Term Capital Leases, Supplemental |
| 1562 | `valuation_allowance_loans_customers` | MATRIX | 0.553 | 其他 | 0 | — | — | — | UNUSABLE | Current Portion of Long-Term Capital Leases,Supplemental |
| 1563 | `fnd23_intfvalld1_idlf` | MATRIX | 0.552 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents cash inflow on the issuance of long-term debt instruments in a company. Long-term debt may include long-term |
| 1564 | `fnd23_intfvm2_dtdv` | MATRIX | 0.549 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax – Domestic |
| 1565 | `fnd23_cf_m_cisf` | MATRIX | 0.548 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Sale/Issuance of Common |
| 1566 | `financing_section_investment_cashflow` | MATRIX | 0.548 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | represents cash inflow from the issuance of common stock. It also includes cash inflow from the sale of treasury shares. |
| 1567 | `fnd23_intfvalld1_lbpl` | MATRIX | 0.547 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Pension Benefits - Underfunded |
| 1568 | `fnd23_intfvm2_olcl` | MATRIX | 0.547 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Obligations |
| 1569 | `fnd23_intfvalld1_rale` | MATRIX | 0.547 | 其他 | 0 | — | — | — | UNUSABLE | Labor costs reported outside of the cost of goods sold, or not clearly labeled as part of the cost of goods sold, for bu |
| 1570 | `fnd23_annfv1a_mria` | MATRIX | 0.546 | 其他 | 0 | — | — | — | UNUSABLE | annual inventories - raw material. |
| 1571 | `fnd23_annfvalld1_dpav` | MATRIX | 0.545 | 其他 | 0 | — | — | — | UNUSABLE | Pension Obligation - Domestic |
| 1572 | `fnd23_annfv1a_oiis` | MATRIX | 0.544 | 其他 | 0 | — | — | — | UNUSABLE | Interest/Investment Income – Operating |
| 1573 | `fnd23_annfvalld1_dppv` | MATRIX | 0.544 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funded Status - Domestic |
| 1574 | `other_appropriations_balance` | MATRIX | 0.544 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Other appropriations balance reported for the annual period. |
| 1575 | `accounts_receivable_gross_2` | MATRIX | 0.543 | 价量与波动 | 0 | — | — | — | UNUSABLE | [Quarterly] Accounts Receivable - Trade, Gross |
| 1576 | `accounts_receivable_gross_3` | MATRIX | 0.543 | 盈利与财务 | 0 | — | — | — | UNUSABLE | gross accounts receivable from sales of trading assets such as inventories or from services provided. |
| 1577 | `fnd23_annfv1a_vnie` | MATRIX | 0.541 | 其他 | 0 | — | — | — | UNUSABLE | investing income from operating section. |
| 1578 | `fnd23_annfv1a_aieo` | MATRIX | 0.540 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents a reversal of non-cash earnings/losses from investments under the Equity Method. For such investments, undist |
| 1579 | `fnd23_annfvalld1_bosi` | MATRIX | 0.540 | 其他 | 0 | — | — | — | UNUSABLE | Deconsolidation of a subsidiary classified as Sale of Business. |
| 1580 | `fnd23_annfvalld1_graa` | MATRIX | 0.540 | 盈利与财务 | 0 | — | — | — | UNUSABLE | gross accounts receivable from sales of trading assets such as inventories or from services provided. |
| 1581 | `fnd23_spd` | MATRIX | 0.540 | 盈利与财务 | 0 | — | — | — | UNUSABLE | dividend per share |
| 1582 | `fnd23_annfvalld1_rale` | MATRIX | 0.539 | 其他 | 0 | — | — | — | UNUSABLE | Labor costs reported outside of the cost of goods sold, or not clearly labeled as part of the cost of goods sold, for bu |
| 1583 | `fnd23_blsm_saoa` | MATRIX | 0.538 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Long Term Assets |
| 1584 | `other_assets_2` | MATRIX | 0.538 | 盈利与财务 | 0 | — | — | — | UNUSABLE | non operational fixed assets that are long term. |
| 1585 | `fnd23_annfvalld1_adpa` | MATRIX | 0.538 | 其他 | 0 | — | — | — | UNUSABLE | represents provisions established for doubtful accounts receivable. Provision for doubtful accounts is usually establish |
| 1586 | `fnd23_annfv1a_cstq` | MATRIX | 0.538 | 其他 | 0 | — | — | — | UNUSABLE | represents the value of common stock owned by the issuing company or its consolidated subsidiaries. Treasury stock is re |
| 1587 | `fnd23_blsm_2dls` | MATRIX | 0.538 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Maturing in Year 2 |
| 1588 | `short_term_loans_2_2` | MATRIX | 0.538 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Year 8 |
| 1589 | `fnd23_intfvalld1_laoo` | MATRIX | 0.537 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents the changes in the combined sum of assets and liabilities when a company reports these totals as a single lin |
| 1590 | `fnd23_annfvalld1_rtcv` | MATRIX | 0.537 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Total |
| 1591 | `fnd23_annfvalld1_ipts` | MATRIX | 0.536 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Interest Cost |
| 1592 | `fnd23_blsm_cila` | MATRIX | 0.536 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Land/Improvements - Gross |
| 1593 | `loans_to_insiders` | MATRIX | 0.536 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | represents land and improvements on land at acquisition cost. Land is not depreciated, but land improvements are normall |
| 1594 | `fnd23_intfvm2_dtcv` | MATRIX | 0.532 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax – Domestic |
| 1595 | `fnd23_annfvalld1_spts` | MATRIX | 0.532 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Service Cost |
| 1596 | `fnd23_intfvalld1_1dls` | MATRIX | 0.532 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long Term Debt Maturing within 1 Year |
| 1597 | `fnd23_intfvalld1_1spdd` | MATRIX | 0.532 | 盈利与财务 | 0 | — | — | — | UNUSABLE | common dividends per share for common stock primary issues. |
| 1598 | `fnd23_annfvalld1_apts` | MATRIX | 0.531 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Plan Assets |
| 1599 | `fnd23_intfvalld1_amae` | MATRIX | 0.531 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of capitalized acquisition costs or goodwill |
| 1600 | `fnd23_blsm_3dls` | MATRIX | 0.531 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Maturing in Year 3 |
| 1601 | `short_term_loans_3_2` | MATRIX | 0.531 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long Term Debt Maturing in Year 3 |
| 1602 | `fnd23_intfvalld1_snii` | MATRIX | 0.530 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Deconsolidation of subsidiaries if ownership interest in a subsidiary is reduced classified as Sale/Maturity of Investme |
| 1603 | `fnd23_intfvalld1_b6dls` | MATRIX | 0.530 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Year 6 & Beyond |
| 1604 | `fnd23_intfvalld1_dltv` | MATRIX | 0.530 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Long-Term Debt, Supplemental reflects the sum of Long-Term Debt maturing within 1 through 10 years and Long-Term D |
| 1605 | `fnd23_icsm_m_pede` | MATRIX | 0.530 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Depreciation/Amortization |
| 1606 | `depreciation_expense_2` | MATRIX | 0.530 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation of fixed assets reported outside of the cost of goods and services sold. |
| 1607 | `fnd23_intfvm_1dls` | MATRIX | 0.528 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long Term Debt Maturing within 1 Year |
| 1608 | `short_term_debt_liabilities` | MATRIX | 0.528 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Maturing within 1 Year |
| 1609 | `fnd23_intfvalld1_ixts` | MATRIX | 0.527 | 其他 | 0 | — | — | — | UNUSABLE | Total Extraordinary Items |
| 1610 | `fnd23_intfvm2_b6dls` | MATRIX | 0.527 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Year 6 & Beyond |
| 1611 | `fnd23_intfvm_dltv` | MATRIX | 0.527 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Long Term Debt, Supplemental reflects the sum of Long Term Debt Maturing within 1 through 10 Years and Long Term |
| 1612 | `valuation_total_liabilities` | MATRIX | 0.527 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Long Term Debt, Supplemental |
| 1613 | `fnd23_intfvalld1_pcsv` | MATRIX | 0.525 | 其他 | 0 | — | — | — | UNUSABLE | Stock-Based Compensation, Supplemental |
| 1614 | `fnd23_intfvalld1_uaie` | MATRIX | 0.523 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Form of an unusual item related to the impairment of long-lived assets, certain identifiable intangibles, and goodwill r |
| 1615 | `fnd23_intfvm_darv` | MATRIX | 0.522 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement classified as Research & Development Expense, S |
| 1616 | `valuation_reinsurance_assets` | MATRIX | 0.522 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Research & Development Expense, Supplemental |
| 1617 | `fnd23_annfvalld1_drdv` | MATRIX | 0.522 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Discount Rate - Domestic |
| 1618 | `fnd23_annfvalld1_tniv` | MATRIX | 0.522 | 其他 | 0 | — | — | — | UNUSABLE | Intangibles - Net |
| 1619 | `fnd23_annfvalld1_lctv` | MATRIX | 0.522 | 其他 | 0 | — | — | — | UNUSABLE | Total Capital Leases, Supplemental |
| 1620 | `fnd23_intfvm2_uaiv` | MATRIX | 0.521 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Impairment-Assets Held for Use,Supplemental |
| 1621 | `fnd23_annfvalld1_rtla` | MATRIX | 0.521 | 其他 | 0 | — | — | — | UNUSABLE | Represents long-term notes receivable, excluding the current portion of the long-term receivables. It also represents al |
| 1622 | `fnd23_intfvalld1_nnis` | MATRIX | 0.521 | 其他 | 0 | — | — | — | UNUSABLE | Net - Net Operating, Total |
| 1623 | `fnd23_annfvalld1_1lcs` | MATRIX | 0.520 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Payments Due in Year 1 |
| 1624 | `other_assets_prepaid_balance` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Accounts Payable |
| 1625 | `fnd23_cf_m_idlf` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Issued |
| 1626 | `other_assets_purchase_balance` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents changes in accounts payable during the period. An increase inaccounts payable has a positive impact on cash f |
| 1627 | `financing_loan_drawdown_inflows` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents cash inflow on the issuance of long-term debt instruments in a company. Long-term debt may include long-term |
| 1628 | `fnd23_annfvalld1_vacl` | MATRIX | 0.519 | 其他 | 0 | — | — | — | UNUSABLE | Advances/deposits from customers for the products to be sold or services to be rendered classified as Customer Advances. |
| 1629 | `fnd23_blsm_4dls` | MATRIX | 0.518 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Maturing in Year 4 |
| 1630 | `short_term_loans_4` | MATRIX | 0.518 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long Term Debt Maturing in Year 4 |
| 1631 | `fnd23_intfvalld1_odix` | MATRIX | 0.518 | 其他 | 0 | — | — | — | UNUSABLE | Discontinued Operations. |
| 1632 | `dividend_income_received` | MATRIX | 0.517 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Depreciation of Right-of-Use Assets, Supplemental |
| 1633 | `dividend_received_unconsolidated` | MATRIX | 0.516 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation of Right-of-Use Assets, Supplemental |
| 1634 | `accumulated_provision_depreciation_assets` | MATRIX | 0.516 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Provision for Doubtful Accounts |
| 1635 | `accounts_payable_3` | MATRIX | 0.515 | 其他 | 0 | — | — | — | UNUSABLE | represents provisions established for doubtful accounts receivable. Provision for doubtful accounts is usually establish |
| 1636 | `fnd23_annfv1a_mocq` | MATRIX | 0.515 | 其他 | 0 | — | — | — | UNUSABLE | other comprehensive income. |
| 1637 | `fnd23_annfvalld1_rnmv` | MATRIX | 0.515 | 其他 | 0 | — | — | — | UNUSABLE | Minority Interest - Non-Redeemable |
| 1638 | `fnd23_annfvalld1_qaii` | MATRIX | 0.515 | 其他 | 0 | — | — | — | UNUSABLE | Franchise acquired (classified as Purchase/Acquisition of Intangibles). |
| 1639 | `fnd23_annfvalld1_cpca` | MATRIX | 0.515 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Construction in Progress - Gross represents the cost of construction in progress of fixed assets for a company's own use |
| 1640 | `fnd23_annfvalld1_crrf` | MATRIX | 0.514 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Treasury Stock, when reported in the financing section of the cash flow statement, is henceforth classified as Sale/Issu |
| 1641 | `fnd23_intfvalld1_rnmv` | MATRIX | 0.513 | 其他 | 0 | — | — | — | UNUSABLE | Minority Interest - Non-Redeemable |
| 1642 | `fnd23_intfvm_saie` | MATRIX | 0.513 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Impairment/write-down/write-off/revaluation of investment securities arising from an unusual event. |
| 1643 | `income_after_tax_2` | MATRIX | 0.513 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Impairment-Assets Held for Sale |
| 1644 | `fnd23_intfvalld1_ttiv` | MATRIX | 0.513 | 其他 | 0 | — | — | — | UNUSABLE | Income Tax - Total reflects the sum of Domestic Tax - Other, Foreign Tax - Other, Local Tax - Other and Other Tax. |
| 1645 | `fnd23_intfvm_cstq` | MATRIX | 0.513 | 其他 | 0 | — | — | — | UNUSABLE | represents the value of common stock owned by the issuing company or its consolidated subsidiaries. Treasury stock is re |
| 1646 | `fnd23_intfvalld1_ltem` | MATRIX | 0.512 | 其他 | 0 | — | — | — | UNUSABLE | Full-Time Employees |
| 1647 | `total_share_capital_3` | MATRIX | 0.512 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Treasury Stock - Common |
| 1648 | `fnd23_annfv1a_ixts` | MATRIX | 0.511 | 其他 | 0 | — | — | — | UNUSABLE | Total Extraordinary Items |
| 1649 | `fnd23_annfvalld1_dciv` | MATRIX | 0.510 | 其他 | 0 | — | — | — | UNUSABLE | Interest Cost - Domestic |
| 1650 | `fnd23_annfvalld1_dapv` | MATRIX | 0.509 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Plan Assets - Domestic |
| 1651 | `fnd23_intfvalld1_bpao` | MATRIX | 0.509 | 其他 | 0 | — | — | — | UNUSABLE | Represents changes in accounts payable during the period. An increase in accounts payable has a positive impact on cash |
| 1652 | `fnd23_annfvalld1_atcq` | MATRIX | 0.509 | 其他 | 0 | — | — | — | UNUSABLE | represents translation gains (losses) on financial statements of foreign subsidiaries. Such adjustments may be required |
| 1653 | `other_off_balance_liabilities` | MATRIX | 0.508 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other off-balance sheet liabilities for the annual period. |
| 1654 | `fnd23_annfvalld1_2lcs` | MATRIX | 0.508 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Payments Due in Year 2 |
| 1655 | `fnd23_annfvalld1_32lcs` | MATRIX | 0.508 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Payments Due in 2-3 Years |
| 1656 | `fnd23_intfvalld1_ctcv` | MATRIX | 0.507 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Total reflects the sum of Current Tax - Domestic, Current Tax - Foreign, Current Tax - Local, Current Tax |
| 1657 | `other_interest_liabilities` | MATRIX | 0.505 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other interest-bearing liabilities reported for the annual period. |
| 1658 | `fnd23_annfvalld1_dcsv` | MATRIX | 0.505 | 其他 | 0 | — | — | — | UNUSABLE | Service Cost - Domestic |
| 1659 | `fnd23_intfvm_pxrv` | MATRIX | 0.505 | 其他 | 0 | — | — | — | UNUSABLE | Rental Expense, Supplemental represents the total value of rental expenses paid for offices, factories, machinery and eq |
| 1660 | `valuation_reinsurance_expense` | MATRIX | 0.505 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Rental Expense, Supplemental |
| 1661 | `fnd23_annfvalld1_vdcv` | MATRIX | 0.504 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Derivative Liabilities - Hedging, Supplemental |
| 1662 | `fnd23_intfvm2_amae` | MATRIX | 0.504 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of capitalized acquisition costs or goodwill |
| 1663 | `fnd23_intfvalld1_oiis` | MATRIX | 0.503 | 其他 | 0 | — | — | — | UNUSABLE | Interest/Investment Income - Operating |
| 1664 | `fnd23_annfvalld1_3lcs` | MATRIX | 0.502 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Payments Due in Year 3 |
| 1665 | `fnd23_ratv` | MATRIX | 0.502 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Audit-Related Fees |
| 1666 | `asset_revaluation_gain` | MATRIX | 0.502 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Audit-Related Fees |
| 1667 | `fnd23_blsm_5dls` | MATRIX | 0.501 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Maturing in Year 5 |
| 1668 | `short_term_loans_5` | MATRIX | 0.501 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Year 5 |
| 1669 | `fnd23_intfvalld1_vnie` | MATRIX | 0.501 | 其他 | 0 | — | — | — | UNUSABLE | investing income from operating section. |
| 1670 | `fnd23_annfvalld1_pwia` | MATRIX | 0.501 | 其他 | 0 | — | — | — | UNUSABLE | inventories that are WIP or work-in-progress. |
| 1671 | `fnd23_annfvalld1_nppv` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Other Property/Plant/Equipment - Net |
| 1672 | `fnd23_annfvalld1_dcdv` | MATRIX | 0.499 | 其他 | 0 | — | — | — | UNUSABLE | Defined Contribution Expense - Domestic |
| 1673 | `fnd23_intfvalld1_ctdv` | MATRIX | 0.496 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax - Total |
| 1674 | `fnd23_intfvm_algn` | MATRIX | 0.496 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gain (Loss) on Sale of Assets. |
| 1675 | `gain_loss_on_asset_sales` | MATRIX | 0.496 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Gain (Loss) on Sale of Assets |
| 1676 | `fnd23_annfvalld1_uaie` | MATRIX | 0.496 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Form of an unusual item related to the impairment of long-lived assets, certain identifiable intangibles, and goodwill r |
| 1677 | `fnd23_annfvalld1_4lcs` | MATRIX | 0.495 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Payments Due in Year 4 |
| 1678 | `fnd23_annfvalld1_54lcs` | MATRIX | 0.495 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Payments Due in 4-5 Years |
| 1679 | `fnd23_intfvm_eros` | MATRIX | 0.495 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other Revenue, Total. |
| 1680 | `retained_earnings_balance_2` | MATRIX | 0.495 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Revenue, Total |
| 1681 | `fnd23_annfvalld1_iwgv` | MATRIX | 0.494 | 其他 | 0 | — | — | — | UNUSABLE | Goodwill - Net |
| 1682 | `fnd23_intfvm2_1spsd` | MATRIX | 0.494 | 其他 | 0 | — | — | — | UNUSABLE | Special DPS – Common Stock Primary Issue |
| 1683 | `valuation_difference_credit` | MATRIX | 0.493 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Deferred Revenue - Current |
| 1684 | `valuation_allowance_deferred_charges` | MATRIX | 0.493 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred Revenue - Current |
| 1685 | `fnd23_annfvmfm2_amav` | MATRIX | 0.493 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of Acquisition Costs, Supplemental |
| 1686 | `fnd23_intfvm_aieo` | MATRIX | 0.492 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents a reversal of non-cash earnings/losses from investments under the Equity Method. For such investments, undist |
| 1687 | `equity_investments_at_cost_2` | MATRIX | 0.492 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Equity in Net Earnings (Loss) |
| 1688 | `fnd23_fttv` | MATRIX | 0.491 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Tax Fees |
| 1689 | `total_transfer_to_funds` | MATRIX | 0.491 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Tax Fees |
| 1690 | `fnd23_intfvalld1_eros` | MATRIX | 0.490 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other Revenue, Total. |
| 1691 | `interest_expense_on_loans` | MATRIX | 0.490 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Expense on Lease Liabilities, Supplemental |
| 1692 | `impairment_expense_loss` | MATRIX | 0.490 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest Expense on Lease Liabilities, Supplemental |
| 1693 | `fnd23_annfvalld1_dcrv` | MATRIX | 0.489 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Compensation Rate - Domestic |
| 1694 | `fnd23_icsm_m_dtdv` | MATRIX | 0.488 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Deferred Tax - Domestic |
| 1695 | `deferred_tax_expense` | MATRIX | 0.488 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax – Domestic |
| 1696 | `fnd23_intfvalld1_b6los` | MATRIX | 0.488 | 其他 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Year 6 and Beyond represents Total Operating Leases, Supplemental less Stan |
| 1697 | `fnd23_intfvalld1_lotv` | MATRIX | 0.488 | 其他 | 0 | — | — | — | UNUSABLE | Total Operating Leases, Supplemental reflects the sum of operating leases maturing within 1 through 10 years, operating |
| 1698 | `fnd23_annfvalld1_5lcs` | MATRIX | 0.488 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Payments Due in Year 5 |
| 1699 | `fnd23_intfvalld1_1los` | MATRIX | 0.488 | 其他 | 0 | — | — | — | UNUSABLE | Operating Lease Payments Due in Year 1 |
| 1700 | `fnd23_annfvalld1_ddrv` | MATRIX | 0.486 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Discount Rate - Domestic |
| 1701 | `fnd23_annfv1a_pwia` | MATRIX | 0.485 | 其他 | 0 | — | — | — | UNUSABLE | inventories that are WIP or work-in-progress. |
| 1702 | `fnd23_annfvalld1_laoo` | MATRIX | 0.484 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents the changes in the combined sum of assets and liabilities when a company reports these totals as a single lin |
| 1703 | `fnd23_annfvalld1_pcsv` | MATRIX | 0.484 | 其他 | 0 | — | — | — | UNUSABLE | Stock-Based Compensation, Supplemental |
| 1704 | `accrued_goodwill_gross_amount` | MATRIX | 0.483 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Goodwill Gross |
| 1705 | `goodwill_gross` | MATRIX | 0.483 | 其他 | 0 | — | — | — | UNUSABLE | Goodwill, Gross |
| 1706 | `fnd23_intfvm2_serv` | MATRIX | 0.483 | 其他 | 0 | — | — | — | UNUSABLE | Restructuring Charge, Supplemental |
| 1707 | `fnd23_intfvalld1_bosi` | MATRIX | 0.483 | 其他 | 0 | — | — | — | UNUSABLE | Deconsolidation of a subsidiary classified as Sale of Business. |
| 1708 | `loans_current_assets_value` | MATRIX | 0.483 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Customer Advances |
| 1709 | `long_term_construction_advances` | MATRIX | 0.483 | 其他 | 0 | — | — | — | UNUSABLE | Advances/deposits from customers for the products to be sold or services to be rendered classified as Customer Advances. |
| 1710 | `fnd23_intfvalld1_ltio` | MATRIX | 0.482 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents changes in inventories during the period. An increase in inventories has a negative impact on cash flow from |
| 1711 | `fnd23_annfvalld1_b6lcs` | MATRIX | 0.481 | 其他 | 0 | — | — | — | UNUSABLE | Cap. Lease Pymts. Due in Year 6 & Beyond |
| 1712 | `fnd23_intfvalld1_crrf` | MATRIX | 0.481 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Treasury Stock, when reported in the financing section of the cash flow statement, is henceforth classified as Sale/Issu |
| 1713 | `fnd23_intfvm2_eptv` | MATRIX | 0.480 | 其他 | 0 | — | — | — | UNUSABLE | Total Pension Expense |
| 1714 | `dividends_payable_long_term` | MATRIX | 0.480 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Dividends per Share - Com Stock Issue 2 |
| 1715 | `fnd23_intfvm_2spdd` | MATRIX | 0.480 | 盈利与财务 | 0 | — | — | — | UNUSABLE | common dividends per share for common stock issue 2. |
| 1716 | `fnd23_cf_m_ltio` | MATRIX | 0.479 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories |
| 1717 | `other_interest_liabilities_2` | MATRIX | 0.479 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents changes in inventories during the period. An increase in inventories has a negative impact on cash flow from |
| 1718 | `fnd23_intfvm_b6los` | MATRIX | 0.479 | 其他 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Year 6 and Beyond represents Total Operating Leases, Supplemental  less St |
| 1719 | `other_noncurrent_liabilities` | MATRIX | 0.479 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Oper. Lse. Pymts. Due in Year 6 & Beyond |
| 1720 | `fnd23_intfvm_lotv` | MATRIX | 0.478 | 其他 | 0 | — | — | — | UNUSABLE | Total Operating Leases, Supplemental reflects the sum of Operating Leases Maturing within 1 through 10 Years, Operating |
| 1721 | `valuation_total_other_liabilities` | MATRIX | 0.478 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Operating Leases, Supplemental |
| 1722 | `fnd23_annfvalld1_fttv` | MATRIX | 0.478 | 其他 | 0 | — | — | — | UNUSABLE | Tax Fees |
| 1723 | `fnd23_intfvm_1los` | MATRIX | 0.477 | 其他 | 0 | — | — | — | UNUSABLE | Operating Lease Payments Due in Year 1 |
| 1724 | `long_term_borrowings` | MATRIX | 0.477 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 1 |
| 1725 | `valuation_adjustment_gross_amount` | MATRIX | 0.477 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Accumulated Goodwill Amortization, Supplemental |
| 1726 | `valuation_allowance_goodwill` | MATRIX | 0.477 | 其他 | 0 | — | — | — | UNUSABLE | Accumulated Goodwill Amortization, Supplemental |
| 1727 | `fnd23_annfvalld1_alge` | MATRIX | 0.476 | 盈利与财务 | 0 | — | — | — | UNUSABLE | loss/gain on sale of assets listed in the operating section. |
| 1728 | `fnd23_annfv1a_odix` | MATRIX | 0.475 | 其他 | 0 | — | — | — | UNUSABLE | Discontinued Operations. |
| 1729 | `fnd23_intfvalld1_alge` | MATRIX | 0.475 | 盈利与财务 | 0 | — | — | — | UNUSABLE | loss/gain on sale of assets listed in the operating section. |
| 1730 | `accrued_assets_gross_amount` | MATRIX | 0.475 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Accumulated Goodwill Amortization |
| 1731 | `accrued_grants_and_allowances` | MATRIX | 0.475 | 其他 | 0 | — | — | — | UNUSABLE | Accumulated Goodwill Amortization represents the accumulated amortization of goodwill acquired through mergers accordin |
| 1732 | `fnd23_annfvalld1_toia` | MATRIX | 0.473 | 其他 | 0 | — | — | — | UNUSABLE | Provision/allowances for inventory reported as a negative value classified as Inventories - Other |
| 1733 | `fnd23_annfvalld1_olcl` | MATRIX | 0.473 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Obligations |
| 1734 | `fnd23_blsm_itsa` | MATRIX | 0.472 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Short Term Investments |
| 1735 | `short_term_investments_other` | MATRIX | 0.472 | 其他 | 0 | — | — | — | UNUSABLE | Short-Term Investments |
| 1736 | `fnd23_annfvalld1_aieo` | MATRIX | 0.472 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity fo |
| 1737 | `fnd23_intfvalld1_algn` | MATRIX | 0.471 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gain (Loss) on Sale of Assets. |
| 1738 | `fnd23_annfvalld1_epts` | MATRIX | 0.469 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total Plan Expected Return |
| 1739 | `fnd23_annfvmfm2_saoo` | MATRIX | 0.469 | 其他 | 0 | — | — | — | UNUSABLE | Accrued interest income for companies other than financial service companies. |
| 1740 | `fnd23_annfv1a_saoo` | MATRIX | 0.469 | 其他 | 0 | — | — | — | UNUSABLE | Accrued interest income for companies other than financial service companies. |
| 1741 | `deferred_pension_plan_expense` | MATRIX | 0.467 | 其他 | 0 | — | — | — | UNUSABLE | Domestic Pension Plan Expense |
| 1742 | `depreciation_of_property_plant_equipment` | MATRIX | 0.467 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Domestic Pension Plan Expense |
| 1743 | `short_term_payables_other` | MATRIX | 0.467 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Plan Obligations |
| 1744 | `short_term_policyholder_obligations` | MATRIX | 0.467 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Obligations |
| 1745 | `fnd23_ssfv` | MATRIX | 0.466 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Funded Status |
| 1746 | `valuation_allowance_financial_securities` | MATRIX | 0.466 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total Funded Status |
| 1747 | `fnd23_intfvm_acda` | MATRIX | 0.466 | 盈利与财务 | 0 | — | — | — | UNUSABLE | current assets of discontinued operations. |
| 1748 | `accumulated_depreciation_current_assets` | MATRIX | 0.466 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Discontinued Operations - Current Asset |
| 1749 | `fnd23_cf_m_bloo` | MATRIX | 0.465 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Liabilities |
| 1750 | `other_operating_liabilities_balance` | MATRIX | 0.465 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other liabilities |
| 1751 | `fnd23_intfvm_nnie` | MATRIX | 0.465 | 其他 | 0 | — | — | — | UNUSABLE | interest expense from net operating income. |
| 1752 | `income_nonoperating` | MATRIX | 0.465 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Expense(Income) - Net Operating |
| 1753 | `fnd23_intfvm2_ppdv` | MATRIX | 0.462 | 其他 | 0 | — | — | — | UNUSABLE | Domestic Pension Plan Expense |
| 1754 | `equity_investments_affiliates` | MATRIX | 0.462 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Equity In Affiliates |
| 1755 | `fnd23_intfvm_aiec` | MATRIX | 0.462 | 盈利与财务 | 0 | — | — | — | UNUSABLE | This item represents the share of earnings/losses that the company is entitled to from unconsolidated affiliated compani |
| 1756 | `fnd23_annfvalld1_dtrv` | MATRIX | 0.462 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Compensation Rate - Domestic |
| 1757 | `fnd23_intfvm2_ftcv` | MATRIX | 0.461 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax – Foreign |
| 1758 | `fnd23_intfvalld1_dgcd` | MATRIX | 0.460 | 盈利与财务 | 0 | — | — | — | UNUSABLE | gross dividends on common stock. |
| 1759 | `unrealized_capital_gains` | MATRIX | 0.459 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Right-of-Use Assets - Capital Lease, Gross - Supplemental |
| 1760 | `unrealized_currency_gain` | MATRIX | 0.459 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Right-of-Use Assets - Capital Lease, Gross - Supplemental |
| 1761 | `fnd23_intfvalld1_inas` | MATRIX | 0.458 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total adjustments to net income represents sum of preferred dividend, general partners' distributions, miscellaneous ear |
| 1762 | `fnd23_intfvm_yppa` | MATRIX | 0.458 | 其他 | 0 | — | — | — | UNUSABLE | prepaid expenses. |
| 1763 | `prepaid_expenses_3` | MATRIX | 0.458 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Prepaid Expenses |
| 1764 | `fnd23_intfvalld1_sere` | MATRIX | 0.458 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Restructuring Charge is an unusual or non-recurring item related to a significant rearrangement of a company's assets an |
| 1765 | `fnd23_intfvalld1_qaii` | MATRIX | 0.457 | 其他 | 0 | — | — | — | UNUSABLE | Franchise acquired (classified as Purchase/Acquisition of Intangibles). |
| 1766 | `fnd23_intfvalld1_tius` | MATRIX | 0.456 | 其他 | 0 | — | — | — | UNUSABLE | Non-Recurring Items, Total |
| 1767 | `fnd23_annfvalld1_hsca` | MATRIX | 0.452 | 其他 | 0 | — | — | — | UNUSABLE | Cash represents cash on hand, balances on demand deposits, and near-term savings and time deposits. These should be read |
| 1768 | `fnd23_annfvalld1_ratv` | MATRIX | 0.452 | 其他 | 0 | — | — | — | UNUSABLE | Audit-Related Fees |
| 1769 | `fnd23_intfvm_dare` | MATRIX | 0.451 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement. |
| 1770 | `research_and_development_expense_3` | MATRIX | 0.451 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | [Quarterly] Research & Development |
| 1771 | `fnd23_annfvalld1_lvdv` | MATRIX | 0.451 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Non-Current Derivative Liabilities - Hedging, Supplemental |
| 1772 | `fnd23_annfvalld1_nvii` | MATRIX | 0.450 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in investments in securities and other investments. Investment, Net is utilized when a company does n |
| 1773 | `fnd23_annfv_value` | VECTOR | 0.450 | 其他 | 0 | — | — | — | UNUSABLE | annual financial values. |
| 1774 | `fnd23_intfvalld1_imae` | MATRIX | 0.449 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Amortization of intangible assets reported outside the cost of goods and services sold. |
| 1775 | `fnd23_intfvm_mocq` | MATRIX | 0.447 | 其他 | 0 | — | — | — | UNUSABLE | other comprehensive income. |
| 1776 | `common_stock_market_value` | MATRIX | 0.446 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Comprehensive Income |
| 1777 | `fnd23_annfv1a_darv` | MATRIX | 0.446 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement classified as Research & Development Expense, S |
| 1778 | `deferred_revenue_debt` | MATRIX | 0.445 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Discount Rate - Domestic |
| 1779 | `fnd23_annfvalld1_dpxv` | MATRIX | 0.445 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected Return on Plan Assets - Domestic |
| 1780 | `valuation_allowance_debt_receivables` | MATRIX | 0.445 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Discount Rate – Domestic |
| 1781 | `fnd23_intfvm_vdav` | MATRIX | 0.445 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Advertising Expense - Supplemental represents the total cost of advertising incurred by the company. |
| 1782 | `valuation_allowance_deferred_value` | MATRIX | 0.445 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | [Quarterly] Advertising Expense, Supplemental |
| 1783 | `fnd23_intfvm2_bpol` | MATRIX | 0.445 | 其他 | 0 | — | — | — | UNUSABLE | Other Payables |
| 1784 | `fnd23_intfvalld1_rtdv` | MATRIX | 0.445 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax - Total |
| 1785 | `fnd23_intfvm2_spts` | MATRIX | 0.445 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Service Cost |
| 1786 | `fnd23_annfvalld1_cstq` | MATRIX | 0.444 | 其他 | 0 | — | — | — | UNUSABLE | represents the value of common stock owned by the issuing company or its consolidated subsidiaries. Treasury stock is re |
| 1787 | `fnd23_intfvm_eror` | MATRIX | 0.444 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other revenue. |
| 1788 | `other_revenue_total` | MATRIX | 0.444 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Revenue |
| 1789 | `fnd23_annfv_item` | VECTOR | 0.443 | 其他 | 0 | — | — | — | UNUSABLE | integer index of the item description field. You can use this index to find out what the value is from itemIx. |
| 1790 | `fnd23_intfvalld1_bloo` | MATRIX | 0.443 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other liabilities |
| 1791 | `extraordinary_items_total_6` | MATRIX | 0.443 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Extraordinary Item |
| 1792 | `fnd23_intfvm2_artx` | MATRIX | 0.443 | 其他 | 0 | — | — | — | UNUSABLE | Extraordinary Item. |
| 1793 | `fnd23_intfvm_artx` | MATRIX | 0.443 | 其他 | 0 | — | — | — | UNUSABLE | Extraordinary Item. |
| 1794 | `fnd23_intfvm_pacv` | MATRIX | 0.442 | 其他 | 0 | — | — | — | UNUSABLE | Interest Capitalized, Supplemental |
| 1795 | `valuation_capital_assets` | MATRIX | 0.442 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Capitalized, Supplemental |
| 1796 | `fnd23_intfvm2_dcsv` | MATRIX | 0.441 | 其他 | 0 | — | — | — | UNUSABLE | Service Cost - Domestic |
| 1797 | `fnd23_intfvalld1_eror` | MATRIX | 0.440 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other revenue. |
| 1798 | `fnd23_intfvalld1_darv` | MATRIX | 0.439 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement classified as Research & Development Expense, S |
| 1799 | `fnd23_intfvm2_ipts` | MATRIX | 0.437 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Interest Cost |
| 1800 | `accounts_payable_deferred` | MATRIX | 0.437 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Pension Obligation - Domestic |
| 1801 | `valuation_allowance_accounts_payable` | MATRIX | 0.437 | 其他 | 0 | — | — | — | UNUSABLE | Pension Obligation - Domestic |
| 1802 | `prepaid_expenses_value` | MATRIX | 0.435 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | [Quarterly] Funded Status - Domestic |
| 1803 | `valuation_allowance_property_plant` | MATRIX | 0.435 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funded Status – Domestic |
| 1804 | `fnd23_intfvm2_ddrv` | MATRIX | 0.435 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Discount Rate – Domestic |
| 1805 | `bonds_payable_long_term` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 2 |
| 1806 | `fnd23_intfvm_2los` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Operating Lease Payments Due in Year 2 |
| 1807 | `fnd23_intfvm_32los` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Years 2 and 3 represents the summation of Standardized Operating Lease Paym |
| 1808 | `other_long_term_liabilities_6` | MATRIX | 0.435 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Pymts. Due in 2-3 Years |
| 1809 | `fnd23_intfvm2_rpts` | MATRIX | 0.434 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Other Expense represents the total amount of other expenses on all of a company’s pension and post-retiremen |
| 1810 | `preferred_stock_dividends` | MATRIX | 0.433 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Plan Service Cost |
| 1811 | `total_premiums_written` | MATRIX | 0.433 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Service Cost |
| 1812 | `fnd23_intfvm2_dciv` | MATRIX | 0.433 | 其他 | 0 | — | — | — | UNUSABLE | Interest Cost – Domestic |
| 1813 | `fnd23_annfv1a_acda` | MATRIX | 0.433 | 盈利与财务 | 0 | — | — | — | UNUSABLE | current assets of discontinued operations. |
| 1814 | `fnd23_intfvalld1_iwgv` | MATRIX | 0.432 | 其他 | 0 | — | — | — | UNUSABLE | Goodwill - Net |
| 1815 | `fnd23_intfvm2_opxv` | MATRIX | 0.432 | 其他 | 0 | — | — | — | UNUSABLE | Other Pension, Net - Domestic |
| 1816 | `debt_conversion_discount` | MATRIX | 0.431 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Defined Contribution Expense – Domestic |
| 1817 | `fnd23_icsm_m_dcdv` | MATRIX | 0.431 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Defined Contribution Expense - Domestic |
| 1818 | `fnd23_annfvalld1_nnis` | MATRIX | 0.431 | 其他 | 0 | — | — | — | UNUSABLE | Net - Net Operating, Total |
| 1819 | `fnd23_intfvalld1_xeal` | MATRIX | 0.430 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Represents operational expenses accrued, but not yet paid. As current liabilities, such expenses are expected to be paid |
| 1820 | `income_before_tax` | MATRIX | 0.429 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Plan Interest Cost |
| 1821 | `total_premiums_issued` | MATRIX | 0.429 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Interest Cost |
| 1822 | `fnd23_intfvm_drpc` | MATRIX | 0.429 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents the total amount of the current dividend requirement on issued preferred stock of a company (including its su |
| 1823 | `preferred_dividends` | MATRIX | 0.429 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents the total amount of the current dividend requirement on issued preferred stock of a company (including its su |
| 1824 | `preferred_stock` | MATRIX | 0.429 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Preferred Dividends |
| 1825 | `fnd23_intfvalld1_rtcv` | MATRIX | 0.427 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Total |
| 1826 | `fnd23_annfv1a_cbpa` | MATRIX | 0.426 | 其他 | 0 | — | — | — | UNUSABLE | represents the gross amount of buildings and their attachments, before being reduced by accumulated depreciation of the |
| 1827 | `fnd23_intfvalld1_nvii` | MATRIX | 0.425 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in investments in securities and other investments. Investment, Net is utilized when a company does n |
| 1828 | `fnd23_intfvm_saoo` | MATRIX | 0.425 | 其他 | 0 | — | — | — | UNUSABLE | Accrued interest income for companies other than financial service companies. |
| 1829 | `other_assets_short_term_2` | MATRIX | 0.425 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Assets |
| 1830 | `fnd23_intfvalld1_nnie` | MATRIX | 0.425 | 其他 | 0 | — | — | — | UNUSABLE | interest expense from net operating income. |
| 1831 | `fnd23_intfvalld1_dtcv` | MATRIX | 0.424 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Domestic |
| 1832 | `allowance_for_investment_gain` | MATRIX | 0.423 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories - Finished Goods |
| 1833 | `investments_in_foreign_government_securities` | MATRIX | 0.423 | 其他 | 0 | — | — | — | UNUSABLE | represents inventories of unsold finished goods on hand. These goods may have been produced internally or purchased for |
| 1834 | `fnd23_intfvm2_dcdv` | MATRIX | 0.423 | 其他 | 0 | — | — | — | UNUSABLE | Defined Contribution Expense – Domestic |
| 1835 | `fnd23_intfvm2_epts` | MATRIX | 0.423 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total Plan Expected Return |
| 1836 | `fnd23_intfvm2_dpxv` | MATRIX | 0.422 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected Return on Plan Assets - Domestic |
| 1837 | `fnd23_intfvalld1_atcq` | MATRIX | 0.420 | 其他 | 0 | — | — | — | UNUSABLE | represents translation gains (losses) on financial statements of foreign subsidiaries. Such adjustments may be required |
| 1838 | `fnd23_intfvalld1_rtla` | MATRIX | 0.420 | 其他 | 0 | — | — | — | UNUSABLE | Represents long-term notes receivable, excluding the current portion of the long-term receivables. It also represents al |
| 1839 | `fnd23_intfvm_tile` | MATRIX | 0.419 | 其他 | 0 | — | — | — | UNUSABLE | litigation costs. These are non-recurring/unusual items reported within the cost of goods and services sold. |
| 1840 | `litigation_expenses` | MATRIX | 0.419 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Litigation |
| 1841 | `service_contract_revenue` | MATRIX | 0.418 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Service Cost - Domestic |
| 1842 | `stock_compensation_expense` | MATRIX | 0.418 | 其他 | 0 | — | — | — | UNUSABLE | Service Cost - Domestic |
| 1843 | `fnd23_intfvm2_saiv` | MATRIX | 0.418 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Impairment-Assets Held for Sale, Supplemental |
| 1844 | `fnd23_annfvalld1_dtcv` | MATRIX | 0.417 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Domestic |
| 1845 | `fnd23_intfvalld1_2los` | MATRIX | 0.416 | 其他 | 0 | — | — | — | UNUSABLE | Operating Lease Payments Due in Year 2 |
| 1846 | `fnd23_intfvalld1_32los` | MATRIX | 0.416 | 其他 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Years 2 and 3 represents the summation of Standardized Operating Lease Paym |
| 1847 | `fnd23_annfvalld1_saoo` | MATRIX | 0.416 | 其他 | 0 | — | — | — | UNUSABLE | Accrued interest income for companies other than financial service companies. |
| 1848 | `fnd23_intfvm2_sptv` | MATRIX | 0.415 | 其他 | 0 | — | — | — | UNUSABLE | Prior Service Cost – Domestic |
| 1849 | `short_term_pension_assets` | MATRIX | 0.413 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total Plan Assets |
| 1850 | `short_term_provisions_assets` | MATRIX | 0.413 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Plan Assets |
| 1851 | `income_from_discontinued_operations` | MATRIX | 0.413 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Cost - Domestic |
| 1852 | `insurance_claims_expense` | MATRIX | 0.413 | 其他 | 0 | — | — | — | UNUSABLE | Interest Cost – Domestic |
| 1853 | `fnd23_intfvm2_hsca` | MATRIX | 0.413 | 其他 | 0 | — | — | — | UNUSABLE | Cash represents cash on hand, balances on demand deposits, and near-term savings and time deposits. These should be rea |
| 1854 | `fnd23_intfvmfm2_hsca` | MATRIX | 0.413 | 其他 | 0 | — | — | — | UNUSABLE | Cash represents cash on hand, balances on demand deposits, and near-term savings and time deposits. These should be rea |
| 1855 | `fnd23_intfvalld1_aiec` | MATRIX | 0.411 | 盈利与财务 | 0 | — | — | — | UNUSABLE | This item represents the share of earnings/losses that the company is entitled to from unconsolidated affiliated compani |
| 1856 | `fnd23_annfv1a_sere` | MATRIX | 0.411 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Restructuring Charge is an unusual or non-recurring item related to a significant rearrangement of a company’s assets an |
| 1857 | `fnd23_intfvalld1_2spdd` | MATRIX | 0.410 | 盈利与财务 | 0 | — | — | — | UNUSABLE | common dividends per share for common stock issue 2. |
| 1858 | `fnd23_icsm_m_nnis` | MATRIX | 0.409 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Expense (Income), Net - Operating, Total |
| 1859 | `fnd23_intfvm2_dtrv` | MATRIX | 0.409 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Compensation Rate – Domestic |
| 1860 | `interest_income_net_total` | MATRIX | 0.409 | 其他 | 0 | — | — | — | UNUSABLE | Net - Net Operating, Total |
| 1861 | `fnd23_intfvm2_gaxv` | MATRIX | 0.409 | 其他 | 0 | — | — | — | UNUSABLE | Actuarial Gains and Losses – Domestic |
| 1862 | `fnd23_annfv1a_tmas` | MATRIX | 0.409 | 其他 | 0 | — | — | — | UNUSABLE | amortization representes sum of amortization of intangibles, amortization of acquisition costs, amortization of deferred |
| 1863 | `fnd23_annfvalld1_dtdv` | MATRIX | 0.409 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax - Domestic |
| 1864 | `fnd23_annfvalld1_imae` | MATRIX | 0.409 | 盈利与财务 | 0 | — | — | — | UNUSABLE | amortization of intangible assets reported outside the cost of goods and services sold |
| 1865 | `fnd23_annfvalld1_oiis` | MATRIX | 0.408 | 其他 | 0 | — | — | — | UNUSABLE | Interest/Investment Income - Operating |
| 1866 | `fnd23_intfvalld1_aemc` | MATRIX | 0.406 | 盈利与财务 | 0 | — | — | — | UNUSABLE | miscellaneous earnings adjustment. |
| 1867 | `fnd23_intfvm2_qftm` | MATRIX | 0.406 | 其他 | 0 | — | — | — | UNUSABLE | Retail Sales represents the total value of sales at retail locations (physical stores) during the period. |
| 1868 | `unrealized_currency_net_balancesheet` | MATRIX | 0.406 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Right-of-Use Assets - Capital Lease, Net - Supplemental |
| 1869 | `valuation_allowance_uncollected_notes` | MATRIX | 0.406 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Right-of-Use Assets - Capital Lease, Net - Supplemental |
| 1870 | `cash_interest_received` | MATRIX | 0.405 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Capitalized - Non-Operating |
| 1871 | `fnd23_intfvm_nicn` | MATRIX | 0.405 | 其他 | 0 | — | — | — | UNUSABLE | non operating interest capitalized. |
| 1872 | `fnd23_intfvalld1_dtdv` | MATRIX | 0.405 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax - Domestic |
| 1873 | `fnd23_intfvm_cdav` | MATRIX | 0.405 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred Revenue - Current |
| 1874 | `fnd23_intfvalld1_indv` | MATRIX | 0.405 | 其他 | 0 | — | — | — | UNUSABLE | Net Interest Cost - Domestic |
| 1875 | `valuation_allowance_deferred_credits` | MATRIX | 0.405 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Deferred Revenue - Current |
| 1876 | `fnd23_intfvm2_tcxv` | MATRIX | 0.404 | 其他 | 0 | — | — | — | UNUSABLE | Curtailments and Settlements – Domestic |
| 1877 | `fnd23_annfvalld1_vnie` | MATRIX | 0.404 | 其他 | 0 | — | — | — | UNUSABLE | investing income from operating section. |
| 1878 | `fnd23_intfvm2_uatv` | MATRIX | 0.403 | 其他 | 0 | — | — | — | UNUSABLE | Audit Fees |
| 1879 | `advances_to_vendors` | MATRIX | 0.403 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | [Quarterly] Advertising Expense |
| 1880 | `fnd23_intfvm_vdae` | MATRIX | 0.403 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | advertising expense reported outside the cost of goods and services sold |
| 1881 | `fnd23_blsm_mria` | MATRIX | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories - Raw Materials |
| 1882 | `investments_in_real_estate` | MATRIX | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories - Raw Materials |
| 1883 | `fnd23_intfvalld1_eiuv` | MATRIX | 0.402 | 其他 | 0 | — | — | — | UNUSABLE | Other Unusual Expense (Income), Supplemental |
| 1884 | `fnd23_annfvalld1_dtsl` | MATRIX | 0.402 | 盈利与财务 | 0 | — | — | — | UNUSABLE | notes payable/short term debt. |
| 1885 | `fnd23_annfvalld1_srav` | MATRIX | 0.400 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Assets Recognized on Balance Sheet |
| 1886 | `provision_for_asset_depreciation` | MATRIX | 0.400 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Plan Assets - Domestic |
| 1887 | `valuation_allowance_property_assets` | MATRIX | 0.400 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Plan Assets - Domestic |
| 1888 | `fnd23_intfvm_ctpa` | MATRIX | 0.400 | 其他 | 0 | — | — | — | UNUSABLE | gross property, plant & equipment. |
| 1889 | `ppent` | MATRIX | 0.400 | 其他 | 0 | — | — | — | UNUSABLE | gross property, plant & equipment. |
| 1890 | `property_plant_equipment_gross` | MATRIX | 0.400 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Property/Plant/Equipment, Total - Gross |
| 1891 | `fnd23_intfvm2_ltcv` | MATRIX | 0.399 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax – Local |
| 1892 | `fnd23_annfv1a_ndsf` | MATRIX | 0.399 | 盈利与财务 | 0 | — | — | — | UNUSABLE | If short-term debt issuances and reductions are not delineated separately, the total is classified as Short Term Debt, N |
| 1893 | `fnd23_intfvalld1_pxrv` | MATRIX | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | Rental Expense, Supplemental represents the total value of rental expenses paid for offices, factories, machinery, and e |
| 1894 | `fnd23_intfvalld1_saie` | MATRIX | 0.397 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Impairment/write-down/write-off/revaluation of investment securities arising from an unusual event. |
| 1895 | `fnd23_rnd_expense` | MATRIX | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | R&D expenses. |
| 1896 | `fnd23_intfvalld1_cstq` | MATRIX | 0.397 | 其他 | 0 | — | — | — | UNUSABLE | Represents the value of common stock owned by the issuing company or its consolidated subsidiaries. Treasury stock is re |
| 1897 | `fnd23_annfvalld1_darv` | MATRIX | 0.396 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement classified as Research & Development Expense, S |
| 1898 | `fnd23_intfvm_vacl` | MATRIX | 0.396 | 其他 | 0 | — | — | — | UNUSABLE | Advances/deposits from customers for the products to be sold or services to be rendered classified as Customer Advances. |
| 1899 | `current_assets` | MATRIX | 0.396 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Customer Advances |
| 1900 | `fnd23_intfvalld1_aieo` | MATRIX | 0.396 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity fo |
| 1901 | `fnd23_intfvm2_eprv` | MATRIX | 0.395 | 其他 | 0 | — | — | — | UNUSABLE | Post-Retirement Plan Expense |
| 1902 | `valuation_realized_currency_difference` | MATRIX | 0.395 | 宏观与行业 | 0 | — | — | — | UNUSABLE | [Quarterly] Compensation Rate - Domestic |
| 1903 | `valuation_allowance_receivables` | MATRIX | 0.394 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Compensation Rate - Domestic |
| 1904 | `fnd23_annfv1a_inas` | MATRIX | 0.394 | 盈利与财务 | 0 | — | — | — | UNUSABLE | total adjustments to net income represents sum of preferred dividend, general partners distributions, misc. earnings adj |
| 1905 | `fnd23_annfvalld1_eros` | MATRIX | 0.392 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other Revenue, Total. |
| 1906 | `fnd23_intfvm_oeis` | MATRIX | 0.391 | 其他 | 0 | — | — | — | UNUSABLE | Interest Expense, Net – Operating |
| 1907 | `fnd23_intfvm_xeie` | MATRIX | 0.391 | 其他 | 0 | — | — | — | UNUSABLE | interest expense. |
| 1908 | `income_from_equity_investments` | MATRIX | 0.391 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Expense |
| 1909 | `interest_expense` | MATRIX | 0.391 | 其他 | 0 | — | — | — | UNUSABLE | Interest Expense, Net – Operating |
| 1910 | `interest_income_value` | MATRIX | 0.391 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Expense, Net - Operating |
| 1911 | `fnd23_intfvm2_odrv` | MATRIX | 0.391 | 价量与波动 | 0 | — | — | — | UNUSABLE | Expected Rate of Return – Domestic |
| 1912 | `fnd23_intfvm2_ppfv` | MATRIX | 0.391 | 其他 | 0 | — | — | — | UNUSABLE | Foreign Pension Plan Expense |
| 1913 | `fnd23_intfvm2_ltdv` | MATRIX | 0.390 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax – Local |
| 1914 | `fnd23_annfv1a_saie` | MATRIX | 0.389 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Impairment/write-down/write-off/revaluation of investment securities arising from an unusual event. |
| 1915 | `fnd23_intfvm2_cspv` | MATRIX | 0.388 | 其他 | 0 | — | — | — | UNUSABLE | Service Cost – Post-Retirement |
| 1916 | `fnd23_intfvm2_csfv` | MATRIX | 0.388 | 其他 | 0 | — | — | — | UNUSABLE | Service Cost |
| 1917 | `accounts_payable_current_2` | MATRIX | 0.388 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Construction in Progress - Gross |
| 1918 | `capitalized_contract_costs` | MATRIX | 0.388 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Construction in Progress – Gross represents the cost of construction in progress of fixed assets for a company’s own us |
| 1919 | `fnd23_intfvalld1_otcv` | MATRIX | 0.385 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Other |
| 1920 | `fnd23_annfvalld1_tmas` | MATRIX | 0.385 | 其他 | 0 | — | — | — | UNUSABLE | Amortization represents sum of amortization of intangibles, amortization of acquisition costs, amortization of deferred |
| 1921 | `fnd23_intfvm2_cifv` | MATRIX | 0.385 | 其他 | 0 | — | — | — | UNUSABLE | Interest Cost – Foreign |
| 1922 | `fnd23_intfvm2_csxv` | MATRIX | 0.385 | 其他 | 0 | — | — | — | UNUSABLE | Prior Service Cost |
| 1923 | `fnd23_intfvm2_cipv` | MATRIX | 0.385 | 其他 | 0 | — | — | — | UNUSABLE | Interest Cost – Post-Retirement |
| 1924 | `fnd23_intfvm_ifpv` | MATRIX | 0.384 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Income After Stock-Based Compensation Expense |
| 1925 | `valuation_pension_fund_investments` | MATRIX | 0.384 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Net Income After Stock-Based Compensation Expense |
| 1926 | `fnd23_intfvm_veev` | MATRIX | 0.384 | 其他 | 0 | — | — | — | UNUSABLE | Pro Forma Stock Compensation Expense represents employee compensation paid in the form of stock options that have not y |
| 1927 | `fnd23_intfvm_bfpv` | MATRIX | 0.384 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Basic EPS After Stock-Based Compensation Expense represents Net Income After Stock-Based Compensation Expense divided b |
| 1928 | `fnd23_intfvm_dfpv` | MATRIX | 0.384 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Diluted EPS After Stock-Based Compensation Expense represents Net Income After Stock-Based Compensation Expense plus th |
| 1929 | `valuation_equity_earnings_value` | MATRIX | 0.384 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Pro Forma Stock Compensation Expense |
| 1930 | `valuation_pension_fund_balance` | MATRIX | 0.384 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | [Quarterly] Basic EPS after Stock Based Comp. Exp. |
| 1931 | `valuation_pension_fund_deficit` | MATRIX | 0.384 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | [Quarterly] Diluted EPS after Stock Based Comp. Exp. |
| 1932 | `fnd23_intfvalld1_pinv` | MATRIX | 0.384 | 其他 | 0 | — | — | — | UNUSABLE | Net Interest Cost - Post-Retirement |
| 1933 | `fnd23_intfvalld1_infv` | MATRIX | 0.383 | 其他 | 0 | — | — | — | UNUSABLE | Net Interest Cost - Foreign represents the increase in projected benefit obligation due to the passage of time for plans |
| 1934 | `fnd23_intfvalld1_otov` | MATRIX | 0.383 | 其他 | 0 | — | — | — | UNUSABLE | Other Tax |
| 1935 | `fnd23_intfvm2_epxv` | MATRIX | 0.383 | 其他 | 0 | — | — | — | UNUSABLE | Other Post-Retirement, Net |
| 1936 | `fnd23_annfvalld1_sonm` | MATRIX | 0.383 | 其他 | 0 | — | — | — | UNUSABLE | Number of Common Shareholders |
| 1937 | `fnd23_intfvm2_rxfv` | MATRIX | 0.382 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected Return on Assets – Foreign |
| 1938 | `fnd23_intfvm2_laxv` | MATRIX | 0.382 | 其他 | 0 | — | — | — | UNUSABLE | Actuarial Gains and Losses – Post-Retirement |
| 1939 | `fnd23_intfvm_tnir` | MATRIX | 0.382 | 其他 | 0 | — | — | — | UNUSABLE | interest income. |
| 1940 | `interest_income_total_3` | MATRIX | 0.382 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Income, Non-Bank |
| 1941 | `fnd23_intfvm2_rtxv` | MATRIX | 0.381 | 其他 | 0 | — | — | — | UNUSABLE | Transition Costs – Domestic |
| 1942 | `fnd23_intfvalld1_dare` | MATRIX | 0.381 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement. |
| 1943 | `fnd23_intfvm_ndsf` | MATRIX | 0.381 | 盈利与财务 | 0 | — | — | — | UNUSABLE | If short-term debt issuances and reductions are not delineated separately, the total is classified as Short Term Debt, N |
| 1944 | `short_term_debt_net` | MATRIX | 0.381 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Short Term Debt, Net |
| 1945 | `fnd23_intfvm2_scxv` | MATRIX | 0.380 | 其他 | 0 | — | — | — | UNUSABLE | Curtailments & Settlements – Post-Retirement |
| 1946 | `fnd23_intfvalld1_ftcv` | MATRIX | 0.380 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Foreign |
| 1947 | `fnd23_intfvm_peda` | MATRIX | 0.380 | 盈利与财务 | 0 | — | — | — | UNUSABLE | aggregate of accumulated depreciation for each fixed asset. |
| 1948 | `accum_depre` | MATRIX | 0.380 | 盈利与财务 | 0 | — | — | — | UNUSABLE | aggregate of accumulated depreciation for each fixed asset. |
| 1949 | `accumulated_depreciation_expense` | MATRIX | 0.380 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Accumulated Depreciation, Total |
| 1950 | `fnd23_intfvm2_fcdv` | MATRIX | 0.380 | 其他 | 0 | — | — | — | UNUSABLE | Defined Contribution Expense – Foreign |
| 1951 | `fnd23_intfvm2_ptfv` | MATRIX | 0.380 | 其他 | 0 | — | — | — | UNUSABLE | Prior Service Cost – Foreign |
| 1952 | `fnd23_intfvm2_ayfv` | MATRIX | 0.379 | 其他 | 0 | — | — | — | UNUSABLE | Actuarial Gains and Losses – Foreign |
| 1953 | `fnd23_intfvm2_fcpv` | MATRIX | 0.379 | 其他 | 0 | — | — | — | UNUSABLE | Other Pension, Net – Foreign |
| 1954 | `fnd23_annfvalld1_cbpa` | MATRIX | 0.378 | 其他 | 0 | — | — | — | UNUSABLE | represents the gross amount of buildings and their attachments, before being reduced by accumulated depreciation of the |
| 1955 | `fnd23_intfvm2_rcdv` | MATRIX | 0.378 | 其他 | 0 | — | — | — | UNUSABLE | Defined Contribution Expense Post-Retirement |
| 1956 | `fnd23_intfvm2_apxv` | MATRIX | 0.376 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected Return on Assets – Post-Retirement |
| 1957 | `fnd23_intfvm2_ctxv` | MATRIX | 0.376 | 其他 | 0 | — | — | — | UNUSABLE | Transition Costs – Post-Retirement |
| 1958 | `fnd23_intfvm_2dls` | MATRIX | 0.376 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Year 4 |
| 1959 | `fnd23_intfvm_32dls` | MATRIX | 0.376 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Years 2 and 3 represents the summation of Standardized Long Term Debt Maturing i |
| 1960 | `accounts_payable_total_3` | MATRIX | 0.376 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Maturing in Year 2 |
| 1961 | `other_short_term_liabilities` | MATRIX | 0.376 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Long Term Debt Maturing in 2-3 Years |
| 1962 | `fnd23_intfvalld1_drpc` | MATRIX | 0.375 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents the total amount of the current dividend requirement on issued preferred stock of a company (including its su |
| 1963 | `fnd23_annfvalld1_ndsf` | MATRIX | 0.375 | 盈利与财务 | 0 | — | — | — | UNUSABLE | If short-term debt issuances and reductions are not delineated separately, the total is classified as Short Term Debt, N |
| 1964 | `fnd23_annfvalld1_ixts` | MATRIX | 0.375 | 其他 | 0 | — | — | — | UNUSABLE | Total Extraordinary Items |
| 1965 | `fnd23_intfvm_gnia` | MATRIX | 0.375 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents the gross purchase value of assets that lack physical existence, before being reduced by accumulated impairm |
| 1966 | `insurance_net_gross` | MATRIX | 0.374 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Intangibles - Gross |
| 1967 | `treasury_stock_current` | MATRIX | 0.374 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Treasury Stock - Common |
| 1968 | `research_and_development_expense` | MATRIX | 0.374 | 宏观与行业 | 0 | — | — | — | UNUSABLE | [Quarterly] Discount Rate - Domestic |
| 1969 | `research_and_development_expense_2` | MATRIX | 0.374 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Discount Rate – Domestic |
| 1970 | `treasury_stock_common` | MATRIX | 0.374 | 其他 | 0 | — | — | — | UNUSABLE | represents the value of common stock owned by the issuing company or its consolidated subsidiaries. Treasury stock is re |
| 1971 | `fnd23_annfvalld1_edav` | MATRIX | 0.373 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity % - Domestic |
| 1972 | `fnd23_intfvm_aiav` | MATRIX | 0.373 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accumulated Intangible Amortization represents accumulated amortization against intangible fixed assets. |
| 1973 | `valuation_allowance_intangible_assets_3` | MATRIX | 0.373 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Accumulated Intangible Amort, Supplemental |
| 1974 | `fnd23_intfvalld1_otdv` | MATRIX | 0.373 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax - Other |
| 1975 | `fnd23_intfvalld1_vdcv` | MATRIX | 0.373 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Derivative Liabilities - Hedging, Supplemental |
| 1976 | `fnd23_intfvalld1_eptv` | MATRIX | 0.372 | 其他 | 0 | — | — | — | UNUSABLE | Total Pension Expense |
| 1977 | `fnd23_annfvmfm2_imao` | MATRIX | 0.372 | 宏观与行业 | 0 | — | — | — | UNUSABLE | When the Indirect Method is utilized, and the company delineates amortization and depreciation separately, the amortizat |
| 1978 | `fnd23_annfv1a_imao` | MATRIX | 0.372 | 宏观与行业 | 0 | — | — | — | UNUSABLE | When the Indirect Method is utilized, and the company delineates amortization and depreciation separately, the amortizat |
| 1979 | `fnd23_annfvalld1_otov` | MATRIX | 0.372 | 其他 | 0 | — | — | — | UNUSABLE | Other Tax |
| 1980 | `fnd23_intfvalld1_lvdv` | MATRIX | 0.371 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Non-Current Derivative Liabilities - Hedging, Supplemental |
| 1981 | `fnd23_annfvalld1_amae` | MATRIX | 0.371 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of capitalized acquisition costs or goodwill |
| 1982 | `fnd23_intfvalld1_bpol` | MATRIX | 0.369 | 其他 | 0 | — | — | — | UNUSABLE | Other payables |
| 1983 | `fnd23_intfvalld1_spev` | MATRIX | 0.367 | 其他 | 0 | — | — | — | UNUSABLE | Supplemental EPS |
| 1984 | `other_operating_assets` | MATRIX | 0.366 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other operating assets reported for the annual period. |
| 1985 | `fnd23_intfvm_odio` | MATRIX | 0.362 | 盈利与财务 | 0 | — | — | — | UNUSABLE | is applicable only if Net Income/Starting Line is income after gains/losses from discontinued operations. |
| 1986 | `interest_due_other` | MATRIX | 0.362 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Discontinued Operations |
| 1987 | `fnd23_intfvalld1_uaiv` | MATRIX | 0.361 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Impairment-Assets Held for Use, Supplemental |
| 1988 | `fnd23_intfvalld1_algv` | MATRIX | 0.361 | 盈利与财务 | 0 | — | — | — | UNUSABLE | (Gain) Loss on Sale of Assets, Supplemental |
| 1989 | `fnd23_annfvalld1_dsdv` | MATRIX | 0.360 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt Securities % - Domestic |
| 1990 | `fnd23_intfvalld1_ppdv` | MATRIX | 0.360 | 其他 | 0 | — | — | — | UNUSABLE | Domestic Pension Plan Expense |
| 1991 | `fnd23_intfvalld1_1spsd` | MATRIX | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Special DPS - Common Stock Primary Issue |
| 1992 | `fnd23_intfvm_tmaa` | MATRIX | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | accumulated intangible amortization. |
| 1993 | `accrued_amortization_total` | MATRIX | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Accumulated Intangible Amortization |
| 1994 | `fnd23_intfvalld1_pacv` | MATRIX | 0.358 | 其他 | 0 | — | — | — | UNUSABLE | Interest Capitalized, Supplemental |
| 1995 | `fnd23_annfvalld1_odix` | MATRIX | 0.357 | 其他 | 0 | — | — | — | UNUSABLE | Discontinued Operations. |
| 1996 | `fnd23_annfvalld1_otcv` | MATRIX | 0.356 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Other |
| 1997 | `valuation_market_adjustment_amount` | MATRIX | 0.355 | 其他 | 0 | — | — | — | UNUSABLE | Amount of market adjustment made to valuation. |
| 1998 | `fnd23_annfv1a_eros` | MATRIX | 0.355 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other Revenue, Total. |
| 1999 | `fnd23_intfvm_niie` | MATRIX | 0.355 | 其他 | 0 | — | — | — | UNUSABLE | interest income from operating section. |
| 2000 | `income_from_investments` | MATRIX | 0.354 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Income - Operating |
| 2001 | `fnd23_intfvalld1_vdav` | MATRIX | 0.353 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Advertising Expense - Supplemental represents the total cost of advertising incurred by the company. |
| 2002 | `fnd23_intfvm_verr` | MATRIX | 0.353 | 盈利与财务 | 0 | — | — | — | UNUSABLE | gross revenue. |
| 2003 | `revenue_total_2` | MATRIX | 0.353 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Gross Revenue |
| 2004 | `fnd23_annfvalld1_rpts` | MATRIX | 0.350 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Other Expense represents the total amount of other expenses on all of a company's pension and post-retirement |
| 2005 | `fnd23_intfvalld1_2dls` | MATRIX | 0.349 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Year 9 |
| 2006 | `fnd23_intfvalld1_32dls` | MATRIX | 0.349 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Years 2 and 3 represents the summation of Standardized Long Term Debt Maturing i |
| 2007 | `fnd23_intfvalld1_serv` | MATRIX | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Restructuring Charge, Supplemental |
| 2008 | `fnd23_intfvalld1_spts` | MATRIX | 0.348 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Service Cost |
| 2009 | `allowance_for_investment_writeoff` | MATRIX | 0.347 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories - Work In Progress |
| 2010 | `fnd23_intfvm_trsr` | MATRIX | 0.347 | 价量与波动 | 0 | — | — | — | UNUSABLE | sales returns and allowances. |
| 2011 | `investments_in_working_process` | MATRIX | 0.347 | 其他 | 0 | — | — | — | UNUSABLE | inventories that are WIP or work-in-progress. |
| 2012 | `short_term_receivables_total` | MATRIX | 0.347 | 价量与波动 | 0 | — | — | — | UNUSABLE | [Quarterly] Sales Returns and Allowances |
| 2013 | `fnd23_intfvalld1_dcsv` | MATRIX | 0.346 | 其他 | 0 | — | — | — | UNUSABLE | Service Cost - Domestic |
| 2014 | `fnd23_annfv1a_odio` | MATRIX | 0.346 | 盈利与财务 | 0 | — | — | — | UNUSABLE | is applicable only if Net Income/Starting Line is income after gains/losses from discontinued operations. |
| 2015 | `cash_and_marketable_equivalents_annual` | MATRIX | 0.346 | 盈利与财务 | 0 | — | — | — | UNUSABLE | miscellaneous earnings adjustment. |
| 2016 | `fnd23_blsm_mocq` | MATRIX | 0.346 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Comprehensive Income |
| 2017 | `common_stock_equity_2` | MATRIX | 0.345 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other comprehensive income. |
| 2018 | `fnd23_annfvalld1_dprv` | MATRIX | 0.345 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Pension Payment Rate - Domestic |
| 2019 | `fnd23_intfvalld1_ipts` | MATRIX | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Interest Cost |
| 2020 | `fnd23_intfvalld1_ddrv` | MATRIX | 0.345 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Discount Rate - Domestic |
| 2021 | `cash_and_equivalents_3` | MATRIX | 0.345 | 其他 | 0 | — | — | — | UNUSABLE | Total cash and cash equivalents held at the end of the period. |
| 2022 | `extraordinary_items_total_5` | MATRIX | 0.344 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Excise Tax Payments |
| 2023 | `fnd23_intfvm_txer` | MATRIX | 0.344 | 其他 | 0 | — | — | — | UNUSABLE | represents government-levied taxes on the manufacture, sale, or consumption of goods and services, which are included in |
| 2024 | `fnd23_intfvalld1_dciv` | MATRIX | 0.343 | 其他 | 0 | — | — | — | UNUSABLE | Interest Cost - Domestic |
| 2025 | `fnd23_annfvalld1_tius` | MATRIX | 0.342 | 其他 | 0 | — | — | — | UNUSABLE | Non-Recurring Items, Total |
| 2026 | `fnd23_intfvm_tmas` | MATRIX | 0.341 | 其他 | 0 | — | — | — | UNUSABLE | amortization representes sum of amortization of intangibles, amortization of acquisition costs, amortization of deferred |
| 2027 | `amortization_total` | MATRIX | 0.341 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Amortization |
| 2028 | `fnd23_intfvm_txee` | MATRIX | 0.340 | 其他 | 0 | — | — | — | UNUSABLE | Excise taxes payment including Sales taxes, value-added tax (VAT) and other excise taxes reported within the cost of goo |
| 2029 | `extraordinary_items_3` | MATRIX | 0.340 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Excise Taxes Payments |
| 2030 | `fnd23_annfvalld1_odrv` | MATRIX | 0.339 | 价量与波动 | 0 | — | — | — | UNUSABLE | Expected Rate of Return - Domestic |
| 2031 | `fnd23_intfvalld1_epts` | MATRIX | 0.339 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total Plan Expected Return |
| 2032 | `fnd23_intfvalld1_dpxv` | MATRIX | 0.338 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected Return on Plan Assets - Domestic |
| 2033 | `fnd23_intfvm_wdre` | MATRIX | 0.338 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | The portion of acquired in-process research and development costs (IPR&D) that was directly expensed in the income state |
| 2034 | `rewards_expense` | MATRIX | 0.338 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Purchased R&D Written-Off |
| 2035 | `net_income_after_tax_stpe` | MATRIX | 0.338 | 价量与波动 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Plan Expected Return |
| 2036 | `total_premiums_expensed` | MATRIX | 0.338 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total Plan Expected Return |
| 2037 | `fnd23_annfvalld1_dixv` | MATRIX | 0.338 | 其他 | 0 | — | — | — | UNUSABLE | Other Investments % - Domestic |
| 2038 | `fnd23_intfvalld1_artx` | MATRIX | 0.337 | 其他 | 0 | — | — | — | UNUSABLE | Extraordinary Item. |
| 2039 | `fnd23_intfvalld1_saoo` | MATRIX | 0.336 | 其他 | 0 | — | — | — | UNUSABLE | Accrued interest income for companies other than financial service companies. |
| 2040 | `fnd23_annfvalld1_eror` | MATRIX | 0.336 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other revenue. |
| 2041 | `fnd23_intfvalld1_rpts` | MATRIX | 0.336 | 其他 | 0 | — | — | — | UNUSABLE | Total Plan Other Expense represents the total amount of other expenses on all of a company's pension and post-retirement |
| 2042 | `fnd23_annfvalld1_drev` | MATRIX | 0.335 | 价量与波动 | 0 | — | — | — | UNUSABLE | Expected Rate of Return - Domestic |
| 2043 | `fnd23_intfvalld1_yppa` | MATRIX | 0.334 | 其他 | 0 | — | — | — | UNUSABLE | prepaid expenses. |
| 2044 | `fnd23_intfvalld1_opxv` | MATRIX | 0.334 | 其他 | 0 | — | — | — | UNUSABLE | Other Pension, Net - Domestic |
| 2045 | `fnd23_icsm_m_nnin` | MATRIX | 0.332 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Interest Income (Expense), Net |
| 2046 | `fnd23_intfvalld1_nicv` | MATRIX | 0.332 | 其他 | 0 | — | — | — | UNUSABLE | Interest Expense (Financial Operating), Supplemental |
| 2047 | `net_income_noncontrolling` | MATRIX | 0.332 | 其他 | 0 | — | — | — | UNUSABLE | Interest expense that is reduced by interest income. |
| 2048 | `fnd23_intfvalld1_3spdd` | MATRIX | 0.330 | 盈利与财务 | 0 | — | — | — | UNUSABLE | common dividends per share for common stock issue 2. |
| 2049 | `fnd23_intfvalld1_dcdv` | MATRIX | 0.330 | 其他 | 0 | — | — | — | UNUSABLE | Defined Contribution Expense - Domestic |
| 2050 | `retirement_benefit_cost` | MATRIX | 0.330 | 宏观与行业 | 0 | — | — | — | UNUSABLE | [Quarterly] Compensation Rate - Domestic |
| 2051 | `retirement_benefit_expense` | MATRIX | 0.330 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Compensation Rate – Domestic |
| 2052 | `fnd23_intfvalld1_dtrv` | MATRIX | 0.329 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Compensation Rate - Domestic |
| 2053 | `fnd23_intfvalld1_ftdv` | MATRIX | 0.328 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax - Foreign |
| 2054 | `accumulated_depreciation_other_assets` | MATRIX | 0.328 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets classified as discontinued operations |
| 2055 | `fnd23_intfvalld1_ltcv` | MATRIX | 0.326 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Local |
| 2056 | `fnd23_intfvalld1_titv` | MATRIX | 0.326 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Income Tax by Region - Total |
| 2057 | `fnd23_intfvalld1_tftv` | MATRIX | 0.326 | 其他 | 0 | — | — | — | UNUSABLE | Foreign Tax |
| 2058 | `fnd23_intfvalld1_tdtv` | MATRIX | 0.326 | 其他 | 0 | — | — | — | UNUSABLE | Domestic Tax |
| 2059 | `fnd23_intfvalld1_sptv` | MATRIX | 0.325 | 其他 | 0 | — | — | — | UNUSABLE | Prior Service Cost - Domestic |
| 2060 | `fnd23_intfvalld1_nicn` | MATRIX | 0.324 | 其他 | 0 | — | — | — | UNUSABLE | Non-operating interest capitalized. |
| 2061 | `fnd23_intfvalld1_gaxv` | MATRIX | 0.324 | 其他 | 0 | — | — | — | UNUSABLE | Actuarial Gains and Losses - Domestic |
| 2062 | `expense_paid_in_advance` | MATRIX | 0.324 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected Return on Plan Assets - Domestic |
| 2063 | `extraordinary_losses` | MATRIX | 0.324 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Expected Return on Assets - Domestic |
| 2064 | `fnd23_intfvalld1_tcxv` | MATRIX | 0.324 | 其他 | 0 | — | — | — | UNUSABLE | Curtailments and Settlements - Domestic |
| 2065 | `fnd23_annfvalld1_dvrv` | MATRIX | 0.323 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Pension Payment Rate - Domestic |
| 2066 | `fnd23_intfvalld1_ftov` | MATRIX | 0.322 | 其他 | 0 | — | — | — | UNUSABLE | Foreign Tax - Other |
| 2067 | `fnd23_intfvalld1_tisx` | MATRIX | 0.322 | 其他 | 0 | — | — | — | UNUSABLE | Tax on Extraordinary Items |
| 2068 | `fnd23_intfvalld1_dtov` | MATRIX | 0.321 | 其他 | 0 | — | — | — | UNUSABLE | Domestic Tax - Other |
| 2069 | `fnd23_annfvalld1_opxv` | MATRIX | 0.321 | 其他 | 0 | — | — | — | UNUSABLE | Other Pension, Net - Domestic |
| 2070 | `bank_acceptances_payable` | MATRIX | 0.320 | 其他 | 0 | — | — | — | UNUSABLE | represents the gross amount of buildings and their attachments, before being reduced by accumulated depreciation of the |
| 2071 | `fnd23_blsm_cbpa` | MATRIX | 0.320 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Buildings Gross |
| 2072 | `fnd23_intfvalld1_ltdv` | MATRIX | 0.320 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax - Local |
| 2073 | `fnd23_intfvalld1_dvrv` | MATRIX | 0.320 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Pension Payment Rate - Domestic |
| 2074 | `fnd23_intfvalld1_qftm` | MATRIX | 0.319 | 其他 | 0 | — | — | — | UNUSABLE | Retail Sales represents the total value of sales at retail locations (physical stores) during the period. |
| 2075 | `fnd23_intfvalld1_dbtm` | MATRIX | 0.319 | 其他 | 0 | — | — | — | UNUSABLE | Comparable Store Sales Growth, Retail, Total - % |
| 2076 | `fnd23_intfvalld1_ifpv` | MATRIX | 0.318 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Income After Stock-Based Compensation Expense |
| 2077 | `fnd23_intfvalld1_saiv` | MATRIX | 0.318 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Impairment-Assets Held for Sale, Supplemental |
| 2078 | `fnd23_intfvalld1_veev` | MATRIX | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | Pro Forma Stock Compensation Expense represents employee compensation paid in the form of stock options that have not ye |
| 2079 | `fnd23_intfvalld1_nirv` | MATRIX | 0.318 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Revenues |
| 2080 | `fnd23_intfvalld1_tile` | MATRIX | 0.318 | 其他 | 0 | — | — | — | UNUSABLE | litigation costs. These are non-recurring/unusual items reported within the cost of goods and services sold. |
| 2081 | `fnd23_intfvalld1_bfpv` | MATRIX | 0.318 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Basic EPS after Stock-Based Compensation Expense represents Net Income after Stock-Based Compensation Expense divided by |
| 2082 | `fnd23_intfvalld1_dfpv` | MATRIX | 0.318 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Diluted EPS After Stock-Based Compensation Expense represents Net Income After Stock-Based Compensation Expense plus the |
| 2083 | `fnd23_intfvalld1_oeis` | MATRIX | 0.317 | 其他 | 0 | — | — | — | UNUSABLE | Interest Expense, Net - Operating |
| 2084 | `fnd23_intfvalld1_xeie` | MATRIX | 0.317 | 其他 | 0 | — | — | — | UNUSABLE | interest expense. |
| 2085 | `contractual_debt_expense` | MATRIX | 0.317 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Tax – Domestic |
| 2086 | `fnd23_icsm_m_dtcv` | MATRIX | 0.317 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Current Tax - Domestic |
| 2087 | `fnd23_intfvalld1_dpgc` | MATRIX | 0.316 | 其他 | 0 | — | — | — | UNUSABLE | General Partners' Distributions |
| 2088 | `fnd23_intfvalld1_totv` | MATRIX | 0.316 | 其他 | 0 | — | — | — | UNUSABLE | Other Tax |
| 2089 | `fnd23_icsm_m_darv` | MATRIX | 0.316 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | [Quarterly] Research & Development Expense, Supplemental |
| 2090 | `advertising_and_promotion_expense` | MATRIX | 0.316 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement classified as Research & Development Expense, S |
| 2091 | `fnd23_intfvalld1_vdae` | MATRIX | 0.316 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | advertising expense reported outside the cost of goods and services sold |
| 2092 | `fnd23_intfvalld1_odrv` | MATRIX | 0.315 | 价量与波动 | 0 | — | — | — | UNUSABLE | Expected Rate of Return - Domestic |
| 2093 | `fnd23_intfvalld1_tmas` | MATRIX | 0.315 | 其他 | 0 | — | — | — | UNUSABLE | Amortization represents sum of amortization of intangibles, amortization of acquisition costs, amortization of deferred |
| 2094 | `fnd23_intfvalld1_eprv` | MATRIX | 0.315 | 其他 | 0 | — | — | — | UNUSABLE | Post-Retirement Plan Expense |
| 2095 | `fnd23_intfvalld1_tnir` | MATRIX | 0.315 | 其他 | 0 | — | — | — | UNUSABLE | interest income. |
| 2096 | `fnd23_intfvm_graa` | MATRIX | 0.314 | 盈利与财务 | 0 | — | — | — | UNUSABLE | gross accounts receivable from sales of trading assets such as inventories or from services provided. |
| 2097 | `accrued_assets_reserve_gross` | MATRIX | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Accounts Receivable - Trade, Gross |
| 2098 | `fnd23_annfvalld1_sere` | MATRIX | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Restructuring Charge is an unusual or non-recurring item related to a significant rearrangement of a company's assets an |
| 2099 | `fnd23_intfvalld1_fdrv` | MATRIX | 0.312 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Discount Rate - Foreign |
| 2100 | `fnd23_intfvalld1_ndsf` | MATRIX | 0.311 | 盈利与财务 | 0 | — | — | — | UNUSABLE | If short-term debt issuances and reductions are not delineated separately, the total is classified as short-term debt, n |
| 2101 | `fnd23_intfvalld1_ppfv` | MATRIX | 0.311 | 其他 | 0 | — | — | — | UNUSABLE | Foreign Pension Plan Expense |
| 2102 | `fnd23_intfvalld1_lbtm` | MATRIX | 0.311 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Merchandise Margins, Total - % |
| 2103 | `fnd23_intfvalld1_cspv` | MATRIX | 0.310 | 其他 | 0 | — | — | — | UNUSABLE | Service Cost - Post-Retirement |
| 2104 | `fnd23_intfvalld1_csfv` | MATRIX | 0.310 | 其他 | 0 | — | — | — | UNUSABLE | Service Cost |
| 2105 | `fnd23_intfvalld1_cifv` | MATRIX | 0.310 | 其他 | 0 | — | — | — | UNUSABLE | Interest Cost - Foreign |
| 2106 | `amortization_intangible_assets_3` | MATRIX | 0.309 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Amortization of Intangibles |
| 2107 | `fnd23_intfvm_imao` | MATRIX | 0.309 | 宏观与行业 | 0 | — | — | — | UNUSABLE | When the Indirect Method is utilized, and the company delineates amortization and depreciation separately, the amortizat |
| 2108 | `fnd23_intfvalld1_cipv` | MATRIX | 0.309 | 其他 | 0 | — | — | — | UNUSABLE | Interest Cost - Post-Retirement |
| 2109 | `fnd23_intfvalld1_ftrv` | MATRIX | 0.309 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Compensation Rate - Foreign |
| 2110 | `fnd23_intfvalld1_csxv` | MATRIX | 0.309 | 其他 | 0 | — | — | — | UNUSABLE | Prior Service Cost |
| 2111 | `fnd23_intfvalld1_acfn` | MATRIX | 0.308 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Foreign Currency Translation Adjustment |
| 2112 | `fnd23_intfvalld1_epxv` | MATRIX | 0.308 | 其他 | 0 | — | — | — | UNUSABLE | Other Post-Retirement, Net |
| 2113 | `fnd23_intfvalld1_rxfv` | MATRIX | 0.308 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected Return on Assets - Foreign |
| 2114 | `fnd23_intfvm_3los` | MATRIX | 0.308 | 其他 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Year 3. |
| 2115 | `fnd23_intfvalld1_uatv` | MATRIX | 0.308 | 其他 | 0 | — | — | — | UNUSABLE | Audit Fees |
| 2116 | `lease_obligations_long_term` | MATRIX | 0.308 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 3 |
| 2117 | `fnd23_intfvalld1_laxv` | MATRIX | 0.308 | 其他 | 0 | — | — | — | UNUSABLE | Actuarial Gains and Losses - Post-Retirement |
| 2118 | `fnd23_cf_m_saoo` | MATRIX | 0.307 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Assets |
| 2119 | `income_tax_expense_3` | MATRIX | 0.307 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Total Extraordinary Items |
| 2120 | `other_operating_assets_2` | MATRIX | 0.307 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accrued interest income for companies other than financial service companies. |
| 2121 | `special_items_income` | MATRIX | 0.307 | 其他 | 0 | — | — | — | UNUSABLE | Total Extraordinary Items |
| 2122 | `fnd23_intfvm2_cpoa` | MATRIX | 0.307 | 其他 | 0 | — | — | — | UNUSABLE | Other Properties/Plant/Equipment – Gross |
| 2123 | `fnd23_intfvalld1_rtxv` | MATRIX | 0.307 | 其他 | 0 | — | — | — | UNUSABLE | Transition Costs - Domestic |
| 2124 | `fnd23_intfvalld1_scxv` | MATRIX | 0.307 | 其他 | 0 | — | — | — | UNUSABLE | Curtailments & Settlements - Post-Retirement |
| 2125 | `fnd23_intfvalld1_cyfv` | MATRIX | 0.307 | 其他 | 0 | — | — | — | UNUSABLE | Curtailments & Settlements - Foreign |
| 2126 | `fnd23_intfvalld1_egrm` | MATRIX | 0.307 | 其他 | 0 | — | — | — | UNUSABLE | Net Operating Income (NOI) |
| 2127 | `long_term_debt_current_liabilities` | MATRIX | 0.306 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Discontinued Operations – Current Liability |
| 2128 | `fnd23_intfvalld1_ayfv` | MATRIX | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Actuarial Gains and Losses - Foreign |
| 2129 | `fnd23_intfvalld1_fcdv` | MATRIX | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Defined Contribution Expense - Foreign |
| 2130 | `fnd23_intfvalld1_fvrv` | MATRIX | 0.306 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Pension Payment Rate - Foreign |
| 2131 | `fnd23_intfvalld1_ptfv` | MATRIX | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Prior Service Cost - Foreign |
| 2132 | `fnd23_intfvalld1_rcdv` | MATRIX | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Defined Contribution Expense Post-Retirement |
| 2133 | `fnd23_intfvalld1_fcpv` | MATRIX | 0.306 | 其他 | 0 | — | — | — | UNUSABLE | Other Pension, Net - Foreign |
| 2134 | `fnd23_intfvalld1_ofrv` | MATRIX | 0.306 | 价量与波动 | 0 | — | — | — | UNUSABLE | Expected Rate of Return - Foreign |
| 2135 | `fnd23_intfvalld1_kgim` | MATRIX | 0.305 | 盈利与财务 | 0 | — | — | — | UNUSABLE | New Business Profit represents the contribution of the total new business sales of an insurer during the period. |
| 2136 | `fnd23_intfvalld1_mdrv` | MATRIX | 0.305 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Discount Rate - Post-Retirement |
| 2137 | `fnd23_intfvalld1_ctxv` | MATRIX | 0.305 | 其他 | 0 | — | — | — | UNUSABLE | Transition Costs - Post-Retirement |
| 2138 | `fnd23_intfvalld1_oinm` | MATRIX | 0.305 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Interest Margin, Total -% |
| 2139 | `fnd23_intfvalld1_fbtm` | MATRIX | 0.304 | 其他 | 0 | — | — | — | UNUSABLE | Comparable Store Sales, Retail (Value) |
| 2140 | `fnd23_intfvalld1_ogim` | MATRIX | 0.304 | 其他 | 0 | — | — | — | UNUSABLE | New Business Annual Premium Equiv. represents the annual premium amount for regular premium contracts plus 10% of new si |
| 2141 | `fnd23_intfvalld1_lbim` | MATRIX | 0.303 | 其他 | 0 | — | — | — | UNUSABLE | Combined Ratio, Total - %. It shows the combination of the loss ratio and the expense ratio, and is an indicator of the |
| 2142 | `fnd23_intfvalld1_ggom` | MATRIX | 0.303 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Oil Equivalent Production (Barrels/Day) |
| 2143 | `fnd23_intfvalld1_kbom` | MATRIX | 0.303 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Crude Oil Production (Barrels) |
| 2144 | `fnd23_intfvalld1_zbim` | MATRIX | 0.303 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Underwriting Profit or Loss represents the money earned or lost by an insurer in its underwriting operations. |
| 2145 | `fnd23_intfvalld1_ghtm` | MATRIX | 0.303 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Online Sales represents the total value of sales generated over the Internet during the period. |
| 2146 | `fnd23_intfvalld1_ogom` | MATRIX | 0.302 | 其他 | 0 | — | — | — | UNUSABLE | Exploration and Development Costs represents the exploration and development costs incurred by the company for feasibili |
| 2147 | `fnd23_intfvalld1_fotv` | MATRIX | 0.302 | 其他 | 0 | — | — | — | UNUSABLE | All Other Fees Paid to Auditor |
| 2148 | `fnd23_intfvalld1_acda` | MATRIX | 0.302 | 盈利与财务 | 0 | — | — | — | UNUSABLE | current assets of discontinued operations. |
| 2149 | `fnd23_annfvalld1_ftcv` | MATRIX | 0.302 | 其他 | 0 | — | — | — | UNUSABLE | Current Tax - Foreign |
| 2150 | `fnd23_intfvalld1_kgps` | MATRIX | 0.302 | 其他 | 0 | — | — | — | UNUSABLE | Gold Production (Troy Ounces) |
| 2151 | `fnd23_intfvm_pxto` | MATRIX | 0.302 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in taxes payable during the period. An increase in income taxes payable has a positive impact on cash |
| 2152 | `tax_payable_2` | MATRIX | 0.302 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Taxes Payable |
| 2153 | `fnd23_intfvalld1_fbim` | MATRIX | 0.301 | 其他 | 0 | — | — | — | UNUSABLE | Expense Ratio, Total - %. It shows the sum of the acquisition costs and other underwriting expenses in relation to the p |
| 2154 | `fnd23_intfvalld1_hbim` | MATRIX | 0.301 | 其他 | 0 | — | — | — | UNUSABLE | Loss Ratio, Total - %. It shows the loss expenses incurred by an insurance company in relation to the total premiums ear |
| 2155 | `deferred_tax_liabilities_long_term` | MATRIX | 0.301 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Pymts. Due in 4-5 Years |
| 2156 | `fnd23_intfvm_4los` | MATRIX | 0.301 | 其他 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Year 4. |
| 2157 | `fnd23_intfvm_54los` | MATRIX | 0.301 | 其他 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Years 4 and 5 represents the summation of Standardized Operating Lease Paym |
| 2158 | `pension_liabilities_long_term` | MATRIX | 0.301 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 4 |
| 2159 | `fnd23_intfvalld1_tilv` | MATRIX | 0.301 | 其他 | 0 | — | — | — | UNUSABLE | Litigation Charge, Supplemental |
| 2160 | `fnd23_intfvalld1_rgim` | MATRIX | 0.300 | 盈利与财务 | 0 | — | — | — | UNUSABLE | New Business Margin, Total - %. It shows the profit from new business sales, expressed as a percentage of the present va |
| 2161 | `fnd23_intfvalld1_ebom` | MATRIX | 0.300 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Crude Oil, Average Production (Barrels/Day) |
| 2162 | `fnd23_intfvalld1_hbom` | MATRIX | 0.300 | 价量与波动 | 0 | — | — | — | UNUSABLE | Crude Oil, Average Sales Price per Barrel, Total |
| 2163 | `fnd23_intfvalld1_ppov` | MATRIX | 0.300 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reported Operating Profit |
| 2164 | `fnd23_intfvalld1_prgv` | MATRIX | 0.300 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reported Gross Profit |
| 2165 | `fnd23_intfvalld1_odps` | MATRIX | 0.300 | 其他 | 0 | — | — | — | UNUSABLE | Copper Production (Metric Tons) |
| 2166 | `fnd23_intfvalld1_kgas` | MATRIX | 0.300 | 价量与波动 | 0 | — | — | — | UNUSABLE | Gold, Average Price per Troy Ounce captures the average selling price of gold per troy ounce during the specified period |
| 2167 | `fnd23_intfvalld1_ebrm` | MATRIX | 0.299 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | FFO per Share (Basic) Funds from Operations (FFO) divided by the basic weighted average shares for the period. |
| 2168 | `fnd23_intfvalld1_ebbm` | MATRIX | 0.298 | 其他 | 0 | — | — | — | UNUSABLE | Passengers, Total represents the number of persons on board a flight who is not a member of the flight or cabin crew. |
| 2169 | `fnd23_intfvalld1_gbrm` | MATRIX | 0.298 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Adjusted FFO (AFFO) represents Funds from Operations (FFO) adjusted for unusual and/or extraordinary items. |
| 2170 | `fnd23_intfvalld1_zdpm` | MATRIX | 0.298 | 其他 | 0 | — | — | — | UNUSABLE | Diamond Production (Carats) |
| 2171 | `fnd23_intfvalld1_cbbm` | MATRIX | 0.298 | 盈利与财务 | 0 | — | — | — | UNUSABLE | EBITDAR represents earnings before interest, taxes, depreciation, amortization, and obsolescence and aircraft rent. |
| 2172 | `fnd23_intfvalld1_gdas` | MATRIX | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Copper, Average Price per Metric Ton captures the average selling price of copper per metric ton during the specified pe |
| 2173 | `fnd23_intfvalld1_gips` | MATRIX | 0.298 | 其他 | 0 | — | — | — | UNUSABLE | Iron Ore Production (Metric Tons) |
| 2174 | `fnd23_intfvalld1_htrm` | MATRIX | 0.298 | 其他 | 0 | — | — | — | UNUSABLE | Rent Growth (Sequential), Total -% |
| 2175 | `fnd23_annfvalld1_imao` | MATRIX | 0.298 | 宏观与行业 | 0 | — | — | — | UNUSABLE | When the Indirect Method is utilized, and the company delineates amortization and depreciation separately, the amortizat |
| 2176 | `fnd23_intfvalld1_fttv` | MATRIX | 0.298 | 其他 | 0 | — | — | — | UNUSABLE | Tax Fees |
| 2177 | `fnd23_intfvalld1_gbbm` | MATRIX | 0.298 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | represents the total number of paying passengers flown on all flight segments. |
| 2178 | `fnd23_intfvalld1_qfbm` | MATRIX | 0.298 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of Trips Flown (Departures) represents the number of takeoffs made at an airport. |
| 2179 | `fnd23_intfvalld1_ratv` | MATRIX | 0.298 | 其他 | 0 | — | — | — | UNUSABLE | Audit-Related Fees |
| 2180 | `fnd23_intfvalld1_oahm` | MATRIX | 0.298 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Property-Level EBITDA |
| 2181 | `fnd23_intfvalld1_odos` | MATRIX | 0.298 | 价量与波动 | 0 | — | — | — | UNUSABLE | Natural Gas, Average Sales Price per Cu.Mt. |
| 2182 | `fnd23_intfvalld1_krbm` | MATRIX | 0.298 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Number of Hours Flown represents the block hours or the number of hours which elapsed between the time the aircraft star |
| 2183 | `fnd23_intfvalld1_gehm` | MATRIX | 0.298 | 其他 | 0 | — | — | — | UNUSABLE | Number of outpatient visits represents the number of individual visits to hospital outpatient departments located on the |
| 2184 | `fnd23_intfvalld1_inum` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Number of Units Sold represents the number of products sold by the electronics company. |
| 2185 | `fnd23_intfvalld1_ksps` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Silver Production (Troy Ounces) |
| 2186 | `fnd23_intfvalld1_zbom` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Gas Liquids Production (Barrels) |
| 2187 | `fnd23_intfvalld1_zlbm` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Average Number of Operating Aircraft |
| 2188 | `fnd23_intfvalld1_gzps` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Zinc Production (Metric Tons) |
| 2189 | `fnd23_intfvalld1_gbtm` | MATRIX | 0.297 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Traffic (Number of Customer Visits) represents the total number of customer visits to all of the company's stores during |
| 2190 | `fnd23_annfv1a_pxto` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in taxes payable during the period. An increase in income taxes payable has a positive impact on cash |
| 2191 | `fnd23_intfvalld1_fbrm` | MATRIX | 0.297 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | FFO per share (diluted) represents funds from operations (FFO) divided by the diluted weighted average shares for the pe |
| 2192 | `fnd23_intfvalld1_ekim` | MATRIX | 0.297 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Number of Page Views (User Traffic) represents the number of hits (page views) that a website has received over the spec |
| 2193 | `fnd23_intfvalld1_gdos` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Natural Gas, Average Prod. (Cu. Meters/Day) |
| 2194 | `fnd23_intfvalld1_gkim` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Value of Paid Clicks represents the total sales resulting from the click-paid activity for an Internet media company. |
| 2195 | `fnd23_intfvalld1_eghm` | MATRIX | 0.297 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Inpatient Revenues represents the total billed value for the services provided by the hospital to its inpatients. |
| 2196 | `fnd23_intfvalld1_fvrm` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Comp. Store Sales, Restaurants (Value) |
| 2197 | `fnd23_intfvalld1_gghm` | MATRIX | 0.297 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net Outpatient Revenues represents the total billed value for the services provided by the hospital to its outpatients. |
| 2198 | `fnd23_intfvalld1_lbrm` | MATRIX | 0.297 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Adjusted FFO per share (diluted) represents adjusted funds from operations (AFFO) divided by the diluted weighted averag |
| 2199 | `fnd23_intfvalld1_etrs` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | Average Rent per Square Meter |
| 2200 | `fnd23_annfv1a_dare` | MATRIX | 0.297 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement. |
| 2201 | `fnd23_intfvalld1_kbrm` | MATRIX | 0.297 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Adjusted FFO per Share (Basic) represents Adjusted Funds from Operations (AFFO) divided by the basic weighted average sh |
| 2202 | `fnd23_intfvalld1_fahm` | MATRIX | 0.296 | 其他 | 0 | — | — | — | UNUSABLE | Occupancy, Total - %. It shows the percentage of rooms that are occupied or rented in a hotel at a given time. |
| 2203 | `fnd23_intfvalld1_lgun` | MATRIX | 0.296 | 其他 | 0 | — | — | — | UNUSABLE | Unrealized Gains (Losses) |
| 2204 | `fnd23_intfvalld1_ksas` | MATRIX | 0.296 | 价量与波动 | 0 | — | — | — | UNUSABLE | Silver, average price per troy ounce captures the average selling price of silver per troy ounce during the specified pe |
| 2205 | `fnd23_intfvalld1_zdos` | MATRIX | 0.296 | 其他 | 0 | — | — | — | UNUSABLE | Natural Gas Production (Cubic Meters) |
| 2206 | `fnd23_intfvalld1_hvrm` | MATRIX | 0.296 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Margin, Total -% |
| 2207 | `fnd23_intfvalld1_zpas` | MATRIX | 0.296 | 价量与波动 | 0 | — | — | — | UNUSABLE | Platinum, Average Price per Troy Ounce captures the average selling price of Platinum per Troy Ounce during the specifie |
| 2208 | `fnd23_intfvalld1_kahm` | MATRIX | 0.296 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue per Available Room (REVPAR), Total |
| 2209 | `fnd23_intfvalld1_dvrm` | MATRIX | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Comp. Store Sales, Restaurants, Total - % |
| 2210 | `fnd23_intfvalld1_lgom` | MATRIX | 0.295 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Production Growth, Total - % for oil and gas companies. |
| 2211 | `fnd23_intfvalld1_fgom` | MATRIX | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Average Production Costs per Barrel, Total |
| 2212 | `fnd23_intfvalld1_hahm` | MATRIX | 0.295 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Average Daily Room Rate (ADR), Total. Represents the company-level average rental income per occupied room in a given ti |
| 2213 | `fnd23_intfvalld1_ldbm` | MATRIX | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Load Factor, Total - % represents the company-level Load Factor percentage that is reported by the company. It represent |
| 2214 | `fnd23_intfvalld1_qbbs` | MATRIX | 0.295 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue Passengers Kilometers (RPK) captures the total distance flown by the airline's revenue passengers in kilometers. |
| 2215 | `fnd23_intfvalld1_zdts` | MATRIX | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Average Sales per Square Meter |
| 2216 | `fnd23_intfvalld1_gdbs` | MATRIX | 0.295 | 价量与波动 | 0 | — | — | — | UNUSABLE | Available Seat Kilometers (ASK) captures the total flight passenger capacity of an airline in kilometers. |
| 2217 | `fnd23_intfvalld1_dtsl` | MATRIX | 0.295 | 盈利与财务 | 0 | — | — | — | UNUSABLE | notes payable/short term debt. |
| 2218 | `fnd23_intfvalld1_zpps` | MATRIX | 0.295 | 其他 | 0 | — | — | — | UNUSABLE | Platinum Production (Troy Ounces) |
| 2219 | `fnd23_intfvalld1_gzas` | MATRIX | 0.295 | 价量与波动 | 0 | — | — | — | UNUSABLE | Zinc, average price per metric ton captures the average selling price of zinc per metric ton, during the specified perio |
| 2220 | `fnd23_intfvalld1_tinm` | MATRIX | 0.295 | 价量与波动 | 0 | — | — | — | UNUSABLE | Net Interest Spread, Total -% |
| 2221 | `fnd23_intfvm_5los` | MATRIX | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Standardized Operating Lease Payments Due in Year 5. |
| 2222 | `provisions_long_term` | MATRIX | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Operating Lease Payments Due in Year 5 |
| 2223 | `fnd23_intfvalld1_cdav` | MATRIX | 0.294 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred Revenue - Current |
| 2224 | `fnd23_intfvalld1_gfbs` | MATRIX | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Passenger Haul, Average Length (Kilometers) captures the average distance traveled by a scheduled fare-paying passenger |
| 2225 | `fnd23_intfvalld1_gias` | MATRIX | 0.294 | 价量与波动 | 0 | — | — | — | UNUSABLE | Iron Ore, Average Price per Metric Ton captures the average selling price of iron ore per metric ton during the specifie |
| 2226 | `fnd23_intfvalld1_gjbs` | MATRIX | 0.294 | 价量与波动 | 0 | — | — | — | UNUSABLE | Operating Expense per ASK captures the total operating expenses incurred per available seat kilometer of the airline. |
| 2227 | `fnd23_intfvalld1_zhbs` | MATRIX | 0.294 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Revenue per ASK captures the total operating revenues earned per available seat kilometer of the airline. |
| 2228 | `fnd23_intfvalld1_rlbm` | MATRIX | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Aircraft Utilization (Hours per Day), Total |
| 2229 | `fnd23_intfvalld1_wdrv` | MATRIX | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Purchased R&D Written-Off, Supplemental |
| 2230 | `fnd23_intfvalld1_ghbs` | MATRIX | 0.294 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Passenger Revenue per RPK captures the total passenger revenues earned per revenue passenger kilometer traveled by the a |
| 2231 | `fnd23_intfvalld1_obom` | MATRIX | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Gas Liquids, Average Production (Barrels/Day) |
| 2232 | `fnd23_intfvalld1_ojbs` | MATRIX | 0.294 | 价量与波动 | 0 | — | — | — | UNUSABLE | Operating Expense per ASK, excluding Fuel captures the total operating expenses, less aircraft fuel, incurred per availa |
| 2233 | `fnd23_intfvalld1_rbom` | MATRIX | 0.294 | 价量与波动 | 0 | — | — | — | UNUSABLE | Gas Liquids, Average Sales Price per Barrel, Total |
| 2234 | `fnd23_intfvalld1_agbm` | MATRIX | 0.294 | 其他 | 0 | — | — | — | UNUSABLE | Average Passenger Fare, Total |
| 2235 | `fnd23_annfv1a_eror` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | other revenue. |
| 2236 | `fnd23_intfvalld1_fnbm` | MATRIX | 0.293 | 其他 | 0 | — | — | — | UNUSABLE | Percentage of Sales - Internet, Total represents the company-level portion of sales that is made from the internet. |
| 2237 | `fnd23_intfvalld1_ofbs` | MATRIX | 0.293 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Aircraft stage, average length (kilometers) captures the average distance flown per flight of an airline in kilometers. |
| 2238 | `fnd23_intfvalld1_ohbs` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Passenger revenue per ASK captures the total passenger revenues earned per available seat kilometer of the airline. |
| 2239 | `fnd23_intfvalld1_hiim` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average Revenue per Customer, Total represents the company-level revenue generated by a customer per month, as reported |
| 2240 | `fnd23_intfvalld1_pghm` | MATRIX | 0.293 | 其他 | 0 | — | — | — | UNUSABLE | Utilization of Licensed Beds, Total - % represents the company level average utilization of the licensed beds during the |
| 2241 | `fnd23_intfvalld1_qdbs` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue per ASK captures the revenue earned by each available seat kilometer of an airline. This item is used as the lin |
| 2242 | `fnd23_intfvalld1_qtps` | MATRIX | 0.293 | 其他 | 0 | — | — | — | UNUSABLE | Titanium Slag Production (Metric Tons) |
| 2243 | `fnd23_intfvalld1_pdam` | MATRIX | 0.293 | 价量与波动 | 0 | — | — | — | UNUSABLE | Diamonds, Average Price per Carat, Total |
| 2244 | `fnd23_intfvalld1_verr` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | gross revenue. |
| 2245 | `fnd23_intfvalld1_hjhm` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Inpatient Revenue per Admission, Total represents the company-level average inpatient revenues earned by the hospital fo |
| 2246 | `fnd23_intfvalld1_ljhm` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Outpatient Revenue per Visit, Total represents the company-level average outpatient revenue earned by the hospital for e |
| 2247 | `fnd23_intfvalld1_pjhm` | MATRIX | 0.293 | 其他 | 0 | — | — | — | UNUSABLE | Average Length of Stay (Days), Total represents the company-level average number of days an admitted patient stays in th |
| 2248 | `fnd23_intfvalld1_rbrm` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | FFO Payout Ratio, Total - %. It shows the dividend payout rate from the Funds from Operations (FFO) for each share. |
| 2249 | `fnd23_intfvalld1_afhm` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue per Visit/Discharge/Case/Scan represents the company-level average revenue earned by the hospital for each visit |
| 2250 | `fnd23_annfvalld1_gaxv` | MATRIX | 0.293 | 其他 | 0 | — | — | — | UNUSABLE | Actuarial Gains and Losses - Domestic |
| 2251 | `fnd23_intfvalld1_elbs` | MATRIX | 0.293 | 其他 | 0 | — | — | — | UNUSABLE | Fuel Cost per Liter captures the unit cost of each liter of fuel consumed by the airline |
| 2252 | `fnd23_intfvalld1_inrv` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Reported Net Income After Tax |
| 2253 | `fnd23_intfvalld1_olbs` | MATRIX | 0.293 | 其他 | 0 | — | — | — | UNUSABLE | Fuel Consumed, Liters |
| 2254 | `fnd23_annfvalld1_otdv` | MATRIX | 0.292 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Tax - Other |
| 2255 | `fnd23_intfvalld1_pace` | MATRIX | 0.291 | 其他 | 0 | — | — | — | UNUSABLE | Interest Capitalized - Operating |
| 2256 | `fnd23_intfvalld1_niie` | MATRIX | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | interest income from operating section. |
| 2257 | `fnd23_annfvalld1_algn` | MATRIX | 0.289 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gain (Loss) on Sale of Assets. |
| 2258 | `fnd23_intfvm_cema` | MATRIX | 0.289 | 其他 | 0 | — | — | — | UNUSABLE | represents the acquisition cost of machinery and other equipment (including delivery equipment, office equipment, machin |
| 2259 | `mortgage_escrow_cash` | MATRIX | 0.289 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Machinery/Equipment - Gross |
| 2260 | `valuation_allowance_uncollected_debt` | MATRIX | 0.288 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Right-of-Use Assets - Capital Lease, Depreciation - Supplemental |
| 2261 | `valuation_unrealized_currency_difference` | MATRIX | 0.288 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Right-of-Use Assets - Capital Lease, Depreciation - Supplemental |
| 2262 | `fnd23_intfvalld1_trsr` | MATRIX | 0.286 | 价量与波动 | 0 | — | — | — | UNUSABLE | sales returns and allowances. |
| 2263 | `fnd23_intfvalld1_offh` | MATRIX | 0.285 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funds From Operations (REIT) |
| 2264 | `fnd23_annfvalld1_sptv` | MATRIX | 0.283 | 其他 | 0 | — | — | — | UNUSABLE | Prior Service Cost - Domestic |
| 2265 | `fnd23_intfvalld1_txer` | MATRIX | 0.282 | 其他 | 0 | — | — | — | UNUSABLE | represents government-levied taxes on the manufacture, sale, or consumption of goods and services, which are included in |
| 2266 | `fnd23_intfvalld1_vacl` | MATRIX | 0.281 | 其他 | 0 | — | — | — | UNUSABLE | Advances/deposits from customers for the products to be sold or services to be rendered classified as Customer Advances. |
| 2267 | `fnd23_intfvalld1_wdre` | MATRIX | 0.279 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | The portion of acquired in-process research and development costs (IPR&D) that was directly expensed in the income state |
| 2268 | `fnd23_intfvalld1_hsca` | MATRIX | 0.279 | 其他 | 0 | — | — | — | UNUSABLE | Cash represents cash on hand, balances on demand deposits, and near-term savings and time deposits. These should be read |
| 2269 | `fnd23_annfvalld1_dlav` | MATRIX | 0.278 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accrued Liabilities - Domestic |
| 2270 | `fnd23_intfvalld1_txee` | MATRIX | 0.278 | 其他 | 0 | — | — | — | UNUSABLE | Excise taxes payment including sales taxes, value-added tax (VAT), and other excise taxes reported within the cost of go |
| 2271 | `fnd23_annfvalld1_acda` | MATRIX | 0.276 | 盈利与财务 | 0 | — | — | — | UNUSABLE | current assets of discontinued operations. |
| 2272 | `fnd23_intfvalld1_ctpa` | MATRIX | 0.275 | 其他 | 0 | — | — | — | UNUSABLE | gross property, plant & equipment. |
| 2273 | `other_amortization_items` | MATRIX | 0.273 | 其他 | 0 | — | — | — | UNUSABLE | Other amortization items reported for the annual period. |
| 2274 | `fnd23_intfvalld1_lgue` | MATRIX | 0.272 | 其他 | 0 | — | — | — | UNUSABLE | Unrealized Losses (Gains) |
| 2275 | `fnd23_intfvalld1_olcl` | MATRIX | 0.272 | 其他 | 0 | — | — | — | UNUSABLE | Capital Lease Obligations |
| 2276 | `fnd23_intfvalld1_acfe` | MATRIX | 0.271 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Foreign Currency Translation Adjustment represents the adjustment required when a company has a foreign subsidiary that |
| 2277 | `fnd23_annfvalld1_ctda` | MATRIX | 0.271 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Represents deferred tax assets with a current maturity. When there is a timing difference between financial reporting an |
| 2278 | `fnd23_annfv1a_algn` | MATRIX | 0.271 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gain (Loss) on Sale of Assets. |
| 2279 | `fnd23_annfvalld1_bpdl` | MATRIX | 0.270 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends Payable |
| 2280 | `fnd23_annfvalld1_lguq` | MATRIX | 0.270 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Unrealized Gain (Loss) represents all unrealized/revaluation gains (losses) reported in the Equity section by a company. |
| 2281 | `fnd23_annfv1a_abpl` | MATRIX | 0.269 | 盈利与财务 | 0 | — | — | — | UNUSABLE | payable or accrued liabilities. |
| 2282 | `fnd23_annfvalld1_tcxv` | MATRIX | 0.267 | 其他 | 0 | — | — | — | UNUSABLE | Curtailments and Settlements - Domestic |
| 2283 | `fnd23_annfvalld1_saie` | MATRIX | 0.266 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Impairment/write-down/write-off/revaluation of investment securities arising from an unusual event. |
| 2284 | `fnd23_intfvm_abpl` | MATRIX | 0.265 | 盈利与财务 | 0 | — | — | — | UNUSABLE | payable or accrued liabilities. |
| 2285 | `payables_and_accruals` | MATRIX | 0.264 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Payable/Accrued |
| 2286 | `fnd23_intfvm_cila` | MATRIX | 0.260 | 其他 | 0 | — | — | — | UNUSABLE | represents land and improvements on land at acquisition cost. Land is not depreciated, but land improvements are normall |
| 2287 | `loans_insurance_companies` | MATRIX | 0.260 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Land/Improvements - Gross |
| 2288 | `earnings_from_residual_operations` | MATRIX | 0.256 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Restructuring Charge |
| 2289 | `equity_investment_income` | MATRIX | 0.256 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Restructuring Charge is an unusual or non-recurring item related to a significant rearrangement of a company’s assets an |
| 2290 | `fnd23_intfvalld1_odio` | MATRIX | 0.255 | 盈利与财务 | 0 | — | — | — | UNUSABLE | is applicable only if Net Income/Starting Line is income after gains/losses from discontinued operations. |
| 2291 | `fnd23_intfvm2_3dls` | MATRIX | 0.251 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long Term Debt Maturing in Year 3 |
| 2292 | `minority_interest_other_securities` | MATRIX | 0.243 | 其他 | 0 | — | — | — | UNUSABLE | Number of Common Shareholders |
| 2293 | `minority_ownership_shares` | MATRIX | 0.243 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | [Quarterly] Number of Common Shareholders |
| 2294 | `agricultural_expense` | MATRIX | 0.243 | 其他 | 0 | — | — | — | UNUSABLE | Actuarial Gains and Losses – Domestic |
| 2295 | `extraordinary_gains` | MATRIX | 0.243 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Actuarial Gains and Losses - Domestic |
| 2296 | `dividend_received_others` | MATRIX | 0.226 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected Rate of Return – Domestic |
| 2297 | `revenue_from_domestic_operations` | MATRIX | 0.226 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Expected Rate of Return - Domestic |
| 2298 | `operating_revenue_other` | MATRIX | 0.224 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Other Revenue, Total |
| 2299 | `other_operating_revenue` | MATRIX | 0.224 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other Revenue, Total. |
| 2300 | `insurance_premiums_subscribed` | MATRIX | 0.221 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Prior Service Cost - Domestic |
| 2301 | `total_premiums_subscribed` | MATRIX | 0.221 | 其他 | 0 | — | — | — | UNUSABLE | Prior Service Cost – Domestic |
| 2302 | `fnd23_annfv1a_vdav` | MATRIX | 0.198 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Advertising Expense - Supplemental represents the total cost of advertising incurred by the company. |
| 2303 | `earnings_from_associates` | MATRIX | 0.197 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Research & Development |
| 2304 | `research_and_development_income` | MATRIX | 0.197 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and development costs expensed directly in the income statement. |
| 2305 | `fnd23_intfvm2_4dls` | MATRIX | 0.195 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long Term Debt Maturing in Year 4 |
| 2306 | `fnd23_intfvm2_54dls` | MATRIX | 0.195 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Years 4 and 5 |
| 2307 | `valuation_allowance_deferred_tax_assets` | MATRIX | 0.189 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accrued Liabilities - Domestic |
| 2308 | `valuation_difference_amount` | MATRIX | 0.189 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Accrued Liabilities - Domestic |
| 2309 | `fnd23_intfvm2_5dls` | MATRIX | 0.189 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standardized Long Term Debt Maturing in Year 5 |
| 2310 | `fnd23_intfvm_adpa` | MATRIX | 0.188 | 其他 | 0 | — | — | — | UNUSABLE | represents provisions established for doubtful accounts receivable. Provision for doubtful accounts is usually establish |
| 2311 | `prepaid_deferred_assets` | MATRIX | 0.188 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Provision for Doubtful Accounts |
| 2312 | `fnd23_intfvm_gfia` | MATRIX | 0.183 | 其他 | 0 | — | — | — | UNUSABLE | represents inventories of unsold finished goods on hand. These goods may have been produced internally or purchased for |
| 2313 | `insurance_funds_gross` | MATRIX | 0.183 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories - Finished Goods |
| 2314 | `fnd23_annfv1a_abpo` | MATRIX | 0.177 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in accounts payable and accrued expenses during the period when a company does not delineate the two |
| 2315 | `advance_payment_expense` | MATRIX | 0.175 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Advertising Expense - Supplemental represents the total cost of advertising incurred by the company. |
| 2316 | `allowance_for_doubtful_accounts` | MATRIX | 0.175 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | [Quarterly] Advertising Expense, Supplemental |
| 2317 | `fnd23_intfvm_abpo` | MATRIX | 0.175 | 其他 | 0 | — | — | — | UNUSABLE | represents changes in accounts payable and accrued expenses during the period when a company does not delineate the two |
| 2318 | `preferred_bank_assets` | MATRIX | 0.175 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Payable/Accrued |
| 2319 | `fnd23_annfv1a_ctda` | MATRIX | 0.173 | 盈利与财务 | 0 | — | — | — | UNUSABLE | represents deferred tax assets with a current maturity. When there is a timing difference between financial reporting an |
| 2320 | `fnd23_intfvm_mria` | MATRIX | 0.171 | 其他 | 0 | — | — | — | UNUSABLE | annual inventories - raw material. |
| 2321 | `insurance_receivables_misc` | MATRIX | 0.170 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories - Raw Materials |
| 2322 | `fnd23_intfvm2_cpca` | MATRIX | 0.161 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Construction in Progress – Gross represents the cost of construction in progress of fixed assets for a company’s own us |
| 2323 | `fnd23_intfvm_pwia` | MATRIX | 0.160 | 其他 | 0 | — | — | — | UNUSABLE | inventories that are WIP or work-in-progress. |
| 2324 | `insurance_written_premiums` | MATRIX | 0.160 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Inventories - Work In Progress |
| 2325 | `bank_debt_total` | MATRIX | 0.157 | 盈利与财务 | 0 | — | — | — | UNUSABLE | [Quarterly] Deferred Taxes |
| 2326 | `fnd23_intfvm_tdbo` | MATRIX | 0.157 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred Taxes for indirect Cash Flow |
| 2327 | `advance_expense_annual` | MATRIX | 0.157 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | advertising expense reported outside the cost of goods and services sold |
| 2328 | `fnd23_annfv1a_tdbo` | MATRIX | 0.156 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred Taxes for indirect Cash Flow |
| 2329 | `fnd23_annfvmfm2_tdbo` | MATRIX | 0.156 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred Taxes for indirect Cash Flow |
| 2330 | `other_borrowings_total` | MATRIX | 0.156 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Total other borrowings reported for the annual period. |
| 2331 | `current_tax_expense` | MATRIX | 0.152 | 其他 | 0 | — | — | — | UNUSABLE | [Quarterly] Current Tax - Foreign |
| 2332 | `contribution_to_funds` | MATRIX | 0.152 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Current Tax – Foreign |

## 六、本地回测证据

- 本地累计回测 **18** 条；其中 `ra_failed_checks` 为空的 **4** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `78NoOeVx` | 1.67 | 1.06 | 2.42 | 0.92 | 0.02 | 0 | 250 | `vector_neut(reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),ts_backfill(ass` |
| `rKOdkZX9` | 1.61 | 1.09 | 1.70 | 0.93 | 0.01 | 0 | 250 | `reverse(rank(ts_mean(divide(ts_backfill(total_financing_cash_flow,252),ts_backfill(assets_` |
| `wpZ9mr9Q` | 1.51 | 0.96 | 1.92 | 0.76 | 0.02 | ["LOW_SHARPE | 249 | `subtract(0,rank(divide(ts_backfill(total_financing_cash_flow,252),ts_backfill(assets_total` |
| `2rwj1kWY` | 1.42 | 0.85 | 2.20 | 0.75 | 0.02 | 0 | 247 | `reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(operating_c` |
| `npdAxjwd` | 1.41 | 0.85 | 2.09 | 0.78 | 0.02 | ["LOW_SHARPE | 248 | `group_neutralize(reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_bac` |
| `O0NJQLwq` | 1.38 | 0.80 | 2.25 | 0.86 | 0.02 | 0 | 248 | `reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(investment_` |
| `GrbgVZv0` | 1.16 | 0.71 | 2.24 | 0.75 | 0.02 | ["LOW_ROBUST | 250 | `vector_neut(reverse(rank(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill` |
| `RRbAjO0g` | 0.75 | 0.32 | 1.36 | 0.64 | 0.02 | ["LOW_SHARPE | 248 | `reverse(rank(divide(ts_backfill(fnd23_debt_issuance,252),abs(ts_backfill(operating_cashflo` |
| `WjbLEmzd` | 0.55 | 0.19 | 0.27 | 0.17 | 0.02 | ["LOW_SHARPE | 247 | `rank(divide(ts_backfill(operating_cashflow,252),abs(ts_backfill(total_income_after_taxes,2` |
| `KPNmKRZE` | 0.46 | 0.14 | -0.20 | 0.50 | 0.03 | ["LOW_SHARPE | 247 | `reverse(rank(ts_delta(divide(ts_backfill(accounts_receivable_total_5,252),ts_backfill(accr` |
| `KPNm01m8` | 0.38 | 0.12 | 0.98 | 0.13 | 0.02 | ["LOW_SHARPE | 249 | `if_else(greater(ts_backfill(operating_cashflow,252),0),-rank(divide(ts_backfill(total_fina` |
| `JjNPl6Lj` | 0.24 | 0.05 | 0.48 | 0.07 | 0.03 | ["LOW_SHARPE | 250 | `reverse(rank(ts_zscore(divide(ts_backfill(total_financing_cash_flow,252),ts_backfill(asset` |
| `e7b6kY86` | -0.03 | 0.00 | -0.14 | -0.14 | 0.03 | ["LOW_SHARPE | 248 | `reverse(rank(ts_delta(divide(ts_backfill(total_financing_cash_flow,252),abs(ts_backfill(op` |
| `gJbWYzdM` | -0.28 | -0.08 | -0.11 | -0.15 | 0.02 | ["LOW_SHARPE | 247 | `reverse(rank(divide(ts_backfill(fnd23_tot_inventory,252),ts_backfill(trade_receivables_cur` |
| `O0NJ1vV1` | -0.29 | -0.08 | 0.19 | -0.31 | 0.01 | ["LOW_SHARPE | 247 | `reverse(rank(divide(ts_backfill(accrued_interest_payable,252),ts_backfill(accrued_cash_equ` |

## 七、判死记录（sealed dead_end）

- `EUR-FND23-CAPSTRUCT-DIVIDEND-DEAD`（2026-10-03）family=fundamental23 资本结构/杠杆族 + 股息族：{"concepts_tested": ["杠杆水平 zscore504 (S-0.62)", "杠杆变化 delta252 (S-0.59)", "净杠杆变化 (S-0.38)", "债务期限结构 ST-LT (S-0.34)", "绝对 LT 债务变化 (S-0.41)", "股息/equity (S0.03)", "股息增长 (S-0.28)", "派息率 dividend/income (S0.08)", "dividend per share zscore504 (S0.07)", "两个取负验证 (S-0.16/-0.14)"], "dataset": "fundamental23", "evidence": {"78600GxQ": "spd zscore504 S0.07 F0.01 robust_univ0.58(闸0.7,本波最接近) 2Y0.73 longCount4
- `EUR-FND23-ACCRUAL-EXPENSE-DEAD`（2026-10-03）family=fundamental23 应计质量/费用结构族：{"concepts_tested": ["异常损益/总资产 S-0.51（本族最强）", "异常损益 zscore504 S-0.32", "异常损益/权益变化 S-0.24", "折旧强度 S-0.19", "实际税负 S0.05", "隐含融资成本 interest_expense_net/debt S0.04"], "dataset": "fundamental23", "evidence": {"9qWbKJwd": "unusual_income_expense/total_assets_4 S-0.51 F-0.18 2Y-0.89 longCount601", "6XK31zw5": "unusual_income_expense zscore504 S-0.32 longCount555", "rKeELAl8": "delta(unusual/equity) S-0.2
- `EUR-FND23-WORKINGCAP-INVENTORY-DEAD`（2026-10-03）family=fundamental23 营运资本/存货效率族：{"concepts_tested": ["inventory/income（周转效率倒数）S0.20", "fnd23_tot_inventory/assets_curr S0.10", "fnd23_tot_inventory/total_assets_4 S0.09", "营运资本 iucs/assets_curr S-0.39", "存货占比变化率 S-0.46", "存货水平 zscore504 S-0.31"], "dataset": "fundamental23", "evidence": {"A1vYaJ9X": "inventory/income S0.20 F0.04 longCount567", "blOVP2Xq": "inventory/assets_curr S0.10 F0.02 longCount478", "kqgbmk7g": "inventory/to

