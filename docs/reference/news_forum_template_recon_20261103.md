# NEWS 情绪类 · 论坛模板侦察（2026-11-03）

> 来源：MCP `search_forum_posts`（3 条查询）+ `read_forum_post`（4 篇全文）。
> 目的：为「GBR NEWS 模板族跨区迁移」补新几何，避免骨架单一（用户硬约束：模板池 ≥10 个结构互异）。

## 1. 已读 4 篇 · 要害

### ① 【Alpha模板】情绪数据中用 ts_covariance 构建 alpha 模板（pid 35294898626711，52 赞 / 28 评）
```
-ts_covariance(<负面情绪>, <正面情绪>, <days>)
```
- 经济含义：负面情绪得分下降、正面情绪得分上升 ⇒ 协方差为负 ⇒ 取负后为正 ⇒ 做多。
- **窗口取长不取短**：作者实缴的 alpha `days` = 63 / 252 / 504；短窗「结果都比较一般」。
- 原帖用 Sentiment21（MATRIX）；本区字段是 VECTOR ⇒ **必须先 `vec_avg`**。
- 文献线索：情绪对收益的影响「4–5 天后以同等幅度反转」（反转效应）。

### ② 【Alpha Idea】给信号标保质期——新闻情绪字段的时效性分级与短窗模板（pid 43175327536279）
- **窗口必须对齐数据源的「保质期」**，不是越短越好：
  | 数据源 | 更新节奏 | 信号有效期 |
  |---|---|---|
  | 实时财经新闻情绪 | 分钟级 | 1–3 天 |
  | 公司公告/行动 | 小时级 | 3–7 天 |
  | 分析师报告/评级 | 日级 | 5–15 天 |
  | 宏观 | 周/月级 | 10–30 天 |
  | 历史财务 | 季度级 | 单独做长窗基本无效 |
- **关键判词**：「如果你的字段扫描出中间峰值（如 66 最强），那是**真周期信号**，不属于保质期问题，别套本帖逻辑。」
  ⇒ **HKG 22/66 峰值、AMR 10/126 与 10/252 峰值都属「真周期信号」**，与既有台账一致。
- **坑**：把「没新闻」当缺失 `ts_backfill` 会污染信号（CHN 已禁 `ts_backfill`；AMR/HKG 慎用）。
- 缺口型 vs 断粮型：停牌/周末空窗可短窗回填；小票「从无覆盖」是真缺，回填=编造中性情绪。

### ③ Alpha idea 推荐 2：估值比率、意外、不确定性与市场情绪（pid 25960462288023）
- 论文：*Valuation ratios, surprises, uncertainty or sentiment*（财报事件前后预测）。
- 结论：**财报公布短期**由盈利/盈利惊喜主导；**公告后中长期**由基本面比率与分析师误差主导。
- 零投资组合年化 11.63% / Sharpe 1.39（扣成本后）。
- 对本区的用法：把「不确定性」当作**独立于情绪水平的第二维度**（AMR `uncertaintypartscr` 已实测为全区最强轴）。

### ④ 【Alpha Idea】财报情绪的「峰值-回差」因子化（pid 43836589723287）★ 本日最高价值
```
-group_normalize(
    ts_target_tvr_hump(ts_max_diff(ts_backfill(SENT, 75), 620),
                       lambda_min=0, lambda_max=1, target_tvr=0.07),
    sector)
```
- **EUR/D1/EARNINGS 实测：Sharpe 1.69 / 2Y 2.24 / Margin 19.95bps / PC 0.6734 / SC 0.2675，0 FAIL，已提交 OS（`O0rM668p`）。**
- **灵魂算子 `ts_max_diff(x, 620)` = today − max(history) ≤ 0**（离 2 年峰值越远越负），取负后 = 「回差」→ 做多。
- **三固定件缺一不可**（作者原话）：`ts_max_diff(PEAK_WIN)` 定回差、`ts_target_tvr_hump` 管换手、`group_normalize` 剥共同成分；去掉任一 Sharpe 掉到 1.4x 以下。
- **可换接口**：`SENT` 可换新闻情绪 / 分析师评级修正 / 目标价变动；**必须是「被推高后回落」的脉冲型情绪**，慢变量（静态评分）会让峰值锚失效。
- **COVER_WIN**：日频情绪数据用 20–30（作者原用 75 是财报季口径）。
- **复用警告**：正确用法是**换字段源**，不是复制字段组合（PC 已 0.6734 逼近 0.7）。

