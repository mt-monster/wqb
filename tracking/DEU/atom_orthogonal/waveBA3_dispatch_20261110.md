# Wave BA3 dispatch — news18 / news50 / news38 首探（2026-11-10）

> 触发：审计撤回「news 塔事件情绪通道终判死」——news18(70f cov0.979/0.70 双层)/news50(37f cov0.764)/news38(3f cov0.599) 从未探针。
> MI 教训落地：全部 ts_backfill(vec_avg()) 事件转面板；分轴 subindustry/industry；矩覆盖 level/delta/vol。

| # | 数据集 | 字段 | 模板 |
|---|---|---|---|
| N1 | news18 | nws18_ssc（复合情绪） | level sub |
| N2 | news18 | nws18_nip（冲击预测） | level 66 sub |
| N3 | news18 | nws18_multiple_comp_ssc（多实体复合 0.98 覆盖层） | level industry |
| N4 | news18 | nws18_sse（事件情绪连续值） | -vol 252 sub |
| N5 | news18 | nws18_ghc_lna（分析师推荐变动） | delta66 industry |
| N6 | news50 | mws50_ssc（0-100 复合） | level sub |
| N7 | news50 | mws50_ens（事件新颖度） | -level 66 industry（新颖度低=旧闻=反应不足假设） |
| N8 | news50 | mws50_nip（冲击预测） | delta66 sub |
| N9 | news38 | story_analytics_relevance_score | level sub |
| N10 | news38 | story_analytics_metric_value | -vol 252 industry |

设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON/maxTradeOFF。
出口：max|S|≥0.6 ⇒ 升级对应数据集十模板池；全灭（<0.35 且 2Y 负）⇒ news18/50/38 探针级 PROVISIONAL（不终判，按新闸留 D1-D6 空档），news 塔降级为「事件情绪族证据极弱」而不是终判死。

---

## BA3 收割（sim 4ed4ij1vL5eXaYyI4rYL5UP，10/10 COMPLETE，0 error）

| # | 数据集 | 模板 | alpha | S | 2Y | lc |
|---|---|---|---|---:|---:|---:|
| N1 | news18 | ssc level | 78YkbZ11 | 0.10 | -0.88 | 112 |
| N2 | news18 | nip level | 3q0Mr9RO | -0.18 | -2.34 | 112 |
| N3 | news18 | 多实体 ssc level | MP6jR1Lo | 0.23 | 0.02 | 148 |
| **N4** | news18 | **-sse vol 252** | **qM7KrW6A** | **0.57** | **1.44** | **170** |
| N5 | news18 | ghc_lna delta66 | RReJQV1e | -0.22 | -1.40 | 126 |
| N6 | news50 | ssc level | QP01k3GM | 0.12 | -0.36 | 121 |
| N7 | news50 | -ens 新颖度 | e7alw93d | 0.21 | 0.54 | 158 |
| N8 | news50 | nip delta66 | j2a5R36e | -0.31 | -0.51 | 126 |
| N9 | news38 | relevance level | d5a2VOZJ | -0.05 | -0.78 | 101 |
| N10 | news38 | -metric vol 252 | VkNvj67J | 0.39 | 0.81 | 148 |

**归因**：
1. 情绪水平/冲击/推荐变动全面弱（|S|≤0.31 且多数 2Y 负）——RavenPack 事件情绪无定价力第 6 次复现（news20/news104 同判）。
2. **唯一亮点：vol/不确定性面**——N4（news18 -sse vol：S0.57/2Y1.44/lc170 高覆盖/TO0.024）+ N10（news38 同结构 +0.39）同机制同向，2Y 为正。与 earningscall T6 语调波动率（Mayew 不确定性溢价）先验同族。

**处置（BA3b 已派）**：level/delta 面两次证死不再铺池；定向打 vol/不确定性机制面 6 条（news18 sse vol 窗口 66/252 + tvr_decay + 多实体层 + news38 两腿）——探明 vol 族天花板后按新闸出 PROVISIONAL 或合规终判。

---

## BA3b 收割（sim 1xXlV22vK4kJ9PttwLzsCUG，6/6 COMPLETE，0 error）

| # | 表达式 | alpha | S | 2Y | sub | lc | TO |
|---|---|---|---|---:|---:|---:|---:|---:|
| V1 | -sse vol 66 | 58JZoVwM | 0.14 | 1.18 | -0.45 | 170 | 0.041 |
| V2 | -sse level 66（对照） | A1xRMdwX | 0.01 | 0.54 | 0.13 | 170 | 0.038 |
| V3 | -sse vol 252 x tvr_decay | 1YWqQ5dQ | **0.57** | **1.43** | -0.15 | 170 | 0.024 |
| V4 | -多实体 sse vol 252 | rK71vmlo | 0.41 | 0.48 | 0.00 | 148 | 0.035 |
| V5 | -news38 metric vol 66 | Jj8VZLOW | 0.32 | 1.21 | 0.14 | 165 | 0.035 |
| V6 | -news38 relevance level 66 | GrmqpvLZ | 0.15 | 0.58 | -0.54 | 150 | 0.041 |

**vol 族终读**：天花板 = **0.57**（BA3 N4 与 BA3b V3 同一表达式族，tv r_decay 平滑版 0.57/1.43 非噪声但也不增长）。窗口 66 版掉到 0.14 ⇒ vol 信号依赖长窗 252；多实体层 0.41、news38 0.32-0.39 同向但更弱。**族天花板 0.57 << 1.58，且 sub_universe_sharpe 为负**（-0.15~-0.45，子宇宙不健康）。

## news 塔新闸结论（2026-11-10）

- news18：**PROVISIONAL 信号层弱**（BA3 10 条 + BA3b 6 条 = 16 条证据；level/delta/vol 三机制面全探，天花板 0.57；缺 D6 第二配置但天花板距离 1.58 达 1.01，配置救不了）⇒ 不再追投，亦不写「终判死」（按新闸 D6 空档保留）。
- news50 / news38：**PROVISIONAL**（各 3-4 条探针，天花板 0.31/0.39）。
- **news 塔整体**：「事件情绪通道终判死」表述已永久撤回，替换为「**事件情绪族 16+ 条证据、三机制面天花板 0.57、子宇宙不健康——证据极弱面，不再追投**」。

## 重开阶梯总结（用户「判死太快」指令闭环）

| 塔 | 波次 | 结果 |
|---|---|---|
| RISK | BA1 探针 → BA2 池 → BA2b 变维 | risk60/risk88 **六维合规信号层死**（0.90/0.79，2Y 弱）；risk68/71/72 数据层排除 |
| NEWS | BA3 首探 → BA3b 定向池 | news18/50/38 **PROVISIONAL 信号层弱**（天花板 0.57，三机制面全探）|
| SOCIALMEDIA | AU2 十模板池 | socialmedia12 维持死（0.73） |

**净产出**：22+6+6+10 = 44 条新证据；2 个塔结案（1 个合规死 + 1 个 PROVISIONAL 弱）；0 个新活件。风险塔原结论全部经受住重开检验，news 塔纠正为证据化表述。重开队列余量：BA4 低优先池（analyst83/multifactor_return_pred/ai_news_scores/news_sentiment_nlp/other545/institutions4/sentiment33 + 待复核档案）。
派发：后台 watcher（cache/_watchBA3.ps1），sim id 落 cache/_out_BA3_ok.json。