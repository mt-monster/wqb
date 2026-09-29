# skills 审查处置台账（闭环）

> 对应 `reports/skills_review_20260929.md`。**每个条目 ID 都有去向**；数据源 `docs/skills_review_closure.json`（`tools/closure_ledger.py` 维护，`tests/unit/test_closure_ledger.py` 守）。生成：`python tools/closure_ledger.py render`。

状态：**fixed** 本轮已改 · **superseded** 被别的改动一并解决 · **declined** 有意不改（含范本）· **needs-platform** 依赖平台实测或业务裁定 · **open** 未处理。

| 状态 | fixed | superseded | declined | needs-platform | open | 合计 |
|---|---|---|---|---|---|---|
| 条数 | 224 | 0 | 2 | 1 | 531 | 758 |

## T0

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| T0-1 | open |  | 上游条件写“SUBMITTABLE”永远不满足；以 `$?==0` 放行的脚本会放行 UNVERIFIABLE |
| T0-2 | open |  | “同族连测”“先 5 个探针”会把最先通过的那颗真提交 |
| T0-3 | open |  | 参数错误或未经确认的真实提交 |
| T0-4 | open |  | 违反“prod≥0.7 不提交”的用户铁律；agent 无从创建 SA |
| T0-5 | open |  | “不执行提交”只靠散文；合法 PPA 被误杀 |
| T0-6 | open |  | 误杀 5 类旁路候选 |
| T0-7 | open |  | S6 回写失败或写入废止键，下一轮读不到结论 |
| T0-8 | open |  | 拒绝合法 universe / 用已下线档位 |
| T0-9 | open |  | 非 Windows 环境全部 Python 命令指向不存在的可执行文件 |
| T0-10 | open |  | 照抄挂闸或绕过闸门；政策与机检口径分叉 |
| T0-11 | open |  | 同一情景 agent 可合规地做出相反动作 |
| T0-12 | open |  | 整批 ERROR/CANCELLED |
| T0-13 | open |  | 知识既不在原处也不在新处 |
| T0-14 | open |  | 误判余量撞 4/4 墙；一小时日界漂移 |
| T0-15 | open |  | 凭据泄露面 + 核心资产外发 |
| T0-16 | open |  | 外部指令/钩子静默进入运行时；覆盖核心 skill |
| T0-17 | open |  | 真相源分裂 |
| T0-18 | open |  | 声明存在而实现缺位，闭环断裂 |
| T0-19 | open |  | 覆盖率 100% 的错觉 |
| T0-20 | open |  | `command not found` / 找不到文件 |

## X

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| X-1 | open |  | prod 墙：同一情景 ≥6 套互相矛盾的处置学说 |
| X-2 | open |  | 提交判定链与“唯一权威” |
| X-3 | open |  | 加权混合 / 腿相加：政策已禁、闸门有缺口、文档仍在教 |
| X-4 | open |  | 术语表：同一个词 2–4 种含义 |
| X-5 | open |  | verdict / 状态词表：≥12 套 |
| X-6 | open |  | 闸门模式开关：形态不一、默认不一、含日期翻转 |
| X-7 | open |  | 多副本真相源与“唯一”宣称的实际状态 |
| X-8 | open |  | “台账记因 / 豁免”：至少 17 处，没有一个键名 |
| X-9 | open |  | 不可逆 / 有外部副作用的动作：防护靠散文 |
| X-10 | open |  | SOP 的结构与写法：规则、叙事、快照、日志分离 |
| X-11 | open |  | 数字漂移总表（应只引用 `config`） |
| X-12 | open |  | 日期快照与硬编码清单 |
| X-13 | open |  | DB 单轨 vs 文件产物 |
| X-14 | open |  | 可移植性：Windows / PowerShell / 固定偏移 |
| X-15 | open |  | 等待 / 退避 / 卡住阈值 |
| X-16 | open |  | 算子与表达式知识：SOP 里的例子要过自家闸 |
| X-17 | open |  | 守护体系：形式有测试，内容无检查 |
| X-18 | open |  | “声明存在、实现缺位”清单 |
| X-19 | open |  | 时间炸弹 |

## P0

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| P0-1 | open |  | SKILL.md L56（`ts_median`，幽灵算子）、L60–61（`scale_down`）、L73–75（`ts_event_sum/count/mean`）仍在；`k |
| P0-2 | open |  | SKILL.md L166–172、L220 仍在，无“历史范式”标注；**补充**：实测 gate.py 对该形态**放行**（权重在右），上一轮“被闸 5 block”对该形态 |
| P0-3 | open |  | INDEX L417–420 与 `tools/quota_status.py` 已改正；但 submit-alpha 同文 L191（不可用）与 **L264（仍叫人用）** 矛 |
| P0-4 | open |  | `submit_alpha` 节点已补 re-POST/`ASYNC_STUCK`（`nodes/submit_alpha.py` L263–288）；submit-alpha 四 |
| P0-5 | open |  | brain-make-some-gem SKILL.md 全文无 “402”；失败表仍缺该项（RA 步 4 引言有） |
| P0-6 | open |  | “5 轴/6 武器/分布形态/体检硬门复验/幽灵算子清单”在 optimization-v1 均零命中；INDEX L113 仍以此为卖点 |
| P0-7 | open |  | brain-alpha-research L60–61（`wqb research`、`wqb settings`）、news-sentiment L70（`wqb news-re |
| P0-8 | open |  | `data/hypothesis_catalog`、`data/field_semantics` 仍不存在；RA 步 2 #6 仍强制切换；未标 dormant |
| P0-9 | open |  | sim-alphas L61–62 已把 `alpha_list.json` 标为“已废弃的文件模式，仅排障/兼容”、`simulation_status.csv` 标为“进度缓存 |

