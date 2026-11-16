# 算子压缩第二轮：36 → 27 ops（多参算术 + 三个 no-op 发现）

- 对象：`1YWnZ9rK`（DEU / TOP500 / D1 / decay 0 / SUBINDUSTRY / trunc 0.08），起点 **36 ops**
- 结果件：**`oma9apvk`** — **27 ops / 12 distinct**，指标与 36 ops **逐位相同**
- 时间：2026-11-16 11:1x　｜　全部 UNSUBMITTED，零 POST

## 一、结论先行

| 版本 | operatorCount | distinct ops | Sharpe | Fitness | Turnover | sub | 2Y | ΔT1 | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| `1YWnZ9rK` 原式 | 36 | 14 | 2.64 | 2.17 | 18.39% | 1.72 | 2.86 | +0.0248 | 被取代 |
| `58JqE0kk` 摊平 + 删 group_zscore | 27 | 13 | 2.64 | 2.17 | 18.39% | 1.72 | 2.86 | +0.0222 | 过渡 |
| **`oma9apvk` 再消 reverse** | **27** | **12** | **2.64** | **2.17** | **18.39%** | **1.72** | **2.86** | **+0.0196** | **采纳** |
| `2r5n57pZ` ts_ir→ts_mean | 26 | 11 | 2.30 | 1.85 | 17.11% | 1.55 | 2.03 | — | 拒 |
| `gJaoeM50` analyst 4 rank 合并 | 25 | 13 | 1.80 | 1.37 | 14.39% | 1.12 | 2.36 | — | 拒 |
| `O0W5A8k1` bucket→sector | 25 | 12 | 2.36 | 2.07 | 16.05% | 1.58 | 2.63 | — | 拒 |
| `pwa1d1Eo` 删 cap 分桶 | 24 | 11 | 2.36 | 2.07 | 16.05% | 1.58 | 2.63 | — | 拒 |

**净收益：operatorCount −25%（36→27）、distinct −14%（14→12），指标零损失，全闸 PASS。**

## 二、新机制（三条，全部可复用）

### 1. 多参算术只计 1 个算子（平台实证）

官方 catalog 自相矛盾：`multiply(x, y, ..., filter=false)` 带 `...`，而 `add(x, y, filter=false)` **没有 `...`**，
只有描述写 "Adds two or more inputs element wise"。文档不可信，用探针实测：

```
add(rank(close), rank(volume), rank(cap))   ->  regular.operatorCount = 4
```

即 3 个 rank + **1** 个 add。⇒ `add/multiply/subtract/max/min` 多参均按 1 次调用计，
嵌套求和可**整层摊平**（加法结合律，指标逐位不变）。本地 `op_arity` 对该写法报 PASS，不误杀。

本轮用法（−8）：
- `add(add(sv1,sv2), add(sv3,sv4))` → `add(sv1,sv2,sv3,sv4)`　−2
- 把子层 `an` 的 3 个 add 整个摊进 `core`，`core` 变成 8 参 add，7 个 add → 1 个　−6

### 2. `group_zscore(x, market)` 是纯 no-op（−1）

`market` 只有 1 个组 ⇒ 单组 zscore = 全截面仿射缩放（减均值、除标准差），
被平台建仓的 `scale()` 归一化**完全抵消**。删除后 S/F/TO/returns/DD/long-short/pnl **逐位相同**。

### 3. `reverse` 可消，且这是唯一能降 distinct 的改动（−1 distinct）

`reverse(x)` = `−x`，外层 `group_rank` 保序 ⇒ `group_rank(reverse(x), g) ≡ 1 − group_rank(x, g)`。
该腿是加性组合的一项，用**三参 `multiply`**一次调用同时补回符号：

```
multiply(gri, group_rank(reverse(days_from_last_change(v)), sector))          # 3 ops, 含 reverse
  ->  multiply(gri, add(group_rank(days_from_last_change(v), sector), -1), -1) # 3 ops, 无 reverse
```

指标逐位相同，distinct 13→12。

## 三、承重件 vs no-op（防止后续误删）

- **承重**：`bucket(rank(cap), range="0,1,0.1")` 的**规模十分位**中性化（删掉 S 2.64→2.36，−0.28）；
  `ts_ir(v,66)`（换 `ts_mean` S→2.30，−0.34）；analyst 的 **4 个独立 `rank`**（合并成 1 个 S→1.80，−0.84）。
- **no-op**：`group_zscore(·, market)`（逐位相同）、`group_neutralize(core, sector)`（与完全不做中性化 S 完全相同 2.36）。

## 四、最终表达式（`oma9apvk`，27 ops / 12 distinct）

```
v = vec_avg(insd1_holdings);
tot = add(significant_value_1, significant_value_2, significant_value_3, significant_value_4);
grm = group_rank(ts_mean(divide(significant_value_1, tot), 66), sector);
gri = group_rank(ts_ir(v, 66), sector);
leg1 = multiply(group_rank(ts_delta(ts_mean(v, 66), 66), sector), grm);
leg2 = multiply(gri, add(group_rank(days_from_last_change(v), sector), -1), -1);
core = add(leg1, leg2, grm, gri,
           rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5)),
           rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 22)),
           rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)),
           rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22)));
group_neutralize(core, bucket(rank(cap), range="0,1,0.1"))
```

distinct 12：`vec_avg · add · divide · ts_mean · group_rank · ts_ir · ts_delta · multiply · days_from_last_change · rank · group_neutralize · bucket`

**判定为本骨架下限**：再减任何一种都要付 S（见上表），或需引入新算子种类（净零）。

## 五、六维影响

| 项 | 值 |
|---|---|
| T1（avg distinct ops/alpha） | 4.6074 → 4.6270，Δ **+0.0196**（原 36 ops 版为 +0.0248，改善 0.0052） |
| T2（avg distinct fields/alpha） | 1.8488 → 1.8677，Δ +0.0189（与算子压缩无关，字段数未变） |
| T3（total distinct ops） | **better**：新引入 `days_from_last_change`（+1） |
| T4（total distinct fields） | **better**：新引入 `significant_value_1..4`（+4） |
| T5 / T6 | n/a（streak 靠每日仿真、community 靠论坛，与选件无关） |

⚠ **两口径务必分开报**：多参摊平降的是 `operatorCount`（调用次数），
官方 tiebreak T1 数的是**去重算子种类** ⇒ 摊平不降 T1。本轮 T1 的 −2 全部来自
`group_zscore` 与 `reverse` 两个**种类**的消除。

## 六、Python Alpha 实证（结论：本件不可移植，且不是 T1 杠杆）

1. **可用性 ✅**：探针 `e7aq5NJg` 在 DEU/TOP500/D1 成功仿真（Python alpha 在本账号可跑）。
2. **硬限制 ❌**：官方文档 `how-translate-fast-expression-alpha-python-alpha` 原文 —
   "Only **MATRIX** fields load. **VECTOR fields**, the GLB region, and multi-sim are **not supported**."
   ⇒ `vec_avg(insd1_holdings)` 这条腿无法移植，本件不能直接转 Python。
3. **`regular.operatorCount = None`**（实测）：官方六维文档只写 T1 = "Avg distinct Operators/Alpha"，
   **未说明 operatorCount 为 null 的 Python alpha 如何计入**。按常规实现（None 无法求和）大概率被**跳过**
   ⇒ T1 收益**无法证实，倾向为零**。

**建议**：Python alpha 的价值在 PAC2026 赛道与 ML/聚类类新信号，不在算子数优化；
若要试，应**从零构造纯 MATRIX 字段**的新 alpha，而不是移植本件。
