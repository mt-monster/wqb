# earnings6 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `earnings6` |
| 名称 | International Findings Data |
| 类别 | EARNINGS |
| 数据字段数(平台) | 66 |
| 覆盖率 | 0.8203 |
| 平台已有 alpha | 1622 |
| valueScore | 1.0 |
| 金字塔倍率 | 1.2 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset offers daily snapshots of international corporate events, including earnings announcements, conference calls, dividend declarations, shareholder meetings, and other key financial events. It provides detailed metadata such as event status, timing, fiscal period, and confirmation level, along with links to press releases and filings. By tracking the timing and revisions of earnings dates, dividend actions, and other corporate events, the dataset enables researchers and traders to anticipate market-moving disclosures, identify signals of management intent, and exploit calendar-based trading strategies. Its forward-looking coverage and granular event data are valuable for predicting price movements, volatility spikes, and abnormal returns around scheduled corporate actions.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **66** |
| 类型分布 | VECTOR×66 |
| 平均覆盖率 | **0.820** |
| 覆盖率区间 | 0.53 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 良（覆盖 70–90%，sub/robust 需关注） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 29 | 43.9% |
| 中 (0.70–0.90) | 16 | 24.2% |
| 低 (0.50–0.70) | 21 | 31.8% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 57 | 86.4% |
| UNUSABLE | 7 | 10.6% |
| DEAD | 2 | 3.0% |

