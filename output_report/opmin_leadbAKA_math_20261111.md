# `leadbAKA` 数学等价替换 / 5-ops 可达性 / Python alpha 评估（2026-11-11 20:0x）

> **只挖不提交**，本轮零提交。

## 0 三问三答

| 问题 | 答案 |
|---|---|
| 还能做算子等价替换吗？ | ✅ **能**：找到 2 条严格恒等式，把交付件 **9 → 8 ops**，指标与 prod 逐位相同 |
| 能压到 5 个以下吗？ | ❌ **不能**（在保信号 + 保全闸的前提下）。代数下界 = **8 ops**；7-ops 三条路径实测全部掉闸 |
| Python alpha 可行吗？ | ⚠️ **平台支持，但不是压缩手段**：实测 `language=PYTHON` 的 REGULAR alpha `58Jx76xX` 存在且 `operatorCount = None`。这是**计量口径消失**，不是信号变简单；且引入语义等价风险与 MultiSim 禁令 |

**新交付件 `2r5MqmVJ`（8 ops）**
```
a = ts_mean(overall_sentiment_score, 66);
m = ts_mean(likelihood_of_neutral_tone, 66);
k = ts_corr(a, m, 252);
group_neutralize(ts_zscore(multiply(a, subtract(add(k, 2), m)), 378), industry)
```

---

## 1 严格数学推导

基准 `88NbAJnl`（9 ops），记：
- `S` = `overall_sentiment_score`，`P` = `likelihood_of_neutral_tone`
- `a = ts_mean(S,66)`
- `b = 1 − P`
- `c = ts_mean(b,66)`
- `ρ = ts_corr(a,c,252)`
- `x = a·(c + 1 − ρ)`
- `out = group_neutralize(ts_zscore(x,378), industry)`

### 恒等式 I1（时序均值线性）

`ts_mean(1 − P, W) = 1 − ts_mean(P, W)`

令 `m = ts_mean(P,66)`，则 `c = 1 − m`。平台 `nanHandling=ON` 下常数与缺失填充均保持线性；实测逐位成立。

### 恒等式 I2（Pearson 相关的仿射不变性）

`ts_corr(u, α + βv, d) = sign(β)·ts_corr(u,v,d)`（β≠0，窗口内方差非零）

`c = 1 − m` ⇒ β = −1 ⇒ **`ρ = −k`**，其中 `k = ts_corr(a,m,252)`。
这条把「先造 `1−P` 再做均值」两步压成一步，并消掉一次 `subtract`。

### 代入

```
c + 1 − ρ = (1 − m) + 1 − (−k) = 2 − m + k
x = a·(2 − m + k)
```

**M1**：`multiply(a, subtract(add(k, 2), m))` = `a·(k + 2 − m)` ⇒ **严格等价**，算子 9→8。

### ★ 常数 2 为什么不能被 `ts_zscore` 吸收（关键反直觉点）

`ts_zscore(x + c₀, W) = ts_zscore(x, W)` 对**常数** `c₀` 成立，`group_neutralize` 同理。
但这里常数在外层 `multiply` **之内**：

`a·(2 − m + k) = 2a − a·m + a·k`

其中 `2a` 随 `a`（随股票、随时间）变化，**不是常数** ⇒ 删掉 2 会改变信号，而非只平移。
实测：把 `add(k,2)` 换成 `subtract(k,m)`（即删 2）→ `A1x9Jvpl` **S 1.74→0.41、F 1.03→0.12、2Y 1.91→0.28**，全崩。
常数换成 1 或 3 也不等价（S 掉到 1.34 / 2Y 掉到 1.80）⇒ 2 是结构性常数。

### 其它两条等价改写（同 9 ops，作为恒等式的独立验证）

