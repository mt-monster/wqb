# USA Turnover 15–30% Theme 破闸方法 —— 论坛取证与对照

**取证日期**：2026-11-20 ｜ **通道**：`wq-brain-http` 的 `search_forum_posts_local`（Zendesk 列表端点 + 本地词命中率过滤，唯一允许通道）
**检索词矩阵**：① `theme`+`turnover` ② `production`+`correlation`（另跑 `investability`/`fitness` 两组）
**scanned**：100–200 篇/组；命中 47 / 59

## 一、四篇核心帖（全文已读，非摘要）

### ① [BRAIN TIPS] How to Deal with High Production Correlation（官方 JO19326, 2026-10-31, 12赞）
`id=44678103399575` — **本主题最权威的一篇**。10 条 tip 全文见下：

| # | 官方 tip | 本仓今日实测对照 |
|---|---|---|
| 1 | **Change the data source or the economic logic**（最可靠）；调窗口/权重/中性化几乎不产生真低相关 | ✅ **完全印证**：8 颗跨 4 类算子 × 5 字段 × 3 TVR 家族 × 2 中性化，prod 全在 0.71–0.76（浮动 ±0.005） |
| 2 | **Use less crowded datasets**（新/小众/少人用的字段） | ✅ 印证：`snt26_relpopularity1` ac=83 ⇒ prod 0.71；`news_sentiment_transfer` 字段 ac=1–27（最冷）却 S≤0.49 无信号 |
| 3 | **Combine two different ideas**（跨类别混合，如 fundamental+sentiment / analyst+price-volume）⇒ PnL 形态不同 | ⚠ **本仓今日完全没试**（全程单集 ATOM）⇒ **下一步主攻** |
| 4 | Trade a different horizon（`ts_*` 不同窗 / `trade_when` 只在特定事件交易） | ⚠ `trade_when` 今日实测 5 臂全劣化（S≤1.32 vs 基线 2.06）—— 但**只在单集内**试过 |
| 5 | `trade_when` 做事件驱动版（只在有事件的日活跃）⇒ 与 always-on alpha 低相关 | ⚠ 同上 |
| 6 | **罕见分组字段 / 双重中性化 `group_cartesian_product`** ⇒ 改横截面结构 | ⚠ **未试**：`group_cartesian_product` 今日零次 |
| 7 | **换 region / universe / delay** ⇒ 同想法在冷门宇宙面对更少相似 alpha | ⚠ 只换过 universe（TOP2000/TOP3000）未换 delay（0/1）；**换 universe 确实改变 S**（TOP2000 时 S 崩到 0.85） |
| 8 | **Change the target, not just the parameters**（对字段做变换：时序变化 / 偏离组均值 / 两字段之比 / surprise 度量） | ✅ 部分印证：字段组合（relpop1−relpop08 等 4 臂）全劣化（S≤1.93）—— **但只在同族字段间做** |
| 9 | **避免"表面"改动**（加 decay、rank↔zscore、改几天窗）通常相关性不变，别烧模拟 | ✅ **强烈印证**：今日 240+ 臂替换扫描中 `ts_decay_linear`/`rank`↔`zscore`/`group_neutralize`↔`group_rank` 类替换对 prod 几乎零影响（0.71→0.76 是唯一例外） |
| 10 | **Sharpe vs 相关性权衡**：若明显优于相关件，有时仍可被接受 ⇒ 查 Submission Checks 确切规则 | ⇒ **可操作**：prod 0.7135 的 `0mPr7AzK`（S2.14/F1.10/2Y1.62）比池内件 S 高得多 |

官方还给出**诊断顺序**（值得固化为本仓读数流程）：
「① 跑相关性检查并读数（不要猜）② 看你的想法用的是哪个 dataset category（热门类更挤）③ 问这是不是经典想法（动量/反转/价值往往已在池里）」

### ② One new structure per family: notes on correlation saturation（XH32267, 2026-11-01, 6赞）
`id=44689167962903` —— **机制解释，最有价值**：
> 「一个 expression 家族往往只落地一次，之后同族变体都会被拒，哪怕 IS 看起来一样干净。
> 机制是：两个相关性闸都对着**你自己近期已被接受的作品**在演进的池子评估。
> 族里第一个成员有时在 0.5–0.6，而后续变体爬到 0.75–0.9，**即使经济逻辑与信号周期都没变**。」

