# 波 179 · `earnings_sent_matrix` 十模板结构扫描（EARNINGS 塔第 2 颗）

- **区域 / 设置**：USA / **TOP2000** / D1 / `neutralization=INDUSTRY` / `truncation=0.08` / `nanHandling=ON`
  - ⚠ **`decay` 未显式传入**，落到工具默认值 **4**，与 `RREXk770` 的 `decay=0` 不对齐。本波仍可与自身内部逐条对比（设置一致），但**跨波与 `RREXk770` 比较时 decay 是混淆变量**。波 180 已修正。
- **multisim**：`vMhKD9nY4hv8IFJQWw63r8`（10 条，全部 COMPLETE，0 错误）
- **数据集**：`earnings_sent_matrix`（7 字段，cov 全 0.70）
- **落库**：`wave_results` USA/179，verdict = PARTIAL，`n_pass=0 / n_near=2`
- **目的**：EARNINGS 塔现持 1 颗（`RREXk770`，S 1.63 / F 1.02 / 2Y 3.00 / fRA 0），需第 2、3 颗。

---

## 1. 数据集的自由度约束（决定模板设计）

7 字段里 6 个是信号，其中 3 个构成**同一分布**：

```
positive_sentiment_probability_3 (P) + negative_sentiment_probability_3 (N)
  + likelihood_of_neutral_tone (NT) = 1
```

⇒ **三重分类只有 2 个真实自由度**。因此下列表达式在数学上是 P 的单调变换，不构成新信息：

- `subtract(P, N)` —— 因为 N = 1 − P − NT
- `reverse(N)`
- `ts_rank(N, W)`

**推论**：`RREXk770`（`ts_rank(P,504)`）与「`ts_rank(NT,504)` 反向」几乎等价。这也解释了为什么 NT 是**最不拥挤字段**（48 alphas vs P 的 366）却**单独无信号**——最拥挤 ≠ 最没用，但最少人用 ≠ 有信号。

**真正有超额信息的四个方向**（本波模板全部从这里派生）：

| 方向 | 数学形式 | 为什么不是 P 的单调变换 |
|---|---|---|
| 三分类**基尼不纯度** | `1 − Σp²` | 二次型，对分布形状敏感，非单调 |
| **argmax 离散类别** | `overall_sentiment_score ∈ {−1,0,1}` | 离散化抹掉置信度，是另一种投影 |
| **W1 − W2 加权方法分歧** | `method1 − method2` | 两个独立加权法的读数差 |
| **条件正概率** | `P / (P + N)` | 剔除了 NT 的干扰，是不同的归一化 |

---

## 2. 十模板清单

| 编号 | 模板 | 自由度数 | 经济含义 | 结构类型 | 来源 |
|---|---|---|---|---|---|
| E1 | `group_rank(ts_rank(NT,504), ind)` | 1（NT 序位） | 中性语调历史分位 | 长窗序位·水平 | 自建 |
| E2 | `group_rank(1−Σp², ind)` | 3（基尼） | 语调**确定性**（越确定越好） | **二次型·分布形状** | 自建（信息熵思路） |
| E3 | `group_rank(ts_mean(argmax,22), ind)` | 1（离散类别） | 平均情绪类别 | **离散化·均值** | 自建 |
| E4 | `group_rank(ts_std_dev(argmax,66), ind)` | 1 | 情绪类别**不稳定度** | 离散化·二阶矩 | 自建 |
| E5 | `group_rank(subtract(W1,W2), ind)` | 2 | 两种加权法的**方法分歧** | **双读数差·一阶** | 自建 |
| E6 | `group_rank(P/(P+N), ind)` | 2 | 条件正概率（剔除中性） | **归一化·比值** | 自建 |
| E7 | `group_rank(ts_delta(NT,66), ind)` | 1 | 中性语调**变化** | 一阶差分 | 自建 |
| E8 | `group_rank(ts_std_dev(1−Σp²,66), ind)` | 3 | 确定性的**波动** | 二次型·二阶矩 | 自建 |
| E9 | `group_rank(ts_zscore(NT,504), ind)` | 1 | 中性语调**异常偏离** | 时序标准化 | 自建（三层剥离 L3 异常层，源自论坛 43805658109463） |
| E10 | `group_rank(subtract(rank(argmax),rank(P)), ind)` | 1 | 离散类别 vs 连续概率的**秩背离** | **双读数秩差** | 自建 |

