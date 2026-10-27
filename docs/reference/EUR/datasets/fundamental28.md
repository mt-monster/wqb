# fundamental28 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental28` |
| 名称 | Global Fundamental Data |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 1605 |
| 覆盖率 | 0.5 |
| 平台已有 alpha | 665 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive, standardized fundamental financial data for public companies worldwide, covering over 96% of global market capitalization. It includes annual and interim/quarterly financial statements, per share data, calculated ratios, pricing, and descriptive company information. With over 1,500 data items, the dataset enables deep peer comparability and historical analysis across regions and industries. It is highly valuable for quantitative research and price prediction, as it allows for the construction of fundamental factors (such as value, quality, profitability, and growth), backtesting of investment strategies, and robust cross-sectional and time-series analysis of company performance and valuation drivers.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **1605** |
| 类型分布 | MATRIX×1605 |
| 平均覆盖率 | **0.500** |
| 覆盖率区间 | 0.50 ~ 0.50 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 1605 | 100.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 1605 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 1605 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 760 | 0.50 | fnd28_anlev_value_08201a、fnd28_anlev_value_08205a、fnd28_anlev_value_08216a |
| 其他 | 617 | 0.50 | fnd28_2_value_08004、fnd28_anlev_value_08211a、fnd28_anlev_value_08215a |
| 价量与波动 | 114 | 0.50 | fnd28_2_value_05002、fnd28_2_value_05003、fnd28_anlev_value_08275a |
| 宏观与行业 | 39 | 0.50 | fnd28_ewsgrowth_value_08821、fnd28_ewsprof_value_08653、fnd28_fsa1_value_04840a |
| 搜索与替代数据 | 35 | 0.50 | fnd28_ewsprof_value_08341、fnd28_fsa1_value_01201a、fnd28_fsa1_value_03493a |
| 持仓与资金流 | 19 | 0.50 | fnd28_fsa1_value_04401a、fnd28_fsa1_value_04821a、fnd28_fsa1_value_04831a |
| 风险与质量 | 17 | 0.50 | fnd28_bdeq_value_18183q、fnd28_fsa1_value_01253a、fnd28_fsq1_value_01253q |
| 修正与预期 | 4 | 0.50 | fnd28_value_08356、fnd28_value_08356a、fnd28_value_08360 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `fnd28_2_value_05002` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - High |
| 2 | `fnd28_2_value_05003` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - Low |
| 3 | `fnd28_2_value_08004` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization - Public |
| 4 | `fnd28_anlev_value_08201a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity % Total Capital |
| 5 | `fnd28_anlev_value_08205a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity % Total Capital - 5 Yr Avg |
| 6 | `fnd28_anlev_value_08211a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest % Total Capital |
| 7 | `fnd28_anlev_value_08215a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest % Total Capital - 5 Yr Avg |
| 8 | `fnd28_anlev_value_08216a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Total Capital |
| 9 | `fnd28_anlev_value_08220a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Total Capital - 5 Yr Avg |
| 10 | `fnd28_anlev_value_08221a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Capital |
| 11 | `fnd28_anlev_value_08225a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Capital - 5 Yr Avg |
| 12 | `fnd28_anlev_value_08226a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Common Equity |
| 13 | `fnd28_anlev_value_08230a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Common Equity - 5 Yr Avg |
| 14 | `fnd28_anlev_value_08231a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Common Equity |
| 15 | `fnd28_anlev_value_08235a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Common Equity - 5 Yr Avg |
| 16 | `fnd28_anlev_value_08236a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Assets |
| 17 | `fnd28_anlev_value_08240a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Assets - 5 Yr Avg |
| 18 | `fnd28_anlev_value_08241a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity % Total Assets |
| 19 | `fnd28_anlev_value_08245a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity % Total Assets - 5 Yr Avg |
| 20 | `fnd28_anlev_value_08246a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividend Coverage Ratio |
| 21 | `fnd28_anlev_value_08250a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividend Coverage Ratio |
| 22 | `fnd28_anlev_value_08251a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Fixed Charge Coverage Ratio |
| 23 | `fnd28_anlev_value_08255a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Fixed Charge Coverage Ratio - 5 Yr Avg |
| 24 | `fnd28_anlev_value_08256a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Payout (% Earnings) |
| 25 | `fnd28_anlev_value_08260a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Payout (% Earnings) - Total Dollar - 5 Yr Avg |
| 26 | `fnd28_anlev_value_08261a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Cash/Fixed Charges |
| 27 | `fnd28_anlev_value_08265a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Cash/Fixed Charges - 5 Yr Avg |
| 28 | `fnd28_anlev_value_08266a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Fixed Assets % Common Equity Company Specific Accounting Practices |
| 29 | `fnd28_anlev_value_08270a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Fixed Assets % Common Equity - 5 Yr Avg |
| 30 | `fnd28_anlev_value_08271a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Working Capital % Total Capital 5 Year Averages |
| 31 | `fnd28_anlev_value_08275a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of annual field: Working Capital % Total Capital - 5 Yr Avg Liquidity Annual Statistics |
| 32 | `fnd28_anlev_value_08287a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets / Common Equity Ratio |
| 33 | `fnd28_anlev_value_08291a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: EBIT / Total Interest Expense Ratio |
| 34 | `fnd28_anlev_value_08906a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividends % Cash Flow |
| 35 | `fnd28_anlev_value_08910a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividends/Cash Flow - 5 Yr Avg |
| 36 | `fnd28_anlev_value_15121a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Capital % Total Assets |
| 37 | `fnd28_anlev_value_15124a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Capital % Total Assets |
| 38 | `fnd28_anliqq_value_08106` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Current Ratio |
| 39 | `fnd28_anliqq_value_08111` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Cash & Equivalents % Total Current Assets Company Specific Accounting Practices |
| 40 | `fnd28_annsttcs2_value_05001` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - Year End |
| 41 | `fnd28_annsttcs_value_05001` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - Year End |
| 42 | `fnd28_annsttcs_value_05201` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings per Share (Supported for Non U.S. only) |
| 43 | `fnd28_annsttcs_value_05202q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Fiscal Period End |
| 44 | `fnd28_annsttcs_value_05476` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Book Value per Share |
| 45 | `fnd28_annsttcs_value_05501` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Flow per Share |
| 46 | `fnd28_annsttcs_value_05503` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Long Term Liabilities per Share |
| 47 | `fnd28_annsttcs_value_05508` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Sales per Share |
| 48 | `fnd28_annualgrowthq_value_08579` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization Growth (year ago) Profitability |
| 49 | `fnd28_annualgrowthq_value_08601` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings per Share Growth |
| 50 | `fnd28_annualgrowthq_value_08606` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Book Value per Share Growth (year ago) |
| 51 | `fnd28_annualgrowthq_value_08611` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividends per Share Growth |
| 52 | `fnd28_annualgrowthq_value_08616` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Equity Growth (year ago) |
| 53 | `fnd28_annualgrowthq_value_08621` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Total Assets Growth (1 year ago) |
| 54 | `fnd28_annualgrowthq_value_08631` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Sales/Revenues Growth |
| 55 | `fnd28_annualgrowthq_value_08636` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Income Growth |
| 56 | `fnd28_annualgrowthq_value_08676` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Margin Growth |
| 57 | `fnd28_annualperfq_value_09104` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Price/Earnings Ratio Close |
| 58 | `fnd28_annualperfq_value_09304` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price/Book Value Ratio - Close |
| 59 | `fnd28_annualprofq_value_08301` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Return on Equity Total (%) |
| 60 | `fnd28_annualprofq_value_08306` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Gross Profit Margin |
| 61 | `fnd28_annualprofq_value_08311` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Flow/Sales |
| 62 | `fnd28_annualprofq_value_08316` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Operating Profit Margin |
| 63 | `fnd28_annualprofq_value_08321` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Pre-tax Margin |
| 64 | `fnd28_annualprofq_value_08326` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Return on Assets |
| 65 | `fnd28_annualprofq_value_08381` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Earnings Return on Equity |
| 66 | `fnd28_annualstats05_value_05202a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Earnings per Share Fiscal Period End |
| 67 | `fnd28_annualstats05_value_05502a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Cash Flow per Share Fiscal Period |
| 68 | `fnd28_anper_value_08801a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of annual field: Total Investment Return Year Ago Growth Rates |
| 69 | `fnd28_anper_value_08805a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Total Investment Return - 5 Yr Annual Return |
| 70 | `fnd28_anper_value_08806a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price Volatility |
| 71 | `fnd28_anper_value_09100a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - High |
| 72 | `fnd28_anper_value_09101a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - Low |
| 73 | `fnd28_anper_value_09104a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Price/Earnings Ratio Close |
| 74 | `fnd28_anper_value_09106a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - Avg High-Low |
| 75 | `fnd28_anper_value_09111a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - 5 Yr Avg High |
| 76 | `fnd28_anper_value_09116a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - 5 Yr Avg Low |
| 77 | `fnd28_anper_value_09121a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - 5 Yr Avg - Close |
| 78 | `fnd28_anper_value_09126a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - 5 Yr Avg High-Low |
| 79 | `fnd28_anper_value_09200a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - High |
| 80 | `fnd28_anper_value_09201a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - Low |
| 81 | `fnd28_anper_value_09204a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - Close |
| 82 | `fnd28_anper_value_09206a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - Avg High-Low |
| 83 | `fnd28_anper_value_09211a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - 5 Yr Avg High |
| 84 | `fnd28_anper_value_09216a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - 5 Yr Avg Low |
| 85 | `fnd28_anper_value_09221a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - 5 Yr Avg - Close |
| 86 | `fnd28_anper_value_09226a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Earnings Yield - 5 Yr Avg High-Low |
| 87 | `fnd28_anper_value_09300a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - High |
| 88 | `fnd28_anper_value_09301a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - Low |
| 89 | `fnd28_anper_value_09304a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - Close |
| 90 | `fnd28_anper_value_09306a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - Avg High-Low |
| 91 | `fnd28_anper_value_09311a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - 5 Yr Avg High |
| 92 | `fnd28_anper_value_09316a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - 5 Yr Avg Low |
| 93 | `fnd28_anper_value_09321a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - 5 Yr Avg - Close |
| 94 | `fnd28_anper_value_09326a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - 5 Yr Avg High-Low |
| 95 | `fnd28_anper_value_09400a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - High |
| 96 | `fnd28_anper_value_09401a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - Low |
| 97 | `fnd28_anper_value_09404a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - Close |
| 98 | `fnd28_anper_value_09406a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - Avg High-Low |
| 99 | `fnd28_anper_value_09504a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Payout per Share |
| 100 | `fnd28_anper_value_09604a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Cash Flow Ratio |
| 101 | `fnd28_anper_value_09621a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Cash Flow Ratio - 5 Yr Avg |
| 102 | `fnd28_anper_value_09704a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization to Common Equity |
| 103 | `fnd28_anper_value_09721a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization/Common Equity - 5 Yr Average Growth Rates Annual Statistics |
| 104 | `fnd28_anper_value_09904a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Sales per Share Ratio |
| 105 | `fnd28_anstaq_value_03151q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Working Capital |
| 106 | `fnd28_anstaq_value_05301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Shares Outstanding |
| 107 | `fnd28_anstaq_value_05486q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Tangible Book Value per Share |
| 108 | `fnd28_anstaq_value_08311q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Flow/Sales |
| 109 | `fnd28_anstaq_value_18191q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings before Interest and Taxes (EBIT) |
| 110 | `fnd28_anstaq_value_18198q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings before Interest, Taxes, Depreciation & Amortization (EBITDA) |
| 111 | `fnd28_anstaq_value_18263q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Net Profit |
| 112 | `fnd28_bdeq_value_03040q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Accounts Payable |
| 113 | `fnd28_bdeq_value_03051q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Short Term Debt & Current Portion of Long Term Debt |
| 114 | `fnd28_bdeq_value_03063q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income Taxes Payable |
| 115 | `fnd28_bdeq_value_03066q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Current Liabilities |
| 116 | `fnd28_bdeq_value_03069q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Accrued Expenses |
| 117 | `fnd28_bdeq_value_03101q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Liabilities - Total |
| 118 | `fnd28_bdeq_value_03245q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Debt Excluding Capitalized Leases |
| 119 | `fnd28_bdeq_value_03251q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Debt |
| 120 | `fnd28_bdeq_value_03255q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Debt |
| 121 | `fnd28_bdeq_value_03263q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes |
| 122 | `fnd28_bdeq_value_03273q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Liabilities |
| 123 | `fnd28_bdeq_value_03351q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Liabilities |
| 124 | `fnd28_bdeq_value_03426q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Minority Interest |
| 125 | `fnd28_bdeq_value_03480q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Stock |
| 126 | `fnd28_bdeq_value_03481q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Surplus |
| 127 | `fnd28_bdeq_value_03495q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Retained Earnings |
| 128 | `fnd28_bdeq_value_03497q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Unrealized Foreign Exchange Gain/Loss |
| 129 | `fnd28_bdeq_value_03498q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Unrealized Gain/Loss On Marketable Securities |
| 130 | `fnd28_bdeq_value_03499q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Treasury Stock |
| 131 | `fnd28_bdeq_value_03501q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Equity |
| 132 | `fnd28_bdeq_value_03999q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Liabilities & Shareholders' Equity |
| 133 | `fnd28_bdeq_value_18183q` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes-Credit |
| 134 | `fnd28_bdeq_value_18184q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes-Debit |
| 135 | `fnd28_bdeq_value_18232q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Portion of Long Term Debt |
| 136 | `fnd28_bsassetq_value_02005q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Cash & Equivalents Generic |
| 137 | `fnd28_bsassetq_value_02140q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Prepaid Expenses |
| 138 | `fnd28_bsassetq_value_02256q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Investments In Associated Companies |
| 139 | `fnd28_bsassetq_value_02300q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets - As Reported |
| 140 | `fnd28_bsassetq_value_02654q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Intangible Other Assets - Gross |
| 141 | `fnd28_bsassetq_value_02655q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Total Intangible Other Assets Accumulated Amortization |
| 142 | `fnd28_bsassetq_value_18280q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Goodwill/Cost in Excess of Assets Purchased |
| 143 | `fnd28_bsassetq_value_18390q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Construction Work in Progress |
| 144 | `fnd28_bsq_value_02001` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Cash & Short Term Investments |
| 145 | `fnd28_bsq_value_02501` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Property, Plant & Equipment - Net |
| 146 | `fnd28_bsq_value_02652` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Other Assets |
| 147 | `fnd28_bsq_value_02999` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Assets |
| 148 | `fnd28_cfq_value_03151q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Working Capital |
| 149 | `fnd28_cfq_value_03998q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Capital |
| 150 | `fnd28_cfq_value_04057q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Cash Flow (Supplementary to Other Cash Flow Total -04051) |
| 151 | `fnd28_cfq_value_04148q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Interest Paid (Cash Flow) |
| 152 | `fnd28_cfq_value_04150q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Taxation (Cash Flow) |
| 153 | `fnd28_cfq_value_04447q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Uses - Financing |
| 154 | `fnd28_cfq_value_04551q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Dividends Paid - Total |
| 155 | `fnd28_cfq_value_04601q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Expenditures (Additions to Fixed Assets) |
| 156 | `fnd28_cfq_value_04701q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Reduction In Long Term Debt |
| 157 | `fnd28_cfq_value_04751q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common/Preferred Redeemed, Retired, Converted, Etc. |
| 158 | `fnd28_cfq_value_04760q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase in Investments |
| 159 | `fnd28_cfq_value_04795q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Uses - Investing |
| 160 | `fnd28_cfq_value_18199q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Debt |
| 161 | `fnd28_chas_value_05001` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - Year End |
| 162 | `fnd28_chas_value_05201` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Earnings per Share (Supported for Non-U.S. only) |
| 163 | `fnd28_chas_value_05476` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Book Value per Share |
| 164 | `fnd28_chas_value_05501` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Flow per Share |
| 165 | `fnd28_chas_value_05503` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Long Term Liabilities per Share |
| 166 | `fnd28_chas_value_05508` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Sales per Share |
| 167 | `fnd28_eurwsbshta_value_02001` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Cash & Short Term Investments |
| 168 | `fnd28_eurwsbshta_value_02501` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Property, Plant & Equipment - Net |
| 169 | `fnd28_eurwsbshta_value_02502` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Goodwill - Gross |
| 170 | `fnd28_eurwsbshta_value_02652` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Other Assets |
| 171 | `fnd28_eurwsbshta_value_02999` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Assets |
| 172 | `fnd28_ewscurrprfnc_value_09014` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Price/Earnings Ratio Close |
| 173 | `fnd28_ewscurrprfnc_value_09304` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price/Book Value Ratio - Close |
| 174 | `fnd28_ewsgrowth_value_08579` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization Growth (year ago) Profitability |
| 175 | `fnd28_ewsgrowth_value_08601` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings per Share Growth |
| 176 | `fnd28_ewsgrowth_value_08606` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Book Value per Share Growth (year ago) |
| 177 | `fnd28_ewsgrowth_value_08611` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividends per Share Growth |
| 178 | `fnd28_ewsgrowth_value_08616` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Equity Growth (year ago) |
| 179 | `fnd28_ewsgrowth_value_08621` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Assets Growth (year ago) |
| 180 | `fnd28_ewsgrowth_value_08626` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Employees Growth |
| 181 | `fnd28_ewsgrowth_value_08631` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Sales/Revenues Growth |
| 182 | `fnd28_ewsgrowth_value_08636` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Income Growth |
| 183 | `fnd28_ewsgrowth_value_08646` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Operating Income Growth |
| 184 | `fnd28_ewsgrowth_value_08676` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Margin Growth |
| 185 | `fnd28_ewsgrowth_value_08816` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings Per Share - Fiscal - 1 Yr Annual Growth |
| 186 | `fnd28_ewsgrowth_value_08821` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Value of field: Book Value Per Share - Fiscal - 1 Yr Growth Rate Three Year Averages |
| 187 | `fnd28_ewsliquidity_value_08101` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Quick Ratio |
| 188 | `fnd28_ewsliquidity_value_08106` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Current Ratio |
| 189 | `fnd28_ewsliquidity_value_08111` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash & Equivalents % Total Current Assets Company Specific Accounting Practices |
| 190 | `fnd28_ewsliquidity_value_08116` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Inventories % Total Current Assets |
| 191 | `fnd28_ewsliquidity_value_08121` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Receivables % Total Current Assets |
| 192 | `fnd28_ewsliquidity_value_08126` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of field: Inventories - Days Held 5-Year Averages |
| 193 | `fnd28_ewsliquidity_value_08131` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Accounts Receivables Days |
| 194 | `fnd28_ewsprof_value_08301` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Return on Equity Total (%) |
| 195 | `fnd28_ewsprof_value_08306` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Gross Profit Margin |
| 196 | `fnd28_ewsprof_value_08311` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Flow/Sales |
| 197 | `fnd28_ewsprof_value_08316` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Operating Profit Margin |
| 198 | `fnd28_ewsprof_value_08321` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Pre-tax Margin |
| 199 | `fnd28_ewsprof_value_08326` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Return on Assets |
| 200 | `fnd28_ewsprof_value_08331` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Cost of Goods Sold / Sales |
| 201 | `fnd28_ewsprof_value_08336` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Selling, General & Administrative Expenses / Sales |
| 202 | `fnd28_ewsprof_value_08341` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of field: Research & Development Expense / Sales |
| 203 | `fnd28_ewsprof_value_08351` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of field: Sales per Employee Five Year Averages |
| 204 | `fnd28_ewsprof_value_08361` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Operating Income Return on Total Capital |
| 205 | `fnd28_ewsprof_value_08376` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Return on Invested Capital |
| 206 | `fnd28_ewsprof_value_08381` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Earnings Return on Equity |
| 207 | `fnd28_ewsprof_value_08653` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of field: Reinvestment Rate Per Share (Fiscal) |
| 208 | `fnd28_ewsprof_value_08901` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Accounts Payable % Sales |
| 209 | `fnd28_ewsprof_value_08911` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Retained Earnings % Equity |
| 210 | `fnd28_fsa1_value_01001a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales or Revenues |
| 211 | `fnd28_fsa1_value_01051a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Cost Of Goods Sold (Excl Depreciation) |
| 212 | `fnd28_fsa1_value_01084a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Staff Costs |
| 213 | `fnd28_fsa1_value_01148a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Depreciation |
| 214 | `fnd28_fsa1_value_01149a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Intangibles |
| 215 | `fnd28_fsa1_value_01150a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Deferred Charges |
| 216 | `fnd28_fsa1_value_01151a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Depreciation, Depletion & Amortization |
| 217 | `fnd28_fsa1_value_01201a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Research and Development Expense |
| 218 | `fnd28_fsa1_value_01249a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Expenses - Total |
| 219 | `fnd28_fsa1_value_01250a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Income |
| 220 | `fnd28_fsa1_value_01251a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Interest Expense on Debt |
| 221 | `fnd28_fsa1_value_01253a` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of annual field: Extraordinary Credit - Pretax |
| 222 | `fnd28_fsa1_value_01254a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Extraordinary Charge - Pretax |
| 223 | `fnd28_fsa1_value_01266a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Non-Operating Interest Income |
| 224 | `fnd28_fsa1_value_01267a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Pre-tax Equity in Earnings |
| 225 | `fnd28_fsa1_value_01301a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Reserves - Increase/Decrease |
| 226 | `fnd28_fsa1_value_01401a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Pre-tax Income |
| 227 | `fnd28_fsa1_value_01451a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Income Taxes |
| 228 | `fnd28_fsa1_value_01501a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest |
| 229 | `fnd28_fsa1_value_01503a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity In Earnings |
| 230 | `fnd28_fsa1_value_01551a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income before Extraordinary Items/Preferred Dividends |
| 231 | `fnd28_fsa1_value_01706a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income after Preferred Dividends (Basic EPS) |
| 232 | `fnd28_fsa1_value_02001a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Cash & Short Term Investments |
| 233 | `fnd28_fsa1_value_02003a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Cash |
| 234 | `fnd28_fsa1_value_02008a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Short Term Investments |
| 235 | `fnd28_fsa1_value_02051a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Receivables (Net) |
| 236 | `fnd28_fsa1_value_02097a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Raw Materials |
| 237 | `fnd28_fsa1_value_02098a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Work in Process |
| 238 | `fnd28_fsa1_value_02099a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Finished Goods |
| 239 | `fnd28_fsa1_value_02100a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Progress Payments & Other |
| 240 | `fnd28_fsa1_value_02101a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Inventories Total |
| 241 | `fnd28_fsa1_value_02140a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Prepaid Expenses |
| 242 | `fnd28_fsa1_value_02201a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Current Assets Total |
| 243 | `fnd28_fsa1_value_02250a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Investments |
| 244 | `fnd28_fsa1_value_02256a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Investments In Associated Companies |
| 245 | `fnd28_fsa1_value_02258a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Receivables |
| 246 | `fnd28_fsa1_value_02301a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Property, Plant and Equipment - Gross |
| 247 | `fnd28_fsa1_value_02401a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accumulated Depreciation |
| 248 | `fnd28_fsa1_value_02501a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Property, Plant & Equipment - Net |
| 249 | `fnd28_fsa1_value_02502a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Goodwill - Gross |
| 250 | `fnd28_fsa1_value_02503a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Goodwill - Accumulated Amortization |
| 251 | `fnd28_fsa1_value_02647a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Charges |
| 252 | `fnd28_fsa1_value_02648a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Tangible Other Assets |
| 253 | `fnd28_fsa1_value_02649a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Intangible Other Assets - Net |
| 254 | `fnd28_fsa1_value_02999a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets |
| 255 | `fnd28_fsa1_value_03040a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accounts Payable |
| 256 | `fnd28_fsa1_value_03051a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Short Term Debt & Current Portion of Long Term Debt |
| 257 | `fnd28_fsa1_value_03054a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accrued Payroll |
| 258 | `fnd28_fsa1_value_03061a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends Payable |
| 259 | `fnd28_fsa1_value_03063a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Income Taxes Payable |
| 260 | `fnd28_fsa1_value_03101a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Current Liabilities - Total |
| 261 | `fnd28_fsa1_value_03245a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt Excluding Capitalized Leases |
| 262 | `fnd28_fsa1_value_03249a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Capitalized Lease Obligations |
| 263 | `fnd28_fsa1_value_03262a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Income |
| 264 | `fnd28_fsa1_value_03263a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Taxes |
| 265 | `fnd28_fsa1_value_03351a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Liabilities |
| 266 | `fnd28_fsa1_value_03426a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest |
| 267 | `fnd28_fsa1_value_03480a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Common Stock |
| 268 | `fnd28_fsa1_value_03481a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Surplus |
| 269 | `fnd28_fsa1_value_03492a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Revaluation Reserves |
| 270 | `fnd28_fsa1_value_03493a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Other Appropriated Reserves |
| 271 | `fnd28_fsa1_value_03494a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Unappropriated (Free) Reserves |
| 272 | `fnd28_fsa1_value_03495a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Retained Earnings |
| 273 | `fnd28_fsa1_value_03496a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: ESOP Guarantees |
| 274 | `fnd28_fsa1_value_03497a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Unrealized Foreign Exchange Gain/Loss |
| 275 | `fnd28_fsa1_value_03499a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Treasury Stock |
| 276 | `fnd28_fsa1_value_03501a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity |
| 277 | `fnd28_fsa1_value_03998a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Total Capital |
| 278 | `fnd28_fsa1_value_04001a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income/Starting Line |
| 279 | `fnd28_fsa1_value_04049a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Depreciation and Depletion |
| 280 | `fnd28_fsa1_value_04050a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Intangible Assets |
| 281 | `fnd28_fsa1_value_04151a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Cash Flow - Total |
| 282 | `fnd28_fsa1_value_04302a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Proceeds From Sale/Issuance of Stock |
| 283 | `fnd28_fsa1_value_04351a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Disposal of Fixed Assets |
| 284 | `fnd28_fsa1_value_04355a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Assets From Acquisitions |
| 285 | `fnd28_fsa1_value_04401a` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Borrowings |
| 286 | `fnd28_fsa1_value_04440a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Decrease in Investments |
| 287 | `fnd28_fsa1_value_04446a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Sources - Financing |
| 288 | `fnd28_fsa1_value_04447a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Uses - Financing |
| 289 | `fnd28_fsa1_value_04551a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividends Paid - Total |
| 290 | `fnd28_fsa1_value_04601a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditures (Additions to Fixed Assets) |
| 291 | `fnd28_fsa1_value_04651a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Additions to Other Assets |
| 292 | `fnd28_fsa1_value_04701a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Reduction In Long Term Debt |
| 293 | `fnd28_fsa1_value_04751a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Common/Preferred Redeemed, Retired, Converted, Etc. |
| 294 | `fnd28_fsa1_value_04760a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Increase in Investments |
| 295 | `fnd28_fsa1_value_04795a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Uses - Investing |
| 296 | `fnd28_fsa1_value_04796a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Sources - Investing |
| 297 | `fnd28_fsa1_value_04821a` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of annual field: Increase/Decrease In Short Term Borrowings |
| 298 | `fnd28_fsa1_value_04825a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Decrease/Increase In Receivables |
| 299 | `fnd28_fsa1_value_04826a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Decrease/Increase In Inventories |
| 300 | `fnd28_fsa1_value_04827a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Increase/Decrease In Accounts Payable |
| 301 | `fnd28_fsa1_value_04830a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Decrease/Increase In Other Assets/Liabilities |
| 302 | `fnd28_fsa1_value_04831a` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of annual field: Funds from/for Other Operating Activities |
| 303 | `fnd28_fsa1_value_04840a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Effect of Exchange Rate on Cash |
| 304 | `fnd28_fsa1_value_04851a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Increase/Decrease in Cash & Short-Term Investments |
| 305 | `fnd28_fsa1_value_04860a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Cash Flow - Operating Activities |
| 306 | `fnd28_fsa1_value_04870a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Net Cash Flow Investing |
| 307 | `fnd28_fsa1_value_04890a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Cash Flow - Financing |
| 308 | `fnd28_fsq1_value_01253q` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of quarterly field: Extraordinary Credit - Pretax |
| 309 | `fnd28_fsq1_value_01254q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Extraordinary Charge - Pretax |
| 310 | `fnd28_fsq1_value_01267q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Equity in Earnings |
| 311 | `fnd28_fsq1_value_01503q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Equity In Earnings |
| 312 | `fnd28_fsq1_value_02140q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Prepaid Expenses |
| 313 | `fnd28_fsq1_value_02256q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Investments In Associated Companies |
| 314 | `fnd28_fsq1_value_03040q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Accounts Payable |
| 315 | `fnd28_fsq1_value_03051q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Short Term Debt & Current Portion of Long Term Debt |
| 316 | `fnd28_fsq1_value_03063q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income Taxes Payable |
| 317 | `fnd28_fsq1_value_03101q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Liabilities - Total |
| 318 | `fnd28_fsq1_value_03245q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Debt Excluding Capitalized Leases |
| 319 | `fnd28_fsq1_value_03249q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capitalized Lease Obligations |
| 320 | `fnd28_fsq1_value_03263q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes |
| 321 | `fnd28_fsq1_value_03351q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Liabilities |
| 322 | `fnd28_fsq1_value_03401q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Non-Equity Reserves |
| 323 | `fnd28_fsq1_value_03426q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Minority Interest |
| 324 | `fnd28_fsq1_value_03451q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Preferred Stock |
| 325 | `fnd28_fsq1_value_03480q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Stock |
| 326 | `fnd28_fsq1_value_03481q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Surplus |
| 327 | `fnd28_fsq1_value_03495q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Retained Earnings |
| 328 | `fnd28_fsq1_value_03497q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Unrealized Foreign Exchange Gain/Loss |
| 329 | `fnd28_fsq1_value_03498q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Unrealized Gain/Loss On Marketable Securities |
| 330 | `fnd28_fsq1_value_03499q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Treasury Stock |
| 331 | `fnd28_fsq1_value_03501q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Equity |
| 332 | `fnd28_fsq1_value_04355q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Assets From Acquisitions |
| 333 | `fnd28_fsq1_value_04447q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Uses - Financing |
| 334 | `fnd28_fsq1_value_04551q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Dividends Paid - Total |
| 335 | `fnd28_fsq1_value_04601q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Expenditures (Additions to Fixed Assets) |
| 336 | `fnd28_fsq1_value_04701q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Reduction In Long Term Debt |
| 337 | `fnd28_fsq1_value_04751q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common/Preferred Redeemed, Retired, Converted, Etc. |
| 338 | `fnd28_fsq1_value_04760q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase in Investments |
| 339 | `fnd28_fsq1_value_04795q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Uses - Investing |
| 340 | `fnd28_fsq1_value_04860q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Cash Flow - Operating Activities |
| 341 | `fnd28_fsq1_value_04870q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Net Cash Flow Investing |
| 342 | `fnd28_fsq1_value_04890q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Cash Flow - Financing |
| 343 | `fnd28_fsq1_value_18150q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income From Continuing Operations |
| 344 | `fnd28_fsq1_value_18183q` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes-Credit |
| 345 | `fnd28_fsq1_value_18184q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes-Debit |
| 346 | `fnd28_fsq1_value_18280q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Goodwill/Cost in Excess of Assets Purchased |
| 347 | `fnd28_fsq1_value_18440q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Fiscal Period - Fully Diluted |
| 348 | `fnd28_isht_value_05002a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Market Price - High |
| 349 | `fnd28_isht_value_05003a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Market Price - Low |
| 350 | `fnd28_ishtq_value_01254q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Extraordinary Charge - Pretax |
| 351 | `fnd28_ishtq_value_01705q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income Used to Calculate Fully Diluted Earnings per Share |
| 352 | `fnd28_ishtq_value_18150q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income From Continuing Operations |
| 353 | `fnd28_ishtq_value_18155q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Income before Depreciation/Amortization (Operating EBITDA) |
| 354 | `fnd28_ishtq_value_18191q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings before Interest and Taxes (EBIT) |
| 355 | `fnd28_ishtq_value_18198q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings before Interest, Taxes, Depreciation & Amortization (EBITDA) |
| 356 | `fnd28_keyfinancials_value_07210a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization (U.S.$) |
| 357 | `fnd28_keyfinancials_value_07220a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity (U.S.$) |
| 358 | `fnd28_keyfinancials_value_07230a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets (U.S.$) |
| 359 | `fnd28_keyfinancials_value_07240a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales or Revenues (U.S.$) |
| 360 | `fnd28_keyfinancials_value_07250a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income (U.S.$) |
| 361 | `fnd28_ndda1_value_01001a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales or Revenues |
| 362 | `fnd28_ndda1_value_01051a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Cost Of Goods Sold (Excl Depreciation) |
| 363 | `fnd28_ndda1_value_01084a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Staff Costs |
| 364 | `fnd28_ndda1_value_01148a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Depreciation |
| 365 | `fnd28_ndda1_value_01149a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Intangibles |
| 366 | `fnd28_ndda1_value_01150a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Deferred Charges |
| 367 | `fnd28_ndda1_value_01151a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Depreciation, Depletion & Amortization |
| 368 | `fnd28_ndda1_value_01201a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Research and Development Expense |
| 369 | `fnd28_ndda1_value_01249a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Expenses - Total |
| 370 | `fnd28_ndda1_value_01250a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Income |
| 371 | `fnd28_ndda1_value_01251a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Interest Expense on Debt |
| 372 | `fnd28_ndda1_value_01253a` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of annual field: Extraordinary Credit - Pretax |
| 373 | `fnd28_ndda1_value_01254a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Extraordinary Charge - Pretax |
| 374 | `fnd28_ndda1_value_01255a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Interest Capitalized |
| 375 | `fnd28_ndda1_value_01266a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Non-Operating Interest Income |
| 376 | `fnd28_ndda1_value_01267a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Pre-tax Equity in Earnings |
| 377 | `fnd28_ndda1_value_01301a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Reserves - Increase/Decrease |
| 378 | `fnd28_ndda1_value_01401a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Pre-tax Income |
| 379 | `fnd28_ndda1_value_01451a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Income Taxes |
| 380 | `fnd28_ndda1_value_01501a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest |
| 381 | `fnd28_ndda1_value_01503a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity In Earnings |
| 382 | `fnd28_ndda1_value_01504a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: After Tax Other Income/Expense |
| 383 | `fnd28_ndda1_value_01505a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Discontinued Operations |
| 384 | `fnd28_ndda1_value_01551a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income before Extraordinary Items/Preferred Dividends |
| 385 | `fnd28_ndda1_value_01701a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Preferred Dividend Requirements |
| 386 | `fnd28_ndda1_value_01706a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income after Preferred Dividends (Basic EPS) |
| 387 | `fnd28_ndda1_value_02001a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Cash & Short Term Investments |
| 388 | `fnd28_ndda1_value_02003a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Cash |
| 389 | `fnd28_ndda1_value_02008a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Short Term Investments |
| 390 | `fnd28_ndda1_value_02051a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Receivables (Net) |
| 391 | `fnd28_ndda1_value_02097a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Raw Materials |
| 392 | `fnd28_ndda1_value_02098a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Work in Process |
| 393 | `fnd28_ndda1_value_02099a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Finished Goods |
| 394 | `fnd28_ndda1_value_02100a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Progress Payments & Other |
| 395 | `fnd28_ndda1_value_02101a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Inventories Total |
| 396 | `fnd28_ndda1_value_02140a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Prepaid Expenses |
| 397 | `fnd28_ndda1_value_02201a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Current Assets Total |
| 398 | `fnd28_ndda1_value_02250a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Investments |
| 399 | `fnd28_ndda1_value_02256a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Investments In Associated Companies |
| 400 | `fnd28_ndda1_value_02258a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Receivables |
| 401 | `fnd28_ndda1_value_02301a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Property, Plant and Equipment - Gross |
| 402 | `fnd28_ndda1_value_02401a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accumulated Depreciation |
| 403 | `fnd28_ndda1_value_02501a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Property, Plant & Equipment - Net |
| 404 | `fnd28_ndda1_value_02502a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Goodwill - Gross |
| 405 | `fnd28_ndda1_value_02503a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Goodwill - Accumulated Amortization |
| 406 | `fnd28_ndda1_value_02647a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Charges |
| 407 | `fnd28_ndda1_value_02648a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Tangible Other Assets |
| 408 | `fnd28_ndda1_value_02649a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Intangible Other Assets - Net |
| 409 | `fnd28_ndda1_value_02999a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets |
| 410 | `fnd28_ndda1_value_03040a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accounts Payable |
| 411 | `fnd28_ndda1_value_03051a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Short Term Debt & Current Portion of Long Term Debt |
| 412 | `fnd28_ndda1_value_03054a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accrued Payroll |
| 413 | `fnd28_ndda1_value_03063a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Income Taxes Payable |
| 414 | `fnd28_ndda1_value_03101a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Current Liabilities - Total |
| 415 | `fnd28_ndda1_value_03245a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt Excluding Capitalized Leases |
| 416 | `fnd28_ndda1_value_03249a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Capitalized Lease Obligations |
| 417 | `fnd28_ndda1_value_03262a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Income |
| 418 | `fnd28_ndda1_value_03263a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Taxes |
| 419 | `fnd28_ndda1_value_03351a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Liabilities |
| 420 | `fnd28_ndda1_value_03401a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Non-Equity Reserves |
| 421 | `fnd28_ndda1_value_03426a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest |
| 422 | `fnd28_ndda1_value_03451a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Preferred Stock |
| 423 | `fnd28_ndda1_value_03480a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Common Stock |
| 424 | `fnd28_ndda1_value_03481a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Surplus |
| 425 | `fnd28_ndda1_value_03492a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Revaluation Reserves |
| 426 | `fnd28_ndda1_value_03493a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Other Appropriated Reserves |
| 427 | `fnd28_ndda1_value_03494a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Unappropriated (Free) Reserves |
| 428 | `fnd28_ndda1_value_03495a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Retained Earnings |
| 429 | `fnd28_ndda1_value_03496a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: ESOP Guarantees |
| 430 | `fnd28_ndda2_value_03497a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Unrealized Foreign Exchange Gain/Loss |
| 431 | `fnd28_ndda2_value_03498a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Unrealized Gain/Loss On Marketable Securities |
| 432 | `fnd28_ndda2_value_03499a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Treasury Stock |
| 433 | `fnd28_ndda2_value_03501a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity |
| 434 | `fnd28_ndda2_value_03998a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Total Capital |
| 435 | `fnd28_ndda2_value_04001a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income/Starting Line |
| 436 | `fnd28_ndda2_value_04049a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Depreciation and Depletion |
| 437 | `fnd28_ndda2_value_04050a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Intangible Assets |
| 438 | `fnd28_ndda2_value_04151a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Cash Flow - Total |
| 439 | `fnd28_ndda2_value_04301a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Proceeds From Stock Options |
| 440 | `fnd28_ndda2_value_04302a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Proceeds From Sale/Issuance of Stock |
| 441 | `fnd28_ndda2_value_04351a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Disposal of Fixed Assets |
| 442 | `fnd28_ndda2_value_04355a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Assets From Acquisitions |
| 443 | `fnd28_ndda2_value_04401a` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Borrowings |
| 444 | `fnd28_ndda2_value_04440a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Decrease in Investments |
| 445 | `fnd28_ndda2_value_04446a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Sources - Financing |
| 446 | `fnd28_ndda2_value_04447a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Uses - Financing |
| 447 | `fnd28_ndda2_value_04551a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividends Paid - Total |
| 448 | `fnd28_ndda2_value_04601a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditures (Additions to Fixed Assets) |
| 449 | `fnd28_ndda2_value_04651a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Additions to Other Assets |
| 450 | `fnd28_ndda2_value_04701a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Reduction In Long Term Debt |
| 451 | `fnd28_ndda2_value_04751a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Common/Preferred Redeemed, Retired, Converted, Etc. |
| 452 | `fnd28_ndda2_value_04760a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Increase in Investments |
| 453 | `fnd28_ndda2_value_04795a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Uses - Investing |
| 454 | `fnd28_ndda2_value_04796a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Sources - Investing |
| 455 | `fnd28_ndda2_value_04821a` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of annual field: Increase/Decrease In Short Term Borrowings |
| 456 | `fnd28_ndda2_value_04825a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Decrease/Increase In Receivables |
| 457 | `fnd28_ndda2_value_04826a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Decrease/Increase In Inventories |
| 458 | `fnd28_ndda2_value_04827a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Increase/Decrease In Accounts Payable |
| 459 | `fnd28_ndda2_value_04830a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Decrease/Increase In Other Assets/Liabilities |
| 460 | `fnd28_ndda2_value_04831a` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of annual field: Funds from/for Other Operating Activities |
| 461 | `fnd28_ndda2_value_04840a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Effect of Exchange Rate on Cash |
| 462 | `fnd28_ndda2_value_04851a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Increase/Decrease in Cash & Short Term Investments |
| 463 | `fnd28_ndda2_value_04860a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Cash Flow - Operating Activities |
| 464 | `fnd28_ndda2_value_04870a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Net Cash Flow Investing |
| 465 | `fnd28_ndda2_value_04890a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Cash Flow - Financing |
| 466 | `fnd28_ndda2_value_05002a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Market Price - High |
| 467 | `fnd28_ndda2_value_05003a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Market Price - Low |
| 468 | `fnd28_ndda2_value_05202a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Earnings per Share Fiscal Period End |
| 469 | `fnd28_ndda2_value_05401a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Preferred Dividends (Cash) |
| 470 | `fnd28_nddq1_value_01253q` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of quarterly field: Extraordinary Credit - Pretax |
| 471 | `fnd28_nddq1_value_01254q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Extraordinary Charge - Pretax |
| 472 | `fnd28_nddq1_value_01267q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Equity in Earnings |
| 473 | `fnd28_nddq1_value_01503q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Equity In Earnings |
| 474 | `fnd28_nddq1_value_01705q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income Used to Calculate Fully Diluted Earnings per Share |
| 475 | `fnd28_nddq1_value_02256q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Investments In Associated Companies |
| 476 | `fnd28_nddq1_value_02300q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets - As Reported |
| 477 | `fnd28_nddq1_value_02654q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Intangible Other Assets - Gross |
| 478 | `fnd28_nddq1_value_02655q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Total Intangible Other Assets Accumulated Amortization |
| 479 | `fnd28_nddq1_value_03040q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Accounts Payable |
| 480 | `fnd28_nddq1_value_03051q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Short Term Debt & Current Portion of Long Term Debt |
| 481 | `fnd28_nddq1_value_03063q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income Taxes Payable |
| 482 | `fnd28_nddq1_value_03069q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Accrued Expenses |
| 483 | `fnd28_nddq1_value_03101q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Liabilities - Total |
| 484 | `fnd28_nddq1_value_03245q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Debt Excluding Capitalized Leases |
| 485 | `fnd28_nddq1_value_03249q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capitalized Lease Obligations |
| 486 | `fnd28_nddq1_value_03263q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes |
| 487 | `fnd28_nddq1_value_03351q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Liabilities |
| 488 | `fnd28_nddq1_value_03401q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Non-Equity Reserves |
| 489 | `fnd28_nddq1_value_03426q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Minority Interest |
| 490 | `fnd28_nddq1_value_03451q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Preferred Stock |
| 491 | `fnd28_nddq1_value_03480q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Stock |
| 492 | `fnd28_nddq1_value_03481q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Surplus |
| 493 | `fnd28_nddq1_value_03495q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Retained Earnings |
| 494 | `fnd28_nddq1_value_03497q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Unrealized Foreign Exchange Gain/Loss |
| 495 | `fnd28_nddq1_value_03498q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Unrealized Gain/Loss On Marketable Securities |
| 496 | `fnd28_nddq1_value_03499q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Treasury Stock |
| 497 | `fnd28_nddq1_value_03501q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Equity |
| 498 | `fnd28_nddq1_value_04057q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Cash Flow (Supplementary to Other Cash Flow Total -04051) |
| 499 | `fnd28_nddq1_value_04150q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Taxation (Cash Flow) |
| 500 | `fnd28_nddq1_value_04355q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Assets From Acquisitions |
| 501 | `fnd28_nddq1_value_04447q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Uses - Financing |
| 502 | `fnd28_nddq1_value_04551q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Dividends Paid - Total |
| 503 | `fnd28_nddq1_value_04601q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Expenditures (Additions to Fixed Assets) |
| 504 | `fnd28_nddq1_value_04701q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Reduction In Long Term Debt |
| 505 | `fnd28_nddq1_value_04751q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common/Preferred Redeemed, Retired, Converted, Etc. |
| 506 | `fnd28_nddq1_value_04760q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase in Investments |
| 507 | `fnd28_nddq1_value_04795q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Uses - Investing |
| 508 | `fnd28_nddq1_value_04860q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Cash Flow - Operating Activities |
| 509 | `fnd28_nddq1_value_04870q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Net Cash Flow Investing |
| 510 | `fnd28_nddq1_value_04890q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Cash Flow - Financing |
| 511 | `fnd28_nddq1_value_05301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Shares Outstanding |
| 512 | `fnd28_nddq1_value_05303q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Treasury Shares |
| 513 | `fnd28_nddq1_value_05309q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Par Value |
| 514 | `fnd28_nddq2_value_18150q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income From Continuing Operations |
| 515 | `fnd28_nddq2_value_18183q` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes-Credit |
| 516 | `fnd28_nddq2_value_18184q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Deferred Taxes-Debit |
| 517 | `fnd28_nddq2_value_18208q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Continuing Operations |
| 518 | `fnd28_nddq2_value_18232q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Portion of Long Term Debt |
| 519 | `fnd28_nddq2_value_18280q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Goodwill/Cost in Excess of Assets Purchased |
| 520 | `fnd28_nddq2_value_18390q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Construction Work in Progress |
| 521 | `fnd28_nddq2_value_18440q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Fiscal Period - Fully Diluted |
| 522 | `fnd28_newa1_value_01100a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Gross Income |
| 523 | `fnd28_newa1_value_01230a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Operating Expenses |
| 524 | `fnd28_newa1_value_01262a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Other Income/Expense Net |
| 525 | `fnd28_newa1_value_02149a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Current Assets |
| 526 | `fnd28_newa1_value_02652a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Assets |
| 527 | `fnd28_newa1_value_03066a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Current Liabilities |
| 528 | `fnd28_newa1_value_03151a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Working Capital |
| 529 | `fnd28_newa1_value_03251a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt |
| 530 | `fnd28_newa1_value_03255a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt |
| 531 | `fnd28_newa1_value_03273a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Liabilities |
| 532 | `fnd28_newa1_value_03995a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Total Shareholders' Equity |
| 533 | `fnd28_newa1_value_03999a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Liabilities & Shareholders' Equity |
| 534 | `fnd28_newa1_value_04051a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Depreciation, Depletion & Amortization |
| 535 | `fnd28_newa1_value_04101a` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Income Taxes and Investment Tax Credit |
| 536 | `fnd28_newa1_value_04199a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Income Taxes (Cash Flow) |
| 537 | `fnd28_newa1_value_04251a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Net Proceeds from Sale/Issuance of Common & Preferred |
| 538 | `fnd28_newa1_value_04501a` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of annual field: Total Sources Uses of Funds |
| 539 | `fnd28_newa1_value_04811a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Uses Supplementary Cash Flow Fields |
| 540 | `fnd28_newa1_value_05502a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Cash Flow per Share Fiscal Period |
| 541 | `fnd28_newa1_value_07210a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization (U.S.$) |
| 542 | `fnd28_newa1_value_07220a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity (U.S.$) |
| 543 | `fnd28_newa1_value_07230a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets (U.S.$) |
| 544 | `fnd28_newa1_value_07240a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales or Revenues (U.S.$) |
| 545 | `fnd28_newa1_value_07250a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income (U.S.$) |
| 546 | `fnd28_newa1_value_08106a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Current Ratio |
| 547 | `fnd28_newa1_value_08111a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Cash & Equivalents % Total Current Assets Company Specific Accounting Practices |
| 548 | `fnd28_newa1_value_08201a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity % Total Capital |
| 549 | `fnd28_newa1_value_08205a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity % Total Capital - 5 Yr Avg |
| 550 | `fnd28_newa1_value_08211a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest % Total Capital |
| 551 | `fnd28_newa1_value_08215a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest % Total Capital - 5 Yr Avg |
| 552 | `fnd28_newa1_value_08216a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Total Capital |
| 553 | `fnd28_newa1_value_08220a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Total Capital - 5 Yr Avg |
| 554 | `fnd28_newa1_value_08221a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Capital |
| 555 | `fnd28_newa1_value_08225a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Capital - 5 Yr Avg |
| 556 | `fnd28_newa1_value_08226a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Common Equity |
| 557 | `fnd28_newa1_value_08230a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Common Equity - 5 Yr Avg |
| 558 | `fnd28_newa1_value_08231a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Common Equity |
| 559 | `fnd28_newa1_value_08235a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Common Equity - 5 Yr Avg |
| 560 | `fnd28_newa1_value_08236a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Assets |
| 561 | `fnd28_newa1_value_08240a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Assets - 5 Yr Avg |
| 562 | `fnd28_newa1_value_08241a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity % Total Assets |
| 563 | `fnd28_newa1_value_08245a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity % Total Assets - 5 Yr Avg |
| 564 | `fnd28_newa1_value_08246a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividend Coverage Ratio |
| 565 | `fnd28_newa1_value_08250a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividend Coverage Ratio |
| 566 | `fnd28_newa1_value_08251a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Fixed Charge Coverage Ratio |
| 567 | `fnd28_newa1_value_08255a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Fixed Charge Coverage Ratio - 5 Yr Avg |
| 568 | `fnd28_newa1_value_08256a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Payout (% Earnings) |
| 569 | `fnd28_newa1_value_08260a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Payout (% Earnings) - Total Dollar - 5 Yr Avg |
| 570 | `fnd28_newa1_value_08261a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Cash/Fixed Charges |
| 571 | `fnd28_newa1_value_08265a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Cash/Fixed Charges - 5 Yr Avg |
| 572 | `fnd28_newa1_value_08266a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Fixed Assets % Common Equity Company Specific Accounting Practices |
| 573 | `fnd28_newa1_value_08270a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Fixed Assets % Common Equity - 5 Yr Avg |
| 574 | `fnd28_newa1_value_08271a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Working Capital % Total Capital Five Year Averages |
| 575 | `fnd28_newa1_value_08275a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of annual field: Working Capital % Total Capital - 5 Yr Avg Liquidity Annual Statistics |
| 576 | `fnd28_newa1_value_08287a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets / Common Equity Ratio |
| 577 | `fnd28_newa1_value_08291a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: EBIT / Total Interest Expense Ratio |
| 578 | `fnd28_newa1_value_08301a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Return on Equity Total (%) |
| 579 | `fnd28_newa1_value_08306a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Gross Profit Margin |
| 580 | `fnd28_newa1_value_08311a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Flow/Sales |
| 581 | `fnd28_newa1_value_08316a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Profit Margin |
| 582 | `fnd28_newa1_value_08321a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Pre-tax Margin |
| 583 | `fnd28_newa1_value_08326a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Return on Assets |
| 584 | `fnd28_newa1_value_08346a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Value of annual field: Tax Rate |
| 585 | `fnd28_newa1_value_08366a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Margin |
| 586 | `fnd28_newa1_value_08371a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Return on Equity - per Share |
| 587 | `fnd28_newa1_value_08381a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Earnings Return on Equity |
| 588 | `fnd28_newa1_value_08401a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Asset Turnover |
| 589 | `fnd28_newa1_value_08416a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure % Total Assets |
| 590 | `fnd28_newa1_value_08421a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure % Sales |
| 591 | `fnd28_newa1_value_08579a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization Growth (year ago) Profitability |
| 592 | `fnd28_newa2_value_08601a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share Growth |
| 593 | `fnd28_newa2_value_08606a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Book Value per Share Growth (year ago) |
| 594 | `fnd28_newa2_value_08611a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends per Share Growth |
| 595 | `fnd28_newa2_value_08616a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity Growth (year ago) |
| 596 | `fnd28_newa2_value_08621a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets Growth (year ago) |
| 597 | `fnd28_newa2_value_08631a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales/Revenues Growth |
| 598 | `fnd28_newa2_value_08636a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income Growth |
| 599 | `fnd28_newa2_value_08651a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Reinvestment Rate - per Share |
| 600 | `fnd28_newa2_value_08676a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Margin Growth |
| 601 | `fnd28_newa2_value_08801a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of annual field: Total Investment Return Year Ago Growth Rates |
| 602 | `fnd28_newa2_value_08805a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Total Investment Return - 5 Yr Annual Return |
| 603 | `fnd28_newa2_value_08806a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price Volatility |
| 604 | `fnd28_newa2_value_08906a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividends % Cash Flow |
| 605 | `fnd28_newa2_value_08910a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Dividends/Cash Flow - 5 Yr Avg |
| 606 | `fnd28_newa2_value_09100a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - High |
| 607 | `fnd28_newa2_value_09101a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - Low |
| 608 | `fnd28_newa2_value_09104a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio Close |
| 609 | `fnd28_newa2_value_09106a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - Avg High-Low |
| 610 | `fnd28_newa2_value_09111a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - 5 Yr Avg High |
| 611 | `fnd28_newa2_value_09116a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - 5 Yr Avg Low |
| 612 | `fnd28_newa2_value_09121a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - 5 Yr Avg - Close |
| 613 | `fnd28_newa2_value_09126a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Earnings Ratio - 5 Yr Avg High-Low |
| 614 | `fnd28_newa2_value_09200a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - High |
| 615 | `fnd28_newa2_value_09201a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - Low |
| 616 | `fnd28_newa2_value_09204a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - Close |
| 617 | `fnd28_newa2_value_09206a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - Avg High-Low |
| 618 | `fnd28_newa2_value_09211a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - 5 Yr Avg High |
| 619 | `fnd28_newa2_value_09216a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - 5 Yr Avg Low |
| 620 | `fnd28_newa2_value_09221a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Yield - 5 Yr Avg - Close |
| 621 | `fnd28_newa2_value_09226a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Earnings Yield - 5 Yr Avg High-Low |
| 622 | `fnd28_newa2_value_09300a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - High |
| 623 | `fnd28_newa2_value_09301a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - Low |
| 624 | `fnd28_newa2_value_09304a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - Close |
| 625 | `fnd28_newa2_value_09306a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - Avg High-Low |
| 626 | `fnd28_newa2_value_09311a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - 5 Yr Avg High |
| 627 | `fnd28_newa2_value_09316a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - 5 Yr Avg Low |
| 628 | `fnd28_newa2_value_09321a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - 5 Yr Avg - Close |
| 629 | `fnd28_newa2_value_09326a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Book Value Ratio - 5 Yr Avg High-Low |
| 630 | `fnd28_newa2_value_09400a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - High |
| 631 | `fnd28_newa2_value_09401a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - Low |
| 632 | `fnd28_newa2_value_09404a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - Close |
| 633 | `fnd28_newa2_value_09406a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - Avg High-Low |
| 634 | `fnd28_newa2_value_09504a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Payout per Share |
| 635 | `fnd28_newa2_value_09604a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Cash Flow Ratio |
| 636 | `fnd28_newa2_value_09621a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Cash Flow Ratio - 5 Yr Avg |
| 637 | `fnd28_newa2_value_09704a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization to Common Equity |
| 638 | `fnd28_newa2_value_09721a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Market Capitalization/Common Equity - 5 Yr Average Growth Rates Annual Statistics |
| 639 | `fnd28_newa2_value_09904a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Price/Sales per Share Ratio |
| 640 | `fnd28_newa3_value_15121a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Capital % Total Assets |
| 641 | `fnd28_newa3_value_15124a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Capital % Total Assets |
| 642 | `fnd28_newa3_value_18155a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Income before Depreciation/Amortization (Operating EBITDA) |
| 643 | `fnd28_newa3_value_18191a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings before Interest and Taxes (EBIT) |
| 644 | `fnd28_newa3_value_18198a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings before Interest, Taxes, Depreciation & Amortization (EBITDA) |
| 645 | `fnd28_newa3_value_18199a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Debt |
| 646 | `fnd28_newq_value_01601q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Extraordinary Items & Gain/Loss Sale of Assets Supplementary Income Statement Fields |
| 647 | `fnd28_newq_value_02005q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Cash & Equivalents Generic |
| 648 | `fnd28_newq_value_03066q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Current Liabilities |
| 649 | `fnd28_newq_value_03151q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Working Capital |
| 650 | `fnd28_newq_value_03251q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Debt |
| 651 | `fnd28_newq_value_03255q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Debt |
| 652 | `fnd28_newq_value_03273q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Liabilities |
| 653 | `fnd28_newq_value_03995q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Total Shareholders' Equity |
| 654 | `fnd28_newq_value_03999q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Liabilities & Shareholders' Equity |
| 655 | `fnd28_newq_value_05486q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Tangible Book Value per Share |
| 656 | `fnd28_newq_value_05502q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Flow per Share Fiscal Period |
| 657 | `fnd28_newq_value_07230q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets (U.S.$) |
| 658 | `fnd28_newq_value_08106q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Ratio |
| 659 | `fnd28_newq_value_08111q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Cash & Equivalents % Total Current Assets Company Specific Accounting Practices |
| 660 | `fnd28_newq_value_08226q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Debt % Common Equity |
| 661 | `fnd28_newq_value_08231q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Debt % Common Equity |
| 662 | `fnd28_newq_value_08236q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Debt % Total Assets |
| 663 | `fnd28_newq_value_08241q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Equity % Total Assets |
| 664 | `fnd28_newq_value_08251q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Fixed Charge Coverage Ratio |
| 665 | `fnd28_newq_value_08261q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Cash/Fixed Charges |
| 666 | `fnd28_newq_value_08266q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Fixed Assets % Common Equity Company Specific Accounting Practices |
| 667 | `fnd28_newq_value_08287q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets / Common Equity Ratio |
| 668 | `fnd28_newq_value_08301q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Return on Equity Total (%) |
| 669 | `fnd28_newq_value_08306q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Gross Profit Margin |
| 670 | `fnd28_newq_value_08311q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Flow/Sales |
| 671 | `fnd28_newq_value_08316q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Profit Margin |
| 672 | `fnd28_newq_value_08321q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Margin |
| 673 | `fnd28_newq_value_08326q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Return on Assets |
| 674 | `fnd28_newq_value_08346q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Tax Rate |
| 675 | `fnd28_newq_value_08366q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Margin |
| 676 | `fnd28_newq_value_08371q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Return on Equity - per Share |
| 677 | `fnd28_newq_value_08381q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Earnings Return on Equity |
| 678 | `fnd28_newq_value_08401q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Asset Turnover |
| 679 | `fnd28_newq_value_08416q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Expenditure % Total Assets |
| 680 | `fnd28_newq_value_08421q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Expenditure % Sales |
| 681 | `fnd28_newq_value_08579q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Market Capitalization Growth (year ago) Profitability |
| 682 | `fnd28_newq_value_08601q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings per Share Growth |
| 683 | `fnd28_newq_value_08606q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Book Value per Share Growth (year ago) |
| 684 | `fnd28_newq_value_08611q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Dividends per Share Growth |
| 685 | `fnd28_newq_value_08616q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Equity Growth (year ago) |
| 686 | `fnd28_newq_value_08621q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets Growth (year ago) |
| 687 | `fnd28_newq_value_08631q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Sales/Revenues Growth |
| 688 | `fnd28_newq_value_08636q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income Growth |
| 689 | `fnd28_newq_value_08651q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Reinvestment Rate - per Share |
| 690 | `fnd28_newq_value_08676q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Margin Growth |
| 691 | `fnd28_newq_value_08801q` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Total Investment Return Year Ago Growth Rates |
| 692 | `fnd28_newq_value_18155q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Income before Depreciation/Amortization (Operating EBITDA) |
| 693 | `fnd28_newq_value_18191q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings before Interest and Taxes (EBIT) |
| 694 | `fnd28_newq_value_18198q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings before Interest, Taxes, Depreciation & Amortization (EBITDA) |
| 695 | `fnd28_newq_value_18199q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Debt |
| 696 | `fnd28_newq_value_18263q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Net Profit |
| 697 | `fnd28_rates_value_08106a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Current Ratio |
| 698 | `fnd28_rates_value_08111a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Cash & Equivalents % Total Current Assets Company Specific Accounting Practices |
| 699 | `fnd28_rates_value_08226a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Debt % Common Equity |
| 700 | `fnd28_rates_value_08231a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Common Equity |
| 701 | `fnd28_rates_value_08236a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Debt % Total Assets |
| 702 | `fnd28_rates_value_08241a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Equity % Total Assets |
| 703 | `fnd28_rates_value_08251a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Fixed Charge Coverage Ratio |
| 704 | `fnd28_rates_value_08261a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Cash/Fixed Charges |
| 705 | `fnd28_rates_value_08266a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Fixed Assets % Common Equity Company Specific Accounting Practices |
| 706 | `fnd28_rates_value_08287a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets / Common Equity Ratio |
| 707 | `fnd28_rates_value_08301a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Return on Equity Total (%) |
| 708 | `fnd28_rates_value_08306a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Gross Profit Margin |
| 709 | `fnd28_rates_value_08311a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Flow/Sales |
| 710 | `fnd28_rates_value_08316a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Profit Margin |
| 711 | `fnd28_rates_value_08321a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Pre-tax Margin |
| 712 | `fnd28_rates_value_08326a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Return on Assets |
| 713 | `fnd28_rates_value_08346a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Value of annual field: Tax Rate |
| 714 | `fnd28_rates_value_08366a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Margin |
| 715 | `fnd28_rates_value_08371a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Return on Equity - per Share |
| 716 | `fnd28_rates_value_08381a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Earnings Return on Equity |
| 717 | `fnd28_rates_value_08401a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Asset Turnover |
| 718 | `fnd28_rates_value_08416a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure % Total Assets |
| 719 | `fnd28_rates_value_08421a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure % Sales |
| 720 | `fnd28_rates_value_08579a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization Growth (year ago) Profitability |
| 721 | `fnd28_rates_value_08601a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share Growth |
| 722 | `fnd28_rates_value_08606a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Book Value per Share Growth (year ago) |
| 723 | `fnd28_rates_value_08611a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends per Share Growth |
| 724 | `fnd28_rates_value_08616a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity Growth (year ago) |
| 725 | `fnd28_rates_value_08621a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets Growth (year ago) |
| 726 | `fnd28_rates_value_08631a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales/Revenues Growth |
| 727 | `fnd28_rates_value_08636a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income Growth |
| 728 | `fnd28_rates_value_08651a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Reinvestment Rate - per Share |
| 729 | `fnd28_rates_value_08676a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Margin Growth |
| 730 | `fnd28_rates_value_08801a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of annual field: Total Investment Return Year Ago Growth Rates |
| 731 | `fnd28_ratesq_value_08106q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Ratio |
| 732 | `fnd28_ratesq_value_08111q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Cash & Equivalents % Total Current Assets Company Specific Accounting Practices |
| 733 | `fnd28_ratesq_value_08226q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Debt % Common Equity |
| 734 | `fnd28_ratesq_value_08231q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Debt % Common Equity |
| 735 | `fnd28_ratesq_value_08236q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Debt % Total Assets |
| 736 | `fnd28_ratesq_value_08241q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Equity % Total Assets |
| 737 | `fnd28_ratesq_value_08251q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Fixed Charge Coverage Ratio |
| 738 | `fnd28_ratesq_value_08261q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Cash/Fixed Charges |
| 739 | `fnd28_ratesq_value_08266q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Fixed Assets % Common Equity Company Specific Accounting Practices |
| 740 | `fnd28_ratesq_value_08287q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets / Common Equity Ratio |
| 741 | `fnd28_ratesq_value_08301q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Return on Equity Total (%) |
| 742 | `fnd28_ratesq_value_08306q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Gross Profit Margin |
| 743 | `fnd28_ratesq_value_08311q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Flow/Sales |
| 744 | `fnd28_ratesq_value_08316q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Profit Margin |
| 745 | `fnd28_ratesq_value_08321q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Margin |
| 746 | `fnd28_ratesq_value_08326q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Return on Assets |
| 747 | `fnd28_ratesq_value_08346q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Tax Rate |
| 748 | `fnd28_ratesq_value_08366q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Margin |
| 749 | `fnd28_ratesq_value_08371q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Return on Equity - per Share |
| 750 | `fnd28_ratesq_value_08381q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash Earnings Return on Equity |
| 751 | `fnd28_ratesq_value_08401q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Asset Turnover |
| 752 | `fnd28_ratesq_value_08416q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Expenditure % Total Assets |
| 753 | `fnd28_ratesq_value_08421q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Capital Expenditure % Sales |
| 754 | `fnd28_ratesq_value_08579q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Market Capitalization Growth (year ago) Profitability |
| 755 | `fnd28_ratesq_value_08601q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings per Share Growth |
| 756 | `fnd28_ratesq_value_08606q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Book Value per Share Growth (year ago) |
| 757 | `fnd28_ratesq_value_08611q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Dividends per Share Growth |
| 758 | `fnd28_ratesq_value_08616q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Equity Growth (year ago) |
| 759 | `fnd28_ratesq_value_08621q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets Growth (year ago) |
| 760 | `fnd28_ratesq_value_08631q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Sales/Revenues Growth |
| 761 | `fnd28_ratesq_value_08636q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income Growth |
| 762 | `fnd28_ratesq_value_08651q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Reinvestment Rate - per Share |
| 763 | `fnd28_ratesq_value_08676q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Margin Growth |
| 764 | `fnd28_ratesq_value_08801q` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Total Investment Return year ago Growth Rates |
| 765 | `fnd28_statisticsq_value_05301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Shares Outstanding |
| 766 | `fnd28_statisticsq_value_05303q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Treasury Shares |
| 767 | `fnd28_statisticsq_value_05309q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Par Value |
| 768 | `fnd28_statisticsq_value_05486q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Tangible Book Value per Share |
| 769 | `fnd28_statisticsq_value_05502q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Cash Flow per Share Fiscal Period |
| 770 | `fnd28_statisticsq_value_07230q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets (U.S.$) |
| 771 | `fnd28_statisticsq_value_18208q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Continuing Operations |
| 772 | `fnd28_value_01001` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Sales or Revenues |
| 773 | `fnd28_value_01051` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Cost Of Goods Sold (Excl Depreciation) |
| 774 | `fnd28_value_01100` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Gross Income |
| 775 | `fnd28_value_01101` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Selling, General & Administrative Expenses |
| 776 | `fnd28_value_01148` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Depreciation |
| 777 | `fnd28_value_01149` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Amortization of Intangibles |
| 778 | `fnd28_value_01151` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Depreciation, Depletion & Amortization |
| 779 | `fnd28_value_01155a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Other Intangibles |
| 780 | `fnd28_value_01156a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Goodwill |
| 781 | `fnd28_value_01157a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Amortization of Computer Software |
| 782 | `fnd28_value_01201` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of field: Research and Development Expense |
| 783 | `fnd28_value_01204a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Taxes Other Than Income Taxes |
| 784 | `fnd28_value_01230` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Other Operating Expenses |
| 785 | `fnd28_value_01249` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Operating Expenses - Total |
| 786 | `fnd28_value_01250` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Operating Income |
| 787 | `fnd28_value_01251` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Interest Expense on Debt |
| 788 | `fnd28_value_01255` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Interest Capitalized |
| 789 | `fnd28_value_01262` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of field: Other Income/Expense Net |
| 790 | `fnd28_value_01266` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Non-Operating Interest Income |
| 791 | `fnd28_value_01268a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Income - Non-Operating |
| 792 | `fnd28_value_01269a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Discontinued Operations - Pre-tax |
| 793 | `fnd28_value_01302a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Provisions |
| 794 | `fnd28_value_01306a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Gain/Loss On Disposal of Assets |
| 795 | `fnd28_value_01306q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Gain/Loss On Disposal of Assets |
| 796 | `fnd28_value_01352a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Exchange Transactions |
| 797 | `fnd28_value_01401` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Pre-tax Income |
| 798 | `fnd28_value_01451` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Income Taxes |
| 799 | `fnd28_value_01501` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Minority Interest |
| 800 | `fnd28_value_01504` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: After Tax Other Income/Expense |
| 801 | `fnd28_value_01505` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Discontinued Operations |
| 802 | `fnd28_value_01551` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Income before Extraordinary Items/Preferred Dividends |
| 803 | `fnd28_value_01651` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Income - Bottom Line |
| 804 | `fnd28_value_01651a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income - Bottom Line |
| 805 | `fnd28_value_01701` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Preferred Dividend Requirements |
| 806 | `fnd28_value_01705a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income Used to Calculate Fully Diluted Earnings per Share |
| 807 | `fnd28_value_01706` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Income after Preferred Dividends (Basic EPS) |
| 808 | `fnd28_value_01751` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Income Used to Calculate Earnings per Share |
| 809 | `fnd28_value_01751a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income Used to Calculate Earnings per Share |
| 810 | `fnd28_value_01801a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Auditor Fees Key Items in US Dollars |
| 811 | `fnd28_value_02003` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Cash |
| 812 | `fnd28_value_02005a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Cash & Equivalents Generic |
| 813 | `fnd28_value_02008` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Short Term Investments |
| 814 | `fnd28_value_02051` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Receivables (Net) |
| 815 | `fnd28_value_02101` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Inventories Total |
| 816 | `fnd28_value_02149` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Other Current Assets |
| 817 | `fnd28_value_02201` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Current Assets Total |
| 818 | `fnd28_value_02256` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Investments In Associated Companies |
| 819 | `fnd28_value_02300a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets - As Reported |
| 820 | `fnd28_value_02301` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Property, Plant and Equipment - Gross |
| 821 | `fnd28_value_02401` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Accumulated Depreciation |
| 822 | `fnd28_value_02507a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Brands, Patents - Net |
| 823 | `fnd28_value_02508a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Brands, Patents - Accumulated Amortization |
| 824 | `fnd28_value_02509a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Brands, Patents - Gross |
| 825 | `fnd28_value_02510a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Licenses - Net |
| 826 | `fnd28_value_02511a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Licenses - Gross |
| 827 | `fnd28_value_02512a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Licenses - Accumulated Amortization |
| 828 | `fnd28_value_02513a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Intangibles - Net |
| 829 | `fnd28_value_02514a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Intangible Assets - Gross |
| 830 | `fnd28_value_02515a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Intangible Assets - Accumulated Amortization |
| 831 | `fnd28_value_02516a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Computer Software - Gross |
| 832 | `fnd28_value_02517a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Computer Software - Accumulated Amortization |
| 833 | `fnd28_value_02648` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Tangible Other Assets |
| 834 | `fnd28_value_02649` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Intangible Other Assets - Net |
| 835 | `fnd28_value_02654a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Intangible Other Assets - Gross |
| 836 | `fnd28_value_02655a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Total Intangible Other Assets Accumulated Amortization |
| 837 | `fnd28_value_03051` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Short Term Debt & Current Portion of Long Term Debt |
| 838 | `fnd28_value_03069a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Other Accrued Expenses |
| 839 | `fnd28_value_03251` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Long Term Debt |
| 840 | `fnd28_value_03255` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Debt |
| 841 | `fnd28_value_03261a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Pension/Post Retirement Benefits |
| 842 | `fnd28_value_03263` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Deferred Taxes |
| 843 | `fnd28_value_03273` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Other Liabilities |
| 844 | `fnd28_value_03351` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Liabilities |
| 845 | `fnd28_value_03401` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Non-Equity Reserves |
| 846 | `fnd28_value_03426` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Minority Interest |
| 847 | `fnd28_value_03451` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Preferred Stock |
| 848 | `fnd28_value_03491a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Goodwill Written Off |
| 849 | `fnd28_value_03495` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Retained Earnings |
| 850 | `fnd28_value_03499` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Treasury Stock |
| 851 | `fnd28_value_03501` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Common Equity |
| 852 | `fnd28_value_03999` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Liabilities & Shareholders' Equity |
| 853 | `fnd28_value_04052a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends |
| 854 | `fnd28_value_04053a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Asset Disposal |
| 855 | `fnd28_value_04055a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Minority Interest |
| 856 | `fnd28_value_04056a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity In Earnings |
| 857 | `fnd28_value_04057a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Other Cash Flow (Supplementary to Other Cash Flow Total -04051) |
| 858 | `fnd28_value_04148a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Interest Paid (Cash Flow) |
| 859 | `fnd28_value_04149a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Interest Income (Cash Flow) |
| 860 | `fnd28_value_04150a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Taxation (Cash Flow) |
| 861 | `fnd28_value_04251` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Net Proceeds from Sale/Issuance of Common & Preferred |
| 862 | `fnd28_value_04500a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: External Financing |
| 863 | `fnd28_value_04551` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Dividends Paid - Total |
| 864 | `fnd28_value_04601` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Capital Expenditures (Additions to Fixed Assets) |
| 865 | `fnd28_value_04751` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Common/Preferred Redeemed, Retired, Converted, Etc. |
| 866 | `fnd28_value_04860` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Cash Flow - Operating Activities |
| 867 | `fnd28_value_04890` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Cash Flow - Financing |
| 868 | `fnd28_value_04900a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Increase/Decrease in Working Capital |
| 869 | `fnd28_value_05001a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Market Price - Year End |
| 870 | `fnd28_value_05002` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - High |
| 871 | `fnd28_value_05003` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - Low |
| 872 | `fnd28_value_05004a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Market Price - 5 Yr Avg-High |
| 873 | `fnd28_value_05005a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Market Price - 5 Yr Avg-High |
| 874 | `fnd28_value_05006` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - Current |
| 875 | `fnd28_value_05007` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - Year to Date - High |
| 876 | `fnd28_value_05008` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Market Price - Year to Date - Low |
| 877 | `fnd28_value_05015a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: January End Market Price |
| 878 | `fnd28_value_05016a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: January High Price |
| 879 | `fnd28_value_05017a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: January Low Price |
| 880 | `fnd28_value_05020a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: February End Market Price |
| 881 | `fnd28_value_05021a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: February High Price |
| 882 | `fnd28_value_05022a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: February Low Price |
| 883 | `fnd28_value_05025a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: March End Market Price |
| 884 | `fnd28_value_05026a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: March High Price |
| 885 | `fnd28_value_05027a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: March Low Price |
| 886 | `fnd28_value_05030a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: April End Market Price |
| 887 | `fnd28_value_05031a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: April High Price |
| 888 | `fnd28_value_05032a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: April Low Price |
| 889 | `fnd28_value_05035a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: May End Market Price |
| 890 | `fnd28_value_05036a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: May High Price |
| 891 | `fnd28_value_05037a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: May Low Price |
| 892 | `fnd28_value_05040a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: June End Market Price |
| 893 | `fnd28_value_05041a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: June High Price |
| 894 | `fnd28_value_05042a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: June Low Price |
| 895 | `fnd28_value_05045a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: July End Market Price |
| 896 | `fnd28_value_05046a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: July High Price |
| 897 | `fnd28_value_05047a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: July Low Price |
| 898 | `fnd28_value_05050a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: August End Market Price |
| 899 | `fnd28_value_05051a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: August High Price |
| 900 | `fnd28_value_05052a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: August Low Price |
| 901 | `fnd28_value_05055a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: September End Market Price |
| 902 | `fnd28_value_05056a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: September High Price |
| 903 | `fnd28_value_05057a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: September Low Price |
| 904 | `fnd28_value_05060a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: October End Market Price |
| 905 | `fnd28_value_05061a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: October High Price |
| 906 | `fnd28_value_05062a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: October Low Price |
| 907 | `fnd28_value_05065a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: November End Market Price |
| 908 | `fnd28_value_05066a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: November High Price |
| 909 | `fnd28_value_05067a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: November Low Price |
| 910 | `fnd28_value_05070a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: December End Market Price |
| 911 | `fnd28_value_05071a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: December High Price |
| 912 | `fnd28_value_05072a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: December Low Price |
| 913 | `fnd28_value_05085a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Period Close Price |
| 914 | `fnd28_value_05085q` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of quarterly field: Period Close Price |
| 915 | `fnd28_value_05091` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of field: Market Price 52 Week High |
| 916 | `fnd28_value_05092` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of field: Market Price 52 Week Low |
| 917 | `fnd28_value_05101` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividends per Share |
| 918 | `fnd28_value_05101a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends per Share |
| 919 | `fnd28_value_05102a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends per Share - Gross |
| 920 | `fnd28_value_05116q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Dividends per Share (Interim) |
| 921 | `fnd28_value_05122a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends per Share Qtr2 |
| 922 | `fnd28_value_05124a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends per Share Qtr4 |
| 923 | `fnd28_value_05126a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: DPS Gross Qtr2 |
| 924 | `fnd28_value_05128a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: DPS Gross Qtr4 |
| 925 | `fnd28_value_05131a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: DPS - 12 Months Qtr1 |
| 926 | `fnd28_value_05132a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: DPS - 12 Months Qtr2 |
| 927 | `fnd28_value_05133a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: DPS - 12 Months Qtr3 |
| 928 | `fnd28_value_05134a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: DPS - 12 Months Qtr4 |
| 929 | `fnd28_value_05140a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends Per Share - 5 Yr Avg |
| 930 | `fnd28_value_05142a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: DPS - 5 yr avg Qtr2 |
| 931 | `fnd28_value_05144a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: DPS - 5 yr avg Qtr4 |
| 932 | `fnd28_value_05145` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividends per Share - Last 12 Months |
| 933 | `fnd28_value_05190` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Indicated Dividend Rate |
| 934 | `fnd28_value_05191` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Common Shares Used to Calculate EPS |
| 935 | `fnd28_value_05191a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Common Shares Used to Calculate EPS |
| 936 | `fnd28_value_05191q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Shares Used to Calculate EPS |
| 937 | `fnd28_value_05192` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Common Shares Used to Calculate Basic EPS |
| 938 | `fnd28_value_05192a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Common Shares Used to Calculate Basic EPS |
| 939 | `fnd28_value_05192q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Shares Used to Calculate Basic EPS |
| 940 | `fnd28_value_05194` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Common Shares Used to Calculate Fully Diluted EPS Balance Sheet Assets |
| 941 | `fnd28_value_05194a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Shares Used to Calculate Fully Diluted EPS Balance Sheet Assets |
| 942 | `fnd28_value_05194q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Shares Used to Calculate Fully Diluted EPS Balance Sheet Assets |
| 943 | `fnd28_value_05201a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share (Supported for Non U.S. only) |
| 944 | `fnd28_value_05210a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Earnings per Share Basic Year |
| 945 | `fnd28_value_05211a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share-Basic Qtr1 |
| 946 | `fnd28_value_05212a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share-Basic Qtr2 |
| 947 | `fnd28_value_05213a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share-Basic Qtr3 |
| 948 | `fnd28_value_05214a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share-Basic Qtr4 |
| 949 | `fnd28_value_05223a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Earnings per Share Q3 |
| 950 | `fnd28_value_05225a` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of annual field: Includes Extraordinary Credit/Charge per |
| 951 | `fnd28_value_05226a` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of annual field: Extraordinary Credit/Charge per Share |
| 952 | `fnd28_value_05227a` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of annual field: Includes Pre-tax Extraordinary Credit/Charge per Share |
| 953 | `fnd28_value_05228a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Discontinued Operations per Share |
| 954 | `fnd28_value_05230a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share after Extraordinary Items |
| 955 | `fnd28_value_05251a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: EPS - 12 Months Qtr1 |
| 956 | `fnd28_value_05252a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: EPS - 12 Months Qtr2 |
| 957 | `fnd28_value_05253a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: EPS - 12 Months Qtr3 |
| 958 | `fnd28_value_05254a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: EPS - 12 Months Qtr4 |
| 959 | `fnd28_value_05255` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings per Share - Last 12 Months |
| 960 | `fnd28_value_05260a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Per Share - 5 Yr Avg |
| 961 | `fnd28_value_05261a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: EPS - 5 yr avg Qtr1 |
| 962 | `fnd28_value_05262a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: EPS - 5 yr avg Qtr2 |
| 963 | `fnd28_value_05263a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: EPS - 5 yr avg Qtr 3 |
| 964 | `fnd28_value_05264a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: EPS - 5 yr avg Qtr4 |
| 965 | `fnd28_value_05290` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Fully Diluted Earnings per Share |
| 966 | `fnd28_value_05290a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Fully Diluted Earnings per Share |
| 967 | `fnd28_value_05291a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Fully Diluted EPS Qtr1 |
| 968 | `fnd28_value_05292a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Fully Diluted EPS Q2 |
| 969 | `fnd28_value_05293a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Fully Diluted EPS Qtr3 |
| 970 | `fnd28_value_05294a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Fully Diluted EPS Qtr4 |
| 971 | `fnd28_value_05301` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Common Shares Outstanding |
| 972 | `fnd28_value_05301a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Common Shares Outstanding |
| 973 | `fnd28_value_05302` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Common Shares Outstanding - Current |
| 974 | `fnd28_value_05303a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Treasury Shares |
| 975 | `fnd28_value_05309a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Par Value |
| 976 | `fnd28_value_05326` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Number of Shares Authorized |
| 977 | `fnd28_value_05326a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Number of Shares Authorized |
| 978 | `fnd28_value_05351a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Length of Fiscal Period |
| 979 | `fnd28_value_05351q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Length of Fiscal Period |
| 980 | `fnd28_value_05376a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Common Dividends (Cash) |
| 981 | `fnd28_value_05450` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Common/Ordinary Shareholders |
| 982 | `fnd28_value_05475` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Closely Held Shares |
| 983 | `fnd28_value_05475a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Closely Held Shares |
| 984 | `fnd28_value_05480` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Book Value per Share - Current |
| 985 | `fnd28_value_05486` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Tangible Book Value per Share |
| 986 | `fnd28_value_05486a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Tangible Book Value per Share |
| 987 | `fnd28_value_05491` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of field: Book Value Outstanding Shares - Fiscal |
| 988 | `fnd28_value_05491a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Book Value Outstanding Shares - Fiscal |
| 989 | `fnd28_value_05491q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Book Value Outstanding Shares - Fiscal |
| 990 | `fnd28_value_05501a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Flow per Share |
| 991 | `fnd28_value_05503a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Long Term Liabilities per Share |
| 992 | `fnd28_value_05505` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Capital Expenditure per Share |
| 993 | `fnd28_value_05505a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure per Share |
| 994 | `fnd28_value_05506` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Working Capital per Share |
| 995 | `fnd28_value_05506a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Working Capital per Share |
| 996 | `fnd28_value_05507` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Free Cash Flow per Share |
| 997 | `fnd28_value_05507a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Free Cash Flow per Share |
| 998 | `fnd28_value_05508a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Sales per Share |
| 999 | `fnd28_value_05509` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Operating Profit per Share |
| 1000 | `fnd28_value_05509a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Profit per Share |
| 1001 | `fnd28_value_05510` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Cash Flow per Share - Current Annual Statistics |
| 1002 | `fnd28_value_05575a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Stock Split/Dividend Ratio - Fiscal Weekly Time Series |
| 1003 | `fnd28_value_05575q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Stock Split/Dividend Ratio - Fiscal Weekly Time Series |
| 1004 | `fnd28_value_05576` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Stock Split/Dividend Ratio |
| 1005 | `fnd28_value_07011a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Employees |
| 1006 | `fnd28_value_07101a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: International Sales |
| 1007 | `fnd28_value_07126a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: International Operating Income |
| 1008 | `fnd28_value_07151a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: International Assets |
| 1009 | `fnd28_value_07210q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Market Capitalization (U.S.$) |
| 1010 | `fnd28_value_07220q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Common Equity (U.S.$) |
| 1011 | `fnd28_value_07260q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Net Profit (U.S. $) |
| 1012 | `fnd28_value_07270q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Trailing 12 Months Net Sales/Revenue (U.S. $) |
| 1013 | `fnd28_value_08001` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization |
| 1014 | `fnd28_value_08001a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization |
| 1015 | `fnd28_value_08001q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Market Capitalization |
| 1016 | `fnd28_value_08002a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Market Capitalization Fiscal Period End |
| 1017 | `fnd28_value_08003` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization (Public) - Current |
| 1018 | `fnd28_value_08004` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization - Public |
| 1019 | `fnd28_value_08004a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization - Public |
| 1020 | `fnd28_value_08005` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization - Current |
| 1021 | `fnd28_value_08021` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Closely Held Shares % |
| 1022 | `fnd28_value_08021a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Closely Held Shares % |
| 1023 | `fnd28_value_08101a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Quick Ratio |
| 1024 | `fnd28_value_08105` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Quick Ratio - 5 Yr Avg |
| 1025 | `fnd28_value_08105a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Quick Ratio - 5 Yr Avg |
| 1026 | `fnd28_value_08110` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Current Ratio - 5 Yr Avg |
| 1027 | `fnd28_value_08110a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Current Ratio - 5 Yr Avg |
| 1028 | `fnd28_value_08115` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash & Equivalents % Total Current Assets - 5 Yr Avg |
| 1029 | `fnd28_value_08115a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash & Equivalents % Total Current Assets - 5 Yr Avg |
| 1030 | `fnd28_value_08116a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Inventories % Total Current Assets |
| 1031 | `fnd28_value_08120` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Inventories % Total Current Assets - 5 Yr Avg |
| 1032 | `fnd28_value_08120a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Inventories % Total Current Assets - 5 Yr Avg |
| 1033 | `fnd28_value_08121a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Receivables % Total Current Assets |
| 1034 | `fnd28_value_08125` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Receivables % Total Current Assets - 5 Yr Avg |
| 1035 | `fnd28_value_08125a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Receivables % Total Current Assets - 5 Yr Avg |
| 1036 | `fnd28_value_08126a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Inventories - Days Held 5 Year Averages |
| 1037 | `fnd28_value_08130` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Inventories - Days Held - 5 Yr Avg |
| 1038 | `fnd28_value_08130a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Inventories - Days Held - 5 Yr Avg |
| 1039 | `fnd28_value_08131a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accounts Receivables Days |
| 1040 | `fnd28_value_08135` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of field: Accounts Receivables Days - 5 Yr Avg Company Specific Accounting Practices |
| 1041 | `fnd28_value_08135a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Accounts Receivables Days - 5 Yr Avg Company Specific Accounting Practices |
| 1042 | `fnd28_value_08136` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Inventory Turnover |
| 1043 | `fnd28_value_08136a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Inventory Turnover |
| 1044 | `fnd28_value_08140` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Inventory Turnover - 5 Yr Avg |
| 1045 | `fnd28_value_08140a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Inventory Turnover - 5 Yr Avg |
| 1046 | `fnd28_value_08141` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Net Sales % Working Capital |
| 1047 | `fnd28_value_08141a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales % Working Capital |
| 1048 | `fnd28_value_08145` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of field: Net Sales % Working Capital - 5 Yr Avg |
| 1049 | `fnd28_value_08145a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Net Sales % Working Capital - 5 Yr Avg |
| 1050 | `fnd28_value_08226` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Long Term Debt % Common Equity |
| 1051 | `fnd28_value_08231` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Debt % Common Equity |
| 1052 | `fnd28_value_08236` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Debt % Total Assets |
| 1053 | `fnd28_value_08241` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Common Equity % Total Assets |
| 1054 | `fnd28_value_08251` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Fixed Charge Coverage Ratio |
| 1055 | `fnd28_value_08261` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Operating Cash/Fixed Charges |
| 1056 | `fnd28_value_08266` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Fixed Assets % Common Equity Company Specific Accounting Practices |
| 1057 | `fnd28_value_08287` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Assets / Common Equity Ratio |
| 1058 | `fnd28_value_08302` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Return On Equity Per Share (Fiscal) |
| 1059 | `fnd28_value_08302a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Return On Equity Per Share (Fiscal) |
| 1060 | `fnd28_value_08305` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Return On Equity - Total (%) - 5 Yr Avg |
| 1061 | `fnd28_value_08305a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Return On Equity - Total (%)- 5 Yr Avg |
| 1062 | `fnd28_value_08310` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Gross Profit Margin - 5 Yr Avg |
| 1063 | `fnd28_value_08310a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Gross Profit Margin - 5 Yr Avg |
| 1064 | `fnd28_value_08315` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Flow/Sales - 5 Yr Avg |
| 1065 | `fnd28_value_08315a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Flow/Sales - 5 Yr Avg |
| 1066 | `fnd28_value_08320` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Operating Profit Margin - 5 Yr Avg |
| 1067 | `fnd28_value_08320a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Profit Margin - 5 Yr Avg |
| 1068 | `fnd28_value_08325` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Pretax Margin - 5 Yr Avg |
| 1069 | `fnd28_value_08325a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Pretax Margin - 5 Yr Avg |
| 1070 | `fnd28_value_08330` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Return On Assets - 5 Yr Avg |
| 1071 | `fnd28_value_08330a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Return On Assets - 5 Yr Avg |
| 1072 | `fnd28_value_08331a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Cost of Goods Sold / Sales |
| 1073 | `fnd28_value_08335` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Cost Of Goods Sold/Sales - 5 Yr Avg |
| 1074 | `fnd28_value_08335a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Cost Of Goods Sold/Sales - 5 Yr Avg |
| 1075 | `fnd28_value_08336a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Selling, General & Administrative Expenses / Sales |
| 1076 | `fnd28_value_08340` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Selling, General & Administrative Exp/Sales - 5 Yr Avg |
| 1077 | `fnd28_value_08340a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Selling, General & Administrative Exp/Sales - 5 Yr Avg |
| 1078 | `fnd28_value_08341a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Research & Development Expense / Sales |
| 1079 | `fnd28_value_08345` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of field: Research & Development/Sales |
| 1080 | `fnd28_value_08345a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Research & Development/Sales |
| 1081 | `fnd28_value_08346` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Value of field: Tax Rate |
| 1082 | `fnd28_value_08350` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of field: Tax Rate |
| 1083 | `fnd28_value_08350a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Tax Rate |
| 1084 | `fnd28_value_08351a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Sales per Employee 5 Year Averages |
| 1085 | `fnd28_value_08355` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Sales per Employee Loan Loss Ratios Annual Statistics |
| 1086 | `fnd28_value_08355a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Sales per Employee Loan Loss Ratios Annual Statistics |
| 1087 | `fnd28_value_08356` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | value of field: Interest Rate - Estimated Average |
| 1088 | `fnd28_value_08356a` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | value of annual field: Interest Rate - Estimated Average |
| 1089 | `fnd28_value_08360` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | value of field: Interest Rate - Estimated Average - 5 Yr Avg |
| 1090 | `fnd28_value_08360a` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | value of annual field: Interest Rate - Estimated Average - 5 Yr Avg |
| 1091 | `fnd28_value_08361a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Income Return on Total Capital |
| 1092 | `fnd28_value_08365` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Operating Income/Total Capital - 5 Yr Avg |
| 1093 | `fnd28_value_08365a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Income/Total Capital - 5 Yr Avg |
| 1094 | `fnd28_value_08366` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Margin |
| 1095 | `fnd28_value_08370` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Net Margin - 5 Yr Avg Asset Utilization Annual Statistics |
| 1096 | `fnd28_value_08370a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Net Margin - 5 Yr Avg Asset Utilization Annual Statistics |
| 1097 | `fnd28_value_08371` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Return on Equity - per Share |
| 1098 | `fnd28_value_08372` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Return on Equity - per Share - Current |
| 1099 | `fnd28_value_08375` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Return On Equity - Per Share - 5 Yr Avg |
| 1100 | `fnd28_value_08375a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Return On Equity - Per Share - 5 Yr Avg |
| 1101 | `fnd28_value_08376a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Return on Invested Capital |
| 1102 | `fnd28_value_08380` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Return On Invested Capital - 5 Yr Avg |
| 1103 | `fnd28_value_08380a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of annual field: Return On Invested Capital - 5 Yr Avg |
| 1104 | `fnd28_value_08385` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Cash Earnings Return On Equity - 5 Yr Avg |
| 1105 | `fnd28_value_08385a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Cash Earnings Return On Equity - 5 Yr Avg |
| 1106 | `fnd28_value_08401` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Asset Turnover |
| 1107 | `fnd28_value_08405` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Total Asset Turnover - 5 Yr Avg Leverage Annual Statistics |
| 1108 | `fnd28_value_08405a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Total Asset Turnover - 5 Yr Avg Leverage Annual Statistics |
| 1109 | `fnd28_value_08406` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Assets per Employee |
| 1110 | `fnd28_value_08406a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Assets per Employee |
| 1111 | `fnd28_value_08410` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Assets per Employee |
| 1112 | `fnd28_value_08410a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Assets per Employee |
| 1113 | `fnd28_value_08411` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Capital Expenditure % Gross Fixed Assets |
| 1114 | `fnd28_value_08411a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure % Gross Fixed Assets |
| 1115 | `fnd28_value_08415` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Capital Expenditure % Gross Fixed Assets |
| 1116 | `fnd28_value_08415a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure % Gross Fixed Assets |
| 1117 | `fnd28_value_08416` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Capital Expenditure % Total Assets |
| 1118 | `fnd28_value_08420` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Capital Expenditure % Total Assets - 5 Year Average |
| 1119 | `fnd28_value_08420a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure % Total Assets - 5 Year Average |
| 1120 | `fnd28_value_08421` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Capital Expenditure % Sales |
| 1121 | `fnd28_value_08425` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Capital Expenditure % Total Sales - 5 Year Average |
| 1122 | `fnd28_value_08425a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Capital Expenditure % Total Sales - 5 Year Average |
| 1123 | `fnd28_value_08426` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Accumulated Depreciation % Gross Fixed Assets |
| 1124 | `fnd28_value_08426a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Accumulated Depreciation % Gross Fixed Assets |
| 1125 | `fnd28_value_08430` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Accumulated Depreciation % Gross Fixed Assets-5 Yr Avg Leverage Annual Statistics |
| 1126 | `fnd28_value_08430a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Accumulated Depreciation % Gross Fixed Assets - 5 Yr Avg Leverage Annual Statistics |
| 1127 | `fnd28_value_08431` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Sales to Gross Fixed Asset |
| 1128 | `fnd28_value_08431a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales to Gross Fixed Asset |
| 1129 | `fnd28_value_08435` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Sales To Gross Fixed Assets - 5 Yr Avg |
| 1130 | `fnd28_value_08435a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales To Gross Fixed Assets - 5 Yr Avg |
| 1131 | `fnd28_value_08581` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization - 3 Year Growth |
| 1132 | `fnd28_value_08581a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Market Capitalization - 3 Year Growth |
| 1133 | `fnd28_value_08604` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Earnings Per Share - 3 Yr Annual Growth Five Year Averages |
| 1134 | `fnd28_value_08604a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Earnings Per Share - 3 Yr Annual Growth Five Year Averages |
| 1135 | `fnd28_value_08605` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings per Share Growth |
| 1136 | `fnd28_value_08605a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings per Share Growth |
| 1137 | `fnd28_value_08610` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Book Value Per Share - 5 Yr Annual Growth Profitability Annual Statistics |
| 1138 | `fnd28_value_08610a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Book Value Per Share - 5 Yr Annual Growth Profitability Annual Statistics |
| 1139 | `fnd28_value_08614a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends per Share Growth |
| 1140 | `fnd28_value_08615` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividends Per Share - 5 Yr Annual Growth |
| 1141 | `fnd28_value_08615a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividends Per Share - 5 Yr Annual Growth |
| 1142 | `fnd28_value_08620` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Equity - 5 Yr Annual Growth |
| 1143 | `fnd28_value_08620a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Equity - 5 Yr Annual Growth |
| 1144 | `fnd28_value_08625` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Total Assets - 5 Yr Annual Growth |
| 1145 | `fnd28_value_08625a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Total Assets - 5 Yr Annual Growth |
| 1146 | `fnd28_value_08626a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Employees Growth |
| 1147 | `fnd28_value_08630` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Employees - 5 Yr Annual Growth |
| 1148 | `fnd28_value_08630a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Employees - 5 Yr Annual Growth |
| 1149 | `fnd28_value_08633a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales/Revenues Growth |
| 1150 | `fnd28_value_08635` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Sales / Revenues - 5 Yr Annual Growth |
| 1151 | `fnd28_value_08635a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Sales / Revenues - 5 Yr Annual Growth |
| 1152 | `fnd28_value_08638a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income Growth |
| 1153 | `fnd28_value_08640` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Net Income Growth |
| 1154 | `fnd28_value_08640a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Income Growth |
| 1155 | `fnd28_value_08646a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Income Growth |
| 1156 | `fnd28_value_08650` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Operating Income - 5 Yr Annual Growth |
| 1157 | `fnd28_value_08650a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Operating Income - 5 Yr Annual Growth |
| 1158 | `fnd28_value_08651` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of field: Reinvestment Rate - per Share |
| 1159 | `fnd28_value_08652` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of field: Reinvestment Rate - per Share - Current |
| 1160 | `fnd28_value_08653a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Reinvestment Rate Per Share (Fiscal) |
| 1161 | `fnd28_value_08655` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of field: Reinvestment Rate - Per Share - 5 Yr Avg |
| 1162 | `fnd28_value_08655a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Reinvestment Rate - Per Share - 5 Yr Avg |
| 1163 | `fnd28_value_08656` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of field: Reinvestment Rate - Total |
| 1164 | `fnd28_value_08656a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Reinvestment Rate - Total |
| 1165 | `fnd28_value_08660` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of field: Reinvestment Rate - Total $ - 5 Yr Avg |
| 1166 | `fnd28_value_08660a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of annual field: Reinvestment Rate - Total $ - 5 Yr Avg |
| 1167 | `fnd28_value_08680` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of field: Net Margin Growth Profitability Annual Statistics |
| 1168 | `fnd28_value_08680a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Net Margin Growth Profitability Annual Statistics |
| 1169 | `fnd28_value_08698q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Sales/Revenue Growth (period vs. year ago) |
| 1170 | `fnd28_value_08699q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings per Share Growth (Period vs. Year Ago) |
| 1171 | `fnd28_value_08701a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Income Margin |
| 1172 | `fnd28_value_08705a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Income Margin |
| 1173 | `fnd28_value_08706a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Asset Turnover |
| 1174 | `fnd28_value_08710a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Asset Turnover |
| 1175 | `fnd28_value_08711a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Return on Assets |
| 1176 | `fnd28_value_08716a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Assets Growth |
| 1177 | `fnd28_value_08720a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Assets Growth |
| 1178 | `fnd28_value_08721a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Sales Growth |
| 1179 | `fnd28_value_08725a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Sales Growth |
| 1180 | `fnd28_value_08726a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Income Growth |
| 1181 | `fnd28_value_08730a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Income Growth |
| 1182 | `fnd28_value_08731a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Sales % Tot Sales |
| 1183 | `fnd28_value_08735a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Sales % Total Sales |
| 1184 | `fnd28_value_08736a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Assets % Tot Assets |
| 1185 | `fnd28_value_08740a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Assets % Total Assets |
| 1186 | `fnd28_value_08741a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Foreign Income % Total Income 5 Year Averages |
| 1187 | `fnd28_value_08745a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Foreign Income % Total Income Other Fields |
| 1188 | `fnd28_value_08801` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of field: Total Investment Return Year-Ago Growth Rates |
| 1189 | `fnd28_value_08803a` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of annual field: Total Investment Return - 3 Yr Annual Return Five Year Averages |
| 1190 | `fnd28_value_08816a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Earnings Per Share - Fiscal - 1 Yr Annual Growth |
| 1191 | `fnd28_value_08821a` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Value of annual field: Book Value Per Share - Fiscal - 1 Yr Growth Rate Three Year Averages |
| 1192 | `fnd28_value_08901a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accounts Payable % Sales |
| 1193 | `fnd28_value_08905` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Accounts Payable/Sales - 5 Yr Avg |
| 1194 | `fnd28_value_08905a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accounts Payable/Sales - 5 Yr Avg |
| 1195 | `fnd28_value_08911a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Retained Earnings % Equity |
| 1196 | `fnd28_value_08915` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Retained Earnings % Equity |
| 1197 | `fnd28_value_08915a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Retained Earnings % Equity |
| 1198 | `fnd28_value_09001` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price Trend - Last Week |
| 1199 | `fnd28_value_09005` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of field: Price Trend - 4 Week |
| 1200 | `fnd28_value_09006` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price Trend - 13 Weeks |
| 1201 | `fnd28_value_09007` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | Value of field: Price Trend 26 Weeks |
| 1202 | `fnd28_value_09011` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price Trend - Quarter to Date |
| 1203 | `fnd28_value_09016` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price Trend - Previous Quarter |
| 1204 | `fnd28_value_09021` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price Trend - Year to Date |
| 1205 | `fnd28_value_09026` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price Trend - 52 Weeks |
| 1206 | `fnd28_value_09102` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Price/Earnings Ratio - Current |
| 1207 | `fnd28_value_09103` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Price/Earnings Ratio - Current High |
| 1208 | `fnd28_value_09104q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Price/Earnings Ratio Close |
| 1209 | `fnd28_value_09105` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Price/Earnings Ratio - Current Low |
| 1210 | `fnd28_value_09202` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings Yield - Current |
| 1211 | `fnd28_value_09203` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings Yield - Current High |
| 1212 | `fnd28_value_09205` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Earnings Yield - Current Low |
| 1213 | `fnd28_value_09302` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of field: Price/Book Value Ratio - Current |
| 1214 | `fnd28_value_09304q` | MATRIX | 0.500 | 价量与波动 | 0 | — | — | — | UNUSABLE | value of quarterly field: Price/Book Value Ratio - Close |
| 1215 | `fnd28_value_09402` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividend Yield - Current |
| 1216 | `fnd28_value_09404` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividend Yield - Close |
| 1217 | `fnd28_value_09404q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Dividend Yield - Close |
| 1218 | `fnd28_value_09411a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - 5 Yr Avg High |
| 1219 | `fnd28_value_09416a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - 5 Yr Avg Low |
| 1220 | `fnd28_value_09421` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividend Yield - 5 Yr Avg - Close |
| 1221 | `fnd28_value_09421a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - 5 Yr Avg - Close |
| 1222 | `fnd28_value_09426a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Yield - 5 Yr Avg High-Low |
| 1223 | `fnd28_value_09502` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Dividend Payout per Share - Current |
| 1224 | `fnd28_value_09521a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Dividend Payout Per Share - 5 Yr Avg |
| 1225 | `fnd28_value_09602` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Price/Cash Flow - Current |
| 1226 | `fnd28_value_09604` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Price/Cash Flow Ratio |
| 1227 | `fnd28_value_09604q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Price/Cash Flow Ratio |
| 1228 | `fnd28_value_09704` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Market Capitalization to Common Equity |
| 1229 | `fnd28_value_09704q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Market Capitalization to Common Equity |
| 1230 | `fnd28_value_09802` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of field: Beta |
| 1231 | `fnd28_value_09803` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of field: Alpha Annual Statistics |
| 1232 | `fnd28_value_09905q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Market Capitalization to Trailing Twelve Months Revenue Ratio |
| 1233 | `fnd28_value_18100` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Enterprise Value |
| 1234 | `fnd28_value_18100a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Enterprise Value |
| 1235 | `fnd28_value_18100q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Enterprise Value |
| 1236 | `fnd28_value_18150a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Income From Continuing Operations |
| 1237 | `fnd28_value_18183a` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Taxes-Credit |
| 1238 | `fnd28_value_18184a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Taxes-Debit |
| 1239 | `fnd28_value_18185a` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of annual field: Income Tax Credits |
| 1240 | `fnd28_value_18186a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Current Domestic Income Tax |
| 1241 | `fnd28_value_18187a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Current Foreign Income Tax |
| 1242 | `fnd28_value_18188a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Domestic Income Tax |
| 1243 | `fnd28_value_18189a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Deferred Foreign Income Tax |
| 1244 | `fnd28_value_18192a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Dividends Provided for or Paid Common |
| 1245 | `fnd28_value_18193q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings per Share - As Reported |
| 1246 | `fnd28_value_18205q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Discontinued Operations Total per Share |
| 1247 | `fnd28_value_18209q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: EPS Fiscal Period Generic after Extra Items |
| 1248 | `fnd28_value_18211` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Restructuring Expense per Share - Pre-tax |
| 1249 | `fnd28_value_18211a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Restructuring Expense per Share - Pre-tax |
| 1250 | `fnd28_value_18227a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Restructuring Expense |
| 1251 | `fnd28_value_18259q` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of quarterly field: Includes Extraordinary Credit/Charge Per Share - Fiscal |
| 1252 | `fnd28_value_18260q` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of quarterly field: Excludes Pre-tax Extraordinary Credit/Charge per Share - Fiscal |
| 1253 | `fnd28_value_18261q` | MATRIX | 0.500 | 风险与质量 | 0 | — | — | — | UNUSABLE | value of quarterly field: Includes Pre-tax Extraordinary Credit/Charge per Share - Fiscal |
| 1254 | `fnd28_value_18262q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Net Sales/Revenues |
| 1255 | `fnd28_value_18264q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Trailing 12 Months Earnings per Share |
| 1256 | `fnd28_value_18265q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Cash Flow per Share |
| 1257 | `fnd28_value_18266q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Dividends |
| 1258 | `fnd28_value_18267q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Gross Margin |
| 1259 | `fnd28_value_18268q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Net Margin Asset Utilization |
| 1260 | `fnd28_value_18269q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Trailing 12 Months Interest Expense |
| 1261 | `fnd28_value_18270q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Trailing 12 Months Income Taxes |
| 1262 | `fnd28_value_18271q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Trailing 12 Months Pre-Tax Income |
| 1263 | `fnd28_value_18280` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Goodwill/Cost in Excess of Assets Purchased |
| 1264 | `fnd28_value_18280a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Goodwill/Cost in Excess of Assets Purchased |
| 1265 | `fnd28_value_18281a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Non Convertible Debt |
| 1266 | `fnd28_value_18289q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Non-Redeemable Preferred Stock |
| 1267 | `fnd28_value_18290q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Redeemable Preferred Stock |
| 1268 | `fnd28_value_18304q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Pre-tax Margin |
| 1269 | `fnd28_value_18305q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Operating Profit |
| 1270 | `fnd28_value_18306q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Operating Margin |
| 1271 | `fnd28_value_18308q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months EBIT |
| 1272 | `fnd28_value_18309q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months EBITDA |
| 1273 | `fnd28_value_18310q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Trailing Twelve Months Net Cash Flow Operating Activities |
| 1274 | `fnd28_value_18311q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Trailing 12 Months Capital Expenditures |
| 1275 | `fnd28_value_18312q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Cost of Goods Sold |
| 1276 | `fnd28_value_18313q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Depreciation, Depletion & Amortization |
| 1277 | `fnd28_value_18318q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Cash Dividends Paid |
| 1278 | `fnd28_value_18321a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Stock Option Compensation Expense, Net of Tax |
| 1279 | `fnd28_value_18324q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Unrealized Valuation Gains/Losses - Total |
| 1280 | `fnd28_value_18375a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Land |
| 1281 | `fnd28_value_18376a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Buildings |
| 1282 | `fnd28_value_18377a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Machinery & Equipment |
| 1283 | `fnd28_value_18379a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Property, Plant & Equipment - Other |
| 1284 | `fnd28_value_18381a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Property, Plant & Equipment under Capitalized Leases |
| 1285 | `fnd28_value_18384a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accumulated Depreciation - Buildings |
| 1286 | `fnd28_value_18385a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accumulated Depreciation - Machinery & Equipment |
| 1287 | `fnd28_value_18387a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Accumulated Depreciation - Other Property, Plant & Equipment |
| 1288 | `fnd28_value_18389a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Accumulated Depreciation - PP&E under Capitalized Lease |
| 1289 | `fnd28_value_18420q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Fiscal Period Basic |
| 1290 | `fnd28_value_18426q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings Per Share (EPS) Included Extra Cr/Chg After Tax Basic |
| 1291 | `fnd28_value_18428q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Included Extra Pre-tax Cr/Chg Basic |
| 1292 | `fnd28_value_18446q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings Per Share (EPS) Included Extra Cr/Chg After Tax Fully Diluted |
| 1293 | `fnd28_value_18448q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Included Extra Pre-tax Cr/Chg Fully Diluted |
| 1294 | `fnd28_value_18457q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Earnings per Share Included Extra Pre-tax Cr/Chg Basic Revised |
| 1295 | `fnd28_value_18469q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Fiscal Period Basic Revised |
| 1296 | `fnd28_value_18470q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Fiscal Period Fully Diluted Revised |
| 1297 | `fnd28_value_18574q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Unrealized Valuation Gains/Losses Hedges/Derivatives |
| 1298 | `fnd28_value_18722a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Current Portion of Long Term Capital Lease Liabilities |
| 1299 | `fnd28_value_18852a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Comprehensive Income Hedging Gain/Loss |
| 1300 | `fnd28_value_18862q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Trailing Twelve Months Funds From Operations Other Fields |
| 1301 | `fnd28_value_19101a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of annual field: Interim Sales Q1 |
| 1302 | `fnd28_value_19102a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Sales Qtr2 |
| 1303 | `fnd28_value_19103a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Sales Qtr3 |
| 1304 | `fnd28_value_19104a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Sales Qtr4 |
| 1305 | `fnd28_value_19105a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Pre-tax Income Qtr1 |
| 1306 | `fnd28_value_19106a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Pre-tax Income Qtr1 |
| 1307 | `fnd28_value_19107a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Pre-tax Income Qtr1 Qtr3 |
| 1308 | `fnd28_value_19108a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Pre-tax Income Qtr1 Qtr4 |
| 1309 | `fnd28_value_19109a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Net Profit Qtr1 |
| 1310 | `fnd28_value_19110a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Net Profit Qtr2 |
| 1311 | `fnd28_value_19111a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Interim Net Profit Qtr3 |
| 1312 | `fnd28_value_19112a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of annual field: Interim Net Profit Q4 |
| 1313 | `fnd28_value_19501` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 1 - Sales |
| 1314 | `fnd28_value_19501a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 1 - Sales |
| 1315 | `fnd28_value_19502` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 1 - Operating Income |
| 1316 | `fnd28_value_19502a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 1 - Operating Income |
| 1317 | `fnd28_value_19503` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 1 - Assets |
| 1318 | `fnd28_value_19503a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 1 - Assets |
| 1319 | `fnd28_value_19504` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 1 - Capital Expenditures |
| 1320 | `fnd28_value_19504a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 1 - Capital Expenditures |
| 1321 | `fnd28_value_19505` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 1 - Depreciation |
| 1322 | `fnd28_value_19505a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 1 - Depreciation |
| 1323 | `fnd28_value_19511` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 2 - Sales |
| 1324 | `fnd28_value_19511a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 2 - Sales |
| 1325 | `fnd28_value_19512` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 2 - Operating Income |
| 1326 | `fnd28_value_19512a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 2 - Operating Income |
| 1327 | `fnd28_value_19513` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 2 - Assets |
| 1328 | `fnd28_value_19513a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 2 - Assets |
| 1329 | `fnd28_value_19514` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 2 - Capital Expenditures |
| 1330 | `fnd28_value_19514a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 2 - Capital Expenditures |
| 1331 | `fnd28_value_19515` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 2 - Depreciation |
| 1332 | `fnd28_value_19515a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 2 - Depreciation |
| 1333 | `fnd28_value_19521` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 3 - Sales |
| 1334 | `fnd28_value_19521a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 3 - Sales |
| 1335 | `fnd28_value_19522` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 3 - Operating Income |
| 1336 | `fnd28_value_19522a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 3 - Operating Income |
| 1337 | `fnd28_value_19523` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 3 - Assets |
| 1338 | `fnd28_value_19523a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 3 - Assets |
| 1339 | `fnd28_value_19524` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 3 - Capital Expenditures |
| 1340 | `fnd28_value_19524a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 3 - Capital Expenditures |
| 1341 | `fnd28_value_19525` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 3 - Depreciation |
| 1342 | `fnd28_value_19525a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 3 - Depreciation |
| 1343 | `fnd28_value_19531` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 4 - Sales |
| 1344 | `fnd28_value_19531a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 4 - Sales |
| 1345 | `fnd28_value_19532` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 4 - Operating Income |
| 1346 | `fnd28_value_19532a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 4 - Operating Income |
| 1347 | `fnd28_value_19533` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 4 - Assets |
| 1348 | `fnd28_value_19533a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 4 - Assets |
| 1349 | `fnd28_value_19534` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 4 - Capital Expenditures |
| 1350 | `fnd28_value_19534a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 4 - Capital Expenditures |
| 1351 | `fnd28_value_19535` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 4 - Depreciation |
| 1352 | `fnd28_value_19535a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 4 - Depreciation |
| 1353 | `fnd28_value_19541` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 5 - Sales |
| 1354 | `fnd28_value_19541a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 5 - Sales |
| 1355 | `fnd28_value_19542` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 5 - Operating Income |
| 1356 | `fnd28_value_19542a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 5 - Operating Income |
| 1357 | `fnd28_value_19543` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 5 - Assets |
| 1358 | `fnd28_value_19543a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 5 - Assets |
| 1359 | `fnd28_value_19544` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 5 - Capital Expenditures |
| 1360 | `fnd28_value_19544a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 5 - Capital Expenditures |
| 1361 | `fnd28_value_19545` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 5 - Depreciation |
| 1362 | `fnd28_value_19545a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 5 - Depreciation |
| 1363 | `fnd28_value_19551` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 6 - Sales |
| 1364 | `fnd28_value_19551a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Product Segment 6 - Sales |
| 1365 | `fnd28_value_19552` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 6 - Operating Income |
| 1366 | `fnd28_value_19553` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of field: Product Segment 6 - Assets |
| 1367 | `fnd28_value_19601a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 1 - Sales |
| 1368 | `fnd28_value_19602a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 1 - Operating Income |
| 1369 | `fnd28_value_19603a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 1 - Assets |
| 1370 | `fnd28_value_19604a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 1 - Capital Expenditures |
| 1371 | `fnd28_value_19605a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 1 - Depreciation |
| 1372 | `fnd28_value_19611a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 2 - Sales |
| 1373 | `fnd28_value_19612a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 2 - Operating Income |
| 1374 | `fnd28_value_19613a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 2 - Assets |
| 1375 | `fnd28_value_19614a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 2 - Capital Expenditures |
| 1376 | `fnd28_value_19621a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 3 - Sales |
| 1377 | `fnd28_value_19623a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 3 - Assets |
| 1378 | `fnd28_value_19624a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 3 - Capital Expenditures |
| 1379 | `fnd28_value_19631a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 4 - Sales |
| 1380 | `fnd28_value_19633a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 4 - Assets |
| 1381 | `fnd28_value_19634a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 4 - Capital Expenditures |
| 1382 | `fnd28_value_19641a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 5 - Sales |
| 1383 | `fnd28_value_19643a` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 5 - Assets |
| 1384 | `fnd28_value_19651a` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of annual field: Geographic Segment 6 - Sales |
| 1385 | `fnd28_value_19761a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1386 | `fnd28_value_19762a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1387 | `fnd28_value_19763a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1388 | `fnd28_value_19764a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1389 | `fnd28_value_19765a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1390 | `fnd28_value_19767a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1391 | `fnd28_value_19768a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1392 | `fnd28_value_19769a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1393 | `fnd28_value_19770a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1394 | `fnd28_value_19771a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1395 | `fnd28_value_19773a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1396 | `fnd28_value_19774a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1397 | `fnd28_value_19775a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1398 | `fnd28_value_19776a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1399 | `fnd28_value_19777a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1400 | `fnd28_value_19779a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1401 | `fnd28_value_19780a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1402 | `fnd28_value_19781a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1403 | `fnd28_value_19782a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1404 | `fnd28_value_19783a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1405 | `fnd28_value_19785a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1406 | `fnd28_value_19786a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1407 | `fnd28_value_19787a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1408 | `fnd28_value_19789a` | MATRIX | 0.500 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | value of annual field: Obsolete field, do not use for research purposes |
| 1409 | `fnd28_wcanstaq_value_01051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cost Of Goods Sold (Excl Depreciation) |
| 1410 | `fnd28_wcanstaq_value_01100q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Gross Income |
| 1411 | `fnd28_wcanstaq_value_01706q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income after Preferred Dividends (Basic EPS) |
| 1412 | `fnd28_wcanstaq_value_01751q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income Used to Calculate Earnings per Share |
| 1413 | `fnd28_wcbshtassetq_value_02001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash & Short Term Investments |
| 1414 | `fnd28_wcbshtassetq_value_02003q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash |
| 1415 | `fnd28_wcbshtassetq_value_02051q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Receivables (Net) |
| 1416 | `fnd28_wcbshtassetq_value_02101q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Inventories Total |
| 1417 | `fnd28_wcbshtassetq_value_02149q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Current Assets |
| 1418 | `fnd28_wcbshtassetq_value_02201q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Current Assets Total |
| 1419 | `fnd28_wcbshtassetq_value_02301q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant and Equipment - Gross |
| 1420 | `fnd28_wcbshtassetq_value_02401q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Accumulated Depreciation |
| 1421 | `fnd28_wcbshtassetq_value_02501q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant & Equipment - Net |
| 1422 | `fnd28_wcbshtassetq_value_02649q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Intangible Other Assets - Net |
| 1423 | `fnd28_wcbshtassetq_value_02652q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Assets |
| 1424 | `fnd28_wcbshtassetq_value_02999q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets |
| 1425 | `fnd28_wcbshtq_value_01001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Sales or Revenues |
| 1426 | `fnd28_wcbshtq_value_01051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cost Of Goods Sold (Excl Depreciation) |
| 1427 | `fnd28_wcbshtq_value_01151q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation, Depletion & Amortization |
| 1428 | `fnd28_wcbshtq_value_01250q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Income |
| 1429 | `fnd28_wcbshtq_value_01251q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Interest Expense on Debt |
| 1430 | `fnd28_wcbshtq_value_01401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Income |
| 1431 | `fnd28_wcbshtq_value_01451q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income Taxes |
| 1432 | `fnd28_wcbshtq_value_01501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Minority Interest |
| 1433 | `fnd28_wcbshtq_value_01505q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Discontinued Operations |
| 1434 | `fnd28_wcbshtq_value_01551q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income before Extraordinary Items/Preferred Dividends |
| 1435 | `fnd28_wcbshtq_value_01701q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Preferred Dividend Requirements |
| 1436 | `fnd28_wcbshtq_value_01706q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income after Preferred Dividends (Basic EPS) |
| 1437 | `fnd28_wcbshtq_value_02001q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash & Short Term Investments |
| 1438 | `fnd28_wcbshtq_value_02003q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash |
| 1439 | `fnd28_wcbshtq_value_02051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Receivables (Net) |
| 1440 | `fnd28_wcbshtq_value_02101q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Inventories Total |
| 1441 | `fnd28_wcbshtq_value_02201q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Current Assets Total |
| 1442 | `fnd28_wcbshtq_value_02301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant and Equipment - Gross |
| 1443 | `fnd28_wcbshtq_value_02401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Accumulated Depreciation |
| 1444 | `fnd28_wcbshtq_value_02501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant & Equipment - Net |
| 1445 | `fnd28_wcbshtq_value_02649q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Intangible Other Assets - Net |
| 1446 | `fnd28_wcbshtq_value_02999q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets |
| 1447 | `fnd28_wcbshtq_value_18722q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Portion of Long Term Capital Lease Liabilities |
| 1448 | `fnd28_wcfsq1_value_01001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Sales or Revenues |
| 1449 | `fnd28_wcfsq1_value_01051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cost Of Goods Sold (Excl Depreciation) |
| 1450 | `fnd28_wcfsq1_value_01151q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation, Depletion & Amortization |
| 1451 | `fnd28_wcfsq1_value_01250q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Income |
| 1452 | `fnd28_wcfsq1_value_01251q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Interest Expense on Debt |
| 1453 | `fnd28_wcfsq1_value_01401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Income |
| 1454 | `fnd28_wcfsq1_value_01451q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income Taxes |
| 1455 | `fnd28_wcfsq1_value_01501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Minority Interest |
| 1456 | `fnd28_wcfsq1_value_01505q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Discontinued Operations |
| 1457 | `fnd28_wcfsq1_value_01551q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income before Extraordinary Items/Preferred Dividends |
| 1458 | `fnd28_wcfsq1_value_01701q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Preferred Dividend Requirements |
| 1459 | `fnd28_wcfsq1_value_01706q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income after Preferred Dividends (Basic EPS) |
| 1460 | `fnd28_wcfsq1_value_02001q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash & Short Term Investments |
| 1461 | `fnd28_wcfsq1_value_02003q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash |
| 1462 | `fnd28_wcfsq1_value_02051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Receivables (Net) |
| 1463 | `fnd28_wcfsq1_value_02101q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Inventories Total |
| 1464 | `fnd28_wcfsq1_value_02201q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Current Assets Total |
| 1465 | `fnd28_wcfsq1_value_02301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant and Equipment - Gross |
| 1466 | `fnd28_wcfsq1_value_02401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Accumulated Depreciation |
| 1467 | `fnd28_wcfsq1_value_02501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant & Equipment - Net |
| 1468 | `fnd28_wcfsq1_value_02649q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Intangible Other Assets - Net |
| 1469 | `fnd28_wcfsq1_value_02999q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets |
| 1470 | `fnd28_wcfsq1_value_04001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income/Starting Line |
| 1471 | `fnd28_wcfsq1_value_04049q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation and Depletion |
| 1472 | `fnd28_wcfsq1_value_04151q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Cash Flow - Total |
| 1473 | `fnd28_wcfsq1_value_04301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Proceeds From Stock Options |
| 1474 | `fnd28_wcfsq1_value_04302q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Proceeds From Sale/Issuance of Stock |
| 1475 | `fnd28_wcfsq1_value_04351q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Disposal of Fixed Assets |
| 1476 | `fnd28_wcfsq1_value_04401q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Borrowings |
| 1477 | `fnd28_wcfsq1_value_04440q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Decrease in Investments |
| 1478 | `fnd28_wcfsq1_value_04446q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Sources - Financing |
| 1479 | `fnd28_wcfsq1_value_04796q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Sources - Investing |
| 1480 | `fnd28_wcfsq1_value_04821q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase/Decrease In Short Term Borrowings |
| 1481 | `fnd28_wcfsq1_value_04831q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Funds from/for Other Operating Activities |
| 1482 | `fnd28_wcfsq1_value_04840q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Effect of Exchange Rate on Cash |
| 1483 | `fnd28_wcfsq1_value_04851q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase/Decrease in Cash & Short Term Investments |
| 1484 | `fnd28_wcfsq1_value_18722q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Portion of Long Term Capital Lease Liabilities |
| 1485 | `fnd28_wcishtq_value_01001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Sales or Revenues |
| 1486 | `fnd28_wcishtq_value_01051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cost Of Goods Sold (Excl Depreciation) |
| 1487 | `fnd28_wcishtq_value_01100q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Gross Income |
| 1488 | `fnd28_wcishtq_value_01151q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation, Depletion & Amortization |
| 1489 | `fnd28_wcishtq_value_01230q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Operating Expenses |
| 1490 | `fnd28_wcishtq_value_01250q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Income |
| 1491 | `fnd28_wcishtq_value_01251q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Interest Expense on Debt |
| 1492 | `fnd28_wcishtq_value_01262q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Other Income/Expense Net |
| 1493 | `fnd28_wcishtq_value_01401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Income |
| 1494 | `fnd28_wcishtq_value_01451q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income Taxes |
| 1495 | `fnd28_wcishtq_value_01501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Minority Interest |
| 1496 | `fnd28_wcishtq_value_01551q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income before Extraordinary Items/Preferred Dividends |
| 1497 | `fnd28_wcishtq_value_01651q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income - Bottom Line |
| 1498 | `fnd28_wcishtq_value_01706q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income after Preferred Dividends (Basic EPS) |
| 1499 | `fnd28_wcishtq_value_01751q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income Used to Calculate Earnings per Share |
| 1500 | `fnd28_wcnddq1_value_01001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Sales or Revenues |
| 1501 | `fnd28_wcnddq1_value_01051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cost Of Goods Sold (Excl Depreciation) |
| 1502 | `fnd28_wcnddq1_value_01151q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation, Depletion & Amortization |
| 1503 | `fnd28_wcnddq1_value_01250q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Income |
| 1504 | `fnd28_wcnddq1_value_01251q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Interest Expense on Debt |
| 1505 | `fnd28_wcnddq1_value_01401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Income |
| 1506 | `fnd28_wcnddq1_value_01451q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income Taxes |
| 1507 | `fnd28_wcnddq1_value_01501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Minority Interest |
| 1508 | `fnd28_wcnddq1_value_01505q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Discontinued Operations |
| 1509 | `fnd28_wcnddq1_value_01551q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income before Extraordinary Items/Preferred Dividends |
| 1510 | `fnd28_wcnddq1_value_01701q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Preferred Dividend Requirements |
| 1511 | `fnd28_wcnddq1_value_01706q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income after Preferred Dividends (Basic EPS) |
| 1512 | `fnd28_wcnddq1_value_02001q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash & Short Term Investments |
| 1513 | `fnd28_wcnddq1_value_02003q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash |
| 1514 | `fnd28_wcnddq1_value_02051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Receivables (Net) |
| 1515 | `fnd28_wcnddq1_value_02101q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Inventories Total |
| 1516 | `fnd28_wcnddq1_value_02201q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Current Assets Total |
| 1517 | `fnd28_wcnddq1_value_02301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant and Equipment - Gross |
| 1518 | `fnd28_wcnddq1_value_02401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Accumulated Depreciation |
| 1519 | `fnd28_wcnddq1_value_02501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant & Equipment - Net |
| 1520 | `fnd28_wcnddq1_value_02649q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Intangible Other Assets - Net |
| 1521 | `fnd28_wcnddq1_value_02999q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets |
| 1522 | `fnd28_wcnddq1_value_04001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income/Starting Line |
| 1523 | `fnd28_wcnddq1_value_04049q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation and Depletion |
| 1524 | `fnd28_wcnddq1_value_04151q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Cash Flow - Total |
| 1525 | `fnd28_wcnddq1_value_04301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Proceeds From Stock Options |
| 1526 | `fnd28_wcnddq1_value_04302q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Proceeds From Sale/Issuance of Stock |
| 1527 | `fnd28_wcnddq1_value_04351q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Disposal of Fixed Assets |
| 1528 | `fnd28_wcnddq1_value_04401q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Borrowings |
| 1529 | `fnd28_wcnddq1_value_04440q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Decrease in Investments |
| 1530 | `fnd28_wcnddq1_value_04446q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Sources - Financing |
| 1531 | `fnd28_wcnddq1_value_04796q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Sources - Investing |
| 1532 | `fnd28_wcnddq1_value_04831q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Funds from/for Other Operating Activities |
| 1533 | `fnd28_wcnddq1_value_04840q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Effect of Exchange Rate on Cash |
| 1534 | `fnd28_wcnddq1_value_04851q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase/Decrease in Cash & Short Term Investments |
| 1535 | `fnd28_wcnddq1_value_05202q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Earnings per Share Fiscal Period End |
| 1536 | `fnd28_wcnewq_value_01100q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Gross Income |
| 1537 | `fnd28_wcnewq_value_01230q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Operating Expenses |
| 1538 | `fnd28_wcnewq_value_01262q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Income/Expense Net |
| 1539 | `fnd28_wcnewq_value_01651q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income - Bottom Line |
| 1540 | `fnd28_wcnewq_value_01751q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income Used to Calculate Earnings per Share |
| 1541 | `fnd28_wcnewq_value_02149q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Current Assets |
| 1542 | `fnd28_wcnewq_value_02652q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Assets |
| 1543 | `fnd28_wcnewq_value_04051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation, Depletion & Amortization |
| 1544 | `fnd28_wcnewq_value_04251q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Proceeds from Sale/Issuance of Common & Preferred |
| 1545 | `fnd28_wcsfq_value_04001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income/Starting Line |
| 1546 | `fnd28_wcsfq_value_04049q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation and Depletion |
| 1547 | `fnd28_wcsfq_value_04051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation, Depletion & Amortization |
| 1548 | `fnd28_wcsfq_value_04151q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Cash Flow - Total |
| 1549 | `fnd28_wcsfq_value_04201q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Funds from Operations |
| 1550 | `fnd28_wcsfq_value_04251q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Proceeds from Sale/Issuance of Common & Preferred |
| 1551 | `fnd28_wcsfq_value_04301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Proceeds From Stock Options |
| 1552 | `fnd28_wcsfq_value_04302q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Proceeds From Sale/Issuance of Stock |
| 1553 | `fnd28_wcsfq_value_04351q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Disposal of Fixed Assets |
| 1554 | `fnd28_wcsfq_value_04401q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Borrowings |
| 1555 | `fnd28_wcsfq_value_04440q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Decrease in Investments |
| 1556 | `fnd28_wcsfq_value_04446q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Sources - Financing |
| 1557 | `fnd28_wcsfq_value_04796q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Sources - Investing |
| 1558 | `fnd28_wcsfq_value_04821q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase/Decrease In Short Term Borrowings |
| 1559 | `fnd28_wcsfq_value_04830q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Decrease/Increase In Other Assets/Liabilities |
| 1560 | `fnd28_wcsfq_value_04831q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Funds from/for Other Operating Activities |
| 1561 | `fnd28_wcsfq_value_04840q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Effect of Exchange Rate on Cash |
| 1562 | `fnd28_wcsfq_value_04851q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase/Decrease in Cash & Short Term Investments |
| 1563 | `fnd28_wsbshtq_value_01001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Sales or Revenues |
| 1564 | `fnd28_wsbshtq_value_01051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cost Of Goods Sold (Excl Depreciation) |
| 1565 | `fnd28_wsbshtq_value_01100q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Gross Income |
| 1566 | `fnd28_wsbshtq_value_01151q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation, Depletion & Amortization |
| 1567 | `fnd28_wsbshtq_value_01230q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Operating Expenses |
| 1568 | `fnd28_wsbshtq_value_01250q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Operating Income |
| 1569 | `fnd28_wsbshtq_value_01251q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Interest Expense on Debt |
| 1570 | `fnd28_wsbshtq_value_01262q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Value of quarterly field: Other Income/Expense Net |
| 1571 | `fnd28_wsbshtq_value_01401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Pre-tax Income |
| 1572 | `fnd28_wsbshtq_value_01451q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Income Taxes |
| 1573 | `fnd28_wsbshtq_value_01501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Minority Interest |
| 1574 | `fnd28_wsbshtq_value_01505q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Discontinued Operations |
| 1575 | `fnd28_wsbshtq_value_01551q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income before Extraordinary Items/Preferred Dividends |
| 1576 | `fnd28_wsbshtq_value_01651q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income - Bottom Line |
| 1577 | `fnd28_wsbshtq_value_01701q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Preferred Dividend Requirements |
| 1578 | `fnd28_wsbshtq_value_01706q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income after Preferred Dividends (Basic EPS) |
| 1579 | `fnd28_wsbshtq_value_01751q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income Used to Calculate Earnings per Share |
| 1580 | `fnd28_wsbshtq_value_02001q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash & Short Term Investments |
| 1581 | `fnd28_wsbshtq_value_02003q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Cash |
| 1582 | `fnd28_wsbshtq_value_02051q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Receivables (Net) |
| 1583 | `fnd28_wsbshtq_value_02101q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Inventories Total |
| 1584 | `fnd28_wsbshtq_value_02149q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Current Assets |
| 1585 | `fnd28_wsbshtq_value_02201q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Assets Total |
| 1586 | `fnd28_wsbshtq_value_02301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant and Equipment - Gross |
| 1587 | `fnd28_wsbshtq_value_02401q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Accumulated Depreciation |
| 1588 | `fnd28_wsbshtq_value_02501q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Property, Plant & Equipment - Net |
| 1589 | `fnd28_wsbshtq_value_02649q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Intangible Other Assets - Net |
| 1590 | `fnd28_wsbshtq_value_02652q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Assets |
| 1591 | `fnd28_wsbshtq_value_02999q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Total Assets |
| 1592 | `fnd28_wsfq1_value_04001q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Net Income/Starting Line |
| 1593 | `fnd28_wsfq1_value_04049q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Depreciation and Depletion |
| 1594 | `fnd28_wsfq1_value_04151q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Cash Flow - Total |
| 1595 | `fnd28_wsfq1_value_04301q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Proceeds From Stock Options |
| 1596 | `fnd28_wsfq1_value_04302q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Proceeds From Sale/Issuance of Stock |
| 1597 | `fnd28_wsfq1_value_04351q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Disposal of Fixed Assets |
| 1598 | `fnd28_wsfq1_value_04401q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Long Term Borrowings |
| 1599 | `fnd28_wsfq1_value_04440q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Decrease in Investments |
| 1600 | `fnd28_wsfq1_value_04446q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Sources - Financing |
| 1601 | `fnd28_wsfq1_value_04796q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Other Sources - Investing |
| 1602 | `fnd28_wsfq1_value_04831q` | MATRIX | 0.500 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | value of quarterly field: Funds from/for Other Operating Activities |
| 1603 | `fnd28_wsfq1_value_04840q` | MATRIX | 0.500 | 宏观与行业 | 0 | — | — | — | UNUSABLE | value of quarterly field: Effect of Exchange Rate on Cash |
| 1604 | `fnd28_wsfq1_value_04851q` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | value of quarterly field: Increase/Decrease in Cash & Short Term Investments |
| 1605 | `fnd28_wsfq1_value_18722q` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | value of quarterly field: Current Portion of Long Term Capital Lease Liabilities |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

