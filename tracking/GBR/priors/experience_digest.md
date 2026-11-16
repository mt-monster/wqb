<!-- BEGIN WQB EXPERIENCE DIGEST -->
# GBR 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:08
- 样本：9835 条 `attempt_knowledge`
- 知识版本（top3）：`65c5fb69-94985c02` n=9549, `e153ce42-94985c02` n=77, `f6057f1e-94985c02` n=72

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `add ( group_rank ( ts_zscore ( F , N ) , F ) , reverse ( group_rank ( ts_zscore ( ts_backfill ( vec_sum ( F ) , N ) , N ) , F ) ) )` | 98 | 74 | 19 | 3.07 | UNKNOWN | 40% |
| `rank ( ts_quantile ( ts_av_diff ( divide ( F , F ) , N ) , N , F F ) )` | 85 | 31 | 34 | 2.51 | 2Y | 53% |
| `group_rank ( ts_target_tvr_decay ( winsorize ( rank ( group_neutralize ( add ( ts_mean ( ts_backfill ( F , N ) , N ) , ts_mean ( ts_backfill ( F , N ) , N ) ) , F ) ) , F N ) , F N , F N , F N ) , F )` | 199 | 11 | 125 | 2.63 | FITNESS | 44% |
| `ts_target_tvr_decay ( group_neutralize ( ts_rank ( ts_mean ( vec_sum ( F ) , N ) , N ) , densify ( F ) ) , F N , F N , F N )` | 38 | 10 | 13 | 2.21 | FITNESS | 74% |
| `group_rank ( ts_av_diff ( ts_backfill ( F , N ) , N ) , F )` | 96 | 9 | 52 | 3.09 | 2Y | 68% |
| `group_rank ( ts_zscore ( F , N ) , F )` | 82 | 7 | 22 | 3.09 | 2Y | 78% |
| `group_rank ( ts_target_tvr_decay ( rank ( ts_delta ( ts_backfill ( F , N ) , N ) ) , F N , F N , F N ) , F )` | 347 | 0 | 171 | 1.97 | 2Y | 1% |
| `winsorize ( signed_power ( ts_quantile ( F , N ) , N ) , F N )` | 100 | 0 | 99 | 1.97 | FITNESS | 14% |
| `group_rank ( ts_target_tvr_decay ( winsorize ( rank ( group_neutralize ( divide ( ts_backfill ( vec_max ( F ) , N ) , add ( ts_backfill ( vec_max ( F ) , N ) , ts_backfill ( vec_max ( F ) , N ) ) ) , F ) ) , F N ) , F N , F N , F N ) , F )` | 80 | 0 | 72 | 1.59 | 2Y | 1% |
| `group_rank ( ts_target_tvr_decay ( winsorize ( rank ( group_neutralize ( divide ( ts_backfill ( vec_avg ( F ) , N ) , add ( ts_backfill ( vec_avg ( F ) , N ) , ts_backfill ( vec_avg ( F ) , N ) ) ) , F ) ) , F N ) , F N , F N , F N ) , F )` | 93 | 0 | 67 | 1.57 | - | 0% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `group_rank ( ts_mean ( F , N ) , F )` | 69 | 0 | 0 | 0.96 | 2Y | 99% |
| `group_rank ( ts_zscore ( vec_avg ( F ) , N ) , F )` | 64 | 0 | 0 | 0.99 | FITNESS | 98% |
| `rank ( ts_mean ( ts_backfill ( vec_avg ( F ) , N ) , N ) )` | 44 | 0 | 0 | 0.86 | 2Y | 100% |
| `group_rank ( ts_target_tvr_decay ( winsorize ( rank ( group_neutralize ( add ( ts_mean ( ts_backfill ( vec_avg ( F ) , N ) , N ) , ts_mean ( ts_backfill ( vec_avg ( F ) , N ) , N ) ) , F ) ) , F N ) , F N , F N , F N ) , F )` | 41 | 0 | 0 | 0.8 | FITNESS | 90% |

## 待确认提案

- dead_families: 1
- dead_skeletons: 4
- wins: 0
- rules: 5（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `65c5fb69-94985c02` (n=9549)
- win 5.0% / near 34.2% / dead 60.8% / 最高|S| 11.18
- vs 上一版：win +5.0% / near +28.9% / dead -34.0%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


