# EUR / news50 / wave1 模板池（在飞等待期零成本增量 · 备靶预备 · 未派发）

> 状态：§97 硬止损未触发、`3HirxTDL4` 在飞占 2 slot，本池**只备不派**。派发前须过 toolkit_static 静态闸（vec_stddev 已确认 EUR 可访问；ts_max/quantile(x,120)/vec_norm 不在白名单）。

## §一 机制面定性（本轮取证的核心发现）
- **news50 与 news48 同源**：37 个 `mws50_*` 字段中，22 个与 news48 的 `nws48_*` 一一对应（ens/g_ens/qep/ssc/qcm/qmb/nip/ens_elapsed/ens_similarity_gap/ghc_lna/ess/rp_story_event_count/rp_story_event_index/vea/relevance/acb/aes/bam/bee/ber/...）——是同一供应商的**连续情绪分数族**。news48 该族在 §95–§97 已判「横截面信号弱、整集收手」。
- **换 id ≠ 换机制面**：若沿用 `vec_avg(mws50_ens)` / `divide(vec_avg(mws50_ens),vec_avg(mws50_g_ens))` 这类 news48 相对化 rank 几何，等于换个数据集 id 重刷刚判死的机制面，白烧整波仿真。§97 硬止损把 `news29/news50` 并列为换面方向，对 news50 必须附本约束。
- **news50 独有新机制面 = 15 个离散分类/元数据字段**：`category / topic / news_type / group / sub_type / evaluation_method / maturity / property / position_name / product_key / country_code / ens_key / g_ens_key / ens_elapsed / time`。语义＝公司新闻的**主题分类、类型标签、分组、显著性、成熟度、时效**——离散分类标签，应走「分类码/分组轴 + 事件计数/广度」骨架，与 news48/news29 离散事件标志面互补但不同。
- 经济学第一性原理（论坛 + 论文）：新闻**主题/类别**携带横截面收益信息（arXiv 2010.07289《Choosing News Topics to Explain Stock Market Returns》；OpenAlex 新闻主题分类→收益可预测性 8052 篇）；分类数据的精准点塔/Single Data Set Alpha（论坛《获取分类数据及精准点塔和构建Single Data Set Alpha》《什么是混信号,什么是 Single Data》votes121）；VECTOR 折叠决定信号定义——计数/广度用 vec_sum、水平/均值用 vec_avg（论坛《折叠的那一刻》《vec_sum 还是 vec_avg》《和AI学点手搓小知识-vec操作符解析》votes48）。
- ★ 与既有纪律配合：论坛/论文只验证「新闻主题分类携带信息」这一第一性原理，不等于验证 news50 离散元数据作分组轴有效；与 §93「写备靶前先做字段画像+判决对照」、§97「news29 备靶须补 ≥10 模板池+preflight」同源，本池即其落地。

## §二 14 个结构互异纯 NEWS 单塔 ATOM 模板（算子数全 ≤12、越少越好）
| 编号 | 表达式 | 骨架/几何 | 矩 | 来源 | 算子数 |
|---|---|---|---|---|---|
| T01 | `rank(vec_sum(mws50_category))` | 零阶计数·vec_sum | 水平 | [S]自建+[F]折叠帖 | 2 |
| T02 | `-rank(vec_avg(mws50_topic))` | 一阶水平·vec_avg(方向对照) | 水平 | [S]自建 | 2 |
| T03 | `rank(vec_sum(mws50_rp_story_event_count))` | 事件计数·vec_sum | 计数 | [S]自建+[P]主题分类论文 | 2 |
| T04 | `group_neutralize(rank(vec_sum(mws50_category)),sector)` | 分组轴·sector 中性化 | 水平 | [S]自建+[F]点塔帖 | 3 |
| T05 | `rank(vec_stddev(mws50_relevance))` | 二阶矩·vec_stddev 分歧度 | 二阶 | [S]自建 | 2 |
| T06 | `rank(ts_delta(ts_backfill(vec_sum(mws50_category),22),5))` | 一阶差分·ts_delta 周窗 | 一阶 | [S]自建 | 4 |
| T07 | `rank(vec_sum(mws50_news_type))` | 零阶计数·类型标签 | 计数 | [S]自建 | 2 |
| T08 | `-rank(vec_avg(mws50_maturity))` | 一阶水平·成熟度(方向对照) | 水平 | [S]自建+[P]信息时效 | 2 |
| T09 | `rank(vec_sum(mws50_sub_type))` | 零阶计数·子类型 | 计数 | [S]自建 | 2 |
| T10 | `rank(ts_zscore(ts_backfill(vec_sum(mws50_rp_story_event_count),22),66))` | 时序分位·ts_zscore 季窗 | 时序 | [S]自建+[P]注意力分位 | 4 |
| T11 | `rank(vec_stddev(mws50_evaluation_method))` | 二阶矩·评估方式分歧 | 二阶 | [S]自建 | 2 |
| T12 | `rank(subtract(vec_sum(mws50_category),vec_sum(mws50_group)))` | 双字段差·分类 vs 分组 | 一阶 | [S]自建 | 3 |
| T13 | `rank(divide(vec_avg(mws50_relevance),vec_avg(mws50_ens)))` | 比率相对化·显著性 vs 情绪 | 比率 | [S]自建 | 3 |
| T14 | `rank(multiply(vec_sum(mws50_category),vec_avg(mws50_qep)))` | 乘积非线性·计数×质量 | 非线性 | [S]自建 | 4 |
- [S]自建 / [F]平台论坛 / [P]外部论文。10 类骨架：零阶计数(vec_sum) / 一阶水平(vec_avg) / 二阶矩(vec_stddev) / 一阶差分(ts_delta) / 时序分位(ts_zscore) / 分组轴(group_neutralize) / 双字段差(subtract) / 比率相对化(divide) / 乘积非线性(multiply) / 方向对照(T01↔T02、T07↔T08)。
- 算子数 `[2,2,2,3,2,4,2,2,2,4,2,3,3,4]` 最大 4 ≤12；换窗口(5/22/66)不算结构差异，靠骨架/几何/矩/分组轴/非线性变换凑够 14 个互异模板。
- 时间窗口取值：日1 / 周5 / 月22 / 季66 均为有意义标准窗；`ts_backfill(...,22)` 月窗兜底稀疏、`ts_zscore(...,66)` 季窗匹配新闻主题半衰期。

