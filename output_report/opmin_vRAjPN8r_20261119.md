# opmin vRAjPN8r · EUR ern6 单数据集聚类（ATOM）优化全记录

- 日期：2026-11-19
- 原件：`vRAjPN8r`（EUR / TOP2500 / D1 / SUBINDUSTRY / decay 2 / trunc 0.08）
- 原件表达式：`group_rank(ts_delta(divide(ts_backfill(vec_avg(ern6_actual_eps),500), add(abs(ts_backfill(vec_avg(ern6_estimated_eps),500)),1)),610), subindustry)`
- 约束：纯单数据集 `earnings6`（ATOM），沿用用户 11-19「优先 ATOM 方向」指令
- 规模：**18 批 / 71 颗仿真**

---

## §1 原件诊断

| 指标 | 值 | 闸门 | 判定 |
|---|---|---|---|
| Sharpe | 1.14 | 1.58 | ✗ |
| Fitness | 1.09 | 1.0 | ✓ |
| 2Y Sharpe | 0.90 | 1.58 | ✗ |
| sub-universe | 0.69 | 0.542 (=0.475×S) | ✓ |
| **CONCENTRATED_WEIGHT** | **0.1677** | 0.1 | ✗ |
| TO / DD / margin | 2.96% / 11.87% / 77bp | — | — |
| 塔 | `EUR/D1/EARNINGS ×1.2` | — | — |

`failed_ra_count = 3`（LOW_SHARPE / CONCENTRATED_WEIGHT / LOW_2Y_SHARPE）。

**逐年统计（决定性）**：2014–2020 **七年零仓位**，仅 2021–2023 有持仓：
- 2021：longCount **299** / shortCount 1538，S 1.46
- 2022：1242 / 1667，S **0.78**
- 2023：1189 / 1573，S 1.11

⇒ `ern6` 数据 2019 年中才起，叠加 `ts_delta(610)` 的 610 天回看 ⇒ 首个有效截面出现在 2021 年中，且 2021 年截面极窄（long 仅 299 只）。**这同时是 CW 与 2Y 两个失败项的同一物理根源。**

---

## §2 universe 扫描：非单调甜点 TOP800

| universe | 中性化 | S | F | 2Y | sub | margin | 备注 |
|---|---|---|---|---|---|---|---|
| TOP2500（原件） | SUBIND | 1.14 | 1.09 | 0.90 | 0.69 | 77bp | — |
| **TOP800** | **SUBIND** | **1.40** | **1.78** | **1.44** | 0.78 | **143bp** | `LLK7YdOa` |
| TOP1200 | COUNTRY | 0.86 | 0.78 | 0.92 | 0.70 | 81bp | — |
| TOP400 | SUBIND | **0.06** | 0.02 | −0.03 | — | 9bp | 完全崩溃 |

**TOP800 是甜点**：S +0.26、F +0.69、margin +66bp、R 11.4%→20.1%。TOP400 崩到 0.06，TOP1200 反而比 TOP2500 差 ⇒ **非单调**，与 GBR TOP700 的物理特性（700 只、ern6 覆盖集中在大中盘）对齐。

---

## §3 三条决定性技术发现

### 3.1 `ts_mean` 平滑是 S 的第一杠杆（63 天尖峰）

| 平滑窗口 | S | F | 2Y | sub | DD |
|---|---|---|---|---|---|
| 无（0） | 1.40 | 1.78 | 1.44 | 0.78 | 10.02% |
| 21 | 1.27 | 1.54 | 1.22 | 0.72 | 9.88% |
| **42** | **1.60** | **2.20** | 1.21 | 0.74 | 10.18% |
| **63** | **1.65** | **2.27** | 1.32 | **0.86** | **9.62%** |
| 105 | 1.30 | 1.61 | 0.90 | 0.11 | 23.1% |
| 126 | 1.31 | 1.64 | 0.95 | 0.44 | 24.1% |
| 252 | 1.32 | 1.67 | 0.96 | 0.48 | 24.4% |

**63 天是尖峰**（105 天起崩塌，DD 从 9.6% 涨到 23–24%）。机制：ern6 是季频事件数据，63 交易日 ≈ 一个季度，正好对齐信息更新周期；超过一季则把上一季的旧信息混入，破坏信号。

### 3.2 `truncation 0.02` 不伤绩效，反而小幅提分

| truncation | 结构 | S | F | sub | margin | CW |
|---|---|---|---|---|---|---|
| 0.08 | 双窗 ts_mean | 1.67 | 2.33 | 0.92 | 176bp | 0.2424 |
| **0.02** | 双窗 ts_mean | **1.79** | **2.60** | **0.97** | **186bp** | 0.2126 |
| 0.02 | 单窗 ts_mean63 | 1.74 | 2.48 | 0.91 | 173bp | — |

