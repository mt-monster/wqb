# fundamental6 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental6` |
| 名称 | Company Fundamental Data for Equity |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 279 |
| 覆盖率 | 0.5 |
| 平台已有 alpha | 513 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive, point-in-time global company fundamental data, capturing daily snapshots of financial statements, balance sheets, cash flows, and key ratios as they were known to the market at each historical date. It includes restatements, amendments, and all changes, ensuring accurate backtesting and minimizing look-ahead bias. The dataset covers a wide range of standardized and normalized financial metrics across regions and industries, making it a critical resource for quantitative research, factor modeling, and alpha generation. By reflecting the true information set available to investors at any given time, it enables robust prediction of price movements and supports the development of systematic investment strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **279** |
| 类型分布 | MATRIX×279 |
| 平均覆盖率 | **0.500** |
| 覆盖率区间 | 0.50 ~ 0.50 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 279 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 279 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 279 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 163 | 0.50 | fnd6_am、fnd6_amsa、fnd6_amy |
| 盈利与财务 | 97 | 0.50 | fnd6_accli、fnd6_acox、fnd6_aoloch |
| 价量与波动 | 8 | 0.50 | fnd6_newa1_ap、fnd6_newa2_sale、fnd6_newq_apq |
| 宏观与行业 | 4 | 0.50 | fnd6_adesinda_curcd、fnd6_exre、fnd6_exrey |
| 持仓与资金流 | 4 | 0.50 | fnd6_ewq_rectoq、fnd6_fopo、fnd6_fopoy |
| 风险与质量 | 2 | 0.50 | fnd6_apchy、fnd6_newa2_txditc |
| 搜索与替代数据 | 1 | 0.50 | fnd6_newa2_xrd |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `fnd6_accli` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accrued Liabilities - Increase/(Decrease) |
| 2 | `fnd6_acox` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Assets - Other - Sundry |
| 3 | `fnd6_adesinda_curcd` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO Currency Code - Company Annual Market |
| 4 | `fnd6_am` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of Intangibles |
| 5 | `fnd6_amsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of Intangibles |
| 6 | `fnd6_amy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of Intangibles |
| 7 | `fnd6_aoloch` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets and Liabilities - Other - Net Change |
| 8 | `fnd6_aolochy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets and Liabilities - Other (Net Change) |
| 9 | `fnd6_aox` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets - Other - Sundry |
| 10 | `fnd6_apch` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Accounts Payable - Increase (Decrease) |
| 11 | `fnd6_apchy` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | Accounts Payable/Creditors - Increase (Decrease) |
| 12 | `fnd6_apo` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Accounts Payable - Other |
| 13 | `fnd6_aqc` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Acquisitions |
| 14 | `fnd6_aqcy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Acquisitions |
| 15 | `fnd6_capxy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Capital Expenditures |
| 16 | `fnd6_ch` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash |
| 17 | `fnd6_cheb` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash and Cash Equivalents at Beginning of Year |
| 18 | `fnd6_chech` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash and Cash Equivalents - Increase/(Decrease) |
| 19 | `fnd6_chechy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash and Cash Equivalents - Increase (Decrease) |
| 20 | `fnd6_chee` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash and Cash Equivalents at End of Year |
| 21 | `fnd6_cogssa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cost of Goods Sold |
| 22 | `fnd6_cogsy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cost of Goods Sold |
| 23 | `fnd6_cptnewq_actq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Assets - Total |
| 24 | `fnd6_cptnewq_atq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets - Total |
| 25 | `fnd6_cptnewq_ceqq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Common/Ordinary Equity - Total |
| 26 | `fnd6_cptnewq_dlttq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-Term Debt - Total |
| 27 | `fnd6_cptnewq_ibq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Before Extraordinary Items |
| 28 | `fnd6_cptnewq_ltq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liabilities - Total |
| 29 | `fnd6_cptnewq_revtq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue - Total |
| 30 | `fnd6_dc` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Charges |
| 31 | `fnd6_dd1` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-Term Debt Due in 1 Year |
| 32 | `fnd6_dfxa` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation of Tangible Fixed Assets |
| 33 | `fnd6_dfxasa` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation of Fixed Assets (Tangible) |
| 34 | `fnd6_dfxay` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation of Fixed Assets (Tangible) |
| 35 | `fnd6_dlcch` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Debt - Changes |
| 36 | `fnd6_dpcy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation and Amortization - Statement of Cash Flows |
| 37 | `fnd6_dpsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Depreciation and Amortization - Total |
| 38 | `fnd6_dpy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Depreciation and Amortization - Total |
| 39 | `fnd6_dvc` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends Common/Ordinary |
| 40 | `fnd6_dvt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends - Total |
| 41 | `fnd6_dvty` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends - Total |
| 42 | `fnd6_dvy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Dividends |
| 43 | `fnd6_eieac` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity Interest in Earnings of Associated Companies |
| 44 | `fnd6_eieacy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity Interest in Earnings of Associated Companies |
| 45 | `fnd6_ero` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity Reserves - Other |
| 46 | `fnd6_ewq_accdq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Accrued Expenses & Deferred Income |
| 47 | `fnd6_ewq_amq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Amortization of Intangibles |
| 48 | `fnd6_ewq_dfxaq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation of Fixed Assets (Tangible) |
| 49 | `fnd6_ewq_dvtq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends - Total |
| 50 | `fnd6_ewq_eqrtq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity Reserves - Total |
| 51 | `fnd6_ewq_eroq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Equity Reserves - Other |
| 52 | `fnd6_ewq_gpq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross Profit (Loss) |
| 53 | `fnd6_ewq_ibmiiq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income before Extraordinary Items and Noncontrolling Interests |
| 54 | `fnd6_ewq_iditq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest Income - Total |
| 55 | `fnd6_ewq_intanq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Intangible Assets - Total |
| 56 | `fnd6_ewq_ivaeqq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Investment and Advances - Equity |
| 57 | `fnd6_ewq_ivaoq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Investment and Advances - Other |
| 58 | `fnd6_ewq_lltq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-Term Liabilities (Total) |
| 59 | `fnd6_ewq_mibnq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Non-Redeemable Noncontrolling Interest (Balance Sheet) - Quarterly |
| 60 | `fnd6_ewq_mibtq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Noncontrolling Interests - Total - Balance Sheet - Quarterly |
| 61 | `fnd6_ewq_nopioq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Other Non-Operating Inc/Expense |
| 62 | `fnd6_ewq_oproq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Revenues - Other |
| 63 | `fnd6_ewq_rectoq` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Receivables - Current Other incl. Tax Refunds |
| 64 | `fnd6_ewq_teqq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Stockholders' Equity - Total - Quarterly |
| 65 | `fnd6_ewq_txdbq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Taxes - Balance Sheet |
| 66 | `fnd6_ewq_xoproq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expense - Other |
| 67 | `fnd6_ewq_xppq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Prepaid Expenses & Accrued Income |
| 68 | `fnd6_ewq_xstq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Staff Expense - Wages/Salaries |
| 69 | `fnd6_exre` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Exchange Rate Effect |
| 70 | `fnd6_exrey` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Exchange Rate Effect |
| 71 | `fnd6_fiao` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Financing Activities - Other |
| 72 | `fnd6_fiaoy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Financing Activities - Other |
| 73 | `fnd6_fincfy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Financing Activities - Net Cash Flow |
| 74 | `fnd6_fopo` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funds from Operations - Other |
| 75 | `fnd6_fopoy` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funds from Operations - Other |
| 76 | `fnd6_gpsa` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross Profit (Loss) |
| 77 | `fnd6_gpy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross Profit (Loss) |
| 78 | `fnd6_ibcy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Income Before Extraordinary Items - Statement of Cash Flows |
| 79 | `fnd6_ibmiisa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income before Extraordinary Items and Noncontrolling Interests |
| 80 | `fnd6_ibmiiy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income before Extraordinary Items and Noncontrolling Interests |
| 81 | `fnd6_ibsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Before Extraordinary Items |
| 82 | `fnd6_iby` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Before Extraordinary Items |
| 83 | `fnd6_idesindq_curcd` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO Currency Code - Company Annual Market |
| 84 | `fnd6_idit` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest and Related Income - Total |
| 85 | `fnd6_iditsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest Income - Total |
| 86 | `fnd6_idity` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest Income - Total |
| 87 | `fnd6_intan` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Intangible Assets - Total |
| 88 | `fnd6_intanp` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Intangible Assets - Purchase |
| 89 | `fnd6_intanpy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Intangible Assets - Purchase |
| 90 | `fnd6_intfact` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest and Dividend Adjustments - Financing Activities |
| 91 | `fnd6_intiact` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest and Dividend Adjustments - Investing Activities |
| 92 | `fnd6_intiacty` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest and Dividend Adjustments - Investing Activities |
| 93 | `fnd6_intoact` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest and Dividend Adjustments - Operating Activities |
| 94 | `fnd6_intoacty` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Interest and Dividend Adjustments - Operating Activities |
| 95 | `fnd6_intpn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest Paid - Net |
| 96 | `fnd6_invch` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Mortgages - Decrease (Increase) |
| 97 | `fnd6_invchy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Inventory - Decrease (Increase) |
| 98 | `fnd6_invfg` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Inventories - Finished Goods |
| 99 | `fnd6_invo` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Inventories - Other |
| 100 | `fnd6_invrm` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Inventories - Raw Materials |
| 101 | `fnd6_invwip` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Inventories - Work In Process |
| 102 | `fnd6_ivaco` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Investing Activities - Other |
| 103 | `fnd6_ivacoy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Investing Activities - Other |
| 104 | `fnd6_ivaeq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Investment and Advances - Equity |
| 105 | `fnd6_ivao` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Investment and Advances - Other |
| 106 | `fnd6_ivch` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Increase in Investments |
| 107 | `fnd6_ivchy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Increase in Investments |
| 108 | `fnd6_ivncfy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Investing Activities - Net Cash Flow |
| 109 | `fnd6_ivst` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Short-Term Investments - Total |
| 110 | `fnd6_lcox` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Liabilities - Other - Sundry |
| 111 | `fnd6_ltdch` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-Term Debt - Change |
| 112 | `fnd6_ltdchy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-Term Debt - Change |
| 113 | `fnd6_mibn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Noncontrolling Interests - Nonredeemable - Balance Sheet |
| 114 | `fnd6_mibt` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Noncontrolling Interests - Total - Balance Sheet |
| 115 | `fnd6_miisa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Noncontrolling Interest - Income Account |
| 116 | `fnd6_miiy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Noncontrolling Interest - Income Account |
| 117 | `fnd6_newa1_aco` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Assets - Other - Total |
| 118 | `fnd6_newa1_act` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Assets - Total |
| 119 | `fnd6_newa1_ao` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets - Other |
| 120 | `fnd6_newa1_ap` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Accounts Payable - Trade |
| 121 | `fnd6_newa1_at` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets - Total |
| 122 | `fnd6_newa1_caps` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Capital Surplus/Share Premium Reserve |
| 123 | `fnd6_newa1_capx` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Capital Expenditures |
| 124 | `fnd6_newa1_ceq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Common/Ordinary Equity - Total |
| 125 | `fnd6_newa1_che` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash and Short-Term Investments |
| 126 | `fnd6_newa1_cogs` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cost of Goods Sold |
| 127 | `fnd6_newa1_cstk` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Common/Ordinary Stock (Capital) |
| 128 | `fnd6_newa1_dlc` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt in Current Liabilities - Total |
| 129 | `fnd6_newa1_dltt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Long-Term Debt - Total |
| 130 | `fnd6_newa1_do` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Discontinued Operations |
| 131 | `fnd6_newa1_dp` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Depreciation and Amortization |
| 132 | `fnd6_newa1_dpact` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Depreciation, Depletion and Amortization (Accumulated) |
| 133 | `fnd6_newa1_dpc` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Depreciation and Amortization (Cash Flow) |
| 134 | `fnd6_newa1_dv` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Cash Dividends (Cash Flow) |
| 135 | `fnd6_newa1_ebit` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Before Interest and Taxes |
| 136 | `fnd6_newa1_ebitda` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings Before Interest |
| 137 | `fnd6_newa1_emp` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Employees |
| 138 | `fnd6_newa1_fca` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Foreign Exchange Income (Loss) |
| 139 | `fnd6_newa1_fincf` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Financing Activities - Net Cash Flow |
| 140 | `fnd6_newa1_gdwl` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Goodwill |
| 141 | `fnd6_newa1_ib` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Before Extraordinary Items |
| 142 | `fnd6_newa1_ibc` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Income Before Extraordinary Items (Cash Flow) |
| 143 | `fnd6_newa1_icapt` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Invested Capital - Total |
| 144 | `fnd6_newa1_invt` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Inventories - Total |
| 145 | `fnd6_newa1_ivncf` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Investing Activities - Net Cash Flow |
| 146 | `fnd6_newa1_lco` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Liabilities - Other - Total |
| 147 | `fnd6_newa1_lct` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Liabilities - Total |
| 148 | `fnd6_newa1_lo` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liabilities - Other - Total |
| 149 | `fnd6_newa1_lse` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liabilities and Stockholders Equity - Total |
| 150 | `fnd6_newa1_lt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liabilities - Total |
| 151 | `fnd6_newa2_mii` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Noncontrolling Interest (Income Account) |
| 152 | `fnd6_newa2_oancf` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Activities - Net Cash Flow |
| 153 | `fnd6_newa2_oiadp` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Income After Depreciation |
| 154 | `fnd6_newa2_oibdp` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Income Before Depreciation |
| 155 | `fnd6_newa2_pi` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Pretax Income |
| 156 | `fnd6_newa2_ppegt` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Property, Plant and Equipment - Total (Gross) |
| 157 | `fnd6_newa2_ppent` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Property, Plant and Equipment - Total (Net) |
| 158 | `fnd6_newa2_pstk` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Preferred/Preference Stock (Capital) - Total |
| 159 | `fnd6_newa2_pstkn` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Preferred/Preference Stock - Nonredeemable |
| 160 | `fnd6_newa2_pstkr` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Preferred/Preference Stock - Redeemable |
| 161 | `fnd6_newa2_re` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Retained Earnings |
| 162 | `fnd6_newa2_rect` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Receivables - Total |
| 163 | `fnd6_newa2_revt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue - Total |
| 164 | `fnd6_newa2_sale` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Sales/Turnover (Net) |
| 165 | `fnd6_newa2_seq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Stockholders' Equity - Parent |
| 166 | `fnd6_newa2_spi` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Special Items |
| 167 | `fnd6_newa2_tstk` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Treasury Stock - Total (All Capital) |
| 168 | `fnd6_newa2_txditc` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | Deferred Taxes and Investment Tax Credit |
| 169 | `fnd6_newa2_txp` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes Payable |
| 170 | `fnd6_newa2_txt` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes - Total |
| 171 | `fnd6_newa2_wcap` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Working Capital (Balance Sheet) |
| 172 | `fnd6_newa2_xido` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Extraordinary Items and Discontinued Operations |
| 173 | `fnd6_newa2_xint` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest and Related Expense - Total |
| 174 | `fnd6_newa2_xrd` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | Research and Development Expense |
| 175 | `fnd6_newa2_xsga` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Selling, General and Administrative Expense |
| 176 | `fnd6_newq_acoq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Assets - Other - Total |
| 177 | `fnd6_newq_acoxq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Other Current Assets - Sundry |
| 178 | `fnd6_newq_ancq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Non-Current Assets - Total |
| 179 | `fnd6_newq_aoq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Assets - Other - Total |
| 180 | `fnd6_newq_apq` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Account Payable/Creditors - Trade |
| 181 | `fnd6_newq_capsq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Capital Surplus/Share Premium Reserve |
| 182 | `fnd6_newq_cheq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cash and Short-Term Investments |
| 183 | `fnd6_newq_cogsq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Cost of Goods Sold |
| 184 | `fnd6_newq_cstkq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Common/Ordinary Stock (Capital) |
| 185 | `fnd6_newq_dlcq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Debt in Current Liabilities |
| 186 | `fnd6_newq_dpactq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Depreciation, Depletion and Amortization (Accumulated) |
| 187 | `fnd6_newq_dpq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Depreciation and Amortization - Total |
| 188 | `fnd6_newq_gdwlq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Goodwill (net) |
| 189 | `fnd6_newq_invtq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Inventories - Total |
| 190 | `fnd6_newq_lcoq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Liabilities - Other - Total |
| 191 | `fnd6_newq_lcoxq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Liabilities - Other (Sundry) |
| 192 | `fnd6_newq_lctq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Current Liabilities - Total |
| 193 | `fnd6_newq_loq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liabilities - Other |
| 194 | `fnd6_newq_lseq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liabilities and Stockholders' Equity - Total |
| 195 | `fnd6_newq_ltmibq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liabilities - Total and Non-controlling Interest |
| 196 | `fnd6_newq_miiq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Noncontrolling Interest - Income Account |
| 197 | `fnd6_newq_nopiq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Non-Operating Income (Expense) - Total |
| 198 | `fnd6_newq_oiadpq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Income After Depreciation - Quarterly |
| 199 | `fnd6_newq_oibdpq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Income Before Depreciation - Quarterly |
| 200 | `fnd6_newq_piq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Pretax Income |
| 201 | `fnd6_newq_ppentq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Property, Plant and Equipment - Total (Net) |
| 202 | `fnd6_newq_reccoq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Receivables - Current - Other |
| 203 | `fnd6_newq_rectq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Receivables - Total |
| 204 | `fnd6_newq_rectrq` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Receivables - Trade |
| 205 | `fnd6_newq_req` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Retained Earnings |
| 206 | `fnd6_newq_saleq` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Sales/Turnover (Net) |
| 207 | `fnd6_newq_sctq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Total Share Capital |
| 208 | `fnd6_newq_seqq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Stockholders' Equity - Total - Quarterly |
| 209 | `fnd6_newq_spiq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Special Items |
| 210 | `fnd6_newq_tstkq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Treasury Stock - Total (All Capital) |
| 211 | `fnd6_newq_txtq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes - Total |
| 212 | `fnd6_newq_xintq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest and Related Expense - Total |
| 213 | `fnd6_newq_xoprq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expense - Total |
| 214 | `fnd6_newq_xsgaq` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Selling, General and Administrative Expenses |
| 215 | `fnd6_nopi` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Nonoperating Income (Expense) |
| 216 | `fnd6_nopiosa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Other Non-Operating Inc/Expense |
| 217 | `fnd6_nopioy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Other Non-Operating Inc/Expense |
| 218 | `fnd6_nopisa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Non-Operating Income (Expense) - Total |
| 219 | `fnd6_nopiy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Non-Operating Income (Expense) - Total |
| 220 | `fnd6_np` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Notes Payable - Short-Term Borrowings |
| 221 | `fnd6_oancfy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Activities - Net Cash Flow |
| 222 | `fnd6_oiadpsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Income After Depreciation - Semiannual |
| 223 | `fnd6_oibdpsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Income Before Depreciation - Semiannual |
| 224 | `fnd6_oibdpy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Income Before Depreciation |
| 225 | `fnd6_oproy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating Revenues - Other |
| 226 | `fnd6_pisa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Pretax Income |
| 227 | `fnd6_piy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Pretax Income |
| 228 | `fnd6_prstkc` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Purchase of Common and Preferred Stock |
| 229 | `fnd6_psfix` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Proceeds From Sale of Fixed Assets |
| 230 | `fnd6_psfixy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Proceeds - Sale of Fixed Assets |
| 231 | `fnd6_purtshr` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Purchase of Treasury Shares |
| 232 | `fnd6_purtshry` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Purchase of Treasury Shares |
| 233 | `fnd6_recch` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Accounts Receivable - Decrease (Increase) |
| 234 | `fnd6_recchy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Accounts Receivable - Decrease (Increase) |
| 235 | `fnd6_recco` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Receivables - Current - Other |
| 236 | `fnd6_rectr` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Receivables - Trade |
| 237 | `fnd6_revtsa` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue - Total |
| 238 | `fnd6_revty` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue - Total |
| 239 | `fnd6_salesa` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Sales/Turnover (Net) |
| 240 | `fnd6_saley` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Sales/Turnover (Net) |
| 241 | `fnd6_siv` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Sale of Investments |
| 242 | `fnd6_sivy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Sale of Investments |
| 243 | `fnd6_spisa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Special Items |
| 244 | `fnd6_spiy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Special Items |
| 245 | `fnd6_sppiv` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Sale of Property, Plant and Equipment and Investments - Gain (Loss) |
| 246 | `fnd6_sppivy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Sale of PP&E and Investments - (Gain) Loss |
| 247 | `fnd6_sstk` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Sale of Common and Preferred Stock |
| 248 | `fnd6_sstky` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Sale of Common and Preferred Stock |
| 249 | `fnd6_teq` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Stockholders' Equity - Total |
| 250 | `fnd6_txc` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes - Current |
| 251 | `fnd6_txdb` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Deferred Taxes - Balance Sheet |
| 252 | `fnd6_txdc` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred Taxes (Cash Flow) |
| 253 | `fnd6_txdi` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes - Deferred |
| 254 | `fnd6_txo` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes - Other |
| 255 | `fnd6_txop` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Taxation - Operating Activities |
| 256 | `fnd6_txopy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Taxation - Operating Activities |
| 257 | `fnd6_txpd` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes Paid |
| 258 | `fnd6_txtsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes - Total |
| 259 | `fnd6_txty` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Income Taxes - Total |
| 260 | `fnd6_txw` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Excise Taxes |
| 261 | `fnd6_wcapopc` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Working Capital/Net Operating Assets - Change |
| 262 | `fnd6_wcapopcy` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Working Capital/Net Operating Assets - Change |
| 263 | `fnd6_xacc` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Accrued Expenses |
| 264 | `fnd6_xintsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest and Related Expense - Total |
| 265 | `fnd6_xinty` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Interest and Related Expense - Total |
| 266 | `fnd6_xlr` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Staff Expense - Total |
| 267 | `fnd6_xopr` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expenses - Total |
| 268 | `fnd6_xopro` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expense - Other |
| 269 | `fnd6_xoprosa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expense - Other |
| 270 | `fnd6_xoproy` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expense - Other |
| 271 | `fnd6_xoprsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expense - Total |
| 272 | `fnd6_xopry` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Operating Expense - Total |
| 273 | `fnd6_xpp` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Prepaid Expenses |
| 274 | `fnd6_xrent` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Rental Expense |
| 275 | `fnd6_xsgasa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Selling, General and Administrative Expenses |
| 276 | `fnd6_xsgay` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Selling, General and Administrative Expenses |
| 277 | `fnd6_xstfws` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Staff Expense - Wages and Salaries |
| 278 | `fnd6_xstsa` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Staff Expense - Wages/Salaries |
| 279 | `fnd6_xsty` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Staff Expense - Wages/Salaries |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

