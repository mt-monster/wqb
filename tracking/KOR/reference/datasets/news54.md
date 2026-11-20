# news54 数据集画像（KOR / TOP600 / Delay=1）— Key Developments Data

> 2026-11-20 建。平台 `get_datafields(news54, filter_sharpe=false)` 实读 complete=true / 40/40。
> 塔：**NEWS（0/3 未点亮）**，倍率 1.6。**结论：不可作数值信号集（元数据/文本表）。**

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | `news54` |
| 名称 | Key Developments Data |
| category | **NEWS**（0/3，乘数 1.6） |
| 结构 | **40 字段全 VECTOR** |
| 覆盖 | 0.1365–0.8762（分字段差异大） |
| 拥挤度 | alphaCount 0–7（极低） |

## 1. 字段全表（40/40）与角色裁决

| 类别 | 字段（cov / aC） | 裁决 |
|---|---|---|
| **时间戳/时刻（20）** | `daily_event_announcement_time`(.612/3)、`daily_event_announcement_time_utc`(.761/0)、`daily_event_earnings_release_time`(.748/0)、`daily_event_entry_time`(.761/0)、`daily_event_entry_time_utc`(.761/1)、`daily_event_last_update_time`(.761/0)、`daily_event_last_update_time_utc`(.761/1)、`daily_event_record_end_time`(.565/0)、`daily_event_record_start_time`(.761/0)、`daily_event_relevant_time_utc`(.761/0)、`event_announcement_time`(.876/1)、`event_entry_time`(.876/0)、`event_last_update_time`(.876/0)、`event_relevant_time_utc`(.876/2)、`future_event_announcement_time`(.645/0)、`future_event_announcement_time_utc`(.796/0)、`future_event_entry_time`(.796/0)、`future_event_entry_time_utc`(.796/0)、`future_event_last_update_time`(.796/0)、`future_event_last_update_time_utc`(.796/0)、`future_event_record_end_time`(.587/0)、`future_event_record_start_time`(.796/0)、`future_event_relevant_time_utc`(.796/0) | ✗ 时刻码，跨日不可序（同 reptime 陷阱） |
| **自由文本（5）** | `mws54_eventsdaily_headline`(.761/2)、`mws54_eventsdaily_situation`(.761/2)、`mws54_futureeventmkt_headline`(.796/2)、`mws54_futureeventmkt_situation`(.796/0)、`mws54_keydevelopments_headline`(.876/2)、`mws54_keydevelopments_situation`(.876/0) | ✗ 非数值 |
| **标志位（3）** | `mws54_eventcallbasicinfo_cancelledflag`(.183/0)、`mws54_eventcallbasicinfo_postponedflag`(.183/1)、`mws54_eventerinfo_cancelledflag`(.720/2)、`mws54_eventerinfo_fullyearflag`(.721/3) | ⚠ 仅可作 presence 门控 |
| **日历标识（6）** | `mws54_eventcallbasicinfo_fiscalquarter`(.137/7)、`mws54_eventcallbasicinfo_fiscalyear`(.137/4)、`mws54_eventerinfo_calendarmonth`(.748/1)、`mws54_eventerinfo_calendaryear`(.720/5)、`mws54_eventerinfo_fiscalquarter`(.720/0)、`mws54_eventerinfo_fiscalyear`(.721/1) | ✗ 周期标识非信号 |
| **唯一真数值（1）** | **`mws54_factor`**（.2449 / **1**）——股息额/拆股比 | ⚠ **cov .245 < 0.5 硬地板**，零配额封存 |

## 2. 裁决

**不可作信号数据集**：40 字段中 20 个是时间戳、6 个自由文本、6 个日历标识、4 个标志位，**唯一数值字段 `mws54_factor` 覆盖率 .2449 低于 0.5 硬地板**。
可用的唯一形态是 `vec_count(任意事件字段)` = 当日关键事件条数（事件强度），但该轴在 KOR 的 news29 已实测无信号（S −0.39 量级），且本集与 news29 同属「事件条数」语义 ⇒ **不重复投入**。

判死口径：数据层排除（覆盖率地板 + 字段语义），**不是**信号层判死；记 PROVISIONAL，若未来 `mws54_factor` 覆盖率上升可重开。
