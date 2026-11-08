# DEU ATOM 战役 · Wave 23 / Wave 24 分段判定台账

- 日期：2026-11-12
- 区域设置（固定）：`region=DEU` / `universe=TOP500` / `delay=1` / `neutralization=SUBINDUSTRY` / `decay=4` / `truncation=0.08` / `nanHandling=OFF` / `pasteurization=ON` / `unitHandling=VERIFY` / `maxTrade=OFF`；仿真区间 2014-01-01 ~ 2023-12-31
- 硬闸：`S≥1.58`、`F≥1.0`、`2Y≥1.58`、`0.01≤TO≤0.7`、`sub_u ≥ 0.474×S`、`failed_ra=0`、`self<0.7`、`prod<0.7`

---

## 一、Wave 23：`institutions6` → **判死**

- 批次：`1HH5N7aFq5gBavw1gFfWRhpw`（10/10 REJECT）
- 字段画像：coverage **1.0000** / 11 字段全 MATRIX / alphaCount **270** / userCount —
  - 这是全 DEU `alphaCount/字段数 = 24.5` 最密集的数据集，属「机构持仓披露计数」族：`count_institutional_{buyers,sellers,holders}_security`、`market_value_institutional_shares_{acquired,disposed}`、`quantity_institutional_shares_{acquired,disposed}`、`aggregate_{equity_value,share_count}_institutions`
  - 全部为**原始计数/金额**，必须先比率归一化才能跨截面比较（本波 10 条全部做了归一化）
- 派出动因：带上 KOR 已验冠军骨架 `trade_when(ts_arg_max(HOLDERS,90)<33, signed_power(ts_quantile(BUYERS/ts_mean(HOLDERS,72),840,gaussian),1.6), -1)`（该骨架在 KOR 上拿到 FT>1.0 首破点）

| # | 模板 | 字段 / 几何 | alpha | S | F | **2Y** | TO | sub_u | failed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| M1 | ★KOR 冠军骨架 trade_when 门控 | BUYERS/ts_mean(HOLDERS,72)，W840，p=1.6 | KPJZxbZx | 0.20 | 0.06 | 0.58 | 0.0803 | **−0.08** | 4 |
| M2 | 净买入广度差 | (buyers−sellers)/holders，W66 | YP1YN26M | −0.01 | −0.00 | −0.08 | 0.0252 | 0.21 | 3 |
| M3 | 净买入金额占比 | (mv_acq−mv_disp)/aggregate_equity_value，W66 | LLM3ngja | −0.27 | −0.09 | −0.28 | 0.0232 | 0.17 | 3 |
| M4 | 股数周转 | qty_acq/aggregate_share_count，W66 | xAr5eP6n | −0.44 | −0.19 | −0.03 | 0.0278 | −0.21 | 3 |
| M5 | 覆盖广度季度变化 | ts_delta(ts_mean(holders,22),66) | WjOJNaqo | 0.29 | 0.11 | 0.48 | 0.0431 | **0.45** | 3 |
| M6 | 异窗 132/11 双窗 add | (buyers−sellers)/holders | npvrnZRx | 0.04 | 0.01 | 0.11 | 0.0306 | 0.35 | 3 |
| M7 | 逆方差加权 | group_rank(buyers/holders)/std²，decay30 | omEZn35v | **0.37** | **0.17** | 0.30 | 0.0356 | 0.22 | 3 |
| M8 | 卖出压力反向 | −sellers/holders，W66 | 6XdNRaVG | −0.15 | −0.04 | 0.03 | 0.0228 | 0.10 | 3 |
| M9 | 双层广度 multiply | rank(buyers/holders)×rank(mv_acq/eq_value) | Xg9Mk2Q0 | 0.16 | 0.04 | 0.20 | 0.0286 | 0.07 | 4 |
| M10 | 净买入股数 z 252 | ts_zscore((qty_acq−qty_disp)/share_count,252) | mLoQqrM2 | 0.09 | 0.02 | **1.20** | 0.0388 | 0.04 | 3 |

### 判定要点