## AR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| AR-01 | open |  | description 与“触发场景”段几乎逐字重复；“数据集发现/字段选择/类别映射”与 `brain-dataset-exploration-general`、`brain-d |
| AR-02 | open |  | 边界句：“不得自行修正/撤回 `config.py` 权威常量；skill 不是常量的第二作者”，同一文件却在步 10 维护“全区域 universe/delay/中性化固化表”约 |
| AR-03 | open |  | 路由表只列 3 个专项 + “其他（本 skill）”；未列同为 L1 的 dataset-exploration / datafield-exploration / featur |
| AR-04 | open |  | 读者是开发者：读源码（`evidence.py`）、补 `config.py` 缺项、扩 `PARADIGMS`；agent 视角的“研究”产出无格式（步 6“机器可读的简明记录” |
| AR-05 | open |  | 步 1 要求“读源码 `src/wqb/research/evidence.py` 理解最新设计信号”，链接为 skill 相对路径（skill 被同步到其它宿主目录后失效）；应是 |
| AR-06 | open |  | 落点清楚（`KB/community_tpl_kb` / `KB/template_kb`，不是代码模板表）——好；但 L46 整段是“已删除模块”的史注，`paradigms.p |
| AR-07 | open |  | “形状覆盖…`validator.check_batch` 正是按 shape signature 判重（≥2 shape signatures），所以形状覆盖是**过闸条件**” |
| AR-08 | open |  | 固化表要点（COUNTRY 中性化仅 EUR/GLB/ASI/MEA；Delay=0 仅 USA/EUR/CHN/GBR/DEU）与 ppa-mining（Delay 0 仅 US |
| AR-09 | open |  | API 实测约束 (a)–(e) 是 ppa-mining §9.1 与 ra-pipeline/ppa-mining-experience 的第 3 份拷贝；(e) 含 `loc |
| AR-10 | open |  | 2026-08-05 快照（HKG 209/KOR 192/EUR 178 数据集、“19 个未开发数据集首选 `ml_factor_proj`”）当作 S0 旁证保留，并在正文里 |
| AR-11 | open |  | 步 13 与 ppa-mining §1.3、ppa-mining-experience 重复；离线包星级说明第 3 次出现 |
| AR-12 | open |  | “运行 `wqb research` / `wqb settings`”——**仓库无此 CLI**（无 `cli.py`、`pyproject.toml` 无 scripts）； |
| AR-13 | open |  | ①5 个无入链（`alpha-inspiration-usa-d1-shortinterest-insiders`、`asi-methodology`、`backtest-expe |

## BM

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| BM-01 | open |  | description 与 H1 把本 skill 定位为“WorldQuant BRAIN **PPA** alpha 挖掘任务的监控/盘点/效率分析”“WQ PPA 挖掘·监控 |
| BM-02 | open |  | “持久化铁律（DB 单轨）”置于 frontmatter 之后、H1 之前，且在多个 skill 里逐字重复；与本 skill 自己的取证来源冲突：§10 的“取证方式”全是 ch |
| BM-03 | open |  | 边界“负责：…§14 台账回写”，同时“**不是** `wave_results`/`registry_empirical` 的正式写入方——唯一正式写入 = toolkit 幂等 |
| BM-04 | open |  | 三处对“机器级进程枚举”的要求互相矛盾：L36“当用户要盯回测/盘点…按下述框架产出**完整分析**”；§7 #6“监控第一视角：**必须**机器级进程枚举为发现入口”；L43–4 |
| BM-05 | open |  | “四关”（① 研究仿真 IS 廉价闸 ② 生产仿真 OOS ③ 生产相关性 ④ 平台 submittable + 真实提交）是全库**第 4 套闸门分类**（gate.py 闸 1 |
| BM-06 | open |  | “取证函数 `collect_verified_pids()`（取 `found_alphas` 的 pid）”——全库检索仅此一处，函数不存在；`found_alphas` 是  |
| BM-07 | open |  | “并发模型·Token-Bucket（C=7）”与 `wqb-concurrency`（L3）重复；核对 `config.CONCURRENCY = {slots 7, burst |
| BM-08 | open |  | 工作纪律 6 条：①“universe 合法性：TOP500/1000/2000/3000 合法；**TOP800/1500/2500/5000 非法**（400 拒）”与 `co |
| BM-09 | open |  | ①“新监控脚本应在 `tools/` 按**统一规范**新建”——规范未给；②“红线：绝不动在跑进程的 checkpoint 与脚本（如 v52b …）”是好红线（🟢），但示例是历 |
| BM-10 | open |  | “提交核查（强制章节，每次汇报不可省略）”：①三级分类“✅ 已正式提交 / ✅ 回测完成待提交 / 🔶 仍需进一步验证”，但“**回测完成待提交**”未定义，且与“PASS_CHE |
| BM-11 | open |  | “ETA（强制章节，每次汇报不可省略）”的输出格式要求“包含 **ds 舰队全部 7 路 + tri_track + v52b**”——这些是 2026-09 前的历史任务（L80 |
| BM-12 | open |  | “标准报告结构（**唯一标准依据**）：§1 背景 / §2 分析维度 / §3 核心发现 / §4 结论与建议”，其中 §2 又写“进程盘点（§1–§2）/ 并发进度（§2）/  |
| BM-13 | open |  | 🟢“判停依据 = poll 熔断参数组：progress 60 min 无变化判 STALLED、总超时 360 min（可被 thresholds.json `poll` 节覆盖 |
| BM-14 | open |  | **命令模板四条全部与真实 CLI 不符**（核对 `_lib/wave_results.py`、`_lib/registry.py`、`_lib/ledger.py`）：①`wa |
| BM-15 | open |  | “方法论规则计数：若本波消费了 `tracking/<REGION>/reference/methodology_rules.json` 的 active 规则，回写 `times |
| BM-16 | open |  | 三条写入路径并列：toolkit CLI（战役目录内）/ `mcp__wqb-db__upsert_*`（无战役目录）/ `upsert_ledger_key`（“如 submit |
| BM-17 | open |  | L159“中文/JSON 参数一律走 `@file` 文件通道（AGENTS.md §5）”，但 `@notes.json` 等文件写到哪里未说（战役目录？scratch？）；与  |
| BM-18 | open |  | 缺三张情景：①**日常一波收尾**（pipeline 完成 → `review_wave` → `wave upsert --verdict` → `get_wave_result |

## CM

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| CM-01 | open |  | 字段顺序与其余 skill 不同（`last_verified` 先于 `name`）；description 后半是“它做什么”（解析配置包、原样派发 S0–S6、回写 regi |
| CM-02 | open |  | 6 个空行；运行环境一句话放在 H1 标题**之前** |
| CM-03 | open |  | 三种说法互相矛盾：职责边界“**本 skill 负责** … 战役后回写 registry”；§4 与 L139“**由本 skill 的 §4 回写流程**提炼判死结论”；L14 |
| CM-04 | open |  | “既有 **31 个**其他 skill”硬编码（现为 33 个 SKILL.md，INDEX 有 32/33 两种说法）；“只做查表与回写、不执行挖掘”在 L24、L32、L36 |
| CM-05 | open |  | 写入路径：L37“走 `campaign.py registry` 幂等 CLI **或** 会话内 `upsert_registry_empirical`”；§4 与硬规则 4“ |
| CM-06 | open |  | 单个 ≈750 字 bullet 含两条规则 + 工具指针：①“强制”标注 `prod_risk: high` / `prod_saturation: likely`，但**没有  |
| CM-07 | open |  | “S0 健康检查 = `wq-brain-ppa-mining` §1.0 硬门槛方法论 + `score_datasets.py`”——把 PPA 专用阈值（cov≥0.85/a |
| CM-08 | open |  | **两套 schema 并存**：表格说 4 张表（`regions`/`datasets`/`registry_empirical`/`cross_region_lessons` |
| CM-09 | open |  | 一段里含历史（2026-08-21 起单轨、JSON 已归档）、读法（MCP 或裸 SELECT）、写法（CLI）、迁移工具（migrate_phase2.py）；提到的 `cam |
| CM-10 | open |  | “region（**必须**）”，却又在 ra-pipeline 三角分工里被定义为“**where=查表选区**选集”。matrix 无法选区（region 是入口参数）；真正的 |
| CM-11 | open |  | 只给调用，没说返回结构与空结果的含义（`get_region_config` 返回空 = 新区？） |
| CM-12 | open |  | 自由文本样例，缺：`prod_risk/prod_saturation`（强制项）、`entry_verdict`（profile）、`lit_towers`（09-19 硬规则） |
| CM-13 | open |  | 把九步派发链**整段复制**（步 2–9 的工具名），与 ra-pipeline 已不同步：仍写步 3 用 `workflow_feature_engineering`（ra-pi |
| CM-14 | open |  | 代码块标 bash、用 `\` 续行，正文却规定 PowerShell；`campaign.py` 裸写，前文说 `$WQ_TOOLKIT_DIR/campaign.py`；示例  |
| CM-15 | open |  | “只记有跨会话价值的结论，不记过程性噪声”——判据抽象 |
| CM-16 | open |  | 步骤**不可执行**：①数据源 `research-data/fresh_datasets_7region.json` 不存在（机械检查）；②“复制到 assets 层/stati |
| CM-17 | open |  | “以更新 registry 为准”歧义（以“更新后的 registry”为准，还是“去更新 registry”？） |
| CM-18 | open |  | “死路 rule **优先于用户直觉**”与 ra-pipeline/decision-table 的“用户显式指令 > 决策表”冲突 |
| CM-19 | open |  | 说“AMR/**JPN** 本工作区未启用（无 profile、无战役目录）”——JPN profile 已于 09-15 补齐（ra-pipeline L62），JPN 有 pr |
| CM-20 | open |  | “禁止散装 SQL”出现 5 次 |
| CM-21 | open |  | 同两行内自相矛盾：“submit_ready … **进战役台账（ledger_kv）不进 registry**”与“registry schema 约定：region 级可增 … |
| CM-22 | open |  | matrix 硬规则 1 说 **registry 是“唯一事实源”**；ra-pipeline 步 4/9 说 **DB KB（`region_kb`/`template_kb` |
| CM-23 | open |  | “S6 均走 toolkit 幂等 CLI”，而 ra-pipeline 步 9 示例是 MCP `upsert_*`；“未回写的复盘视为未完成”与 ra-pipeline 完成定 |
| CM-24 | open |  | **没有失败分支与反例**：`get_region_config` 空、region 不在 REGIONS、registry 与 profile 冲突、写入被幂等 CLI 拒绝（缺 |

## DE

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| DE-01 | open |  | description 中“跨平台调研”正文没有对应步骤；“字段分类”触发与 news-sentiment 重叠；运行环境句在 H1 之前、7 个空行 |
| DE-02 | open |  | 边界句禁止“自行维护区域表”，随后维护一张“Region → Universe”表；表中 **JPN “不是有效的 EQUITY 区域，`get_datasets` 返回 0”** |
| DE-03 | open |  | 边界说“上游=S0 白名单（数据集已选定）”，Phase 1 第 1 步又是“确定数据集：根据战略重要性或用户需求选择”且无判据 |
| DE-04 | open |  | 字段分类按业务职能/数据类型/频率/层级，**没有产出位置**；下游 RA 的硬前置是 `s1_semantic_<ds>` 台账（`field_semantic_classify |
| DE-05 | open |  | 给出的评分公式是**旧式**：`0.30/(1+log10(1+alphaCount))`、“vs 缺失按 0.3”、tier2“cov≥0.85/ac≤200/fc≥5”；而其指 |
| DE-06 | open |  | “调研：查阅论坛（`brain-forum-browse` skill 或 `search_forum_posts`）”——与 RA“论坛默认不查（token 黑洞）”冲突；加载  |
| DE-07 | open |  | “撰写详细描述”“改进描述”“为所有字段编目”——无输出位置/格式；对 1000+ 字段的数据集（JPN analyst 1026）不可行，无范围控制 |
| DE-08 | open |  | 英文岗位手册体裁（Position Overview、Deliverables），与中文 SKILL 混用；含旧流程 |

## DF

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| DF-01 | open |  | 标题/description 说“6 种方法”，正文有 6 法 + 2 个备注 + “7. 批量字段收割”，编号跳跃 |
| DF-02 | open |  | “运行这些模拟时用 Neutralization None、Decay 0、Test Period **P0Y0M**”——6 种方法每个字段各需 ≥1 次仿真，文中**没有成本提 |
| DF-03 | open |  | `ts_median(datafield, 1000)` 注为“5 年中位数”——1000 交易日≈4 年（标准窗口是 1008=4 年），窗口非标且换算错；**更根本的是 `ts |
| DF-04 | open |  | “VECTOR 字段应**直接**用于 rank/ts_*，**不要**包在 `vec_*` 里；`winsorize` 安全”——与全库相反：toolkit 闸 3“type== |
| DF-05 | open |  | “EVENT 先用 `ts_event_*` **转换为 VECTOR**”——把 `ts_event_*` 的输出称为 VECTOR，与闸 3 对 VECTOR（需 `vec_* |
| DF-06 | open |  | “GET /data-fields 裸 `dataset=` 被静默忽略→必须 `dataset.id=`（KOR 2026-08-15 实测）”+ 4 步规避 + 实测说明——* |
| DF-07 | open |  | 只讲“怎么测”，没有“测完怎么用”（覆盖%、频率→窗口选择、范围→预处理的**决策映射**），职责上交给特征工程但无链接 |
| DF-08 | open |  | **算子口径与库内清单/闸门不一致（上一轮评审 P0-1，至今未修）**：方法 5 用 `ts_median(datafield, 1000)`——`ts_median` 在 `p |

## EV

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| EV-01 | open |  | 标题“校验非法表达式”，示例 `rank(close, 5)`，注释却说“rank(x, n) 是合法的（n 为窗口），此例仅演示运行位置”——**没有任何真正非法的示例、也没有期 |
| EV-02 | open |  | 路径两种写法（`$WQ_VALIDATOR_DIR/verify_expr.py` 与示例里的 `scripts/verify_expr.py`），`$WQ_VALIDATOR_D |
| EV-03 | open |  | `densify()` 可接收原生 GROUP 分组轴，“本层无法确认平台类型；输出仍是分组键，不能交给 `rank()` 等数值参数”——明确写出**本层做不到什么** |
| EV-04 | open |  | “gate.py（**5 闸**）”（实为 8 闸+闸 0）、“validator.py（1363 行巨石）”行数会漂移；“不要改 validator.py”是变更纪律，宜放 AG |
| EV-05 | open |  | 无失败分支：脚本找不到、依赖缺失、`errors` 各类型的含义与处理 |

## EX

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| EX-01 | open |  | 边界与衔接协议称本 skill 服务于“Mode B 换概念前**先查概念重叠**”与“提交前对战略级候选做收益来源确认”。但 6 步模板全部是“解释一个 alpha”，**没有一 |
| EX-02 | open |  | “必填/推荐参数：`instrument_type`（如 EQUITY）、region、delay、universe、data_type、search”——MCP `get_dat |
| EX-03 | open |  | 第 2 步“获取每个数据字段的详细信息”，但工具默认 `filter_sharpe=True`——**OS/IS Sharpe<0 的字段被静默过滤**。解释一个已有 alpha  |
| EX-04 | open |  | 首例 `quantile(ts_regression(oth423_find, group_mean(oth423_find, vec_max(shrt3_bar), countr |
| EX-05 | open |  | reference 说“本手册附录提供了最常用算子的速查表”，但附录只有“附录 A：理解 Vector 数据”——**指向不存在的附录**；第 3 步全量 `get_operato |
| EX-06 | open |  | 第 5 步“可选”，但：①`python scripts/arxiv_api.py` 是相对路径，agent 的 CWD 通常不在 skill 目录；②同名脚本在 optimiza |
| EX-07 | open |  | 🟢 四段模板与“收益来源归因”的用途对得上。P2：①“数据理由”只问“它们代表什么”，**没有证据要求**——收益主要来自 long 侧还是 short 侧、哪一年、哪个行业（`g |
| EX-08 | open |  | “需要聚合（如 `vec_mean`、`vec_sum`）”——**`vec_mean` 不在 `known_ops`（103）**，平台算子是 `vec_avg`（`vector |
| EX-09 | open |  | 上游 selfcorr-quick；本 skill 是“S4 按需工具”；下游 robustness（必经闸）。而 robustness 又把 explain-alphas 列为其 |
| EX-10 | open |  | 缺两个情景：①“Mode B 换概念前查重叠”——给一个含 3 个 ACTIVE alpha 的 book，目标候选与其中 1 个共享（字段族、时序骨架），输出“重叠高 → 建议换 |

## FB

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FB-01 | open |  | description 中英混杂并含 markdown 粗体；把 explore/contribute 两个社交模式写入触发，recon 不在触发词里（而 RA 恰是它最大的调用方 |
| FB-02 | open |  | 一个 skill 同时是①社区互动（强制贡献 + Run Contract + 对抗审查 + curator）②流水线 recon（只读、免贡献/合同/工作区记忆）——治理规则** |
| FB-03 | open |  | “不要用于提交前审查 → 用 `brain-alpha-judge`”，边界句却说提交审查归 `tools/submit_verdict.py`、judge 仅参考 |
| FB-04 | open |  | “每轮必贡献/不允许只浏览/不可协商”至少**6 处**重复且措辞强度各异；而环境无写工具（`search_forum_posts`、`read_forum_post` 是仅有的两 |
| FB-05 | open |  | 表里先用 E1、7.5、Contract、6–9、auto-send，而 E1/E2/E3 到 L72/L180 才定义、Phase 编号从未在 SKILL.md 里成序列出现；四 |
| FB-06 | open |  | 链接**文字是已合并的旧文件名**（`auto-send-e1.md`、`profile-bootstrap.md`、`personal-perspective.md`、`exte |
| FB-07 | open |  | 决策树是全文最清楚的一处（好），却自称“唯一表述，替代分散规则”，而规则仍散落（FB-04）；L77“无话可说仍尝试 linker 式最小价值”与 L179“仅在有 E2 + 索引 |
| FB-08 | open |  | 引用块里有**高价值排障**（“服务没起=论坛工具‘不存在’、极易误判为未实现”；排查顺序 ①`start_wq_mcp.py --check` ②`MCP_PORT=8876`  |
| FB-09 | open |  | 表头是“**必须**用的 MCP”，第 5 行却是“wq-brain-http **未实现**” |
| FB-10 | open |  | “凭据来自 MCP 服务器配置；**仅在认证失败时才传 `email`/`password`**”——与 AGENTS.md（凭据只在 `.env`、禁止读取/打印）及本 skil |
| FB-11 | open |  | “运行时**不要探测或列举 MCP 工具**”与“工具在表里搜不到时按排障顺序检查”并存 |
| FB-12 | open |  | 两个表重复同一批工具；L129 写 `search_forum_posts`“**唯一**搜索工具”，而标题“多种方法/自行选型”、L194“不必每次 slow，也不要只知道 fa |
| FB-13 | open |  | 命令用裸 `python`、`scripts/…` 相对路径（仅当 CWD=skill 目录才成立）；`outputs/workspace/` 位置未说（skill 目录？仓库根？ |
| FB-14 | open |  | “硬性规则”20 条：≥8 条重复前文（每轮必贡献×3、MCP 优先×3、论坛数据仅来自 MCP、默认 explore、Run Contract 闸、Search 工具箱）；“MC |
| FB-15 | open |  | Pipeline 阶段号非单调（7.5 → 1.5 → 6–9，Phase 7 在 6 与 7.5 之间），全文没有一份成序的阶段清单；“每个会话 **L1**”的 L1 与全库“ |
| FB-16 | open |  | 记忆层 P0–P5 与全库其它 P 编号（S0 的 P5 饱和拍平、probe 模板 P5、审计 P-codes）同号异义 |
| FB-17 | open |  | “每次运行最多计划 3 个写操作”与“每轮必≥1”并存；recon 的 `--max-search-rounds` 只说是“安全上限”，无缺省数值 |
| FB-18 | open |  | 参考资料索引清楚（好），但括号里仍列已合并前的旧文件名 |

## FE

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FE-01 | open |  | 三种说法：①定位修正（09-15）：节点产出是**确定性模板**、不再被 GEM 注入，agent **人工**完成并写 `source=manual` 才注入；②L162：本 i |
| FE-02 | open |  | 第 6 步 ledger 示例里 `"source": "standalone"`；而 RA/GEM 规则是 `source ∈ {feature_engineering_node |
| FE-03 | open |  | “S1⇄S2 统一逻辑链”写：`s1_<ds>_d<delay>` 命中且 `ideas_md_path` 可读 → `--ideas-file` 注入——未按 source 区分 |
| FE-04 | open |  | 边界说“不做选集/输入=S1 白名单”，第 1 步却包含“未提供 dataset_id 时基于元数据选择最相关的数据集”（选集属 S0/dataset-exploration）；输 |
| FE-05 | open |  | “universe 默认 `TOP3000`”对多数区域错误（KOR TOP600、EUR TOP2500…） |
| FE-06 | open |  | 分档判据有数值（描述覆盖≥80% 且均值>5 词；<30%）和依据（103 个 s1 键的审计）——好；但三档均“满足其一”，`model*` 集若描述覆盖≥80% 同时满足透明与 |
| FE-07 | open |  | 8 问 × 每字段 → 概念数无上限；RA 已实证“组合爆炸”（黑名单字段占 9.9% 却吃 49.4% 生成预算）；步 4 的 8 属性模板没有 GEM 需要的 **Implem |
| FE-08 | open |  | 输出写到相对路径 `./output_report/…_ideas.md`（该目录是审计报告目录，与运行 CWD 有关），同时又写 ledger；“DB 唯一事实源”与文件产物的主 |
| FE-09 | open |  | 报告提纲（1–5 章、3.1–3.8）与 `OUTPUT_TEMPLATE.md`（325 行）内容重复，且提纲每项只是“度量××的概念”类空泛描述 |
| FE-10 | open |  | “本 skill 不应当：让用户思考/提供通用模板”与节点的实际行为（确定性模板）矛盾；原则 5 条为泛化口号 |
| FE-11 | open |  | 示例数据集 `BEME`、字段 `book_value/market_cap/book_to_market` 疑为虚构（与“保持具体：引用真实字段名”自相矛盾）；未含窗口/表达式 |
| FE-12 | open |  | 质量自查“**所有字段都被分析**”与第 0 步允许透明集**跳过 8 问**冲突；“新颖/避开传统思维陷阱”无法检验 |
| FE-13 | open |  | `brain-make-some-gem/scripts/trailSomeAlphas/skills/` 下的 `brain-data-feature-engineering`、 |

## FI

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FI-01 | open |  | description 的触发语“当用户提供 idea 文档、**要求生成 alpha 表达式**或下载数据集时使用”会让它被直接触发，而边界句与 RA 反模式都禁止把它当主链入口 |
| FI-02 | open |  | “skill 层不直接调用 MCP”，数据下载经 `ace_lib` 用 **skill 目录内 `config.json` 的明文邮箱/口令**——又一种凭据来源（全库已有 ≥8 |
| FI-03 | open |  | “定位脚本：`ls -R` / `Get-ChildItem -Recurse` 找 `fetch_dataset.py`，通常在 …/scripts”——**没有给出确定路径** |
| FI-04 | open |  | “使用 `TaskCreate` 工具创建计划”——宿主专有工具；GEM 把本文件拼进 LLM prompt 时该指令无意义 |
| FI-05 | open |  | 步骤 5 产出 `final_expressions.json` 并“向用户报告文件路径”，而边界头与全库均规定该文件**不是真相源**、DB 才是；手动流程没有入库步骤 |
| FI-06 | open |  | “描述”节里塞了行为规则（占位符只绑定一次、GROUP 不自动扩展数值变体） |

## FQ

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FQ-01 | open |  | “按 `alphaCount` **降序**排字段、从分布头部开始播种（社区反复用来构建可提交 alpha 的字段更可靠）；低使用量字段只用于去相关/新颖性”——与 RA 步 3  |
| FQ-02 | open |  | “用 `jq` 把保存的 `get_datafields` 结果排序取前 ~30”——`jq` 在 Windows 环境未必存在；DB 唯一模式下字段目录在 `fields` 表， |
| FQ-03 | open |  | 规则速查 (a)“甜点区 100≤count≤3000 且 sharpe≥1.1×均值；<50 不可信、**>30K 饱和**”——饱和阈值 30K，而 RA 步 2 #6 用 * |
| FQ-04 | open |  | 核心 26 条规则在另一个 skill 的 reference（`../brain-alpha-research/references/…`，跨 skill 相对链接），且写“23 |
| FQ-05 | open |  | 数据包覆盖边界（7 区、9 组合、160 条/125 名）+ 判定顺序 + 免预筛留痕——**场景→顺序→动作**清楚；小笔误“这此区域” |
| FQ-06 | open |  | “**每次切换区域回测前必须**先跑 `webdata_quality.py`（用户强制纪律）”，但 DEU/IND/GBR/MEA/TWN 不在包内，预筛必空；本节未提上一节的豁 |
| FQ-07 | open |  | “机器门禁 `prescreen_gate.py`……当前为工具级门禁，节点内嵌接线待 `nodes/campaign.py` 并行改动落定后跟进”——待办状态写进 SOP；且 r |
| FQ-08 | open |  | 验证清单 3 条都是“确认已…”，无期望输出/无留痕位置 |

## FR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FR-01 | open |  | 头注“合并自 modes-and-contract.md / modes-and-contract.md / auto-send-e1.md”（自己出现两次）；“三种模式”遗漏 r |
| FR-02 | open |  | **A1–A8 是全库最可检的条件清单**：恰好 1 条、E1-only、零推断（列出禁用词）、第一人称事实、含指标须本轮已调 `get_user_alphas`……并配“自检清单 |
| FR-03 | open |  | 允许“本机 AI 对话（P4）”作 E1 公开来源，未给脱敏/同意规则（FB-10） |
| FR-04 | open |  | 约一半是空行（逐行双倍间隔的转换痕迹）；中英混排；末尾“Decision tree”含改名残留：`get_glossary_terms, get_glossary_terms`、“ |
| FR-05 | open |  | 机械检查 §B 报“断链 → url”是示例表格里的 `[文字](url)`，属**误报**；但整篇 136 行只在写路径开通后才有意义 |
| FR-06 | open |  | 均以“Phase/Run Contract/对抗审查/Role Matrix/Index Post”等写路径概念为主；`self_overlap < 0.4` 等阈值无依据；与 S |
| FR-07 | open |  | 模板与脚本都服务写路径；脚本用 skill 相对路径 |

## GM

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| GM-01 | open |  | “`priors_snapshot_<region>` 只读消费，唯一写入方=assemble-priors；stale 只 WARN 不阻断，**不得据此认为‘已确认安全’**； |
| GM-02 | open |  | 下游写成“`check_batch` 多样性守卫 → `check_expr_against_inspect` 体检硬门 → `wave_gate` 闸 1–5”三段串联——实际应 |
| GM-03 | open |  | 一段 ≈400 字含 4 个主题：`pipeline_mode` 透传、headless 缺省改 phased、ideas 注入规则（模板渲染 source 不注入）、预闸内容（q |
| GM-04 | open |  | 铁律 2“必须带 priors（默认 DB 快照，fail-closed）；`priors_file` 仅作覆盖”**正确**，印证 RA 硬约束 #2“必须带 `priors_f |
| GM-05 | open |  | “只消费 `wins`(≤6)/`dead_ends`(≤12) 两键，其余忽略”与 RA（`methodology`/`signal_family_rules` 作 region |
| GM-06 | open |  | 铁律 6 允许“第二腿之后每加一腿，须点名它修哪个闸（sub_universe/2Y/CW）”——即**用补腿修不达标的信号**，而 decision-table D3/RA“路线 |
| GM-07 | open |  | 铁律 7 声明“旧规则强制每波 ≥1 个 Logical 算子已废除；算子多样性应是语义多样性的结果”——但 toolkit 闸 6 的契约仍可强制 `required_opera |
| GM-08 | open |  | “Expected Exposure 会被验证：`risk_neutralized_sharpe`≈0/为负而 raw 高 ⇒ **该概念**就是暴露本身，判 dead_end 且 |
| GM-09 | open |  | 返回 `mode_b_required`（EXPECTED_BLOCK>0 时为真）后**做什么**没写；`quality_estimation` 与 wave_gate 的 qp |
| GM-10 | open |  | “直接命令”只写生成，**没有写入 DB 的一步**（产物契约又说“未验证 DB 有表达式，不得声称步 4 成功”）；`--dry-run` 只验证命令构建，未提“不验证 LLM  |
| GM-11 | open |  | “看实时生成过程”：给了两种方式、**代价**（关窗口=杀任务，phased 无断点）与**默认选择**（`--watch`）——范式；但含 Windows 控制台专有细节（`DE |
| GM-12 | open |  | 三段查找路径 + “旧位勿再用于新跑” + “文件不是真相源”；迁移事故（16 个产物文件混入仓库）交代清楚。含行号引用 `gem.py:1219`（会漂移） |
| GM-13 | open |  | skill 目录解析顺序（env > skill_roots > 内嵌）、打印行 `[skill-doc] … OK/MISSING`、“看到 MISSING/`embedded: |
| GM-14 | open |  | 失败表缺**最具迷惑性的两种**：LLM 余额不足 `402 Insufficient Balance`（表现为“no meta.json within 90s”、干跑假绿，RA  |
| GM-15 | open |  | 仍把**旧深嵌套路径**（`scripts/trailSomeAlphas/skills/brain-feature-implementation/data/...`）当**产物与 |

## HF

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| HF-01 | open |  | 本 skill：“假设目录为空时**不强行路由**（需先有假设生成器）”；RA：数据集 alphaCount≥1 万或连续 2 波全灭 → “**强制**切本工作流，不再做模板遍历 |
| HF-02 | open |  | “上游 = 字段扫描产出的假设目录”不准：目录由 agent 按 §3 手写，字段扫描不产假设 |
| HF-03 | open |  | 三个切换信号：α≥10K（量化）、“90 条模板会话已见顶（news12 Fitness≈0.42）”（个例数字）、“论坛高赞自动化流程…已把模板空间挖到天花板”（无法度量），而  |
| HF-04 | open |  | 新产物 `data/field_semantics/*.yaml`（`anchor_only` 等）与 RA 闸 SEM 的 `s1_semantic_<ds>` 台账（signa |
| HF-05 | open |  | 示例窗口用 20（非标准窗口，CLAUDE.md 要求 1/5/22/66…，RA 预闸会别名 20→22）；`control_constant` 的内容是 `volume` 的  |
| HF-06 | open |  | 12 类假设与 `concept-taxonomy-map.md`（只映射 10 类，缺 `under_reaction`、`event_conditional`）不一致 |
| HF-07 | open |  | “`run_hypothesis_round` 派发一个实验=4 条 alpha”，节点说明写“**实跑纯本地构建、不触平台**”——所以这一步只产**计划**；此后怎样入库、过闸 |
| HF-08 | open |  | 判定四态（rejected/partially_supported/supported/needs_refinement）是**又一套 verdict 词汇**；“伪信号（主 Sh |
| HF-09 | open |  | 台账位置两处不同：`data/hypothesis_ledger/<session>.jsonl`（§6）与 `tracking/hypotheses/ledger.jsonl`（ |
| HF-10 | open |  | “字段质量先验（alphaCount/userCount）仍作种子排序依据”——**饱和数据集里的高使用字段最易撞 prod 墙**（RA 步 3），与 FQ-01 同源冲突 |

## HP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| HP-01 | open |  | description 与职责边界自称“**只读**查阈值、解释为何不过闸；不产生表达式、不回测、不改候选”，正文却含两条执行性规则：L73“提交纪律：先看 IS 阶段该闸状态，W |
| HP-02 | open |  | 阈值只有“平台默认值”一列（Fitness D1>1、Sharpe D1>1.25、Turnover 1–70%）。本库**实际闸线更严**：`GATES_INTERNAL` Sh |
| HP-03 | open |  | 一句话塞了三件事：检查工具（`get_alpha_details`）、**配额读取方式**、**工具移除史**：“提交配额从 submit 响应的 `REGULAR_SUBMISS |
| HP-04 | open |  | Fitness/Sharpe 的 Delay-0 / Delay-1 两列并列，但本战役几乎全是 D1，未说明“取哪一列、delay 从哪读（`settings.delay`）”。 |
| HP-05 | open |  | “对流动性/非流动性股票分别做 decay”在 §2 与 §5 各出现一次而无表达式；reference L166 的示例 `ts_decay_linear(s,5)*rank(v |
| HP-06 | open |  | “改进建议：使用中性化…”后紧跟缩进注释“⚠ 2026-09-01 实测修正：中性化对本闸无效”——先给一条错建议再在注释里撤回，只读要点行的人会照做；同时该节标题“Weight  |
| HP-07 | open |  | 🟢 因果链完整（见总评）。P2：①证据仅来自 **IND/TOP500 的分析师修正族**，小标题却是通用的“★ 实测要点”，未标适用范围与置信度（n=4，其中 2 例 FAIL） |
| HP-08 | open |  | “IS 阶段 WARNING 的 alpha 提交后必 FAIL … WARNING 就别提”是**提交纪律**，且已有唯一实现：`config.check_counts_as_f |
| HP-09 | open |  | Sub-universe 只给公式与两条泛泛建议（“避免市值相关乘数”“分别 decay”），缺：①平台检查名 `LOW_SUB_UNIVERSE_SHARPE`；②数值例：TOP |
| HP-10 | open |  | 标题 Self-Correlation，“要求”是 **SELF**（与自己已提交 alpha 的 PnL 相关 <0.7），“改进建议”整段讲的却是 **PROD**（`GET  |
| HP-11 | open |  | “`check_correlation`… **依赖 Redis（本环境不可用）→ 易「等死」**”与代码不符：Redis 只是**可选缓存**（`brain_mixin_tran |
| HP-12 | open |  | SKILL 版 SELF 判据只有“相关 <0.7”，漏掉平台的第二条通过路径——reference L175：“Or Sharpe at least 10% greater th |
| HP-13 | open |  | “通用建议”三条都是 USA/D1 口径且与全库规范冲突：①“选择 TOP3000（USA, D1）”——KOR TOP600、EUR TOP2500 等；本 skill 的“FA |
| HP-14 | open |  | 上游句同时写真相源（`backtest_results` 表）与文件回退（`simulation_status.csv`），未说何时用回退；“S4 链首步”用 S-label，全库 |
| HP-15 | open |  | **资格线模型已过期**：文中“对照区域 `thresholds.json` 的 `mode_b_qualification`（缺省 sharpe≥1.25 且 fitness≥0 |
| HP-16 | open |  | 第 1 条“未达标 → 判死（dead_end 回写 + wave 台账 closed，**勿送 near_pool**）”与第 2 条“快达标因子（S≥1.0 且 prod co |
| HP-17 | open |  | 🟢 playbook 的“先诊断 → 三轴按成本递增 → 有数值的判死规则 + 反例表 + ‘不再调参’的止损线”是全库最好的决策树。P2：①判死范围写“家族判死”，但证据全来自  |
| HP-18 | open |  | “Turnover and Drawdown … (e.g., low turnover **< 250%**)”与同文 L131 “1% < Turnover < 70%”直接冲 |
| HP-19 | open |  | 63 行“想法层通识”（idea sources、arXiv、ATOM、6 种字段探测、社区模板、官方例子）与提交测试阈值无关，且与 optimization-v1 Mode B、 |
| HP-20 | open |  | ①arxiv 脚本路径 `wq-brain-alpha-optimization-v1/scripts/arxiv_api.py` 无根前缀（checker 判 MISSING；库 |
| HP-21 | open |  | 缺一组“症状 → 根因 → 动作 → 验收”情景卡。建议 5 张：①Fitness 不过但 Sharpe 过（→ 看 turnover 是否 >25%，`ts_decay_line |

## IR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| IR-01 | open |  | description 442 字，含“不要用于增强模板”——“增强模板”“raw template”在全库其它处没有定义；“创建 alpha 列表”触发与 sim-alphas  |
| IR-02 | open |  | 铁律：`alpha_list.json` 等**不得当交接真相源、Agent 禁止 Write**；而本 skill 的输出与下游明写“`alpha_list.json` 交 si |
| IR-03 | open |  | 设置决策有三种口径：blockquote“人工设置决策环节已删除，仅两个职能”；职责边界“产出**设置计划**（universe/中性化/decay/truncation/maxT |
| IR-04 | open |  | “上游 = GEM 产出的 `*_idea_*.json`”，但 GEM 节点已直接把表达式落 `expressions` 表；`build_alpha_list.py` 直写同一 |
| IR-05 | open |  | 凭据来源再增 3 种：`BRAIN_USERNAME/BRAIN_EMAIL`+`BRAIN_PASSWORD`、skill 内 `config.json`、`~/secrets/ |
| IR-06 | open |  | “先 `cd "path/to/…"`”是占位；产物落在 skill 目录下的 `processed_templates/<filename>/`（skill 树内写文件，GEM  |
| IR-07 | open |  | 可选字段默认值：`nanhandling`(**OFF**)、`maxtrade`(**OFF**)、`testperiod`(P0Y0M0D)；而战役 `settings.jso |
| IR-08 | open |  | “中性化必须始终选一个有效选项（**不能为 None**）”，而 datafield-exploration 要求字段探测用“**Neutralization: None**” |

## IX

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| IX-01 | open |  | 头部称“本文件是全部 WQ/BRAIN skill 的架构基准……修改任何 skill 前先读本文件”，但 428 行里混了 ≥6 类内容：架构/路由（分层、阶段表）、契约规范（f |
| IX-02 | open |  | “唯一权威副本 = 仓库 `Claude/skills/`”，而同节 L27–29 的运行时解析顺序是 `WQ_VALIDATOR_DIR/WQ_TOOLKIT_DIR → ~/. |
| IX-03 | open |  | “`$WQ_PY` 定义（本机**单一事实源**）：`<repo>/world-quant-brain-mcp/.venv/Scripts/python.exe`”，bash 版同 |
| IX-04 | open |  | 持久化铁律“禁止 Write / Copy-Item 战役 json/csv……当真相源；静态配置与凭证、CLI 临时 `@file.json`、BRAIN 原始 CSV 仍用文件 |
| IX-05 | open |  | 🟢 表格式（region / profile / 战役目录 / entry_verdict）+“新增/删除区域须同步四处”+“代码 14 / profile 11 / 口头清单各异 |
| IX-06 | open |  | 分层图 L0–L7 与阶段表 S0–S6 **数字一一对应**（L0=S0…L6=S6，L-RA/L-PRE/L-TOOL 为编排层）却用两套名字；frontmatter 写 `l |
| IX-07 | open |  | “外部扩展区迁入记录（2026-08-23 完成）”是迁移日志：`~~brain-alpha-orchestrator~~` 删除线行、“通用非 WQ 元技能不进入本目录”“历史  |
| IX-08 | open |  | ①S5 行“`tools/submit_verdict.py`（**提交层唯一权威**）”与 RA L681“提交层唯一权威**不是** submit_verdict”、submi |
| IX-09 | open |  | 引擎映射行夹带实现细节与历史：S2“`build_wave.py` 只做去重/分桶/骨架配给”与 toolkit SKILL 的 `linear_mix≤50%` 骨架配给并存（T |
| IX-10 | open |  | 标题“闸门阶梯（**唯一基准表述**）”，称数字唯一事实源是 `config.GATES/CONCURRENCY`（核对：`GATES`、`GATES_INTERNAL`、`GAT |
| IX-11 | open |  | “gate.py 闸编号（权威 = gate.py 模块头）”表列闸0–闸8，并称“**不要再用第三种口径**”。核对 `gate.py`：模块头同样只有闸0–8，但代码里另有 * |
| IX-12 | open |  | “MCP 工具/节点计数（唯一基准）”里嵌 7 条 ⚠ 变更史（49→43→45→44；18→17→18→19→18→19），且**顺序混乱**（“2026-09-26 移除 1  |
| IX-13 | open |  | “2026-09-19 挖掘流程优化落地”与“2026-09-15 接线修复”是两段**功能变更日志**（15 条），含环境变量 `WQB_GLOBAL_SLOTS`（缺省 7）、 |
| IX-14 | open |  | “分工声明”重申“Mode B（默认入口，70%）/ Mode A（30%）……两者都失败 >10 种结构才转向换数据集”——70/30 与 “>10” 是 OP-02 的不可度量 |
| IX-15 | open |  | 🟢 “权威版本声明”把嵌套副本的**真实角色**写成 4 条可测纪律（内嵌 `scripts/` 是硬依赖不删不改；内嵌 FI/SKILL.md 必须与顶层逐字一致并由测试守护；内 |
| IX-16 | open |  | “并发口径（演进注记）”：旧 C=5（2026-07 前）/ 新 Token-Bucket C≈7（**引 `wq-backtest-monitor` §6**）/ 七槽填槽（** |
| IX-17 | open |  | 命名规范附 7 行“旧名（禁用）→ 现名”改名表（迁移日志），同时声明“旧名禁止在任何文档/代码/引用中再出现”——旧名出现在此表本身（自相矛盾），也使机械扫描需为本节开白名单；“ |
| IX-18 | open |  | frontmatter 规范：必需 `name/layer/description/last_verified`，可选 `version/user-invocable/allowe |
| IX-19 | open |  | “职责边界”由 `test_skill_boundaries.py` 守护——**守护的是该段存在且有三条（形式），不是内容为真**。本次审查中至少 6 个 skill 的边界声明 |
| IX-20 | open |  | 🟢 表头（产物 / 唯一正式写入方 / 只读消费方 / 刷新失效责任 / 逃生阀）是好设计，`priors_snapshot_<region>` 行含事故动机与“stale 仅 W |
| IX-21 | open |  | 质量门禁三条命令 + 7 项校验，但：①“无已废弃路径引用（`.qoder/skills/` 等）”**未覆盖 reference.md**（selfcorr-quick 的 re |
| IX-22 | open |  | 提交配额口径整段是**第 4 次**完整重述（submit-alpha ×2、superalpha、INDEX S5 行、此处）。本段是全库**唯一正确**处理 `activiti |
| IX-23 | open |  | “2026-09-19 平台区域硬事实（当日实测，优先级高于任何旧记）”是**带日期的区域事实**（ALL/AMR 选项、JPN 无 pv1、IND robust 闸定义与破墙配方 |
| IX-24 | open |  | 作为“路由文件”，缺**任务 → skill 的场景路由表**：用户说“提交 alpha”应命中谁？（submit-alpha / superalpha / judge 三个 de |

## JD

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| JD-01 | open |  | description 首句“（参考层·非提交判定）”，末句却写“……或**在明确确认后提交**时使用”与英文触发语 “Before submitting a Regular or |
| JD-02 | open |  | 同一条边界写了 **5 次**：职责边界（L25–27）、“三职能…存活的全部价值”（L31–37）、弃用声明（L41）、衔接协议（L52）、确认规则/提交路由（L238–250） |
| JD-03 | open |  | **同文件自相矛盾**：L42–44“`GET /alphas/{id}/submit` **恒返回 404**；提交层 403 分支是死代码；唯一真闸 = 确认后 POST 三态 |
| JD-04 | open |  | 提交后翻转延迟三个数：“~40 s 内翻 OS/ACTIVE”（L46）、“等 **4 分钟**后补发”（L114）、submit-alpha“2~3 分钟”；“受理后再次 POS |
| JD-05 | open |  | robustness 与 judge 对照表（核心问题 / 判定性质 / 关注指标 / 数据源 / 是否改表达式 / 输出）结构清晰（🟢），但：①judge 被标“**决策性**（ |
| JD-06 | open |  | “V1 当前包含 20 篇……长超时本地恢复扫描后，剩余 0 条内置搜索快照条目”是**建库过程说明**，非适用范围；篇数已漂移：`data/forum_corpus/` 与 `i |
| JD-07 | open |  | “凭据前置”规定读取顺序：`configs/config.json`（含明文 `username/password` 字段）→ 环境变量 `BRAIN_USERNAME/PASSW |
| JD-08 | open |  | “闸门顺序”六步没有输入/命令/产物：①“确认 alpha 在基线上可提交”本身是判定（与“不作判定”冲突）；②步 2“若为 PPA（或标签含 PowerPoolSelected） |
| JD-09 | open |  | PPA 附加闸门与代码/规范不符：①**颜色**：“标签必须含 PowerPoolSelected；颜色为 **GREEN**”，但 `alpha_properties.COLOR |
| JD-10 | open |  | LLM 决策层：①“Agent 模式：直接使用当前 AI 会话产出 LLM 判定”与“judge 可调用 LLM”——在 agent 会话里 LLM 即 agent 自身，“调用” |
| JD-11 | open |  | “建议必须引用语料/标准证据（帖子 ID 或规则 ID）”“REVIEW/BLOCK 至少 3 条具体行动”：①语料是 21 篇静态论坛帖，许多合理建议（“换数据集”“错开 dec |
| JD-12 | open |  | 🟢 trend score 字段定义完整（`N/A/P/P_max/S_A/S_P/S_H`；`diversity_score=S_A×S_P×S_H`；仅 `stage=OS`、 |
| JD-13 | open |  | CLI 段：①PowerShell 语法（`Set-Location`、`Get-ChildItem`）+ 裸 `python scripts/judge_alpha.py` +  |
| JD-14 | open |  | ①“确认规则（已简化：本 skill 不执行提交）……`--confirm-submit` 已废弃，勿再用”——但 `scripts/judge_alpha.py` **仍保留 ` |
| JD-15 | open |  | 点塔优选整节是 submit-alpha L196–233 的**第二份拷贝**（三层口径、A/B/C 档、过度提交、UNKNOWN 处理、`GET /data-fields`、` |
| JD-16 | open |  | 同 SB-16/SB-17：“候选将点亮哪座塔”UNKNOWN 无算法；`GET /data-fields/{field}`“列表接口带 search 返回 Invalid que |
| JD-17 | open |  | “独立原则：将本 skill 视为自包含；仅从本 skill 目录导入；vendor/ 放运行时辅助；不要依赖 `untracked/`、`untracked/APP/`”是**给 |
| JD-18 | open |  | references 5 个文件中 `improvement-roadmap.md`（73 行）与 `future-improvement-guide.md`（179 行）是**规 |
| JD-19 | open |  | 缺三张情景：①**PPA 候选**（Sharpe 1.2、PPAC 0.42、主题当期匹配）——按现规则 BLOCK，按 PPA 口径应放行：写明用哪套口径；②**多候选点塔排序* |

## LB

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| LB-01 | open |  | 阶段定位三说：“S0 前”“结论只作 **S1** 输入”“在 **S2** 候选设计之前”。且它服务的是 Labs 的 Python alpha，而 RA 流水线只产 FASTE |
| LB-02 | open |  | 链接文字 `reference/…` 而目标 `docs/reference/…`（仓库根路径，skill 目录内不存在），同步到其它宿主目录后断 |
| LB-03 | open |  | 第 4 步“在 Brain Labs 里运行该脚本”只能由**人**在浏览器完成，全文没有标出“此处暂停等用户回传 JSON”；第 2 步“配额告警后已获批准”未定义（哪种配额？谁 |
| LB-04 | open |  | `labs_output="/tmp/…"` 是 Linux 路径（工作区为 Windows）；第 7 步写 `tracking/runs/*.json` 与“DB 唯一事实源、禁 |
| LB-05 | open |  | “返回接受/拒绝的机制及对 Python alpha 的启示”——无输出格式 |
| LB-06 | open |  | `rtk python3 …`（“本机沙箱代理运行器”）只存在于作者环境，同一行又说“无 rtk 用 `$WQ_PY`”；与 AGENTS.md“用 venv python”不一致 |
| LB-07 | open |  | “下游 Python alpha 设计禁止用 VECTOR/GROUP 字段”与 RA/GEM（VECTOR 用 `vec_*`、group 用 `group_*`）口径不同，未说 |
| LB-08 | open |  | “体检数据包是 2012–2021 离线快照”与 RA 使用的 `WebData_20260219` 快照不符；“`check_expr_against_inspect`”函数在  |
| LB-09 | open |  | 默认示例给了字段、角色（主信号/上下文）与倾向（状态切换/意外抽取优于水平值）及条件 |

## ME

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| ME-01 | open |  | frontmatter 缺 `allowed-tools`，description 无“当…时使用”触发句（只有用途描述）；其余 skill 均有 |
| ME-02 | open |  | “先收回回测、完成 S4 与 **`s6_verdict_<wave>` 回写**，再调用本技能”“结构化结论仍经 wqb-db 回写 **`s6_verdict_*`**／reg |
| ME-03 | open |  | “单次失败只约束『字段搭配＋结构＋设置』，不能据此判死整个字段或数据集；推翻旧经验须提供新证据”——**判死粒度**的最清晰表述 |
| ME-04 | open |  | 干跑→实跑→`workflow_task_status`；省略 wave/dataset 的语义、D1 战役传 `--delay 1`——具体、可执行；RA 步 9 写 `str( |
| ME-05 | open |  | “核对仓库文件的波次和行数，不能只凭任务 succeeded 判定”——好规则，但没给**期望值**（应出现哪些波号、哪一块被替换） |
| ME-06 | open |  | 人工复盘 5 条都是分号串起的长句，且没有提供**自动生成文件的骨架**（各级标题、块外应写在何处），读者不知道“块外”的具体位置；“一次纠错复验的边界见主流程链接的选波清单”—— |
| ME-07 | open |  | “缺失写未核实，不拼接不同候选最好指标”“有测量缺陷的比较不写成机制有效/无效的证据”——反 cherry-pick 护栏 |
| ME-08 | open |  | `research_leads_w<W>` 是一个新 ledger 键，未登记于 ledger-schema |
| ME-09 | open |  | `tools/dataset_experience.py --waves` 被检查器判“flag 缺失”是**误报**（flag 在 `src/wqb/research/datas |

## NM

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| NM-01 | open |  | 只写“日报/早报/状态检查”，但 §5.5 是 RA 用来“选区/转区”的区域态势；用户说“哪个区更值得挖”不会命中本 skill |
| NM-02 | open |  | 边界句说“本 skill 不选字段、非流水线前置”，但 ra-pipeline 把它当**分支终点**（步 1 失败→“转 next-move 选新区域”；停止规则→“转 next |
| NM-03 | open |  | 又一次把“S0 体检白名单由 `wq-brain-ppa-mining §1.0` 产出”（PPA 专用方法论当全体 S0） |
| NM-04 | open |  | 唯一一句无方法：缺“输入（哪些表/工具）”“如何得出金字塔缺口”“建议的固定格式”“必须遵守的约束”。且 §5 建议用 `get_pyramid_multipliers`“金字塔定 |
| NM-05 | open |  | “IS/OS 表现”没说范围：全部？最近 N 天？Top N？reference 写 `limit 30, offset 0`（无排序说明）——3 万条 IS 库存里取任意 30  |
| NM-06 | open |  | “首选 `region_status.py`”后又说“手动查询仍可按下列口径执行”并称“下述判据即其实现口径”——文档复述了代码逻辑，两份实现必漂移；区域清单写死“USA/EUR/ |
| NM-07 | open |  | “≥10 且风格同质→`prod_saturation: likely`”与 campaign-matrix、USA profile 是**第三份拷贝**，“风格同质”无判据；“p |
| NM-08 | open |  | 好：有固定输出表。缺：“达标数”是 `sharpe≥1.58` 的宽口径，而 RA 的选区先验用严格口径（`ra_failed_checks` 为空）；“建议动作”四选一的判据没有 |
| NM-09 | open |  | 用一段话定义了 `entry_verdict` 三态的**默认行为**（active 默认继续；probe-only 默认不开战役；frozen 仅报状态）——这正是 ra-pip |
| NM-10 | open |  | 维护警示“注册名含大写 S…勿再改”属开发者备注 |
| NM-11 | open |  | 叙事体（“帮助秘书接手”“请随时与前任秘书联系”），对 agent 无指令价值；示例日期 2025-08-09、GAC2025 已过期 |
| NM-12 | open |  | “获取当前时间，running `get_ny_time.py`”——脚本不存在（机械检查 MISSING），且与 L99“使用系统日期动态获取”并存；日期错则事件过滤全错 |
| NM-13 | open |  | 与 SKILL 不一致：reference 是 0 摘要/1 基本信息/2 平台/3 比赛/4 活动/5 建议/6 Alpha；SKILL 是 0 摘要/1 平台/2 比赛/3 事 |
| NM-14 | open |  | ①要求“`authenticate` 提供用户的电子邮件和密码”——`authenticate(email, password)` 确实收明文，但 AGENTS.md 规定凭据只在 |
| NM-15 | open |  | “IS = 正在回测的 alpha”“OS = 最近成功提交的”语义不准（IS=样本内阶段的 alpha，OS=已提交）；`get_alpha_yearly_stats` 在同一行 |
| NM-16 | open |  | “善用论坛”（与 RA“论坛默认不查”冲突，且无具体工具）；“`todo_write`”是某宿主专有工具 |
| NM-17 | open |  | 错误防范里只有 GAC 一个**具体场景**（好）；“数据解读错误/输出格式错误/持续改进机制”是空泛口号 |

## NS

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| NS-01 | open |  | 6 桶的**名称与定义没有写在 SKILL 里**（只出现“Event / Dispersion / Propagation 三桶高优先”），依赖 `docs/reference/ |
| NS-02 | open |  | R/A/V/M/T 的 “M” 与 motif “M1–M6” 同字母；“M4 → surprise **或** change”未说何时取哪个 |
| NS-03 | open |  | “冷启动任务路由到 **Tier A**（fieldCount≥50 且 alphaCount/fieldCount≤5 且 pyramidMultiplier≥1.2）：news |
| NS-04 | open |  | `wqb news-refresh-portfolio` 命令**不存在**（同 AR-12） |
| NS-05 | open |  | “Tier B 已饱和——挖掘前必须向用户标注”只有告知，没有“告知之后怎么办”的分支（继续/放弃/换结构） |
| NS-06 | open |  | 多个日期括号（2026-04-21/23）和数据快照（120K α 等）未标失效条件 |

## OP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| OP-01 | open |  | description 承诺“**把 PROD 相关性压到 0.7 以下**”；RA 步 5b 明令“家族首探 prod ≥0.7 → 记 dead_end 换机制，**不做任何去 |
| OP-02 | open |  | “Mode B 70% / Mode A 30% 精力”在 RA 步 7、D11、ra-campaign-prompt 2.3 也被引用，含义各异（时间？模拟配额？变体条数？）；同 |
| OP-03 | open |  | B1–B5 每步给“5–10 min”式时间预算——这是给人的节奏，agent 无意义；B1 两行都是 `get_alpha_details` |
| OP-04 | open |  | arXiv 概念检索用 `scripts/arxiv_api.py --concepts --llm`，走 **DeepSeek** 概念层，凭证在 `scripts/.arxiv |
| OP-05 | open |  | “旧文写的 `create_multiSim` 不是真实工具名（2026-09-26 审计）”为文档改错史 |
| OP-06 | open |  | 硬规则 7 与工作流 8：回测后“立即以 UTF-8 追加模式把本批结果写入**指定的文本文件**”——与 DB 单轨（回测结果已由 harvest 入 `backtest_res |
| OP-07 | open |  | “operatorCount>8 的候选无效”“平台是最终裁判”——**算子≤8 是 PPA 的限制**；REGULAR 无此上限（GEM 过闸样本 p90=12 个算子），rob |
| OP-08 | open |  | “Stage A 阶段禁止纯微调”——Stage A 在全库只在 toolkit 探针里有定义（Stage A/B 探针），此处未定义 |
| OP-09 | open |  | Mode A/B 的变体只经“本地 `validate_expression` + verifier”就直接 `create_multi_simulation`，**没有经过 `w |
| OP-10 | open |  | “陷阱”里含 SuperAlpha 构造，与优化陷阱无关；EVENT/`winsorize` 条重复 datafield-exploration |
| OP-11 | open |  | 🟢 仅就**写法**而言：触发线 → 动作 → 卡点→`boost_dim` 映射五行，**触发条件→动作**清晰；**内容已过期**——资格线的数值与“未达线一律判死”已被 `m |
| OP-12 | open |  | 构造纪律明确（主腿冻结、辅助腿 ≤2 且取自 salvage_pool、禁加权/权重网格、溯源标记）——**是 RA-90 缺的“辅助腿入场”答案**。但合规判据仍是“成品须能用一 |
| OP-13 | open |  | 说明 salvage_pool 由 `review_wave.py --write-ledger` 自动入池（S≥1.0 且 prod<0.5）；RA 用 `min_sharpe= |
| OP-14 | open |  | “过拟合与稳健性测试”四项与 `brain-alpha-robustness` Phase C 大量重复但**阈值不同**（子宇宙：此处 sharpe>1、fitness>0.7、 |
| OP-15 | open |  | “`tools/submit_verdict.py`（提交层**权威**判定）”——第 5 处“权威”字样，与 RA L681“提交层唯一权威不是 submit_verdict”冲 |
| OP-16 | open |  | 预期产出把 Turnover 写成“1%–40%（内部目标 ≤40%）”；全库换手区间现有：平台 1–70%（config）、内部 5–20%（config）、D0 “5–20%” |
| OP-17 | open |  | “持续迭代直到至少一个候选满足全部条件”是无终止条件的循环（与 3–5 周期/10 种结构上限矛盾） |
| OP-18 | open |  | “触发线：本 alpha 必须已过 `mode_b_qualification` 资格线（sharpe≥1.25 且 fitness≥0.8，以区域 `thresholds.jso |

## PB

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| PB-01 | open |  | 导入外部 skill = 向运行时注入**指令与可执行物**，本 skill **没有任何入库前审查步骤**：不列 `hooks` / `allowed-tools` / `scr |
| PB-02 | open |  | “首选推荐”的示例 1 默认带 **`--overwrite`**；脚本对已存在目录先 `shutil.rmtree(dest_folder)` 再复制——**无备份、无确认、无  |
| PB-03 | open |  | **文档与代码默认目的地相反**：SKILL 写“`--dest` 默认 = 仓库真相源 `Claude/skills/`（导入后须跑 `sync_skills.py`）”，而 ` |
| PB-04 | open |  | ZIP 地址“在仓库 URL 后追加 `/archive/refs/heads/main.zip`”：①假设默认分支是 `main`（`master` 仓库 404）；②分支头是* |
| PB-05 | open |  | “有效 skill”只要求“顶层文件夹里有 SKILL.md/skill.md”，比本库契约（name==目录名、layer、last_verified、职责边界段、kebab-c |
| PB-06 | open |  | “导入后必须人工归层并跑 `python tools/sync_skills.py` + `pytest tests/unit/test_skill_integrity.py -q |
| PB-07 | open |  | 缺三个情景：①从 GitHub 仓库导入 1 个 skill 到审查区并生成审查报告（含 hooks/allowed-tools/scripts 清单）；②导入的 skill 与现 |

## PP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| PP-01 | open |  | 466 字；触发含“WorldQuant / WQ Brain / alpha 挖掘 / 用户要开新战役·换区域·问某数据集能不能打 → **必须先执行 §1.0**”，会被**所 |
| PP-02 | open |  | 边界句声称负责“**PPA 主题匹配核查**”，全文找不到这一节（主题门禁实际在 RA 步 1 的 `get_messages` 扫描、`worldquant-submit-alp |
| PP-03 | open |  | 大量步骤写成“读 hover 卡片 / 读徽章 / distribution.js 白空间表 / genius.js 算子分析”——这是 **Chrome 扩展的 UI 操作**， |
| PP-04 | open |  | 体检执行器**三套**：本 skill 的 `scripts/dataset_health_check.py`（§1.0、§7 步 0 都要求“不可跳过”）、boundary 里写 |
| PP-05 | open |  | ①cov 阈值有 0.85（硬门）、0.7（一票否决）两档，而 D4/代码用 0.65（文档）/0.7（代码缺省）、保底带 0.65–0.85；②“`alphaCount==0`  |
| PP-06 | open |  | EUR 32 次回测教训有数据、有反事实，是好范式；但“若前置则完全可避免”的反事实后来未被验证（ac=0 集实测多为伪白空间） |
| PP-07 | open |  | 标题“规则引擎（从台账自动推导，**无需硬编码**）”，随后表内硬编码 KOR/MEA 区域特征与 6 组“当前已知红灯”（图表形态、新闻/情绪、AI/ML、信用风险、行为金融、G |
| PP-08 | open |  | “sweet-spot：100 ≤ count ≤ 3000 且 sharpe ≥ 1.1×均值”与本文 §1.0 的 alphaCount≤50、toolkit calibrat |
| PP-09 | open |  | 同一 skill 内：“KOR → SECTOR 最佳（0.562）”“按 dominant method（KOR→SECTOR）”与“SECTOR/MARKET 中性化大幅降低  |
| PP-10 | open |  | “离线包缺≠平台缺；离线包有≠平台有”+ EUR 四个集根本不存在的反例 + 规则“先体检确认存在且达标，判‘不可用’前换区查一遍”——**场景→规则→动作**齐全 |
| PP-11 | open |  | “IS sharpe >> OS sharpe”用“>>”，无量化（field-quality 用“差 >0.15”）；对 KOR `model253` 的引用是个例 |
| PP-12 | open |  | 表里“极低(<30%) → **加 `is_placeholder`** 或换字段”——`is_placeholder` **不是 BRAIN 算子或字段**（仓库只有内部函数 ` |
| PP-13 | open |  | “组合范式（V9 突破版）”：`scale(rank(ts_zscore(subtract(...),189))) + scale(-rank(ts_zscore(returns, |
| PP-14 | open |  | §3.1 把 KOR 的 **Sentiment/Option/Macro 空白**列为“真·低竞争机会（重点）”，而 §1.0.x 把 KOR 新闻/情绪族列为**三连判死红灯* |
| PP-15 | open |  | 鼓励“补进极少使用的算子（如 `ts_regression`…）以满足 Genius 六维”，而 §5.9 又说 `ts_regression(A,B,n).residual` 语 |
| PP-16 | open |  | “并发上限 **C=5**”出现两次，而 `config.CONCURRENCY.slots=7`（config 注释还专门记录了历史上 5/8/6/4/3 并存的问题）；D10  |
| PP-17 | open |  | testPeriod 三个值并存：示例 `P0D`、最佳参数 `P6Y`、“最大 P6Y0M0D” |
| PP-18 | open |  | hump：“破坏性，**勿用**”（§5.7）与“`hump(x, hump=0.01)` **必须命名参数**”（§9）并存；D6 称“已废弃禁用”，RA 预闸却自动改写 hum |
| PP-19 | open |  | 把 “Margin > 5bp、Returns > 5%” 列为**平台硬线**；`config.GATES_PLATFORM` 没有这两项，`GATES_INTERNAL` 是  |
| PP-20 | open |  | 步 4“建 reversed spread，加 returns 反转组合”＝PP-13 的混合；步 5“**权重**/窗口/中性化/truncation 微调”＝参数扫描，与 CL |
| PP-21 | open |  | “**提交**：`tags=["PowerPoolSelected"]`, `color=GREEN`”——`worldquant-submit-alpha` / `brain-a |
| PP-22 | open |  | 2026-08-05/23 的区域快照（KOR 192 集、EUR 178 集、HKG 209 集；“首选 `news_sentiment_nlp`：三区 alphaCount=0 |
| PP-23 | open |  | “自行实现 `_reauth()`”与“禁止手写 requests、用 `BrainApiClient`”冲突；429 退避写了第三种（`min(20+attempt*8,45)s |
| PP-24 | open |  | 合法 universe 表仍含 `ILLIQUID_MINVOL1M`（USA/EUR/ASI）；`config.REGIONS` 注释：2026-09-22 已从 USA/EUR |
| PP-25 | open |  | 两份 PPA 方法论（24 段重复，Jaccard 0.50）；ra-pipeline 版还引用不存在的 `wq-brain-ra-pipeline/scripts/dataset |
| PP-26 | open |  | 六条实测约束（数据集级体检走 `get_datasets`；`/data-fields` 四参齐全；非法 universe 报 500 而非 400；TLS 抖动优先复用常驻 MC |

## PW

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| PW-01 | open |  | frontmatter 内嵌 4 类 shell 钩子：SessionStart / PostToolUse 的 `echo`；PreToolUse（匹配 `Write\ |
| PW-02 | open |  | 触发条件三个口径：description“需要 **>5 次工具调用**的任务”、正文“多步任务（**3 步以上**）/任何需要组织规划的任务”、SessionStart 提示“A |
| PW-03 | open |  | “两动作规则”（每 2 次查看/浏览/搜索就写文件）与“**永不重复失败**：`if action_failed: next_action != same_action`，绝不重复 |
| PW-04 | open |  | “规划文件应创建在项目目录（当前工作的文件夹）”：WQ 仓库 `.gitignore` 只忽略**仓库根**的 `/task_plan.md`、`/findings.md`、`/p |
| PW-05 | open |  | “3 次失败后：上报给用户”与 RA 停止规则 A/B1/B2、optimization-v1“>10 种结构 / 3–5 周期”、monitor“>10 种结构才转向”、subm |
| PW-06 | open |  | 🟢 读/写决策矩阵与“五问重启测试”是全文最可执行的部分，直接对应“压缩后恢复”；表述短、判据明确（“刚写完文件 → 不要读”“间隔后恢复 → 读取所有规划文件”） |
| PW-07 | open |  | 脚本为 bash（Windows 主宿主需 Git Bash/WSL，未说明）；模板阶段是软件开发通用阶段（“Requirements & Discovery / Planning |
| PW-08 | open |  | 反模式“用 TodoWrite 做持久化 → 创建 `task_plan.md`”：宿主提供 Task 工具（TaskCreate/TaskUpdate）并要求维护任务清单，二者是 |
| PW-09 | open |  | `version: "2.1.0"`（外部来源版本号，与本库“内容版本递增”的关系未说）；来源、许可与上游同步策略未标（疑为外部开源 skill 的中文化）；`user-invoc |
| PW-10 | open |  | 缺三个 WQ 情景：①**一次 RA 战役**的 task_plan（九步阶段 + 每步产物写 DB 的检查点）；②**长任务被压缩后恢复**：五问 → 读 task_plan → |

## RA

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RA-01 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md | description 只留整链/开战役/从零到提交/日循环触发；单点动作词让给 matrix / sim-alphas / submit，正文「分工」段写明何时调它们 |
| RA-02 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/tool-index.md | 职责边界改为「不实现能力，但规定调用顺序与判据」；CLI→步→归属表放 tool-index.md T.1；直读 sqlite 换成 MCP 或注明原因 |
| RA-03 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| AGENTS.md \| Claude/skills/GLOSSARY.md | 全库统一「否决权威 / 放行权威」两词，删除「唯一权威 = submit_verdict」；RA 正文只剩三句（UNVERIFIABLE 不是放行） |
| RA-04 | fixed | Claude/skills/CHANGELOG.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 变更史 / 过程叙述迁入 CHANGELOG：brain-deepExplore 废止说明、2026-09-26 审计补入边、脚本归档说明；正文只留正向指向 |
| RA-05 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md | 「分工」段：when/what=本 skill、where=matrix（用户没给 REGION 时先调、多区并列回问）、how=toolkit，并列出其余去向 |
| RA-06 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md | 变量表： 必填；/ 来自 settings.json；/// 各有来源； 明确为字符串 |
| RA-07 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| tools/_pyenv.py \| tests/unit/test_pyenv.py | 「MCP 应用尽用」给出判据（有对应 MCP 工具即用）；6 个 tools/*.py 接入 _pyenv，文档可写裸 python 且跨平台可解析 |
| RA-08 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md | 「复写」定义 = 拷贝 config GATES* 闸门值；区域/机制经验阈值允许但须带出处；正文字面数字下沉到 references 并带出处 |
| RA-09 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 「冲突裁决」一行：用户指令 > 代码 fail-closed > profile > 决策表 > 正文；D0-P 不接受区域改写；红线不可覆盖 |
| RA-10 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| tests/unit/test_ra_sop_template.py | 每步固定模板（目的/前置/调用/产物/完成定义/失败分支/不做/细则）由测试守；FAIL 三种含义在「怎么读」里点明 |
| RA-11 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md | 编号：正文只用「步 N」，S 编号仅在 MCP 参数处；一张对照表（步↔阶段） |
| RA-12 | fixed | tests/unit/test_region_alignment.py \| Claude/skills/INDEX.md \| Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md | 删掉硬编码的 13/14 个区域说法；三处清单（config.REGIONS / profile / tracking）由测试对齐，已知缺口显式登记（AMR 无 profile、TWN 无 tracking） |
| RA-13 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md | Profile 注入表增「谁读 / 缺失回落」两列；键的实际读取方（代码 vs 文档）写在契约文件 §1 |
| RA-14 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | entry_verdict 三态默认含义放 step1 §1.1，profile 只写差异；frozen 步 1 即拒（与「不继续步 2」统一）；probe-only 含义写明 |
| RA-15 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | step1 §1.3 写明查表用哪个 MCP 工具（get_campaign_summary/get_dead_ends/…），「以 DB 查表结果为准」指向具体工具 |
| RA-16 | fixed | Claude/skills/wq-brain-ra-pipeline/references/forum-recon-triggers.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | forum_recon 五个触发点并成一张表（触发条件、额度以「查出有效文章」为准、7 天缓存、退出码）；正文只留「默认不查，触发点见表」 |
| RA-17 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | entry_verdict 三态默认含义放 step1 §1.1，profile 只写差异；frozen 步 1 即拒（与「不继续步 2」统一）；probe-only 含义写明 |
| RA-18 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | 库存盘点给出量化分流（篮子 ≥ target 且覆盖 ≥3 座未点亮塔 → 跳步 7/8；否则只补缺口塔）；篮子口径统一为 Failed RA==0；产物写到哪（settings.json / ledger）写明 |
| RA-19 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | 库存盘点给出量化分流（篮子 ≥ target 且覆盖 ≥3 座未点亮塔 → 跳步 7/8；否则只补缺口塔）；篮子口径统一为 Failed RA==0；产物写到哪（settings.json / ledger）写明 |
| RA-20 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | 长行拆开：调用/解析字段/标签/重扫铁律/带日期快照分列；快照过期状态不再写进正文 |
| RA-21 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 不再用 LIKE '%ds%' 扫 payload（model1 误命中 model109）；跨区死路走 get_dead_ends 不传 region |
| RA-22 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | §1.5 两个比率含义分开：conversion（修管道）与 yield（换标的）；yield 是累计比值，「连续为 0」改写为「累计为 0 且已测 ≥ 100」并说明 100 = 停止规则 A 的样本量下限 |
| RA-23 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | 库存盘点给出量化分流（篮子 ≥ target 且覆盖 ≥3 座未点亮塔 → 跳步 7/8；否则只补缺口塔）；篮子口径统一为 Failed RA==0；产物写到哪（settings.json / ledger）写明 |
| RA-24 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 库存盘点转向 matrix 选区（next-move 是并行情报层，不产配置） |
| RA-25 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 步 2 调用顺序改为 s0-select → calibrate → S0 排名 → 硬约束筛 → 锁白名单 → 体检包核对；「先锁白名单后读约束」的颠倒消除 |
| RA-26 | fixed | Claude/skills/INDEX.md \| Claude/skills/wq-brain-ra-pipeline/references/ppa-mining-experience.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/ASI.md | dataset_health_check.py 只在 wq-brain-ppa-mining/scripts/（兜底体检）；INDEX、ASI profile、经验文档里的路径统一；删除「已归档到 attic」变更史 |
| RA-27 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | §2.4 给出 s0_whitelist 最小形态（universe / delay / datasets / entries）与读取一律经 wqb.ledger_whitelist.normalize；写入先读再 mode=merge，「工具产物 vs 手工锁」分开 |
| RA-28 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 体检包：缺省 warn 放行并告警；--inspect-mode off 才需 inspect waiver；标题不再写「硬前置」而实际 warn |
| RA-29 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | 快照数字（包数 / 区域计数）删除或带日期与出处，不在两处各写一遍 |
| RA-30 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | 一大段拆成：命令 / 选择增强 / 新列新标记 / 历史背景（IND 7 集 197 回测）分列 |
| RA-31 | fixed | Claude/skills/INDEX.md \| tools/README.md | INDEX 里 tools/backfill_backtest_dataset.py 指令改为「已一次性跑完并归档到 tools/legacy/」，不再是可调用入口 |
| RA-32 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | est_seats 缺省 2 给出依据，并写明与「3 颗点亮一座塔」的关系 |
| RA-33 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | 白名单约束 0–7 分「硬（代码执行）/ 准则（启发式）」两栏并写执行点；#1 候选≠白名单、#0 已点亮塔不进白名单区分 |
| RA-34 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | calibrate/score 内部函数名与历史评审问答移出；ac 缩写给出定义 |
| RA-35 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | 内部工单号（P0/P2/P3/P5/P6）不再出现在 SOP；默认 OFF 的增强只说「何时打开」，机制细节指向 toolkit |
| RA-36 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md \| Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md | findings 写哪里：wave_results.key_findings（步 9 写入契约） |
| RA-37 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step3-s1-semantic.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 步 3 把「必做（typed catalog）」与「按需（深度字段理解、禁注入 GEM）」分栏；两条必做铁律的落点写明 |
| RA-38 | fixed | Claude/skills/CHANGELOG.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 变更史 / 过程叙述迁入 CHANGELOG：brain-deepExplore 废止说明、2026-09-26 审计补入边、脚本归档说明；正文只留正向指向 |
| RA-39 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step3-s1-semantic.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 步 3 把「必做（typed catalog）」与「按需（深度字段理解、禁注入 GEM）」分栏；两条必做铁律的落点写明 |
| RA-40 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step3-s1-semantic.md \| Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md | 50/10/9/≥50% 阈值补出处；「已确认超标字段族」登记处写明；orchestrator 迁移说明移出 |
| RA-41 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step3-s1-semantic.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 步 3 把「必做（typed catalog）」与「按需（深度字段理解、禁注入 GEM）」分栏；两条必做铁律的落点写明 |
| RA-42 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step3-s1-semantic.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 「双重 fail-closed」按代码实况重写：s1_semantic_<ds> 由 wave_gate 读；GEM 侧不过滤；闸 SEM 缺省 enforce，exit 2 |
| RA-43 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step3-s1-semantic.md | 闸 SEM 起因证据（348 条 / 49.4% / 37/373）压成一行放证据小节，规则本身在前 |
| RA-44 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 体检包：缺省 warn 放行并告警；--inspect-mode off 才需 inspect waiver；标题不再写「硬前置」而实际 warn |
| RA-45 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | LLM 402 余额不足被误报成 no meta.json 90s：失败分支先查 LLM 通道、不重试；干跑假绿在同处成对说明 |
| RA-46 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md \| Claude/skills/CHANGELOG.md | 加权混合矛盾消除：已验证配方只记「信号概念 + 设置」，不再以 0.4×慢+0.6×快为配方；允许形态只有一份清单（步 7 §7.7）；slow_fast_mix 只留作 09-13 之前历史（CHANGELOG） |
| RA-47 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md | priors_file 已可省略（GEM 从 DB 快照直读），硬约束 #2 改写；两处不再矛盾 |
| RA-48 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/GLOSSARY.md | 「槽」三义拆词：并发令牌 / 波内配额 / 批；数值冲突（≥2 槽 vs ≥1 win）统一为一处；PASS_CHEAP 在首次出现处链接定义 |
| RA-49 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/GLOSSARY.md | 「槽」三义拆词：并发令牌 / 波内配额 / 批；数值冲突（≥2 槽 vs ≥1 win）统一为一处；PASS_CHEAP 在首次出现处链接定义 |
| RA-50 | fixed | Claude/skills/wq-brain-ra-pipeline/references/assemble-priors-internals.md | 按代码重写：wins/dead_ends 的真实来源与截断顺序、registry_empirical win/dead_end 层、profile 兜底范围；旧文里代码没有的映射删除 |
| RA-51 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md | assemble-priors 只在一处调用；「stage=S2 与路由无关」的答辩注释删除 |
| RA-52 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md | 伪赋值与真调用分块；build-wave 那一行加注释；pipeline 参数说明补全 |
| RA-53 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md | 自动改写 6 类（hump / bucket / 非法 group / 窗口别名 / 每骨架封顶 12 / quantile 归一）列表化：系统做什么 + agent 看到什么 + 不用再手改 |
| RA-54 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 完成定义有验证手段：list_expressions 查到本波条目，否则不得声称步 4 成功；首句补主语 |
| RA-55 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md | 13 行无编号大段拆成带编号的短规则（8 条非上限、--size 语义、清单写入 ledger、条数由清单推导…） |
| RA-56 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md | 「超时恢复清单」未定义的指向删除，改为 step6 §6.4 故障表；手写 ideas ≠ 手写表达式在步 4 区分 |
| RA-57 | fixed | Claude/skills/wq-brain-ra-pipeline/references/forum-recon-triggers.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | forum_recon 五个触发点并成一张表（触发条件、额度以「查出有效文章」为准、7 天缓存、退出码）；正文只留「默认不查，触发点见表」 |
| RA-58 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md | 两条禁令附理由与正向指向（用 wave_gate.py，结果落 gate_results） |
| RA-59 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | wave_gate 含哪些闸只在 INDEX 两张生成表（GATE_REGISTRY / waiver.GATE_POLICIES）；正文不再 5 处各写一遍 |
| RA-60 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md | 删除线原文与「已收敛」历史叙述清掉；check_batch 不再作判据 |
| RA-61 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md | 契约过期的处理顺序写成一条：过期 → 自动续约 → 用新契约重判（重判仍可 FAIL）；60% / 2/3 标注为 wave94/95/98/104 实证的经验值 |
| RA-62 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md \| Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md | 体检包由 gen_field_inspect_packs.py 生成，webdata_quality --export-expr 是另一用途，两处统一 |
| RA-63 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md \| Claude/skills/wq-brain-ra-pipeline/references/tool-index.md | MCP 与 CLI 同一实现，示例同时给节点名；ghost-audit 命令只出现一处 |
| RA-64 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md | 两条无关提示拆开；repair 批默认豁免多样性闸只在闸表一处写 |
| RA-65 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md | 闸 2b（非法 group 字段 FAIL）与预闸（丢弃）的关系写明：预闸先丢、语法闸兜底 |
| RA-66 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md | 幽灵算子命中后三种处置给出选择判据（等价替换 / preflight 单测 / 丢弃） |
| RA-67 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md | 失败分支全表：闸 SEM / 体检包 / 闸 PF / 闸 2b / 幽灵算子 / 闸 7/8 → 现象 → 动作 → 回哪步 → 能否豁免 |
| RA-68 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 闸 PF 硬/软分开：已知死骨架拦整波、新骨架 WARN；「新」= 本区台账内未见；prod-first 处置只走 D0-P |
| RA-69 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | prod 墙处置只剩决策表 D0-P 一张（<0.60 扩 / 0.60–0.70 不扩变体当天进步 8 / 0.70–0.75 一次结构性尝试 / ≥0.75 dead_end）；prod-first 定义只在核心步 5b |
| RA-70 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 闸 PF 硬/软分开：已知死骨架拦整波、新骨架 WARN；「新」= 本区台账内未见；prod-first 处置只走 D0-P |
| RA-71 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | S3 入口三处并列写明分工：workflow_batch_track（默认）/ sim-alphas（手写 alpha_list）/ toolkit pipeline（调试） |
| RA-72 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/GLOSSARY.md | 「槽」三义拆词：并发令牌 / 波内配额 / 批；数值冲突（≥2 槽 vs ≥1 win）统一为一处；PASS_CHEAP 在首次出现处链接定义 |
| RA-73 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 设置跟 win / ILLIQUID 永久停提 / QUICK-FULL / 设置层先验拆开；QUICK 产物不可提交单列为「不做」 |
| RA-74 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | prod 墙处置只剩决策表 D0-P 一张（<0.60 扩 / 0.60–0.70 不扩变体当天进步 8 / 0.70–0.75 一次结构性尝试 / ≥0.75 dead_end）；prod-first 定义只在核心步 5b |
| RA-75 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md | §6.3 第 5 条：「表达式从 list_expressions 取」与安全规则拆开、安全规则放最前；「自动」的判据 = confirm_submit=True 只在步 8 用户确认后单独调用；pipeline.py --submit / submit_batch 是派发仿真 |
| RA-76 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/S2_COMPLIANCE_GUIDE.md \| Claude/skills/wq-brain-campaign-toolkit/references/S2_COMPLIANCE_CHECKLIST.md \| Claude/skills/wq-brain-campaign-toolkit/SKILL.md | toolkit 的 S2 合规文档同步为「仅提示、不阻断、无 --force」（2026-09-15 降级）；指南 v2.0，清单末条改写，SKILL ⑥ 行加链接 |
| RA-77 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md | 历史注释（--concurrency 不存在→argparse exit 2）移到 incidents；命令块只留命令 |
| RA-78 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md \| Claude/skills/wqb-concurrency/SKILL.md | 429：并发由 pipeline 内部锁 min(7,批数)，外部传非 7 只 warning；降批大小走 §6.4 故障表；指数退避与 429 行统一 |
| RA-79 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md | 故障表「依据」列由 wave 代号改为现象描述 + 日期；「全 ERROR 重发相同表达式」与「先归因再重发」统一为先归因 |
| RA-80 | fixed | Claude/skills/wqb-concurrency/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 账户级槽位仲裁（slots.py / WQB_GLOBAL_SLOTS）落在 wqb-concurrency §8.1；RA 只引用不重复 |
| RA-81 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | 积压清理提到 campaign_intel.py backlog-drop；近闸积压、2 倍给出口径与出处 |
| RA-82 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | S4 节点内部实现细节与修复史移出；「解析不到 alpha_id 即 FAIL → 用其列出的字符串波号重试」写成 agent 动作 |
| RA-83 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | RN_EXPOSURE 只留一版：rn_sharpe ≤ rn_sharpe_min（默认 0）→ 墙，不进候选 / near / salvage / 组合腿；想法级判死另列 |
| RA-84 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | Mode B / Mode A 比例的解释与出处；未编排增强节点去留登记移到 CHANGELOG |
| RA-85 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | prod 墙处置只剩决策表 D0-P 一张（<0.60 扩 / 0.60–0.70 不扩变体当天进步 8 / 0.70–0.75 一次结构性尝试 / ≥0.75 dead_end）；prod-first 定义只在核心步 5b |
| RA-86 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md \| Claude/skills/GLOSSARY.md | 墙 / 池术语（RN_EXPOSURE、ROBUST_STRUCTURAL、PARTIAL、near、salvage、停止规则 B）在首次出现处给一句定义并链接 GLOSSARY |
| RA-87 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | S4 两套实现（review_wave 与逐候选链）并列写明分工与先后：评审在前、逐候选链在后 |
| RA-88 | declined |  | 范本，保留：说明「别拿它做什么」的语义边界写法（IS→OS 衰减校准不抬高 IS 阈值）；已原样保留在步 7 与 CHANGELOG |
| RA-89 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | 步 7 §7.7：subtract(rank A, rank B) 须同源且有单一经济含义（跨数据集由闸 5 spread_cross_dataset 拦）；等价 add(a,-b) 的漏洞按同罪处理 |
| RA-90 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | 辅助腿入场三式（条件 trade_when / 分组 bucket / 残差 neutralize）；每式的证据强度与已知局限；multiply(rank,rank) 为灰区默认不用 |
| RA-91 | fixed | Claude/skills/GLOSSARY.md \| Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md | 「路线 A」不再作术语出现；权重禁令直接写规则并指向 CHANGELOG 的 2026-09-13 条 |
| RA-92 | fixed | Claude/skills/wq-brain-ra-pipeline/references/incidents.md \| Claude/skills/CHANGELOG.md | commit 级细节（_detect_weighted_mix_structural、platform_constraints v1.5、16 条测试构成）移出正文，事故与落点见 incidents I-1 与 CHANGELOG |
| RA-93 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | prod 墙处置只剩决策表 D0-P 一张（<0.60 扩 / 0.60–0.70 不扩变体当天进步 8 / 0.70–0.75 一次结构性尝试 / ≥0.75 dead_end）；prod-first 定义只在核心步 5b |
| RA-94 | fixed | Claude/skills/wq-brain-ra-pipeline/references/forum-recon-triggers.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | forum_recon 五个触发点并成一张表（触发条件、额度以「查出有效文章」为准、7 天缓存、退出码）；正文只留「默认不查，触发点见表」 |
| RA-95 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md \| Claude/skills/wq-brain-ra-pipeline/references/incidents.md | 步 8 完成判定链改为有序清单：资格门 → submit_verdict（否决）→ prod 实测 → 用户确认 → workflow_submit_alpha；标签用真实值（SUBMITTABLE 不存在；UNVERIFIABLE 不是放行） |
| RA-96 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md \| Claude/skills/wq-brain-ra-pipeline/references/incidents.md | 步 8 完成判定链改为有序清单：资格门 → submit_verdict（否决）→ prod 实测 → 用户确认 → workflow_submit_alpha；标签用真实值（SUBMITTABLE 不存在；UNVERIFIABLE 不是放行） |
| RA-97 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/submit-chain.md | 删除「直接 POST 零成本」说法：POST 通过即真实提交；prod 一律 check_correlation；确认前禁止一切真提交入口 |
| RA-98 | fixed | Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | Failed-count 资格门口径与步 1 统一（RA 口径：WARNING/ERROR 也计）；名单以 config.RA_CHECK_NAMES 为准，文档不再抄一份 |
| RA-99 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md | 「不做」列出真提交入口全集（workflow_submit_alpha / submit_alpha 节点 / workflow_superalpha / super_build.py submit）并写明 submit_batch 与 pipeline.py --submit 是派发仿真 |
| RA-100 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/ppa-vs-ra.md | 步 8 分流三类：REGULAR → submit-alpha；SUPER → superalpha；PPA → web UI 交接（MCP 预检不够时 agent 停下，用户不在线则留在 submit_ready）；「当天优先提 PPA」只在渠道允许时成立 |
| RA-101 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md | 四态处置表在 submit-alpha 一处维护，补发已自动化的说明与等待窗口依据在该 skill；RA 只指向它 |
| RA-102 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md \| Claude/skills/wq-brain-ra-pipeline/references/incidents.md | 步 8 完成判定链改为有序清单：资格门 → submit_verdict（否决）→ prod 实测 → 用户确认 → workflow_submit_alpha；标签用真实值（SUBMITTABLE 不存在；UNVERIFIABLE 不是放行） |
| RA-103 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md | 步 9 按执行顺序写成有序清单（step_funnel → verdict → pyramid → upsert_wave_result → seal/win → mark-saturated → dataset-experience → assemble-priors）；完成定义清单 §9.7 |
| RA-104 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 调用写成真实工具名与参数（伪函数删除）；「未回写 = 本波未完成」保留 |
| RA-105 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md \| tools/campaign_intel.py | dataset-experience 范围统一为「本区域已回测的全部数据集」，Artifact 表同步；判死集另有 seal_dead_end |
| RA-106 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md | 步 9 按执行顺序写成有序清单（step_funnel → verdict → pyramid → upsert_wave_result → seal/win → mark-saturated → dataset-experience → assemble-priors）；完成定义清单 §9.7 |
| RA-107 | fixed | Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md | 「达标」三种口径分别命名并列表（停止规则 A / 严格 yield / 过全部评审闸） |
| RA-108 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 可执行块里不再出现废止命令；s6_verdict_<wave> / wave<N>_verdict 仅在「不做」与反模式里作为废止说明（skill_lint 计数下降） |
| RA-109 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 「论坛无解」措辞改为引用 D2 实际含义；软提示措辞与「须」区分 |
| RA-110 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md | seal_dead_end 是 upsert：先建（entry_id 由它返回）再补；写入顺序在 §9.1 |
| RA-111 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md | add-win / add-dead-end 换成真实命令（upsert_registry_empirical / seal_dead_end） |
| RA-112 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md | 多样性监控与 IS→OS 归因写入字段（key_findings）与触发阈值写明 |
| RA-113 | fixed | tools/campaign_intel.py \| tests/unit/test_campaign_intel_mark_saturated.py \| docs/ledger_keys.json \| Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md | S6→S0 反馈环接通：新增 campaign_intel.py mark-saturated 写 saturated_datasets（S0 评分读取）；submit_ready_blocked 降为 deprecated |
| RA-114 | fixed | Claude/skills/wq-brain-ra-pipeline/references/tool-index.md | tool-index T.1 按步给出 MCP / 节点 / CLI（judge、submit_alpha、superalpha 归步 8）；T.2 写明步 1 分流、步 7 逐候选、步 8 提交、步 9 判死封存没有单一节点或不该入链 |
| RA-115 | fixed | Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | LLM 402 余额不足被误报成 no meta.json 90s：失败分支先查 LLM 通道、不重试；干跑假绿在同处成对说明 |
| RA-116 | fixed | src/wqb/workflow/executor.py \| tests/unit/test_workflow_chain_irreversible_guard.py \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 「提交类节点不入链」由代码强制：execute_chain 拒绝带 confirm_submit=True 的 submit_alpha / superalpha |
| RA-117 | fixed | Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md | 停止规则 A / B1 / B2、signal_floor、放行协议拆成表，每条配缺省数字与数字例；会过期的状态（GBR 至 09-30）不再写 |
| RA-118 | fixed | Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md | 三套「连续 3 波」规则按对象分列（B1 同轴 closed 波 FAIL / B2 区级多轴 / gate 通过率 0），先后顺序写明 |
| RA-119 | fixed | Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md \| tests/unit/test_docs_consistency.py | signal_floor：区域数以磁盘实况为准（测试守）；不再写含 TWN 遗漏的名单 |
| RA-120 | fixed | Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md \| Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 日界 21:30 ET 与配额 00:00 ET 的区别与「NY 日」定义写明 |
| RA-121 | fixed | Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md | 配额耗尽继续步 2–9 时未提交积压的上限与路由写明；ACTIVE RA ≥10 转 superalpha 的判据保留 |
| RA-122 | fixed | Claude/skills/CHANGELOG.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | 变更史 / 过程叙述迁入 CHANGELOG：brain-deepExplore 废止说明、2026-09-26 审计补入边、脚本归档说明；正文只留正向指向 |
| RA-123 | fixed | Claude/skills/wq-brain-ra-pipeline/references/scenarios.md \| Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 快捷入口「发批」补前置：闸 SEM（缺 s1_semantic_<ds> exit 2）与体检包会拦；情景卡 RA-0x 逐一给出 |
| RA-124 | fixed | docs/time_bombs.json \| Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md | 带日期的「到期即变」文案登记到 docs/time_bombs.json（TB-01/02）；正文只在 L.3 留一处 CLI 日期说明 |
| RA-125 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md | 整链执行一节改为可读句式；「配置包」不再无定义地出现 |
| RA-126 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ppa-mining-experience.md \| Claude/skills/wq-brain-ra-pipeline/references/ppa-vs-ra.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | PPA 方法论合并：ppa-mining-experience.md 由 312 行（39/52 段与 ppa-mining SKILL 逐字重复）缩为独有实证 + 作废旧说法表；PPA 分支差异表在 ppa-vs-ra.md；删除 GET/POST 提交判定脚本 |
| RA-127 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/ppa-vs-ra.md | 步 8 分流三类：REGULAR → submit-alpha；SUPER → superalpha；PPA → web UI 交接（MCP 预检不够时 agent 停下，用户不在线则留在 submit_ready）；「当天优先提 PPA」只在渠道允许时成立 |
| RA-128 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md | Artifact 契约：战役事实源只入 wqb.db；一次性中间文件（cache/*.json、--exprs-file）可写但可丢弃 |
| RA-129 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| docs/ledger_keys.json | Artifact 表补全并指向 docs/ledger_keys.json（键的用途 / 写入方 / 读取方由测试守） |
| RA-130 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/incidents.md | 反模式每条改为「因 X 发生过 Y → 改用 Z」，补上最痛的 5 条（QUICK 进提交、无确认 POST、--skip-semantic-gate、双写 verdict、LLM 402 干跑） |
| RA-131 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| AGENTS.md \| Claude/skills/GLOSSARY.md | 全库统一「否决权威 / 放行权威」两词，删除「唯一权威 = submit_verdict」；RA 正文只剩三句（UNVERIFIABLE 不是放行） |

## RB

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RB-01 | open |  | 两个引用块置于 H1 之前，后一块（“权威性”）是关于**本 skill 副本谁为真相源**的元说明（旧说法已删），与稳健性无关，应在 INDEX |
| RB-02 | open |  | 本文自相矛盾：头部“`brain-alpha-judge` = **S5 唯一提交评审入口**（双闸评审），先过本闸再进 judge”；衔接协议与 Phase C 写“PASS → |
| RB-03 | open |  | 声明“S4→S5 **必经**闸”，但**没有任何代码读取该判定**（全仓 grep：只有 `judge.py` 注释提到；`submit_verdict`/提交节点不检查）；Ph |
| RB-04 | open |  | Phase A 要求每次运行先 `forum_cache_builder --status`，过期则手工重拉 5 个关键词包（≥30 帖）并去重写回缓存——同一段先说“统一走 `- |
| RB-05 | open |  | “若刷新发现下方核对表之外的新规则，**以新规则为准**（在会话日志记录）”——闸门阈值可被当日论坛内容改写：同一候选在不同日期可得不同判定，不可复现、无审批 |
| RB-06 | open |  | 步骤仍写“先经 MCP `authenticate`”（需邮箱/口令）——与 AGENTS.md 凭据红线冲突（同 NM-14/FB-10） |
| RB-07 | open |  | B.0：“Failed RA/PPA 非零 → **立即 REJECT**、无 CONDITIONAL 通道”；RA 步 8：非零 → **回步 7 修复**。同一情形一处“拒绝” |
| RB-08 | open |  | B.0a 从 `tracking/field_inspect_<region>.json` 取体检结果——RA 的体检包路径是 `tracking/mining/field_ins |
| RB-09 | open |  | 近窗制度（用户指令 2026-06-20，理由：要求 10 年全强会杀活信号）+ 计算口径 + 全历史指标仅作软标记——**判据与理由并举**；“sharpe > ~0.3”“用户 |
| RB-10 | open |  | 判定表个别行与他处不符：①“Sub-universe 全部 ≥1.0（TOP1000/500/200）”固定了子宇宙档，而平台 LOW_SUB_UNIVERSE_SHARPE 是* |
| RB-11 | open |  | REJECT 后要求调用 `wqb.search.failure_memory.record(category, dataset, universe, paradigm, shap |
| RB-12 | open |  | Phase E 编号 1,3,4,5,6（**缺 2**） |
| RB-13 | open |  | “提交前用 `set_alpha_properties` 预置描述 + `tags=["PowerPoolSelected"]` + `color=GREEN`”与本节第 1 条“ |
| RB-14 | open |  | “幽灵提交识别：台账记 ACTIVE 但平台 404 → **修正台账为 PHANTOM**”——`PHANTOM` 不是代码中存在的状态；且 2026-09-28 N35 之后， |
| RB-15 | open |  | “**提交探测协议**：选 5 个最大化多样样本，逐个提交+轮询 `/check` 读 prodCorr；5 个全 FAIL → 整族不可提交”——提交即真实动作（若通过即 ACT |
| RB-16 | open |  | “判定阈值可通过 skill 参数放宽”——skill 没有参数机制；阈值来源“2026-04-22 论坛共识” |
| RB-17 | open |  | 验证清单第 2 条藏着**最重要的操作知识**：`check_correlation` 阻塞轮询、依赖 Redis（“本环境不可用”）易“等死”；可靠取法是 15s 间隔轮询 `G |

## RC

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RC-01 | fixed | Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | prod-corr-avoidance 改写为 prod 总纲：删除「POST / GET /submit 触发 prod 计算」的危险旧指令（GET 恒 404；POST 通过即真实提交）；prod 一律 check_correlation |
| RC-02 | fixed | Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md | 「已确认」表只收提交实测的族；推测项单列为「待验证（推测，未触发实测）」 |
| RC-03 | fixed | Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 「不再投任何变体」限定为已确认撞墙的族；变体尝试的唯一例外（踩线带 1 次结构性尝试）在 D0-P，两处不再相悖 |
| RC-04 | fixed | Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md | 「GLB 黄金配方」标为历史：该族已判死，且 margin 5.0–5.1bp 低于 GATES_INTERNAL.margin_bp_min（10），不得当直接套用配方 |
| RC-05 | fixed | Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md | §4 证据附录整体标为历史（GLB 双墙实验），假设与其证伪不再并列作待办；会过期的状态说法降为带日期的历史结论 |
| RC-06 | fixed | Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md | 排队纪律（触发 / 缓存 7 天 / refresh=True / from_cache / 串行泳道）提到最前一节，Redis 键名等实现细节收进出处列 |
| RC-07 | fixed | Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/SKILL.md | prod 总纲成为唯一入口：怎么测 / 怎么读 / 已确认族在此；「拿到值之后怎么办」只有 D0-P 一张表，其余文档只引用 |

## RD

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RD-01 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 头注加优先级与红线：用户指令与硬约束冲突时执行并写 waiver 留痕；红线（提交前用户确认 / 凭据 / 平台限额）任何人批准都无效；「表中没有的分支才允许停下问用户」限于非红线 |
| RD-02 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D0 廉价闸只引 config.GATES["internal"]（TVR 区间、margin 等不再在表里复写）；用户临时阈值只在该次会话内生效 |
| RD-03 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | D3 按意图重定义：跨数据集补腿不是提分捷径；第二数据集只能以条件 / 分组 / 残差入场，不并列相加；删除「主动混合冲更高 Sharpe」 |
| RD-04 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | prod 墙只剩 D0-P 一张表；D14 降为「踩线带内那 1 次结构性尝试怎么做」；镜像稀释撤回 |
| RD-05 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D1 第 2 步 LOW_2Y 以平台线为准（PLATFORM_CHECK_LINES），删除「strictly > 1.6」与「> 1.58」并存 |
| RD-06 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D1 第 4 步区分平台线（PROD/SELF < 0.7、CW 必过）与内部线（SELF < 0.5）；PPAC / CW 缩写首次出现处给全称 |
| RD-07 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D1 第 6 步：submit_ready 是独立 SQL 表（submit_queue.py 单一事实源），不是 ledger_kv 键 |
| RD-08 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/worldquant-submit-alpha/SKILL.md | 删除「201 + success:false 是工具 bug」；提交响应四态统一由 submit-alpha 处置，判据只认 status == ACTIVE |
| RD-09 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D2「sharpe < 0.8 放弃」改为「该集最强 \|sharpe\| < 0.8 且已做镜像探针（D12）」：符号盲与粒度错位修正 |
| RD-10 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D2 / D6：CW 失败只按 D6 修法顺序（时间平滑 → 换算子几何 → 单信号结构 → 换字段），不补腿（D3） |
| RD-11 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | D3 按意图重定义：跨数据集补腿不是提分捷径；第二数据集只能以条件 / 分组 / 残差入场，不并列相加；删除「主动混合冲更高 Sharpe」 |
| RD-12 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 删除线原文（MINING.slow_fast_mix、add(multiply…)、慢×快加权混合）全部清除，历史只在 CHANGELOG |
| RD-13 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | D4：S0 三个入口名并成一个顺序（s0-select → calibrate → 打分），score_datasets.py 是 workflow_campaign(S0) 的内部实现 |
| RD-14 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D4 字段数 / 覆盖率 → 处置：一张四行表，区分 usableFields（S0）与「有覆盖的字段数」（S1）两个量，阈值与处置各一处 |
| RD-15 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D4：两条用户指令冲突时，后到的显式指令覆盖先前的「定案」并记 override |
| RD-16 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D4 MCP 不可达行去掉写死的 127.0.0.1:8876，改为「见环境章」 |
| RD-17 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D5：ILLIQUID_MINVOL1M 对 USA / ASI / EUR 已停提，不得作对照档；universe 见 config.REGIONS |
| RD-18 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D6：hump 仍受支持但须命名参数 hump(x, hump=k)，删除「已废弃禁用」 |
| RD-19 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D2 / D6：CW 失败只按 D6 修法顺序（时间平滑 → 换算子几何 → 单信号结构 → 换字段），不补腿（D3） |
| RD-20 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D7（S2-D 多样性榨取）标为可选、默认关闭，并说明 enter_multi_dataset 与「单数据集 atom 优先」方向相反 |
| RD-21 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md | D8 只留「条件 → 动作」的真决策；步骤清单并入步 6 细则；WAVE_LEDGER.md / ledger.json 写法删除（战役产物只入 wqb.db） |
| RD-22 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/step6-backtest.md | D8 只留「条件 → 动作」的真决策；步骤清单并入步 6 细则；WAVE_LEDGER.md / ledger.json 写法删除（战役产物只入 wqb.db） |
| RD-23 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D9：合法 PPA 只能走平台 web UI（MCP 通道不感知 PPA），agent 停下交接 |
| RD-24 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D10：verdict 持久化到 DB（战役 state json 已废）；多样性评估节奏标「经验，无统计依据」；并发以 config.CONCURRENCY 为准 |
| RD-25 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D11 重写为只保留仍有效的规则；加权混合配方标已废止，「腿禁用 ≠ 整集判死」给定义 |
| RD-26 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D15 判死判据表：对象 / 判据 / 出处 / 记录位置摆在一处（不强行统一不同粒度的数字） |
| RD-27 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/step3-s1-semantic.md | D13 由步 3 §3.2 直接引用；profile 不再有 longcount_min 键（等同全局默认且无代码读取） |
| RD-28 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | D3 按意图重定义：跨数据集补腿不是提分捷径；第二数据集只能以条件 / 分组 / 残差入场，不并列相加；删除「主动混合冲更高 Sharpe」 |
| RD-29 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | D14 中 0.7003→0.6993 证据标注 n=1、差值在测量噪声内，只算「可试」；同文 pv103 0.6997→1.0000 说明单次读数会被外部提交冲走 |
| RD-30 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 头注「被 SKILL 哪一步引用」索引：每条 D 对应哪些步骤消费一目了然 |

## RE

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RE-01 | open |  | 声明“5 轴旋转、降相关 6 武器、分布形态→修复方向映射、news/sentiment 专用方向、幽灵算子警告、体检硬门复验已于 2026-08-23 全部上移进 optimiz |
| RE-02 | open |  | description、职责边界、“触发场景”三处重复同一列表；定位声明称“改进的唯一入口是 optimization-v1”，边界又称“只作配方参考、不直接执行”。descrip |
| RE-03 | open |  | 🟢“REGULAR 修复成功的唯一标准是 `Failed RA == 0`；PPA 是 `Failed PPA == 0`；改善 Sharpe/Fitness/相关性但 faile |
| RE-04 | open |  | “选定任何算子前先确认它在当前 `get_operators` 返回里”——方向对，但成本高（全量返回），且已有机械守护（gate0 的 `known_ops`/`ghost_op |
| RE-05 | open |  | 三条 bullet：turnover 写“平台支持的降换手算子”（**无算子名**）、coverage 写“回填、重审向量聚合、复查 NaN 策略”（无参数）、correlatio |
| RE-06 | open |  | 链接 `docs/reference/news_sentiment_playbook.md` 以仓库根为基准书写，而 markdown 相对链接应从 skill 目录解析（会落到  |
| RE-07 | open |  | 声明自己是该教训的“**唯一完整版**；ppa-mining §1.0.x 红灯行与其它文档只允许引用此处”。问题：①把一条“唯一权威”实证放在**自称已退役**的 skill 里 |
| RE-08 | open |  | “提交探测零成本（硬闸失败不消耗**周**额度），但浪费时间——先 5 个多样化探针（不同前缀×universe×neutralization）确认 prodCorr 再决定是否全 |
| RE-09 | open |  | “USA REGULAR 修复保持 TOP3000 默认 universe；用其他 USA universe 时台账必须记录 TOP3000 失败原因与该 universe 回答的 |
| RE-10 | open |  | “修复记录为新的轨迹步骤”“确认修复路径在 `trajectory_steps` 可见”：`trajectory_steps` 是 `wqb.memory.SimulationDB |
| RE-11 | open |  | 4 条验证项里，第 2 条（failed count 为零）机器可判，第 4 条“确认 §2d 的教训在修复决策时被读取”**无可检产物**（“读取”不留痕） |
| RE-12 | open |  | 应有三张情景卡：①降换手（turnover 32%、Sharpe 1.7 → 动作、预期、验收 `Failed RA==0`）；②覆盖不足（cr<0.4 → `ts_backfil |

## RF

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RF-01 | fixed | Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md | 名单以 config.RA_CHECK_NAMES（18 项）/ PPA_CHECK_NAMES 为准，文档不再抄名单（旧版缺 LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO）；冻结副本由测试守 |
| RF-02 | fixed | Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md | 来源版本引用以 config.py 注释为准，并说明插件在仓外无法复核 |
| RF-03 | fixed | Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md | §2 PENDING：Failed == 0 不等于已通过；给出 Failed × 名单内 PENDING 的三行含义表与调用方动作 |
| RF-04 | fixed | Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md | 明确 PPA 另计 LOW_SHARPE value < 1；RA 侧只认 result，不看 value |
| RF-05 | fixed | Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md | 名单以 config.RA_CHECK_NAMES（18 项）/ PPA_CHECK_NAMES 为准，文档不再抄名单（旧版缺 LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO）；冻结副本由测试守 |
| RF-06 | fixed | Claude/skills/wq-brain-ra-pipeline/references/webdatascope-failed-gates.md | 全文改为中文，并指向 config.compute_webdata_failed_counts 为唯一实现 |

## RP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RP-01 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 提示词不再复写数字（引用 config / 决策表）；铁律逐条指向 SKILL 步 |
| RP-02 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 「步 0」删除；operator_audit（平台算子表）与 ghost-audit（表达式级）区分 |
| RP-03 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 步 2 补齐：calibrate、已点亮塔不进白名单、体检包前置与 --inspect-mode、座位可达性、饱和路由 |
| RP-04 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | workflow_feature_engineering 从步 3 动作里移除（按需、仅人读、禁注入 GEM） |
| RP-05 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | priors_file 可省略与波内配额 ≥ 2 位换腿与 SKILL 统一（同 RA-47 / RA-48） |
| RP-06 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 步 5 顺序改为 ghost-audit 先行、wave_gate 随后；缺闸（SEM / PF / 体检）补齐 |
| RP-07 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 逐候选链补 check_correlation；撞 prod 墙只引 D0-P（不再「按 D14 三条路径」） |
| RP-08 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 步 9 补 assemble-priors 刷新与 dataset-experience；验收表不再要求写 s6_verdict_<wave> |
| RP-09 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md \| Claude/skills/wq-brain-ra-pipeline/references/loop-and-stop.md | 「连续 3 波 gate 通过率 0」的动作与 SKILL 循环表统一（转 matrix 换数据集 / next-move 换区域，或用户显式放行） |
| RP-10 | fixed | Claude/skills/wq-brain-ra-pipeline/SKILL.md \| tests/unit/test_ra_sop_template.py \| Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 「步 \| 动作 \| 命令 \| 产物 \| 通过？\| 失败分支」提升为 SKILL 每步固定模板（RA-10，由测试守）；提示词里只留一行格式引用 |
| RP-11 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md \| Claude/skills/wq-brain-ra-pipeline/references/scenarios.md | 发批快捷入口与 SKILL 一致（步 5 起，前置闸 SEM / 体检包会拦）；Mode B 描述与 §7.7 统一；情景卡 RA-02 / RA-03 |
| RP-12 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md \| Claude/skills/brain-alpha-repair/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 失败点 → 修法族速查表放 brain-how-to-pass-alpha-test，repair 与 RA 提示词双向链接（PROD 一行只引 D0-P） |
| RP-13 | fixed | Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md | 验收表补：SEM / 体检包、5b prod-first、assemble-priors 刷新、dataset-experience、QUICK 产物隔离；submit_verdict 标签用真实值 |

## RR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RR-01 | fixed | Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/USA.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/IND.md | region-profile-contract §1：front-matter 哪些键被代码读（只有 entry_verdict / priors 兜底），其余为文档；gate_overrides 只写与默认不同的键（删除 longcount_min / prod_corr_early_warn 等同默认项） |
| RR-02 | fixed | Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/USA.md | USA「0.6 即停扩换腿」并入 D0-P 0.60–0.70 行；profile 不得另设预警线（契约 §1 明文） |
| RR-03 | fixed | Claude/skills/wq-brain-ra-pipeline/references/regions/IND.md | IND front-matter：green 清空并加 green_note（已点亮塔不作主数据集，旧版把 mdl177 列 green 与 2026-09-19 用户定案相反）；signal_families_include 与正文对齐 |
| RR-04 | fixed | Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md | §3 last_verified = 最近一次「内容核对」日期，批量机械刷新不得改这个戳 |
| RR-05 | fixed | Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/IND.md | §2 正文固定模板（定位 → 硬规则 → 流程变体 → 配方 → 避坑 → 证据附录）；IND 已按此重排，其余区域在下次被编辑时随手整理 |
| RR-06 | fixed | Claude/skills/wq-brain-ra-pipeline/references/regions/IND.md | IND 步 7/8 注入：2Y 强只免于被误杀、不免闸，最终过闸路径写明 |
| RR-07 | fixed | Claude/skills/wq-brain-ra-pipeline/references/regions/IND.md | 表格行内 \|ts_mean(P,252)\| 改为 abs(ts_mean(P,252))，GFM 不再把该行拆列 |
| RR-08 | declined |  | 范本，保留：trade_when 慢开关辅助腿与「无效结构」反例；内容已上移为步 7 §7.7.3（辅助腿入场三式）并在 IND profile 保留区域画像 |
| RR-09 | fixed | tests/unit/test_region_alignment.py \| Claude/skills/INDEX.md \| Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md | 删掉硬编码的 13/14 个区域说法；三处清单（config.REGIONS / profile / tracking）由测试对齐，已知缺口显式登记（AMR 无 profile、TWN 无 tracking） |
| RR-10 | fixed | Claude/skills/wq-brain-ra-pipeline/references/regions/KOR.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/TWN.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/HKG.md | 缺省项统一写成「缺省（决策表 D15：新数据集 8 探针无 \|S\|≥0.5 即判死）」；只有 KOR / HKG / TWN / JPN / DEU / MEA 写各自差异；语义 = 文档级快判死（D15 说明），代码不读 |

## RT

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| RT-01 | fixed | Claude/skills/wq-brain-ra-pipeline/references/concept-taxonomy-map.md \| tests/unit/test_concept_taxonomy_map.py | 分类表按代码实况重写：类名与数量对齐（不再写「12 类」而表中 10 个），由 test_concept_taxonomy_map 守 |
| RT-02 | fixed | Claude/skills/wq-brain-ra-pipeline/references/concept-taxonomy-map.md | 「主分类」与「同时标 dfe_question / hypothesis_class」的矛盾消除：一次生成只挂一套主分类，另一套作交叉标签 |
| RT-03 | fixed | Claude/skills/wq-brain-ra-pipeline/references/concept-taxonomy-map.md | validator.check_batch 只作方法论参考（全仓零调用方），不再作有效机制引用 |
| RT-04 | fixed | Claude/skills/wq-brain-ra-pipeline/references/concept-taxonomy-map.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | 组合腿（slow × fast spread）/ subtract(rank A, rank B) 不再作标准概念位；同源对偶价差才允许（步 7 §7.7.2） |
| RT-05 | fixed | Claude/skills/wq-brain-ra-pipeline/references/concept-taxonomy-map.md \| Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md | 归属说明：文件保留在 ra-pipeline/references（GEM 与 hypothesis-first 共用），双方以链接互相指向 |

## SA

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| SA-01 | open |  | description 触发含“**批量提交 alpha**”，而边界写“不提交 alpha、`--submit`=提交**回测**”；“调并发/配额闸/战役 pipeline”分 |
| SA-02 | open |  | “S3 **唯一**执行者/单一入口”，RA 步 6 却列出三个入口（`workflow_batch_track`、本 skill、toolkit）并让 agent 自选；边界“不 |
| SA-03 | open |  | “长任务执行规则”整节以**文件模式**为主线：启动前预检 `alpha_list.json` 存在、“进度真相源=输出 CSV”、“失败=进程停止 且 CSV 无进展≥**3 分 |
| SA-04 | open |  | 兼容命令示例用保守值（`--batch-size 3 --concurrency 2`），⚠ 警告放在代码**之后**；裸 `python` 与“$WQ_PY”规则不符 |
| SA-05 | open |  | 多样性增强**默认 `always`**：按“算子熵<2.0/覆盖率<50%/新颖度<80%/结构相似度>70%”自动做结构变异、**算子替换（ts_rank→ts_scale）* |
| SA-06 | open |  | 阶段→脚本→产物表是同一映射的**第 3 份**（toolkit §6、RA Artifact 表、本表），且产物写成旧文件名（`reference/…_dataset_ranki |
| SA-07 | open |  | “禁止**五**数据集同时首探”——数字 5 与七槽不符（RA 反模式写“七槽全裸探针”） |
| SA-08 | open |  | 凭据变量名 `BRAIN_EMAIL/BRAIN_PASSWORD` 与 inspect（`BRAIN_USERNAME`…）、concurrency/toolkit（`WQ_US |

## SB

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| SB-01 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md | description 改为触发条件 + 范围；关键坑放正文 |
| SB-02 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/quota-and-tower.md \| Claude/skills/worldquant-submit-alpha/references/ppa-handoff.md | 拆出 quota-and-tower / ppa-handoff / scenarios / fallback-rest；SUPER、PPA 各压成一句指针 |
| SB-03 | fixed | Claude/skills/worldquant-submit-alpha/references/submit-chain.md \| src/wqb/submit_verdict_core.py | 可达状态机（否决/放行权威）+ 独立退出码 1/10/11；文档不再写「等 SUBMITTABLE」 |
| SB-04 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/fallback-rest.md | 前置只写「凭据由 MCP 服务端加载，agent 不接触」；fallback 只读进程环境变量，不读 .env |
| SB-05 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md | 属性规范引用规格表；定义 R\|S；tags 上限写死 5；说明由 validate_color/build_tags/check_tags 各管什么 |
| SB-06 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md \| world-quant-brain-mcp/tools_workflow.py \| tests/unit/test_submit_chain_defaults.py | 示例拆预检(confirm_submit=False)与确认后提交；删不存在的形参；description 下限统一；顺带修 MCP 工具 color 默认 GREEN 顶掉节点 BLUE 缺省 |
| SB-07 | fixed | Claude/skills/worldquant-submit-alpha/references/ppa-handoff.md | PPA 路由表：满足本地预检线走 MCP，否则 web UI 交接 |
| SB-08 | fixed | Claude/skills/worldquant-submit-alpha/references/ppa-handoff.md \| Claude/skills/worldquant-submit-alpha/SKILL.md | 列出 pre_submit_check 实际规则与 force 的允许场景（合法 PPA / SUPER） |
| SB-09 | fixed | Claude/skills/worldquant-submit-alpha/references/fallback-rest.md | fallback 重写：403 读 checks、异步补发一次 + ASYNC_STUCK、规范属性、Retry-After 退避、不读 .env、CONFIRMED_BY_USER 闸 |
| SB-10 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/scenarios.md | 四态表保留并补：补发前确认 dateSubmitted 空；工具返回 False 见 201/202/空体 时按 ②③ 处置；>24h 悬空交用户 |
| SB-11 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md \| Claude/skills/GLOSSARY.md | PENDING「不据此判死也不据此放行」两栏；value>=limit；重新编号 |
| SB-12 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md | description PATCH 已封装，只留一句；删「21 项」；提交后 checks 只会 ALREADY_SUBMITTED 并入终态表 |
| SB-13 | fixed | Claude/skills/worldquant-submit-alpha/references/submit-chain.md | 提交层信息来源表：GET 恒 404 / POST（通过即提交）/ is.checks 各能回答什么；删审计叙事 |
| SB-14 | fixed | Claude/skills/GLOSSARY.md \| Claude/skills/worldquant-submit-alpha/SKILL.md | WARNING 分硬闸类（RA/PPA 名单 + SUBMIT_HARD_GATE_WARNINGS）与提示类，引用代码名单 |
| SB-15 | fixed | Claude/skills/worldquant-submit-alpha/references/quota-and-tower.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py | 配额只留一处；activities 统一为不可用；复检 = quota_status.py 不再 POST |
| SB-16 | fixed | Claude/skills/worldquant-submit-alpha/references/quota-and-tower.md | 点塔规则：过度提交改为交用户拍板；UNKNOWN 不预测；同档内先轮转再排序；单字段端点说明；反向约束指向 ra-pipeline 步 2 |
| SB-17 | fixed | Claude/skills/worldquant-submit-alpha/references/quota-and-tower.md | 点塔规则：过度提交改为交用户拍板；UNKNOWN 不预测；同档内先轮转再排序；单字段端点说明；反向约束指向 ra-pipeline 步 2 |
| SB-18 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md | 删无出处的 0.9 内部线；终态表补未决 / 卡住行 |
| SB-19 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md | SUPER 压成 3 行指针；不再把 POST 探测说成零成本 |
| SB-20 | needs-platform | 在用户同意下对一颗已 ACTIVE 的 alpha 重复 POST 一次，比对前后 REGULAR_SUBMISSION.value 是否变化 | 文档已改为「重复 POST 是否扣配额没有实测结论，故不做」，去掉「幂等」与「浪费额度」的矛盾说法 |
| SB-21 | fixed | Claude/skills/worldquant-submit-alpha/references/quota-and-tower.md \| src/wqb/timeutil.py \| src/wqb/store/_submissions.py | 配额模型只留一处；ET 用 America/New_York（冬令时 13:00）；删改动史；删无调用方的 48h 滚动 get_quota_status |
| SB-22 | fixed | tools/ppa_handoff.py \| Claude/skills/worldquant-submit-alpha/references/ppa-handoff.md \| tests/unit/test_ppa_handoff.py | 交接单模板 + 回写命令（核验后写 submission_ledger）+ 用户不在线的默认动作 |
| SB-23 | fixed | Claude/skills/worldquant-submit-alpha/references/ppa-handoff.md | 预检规则与 pre_submit_check 一致：margin 只是 warning，turnover 4–40%、returns>4% 是硬失败 |
| SB-24 | fixed | AGENTS.md \| tools/README.md \| tools/submit_batch.py \| world-quant-brain-mcp/tools_ops.py \| Claude/skills/worldquant-submit-alpha/SKILL.md | submit_batch = 派发仿真（dispatch）写入词表与各处文案；submit_verdict 不再称「唯一可信入口」 |
| SB-25 | fixed | Claude/skills/worldquant-submit-alpha/references/scenarios.md | 四张情景卡：正常 / 异步未翻转 / 配额 403 / 并行会话用光配额 |

## SC

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| SC-01 | open |  | 边界清楚（本地快筛 / 不占平台配额 / 不替代实测 / 不作提交判定）。但 MCP 已有 `check_self_correlation`（本地增量缓存；`correlation |
| SC-02 | open |  | “若 self-corr 高于 0.7，甚至无需再向平台查询生产相关性——因为平台结果同样会高于 0.7”。**SELF（自己已提交）与 PROD（平台生产池）是两个池**，SEL |
| SC-03 | open |  | 🟢 见总评。P2：①未给“近期”的量化界线（新提交多久后进池？池刷新周期？）；②无“何时本地值可信”的检查步骤（如比较池文件 mtime 与最近提交时间）；③“务必先读”的 ★★  |
| SC-04 | open |  | 推荐“同族连测场景不要依赖本地 SELF，改用零成本实测：`POST /alphas/{id}/submit`”。**仅当硬闸失败时才不消耗配额；若该 alpha 全部通过，POS |
| SC-05 | open |  | “`PENDING` ≠ `FAIL`、不挡提交”“`GET /alphas/{id}/submit` 恒 404”是有价值的**否定性事实**。但：①夹带改错史（“旧文写的 `G |
| SC-06 | open |  | “`REGULAR_SUBMISSION: FAIL value=4 limit=4` … 换日即失效”：①“4/4”是某次实测，limit 随账号/日变化，应写 `value ≥ |
| SC-07 | open |  | 脚本段：①示例 `python <SKILL_ROOT>/…/skill.py`——`<SKILL_ROOT>` 未定义，裸 `python` 而非库内约定的 `$WQ_PY`；r |
| SC-08 | open |  | 下游写“explain-alphas → 过拟合/稳健性测试（见 optimization-v1）→ judge”。robustness 已是独立 skill（`brain-alp |
| SC-09 | open |  | 英文原译混在中文 skill 里；`--sharpe-threshold -1.0`/`--fitness-threshold -1.0` 默认意味着“不过滤”，未解释；结果“保存 |
| SC-10 | open |  | 用一张 3 行决策表替换现有 3 条规则：①“同族 5 个孪生体，其中 blRaArVZ 昨日提交；本地 SELF=0.23” → **不采信**，预检平台实测；②“本地 SELF |

## SP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| SP-01 | open |  | description 400 字，塞入 `(1 + 0 * (prod_correlation > 0))`、`score = (0.7 - prod_correlation)` |
| SP-02 | open |  | 边界写得好：“本区 ACTIVE REGULAR ≥10 且双闸达标；**不得改用 REGULAR 路径绕过**”（🟢 有止损句）。问题：①上游写“`submit_verdict` |
| SP-03 | open |  | “硬前置（必读，否则必败）”混了四类东西：①规则（≥10 颗、异步校验、描述 ≥100 字、裸 PATCH）；②**日期快照**——“现状（2026-09-11）：USA 133  |
| SP-04 | open |  | 🟢“**201 ≠ SA 合法**：错误异步出现在模拟结果（`status:"ERROR"`，`At least 10 component alphas are required` |
| SP-05 | open |  | “MEA 通道已关闭：`POST /simulations region=MEA` → 400 ‘Region MEA is not available’，既有 2 颗 MEA S |
| SP-06 | open |  | 🟢“各需 ≥100 英文字；`set_alpha_properties` 对 SUPER 必 400（无条件带 `regular` 字段）；正确写法 = 裸 PATCH 最小 pa |
| SP-07 | open |  | 配额模型再次重述（ET 日 REGULAR 4 + SUPER 1；`get_submission_quota` 已移除；读 submit 响应；“硬闸 FAIL 不消耗配额，属零 |
| SP-08 | open |  | ①combo 只给“`1 - maxCorr`；maxCorr 借助 `generate_stats/self_corr/reduce_max/if_else` 等算子构造”，示例 |
| SP-09 | open |  | **追加式文档：后文推翻前文，前文未改。** L108“把 PROD 压到 0.7 以下的**决定性因素**是 SUBINDUSTRY”；后文：“PROD 已结构性饱和（USA 0 |
| SP-10 | open |  | 🟢 篮宽×decay 表与 KOR decay 曲线（12→300 逐档 SELF / S / F / turnover）是全库最完整的参数-指标对照。P2：①“USA V8/V9 |
| SP-11 | open |  | “**`GET /alphas/{id}/submit` 200 可能是 PENDING 假阳性**”——与 submit-alpha 关键坑 #5（“`GET /submit`  |
| SP-12 | open |  | “零成本双闸探针（提交前必做）”用 MCP `check_self_correlation` 与 `check_correlation`：①配套 CLI `super_build. |
| SP-13 | open |  | submit 流程有**两个入口，安全性不同**：Step 0 的 **prod 闸**（max≥0.7 拒绝；超时 fail-closed；`--allow-prod-above |
| SP-14 | open |  | 四个“真实案例”按时间顺序堆叠：案例 1 自称使用已禁用的 `combination()`，“此处仅为等价思路说明”，**不可复现**，且“成分：…→ 等价体须 PROD≤0.7  |
| SP-15 | open |  | “判定只看 result，不看 value”出现 3 次，“我方铁律 prod≥0.7 不提交，以我方闸为准”出现 2 次，**两者并存时的优先级只在验证清单末尾一句**（L243 |
| SP-16 | open |  | “淘汰的同构变体打 `RETIRE_<date>_DUP_SA` + color RED + hidden，防审计误报”——`RETIRE_…` 是 tag 还是 name 未说， |
| SP-17 | open |  | 🟢 六条勾选项可检（“组件恰好 10 颗时必须放宽 gate，否则秒拒”“只看 result 但我方 prod 闸优先”）。P3：“neutralization 逐区扫描（USA/ |
| SP-18 | open |  | “`alpha-expression-verifier`：提交前本地校验 selection/combo 表达式语法”——核对：该 skill 全文**无** selection  |
| SP-19 | open |  | 缺三张“从零到一”情景：①**KOR/IND 从 0 到 SA**：数组件 → 差 N 颗回 RA → `select`（decay / nu / self-gate）→ `sta |

## TK

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| TK-01 | open |  | description 702 字（全库最长）是**功能清单**（含“骨架配给 linear_mix≤0.5”“REGULAR 4/日+SUPER 1/日+PPA 1/日”等实现细 |
| TK-02 | open |  | 7 个连续空行；“ledging”笔误 |
| TK-03 | open |  | 声称本 skill 是 **`wave_results` / `registry_empirical` / `ledger_kv` 的“唯一正式写入方”**——但 `mcp__wq |
| TK-04 | open |  | `campaign.py dataset-experience` 的说明是孤立段落，夹在“职责边界”与“1. 定位”之间；§6 子命令表里没有这一行 |
| TK-05 | open |  | “本 skill 是战役脚本的**唯一权威实现**”——实际引擎分两处：本 toolkit（gate/pipeline/build_wave/score_datasets/revi |
| TK-06 | open |  | 标题是“使用率分级”，正文却含**行为契约与安全规则**：选波数量契约（L53–62）、异步恢复（L64–68，含 “MCP 桥接超时返回 `outcome_unknown`、`r |
| TK-07 | open |  | 已归档脚本（`distill_experience/os_feedback/family_atlas/budget_planner/campaign_mutex/signal_cl |
| TK-08 | open |  | “核心 5 工具”按 2026-08-31 的静态引用扫描定义，`score_datasets/build_wave/review_wave` 被划为“中使用率”，而 RA 的 S |
| TK-09 | open |  | 10 行无编号、中英文无空格（“`--size`在CLI与workflow S2中都只表示容量”），与 RA L397–409 及 `selection-plan.md` 是**同 |
| TK-10 | open |  | 同一段里放了两件无关的事：异步任务恢复、救援池 `exclude_dataset` 的来源排除；后者属于 `get_salvage_pool`/RA 步 7 |
| TK-11 | open |  | “brain-sim-alphas-in-batch-and-track 是**唯一运行时调用方**”不成立：`workflow_batch_track` / `workflow_ |
| TK-12 | open |  | 该行是**最好的产物契约**（脚本 → 库表/ledger key），但是一整行 700 字；且与 RA Artifact 表冲突：这里 `review_wave.py → led |
| TK-13 | open |  | 契约里夹带“KOR/IND/DEU 混合形态、`probe_scoring_v2` 刻意缺”的决策记录（对 agent 的动作是什么？）；`campaign-dir-contrac |
| TK-14 | open |  | 凭据链列了 4 个来源（环境变量 / `BRAIN_CREDENTIALS` / `~/.brain_credentials` / `MCP_CONFIG_FILE`），与 AGE |
| TK-15 | open |  | 开波闸模式段 560 字，实际决策只有“命令行 > 环境变量 > 按日期缺省；节点一律拦截” |
| TK-16 | open |  | ①bash 变量赋值（`PY=$WQ_PY`）与全库 PowerShell 约定不符；②流程只用 `gate.py`（闸 1–6），**完全不含 `tools/wave_gate. |
| TK-17 | open |  | 子命令表：①含 5 个已归档脚本（TK-07）；②缺 RA 依赖的 `campaign.py assemble-priors`、`dataset-experience`、`dive |
| TK-18 | open |  | §6.x 记录 `saturated_datasets`、`seat_model` 是“数据源台账”，但**全仓库没有任何代码或指令写入 `saturated_datasets`* |
| TK-19 | open |  | P0/P2/P3/P5/P6 是审计工单号（无 P1；P4 只在 L169 出现）；与 `probe-scoring-v2.md` 的“P5 分段罚”、探针模板 P1–P8 **同 |
| TK-20 | open |  | “`score`=信号强度榜、`pyramid_view`=点塔战略榜，语义分离，**勿相加或混排**”——明确写了“不要拿它做什么” |
| TK-21 | open |  | “接线修复落地（审计①③⑥⑦）”是变更记录，圈号指向外部审计报告；内容与 RA（settings prior、region_kb 刷新、S2-COMPLIANCE 降级、rn 墙/ |
| TK-22 | open |  | “小宇宙区域 KOR/HKG/TWN **按 profile 升级 FAIL**”“CW 在区域 profile 的 `cw_gate` 覆盖中处理”——代码核对：`gate.py |
| TK-23 | open |  | “无效努力七信号”里 4 条是定性判断（“换变体无本质变化”“反复失败”“偏高”）未给可测口径；“priority 65”魔法数；链接 `docs/experience/fail_ |
| TK-24 | open |  | 标题“今日实证驱动”（相对时间）；第 1 行 `prod-first` 与 RA 步 7 的 `--top-k 3` 不一致（此处 `--prod-first-top-k 2`，与 |
| TK-25 | open |  | **同一协议写了两遍**：§7.y“二分排障（5 步）”与文末“平台报错二分定位（3 条）”；同步目标一处写 2 个（`platform_constraints.json` + p |
| TK-26 | open |  | “禁止 record_*.py 式直改”×2、“禁止第二权威实现”×2、“单轨数据库”与 matrix 重复；#2 的 429 退避属 wqb-concurrency；#3 仍提  |
| TK-27 | open |  | “**提交配额**是稀缺资源：未过 gate 不提交；pipeline 默认只干跑，显式 `--submit` 才烧配额；`--force` 才越过配额闸”——“提交/配额”同时指 |
| TK-28 | open |  | 把 RA 步 4 硬约束**原样抄第三份**，含①已被禁的加权混合范例“EUR：`0.40` 慢 MODEL 残差 × `0.60` 快 PV”，②“有信号字段先做组合（同集或跨金 |
| TK-29 | open |  | “新增/修改 workflow 节点 → 四处同步”是**开发者流程**（改 registry.py、两个测试、INDEX 计数，`audit_node_registration. |
| TK-30 | open |  | “**AI 回写一律走 `campaign.py wave` CLI**”与 RA 步 9“`mcp__wqb-db__upsert_wave_result`”“一律”冲突（两者虽 |
| TK-31 | open |  | “WAVE_LEDGER.md 是从数据库**生成**的快照（覆盖写，勿手改）”——正确，且与 decision-table D8 的“追加 WAVE_LEDGER.md”矛盾 |
| TK-32 | open |  | 查询清单把 `get_ledger_key(key="submit_ready")` / `get_submit_ready` 当作“达标池”读法；但 **`submit_read |
| TK-33 | open |  | 15 个 MCP 查询示例（含 alpha 查询、区域概览）属 INDEX/wqb-db 工具说明，而非引擎职责 |
| TK-34 | open |  | 唯一说明“toolkit vs tools/ 分工”的位置（好），但只有 5 行，且用了已被 RA 作废的旧称“提交层判定（403 盲区）” |
| TK-35 | open |  | 文末又一个“2026-09-19 新增”，见 TK-25；另含“2026-09-19～27 它不在 MCP 工具表里（装饰器错挂，N31）”这样的故障史 |

## TR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| TR-01 | open |  | 声称“闸编号唯一基准 = `gate.py` 模块头”；而 ra-pipeline、toolkit SKILL 都写“唯一基准见 INDEX.md「gate.py 闸编号」”——* |
| TR-02 | open |  | “当前平台级：`nested_three_leg_add`”——`platform_constraints.json` v1.5 实有 **6 条**（另有 `weighted_s |
| TR-03 | open |  | 写“契约到 `expires_after_batches` 自动**失效**”；`gate.py` 与 RA 均为“过期→**FAIL-CLOSED** 并自动续约”（gate.p |
| TR-04 | open |  | “构建端：`diversity_slots.py --campaign-dir <DIR>` 打印当前契约”——该脚本已归档（SKILL L73），文件不存在 |
| TR-05 | open |  | “注入算子的经济学写法”以 `ts_corr(慢腿,快腿,20)` / `if_else` / `group_zscore(慢腿, sector)` 为例，仍是“慢×快”双腿叙事； |
| TR-06 | open |  | 描述**文件模式**（`<region>_wave*_exprs.json`、`candidates/*.json`、`reviews/*.json`、输出 `candidates |
| TR-07 | open |  | `diversity_extract.py` 在此写了 40 行，又有根目录 3 份说明（546 行）、D7 一份——同一工具 5 份文档 |
| TR-08 | open |  | 墙枚举“SHARPE/FITNESS/2Y/MARGIN/TVR/CW/RA_OTHER/NO_DATA”缺 `RN_EXPOSURE`、`ROBUST_STRUCTURAL`、p |
| TR-09 | open |  | verifier 查找顺序把用户主目录已安装副本（`~/.claude/skills`…）放在**仓库 `Claude/skills` 之前**——旧副本会覆盖仓库版本，验证行为不 |
| TR-10 | open |  | `--fix` 段与闸 4 的“不要改 validator.py”“对 ops_used 判定是死代码”是给开发者的实现注释；闸 3 同句称 VECTOR 违规报 “[EVENT] |
| TR-11 | open |  | “`stage_submit_poll` … 并行提交+轮询 N 批（**N=min(5, 批数)**）”——代码是 `n_slots = min(7, n_total)`（`pi |
| TR-12 | open |  | 整节是“单批在飞规则（**已废弃**）”：删除线原文 + 纠正 + 历史实证；agent 读到的第一句是被废止的规则 |
| TR-13 | open |  | 配额只写两条通道（REGULAR 4 + SUPER 1），而 toolkit description、`campaign-dir-contract` 写三条（含 PPA `POW |
| TR-14 | open |  | “凭证与登录”一节混入 metrics_cache 读穿缓存 |
| TR-15 | open |  | 仍把 `wave<N>_verdict` + `ledger set-verdict` 当作**逐波结论的正式通道**——RA 已于 09-28 声明“结论唯一真相源=`wave_ |
| TR-16 | open |  | `submit_ready[]` 只描述 ledger 列表，完全没提 SQL 表 `submit_ready`（TK-32 脑裂） |
| TR-17 | open |  | “键命名约定”只有 12 行且多为旧键；正文与 RA 用到的活跃键（`s0_ranking`、`s0_whitelist`、`s1_<ds>_d<delay>`、`s1_seman |
| TR-18 | open |  | 原语（`.bak` 滚动备份、`atomic_save`、双遍重放）是 **JSON 后端** 的描述；默认后端已是 SQLite |
| TR-19 | open |  | 标题“CLI（campaign.py ledger / 直接 _lib.ledger 不支持，走 campaign.py）”语句不通 |
| TR-20 | open |  | 目录布局把**仍必需**（`config/`、`reference/` typed catalog）与**DB 唯一模式下已不产出**（`candidates/`、`reviews |
| TR-21 | open |  | 示例 JSON 含行内 `#` 注释（非法 JSON，复制会报错）；示例中性化 `SECTOR`，而决策表 D5 称 SECTOR/MARKET 会压垮 IS_LADDER |
| TR-22 | open |  | `hard_gates` 的“权威定义见 brain-how-to-pass-alpha-test”——而 `config.GATES` 才是全库唯一事实源 |
| TR-23 | open |  | 称 `diversity.signal_floor` 是“**唯一有消费方**的子键”，下文又给 `diversity.stop_rules`（同样被 `_run_stop_rul |
| TR-24 | open |  | “上表”指的是其后的表；“11 个区域已补齐”与 RA 的“13/13”、REGIONS=14、TWN 缺目录三种数字并存 |
| TR-25 | open |  | **优点**：有完整 JSON 清单示例（hypothesis/control 配对、“ID 仅为格式示例”）。**问题**：①标题“选波”，后半（L44–60）是波后解读与研究线 |
| TR-26 | open |  | 文档 tier 分位 **P80/P55**、`coverage_hard_min` **0.65**；代码缺省 **P60/P30**、`coverage_hard_min` 缺 |
| TR-27 | open |  | 三灯动作建议：“绿灯带 CW 失败 → 骨架直接上**跨 Category rank 加法**”“黄灯 → 只做镜像腿与**两两融合**限 2 批”——直接**推荐**被禁的 le |
| TR-28 | open |  | “calibrate **不在默认流程里**（ra-pipeline SOP 都不自动调）”，而 RA 步 2 把 calibrate 列为“**必需**”——一处说“没人调”，一 |
| TR-29 | open |  | P 编号同号异义（“P5 分段罚”对 SKILL“P5 饱和拍平 model”；探针模板 P1–P8）；三灯里 `margin(>5bp)`/`tvr(5–30%)`/`rn(>= |
| TR-30 | open |  | “审 dry-run 时重点看两处异常 → 该怎么办（勿 apply，先查 ac 来源）”“数据源优先级 ①–④”——**场景→动作→理由**齐全，是全库最好的情景范式；RA 步  |
| TR-31 | open |  | 整篇描述 9 个脚本（`proxy_prescreen/ortho_prescreen/migrate_templates/diversity_slots/param_opt/bu |
| TR-32 | open |  | 要求“每次进 S2 必须调用 `brain-data-feature-engineering`、候选池**基于特征工程文档构建**、`pipeline.py` 硬闸缺记录即中止”— |
| TR-33 | open |  | 3 份互为近似拷贝（9 个共享段落，Jaccard 见机械检查 §G），孤儿，营销文风（“核心价值/深度集成方案总结”），引用不存在的 `scripts/test_diversit |

## WC

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| WC-01 | open |  | description 329 字，含“每次挖掘必须执行”“下一波设计强制以台账决策为输入”这类**要求**；“提交成功数极低”歧义（实指 429 下的模拟接受数） |
| WC-02 | open |  | 边界：“不发起回测、不改表达式、不提交”，只管并发；§8 却包含台账同步门（`check_ledger_sync`）、写波结论（`wave upsert`/`ledger set` |
| WC-03 | open |  | 演进注记：“配置基准以新模型为准（**瞬时 ≤6 安全**、批间 ≥45s）”；§8 末：“7 批 multisim 仅耗 7 令牌、**瞬时 ≤7 安全包络内**”——同文件两个 |
| WC-04 | open |  | §2 给出 `self._sub_sem = threading.Semaphore(C)` 的实现代码、§3 教“线程=C+1”，例子仍用 **C=5**（“3 线程×2 数据集 |
| WC-05 | open |  | 429 退避 `wait=min(20+attempt*8,45)s，最多 ~40 次`——全库第 3 套退避（toolkit：5s×2×5 次；BrainApiClient 自带 |
| WC-06 | open |  | 凭据加载“`load_dotenv(...abspath(__file__), ".env")`”是给脚本作者的代码，对 agent 应写“**不读取 .env**（AGENTS. |
| WC-07 | open |  | SOP 步 3“`lookINTO_SimError_message` → children → `get_alpha_details` 逐 ID”是旧 3 段链；RA 已用 `h |
| WC-08 | open |  | “`validate_fields=false` 避免预检超时”与 RA 步 3“新字段先 `create_multi_simulation(validate_fields=tru |
| WC-09 | open |  | 台账同步门（`check_ledger_sync`）是“执行层硬门”，但 RA 步 6 正文没有它（只在 decision-table D8 与本文）；“创建批次文件时同步在台账登 |
| WC-10 | open |  | 步 4 是一个 ≈600 字段落含 6 条规则（写 DB、快照勿手改、禁 runs/ 散件、未写不得提交下一波、判死当场写、每 10 波评估） |
| WC-11 | open |  | “提交配额与回测并行槽位是**两个独立机制**”——引擎里 `pipeline.stage_submit_poll` 在**提交配额耗尽时中止回测发起**（`--force` 才继 |
| WC-12 | open |  | 测 C 的 4 步给出**易踩坑**（`language` 必须 FASTEXPR，错了是 400 而非 429）、判据（首批连续 201 数=C）、“429 报文不含数字”与“/ |
