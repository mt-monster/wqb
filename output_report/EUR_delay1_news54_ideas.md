# news54 Feature Engineering Analysis Report

**Dataset**: news54
**Region**: EUR
**Delay**: 1


- **Dataset**: `news54`
- **Category**: `news`
- **Region**: `EUR`
- **Delay**: `1`
- **Universe**: `TOP2500`
- **Fields Analyzed**: 40
- **Generated**: 2026-09-04T02:24:56.362695

---

## Executive Summary

本数据集提供 40 个字段（MATRIX 0 / VECTOR 40 / GROUP 0），覆盖 `news` 类信号。以下为自动生成的特征工程思路，供 S2 GEM 阶段绑定字段池。

## 字段画像（Field Inventory）

| Field ID | Type | Coverage | Field Type | Operator Adaptation | Description |
|---|---|---|---|---|---|
| `daily_event_announcement_time` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time of the announcement in the announcedDateTimeZoneId time zone |
| `daily_event_announcement_time_utc` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time the event was announced (UTC) |
| `daily_event_earnings_release_time` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time of the earnings release |
| `daily_event_entry_time` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The time when the event was entered in the dataset. |
| `daily_event_entry_time_utc` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time the record was first entered into the system (UTC) |
| `daily_event_last_update_time` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time the event record was last modified |
| `daily_event_last_update_time_utc` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time the record was last modified (UTC) |
| `daily_event_record_end_time` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The time when the current record for the daily event ceased to be active. |
| `daily_event_record_start_time` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The time when the current record for the daily event became active. |
| `daily_event_relevant_time_utc` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time in UTC of the event’s key moment (often the event time; otherwise announcement time) |
| `event_announcement_time` | VECTOR | 98% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The UTC time at which the event was announced |
| `event_entry_time` | VECTOR | 98% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The time when the event record was entered into the system |
| `event_last_update_time` | VECTOR | 98% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | The time when the event record was last modified |
| `event_relevant_time_utc` | VECTOR | 98% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | UTC time of the key moment for the event (usually the announced time; for scheduled events, the event time) |
| `future_event_announcement_time` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time the announcement is scheduled to be made, in UTC |
| `future_event_announcement_time_utc` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time the announcement is scheduled/made in UTC |
| `future_event_entry_time` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time when this Future Event was entered |
| `future_event_entry_time_utc` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time the Future Event was entered, in UTC |
| `future_event_last_update_time` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time of the last modification to the Future Event |
| `future_event_last_update_time_utc` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time of the last modification in UTC |
| `future_event_record_end_time` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | End time of the S&P effective window during which this record is valid |
| `future_event_record_start_time` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Start time of the S&P effective window for this record |
| `future_event_relevant_time_utc` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Time the event occurs in UTC time zone |
| `mws54_eventcallbasicinfo_cancelledflag` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Flag indicating whether the event call was cancelled, 0=no, 1=yes |
| `mws54_eventcallbasicinfo_fiscalquarter` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Fiscal quarter associated with the event |
| `mws54_eventcallbasicinfo_fiscalyear` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Fiscal year pertaining to the event call |
| `mws54_eventcallbasicinfo_postponedflag` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Indicator whether the event call was postponed; 0=no, 1=yes |
| `mws54_eventerinfo_calendarmonth` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Calendar month of the earnings release |
| `mws54_eventerinfo_calendaryear` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Calendar year of the earnings release |
| `mws54_eventerinfo_cancelledflag` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Indicator that the earnings event was canceled |
| `mws54_eventerinfo_fiscalquarter` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Fiscal quarter associated with the earnings release |
| `mws54_eventerinfo_fiscalyear` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Fiscal year of the earnings release |
| `mws54_eventerinfo_fullyearflag` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Flag indicating the earnings release covers a full fiscal year, 0=no, 1=yes |
| `mws54_eventsdaily_headline` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Headline text for the event |
| `mws54_eventsdaily_situation` | VECTOR | 87% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Additional descriptive text for the event |
| `mws54_factor` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Numeric amount/factor associated with the event, e.g., dividend amount or stock split ratio |
| `mws54_futureeventmkt_headline` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Headline for the event |
| `mws54_futureeventmkt_situation` | VECTOR | 91% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Additional descriptive text/details for the event |
| `mws54_keydevelopments_headline` | VECTOR | 98% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Headline text describing the event |
| `mws54_keydevelopments_situation` | VECTOR | 98% | VECTOR | vec_avg/vec_sum/vec_stddev + ts_mean/ts_delta/rank | Additional descriptive narrative text about the event |

