# 挖掘类 Skills 全量精读分析报告

> 2026-09-12 · 范围：`Claude/skills/` 全部 32 个 skill 的 SKILL.md 正文 + workflow 代码（`src/wqb/` 2082 行表达式核心 + workflow 8 节点 + modeb 2400 行）+ 4 份 toolkit config JSON + verifier 1377 行 validator + gem skeletons/run_pipeline + DB 模板台账（ledger `KB/*`）。
> 方法：12 个核心 skill 逐行精读 + 20 个其余 skill 全文通读 + 模板/算子资产交叉核算（代码、配置、DB 三方对账）。
> 集成度分级：**A1**=代码级内嵌（被 workflow 节点/引擎代码直调）；**A2**=SOP 步骤内嵌（九步中明确站位，Agent 按步执行）；**B**=链上引用（被其他 skill 按需调用）；**C**=独立/外围（SOP 无固定站位）；**元**=非挖掘专用。

---

## 第一部分 · 逐 Skill 分析（按 layer 分组）

### 编排层（SOP 骨架）

#### 1. wq-brain-ra-pipeline 【A1】
1. **定位**：唯一挖掘编排 SOP，九步（S-PRE→S6）定义每步目的/MCP 调用/产物/失败分支；区域 profile（11 份 frontmatter 契约）+ 决策表（D1-D14）+ PPA 经验库是它的三大参考资产。
2. **集成**：既是流程本身也是流程入口。`workflow_chain` 可串步 2-6（dry-run 先行）；8 个 registry 节点中 5 个直接对应它的步 2/3/4/5/6。实际效果：GBR 180 条零达标事故后，步 5 门禁 + 天花板闸接线使其成为"配额保险丝"。
3. **未集成部分**：步 1/7/8/9 无节点（设计如此——查表/评审/提交判定/回写涉及人工确认）。
4. **优化点**：① 535 行偏长，步 7 的 D14 三条破墙路径与 optimization-v1 的回流规则存在**两处表述**（内容一致但维护两份）；② profile 的 `entry_verdict=frozen` 判定依赖人工维护，未接 monitor §5.5 的饱和度输出（两套"区域状态"判断并存）。

#### 2. wq-brain-campaign-toolkit 【A1】
1. **定位**：战役引擎（唯一权威实现）：8 闸 gate.py、build_wave 选波、pipeline 端到端、scan_fields、LedgerStore、distill/os_feedback/family_atlas 三个学习闭环工具。
2. **集成**：双通道——CLI（被 sim-alphas subprocess 调用）+ MCP（wave_gate 节点包装 `tools/wave_gate.py`）。config/ 下 4 份 JSON 是全系统的"宪法"：platform_constraints（闸5/闸4 判据）、template_families（GEM 选族）、operator_semantics（GEM 语义）、methodology_rules（选波规则+计数回写）。
3. 不适用（已深度集成）。
4. **优化点**：① 4 份 config 的消费方分散在 gate.py/build_wave/gem 三处，**没有 schema 校验测试**——字段改名只能靠运行时报错；② `campaign.py` 子命令 15+ 个，README 索引与 SKILL §6 有轻微不同步；③ known_ops 与 operator_semantics 存在 6 处漂移（详见算子专题）。

#### 3. wq-brain-campaign-matrix 【A2】
1. **定位**：S-PRE 查表层：读 registry_empirical 三层（static/assets/empirical）→ 预解析配置包（含 PROD 饱和风险标注）。
2. **集成**：步 1 唯一入口；输出被 S0 体检与 score_datasets 消费；S6→S-PRE 闭环的另一端。
3. 不适用。
4. **优化点**：① §3 派发列表手工维护，与 ra-pipeline 正文存在**第三次重复**（同一派发信息三处书写——09-11 曾漏改此处）；② 扩区流程（§5）要求"三处同步"（REGIONS/profile/INDEX）纯靠人工，无测试锁（docs-consistency 测了前两处，第三处靠 review）。

#### 4. wq-brain-ppa-mining 【A2】
1. **定位**：S0 数据集级决策方法论：§1.0 三硬门槛（cov≥0.85/alphaCount≤50/fields≥10）+ 区域-类型亲和矩阵 + WebDataScope 10 指标→预处理映射 + 白空间发现 + 跨区域倍率表。
2. **集成**：S0 的方法论权威（"mode=ppa 下一票否决"）；执行工具 `dataset_health_check.py` 双通道（MCP 8876/direct）。白名单经 `upsert_ledger_key(s0_whitelist)` 入库供 S1 校验。
3. 不适用（§1.0 强制；§3 白空间/§8 倍率表为决策参考层）。
4. **优化点**：① §8 区域实证数据停留在 08-05 快照（KOR/EUR/HKG 数据集数），**没有刷新机制**——与 next-move §5.5 的饱和度检测功能重叠但互不引用；② 亲和矩阵的红灯规则（§1.0.x）是手写常量，未从 `get_dead_ends` 自动推导（文档自己说"规则引擎从台账自动推导"，实际是人工维护）；③ §6 两线口径 09-12 刚对齐 INDEX，但 §7 提交流程未链到 submit-alpha 新增的 PPA 通道节。

