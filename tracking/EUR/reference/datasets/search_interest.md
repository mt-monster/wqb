# search_interest · EUR / TOPCS1600 / D1 字段画像

> 类型 VECTOR · 5 字段 · cov 0.91（_7）/ 0.25（_8）· category = **other**（×1.5）· αC 8
> 采集：2026-11-07

| 字段 | 语义 |
|---|---|
| `relative_interest_score_6/_7/_8` | 标准化搜索兴趣分（非 0-100 原始刻度） |
| `trend_confidence_overlap_months_4` / `trend_estimation_confidence_score_4` | nowcast 置信度（辅助轴） |

## 实测（已终态,multisim `Djp2bePm59Lc7pIx1DuNo9`,FAST/decay15）

| 变体 | alpha id | S | 2Y |
|---|---|---|---|
| reverse _7 66/252 | `xAr21zoq` | −0.87 | −0.33 |
| **正向 _7 66/252** | **`KPJ5m8p8`** | **0.87** | 0.33 |
| reverse _7 22/252 | `N1NJejG7` | −0.82 | −0.06 |
| reverse _6 66/252 | `npveAzla` | −0.82 | −0.51 |

**归因**：搜索兴趣**正向动量**（高搜索→继续涨,与 behavioral_signals 的 streak 动量同构）——Da et al. 反转在 EUR 不成立;正向 0.87 距闸 1.8×,4 探针 + 同构先验,**归档**。与 news18 密度席位机制不同源（密度是事件计数反转,本集是搜索量动量）,若未来需要 OTHER 塔可回补正向 0.87 作为起点,但优先级低。