⇒ **★ 这解释了本仓今日 prod 墙的一半**：我 240+ 臂全部落在同一个「DNS 流行度」家族 ⇒ 池里已有同族件 ⇒ 变体 prod 天然抬到 0.71+。
⇒ **实操含义**：**每族只值得押 1 个新结构**；变体预算要留给**新核心（new core）**，不是新皮（new skin）。
⇒ 与本仓记忆 [[corr-gate-duplicate-traps]]（同表达式母件上线后 IS 件 prod/self 爆 ~1）同源，**但这篇补充了「同族不同表达式也会互相抬 prod」**。

### ③ Three things I learned this week about Fitness, hidden reversal and prod correlation（JV71453, 2026-10-27, 1赞）
`id=44557078934039` —— **F 闸闭式 + 慢腿拥挤的实证**：
> 「**Fitness = Sharpe × sqrt(Returns / max(Turnover, 12.5%))**。重排后，Fitness 到 1.0 的条件是 turnover ≤ Returns × Sharpe²。
> 削换手前先算这个数；若缺口大，decay 和 trade_when 通常补不上 —— 它们**砍 Sharpe 比砍 turnover 更快**，Fitness 反而降。」
> 「**慢基本面腿能修 Fitness 但把 prod 推到 0.9 以上**。给快反转信号加慢价值腿，Fitness 从 0.88 到 1.2；坑是 `operating_income/cap` 用得太广 ⇒ prod 0.925。
> 现在改试更冷门的慢腿（**asset growth、net share issuance**）来拿 Fitness 收益而不拥挤。」

⇒ **★ 与本仓 F 闭式完全一致**（记忆 `metric-optimization-playbook`：`F = S·√(ret/max(TO,.125))`）。本仓今日实测：`2r5mKxY8` F=1.06 时 ret×S² = 0.0401×2.04² = **0.167** > TO 0.1486 ⇒ F≥1 可达 ⇒ 与该帖判据吻合。
⇒ **★ 慢腿策略**：用**冷门慢腿**（asset growth / net share issuance 之类）替代拥挤慢腿（operating_income/cap）来提 F 不抬 prod。

### ④ Alpha Diversity: Why Different Expressions Can Represent the Same Idea（SN11340, 2026-10-29, 8赞）
`id=44636553257495` —— 「**句法多样性 ≠ 信息多样性**」：反复对同一数据集做 ranking/scaling/neutralization/时序变换，
表达式看起来不同但捕获同一信息 ⇒ 换算子不自动产生新信息源。
⇒ 与 ① 的 tip 9 同源，但给了**可操作的分类法**（Value / Momentum / Analyst revisions / Trading activity / Risk 五类假设），
可用于**按假设而非按数据集组织研究** ⇒ 直接对上「一个家族只押一个新结构」。

## 二、★ 官方 tip 与本仓今日实测的交叉结论（本轮新增可复用）

| 官方 tip | 本仓验证 | 结论 |
|---|---|---|
| #1 换数据源/经济逻辑 | ✅ 8 颗 prod 恒定 0.71–0.76 | **prod 墙是信息源级**（本仓今日核心发现，官方 tip #1 的定量版） |
| #3 混合两个想法 | ⚠ 未试 | **下一步主攻方向**（唯一未系统试过的 prod 破法） |
| #4/#5 `trade_when` 事件版 | ⚠ 单集内实测全劣化（S≤1.32） | **跨类别混合后再试**才公平；单集内已证死 |
| #6 罕见分组/双重中性化 | ⚠ 未试 `group_cartesian_product` | 下一步次攻（零成本试法） |
| #7 换 universe/delay | ⚠ 只换过 universe | **delay 0 未试**（美国 delay-0 是独立池） |
| #8 变换目标而非参数 | ⚠ 只在同族字段间组合（全劣化） | 跨类别字段间组合未试 |
| #9 避免表面改动 | ✅ 240+ 臂印证 | 「换算子刷 prod」这条路本仓今日已彻底证死 |
| #10 Sharpe 权衡 | 可操作 | prod 0.7135 的 `0mPr7AzK` S2.14 显著优于池内件 ⇒ 值得查 Submission Checks 确切规则 |

