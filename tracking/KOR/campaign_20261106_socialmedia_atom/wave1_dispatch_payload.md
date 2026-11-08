# Wave1 派发载荷（READY · 未提交）

> 仅在用户聊天明文确认「发」后，用 MCP `create_multi_simulation` 提交下列参数。
> 问卷超时自动勾选 **不算** 授权。

```json
{
  "region": "KOR",
  "universe": "TOP600",
  "delay": 1,
  "decay": 4,
  "neutralization": "STATISTICAL",
  "truncation": 0.08,
  "unit_handling": "VERIFY",
  "nan_handling": "OFF",
  "pasteurization": "ON",
  "max_trade": "OFF",
  "language": "FASTEXPR",
  "wait_for_completion": false,
  "validate_fields": true,
  "alpha_expressions": [
    "subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(aggregate_comment_volume), 22), 5), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_stddev(aggregate_comment_volume), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_sell_opinion_score), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_buy_opinion_score), 22), sector))",
    "group_rank(ts_mean(subtract(vec_avg(aggregate_buy_opinion_score), vec_avg(aggregate_sell_opinion_score)), 22), sector)",
    "subtract(group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), sector), 0.5)",
    "subtract(0.5, group_rank(ts_mean(vec_avg(total_distinct_participants_count), 22), sector))"
  ],
  "tags": [
    "T01_attn_lvl",
    "T02_attn_delta",
    "T03_attn_std",
    "T04_sell",
    "T05_buy",
    "T06_net",
    "T01_rev",
    "T08_breadth"
  ]
}
```

提交后：用返回的 location → `lookINTO_SimError_message` / `batch_status` 盯进度 → `harvest_multisim_alphas` 收割。
