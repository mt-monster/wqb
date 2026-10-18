# ★ RA 全闸通过 —— KOR/D1 未点亮塔里程碑（2026-10-13）

> 判定依据：MCP `get_alpha_details`（`failed_ra_count` / `failed_ppa_count` / `checks`）+ `check_self_correlation` + `check_correlation(prod)`。
> **未提交** —— 提交权在用户；当前唯一剩余项为 **prod < 0.70**（实测 0.7275–0.7716）。

---

## 一、破闸构型（**4 颗均 `failed_ra_count = 0`**）

```
BASE = multiply(rank(multiply(-1, ts_kurtosis(<FIELD_K>, 140))),
                rank(multiply(-1, ts_rank(<FIELD_1>, 132))),
                rank(multiply(-1, ts_rank(<FIELD_2>, 252))))
ALPHA = vector_neut( trade_when(greater(rank(adv20), 0.1),
                                 scale(BASE, shortscale=0.5), -1),
                      power(rank(rsk68_weight_dadv), POW) )
设置：KOR / TOP600 / D1 · decay 4 · neutralization=MARKET · truncation 0.08 · nanHandling ON
```

| alpha | 字段组合 | POW | S | F | TO | SUB | **2Y** | **inv/限** | **self** | **prod** | failed_ra |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **`zqrqpZX8`** | spret / spret / spret | 0.5 | **1.90** | **1.16** | 0.4415 | **1.71** | **1.92** | **1.33/1.33 ✅** | **0.397 ✅** | **0.7292 ❌** | **0** |
| **`KPmPa3xl`** | spret / spret / spret | 0.75 | 1.87 | **1.17** | 0.4294 | **1.70** | **1.80** | **1.34/1.309 ✅** | **0.397 ✅** | 0.7485 ❌ | **0** |
| `1YjY5A6m` | spret / spret / spret@462 | 0.5 | 1.88 | 1.14 | 0.4422 | — | 1.91 | — | 0.3948 ✅ | **0.7275 ❌** | — |
| `kqJq56RO` | spret / spret@180 / spret | 0.5 | **1.90** | 1.16 | 0.4415 | — | 1.91 | — | 0.3941 ✅ | 0.7278 ❌ | — |
| `j2e2NQ9j` | spret / spret / **frac** | 0.5 | 1.70 | 1.07 | 0.3786 | **1.59** | **1.70** | **1.24/1.19 ✅** | 0.3956 ✅ | 0.7716 ❌ | **0** |
| `zqrqXz5V` | spret / **frac** / spret | 0.5 | 1.71 | 1.08 | 0.3788 | **1.59** | **1.71** | **1.23/1.197 ✅** | 0.3951 ✅ | 0.7715 ❌ | **0** |

**4 颗均点 2 个 0 计数塔**：KOR/D1/**RISK**(1.3) + KOR/D1/**PV**(1.4)，effective **2**。
`failed_ppa_count` 亦为 **0**（PPA 全过）。`frac` = `idiosyncratic_return_fraction`。

## 二、★ 破墙三要素（缺一不可）

1. **`ts_kurtosis(·, 140)` —— 防御腿；K 窗口直接决定 2Y**
   实测：K=132 → 2Y 1.50｜**K=140 → 2.02**｜K=150 → 2.00｜K=160 → 1.47｜K=180 → 1.40
2. **`trade_when(rank(adv20)>0.1)` + `scale(·, shortscale=0.5)`** —— 流动性过滤 + 空端缩放
3. **`vector_neut(·, power(rank(rsk68_weight_dadv), POW))`** —— 残差到 **RISK 塔美元 ADV 轴**（cov 1.0），保留率的钥匙

**POW 档位 ↔ 两闸（K=140）**：0.25 → 2Y 2.02 / inv 67.2% ❌｜**0.5 → 2Y 1.92 / inv 70.0% ✅（交点）**｜
0.75 → 1.80 / 71.7% ✅｜1.0 → 1.56 / 73.2% ❌ ⇒ **POW=0.5 是 2Y 与 investability 的交点**。

## 三、六天推进路径

| 阶段 | 结果 |
|---|---|
| 起点 | 12 个 0 塔全灭；2Y 与 investability 两道墙 |
| 找 2Y 钥匙 | `ts_kurtosis`（防御维）→ 2Y 天花板 **1.15 → 1.59** |
| 定中性化 | 11 档全试 → **MARKET** 唯一「F 与 2Y 兼顾」 |
| 破 investability | 115 条实验后，**`vector_neut` 到美元 ADV 轴** → 保留率 **57–65% → 73.2%** |
| 找 2Y 余量 | K=160→1.47，改用 **K=140** → 2Y **2.02** |
| 定交点 | POW=0.5 → **`failed_ra_count = 0`** |

## 四、唯一剩余：**prod 墙**（0.7275 vs 0.70）—— 已实测为「密墙」

| 尝试 | prod |
|---|---|
| 基准（K140/POW0.5）| 0.7292 |
| `ts_rank` 第二窗 66/100/110/150/180 + 第三窗 462 | **0.7275–0.7292**（不动）|
| POW 0.55 / 0.6 | 0.7344 / 0.7275（不动）|
| **换第二腿语义**（→ `idiosyncratic_return_fraction`）| **0.7715**（更差）|

⇒ prod 恒在 **0.727–0.771**，由「特质收益反转」这一**核心语义**决定，同族内任何结构改动都无效
（[0.7,0.8) 桶已密）。**若要破，必须引入第二个经济维度**（合规形态：`trade_when` 条件 / `group_rank` 分组 / `vector_neut` 残差），或接受现状。

---
*已提交 3 颗（OS 池内）：`O08kz5Mv`(SHORTINTEREST) · `gJZR9XNm`(MODEL) · `0mre68gv`(MODEL)*
*本 4 颗（RA 全闸通过）**未提交**，待 prod 墙破除或由您决策。*
