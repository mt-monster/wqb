# EUR × news21 字段画像（2026-11-09，S1 后备候选归档）

> 平台目录：47/47 字段全量拉取（complete=true，MCP get_datafields，TOPCS1600/D1，filter_sharpe=false）
> 塔位：NEWS（本季 1/3 未点亮，×1.3）｜数据集名 "Macro Economic Event Data"｜os_is 0.8275（未点亮类最高，recommend_datasets）
> 定位：**第 2 席后备**（首选仍在 institutions 内做尽，见 W8）；本画像为证「已按 goal 扫描并归档」，非立即派发。

## 一、覆盖与类型（关键结构事实）
- 47 字段 = 24 MATRIX + 23 VECTOR；**字段级 cov min 0.1616 / max 0.769 / mean 0.5266，无一 ≥0.85**。
- ⚠ sub 闸结构性风险：信号主体字段 cov 仅 0.5102（transcript 情绪）/0.4146–0.5102（事件频率）；按 EUR cov<0.85 sub 难达标的前科（fundamental28），需实测验证而非先验判死（GBR 教训：数据集级 cov 会误导，FHP _active cov0.843 仍过 sub）。

## 二、字段族分组与适用性
| 族 | 字段（代表） | 类型 | cov | 语义 | alpha 适用性 |
|---|---|---|---|---|---|
| N1 财报事件元数据 | earning_fiscal_year/quarter、earning_calendar_quarter_end、event_*_date_type、earning_time_type | VECTOR | 0.6194 | 日期/标签/财季编码 | 非信号主体，仅事件对齐/门控 |
| N2 电话会文本情绪 | event_transcript_sentiment_score、positive/negative_score、word_count | MATRIX | 0.5102 | 正负词占比/净语气 | 情绪极性信号（news 类历史弱，需夺冠几何复核） |
| N3 归一化语气 | nws21_tone_tone_sc、nws21_pos_sc、nws21_neg_sc、nws21_qerf_gen/sop | MATRIX | 0.5102 | 归一化 tone/词数 | 同 N2，aC 3–11 冷门 |
| N4 事件频率=关注度 | event_frequency_label、nws21_event_freq | MATRIX | 0.4146/0.5102 | StreetEvents 提及次数 | **Da et al. 注意力机制**（news18 席 2 同源），最有希望 |
| N5 财报数值 | earning_number_value、earning_broker_count | VECTOR | 0.6194 | EPS/贡献券商数 | 事件型，需 vec 聚合 |
| N6 公司事件日历 | next_earnings_call_date、next_shareholder_meeting_date、next_ex_dividend_event_date(aC152)、next_corporate_presentation_date | MATRIX | 0.16–0.54 | 未来事件日期 | 日期元数据；ex_dividend aC152 拥挤但属日历非信号 |
| N7 事件情绪 VECTOR | overall_tone_score_1、positive/negative_sentiment_score_1、negative_word_count_1 | VECTOR | 0.4169 | 事件语气 | 需 vec_avg，cov 偏低 |

## 三、结论与下一步
1. news21 信号主体 = N4 事件频率（注意力）+ N2/N3 电话会语气；其余多为财报/事件日历元数据。
2. **覆盖是主疑点**（信号字段 cov 0.51）：若派发，先按夺冠几何（level z + ts_mean 平滑 + country 轴，FHP 实证）控 TO 并实测 sub；sub 结构性不达则 coverage-death 归档。
3. 本画像存档备查；**当前不派发**——先在 institutions 内做尽（W8 夺冠几何横扫其余 FHP 字段），无果再转 news21（避免频繁换数据集）。
