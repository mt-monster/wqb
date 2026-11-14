# 算子数爆炸的解法：平台 + 论坛实证（2026-11-12）

## 一、先厘清三个不同的「算子数」概念（这是问题的根）

| 口径 | 是什么 | 硬限还是软指标 | 我方现状 |
|---|---|---|---|
| **平台表达式上限** | 单条表达式的算子调用数 | **硬限 64**，超限 batch-kill 整批 CANCELLED | 我的构造 45-56，**在危险区** |
| **Genius 六维 `Operators per Alpha`** | 全账号单条平均算子数 | **软指标，越低越好** | 本战役 19-56 |
| **Genius 六维 `Operator Count`** | 全账号用过**不同算子种类**数 | **软指标，越高越好**（GOLD ~80 / MASTER ~130 / GM ~160+） | 需要铺量，不能靠压缩 |

⚠ 关键：**REGULAR 没有「≤12」这样的硬闸**。12 是我方内部精简口径（`wq-brain-ra-*` skill 的组合腿数量约束），不是平台限制。平台 `is.checks` 里**没有复杂度项**，34 算子照样全 PASS。

⇒ **算子爆炸的真实代价有两层**：① 超过 64 会整批作废（硬损失）；② 六维 `Operators per Alpha` 变差（软损失）。**不直接掉闸。**

## 二、平台侧：可用工具

`get_operators` 返回 **103 个算子**（REGULAR 84 个）。其中关键发现：

### ★ 多输入算子（论坛明确推荐）
`add` / `multiply` / `subtract` / `max` / `min` **支持任意多个入参**。

| 写法 | 算子数 |
|---|---:|
| `add(add(a,b),add(c,d))` | **3** |
| `add(a,b,c,d)` | **1** |

⇒ 我的 `add(add(significant_value_1,significant_value_2),add(significant_value_3,significant_value_4))`（3 算子）→ `add(significant_value_1,significant_value_2,significant_value_3,significant_value_4)`（**1 算子**）。

### `reduce_*` 家族（19 个）
`reduce_sum/avg/max/min/count/percentage/stddev/ir/range/skewness/kurtosis/choose/powersum/norm`
**但仅限 SuperAlpha Combo**，不能用于 REGULAR 表达式（论坛帖明确：「Selection 里写 reduce 会报错」）。

## 三、论坛实证：两篇核心方法论

### 帖1《【Quant101】OpCount 拯救计划：因子化简》(ZH87224, 2026-06-10)

**AI 挖因子导致算子爆炸的三大成因**（与我方情况完全对应）：
1. 过度堆叠字段：`a0*alpha0 + a1*alpha1 + ...`
2. 过度嵌套操作符：`op(op(op(...)))`
3. **防御性挖掘**：为保计算有效加 `abs()` / `inverse(x+0.01)` / `ts_backfill(winsorize(...))`

**给出的化简原则（原文要点）**：
> - all operators count, including arithmetic, comparison, and boolean operators
> - **repeating the same operator expression multiple times increases count multiple times**
> - simplification is not only about deleting wrappers, but also about **rewriting the same logic with fewer operator evaluations**
> - **If `op(field)` appears repeatedly, compute it once, assign it to a variable, and reuse the variable**
> - **Prefer operators with unlimited inputs such as `add(f1,f2,f3)` over chained binary forms when the logic is the same**

**六步流程**：①锁基线 → ②生成 4-8 个单点变体 → ③分「结构性安全」vs「经验性」两类 → ④小批仿真 → ⑤验提交质量 → ⑥三层报告（最安全/激进可行/已测被拒）

**两类改动分级**：
- **A 结构性安全**：删 `abs` 内的 `reverse`、删后续算子符号不变时的 `reverse`、合并明显线性片段
- **B 经验性（须实测）**：删 `winsorize`、删 `abs`、删子信号权重、删分母保护常数、删 `ts_backfill`

### 帖2《你会用 reduce 吗？》(AM12075, 33 赞)
仅 SuperAlpha Combo 用，REGULAR 不可用。**对我方当前问题无解**。