## 2. 移植到本工作区的三条修正

1. **`group_normalize` 在 FASTEXPR 里不存在**（`docs/reference/operators_notes.md` Group 段无此项）。
   最接近的合法替代 = `group_scale(x, group)`（组内缩放）。⇒ 移植时用 `group_scale` 或沿用本区已验证的 `group_neutralize`，**不要照抄 `group_normalize`**。
2. **`ts_max_diff(x, d)` 语义按原帖 = today − ts_max(x, d) ≤ 0**（本地 `operator_semantics.json` 写「w 天内最大波动幅度」与此冲突，以原帖实证为准；波次内含正负两极可自校验符号）。
3. **AMR/HKG 的字段是 VECTOR** ⇒ 所有模板进入前必须 `vec_avg`。

## 3. 由此派生的波次

| 波次 | 区域 | 骨架 | 状态 |
|---|---|---|---|
| AMR wave7 | AMR/news73 | `ts_target_tvr_decay(group_neutralize(-ts_max_diff(vec_avg(F), 620), densify(market)), …)` × 7 字段 + 镜像 + 252/1008 + hump + group_scale | 已派发 |
| HKG wave10 | HKG/news36 | 同上，字段换 `mws36_*` | 已派发 |
| 待设计 | AMR/HKG | `-ts_covariance(vec_avg(负向), vec_avg(正向), 63/252/504)` | 待波次空档 |

## 4. 未读但值得后续读的帖子（search 命中）

- `43620895448343` EUR 财报电话会「情绪概率差」（正/负概率分布层面的净情绪）
- `43614940683799` 从「变化的稳定性」而不是「变化的大小」入手（符号持续性 / 连续同号长度）
- `25066287753367` Machine Alpha 基础知识 3：情绪类数据时序模板（基础几何）
- `34435098185751` 【Alpha灵感】情绪类因子
- `34154000968087` 【Alpha灵感启示录】新闻、情绪和量化因子（悲观情绪对次日道指 8.1bp）
# 第二批读帖（5 篇，2026-11-03 15:50 补）

## 5. 五篇全文结论

### 5.1 帖 43620895448343 EUR 财报电话会「情绪概率差」★最高价值

- 数据给的是 [正/中/负] 三类概率分布，不是单一 tone 分数。核心假设 = 「正面概率 − 负面概率」的分布层净情绪比 tone 分数信息量更高，尤其不确定性（中性概率）。
- 表达式（EUR/TOP2500/D1/COUNTRY）：signed_power(subtract(ts_zscore(ts_backfill(positive_sentiment_probability_3, 60), 250), ts_zscore(ts_backfill(negative_sentiment_probability_3, 60), 250)), 3)
- 三个算子：ts_backfill(60)=事件稀疏的有界填充（情绪有效期）；ts_zscore(250)=自身历史标准化（把水平翻译成「相对自身一年的意外」，与本区惯用 ts_rank 横截面几何完全不同）；signed_power(3)=保号立方，只给极端偏离下重注，实测显著降低与 production 的持仓重合度。
- 数据探索：同集 overall_sentiment_score（argmax 标签）单独用 Sharpe 仅 ~1.2–1.5；保留概率差明显更高 ⇒ 数据给出分布时用分布，不要塌缩成标签。
- 可移植：HKG news36 有 mws36_sentiment_positive_confidence / mws36_sentiment_negative_confidence（置信度即概率）；AMR news73 有实体级 ..._positivepartscr / ..._negativepartscr 与全局 globalsent_positivescore / globalsent_negativescore。⇒ 已派生 HKG wave12 / AMR wave9。

