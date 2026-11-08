# S1 字段画像 · equity_forum_data（KOR / TOP600 / D1）

> 画像日期：2026-11-06。数据源：MCP get_datafields(filter_sharpe=false) 实测 6/6（platform_count=6 / complete=true）。
> 塔归属：other（KOR/D1/OTHER 1/3 未点亮，乘数 1.6）。
> 警告：本集 category=other，语义为股吧/论坛活跃与买卖意见，作为 Social Media social-adjacent 主战场（严格 Social Media 仅 1 字段 ID 向量不可连续定价）。本决议来自问卷超时自动推荐，用户可改。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset id | equity_forum_data |
| name | International Equity Forum Activity |
| category | other（非 socialmedia 字面，但是论坛活动） |
| 字段数 | 6，全部 VECTOR（须 vec_* 降维） |
| 覆盖率 | 0.8948（6 字段同值） |
| 拥挤度 | 极低：单字段 aC 0–7（最高 aggregate_sell_opinion_score=7） |
| 本质 | 多源股吧/论坛的 买卖意见分 + 评论量 + 参与人数 |

## 1. 字段全表（以 description 为准）

| 字段 | type | cov | aC | uC | 语义族 | 可用性 |
|---|---|---:|---:|---:|---|---|
| aggregate_buy_opinion_score | VECTOR | .8948 | 5 | 4 | A 意见强度·买 | 信号腿候选 |
| aggregate_sell_opinion_score | VECTOR | .8948 | 7 | 5 | A 意见强度·卖 | 信号腿候选 |
| aggregate_comment_volume | VECTOR | .8948 | 3 | 3 | B 注意力·总量 | 信号腿候选 |
| comment_volume_per_platform | VECTOR | .8948 | 3 | 3 | B 注意力·分平台 | 辅助/对照 |
| total_distinct_participants_count | VECTOR | .8948 | 1 | 1 | C 参与广度 | 信号腿候选 |
| distinct_user_count_per_platform | VECTOR | .8948 | 0 | 0 | C 参与广度·分平台 | 最白空间 |

## 2. 五问 + 预处理

1. 时间维度：意见分/评论量 = 流量型水平（非存量会计），可水平用，也可 ts_delta 看变化。
2. 相对性：截面排序差异（group_rank / rank），行业内更稳。
3. 被定价的是谁：零售注意力/散户买卖意见；广度（参与人数）vs 强度（意见分）应分测。
4. 有无博弈：论坛拥挤本身可能是反转信号（过度关注 → 反转）。
5. 事件性：非严格事件稀疏（日更流量），但 VECTOR 日内多帖需 vec_avg/vec_sum/vec_stddev。

预处理决策：
- 全部 VECTOR → 先 vec_avg（水平）/ vec_sum（总量）/ vec_stddev（分歧）。
- cov 0.89 > 0.4 → 不必强制 ts_backfill。
- 意见分可能有符号或单边，正反两臂各测（铁律 B）。
- 净意见可试 subtract(buy, sell)（同源同机制价差，合规；禁等权相加混信号）。

## 3. 质量先验 TOP（按 aC）

1. aggregate_sell_opinion_score aC7
2. aggregate_buy_opinion_score aC5
3. aggregate_comment_volume / comment_volume_per_platform aC3
4. total_distinct_participants_count aC1
5. distinct_user_count_per_platform aC0（最白）

头部轴 = 卖意见强度 + 买意见强度 + 评论量，不是参与人数。组装方向优先 A/B 族。

## 4. 机制假说（A-2 草稿）

| 机制 | 谁被定价 | 为什么错 | 修复期 | 方向草稿 |
|---|---|---|---|---|
| M1 注意力反转 | 高评论量股票被散户过度关注 | 注意力驱动短期高估（Barber-Odean / Da-Engelberg-Gao） | 数周~月 | 高评论量 → 后续低收益 |
| M2 净卖意见 | 论坛净卖出意见 | 散户情绪极端反向（Antweiler-Frank） | 数日~数周 | 高卖意见 → 待测（正反两臂） |
| M3 意见分歧 | buy/sell 同时高 | Miller 分歧-高估 | 月窗 | 高分歧 → 后续低收益 |
| M4 参与广度 | 独立用户数上升 | 信息扩散/关注拥挤 | 月窗 | 广度升 → 反转 |

## 5. socialmedia39 对照（严格 Social Media）

| 字段 | type | cov | aC | 说明 |
|---|---|---:|---:|---|
| scl39_top5_people_also_watch_ticker_ii | VECTOR | 1.0 | 580 | Atlas instrument ID 列表，非连续量；本轮仅探针，不作为主交付轴 |
