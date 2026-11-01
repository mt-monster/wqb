# GBR/D1/TOP700 · `fundamental86` 多支柱评分卡（Stock Reports Plus）模板库

> 区域：GBR · universe：TOP700（唯一档） · delay：1 · 全部 MATRIX
> 覆盖判定：**已验证有数据**（见 §2），平台 `coverage: 0.0` 是 bug
> 塔归属：**恒为 `GBR/D1/FUNDAMENTAL`**（见 §6，与用了哪根支柱无关）
> 建立：2026-10-31

---

## §1 数据集画像（7 字段全量）

全部 `MATRIX`，全部 `decile 1–10` 整数分（"higher is better"），**全部无量纲**
⇒ 单位闸零风险、天然截尾、TO 天然偏低。

| 字段 | 语义（平台 description 原文要点） | u / a | 拥挤度 | 首次实测 |
|---|---|---|---|---|
| `fnd86_average_score` | Overall composite aggregating **all pillars** | 56 / 69 | 中 | ✅ S 0.73–0.76 |
| `fnd86_earnings_score` | Earnings pillar：质量 + 修正 + 增长 | 60 / 72 | 中 | ✅ 见 T2 |
| `fnd86_fundamental_score` | Fundamental quality | 25 / 35 | **低** | 未测 |
| `fnd86_insider_trading_score` | Insider activity pillar | **1 / 2** | **极低（蓝海）** | 在飞 |
| `fnd86_price_momentum_score` | Price momentum（stronger recent trend 得高分） | 61 / 79 | 中 | 在飞 |
| `fnd86_relative_valuation_score` | Relative valuation vs peers in region | **119 / 191** | **最高拥挤** | ✅ S 0.06（位移）/ 见 T2 |
| `fnd86_risk_score` | Risk pillar，integer decile | 25 / 35 | **低** | ✅ 见 T2 |

数据集级 `coverage` 报 0.0 —— **不可信**，见 §2。

---

## §2 覆盖率判定：有数据，非假空缺（零成本 + 一次探针）

**外部侧证**（论坛帖 `42587179348119`「GBR/DEU 新地区不出货？」，87 赞 / 36 评论）：
GBR 首周全球提交数据集排行第 4 位，**17 个提交**，位于

```
sentiment27 (20) > intraday_pv_feats (19) > continuation_score (17)
> fundamental86 (17) > model110 (17) > news81 (17) > model36 (16) ...
```

⇒ 该数据集在 GBR **确定能出货**。

**探针侧证**（`rKRQG6vd` / `pwdQG6Lb`，decay 10 / INDUSTRY / trunc 0.05）：

| 口径 | 值 | 判读 |
|---|---|---|
| `longCount + shortCount` | 289+290 / 292+287 ≈ **579–580** | TOP700 的 **83%** 有持仓 ⇒ 覆盖充分 |
| `turnover` | 5.89% – 6.09% | 正常换手，非「无数据」的 0.00% |
| `margin` | **12.08 – 12.86 bp** | **高于 GBR 中位数 11.9 bp** ⇒ 单笔收益质量正常 |

**三条同时成立 ⇒ 有覆盖、有收益、只是幅度不足。** 与「无数据」的判据（`TO ≈ 0.00%` + `returns = 0.0`）明确区分。

---

## §3 已测模板与实测结果

设置一律 **GBR / TOP700 / D1 / decay 10 / INDUSTRY / truncation 0.05**
（FUND 族最优档，由 `QPvmbn2w` 族 2×2 因子设计确立）。

| # | 模板（骨架） | alpha | S | F | TO | 2Y | SUB | SUB/S | dd | margin |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|
| T1 | 水平 + 横截面 `rank` | `rKRQG6vd` | 0.73 | 0.39 | 5.89% | 0.68 | 0.30 | 0.41 | 13.93% | 12.08bp |
| T2 | 支柱 spread（盈利 − 风险） | `qMLeGkqv` | **0.26** | 0.08 | 6.33% | **−0.61** | 0.17 | 0.65 | 10.03% | 3.64bp |
| T3 | 位移（估值分 Δ252） | `WjOKzp5O` | **0.06** | 0.01 | 5.40% | −0.19 | 0.17 | 2.83 | 13.17% | **1.31bp** |
| T4 | 去掉 `rank` 层（保留幅度） | `pwdQG6Lb` | **0.76** | 0.43 | 6.09% | 0.71 | 0.35 | 0.46 | 15.86% | **12.86bp** |

