# Wave3b news20 Mode A decay 备胎（READY · 仅 Wave3 弱读数后）

> 启用条件：Wave3 news20（decay=4）收割后 max|S|<1.0，但非字段全空/语法废批。
> 依据：论坛 43554129390103「新闻情绪时效短，decay 必须调大」。
> 继承：同骨架 + 注意力加权/corr；只动 decay=10。算子数 4-7 不超过 12。

## 表达式（decay=10）
1. subtract(0.5, group_rank(ts_mean(vec_avg(nws20_ssc), 22), sector))
2. subtract(0.5, group_rank(ts_mean(multiply(vec_avg(nws20_ssc), divide(vec_avg(nws20_relevance), 100)), 22), sector))
3. subtract(0.5, group_rank(ts_mean(vec_avg(nws20_nip), 22), sector))
4. subtract(0.5, group_rank(ts_mean(vec_avg(nws20_event_sentiment_score), 22), sector))
5. subtract(0.5, group_rank(ts_mean(vec_avg(nws20_rp_story_event_count), 22), sector))
6. subtract(0.5, group_rank(ts_corr(vec_avg(nws20_rp_story_event_count), vec_avg(nws20_ssc), 22), sector))
7. subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(nws20_ssc), 22), 5), sector))
8. subtract(0.5, group_rank(ts_mean(multiply(vec_avg(nws20_ssc), vec_avg(nws20_rp_story_event_count)), 22), sector))

设置：KOR/TOP600/D1 STATISTICAL trunc0.08 nan OFF pasteurization ON maxTrade OFF

## 决策顺序
1. Wave3 decay4 收割
2. S>=1.58 破闸；1.0<=S<1.58 换 R&M/industry/倒数
3. max|S|<1.0 -> 本备胎 decay=10（论坛先验）
4. 本备胎再灭 -> news66
