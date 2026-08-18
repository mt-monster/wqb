# Alpha 生成经验归纳总结（基于 WorldQuant BRAIN 中文论坛）

> **来源与方法**：通过 `wq-brain-http` MCP（HTTP 端点 `http://localhost:8876/mcp`，服务 `brain-platform-mcp v1.29.0`）以多关键词搜索到 **175 篇不重复相关帖**，深读其中 **22 篇高相关帖（含评论区）**，按主题归纳。
> **浏览性质**：本次为**只读浏览**——该环境 MCP 未实现发帖/评论/点赞写工具（`forum_functions.py` 仅有 search/read），按 `brain-forum-browse` skill 豁免条款，写贡献义务自动豁免，未向论坛发布任何内容。
> **证据标注**：每条经验后括注来源帖 ID（如 `[28239268385431]`）或评论区实证（Cn）。

---

## 一、Alpha 生成方法论：LLM / 自动化工作流

论坛当前主流方向是"大模型辅助生成 Alpha"——选字段 → 组表达式 →（接 API）自动提交一条龙。核心共识：

1. **分步引导优于从零生成完整表达式**。`[28239268385431]` 及评论 C1：直接让 LLM 生成完整表达式成功率低（模型对 BRAIN 算子语义/约束理解不足、易幻觉）；应分三步——① 模型提经济逻辑与字段组合 → ② 人工/规则翻译成 FastExpr → ③ 模型做语法检查与优化。
2. **算子幻觉治理**。`[35591278645015]` C3：新对话前先让模型"学"全部可用操作符（`data/operators.csv`，约 66 ops），基本消除操作符幻觉；评论 C2 指出幻觉两类——自创字段/算子、参数瞎填。
3. **字段/算合法性预检**。`[41653035827223]` C2（EUR TOP2500 实测）：LLM 输出立刻用本地 `operators.csv`+`fields.csv` 比对，把无意义 422 错误从 ~10% 压到 <1%。
4. **两种工作流模式**（`[41653035827223]` 正文 + C1/C2 量化验证）：
   - **Agent 模式**（探索新数据）：全交给 Agent，产出高但费 token。
   - **工厂模式**（已验证信号模板化）：脚本固定流水线，只把"创意环节"（独特算子设计、空值逻辑）交给 LLM → **省 55–60% token**。
5. **分工边界 + 失败缓存**。`[41653035827223]` C1/C2：给 Agent 固定任务边界，强制只输出通用算子模板，遍历/仿真/解析/结果筛选全交离线脚本；用 `rounds/{alpha_id}/processed_alphas.json` 记录每轮已尝试表达式+失败原因，新轮必读历史避免重复建议已衰减变体。
6. **离线因子预过滤**：LLM 候选先过维度/空值/universe 掩码/浮点四大规范，筛除 ~80% 劣质代码，不占仿真次数。

---

## 二、Python Alpha 的差异化竞争力

`[41653035827223]` 核心论点：**做 Fast Expression Operator 无法实现 / 拥挤度高的信号**。

1. **空值处理差异**：`np.nanmean`/`np.nan_to_num` vs `ts_backfill`/`group_backfill` 行为不同，探索空间大，易在降 turnover 同时提 return。
2. **独特算子**：`squared_tail_rank`、`split_leg_polarization`、FFT/维纳滤波/小波等，提取与 FastExpr 完全不同的特征。
3. **铁律（评论量化验证）**：**信号互补性 > 信号强度**。`[41653035827223]` C3：两子信号 Sharpe 1.2 与 1.0，相关性 0.1→0.9 时融合 Sharpe 1.6→1.25；C4：IND 上两 Sharpe 1.0 但相关性 0.2 的子信号融合 Sharpe 1.4，而两 Sharpe 1.3 但相关性 0.8 的融合仅 1.35。**正交信号源比单信号极致优化更重要。**
4. **NaN 边界**：截面 NaN 比例 >50% 时 `rankdata` 失真，计算前先 universe 过滤。

---

## 三、论文 / 研报驱动

`[30628371704215]` 五步法：理解论文核心见解（市场低效/因子/统计关系）→ 匹配 BRAIN 数据字段 → 选算子（rank/delta/scale/reverse）→ 构建 → 回测优化（看 IC、Rank IC、换手率、行业中性化）。评论建议复现 **Alpha101** 加深量价/因子构建理解。

**八问分析框架**（来自 `[42078917602455]` C2，AI-Alpha 比赛培训）：Q1 不变 / Q2 变化 / Q3 异常 / Q4 组合 / Q5 结构 / Q6 累积 / Q7 相对 / Q8 本质——系统性激发因子思路，按工作流嵌入 prompt。

---

## 四、模板 / 算子工程