## 字段-算子适配表（Field-Operator Adaptation）

| Field Type | Valid Operators | Forbidden Operators | Example |
|---|---|---|---|
| 连续数值型 | `ts_mean/ts_delta/rank/ts_zscore/ts_corr/ts_regression` | `ts_std_dev`（波动率无预测力）、`ts_max_diff`（加速脉冲失效） | `rank(ts_mean(surprise, 22))` |
| 分类型（quantile_label/rank） | `rank/group_rank/ts_backfill` | `ts_mean`（分类平均无意义）、`ts_zscore`（非连续分布） | `rank(ts_backfill(quantile_label, 66))` |
| 概率型（prob_class） | `rank/subtract/if_else` | `ts_mean`（概率平均稀释信号）、`ts_delta`（概率变化噪声大） | `rank(prob_class1) - rank(prob_class0)` |
| 计数型（count/usd） | `ts_sum/trade_when/ts_backfill` | `ts_delta`（计数变化=已反应）、`ts_max_diff`（加速脉冲失效） | `trade_when(count > 0, rank(x), NaN)` |
| 比率型（to_price/ratio） | `rank/group_zscore/group_neutralize` | `ts_mean`（比率平均无意义）、`ts_delta`（比率变化噪声） | `group_zscore(ratio, industry)` |
| VECTOR 型 | `vec_avg/vec_sum/vec_stddev/vec_range` + `ts_mean/ts_delta/rank` | 直接用 `ts_mean`（必须先聚合） | `rank(ts_mean(vec_avg(sentiment), 22))` |

## 字段解构（Field Deconstruction）

### `event_announcement_time`（VECTOR）
- **测什么**：The UTC time at which the event was announced
- **覆盖率**：0.9827
- **字段名语义**：`event_announcement_time` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `event_entry_time`（VECTOR）
- **测什么**：The time when the event record was entered into the system
- **覆盖率**：0.9827
- **字段名语义**：`event_entry_time` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `event_last_update_time`（VECTOR）
- **测什么**：The time when the event record was last modified
- **覆盖率**：0.9827
- **字段名语义**：`event_last_update_time` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `event_relevant_time_utc`（VECTOR）
- **测什么**：UTC time of the key moment for the event (usually the announced time; for scheduled events, the event time)
- **覆盖率**：0.9827
- **字段名语义**：`event_relevant_time_utc` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `mws54_keydevelopments_headline`（VECTOR）
- **测什么**：Headline text describing the event
- **覆盖率**：0.9827
- **字段名语义**：`mws54_keydevelopments_headline` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `mws54_keydevelopments_situation`（VECTOR）
- **测什么**：Additional descriptive narrative text about the event
- **覆盖率**：0.9827
- **字段名语义**：`mws54_keydevelopments_situation` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `future_event_announcement_time`（VECTOR）
- **测什么**：Time the announcement is scheduled to be made, in UTC
- **覆盖率**：0.9131
- **字段名语义**：`future_event_announcement_time` 的命名前缀用于字段族聚类（S1 前缀扫描）

### `future_event_announcement_time_utc`（VECTOR）
- **测什么**：Time the announcement is scheduled/made in UTC
- **覆盖率**：0.9131
- **字段名语义**：`future_event_announcement_time_utc` 的命名前缀用于字段族聚类（S1 前缀扫描）

## 预处理决策（Preprocessing）

- group_zscore / group_rank：对 VECTOR/GROUP 字段先截面聚合再中性化
- vec_ 向量包装：40 个 VECTOR 字段需用 vec_* 算子读取

## 特征概念（信号优先重写版 2026-09-11）

