# USA prod 墙归因分析 + 对照实验（2026-10-27 夜）

> 目标：15 算子内、eff=2（金字塔只涉两类）、prod < 0.70
> 信号源：`earningscall_sentiment` / `assetutilization_sentiment_polarity`（VECTOR，事件型季度情绪）
> 固定设置：USA / TOP3000 / D1 / decay 5 / CROWDING / trunc 0.08 / nanHandling ON / maxTrade OFF / 2014-01-01→2023-12-31

## 一、确认的全闸通过候选（3 颗，1 颗作废）

| alpha | 构造 | ops | S | F | 2Y | sub | inv | prod | self | eff |
|---|---|---|---|---|---|---|---|---|---|---|
| **`rKRY3NZ1`** | cap桶 + 动量63桶 + 波动252桶 | **15 ✅** | 1.79 | 1.17 | 2.28 | 0.93 | 1.65 | **0.6995** | 0.4700 | **2** |
| **`zq3ZMvkX`** | cap桶 + 动量63桶 + RISK动量桶 | **14 ✅** | 1.87 | 1.26 | 2.36 | 1.13 | 1.73 | **0.6737** | 0.4652 | **0** |
| `e75kq7LE` | cap+动量63+波动252+波动63+价量相关（5 轴） | 25 ❌ | 1.85 | 1.18 | 2.18 | 1.02 | 1.70 | 0.6509 | 0.4275 | 2 |

> `e75kq7LE` 超算子上限（25 > 15），已作废，仅作 prod 下界参照。

## 二、算子成本精算（15 预算是硬顶）

| 部件 | 写法 | ops |
|---|---|---|
| 基底 | `group_rank(ts_zscore(ts_backfill(vec_avg(F),BF),W), industry)` | **4** |
| 桶轴（MATRIX 字段） | `group_neutralize(·, bucket(rank(cap), "0,1,0.1"))` | **3** |
| 桶轴（需 ts_* 计算） | `group_neutralize(·, bucket(rank(ts_mean(returns,63)), "0,1,0.1"))` | **4** |
| 投影轴 | `vector_neut(·, rank(F))` | 2（实测无效） |
| `subtract(·, 0.5)` | 可删，指标完全不变 | **−1** |

- `ts_zscore` **不可删**：删后 S 从 1.87 → 1.07（`QPvMJoY5`），2Y 0.19、sub 0.17、RA fail 4 项
- 15 = 4 + 3 + 4 + 4（基底 + 三条桶轴）= **绝对上限**
- 四条桶轴最低 17 ops ⇒ 15 内不可能

## 三、对照实验 A：第三条轴的语义类型（单变量，其余全固定）

基底 4 + cap桶 3 + 动量63桶 4 = 11 ops，只换第三条轴。

| 第三条轴 | ops | S | **prod** | Δprod | eff |
|---|---|---|---|---|---|
| **RISK `price_momentum_factor_score` 桶** | 3 | 1.87 | **0.6737** | **−0.061** | 0 |
| **`ts_std_dev(returns,252)` 桶** | 4 | 1.79 | **0.6995** | **−0.035** | **2** |
| RISK `residual_volatility_factor` + 无动量桶 | 3×2 | 1.74 | 0.7067 | −0.028 | 0 |
| `ts_mean(volume,63)` 桶 | 4 | 1.83 | 0.7216 | −0.013 | 2 |
| `returns`（当日）桶 | 2 | 1.90 | 0.7305 | −0.004 | 2 |
| 无第三条轴（只有 cap + 动量63） | — | 1.92 | 0.7349 | 基准 | 2 |
| `ts_std_dev(returns,252)` **投影**（vector_neut） | 3 | 1.88 | 0.7361 | **+0.001** | 2 |
| `volume` + `adv20` 双投影 | 4 | 1.83 | **0.7816** | **+0.047** | 2 |

### 归因结论 A

1. **只有「Barra 风险因子桶」和「长窗波动桶」能实质降 prod**（−0.06 / −0.035）；其余 PV 轴只有 −0.004~−0.013。
2. **投影式（`vector_neut`）完全无效**，`volume`/`adv20` 投影甚至**反向**（+0.047）。
   机理：生产库里流动性/成交量类 alpha 极多，投影到流动性 = 主动靠近拥挤。
3. **RISK 轴 3 ops 比波动桶 4 ops 更便宜且更有效**，但会把 pyramid 变成三类 → `eff=0`（见第四节）。
4. `adv20` 与 `volume` 高度共线（3 轴与 4 轴的 S/F/sub 完全相同）⇒ adv20 轴零信息。

## 四、归因：为什么 eff=0 是硬伤（论坛实证）

论坛帖（`从 Theme 到 Osmosis：如何用好 Multiplier`）原话：
> **「混数据的话，如果你有多个 pyramid，pyramid 的乘数按最低的走，如果其中有一个 pyramid 乘数为 1，那么你的 pyramid 这个就乘数为 1，相当于 pyramid 没有加成了。」**

⇒ `zq3ZMvkX` = `[PV(1.1×), RISK(1.1×), OTHER(1.4×)]` 三类 → 按最低走 → **加成为 1，等于无 pyramid 加成**。
⇒ `rKRY3NZ1` = `[PV(1.1×), OTHER(1.4×)]` 两类 → min(1.1, 1.4) = **1.1× 加成有效**。

**这是 rKRY3NZ1（0.6995 / eff=2）优于 zq3ZMvkX（0.6737 / eff=0）的关键判据** —— 尽管后者 prod 低 0.026。

## 五、研究：论坛 + 论文给出的破局杠杆

### 5.1 论坛（两篇高票实战帖）

