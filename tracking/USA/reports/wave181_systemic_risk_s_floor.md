# Wave 181 — systemic_risk_measure_2 提 S 的十模板穷举（判死）

**日期**：2026-10-29
**区域 / 宇宙 / 延迟**：USA / TOP3000 / D1
**数据集**：`mfm_model_output`（117 字段，cov 0.9963，alphaCount 308，valueScore 3.0 → RISK 塔）
**目标字段**：`systemic_risk_measure_2`（3 users / 4 alphas，全数据集最不拥挤之一）
**multisim**：`bAhUf5J14ID9wb4HwyD3se`
**设置**：STATISTICAL / decay 2 / truncation 0.05 / nanHandling OFF / pasteurization ON / maxTrade OFF
**结论**：**FAIL** — 10 个结构互异模板，S 天花板 **0.92**，距闸（1.58）差 **72%**。字段与载体 `N1NMQJog` 一并判死。

> 说明：本波回测行未写入本地 `backtest_results`（仅 `wave_results` 有台账），下文的表达式为**设计时的模板骨架**。精确表达式全文可按 alpha id 从平台 `get_alpha_details` 回取。

---

## 1. 背景：为什么押这个字段

RISK 塔当时已持有 2 颗可共存的全闸候选：

| alpha | 结构 | S | F | 2Y | SUB | 与另一颗相关 |
|---|---|---|---|---|---|---|
| `ZYQZEawY` | `discount_store_retail_score` 残差反转 | 1.64 | 1.00 | 1.64 | 0.78 | 0.1277 |
| `qMLbW8xP` | `short_interest_factor_score_2` 水平反转 | 1.73 | 1.02 | 2.48 | 0.84 | 0.1277 |

点亮 RISK 塔需要第 3 颗。第 3 颗必须**同时**满足：
1. 与已有两颗相关 < 0.7（硬约束，否则 self-corr 拦下）
2. 自身全闸通过（S ≥ 1.58 / F ≥ 1.0 / 2Y / SUB / invest_S）

波 178 曾用 `systemic_risk_measure_2` 跑出 `N1NMQJog`（S 0.91 / F 0.45 / TO 6.74% / 2Y 1.84 / SUB 0.66 / invest_S 0.86），它与已有两颗的相关分别是 −0.0984 / 0.4321 —— **相关性上完美，是理想第三腿**，只差 S。

换算门槛（TO 6.74% 在地板 0.125 下）：
```
F = S × sqrt(R / 0.125) ,  R = margin × TO × 504
  = S × sqrt(k / 0.125)  （k = R/S 常数）
  ⇒ F = 1 需 S ≈ 1.541
```
S 闸（1.58）与 F 闸（1.541）重合，所以**只需攻 S 一个目标**：从 0.91 推到 1.58，需 **+74%**。

本波就是穷举 10 个结构互异骨架，看能否把它推上去。

---

## 2. 十模板清单（结构互异）

设 `x = ts_backfill(systemic_risk_measure_2, 22)`。

| # | 模板骨架 | 经济机制 | 结构差异 |
|---|---|---|---|
| T1 | `group_rank(reverse(ts_decay_linear(x, 66)), industry)` | 系统风险水平 → 反转 | 线性衰减几何（对照波 178 的 `ts_mean22`） |
| T2 | `group_rank(reverse(ts_rank(x, 504)), industry)` | 风险的历史分位 → 反转 | 非参数长窗秩 |
| T3 | `group_rank(divide(ts_mean(x, 22), ts_std_dev(x, 66)), industry)` | 风险调整比（单位波动承担的风险水平） | 除法几何（IR 式） |
| T4 | `group_rank(reverse(ts_zscore(x, 504)), industry)` | 风险的时序异常 → 反转 | 参数型长窗标准化 |
| T5 | `group_rank(reverse(ts_mean(x, 22)), subindustry)` | 同上，细分组轴 | 分组轴（subindustry vs industry） |
| T6 | `group_rank(reverse(ts_zscore(x, 504)), market)` | 同 T4，最粗分组轴 | 分组轴（market）+ 长窗标准化组合 |
| T7 | `group_rank(reverse(ts_av_diff(x, 252)), industry)` | 相对自身 252 日均值的偏离 → 反转 | `ts_av_diff` 去趋势 |
| T8 | `group_rank(multiply(ts_mean(x, 22), ts_delta(x, 66)), industry)` | 双矩乘积（水平 × 一阶差分） | 乘法几何（两矩交互） |
| T9 | `group_rank(rank(x), industry)` | 双重秩（检验幂等） | 秩的嵌套 |
| T10 | `group_rank(reverse(ts_std_dev(x, 66)), industry)` | 风险的波动（二阶矩）→ 反转 | 二阶矩 |