> 本数据集为 S&P Capital IQ 公司事件流。真正有信号价值的字段仅三类：
> ① `mws54_factor`（事件数值：股息金额/拆股比例，coverage 0.91，唯一数值信号）
> ② 事件标志 `mws54_eventerinfo_cancelledflag` / `mws54_eventcallbasicinfo_postponedflag`（取消/推迟=利空冲击）
> ③ 事件密度（vec_count 事件计数，公司事件活跃度）
> 时间戳字段（announcement/entry/relevant time）本身不是信号，禁止直接包装。
> 全部 VECTOR 字段必须先 vec_* 聚合；稀疏事件流必须 trade_when/ts_backfill 门控防空窗抖动。

### 核心信号概念（聚焦 mws54_factor + event_flag + 事件密度）

**Concept**: 事件数值因子强度（mws54_factor 水平）
- **Mechanism**: 事件数值（股息/拆股比例）截面相对定位，高事件数值=强公司行动信号
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `trade_when(vec_count({mws54_factor}) > 0, rank(ts_backfill(vec_avg({mws54_factor}), 66)), NaN)`
- **Direction**: High → long

**Concept**: 事件数值因子变化（mws54_factor 动量）
- **Mechanism**: 事件数值的时间序列变化，捕捉公司行动升级/降级
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `trade_when(vec_count({mws54_factor}) > 0, rank(ts_delta(ts_backfill(vec_avg({mws54_factor}), 66), 21)), NaN)`
- **Direction**: High → long

**Concept**: 事件取消冲击（cancelledflag 利空）
- **Mechanism**: 事件取消=利空，取消比例高=负面信号，反向取号
- **Fields Used**: `mws54_eventerinfo_cancelledflag`
- **Implementation Example**: `trade_when(vec_count({mws54_eventerinfo_cancelledflag}) > 0, subtract(0, rank(ts_mean(vec_avg({mws54_eventerinfo_cancelledflag}), 22))), NaN)`
- **Direction**: Low（高取消） → short

**Concept**: 事件推迟冲击（postponedflag 利空）
- **Mechanism**: 事件推迟=不确定性利空，推迟标志反向
- **Fields Used**: `mws54_eventcallbasicinfo_postponedflag`
- **Implementation Example**: `trade_when(vec_count({mws54_eventcallbasicinfo_postponedflag}) > 0, subtract(0, rank(ts_mean(vec_avg({mws54_eventcallbasicinfo_postponedflag}), 22))), NaN)`
- **Direction**: Low（高推迟） → short

**Concept**: 事件密度活跃度（vec_count 计数）
- **Mechanism**: 单位时间事件数量=公司事件活跃度，高密度=高关注
- **Fields Used**: `mws54_keydevelopments_headline`
- **Implementation Example**: `rank(ts_sum(vec_count({mws54_keydevelopments_headline}), 22))`
- **Direction**: High → long

**Concept**: 未来事件预期强度（future_event 前瞻）
- **Mechanism**: 未来事件数值因子=前瞻公司行动预期
- **Fields Used**: `mws54_factor`, `future_event_relevant_time_utc`
- **Implementation Example**: `trade_when(vec_count({mws54_factor}) > 0, group_rank(ts_backfill(vec_avg({mws54_factor}), 66), industry), NaN)`
- **Direction**: High → long

**Concept**: 事件数值因子行业相对（group_rank 中性化）
- **Mechanism**: 事件数值在行业内相对定位，剥离行业事件密度差异
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `trade_when(vec_count({mws54_factor}) > 0, group_rank(ts_backfill(vec_avg({mws54_factor}), 66), subindustry), NaN)`
- **Direction**: High → long

**Concept**: 事件数值因子 zscore 离群（截面异常）
- **Mechanism**: 事件数值截面 zscore 识别异常大的公司行动
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `trade_when(vec_count({mws54_factor}) > 0, rank(zscore(ts_backfill(vec_avg({mws54_factor}), 66))), NaN)`
- **Direction**: High → long

## GEM 兼容模板（Concept Blocks）

> 以下 Concept 块供 S2 `brain-makeSomeGem` 直接消费（`--ideas-file` 注入）。
> 占位符 `{field_id}` 为字段白名单中的真实字段 id，run_pipeline 可解析绑定。
> 2026-09-11：模板统一为单占位符形式（每模板 1 个 `{field}`），配合 GEM 孤字段
> 多样性展开（wrapper×窗口几何变体），避免同字段多占位符被 same_field_combo 拦截。