1. **设计模式**（`[41379941061143]`）：
   - 鲁棒标准化输入：`zscore(winsorize(pasteurize({field}), std=4.0))`
   - 横截面相对价值：`group_neutralize(winsorize({field}), {group})`
   - 智能加权趋势：`ts_decay_linear({field}, {w}, dense=true) - ts_delay({field}, {w})`
   - 波动率调整均值回归：`ts_zscore({field}, {w})`
2. **算子分类**：差分/变动、归一化/排序、窗口聚合、位置/索引。
3. **多模型指令分发 + 模板整合**（`[36881490529815]`）：跨模型高相似度模板（共识性/普适性强）+ 与自身差异显著模板（打破定式/低相关）。
4. **通用大模型零预算方案原则**：角色去特定化（不绑定 WQ）、仅锚定底层逻辑（数据类型/运算符/窗口/中性化），释放 AI 自主性避免同质化。约束：每因子 ≤1 字段、运算符 ≤4、窗口匹配数据时效（news/sentiment ≤20，fundamental ≥60）、组别匹配逻辑（行业因子→industry/subindustry，全市场量价→market）。
5. **操作符覆盖式生成**（`[35591278645015]`）：给定稀有操作符（如 `ts_covariance`）+ 字段，让 LLM 批量生成，覆盖"每个操作符都提交"。

---

## 五、中性化（Neutralization）

`[41285612019351]` + 评论 C1 实证：

- **类型**：NONE（基本无法通过 check，新手避坑）/ MARKET（去市场贝塔）/ SUBINDUSTRY（去行业+市场）/ INDUSTRY / SECTOR / GROUP。
- **新兴市场**：IND/KOR 的 MARKET 后仍残留行业暴露 → 叠加 `group_neutralize` 手动 double neutralization。
- **小盘 universe**（TOP500/MINVOL1M）：SUBINDUSTRY 分组过细样本不足、信号变弱 → 优先 INDUSTRY。
- **★ 关键杠杆**：中性化选择**直接影响 prod correlation**。同一表达式 MARKET `pc=0.65`（过）换成 SUBINDUSTRY `pc=0.72`（超标）。**提交前须在目标中性化下重查 corr。**
- 用好中性化可大幅降 IND 地区相关性。

> **与本地实战交叉印证**：工作记忆记载"KOR 单 alpha 改 SUBINDUSTRY 后 prod-corr 几乎不变（0.7668→0.7654）"，论坛实证"SUBINDUSTRY 可能反而更高（0.65→0.72）"——两者一致：**中性化切换对单 alpha PC 影响有限且方向不定**，不可当作降 PC 银弹；组合层（SA 10+ 成分）降相关需另论（见 §十）。

---

## 六、Prod Correlation（生产相关性）治理

PC>0.7 被拒，衡量与平台已有生产策略的相似度，过高=缺乏独特性。

1. **四大降 PC 方向**（`[36680834830743]`）：
   - 调时间窗口：`ts_backfill(x,120)→60/90`；`ts_rank(x,66)→50/70`。
   - 放宽 winsorize：`std=4→5`。
   - 非线性变换：`signed_power(scale(x),2)`、`log(x)`。
   - 强化中性化：`group_neutralize(x, densify(industry))` / `market_cap_group`。
   - 组合使用最佳；**迭代逐个调，勿一次改太多参数**。
2. **批量监测**（`[37084044827159]`）：脚本把 PC 写入 alpha 名称+颜色标记（<0.6 蓝 / 0.6–0.7 紫 / >0.7 黄），每 3h 循环筛出可提交；RA 24h 可检 ~600 个 `[36947868698519]`。
3. **嵌套降 PC 的代价**：`[29878528858135]` C1 实证部分 alpha 反复嵌套后 PC 从 0.8+ 降到可提交，但 C2 警告"为交而交"、反复嵌套易过拟合、长期损害 VF（见 §九）。

---

## 七、Turnover / Fitness / Margin

`[19253259366039]` + 评论 C1 与 `[30927669645207]`：

- **公式**：`Fitness = Sharpe * sqrt(|Returns| / max(Turnover, 0.125))`。Turnover 高 → 交易成本高 → Fitness 降。
- **关系**：`return ≈ turnover * margin`；给定收益下 turnover 越高 margin 越低（影响被 PM 采纳的 weight）。
- **降 turnover 三法**：① 增加 decay（提升信号一致性）；② `trade_when`（加开平仓条件）；③ 降 turn 算子 `ts_target_tvr_decay` / `ts_target_tvr_hump`（实测好用）。
  - `ts_target_tvr_decay` 实战坑（`[42078917602455]` C1）：`target_tvr` **必须关键字参数**；甜区窄（~0.65 稳过 returns ratio 0.75，>0.79 反 HIGH_TURNOVER FAIL）。
- **High Turnover PPA**：真正筛子是 `returns ratio > 0.75`（非 Turnover>20%）；订单流数据（`order_flow_imb`/`option18`）天然高换手；**coverage 非 100% 导致被动换仓污染 turnover（占 5–8% noise turnover）**，用短窗 `ts_backfill(3–5)` 或 minimum trade days 门控 `[42078917602455]` C4。