- `add(multiply(a, subtract(c,ρ)), a)` = `a(c−ρ) + a` = `a(c+1−ρ)` (**分配律**，逐位相同）
- 仅用 I1（`c = 1 − ts_mean(P,66)`，ρ 仍作用于 c）⇒ 逐位相同

---

## 2 代数下界：为什么 5 ops 不可达

保留全部信号内容所需的最小算子结构：

| 层 | 必需算子 | 数量 |
|---|---|---:|
| L3 时序统计（三个独立量） | `ts_mean(S,66)` = a、`ts_mean(P,66)` = m、`ts_corr(a,m,252)` = k | **3** |
| L1 三元线性组合 + 相乘 | `2 − m + k` 至少 2 个二元算术（`add(k,2)` + `subtract(·,m)`），再 `multiply(a,·)` | **3** |
| L4/L3 输出层 | `ts_zscore(·,378)` 时序标准化 + `group_neutralize(·,industry)` 截面去均值（数学上不可交换、不可合并） | **2** |
| 变量赋值 | `a/m/k` 赋值本身不计数（已实证） | 0 |
| **合计** | | **8** |

`ts_zscore` 与 `group_neutralize` 不可交换：先做截面去均值会改变每只股票自身的历史均值/标准差，从而改变时序 z-score；也不存在单算子同时做时序标准化 + 组内去均值。

要到 ≤5 必须砍掉 ≥3 个算子，只有两条路：
1. **砍掉整条 corr 腿**（−1 时序 + 2 算术 = −3 ⇒ 5 ops）：批 B 实测 `MP6OwzpM` S 1.51 / F 0.85 / 2Y 1.51 **FAIL**，且这双腿正是把 prod 从基线 0.8078 压到 0.674 的关键，删了 prod 回墙。
2. **砍输出层 2 个 + 任意 1 个**：批 C 实测 `kqadkgAP`（删 zscore，7 ops）S 1.00 / F 0.52；`d5ap81GJ`（删 group，7 ops）S 1.44 / F 0.85 / 2Y 1.27 ⇒ 全掉闸。

⇒ **8 ops 是「全闸通过 + 保留信号」的下界**，5 ops 以下在当前信号上无解。

---

## 3 批 C 实测（10 条，全部 FULL 仿真）

| # | id | ops | S | F | 2Y | sub | CL | 变体 |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | **`2r5MqmVJ`** | **8** | **1.74** | **1.03** | **1.91** | **1.48/0.90** | 1.26 | **M1 严格等价** ✅ |
| 2 | `1YWeVZ3K` | 8 | 1.74 | 1.03 | 1.91 | 1.48/0.90 | 1.26 | M1 分配律写法，逐位相同 ✅ |
| 3 | `gJa6qZNl` | 9 | 1.74 | 1.03 | 1.91 | 1.48/0.90 | 1.26 | 仅 I1，逐位相同 ✅ |
| 4 | `GrmP0O23` | 9 | 1.74 | 1.03 | 1.91 | 1.48/0.90 | 1.26 | 分配律重组，逐位相同 ✅ |
| 5 | `A1x9Jvpl` | 7 | **0.41** | 0.12 | 0.28 | — | 0.04 | **误删常数 2 → 崩塌** |
| 6 | `vRA8n2Eb` | 8 | 1.34 | 0.67 | 1.53 | 1.35/0.70 | 0.98 | 常数改 1 |
| 7 | `P05NrgVq` | 8 | 1.73 | 1.03 | 1.80 | 1.46/0.90 | **1.31** | 常数改 3（CL 略升但 2Y 降） |
| 8 | `kqadkgAP` | 7 | 1.00 | 0.52 | 1.11 | 0.78/0.52 | 0.77 | 删 `ts_zscore` |
| 9 | `d5ap81GJ` | 7 | 1.44 | 0.85 | 1.27 | 1.24/0.75 | 1.01 | 删 `group_neutralize` |
| 10 | `gJa6qZnv` | 8 | 1.58 | 0.90 | 1.71 | 1.32/0.82 | 1.24 | `ts_corr` 窗口 504 |

`2r5MqmVJ` prod 复检 = **0.6740**（`passes_check=true`，直方图与 `88NbAJnl` 逐位一致）⇒ 数学等价在 IS 指标与相关性两个层面都成立。

---

## 4 Python alpha：平台实测与判断

### 实测（本轮真的跑了一次）

用 `create_simulation(language="PYTHON", lookback=70, ...)` 派发最小探针 `58Jx76xX`：
- `status=UNSUBMITTED`、`type=REGULAR`、`stage=IS`、`settings.language=PYTHON`
- 有完整 **15 项 `is.checks`**（RA 闸、塔 `EUR/D1/EARNINGS` ×1.2）
- **`regular.operatorCount = None`** —— 平台对 Python 代码**不统计算子数**

⇒ 所以 Python alpha 在本账号**确实可用**（不是纯 Labs 概念），EUR 区可跑，走同一套 RA checks。

### 但它不解决「压到 5 ops」

1. **口径消失 ≠ 信号变简单**：`operatorCount` 变 `None` 只是平台不数 NumPy 调用。要复现同一信号仍需手写 `ts_mean` / `ts_corr` / 严格全窗 `ts_zscore` / `group_neutralize` 四个 helper + typed `store` 缓存（因 `ts_corr` 与 `ts_zscore` 都包装了计算中间量）。代码量远大于 8 行，计算复杂度不降。
2. **六维 `Operators per Alpha` 是 FASTEXPR 口径的软指标**；用 Python 让该指标不计数，属于换计量体系，不是数学压缩。
3. **语义等价风险**：论坛两篇高赞（105 赞 `41032955115927`、35 赞 `41421186876439`）反复警告 `np.nanmean ≠ ts_mean`、严格全窗 `ts_zscore` 覆盖、`store` warm-up 与 FastExpr pre-start 历史不一致 → 指标会偏离。这次要的是「等价替换」，Python 恰恰更难保证等价。
4. **平台限制**：Python alpha **不支持 MultiSim**（本轮 10 条并批的做法不可用）、**GLB 暂不支持**、不支持 VECTOR 字段 / `vec_*`；settings schema 也不同（`nanHandling`/`unitHandling`/`startDate`/`endDate` 不能照搬，需加 `lookback`）。
5. **轨道边界**：本地 `alpha-template-labs-data-analysis/SKILL.md` 明确「RA 流水线只产 FASTEXPR REGULAR，两条轨道产物不能互换」「不能进入提交路径」。Python alpha 即便跑通也是**另一颗 alpha**，不能替换当前候选的提交。

⇒ **结论：不建议为「压算子」而切 Python alpha**。若目标是换轨研究（更自由的信号表达、自定义 stateful 逻辑），可另开一轮，但那是不同任务，且需先解决等价性验证。

---

## 5 最终交付件更新

| 项 | `88NbAJnl`（9 ops） | **`2r5MqmVJ`（8 ops）** |
|---|---|---|
| 表达式 | 原式含 `1−P` 与 `1−ρ` | 用 I1+I2 化简为 `a·(2−m+k)` |
| S / F / 2Y | 1.74 / 1.03 / 1.91 | **逐位相同** |
| sub / CL / TO | 1.48/0.90 / 1.26 / 0.0881 | **逐位相同** |
| prod / self | 0.6740 / 0.2393 | **0.6740**（复检）/ 继承 |
| ΔS | +0.05（`EQUITY:EUR:1`） | 继承 |
| mix | `two_leg` 需三问 | 继承 |
| ops | 9 | **8** ✅ |

按「同等绩效取算子最少」铁律，**`2r5MqmVJ` 取代 `88NbAJnl` 成为交付件**。提交前置不变：补三问、prod `refresh=True`、2019 弱年复核（台账 `robustness_88NbAJnl`=CONDITIONAL 可继承）、三段式属性。

---

## 6 产物与来源

- 报告：`output_report/opmin_leadbAKA_math_20261111.md`
- 批次：`results/wp_leadbAKA_C_20261111.txt`、`results/wp_leadbAKA_batchC_20261111.json`；签核 `results/op_coverage_signoff.jsonl`（+1 条）
- 平台：10 条 FULL 仿真（`2NXlU01NP4GMcgd1bl84Cr1R`）、`create_simulation(language=PYTHON)` 探针 `58Jx76xX`、`check_correlation(production)`、论坛帖 `41032955115927` / `41421186876439`、本地 `Claude/skills/alpha-template-labs-data-analysis/SKILL.md`

**本轮零提交、零平台写操作**（仅新增 1 条 Python 探针仿真 + 10 条回测）。