**Concept**: 事件数值因子强度（mws54_factor 水平）
- **Mechanism**: 事件数值（股息/拆股比例）截面相对定位，高事件数值=强公司行动信号
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `rank(ts_backfill(vec_avg({mws54_factor}), 66))`
- **Direction**: High → long

**Concept**: 事件数值因子变化（mws54_factor 动量）
- **Mechanism**: 事件数值的时间序列变化，捕捉公司行动升级/降级
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `rank(ts_delta(vec_avg({mws54_factor}), 21))`
- **Direction**: High → long

**Concept**: 事件取消冲击（cancelledflag 利空）
- **Mechanism**: 事件取消=利空，取消比例高=负面信号，反向取号
- **Fields Used**: `mws54_eventerinfo_cancelledflag`
- **Implementation Example**: `subtract(0, rank(ts_mean(vec_avg({mws54_eventerinfo_cancelledflag}), 22)))`
- **Direction**: Low（高取消） → short

**Concept**: 事件推迟冲击（postponedflag 利空）
- **Mechanism**: 事件推迟=不确定性利空，推迟标志反向
- **Fields Used**: `mws54_eventcallbasicinfo_postponedflag`
- **Implementation Example**: `subtract(0, rank(ts_mean(vec_avg({mws54_eventcallbasicinfo_postponedflag}), 22)))`
- **Direction**: Low（高推迟） → short

**Concept**: 事件密度活跃度（vec_count 计数）
- **Mechanism**: 单位时间事件数量=公司事件活跃度，高密度=高关注
- **Fields Used**: `mws54_keydevelopments_headline`
- **Implementation Example**: `rank(ts_sum(vec_count({mws54_keydevelopments_headline}), 22))`
- **Direction**: High → long

**Concept**: 未来事件预期强度（future_event 前瞻）
- **Mechanism**: 未来事件数值因子=前瞻公司行动预期
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `group_rank(ts_backfill(vec_avg({mws54_factor}), 66), industry)`
- **Direction**: High → long

**Concept**: 事件数值因子行业相对（group_rank 中性化）
- **Mechanism**: 事件数值在行业内相对定位，剥离行业事件密度差异
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `group_rank(ts_backfill(vec_avg({mws54_factor}), 66), subindustry)`
- **Direction**: High → long

**Concept**: 事件数值因子 zscore 离群（截面异常）
- **Mechanism**: 事件数值截面 zscore 识别异常大的公司行动
- **Fields Used**: `mws54_factor`
- **Implementation Example**: `rank(zscore(vec_avg({mws54_factor})))`
- **Direction**: High → long

## 字段白名单（Field Whitelist）

```
daily_event_announcement_time
daily_event_announcement_time_utc
daily_event_earnings_release_time
daily_event_entry_time
daily_event_entry_time_utc
daily_event_last_update_time
daily_event_last_update_time_utc
daily_event_record_end_time
daily_event_record_start_time
daily_event_relevant_time_utc
event_announcement_time
event_entry_time
event_last_update_time
event_relevant_time_utc
future_event_announcement_time
future_event_announcement_time_utc
future_event_entry_time
future_event_entry_time_utc
future_event_last_update_time
future_event_last_update_time_utc
future_event_record_end_time
future_event_record_start_time
future_event_relevant_time_utc
mws54_eventcallbasicinfo_cancelledflag
mws54_eventcallbasicinfo_fiscalquarter
mws54_eventcallbasicinfo_fiscalyear
mws54_eventcallbasicinfo_postponedflag
mws54_eventerinfo_calendarmonth
mws54_eventerinfo_calendaryear
mws54_eventerinfo_cancelledflag
mws54_eventerinfo_fiscalquarter
mws54_eventerinfo_fiscalyear
mws54_eventerinfo_fullyearflag
mws54_eventsdaily_headline
mws54_eventsdaily_situation
mws54_factor
mws54_futureeventmkt_headline
mws54_futureeventmkt_situation
mws54_keydevelopments_headline
mws54_keydevelopments_situation
```

*Report generated: 2026-09-04T02:24:56.362695*