⇒ 收紧截断**同时**提升 S/F/sub/margin。但 CW 仅从 0.2424 降到 0.2126（−0.03），**证明 CW 检查的不是截断后的最终权重**。

### 3.3 分组轴与 neutralization 的完整图谱

| 分组轴（外层） | S | F | 2Y | sub | CW |
|---|---|---|---|---|---|
| **market** | **1.87** | **2.77** | **1.49** | 0.85 | **0.2435** |
| industry | 1.68 | 2.31 | 1.35 | 0.87 | — |
| sector | 1.55 | 2.06 | 1.19 | 0.87 | — |
| subindustry | 1.65 | 2.27 | 1.32 | 0.86 | 0.2424 |

**`market` 轴绩效最优（S 1.87 / margin 203bp），但 CW 更差（0.2435）** ⇒ CW 与分组轴无关。

**`COUNTRY` neutralization 在 TOP800 上全面失效**（0.55–1.04 vs SUBINDUSTRY 的 1.40）：欧洲国别因子不是本信号的相关维度，与「欧洲横截面差异主要在国别」的直觉**相反**。**`SUBINDUSTRY` neutralization 是必需的。**

---

## §4 CW 是物理硬约束（全部手段证否）

CW 打击日集中在 **2021-06-28 / 2021-08-30**（数据起量期）。CW 0.2160 ≈ 1/4.63 ⇒ **当日仅 4–5 只票能算出 `ts_delta(ratio,610)`**（需 2019-02 的 ratio，而 ern6 从 2019 年中起）。

七种尝试全部无效或反效：

| 手段 | 结果 |
|---|---|
| `group_neutralize(x, sector)` 内层 | CW 0.1677→0.1679（**无变化**） |
| `truncation 0.08→0.02` | CW 0.2424→0.2126（−0.03） |
| `ts_mean` 平滑 21/42/63/105/126/252 | 最好降到 0.2424（−0.017） |
| 分组轴 market/industry/sector | `market` 反而升到 0.2435 |
| `ts_backfill(signal, 250/300)` | S 崩（1.35/DD 23%，sub 0.36–0.43） |
| `group_backfill(signal, subindustry, 250)` | **S −0.86 / DD 60.4%**（灾难） |
| `if_else(is_nan(610腿), 252腿, 610腿)` 并集 | **S 0.51 / DD 31.6%**（窄截面样本被放大） |

**窗口—CW 的直接对照**：

| W | 平滑 | S | 2Y | sub | CW 状态 |
|---|---|---|---|---|---|
| 610 | 无 | 1.40 | 1.44 | 0.78 | 0.2593 ✗ |
| 610 | 63 | 1.65 | 1.32 | 0.86 | 0.2424 ✗ |
| **480** | 63 | **1.07** | 1.19 | 0.66 | 可通过（截面宽） |
| **504** | 63 | **1.01** | 0.99 | 0.03 | 可通过 |
| 480 | 无 | 0.91 | 0.98 | 0.60 | 可通过 |

⇒ **CW 要求 W ≤ 480，而 S ≥ 1.58 要求 W ≥ 610，两者互斥。** 这不是参数问题，是数据可用性决定的。

**趋势类算子（不需精确端点）同样救不了**：

| 算子 | S | 2Y | sub | CW 隐含 |
|---|---|---|---|---|
| `ts_regression(ratio, ts_step(1), 610, rettype=2)` 斜率 | 0.48 | 0.85 | 0.83 | 宽截面 ✓ |
| `ts_regression(..., 480, rettype=2)` | 0.54 | 1.00 | 0.93 | ✓ |
| `ts_corr(ratio, ts_step(1), 610)` | 0.47 | 0.71 | 0.89 | ✓ |
| `ts_rank(ratio, 750)` | 0.69 | 1.21 | 0.86 | ✓ |
| `ts_rank(ratio, 500)` | 0.69 | 1.15 | 0.80 | ✓ |
| `ts_delta(ratio, 610)` | **1.65** | 1.32 | 0.86 | 0.24 ✗ |

**全窗口算子把 sub 修到 0.83–0.93（截面宽），但 S 只剩 0.47–0.69。端点差分的信号强度不可替代。**

---

## §5 双窗结构的价值

`add(ts_mean(ts_delta(610),w), ts_mean(ts_delta(252),w))` 是本轮最优结构：252 腿补近期动量，610 腿保长期重估。