### 生成与回测层（S2/S3）

#### 5. brain-make-some-gem 【A1】
1. **定位**：S2 概念优先生成引擎（七槽配给、复杂度预算 2-5 算子、语义多样性判据、Expected Exposure 验证）。
2. **集成**：`workflow_gem` 节点强制调用；产物 `final_expressions.json` 经 `_find_final_expressions` 双路径校验后入 expressions 表；`--ideas-file` 消费 data-feature-engineering 的 S1 报告（ledger `s1_<ds>_d<delay>` 命中即跳过内嵌 S1）。
3. 不适用。
4. **优化点**：① **内嵌 `skills/brain-feature-implementation` 副本与正本已分叉**（`implement_idea.py` md5 不一致，副本内还多一份 validator.py）——第二实现危险信号；② template_families.json 的 8 族消费点在 run_pipeline，但**族与七槽的配给映射**（≥2 跨金字塔/≥1 win 换腿）写在 ra-pipeline 正文而非 config，改配给要动 SOP 文档；③ skeleton mode（P0）与 family mode 的选择逻辑在代码里，SKILL.md 只字未提 skeleton mode 的触发条件。

#### 6. brain-sim-alphas-in-batch-and-track 【A1】
1. **定位**：S3 批量回测单一入口（入口/引擎分工：本 skill 编排，toolkit 执行）。
2. **集成**：`workflow_batch_track` 节点；`--from-db` 默认读 expressions 表；断点续跑 CSV 定位已澄清（进度缓存≠真相源）。
3. 不适用。
4. **优化点**：① 双路径（战役引擎 pipeline.py vs 自带 batch_simulator.py）长期共存，ad-hoc 路径的 `--batch-size 3 --concurrency 2` 示例数字与七槽纪律并存，新人易混（已加边界注释但示例本身仍可跑出反纪律行为）；② 与 wqb-concurrency §8 的内容重叠面仍有 30%（SOP 表格复述了七槽要点），单源化未彻底。

#### 7. brain-inspect-raw-template-create-setting 【A2→B】
1. **定位**：idea JSON → expressions 表的入库通道（`build_alpha_list.py` 直写）+ 新区域 sim_options 快照；2026-09-01 已精简掉人工设置决策环。
2. **集成**：上游接 gem 产出的 `*_idea_*.json`；下游 S3 `--from-db`。但 gem 主路径下表达式由 gem 自己入库，**本 skill 实际只服务"手动提供模板 JSON"与"新区域快照"两个场景**——集成度已从 A2 降为 B。
3. **潜在价值**：新区域（如 JPN/ILLIQUID 若启用）首次设置快照是刚需；可把它显式登记为 ra-pipeline 扩区流程（§5）的标准步，而不是游离子。
4. **优化点**：① 名称极长且名不副实（"create-setting"职能已删）；② `alpha_list.json` 追加模式与"DB 单轨"铁律并存，是三条持久化铁律声明中唯一还保留文件产物的 skill（文档已声明其为兼容，但两轨并行易误用）。

#### 8. brain-data-feature-engineering 【A1】
1. **定位**：S1 字段→特征概念（8 问问题库、字段透明度分档、S1⇄S2 状态机）。
2. **集成**：双路径统一——standalone（写 ideas.md + ledger `s1_<ds>_d<delay>` source=standalone）与 gem 内嵌（source=s2_nested），**同一 ledger key 收敛**，这是全仓设计最精巧的单点收敛；另有 `workflow_feature_engineering` 节点。
3. 不适用。
4. **优化点**：① 312 行全仓第 4 长，8 问框架与 GEM 的 8 个概念位、hypothesis-first 的 12 假设类三者是**三套概念分类学**，映射关系无人写明（同一字段可能被三套框架贴三个标签）；② 分档规则（透明/黑盒/半透明）是 2026-09-01 一次性审计结论，硬编码在文档里，没有随字段描述覆盖率数据自动复核的机制。

### 研究与数据层（S0/S1 支撑）

#### 9. brain-alpha-research 【B】
1. **定位**：研究总入口 + 论坛模板挖掘协议（PARADIGMS P1-P13 分类、形状覆盖检查、17 幽灵算子核对、universe 固化表）。
2. **集成**：路由表已把 3 个子方向拆出；研究产出回写 `config.py`/`KB/community_tpl_kb`。
3. 不适用。
4. **优化点**：① §7-9（模板挖掘三规则）是**模板链路上最重要的治理条款，却埋在研究 skill 里**——GEM 与 toolkit 的文档都不引用它；② `grammar._OP_ARITY` 扩展流程（先 get_operators 核实再入库）无自动化（论坛新模板的算子仍是人工核对）。

