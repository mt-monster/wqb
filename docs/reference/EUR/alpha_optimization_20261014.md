# EUR 两颗候选 alpha 优化报告

> 2026-10-14 ｜ 工具：skill `wq-alpha-gate-push-op-min`（双目标：推到全闸 + 算子压到最少）
> 参照次序：① 采集 → ② 算子审计 → ③ 杠杆推指标 → ④ 压缩算子 → ⑤ 设置收敛 → ⑥ 判定

---

## 一、结论速览

| # | alpha | 数据集（塔） | S | F | TO | SUB | CLUSTER | ROBUST | 2Y | returns | PROD | SELF | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | **`786pLKnb`** | analyst_factor_signals（Analyst / 未点亮） | 1.71 | 1.09 | 0.1124 | 1.16 | 1.62 | 0.98 | 1.78 | 5.07% | 0.6171 | 0.1753 | ★ **ACTIVE**（已提交） |
| 2 | ★**`LL5VwgO1`** | techindi_model（Other / 未点亮） | **2.64** | **1.27** | 0.3774 | 1.71 | 1.88 | **0.97** | **2.07** | **8.71%** | 0.6926 | −0.0114 | 全闸过，待用户确认 |

**两腿互相关 = 0.0947** ⇒ 完全独立，可各自提交。

---

## 二、`786pLKnb`（Analyst 腿）—— 无优化空间（已是局部最优）

**表达式（4 算子 = 结构下限）**
```
signed_power(group_rank(divide(eps_revision_magnitude,
                               ts_mean(eps_y1_estimate_coeff_var, 55)),
                        industry),
             3.0)
```

### 2.1 平台回执
```
VERDICT: ALREADY_SUBMITTED（status=ACTIVE）   ← 该腿已提交生效
模拟层 checks: 13 条（FAIL 0 / WARNING 1）
```

### 2.2 杠杆扫描（wave547，8 条）—— 全部劣于原版

| 变体 | S | F | 2Y | 判定 |
|---|---:|---:|---:|---|
| **原版**（industry / p3.0 / 窗 55 / decay1） | **1.71** | **1.09** | **1.78** | ★ **最优** |
| 轴 → `sector` | 1.62 | 1.02 | 1.50 | ❌ 2Y 掉闸 |
| 轴 → `market` | 1.58 | 0.99 | 1.47 | ❌ 2Y 掉闸 |
| 幂次 → 4.0 | 1.68 | 1.07 | 1.73 | ❌ |
| 窗 55 → 66 | 1.68 | 1.07 | 1.73 | ❌ |
| 窗 55 → 44 | 1.68 | 1.06 | 1.67 | ❌ |
| **`winsorize(..., std=3)`** | 1.71 | 1.09 | 1.78 | ⚪ **no-op**（指标逐位相同） |
| 双窗秩乘积（short 2 / long 252） | 1.42–1.43 | 0.86–0.88 | 1.62 / 1.58 | ❌ |

### 2.3 算子压缩（4 算子为结构下限，逐算子消融结论）
| 删除/替换 | 后果 |
|---|---|
| 删 `signed_power` | F 1.09 → **0.88 掉闸** |
| 删 `ts_mean` | 2Y 1.78 → **1.52 掉闸** |
| `group_rank` → `rank`（去轴） | 2Y 1.78 → **1.16 掉闸** |
| 删 `divide` | 结构消失 |

⇒ **该腿已完全收敛**：4 个算子缺一不可，全部已知杠杆均已扫描。

---

## 三、`e76kv2xE` → **优化为 `LL5VwgO1`**（techindi 腿）

**优化后表达式（7 算子，与优化前同）**
```
signed_power(group_rank(multiply(rank(ts_mean(predicted_fifth_quantile_ten_day_return_15, 2)),
                                 rank(ts_mean(predicted_fifth_quantile_ten_day_return_15, 252))),
                        industry),
             2.5)
```
**唯一改动 = `signed_power` 幂次 3.0 → 2.5**

### 3.1 优化前后逐项对比