| 结构 | S | F | 2Y | sub | margin | DD |
|---|---|---|---|---|---|---|
| 单窗 610 × 63 | 1.65 | 2.27 | 1.32 | 0.86 | 161bp | 9.62% |
| 双窗 × 21 | 1.39 | 1.75 | 1.35 | 0.65 | 146bp | 9.70% |
| 双窗 × 42（subind 轴） | **1.85** | **2.74** | 1.44 | 0.84 | **197bp** | **8.63%** |
| **双窗 × 63（market 轴）** | 1.74 | 2.39 | **1.57** | **0.92** | 176bp | **8.27%** |
| 双窗 × 63（subind 轴） | 1.79 | 2.60 | 1.41 | 0.97 | 186bp | 10.69% |
| 三窗（+126） | 1.69 | 2.40 | 1.27 | 0.89 | 176bp | 11.55% |

**双窗把 2Y 从 1.32 抬到 1.57（+0.25）**，是 2Y 的最大杠杆。

---

## §6 最终候选（按失败项与绩效排）

| 件 | 结构 / 设置 | S | F | 2Y | sub | TO | DD | margin | R | 失败项 |
|---|---|---|---|---|---|---|---|---|---|---|
| **`zqdYqw3X`** | 双窗×63 · **market 轴** · trunc 0.02 | 1.74 | 2.39 | **1.57** | **0.92** | 2.67% | **8.27%** | 176bp | 23.5% | **2**（CW 0.2160、2Y 差 0.01） |
| **`6XMl5bkJ`** | 双窗×63 · subind 轴 · trunc 0.02 | 1.79 | 2.60 | 1.41 | **0.97** | 2.83% | 10.69% | 186bp | 26.3% | **2**（CW 0.2126、2Y） |
| **`xAvYAw1n`** | 双窗×**42** · subind 轴 · trunc 0.02 | **1.85** | **2.74** | 1.44 | 0.84 | 2.78% | **8.63%** | **197bp** | **27.4%** | 3（CW、sub、2Y） |
| `gJaQJqWe` | 610×63 + 126×63 · subind | 1.76 | 2.53 | 1.33 | **0.96** | 2.99% | 10.13% | 173bp | 25.8% | 2（CW、2Y） |
| `1YWwr5MX` | 单窗×63 · trunc 0.02 | 1.74 | 2.48 | 1.34 | 0.91 | 2.94% | **8.94%** | 173bp | 25.4% | 3 |
| `QP07xkJW` | 双窗×63 · trunc 0.08 | 1.67 | 2.33 | 1.36 | 0.92 | 2.76% | 11.84% | 176bp | 24.3% | 2（CW、2Y） |
| `0mPRmgWG` | 单窗×42 · market 轴 · trunc 0.02 | 1.83 | 2.67 | 1.43 | 0.85 | 2.93% | 9.26% | 181bp | 26.5% | 3 |
| `78Yje9b1` | 单窗×63 · market 轴 · trunc 0.08 | **1.87** | **2.77** | 1.49 | 0.85 | 2.71% | 10.89% | **203bp** | **27.5%** | 3 |

### 相对原件的改进幅度（以 `xAvYAw1n` 为例）

| 指标 | 原件 `vRAjPN8r` | `xAvYAw1n` | 变化 |
|---|---|---|---|
| Sharpe | 1.14 | **1.85** | **+0.71（+62%）** |
| Fitness | 1.09 | **2.74** | **+1.65（+151%）** |
| 2Y | 0.90 | 1.44 | +0.54 |
| sub | 0.69 | 0.84 | +0.15 |
| margin | 77bp | **197bp** | **+120bp（+156%）** |
| Returns | 11.36% | **27.39%** | +16.0pp |
| Drawdown | 11.87% | **8.63%** | −3.24pp |
| 失败项 | 3 | 3 | 未变（CW 换掉 S，2Y 仍在） |

---

## §7 六维（当季 Q4，N=141）

| 项 | 值 |
|---|---|
| distinct ops | **7**（`abs / add / divide / group_rank / ts_delta / ts_mean / vec_avg`） |
| ΔT1 | **+0.0091**（原件 6 ops / +0.0020） |
| fields | 2（`ern6_actual_eps` / `ern6_estimated_eps`） |
| ΔT2 | −0.0006 |
| T3 新增 | 0（`ts_mean`/`ts_delta`/`group_rank` 均已用过） |
| T4 新增 | **0**（两个字段已被 GBR `WjlAp92x`/`aka1eWJR` 本季消耗） |
| 塔 | `EUR/D1/EARNINGS ×1.2`（有效 1 席） |

`ts_mean` 是唯一新增算子，代价 ΔT1 +0.0071，换来 S +0.25——六维上是划算的。

---

## §8 结论与建议

### 结论

