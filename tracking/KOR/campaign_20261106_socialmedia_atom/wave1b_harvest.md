# Wave1b socialmedia39 收割（2026-11-06）

- multisim: `3M3PjSdj14pubj91Mn22kaA`
- 状态：COMPLETE · 2/2 · error_count=0
- 用途：严格 Social Media 负对照（共搜 ticker ID 向量）

## 指标

| alpha_id | 几何 | S | 2Y | Fitness | TO | fail_ra | 判定 |
|---|---|---:|---:|---:|---:|---:|---|
| Vkxm2zGY | vec_count | -0.66 | -0.66 | -0.41 | 0.1377 | 5 | REJECT（反向死） |
| leA5QGWA | vec_avg | 0.94 | 1.44 | 0.54 | 0.0685 | 3 | REJECT（S/2Y 未达 1.58） |

## 归因要点
- ID 向量对照未出货：不进入主交付。
- vec_avg 臂 S0.94/2Y1.44 高于 vec_count 负臂，但仍远低于 REGULAR 线；决策树「scl39 出奇强」分支未触发。
- 主战场仍看 Wave1 `equity_forum_data`（在飞）。

## 表达式
```
Vkxm2zGY: subtract(0.5, group_rank(ts_mean(vec_count(scl39_top5_people_also_watch_ticker_ii), 22), sector))
leA5QGWA: subtract(0.5, group_rank(ts_mean(vec_avg(scl39_top5_people_also_watch_ticker_ii), 22), sector))
```
