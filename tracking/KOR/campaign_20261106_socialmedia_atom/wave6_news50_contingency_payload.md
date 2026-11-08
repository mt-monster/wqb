# Wave6 news50 应急载荷（READY · 5b 再灭后）

> preflight valid=true unknown=[]
> 模板 12；首派前 8。算子数 4/4/4/4/5/7/4/4/4/4/4/5

N01 subtract(0.5, group_rank(ts_mean(vec_avg(mws50_ber), 22), sector))
N02 subtract(0.5, group_rank(ts_mean(vec_avg(mws50_aes), 22), sector))
N03 subtract(0.5, group_rank(ts_mean(vec_avg(mws50_ens), 66), sector))
N04 subtract(0.5, group_rank(ts_mean(vec_avg(mws50_acb), 22), sector))
N05 subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(mws50_ber), 22), 5), sector))
N06 subtract(0.5, group_rank(ts_mean(multiply(vec_avg(mws50_ber), divide(vec_avg(mws50_aes), 100)), 22), sector))
N07 subtract(group_rank(ts_mean(vec_avg(mws50_ber), 22), sector), 0.5)
N08 subtract(0.5, group_rank(ts_zscore(vec_avg(mws50_ber), 66), sector))
N09 subtract(0.5, group_rank(ts_mean(vec_avg(mws50_bam), 22), sector))
N10 subtract(0.5, group_rank(ts_decay_linear(vec_avg(mws50_ber), 22), sector))
N11 subtract(0.5, group_rank(ts_mean(vec_avg(mws50_ber), 22), industry))
N12 subtract(0.5, group_rank(ts_corr(vec_avg(mws50_ber), vec_avg(mws50_aes), 22), sector))

设置：KOR/TOP600/D1 decay4 STATISTICAL trunc0.08
