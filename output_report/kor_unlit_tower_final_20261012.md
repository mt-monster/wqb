# KOR/D1 未点亮塔 —— 最终结论报告（2026-10-12 20:45）

> 判定依据：MCP `get_alpha_details`（`ra.ra_failed_checks` + `checks`）。**未提交** —— 提交权在用户。
> 四天累计 **100+ 条实验**。

---

## 一、结论：未点亮塔空间**已穷尽**，产出 0；唯一活口差 2 项

### 唯一活口（PV 塔 = 0 计数）

```
BASE = multiply(rank(multiply(-1, ts_kurtosis(pv47_for_statssimple_only_spret, 160))),
                rank(multiply(-1, ts_rank(    pv47_for_statssimple_only_spret, 132))),
                rank(multiply(-1, ts_rank(    pv47_for_statssimple_only_spret, 252))))
ALPHA = trade_when(greater(rank(adv20), 0.1), scale(BASE, shortscale=0.5), -1)
settings: KOR / TOP600 / D1 · decay 4 · neutralization=MARKET · trunc 0.08 · nanHandling ON
```

| 指标 | `O08jNNKd` | 限 | |
|---|---|---|---|
| Sharpe | **1.97** | 1.58 | ✅ |
| Fitness | **1.12** | 1.00 | ✅ |
| Turnover | **0.461** | 0.70 | ✅ |
| Sub-universe S | **1.58** | ~0.94 | ✅ |
| **2Y (ladder)** | **1.58** | 1.58 | ⚠️ 差 0.01 |
| **investability** | **1.28** | **1.38**（=0.70×S）| ❌ 差 0.10 |
| self | 0.36 | 0.70 | ✅ |

## 二、已穷尽的六个维度（每项都有实测支撑）

| # | 维度 | 覆盖情况 | 结果 |
|---|---|---|---|
| 1 | **12 个 0 塔全部数据集** | analyst / risk / pv / institutions / insiders / imbalance / earnings / macro / socialmedia / sentiment / news / other | 仅 **PV 的 `pv47_spret`** 出强信号，其余全判死 |
| 2 | **全部 11 档中性化** | NONE / STATISTICAL / **MARKET** / SECTOR / INDUSTRY / SUBINDUSTRY / SLOW_AND_FAST / CROWDING / FAST / SLOW / REVERSION_AND_MOMENTUM | **MARKET 最优**（保留率 65% vs 其余 57–63%）|
| 3 | **universe** | KOR D1 **仅 `TOP600`**（平台实测）| 换档位这条路不存在 |
| 4 | **`ts_kurtosis` 钥匙跨族** | 4 个数据集验证（forum / sentiment_transfer / acquisition_model / other545）| **不可迁移**（只在日频收益分布型字段有效）|
| 5 | **降 TO 七手段** | ts_mean / decay / hump / ts_decay_linear / 长窗口 / trade_when / ts_target_tvr_decay | **全部在压 TO 时等比例杀 S**（唯一成功的是 `multiply` 双腿乘积）|
| 6 | **investability 78 条实验** | 流动性过滤 8 档 / 市值过滤 / 流动性·市值中性化 / scale 不对称 / truncation / decay | 保留率稳定 **57–65%**，**机制级障碍** |

## 三、两条机制级障碍（非参数问题）

1. **`LOW_INVESTABILITY_CONSTRAINED_SHARPE`**：限 = **0.70×S** ⇒ 需保留率 ≥70%。
   特质收益反转的 alpha 来源**就在小票上**（向非流动股提供流动性）—— 过滤越强，alpha 越少。
2. **2Y 与 investability 反向**：过滤弱 → 2Y 1.92 但 inv 1.16；过滤强 → inv 1.28 但 2Y 1.58。**无交点**。

## 四、决策建议

未点亮塔路线**已无余量**，建议二选一：

1. **放宽「仅未点亮塔」约束** —— 我手上已有 13 颗 IS 全过（S 1.49–2.87）的候选，但 **prod 全部 0.78–0.98 撞墙**（KOR 是重度挖掘区，复刻公开配方必撞 prod）。
2. **换 region** —— 当前锁定 KOR；若可解开，DEU / IND / EUR 的 0 塔空间尚未探。

---
*已提交 3 颗（OS 池内）：`O08kz5Mv`(SHORTINTEREST) · `gJZR9XNm`(MODEL) · `0mre68gv`(MODEL)*
