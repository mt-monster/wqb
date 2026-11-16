<!-- BEGIN WQB EXPERIENCE DIGEST -->
# ASI 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:21
- 样本：1543 条 `attempt_knowledge`
- 知识版本（top3）：`06d2b519-4335499a` n=1438, `c5ff1b24-4335499a` n=72, `ed0eb4e2-4335499a` n=24

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `multiply ( N , group_rank ( ts_rank ( F , N ) , F ) )` | 42 | 13 | 21 | 4.02 | FITNESS | 60% |
| `trade_when ( less ( days_from_last_change ( F ) , N ) , ts_decay_linear ( group_rank ( ts_rank ( ts_mean ( F , N ) , N ) , F ) , N ) , N )` | 26 | 4 | 9 | 2.3 | SHARPE | 77% |
| `rank ( ts_delta ( ts_zscore ( divide ( F , F ) , N ) , N ) )` | 10 | 3 | 6 | 2.29 | SHARPE | 70% |
| `group_rank ( ts_rank ( F , N ) , F )` | 51 | 2 | 47 | 4.82 | UNKNOWN | 82% |
| `group_rank ( vec_avg ( F ) , group_cartesian_product ( bucket ( zscore ( F ) , F N , N , N ) , bucket ( zscore ( F ) , F N , N , N ) ) )` | 52 | 2 | 5 | 2.06 | SHARPE | 13% |
| `multiply ( N , group_rank ( F , F ) )` | 21 | 1 | 5 | 2.84 | SHARPE | 95% |
| `rank ( ts_decay_linear ( ts_delta ( ts_zscore ( divide ( F , F ) , N ) , N ) , N ) )` | 8 | 1 | 0 | 2.27 | FITNESS | 88% |
| `trade_when ( rank ( divide ( F , ts_mean ( F , N ) ) ) N , signed_power ( subtract ( N , group_rank ( ts_decay_linear ( F , N ) , F ) ) , N ) , rank ( divide ( F , ts_mean ( F , N ) ) ) N )` | 44 | 0 | 44 | 2.76 | SHARPE | 100% |
| `group_zscore ( ts_decay_linear ( F , N ) , F )` | 42 | 0 | 38 | 3.11 | SHARPE | 100% |
| `signed_power ( subtract ( N , group_rank ( ts_decay_linear ( F , N ) , F ) ) , N )` | 39 | 0 | 37 | 2.4 | SHARPE | 64% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `group_rank ( ts_delta ( vec_avg ( F ) , N ) , F )` | 19 | 0 | 0 | 0.86 | 2Y | 100% |
| `group_rank ( vec_avg ( F ) , F )` | 15 | 0 | 0 | 0.87 | 2Y | 87% |
| `divide ( F , F )` | 13 | 0 | 0 | 0.7 | 2Y | 100% |
| `rank ( F )` | 10 | 0 | 0 | 0.75 | FITNESS | 100% |

## 待确认提案

- dead_families: 0
- dead_skeletons: 4
- wins: 0
- rules: 4（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `06d2b519-4335499a` (n=1438)
- win 3.1% / near 48.3% / dead 45.3% / 最高|S| 5.75
- vs 上一版：win +3.1% / near +48.3% / dead -54.7%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


