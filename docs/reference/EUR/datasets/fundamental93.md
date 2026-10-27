# fundamental93 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental93` |
| 名称 | Earnings Tax Data |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 46 |
| 覆盖率 | 0.3285 |
| 平台已有 alpha | 1 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive, point-in-time fundamental financial data for public companies worldwide, with annual history dating back to 1980 for developed markets and the 1990s for developing markets. It includes detailed financial statement items, ratios, per-share data, and key performance indicators, all mapped to unique company and security identifiers. The data covers balance sheets, income statements, cash flows, segment information, and restatements, enabling robust analysis of company performance, valuation, and risk. By offering granular, timely, and historically consistent financial metrics, this dataset is essential for building and backtesting quantitative models, screening for investment opportunities, and forecasting price movements based on fundamental drivers.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **46** |
| 类型分布 | MATRIX×46 |
| 平均覆盖率 | **0.328** |
| 覆盖率区间 | 0.18 ~ 0.46 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 46 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 46 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 46 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 40 | 0.31 | fnd93_expense_d1_asset_change、fnd93_accruals_d1_length、fnd93_liability_d1_length |
| 其他 | 5 | 0.43 | fnd93_expense_d1_length、fnd93_expense_d1_max、fnd93_expense_d1_mean |
| 风险与质量 | 1 | 0.35 | fnd93_expense_d1_current_t |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `fnd93_expense_d1_length` | MATRIX | 0.459 | 其他 | 0 | — | — | — | UNUSABLE | Number of available deferred tax expense ratio observations over the LTM (last twelve months) window |
| 2 | `fnd93_expense_d1_max` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Maximum value of the deferred tax expense ratio over the LTM window |
| 3 | `fnd93_expense_d1_mean` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Mean of the deferred tax expense ratio over the LTM window |
| 4 | `fnd93_expense_d1_min` | MATRIX | 0.435 | 其他 | 0 | — | — | — | UNUSABLE | Minimum value of the deferred tax expense ratio over the LTM window |
| 5 | `fnd93_expense_d1_asset_change` | MATRIX | 0.424 | 盈利与财务 | 0 | — | — | — | UNUSABLE | YoY asset change ratio: latest total assets divided by total assets 12 months earlier (e.g., Asset_2018Q3 / Asset_2017Q3) |
| 6 | `fnd93_accruals_d1_length` | MATRIX | 0.419 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of available accruals ratio observations within the trailing twelve-month (LTM) window |
| 7 | `fnd93_liability_d1_length` | MATRIX | 0.419 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of deferred tax liability ratio observations available in the trailing 12-month (LTM) window |
| 8 | `fnd93_expense_d1_dts` | MATRIX | 0.405 | 其他 | 0 | — | — | — | UNUSABLE | Standard deviation of the deferred tax expense ratio over the LTM window |
| 9 | `fnd93_deferred_tax_expense_11` | MATRIX | 0.405 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 7 ratio fields with naming pattern "DEFERRED_TAX_EXPENSE_XX", where XX denotes the index of denominator. We use (Net deferred tax  |
| 10 | `fnd93_deferred_tax_expense_12` | MATRIX | 0.405 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 7 ratio fields with naming pattern "DEFERRED_TAX_EXPENSE_XX", where XX denotes the index of denominator. We use (Net deferred tax  |
| 11 | `fnd93_deferred_tax_expense_31` | MATRIX | 0.404 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 7 ratio fields with naming pattern "DEFERRED_TAX_EXPENSE_XX", where XX denotes the index of denominator. We use (Net deferred tax  |
| 12 | `fnd93_accrualsratio_d1_asset_change` | MATRIX | 0.398 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Asset change ratio = latest total assets divided by asset_ltm (e.g., Asset_2018Q3 / Asset_2017Q3) |
| 13 | `fnd93_liability_d1_asset_change` | MATRIX | 0.397 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio of latest total assets to asset_ltm (e.g., Assets_current quarter / Assets_same quarter prior year) |
| 14 | `fnd93_liability_d1_max` | MATRIX | 0.388 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Maximum value of the deferred tax liability ratio over the LTM window |
| 15 | `fnd93_liability_d1_mean` | MATRIX | 0.388 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Mean of the deferred tax liability ratio over the LTM window |
| 16 | `fnd93_liability_d1_min` | MATRIX | 0.388 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Minimum value of the deferred tax liability ratio over the LTM window |
| 17 | `fnd93_liability_d1_dts` | MATRIX | 0.376 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of the deferred tax liability ratio over the LTM window |
| 18 | `fnd93_deferred_tax_expense_51` | MATRIX | 0.365 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 7 ratio fields with naming pattern "DEFERRED_TAX_EXPENSE_XX", where XX denotes the index of denominator. We use (Net deferred tax  |
| 19 | `fnd93_deferred_tax_expense_41` | MATRIX | 0.355 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 7 ratio fields with naming pattern "DEFERRED_TAX_EXPENSE_XX", where XX denotes the index of denominator. We use (Net deferred tax  |
| 20 | `fnd93_deferred_tax_expense_21` | MATRIX | 0.351 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 7 ratio fields with naming pattern "DEFERRED_TAX_EXPENSE_XX", where XX denotes the index of denominator. We use (Net deferred tax  |
| 21 | `fnd93_deferred_tax_expense_22` | MATRIX | 0.350 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 7 ratio fields with naming pattern "DEFERRED_TAX_EXPENSE_XX", where XX denotes the index of denominator. We use (Net deferred tax  |
| 22 | `fnd93_deferred_tax_liability_12` | MATRIX | 0.350 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 23 | `fnd93_deferred_tax_liability_11` | MATRIX | 0.349 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 24 | `fnd93_expense_d1_current_t` | MATRIX | 0.348 | 风险与质量 | 0 | — | — | — | UNUSABLE | Z-score (t-statistic) of the current deferred tax expense ratio relative to the LTM window, computed as (current ratio − mean) / std |
| 25 | `fnd93_deferred_tax_liability_31` | MATRIX | 0.345 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 26 | `fnd93_deferred_tax_liability_13` | MATRIX | 0.331 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 27 | `fnd93_deferred_tax_liability_51` | MATRIX | 0.314 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 28 | `fnd93_liability_d1_current_t` | MATRIX | 0.310 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Z-score of the current liability ratio versus the LTM window, computed as (current ratio − mean) / std |
| 29 | `fnd93_deferred_tax_liability_41` | MATRIX | 0.304 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 30 | `fnd93_deferred_tax_liability_21` | MATRIX | 0.302 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 31 | `fnd93_deferred_tax_liability_22` | MATRIX | 0.300 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 32 | `fnd93_accruals_d1_max` | MATRIX | 0.275 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Maximum accruals ratio observed within the trailing twelve-month (LTM) window |
| 33 | `fnd93_accruals_d1_mean` | MATRIX | 0.275 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Average of the accruals ratio over the trailing twelve-month (LTM) window |
| 34 | `fnd93_accruals_d1_min` | MATRIX | 0.275 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Minimum accruals ratio observed within the trailing twelve-month (LTM) window |
| 35 | `fnd93_deferred_tax_liability_23` | MATRIX | 0.267 | 盈利与财务 | 0 | — | — | — | UNUSABLE | There are 9 ratio fields with naming pattern "DEFERRED_TAX_LIABILITY_XX", where XX denotes the index of denominator. We use deferred tax exp |
| 36 | `fnd93_accruals_d1_dts` | MATRIX | 0.267 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Standard deviation of the accruals ratio over the trailing twelve-month (LTM) window |
| 37 | `fnd93_tax_accruals_31` | MATRIX | 0.250 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 3, candidate 1 (suffix 31); unit: ratio |
| 38 | `fnd93_tax_accruals_11` | MATRIX | 0.250 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 1, candidate 1 (suffix 11); unit: ratio |
| 39 | `fnd93_tax_accruals_12` | MATRIX | 0.220 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 1, candidate 2 (suffix 12); unit: ratio |
| 40 | `fnd93_tax_accruals_13` | MATRIX | 0.210 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 1, candidate 3 (suffix 13); unit: ratio |
| 41 | `fnd93_tax_accruals_51` | MATRIX | 0.203 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 5, candidate 1 (suffix 51); unit: ratio |
| 42 | `fnd93_accruals_d1_current_t` | MATRIX | 0.199 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Z-score of the current accruals ratio versus its LTM window: (current ratio − mean) / std |
| 43 | `fnd93_tax_accruals_21` | MATRIX | 0.198 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 2, candidate 1 (suffix 21); unit: ratio |
| 44 | `fnd93_tax_accruals_22` | MATRIX | 0.196 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 2, candidate 2 (suffix 22); unit: ratio |
| 45 | `fnd93_tax_accruals_41` | MATRIX | 0.194 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 4, candidate 1 (suffix 41); unit: ratio |
| 46 | `fnd93_tax_accruals_23` | MATRIX | 0.177 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio computed as tax expense minus cash tax paid divided by denominator group 2, candidate 3 (suffix 23); unit: ratio |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-OTHER401-WEAK`（2026-09-23T18:27:10）family=other401 基本面矩阵族（oth401_* 65 字段 MATRIX）：{"family": "other401 基本面矩阵族（oth401_* 65 字段 MATRIX）", "reason": "wave235 9 探针全灭：best sharpe 0.70 / fit 0.34 / 2Y 1.07，CONCENTRATED_WEIGHT+LOW_ROBUST_UNIVERSE；D4 资格线 1.25 未达 → 判死。1 条 group_cartesian_product(sector,sector) 坏式被自动隔离。FUNDAMENTAL 塔候选 other401 出局；other452(cov0.37)/fundamental93(0.33) 均低于地板。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "seal
- `EUR-FND93-TAXACCRUAL-ZERO-SIGNAL-DEAD`（2026-10-03）family=fundamental93 Earnings Tax Data（递延税/税务应计族）：{"dataset": "fundamental93", "evidence": {"JjQY0nZm": "deferred_tax_expense_11/_12 比值 S0.53 F0.18 2Y1.52 RA_fail=4 longCount566", "vR2xn5MG": "tax_accruals_11-_12 S0.48 F0.17 2Y-0.16 RA_fail=5 longCount371", "rKeE6bg1": "liability_d1_length zscore S0.38 F0.12 2Y-0.03 RA_fail=4 longCount403", "leKk67O7": "expense_d1_mean zscore S0.03 F0.00 RA_fail=5 longCount500"}, "family": "fundamental93 Earnings

