# Skills 变更日志

> 从各 SKILL.md 正文里迁出的「日期 / 新增 / 修正 / 事故」叙述。**规则在 SKILL.md 与 `references/`；日期与变更在这里。**
> 约定：新条目加在最上面；一条一行：`日期 · skill · 改了什么（为什么） → 证据 / 落点`。事故与起因写进对应 skill 的 `references/incidents.md`，这里只留指针。
> 决策与证据登记：[`docs/skills_review_decisions.md`](../../docs/skills_review_decisions.md)；逐条处置：`reports/skills_review_20260929_closure.md`。

## 2026-09-29 · skills 审查整改（`reports/skills_review_20260929.md`）

**wq-brain-ppa-mining / brain-alpha-research（S-E-3）**
- ppa-mining 收敛为 PPA 方法论：适用域表（PPA vs RA vs 代码缺省，测试逐项对照 `score_datasets.py`）、单一执行器（`workflow_campaign(stage="S0")` + `s0-select`，旧 `dataset_health_check.py` 归档到 `attic/ppa_mining_20260929/`）、三个「最优拥挤度」口径各标轴与出处、`alphaCount = 0` 不再「优先级最高」；字段级决策表与体检硬门（`check_expr_against_inspect`）同源；「V9 突破版」带权重配方删除并给合规改写；`is_placeholder` / C = 5 / 过期 universe 档位表 / `PowerPoolSelected` 的 MCP 提交删除；2026-08 区域快照移到 `references/region-snapshots-2026-08.md`（带失效条件，非指令）→ PP-01…26 / DEC-46
- alpha-research：拆研究者 / 维护者步骤，常量只引用 config，验证改为真实命令（`wqb research` 不存在）；`check_batch` 不再称门禁；WebDataScope 26 条规则移入 field-quality；references 清 wikilink / 旧路径并逐个入链；ASI 档的等权拼腿结果标「已被政策禁止」→ AR-01…13 / DEC-47
- 校验器：`subtract(x, y, filter=true)` 命名参数被误拒（漏标 `param_names`）已修，四份镜像同步 → DEC-48

**brain-forum-browse（S-E-2）**
- SKILL 改写为现役能力（只读 explore + 薄 recon + MCP 排障表）；「每轮必须贡献 / 不可协商」撤销——没有写工具时它无法满足；写路径（Run Contract / Auto-Send E1 / 对抗审查 / curator / 论坛 HTML）整体移入 `references/write-path/`（休眠，含阶段执行顺序表、术语消歧、公开内容脱敏清单），`mcp-by-phase.md` 460 → 43 行；模板与 `init_workspace.py` 默认只读、`--write-path` 显式开启 → FB-01…18 / FR-01…07 / DEC-45
- MCP：`get_glossary_terms` / `search_forum_posts` / `read_forum_post` / `get_daily_and_quarterly_payment` 删除 `email` / `password` 参数（凭据只由服务端配置提供），并加全库守护测试 → FB-10 / DEC-44

**brain-next-move-analysis / labs / expression-verifier / feature-implementation / dataset-mining-experience（S-E-1）**
- next-move 定为**报告器**：只转述 `tools/region_status.py` 的输出，选区决策归 `wqb.region_rotation`；判据数值提为 `region_status.py` 顶部常量（文档判据表与 matrix 的 `≥ 10` 由测试钉死）；日报按固定五列模板给建议，三项前置检查（点亮塔 / 跨区弱先验 / 停波闸）；`reference.md` 改规范体，删「传邮箱口令」「`get_ny_time.py`」「`random_string`」等不存在的东西 → NM-01…17 / DEC-40
- `validator.py` 四份三版本 → 逐字节镜像权威版（GEM 与外部 idea 入库通道此前用缺 hump / bucket / densify 修复的旧副本本地放行）；verifier SKILL 换真实非法示例与退出码语义 → EV-01…05 / DEC-41
- labs skill：规范移入 skill、按引擎实际形态重写；默认示例修正（`imb5_mktcap` 被引擎合规约束排除）；人工暂停点显式标出 → LB-01…09 / DEC-42
- feature-implementation：description 撤出「生成表达式」触发；`fetch_dataset.py` 认 `CREDENTIALS_*`、不再强制 `config.json`、不回显邮箱；核实 GEM 已不把 FI 文本拼进 prompt（AST 测试钉死）→ FI-01…06 / DEC-43
- dataset-mining-experience：已废止的 `s6_verdict_<wave>` 教学清零（最后一处）；补核验步骤与文件骨架 → ME-01…09

