# EUR / D1 / TOP2500 — earnings 类别字段完备画像（2026-11-19）

> 范围：EUR region、delay 1、universe TOP2500 下的 **earnings 类别全部数据集**。
> 口径：**全字段探测，禁止抽样**——字段全表 = 平台 `get_datafields` 返回的全量（含被默认 sharpe 过滤剔除的字段，本次用 `filter_sharpe=false` 拉取）。
> 数据源：`mcp__wq-brain-http__get_datafields`（platform catalog，`complete=true`）。
> 目录快照：earnings6 于 `2026-11-10T19:25:56`、earnings_sent_matrix 于 `2026-11-17T16:12:17` 抓取；与 2026-11-19 平台读数逐位一致（抽样核对 `ern6_3q` 127/173、`ern6_actual_eps` 107/142、`ern6_quarter_215` 169/216）。

## 1. 数据集概览

| 数据集 | 名称 | 类别 | 字段数 | 覆盖率 | userCount | alphaCount | 塔倍率 |
|---|---|---|---:|---:|---:|---:|---:|
| `earnings6` | International Findings Data | earnings | 66 | 0.8203 | 1014 | 3442 | 1.2 |
| `earnings_sent_matrix` | Global Earnings Call Sentiment Matrix | earnings | 7 | 0.5062 | 666 | 1532 | 1.2 |

**结构性事实**

- `earnings6` 的 66 个字段**全部是 VECTOR 类型**：表达式里必须经 `vec_*` 聚合（`vec_avg` / `vec_sum` / `vec_max` 等）降维后才能进信号，否则平台直接语法错。
- `earnings_sent_matrix` 的 7 个字段**全部是 MATRIX 类型**且覆盖率同为 0.5062（同一份日内电话会切片的三种输出）。
- 两个数据集都是**事件驱动**（财报/电话会/股息公告/股东大会），非日频连续量：零膨胀严重，裸水平值多为常数 0。

## 2. 字段全表

> 本节是分母：逐字段列出真实 id，无通配、无「同构孪生」省略。`dateCoverage` 是平台口径的日期覆盖比例（非起止日期）。