#### 10. brain-alpha-research-field-quality 【B】
1. **定位**：字段质量先验（alphaCount/userCount 排序播种）+ WebDataScope 23 条预筛规则 + **区域切换强制门禁**。
2. **集成**：S0 前置纪律（区域切换必跑 `webdata_quality.py`）；与 ppa-mining §1.0 互补（一个数据集级、一个字段级）。
3. 不适用。
4. **优化点**：① "区域切换门禁"靠纪律与验证清单保证，**没有像天花板闸那样的机器拦截**（谁忘跑谁全批烧配额——USA/GBR 曾违规）；② 23 条规则速查与全文（research/references）两处维护，速查表会漂移。

#### 11. brain-alpha-research-hypothesis-first 【C，高潜】
1. **定位**：饱和数据集（≥1 万 alpha）的假设优先工作流：字段语义 YAML（anchor_only 标记）→ ≥20 条可证伪假设目录 → `hypothesis_miner.run_hypothesis_round` 每实验派发 4 条（主假设/消融/对照/变体）→ 四态判定。
2. **集成**：**未实际挂接**。代码支撑真实存在（`src/wqb/research/hypothesis_miner.py`），但九步 SOP 无站位、无节点、主力战役（IND/USA/EUR）从未按此流程跑过。INDEX 登记为 L1。
3. **潜在价值（全仓最高）**：存量信号空间"开采殆尽"是当前第一瓶颈（SELF/PROD 双闸 + 模板遍历到顶），本 skill 是唯一直接对准该瓶颈的方法论——对照/消融设计天然产出"与 book 正交"的证据链。**可行路径**：① 在 ra-pipeline 步 2（S0-select）加一条路由："dataset alphaCount≥10K 或连续 2 波模板全灭 → 强制转 hypothesis-first"；② 把假设目录（YAML）纳入 ledger（`hyp_<ds>` 键）复用 S1⇄S2 同款状态机；③ `run_hypothesis_round` 包一个 workflow 节点（照 wave_gate 节点模式，低成本）。
4. **优化点**：`data/hypothesis_catalog/` 与 `data/hypothesis_ledger/` 是文件态台账，与"DB 单轨"铁律冲突（同类问题：idea_ledger 在 src/wqb/memory 有 DB 版但此 skill 用 JSONL）。

#### 12. brain-alpha-research-news-sentiment 【B→降级】
1. **定位**：新闻/情绪 5 家族分类 + 6 桶配对硬闸 + Tier A 组合（`news_field_classifier.py` 代码真实存在）。
2. **集成**：对 news 类数据集的 S1 强制分类闸；Tier B（news12/news18/socialmedia12）饱和标注。
3. **价值重估**：GLB emotion 族 42 候选全灭（PROD 0.82-0.86）后，情绪方向的性价比已被亲和矩阵标红；但 5 家族/6 桶作为**分类闸**对任何 news 数据集仍有效（HKG `news_sentiment_nlp` 是当前头号目标）。可行路径：与 ppa-mining 的白空间表联动，把 Tier A 清单按区域×倍率动态化（现清单是 2026-04 静态值）。
4. **优化点**：Tier A 清单静态（news59 等的倍率/拥挤度会轮动），§3 自己说"平台倍率变化时用 wqb news-refresh-portfolio 刷新"，但该命令消费无人值守；6 桶闸的判定在文档，分类器代码只做家族归属——**桶配对校验没有代码实现**。

#### 13. alpha-template-labs-data-analysis 【C】
1. **定位**：S0 前研究（Python alpha 前置）：Labs WorkSpaces 原始面板诊断 → ≤2 个 MATRIX 字段的机制结论。
2. **集成**：未进 SOP（INDEX 登记为 L0 user-invocable）；MCP Labs 工具链（authenticate_brainlabs/emit_labs_script/ingest_labs_result）+ CLI 专用步骤。
3. **潜在价值**：MATRIX 数据集的 Python 原生优势判定（非 FASTEXPR 表达式赛道）——是 USA/TOP3000/D1 之外几乎唯一的差异化赛道，但当前挖掘管线 100% 走表达式，本 skill 处于"备而未用"。可行路径：在 campaign-matrix 的意图解析里加 "python_alpha" 意图分支；或明确宣布搁置（避免维护负担）——二选一，不要悬置。
4. **优化点**：引用了 `mcp__wqb-mcp__*` 前缀（**与本仓 MCP 名 `wq-brain-http` 不一致**——是旧名残留，调用即失败）；`rtk python3` 的 rtk 是外部工具，未在运行环境节说明。

#### 14. brain-alpha-repair 【C（薄指针）】
1. **定位**：2026-08-23 单源化后只剩"不适合通用工作流的补充实证"：failed-count 判据、GLB emotion 全灭实证（§2d）、fingerprint 纪律。
2. **集成**：作为触发词触发的入口，正文全部指向 optimization-v1。设计正确（消灭第二实现）。
3. 不适用。
4. **优化点**：§2d 的 GLB 实证与 optimization-v1/亲和矩阵三处重复出现同一结论（换壳>磨参数）——GLB 教训应收敛到**一处**（建议 ledger 跨区铁律 `cross_region_lessons`，其余引用）。