| 指标 | 原版 `e76kv2xE`（p3.0） | ★**优化版 `LL5VwgO1`（p2.5）** | 变化 |
|---|---:|---:|---|
| **Sharpe** | 2.60 | **2.64** | **+0.04** |
| **Fitness** | 1.23 | **1.27** | **+0.04** |
| Turnover | 0.3834 | **0.3774** | −0.006 |
| SUB_UNIVERSE（限 1.4） | 1.67 | **1.71** | +0.04 |
| CLUSTER_TEST | 1.82 | **1.88** | +0.06 |
| **ROBUST_UNIVERSE** | 0.93 | **0.97** | **+0.04** |
| **IS Ladder（2Y）** | 1.94 | **2.07** | **+0.13** |
| **returns** | 8.54% | **8.71%** | +0.17pp |
| **PROD** | 0.6916 | **0.6926** | +0.001（仍 ✅ <0.7） |
| **SELF** | −0.0149 | **−0.0114** | ✅ |
| 算子数 | 7 | **7** | 相同 |

⇒ **除 prod 微升 0.001 外，全部指标同向改善** ⇒ 采纳 `LL5VwgO1`，原 `e76kv2xE` 标 **SUPERSEDED**。

### 3.2 ★ 幂次 ↔ prod 的关键关系（本轮核心实证）

| 幂次 | S | F | 2Y | **PROD** |
|---|---:|---:|---:|---:|
| **2.5** | **2.64** | **1.27** | **2.07** | **0.6926 ✅** |
| 2.6 | 2.63 | 1.26 | 2.04 | — |
| 2.8 | 2.62 | 1.24 | 1.99 | — |
| 3.0 | 2.60 | 1.23 | 1.94 | **0.6916 ✅** |
| 4.0 | 2.52 | 1.15 | 1.74 | 0.6918 ✅ |
| **删 `signed_power`** | **2.75** | **1.42** | **2.58** | **0.7455 ❌** |

**两条结论**
1. **幂次 2.5 是 IS 最优点**（S/F/2Y 同时最高）；prod 在 2.5–4.0 区间基本平坦（0.6916–0.6926）。
2. ★★ **`signed_power` 是「压 prod 的核心算子」**：删掉它虽使 IS 全面变好（S 2.75 / F 1.42 / 2Y 2.58），
   但 **prod 从 0.69 冲到 0.7455 ⇒ 硬闸失败**。⇒ **该结构下 `signed_power` 不可压缩**（「算子最少」目标在此止步）。
   机制：幂次放大信号极端值 ⇒ 持仓更集中 ⇒ 与 book 同族 alpha 的持仓重叠下降。

### 3.3 其余压缩尝试（均失败，故不采纳）
| 尝试 | 省算子 | 结果 |
|---|---:|---|
| 删 `signed_power`（6 ops） | −1 | S 2.75/F 1.42 但 **prod 0.7455 ❌** |
| `signed_power(rank(...))` 换外层（7 ops） | 0 | S 2.48 / F 1.20（无增益） |
| `rank(F)` 替代 `rank(ts_mean(F,2))` | −1 | TO 升、S 降 |
| 窗 (3, 252) | 0 | **robust 掉闸** |
| 窗 (2, 126) | 0 | prod **0.7023 ❌** |
| `winsorize(std=3)` 包裹 | +1 | **no-op**（不采纳） |

---

## 四、终验

| alpha | 模拟层 | PROD | SELF | 互相关 |
|---|---|---|---|---|
| `786pLKnb` | 13 条 checks，FAIL 0 | 0.6171 ✅ | 0.1753 ✅ | 0.0947 |
| `LL5VwgO1` | 17 条 checks，**FAIL 0 / WARNING 1**（仅 MATCHES_THEMES 信息项） | **0.6926 ✅** | **−0.0114 ✅** | 0.0947 |

⇒ 两条腿 **完全独立**（`max_mutually_below_subset_size = 2`），均可提交。

---

## 五、设置层（表达式冻结后未改动）

