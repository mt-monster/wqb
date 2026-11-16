<!-- BEGIN WQB EXPERIENCE DIGEST -->
# HKG 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:24
- 样本：425 条 `attempt_knowledge`
- 知识版本（top3）：`ae3da471-581d98fe` n=403, `def402de-581d98fe` n=22

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `group_rank ( ts_mean ( F , N ) , F )` | 32 | 11 | 3 | 2.34 | 2Y | 62% |
| `group_zscore ( divide ( ts_mean ( subtract ( F , F ) , N ) , ts_std_dev ( subtract ( F , F ) , N ) ) , F )` | 21 | 6 | 7 | 2.42 | 2Y | 71% |
| `trade_when ( rank ( divide ( F , ts_mean ( F , N ) ) ) N , signed_power ( subtract ( N , group_rank ( ts_decay_linear ( F , N ) , F ) ) , N ) , rank ( divide ( F , ts_mean ( F , N ) ) ) N )` | 2 | 1 | 1 | 2.87 | SHARPE | 50% |
| `reverse ( group_zscore ( ts_mean ( subtract ( F , F ) , N ) , F ) )` | 3 | 1 | 0 | 1.97 | 2Y | 67% |
| `group_zscore ( ts_mean ( F , N ) , F )` | 2 | 1 | 0 | 2.0 | UNKNOWN | 100% |
| `signed_power ( rank ( ts_rank ( F , N ) ) , N ) F` | 13 | 0 | 12 | 1.64 | - | 0% |
| `group_rank ( F , F )` | 29 | 0 | 11 | 1.36 | 2Y | 28% |
| `rank ( ts_rank ( ts_mean ( F , N ) , N ) )` | 8 | 0 | 8 | 1.78 | - | 0% |
| `rank ( ts_rank ( ts_mean ( F , N ) , N ) ) F` | 8 | 0 | 8 | 1.58 | - | 0% |
| `reverse ( group_zscore ( ts_mean ( subtract ( F , F ) , N ) , bucket ( rank ( F ) , F N , N , N ) ) )` | 7 | 0 | 7 | 2.11 | 2Y | 100% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `group_zscore ( ts_mean ( vec_avg ( F ) , N ) , F )` | 9 | 0 | 0 | 0.49 | 2Y | 100% |
| `group_rank ( ts_mean ( vec_avg ( F ) , N ) , F )` | 8 | 0 | 0 | 0.73 | FITNESS | 100% |
| `subtract ( N , group_rank ( ts_mean ( vec_avg ( F ) , N ) , F ) )` | 7 | 0 | 0 | 0.49 | 2Y | 100% |
| `group_rank ( ts_mean ( subtract ( F , F ) , N ) , F )` | 6 | 0 | 0 | 0.47 | 2Y | 100% |
| `divide ( rank ( ts_mean ( F , N ) ) , add ( N , rank ( ts_mean ( F , N ) ) ) )` | 4 | 0 | 0 | 0.21 | 2Y | 100% |
| `group_rank ( ts_delta ( ts_backfill ( winsorize ( F , F N ) , N ) , N ) , F )` | 4 | 0 | 0 | 0.64 | 2Y | 100% |
| `group_rank ( ts_zscore ( F , N ) , F )` | 4 | 0 | 0 | 0.69 | 2Y | 100% |
| `group_rank ( ts_mean ( divide ( divide ( ts_backfill ( F , N ) , ts_backfill ( F , N ) ) , F` | 4 | 0 | 0 | 0.88 | 2Y | 100% |
| `group_zscore ( subtract ( F , F ) , F )` | 3 | 0 | 0 | 0.28 | FITNESS | 100% |
| `group_rank ( subtract ( ts_scale ( ts_zscore ( ts_backfill ( winsorize ( F , F N ) , N ) , N ) , N ) , ts_scale ( ts_zscore ( ts_backfill ( winsorize ( F , F N ) , N ) , N ) , N ) ) , F )` | 3 | 0 | 0 | 0.51 | 2Y | 100% |

## 待确认提案

- dead_families: 0
- dead_skeletons: 12
- wins: 0
- rules: 12（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `ae3da471-581d98fe` (n=403)
- win 7.7% / near 28.8% / dead 63.5% / 最高|S| 2.87
- vs 上一版：win +7.7% / near +6.0% / dead -13.8%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


