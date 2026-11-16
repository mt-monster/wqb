<!-- BEGIN WQB EXPERIENCE DIGEST -->
# JPN 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:26
- 样本：254 条 `attempt_knowledge`
- 知识版本（top3）：`edbe1c01-7bcfd7a9` n=214, `40533689-7bcfd7a9` n=40

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `rank ( ts_mean ( F , N ) )` | 15 | 0 | 1 | 1.02 | 2Y | 93% |
| `ts_zscore ( F , N )` | 12 | 0 | 1 | 1.41 | SHARPE | 100% |
| `divide ( subtract ( max ( F , F , F ) , min ( F , F , F ) ) , add ( abs ( F ) , abs ( F ) ) )` | 2 | 0 | 1 | 1.24 | 2Y | 50% |
| `rank ( ts_decay_linear ( ts_backfill ( F , N ) , N ) )` | 2 | 0 | 1 | 1.03 | 2Y | 50% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `rank ( ts_backfill ( F , N ) )` | 12 | 0 | 0 | 0.9 | 2Y | 100% |
| `divide ( subtract ( F , F ) , add ( abs ( F ) , abs ( F ) ) )` | 8 | 0 | 0 | 0.86 | 2Y | 100% |
| `divide ( F , F )` | 7 | 0 | 0 | 0.67 | FITNESS | 100% |
| `vector_neut ( F , F )` | 6 | 0 | 0 | 0.63 | 2Y | 100% |
| `ts_corr ( F , F , N )` | 6 | 0 | 0 | 0.69 | 2Y | 100% |
| `subtract ( F , F )` | 5 | 0 | 0 | 0.41 | 2Y | 100% |
| `rank ( ts_ir ( F , N ) )` | 4 | 0 | 0 | 0.58 | 2Y | 100% |
| `rank ( F )` | 4 | 0 | 0 | 0.86 | 2Y | 100% |
| `divide ( ts_delta ( F , N ) , ts_std_dev ( F , N ) )` | 3 | 0 | 0 | 0.45 | 2Y | 100% |
| `rank ( ts_quantile ( F , N , F F ) )` | 3 | 0 | 0 | 0.54 | 2Y | 100% |

## 待确认提案

- dead_families: 0
- dead_skeletons: 12
- wins: 0
- rules: 12（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `40533689-7bcfd7a9` (n=40)
- win 0.0% / near 2.5% / dead 97.5% / 最高|S| 1.41
- vs 上一版：win +0.0% / near +1.1% / dead -1.1%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


