# BE53/BE54 待发网格（已预检通过，槽位一空即派）

> 2026-11-11 预检通过（valid=true, unknown_fields=[]）。

## BE53 · option1（OPTION 塔未点亮）—— 7 臂（Xing-Zhang-Zhao 2010 文献臂）

字段面：opt1_p_deltasurface_d1_vi 是 (moneyness, period) 曲面网格上的隐含波动率值，
故 vec_stddev = 微笑曲率代理、vec_range = 跨面极差、vec_max = 最坏情形 IV。
XZZ(2010)：卖权侧微笑最陡的股票在控规模/价值/动量/流动性后年化跑输 10.9% ⇒ 微笑斜率做空。

```
-group_zscore(group_rank(ts_backfill(vec_avg(opt1_p_deltasurface_d1_vi),66),sector),market)
-group_zscore(group_rank(ts_backfill(vec_stddev(opt1_p_deltasurface_d1_vi),66),sector),market)
-group_zscore(group_rank(ts_delta(ts_backfill(vec_avg(opt1_p_deltasurface_d1_vi),132),66),sector),market)
-group_zscore(group_rank(ts_zscore(ts_backfill(vec_avg(opt1_p_deltasurface_d1_vi),132),252),sector),market)
-group_zscore(group_rank(ts_backfill(vec_range(opt1_p_deltasurface_d1_vi),66),sector),market)
-group_zscore(group_rank(ts_backfill(vec_max(opt1_p_deltasurface_d1_vi),66),sector),market)
-group_zscore(group_rank(ts_delta(ts_backfill(vec_sum(opt1_volume),66),22),sector),market)
```

## BE54 · pattern_scores（PV 塔未点亮）—— 10 臂（Lo-Mamaysky-Wang 文献臂 + 论坛 Peak 做空模板）

```
group_zscore(group_rank(ts_zscore(breakaway_gap_up_dynamic_simscore_lookback60,252),sector),market)
group_zscore(group_rank(ts_delta(breakaway_gap_up_dynamic_simscore_lookback60,66),sector),market)
group_zscore(add(group_rank(ts_zscore(breakaway_gap_up_dynamic_simscore_lookback60,252),sector),-group_rank(ts_zscore(breakaway_gap_down_mean_simscore_lookback60,252),sector)),market)
group_zscore(group_rank(subtract(breakaway_gap_up_q95_simscore_lookback60,breakaway_gap_up_mean_simscore_lookback60),sector),market)
-group_zscore(group_rank(ts_zscore(avg_similarity_downward_symmetrical_triangle,252),sector),market)
group_zscore(group_rank(ts_delta(avg_similarity_v_reversal_bottom,66),sector),market)
group_zscore(subtract(group_rank(avg_similarity_falling_wedge_pattern,sector),group_rank(avg_similarity_rising_wedge_pattern,sector)),market)
group_zscore(group_rank(breakaway_gap_up_max_simscore_lookback120,sector),market)
group_zscore(group_rank(adaptive_similarity_upward_breakaway_gap_120,sector),market)
-group_zscore(group_rank(ts_zscore(avg_similarity_ascending_channel,252),sector),market)
```

## BE55 · risk72（RISK 塔未点亮）—— 2 臂收口

覆盖证书理由：31 字段里 24 个是 residualized_return（日收益序列，实测 TO 0.77-0.85 违反 HIGH_TURNOVER 闸，结构性不可用）；
余下 replicator1/2 是因子复制值，实测 lc 25-26（<100 数据不足）。故只补 replicator 的两个矩，判死留证书。

```
group_zscore(group_rank(ts_rank(ts_backfill(vec_avg(cfg2_top800_replicator1),132),252),sector),market)
group_zscore(group_rank(ts_zscore(ts_backfill(vec_avg(cfg2_top1200_replicator1),132),252),sector),market)
```