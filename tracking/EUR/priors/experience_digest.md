<!-- BEGIN WQB EXPERIENCE DIGEST -->
# EUR 经验摘要（自动生成）

- generated_at: 2026-11-15T16:03:11
- 样本：6029 条 `attempt_knowledge`
- 知识版本（top3）：`0cd8a385-088149f5` n=5774, `dda432d7-088149f5` n=158, `6c1c896e-088149f5` n=39

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `group_neutralize ( add ( signed_power ( group_zscore ( divide ( subtract ( F , F ) , F ) , F ) , N ) , multiply ( N , subtract ( group_rank ( ts_zscore ( ts_backfill ( divide ( subtract ( F , F ) , F ) , N ) , N ) , F ) , N ) ) ) , F )` | 68 | 26 | 40 | 2.24 | 2Y | 51% |
| `group_rank ( add ( group_rank ( subtract ( F , F ) , F ) , group_rank ( divide ( F , ts_mean ( F , N ) ) , F ) ) , F )` | 54 | 25 | 24 | 4.26 | UNKNOWN | 74% |
| `group_neutralize ( signed_power ( group_zscore ( divide ( subtract ( F , F ) , F ) , F ) , N ) , F )` | 135 | 21 | 87 | 2.31 | 2Y | 66% |
| `group_rank ( add ( group_rank ( subtract ( F , F ) , F ) , group_rank ( ts_backfill ( F , N ) , F ) ) , F )` | 27 | 17 | 7 | 4.06 | UNKNOWN | 63% |
| `group_neutralize ( group_scale ( add ( signed_power ( rank ( ts_backfill ( F , N ) ) , N ) , multiply ( N , signed_power ( rank ( ts_backfill ( F , N ) ) , N ) ) ) , F ) , F )` | 24 | 16 | 7 | 2.74 | FITNESS | 33% |
| `ts_target_tvr_decay ( trade_when ( greater ( vec_avg ( F ) , vec_avg ( F ) ) , group_zscore ( divide ( vec_avg ( F ) , vec_avg ( F ) ) , F ) , N ) , F N , F N , F N )` | 58 | 12 | 26 | 1.75 | SHARPE | 66% |
| `group_rank ( subtract ( F , F ) , F )` | 55 | 10 | 9 | 4.84 | 2Y | 67% |
| `trade_when ( less ( group_rank ( ts_mean ( ts_backfill ( F , N ) , N ) , F ) , N ) , group_neutralize ( group_scale ( signed_power ( group_zscore ( divide ( F , add ( F , F ) ) , F ) , N ) , F ) , F ) , N )` | 27 | 8 | 18 | 2.8 | SUB | 48% |
| `vector_neut ( vector_neut ( reverse ( rank ( divide ( F , F ) ) ) , rank ( divide ( F , F ) ) ) , rank ( divide ( F , F ) ) )` | 27 | 8 | 9 | 1.76 | SHARPE | 70% |
| `group_neutralize ( group_scale ( add ( signed_power ( group_zscore ( divide ( subtract ( F , F ) , F ) , F ) , N ) , multiply ( N , group_rank ( F , F ) ) ) , F ) , F )` | 28 | 7 | 18 | 2.28 | 2Y | 64% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `group_rank ( ts_mean ( vec_avg ( F ) , N ) , F )` | 36 | 0 | 0 | 0.87 | FITNESS | 97% |
| `multiply ( N , group_zscore ( ts_delta ( F , N ) , F ) )` | 29 | 0 | 0 | 0.57 | 2Y | 100% |
| `group_rank ( ts_zscore ( vec_avg ( F ) , N ) , F )` | 25 | 0 | 0 | 0.76 | 2Y | 100% |
| `group_rank ( vec_avg ( F ) , F )` | 23 | 0 | 0 | 0.6 | 2Y | 100% |

## 待确认提案

- dead_families: 3
- dead_skeletons: 4
- wins: 5
- rules: 7（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `0cd8a385-088149f5` (n=5774)
- win 8.7% / near 36.5% / dead 54.3% / 最高|S| 6.54
- vs 上一版：win +8.7% / near +36.5% / dead -45.7%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


