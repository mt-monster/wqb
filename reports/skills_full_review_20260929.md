# WQ/BRAIN Skills 全量文档质量审查报告

> 审查日期：2026-09-29 · 范围：`Claude/skills/` 全部 34 个 skill · 方法：4 维度逐段评估 + 5 组并行精审 + 核心编排层主审
> 结论先行：**共发现约 163 个实质问题点**，集中在「自称闸/硬门但实为文档约定（靠 Agent 记得）」「跨 skill 口径漂移」「正文与自身定位声明矛盾」三大类。

---

## 0. 审查方法（4 维度）

对每个 skill 的每一段（按 `##`/`###` 阶段划分）评估：

| 维度 | 判据 |
|---|---|
| **书写逻辑** | 段落结构清晰？前后矛盾？冗余？关键信息缺失？ |
| **职责划分** | 做什么/不做什么明确？上下游衔接清晰？ |
| **边界界定** | 与其他 skill 重叠/空白？触发条件可判定？ |
| **情景化需求** | 有无"必做/记得/按需/优先"等模糊表述，易被绕过或遗漏？需用何种具体场景/判据规范？ |

---

## 1. 审查总览

| 层 | skill 数 | 问题点 | 主要病灶 |
|---|---|---|---|
| L-RA 编排 | 1（ra-pipeline） | ~7 | 编排层塞入方法论细节、铁律散落、双编号体系 |
| L-TOOL 引擎 | 1（campaign-toolkit） | ~4 | description 口径冲突、灰度闸双入口行为不一致 |
| L-PRE 查表 | 1（campaign-matrix） | ~4 | 中性化默认值与 config 口径需标注、饱和"同质"无量化 |
| L0 情报 | 4 | 30 | 无完成判据/失败降级、写工具未实现却写"必贡献" |
| L1 数据 | 7 | 27 | 死链、路由靠关键词无判定序、字段 source 语义打架 |
| L2–L3 生成/仿真 | 6 | 24 | 自相矛盾（独立入口 vs 被内嵌）、并发数字 C 6/7 冲突 |
| L4 诊断优化 | 6 | 29 | "必经闸"被 force/声明架空、改进建议被自身证伪 |
| L5–L7 提交/复盘/元 | 7 | 38 | 判定权移交后残留判定语义、GET /submit 结论三处打架 |
| **合计** | **33** | **~163** | — |

---

## 2. 跨 skill 共性病灶（最高优先级，一改治一片）

### 病灶 A：文档级"闸/硬门"名不副实（靠 Agent 记得，非代码强制）
- `brain-alpha-robustness` 自称「S4→S5 必经闸」，但 `robustness_audited` 是自我声明、`force=True` 可绕过、Phase B/C 无法自动 → 已被本次 P0 部分焊进提交路由，但**仍须在文档标注"默认强制、force 留痕可绕过"**，勿再自称绝对"必经"。
- `wq-brain-ra-pipeline` 步 5b「prod-first 探针（升为硬门）」——"硬门"但靠 Agent 记得跑 `campaign_intel prod-first`，无代码强制。
- `brain-alpha-research-field-quality` 第 3 步自称「机器门禁」，正文自注"节点内嵌接线待落地"，实为软门禁。
- `brain-alpha-research-news-sentiment` 的"硬闸"（禁止 3 字段同家族）无任何机器判据。
- **改进通则**：凡文档写"闸/硬门/必经"，必须标注其实现形态（代码 fail-closed / CLI 工具需主动调 / 纯文档约定），否则一律视为"约定"。

