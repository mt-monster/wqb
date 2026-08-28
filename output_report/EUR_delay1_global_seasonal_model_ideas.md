# EUR D1 global_seasonal_model ideas (Wave71 — agent S1)

Wave70 AFT `_2` 全弱 max S0.58；离开 AFT。Wave20 GSM 只测了 `trading_days_to_next_event` + analyst_meta（平台 ERROR）+ pv_weekly **收益预测**（S0.98 但属 returns 族）。本波只打 **股票特定公司事件** 字段，不用日历常数（iso_week/month/quarter/weekday/month_end/regime 横截面无差异，rank 失效）。

禁止：pv_/prob_bucket/predicted_return 前向收益；type_code 类别码；v_rev/wedge mix；resid×PV。
OS ACTIVE=3。慢腿未证明 |S|≥1 前不混快 PV。

## Concepts
1. Last-event confirmation — `last_event_confirmation_level`（0-alpha）
2. Next-event reschedule/cancel — `future_event_update_flag`（0-alpha）
3. Last-event update flag — `last_event_update_flag`
4. Next-event confirmation — `next_event_confirmation_level`
5. Last-event transcript available — `last_event_transcript_flag`
6. Days since last event — `trading_days_since_last_event`（非 Wave20 的 to-next）
7. Next-event transcript expected — `next_event_transcript_flag`

Skip: `trading_days_to_next_event`（Wave20）、日历常数、全部 return-quantile 模型。
