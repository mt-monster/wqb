# 波 178 · RISK 塔第 3 颗载体扫描（受控字段对照 + 单字段自由度判定）

- **区域 / 设置**：USA / TOP3000 / D1 / `neutralization=STATISTICAL` / `decay=2` / `truncation=0.05` / `nanHandling=OFF`
- **multisim**：`3e0lMk9yy59VcIcDIdtSMiA`（10 条，全部 COMPLETE，0 错误）
- **数据集**：`mfm_model_output`（A 组 7 条）+ `short_interest_factor_score_2`（B 组 3 条，同属该数据集）
- **落库**：`wave_results` USA/178，verdict = PARTIAL，`n_pass=0 / n_near=1`
- **目的**：RISK 塔已持有两颗合格且互相关 0.1277 的 alpha（`ZYQZEawY` + `qMLbW8xP`），需要第 3 颗且必须与两者 < 0.7。

---

## 1. 实验设计：为什么是「同骨架只换字段」

RISK 塔第 3 颗的困难不在「找不到强信号」，而在「找到的强信号与已有两颗解耦」。此前 11 次跨数据集尝试（ER 残差、shortinterest 方差、order book、PV 混塔）全部败在相关性或 prod 墙。

本波改用**受控对照组**：**冻结骨架**，只换字段。

```
group_rank(reverse(ts_mean(ts_backfill(<FIELD>, 22), 22)), industry)
```

这个骨架正是 `qMLbW8xP` 的夺冠结构（S 1.73 / F 1.02 / 2Y 2.48 / fRA 0），把它套到 `mfm_model_output` 其余 6 个字段上：

- 若某字段出 S 高 ⇒ **是字段本身的信号强**，不是骨架运气；
- 若全部出低 S ⇒ 说明 mfm 里只有 `discount_store_retail_score` 与 `short_interest_factor_score_2` 两个字段真的有信号，其余 11 个是噪声。

这比「每个字段配一个专属骨架」更干净——后者把「骨架选错」和「字段没信号」混在一起，是本项目反复踩的坑（波 176 `earnings_chart_dl` 7/7 全灭就是无法区分这两者）。

B 组是另一件事：判定 `short_interest_factor_score_2` 是否还有除「水平」之外的第二个自由度。若有，RISK 塔内可直接出第 2 颗同集 alpha 而无需跨集。

---

## 2. 十模板清单（结构互异）

| 编号 | 字段 | 骨架结构 | 经济含义 | 结构类型 | 来源 |
|---|---|---|---|---|---|
| A1 | `relative_momentum_factor` | reverse(ts_mean22) + group_rank ind | 低动量溢价（反向） | 水平·短平滑 | 自建（沿用 qMLbW8xP 骨架） |
| A2 | `hedge_fund_ownership_factor0` | 同上 | 低对冲基金持股溢价 | 水平·短平滑 | 自建 |
| A3 | `relative_size_factor` | 同上 | 小市值溢价（反向=买大） | 水平·短平滑 | 自建 |
| A4 | `relative_liquidity_factor` | 同上 | 低流动性溢价 | 水平·短平滑 | 自建 |
| A5 | `systemic_risk_measure_2` | 同上 | 低系统性风险溢价 | 水平·短平滑 | 自建 |
| A6 | `relative_volatility_factor` | 同上 | 低波动异象 | 水平·短平滑 | 自建 |
| A7 | `momentum_factor_score` | 同上 | 同 A1（别名验证） | 水平·短平滑 | 自建 |
| B1 | `short_interest_factor_score_2` | ts_std_dev(F,66) 不 reverse | 卖空费率**波动**溢价 | **二阶矩** | 波 167 已验证矩族 |
| B2 | `short_interest_factor_score_2` | reverse(ts_delta(F,66)) | 卖空费率**下降** | **一阶差分** | 波 167 |
| B3 | `short_interest_factor_score_2` | reverse(ts_rank(F,252)) 全局序位 + subindustry | 费率历史**相对位置** | 长窗序位 + 细分组轴 | 波 167 / 43805658109463 |

A 组 7 条的设计意图是**故意同构**（这是对照组，不是多样性波次）；真正的结构多样性由 B 组三个不同矩 + 波 181 承担。

---

## 3. 完整结果