两颗均为：`TOPCS1600 / SUBINDUSTRY / delay 1 / **decay 1** / truncation 0.08 / nanHandling ON / maxTrade OFF`。
> ⚠ 注意：区域 `settings.json` 声明 `decay 4 / maxTrade ON`，但两条腿的实证最优档均为 **decay 1 / maxTrade OFF**
> （decay 4 会使 Fitness 掉闸）——复现或重跑时必须拉其自身 settings。

---

**本轮零提交**（`786pLKnb` 的 ACTIVE 状态系既往流程/用户提交所致）；`LL5VwgO1` 仅仿真，提交权归用户。

---

## 六、提交执行记录（2026-10-14，用户明确确认后）

### 6.1 提交对象选择：**优先价值最大者**

| # | alpha | S | F | TO | 2Y | returns | PROD | 提交前状态 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `786pLKnb` | 1.71 | 1.09 | 0.1124 | 1.78 | 5.07% | 0.6171 | **已 ACTIVE**（2026-10-12 提交） |
| 2 | ★**`LL5VwgO1`** | **2.64** | **1.27** | 0.3774 | **2.07** | **8.71%** | 0.6926 | UNSUBMITTED |
⇒ 价值最大且待提交 = **`LL5VwgO1`** ⇒ 本次提交对象。

### 6.2 提交链执行（skill `worldquant-submit-alpha`）

| 步骤 | 动作 | 结果 |
|---|---|---|
| 前置 | `submit_verdict` 非 BLOCKED（Failed RA = 0）；prod 0.6926 < 0.7；用户明确确认；配额 `regular 0/4` | ✅ |
| 前置 | 稳健性台账 `robustness_LL5VwgO1` 无记录 ⇒ 先跑逐年统计 | ✅ 逐年 Sharpe **1.81–4.56 全正** ⇒ 落盘 `verdict=PASS` |
| 步骤 1 | 预检 `confirm_submit=False` | ✅ `passed=true / blocked=false / failed_ra=0 / robustness PASS` |
| 步骤 2 | 提交 `confirm_submit=True` | ⚠ 两次回执 **`fetch failed`**（客户端传输假象） |
| 步骤 3 | **核验 `get_alpha_details`** | ★ **`status=ACTIVE`，`dateSubmitted=2026-10-13T21:12:41-04:00`** |

### 6.3 ★ `fetch failed` 铁律再次得到验证（**第 3 次**）

两次 `workflow_submit_alpha(confirm_submit=True)` 均返回 `MCP ... fetch failed`，但：
- **属性已写入**（`name=EUR_R_techindirankprod_01`、`color=BLUE`、`tags` 齐全）⇒ 节点已执行到 `set_properties`；
- 等待一个 flip 窗口（240 s）后 **`status` 翻为 `ACTIVE`**。

⇒ **再次确认：提交/不可逆类动作的报错一律不得据以补发，必须以 `get_alpha_details` 的 `status` + `dateSubmitted` 为准。**

### 6.4 提交后属性与点塔

```
alpha_id      = LL5VwgO1
name          = EUR_R_techindirankprod_01
color         = BLUE（提交态默认，GREEN 须由 OS 挣得）
tags          = [CH_REG, SRC_techindi_model, W549, EXPRFAM_rankprod]
status        = ACTIVE
dateSubmitted = 2026-10-13T21:12:41-04:00
```
**金字塔（`campaign_intel.py pyramid --region EUR --delay 1`）**

| 塔 | alphaCount | 倍率 | 缺口 |
|---|---:|---:|---:|
| **other** | **1** ← 本次 +1 | 1.5 | 差 2 |
| **analyst** | **1** ← `786pLKnb` | 1.3 | 差 2 |
| 其余 12 类 | 0 | 1.0–1.2 | 差 3 |

### 6.5 EUR 最终交付（两条独立腿，均已提交生效）

