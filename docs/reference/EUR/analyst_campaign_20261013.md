# EUR × Analyst 战役报告

> 2026-10-12 – 10-13 ｜ **21 波 ≈168 条仿真** ｜ 目标：Analyst 类别（未点亮塔）挖 10 颗可提交 regular alpha
> **结论：Analyst 内可提交 = 1 颗**（唯一有效结构已穷尽；互相关实测证明同族只能出 1 颗）

---

## 一、达标候选（`all_passed = True`）—— **已压缩至 4 算子**

```python
signed_power(group_rank(divide(eps_revision_magnitude,
                                ts_mean(eps_y1_estimate_coeff_var, 55)), industry), 3.0)
```
**alpha id：`786pLKnb`**（4 算子；压缩前 `O083qZQp` 为 5 算子）

| 闸 | 值 | 平台线 | 状态 |
|---|---:|---|---|
| Sharpe | **1.71** | 1.58 | ✅ |
| Fitness | **1.09** | 1.0 | ✅ |
| Turnover | **0.1123** | 0.05–0.3 | ✅ |
| IS Ladder Sharpe (2Y) | **1.78** | 1.58 | ✅ |
| Margin | 9.02bp | ≥5bp | ✅ |
| **PROD correlation** | **0.6170** | <0.7 | ✅ |
| **SELF correlation** | **0.1753** | <0.7 | ✅ |
| verdict | **FAIL 0 / WARNING 1**（仅 MATCHES_THEMES 信息项） | — | ✅ |

**经济含义**：**分析师 EPS 修正幅度 ÷ 分析师分歧度**（分歧度取 55 日均值平滑）——
「修正的确定性程度」。分歧度越小而修正幅度越大 ⇒ 该修正越可信 ⇒ 后续价格漂移越强。
对应类别原语 = *revision surprise ÷ dispersion*。

---

## 二、六层杠杆（按增益排序，全部实证）

| # | 杠杆 | 效果 |
|---|---|---|
| ① | **`eps_revision_magnitude ÷ eps_y1 分歧度` 原语** | S 0.71 → **1.32**（+0.61） |
| ② | **分组轴 → `industry`** | industry 1.38 > sector 1.32 > market 1.29 > c5 0.96 |
| ③ | **`target_tvr` 0.06 → 0.18** | **S 与 2Y 同步提升**（S 1.43→1.58、2Y 1.34→1.53） |
| ④ | **分母 `ts_mean` 平滑（窗 55）** | **2Y 1.55→1.81；prod 0.7064→0.6617** |
| ⑤ | **`signed_power` 1.8 → 3.0** | **S/F 提升且 prod 下降**（S 1.67→1.71、F 1.04→1.09、prod 0.6617→**0.6170**） |
| ⑥ | **窗口 55/88 安全，44 是 prod 陷阱**（窗44 prod 0.7064 > 0.7） | — |

**关键机制发现**：
- `ts_mean` 平滑分母 **同时**改善 2Y、降低 prod、保持 S —— 平滑分歧度 ⇒ 分母更稳定 ⇒ 持仓更集中 ⇒ 小宇宙表现改善 + 与存量 alpha 相似度下降
- `signed_power` 幂次 **同时**是 S/F 提升器与 prod 降低器

---

## 三、为何不是 10 颗（互相关实测证据）

`get_mutual_correlation` 对 4 颗达标候选（power 1.8 / 2.2 / 2.4 / 3.0）：

| 对 | 相关系数 |
|---|---:|
| `A1vAYPjR` ↔ `mL6v2dZW` | **0.9993** |
| `mL6v2dZW` ↔ `ZYAJZL93` | 0.9965 |
| `O083qZQp` ↔ `A1vAYPjR` | 0.9950 |
| `O083qZQp` ↔ `ZYAJZL93` | 0.9757 |

⇒ `max_mutually_below_subset_size = **1**`

**提交任一颗后，其余候选的 self 相关性将 >0.7（触发自我相关闸，拒绝）** ⇒ 一个信号族只能出一颗。

差异化尝试亦无效：窗口 88（S 1.68 / 2Y 1.67）与主腿相关仍 ~0.98；窗口 44 / sector / market / subindustry 轴 **2Y 全部不达标**（≤1.50）。

---

## 四、判死清单（21 波 168 条，避免重复投入）

