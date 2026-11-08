# 应急模板池 · other553（仅 Wave1 forum 全灭后启用）

> category=sentiment，塔 0/3，乘数 1.6。字段实为分析师估计/目标价/推荐意见挖掘，非股吧流量。
> 全部 VECTOR → vec_avg。窗口 5/22/66。算子 ≤12。

| ID | 机制 | 骨架 |
|---|---|---|
| C01 | 估计值水平 | `subtract(0.5, group_rank(ts_mean(vec_avg(oth553_est_estvalue), 22), sector))` |
| C02 | 估计变化 | `subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(oth553_est_estvalue), 22), 5), sector))` |
| C03 | 分析师覆盖广度 | `subtract(0.5, group_rank(ts_mean(vec_avg(oth553_est_analyst), 22), sector))` |
| C04 | 目标价水平 | `subtract(0.5, group_rank(ts_mean(vec_avg(oth553_ptgvalue), 22), sector))` |
| C05 | 目标价变化 | `subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(oth553_ptgvalue), 22), 5), sector))` |
| C06 | 推荐值 | `subtract(0.5, group_rank(ts_mean(vec_avg(oth553_recvalue), 22), sector))` |
| C07 | 推荐变化 | `subtract(0.5, group_rank(ts_mean(ts_delta(vec_avg(oth553_recvalue), 22), 5), sector))` |
| C08 | 销售估计 | `subtract(0.5, group_rank(ts_mean(vec_avg(oth553_sal_estvalue), 22), sector))` |
| C09 | 估计-前值价差 | `group_rank(ts_mean(subtract(vec_avg(oth553_est_estvalue), vec_avg(oth553_est_preestvalue)), 22), sector)` |
| C10 | 发言活跃 | `subtract(0.5, group_rank(ts_mean(vec_avg(oth553_est_yearspeakcnt), 66), sector))` |

## 启用条件
- Wave1 equity_forum_data max|S|<0.5 且 Wave1b 无可用信号
- 切换原因写入 waves：严格 Social Media 不可用 + forum social-adjacent 全灭
