<!-- BEGIN WQB EXPERIENCE DIGEST -->
# KOR 经验摘要（自动生成）

- generated_at: 2026-11-15T16:02:57
- 样本：3764 条 `attempt_knowledge`
- 知识版本（top3）：`214b3c11-43199e76` n=3496, `7647a12f-43199e76` n=250, `f7870609-43199e76` n=10

## 有效骨架（win+near，top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `subtract ( N , group_rank ( ts_mean ( vec_stddev ( F ) , N ) , F ) )` | 82 | 21 | 32 | 2.01 | SHARPE | 73% |
| `subtract ( N , group_rank ( ts_mean ( F , N ) , F ) )` | 62 | 18 | 13 | 2.12 | SHARPE | 69% |
| `ts_target_tvr_decay ( signed_power ( group_rank ( winsorize ( vector_neut ( rank ( ts_backfill ( F , N ) ) , rank ( ts_backfill ( F , N ) ) ) , F N ) , F ) , N ) , F N )` | 99 | 17 | 37 | 1.68 | SHARPE | 79% |
| `group_neutralize ( multiply ( group_rank ( ts_av_diff ( F , N ) , F ) , group_rank ( ts_av_diff ( F , N ) , F ) ) , F )` | 94 | 16 | 71 | 1.97 | 2Y | 72% |
| `multiply ( group_rank ( ts_delta ( F , N ) , F ) , group_rank ( ts_mean ( F , N ) , F ) )` | 21 | 14 | 5 | 1.89 | UNKNOWN | 67% |
| `group_neutralize ( multiply ( group_rank ( ts_rank ( F , N ) , F ) , group_rank ( ts_rank ( F , N ) , F ) ) , F )` | 26 | 12 | 14 | 2.03 | 2Y | 54% |
| `subtract ( group_rank ( ts_mean ( divide ( N , add ( vec_stddev ( F ) , N ) ) , N ) , F ) , N )` | 18 | 6 | 11 | 1.7 | SHARPE | 67% |
| `quantile ( group_rank ( ts_rank ( group_rank ( divide ( F , F ) , F ) , N ) , F ) )` | 38 | 5 | 22 | 2.12 | 2Y | 79% |
| `quantile ( group_rank ( ts_backfill ( ts_rank ( subtract ( F , F ) , N ) , N ) , F ) )` | 20 | 5 | 10 | 2.88 | SHARPE | 70% |
| `hump ( subtract ( group_rank ( ts_av_diff ( F , N ) , F ) , group_rank ( ts_mean ( vec_stddev ( F ) , N ) , F ) ) , F N )` | 15 | 4 | 10 | 1.92 | SHARPE | 53% |

## 统计死路（advisory，不是硬禁；top 10）

| 名称 | n | win | near | 最高\|S\| | 主墙 | 占比 |
|---|---:|---:|---:|---:|---|---:|
| `trade_when ( ts_arg_max ( F , N ) N , signed_power ( ts_quantile ( divide ( subtract ( F , F ) , ts_mean ( F , N ) ) , N , F F ) , N ) , N )` | 19 | 0 | 0 | 0.92 | FITNESS | 100% |

## 待确认提案

- dead_families: 0
- dead_skeletons: 1
- wins: 0
- rules: 1（proposed 不生效；满 2 个独立波次确认后才转 active）

## 最新知识版本产出率

- knowledge_version: `214b3c11-43199e76` (n=3496)
- win 8.0% / near 32.2% / dead 59.8% / 最高|S| 5.96
- vs 上一版：win +8.0% / near +32.2% / dead -40.2%

> 判死仍走 `forum_recon` + `seal_dead_end`；本摘要只提供统计与提案，不自动封存。
<!-- END WQB EXPERIENCE DIGEST -->


