# Skills 变更日志

> 从各 SKILL.md 正文里迁出的「日期 / 新增 / 修正 / 事故」叙述。**规则在 SKILL.md 与 `references/`；日期与变更在这里。**
> 约定：新条目加在最上面；一条一行：`日期 · skill · 改了什么（为什么） → 证据 / 落点`。事故与起因写进对应 skill 的 `references/incidents.md`，这里只留指针。
> 决策与证据登记：[`docs/skills_review_decisions.md`](../../docs/skills_review_decisions.md)；逐条处置：`reports/skills_review_20260929_closure.md`。

## 2026-09-29 · skills 审查整改（`reports/skills_review_20260929.md`）

**伞形条目收口 / 区域 profile 对齐 / 全库扫描守护（S-F-2）**
- 伞形条目 P0-1…9 / T0-1…20 / X-1…19（共 48 条）逐项核验并收口：闭环台账 758 条 → 751 fixed / 3 declined / 4 needs-platform / 0 open，每条落到已有测试或本轮新增测试；台账新增「`verify` 指针必须仍指向存在的测试」检查（PW-09 的指针就是一个已改名的测试）→ DEC-61…66
- 区域 profile：EUR / DEU 的 `static.universe` 与默认档对齐 `config.REGIONS`（此前 EUR 仍列已被平台移除的 `ILLIQUID_MINVOL1M` 且默认 TOP1600、DEU 多列一个 config 没有的 TOP300）；EUR / KOR 的 `win_recipes` 种子不再记混合比例——该种子在 DB KB 为空时经 assemble-priors 进入 GEM 的 priors；新增三条 profile ↔ config 机检（universe ⊆ config 且默认相等 / delay ⊆ config / 已移除档位不得出现）→ T0-8 / DEC-61
- 全库扫描守护 `test_sf_sweeps`（11 条）：幽灵 / 未知算子（`ts_median` / `scale_down` / `vec_mean` / `is_placeholder`）与 `ts_event_*` 只许以警示口吻出现；加权 / 等权拼腿只许以反例出现或在文件头「现行政策提示」横幅之下（4 份 `docs/reference` 历史资料已加横幅，两份 SOP 的 `ts_event_*` 更正）；`confirm_submit=True` 只许与用户确认同行；`POST /submit` 不得当零成本探针教；一个文件只用一种 shell 方言 → T0-2 / T0-3 / T0-10 / T0-12 / X-3 / X-9 / X-14
- `skill_lint` 新增 `path-token` 检查（反引号里的仓库内路径必须存在，说明「不存在 / 已归档」的行豁免）；`last_verified` 两条测试（格式合法且不在未来；不早于最近一次改动该 skill 文档的提交，浅克隆下 skip）→ T0-20 / X-17
- 文档更正：RA `step5-gates.md`（`--export-expr` 的理由）、GBR / KOR / DEU / EUR profile、field-quality 参考（导出块改 PowerShell，注明日常生成器是 `gen_field_inspect_packs.py`）；`last_verified` 只对本次改过文档且已重新核对的 2 个 skill（`wq-brain-ra-pipeline`、`brain-alpha-research-field-quality`）更新为 2026-09-30，其余 31 个没有改动就不动
- **需要人看的**：GBR `stop_rules_override` 于 2026-09-30 到期（含当天）；`scale_down` 是否存在待平台复核（DEC-62，复核前文档按不可用处理）；其余待办与遗留见 DEC-66

**INDEX 拆分 / 契约 / 生成表 / 凭据登记（S-F-1）**
- INDEX 只做路由与分层（460 → 约 275 行）：新增首节「任务 → skill 场景路由表」；契约拆到新增的 `CONTRACT.md`（frontmatter 逐字段定义、`description` ≤ 300 字全库机检、硬裁定、共享产物归属、质量门禁）；全部日期条目 / 迁入记录 / 改名表 / 演进注记移入本文件末「更早的历史」→ IX-01…24 / DEC-58
- 可由代码导出的表改为**生成 + 逐字比对**：区域清单（config.REGIONS × profile × 目录，修掉 DEU / AMR 两处事实错误）、闸门阶梯（按检查名给平台线 / 内部线 / 来源常量，「平台 Sharpe 硬线」不再是一个数）、环境变量目录（新增 `docs/env_and_switches.md` + `docs/env_registry.json`，102 个变量，代码读了未登记 / 登记了不读都红）；生成器 `tools/index_tables.py`
- **行为变更**：sim-alphas `batch_simulator.py` 的凭据顺序改为环境变量 > `configs/config.json` > MCP `.env`（此前 config.json 排在环境变量之前），且启动前覆盖 vendored `ace_lib.get_credentials`——该库默认会把口令**明文写进** `~/secrets/platform-brain.json` → T0-15 / DEC-59
- `skill_lint` 新增 `const-literal` 类（门槛数字抄写棘轮，现存 29 处入基线）；`bare-python` 基线归零；GEM `trailSomeAlphas/README.md` 英文旧稿重写（清掉 `.qoder/skills`、旧产物路径、不存在的 `MOONSHOT_MODEL`）；`AGENTS.md` 更正「repair 配方已上移 optimization-v1」（并没有）并新增 §8.10 → DEC-60