#### 15. brain-datafield-exploration-general 【B】
1. **定位**：单字段 6 评测法（neutral settings 定性）+ EVENT 字段 `ts_event_*` 处理铁律 + dataset.id= 陷阱。
2. **集成**：被 optimization-v1 Step B2、dataset-exploration Phase 4 引用；批量收割明确让位给 scan_fields。
3. 不适用。
4. **优化点**：EVENT 陷阱知识同时存在于本 skill、optimization-v1 陷阱节、gate 闸8 判据三处——本 skill 的"实测说明"（KOR short-interest 即使标 VECTOR 也触发）是独有价值，建议把这段实证上浮到 gate-rules（离闸门最近）。

#### 16. brain-dataset-exploration-general 【B】
1. **定位**：数据集审计五阶段 + 双门槛评分/两段式探针（指向 ppa-mining 权威）+ Region→Universe 映射表（JPN 非 EQUITY 等实测）。
2. **集成**：S0/S1 的手动审计路径；universe 表与 config.REGIONS 单源对齐（实测值一致）。
3. 不适用。
4. **优化点**：Phase 3 的评分公式与 toolkit probe-scoring-v2.md 是**公式两处书写**（0.40*cov+0.30/log10...），应只留引用；universe 表第三列"备注"含时效性数字（192 个数据集），易过期。

### 质量与验证层（S4/S5 闸门）

#### 17. alpha-expression-verifier 【A1】
1. **定位**：纯语法校验（词法/语法/函数签名/括号），1377 行 validator.py 巨石，明确"仅语法、字段归 gate"。
2. **集成**：被 toolkit gate.py 闸1 **直调**（非子进程，`WQ_VALIDATOR_DIR` 探测）；quantile 1-3 参语法事实与闸4 加严的分工写得极清楚。
3. 不适用。
4. **优化点**：① 1377 行巨石自身声明"不要改"，但**签名表与平台演进（新算子）如何同步无机制**——目前靠论坛模板触发人工扩展 grammar；② 与 src/wqb/expression/validator.py（395 行，shape 分类 + check_batch）同名不同物，跨仓引用时极易拿错（建议 src 侧改名 shape_validator 或在两处 docstring 互指）。

#### 18. brain-how-to-pass-alpha-test 【B】
1. **定位**：各 IS 闸门阈值手册（含 sub-universe 平台公式 0.75×sqrt×sharpe、thresholds 对照）。
2. **集成**：S4 链首（失败项定位）→ optimization-v1 强制回流。
3. 不适用。
4. **优化点**：与 INDEX 两线三层、submit-alpha 验证清单三处数字并存（09-12 已对齐标注，但**"阈值手册"本身应成为唯一数字来源、INDEX 引用它**——现在的指向方向反了）。

#### 19. wq-brain-alpha-optimization-v1 【A2】
1. **定位**：改进唯一入口（Mode B 想法层 70%/Mode A 参数层 30%）+ salvage_pool 组合腿救援 + 过拟合四查 + arXiv 概念检索。
2. **集成**：S4 判 FAIL 且达 mode_b_qualification（1.25/0.8）强制回流；repair 的配方收纳方；下游 selfcorr-quick→explain→robustness→verdict 链路完整。
3. 不适用。
4. **优化点**：① Mode B 的"5 步工作流"由 Agent 手动执行，**无节点化**（相比 wave_gate，B1-B5 的 LLM 判断难以代码化——可只把 Step B4 的 8 候选批校验做成节点）；② 模板/算子关联：Step B3 幽灵算子清单引用 operators_notes.md——是"算子白名单"消费方之一，但没写"改前先 get_operators 核对"的研究协议（research §8 有），两处应互链。

#### 20. brain-alpha-robustness 【A2】
1. **定位**：S4→S5 必经闸：WebDataScope failed-count 硬前置（Failed RA==0）、参数敏感性/子宇宙/逐年/概念对照四查、**PPA 提交路径实证**（MCP submit 非 PPA 感知 → web UI）。
2. **集成**：S4→S5 强制；judge 的前置（robustness REJECT 不进 judge）。
3. 不适用。
4. **优化点**：PPA web-UI-only 的关键事实 09-12 已上浮到 submit-alpha，但本 skill 仍是**唯一出处**（:117）——建议把这段整体搬到 submit-alpha 并反向引用，避免"最关键事实住在最不直觉的位置"。

#### 21. brain-calculate-alpha-selfcorr-quick 【A2】
1. **定位**：本地 SELF/PPAC 快算（os_pnl_pool.pkl）。
2. **集成**：S4 链第三步；"本地>0.7 可信判死、本地低≠平台低"的**结构性盲区**（近期提交孪生体不可见，0.229 vs 平台 0.8392 实证）已文档化——这是全仓最诚实的 skill 文档之一。
3. 不适用。
4. **优化点**：盲区缓解（403 探针）写在文档但**没有工具化**（`_quota_now2.py` 是另一套）；可给 scripts/skill.py 加 `--probe-403` 参数把零成本实测纳入同一入口。

