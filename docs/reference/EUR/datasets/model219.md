# model219 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model219` |
| 名称 | — |
| 类别 | MODEL |
| 数据字段数(平台) | 1675 |
| 覆盖率 | 0.9203 |
| 平台已有 alpha | 2828 |
| valueScore | 4 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

（平台目录未返回描述）

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **1675** |
| 类型分布 | MATRIX×1675 |
| 平均覆盖率 | **0.920** |
| 覆盖率区间 | 0.48 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 1257 | 75.0% |
| 中 (0.70–0.90) | 365 | 21.8% |
| 低 (0.50–0.70) | 52 | 3.1% |
| 稀疏 (<0.50) | 1 | 0.1% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 1668 | 99.6% |
| UNUSABLE | 7 | 0.4% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 1668 / UNUSABLE 7 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 855 | 0.92 | mdl219_q_glb_dlr_1_acqmul、mdl219_q_glb_dlr_1_aqi、mdl219_q_glb_dlr_1_aspanratio |
| 价量与波动 | 362 | 0.93 | mdl219_q_glb_dlr_1_actrtn12m、mdl219_q_glb_dlr_1_actrtn18m、mdl219_q_glb_dlr_1_actrtn1m |
| 其他 | 288 | 0.91 | mdl219_q_glb_dlr_1_aci、mdl219_q_glb_dlr_1_acp、mdl219_q_glb_dlr_1_capexsale |
| 修正与预期 | 104 | 0.93 | mdl219_q_glb_dlr_1_chg6mltg、mdl219_q_glb_dlr_1_fc_cvfy1eps、mdl219_q_glb_dlr_1_fc_cvfy2eps |
| 宏观与行业 | 41 | 0.92 | mdl219_q_glb_dlr_1_bdi、mdl219_q_glb_dlr_1_cg3ysales、mdl219_q_glb_dlr_1_epschgetr |
| 风险与质量 | 14 | 0.90 | mdl219_q_glb_dlr_1_beta、drawdown_one_month_standard_deviation、high_sensitivity_score |
| 搜索与替代数据 | 8 | 0.84 | mdl219_q_glb_dlr_1_app、mdl219_q_glb_dlr_1_rdsale、mdl219_q_glb_dlr_2_app |
| 持仓与资金流 | 3 | 0.91 | intellectual_property_indicator、trailing_weighted_cash_position、cash_to_sales_ratio_6 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl219_q_glb_dlr_1_aci` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Abnormal capital investment measuring changes in capital expenditure intensity. |
| 2 | `mdl219_q_glb_dlr_1_acp` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Average collection period calculated as accounts receivable times 365 divided by sales. |
| 3 | `mdl219_q_glb_dlr_1_acqmul` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Acquisition multiple calculated as invested capital divided by EBITDA. |
| 4 | `mdl219_q_glb_dlr_1_actrtn12m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual 12-month total return |
| 5 | `mdl219_q_glb_dlr_1_actrtn18m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual stock return over 18 months, percent |
| 6 | `mdl219_q_glb_dlr_1_actrtn1m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 1 month; percent |
| 7 | `mdl219_q_glb_dlr_1_actrtn24m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 24 months; percent |
| 8 | `mdl219_q_glb_dlr_1_actrtn2m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over the past 2 months |
| 9 | `mdl219_q_glb_dlr_1_actrtn36m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 36 months; percent |
| 10 | `mdl219_q_glb_dlr_1_actrtn3m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 3 months |
| 11 | `mdl219_q_glb_dlr_1_actrtn60m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over the past 60 months |
| 12 | `mdl219_q_glb_dlr_1_actrtn6m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 6 months |
| 13 | `mdl219_q_glb_dlr_1_actrtn9m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 9-month active return representing the percent change in stock price. |
| 14 | `mdl219_q_glb_dlr_1_alpha60m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month alpha calculated as the intercept of a regression of stock returns against a benchmark. |
| 15 | `mdl219_q_glb_dlr_1_app` | MATRIX | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Average payable period calculated as accounts payable times 365 divided by cost of goods sold. |
| 16 | `mdl219_q_glb_dlr_1_aqi` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset quality index measuring changes in the ratio of non-current assets to total assets. |
| 17 | `mdl219_q_glb_dlr_1_aspanratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Attention span ratio measuring operating assets minus liabilities scaled by total assets. |
| 18 | `mdl219_q_glb_dlr_1_astcomp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset composition ratio representing current assets divided by total assets. |
| 19 | `mdl219_q_glb_dlr_1_astto` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset turnover ratio (sales divided by total assets) |
| 20 | `mdl219_q_glb_dlr_1_bdi` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Baltic Dry Index (shipping/freight cost proxy); macro indicator |
| 21 | `mdl219_q_glb_dlr_1_beta` | MATRIX | 1.000 | 风险与质量 | 0 | — | — | — | UNTESTED | Beta coefficient measuring systematic risk relative to the market |
| 22 | `mdl219_q_glb_dlr_1_betasigma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Product of beta and return volatility (sigma) |
| 23 | `mdl219_q_glb_dlr_1_booklev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book leverage calculated as total assets divided by book equity. |
| 24 | `mdl219_q_glb_dlr_1_bp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Book‑to‑Price ratio (inverse of P/B) |
| 25 | `mdl219_q_glb_dlr_1_capacq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital acquisition ratio measuring operating cash flow less dividends divided by expenditures. |
| 26 | `mdl219_q_glb_dlr_1_capexast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital expenditure-to-assets ratio measuring investment intensity. |
| 27 | `mdl219_q_glb_dlr_1_capexsale` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Capital expenditures divided by sales (CapEx-to-sales ratio) |
| 28 | `mdl219_q_glb_dlr_1_cashburnrate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash burn rate calculated as negative operating and investment cash flows divided by cash holdings. |
| 29 | `mdl219_q_glb_dlr_1_cashc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Cash cycle calculated as inventory days plus collection days minus payable days. |
| 30 | `mdl219_q_glb_dlr_1_cashp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Cash-to-price ratio calculated as cash per share divided by stock price. |
| 31 | `mdl219_q_glb_dlr_1_cashratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash-to-current liabilities ratio measuring liquidity. |
| 32 | `mdl219_q_glb_dlr_1_cashratiofixed` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash ratio calculated as cash and equivalents divided by current liabilities. |
| 33 | `mdl219_q_glb_dlr_1_cashsale` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-sales ratio calculated as average cash divided by sales. |
| 34 | `mdl219_q_glb_dlr_1_cashsev` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-enterprise value ratio representing total cash divided by enterprise value. |
| 35 | `mdl219_q_glb_dlr_1_ccd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current cash flow debt coverage ratio measuring cash flow relative to debt. |
| 36 | `mdl219_q_glb_dlr_1_cfita` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow from investment-to-assets ratio calculated over trailing 12 months. |
| 37 | `mdl219_q_glb_dlr_1_cfleverage` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow leverage calculated as total liabilities divided by operating cash flow. |
| 38 | `mdl219_q_glb_dlr_1_cfroi` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow return on invested capital calculated over trailing 12 months. |
| 39 | `mdl219_q_glb_dlr_1_cg3ysales` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | 3-year compound annual growth rate of sales. |
| 40 | `mdl219_q_glb_dlr_1_chg3ycfast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in cash flow from assets scaled by total assets. |
| 41 | `mdl219_q_glb_dlr_1_chg3ycfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow per share scaled by price. |
| 42 | `mdl219_q_glb_dlr_1_chg3yepsast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in EPS scaled by total assets. |
| 43 | `mdl219_q_glb_dlr_1_chg3yepsp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-year change in EPS scaled by price. |
| 44 | `mdl219_q_glb_dlr_1_chg3yfcfast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow scaled by total assets. |
| 45 | `mdl219_q_glb_dlr_1_chg3yfcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow per share scaled by price. |
| 46 | `mdl219_q_glb_dlr_1_chg3yocfast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in operating cash flow scaled by total assets. |
| 47 | `mdl219_q_glb_dlr_1_chg3yocfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in operating cash flow per share scaled by price. |
| 48 | `mdl219_q_glb_dlr_1_chg6malpha18m` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 18-month alpha. |
| 49 | `mdl219_q_glb_dlr_1_chg6mltg` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month change in long-term growth estimates. |
| 50 | `mdl219_q_glb_dlr_1_chgalpha12m` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 12-month alpha. |
| 51 | `mdl219_q_glb_dlr_1_chgalpha36m` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 36-month alpha. |
| 52 | `mdl219_q_glb_dlr_1_chgars` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in accounts receivable as a percentage of sales. |
| 53 | `mdl219_q_glb_dlr_1_chgcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow scaled by total assets. |
| 54 | `mdl219_q_glb_dlr_1_chgcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow per share scaled by price. |
| 55 | `mdl219_q_glb_dlr_1_chgeps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in EPS scaled by total assets. |
| 56 | `mdl219_q_glb_dlr_1_chgepsp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in TTM EPS versus four quarters ago, scaled by price |
| 57 | `mdl219_q_glb_dlr_1_chgfcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow scaled by total assets. |
| 58 | `mdl219_q_glb_dlr_1_chgfcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow per share scaled by price. |
| 59 | `mdl219_q_glb_dlr_1_chgis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in inventory as a percentage of sales. |
| 60 | `mdl219_q_glb_dlr_1_chgnoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net operating assets scaled by total assets. |
| 61 | `mdl219_q_glb_dlr_1_chgnpm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net profit margin over the recent period |
| 62 | `mdl219_q_glb_dlr_1_chgocf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating cash flow scaled by total assets. |
| 63 | `mdl219_q_glb_dlr_1_chgocfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating cash flow per share scaled by price. |
| 64 | `mdl219_q_glb_dlr_1_chgollev` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in operating leverage; period‑over‑period change |
| 65 | `mdl219_q_glb_dlr_1_chgopm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating profit margin over the last four quarters |
| 66 | `mdl219_q_glb_dlr_1_chgreccast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accounts receivable relative to current assets. |
| 67 | `mdl219_q_glb_dlr_1_chgsgasale` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in SG&A expenses relative to sales over the last year. |
| 68 | `mdl219_q_glb_dlr_1_chgshare` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Percent change in shares outstanding over the last year. |
| 69 | `mdl219_q_glb_dlr_1_chgvolpre4y` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-year change in average trading volume. |
| 70 | `mdl219_q_glb_dlr_1_cogsinvt` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in cost of goods sold relative to inventory levels. |
| 71 | `mdl219_q_glb_dlr_1_covol` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month trading volume trend. |
| 72 | `mdl219_q_glb_dlr_1_curindbp_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative book-to-price ratio adjusted for industry averages. |
| 73 | `mdl219_q_glb_dlr_1_curindcfp_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative cash flow-to-price ratio adjusted for industry averages. |
| 74 | `mdl219_q_glb_dlr_1_curinddivp_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative dividend yield adjusted for industry averages. |
| 75 | `mdl219_q_glb_dlr_1_curindebitdap_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock’s EBITDA-to-price ratio minus its industry average (industry-relative EBITDA/P) |
| 76 | `mdl219_q_glb_dlr_1_curindep_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative EPS-to-price ratio adjusted for industry averages. |
| 77 | `mdl219_q_glb_dlr_1_curindfcfp_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock’s trailing 12‑month free cash flow to price minus its industry average; industry‑relative FCF/P |
| 78 | `mdl219_q_glb_dlr_1_curindocfp_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock’s trailing 12-month operating cash flow to price minus industry average |
| 79 | `mdl219_q_glb_dlr_1_curindocfta_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock’s trailing 12‑month operating cash flow to total assets minus industry average; industry‑relative OCFTA |
| 80 | `mdl219_q_glb_dlr_1_curindsp_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative sales-to-price ratio adjusted for industry averages. |
| 81 | `mdl219_q_glb_dlr_1_curratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current ratio calculated as current assets divided by current liabilities. |
| 82 | `mdl219_q_glb_dlr_1_cvpre90dp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient of variation of prior 90-day closing prices. |
| 83 | `mdl219_q_glb_dlr_1_cvvolp20d` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 20-day volume volatility relative to price volatility |
| 84 | `mdl219_q_glb_dlr_1_de` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Debt-to-Equity ratio |
| 85 | `mdl219_q_glb_dlr_1_debtcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt-to-cash flow ratio calculated over trailing 12 months. |
| 86 | `mdl219_q_glb_dlr_1_dfl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Financial leverage calculated as pretax income plus interest expense divided by pretax income. |
| 87 | `mdl219_q_glb_dlr_1_div5yg` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year dividend growth rate; percent |
| 88 | `mdl219_q_glb_dlr_1_divcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends-to-cash flow ratio calculated over trailing 12 months. |
| 89 | `mdl219_q_glb_dlr_1_divcov` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend coverage ratio (ability to cover dividends from income) |
| 90 | `mdl219_q_glb_dlr_1_divyield` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend yield (TTM dividends per share divided by price) |
| 91 | `mdl219_q_glb_dlr_1_dpcapex` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in depreciation relative to capital expenditures over the last year. |
| 92 | `mdl219_q_glb_dlr_1_ebitdaev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA to Enterprise Value ratio; valuation metric; higher indicates cheaper valuation |
| 93 | `mdl219_q_glb_dlr_1_ebitdap` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month EBITDA-to-price ratio used for valuation. |
| 94 | `mdl219_q_glb_dlr_1_epschgetr` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | EPS change due to changes in effective tax rate over the last year. |
| 95 | `mdl219_q_glb_dlr_1_equityto` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity turnover ratio calculated as sales divided by average book equity. |
| 96 | `mdl219_q_glb_dlr_1_fc_curindfwdep_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward earnings-to-price ratio relative to industry (stock’s next 4-quarter EPS forecast divided by price minus industry average) |
| 97 | `mdl219_q_glb_dlr_1_fc_cvfy1eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Dispersion of FY1 EPS estimates calculated as standard deviation divided by mean. |
| 98 | `mdl219_q_glb_dlr_1_fc_cvfy2eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Coefficient of variation of FY2 EPS estimates; standard deviation divided by mean forecast |
| 99 | `mdl219_q_glb_dlr_1_fc_dypeg` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of dividend yield-adjusted PEG ratio. |
| 100 | `mdl219_q_glb_dlr_1_fc_ebop` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Edwards-Bell-Ohlson value-to-price ratio based on valuation models. |
| 101 | `mdl219_q_glb_dlr_1_fc_egp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow to Equity (FCFE) ratio, current period |
| 102 | `mdl219_q_glb_dlr_1_fc_epsrm` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision magnitude measuring 3-month change in median earnings forecast. |
| 103 | `mdl219_q_glb_dlr_1_fc_estep` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leading 12-month median earnings yield calculated as forward EPS divided by price. |
| 104 | `mdl219_q_glb_dlr_1_fc_f12mepssev` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward EPS-to-enterprise value ratio based on consensus estimates. |
| 105 | `mdl219_q_glb_dlr_1_fc_fcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward free cash flow to price ratio (forecasted FCF divided by market capitalization) |
| 106 | `mdl219_q_glb_dlr_1_fc_fcfroey1p` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward (FY1) free cash flow to price; forecasted next‑year FCF divided by current market cap |
| 107 | `mdl219_q_glb_dlr_1_fc_fwdep` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward earnings yield based on consensus estimates divided by price. |
| 108 | `mdl219_q_glb_dlr_1_fc_fwdroe` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecasted (forward) return on equity based on analyst/Model estimates |
| 109 | `mdl219_q_glb_dlr_1_fc_hlep` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision confidence measuring the sum of 3-month changes in highest and lowest earnings forecasts. |
| 110 | `mdl219_q_glb_dlr_1_fc_numest` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of FY1 earnings estimates in the analyst consensus |
| 111 | `mdl219_q_glb_dlr_1_fc_numrevy1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Net number of FY1 analyst forecast revisions (raised minus lowered) within a month. |
| 112 | `mdl219_q_glb_dlr_1_fc_pdy` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted dividend yield based on payout ratio and forward EPS estimates. |
| 113 | `mdl219_q_glb_dlr_1_fc_rel5yfwdep` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative forward 12-month EPS-to-price ratio compared to historical averages. |
| 114 | `mdl219_q_glb_dlr_1_fc_rev3y1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY1 EPS forecasts scaled by price. |
| 115 | `mdl219_q_glb_dlr_1_fc_rev3y2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY2 EPS forecasts scaled by price. |
| 116 | `mdl219_q_glb_dlr_1_fc_rev6` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Average of prior 6-month changes in FY1 consensus earnings forecasts. |
| 117 | `mdl219_q_glb_dlr_1_fc_stdevfy1epsp` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY1 EPS estimates scaled by price. |
| 118 | `mdl219_q_glb_dlr_1_fc_stdevfy2epsp` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY2 EPS estimates scaled by price. |
| 119 | `mdl219_q_glb_dlr_1_fc_y2aepsg` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 2-year projected EPS growth based on analyst forecasts. |
| 120 | `mdl219_q_glb_dlr_1_fcfequity` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow to Equity |
| 121 | `mdl219_q_glb_dlr_1_fcfroi` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow return on invested capital calculated over trailing 12 months. |
| 122 | `mdl219_q_glb_dlr_1_fcfsale` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow to sales; percent |
| 123 | `mdl219_q_glb_dlr_1_ff10mrtn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Fama-French momentum factor measuring percent change in stock price over 12 months excluding the most recent month. |
| 124 | `mdl219_q_glb_dlr_1_fixastto` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fixed asset turnover ratio calculated as sales divided by fixed assets. |
| 125 | `mdl219_q_glb_dlr_1_flowratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flow ratio measuring liquidity as current assets minus cash divided by liabilities minus debt. |
| 126 | `mdl219_q_glb_dlr_1_gear` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital gearing ratio calculated as long-term debt divided by total assets minus current liabilities. |
| 127 | `mdl219_q_glb_dlr_1_high52w` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest stock price over the past 52 weeks |
| 128 | `mdl219_q_glb_dlr_1_indrelcroe_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-adjusted quarterly return on equity relative to industry averages. |
| 129 | `mdl219_q_glb_dlr_1_indrelrecd_` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-relative recapitalization degree; deviation from industry median/mean (standardized) |
| 130 | `mdl219_q_glb_dlr_1_indrelrtn4w_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative 4-week return; performance versus industry baseline |
| 131 | `mdl219_q_glb_dlr_1_indrelrtn5d_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock’s return over the last 5 days relative to its industry |
| 132 | `mdl219_q_glb_dlr_1_intcov` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Interest coverage ratio (EBIT divided by interest expense) |
| 133 | `mdl219_q_glb_dlr_1_invast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inventory-to-total assets ratio calculated as inventory divided by total assets. |
| 134 | `mdl219_q_glb_dlr_1_invto` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Inventory turnover ratio calculated as cost of goods sold divided by average inventory. |
| 135 | `mdl219_q_glb_dlr_1_lagegp` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Lagged inverse PEG ratio calculated using trailing 12-month EPS and sales growth. |
| 136 | `mdl219_q_glb_dlr_1_liqcoeff` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity coefficient measuring the relationship between trading turnover and price returns. |
| 137 | `mdl219_q_glb_dlr_1_ltg` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term growth rate estimates based on analyst forecasts. |
| 138 | `mdl219_q_glb_dlr_1_milliq` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock illiquidity calculated as the monthly average of daily absolute return to daily dollar trading volume. |
| 139 | `mdl219_q_glb_dlr_1_mktcappera` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Market capitalization per analyst calculated as month-end market cap divided by the number of analysts. |
| 140 | `mdl219_q_glb_dlr_1_mktlev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market leverage calculated as market value plus book debt divided by market value. |
| 141 | `mdl219_q_glb_dlr_1_navp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value per share |
| 142 | `mdl219_q_glb_dlr_1_ncfeps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in EPS relative to operating cash flows over the last year. |
| 143 | `mdl219_q_glb_dlr_1_netcashp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net cash-to-price ratio calculated as cash minus debt divided by market price. |
| 144 | `mdl219_q_glb_dlr_1_netdebt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt (total debt minus cash and equivalents); leverage measure |
| 145 | `mdl219_q_glb_dlr_1_nfaldebt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net fixed assets-to-long-term debt ratio measuring asset coverage. |
| 146 | `mdl219_q_glb_dlr_1_niper` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per share |
| 147 | `mdl219_q_glb_dlr_1_nlassets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Natural logarithm of total assets; scale transformation for size |
| 148 | `mdl219_q_glb_dlr_1_nlmktcap` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of market capitalization used for normalization. |
| 149 | `mdl219_q_glb_dlr_1_nlprice` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Natural logarithm of the stock price |
| 150 | `mdl219_q_glb_dlr_1_nlsales` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of trailing 12-month sales used for normalization. |
| 151 | `mdl219_q_glb_dlr_1_nlvolcap` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of trading volume divided by market capitalization. |
| 152 | `mdl219_q_glb_dlr_1_nnastp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net net current assets-to-price ratio calculated as current assets minus liabilities divided by price. |
| 153 | `mdl219_q_glb_dlr_1_noato` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net operating asset turnover |
| 154 | `mdl219_q_glb_dlr_1_nopatmargin` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net Operating Profit After Tax margin; profitability ratio |
| 155 | `mdl219_q_glb_dlr_1_npm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit margin (net income divided by sales); percent |
| 156 | `mdl219_q_glb_dlr_1_ocfast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow scaled by total assets |
| 157 | `mdl219_q_glb_dlr_1_ocfmargin` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow margin (TTM operating cash flow divided by revenue) |
| 158 | `mdl219_q_glb_dlr_1_ocfratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow to revenue ratio (TTM); cash flow efficiency; higher is better |
| 159 | `mdl219_q_glb_dlr_1_ocfroi` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow return on invested capital calculated over trailing 12 months. |
| 160 | `mdl219_q_glb_dlr_1_ollev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating liability leverage calculated as liabilities divided by operating assets. |
| 161 | `mdl219_q_glb_dlr_1_opincltd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating income relative to long-term debt over the last year. |
| 162 | `mdl219_q_glb_dlr_1_oplev` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Operating leverage; sensitivity of operating income to sales; higher implies more fixed‑cost leverage; TTM ratio |
| 163 | `mdl219_q_glb_dlr_1_opmb` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating profit margin; operating income divided by sales; trailing twelve-month ratio |
| 164 | `mdl219_q_glb_dlr_1_p50_200ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-day moving average price divided by the 200-day moving average price. |
| 165 | `mdl219_q_glb_dlr_1_past` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-total assets ratio calculated as market price divided by total assets per share. |
| 166 | `mdl219_q_glb_dlr_1_pctabv260low` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent above the lowest trading price in the last 260 days. |
| 167 | `mdl219_q_glb_dlr_1_pctchg3ycf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in free cash flow over the past 3 years; cumulative percent growth |
| 168 | `mdl219_q_glb_dlr_1_pctchg3yeps` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 3-year growth in EPS calculated as a percentage. |
| 169 | `mdl219_q_glb_dlr_1_pctchg3yfcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in free cash flow over three years |
| 170 | `mdl219_q_glb_dlr_1_pctchg3yocf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in operating cash flow over the past 3 years; cumulative percent growth |
| 171 | `mdl219_q_glb_dlr_1_pctchgastto` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in asset turnover ratio calculated as a percentage. |
| 172 | `mdl219_q_glb_dlr_1_pctchgcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in cash flow; period‑over‑period |
| 173 | `mdl219_q_glb_dlr_1_pctchgeps` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Percent change in EPS over a recent period |
| 174 | `mdl219_q_glb_dlr_1_pctchgfcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in free cash flow per share calculated as a percentage. |
| 175 | `mdl219_q_glb_dlr_1_pctchgocf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in operating cash flow; period‑over‑period |
| 176 | `mdl219_q_glb_dlr_1_pctchgqtrast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in total assets calculated as a percentage. |
| 177 | `mdl219_q_glb_dlr_1_pctchgqtrsales` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in sales calculated as a percentage. |
| 178 | `mdl219_q_glb_dlr_1_pcurlia` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities-to-price ratio calculated as liabilities per share divided by stock price. |
| 179 | `mdl219_q_glb_dlr_1_perg` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Risk-adjusted PEG ratio calculated as price divided by forward EPS and scaled by growth rate. |
| 180 | `mdl219_q_glb_dlr_1_pinoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-net-asset ratio; valuation relative to net assets; higher indicates premium valuation |
| 181 | `mdl219_q_glb_dlr_1_pr_1536` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 15-week moving average price divided by 36-week moving average price. |
| 182 | `mdl219_q_glb_dlr_1_pr_30w75w` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price momentum ratio of 30-week to 75-week moving averages; higher suggests stronger upward trend |
| 183 | `mdl219_q_glb_dlr_1_qr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick ratio; liquidity metric (current assets excluding inventory divided by current liabilities) |
| 184 | `mdl219_q_glb_dlr_1_rationalalpha` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational decay alpha measuring excess return using a decay function for weighting. |
| 185 | `mdl219_q_glb_dlr_1_ratrev6m` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month average of analyst rating revisions. |
| 186 | `mdl219_q_glb_dlr_1_rdsale` | MATRIX | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | R&D intensity calculated as research and development expenses divided by sales. |
| 187 | `mdl219_q_glb_dlr_1_reinrate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment rate calculated as EPS minus dividends divided by book equity. |
| 188 | `mdl219_q_glb_dlr_1_rel5ybp` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 5-year relative book-to-market ratio compared to historical averages. |
| 189 | `mdl219_q_glb_dlr_1_rel5ycfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative cash flow-to-price ratio compared to historical averages. |
| 190 | `mdl219_q_glb_dlr_1_rel5ydivp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative dividend yield compared to historical averages. |
| 191 | `mdl219_q_glb_dlr_1_rel5yebitdap` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative EBITDA-to-price ratio compared to historical averages. |
| 192 | `mdl219_q_glb_dlr_1_rel5yep` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative EPS-to-price ratio compared to historical averages. |
| 193 | `mdl219_q_glb_dlr_1_rel5yfcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow to Price relative to own 5-year history; scaled (percentile or z-score) |
| 194 | `mdl219_q_glb_dlr_1_rel5yocfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Five-year relative operating cash flow to price metric (e.g., z-score/percentile vs own 5Y history) |
| 195 | `mdl219_q_glb_dlr_1_rel5ysp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative sales-to-price ratio compared to historical averages. |
| 196 | `mdl219_q_glb_dlr_1_relpricestrength_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month relative price strength compared to industry averages. |
| 197 | `mdl219_q_glb_dlr_1_reoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings-to-total assets ratio calculated as cumulative retained earnings divided by total assets. |
| 198 | `mdl219_q_glb_dlr_1_rerror60m` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 60-month rolling error measure (process/variation indicator) |
| 199 | `mdl219_q_glb_dlr_1_revper` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per share (total revenue divided by shares outstanding) |
| 200 | `mdl219_q_glb_dlr_1_roa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Assets; net income divided by total assets; percent; higher is better |
| 201 | `mdl219_q_glb_dlr_1_roe` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity |
| 202 | `mdl219_q_glb_dlr_1_roic` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Return on invested capital (ratio) |
| 203 | `mdl219_q_glb_dlr_1_rsi26w` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 26-week Relative Strength Index |
| 204 | `mdl219_q_glb_dlr_1_rtn2nd6m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Second preceding 6-month return calculated as the percent change in stock price from month t-12 to t-7. |
| 205 | `mdl219_q_glb_dlr_1_rtn39w` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 39-week return with a 4-week lag calculated as the price change from week t-43 to week t-4. |
| 206 | `mdl219_q_glb_dlr_1_saleeps` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales per share |
| 207 | `mdl219_q_glb_dlr_1_saleg5y` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Five‑year sales growth rate (percent) |
| 208 | `mdl219_q_glb_dlr_1_salegpm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in quarterly sales relative to gross profit margin over the last year. |
| 209 | `mdl219_q_glb_dlr_1_salerec` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing 12-month sales relative to accounts receivable. |
| 210 | `mdl219_q_glb_dlr_1_sga` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Selling, General and Administrative expenses; operating expense line item, typically trailing twelve months |
| 211 | `mdl219_q_glb_dlr_1_sigma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return volatility calculated as the standard deviation of monthly returns over the last 60 months. |
| 212 | `mdl219_q_glb_dlr_1_skew90cortn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 90-day skewness of returns |
| 213 | `mdl219_q_glb_dlr_1_skew90drtn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-day daily returns calculated as the asymmetry of daily price returns. |
| 214 | `mdl219_q_glb_dlr_1_slope52wp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 52-week price trend line calculated using regression analysis. |
| 215 | `mdl219_q_glb_dlr_1_slope66wp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 66-week price trend line calculated using regression analysis. |
| 216 | `mdl219_q_glb_dlr_1_stockrating` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Street consensus rating calculated as the average analyst recommendation. |
| 217 | `mdl219_q_glb_dlr_1_surp` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Real earnings surprise calculated as the difference between actual EPS and consensus forecasts. |
| 218 | `mdl219_q_glb_dlr_1_susgrowth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sustainable growth rate calculated as ROE multiplied by (1 - dividend payout ratio). |
| 219 | `mdl219_q_glb_dlr_1_swc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Working capital-to-sales ratio calculated as average working capital divided by trailing 12-month sales. |
| 220 | `mdl219_q_glb_dlr_1_tobinq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tobin’s Q ratio (market value to replacement cost of assets); higher indicates potential overvaluation |
| 221 | `mdl219_q_glb_dlr_1_totalcov` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total coverage ratio measuring operating cash flow divided by debt payments. |
| 222 | `mdl219_q_glb_dlr_1_totalsaleg` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Yearly trailing 12-month total sales growth rate calculated as a percentage change. |
| 223 | `mdl219_q_glb_dlr_1_tstalp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year price momentum indicator calculated using correlation-based analysis. |
| 224 | `mdl219_q_glb_dlr_1_ttmaccu` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting accruals calculated as the difference between trailing 12-month net income and operating cash flow. |
| 225 | `mdl219_q_glb_dlr_1_ttmcapexp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12‑month capital expenditures to price; CapEx scaled by market price |
| 226 | `mdl219_q_glb_dlr_1_ttmcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month cash flow-to-price ratio calculated as cash flow per share divided by price. |
| 227 | `mdl219_q_glb_dlr_1_ttmepa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve-month earnings per share |
| 228 | `mdl219_q_glb_dlr_1_ttmepb` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month EPS before extraordinary items-to-price ratio calculated as EPS divided by price. |
| 229 | `mdl219_q_glb_dlr_1_ttmfcfev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-enterprise value ratio calculated over trailing 12 months. |
| 230 | `mdl219_q_glb_dlr_1_ttmfcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months Free Cash Flow to Price ratio |
| 231 | `mdl219_q_glb_dlr_1_ttmgfp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month growth flow-to-price ratio calculated as growth flow per share divided by price. |
| 232 | `mdl219_q_glb_dlr_1_ttmocfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow to market capitalization over the trailing 12 months; higher is better |
| 233 | `mdl219_q_glb_dlr_1_ttmpiqp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing twelve months pre-tax income to price ratio; TTM pre-tax income divided by current price |
| 234 | `mdl219_q_glb_dlr_1_ttmsaleev` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Trailing 12-month sales-to-enterprise value ratio calculated as sales divided by enterprise value. |
| 235 | `mdl219_q_glb_dlr_1_ttmsp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12‑month Sales‑to‑Price ratio (sales divided by market price) |
| 236 | `mdl219_q_glb_dlr_1_tw_ep` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings yield calculated as the weighted average of reported EPS and forward EPS divided by price. |
| 237 | `mdl219_q_glb_dlr_1_uap` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in accounts payable scaled by total assets. |
| 238 | `mdl219_q_glb_dlr_1_uar` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in accounts receivable scaled by total assets. |
| 239 | `mdl219_q_glb_dlr_1_udep` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in depreciation scaled by total assets. |
| 240 | `mdl219_q_glb_dlr_1_uinv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in inventory scaled by total assets. |
| 241 | `mdl219_q_glb_dlr_1_var24m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Variance/volatility over 24 months |
| 242 | `mdl219_q_glb_dlr_1_varresirtn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Variance of residual (idiosyncratic) return vs market |
| 243 | `mdl219_q_glb_dlr_1_visiratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Visibility ratio calculated as the most recent daily trading volume divided by the average daily trading volume over the last 50 days. |
| 244 | `mdl219_q_glb_dlr_1_volpre6m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average trading volume over the preceding 6 months calculated as the moving average of monthly turnover. |
| 245 | `mdl219_q_glb_dlr_1_volto` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading turnover ratio calculated as monthly trading volume divided by shares outstanding. |
| 246 | `mdl219_q_glb_dlr_1_wcacc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital accruals calculated as changes in current assets minus liabilities. |
| 247 | `mdl219_q_glb_dlr_1_wcast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital-to-total assets ratio calculated as average working capital divided by average total assets. |
| 248 | `mdl219_q_glb_dlr_1_wcinv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Working capital-to-inventory ratio calculated as working capital divided by inventory. |
| 249 | `mdl219_q_glb_dlr_1_yoychgaa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accruals-to-assets ratio. |
| 250 | `mdl219_q_glb_dlr_1_yoychgcr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in current ratio. |
| 251 | `mdl219_q_glb_dlr_1_yoychgda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in leverage calculated as total liabilities as a percentage of assets. |
| 252 | `mdl219_q_glb_dlr_1_yoychggpm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in gross profit margin |
| 253 | `mdl219_q_glb_dlr_1_yoychgroa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on assets; percent |
| 254 | `mdl219_q_glb_dlr_2_aci` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Abnormal capital investment measuring changes in capital expenditure intensity for the second module. |
| 255 | `mdl219_q_glb_dlr_2_acp` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Average collection period calculated as accounts receivable times 365 divided by sales for the second module. |
| 256 | `mdl219_q_glb_dlr_2_acqmul` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Acquisition multiple calculated as invested capital divided by EBITDA for the second module. |
| 257 | `mdl219_q_glb_dlr_2_actrtn12m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 12 months; percent |
| 258 | `mdl219_q_glb_dlr_2_actrtn18m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 18-month realized stock return; percentage |
| 259 | `mdl219_q_glb_dlr_2_actrtn1m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | One-month actual return |
| 260 | `mdl219_q_glb_dlr_2_actrtn24m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 24-month total return |
| 261 | `mdl219_q_glb_dlr_2_actrtn2m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 2 months |
| 262 | `mdl219_q_glb_dlr_2_actrtn36m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 36 months |
| 263 | `mdl219_q_glb_dlr_2_actrtn3m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over the past 3 months |
| 264 | `mdl219_q_glb_dlr_2_actrtn60m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month realized stock return; percentage |
| 265 | `mdl219_q_glb_dlr_2_actrtn6m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past 6 months |
| 266 | `mdl219_q_glb_dlr_2_actrtn9m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 9-month total return |
| 267 | `mdl219_q_glb_dlr_2_alpha60m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month alpha (risk-adjusted return intercept) |
| 268 | `mdl219_q_glb_dlr_2_app` | MATRIX | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Average payable period calculated as accounts payable times 365 divided by cost of goods sold for the second module. |
| 269 | `mdl219_q_glb_dlr_2_aqi` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset quality index measuring changes in the ratio of non-current assets to total assets for the second module. |
| 270 | `mdl219_q_glb_dlr_2_aspanratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Attention span ratio measuring operating assets minus liabilities scaled by total assets for the second module. |
| 271 | `mdl219_q_glb_dlr_2_astcomp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month sales divided by most recent quarterly assets |
| 272 | `mdl219_q_glb_dlr_2_astto` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset Turnover: sales divided by total assets |
| 273 | `mdl219_q_glb_dlr_2_bdi` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Basic defensive interval measuring the number of days a company can cover expenses using cash and receivables for the second module. |
| 274 | `mdl219_q_glb_dlr_2_beta` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Market beta coefficient measuring the stock’s sensitivity to market returns (overlay-repaired under DLR_2 when needed) |
| 275 | `mdl219_q_glb_dlr_2_betasigma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Product of beta and volatility (sigma) |
| 276 | `mdl219_q_glb_dlr_2_booklev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book leverage ratio (total assets divided by book equity) |
| 277 | `mdl219_q_glb_dlr_2_bp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Book-to-Price ratio (inverse of P/B) |
| 278 | `mdl219_q_glb_dlr_2_capacq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital acquisition ratio measuring operating cash flow less dividends divided by expenditures for the second module. |
| 279 | `mdl219_q_glb_dlr_2_capexast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital expenditure-to-assets ratio measuring investment intensity for the second module. |
| 280 | `mdl219_q_glb_dlr_2_capexsale` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Capital expenditures divided by sales (capex-to-sales ratio) |
| 281 | `mdl219_q_glb_dlr_2_cashburnrate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash burn rate calculated as negative operating and investment cash flows divided by cash holdings for the second module. |
| 282 | `mdl219_q_glb_dlr_2_cashc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Cash cycle calculated as inventory days plus collection days minus payable days for the second module. |
| 283 | `mdl219_q_glb_dlr_2_cashp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Cash-to-price ratio calculated as cash per share divided by stock price for the second module. |
| 284 | `mdl219_q_glb_dlr_2_cashratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash-to-current liabilities ratio measuring liquidity for the second module. |
| 285 | `mdl219_q_glb_dlr_2_cashratiofixed` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash ratio calculated as cash and equivalents divided by current liabilities for the second module. |
| 286 | `mdl219_q_glb_dlr_2_cashsale` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-sales ratio calculated as average cash divided by sales for the second module. |
| 287 | `mdl219_q_glb_dlr_2_cashsev` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-enterprise value ratio representing total cash divided by enterprise value for the second module. |
| 288 | `mdl219_q_glb_dlr_2_ccd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current cash flow debt coverage ratio measuring cash flow relative to debt for the second module. |
| 289 | `mdl219_q_glb_dlr_2_cfita` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow from investment-to-assets ratio calculated over trailing 12 months for the second module. |
| 290 | `mdl219_q_glb_dlr_2_cfleverage` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow leverage calculated as total liabilities divided by operating cash flow for the second module. |
| 291 | `mdl219_q_glb_dlr_2_cfroi` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow return on investment |
| 292 | `mdl219_q_glb_dlr_2_cg3ysales` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | 3-year compound annual growth rate of sales for the second module. |
| 293 | `mdl219_q_glb_dlr_2_chg3ycfast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in cash flow from assets scaled by total assets for the second module. |
| 294 | `mdl219_q_glb_dlr_2_chg3ycfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow per share scaled by price for the second module. |
| 295 | `mdl219_q_glb_dlr_2_chg3yepsast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in EPS scaled by total assets for the second module. |
| 296 | `mdl219_q_glb_dlr_2_chg3yepsp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-year change in EPS scaled by price for the second module. |
| 297 | `mdl219_q_glb_dlr_2_chg3yfcfast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow scaled by total assets for the second module. |
| 298 | `mdl219_q_glb_dlr_2_chg3yfcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow per share scaled by price for the second module. |
| 299 | `mdl219_q_glb_dlr_2_chg3yocfast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in operating cash flow scaled by total assets for the second module. |
| 300 | `mdl219_q_glb_dlr_2_chg3yocfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in operating cash flow per share scaled by price for the second module. |
| 301 | `mdl219_q_glb_dlr_2_chg6malpha18m` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Six-month change in 18-month alpha |
| 302 | `mdl219_q_glb_dlr_2_chg6mltg` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month change in long-term growth estimates for the second module. |
| 303 | `mdl219_q_glb_dlr_2_chgalpha12m` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 12-month alpha for the second module. |
| 304 | `mdl219_q_glb_dlr_2_chgalpha36m` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 36-month alpha for the second module. |
| 305 | `mdl219_q_glb_dlr_2_chgars` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in accounts receivable as a percentage of sales for the second module. |
| 306 | `mdl219_q_glb_dlr_2_chgcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow scaled by total assets for the second module. |
| 307 | `mdl219_q_glb_dlr_2_chgcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow per share scaled by price for the second module. |
| 308 | `mdl219_q_glb_dlr_2_chgeps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in EPS scaled by total assets for the second module. |
| 309 | `mdl219_q_glb_dlr_2_chgepsp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year change in EPS scaled by price for the second module. |
| 310 | `mdl219_q_glb_dlr_2_chgfcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow scaled by total assets for the second module. |
| 311 | `mdl219_q_glb_dlr_2_chgfcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow per share scaled by price for the second module. |
| 312 | `mdl219_q_glb_dlr_2_chgis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in inventory as a percentage of sales for the second module. |
| 313 | `mdl219_q_glb_dlr_2_chgnoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net operating assets; measures asset growth/efficiency shifts |
| 314 | `mdl219_q_glb_dlr_2_chgnpm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in net profit margin for the second module. |
| 315 | `mdl219_q_glb_dlr_2_chgocf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating cash flow scaled by total assets for the second module. |
| 316 | `mdl219_q_glb_dlr_2_chgocfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating cash flow per share scaled by price for the second module. |
| 317 | `mdl219_q_glb_dlr_2_chgollev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating liability leverage over the last year for the second module. |
| 318 | `mdl219_q_glb_dlr_2_chgopm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating profit margin over the last four quarters |
| 319 | `mdl219_q_glb_dlr_2_chgreccast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accounts receivable relative to current assets for the second module. |
| 320 | `mdl219_q_glb_dlr_2_chgsgasale` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in SG&A expenses relative to sales over the last year for the second module. |
| 321 | `mdl219_q_glb_dlr_2_chgshare` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Percent change in shares outstanding over the last year for the second module. |
| 322 | `mdl219_q_glb_dlr_2_chgvolpre4y` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-year change in average trading volume for the second module. |
| 323 | `mdl219_q_glb_dlr_2_cogsinvt` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Cost of goods sold divided by inventory (TTM) |
| 324 | `mdl219_q_glb_dlr_2_covol` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month trading volume trend for the second module. |
| 325 | `mdl219_q_glb_dlr_2_curindbp_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative book-to-price ratio adjusted for industry averages for the second module. |
| 326 | `mdl219_q_glb_dlr_2_curindcfp_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative cash flow-to-price ratio adjusted for industry averages for the second module. |
| 327 | `mdl219_q_glb_dlr_2_curinddivp_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current industry dividend payout ratio |
| 328 | `mdl219_q_glb_dlr_2_curindebitdap_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative EBITDA-to-price ratio adjusted for industry averages for the second module. |
| 329 | `mdl219_q_glb_dlr_2_curindep_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative EPS-to-price ratio adjusted for industry averages for the second module. |
| 330 | `mdl219_q_glb_dlr_2_curindfcfp_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative free cash flow-to-price ratio adjusted for industry averages for the second module. |
| 331 | `mdl219_q_glb_dlr_2_curindocfp_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Stock’s trailing 12-month operating cash flow-to-price minus the industry average |
| 332 | `mdl219_q_glb_dlr_2_curindocfta_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative operating cash flow-to-assets ratio adjusted for industry averages for the second module. |
| 333 | `mdl219_q_glb_dlr_2_curindsp_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative sales-to-price ratio adjusted for industry averages for the second module. |
| 334 | `mdl219_q_glb_dlr_2_curratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current ratio (current assets divided by current liabilities) |
| 335 | `mdl219_q_glb_dlr_2_cvpre90dp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient of variation of prior 90-day closing prices for the second module. |
| 336 | `mdl219_q_glb_dlr_2_cvvolp20d` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 20-day volume volatility relative to price volatility for the second module. |
| 337 | `mdl219_q_glb_dlr_2_de` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Debt-to-equity ratio |
| 338 | `mdl219_q_glb_dlr_2_debtcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt-to-cash flow ratio calculated over trailing 12 months for the second module. |
| 339 | `mdl219_q_glb_dlr_2_dfl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Financial leverage calculated as pretax income plus interest expense divided by pretax income for the second module. |
| 340 | `mdl219_q_glb_dlr_2_div5yg` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year dividend growth rate (percent) |
| 341 | `mdl219_q_glb_dlr_2_divcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends-to-cash flow ratio calculated over trailing 12 months for the second module. |
| 342 | `mdl219_q_glb_dlr_2_divcov` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend coverage ratio calculated as operating earnings divided by dividends for the second module. |
| 343 | `mdl219_q_glb_dlr_2_divyield` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing dividend yield (dividends per share divided by price) |
| 344 | `mdl219_q_glb_dlr_2_dpcapex` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in depreciation relative to capital expenditures over the last year for the second module. |
| 345 | `mdl219_q_glb_dlr_2_ebitdaev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA to Enterprise Value ratio |
| 346 | `mdl219_q_glb_dlr_2_ebitdap` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month EBITDA-to-price ratio used for valuation for the second module. |
| 347 | `mdl219_q_glb_dlr_2_epschgetr` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | EPS change due to changes in effective tax rate over the last year for the second module. |
| 348 | `mdl219_q_glb_dlr_2_equityto` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity turnover ratio calculated as sales divided by average book equity for the second module. |
| 349 | `mdl219_q_glb_dlr_2_fc_curindfwdep_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative forward 12-month EPS-to-price ratio adjusted for industry averages for the second module. |
| 350 | `mdl219_q_glb_dlr_2_fc_cvfy1eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst forward next fiscal year EPS estimate (CY1) |
| 351 | `mdl219_q_glb_dlr_2_fc_cvfy2eps` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Coefficient of variation of FY2 EPS estimates (std dev divided by mean) |
| 352 | `mdl219_q_glb_dlr_2_fc_dypeg` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of dividend yield-adjusted PEG ratio for the second module. |
| 353 | `mdl219_q_glb_dlr_2_fc_ebop` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Edwards-Bell-Ohlson value-to-price ratio based on valuation models for the second module. |
| 354 | `mdl219_q_glb_dlr_2_fc_egp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inverse PEG ratio adjusted for dividend yield for the second module. |
| 355 | `mdl219_q_glb_dlr_2_fc_epsrm` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision magnitude measuring 3-month change in median earnings forecast for the second module. |
| 356 | `mdl219_q_glb_dlr_2_fc_estep` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leading 12-month median earnings yield calculated as forward EPS divided by price for the second module. |
| 357 | `mdl219_q_glb_dlr_2_fc_f12mepssev` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward EPS-to-enterprise value ratio based on consensus estimates for the second module. |
| 358 | `mdl219_q_glb_dlr_2_fc_fcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward free cash flow to price ratio (forecast FCF divided by market cap) |
| 359 | `mdl219_q_glb_dlr_2_fc_fcfroey1p` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Product of trailing 12-month free cash flow yield and forward ROE for the second module. |
| 360 | `mdl219_q_glb_dlr_2_fc_fwdep` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward earnings yield based on consensus estimates divided by price for the second module. |
| 361 | `mdl219_q_glb_dlr_2_fc_fwdroe` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward return on equity estimated from forecasted earnings |
| 362 | `mdl219_q_glb_dlr_2_fc_hlep` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision confidence measuring the sum of 3-month changes in highest and lowest earnings forecasts for the second module. |
| 363 | `mdl219_q_glb_dlr_2_fc_numest` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of FY1 earnings estimates |
| 364 | `mdl219_q_glb_dlr_2_fc_numrevy1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Net number of FY1 analyst forecast revisions (raised minus lowered) within a month for the second module. |
| 365 | `mdl219_q_glb_dlr_2_fc_pdy` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted dividend yield based on payout ratio and forward EPS estimates for the second module. |
| 366 | `mdl219_q_glb_dlr_2_fc_rel5yfwdep` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative forward 12-month EPS-to-price ratio compared to historical averages for the second module. |
| 367 | `mdl219_q_glb_dlr_2_fc_rev3y1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY1 EPS forecasts scaled by price for the second module. |
| 368 | `mdl219_q_glb_dlr_2_fc_rev3y2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY2 EPS forecasts scaled by price for the second module. |
| 369 | `mdl219_q_glb_dlr_2_fc_rev6` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Average of prior 6-month changes in FY1 consensus earnings forecasts for the second module. |
| 370 | `mdl219_q_glb_dlr_2_fc_stdevfy1epsp` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY1 EPS estimates scaled by price for the second module. |
| 371 | `mdl219_q_glb_dlr_2_fc_stdevfy2epsp` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY2 EPS estimates scaled by price for the second module. |
| 372 | `mdl219_q_glb_dlr_2_fc_y2aepsg` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 2-year projected EPS growth based on analyst forecasts for the second module. |
| 373 | `mdl219_q_glb_dlr_2_fcfequity` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow to equity |
| 374 | `mdl219_q_glb_dlr_2_fcfroi` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow Return on Investment; ratio |
| 375 | `mdl219_q_glb_dlr_2_fcfsale` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow to sales ratio; percentage |
| 376 | `mdl219_q_glb_dlr_2_ff10mrtn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Fama-French momentum factor measuring percent change in stock price over 12 months excluding the most recent month for the second module. |
| 377 | `mdl219_q_glb_dlr_2_fixastto` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fixed asset turnover ratio calculated as sales divided by fixed assets for the second module. |
| 378 | `mdl219_q_glb_dlr_2_flowratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flow ratio measuring liquidity as current assets minus cash divided by liabilities minus debt for the second module. |
| 379 | `mdl219_q_glb_dlr_2_gear` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital gearing ratio calculated as long-term debt divided by total assets minus current liabilities for the second module. |
| 380 | `mdl219_q_glb_dlr_2_high52w` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest trading price over the past 52 weeks |
| 381 | `mdl219_q_glb_dlr_2_indrelcroe_` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-adjusted quarterly return on equity relative to industry averages for the second module. |
| 382 | `mdl219_q_glb_dlr_2_indrelrecd_` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-adjusted doubtful account receivables relative to industry averages for the second module. |
| 383 | `mdl219_q_glb_dlr_2_indrelrtn4w_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative 4-week total return versus industry median/mean |
| 384 | `mdl219_q_glb_dlr_2_indrelrtn5d_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative 5-day return |
| 385 | `mdl219_q_glb_dlr_2_intcov` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Interest coverage ratio (EBIT divided by interest expense) |
| 386 | `mdl219_q_glb_dlr_2_invast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inventory-to-total assets ratio calculated as inventory divided by total assets for the second module. |
| 387 | `mdl219_q_glb_dlr_2_invto` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Inventory turnover ratio (cost of goods sold divided by average inventory; higher indicates efficiency) |
| 388 | `mdl219_q_glb_dlr_2_lagegp` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Lagged inverse PEG ratio calculated using trailing 12-month EPS and sales growth for the second module. |
| 389 | `mdl219_q_glb_dlr_2_liqcoeff` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity coefficient measuring the relationship between trading turnover and price returns for the second module. |
| 390 | `mdl219_q_glb_dlr_2_ltg` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term growth rate estimates based on analyst forecasts for the second module. |
| 391 | `mdl219_q_glb_dlr_2_milliq` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock illiquidity calculated as the monthly average of daily absolute return to daily dollar trading volume for the second module. |
| 392 | `mdl219_q_glb_dlr_2_mktcappera` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market capitalization divided by total assets |
| 393 | `mdl219_q_glb_dlr_2_mktlev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market leverage calculated as market value plus book debt divided by market value for the second module. |
| 394 | `mdl219_q_glb_dlr_2_navp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value-to-price ratio calculated as book value of net assets divided by price for the second module. |
| 395 | `mdl219_q_glb_dlr_2_ncfeps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in EPS relative to operating cash flows over the last year for the second module. |
| 396 | `mdl219_q_glb_dlr_2_netcashp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net cash-to-price ratio calculated as cash minus debt divided by market price for the second module. |
| 397 | `mdl219_q_glb_dlr_2_netdebt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt (total debt minus cash and equivalents), level |
| 398 | `mdl219_q_glb_dlr_2_nfaldebt` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net fixed assets-to-long-term debt ratio measuring asset coverage for the second module. |
| 399 | `mdl219_q_glb_dlr_2_niper` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per share |
| 400 | `mdl219_q_glb_dlr_2_nlassets` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Natural log of total assets |
| 401 | `mdl219_q_glb_dlr_2_nlmktcap` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of market capitalization used for normalization for the second module. |
| 402 | `mdl219_q_glb_dlr_2_nlprice` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Natural logarithm of current stock price |
| 403 | `mdl219_q_glb_dlr_2_nlsales` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of trailing 12-month sales used for normalization for the second module. |
| 404 | `mdl219_q_glb_dlr_2_nlvolcap` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of trading volume divided by market capitalization for the second module. |
| 405 | `mdl219_q_glb_dlr_2_nnastp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net net current assets-to-price ratio calculated as current assets minus liabilities divided by price for the second module. |
| 406 | `mdl219_q_glb_dlr_2_noato` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net operating asset turnover calculated as sales divided by average net operating assets for the second module. |
| 407 | `mdl219_q_glb_dlr_2_nopatmargin` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net operating profit after tax margin |
| 408 | `mdl219_q_glb_dlr_2_npm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit margin (net income divided by sales) |
| 409 | `mdl219_q_glb_dlr_2_ocfast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow-to-assets ratio calculated over trailing 12 months for the second module. |
| 410 | `mdl219_q_glb_dlr_2_ocfmargin` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow margin (TTM ratio) |
| 411 | `mdl219_q_glb_dlr_2_ocfratio` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow to revenue ratio (TTM); cash flow efficiency |
| 412 | `mdl219_q_glb_dlr_2_ocfroi` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow return on invested capital calculated over trailing 12 months for the second module. |
| 413 | `mdl219_q_glb_dlr_2_ollev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating liability leverage calculated as liabilities divided by operating assets for the second module. |
| 414 | `mdl219_q_glb_dlr_2_opincltd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating income relative to long-term debt over the last year for the second module. |
| 415 | `mdl219_q_glb_dlr_2_oplev` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Operating leverage calculated as the percent change in operating income divided by the percent change in sales for the second module. |
| 416 | `mdl219_q_glb_dlr_2_opmb` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating profit margin calculated as operating income divided by sales for the second module. |
| 417 | `mdl219_q_glb_dlr_2_p50_200ratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-day moving average price divided by the 200-day moving average price for the second module. |
| 418 | `mdl219_q_glb_dlr_2_past` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-total assets ratio calculated as market price divided by total assets per share for the second module. |
| 419 | `mdl219_q_glb_dlr_2_pctabv260low` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent distance above the 260-day low price |
| 420 | `mdl219_q_glb_dlr_2_pctchg3ycf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year growth in cash flow per share calculated as a percentage for the second module. |
| 421 | `mdl219_q_glb_dlr_2_pctchg3yeps` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Percent change in trailing 12-month EPS over the past 3 years |
| 422 | `mdl219_q_glb_dlr_2_pctchg3yfcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in Free Cash Flow over the past 3 years |
| 423 | `mdl219_q_glb_dlr_2_pctchg3yocf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in operating cash flow over the past 3 years |
| 424 | `mdl219_q_glb_dlr_2_pctchgastto` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in asset turnover |
| 425 | `mdl219_q_glb_dlr_2_pctchgcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in cash flow period-over-period |
| 426 | `mdl219_q_glb_dlr_2_pctchgeps` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 1-year growth in EPS calculated as a percentage for the second module. |
| 427 | `mdl219_q_glb_dlr_2_pctchgfcf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in free cash flow per share calculated as a percentage for the second module. |
| 428 | `mdl219_q_glb_dlr_2_pctchgocf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in operating cash flow |
| 429 | `mdl219_q_glb_dlr_2_pctchgqtrast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percent change in total assets quarter over quarter |
| 430 | `mdl219_q_glb_dlr_2_pctchgqtrsales` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in sales calculated as a percentage for the second module. |
| 431 | `mdl219_q_glb_dlr_2_pcurlia` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities-to-price ratio calculated as liabilities per share divided by stock price for the second module. |
| 432 | `mdl219_q_glb_dlr_2_perg` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Risk-adjusted PEG ratio calculated as price divided by forward EPS and scaled by growth rate for the second module. |
| 433 | `mdl219_q_glb_dlr_2_pinoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax return on net operating assets calculated as operating income divided by net operating assets for the second module. |
| 434 | `mdl219_q_glb_dlr_2_pr_1536` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 15-week moving average price divided by 36-week moving average price for the second module. |
| 435 | `mdl219_q_glb_dlr_2_pr_30w75w` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price momentum ratio of 30-week to 75-week moving averages; higher suggests upward trend |
| 436 | `mdl219_q_glb_dlr_2_qr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick ratio calculated as current assets minus inventory divided by current liabilities for the second module. |
| 437 | `mdl219_q_glb_dlr_2_rationalalpha` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational decay alpha measuring excess return using a decay function for weighting for the second module. |
| 438 | `mdl219_q_glb_dlr_2_ratrev6m` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month average of analyst rating revisions for the second module. |
| 439 | `mdl219_q_glb_dlr_2_rdsale` | MATRIX | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | R&D intensity calculated as research and development expenses divided by sales for the second module. |
| 440 | `mdl219_q_glb_dlr_2_reinrate` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment rate calculated as EPS minus dividends divided by book equity for the second module. |
| 441 | `mdl219_q_glb_dlr_2_rel5ybp` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 5-year relative book-to-market ratio compared to historical averages for the second module. |
| 442 | `mdl219_q_glb_dlr_2_rel5ycfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative cash flow-to-price ratio compared to historical averages for the second module. |
| 443 | `mdl219_q_glb_dlr_2_rel5ydivp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative dividend yield compared to historical averages for the second module. |
| 444 | `mdl219_q_glb_dlr_2_rel5yebitdap` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative EBITDA-to-price ratio compared to historical averages for the second module. |
| 445 | `mdl219_q_glb_dlr_2_rel5yep` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative EPS-to-price ratio compared to historical averages for the second module. |
| 446 | `mdl219_q_glb_dlr_2_rel5yfcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative free cash flow-to-price ratio compared to historical averages for the second module. |
| 447 | `mdl219_q_glb_dlr_2_rel5yocfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative operating cash flow to price (current vs 5-year baseline) |
| 448 | `mdl219_q_glb_dlr_2_rel5ysp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative sales-to-price ratio compared to historical averages for the second module. |
| 449 | `mdl219_q_glb_dlr_2_relpricestrength_` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month relative price strength compared to industry averages for the second module. |
| 450 | `mdl219_q_glb_dlr_2_reoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings-to-total assets ratio calculated as cumulative retained earnings divided by total assets for the second module. |
| 451 | `mdl219_q_glb_dlr_2_rerror60m` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Regression error of 60-month CAPM used for trend analysis for the second module. |
| 452 | `mdl219_q_glb_dlr_2_revper` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per share (total revenue divided by shares outstanding) |
| 453 | `mdl219_q_glb_dlr_2_roa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on assets net income divided by total assets |
| 454 | `mdl219_q_glb_dlr_2_roe` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on Equity; net income divided by shareholders’ equity; profitability ratio |
| 455 | `mdl219_q_glb_dlr_2_roic` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Return on invested capital, typically trailing twelve months |
| 456 | `mdl219_q_glb_dlr_2_rsi26w` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | 26-week Relative Strength Index |
| 457 | `mdl219_q_glb_dlr_2_rtn2nd6m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Second preceding 6-month return calculated as the percent change in stock price from month t-12 to t-7 for the second module. |
| 458 | `mdl219_q_glb_dlr_2_rtn39w` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 39-week return with a 4-week lag calculated as the price change from week t-43 to week t-4 for the second module. |
| 459 | `mdl219_q_glb_dlr_2_saleeps` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing 12-month sales relative to EPS for the second module. |
| 460 | `mdl219_q_glb_dlr_2_saleg5y` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | 5-year sales growth rate (percent/CAGR) |
| 461 | `mdl219_q_glb_dlr_2_salegpm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in quarterly sales relative to gross profit margin over the last year for the second module. |
| 462 | `mdl219_q_glb_dlr_2_salerec` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing 12-month sales relative to accounts receivable for the second module. |
| 463 | `mdl219_q_glb_dlr_2_sga` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Selling, General and Administrative expenses |
| 464 | `mdl219_q_glb_dlr_2_sigma` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return volatility calculated as the standard deviation of monthly returns over the last 60 months for the second module. |
| 465 | `mdl219_q_glb_dlr_2_skew90cortn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-day daily excess returns calculated as the asymmetry of daily excess price returns for the second module. |
| 466 | `mdl219_q_glb_dlr_2_skew90drtn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-day daily returns calculated as the asymmetry of daily price returns for the second module. |
| 467 | `mdl219_q_glb_dlr_2_slope52wp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 52-week price trend line calculated using regression analysis for the second module. |
| 468 | `mdl219_q_glb_dlr_2_slope66wp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 66-week price trend line calculated using regression analysis for the second module. |
| 469 | `mdl219_q_glb_dlr_2_stockrating` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Street consensus rating calculated as the average analyst recommendation for the second module. |
| 470 | `mdl219_q_glb_dlr_2_surp` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Real earnings surprise calculated as the difference between actual EPS and consensus forecasts for the second module. |
| 471 | `mdl219_q_glb_dlr_2_susgrowth` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sustainable growth rate calculated as ROE multiplied by (1 - dividend payout ratio) for the second module. |
| 472 | `mdl219_q_glb_dlr_2_swc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Working capital-to-sales ratio calculated as average working capital divided by trailing 12-month sales for the second module. |
| 473 | `mdl219_q_glb_dlr_2_tobinq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tobin’s Q ratio (market value to asset replacement cost/value) |
| 474 | `mdl219_q_glb_dlr_2_totalcov` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total coverage ratio measuring operating cash flow divided by debt payments for the second module. |
| 475 | `mdl219_q_glb_dlr_2_totalsaleg` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Yearly trailing 12-month total sales growth rate calculated as a percentage change for the second module. |
| 476 | `mdl219_q_glb_dlr_2_tstalp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year price momentum indicator calculated using correlation-based analysis for the second module. |
| 477 | `mdl219_q_glb_dlr_2_ttmaccu` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting accruals calculated as the difference between trailing 12-month net income and operating cash flow for the second module. |
| 478 | `mdl219_q_glb_dlr_2_ttmcapexp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month capital expenditures-to-price ratio calculated as capital expenditures per share divided by price for the second module. |
| 479 | `mdl219_q_glb_dlr_2_ttmcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month cash flow-to-price ratio calculated as cash flow per share divided by price for the second module. |
| 480 | `mdl219_q_glb_dlr_2_ttmepa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month earnings per share |
| 481 | `mdl219_q_glb_dlr_2_ttmepb` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month EPS before extraordinary items-to-price ratio calculated as EPS divided by price for the second module. |
| 482 | `mdl219_q_glb_dlr_2_ttmfcfev` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months free cash flow to enterprise value (ratio) |
| 483 | `mdl219_q_glb_dlr_2_ttmfcfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month free cash flow to price (FCF yield) ratio |
| 484 | `mdl219_q_glb_dlr_2_ttmgfp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month growth flow-to-price ratio calculated as growth flow per share divided by price for the second module. |
| 485 | `mdl219_q_glb_dlr_2_ttmocfp` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month operating cash flow to market capitalization ratio |
| 486 | `mdl219_q_glb_dlr_2_ttmpiqp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing twelve months pre-tax income to price ratio |
| 487 | `mdl219_q_glb_dlr_2_ttmsaleev` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Trailing 12-month sales-to-enterprise value ratio calculated as sales divided by enterprise value for the second module. |
| 488 | `mdl219_q_glb_dlr_2_ttmsp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | TTM sales-to-price ratio |
| 489 | `mdl219_q_glb_dlr_2_tw_ep` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings yield calculated as the weighted average of reported EPS and forward EPS divided by price for the second module. |
| 490 | `mdl219_q_glb_dlr_2_uap` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in accounts payable scaled by total assets for the second module. |
| 491 | `mdl219_q_glb_dlr_2_uar` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in accounts receivable scaled by total assets for the second module. |
| 492 | `mdl219_q_glb_dlr_2_udep` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in depreciation scaled by total assets for the second module. |
| 493 | `mdl219_q_glb_dlr_2_uinv` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Uninvested cash or inventory balance; currency |
| 494 | `mdl219_q_glb_dlr_2_var24m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month value at risk calculated as the minimum monthly price return over the last 20 months for the second module. |
| 495 | `mdl219_q_glb_dlr_2_varresirtn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month residual return variance calculated as the variance of monthly residual returns for the second module. |
| 496 | `mdl219_q_glb_dlr_2_visiratio` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Visibility ratio calculated as the most recent daily trading volume divided by the average daily trading volume over the last 50 days for th |
| 497 | `mdl219_q_glb_dlr_2_volpre6m` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Average trading volume over the preceding 6 months calculated as the moving average of monthly turnover for the second module. |
| 498 | `mdl219_q_glb_dlr_2_volto` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading turnover ratio calculated as monthly trading volume divided by shares outstanding for the second module. |
| 499 | `mdl219_q_glb_dlr_2_wcacc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital accruals calculated as changes in current assets minus liabilities for the second module. |
| 500 | `mdl219_q_glb_dlr_2_wcast` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital-to-total assets ratio calculated as average working capital divided by average total assets for the second module. |
| 501 | `mdl219_q_glb_dlr_2_wcinv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Working capital-to-inventory ratio calculated as working capital divided by inventory for the second module. |
| 502 | `mdl219_q_glb_dlr_2_yoychgaa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accruals-to-assets ratio for the second module. |
| 503 | `mdl219_q_glb_dlr_2_yoychgcr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in current ratio for the second module. |
| 504 | `mdl219_q_glb_dlr_2_yoychgda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in leverage calculated as total liabilities as a percentage of assets for the second module. |
| 505 | `mdl219_q_glb_dlr_2_yoychggpm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in gross profit margin (percent) |
| 506 | `mdl219_q_glb_dlr_2_yoychgroa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on assets |
| 507 | `mdl219_1_nlmktcap` | MATRIX | 0.982 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of market capitalization used for normalization. |
| 508 | `mdl219_1_nlprice` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Natural logarithm of closing price used for normalization. |
| 509 | `mdl219_1_volto` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading turnover ratio calculated as monthly trading volume divided by shares outstanding. |
| 510 | `mdl219_1_milliq` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock illiquidity calculated as the monthly average of daily absolute return to daily dollar trading volume. |
| 511 | `mdl219_1_actrtn1m` | MATRIX | 0.982 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-month active return representing the percent change in stock price. |
| 512 | `mdl219_1_actrtn2m` | MATRIX | 0.981 | 价量与波动 | 0 | — | — | — | UNTESTED | 2-month active return representing the percent change in stock price. |
| 513 | `mdl219_1_visiratio` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | Visibility ratio calculated as the most recent daily trading volume divided by the average daily trading volume over the last 50 days. |
| 514 | `mdl219_1_indrelrtn4w_` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-week industry-relative return adjusted for industry averages. |
| 515 | `mdl219_1_actrtn3m` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-month active return representing the percent change in stock price. |
| 516 | `mdl219_1_cvvolp20d` | MATRIX | 0.980 | 价量与波动 | 0 | — | — | — | UNTESTED | 20-day volume volatility relative to price volatility |
| 517 | `mdl219_1_aor` | MATRIX | 0.980 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on assets calculated as net income divided by average total assets. |
| 518 | `mdl219_1_equityto` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity turnover ratio calculated as sales divided by average book equity. |
| 519 | `mdl219_1_nlassets` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Natural logarithm of total assets used for normalization. |
| 520 | `mdl219_1_noato` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net operating asset turnover calculated as sales divided by average net operating assets. |
| 521 | `mdl219_1_pvan` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value-to-price ratio calculated as book value of net assets divided by price. |
| 522 | `mdl219_1_astto` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset turnover ratio calculated as sales divided by total assets. |
| 523 | `mdl219_1_stockrating` | MATRIX | 0.979 | 修正与预期 | 0 | — | — | — | UNTESTED | Street consensus rating calculated as the average analyst recommendation. |
| 524 | `mdl219_1_booklev` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book leverage calculated as total assets divided by book equity. |
| 525 | `mdl219_1_past` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-total assets ratio calculated as market price divided by total assets per share. |
| 526 | `mdl219_1_cfita` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow from investment-to-assets ratio calculated over trailing 12 months. |
| 527 | `mdl219_1_ocfast` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow-to-assets ratio calculated over trailing 12 months. |
| 528 | `mdl219_1_pb` | MATRIX | 0.979 | 价量与波动 | 0 | — | — | — | UNTESTED | Book-to-market ratio calculated as book value divided by market price. |
| 529 | `mdl219_1_ed` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Debt-to-equity ratio measuring financial leverage. |
| 530 | `mdl219_1_ttmaccu` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting accruals calculated as the difference between trailing 12-month net income and operating cash flow. |
| 531 | `mdl219_1_netdebt` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt ratio calculated as net debt divided by the sum of net debt, preferred stock, and common stock. |
| 532 | `mdl219_1_ocfroi` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow return on invested capital calculated over trailing 12 months. |
| 533 | `mdl219_1_gspea2y_cf` | MATRIX | 0.979 | 修正与预期 | 0 | — | — | — | UNTESTED | 2-year projected EPS growth based on analyst forecasts. |
| 534 | `mdl219_1_mktcappera` | MATRIX | 0.979 | 修正与预期 | 0 | — | — | — | UNTESTED | Market capitalization per analyst calculated as month-end market cap divided by the number of analysts. |
| 535 | `mdl219_1_yoychgda` | MATRIX | 0.979 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in leverage calculated as total liabilities as a percentage of assets. |
| 536 | `mdl219_1_apemtt` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month EPS after extraordinary items-to-price ratio calculated as EPS divided by price. |
| 537 | `mdl219_1_bpemtt` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month EPS before extraordinary items-to-price ratio calculated as EPS divided by price. |
| 538 | `mdl219_1_pe_wt` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings yield calculated as the weighted average of reported EPS and forward EPS divided by price. |
| 539 | `mdl219_1_pedwf_cf` | MATRIX | 0.978 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward earnings yield based on consensus estimates divided by price. |
| 540 | `mdl219_1_pqipmtt` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month pretax income-to-price ratio calculated as pretax income per share divided by price. |
| 541 | `mdl219_1_fc_estep` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leading 12-month median earnings yield calculated as forward EPS divided by price. |
| 542 | `mdl219_1_pfgmtt` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month growth flow-to-price ratio calculated as growth flow per share divided by price. |
| 543 | `mdl219_1_psmtt` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month sales-to-price ratio calculated as sales per share divided by price. |
| 544 | `mdl219_1_ttmsaleev` | MATRIX | 0.978 | 其他 | 0 | — | — | — | UNTESTED | Trailing 12-month sales-to-enterprise value ratio calculated as sales divided by enterprise value. |
| 545 | `mdl219_1_curindbp_` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative book-to-price ratio adjusted for industry averages. |
| 546 | `mdl219_1_curindocfta_` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative operating cash flow-to-assets ratio adjusted for industry averages. |
| 547 | `mdl219_1_fc_numest` | MATRIX | 0.978 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts providing earnings estimates for FY1. |
| 548 | `mdl219_1_pd09erpvc` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient of variation of prior 90-day closing prices. |
| 549 | `mdl219_1_skew90cortn` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-day daily excess returns calculated as the asymmetry of daily excess price returns. |
| 550 | `mdl219_1_skew90drtn` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-day daily returns calculated as the asymmetry of daily price returns. |
| 551 | `mdl219_1_speghc` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in EPS scaled by total assets. |
| 552 | `mdl219_1_yoychgroa` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on assets. |
| 553 | `mdl219_1_curindep_` | MATRIX | 0.978 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative EPS-to-price ratio adjusted for industry averages. |
| 554 | `mdl219_1_mpn` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit margin calculated as net income divided by sales. |
| 555 | `mdl219_1_pfcomtt` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month operating cash flow-to-price ratio calculated as operating cash flow per share divided by price. |
| 556 | `mdl219_1_fc_numrevy1` | MATRIX | 0.978 | 修正与预期 | 0 | — | — | — | UNTESTED | Net number of FY1 analyst forecast revisions (raised minus lowered) within a month. |
| 557 | `mdl219_1_pfcfmtt` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-price ratio calculated over trailing 12 months. |
| 558 | `mdl219_1_fcfroi` | MATRIX | 0.978 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow return on invested capital calculated over trailing 12 months. |
| 559 | `mdl219_1_fc_curindfwdep_` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative forward 12-month EPS-to-price ratio adjusted for industry averages. |
| 560 | `mdl219_1_pctchgastto` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in asset turnover ratio calculated as a percentage. |
| 561 | `mdl219_1_ocfmargin` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow margin calculated as operating cash flow divided by sales. |
| 562 | `mdl219_1_curindsp_` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative sales-to-price ratio adjusted for industry averages. |
| 563 | `mdl219_1_high52w` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | 52-week high calculated as the highest monthly closing price over the past year. |
| 564 | `mdl219_1_nlsales` | MATRIX | 0.977 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of trailing 12-month sales used for normalization. |
| 565 | `mdl219_1_capexast` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital expenditure-to-assets ratio measuring investment intensity. |
| 566 | `mdl219_1_fcfsale` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-sales ratio calculated over trailing 12 months. |
| 567 | `mdl219_1_volpre6m` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | Average trading volume over the preceding 6 months calculated as the moving average of monthly turnover. |
| 568 | `mdl219_1_curindocfp_` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative operating cash flow-to-price ratio adjusted for industry averages. |
| 569 | `mdl219_1_curindfcfp_` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative free cash flow-to-price ratio adjusted for industry averages. |
| 570 | `mdl219_1_pctabv260low` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent above the lowest trading price in the last 260 days. |
| 571 | `mdl219_1_fcoghc` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating cash flow scaled by total assets. |
| 572 | `mdl219_1_pspeghc` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year change in EPS scaled by price. |
| 573 | `mdl219_1_yoychgaa` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accruals-to-assets ratio. |
| 574 | `mdl219_1_gear` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital gearing ratio calculated as long-term debt divided by total assets minus current liabilities. |
| 575 | `mdl219_1_aoer` | MATRIX | 0.977 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings-to-total assets ratio calculated as cumulative retained earnings divided by total assets. |
| 576 | `mdl219_1_ttmcapexp` | MATRIX | 0.977 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month capital expenditures-to-price ratio calculated as capital expenditures per share divided by price. |
| 577 | `mdl219_1_fcfequity` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow to equity calculated as trailing 12-month free cash flow divided by average book equity. |
| 578 | `mdl219_1_fcfghc` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow scaled by total assets. |
| 579 | `mdl219_1_fixastto` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fixed asset turnover ratio calculated as sales divided by fixed assets. |
| 580 | `mdl219_1_roe` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity calculated as net income divided by shareholder equity. |
| 581 | `mdl219_1_mktlev` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market leverage calculated as market value plus book debt divided by market value. |
| 582 | `mdl219_1_vesspem21f_cf` | MATRIX | 0.976 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward EPS-to-enterprise value ratio based on consensus estimates. |
| 583 | `mdl219_1_capexsale` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital expenditure-to-sales ratio measuring investment relative to revenue. |
| 584 | `mdl219_1_vefcfmtt` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-enterprise value ratio calculated over trailing 12 months. |
| 585 | `mdl219_1_w62isr` | MATRIX | 0.976 | 价量与波动 | 0 | — | — | — | UNTESTED | 26-week relative price strength calculated as the most recent weekly closing price divided by the price 26 weeks ago. |
| 586 | `mdl219_1_indrelcroe_` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-adjusted quarterly return on equity relative to industry averages. |
| 587 | `mdl219_1_pctchgqtrast` | MATRIX | 0.976 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in total assets calculated as a percentage. |
| 588 | `mdl219_1_lfd` | MATRIX | 0.976 | 其他 | 0 | — | — | — | UNTESTED | Financial leverage calculated as pretax income plus interest expense divided by pretax income. |
| 589 | `mdl219_1_roic` | MATRIX | 0.975 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on invested capital calculated as net income and interest expenses divided by invested capital. |
| 590 | `mdl219_1_fc_rev3y1` | MATRIX | 0.975 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY1 EPS forecasts scaled by price. |
| 591 | `mdl219_1_fc_rev3y2` | MATRIX | 0.975 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY2 EPS forecasts scaled by price. |
| 592 | `mdl219_1_totalsaleg` | MATRIX | 0.975 | 宏观与行业 | 0 | — | — | — | UNTESTED | Yearly trailing 12-month total sales growth rate calculated as a percentage change. |
| 593 | `mdl219_1_actrtn6m` | MATRIX | 0.975 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-month active return representing the percent change in stock price. |
| 594 | `mdl219_1_lagegp` | MATRIX | 0.975 | 其他 | 0 | — | — | — | UNTESTED | Lagged inverse PEG ratio calculated using trailing 12-month EPS and sales growth. |
| 595 | `mdl219_1_cfroi` | MATRIX | 0.975 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow return on invested capital calculated over trailing 12 months. |
| 596 | `mdl219_1_pfcmtt` | MATRIX | 0.974 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month cash flow-to-price ratio calculated as cash flow per share divided by price. |
| 597 | `mdl219_1_pfcoghc` | MATRIX | 0.974 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating cash flow per share scaled by price. |
| 598 | `mdl219_1_fc_fcfroey1p` | MATRIX | 0.974 | 盈利与财务 | 0 | — | — | — | UNTESTED | Product of trailing 12-month free cash flow yield and forward ROE. |
| 599 | `mdl219_1_pfcfghc` | MATRIX | 0.974 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow per share scaled by price. |
| 600 | `mdl219_1_fc_fwdroe` | MATRIX | 0.974 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward return on equity calculated as next 4-quarter earnings estimates divided by book equity. |
| 601 | `mdl219_1_curindcfp_` | MATRIX | 0.974 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative cash flow-to-price ratio adjusted for industry averages. |
| 602 | `mdl219_1_mpnghc` | MATRIX | 0.974 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in net profit margin. |
| 603 | `mdl219_1_6351_rp` | MATRIX | 0.974 | 价量与波动 | 0 | — | — | — | UNTESTED | 15-week moving average price divided by 36-week moving average price. |
| 604 | `mdl219_1_pctchgqtrsales` | MATRIX | 0.974 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in sales calculated as a percentage. |
| 605 | `mdl219_1_divyield` | MATRIX | 0.973 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month dividend yield calculated as dividends per share divided by stock price. |
| 606 | `mdl219_1_indrelrtn5d_` | MATRIX | 0.973 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-day industry-relative return adjusted for industry averages. |
| 607 | `mdl219_1_pelh_cf` | MATRIX | 0.973 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision confidence measuring the sum of 3-month changes in highest and lowest earnings forecasts. |
| 608 | `mdl219_1_fcghc` | MATRIX | 0.973 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow scaled by total assets. |
| 609 | `mdl219_1_curinddivp_` | MATRIX | 0.973 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative dividend yield adjusted for industry averages. |
| 610 | `mdl219_1_tobinq` | MATRIX | 0.973 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tobin's Q ratio calculated as the market value of equity plus debt divided by assets. |
| 611 | `mdl219_1_actrtn9m` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | 9-month active return representing the percent change in stock price. |
| 612 | `mdl219_1_bmpo` | MATRIX | 0.972 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating profit margin calculated as operating income divided by sales. |
| 613 | `mdl219_1_ebitdap` | MATRIX | 0.972 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month EBITDA-to-price ratio used for valuation. |
| 614 | `mdl219_1_p50_200ratio` | MATRIX | 0.972 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-day moving average price divided by the 200-day moving average price. |
| 615 | `mdl219_1_curindebitdap_` | MATRIX | 0.972 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative EBITDA-to-price ratio adjusted for industry averages. |
| 616 | `mdl219_1_ebitdaev` | MATRIX | 0.972 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA-to-enterprise value ratio used for valuation. |
| 617 | `mdl219_1_ratrev6m` | MATRIX | 0.972 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month average of analyst rating revisions. |
| 618 | `mdl219_1_capacq` | MATRIX | 0.971 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital acquisition ratio measuring operating cash flow less dividends divided by expenditures. |
| 619 | `mdl219_1_w93ntr` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | 39-week return with a 4-week lag calculated as the price change from week t-43 to week t-4. |
| 620 | `mdl219_1_nlvolcap` | MATRIX | 0.971 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of trading volume divided by market capitalization. |
| 621 | `mdl219_1_reinrate` | MATRIX | 0.971 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment rate calculated as EPS minus dividends divided by book equity. |
| 622 | `mdl219_1_pedu` | MATRIX | 0.971 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in depreciation scaled by total assets. |
| 623 | `mdl219_1_pfcf_cf` | MATRIX | 0.970 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-price ratio calculated over trailing 12 months. |
| 624 | `mdl219_1_susgrowth` | MATRIX | 0.970 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sustainable growth rate calculated as ROE multiplied by (1 - dividend payout ratio). |
| 625 | `mdl219_1_pfcghc` | MATRIX | 0.970 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow per share scaled by price. |
| 626 | `mdl219_1_ntrm01ff` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Fama-French momentum factor measuring percent change in stock price over 12 months excluding the most recent month. |
| 627 | `mdl219_1_m6dn2ntr` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | Second preceding 6-month return calculated as the percent change in stock price from month t-12 to t-7. |
| 628 | `mdl219_1_tstalp` | MATRIX | 0.969 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year price momentum indicator calculated using correlation-based analysis. |
| 629 | `mdl219_1_fc_stdevfy2epsp` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY2 EPS estimates scaled by price. |
| 630 | `mdl219_1_fc_stdevfy1epsp` | MATRIX | 0.968 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY1 EPS estimates scaled by price. |
| 631 | `mdl219_1_slope52wp` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 52-week price trend line calculated using regression analysis. |
| 632 | `mdl219_1_actrtn12m` | MATRIX | 0.968 | 价量与波动 | 0 | — | — | — | UNTESTED | 12-month active return representing the percent change in stock price. |
| 633 | `mdl219_1_relpricestrength_` | MATRIX | 0.967 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month relative price strength compared to industry averages. |
| 634 | `mdl219_1_debtcf` | MATRIX | 0.967 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt-to-cash flow ratio calculated over trailing 12 months. |
| 635 | `mdl219_1_chg3yepsast` | MATRIX | 0.967 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in EPS scaled by total assets. |
| 636 | `mdl219_1_niper` | MATRIX | 0.966 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per employee calculated as income after taxes divided by the number of employees. |
| 637 | `mdl219_1_revper` | MATRIX | 0.966 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per employee calculated as trailing 12-month sales divided by the number of employees. |
| 638 | `mdl219_1_surp` | MATRIX | 0.966 | 修正与预期 | 0 | — | — | — | UNTESTED | Real earnings surprise calculated as the difference between actual EPS and consensus forecasts. |
| 639 | `mdl219_1_rationalalpha` | MATRIX | 0.966 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational decay alpha measuring excess return using a decay function for weighting. |
| 640 | `mdl219_1_chg3yepsp` | MATRIX | 0.966 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-year change in EPS scaled by price. |
| 641 | `mdl219_1_chgshare` | MATRIX | 0.966 | 其他 | 0 | — | — | — | UNTESTED | Percent change in shares outstanding over the last year. |
| 642 | `mdl219_1_mpoghc` | MATRIX | 0.965 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating profit margin. |
| 643 | `mdl219_1_fc_rev6` | MATRIX | 0.965 | 修正与预期 | 0 | — | — | — | UNTESTED | Average of prior 6-month changes in FY1 consensus earnings forecasts. |
| 644 | `mdl219_1_slope66wp` | MATRIX | 0.964 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 66-week price trend line calculated using regression analysis. |
| 645 | `mdl219_1_nopatmargin` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | NOPAT margin calculated as net operating profit after tax divided by net sales. |
| 646 | `mdl219_1_pctchgeps` | MATRIX | 0.964 | 其他 | 0 | — | — | — | UNTESTED | 1-year growth in EPS calculated as a percentage. |
| 647 | `mdl219_1_pctchgocf` | MATRIX | 0.964 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in operating cash flow per share calculated as a percentage. |
| 648 | `mdl219_1_voctni` | MATRIX | 0.963 | 其他 | 0 | — | — | — | UNTESTED | Interest coverage ratio calculated as operating income divided by interest expenses. |
| 649 | `mdl219_1_cfleverage` | MATRIX | 0.963 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow leverage calculated as total liabilities divided by operating cash flow. |
| 650 | `mdl219_1_w57w03_rp` | MATRIX | 0.963 | 价量与波动 | 0 | — | — | — | UNTESTED | 30-week moving average price divided by 75-week moving average price. |
| 651 | `mdl219_1_pctchgcf` | MATRIX | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in cash flow per share calculated as a percentage. |
| 652 | `mdl219_1_chgalpha12m` | MATRIX | 0.962 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 12-month alpha. |
| 653 | `mdl219_1_oplev` | MATRIX | 0.962 | 其他 | 0 | — | — | — | UNTESTED | Operating leverage calculated as the percent change in operating income divided by the percent change in sales. |
| 654 | `mdl219_1_lumqca` | MATRIX | 0.961 | 盈利与财务 | 0 | — | — | — | UNTESTED | Acquisition multiple calculated as invested capital divided by EBITDA. |
| 655 | `mdl219_1_actrtn18m` | MATRIX | 0.961 | 价量与波动 | 0 | — | — | — | UNTESTED | 18-month active return representing the percent change in stock price. |
| 656 | `mdl219_1_mrspe_cf` | MATRIX | 0.961 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision magnitude measuring 3-month change in median earnings forecast. |
| 657 | `mdl219_1_epschgetr` | MATRIX | 0.960 | 宏观与行业 | 0 | — | — | — | UNTESTED | EPS change due to changes in effective tax rate over the last year. |
| 658 | `mdl219_1_chg3yocfast` | MATRIX | 0.960 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in operating cash flow scaled by total assets. |
| 659 | `mdl219_1_chg3yfcfast` | MATRIX | 0.959 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow scaled by total assets. |
| 660 | `mdl219_1_spe1yfvc_cf` | MATRIX | 0.958 | 修正与预期 | 0 | — | — | — | UNTESTED | Dispersion of FY1 EPS estimates calculated as standard deviation divided by mean. |
| 661 | `mdl219_1_totalcov` | MATRIX | 0.958 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total coverage ratio measuring operating cash flow divided by debt payments. |
| 662 | `mdl219_1_liqcoeff` | MATRIX | 0.958 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity coefficient measuring the relationship between trading turnover and price returns. |
| 663 | `mdl219_1_spe2yfvc_cf` | MATRIX | 0.958 | 修正与预期 | 0 | — | — | — | UNTESTED | Dispersion of FY2 EPS estimates calculated as standard deviation divided by mean. |
| 664 | `mdl219_1_chg6malpha18m` | MATRIX | 0.955 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 18-month alpha. |
| 665 | `mdl219_1_m42rav` | MATRIX | 0.955 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month value at risk calculated as the minimum monthly price return over the last 20 months. |
| 666 | `mdl219_1_saleeps` | MATRIX | 0.954 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing 12-month sales relative to EPS. |
| 667 | `mdl219_1_chg3ycfast` | MATRIX | 0.954 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in cash flow from assets scaled by total assets. |
| 668 | `mdl219_1_actrtn24m` | MATRIX | 0.954 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month active return representing the percent change in stock price. |
| 669 | `mdl219_1_pfcoy3ghc` | MATRIX | 0.953 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in operating cash flow per share scaled by price. |
| 670 | `mdl219_1_ica` | MATRIX | 0.953 | 其他 | 0 | — | — | — | UNTESTED | Abnormal capital investment measuring changes in capital expenditure intensity. |
| 671 | `mdl219_1_pfcfy3ghc` | MATRIX | 0.953 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow per share scaled by price. |
| 672 | `mdl219_1_nfaldebt` | MATRIX | 0.952 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net fixed assets-to-long-term debt ratio measuring asset coverage. |
| 673 | `mdl219_1_spefcn` | MATRIX | 0.950 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in EPS relative to operating cash flows over the last year. |
| 674 | `mdl219_1_pctchg3yeps` | MATRIX | 0.950 | 其他 | 0 | — | — | — | UNTESTED | 3-year growth in EPS calculated as a percentage. |
| 675 | `mdl219_1_cg3ysales` | MATRIX | 0.949 | 宏观与行业 | 0 | — | — | — | UNTESTED | 3-year compound annual growth rate of sales. |
| 676 | `mdl219_1_pfcy3ghc` | MATRIX | 0.948 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow per share scaled by price. |
| 677 | `distribution_range_interquartile` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Interquartile range of a distribution, indicating spread. |
| 678 | `fifty_two_week_high_price_6` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest share price reached in the past fifty-two weeks. |
| 679 | `market_liquidity_score` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Score or measure of the stock's market liquidity. |
| 680 | `net_liquidation_market_cap` | MATRIX | 0.947 | 其他 | 0 | — | — | — | UNTESTED | Market capitalization based on net liquidation value. |
| 681 | `net_liquidation_price_2` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Net liquidation price of the security. |
| 682 | `relative_strength_index_fourteen_days` | MATRIX | 0.947 | 其他 | 0 | — | — | — | UNTESTED | Relative Strength Index calculated over fourteen days. |
| 683 | `volume_turnover_ratio_3` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of trading volume to shares outstanding. |
| 684 | `actual_one_month_return` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return achieved over the past one month. |
| 685 | `drawdown_one_month_standard_deviation` | MATRIX | 0.947 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of drawdowns over one month. |
| 686 | `normalized_last_price_usd` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Normalized last traded price in US dollars. |
| 687 | `normalized_market_cap_usd` | MATRIX | 0.947 | 其他 | 0 | — | — | — | UNTESTED | Market capitalization in USD, normalized for comparison. |
| 688 | `percent_above_260_day_low_2` | MATRIX | 0.947 | 其他 | 0 | — | — | — | UNTESTED | Percentage that current value is above the 260-day low. |
| 689 | `coefficient_of_variation_volume_20_days` | MATRIX | 0.947 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient of variation for trading volume over the past 20 days. |
| 690 | `actual_return_two_months_2` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over the past two months. |
| 691 | `visibility_ratio_metric_2` | MATRIX | 0.946 | 其他 | 0 | — | — | — | UNTESTED | Metric indicating the visibility of company operations. |
| 692 | `net_liquid_assets_usd_2` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net liquid assets measured in US dollars. |
| 693 | `book_leverage_ratio_12` | MATRIX | 0.946 | 其他 | 0 | — | — | — | UNTESTED | Book value based leverage ratio. |
| 694 | `book_value_per_equity_share` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value per share, representing net asset value per equity share. |
| 695 | `depreciation_amortization_value` | MATRIX | 0.946 | 其他 | 0 | — | — | — | UNTESTED | Depreciation and amortization value. |
| 696 | `historical_performance_metric_2` | MATRIX | 0.946 | 其他 | 0 | — | — | — | UNTESTED | Metric representing past performance of the company. |
| 697 | `net_asset_value_per_share_6` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value divided by number of shares. |
| 698 | `net_liquid_assets_amount` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Amount of net liquid assets held by the company. |
| 699 | `debt_to_equity_ratio_10` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to total equity. |
| 700 | `return_on_assets_ratio_12` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio measuring net income generated from total assets. |
| 701 | `trailing_twelve_months_price_income_quality_per_share` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Price to income quality per share over the trailing twelve months. |
| 702 | `ttm_earnings_per_share_b` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months earnings per share, version b. |
| 703 | `actual_return_three_months_2` | MATRIX | 0.946 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return achieved over three months. |
| 704 | `asset_turnover_ratio_13` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of sales to average assets. |
| 705 | `equity_turnover_ratio_9` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Turnover ratio of equity. |
| 706 | `net_operating_assets_turnover_2` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Turnover ratio of net operating assets. |
| 707 | `return_on_equity_operating_assets` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity calculated using operating assets. |
| 708 | `trailing_twelve_months_gross_profit_per_share_2` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross profit per share over the trailing twelve months. |
| 709 | `trailing_twelve_months_sales_per_share_2` | MATRIX | 0.946 | 其他 | 0 | — | — | — | UNTESTED | Sales per share calculated over the trailing twelve months. |
| 710 | `ttm_earnings_per_share_a` | MATRIX | 0.946 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months earnings per share, version a. |
| 711 | `ttm_sales_enterprise_value_ratio` | MATRIX | 0.946 | 其他 | 0 | — | — | — | UNTESTED | Trailing twelve months sales to enterprise value ratio. |
| 712 | `core_earnings_per_share_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Core earnings per share, excluding nonrecurring items. |
| 713 | `financial_leverage_ratio_5` | MATRIX | 0.945 | 其他 | 0 | — | — | — | UNTESTED | Ratio indicating the degree of financial leverage. |
| 714 | `industry_relative_return_5d_2` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Return relative to industry over the past 5 days. |
| 715 | `market_leverage_ratio_6` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market leverage, typically debt to equity or similar ratio. |
| 716 | `stock_analyst_rating_score` | MATRIX | 0.945 | 修正与预期 | 0 | — | — | — | UNTESTED | Score representing analyst rating or recommendation for the stock. |
| 717 | `current_industry_book_value_per_share` | MATRIX | 0.945 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current book value per share relative to industry peers. |
| 718 | `industry_relative_return_four_weeks_2` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Return relative to industry peers over four weeks. |
| 719 | `current_industry_sales_per_share` | MATRIX | 0.945 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current industry average sales per share. |
| 720 | `operating_cash_flow_return_on_investment_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on investment calculated using operating cash flow. |
| 721 | `operating_cash_flow_to_assets_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of operating cash flow to total assets. |
| 722 | `trailing_twelve_months_accruals` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accruals calculated over the trailing twelve months. |
| 723 | `ttm_operating_cash_flow_enterprise_value` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months operating cash flow to enterprise value ratio. |
| 724 | `ttm_operating_cash_flow_per_share` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months operating cash flow per share. |
| 725 | `year_over_year_change_depreciation_amortization_2` | MATRIX | 0.945 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in depreciation and amortization. |
| 726 | `cash_flow_to_invested_assets` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash flow to invested assets. |
| 727 | `current_industry_eps` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current industry average earnings per share. |
| 728 | `inverse_ratio_ttm_sales_ev` | MATRIX | 0.945 | 其他 | 0 | — | — | — | UNTESTED | Inverse ratio of trailing twelve months sales to enterprise value. |
| 729 | `net_debt_value_3` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt held by the company. |
| 730 | `sixty_day_volatility` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Volatility measured over the past 60 days. |
| 731 | `percent_change_quarterly_assets_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in assets from the previous quarter. |
| 732 | `ttm_free_cash_flow_per_share` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months free cash flow per share. |
| 733 | `net_liquid_sales_usd` | MATRIX | 0.945 | 其他 | 0 | — | — | — | UNTESTED | Net liquid sales measured in US dollars. |
| 734 | `price_to_revenue_ratio_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of share price to revenue per share. |
| 735 | `change_eps_per_share` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share over a period. |
| 736 | `change_twelve_month_total_debt_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in total debt over the past twelve months. |
| 737 | `net_profit_margin_value` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit margin as a percentage of revenue. |
| 738 | `volume_prior_six_months` | MATRIX | 0.945 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading volume measured over the prior six months. |
| 739 | `change_earnings_per_share_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share value. |
| 740 | `current_industry_operating_cash_flow_per_share_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current operating cash flow per share relative to industry peers. |
| 741 | `current_industry_operating_cash_flow_to_assets` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow to assets ratio for the current industry. |
| 742 | `net_latest_sales_value` | MATRIX | 0.945 | 其他 | 0 | — | — | — | UNTESTED | Most recent net sales value reported by the company. |
| 743 | `yoy_change_return_on_assets_2` | MATRIX | 0.945 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on assets. |
| 744 | `forecast_estimated_eps` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Forecasted estimated earnings per share. |
| 745 | `forecast_forward_eps` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted forward earnings per share. |
| 746 | `forecast_number_of_estimates` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analyst estimates in forecast. |
| 747 | `free_cash_flow_to_equity_value` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow available to equity holders. |
| 748 | `market_capitalization_per_asset_2` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market capitalization divided by total assets. |
| 749 | `trailing_twelve_months_capex_per_share` | MATRIX | 0.944 | 其他 | 0 | — | — | — | UNTESTED | Capital expenditures per share over the trailing twelve months. |
| 750 | `current_industry_free_cash_flow_per_share_2` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current free cash flow per share relative to industry peers. |
| 751 | `forward_year_two_annual_eps_growth` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected annual earnings per share growth for the second forward year. |
| 752 | `free_cash_flow_return_on_investment_2` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on investment based on free cash flow. |
| 753 | `total_working_earnings_power` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total working earnings power metric. |
| 754 | `year2_ahead_eps_growth_pct` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share growth percentage two years ahead. |
| 755 | `ttm_free_cash_flow_enterprise_value` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months free cash flow to enterprise value ratio. |
| 756 | `coefficient_variation_pre_90d_price_2` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient of variation for price over the 90 days prior. |
| 757 | `operating_cash_flow_margin_4` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Margin calculated from operating cash flow as a percentage of sales. |
| 758 | `change_in_operating_cash_flow` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating cash flow over a specified period. |
| 759 | `change_operating_cash_flow_per_share` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating cash flow per share over a specified period. |
| 760 | `skewness_90d_return` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of returns over the past 90 days. |
| 761 | `skewness_of_ninety_day_co_return` | MATRIX | 0.944 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of co-movement returns over a ninety-day period. |
| 762 | `free_cash_flow_to_sales` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow divided by sales. |
| 763 | `year_over_year_change_average_assets_2` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in average assets. |
| 764 | `capital_expenditure_to_assets_3` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of capital expenditures to total assets. |
| 765 | `change_in_free_cash_flow_per_share_2` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in free cash flow per share over a period. |
| 766 | `lagged_earnings_growth_percent_2` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings growth percentage from a previous period. |
| 767 | `total_sales_growth_2` | MATRIX | 0.944 | 其他 | 0 | — | — | — | UNTESTED | Growth in total sales over a period. |
| 768 | `fixed_asset_turnover_ratio_2` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of sales to fixed assets, measuring asset efficiency. |
| 769 | `percent_change_in_asset_turnover` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in asset turnover ratio over a period. |
| 770 | `percent_change_quarterly_sales_3` | MATRIX | 0.944 | 其他 | 0 | — | — | — | UNTESTED | Percentage change in sales compared to the previous quarter. |
| 771 | `capital_expenditure_to_sales` | MATRIX | 0.944 | 其他 | 0 | — | — | — | UNTESTED | Ratio of capital expenditures to sales. |
| 772 | `forecasted_forward_12m_eps_to_ev` | MATRIX | 0.944 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted forward 12-month earnings per share to enterprise value ratio. |
| 773 | `forecasted_number_of_revenue_estimates_year1` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of revenue estimates for the next fiscal year based on forecasts. |
| 774 | `number_of_revenue_estimates_year_two` | MATRIX | 0.944 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of revenue estimates for the second forecast year. |
| 775 | `earnings_shortfall_value` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shortfall in earnings compared to expectations. |
| 776 | `change_in_free_cash_flow` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in free cash flow over a specified period. |
| 777 | `change_net_profit_margin_3` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net profit margin over a specified period. |
| 778 | `forecasted_current_industry_forward_eps_2` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted forward earnings per share for the current industry. |
| 779 | `compensation_depreciation_amortization_ratio` | MATRIX | 0.943 | 其他 | 0 | — | — | — | UNTESTED | Ratio of compensation to depreciation and amortization expenses. |
| 780 | `return_on_equity_ratio_15` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio measuring net income generated from shareholders' equity. |
| 781 | `tobin_q_ratio_3` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of market value of assets to replacement cost of assets. |
| 782 | `industry_relative_cash_return_on_equity_2` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash return on equity relative to industry peers. |
| 783 | `mdl219_1_pctchg3yocf` | MATRIX | 0.943 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year growth in operating cash flow per share calculated as a percentage. |
| 784 | `dividend_yield_percent_6` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend yield as a percentage of share price. |
| 785 | `relative_strength_index_26w` | MATRIX | 0.942 | 其他 | 0 | — | — | — | UNTESTED | Relative Strength Index calculated over a 26-week period. |
| 786 | `degree_financial_leverage_3` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Degree of financial leverage, indicating sensitivity of earnings to debt. |
| 787 | `return_on_invested_capital_value` | MATRIX | 0.942 | 价量与波动 | 0 | — | — | — | UNTESTED | Return on invested capital as a percentage. |
| 788 | `forecasted_revenue_three_years_one_period` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted revenue for three years, one period. |
| 789 | `reinvestment_rate_5` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Rate at which earnings or cash flow are reinvested in the business. |
| 790 | `sustainable_growth_rate_value_2` | MATRIX | 0.942 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sustainable growth rate of the company. |
| 791 | `current_industry_dividend_per_share` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current industry average dividend per share. |
| 792 | `forecast_revenue_3y2` | MATRIX | 0.942 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted revenue for the third year in a two-year period. |
| 793 | `actual_return_six_months_2` | MATRIX | 0.941 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over the past six months. |
| 794 | `current_ratio_percent` | MATRIX | 0.941 | 其他 | 0 | — | — | — | UNTESTED | Current ratio expressed as a percentage. |
| 795 | `forward_roe_projection` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected return on equity for a forward period. |
| 796 | `high_sensitivity_score` | MATRIX | 0.941 | 风险与质量 | 0 | — | — | — | UNTESTED | Score indicating the stock's sensitivity to market or factor changes. |
| 797 | `inflation_rate_value` | MATRIX | 0.941 | 宏观与行业 | 0 | — | — | — | UNTESTED | Value of the inflation rate. |
| 798 | `intellectual_property_score` | MATRIX | 0.941 | 风险与质量 | 0 | — | — | — | UNTESTED | Score or measure related to the company's intellectual property. |
| 799 | `oil_price_value_2` | MATRIX | 0.941 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of oil price. |
| 800 | `volatility_index_value` | MATRIX | 0.941 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of the volatility index, indicating market volatility. |
| 801 | `yield_spread_value` | MATRIX | 0.941 | 价量与波动 | 0 | — | — | — | UNTESTED | Difference between yields of two financial instruments. |
| 802 | `forward_fcfe_return_on_equity_y1` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward free cash flow to equity return on equity for year one. |
| 803 | `mdl219_1_opincltd` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating income relative to long-term debt over the last year. |
| 804 | `mdl219_1_saleg5y` | MATRIX | 0.941 | 其他 | 0 | — | — | — | UNTESTED | 5-year sales growth calculated as the difference between trailing 12-month sales and sales 20 quarters ago. |
| 805 | `current_industry_cash_flow_per_share` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current cash flow per share compared to industry average. |
| 806 | `trailing_twelve_months_cash_flow_per_share` | MATRIX | 0.941 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share over the trailing twelve months. |
| 807 | `normalized_volume_capitalization` | MATRIX | 0.940 | 价量与波动 | 0 | — | — | — | UNTESTED | Normalized volume capitalization value. |
| 808 | `price_ratio_fifteen_to_thirtysix` | MATRIX | 0.940 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of price over 15 periods to price over 36 periods. |
| 809 | `cash_flow_return_on_investment_6` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on investment calculated using cash flow. |
| 810 | `mdl219_1_pctchg3ycf` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year growth in cash flow per share calculated as a percentage. |
| 811 | `forecast_high_low_eps_2` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted high and low values for earnings per share. |
| 812 | `current_industry_ebitda_per_share_2` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current EBITDA per share compared to industry average. |
| 813 | `ebitda_per_share_3` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA divided by number of shares. |
| 814 | `mdl219_1_dcc` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current cash flow debt coverage ratio measuring cash flow relative to debt. |
| 815 | `trailing_twelve_months_operating_income_ev` | MATRIX | 0.940 | 其他 | 0 | — | — | — | UNTESTED | Operating income to enterprise value ratio over the trailing twelve months. |
| 816 | `compound_estimated_return_on_equity` | MATRIX | 0.940 | 修正与预期 | 0 | — | — | — | UNTESTED | Compound estimated return on equity over a period. |
| 817 | `six_month_revenue_forward_year_two` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected revenue for six months in the second forward year. |
| 818 | `change_cash_flow` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow over a period. |
| 819 | `ebitda_to_enterprise_value_ratio_10` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of EBITDA to enterprise value. |
| 820 | `mdl219_1_actrtn36m` | MATRIX | 0.940 | 价量与波动 | 0 | — | — | — | UNTESTED | 36-month active return representing the percent change in stock price. |
| 821 | `operating_margin_b` | MATRIX | 0.940 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating margin, version b. |
| 822 | `forecast_stddev_next_year_eps_per_share` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of forecasted earnings per share for the next fiscal year. |
| 823 | `change_in_shares_outstanding_2` | MATRIX | 0.939 | 其他 | 0 | — | — | — | UNTESTED | Change in the number of shares outstanding. |
| 824 | `forecast_stddev_fy2_eps_per_share_2` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of forecasted earnings per share for fiscal year two. |
| 825 | `capital_acquisition_ratio_8` | MATRIX | 0.939 | 其他 | 0 | — | — | — | UNTESTED | Ratio measuring the amount of capital acquired by a company. |
| 826 | `forward_sales_per_share_projection` | MATRIX | 0.939 | 其他 | 0 | — | — | — | UNTESTED | Projected sales per share for a forward period. |
| 827 | `mdl219_1_gtl` | MATRIX | 0.939 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term growth rate estimates based on analyst forecasts. |
| 828 | `median_to_long_term_price_ratio` | MATRIX | 0.939 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of median price over 50 days to price over 200 days, measuring price trend. |
| 829 | `twelve_week_sales_per_share` | MATRIX | 0.939 | 其他 | 0 | — | — | — | UNTESTED | Sales per share measured over a twelve-week period. |
| 830 | `actual_return_nine_months_2` | MATRIX | 0.939 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over the past nine months. |
| 831 | `change_cash_flow_per_share` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow per share over a specified period. |
| 832 | `mdl219_1_pge_cf` | MATRIX | 0.939 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inverse PEG ratio adjusted for dividend yield. |
| 833 | `six_month_revenue_ratio` | MATRIX | 0.938 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of revenue over a six-month period. |
| 834 | `thirty_nine_week_return` | MATRIX | 0.938 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return over the past thirty-nine weeks. |
| 835 | `unearned_depreciation_expense` | MATRIX | 0.938 | 其他 | 0 | — | — | — | UNTESTED | Total unearned depreciation expense. |
| 836 | `percent_change_operating_cash_flow_2` | MATRIX | 0.938 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in operating cash flow over a period. |
| 837 | `debt_to_market_capitalization_ratio_2` | MATRIX | 0.938 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to market capitalization. |
| 838 | `forward_free_cash_flow_per_share` | MATRIX | 0.938 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected free cash flow per share for a forward period. |
| 839 | `nopat_margin_value` | MATRIX | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net operating profit after tax margin. |
| 840 | `operating_leverage_value` | MATRIX | 0.937 | 其他 | 0 | — | — | — | UNTESTED | Value of operating leverage. |
| 841 | `three_year_change_eps_per_share` | MATRIX | 0.937 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share over three years. |
| 842 | `three_year_change_in_eps_to_assets` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share to assets ratio over the past three years. |
| 843 | `fama_french_ten_month_return` | MATRIX | 0.936 | 价量与波动 | 0 | — | — | — | UNTESTED | Return based on the Fama-French ten-month methodology. |
| 844 | `second_six_month_return` | MATRIX | 0.936 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return during the second six-month period. |
| 845 | `net_income_percent` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income as a percentage of a reference value. |
| 846 | `revenue_performance_score` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Score or measure of revenue performance. |
| 847 | `total_stable_liabilities_per_share` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total stable liabilities divided by number of shares. |
| 848 | `slope_52_week_price_2` | MATRIX | 0.936 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of price trend over 52 weeks. |
| 849 | `actual_return_twelve_months_2` | MATRIX | 0.936 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over the past twelve months. |
| 850 | `change_in_operating_margin_3` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating margin over a specified period. |
| 851 | `three_year_change_ocf_to_assets_2` | MATRIX | 0.936 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year change in the ratio of operating cash flow to total assets. |
| 852 | `change_operating_leverage_3` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Change in operating leverage over a specified period. |
| 853 | `revenue_3m_yoy_stddev` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of three-month year-over-year revenue. |
| 854 | `earnings_surprise_percent` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage by which actual earnings differ from expectations. |
| 855 | `revenue_three_month_year_one_stddev` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of revenue over three months in the first year. |
| 856 | `three_year_change_operating_cf_per_share` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating cash flow per share over three years. |
| 857 | `forward_book_value_per_share_2` | MATRIX | 0.935 | 其他 | 0 | — | — | — | UNTESTED | Projected book value per share for a future period. |
| 858 | `mdl219_1_ollev` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating liability leverage calculated as liabilities divided by operating assets. |
| 859 | `percent_change_earnings_per_share_2` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in earnings per share over a period. |
| 860 | `interest_coverage_ratio_15` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of earnings before interest and taxes to interest expense. |
| 861 | `relative_price_strength_score` | MATRIX | 0.935 | 价量与波动 | 0 | — | — | — | UNTESTED | Score measuring the stock's price performance relative to peers or market. |
| 862 | `three_year_change_fcf_to_assets_2` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in free cash flow to assets over three years. |
| 863 | `ebitda_to_debt_ratio_5` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of EBITDA to total debt. |
| 864 | `rational_alpha_score_2` | MATRIX | 0.935 | 风险与质量 | 0 | — | — | — | UNTESTED | Score representing the rationality or quality of alpha signals. |
| 865 | `three_year_change_free_cash_flow_per_share_2` | MATRIX | 0.935 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year change in free cash flow per share. |
| 866 | `compound_growth_three_year_sales` | MATRIX | 0.934 | 宏观与行业 | 0 | — | — | — | UNTESTED | Compound annual growth rate of sales over the past three years. |
| 867 | `percent_change_cash_flow` | MATRIX | 0.934 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in cash flow over a given period. |
| 868 | `forecasted_coefficient_variation_next_year_eps` | MATRIX | 0.934 | 盈利与财务 | 0 | — | — | — | UNTESTED | Coefficient of variation for forecasted next year earnings per share. |
| 869 | `forecast_coefficient_variation_fy2_eps` | MATRIX | 0.934 | 其他 | 0 | — | — | — | UNTESTED | Coefficient of variation for forecasted FY2 EPS. |
| 870 | `mdl219_1_chgollev` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating liability leverage over the last year. |
| 871 | `net_financial_liabilities_debt_2` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net financial liabilities related to company debt. |
| 872 | `mdl219_1_chgalpha36m` | MATRIX | 0.933 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 36-month alpha. |
| 873 | `slope_66_week_price` | MATRIX | 0.933 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of price trend over 66 weeks. |
| 874 | `liquidity_coefficient_5` | MATRIX | 0.933 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient indicating the liquidity position of the company. |
| 875 | `total_coverage_ratio_5` | MATRIX | 0.933 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total coverage ratio, often used to assess debt service ability. |
| 876 | `two_way_book_price_ratio` | MATRIX | 0.932 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio comparing two different book price measures. |
| 877 | `price_ratio_30w_75w` | MATRIX | 0.932 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of price over 30-week to 75-week moving average. |
| 878 | `change_alpha_twelve_months` | MATRIX | 0.931 | 其他 | 0 | — | — | — | UNTESTED | Change in alpha over a twelve-month period. |
| 879 | `five_year_eps_trend_slope_4` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | Slope of the earnings per share trend over the past five years. |
| 880 | `r_squared_four_quarter_eps_five_years` | MATRIX | 0.931 | 其他 | 0 | — | — | — | UNTESTED | R-squared of four-quarter EPS over a five-year period. |
| 881 | `three_year_change_in_cash_flow_to_assets` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow to assets ratio over the past three years. |
| 882 | `yoy_change_roe_artificial` | MATRIX | 0.931 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on equity (artificially calculated). |
| 883 | `percent_change_three_year_operating_cash_flow` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in operating cash flow over three years. |
| 884 | `forecasted_eps_rolling_mean` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | Rolling mean of forecasted earnings per share. |
| 885 | `three_year_change_cash_flow_per_share_3` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow per share over three years. |
| 886 | `actual_return_eighteen_months_2` | MATRIX | 0.930 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return achieved over eighteen months. |
| 887 | `cash_flow_to_leverage_ratio` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash flow to total leverage, indicating debt coverage by cash flow. |
| 888 | `debt_to_cash_flow_ratio_4` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to cash flow. |
| 889 | `mdl219_1_fc_dypeg` | MATRIX | 0.930 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of dividend yield-adjusted PEG ratio. |
| 890 | `fifty_two_week_high_price_5` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Highest price reached in the last 52 weeks. |
| 891 | `forecasted_year_two_earnings_growth` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected earnings growth for the second forecast year. |
| 892 | `interquartile_range_debt_ratio` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Interquartile range of the debt ratio. |
| 893 | `market_illiquidity_indicator` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Indicator of market illiquidity. |
| 894 | `net_liquidation_price` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Net liquidation price of a security. |
| 895 | `net_liquidation_price_usd` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Net liquidation price of a security in US dollars. |
| 896 | `normalized_market_capitalization` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Market capitalization normalized for comparison. |
| 897 | `normalized_market_capitalization_usd` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Market capitalization normalized and expressed in US dollars. |
| 898 | `relative_strength_index_14d` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Relative Strength Index calculated over 14 days. |
| 899 | `volume_turnover_ratio_2` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of trading volume turnover. |
| 900 | `actual_return_one_month` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over a one-month period. |
| 901 | `one_month_return_volatility_3` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of returns over a one-month period. |
| 902 | `percent_above_260_day_low` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentage above the 260-day low price. |
| 903 | `coefficient_variation_volume_past_twenty_days` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient of variation for trading volume over the past twenty days. |
| 904 | `operating_leverage_ratio_5` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Ratio measuring the degree of operating leverage. |
| 905 | `percent_change_three_year_eps_2` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in earnings per share over three years. |
| 906 | `asset_composition_index` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Index measuring the composition of company assets. |
| 907 | `coefficient_variation_four_quarter_eps_five_years` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Coefficient of variation for four-quarter EPS over five years. |
| 908 | `eps_change_effective_tax_rate_2` | MATRIX | 0.929 | 宏观与行业 | 0 | — | — | — | UNTESTED | Change in effective tax rate due to EPS changes. |
| 909 | `net_liquid_assets_usd` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net liquid assets denominated in US dollars. |
| 910 | `forward_six_month_revenue_projection` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected revenue for the next six months. |
| 911 | `actual_return_two_months` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past two months. |
| 912 | `book_value_per_share_10` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book value of equity per share outstanding. |
| 913 | `visibility_ratio_metric` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Ratio indicating the visibility of financial metrics or forecasts. |
| 914 | `actual_return_three_months` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past three months. |
| 915 | `asset_turnover_ratio_12` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of sales to average total assets. |
| 916 | `book_leverage_ratio_11` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Leverage ratio based on book values. |
| 917 | `core_earnings_per_share` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Core earnings per share, excluding nonrecurring items. |
| 918 | `current_industry_book_price` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Current book price relative to industry peers. |
| 919 | `current_industry_earnings_per_share` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current earnings per share for the industry. |
| 920 | `current_industry_sales_performance` | MATRIX | 0.929 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current sales performance relative to industry. |
| 921 | `debt_to_equity_ratio_9` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to total equity. |
| 922 | `discretionary_accruals` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Amount of discretionary accruals in financial statements. |
| 923 | `equity_turnover_ratio_8` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Turnover ratio of equity. |
| 924 | `gearing_ratio_metric` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Metric representing the company's gearing ratio. |
| 925 | `historical_performance_metric` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Metric representing past performance. |
| 926 | `industry_relative_return_5_days` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Return relative to industry peers over 5 days. |
| 927 | `market_leverage_ratio_5` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of total debt to market capitalization. |
| 928 | `net_asset_value_per_share_5` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value per share. |
| 929 | `net_liquid_assets_value` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Value of net liquid assets held by the company. |
| 930 | `return_on_assets_ratio_11` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on assets, measuring profitability relative to total assets. |
| 931 | `return_on_equity_assets` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity relative to assets. |
| 932 | `trailing_twelve_months_eps_variant_a` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share for the trailing twelve months, version a. |
| 933 | `trailing_twelve_months_sales_per_share` | MATRIX | 0.929 | 其他 | 0 | — | — | — | UNTESTED | Sales per share over the trailing twelve months. |
| 934 | `ttm_earnings_per_share_version_b` | MATRIX | 0.929 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months earnings per share, version b. |
| 935 | `ttm_price_income_quality_per_share` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing twelve months price to income quality per share. |
| 936 | `volume_previous_6_months` | MATRIX | 0.929 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading volume over the previous 6 months. |
| 937 | `coefficient_variation_pre_90d_price` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient of variation for price over the 90 days prior. |
| 938 | `current_industry_operating_cash_flow_per_share` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current industry average operating cash flow per share. |
| 939 | `current_industry_operating_cashflow_to_assets` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current operating cash flow to assets ratio for the industry. |
| 940 | `industry_relative_cash_return_on_equity` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative cash return on equity. |
| 941 | `industry_relative_return_four_weeks` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Return relative to industry peers over four weeks. |
| 942 | `inverse_ttm_sales_to_enterprise_value` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Inverse of trailing twelve months sales to enterprise value ratio. |
| 943 | `operating_cash_flow_return_on_investment` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on investment calculated using operating cash flow. |
| 944 | `operating_cashflow_to_assets_4` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of operating cash flow to total assets. |
| 945 | `percent_change_quarterly_assets` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in assets from one quarter to the next. |
| 946 | `return_on_equity_ratio_14` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity, measuring profitability relative to shareholder equity. |
| 947 | `skewness_90_day_return` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of returns over a 90-day period. |
| 948 | `skewness_ninety_day_co_return` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of co-movement returns over ninety days. |
| 949 | `trailing_twelve_months_free_cash_flow_per_share` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share over the trailing twelve months. |
| 950 | `trailing_twelve_months_operating_cash_flow_per_share` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow per share over the trailing twelve months. |
| 951 | `trailing_twelve_months_sales_to_enterprise_value` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Sales to enterprise value ratio over the trailing twelve months. |
| 952 | `ttm_accumulation_metric` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Accumulation metric calculated over the trailing twelve months. |
| 953 | `year_over_year_change_depreciation_amortization` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in depreciation and amortization. |
| 954 | `cash_flow_to_invested_assets_ratio` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash flow to invested assets. |
| 955 | `change_operating_cash_flow` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating cash flow over a specified period. |
| 956 | `change_operating_cashflow_per_share` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating cash flow per share over a period. |
| 957 | `compound_growth_three_year_ttm_eps_a` | MATRIX | 0.928 | 宏观与行业 | 0 | — | — | — | UNTESTED | Compound annual growth rate of trailing twelve months EPS (version a) over three years. |
| 958 | `current_industry_free_cash_flow_per_share` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current industry average free cash flow per share. |
| 959 | `free_cash_flow_to_equity_3` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow available to equity holders. |
| 960 | `net_debt_amount` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total debt minus cash and cash equivalents. |
| 961 | `net_liquidation_volume_cap` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Net liquidation volume cap for a security. |
| 962 | `net_local_sales_usd` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Net sales in US dollars. |
| 963 | `net_operating_assets_turnover` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Turnover ratio of net operating assets. |
| 964 | `price_return` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Return based on price appreciation. |
| 965 | `relative_strength_index_twenty_six_weeks` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Relative Strength Index calculated over twenty-six weeks. |
| 966 | `year_over_year_change_return_on_assets` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on assets. |
| 967 | `actual_return_six_months` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over a six-month period. |
| 968 | `capital_expenditure_to_assets_2` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of capital expenditure to total assets. |
| 969 | `crude_oil_price_metric` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Metric representing the price of crude oil. |
| 970 | `current_ratio_proportion_2` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Proportion of current assets to current liabilities. |
| 971 | `free_cash_flow_return_on_investment` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on investment calculated using free cash flow. |
| 972 | `high_low_mid_price_indicator` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Indicator representing high, low, and mid price levels for a security. |
| 973 | `inflation_rate_2` | MATRIX | 0.928 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rate of inflation over a specified period. |
| 974 | `intellectual_property_indicator` | MATRIX | 0.928 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Indicator or value related to intellectual property holdings. |
| 975 | `operating_cash_flow_margin_3` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Margin of operating cash flow as a percentage of sales. |
| 976 | `price_return_15_36` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Price return over the 15 to 36 period window. |
| 977 | `sixty_day_standard_deviation` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of a financial metric over the past 60 days. |
| 978 | `trailing_twelve_months_capital_expenditure_per_share` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Capital expenditure per share over the trailing twelve months. |
| 979 | `ttm_free_cashflow_to_enterprise_value` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing twelve months free cash flow to enterprise value ratio. |
| 980 | `us_dollar_value_metric` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Metric value expressed in US dollars. |
| 981 | `volatility_index_metric` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Volatility index representing market expectations of volatility. |
| 982 | `yield_spread_metric` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Metric representing the spread between yields. |
| 983 | `capital_expenditure_to_sales_ratio_5` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Ratio of capital expenditures to total sales. |
| 984 | `change_free_cash_flow` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in free cash flow over a specified period. |
| 985 | `free_cashflow_to_sales_ratio_4` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of free cash flow to sales. |
| 986 | `net_local_sales_amount` | MATRIX | 0.928 | 宏观与行业 | 0 | — | — | — | UNTESTED | Net sales in local currency. |
| 987 | `net_profit_margin_5` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit margin as a percentage of sales. |
| 988 | `percent_change_asset_turnover` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in asset turnover ratio. |
| 989 | `percent_change_quarterly_sales_2` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Percent change in sales from the previous quarter. |
| 990 | `total_sales_growth` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Total growth in sales over a specified period. |
| 991 | `trailing_twelve_months_gross_profit_per_share` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross profit per share calculated for the trailing twelve months. |
| 992 | `actual_return_nine_months` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual total return over the past nine months. |
| 993 | `change_shares_outstanding` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Change in the number of shares outstanding. |
| 994 | `change_twelve_month_total_debt` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in total debt over the past twelve months. |
| 995 | `cumulative_effect_return_on_equity` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cumulative effect on return on equity. |
| 996 | `price_50_200_day_ratio` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of price over 50 days to price over 200 days. |
| 997 | `return_39_weeks` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Total return over a 39-week period. |
| 998 | `trailing_twelve_months_operating_cash_flow_ev` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow to enterprise value over the trailing twelve months. |
| 999 | `change_earnings_per_share` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share over a specified period. |
| 1000 | `change_earnings_per_share_period` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share over a specific period. |
| 1001 | `mdl219_1_pctchgfcf` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in free cash flow per share calculated as a percentage. |
| 1002 | `percent_change_operating_cash_flow` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in operating cash flow. |
| 1003 | `change_in_free_cash_flow_per_share` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in free cash flow per share over a period. |
| 1004 | `dividend_yield_ratio_10` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend yield expressed as a percentage of share price. |
| 1005 | `earnings_shortfall_indicator_2` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of earnings falling short of expectations. |
| 1006 | `fixed_asset_turnover` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of sales to fixed assets. |
| 1007 | `forward_10_month_return` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Return projected for the next ten months. |
| 1008 | `lagged_earnings_growth_percent` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Lagged percentage growth in earnings. |
| 1009 | `liquidity_coefficient_4` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient measuring the liquidity of a security. |
| 1010 | `return_second_six_months` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Total return during the second six-month period. |
| 1011 | `slope_52_week_price` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of price trend over 52 weeks. |
| 1012 | `total_stability_long_period` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Stability measure over a long period. |
| 1013 | `year_over_year_change_average_assets` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in average assets. |
| 1014 | `actual_return_twelve_months` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over a twelve-month period. |
| 1015 | `current_industry_dividend_payout` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current industry average dividend payout ratio. |
| 1016 | `rational_alpha_score` | MATRIX | 0.928 | 风险与质量 | 0 | — | — | — | UNTESTED | Score representing the rational alpha signal. |
| 1017 | `change_net_profit_margin_2` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net profit margin over a specified period. |
| 1018 | `company_depreciation_amortization` | MATRIX | 0.928 | 其他 | 0 | — | — | — | UNTESTED | Company's depreciation and amortization value. |
| 1019 | `relative_price_strength` | MATRIX | 0.928 | 价量与波动 | 0 | — | — | — | UNTESTED | Strength of a security's price performance relative to the market. |
| 1020 | `stock_rating_indicator` | MATRIX | 0.928 | 修正与预期 | 0 | — | — | — | UNTESTED | Indicator of stock rating or analyst recommendation. |
| 1021 | `three_year_percent_change_cash_flow` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in cash flow over three years. |
| 1022 | `tobin_q_ratio_2` | MATRIX | 0.928 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tobin's Q ratio, comparing market value to asset replacement cost. |
| 1023 | `change_3y_operating_cashflow_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating cash flow per share over three years. |
| 1024 | `change_3y_operating_cashflow_to_assets_2` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating cash flow to assets ratio over three years. |
| 1025 | `compound_growth_3y_free_cash_flow` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year compound growth rate of free cash flow. |
| 1026 | `sustainable_growth_rate_6` | MATRIX | 0.927 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rate at which a company can grow sustainably. |
| 1027 | `change_cashflow` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow over a specified period. |
| 1028 | `change_three_year_fcf_to_assets` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in free cash flow to assets ratio over three years. |
| 1029 | `change_three_year_free_cash_flow_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in free cash flow per share over three years. |
| 1030 | `current_industry_cashflow_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current cash flow per share for the industry. |
| 1031 | `percent_change_earnings_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in earnings per share over a period. |
| 1032 | `reinvestment_rate_4` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Rate at which earnings are reinvested in the business. |
| 1033 | `slope_66_week_price_trend` | MATRIX | 0.927 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of price trend over 66 weeks. |
| 1034 | `trailing_twelve_months_cashflow_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share over the trailing twelve months. |
| 1035 | `cash_flow_return_on_investment_5` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on investment calculated using cash flow. |
| 1036 | `net_financial_liabilities_debt` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net financial liabilities related to debt obligations. |
| 1037 | `price_ratio_30_week_75_week` | MATRIX | 0.927 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of price over 30 weeks to price over 75 weeks. |
| 1038 | `upward_movement_indicator` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | Indicator of upward movement in a financial metric. |
| 1039 | `change_alpha_12_months` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | Change in alpha metric over the past 12 months. |
| 1040 | `change_three_year_eps_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share over three years. |
| 1041 | `change_three_year_eps_to_assets` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in the ratio of earnings per share to assets over three years. |
| 1042 | `ratio_revenue_6_months` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of revenue over the past 6 months. |
| 1043 | `actual_return_eighteen_months` | MATRIX | 0.927 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over an eighteen-month period. |
| 1044 | `cumulative_growth_3y_sales` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | Cumulative growth in sales over three years. |
| 1045 | `current_industry_ebitda_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current EBITDA per share for the industry. |
| 1046 | `change_in_cash_flow_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow per share over a period. |
| 1047 | `ebitda_per_share` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA calculated on a per share basis. |
| 1048 | `ebitda_to_enterprise_value_ratio_9` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of EBITDA to enterprise value. |
| 1049 | `acquisition_multiple_value` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | Acquisition multiple used in company valuation. |
| 1050 | `cash_conversion_days` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Number of days required to convert cash investments into revenue. |
| 1051 | `price_book_roe_residual` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Residual value from price-to-book and return on equity analysis. |
| 1052 | `ebitda_to_debt_ratio_4` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of EBITDA to total debt. |
| 1053 | `graham_number` | MATRIX | 0.927 | 修正与预期 | 0 | — | — | — | UNTESTED | Intrinsic value estimate based on Graham's formula. |
| 1054 | `percent_change_3y_operating_cashflow` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in operating cash flow over three years. |
| 1055 | `ttm_operating_income_to_enterprise_value` | MATRIX | 0.927 | 其他 | 0 | — | — | — | UNTESTED | Trailing twelve months operating income divided by enterprise value. |
| 1056 | `cash_flow_leverage_ratio_3` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash flow to leverage. |
| 1057 | `debt_to_cash_flow_ratio_3` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of debt to cash flow. |
| 1058 | `percent_change_free_cash_flow` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in free cash flow over a given period. |
| 1059 | `unexpected_profit_indicator` | MATRIX | 0.927 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator for unexpected profit events. |
| 1060 | `net_debt_to_ebitda` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt divided by EBITDA. |
| 1061 | `net_income_percentage` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income as a percentage of revenue. |
| 1062 | `operating_income_ltd` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Cumulative operating income to date. |
| 1063 | `revenue_per_share_3` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue generated per share outstanding. |
| 1064 | `capital_acquisition_ratio_7` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Ratio of capital acquired over a period. |
| 1065 | `eps_change_effective_tax_rate` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in earnings per share due to effective tax rate variation. |
| 1066 | `operating_profit_margin_b` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating profit margin, version B. |
| 1067 | `percent_change_three_year_eps` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in earnings per share over three years. |
| 1068 | `unlevered_debt_equity_position` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unlevered debt to equity position. |
| 1069 | `change_six_month_alpha_eighteen_months` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Change in alpha over six months compared to the previous eighteen months. |
| 1070 | `forecast_count_estimates` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of forecasts or analyst estimates available. |
| 1071 | `forward_estimated_earnings_per_share` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward estimate of earnings per share. |
| 1072 | `forward_estimated_earnings_per_share_next_period` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward estimate of earnings per share for the next reporting period. |
| 1073 | `market_capitalization_per_asset` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market capitalization divided by total assets. |
| 1074 | `percent_change_cashflow` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in cash flow over a specified period. |
| 1075 | `return_on_invested_capital_ratio_2` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on invested capital, measuring profitability relative to invested capital. |
| 1076 | `sales_to_eps_ratio` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of sales to earnings per share. |
| 1077 | `variance_24_months` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Variance of a financial metric over the past 24 months. |
| 1078 | `forecast_year2_annualized_eps_growth` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected annualized earnings per share growth for the second forecast year. |
| 1079 | `forecasted_current_industry_forward_eps` | MATRIX | 0.926 | 宏观与行业 | 0 | — | — | — | UNTESTED | Projected forward EPS for the current industry. |
| 1080 | `time_weighted_earnings_per_share` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings per share. |
| 1081 | `year_two_annual_eps_growth_percent_change` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Percent change in annual EPS growth for year two. |
| 1082 | `six_month_change_alpha_eighteen_months` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Six-month change in alpha measured over an eighteen-month window. |
| 1083 | `variance_twenty_four_months` | MATRIX | 0.926 | 价量与波动 | 0 | — | — | — | UNTESTED | Variance of returns over twenty-four months. |
| 1084 | `forward_ebitda_enterprise_value_ratio_4` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking EBITDA to enterprise value ratio. |
| 1085 | `relative_5y_book_price` | MATRIX | 0.926 | 价量与波动 | 0 | — | — | — | UNTESTED | Relative book price over five years. |
| 1086 | `actual_return_24_months` | MATRIX | 0.926 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over a 24-month period. |
| 1087 | `average_ten_year_earnings_per_share` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average earnings per share over the past ten years. |
| 1088 | `forecast_count_revenue_year_one` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Number of revenue forecasts for the first year. |
| 1089 | `percent_change_three_year_free_cash_flow` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in free cash flow over three years. |
| 1090 | `relative_five_year_earnings_power` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings power relative to the five-year average. |
| 1091 | `relative_five_year_operating_cash_flow_performance` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow performance relative to peers over five years. |
| 1092 | `relative_five_year_sales_performance` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Sales performance relative to peers over five years. |
| 1093 | `cash_conversion_days_2` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Number of days required to convert resources into cash flows. |
| 1094 | `degree_financial_leverage_2` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Degree of financial leverage for the company. |
| 1095 | `forecast_high_low_eps` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | High and low forecasted earnings per share. |
| 1096 | `forecast_revenue_three_year_one` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted revenue for the first of three years. |
| 1097 | `number_revenue_year2` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Number of revenue entries for year two. |
| 1098 | `relative_5y_free_cashflow_per_share` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share relative to a benchmark over five years. |
| 1099 | `sales_growth_5_years` | MATRIX | 0.926 | 其他 | 0 | — | — | — | UNTESTED | Sales growth over the past five years. |
| 1100 | `asset_coverage_index` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Index measuring the coverage of assets. |
| 1101 | `change_3y_cashflow_per_share` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow per share over three years. |
| 1102 | `change_3y_cashflow_to_assets` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in cash flow to assets ratio over three years. |
| 1103 | `forward_revenue_3_years_ago_2` | MATRIX | 0.926 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward revenue estimate for the period three years ago, version 2. |
| 1104 | `net_cashflow_earnings_per_share` | MATRIX | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net cash flow earnings per share. |
| 1105 | `actual_return_twenty_four_months` | MATRIX | 0.925 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return achieved over twenty-four months. |
| 1106 | `coefficient_of_volatility` | MATRIX | 0.925 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient measuring volatility of returns or other metrics. |
| 1107 | `forecast_free_cash_flow_return_on_equity_year_one` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted free cash flow return on equity for year one. |
| 1108 | `forecasted_forward_12m_eps_to_enterprise_value` | MATRIX | 0.925 | 其他 | 0 | — | — | — | UNTESTED | Projected forward 12-month EPS to enterprise value ratio. |
| 1109 | `forecasted_forward_return_on_equity` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted forward-looking return on equity. |
| 1110 | `net_operating_profit_after_tax_margin_2` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Margin of net operating profit after tax. |
| 1111 | `time_weighted_ebitda_to_enterprise_value_3` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted ratio of EBITDA to enterprise value. |
| 1112 | `beta_coefficient` | MATRIX | 0.925 | 风险与质量 | 0 | — | — | — | UNTESTED | Beta coefficient measuring systematic risk relative to the market. |
| 1113 | `ebitda_to_debt_change_ratio` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of EBITDA to change in debt. |
| 1114 | `percent_change_three_year_cash_flow` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in cash flow over the past three years. |
| 1115 | `actual_return_thirty_six_months` | MATRIX | 0.925 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over a thirty-six month period. |
| 1116 | `total_coverage_metric_2` | MATRIX | 0.925 | 其他 | 0 | — | — | — | UNTESTED | Metric representing total coverage of a financial variable. |
| 1117 | `change_alpha_36_months` | MATRIX | 0.925 | 其他 | 0 | — | — | — | UNTESTED | Change in alpha metric over the past 36 months. |
| 1118 | `forward_eps_return_metric` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward earnings per share return metric. |
| 1119 | `forecast_free_cashflow_per_share` | MATRIX | 0.925 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted free cash flow per share. |
| 1120 | `variance_residual_return` | MATRIX | 0.925 | 价量与波动 | 0 | — | — | — | UNTESTED | Variance of residual returns. |
| 1121 | `change_in_operating_margin_2` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating margin over a period. |
| 1122 | `year_over_year_change_in_roe_percent` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year percentage change in return on equity. |
| 1123 | `r_squared_4q_eps_5y` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | R-squared value for four-quarter EPS over five years. |
| 1124 | `relative_five_year_dividend_to_price` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of dividend to price relative to peers over five years. |
| 1125 | `slope_4q_eps_5y` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Slope of quarterly earnings per share over five years. |
| 1126 | `acquisition_multiple_2` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Valuation multiple used in acquisition analysis. |
| 1127 | `interest_coverage_ratio_14` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of earnings before interest and taxes to interest expense. |
| 1128 | `operating_leverage_metric_2` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Measure of operating leverage. |
| 1129 | `relative_five_year_cash_flow_per_share` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow per share relative to the five-year average. |
| 1130 | `change_volume_previous_four_years` | MATRIX | 0.924 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in trading volume compared to four years prior. |
| 1131 | `coefficient_variation_4q_eps_5y` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Coefficient of variation for four-quarter EPS over five years. |
| 1132 | `compound_growth_three_years_return_on_invested_capital` | MATRIX | 0.924 | 价量与波动 | 0 | — | — | — | UNTESTED | Compound growth rate of return on invested capital over three years. |
| 1133 | `surprise_metric` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Metric indicating the degree of surprise in reported results. |
| 1134 | `actual_return_60_months` | MATRIX | 0.924 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over the past 60 months. |
| 1135 | `alpha_metric_60_months` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Alpha value calculated over 60 months. |
| 1136 | `beta_standard_deviation` | MATRIX | 0.924 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of beta values over a specified period. |
| 1137 | `five_year_dividend_growth_3` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth rate of dividends over five years. |
| 1138 | `forecast_stddev_fy1_eps_per_share` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of forecasted earnings per share for fiscal year one. |
| 1139 | `forecast_stddev_fy2_eps_per_share` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of forecasted earnings per share for fiscal year two. |
| 1140 | `residual_error_60_months` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Residual error calculated over 60 months. |
| 1141 | `sales_emea_region` | MATRIX | 0.924 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sales generated in the EMEA (Europe, Middle East, Africa) region. |
| 1142 | `standard_deviation_returns` | MATRIX | 0.924 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of returns over a specified period. |
| 1143 | `forward_relative_5y_earnings_per_share` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward relative earnings per share over five years. |
| 1144 | `revenue_6_months_forward_year_2` | MATRIX | 0.924 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue forecast for the next 6 months in the second forward year. |
| 1145 | `operating_leverage_ratio_4` | MATRIX | 0.924 | 其他 | 0 | — | — | — | UNTESTED | Ratio measuring the sensitivity of operating income to sales. |
| 1146 | `revenue_3_months_year_1_stddev` | MATRIX | 0.923 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of revenue over 3 months in year 1. |
| 1147 | `change_quarterly_eps_surprise_2` | MATRIX | 0.923 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in quarterly earnings per share surprise. |
| 1148 | `change_operating_leverage_2` | MATRIX | 0.923 | 其他 | 0 | — | — | — | UNTESTED | Change in operating leverage over a specified period. |
| 1149 | `revenue_3_months_year_2_stddev` | MATRIX | 0.923 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of revenue over 3 months in year 2. |
| 1150 | `forecast_coefficient_variation_fy1_eps` | MATRIX | 0.923 | 其他 | 0 | — | — | — | UNTESTED | Coefficient of variation for forecasted EPS in fiscal year 1. |
| 1151 | `forecasted_coefficient_variation_fy2_eps` | MATRIX | 0.923 | 其他 | 0 | — | — | — | UNTESTED | Projected coefficient of variation for second fiscal year EPS. |
| 1152 | `forward_book_value_per_share` | MATRIX | 0.923 | 其他 | 0 | — | — | — | UNTESTED | Projected book value per share for a future period. |
| 1153 | `forward_earnings_before_operations` | MATRIX | 0.923 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward estimate of earnings before operations. |
| 1154 | `mdl219_1_covol` | MATRIX | 0.923 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month trading volume trend. |
| 1155 | `ebitda_debt_change` | MATRIX | 0.923 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in EBITDA relative to debt. |
| 1156 | `forward_revenue_6_months` | MATRIX | 0.923 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward revenue estimate for the next 6 months. |
| 1157 | `forward_year_2_eps_growth` | MATRIX | 0.923 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward earnings per share growth for year 2. |
| 1158 | `operating_income_limited_adjustment` | MATRIX | 0.923 | 其他 | 0 | — | — | — | UNTESTED | Operating income adjusted for specific limitations or exclusions. |
| 1159 | `relative_5y_ebitda_per_share` | MATRIX | 0.923 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA per share relative to a benchmark over five years. |
| 1160 | `forecast_earnings_growth_percent` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted percentage growth in earnings. |
| 1161 | `forecast_quarterly_surprise_standard_deviation` | MATRIX | 0.922 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of forecasted quarterly surprises. |
| 1162 | `long_term_growth_projection_2` | MATRIX | 0.922 | 宏观与行业 | 0 | — | — | — | UNTESTED | Projected long-term growth rate for a company or security. |
| 1163 | `dividend_coverage_ratio_5` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of earnings to dividends paid. |
| 1164 | `time_weighted_sales_performance` | MATRIX | 0.922 | 其他 | 0 | — | — | — | UNTESTED | Sales performance weighted by time. |
| 1165 | `forecasted_quarterly_surprise_standard_deviation` | MATRIX | 0.922 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of forecasted quarterly surprises. |
| 1166 | `forecast_surprise_std_60d_lag` | MATRIX | 0.922 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of forecast surprise with a 60-day lag. |
| 1167 | `net_equity_yield` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net yield generated from equity holdings. |
| 1168 | `percent_change_free_cash_flow_value` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in free cash flow value over a period. |
| 1169 | `forward_sales_per_share` | MATRIX | 0.922 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward estimate of sales per share. |
| 1170 | `time_weighted_eps_revenue` | MATRIX | 0.922 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share weighted by time and revenue. |
| 1171 | `total_working_capital_per_share` | MATRIX | 0.921 | 其他 | 0 | — | — | — | UNTESTED | Total working capital divided by number of shares. |
| 1172 | `change_quarterly_eps_surprise_3` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in quarterly earnings per share surprise. |
| 1173 | `average_ten_year_earnings_power` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Average earnings power over the past ten years. |
| 1174 | `compound_growth_three_year_operating_margin` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Compound annual growth rate of operating margin over the past three years. |
| 1175 | `forward_dividend_yield_peg_ratio` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of forward dividend yield to price/earnings/growth. |
| 1176 | `net_asset_sales` | MATRIX | 0.921 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sales generated from net assets. |
| 1177 | `accounts_payable_to_sales_ratio_4` | MATRIX | 0.921 | 其他 | 0 | — | — | — | UNTESTED | Ratio of accounts payable to total sales. |
| 1178 | `time_weighted_book_price` | MATRIX | 0.921 | 价量与波动 | 0 | — | — | — | UNTESTED | Book price weighted by time. |
| 1179 | `price_to_earnings_growth_ratio` | MATRIX | 0.920 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of price to earnings growth. |
| 1180 | `time_weighted_eps_standardized_revenue` | MATRIX | 0.920 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share weighted by time and standardized revenue. |
| 1181 | `chg_3y_ttm_eps_version_a` | MATRIX | 0.920 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing twelve months EPS over three years, version a. |
| 1182 | `cumulative_growth_three_year_free_cash_flow` | MATRIX | 0.920 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cumulative growth of free cash flow over three years. |
| 1183 | `latest_available_sales_amount` | MATRIX | 0.920 | 其他 | 0 | — | — | — | UNTESTED | Most recent available sales figure. |
| 1184 | `trailing_weighted_cash_position` | MATRIX | 0.920 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Trailing weighted cash position for a company. |
| 1185 | `forecasted_price_to_dividend_yield` | MATRIX | 0.920 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected ratio of price to dividend yield. |
| 1186 | `forward_cash_per_share_2` | MATRIX | 0.920 | 其他 | 0 | — | — | — | UNTESTED | Projected cash per share for a future period. |
| 1187 | `mdl219_1_gtlm6ghc` | MATRIX | 0.920 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month change in long-term growth estimates. |
| 1188 | `change_six_month_long_term_growth` | MATRIX | 0.920 | 其他 | 0 | — | — | — | UNTESTED | Change in long-term growth over the past six months. |
| 1189 | `net_debt_to_ebitda_ratio_2` | MATRIX | 0.919 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of net debt to EBITDA. |
| 1190 | `year_over_year_change_roe_artificial` | MATRIX | 0.919 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on equity (artificially adjusted). |
| 1191 | `net_equity_yield_2` | MATRIX | 0.919 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net equity yield value. |
| 1192 | `trailing_weighted_ebitda_to_enterprise_value` | MATRIX | 0.919 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing weighted EBITDA to enterprise value ratio. |
| 1193 | `selling_general_admin_expense_11` | MATRIX | 0.919 | 其他 | 0 | — | — | — | UNTESTED | Selling, general, and administrative expense value. |
| 1194 | `forward_ebitda_to_enterprise_value_ratio` | MATRIX | 0.919 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of forecasted EBITDA to enterprise value. |
| 1195 | `mdl219_1_dpcapex` | MATRIX | 0.919 | 其他 | 0 | — | — | — | UNTESTED | Change in depreciation relative to capital expenditures over the last year. |
| 1196 | `sales_growth_five_years` | MATRIX | 0.919 | 其他 | 0 | — | — | — | UNTESTED | Sales growth measured over five years. |
| 1197 | `coefficient_of_return_volatility` | MATRIX | 0.919 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient measuring the volatility of returns. |
| 1198 | `year_over_year_change_roe_percent` | MATRIX | 0.919 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year percentage change in return on equity. |
| 1199 | `forward_cash_per_share` | MATRIX | 0.918 | 其他 | 0 | — | — | — | UNTESTED | Projected cash per share for a future period. |
| 1200 | `dividend_to_cashflow_ratio` | MATRIX | 0.918 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of dividends paid to cash flow generated. |
| 1201 | `sales_to_earnings_per_share_ratio` | MATRIX | 0.918 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of sales to earnings per share. |
| 1202 | `change_sga_to_sales_ratio_3` | MATRIX | 0.918 | 其他 | 0 | — | — | — | UNTESTED | Change in selling, general, and administrative expenses as a proportion of sales. |
| 1203 | `chg_3y_return_on_invested_capital` | MATRIX | 0.918 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in return on invested capital over three years. |
| 1204 | `emea_region_sales_2` | MATRIX | 0.917 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sales generated in Europe, Middle East, and Africa. |
| 1205 | `actual_return_60_months_12_month_lag` | MATRIX | 0.917 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over 60 months with a 12-month lag. |
| 1206 | `cumulative_growth_three_year_operating_margin` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cumulative growth in operating profit margin over three years. |
| 1207 | `net_cash_flow_earnings_per_share` | MATRIX | 0.917 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net cash flow earnings per share. |
| 1208 | `mdl219_1_beta` | MATRIX | 0.917 | 价量与波动 | 0 | — | — | — | UNTESTED | Beta calculated over 60 months, measuring stock volatility relative to the market. |
| 1209 | `graham_valuation_number_2` | MATRIX | 0.917 | 其他 | 0 | — | — | — | UNTESTED | Value derived from Graham's formula for conservative stock valuation. |
| 1210 | `actual_thirty_six_month_return` | MATRIX | 0.916 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return achieved over the past thirty-six months. |
| 1211 | `percent_change_three_year_free_cash_flow_2` | MATRIX | 0.915 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentage change in free cash flow over three years. |
| 1212 | `forecast_surprise_stddev_60d_lag` | MATRIX | 0.914 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of forecast surprise with a 60-day lag. |
| 1213 | `forecasted_relative_five_year_forward_eps` | MATRIX | 0.913 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted forward earnings per share relative to peers over five years. |
| 1214 | `price_book_roe_residual_2` | MATRIX | 0.913 | 盈利与财务 | 0 | — | — | — | UNTESTED | Residual value from price to book and return on equity regression. |
| 1215 | `mdl219_1_fc_rel5yfwdep` | MATRIX | 0.913 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative forward 12-month EPS-to-price ratio compared to historical averages. |
| 1216 | `earnings_torpedo_indicator_2` | MATRIX | 0.912 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator for significant negative earnings events. |
| 1217 | `capital_expenditure_to_depreciation_link` | MATRIX | 0.912 | 其他 | 0 | — | — | — | UNTESTED | Relationship between capital expenditures and depreciation. |
| 1218 | `change_alpha_thirtysix_months` | MATRIX | 0.912 | 其他 | 0 | — | — | — | UNTESTED | Change in alpha over a thirty-six month period. |
| 1219 | `mdl219_1_fc_ebop` | MATRIX | 0.912 | 价量与波动 | 0 | — | — | — | UNTESTED | Edwards-Bell-Ohlson value-to-price ratio based on valuation models. |
| 1220 | `depreciation_to_capital_expenditure_ratio` | MATRIX | 0.911 | 其他 | 0 | — | — | — | UNTESTED | Ratio of depreciation to capital expenditures. |
| 1221 | `mdl219_1_chgvolpre4y` | MATRIX | 0.911 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-year change in average trading volume. |
| 1222 | `market_beta_value` | MATRIX | 0.910 | 风险与质量 | 0 | — | — | — | UNTESTED | Beta value representing market risk exposure. |
| 1223 | `mdl219_1_alpha60m` | MATRIX | 0.910 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month alpha calculated as the intercept of a regression of stock returns against a benchmark. |
| 1224 | `twelve_week_eps_to_revenue` | MATRIX | 0.910 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share to revenue ratio over twelve weeks. |
| 1225 | `mdl219_1_rerror60m` | MATRIX | 0.909 | 其他 | 0 | — | — | — | UNTESTED | Regression error of 60-month CAPM used for trend analysis. |
| 1226 | `mdl219_1_sigma` | MATRIX | 0.909 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return volatility calculated as the standard deviation of monthly returns over the last 60 months. |
| 1227 | `mdl219_1_betasigma` | MATRIX | 0.909 | 价量与波动 | 0 | — | — | — | UNTESTED | Product of beta and sigma, combining volatility and market sensitivity. |
| 1228 | `mdl219_1_actrtn60m` | MATRIX | 0.908 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month active return representing the percent change in stock price. |
| 1229 | `forecasted_earnings_before_operations_per_share` | MATRIX | 0.908 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted earnings before operations per share. |
| 1230 | `twelve_week_eps_standard_deviation_revenue` | MATRIX | 0.908 | 盈利与财务 | 0 | — | — | — | UNTESTED | Standard deviation of EPS over twelve weeks relative to revenue. |
| 1231 | `mdl219_1_cashp` | MATRIX | 0.908 | 价量与波动 | 0 | — | — | — | UNTESTED | Cash-to-price ratio calculated as cash per share divided by stock price. |
| 1232 | `mdl219_1_aspanratio` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | Attention span ratio measuring operating assets minus liabilities scaled by total assets. |
| 1233 | `mdl219_1_cashsev` | MATRIX | 0.907 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-enterprise value ratio representing total cash divided by enterprise value. |
| 1234 | `north_america_sales_2` | MATRIX | 0.907 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sales generated in North America. |
| 1235 | `mdl219_1_chgnoa` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net operating assets scaled by total assets. |
| 1236 | `mdl219_1_pctchg3yfcf` | MATRIX | 0.907 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year growth in free cash flow per share calculated as a percentage. |
| 1237 | `mdl219_1_cashsale` | MATRIX | 0.907 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-sales ratio calculated as average cash divided by sales. |
| 1238 | `mdl219_1_pca` | MATRIX | 0.906 | 其他 | 0 | — | — | — | UNTESTED | Average collection period calculated as accounts receivable times 365 divided by sales. |
| 1239 | `mdl219_1_rel5ybp` | MATRIX | 0.906 | 其他 | 0 | — | — | — | UNTESTED | 5-year relative book-to-market ratio compared to historical averages. |
| 1240 | `relative_five_year_book_value_per_share` | MATRIX | 0.906 | 其他 | 0 | — | — | — | UNTESTED | Book value per share relative to peers over five years. |
| 1241 | `mdl219_1_rel5yep` | MATRIX | 0.906 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative EPS-to-price ratio compared to historical averages. |
| 1242 | `relative_five_year_earnings_per_share` | MATRIX | 0.906 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings per share relative to peers over five years. |
| 1243 | `mdl219_1_cashburnrate` | MATRIX | 0.906 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash burn rate calculated as negative operating and investment cash flows divided by cash holdings. |
| 1244 | `relative_five_year_sales_per_share` | MATRIX | 0.906 | 其他 | 0 | — | — | — | UNTESTED | Relative value of sales per share over five years. |
| 1245 | `relative_five_year_free_cash_flow_per_share` | MATRIX | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow per share relative to peers or market over the past five years. |
| 1246 | `relative_five_year_operating_cash_flow_per_share` | MATRIX | 0.905 | 盈利与财务 | 0 | — | — | — | UNTESTED | Relative value of operating cash flow per share over five years. |
| 1247 | `mdl219_1_rel5ysp` | MATRIX | 0.905 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative sales-to-price ratio compared to historical averages. |
| 1248 | `mdl219_1_netcashp` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net cash-to-price ratio calculated as cash minus debt divided by market price. |
| 1249 | `mdl219_1_rau` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in accounts receivable scaled by total assets. |
| 1250 | `long_term_growth_projection_3` | MATRIX | 0.904 | 其他 | 0 | — | — | — | UNTESTED | Projection of long-term growth for the company. |
| 1251 | `forecasted_earnings_growth_potential` | MATRIX | 0.904 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected potential for earnings growth based on forecasts. |
| 1252 | `mdl219_1_chgars` | MATRIX | 0.903 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in accounts receivable as a percentage of sales. |
| 1253 | `mdl219_1_salerec` | MATRIX | 0.903 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing 12-month sales relative to accounts receivable. |
| 1254 | `capex_depreciation_linkage_3` | MATRIX | 0.902 | 其他 | 0 | — | — | — | UNTESTED | Linkage between capital expenditures and depreciation. |
| 1255 | `variance_residual_return_2` | MATRIX | 0.902 | 价量与波动 | 0 | — | — | — | UNTESTED | Variance of residual returns. |
| 1256 | `change_volume_prior_four_years` | MATRIX | 0.902 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in trading volume compared to four years prior. |
| 1257 | `mdl219_1_perg` | MATRIX | 0.900 | 价量与波动 | 0 | — | — | — | UNTESTED | Risk-adjusted PEG ratio calculated as price divided by forward EPS and scaled by growth rate. |
| 1258 | `relative_five_year_cash_flow_per_share_2` | MATRIX | 0.900 | 盈利与财务 | 0 | — | — | — | UNTESTED | Relative value of cash flow per share over five years. |
| 1259 | `relative_five_year_ebitda_per_share` | MATRIX | 0.899 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA per share relative to peers or market over the past five years. |
| 1260 | `cash_per_share_2` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Amount of cash held per share outstanding. |
| 1261 | `cash_to_enterprise_value_ratio_6` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Ratio of cash to enterprise value. |
| 1262 | `investment_in_assets` | MATRIX | 0.898 | 盈利与财务 | 0 | — | — | — | UNTESTED | Amount invested in assets by a company. |
| 1263 | `asset_span_ratio` | MATRIX | 0.898 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio measuring the span of assets. |
| 1264 | `average_collection_period_3` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Average time taken to collect receivables. |
| 1265 | `cash_burn_rate_value` | MATRIX | 0.898 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rate at which cash is spent over a period. |
| 1266 | `cash_to_sales_ratio_5` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Ratio of cash to sales. |
| 1267 | `change_net_operating_assets_4` | MATRIX | 0.898 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net operating assets over a period. |
| 1268 | `mdl219_1_divcov` | MATRIX | 0.898 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend coverage ratio calculated as operating earnings divided by dividends. |
| 1269 | `depreciation_to_capex_ratio_3` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Ratio of depreciation expense to capital expenditures. |
| 1270 | `beta_standard_deviation_2` | MATRIX | 0.898 | 风险与质量 | 0 | — | — | — | UNTESTED | Standard deviation of the stock's beta, indicating variability in market sensitivity. |
| 1271 | `net_cash_per_share` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Net cash available per share. |
| 1272 | `sixty_month_return_forecast_error` | MATRIX | 0.898 | 价量与波动 | 0 | — | — | — | UNTESTED | Forecast error in returns over a sixty-month period. |
| 1273 | `standard_deviation_value_3` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of a financial metric. |
| 1274 | `alpha_sixty_months` | MATRIX | 0.898 | 其他 | 0 | — | — | — | UNTESTED | Alpha value calculated over sixty months. |
| 1275 | `change_inventory_average_assets` | MATRIX | 0.898 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in inventory relative to average assets. |
| 1276 | `unexpected_announcement_return` | MATRIX | 0.897 | 价量与波动 | 0 | — | — | — | UNTESTED | Return associated with unexpected company announcements. |
| 1277 | `forecast_dividend_yield_peg` | MATRIX | 0.897 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forecasted dividend yield price/earnings to growth ratio. |
| 1278 | `sales_to_receivables_ratio` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | Ratio of sales to accounts receivable. |
| 1279 | `change_in_income_statement_metric` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | Change in a key income statement metric over time. |
| 1280 | `actual_return_sixty_months` | MATRIX | 0.897 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return achieved over sixty months. |
| 1281 | `change_accounts_receivable` | MATRIX | 0.897 | 其他 | 0 | — | — | — | UNTESTED | Change in accounts receivable over a period. |
| 1282 | `distribution_metric` | MATRIX | 0.896 | 其他 | 0 | — | — | — | UNTESTED | Metric representing the statistical distribution of a financial variable. |
| 1283 | `year_over_year_change_gross_profit_margin` | MATRIX | 0.895 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in gross profit margin. |
| 1284 | `sales_gross_profit_margin` | MATRIX | 0.895 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross profit margin derived from sales. |
| 1285 | `cash_per_share_value_4` | MATRIX | 0.894 | 其他 | 0 | — | — | — | UNTESTED | Amount of cash held per share. |
| 1286 | `investment_to_assets_ratio` | MATRIX | 0.894 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of investments to total assets. |
| 1287 | `cash_to_enterprise_value_3` | MATRIX | 0.894 | 其他 | 0 | — | — | — | UNTESTED | Ratio of cash to enterprise value. |
| 1288 | `gross_profit_margin_value` | MATRIX | 0.894 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross profit margin as a percentage. |
| 1289 | `mdl219_1_ydp_cf` | MATRIX | 0.894 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted dividend yield based on payout ratio and forward EPS estimates. |
| 1290 | `mdl219_1_sighc` | MATRIX | 0.894 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in inventory as a percentage of sales. |
| 1291 | `asset_span_ratio_2` | MATRIX | 0.894 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio measuring the span or spread of assets. |
| 1292 | `cash_to_sales_ratio_6` | MATRIX | 0.893 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Ratio of cash holdings to total sales. |
| 1293 | `average_collection_period_4` | MATRIX | 0.893 | 其他 | 0 | — | — | — | UNTESTED | Average number of days to collect receivables. |
| 1294 | `selling_general_administrative_expense` | MATRIX | 0.893 | 其他 | 0 | — | — | — | UNTESTED | Total selling, general, and administrative expenses. |
| 1295 | `mdl219_1_rel5yocfp` | MATRIX | 0.893 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative operating cash flow-to-price ratio compared to historical averages. |
| 1296 | `change_net_operating_assets_5` | MATRIX | 0.893 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net operating assets. |
| 1297 | `mdl219_1_rel5yfcfp` | MATRIX | 0.893 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative free cash flow-to-price ratio compared to historical averages. |
| 1298 | `mdl219_1_varresirtn` | MATRIX | 0.893 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month residual return variance calculated as the variance of monthly residual returns. |
| 1299 | `unusual_inventory_metric` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Metric for unusual inventory levels or changes. |
| 1300 | `cash_burn_rate_ratio_3` | MATRIX | 0.892 | 宏观与行业 | 0 | — | — | — | UNTESTED | Rate at which a company is using up its cash reserves. |
| 1301 | `change_inventory_avg_assets_2` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in inventory relative to average assets. |
| 1302 | `one_year_change_gross_profit_asset` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in gross profit to asset ratio over one year. |
| 1303 | `unusual_accounts_receivable_ratio` | MATRIX | 0.891 | 其他 | 0 | — | — | — | UNTESTED | Ratio indicating abnormal accounts receivable levels. |
| 1304 | `baltic_dry_index` | MATRIX | 0.891 | 宏观与行业 | 0 | — | — | — | UNTESTED | Baltic Dry Index, a measure of shipping rates for dry bulk cargo. |
| 1305 | `accounts_payable_to_sales_ratio_5` | MATRIX | 0.891 | 其他 | 0 | — | — | — | UNTESTED | Ratio of accounts payable to total sales. |
| 1306 | `change_accounts_receivable_sales_2` | MATRIX | 0.891 | 其他 | 0 | — | — | — | UNTESTED | Change in accounts receivable as a percentage of sales. |
| 1307 | `net_cash_per_share_2` | MATRIX | 0.891 | 其他 | 0 | — | — | — | UNTESTED | Net cash available per share. |
| 1308 | `change_inventory_sales_2` | MATRIX | 0.891 | 其他 | 0 | — | — | — | UNTESTED | Change in inventory relative to sales. |
| 1309 | `mdl219_1_invast` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inventory-to-total assets ratio calculated as inventory divided by total assets. |
| 1310 | `sales_to_receivables_ratio_2` | MATRIX | 0.890 | 其他 | 0 | — | — | — | UNTESTED | Ratio of sales to accounts receivable. |
| 1311 | `mdl219_1_rel5yebitdap` | MATRIX | 0.889 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative EBITDA-to-price ratio compared to historical averages. |
| 1312 | `mdl219_1_salegpm` | MATRIX | 0.889 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in quarterly sales relative to gross profit margin over the last year. |
| 1313 | `three_year_change_gross_profit_assets` | MATRIX | 0.889 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in gross profit to assets ratio over three years. |
| 1314 | `dividend_to_gross_profit_ratio_3` | MATRIX | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of dividends paid to gross profit. |
| 1315 | `three_year_change_gross_profit_margin_3` | MATRIX | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in gross profit margin over three years. |
| 1316 | `mdl219_1_yoychggpm` | MATRIX | 0.888 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in gross profit margin. |
| 1317 | `gross_profit_margin_percent` | MATRIX | 0.886 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross profit margin expressed as a percentage. |
| 1318 | `gross_profitability_asset` | MATRIX | 0.884 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross profitability relative to assets. |
| 1319 | `latest_annual_sales_value` | MATRIX | 0.884 | 其他 | 0 | — | — | — | UNTESTED | Most recent annual sales value reported by the company. |
| 1320 | `cumulative_growth_3y_gross_profit_margin` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cumulative growth in gross profit margin over three years. |
| 1321 | `relative_five_year_dividend_payout` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend payout relative to peers or market over the past five years. |
| 1322 | `year_over_year_change_gross_profit_margin_2` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in gross profit margin. |
| 1323 | `sales_to_gross_profit_margin` | MATRIX | 0.883 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross profit margin calculated from sales. |
| 1324 | `mdl219_1_rel5ycfp` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative cash flow-to-price ratio compared to historical averages. |
| 1325 | `actual_return_60m_12lag` | MATRIX | 0.882 | 价量与波动 | 0 | — | — | — | UNTESTED | Actual return over 60 months with a 12-month lag. |
| 1326 | `debt_maturity_metric` | MATRIX | 0.882 | 盈利与财务 | 0 | — | — | — | UNTESTED | Metric representing the maturity profile of debt. |
| 1327 | `six_month_change_long_term_growth_4` | MATRIX | 0.881 | 宏观与行业 | 0 | — | — | — | UNTESTED | Six-month change in long-term growth rate. |
| 1328 | `one_year_change_gross_profit_to_assets_3` | MATRIX | 0.880 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in gross profit to assets ratio over one year. |
| 1329 | `price_to_earnings_growth_ratio_2` | MATRIX | 0.880 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of share price to earnings growth rate. |
| 1330 | `dividend_coverage_ratio_6` | MATRIX | 0.879 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of earnings to dividends paid. |
| 1331 | `change_sga_to_sales_ratio_4` | MATRIX | 0.878 | 其他 | 0 | — | — | — | UNTESTED | Change in the ratio of selling, general, and administrative expenses to sales. |
| 1332 | `dividend_five_year_growth` | MATRIX | 0.876 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth rate of dividends over five years. |
| 1333 | `forward_price_dividend_yield_ratio` | MATRIX | 0.876 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking price to dividend yield ratio. |
| 1334 | `mdl219_1_vniu` | MATRIX | 0.873 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in inventory scaled by total assets. |
| 1335 | `mdl219_1_ags` | MATRIX | 0.873 | 其他 | 0 | — | — | — | UNTESTED | SG&A expenses-to-sales ratio calculated as selling, general, and administrative expenses divided by sales. |
| 1336 | `unusual_inventory_ratio` | MATRIX | 0.872 | 其他 | 0 | — | — | — | UNTESTED | Ratio indicating abnormal or unusual inventory levels relative to norms. |
| 1337 | `working_capital_accruals_metric` | MATRIX | 0.871 | 盈利与财务 | 0 | — | — | — | UNTESTED | Measure of accruals in working capital. |
| 1338 | `three_year_change_gross_profit_assets_2` | MATRIX | 0.868 | 盈利与财务 | 0 | — | — | — | UNTESTED | Three-year change in the ratio of gross profit to assets. |
| 1339 | `mdl219_1_rel5ydivp` | MATRIX | 0.868 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative dividend yield compared to historical averages. |
| 1340 | `mdl219_1_div5yg` | MATRIX | 0.866 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year dividend growth rate measuring compounded annual growth in dividends. |
| 1341 | `three_year_change_gross_profit_margin_4` | MATRIX | 0.866 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in gross profit margin over three years. |
| 1342 | `mdl219_1_divcf` | MATRIX | 0.863 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividends-to-cash flow ratio calculated over trailing 12 months. |
| 1343 | `compound_growth_three_year_gross_profit_margin` | MATRIX | 0.862 | 盈利与财务 | 0 | — | — | — | UNTESTED | Compound annual growth rate of gross profit margin over the past three years. |
| 1344 | `mdl219_1_chgsgasale` | MATRIX | 0.859 | 其他 | 0 | — | — | — | UNTESTED | Change in SG&A expenses relative to sales over the last year. |
| 1345 | `dividend_to_gross_profit_ratio_4` | MATRIX | 0.857 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of dividend payments to gross profit. |
| 1346 | `asset_composition_ratio_3` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio indicating the composition of assets. |
| 1347 | `net_non_asset_per_share` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net non-asset value per share. |
| 1348 | `cash_to_liabilities_ratio_3` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash to total liabilities. |
| 1349 | `price_to_current_liabilities_ratio` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of price to current liabilities. |
| 1350 | `current_ratio_6` | MATRIX | 0.854 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current assets divided by current liabilities. |
| 1351 | `quick_ratio_value_4` | MATRIX | 0.854 | 价量与波动 | 0 | — | — | — | UNTESTED | Quick ratio, a measure of liquidity. |
| 1352 | `liquidity_flow_ratio` | MATRIX | 0.853 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio measuring liquidity flow within the company. |
| 1353 | `operating_cashflow_ratio_2` | MATRIX | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of operating cash flow to another financial metric. |
| 1354 | `working_capital_to_assets_2` | MATRIX | 0.853 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of working capital to total assets. |
| 1355 | `short_term_working_capital` | MATRIX | 0.853 | 其他 | 0 | — | — | — | UNTESTED | Short-term working capital value. |
| 1356 | `profitability_index_net_operating_assets` | MATRIX | 0.852 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability index based on net operating assets. |
| 1357 | `year_over_year_change_current_ratio_3` | MATRIX | 0.852 | 价量与波动 | 0 | — | — | — | UNTESTED | Year-over-year change in the current ratio, a liquidity metric. |
| 1358 | `altman_z_score_7` | MATRIX | 0.852 | 风险与质量 | 0 | — | — | — | UNTESTED | Altman Z-score, a measure of bankruptcy risk. |
| 1359 | `asset_quality_index_value` | MATRIX | 0.852 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset quality index value. |
| 1360 | `change_receivables_cast_metric` | MATRIX | 0.852 | 其他 | 0 | — | — | — | UNTESTED | Change in receivables as measured by a specific metric. |
| 1361 | `ohlson_o_score_3` | MATRIX | 0.852 | 风险与质量 | 0 | — | — | — | UNTESTED | Ohlson O-score, a measure of bankruptcy risk. |
| 1362 | `average_purchase_price` | MATRIX | 0.849 | 价量与波动 | 0 | — | — | — | UNTESTED | Average price paid for purchases. |
| 1363 | `cash_and_cash_equivalents_6` | MATRIX | 0.849 | 其他 | 0 | — | — | — | UNTESTED | Total cash and cash equivalents available. |
| 1364 | `dividend_to_cash_flow_ratio` | MATRIX | 0.848 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of dividend payments to cash flow. |
| 1365 | `unexpected_announcement_profit` | MATRIX | 0.846 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profit associated with unexpected company announcements. |
| 1366 | `cost_of_goods_sold_to_inventory_ratio` | MATRIX | 0.846 | 其他 | 0 | — | — | — | UNTESTED | Ratio of cost of goods sold to inventory. |
| 1367 | `bulk_dry_index_value` | MATRIX | 0.845 | 宏观与行业 | 0 | — | — | — | UNTESTED | Bulk Dry Index value representing shipping rates. |
| 1368 | `inventory_turnover_ratio_14` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio indicating how often inventory is sold and replaced over a period. |
| 1369 | `earnings_torpedo_indicator_3` | MATRIX | 0.840 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator of significant negative earnings events. |
| 1370 | `industry_relative_recommendation_delta` | MATRIX | 0.837 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in analyst recommendation relative to industry peers. |
| 1371 | `working_capital_to_inventory_ratio_2` | MATRIX | 0.830 | 其他 | 0 | — | — | — | UNTESTED | Ratio of working capital to inventory. |
| 1372 | `mdl219_1_astcomp` | MATRIX | 0.815 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset composition ratio representing current assets divided by total assets. |
| 1373 | `mdl219_1_cashratio` | MATRIX | 0.815 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash-to-current liabilities ratio measuring liquidity. |
| 1374 | `mdl219_1_ocfratio` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow ratio calculated as cash flow divided by current liabilities. |
| 1375 | `mdl219_1_pcurlia` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities-to-price ratio calculated as liabilities per share divided by stock price. |
| 1376 | `mdl219_1_cashratiofixed` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash ratio calculated as cash and equivalents divided by current liabilities. |
| 1377 | `mdl219_1_nnastp` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net net current assets-to-price ratio calculated as current assets minus liabilities divided by price. |
| 1378 | `mdl219_1_curratio` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current ratio calculated as current assets divided by current liabilities. |
| 1379 | `mdl219_1_rq` | MATRIX | 0.813 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick ratio calculated as current assets minus inventory divided by current liabilities. |
| 1380 | `mdl219_1_flowratio` | MATRIX | 0.812 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flow ratio measuring liquidity as current assets minus cash divided by liabilities minus debt. |
| 1381 | `mdl219_1_wcast` | MATRIX | 0.811 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital-to-total assets ratio calculated as average working capital divided by average total assets. |
| 1382 | `mdl219_1_yoychgcr` | MATRIX | 0.810 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in current ratio. |
| 1383 | `mdl219_1_cws` | MATRIX | 0.810 | 其他 | 0 | — | — | — | UNTESTED | Working capital-to-sales ratio calculated as average working capital divided by trailing 12-month sales. |
| 1384 | `mdl219_1_pinoa` | MATRIX | 0.810 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax return on net operating assets calculated as operating income divided by net operating assets. |
| 1385 | `mdl219_1_chgreccast` | MATRIX | 0.809 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accounts receivable relative to current assets. |
| 1386 | `mdl219_1_iqa` | MATRIX | 0.808 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset quality index measuring changes in the ratio of non-current assets to total assets. |
| 1387 | `mdl219_1_ppa` | MATRIX | 0.806 | 其他 | 0 | — | — | — | UNTESTED | Average payable period calculated as accounts payable times 365 divided by cost of goods sold. |
| 1388 | `mdl219_1_otvni` | MATRIX | 0.805 | 价量与波动 | 0 | — | — | — | UNTESTED | Inventory turnover ratio calculated as cost of goods sold divided by average inventory. |
| 1389 | `mdl219_1_idb` | MATRIX | 0.805 | 其他 | 0 | — | — | — | UNTESTED | Basic defensive interval measuring the number of days a company can cover expenses using cash and receivables. |
| 1390 | `mdl219_1_cashc` | MATRIX | 0.804 | 其他 | 0 | — | — | — | UNTESTED | Cash cycle calculated as inventory days plus collection days minus payable days. |
| 1391 | `mdl219_1_pau` | MATRIX | 0.802 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in accounts payable scaled by total assets. |
| 1392 | `mdl219_1_cogsinvt` | MATRIX | 0.800 | 其他 | 0 | — | — | — | UNTESTED | Change in cost of goods sold relative to inventory levels. |
| 1393 | `mdl219_2_nlmktcap` | MATRIX | 0.799 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of market capitalization used for normalization for the second module. |
| 1394 | `mdl219_2_nlprice` | MATRIX | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | Natural logarithm of closing price used for normalization for the second module. |
| 1395 | `mdl219_2_volto` | MATRIX | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | Trading turnover ratio calculated as monthly trading volume divided by shares outstanding for the second module. |
| 1396 | `mdl219_2_milliq` | MATRIX | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock illiquidity calculated as the monthly average of daily absolute return to daily dollar trading volume for the second module. |
| 1397 | `mdl219_2_actrtn1m` | MATRIX | 0.799 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-month active return representing the percent change in stock price for the second module. |
| 1398 | `research_development_to_sales_ratio` | MATRIX | 0.798 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Ratio of research and development expenses to sales. |
| 1399 | `mdl219_2_actrtn2m` | MATRIX | 0.798 | 价量与波动 | 0 | — | — | — | UNTESTED | 2-month active return representing the percent change in stock price for the second module. |
| 1400 | `asset_composition_ratio_4` | MATRIX | 0.797 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio describing the composition of assets. |
| 1401 | `mdl219_2_visiratio` | MATRIX | 0.797 | 价量与波动 | 0 | — | — | — | UNTESTED | Visibility ratio calculated as the most recent daily trading volume divided by the average daily trading volume over the last 50 days for th |
| 1402 | `price_to_current_liabilities_ratio_2` | MATRIX | 0.797 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of share price to current liabilities. |
| 1403 | `cash_to_liabilities_ratio_4` | MATRIX | 0.797 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash holdings to total liabilities. |
| 1404 | `net_non_asset_per_share_2` | MATRIX | 0.797 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net non-asset value per share. |
| 1405 | `operating_cash_flow_ratio_5` | MATRIX | 0.797 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of operating cash flow to a reference value. |
| 1406 | `mdl219_2_actrtn3m` | MATRIX | 0.797 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-month active return representing the percent change in stock price for the second module. |
| 1407 | `mdl219_2_cvvolp20d` | MATRIX | 0.797 | 价量与波动 | 0 | — | — | — | UNTESTED | 20-day volume volatility relative to price volatility for the second module. |
| 1408 | `mdl219_2_indrelrtn4w_` | MATRIX | 0.797 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-week industry-relative return adjusted for industry averages for the second module. |
| 1409 | `mdl219_2_aor` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on assets calculated as net income divided by average total assets for the second module. |
| 1410 | `mdl219_2_nlassets` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Natural logarithm of total assets used for normalization for the second module. |
| 1411 | `mdl219_2_stockrating` | MATRIX | 0.796 | 修正与预期 | 0 | — | — | — | UNTESTED | Street consensus rating calculated as the average analyst recommendation for the second module. |
| 1412 | `mdl219_2_equityto` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity turnover ratio calculated as sales divided by average book equity for the second module. |
| 1413 | `mdl219_2_astto` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset turnover ratio calculated as sales divided by total assets for the second module. |
| 1414 | `mdl219_2_noato` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net operating asset turnover calculated as sales divided by average net operating assets for the second module. |
| 1415 | `mdl219_2_pvan` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net asset value-to-price ratio calculated as book value of net assets divided by price for the second module. |
| 1416 | `mdl219_2_booklev` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Book leverage calculated as total assets divided by book equity for the second module. |
| 1417 | `current_ratio_value_4` | MATRIX | 0.796 | 价量与波动 | 0 | — | — | — | UNTESTED | Current ratio, a measure of liquidity. |
| 1418 | `mdl219_2_cfita` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow from investment-to-assets ratio calculated over trailing 12 months for the second module. |
| 1419 | `mdl219_2_ocfast` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow-to-assets ratio calculated over trailing 12 months for the second module. |
| 1420 | `mdl219_2_past` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-total assets ratio calculated as market price divided by total assets per share for the second module. |
| 1421 | `quick_ratio_value_5` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick ratio measuring liquidity using most liquid assets. |
| 1422 | `mdl219_2_ed` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Debt-to-equity ratio measuring financial leverage for the second module. |
| 1423 | `mdl219_2_pb` | MATRIX | 0.796 | 价量与波动 | 0 | — | — | — | UNTESTED | Book-to-market ratio calculated as book value divided by market price for the second module. |
| 1424 | `mdl219_2_ttmaccu` | MATRIX | 0.796 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accounting accruals calculated as the difference between trailing 12-month net income and operating cash flow for the second module. |
| 1425 | `mdl219_2_gspea2y_cf` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | 2-year projected EPS growth based on analyst forecasts for the second module. |
| 1426 | `mdl219_2_mktcappera` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Market capitalization per analyst calculated as month-end market cap divided by the number of analysts for the second module. |
| 1427 | `mdl219_2_ocfroi` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow return on invested capital calculated over trailing 12 months for the second module. |
| 1428 | `mdl219_2_pe_wt` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Time-weighted earnings yield calculated as the weighted average of reported EPS and forward EPS divided by price for the second module. |
| 1429 | `mdl219_2_pedwf_cf` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward earnings yield based on consensus estimates divided by price for the second module. |
| 1430 | `mdl219_2_yoychgda` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in leverage calculated as total liabilities as a percentage of assets for the second module. |
| 1431 | `mdl219_2_apemtt` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month EPS after extraordinary items-to-price ratio calculated as EPS divided by price for the second module. |
| 1432 | `mdl219_2_bpemtt` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month EPS before extraordinary items-to-price ratio calculated as EPS divided by price for the second module. |
| 1433 | `mdl219_2_fc_estep` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Leading 12-month median earnings yield calculated as forward EPS divided by price for the second module. |
| 1434 | `mdl219_2_pqipmtt` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month pretax income-to-price ratio calculated as pretax income per share divided by price for the second module. |
| 1435 | `cash_flow_ratio_value` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of cash flow to a reference value. |
| 1436 | `mdl219_2_psmtt` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month sales-to-price ratio calculated as sales per share divided by price for the second module. |
| 1437 | `mdl219_2_curindocfta_` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative operating cash flow-to-assets ratio adjusted for industry averages for the second module. |
| 1438 | `mdl219_2_pfgmtt` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month growth flow-to-price ratio calculated as growth flow per share divided by price for the second module. |
| 1439 | `mdl219_2_ttmsaleev` | MATRIX | 0.795 | 其他 | 0 | — | — | — | UNTESTED | Trailing 12-month sales-to-enterprise value ratio calculated as sales divided by enterprise value for the second module. |
| 1440 | `mdl219_2_fc_numest` | MATRIX | 0.795 | 修正与预期 | 0 | — | — | — | UNTESTED | Number of analysts providing earnings estimates for FY1 for the second module. |
| 1441 | `mdl219_2_curindbp_` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative book-to-price ratio adjusted for industry averages for the second module. |
| 1442 | `mdl219_2_pd09erpvc` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Coefficient of variation of prior 90-day closing prices for the second module. |
| 1443 | `mdl219_2_skew90cortn` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-day daily excess returns calculated as the asymmetry of daily excess price returns for the second module. |
| 1444 | `mdl219_2_skew90drtn` | MATRIX | 0.795 | 价量与波动 | 0 | — | — | — | UNTESTED | Skewness of 90-day daily returns calculated as the asymmetry of daily price returns for the second module. |
| 1445 | `mdl219_2_speghc` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in EPS scaled by total assets for the second module. |
| 1446 | `mdl219_2_yoychgroa` | MATRIX | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in return on assets for the second module. |
| 1447 | `mdl219_2_fc_numrevy1` | MATRIX | 0.794 | 修正与预期 | 0 | — | — | — | UNTESTED | Net number of FY1 analyst forecast revisions (raised minus lowered) within a month for the second module. |
| 1448 | `mdl219_2_netdebt` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net debt ratio calculated as net debt divided by the sum of net debt, preferred stock, and common stock for the second module. |
| 1449 | `mdl219_2_pfcomtt` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month operating cash flow-to-price ratio calculated as operating cash flow per share divided by price for the second module. |
| 1450 | `mdl219_2_curindep_` | MATRIX | 0.794 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative EPS-to-price ratio adjusted for industry averages for the second module. |
| 1451 | `mdl219_2_pfcfmtt` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-price ratio calculated over trailing 12 months for the second module. |
| 1452 | `altman_z_score_8` | MATRIX | 0.794 | 风险与质量 | 0 | — | — | — | UNTESTED | Altman Z-score, a measure of bankruptcy risk. |
| 1453 | `mdl219_2_fcfroi` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow return on invested capital calculated over trailing 12 months for the second module. |
| 1454 | `mdl219_2_high52w` | MATRIX | 0.794 | 价量与波动 | 0 | — | — | — | UNTESTED | 52-week high calculated as the highest monthly closing price over the past year for the second module. |
| 1455 | `mdl219_2_pctchgastto` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in asset turnover ratio calculated as a percentage for the second module. |
| 1456 | `mdl219_2_fc_curindfwdep_` | MATRIX | 0.794 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative forward 12-month EPS-to-price ratio adjusted for industry averages for the second module. |
| 1457 | `mdl219_2_volpre6m` | MATRIX | 0.794 | 价量与波动 | 0 | — | — | — | UNTESTED | Average trading volume over the preceding 6 months calculated as the moving average of monthly turnover for the second module. |
| 1458 | `mdl219_2_curindsp_` | MATRIX | 0.794 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-relative sales-to-price ratio adjusted for industry averages for the second module. |
| 1459 | `mdl219_2_mpn` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net profit margin calculated as net income divided by sales for the second module. |
| 1460 | `mdl219_2_pctabv260low` | MATRIX | 0.794 | 价量与波动 | 0 | — | — | — | UNTESTED | Percent above the lowest trading price in the last 260 days for the second module. |
| 1461 | `mdl219_2_fcoghc` | MATRIX | 0.794 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating cash flow scaled by total assets for the second module. |
| 1462 | `mdl219_2_capexast` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital expenditure-to-assets ratio measuring investment intensity for the second module. |
| 1463 | `mdl219_2_curindocfp_` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative operating cash flow-to-price ratio adjusted for industry averages for the second module. |
| 1464 | `mdl219_2_curindfcfp_` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative free cash flow-to-price ratio adjusted for industry averages for the second module. |
| 1465 | `mdl219_2_ocfmargin` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow margin calculated as operating cash flow divided by sales for the second module. |
| 1466 | `mdl219_2_yoychgaa` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accruals-to-assets ratio for the second module. |
| 1467 | `mdl219_2_fcfsale` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-sales ratio calculated over trailing 12 months for the second module. |
| 1468 | `mdl219_2_nlsales` | MATRIX | 0.793 | 其他 | 0 | — | — | — | UNTESTED | Natural logarithm of trailing 12-month sales used for normalization for the second module. |
| 1469 | `mdl219_2_pspeghc` | MATRIX | 0.793 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year change in EPS scaled by price for the second module. |
| 1470 | `working_capital_assets` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total assets classified as working capital. |
| 1471 | `mdl219_2_fcfghc` | MATRIX | 0.793 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow scaled by total assets for the second module. |
| 1472 | `mdl219_2_ttmcapexp` | MATRIX | 0.793 | 价量与波动 | 0 | — | — | — | UNTESTED | Trailing 12-month capital expenditures-to-price ratio calculated as capital expenditures per share divided by price for the second module. |
| 1473 | `mdl219_2_gear` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital gearing ratio calculated as long-term debt divided by total assets minus current liabilities for the second module. |
| 1474 | `mdl219_2_pctchgqtrast` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in total assets calculated as a percentage for the second module. |
| 1475 | `short_term_working_capital_2` | MATRIX | 0.792 | 其他 | 0 | — | — | — | UNTESTED | Short-term working capital value. |
| 1476 | `year_over_year_change_current_ratio_4` | MATRIX | 0.792 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in current ratio. |
| 1477 | `mdl219_2_fcfequity` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow to equity calculated as trailing 12-month free cash flow divided by average book equity for the second module. |
| 1478 | `mdl219_2_vefcfmtt` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-enterprise value ratio calculated over trailing 12 months for the second module. |
| 1479 | `mdl219_2_vesspem21f_cf` | MATRIX | 0.792 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward EPS-to-enterprise value ratio based on consensus estimates for the second module. |
| 1480 | `mdl219_2_w62isr` | MATRIX | 0.792 | 价量与波动 | 0 | — | — | — | UNTESTED | 26-week relative price strength calculated as the most recent weekly closing price divided by the price 26 weeks ago for the second module. |
| 1481 | `ohlson_o_score_4` | MATRIX | 0.792 | 风险与质量 | 0 | — | — | — | UNTESTED | Ohlson O-score, a bankruptcy risk metric. |
| 1482 | `change_receivables_current_assets` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in receivables as a proportion of current assets. |
| 1483 | `mdl219_2_aoer` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Retained earnings-to-total assets ratio calculated as cumulative retained earnings divided by total assets for the second module. |
| 1484 | `mdl219_2_capexsale` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital expenditure-to-sales ratio measuring investment relative to revenue for the second module. |
| 1485 | `mdl219_2_mktlev` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market leverage calculated as market value plus book debt divided by market value for the second module. |
| 1486 | `mdl219_2_fc_rev3y1` | MATRIX | 0.792 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY1 EPS forecasts scaled by price for the second module. |
| 1487 | `mdl219_2_fc_rev3y2` | MATRIX | 0.792 | 修正与预期 | 0 | — | — | — | UNTESTED | 3-month revision in FY2 EPS forecasts scaled by price for the second module. |
| 1488 | `mdl219_2_fixastto` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fixed asset turnover ratio calculated as sales divided by fixed assets for the second module. |
| 1489 | `profitability_index_net_operating_assets_2` | MATRIX | 0.792 | 盈利与财务 | 0 | — | — | — | UNTESTED | Profitability index based on net operating assets. |
| 1490 | `mdl219_2_totalsaleg` | MATRIX | 0.791 | 宏观与行业 | 0 | — | — | — | UNTESTED | Yearly trailing 12-month total sales growth rate calculated as a percentage change for the second module. |
| 1491 | `asset_quality_index_value_2` | MATRIX | 0.791 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset quality index measuring proportion of non-current assets. |
| 1492 | `mdl219_2_actrtn6m` | MATRIX | 0.791 | 价量与波动 | 0 | — | — | — | UNTESTED | 6-month active return representing the percent change in stock price for the second module. |
| 1493 | `mdl219_2_lagegp` | MATRIX | 0.791 | 其他 | 0 | — | — | — | UNTESTED | Lagged inverse PEG ratio calculated using trailing 12-month EPS and sales growth for the second module. |
| 1494 | `mdl219_2_cfroi` | MATRIX | 0.790 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow return on invested capital calculated over trailing 12 months for the second module. |
| 1495 | `mdl219_2_pfcoghc` | MATRIX | 0.790 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating cash flow per share scaled by price for the second module. |
| 1496 | `inventory_turnover_ratio_15` | MATRIX | 0.790 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of cost of goods sold to average inventory. |
| 1497 | `mdl219_2_pfcfghc` | MATRIX | 0.790 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow per share scaled by price for the second module. |
| 1498 | `mdl219_2_lfd` | MATRIX | 0.790 | 其他 | 0 | — | — | — | UNTESTED | Financial leverage calculated as pretax income plus interest expense divided by pretax income for the second module. |
| 1499 | `mdl219_2_pfcmtt` | MATRIX | 0.790 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month cash flow-to-price ratio calculated as cash flow per share divided by price for the second module. |
| 1500 | `mdl219_2_roic` | MATRIX | 0.790 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on invested capital calculated as net income and interest expenses divided by invested capital for the second module. |
| 1501 | `accounts_payable_period` | MATRIX | 0.789 | 其他 | 0 | — | — | — | UNTESTED | Average period for accounts payable. |
| 1502 | `mdl219_2_6351_rp` | MATRIX | 0.789 | 价量与波动 | 0 | — | — | — | UNTESTED | 15-week moving average price divided by 36-week moving average price for the second module. |
| 1503 | `mdl219_2_curindcfp_` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative cash flow-to-price ratio adjusted for industry averages for the second module. |
| 1504 | `mdl219_2_pctchgqtrsales` | MATRIX | 0.789 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in sales calculated as a percentage for the second module. |
| 1505 | `mdl219_2_pelh_cf` | MATRIX | 0.789 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision confidence measuring the sum of 3-month changes in highest and lowest earnings forecasts for the second module. |
| 1506 | `mdl219_2_roe` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity calculated as net income divided by shareholder equity for the second module. |
| 1507 | `mdl219_2_divyield` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month dividend yield calculated as dividends per share divided by stock price for the second module. |
| 1508 | `mdl219_2_fc_fcfroey1p` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | Product of trailing 12-month free cash flow yield and forward ROE for the second module. |
| 1509 | `mdl219_2_fcghc` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow scaled by total assets for the second module. |
| 1510 | `mdl219_2_mpnghc` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in net profit margin for the second module. |
| 1511 | `mdl219_2_indrelcroe_` | MATRIX | 0.789 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-adjusted quarterly return on equity relative to industry averages for the second module. |
| 1512 | `mdl219_2_indrelrtn5d_` | MATRIX | 0.789 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-day industry-relative return adjusted for industry averages for the second module. |
| 1513 | `cash_and_cash_equivalents_7` | MATRIX | 0.788 | 其他 | 0 | — | — | — | UNTESTED | Amount of cash and cash equivalents held. |
| 1514 | `mdl219_2_curinddivp_` | MATRIX | 0.788 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative dividend yield adjusted for industry averages for the second module. |
| 1515 | `mdl219_2_ratrev6m` | MATRIX | 0.787 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month average of analyst rating revisions for the second module. |
| 1516 | `mdl219_2_actrtn9m` | MATRIX | 0.787 | 价量与波动 | 0 | — | — | — | UNTESTED | 9-month active return representing the percent change in stock price for the second module. |
| 1517 | `mdl219_2_tobinq` | MATRIX | 0.787 | 盈利与财务 | 0 | — | — | — | UNTESTED | Tobin's Q ratio calculated as the market value of equity plus debt divided by assets for the second module. |
| 1518 | `mdl219_2_p50_200ratio` | MATRIX | 0.787 | 价量与波动 | 0 | — | — | — | UNTESTED | 50-day moving average price divided by the 200-day moving average price for the second module. |
| 1519 | `mdl219_2_fc_fwdroe` | MATRIX | 0.787 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward return on equity calculated as next 4-quarter earnings estimates divided by book equity for the second module. |
| 1520 | `mdl219_2_ebitdap` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing 12-month EBITDA-to-price ratio used for valuation for the second module. |
| 1521 | `mdl219_2_nlvolcap` | MATRIX | 0.786 | 价量与波动 | 0 | — | — | — | UNTESTED | Logarithm of trading volume divided by market capitalization for the second module. |
| 1522 | `mdl219_2_w93ntr` | MATRIX | 0.786 | 价量与波动 | 0 | — | — | — | UNTESTED | 39-week return with a 4-week lag calculated as the price change from week t-43 to week t-4 for the second module. |
| 1523 | `mdl219_2_bmpo` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating profit margin calculated as operating income divided by sales for the second module. |
| 1524 | `mdl219_2_curindebitdap_` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | Industry-relative EBITDA-to-price ratio adjusted for industry averages for the second module. |
| 1525 | `mdl219_2_ebitdaev` | MATRIX | 0.786 | 盈利与财务 | 0 | — | — | — | UNTESTED | EBITDA-to-enterprise value ratio used for valuation for the second module. |
| 1526 | `unusual_accounts_payable_ratio` | MATRIX | 0.785 | 其他 | 0 | — | — | — | UNTESTED | Ratio indicating abnormal accounts payable levels. |
| 1527 | `mdl219_2_pfcf_cf` | MATRIX | 0.785 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow-to-price ratio calculated over trailing 12 months for the second module. |
| 1528 | `mdl219_2_capacq` | MATRIX | 0.785 | 盈利与财务 | 0 | — | — | — | UNTESTED | Capital acquisition ratio measuring operating cash flow less dividends divided by expenditures for the second module. |
| 1529 | `mdl219_2_pedu` | MATRIX | 0.785 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in depreciation scaled by total assets for the second module. |
| 1530 | `mdl219_2_pfcghc` | MATRIX | 0.785 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in free cash flow per share scaled by price for the second module. |
| 1531 | `mdl219_2_reinrate` | MATRIX | 0.784 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reinvestment rate calculated as EPS minus dividends divided by book equity for the second module. |
| 1532 | `cost_goods_sold_inventory_ratio` | MATRIX | 0.783 | 其他 | 0 | — | — | — | UNTESTED | Ratio of cost of goods sold to inventory. |
| 1533 | `mdl219_2_fc_stdevfy1epsp` | MATRIX | 0.783 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY1 EPS estimates scaled by price for the second module. |
| 1534 | `mdl219_2_fc_stdevfy2epsp` | MATRIX | 0.783 | 修正与预期 | 0 | — | — | — | UNTESTED | Standard deviation of FY2 EPS estimates scaled by price for the second module. |
| 1535 | `mdl219_2_m6dn2ntr` | MATRIX | 0.783 | 价量与波动 | 0 | — | — | — | UNTESTED | Second preceding 6-month return calculated as the percent change in stock price from month t-12 to t-7 for the second module. |
| 1536 | `mdl219_2_ntrm01ff` | MATRIX | 0.783 | 价量与波动 | 0 | — | — | — | UNTESTED | Fama-French momentum factor measuring percent change in stock price over 12 months excluding the most recent month for the second module. |
| 1537 | `mdl219_2_susgrowth` | MATRIX | 0.783 | 盈利与财务 | 0 | — | — | — | UNTESTED | Sustainable growth rate calculated as ROE multiplied by (1 - dividend payout ratio) for the second module. |
| 1538 | `mdl219_2_tstalp` | MATRIX | 0.782 | 价量与波动 | 0 | — | — | — | UNTESTED | 1-year price momentum indicator calculated using correlation-based analysis for the second module. |
| 1539 | `mdl219_2_slope52wp` | MATRIX | 0.782 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 52-week price trend line calculated using regression analysis for the second module. |
| 1540 | `mdl219_2_chg3yepsast` | MATRIX | 0.782 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in EPS scaled by total assets for the second module. |
| 1541 | `mdl219_2_actrtn12m` | MATRIX | 0.782 | 价量与波动 | 0 | — | — | — | UNTESTED | 12-month active return representing the percent change in stock price for the second module. |
| 1542 | `mdl219_2_relpricestrength_` | MATRIX | 0.781 | 价量与波动 | 0 | — | — | — | UNTESTED | Industry-adjusted 12-month relative price strength compared to industry averages for the second module. |
| 1543 | `mdl219_2_niper` | MATRIX | 0.781 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net income per employee calculated as income after taxes divided by the number of employees for the second module. |
| 1544 | `mdl219_2_revper` | MATRIX | 0.781 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue per employee calculated as trailing 12-month sales divided by the number of employees for the second module. |
| 1545 | `mdl219_2_chg3yepsp` | MATRIX | 0.781 | 价量与波动 | 0 | — | — | — | UNTESTED | 3-year change in EPS scaled by price for the second module. |
| 1546 | `mdl219_2_surp` | MATRIX | 0.780 | 修正与预期 | 0 | — | — | — | UNTESTED | Real earnings surprise calculated as the difference between actual EPS and consensus forecasts for the second module. |
| 1547 | `mdl219_2_chgshare` | MATRIX | 0.780 | 其他 | 0 | — | — | — | UNTESTED | Percent change in shares outstanding over the last year for the second module. |
| 1548 | `mdl219_2_rationalalpha` | MATRIX | 0.779 | 价量与波动 | 0 | — | — | — | UNTESTED | Rational decay alpha measuring excess return using a decay function for weighting for the second module. |
| 1549 | `working_capital_accruals_4` | MATRIX | 0.778 | 盈利与财务 | 0 | — | — | — | UNTESTED | Accruals related to working capital. |
| 1550 | `mdl219_2_mpoghc` | MATRIX | 0.777 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in operating profit margin for the second module. |
| 1551 | `mdl219_2_slope66wp` | MATRIX | 0.777 | 价量与波动 | 0 | — | — | — | UNTESTED | Slope of the 66-week price trend line calculated using regression analysis for the second module. |
| 1552 | `mdl219_2_pctchgocf` | MATRIX | 0.775 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in operating cash flow per share calculated as a percentage for the second module. |
| 1553 | `mdl219_2_w57w03_rp` | MATRIX | 0.775 | 价量与波动 | 0 | — | — | — | UNTESTED | 30-week moving average price divided by 75-week moving average price for the second module. |
| 1554 | `mdl219_2_chg3yocfast` | MATRIX | 0.774 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in operating cash flow scaled by total assets for the second module. |
| 1555 | `mdl219_2_debtcf` | MATRIX | 0.773 | 盈利与财务 | 0 | — | — | — | UNTESTED | Long-term debt-to-cash flow ratio calculated over trailing 12 months for the second module. |
| 1556 | `mdl219_2_pctchgcf` | MATRIX | 0.773 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in cash flow per share calculated as a percentage for the second module. |
| 1557 | `mdl219_2_chgalpha12m` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 12-month alpha for the second module. |
| 1558 | `mdl219_1_ccacw` | MATRIX | 0.773 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital accruals calculated as changes in current assets minus liabilities. |
| 1559 | `mdl219_2_chg3yfcfast` | MATRIX | 0.773 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow scaled by total assets for the second module. |
| 1560 | `mdl219_2_voctni` | MATRIX | 0.773 | 其他 | 0 | — | — | — | UNTESTED | Interest coverage ratio calculated as operating income divided by interest expenses for the second module. |
| 1561 | `mdl219_1_vnicw` | MATRIX | 0.772 | 其他 | 0 | — | — | — | UNTESTED | Working capital-to-inventory ratio calculated as working capital divided by inventory. |
| 1562 | `mdl219_2_fc_rev6` | MATRIX | 0.772 | 修正与预期 | 0 | — | — | — | UNTESTED | Average of prior 6-month changes in FY1 consensus earnings forecasts for the second module. |
| 1563 | `mdl219_2_actrtn18m` | MATRIX | 0.772 | 价量与波动 | 0 | — | — | — | UNTESTED | 18-month active return representing the percent change in stock price for the second module. |
| 1564 | `mdl219_2_nopatmargin` | MATRIX | 0.772 | 盈利与财务 | 0 | — | — | — | UNTESTED | NOPAT margin calculated as net operating profit after tax divided by net sales for the second module. |
| 1565 | `mdl219_2_spe1yfvc_cf` | MATRIX | 0.771 | 修正与预期 | 0 | — | — | — | UNTESTED | Dispersion of FY1 EPS estimates calculated as standard deviation divided by mean for the second module. |
| 1566 | `mdl219_2_spe2yfvc_cf` | MATRIX | 0.770 | 修正与预期 | 0 | — | — | — | UNTESTED | Dispersion of FY2 EPS estimates calculated as standard deviation divided by mean for the second module. |
| 1567 | `mdl219_2_oplev` | MATRIX | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Operating leverage calculated as the percent change in operating income divided by the percent change in sales for the second module. |
| 1568 | `mdl219_2_cfleverage` | MATRIX | 0.769 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow leverage calculated as total liabilities divided by operating cash flow for the second module. |
| 1569 | `mdl219_2_lumqca` | MATRIX | 0.769 | 盈利与财务 | 0 | — | — | — | UNTESTED | Acquisition multiple calculated as invested capital divided by EBITDA for the second module. |
| 1570 | `mdl219_2_liqcoeff` | MATRIX | 0.769 | 价量与波动 | 0 | — | — | — | UNTESTED | Liquidity coefficient measuring the relationship between trading turnover and price returns for the second module. |
| 1571 | `mdl219_2_pctchgeps` | MATRIX | 0.768 | 其他 | 0 | — | — | — | UNTESTED | 1-year growth in EPS calculated as a percentage for the second module. |
| 1572 | `mdl219_2_mrspe_cf` | MATRIX | 0.767 | 修正与预期 | 0 | — | — | — | UNTESTED | Street revision magnitude measuring 3-month change in median earnings forecast for the second module. |
| 1573 | `mdl219_2_pfcoy3ghc` | MATRIX | 0.767 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in operating cash flow per share scaled by price for the second module. |
| 1574 | `mdl219_2_chg3ycfast` | MATRIX | 0.766 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in cash flow from assets scaled by total assets for the second module. |
| 1575 | `mdl219_2_pfcfy3ghc` | MATRIX | 0.766 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow per share scaled by price for the second module. |
| 1576 | `mdl219_2_chg6malpha18m` | MATRIX | 0.763 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 18-month alpha for the second module. |
| 1577 | `mdl219_2_m42rav` | MATRIX | 0.763 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month value at risk calculated as the minimum monthly price return over the last 20 months for the second module. |
| 1578 | `mdl219_2_totalcov` | MATRIX | 0.763 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total coverage ratio measuring operating cash flow divided by debt payments for the second module. |
| 1579 | `mdl219_2_ica` | MATRIX | 0.763 | 其他 | 0 | — | — | — | UNTESTED | Abnormal capital investment measuring changes in capital expenditure intensity for the second module. |
| 1580 | `mdl219_2_actrtn24m` | MATRIX | 0.762 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month active return representing the percent change in stock price for the second module. |
| 1581 | `mdl219_2_epschgetr` | MATRIX | 0.762 | 宏观与行业 | 0 | — | — | — | UNTESTED | EPS change due to changes in effective tax rate over the last year for the second module. |
| 1582 | `mdl219_2_cg3ysales` | MATRIX | 0.761 | 宏观与行业 | 0 | — | — | — | UNTESTED | 3-year compound annual growth rate of sales for the second module. |
| 1583 | `mdl219_2_pfcy3ghc` | MATRIX | 0.759 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year change in free cash flow per share scaled by price for the second module. |
| 1584 | `working_capital_to_inventory_ratio_3` | MATRIX | 0.756 | 其他 | 0 | — | — | — | UNTESTED | Ratio of working capital to inventory. |
| 1585 | `mdl219_2_pctchg3yeps` | MATRIX | 0.754 | 其他 | 0 | — | — | — | UNTESTED | 3-year growth in EPS calculated as a percentage for the second module. |
| 1586 | `mdl219_2_pctchg3yocf` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year growth in operating cash flow per share calculated as a percentage for the second module. |
| 1587 | `mdl219_2_nfaldebt` | MATRIX | 0.751 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net fixed assets-to-long-term debt ratio measuring asset coverage for the second module. |
| 1588 | `mdl219_2_saleeps` | MATRIX | 0.750 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing 12-month sales relative to EPS for the second module. |
| 1589 | `mdl219_2_gtl` | MATRIX | 0.749 | 修正与预期 | 0 | — | — | — | UNTESTED | Long-term growth rate estimates based on analyst forecasts for the second module. |
| 1590 | `mdl219_2_pctchg3ycf` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year growth in cash flow per share calculated as a percentage for the second module. |
| 1591 | `mdl219_2_pge_cf` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inverse PEG ratio adjusted for dividend yield for the second module. |
| 1592 | `mdl219_2_ollev` | MATRIX | 0.749 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating liability leverage calculated as liabilities divided by operating assets for the second module. |
| 1593 | `mdl219_2_spefcn` | MATRIX | 0.748 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in EPS relative to operating cash flows over the last year for the second module. |
| 1594 | `mdl219_2_chgollev` | MATRIX | 0.747 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating liability leverage over the last year for the second module. |
| 1595 | `mdl219_2_saleg5y` | MATRIX | 0.747 | 其他 | 0 | — | — | — | UNTESTED | 5-year sales growth calculated as the difference between trailing 12-month sales and sales 20 quarters ago for the second module. |
| 1596 | `mdl219_1_rdsale` | MATRIX | 0.742 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | R&D intensity calculated as research and development expenses divided by sales. |
| 1597 | `mdl219_2_actrtn36m` | MATRIX | 0.741 | 价量与波动 | 0 | — | — | — | UNTESTED | 36-month active return representing the percent change in stock price for the second module. |
| 1598 | `mdl219_2_fc_dypeg` | MATRIX | 0.735 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reciprocal of dividend yield-adjusted PEG ratio for the second module. |
| 1599 | `mdl219_2_opincltd` | MATRIX | 0.735 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in operating income relative to long-term debt over the last year for the second module. |
| 1600 | `industry_relative_recommendation_delta_2` | MATRIX | 0.732 | 修正与预期 | 0 | — | — | — | UNTESTED | Change in analyst recommendation relative to industry peers. |
| 1601 | `mdl219_2_dcc` | MATRIX | 0.732 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current cash flow debt coverage ratio measuring cash flow relative to debt for the second module. |
| 1602 | `mdl219_2_chgalpha36m` | MATRIX | 0.732 | 其他 | 0 | — | — | — | UNTESTED | 6-month change in 36-month alpha for the second module. |
| 1603 | `mdl219_2_gtlm6ghc` | MATRIX | 0.724 | 修正与预期 | 0 | — | — | — | UNTESTED | 6-month change in long-term growth estimates for the second module. |
| 1604 | `mdl219_2_covol` | MATRIX | 0.722 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month trading volume trend for the second module. |
| 1605 | `mdl219_2_pctchgfcf` | MATRIX | 0.721 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year growth in free cash flow per share calculated as a percentage for the second module. |
| 1606 | `mdl219_1_indrelrecd_` | MATRIX | 0.718 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry-adjusted doubtful account receivables relative to industry averages. |
| 1607 | `mdl219_2_dpcapex` | MATRIX | 0.711 | 其他 | 0 | — | — | — | UNTESTED | Change in depreciation relative to capital expenditures over the last year for the second module. |
| 1608 | `mdl219_2_beta` | MATRIX | 0.711 | 价量与波动 | 0 | — | — | — | UNTESTED | Beta calculated over 60 months, measuring stock volatility relative to the market for the second module. |
| 1609 | `mdl219_2_cashburnrate` | MATRIX | 0.709 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash burn rate calculated as negative operating and investment cash flows divided by cash holdings for the second module. |
| 1610 | `mdl219_2_cashp` | MATRIX | 0.709 | 价量与波动 | 0 | — | — | — | UNTESTED | Cash-to-price ratio calculated as cash per share divided by stock price for the second module. |
| 1611 | `mdl219_2_cashsev` | MATRIX | 0.708 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-enterprise value ratio representing total cash divided by enterprise value for the second module. |
| 1612 | `mdl219_2_aspanratio` | MATRIX | 0.708 | 盈利与财务 | 0 | — | — | — | UNTESTED | Attention span ratio measuring operating assets minus liabilities scaled by total assets for the second module. |
| 1613 | `mdl219_2_chgnoa` | MATRIX | 0.708 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in net operating assets scaled by total assets for the second module. |
| 1614 | `mdl219_2_fc_rel5yfwdep` | MATRIX | 0.708 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative forward 12-month EPS-to-price ratio compared to historical averages for the second module. |
| 1615 | `mdl219_2_cashsale` | MATRIX | 0.707 | 其他 | 0 | — | — | — | UNTESTED | Cash-to-sales ratio calculated as average cash divided by sales for the second module. |
| 1616 | `mdl219_2_pca` | MATRIX | 0.707 | 其他 | 0 | — | — | — | UNTESTED | Average collection period calculated as accounts receivable times 365 divided by sales for the second module. |
| 1617 | `mdl219_2_netcashp` | MATRIX | 0.705 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net cash-to-price ratio calculated as cash minus debt divided by market price for the second module. |
| 1618 | `mdl219_2_rau` | MATRIX | 0.705 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in accounts receivable scaled by total assets for the second module. |
| 1619 | `mdl219_2_fc_ebop` | MATRIX | 0.704 | 价量与波动 | 0 | — | — | — | UNTESTED | Edwards-Bell-Ohlson value-to-price ratio based on valuation models for the second module. |
| 1620 | `mdl219_2_chgars` | MATRIX | 0.704 | 其他 | 0 | — | — | — | UNTESTED | 1-year change in accounts receivable as a percentage of sales for the second module. |
| 1621 | `mdl219_2_salerec` | MATRIX | 0.704 | 其他 | 0 | — | — | — | UNTESTED | Change in trailing 12-month sales relative to accounts receivable for the second module. |
| 1622 | `mdl219_2_chgvolpre4y` | MATRIX | 0.700 | 价量与波动 | 0 | — | — | — | UNTESTED | 4-year change in average trading volume for the second module. |
| 1623 | `mdl219_2_rerror60m` | MATRIX | 0.698 | 其他 | 0 | — | — | — | UNTESTED | Regression error of 60-month CAPM used for trend analysis for the second module. |
| 1624 | `mdl219_2_sigma` | MATRIX | 0.698 | 价量与波动 | 0 | — | — | — | UNTESTED | Stock return volatility calculated as the standard deviation of monthly returns over the last 60 months for the second module. |
| 1625 | `mdl219_2_alpha60m` | MATRIX | 0.697 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month alpha calculated as the intercept of a regression of stock returns against a benchmark for the second module. |
| 1626 | `mdl219_2_betasigma` | MATRIX | 0.697 | 价量与波动 | 0 | — | — | — | UNTESTED | Product of beta and sigma, combining volatility and market sensitivity for the second module. |
| 1627 | `mdl219_2_pctchg3yfcf` | MATRIX | 0.697 | 盈利与财务 | 0 | — | — | — | UNTESTED | 3-year growth in free cash flow per share calculated as a percentage for the second module. |
| 1628 | `mdl219_2_actrtn60m` | MATRIX | 0.696 | 价量与波动 | 0 | — | — | — | UNTESTED | 60-month active return representing the percent change in stock price for the second module. |
| 1629 | `mdl219_2_sighc` | MATRIX | 0.695 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in inventory as a percentage of sales for the second module. |
| 1630 | `mdl219_2_rel5ybp` | MATRIX | 0.692 | 其他 | 0 | — | — | — | UNTESTED | 5-year relative book-to-market ratio compared to historical averages for the second module. |
| 1631 | `mdl219_2_invast` | MATRIX | 0.692 | 盈利与财务 | 0 | — | — | — | UNTESTED | Inventory-to-total assets ratio calculated as inventory divided by total assets for the second module. |
| 1632 | `mdl219_2_rel5yep` | MATRIX | 0.692 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative EPS-to-price ratio compared to historical averages for the second module. |
| 1633 | `mdl219_2_rel5ysp` | MATRIX | 0.691 | 价量与波动 | 0 | — | — | — | UNTESTED | 5-year relative sales-to-price ratio compared to historical averages for the second module. |
| 1634 | `mdl219_2_perg` | MATRIX | 0.690 | 价量与波动 | 0 | — | — | — | UNTESTED | Risk-adjusted PEG ratio calculated as price divided by forward EPS and scaled by growth rate for the second module. |
| 1635 | `mdl219_2_salegpm` | MATRIX | 0.688 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in quarterly sales relative to gross profit margin over the last year for the second module. |
| 1636 | `mdl219_2_yoychggpm` | MATRIX | 0.688 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in gross profit margin for the second module. |
| 1637 | `mdl219_2_rel5yfcfp` | MATRIX | 0.677 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative free cash flow-to-price ratio compared to historical averages for the second module. |
| 1638 | `mdl219_2_rel5yocfp` | MATRIX | 0.677 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative operating cash flow-to-price ratio compared to historical averages for the second module. |
| 1639 | `mdl219_2_varresirtn` | MATRIX | 0.675 | 价量与波动 | 0 | — | — | — | UNTESTED | 24-month residual return variance calculated as the variance of monthly residual returns for the second module. |
| 1640 | `mdl219_2_vniu` | MATRIX | 0.670 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in inventory scaled by total assets for the second module. |
| 1641 | `mdl219_2_rel5yebitdap` | MATRIX | 0.667 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative EBITDA-to-price ratio compared to historical averages for the second module. |
| 1642 | `mdl219_2_rel5ycfp` | MATRIX | 0.665 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative cash flow-to-price ratio compared to historical averages for the second module. |
| 1643 | `mdl219_2_ydp_cf` | MATRIX | 0.659 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted dividend yield based on payout ratio and forward EPS estimates for the second module. |
| 1644 | `mdl219_2_divcov` | MATRIX | 0.658 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend coverage ratio calculated as operating earnings divided by dividends for the second module. |
| 1645 | `research_and_development_to_sales_ratio_2` | MATRIX | 0.648 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Ratio of research and development expenses to total sales. |
| 1646 | `mdl219_2_cashratio` | MATRIX | 0.634 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash-to-current liabilities ratio measuring liquidity for the second module. |
| 1647 | `mdl219_2_ocfratio` | MATRIX | 0.634 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating cash flow ratio calculated as cash flow divided by current liabilities for the second module. |
| 1648 | `mdl219_2_curratio` | MATRIX | 0.634 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current ratio calculated as current assets divided by current liabilities for the second module. |
| 1649 | `mdl219_2_astcomp` | MATRIX | 0.634 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset composition ratio representing current assets divided by total assets for the second module. |
| 1650 | `mdl219_2_div5yg` | MATRIX | 0.634 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year dividend growth rate measuring compounded annual growth in dividends for the second module. |
| 1651 | `mdl219_2_pcurlia` | MATRIX | 0.634 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current liabilities-to-price ratio calculated as liabilities per share divided by stock price for the second module. |
| 1652 | `mdl219_2_cashratiofixed` | MATRIX | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash ratio calculated as cash and equivalents divided by current liabilities for the second module. |
| 1653 | `mdl219_2_rel5ydivp` | MATRIX | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | 5-year relative dividend yield compared to historical averages for the second module. |
| 1654 | `mdl219_2_flowratio` | MATRIX | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Flow ratio measuring liquidity as current assets minus cash divided by liabilities minus debt for the second module. |
| 1655 | `mdl219_2_rq` | MATRIX | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Quick ratio calculated as current assets minus inventory divided by current liabilities for the second module. |
| 1656 | `mdl219_2_nnastp` | MATRIX | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Net net current assets-to-price ratio calculated as current assets minus liabilities divided by price for the second module. |
| 1657 | `mdl219_2_wcast` | MATRIX | 0.633 | 盈利与财务 | 0 | — | — | — | UNTESTED | Working capital-to-total assets ratio calculated as average working capital divided by average total assets for the second module. |
| 1658 | `mdl219_2_yoychgcr` | MATRIX | 0.632 | 其他 | 0 | — | — | — | UNTESTED | Year-over-year change in current ratio for the second module. |
| 1659 | `mdl219_2_chgreccast` | MATRIX | 0.631 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year-over-year change in accounts receivable relative to current assets for the second module. |
| 1660 | `mdl219_2_cws` | MATRIX | 0.631 | 其他 | 0 | — | — | — | UNTESTED | Working capital-to-sales ratio calculated as average working capital divided by trailing 12-month sales for the second module. |
| 1661 | `mdl219_2_pinoa` | MATRIX | 0.631 | 盈利与财务 | 0 | — | — | — | UNTESTED | Pretax return on net operating assets calculated as operating income divided by net operating assets for the second module. |
| 1662 | `mdl219_2_iqa` | MATRIX | 0.630 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset quality index measuring changes in the ratio of non-current assets to total assets for the second module. |
| 1663 | `mdl219_2_ppa` | MATRIX | 0.623 | 其他 | 0 | — | — | — | UNTESTED | Average payable period calculated as accounts payable times 365 divided by cost of goods sold for the second module. |
| 1664 | `mdl219_2_ags` | MATRIX | 0.621 | 其他 | 0 | — | — | — | UNTESTED | SG&A expenses-to-sales ratio calculated as selling, general, and administrative expenses divided by sales for the second module. |
| 1665 | `mdl219_2_pau` | MATRIX | 0.620 | 盈利与财务 | 0 | — | — | — | UNTESTED | Unexpected change in accounts payable scaled by total assets for the second module. |
| 1666 | `mdl219_2_cashc` | MATRIX | 0.617 | 其他 | 0 | — | — | — | UNTESTED | Cash cycle calculated as inventory days plus collection days minus payable days for the second module. |
| 1667 | `mdl219_2_otvni` | MATRIX | 0.608 | 价量与波动 | 0 | — | — | — | UNTESTED | Inventory turnover ratio calculated as cost of goods sold divided by average inventory for the second module. |
| 1668 | `mdl219_2_cogsinvt` | MATRIX | 0.602 | 其他 | 0 | — | — | — | UNTESTED | Change in cost of goods sold relative to inventory levels for the second module. |
| 1669 | `mdl219_2_divcf` | MATRIX | 0.599 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Dividends-to-cash flow ratio calculated over trailing 12 months for the second module. |
| 1670 | `mdl219_2_chgsgasale` | MATRIX | 0.591 | 其他 | 0 | — | — | — | UNUSABLE | Change in SG&A expenses relative to sales over the last year for the second module. |
| 1671 | `mdl219_2_vnicw` | MATRIX | 0.581 | 其他 | 0 | — | — | — | UNUSABLE | Working capital-to-inventory ratio calculated as working capital divided by inventory for the second module. |
| 1672 | `mdl219_2_idb` | MATRIX | 0.540 | 其他 | 0 | — | — | — | UNUSABLE | Basic defensive interval measuring the number of days a company can cover expenses using cash and receivables for the second module. |
| 1673 | `mdl219_2_rdsale` | MATRIX | 0.521 | 搜索与替代数据 | 0 | — | — | — | UNUSABLE | R&D intensity calculated as research and development expenses divided by sales for the second module. |
| 1674 | `mdl219_2_ccacw` | MATRIX | 0.501 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Working capital accruals calculated as changes in current assets minus liabilities for the second module. |
| 1675 | `mdl219_2_indrelrecd_` | MATRIX | 0.476 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Industry-adjusted doubtful account receivables relative to industry averages for the second module. |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