### 病灶 B：跨 skill 同一事实多份表述、口径漂移
- **体检工具三权威**：ppa-mining §1.0 用 `dataset_health_check.py`，next-move 说 `score_datasets.py` 权威，campaign-matrix §2 又说 `score_datasets.py` 执行 → 需一张"体检工具分工表"。
- **GET /submit 结论三处打架**：judge 说"200=成功/403=被拒/404=清除"，worldquant-submit-alpha 说"恒 404 勿用于判定"，superalpha 说"200 假阳性" → 统一为"提交层信息只存在于 POST 响应"。
- **robustness 下游链**：selfcorr-quick 写"→ robustness（见 optimization-v1）→ judge"，与 optimization-v1/robustness 的"robustness 必经 → submit_verdict → judge（可选）"不一致。
- **提交探测协议三处重复**：selfcorr-quick 盲区、robustness Phase E、repair §2d 各一份 → 单源到一处。
- **并发 C 值**：wqb-concurrency 第 1 节"≤6"、第 8 节"C≈7"、例子仍用 C=5 → 统一。

### 病灶 C：正文与自身定位声明矛盾（Agent 读了会做错事）
- `brain-feature-implementation`：定位"被 gem 内嵌、非主链入口"，正文却是完整独立五步流程。
- `brain-alpha-repair`：定位"只作配方参考不执行"，工作流通篇"改公式…结构修复…"祈使句。
- `wq-brain-ppa-mining`：职责"不作编排器"，§7 给 0–8 步完整编排 + 步 8 提交。
- `brain-alpha-judge`：判定权已移交 submit_verdict，但 description/职责表/LLM 层/闸门顺序残留"判定/提交"语义。
- `brain-inspect-raw-template-create-setting`：顶部"人工设置决策已删除" vs 运行步骤"手动选定设置"。
- `brain-data-feature-engineering`：头部"ideas 不再被 GEM 当输入" vs 第 5 步"本 ideas 是 S2 法定输入"。

### 病灶 D：模糊判据（易被绕过）
"战略级/近闸"（explain-alphas）、"异常稳定/不拥挤"（labs）、"风格同质/集中"（matrix+next-move）、"满意效果/一种结构"（backtest-monitor）、"确实需要/已获批准"（labs）——均无量化口径，Agent 无法稳定执行。

---

## 3. 核心编排层精审（主审）

### wq-brain-ra-pipeline（1000 行，L-RA 编排）
总体：九步骨架完整、决策密集，但**编排层被方法论细节撑爆**，与"只做编排"定位冲突。

- **[description]** 触发词含"选数据集/中性化/窗口"，与正文"本 skill 只做编排、不产表达式/不选字段"张力 → description 收敛为"编排/开战役/日循环"类，删除"选数据集/中性化"等下游动作词。
- **[步 4/步 7 方法论堆叠]** 步 4 塞"形状配额+形状源分工"、步 7 塞"四道提交闸+SUB 比例律"、步 8 塞"robustness 判死"——这些是 optimization-v1/how-to-pass/robustness 的权威内容，编排层重复维护会成第二份权威并漂移 → 方法论下沉到对应 skill，本 skill 只留"何时调、调到哪一节"。
- **[九步 vs S0–S6 双编号]** "步 1（S-PRE）…步 9（S6）"两套编号并行，campaign-matrix §3 引用时从"步 2 S0"起跳 → 明确"步 N 是唯一编号，S 阶段是映射标签"，并在 INDEX 固定映射表。
- **[铁律散落]** "禁止 add(A,B) 混信号"在步 4、"等权豁免漏洞"在步 5 闸、prod-first 在步 5b——无统一"铁律汇总"节，Agent 漏看即踩雷 → 顶部加"铁律速查"锚点，散落处引用之。
- **[步 5b 硬门无强制]** prod-first"升为硬门"但靠 Agent 记得跑 `campaign_intel prod-first`，与 P0 刚焊进提交路由的 submit_gate 形成对比 → 评估是否把 prod-first 也接入 wave_gate/batch_track 前置（P1 候选）。
- **[步 8 提交判定]** 段内同时出现 submit_verdict 预检、robustness 必经、用户确认——三层口径，且 P0 后 submit_gate+robustness_audited 已落代码，此处文档须同步引用，勿再写"robustness 必经"软表述。
- **[日循环/一键战役与九步]** 947/955 行的日循环、PPA 日循环停止闸与正文九步的关系散落在文件尾部，未前置到"编排总览" → 收敛为"运行模式"节（九步 / 日循环 / 一键战役 / PPA 分支）统一入口。

