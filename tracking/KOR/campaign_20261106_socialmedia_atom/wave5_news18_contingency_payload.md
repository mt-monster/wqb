# Wave5 news18 Ravenpack 应急载荷（READY · 3b+4 双灭后）

> 启用：Wave3b 与 Wave4 均 max|S|<1.0。
> 模板 12 结构互异；MATRIX 裸用 / VECTOR 包 vec_avg；禁混 PV。
> preflight valid=true unknown=[]
> 算子数：R01_ess_earn=3, R02_css_biz=3, R03_nip_biz=3, R04_ess_biz=3, R05_ssc_rel=7, R06_qep=4, R07_ess_dlt=4, R08_nip_earn=3, R09_css_rev=3, R10_qcm=4, R11_ssc_z=4, R12_ess_rev_arm=3

## 首派 8（decay=4 STATISTICAL）
R01_ess_earn subtract(0.5, group_rank(ts_mean(rp_ess_earnings, 22), sector))
R02_css_biz subtract(0.5, group_rank(ts_mean(rp_css_business, 22), sector))
R03_nip_biz subtract(0.5, group_rank(ts_mean(rp_nip_business, 22), sector))
R04_ess_biz subtract(0.5, group_rank(ts_mean(rp_ess_business, 22), sector))
R05_ssc_rel subtract(0.5, group_rank(ts_mean(multiply(vec_avg(nws18_ssc), divide(vec_avg(nws18_relevance), 100)), 22), sector))
R06_qep subtract(0.5, group_rank(ts_mean(vec_avg(nws18_qep), 22), sector))
R07_ess_dlt subtract(0.5, group_rank(ts_mean(ts_delta(rp_ess_earnings, 22), 5), sector))
R08_nip_earn subtract(0.5, group_rank(ts_mean(rp_nip_earnings, 22), sector))

## 储备
R09_css_rev subtract(0.5, group_rank(ts_mean(rp_css_revenue, 22), sector))
R10_qcm subtract(0.5, group_rank(ts_mean(vec_avg(nws18_qcm), 22), sector))
R11_ssc_z subtract(0.5, group_rank(ts_zscore(vec_avg(nws18_ssc), 66), sector))
R12_ess_rev_arm subtract(group_rank(ts_mean(rp_ess_earnings, 22), sector), 0.5)

设置：KOR/TOP600/D1 decay4 STATISTICAL trunc0.08 nan OFF
注意：论坛 EUR news18 难搞≠KOR判死；优先 ESS/NIP/CSS×主题轴。