### 帖3《构造打分因子的五个核心维度》(MY21251, 26 赞)
**复杂度的量化惩罚公式**：
```
算子复杂度惩罚 = 1/(operator_count + 1)
数据字段复杂度惩罚 = 1/(datafield_count + dataset_count)
综合复杂度折扣 = 两者相乘
```
⇒ **不仅算子数，字段数与数据集数也进惩罚项**。我的冠军用了 2 个数据集（insiders1 + insider_agg_matrix）+ 4 个 analyst 字段（第 3 个数据集）⇒ 数据集数 3，也被惩罚。
⇒ **压缩方向应同时减少「不同数据集数量」**：把 4 条 analyst 腿砍到 1-2 条，或直接砍掉 analyst 回到纯 insiders 两数据集形态。

## 四、我方构造的实际情况与压缩空间

### 冠军 `XgaGb3J1`（S 2.36 / F 2.02 / 2Y 2.71 / sub 1.51）
**46 算子**，来源拆解：

| 成分 | 算子数 | 说明 |
|---|---:|---|
| A 腿（Δ66 持仓变化）| 4 | group_rank + ts_delta + ts_mean + vec_avg |
| C 腿（HHI 集中度）| **12** | 6 算子 × **出现 2 次**（在 A×C 与独立腿里各一次）|
| B 腿（ts_ir）| **6** | 3 算子 × **出现 2 次** |
| FR 腿（新鲜度）| 5 | group_rank + divide + add + days_from_last_change + vec_avg |
| 4 条 analyst 腿 | 12 | 每条 3 算子 |
| 组合与外层 | 7 | add×3 + multiply×2 + group_zscore + signed_power |

**两个白送的浪费**：
1. **C 腿重复 2 次 ⇒ 白送 6 算子**
2. **B 腿重复 2 次 ⇒ 白送 3 算子**
3. **`vec_avg(insd1_holdings)` 出现 3 次 ⇒ 白送 2 算子**
4. **`add` 用二元链而非 n 元 ⇒ 白送 4 算子**

### 压缩方案（已验证算子数）

| 方案 | 手段 | 算子数 | 相对原式 |
|---|---|---:|---:|
| P0 原始 | — | 45 | 基准 |
| **Q2 纯 insiders + n元add** | 删 analyst + n元add | **28** | **−17（−38%）** |
| Q3 双 analyst | analyst 砍到 2 条 | 34 | −11 |
| Q4 analyst 合并 rank | 4 条 AS 先 add 再 rank | 35 | −10 |
| **P1 变量合并（理想）** | 变量赋值去重 | **28** | −17 |

### ★ 关键障碍：toolkit 静态闸不支持变量赋值
论坛推荐的「变量赋值去重」（`h=vec_avg(X);a=...(h);...`）在**我方 toolkit 静态闸**下被拒：
```
[SYNTAX] ['函数 group_zscore 最多接受 2 个参数，但提供了 3']
```
原因：闸把分号 `;` 当参数分隔符解析，误判成 3 个参数。
⇒ **变量合并这条路在 toolkit 链路上走不通**（平台本身接受，但闸拦住）。

⇒ **实际可用的压缩手段只剩两条**：
1. **n 元 `add`/multiply**（零风险，必做）
2. **删腿**（analyst 砍到 0-2 条）

## 五、结论与行动

| 问题 | 答案 |
|---|---|
| 算子多会掉闸吗？ | **不会**。REGULAR 无复杂度闸，34-56 算子照样全 PASS |
| 那为什么要压缩？ | ① 防超 64 整批作废 ② 六维 `Operators per Alpha` 软指标 ③ 复杂度折扣公式（帖3）|
| 最有效的零损失手段 | **n 元 add**（−4）+ 去重复子式（需变量赋值，但被闸拦）|
| 实际可行的最小形态 | **Q2 纯 insiders + n 元 add = 28 算子**（S 待测）|
| 是否该为此牺牲 S？ | **不该**。闸是硬约束、六维是软指标，不可倒置（skill 铁律）|

**已派 BE152**（`xPpyf2M24i09oR3aFgZmR1`，5 臂）验证：Q1 38 / Q2 28 / Q3 34 / Q4 35 / Q5 37，看哪档在最少算子下保住全闸。