### wq-brain-campaign-toolkit（363 行，L-TOOL 引擎）
总体：引擎契约最扎实、工具使用率分级是好实践，但 description 口径与灰度闸行为不一致。

- **[description 闸数冲突]** description 写"8 闸预检"但列举"闸1–5"，INDEX 明确"5 闸=闸1–5、7 闸=闸1–7" → 与 INDEX 统一，勿在 description 出现第三种口径。
- **[开波区域闸双入口不一致]** §4 第 7 条：CLI `--gate-mode` 走 warn（灰度到 2026-10-12），但"workflow 节点（campaign S2/S3、batch_track）不看这个模式，一律拦截"——同一闸 CLI 与 workflow 行为分叉，且硬编码 `WARN_SUNSET=2026-10-12` 过期后语义漂移 → 明确"CLI 与 workflow 最终口径一致（enforce）"，灰度期是临时豁免并注明到期自动失效。
- **[description 过长]** 400+ 字功能清单与触发词混杂 → 触发词与功能分列，功能清单移到正文"子命令一览"。
- **[学习闭环残留]** 已归档 6 工具注释"学习闭环（G1/G2/G3）仅存在于文档叙述"，但正文多处仍残留"经验蒸馏 G1 学习闭环"表述 → 清理残留叙事，或明确"G 闭环未落地"的事实标注。

### wq-brain-campaign-matrix（143 行，L-PRE 查表）
总体：查表/回写闭环清晰。**勘误（2026-09-29 复核）**：§2 配置包示例 `region=KOR universe=TOP600` 是**正确的**——`config.py` 权威定义 KOR `universes=["TOP600"]`（KOR 是独立区域，与 USA 的 TOP500/1000/2000/3000 档位无关），非硬伤。

- **[§2 中性化默认值]** 示例写 `neutralization=STATISTICAL`，但 `config.py` 注「KOR campaigns start from SECTOR」、`tracking/KOR/config/settings.json` 又是 STATISTICAL——三处对 KOR 默认中性化口径不一 → 标注"KOR 默认中性化以 config.py `KOR.neutralizations` 为准（SECTOR 优先），settings.json 是当前战役实例值，二者可能不同"。
- **[§38 饱和"风格同质"无量化]** `search_alphas_by_sharpe ≥10 且风格同质 → likely`——"同质"无口径（同族几个算同质？占比多少？）→ 给出可算判据（如同一数据集/算子家族占比 ≥60%），或统一引用 `region_status.py` 的既有口径。
- **[§3 派发步编号起跳]** 从"步 2 S0 体检"起（步 1 S-PRE 即本 skill 自身），但未显式说明，读者易与 ra-pipeline 九步错位 → 标注"步 2–9 对应 ra-pipeline 九步，步 1 即本查表层"。
- **[§5 扩区 `fresh_datasets_7region.json`]** 文件名"7region"与 14 区域矛盾、路径未验证 → 核对文件是否仍存在并改名/删引用。
- **[体检工具归属]** §2 说 `score_datasets.py` 执行体检，与 ppa-mining §1.0 的 `dataset_health_check.py`、next-move 的"score_datasets 权威"三者不一 → 与病灶 B 统一。

---

## 4. L0 情报层（30 问题点）

### brain-next-move-analysis
总体：日报清单齐全但"检查"类步骤无完成判据与失败降级，且与 ppa-mining 体检工具口径不一致。
- [§0 执行摘要] 段名"执行摘要"却放全文最前、正文只一句"总结下述…"——摘要应是分析后产物，位置与语义矛盾，且未定义必含字段 → 改"摘要（分析后回填）"并给 3 项必含字段。
- [§4 研究与建议] "下一步行动"无判定规则（何时换数据集/开战役/停手），全篇最易被跳过的空壳 → 给 3–4 个可判定分支并引用 §5.5 饱和度作输入。
- [§1/2/3/5 检查段] 只写"查什么"未写"查到什么算完成、查不到怎么办"，仅 §5.5 有降级 → 统一补"空结果标注不可用并继续"的通用降级规则。
- [§5.5 定位] "可选并行情报层"与日报主流程定位冲突，且"脚本 vs 手动"两套口径并存未定主次 → 明确脚本为准、手动仅排查。
- [§5.5 判据] "风格同质/集中"无量化 → 给可算口径（同数据集/算子家族占比 ≥60%）。
- [职责边界·上游] "DB"指代不清，未列实际用到的 DB 工具名 → 显式列出。
- [定位声明] 与 ppa-mining 体检工具名冲突 → 与病灶 B 统一。