**多样性自检**：10 个模板在「矩」上分布为 水平 3（E1/E5/E8 各自不同型）、一阶差分 1（E7）、二阶矩 3（E4/E8/E9）、比值/二次型 3（E2/E6/E10）；在「加工方式」上覆盖长窗序位 / 二次型 / 离散化 / 双读数差 / 归一化比值 / 时序标准化 / 秩背离；分组轴全部 `industry` 冻结（本波不测分组轴，留给波 180）。

---

## 3. 完整结果

| 编号 | alpha | S | F | TO | 2Y | SUB | invest_S | risk_neut_S | fRA |
|---|---|---|---|---|---|---|---|---|---|
| E1 | `Xg9qWdLx` | 0.19 | 0.04 | 6.55% | 0.34 | −0.16 | 0.08 | −0.14 | 4 |
| E2 | `1YNvxrmJ` | 0.75 | 0.31 | 5.46% | **1.55** | 0.39 | 0.82 | 0.55 | 4 |
| E3 | `0mYoR1Q1` | 0.74 | 0.32 | **3.82%** | 0.93 | **0.86** | 0.77 | 0.32 | 3 |
| E4 | `xArMYJmb` | 0.44 | 0.16 | 4.52% | 0.60 | 0.43 | 0.47 | −0.35 | 3 |
| **E5** | **`YP1Z5R26`** | **0.95** | 0.47 | 5.34% | **1.61** | 0.68 | **0.89** | 0.67 | **2** |
| **E6** | **`RREXVG2b`** | **0.97** | **0.51** | 5.09% | 1.30 | 0.75 | **0.89** | **0.74** | 3 |
| E7 | `rKRk5Zb1` | 0.37 | 0.11 | 7.97% | 1.14 | 0.33 | 0.35 | 0.00 | 3 |
| E8 | `kqNRVznK` | 0.47 | 0.17 | 4.30% | 0.67 | 0.54 | 0.47 | −0.37 | 3 |
| E9 | `mLoOgEqK` | 0.32 | 0.09 | 6.32% | 0.82 | 0.09 | 0.33 | −0.27 | 4 |
| E10 | `3qod98zQ` | 0.27 | 0.06 | 5.75% | 0.42 | 0.12 | 0.16 | 0.02 | 4 |

**精确表达式（DB 实取）**：

```
Xg9qWdLx  group_rank(ts_rank(ts_backfill(likelihood_of_neutral_tone, 252), 504), industry)
1YNvxrmJ  group_rank(subtract(1, add(add(multiply(ts_backfill(positive_sentiment_probability_3, 252), ts_backfill(positive_sentiment_probability_3, 252)), multiply(ts_backfill(negative_sentiment_probability_3, 252), ts_backfill(negative_sentiment_probability_3, 252))), multiply(ts_backfill(likelihood_of_neutral_tone, 252), ts_backfill(likelihood_of_neutral_tone, 252)))), industry)
0mYoR1Q1  group_rank(ts_mean(ts_backfill(overall_sentiment_score, 252), 22), industry)
xArMYJmb  group_rank(ts_std_dev(ts_backfill(overall_sentiment_score, 252), 66), industry)
YP1Z5R26  group_rank(subtract(ts_backfill(sentiment_weighting_method1, 252), ts_backfill(sentiment_weighting_method2, 252)), industry)
RREXVG2b  group_rank(divide(ts_backfill(positive_sentiment_probability_3, 252), add(ts_backfill(positive_sentiment_probability_3, 252), ts_backfill(negative_sentiment_probability_3, 252))), industry)
rKRk5Zb1  group_rank(ts_delta(ts_backfill(likelihood_of_neutral_tone, 252), 66), industry)
kqNRVznK  group_rank(ts_std_dev(subtract(1, add(add(multiply(ts_backfill(positive_sentiment_probability_3, 252), ts_backfill(positive_sentiment_probability_3, 252)), multiply(ts_backfill(negative_sentiment_probability_3, 252), ts_backfill(negative_sentiment_probability_3, 252))), multiply(ts_backfill(likelihood_of_neutral_tone, 252), ts_backfill(likelihood_of_neutral_tone, 252)))), 66), industry)
mLoOgEqK  group_rank(ts_zscore(ts_backfill(likelihood_of_neutral_tone, 252), 504), industry)
3qod98zQ  group_rank(subtract(rank(ts_backfill(overall_sentiment_score, 252)), rank(ts_backfill(positive_sentiment_probability_3, 252))), industry)
```