**帖 A《PROD CORRELATION < 0.7 实战复盘》（30 票）**：prod 0.856 → **0.666**
- 「**mm 结构**」：`ts_max_diff(ts_backfill(X,22),W) − ts_av_diff(ts_backfill(X,22),W)`
  （滚动窗口极值差 − 均值差）作用在低频字段上，效果三合一：TO 0.162→0.036、SUB 0.98→1.68、**prod 0.856→0.666**
- 「字段结构对相关性的影响远大于外层平滑」
- group 维度：**industry 常常是被低估的选项**（sector/subindustry/country/market 全部 CLUSTER 不达标）
- 中性化必须是 CROWDING（REVERSION_AND_MOMENTUM / STATISTICAL 全崩）

**帖 B《应对 Production Correlation：EUR/GBR/GLB 数百次模拟》（42 票）**：0.855 → **0.32**
五大杠杆按实测效果排序：

| # | 杠杆 | 实测 |
|---|---|---|
| 1 | 切换中性化（MARKET→STATISTICAL） | 0.855 → 0.726 |
| 2 | **差异化结构**（纯 SI vs 新闻+SI 混合） | 0.64 vs **0.46** |
| 3 | **`trade_when` 分层事件架构** | **0.51** |
| 4 | **不对称双塔**（right_tail 多 + left_tail 空 + 异构窗口） | **0.42** |
| 5 | **`group_rank` 外套 `hump` 平滑**（hump=0.0012） | **0.32** |

**共同原理（关键）**：
> 「参数级变化（窗口 ±5、权重 ±0.1）不改变交易画像，prod corr 自然不动。
> 只有改变 **事件时序**（哪些天在场）、**尾部暴露**（只取右尾 vs 全分布）、
> 或 **隐含正交的风险模型**，才能真正把这个数字压下去。」

**诊断判据**：「参数扫一遍，corr 纹丝不动 = 信号类别已饱和，立刻换类别」
⇒ 我的实测：assetutil 族的轴扫描 **corr 会动**（0.6737→0.7816，幅度 0.11）⇒ **未饱和，还有结构空间**。

### 5.2 外部论文

**Blitz, Huij & Martens (2011), Journal of Empirical Finance —— Residual Momentum**
- 传统动量有显著的**时变 Fama-French 因子暴露**；用**残差收益**排名可消除该暴露
- 结果：波动 **22.7% → 12.5%**（−45%）；Sharpe **0.45 → 0.90**（翻倍）
- 更少集中在截面极端 ⇒ 与"拥挤度"同向改善
- 2000–2009 传统动量 −8.5%/年，残差动量 **+4.7%/年**

**AEA 2023《What Does Residual Momentum Tell Us About Firm-Specific Momentum?》**
- beta 中性残差动量的 Sharpe **0.59 → 1.23**
- **关键**：beta 中性残差策略「**they correlate less with each other across regions and they correlate less with factor momentum**」
  ⇒ **残差化直接降低与其他因子的相关性** —— 这正是 prod 的机制
- 方法：短期残差收益 × 长期 beta，选一个既无动量也无反转的 lookback 窗口，两者正交

**对本战役的直接启示**：
- prod 的本质是「与生产组合的因子暴露重叠」。论文的答案是**残差化**（剥离共同因子），论坛的答案是**改变事件时序/尾部暴露**。
- 我已做的「桶轴分组中性化」是残差化的**分组近似**；**回归残差**（`ts_regression`）尚未尝试。

## 六、待验证的新构造（进行中）

### B. 归一算子对照（同 15 ops，只换基底里的归一算子）

| 变体 | 归一算子 | 语义 |
|---|---|---|
| 基准 | `ts_zscore(x, 504)` | 时序 z 分数 |
| `c_tsrank` | `ts_rank(x, 504)` | 时序百分位 |
| `c_mmdiff` | `ts_max_diff(x, 252)`（论坛 mm 结构成分） | 窗口极值差 |
| `c_avdiff` | `ts_av_diff(x, 252)` | 窗口均值差 |
| `c_tsquant` | `ts_quantile(x, 504)` | 时序分位 |
| `c_zscore` | `zscore(x)`（截面） | 截面标准化 |
| `c_tsmean` | `ts_mean(x, 504)` | 时序均值 |

### C. 事件时序对照（论坛杠杆 3/5）

| 变体 | 门控 | 语义 | ops |
|---|---|---|---|
| `t1_tw_mom` | `trade_when(ts_zscore(returns,63) > 0, ·, -1)` | 只在上行动量期在场 | 13 |
| `t2_tw_growth` | `trade_when(ts_delta(cap,63) > 0, ·, -1)` | 只在规模扩张期在场 | 13 |
| `h1_hump0001` | `hump(·, 0.0001)` | 极轻换手抑制 | 12 |
| `h2_hump0005` | `hump(·, 0.0005)` | 轻换手抑制 | 12 |

### D. 残差化对照（论文杠杆）

| 变体 | 构造 | ops |
|---|---|---|
| `r1_regression` | `group_rank(ts_regression(ts_zscore(F_bf,504), ts_mean(returns,63), 252), industry)` + cap桶 + 波动桶 | 14 |

## 七、决策门槛（预先设定，避免事后解释）

- **接受条件**：prod ≤ 0.685（留 0.015 余量）、eff=2、ops ≤ 15、RA 全过
- **若全部失败**：结论为「15 ops + eff=2 ⇒ prod 地板 = 0.6995（压线）」，
  此时按用户抉择 A（接受压线）/ B（eff=0 安全）/ C（换信号源）
- **预算**：本批 ≤ 12 次模拟（论坛建议每战役 ~50 次止损，本战役累计已用约 30 次）
