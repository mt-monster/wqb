# EUR / news73 / wave1 模板池（NEWS 面新机制面 · Dow Jones 实体级细粒度情绪分量族）

> 状态：取证齐备（字段画像 + 判决对照 + 论坛 3 篇 + 外部论文 3 篇） + 12/12 结构互异模板 + preflight/validate 全过，**未派发**。
> 触发条件：在飞批次 `3HirxTDL4IfaCt26gC8b8O`（占 2 slot）解冻收批写 §98 后、并发槽释放；按 §93 换面纪律，news73 是「无判决记录 + 与 news48/news50/news29 不同源」的合法新机制面。
> 派发纪律：并发 2、`create_multi_simulation` 每批恰好 2 条、一批一套 settings（EUR/TOP2500/D1/FAST/decay1/trunc0.04/unit VERIFY/nan OFF/pasteurization ON/max_trade OFF）、过 toolkit_static 静态闸；派发后按模板编号归因。
> 算子数硬约束：12 模板算子数 2–5，全部 ≤12、越少越好；无装饰算子、无权重网格。

## §一 机制面定性（本轮 S1 取证核心）
- **数据集**：news73，EUR/TOP2500/D1，22 字段全 VECTOR、cov 均 0.813（`get_datafields filter_sharpe=false` 全量；默认 `filter_sharpe=true` 只回 17 字段，台账 §88 枚举表记 22 字段一致）。
- **本质**：Dow Jones / Acuity 文章级 + 实体级**细粒度情绪分量**，不是 news48 的连续综合分数、不是 news29 的离散事件标签、不是 news50 与 news48 同源的连续分数族 ⇒ **换 dataset id 也换了机制面**（§97 附录 5 同源比对纪律满足）。
- **字段三族**：
  - 文章级全局 8 分量 `nws73_globalsent_{certainty,fear,findown,finhype,finup,finvolatile,negative,positive,uncertainty}score`（9 个，含 finup）
  - 实体级 8 分量 `nws73_entitiessent_{certainty,fear,findown,finhype,finup,finvolatile,negative,positive,uncertainty}partscr`（按 `entitiesCounter_str` 对齐的 per-entity 部分分数）
  - 元数据 4 `nws73_djnsubject`(主题码) / `nws73_djnindustry`(行业码) / `nws73_entitiescounter`(实体提及计数字典) / `nws73_headlines`(标题文本)
- **可建骨架族**：① 分量水平 rank ② 全局−实体级价差（文章基调 vs 被点名实体的定向情绪错位）③ 分量比值/非线性 ④ 实体间分歧 `vec_stddev` 二阶矩 ⑤ 实体广度计数 `vec_sum(entitiescounter)` ⑥ 一阶差分/时序 zscore 新闻动量 ⑦ 分组轴 `sector`/`industry` 中性化。

## §二 判决对照（§93 / §97 附录 2 纪律）
- `get_dead_datasets(EUR)` 仅 4 集 `ml_factor_proj/model354/news36/news38`（只读 ledger_kv `*_dead` 键），**不含 news73**。
- WAVE_LEDGER 散文 grep：news73 仅 2 命中 —— §88 L4708 枚举表标「未探」、§93 附录 A L6528 列在「无实质判决(12)」清单。**无判死/判贫瘠/收手记录**。
- §93 附录 A 号称「12 个无判决 NEWS 集」本轮已纠偏：news84/news85/news46/news17 早判死、news54 S0.22、news59 仅 2 字段贫瘠；真正干净的新机制面 = news73 / news31 / news20。本池取 news73。
- **同源比对**：news48 `nws48_*` 连续综合分数族、news50 `mws50_*` 与 news48 22 后缀一一对应、news29 公司事件离散标签族 —— news73 `nws73_globalsent_*/entitiessent_*` 与三者**无后缀同源**，不是换 id 重刷判死面。

## §三 论坛取证（platform `search_forum_posts` + `read_forum_post`，3 篇正文）
- `43444585257879`「vec_sum 还是 vec_avg：拿到 VECTOR 字段先回答这个问题再写表达式」→ 5 种 VECTOR 折叠几何：`vec_avg` 水平 / `vec_sum` 广度 / `vec_count` / `hump` 降换手 / `kth_element` 取单元素 / `group_neutralize` 去行业偏。支撑 T01/T06/T07/T10 的折叠选型。
- `18641983716503`「【Alpha灵感】The Momentum of News」(17 票) → `ts_delta(vec_avg(...),5)` 新闻动量 + `signed_power` 非线性 + `trade_when` 事件门控。支撑 T08/T09。
- `4084748100087`「【Alpha灵感】使用nip族数据点亮news塔」(94 票/22 评论，EUR 区) → `ts_corr` / `group_neutralize` / FAST neutralization 适合 sentiment 类数据、news 与 sentiment 强关联、nip 门控几何。支撑 T03/T05/T12 的分组轴与相对化。