## 三、本仓今日 240+ 臂与官方 tip 的**分歧点**（必须诚实记）

官方 tip #3/#5/#6/#7/#8 都说「可以破 prod」，但**本仓今日的实测是：在单一信息源内，这些手段全部无效**。
⇒ 本仓今日的结论**不是与官方矛盾，而是补了官方没说的前提**：
> **官方 tip 默认你还有「另一个数据源/想法」可换。本仓今日的处境是：在 USA 未亮塔的多个候选集里，
> 唯一有信号的（DNS 流行度）已被同族件挤满 ⇒ 官方所有 tip 里的「换」都指向未测的新集。**
⇒ **⇒ 决策含义：prod 破闸的下一步不是在本族内试 tip #3–#8，而是去测「另一个假设族」**
（官方五分类里的 Value / Trading activity / Risk —— 对应本仓未测的 fundamental 塔 / institutions20 短卖量 / pv47 specific returns）。

## 四、官方 tip #3–#7 在本仓 USA 的实测判决（全部无效，但各自原因不同）

| 官方 tip | 本仓实测 | 判决 |
|---|---|---|
| #3 混合两个想法（跨类别） | ⚠ **未系统试**（红线：PV/MODEL/OTHER 内部禁组腿；总腿数 ≤5；优先 ATOM） | 唯一未试的主攻方向 |
| #4/#5 `trade_when` 事件版 | ✅ 单集内 5 臂全劣化（S 1.24–1.32 vs 基线 2.06） | ❌ 单集内无效 |
| #6 罕见分组 / 双重中性化 `group_cartesian_product` | ✅ 实测 5 臂：`LLK5nWOe` prod **0.7281**（基线 0.7143）⇒ **反而更高** | ❌ 无效 |
| #7 换 region / universe / delay | ✅ TOPSP500 宇宙 5 臂全 REJECT（S ≤0.87，TO 升但 S 崩）；USA 无 TOP5000（最大 TOP3000）；delay-0 未试 | ❌ 宇宙无效 / delay 未试 |
| #8 变换目标而非参数 | ✅ 同族字段组合 4 臂全劣化（S ≤1.93）；跨类别字段组合未试 | ⚠ 同族无效 |
| #9 避免表面改动 | ✅ 240+ 臂印证（唯一例外：外层 group_neutralize→group_rank 让 prod 0.83→0.76） | ✅ 印证 |
| #10 Sharpe vs 相关性权衡 | ✅ `0mPr7AzK`（prod 0.7135 / S2.14 / F1.10 / 2Y1.62）显著优于池内件 | ⏳ 待查 Submission Checks 确切规则 |

## 五、★ 取证的核心结论（比任何单条 tip 更重要）

**官方 tip 全部隐含一个前提：「你还有别的数据源/想法可换」。**
本仓 USA 的处境是：**唯一有信号的未亮塔数据集（DNS 流行度 = `sentiment26`）已被同族件挤满**
⇒ 官方所有 tip 里的「换」都指向**未测的新族**，不是本族内的形态变化。

⇒ **决策含义（比继续扫算子重要）**：
1. **本族内（`sentiment26`）prod 墙已闭合**：8 颗形态/字段/算子/TVR 家族/中性化/双重中性化/宇宙
   实测 prod 0.71–0.73，无一 <0.70。
2. **要破 prod，必须去测「另一个假设族」**（官方 ④ 的五分类：Value / Momentum / Analyst revisions /
   Trading activity / Risk）⇒ 对应本仓 USA 未测的：
   - **Value → fundamental 塔**（fundamental13/25/35/69/110/452，fundamental22 已否证）
   - **Trading activity → institutions20 短卖量 / pv47 specific returns**
   - **Risk → pv47 / macro4**
3. **「一族一结构」预算要立刻用上**（帖 ②）：本族（DNS 流行度）**不要再投入第二个结构** ——
   池里已有同族件，变体 prod 只会更高（帖 ② 实测：族内第一个 0.5–0.6，后续变体 0.75–0.9）。
   ⇒ **本族的下一个动作不是"再试一个变体"，而是"整族封存、换族"。**
