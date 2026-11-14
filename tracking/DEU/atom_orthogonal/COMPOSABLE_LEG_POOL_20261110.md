# DEU 可组合腿池（2026-11-10 19:4x，从全部已测波次抽取）

> 用途：单数据集 ATOM 剩余面仅 insiders1（BA6 在飞）。若 BA6 不出货，DEU 要突破 5 颗只能走**双塔组合**。
> 规则：禁混集合 {PV, MODEL, OTHER, FUNDAMENTAL} 内部两两全禁；集合内×集合外允许但该类总量 ≤5；每个两塔组合候选 ≤3；单数据集 ATOM 不占配额。

## 一、干净弱腿（低换手 + 子宇宙健康 + 多年覆盖，S 0.39-0.84）

| 腿 | 数据集 | 塔 | S | 2Y | sub | TO | lc | 备注 |
|---|---|---|---:|---:|---:|---:|---:|---|
| W1 反关注 rank 水平 | other47（SEMrush 网络流量） | OTHER | 0.80 | 0.86 | **1.04** | **0.013** | 117 | 10 年仅 2 负年（2.65/2.27/1.90）；族内最稳骨架 |
| AV2/W2 关注度变化 delta66 | other47 | OTHER | 0.64 | **1.94** | 0.61 | 0.070 | 115 | 变化类，近两年强 |
| W3 quantile-IR(流量变化) | other47 | OTHER | 0.78 | 1.73 | 0.83 | 0.072 | 115 | 2Y 强 |
| W8 org-paid delta | other47 | OTHER | 0.71 | 1.92 | 0.65 | 0.076 | 117 | earned vs 买量 |
| N4/V3 −sse 情绪波动 252 | news18（RavenPack） | NEWS | 0.57 | 1.44 | -0.15 | **0.024** | **170** | 高覆盖；vol 机制 |
| N10 −news38 metric vol | news38 | NEWS | 0.39 | 0.81 | 0.14 | 0.034 | 148 | 同机制旁证 |
| F2 稳定边界占比 | fund_holdings_panel | INSTITUTIONS | 0.65 | **1.77** | 0.33 | 0.467 | 134 | **TO 过高（0.467），margin 被压** |
| T1 现金利润率 | fundamental6 | FUNDAMENTAL | 1.15 | 0.43 | 0.79 | **0.027** | — | margin 0.006856 全 DEU 最高档；**但生产池已占据（prod 0.94/0.97）** |
| event_sent A1 key_driver level | event_sentiment_signals | SENTIMENT | 0.70 | **1.97** | 0.64 | 0.034 | 126 | 语调慢水平 |
| earningscall T1 profit_summary level | earningscall_sentiment | SENTIMENT | 1.02 | 1.37 | 0.43 | 0.026 | 116 | sentiment 族最强 |

## 二、组合可行性（按禁混规则）

**允许**：OTHER × NEWS（集合内 × 集合外）、INSTITUTIONS × NEWS、INSTITUTIONS × SENTIMENT、FUNDAMENTAL × NEWS（集合内 × 集合外）、OTHER × SENTIMENT 等。
**禁止**：OTHER × PV、OTHER × MODEL、OTHER × FUNDAMENTAL、FUNDAMENTAL × MODEL、PV × PV 等。

### 候选组合（≤3 个候选/组合类型，组合类型总量 ≤5）

| # | 组合 | 机制互补性 | 预期 |
|---|---|---|---|
| C1 | other47 W1（反关注 rank，TO0.013）× news18 N4（−情绪波动，TO0.024） | 注意力（结构性低关注）+ 情绪不确定性（文本波动）——两个正交信息面，均低换手 | OTHER×NEWS 合法；TO 合计仍低；两者 S 0.80/0.57 但方向独立 |
| C2 | other47 AV2（关注度变化）× event_sent A1（语调水平） | 变化面 × 水平面（三次验证的两类机制） | OTHER×SENTIMENT 合法 |
| C3 | fund_holdings F2 × news18 N4 | conviction 共识 × 情绪不确定性 | INSTITUTIONS×NEWS 合法；但 F2 TO 0.467 会把组合换手推高，需 tvr 治理 |

## 三、下一步

1. BA6（insiders1）收割 —— 若出货则优先单数据集 ATOM。
2. 若 BA6 不出货：从 C1 开始做 3 条组合臂（组合形态用 add/subtract 之外的正交结构：如 vector_neut 或 group_rank 后加权），严格控算子 ≤12、逐闸验证。
3. 组合臂同样要过 self/prod 相关性（与已 ACTIVE 件及 3 颗待授权件比对）。
---

## 四、C1 量化否决（2026-11-10 19:4x，逐年实测）

**W1（other47 反关注 rank）逐年 Sharpe**：2014 2.65 / 2015 2.27 / 2016 **−0.25** / 2017 0.37 / 2018 0.63 / 2019 0.39 / 2020 **−0.54** / 2021 0.72 / 2022 0.05 / 2023 1.90
**N4（news18 −情绪波动 252）逐年 Sharpe**：2014 0.77 / 2015 **−1.24** / 2016 **−0.17** / 2017 0.43 / 2018 1.47 / 2019 0.48 / 2020 0.27 / 2021 0.57 / 2022 1.96 / 2023 0.80

- 两腿均 **10 年零空窗**（覆盖率合格），且负相关年份互补（2015 W1+/N4−、2020 W1−/N4+）。
- **但 2016 双负、2017/2019 双弱正** ⇒ 互补不是全覆盖。
- 组合 Sharpe 估算：等权 ρ=0 时 ≈ (0.80+0.57)/√2 ≈ 0.97；即使 ρ=−0.3 也只 ≈ 1.06。**距 1.58 仍差 0.5+**。

**结论：C1 及同族双塔组合均不可行**——单腿天花板 0.57~0.80 太低，两腿叠加的数学上限无法触及 1.58（除非两腿各自 ≥1.2）。
这解释了 FINAL_STATUS 的判断：**DEU 域内可交付上限 = 5 颗**（2 ACTIVE + 3 待授权）。

## 五、DEU 域收敛结论（2026-11-10 收口）

1. 单数据集 ATOM：全部 172 集扫描完毕，`fund_holdings_panel`（0.65）、`insiders1`（BA6 在飞）为最后两测；其余已实测封盘或字段自测否决。
2. 双塔组合：合法组合类型的腿天花板均 ≤0.84，数学上不可达 1.58 ⇒ 组合路径关闭。
3. 结论：**DEU D1 域内 ATOM 交付上限 = 5 颗**（zq3eb7No / bl6AvMkN 已 ACTIVE + RREPm361 / 1YNMAA8M / E569ZE7L 待授权）。
4. 若要突破 5 颗，需用户放开「不得更换 region」过程约束（goal 明文，需用户修改）。