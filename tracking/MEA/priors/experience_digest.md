<!-- BEGIN WQB EXPERIENCE DIGEST -->
# MEA 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:22
- 样本：488 条 `attempt_knowledge`
- 知识版本（top3）：`na-3dc4cb2c` n=488

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `( ( rank ( ts_delta ( divide ( ts_backfill ( vec_avg ( F ) , N ) , ts_backfill ( vec_avg ( F ) , N ) ) , N ) ) N ) ( rank ( divide ( ts_backfill ( vec_avg ( F ) , N ) , ts_backfill ( vec_avg ( F ) , N ) ) ) N ) ) ( rank ( ts_mean ( F , N ) ) N )` | 24 | 0 | 23 | 1.56 | - | 0% |
| `ts_decay_linear ( rank ( vec_avg ( F ) vec_avg ( F ) ) , N )` | 19 | 0 | 17 | 2.12 | - | 0% |
| `rank ( subtract ( vec_avg ( F ) , vec_avg ( F ) ) ) N rank ( divide ( ts_backfill ( vec_avg ( F ) , N ) , ts_backfill ( vec_avg ( F ) , N ) ) ) N` | 17 | 0 | 16 | 1.47 | - | 0% |
| `( rank ( ts_delta ( divide ( ts_backfill ( vec_avg ( F ) , N ) , ts_backfill ( vec_avg ( F ) , N ) ) , N ) ) N ) ( rank ( ts_mean ( F , N ) ) N )` | 16 | 0 | 15 | 1.59 | - | 0% |
| `add ( multiply ( rank ( subtract ( vec_avg ( F ) , vec_avg ( F ) ) ) , N ) , multiply ( rank ( multiply ( ts_delta ( vec_avg ( F ) , N ) , N ) ) , N ) )` | 15 | 0 | 15 | 1.93 | - | 0% |
| `( ( rank ( ts_delta ( divide ( ts_backfill ( vec_avg ( F ) , N ) , ts_backfill ( vec_avg ( F ) , N ) ) , N ) ) N ) ( rank ( ts_mean ( F , N ) ) N ) ) ( rank ( subtract ( vec_avg ( F ) , vec_avg ( F ) ) ) N )` | 15 | 0 | 15 | 1.69 | - | 0% |
| `rank ( ts_delta ( divide ( ts_backfill ( vec_avg ( F ) , N ) , ts_backfill ( vec_avg ( F ) , N ) ) , N ) )` | 24 | 0 | 14 | 1.39 | - | 0% |
| `rank ( vec_avg ( F ) vec_avg ( F ) )` | 22 | 0 | 14 | 2.13 | - | 0% |
| `add ( multiply ( rank ( subtract ( vec_avg ( F ) , vec_avg ( F ) ) ) , N ) , multiply ( rank ( multiply ( ts_zscore ( vec_avg ( F ) , N ) , N ) ) , N ) )` | 14 | 0 | 13 | 2.12 | - | 0% |
| `rank ( subtract ( vec_avg ( F ) , vec_avg ( F ) ) ) N rank ( subtract ( vec_avg ( F ) , vec_avg ( F ) ) ) N rank ( divide ( ts_backfill ( vec_avg ( F ) , N ) , ts_backfill ( vec_avg ( F ) , N ) ) ) N` | 11 | 0 | 11 | 1.77 | - | 0% |

## 统计死路（advisory，不是硬禁；top 10）

（暂无）

## 待确认提案

- dead_families: 0
- dead_skeletons: 0
- wins: 0
- rules: 0（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `na-3dc4cb2c` (n=488)
- win 0.0% / near 58.0% / dead 34.2% / 最高|S| 2.38

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->