**wq-brain-ra-pipeline v3.0（重构）**
- 核心 `SKILL.md` 由 950 行 → 约 220 行：每步固定模板（目的 / 前置 / 调用 / 产物 / 完成定义 / 失败分支 / 不做 / 细则）；细则、事故、情景卡拆到 `references/`（`step1`–`step9`、`loop-and-stop`、`forum-recon-triggers`、`ppa-vs-ra`、`tool-index`、`scenarios`、`incidents`）→ RA-10 / RA-103 / RA-117
- `assemble-priors-internals.md` **按代码重写**：旧文写的「`GLOBAL/region_kb.templates[]` → wins」「`methodology[]` → region_context」代码里都没有，真正承载 S6 回写的 `registry_empirical` win / dead_end 层旧文一个字没提 → RA-50
- 新增 S6→S0 饱和反馈写入口 `campaign_intel.py mark-saturated`（`saturated_datasets` 此前全仓库只有读取方）；`submit_ready_blocked` 降为 deprecated → RA-113 / IX-20（`tests/unit/test_campaign_intel_mark_saturated.py`）
- 「提交类节点不入链」由代码强制：`execute_chain` 拒绝带 `confirm_submit=True` 的 `submit_alpha` / `superalpha` → RA-116 / X-9（`tests/unit/test_workflow_chain_irreversible_guard.py`）
- prod 墙处置只剩决策表 D0-P 一张；`prod-corr-avoidance.md` 改写为 prod 总纲，删除「POST / GET `/submit` 触发 prod 计算」的危险旧指令 → X-1 / RC-01 / RC-07
- 组合形态「允许清单」唯一一份（步 7 §7.7）；补「辅助腿入场三式」（条件 / 分组 / 残差）；`subtract` 价差须同源且有单一经济含义 → RA-89 / RA-90 / X-3
- 停止规则、放行、四道开波闸从一个 ≈2000 字的表格单元拆成 `loop-and-stop.md`（每条配缺省数字与数字例；旧文里「GBR 至 09-30」这类状态不再写）→ RA-117 / RA-118
- forum_recon 五个触发点并成一张表（额度以查出有效文章为标准、7 天缓存）→ RA-16 / RA-57 / RA-94
- 6 个 `tools/*.py`（`build_gate_prior_from_inventory` / `select_ra_basket` / `gen_field_inspect_packs` / `field_semantic_classify` / `wave_gate` / `sync_platform_alphas`）接入 `tools/_pyenv`：作为脚本运行时自动切到 MCP venv，文档里可写裸 `python`（skill_lint bare-python）→ RA-07 / X-14
- 词表：**信号族**（字段集合，prod-first 分组）与**骨架指纹**（前 2 个算子，闸 PF）分开定义；旧 GLOSSARY 把两者写反 → RA-68

