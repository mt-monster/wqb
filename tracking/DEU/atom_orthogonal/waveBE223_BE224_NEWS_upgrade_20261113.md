# BE221/BE222 收割归因 + BE223/BE224 升级派发（2026-11-13）

## 一、BE221/BE222 失败归因（甄别批 1IPrC77k14PpaDc9oI7nK61 定案）

| 波 | 结果 | 根因 |
|---|---|---|
| BE221 news18 8臂 | 8/8 FAIL（无错误文本） | **平台瞬态**：甄别批同表达式 COMPLETE（BE75 先例同型）；重派 BE223 |
| BE222 news17 10臂 | 3 ERROR + 7 CANCELLED | **我的预检失误**：preflight 只传 dataset_id=news18，news17 字段未进 VECTOR 修复名单，multiply/subtract 内裸字段未包裹 → `Operator multiply/subtract does not support event inputs` + 整批连坐。**教训：混集表达式必须逐集跑 preflight（dataset_id 只认单集）** |

## 二、甄别批读数（4/4 COMPLETE）

| 臂 | 表达式 | id | S | 2Y | sub | TO | 定性 |
|---|---|---|---:|---:|---:|---:|---|
| 1 | news17 acb w22 subind（历史 T3 复刻） | zqdzeE0X | **0.94** | **1.22** | 0.28 | 11.6% | 最强；历史 0.84→0.94 漂移 +0.10 |
| 2 | news18 ssc w22 subind | O0WvgjVp | 0.12 | 0.16 | 0.31 | 10.7% | 弱 |
| 3 | news18 ssc bf126 sector | O0WvgjVR | 0.42 | −0.79 | 0.55 | 48.0% | 弱+TO 爆 |
| 4 | news17 ssc bf126 sector | 88NqXZYW | 0.05 | −0.01 | −0.39 | 33.1% | 死 |

⇒ **news17 的 acb（财报情绪）通道是 NEWS 面最强信号（0.94），落在升级带**；ssc 综合情绪双集皆弱。

## 三、BE224 派发：news17 acb 升级 8 臂（单数据集 ATOM）

基线 = zqdzeE0X（w22/subind/vec_avg, S 0.94）。升级维度：窗阶梯 / 聚合 / 轴 / 杠杆A / 同集双分类器 / relevance 加权 / 新颖度门控。

| # | 臂 | 表达式 |
|---|---|---|
| 1 | 窗 66 | `group_rank(ts_mean(vec_avg(nws17_multiple_comp_acb), 66), subindustry)` |
| 2 | 窗 126 | `group_rank(ts_mean(vec_avg(nws17_multiple_comp_acb), 126), subindustry)` |
| 3 | vec_sum（事件量加权） | `group_rank(ts_mean(vec_sum(nws17_multiple_comp_acb), 22), subindustry)` |
| 4 | industry 轴 | `group_rank(ts_mean(vec_avg(nws17_multiple_comp_acb), 22), industry)` |
| 5 | 杠杆A 双层中性化 | `group_zscore(group_neutralize(group_zscore(ts_mean(vec_avg(nws17_multiple_comp_acb), 22), sector), subindustry), sector)` |
| 6 | acb+bee 同集双分类器 | `group_rank(add(ts_mean(vec_avg(nws17_multiple_comp_acb), 22), ts_mean(vec_avg(nws17_multiple_comp_bee), 22)), subindustry)` |
| 7 | relevance 加权 | `group_rank(ts_mean(multiply(vec_avg(nws17_multiple_comp_acb), vec_avg(nws17_multiple_comp_relevance)), 22), subindustry)` |
| 8 | 新颖度门控 | `trade_when(less(vec_max(nws17_multiple_comp_event_similarity_days), 30), group_rank(ts_mean(vec_avg(nws17_multiple_comp_acb), 22), subindustry), -1)` |

## 四、BE223 派发：news18 机制矩阵重派 8 臂（BE221 修正版）

ssc 水平已被甄别批测死（0.12/0.42）⇒ 换未测机制 + acb 双胞胎迁移臂。

| # | 臂 | 表达式 |
|---|---|---|
| 1 | nip 尾部冲击 | `group_rank(ts_backfill(vec_max(nws18_multiple_comp_nip), 126), sector)` |
| 2 | 事件量反转 | `-group_rank(ts_backfill(vec_sum(multi_entity_story_event_count), 126), sector)` |
| 3 | ssc-sse 分歧 | `group_rank(ts_backfill(vec_sum(subtract(vec_avg(nws18_multiple_comp_ssc), vec_avg(nws18_multiple_comp_sse))), 126), sector)` |
| 4 | 新颖度门控 | `trade_when(vec_max(nws18_mltpl_cmp_event_simildays) < 30, group_rank(ts_backfill(vec_avg(nws18_multiple_comp_ssc), 126), sector), -1)` |
| 5 | 情绪动量 | `group_rank(ts_delta(ts_backfill(vec_sum(nws18_multiple_comp_ssc), 126), 22), sector)` |
| 6 | 杠杆A | `group_zscore(group_neutralize(group_zscore(ts_backfill(vec_avg(nws18_multiple_comp_ssc), 126), sector), subindustry), sector)` |
| 7 | relevance 加权 | `group_rank(ts_backfill(vec_sum(multiply(vec_avg(nws18_multiple_comp_ssc), vec_avg(nws18_multiple_comp_relevance))), 126), sector)` |
| 8 | acb 迁移臂（news17 最强机制跨集验证） | `group_rank(ts_mean(vec_avg(nws18_multiple_comp_acb), 22), subindustry)` |

设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON/maxTrade OFF；并发 2 multisim。