### brain-forum-browse
总体：核心"每轮必贡献写操作"硬规则与"写工具未实现"现实矛盾，整套贡献/合同体系实际永远走豁免。
- [硬性规则 vs MCP 只读] "必贡献写操作"与"wq-brain-http 只实现只读工具"直接矛盾 → 写贡献降级为"有写工具时必做"，只读环境产出（本地 notes 草稿）定义为默认可交付物。
- [决策树] 第一层"是否提供写工具？是→必贡献"恒为"否"，整棵树形同虚设 → 重构为"只读环境产出什么"主路径。
- [recon 职责膨胀] recon（经 forum_recon.py）与论坛贡献无关，且触发词不在 description → 拆分或补触发词。
- [hybrid 冗余] "hybrid（弃用别名）"两处重复声明，explore/contribute 边界"更严格"未量化 → 删 hybrid、用差异对比表量化。
- [HTML 转换死代码] 写工具未实现时 md_to_forum_html 等是无触发条件死代码 → 标注"写工具启用后待激活"。
- [Run Contract 例外] "恰好 1 次/零推断"高度主观 → 加机械判据（字数上限/无 sim 数值/命中 E1 模板）。
- [禁止菜单 vs 后续灵感] 边界模糊，Agent 可把选项包装成"灵感"绕过 → 用形态判据区分（菜单=向用户提问，灵感=仅落盘 notes）。
- [curator 未实现] 点赞依赖未实现的 upvote_forum_comment 却写入硬规则 → 只读环境降级为"标注值得点赞的帖子 ID"。

### wq-brain-ppa-mining
总体：方法论密度高，但三硬门槛数值自相矛盾、"不作编排器"与 §7 冲突、体检工具名跨 skill 不一致。
- [§1.0 三硬门槛] 0.85/50/10 与"一票否决 0.7/1000"两套阈值，中间灰色地带无动作 → 统一阈值体系并定义中间区间动作。
- [§1.0 vs next-move] 体检工具三权威（dataset_health_check/score_datasets/ra-pipeline 步2）→ 出"体检工具分工表"。
- [职责边界 vs §7] "不作编排器"与 §7 全流程+步8 提交自相矛盾 → §7 标注"仅供 ra-pipeline 消费的方法论参考"，删步 8 提交。
- [衔接协议·输出白名单] 主语模糊（本 skill 还是 ra-pipeline 产出？用哪个工具？）→ 用"谁执行/谁回写/读哪个键"改写。
- [§1.0 vs §1.0.x 排序] 两套排序体系（倍率排序 vs 红黄绿灯）未说明先后 → 明确组合顺序。
- [§1.3 ★★★] "不参与可用性判断"却置于决策三节并列，定位混乱 → 降级为快照完备性备注。
- [§4 payload] 标准请求体硬编码 SUBINDUSTRY，与"不硬编码、按 dominant method"冲突 → 加醒目警告。
- [§6 闸门数值] 硬编码数值无 INDEX 回查路径 → 补引用。

