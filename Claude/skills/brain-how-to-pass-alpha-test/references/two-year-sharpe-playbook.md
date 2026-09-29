# LOW_2Y_SHARPE / IS_LADDER 破闸手册（2026-09-19，论坛实证 + 公开文献 + KOR 实测）

> 平台口径：`LOW_2Y_SHARPE` = 最近两年（IS 末两年）Sharpe，D1 限 1.58（CHN 2.08）；`IS_LADDER_SHARPE`
> 从最近 2 年起逐年加长，FAIL 线 1.59，PASS 线 2.38（2–5 年）→ 2.22/2.06/1.90/1.74/1.59（6–10 年）；
> turnover<30% 时 PASS 线 ×0.85。两者本质相同：**信号在最近两年还活着吗**。
> **数字来源**：以上阶梯数字来自平台口径 / 论坛实证，**未入 `wqb.config`**；仓库对这两个检查的实测 limit 是 `config.PLATFORM_CHECK_LINES['low_2y_sharpe_min']`（1.58，同时用于 `LOW_2Y_SHARPE` 与 `IS_LADDER_SHARPE`）。两者出入时以 `is.checks` 里的 `limit` 为准。
> **窗口说明**：文中论坛实验窗口 250 / 50 / 500 不在本库标准窗口白名单（`[1, 5, 22, 66, 252, 504, 1008, 1260]`）；复现时取 252 / 66 / 504 并复验（文中括号标了对应值）。
> **`rank_by_side` 等算子**：不在 `known_ops`（平台 `get_operators` 实测清单）——动手前先 `get_operators` 确认账号可用；「未解锁」= 该算子不在 `get_operators` 返回里。

## 0. 先诊断，再修（1 次 API）

`get_alpha_yearly_stats(alpha_id)` 看逐年 Sharpe：

| 逐年形态 | 结论 | 处置 |
|---|---|---|
| 各年都正，只是末两年 1.0–1.5 | 幅度问题 | §1 设置轴 → §2 表达式轴（低成本先试） |
| 末两年某一年被少数股/极端值拖垮（回撤突增） | 集中度问题 | §2 rank_by_side / signed_power / 外层 ts_zscore |
| 末两年**符号反转**（如 KOR 残差反转 2016–20 年 Sharpe 2.8–3.1，2022 年 0.75，2023 年 −1.21） | **机制失效** | §3 机制轴；全部条件化仍反转 → 判死家族，不再调参 |

论坛共识（SZ83096「从潜力 Alpha 到成功 Alpha」、DA98440「时间是最诚实的裁判」）：
**初筛字段先看 2Y 而不是 Sharpe；2Y 差的字段族直接出局**。2Y 是家族属性，不是参数。

## 1. 设置轴（成本 = 1 条模拟，先试）

- **中性化**（ZZ47696 GLB 同内核 7 组对照）：纯风险因子中性化 STATISTICAL/FAST/SLOW/SLOW_AND_FAST 近两年 2Y 全崩
  （1.15/1.30/0.96/0.72），换 **REVERSION_AND_MOMENTUM 2.04 / CROWDING 2.17**，全期 Sharpe 几乎不变——
  风险因子模型近两年与信号重叠，把有效收益一起中性化掉了。全期正常、只 2Y 不过 → 先换 RAM/CROWDING。
  ⚠ 对**反转类**信号无效（KOR risk71 实测：RAM 0.78/2Y −0.40，CROWDING 1.07/2Y −0.02）——RAM 直接吃掉反转暴露。
- **decay 按换手阶梯**（LC69991）：换手低给小 decay、高给大 decay；统一 decay=5 常拉低 2Y。
- **truncation 0.08→0.05**（QQ68782）：2Y 差 0.1–0.2 时配合 signed_power 用。
- **缩短动量/差分窗口**（YZ54944 MEA：ts_delta 500→250〔白名单取 504→252〕，2Y 0.81→1.63），但要**逐年确认都为正**，小池短窗最易"假性通过"。
- margin 几乎只由 setting 决定（换 setting 跨 2.3×，换算子 ±1%）；`Fitness = Sharpe × √(505 × margin)`，
  牺牲 margin 换稳定的净赚条件：Sharpe 保留率 > 1/√(margin 倍数)。

## 2. 表达式轴（不改机制）