1. **S 上限 0.37 / F 上限 0.17 / 2Y 上限 1.20** ⇒ 三项全部远低于闸线，无任何一条接近。
2. **KOR 冠军骨架在 DEU 上 S 只有 0.20，sub_u −0.08** ⇒ 同一骨架跨区不可移植。KOR 的 institutions6 有效性来自韩国机构披露密度与散户结构，德国 TOP500 的机构持股已高度饱和（coverage=1.0 反而是坏事：所有票都有值 ⇒ 无区分度）。
3. **方向混乱**：10 条里 5 条正 5 条负，最大绝对值 0.44 ⇒ 无稳定符号，属纯噪声。
4. **M10 是唯一亮点**：`ts_zscore(净买入股数占比, 252)` 2Y **1.20**，但 S 只有 0.09、sub_u 0.04 ⇒ 典型的「2Y 高但整体无信号」，不可用。
5. `coverage=1.0` 在本区第二次反向验证：Wave 19 model28 的 7 个 cov=1.0 rank 字段跑出 S≈0.00；本集全部 11 字段 cov=1.0 跑出 S 上限 0.37。

### ★ 新增判据：`coverage = 1.0` 在 DEU 是**负向信号**

**机理**：DEU TOP500 只有 500 只大票，coverage=1.0 意味着该实体对每一只票都有记录 ⇒ 该字段在截面上要么是慢变常量（如机构持股比例），要么是披露口径统一后的普适统计量，**缺乏横截面区分度**。
- 实证：`institutions6` cov 1.0 → S 上限 0.37；`model28` 7 个 cov 1.0 字段 → S≈0.00；`risk88` cov 1.0（单字段市值）未测但同族。
- 反证：出货的 6 颗全部来自 cov 0.57–0.92 的数据集（predictive_starmine 0.86 / analyst93 0.60 / sentiment27 0.90 / sentiment7 / model216）。
- **落地**：选集时 `cov=1.0` 应在体检阶段降权，而不是优先（与「覆盖率只作下限筛」一致，本波给出上限方向的反向证据）。

---

## 二、Wave 24：`analyst_factor_signals` → **命中本区最强新信号（继续深挖）**

- 批次：`1ViKkJc9W4QobFfiJbOFxDu`（10/10 REJECT，但出现结构突破）
- 字段画像：coverage **0.5996**（顶层）/ 实际高价值字段 cov ≈ **0.92** / 108 字段全 MATRIX / alphaCount **1575**
- 结构：`{eps|netprofit|revenue}` × `{q1|q2|y1|y2}` × `{consensus_value / estimate_change_3mo / estimate_change_1mo / revision_magnitude / coeff_var / skewness / asymmetry / cagr_2-5yr / trend_slope / yoy_growth / qoq_growth / surprise_*}`
- 派出动因：`alphaCount/字段数 = 14.6`，全 DEU 第二密集（仅次于 institutions6）

| # | 模板 | 核心字段 | alpha | S | F | **2Y** | TO | sub_u | failed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| M1 | 水平探针 W22 | eps_revision_magnitude | 3qoJEnR6 | 0.69 | 0.36 | 0.45 | 0.0510 | 0.45 | 3 |
| M2 | 异窗 132/11 | revenue_revision_magnitude | YP1YNW0M | 0.79 | 0.47 | 0.70 | 0.0489 | 0.10 | 4 |
| M3 | ★水平 W22 | **eps_y1_estimate_change_3mo** | bl6ANWqK | **1.57** | **1.29** | **1.01** | 0.0481 | **0.64** | 3 |
| M4 | 三口径广度 | 三个 revision_magnitude | mLoQqxbE | 0.71 | 0.38 | 0.42 | 0.0507 | 0.38 | 3 |
| M5 | 增长预期 W22 | eps_y1_cagr_2yr | 9qxk9A7o | −0.07 | −0.01 | 0.13 | 0.0226 | 0.30 | 3 |
| M6 | 逆方差 | eps_revision_magnitude | P0oKnXOp | 0.70 | 0.38 | 0.04 | 0.0478 | 0.17 | 4 |
| M7 | 偏度反向 | revenue_y1_estimate_skewness | pwd3n1Kx | 0.37 | 0.13 | **0.94** | 0.0562 | 0.31 | 3 |
| M8 | 动量 ts_delta 66 | netprofit_y1_estimate_change_3mo | mLoQqxVE | 0.67 | 0.34 | 0.45 | 0.0630 | 0.04 | 4 |
| M9 | 双确认 multiply | eps_revision_magnitude × eps_y1_change_3mo | QPv6n5Gr | **1.29** | 0.95 | 0.82 | 0.0492 | 0.53 | 4 |
| M10 | 共识预期水平 | revenue_y1_consensus_value | rKR8br2j | −0.21 | −0.07 | −1.10 | 0.0270 | −0.10 | 3 |