### alpha-template-labs-data-analysis
总体：边界最松散，产物契约、跨 skill 衔接、多个"必做/可选"判据缺失。
- [职责 vs 硬规则] "不选最终字段"与"推荐至多两个字段"张力 → 精确区分候选方向 vs 最终拍板。
- [三套步骤清单] 8 步主流程/硬规则/CLI 专用重叠不一致 → 合并为"主流程+增强+兜底"并标注触发条件。
- [第 2 步"确实需要/已获批准"] 无判据与批准方 → 给机械判据与明确入口。
- [第 7 步产物 JSON] 未定义 schema → 定义最小 schema 并写明 S1 读取方式。
- [论坛材料] 无论坛工具却写"禁止照抄论坛公式" → 注明来源 skill。
- [WebDataScope 交叉验证] 工具路径/执行方/失败动作不明确 → 写明。
- [默认示例"异常稳定/不拥挤"] 无量化 → 给可算口径。

---

## 5. L1 数据层（27 问题点）

### brain-dataset-exploration-general
- [职责 vs 快照表] 声明"不得自行维护区域表"却硬编码 Region→Universe 快照 → 删快照，只留实时复核路径。
- [Phase 3 空转] 标题"战役级评分"却转发 ppa-mining/toolkit → 明确本 skill 只做数据集级定性。
- [Phase 4/5] "关键字段"无判据、头脑风暴踩入 feature-engineering 职责 → 界定。
- [JPN 行] "非有效 EQUITY 区域→返回 0"未标时效 → 标快照日期。

### brain-datafield-exploration-general
- [标题 6 vs 7] "6 种方法"却有"7. 批量收割" → 第 7 段独立成节。
- [EVENT 陷阱位置] 致命陷阱埋在批量收割小节 → 上提到全局前置。
- [type 标记不可靠] "先确认 type"与实际"VECTOR 也误报"矛盾 → type 仅供参考，单字段诊断设为强制前置。

### brain-data-feature-engineering
- [头部 vs 第 5 步] "ideas 不再被 GEM 当输入"与"本 ideas 是 S2 法定输入"直接矛盾 → 下沉改写正文。
- [source 字段三处打架] manual/standalone/s2_nested 语义不一 → 收敛单一契约。
- [第 0 步分档] "覆盖率≥80%/均值>5词"无数据来源与口径 → 指定查询来源。
- [输入要求 vs 核心原则] "必填参数"与"无需用户输入"矛盾 → 明确最小输入契约。

### brain-alpha-research（总入口）
- [专项路由] 纯关键词、无强制判定序，交叉任务路由冲突 → 给判定顺序。
- [工作流 1-13] 全是带日期戳历史沉淀、无顺序 → 拆主链路+陷阱库附录。
- [第 12 条] 既有裁定"以 config 为准"仍保留相反实证 → 移出正文。
- [验证清单] "确认 §10-13 被读取"是元动作无法判定 → 改为可验证项。

### brain-alpha-research-field-quality
- [第 3 步"机器门禁"] 实为软门禁（接线未落地）→ 标注"接线完成前为软门禁"。
- [第 2 vs 第 3 步] 本质同一动作、命令参数不一致 → 合并。
- [不覆盖区域闭环] 不覆盖区域若不登记 prescreen 键会永远 BLOCK → 补特殊状态登记。

### brain-alpha-research-hypothesis-first
- [触发条件三处不一致] 职责边界/触发场景/引擎衔接三套集合 → 统一。
- [假设目录起点] "假设从哪来""假设生成器是谁"未定义 → 补产出者。
- [台账路径分叉] data/hypothesis_ledger vs tracking/hypotheses/ledger 不一致 → 统一。

### brain-alpha-research-news-sentiment
- [reference 死链] 4 个核心 reference 文件全部死链，skill 沦为空壳 → 补齐或内联。
- [硬闸无判据] "禁止 3 字段同家族"无机器判据 → 标注文档约定或接 gate。
- [验证清单阈值] 阈值只在验证清单、正文未定义 → 写入正文。
- [news12 重映射] peer_context 无对应未说明 → 补说明。

---

## 6. L2–L3 生成/仿真层（24 问题点）

