# Wave1 计划 · equity_forum_data（待用户显式确认后才派发）

> 状态：**READY / 未派发**。问卷超时自动选了 forum_first；本文件不构成发仿真授权。
> 设置档：KOR / TOP600 / D1；decay=4；truncation=0.08；nanHandling=OFF；pasteurization=ON；maxTrade=OFF。
> 中性化：批 A = STATISTICAL（区域默认）；若批 A 有活苗再开批 B = REVERSION_AND_MOMENTUM（铁律：换壳重扫中性化）。
> 并发：create_multi_simulation 任务并发 ≤2（goal 约束）。

## 准入 / 继承 / 收窄
- 继承：S0 严格 Social Media 字段=ID 向量不可用 → 扩到 social-adjacent forum；USA virgin 死靶风险 → Wave1 小批快判。
- 准入：仅 equity_forum_data 单集 ATOM；禁混信号；算子≤12。
- 收窄：从 12 模板收成 8 条探针（T01–T06 + T01 反臂 + T08）。

## 探针列表

| tag | 模板 | 表达式 |
|---|---|---|
| T01_attn_lvl | T01_attn_lvl | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), sector))` |
| T02_attn_delta | T02_attn_delta | `subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(aggregate_comment_volume), 22), 5), sector))` |
| T03_attn_std | T03_attn_std | `subtract(0.5, group_rank(ts_mean(vec_stddev(aggregate_comment_volume), 22), sector))` |
| T04_sell | T04_sell | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_sell_opinion_score), 22), sector))` |
| T05_buy | T05_buy | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_buy_opinion_score), 22), sector))` |
| T06_net | T06_net | `group_rank(ts_mean(subtract(vec_avg(aggregate_buy_opinion_score), vec_avg(aggregate_sell_opinion_score)), 22), sector)` |
| T01_rev | T01_rev | `subtract(group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), sector), 0.5)` |
| T08_breadth | T08_breadth | `subtract(0.5, group_rank(ts_mean(vec_avg(total_distinct_participants_count), 22), sector))` |

## 批 B 预案（REVERSION_AND_MOMENTUM，仅在批 A 有活苗或批 A 全灭需换中性化档时发）

| tag | 表达式 |
|---|---|
| B_T01 | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), sector))` |
| B_T04 | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_sell_opinion_score), 22), sector))` |
| B_T05 | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_buy_opinion_score), 22), sector))` |
| B_T06 | `group_rank(ts_mean(subtract(vec_avg(aggregate_buy_opinion_score), vec_avg(aggregate_sell_opinion_score)), 22), sector)` |
| B_T08 | `subtract(0.5, group_rank(ts_mean(vec_avg(total_distinct_participants_count), 22), sector))` |
| B_T10 | `subtract(0.5, group_rank(ts_mean(divide(1, add(vec_avg(aggregate_comment_volume), 1)), 22), sector))` |
| B_T11 | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), industry))` |
| B_T12 | `subtract(0.5, ts_rank(vec_avg(aggregate_comment_volume), 66))` |

批 B preflight：见本轮记录（应 valid）。

## 判读门槛（快判死）
- 8 条 max|S| < 0.5 → 机制性弱，停扫同族参数，换机制或换集。
- 仅单年尖峰 → 过拟合指纹，换机制。
- 有 S≥1.0 活苗 → 归因后收窄发 Wave2（候选数 ≤ Wave1 的 1/3）。
