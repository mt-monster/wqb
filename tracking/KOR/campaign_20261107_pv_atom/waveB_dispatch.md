# Wave B 派发台账 · KOR × PV × ATOM（continuation_score）

## 背景
- analyst 塔已点亮（KOR/D1/analyst = 3）⇒ 按「已点亮塔不选」停挖 analyst。
- 当前已点亮：analyst 3 / fundamental 3 / model 3 / shortinterest 4。
- 未点亮：risk 0 / insiders 1 / earnings 0 / institutions 0 / macro 0 / news 0 / sentiment 0 / socialmedia 0 / imbalance 0 / other 1 / **pv 2**。
- PV 仅 2/3，未点亮；单数据集 ATOM 不触发禁混规则 ⇒ 合法可挖。

## 选集依据
| 数据集 | cov | 字段 | aC | users | vs | 备注 |
|---|---:|---:|---:|---:|---:|---|
| **continuation_score** | 1.0 | 560 (全 MATRIX) | **544** | 273 | **4.0** | 形态相似度，覆盖率满分，拥挤度低 |
| pattern_scores | 1.0 | 504 (MATRIX) | 331 | 177 | 4.0 | 备选，另一套形态分类法 |
| pv106 | 1.0 | 29 | 992 | 351 | 2.0 | 微观结构价差，备选 |
| pv1 | 1.0 | 24 | **91663** | 3465 | 1.0 | 极度饱和，不用 |

## 机制来源
- **论坛**：《continuation_score 数据集因子模板分享》（MW42501, 2026-09-01），模板 = bullish净分 − bearish净分 → rank，建议 TWN/D1。
- **论文**：Lo, Mamaysky & Wang (2000), *Foundations of Technical Analysis*, J. Finance 55(4) — 系统化形态识别（核回归）在美股 1962–1996 上「若干技术指标确实提供增量信息」。

## 10 个结构互异模板（算子数）
| # | 机制 | 几何 | 算子 |
|---|---|---|---:|
| B-01 | 三对净分加总（论坛模板） | rank + add链 | 7 |
| B-02 | bull/bear 比例 | divide | 5 |
| B-03 | 缺口延续方向 | 单对差值 | 3 |
| B-04 | 净分时序变化速度 | ts_delta 22 | 6 |
| B-05 | 净分时序历史分位 | ts_rank 252 | 4 |
| B-06 | 主导形态强度（取大） | max | 5 |
| B-07 | 形态离散度/模糊度 | 反向 add | 3 |
| B-08 | 形态新鲜度 recent−avg | 单形态差 | 3 |
| B-09 | 尾部强度 p95 差 | 分位差 | 3 |
| B-10 | 反转形态 cup&handle vs inverse | 单对差值 | 3 |

## 预检
- 第一轮 `valid=false`，抓到幽灵字段 `bearish_pennant_similarity_average`（实际只有 `_h40w` / `_recent`）⇒ 已替换为 `bearish_pennant_similarity_average_h40w`。
- 第二轮：`valid=true` / `unknown_fields=[]` / `any_changed=false`。

## 设置档
REVERSION_AND_MOMENTUM · decay 4 · truncation 0.08 · nanHandling ON · 2014-01-01~2023-12-31

## 判读预案
- 任一 S≥1.58 且 F≥1.0 且 2Y≥1.58 ⇒ 进交付队列，查逐年覆盖 + self/prod。
- B-01/B-02/B-05 最强 ⇒ 沿 net-similarity 族扩产（换形态对、换窗口）。
- 全灭 ⇒ 转 pattern_scores（另一套分类法）或 pv106 价差族。