| 字段 | 数据集 | 类型 | 覆盖率 | userCount | alphaCount | dateCreated | dateCoverage |
|---|---|---|---:|---:|---:|---|---:|
| `eps_change_absolute_value` | earnings6 | VECTOR | 0.5258 | 16 | 17 | 2025-11-01 | 0.5307 |
| `eps_change_percentage_value` | earnings6 | VECTOR | 0.5258 | 9 | 9 | 2025-11-01 | 0.5307 |
| `ern6_1q` | earnings6 | VECTOR | 0.6372 | 88 | 127 | 2025-11-01 | 0.6624 |
| `ern6_1q_221` | earnings6 | VECTOR | 1.0 | 17 | 20 | 2024-06-01 | 0.6624 |
| `ern6_2q` | earnings6 | VECTOR | 0.6372 | 66 | 76 | 2025-11-01 | 0.6624 |
| `ern6_2q_222` | earnings6 | VECTOR | 1.0 | 8 | 8 | 2024-06-01 | 0.6624 |
| `ern6_3q` | earnings6 | VECTOR | 0.6372 | 127 | 173 | 2025-11-01 | 0.6624 |
| `ern6_3q_223` | earnings6 | VECTOR | 1.0 | 28 | 35 | 2024-06-01 | 0.6624 |
| `ern6_4q` | earnings6 | VECTOR | 0.6372 | 67 | 76 | 2025-11-01 | 0.6624 |
| `ern6_4q_224` | earnings6 | VECTOR | 1.0 | 17 | 19 | 2024-06-01 | 0.6624 |
| `ern6_actual_currenty_256` | earnings6 | VECTOR | 0.8075 | 41 | 46 | 2024-07-01 | 0.5307 |
| `ern6_actual_eps` | earnings6 | VECTOR | 0.5258 | 107 | 142 | 2025-11-01 | 0.5307 |
| `ern6_actual_eps_274` | earnings6 | VECTOR | 0.5367 | 13 | 14 | 2024-06-01 | 0.5307 |
| `ern6_actual_fiscal_year` | earnings6 | VECTOR | 0.5258 | 84 | 106 | 2025-11-01 | 0.5307 |
| `ern6_actual_fiscal_year_258` | earnings6 | VECTOR | 0.795 | 15 | 15 | 2024-06-01 | 0.5307 |
| `ern6_actual_period_259` | earnings6 | VECTOR | 0.8075 | 50 | 57 | 2024-06-01 | 0.5307 |
| `ern6_actual_source_260` | earnings6 | VECTOR | 0.8075 | 57 | 67 | 2024-06-01 | 0.5307 |
| `ern6_actual_url_262` | earnings6 | VECTOR | 0.8075 | 55 | 64 | 2024-06-01 | 0.5307 |
| `ern6_board_of_directors_meeting` | earnings6 | VECTOR | 0.6372 | 47 | 50 | 2025-11-01 | 0.6624 |
| `ern6_board_of_directors_meeting_247` | earnings6 | VECTOR | 0.8575 | 10 | 10 | 2024-06-01 | 0.6624 |
| `ern6_company_name_264` | earnings6 | VECTOR | 0.8075 | 36 | 44 | 2024-06-01 | 0.5307 |
| `ern6_company_names_213` | earnings6 | VECTOR | 1.0 | 20 | 23 | 2024-06-01 | 0.6624 |
| `ern6_conferencecalltime` | earnings6 | VECTOR | 0.6372 | 65 | 74 | 2025-11-01 | 0.6624 |
| `ern6_conferencecalltime_227` | earnings6 | VECTOR | 0.7517 | 25 | 28 | 2024-06-01 | 0.6624 |
| `ern6_confnumber_229` | earnings6 | VECTOR | 1.0 | 43 | 52 | 2024-06-01 | 0.6624 |
| `ern6_confpasscode_230` | earnings6 | VECTOR | 1.0 | 11 | 11 | 2024-06-01 | 0.6624 |
| `ern6_div_freq_232` | earnings6 | VECTOR | 1.0 | 33 | 44 | 2024-07-01 | 0.6624 |
| `ern6_dividend_status_240` | earnings6 | VECTOR | 1.0 | 47 | 53 | 2024-06-01 | 0.6624 |
| `ern6_eps6stock_symbol_271` | earnings6 | VECTOR | 0.8075 | 65 | 76 | 2024-07-01 | 0.5307 |
| `ern6_eps6ww_status_273` | earnings6 | VECTOR | 0.8075 | 41 | 52 | 2024-06-01 | 0.5307 |
| `ern6_estimated_eps` | earnings6 | VECTOR | 0.5258 | 54 | 64 | 2025-11-01 | 0.5307 |
| `ern6_estimated_etype_266` | earnings6 | VECTOR | 0.8075 | 56 | 72 | 2024-07-01 | 0.5307 |
| `ern6_estimated_fiscal_year` | earnings6 | VECTOR | 0.5258 | 92 | 122 | 2025-11-01 | 0.5307 |
| `ern6_estimated_fiscal_year_267` | earnings6 | VECTOR | 0.8075 | 7 | 7 | 2024-06-01 | 0.5307 |
| `ern6_estimated_period_268` | earnings6 | VECTOR | 0.8075 | 34 | 40 | 2024-06-01 | 0.5307 |
| `ern6_estimated_tod_269` | earnings6 | VECTOR | 0.8075 | 47 | 60 | 2024-07-01 | 0.5307 |
| `ern6_estimated_url_270` | earnings6 | VECTOR | 0.8075 | 43 | 47 | 2024-06-01 | 0.5307 |
| `ern6_etype_219` | earnings6 | VECTOR | 1.0 | 29 | 34 | 2024-06-01 | 0.6624 |
| `ern6_goto_broadcast_231` | earnings6 | VECTOR | 1.0 | 79 | 101 | 2024-06-01 | 0.6624 |
| `ern6_isin_212` | earnings6 | VECTOR | 1.0 | 15 | 16 | 2024-06-01 | 0.6624 |
| `ern6_meeting_status_254` | earnings6 | VECTOR | 1.0 | 81 | 102 | 2024-06-01 | 0.6624 |
| `ern6_mtg_type_248` | earnings6 | VECTOR | 1.0 | 51 | 56 | 2024-07-01 | 0.6624 |
| `ern6_next_ed` | earnings6 | VECTOR | 0.6372 | 62 | 90 | 2025-11-01 | 0.6624 |
| `ern6_next_ed_216` | earnings6 | VECTOR | 1.0 | 16 | 17 | 2024-06-01 | 0.6624 |
| `ern6_next_ed_fiscal_year` | earnings6 | VECTOR | 0.6372 | 111 | 124 | 2025-11-01 | 0.6624 |
| `ern6_next_ed_fiscal_year_218` | earnings6 | VECTOR | 1.0 | 21 | 24 | 2024-06-01 | 0.6624 |
| `ern6_next_ed_quarter_217` | earnings6 | VECTOR | 1.0 | 110 | 145 | 2024-06-01 | 0.6624 |
| `ern6_prelim_earnings_link_279` | earnings6 | VECTOR | 0.8075 | 54 | 63 | 2024-06-01 | 0.5307 |
| `ern6_quarter_215` | earnings6 | VECTOR | 1.0 | 169 | 216 | 2024-07-01 | 0.6624 |
| `ern6_split_status_255` | earnings6 | VECTOR | 1.0 | 138 | 181 | 2024-06-01 | 0.6624 |
| `ern6_stock_exchange_214` | earnings6 | VECTOR | 1.0 | 34 | 35 | 2024-06-01 | 0.6624 |
| `ern6_stock_split_ratio_243` | earnings6 | VECTOR | 1.0 | 26 | 30 | 2024-06-01 | 0.6624 |
| `ern6_stock_symbol` | earnings6 | VECTOR | 1.0 | 44 | 50 | 2024-07-01 | 0.6624 |
| `ern6_time_of_day_220` | earnings6 | VECTOR | 1.0 | 115 | 151 | 2024-06-01 | 0.6624 |
| `ern6_time_zone_228` | earnings6 | VECTOR | 1.0 | 7 | 7 | 2024-07-01 | 0.6624 |
| `ern6_transcript_fiscal_year` | earnings6 | VECTOR | 0.6372 | 8 | 9 | 2025-11-01 | 0.6624 |
| `ern6_transcript_quarter_250` | earnings6 | VECTOR | 1.0 | 37 | 48 | 2024-07-01 | 0.6624 |
| `ern6_wqreceivetimestamp` | earnings6 | VECTOR | 0.6372 | 30 | 32 | 2025-11-01 | 0.6624 |
| `ern6_wqreceivetimestamp_252` | earnings6 | VECTOR | 1.0 | 4 | 4 | 2024-06-01 | 0.6624 |
| `ern6_ww_status` | earnings6 | VECTOR | 1.0 | 31 | 36 | 2024-06-01 | 0.6624 |
| `ern6_x_dividend` | earnings6 | VECTOR | 0.6372 | 77 | 96 | 2025-11-01 | 0.6624 |
| `ern6_x_dividend_233` | earnings6 | VECTOR | 0.9258 | 8 | 8 | 2024-06-01 | 0.6624 |
| `ern6_x_dividend_oc` | earnings6 | VECTOR | 0.6372 | 60 | 81 | 2025-11-01 | 0.6624 |
| `ern6_x_dividend_oc_235` | earnings6 | VECTOR | 0.9258 | 12 | 13 | 2024-06-01 | 0.6624 |
| `preliminary_eps_range_lower_bound` | earnings6 | VECTOR | 0.5258 | 13 | 13 | 2025-11-01 | 0.5307 |
| `preliminary_eps_range_upper_bound` | earnings6 | VECTOR | 0.5258 | 12 | 12 | 2025-11-01 | 0.5307 |
| `intraday_delay_indicator` | earnings_sent_matrix | MATRIX | 0.0 | 53 | 70 | 2026-07-01 | 1.0000 |
| `likelihood_of_neutral_tone` | earnings_sent_matrix | MATRIX | 0.0 | 59 | 73 | 2026-07-01 | 1.0000 |
| `negative_sentiment_probability_3` | earnings_sent_matrix | MATRIX | 0.0 | 112 | 151 | 2026-07-01 | 1.0000 |
| `overall_sentiment_score` | earnings_sent_matrix | MATRIX | 0.0 | 68 | 84 | 2026-07-01 | 1.0000 |
| `positive_sentiment_probability_3` | earnings_sent_matrix | MATRIX | 0.0 | 114 | 171 | 2026-07-01 | 1.0000 |
| `sentiment_weighting_method1` | earnings_sent_matrix | MATRIX | 0.0 | 144 | 232 | 2026-07-01 | 1.0000 |
| `sentiment_weighting_method2` | earnings_sent_matrix | MATRIX | 0.0 | 77 | 91 | 2026-07-01 | 1.0000 |

