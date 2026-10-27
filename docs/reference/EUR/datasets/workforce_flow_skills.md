# workforce_flow_skills — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `workforce_flow_skills` |
| 名称 | Global Workforce Flow and Skills Analytics |
| 类别 | OTHER |
| 数据字段数(平台) | 33 |
| 覆盖率 | 0.2456 |
| 平台已有 alpha | 0 |
| valueScore | 6.0 |
| 金字塔倍率 | 1.5 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive, monthly-tracked information on workforce dynamics, including headcount, inflows, outflows, seniority, roles, skills, salaries, and prestige across thousands of companies and regions. It aggregates data from online professional profiles and job postings, standardizing job titles and skill clusters for robust cross-company and cross-industry analysis. The dataset includes detailed metrics on employee transitions, skill acquisition, layoffs, and sentiment from employee reviews, offering granular insights into talent flow, workforce optimization, and organizational health. By monitoring changes in hiring, attrition, and skill trends, investors and analysts can identify early signals of operational strength or weakness, anticipate company performance shifts,

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **33** |
| 类型分布 | VECTOR×33 |
| 平均覆盖率 | **0.246** |
| 覆盖率区间 | 0.24 ~ 0.25 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 33 | 100.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 33 | 100.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 0 / UNUSABLE 33 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 持仓与资金流 | 25 | 0.25 | employee_headcount、employee_inflow_count、employee_inflow_count_2 |
| 其他 | 5 | 0.25 | adjusted_employee_headcount、employee_headcount_2、unreliable_user_count_2 |
| 风险与质量 | 3 | 0.25 | employee_prestige_score_2、unreliable_user_count、unreliable_user_count_3 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `adjusted_employee_headcount` | VECTOR | 0.250 | 其他 | 0 | — | — | — | UNUSABLE | Scaled count measure used in delta panels (unitless or scaled) |
| 2 | `employee_headcount` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Expected number of employees in the position represented in that row at that date |
| 3 | `employee_headcount_2` | VECTOR | 0.250 | 其他 | 0 | — | — | — | UNUSABLE | Count measure for the record slice (unit = count) |
| 4 | `employee_inflow_count` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly hires/inflow count |
| 5 | `employee_inflow_count_2` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly inflow count (hires/additions during the month) |
| 6 | `employee_outflow_count` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Expected number of employees moving out of the specified position in that month |
| 7 | `employee_outflow_count_2` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly outflow count (departures during the month) |
| 8 | `employee_prestige_score` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Average prestige for employees in the position at that date, based on universities, degrees, and previous companies; corresponds to count |
| 9 | `employee_prestige_score_2` | VECTOR | 0.250 | 风险与质量 | 0 | — | — | — | UNUSABLE | Prestige score for the role/entity (scaled metric) |
| 10 | `position_seniority_level` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | The level of seniority of a position (1 = most junior, 4 = most senior) |
| 11 | `position_seniority_level_2` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Seniority level of the position, from 1 (most junior) to 4 (most senior) |
| 12 | `total_salary_amount` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Expected total salary for employees in the position at the given date, corresponding to count |
| 13 | `total_salary_amount_2` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Expected total salary for employees in the specified position at that date |
| 14 | `unreliable_user_count` | VECTOR | 0.250 | 风险与质量 | 0 | — | — | — | UNUSABLE | Count of records flagged as “bad users” (data quality indicator) |
| 15 | `unreliable_user_count_2` | VECTOR | 0.250 | 其他 | 0 | — | — | — | UNUSABLE | Count of flagged bad user records |
| 16 | `unreliable_user_inflow` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly inflow of flagged “bad user” records (data quality; unit = count) |
| 17 | `unreliable_user_inflow_2` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly inflow count of records flagged as bad users (data quality indicator) |
| 18 | `unreliable_user_outflow` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly outflow count of flagged bad user records (data quality removals) |
| 19 | `unreliable_user_outflow_2` | VECTOR | 0.250 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly outflow count of records flagged as bad users (data quality indicator) |
| 20 | `employee_departure_count` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly outflow count (number of entries removed during the period); unit = count |
| 21 | `employee_headcount_3` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Our expectation of the number of employees in the position represented in that row at that date |
| 22 | `employee_headcount_4` | VECTOR | 0.239 | 其他 | 0 | — | — | — | UNUSABLE | Record count for the specific dataset slice (unit: count) |
| 23 | `employee_incoming_count` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly inflow count (number of entries added during the period); unit = count |
| 24 | `employee_inflow_count_3` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly inflow count (number of hires added in the month); unit = count |
| 25 | `employee_outflow_count_3` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly outflow count for the skill record (number of departures; unit = count) |
| 26 | `position_experience_level` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Seniority level label describing the job/employee hierarchy (string) |
| 27 | `position_seniority_level_3` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Seniority level label in the employment hierarchy (string) |
| 28 | `unreliable_entries_departing` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly outflow of flagged bad user records; unit = count |
| 29 | `unreliable_entries_incoming` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly inflow of flagged bad user records; unit = count |
| 30 | `unreliable_user_count_3` | VECTOR | 0.239 | 风险与质量 | 0 | — | — | — | UNUSABLE | Count of records flagged as “bad users” (data quality indicator; unit = count) |
| 31 | `unreliable_user_count_4` | VECTOR | 0.239 | 其他 | 0 | — | — | — | UNUSABLE | Count of flagged bad user records; unit = count |
| 32 | `unreliable_user_inflow_3` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly inflow count of flagged “bad users” (data quality flag) |
| 33 | `unreliable_user_outflow_3` | VECTOR | 0.239 | 持仓与资金流 | 0 | — | — | — | UNUSABLE | Monthly outflow count of flagged “bad users” (data quality flag) |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

