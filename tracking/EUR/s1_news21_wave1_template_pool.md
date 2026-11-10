# EUR × news21 · W1 模板池（2026-11-09，30 式全字段覆盖）

> 设置：EUR/**TOP2500**（news18 事件密度机制前科：TOPCS1600 归零，宽宇宙才活）/D1/SUBINDUSTRY/decay4/trunc0.08/maxTrade OFF/nan ON。
> 字段全集 47/47（24 MATRIX+23 VECTOR）；覆盖自检 47/47、最大算子数 11（≤12）。
> 半衰期纪律（论坛 17 赞帖）：事件驱动字段窗口取短（5/22），**禁 ts_rank(252)**（日频动量窗对事件字段=拟合噪声）。
> 选题纪律（FHP prod 墙教训）：优先冷字段——transcript 语气族 aC 1–11 冷；**date 族 aC 54–763 拥挤，预期 prod 墙，仅覆盖探测**。

## ≥10 结构互异模板（来源标注）
| # | 结构 | 代表式 | 字段 | 来源 |
|---|---|---|---|---|
| T1 | level-z+短平滑 | ts_mean(group_zscore(x,country),5) | transcript_sentiment/neg/pos/nws21_pos/neg/event_freq_label/overall_tone/earning_value/meeting_date_est | FHP 夺冠几何（本役实证） |
| T2 | 意外偏离 | x−ts_mean(x,22) | nws21_tone_tone_sc | forum「Slowly Incorporated News」/ Hong-Stein 渐进信息扩散 |
| T3 | 短窗动量 | ts_delta(x,5) | transcript_positive_score | 半衰期纪律（forum） |
| T4 | 正负不对称比 | (pos−neg)/(total+1) | pos_word/neg_word/total_word | 语气不对称（self+文献） |
| T5 | 注意力密度 | event_freq level-z | nws21_event_freq | Da et al. 2011 注意力 |
| T6 | 语气离散度 | ts_std_dev(x,22) | nws21_tone_tone_sc | 不确定性溢价（self） |
| T7 | 短窗分位 | ts_rank(x,22) | transcript_positive_score | 半衰期纪律 |
| T8 | 正负计数净差 | z(pos_count)−z(neg_count) | nws21_qerf_sop/gen | 净语气（self） |
| T9 | VECTOR 情绪净差 | z(vec_avg(pos)−vec_avg(neg)) | sentiment_score_1/word_count_1 正负 | self |
| T10 | 每券商估计 | value/(broker+1) | earning_number_value/broker_count | 分析师人均估计（self） |
| T11 | 事件间隔 | next_date−prev_date | earnings_call/shareholder_meeting/ex_dividend/presentation 各 next/prev | 事件节奏（self；date 族拥挤仅覆盖） |
| T12 | 日期修正 | ts_delta(date,5) | next_earnings_estimate/previous_sales_statement | 改期=信息（self） |
| T13 | 事件门控 | trade_when(and(元数据条件),CORE,0) | 16 个元数据/标签字段 | 覆盖+事件条件化（self） |

## 字段覆盖映射（47/47）
- 信号主体（13 MATRIX 冷字段）：N1–N12；VECTOR 情绪 5：N13–N15；earnings 2：N16–N17。
- date 族 11：N18–N24（间隔/修正）。元数据 16：N25–N30 门控（每式 2–3 条件，算子≤11）。
- ⚠ 覆盖探测 ≠ 信号预期：date/元数据族多为拥挤或无信号，探明即归档；主攻 = T1–T10 冷语气/注意力族。

## 判读预案
- 冷语气族任一 S≥1.2 近闸 → S4 破闸 + **先族代表 prod 预判**（吸取 FHP 教训，别等全闸才发现墙）。
- date 族若 S 高但 aC 拥挤 → 直接 prod 预判，墙则弃。
- 全族 |S|<0.5 且三闸过 → seal_dead_end（论坛取证前置）。
