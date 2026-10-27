# other452 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other452` |
| 名称 | Earnings Tax Data |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 29 |
| 覆盖率 | 0.3727 |
| 平台已有 alpha | 1 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset comprehensively studies a wide range of tax-related ratios that are useful for earnings management or financial fraud detection because tax-related accounts in financial statements and footnotes reveal significant information about earnings quality.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **29** |
| 类型分布 | MATRIX×29 |
| 平均覆盖率 | **0.373** |
| 覆盖率区间 | 0.25 ~ 0.54 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 5 | 17.2% |
| 稀疏 (<0.50) | 24 | 82.8% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 29 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 29 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 17 | 0.35 | oth452_expense_d1_asset_change、oth452_accrualsratio_d1_asset_change、oth452_liability_d1_asset_change |
| 其他 | 12 | 0.41 | oth452_deferred_tax_expense_11、oth452_deferred_tax_expense_31、oth452_deferred_tax_expense_12 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth452_deferred_tax_expense_11` | MATRIX | 0.538 | 其他 | 0 | — | — | — | UNUSABLE | Deferred tax expense |
| 2 | `oth452_deferred_tax_expense_31` | MATRIX | 0.537 | 其他 | 0 | — | — | — | UNUSABLE | Deferred tax expense |
| 3 | `oth452_deferred_tax_expense_12` | MATRIX | 0.537 | 其他 | 0 | — | — | — | UNUSABLE | Deferred tax expense |
| 4 | `oth452_deferred_tax_expense_51` | MATRIX | 0.513 | 其他 | 0 | — | — | — | UNUSABLE | Deferred tax expense |
| 5 | `oth452_deferred_tax_expense_41` | MATRIX | 0.506 | 其他 | 0 | — | — | — | UNUSABLE | Deferred tax expense |
| 6 | `oth452_deferred_tax_expense_21` | MATRIX | 0.448 | 其他 | 0 | — | — | — | UNUSABLE | Deferred tax expense |
| 7 | `oth452_deferred_tax_expense_22` | MATRIX | 0.446 | 其他 | 0 | — | — | — | UNUSABLE | Deferred tax expense |
| 8 | `oth452_expense_d1_asset_change` | MATRIX | 0.433 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Expense d1 asset change |
| 9 | `oth452_accrualsratio_d1_asset_change` | MATRIX | 0.406 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Accruals ratio d1 asset change |
| 10 | `oth452_liability_d1_asset_change` | MATRIX | 0.405 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liability d1 asset change |
| 11 | `oth452_deferred_tax_liability_31` | MATRIX | 0.365 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liability |
| 12 | `oth452_liability_d1_length` | MATRIX | 0.363 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liability d1 length |
| 13 | `oth452_liability_d1_mean` | MATRIX | 0.358 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liability d1 mean |
| 14 | `oth452_liability_d1_max` | MATRIX | 0.355 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liability d1 max |
| 15 | `oth452_liability_d1_min` | MATRIX | 0.355 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liability d1 min |
| 16 | `oth452_deferred_tax_liability_11` | MATRIX | 0.354 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liability |
| 17 | `oth452_deferred_tax_liability_12` | MATRIX | 0.354 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liability |
| 18 | `oth452_liability_d1_dts` | MATRIX | 0.342 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liability d1 distributions |
| 19 | `oth452_deferred_tax_liability_41` | MATRIX | 0.338 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liability |
| 20 | `oth452_deferred_tax_liability_51` | MATRIX | 0.337 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liability |
| 21 | `oth452_deferred_tax_liability_13` | MATRIX | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liability |
| 22 | `oth452_deferred_tax_liability_21` | MATRIX | 0.293 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liability |
| 23 | `oth452_deferred_tax_liability_22` | MATRIX | 0.292 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Deferred tax liability |
| 24 | `oth452_expense_d1_length` | MATRIX | 0.280 | 其他 | 0 | — | — | — | UNUSABLE | Expense d1 length |
| 25 | `oth452_expense_d1_mean` | MATRIX | 0.275 | 其他 | 0 | — | — | — | UNUSABLE | Expense d1 mean |
| 26 | `oth452_expense_d1_max` | MATRIX | 0.273 | 其他 | 0 | — | — | — | UNUSABLE | Expense d1 max |
| 27 | `oth452_expense_d1_min` | MATRIX | 0.272 | 其他 | 0 | — | — | — | UNUSABLE | Expense d1 min |
| 28 | `oth452_liability_d1_current_t` | MATRIX | 0.264 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Liability d1 current t |
| 29 | `oth452_expense_d1_dts` | MATRIX | 0.254 | 其他 | 0 | — | — | — | UNUSABLE | Expense d1 dts |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-OTHER401-WEAK`（2026-09-23T18:27:10）family=other401 基本面矩阵族（oth401_* 65 字段 MATRIX）：{"family": "other401 基本面矩阵族（oth401_* 65 字段 MATRIX）", "reason": "wave235 9 探针全灭：best sharpe 0.70 / fit 0.34 / 2Y 1.07，CONCENTRATED_WEIGHT+LOW_ROBUST_UNIVERSE；D4 资格线 1.25 未达 → 判死。1 条 group_cartesian_product(sector,sector) 坏式被自动隔离。FUNDAMENTAL 塔候选 other401 出局；other452(cov0.37)/fundamental93(0.33) 均低于地板。", "source": "registry_dead_end", "salvage": {"alpha_ids": [], "count": 0, "source_waves": [], "seal

