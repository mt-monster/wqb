# Wave5b news18 Mode A：nip x FAST（READY）

> 论坛 40847481080087：相关性算子+FAST+nip 点亮 news（EUR）。KOR 假说。
> 启用：Wave5 STATISTICAL 弱灭后。避开 PV returns 腿（禁混）。

F01 subtract(0.5, group_rank(ts_mean(rp_nip_earnings, 22), sector))
F02 subtract(0.5, group_rank(ts_mean(rp_nip_business, 22), sector))
F03 subtract(0.5, group_rank(ts_corr(rp_nip_earnings, rp_ess_earnings, 22), sector))
F04 subtract(0.5, group_rank(ts_mean(ts_delta(rp_nip_earnings, 22), 5), sector))
F05 subtract(0.5, group_rank(ts_mean(vec_avg(nws18_nip), 22), sector))
F06 subtract(0.5, group_rank(ts_zscore(rp_nip_business, 66), sector))
F07 subtract(group_rank(ts_mean(rp_nip_earnings, 22), sector), 0.5)
F08 subtract(0.5, group_rank(ts_mean(multiply(rp_nip_earnings, divide(vec_avg(nws18_relevance), 100)), 22), sector))

设置：KOR/TOP600/D1 decay4 neutralization=FAST trunc0.08
