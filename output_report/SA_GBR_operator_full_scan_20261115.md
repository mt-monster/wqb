# GBR SuperAlpha 全算子扫描与最优配方（2026-11-15）

> 目标：在 GBR/TOP700 上「持续优化直到最佳」，并把平台**全部可用于组 SA 的算子**纳入审计。
> **本轮未提交任何 alpha**，提交权归用户。
> 规模：**11 批 33 条仿真 + 9 次双闸实测 + 1 次互测矩阵**。

---

## 1 执行摘要 — 最优件

### 1.1 第一顺位：`kqabOm7g`

| 项 | 值 |
|---|---|
| 配置 | GBR / TOP700 / d1 / **SECTOR** / **decay 3** / trunc 0.02 / **selectionLimit 14** |
| Selection | `if_else(is_nan(long_count),1,long_count) * (self_correlation<0.7) * (turnover>0.01) * (turnover<0.6)` |
| Combo | `stats=generate_stats(alpha); innerCorr=self_corr(stats.returns,500); ic=if_else(innerCorr==1.0,nan,innerCorr); maxCorr=reduce_max(ic); w=1-maxCorr; w` |
| IS | **S 4.53 / F 5.41 / TO 0.1254 / R 0.1787 / DD 0.0332 / margin 0.00285** |
| 2Y / sub | **2Y 3.86** / **sub 3.07** / investability 4.02 |
| 双闸（refresh=True） | **prod 0.6428**（余量 .0572）/ **self 0.5291**（余量 .1709） |
| IS checks | **8 PASS / 0 FAIL**（仅 MATCHES_COMPETITION WARNING） |

### 1.2 相对本轮起点基线的跃升

基线 `GrWjwp8Q`（S3.07 / F3.08 / TO .1355 / prod .6705 / self .6092）：

| 指标 | 基线 | 最优 | Δ |
|---|---|---|---|
| Sharpe | 3.07 | 4.53 | **+47.6%** |
| Fitness | 3.08 | **5.41** | **+75.6%** |
| Returns | .1366 | .1787 | +30.8% |
| Drawdown | .0601 | .0332 | **−44.8%** |
| Margin | .002017 | .00285 | **+41.3%** |
| Turnover | .1355 | .1254 | **−7.5%** |
| 2Y | 3.05 | 3.86 | +26.6% |
| sub | 2.20 | 3.07 | +39.5% |
| prod | .6705 | .6428 | −.0277 |
| self | .6092 | .5291 | −.0801 |

**S/F 大涨、DD/TO 下降、prod/self 双降 —— 全维度改善，无权衡代价。**

### 1.3 种子候选池（互测 ρ >0.96，只能取一颗）

| 件 | 族 / decay | S | F | TO | R | DD | margin | prod | self |
|---|---|---|---|---|---|---|---|---|---|
| **`kqabOm7g`** | **SECTOR d3** | 4.53 | **5.41** | **.1254** | **.1787** | .0332 | **.00285** | .6428 | .5291 |
| `XgaPzoVX` | INDUSTRY d1 | **4.64** | 4.77 | .1641 | .1734 | **.0283** | .002114 | **.6039** | **.5196** |
| `akaMwk9O` | SECTOR d1 | **4.66** | 4.96 | .1629 | — | — | — | .6403 | .5183 |
| `ZYaqMPgZ` | INDUSTRY d2 | 4.58 | 5.06 | .1400 | — | — | — | .6039 | .5185 |
| `QP0qgEdW` | INDUSTRY d3 | 4.51 | 5.19 | .1265 | — | — | — | .6039* | — |
| `rK7EVE1E` | SECTOR d2 | 4.60 | 5.27 | .1389 | — | — | — | .6403* | — |
| `P05q8paq` | INDUSTRY d4 | 4.45 | 5.11 | .1170 | — | — | — | .6039* | — |
| `YPanJmVl` | SECTOR d4 | 4.47 | 5.30 | .1159 | — | — | — | .6403* | — |

`*` = 同成分池推断（已在 d1/d2/d3 上验证 prod 只由成分池决定，decay 不改 prod）

---

## 2 ★★★ 本轮推翻的三条旧判据

### 2.1 判据推翻一：SA 换中性化族 ≠ 新席（互测 ρ .9685）

