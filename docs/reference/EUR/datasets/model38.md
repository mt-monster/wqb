# model38 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model38` |
| 名称 | Growth Valuation Model |
| 类别 | MODEL |
| 数据字段数(平台) | 145 |
| 覆盖率 | 0.7774 |
| 平台已有 alpha | 4959 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive stock valuation rankings by integrating multiple fundamental ratios and advanced earnings projections. It combines six key valuation metrics—such as earnings/price, cash flow/price, EBITDA/EV, sales/EV, book/price, and dividends/price—along with share buyback activity, to generate a single, robust relative valuation score for each company. The model leverages both reported financials and refined analyst estimates to address systematic biases and improve forecast accuracy. Additionally, it includes intrinsic value calculations using discounted future profitability measures, such as dividends and earnings, and offers detailed projections for earnings and dividends over multiple years. These features make the dataset highly valuable for identifying underval

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **145** |
| 类型分布 | MATRIX×144　SYMBOL×1 |
| 平均覆盖率 | **0.777** |
| 覆盖率区间 | 0.57 ~ 0.97 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 16 | 11.0% |
| 中 (0.70–0.90) | 73 | 50.3% |
| 低 (0.50–0.70) | 56 | 38.6% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 143 | 98.6% |
| UNUSABLE | 2 | 1.4% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 143 / UNUSABLE 2 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 62 | 0.77 | star_val_dividend_projection_fy1、star_val_dividend_projection_fy10、star_val_dividend_projection_fy11 |
| 盈利与财务 | 31 | 0.77 | star_val_earnings_measure_type、pe_ratio_relative_score、star_val_pe |
| 宏观与行业 | 22 | 0.84 | region_relative_valuation_rank、star_val_region_rank、sector_relative_valuation_rank |
| 价量与波动 | 20 | 0.76 | pb_ratio_relative_component_rank_d1、star_val_pb、region_rank_price_to_intrinsic_value |
| 风险与质量 | 7 | 0.75 | mdl38_rel_val_global_rk、global_relative_valuation_rank_main、global_relative_valuation_score |
| 其他 | 2 | 0.76 | latest_fiscal_year_period_end_date_d1、justified_forward_pe_ratio_2 |
| 持仓与资金流 | 1 | 0.96 | relative_valuation_global_position_d1 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `star_val_earnings_measure_type` | MATRIX | 0.970 | 盈利与财务 | 0 | — | — | — | UNTESTED | IV Earnings Measure Type : This field displays the type of earnings projected for this company in the StarMine SmartGrowth model. The field  |
| 2 | `star_val_dividend_projection_fy1` | MATRIX | 0.962 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 1, projected by the StarMine SmartGrowth model |
| 3 | `pe_ratio_relative_score` | MATRIX | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Floating-point percentile score representing the global-relative attractiveness (valuation rank) based on the Price/Earnings ratio component |
| 4 | `star_val_pe` | MATRIX | 0.962 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of the security for its price/earnings (P/E) ratio valuation component versus global peers; higher scores mean more  |
| 5 | `pb_ratio_relative_component_rank_d1` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Floating-point percentile score representing the global-relative attractiveness (valuation rank) based on the Price/Book ratio component |
| 6 | `star_val_pb` | MATRIX | 0.960 | 价量与波动 | 0 | — | — | — | UNTESTED | Global percentile rank of the stock in the Price/Book component of the Relative Valuation Model, 1-100 scale; higher scores indicate better  |
| 7 | `mdl38_rel_val_global_rk` | MATRIX | 0.959 | 风险与质量 | 0 | — | — | — | UNTESTED | Current global percentile (1-100) rank of a stock’s attractiveness in the Relative Valuation Model; higher is better value |
| 8 | `region_relative_valuation_rank` | MATRIX | 0.959 | 宏观与行业 | 0 | — | — | — | UNTESTED | Floating-point percentile rank for relative valuation attractiveness within region; higher is more attractive |
| 9 | `relative_valuation_global_position_d1` | MATRIX | 0.959 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Floating-point global percentile rank for relative valuation attractiveness; higher is more attractive |
| 10 | `star_val_region_rank` | MATRIX | 0.959 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current regional percentile (1-100) rank of a stock’s attractiveness in the Relative Valuation Model; higher is better value |
| 11 | `sector_relative_valuation_rank` | MATRIX | 0.958 | 宏观与行业 | 0 | — | — | — | UNTESTED | Floating-point percentile rank for relative valuation attractiveness within sector; higher is more attractive |
| 12 | `star_val_sector_rank` | MATRIX | 0.958 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sector-relative valuation rank (1-100) indicating attractiveness within the sector |
| 13 | `industry_relative_valuation_rank` | MATRIX | 0.945 | 宏观与行业 | 0 | — | — | — | UNTESTED | Floating-point percentile rank for relative valuation attractiveness within industry; higher is more attractive |
| 14 | `star_val_industry_rank` | MATRIX | 0.945 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of the security’s valuation attractiveness versus industry peers in the Relative Valuation Model; higher scores indi |
| 15 | `buyback_yield_relative_component_rank_d1` | MATRIX | 0.939 | 宏观与行业 | 0 | — | — | — | UNTESTED | Floating-point percentile score representing the global-relative attractiveness (valuation rank) based on the Buyback Yield component |
| 16 | `star_val_buyback_yield` | MATRIX | 0.939 | 宏观与行业 | 0 | — | — | — | UNTESTED | Global percentile rank of the stock in the buyback yield component of the Relative Valuation Model, 1-100 scale; higher scores indicate bett |
| 17 | `dividend_yield_relative_component_rank_d1` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Floating-point percentile score representing the global-relative attractiveness (valuation rank) based on the Dividend Yield component |
| 18 | `star_val_dividend_yield` | MATRIX | 0.860 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile (1-100) rank of the stock’s dividend yield within the Relative Valuation Model; higher means better value on dividend yield |
| 19 | `earnings_projection_metric_type_d1` | MATRIX | 0.850 | 盈利与财务 | 0 | — | — | — | UNTESTED | Floating-point code indicating which earnings measure is used, typically EPS or FFO |
| 20 | `latest_fiscal_year_period_end_date_d1` | SYMBOL | 0.850 | 其他 | 0 | — | — | — | UNTESTED | Date marking the end of the most recent fiscal year for the company (d1 version). |
| 21 | `long_term_assumed_annual_earnings` | MATRIX | 0.850 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year when the company is projected to reach steady state earnings growth |
| 22 | `mdl38_iv_discount_rate` | MATRIX | 0.850 | 盈利与财务 | 0 | — | — | — | UNTESTED | Discount rate used in the StarMine Intrinsic Valuation model for discounting dividends to FY0 |
| 23 | `mdl38_iv_div_payout_rate` | MATRIX | 0.850 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend payout rate of the company at and after the steady state year defined in the StarMine model |
| 24 | `mdl38_iv_growth_ear` | MATRIX | 0.850 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings growth rate expected at steady state |
| 25 | `mdl38_iv_year_div` | MATRIX | 0.850 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year when the company is projected to reach steady state dividends |
| 26 | `star_val_dividend_projection_fy10` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 10, projected by the StarMine SmartGrowth model |
| 27 | `star_val_dividend_projection_fy11` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 11 dividends per share (DPS) estimate from StarMine SmartGrowth model |
| 28 | `star_val_dividend_projection_fy12` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 12, projected by the StarMine SmartGrowth model |
| 29 | `star_val_dividend_projection_fy13` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 13, as projected by the StarMine SmartGrowth model |
| 30 | `star_val_dividend_projection_fy14` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 14, projected by the StarMine SmartGrowth model |
| 31 | `star_val_dividend_projection_fy15` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 15, as projected by the StarMine SmartGrowth model |
| 32 | `star_val_dividend_projection_fy2` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 2, projected by the StarMine SmartGrowth model |
| 33 | `star_val_dividend_projection_fy3` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 3, projected by the StarMine SmartGrowth model |
| 34 | `star_val_dividend_projection_fy4` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 4, as projected by the StarMine SmartGrowth model |
| 35 | `star_val_dividend_projection_fy5` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 5, as projected by the StarMine SmartGrowth model |
| 36 | `star_val_dividend_projection_fy6` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 6, projected by the StarMine SmartGrowth model |
| 37 | `star_val_dividend_projection_fy7` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 7, as projected by the StarMine SmartGrowth model |
| 38 | `star_val_dividend_projection_fy8` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 8, projected by the StarMine SmartGrowth model |
| 39 | `star_val_dividend_projection_fy9` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 9 dividends per share (DPS) estimate from StarMine SmartGrowth model |
| 40 | `star_val_earnings_projection_fy1` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 1, projected by the StarMine SmartGrowth model |
| 41 | `star_val_earnings_projection_fy10` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 10, as projected by the StarMine SmartGrowth model |
| 42 | `star_val_earnings_projection_fy11` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 11, as projected by the StarMine SmartGrowth model |
| 43 | `star_val_earnings_projection_fy12` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 12, projected by the StarMine SmartGrowth model |
| 44 | `star_val_earnings_projection_fy13` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 13, as projected by the StarMine SmartGrowth model |
| 45 | `star_val_earnings_projection_fy14` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 14, as projected by the StarMine SmartGrowth model |
| 46 | `star_val_earnings_projection_fy15` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 15, projected by the StarMine SmartGrowth model |
| 47 | `star_val_earnings_projection_fy2` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 2, projected by the StarMine SmartGrowth model |
| 48 | `star_val_earnings_projection_fy3` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 3, projected by the StarMine SmartGrowth model |
| 49 | `star_val_earnings_projection_fy4` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 4 EPS estimate from StarMine SmartGrowth model |
| 50 | `star_val_earnings_projection_fy5` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 5, projected by the StarMine SmartGrowth model |
| 51 | `star_val_earnings_projection_fy6` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 6, projected by the StarMine SmartGrowth model |
| 52 | `star_val_earnings_projection_fy7` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 7, projected by the StarMine SmartGrowth model |
| 53 | `star_val_earnings_projection_fy8` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 8, projected by the StarMine SmartGrowth model |
| 54 | `star_val_earnings_projection_fy9` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated earnings per share (EPS) for fiscal year 9, as projected by the StarMine SmartGrowth model |
| 55 | `star_val_iv_projection` | MATRIX | 0.850 | 宏观与行业 | 0 | — | — | — | UNTESTED | Intrinsic value of the stock calculated by StarMine, expressed in the currency used for projections |
| 56 | `mdl38_iv_cagr_base_year` | MATRIX | 0.850 | 宏观与行业 | 0 | — | — | — | UNTESTED | Compound annual growth rate (CAGR) computed over the designated base years as used in the intrinsic value model’s projections; serves as bas |
| 57 | `star_val_fwd10_eps_cagr` | MATRIX | 0.850 | 宏观与行业 | 0 | — | — | — | UNTESTED | Compound annual growth rate (CAGR) between last reported EPS and forecasted EPS for year 10 from StarMine SmartGrowth model |
| 58 | `star_val_fwd5_eps_cagr` | MATRIX | 0.850 | 宏观与行业 | 0 | — | — | — | UNTESTED | Compound annual growth rate (CAGR) between last reported EPS and forecasted EPS for year 5 from StarMine SmartGrowth model |
| 59 | `region_rank_price_to_intrinsic_value` | MATRIX | 0.850 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile ranking (as a floating-point value) of the Price/Intrinsic Value ratio for the stock relative to its regional peer group; higher  |
| 60 | `star_val_piv_ratio` | MATRIX | 0.850 | 价量与波动 | 0 | — | — | — | UNTESTED | Ratio of previous day's market close price to the StarMine model's calculated intrinsic value |
| 61 | `star_val_piv_region_rank` | MATRIX | 0.850 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile ranking (integer value, scale 1-100) of the Price/Intrinsic Value ratio for the stock relative to its regional peer group; higher |
| 62 | `mdl38_iv_warranted_f12m_p_e` | MATRIX | 0.850 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward 12-month price-to-earnings ratio implied by the StarMine intrinsic value and SmartGrowth EPS projections; represents what the P/E wo |
| 63 | `sector_rank_price_to_intrinsic_value` | MATRIX | 0.849 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile ranking (as a floating-point value) of the Price/Intrinsic Value ratio for the stock relative to its sector peer group; higher ra |
| 64 | `star_val_piv_sector_rank` | MATRIX | 0.849 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of a stock’s price to intrinsic value ratio within its region-sector; higher means more undervalued within sector |
| 65 | `star_val_implied10_eps_cagr` | MATRIX | 0.848 | 修正与预期 | 0 | — | — | — | UNTESTED | Forward compound annual growth rate of EPS over 10 years implied by the market price and analyst projections, such that intrinsic value matc |
| 66 | `star_val_implied5_eps_cagr` | MATRIX | 0.848 | 价量与波动 | 0 | — | — | — | UNTESTED | Market-implied compound annual EPS growth rate over 5 years needed for intrinsic value to equal current market price |
| 67 | `ev_ebitda_relative_score` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Floating-point percentile score representing the global-relative attractiveness (valuation rank) based on the EV/EBITDA ratio component |
| 68 | `mdl38_rel_val_ev_ebitda` | MATRIX | 0.814 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of the security for its enterprise value/EBITDA (EV/EBITDA) ratio valuation component versus global peers; higher sc |
| 69 | `pe_ratio_relative_score_float` | MATRIX | 0.778 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile score (floating-point) for Price/Earnings ratio, measuring valuation attractiveness globally in StarMine’s model |
| 70 | `pe_ratio_relative_score_main` | MATRIX | 0.778 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of the stock’s valuation attractiveness based solely on its price-to-earnings (P/E) ratio |
| 71 | `projected_dividends_fy1_2` | MATRIX | 0.777 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of dividends per share (DPS) for fiscal year 1, projected by StarMine SmartGrowth model |
| 72 | `pb_ratio_relative_score` | MATRIX | 0.776 | 价量与波动 | 0 | — | — | — | UNTESTED | Contribution of price-to-book ratio to the overall relative valuation attractiveness score |
| 73 | `pb_ratio_relative_score_float` | MATRIX | 0.776 | 价量与波动 | 0 | — | — | — | UNTESTED | Floating-point percentile rank for the Price/Book ratio component in the relative valuation model |
| 74 | `global_relative_valuation_rank_main` | MATRIX | 0.775 | 风险与质量 | 0 | — | — | — | UNTESTED | Current global 1–100 percentile rank of the security’s valuation attractiveness in the Relative Valuation Model, combining all measures, wit |
| 75 | `global_relative_valuation_score` | MATRIX | 0.775 | 风险与质量 | 0 | — | — | — | UNTESTED | Current global percentile rank (floating-point) in the StarMine Relative Valuation Model, reflecting overall valuation attractiveness compar |
| 76 | `region_relative_valuation_score` | MATRIX | 0.775 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) for valuation attractiveness within the given region, reflecting how the stock compares to peers according to the Re |
| 77 | `region_relative_valuation_score_float` | MATRIX | 0.775 | 宏观与行业 | 0 | — | — | — | UNTESTED | Floating-point regional percentile rank of the stock in the Relative Valuation Model |
| 78 | `sector_relative_valuation_rank_main` | MATRIX | 0.774 | 宏观与行业 | 0 | — | — | — | UNTESTED | Current 1–100 percentile rank of the stock in its sector within the overall Relative Valuation Model; higher scores mean the stock is viewed |
| 79 | `sector_relative_valuation_score_float` | MATRIX | 0.774 | 宏观与行业 | 0 | — | — | — | UNTESTED | Floating-point version of the sector-relative percentile rank for valuation attractiveness |
| 80 | `industry_relative_valuation_rank_main` | MATRIX | 0.765 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry percentile rank (1-100) of the stock's valuation attractiveness within its industry, higher is better |
| 81 | `industry_relative_valuation_score` | MATRIX | 0.765 | 宏观与行业 | 0 | — | — | — | UNTESTED | Floating-point percentile rank of the stock in the relative valuation model within its industry; higher scores signal more attractive valuat |
| 82 | `buyback_yield_relative_score` | MATRIX | 0.761 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of the stock’s valuation attractiveness based solely on its buyback yield |
| 83 | `buyback_yield_relative_score_float` | MATRIX | 0.761 | 宏观与行业 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) of buyback yield’s contribution to relative valuation within peer group |
| 84 | `ev_sales_relative_component_rank_d1` | MATRIX | 0.755 | 风险与质量 | 0 | — | — | — | UNTESTED | Floating-point percentile score representing the global-relative attractiveness (valuation rank) based on the EV/Sales ratio component |
| 85 | `star_val_ev_sales` | MATRIX | 0.755 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile (1-100) rank of the stock’s enterprise value/sales ratio in the Relative Valuation Model; higher means better value on EV/Sales |
| 86 | `pcf_ratio_relative_component_rank_d1` | MATRIX | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Floating-point percentile score representing the global-relative attractiveness (valuation rank) based on the Price/Cash Flow ratio componen |
| 87 | `star_val_pcf` | MATRIX | 0.755 | 盈利与财务 | 0 | — | — | — | UNTESTED | Global percentile rank of the stock in the Price/Cash Flow component of the Relative Valuation Model, 1-100 scale; higher scores indicate be |
| 88 | `price_to_intrinsic_value_industry_position_d1` | MATRIX | 0.725 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile ranking (as floating-point value) of the Price/Intrinsic Value ratio for the stock relative to its industry peer group; higher ra |
| 89 | `star_val_piv_industry_rank` | MATRIX | 0.725 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile ranking (integer value, scale 1-100) of the Price/Intrinsic Value ratio for the stock relative to its industry peer group; higher |
| 90 | `earnings_measure_type_float` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Indicator (floating-point) specifying the type of earnings measure used (e.g., EPS, FFO) in the intrinsic valuation |
| 91 | `intrinsic_value_in_currency` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Intrinsic value of the security (fair value estimate) calculated by StarMine, expressed in the chosen projection currency |
| 92 | `long_term_assumed_annual_dividends` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year in which the company is projected to reach steady state dividend payout |
| 93 | `long_term_assumed_annual_earnings_main` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year in which the company is projected to reach steady state earnings growth |
| 94 | `long_term_dividend_payout_ratio_2` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Dividend payout rate the company is projected to maintain at steady state in future years |
| 95 | `long_term_earnings_growth_rate_2` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings growth rate the company is projected to maintain at steady state in future years |
| 96 | `model_discount_rate` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Discount rate used by the StarMine Intrinsic Valuation model when discounting future cash flows (primarily dividends) |
| 97 | `projected_dividends_fy10_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of dividends per share (DPS) for fiscal year 10, projected by StarMine SmartGrowth model |
| 98 | `projected_dividends_fy11_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 11 according to the StarMine SmartGrowth model |
| 99 | `projected_dividends_fy12_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share estimate for fiscal year 12 from the StarMine SmartGrowth model |
| 100 | `projected_dividends_fy13_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share estimate for fiscal year 13 from the StarMine SmartGrowth model |
| 101 | `projected_dividends_fy14_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of dividends per share (DPS) for fiscal year 14, projected by StarMine SmartGrowth model |
| 102 | `projected_dividends_fy15_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share (DPS) for fiscal year 15 projected by the StarMine SmartGrowth model |
| 103 | `projected_dividends_fy2_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of dividends per share (DPS) for fiscal year 2, projected by StarMine SmartGrowth model |
| 104 | `projected_dividends_fy3_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of dividends per share (DPS) for fiscal year 3, projected by StarMine SmartGrowth model |
| 105 | `projected_dividends_fy4_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartGrowth model’s estimated dividends per share (DPS) for fiscal year 4 for the security |
| 106 | `projected_dividends_fy5_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of dividends per share (DPS) for fiscal year 5, projected by StarMine SmartGrowth model |
| 107 | `projected_dividends_fy6_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated dividends per share for fiscal year 6 based on the intrinsic valuation model |
| 108 | `projected_dividends_fy7_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share estimate for fiscal year 7 from the StarMine SmartGrowth model |
| 109 | `projected_dividends_fy8_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimate of dividends per share (DPS) for fiscal year 8, projected by StarMine SmartGrowth model |
| 110 | `projected_dividends_fy9_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Dividend per share estimate for fiscal year 9 from the StarMine SmartGrowth model |
| 111 | `projected_earnings_fy10_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartGrowth model’s estimated earnings per share (EPS) for fiscal year 10 for the security |
| 112 | `projected_earnings_fy11_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Projected EPS estimate for fiscal year 11 for the company, based on the StarMine SmartGrowth model |
| 113 | `projected_earnings_fy12_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Fiscal year 12 EPS estimate from the StarMine SmartGrowth model |
| 114 | `projected_earnings_fy13_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartGrowth model’s estimated earnings per share (EPS) for fiscal year 13 for the security |
| 115 | `projected_earnings_fy14_2` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected earnings per share (EPS) for fiscal year 14 from StarMine SmartGrowth model |
| 116 | `projected_earnings_fy15_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartGrowth model’s estimated earnings per share (EPS) for fiscal year 15 for the security |
| 117 | `projected_earnings_fy1_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartGrowth model’s estimated earnings per share (EPS) for fiscal year 1 for the security |
| 118 | `projected_earnings_fy2_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartGrowth model’s estimated earnings per share (EPS) for fiscal year 2 for the security |
| 119 | `projected_earnings_fy3_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartGrowth model’s estimated earnings per share (EPS) for fiscal year 3 for the security |
| 120 | `projected_earnings_fy4_2` | MATRIX | 0.673 | 盈利与财务 | 0 | — | — | — | UNTESTED | Projected earnings per share (EPS) for fiscal year 4 from StarMine SmartGrowth model |
| 121 | `projected_earnings_fy5_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | StarMine SmartGrowth model’s estimated earnings per share (EPS) for fiscal year 5 for the security |
| 122 | `projected_earnings_fy6_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Projected EPS estimate for fiscal year 6 for the company, based on the StarMine SmartGrowth model |
| 123 | `projected_earnings_fy7_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated EPS for fiscal year 7 projected by the StarMine SmartGrowth model |
| 124 | `projected_earnings_fy8_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Projected adjusted earnings for fiscal year 8, based on analyst estimates and StarMine modeling |
| 125 | `projected_earnings_fy9_2` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated EPS for fiscal year 9 projected by the StarMine SmartGrowth model |
| 126 | `forward_10yr_eps_growth_rate` | MATRIX | 0.673 | 宏观与行业 | 0 | — | — | — | UNTESTED | Compound annual growth rate of EPS from last reported EPS to fiscal year 10, projected by StarMine SmartGrowth model |
| 127 | `forward_5yr_eps_growth_rate` | MATRIX | 0.673 | 宏观与行业 | 0 | — | — | — | UNTESTED | Compound annual growth rate of EPS from last reported EPS to fiscal year 5, projected by StarMine SmartGrowth model |
| 128 | `justified_forward_pe_ratio_2` | MATRIX | 0.673 | 其他 | 0 | — | — | — | UNTESTED | Forward 12-month P/E ratio warranted by the intrinsic valuation model, calculated as intrinsic value divided by year-ahead EPS projection |
| 129 | `price_to_intrinsic_value_ratio` | MATRIX | 0.673 | 修正与预期 | 0 | — | — | — | UNTESTED | Ratio of current market price to model-estimated intrinsic value; values below 1 indicate possible undervaluation |
| 130 | `region_rank_price_intrinsic_value` | MATRIX | 0.673 | 价量与波动 | 0 | — | — | — | UNTESTED | A 1-100 percentile score ranking the stock’s price/intrinsic value ratio relative to all stocks in its region, where a lower ratio (cheaper  |
| 131 | `region_rank_price_to_intrinsic_value_float` | MATRIX | 0.673 | 价量与波动 | 0 | — | — | — | UNTESTED | Floating-point percentile rank of price/intrinsic value within the region |
| 132 | `sector_rank_price_intrinsic_value` | MATRIX | 0.672 | 价量与波动 | 0 | — | — | — | UNTESTED | A 1-100 percentile score ranking the stock’s price/intrinsic value ratio relative to all stocks in its sector within the same region, higher |
| 133 | `sector_rank_price_to_intrinsic_value_float` | MATRIX | 0.672 | 价量与波动 | 0 | — | — | — | UNTESTED | Floating-point version of the sector-relative percentile ranking for price/intrinsic value |
| 134 | `market_implied_10yr_eps_growth` | MATRIX | 0.671 | 盈利与财务 | 0 | — | — | — | UNTESTED | Market-implied compound annual growth rate of earnings per share over the next 10 years based on current market price |
| 135 | `market_implied_5yr_eps_growth` | MATRIX | 0.671 | 价量与波动 | 0 | — | — | — | UNTESTED | Forward 5-year compound annual growth rate (CAGR) of EPS implied by the market price (adjusted EPS over FY1-FY5 so the calculated intrinsic  |
| 136 | `dividend_yield_relative_score` | MATRIX | 0.668 | 盈利与财务 | 0 | — | — | — | UNTESTED | Global percentile rank (integer 1-100) of the stock for Dividend Yield component of the Relative Valuation model — higher value = better val |
| 137 | `dividend_yield_relative_score_float` | MATRIX | 0.668 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point) for dividend yield’s contribution to relative valuation within peer group |
| 138 | `ev_ebitda_relative_score_float` | MATRIX | 0.665 | 盈利与财务 | 0 | — | — | — | UNTESTED | Floating-point normalized score showing the contribution of the EV/EBITDA ratio to the relative valuation component |
| 139 | `ev_ebitda_relative_score_main` | MATRIX | 0.665 | 盈利与财务 | 0 | — | — | — | UNTESTED | Global percentile rank (integer 1-100) of the stock for the EV/EBITDA component in the Relative Valuation model — higher value means better  |
| 140 | `ev_sales_relative_score` | MATRIX | 0.609 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of the stock’s valuation attractiveness based solely on its EV/Sales ratio |
| 141 | `ev_sales_relative_score_float` | MATRIX | 0.609 | 风险与质量 | 0 | — | — | — | UNTESTED | Percentile rank (floating-point, global) for valuation based on EV/Sales component in the Relative Valuation Model |
| 142 | `pcf_ratio_relative_score` | MATRIX | 0.609 | 价量与波动 | 0 | — | — | — | UNTESTED | Percentile rank (1-100) of the stock’s valuation attractiveness based solely on its price-to-cash-flow (P/CF) ratio |
| 143 | `pcf_ratio_relative_score_float` | MATRIX | 0.609 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile score (floating-point) for Price/Cash Flow ratio, measuring valuation attractiveness globally in StarMine’s model |
| 144 | `industry_rank_price_intrinsic_value` | MATRIX | 0.575 | 价量与波动 | 0 | — | — | — | UNUSABLE | A 1-100 percentile score ranking the stock’s price/intrinsic value ratio among stocks in its industry within the same region, higher scores  |
| 145 | `industry_rank_price_to_intrinsic_value` | MATRIX | 0.575 | 价量与波动 | 0 | — | — | — | UNUSABLE | Percentile rank (floating-point) of a stock’s price-to-intrinsic value ratio within its industry; higher scores suggest more undervaluation |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