四条 RA 失败项均为 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE`（T2、T3 无 SUB 失败，因 S 太低导致 SUB 门槛也低）。
`pyramids.list` 四条全部 `GBR/D1/FUNDAMENTAL`（multiplier 1.6）。

---

## §4 关键教训（本数据集专属，勿跨数据集照搬）

### 4.1 ★★★ decile 整数分**只适合做水平，不适合做差分**

`fnd86_relative_valuation_score` 取值是 1–10 的整数。`ts_delta(·, 252)` 之后剩下
−9…+9 的整数格，且绝大多数期次为 **0**（评分不常变）⇒ **位移信号的分辨率被离散化吃光**。

对照证据：

| 载体 | 位移几何 | 结果 |
|---|---|---|
| `rKRQbPPE`（连续比率 EBITDA/EV） | `ts_delta(·, 252)` | **S 2.48** |
| `fnd86_relative_valuation_score`（1–10 整数分） | `ts_delta(·, 252)` | **S 0.06**（margin 仅 1.31 bp） |

⇒ **机制没错，是字段的离散化不支持该机制。** 对 decile / 评级 / 分档类字段，
优先用**水平**、**时序分位**、**支柱间关系**，禁用一阶/二阶差分。

### 4.2 ★★ `rank` 层不是瓶颈

T1（有 `rank`）→ T4（无 `rank`）只带来小幅全面提升：

| 指标 | T1 有 rank | T4 无 rank | Δ |
|---|---:|---:|---:|
| S | 0.73 | 0.76 | +4.1% |
| F | 0.39 | 0.43 | +10.3% |
| SUB | 0.30 | 0.35 | +16.7% |
| margin | 12.08 bp | 12.86 bp | +6.5% |

⇒ 裸综合分的真实信息量就在 **S ≈ 0.76**，与「抹掉幅度」（`group_rank` 式重创）
的机制不同：这里是**去 rank** 而非**加更粗的横截面层**。方向上「少一层更好」，
但幅度小 ⇒ 不要再把仿真配额押在横截面层上。

### 4.3 ★★ 支柱 spread 反而伤 2Y

T2（盈利 − 风险）全期 S 0.26 / **2Y −0.61**。两条离散分相减后，
剩余的是「两支柱评级差异」，其经济含义被稀释成噪声；近期尤其反向。

⇒ 在评分卡体系内，**支柱间相减不是因子合成的好形式**。要组合支柱，
优先用**条件门控**（T9）或**比值**（T6），而不是等权相减。

### 4.4 ★ 支柱归塔与信号内容无关

无论用 `fnd86_price_momentum_score`（价格动量内容）还是 `fnd86_risk_score`，
`pyramids.list` 一律为 **`GBR/D1/FUNDAMENTAL`**。
⇒ **`fnd86_price_momentum_score` 可以合法地为 FUNDAMENTAL 塔贡献「动量类」alpha**，
这是 PV 池见底后补 FUND 塔的合法路径（不触碰塔混禁令，因为是单数据集单塔）。

---

## §5 模板池（13 个，结构互异，占位待实测填充）

多样性维度分布：**水平 / 位移 / 分位 / 比值 / 二阶矩 / 加速度 / 条件 / 分组相对 / 偏离 / 极值**，
覆盖 6 个信息加工层次，非「同一骨架换窗口」。

| # | 骨架结构 | 算子几何 | 矩 / 加工层 | 来源 | 状态 |
|---|---|---|---|---|---|
| T1 | 水平 + 横截面 rank | `rank(ts_backfill(F,66))` | 水平 | 自建 + **paper: Piotroski 2000 F-Score**（9 项打分合成思路） | ✅ S 0.73 |
| T2 | 支柱等权相减 | `rank(subtract(A,B))` | 水平差 | 自建 + **paper: Asness-Moskowitz-Pedersen 2013「Value and Momentum Everywhere」** | ✅ S 0.26 |
| T3 | 位移（一阶差分） | `rank(ts_delta(ts_backfill(F,66),252))` | 变化 | **paper: Bernard-Thomas 1989 反应不足** + 复用 `rKRQbPPE` 估值位移 | ✅ S 0.06 |
| T4 | 去横截面层（保留幅度） | `ts_backfill(F,66)` | 水平（原值） | 自建（归因对照） | ✅ S 0.76 |
| T5 | 时序分位 | `ts_quantile(ts_backfill(F,66),252)` | 位置 | 自建（decile → 自身历史位置） | 待测 |
| T6 | 支柱比值（同体系同单位） | `rank(divide(ts_backfill(A,66),ts_backfill(B,66)))` | 相对强度 | 自建 | 待测 |
| T7 | 加速度（二阶差分） | `rank(ts_delta(ts_delta(ts_backfill(F,66),66),252))` | 二阶 | 自建 | 待测（**T3 已示警，预期低**） |
| T8 | 时序稳定性 | `reverse(rank(ts_std_dev(ts_backfill(F,66),252)))` | 二阶矩 | **paper: 质量因子低波动（Novy-Marx 2013 / Asness QMJ）** | 待测 |
| T9 | 条件门控 | `trade_when(greater(rank(ts_backfill(G,66)),0.5), ts_backfill(F,66), -1)` | 条件 | **forum: TPL-009 信号质量分组**（帖 `37117908343831`） | 待测 |
| T10 | 行业内去均值（保留幅度） | `group_neutralize(ts_backfill(F,66), subindustry)` | 行业相对 | 自建 | 待测 |
| T11 | 综合分与支柱的偏离 | `rank(subtract(ts_backfill(avg,66), ts_backfill(pillar,66)))` | 残差 | 自建（捕捉「非基本面支柱贡献过大」） | 待测 |
| T12 | 极值 / 分位带 | `ts_rank(ts_backfill(F,66),252)` + 截尾 | 极值 | 自建 | 待测 |
| T13 | 位移 × 门控复合 | `trade_when(gate, delta, -1)` | 条件 + 变化 | 自建 | 待测（依赖 T3/T9 结论） |

**使用约束**：
- T3 / T7 / T13 的位移与加速度**前置条件是字段连续**。本数据集为 decile 整数分，
  已有 T3 反例 ⇒ T7 / T13 优先级最低，除非换到连续字段。
- T9 / T13 的门控腿必须是**同数据集**字段（`fnd86_*`），否则跨数据集会改变塔归属；
  且门控一律 `greater(rank(x), 0.5)`（单位闸约束）。
- T6 的分子分母**必须同单位**（都是 decile 分，天然满足）。
- T10 用 `group_neutralize` 而非 `group_rank`：后者是实测的 `SUB/S` 杀手
  （0.44 → 0.29，见 memory 2026-10-30）。

---

## §6 提交口径备忘

- 塔：`GBR/D1/FUNDAMENTAL`，multiplier 1.6。
- 全期区间：`startDate 2014-01-01` → `endDate 2023-12-31`（覆盖近十年，满足硬门槛）。
- 硬闸：`LOW_SHARPE` 1.58 / `LOW_FITNESS` 1.0 / `LOW_2Y_SHARPE` 1.58 /
  `LOW_SUB_UNIVERSE_SHARPE` ≈ **0.474 × S**（T4 实测 0.35 / 0.76 = 0.460，
  T1 0.30 / 0.73 = 0.411）。
- `CLUSTER_TEST` 在 T1/T4 报 **0.82–0.83**（warning，limit 1），T2/T3 只有 0.09
  ⇒ 前两者的信号高度集中于同一簇，**这与低 S 同时出现，说明信息被少数票主导**。

---

## §7 待办

1. 单支柱实测：`price_momentum` / `insider_trading`（在飞）、`fundamental` / `risk` / `earnings`。
2. T5 分位层与 T10 分组中性化（保留幅度的两条正路）。
3. T9 门控：用低拥挤支柱（`fundamental_score` 或 `insider_trading_score`）当门，
   高信号支柱当主体。
4. 若单支柱全部落在 S < 1.0，判本数据集为「**覆盖好、幅度弱**」，
   与 `fundamental6` 的会计比率族并列，停止投配额。