实测互测矩阵（`compute_mutual_correlation`，4 年日收益，1021 点）：

```
XgaPzoVX (INDUSTRY d1) ↔ ZYaqMPgZ (INDUSTRY d2) : 0.9986
XgaPzoVX (INDUSTRY d1) ↔ akaMwk9O  (SECTOR   d1) : 0.9685   ← 族不同！
ZYaqMPgZ (INDUSTRY d2) ↔ akaMwk9O  (SECTOR   d1) : 0.9669
```

**跨中性化族（INDUSTRY vs SECTOR）在同 selection+combo 骨架上互相关仍 0.9685。**

机制：`neutralization` 是 SA **最后一步的末端再剥离**，作用于已经加权完成的组合。它不改变「选了哪些成分、各自什么权重」——底层的 PnL 来源完全相同，只改最后的行业暴露投影粒度。

⇒ **SA 席位由「selection 取到的成分集合 + combo 权重」决定；中性化族与 decay 只是末端微调，不构成独立席。**

这修正了 §0.6.1-2 的「同族=死、异族可共存」：那条结论来自**历史不同批次、selection/limit 不同**的件（真正的差异在成分集合），而非中性化族本身。

**新判据（SA build 场景）**：
- 同 selection 表达式 + 同 limit ⇒ 同席（无论族/decay 怎么变），预期 ρ >0.96
- 只有**成分集合变化**（改 selection 排序轴 / 改 limit）才可能产生新席
- 验证顺序：本地 `compute_mutual_correlation`（免费不占槽）→ 再谈提交

**★ 另注**：`self` correlation 只对**已提交 OS 池**计算。未提交的候选彼此之间的 ρ **不在 self 里体现**，必须单独跑互测。本轮若不跑互测，会误判这 8 颗为「8 个独立席」。

### 2.2 判据推翻二：prod 随 limit 非单调，l14 是谷底

```
limit :  10     12     13     14     15     16     20
S     : 4.20   4.34   4.40   4.64   4.41   4.29   4.00~4.04
F     : 3.79   4.21   4.37   4.77   4.64   4.55   4.44~4.49
prod  : .6674   —      —    .6039   —      —    .7368~.7521
```

**l14 同时是 S/F 峰值和 prod 谷底**（双重最优，非巧合）。机制：
- l10（`long_count` top10）= 覆盖最广的 10 颗，风格高度同质（多为大覆盖 fundamental 类）⇒ 组合后拥挤度反而高
- 第 11–14 名引入**异风格成分** ⇒ 分散度跳升，prod 掉 .0626
- 超过 14 颗后新增成分自身拥挤且稀释 S ⇒ prod 回升（l20 .7368~.7521，撞红线）、S 下降

⇒ **「组件数↑⇒prod↑」（旧记 §0.4）不是普适规律**。在「按覆盖广度排序取前 k」语境下 prod 是 k 的 **U 型曲线**，谷底须逐区实测。

### 2.3 判据推翻三：truncation 在 SA 层完全无效

`0mP9gk8v`（trunc .02）与 `6XM30EPP`（trunc .08）指标**逐位相同**：S4.00 / F4.44 / TO.1522。
⇒ SA 的 truncation 设置被 combo 内部行为吸收，不是杠杆（再次印证 §0.5，但这次是在 limit 20 的等权配方上验证）。

---

## 3 本轮建立的三个平台事实

### 3.1 Selection 只能排序，不能筛质量

官方语义（`selection-expression` 文档，2026-09-30 更新）：输出为 `selection weight`，Alphas 按该值降序取前 `selectionLimit`；`POSITIVE` handling 下只有 >0 的入选，`0`/`NaN` 排除。

⇒ **任何保号单调变换都是 no-op**。本地核验：`power(0.7-prod,3)`、`(0.7-prod)*long_count`、`(0.7-prod)*sqrt(long_count)` 三种写法选出的 10 颗**完全一致**。

**有效杠杆仅三个**：①换非单调组合 ②加/减硬门槛 ③换排序主键。

### 3.2 `author_*` 属性对本人的 alpha 无效（实测炸两次）

文档列 20 个作者级属性（含 `author_sharpe` / `author_fitness` / `author_returns_to_drawdown`）。实测：