### ★★★ 核心发现：`*_estimate_change_3mo` 族是本区第 5 个真信号维度

`bl6ANWqK` = `group_rank(ts_mean(eps_y1_estimate_change_3mo, 22), industry)`，**2 个算子**，指标：

| 指标 | 值 | 闸线 | 差 |
|---|---:|---:|---:|
| Sharpe | **1.5700** | 1.58 | **−0.01** |
| Fitness | 1.2900 | 1.00 | ✓ +29% |
| 2Y Sharpe | 1.0100 | 1.58 | −0.57 |
| Turnover | 0.0481 | [0.01, 0.7] | ✓ |
| sub_universe | 0.6400 | 0.744 | −0.14 |
| investability_sharpe | 1.2200 | — | **> sharpe（真信号标记）** |
| margin | 0.003525 | — | 高（低换手高收益） |
| drawdown | 0.0805 | — | 低（全战役最低之一） |

**三重意义**：
1. **本战役唯一一颗用 2 个算子就拿到 S 1.57 的件**（所有已交付件都用 6–12 个算子）。
2. S 只差 **0.01** —— 任何轻微的几何调整都可能越线；这是 25 波以来最近的一次。
3. `investability_sharpe 1.22 > sharpe 1.57 的 78%` + `sub_u 0.64` 说明信号不是规模伪影（对比 model238 全波 sub_u ≤0.38）。

**失败闸解读**（`ra_failed_checks = [LOW_SHARPE, LOW_SUB_UNIVERSE_SHARPE, LOW_2Y_SHARPE]`）：
- `LOW_SHARPE 1.57 / limit 1.58` ⇒ 差 0.01，是**唯一** 0.01 级差距。
- `LOW_SUB_UNIVERSE_SHARPE 0.64 / limit 0.74` ⇒ 缺口 14%，需要 sub_u 与 S 同步提升（闸线 = 0.474×S，提 S 会把闸线一起推高）。
- `LOW_2Y_SHARPE 1.01 / limit 1.58` ⇒ **唯一的刚性瓶颈**，缺口 56%。

### 判定要点

1. **本数据集的有效维度 = `estimate_change_3mo` 族（3 个月分析师共识修正），不是 `revision_magnitude` 族**。
   - `revision_magnitude` 三个口径 S 全部落在 0.69–0.79（M1/M2/M4）⇒ 已被平台充分挖掘（`eps_revision_magnitude` 单字段 alphaCount 88–299），边际递减。
   - 而 `estimate_change_3mo` 的 `eps_y1_*` 单字段 alphaCount **506**（全数据集最高）却是唯一跑出 S 1.57 的字段。
2. **`eps_y1_cagr_2yr` 与 `revenue_y1_consensus_value` 双双无效**（−0.07 / −0.21，后者 2Y −1.10）⇒ 增长预期与共识水平不是信号，**只有"变化率"是信号**。这与 memory 中「期限结构族彻底封盘」互补：**水平量全部无效，变化量有效**。
3. **逆方差模板第 5 次失效**（M6 S 0.70，2Y 0.04）。分子 `eps_revision_magnitude` 本身 S 0.69 ⇒ 逆方差确实不是提 S 工具，且这次连 2Y 都没提到（0.04，全波最差）。
4. **偏度反向 M7 的 2Y 0.94 是全波第二高**，但 S 只有 0.37 ⇒ 再次印证「2Y 由字段定、S 由几何定」。
5. **`multiply` 双确认 M9 S 1.29** 是本波第二强 ⇒ `multiply` 在 DEU 不杀信号（第 3 次验证）。

### 与已交付件的关系

- `bl6ANWqK` 的 pyramid = `DEU/D1/ANALYST`（与已交付 `QPv6jLvX`（analyst93）同塔），但**数据集不同、字段完全不同** ⇒ 严格 ATOM 合格，且互相关预期低（待实测）。
- ANALYST 塔当前已提交 0 颗（全部 UNSUBMITTED）⇒ 塔未点亮，仍可开采。

