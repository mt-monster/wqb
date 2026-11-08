# Wave4 news66 应急派发载荷（READY · Wave3b 再灭后）

> 启用条件：Wave3b news20 decay=10 再灭（max|S|<1.0）。
> 模板 ≥12 结构互异（水平/变化/方差/反向/时序秩/倒数/zscore/decay_linear/group_zscore/幂次/行业轴）。
> 首派取前 8；V09–V12 留第二批。算子数 3–6 ≤12。preflight 已绿（mws66_api_views）。
> 论文：Guo/Peng/Tao/Tu 2017 Joint News Attention Spillover — 注意力传染 ⇒ 浏览量水平与变化可定价；本集仅单字段注意力代理。

## 首派 8（decay=4 STATISTICAL）
V01 subtract(0.5, group_rank(ts_mean(vec_avg(mws66_api_views), 22), sector))
V02 subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(mws66_api_views), 22), 5), sector))
V03 subtract(0.5, group_rank(ts_mean(vec_stddev(mws66_api_views), 22), sector))
V04 subtract(group_rank(ts_mean(vec_avg(mws66_api_views), 22), sector), 0.5)
V05 subtract(0.5, group_rank(ts_rank(vec_avg(mws66_api_views), 66), sector))
V06 subtract(0.5, group_rank(ts_mean(divide(1, add(vec_avg(mws66_api_views), 1)), 22), sector))
V07 subtract(0.5, group_rank(ts_zscore(vec_avg(mws66_api_views), 66), sector))
V08 subtract(0.5, group_rank(ts_decay_linear(vec_avg(mws66_api_views), 22), sector))

## 储备
V09 group_zscore(ts_mean(vec_avg(mws66_api_views), 22), sector)
V10 subtract(0.5, group_rank(ts_delta(vec_avg(mws66_api_views), 66), sector))
V11 subtract(0.5, group_rank(signed_power(ts_mean(vec_avg(mws66_api_views), 22), 2), sector))
V12 subtract(0.5, group_rank(ts_mean(vec_avg(mws66_api_views), 22), industry))

设置：KOR/TOP600/D1 decay4 STATISTICAL trunc0.08 nan OFF pasteurization ON

## Preflight（本回合）
valid=true unknown=[] fields=["mws66_api_views"]