**`vRAjPN8r` 这条 EUR `ern6` 单数据集骨架，在 ATOM 约束下无法过全闸。** 绩效已优化到 S 1.85 / F 2.74 / margin 197bp（相对原件 +62% / +151% / +156%），但 **CW 与 S 是一对物理互斥量**：

- CW ≤ 0.1 需要 `ts_delta` 窗口 ≤ 480 天（截面宽）
- S ≥ 1.58 需要窗口 ≥ 610 天（信号强）
- 两者不可兼得，因 `ern6` 覆盖仅 52.6% 且 2019 年中才起

**最佳可用件（若 CW 闸口径放宽或平台数据历史前推，可直接取用）**：
- 收益最优 → `xAvYAw1n`（S 1.85 / F 2.74 / margin 197bp / DD 8.63%）
- 最接近全闸 → `zqdYqw3X`（仅 CW + 2Y 差 0.01）

### 建议的下一步（按成功率排）

1. **换区域到同规模市场**：GBR TOP700 上同一骨架已 ACTIVE（`aka1eWJR`，S 2.28）。但 **DEU TOP500 经实测无信号**（S 0.24 / 2Y −0.48，`ern6` coverage 实测 0.0），不可复制。
2. **换数据集**：EUR 的 `earnings6` 内 `eps_change_percentage_value` 实测**全零（死字段）**，`preliminary_eps_range_*` 未测（可作「盈利不确定性宽度」新机制）。脱离 ATOM 可回到 `analyst + institutions` 双腿（但混腿倍率降至 1.1、T2 涨到 6）。
3. **接受 CW 上限，转向高 T3 价值件**：`gJaQJqWe`（S 1.76 / sub 0.96 / 2Y 1.33）与 `6XMl5bkJ` 同为 2 FAIL，若后续 CW 无法突破，建议不在本族继续投入。

### 本轮沉淀的可复用判据

- **`ts_mean` 平滑窗口 = 信息更新周期**：季频事件数据用 63 交易日（≈1 季）是尖峰，105 天起崩塌。
- **`truncation` 收紧（0.08→0.02）可同时提升 S/F/sub/margin**，但**不修 CW** ⇒ 反证 CW 不是「截断后权重」。
- **`COUNTRY` neutralization 在 EUR 上失效**（0.55–1.04 vs SUBINDUSTRY 1.40）⇒ 国别不是本信号的相关维度。
- **`add(NaN, x) = NaN`** ⇒ 双窗相加会取交集而非并集，2021 年窄截面问题因此被放大而非缓解。
- **`ts_regression`/`ts_corr`/`ts_rank` 等全窗口算子**能修 CW（sub 0.83–0.93），但信号强度只有端点差分的 1/3（S 0.47–0.69）。
- **CW 与 sub 在 EUR TOP800 上对立**：subindustry 轴 sub 0.97 但 CW 0.21；market 轴 CW 0.24 且 sub 0.85 ⇒ 两轴皆败。

---

## §9 第二轮：从 3 FAIL 打到 1 FAIL（2026-11-19 14:00-15:40，又 15 批 ~45 颗）

### 9.1 终选 `KPgOY1lk` —— 9 项全 PASS，仅 CW 失败

```
group_rank(add(
  ts_mean(ts_delta(group_backfill(group_backfill(
    divide(ts_backfill(vec_avg(ern6_actual_eps),500),
           add(abs(ts_backfill(vec_avg(ern6_estimated_eps),500)),1)), sector, 20), market, 20), 610), 105),
  ts_mean(ts_delta(divide(ts_backfill(vec_avg(ern6_actual_eps),500),
           add(abs(ts_backfill(vec_avg(ern6_estimated_eps),500)),1)), 252), 105)
), market)
```
设置：EUR / **TOP800** / D1 / **decay 32** / **truncation 0.01** / SUBINDUSTRY 中性化 / pasteurization ON

| 指标 | 原件 `vRAjPN8r` | **`KPgOY1lk`** | 变化 |
|---|---|---|---|
| Sharpe | 1.14 | **2.48** | **+118%** |
| Fitness | 1.09 | **3.86** | **+254%** |
| 2Y Sharpe | 0.90 | **2.09 ✓ PASS** | +1.19 |
| sub-universe | 0.69 | **1.42 ✓ PASS** | +0.73 |
| margin | 77bp | **225bp** | **+192%** |
| Returns | 11.36% | **30.35%** | +19.0pp |
| Drawdown | 11.87% | **7.43%** | −4.44pp |
| **CW** | 0.1677 ✗ | **0.1671 ✗** | −0.0006 |
| failed_ra_count | **3** | **1** | −2 |

