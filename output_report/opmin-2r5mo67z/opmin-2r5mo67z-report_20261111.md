# op-min 压缩报告 — `2r5MO67Z`（DEU / TOP500 / D1）

执行时间：2026-11-16 11:20 (GMT+8)｜skill `wq-alpha-gate-push-op-min`｜3 轮 / 14 条仿真 / 零提交

## 一、最终推荐：`1YWnZ9rK`（36 算子，指标全维更优）

```text
v = vec_avg(insd1_holdings); s1 = add(significant_value_1, significant_value_2); s2 = add(significant_value_3, significant_value_4); tot = add(s1, s2); r = divide(significant_value_1, tot); m = ts_mean(r, 66); grm = group_rank(m, sector); iri = ts_ir(v, 66); gri = group_rank(iri, sector); leg1 = multiply(group_rank(ts_delta(ts_mean(v, 66), 66), sector), grm); leg2 = multiply(gri, group_rank(reverse(days_from_last_change(v)), sector)); an = add(add(rank(ts_mean(predicted_surprise_f12m_ebitda_4, 5)), rank(ts_mean(predicted_surprise_pct_fy2_earnings_4, 22))), add(rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4, 5)), rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3, 22)))); core = add(add(add(add(leg1, leg2), grm), gri), an); group_zscore(group_neutralize(core, bucket(rank(cap), range="0,1,0.1")), market)
```

| 维度 | 原件 `2r5MO67Z` | `1YWnZ9rK` | 变化 |
|---|---|---|---|
| **operatorCount** | **50** | **36** | **−14（−28%）** |
| Sharpe | 2.63 | **2.64** | +0.01 |
| Fitness | 2.13 | **2.17** | +0.04 |
| Turnover | 19.70% | **18.39%** | −1.31pp |
| Returns | 12.95% | 12.47% | −0.48pp |
| Drawdown | 4.74% | 5.06% | +0.32pp |
| Margin | 13.15 bp | 13.56 bp | +0.41 bp |
| sub-universe | 1.63 | **1.72** | +0.09 |
| 2Y | 2.94 | 2.86 | −0.08 |
| self | 0.5535 | **0.5487** | −0.005 |
| prod | 0.5534 | **0.5485** | −0.005 |
| 方案 D v2 | pass | **pass**（ΔS +0.04 / ΔF +0.03 / ΔRet +0.10pp / ΔTO +0.20pp / ΔDD −0.02pp） | — |
| 塔 | PV+INSIDERS+MODEL，effective **0** | 同，effective **0** | 不变 |
| distinct ops / fields | 14 / 9 | 14 / 9 | 0 / 0 |

`checks.fail = []`，九项提交测试全 PASS。

## 二、三步压缩账（50 → 36）

| # | 改动 | 省 | 性质 | 实测 |
|---|---|---:|---|---|
| 1 | **重复子式变量合并**（`vec_avg(insd1_holdings)`×4、`group_rank(ts_mean(divide(sv1,...),66),sector)`×2、`group_rank(ts_ir(...),66)`×2、`add(add(sv1,sv2),add(sv3,sv4))`×2） | **−11** | 零损失 | `vRAJrjdG` 50→39，指标**逐位相同** |
| 2 | `group_rank(divide(1, add(days_from_last_change(v),1)),sector)` → `group_rank(reverse(days_from_last_change(v)),sector)` | **−2** | 数学等价 | `O0W5N7od` 39→38，指标**逐位相同**（`1/(d+1)` 与 `−d` 同为严格递减，group_rank 吸收） |
| 3 | 删 `signed_power(·, 1.3)` | **−1** | 有损但更优 | `ZYaWb7ox` 38→37，S **2.63→2.65**、F 2.13→2.16、TO 19.70%→18.66% |
| 4 | 外层 `group_zscore(·,sector)` 单层（保留 market） | **−1** | 有损但更优 | `1YWnZ9rK` 37→**36**，S 2.65→2.64、F 2.16→**2.17**、TO 18.66%→**18.39%**、sub 1.67→**1.72** |

## 三、试过但否决（各有硬理由）

| 改动 | 省 | 结果 | 否决理由 |
|---|---:|---|---|
| `core = add(add(leg1,leg2), an)` 删两个独立项 | −2 | `KPgwr0W1` S **2.38**（−0.26）、DD 7.02% | 指标跌幅远超 2 个算子的六维收益（单颗权重 1/378） |
| analyst 4 腿 → 2 腿 | −6 | `1YWnXwg6` S **1.97**、sub 1.28 vs 线 1.25 | sub 余量只剩 +0.03，是唯一贴线闸，不划算 |
| `bucket(rank(cap))` → `sector` / `industry` | −2 | `XgaYJQjX` / `0mPKr3bq` S 2.36、**pyramid effective 0→2** | **self 从 0.549 涨到 0.671/0.678**（距 0.7 仅 0.02）；且 ΔS 仅 +0.01 ⇒ 触发分散度软闸（self≥0.55 ∧ ΔS<+0.02）；更关键**塔实际边际 = 0**：DEU 当期 INSIDERS=1（交后 2，不到 3）、MODEL=3（已亮），两席都不新点亮 |
| `bucket(rank(cap))` → `bucket(rank(v / ts_mean(v,66) / iri))` | −1 | `78YK6nPb` S **−0.15**、`mLax6Vn9` S 0.70、`A1xOv7Xd` S **−0.07** | `vec_avg(insd1_holdings)` 太稀疏，bucket 后组极不平衡，TO 飙到 27–51% ⇒ 方向封死 |

## 四、关键机制发现（本次新增，已入记忆）

1. **`bucket(rank(cap))` 里的 `cap` 属于 PV 数据集** —— 这是本件 pyramid 从 `INSIDERS+MODEL` 两类被撑成 `PV+INSIDERS+MODEL` 三类、`effective=0` 的**隐形第三类来源**。想救塔必须换掉这个轴，而不是删 analyst 腿（`mean_estimate_change_*` 属 MODEL 不属 ANALYST）。
2. **换掉 cap 轴会让 self 跳升 0.12**（0.549→0.671/0.678）—— 因为 `cap` 十分位提供了一层规模中性化，与某个已提交件（`Vk65zLzG`，相关 0.55→0.68）解耦。**换来 effective=2 的代价是 self 余量只剩 0.02，且撞分散度软闸。**
3. **「effective=2」≠「塔边际 +2」**：必须再对齐 `get_pyramid_alphas` 当期计数。本件两席分别是 1（差 2 颗）和 3（已亮），实际边际为 0。

## 五、状态

全部 14 条变体均为 `UNSUBMITTED`，**零 POST**。原件 `2r5MO67Z` 未改动。提交权归用户。
被压缩取代的中间件（`vRAJrjdG` / `O0W5N7od` / `ZYaWb7ox` / `LLKlN7Ra` 等）建议标 `SUPERSEDED`，仅保留 `1YWnZ9rK`。
