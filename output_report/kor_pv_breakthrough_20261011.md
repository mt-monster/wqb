# KOR/D1 未点亮塔破冰报告（2026-10-11 更新）

> 判定依据：MCP `get_alpha_details`（`ra.ra_failed_checks` + `checks`）。**未提交** —— 提交权在用户。

---

## 一、结论：PV 塔（0 计数）**5 项硬闸已破 4 项**

| 候选 | S | F | TO | SUB | **2Y** | investability / 限 | self |
|---|---|---|---|---|---|---|---|
| **`58gePWJM`** | 1.88 | **1.03** | 0.509 | 1.52 | **1.59 ✅** | **1.20 / 1.32**（64%）❌ | **0.36 ✅** |
| `88PXo9zo`（+流动性过滤）| 1.95 | 1.11 | 0.461 | 1.55 | 1.56 ❌ | 1.27 / 1.36（65%）❌ | — |
| `zqbeKZEG`（+adv20 过滤）| 1.86 | 1.03 | 0.466 | 1.49 | **1.91 ✅** | 1.16 / 1.30（62%）❌ | — |

**唯一剩余障碍 = `LOW_INVESTABILITY_CONSTRAINED_SHARPE`**（要求 investability_sharpe ≥ **0.70×S**，
即**保留率 ≥70%**；本族稳定 62–65%）。

## 二、核心构型（可复用）

```
multiply(rank(multiply(-1, ts_kurtosis(pv47_for_statssimple_only_spret, 160))),
         rank(multiply(-1, ts_rank(    pv47_for_statssimple_only_spret, 132))),
         rank(multiply(-1, ts_rank(    pv47_for_statssimple_only_spret, 252))))
settings: KOR / TOP600 / D1 / decay 4 / neutralization=MARKET / truncation 0.08 / nanHandling ON
塔: KOR/D1/PV (1.4)  ← 0 计数
```

## 三、三条硬发现

1. **2Y 钥匙 = `ts_kurtosis`（防御维）** —— 竞态/不确定性维度，契合 KOR 2022–23 熊市。
   把 0 塔信号族的 2Y 天花板从 **1.15 → 1.59（+38%）**。
2. **`MARKET` 是唯一「F 与 2Y 兼顾」的中性化档**（STATISTICAL 2Y 高 F 低；INDUSTRY 反之；SECTOR 居中）。
3. **算子可用性**：`ts_ir` / `ts_target_tvr_hump` **KOR 不可用**（整批连坐 FAIL 且无报错）；
   `ts_target_tvr_decay` 可用，但压 TO 的同时**等比例杀 S**。

## 四、investability —— 已试手段全表（全部无效）

| 手段 | 结果 |
|---|---|
| 流动性过滤 `trade_when(greater(rank(adv20),0.1), X, -1)` | inv 1.20→**1.27** ✅ 但 2Y 1.59→**1.56** ❌ |
| 该过滤族 × 窗口扫描（8 条）| S 1.64–2.03，**2Y 上限 1.56** |
| 市值过滤（剔大盘 / 剔小盘）| 反向，更差 |
| 流动性/市值中性化（`group_neutralize` 到桶 / `vector_neut`）| 无提升 |
| truncation 0.02 / 0.15、decay 1 / 8 | S 崩 或 TO 爆 |

## 五、当前正在验证的新方向

**把获胜模板移植到「天然高流动」的 `pv103`（KOR 收盘拍卖时段 14:30–14:30）** —— 从源头提高保留率，
而非事后过滤。字段：`final/initial`（盘中收益）、`VWAP/final`、`max/min`、`market_value/volume`。

---
*已提交 3 颗（OS 池内）：`O08kz5Mv`(SHORTINTEREST) · `gJZR9XNm`(MODEL) · `0mre68gv`(MODEL)*
