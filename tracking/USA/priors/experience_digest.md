<!-- BEGIN WQB EXPERIENCE DIGEST -->
# USA 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:15
- 样本：4699 条 `attempt_knowledge`
- 知识版本（top3）：`eb06a6b8-f290a0e4` n=4557, `5283e546-f290a0e4` n=79, `bc303849-f290a0e4` n=30

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `vector_neut ( multiply ( subtract ( ts_zscore ( ts_mean ( divide ( F , F ) , N ) , N ) , ts_zscore ( ts_mean ( divide ( F , F ) , N ) , N ) ) , rank ( F ) ) , ts_backfill ( F , N ) )` | 20 | 19 | 1 | 2.52 | 2Y | 5% |
| `ts_zscore ( ts_sum ( F , N ) , N )` | 70 | 17 | 34 | 5.29 | UNKNOWN | 41% |
| `group_neutralize ( ts_zscore ( ts_sum ( F , N ) , N ) , F )` | 28 | 11 | 7 | 3.73 | SUB | 39% |
| `group_rank ( group_rank ( multiply ( rank ( ts_backfill ( F , N ) ) , rank ( ts_backfill ( F , N ) ) ) , bucket ( rank ( ts_backfill ( F , N ) ) , F N , N , N ) ) , F )` | 28 | 9 | 19 | 1.78 | UNKNOWN | 68% |
| `ts_corr ( vec_avg ( F ) , vec_avg ( F ) , N )` | 21 | 8 | 11 | 2.24 | SUB | 10% |
| `ts_decay_linear ( group_rank ( ts_zscore ( ts_backfill ( subtract ( vec_avg ( F ) , vec_avg ( F ) ) , N ) , N ) , F ) , N )` | 23 | 7 | 12 | 2.63 | SUB | 65% |
| `tail ( group_rank ( reverse ( ts_mean ( F , N ) ) , F ) , F N , F N , F N )` | 23 | 6 | 12 | 1.98 | FITNESS | 57% |
| `ts_rank ( F , N )` | 20 | 6 | 6 | 2.94 | 2Y | 50% |
| `tail ( winsorize ( group_rank ( ts_zscore ( F , N ) , F ) , F N ) , F N , F N , F N )` | 29 | 5 | 20 | 3.31 | SUB | 76% |
| `group_rank ( ts_mean ( F , N ) , F )` | 150 | 4 | 14 | 1.82 | FITNESS | 96% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `quantile ( ts_arg_max ( ts_backfill ( F , N ) , N ) )` | 62 | 0 | 0 | 0.88 | 2Y | 100% |
| `quantile ( ts_arg_min ( ts_backfill ( F , N ) , N ) )` | 49 | 0 | 0 | 0.65 | 2Y | 100% |
| `quantile ( subtract ( ts_backfill ( F , N ) , ts_backfill ( F` | 24 | 0 | 0 | 0.7 | 2Y | 100% |

## 待确认提案

- dead_families: 3
- dead_skeletons: 3
- wins: 7
- rules: 6（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `eb06a6b8-f290a0e4` (n=4557)
- win 6.2% / near 30.6% / dead 62.8% / 最高|S| 9.25
- vs 上一版：win +6.2% / near +30.6% / dead -37.2%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