## §三 4 对照轴（收批按模板编号归因）
- 轴① 计数 vs 水平：T01(vec_sum category) ↔ T02(vec_avg topic)——离散标签该用计数还是均值。
- 轴② 二阶矩/分歧度：T05 / T11(vec_stddev)——分类分歧是否比水平更有横截面信号。
- 轴③ 时序加工：T06(ts_delta 一阶) / T10(ts_zscore 分位)——分类计数是否需意外化/分位化。
- 轴④ 分组轴 vs 相对化 vs 非线性：T04 / T13 / T14 / T12——sector 中性化、比率、乘积、双字段差哪条几何能提炼分类信息。
- 硬止损（预置）：累计 ≥6 个结构互异骨架全灭(S<1.58 且 2Y<1.58) ⇒ 判 news50 离散元数据面在 EUR/TOP2500 弱、整集收手；换面只走 S1 枚举×判决对照后的新机制面，不得凭记忆点名已判死集。

## §四 派发契约（触发后，未派发）
- 首批 T01+T03（零阶计数 vs 事件计数，干净单变量对照）；每批恰好 2 条并发 2，`create_multi_simulation` 须过 toolkit_static 静态闸；settings 沿用 EUR/TOP2500/D1/FAST/decay1/trunc0.04/unit_handling VERIFY/nan_handling OFF/pasteurization ON/max_trade OFF。
- **禁止**把 `vec_avg(mws50_ens)` / `divide(vec_avg(mws50_ens),vec_avg(mws50_g_ens))` 等 news48 同源连续情绪分数几何当 news50 新模板——那是重刷已判死面。
- 收批：harvest→get_alpha_details/逐年 longCount>0&&pnl≠0→pyramid 是否纯净 NEWS 单塔 ATOM→按模板编号归因 + 4 对照轴逐轴判定→workflow_auto_harvest 入库。
- MCP `preflight_expressions(EUR,TOP2500,D1,dataset_id=news50,auto_fix_vector=true)` 14 条全过：`valid=true / unknown_fields=[] / any_changed=false / vector_fields 37 / platform_field_count=11`（手写 vec_sum/vec_avg/vec_stddev 已覆盖全部 37 个 VECTOR 字段）。

> 口径同步：本池与 `WAVE_LEDGER.md` §97 附录 5 同步；若 §97 硬止损触发且选中 news50，必须从本池离散元数据面派发，不得回退 news48 同源族。

---

## ★ 判决三源全文对照纠偏（§101，2026-11-05 补记，覆盖上文「判决对照/状态」失实结论）
- 上文「判决对照」章节只查了 `get_dead_datasets` + WAVE_LEDGER 散文两源、并据此写「无判死记录 / 合法新面 / 备靶待派」——**已失实**。按 §101 的「全文 token 级三源叠加」复核：`get_dead_ends(EUR)` 全文里本集有独立判死记录（news29 主题显著性族 id=1343 / news50 机制封存 id=1352 / news73 整集判死 id=1600）。
- ⇒ 本模板池**不得派发**：已判死面，剩余模板一律不派、不另开波、不作换面备靶；本会话此前据此派发的批次属重复刷判死面白烧，已在 §101 据实记录。
- 换面前置四项硬约束（字段族同源比对 / 逐年覆盖 / 论坛论文取证 / ≥10 模板池）与 173 集三源全文底表见 `tracking/EUR/VERDICT_AUDIT_20261105.md`；本池仅作历史归档，不作「合法新面」依据。