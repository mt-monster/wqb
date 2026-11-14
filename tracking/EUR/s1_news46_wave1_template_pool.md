# EUR news46 模板池（2026-11-11 草拟，10 结构互异，待 val100 网格收官后派发）

> 字段画像：news46 = RavenPack News Analytics EUR 版（30 字段：19 VECTOR 事件级 + 11 MATRIX 聚合级）。
> OS 先例：Xgojww1X（[RISK,NEWS] 组合，news46 story-count 注意力腿）。塔位：NEWS 1/3。
> 模板来源：论坛 4 帖（nip 族 94 赞 / relevance 加权 31 赞 / 注意力摊薄 / 新闻密度 79 赞）+ 六步骨架。

| # | 模板 | 骨架（VEC 需 vec_avg） | 机制 | 来源 |
|---|---|---|---|---|
| N1 | nip 水平秩 | group_rank(vec_avg(mws46_nip), subindustry) | 新闻影响力预测分越高=定价越快 | 论坛 nip 族 94 赞 |
| N2 | nip 聚合均值变化 | group_rank(ts_delta(mws46_ravenpack_mean_nip,22),industry) | 影响力预期抬升 | 论坛 nip 族 |
| N3 | relevance×ssc 加权 | group_rank(multiply(vec_avg(mws46_ssc),vec_avg(mws46_relevance)),industry) | relevance 加权情绪（反裸 sentiment） | 论坛 31 赞 |
| N4 | 注意力密度 | group_rank(ts_sum(vec_avg(mws46_story_count),22),subindustry) | 新闻条数=关注度（OS 先例） | Xgojww1X + 79 赞 |
| N5 | 注意力突变 | group_zscore(ts_delta(ts_sum(vec_avg(mws46_story_count),22),5),subindustry) | 密度曲线一阶差 | 79 赞 |
| N6 | 注意力摊薄 | group_rank(divide(vec_avg(mws46_mce),add(vec_avg(mws46_story_count),vec_avg(mws46_mce))),industry) | 单事件注意力浓度 | 论坛摊薄帖 |
| N7 | novelty 过滤情绪 | group_rank(multiply(vec_avg(mws46_ess),divide(vec_avg(mws46_ens),100)),industry) | 新颖度高时情绪才可信 | 论坛 31 赞 |
| N8 | 慢变量 nip 水平 | ts_rank(mws46_ravenpack_mean_nip,66) | MATRIX 慢变量用水平面（快慢判据） | 快慢矩判据 |
| N9 | 均值 nip 时间分位 | group_rank(ts_rank(mws46_ravenpack_mean_nip,66),industry) | 影响力自身基线分位 | A8 时序分位 |
| N10 | 双向摊薄门控 | trade_when(greater(ts_sum(vec_avg(mws46_story_count),22),2),group_rank(vec_avg(mws46_nip),industry),-1) | 有新闻覆盖才建仓 | 门控族 |

## F 天花板预检纪律（派发前）
- news 事件族 EUR 实证 ret≤5% ⇒ F 系统性死（五集全证）。首波 10 条兼测 ret/TO：
- 若 best |S|<0.8 且 ret<3% ⇒ 快速判死转 news23（PE/VC）或放弃 news 塔 ATOM（只留组合腿）。
- 若 |S|≥1.0：按 val100 同款形状×设置穷举纪律推进。

## 归档路径
- 模板池：tracking/EUR/s1_news46_wave1_template_pool.md（本文件）
- 字段画像：tracking/EUR/reference/eur_news46_fields.json（已有）+ TOP2500 复核件归档
