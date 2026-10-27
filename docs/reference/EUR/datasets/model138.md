# model138 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model138` |
| 名称 | Stock Selection from Accounting-based Factors |
| 类别 | MODEL |
| 数据字段数(平台) | 120 |
| 覆盖率 | 0.5537 |
| 平台已有 alpha | 1260 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset contains a comprehensive suite of Performance Deviation Index (PDI) factors derived from 14 key accounting variables, designed to measure the deviation of a company's latest financial metrics from its historical averages. The dataset includes composite models, quality-focused variants, and sector-neutralized signals, all constructed using advanced techniques such as risk parity weighting, deseasonalization, and clustering. By capturing anomalies and behavioral biases in financial statement data, these factors have demonstrated superior risk-adjusted returns compared to traditional accounting ratios and growth metrics. The dataset is valuable for quantitative investors seeking to enhance stock selection, improve portfolio diversification, and boost predictive power for price mo

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **120** |
| 类型分布 | VECTOR×120 |
| 平均覆盖率 | **0.554** |
| 覆盖率区间 | 0.55 ~ 0.55 |
| 更新频率（推断） | 低频（季/年） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 120 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 120 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 120 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 88 | 0.55 | mdl138_aor_3idpq、mdl138_aor_4idpq、mdl138_aor_5idpq |
| 其他 | 14 | 0.55 | mdl138_epp_3idp、mdl138_pa_3idp、mdl138_pa_4idp |
| 价量与波动 | 11 | 0.55 | mdl138_pdi5_cash、mdl138_qpdi3_invent_to、mdl138_qpdi3_payable_to |
| 持仓与资金流 | 5 | 0.55 | mdl138_3idpc、mdl138_4idpc、mdl138_5idpc |
| 风险与质量 | 2 | 0.55 | mdl138_3idpqc、mdl138_4idpqc |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl138_3idpc` | VECTOR | 0.554 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Composite Performance Deviation Index over 3 quarters, aggregating all PDI3 factors using risk parity weighting to reflect overall abnormal  |
| 2 | `mdl138_3idpqc` | VECTOR | 0.554 | 风险与质量 | 0 | — | — | — | UNUSABLE | Composite quality-adjusted performance deviation index over 3 trailing quarters, aggregating standardized deviations of multiple financial r |
| 3 | `mdl138_4idpc` | VECTOR | 0.554 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Composite PDI score aggregated from raw four-quarter PDI factors using risk parity weighting, showing a holistic measure of absolute fundame |
| 4 | `mdl138_4idpqc` | VECTOR | 0.554 | 风险与质量 | 0 | — | — | — | UNUSABLE | Composite quality PDI score over 4 trailing quarters, aggregating all quality-adjusted PDI factors by clustering similar metrics, equal-weig |
| 5 | `mdl138_5idpc` | VECTOR | 0.554 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Composite PDI score aggregating all PDI factors over 5 trailing quarters using risk parity weighting; summarizes absolute magnitude of funda |
| 6 | `mdl138_5idpqc` | VECTOR | 0.554 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Composite Quality-adjusted PDI score over 5 trailing quarters, aggregating QPDI5 factors across seven fundamental clusters with risk parity  |
| 7 | `mdl138_aor_3idpq` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 trailing quarters based on Return on Assets (ROA), measuring deviation of ROA ratio from |
| 8 | `mdl138_aor_4idpq` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 trailing quarters based on Return on Assets (Net Income divided by total assets), showin |
| 9 | `mdl138_aor_5idpq` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 5 quarters for return on assets, capturing deviations in firm profitability (net income /  |
| 10 | `mdl138_dtl_3idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 3 trailing quarters, measuring deviation of long-term debt from historical levels, providing insight into c |
| 11 | `mdl138_dtl_4idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 4 trailing quarters measuring deviation of long-term debt from historical norm, likely scaled by firm size  |
| 12 | `mdl138_dtl_5idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 5 trailing quarters, measuring the absolute deviation of a firm's long-term debt from its historical norm,  |
| 13 | `mdl138_epp_3idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | 3-quarter absolute-level PDI factor measuring deviation in property, plant, and equipment over the last 3 quarters versus historical trend,  |
| 14 | `mdl138_epp_4idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 4-quarter absolute-level PDI factor measuring deviation in the amount of property, plant, and equipment (PPE) from its historical trend, typ |
| 15 | `mdl138_epp_5idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over trailing 5 quarters based on Property, Plant & Equipment (PPE), likely representing deviation in the carryi |
| 16 | `mdl138_er_3idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Raw Performance Deviation Index over 3 trailing quarters, measuring the deviation in retained earnings from its historical norm, scaled by s |
| 17 | `mdl138_er_4idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | PDI-4 Factor based on Retained Earnings |
| 18 | `mdl138_er_5idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over trailing 5 quarters for retained earnings (cumulative net earnings retained in equity), measuring deviation |
| 19 | `mdl138_in_3idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation over the past 3 quarters of the firm's net income (scaled by firm size) from its historical average, capturing recent abnormal ear |
| 20 | `mdl138_in_4idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 4 trailing quarters based on absolute net income, measuring how much net earnings deviate from the firm's h |
| 21 | `mdl138_in_5idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Raw PDI factor over 5 trailing quarters measuring deviation in net income (scaled by firm size) from its long-term average |
| 22 | `mdl138_ofc_3idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index (PDI) over 3 quarters for Cash Flow from Operations (CFO), quantifying how much operational cash flows deviate f |
| 23 | `mdl138_ofc_4idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index (PDI) over 4 quarters for Cash Flow from Operations (CFO), indicating deviations in operating cash flow against  |
| 24 | `mdl138_ofc_5idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index (PDI) over 5 quarters for Cash Flow from Operations (CFO), capturing the deviation of operational cash flows fro |
| 25 | `mdl138_pa_3idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 3 trailing quarters measuring the deviation of accounts payable from its historical norm, likely scaled by  |
| 26 | `mdl138_pa_4idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over trailing 4 quarters for absolute accounts payable, scaled, quantifying deviation from its historical baseli |
| 27 | `mdl138_pa_5idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 5 trailing quarters, measuring the absolute deviation of Accounts Payable (amount owed to suppliers) from i |
| 28 | `mdl138_pdi3_caps` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Absolute deviation over the past 3 quarters in the firm's capital surplus (excess paid-in capital), scaled for firm size |
| 29 | `mdl138_pdi3_cash` | VECTOR | 0.554 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Deviation in the firm's total cash holdings, measured at an absolute level over 3 trailing quarters and scaled by firm size to identify abno |
| 30 | `mdl138_pdi3_ebitda` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 3 trailing quarters, measuring absolute deviation in EBITDA from the firm's historical norm, scaled by firm |
| 31 | `mdl138_pdi3_sale` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Raw Performance Deviation Index over 3 trailing quarters, quantifying how much the firm's sales have deviated from their historical norm, sc |
| 32 | `mdl138_pdi4_caps` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 4 quarters for Capital Surplus, measuring its deviation from the historical or expected value |
| 33 | `mdl138_pdi4_cash` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | PDI factor quantifying the absolute deviation in cash levels from the firm’s historical norm over the trailing 4 quarters, scaled by size |
| 34 | `mdl138_pdi4_ebitda` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index (PDI) over 4 quarters for EBITDA, measuring deviation of EBITDA from its historical baseline, scaled by total as |
| 35 | `mdl138_pdi4_sale` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 4 trailing quarters based on absolute sales (turnover), measuring deviation of firm's sales from its recent |
| 36 | `mdl138_pdi5_caps` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over five trailing quarters for capital surplus, quantifying absolute deviation from its historical values, size |
| 37 | `mdl138_pdi5_cash` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | The PDI factor over 5 trailing quarters, measuring the deviation in the firm's cash holdings from its historical average, scaled appropriate |
| 38 | `mdl138_pdi5_ebitda` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index (PDI) over 5 quarters for EBITDA, measuring the deviation in earnings before interest, taxes, depreciation, and  |
| 39 | `mdl138_pdi5_sale` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over trailing 5 quarters based on absolute sales revenue, scaled appropriately, capturing deviation in sales ver |
| 40 | `mdl138_pg_3idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The PDI factor over 3 trailing quarters, measuring the deviation of the firm's Gross Profit from its historical average, scaled for size, re |
| 41 | `mdl138_pg_4idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 4 quarters measuring the deviation of Gross Profit from its expected or average value (absolute, scaled by  |
| 42 | `mdl138_pg_5idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Raw PDI factor over 5 trailing quarters measuring deviation in gross profit (scaled appropriately) from its historical value |
| 43 | `mdl138_qpdi3_berry` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 quarters capturing deviation in the Berry Ratio (Gross Profit / Operating Expenses), mea |
| 44 | `mdl138_qpdi3_cfo_curr_liab` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor measuring deviation of operating cash flow to current liabilities ratio over the trailing 3 quarters |
| 45 | `mdl138_qpdi3_cfrnoa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 3 trailing quarters based on Cash Flow Return on Net Operating Assets, tracking deviation from the historical base |
| 46 | `mdl138_qpdi3_cfroa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 quarters measuring deviation in Cash Flow Return on Assets from its norm |
| 47 | `mdl138_qpdi3_cfroe` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 3-quarter quality-adjusted PDI factor measuring deviation in cash flow return on equity (cash flow from operations divided by equity) from i |
| 48 | `mdl138_qpdi3_current_r` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 quarters for the current ratio (Current Assets / Current Liabilities), measuring the dev |
| 49 | `mdl138_qpdi3_debt_capital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Three-quarter trailing quality-adjusted PDI factor measuring deviation in the Debt-to-Capital ratio (Total Debt / [Debt + Shareholders’ Equi |
| 50 | `mdl138_qpdi3_debt_equity` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 trailing quarters, measuring the deviation of the company's Debt to Equity ratio from it |
| 51 | `mdl138_qpdi3_debt_mktcapital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The QPDI factor over 3 trailing quarters, measuring deviation of the ratio of Total Debt to Total Capital at Market Value from its historica |
| 52 | `mdl138_qpdi3_gross_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 3 trailing quarters measuring deviation of the firm's gross margin ratio (gross profit divided by sales) fr |
| 53 | `mdl138_qpdi3_int_cover` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 trailing quarters, measuring deviation of the interest coverage ratio (EBIT/Interest Exp |
| 54 | `mdl138_qpdi3_invent_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index measuring deviation of Inventory Turnover ratio (typically sales or cost of goods sold divided  |
| 55 | `mdl138_qpdi3_lt_dt_capital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 quarters for the Long-term Debt to Capital ratio, reflecting deviation from the firm’s n |
| 56 | `mdl138_qpdi3_lt_dt_equity` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 trailing quarters, measuring the deviation of Long-Term Debt to Common Equity ratio from |
| 57 | `mdl138_qpdi3_net_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 3 trailing quarters measuring deviation in net income margin ratio from its normal level |
| 58 | `mdl138_qpdi3_op_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 3 trailing quarters measuring deviation of the firm's operating profit margin (EBIT divided by sales) from  |
| 59 | `mdl138_qpdi3_payable_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 3 trailing quarters, capturing deviation in Accounts Payable Turnover (efficiency of payin |
| 60 | `mdl138_qpdi3_quick_r` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation over the past 3 quarters of the firm's quick ratio (liquid assets/current liabilities) from its historical average, indicating rec |
| 61 | `mdl138_qpdi3_receiva_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 3 trailing quarters based on Accounts Receivable Turnover, capturing changes or deviations in receivables turnover |
| 62 | `mdl138_qpdi3_rnoa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 3 trailing quarters based on deviation in Return on Net Operating Assets ratio from its historical norm |
| 63 | `mdl138_qpdi3_roe` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor measuring the deviation of Return on Equity (ROE) from its historical average over the trailing 3 quarters |
| 64 | `mdl138_qpdi3_roic` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation over the past 3 quarters in Return on Invested Capital (ROIC), a profitability quality ratio |
| 65 | `mdl138_qpdi3_sale_empl` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 3 trailing quarters, measuring deviation in the ratio of sales (revenue) per employee from its historical baseline |
| 66 | `mdl138_qpdi4_berry` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 trailing quarters, measuring deviation of the Berry Ratio (Gross Profit divided by Opera |
| 67 | `mdl138_qpdi4_cfo_curr_liab` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 4-quarter quality-adjusted PDI factor measuring deviation in the ratio of operating cash flow to current liabilities from its historical ave |
| 68 | `mdl138_qpdi4_cfrnoa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 4 trailing quarters, measuring deviation in cash flow return on net operating assets (CFO/(Total Assets - Current  |
| 69 | `mdl138_qpdi4_cfroa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 4 trailing quarters, measuring deviation in the cash flow return on assets (CFO/Total Assets) from its historical  |
| 70 | `mdl138_qpdi4_cfroe` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation over the past 4 quarters of the firm's cash flow return on equity (operating cash flow divided by equity) from its historical norm |
| 71 | `mdl138_qpdi4_current_r` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index based on Current Ratio (Current Assets / Current Liabilities), measuring deviation from histori |
| 72 | `mdl138_qpdi4_debt_capital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 trailing quarters, measuring the deviation of the company's Debt to Total Capital ratio  |
| 73 | `mdl138_qpdi4_debt_equity` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 trailing quarters, reflecting deviation in the Debt-to-Equity financial leverage ratio f |
| 74 | `mdl138_qpdi4_debt_mktcapital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 trailing quarters, measuring deviation in the Total Debt to Total Capital at Market Valu |
| 75 | `mdl138_qpdi4_gross_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 4 quarters, measuring deviation in the firm's gross margin (gross profit to sales) compared to history, capturing  |
| 76 | `mdl138_qpdi4_int_cover` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 4 trailing quarters measuring deviation in the interest coverage ratio (such as EBIT/Interest Expense) from its hi |
| 77 | `mdl138_qpdi4_invent_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 4 trailing quarters for inventory turnover ratio, measuring deviation from baseline inventory turnover |
| 78 | `mdl138_qpdi4_lt_dt_capital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 quarters for the Long-term Debt to Capital ratio, reflecting deviation from the firm’s n |
| 79 | `mdl138_qpdi4_lt_dt_equity` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation (over last 4 quarters) of long-term debt to common equity ratio from its historical norm, quality-adjusted leverage metric |
| 80 | `mdl138_qpdi4_net_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 4 trailing quarters measuring deviation of the firm's net income margin (net income divided by sales) from  |
| 81 | `mdl138_qpdi4_op_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 quarters for operating profit margin (EBIT/Sales), indicating deviation in profitability |
| 82 | `mdl138_qpdi4_payable_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 quarters based on accounts payable turnover ratio, measuring deviations in how quickly t |
| 83 | `mdl138_qpdi4_quick_r` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 4 trailing quarters based on deviation in the Quick Ratio (liquid assets to current liabilities) from its n |
| 84 | `mdl138_qpdi4_receiva_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 quarters, measuring the deviation in the receivables turnover ratio (sales/accounts rece |
| 85 | `mdl138_qpdi4_rnoa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 4 trailing quarters based on Return on Net Operating Assets (RNOA), measuring how much the |
| 86 | `mdl138_qpdi4_roe` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Four-quarter trailing quality-adjusted PDI factor measuring deviation of Return on Equity (Net Income / Average Shareholders’ Equity) from i |
| 87 | `mdl138_qpdi4_roic` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | 4-quarter quality-adjusted PDI factor capturing deviation in return on invested capital (ROIC) over the past 4 quarters versus history, refl |
| 88 | `mdl138_qpdi4_sale_empl` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation (over last 4 quarters) of revenue per employee from its historical norm, quality-adjusted and scaled for cross-company comparison |
| 89 | `mdl138_qpdi5_berry` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 5 quarters measuring how much the Berry Ratio (Gross Profit / Operating Expenses) has devi |
| 90 | `mdl138_qpdi5_cfo_curr_liab` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Five-quarter trailing quality-adjusted PDI factor capturing changes in the CFO to Current Liabilities ratio (Operating Cash Flow / Current L |
| 91 | `mdl138_qpdi5_cfrnoa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 5 trailing quarters measuring deviation in Cash Flow Return on Net Operating Assets ratio from its expected |
| 92 | `mdl138_qpdi5_cfroa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor measuring deviation in cash flow return on assets (CFO/Total Assets) over the trailing 5 quarters |
| 93 | `mdl138_qpdi5_cfroe` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 5 trailing quarters, reflecting deviation in Cash Flow Return on Equity from its historica |
| 94 | `mdl138_qpdi5_current_r` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-quarter quality-adjusted PDI factor measuring deviation in the current ratio (current assets divided by current liabilities) from historic |
| 95 | `mdl138_qpdi5_debt_capital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted Performance Deviation Index over 5 quarters for the debt-to-total-capital ratio, measuring changes in balance sheet leverag |
| 96 | `mdl138_qpdi5_debt_equity` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-quarter quality-adjusted PDI factor measuring deviation in total debt to total equity ratio versus historical levels, capturing leverage s |
| 97 | `mdl138_qpdi5_debt_mktcapital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 5 trailing quarters, measuring deviation in the ratio of total debt to total capital at market value from its hist |
| 98 | `mdl138_qpdi5_gross_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation in the firm's Gross Margin (Gross Profit divided by Sales), measured over 5 trailing quarters as a quality-adjusted factor to capt |
| 99 | `mdl138_qpdi5_int_cover` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation (over last 5 quarters) of interest coverage ratio (earnings to interest expense) from its historical norm, quality-adjusted liquid |
| 100 | `mdl138_qpdi5_invent_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | 5-quarter quality-adjusted PDI factor capturing deviation in inventory turnover ratio from its historical norm, indicating changes in operat |
| 101 | `mdl138_qpdi5_lt_dt_capital` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-quarter quality-adjusted PDI factor capturing deviation in the ratio of long-term debt to total capital (often debt plus equity), from its |
| 102 | `mdl138_qpdi5_lt_dt_equity` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-quarter quality-adjusted PDI factor capturing deviation in the ratio of long-term debt to common equity from its historical baseline, meas |
| 103 | `mdl138_qpdi5_net_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 5 trailing quarters measuring deviation of the firm's net income margin (net income divided by sales) from  |
| 104 | `mdl138_qpdi5_op_margin` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI factor over 5 trailing quarters, measuring deviation in Operating Profit Margin (EBIT Margin) from its normal historica |
| 105 | `mdl138_qpdi5_payable_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | The QPDI factor over 5 trailing quarters, measuring deviation of Accounts Payable Turnover (typically Cost of Goods Sold divided by Accounts |
| 106 | `mdl138_qpdi5_quick_r` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deviation over the past 5 quarters of the firm's quick ratio (liquid assets divided by current liabilities, a liquidity measure) from its hi |
| 107 | `mdl138_qpdi5_receiva_to` | VECTOR | 0.554 | 价量与波动 | 0 | — | — | — | UNUSABLE | Deviation over the past 5 quarters in accounts receivable turnover (sales divided by accounts receivable), reflecting efficiency in collecti |
| 108 | `mdl138_qpdi5_rnoa` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 5 quarters measuring the deviation in return on net operating assets ratio (CFO or NI divided by net operating ass |
| 109 | `mdl138_qpdi5_roe` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-quarter quality-adjusted PDI factor measuring deviation in return on equity (ROE) from its historical average, reflecting change in profit |
| 110 | `mdl138_qpdi5_roic` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | 5-quarter quality-adjusted PDI factor capturing deviation in return on invested capital (ROIC) from historical baseline, measuring changes i |
| 111 | `mdl138_qpdi5_sale_empl` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Quality-adjusted PDI over 5 trailing quarters, measuring deviation in the ratio of sales (revenue) per employee from its historical baseline |
| 112 | `mdl138_tvni_3idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 3 trailing quarters based on inventory levels, indicating by how much the firm's inventory amount diverges  |
| 113 | `mdl138_tvni_4idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 4 quarters for inventory, measuring how much inventory levels have deviated from their typical recent value |
| 114 | `mdl138_tvni_5idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | PDI factor quantifying the absolute deviation in inventories from the firm’s historical norm over the trailing 5 quarters, scaled by total a |
| 115 | `mdl138_vcer_3idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 3 trailing quarters, measuring the deviation of accounts receivable from its historical value, indicating u |
| 116 | `mdl138_vcer_4idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | The PDI factor over 4 trailing quarters, measuring the deviation in the firm's Accounts Receivable from its historical norm, scaled by compa |
| 117 | `mdl138_vcer_5idp` | VECTOR | 0.554 | 其他 | 0 | — | — | — | UNUSABLE | Raw Performance Deviation Index over 5 trailing quarters, quantifying the deviation in accounts receivable levels from their historical norm |
| 118 | `mdl138_vd_3idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 3 quarters assessing how much the firm's cash dividends deviate from their recent historical levels, scaled |
| 119 | `mdl138_vd_4idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Performance Deviation Index over 4 trailing quarters measuring deviation in Cash Dividends from its historical average, scaled appropriately |
| 120 | `mdl138_vd_5idp` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Raw PDI factor over 5 trailing quarters measuring deviation in cash dividends paid from the historical pattern or expected value |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