```
selection = (0.7-prod_correlation) * gate * author_fitness        → run_selection count = 0
selection = (0.7-prod_correlation) * gate * power(author_fitness,2) → count = 0
→ 仿真报 "At least 10 component alphas are required"
```

**平台不提供裸 `sharpe` / `fitness` 字段**，`author_*` 对自己提交的件返回 NaN。
⇒ 论坛阈值 `author_fitness≥2` 在本仓**不可实现**；即便可用，GBR 池仅 1 颗 >2、4 颗 >1.5，会直接炸。

### 3.3 组件质量通道只剩 combo 的 `ts_ir`，且它是劣的

`generate_stats(alpha)` 输出 14 个日频统计：`drawdown / hold_pnl / hold_shares / hold_value / long_count / long_value / pnl / returns / short_count / short_value / trade_pnl / trade_shares / trade_value / turnover`（**无 sharpe/fitness**）。

唯一可算的组件「质量」是 `ts_ir(stats.returns, d)`。**实测无效**：
- `w * ts_ir250` → F **2.71**（基线 3.08），S 持平，TO↑
- 纯 `ts_ir250` → F **2.70**
- `ts_ir500` 同向劣

原因：IR 加权把权重推向近期高波动成分，收益质量反降。

### 3.4 唯一有效的新杠杆：`long_count`（覆盖广度）

文档可用属性里的 `long_count`（IS 平均多头持仓数）是**组合分散度的最佳可得前兆**。这是本轮全部收益的来源——按它排序取前 14 颗，使 S +47%、F +76%、prod −.027、self −.080。

---

## 4 全部 160 个 SA 算子审计

平台 SA 算子共 **160**（`SELECTION` 43 + `COMBO` 117）。本轮前本仓累计用 **4 个**（覆盖率 2.5%），本轮扩到 **8 个**（5.0%）：`generate_stats / self_corr / if_else / reduce_max / reduce_avg / reduce_percentage(试) / ts_ir(试) / is_nan`。

### 4.1 SELECTION 可用算子（43 个）

| 类 | 算子 | 对 SA 的实际作用 | 本轮结论 |
|---|---|---|---|
| 算术（14） | `add subtract multiply divide power sqrt log exp s_log_1p signed_power inverse abs negate reverse sign` | 保号单调 ⇒ 入选集合不变 | **无效**（已本地核验） |
| 比较/逻辑（11） | `less greater equal less_equal greater_equal not_equal and or not if_else` | 构造多门槛/条件加权 | **有效**（gate 全靠它） |
| 非有限（7） | `is_nan is_not_nan is_finite is_not_finite nan_mask nan_out to_nan` | NaN 兜底 | **有效**（`if_else(is_nan(long_count),1,·)`） |
| 三角/离散（9） | `arc_cos arc_sin arc_tan ceiling floor round frac clamp purify` | 破坏排序单调性 | 不做（语义不明） |
| 形状（2） | `sigmoid tanh` | 单调 | **无效** |
| 特殊（1） | **`universe_size`** | 官方 `long_count/sqrt(universe_size())` | 单 universe 时排序等价 ⇒ 无增益 |

### 4.2 COMBO 独有算子（117 个）按机制分级

**A 级 — 已实测**

| 算子 | 结果 |
|---|---|
| `generate_stats` `self_corr` `if_else` `reduce_max` | 基线配方 `1-maxCorr`；**w¹ 最优** |
| `reduce_avg` | 与基线**完全持平**（S3.08/F3.08 vs 3.07/3.08）⇒ 权重形状不敏感 |
| `w²` / `w³` / `w⁵` | 全部**略劣**（4.62/4.72、4.62/4.71 vs 4.64/4.77）⇒ 幂次无增益 |
| `ts_ir` | **劣**（F 3.08→2.70） |
| `reduce_percentage` | 语法需具名参 `percentage=0.9`；未成行 |

**B 级 — 机制清晰，待实测（下轮）**

