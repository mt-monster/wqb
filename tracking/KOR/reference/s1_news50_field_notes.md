# S1 字段理解：news50（KOR/TOP600/D1）

- 数据集类型：81 字段全 VECTOR（RavenPack 事件新闻），coverage≈0.65（主族）/0.54（元数据族）/0.35（ens 族）
- 主题：事件新闻多维评分——分析师推荐变更、事件新颖度、新闻冲击力预测、事件量、正面事件比率
- **定位差异化**：KOR 新闻 tone/sentiment 族已三波判死（news87/news96/news141），本集避开 *_sentiment_score tone 字段，走 analyst-rec-change + novelty + impact-projection 非情绪机制

## 字段/特征/建议

- 特征：0-100 评分类偏态需 rank；计数字段（event_count/vea）非负偏态；d0 与 twn 为同一信号双 cutoff 变体（选 d0，users=0 更冷门）
- 建议：主信号 = analyst_recommendation_change_score_d0（users=0，与 wave 143 EPS 修订 WIN 同机制族）/ news_volatility_projection_score_d0（users=0）/ event_novelty_score_d0（users=0）；辅助 = positive_event_ratio_score_d0 / mws50_vea（事件量过度关注）；vec_avg + ts_backfill 22；industry/sector 组内相对化；ts_decay_linear 平滑（wave 143 验证 +0.07S）
- 风险提示：mws50_ess/ens 族覆盖 0.35 禁用；元数据字段（category/time/type/group/property/*_key）非数值禁用；coverage 0.65 边缘，低覆盖硬门要求 ts_backfill

## 初始信号

1. 分析师推荐变更动量（analyst_recommendation_change_score_d0，正向：推荐上调→漂移）
2. 新闻冲击力预测（news_volatility_projection_score_d0，方向待验证：高冲击→过度反应反转 or 波动规避）
3. 正面事件比率（positive_event_ratio_score_d0，正向）

## 进阶信号

- 事件新颖度门控：event_novelty_score_d0 高 = 新信息含量高
- 事件量过度关注：mws50_vea 91 日事件量 → 负向（attention reversal）
- industry 组内相对化（wave 143 验证 industry > sector +0.10S）
- ts_decay_linear(x, 22) 平滑提 Sharpe

## 预处理决策

- VECTOR → vec_avg 聚合；日间无更新 → ts_backfill 22 补洞
- 0-100 评分 → rank 强制；计数 → rank 强制
- d0 变体优先（users=0，避开 twn 拥挤）