**brain-data-feature-engineering / brain-make-some-gem（S-E-5）**
- feature-engineering：SKILL 重写为「两条产物路径」——节点 = 确定性模板（`source=feature_engineering_node`，GEM 不注入）/ agent 人工 = `source=manual`（注入）——与 `source → 是否注入` 对照表（对照 `gem.py::TEMPLATE_IDEAS_SOURCES`）；台账示例此前写 `source: "standalone"`，照做的人工产物会被 GEM 静默忽略；概念预算 8–12、GEM 摄入契约（Concept / Implementation Example / Expected Exposure）、示例换 `pv1` 真实字段并经真实 GEM 解析器 + 规范校验器实测；产物路径 `data/gem_runs/output_report/manual_…`；提纲只在 `OUTPUT_TEMPLATE.md`；验收改 4 项可检产物 → FE-01…13 / DEC-54
- make-some-gem：**更正**「两份 SKILL.md 拼进 LLM prompt」（旧文、内嵌 README、两处代码注释都写反；AST 测试钉死正文从不进 prompt）；priors 键与上限以代码为准；铁律 6 / 7 与 RA D3 / 闸 6 契约对齐；`mode_b_required` 动作；落库核对（`run_pipeline` 自己写 `expressions`）；失败表增 `402` / LLM 通道不可达；`reference.md` / `examples.md` 英文旧稿 → 中文重写 → GM-01…15 / DEC-55
- **行为变更**：GEM headless runner 凭据优先级改为「环境变量 > `config.json`」（此前 `config.json` 无条件覆盖环境变量）；`--ideas-file` 模式不再要求 `moonshot_api_key`；缺键只报键名；启动打印 `[cred]` 来源行；新增全空 `config.example.json`；`sync_skills` 不再把 `config.json` 复制到安装位（也不再同步 `*.log` 运行时日志——vendored `ace_lib` 一 import 就在 CWD 建 `ace.log`）→ DEC-56 / DEC-57
- 内嵌 dfe 副本纳入同步与守护（`sync_gem_embedded_skill.py` 改 pairs 制；`reference.md` 此前已漂移到 399 行旧稿）+ `GENERATED.md` 标记
- 可移植性：MCP `requirements.txt` 补 `tqdm` / `Jinja2`（vendored `ace_lib` / `helpful_functions` 顶层依赖，此前按文档建的 venv 里 GEM 等一 import 就失败）；`test_gem_skill_paths` 实跑解析认 POSIX venv 布局 → DEC-57

**field-quality / news-sentiment / hypothesis-first / dataset-exploration / datafield-exploration（S-E-4）**
- field-quality：`alphaCount` 先验**分阶段**（选方向用、造批服从 RA 步 3 §3.3、饱和集不叠加）；五个「拥挤度」数字标明各自的轴与源码（测试逐项对照）；区域切换预筛自检明示为工具级、未接入节点，数据包不覆盖的区域走 `--source exempt`；规则 13 补「理论下限 vs 硬门代码口径」两层 → FQ-01…08 / DEC-51
- news-sentiment：6 桶 / 每批目标明示为**指引、无代码闸**（`news_loop.py`、Beta 桶采样、`wqb news-refresh-portfolio` 都不存在），6 桶表内联并由测试对照矩阵；Tier A 改候选来源 + 路由前三查；Tier B 三分支；分类器事实更正（覆盖只有 news12、缓存路径、`novelty` 归 attention、无调用方）；news12 字段码 M → C；四份 `docs/reference/news*.md` 原位修正 → NS-01…06 / DEC-49
- hypothesis-first：条件激活（目录缺失由 agent 起草，取消与 RA「强制切换」的互锁）；取消无人读的 `field_semantics` YAML；类别词表单一来源 = `HYPOTHESIS_CLASSES`（此前代码与 SKILL 各一份互不重叠），`load_catalog` 拒收词表外的类；`judge()` 修「对照更好却判 partially_supported」；节点账本目录锚仓库根、单测不再污染仓库账本；补「构建 → 入库 → 闸 → 回测 → judge → 写回」回路 → HF-01…10 / DEC-50
- dataset-exploration：区域 → universe 表删（JPN 是有效区域）；评分只留指针；分类落 `s1_semantic_<ds>` + 分类法一览；调研默认不查论坛；范围控制；reference 436 行英文手册 → 精简中文 → DE-01…08 / DEC-53
- datafield-exploration：六法全部改为**平台算子目录内的算子 + 比较式**（`ts_median` 幽灵 / `scale_down` 不在目录 / `ts_event_*` 平台没有 / `? :` 过不了 MCP 静态语法闸），逐条过校验器；类型先行表按闸 3 / 闸 8；先离线体检包后在线最小集，每法「→ 交 FE」→ DF-01…08 / DEC-52
- INDEX S1 行去掉不存在的 `ts_event_*` 预处理项；`upsert_expressions` 文档补 `hypothesis` 来源标签

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