| 算子 | 预期机制 |
|---|---|
| `reduce_ir` | ic 的 IR 聚合，抗噪优于 max |
| `reduce_stddev` / `reduce_range` | 只惩罚「拥挤且离散」组合 |
| `reduce_choose` | 取第 n 大相关（max 与 avg 之间的可调档） |
| `hump` / `hump_decay` / `jump_decay` | 直接压权重抖动 ⇒ 继续降 TO（当前 .1254 仍有空间） |
| `ts_decay_linear` / `ts_decay_exp_window` / `ts_weighted_decay` | 权重时序平滑，等价 combo 层 decay |
| `rank` / `zscore` / `scale` / `normalize` / `quantile` / `winsorize` | 权重标准化；`rank` 变等距会实质改变权重分布 |
| `vector_neut` / `regression_neut` / `vector_proj` | 权重对基准正交化 |
| `combo_a(alpha,nlength,mode)` | **平台内置组合器，完全未试** |
| `inst_tvr` / `inst_pnl` | 成分级换手/盈亏 ⇒ 「低换手优先」权重 |
| `ts_percentage` / `ts_median` / `ts_rank` | 分量级稳健统计替代均值 |
| `sigmoid` / `tanh` / `clamp` | 权重压缩，抑制极端权重 |

**C 级 — 结构/类型，无清晰收益路径**

`convert densify pasteurize unit replace count bucket trade_when keep filter position_safeguard one_side rank_by_side combo_weight`（12 个）

**D 级 — 数学上无意义或纯噪声（约 50 个）**

- 三角/离散：`arc_cos arc_sin arc_tan ceiling floor round round_down frac`
- 纯掩码：`is_nan is_finite to_nan nan_mask nan_out`
- 权重矩阵上语义弱：`kth_element last_diff_value days_from_last_change ts_step ts_count_nans ts_arg_max ts_arg_min ts_max ts_min ts_max_diff ts_min_diff ts_min_max_cps ts_min_max_diff ts_triple_corr ts_theilsen ts_poly_regression ts_partial_corr ts_co_skewness ts_co_kurtosis rank_gmean_amean_diff ts_rank_gmean_amean_diff`
- 分组族 17 个：`group_backfill/count/extra/max/mean/median/min/neutralize/normalize/percentage/rank/scale/std_dev/sum/zscore/cartesian_product/vector_neut/vector_proj` —— combo 的 group 维度是 Alpha 索引而非行业，语义不符

---

## 5 本轮完整实测矩阵（33 条）

### 5.1 失败 / 无效（早停）

| 件 | 配置 | 结果 |
|---|---|---|
| — | selection `*author_fitness` | ✗ `<10 component alphas` |
| — | selection `*power(author_fitness,2)` | ✗ 同上 |
| — | combo `reduce_percentage(ic,0.9)` | ✗ `Required attribute "percentage" must have a value` |
| `E5QY8Pbr` | l10 默认sel + `w*ts_ir250` | S3.07 F**2.71** ⇒ 劣 |
| `RReqlxj1` | l10 默认sel + `ts_ir250` | S3.08 F**2.70** ⇒ 劣 |
| `LLKqzW3M` | l10 默认sel + `w²` | S3.04 F3.05 ⇒ 略劣 |
| `e7agG71M` | l10 默认sel + `reduce_avg` | S3.08 F3.08 ⇒ 持平（2Y3.06/sub2.18/8PASS） |
| `zqdQGw0R` | l10 默认sel + d2 | S3.02 F3.13 ⇒ 持平 |
| `A1xYzerY` | l12 + LC + `prod<0.65` | S3.79 F3.76 ⇒ 硬筛伤 S |

### 5.2 limit 扫描（INDUSTRY d1，LC = long_count 排序）

| 件 | limit | S | F | TO | prod | self |
|---|---|---|---|---|---|---|
| `GrWjwp8Q` | 10（默认 sel） | 3.07 | 3.08 | .1355 | .6705 | .6092 |
| `pwaoGo3x` | 10 | 4.20 | 3.79 | .1971 | **.6674** | **.5873** |
| `vRAxGk2A` | 10（等权） | 4.20 | 3.84 | .1896 | — | — |
| `YPanz5dJ` | 12 | 4.34 | 4.21 | .1777 | — | — |
| `blaVz07N` | 13 | 4.40 | 4.37 | .1664 | — | — |
| **`XgaPzoVX`** | **14** | **4.64** | 4.77 | .1641 | **.6039** | **.5196** |
| `zqdQG7XR` | 15 | 4.41 | 4.64 | .1579 | — | — |
| `LLKqzYR9` | 16 | 4.29 | 4.55 | .1549 | — | — |
| `0mP9gk8v` | 20（等权） | 4.00 | 4.44 | .1522 | **.7521 ✗** | — |
| `0mP9gzlK` | 20 | 4.04 | 4.49 | .1506 | **.7368 ✗** | — |
| `XgaPz1Q8` | 20 等权 d2 | 3.95 | 4.65 | .1331 | — | — |
| `6XM30EPP` | 20 等权 trunc.08 | 4.00 | 4.44 | .1522 | — | — |