- 已实测字段：**2** 个（3%），best_sharpe 最高 **0.18**，中位 0.18

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 盈利与财务 | 28 | 0.80 | ern6_1q_221、ern6_2q_222、ern6_3q_223 |
| 其他 | 18 | 0.82 | preliminary_eps_range_upper_bound、ern6_actual_eps、ern6_company_names_213 |
| 修正与预期 | 7 | 0.73 | ern6_estimated_etype_266、ern6_estimated_fiscal_year_267、ern6_estimated_period_268 |
| 元数据与非信号 | 3 | 0.88 | ern6_confpasscode_230、ern6_wqreceivetimestamp_252、ern6_wqreceivetimestamp |
| 搜索与替代数据 | 3 | 0.94 | ern6_goto_broadcast_231、ern6_split_status_255、ern6_actual_source_260 |
| 价量与波动 | 3 | 0.94 | ern6_stock_exchange_214、ern6_ww_status、ern6_eps6ww_status_273 |
| 宏观与行业 | 2 | 0.90 | ern6_isin_212、ern6_actual_currenty_256 |
| 交易与微观结构 | 2 | 0.90 | ern6_stock_symbol、ern6_eps6stock_symbol_271 |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `preliminary_eps_range_upper_bound` | VECTOR | 0.526 | 其他 | 2 | 0.18 | 0.06 | 0.23 | DEAD | High end of the preliminary EPS range, or same as prelim_amount_from if single value |
| 2 | `ern6_actual_eps` | VECTOR | 0.526 | 其他 | 2 | -0.35 | -0.08 | -0.38 | DEAD | Reported non-GAAP diluted (or basic if diluted unavailable) EPS |
| 3 | `ern6_1q_221` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Date for 1st quarter - may be historical |
| 4 | `ern6_2q_222` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Date for 2nd quarter - may be historical |
| 5 | `ern6_3q_223` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Date for 3rd quarter - may be historical |
| 6 | `ern6_4q_224` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings Date for 4th quarter - may be historical |
| 7 | `ern6_company_names_213` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Name of the company |
| 8 | `ern6_confnumber_229` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Publicly available phone number for replay conference call |
| 9 | `ern6_confpasscode_230` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Passcode for replay conference call |
| 10 | `ern6_div_freq_232` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Identifies payment frequency of announced dividend. "ANNUAL", "SEMI-ANNUAL", "QUARTERLY", "MONTHLY" or "SPECIAL" |
| 11 | `ern6_dividend_status_240` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | P - Pays, X - Does not pay, S - Suspended, R - Resumed |
| 12 | `ern6_etype_219` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | T - Tentative date, V - Verified date I - Inferred date See Earnings Date Status Definitions section for additional info |
| 13 | `ern6_goto_broadcast_231` | VECTOR | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Website link for Conference Call recording |
| 14 | `ern6_isin_212` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | This is a unique security identifier structured to include the country in which the issuing company is headquartered, th |
| 15 | `ern6_meeting_status_254` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Possible values are PENDING, INPROCESS, HELD, CANCEL or POSTPONED. |
| 16 | `ern6_mtg_type_248` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Identifies whether it’s a BoD (B) or Shareholder (S) meeting |
| 17 | `ern6_next_ed_216` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Next Earnings Date. See Etype to determine how to interpret this field |
| 18 | `ern6_next_ed_fiscal_year_218` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The fiscal year associated with Next ED and Next ED Quarter |
| 19 | `ern6_next_ed_quarter_217` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Corresponds to the Next ED |
| 20 | `ern6_quarter_215` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The letter "Q" followed by the quarter number the earnings information applies to |
| 21 | `ern6_split_status_255` | VECTOR | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Possible values are PENDINGor APPROVED |
| 22 | `ern6_stock_exchange_214` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | This is the exchange the stock is traded on |
| 23 | `ern6_stock_split_ratio_243` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Split parameters (typically #:#) where the first number is the amount of the new shares, the second number is original s |
| 24 | `ern6_stock_symbol` | VECTOR | 1.000 | 交易与微观结构 | 0 | — | — | — | UNTESTED | This is the stock ticker symbol. A “CA.” prefix is used for companies WSH tracks as Canadian |
| 25 | `ern6_time_of_day_220` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Indicates the time of the announcement: Before Market, During Market, After Market, Unspecified |
| 26 | `ern6_time_zone_228` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Time zone for conference call |
| 27 | `ern6_transcript_quarter_250` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The letter “Q” followed by the quarter number the earnings transcript applies to |
| 28 | `ern6_wqreceivetimestamp_252` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | This is added timestamp at the end of the file with fixed format |
| 29 | `ern6_ww_status` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Denotes whether the security trades on a North American stock exchange (NA) or not (WW) |
| 30 | `ern6_x_dividend_233` | VECTOR | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | Amount of dividend in US dollars. If converted to USD, exchange rate at time of entry is used |
| 31 | `ern6_x_dividend_oc_235` | VECTOR | 0.926 | 盈利与财务 | 0 | — | — | — | UNTESTED | The amount of the dividend in the currency specified by x_dividend_currency |
| 32 | `ern6_board_of_directors_meeting_247` | VECTOR | 0.858 | 其他 | 0 | — | — | — | UNTESTED | Date of Board/Shareholder Meeting |
| 33 | `ern6_actual_currenty_256` | VECTOR | 0.807 | 宏观与行业 | 0 | — | — | — | UNTESTED | Actual Currency |
| 34 | `ern6_actual_period_259` | VECTOR | 0.807 | 盈利与财务 | 0 | — | — | — | UNTESTED | The actual quarter or half year as reported in the earnings announcement |
| 35 | `ern6_actual_source_260` | VECTOR | 0.807 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Possible values are PR (press release), WEBSITE, SEC-SEDAR, OTHER or nulls |
| 36 | `ern6_actual_url_262` | VECTOR | 0.807 | 盈利与财务 | 0 | — | — | — | UNTESTED | The link to the earnings announcement press release or SEC filing |
| 37 | `ern6_company_name_264` | VECTOR | 0.807 | 其他 | 0 | — | — | — | UNTESTED | Name of the company |
| 38 | `ern6_eps6stock_symbol_271` | VECTOR | 0.807 | 交易与微观结构 | 0 | — | — | — | UNTESTED | This is the stock ticker symbol. A “CA.” prefix is used for companies WSH tracks as Canadian |
| 39 | `ern6_eps6ww_status_273` | VECTOR | 0.807 | 价量与波动 | 0 | — | — | — | UNTESTED | Denotes whether the security trades on a North American stock exchange (NA) or not (WW) |
| 40 | `ern6_estimated_etype_266` | VECTOR | 0.807 | 修正与预期 | 0 | — | — | — | UNTESTED | This indicates the status of scheduled earnings date; "Verified" or "Unconfirmed" |
| 41 | `ern6_estimated_fiscal_year_267` | VECTOR | 0.807 | 修正与预期 | 0 | — | — | — | UNTESTED | The fiscal year associated with the quarter or half-year |
| 42 | `ern6_estimated_period_268` | VECTOR | 0.807 | 修正与预期 | 0 | — | — | — | UNTESTED | The scheduled earnings quarter or half year we have a date for |
| 43 | `ern6_estimated_tod_269` | VECTOR | 0.807 | 修正与预期 | 0 | — | — | — | UNTESTED | This indicates the scheduled time of earnings announcement; "Unspecified" or "Before Market" or "During Market" or "Afte |
| 44 | `ern6_estimated_url_270` | VECTOR | 0.807 | 修正与预期 | 0 | — | — | — | UNTESTED | The link to the company website |
| 45 | `ern6_prelim_earnings_link_279` | VECTOR | 0.807 | 盈利与财务 | 0 | — | — | — | UNTESTED | The link to the preliminary earnings announcement press release |
| 46 | `ern6_actual_fiscal_year_258` | VECTOR | 0.795 | 盈利与财务 | 0 | — | — | — | UNTESTED | The fiscal year that corresponds to the earnings release (YYYY) |
| 47 | `ern6_conferencecalltime_227` | VECTOR | 0.752 | 其他 | 0 | — | — | — | UNTESTED | Published time of conference call |
| 48 | `ern6_1q` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings date for the 1st quarter (may be historical) |
| 49 | `ern6_2q` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings date for the 2nd quarter (may be historical) |
| 50 | `ern6_3q` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings date for the 3rd quarter (may be historical) |
| 51 | `ern6_4q` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings date for the 4th quarter (may be historical) |
| 52 | `ern6_board_of_directors_meeting` | VECTOR | 0.637 | 其他 | 0 | — | — | — | UNTESTED | Date of Board/Shareholder Meeting |
| 53 | `ern6_conferencecalltime` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Published time of the earnings conference call |
| 54 | `ern6_next_ed` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Next earnings date (interpret using Etype status) |
| 55 | `ern6_next_ed_fiscal_year` | VECTOR | 0.637 | 其他 | 0 | — | — | — | UNTESTED | Fiscal year associated with Next_ED and Next_ED_QUARTER |
| 56 | `ern6_transcript_fiscal_year` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Fiscal year in YYYY format for the earnings transcript |
| 57 | `ern6_wqreceivetimestamp` | VECTOR | 0.637 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Ingestion timestamp added at file end in a fixed format |
| 58 | `ern6_x_dividend` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | Amount of dividend in US dollars; if converted, uses the exchange rate at time of entry |
| 59 | `ern6_x_dividend_oc` | VECTOR | 0.637 | 盈利与财务 | 0 | — | — | — | UNTESTED | The amount of the dividend in the currency specified by X_Dividend_currency |
| 60 | `ern6_actual_eps_274` | VECTOR | 0.537 | 其他 | 0 | — | — | — | UNUSABLE | The diluted (or basic if diluted not provided) non-GAAP EPS as reported in the press release or filing |
| 61 | `eps_change_absolute_value` | VECTOR | 0.526 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The absolute change in earnings per share compared to the previous period. |
| 62 | `eps_change_percentage_value` | VECTOR | 0.526 | 盈利与财务 | 0 | — | — | — | UNUSABLE | The percentage change in earnings per share compared to the previous period. |
| 63 | `ern6_actual_fiscal_year` | VECTOR | 0.526 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Fiscal year corresponding to the actual earnings release (YYYY) |
| 64 | `ern6_estimated_eps` | VECTOR | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Estimize weighted EPS estimate for the last completed period |
| 65 | `ern6_estimated_fiscal_year` | VECTOR | 0.526 | 修正与预期 | 0 | — | — | — | UNUSABLE | Fiscal year associated with the scheduled (estimated) earnings period |
| 66 | `preliminary_eps_range_lower_bound` | VECTOR | 0.526 | 其他 | 0 | — | — | — | UNUSABLE | Preliminary EPS or the low end of the preliminary EPS range reported by the company |

## 六、本地回测证据

- 本地累计回测 **4** 条；其中 `ra_failed_checks` 为空的 **0** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `rKOdRNkj` | 0.18 | 0.12 | 0.06 | 0.23 | 0.07 | ["LOW_SHARPE | 255 | `reverse(group_rank(ts_backfill(divide(subtract(vec_avg(preliminary_eps_range_upper_bound),` |
| `N1aeNJME` | 0.18 | 0.12 | 0.06 | 0.23 | 0.07 | ["LOW_SHARPE | 255 | `reverse(group_rank(ts_backfill(sign(divide(subtract(vec_avg(preliminary_eps_range_upper_bo` |
| `qMxELYZ2` | -0.35 | -0.23 | -0.08 | -0.38 | 0.07 | ["LOW_SHARPE | 255 | `group_rank(ts_backfill(divide(subtract(vec_avg(ern6_actual_eps),vec_avg(ern6_estimated_eps` |
| `vRrO1p0z` | -0.39 | -0.27 | -0.09 | -0.41 | 0.07 | ["LOW_SHARPE | 255 | `group_rank(ts_backfill(sign(divide(subtract(vec_avg(ern6_actual_eps),vec_avg(ern6_estimate` |

## 七、判死记录（sealed dead_end）

- `EUR-W255-EARNINGS6-EPS-EVENT-PAIRS`（2026-09-25）family=earnings6 normalized EPS surprise and preliminary range SUBINDUSTRY decay4：{"dataset": "earnings6", "wave": "255", "scope": "exact_structures", "whole_dataset_dead": false, "expressions": ["group_rank(ts_backfill(divide(subtract(vec_avg(ern6_actual_eps),vec_avg(ern6_estimated_eps)),max(abs(vec_avg(ern6_actual_eps)),abs(vec_avg(ern6_estimated_eps)))),22),subindustry)", "group_rank(ts_backfill(sign(divide(subtract(vec_avg(ern6_actual_eps),vec_avg(ern6_estimated_eps)),max(a

