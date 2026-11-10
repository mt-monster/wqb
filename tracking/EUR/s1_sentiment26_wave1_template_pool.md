# EUR × sentiment26 · W1 模板池（2026-11-09，残余评估最后实测对象）

> 数据集本质：**DNS 域名注意力**（Cisco Umbrella 流行度排名），非传统情绪。SENTIMENT 塔 ×1.4（2/3 差 1）。
> 19 字段全 VECTOR（需 vec_avg）；cov：主字段 0.7482 / rank 0.5835 / dltcc 1.0（ccTLD 元数据）；设置 TOPCS1600/SUBIND/decay4/trunc0.08/maxTrade OFF/nan ON。
> 机制先验：Da et al. 2011 注意力（DNS 版）——公众注意力高→过度定价→低收益（反向先验，方向以回测为准）。EUR 公众注意力族历史：other571/search_interest/behavioral_signals 均归档——本集独特处 = **形态学读数（kurtosis/skewness）与分位排名结构无历史**。
> 判读纪律：近闸臂 → **立即族代表 prod 预判**（FHP 教训）；全波 |S|<0.5 → 整集归档（sentiment 类别封盘）。

| # | 结构 | 表达式要点 | 字段 |
|---|---|---|---|
| T1 | 注意力广度 level-z | ts_mean(group_zscore(vec_avg(relpopularity1),country),5) | relpopularity1 |
| T2 | 广度 α=0.8 对照 | 同构 relpopularity08 | relpopularity08 |
| T3 | 排名水平 z（先验负向：热门=rank 低=跌） | ts_mean(group_zscore(vec_avg(rank),country),5) | rank |
| T4 | 峰度 z（注意力集中形态，全新） | ts_mean(group_zscore(vec_avg(kurtosis),country),5) | kurtosis |
| T5 | 偏度 z（全新） | ts_mean(group_zscore(vec_avg(skewness),country),5) | skewness |
| T6 | 域名广度 z | ts_mean(group_zscore(vec_avg(totaldomains),country),5) | totaldomains |
| T7 | 国际化域名占比 | z(vec_avg(totalcountrydomains)/vec_avg(totaldomains)) | totalcountrydomains+totaldomains |
| T8 | 头部注意力集中度 | z(vec_avg(rank)−vec_avg(top10pctrankingavg)) | rank+top10pctrankingavg |
| T9 | 分位排名梯度 | z(vec_avg(top10pctrankingavg)−vec_avg(top75pctrankingavg)) | top10/75pctrankingavg |
| T10 | 平均排名短动量 | ts_delta(vec_avg(avgranking),5) | avgranking |
| 覆盖 | ccTLD 计数+剩余分位+topranking+PIT 门控 | vec_count/trade_when 组合覆盖 dltcc/top10-75pctranking/topranking/wq_pit | 余下字段 |
