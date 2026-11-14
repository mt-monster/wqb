# BE43a 派发：NEWS×INSIDERS 破闸救援（窗口谷 + 未试字段变换，2026-11-11）

## 一、为什么再投这一线

BE14 把 nws20×I7 线推到 S 1.52（QP010j5W），差 0.06 破闸；且 S-TO 前沿上有
kqaxaX1l（hump 版：F1.01/sub0.74/2Y2.29 全过、仅 S 1.38 差 0.20）。
按用户纪律「有进展方向必须持续投入直到破闸（连续 ≥3 档无改善才算死）」，
本波填 BE14 没扫过的微调杠杆：

1. **窗口谷**：Δ 只试过 66/132/264，44/55/88 未扫；
2. **字段维度**：news20 的 multiple_comp 家族（cov 0.9191）里
   nip（影响度）×ssc（综合情绪）= BE38 在 news18 上验证过的「影响度×情绪」
   几何（0.20→0.79 提升实证），从未套在 nws20 上；
3. **relevance 加权**：event_relevance（0-100）乘 sentiment，BE38 同源先验；
4. **第二腿窗口**：I7 的 ts_rank 504 变体（BE14 只试过 ts_mean22 平滑，反而更差）;
5. **QP010j5W+轻平滑杂交**：外层 group_rank（S 1.52 来源）+ ts_mean(8)（TO 压向 0.125 甜点）。

## 二、派发内容（sim 28xKtQ3dj4hQa7j1aVK5tr0A，8 臂）

设置：DEU / TOP500 / D1 / decay4 / SUBINDUSTRY / trunc 0.08 / nan ON（与 BE13b-BE22 完全一致）。

| 臂 | 变体 | 预检 |
|---|---|---|
| 1 | Δ44 窗口谷 | valid |
| 2 | Δ88 窗口谷 | valid |
| 3 | nip×ssc 影响度加权（BE38 几何移植） | valid |
| 4 | ssc 综合情绪替 event_sentiment_score | valid |
| 5 | relevance 加权（sentiment × event_relevance） | valid |
| 6 | ts_backfill 132→66（回填谷） | valid |
| 7 | I7 ts_rank 252→504 | valid |
| 8 | QP010j5W（外层 group_rank）+ ts_mean8 轻平滑 | valid |

算子数：10-12/臂（≤12 硬约束 ✓）。news 腿负号沿用 BE13b 实证符号。

## 三、验收预锁

出货判据：S≥1.58 且 F≥1.0 且 2Y≥1.58 且 sub≥0.474×S 且 TO∈[0.01,0.7]
→ 过 IS 全闸后才测 self/prod（SOP 闸序纪律）。
