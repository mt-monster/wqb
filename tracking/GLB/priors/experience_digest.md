<!-- BEGIN WQB EXPERIENCE DIGEST -->
# GLB 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:17
- 样本：3078 条 `attempt_knowledge`
- 知识版本（top3）：`adbe6733-1f42b1f2` n=3011, `a7051cdf-1f42b1f2` n=61, `720fe788-1f42b1f2` n=6

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `trade_when ( rank ( ts_mean ( F , N ) ) N , signed_power ( subtract ( group_rank ( F , F ) , N ) , N ) , rank ( ts_mean ( F , N ) ) N )` | 136 | 46 | 54 | 4.81 | SHARPE | 53% |
| `signed_power ( subtract ( group_rank ( F , F ) , N ) , N )` | 36 | 21 | 7 | 4.61 | SHARPE | 25% |
| `trade_when ( rank ( ts_mean ( F , N ) ) N , signed_power ( subtract ( group_rank ( F , F ) , N ) , N ) , N )` | 45 | 19 | 22 | 4.14 | FITNESS | 44% |
| `trade_when ( rank ( ts_mean ( vec_avg ( F ) , N ) ) N , signed_power ( subtract ( group_rank ( F , F ) , N ) , N ) , rank ( ts_mean ( vec_avg ( F ) , N ) ) N )` | 36 | 14 | 11 | 3.45 | SHARPE | 53% |
| `group_zscore ( ts_decay_linear ( F , N ) , F )` | 135 | 13 | 63 | 3.13 | SHARPE | 72% |
| `signed_power ( group_rank ( ts_zscore ( ts_mean ( F , N ) , N ) , F ) , N )` | 22 | 12 | 6 | 5.95 | 2Y | 45% |
| `N group_zscore ( ts_decay_linear ( F , N ) , F )` | 41 | 9 | 21 | 2.99 | SHARPE | 76% |
| `group_zscore ( F , F )` | 14 | 9 | 0 | 4.45 | UNKNOWN | 21% |
| `trade_when ( rank ( ts_delta ( F , N ) ) N , signed_power ( subtract ( group_rank ( F , F ) , N ) , N ) , N )` | 12 | 7 | 5 | 3.8 | 2Y | 42% |
| `trade_when ( and ( rank ( ts_mean ( vec_avg ( F ) , N ) ) N , rank ( F ) N ) , signed_power ( subtract ( group_rank ( F , F ) , N ) , N ) , or ( rank ( ts_mean ( vec_avg ( F ) , N ) ) N , rank ( F ) N ) )` | 13 | 5 | 8 | 3.68 | SHARPE | 54% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `divide ( F , add ( F , F ) )` | 25 | 0 | 0 | 0.64 | 2Y | 100% |
| `if_else ( greater ( ts_corr ( F , F , N ) , N ) , F , reverse ( F ) )` | 24 | 0 | 0 | 0.77 | 2Y | 100% |
| `group_neutralize ( subtract ( F , F ) , F )` | 16 | 0 | 0 | 0.24 | SHARPE | 100% |
| `divide ( subtract ( F , F ) , add ( abs ( F ) , abs ( F ) ) )` | 16 | 0 | 0 | 0.46 | SHARPE | 100% |
| `group_rank ( ts_decay_linear ( ts_backfill ( vec_avg ( F ) , N ) , N ) , F )` | 16 | 0 | 0 | 0.7 | 2Y | 100% |
| `divide ( subtract ( F , F ) , ts_std_dev ( subtract ( F , F ) , N ) )` | 16 | 0 | 0 | 0.99 | SHARPE | 100% |
| `group_rank ( subtract ( F , F ) , F )` | 13 | 0 | 0 | 0.39 | SHARPE | 92% |

## 待确认提案

- dead_families: 0
- dead_skeletons: 7
- wins: 0
- rules: 7（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `adbe6733-1f42b1f2` (n=3011)
- win 10.4% / near 23.1% / dead 65.6% / 最高|S| 7.45
- vs 上一版：win +10.4% / near +21.4% / dead -32.8%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


