<!-- BEGIN WQB EXPERIENCE DIGEST -->
# IND 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:19
- 样本：1928 条 `attempt_knowledge`
- 知识版本（top3）：`9631073e-5b4ce2c0` n=1709, `97b9bcd2-5b4ce2c0` n=219

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `rank ( ts_regression ( ts_zscore ( F , N ) , ts_zscore ( F , N ) , N , F N ) )` | 58 | 39 | 16 | 4.79 | UNKNOWN | 33% |
| `signed_power ( subtract ( group_rank ( divide ( subtract ( ts_backfill ( vec_avg ( F ) , N ) , ts_mean ( ts_backfill ( vec_avg ( F ) , N ) , N ) ) , add ( abs ( ts_mean ( ts_backfill ( vec_avg ( F ) , N ) , N ) ) , N ) ) , F ) , N ) , N )` | 26 | 13 | 12 | 1.67 | UNKNOWN | 54% |
| `rank ( ts_regression ( ts_zscore ( F , N ) , ts_zscore ( ts_backfill ( F , N ) , N ) , N , F N ) )` | 16 | 12 | 2 | 2.82 | UNKNOWN | 88% |
| `rank ( ts_regression ( ts_zscore ( F , N ) , ts_zscore ( ts_backfill ( vec_avg ( F ) , N ) , N ) , N , F N ) )` | 27 | 8 | 17 | 2.45 | 2Y | 63% |
| `rank ( ts_mean ( ts_backfill ( F , N ) , N ) )` | 22 | 8 | 4 | 4.77 | SHARPE | 64% |
| `group_rank ( ts_regression ( ts_zscore ( F , N ) , ts_zscore ( ts_delta ( subtract ( F , F ) , N ) , N ) , N , F N ) , F )` | 8 | 8 | 0 | 3.34 | - | 0% |
| `rank ( ts_regression ( ts_zscore ( F , N ) , ts_rank ( ts_backfill ( vec_avg ( F ) , N ) , N ) , N , F N ) )` | 10 | 7 | 1 | 2.19 | UNKNOWN | 70% |
| `group_rank ( ts_mean ( ts_backfill ( F , N ) , N ) , F )` | 57 | 6 | 33 | 1.87 | SHARPE | 89% |
| `rank ( ts_delta ( ts_backfill ( F , N ) , N ) )` | 22 | 5 | 6 | 5.18 | 2Y | 68% |
| `ts_target_tvr_hump ( multiply ( N , signed_power ( subtract ( group_rank ( divide ( subtract ( ts_backfill ( F , N ) , ts_mean ( ts_backfill ( F , N ) , N ) ) , add ( abs ( ts_mean ( ts_backfill ( F , N ) , N ) ) , N ) ) , F ) , N ) , N ) ) , F N )` | 14 | 4 | 1 | 3.35 | SHARPE | 71% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `ts_rank ( ts_backfill ( vec_avg ( F ) , N ) , N )` | 14 | 0 | 0 | 0.6 | 2Y | 100% |
| `group_rank ( ts_mean ( vec_avg ( F ) , N ) , F )` | 12 | 0 | 0 | 0.96 | 2Y | 100% |
| `group_rank ( ts_delta ( vec_avg ( F ) , N ) , F )` | 10 | 0 | 0 | 0.45 | FITNESS | 100% |

## 待确认提案

- dead_families: 0
- dead_skeletons: 6
- wins: 0
- rules: 6（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `9631073e-5b4ce2c0` (n=1709)
- win 12.7% / near 36.5% / dead 50.7% / 最高|S| 7.28
- vs 上一版：win +12.7% / near +32.4% / dead -45.2%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->