## §四 外部论文取证（arXiv API HTTP200 + OpenAlex DOI 直取端点 HTTP200；论坛/论文只验第一性原理，不等于验证 news73 作分组轴有效）
- **Tetlock 2007**《Giving Content to Investor Sentiment: The Role of Media in the Stock Market》(Journal of Finance, cited 4790, OpenAlex `works/https://doi.org/10.1111/j.1540-6261.2007.01232.x`)：高媒体悲观预测价格下行压力、随后回归基本面，高低悲观伴随高成交量 ⇒ 支撑「情绪分量水平 + 方向（fear/negative）」骨架与 T02/T08 反向先验。
- **arXiv**《A Framework for Measuring How News Topics Drive Stock Movement》：多数研究把每日新闻情绪聚成单一分数，掩盖主题内容与相关性差异 ⇒ 支撑「分量拆解 / 主题码分层」而非单分数（本池 12 模板全部按分量拆）。
- **arXiv**《Beyond Polarity: Multi-Dimensional LLM Sentiment Signals for WTI Crude Oil Futures Return Prediction》：传统单一极性情绪漏掉大量非结构化新闻信息，多维度情绪信号改善预测 ⇒ 支撑 news73 的 fear / uncertainty / certainty / finhype / finvolatile 多分量并行。
- **arXiv**《News-based trading strategies》：新闻文本中的分散信息被市场即时处理 ⇒ 支撑新闻动量 `ts_delta`/`ts_zscore` 骨架。
- 通道备注：`web_search` 402 余额耗尽、Semantic Scholar 429、OpenAlex `works?search=` 匿名限流 429；本轮改走 arXiv `export.arxiv.org/api/query` + OpenAlex `works/https://doi.org/<doi>` 直取端点，均 HTTP200、无需密钥，论文取证闭环。Tetlock 2008 DOI 误配到《Term Structure of Real Rates》，不采用；Garcia 2013 DOI 端点 404，不采用、不编造。

## §五 12 个结构互异模板（preflight valid / validate valid / 算子数 2–5）

| 编号 | 机制面 | 表达式 | 算子数 | 来源 |
|---|---|---|---|---|
| T01 | 极性净差·水平 (pos−neg) 经 sector 中性化 | `group_neutralize(rank(subtract(vec_avg(nws73_globalsent_positivescore),vec_avg(nws73_globalsent_negativescore))),sector)` | 5 | paper Tetlock2007 + forum nip 分组轴 |
| T02 | 恐惧水平·反向 | `-rank(vec_avg(nws73_globalsent_fearscore))` | 2 | paper Tetlock2007 |
| T03 | 不确定性·分组轴 group_rank | `group_rank(vec_avg(nws73_globalsent_uncertaintyscore),industry)` | 2 | forum nip / vec 折叠帖 |
| T04 | 波动/确定性比值·非线性相对化 | `-rank(divide(vec_avg(nws73_globalsent_finvolatilescore),vec_avg(nws73_globalsent_certaintyscore)))` | 4 | paper 多维度情绪 + forum momentum |
| T05 | 全局−实体级定向情绪价差 (findown) | `group_neutralize(rank(subtract(vec_avg(nws73_globalsent_findownscore),vec_avg(nws73_entitiessent_findownpartscr))),sector)` | 5 | 自建（实体级分量本集独有机制） |
| T06 | 实体间恐惧分歧·二阶矩 vec_stddev | `rank(vec_stddev(nws73_entitiessent_fearpartscr))` | 2 | forum vec 折叠帖(vec_stddev 分歧几何) |
| T07 | 实体提及广度·vec_sum 计数 | `rank(vec_sum(nws73_entitiescounter))` | 2 | forum vec 折叠帖(计数用 vec_sum) |
| T08 | 负面新闻动量·一阶差分 ts_delta 5(周窗) | `-rank(ts_delta(vec_avg(nws73_globalsent_negativescore),5))` | 3 | forum The Momentum of News + arXiv News-based trading |
| T09 | 正面分量·非线性 signed_power | `group_neutralize(signed_power(rank(vec_avg(nws73_globalsent_positivescore)),2),sector)` | 4 | forum The Momentum of News(signed_power) |
| T10 | 金融炒作分量·水平 | `rank(vec_avg(nws73_globalsent_finhypescore))` | 2 | paper 多维度情绪(非单一极性) |
| T11 | 实体级负面 − 全局负面·错位价差 | `rank(subtract(vec_avg(nws73_entitiessent_negativepartscr),vec_avg(nws73_globalsent_negativescore)))` | 4 | 自建（实体级分量本集独有机制） |
| T12 | 恐惧·时序 zscore 66(季窗) 经 sector 中性化 | `group_neutralize(rank(ts_zscore(vec_avg(nws73_globalsent_fearscore),66)),sector)` | 4 | forum momentum(时序平滑) + 分组轴 |

