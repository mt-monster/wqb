# analyst81 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst81` |
| 名称 | Creditworthiness model |
| 类别 | ANALYST |
| 数据字段数(平台) | 5 |
| 覆盖率 | 0.2402 |
| 平台已有 alpha | 5 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive global credit ratings and default probabilities for industrial companies, derived from financial statement data using a multi-objective rating evaluation model. It includes risk classes (from AAA to D), probability of default, credit limits, and a wide range of financial ratios such as solvency, liquidity, profitability, and leverage metrics. The dataset also features transition matrices, rating migration and stability statistics, and sector/country breakdowns. By quantifying creditworthiness and default risk, this dataset is highly valuable for predicting price movements, as changes in credit ratings and financial health often precede significant shifts in equity and bond prices. It enables risk assessment, early warning of distress, and the development

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **5** |
| 类型分布 | MATRIX×5 |
| 平均覆盖率 | **0.240** |
| 覆盖率区间 | 0.23 ~ 0.25 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 5 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 5 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 5 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 2 | 0.24 | default_likelihood_percent、anl81_probability_of_default_percent |
| 盈利与财务 | 2 | 0.24 | financial_data_completeness_percent、anl81_confidence_level_percent |
| 风险与质量 | 1 | 0.23 | anl81_class |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `default_likelihood_percent` | MATRIX | 0.253 | 修正与预期 | 0 | — | — | — | UNUSABLE | Previous-period probability of default estimated by mode_finance, expressed as a percentage from 0 to 100 |
| 2 | `financial_data_completeness_percent` | MATRIX | 0.253 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Confidence level for the lagged assessment, 0–100%, indicating completeness/reliability of available data |
| 3 | `anl81_class` | MATRIX | 0.232 | 风险与质量 | 0 | — | — | — | UNUSABLE | Creditwrothiness class indices in integers: 9(AAA), 5(AA), 4(A), 1(BBB), 2(BB), 3(B), 7(CCC), 8(CC), 6(C), 10(D) |
| 4 | `anl81_confidence_level_percent` | MATRIX | 0.232 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Confidence level of the assessment, measuring data completeness and reliability as a percentage from 0 to 100 |
| 5 | `anl81_probability_of_default_percent` | MATRIX | 0.232 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated probability of default over the rating horizon, expressed as a percentage from 0 to 100 |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-CREDIT-DEFAULT-ANALYST81-MODEL52`（2026-10-19）family=credit_default：{"batch": "2tRfk57w04Tob49Lqt0jIG2", "best_abs_sharpe": 0.42, "coverage": {"analyst81": 0.2402, "model52": 0.1986}, "date": "2026-10-19", "decision_table": "D15（8 探针无 S >= 0.5 即判死）", "family": "credit_default", "field_trap": "anl81_class / cr_class 用打乱序数的编码（9=AAA,5=AA,4=A,1=BBB,2=BB,3=B,7=CCC,8=CC,6=C,10=D），任何单调算子（rank/zscore/ts_rank）在其上无意义，只能当分组或条件变量。", "id": "EUR-CREDIT-DEFAULT-ANALYST81-MODEL52

