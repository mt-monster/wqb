# EUR × news7 字段画像（2026-11-09）

> 118/118 字段全量拉取（complete=true）；Real Time News Feed Data（欧洲新闻服务实时流）
> 塔位：NEWS(×1.4，1/3)；拥挤度：aC 308 / uC 194；os_is 0.4147

## 一、字段族结构（六维）

| 族 | 字段（示例） | 类型/cov | 更新频率 | 分布 | 可用性 | 适用性 |
|---|---|---|---|---|---|---|
| A1 新闻频率（关注度） | nws7_eur_news_freq_2_qerf(0.957)、news_mention_frequency_2(0.931)、_alt_nf(0.9313)、_pzeng(0.9306) | MATRIX/0.93+ | 日频事件流 | 计数右偏，稀疏日多 | uC 13-20 中等冷门 | **唯一可用读数**：关注度=条数（Xgojww1X 同机制族） |
| A2 关键词过滤频次 | _qerf 系列（earnings/sales/analyst 关键词，cov 0.40-0.57） | MATRIX/0.40-0.57 | 日频 | 稀疏 | uC 0-2 极冷 | earnings/sales 事件日注意力，cov 不足 sub 闸风险 |
| B 情绪语气 | headline_overall_tone_score_2(0.926)、storytone_tone_score(0.451) | MATRIX/0.43-0.93 | 日频 | [-1,1] 近对称 | uC 4-14 | **极性族判死**（news46 77 条 S<0.6 同族）——禁做 |
| C 元数据 | story_time/take_seqno/product_code/area/display_name | VECTOR | — | — | — | 禁作信号 |
| D 全文/标签 | livenews_story_full_text(0.976) | VECTOR | — | — | — | 文本原稿，不可直接用 |

## 二、关键风险
- **事件型 TO 爆炸**（普查表判 news7「TO 风险」；news7 提及计数日间跳变）
- 与 news46（RavenPack）同机制族：关注度天花板 1.32 已实证——news7 频率读数先验同级

## 三、结论
1. 唯一可用读数 = A1 频率计数（cov 0.93 版本），机制族与 news46 相同 → 天花板先验 ≈1.3
2. 情绪语气族禁做（家族判死）；元数据禁用
3. **判定：低强度先验 + TO 风险 + 同族天花板已实证 → 留档不投槽**（若投需 2 臂探针：freq z-score 35d + 双窗 5/66，与 news46 同几何）