| # | alpha | 数据集（塔） | S | F | 2Y | returns | 状态 |
|---|---|---|---:|---:|---:|---:|---|
| 1 | `786pLKnb` | analyst_factor_signals（**analyst**） | 1.71 | 1.09 | 1.78 | 5.07% | **ACTIVE** |
| 2 | `LL5VwgO1` | techindi_model（**other**） | **2.64** | **1.27** | **2.07** | **8.71%** | ★ **ACTIVE** |

⇒ 两腿互相关 **0.0947** ⇒ 完全独立；**EUR 由 0 塔点亮 → 2 个类别各 1 颗**。

---

## 七、补充：`786pLKnb` 的通道问题与新腿尝试（2026-10-14 下午）

### 7.1 `786pLKnb` 实为 **PPA（Power Pool）通道**

```
status = ACTIVE     dateSubmitted = 2026-10-12T20:32:17-04:00
tags   = ['PowerPoolSelected']         ← PPA 通道标记
checks 含 POWER_POOL_CORRELATION       ← PPA 专属检查项
submit_verdict → ALREADY_SUBMITTED（退出码 11，附言「请勿重复 POST」）
```
⇒ 按项目口径（**RA 是唯一可接受通道；PPA 一律不算数**），**该提交不算数**。

### 7.2 ★★★ 新铁律：PPA 提交「不占 self 池、**但占 prod 池**」

为验证「能否用 RA 通道重提同一腿」，造了 3 个 analyst 腿兄弟（wave551）：

| alpha | S | F | TO | 2Y | **SELF** | **PROD** |
|---|---:|---:|---:|---:|---:|---:|
| `mLYpM8Z2`（power 2.8） | 1.72 | 1.09 | 0.1114 | 1.78 | **0.1837 ✅** | **0.9994 ❌** |
| `rKdYvoAj`（power 3.2） | 1.71 | 1.09 | 0.1132 | 1.77 | **0.1671 ✅** | — |
| `58jxowM5`（窗 66） | 1.69 | 1.07 | 0.1128 | 1.73 | — | — |

- 兄弟与 `786pLKnb` 的互相关 = **0.9995**（同一腿）
- 但 **SELF 仅 0.18** ⇒ 证实 **PPA alpha 已被平台从 SELF 池剔除**
- 而 **PROD = 0.9994** ⇒ **PPA alpha 仍在 PROD 池中**
- ⇒ ★ **「PPA 不占 self」≠「该腿可再走 RA」**：**prod 池照样锁死**。
- ⇒ **实操判据：判断某腿能否改走 RA，必须实测 `prod`，不能只看 `self`。**

**结论：analyst 腿已被 PPA 提交永久占用，不可改走 RA。**

### 7.3 新腿尝试（全部判死）

| 波 | 数据集 | 机制 | 结果 |
|---|---|---|---|
| 550 | `dl_riskfree_returns` | 单分位（`probability_label1_2quantile_60day` 等 8 种） | ❌ S 0.18–1.37、2Y 全 DEAD ⇒ 天花板 1.40 < 所需 1.81 |
| 552 | `insider_trx_matrix`（αC **37**，最低拥挤） | 买卖 USD 比率 ×3 + 双窗秩乘积 + 平滑 | ❌ S −0.85~−0.14、**TO 0.88–1.67 爆炸** |
| 552 | `other315`（OTC FX 期权） | call/put 比率 / put 水平 | ❌ S 0.09–0.16、2Y = 0 |

### 7.4 当前 RA 口径交付

| # | alpha | 数据集（塔） | S | F | 2Y | returns | 通道 | 算数？ |
|---|---|---|---:|---:|---:|---:|---|---|
| 1 | ★`LL5VwgO1` | techindi_model（**other**） | **2.64** | **1.27** | **2.07** | **8.71%** | **CH_REG (RA)** | ★ **是** |
| 2 | `786pLKnb` | analyst_factor_signals（analyst） | 1.71 | 1.09 | 1.78 | 5.07% | CH_PPA | ❌ 否（且不可改走 RA） |

⇒ **RA 口径下 EUR 累计 1 颗**；要凑第 2 条 RA 腿**必须拓新数据集**（现有 23 个已探数据集的空间已见底）。
