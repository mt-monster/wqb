# S1 模板池 · EUR/D1 news52 (电话会文本结构/规模统计) wave2 备靶 · 2026-11-05

> 硬约束：模板库 ≥10 个**结构互异**模板；差异落在 骨架结构 / 算子几何 / 矩(水平·一阶差分·二阶方差) / 分组轴 / 非线性变换，换窗口不算。来源 [F]平台论坛 [P]论坛帖引用论文 [S]自建。
> 全部为 **单数据集 ATOM**：仅 news52 内部字段 + 平台内置 group 轴(sector/industry)，**不含 returns / price / volume 腿** —— 规避 batch1 §82 发现的「returns 腿被计入 PV 塔」；补 NEWS 塔(当前 1/3)，不占塔组合配额。派发后按 platform pyramid 实测确认塔位，不预判。

## 字段面（MCP get_datafields，EUR/TOP2500/D1，24 字段 100% 拉全 complete=true）
- **认知修正**：news52 不是情绪分数集，是**电话会文本结构/规模统计**。几无拥挤(alphaCount 0–14)。
- MATRIX 18 个，cov 0.4985：`mws52_{chars,paragraphs,sentences,words,talks,questions}_{in_presentation,in_qa}`(pr/qa 成对) / `mws52_conference_call_participants`(非公司方=分析师/第三方) / `mws52_corporate_participants`(公司方) / `mws52_eventtype` / `mws52_{starttime,lastuptime,expirationtime}`(时间戳)。
- VECTOR 6 个，cov 0.38：`mws52_occurence{,_presentation,_qa}`(关键词出现次数) / `mws52_position{,_presentation,_qa}`(关键词绝对位置)。用前必 `vec_avg` 聚合。

## 论坛/论文取证（本轮已读 4 篇正文）
- [F] **41858884736919** Earnings 实战指南：电话会情感是事件驱动、天然低相关；事件后 3–10 天信号最强；decay 5–15 短、trunc 0.01–0.05、Industry 中性；「其他地区覆盖低但竞争更少」。
- [F] **41995684467479** 事件字段别盲用 ts_rank(252)：半衰期决定窗口，长窗跨财报季跳变令 IS Sharpe 虚高(1.3)/实际 0.7；改 `ts_decay_linear(...,d=20)` 短窗或 `ts_backfill` 对齐事件日；`ts_mean(5)+ts_decay_linear(10)` IC 比 252 高约 2 倍；评论给实证 OS Sharpe 0.6→1.0。
- [F] **43691920948759** LM2 vs VADER：**qa 相对 pr 的变化量比绝对值更有信息**（问答即兴、暴露真实态度）；合成总分先用前拆清楚混了什么。
- [F] **43691562191895** 语调札记：pr 排演/qa 即兴、CEO 与其他高管差异有信息；语调变化领先行为；须跨公司可比校准。
- [F] 41995684467479 评论(JR57542)：**连续型计数子字段(词数/问题数)适合当主干、天然低 self-corr**，与稀疏情绪族半衰期不同 ⇒ 按字段族降自相关是免费正交维度。
- 论文线：论坛帖内引用 Earnings Quality on the Street / Earnings Volatility 等(21004691882135 / 24897131810839)；web_search 402 余额耗尽，独立外部论文线仍未通，此处为论坛帖内引用非独立核验。

## 窗口口径（硬约束：日1/周5/月22/季66；其它值须给解释+实证）
- 主体用 **1 / 5 / 10 / 22**：`ts_delta(...,1)` 事件日对齐、`ts_mean(...,5)` 周窗平滑、`ts_decay_linear(...,10)` 与 `d=20` 短半衰期窗（论坛 41995684467479 给 IC×2 / OS 0.6→1.0 实证）、`ts_backfill(...,22)` 月窗对齐事件日。
- **Q14 故意保留 66(季) 长窗作单变量对照**：batch1(§82) news18 用 66 窗 2Y 全 1.0–1.3，论坛归因假设「长窗跨季跳变」；本波主体短窗 + 1 条长窗，用于验证「2Y 衰减是字段问题还是窗口匹配问题」。

