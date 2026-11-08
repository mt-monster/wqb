# EUR / news29 / wave1 模板池（NEWS 面新机制面 · 公司事件新闻元数据/分类标签族）

> 状态（§100 后更新）：取证齐备 + 模板池就绪 + preflight 14/14 valid；**首批 T01+T03（§99，0/2）、递进探针第二批 T05+T10（§100，0/2）均已收批入库，累计 4/6 结构互异骨架全灭；第三批 T07+T08 已派发（multisim nRViNbSm5bpbYy1eyjDNaTR，收批在途、结果未知）**。未触发 §七 硬止损（须累计 ≥6）；第三批若仍全灭即达 6 ⇒ 正式收手换 news50/news73。
> 换面依据（§98 重新裁定）：`3HirxTDL4` 判僵尸批（progress 0.9 停滞 12 读数 + 并发槽实测空闲），news48 按已实测 6 模板全灭整集收手；T09/T11 记为「平台侧未产出/弃测」，非「测了 0/2」。按 §93 纠偏换面到此集，并发 2、每批恰好 2 条。当前唯一活跃批次 = nRViNbSm5bpbYy1eyjDNaTR（第三批 T07/T08）占 2 slot，收批释放前不叠加；首批 48bbH7F24P2ap4tczX6Rf3、第二批 3f3pmLeDr5ezab118I0FizsD 均已收批入库、旧僵尸批 3HirxTDL4 不占槽。

## 一、数据集画像（MCP get_datafields，EUR/TOP2500/D1，complete=true/platform_count=12）
12 字段全 VECTOR、cov 0.2956–0.7733。本质是「公司事件新闻元数据/分类标签」族，不是连续情绪分数：
- 文本全文/标题：company_event_description_text_full(.7733) / company_event_headline_text_full(.7733) / company_event_structured_fields_full(.2956)
- 主题码：event_secondary_topic_code(.7559) / event_tertiary_topic_code(.7559) / nws29_full_topic1(.7559) / nws29_topic1(.7733) / nws29_topic2(.371)
- 显著性：nws29_significance(1=High/2=Med/3=Low, .7733) / nws29_full_significance(High/Med/Low, .7559)
- 头版标志：nws29_frontpage(0/1, .7733) / nws29_full_frontpage(0/1, .7559)

机制定性（CLAUDE.md 准则）：离散分类标签 / 事件标志 ⇒ 适合做 group/bucket 自定义分组或事件计数/广度，不适合直接 rank 水平值（news48 连续情绪分数 rank 几何已在 EUR 证伪）。本池骨架落在「事件计数(vec_sum) / 显著性水平(vec_avg) / 时序分位(ts_zscore·ts_rank) / 一阶差分(ts_delta) / 二阶矩(vec_stddev) / 分组轴(sector) / 条件门控(trade_when) / 比率 / 乘积非线性」——与 news48「vec_avg 单/双字段 + rank/比率」高度同质的 4 模板形成结构互异。

## 二、取证（用机制前查论坛 + 外部论文，Goal 第 2 条）
- 论坛 search_forum_posts：「news event vector aggregate salience template」命中 news54/news48/Sentiment1/nip 等他集帖；「news29 Data Idea」两次未命中 news29 专属 Data Idea（第 7 轮 + §97 附录 2 一致）。无专属模板可抄，骨架靠第一性原理自建。
- 外部论文（§93 附录 D 已闭环，web_fetch OpenAlex/arXiv HTTP200 备用通道）：arXiv:2010.07289「Choosing News Topics to Explain Stock Market Returns」(sLDA 监督主题模型选新闻主题解释收益) 支撑「主题码携带收益信息」；OpenAlex W3171163353 / doi 10.2139/ssrn.3850923；Tetlock(2007) JF、Da/Engelberg/Gao(2011) JF、arXiv 2309.05560「New News is Bad News」一致指向「须相对化 / 新颖性」。窄查询 news+salience+attention+returns 命中 0 篇，诚实标注未取到。
- 诚实边界：论文验证的是「新闻主题/情绪分类携带收益信息」这一第一性原理，不等于已验证 news29 的「主题码/显著性元数据」作分组轴有效；须实测归因。

## 三、判决对照（§93 纠偏）
- get_dead_datasets(EUR) 仅返回 4 集 ml_factor_proj/model354/news36/news38（只读 ledger_kv 的 *_dead 键）；叠加 WAVE_LEDGER grep 散文对照：news29 命中 4 行（6362 枚举 / 6528 无判决清单 / 6529 S1 队列 / 6548 附录B 画像）+ 附录D 论文取证，无实质判决，是合法 S1 体检队列。不得只凭工具返回里没出现就推定无判决、也不得把已判死集(sentiment27/other553/sentiment7/news17/news52/news54)写成备靶。

## 四、14 个结构互异模板（T01–T14，纯 NEWS 单塔 ATOM，算子 ≤12、越少越好）
来源标注：[S]自建第一性原理 / [F]论坛概念骨架 / [P]论文方向先验。字段已全部手动 vec_* 包裹。