| 编号 | alpha | S | F | TO | 2Y | SUB | invest_S | fRA | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| A1 | `3qod9kbP` | −0.12 | −0.02 | 11.54% | 0.60 | 0.64 | −0.46 | 3 | 灭 |
| A2 | `78LOZvbx` | **−1.04** | −0.45 | 5.89% | **−1.36** | −0.01 | −1.01 | 3 | 灭（反向 S 1.04） |
| A3 | `P0oeZYaL` | −0.28 | −0.08 | 7.62% | −1.58 | −0.29 | −0.39 | 4 | 灭 |
| A4 | `1YNvxlEM` | −0.09 | −0.01 | 6.70% | 0.81 | −0.06 | −0.15 | 4 | 灭 |
| **A5** | **`N1NMQJog`** | **0.91** | **0.45** | **6.74%** | **1.84** | **0.66** | **0.86** | **2** | **保留** |
| A6 | `E563v8AL` | 0.59 | 0.24 | 6.84% | 1.42 | 0.25 | 0.55 | 4 | 弱（且与 A5 相关 0.88） |
| A7 | `E563v831` | −0.12 | −0.02 | 11.54% | 0.60 | 0.64 | −0.46 | 3 | 灭（≡A1） |
| B1 | `ZYQZ0dZx` | 0.22 | 0.04 | 6.97% | 0.21 | −0.02 | 0.30 | 4 | 灭 |
| B2 | `58ERQARk` | −0.26 | −0.04 | 17.95% | −0.59 | 0.09 | 0.11 | 3 | 灭 |
| B3 | `Xg9qWvqa` | 0.58 | 0.14 | 17.52% | 0.45 | 0.78 | 0.64 | 3 | 灭 |

**精确表达式（DB 实取）**：

```
3qod9kbP  group_rank(reverse(ts_mean(ts_backfill(relative_momentum_factor, 22), 22)), industry)
78LOZvbx  group_rank(reverse(ts_mean(ts_backfill(hedge_fund_ownership_factor0, 22), 22)), industry)
P0oeZYaL  group_rank(reverse(ts_mean(ts_backfill(relative_size_factor, 22), 22)), industry)
1YNvxlEM  group_rank(reverse(ts_mean(ts_backfill(relative_liquidity_factor, 22), 22)), industry)
N1NMQJog  group_rank(reverse(ts_mean(ts_backfill(systemic_risk_measure_2, 22), 22)), industry)
E563v8AL  group_rank(reverse(ts_mean(ts_backfill(relative_volatility_factor, 22), 22)), industry)
E563v831  group_rank(reverse(ts_mean(ts_backfill(momentum_factor_score, 22), 22)), industry)
ZYQZ0dZx  group_rank(ts_std_dev(ts_backfill(short_interest_factor_score_2, 22), 66), industry)
58ERQARk  group_rank(reverse(ts_delta(ts_backfill(short_interest_factor_score_2, 22), 66)), industry)
Xg9qWvqa  group_rank(reverse(ts_rank(ts_backfill(short_interest_factor_score_2, 252), 504)), subindustry)
```

**命名更正（重要）**：实际表达式是 `reverse(ts_mean(F,22))`，**不是** `reverse(ts_mean22)` 外套顺序笔误——即「低值做多」，A 组全部同向。因此 A2 的 S −1.04 表示**「低对冲基金持股」是亏的，反过来「高对冲基金持股」赚**，与常见机构持股溢价先验相反。

---

## 4. 四个确定性发现

### 4.1 `momentum_factor_score` ≡ `relative_momentum_factor`（同字段别名）

`3qod9kbP` 与 `E563v831` 除字段名外表达式逐字相同，指标逐位一致：

| | S | F | TO | 2Y | SUB | invest_S | margin |
|---|---|---|---|---|---|---|---|
| `3qod9kbP` | −0.12 | −0.02 | 0.1154 | 0.60 | 0.64 | −0.46 | −5.4e-05 |
| `E563v831` | −0.12 | −0.02 | 0.1154 | 0.60 | 0.64 | −0.46 | −5.4e-05 |

⇒ 该数据集 13 个风格因子里**只有 12 个真实维度**；后续台账不得把两者当两个字段分别投入。

### 4.2 `systemic_risk_measure_2` 是唯一新载体，且它的 2Y 早已过闸

`N1NMQJog`：S 0.91 / F 0.45 / TO 6.74% / **2Y 1.84** / SUB 0.66 / **invest_S 0.86**（> 自设 0.70 闸）/ margin 9.18bp / fRA 只有 2 项。

对比同数据集里已被否掉的两颗（`ZYQZEawY`、`qMLbW8xP`）：这两颗的 strength 来源分别是「特质残差日收益」与「卖空费率水平」，与「系统性风险水平」在经济机制上**完全不同轴** ⇒ 这是 RISK 塔唯一还没被消耗的独立轴。

### 4.3 `short_interest_factor_score_2` 只有「水平」一个自由度

B 组三条（二阶矩 / 一阶差分 / 长窗序位）**全部 ≤ 0.58**，而水平式的 `qMLbW8xP` 是 1.73：

| 矩 | 表达式核心 | S |
|---|---|---|
| 水平（短平滑） | reverse(ts_mean22) | **1.73** |
| 二阶矩 | ts_std_dev66 | 0.22 |
| 一阶差分 | reverse(ts_delta66) | −0.26 |
| 长窗序位 + 细分轴 | reverse(ts_rank252→504) | 0.58 |

⇒ **该字段无法在 RISK 塔内出第 2 颗 alpha**，第 3 颗必须靠另一个字段（A 组结论）或换数据集。