### 5.3 中性化族 × decay（l14 + LC）

| 件 | 族 / d | S | F | TO | prod | self |
|---|---|---|---|---|---|---|
| `XgaPzoVX` | INDUSTRY d1 | **4.64** | 4.77 | .1641 | **.6039** | **.5196** |
| `ZYaqMPgZ` | INDUSTRY d2 | 4.58 | 5.06 | .1400 | .6039 | .5185 |
| `QP0qgEdW` | INDUSTRY d3 | 4.51 | 5.19 | .1265 | .6039* | — |
| `P05q8paq` | INDUSTRY d4 | 4.45 | 5.11 | .1170 | .6039* | — |
| `O0WqV1xb` | SUBINDUSTRY d1 | 4.35 | 4.16 | .1680 | — | — |
| `akaMwk9O` | SECTOR d1 | **4.66** | 4.96 | .1629 | .6403 | .5183 |
| `rK7EVE1E` | SECTOR d2 | 4.60 | 5.27 | .1389 | .6403* | — |
| **`kqabOm7g`** | **SECTOR d3** | 4.53 | **5.41** | **.1254** | **.6428** | **.5291** |
| `YPanJmVl` | SECTOR d4 | 4.47 | 5.30 | .1159 | .6403* | — |

规律：
- **decay 1→3 单调提 F、降 TO、微降 S**；F 在 d3 见顶（两族一致）
- **decay 4 开始回落** ⇒ 与 §0.4「每区有 decay 上限」一致，GBR 上限 = 3
- **SECTOR 族比 INDUSTRY 族 F 高约 .2-.4、prod 高约 .037**；SUBINDUSTRY 全面劣

---

## 6 最优件五量（GBR μ̄ = 1.9064）

| 件 | N | S | U | N_eff | ρ_eff | Eff | ΔCAP% |
|---|---|---|---|---|---|---|---|
| `GrWjwp8Q` 基线 | 10 | 3.07 | .5092 | 2.593 | +.3173 | 1.735 | +.009 |
| `pwaoGo3x` l10 LC | 10 | 4.20 | **.6967** | 4.854 | +.1178 | 3.437 | +.009 |
| `XgaPzoVX` l14 IND d1 | 14 | **4.64** | **.6505** | **5.924** | **+.1049** | **4.527** | +.013 |
| **`kqabOm7g` l14 SEC d3** | 14 | 4.53 | .6351 | 5.646 | +.1138 | 4.081 | +.011 |

读法：
- `N_eff` 2.59 → **5.92**（等效独立腿数 ×2.3）
- `ρ_eff` +.317 → **+.105**（隐含组件平均相关降 67%）
- `Eff` 1.74 → **4.53**（每单位拥挤度换到的 Sharpe 溢价 ×2.6）
- **`U` 单指标不可作排序主键**：l10 版本 U 最高（.6967）却因 N 小、S 低而 Eff/N_eff 落后 ⇒ 印证 §0.6.1-3

**终选权衡**：`kqabOm7g`（F5.41 最高、TO 最低、R/margin 最高）vs `XgaPzoVX`（S4.64 最高、U/Eff 最高、prod 余量大 1.7 倍）。两者互测 ρ .9669-.9685 ⇒ **只能取一颗**。

---

## 7 与现存 6 颗 GBR SUPER 对比