**wq-brain-superalpha v2.0（重构）**
- 旧 SKILL 是按时间追加的日记（后文推翻前文而前文不改；**全文没有「怎么建 SUPER simulation」的调用**；`force=True` 的 MCP 路径绕过 prod 闸；「预检」其实是真提交）。改为核心 SKILL（入口表 + 不可逆动作块 + 判定优先级 + 步 0–4 固定模板 + 参数取值理由 + 验证清单）+ `references/`（`levers-and-evidence.md` 决策表与参数-指标对照、`cases.md` 四个案例、`scenarios.md` 四张情景卡）→ SP-01 ~ SP-19
- 由代码强制：`submit_alpha` 节点拒绝 `type == SUPER` 的 `confirm_submit=True`（SUPER 只走 `super_build.py submit`，内置 prod ≥ 0.7 闸）→ SP-13 / T0-4（`tests/unit/test_submit_alpha_super_guard.py`）
- `super_build.py`：`--neutralization` 无缺省；universe / delay 取自 `config.REGIONS` 并校验；新增 `--selection` / `--combo`（`workflow_superalpha` 的同名参数此前被静默忽略）→ SP-17 / T0-8
- MCP `set_alpha_properties`：允许只传 SUPER 的 selection / combo 描述（此前缺省 `descriptions` 一律报错）→ SP-06
- 区域状态（MEA 通道对 SUPER 已关闭）从 SKILL 移到 MEA profile；「现状计数」快照删除，改为 `sa_probe` 实时命令

**brain-alpha-judge（三职能重排 + 安全收口）**
- SKILL 由「两道硬闸 + 六步 + 确认后提交」的旧骨架重排为三职能（PPA 核对清单 / trend score / 点塔排序）；旧「提交语义（GBR 旧口径）」「确认规则」「提交路由」整节删除，点塔口径只留 submit-alpha 的 `quota-and-tower.md` §2 → JD-01 ~ JD-05、JD-15 / JD-16
- 代码：凭据只读进程环境变量（不读 `.env` / 明文文件）；LLM 只能收紧确定性判定；降级运行标记；`--alpha-id` 模式取平台三段式 description 补 rubric 必填证据字段；补 `test_judge_gates_match_config.py`（脚本注释早引用、文件并不存在）→ JD-07 / JD-09 / JD-10 / JD-13
- 更正：`quota-and-tower.md` 的分档「差 1–2 颗一次点亮」（与「差 2 颗」重叠，且差 2 颗一次提交仍差 1 颗）；RA 文档里 `WAIT_THEME_ROTATION` 「judge 用同名结果值」的说法（没有代码实现）
- 规划文档 `improvement-roadmap.md` / `future-improvement-guide.md` 归档到 `attic/judge_planning_docs_20260929/`

**brain-alpha-robustness（「必经闸」有了代码落点）**
- 判定写 ledger `robustness_<alpha_id>`，`submit_verdict`（CLI / MCP / 批量）读取：REJECT → BLOCKED，CONDITIONAL / 无记录只提示（新模块 `wqb.robustness_record`，键进 `docs/ledger_keys.json`，单测在 `tests/unit/test_submit_verdict_core.py`）→ RB-03 / T0-18
- Phase A 拆分：闸门只读 `references/techniques.md`，论坛新发现只作「提案」（E 节）；`forum_cache_builder` 缓存路径改仓库内 → RB-04 / RB-05
- 删除「提交探测协议」（逐个提交读 prodCorr，提交即真实动作）；判定表更正（子宇宙引平台相对公式、算子数降软标记、Margin 标经验线）→ RB-10 / RB-15
- `allowed-tools` +`mcp__wqb-db__*`（写台账所需，能力基线已人审登记）

**wq-brain-alpha-optimization-v1（Mode B 资格单一真相源 + Mode A 收口）**
- 新增 `references/mode-b-qualification.md`：主闸 + 旁路 A–E + 判死线 + 覆盖优先级 + 各代码入口实际覆盖范围（judge 节点只喂 6 个指标，A / B / D 恒不命中）；「未达资格线一律判死」全库作废并由测试扫描禁止；新增只读 CLI `tools/mode_b_qualify.py`（同一判定函数、全指标）→ OP-18 / HP-15 / OP-11 / OP-13（`tests/unit/test_mode_b_qualification_doc.py`、`test_mode_b_qualify_cli.py`）
- `mode_b_config.py` 模块文档串的覆盖顺序更正（区域 ledger > 区域 thresholds > GLOBAL ledger > 内置），测试钉住
- Mode A：结果入库（不写自建文本文件）；算子上限标注 PPA-only；校验层固定三段（verifier → `ghost-audit` → `wave_gate --batch-type repair`）；主题算子表按 `known_ops` 分「已核验 / 未列入清单」栏（62 个里 35 个未在清单）；止损阶梯合并；删「70/30 精力」与分钟级预算；手抄阈值改引 `config` → OP-01…OP-17（`test_optimization_v1_docs.py`）
- 形态库：加「入场方式」五类可检判据；F1 限同源（用户 2026-09-28 `spread_signal_ruling`）；`hump` 状态统一 → OP-12
- arXiv：脚本全库只留一份；写明外发边界（查询词发 arxiv.org；`--llm` 才把公开摘要发第三方，密钥仅环境变量 / gitignore 的 `.arxiv_llm.env`）；`sync_skills` 不再复制 `*.env` → OP-04 / EX-06