`checks.pass` 已包含：LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / LOW_SUB_UNIVERSE_SHARPE / **LOW_2Y_SHARPE** / MATCHES_PYRAMID。

### 9.2 突破链条（按贡献排序）

| # | 手段 | 效果 |
|---|---|---|
| 1 | universe **TOP800** | S 1.14→1.40（TOP2500 1.14｜TOP800 1.40｜TOP1200 0.86｜TOP400 0.06，**非单调**） |
| 2 | `ts_mean` 平滑 **63→105** | S 1.65→**2.28**（63 时 1.65；105 尖峰；115/125/135 回落 1.91/1.81/1.78） |
| 3 | `truncation 0.02→0.01` + `decay 16→32` | S 2.28→**2.48**、DD 8.62%→7.43%、margin 197→225bp |
| 4 | **`group_backfill` ratio 侧 market 组** | CW 0.2424→**0.1671** |
| 5 | **`group_backfill` 字段侧 sector 组** | 2Y 1.66→**2.01**（sector 2.01 ＞ market 1.99 ＞ industry 1.69 ＞ subindustry 1.61） |
| 6 | 双窗 **610 + 252** | 2Y 最大杠杆（单窗 610 仅 1.32；252/480/750 单窗全崩 S −0.39/0.16/0.73） |

### 9.3 `LOW_2Y_SHARPE` 的真实口径（官方文档 + 日频复算）

官方 `IS-Ladder` 表（D1）：FAIL **1.59**｜2/3/4/5 年 PASS **2.38**｜6 年 2.22｜7 年 2.06｜8 年 1.90｜9/10 年 1.74/1.59。
**turnover < 30% ⇒ PASS 阈值 × 0.85** ⇒ 2–5 年档实际 **2.023 ≈ 2.02**。

两个 limit 显示不同的原因：

| 件 | 2Y | 显示 limit | 含义 |
|---|---|---|---|
| `zqdYqw3X` | 1.57 | **1.58** | 2Y < FAIL 1.59，第一档直接失败，报 FAIL 阈值 |
| `XgaWrVPx` | 1.66 | **2.02** | 2Y > 1.59 但 < PASS，报未达标的 PASS 阈值 |

**实测验证为「固定 2 年」检查**：`0mPRvMA8` 的 3Y 日频复算 = **2.082 > 2.02**，平台仍判 FAIL（2Y 1.77）⇒ **必须 2Y 真实 ≥ 2.02**，不能靠更长窗口绕过。

复算方法：`get_record_set_data(alpha, "pnl")` 取累计 PnL → 差分 → `sqrt(250)×mean/std`，与平台口径一致（2Y 复算 1.8185 vs 平台 1.81）。

### 9.4 CW 0.167124 是绝对地板

**三重借用（sector→market→sector）与单层借用得到完全相同的 0.167124** ⇒ 2021-05-31 那天恒为 **6 只票、各 16.7%**。

根因：`ern6` 覆盖 2019 年中才起 + `ts_delta(610)` 需 610 天前数据 ⇒ 2021 年上半年全市场仅 6 只票可算。

| 证否手段 | 结果 |
|---|---|
| `truncation 0.01`（已最小） | CW 仍 0.1671（反证 CW 不是截断后权重） |
| `decay 32` | 无变化 |
| 字段侧 gb（subindustry/industry/sector/market/country） | sector/market 保持 0.1671；country/market 恶化到 0.4151/0.3216 |
| 三层 `group_backfill` | 完全相同 0.167124 |
| **TOP2500**（票数 ×3） | S 崩到 0.99–1.16 |
| `ts_count_nans` 门控 | S −0.54 / −0.96 / −0.01 |
| `pasteurization OFF` | S 1.88（3 FAIL） |
| `max_position ON` | 接口不支持 |

### 9.5 中间权衡表（CW 与 2Y 的对抗）

| 配置 | S | 2Y | sub | CW | FAIL |
|---|---|---|---|---|---|
| ratio 侧 gb only（`XgaW52Zl`） | 2.14 | 1.66 | 1.18 | **0.1671** | 2 |
| 字段 market + ratio（`kqaVR9od`，平滑105） | 2.28 | 1.99 | 1.23 | 0.3223 | 2 |
| 字段 sector + ratio（`wpoYXPZ1`，平滑105） | 2.39 | 2.01 | 1.36 | **0.1671** | 2 |
| **字段 sector + ratio + decay32 + trunc.01（`KPgOY1lk`）** | **2.48** | **2.09** | **1.42** | **0.1671** | **1** |

**关键转折点**：字段侧借用组从 market 换成 **sector**，在保持 CW 0.1671 的同时把 2Y 从 1.66 拉到 2.01；再叠加 decay 32 + truncation 0.01 把 2Y 推过 2.02。

