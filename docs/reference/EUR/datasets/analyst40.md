# analyst40 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `analyst40` |
| 名称 | Information on board of director |
| 类别 | ANALYST |
| 数据字段数(平台) | 22 |
| 覆盖率 | 0.301 |
| 平台已有 alpha | 13 |
| valueScore | 5.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset aggregates and harmonizes board and executive data from multiple leading sources, providing a comprehensive view of board composition, director profiles, and inter-company board connections across global public companies. It includes detailed information on board structure, director demographics (such as gender, age, and nationality), independence, tenure, and movements, as well as the network of interlocking directorships. By capturing both point-in-time and historical changes, the dataset enables analysis of boardroom dynamics, governance quality, and the flow of information or influence between companies. Such insights are valuable for predicting price movements, as changes in board composition, director turnover, and network centrality have been empirically linked to firm 

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **22** |
| 类型分布 | MATRIX×20　VECTOR×2 |
| 平均覆盖率 | **0.301** |
| 覆盖率区间 | 0.26 ~ 0.36 |
| 更新频率（推断） | 日频 |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 22 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 22 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 22 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 16 | 0.30 | anl40_newcount、anl40_oldcount、anl40_totalchange |
| 价量与波动 | 2 | 0.32 | anl40_netturnoverrate、anl40_turnoverrate |
| 元数据与非信号 | 2 | 0.28 | anl40_age、anl40_relation |
| 盈利与财务 | 1 | 0.36 | anl40_brdcount |
| 宏观与行业 | 1 | 0.27 | anl40_employmentrate |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `anl40_newcount` | MATRIX | 0.365 | 其他 | 0 | — | — | — | UNUSABLE | How many directors in this company after today's movement. Due to lack of original data on history file, there is no newCount record before  |
| 2 | `anl40_brdcount` | MATRIX | 0.365 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Count of unique IDs of industry participants. Industry stands for an aggregate view of all  equity clearance activity for the date, symbol,  |
| 3 | `anl40_oldcount` | MATRIX | 0.365 | 其他 | 0 | — | — | — | UNUSABLE | How many directors in this company before today's movement. Due to lack of original data on history file, there is no oldCount record before |
| 4 | `anl40_netturnoverrate` | MATRIX | 0.352 | 价量与波动 | 0 | — | — | — | UNUSABLE | TotalChanges / (OldCount + NewCount). No record before 20160729. |
| 5 | `anl40_totalchange` | MATRIX | 0.342 | 其他 | 0 | — | — | — | UNUSABLE | Total changes in director members in that day, which equals (addIn - moveOut). |
| 6 | `anl40_overall_genderratio` | MATRIX | 0.300 | 其他 | 0 | — | — | — | UNUSABLE | proportion of male directors of overall directors |
| 7 | `anl40_overall_timeretirement` | MATRIX | 0.300 | 其他 | 0 | — | — | — | UNUSABLE | average time to retirement of overall directors |
| 8 | `anl40_overall_stdevage` | MATRIX | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | standard deviation of directors' ages of overall directors |
| 9 | `anl40_sd_genderratio` | MATRIX | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | proportion of male directors of supervisory directors |
| 10 | `anl40_sd_timeretirement` | MATRIX | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | average time to retirement of supervisory directors |
| 11 | `anl40_overall_timerole` | MATRIX | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | average time in role of overall directors |
| 12 | `anl40_sd_timerole` | MATRIX | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | average time in role of supervisory directors |
| 13 | `anl40_sd_stdevage` | MATRIX | 0.297 | 其他 | 0 | — | — | — | UNUSABLE | standard deviation of directors' ages of supervisory directors |
| 14 | `anl40_turnoverrate` | MATRIX | 0.283 | 价量与波动 | 0 | — | — | — | UNUSABLE | MoveOut / (OldCount + NewCount). No record before 20160729. |
| 15 | `anl40_age` | VECTOR | 0.279 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Age of the mutual board member at the event date |
| 16 | `anl40_relation` | VECTOR | 0.279 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Instrument index identifier of the related company that shares a mutual board member |
| 17 | `anl40_employmentrate` | MATRIX | 0.272 | 宏观与行业 | 0 | — | — | — | UNUSABLE | AddIn / (OldCount + NewCount). No record before 20160729. |
| 18 | `anl40_moveout` | MATRIX | 0.271 | 其他 | 0 | — | — | — | UNUSABLE | Number of leaving directors |
| 19 | `anl40_addin` | MATRIX | 0.271 | 其他 | 0 | — | — | — | UNUSABLE | Number of new directors |
| 20 | `anl40_ed_timerole` | MATRIX | 0.263 | 其他 | 0 | — | — | — | UNUSABLE | average time in role of executive directors |
| 21 | `anl40_ed_genderratio` | MATRIX | 0.262 | 其他 | 0 | — | — | — | UNUSABLE | proportion of male directors of executive directors |
| 22 | `anl40_ed_timeretirement` | MATRIX | 0.262 | 其他 | 0 | — | — | — | UNUSABLE | Average time to retirement of executive directors |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-CREDIT-DEFAULT-ANALYST81-MODEL52`（2026-10-19）family=credit_default：{"batch": "2tRfk57w04Tob49Lqt0jIG2", "best_abs_sharpe": 0.42, "coverage": {"analyst81": 0.2402, "model52": 0.1986}, "date": "2026-10-19", "decision_table": "D15（8 探针无 S >= 0.5 即判死）", "family": "credit_default", "field_trap": "anl81_class / cr_class 用打乱序数的编码（9=AAA,5=AA,4=A,1=BBB,2=BB,3=B,7=CCC,8=CC,6=C,10=D），任何单调算子（rank/zscore/ts_rank）在其上无意义，只能当分组或条件变量。", "id": "EUR-CREDIT-DEFAULT-ANALYST81-MODEL52