## 模板池（14 个，结构互异）
| # | 来源 | 机制 / 结构轴 | 表达式骨架 | 算子数 | 经济含义 |
|---|---|---|---|---|---|
| Q01 | [F][S] | qa−pr 变化量·一阶差分 | `rank(ts_delta(ts_backfill(subtract(mws52_words_in_qa, mws52_words_in_presentation), 22), 5))` | 4 | 问答相对演讲篇幅变化=即兴信息增量，周窗差分 |
| Q02 | [S] | qa/pr 比率·水平 | `rank(ts_backfill(divide(mws52_chars_in_qa, mws52_chars_in_presentation), 22))` | 3 | 问答占比高=管理层被追问多、披露压力 |
| Q03 | [F] | 参与者广度·分组 | `group_rank(ts_mean(ts_backfill(mws52_conference_call_participants, 22), 5), sector)` | 3 | 分析师参会多=关注度高，行业内可比 |
| Q04 | [S] | 二阶矩·篇幅分歧 | `-rank(ts_std_dev(ts_backfill(mws52_words_in_presentation, 22), 22))` | 3 | 演讲稿长度波动=沟通策略不稳(Miller 方向) |
| Q05 | [F] | 短半衰期·decay 窗 | `rank(ts_decay_linear(ts_delta(ts_backfill(mws52_sentences_in_qa, 22), 1), 10))` | 4 | 事件日问答句数冲击按 10 日半衰衰减(论坛推荐) |
| Q06 | [F] | 连续计数主干·一阶差分 | `rank(ts_delta(ts_backfill(mws52_questions_in_qa, 22), 5))` | 3 | 提问者数量变化=质疑强度，计数族天然低 self |
| Q07 | [F] | 双均值差·pr/qa 发言 | `rank(subtract(ts_mean(ts_backfill(mws52_talks_in_qa, 22), 5), ts_mean(ts_backfill(mws52_talks_in_presentation, 22), 5)))` | 6 | 发言轮次 qa−pr = 互动强度 |
| Q08 | [S] | VECTOR 计数·注意力 | `rank(ts_mean(vec_avg(mws52_occurence), 22))` | 3 | 关键词出现次数=主题强度(vec_avg 聚合) |
| Q09 | [S] | VECTOR 位置·结构 | `rank(ts_mean(vec_avg(mws52_position_qa), 22))` | 3 | 关键词落在问答的位置=话题次序信息 |
| Q10 | [S] | 非线性·幅值 | `rank(signed_power(group_zscore(ts_backfill(mws52_paragraphs_in_presentation, 22), sector), 1.5))` | 4 | signed_power 压幅 + 行业内 zscore |
| Q11 | [F] | 回归残差·qa 对 pr | `rank(ts_regression(ts_backfill(mws52_words_in_qa, 22), ts_backfill(mws52_chars_in_presentation, 22), 22, lag=0, rettype=2))` | 4 | 剥离 pr 规模后的 qa 独立增量(两腿均内部字段,不带 PV) |
| Q12 | [S] | 参与者结构比 | `rank(ts_backfill(divide(mws52_conference_call_participants, mws52_corporate_participants), 22))` | 3 | 外部分析师/公司方 = 外部审视强度 |
| Q13 | [F] | 演讲稿收缩·反转 | `-rank(ts_delta(ts_backfill(mws52_sentences_in_presentation, 22), 5))` | 3 | 官方措辞变短=回避/谨慎，方向取反 |
| Q14 | [S] | 长窗对照·分组 | `group_rank(ts_backfill(mws52_words_in_qa, 66), industry)` | 2 | 故意用 66 季窗，验证长窗跨季跳变假设 |

## 全模板字段预检（MCP preflight_expressions，零回测成本）
- 14/14 `valid=true` / `unknown_fields=[]` / `any_changed=false`（VECTOR 字段已手工 vec_avg，preflight 复核无需再修）。
- 算子数逐一 2–6，**全部 ≤12** 合规。
- **软标记**：preflight 对 `mws52_corporate_participants` 的二次分页探查报 `get_datafields(offset=50): failed after 6 attempts`（平台瞬时故障）；该字段在首轮全字段面确证在架(cov0.4985/ac4)且 valid 判定未受影响 ⇒ 不判字段缺失，Q12 派发时以回测结果复核。

## 派发纪律（待 batch2 释放并发槽后执行，本轮未派）
- 每批恰好 2 条 `create_multi_simulation`（并发限 2），一批一套 settings：EUR/TOP2500/D1、FAST(或按论坛 Industry)、decay1、trunc0.04、maxTrade OFF。
- 收批按**模板编号**归因；逐年空窗闸/算子≤12/CW/self/prod 逐件验；按 pyramid 实测塔位(确认是否纯 NEWS ATOM)。
- 首批建议 Q01(qa−pr 一阶差分) + Q02(qa/pr 比率)：论坛最命中的「变化量 vs 绝对值」单变量对照，纯内部字段、短事件窗。