---

## 4. 归因：为什么 E5 / E6 赢，E1 / E9 / E10 输

### 4.1 赢的两条都建立在「剔除分歧」而不是「提高精度」

- **E6 = P/(P+N)** 把 NT 从分母里去掉。NT 是这个数据集里最不稳定的分量（E1 0.19 / E7 0.37 / E9 0.32 三条全灭，说明 NT 的序位、变化、异常**都没有信号**）。把噪声分量剔掉 ⇒ 剩下两个分量的比值就是最干净的语调方向。
- **E5 = W1 − W2** 是两个独立加权法的读数差。它捕捉的不是语调本身，而是**测度方法之间的不一致**——这是该数据集里唯一不与 P 共线的独立信息（W1/W2 的 userCount 91/101，明显低于 P 的 189）。

两条的共同点：**都在做「减法」——去掉一个已知无信号的维度**。这与 E2/E8（基尼不纯度）不同，后者保留全部三个分量、只是重新加权。

### 4.2 三分类展开的三条（E1/E7/E9）是同一个死信号

`NT` 的序位（E1 0.19）、变化（E7 0.37）、异常（E9 0.32）三条最高只到 0.37，量级一致。

⇒ **NT 是一个纯噪声维度**。这也反证了 `P + N + NT = 1` 里真正有信息的是 P 与 N，NT 只是残差容器。

**工程教训**：此前一度认为「NT 最不拥挤（48 alphas）所以最可能藏着 alpha」。**拥挤度与信号强度无关，二者甚至可以反向**（NT 无人问津恰恰因为它没信号）。

### 4.3 离散化（argmax）保留了子域稳健性但丢了强度

- `0mYoR1Q1`（argmax 均值）S 0.74 / **SUB 0.86** / **TO 3.82%**（全波最低换手）
- `xArMYJmb`（argmax 波动）S 0.44 / SUB 0.43

argmax 是「置信度抹平」的投影：把连续概率压成三档，**换手骤降**（3.82% vs E6 的 5.09%）但信息量也下降。SUB 0.86 是本波最高，说明离散化让信号在子宇宙里更均匀——这与「粗分组轴救 F、细分组轴救 SUB」是同一族现象（此处是**信息粗化救 SUB**）。

### 4.4 基尼不纯度：水平有用、波动没用

- `1YNvxrmJ`（1−Σp² 水平）S 0.75 / **2Y 1.55**（已过 2Y 闸）
- `kqNRVznK`（1−Σp² 波动）S 0.47 / 2Y 0.67

⇒ 「语调确定性」是有信号的慢变量，但「确定性的变化率」是噪声。E2 的 2Y 1.55 说明它在近年更强，是可用的**2Y 补强腿**（虽然自身 S 不够主腿）。

---

## 5. 换手结构与 F 的强耦合（本波最重要的工程结论）

**十条换手全部落在 3.82% – 7.97%，无一超过 TO 地板 0.125。**

⇒ F 走地板分支 `F = S × sqrt(R / 0.125)`，与 TO **完全无关**。

用 `margin = R/(TO×504)` 反解 R，再拟合 `R = k·S`：

| alpha | S | F | TO | margin | 反解 R | k = R/S | `F = S^1.5 × sqrt(k/0.125)` | 验算 F |
|---|---|---|---|---|---|---|---|---|
| `RREXVG2b` (E6) | 0.97 | 0.51 | 5.09% | 13.50bp | 3.46% | 0.03570 | S^1.5 × 0.5344 | 0.511 ✅ |
| `YP1Z5R26` (E5) | 0.95 | 0.47 | 5.34% | 11.70bp | 3.15% | 0.03315 | S^1.5 × 0.5150 | 0.477 ✅ |

