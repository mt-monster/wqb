# model31 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model31` |
| 名称 | Earnings Quality Model |
| 类别 | MODEL |
| 数据字段数(平台) | 74 |
| 覆盖率 | 0.6672 |
| 平台已有 alpha | 712 |
| valueScore | 2.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset offers a global, quantitative model that evaluates the sustainability and quality of company earnings by decomposing past earnings into sustainable and non-sustainable components. It includes a wide range of financial metrics such as accruals, cash flow, asset turnover, debt-to-equity, and various profitability ratios, along with percentile ranks and region-based comparisons. The model is designed to identify companies likely to experience high or low earnings sustainability over the next twelve months, making it a valuable tool for predicting future price movements. By highlighting firms with strong or weak earnings quality, the dataset supports the development of alpha-generating strategies and risk management frameworks.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **74** |
| 类型分布 | MATRIX×74 |
| 平均覆盖率 | **0.667** |
| 覆盖率区间 | 0.30 ~ 0.90 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 39 | 52.7% |
| 低 (0.50–0.70) | 13 | 17.6% |
| 稀疏 (<0.50) | 22 | 29.7% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 39 | 52.7% |
| UNUSABLE | 35 | 47.3% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 39 / UNUSABLE 35 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 59 | 0.65 | mdl31_dse_last_y、mdl31_fcf_mm_last_y、mdl31_ass_tvr_last_y |
| 价量与波动 | 10 | 0.73 | mdl31_pricesales_current、mdl31_pb_current、mdl31_pricesales_last_y |
| 其他 | 4 | 0.77 | auditor_switch_indicator_prev_year、mdl31_bv_share_last_y、mdl31_bv_share_prior_y |
| 风险与质量 | 1 | 0.39 | mdl31_oe_chg_1_qtr |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `auditor_switch_indicator_prev_year` | MATRIX | 0.895 | 其他 | 0 | — | — | — | UNTESTED | Whether the company changed its external auditor during the last fiscal year (1 = yes, 0 = no) |
| 2 | `mdl31_dse_last_y` | MATRIX | 0.895 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of long-term debt to total equity for the last fiscal year, measuring company leverage |
| 3 | `mdl31_bv_share_last_y` | MATRIX | 0.895 | 其他 | 0 | — | — | — | UNTESTED | Book value per share as of last completed fiscal year (book value divided by shares outstanding) |
| 4 | `mdl31_fcf_mm_last_y` | MATRIX | 0.894 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free Cash Flow in millions for the most recently completed fiscal year, calculated as cash from operations minus capital |
| 5 | `mdl31_ass_tvr_last_y` | MATRIX | 0.893 | 盈利与财务 | 0 | — | — | — | UNTESTED | Revenue generated per unit of total assets (Asset Turnover = Net Revenue/Total Assets) for the last year |
| 6 | `mdl31_dse_prior_y` | MATRIX | 0.893 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of long-term debt to total equity for the prior year; higher values indicate greater leverage |
| 7 | `mdl31_roe_pct_last_y` | MATRIX | 0.893 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity percentage for the last completed fiscal year |
| 8 | `mdl31_bv_share_prior_y` | MATRIX | 0.892 | 其他 | 0 | — | — | — | UNTESTED | Book value per share as reported for the previous fiscal year |
| 9 | `mdl31_om_pct_last_y` | MATRIX | 0.892 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating profit margin for the last completed fiscal year; operating income divided by revenue, as a percentage |
| 10 | `star_eq_rank` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Quality region rank before beta neutralization (1–100, higher = better) for the current period |
| 11 | `star_eq_region_rank` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current percentile rank for earnings quality, comparing the security to all others in the same region, higher scores mea |
| 12 | `mdl31_erq_re_rk_chg_1_day` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-day change in the regional percentile rank based on the Earnings Quality Model, comparing the security to all other se |
| 13 | `star_eq_accruals_rank` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current percentile rank for Accruals Component of Earnings Quality Model; higher scores indicate healthier accruals stru |
| 14 | `mdl31_acc_chg_1_day` | MATRIX | 0.891 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in accruals component percentile rank for the company compared to the prior day; 100 is largest positive change, |
| 15 | `mdl31_om_pct_prior_y` | MATRIX | 0.890 | 盈利与财务 | 0 | — | — | — | UNTESTED | Operating margin percentage for the prior year |
| 16 | `star_eq_ope_rank` | MATRIX | 0.889 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current value of percentile rank reflecting Operating Efficiency factors in Earnings Quality; 100=highest rated stock |
| 17 | `mdl31_oe_chg_1_day` | MATRIX | 0.889 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-day change in the Operating Efficiency component percentile rank of the Earnings Quality model (1–100; higher is bette |
| 18 | `mdl31_ass_tvr_prior_y` | MATRIX | 0.889 | 盈利与财务 | 0 | — | — | — | UNTESTED | Asset turnover ratio for the prior fiscal year; net revenue divided by total assets |
| 19 | `mdl31_roe_pct_prior_y` | MATRIX | 0.889 | 盈利与财务 | 0 | — | — | — | UNTESTED | Return on equity percentage for the prior year |
| 20 | `mdl31_pricesales_current` | MATRIX | 0.888 | 价量与波动 | 0 | — | — | — | UNTESTED | Current price-to-sales ratio |
| 21 | `mdl31_pb_current` | MATRIX | 0.881 | 价量与波动 | 0 | — | — | — | UNTESTED | Current price to book ratio |
| 22 | `mdl31_pricesales_last_y` | MATRIX | 0.874 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-sales ratio for the last fiscal year |
| 23 | `star_eq_cashflow_rank` | MATRIX | 0.870 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current percentile score (1-100) for Cash Flow factors, region-relative; higher is better earnings quality |
| 24 | `mdl31_cf_chg_1_day` | MATRIX | 0.869 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-day change in percentile rank for Cash Flow component of the Earnings Quality Model |
| 25 | `mdl31_pb_last_y` | MATRIX | 0.867 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-book ratio for the last fiscal year |
| 26 | `mdl31_erq_re_rk_prior_y` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank of earnings quality from the prior year, comparing to others in the same region, higher scores indicate |
| 27 | `mdl31_acc_prior_y` | MATRIX | 0.858 | 盈利与财务 | 0 | — | — | — | UNTESTED | Percentile rank reflecting only the Accruals factors of the Earnings Quality Model for the prior fiscal year, where 100 |
| 28 | `mdl31_oe_prior_y` | MATRIX | 0.856 | 盈利与财务 | 0 | — | — | — | UNTESTED | Prior year percentile rank reflecting operating efficiency factors of the Earnings Quality Model for the company; 100 is |
| 29 | `mdl31_pricesales_prior_y` | MATRIX | 0.851 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-sales ratio for the prior year |
| 30 | `mdl31_pb_prior_y` | MATRIX | 0.845 | 价量与波动 | 0 | — | — | — | UNTESTED | Prior year price-to-book ratio |
| 31 | `mdl31_erq_re_rk_chg_1_fy` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in Earnings Quality Region Rank over the past fiscal year (1=worst, 100=best improvement) |
| 32 | `mdl31_acc_chg_1_fy` | MATRIX | 0.845 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in the Accruals component percentile rank (1–100; higher is better) |
| 33 | `mdl31_oe_chg_1_fy` | MATRIX | 0.841 | 盈利与财务 | 0 | — | — | — | UNTESTED | 1-year change in the Operating Efficiency component percentile rank of the Earnings Quality model (1–100; higher is bett |
| 34 | `mdl31_cf_prior_y` | MATRIX | 0.838 | 盈利与财务 | 0 | — | — | — | UNTESTED | Prior year percentile rank reflecting cash flow factors of the Earnings Quality Model for the company; 100 is best, 1 is |
| 35 | `mdl31_dy_pct_current` | MATRIX | 0.828 | 盈利与财务 | 0 | — | — | — | UNTESTED | Current dividend yield percentage, calculated as dividends per share divided by current share price |
| 36 | `mdl31_dps_last_y` | MATRIX | 0.828 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total cash dividends per share declared in the last fiscal year, including both common and preferred shares |
| 37 | `mdl31_cf_chg_1_fy` | MATRIX | 0.820 | 盈利与财务 | 0 | — | — | — | UNTESTED | Change in percentile rank over prior fiscal year for cash flow factors in Earnings Quality Model |
| 38 | `mdl31_gm_pct_last_y` | MATRIX | 0.810 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross margin percentage for the last fiscal year |
| 39 | `mdl31_gm_pct_prior_y` | MATRIX | 0.809 | 盈利与财务 | 0 | — | — | — | UNTESTED | Gross margin percentage for the prior year |
| 40 | `mdl31_gva` | MATRIX | 0.584 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average net operating assets in millions for the last quarter |
| 41 | `mdl31_dps_last_qtr` | MATRIX | 0.568 | 盈利与财务 | 0 | — | — | — | UNUSABLE | All cash dividends declared per share (common and preferred stock) by the company in the last quarter |
| 42 | `mdl31_pricesales_last_qtr` | MATRIX | 0.553 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-to-sales ratio for the last quarter |
| 43 | `mdl31_dse_last_qtr` | MATRIX | 0.541 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of long-term debt to total equity for the last quarter; higher values indicate greater leverage |
| 44 | `mdl31_pb_last_qtr` | MATRIX | 0.536 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-to-book ratio for the last fiscal quarter |
| 45 | `mdl31_dty_mm_fcf` | MATRIX | 0.532 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Year-to-date free cash flow (operations minus capex), in millions |
| 46 | `mdl31_dse_prior_qtr` | MATRIX | 0.530 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of long-term debt to total equity for the prior quarter, measuring company leverage for that period |
| 47 | `mdl31_pb_prior_qtr` | MATRIX | 0.521 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price-to-book ratio for the prior quarter |
| 48 | `mdl31_acc_prior_qtr` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentile score (1-100) for Accruals Component relative to region for prior quarter; higher is better earning quality |
| 49 | `mdl31_erq_raw_prior_qtr` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Prior quarter Earnings Quality region rank before beta neutralization (1–100, higher = better) |
| 50 | `mdl31_erq_re_rk_prior_qtr` | MATRIX | 0.519 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Percentile rank of earnings quality for the prior quarter compared to peers in the same region, with higher scores signa |
| 51 | `mdl31_oe_prior_qtr` | MATRIX | 0.518 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Prior quarter percentile rank reflecting operating efficiency factors of the Earnings Quality Model for the company; 100 |
| 52 | `mdl31_cf_prior_qtr` | MATRIX | 0.508 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Prior quarter percentile rank reflecting cash flow factors of the Earnings Quality Model for the company; 100 is best, 1 |
| 53 | `mdl31_pricesales_prior_qtr` | MATRIX | 0.496 | 价量与波动 | 0 | — | — | — | UNUSABLE | Prior quarter price-to-sales ratio |
| 54 | `mdl31_q4t_mm_fcf` | MATRIX | 0.482 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free cash flow from operations (CF from Ops minus capex) summed over the trailing four quarters, in millions of local cu |
| 55 | `mdl31_om_pct_last_qtr` | MATRIX | 0.432 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating margin percentage for the last quarter |
| 56 | `mdl31_bv_share_last_qtr` | MATRIX | 0.419 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Book value per share for the last completed fiscal quarter, calculated as total shareholder equity divided by shares out |
| 57 | `mdl31_om_pct_prior_qtr` | MATRIX | 0.406 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating margin percentage for the prior quarter |
| 58 | `mdl31_roe_pct_last_qtr` | MATRIX | 0.401 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on equity percentage for the last fiscal quarter |
| 59 | `mdl31_bv_share_prior_qtr` | MATRIX | 0.398 | 其他 | 0 | — | — | — | UNUSABLE | Book value per share in the prior quarter, i.e., book value divided by total shares outstanding |
| 60 | `mdl31_acc_chg_1_qtr` | MATRIX | 0.396 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in Accruals Component percentile rank over the past quarter (region-relative, 1=worst, 100=best) |
| 61 | `mdl31_erq_re_rk_chg_1_qtr` | MATRIX | 0.396 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in Earnings Quality Region Rank over the past quarter (1=worst, 100=best improvement) |
| 62 | `mdl31_oe_chg_1_qtr` | MATRIX | 0.395 | 风险与质量 | 0 | — | — | — | UNUSABLE | Change in the Operating Efficiency Component percentile rank compared to the prior quarter; indicates improvement or det |
| 63 | `mdl31_ass_tvr_last_qtr` | MATRIX | 0.395 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Asset turnover ratio for the last quarter; net revenue divided by total assets |
| 64 | `mdl31_gm_pct_last_qtr` | MATRIX | 0.390 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross margin percentage for the last completed fiscal quarter |
| 65 | `mdl31_cf_chg_1_qtr` | MATRIX | 0.386 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Change in percentile rank over the last quarter for the cash flow factors of Earnings Quality Model |
| 66 | `mdl31_fcf_mm_last_qtr` | MATRIX | 0.379 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Free Cash Flow in millions for the last completed fiscal quarter, calculated as cash from operations minus capital expen |
| 67 | `mdl31_roe_pct_prior_qtr` | MATRIX | 0.378 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on equity percentage for the prior quarter |
| 68 | `mdl31_ass_tvr_prior_qtr` | MATRIX | 0.374 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue generated per unit of total assets (Asset Turnover = Net Revenue/Total Assets) for the prior quarter |
| 69 | `mdl31_gm_pct_prior_qtr` | MATRIX | 0.368 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross margin percentage for the prior (most recent previous) fiscal quarter |
| 70 | `mdl31_ass_tvr_t4q` | MATRIX | 0.335 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Revenue generated per unit of total assets (Asset Turnover = Net Revenue/Total Assets) over the trailing 4 quarters |
| 71 | `mdl31_roe_pct_t4q` | MATRIX | 0.333 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Return on equity over the trailing four quarters, as a percentage |
| 72 | `mdl31_om_pct_t4q` | MATRIX | 0.332 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Operating margin percentage measured over the trailing four quarters |
| 73 | `mdl31_dps_t4q` | MATRIX | 0.312 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total cash dividends declared over the trailing four quarters, on both common and preferred stock, per share |
| 74 | `mdl31_gm_pct_t4q` | MATRIX | 0.304 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Gross margin percentage for the trailing four quarters |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