---

## 八、数据集 / 区域（Pyramid）

`[28466349225623]` / `[28790043236887]` + 评论实证：

- **数据集选择**：参考因子区域差异/多因子整合；coverage 一般 >50%；小众/蓝海数据集（value score 高、竞争低）更易出低相关。
- **区域节奏**：ASI/TWN 起步（数据完备、竞争温和）→ GLB/KOR（字段重叠高、需精细稳健化）→ EUR（被低估增长点，EUR TOP2500+STATISTICAL 好，IS Sharpe 3.6–4.5）。
- **模板跨区域复用**：共享字段换 region/universe 快速验证。
- **★ 2026 VF 算法升级"质量优先"**：数量权重贬值，走"10+ ATOM + margin≥30bp + yearly-stats 逐年不下滑"扎实路线 `[28790043236887]` C2。
- **KOR 铁律**：`vector_neut`（风险因子向量中和）；KOR D1 TOP600 SECTOR delay=1 实测 multiplier 1.7–1.8 `[28790043236887]` C1。

---

## 九、过拟合识别与防护（最重要纪律）

`[42018671130391]` + 评论 C2 补第 4 信号：

1. **3 个早期信号**：① Sharpe 随 decay 断崖下跌（decay=5 即 1.8→0.8）；② 年份间 Sharpe 方差 >1.0（正常 0.3–0.5）；③ 去掉 top/bottom 10% 后 Sharpe 腰斩（赌 outlier）。
2. **第 4 信号（逐年 corr 跳变）**：相邻两年信号相关性突然跳变 >0.4 = 训练窗口覆盖独特 regime，根因；只看汇总 Sharpe 看不出。
3. **提交前验证**：换同类型 datafield（崩了=数据特征在赚钱非因子逻辑）；随机打散 stock-level 信号重 rank（不降反升=中性化有问题）。
4. **一阶优先**：`[34417037635863]`（鼠鼠）实证——二阶套二阶致 VF 从 0.9 掉 0.1，改只跑一阶、操作符≤3 后 VF→0.98、combined→3.13。嵌套反复套虽能降 PC，但"为交而交"长期损害 VF。
5. **鲁棒性测试**：可提交后遍历微调参数，若结果变化大=不健壮，不提交 `[29878528858135]` C4。
6. **时间窗警示**：覆盖极端行情（如 VIX 飙升月）需特别谨慎。

---

## 十、提交前 QC 与自相关 / SuperAlpha

`[30523862838167]` + `[42738863064215]`：

- **本地 self-correlation**：累计 PnL **必须先 `diff()` 成每日 PnL 再 `corr()`**，否则得伪相关≈1；阈值 0.7；分批 10–20 个避免超时；`dropna` 清理。
- **self + cross 合并 pipeline**：先筛 self<0.7，再做 pairwise corr 矩阵识别冗余簇，提交前 QC 一步到位。
- **SuperAlpha Combination**：`1 - maxCorr`（自相关减分加权）奖励日收益独立组件，压住 SELF_CORRELATION 检查；变体 `1-maxCorr^2` / `reduce_mean` / 窗口 250–750。实测 MEA 上 IS Sharpe 5.39、Fitness 6.59，investability 下 Sharpe 2.95 且自相关稳住。
- `prod_corr` 直接写进组合公式目前论坛无成熟方案，留作开放问题。

---

## 十一、可直接复用的行动清单

| 环节 | 推荐做法 |
|---|---|
| 生成工作流 | 字段/算合法性预检 + 失败缓存 + 离线预过滤 + 自动回测筛选；LLM 只做创意，机械活全交脚本 |
| 差异化方向 | 优先 Python Alpha 做 FastExpr 不可为的信号（空值处理、独特算子） |
| 提交硬门 | prod_corr<0.7、self_corr<0.7、目标中性化下重查 corr、逐年 stats 不下滑 |
| 过拟合防护 | 一阶、低嵌套、换同类型字段验证、逐年 corr 跳变检查 |
| 多样性 | 跨模型共识模板 + 差异模板并用；类比生物多样性，不交高度相似的 alpha |
| 区域/数据集 | ASI/TWN 打底 → GLB/KOR/EUR 扩张；优先蓝海/小众数据集；质量优先于数量 |

---

## 附：本次抓取支撑数据

- `reports/forum_alpha_research/search_results.json` — 175 篇相关帖（ID+标题+命中关键词）
- `reports/forum_alpha_research/read_posts.json` — 22 篇深读帖（正文+评论）
- `reports/forum_alpha_research/digest.txt` — 可读摘要
- 抓取/解析脚本：`gather_search_v2.py`、`read_posts.py`、`make_digest.py`（可复用）
