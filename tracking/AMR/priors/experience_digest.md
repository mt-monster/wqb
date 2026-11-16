<!-- BEGIN WQB EXPERIENCE DIGEST -->
# AMR 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:25
- 样本：343 条 `attempt_knowledge`
- 知识版本（top3）：`b95dd38d-146eda12` n=343

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `add ( multiply ( N , ts_decay_linear ( ts_rank ( ts_backfill ( multiply ( N , F ) , N ) , N ) , N ) ) , group_neutralize ( rank ( ts_backfill ( F , N ) ) , F ) )` | 2 | 2 | 0 | 2.0 | UNKNOWN | 100% |
| `ts_decay_linear ( ts_rank ( ts_backfill ( multiply ( N , F ) , N ) , N ) , N )` | 13 | 0 | 9 | 1.82 | FITNESS | 100% |
| `ts_rank ( ts_backfill ( vec_avg ( F ) , N ) , N )` | 7 | 0 | 3 | 1.06 | 2Y | 100% |
| `group_zscore ( F , F )` | 4 | 0 | 3 | 1.14 | 2Y | 25% |
| `signed_power ( ts_decay_linear ( ts_rank ( ts_backfill ( multiply ( N , F ) , N ) , N ) , N ) , N )` | 2 | 0 | 2 | 1.7 | FITNESS | 100% |
| `multiply ( N , ts_rank ( ts_delta ( F , N ) , N ) )` | 2 | 0 | 1 | 1.14 | 2Y | 100% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `ts_zscore ( F , N )` | 33 | 0 | 0 | 0.98 | FITNESS | 100% |
| `group_rank ( ts_backfill ( vec_avg ( F ) , N ) , F )` | 16 | 0 | 0 | 0.26 | 2Y | 100% |
| `rank ( F )` | 9 | 0 | 0 | 0.57 | 2Y | 100% |
| `ts_mean ( vec_avg ( F ) , N )` | 9 | 0 | 0 | 0.8 | FITNESS | 100% |
| `ts_delta ( vec_avg ( F ) , N ) ts_delay ( vec_avg ( F ) , N )` | 8 | 0 | 0 | 0.42 | 2Y | 100% |
| `ts_decay_linear ( vec_avg ( F ) , N )` | 8 | 0 | 0 | 0.57 | 2Y | 100% |
| `ts_zscore ( ts_mean ( vec_avg ( F ) , N ) , N )` | 8 | 0 | 0 | 0.57 | 2Y | 100% |
| `ts_zscore ( rank ( F ) , N )` | 8 | 0 | 0 | 0.58 | 2Y | 100% |
| `ts_rank ( vec_avg ( F ) , N )` | 8 | 0 | 0 | 0.97 | FITNESS | 100% |
| `ts_zscore ( vec_avg ( F ) , N )` | 7 | 0 | 0 | 0.5 | 2Y | 100% |

## 待确认提案

- dead_families: 0
- dead_skeletons: 32
- wins: 0
- rules: 32（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `b95dd38d-146eda12` (n=343)
- win 1.2% / near 7.3% / dead 91.5% / 最高|S| 2.56

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