### brain-make-some-gem
- [priors fail-closed vs stale WARN] "无快照报错"但 stale 只 WARN，Agent 易拿过期先验 → stale 给可判定阈值（落后 N 天即阻断）。
- [Expected Exposure 验证归属] "回测后核对"但本 skill 不回测 → 明确验证落在 S4。
- [标准调用 vs 直接命令] 命令细节堆主文档 → 下沉 reference.md。
- [与 FI 边界] 只 gem 侧声明、FI 侧未收敛 → 双向统一。

### brain-feature-implementation
- [职责 vs 操作步骤] 定位"非主链入口"却写完整独立流程+产物报告 → 收敛为实现细节。
- [占位符唯一性] "只绑定一次"无消解规则 → 给后缀歧义消解规则。
- [输出验证] "验证输出"无判据且与前文矛盾 → 给最小判据。
- [元数据缺失软动作] 只"向用户澄清" → 阻断并列必需字段清单；语法校验指向 gate。

### alpha-expression-verifier
- [运行环境 vs 示例] 铁律"$WQ_PY"但示例写 `python scripts/...` → 示例统一为 `$WQ_PY "$WQ_VALIDATOR_DIR/verify_expr.py"`。
- [非法示例不非法] `rank(close,5)` 注释自认合法 → 换真正非法反例。
- [densify 段越界] 混入平台类型判定（本 skill 明言不做）→ 删或并入边界说明。
- [禁令无情景] "不要改 validator.py"无理由 → 补触发情景与正确上报路径。

### brain-inspect-raw-template-create-setting
- [人工设置矛盾] 顶部"已删除" vs 运行步骤"手动选定" → 删手动环节。
- [职能描述不一致] "两个职能" vs "产出设置计划" vs settings_candidates 名实冲突 → 统一。
- [入库前无校验] build_alpha_list 直写 DB 无语法/字段校验衔接 → 明确 gate 闸1-4 前置。

### brain-sim-alphas-in-batch-and-track
- [真相源自相矛盾] "进度真相源=CSV" vs "CSV 只是缓存、真相源=backtest_results" → 统一措辞。
- [两套并发数字] MCP 7 槽 vs batch_simulator 2/3 → 给场景判定。
- [status 枚举不统一] COMPLETE/COMPLETED、ERROR/FAIL 并列 → 统一或明示两字面量均统计。
- [职责过载] 把 S1-S6 全搬进来 → 收敛 S3 行，其余引用。

### wqb-concurrency
- [C 值矛盾] 第 1 节"≤6" vs 第 8 节"C≈7" vs 例子 C=5 → 统一单一安全包络。
- [两套退避] 线性 45 封顶 vs 倍增 120 封顶 → 明确各自入口与触发。
- [测 C 循环论证] "提交 N(≥C+3)" 但 C 未知 → 给安全初始试探值。

---

## 7. L4 诊断优化层（29 问题点）

### brain-how-to-pass-alpha-test
- [改进建议被证伪] Weight 建议"中性化分散权重"紧接着"中性化对本闸无效" → 删证伪建议，统一"ts_mean/ts_decay_linear"。
- [Fitness 建议无解释] "搭配 pv13"无出处 → 删或补示例。
- [Self-Correlation 变换] 一句"做变换"无动作 → 写具体（如 `-expr`）。
- [通用建议松散] 与编号闸无对应、ATOM 未展开 → 并入各闸或成附录。
- [下游双源] 职责边界"下游=optimization-v1"与衔接协议"→ selfcorr→explain"不一致 → 单源。

### wq-brain-alpha-optimization-v1
- [批数量三处不一] "恰好 8 候选" vs Mode B "2–8 条" → 明确 8 条仅 Mode A/救援。
- [结果文件名未定] "写入指定文本文件"无路径 → 给命名规则。
- [阈值与 how-to-pass 冲突] 预期产出硬指标与平台闸数值不一 → 以 how-to-pass 为唯一权威。
- [稳健性重复] 自列 4 项又说"见 robustness" → 标"快速自查 vs 必经权威"。
- [三灯生搬硬套] probe 三灯公式套到 alpha 变体无映射 → 删或写字段映射。