| # | 表达式 | 机制骨架 | 几何/矩/分组轴 | 算子数 | 来源 |
|---|---|---|---|---|---|
| T01 | rank(vec_sum(nws29_frontpage)) | 头版事件计数·水平 | vec_sum 总量·零阶计数 | 2 | [S] |
| T02 | -rank(vec_sum(nws29_full_frontpage)) | 全量头版计数·反向 | vec_sum 反向 (方向自洽对照 T01) | 2 | [S] |
| T03 | -rank(vec_avg(nws29_significance)) | 显著性水平·反向(High=1) | vec_avg 水平·一阶中心矩 | 2 | [S][P] |
| T04 | rank(vec_avg(nws29_full_significance)) | 全量显著性·正向 | vec_avg 水平 (版本族对照 T03) | 2 | [S] |
| T05 | rank(ts_zscore(ts_backfill(vec_sum(nws29_frontpage),22),66)) | 头版计数·时序分位 | ts_zscore 66 季窗 + backfill | 4 | [S][P] |
| T06 | -rank(ts_rank(ts_backfill(vec_sum(nws29_full_frontpage),22),252)) | 全量头版·年窗分位反向 | ts_rank 252 年窗 + backfill | 4 | [S] |
| T07 | rank(ts_delta(ts_backfill(vec_sum(nws29_frontpage),22),5)) | 头版事件·一阶差分(新增事件) | ts_delta 5 周窗·一阶差分 | 4 | [S][F] |
| T08 | -rank(vec_stddev(nws29_topic1)) | 主题码分歧·二阶矩 | vec_stddev 二阶矩 / 主题族 | 2 | [S] |
| T09 | rank(vec_stddev(event_secondary_topic_code)) | 二级主题分歧·二阶矩 | vec_stddev / 跨字段族 | 2 | [S] |
| T10 | group_neutralize(rank(vec_sum(nws29_frontpage)),sector) | 头版计数·行业中性 | group_neutralize 分组轴 | 3 | [S] |
| T11 | trade_when(greater(vec_sum(nws29_frontpage),0),-rank(vec_avg(nws29_significance)),-1) | 有头版事件才反向押显著性 | trade_when 条件门控 | 6 | [S][P] |
| T12 | rank(subtract(vec_sum(nws29_frontpage),vec_sum(nws29_full_frontpage))) | 两版头版计数差·版本族套利 | subtract 双字段差 | 4 | [S] |
| T13 | -rank(divide(vec_avg(nws29_significance),vec_avg(nws29_full_significance))) | 显著性比率·相对化 | divide 比率 / 相对化 | 4 | [S][P] |
| T14 | rank(multiply(vec_sum(nws29_frontpage),vec_avg(nws29_significance))) | 计数×显著性·乘积非线性 | multiply 非线性交互 | 4 | [S] |

结构互异性自检：零阶计数(T01/T02) / 一阶水平(T03/T04) / 时序分位(T05/T06) / 一阶差分(T07) / 二阶矩(T08/T09) / 分组轴(T10) / 条件门控(T11) / 双字段差(T12) / 比率相对化(T13) / 乘积非线性(T14) —— 10 类骨架、≥10 个结构互异，差异落在几何/矩/分组轴/非线性，非「换窗口换常数」。方向自洽对照：T01↔T02、T03↔T04。算子数 [2,2,2,2,4,4,4,2,2,3,6,4,4,4]，最大 6 ≤12。

## 五、preflight（MCP preflight_expressions，本轮实测）
region=EUR / universe=TOP2500 / delay=1 / dataset_id=news29 / auto_fix_vector=true：
valid=true / unknown_fields=[] / any_changed=false / vector_fields 12 / platform_field_count=6 / 14 条表达式全过。手写的 vec_sum/vec_avg/vec_stddev 已覆盖全部 VECTOR 字段，无需自动修复。

## 六、门禁与派发契约（触发后执行）
- 每批恰好 2 条、并发限制 2、settings 沿用 EUR/TOP2500/D1/FAST/decay1/trunc0.04/unit VERIFY/nan OFF/pasteurization ON/maxTrade OFF。
- 派发前须 create_multi_simulation 过 toolkit_static 静态闸（preflight 只验字段+VECTOR，不验算子 arity/可访问性；vec_stddev 已 §97 确认 EUR 可访问、ts_max/quantile(x,120)/vec_norm 不在白名单）。本池用到的算子：rank/vec_sum/vec_avg/vec_stddev/ts_zscore/ts_rank/ts_backfill/ts_delta/group_neutralize/trade_when/greater/subtract/divide/multiply —— 除 vec_stddev 外均已在 EUR 历批实测通过；若门禁拦某算子，换已验证等价算子，不照抄论坛/跨区表达式。
- 首批建议：T01(计数水平) + T03(显著性反向) 作干净单变量对照，先判字段族有无横截面信号。
- 收批按模板编号归因 + 逐年 longCount>0&&pnl≠0 空窗核验 + pyramid 是否纯净 NEWS 单塔；同族全灭按 news52 三因分法（字段衰减/窗口错配/字段本身弱）做单变量只改窗长对照，别把骨架选错误判成字段没信号。