#### 22. brain-explain-alphas 【B】
1. **定位**：表达式归因六步（2026-09-01 从必经改按需：换概念前查重叠/战略候选确认）。
2. **集成**：optimization-v1/judge 引用；arxiv_api.py 与 optimization-v1 共用（同脚本两处引用，单一实现 ✓）。
3. 不适用。
4. **优化点**：定位从"必经"改"按需"后，旧文档（optimization-v1 下游链、judge 上游链）的链路图仍把它画在主链上——三处链路图不同步是通用病（建议每 skill 的衔接协议图由 INDEX 单源生成）。

#### 23. brain-alpha-judge 【B（参考层）】
1. **定位**：弃用声明后保留三职能：PPA 主题/相关性人工核对清单、value-factor trend score（diversity_score=S_A×S_P×S_H + 假设投影）、点塔优选排序（A/B/C 档）；内置 20 篇中文论坛语料。
2. **集成**：S5 评审参考（判定权威=submit_verdict.py）；robustness 先/judge 后的顺序硬约束。
3. 不适用。
4. **优化点**：① 弃用声明与 274 行正文并存，**READY/REVIEW/BLOCK 三态语义仍在**——建议把存活的三职能拆成三个小节并删除判定器叙事（现在读者要读到 140 行才知道它已不是判定器）；② PPA 附加闸门的"TVR 5-20%/SELF<0.5"是内部线口径（09-12 ppa-mining 已改两线标注，此处还没跟）；③ 语料 20 篇 + index.json 的更新机制（论坛新帖何时入库）未定义。

### 提交与运维层（S5/S6/横向）

#### 24. worldquant-submit-alpha 【A2】
1. **定位**：真提交 API + 静默丢弃两成因 + 点塔优先规则 + 三通道配额（09-12 已补 PPA 通道节）。
2. **集成**：S5 落地；`workflow_submit_alpha` 节点（confirm_submit 需用户确认）。
3. 不适用。
4. **优化点**：PPA 走 web UI 后，**提交台账的 PPA 类型回写无自动化路径**（人肉提交→人肉回写，ledger PPA=0 的另一半原因）；建议 web UI 提交后用 `submit_verdict.py --alpha-id` 补录的标准动作写进验证清单。

#### 25. wq-brain-superalpha 【A1】
1. **定位**：SUPER 组套（selection/combo 语法实证、SUBINDUSTRY 杠杆、decay 压 SELF 曲线、双闸此消彼长）。
2. **集成**：`workflow_superalpha` 节点；submit_alpha 的 SUPER 分支路由到它。
3. 不适用。
4. **优化点**：内容质量高但全部是 USA/KOR/MEA 实证，**缺 EUR/IND 的区域化差异**（组件池 18 颗的 IND 从未组过 SA）；decay 曲线表只有 KOR 一组，换区需重测——建议把"decay 扫描"做成 budget_planner 的标准前置步。

#### 26. wq-backtest-monitor 【A2】
1. **定位**：S6 监控框架（四关审计/ETA/判停/§14 回写闭环 + verdict 必填硬约束 + methodology_rules 计数回写）。
2. **集成**：S6 强制章节；§14.2 命令模板闭环到 campaign-matrix。
3. 不适用。
4. **优化点**：① §7 的 universe 合法性清单（TOP800/1500/2500/5000 非法）与 config.REGIONS 重复——已被 09-12 的计数基准段模式证明可收敛；② §10-12 大量脚本实例名（v52b/tri_track/ds 舰队）是**历史战役快照**，时效性强，建议移 `references/history/` 并在正文留判据。

#### 27. wqb-concurrency 【B】
1. **定位**：横向并发纪律（Token-Bucket C≈7、七槽填槽 SOP、孤儿模拟防治）。
2. **集成**：S3 的并发唯一权威；台账口径 09-12 已改 DB 单轨。
3. 不适用。
4. **优化点**：§8 与 sim-alphas/ra-pipeline 步 6 的重叠已收敛大半，剩"7 批×8 条"数字在两处（建议与计数基准段同法收敛）。

#### 28. brain-next-move-analysis 【C】
1. **定位**：L0 并行日报 + §5.5 区域饱和度检测（PROD 饱和/campaign exhaustion/开战役候选三表 + entry_verdict 联动）。
2. **集成**：非流水线前置（INDEX 明确）；ra-pipeline 循环表"连续 3 波全 FAIL → 转 next-move"是它唯一挂接点。
3. **潜在价值**：§5.5 与 campaign-matrix 的 prod_saturation 标注、与我在挖掘优化方案里提的"数据集记分板"三者是**同一个需求的三个原型**——收敛为 `tools/dataset_scoreboard.py` 后，日报 §5.5 直接消费，即可升级为 C→B。
4. **优化点**：工具名笔误 `value_factor_trendScore`（应为 `value_factor_trend`）；MEA frozen 判定硬编码在文档（"MEA 为 frozen"），应读 profile entry_verdict。