**brain-how-to-pass-alpha-test / brain-alpha-repair / brain-explain-alphas / brain-calculate-alpha-selfcorr-quick**
- how-to-pass：SKILL §0 把 18 个 `RA_CHECK_NAMES` + SELF / PROD 逐项登记「平台线 / 内部线（config 键）/ 读哪节」；数值例（Fitness / 子宇宙）；§6 拆 SELF / PROD；CW 证据迁 `references/`；删 quota-via-submit 句；「FAIL 回流」改「建议路径（不执行）」；情景卡 → HP-01…HP-21
- `check_correlation` 环境事实（阻塞轮询、单并发、Redis 只是可选缓存、`refresh` 量化）只写 RA `prod-corr-avoidance.md` §1 一处 → HP-11
- repair：撤回不可恢复的「5 轴旋转 / 降相关 6 武器」，其余配方登记去向并由测试校验（「声明已上移的术语必须能 grep 到」）；description 退役触发词；三张情景卡 → RE-01…RE-12（`test_brain_alpha_repair_docs.py`）
- explain：真实 `get_datafields` 签名 + `filter_sharpe=False`；`vec_mean` → `vec_avg`；新增第 7 步概念重叠检查及只读程序 `tools/concept_overlap.py`；结构化「进一步启发」→ EX-01…EX-10
- selfcorr-quick：SELF / PROD 不互相推导；删「POST /submit 零成本实测」；脚本改 `importlib.metadata`、tqdm 缺失降级、非交互不安装、凭据环境变量优先、固定产物目录、Excel `Meta` sheet 与盲区自动警告 → SC-01…SC-10（`test_selfcorr_quick_script.py`）

**wq-backtest-monitor / planning-with-files / pull-brain-skills（L6 / L7）**
- monitor：重新定位为 S6「监控与复盘」（REGULAR / PPA / SUPER 通用）；写入 SOP 只在 RA 步 9，monitor 只触发并核验；命令模板按真实 CLI 重写（旧四条全错、其中一条写已废止的 `wave{W}_verdict` 键）并由测试对真实 argparse 校验；checkpoint 位置更正为 ledger `ckpt_w<wave>`；判停阈值只引 `config.WAIT_THRESHOLDS`；删「四关」、并发模型（改指 `config.CONCURRENCY`）、全部历史任务实例与「TOP800/1500/2500/5000 非法」的错误 universe 论断；OS 表现监控与重着色声明无承接者（INDEX / superalpha / submit-alpha 同步）；INDEX 的 `wave_results` 归属更正为「唯一写入函数 + 两个等价入口」→ BM-01…BM-18（`test_wq_backtest_monitor_docs.py`、`test_wait_thresholds.py`）
- planning-with-files：触发口径唯一、优先级「用户 > 领域协议 > 本 skill」；「永不重复失败」改为区分确定性 / 暂时性失败；PreToolUse 钩子只挂 `Write|Edit`（20 行）；钩子逐条写明成本；规划文件固定仓库根；INDEX 持久化铁律加豁免句、`version` / `hooks` 语义；新增 WQ 战役示例 → PW-01…PW-10（`test_planning_with_files_docs.py`）
- pull-brain-skills：SKILL 与代码默认值对齐（暂存目录、审查、不安装）并由测试守；空导入退出码 4、`--subdir`、ZIP 超时 + 大小上限；ZIP 示例用固定 commit；导入后清单、回滚、情景卡 → PB-01…PB-07（`test_pull_skills_safety.py`）

