# Wave3 news20 应急派发载荷（READY · 未派发）

> 启用条件：Wave2 other553 按 `wave3_decision_tree.md` 判全灭。
> preflight 2026-11-06：valid=true · unknown_fields=[] · 10/10。
> 模板来源：论坛 news20 降噪 + relevance 加权；RavenPack CSS×REL / novelty 论文同构。
> 首派建议取前 8 条（并发友好）；N09/N10 留第二批或替换。

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
    "subtract(0.5, group_rank(ts_mean(vec_avg(nws20_ssc), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(multiply(vec_avg(nws20_ssc), divide(vec_avg(nws20_relevance), 100)), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(nws20_nip), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(nws20_event_sentiment_score), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(nws20_event_similarity_days), 66), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(nws20_rp_story_event_count), 22), sector))",
    "subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(nws20_ssc), 22), 5), sector))",
    "subtract(0.5, group_rank(ts_mean(vec_avg(nws20_qmb), 22), sector))"
  ],
  "tags": [
    "N01_ssc",
    "N02_ssc_rel",
    "N03_nip",
    "N04_evt_snt",
    "N05_novelty",
    "N06_evt_cnt",
    "N07_ssc_dlt",
    "N08_qmb"
  ],
  "reserve": {
    "N09_qep": "subtract(0.5, group_rank(ts_mean(vec_avg(nws20_qep), 22), sector))",
    "N10_ssc_std": "subtract(0.5, group_rank(ts_mean(vec_stddev(nws20_ssc), 22), sector))"
  }
}
```
## 设置备注（论坛）
- 新闻情绪时效短：可试 **decay=8~10**（论坛「衰减要大」）；首波仍用 decay=4 与战役默认对齐，活苗后再 Mode A 扫 decay。
- 已嵌入：N02=ssc×relevance；N05=novelty 天数；N06=story event count。
- 破闸加试：`nws20_ghc_lna` 变化臂；relevance 阈值门控（>60）若平台表达允许。