## 更早的历史（2026-09-29 从 INDEX 拆出，原样保留，一行一条；INDEX 只留规则与生成表）

**MCP 工具 / 节点计数变更史**（现值见 INDEX「MCP 工具/节点计数」，由测试守护）
- 2026-09-28 P4 · `forum_recon` 节点上线（18→19；论坛问题驱动只读检索，额度 = 以查出有效文章为标准），由 ra-pipeline 步 4 / 5 / 7 / 9 的 recon 触发点经 `workflow_execute` 调用
- 2026-09-27（N31）· `harvest_multisim_results` 复位为工具——09-19 起 `@mcp.tool()` 错挂在私有函数 `_flatten_platform_alpha` 上（该函数随之退出工具表，总数不变）；`workflow_auto_harvest` 带 `alphas` 时同样入库
- 2026-09-26 P2.1 · 移除 `workflow_field_understanding`（wqb-db 45→44）与 `field_understanding` 节点（19→18；重复的第三套 S1 实现，S1 字段理解走 `feature_engineering`）；同批修复 `auto_pyramid` / `auto_review` / `alpha_booster` / `modeb_improve` 假 dry-run（诚实构建命令 / 计划）
- 2026-09-18 · 新增 `persist_correlation`（相关性检查结果直落 `alphas`，NULL-only / [0,1] 校验 / source 溯源）与 `get_alpha_corr_metrics`（本地库筛选相关性，**零平台配额**）（wqb-db 43→45）；alphas 表 +9 列（sub_universe_sharpe / returns / drawdown / long_count / short_count / concentrated_weight / cluster_test / prod_corr_source / corr_checked_at），`CampaignStore.persist_correlation` 为唯一落库入口；`alpha_booster` 节点上线（18→19，通用 Alpha 短板提升，S4 增强）
- 2026-09-17 · 移除 6 个 wqb-db 工具（49→43）：`record_step_metrics` / `get_step_metrics` / `compute_wave_summary` / `compute_campaign_summary` / `get_step_gain_report` / `workflow_step_metrics`——step-metrics 子系统整体下线（归档 `attic/step_metrics_20260917/`），替代方案 `tools/step_funnel.py`（只读步级漏斗）；`step_metrics` 节点下线（18→17）、`modeb_improve` 节点上线（17→18）
- 2026-09-16 · wqb-db 含 `workflow_inventory_scan` / `workflow_gem_wave` / `workflow_unified_gate` / `workflow_auto_harvest` / `workflow_auto_review` / `workflow_auto_pyramid`
- 2026-09-15 · wqb-db 含 `set_expression_status`（批量改状态，只传 id / 状态过滤，不回传表达式正文）