**worldquant-submit-alpha / GLOSSARY / decision-table / INDEX 等（提交链单一叙述）**：见 `reports/skills_review_20260929_closure.md` 的 SB-* / X-1 / X-2 / X-4~6 条目。

**已迁出本日志的历史（原 RA `SKILL.md` 里的日期叙述，按时间倒序，仅留一行）**
- 2026-09-28 · 闸 SEM 落地（GEM 之前必做，缺台账 exit 2；KOR fundamental17 首波 49.4% 落在货币 / 汇率非信号字段）；组合形态加严（等权 `add(rank,rank)` 同罪，`equal_weight_leg_add`）；`s6_verdict_<wave>` 废止（结论唯一源 = `wave_results.verdict`）；`forum_recon` 接线；提交层「唯一权威」改为「否决权威」（`GET /alphas/{id}/submit` 恒 404）；RA 外壳脚本 `ralph_daily_loop.py` / `ralph_runner.py` 归档到 `attic/ra_pipeline_shell_20260928/`（零运行痕迹）；未编排增强节点 `alpha_booster` / `modeb_improve` 去留登记
- 2026-09-27 · `assemble-priors` 节点写 DB 快照（此前只重写文件，GEM 读到旧快照）；S6 完成定义补「再跑 assemble-priors」；verdict 判定表与 `upsert_wave_result` 合并语义；三道开波闸接入 `batch_track`；停止规则 B 窗口按波开始时刻取
- 2026-09-26 · 审计补入边：步 8 挂上执行 skill（`worldquant-submit-alpha` / `wq-brain-superalpha`）；提交响应四态表（3 颗候选因只轮询不补发悬空 > 24 h）
- 2026-09-25 · 闸 PF（骨架级 prod-first 前置硬门）落地
- 2026-09-23 · 停止规则按轴（region × dataset）改版：B1 同轴熔断 / B2 区级多轴停
- 2026-09-20 · IS→OS 衰减校准接线（`os_decay.py`；Spearman 仅 +0.086，不抬 IS 阈值）
- 2026-09-19 · prod-first 升硬门；near 池不收结构性死信号（`ROBUST_STRUCTURAL`）；已点亮塔不进白名单（用户定案）；产出率严格口径；IND pv103 同日提交教训
- 2026-09-17 · `step_funnel.py`；signal_floor 改 fail-closed；`webdatascope-failed-gates` 资格门
- 2026-09-15 · 设置层先验（settings prior）；`region_kb` 波后自动刷新；`RN_EXPOSURE` 接线；停止规则 / 积压闸 SQL 化
- 2026-09-13 · 加权混合全局禁令（「路线 A」；同时废止 `MINING.slow_fast_mix`——0.40 / 0.60 慢快配比，只留作 2026-09-13 之前的历史配方）；先沉降、再封存（`seal_dead_end`）
- 2026-09-11 · 整链执行纠正（不是「九步可整条交给 workflow_chain」）；`wave_gate` 节点
- 2026-09-09 · `s4-prescreen`、`pyramid`、收批压缩（`harvest_multisim_alphas`）
- 2026-09-08 · 库存盘点先于新挖；`risk_neutralized_sharpe` 硬规则
- 2026-09-06 · signal_floor 接线；`--concurrency` 不存在导致 S3 从未真跑的修复；产出率先验
- 2026-08-25 · 区域 Profile 路由落地；并发由 5 → 7（Token-Bucket C≈7）
- `brain-deepExplore` 已废止并入 ra-pipeline；其 S2-D / S2-M 概念已废，见步 4