### 4.4 `relative_liquidity_factor` 方向必须为正

同一字段、同一设置，只翻方向：
- 波 177 `WjOkPM7Z`：**正向** `ts_rank(F,504)` ⇒ S **+0.86**
- 波 178 A4 `1YNvxlEM`：`reverse(ts_mean22)` ⇒ S −0.09

⇒ 该因子是「**高流动性跑赢**」，方向不可翻。这与 `relative_size_factor`（正向 `ts_av_diff252` 得 S −1.16，即反向才赚）方向相反，两个字段不能套同一骨架符号。

---

## 5. 相关性全矩阵：RISK 塔已有 5 个可共存载体

`compute_mutual_correlation(threshold=0.7, years=4)`，986 个日收益点：

| 对 | 相关 | 判定 |
|---|---|---|
| `N1NMQJog` × `qMLbW8xP` | **0.4321** | ✓ 安全 |
| `N1NMQJog` × `ZYQZEawY` | **−0.0984** | ✓ 安全 |
| `N1NMQJog` × `WjOkPM7Z` | −0.1471 | ✓ 安全 |
| `N1NMQJog` × `78LOZvbx` | 0.1213 | ✓ 安全 |
| **`N1NMQJog` × `E563v8AL`** | **0.8804** | ✗ 同族（系统性风险 vs 相对波动率），只能取一 |
| `E563v8AL` × `qMLbW8xP` | 0.4416 | ✓ |

`max_mutually_below_subset = [N1NMQJog, qMLbW8xP, ZYQZEawY, WjOkPM7Z, 78LOZvbx]`，`max_mutually_below_subset_size = 5`，`max_subset_exact = true`。

⇒ **RISK 塔的点塔瓶颈不再是「缺解耦载体」**——候选池里已有 5 个两两 < 0.7 的载体，其中 2 个已全闸（`ZYQZEawY` / `qMLbW8xP`）、1 个差 S（`N1NMQJog` 0.91）、1 个差 S 且 2Y 弱（`WjOkPM7Z` 0.86 / 2Y 0.72）、1 个 SUB 极弱（`78LOZvbx` SUB −0.01）。

**瓶颈唯一的形态是：把某一个载体的 S 推过 1.58。**

---

## 6. `N1NMQJog` 的 S 缺口算术（本轮最重要的工程结论）

`TO = 6.74% < 0.125` ⇒ F 走地板分支 `F = S × sqrt(R / 0.125)`。

先由 margin 反解 R（本数据集 `margin = R / (TO × 504)`）：

```
R = margin × TO × 504 = 0.000918 × 0.0674 × 504 = 3.12%
```

验算：`F = 0.91 × sqrt(0.0312/0.125) = 0.91 × 0.4996 = 0.455` ✅ 对上报告的 0.45。

设 margin 比不变 ⇒ `R = k · S`，`k = 0.0312 / 0.91 = 0.03429`：

```
F = S × sqrt(k·S / 0.125) = S^1.5 × sqrt(0.03429/0.125) = S^1.5 × 0.5238
```

| 目标 | 所需 S |
|---|---|
| F = 1.00 | **S = 1.541** |
| S 闸 1.58（此时 F = 1.038） | **S = 1.58** |

⇒ **F 闸与 S 闸在这个信号上几乎完全重合，只需攻 S 一个目标。**

⚠ **勘误**：本轮早期口头推演曾出现「S 到 1.10 时 F 就过闸」的说法，那是把 `sqrt` 项误当成线性项的算错。正确门槛是 S ≈ 1.54。此处以本节的逐位验算为准。

同一算式在波 179 的 `RREXVG2b` 上独立复现（k=0.03570 ⇒ F=1 需 S=1.519），两波交叉验证一致。

---

## 7. 下一步

1. **波 181 已派发**（`bAhUf5J14ID9wb4HwyD3se`，10 条）：全部押 `systemic_risk_measure_2`，用 10 个结构互异模板攻 S 0.91 → 1.54+。模板覆盖：线性衰减平滑 / 时序分位 504 / 风险调整比（二阶矩÷一阶矩）/ 时序 z 标准化 / 细分组轴 / 最粗分组轴 + 长窗 zscore / 长记忆去趋势偏离 / 双矩乘积交互 / 双重 rank 平滑 / 纯二阶矩离散度。
2. 若波 181 全部卡在 S < 1.2 ⇒ 判定「`systemic_risk_measure_2` 的天花板就是 S≈1.0」，RISK 塔第 3 颗转攻 `WjOkPM7Z`（`relative_liquidity_factor`，相关完美但 S 0.86 / 2Y 0.72 双缺口）。
3. `E563v8AL` 与 `N1NMQJog` 相关 0.8804 ⇒ 永久只保留一席，不再为 `relative_volatility_factor` 花仿真槽。
4. `78LOZvbx`（SUB −0.01）虽 S 反向 1.04，但子域闸几乎无法救，降级为末位备选。