## 3. 逐字段画像（语义族 / 更新频率 / 分布形态 / 适用性）

| 字段 | 语义族 | 更新频率 | 分布形态 | 适用性判定 |
|---|---|---|---|---|
| `eps_change_absolute_value` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `eps_change_percentage_value` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `ern6_1q` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_1q_221` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_2q` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_2q_222` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_3q` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_3q_223` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_4q` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_4q_224` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_actual_currenty_256` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_actual_eps` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `ern6_actual_eps_274` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `ern6_actual_fiscal_year` | 财年/期间元数据 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 元数据：对齐/去重键，非信号 |
| `ern6_actual_fiscal_year_258` | 财年/期间元数据 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 元数据：对齐/去重键，非信号 |
| `ern6_actual_period_259` | 财年/期间元数据 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 元数据：对齐/去重键，非信号 |
| `ern6_actual_source_260` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_actual_url_262` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_board_of_directors_meeting` | 状态标签族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_board_of_directors_meeting_247` | 状态标签族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_company_name_264` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_company_names_213` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_conferencecalltime` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_conferencecalltime_227` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_confnumber_229` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_confpasscode_230` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_div_freq_232` | 股息族 | 事件驱动（公告日快照） | 金额量、右偏重尾（需 rank/log 压缩） | 仅分组键/门控（离散标签） |
| `ern6_dividend_status_240` | 股息族 | 事件驱动（公告日快照） | 金额量、右偏重尾（需 rank/log 压缩） | 仅分组键/门控（离散标签） |
| `ern6_eps6stock_symbol_271` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 不可作信号（标识/文本/时间戳） |
| `ern6_eps6ww_status_273` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 不可作信号（标识/文本/时间戳） |
| `ern6_estimated_eps` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `ern6_estimated_etype_266` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_estimated_fiscal_year` | 财年/期间元数据 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 元数据：对齐/去重键，非信号 |
| `ern6_estimated_fiscal_year_267` | 财年/期间元数据 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 元数据：对齐/去重键，非信号 |
| `ern6_estimated_period_268` | 财年/期间元数据 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 元数据：对齐/去重键，非信号 |
| `ern6_estimated_tod_269` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_estimated_url_270` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_etype_219` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_goto_broadcast_231` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 不可作信号（标识/文本/时间戳） |
| `ern6_isin_212` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_meeting_status_254` | 状态标签族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_mtg_type_248` | 状态标签族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_next_ed` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_next_ed_216` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_next_ed_fiscal_year` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_next_ed_fiscal_year_218` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_next_ed_quarter_217` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_prelim_earnings_link_279` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_quarter_215` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 元数据：对齐/去重键，非信号 |
| `ern6_split_status_255` | 状态标签族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_stock_exchange_214` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_stock_split_ratio_243` | 状态标签族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_stock_symbol` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_time_of_day_220` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `ern6_time_zone_228` | 盈告时点/日期状态族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 不可作信号（标识/文本/时间戳） |
| `ern6_transcript_fiscal_year` | 财年/期间元数据 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_transcript_quarter_250` | 盈告日期族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 事件型：ts_arg_max / ts_delta(days) / trade_when |
| `ern6_wqreceivetimestamp` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_wqreceivetimestamp_252` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_ww_status` | 标识/文本族 | 事件驱动（公告日快照） | 标识/文本（无横截面序） | 不可作信号（标识/文本/时间戳） |
| `ern6_x_dividend` | 股息族 | 事件驱动（公告日快照） | 金额量、右偏重尾（需 rank/log 压缩） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `ern6_x_dividend_233` | 股息族 | 事件驱动（公告日快照） | 金额量、右偏重尾（需 rank/log 压缩） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `ern6_x_dividend_oc` | 股息族 | 事件驱动（公告日快照） | 金额量、右偏重尾（需 rank/log 压缩） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `ern6_x_dividend_oc_235` | 股息族 | 事件驱动（公告日快照） | 金额量、右偏重尾（需 rank/log 压缩） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `preliminary_eps_range_lower_bound` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `preliminary_eps_range_upper_bound` | EPS 数值族 | 事件驱动（公告日快照） | 连续量、右偏、零膨胀（非公告日为空） | 量纲族：ts_delta / ts_zscore / group_rank（先 rank 压缩） |
| `intraday_delay_indicator` | 状态标签族 | 事件驱动（公告日快照） | 离散/零膨胀（事件型） | 仅分组键/门控（离散标签） |
| `likelihood_of_neutral_tone` | 情绪概率/打分族 | 事件驱动（公告日快照） | 概率 [0,1] / 打分（有界） | 待实证裁决 |
| `negative_sentiment_probability_3` | 情绪概率/打分族 | 事件驱动（公告日快照） | 概率 [0,1] / 打分（有界） | 待实证裁决 |
| `overall_sentiment_score` | 情绪概率/打分族 | 事件驱动（公告日快照） | 概率 [0,1] / 打分（有界） | 待实证裁决 |
| `positive_sentiment_probability_3` | 情绪概率/打分族 | 事件驱动（公告日快照） | 概率 [0,1] / 打分（有界） | 待实证裁决 |
| `sentiment_weighting_method1` | 情绪概率/打分族 | 事件驱动（公告日快照） | 概率 [0,1] / 打分（有界） | 待实证裁决 |
| `sentiment_weighting_method2` | 情绪概率/打分族 | 事件驱动（公告日快照） | 概率 [0,1] / 打分（有界） | 待实证裁决 |

## 4. 字段族聚类

| 语义族 | 字段计数 | 代表字段 |
|---|---:|---|
| 标识/文本族 | 14 | `ern6_actual_currenty_256`、`ern6_actual_url_262`、`ern6_company_name_264` |
| 盈告日期族 | 13 | `ern6_1q`、`ern6_1q_221`、`ern6_2q` |
| 盈告时点/日期状态族 | 11 | `ern6_actual_source_260`、`ern6_conferencecalltime`、`ern6_conferencecalltime_227` |
| EPS 数值族 | 9 | `eps_change_absolute_value`、`eps_change_percentage_value`、`ern6_actual_eps` |
| 财年/期间元数据 | 7 | `ern6_actual_fiscal_year`、`ern6_actual_fiscal_year_258`、`ern6_actual_period_259` |
| 状态标签族 | 7 | `ern6_board_of_directors_meeting`、`ern6_board_of_directors_meeting_247`、`ern6_meeting_status_254` |
| 股息族 | 6 | `ern6_div_freq_232`、`ern6_dividend_status_240`、`ern6_x_dividend` |
| 情绪概率/打分族 | 6 | `likelihood_of_neutral_tone`、`negative_sentiment_probability_3`、`overall_sentiment_score` |

## 5. VECTOR 处理契约（earnings6 全部适用）

```
vec_avg(<field>)      # 均值：最常用，等价于「该事件所有条目的平均」
vec_sum(<field>)      # 求和：金额/股数族的自然口径
vec_max / vec_min     # 极值：最大单笔交易
```
- 未包裹直接写 `ern6_actual_eps` 会整批语法失败（VECTOR 不可直接进算术）。
- 覆盖率 0.5258–0.5367 的 EPS 族与覆盖率 0.6372 的「新版」日期族，非公告日为空值，`ts_backfill` 是必需前置。
- 覆盖率 1.0 的字段（如 `ern6_quarter_215`、`ern6_isin_212`）多为**载体字段**：覆盖全但语义是标签/标识，不代表有信号。

## 6. 可用性分层

| 层级 | 判定 | 字段范围 | 含义 |
|---|---|---|---|
| L1 可作信号 | 量纲/方向有意义 | EPS 数值族、股息族 | 需 `ts_backfill` + 时序族算子 |
| L2 仅门控/分组 | 离散标签 | 状态标签族（会议/拆股/股息状态）、盈告时点族（tod/etype）、`intraday_delay_indicator` | 作 `trade_when` 条件或 `bucket` 分组键 |
| L3 仅事件时点 | 日期 | 各季度盈告日、`ern6_next_ed`、电话会时间 | `ts_arg_max` / `ts_delta(days)` 构造「距公告天数」 |
| L4 排除 | 标识/文本/时间戳 | 公司名、ticker、ISIN、交易所、URL、电话、密码、币种、`*_ww_status`、`*timestamp`、`time_zone` | 无横截面序或含未来信息风险，**不得进信号** |

## 7. 字段 → 候选模板白名单（静态先验，需实证裁决）

> 来源：本档案静态全量筛（类型/覆盖/量纲/语义）+ EUR 已固化定律（时序族 vs 截面族、`!=0` 掩码、winsorize 甜点）。
> ⚠ **这是准入先验，不是实证结论**：按经验库纪律，落回测前须对每字段做六法实证裁决（静态推定当实证是历史事故根因）。

| 语义族 | 白名单模板 | 排除模板 | 依据 |
|---|---|---|---|
| EPS 数值族 | `group_rank(ts_delta(vec_avg(F), 63|252), industry)`；`group_rank(ts_zscore(vec_avg(F), 66|252), subindustry)`；surprise = `(actual-estimated)/|estimated|` 后 `ts_mean` | 裸水平 `group_rank(vec_avg(F))`；`ts_mean` 直读 | EUR 定律：水平量/存量走时序族，截面族易归零 |
| 股息族 | `ts_sum(vec_sum(F), 252)` 再 `rank`/`log` 压缩；`ts_delta` 捕捉增减 | 裸金额 rank（量纲跨股票不可比） | 金额右偏重尾 |
| 盈告日期族 | `trade_when(小于(距公告天数, N), 信号, -1)`；`ts_arg_max(事件标记, 252)` | 直接当数值信号 | 事件型稀疏 |
| 状态标签/盈告时点族 | `bucket(...)` 分组键；`trade_when(状态==X, 信号, -1)` | 算术运算 | 离散标签 |
| 标识/文本族 | **不参与** | 全部 | 无横向可比序 |
| 情绪概率/打分族（sent_matrix） | `group_rank(ts_delta(F, 22|66), industry)`；`subtract(pos_prob, neg_prob)` 合成极性后时序化 | 裸概率水平 | 有界概率、拒绝域窄 |

## 8. 已知实测读数（本地库，2026-11-19 只读查询）

`field_profile_full`（region=EUR）对 earnings6 覆盖 **66/66** 行、earnings_sent_matrix **7/7** 行；但其中**只有 2 个字段有真实回测读数**：

| 字段 | 测试次数 | 最好 S | 对应 2Y | 判定 |
|---|---:|---:|---:|---|
| `preliminary_eps_range_upper_bound` | 2 | 0.18 | 0.06 | DEAD |
| `ern6_actual_eps` | 2 | -0.35 | -0.08 | DEAD |

⇒ **71 个字段在 EUR 从未回测**（`is_untested=1`）。这是「字段画像完备 ≠ 信号已验证」的分界：本档案只解决「知道有哪些字段、各自形状与合法性」，不构成任何可交付性结论。

## 9. 结论与下一步

1. **可挖面（分层为程序计数，非估计）**：73 个字段中 L1 量纲可作信号 **11**、L1′ 待实证裁决（情绪概率/打分） **6**、L2 仅门控/分组 **12**、L3 事件时点 **19**、L4 排除 **25**。真正可能有 alpha 的是 L1/L1′ + L3 组合出的「事件驱动 + 量纲」形态。
2. **ATOM 约束**：earnings6 是单数据集，ATOM 合规；但 VECTOR 必须先 `vec_*` 降维，且与其他集（如 analyst）混用即退化为 regular。
3. **已证伪读数**：本地库对 earnings6 的最好历史读数为 S 0.91（2026-11-01 波次），与 EUR 未点亮塔 ATOM 评估一致——该集 ATOM 天花板远低于 1.58 闸。
4. **下一步（若继续）**：按 §7 白名单对 L1 + L1′ 的 17 个字段各出 1–2 臂做六法实证裁决，重点验 `surprise = (actual−estimated)/|estimated|` 与「距公告天数门控」两条机制；不要再用裸水平或截面族试探。

---

配套闸：`python tools/gates/field_profile_completeness_gate.py --profile tracking/EUR/reference/profiles/eur_earnings_earnings6_earnings_sent_matrix_profile_20261119.md`
