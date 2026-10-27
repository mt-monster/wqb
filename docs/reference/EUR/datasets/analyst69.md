# analyst69 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst69` |
| 名称 | Fundamental Analyst Estimates |
| 类别 | ANALYST |
| 数据字段数(平台) | 813 |
| 覆盖率 | 0.648 |
| 平台已有 alpha | 14196 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

The FactSet Fundamental dataset provides comprehensive annual and interim financial statement data, ratios, and per-share metrics for global companies, with coverage starting from 1980 for developed markets and the 1990s for developing markets. The dataset includes restatements, detailed line items, and standardized fields, enabling robust cross-company and cross-market comparisons. Key fields include balance sheet, income statement, and cash flow items, as well as derived ratios such as return on equity, margins, and growth rates. This dataset is valuable for quantitative and fundamental analysis, backtesting, and predictive modeling, as it allows users to track historical financial performance, identify trends, and build factor models that can help forecast future price movements based o

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **813** |
| 类型分布 | VECTOR×573　MATRIX×240 |
| 平均覆盖率 | **0.648** |
| 覆盖率区间 | 0.26 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 234 | 28.8% |
| 中 (0.70–0.90) | 21 | 2.6% |
| 低 (0.50–0.70) | 550 | 67.7% |
| 稀疏 (<0.50) | 8 | 1.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 552 | 67.9% |
| UNTESTED | 261 | 32.1% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 261 / UNUSABLE 552 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 420 | 0.54 | anl69_best_analyst_rating、anl69_best_ebitda_numest、anl69_best_roe_numest |
| 盈利与财务 | 231 | 0.79 | anl69_best_cps_4wk_dn、anl69_best_cps_4wk_up、anl69_best_cps_numest |
| 其他 | 121 | 0.72 | anl69_best_bps、anl69_best_bps_4wk_chg、anl69_best_bps_4wk_dn |
| 元数据与非信号 | 19 | 0.81 | anl69_ltg_dif_best_cur_fiscal_year_period、anl69_ltg_dif_best_fiscal_period_dt、anl69_ltg_dif_most_recent_period_end_dt |
| 宏观与行业 | 13 | 0.82 | anl69_best_ltg_4wk_dn、anl69_best_ltg_4wk_up、anl69_best_ltg_numest |
| 持仓与资金流 | 9 | 0.64 | anl69_best_ffops_4wk_dn、anl69_best_ffops_4wk_up、anl69_best_ffops_numest |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl69_best_analyst_rating` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst Rating |
| 2 | `anl69_best_bps` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share |
| 3 | `anl69_best_bps_4wk_chg` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share 4 wk Chg |
| 4 | `anl69_best_bps_4wk_dn` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share 4 wk Down |
| 5 | `anl69_best_bps_4wk_up` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share 4 wk Up |
| 6 | `anl69_best_bps_chg_pct` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share % Chg |
| 7 | `anl69_best_bps_hi` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share High |
| 8 | `anl69_best_bps_lo` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share Low |
| 9 | `anl69_best_bps_median` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share Median |
| 10 | `anl69_best_bps_numest` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share # Ests |
| 11 | `anl69_best_cps_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share 4 wk Down |
| 12 | `anl69_best_cps_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share 4 wk Up |
| 13 | `anl69_best_cps_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share # Ests |
| 14 | `anl69_best_dps` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share |
| 15 | `anl69_best_dps_4wk_chg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share 4 wk Chg |
| 16 | `anl69_best_dps_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share 4 wk Down |
| 17 | `anl69_best_dps_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share 4 wk Up |
| 18 | `anl69_best_dps_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share High |
| 19 | `anl69_best_dps_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share Low |
| 20 | `anl69_best_dps_median` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share Median |
| 21 | `anl69_best_dps_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share # Ests |
| 22 | `anl69_best_dps_stddev` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend per share Std Dev |
| 23 | `anl69_best_ebit` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT |
| 24 | `anl69_best_ebit_4wk_chg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT 4 wk Chg |
| 25 | `anl69_best_ebit_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT 4 wk Up |
| 26 | `anl69_best_ebit_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT High |
| 27 | `anl69_best_ebit_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT Low |
| 28 | `anl69_best_ebit_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT # Ests |
| 29 | `anl69_best_ebitda_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA 4 wk Down |
| 30 | `anl69_best_ebitda_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA 4 wk Up |
| 31 | `anl69_best_ebitda_numest` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | EBITDA # Estimates |
| 32 | `anl69_best_eps_4wk_chg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share 4 wk Chg |
| 33 | `anl69_best_eps_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share 4 wk Down |
| 34 | `anl69_best_eps_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share 4 wk Up |
| 35 | `anl69_best_eps_chg_pct` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share % Chg |
| 36 | `anl69_best_eps_gaap` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP |
| 37 | `anl69_best_eps_gaap_4wk_chg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP 4 wk Chg |
| 38 | `anl69_best_eps_gaap_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP 4 wk Down |
| 39 | `anl69_best_eps_gaap_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP 4 wk Up |
| 40 | `anl69_best_eps_gaap_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP High |
| 41 | `anl69_best_eps_gaap_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP Low |
| 42 | `anl69_best_eps_gaap_median` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP Median |
| 43 | `anl69_best_eps_gaap_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP # Ests |
| 44 | `anl69_best_eps_gaap_stddev` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share GAAP Std Dev |
| 45 | `anl69_best_eps_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share High |
| 46 | `anl69_best_eps_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share Low |
| 47 | `anl69_best_eps_median` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share Median |
| 48 | `anl69_best_eps_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share # Ests |
| 49 | `anl69_best_eps_stddev` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share Std Dev |
| 50 | `anl69_best_ffops_4wk_dn` | VECTOR | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Funds from Operations per share 4 wk Down |
| 51 | `anl69_best_ffops_4wk_up` | VECTOR | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Funds from Operations per share 4 wk Up |
| 52 | `anl69_best_ffops_numest` | VECTOR | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Funds from Operations per share # Ests |
| 53 | `anl69_best_ltg_4wk_dn` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long term EPS growth rate 4 wk Down |
| 54 | `anl69_best_ltg_4wk_up` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long term EPS growth rate 4 wk Up |
| 55 | `anl69_best_ltg_numest` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long term EPS growth rate # Ests |
| 56 | `anl69_best_nav_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value 4 wk Down |
| 57 | `anl69_best_nav_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value 4 wk Up |
| 58 | `anl69_best_nav_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value # Ests |
| 59 | `anl69_best_ndebt_4wk_chg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT 4 wk Chg |
| 60 | `anl69_best_ndebt_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT 4 wk Down |
| 61 | `anl69_best_ndebt_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT 4 wk Up |
| 62 | `anl69_best_ndebt_chg_pct` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT % Chg |
| 63 | `anl69_best_ndebt_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT High |
| 64 | `anl69_best_ndebt_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT Low |
| 65 | `anl69_best_ndebt_median` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT Median |
| 66 | `anl69_best_ndebt_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT # Ests |
| 67 | `anl69_best_net_4wk_chg` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net Inc 4 wk Chg |
| 68 | `anl69_best_net_4wk_dn` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net Inc 4 wk Down |
| 69 | `anl69_best_net_4wk_up` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net Inc 4 wk Up |
| 70 | `anl69_best_net_chg_pct` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net Inc % Chg |
| 71 | `anl69_best_net_debt` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Debt |
| 72 | `anl69_best_net_gaap` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP |
| 73 | `anl69_best_net_gaap_4wk_chg` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP 4 wk Chg |
| 74 | `anl69_best_net_gaap_4wk_dn` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP 4 wk Down |
| 75 | `anl69_best_net_gaap_4wk_up` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP 4 wk Up |
| 76 | `anl69_best_net_gaap_hi` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP High |
| 77 | `anl69_best_net_gaap_lo` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP Low |
| 78 | `anl69_best_net_gaap_median` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP Median |
| 79 | `anl69_best_net_gaap_numest` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP # Ests |
| 80 | `anl69_best_net_gaap_stddev` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net GAAP Std Dev |
| 81 | `anl69_best_net_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income High |
| 82 | `anl69_best_net_income` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income |
| 83 | `anl69_best_net_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Income Low |
| 84 | `anl69_best_net_median` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net Inc Median |
| 85 | `anl69_best_net_numest` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net Inc # Ests |
| 86 | `anl69_best_net_stddev` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Net Inc Std Dev |
| 87 | `anl69_best_ni_adj_to_sales` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profit Margin |
| 88 | `anl69_best_opp` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit |
| 89 | `anl69_best_opp_4wk_chg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit 4 wk Chg |
| 90 | `anl69_best_opp_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit 4 wk Down |
| 91 | `anl69_best_opp_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit 4 wk Up |
| 92 | `anl69_best_opp_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit High |
| 93 | `anl69_best_opp_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit Low |
| 94 | `anl69_best_opp_median` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit Median |
| 95 | `anl69_best_opp_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit # Ests |
| 96 | `anl69_best_opp_to_sales` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Margin |
| 97 | `anl69_best_pe_ratio` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | P/E Ratio |
| 98 | `anl69_best_ptp` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit |
| 99 | `anl69_best_ptp_4wk_chg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit 4 wk Chg |
| 100 | `anl69_best_ptp_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit 4 wk Down |
| 101 | `anl69_best_ptp_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit 4 wk Up |
| 102 | `anl69_best_ptp_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit High |
| 103 | `anl69_best_ptp_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit Low |
| 104 | `anl69_best_ptp_median` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit Median |
| 105 | `anl69_best_ptp_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit # Ests |
| 106 | `anl69_best_ptp_stddev` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax profit Std Dev |
| 107 | `anl69_best_ptp_to_sales` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pre-Tax Margin |
| 108 | `anl69_best_px_bps_ratio` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | P/Bk |
| 109 | `anl69_best_roa_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets 4 wk Down |
| 110 | `anl69_best_roa_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets 4 wk Up |
| 111 | `anl69_best_roa_numest` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets # Ests |
| 112 | `anl69_best_roe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity |
| 113 | `anl69_best_roe_4wk_chg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity 4 wk Chg |
| 114 | `anl69_best_roe_4wk_dn` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity 4 wk Down |
| 115 | `anl69_best_roe_4wk_up` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity 4 wk Up |
| 116 | `anl69_best_roe_chg_pct` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity % Chg |
| 117 | `anl69_best_roe_hi` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity High |
| 118 | `anl69_best_roe_lo` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity Low |
| 119 | `anl69_best_roe_median` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity Median |
| 120 | `anl69_best_roe_numest` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Return on Equity # Estimates |
| 121 | `anl69_best_sales` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales |
| 122 | `anl69_best_sales_4wk_chg` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales 4 wk Chg |
| 123 | `anl69_best_sales_4wk_dn` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales 4 wk Down |
| 124 | `anl69_best_sales_4wk_up` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales 4 wk Up |
| 125 | `anl69_best_sales_chg_pct` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales % Chg |
| 126 | `anl69_best_sales_hi` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales High |
| 127 | `anl69_best_sales_lo` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales Low |
| 128 | `anl69_best_sales_median` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales Median |
| 129 | `anl69_best_sales_numest` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales # Ests |
| 130 | `anl69_best_sales_stddev` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales Std Dev |
| 131 | `anl69_best_target_4wk_chg` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Target Price 4 Wk Chg |
| 132 | `anl69_best_target_hi` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | High Target Price |
| 133 | `anl69_best_target_lo` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Low Target Price |
| 134 | `anl69_best_target_median` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Median Target Price |
| 135 | `anl69_best_target_price` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Target Price |
| 136 | `anl69_eqy_fund_crncy` | VECTOR | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Currency Override |
| 137 | `anl69_eqy_rec_cons` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Recommendation Consensus |
| 138 | `anl69_ltg_dif_best_crncy_iso` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency (ISO) |
| 139 | `anl69_ltg_dif_best_cur_fiscal_year_period` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Current Fiscal Year Period Date |
| 140 | `anl69_ltg_dif_best_eeps_cur_yr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Est Earnings per share Curr Year |
| 141 | `anl69_ltg_dif_best_eeps_nxt_yr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Est Earnings per share Next Year |
| 142 | `anl69_ltg_dif_best_fiscal_period_dt` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Fiscal Period Date |
| 143 | `anl69_ltg_dif_best_fperiod_override` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Fiscal Period Override |
| 144 | `anl69_ltg_dif_expected_report_dt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Date |
| 145 | `anl69_ltg_dif_expected_report_period` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Period |
| 146 | `anl69_ltg_dif_expected_report_time` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Time |
| 147 | `anl69_ltg_dif_market_status` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Market Status |
| 148 | `anl69_ltg_dif_most_recent_period_end_dt` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Most Recent Period End Date |
| 149 | `anl69_pe_all_delay_1_best_crncy_iso` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency (ISO) |
| 150 | `anl69_pe_all_delay_1_best_cur_fiscal_year_period` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Current Fiscal Year Period Date |
| 151 | `anl69_pe_all_delay_1_best_eeps_cur_yr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Est Earnings per share Curr Year |
| 152 | `anl69_pe_all_delay_1_best_eeps_nxt_yr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Est Earnings per share Next Year |
| 153 | `anl69_pe_all_delay_1_expected_report_dt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Date |
| 154 | `anl69_pe_all_delay_1_expected_report_time` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Time |
| 155 | `anl69_roe_best_crncy_iso` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency (ISO) |
| 156 | `anl69_roe_best_cur_fiscal_year_period` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Current Fiscal Year Period Date |
| 157 | `anl69_roe_best_eeps_cur_yr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Est Earnings per share Curr Year |
| 158 | `anl69_roe_best_eeps_nxt_yr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Est Earnings per share Next Year |
| 159 | `anl69_roe_best_fiscal_period_dt` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Fiscal Period Date |
| 160 | `anl69_roe_best_fperiod_override` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Fiscal Period Override |
| 161 | `anl69_roe_expected_report_dt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Date |
| 162 | `anl69_roe_expected_report_period` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Period |
| 163 | `anl69_roe_expected_report_time` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Time |
| 164 | `anl69_roe_market_status` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Market Status |
| 165 | `anl69_roe_most_recent_period_end_dt` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Most Recent Period End Date |
| 166 | `anl69_sales_best_crncy_iso` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Currency (ISO) |
| 167 | `anl69_sales_best_cur_fiscal_year_period` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Current Fiscal Year Period Date |
| 168 | `anl69_sales_best_eeps_cur_yr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Est Earnings per share Curr Year |
| 169 | `anl69_sales_best_eeps_nxt_yr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Est Earnings per share Next Year |
| 170 | `anl69_sales_best_fiscal_period_dt` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Fiscal Period Date |
| 171 | `anl69_sales_best_fperiod_override` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Fiscal Period Override |
| 172 | `anl69_sales_expected_report_dt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Date |
| 173 | `anl69_sales_expected_report_period` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Period |
| 174 | `anl69_sales_expected_report_time` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected Earnings Report Time |
| 175 | `anl69_sales_market_status` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Market Status |
| 176 | `anl69_sales_most_recent_period_end_dt` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Most Recent Period End Date |
| 177 | `anl69_tot_buy_rec` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Total Buy Recommendations |
| 178 | `anl69_tot_hold_rec` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Total Hold Recommendations |
| 179 | `anl69_tot_sell_rec` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Total Sell Recommendations |
| 180 | `anl69_best_cps` | VECTOR | 0.989 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share |
| 181 | `anl69_best_cps_hi` | VECTOR | 0.989 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share High |
| 182 | `anl69_best_cps_lo` | VECTOR | 0.989 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share Low |
| 183 | `anl69_best_cps_4wk_chg` | VECTOR | 0.985 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share 4 wk Chg |
| 184 | `anl69_best_roe_stddev` | VECTOR | 0.985 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity Std Dev |
| 185 | `anl69_best_ebit_median` | VECTOR | 0.984 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT Median |
| 186 | `anl69_best_ebit_to_sales` | VECTOR | 0.983 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT Margin |
| 187 | `anl69_best_ebitda` | VECTOR | 0.981 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA |
| 188 | `anl69_best_ebitda_hi` | VECTOR | 0.981 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA High |
| 189 | `anl69_best_ebitda_lo` | VECTOR | 0.981 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA Low |
| 190 | `anl69_best_px_cps_ratio` | VECTOR | 0.981 | 其他 | 0 | — | — | — | UNTESTED | P/CF |
| 191 | `anl69_best_ebitda_4wk_chg` | VECTOR | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA 4 wk Chg |
| 192 | `anl69_best_ebit_chg_pct` | VECTOR | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT % Chg |
| 193 | `anl69_best_bps_stddev` | VECTOR | 0.974 | 其他 | 0 | — | — | — | UNTESTED | Book value per share Std Dev |
| 194 | `anl69_best_cps_median` | VECTOR | 0.974 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share Median |
| 195 | `anl69_ltg_dif_best_cur_fiscal_qtr_period` | MATRIX | 0.970 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Current Fiscal Quarter Period Date |
| 196 | `anl69_roe_best_cur_fiscal_qtr_period` | MATRIX | 0.970 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Current Fiscal Quarter Period Date |
| 197 | `anl69_sales_best_cur_fiscal_qtr_period` | MATRIX | 0.970 | 其他 | 0 | — | — | — | UNTESTED | Current Fiscal Quarter Period D |
| 198 | `anl69_pe_all_delay_1_best_cur_fiscal_qtr_period` | MATRIX | 0.970 | 其他 | 0 | — | — | — | UNTESTED | Current Fiscal Quarter Period D |
| 199 | `anl69_best_cur_ev_to_ebitda` | VECTOR | 0.963 | 盈利与财务 | 0 | — | — | — | UNTESTED | EV to EBITDA |
| 200 | `anl69_best_opp_stddev` | VECTOR | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating Profit Std Dev |
| 201 | `anl69_best_cps_chg_pct` | VECTOR | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share % Chg |
| 202 | `anl69_best_ebit_stddev` | VECTOR | 0.959 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBIT Std Dev |
| 203 | `anl69_best_ev_to_best_ebit` | VECTOR | 0.957 | 盈利与财务 | 0 | — | — | — | UNTESTED | EV / EBIT |
| 204 | `anl69_best_ebitda_median` | VECTOR | 0.947 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA Median |
| 205 | `anl69_best_ebitda_stddev` | VECTOR | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA Std Dev |
| 206 | `anl69_best_ebitda_chg_pct` | VECTOR | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA % Chg |
| 207 | `anl69_best_ndebt_stddev` | VECTOR | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | NDEBT Std Dev |
| 208 | `consensus_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus estimate was updated for the selected metric. |
| 209 | `company_guidance_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest company guidance estimate was updated. |
| 210 | `consensus_adjusted_eps_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus adjusted earnings per share estimate was updated. |
| 211 | `consensus_book_value_per_share_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus book value per share estimate was updated. |
| 212 | `consensus_cash_flow_per_share_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus cash flow per share estimate was updated. |
| 213 | `consensus_dividend_per_share_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus dividend per share estimate was updated. |
| 214 | `consensus_ebit_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus EBIT estimate was updated. |
| 215 | `consensus_ebitda_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus EBITDA estimate was updated. |
| 216 | `consensus_eps_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus earnings per share estimate was updated. |
| 217 | `consensus_eps_gaap_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus GAAP earnings per share estimate was updated. |
| 218 | `consensus_funds_from_ops_per_share_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus funds from operations per share estimate was updated. |
| 219 | `consensus_nav_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus net asset value estimate was updated. |
| 220 | `consensus_net_debt_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus net debt estimate was updated. |
| 221 | `consensus_net_income_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus net income estimate was updated. |
| 222 | `consensus_net_income_new_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus net income (new methodology) estimate was updated. |
| 223 | `consensus_operating_profit_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus operating profit estimate was updated. |
| 224 | `consensus_pe_ratio_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus price-to-earnings ratio estimate was updated. |
| 225 | `consensus_pre_tax_profit_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus pre-tax profit estimate was updated. |
| 226 | `consensus_roa_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus return on assets estimate was updated. |
| 227 | `consensus_roe_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus return on equity estimate was updated. |
| 228 | `consensus_sales_estimate_last_update_dt` | VECTOR | 0.916 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus sales estimate was updated. |
| 229 | `anl69_ebit_best_ebit_4wk_dn` | VECTOR | 0.912 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst EBIT estimates that have been revised downward in the last 4 weeks |
| 230 | `anl69_cest_expected_report_period` | VECTOR | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected accounting period for the next earnings or financial report |
| 231 | `anl69_ltg_dif_best_cur_fiscal_semi_year_period` | MATRIX | 0.907 | 其他 | 0 | — | — | — | UNTESTED | Current Fiscal Semi-Year Period |
| 232 | `anl69_roe_best_cur_fiscal_semi_year_period` | MATRIX | 0.907 | 其他 | 0 | — | — | — | UNTESTED | Current Fiscal Semi-Year Period |
| 233 | `anl69_sales_best_cur_fiscal_semi_year_period` | MATRIX | 0.907 | 其他 | 0 | — | — | — | UNTESTED | Current Fiscal Semi-Year Period |
| 234 | `anl69_pe_all_delay_1_best_cur_fiscal_semi_year_period` | MATRIX | 0.907 | 其他 | 0 | — | — | — | UNTESTED | Current Fiscal Semi-Year Period |
| 235 | `anl69_best_cps_stddev` | VECTOR | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share Std Dev |
| 236 | `anl69_best_nav` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value |
| 237 | `anl69_best_nav_hi` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value High |
| 238 | `anl69_best_nav_lo` | VECTOR | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value Low |
| 239 | `anl69_best_nav_4wk_chg` | VECTOR | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value 4 wk Chg |
| 240 | `anl69_best_roa_median` | VECTOR | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets Median |
| 241 | `anl69_best_nav_median` | VECTOR | 0.839 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value Median |
| 242 | `anl69_best_roa` | VECTOR | 0.825 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets |
| 243 | `anl69_best_roa_hi` | VECTOR | 0.825 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets High |
| 244 | `anl69_best_roa_lo` | VECTOR | 0.825 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets Low |
| 245 | `anl69_best_roa_4wk_chg` | VECTOR | 0.817 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets 4 wk Chg |
| 246 | `anl69_best_roa_chg_pct` | VECTOR | 0.817 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets % Change |
| 247 | `anl69_eqy_recent_qt_end` | VECTOR | 0.793 | 其他 | 0 | — | — | — | UNTESTED | Most Recent Quarter End |
| 248 | `anl69_ltg_dif_latest_ann_dt_qtrly` | VECTOR | 0.786 | 其他 | 0 | — | — | — | UNTESTED | Latest Announcement Date Quarterly |
| 249 | `anl69_roe_latest_ann_dt_qtrly` | VECTOR | 0.786 | 其他 | 0 | — | — | — | UNTESTED | Latest Announcement Date Quarterly |
| 250 | `anl69_sales_latest_ann_dt_qtrly` | VECTOR | 0.786 | 其他 | 0 | — | — | — | UNTESTED | Latest Announcement Date Quarterly |
| 251 | `consensus_analyst_count_last_update_dt` | VECTOR | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus analyst count was updated. |
| 252 | `consensus_equity_estimate_last_update_dt` | VECTOR | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus equity estimate was updated. |
| 253 | `consensus_recommendation_last_update_dt` | VECTOR | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus analyst recommendation was updated. |
| 254 | `consensus_target_price_last_update_dt` | VECTOR | 0.735 | 修正与预期 | 0 | — | — | — | UNTESTED | Date when the latest consensus target price estimate was updated. |
| 255 | `company_guidance_last_update_dt` | VECTOR | 0.723 | 其他 | 0 | — | — | — | UNTESTED | Date when the company last updated its official guidance. |
| 256 | `anl69_best_ltg_eps` | VECTOR | 0.695 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long term EPS growth rate Earnings per share |
| 257 | `anl69_best_ltg_hi` | VECTOR | 0.695 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long term EPS growth rate High |
| 258 | `anl69_best_ltg_lo` | VECTOR | 0.695 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long term EPS growth rate Low |
| 259 | `anl69_best_ltg_4wk_chg` | VECTOR | 0.683 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long term EPS growth rate 4 wk Chg |
| 260 | `anl69_best_ltg_median` | VECTOR | 0.641 | 宏观与行业 | 0 | — | — | — | UNTESTED | Long term EPS growth rate Median |
| 261 | `anl69_best_nav_stddev` | VECTOR | 0.628 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value Std Dev |
| 262 | `anl69_best_ltg_chg_pct` | VECTOR | 0.590 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Long term EPS growth rate % Chg |
| 263 | `anl69_best_aeps_lst_qtr` | VECTOR | 0.564 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Actual Earnings per share Last Quarter |
| 264 | `anl69_best_roa_stddev` | VECTOR | 0.554 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on Assets Std Dev |
| 265 | `anl69_aeps_best_aeps_lst_qtr` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The actual reported Earnings Per Share (EPS) value from the most recent fiscal quarter |
| 266 | `anl69_aeps_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code (e.g., USD, EUR) for the consensus estimate values |
| 267 | `anl69_aeps_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier indicating the current fiscal quarter period for the company as of the point-in-time estimate |
| 268 | `anl69_aeps_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Semi-Year Period |
| 269 | `anl69_aeps_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current fiscal year period associated with the consensus or "best" estimate, likely denoting the fiscal year covered by consensus estimates |
| 270 | `anl69_aeps_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The current consensus estimate for Earnings Per Share (EPS) for the ongoing fiscal year |
| 271 | `anl69_aeps_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus estimate for Earnings Per Share (EPS) for the next fiscal year |
| 272 | `anl69_aeps_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The specific date marking the end of the current or forecasted fiscal period being referenced in the estimates |
| 273 | `anl69_aeps_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 274 | `anl69_aeps_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled date when the company's earnings report is expected to be released |
| 275 | `anl69_aeps_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The reporting period (e.g., fiscal quarter or year) for which the upcoming earnings report is expected to cover |
| 276 | `anl69_aeps_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected specific time of day when the company's earnings report will be released |
| 277 | `anl69_aeps_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly earnings announcement |
| 278 | `anl69_aeps_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 279 | `anl69_aeps_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The end date of the company’s most recently completed reporting period |
| 280 | `anl69_analyst_best_analyst_rating` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The aggregated analyst recommendation rating, numerically coded (1=Strong Buy, 2=Buy, 3=Hold, 4=Reduce, 5=Sell), indicating consensus analys |
| 281 | `anl69_analyst_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code for the currency in which the consensus estimate is reported |
| 282 | `anl69_analyst_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date representing the current fiscal quarter period for the company according to analyst consensus estimates |
| 283 | `anl69_analyst_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date representing the current fiscal semi-annual (half-year) period for the company according to analyst consensus estimates |
| 284 | `anl69_analyst_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date representing the current fiscal year period for the company according to analyst consensus estimates |
| 285 | `anl69_analyst_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of earnings per share (EPS) for the current fiscal year |
| 286 | `anl69_analyst_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of earnings per share (EPS) for the next fiscal year |
| 287 | `anl69_analyst_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date representing the end or reference point of the fiscal period used in analyst estimates |
| 288 | `anl69_analyst_best_fperiod_override` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Override value for the fiscal period used in consensus estimates when the default period is not applicable |
| 289 | `anl69_analyst_expected_report_dt` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The expected date the company will release its earnings report |
| 290 | `anl69_analyst_expected_report_period` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The fiscal period (quarter, semi-annual, or year) during which the next earnings report is expected |
| 291 | `anl69_analyst_expected_report_time` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The expected time of day at which the earnings report will be released |
| 292 | `anl69_analyst_latest_ann_dt_qtrly` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly earnings or financial announcement by the company |
| 293 | `anl69_analyst_market_status` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Indicator denoting the current trading status of the market (e.g., open, closed) |
| 294 | `anl69_analyst_most_recent_period_end_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The end date of the most recent fiscal or reporting period for which analyst estimates or data are available |
| 295 | `anl69_analyst_tot_analyst_rec` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The total number of analysts providing recommendations or estimates for the security |
| 296 | `anl69_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code representing the currency of the reported or estimated financial metrics |
| 297 | `anl69_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date (or identifier) for the company's current fiscal quarter period for which financial data or estimates apply |
| 298 | `anl69_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The current fiscal semi-annual period (first half/second half of fiscal year) for which estimates are reported, based on consensus |
| 299 | `anl69_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date (or identifier) for the company's current fiscal year period for which financial data or estimates apply |
| 300 | `anl69_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for the company's earnings per share (EPS) for the current fiscal year |
| 301 | `anl69_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for the company's earnings per share (EPS) for the next fiscal year |
| 302 | `anl69_best_eps` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus (best) estimate of earnings per share (EPS) from analysts as of a specific date |
| 303 | `anl69_best_fperiod_override` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Fiscal period override identifier used if the estimate relates to a non-standard or adjusted fiscal period |
| 304 | `anl69_bps_best_bps` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus (best estimate) for Book Value Per Share (BPS) for the company |
| 305 | `anl69_bps_best_bps_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Absolute change in the consensus Book Value Per Share (BPS) estimate over the last four weeks |
| 306 | `anl69_bps_best_bps_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst BPS estimates revised downward in the past four weeks |
| 307 | `anl69_bps_best_bps_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of BPS estimates revised up over the past 4 weeks |
| 308 | `anl69_bps_best_bps_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The percentage change in the consensus Book Value Per Share (BPS) estimate over a specified period, commonly compared to the previous estima |
| 309 | `anl69_bps_best_bps_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest BPS value among all contributing analyst estimates for the current period |
| 310 | `anl69_bps_best_bps_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest BPS value among all contributing analyst estimates for the current period |
| 311 | `anl69_bps_best_bps_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value among analyst estimates for Book Value Per Share (BPS) for the specified period |
| 312 | `anl69_bps_best_bps_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates included in calculating the best BPS consensus figure |
| 313 | `anl69_bps_best_bps_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation among all contributing analyst estimates of BPS, measuring dispersion |
| 314 | `anl69_bps_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO code for currency in which the best BPS estimate is reported (e.g., USD, EUR) |
| 315 | `anl69_bps_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier for the current fiscal quarter period for which the estimate is relevant |
| 316 | `anl69_bps_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Identifier of the current reporting semi-annual fiscal period for the company |
| 317 | `anl69_bps_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The current fiscal year period relevant for the best BPS estimate |
| 318 | `anl69_bps_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate of Earnings Per Share (EPS) for the current fiscal year |
| 319 | `anl69_bps_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Best (primary consensus) estimate for Earnings Per Share (EPS) for the next fiscal year |
| 320 | `anl69_bps_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date marking the end of the fiscal period relevant for the best BPS estimate |
| 321 | `anl69_bps_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 322 | `anl69_bps_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled or expected date for the company’s next earnings or financial report |
| 323 | `anl69_bps_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The fiscal period expected to be covered in the upcoming earnings report (for BPS) |
| 324 | `anl69_bps_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Time at which the earnings report is expected to be published |
| 325 | `anl69_bps_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly earnings announcement for the company |
| 326 | `anl69_bps_market_status` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current status of the market (open, closed, pre-market, post-market, etc.) at the time of estimate |
| 327 | `anl69_bps_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The end date of the most recently reported fiscal period for the company (e.g., last quarter's or semiannual close date) |
| 328 | `anl69_cest_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code for the estimates in the dataset (e.g., USD, EUR) |
| 329 | `anl69_cest_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Quarter Period D |
| 330 | `anl69_cest_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Semi-Year Period |
| 331 | `anl69_cest_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or period identifier representing the current fiscal year for which the best estimate or consensus is provided |
| 332 | `anl69_cest_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best-estimate expected earnings per share (EPS) for the current fiscal year |
| 333 | `anl69_cest_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best-estimate expected earnings per share (EPS) for the next fiscal year |
| 334 | `anl69_cest_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The fiscal period's end date that the estimate or consensus value refers to |
| 335 | `anl69_cest_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 336 | `anl69_cest_cest_sales` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Company-issued guidance (forward-looking estimate) for expected sales/revenue for the period |
| 337 | `anl69_cest_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled or expected date for the company's upcoming earnings report release |
| 338 | `anl69_cest_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled or expected time (hour/minute) for the company's upcoming earnings report release |
| 339 | `anl69_cest_latest_ann_dt_qtrly` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly financial results announcement by the company |
| 340 | `anl69_cest_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 341 | `anl69_cest_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recently reported accounting period |
| 342 | `anl69_cps_best_cps` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus (best/primary) point-in-time analyst estimate for Cash Per Share (CPS) |
| 343 | `anl69_cps_best_cps_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the consensus CPS estimate over the last four weeks |
| 344 | `anl69_cps_best_cps_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst CPS estimates that have been revised downward in the past 4 weeks |
| 345 | `anl69_cps_best_cps_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst CPS estimates that have been revised upward in the past 4 weeks |
| 346 | `anl69_cps_best_cps_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the consensus Cash Per Share (CPS) estimate over a specified period (likely 4 weeks) |
| 347 | `anl69_cps_best_cps_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate in the consensus for Cash per Share (CPS) |
| 348 | `anl69_cps_best_cps_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest consensus analyst estimate for Cash Per Share (CPS) for the specified observation period |
| 349 | `anl69_cps_best_cps_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of analyst estimates for Cash Per Share (CPS) |
| 350 | `anl69_cps_best_cps_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the consensus CPS figure |
| 351 | `anl69_cps_best_cps_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation across analyst estimates for Cash Per Share (CPS), indicating dispersion/confidence |
| 352 | `anl69_cps_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The ISO currency code in which the consensus estimates are denominated (e.g., EUR, USD) |
| 353 | `anl69_cps_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Identifier or date for the current fiscal quarter being analyzed |
| 354 | `anl69_cps_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Identifier or date for the current fiscal semi-annual (half-year) financial period |
| 355 | `anl69_cps_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The specific current fiscal year period (e.g., FY2023) being referenced for CPS estimates or reporting |
| 356 | `anl69_cps_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of Earnings Per Share (EPS) for the current fiscal year |
| 357 | `anl69_cps_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of Earnings Per Share (EPS) for next fiscal year |
| 358 | `anl69_cps_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or code representing the fiscal period associated with the current best estimate |
| 359 | `anl69_cps_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 360 | `anl69_cps_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled date for the upcoming earnings report for the relevant period |
| 361 | `anl69_cps_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The fiscal period (quarter/year) expected to be covered by the upcoming earnings report |
| 362 | `anl69_cps_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled time of day for the upcoming earnings report release |
| 363 | `anl69_cps_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly earnings announcement |
| 364 | `anl69_cps_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 365 | `anl69_cps_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recently reported financial period |
| 366 | `anl69_dps_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code indicating the currency in which the best DPS estimate is denominated (e.g., JPY, USD) |
| 367 | `anl69_dps_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or period for the best-consensus estimate of the company's current fiscal quarter |
| 368 | `anl69_dps_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier or date for the current fiscal semi-year (half-year) period related to DPS estimate |
| 369 | `anl69_dps_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier or date for the current fiscal year period relevant to the DPS estimate |
| 370 | `anl69_dps_best_dps` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus (BEST) estimate of Dividends Per Share (DPS) for the relevant period |
| 371 | `anl69_dps_best_dps_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The change in the consensus dividend per share (DPS) estimate over the past four weeks |
| 372 | `anl69_dps_best_dps_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst DPS estimates that decreased in the last 4 weeks |
| 373 | `anl69_dps_best_dps_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The number of upward revisions to the dividend per share (DPS) estimate made by analysts in the last four weeks |
| 374 | `anl69_dps_best_dps_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest estimate value for Dividend Per Share (DPS) among contributing analysts, showing maximum forecast for the period |
| 375 | `anl69_dps_best_dps_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst consensus estimate for Dividend Per Share (DPS) for the relevant period |
| 376 | `anl69_dps_best_dps_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of analyst estimates for dividend per share, representing the middle forecast among all contributors |
| 377 | `anl69_dps_best_dps_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates that contribute to the consensus DPS figure |
| 378 | `anl69_dps_best_dps_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst Dividend Per Share (DPS) estimates, measuring the dispersion or consensus variability for the period |
| 379 | `anl69_dps_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus estimate for earnings per share (EPS) for the company for the current fiscal year |
| 380 | `anl69_dps_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus estimate for earnings per share (EPS) for the company for the next fiscal year |
| 381 | `anl69_dps_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date marking the fiscal period (e.g., quarter or year) relevant to the best DPS estimate |
| 382 | `anl69_dps_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 383 | `anl69_dps_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The anticipated date when the company's earnings report will be released |
| 384 | `anl69_dps_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fiscal period in which the earnings report (and related Dividend Per Share data) is expected to be announced |
| 385 | `anl69_dps_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The anticipated time of day when the company's earnings report will be released |
| 386 | `anl69_dps_latest_ann_dt_qtrly` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Date of the most recent quarterly financial announcement or report for the company |
| 387 | `anl69_dps_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 388 | `anl69_dps_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The end date of the company’s most recently completed financial reporting period |
| 389 | `anl69_ebit_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code (e.g. USD, EUR) for the EBIT estimate values |
| 390 | `anl69_ebit_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier/code for the current fiscal quarter in focus for the EBIT estimate (e.g., Q1, Q2) |
| 391 | `anl69_ebit_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Semi-Year Period |
| 392 | `anl69_ebit_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date (or identifier) representing the company's current fiscal year period as used for consensus EBIT estimates |
| 393 | `anl69_ebit_best_ebit` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The best consensus estimate of earnings before interest and taxes (EBIT) for the relevant fiscal period |
| 394 | `anl69_ebit_best_ebit_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The change in consensus EBIT estimate over the most recent 4-week period, showing estimate momentum or revisions |
| 395 | `anl69_ebit_best_ebit_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst EBIT estimates that have been revised upward in the last 4 weeks |
| 396 | `anl69_ebit_best_ebit_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the consensus EBIT estimate over the specified period |
| 397 | `anl69_ebit_best_ebit_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst EBIT estimate among the consensus for the current period |
| 398 | `anl69_ebit_best_ebit_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate for EBIT for the specified period and region (AMR) |
| 399 | `anl69_ebit_best_ebit_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of analyst EBIT estimates |
| 400 | `anl69_ebit_best_ebit_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the best consensus EBIT figure |
| 401 | `anl69_ebit_best_ebit_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The standard deviation of analyst EBIT estimates, showing the dispersion or variability among contributing forecasts |
| 402 | `anl69_ebit_best_ebit_to_sales` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus EBIT margin, calculated as EBIT divided by sales/revenue (expressing operating profitability as a percentage of sales) |
| 403 | `anl69_ebit_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimated EPS (Earnings Per Share) for the current fiscal year |
| 404 | `anl69_ebit_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for earnings per share (EPS) for the next fiscal year |
| 405 | `anl69_ebit_best_ev_to_best_ebit` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Ratio of enterprise value to best consensus EBIT, a valuation metric |
| 406 | `anl69_ebit_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date corresponding to the fiscal period for which the consensus EBIT estimate is made |
| 407 | `anl69_ebit_best_fperiod_override` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 408 | `anl69_ebit_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled date when the company's earnings report is expected to be released |
| 409 | `anl69_ebit_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The fiscal period (e.g., quarter, half-year) for which the earnings report is expected, identified as the reporting scope |
| 410 | `anl69_ebit_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled time when the company's earnings report is expected to be released |
| 411 | `anl69_ebit_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Most recent announcement date for quarterly results pertaining to EBIT |
| 412 | `anl69_ebit_market_status` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Indicates the current market status (e.g., open, closed) relevant to the data timestamp |
| 413 | `anl69_ebit_most_recent_period_end_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | End date of the most recently completed fiscal period for the entity, regardless of estimate timing |
| 414 | `anl69_ebitda_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The ISO code for the currency in which the EBITDA estimate is reported (e.g., USD, CNY) |
| 415 | `anl69_ebitda_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date representing the best estimate of the current fiscal quarter period end for the company, as determined by consensus or guidance |
| 416 | `anl69_ebitda_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier representing the current fiscal semi-year period for which EBITDA estimates are applicable |
| 417 | `anl69_ebitda_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date representing the best estimate of the current fiscal year period end for the company, as determined by consensus or guidance |
| 418 | `anl69_ebitda_best_ebitda` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The best (consensus or most representative) estimate of EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) for the com |
| 419 | `anl69_ebitda_best_ebitda_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Absolute change in the EBITDA consensus estimate over the past 4 weeks |
| 420 | `anl69_ebitda_best_ebitda_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Count of analysts who have revised their EBITDA estimate downward in the past 4 weeks |
| 421 | `anl69_ebitda_best_ebitda_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst upward revisions to the consensus EBITDA estimate over the past four weeks |
| 422 | `anl69_ebitda_best_ebitda_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the consensus EBITDA estimate over the specified period, usually recent weeks |
| 423 | `anl69_ebitda_best_ebitda_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest consensus estimate for EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) among contributing analysts for the  |
| 424 | `anl69_ebitda_best_ebitda_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest consensus estimate for EBITDA among contributing analysts for the best (primary) estimate as of a specific observation date |
| 425 | `anl69_ebitda_best_ebitda_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The median value among analyst estimates for EBITDA included in the BEST consensus for the specified period |
| 426 | `anl69_ebitda_best_ebitda_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of individual analyst EBITDA estimates included in the consensus calculation |
| 427 | `anl69_ebitda_best_ebitda_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst EBITDA estimates, indicating dispersion or disagreement in consensus |
| 428 | `anl69_ebitda_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate of Earnings Per Share (EPS) for the current fiscal year |
| 429 | `anl69_ebitda_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus analyst estimate for the company’s Earnings Per Share (EPS) for the next fiscal year |
| 430 | `anl69_ebitda_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date marking the end of the fiscal period to which the EBITDA estimate applies |
| 431 | `anl69_ebitda_best_fperiod_override` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Override identifier for the fiscal period to which the current best EBITDA estimate applies |
| 432 | `anl69_ebitda_expected_report_dt` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The expected date when the company will release its earnings report relevant to the EBITDA estimate |
| 433 | `anl69_ebitda_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fiscal period (e.g., quarter, year) for which the next earnings report or disclosure is expected |
| 434 | `anl69_ebitda_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled or projected time (of day) for the company's earnings or financial report related to EBITDA |
| 435 | `anl69_ebitda_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the most recent quarterly earnings announcement for the company |
| 436 | `anl69_ebitda_market_status` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Market Status |
| 437 | `anl69_ebitda_most_recent_period_end_dt` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | End date of the most recently reported fiscal period for the company |
| 438 | `anl69_eps_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code (e.g., JPY, USD) in which the consensus EPS estimate is reported |
| 439 | `anl69_eps_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier representing the current fiscal quarter period for which the best (consensus) estimate is reported |
| 440 | `anl69_eps_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Semi-Year Period |
| 441 | `anl69_eps_best_cur_fiscal_year_period` | MATRIX | 0.500 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | The date or identifier of the current fiscal year period for the company |
| 442 | `anl69_eps_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated consensus EPS value for the current fiscal year for the selected company |
| 443 | `anl69_eps_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus analyst estimate for earnings per share (EPS) for the next fiscal year |
| 444 | `anl69_eps_best_eps` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The current consensus estimate of earnings per share (EPS), representing the aggregated analyst forecast for the specified period |
| 445 | `anl69_eps_best_eps_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The change in the consensus EPS estimate over the most recent four-week period |
| 446 | `anl69_eps_best_eps_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst EPS estimates revised downward in the last four weeks |
| 447 | `anl69_eps_best_eps_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst EPS estimates revised upward in the last four weeks |
| 448 | `anl69_eps_best_eps_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the consensus EPS estimate over a specified period |
| 449 | `anl69_eps_best_eps_gaap_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of GAAP EPS estimates revised downward in the last four weeks |
| 450 | `anl69_eps_best_eps_gaap_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of GAAP EPS estimates revised upward in the last four weeks |
| 451 | `anl69_eps_best_eps_gaap_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of all GAAP-based analyst EPS estimates for the period |
| 452 | `anl69_eps_best_eps_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The highest analyst estimate of earnings per share (EPS) within the contributing estimates for the specified period |
| 453 | `anl69_eps_best_eps_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst consensus estimate for EPS (earnings per share) for the point-in-time period |
| 454 | `anl69_eps_best_eps_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of analyst consensus estimates for Earnings Per Share (EPS) for the selected company and period |
| 455 | `anl69_eps_best_eps_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The number of individual analyst estimates contributing to the consensus EPS figure |
| 456 | `anl69_eps_best_eps_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst EPS estimates, showing variability or dispersion among estimates |
| 457 | `anl69_eps_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date corresponding to the end of the fiscal period relevant to the EPS estimate |
| 458 | `anl69_eps_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 459 | `anl69_eps_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Anticipated date when the company's earnings report will be released |
| 460 | `anl69_eps_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The fiscal period for which the upcoming earnings (EPS) report is expected to cover |
| 461 | `anl69_eps_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled time for the upcoming earnings report announcement |
| 462 | `anl69_eps_gaap_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code in which the estimates are denominated (e.g., EUR, USD) |
| 463 | `anl69_eps_gaap_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier representing the current fiscal quarter period for the company as considered in consensus estimates |
| 464 | `anl69_eps_gaap_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier representing the current fiscal semi-annual period for the company as considered in consensus estimates |
| 465 | `anl69_eps_gaap_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier representing the current fiscal year period for the company as considered in consensus estimates |
| 466 | `anl69_eps_gaap_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus estimate of GAAP earnings per share (EPS) for the current fiscal year |
| 467 | `anl69_eps_gaap_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus estimate of GAAP earnings per share (EPS) for the next fiscal year |
| 468 | `anl69_eps_gaap_best_eps_gaap` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus "best" estimate of GAAP earnings per share (EPS) for the relevant period |
| 469 | `anl69_eps_gaap_best_eps_gaap_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the consensus GAAP EPS estimate over the past 4 weeks |
| 470 | `anl69_eps_gaap_best_eps_gaap_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The highest GAAP EPS estimate among contributing analysts for the specified fiscal period |
| 471 | `anl69_eps_gaap_best_eps_gaap_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The lowest analyst estimate among the contributors for EPS (under GAAP accounting) for the considered period |
| 472 | `anl69_eps_gaap_best_eps_gaap_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The number of individual analyst estimates that contribute to the consensus GAAP EPS estimate |
| 473 | `anl69_eps_gaap_best_eps_gaap_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation among analyst GAAP EPS estimates, indicating dispersion or variability |
| 474 | `anl69_eps_gaap_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 475 | `anl69_eps_gaap_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected date on which the company's earnings report will be released |
| 476 | `anl69_eps_gaap_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected time of day at which the company's earnings report will be released |
| 477 | `anl69_eps_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The date of the most recent quarterly earnings announcement for the equity |
| 478 | `anl69_eps_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 479 | `anl69_eps_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recently completed fiscal period for the company |
| 480 | `anl69_eqy_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code representing the currency in which consensus estimates are denominated (e.g., USD, CNY) |
| 481 | `anl69_eqy_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The current fiscal quarter period (e.g., Q1, Q2, Q3, Q4 date or code) used in consensus estimates |
| 482 | `anl69_eqy_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The identifier or label for the company's current fiscal semi-annual (half-year) period being referenced by consensus or estimates |
| 483 | `anl69_eqy_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or period marking the current fiscal year for the company as used in consensus estimates |
| 484 | `anl69_eqy_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of Earnings Per Share (EPS) for the current fiscal year |
| 485 | `anl69_eqy_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of Earnings Per Share (EPS) for the next fiscal year |
| 486 | `anl69_eqy_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date corresponding to the best estimate of the relevant fiscal period for the equity, typically representing the period being forecasted |
| 487 | `anl69_eqy_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 488 | `anl69_eqy_eqy_fund_crncy` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The currency code (ISO format, e.g., USD, EUR, JPY) representing the reporting or functional currency used for all financial data and estima |
| 489 | `anl69_eqy_eqy_rec_cons` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus recommendation for the equity, typically indicating the aggregate analyst consensus (e.g., Buy, Hold, Sell) on the stock |
| 490 | `anl69_eqy_eqy_recent_qt_end` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The end date of the most recently finished fiscal quarter for the company |
| 491 | `anl69_eqy_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled or expected date on which earnings or financial results will be reported for the company |
| 492 | `anl69_eqy_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fiscal period (e.g., quarter or year) for which the next earnings report is expected |
| 493 | `anl69_eqy_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Time of day at which the company's earnings report is expected to be released |
| 494 | `anl69_eqy_latest_ann_dt_qtrly` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Most recent date on which the company announced quarterly financial results |
| 495 | `anl69_eqy_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 496 | `anl69_eqy_most_recent_period_end_dt` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The end date of the most recently completed fiscal period for the equity |
| 497 | `anl69_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date when the company is expected to release its earnings report |
| 498 | `anl69_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The anticipated time (hour/minute) at which the company is expected to release its earnings report, as forecast by Bloomberg |
| 499 | `anl69_ffops_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code (e.g., USD, EUR) for the reported FFOPS estimate |
| 500 | `anl69_ffops_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current fiscal quarter period for which the consensus FFOPS estimate applies |
| 501 | `anl69_ffops_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current fiscal semi-annual period relevant to the best estimate—e.g., H1 or H2 if company reports twice yearly |
| 502 | `anl69_ffops_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current fiscal year and period for which the consensus FFOPS estimate applies |
| 503 | `anl69_ffops_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus “best” estimate of Earnings Per Share (EPS) for the current fiscal year |
| 504 | `anl69_ffops_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus “best” estimate of Earnings Per Share (EPS) for the next fiscal year |
| 505 | `anl69_ffops_best_ffops` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus “best” estimate of Funds From Operations per Share (FFOPS), a key metric for REITs and real estate equities |
| 506 | `anl69_ffops_best_ffops_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in consensus "best" Funds From Operations per Share (FFOPS) estimate over the past four weeks |
| 507 | `anl69_ffops_best_ffops_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst FFOPS estimates that have been revised downward in the past four weeks |
| 508 | `anl69_ffops_best_ffops_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst FFOPS estimates that have been revised upward in the past four weeks |
| 509 | `anl69_ffops_best_ffops_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change of the consensus “best” FFOPS estimate over a specified previous period |
| 510 | `anl69_ffops_best_ffops_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest FFOPS estimate among contributing analysts for the current period |
| 511 | `anl69_ffops_best_ffops_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate contributing to the consensus FFOPS (“best” low FFOPS estimate) |
| 512 | `anl69_ffops_best_ffops_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of consensus FFOPS estimates from contributing analysts |
| 513 | `anl69_ffops_best_ffops_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the consensus FFOPS for the current period |
| 514 | `anl69_ffops_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date representing the fiscal period associated with the “best” consensus FFOPS estimate |
| 515 | `anl69_ffops_best_fperiod_override` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier or code for the “best” consensus fiscal period override, indicating an adjusted or user-specified period rather than standard cal |
| 516 | `anl69_ffops_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date on which the next earnings or financial report is expected to be released |
| 517 | `anl69_ffops_expected_report_period` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The anticipated fiscal period for the forthcoming earnings report, as projected by consensus or company guidance |
| 518 | `anl69_ffops_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled time at which the next earnings report is expected to be released |
| 519 | `anl69_ffops_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The date of the most recent quarterly earnings announcement for the company |
| 520 | `anl69_ffops_market_status` | VECTOR | 0.500 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Indicator or code showing whether the market is open, closed, or in another status at the time of data capture |
| 521 | `anl69_ffops_most_recent_period_end_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | End date of the most recently reported fiscal period relevant to the FFOPS estimate |
| 522 | `anl69_ltgl_dif_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code (e.g., EUR, USD) for the estimates expressed |
| 523 | `anl69_ltgl_dif_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date/identifier for the current fiscal quarter period relevant to the estimate |
| 524 | `anl69_ltgl_dif_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Best estimate of the current semi-annual fiscal period (e.g. H1 2024) |
| 525 | `anl69_ltgl_dif_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date/identifier for the current fiscal year period relevant to the estimate |
| 526 | `anl69_ltgl_dif_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of Earnings Per Share (EPS) for the current fiscal year |
| 527 | `anl69_ltgl_dif_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of Earnings Per Share (EPS) for the next fiscal year |
| 528 | `anl69_ltgl_dif_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date marking the fiscal period associated with the estimate, usually fiscal quarter or year end date |
| 529 | `anl69_ltgl_dif_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 530 | `anl69_ltgl_dif_best_ltg_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the consensus long-term growth (LTG) estimate over the past 4 weeks |
| 531 | `anl69_ltgl_dif_best_ltg_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of LTG estimates that have been revised downward over the past 4 weeks |
| 532 | `anl69_ltgl_dif_best_ltg_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of long-term growth (LTG) estimates that have been revised upward in the last 4 weeks |
| 533 | `anl69_ltgl_dif_best_ltg_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the consensus LTG estimate over a specified period, likely the last 4 weeks |
| 534 | `anl69_ltgl_dif_best_ltg_eps` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus analyst estimate for long-term growth (LTG) in earnings per share (EPS) |
| 535 | `anl69_ltgl_dif_best_ltg_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate for long-term growth (LTG) among contributors |
| 536 | `anl69_ltgl_dif_best_ltg_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest long-term growth (LTG) estimate among analysts |
| 537 | `anl69_ltgl_dif_best_ltg_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median of analyst long-term growth (LTG) estimates |
| 538 | `anl69_ltgl_dif_best_ltg_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analyst estimates contributing to the consensus long-term growth (LTG) estimate |
| 539 | `anl69_ltgl_dif_best_ltg_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst long-term growth (LTG) estimates, showing estimate dispersion |
| 540 | `anl69_ltgl_dif_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date when the company is scheduled or expected to report earnings for the relevant fiscal period |
| 541 | `anl69_ltgl_dif_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The fiscal period for which the earnings report is expected (e.g. Q2 2024) |
| 542 | `anl69_ltgl_dif_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled time for the earnings report for the company |
| 543 | `anl69_ltgl_dif_latest_ann_dt_qtrly` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly announcement for the company |
| 544 | `anl69_ltgl_dif_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Current trading status of the relevant market (e.g. open, closed) |
| 545 | `anl69_ltgl_dif_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recently reported fiscal period |
| 546 | `anl69_nav_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code used for the NAV estimates (e.g., EUR, USD, JPY) |
| 547 | `anl69_nav_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier for the current fiscal quarter period for the entity, as used in the estimate NAV module |
| 548 | `anl69_nav_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier for the current fiscal semi-annual period for the entity, as used in the estimate NAV module |
| 549 | `anl69_nav_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier representing the current fiscal year period for the entity, as used in the estimate NAV module |
| 550 | `anl69_nav_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for Earnings Per Share (EPS) for the current fiscal year, as aggregated by Bloomberg from analyst forecasts |
| 551 | `anl69_nav_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for Earnings Per Share (EPS) for the next fiscal year, as assessed by analysts and aggregated by Bloomberg at the given o |
| 552 | `anl69_nav_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date corresponding to the best (consensus) fiscal period for which the NAV estimate is provided; typically the fiscal period end date |
| 553 | `anl69_nav_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 554 | `anl69_nav_best_nav` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus (best) analyst estimate of Net Asset Value (NAV) for the security for the relevant fiscal period |
| 555 | `anl69_nav_best_nav_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The change in the consensus or best NAV estimate over the past four weeks |
| 556 | `anl69_nav_best_nav_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of NAV consensus estimates revised downwards in the past four weeks |
| 557 | `anl69_nav_best_nav_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of NAV consensus estimates revised upwards in the past four weeks |
| 558 | `anl69_nav_best_nav_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The highest consensus estimate for Net Asset Value (NAV) among contributing analysts for the period, reflecting the top end of the NAV forec |
| 559 | `anl69_nav_best_nav_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The lowest analyst estimate for Net Asset Value (NAV) among those contributing to the consensus |
| 560 | `anl69_nav_best_nav_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of all analyst NAV estimates for the specified period, showing the central tendency of forecasts |
| 561 | `anl69_nav_best_nav_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The number of analyst estimates used to calculate the consensus best NAV estimate |
| 562 | `anl69_nav_best_nav_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The standard deviation of analysts' best NAV estimates, measuring the dispersion or disagreement among analyst forecasts for NAV |
| 563 | `anl69_nav_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled date when the earnings or financial report is expected to be released for the entity |
| 564 | `anl69_nav_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The fiscal period (e.g., year or quarter) that the upcoming expected earnings report will cover |
| 565 | `anl69_nav_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The specific scheduled time when the earnings or financial report is expected to be released for the entity |
| 566 | `anl69_nav_latest_ann_dt_qtrly` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | The most recent announcement or disclosure date for the company’s quarterly financial results as reflected in Bloomberg data |
| 567 | `anl69_nav_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 568 | `anl69_nav_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recently reported financial period |
| 569 | `anl69_ndebt_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The ISO currency code (e.g., USD, CNY) in which the best estimate values are reported |
| 570 | `anl69_ndebt_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current fiscal quarter period being used for net debt estimates |
| 571 | `anl69_ndebt_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current fiscal semi-annual period (such as H1 or H2) used for the net debt consensus estimate |
| 572 | `anl69_ndebt_best_cur_fiscal_year_period` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Year Period Date |
| 573 | `anl69_ndebt_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Best/latest consensus estimate for Earnings Per Share (EPS) for the current fiscal year |
| 574 | `anl69_ndebt_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate of earnings per share (EPS) for the next fiscal year |
| 575 | `anl69_ndebt_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date marking the fiscal period for which the best net debt estimate applies |
| 576 | `anl69_ndebt_best_fperiod_override` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | An override or manually-set value for the fiscal period being used for net debt estimates, typically applied in special circumstances (such  |
| 577 | `anl69_ndebt_best_ndebt_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the consensus estimate of net debt over the past four weeks |
| 578 | `anl69_ndebt_best_ndebt_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst net debt estimates revised downward in the past 4 weeks |
| 579 | `anl69_ndebt_best_ndebt_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of Net Debt estimates that have been revised upward in the past 4 weeks |
| 580 | `anl69_ndebt_best_ndebt_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the consensus net debt estimate over a certain period (likely vs previous estimate) |
| 581 | `anl69_ndebt_best_ndebt_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest net debt estimate among analysts for the relevant period |
| 582 | `anl69_ndebt_best_ndebt_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The lowest net debt estimate among all contributing analyst estimates for the relevant period |
| 583 | `anl69_ndebt_best_ndebt_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The median value among analyst estimates for net debt for the specified period and company |
| 584 | `anl69_ndebt_best_ndebt_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates included in the current consensus Net Debt calculation |
| 585 | `anl69_ndebt_best_ndebt_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation among analyst estimates of net debt, measuring dispersion |
| 586 | `anl69_ndebt_best_net_debt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The best (consensus or most representative) analyst estimate for net debt for the given company and period |
| 587 | `anl69_ndebt_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected date of the next earnings report |
| 588 | `anl69_ndebt_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fiscal period for which the earnings report is expected (e.g., Q1 2023) |
| 589 | `anl69_ndebt_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected time of day when the company's earnings report will be released |
| 590 | `anl69_ndebt_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the most recent quarterly announcement/disclosure for the company related to net debt |
| 591 | `anl69_ndebt_market_status` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Status of the market (e.g., open, closed, post-market) at the time of estimate or report |
| 592 | `anl69_ndebt_most_recent_period_end_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The end date of the most recent period for which the net debt estimate or data is relevant |
| 593 | `anl69_net_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code used for the net income estimate (e.g., USD, EUR) |
| 594 | `anl69_net_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier for the current fiscal quarter period as relevant for the consensus/estimate snapshot |
| 595 | `anl69_net_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier for the current fiscal semi-annual (half-year) period used in estimates |
| 596 | `anl69_net_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier representing the most recent fiscal year period for which consensus or estimate data is calculated |
| 597 | `anl69_net_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate for Earnings Per Share (EPS) for the current fiscal year |
| 598 | `anl69_net_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate for Earnings Per Share (EPS) for the next fiscal year |
| 599 | `anl69_net_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date representing the fiscal period (e.g., quarter-end or year-end) for which the Bloomberg consensus Net Income estimate is calculated |
| 600 | `anl69_net_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 601 | `anl69_net_best_net_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst Net Income estimates revised downward in last 4 weeks |
| 602 | `anl69_net_best_net_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst Net Income estimates revised upward in last 4 weeks |
| 603 | `anl69_net_best_net_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the consensus or "best" estimate of net income compared to a prior period or prior estimate |
| 604 | `anl69_net_best_net_gaap` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate (average/aggregated) for Net Income (GAAP) |
| 605 | `anl69_net_best_net_gaap_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in consensus net income (GAAP) estimate over the past four weeks |
| 606 | `anl69_net_best_net_gaap_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst Net Income (GAAP) estimates revised downward in last 4 weeks |
| 607 | `anl69_net_best_net_gaap_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst Net Income (GAAP) estimates revised upward in last 4 weeks |
| 608 | `anl69_net_best_net_gaap_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The highest analyst estimate for GAAP net income among all contributors for the relevant period |
| 609 | `anl69_net_best_net_gaap_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The lowest analyst estimate for GAAP net income among all contributors for the relevant period |
| 610 | `anl69_net_best_net_gaap_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of analyst estimates for GAAP net income |
| 611 | `anl69_net_best_net_gaap_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the GAAP net income consensus |
| 612 | `anl69_net_best_net_gaap_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for GAAP net income |
| 613 | `anl69_net_best_net_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of analyst estimates for net income, representing the central tendency among contributors |
| 614 | `anl69_net_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled date for the company’s upcoming or most recent earnings report |
| 615 | `anl69_net_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The forecasted or scheduled reporting period for upcoming earnings or financial disclosure for the company |
| 616 | `anl69_net_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected or announced time of day for the next earnings report release |
| 617 | `anl69_net_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the most recent quarterly earnings announcement for the company |
| 618 | `anl69_net_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 619 | `anl69_net_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recently completed fiscal reporting period |
| 620 | `anl69_net_new_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The ISO currency code (e.g., USD, EUR) in which the best consensus net income estimate is denominated |
| 621 | `anl69_net_new_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Quarter Period D |
| 622 | `anl69_net_new_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Semi-Year Period |
| 623 | `anl69_net_new_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier of the current fiscal year period for the estimate, according to consensus |
| 624 | `anl69_net_new_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus best current estimate of earnings per share (EPS) for the current fiscal year |
| 625 | `anl69_net_new_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus best current estimate of earnings per share (EPS) for the next fiscal year |
| 626 | `anl69_net_new_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 627 | `anl69_net_new_best_net_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the consensus net income estimate over the last four weeks |
| 628 | `anl69_net_new_best_net_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst estimate among net income forecasts included in consensus |
| 629 | `anl69_net_new_best_net_income` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus best current estimate of net income for the underlying company or security |
| 630 | `anl69_net_new_best_net_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate for net income (among all contributing analysts) |
| 631 | `anl69_net_new_best_net_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The number of analyst estimates contributing to the best consensus net income figure |
| 632 | `anl69_net_new_best_net_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The standard deviation reflecting the dispersion among analyst net income estimates |
| 633 | `anl69_net_new_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled or forecasted date for the upcoming earnings report |
| 634 | `anl69_net_new_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled time when the earnings report (containing net income) is expected to be released |
| 635 | `anl69_opp_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code in which the estimate is reported (e.g., USD, EUR, JPY) |
| 636 | `anl69_opp_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The current fiscal quarter (like Q1, Q2, Q3, Q4) period for which the consensus OPP estimate is reported |
| 637 | `anl69_opp_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Current semi-annual fiscal period for which "BEST" estimates are provided |
| 638 | `anl69_opp_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The identifier or label of the current fiscal year for which the consensus 'BEst' estimate is provided |
| 639 | `anl69_opp_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimated Earnings Per Share (EPS) for the current fiscal year |
| 640 | `anl69_opp_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus (best estimate) for expected earnings per share (EPS) for the next fiscal year |
| 641 | `anl69_opp_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date representing the fiscal period covered by the current "BEST" estimate metric |
| 642 | `anl69_opp_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 643 | `anl69_opp_best_opp` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus point-in-time operating profit estimate for the specified fiscal period |
| 644 | `anl69_opp_best_opp_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in consensus operating profit estimate over the last four weeks |
| 645 | `anl69_opp_best_opp_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst OPP estimates revised downward in the past four weeks |
| 646 | `anl69_opp_best_opp_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst operating profit estimates revised upward in the last four weeks |
| 647 | `anl69_opp_best_opp_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest operating margin estimate among all contributing analysts for the specified period |
| 648 | `anl69_opp_best_opp_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst estimate for operating profit (OPP) within consensus for the given period |
| 649 | `anl69_opp_best_opp_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The median value of all analyst OPP estimates collected in the consensus window, providing a measure of central tendency less impacted by ou |
| 650 | `anl69_opp_best_opp_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the consensus operating margin figure |
| 651 | `anl69_opp_best_opp_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst operating profit estimates, indicating dispersion/variability |
| 652 | `anl69_opp_best_opp_to_sales` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimated operating margin, defined as operating profit divided by sales, for the period |
| 653 | `anl69_opp_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The anticipated calendar date on which the company's earnings report is expected to be released |
| 654 | `anl69_opp_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The fiscal or reporting period (e.g., quarter or year) for which the upcoming earnings report is scheduled |
| 655 | `anl69_opp_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected time of day at which the company's earnings report is scheduled to be released |
| 656 | `anl69_opp_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly earnings or financial announcement |
| 657 | `anl69_opp_market_status` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Status indicator of the market (open, closed, etc.) when the snapshot or estimate was captured |
| 658 | `anl69_opp_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Calendar date marking the end of the most recently completed fiscal period for the company |
| 659 | `anl69_pe_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code (e.g., USD, EUR, JPY) used for the estimates in this module |
| 660 | `anl69_pe_best_cur_ev_to_ebitda` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus (BEST) estimate of the enterprise value to EBITDA ratio for the security |
| 661 | `anl69_pe_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or code representing the best estimate for the current fiscal quarter period for the company |
| 662 | `anl69_pe_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier for the current fiscal semi-annual period (half-year) used for best (consensus) estimates |
| 663 | `anl69_pe_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date or identifier for the current fiscal year period which the best (consensus or most representative) estimates are based on |
| 664 | `anl69_pe_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate for Earnings Per Share (EPS) for the current fiscal year |
| 665 | `anl69_pe_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate for Earnings Per Share (EPS) for the next fiscal year |
| 666 | `anl69_pe_best_fperiod_override` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Override value for the fiscal period to which the best estimate applies, potentially used if the standard fiscal period is substituted |
| 667 | `anl69_pe_best_pe_ratio` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate for the company's Price-to-Earnings (P/E) Ratio |
| 668 | `anl69_pe_best_px_bps_ratio` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate for the company's Price-to-Book (P/Bk) ratio |
| 669 | `anl69_pe_best_px_cps_ratio` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate for the company's Price-to-Cash Flow (P/CF) ratio |
| 670 | `anl69_pe_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected date when the company's earnings report will be released |
| 671 | `anl69_pe_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected specific time when the company's earnings report will be released |
| 672 | `anl69_ptp_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The ISO three-letter code for the currency in which the best/consensus PTP estimate is expressed (e.g., JPY, USD) |
| 673 | `anl69_ptp_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The quarter identifier (such as Q1, Q2, etc.) for the current fiscal period associated with the best estimates |
| 674 | `anl69_ptp_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Semi-Year Period |
| 675 | `anl69_ptp_best_cur_fiscal_year_period` | MATRIX | 0.500 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Year Period Date |
| 676 | `anl69_ptp_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of earnings per share (EPS) for the current fiscal year |
| 677 | `anl69_ptp_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of earnings per share (EPS) for the company for the next fiscal year |
| 678 | `anl69_ptp_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date marking the fiscal period (such as quarter, semi-year, or year) for which the estimates are considered 'best' or consensus accordin |
| 679 | `anl69_ptp_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 680 | `anl69_ptp_best_ptp` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus Point-in-Time Price Target estimate, representing the aggregate price target forecast for the security |
| 681 | `anl69_ptp_best_ptp_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in consensus Profit Before Tax (PTP) estimate over the past 4 weeks |
| 682 | `anl69_ptp_best_ptp_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates for pre-tax profit (PTP) that have been revised downward over the past four weeks |
| 683 | `anl69_ptp_best_ptp_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst pre-tax profit (PTP) estimates revised up in the last 4 weeks |
| 684 | `anl69_ptp_best_ptp_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst consensus estimate for Pre-Tax Profit (PTP) for the specified period |
| 685 | `anl69_ptp_best_ptp_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst consensus estimate for Pre-Tax Profit (PTP) for the specified period |
| 686 | `anl69_ptp_best_ptp_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median analyst estimate of pre-tax profit margin for the current period |
| 687 | `anl69_ptp_best_ptp_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The number of analyst estimates contributing to the consensus PTP figure for the observation period |
| 688 | `anl69_ptp_best_ptp_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst estimates for pre-tax profit margin, indicating dispersion |
| 689 | `anl69_ptp_best_ptp_to_sales` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of pre-tax margin, i.e., Pre-Tax Profit (PTP) divided by Sales/Revenue |
| 690 | `anl69_ptp_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date on which the company is expected to report earnings for the relevant period |
| 691 | `anl69_ptp_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The anticipated fiscal period for which the company's earnings report is expected to be released (e.g., Q1 2024, FY2024) |
| 692 | `anl69_ptp_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The scheduled or anticipated time for the company's upcoming earnings report |
| 693 | `anl69_ptp_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly announcement (e.g., earnings release) for the company |
| 694 | `anl69_ptp_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 695 | `anl69_ptp_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recently reported fiscal period |
| 696 | `anl69_rec_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code in which the estimates are denominated (e.g., USD, CNY) |
| 697 | `anl69_rec_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Best estimate of the current fiscal quarter period or end date for the company, as used for financial consensus and estimates |
| 698 | `anl69_rec_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Best estimate of the current fiscal semi-annual (half-year) period or end date for the company, as used for financial consensus and estimate |
| 699 | `anl69_rec_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Best estimate of the current fiscal year period or end date for the company, as used for financial consensus and estimates |
| 700 | `anl69_rec_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of earnings per share (EPS) for the current fiscal year, based on analyst projections |
| 701 | `anl69_rec_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of earnings per share (EPS) for the next fiscal year, based on analyst projections |
| 702 | `anl69_rec_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The end date of the fiscal period corresponding to the best (consensus) estimate |
| 703 | `anl69_rec_best_fperiod_override` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Alternative or manually overridden fiscal period identifier for the company, potentially used to correct or align periods in estimate data |
| 704 | `anl69_rec_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date when the next earnings report for the company is expected to be published |
| 705 | `anl69_rec_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected fiscal period (such as quarter or year) for which an earnings report is anticipated to be released |
| 706 | `anl69_rec_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected time of day when the company's earnings or financial report is scheduled for release |
| 707 | `anl69_rec_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The date of the most recent quarterly earnings or financial announcement for the company |
| 708 | `anl69_rec_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 709 | `anl69_rec_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recent reporting period for the company |
| 710 | `anl69_rec_tot_analyst_rec` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analyst recommendations or ratings currently available for the company's security |
| 711 | `anl69_rec_tot_buy_rec` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analysts giving a "Buy" recommendation for the security |
| 712 | `anl69_rec_tot_hold_rec` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analysts giving a "Hold" recommendation for the security |
| 713 | `anl69_rec_tot_sell_rec` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Total number of analysts who issued a 'Sell' recommendation for the security |
| 714 | `anl69_roa_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code in which the ROA estimate is denominated (e.g., USD, EUR) |
| 715 | `anl69_roa_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier or date for the current fiscal quarter covered by the ROA consensus estimate |
| 716 | `anl69_roa_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier or date range for the current semi-annual (half-year) fiscal period relevant to the ROA estimate |
| 717 | `anl69_roa_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Identifier or date range for the current fiscal year relevant to the ROA consensus estimate |
| 718 | `anl69_roa_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Best consensus estimate of Earnings Per Share (EPS) for the current fiscal year |
| 719 | `anl69_roa_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Best consensus estimate of Earnings Per Share (EPS) for the next fiscal year |
| 720 | `anl69_roa_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Calendar date corresponding to the fiscal period for which the ROA consensus estimate is calculated |
| 721 | `anl69_roa_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 722 | `anl69_roa_best_roa` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus analyst estimate of Return on Assets (ROA) for the given period |
| 723 | `anl69_roa_best_roa_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The change in consensus ROA estimate over the past 4 weeks |
| 724 | `anl69_roa_best_roa_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of ROA (Return on Assets) analyst estimates revised downward in the last 4 weeks |
| 725 | `anl69_roa_best_roa_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of ROA (Return on Assets) analyst estimates revised upward in the last 4 weeks |
| 726 | `anl69_roa_best_roa_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The percentage change in the consensus ROA estimate over the specified period, typically reflecting short-term momentum or revision dynamics |
| 727 | `anl69_roa_best_roa_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The highest analyst forecast for ROA among all estimates, representing the upper bound of consensus dispersion |
| 728 | `anl69_roa_best_roa_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst ROA estimate for the period (the lower bound of consensus) |
| 729 | `anl69_roa_best_roa_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of analyst ROA estimates for the consensus period |
| 730 | `anl69_roa_best_roa_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The total number of analyst estimates contributing to the consensus ROA figure for the specified period |
| 731 | `anl69_roa_best_roa_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of ROA estimates, showing dispersion among contributing analysts |
| 732 | `anl69_roa_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected date for the next earnings report for the company |
| 733 | `anl69_roa_expected_report_period` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Expected reporting period for earnings that the ROA estimate pertains to |
| 734 | `anl69_roa_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected time of day the earnings report will be released |
| 735 | `anl69_roa_latest_ann_dt_qtrly` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly announcement or data release relevant to the ROA estimate |
| 736 | `anl69_roa_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 737 | `anl69_roa_most_recent_period_end_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The end date of the most recently reported fiscal period covered by the Return on Assets (ROA) estimates |
| 738 | `anl69_roel_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code (e.g., JPY, USD) used for the best ROE estimate |
| 739 | `anl69_roel_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier representing the current fiscal quarter period for which consensus ROE estimates are provided |
| 740 | `anl69_roel_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Semi-Year Period |
| 741 | `anl69_roel_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier representing the current fiscal year period for which consensus ROE estimates are provided |
| 742 | `anl69_roel_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for earnings per share (EPS) for the current fiscal year |
| 743 | `anl69_roel_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate for earnings per share (EPS) for the next fiscal year |
| 744 | `anl69_roel_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The fiscal period end date relating to the consensus ROE estimate for the equity in Asia |
| 745 | `anl69_roel_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 746 | `anl69_roel_best_roe` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus or best estimate for Return on Equity (ROE) for the relevant period |
| 747 | `anl69_roel_best_roe_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the consensus ROE estimate over the past 4 weeks |
| 748 | `anl69_roel_best_roe_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst ROE estimates that have been revised downward in the past four weeks for the specified equity |
| 749 | `anl69_roel_best_roe_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst ROE estimates that have been revised upward in the past four weeks for the specified equity |
| 750 | `anl69_roel_best_roe_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in consensus ROE estimate over a specified period (likely the past four weeks) for the Asia-region equity |
| 751 | `anl69_roel_best_roe_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The highest value among analyst ROE estimates, representing the maximum forecast within the consensus |
| 752 | `anl69_roel_best_roe_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The lowest analyst estimate for return on equity (ROE) among all collected estimates for the relevant period |
| 753 | `anl69_roel_best_roe_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The median value among analyst estimates for the Return on Equity (ROE) consensus for a specified period |
| 754 | `anl69_roel_best_roe_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The number of analyst estimates that are included in calculating the consensus (BEST) ROE |
| 755 | `anl69_roel_best_roe_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The standard deviation of all analyst estimates included in the consensus ROE, a measure of dispersion or analyst disagreement |
| 756 | `anl69_roel_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled date when the company is expected to report earnings or financial results |
| 757 | `anl69_roel_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected reporting period for upcoming earnings or financial disclosure associated with the equity's ROE in Asia |
| 758 | `anl69_roel_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled time when the company is expected to report earnings or financial results |
| 759 | `anl69_roel_latest_ann_dt_qtrly` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The date of the most recent quarterly announcement relevant to the consensus ROE estimate |
| 760 | `anl69_roel_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Current market trading status indicator, such as open, closed, halted |
| 761 | `anl69_roel_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Date marking the end of the most recently reported fiscal period |
| 762 | `anl69_salesl_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code for the sales estimate values (e.g. USD, JPY) |
| 763 | `anl69_salesl_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Quarter Period D |
| 764 | `anl69_salesl_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Semi-Year Period |
| 765 | `anl69_salesl_best_cur_fiscal_year_period` | MATRIX | 0.500 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | BEst Current Fiscal Year Period Date |
| 766 | `anl69_salesl_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus "best" estimate for earnings per share (EPS) for the current year |
| 767 | `anl69_salesl_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimate of earnings per share (EPS) for the next fiscal year |
| 768 | `anl69_salesl_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date representing the fiscal period for which the sales estimate applies |
| 769 | `anl69_salesl_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 770 | `anl69_salesl_best_ni_adj_to_sales` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus profit margin for the period, calculated as adjusted net income to sales |
| 771 | `anl69_salesl_best_sales` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus "best" estimate of sales for the relevant period |
| 772 | `anl69_salesl_best_sales_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the best (consensus) sales estimate over the past 4 weeks |
| 773 | `anl69_salesl_best_sales_4wk_dn` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst sales estimates revised downward in the past 4 weeks |
| 774 | `anl69_salesl_best_sales_4wk_up` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst sales estimates revised upward in the last 4 weeks |
| 775 | `anl69_salesl_best_sales_chg_pct` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Percentage change in the consensus sales estimate over the specified period |
| 776 | `anl69_salesl_best_sales_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest analyst sales estimate among all contributing analysts for the period |
| 777 | `anl69_salesl_best_sales_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest analyst sales estimate (consensus low) for the specific period |
| 778 | `anl69_salesl_best_sales_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of all analyst sales estimates for the period |
| 779 | `anl69_salesl_best_sales_numest` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Number of analyst estimates contributing to the best sales consensus for the period |
| 780 | `anl69_salesl_best_sales_stddev` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Standard deviation of analyst sales estimates, indicating dispersion for the specific period |
| 781 | `anl69_salesl_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled date when the company's earnings or sales report is expected to be released |
| 782 | `anl69_salesl_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Scheduled or anticipated reporting period for the company's upcoming earnings report |
| 783 | `anl69_salesl_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expected time of the upcoming earnings (sales-related) report |
| 784 | `anl69_salesl_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the most recent quarterly earnings announcement |
| 785 | `anl69_salesl_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 786 | `anl69_salesl_most_recent_period_end_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date marking the end of the most recent financial or reporting period for which sales estimates are referenced |
| 787 | `anl69_target_best_crncy_iso` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | ISO currency code in which the estimates or target prices are denominated, such as JPY or USD |
| 788 | `anl69_target_best_cur_fiscal_qtr_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Represents the identifier for the company's current best-estimate fiscal quarter (e.g., Q1, Q2, Q3, Q4), based on the latest available data |
| 789 | `anl69_target_best_cur_fiscal_semi_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier for the current fiscal semi-year (half-year) period as used in estimates |
| 790 | `anl69_target_best_cur_fiscal_year_period` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date or identifier for the current fiscal year period as used in estimates |
| 791 | `anl69_target_best_eeps_cur_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus estimated earnings per share (EPS) for the current fiscal year |
| 792 | `anl69_target_best_eeps_nxt_yr` | MATRIX | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | The consensus estimated earnings per share (EPS) for the next fiscal year |
| 793 | `anl69_target_best_fiscal_period_dt` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Date corresponding to the fiscal period relevant to the current estimates |
| 794 | `anl69_target_best_fperiod_override` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | BEst Fiscal Period Override |
| 795 | `anl69_target_best_target_4wk_chg` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Change in the consensus target price over the past 4 weeks |
| 796 | `anl69_target_best_target_hi` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Highest target price among analysts as of the observation date |
| 797 | `anl69_target_best_target_lo` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Lowest target price estimate provided by analysts |
| 798 | `anl69_target_best_target_median` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Median value of target price estimates among analysts |
| 799 | `anl69_target_best_target_price` | VECTOR | 0.500 | 修正与预期 | 0 | — | — | — | UNUSABLE | Consensus best estimate for target price as provided by analysts |
| 800 | `anl69_target_expected_report_dt` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected calendar date when the company's earnings report will be released |
| 801 | `anl69_target_expected_report_period` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fiscal period for which the next earnings report is expected (e.g., Q1 2024) |
| 802 | `anl69_target_expected_report_time` | MATRIX | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The expected time of day (e.g., before market open, after market close) when the upcoming earnings report will be released |
| 803 | `anl69_target_latest_ann_dt_qtrly` | VECTOR | 0.500 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Date of the latest quarterly earnings or financial announcement |
| 804 | `anl69_target_market_status` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | Market Status |
| 805 | `anl69_target_most_recent_period_end_dt` | VECTOR | 0.500 | 其他 | 0 | — | — | — | UNUSABLE | End date of the most recent financial reporting period for the company |
| 806 | `anl69_best_ltg_stddev` | VECTOR | 0.398 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Long Term Growth Rate Std Dev |
| 807 | `anl69_best_ffops` | VECTOR | 0.361 | 其他 | 0 | — | — | — | UNUSABLE | FFO Per Share |
| 808 | `anl69_best_ffops_hi` | VECTOR | 0.361 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funds from Operations per share High |
| 809 | `anl69_best_ffops_lo` | VECTOR | 0.361 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funds from Operations per share Low |
| 810 | `anl69_best_ffops_4wk_chg` | VECTOR | 0.356 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funds from Operations per share 4 wk Chg |
| 811 | `anl69_best_ffops_median` | VECTOR | 0.355 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funds from Operations per share Median |
| 812 | `anl69_best_ffops_chg_pct` | VECTOR | 0.342 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Funds from Operations per share % Chg |
| 813 | `anl69_cest_sales` | VECTOR | 0.263 | 其他 | 0 | — | — | — | UNUSABLE | Sales |

## 六、本地回测证据

- 本地累计回测 **20** 条；其中 `ra_failed_checks` 为空的 **20** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `Grgoopa5` | 0.94 | 0.48 | -0.31 | 0.34 | 0.04 | 0 | w609 | `group_rank(ts_mean(ts_backfill(vec_avg(anl69_best_eps_4wk_chg), 22), 66), sector)` |
| `j2eggOMQ` | 0.92 | 0.25 | -0.40 | 0.34 | 0.36 | 0 | w612 | `signed_power(group_rank(divide(vec_avg(anl69_best_eps_chg_pct), ts_mean(divide(vec_avg(anl` |
| `npAWWM9l` | 0.87 | 0.42 | 0.86 | 0.54 | 0.19 | 0 | w609 | `subtract(0, group_rank(divide(vec_avg(anl69_best_eps_stddev), abs(vec_avg(anl69_best_eps_m` |
| `78oddEA8` | 0.77 | 0.39 | 0.44 | 0.59 | 0.16 | 0 | w609 | `subtract(0, group_rank(divide(vec_avg(anl69_best_net_gaap_stddev), abs(vec_avg(anl69_best_` |
| `XgRKK5rz` | 0.70 | 0.21 | -0.14 | 0.49 | 0.29 | 0 | w609 | `group_rank(subtract(vec_avg(anl69_best_eps_4wk_up), vec_avg(anl69_best_eps_4wk_dn)), secto` |
| `WjLgg6MP` | 0.69 | 0.28 | 0.71 | 0.65 | 0.19 | 0 | w609 | `subtract(0, group_rank(divide(vec_avg(anl69_best_sales_stddev), abs(vec_avg(anl69_best_sal` |
| `LL5RR32m` | 0.64 | 0.21 | -0.01 | 0.19 | 0.21 | 0 | w612 | `group_rank(divide(ts_backfill(vec_avg(anl69_best_ebitda_chg_pct), 22), ts_mean(divide(vec_` |
| `KPmLLj0E` | 0.57 | 0.25 | -0.69 | 0.52 | 0.04 | 0 | w609 | `group_rank(ts_mean(ts_backfill(vec_avg(anl69_best_target_4wk_chg), 22), 66), sector)` |
| `0mj880lr` | 0.56 | 0.29 | 0.44 | 0.40 | 0.13 | 0 | w609 | `subtract(0, group_rank(divide(subtract(vec_avg(anl69_best_target_hi), vec_avg(anl69_best_t` |
| `pwv773pX` | 0.53 | 0.18 | -0.31 | 0.24 | 0.16 | 0 | w612 | `group_rank(divide(ts_backfill(vec_avg(anl69_best_eps_4wk_chg), 22), ts_mean(divide(vec_avg` |
| `LL5RR321` | 0.46 | 0.15 | -0.48 | 0.42 | 0.15 | 0 | w612 | `group_rank(divide(ts_backfill(vec_avg(anl69_best_eps_gaap_4wk_chg), 22), ts_mean(divide(ve` |
| `9qERRk22` | 0.44 | 0.12 | -0.30 | 0.58 | 0.22 | 0 | w612 | `group_rank(divide(vec_avg(anl69_best_target_4wk_chg), divide(subtract(vec_avg(anl69_best_t` |
| `88vLLXXV` | 0.42 | 0.11 | -0.35 | 0.08 | 0.21 | 0 | w612 | `group_rank(divide(ts_backfill(vec_avg(anl69_best_net_chg_pct), 22), ts_mean(divide(vec_avg` |
| `E5VKKxxK` | 0.39 | 0.09 | -0.63 | 0.04 | 0.23 | 0 | w612 | `group_rank(divide(ts_backfill(vec_avg(anl69_best_eps_chg_pct), 22), ts_mean(divide(vec_avg` |
| `0mj88552` | 0.37 | 0.09 | -0.21 | 0.17 | 0.21 | 0 | w612 | `group_rank(divide(ts_backfill(vec_avg(anl69_best_sales_chg_pct), 22), ts_mean(divide(vec_a` |

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