- **表达式内 `group_neutralize(x, industry)` + 外层更粗的 setting**（ZZ47696：2Y 1.15→2.04，S +29%）。
  铁律：内层粒度必须**严格细于**外层 setting，否则被外层投影吸收（内 industry + 外 SUBINDUSTRY → SELF_CORR 0.993 ≈ 恒等）。
  KOR risk71 实测：内层 industry + 外 STATISTICAL 是 8 变体里最好的（S 1.54 / sub 1.13 / 2Y 0.16），但救不了符号反转。
- **`rank_by_side(x)`**（XC66172：ladder 0.28→2.44；**不在 `known_ops`，先 `get_operators` 确认**）：正负各侧分别排序，压极端、保方向；副作用 margin −6~15%，
  高换手线慎用；信号多空方向月度不稳（正值占比 12 月滚动 std>0.15）时反而锁错方向。未解锁时替代：
  `if_else(less(x,0), subtract(group_rank(x, sign(x)), 1), group_rank(x, sign(x)))`。
- **`signed_power(x, 0.5)`**（LC69991/QQ68782）：保号开方压长尾；0.5 最稳，0.7 易压过头。
- **`quantile(normalize(x))`** 替代 rank：尾部压缩更均匀，ladder 更稳（XG31364 ASI）。
- **外层 `ts_zscore(x, 250)`**〔白名单取 252〕：时间维归一化，同时修 Weight Concentration（YZ54944）。
- margin 回补：归一化后叠 `ts_av_diff(field, 50)`〔白名单取 66〕注回时序幅度（XG31364：margin 0.0012→0.0016，SC 还降）。

## 3. 机制轴（改信号来源；公开文献）

- **Medhat & Schmeling (2022) Short-term Momentum**：高换手股票的 1 月收益**延续**，低换手股票才反转 →
  `trade_when(低换手, -R, 高换手退出)` 或 `if_else(高换手, +R, -R)`。KOR 2023 散户题材狂潮正是这一机制；
  实测 sign-switch 版把 2023 从 −1.21 修到 −0.53，但 2022 从 0.75 掉到 −1.63 → 末两年整体仍负。
- **Cooper (1999) / Conrad-Hameed-Niden (1994)**：伴随放量的价格变动更可能延续，缩量才反转 → 量能意外 `trade_when(低量, -R, 高量退出)`。
- **Da, Liu & Schaumburg (2014)**：反转只存在于非新闻/残差成分，新闻日后无反转 → 用残差收益 + 排除财报/新闻日（earnings 日历字段作 trade_when 门控）。
- **Hameed & Mian (2015)**：行业内反转更强更稳，行业成分是动量 → 内层 `group_neutralize(x, industry)`（同 §2 第一条）。
- **Nagel (2012) Evaporating Liquidity**：反转收益 = 流动性供给补偿，高波动时期强、平静期弱。⚠ 平台每日按 book 归一化，
  **整体乘以市场波动标量无效**（权重被重新归一），只能做截面条件化（按个股波动/流动性分桶），而这会撞 robust/investability。
- **Avramov-Chordia-Goyal (2006)**：反转集中在非流动股 → 与 IND robust 闸（流动子集 Sharpe ≥1）天然冲突。

## 4. 判死规则（KOR risk71 案例）

8 变体（低换手门控、换手 sign-switch、缩量门控、内层 industry GN、RAM、CROWDING、波动门控、signed_power）
全部 2Y ≤ 0.16，逐年 2022–2023 仍为负 → **残差反转在 KOR 2022–23 结构性反转（题材动量 + 2023-11 卖空禁令），家族判死**。

**规则**：逐年 Sharpe 末两年符号反转，且 §1–§3 三轴各试过 ≥1 个代表变体仍不过 → 该 **(区域, 家族)** 记 dead_end，换机制 / 换集，**不再调参**。
- **范围**：证据全部来自 **KOR 2022–23**（题材动量 + 2023-11 卖空禁令这一区域 / 时段特有的冲击），所以判死对象是 **(region, family)**，**不是**跨区域的「家族判死」；换区域重测前不要把它当成该族的普遍结论。
- **落台账的路径**：先 `python tools/forum_recon.py --question "<数据集/信号族> 有无解法" …`（`found=true` 不得直接判死），再 `mcp__wqb-db__seal_dead_end`——流程与「候选判死 ≠ 家族判死」见 RA [`step9-writeback.md`](../../wq-brain-ra-pipeline/references/step9-writeback.md) §9.5。**本手册与 how-to-pass 只建议，不执行回写。**
