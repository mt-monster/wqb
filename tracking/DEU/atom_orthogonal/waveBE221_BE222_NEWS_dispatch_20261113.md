# BE221/BE222 派发：NEWS 塔首攻探针（news18 + news17，2026-11-13）

> S0/S1 产物：候选清单 [S0_DATASET_SCAN_20261113.md](S0_DATASET_SCAN_20261113.md) ｜ 字段画像 [FIELD_PROFILE_NEWS17_NEWS18_20261113.md](FIELD_PROFILE_NEWS17_NEWS18_20261113.md)
> 任务：DEU 20 颗（17 在篮 + 缺口 3）；NEWS 塔判死已撤回后的正当开矿。
> 并发 = 2 multisim（用户约束）。

## 派发记录

| 波 | 数据集 | multisim id | 臂数 | 设置 |
|---|---|---|---:|---|
| BE221 | news18（multi_entity 档 cov 0.9788） | `3os2rYftY4NOahq1bbmp4UKN` | 8 | DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON/maxTrade OFF |
| BE222 | news17（multiple_comp 档 cov 0.9323） | `3jdCvT7cs4UK942xM4nCSp1` | 10 | 同上 |

## BE221 八臂（news18）

| # | 机制 | 表达式 |
|---|---|---|
| 1 | M2 情绪水平对照 | `group_rank(ts_backfill(vec_avg(nws18_multiple_comp_ssc), 126), sector)` |
| 2 | M1 relevance 加权 | `group_rank(ts_backfill(vec_sum(multiply(vec_avg(ssc), vec_avg(relevance))), 126), sector)` |
| 3 | M5 nip 尾部冲击 | `group_rank(ts_backfill(vec_max(nws18_multiple_comp_nip), 126), sector)` |
| 4 | M4 事件量反转 | `-group_rank(ts_backfill(vec_sum(multi_entity_story_event_count), 126), sector)` |
| 5 | M6 ssc-sse 分歧 | `group_rank(ts_backfill(vec_sum(subtract(vec_avg(ssc), vec_avg(sse))), 126), sector)` |
| 6 | M3 新颖度门控 | `trade_when(vec_max(simildays) < 30, M2 信号, -1)` |
| 7 | M9 情绪动量 | `group_rank(ts_delta(ts_backfill(vec_sum(ssc), 126), 22), sector)` |
| 8 | M7 双层中性化（杠杆A） | `group_zscore(group_neutralize(group_zscore(bf(vec_avg(ssc),126), sector), subindustry), sector)` |

## BE222 十臂（news17）

同机制矩阵 + acb 盈利通道 + spread(ssc−event_sentiment) + nip×relevance 交互。

## 判读预案

- 任一臂 S≥1.58 且 2Y≥1.58 → 全闸验证 + 与 17 颗篮互相关
- S 1.0-1.58 → 升级窗（66/126/252 阶梯）/ 轴 / 聚合算子（vec_max>vec_avg 实证）
- 双结构全 <0.5 → 转候选 #3/#4（model238/model36）
- VECTOR 聚合纪律已过 preflight（相乘字段逐个 vec_avg 包裹）；ber/ghc_lna 分析师通道首波刻意不派（篮内 ANALYST 相关性风险）