**引擎与执行层（campaign-matrix / campaign-toolkit / wqb-concurrency / sim-alphas / inspect-raw）**
- `wq-brain-campaign-toolkit`：SKILL 由 354 行追加式日志 → 251 行：description 702 字功能清单 → 173 字触发场景；「唯一权威实现 / 唯一正式写入方」删，改 §3 写入矩阵与 §1 toolkit-vs-`tools/` 分工表；「使用率分级」删，改「按阶段选脚本」；子命令表补全并删已归档脚本；「重发安全与异步恢复」独立成节（`outcome_unknown` 三步恢复）；产物契约表；二分排障合并成一份；文末日志与开发者流程（节点四处同步，AGENTS.md 已有）撤出 → TK-01…TK-35
- toolkit references 全部按代码核对重写：`gate-rules`（闸 5 列全 8 条毒模式、闸 6 过期 = FAIL-CLOSED、闸 7 只有 WARN、闸 8 更正为「引用即拦」、build_wave 改 DB 口径）、`poll-and-quota`（七槽 = 7、配额闸缺省关闭、`quota` 不区分通道）、`ledger-schema`（指向 `docs/ledger_keys.json`，`wave<N>_verdict` 标废止）、`campaign-dir-contract`（必需 / 可选 / 历史）、`probe-scoring-v2`（P60 / P30 / 0.7 是代码缺省）；`selection-plan` 拆出 `post-wave-reading`；新增 `diversity-extract`（合并 546 行三份说明）；`enhancement-v2` / `S2_COMPLIANCE_*` / `DIVERSITY_EXTRACT_*` 归档到 `attic/toolkit_docs_20260929/` → TR-01…TR-33
- `wq-brain-campaign-matrix`：重写为「存储地图 + 配置包字段表 + 回写规范 + 失败处置 + 三张情景卡」；不再复制九步派发链；`cross_region_lessons` 表标已废弃；开新区检查表移到 INDEX 唯一维护 → CM-01…CM-24
- `wqb-concurrency`：边界收回「只管并发」（台账 / 复盘 / 选波撤给 RA 步 1 / 步 9）；两个「安全包络」澄清为两个量（七槽 7 与保守档 6，后者当前无代码读取）；§2–§3 标「给引擎维护者」；SOP 步 3 换成 `harvest_multisim_alphas`；`validate_fields` 分场景；§4 / §8 / §8.1 编号不变（被 20 处引用）→ WC-01…WC-12
- `brain-sim-alphas-in-batch-and-track`：「唯一入口」改入口选用表（三入口各管一类）；长任务规则分 MCP / CLI 两路（60 分钟与 3 分钟判的是不同层）；第 3 份阶段映射表删；凭据标准名 `CREDENTIALS_*`；README / reference / examples 同步 → SA-01…SA-08
- `brain-inspect-raw-template-create-setting`：边界与步骤改为「外部 / 手写 idea → 核对设置 → 写 `expressions` 表」，GEM 已入库的批次不走本 skill（互斥）；`build_alpha_list.py` 新增 `--campaign-dir` 并**打印每个可选字段的来源**；`process_template.py` 新增 `--out-dir`；提示文案不再要求「交还 AI 做设置决策」→ IR-01…IR-08
- 代码（DEC-33…39）：MCP `get_submit_ready` 改读 SQL 队列表（ledger 同名键降 legacy 审计副本）；registry 写入校验唯一实现 `src/wqb/registry_contract.py`（CLI 与 MCP `upsert_registry_empirical` / `seal_dead_end` 共用，`seal_dead_end` 新建须带 `rule`）；`--enhance-diversity` 缺省 `always` → `never`（`build_wave.py` / `batch_simulator.py`）；`ledger set-verdict` / `submit-ready` 打印废止提示；`pipeline --force` 语义写准；三灯 `action` 不再推荐拼腿；L3 榨取窗口与探针 P6 收敛到有意义的窗口；gate 每进程打印所用 verifier 路径；作者盘符兜底全部移除（AST 测试守护）
- 测试：`tests/unit/test_sd_docs.py`（文档 ↔ 代码）、`test_sd_engine_contracts.py`（契约与缺省）、`test_sd_portability.py`（盘符）