**F = 1.00 所需的 S**：

| alpha | 所需 S |
|---|---|
| `RREXVG2b` | **1.519** |
| `YP1Z5R26` | **1.560** |

而 S 闸本身就是 1.58 ⇒ **两条候选只要把 S 推到 1.58，F 会自然落在 1.02–1.04，不需要任何单独的 F 优化。**

这与「降换手提 fitness」的常规思路完全相反——后者只在 **TO > 0.125** 时成立。两条候选**都已经在地板下**，任何压换手的动作只会同时砍掉 R 与 F，纯亏。

**推论（可迁移）**：拿到任何低换手候选，先判 TO 在哪一侧。地板下时唯一目标是提 S。

> ⚠ **勘误（2026-10-29 波 180 实测否定本段初稿的推断）**
> 本报告初稿曾写「地板下 `decay` 也只是砍 R」，**这是错的**。同表达式单变量对照：
> `RREXVG2b`（decay 4）S 0.97 / F 0.51 / 2Y 1.30 / SUB 0.75 → `mLoOm8vX`（decay 0）S 1.23 / F 0.72 / 2Y 1.89 / SUB 0.93
> ⇒ **decay 0 不是压换手，是减少信号滞后，直接提 S（+0.26）与 2Y（+0.59）。**
> 机理：`earnings_sent_matrix` 是季频事件型数据，`ts_backfill(F,252)` 把季度值前向填充到日频。decay 在此平滑的是**已经过期的信息**，只增加滞后、不降噪。**季频事件型数据的 decay 应取 0。**
> 更一般地：地板下「TO 已无关」只说明**压换手**无收益，不代表**改 decay** 无收益 —— 两者是不同动作，decay 改的是信号时序，不是交易频率。

---

## 6. 下一步

1. **波 180 已派发**（`3RHtYN3fI4u8buYGE4NRsL3`，10 条，**显式 `decay=0`**）：以 E6 的 `P/(P+N)` 为核，逐条只改一项——4 个分组轴（industry/subindustry/sector/market）、`group_zscore` 换 `group_rank`、`ts_rank504` 长窗、`reverse` 反号、`signed_power(cube)` 非线性、`ts_mean22` 平滑、`ts_zscore504` 时序标准化。其中第 1 条与 `RREXVG2b` **表达式完全相同而 decay 由 4→0**，构成干净的 decay 单变量对照。
2. ~~若波 180 仍无 S ≥ 1.58 ⇒ `earnings_sent_matrix` 的 S 天花板实测为 0.97，需换数据集~~
   **✅ 波 180 已回收（2026-10-29）：S 天花板推翻，两个模板同时突破 1.58。**
   - `ZYQZbnYx` = `group_rank(ts_zscore(CP, 504), industry)` → **S 1.71 / F 1.19 / 2Y 2.97 / SUB 1.24 / invest_S 1.37 / margin 17.75bp / fRA 0**
   - `88RAjQmo` = `group_rank(ts_rank(CP, 504), industry)` → **S 1.70 / F 1.15 / 2Y 2.59 / SUB 1.11 / fRA 0**
   - 提 S 杠杆实测排序：**长窗时序标准化（+0.48）≫ decay 4→0（+0.26）> subindustry（+0.13）**；`ts_mean22` 平滑 −0.41、`group_zscore` 替 rank −0.22 均为有害。
   - ⚠ 但**该数据集仍只能提交 1 颗**：6 颗全家族互相关 0.7576–0.9947，`max_mutually_below_subset` size = **1**。建议提交 `ZYQZbnYx`。
   - ⇒ 换数据集的需求不变，只是原因从「S 不够」变成「**信息自由度只有 2 个，只能撑 1 颗**」。详见 `wave180_earnings_cp_ablation.md`。
3. `0mYoR1Q1`（argmax 均值，SUB 0.86 / TO 3.82%）保留为**子域补强腿**，不单独提交。
4. `1YNvxrmJ`（基尼水平，2Y 1.55）保留为 **2Y 补强腿**。