### 9.6 本轮六维

| 项 | 值 |
|---|---|
| distinct ops | **8**（`abs / add / divide / group_rank / group_backfill / ts_delta / ts_mean / vec_avg`）；`group_backfill` 按官方脚注不计数 |
| ΔT1 | **+0.0162** |
| fields / ΔT2 | 2 / −0.0006 |
| T3 / T4 | +0 / +0 |
| 塔 | `EUR/D1/EARNINGS ×1.2` |

### 9.7 结论

**9 项测试全过，唯一剩余 CW 0.1671（限 0.1）**。差距 0.067，但已证明是「2021 年上半年全市场只有 6 只票可算」的物理地板——所有表达式层与 settings 层手段均已穷尽。

`KPgOY1lk` 的绩效（S 2.48 / F 3.86 / margin 225bp / DD 7.43% / R 30.35%）已远超同族 GBR 已提交件（`aka1eWJR` S 2.28 / F 2.16 / margin 22bp），唯一差别是 GBR 的 2021 年数据起点更早、截面更宽。

---

## §10 第三轮：group_cartesian_product 与 CW 的成因定论（2026-11-19 15:15-17:00，9 批 ~29 颗）

### 10.1 用户提问的直接回答：`group_cartesian_product` 有害且方向相反

`group_cartesian_product(g1, g2)`：把两个分组字段合成一个，**分组数变成 len₁ × len₂**（官方定义原文）。即它只能**细分**分组，永远不能变粗。

实测（终轴换成 gcp，其余同 `KPgOY1lk`）：

| 终轴 | S | 2Y | sub | DD | CW |
|---|---|---|---|---|---|
| `market`（对照 `KPgOY1lk`） | **2.48** | **2.09** | **1.42** | 7.43% | 0.1671 |
| `group_cartesian_product(subindustry, country)` | 1.89 | 1.61 | 0.90 | 16.81% | 0.1671 |
| `group_cartesian_product(subindustry, market)` | 1.74 | 1.42 | **0.40** | 16.37% | 0.1671 |

⇒ **全面变差，CW 一点没动**。原因：CW 需要「更多票 + 权重更分散」，gcp 只让每组票更少。
（注：静态门禁对 gcp 有单位误判——`Incompatible unit ... found "Unit[Group:1]"`，是 toolkit 未把 gcp 注册为分组算子，属假阳性。）

### 10.2 ★★★★★ 推翻旧结论：CW 不是「票太少」

**证据一**：`group_count(delta610, market)` 门控四档（20/30/60/120）结果**逐位完全相同**（S 2.12 / F 3.03 / 2Y 1.66 / sub 0.98 / DD 11.05% / CW 0.167124）⇒ **门控从未触发** ⇒ 凡 610 差分有值的日子，市场范围内有效票数恒 ≥120。

**证据二**：`longCount = 600`、`shortCount = 258`（858 只有仓位），不是 6 只。

⇒ 之前「2021-05-31 全市场只有 6 只票可算 `ts_delta(610)`（CW≈1/6）」的推论**错误**，应立即废弃。

### 10.3 ★★★★★ CW 的真正成因：平台中性化轴

把 settings 里的 neutralization 逐一替换（表达式完全不变）：

| neutralization | S | 2Y | sub（限值） | DD | CW | failed_ra |
|---|---|---|---|---|---|---|
| **SUBINDUSTRY** | **2.48** | **2.09** | **1.42 ✓** | 7.43% | **0.1671 ✗** | **1** |
| INDUSTRY | 1.70 | 1.71 | 0.79 ✗（0.90） | 14.42% | **PASS** | 2 |
| SECTOR | 1.58 | 1.50 ✗ | 0.77 ✗（0.84） | 17.00% | **PASS** | 2 |
| MARKET | 1.47 ✗ | 1.49 ✗ | 0.65 ✗ | 15.33% | **PASS** | 3 |
| FAST | 1.32 ✗ | 1.51 ✗ | 0.78 ✓ | 4.08% | **PASS** | 2 |
| STATISTICAL | 1.18 ✗ | 1.46 ✗ | 0.74 ✗ | 3.19% | PASS | 3 |

机制：**平台在最终 alpha 值上做行业去均值**。SUBINDUSTRY 时每个细分行业内各自中心化，行业组薄 ⇒ 少数票承担全部权重 ⇒ 单票 16.7%；换成 INDUSTRY/SECTOR/MARKET 相当于在更大的池里中心化 ⇒ 权重自然摊平 ⇒ CW 通过。

试图两者兼得（把去均值挪进表达式、平台留 MARKET）也失败：