#### 29. brain-forum-browse 【C】
1. **定位**：论坛 stroll 协议（explore/contribute 两模式、贡献义务决策树、写工具缺失自动降级只读）。
2. **集成**：独立触发词触发；与挖掘链的唯一交点是 research §7（论坛模板挖掘协议）——但两者互不引用（browse 的 stroll 产出可以直接喂 research 的 PARADIGMS 分类，当前靠会话巧合）。
3. **潜在价值**：作为 `KB/community_tpl_kb`（现 59KB/ledger）的**供给管道**正式化：stroll 发现的高赞模板 → research §7 分类 → KB 入库 → GEM 消费，这条链值得在 browse 文档里显式写一步"模板候选移交"。
4. **优化点**：241 行协议密度极高（auto-send E1/Run Contract/curator），但**写工具不存在的现实**（wq-brain-http 只读）使 60% 的写路径长期 dormant——建议把"只读降级"分支提为主路径文档结构。

### 元技能（非挖掘专用，简评）

#### 30-31. planning-with-files / pull-brain-skills 【元】
规划文件化与 skill 导入工具，与挖掘链无直接耦合；pull-brain-skills 的 `--dest` 已对齐仓库真相源。无需改动。INDEX 分层 L7 正确。

---

## 第二部分 · 模板（Template）专题横切

**全仓共 6 套模板系统 + 1 个用户级增强 skill，按数据流排列：**