**互异维度覆盖**：分组轴 3 档（industry / subindustry / market）· 矩 4 类（水平 / 一阶差分 / 二阶矩 / 双矩乘积）· 时序几何 4 种（`ts_decay_linear` / `ts_rank` / `ts_zscore` / `ts_av_diff` / `ts_mean`）· 非线性 1 种（除法比）· 幂等检验 1 条（嵌套 rank）。无两条只差窗口。

---

## 3. 完整结果表

| # | 模板 | alpha | S | F | TO | 2Y | SUB | invest_S |
|---|---|---|---|---|---|---|---|---|
| **T1** | reverse(ts_decay_linear66) | `P0oe2gGK` | **0.92** | 0.46 | 6.63% | 1.82 | **0.72** | 0.88 |
| T2 | reverse(ts_rank504) | `GrWVbOlJ` | 0.40 | 0.11 | 12.44% | 1.28 | 0.15 | 0.40 |
| T3 | 风险调整比 mean/std | `vR10r2jd` | **−0.03** | −0.00 | 7.51% | 0.63 | 0.13 | −0.03 |
| T4 | reverse(ts_zscore504) | `58ERzgl1` | 0.52 | 0.16 | 8.26% | 1.24 | 0.13 | 0.61 |
| T5 | subindustry | `78LON6ZQ` | 0.74 | 0.29 | 5.66% | 1.86 | 0.55 | 0.78 |
| T6 | market + 长窗 zscore | `QPvebK3K` | 0.92 | **0.52** | 8.14% | 1.88 | 0.50 | 0.86 |
| T7 | reverse(ts_av_diff252) | `88RAjPjm` | **−0.04** | −0.00 | 8.32% | 0.71 | −0.19 | 0.12 |
| T8 | 双矩乘积（水平 × 一阶差分） | `MPYwa3a9` | 0.34 | 0.09 | 10.35% | 0.78 | **−0.12** | 0.25 |
| T9 | group_rank(rank(x)) | `78LON6NZ` | 0.91 | 0.45 | 6.74% | 1.84 | 0.66 | 0.86 |
| T10 | reverse(ts_std_dev66) | `RREXb6bz` | 0.40 | 0.11 | 7.50% | 0.28 | 0.10 | 0.42 |

10 条表达式全部 COMPLETE、0 错误。

**S 分布**：最高 0.92（两次，T1 与 T6）· 次高 0.91（T9）· 其余 0.34–0.74 · 两条为负（T3、T7）。

---

## 4. 六条确定性发现

### 4.1 S 天花板实测 0.92，且被三个不同骨架同时顶到

T1（线性衰减 · industry）、T6（长窗 zscore · market）、T9（嵌套秩 · industry）三个**结构完全不同**的骨架分别得到 0.92 / 0.92 / 0.91。

这是很强的信号：**0.91–0.92 是这个字段的 S 上界**，不是某个骨架选错了。距闸 1.58 差 72%，不是靠调窗口或换轴能补的量级。

### 4.2 `group_rank(rank(x))` ≡ `group_rank(x)` —— 逐位相同

`78LON6NZ`（T9）与 `N1NMQJog`（波 178）指标**逐位相同**：
S 0.91 / F 0.45 / TO 6.74% / 2Y 1.84 / SUB 0.66 / invest_S 0.86

内层 `rank` 是单调变换，被外层 `group_rank` 完全吃掉。这与波 180 的 `signed_power(subtract(CP,0.5),3)` ≡ 裸 CP 是**同一条铁律的两次独立复现**：

> `group_rank` / `rank` / `ts_rank` 内部**只允许非单调变换**。保序变换（`signed_power` 正次幂、`log`、`sqrt`、线性缩放、加减常数、内层 `rank`）一律等价于没做。

### 4.3 归一化 / 去趋势彻底毁信号 —— 全部信息都在「水平」里

| 构造 | S | 判断 |
|---|---|---|
| `divide(ts_mean(x,22), ts_std_dev(x,66))` | **−0.03** | 完全归零 |
| `reverse(ts_av_diff(x,252))` | **−0.04** | 完全归零 |
| 基线 `reverse(ts_mean(x,22))` | 0.91 | 参考 |

把一个有信号的量除以它的滚动波动，或者在它里面减去它自己的长期均值，信号就消失了。这说明 `systemic_risk_measure_2` 携带的信息**纯在绝对水平**，不在「相对自己历史的偏离」，也不在「单位风险承担的风险」。

这一点与波 180 的 `earnings_sent_matrix` **完全相反**：CP 的健康构造恰恰是「相对自己两年的异常」（`ts_zscore(CP,504)` 把 S 从 1.23 推到 1.71，+48%）。

> **判据沉淀**：不能先验假设「相对自己的异常」一定优于「绝对水平」。这必须逐字段实测——两者在不同字段上可以是相反的方向。

### 4.4 二阶矩弱于水平，双矩乘积是稀释而非补强