| 方向 | 结果 |
|---|---|
| `revenue_*` / `netprofit_*` 版本（含平滑） | S ≤1.49（差 0.09） |
| `eps_y2_estimate_coeff_var` 作分母 | S 1.45 |
| `eps_y1_estimate_change_3mo`（变化）作分子 | S 0.91 |
| `eps_y*_consensus_value`（预期增速）作分子 | S 负（−0.22 / −0.63） |
| 期限差 `y2_change − y1_change` | S −0.97 |
| `eps_y1_cagr_2yr/3yr` 作分子 | S ≤0.51 |
| `asymmetry` / `volatility_adj_2yr` 作分母 | S ≤0.42 |
| 跨指标 multiply | S 0.11 |
| **`analyst_consensus` breadth（`estimate_count_*`，8 条）** | S ≤0.21 ⇒ 数据集判死 |
| `analyst45`（44 VECTOR） | S 0.36 ⇒ 判死 |
| `analyst9` / `analyst10` 共识水平 | S ≤0.76 |
| sector / market / subindustry 轴 | 2Y ≤1.50 |
| TOP2500 universe | S 崩至 1.34–1.40 |
| decay 4 | S 1.47 |

---

## 五、结论与建议

**Analyst 类别可提交 regular alpha = 1 颗**（`O083qZQp`）。

要凑够 10 颗必须离开 Analyst 类别。可选路径：

| 路径 | 说明 |
|---|---|
| **A** | 把本配方迁移到**其它未点亮类别**（Social Media `socialmedia15` 现有 \|S\|0.88 / Institutions `fund_holdings_panel` 现有 S 0.80）—— 配方（平滑分母 + 高幂次）已被证明能同时提 2Y、降 prod，可能把 0.80–0.88 推到达标线 |
| **B** | 转向**已点亮但素材更多**的类别（Price Volume 108 条回测、Model 156 条） |
| **C** | 接受 1 颗，收尾 |

**建议 A**：配方成熟、迁移成本低，且新类别与 Analyst 腿来源不同 ⇒ 互相关低 ⇒ 每类可各出 1–2 颗，多条腿合起来才可能接近 10 颗。

---
**全程零提交**（`ALLOW_ALPHA_SUBMIT` 未开启；所有 alpha 均为 UNSUBMITTED 状态的仿真产物）。

---

## 六、算子压缩（skill `wq-alpha-gate-push-op-min`，2026-10-13）

### 6.1 结果：**5 → 4 算子，指标与相关性零损失**

| 项 | 原版 `O083qZQp` | 压缩版 **`786pLKnb`** |
|---|---:|---:|
| 算子调用点 | 5 | **4** |
| Sharpe | 1.71 | **1.71** |
| Fitness | 1.09 | **1.09** |
| Turnover | 0.1124 | **0.1124** |
| 2Y | 1.78 | **1.78** |
| Margin | 9.02bp | 9.02bp |
| **PROD** | 0.6170 | **0.6171** ✅ |
| **SELF** | 0.1753 | **0.1752** ✅ |
| verdict | FAIL 0 | **FAIL 0** |

### 6.2 消融明细（逐算子，一次只删一个）

| 删除/替换的算子 | 剩余算子 | S | F | 2Y | 结论 |
|---|---:|---:|---:|---:|---|
| **`ts_target_tvr_decay`** | **4** | **1.71** | **1.09** | **1.78** | ★**无损 ⇒ 采纳** |
| `signed_power` | 4 | 1.49 | 0.88 | 1.86 | ❌ F 掉闸 ⇒ 必需 |
| `ts_mean` | 4 | 1.67 | 1.08 | 1.52 | ❌ 2Y 掉闸 ⇒ 必需 |
| `group_rank` → `rank`（去轴） | 4 | 1.62 | 1.13 | 1.16 | ❌ 2Y 掉闸 ⇒ 必需 |

⇒ **4 个算子是结构下限**（每个删除都会导致某闸失败）。

### 6.3 新铁律（已写入 skill `op-compression.md` C15）

**`ts_target_tvr_decay` 在「自然换手 < `target_tvr`」时是 NO-OP。**
本候选自然 TO = 0.112 < 目标 0.18 ⇒ 限速器从未激活 ⇒ **可无损整删，省 1 算子**。
⚠ 删前必须先看自然 TO：若 `TO > t` 则限速器会激活，删除将同时改变 TO 与 S。

### 6.4 设置收敛（表达式冻结后，不占算子）

| 设置 | 取值 | 依据 |
|---|---|---|
| universe | TOPCS1600 | TOP2500 使 S 崩至 1.34–1.40 |
| neutralization | SUBINDUSTRY | 换 MARKET 使 S −25%（成立条件） |
| delay / truncation | 1 / 0.08 | truncation 零杠杆 |
| **decay** | **1** | decay=4 使 S 1.71→1.58、F 1.09→0.97（掉闸） |
| nanHandling / maxTrade | ON / OFF | 与本区 win 设置一致 |