**2026-09-19 挖掘流程优化落地（RA×10 战役复盘；细节见 wq-brain-ra-pipeline 各步）**
- ① 连坐隔离：`pipeline.py` ERROR 批解析子模拟 → 坏式回写 `expressions.status='fail'` → 无辜兄弟重发一次（`--no-isolate-errors` 关）
- ② 账户级槽位仲裁：`_lib/slots.py`（`logs/_slots/` token 文件，`WQB_GLOBAL_SLOTS` 缺省 7，陈旧自动回收），多流水线同跑不再超 C≈7
- ③ prod-first 探针：`tools/campaign_intel.py prod-first --region R --wave W` 收批后族级串行探 prod，STOP 族不扩变体；结果入 `alphas.prod_correlation` + ledger `prod_first_<wave>`
- ④ near 池剔除结构性死信号：`review_wave.is_near/structurally_dead`（robust/limit < `near.robust_min_ratio` 缺省 0.5）；metrics 行新增 `robust_sharpe/robust_limit/sub_universe_sharpe`；停止规则 B 因此真正可触发
- ⑤ 产出率严格口径：`get_mining_yield(strict=True)` 默认 `yield_rate=ra_clean/backtested`，另给 `prod_clean/prod_blocked/prod_wall_ratio`；`s0-select` 同源，并新增跨区负先验 / 字段数守卫 / maxS 列
- ⑥ GEM 生成侧预闸扩展：`hump` 命名参数、`bucket` 缺 range 补 / 丢、区域非法 group 字段（`platform_constraints.json` `region_invalid_group_fields`）、非标窗口别名归一、同骨架换字段封顶（`WQB_GEM_MAX_PER_SKELETON` 缺省 12）
- ⑦ 闸门：`gate.py` 闸 2b 区域非法 group 字段 FAIL；validator `bucket()` 必带 range / buckets
- ⑧ 台账修复：pipeline 收批写 `backtest_results.dataset`（此前恒 NULL，928 行）；历史空值回填（`backfill_backtest_dataset.py`，只填空）已一次性跑完并归档到 `tools/legacy/`，不再是可调用入口；`build_wave` 波号残留（全 dropped）时回退源池

**2026-09-15 接线修复（审计落地）**
- ① 设置层先验：`region_kb.gate_priors` 的 decay / neutralization 由 toolkit `pipeline.py run` 直接改写设置（`_lib/region_kb.py`），GEM prompt 只再注入 operator-count / field-family
- ② GEM：节点 / MCP 透传 `pipeline_mode`（runner 缺省 phased，skeleton 可达）；S1 模板渲染文档不再自动注入；落盘前 `pipeline_pregate.py` 归一 `quantile` 默认 driver、丢弃加权混合毒模式
- ③ 台账：`expressions.dataset` / `backtest_results.dataset` 污染已回填（`tools/backfill_expression_dataset.py`）；pipeline 收批后自动刷新 `region_kb`（recent_waves / gate_priors_local / updated_at）
- ④ `workflow_campaign(stage="S4")` 先解析本波 alpha_id 再拼 `review_wave.py --alphas`
- ⑤ `s2_field_pool` 跨主体簇轮转采样，`builder_version` 版本化缓存
- ⑥ S2-COMPLIANCE 降级为提示；`pipeline.py` 中止路径 rc=2
- ⑦ `RN_EXPOSURE` 墙进 `review_wave.walls()/passes()`；停止规则 SQL 化（`campaign` 节点 S2 / S3 前置，`stop_rules_override` 台账放行）；`wave_results.verdict` 写入强制枚举

**外部扩展区迁入记录（2026-08-23 完成）与并入 / 退役**
- 原「外部 Agent Skill 登记」段登记的 4 个 skill 历史上只存在于项目内 `.workbuddy/skills/_unpacked_brain/` 扩展区，2026-08-23 已全部迁入本权威目录并归层，外部扩展区随项目级副本一并归档：`brain-alpha-repair`（L4）、`brain-alpha-research`（L1）、`alpha-template-labs-data-analysis`（L0）；`brain-alpha-robustness` 已于 2026-08-22 迁入 L4，2026-08-23 同步到最新版本
- `brain-alpha-orchestrator` 2026-08-31 并入 `wq-brain-ra-pipeline`（独有硬门已迁移：ghost-op / PPA 门禁、check_batch + check_expr_against_inspect、批次故障协议、failed-count 资格门；「L-INT 编排层」随之取消）；`wq-brain-campaign-auto`（2026-08-22）与 `brain-deepExplore`（2026-08-24）均已并入 RA，触发词「一键战役 / auto campaign / 开战役 / 持续挖掘」归 ra-pipeline
- 通用非 WQ 元技能（`code-optimization`、`dead-code-cleanup`、`gold-analysis`、`jin10-news`）只由 `~/.workbuddy/skills` 独立维护，**不进入本目录**，避免 WQ 任务中误触发；历史 `.cursor/skills/` 冗余副本已于 2026-08-16 全部移除

**权威副本处置记录（2026-09-11 修订；2026-09-10 审计废止「以某个安装位为权威」——那是漂移反复复发的根因）**
- `<wqb>/.qoder-cn/skills/_unpacked_wq`（26 个，停留 08-17）→ 已归档 `attic/skills_archive/2026-08-23-pre-consolidation/proj-qoder-cn-skills/`
- `<wqb>/.workbuddy/skills/_unpacked_brain`（35 个，混合体）→ 已归档 `attic/skills_archive/2026-08-23-pre-consolidation/proj-workbuddy-skills/`
- `world-quant-brain-mcp/.venv/.../cnhkmcp/untracked/skills`（20 个，含已废弃 `brain-improve-alpha-performance`）→ 第三方包内僵尸副本，禁止调用，随包升级自行消失
- `~/.codex/skills` 2026-09-10 前不在解析链，导致长期分叉；`~/.cursor/skills` 的 WQ 技能为指向 `.claude` 的 Junction；`~/.qoder-cn/skills` 整目录 Junction 到 `~/.claude/skills`