### brain-calculate-alpha-selfcorr-quick
- [主结论不清] ">0.7 无需查平台"与"本地低≠平台低"方向相反 → 合并判定规则表。
- [探测越界] "POST submit 当相关性探测"越界且三处重复 → 单源到 robustness 并标注前提。
- [脚本三要素缺失] region 合法值/输出路径/依赖安装 → 补。
- [下游链不一致] 把 robustness 写成"见 optimization-v1"、judge 写成必经 → 统一。

### brain-explain-alphas
- ["战略级/近闸"不可判定] → 硬判据（Mode B 换概念前 / robustness CONDITIONAL 且用户要求）。
- [上游错位] 场景①上游实为 optimization-v1 而非 selfcorr-quick → 分场景写上游。
- [arXiv 双套] 与 optimization-v1 的 arxiv 调用重叠 → 明确本 skill 只做理解性检索。

### brain-alpha-robustness（本组最核心，已部分 P0 落地）
- [必经闸被架空] 自曝三软肋（self 声明/force 绕过/Phase B/C 无法自动）→ 降级表述 + robustness_audited 必须附归因报告路径。
- [check_correlation 阻塞] 正文仍写 `check_correlation`，验证清单已警示改 correlations/prod → 正文改轮询写法。
- [B.0 vs B.0a 顺序倒挂] 体检硬门应在 failed-count 门之前 → 改编号顺序。
- [Phase E 编号跳号] "1"后直接"3"缺"2" → 修。
- [近窗制度口径] "每年 >0.3" vs Decision table "0–0.3=CONDITIONAL" → 统一 Decision table。
- [RA/PPA 判定顺序] 未给二选一决策图 → 补。

### brain-alpha-repair
- [定位 vs 工作流] "只作配方参考"却通篇"改公式"祈使句 → 二选一或改速查表语气。
- [被掏空] 三子步骤句句"已上移" → turnover/coverage 也写成真实算子名。
- [触发无判据] "何时调本 skill vs optimization-v1" → 写清。
- [fingerprint 未定义] settings fingerprint/表达式哈希无定义 → 补一处定义。
- [universe 换档无判据] "其他 universe 记录原因"无触发条件 → 补。

---

## 8. L5–L7 提交/复盘/元层（38 问题点）

### brain-alpha-judge
- [description 残留判定语义] "deciding if worth submitting" vs 正文"不判定" → 改 description。
- [职责表"决策性"] READY/REVIEW/BLOCK 定性为"决策性"与"仅供参考"矛盾 → 改"参考性"。
- [LLM 层产 verdict] 仍产出 verdict/overall_verdict → 改名"评审意见/confidence"。
- [闸门顺序第 6 步] "确认后提交"残留提交语义 → 降级为"输出参考结论交 submit_verdict"。
- [提交语义三处打架] GET 200/403/404 vs 恒 404 → 删除废弃三态描述。
- [点塔分级重叠] A 档"差≤2"包含 B 档"差 2" → 三档改互斥（差1/差2/差3）。

### worldquant-submit-alpha
- [四态/三态命名] "四态"字面只列 3 状态码、又写"三态" → 统一"四种响应形态①②③④"。
- [配额判据矛盾] "activities 缺 today 不可用" vs "按日聚合判断今天几颗" → 删后者，唯一认 POST 响应。
- [submit_verdict 定位] 注释"唯一可信判定入口" vs "403 死代码、真闸靠 POST" → 改"模拟层+参考视图"。
- [PPA 归属三处不一致] 只 REGULAR vs 上游含 PPA vs PPA 走 web UI → 明确"本 skill MCP 只覆盖 REGULAR"。
- [异步受理取证端点] "仍 UNSUBMITTED"的取证字段未写清 → 补 get_alpha_details 查 status。
- [force 后门] force=True 绕过 submit_gate/robustness → 明确"仅限人工确认后显式豁免"+留痕字段。