| 件 | 提交日 | 族 | S | F | TO | prod |
|---|---|---|---|---|---|---|
| `3qompGeZ` | 11-08 | STAT d5 | 4.42 | 4.27 | .1366 | .6221 |
| `QPvGdLYQ` | 11-02 | SLOW d1 | 4.23 | 3.54 | .1698 | .6330 |
| `rKRbrZKo` | 10-31 | FAST d1 | 3.80 | 2.96 | .2071 | .6167 |
| `MPYAOR0r` | 10-28 | STAT d1 | 3.72 | 2.57 | .2114 | .5295 |
| `e7QGwrx6` | 10-10 | STAT d1 | 3.44 | 2.99 | .1392 | .6550 |
| `YPMp39q6` | 10-08 | R&M d1 | 2.67 | 1.86 | .1905 | .5799 |
| **`kqabOm7g`** | 未提交 | **SECTOR d3 l14** | 4.53 | **5.41** | **.1254** | .6428 |
| **`XgaPzoVX`** | 未提交 | **INDUSTRY d1 l14** | **4.64** | 4.77 | .1641 | **.6039** |

两颗都在 S 或 F 上超过现存最佳 `3qompGeZ`（4.42/4.27）。self top1 均为 `rKRbrZKo` / `3qompGeZ`，ρ ≈ .52 ⇒ 真实独立新席。

---

## 8 提交建议（**本轮未提交，等待用户指令**）

### 8.1 第一顺位：`kqabOm7g`

| 检查项 | 值 | 结论 |
|---|---|---|
| prod ≤ 0.68 | **.6428**（余量 .0572） | ✅ |
| self ≤ 0.68 | **.5291**（余量 .1709） | ✅ |
| IS checks 零 FAIL | 8 PASS / 0 FAIL | ✅ |
| 台账 REJECT | 无 | ✅ |
| 同档异族 | SECTOR+d3+l14 组合在 GBR 未提交过 | ✅ |
| B 档（TO<0.30 ∧ prod<0.60） | TO .1254 ✅ / prod .6428（差 .0428） | 接近 |

### 8.2 备选（与首顺互测 .967-.999，只能取一颗）

| 顺位 | 件 | 优势 | 劣势 |
|---|---|---|---|
| 2 | `XgaPzoVX` | S4.64 最高、prod .6039 最低（余量 1.7×）、Eff 4.53 | F 4.77 低 .64、TO 高 .039 |
| 3 | `akaMwk9O` | S4.66 最高 | F4.96、prod .6403 |
| 4 | `ZYaqMPgZ` | F5.06 + prod .6039 兼得 | S 4.58 |

### 8.3 配额
- `SUPER_SUBMISSION` = 1 颗/ET 日历日（账户级），00:00 ET 重置 = GMT+8 13:00
- 当前 ET 日 2026-11-14 **未用**（末次 `Wjl6JJQO` ET 11-13 20:48）

### 8.4 命令模板（仅供用户执行）
```bash
cd D:/coding/traeCN_project/wqb && WQB_ALLOW_ALPHA_SUBMIT=1 world-quant-brain-mcp/.venv/Scripts/python.exe tools/super_build.py submit --alpha-id kqabOm7g --region GBR
```

### 8.5 两个已知坑
1. 提交前停后台批次（并发会让 `_probe_prod_max` 抛 ProxyError）
2. prod 槽 195s 冷却（`logs/_dblock/correlation.cooldown.json`），未过期会 fail-fast

---

## 9 剩余优化路线（下轮）

1. **B 级 combo 算子**：在 `l14 + SECTOR d3` 骨架上单变量替换 `reduce_ir` / `reduce_stddev` / `reduce_choose` / `hump` / `rank` / `combo_a` / `inst_tvr`
2. **decay 3 邻域精修**：SECTOR d3 已是 F 峰，但 l13/l15 在 d3 下未测
3. **selection 换排序主键**：`min(long_count, short_count)`（双边覆盖）、`operator_count` 反向（简洁优先）
4. **★★ 跨区复用（最高价值）**：`long_count 排序 + limit U 型谷底定位 + decay d3 + SECTOR/INDUSTRY 对比` 这套方法论直接迁往 DEU/EUR/USA，预期同样能拿到 S/F 大幅提升（GBR 的旧配方曾被认为已到顶）
5. **新判据写回**：把 §2.1「中性化族不是新席」写进 `docs/experience/`，替换旧的「异族可共存」表述

---

## 附录：数据落盘

- 仿真结果：`results/sa_opt_20261115/res_*.json`（33 条）
- 批脚本：`results/sa_opt_20261115/batch1..11.sh`
- 日志：`results/sa_opt_20261115/log_*.log`
