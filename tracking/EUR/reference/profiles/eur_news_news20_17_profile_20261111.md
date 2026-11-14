# EUR news 塔 W1：news20/news17 跨集画像（2026-11-11）

> 塔：NEWS（1/3 未点亮，乘数 1.4）；数据集均 RavenPack 系事件明细（全 VECTOR，需 vec_* 聚合）

## news20（68 字段，cov 0.48-1.0，aC 0-8 低拥挤）
- 情绪分类器族：acb(盈利)/bam(公司行为)/bee(盈利评估)/ber(分析师推荐)/qep(正负词)/qmb(M&A)/nip(市场冲击)/ssc(连续情绪)/qcm(语调)/ghc_lna
- 事件元数据族：event_relevance(0-100)/event_sentiment_score(-1~1)/event_similarity_days
- 计数族：rp_story_event_count；时间戳/文本/国家族（非信号）

## news17（88 字段，cov 0.27-0.98，aC 0-9 低拥挤）
- 同 RavenPack 结构 + analyst_recommendation_change_score（aC 5）
- multiple_comp / comp_d1 双口径（与 news20 同构）

## W1 波（multisim 4pmcWI1Mh56xbQkP9VRtrKP，10 条）
N1 ssc 水平 / N2 ssc z / N3 acb-bam 差 / N4 nip 反转 / N5 相关度加权情绪 / N6 相似事件新鲜度 / N7 新闻量能反转 / N8 ssc 5日动量 / N9 双分类器一致性 / N10 news17_acb 跨集对照
- 全部 vec_avg/vec_sum 聚合，算子 2-5 个/条
- 设计依据：news 类先验「水平类几何 > 变化类」（语调是慢水平信号，DEU 实证 T2>T5 部分应验）

## 判据预锁
max|S| < 1.0 ⇒ news20/17 判弱；S≥1.58 进相关性验证；分组轴用 subindustry（国家族 country_code 可做 group 轴备选）
