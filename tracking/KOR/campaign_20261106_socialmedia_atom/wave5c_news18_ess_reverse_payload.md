# Wave5c news18 ESS 反臂（READY · 与 5b 并列备选）

> 依据：Wave5 RREl8d3g ess_earnings S-0.72；铁律 B 正反各测（取负不精确翻转）。
> preflight valid=true unknown=[]
> 优先于换集 news50：同集尚未试反臂。

E01 subtract(group_rank(ts_mean(rp_ess_earnings, 22), sector), 0.5)
E02 subtract(group_rank(ts_mean(rp_ess_business, 22), sector), 0.5)
E03 subtract(group_rank(ts_mean(vec_avg(nws18_qep), 22), sector), 0.5)
E04 subtract(group_rank(ts_mean(rp_css_business, 22), sector), 0.5)
E05 subtract(0.5, group_rank(ts_mean(multiply(-1, rp_ess_earnings), 22), sector))
E06 subtract(group_rank(ts_mean(ts_delta(rp_ess_earnings, 22), 5), sector), 0.5)
E07 subtract(group_rank(ts_zscore(rp_ess_earnings, 66), sector), 0.5)
E08 subtract(group_rank(ts_mean(rp_ess_earnings, 22), industry), 0.5)

设置：KOR/TOP600/D1 decay4 STATISTICAL（可再试 FAST）
