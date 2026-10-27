# fundamental1 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `fundamental1` |
| 名称 | Management and Executive Data |
| 类别 | FUNDAMENTAL |
| 数据字段数(平台) | 183 |
| 覆盖率 | 0.5096 |
| 平台已有 alpha | 180 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.1 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides comprehensive biographical and professional information on board members and senior executives from companies worldwide. It includes details such as employment history, education, achievements, compensation, board roles, committee memberships, and network connections across organizations. By analyzing board composition, director expertise, compensation structures, and interlocking directorates, investors and researchers can assess governance quality, leadership stability, and potential strategic shifts. These insights are valuable for predicting price movements, as changes in executive leadership, board structure, or director networks often precede significant corporate actions, impact investor sentiment, and influence firm performance.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **183** |
| 类型分布 | VECTOR×183 |
| 平均覆盖率 | **0.510** |
| 覆盖率区间 | 0.22 ~ 0.65 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 中（覆盖 50–70%，截面偏窄） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 118 | 64.5% |
| 稀疏 (<0.50) | 65 | 35.5% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 118 | 64.5% |
| UNUSABLE | 65 | 35.5% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 118 / UNUSABLE 65 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 68 | 0.50 | aggregate_director_compensation_2、annual_base_salary、annual_bonus_payment |
| 价量与波动 | 58 | 0.50 | intrinsic_value_options_awarded_2、intrinsic_value_options_held_2、ltip_award_value_2 |
| 元数据与非信号 | 28 | 0.63 | current_other_board_total、current_other_listed_boards_count_2、fnd1_board_characteristics_noquals |
| 修正与预期 | 14 | 0.37 | estimated_value_options_awarded_2、estimated_value_options_held、estimated_option_value_held |
| 宏观与行业 | 7 | 0.37 | compensation_currency_code_2、compensation_currency_code、monetary_unit_code |
| 盈利与财务 | 6 | 0.65 | equity_linked_compensation_ratio_2、total_equity_at_risk_2、total_equity_linked_wealth_2 |
| 风险与质量 | 2 | 0.65 | fnd1_succession、fnd1_filtered_succession |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `aggregate_director_compensation_2` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Sum of the director's salary and bonus for the report period |
| 2 | `annual_base_salary` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Base annual cash salary for the director in the report period |
| 3 | `annual_bonus_payment` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Bonus payment received by the director during the report period |
| 4 | `bonus_proportion_total_comp` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Bonus amount as a proportion of total direct compensation excluding defined contribution pension |
| 5 | `compensation_change_percent_2` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Percentage change in total compensation from previous report period for the director |
| 6 | `compensation_currency_code_2` | VECTOR | 0.648 | 宏观与行业 | 0 | — | — | — | UNTESTED | ISO code of the currency in which all reported values are displayed |
| 7 | `employer_pension_contribution_2` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Employer’s defined pension contribution for each director during the reporting period |
| 8 | `equity_linked_compensation_ratio_2` | VECTOR | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Equity-linked compensation (such as shares/options/LTIPs) as a proportion of total compensation, based on annual report date stock price |
| 9 | `estimated_value_options_awarded_2` | VECTOR | 0.648 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated value of options awarded to the director during the period, based on closing stock price from the annual report date |
| 10 | `estimated_value_options_held` | VECTOR | 0.648 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated value of options held at end of period by the director, valued at annual report closing price |
| 11 | `intrinsic_value_options_awarded_2` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Intrinsic value of options awarded during the period, valued at annual report date closing stock price |
| 12 | `intrinsic_value_options_held_2` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of stock options held by the director at period end, using closing stock price from the annual report date |
| 13 | `ltip_award_value_2` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of Long-Term Incentive Plans (LTIPs) awarded during the period, valued at closing stock price on the annual report date |
| 14 | `ltip_plan_value_held_2` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of LTIPs held at period end, valued at closing stock price on annual report date |
| 15 | `ltip_to_total_remuneration_ratio_2` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Ratio of LTIP value to total awards for the period (LTIPValue/TotRemPeriod) |
| 16 | `other_cash_payments_2` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Annual value of ad hoc cash payments such as relocation allowances |
| 17 | `share_award_value_2` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of shares awarded during the period, using closing stock price on the annual report date |
| 18 | `total_director_cash_comp` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Total direct compensation: sum of salary, bonus, other cash, and pension employer contributions for the director |
| 19 | `total_equity_at_risk_2` | VECTOR | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total stock |
| 20 | `total_equity_linked_wealth_2` | VECTOR | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total valuation of director’s equity-linked wealth at period end, calculated at closing stock price of the annual report date |
| 21 | `total_remuneration_period` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Total remuneration or awards received by the director during the period |
| 22 | `total_shareholding_value_2` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of shares held by the director at the end of the reporting period, calculated using the annual report date's closing stock price |
| 23 | `wealth_sensitivity_to_stock_2` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the director's company-specific wealth for a 1% change in stock price at the annual report date, as valued at that date |
| 24 | `aggregate_director_compensation` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Sum of salary and bonus received by the director for the report period |
| 25 | `bonus_to_compensation_ratio` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Bonus as a proportion of total direct compensation less defined contribution pension for the director |
| 26 | `compensation_change_percent` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Percentage change in the director's total compensation compared to the previous reporting period |
| 27 | `compensation_currency_code` | VECTOR | 0.648 | 宏观与行业 | 0 | — | — | — | UNTESTED | ISO currency code representing the currency in which all values in the row are displayed |
| 28 | `director_base_salary` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Base annual cash salary paid to the director during the reported period |
| 29 | `director_bonus_payment` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Bonus payments received by the director during the report period |
| 30 | `employer_pension_contribution` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Employer's defined contribution to the director's pension for each report period |
| 31 | `equity_linked_compensation_ratio` | VECTOR | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Ratio of equity-linked compensation to total compensation for the director, calculated at closing stock price |
| 32 | `estimated_option_value_held` | VECTOR | 0.648 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated value of options held by the director at the end of the reporting period, calculated at the closing stock price of the annual repo |
| 33 | `estimated_value_options_awarded` | VECTOR | 0.648 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated valuation of options awarded to the director during the period, calculated at the closing stock price on the report date |
| 34 | `intrinsic_value_options_awarded` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Intrinsic value of options awarded to the director during the period, valued at closing stock price on the report date |
| 35 | `intrinsic_value_options_held` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Valuation of stock options held by the director at period end, using the closing share price on the annual report date |
| 36 | `ltip_award_value` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of long-term incentive plan (LTIP) awards granted during the period, measured at the closing stock price of the report date |
| 37 | `ltip_plan_value_held` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of long-term incentive plans (LTIPs) held by the director at the end of the period, at closing stock price |
| 38 | `ltip_to_total_remuneration_ratio` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Ratio of LTIP value to total compensation for the director during the report period |
| 39 | `other_cash_payments` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Annual ad hoc cash payments made to the director, such as relocation allowances or similar items |
| 40 | `share_award_value` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of shares awarded to the director during the reporting period, measured at closing stock price |
| 41 | `total_awards_period` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Total compensation or awards received by the director for the reporting period |
| 42 | `total_director_cash_compensation` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Total direct compensation received by the director, calculated as Salary plus Bonus plus Other plus PenEmpCont (Pension/Employer contributio |
| 43 | `total_equity_at_risk` | VECTOR | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value or volume of equity at risk (held or awarded shares and options) |
| 44 | `total_equity_linked_wealth` | VECTOR | 0.648 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total value of equity-linked wealth (e.g., shares, options) held by the director at the end of the period, valued using closing stock price  |
| 45 | `total_shareholding_value` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Value of shares held by the individual director at the end of the reporting period, measured at the closing stock price of the annual report |
| 46 | `wealth_sensitivity_to_stock` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Change in the director's wealth in the company for a 1% change in share price at the annual report date; calculated using holdings and the c |
| 47 | `board_nationality_diversity_ratio_2` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Proportion of directors from different countries among executive directors (board nationality diversity) |
| 48 | `current_other_board_total` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of other boards the director serves on as of the selected annual report date |
| 49 | `current_other_listed_boards_count_2` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of other boards the individual currently serves on as of the annual report date |
| 50 | `director_attrition_ratio_2` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Proportion of executive directors who have left roles relative to average number for the preceding reporting period |
| 51 | `director_attrition_ratio_3yr` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Proportion of executive directors who have left roles relative to average number for the preceding 3 years |
| 52 | `fnd1_board_characteristics_avgtimeothco` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Average time executive directors serve on other quoted boards (excluding the one analyzed) |
| 53 | `fnd1_board_characteristics_noquals` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Total number of educational qualifications at undergraduate level or above as of the annual report date |
| 54 | `fnd1_board_characteristics_timebrd` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Average time spent on the board by executive directors as of the selected annual report date |
| 55 | `fnd1_board_characteristics_timeinco` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Average time spent at the company by executive directors as of the selected annual report date |
| 56 | `fnd1_board_characteristics_timeretirement` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Average time to retirement for executive directors as of the selected annual report date |
| 57 | `fnd1_board_characteristics_timerole` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | The average length of time executive directors have served in their current role |
| 58 | `fnd1_board_characteristics_totcurrnolstdbrd` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | The average number of quoted (public) boards currently served on by executive directors in the company |
| 59 | `fnd1_board_characteristics_totcurrnounlstdbrd` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | The average number of private (unlisted) boards currently served on by executive directors in the company |
| 60 | `fnd1_board_characteristics_totnolstdbrd` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | The average cumulative number of quoted (public) boards served on over time by executive directors |
| 61 | `fnd1_board_characteristics_totnounlstdbrd` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Average number of private boards served on over time by Executive Directors |
| 62 | `fnd1_director_characteristics_avgtimeothco` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Average time the director sits on boards of quoted (public) companies |
| 63 | `fnd1_director_characteristics_noquals` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Total number of educational qualifications (undergraduate and above) for the director as of the selected annual report date |
| 64 | `fnd1_director_characteristics_timebrd` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Time spent by the director on the board as of the selected annual report date |
| 65 | `fnd1_director_characteristics_timeinco` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Time spent by the director in the company as of the selected annual report date |
| 66 | `fnd1_director_characteristics_timeretirement` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of years or time until the director's retirement at the annual report date |
| 67 | `fnd1_director_characteristics_timerole` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Time spent by the director in their current role as of the selected annual report date |
| 68 | `fnd1_director_characteristics_totcurrnolstdbrd` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of quoted (public) boards the director serves on as of the selected annual report date |
| 69 | `fnd1_director_characteristics_totcurrnounlstdbrd` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of private (unlisted) boards the director serves on as of the selected annual report date |
| 70 | `fnd1_director_characteristics_totnolstdbrd` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Total number of quoted (publicly-listed) boards the director has served on historically up to the selected annual report date |
| 71 | `fnd1_director_characteristics_totnounlstdbrd` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Total number of private (unlisted) boards served by the director up to the selected annual report date |
| 72 | `fnd1_genderratio` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Proportion of male directors among executive directors |
| 73 | `fnd1_numberdirectors` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Number of Executive Directors on the board |
| 74 | `fnd1_stdevage` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of ages of Executive Directors |
| 75 | `fnd1_stdevnoquals` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | The standard deviation of the number of educational qualifications (undergraduate and above) for executive directors |
| 76 | `fnd1_stdevtimebrd` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of “time on board” for executive directors (i.e., how long they have sat on boards) |
| 77 | `fnd1_stdevtimeincompany` | VECTOR | 0.648 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of time in company among executive directors |
| 78 | `fnd1_stdevtotcurrnolstdbrd` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the number of quoted boards currently served on by executive directors |
| 79 | `fnd1_stdevtotnolstdbrd` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of total number of quoted boards served on over time among executive directors |
| 80 | `fnd1_succession` | VECTOR | 0.648 | 风险与质量 | 0 | — | — | — | UNTESTED | Degree to which Executive Directors’ ages are clustered near retirement age, indicating succession risk |
| 81 | `other_board_total_count` | VECTOR | 0.648 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Total number of other boards the director has served on up to the selected annual report date |
| 82 | `total_other_listed_boards_count_2` | VECTOR | 0.648 | 价量与波动 | 0 | — | — | — | UNTESTED | Total number of other (non-quoted, non-private) boards an individual has served on as of the annual report date |
| 83 | `board_nationality_diversity_ratio` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Proportion of executive directors from different countries on the board |
| 84 | `current_other_listed_boards_count` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of other types of boards (neither quoted nor private) an executive director serves on as of the annual report date |
| 85 | `director_attrition_ratio` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Proportion of executive directors who left since previous period to average number of directors in previous period |
| 86 | `director_current_other_listed_boards_count` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of other types of boards the individual currently serves on at the selected date |
| 87 | `director_total_other_listed_boards_count` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Total number of other types of boards the individual has served on up to the selected date |
| 88 | `fnd1_board_characteristics_filtered_avgtimeothco` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Average time executive directors sit on the boards of quoted companies (excluding current organization) |
| 89 | `fnd1_board_characteristics_filtered_noquals` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Total number of educational qualifications undergraduate and above held by the individual |
| 90 | `fnd1_board_characteristics_filtered_timebrd` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Length of time the individual has served on the board up to the annual report date |
| 91 | `fnd1_board_characteristics_filtered_timeinco` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Tenure of the individual at the company as of the annual report date |
| 92 | `fnd1_board_characteristics_filtered_timeretirement` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Time to retirement for the individual at the chosen AnnualReportDate |
| 93 | `fnd1_board_characteristics_filtered_timerole` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Time in current role for the individual at the chosen AnnualReportDate |
| 94 | `fnd1_board_characteristics_filtered_totcurrnolstdbrd` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of quoted (publicly listed) boards an executive director serves on as of the annual report date |
| 95 | `fnd1_board_characteristics_filtered_totcurrnounlstdbrd` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of private (non-quoted) boards an executive director serves on as of the annual report date |
| 96 | `fnd1_board_characteristics_filtered_totnolstdbrd` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Total number of quoted (public) boards an individual has served up to the AnnualReportDate |
| 97 | `fnd1_board_characteristics_filtered_totnounlstdbrd` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Total number of private (non-quoted) boards an executive director has ever served on to date |
| 98 | `fnd1_director_characteristics_filtered_avgtimeothco` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Average time the director sits on the boards of other quoted companies |
| 99 | `fnd1_director_characteristics_filtered_noquals` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Total number of educational qualifications (undergraduate and above) held by the individual |
| 100 | `fnd1_director_characteristics_filtered_timebrd` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Length of time the individual has served on the board at the selected annual report date |
| 101 | `fnd1_director_characteristics_filtered_timeinco` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Total time the individual has been with the company at the selected annual report date |
| 102 | `fnd1_director_characteristics_filtered_timeretirement` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Time to retirement for the individual at the selected annual report date |
| 103 | `fnd1_director_characteristics_filtered_timerole` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Length of time the individual has served in the current role at the selected annual report date |
| 104 | `fnd1_director_characteristics_filtered_totcurrnolstdbrd` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Number of quoted boards the individual currently serves on at the selected date |
| 105 | `fnd1_director_characteristics_filtered_totcurrnounlstdbrd` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Number of private boards the individual currently serves on at the selected date |
| 106 | `fnd1_director_characteristics_filtered_totnolstdbrd` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Total number of quoted (public) boards the individual has served on up to the selected date |
| 107 | `fnd1_director_characteristics_filtered_totnounlstdbrd` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Total number of private boards the individual has served on up to the selected date |
| 108 | `fnd1_filtered_attrition3yr` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Proportion of executive directors who left over the preceding 3 years compared to average number of directors in that period |
| 109 | `fnd1_filtered_genderratio` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Proportion of male executive directors on the board |
| 110 | `fnd1_filtered_numberdirectors` | VECTOR | 0.647 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Total number of executive directors as of the annual report date |
| 111 | `fnd1_filtered_stdevage` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation across the executive directors on the board for their ages (how spread out the ages are among executive directors) |
| 112 | `fnd1_filtered_stdevnoquals` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation across the executive directors on the board for the number of educational or professional qualifications each executive d |
| 113 | `fnd1_filtered_stdevtimebrd` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of time served on board among executive directors |
| 114 | `fnd1_filtered_stdevtimeincompany` | VECTOR | 0.647 | 其他 | 0 | — | — | — | UNTESTED | Standard deviation of time in company among executive directors |
| 115 | `fnd1_filtered_stdevtotcurrnolstdbrd` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of the number of quoted boards currently served on by executive directors in the board |
| 116 | `fnd1_filtered_stdevtotnolstdbrd` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Standard deviation of total quoted boards served among executive directors |
| 117 | `fnd1_filtered_succession` | VECTOR | 0.647 | 风险与质量 | 0 | — | — | — | UNTESTED | Measure of how many directors are clustered near retirement age (succession risk) |
| 118 | `total_other_listed_boards_count` | VECTOR | 0.647 | 价量与波动 | 0 | — | — | — | UNTESTED | Total number of other boards (neither quoted nor private) an executive director has served on to date |
| 119 | `cash_incentive_plan_value` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Value of any cash-based incentive plan awarded |
| 120 | `estimated_value_exercisable_options` | VECTOR | 0.299 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated value of exercisable options awarded in the period, valued at closing stock price on annual report date |
| 121 | `estimated_value_unexercisable_options` | VECTOR | 0.299 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated value of unexercisable options awarded in the period, valued at closing stock price on annual report date |
| 122 | `exercisable_option_quantity` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Maximum number of exercisable options awarded for that incentive plan in the period |
| 123 | `expired_option_quantity` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Number of expired options in the incentive plan |
| 124 | `intrinsic_value_exercisable_options` | VECTOR | 0.299 | 价量与波动 | 0 | — | — | — | UNUSABLE | Exercise price at which the exercisable options can be exercised |
| 125 | `intrinsic_value_unexercisable_options` | VECTOR | 0.299 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation of unexercisable options awarded in the period, using the closing stock price at the annual report date |
| 126 | `ltip_wealth_stock_price` | VECTOR | 0.299 | 价量与波动 | 0 | — | — | — | UNUSABLE | Stock price for the awarded security on the annual report date |
| 127 | `matched_share_award_quantity` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Maximum number of shares awarded plus the matched percentage in the period under a specific incentive plan |
| 128 | `matched_share_award_value` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Value of shares awarded plus matched percentage for the given incentive plan |
| 129 | `monetary_unit_code` | VECTOR | 0.299 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO code of the currency in which all monetary values are reported |
| 130 | `option_strike_price` | VECTOR | 0.299 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price at which awarded options can be exercised |
| 131 | `share_award_quantity` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Maximum number of shares awarded during the period for the specified incentive plan |
| 132 | `share_award_value_3` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Total value of shares awarded for a given incentive plan |
| 133 | `unexercisable_option_quantity` | VECTOR | 0.299 | 其他 | 0 | — | — | — | UNUSABLE | Maximum number of unexercisable options awarded for the incentive plan in the period |
| 134 | `cash_incentive_plan_value_ltip` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Value held in cash-based incentive plans for the director or period |
| 135 | `estimated_value_exercisable_options_ltip` | VECTOR | 0.290 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated valuation of exercisable options awarded in the period |
| 136 | `estimated_value_unexercisable_options_ltip` | VECTOR | 0.290 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated valuation of unexercisable options awarded in the period |
| 137 | `exercisable_option_quantity_ltip` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Number of exercisable options awarded in the incentive plan |
| 138 | `expired_option_quantity_ltip` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Number of expired options in the incentive plan |
| 139 | `intrinsic_value_exercisable_options_ltip` | VECTOR | 0.290 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation of exercisable options awarded, based on closing stock price at annual report date |
| 140 | `intrinsic_value_unexercisable_options_ltip` | VECTOR | 0.290 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation of unexercisable options awarded, based on closing stock price at annual report date |
| 141 | `matched_share_award_quantity_ltip` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Maximum number of shares awarded plus any matched percentage in the period for the relevant incentive plan |
| 142 | `matched_share_award_value_ltip` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Total value of shares awarded, including the value of any additional matched shares, for a given incentive plan during the period |
| 143 | `monetary_unit_code_ltip` | VECTOR | 0.290 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO 4217 code of the currency used for monetary values in this module |
| 144 | `option_strike_price_ltip` | VECTOR | 0.290 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price at which awarded options can be exercised |
| 145 | `security_market_price_ltip` | VECTOR | 0.290 | 价量与波动 | 0 | — | — | — | UNUSABLE | Stock price at the grant date (or annual report date) for the awarded plan |
| 146 | `share_award_quantity_ltip` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Maximum number of shares awarded in the period for a given incentive plan |
| 147 | `share_award_value_ltip` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Value of shares awarded for a given incentive plan |
| 148 | `unexercisable_option_quantity_ltip` | VECTOR | 0.290 | 其他 | 0 | — | — | — | UNUSABLE | Number of unexercisable options awarded in the incentive plan |
| 149 | `exercisable_option_estimated_value` | VECTOR | 0.255 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated value of exercisable options awarded, valued at the closing stock price |
| 150 | `exercisable_option_intrinsic_value` | VECTOR | 0.255 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation of exercisable options, usually at the period's closing stock price |
| 151 | `exercisable_option_volume` | VECTOR | 0.255 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of exercisable options awarded in the incentive plan |
| 152 | `expired_option_volume` | VECTOR | 0.255 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of expired options in the director's incentive plan |
| 153 | `option_exercise_price` | VECTOR | 0.255 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price at which options can be exercised by the director |
| 154 | `option_plan_currency_code` | VECTOR | 0.255 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO code of the currency in which financial values are expressed |
| 155 | `option_plan_stock_price` | VECTOR | 0.255 | 价量与波动 | 0 | — | — | — | UNUSABLE | Closing price of the stock at the time of the annual report or the relevant award date |
| 156 | `unexercisable_option_estimated_value` | VECTOR | 0.255 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated value of unexercisable options awarded, valued at the closing stock price |
| 157 | `unexercisable_option_intrinsic_value` | VECTOR | 0.255 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation of unexercisable options, usually at the closing stock price for the period |
| 158 | `unexercisable_option_volume` | VECTOR | 0.255 | 价量与波动 | 0 | — | — | — | UNUSABLE | Number of unexercisable options awarded in the incentive plan |
| 159 | `cash_incentive_plan_value_ltipw` | VECTOR | 0.218 | 其他 | 0 | — | — | — | UNUSABLE | Value of any cash-based incentive plan held |
| 160 | `estimated_value_exercisable_options_ltipw` | VECTOR | 0.218 | 修正与预期 | 0 | — | — | — | UNUSABLE | Valuation of exercisable options awarded in the period at closing price |
| 161 | `estimated_value_unexercisable_options_ltipw` | VECTOR | 0.218 | 修正与预期 | 0 | — | — | — | UNUSABLE | Valuation of unexercisable options awarded in the period at closing price |
| 162 | `exercisable_option_quantity_ltipw` | VECTOR | 0.218 | 其他 | 0 | — | — | — | UNUSABLE | Number of exercisable options awarded in that plan |
| 163 | `expired_option_quantity_ltipw` | VECTOR | 0.218 | 其他 | 0 | — | — | — | UNUSABLE | Number of expired options in the incentive plan |
| 164 | `intrinsic_value_exercisable_options_ltipw` | VECTOR | 0.218 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation of exercisable options at closing stock price of the report date |
| 165 | `intrinsic_value_unexercisable_options_ltipw` | VECTOR | 0.218 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation of unexercisable options at closing stock price of the report date |
| 166 | `matched_share_award_quantity_ltipw` | VECTOR | 0.218 | 其他 | 0 | — | — | — | UNUSABLE | Maximum number of shares awarded plus the matched percentage in the period for a specific conditional LTIP incentive plan |
| 167 | `matched_share_award_value_ltipw` | VECTOR | 0.218 | 其他 | 0 | — | — | — | UNUSABLE | Monetary value of shares awarded plus the matched percentage for a specific incentive plan |
| 168 | `monetary_unit_code_ltipw` | VECTOR | 0.218 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO currency code in which all values are shown |
| 169 | `option_strike_price_ltipw` | VECTOR | 0.218 | 价量与波动 | 0 | — | — | — | UNUSABLE | Exercise price at which options can be exercised |
| 170 | `security_market_price_ltipw` | VECTOR | 0.218 | 价量与波动 | 0 | — | — | — | UNUSABLE | Stock price of the awarded stock at the annual report date |
| 171 | `share_award_quantity_ltipw` | VECTOR | 0.218 | 其他 | 0 | — | — | — | UNUSABLE | Maximum number of shares awarded in the period for a given incentive plan |
| 172 | `share_award_value_ltipw` | VECTOR | 0.218 | 其他 | 0 | — | — | — | UNUSABLE | Value of shares awarded for a given incentive plan |
| 173 | `unexercisable_option_quantity_ltipw` | VECTOR | 0.218 | 其他 | 0 | — | — | — | UNUSABLE | Number of unexercisable options awarded in that plan |
| 174 | `estimated_value_exercisable_options_opt` | VECTOR | 0.217 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated value of exercisable options awarded in the period, valued at the closing stock price of the selected annual report date |
| 175 | `estimated_value_unexercisable_options_opt` | VECTOR | 0.217 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimated value of unexercisable options awarded in the period, valued at the closing stock price of the annual report date |
| 176 | `exercisable_option_quantity_opt` | VECTOR | 0.217 | 其他 | 0 | — | — | — | UNUSABLE | Number of exercisable options awarded under the plan for the director |
| 177 | `expired_option_quantity_opt` | VECTOR | 0.217 | 其他 | 0 | — | — | — | UNUSABLE | Number of expired options under the conditional incentive plan for the director |
| 178 | `intrinsic_value_exercisable_options_opt` | VECTOR | 0.217 | 元数据与非信号 | 0 | — | — | — | UNUSABLE | Valuation of exercisable options awarded in the period, calculated at the annual report date |
| 179 | `intrinsic_value_unexercisable_options_opt` | VECTOR | 0.217 | 价量与波动 | 0 | — | — | — | UNUSABLE | Valuation of unexercisable options awarded in the period, valued at the closing stock price of the annual report date |
| 180 | `monetary_unit_code_opt` | VECTOR | 0.217 | 宏观与行业 | 0 | — | — | — | UNUSABLE | ISO code representing the currency for all monetary values in this record |
| 181 | `option_strike_price_opt` | VECTOR | 0.217 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price at which awarded options can be exercised by the director |
| 182 | `security_market_price_opt` | VECTOR | 0.217 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price of the stock as of the relevant report date, used for valuing awards |
| 183 | `unexercisable_option_quantity_opt` | VECTOR | 0.217 | 其他 | 0 | — | — | — | UNUSABLE | Number of unexercisable options awarded under the plan for the director |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

- `EUR-W251-FUNDAMENTAL17-QUALITY-PROBE`（2026-09-24）family=fundamental17 operating-quality changes and matched levels：{"dataset": "fundamental17", "wave": 251, "delay": 1, "universe": "TOPCS1600", "settings": "SUBINDUSTRY decay4 truncation.08", "scope": "12 exact expressions in selection_w251 only; not entire dataset", "best_alpha": "N1aeg3pp", "best_sharpe": 1.18, "same_alpha_fitness": 0.8, "two_year_sharpe": 0.43, "reason": "No candidate reaches joint Sharpe>=1.25 and Fitness>=.8; slow turnover 1.00%-2.11%; lev
- `EUR-W252-FUNDAMENTAL17-MEASUREMENT-RETEST`（2026-09-24）family=fundamental17 reported earnings level and accounting adjustment：{"dataset": "fundamental17", "wave": 252, "delay": 1, "universe": "TOPCS1600", "scope": "2 exact selection_w252 expressions and current settings only", "evidence": [{"alpha_id": "QPbYaMlK", "role": "reported_income_level", "sharpe": 1.13, "fitness": 0.75, "two_year_sharpe": 0.47, "rn_sharpe": 0.52, "turnover": 0.0112, "sub_sharpe": 0.71, "robust_sharpe": 0.9, "units_warning": false, "failed_ra": [