## 七、硬止损（预置，触发后生效）
若首批及递进探针累计 ≥6 个结构互异骨架全灭（S<1.58 且 2Y<1.58、0 过硬闸）⇒ 判 news29 整集字段族在 EUR/TOP2500 横截面信号弱、整集收手；换面只走 §93 附录 A 的 NEWS 面无判决集队列（news21/23/31/50/59/7/73/76/84/85 等，须各自先 S1 画像+论坛论文取证+≥10 模板池），不得凭记忆点名已判死集。

## 状态（§100 后更新）
- 取证齐备(论坛2次未命中专属帖 + 论文4篇独立核验) + 字段画像12字段 + 判决对照(无实质判决) + 14 结构互异模板 + preflight 14/14 valid + 算子 ≤6 ≤12 上限。
- **首批已收批（§99，48bbH7F24P2ap4tczX6Rf3 → N1Nel7pq/A1VQ8lwQ）**：T01 S0.15/F0.02/2Y−0.51/TO63%/CW超线、T03 S−0.2/F−0.02/2Y1.02/TO159.7%爆表，0/2 过硬闸 ⇒ 轴①水平几何无稳定横截面信号（逐年 sharpe 符号时变=日频噪声伪影）。`workflow_auto_harvest` 入库 upserted:2、暂定 verdict=FAIL。
- **递进探针第二批已收批（§100，3f3pmLeDr5ezab118I0FizsD → akKVmAlw/78LoPaQ2）**：T05（时序分位）S0.02/F0/2Y−1.08/TO29.86%（较 T01 腰斩但 S/2Y 没保住 ⇒ 证伪「强信号被换手税吃掉」、坐实噪声伪影）、T10（sector 中性）S0.57/F0.1/2Y0.7/TO65.79%（分组轴把 longCount 1372→436 仍够不到 1.58 闸）；0/2 过硬闸、逐年零空窗、纯净 NEWS 单塔 ⇒ 轴②时序分位、轴③分组轴均全灭。`workflow_auto_harvest` 入库 upserted:2、暂定 verdict=FAIL（0/4 过硬闸）。**累计 4/6 骨架，未触发 §七 硬止损**。
- **第三批已派发（§100，在途结果未知）**：T07 `rank(ts_delta(ts_backfill(vec_sum(nws29_frontpage),22),5))`（一阶差分·新增事件流）+ T08 `-rank(vec_stddev(nws29_topic1))`（主题码分歧·二阶矩，跨到 topic 码族验论文先验），全新几何 + 跨字段族、与已测 4 骨架互不重叠；preflight valid / unknown_fields=[] / any_changed=false、create_multi_simulation success 无 429、`multisim_id nRViNbSm5bpbYy1eyjDNaTR`。settings 同首批。
- 下一检查轮：收批 T07/T08 按模板编号归因 + 逐年空窗 + pyramid + 入库写 §101；**累计骨架将达 6**，若 T07/T08 仍全灭 ⇒ **正式触发 §七 硬止损**：判 news29 整集字段族在 EUR/TOP2500 横截面信号弱、整集收手，换面只走已备靶 news50 离散分类面 / news73 多分量面（各自 S1 画像 + 论坛/论文取证 + ≥10 模板池已在盘、须过 toolkit_static），不得凭记忆点名已判死集；有货按出货几何定向补 T06/T09/T11/T12/T13/T14。并发纪律：nRViNbSm5bpbYy1eyjDNaTR 是唯一活跃批次占 2 slot，收批释放前不叠加；旧僵尸批 3HirxTDL4 不占槽。
- 唯一待授权(§97 附录 6)：`ZYQmolVx`；`LLM5eAMn` 已提交、`1YNjqknX` 被 self 顶死、`bl6Ogwm6` §72 族级判死。本波零 POST submit、零不可逆动作。


---

## ★ 判决三源全文对照纠偏（§101，2026-11-05 补记，覆盖上文「判决对照/状态」失实结论）
- 上文「判决对照」章节只查了 `get_dead_datasets` + WAVE_LEDGER 散文两源、并据此写「无判死记录 / 合法新面 / 备靶待派」——**已失实**。按 §101 的「全文 token 级三源叠加」复核：`get_dead_ends(EUR)` 全文里本集有独立判死记录（news29 主题显著性族 id=1343 / news50 机制封存 id=1352 / news73 整集判死 id=1600）。
- ⇒ 本模板池**不得派发**：已判死面，剩余模板一律不派、不另开波、不作换面备靶；本会话此前据此派发的批次属重复刷判死面白烧，已在 §101 据实记录。
- 换面前置四项硬约束（字段族同源比对 / 逐年覆盖 / 论坛论文取证 / ≥10 模板池）与 173 集三源全文底表见 `tracking/EUR/VERDICT_AUDIT_20261105.md`；本池仅作历史归档，不作「合法新面」依据。