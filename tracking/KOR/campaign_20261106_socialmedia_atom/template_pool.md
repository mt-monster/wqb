# 模板池 · KOR Social-adjacent / equity_forum_data（≥10 结构互异）

> 来源标注：FM=论坛 / PP=论文 / SB=自建。差异落在骨架/算子几何/矩/分组轴/非线性，不只换窗口。
> 主字段均来自 equity_forum_data（VECTOR）。窗口只用 5/22/66/252。算子数上限 12、越少越好。
> ⚠ USA OTHER 池复盘称 equity_forum_data 为 virgin 靶仍死于「低竞争≠有信号」——KOR 须实测，不得照搬判死。

| ID | 机制 | 骨架（占位） | 结构差异点 | 来源 |
|---|---|---|---|---|
| T01 | M1 注意力反转·水平 | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), sector))` | 水平矩 + sector 分组 | PP Da-Engelberg-Gao + SB |
| T02 | M1 注意力·变化率 | `subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(aggregate_comment_volume), 22), 5), sector))` | 一阶差分矩 | SB + 铁律 A 变体 |
| T03 | M1 注意力·波动/分歧 | `subtract(0.5, group_rank(ts_mean(vec_stddev(aggregate_comment_volume), 22), sector))` | 二阶矩 VECTOR 内分歧 | SB（对标 insiders M1） |
| T04 | M2 卖意见强度 | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_sell_opinion_score), 22), sector))` | 换信号腿·卖意见 | PP Antweiler-Frank + SB |
| T05 | M2 买意见强度 | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_buy_opinion_score), 22), sector))` | 换信号腿·买意见 | 同上 |
| T06 | M2 净意见价差 | `group_rank(ts_mean(subtract(vec_avg(aggregate_buy_opinion_score), vec_avg(aggregate_sell_opinion_score)), 22), sector)` | 同源价差（合规，非等权相加） | FM net_buy 驯服帖思路 + SB |
| T07 | M3 买卖意见分歧 | `subtract(0.5, group_rank(ts_mean(abs(subtract(vec_avg(aggregate_buy_opinion_score), vec_avg(aggregate_sell_opinion_score))), 22), sector))` | 绝对价差=分歧 | PP Miller + SB |
| T08 | M4 参与广度 | `subtract(0.5, group_rank(ts_mean(vec_avg(total_distinct_participants_count), 22), sector))` | 广度轴·独立用户 | SB |
| T09 | M4 分平台用户白空间 | `subtract(0.5, group_rank(ts_mean(vec_avg(distinct_user_count_per_platform), 22), sector))` | aC=0 白字段 | SB |
| T10 | 非线性倒数破壁 | `subtract(0.5, group_rank(ts_mean(divide(1, add(vec_avg(aggregate_comment_volume), 1)), 22), sector))` | 单调非线性（eps 按量纲试） | SB（KOR 倒数破 S 墙实证） |
| T11 | 分组轴换 industry | `subtract(0.5, group_rank(ts_mean(vec_avg(aggregate_comment_volume), 22), industry))` | 分组轴差异 | SB |
| T12 | 时序分位拥挤 | `subtract(0.5, ts_rank(vec_avg(aggregate_comment_volume), 66))` | 自身历史分位（无截面 group） | SB |

## 辅助轴（不单独成模板，作破闸壳）
- 内层 ts_mean(5/22) 专治 2Y；正反两臂各测（铁律 B）。
- 论坛帖：散户日度计数高换手 → 先时序聚合再 rank，勿只加 decay（FM YQ11169 net_buy 驯服）。
- 禁：winsorize 放 group_rank 前；禁跨字段等权 add；禁 PV/MODEL/OTHER/FUNDAMENTAL 混腿（本集已是 OTHER 单塔 ATOM）。

## 多样性自检
- 12 个模板；经济机制 ≥4（注意力/意见强度/净价差/广度）；矩含水平·差分·二阶·分位；分组含 sector/industry/无分组；含非线性。
- socialmedia39 对照探针另列，不计入本池交付主轴。