---

## 三、本段两条新判据（累积入库）

### ★★★ 判据 A：`estimate_change_3mo` 是"变化率"信号，不是"水平"信号

同一数据集 `analyst_factor_signals` 内的对照组（同几何 `group_rank(ts_mean(F,22), industry)`，只换字段）：

| 字段 | 语义 | S |
|---|---|---:|
| `eps_y1_estimate_change_3mo` | 3 个月变化率 | **1.57** |
| `eps_revision_magnitude` | 修正幅度（已充分挖掘） | 0.69 |
| `eps_y1_cagr_2yr` | 增长 CAGR（水平） | −0.07 |
| `revenue_y1_consensus_value` | 共识水平 | −0.21 |

⇒ **只有"变化率"维度的有信号，水平量族（consensus_value / cagr / trend_slope）全部无效。**
这与「期限结构族 `subtract(近端,远端)` 彻底封盘」不矛盾：期限差是**跨期结构差**，共识修正是**同期限本期变化**，机制不同。

### ★★ 判据 B：`coverage = 1.0` 在 DEU 是负向信号（见 Wave 23 节）

---

## 四、后续动作（本段已派发）

| 波次 | 批次 ID | 数据集 | 机制 | 目的 |
|---|---|---|---|---|
| **Wave 25** | `WSN8b1yM4w5ba9CK7Ohlvw` | `analyst_factor_signals` | `estimate_change_3mo` 族深挖，10 个结构互异模板 | 破 S 1.58 / sub_u 0.74 / 2Y 1.58 三闸 |
| **Wave 26** | `3GH368axV5fn9ilrTOrCipm` | `fundamental6` | 经典会计异象（Gross Profitability / ROA / Sloan 应计 / 资产增长 / 杠杆 / Capex / R&D / 毛利率扩张 / 营运资本 / 三口径盈利质量） | FUNDAMENTAL 塔首开，机制与已出货四塔全正交 |

**Wave 25 十模板结构清单**（全部 ≤9 算子）：

| # | 结构 | 窗口/算子 | 算子数 |
|---|---|---|---:|
| T1 | 异窗双窗 add | 132/11 | 6 |
| T2 | 异窗双窗 add | 66/5（13.2× 倍率） | 6 |
| T3 | 异窗双窗 add + 换 y2 期限 | 132/11 | 6 |
| T4 | 异窗双窗 add + 净利口径 | 132/11 | 6 |
| T5 | 异窗双窗 add + 营收口径 | 132/11 | 6 |
| T6 | 三窗 add 阶梯 | 66/22/5 | 8 |
| T7 | 三 metric 广度 | 66 同窗 | 7 |
| T8 | 非线性 signed_power + ts_zscore 252 | 22 / 252 / p=3 | 4 |
| T9 | 逆方差（分子首次有信号） | 22 / decay30 | 9 |
| T10 | bucket 分组 + group_neutralize（QPvzNNGG 2Y 2.18 结构） | 12/252 + 0.05 桶 | 7 |

设计依据：已交付 6 颗的 2Y 全部 ≥1.69，而它们**全部**使用「双窗/多窗 add」或「bucket + group_neutralize」结构；单窗 `ts_mean(·,22)` 只有 2Y 1.01。故 Wave 25 以「异窗 add 族」为主轴押注 2Y。

---

## 五、累计进度（截至本段）

- **合格件 6 颗（全闸通过，全 UNSUBMITTED）**，严格单数据集 ATOM **4 颗**，剔除违禁 `E56pROb9`（MODEL+MODEL）后 **5 颗**。
- **判死/判弱数据集累计 89 个**（含 cov=0 的 44 个）；本段 +2：`institutions6`（判死）、`analyst_factor_signals`（**命中，继续深挖**）。
- **已确认的真信号维度共 5 个**：predictive_starmine `f12m` / analyst93 `profitability2` / shortinterest3 `shrt3_bar` / sentiment27 `relpopularity08` / **analyst_factor_signals `estimate_change_3mo`**。
- **2Y 仍是本区系统性病灶**：Wave 14–19 共 50 条 alpha 中 2Y >1.58 的一条都没有；本段 Wave 24 最高 2Y 1.20（M10）与 1.01（M3）。
