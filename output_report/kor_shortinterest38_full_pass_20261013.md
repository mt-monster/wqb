# ★ 全闸通过 —— KOR/D1 `shortinterest38` 成品报告（2026-10-13）

> 双确认：手工逐闸核验（`get_alpha_details` + `check_self_correlation` + `check_correlation(prod)`）
> ＋ 平台预检 `submit_verdict`（**`failed_ra = 0` / `failed_ppa = 0` / `sim_fails = []` / `hard_gate_warnings = []`**）。
> **未提交** —— 提交权归用户。

---

## 一、配方（两把钥匙破 `prod` 墙）

```
hump( subtract( group_rank( divide(vec_sum(shrt38_stk_invactsell_amt),
                                    add(vec_sum(shrt38_stk_invactbuy_amt), 0.0001)),
                             industry), 0.5),
      hump=0.003 )
设置：KOR / TOP600 / D1 · decay 4 · neutralization=SECTOR · truncation 0.08 · nanHandling ON
```

| 钥匙 | prod 变化 |
|---|---|
| 基准（`sector` + `hump=0.003`）| 0.7522 ❌ |
| **分组轴 `sector` → `industry`** | **0.6663 ✅** |
| **`hump` 0.003 → 0.005** | **0.604 ✅** |
| ⚠ 反例：`ts_mean(R, 5)` 时间平滑 | 0.7618（更差） |

## 二、成品（两颗，全闸通过）

| alpha | S | F | TO | SUB | **2Y** | inv / 限 | CW | CLUSTER | **self** | **prod** | 预检 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **`d5K508qg`** | **1.99** | **1.04** | 0.4159 | 1.59 | **2.03** | **1.74 / 1.39** | 未触发 | **1.34** | **0.413** | **0.6663** | ra=0 / ppa=0 |
| **`0mjmEkWG`** | 1.71 | **1.60** | 0.1556 | 1.57 | **2.09** | ✅ | 未触发 | — | **0.379** | **0.604** | ra=0 / ppa=0 |

点 **`KOR/D1/SHORTINTEREST`**（该数据集已提交 2 颗 → **本配方再提 1 颗即达 3，之后转点亮，须换集**）。

## 三、本会话打开的两道机制级墙（可复用）

| 墙 | 破法 | 实证 |
|---|---|---|
| **`LOW_INVESTABILITY_CONSTRAINED_SHARPE`**（限 = 0.70×S）| `vector_neut(·, power(rank(rsk68_weight_dadv), 0.5))`（残差到 **RISK 塔美元 ADV 轴**）| 保留率 57–65% → **70–73%**（115 条实验后首次通过） |
| **`CONCENTRATED_WEIGHT`**（KOR 特化 cw_gate=FAIL）| **居中放进 `hump` 内层**：`hump(subtract(group_rank(·), 0.5), hump=…)` | 23 条对照：单独居中 ❌ / 单独 hump ❌ / 组合 ✅ |

## 四、本会话全部成品清单

| 类别 | alpha | 状态 |
|---|---|---|
| **全闸通过（可直接提交）** | **`d5K508qg`** · **`0mjmEkWG`** | **RA 0 失败 / PPA 0 失败 / prod < 0.7 / self < 0.7** |
| 全 IS 闸通过（差 prod） | `e767ra3g`(0.7522) · `zqrqpZX8`(0.7292，PV 塔) · `KPmPa3xl` · `1YjY5A6m` · `kqJq56RO` | 待破 prod |

---
*⚠ 同族一次只提 1 颗（家族近亲提交会把后来者 self 冲 0.99+）；提完后必测 self。*
*⚠ 按用户政策：agent 不提交。*