- **结构互异校验**（骨架/算子几何/矩/分组轴/非线性五维）：水平 rank(T02/T10) · 净差(T01) · 比值(T04) · 全局−实体价差(T05/T11) · 二阶矩(T06) · 计数广度(T07) · 一阶差分(T08) · 时序 zscore(T12) · 非线性 signed_power(T09) · 分组轴 group_rank(T03) · sector/industry 中性化(T01/T05/T09/T12)。无「同骨架换窗口/换常数」凑数；`5` 为周窗、`66` 为季窗，均有意义。
- **preflight/validate 结果**：`preflight_expressions(dataset_id=news73, auto_fix_vector=true)` → `valid:true / unknown_fields:[] / any_changed:false`；`validate_expressions` → `valid:true / unknown_fields:[]`；12 条字段全在平台 EUR 字段面（含被默认 sharpe 过滤的 finup/entity positive/uncertainty）。未用 `ts_max` / `quantile(x,120)` / `vec_norm` / `clamp` 等 EUR 不可访问算子。

## §六 派发前/收批后契约
- 派发前：确认 `3HirxTDL4` 已收批写 §98、并发槽释放（task_query(running)=0）；本池 12 模板分 6 批、每批 2 条，按编号顺序 T01+T02 → T03+T04 → …，一批一套 settings，不叠加。
- 收批后：按模板编号归因（哪个模板族出货/全灭）、逐年 `get_alpha_yearly_stats` 查 2014–2023 `longCount>0 && pnl≠0`（连续空窗判死口径）、pyramid 是否纯净 NEWS 单塔 ATOM、CW/TO 双边闸 `[1%,70%]`、破墙成功判据「TO 降 + CW 转 PASS + S/2Y 仍在」三者同时。
- 硬止损：若 12 模板全灭，按 §93 纪律写备靶前先对候选集逐个做字段画像 + 台账判决对照，不得凭记忆点名已判死集；合法下一步只剩 news31(文本形态统计族)/news20(专用分类器情绪族) 或已登记组合备靶，且须标注配额。
- 与 §97 附录 8/10 口径一致：progress 0.15→0.9 决定性推进 = 活跃注册批次非孤儿，`3HirxTDL4` 不按冻结轮数重发、不叠加新批、不占 prod 队列；`bl6Ogwm6` 维持 §72 fee×shortint 族级判死；唯一待授权 `ZYQmolVx`。



---

## ★ 判决三源全文对照纠偏（§101，2026-11-05 补记，覆盖上文「判决对照/状态」失实结论）
- 上文「判决对照」章节只查了 `get_dead_datasets` + WAVE_LEDGER 散文两源、并据此写「无判死记录 / 合法新面 / 备靶待派」——**已失实**。按 §101 的「全文 token 级三源叠加」复核：`get_dead_ends(EUR)` 全文里本集有独立判死记录（news29 主题显著性族 id=1343 / news50 机制封存 id=1352 / news73 整集判死 id=1600）。
- ⇒ 本模板池**不得派发**：已判死面，剩余模板一律不派、不另开波、不作换面备靶；本会话此前据此派发的批次属重复刷判死面白烧，已在 §101 据实记录。
- 换面前置四项硬约束（字段族同源比对 / 逐年覆盖 / 论坛论文取证 / ≥10 模板池）与 173 集三源全文底表见 `tracking/EUR/VERDICT_AUDIT_20261105.md`；本池仅作历史归档，不作「合法新面」依据。