| # | 系统 | 载体 | 生产者→消费者 | 状态 |
|---|---|---|---|---|
| T1 | **mechanism families**（8 族） | `toolkit/config/template_families.json`（19KB：family_id/mechanism/economic_theme/**skeleton 表达式串**/placeholders/field_profile_match/**forbidden_operators**） | toolkit → gem run_pipeline（经 skill_roots 探测加载） | ✅ 主力 |
| T2 | **skeleton 骨架库**（代码态） | `gem/trailSomeAlphas/skeletons.py`（field layering→WINDOW_DOMAINS→骨架组装，LLM 只出结构化 JSON，"语法合法性构造保证"） | gem skeleton mode | ✅ 已落地（P0） |
| T3 | **社区模板 KB** | ledger 键 `KB/community_tpl_kb`（**59KB 实存**：category/placeholder_conventions/ghost_operator_advisory）+ `KB/template_kb`（validated/failed） | 论坛→research §7 分类→KB→GEM | ⚠️ 有库无消费闭环 |
| T4 | **`{后缀}` format 模板** | feature-implementation `implement_idea.py`（`{gro}/{pe}` 后缀匹配，正本）+ **gem 内嵌副本（已分叉！）** | idea md → 表达式 | ⚠️ 双份分叉 |
| T5 | **范式与形状** | `config.PARADIGMS`（P1-P13）+ `config.SHAPE_CLASSES`（S0-S9；`validator.classify_shape`） | research 分类 → toolkit check_batch 判重 | ✅ 治理层 |
| T6 | **Mode B 变换引擎** | `src/wqb/modeb/`（operator_catalog 1281 行/transform_engine/variant_generator，并行工作流） | optimization-v1 Mode B | 🚧 开发中 |

**问题与冗余（按危害排序）：**
1. **T4 分叉是唯一实锤事故隐患**：gem 内嵌副本的 `implement_idea.py` 与正本 md5 不一致——"禁止第二实现"纪律在 vendored 场景失效。修法：gem 改为 import 正本（skill_roots 探测 `brain-feature-implementation/scripts`），删除内嵌副本（或 CI 校验 md5 相同）。
2. **T3 有库无消费**：59KB 社区模板躺在 ledger，但 GEM 的族选择只读 T1，没有任何代码从 `community_tpl_kb` 取模板进波。修法：build_wave 加 `--from-kb` 数据源（按 category/ghost advisory 过滤），让论坛沉淀真正回流生成端。
3. **T1 与 T2 的关系未文档化**：family skeleton（静态表达式串）与 code skeleton（动态组装）何时用哪个、是否允许混用，SKILL.md 未写——这是 GEM 内部的"两种生成哲学"并存，需要一段定位声明。
4. **T5 是治理资产但可见度低**：PARADIGMS/SHAPE_CLASSES 决定模板入库合法性，却只有 research §7-9 提及。
5. **模板生命周期断点**：distill_experience 有"模板晋升"（G1），但晋升目标（KB/template_kb? template_families?）没有写明——三套终点含糊。

---

## 第三部分 · 算子（Operator）专题横切

**全仓 7 处算子知识载体：**

| # | 载体 | 内容 | 角色 |
|---|---|---|---|
| O1 | `toolkit/config/platform_constraints.json` | known_ops **107** / inaccessible **2**（ts_min,ts_max）/ quantile_arity 1 / vector_only 8 | 平台级约束**单一事实源**（自述） |
| O2 | `toolkit/config/operator_semantics.json` | **103** 算子语义 + 12 roles（price/volume/...） | GEM 概念绑定/语义多样性 |
| O3 | `alpha-expression-verifier/scripts/validator.py`（1377 行） | 完整签名表（quantile 1-3 参=语法事实） | 语法校验引擎 |
| O4 | `src/wqb/expression/`（grammar._OP_ARITY + op_arity.py 532 行 + _op_signatures.py） | 语法生成器算子域 | 表达式构造 |
| O5 | `docs/reference/operators_notes.md` | **17 幽灵算子清单** + 替换表 + 扩展白名单 | 负清单权威 |
| O6 | ledger `KB/community_tpl_kb.ghost_operator_advisory` | 随模板条目的幽灵警告 | 模板级过滤 |
| O7 | `src/wqb/modeb/operator_catalog.py`（1281 行） | Mode B 变换目录 | 并行工作流 |

**实测漂移（对账结果）：**
1. **O1 vs O2：6 处不一致**——semantics 多 `vector_neut`；known_ops 多 `delay/delta/exp/range/vec_norm`（5 个）。两份"算子宪法"互不同步，闸5（毒模式/known_ops）与 GEM 语义绑定对同一算子可能得出不同存在性判断。
2. **O5 的 17 幽灵算子是负清单权威，但 O1/O2/O3 都不含幽灵标记**——即 verifier 会放行幽灵算子语法（语法合法），gate 闸4 只拦 ts_min/ts_max 两个，**其余 15 个幽灵算子靠 gem 查 KB advisory 自觉规避**；漏查=整批静默失败（血泪教训已写进 gem 铁律 5）。
3. **O3 与 O4 是两套签名系统**（verifier 语法事实 vs grammar 生成域），quantile 的"1-3 参合法/战役仅 1 参"分工已文档化——这是全仓算子分工写得最好的一处，可作为其余收敛的样板。
4. **O7（modeb）自成一体**：1281 行目录与 O1/O2 无 import 关系（并行工作流开发中），落地时若不同步 known_ops 会再造一张漂移表。

**算子收敛建议（一处权威 + 派生视图）**：以 O1（platform_constraints）为存在性/约束权威，O2 保留语义但**加 schema 测试断言 `operators ⊆ known_ops`**（当前会红：vector_neut）；O5 幽灵清单并入 O1（`ghost_ops` 数组 + 替换表），verifier/gem/KB 全部引用同一来源；O7 落地前先过 O1 对账。

---

## 第四部分 · 整体汇总与优化优先级

### 汇总矩阵（集成度 × 数量）

| 集成度 | 数量 | 名单 |
|---|---|---|
| A1 代码内嵌 | 7 | ra-pipeline、toolkit、gem、sim-alphas、verifier、superalpha、data-feature-engineering |
| A2 SOP 内嵌 | 8 | campaign-matrix、ppa-mining、inspect-raw(降B倾向)、optimization-v1、robustness、selfcorr-quick、submit-alpha、backtest-monitor |
| B 链上引用 | 10 | datafield/dataset-exploration、research、field-quality、news-sentiment、how-to-pass、explain-alphas、judge、concurrency、repair(薄) |
| C 独立/外围 | 5 | **hypothesis-first（高潜）**、template-labs、next-move、forum-browse、feature-impl入口限制 |
| 元 | 2 | planning-with-files、pull-brain-skills |

**结构性结论**：九步主干（A1/A2 共 15 个）成熟且经 09-11/09-12 两轮治理后事实错误清零；真正的价值洼地在 **C 级三个 skill**（hypothesis-first 直接对准存量饱和瓶颈、next-move §5.5 与记分板需求重合、template-labs 是唯一 Python 赛道）以及**模板/算子两横切面的收敛**。

### 优化优先级

**P0（防事故，1-2 天）**
1. **消除 T4 分叉**：gem 内嵌 feature-implementation 副本改引用正本或删副本（+md5 测试锁）。
2. **算子表对账**：semantics↔known_ops 6 处漂移修复 + `test_operator_configs_consistent` 断言（operators ⊆ known_ops）；幽灵清单并入 platform_constraints.json。
3. next-move 工具名笔误修复（value_factor_trendScore）+ template-labs 的 `mcp__wqb-mcp__*` 旧前缀修复（当前调用必失败）。

**P1（价值释放，1 周）**
4. **hypothesis-first 挂接**：ra-pipeline 步 2 加路由条件（dataset≥1 万 alpha 或 2 波模板全灭）+ 假设目录入 ledger + `run_hypothesis_round` 节点化——对准"存量饱和、出量靠新方向"的第一瓶颈。
5. **KB 模板消费闭环**：build_wave `--from-kb`（59KB 社区模板回流生成端）；distill 晋升终点写明。
6. **区域状态单源**：next-move §5.5 / campaign-matrix prod_saturation / 数据集记分板三者收敛为一个 DB 驱动工具，日报与 S-PRE 都消费它。
7. field-quality 区域切换门禁机器化（天花板闸模式：切换区域且无预筛记录 → S0 拒绝开波）。

**P2（卫生与文档，随例行）**
8. judge 瘦身（弃用叙事下沉，三职能前置）；robustness 的 PPA 路径段上移 submit-alpha；GLB 教训收敛 cross_region_lessons。
9. 两套 validator 命名区分（src 侧 shape_validator）；backtest-monitor 历史战役快照移 references/history/。
10. dfe 8 问 / GEM 8 概念位 / hypothesis 12 类三套概念分类学写一张映射表；S1 报告模板中的时效性数字标注快照日期。
11. 模板定位声明（T1 family vs T2 skeleton 的适用条件）补进 gem SKILL.md。

---
*核算脚本输出与本报告差异均可复现：config JSON 结构、ledger `KB/*` 大小、md5 对比、semantics↔known_ops 差集均为 2026-09-12 实测。*

---

## 附 · 落地记录（2026-09-12 02:15，三阶段全部完成）

**验收：`pytest tests/ -q` = 771 passed（较基线 +44）；dry-run 断言 35/35 PASS；`sync_skills.py --check` 4/4 一致。**

| Phase | 落地 | 关键产出 |
|---|---|---|
| **P0** | ① T4 分叉消除：先三方甄别确认**副本是功能超集**（implement_idea 含 P1a 语义 lint 等），以 gem 运行版回灌正本 4 文件（6 文件 md5 全等 + 编译通过）+ `test_feature_impl_vendored_matches_canonical` parity 锁；② 算子对账（真相链实证：`operators_verified.verified(103)` 是真值，semantics 与其全等，known_ops 107 为旧快照多 5 少 1）→ known_ops:=verified + 5 个残留名记录在案；幽灵清单真身 = ledger `KB/community_tpl_kb.ghost_operator_advisory`（10 ghost+unverified+forbidden），并入 `platform_constraints.ghost_ops` + `test_operator_configs_consistent`；③ 四处陈旧指针/笔误：template-labs `mcp__wqb-mcp__`→`wq-brain-http`（4 处）、operators_notes 定性头注（它**不是**幽灵清单——research §8/repair 的旧指针全部改写）、research §8 指针、repair 幽灵指针。**next-move 的 `value_factor_trendScore` 注册校验测试拦下了我的"改正"——真名含大写 S，已回滚并留勿改注** | 10 断言 PASS |
| **P1** | ④ hypothesis-first 挂接：新增第 9 个 workflow 节点 `hypothesis_round`（dry-run 契约 + `_context.dry_run` 约定 + 4 测试），registry/INDEX/tools_workflow/skill_call_chain/ppa-mining 八处计数面同步 8→9；ra-pipeline 步 2 新增饱和路由（alphaCount≥1 万或 2 波全灭→强制切换）；hypothesis-first SKILL §3 修复 YAML/字段名与 `load_catalog` 的 schema 漂移；⑤ `tools/kb_templates.py`（141 个 KB 模板检索/ghost 过滤/`--emit-ideas` 导出供 GEM 消费）+ research §7 闭环说明；⑥ `tools/region_status.py` 区域状态记分板（冒烟输出与实证吻合：IND 36%/EUR exhausted 100%）+ next-move/campaign-matrix 双指向单源；⑦ `tools/prescreen_gate.py` 区域切换机器门禁（查门/登记，exit 0/1）+ field-quality 说明（节点内嵌接线待并行 campaign.py 落定） | 12 断言 PASS |
| **P2** | ⑧ judge 三职能前置 + PPA 内部线两线标注；robustness PPA 段上移 submit-alpha 单源；repair §2d 定为 GLB 教训唯一完整版 + ppa-mining 交叉引用；⑨ 双 validator 命名辨析互指（选择文档方案而非改名——并行脏树下零风险）；monitor 历史快照标注；⑩ `concept-taxonomy-map.md`（8问↔概念位↔12类）+ dfe/hyp 两处链接；dataset-exploration universe 表快照标注；⑪ gem「两种生成模式定位」声明（family vs skeleton 触发与产出方） | 13 断言 PASS |

**过程中的两个教训（已进守护）**：① 我对 `value_factor_trendScore` 的"修正"是错的——注册校验测试当场拦下，教训：改工具名前先 grep 注册表（已留勿改注）；② 新链接首跑被相对链接测试拦下（`../../` 少一级）——两道防线都在第一次犯错时就地拦截，验证了"审计结论固化为断言"路线的价值。

**未做/顺延**：`--from-kb` 未接入 build_wave（KB 模板的正确消费位是 GEM ideas 通道而非选波——以 `kb_templates.py --emit-ideas` 替代）；prescreen 门禁的节点内嵌接线待 `nodes/campaign.py` 并行改动落定；假设台账 DB 化待后续。

**待确认**：本轮改动（1 新节点 + 3 新工具 + 1 新 reference + ~20 处文档/测试/config）未提交，与并行脏树共存，按 §7 纪律可显式路径切分提交。