### 6.5 同族变体处置

`O083qZQp`(5 ops) / `A1vAYPjR` / `mL6v2dZW` / `ZYAJZL93` 全部标 **SUPERSEDED**
—— 同骨架互相关 0.976–0.999，按纪律**只保留指标最好且算子最少的那 1 个 = `786pLKnb`**。

### 6.6 入队

已写入 `results/mining_ledger/alpha_ledger.jsonl`（`id:786pLKnb`，wave `w493`）。

---

# 附章：EUR 未点亮 8 类别【完全穷尽】总表

> 2026-10-12 – 10-13 ｜ **34 波 ≈272 条仿真** ｜ 目标：未点亮类别（不选已点亮塔）挖 10 颗可提交 regular alpha
> **结论：可提交 = 1 颗**（8 类别 100% 穷尽；其余 7 类有明确的数学/结构判死依据）

## 一、最终总表

| 类别 | 最优数据集 | S 上限 | 反推 returns | 判定依据 |
|---|---|---:|---:|---|
| ★**Analyst** | `analyst_factor_signals` | ★**1.71** | **5.07%** | ★**产出 1 颗**（`786pLKnb`，4 算子，全闸+prod/self 通过） |
| Sentiment | `sentiment27` | 1.33 | **5.68%** | S 距线 0.25（returns 够，S 不够；4 次验证均收敛） |
| Imbalance | `imbalance5` | 1.43 | 2.66% | ❌ **2Y = 0.05**（recency 结构性失效）+ returns 不足 |
| Institutions | `fund_holdings_panel` | 0.81 | 2.33% | ❌ returns 不足 ⇒ F 上限 0.68 |
| Macro | `macro27` | 0.54 | 2.27% | ❌ returns 不足 |
| Insiders | `insiders1` | 0.50 | ~0 | ❌ **TO 爆炸 1.52–1.61** + margin ≈ 0 |
| Social Media | `socialmedia15` | −0.03 | — | ❌ **TO 爆炸 1.23–1.33** |
| Earnings | `earnings6` | ~0 | — | ❌ 字段全 NaN（空信号） |

## 二、★★★ 三条通用规律（已沉淀到 skill）

### 1. `returns ≥ 0.05` 是 EUR 可提交的数学硬前提

平台 Fitness 计算式：**F = Sharpe × sqrt(returns / max(turnover, 0.125))**

- 反推公式：**returns = 0.125 × (F / S)²**（可直接从任何回测的 S/F 反算）
- S = 1.58（Sharpe 闸线）时需 **returns ≥ 0.0501** 才能过 F 闸（≥1.0）
- **上表 8 类中仅 2 类的信号 returns ≥ 5%** ⇒ 其余 6 类**无论怎么调算子都不可能过 F 闸**

**⇒ 选集的第一个动作应是**：跑 8 条探针 → 反推 returns → `returns < 5%` 的直接放弃（省掉整轮深挖）。

### 2. 稀疏事件型 VECTOR + `vec_avg` ⇒ TO 爆炸

`insiders1` TO 1.52–1.61、`socialmedia15` TO 1.23–1.33（硬线 0.7）——
事件稀疏 ⇒ 归约后个股间剧烈跳变。

**⇒ 判据：探针若 TO > 0.7 立即放弃该数据集（不必看 S）。**

### 3. 配方与数据集强绑定，不可迁移

`A ÷ ts_mean(B,55)` + `signed_power 3.0` 在 analyst（日频修正 + 稠密分歧度）上有效；
换到情绪评分/持仓数据后要么 TO 爆炸、要么 S 天花板仅 +0.01。

## 三、各杠杆在 EUR 的实测有效性（跨类别汇总）

| 杠杆 | 有效性 |
|---|---|
| `signed_power` 幂次（1.8→3.0） | ✅ **提 S/F 且降 prod**（唯一「三赢」杠杆） |
| `ts_mean` 平滑分母 | ✅ 提 2Y + 降 prod，但**降 returns** ⇒ 需 returns 有余量 |
| 分组轴 `industry` | ✅ industry > sector > market > c5 |
| `target_tvr` | ⚠ 仅当 TO > t 时有效；否则 **no-op 可无损删除**（省 1 算子） |
| **L2 双窗级联** | ❌ sentiment27 上 S 仅 0.32–0.66 |
| 跨数据集组合（16 种） | ❌ 全部 ≤ 单腿 |
| TOP2500 universe / decay 4 / sector·market 中性化 | ❌ S 崩或双降 |
| 稀疏数据上的 `vec_avg` | ❌ TO 爆炸 |

---
**全程零提交**（`ALLOW_ALPHA_SUBMIT` 未开启）。