### wq-brain-superalpha
- [GET 200 假阳性 vs 恒 404] 冲突 → 统一"不看 GET，二次 POST 四项闸全 PASS 为准"。
- [prod 双口径散落] "max≥0.7 一律拒" vs "只看 result 不看 value"三处 → 单列一条硬规则并收敛引用。
- [中性化结论分散] 四处无对照表 → 增区域→中性化对照表。
- [硬前置嵌套历史] "组件数量"条目内嵌六层含历史教训 → 拆分。
- [何时用 vs 职责边界重复] → 合并。

### wq-backtest-monitor
- [章节号断档] §1-4/§9 缺失、§4 被引用却已删 → 重新编号。
- [§5 vs §10 四关重复] → §5 删历史数字、§10 为唯一强制口径。
- [ETA 取证不一] §11 用 progress.log vs §13 用 checkpoint → §11 以 §13 为准。
- [职责 vs §14 回写张力] "不是写入方" vs "必须回写" → 改"调用方身份"。
- [§7 "10 种结构"模糊] → 定义"一种结构"三元组 + "满意"判据。
- [盲区章节] 已删却 §12 仍要求输出 → 恢复或删报告项。

### brain-dataset-mining-experience
- ["只读"字面矛盾] "只读台账"却主功能是写经验文件 → 改"只读 DB、仅产出派生 Markdown"。
- ["记录失败" vs "判死"分界] → 加判据（只记搭配+失败指标，不下"已死"结论）。
- [三入口不清] workflow_campaign/tools/dataset_experience.py/src 实现 → 明确首选与三者关系。
- [s6_verdict 主动语态矛盾] → 改"由上游 S6 完成，本 skill 只消费"。
- ["测量缺陷"无判据] → 给缺陷清单（跨 UNITS/universe/延迟等）。

### pull-brain-skills
- [命名校验矛盾] "不校验命名" vs "应警告 camelCase" → 统一。
- [人工归层无判据] → 注明归层依据见 INDEX。
- [--branch 与 ZIP 关系] → 明确仅 Git 生效。
- [示例单一] → 补非 GitHub/非 main 反例。
- [有效性规则重复] → 合并。

### planning-with-files
- [hooks 占位符隐患] `<SKILL_ROOT>` 不会替换、`cat` 假设 cwd=根 → 改确定路径。
- [触发阈值不一致] ">5 次工具调用" vs "3 步以上" → 统一量纲。
- [两动作规则不可计数] → 删粗规则、以决策矩阵为准。
- ["auto-activates"误导] hooks 无复杂度判定 → 改"打印提示引导"。
- [三文件职责重叠] → 加归类判据。

---

## 9. 优先修复建议（按 ROI）

| 优先级 | 动作 | 涉及 skill |
|---|---|---|
| **P0** | 修正会**直接误导执行**的硬伤：verifier 示例路径 `python scripts/`、news-sentiment 4 个死链、judge 提交语义三处打架 | verifier / news-sentiment / judge |
| **P0** | 统一"闸/硬门"表述：凡自称必经闸/硬门必须标注实现形态（代码/工具/文档约定） | robustness / field-quality / news-sentiment / ra-pipeline 步5b |
| **P1** | 单源化跨 skill 重复事实：体检工具分工表、GET /submit 结论、提交探测协议、robustness 下游链、并发 C 值 | ppa-mining / next-move / submit-alpha / superalpha / selfcorr / robustness / concurrency |
| **P1** | 消除"正文 vs 定位声明"矛盾（Agent 会做错事） | FI / repair / ppa-mining / judge / inspect-setting / feature-engineering |
| **P2** | 模糊判据量化（战略级/近闸/同质/满意/一种结构） | explain / labs / matrix / next-move / backtest-monitor |
| **P2** | 死代码与残留叙事清理（hybrid 别名、HTML 转换、学习闭环 G1） | forum-browse / toolkit |

---

> 本报告只做审查与建议，未改动任何 skill 正文（除本轮已完成的 P0 提交路由、robustness/worldquant-submit-alpha 两处文档同步）。
> 建议按 P0 → P1 → P2 分批落地，每批改完跑 `python tools/sync_skills.py` + `pytest tests/` 回归。