| 表达式内 | S | 2Y | sub | CW |
|---|---|---|---|---|
| `group_rank(group_neutralize(sig, subindustry), market)` | 1.36 | 1.47 | 0.41 | PASS |
| `group_rank(group_neutralize(sig, sector), market)` | 1.50 | 1.62 | 0.55 | PASS |
| `group_rank(group_neutralize(sig, industry), market)` | 1.51 | 1.64 | 0.52 | PASS |

⇒ **这是「sub 检验 ↔ weight 检验」的两侧夹击**：sub 要求细分粒度（权重压在流动性好的票上），weight 要求权重分散。SUBINDUSTRY 满足前者必败后者；粗轴反之。

### 10.4 另外三条被证否的方向

| 尝试 | 结果 |
|---|---|
| `ts_backfill` 回看 500→750/1000/1500/2000 | **750 已饱和**（四者逐位同分：S 2.19/2Y 1.72/sub 1.03/DD 11.05%）；且全面劣于 500（S 2.48→2.19、2Y 2.09→1.72、sub 1.42→1.03、fail 1→3） |
| `add(leg610, leg252, filter=true)`（官方语法：NaN 当 0） | **灾难**：S 0.62/0.59、2Y 0.63。这是「并集」思路第 3 次独立证否（前两次：`if_else(is_nan)`、`group_backfill` 信号侧） |
| `group_count` 广度门控（trade_when + `greater(..., 20/30/60/120)`） | 四档逐位相同 ⇒ 门控从不触发；且整体劣于无门控（S 2.12 vs 2.48） |

### 10.5 论坛查证状态

- `search_forum_posts` 连续多次返回 `total_found: 0`（工具故障，非无结果）。
- 官方文档引用的关键帖「Why fundamental alphas always show Weight is too strongly concentrated or too few instruments are assigned weight」(post 8394917303575) 经 `read_forum_post` 与 WebFetch 双双确认**已 404 删除**。
- 但官方文档本身给出了确定规则（`alpha-submission` + `consultant-submission-tests`）：
  - Weight test = **「Max weight in any stock < 10%」**，且「**assigning zero weights to all stocks at the start of the simulation does not fail this condition, it only applies after the Alpha starts assigning weights**」。
  - 另一条触发条件：**「Too few stocks are assigned weight for significant number of days in a year」**，最小票数随 universe 变化。

### 10.6 本轮结论

**CW 的两侧夹击在本族内无解**：SUBINDUSTRY 中性化是本骨架 S 2.48 / 2Y 2.09 / sub 1.42 的唯一来源，但它同时在数学上导致单票权重 16.7%。改任何其他中性化轴都能让 CW 通过，代价是 S 掉到 ≤1.70，sub 与 2Y 随之失败。

`KPgOY1lk`（SUBINDUSTRY，S 2.48 / F 3.86 / 2Y 2.09 / sub 1.42 / DD 7.43% / margin 225bp / R 30.35%，**9 项 PASS，仅 CW 0.1671 FAIL**）仍是本族最优件。若要提交本族，唯一现实路径是**换数据集**（换掉 `ern6` 对 610 天历史长度的依赖），而不是继续在表达式/参数层找解。

---

## §11 第四轮：换字段（2026-11-19 15:56-17:50，7 批 26 颗）

### 11.1 动机

CW 的成因是「平台 SUBINDUSTRY 中性化 + 早期某日仅少数细分行业有 ≥2 只有效票」。若换一个**历史更长 / 覆盖更宽**的字段，早期截面就会填满，CW 从根上消失。故本轮系统性地替换 `earnings6` 内的字段，并试同 pyramid 的另一数据集。

### 11.2 字段替换结果（全部负面）

| 字段 / 机制 | 覆盖 | S | 2Y | sub | 结论 |
|---|---|---|---|---|---|
| `ern6_actual_eps`（现用，对照） | 0.5258 | 2.48 | 2.09 | 1.42 | 基准 |
| **`ern6_actual_eps_274`**（旧版 2024-06 建，含 gb 全套） | 0.5367 | 2.12 | 1.66 | 0.98 | **更差**；两个字段 id 数值不同、历史不更长 |
| 同上但去掉 gb 层 | — | 1.62 | 1.16 | 0.59 | 差 |
| `ern6_actual_eps_274` 水平（`ts_mean` 105） | — | 0.25 | −0.28 | 0.10 | 无信号 |
| **`eps_change_absolute_value`**（已是变化量，无需长回看） | 0.5258 | **0.00** | — | — | **死字段（全零，TO=0）** |
| 同上 + `ts_delta(252)` | — | **0.00** | — | — | 死 |
| `preliminary_eps_range` 宽度（`(U−L)/(|U|+|L|)`） | 0.5258 | −0.49 | 0.59 | −0.44 | DD **81%**，噪声 |
| `ern6_x_dividend` 增长 `ts_delta(252)` | **0.9258** | 0.06 | −0.05 | 0.35 | 无信号 |
| `ern6_x_dividend` 水平 `ts_zscore(504)` | 0.9258 | 0.10 | 0.28 | 0.22 | 无信号 |
| `ern6_x_dividend_oc` 水平 | 0.9258 | 0.35 | 0.14 | 0.46 | 无信号 |

