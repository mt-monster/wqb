# IND delay1 analyst45（Analyst Trade Ideas）特征工程文档

**Dataset**: analyst45
**Region**: IND
**Delay**: 1


- **数据集**: analyst45 Analyst Trade Ideas（分析师公开投资想法台账：入场/持有/平仓全生命周期指标）
- **区域/延迟/域**: IND / delay1 / TOP500
- **类目**: Analyst（IND 唯一验证有效信号族；alphaCount=1063，userCount=422，valueScore=2.0，pm=1.4）
- **生成方式**: brain-data-feature-engineering skill（standalone），字段清单源 `db fields/IND/analyst45`（241 字段，全 VECTOR）
- **日期**: 2026-08-31

---

## 1. 数据集理解（字段）

### 1.1 数据结构要点

- **241 字段全为 VECTOR 事件型**（每只股票同一时点可能有多个 idea 记录）→ 必须 `vec_*` 聚合（vec_avg/vec_sum/vec_count/vec_max）+ `ts_backfill(66)` 后进常规算子。
- **coverage 平台报 1.0**，但约半数同义字段实际覆盖 0.4329（`*_limited` 与全量双套字段）→ 优先用全量套（coverage=1.0 的 anl45_* 前缀字段），慎用 0.4329 套。
- **三类字段三套命名**（anl45_* / 语义化长名 / *_2/*_3 后缀）大量同义冗余 → 白名单只收代表字段，防候选池冗余。
- **枚举/货币/汇率类字段无信号**（*_currency_*、*_fx_rate、Non-Functional 占位）→ 排除。

### 1.2 字段分类（字段画像）

| 类别 | 代表字段 | 含义 | 预处理决策 |
|---|---|---|---|
| 净敞口（方向性共识） | anl45_net_market_exposure, net_exposure_value | 分析师想法组合的多空净敞口差 | vec_avg；截面 quantile+行业中性 |
| 想法绩效（能力追踪） | anl45_tot_ret_per, anl45_ad_ret_per, anl45_jensensalpha, anl45_treynor_ratio | idea 生命周期回报/日均回报/风险调整 alpha | vec_avg（能力均值）；长窗 ts_mean(126-252) |
| 信心/概率 | anl45_probability, success_likelihood_score_* | 作者对 idea 的量化信心 | vec_avg；整数/档位类用 rank |
| 目标价空间 | anl45_target_prc, anl45_latest_prc, anl45_avg_initial_prc | 目标价 vs 现价 vs 入场价 → 上行空间/已实现幅度 | 比率化 (target/latest, latest/entry) 后 rank |
| 一致性/拥挤度 | anl45_idea_count, grouped_idea_quantity | 同股 idea 数量 = 分析师共识度 | vec_count 或 vec_sum；计数类用 rank 不平滑 |
| 止损/目标调整行为 | anl45_new_value, anl45_old_value, updated_field_value_3 | 止损/目标价/仓位调整幅度（信心变化） | (new-old)/old 变化率；事件门控 |
| 持仓结构 | anl45_current_inv, anl45_real_value, anl45_unreal_value | 当前投入/已实现/未实现结构 | 比率（已实现占比）|
| 久期 | anl45_days_since_inception, anl45_avg_dur, anl45_time | idea 年龄/预期期限 | vec_avg；年龄类取新鲜度差分 |
| 当日动态 | anl45_ret_per_today, anl45_unreal_ret_today | idea 当日回报增量 | 短窗事件信号，慎用（换手高）|

### 1.3 数据讲述的故事

analyst45 = **分析师以真金白银式想法台账表达的持续观点流**：净敞口=方向共识、jensensalpha=历史选股能力、target/latest=上行空间、idea_count=共识拥挤度、调整行为=信心边际变化。与 anl9（升降级广度，已产出 4 颗 ACTIVE）同族但**信息载体不同**（idea 台账 vs 评级流），是 IND 唯一验证有效信号源的延伸面。

---

## 2. 特征工程建议（按问题驱动分类）

### 2.1 稳定性特征
- **选股能力均值**：`ts_mean(backfill(vec_avg(anl45_jensensalpha)),252)`。长期风险调整能力稳定的分析师观点更可信。方向：long 高能力。

### 2.2 变化特征
- **信心边际变化**：`vec_avg(new_value)/vec_avg(old_value)-1`（止损/目标价调整）。上调=信心增强。
- **当日未实现回报增量**：`vec_avg(anl45_unreal_ret_today)` 短窗（高换手，仅作辅腿）。

### 2.3 异常特征
- **能力-敞口背离**：高能力分析师净敞口骤变 = 强信号事件。`ts_delta(vec_avg(net_market_exposure),21)` × 能力分。

### 2.4 交互特征
- **上行空间×共识度**：`(target_prc/latest_prc - 1) × idea_count`。空间大且多人共识 = 强方向信号。
- **能力加权敞口**：`net_market_exposure × jensensalpha`。能力加权的净方向暴露。

### 2.5 结构特征
- **已实现占比**：`real_value/(real_value+unreal_value+0.0001)`。落袋比例高 = 观点已兑现（反向：剩余空间）。
- **多空净敞口**：`net_market_exposure` 截面分位（主信号候选）。

### 2.6 累积特征
- **想法流强度**：`ts_mean(backfill(vec_count(*)),66)` 想法产生频率的长窗累积 = 关注度趋势。

### 2.7 相对特征
- **行业内相对能力**：`group_rank(ts_mean(vec_avg(jensensalpha),252),industry)`。
- 主骨架统一：`quantile(...)` + `group_rank(...,industry)`，与 IND win 配方（anl9/pv106）对齐。

### 2.8 本质特征
- **观点的一阶矩**：分析师想法台账的本质是"带仓位的观点"。方向（净敞口）、质量（风险调整回报）、空间（目标价）、共识（idea 数）四轴构成信号骨架——这是与评级流（anl9）正交的第二信息面。

---

## 3. 实现约束与主辅信号分配建议

1. **每条表达式只用 1-2 个字段**（用户约束）；同数据集字段组合允许。
2. **VECTOR 必包**：`vec_*` → `ts_backfill(x,66)` → 常规算子。
3. **主辅分配**：主信号（净敞口/能力分/上行空间）权重 ≥0.7；辅腿（共识度/当日增量）只做降相关与抬 robust；禁止同信号调权重。
4. **中性化**：首轨 SUBINDUSTRY（IND analyst 族实证最优：e7z1vG06 SUBINDUSTRY robust=1.02 > SECTOR 0.95 > STATISTICAL）；REVERSION_AND_MOMENTUM 禁用（与动量型信号冲突实证）。
5. **SELF-CORR 红线**：analyst 族已有 4 颗 ACTIVE（LL7mzYQv/e7z1vG06/Wj7YP5JN/58l2or1N），同骨架变体 self 易撞 0.7 → 本集骨架必须换 wrapper/分组变量，禁克隆 anl9 修正广度结构。
6. **判死止损线**：批 1 若全 |S|<0.7 且无窗口梯度，直接判死。

## 4. 风险与局限

- 与 anl9 同源风险：平台 self/prod 相关可能偏高，回测后必须查 self_corr（对 4 颗 ACTIVE）与 prod_corr。
- 三套同义字段若同时入池会制造伪多样性 → 白名单收敛到代表字段。
- alphaCount=1063 非零竞争 → prod_corr≥0.7 一律回 Mode B 换字段组合。

---

## 5. 概念块（GEM 实现模板）

**Concept**: Net Exposure Directional Consensus
- **Mechanism**: Analysts' idea books carry explicit long/short net exposure; a high positive net exposure across a stock's ideas is a directional consensus from informed intermediaries, which tends to drift.
- **Fields**: `anl45_net_market_exposure`
- **Implementation Example**: `group_rank(ts_mean(ts_backfill(vec_avg({anl45_net_market_exposure}), 66), 126), subindustry)`
- **Direction**: Long high net exposure
- **Expected Exposure**: momentum
- **Expected Turnover Band**: low
- **Expected Coverage Band**: high
- **Why not crowded**: Uses idea-book positioning rather than rating flows (anl9), a different information carrier in the analyst family.

**Concept**: Skill-Weighted Conviction
- **Mechanism**: Ideas from historically skilled authors (high Jensen's alpha) deserve more weight; the skill level of idea authors on a stock proxies informed conviction quality.
- **Fields**: `anl45_jensensalpha`
- **Implementation Example**: `quantile(ts_mean(ts_backfill(vec_avg({anl45_jensensalpha}), 66), 252))`
- **Direction**: Long high skill
- **Expected Exposure**: quality
- **Expected Turnover Band**: low
- **Expected Coverage Band**: high
- **Why not crowded**: Author-skill weighting is unused in IND analyst alphas which focus on revision breadth.

**Concept**: Target Price Upside Times Consensus
- **Mechanism**: The gap between author target price and latest price measures remaining upside; multiplying by idea count scales it by consensus breadth.
- **Fields**: `anl45_target_prc`, `anl45_latest_prc`, `anl45_idea_count`
- **Implementation Example**: `quantile(ts_mean(multiply(subtract(divide(ts_backfill(vec_avg({anl45_target_prc}), 66), add(ts_backfill(vec_avg({anl45_latest_prc}), 66), 0.0001)), 1), ts_backfill(vec_sum({anl45_idea_count}), 66)), 42))`
- **Direction**: Long high upside-times-consensus
- **Expected Exposure**: growth
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: medium
- **Why not crowded**: Target-price gap is idea-book specific and absent from rating datasets.

**Concept**: Realized Ratio Residual Room
- **Mechanism**: A low realized-to-total value ratio means ideas are still open and unmonetized: remaining room for the thesis to play out; high realized ratio means the thesis already paid out.
- **Fields**: `anl45_real_value`, `anl45_unreal_value`
- **Implementation Example**: `-rank(ts_mean(ts_backfill(divide(vec_avg({anl45_real_value}), add(add(vec_avg({anl45_real_value}), vec_avg({anl45_unreal_value})), 0.0001)), 66), 126))`
- **Direction**: Long low realized ratio (short notation via -rank)
- **Expected Exposure**: quality
- **Expected Turnover Band**: low
- **Expected Coverage Band**: medium
- **Why not crowded**: Position lifecycle structure is unique to the idea ledger.

**Concept**: Confidence Revision Shock
- **Mechanism**: When authors revise stop-loss/target/allocation upward (new vs old value), it is a marginal confidence upgrade; normalized change captures conviction shocks.
- **Fields**: `anl45_new_value`, `anl45_old_value`
- **Implementation Example**: `quantile(ts_mean(ts_backfill(divide(subtract(vec_avg({anl45_new_value}), vec_avg({anl45_old_value})), add(abs(vec_avg({anl45_old_value})), 0.0001)), 66), 21))`
- **Direction**: Long positive revision
- **Expected Exposure**: momentum
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: medium
- **Why not crowded**: Revision events inside idea books are orthogonal to estimate revisions (anl39 family is dead in IND).

**Concept**: Idea Flow Intensity
- **Mechanism**: Rising idea creation frequency marks growing analyst attention; attention trend precedes re-rating.
- **Fields**: `anl45_idea_count`
- **Implementation Example**: `group_rank(ts_delta(ts_mean(ts_backfill(vec_sum({anl45_idea_count}), 66), 42), 21), industry)`
- **Direction**: Long rising flow
- **Expected Exposure**: momentum
- **Expected Turnover Band**: medium
- **Expected Coverage Band**: high
- **Why not crowded**: Attention-flow is an event-count dimension absent from score-based analyst datasets.

**Concept**: Skill-Weighted Net Exposure
- **Mechanism**: Net exposure signed by author skill separates informed positioning from noise positioning; cross-field interaction amplifies the informed component.
- **Fields**: `anl45_net_market_exposure`, `anl45_jensensalpha`
- **Implementation Example**: `quantile(ts_mean(multiply(ts_backfill(vec_avg({anl45_net_market_exposure}), 66), ts_backfill(vec_avg({anl45_jensensalpha}), 66)), 66))`
- **Direction**: Long high skill-weighted exposure
- **Expected Exposure**: momentum
- **Expected Turnover Band**: low
- **Expected Coverage Band**: high
- **Why not crowded**: Interaction of positioning and skill is a new axis in the analyst family.

**Concept**: Daily Idea Return Drift
- **Mechanism**: Aggregate same-day unrealized return increments across a stock's open ideas is a high-frequency informed-flow print; smoothed, it becomes a drift signal.
- **Fields**: `anl45_unreal_ret_today`
- **Implementation Example**: `quantile(ts_mean(ts_backfill(vec_avg({anl45_unreal_ret_today}), 66), 21))`
- **Direction**: Long positive drift
- **Expected Exposure**: momentum
- **Expected Turnover Band**: high
- **Expected Coverage Band**: high
- **Why not crowded**: Daily idea P&L increments are ledger-native and untouched by existing IND analyst alphas.
