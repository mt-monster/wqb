# EUR × news46 字段画像（2026-11-08）

> 平台目录：30/30 字段全量（complete=true；18 VECTOR 原始事件流 + 12 MATRIX ravenpack 聚合）
> 塔位：NEWS(×1.4，本季 1/3，差 2 颗点亮)；MWS46 = 每股聚合的 MarketWatch/RavenPack 新闻评分

## 一、字段族分组

| 族 | 字段 | 类型/cov | 语义 | 适用性 |
|---|---|---|---|---|
| A1 关注度 | mws46_ravenpack_sum_story_count | MATRIX/0.9081 | 聚合窗内故事条数总和 | **已验证方向（Xgojww1X 在用）**：注意力=关注度；新候选必须换几何避开 |
| A1' 原始流 | mws46_story_count | VECTOR/1.0 | 逐事件故事计数 | 需 vec_sum，事件型 TO 风险 |
| A2 影响力 | mws46_ravenpack_sum_nip / mean_nip | MATRIX/0.9081 | 新闻冲击预测分（未来 2h 市场影响 0–100） | **未开采**：冲击加权注意力 |
| A3 新颖度 | mws46_ravenpack_sum_ens / mean_ens | MATRIX/0.6975 | 事件新颖度（0–100） | cov 0.70 贴线，sub 闸风险 |
| A4 极性 | mws46_ravenpack_sum_ess/ssc、mean_ess/ssc | MATRIX/0.70–0.91 | 情绪极性分 | **已判死**（77 条 S<0.6），禁做 |
| A5 相关度 | mws46_ravenpack_sum_relevance / mean_relevance | MATRIX/0.9081 | 实体相关度（0–100） | 加权分母备选 |
| B 事件类目 | mws46_mcp/mce/mcr/mcv、news_type | VECTOR/1.0 | 事件类别评分（盈利/公司行动/并购） | 需 vec_*；类目门控备选 |
| C 元数据 | mws46_time、ens_key、story_index、ens_elapsed | VECTOR | 时间戳/链键 | 禁作信号 |

## 二、实证

- **Xgojww1X**（ACTIVE，[RISK,NEWS]，S1.8/prod 0.5906/self 0.2431）：`(group_rank(ts_zscore(ts_backfill(sum_story_count,120),35),subindustry) + group_rank(ts_zscore(ts_backfill(rsk70_mfm2_euetrd_earnyild,120),20),subindustry)) / 2`——**关注度 z-score 35d + 子行业秩**读数已占位。
- 极性读数 77 条判死（S<0.6）⇒ 新读数只允许从 A2 影响力 / A3 新颖度 / A1 几何变体（动量/惊喜/双窗）里找。
- 文献先验：Da-Engelberg-Gao 2011（注意力→短期正收益）；Tetlock 2011（陈词滥调→反转）。

## 三、结论

1. 主攻：A2 影响力加权注意力（sum_nip，与条数计数不同权重结构）与**关注度惊喜**（短窗秩 − 长窗秩）。
2. 禁区：极性族（判死）、元数据族。
3. 与 Xgojww1X 的 self 检查必须做（本地 compute_mutual_correlation 免费）。
