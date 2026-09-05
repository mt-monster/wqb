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

## 特征概念（8 问框架，模板化）

### Q1 稳定性/不变量
- **使用字段**：`event_announcement_time`, `event_entry_time`
- **建议**：ts_mean / ts_std_dev 度量字段的长期水平与稳定性

### Q2 变化
- **使用字段**：`event_announcement_time`, `event_entry_time`
- **建议**：ts_delta / ts_scale 捕捉变化率与动量

### Q3 异常
- **使用字段**：`event_announcement_time`, `event_entry_time`
- **建议**：zscore / ts_rank 识别截面与时间序列上的离群

### Q4 交互
- **使用字段**：`event_announcement_time`, `event_entry_time`
- **建议**：两字段 add/multiply 合成新含义，注意先各自中性化

### Q5 结构
- **使用字段**：`event_announcement_time`, `event_entry_time`
- **建议**：字段占比 / 比例关系（如 components 型字段）

### Q6 累积
- **使用字段**：`event_announcement_time`, `event_entry_time`
- **建议**：ts_sum / ts_decay_linear 累积与衰减记忆

### Q7 相对
- **使用字段**：`event_announcement_time`, `event_entry_time`
- **建议**：rank / group_rank 相对定位与归一化

### Q8 本质
- **使用字段**：`event_announcement_time`, `event_entry_time`
- **建议**：第一性原理直取原始字段，剥离过拟合包装

## GEM 兼容模板（Concept Blocks）

> 以下 Concept 块供 S2 `brain-makeSomeGem` 直接消费（`--ideas-file` 注入）。
> 占位符 `{field_id}` 为字段白名单中的真实字段 id，run_pipeline 可解析绑定。

**Concept**: event_announcement_time 长期水平稳定（Q1）
- **Mechanism**: ts_mean 度量字段长期水平，rank 截面归一化
- **Fields Used**: `event_announcement_time`, `event_entry_time`
- **Implementation Example**: `rank(ts_mean({event_announcement_time}, 66))`
- **Direction**: High → long

**Concept**: event_announcement_time 变化动量（Q2）
- **Mechanism**: ts_delta 捕捉 21 日变化率，rank 截面归一化
- **Fields Used**: `event_announcement_time`, `event_entry_time`
- **Implementation Example**: `rank(ts_delta({event_announcement_time}, 21))`
- **Direction**: High → long

**Concept**: event_announcement_time 截面离群（Q3）
- **Mechanism**: zscore 识别截面离群，rank 归一化
- **Fields Used**: `event_announcement_time`, `event_entry_time`
- **Implementation Example**: `rank(zscore({event_announcement_time}))`
- **Direction**: High → long

**Concept**: event_announcement_time × event_entry_time 交互（Q4）
- **Mechanism**: 两字段各自 ts_zscore 中性化后 multiply 合成
- **Fields Used**: `event_announcement_time`, `event_entry_time`
- **Implementation Example**: `rank(multiply(ts_zscore({event_announcement_time}, 66), ts_zscore({event_entry_time}, 66)))`
- **Direction**: High → long

**Concept**: event_announcement_time 结构占比（Q5）
- **Mechanism**: divide 构造比例关系，rank 截面归一化
- **Fields Used**: `event_announcement_time`, `event_entry_time`
- **Implementation Example**: `rank(divide({event_announcement_time}, {event_entry_time}))`
- **Direction**: High → long

**Concept**: event_announcement_time 累积衰减（Q6）
- **Mechanism**: ts_decay_linear 累积记忆衰减，rank 归一化
- **Fields Used**: `event_announcement_time`, `event_entry_time`
- **Implementation Example**: `rank(ts_decay_linear({event_announcement_time}, 21))`
- **Direction**: High → long

**Concept**: event_announcement_time 截面相对定位（Q7）
- **Mechanism**: ts_backfill 稀疏回填 + group_rank 行业内相对定位
- **Fields Used**: `event_announcement_time`, `event_entry_time`
- **Implementation Example**: `group_rank(ts_backfill({event_announcement_time}, 66), industry)`
- **Direction**: High → long

**Concept**: event_announcement_time 本质直取（Q8）
- **Mechanism**: 第一性原理直取原始字段，rank 截面归一化
- **Fields Used**: `event_announcement_time`, `event_entry_time`
- **Implementation Example**: `rank({event_announcement_time})`
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