- 单二阶矩：`reverse(ts_std_dev(x,66))` S 0.40 / 2Y **0.28**（基线 2Y 1.82）
- 双矩乘积：`multiply(ts_mean(x,22), ts_delta(x,66))` S 0.34 / SUB **−0.12**（唯一负 SUB）

一阶差分本身弱（T7 的 `ts_av_diff` 也是 −0.04），把它和水平乘起来不会补强，只会把水平里的信息摊薄并引入噪声。**「两矩交互」不是通用提 S 手段，只在两矩各自都有独立信号时才有意义**（对照波 180：`earnings_sent_matrix` 的两矩也都弱，同样收敛）。

### 4.5 分组轴方向与 earnings 相反

| 分组轴 | S（同骨架 `reverse(ts_mean22)`） |
|---|---|
| subindustry | 0.74 |
| **industry** | **0.91** |

`earnings_sent_matrix` 上是 subindustry（1.36）> industry（1.23）；`systemic_risk_measure_2` 上反过来，subindustry（0.74）< industry（0.91）。

同时最粗轴 market 配长窗 zscore 得到 **F 0.52（全波最高）**，尽管 S 仍是 0.92。

> **判据沉淀**：「细分组轴救子域、粗分组轴救 F」这条规律**不可跨数据集迁移**。分组轴的效果取决于该字段的横截面异质性落在哪一层——行业内的风险共性强的字段，细分反而把信号切碎。

### 4.6 `ts_decay_linear` 与 `ts_mean` 等价，decay 几何不构成新维度

T1（`ts_decay_linear(x,66)`）S 0.92 vs 基线（`ts_mean(x,22)`）S 0.91 —— 差 0.01，在噪声内。

线性衰减权重和等权平均在这个字段上是同一个东西，因为字段本身变化极慢（日频风险估计）。**衰减几何只在快变信号上才有区分度。**

---

## 5. 判死结论与后续

### 判死

| 对象 | 理由 |
|---|---|
| `systemic_risk_measure_2`（字段） | 10 个结构互异模板 S 上限 0.92，距闸差 72%；三个不同骨架同时顶到同一上界 ⇒ 结构性天花板，非选型失误 |
| `N1NMQJog`（载体） | 由该字段构成，随之失效 |
| `WjOkPM7Z`（载体） | `relative_liquidity_factor`，S 0.86 / 2Y **0.72** 双缺口 |
| `78LOZvbx`（载体） | `hedge_fund_ownership_factor0`，SUB **−0.01** |

⇒ **RISK 塔内已无可用的第 3 载体，必须换数据集。**

### 换数据集的方向（按产出率排）

`get_mining_yield`（strict，ra_clean / backtested）给出的 USA RISK 类数据集产出率：

| 数据集 | 产出率 | 字段 | cov | alphaCount |
|---|---|---|---|---|
| `risk65` | **0.50（3/6）** | 6（全 MATRIX） | 0.9743 | 411 |
| `risk60` | 0.182（4/22） | 5 | 1.0 | 1,984 |
| `risk_multi_source` | 0.167（1/6） | — | — | — |
| `risk59` | 未测 | 16（全 VECTOR） | 0.9806 | 82 |

**选 `risk65`**（波 182 已派发，multisim `1qA37hFS58T9a9CF3J71cr`）。

理由与风险：
- 6 个字段全是 MATRIX（无 VECTOR 聚合负担），cov 1.0 / 0.9485，valueScore 3.0，USA 全类别产出率第 3 高
- 字段分两个经济轴：`*_dsrt_intermediate` / `trsd_*` = 特质**残差收益**；`*_srisk` = 特质**风险估计**
- ⚠ **重叠风险**：`mfm_model_output.discount_store_retail_score` 已被证实实为「特质残差日收益 %」，正是 `ZYQZEawY` / `0mYop7r`（相关 0.8914）的载体。`risk65` 的 4 个 dsrt/trsd 字段同为「特质残差收益」⇒ **大概率为同一现象的另一个供应商版本，与 `ZYQZEawY` 可能高相关**。因此波 182 把 10 个模板中的 6 个押在 `*_srisk`（特质风险，与 RISK 塔已有载体机制不同轴），4 个 dsrt/trsd 只作相关性与机制对照。

`risk59` 降为次选：16 字段全 VECTOR（借券费率 / 空头拥挤度），与已确认 prod 墙的 `shortinterest3`（`kqNRbvJP` PC = 0.8463）机制同源 ⇒ **prod 墙风险高**。

---

## 附：相关文件

- 前序报告：`tracking/USA/reports/wave178_risk_winner_skeleton_scan.md`（波 178，`N1NMQJog` 的诞生与 S 缺口算术）
- 波次台账：`upsert_wave_result(region="USA", wave_number=181, verdict="FAIL", n_pass=0, n_near=1)`
- 后续：波 182（`risk65`，`1qA37hFS58T9a9CF3J71cr`）
