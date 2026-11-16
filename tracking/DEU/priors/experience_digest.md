<!-- BEGIN WQB EXPERIENCE DIGEST -->
# DEU 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:03
- 样本：12433 条 `attempt_knowledge`
- 知识版本（top3）：`3e795546-ef921fb7` n=12425, `d0569692-ef921fb7` n=8

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `group_rank ( ts_target_tvr_decay ( multiply ( rank ( ts_delta ( ts_backfill ( vec_avg ( F ) , N ) , N ) ) , rank ( ts_delta ( ts_backfill ( vec_avg ( F ) , N ) , N ) ) ) , F N ) , F )` | 252 | 25 | 125 | 1.85 | SHARPE | 88% |
| `multiply ( multiply ( group_rank ( ts_mean ( F , N ) , F ) , group_rank ( ts_mean ( F , N ) , F ) ) , group_rank ( ts_mean ( F , N ) , F ) )` | 86 | 18 | 66 | 2.12 | 2Y | 79% |
| `group_rank ( add ( ts_zscore ( F , N ) , ts_zscore ( subtract ( F , F ) , N ) ) , F )` | 60 | 15 | 36 | 2.19 | 2Y | 72% |
| `multiply ( multiply ( group_rank ( ts_mean ( F , N ) , F ) , group_rank ( ts_mean ( F , N ) , F ) ) , group_rank ( ts_sum ( F , N ) , F ) )` | 51 | 12 | 39 | 1.8 | SHARPE | 67% |
| `group_neutralize ( rank ( add ( ts_mean ( ts_backfill ( F , N ) , N ) , ts_mean ( ts_backfill ( F , N ) , N ) ) ) , bucket ( rank ( ts_mean ( ts_backfill ( F , N ) , N ) ) , F N , N , N ) )` | 124 | 11 | 71 | 1.67 | 2Y | 48% |
| `multiply ( group_rank ( ts_mean ( F , N ) , F ) , group_rank ( ts_mean ( F , N ) , F ) )` | 122 | 9 | 109 | 2.09 | 2Y | 93% |
| `group_rank ( F , F )` | 185 | 8 | 52 | 2.7 | 2Y | 90% |
| `group_neutralize ( ts_decay_linear ( subtract ( rank ( add ( ts_mean ( ts_backfill ( F , N ) , N ) , ts_mean ( ts_backfill ( F , N ) , N ) ) ) , rank ( group_mean ( add ( ts_mean ( ts_backfill ( F , N ) , N ) , ts_mean ( ts_backfill ( F , N ) , N ) ) , N , F ) ) ) , N ) , bucket ( rank ( ts_mean ( ts_backfill ( F , N ) , N ) ) , F N , N , N ) )` | 104 | 3 | 80 | 1.7 | 2Y | 95% |
| `group_zscore ( add ( group_rank ( ts_delta ( ts_backfill ( vec_avg ( F ) , N ) , N ) , F ) , group_rank ( ts_rank ( ts_backfill ( vec_avg ( F ) , N ) , N ) , F ) ) , F )` | 51 | 3 | 37 | 1.91 | SHARPE | 84% |
| `group_rank ( multiply ( multiply ( rank ( ts_delta ( F , N ) ) , rank ( ts_delta ( F , N ) ) ) , rank ( ts_rank ( F , N ) ) ) , F )` | 55 | 3 | 35 | 1.79 | SHARPE | 93% |

## 统计死路（advisory，不是硬禁；top 10）

（暂无）

## 待确认提案

- dead_families: 0
- dead_skeletons: 0
- wins: 0
- rules: 0（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `3e795546-ef921fb7` (n=12425)
- win 3.5% / near 32.2% / dead 64.3% / 最高|S| 11.71
- vs 上一版：win +3.5% / near +32.2% / dead -35.7%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