**GEM 内嵌副本审计叙事（2026-09-26；2026-09-29 更正）**
- 2026-09-26 旧文称「嵌套副本是运行时依赖，不删除、不修改」——被实测推翻：内嵌 dfe 目录连 SKILL.md 都没有，`read_text_optional()` 失败返回空串，当时的结论是「顶层 322 行字段工程文档从未进入 LLM prompt 且完全静默（现已修）」
- **2026-09-29 再更正**：那两份 SKILL.md 的**正文从不进 LLM prompt**（`build_prompt` 只把 dfe「是否非空」当真值判断附一句固定的 8 问提示，FI 完全不用；AST 测试钉死）——所谓「静默屏蔽」的真实后果只是少一句固定提示，`MISSING` 的真正含义是 skill 目录解析异常 → DEC-55

**命名规范：2026-09-10 改名清单**（旧名禁止再出现在任何文档 / 代码 / 引用中；本条是历史记录，规则见 CONTRACT §3）
- 旧名 → 现名（迁移记录）：`pull_BRAINSkill` → `pull-brain-skills` · `brain-makeSomeGem` → `brain-make-some-gem` · `brain-simAlphasinBatch-and-track` → `brain-sim-alphas-in-batch-and-track` · `brain-calculate-alpha-selfcorrQuick` → `brain-calculate-alpha-selfcorr-quick` · `brain-how-to-pass-AlphaTest` → `brain-how-to-pass-alpha-test` · `brain-inspectRawTemplate-create-Setting` → `brain-inspect-raw-template-create-setting` · `brain-nextMove-analysis` → `brain-next-move-analysis`

**并发口径演进**（现值以 `config.CONCURRENCY` 为准）
- 2026-07 前：固定槽位 C=5（wqb-concurrency 阶梯实测）→ 新模型 Token-Bucket，突发容量 C≈7、慢补充约 1 令牌 / 20–40 s；2026-08-25 更新 5→7（七槽填槽：四重门禁后 7 批 multisim 同提实证安全，连续多波 0 连坐；每轮 7 批 × 8 条同提 → 统一轮询 → 即收即补）；旧「单批在飞串行」模式废弃；SOP 全文见 `wqb-concurrency` §8

**2026-09-19 平台区域硬事实（当日实测；已迁入对应 profile / 决策表，带各自的 `last_verified`）**
- `get_platform_setting_options` 含区域 **ALL**（D1，LARGE / MEDIUM / SMALL）与 **AMR**（TOP600）：ALL 不能跑 REGULAR（平台 400「Region ALL is not available for simulation type REGULAR」）；AMR 只有 sentiment7 + univ1、无 pv1；两者都不是 RA 挖掘区 → `region-profile-contract.md` §4
- JPN / TOP1600 / D1 无 pv1（close / adv20 / returns 全部 Invalid data field），`ts_*(vec_*(VECTOR))` 必 ERROR；GEM 预闸与闸 2b 按 `region_invalid_fields` / `vector_ts_forbidden` 处理 → `regions/JPN.md` 硬事实 6
- IND robust 闸 = 流动性子集重跑 Sharpe ≥ 1.0（官方 India Alphas 页）；日内反转族 IS 4–6 但 prod 0.79–1.0 撞墙；破 robust 墙的配方 = 自归一化 + 市值十分位 group_rank + decay 7–10（pwRJmvP3 ACTIVE 实证）→ `regions/IND.md`
- prod 竞速：prod 0.60–0.70 的候选必须当天提交（pv103 一小时内被外部同款堵成 1.0）→ ra-pipeline 决策表 D0-P 与 `references/incidents.md` I-2

**门禁与边界规则的来历**
- 2026-09-11：INDEX 曾引用的 `validate_skills.py` 本仓库并不存在（悬空引用），已替换为真实门禁（现行命令见 CONTRACT §5）
- 2026-09-26：新增「职责边界」必备段——审计实测边界声明覆盖率仅 39%（13 / 33），是选错 skill / 重复实现的主因；2026-09-27 补共享产物归属表——硬裁定②此前实质覆盖率仅 1 / 33，直接导致 `priors_snapshot` 无人认领刷新责任（GBR 快照落后 KB 源 8 天）、`wave_gate` 三方调用无主写方（自动链 100% `TypeError`）
