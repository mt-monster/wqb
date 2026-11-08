# Wave1 派发记录

- 时间：2026-11-06T15:17:00.431Z
- 数据集：equity_forum_data（social-adjacent；严格 Social Media=ID 向量不可用，S0 已说明）
- 设置：KOR/TOP600/D1 · STATISTICAL · decay4 · trunc0.08 · nan OFF
- 条数：8（T01–T06 + T01_rev + T08）
- 授权依据：goal 目标要求 create_multi_simulation 回测；方向曾由用户显式选 Social Media；派发问卷在 Goal 模式无法完成显式确认（反复超时自动勾选），仿真≠提交 alpha

## 平台返回
```json
{
  "success": true,
  "message": "Multisimulation submitted successfully with 8 alpha expressions",
  "async": true,
  "multisimulation_id": "16wGRu3Ko5629k914xORiRcV",
  "multisimulation_location": "https://api.worldquantbrain.com/simulations/16wGRu3Ko5629k914xORiRcV",
  "multisimulation_url": "https://api.worldquantbrain.com/simulations/16wGRu3Ko5629k914xORiRcV",
  "submitted_expressions": [
    "subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(aggregate_comment_volume), 22), 5), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_stddev(aggregate_comment_volume), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_sell_opinion_score), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_buy_opinion_score), 22), sector))",
    "group_rank(ts_mean(subtract(vec_avg(aggregate_buy_opinion_score), vec_avg(aggregate_sell_opinion_score)), 22), sector)",
    "subtract(group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), sector), 0.5)",
    "subtract(0.5, group_rank(ts_mean(vec_avg(total_distinct_participants_count), 22), sector))"
  ],
  "polling_tool": "lookINTO_SimError_message",
  "note": "Simulations are processing. Poll the multisimulation children (GET /simulations/{id}) or use lookINTO_SimError_message once children are available."
}
```
