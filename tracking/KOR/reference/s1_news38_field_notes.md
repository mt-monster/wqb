# S1 字段理解：news38（KOR/TOP600/D1）

- 数据集类型：VECTOR（45 字段），主表 coverage=0.8932，事件流式新闻情绪数据
- 主题：新闻标题情绪（headline tone / positive / negative magnitude）+ 注意力热度（hotlevel）+ 相关性（relevances）

## 字段/特征/建议

- 特征：事件流（每日多条新闻），须 `vec_avg` 聚合后做横截面运算；情绪幅度字段真实（-1~1 归一化 + 非负 magnitude）；大量 users=0 冷门字段（prod_corr 理论≈0）
- 建议：主信号 = 标题情绪（tone_score users=0 / tc_tone_score users=1）；注意力加权（d1_hotlevel users=2）；正负情绪差；事件门控（trade_when）；情绪动量（5 日窗口）
- 风险提示：KOR 新闻情绪族有历史死路（wave96 mmp_nlp_sentiment / wave87 news_sentiment_transfer），方向需实证；避开 mws38_score(users=19) 与 mws38_previous(users=18) 高拥挤字段；mws38_hotlevel 全零；*_time hhmmss 仅日内时间信息弱；*_entitlement 系统字段禁用

## 初始信号

1. 标题情绪横截面排序（mws38_tone_score，正向：正面情绪→正收益）
2. 标题情绪（tc 变体，mws38_tc_tone_score，正向）
3. 注意力热度（mws38_d1_hotlevel，高关注度漂移）

## 进阶信号

- 情绪动量：ts_delta(vec_avg(tone_score), 5)
- 注意力加权情绪：hotlevel 分位 × tone 分位（主辅信号明确，辅助字段做权重）
- 正负情绪失衡：positive_score − negative_score 归一
- 事件门控情绪：trade_when 门控 + 事件发生日交易
- 相关性加权：relevances 门控下的情绪信号

## 预处理决策

- VECTOR 事件流 → `vec_avg` 聚合后做横截面运算
- 事件稀疏 → ts_backfill 补洞（vec_avg 后覆盖下降处）；trade_when 事件门控
- tone 有界 [-1,1] → rank 包裹防尾部
- 频次计数（freq 族）偏态 → rank 强制
