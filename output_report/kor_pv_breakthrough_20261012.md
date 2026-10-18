# KOR/D1 PV 塔破冰报告（2026-10-12 更新：investability 攻坚结论）

> 判定依据：MCP `get_alpha_details`（`ra.ra_failed_checks` + `checks`）。**未提交** —— 提交权在用户。

---

## 一、当前状态：5 项硬闸过 4 项，卡 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`

| 候选 | S | F | TO | SUB | 2Y | **investability / 限** |
|---|---|---|---|---|---|---|
| **`O08jNNKd`** | **1.97** | **1.12** | 0.461 | 1.58 | **1.58**（差 0.01）| **1.28 / 1.38** |
| `d51MWeZ2` | 1.83 | 1.00 | 0.479 | 1.52 | **1.92** ✅ | 1.16 / 1.28 |
| `58gePWJM` | 1.88 | 1.03 | 0.509 | 1.52 | **1.59** ✅ | 1.20 / 1.32 |

**该项限 = 0.70 × S ⇒ 需「保留率 ≥70%」；本族稳定 62–65%。**

## 二、本回合全部已试手段（d174–d179，55 条）

| 手段 | 结果 |
|---|---|
| 流动性过滤 × 8 窗口 | S 1.64–2.03，**2Y 上限 1.56** ⇒ 过滤与 2Y 反向 |
| `scale(shortscale)` / `normalize` / `zscore` / `winsorize` | S 抬到 1.97、2Y 1.58，**inv 不动（1.22→1.28）** |
| 过滤+scale 组合 | 最优：S1.97/F1.12/2Y1.58/inv1.28（两项各差 0.01 / 0.10）|
| 更温和过滤（adv20>0.05）| **2Y 1.92 ✅** 但 inv 降到 1.16 |
| 更强过滤（adv20>0.3/0.5）| S 崩到 1.41/0.97 ⇒ **inv 与 S 反向** |
| `scale(longscale=…)` | **无效**（平台只对 short 端生效）|
| 换 pv47 其它字段 | 更弱或同解 |

## 三、★ 结论：这是**机制级**障碍，不是参数问题

> **特质收益反转的本质是「向非流动股提供流动性」，其 alpha 来源就在小票上。**
> 无论怎么过滤 / 缩放，保留率都在 **62–65%** 震荡，无窗口组合能同时推到 70% 与 2Y≥1.59。

过滤强度与三个指标的关系：

| 过滤强度 | 2Y | investability | S |
|---|---|---|---|
| 无 | 1.59 ✅ | 1.20 ❌ | 1.88 |
| adv20>0.05 | **1.92** ✅ | 1.16 ❌ | 1.83 |
| adv20>0.10 | 1.58 ❌ | **1.28**（最接近）| **1.97** |
| adv20>0.30 | 1.00 | — | 1.41 ❌ |

## 四、核心资产（可复用构型）

```
BASE = multiply(rank(multiply(-1, ts_kurtosis(pv47_for_statssimple_only_spret, 160))),
                rank(multiply(-1, ts_rank(    pv47_for_statssimple_only_spret, 132))),
                rank(multiply(-1, ts_rank(    pv47_for_statssimple_only_spret, 252))))
settings: KOR / TOP600 / D1 / decay 4 / neutralization=MARKET / trunc 0.08 / nanHandling ON
塔: KOR/D1/PV (1.4) ← 0 计数
```
- **2Y 钥匙 = `ts_kurtosis`（防御维）** —— 0 塔信号族 2Y 天花板 1.15 → **1.59**。
- **`MARKET` 是唯一 F 与 2Y 兼顾的中性化档**。
- **`ts_ir` / `ts_target_tvr_hump` KOR 不可用**；`ts_target_tvr_decay` 可用但等比例杀 S。

## 五、下一步（待决策）
1. **换数据集**：PV 塔内换「天然高流动」字段族（`pv103` 本地字段名平台不可用，需先 `get_datafields` 核实命名）。
2. **换塔**：把 `ts_kurtosis` 钥匙用到 OTHER/NEWS 等 0 塔的高流动字段上。
3. **接受现状**：`O08jNNKd` 距全闸仅 0.01（2Y）+ 0.10（inv）。

---
*已提交 3 颗（OS 池内）：`O08kz5Mv`(SHORTINTEREST) · `gJZR9XNm`(MODEL) · `0mre68gv`(MODEL)*