### 5.2 帖 43614940683799 从「变化的稳定性」而非「变化的大小」入手

- 同样大小的变化，一周内反复反转 vs 连续几周方向一致，经济含义完全不同。
- 路径：先造字段变化 → 观察符号持续性 / 连续同号长度 / 滚动一致性 → 比较「幅度信号」与「稳定性信号」。
- 踩坑：窗口重叠、缺失、换手；稳定性指标可能退化成低频风格暴露，需配合规模/行业/市场暴露检查。
- 可移植几何：ts_mean(sign(ts_delta(x, 5)), 22)（正变化占比）/ ts_std_dev(ts_delta(x,5), 22)——本区尚未用过 sign + ts_delta 组合。

### 5.3 帖 25066287753367 Machine Alpha 基础知识 3：情绪类时序模板

- 官方模板：time_series_operator(positive_sentiment - negative_sentiment, days)，天数 5/20/60/250。
- 扩展：先 rank(backfill_op(positive_sentiment, days)) 与 rank(backfill_op(negative_sentiment, days))，再用 compare_op 组合，最后过 time_series_operator(…, days)。
- backfill_op 用 ts_backfill 或 to_nan；rank 用于去噪 + 控制分布范围。
- ⇒ 与本区 GBR 五轴骨架（ts_rank(ts_mean(SIG, W1), W2)）同源，属已覆盖几何，仅作确认。

### 5.4 帖 34435098185751 【Alpha灵感】情绪类因子

- 论文《Dynamic Asset Pricing: Integrating FinBERT-Based Sentiment Quantification with the Fama–French Five-Factor Model》。
- 结论：正常时期情绪对收益有持续积极影响；极端市场条件下被放大甚至逆转。
- 实操：decay=0（新闻实时性）；数据稀疏 ⇒ 只能作事件 alpha 触发。
- 时变性：用过去 N 天（如 30 天）新闻计算情绪因子以保证时效性。⇒ 支持本区「窗口阶梯优先于换轴」结论。

### 5.5 帖 34154000968087 【Alpha灵感启示录】新闻、情绪和量化因子

- 源头：WSJ 专栏「悲观度」预测短期市场反转与成交量——悲观情绪每 1σ 变化 → 次日道指 −8.1bp（大于无条件均值 5.4bp）。
- 构造：情绪差 × 收盘逆向；实证 10 情绪差 × 5 日收益逆向 在 20/21 疫情极端行情效果好。
- 方法论：「强弱比」无量纲 ⇒ 用「净水平差 → 相对占比」保持横截面对比；「负面在分母」的比值非线性放大负面，贴合「负面 → 次日下跌 → 周内反转」。
- ⇒ 两条可移植点：① 相对占比归一（本区词数归一已用，同族）；② 情绪 × 价格逆向的跨源乘子——价格与情绪不同源，合规（对照 AMR 乘子全灭于同族字段）。

## 6. 由此派生的新波次（已生成 + 预检通过）

| 波次 | 区域 | 新几何 | 状态 |
|---|---|---|---|
| HKG wave12 | HKG/news36 | 分布概率差（confidence 对）+ ts_zscore + signed_power(3)；12 个结构互异变体 | 预检 valid，待槽 |
| AMR wave9 | AMR/news73 | 同上，字段换实体级/全局 pos-neg、certainty−uncertainty、finup−findown；含 uncertainty 轴的 zscore 版 | 预检 valid，待槽 |

注意：group_normalize 在 FASTEXPR 不存在（§2）；ts_max_diff 语义以原帖为准（§2）；AMR/HKG 字段为 VECTOR ⇒ 全部已 vec_avg。
