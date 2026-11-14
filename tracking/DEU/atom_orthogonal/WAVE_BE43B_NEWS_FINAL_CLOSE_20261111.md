# BE43b 判决：NEWS×INSIDERS 线正式收口（S 天花板 1.52，六维穷尽）（2026-11-11）

## 一、正号救援波 8 臂结果（sim 1deDcm33t5k4awe15y26MWm6，complete=8）

| 臂 | 变体 | alpha | S | F | TO | sub | y2 | fail |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | Δ44 窗口谷 | LLKLOorL | 1.15 | 0.54 | 0.25 | 0.57 | 1.38 | 3 |
| 2 | Δ55 窗口谷 | omamQjr2 | 1.16 | 0.56 | 0.24 | 0.30 | 1.55 | 4 |
| 3 | Δ88 窗口谷 | P05JxzeK | 1.31 | 0.68 | 0.23 | **0.81** | **1.57** | 3 |
| 4 | nip×ssc 影响度加权 | rK7KQaVo | 1.04 | 0.43 | 0.30 | 0.11 | 1.53 | 4 |
| 5 | relevance 加权 | YPaPX3JJ | **1.52** | 0.85 | 0.23 | 0.52 | 1.43 | 4 |
| 6 | backfill 66 | pwawQbZb | 1.34 | 0.71 | 0.23 | 0.61 | 1.34 | 4 |
| 7 | I7 ts_rank 504 | akakXmG6 | 1.43 | 0.76 | 0.24 | 0.62 | 1.30 | 4 |
| 8 | 外层 group_rank + mean8 | LLKLOo36 | 1.33 | **0.88** | 0.14 | 0.67 | 1.37 | 3 |

## 二、窗口谷确认与天花板确认

- Δ 窗口全扫：44→1.15 / 55→1.16 / **66→1.46（峰）** / 88→1.31 / 132→1.10 / 264→1.09——66 就是峰；
- 影响度加权（nip×ssc，news18 的成功几何）**不可迁移**到 news20（1.04）；
- relevance 加权 1.52 = QP010j5W 1.52——**两条独立构造同时顶在 1.52**；
- 全部 8 臂无人破 1.58。

## 三、线状态与相关性

- P05JM61x 对全量 OS 池 self = **0.2102 PASS**（top 2rmGAPqN）——线是干净的，死在强度；
- BE14 1.52 → BE43b 1.52：两轮无改善。

## 四、六维穷尽度（判死档案要求，全部覆盖）

| 维度 | 覆盖 |
|---|---|
| D1 模板互异 ≥10 | ✅ BE13b 5 + BE14 10 + BE43a 8（差值几何证伪）+ BE43b 8 = 31 臂 |
| D2 字段族自测 | ✅ event_sentiment_score / ssc / nip / qep / relevance / ghc_lna / ber（nws 族历史波）|
| D3 矩全家 | ✅ Δ44/55/66/88/132/264、水平 zscore、ts_rank 位置、平滑 mean8/22/44、hump |
| D4 分组轴 | ✅ sector 内层 / market 外层 / industry / subindustry 外层 |
| D5 非线性 | ✅ hump 门控、外层 group_rank、relevance/nip 乘法加权、winsorize（f 族波） |
| D6 配置 | ✅ 中性化 4 档曲线（SUBINDUSTRY 1.46 > STATISTICAL 1.38 > INDUSTRY 1.37 > FAST 1.32）× TOP500/D1 唯一组合 |

## 五、终审

**NEWS×INSIDERS 线 S 天花板 = 1.52，S≥1.58 不可达。** 判死（非 PROVISIONAL）。
NEUTRALIZATION 若未来作为微调：INDUSTRY 档以 S−0.09 换 sub+0.18/y2+0.16，仅当其它维度卡 sub 时可用。