**`earnings_sent_matrix`（同 `earnings` 类另一数据集，7 个矩阵字段）全族无信号**：

| 字段 | S | 2Y |
|---|---|---|
| `overall_sentiment_score`（ts_zscore 252） | −0.11 | −0.11 |
| `sentiment_weighting_method1` | −0.08 | −0.65 |
| `sentiment_weighting_method2` | −0.08 | −0.51 |
| `(pos−neg)/(pos+neg)` | 0.55 | 0.13 |
| `ts_delta(overall_sentiment_score, 252)` | 0.11 | 0.84 |

（另：`preliminary_eps_range` 首次提交报单位错 `add at index 1, expected Unit[CSPrice:1], found Unit[]` —— 价格量不能加常数 1，改用 `add(|U|,|L|)` 作分母。）

### 11.3 新试的两个组合（均未成功）

**(a) 让「排序轴 = 中性化轴」**：`group_rank(sig, subindustry)` + 平台粗轴中性化。理论上值在每个细分行业内已均匀分布，平台只扣近似常数，权重不应再集中：

| 平台中性化 | S | 2Y | sub | CW |
|---|---|---|---|---|
| MARKET | 1.29 | 1.38 | 0.30 | **PASS** |
| INDUSTRY | 1.46 | 1.58 | 0.33 | **PASS** |

⇒ CW 通过，但 `group_rank(subindustry)` 这个终轴本身就把跨行业的维度删掉了，S 从 2.48 掉到 1.3–1.5，sub 掉到 0.3。

**(b) 并列值填充（用高覆盖股息字段做 tie-breaker）**：`add(SIG, k · rank(ern6_x_dividend))`，k = 1e-5 / 1e-3 / 5e-2：

| k | S | 2Y | sub | CW | DD |
|---|---|---|---|---|---|
| 三档**结果完全相同** | 1.71 | 1.58 | **1.61 ✓** | **0.2161**（@2021-06-28） | 7.32% |

⇒ 有趣但不够：**sub 大幅改善到 1.61**（原 1.42），可是 CW 反而从 0.1671 恶化到 0.2161，且三档量级结果逐位相同（扰动被末端 `group_rank` 重新排序吸收）。

### 11.4 扩 universe 无效（决定性反证）

同一最优表达式，仅换 universe（SUBINDUSTRY / decay 32 / trunc 0.01）：

| universe | S | 2Y | sub | CW |
|---|---|---|---|---|
| **TOP800（基准）** | **2.48** | **2.09** | **1.42** | **0.1671** |
| TOP1200 | 1.11 | 0.89 | 0.83 | **0.1616** |
| TOP2500 | 0.66 | 0.25 | 0.51 | — |

⇒ **票数变成 1.5 倍，CW 只从 0.1671 降到 0.1616**；S 却崩掉 55%。这再次证明权重集中与「股票池大小」无关，而是「早期某日只有约 6 个细分行业凑得出 2 只有效票」的结构性事实。

### 11.5 本轮结论

**EUR `earnings6` 的数值字段已被挖尽**：EPS 双字段（已用）、`eps_change_*`（全零死字段）、`preliminary_eps_range_*`（纯噪声）、`x_dividend*`（无信号）、`earnings_sent_matrix`（整族无信号）、客户类/文本类字段不可做数值信号。

`KPgOY1lk` 仍是本族唯一「9 项 PASS、仅 CW 0.1671 一项失败」的件（S 2.48 / F 3.86 / 2Y 2.09 / sub 1.42 / DD 7.43% / margin 225bp / R 30.35%）。

若目标是「在 EUR 交出一颗能过的 alpha」，`6XMloL2J`（analyst ATOM，`group_neutralize(signed_power(group_zscore(divide(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks), est_12m_ebi_num_4wks_ago), sector), 2.1), market)`，TOP2500 / decay 40 / FAST）是**唯一 `fail=[]` 9 项全 PASS** 的件（S 1.79 / F 1.21 / 2Y 1.59 / sub 0.93 / ops 5 / fields 3 / ΔT1 −0.0051 / T4 +1），只是 `EUR/D1/ANALYST` 塔已点亮（当季 10 颗）。
