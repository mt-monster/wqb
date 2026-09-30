# skills 审查处置台账（闭环）

> 对应 `reports/skills_review_20260929.md`。**每个条目 ID 都有去向**；数据源 `docs/skills_review_closure.json`（`tools/closure_ledger.py` 维护，`tests/unit/test_closure_ledger.py` 守）。生成：`python tools/closure_ledger.py render`。

状态：**fixed** 本轮已改 · **superseded** 被别的改动一并解决 · **declined** 有意不改（含范本）· **needs-platform** 依赖平台实测或业务裁定 · **open** 未处理。

| 状态 | fixed | superseded | declined | needs-platform | open | 合计 |
|---|---|---|---|---|---|---|
| 条数 | 751 | 0 | 3 | 4 | 0 | 758 |

## T0

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| T0-1 | fixed | src/wqb/submit_verdict_core.py \| tools/submit_verdict.py \| Claude/skills/worldquant-submit-alpha/references/submit-chain.md \| Claude/skills/GLOSSARY.md | 状态机改写为可达（submit-chain.md §2 七步：资格门 → submit_verdict → prod 实测 → 用户确认 → POST → 轮询补发 → 回写），只依赖 UNVERIFIABLE / BLOCKED / ALREADY_SUBMITTED 三态（模块文档串明写「不得写『等 SUBMITTABLE』」）；退出码分开：0 = SUBMITTABLE / 1 = BLOCKED / 10 = UNVERIFIABLE / 11 = ALREADY_SUBMITTED（DEC-04），CLI / MCP / batch 三份判定收成 wqb.submit_verdict_core 一份，GLOSSARY 与 submit-chain 的退出码由测试对照代码。SUBMITTABLE 保留为防御分支——GET /submit 是否真恒 404 无法向平台复核（平台不可达） |
| T0-2 | fixed | Claude/skills/worldquant-submit-alpha/references/submit-chain.md \| tests/unit/test_sf_sweeps.py \| Claude/skills/worldquant-submit-alpha/SKILL.md | 全库一个警告块（submit-chain.md §0「不可逆动作块」），各 skill 只引用；「POST /submit = 零成本探针」在 12+ 处（RC-01 / SC-04 / HP-03 / RB-15 / RE-08 / RA-97 / SB-13 / SB-19 / SP-13 …）已改成「没有零成本 POST 探测；探测一律 confirm_submit=False 预检 / check_correlation 只读」；test_sf_sweeps 全库扫「POST … submit … 探针 / 零成本」句式，没有否定 / 警示口吻即红 |
| T0-3 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md \| tests/unit/test_sf_sweeps.py \| tests/unit/test_submit_chain_defaults.py | 示例拆两步：先 confirm_submit=False 预检，再「仅在用户确认后」的 True 版；不存在的形参（dataset / wave / expr_family）删；workflow_submit_alpha 缺省 confirm_submit=False、color 缺省不再是 GREEN（DEC-09）；test_sf_sweeps 扫全库：confirm_submit=True 只许与「用户确认 / 不可逆」同行出现 |
| T0-4 | fixed | src/wqb/workflow/nodes/submit_alpha.py \| tools/super_build.py \| Claude/skills/wq-brain-superalpha/SKILL.md \| tests/unit/test_submit_alpha_super_guard.py \| tests/unit/test_super_build_prod_gate.py | SUPER 唯一入口 super_build.py {select\|status\|probe\|submit}（= workflow_superalpha(confirm_submit=True) 的最后一步，prod 闸在 CLI 内置：max ≥ 0.7 或探针超时一律拒，--allow-prod-above-07 是显式豁免）；submit_alpha 节点在任何副作用之前拒绝 type==SUPER 的 confirm_submit=True（reason=super_requires_super_build，force 无效）——MCP 路径 force=True 绕 prod 闸不再可能（DEC-18）；superalpha 补「如何创建 SA」的调用序列与不可逆动作块，「预检 = 真提交」的说法删。GET /submit 对 SUPER 与 REGULAR 是否一致未复核（SP-11 needs-platform），文档一律「不得用它放行」 |
| T0-5 | fixed | Claude/skills/brain-alpha-judge/SKILL.md \| Claude/skills/brain-alpha-judge/scripts \| tests/unit/test_judge_never_submits.py | judge 脚本删掉全部提交路径：--confirm-submit 在任何网络调用前就大声失败、client 的 submit_alpha 已删且不发请求、全部 judge 脚本不得含 POST /submit（参数化测试逐个文件守）；PPA 口径取 config（Sharpe 线 1.0 = 平台 LOW_SHARPE，颜色 PURPLE 脚本不校验并明写；Regular 用内部线，不再把合法 PPA 按 Regular 1.58 误杀）；CW 配方推荐改指 how-to-pass §4（时间平滑），删被禁的加权相加 |
| T0-6 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/references/mode-b-qualification.md \| src/wqb/workflow/mode_b_config.py \| tools/mode_b_qualify.py \| tests/unit/test_mode_b_qualification_doc.py \| tests/unit/test_mode_b_qualify_cli.py | 判定表单一真相源 optimization-v1/references/mode-b-qualification.md（主闸 + 旁路 A–E + 判死线，数值与动作文案由测试对照 mode_b_config 的 _DEFAULT_GLOBAL，另钉覆盖优先级 区域 ledger > 区域 thresholds > GLOBAL > 内置）；HP-15 / OP-18 / RA 步 7 改引它；新增只读 CLI tools/mode_b_qualify.py 补上 judge 节点喂不到的旁路 A / B / D；no_qualify ≠ 判死，旧措辞「未达资格线一律判死」由测试扫全部 skill 文档禁止（DEC-24） |
| T0-7 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md \| tests/unit/test_wq_backtest_monitor_docs.py | 回写 SOP 只在 RA 步 9，monitor 只触发 + 核验；命令模板按真实 argparse 重写，并由 skill_lint 的 cmd-flag / cmd-required 检查 + test_wq_backtest_monitor_docs 对照真实 CLI（此前 4/4 与 CLI 不符，且旧检查只核 flag 名是否出现在同目录脚本里，一条没抓到）；旧键 wave<N>_verdict / s6_verdict_<wave> 只以「已废止，不要写」出现（ledger set-verdict 仍会写它，但每次打印废止提示，DEC-30 / DEC-36），结论唯一来源 wave_results.verdict |
| T0-8 | fixed | Claude/skills/wq-brain-ra-pipeline/references/regions/EUR.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/DEU.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/GBR.md \| src/wqb/config.py \| tests/unit/test_region_alignment.py \| tests/unit/test_config.py | monitor 的「TOP2500 / TOP800 非法」说法已删，一律取 config.REGIONS[region].universes；ILLIQUID_MINVOL1M 已从档位表移除（2026-09-22 实测）且对 USA / ASI / EUR 永久停提（2026-09-14 公告），文档只以「已移除 / 不得」口吻出现。本轮补完 profile 层残留：EUR profile 的 static.universe / default 改为与 config 一致（此前列 TOP1600 / ILLIQUID_MINVOL1M、默认 TOP1600，而平台档位表是 TOP2500 / TOPCS1600 / TOP1200 / TOP800 / TOP400、默认 TOP2500），step-6 探索队列去掉 ILLIQUID_MINVOL1M，DEU 多列的 TOP300 去掉（config 只有 TOP500；待平台实测后由 config 补入），并新增机检：profile 的 static.universe ⊆ config.REGIONS[r].universes、default 相等、delay ⊆ config（DEC-61） |
| T0-9 | fixed | Claude/skills/INDEX.md \| tools/_pyenv.py \| tools/skill_lint.py \| tests/unit/test_pyenv.py \| tests/unit/test_sd_portability.py | $WQ_PY 在 INDEX 按平台给三行（Windows Scripts/python.exe、POSIX bin/python、跨平台自动探测 tools/_pyenv.py，顺序由测试对照源码）；skill_lint 的 bare-python 棘轮把全库裸 python 数成 0（目标脚本已接 _pyenv 自动切 venv 者豁免）；<SKILL_ROOT> 只在 CONTRACT 里定义为文档记号，钩子命令不得含未解析占位符（测试守）；运行时代码里的作者盘符兜底约 14 处清掉（DEC-37，test_sd_portability 守）；PowerShell / bash 混用见 X-14（一个文件只用一种方言由测试守） |
| T0-10 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/references/structural-interaction-forms.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py \| tests/unit/test_gate5_coverage_matrix.py \| tests/unit/test_sf_sweeps.py \| docs/reference/combination_optimization_strategy.md | 一条规则：禁止把两条及以上独立信号腿按任意（等 / 非等）权重线性相加，无论函数式 / 中缀 / 减号；允许的只有 structural-interaction-forms.md 的形态与单信号结构；同源价差 subtract(A,B) 是唯一豁免（platform_constraints.spread_signal_ruling，用户 2026-09-28 裁定）。闸 5 覆盖矩阵（形态 × 权重位置 × 运算）期望值写在测试里：报告实测放行的 rank(A)*0.6+rank(B)*0.4、V9 的 X+Y*0.35 现被 infix_leg_sum 拦，subtract 同源价差放行、跨数据集价差被 spread_cross_dataset 拦、带系数价差只告警。文档侧：各 SOP 的加权示例改写或标 counterexample，纯历史资料（4 份 docs/reference）加「现行政策提示」头部横幅，EUR / GBR / KOR profile 的 win 配方去掉混合比例；test_sf_sweeps 全库扫描防回潮 |
| T0-11 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/incidents.md \| tests/unit/test_se_docs.py \| tests/unit/test_optimization_v1_docs.py \| docs/skills_review_decisions.md | 一张表（decision-table D0-P，「唯一决策表」，DEC-07）：< 0.60 扩变体；0.60–0.70 不扩变体当天进步 8；0.70–0.75 踩线带只许 1 次结构性尝试，仍 ≥ 0.70 → dead_end；≥ 0.75 直接 dead_end；镜像稀释撤回（它是腿相加）；区域 profile 不得另设预警线；RA 步 5b / 7、OP、RC、RP、RR、RE、SP 逐处改引 D0-P；事故记入 incidents.md I-15。**注意**：表中的实证（MEA 9qXoJge2 0.716→0.6525、KOR wave113 0.7003→0.6993 等）来自历史记录，未能向平台复核 |
| T0-12 | fixed | tools/skill_lint.py \| tests/unit/test_sf_sweeps.py \| tests/unit/test_ghost_operator_lists.py \| src/wqb/config.py | 幽灵 / 未知算子：ts_median 判幽灵（MCP operator_audit 实测，DEC-02）、scale_down 不在 103 算子目录、ts_event_* 平台没有（闸 8 已直接 FAIL）、vec_mean 应为 vec_avg、is_placeholder 不存在——SOP / reference / docs/reference 一律移除或只以警示口吻出现（test_sf_sweeps 全库扫）；幽灵单源 = config.GHOST_OPERATORS ∪ platform_constraints.ghost_ops 再减去账号不可用者（DEC-03，test_ghost_operator_lists 守）；「SOP 算子 ∈ known_ops」机检 = skill_lint 的 expr-gate（fenced / 行内表达式过 gate.check_one 的 GHOST / INACCESSIBLE / SYNTAX / ARITY，反例语境豁免）。scale_down 的平台实测复核见 X-16（needs-platform） |
| T0-13 | fixed | Claude/skills/brain-alpha-repair/references/repair-recipes.md \| Claude/skills/INDEX.md \| AGENTS.md \| tests/unit/test_brain_alpha_repair_docs.py | 同 P0-6：repair 的「5 轴旋转」「降相关 6 武器」原文遗失不可恢复，声明撤回（不假装恢复）；其余 4 项在别处有并登记去向；INDEX 卖点更正；「声明已上移的术语必须 grep 到承接侧」由 test_brain_alpha_repair_docs 逐行校验，AGENTS.md 同步更正（DEC-27） |
| T0-14 | fixed | src/wqb/timeutil.py \| tools/quota_status.py \| Claude/skills/worldquant-submit-alpha/references/quota-and-tower.md \| docs/time_bombs.json | 配额只留一处（submit-alpha references/quota-and-tower.md，INDEX 只留指针）；activities/submissions 全库统一「不可用」，当日数以 quota_status.py 为准；日界用 America/New_York（wqb.timeutil，缺 tz 数据库时回退到规则实现，逐小时等价性有测试），quota_status.py 与 pipeline.py 不再写死 UTC-4；文档不再写死「12:00 GMT+8」（夏令时 12:00 / 冬令时 13:00，以 quota_status 输出为准）；2026-11-01 DST 结束登记为 TB-03（kind=code，无需人工）；SubmissionsMixin.get_quota_status（48h 滚动口径，无调用方）已删（DEC-11） |
| T0-15 | fixed | docs/env_and_switches.md \| docs/env_registry.json \| tools/skill_lint.py \| tests/unit/test_sf_docs.py \| tests/unit/test_judge_never_submits.py \| tests/unit/test_sync_skills_ignores_secret_files.py | 标准名 CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD（旧别名保留）；docs/env_and_switches.md §1 登记 9 个消费者的来源顺序与是否落盘；judge 只读进程环境变量（明文 config.json / ~/secrets 不再读，发现时 stderr 提示迁移、不打印值）；batch_simulator 改「环境变量 > config.json > .env」并覆盖 ace_lib.get_credentials，不再向 ~/secrets/platform-brain.json 明文写盘；GEM runner 环境变量 > config.json（DEC-56）；skill_lint 的 env-read / cli-password 守「文档不得指示读 .env / 命令行传口令」；sync_skills 忽略 config.json 与 *.log，不把密钥文件复制到安装位；外发 4 条通道登记（GEM → Moonshot 缺省开、judge → LLM 缺省关且表达式原文默认不发、arXiv 摘要、论坛检索），论坛 / 付款 MCP 工具删 email / password 参数（DEC-44）。本轮没有读取任何真实 .env / config.json |
| T0-16 | fixed | Claude/skills/pull-brain-skills/SKILL.md \| Claude/skills/pull-brain-skills/scripts/pull_skills.py \| Claude/skills/planning-with-files/SKILL.md \| Claude/skills/CONTRACT.md \| tests/unit/test_pull_skills_safety.py \| tests/unit/test_skill_hooks_and_tools_guard.py | pull-brain-skills：默认目的地 = 隔离暂存区 attic/import_staging 且文档默认值 = 代码默认值（测试对拍）；静态审查报告（hooks / allowed-tools / scripts / 符号链接 / 风险模式 / 同名碰撞）；--overwrite 不再 rmtree——旧目录移开备份、示例不带；ZIP 路径穿越拒绝、下载大小 / 超时有界、空导入退出码 4（DEC-32）。planning-with-files：Stop 钩子改内联、永不阻塞、不含未解析占位符；hooks 受限白名单 + 逐条写明成本（CONTRACT §1），test_skill_hooks_and_tools_guard 守「只有审过的 skill 可声明 hooks」「钩子命令可解析且无害」「allowed-tools 不得超过基线」 |
| T0-17 | fixed | Claude/skills/INDEX.md \| Claude/skills/CONTRACT.md \| tests/unit/test_index_tables.py | INDEX「允许写的文件只有五类」表：A 真相源 DB / B 运行态缓存 / C 静态配置与凭证 / D CLI 临时 @file / E 人读产物；各 skill 按类改写（OP-06 回测结果走 harvest 入库、IR-02 / SA-03 的 alpha_list.json 与 status CSV 标运行态缓存、FI-05 final_expressions.json 标中间产物非真相源、RD-21 WAVE_LEDGER 归 E、BM-15 手工回写删）。**未做**：「文档里每个文件路径都须归入其中一类」的通用归类器——只做到路径必须存在（skill_lint path-token）+ 关键产物位置由各 skill 的 doc→code 测试钉住（DEC-65） |
| T0-18 | fixed | src/wqb/robustness_record.py \| tools/campaign_intel.py \| docs/ledger_keys.json \| tests/unit/test_campaign_intel_mark_saturated.py \| tests/unit/test_ledger_key_catalog.py \| Claude/skills/wq-backtest-monitor/SKILL.md | 逐行对照（X-18 表）：S6「OS 表现监控 / 重着色」明确声明无承接者（BM-01，RA 步 9 §9.8 登记，不再假装有）；robustness「必经闸」补代码落点——判定写台账 robustness_<alpha_id>，submit_verdict 三入口读取，REJECT → BLOCKED，CONDITIONAL / 无记录只提示（DEC-23）；S6→S0 反馈环接通——新增 campaign_intel.py mark-saturated 写 saturated_datasets，submit_ready_blocked 降 deprecated（DEC-13）；其余有主无人读的键登记为 orphan 且测试守「登记必须仍为真」（DEC-12，seat_model / template_kb / operator_principle_kb）；X-18 表 15 行涉及的 18 个逐条 ID 均已在各 skill 收口（EX-01 补概念重叠程序、RE-10 删无写入方的要求、SB-22 补交接单、FQ-07 写明未接线……） |
| T0-19 | fixed | Claude/skills/CONTRACT.md \| tools/skill_lint.py \| tests/unit/test_skill_boundaries.py \| tests/unit/test_sf_docs.py | 边界声明与正文 / 代码的矛盾逐个改正（IX-19、SB-02、JD-02、BM-03、SP-02、HP-01、RE-02 均已收口，各自带 doc→code 测试：submit-alpha 不再自称「唯一提交判定」、judge 不再自称评审入口、monitor 不做 OS 监控、superalpha 入口表列全……）；CONTRACT §2 写明「边界『不做』的动作出现在正文须带『仅引用』标记」；实质一致性靠各 skill 的 doc→code 测试 + skill_lint（命令 / MCP / 表达式 / 路径 / 常量）。**未做**：报告提议的通用「边界动作词 ↔ 正文」语义检查——误报率高、需要人写词表，收益不抵成本（DEC-64） |
| T0-20 | fixed | tools/skill_lint.py \| tests/unit/test_skill_lint.py \| Claude/skills/brain-next-move-analysis/SKILL.md | 死指针 / 死命令清零：不存在的 CLI（wqb research / settings / news-refresh-portfolio）、脚本（backfill_backtest_dataset.py、get_ny_time.py、collect_verified_pids、logs/_fix_desc_sa4.py）、文档（prod_wall_breakthrough_sop.md、fresh_datasets_7region.json）现在要么已删、要么只以「不存在」的口吻出现；机检接入测试：skill_lint 的 cmd-* / mcp-* 与新增的 path-token（反引号里的仓库内 .py / .md / .json / .yaml 路径必须真实存在，行内说明「不存在 / 已归档」的豁免），并与基线棘轮配合——新增死指针必红 |

## X

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| X-1 | fixed | Claude/skills/wq-brain-ra-pipeline/references/decision-table.md \| Claude/skills/wq-brain-ra-pipeline/references/incidents.md \| tests/unit/test_se_docs.py | 同 T0-11：唯一决策表 D0-P；其余文档（RA 步 5b / 7、D14、OP、RC、RP、RR、RE、SP、区域 profile）一律引用，不得另立学说；镜像稀释撤回；prod 一律用 check_correlation 只读取数，禁止 POST /submit 探测。表内实证来自历史记录，未能向平台复核（DEC-07） |
| X-2 | fixed | Claude/skills/worldquant-submit-alpha/references/submit-chain.md \| tools/authority_claims.py \| Claude/skills/GLOSSARY.md \| tests/unit/test_glossary_docs.py | 「权威」拆成两个词并全库统一：否决权威（资格门 / submit_verdict / prod 实测 / 稳健性闸，只能拦不能放）与放行权威（用户明确确认 + workflow_submit_alpha(confirm_submit=True)）；提交链写成可达状态机（submit-chain.md §1–2）；「唯一权威」类宣称登记（tools/authority_claims.py + 基线，只许减少，INDEX 现存 4 处）；GLOSSARY 收词 |
| X-3 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/references/structural-interaction-forms.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py \| tests/unit/test_gate5_coverage_matrix.py \| tests/unit/test_weighted_mix_structural_gate5.py \| tests/unit/test_sf_sweeps.py | 同 T0-10：一条规则 + 形态白名单（structural-interaction-forms.md）+ 闸 5 覆盖矩阵测试 + 文档扫描防回潮；同源价差 subtract 的地位按用户 2026-09-28 裁定写入 platform_constraints.spread_signal_ruling，闸 5 报错文案指向合规替代 |
| X-4 | fixed | Claude/skills/GLOSSARY.md \| tests/unit/test_glossary_docs.py | 术语表 Claude/skills/GLOSSARY.md（一词一义：信号族 = 代码里 _pf_family 的字段集合粒度〔DEC-14〕、提交 / dispatch、否决 / 放行权威、FAIL / PENDING / WARNING 等），各 skill 只引用；test_glossary_docs 校验：登记行指向的文件 / 符号 / 测试真实存在、文档里写的限定符号存在、GLOSSARY 从 INDEX 可达 |
| X-5 | fixed | Claude/skills/GLOSSARY.md \| tests/unit/test_glossary_docs.py \| tests/unit/test_wave_verdict_enum.py | verdict / 状态词表收敛到 GLOSSARY 的词表节，并由测试钉「代码枚举必须出现在词表」（提交判定四态、wave_results.verdict 枚举、稳健性三态……）；wave verdict 归一化只有一处实现（N30c）；**未做**：「文档里出现的每个状态词都必须在登记表」的反向检查（DEC-64） |
| X-6 | fixed | src/wqb/waiver.py \| tools/waiver.py \| Claude/skills/INDEX.md \| docs/env_and_switches.md \| tests/unit/test_waiver.py | 闸门模式开关统一为 waiver 协议 + 生成表：wqb.waiver.GATE_POLICIES 是单源，INDEX 的「闸与逃生口总表」与 docs/env_and_switches.md 的开关表由 tools/waiver.py gates --markdown 生成并逐字比对（形态 / 默认 / 有效期 / 批准人一栏看全）；含日期翻转的开关（--gate-mode warn → enforce，2026-10-12）登记为 TB-02，翻转后措辞由 time_bombs 测试提醒 |
| X-7 | fixed | tools/index_tables.py \| tools/ledger_keys.py \| docs/ledger_keys.json \| docs/env_registry.json \| tests/unit/test_index_tables.py \| tests/unit/test_gate_registry_docs.py | 通则落地：凡可由代码导出的表都由代码生成并嵌入文档、测试比对——闸表（gate.py GATE_REGISTRY）、开关表（waiver）、区域表 / 闸门阶梯（tools/index_tables.py）、环境变量目录（docs/env_registry.json 与代码扫描双向核对）、ledger 键目录（docs/ledger_keys.json）、MCP 工具 / 节点计数（test_docs_consistency::test_mcp_tool_counts_match_index）；validator 有 1 份权威 + 3 份逐字节相同的镜像，并有测试守（DEC-41）；人写的「唯一」宣称登记进 authority_claims 基线（X-2） |
| X-8 | fixed | src/wqb/waiver.py \| tools/waiver.py \| tests/unit/test_waiver.py \| tests/unit/test_wave_gate_waiver_phase.py | 统一 waiver 协议（DEC-06）：ledger 键 waiver_<gate>_<region>_<wave\|all>，值 {gate, reason_code, evidence, approved_by, created_at, expires_at}；wqb.waiver 是唯一实现，expires_at 必填、按闸限批准人与最长有效期、红线不可豁免；旧键继续识别（缺 until 仍放行但告警 NO_EXPIRY）；gate 报告首行打印被豁免的闸；逃生口缺省 warn（无 waiver 只在首屏告警），--waiver-mode enforce 才拒绝 |
| X-9 | fixed | Claude/skills/worldquant-submit-alpha/references/submit-chain.md \| Claude/skills/wq-brain-superalpha/SKILL.md \| docs/env_and_switches.md \| tests/unit/test_sf_sweeps.py \| tests/unit/test_workflow_chain_irreversible_guard.py | 「不可逆动作块」模板落地并各处引用：POST /submit（submit-chain.md §0、superalpha、RA）、force=True（submit_alpha 节点拒 SUPER）、judge 提交路径（删）、super_build.py submit、pull_skills --overwrite（移开备份）、hooks（CONTRACT 白名单）、LLM 外发与凭据来源（docs/env_and_switches.md §1）、PPA web UI 提交（交接单 + 回写命令）；「探测」一律改只读手段（check_correlation / confirm_submit=False 预检），并有全库扫描测试与「提交类节点不入链」的代码强制（DEC-15） |
| X-10 | fixed | Claude/skills/CONTRACT.md \| Claude/skills/CHANGELOG.md \| tests/unit/test_ra_sop_template.py \| tests/unit/test_sf_docs.py | 结构：核心 SKILL.md ≤ 251 行（RA 由 950 降到 220，最长的 toolkit 251，略超 250 的目标）+ references/ 按需加载 + 仓库级 CHANGELOG.md；RA 九步固定模板（目的 → 前置 → 调用 → 产物 → 完成定义 → 失败分支 → 不做什么，test_ra_sop_template 守）；7 个 skill 有情景卡（judge / repair / how-to-pass / submit-alpha / monitor / RA / superalpha）；description ≤ 300 字触发语句（全库机检）；带日期的快照移 CHANGELOG / profile 或登记 time_bombs |
| X-11 | fixed | src/wqb/config.py \| tools/skill_lint.py \| tests/fixtures/skill_lint_baseline.json \| tests/unit/test_threshold_relations.py \| tests/unit/test_judge_gates_match_config.py | config 内把「平台线」与「内部线」按检查名分开登记（GATES_INTERNAL / GATES_PLATFORM / PLATFORM_CHECK_LINES，IX-10）；并发 C = 7、等待阈值取 WAIT_THRESHOLDS；文档阈值字面量由 skill_lint 的 const-literal 检查守——数值与 config 当前值相同而没有引用常量名 / config.X / from config.X 标记即违规，**现存 29 处登记进基线（新检查类别的初始基线，不是掩盖新违规）**，新增必红、修复必须从基线移除（DEC-60）。config 改值后旧抄写不再命中——交 last_verified 与 time_bombs 兜底 |
| X-12 | fixed | Claude/skills/INDEX.md \| Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md \| docs/time_bombs.json \| tests/unit/test_time_bombs.py | 日期快照（stop_rules_override 至 09-30、区域数据集计数、monitor 舰队、INDEX 09-19 区域硬事实、区域名单 13/14 / AMR·JPN 未启用）：区域名单改由代码生成；区域平台事实进各区 profile 与 region-profile-contract §4 且带日期；monitor 的具体 alpha / 数据集舰队删；带日期的状态一律进 CHANGELOG 或 docs/time_bombs.json；文档里出现未登记的未来日期即红（test_time_bombs）。**遗留**：tracking/GBR\|KOR/priors/*.json 仍是含 T-KB-01 加权配方的历史快照（数据文件，待 DB template_kb 清理后由 assemble-priors 重新生成），本轮不手改数据（DEC-66） |
| X-13 | fixed | Claude/skills/INDEX.md \| tests/unit/test_index_tables.py | 同 T0-17：五类允许写的文件表进 INDEX（A 真相源 DB / B 运行态缓存 / C 静态配置与凭证 / D CLI 临时 @file / E 人读产物）并有测试；仍要求写文件的文档（OP-06 / IR-02 / SA-03 / RD-21 / FI-05 / TR-06 / BM-15 / HF-04·09 / IX-08）逐条按类改写。通用「路径 → 五类」归类器未做（DEC-65） |
| X-14 | fixed | Claude/skills/INDEX.md \| tools/_pyenv.py \| tools/skill_lint.py \| tests/unit/test_sf_sweeps.py \| tests/unit/test_pyenv.py \| tests/unit/test_mcp_config_portable.py | $WQ_PY 三平台定义 + tools/_pyenv.py 自动探测；bare-python 棘轮 = 0；<SKILL_ROOT> 只在 CONTRACT 定义、钩子不得含占位符；作者盘符兜底清掉；ET 用 America/New_York；Get-CimInstance 无 Linux 等价命令的段落（BM-04）补 POSIX 写法；一个文件只用一种 shell 方言（本轮把最后一处混用改齐并加全库测试）。**否决**：全库整体统一 shell（推荐 PowerShell 主）——现有 31 个 PowerShell 块 / 32 个 bash 块是各 skill 的既有取向，命令都经 $WQ_PY，强行统一收益低、改动面大（DEC-63）；.mcp.json 保留作者的 Windows 默认（非 Windows 环境须设 WQB_HOME / WQB_MCP_PY / WQB_DB_MCP_PY，见 INDEX 与 env_and_switches） |
| X-15 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/poll-and-quota.md \| src/wqb/config.py \| tests/unit/test_wait_thresholds.py \| tests/unit/test_glossary_docs.py | poll-and-quota.md 建了唯一的「等待 / 退避 / 卡住阈值表」，其余文档按键名引用；代码字面量取自 config.WAIT_THRESHOLDS（提交翻转窗口 240 s 由节点与 MCP 工具共用、prod 相关性轮询、模拟卡住 / 超时与 toolkit poller 一致、super_build 无不可达 sleep），test_wait_thresholds 钉死；文档里复述窗口数字而不引用键名会红（test_glossary_docs） |
| X-16 | needs-platform | DEC-62 | 已做：SOP fenced / 行内表达式过 gate.check_one（skill_lint expr-gate：GHOST / INACCESSIBLE / SYNTAX / ARITY / POISON，反例语境豁免）；ts_median / vec_mean / is_placeholder / ts_event_* 只以警示口吻出现（test_sf_sweeps）；VECTOR 规则（先 vec_* 聚合、MATRIX 禁 vec_*）口径对齐闸 3；非标窗口走白名单 + 证据脚注（window_whitelist）。**待平台**：scale_down 是否真不在平台——现有依据只有 docs/reference/operators_catalog.json（103 个算子，2026-09-07 抓取，无 scale_down）与「幽灵单源」里没有它；平台不可达，无法用当前 get_operators 复核；复核前文档一律按不可用处理（安全侧）。DEC-62 |
| X-17 | fixed | tools/skill_lint.py \| tools/authority_claims.py \| tools/closure_ledger.py \| docs/time_bombs.json \| tests/unit/test_skill_lint.py \| tests/unit/test_closure_ledger.py \| tests/unit/test_sf_docs.py | 报告 14 项检查逐项状态：#1 命令→argparse 子命令级（skill_lint cmd-*）、#2 MCP 名与参数（mcp-*）、#3 链接与路径 token（test_docs_consistency 链接 + skill_lint path-token）、#4 阈值字面量（const-literal，初始基线 29）、#5 fenced 表达式过闸（expr-gate）、#6 ledger 键目录（docs/ledger_keys.json + test_ledger_key_catalog）、#7 闸 / 区域 / 开关 / 环境变量 / 计数由代码生成并比对、#9 「唯一 / 权威」登记（authority_claims 基线只减不增）、#10 last_verified 不得早于最近一次改动该 skill 文档的提交（git 判定，浅克隆下 skip）且格式合法不在未来、#11 未来日期条件登记（time_bombs）、#13 守护输入可指定（WQ_SKILLS_DIR）、#14 裸 python / .env 读取 / 命令行口令 / hooks / allowed-tools 白名单；另加：闭环台账的 verify 指针必须仍指向存在的测试（本轮新增）。**未做**：#8 完整的 verdict 词表（只做到代码枚举必须出现在 GLOSSARY）、#10 的「> 30 天告警」、#12 通用边界动作词语义检查（DEC-64） |
| X-18 | fixed | docs/ledger_keys.json \| tools/campaign_intel.py \| src/wqb/robustness_record.py \| tests/unit/test_ledger_key_catalog.py \| tests/unit/test_campaign_intel_mark_saturated.py | 同 T0-18：15 行「声明存在、实现缺位」逐行处置——补实现 4 项（robustness 读取、mark-saturated 写入口、EX-01 概念重叠程序、PPA 交接单 + 回写命令）；撤声明 / 明写「没有实现」5 项（S6 OS 监控与重着色、judge 的 WAIT_THEME_ROTATION、judge 引用 robustness、repair 配方、repair 的 trajectory_steps）；改口径 / 补流程 6 项（SA 创建入口列全、FQ-07 写明工具级未接线、hypothesis-first 条件激活、methodology_rules 计数由代码自动完成、配额复检不再 POST、check_correlation 的环境事实更正）；仍缺写入方的键登记为 orphan 且测试守「登记必须仍为真」 |
| X-19 | fixed | docs/time_bombs.json \| src/wqb/timeutil.py \| src/wqb/waiver.py \| tests/unit/test_time_bombs.py | docs/time_bombs.json 登记 3 项并分「auto / code / manual」：TB-01 GBR stop_rules_override（**到期日 2026-09-30，含当天有效**，次日起区域停止规则恢复约束——需用户决定是否续期，续期须新写 waiver_stop_rules_GBR_all，approved_by=user、≤ 30 天）、TB-02 CLI 开波区域闸 warn → enforce（2026-10-12）、TB-03 美国夏令时结束（2026-11-01，代码按 America/New_York 计算，无需操作）；test_time_bombs 守：人工项过期未办完即红、文档里出现未登记的未来日期即红、代码里的时间相关常量必须登记。「last_verified 批量戳」由 X-17 #10 的 git 判定兜底；区域平台状态快照见 X-12 |

## P0

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| P0-1 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md \| tests/unit/test_sf_sweeps.py \| tests/unit/test_ghost_operator_lists.py | DF-08 / EX-08 / HP-19 已改：ts_median（幽灵，会 CANCEL 整批）、scale_down（不在 103 算子目录）、ts_event_*（平台没有，KOR wave16 实测 8/8 ERROR；闸 8 已改为直接 FAIL）在全库文档里只以警示 / 反例口吻出现——test_sf_sweeps 扫全部 skills + docs/reference + AGENTS + README（另含 vec_mean、is_placeholder）。scale_down 是否真不存在待平台 get_operators 复核（X-16 needs-platform，DEC-62）；复核前文档一律按不可用处理，是安全侧 |
| P0-2 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md \| tests/unit/test_gate5_coverage_matrix.py \| tests/unit/test_sf_sweeps.py | V9「scale(A)+scale(B)*0.35」已删作配方（PP-13：SKILL 只留历史说明 + 合规改写——把 returns 反转当条件 / 分组，而不是加法项）；报告补充的缺口（gate.py 对权重在右的形态放行）由闸 5 覆盖矩阵关闭：形态（函数式 / 中缀）× 权重位置（左 / 右 / 无）× 运算，V9 顶层形态本身就是矩阵里的一行且期望被拦；test_sf_sweeps 另扫全库，不得再以正面口吻教加权 / 等权拼腿 |
| P0-3 | fixed | Claude/skills/worldquant-submit-alpha/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py \| tools/quota_status.py \| Claude/skills/INDEX.md | 配额只留一处（worldquant-submit-alpha/references/quota-and-tower.md，INDEX 只留指针）；activities/submissions 全库统一「不可用」（缺 today 字段），当日已提交数以 tools/quota_status.py 数 stage=OS 的 dateSubmitted 为准；pipeline.py 不再读 activities（注释与提示已更正，旧 48h 滚动口径废止）；日界按 America/New_York 计算（含夏令时） |
| P0-4 | fixed | src/wqb/workflow/nodes/submit_alpha.py \| Claude/skills/worldquant-submit-alpha/references/submit-chain.md \| Claude/skills/wq-brain-superalpha/SKILL.md \| tests/unit/test_wait_thresholds.py | submit_alpha 节点的 re-POST / ASYNC_STUCK 早已落地；本轮补齐其余几处：MCP _poll_submit_until_resolved 与节点共用同一份等待窗口（WAIT_THRESHOLDS，测试钉死两处一致）、super_build.py 的不可达 sleep 分支已删（测试钉死）、superalpha 写明「201 ≠ SA 合法，错误异步出现在模拟结果」并给失败分支；「补发」只指 REGULAR 的 re-POST（确认 dateSubmitted 为空后补一次，见 submit-chain 步 7），SUPER 没有补发语义——CLI 只发一次 POST，只走 super_build.py submit |
| P0-5 | fixed | Claude/skills/brain-make-some-gem/SKILL.md \| Claude/skills/brain-make-some-gem/examples.md \| tests/unit/test_se_docs.py | GEM SKILL 失败表补 402（LLM 余额不足，不可重试）与「no meta.json within 90s 先查 LLM 通道、402 会被这句误导性报错吞掉、干跑也验证不了」，绕行 = 手写 manual ideas 走 ideas_file（完全跳过 LLM）；runner 对 401 / 402 / 403 不重试并带绕行指引抛出 |
| P0-6 | fixed | Claude/skills/brain-alpha-repair/SKILL.md \| Claude/skills/brain-alpha-repair/references/repair-recipes.md \| tests/unit/test_brain_alpha_repair_docs.py \| AGENTS.md | 配方逐项核销（DEC-27）：4 项在别处有（字段体检文档 / 代码闸 / RA step5 / news_sentiment_playbook）并登记去向；「5 轴旋转」「降相关 6 武器」git 内 optimization-v1 从未有过、原文遗失不可恢复——**撤回声明**，不假装恢复；INDEX 卖点更正；测试：声明已上移的术语必须能在承接侧 grep 到，AGENTS.md 里「repair 配方已上移」的说法同步更正 |
| P0-7 | fixed | Claude/skills/brain-alpha-research/SKILL.md \| Claude/skills/brain-alpha-research-news-sentiment/SKILL.md \| tools/skill_lint.py \| tests/unit/test_skill_lint.py | 不存在的 CLI（wqb research / wqb settings / wqb news-refresh-portfolio）已从可执行说明里删除，只以「不存在」的口吻出现；skill_lint 的 cmd-* 检查逐条核对 fenced 命令的脚本 / 子命令 / flag，path-token 检查核对反引号路径 |
| P0-8 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | hypothesis-first 标「条件激活（dormant）」：仓库不带假设目录、目录缺失由 agent 按 §3 起草（干跑校验，闸即批准人），起草不出回步 2 换集；RA 步 2 #6 的「强制切换」改为「切到 hypothesis-first（先看其状态说明）」，「等假设生成器」与 RA「强制切换」的互锁取消；取消无人读的 field_semantics YAML；类别词表单一来源 = HYPOTHESIS_CLASSES（DEC-50） |
| P0-9 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md \| Claude/skills/INDEX.md | sim-alphas 把 alpha_list.json 标「已废弃的文件模式，仅跨区临时批 / 排障」、status CSV 标「运行态缓存」（不是真相源）；INDEX S3 行改为「backtest_results（DB）；alpha_list.json / status CSV 只是兼容 CLI 的运行态缓存」；INDEX「允许写的文件只有五类」把它们归 B 类 |

## AR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| AR-01 | fixed | Claude/skills/brain-alpha-research/SKILL.md | description 只写研究方法 / 搜索空间扩展 + 指向路由表，删与其重复的「触发场景」段 |
| AR-02 | fixed | Claude/skills/brain-alpha-research/SKILL.md | 边界改「常量只引用 config；研究结论可写但须标日期与失效条件」；固化表与区域优先级观测删除（只留指针），步 12 标题去「撤回」 |
| AR-03 | fixed | Claude/skills/brain-alpha-research/SKILL.md | §1 路由表补全 8 类任务（含 dataset-exploration / datafield-exploration / feature-engineering / S0），每行一句判据 |
| AR-04 | fixed | Claude/skills/brain-alpha-research/SKILL.md | 分「研究者步骤」（§2）与「维护者步骤」（§4）；研究记录 schema = Evidence 六字段 + applies_to / expires_when，落点写清；新增 vs 修正的判据：仅新增且经平台实测才可写 config |
| AR-05 | fixed | Claude/skills/brain-alpha-research/SKILL.md | 去掉「读源码 evidence.py」的 skill 相对链接，改为运行入口（打印 EVIDENCE_REGISTRY 的命令，测试实跑） |
| AR-06 | fixed | Claude/skills/brain-alpha-research/SKILL.md \| Claude/skills/brain-alpha-research/references/jump-decay-methodology.md | 「已删除模块」史注移出正文（进 CHANGELOG）；jump-decay 里的 paradigms.py / grammar.py 改成历史说明；--emit-ideas 写明产物是确定性模板，只作人读参考或经 LLM 改写后注入（对账 RA 步 4） |
| AR-07 | fixed | Claude/skills/brain-alpha-research/SKILL.md \| src/wqb/research/evidence.py | 删「check_batch 是过闸条件」——AST 测试证明它零调用方；真门禁 = gate.py 闸 6；SHAPE_CLASSES 与代码对齐（4 类，不含 S0）；evidence.py 里同样陈旧的规则文字一并改指闸 6 |
| AR-08 | fixed | Claude/skills/brain-alpha-research/SKILL.md | 固化表两句（COUNTRY 中性化仅 4 区 / Delay 0 仅 5 区）已不成立且互相矛盾，删；只引用 config.REGIONS，并写「支持 vs 数据广」 |
| AR-09 | fixed | Claude/skills/brain-alpha-research/SKILL.md | API 实测约束只留指针（唯一出处 = ppa-mining §11），删 localhost:8876 等环境细节 |
| AR-10 | fixed | Claude/skills/brain-alpha-research/SKILL.md \| tools/fetch_all_universes.py | 区域快照与「首选 ml_factor_proj」删除（已移到 ppa-mining 的历史页）；区域优先级只写 config.REGION_PRIORITY，选区用 region_rotation / s0-select；顺带修 fetch_all_universes.py 缺省 .env 指向作者桌面目录（改认 CREDENTIALS_* 与仓库内 .env） |
| AR-11 | fixed | Claude/skills/brain-alpha-research/SKILL.md | 离线包星级说明只在 ppa-mining §5.1 一处，本文留指针 |
| AR-12 | fixed | Claude/skills/brain-alpha-research/SKILL.md | 验证清单改真实可跑的命令 + 期望输出（第二条打印 TOP3000 与 11 项中性化顺序），并注明 wqb research / wqb settings 不存在；测试实跑 |
| AR-13 | fixed | Claude/skills/brain-alpha-research/SKILL.md \| Claude/skills/brain-alpha-research-field-quality/references/webdatascope-data-quality.md \| Claude/skills/brain-alpha-research/references/asi-methodology.md \| Claude/skills/brain-alpha-research/references/backtest-experience-archive.md \| Claude/skills/brain-alpha-research/references/jump-decay-methodology.md | SKILL 里每个 reference 一行「何时读」（测试：无孤儿）；webdatascope-data-quality.md（26 条规则）移入 field-quality 并修入链、消费位置表与 check_batch 说法；wikilink 全清、wqb-share-03 旧路径标注；jump-decay 标 [未验证]；asi 的等权拼腿结果标「已被政策禁止」；alpha-inspiration 去掉「已过 check_batch」 |

## BM

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| BM-01 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md \| Claude/skills/INDEX.md \| Claude/skills/wq-brain-superalpha/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/scenarios.md | 重新定位为 S6「监控与复盘」（REGULAR/PPA/SUPER 通用），去掉「PPA」定位；OS 表现监控与重着色明确声明无承接者（RA step9 §9.8 已登记），INDEX / superalpha / submit-alpha 的措辞同步改；不拆 skill，改为「监控 + 触发核验」，写入 SOP 归 RA 步 9 |
| BM-02 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 持久化铁律缩为一句；checkpoint 明确为「运行态证据（可读、非真相源）」，位置是 ledger ckpt_w<wave>（不再教读 results/*.json）；提交状态盘点改读 alphas / robustness / submit_verdict |
| BM-03 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 边界改「触发并核验」，写入 SOP 只在 RA step9；补「写失败怎么办」（按 suggestion 显式传枚举重试一次，仍失败走同函数的 CLI 逃生阀并报告，不得静默跳过） |
| BM-04 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 定一个默认：日常读 DB / checkpoint / batch_status，故障排查才枚举进程（Linux 与 Windows 各一条命令）；删除指向不存在 attic 归档的说法 |
| BM-05 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 删除「四关」体系（全库第 4 套闸门分类）与历史快照；改为映射到既有口径：Failed RA / submit_verdict 标签 / D0-P；阈值不抄，引 config |
| BM-06 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 持久化铁律缩为一句；checkpoint 明确为「运行态证据（可读、非真相源）」，位置是 ledger ckpt_w<wave>（不再教读 results/*.json）；提交状态盘点改读 alphas / robustness / submit_verdict |
| BM-07 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md \| Claude/skills/INDEX.md | 并发模型整节删除，改指 config.CONCURRENCY 与 wqb-concurrency §8；INDEX 里把出处写成 monitor §6 的那行改指向唯一来源；不再下带时点的「瓶颈」判断 |
| BM-08 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | universe 合法性改取 config.REGIONS[region]['universes']（旧文把 EUR 默认 TOP2500 判非法）；止损线指向 RA loop-and-stop 与 optimization-v1；「PASS_CHEAP 不得称可提交」合并为一处 |
| BM-09 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 红线泛化为「status=RUNNING 战役的 checkpoint 与运行脚本不得修改/移动/删除」；给出新监控脚本规范（tools/、docstring 三段、import _pyenv、只读、单测）；实例（v52b 等）全部删除，历史快照标注随之失效 |
| BM-10 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 三级分类映射到 submit_verdict 标签 + 提交队列 SQL 表（tools/submit_queue.py list）+ alphas.status；取证改读 DB；句式「N 个候选：a 已提交，b 待提交，c 仍需验证」保留；ledger 键 submit_ready 与同名 SQL 表不是同一物 |
| BM-11 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md \| Claude/skills/wq-backtest-monitor/references/scenarios.md | ETA 改「每个在飞 wave 一行」；如实写明 checkpoint 只有 submitted_at 与终态、无完成时间戳，故用吞吐法粗估；置信度标注为经验值；无完成批 → 未知；与 sim_stall_min 联动（已挂起不再报数）；历史任务名删除 |
| BM-12 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 报告章节改编号 R1–R4（不再与 skill 章节号混用）；删「唯一标准依据」；allowed-tools 只补 5 个只读 wqb-db 工具（能力基线已登记，待用户复核） |
| BM-13 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md \| src/wqb/config.py | 判停阈值只引 config.WAIT_THRESHOLDS（sim_stall_min / sim_timeout_min，与 poller.DEFAULT_POLL 由 test_wait_thresholds 钉住），即「等待/卡住阈值表」 |
| BM-14 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 命令模板按真实 CLI 重写（wave upsert 用 --finding，registry add-* 带必填参数，先 --dry-run），删 ledger set-verdict（写已废止的 wave<N>_verdict 键）；测试用真实 argparse 校验每个 flag |
| BM-15 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 方法论规则计数由代码自动完成（gate.py 消费契约、pipeline.py 校验 universe 杠杆与收批后 validate_rules，规则存 ledger methodology_rules），删除手工回写要求以免重复计数 |
| BM-16 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | 三级分类映射到 submit_verdict 标签 + 提交队列 SQL 表（tools/submit_queue.py list）+ alphas.status；取证改读 DB；句式「N 个候选：a 已提交，b 待提交，c 仍需验证」保留；ledger 键 submit_ready 与同名 SQL 表不是同一物 |
| BM-17 | fixed | Claude/skills/wq-backtest-monitor/SKILL.md | @file 临时文件写会话 scratchpad、用完删除；末行「修改报告结构前先与用户确认」移入报告骨架一节 |
| BM-18 | fixed | Claude/skills/wq-backtest-monitor/references/scenarios.md | 三张情景卡：日常一波收尾（真实命令序列 + get_wave_result 自检）、挂起处置（STALLED 判定 / 平台侧核对 / 留痕）、≤20 行的合规汇报样例 |

## CM

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| CM-01 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md \| tests/fixtures/skill_capabilities_baseline.json | description 改为「区域已定、需要 dataset / 死路 / 胜绩配置包时」，不再与 ra-pipeline 抢「开战役」触发词；allowed-tools 补 4 个只读 wqb-db 工具（能力基线 _doc 已登记理由，待用户复核）；frontmatter 字段顺序沿用全库多数写法，未另做统一 |
| CM-02 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 6 个连续空行删除；「运行环境」单句挪出 H1 之前（现 H1 后紧跟「职责边界」，由测试守） |
| CM-03 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/references/ledger-schema.md | 唯一归属：registry 的 schema / ID 命名 / 校验归 matrix（回写规范一节），何时写与写什么归 RA 步 9；职责边界删「回写」改「拥有写入规范」，闭环段落删除 |
| CM-04 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 删硬编码「31 个其他 skill」；「只查表不执行」只在职责边界写一次 |
| CM-05 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md \| src/wqb/registry_contract.py \| wqb_db_mcp.py \| Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/registry.py \| Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md \| docs/ra-mining-prompt-region-agnostic.md | DEC-34：措辞统一为「MCP 可用时 MCP，无 MCP / 批量用 CLI」；并把它落成代码——校验只在 registry_contract 一份，CLI 与 MCP upsert_registry_empirical / seal_dead_end 共用；seal_dead_end 新建条目必须带 rule |
| CM-06 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 配置包给固定字段表：prod_risk（与含 PROD_CORRELATION 类墙的 dead_end 重叠，附条目 id）/ prod_saturation（region_status.py --json 的 pass_ge_158 ≥ 10，口径只此一处）；样例补齐两字段；删 min_sharpe=1.58 字面值；不再引用不存在的「输出契约」节；撞墙后怎么办只指向 D0-P |
| CM-07 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 配置包带 mode 字段；体检方法分模式：RA 走决策表 D4 / 步 2，PPA 走 ppa-mining §1.0，不再把 PPA 阈值当全部战役的 S0 方法论 |
| CM-08 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 重写为唯一一张「存储地图」（概念 → 表 / layer → 读 → 写）；cross_region_lessons 表标已废弃（迁入 registry_empirical layer='cross_region'）；「层」一词只指 layer 列；registry 与 region_kb 并列合并（无谁派生谁） |
| CM-09 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 历史（单轨、JSON 归档、迁移工具）从正文移除（CHANGELOG 记一笔）；读法只保留 MCP；不再出现 campaign_registry.json 文件名 |
| CM-10 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | region 是入口参数、matrix 不选区：缺 region 回问用户，或转 next-move / region_status --rotate；删「最高优先级」（campaign 层只有 status 三值，没有排序键） |
| CM-11 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 查表调用后附返回摘要与空结果含义（region not found = 该区从未入库，不是「没有配置」） |
| CM-12 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 完整配置包样例 + 字段来源表；「候选 = 待 S0 筛选的超集，不是白名单」（已点亮塔、win 族、体检硬门由 S0 执行）；「数据集 dominant」一说删除 |
| CM-13 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 整段九步派发链删除，改一句「交还 ra-pipeline 步 2」；测试断言 matrix 不再出现 workflow_batch_track / submit_verdict 等编排词 |
| CM-14 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 命令改 PowerShell + $WQ_TOOLKIT_DIR，日期改占位；定义 ID 命名规则（<REGION>-<数据集或族>-<症状>-DEAD）与各 layer 必填字段表（与 registry_contract 一致，测试守）；--key 定义为「设置与骨架」，不记混合比例 |
| CM-15 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 给 3 正例（带 rule 的 dead_end、可复用 win 配方、数据集 exhausted）与 3 反例（单波 FAIL、单条 alpha 未过闸、参数扫描结果） |
| CM-16 | fixed | Claude/skills/INDEX.md \| Claude/skills/wq-brain-campaign-matrix/SKILL.md | 开新区检查表在 INDEX 唯一维护（落点 + 验证命令）；不存在的 fresh_datasets_7region.json 删除；regions / datasets 表的写入路径写清（CampaignStore 自动建行、discover / ingest_dataset_assets）；tracking/region_config.json 无代码读取，明确排除 |
| CM-17 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 改「与 registry 冲突时以 registry 为准，并在发现处修正来源文档」 |
| CM-18 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 死路 rule 与用户指令：先提示一次依据，用户坚持则执行并在 key_findings 记「用户覆盖」——与 RA「用户显式指令 > 决策表」一致；情景 MX-2 |
| CM-19 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md \| Claude/skills/INDEX.md | 区域覆盖事实只在 INDEX §区域清单维护，硬规则 3 改「以 config.REGIONS 与 INDEX 为准」，不再断言 AMR / JPN 未启用（JPN profile 已于 09-15 补齐） |
| CM-20 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 「禁止散装 SQL」收敛为硬规则 4 一处 |
| CM-21 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md \| docs/ledger_keys.json \| wqb_db_mcp.py | DEC-33：submit_ready 唯一存储 = SQL 表；registry schema 不再有 submit_ready[] 镜像；matrix 存储地图与台账边界只提 SQL 表 |
| CM-22 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 写明同步关系：registry 与 region_kb 并列，由 assemble-priors 合并（registry 的 win / dead_end 层 + region_kb 的论坛模板 / 配方 / 死路模式 / 过闸率先验）；S6 只写 registry；回写后必须再跑 assemble-priors |
| CM-23 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | S6 回写细节整段删除，只保留「回写后必须再跑 assemble-priors」并指向 RA 步 9 的完成定义 |
| CM-24 | fixed | Claude/skills/wq-brain-campaign-matrix/SKILL.md | 增「常见失败与处置」表（region not found / 缺 region / frozen / registry 与 profile 冲突 / 回写被拒缺 rule / entry_id 不一致 / prod_saturation=unknown）与 3 张情景卡 MX-1..3 |

## DE

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| DE-01 | fixed | Claude/skills/brain-dataset-exploration-general/SKILL.md | description 限定「已在白名单 / 点名的某一个数据集」的数据集级审计，撤出「跨平台调研」；新闻字段 5 家族分类交 news-sentiment；运行环境句删（唯一 Python 命令自带 _pyenv），头部空行整理 |
| DE-02 | fixed | Claude/skills/brain-dataset-exploration-general/SKILL.md | Region → Universe 表删，改 config.REGIONS[<R>][default_universe] 与 get_platform_setting_options；JPN「非有效 EQUITY 区域」删（config 有 JPN / TOP1600，RA 有 profile）；universe 传错的症状（get_datasets 静默返回 0 条 / 手写 /data-fields 报 500）保留 |
| DE-03 | fixed | Claude/skills/brain-dataset-exploration-general/SKILL.md | 上游 = 白名单内某集或用户点名；无白名单且未点名 → 先走 RA 步 2 选集；Phase 1「按战略重要性选择」删 |
| DE-04 | fixed | Claude/skills/brain-dataset-exploration-general/SKILL.md | §3 字段分类落点 = ledger s1_semantic_<ds>（field_semantic_classify.py，读 fields 表，唯一有下游消费者）；四维分类降为阅读辅助；加「字段分类法一览」（S1 语义 / 新闻 5 家族 / 三套互映射本体）；说明经济大类偏财报口径，非财报集多落 other |
| DE-05 | fixed | Claude/skills/brain-dataset-exploration-general/SKILL.md | 评分公式与阈值删，只留指针（score_datasets.py + probe-scoring-v2.md）；旧 0.30/(1+log10(1+alphaCount)) 与 tier2 门槛标已被 v3.1 取代、不要再用（测试） |
| DE-06 | fixed | Claude/skills/brain-dataset-exploration-general/SKILL.md | 调研默认不查论坛：触发条件（判死复开 / 机制枯竭）走 forum_recon.py；不为审计加载 brain-forum-browse |
| DE-07 | fixed | Claude/skills/brain-dataset-exploration-general/SKILL.md \| Claude/skills/brain-dataset-exploration-general/reference.md | §1 范围控制：分类永远全量（本地脚本零配额），深挖代表字段 ≤ 12（每类 1–2 + 3 冷门）；不产「增强描述」；审计结论模板与落点写清（对话 / reports/dataset_audit_*.md，非事实源） |
| DE-08 | fixed | Claude/skills/brain-dataset-exploration-general/reference.md | 436 行英文岗位手册 → ≤ 60 行中文背景（结论模板 / MCP 速查 / 文档页）；其中的 6-Tips 方法只在 datafield-exploration 保留一份（此前两处各抄一遍，都带不可用算子） |

## DF

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| DF-01 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md | 「6 种方法」对应正文「法 1–6」连号；类型陷阱、批量收割改为无编号章节，不再跳号（测试） |
| DF-02 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md \| Claude/skills/brain-datafield-exploration-general/reference.md | §0 先离线后在线 + 成本：体检包先答法 1 / 3 / 6；在线最小集 6 条一批 / 扩展集 ≤ 8，全跑六法 ≈ 15 条；create_multi_simulation 单次 2–10 条、连坐、有静态门禁；手工探索不入库不进战役统计；testPeriod 统一 P0Y0M0D |
| DF-03 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md \| tests/fixtures/skill_lint_baseline.json | 法 5 改 ts_mean(datafield, 252)（1 年；要 4 年用 1008，标准窗口），ts_median 标幽灵算子；skill_lint 基线里对应的 GHOST 条目已清 |
| DF-04 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md \| Claude/skills/brain-datafield-exploration-general/reference.md | 「类型先行」表：MATRIX 不包 vec_*；VECTOR 必须先 vec_*（闸 3；裸用 → 平台 400 event inputs；fix_vector_fields / preflight auto_fix_vector）；旧「直接用、winsorize 安全」标已更正 |
| DF-05 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md \| Claude/skills/INDEX.md | EVENT（type==EVENT）：平台没有 ts_event_*（KOR wave16 实测 8/8 ERROR），闸 8 直接 FAIL、先单条探针；不再把 ts_event_* 输出称作 VECTOR；INDEX S1 行的 ts_event_* 预处理项同步改 |
| DF-06 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md | 范式保留为「症状 → 原因 → 规避」表：裸 dataset= 被静默忽略 → dataset.id=；补 MCP get_datafields 已封装（源码核对），只在手写 REST 时会踩 |
| DF-07 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md | 每法末加「→ 交 FE」：覆盖 → backfill、非零 → trade_when、频率 → 窗口下限（体检 min_window / 硬门代码口径）、范围 → 去量纲、中心 → 单边先取变化率、形态 → winsorize / rank / 门控；链接 brain-data-feature-engineering |
| DF-08 | fixed | Claude/skills/brain-datafield-exploration-general/SKILL.md \| Claude/skills/brain-datafield-exploration-general/reference.md | 算子口径以平台 103 算子目录裁决：ts_median（幽灵）→ ts_mean；scale_down（不在目录）→ zscore 刻度；ts_event_*（平台没有）删；机械检查：SKILL / reference 里出现的算子必须在目录内或标为反例（测试）；顺带发现 ? : 三元过不了 MCP 静态语法闸，六法表达式改比较式并逐条过校验器 |

## EV

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| EV-01 | fixed | Claude/skills/alpha-expression-verifier/SKILL.md | 示例表换成 6 个真实输入与真实 errors（合法 / 括号不匹配 / 元数不足 / 元数过多 / 未知函数 / rank(x,5) 合法且第二参是 rate），测试逐行对真实校验器 |
| EV-02 | fixed | Claude/skills/alpha-expression-verifier/SKILL.md | 只留一种写法（仓库根相对路径）+ $WQ_VALIDATOR_DIR 的含义与 gate.py 同变量；史注删除 |
| EV-03 | fixed | Claude/skills/alpha-expression-verifier/SKILL.md | densify 分组键说明保留（本层做不到什么） |
| EV-04 | fixed | Claude/skills/alpha-expression-verifier/SKILL.md \| Claude/skills/alpha-expression-verifier/scripts/validator.py | 「5 闸」「1363 行」删除（不再写会漂移的数字）；变更纪律留一句并指向影响面。同时发现并修复更实质的问题：validator.py 有 4 份、3 个版本，FI / GEM 内嵌 / inspect-raw 三份缺 hump 命名参数、bucket 必带 range、densify 类型三处已修复的事故修复——改为逐字节镜像权威版，并加测试守护 |
| EV-05 | fixed | Claude/skills/alpha-expression-verifier/SKILL.md | 新增「常见错误 → 含义 → 处理」表与退出码语义（非法表达式也退 0，调用方必须解析 valid；只有缺参 / 导入失败 / 异常才退 1，均有测试） |

## EX

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| EX-01 | fixed | Claude/skills/brain-explain-alphas/SKILL.md \| tools/concept_overlap.py | 补第 7 步概念重叠检查及对应程序：目标 vs 本区 ACTIVE book 的（字段集合、骨架指纹），与闸 PF / prod-first 同源函数；HIGH/MEDIUM/LOW/CLEAR 是启发式提示（Jaccard 0.5 阈值有取值理由、未做样本外标定），不构成平台判定 |
| EX-02 | fixed | Claude/skills/brain-explain-alphas/SKILL.md \| Claude/skills/brain-explain-alphas/reference.md | get_datafields 真实签名（region / dataset_id / universe 必传，无 instrument_type），区分必填 / 推荐 |
| EX-03 | fixed | Claude/skills/brain-explain-alphas/SKILL.md \| Claude/skills/brain-explain-alphas/reference.md | 解释既有 alpha 时 filter_sharpe=False、search 用完整 field id、返回为空的排查顺序 |
| EX-04 | fixed | Claude/skills/brain-explain-alphas/reference.md | 示例标注 VECTOR→必须 vec_*、MATRIX→禁 vec_*；country 作 group 部分区域无效；字段含义分「事实 / 推测」两栏 |
| EX-05 | fixed | Claude/skills/brain-explain-alphas/SKILL.md \| Claude/skills/brain-explain-alphas/reference.md | 删「附录速查表」的不存在引用；改「取回全量后只读用到的算子」 |
| EX-06 | fixed | Claude/skills/brain-explain-alphas/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/arXiv_API_Tool_Manual.md | 脚本单份、路径写全；外发边界一句话（只发通用关键词） |
| EX-07 | fixed | Claude/skills/brain-explain-alphas/reference.md \| Claude/skills/brain-explain-alphas/SKILL.md | 给出对首例的完整四段成品示例；证据要求（逐年 / PnL / long-short 与行业未核验就写未核验）；落点（回复 / key_findings，不新造键）；「进一步启发」改结构化 3 栏 |
| EX-08 | fixed | Claude/skills/brain-explain-alphas/SKILL.md \| Claude/skills/brain-explain-alphas/reference.md | vec_mean → vec_avg，并以 platform_constraints.vector_only_ops 为准列出（vec_norm 标需复核） |
| EX-09 | fixed | Claude/skills/brain-explain-alphas/SKILL.md \| Claude/skills/brain-alpha-robustness/SKILL.md | 链图写成 selfcorr-quick →(可选) explain → robustness，写明跳过 explain 不影响 robustness 入场；robustness 的上游同步改；删改动史 |
| EX-10 | fixed | Claude/skills/brain-explain-alphas/reference.md \| tests/unit/test_concept_overlap.py | 两张情景卡：Mode B 换概念前查重叠（3 个 ACTIVE alpha 的 book，输出 HIGH + 换概念）/ 战略级候选提交前确认收益来源（三条警示信号，未核验不得写成通过） |

## FB

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FB-01 | fixed | Claude/skills/brain-forum-browse/SKILL.md | description 改纯中文、去 markdown 粗体，只写触发场景（逛论坛 / 看看 / 查论坛里有没有 X），并点明「流水线的问题驱动检索走 tools/forum_recon.py」；recon 在正文 §5 单列一节 |
| FB-02 | fixed | Claude/skills/brain-forum-browse/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/forum-recon-triggers.md \| Claude/skills/brain-forum-browse/references/write-path/README.md | DEC-45：不新建 skill 目录，按职责分节——§3 explore（只读）、§5 recon（薄，触发表只在 RA 一张）、§6 休眠写路径；写路径整体移入 references/write-path/，两种相反治理不再混在同一份规则里；RA 不加载本 skill、直接调 forum_recon |
| FB-03 | fixed | Claude/skills/brain-forum-browse/SKILL.md | 边界与正文统一：提交前审查 = tools/submit_verdict.py，brain-alpha-judge 只是参考层 |
| FB-04 | fixed | Claude/skills/brain-forum-browse/SKILL.md \| Claude/skills/brain-forum-browse/references/write-path/modes-and-contract.md | 「当前能力 = 只读」提到最前；「每轮必贡献」撤销（无写工具无法满足），唯一表述 = write-path/modes-and-contract §2 决策树（有写工具才成立，否 → 休眠）；写路径规则全部标休眠 |
| FB-05 | fixed | Claude/skills/brain-forum-browse/references/write-path/README.md \| Claude/skills/brain-forum-browse/references/write-path/modes-and-contract.md | E1/E2/E3 在 README 术语与 evidence 文档首现处定义；hybrid 只在两处标弃用别名；modes 标题改「四种模式」并含 recon；阶段按执行顺序成表 |
| FB-06 | fixed | Claude/skills/brain-forum-browse/SKILL.md \| Claude/skills/brain-forum-browse/references/write-path/README.md | 全部旧文件名标签清除（合并前的 auto-send-e1 / personal-perspective / profile-bootstrap / external-memory-sources / merge-with-alpha-judge / file-workspace / index-post-protocol / mcp-tools-and-search），测试扫描整个 skill 目录并逐条核对 SKILL 链接 |
| FB-07 | fixed | Claude/skills/brain-forum-browse/references/write-path/modes-and-contract.md | 决策树补第三支（无写工具 → 休眠、只读 explore）；linker 兜底统一为唯一条件：本轮有 E2 且有索引理由，不允许硬发链接 |
| FB-08 | fixed | Claude/skills/brain-forum-browse/SKILL.md | MCP 排障抽成 §4 症状 / 原因 / 处置表（服务没起≠没实现、检查命令、stdio 与 HTTP 两种、重启宿主会话、ENOENT ${WQB_MCP_PY} 一行——本环境实测遇到）；服务名与端点只写一处；旧「。。」笔误与 user-brain-api 删除 |
| FB-09 | fixed | Claude/skills/brain-forum-browse/SKILL.md | 工具表只列现役 6 个读工具（测试对照代码签名）；不存在的写工具单列一行，不再混入「必须用」表 |
| FB-10 | fixed | world-quant-brain-mcp/tools_forum.py \| world-quant-brain-mcp/tools_account.py \| Claude/skills/brain-forum-browse/SKILL.md \| Claude/skills/brain-forum-browse/references/write-path/README.md | DEC-44：四个 MCP 工具删除 email/password 参数（凭据只由服务端配置提供）+ 全库守护测试；文档：认证失败 → 停止并请用户在本机修配置，不在对话传口令；公开内容脱敏清单（含 P4 对话史须同意 + 转述）；harvest 隐私提示 |
| FB-11 | fixed | Claude/skills/brain-forum-browse/references/tools-and-troubleshooting.md | 分情景：正常调用直接用名、不探测；工具搜不到才走排障（写在同一处） |
| FB-12 | fixed | Claude/skills/brain-forum-browse/SKILL.md \| Claude/skills/brain-forum-browse/references/tools-and-troubleshooting.md | 两个重复的工具表并成一张现役表（名 / 参数 / 缺省 / 用途）；「唯一搜索工具」「fast / slow / list」「替代…」「已安装但超出范围：delete_forum_*」全部删除（这些工具未注册，测试断言） |
| FB-13 | fixed | Claude/skills/brain-forum-browse/SKILL.md \| Claude/skills/brain-forum-browse/references/write-path/workspace-and-memory.md \| Claude/skills/brain-forum-browse/scripts/init_workspace.py | 命令写全路径 & $WQ_PY Claude/skills/brain-forum-browse/scripts/…；工作区落点写明（skill 目录 outputs/，已 .gitignore，同步到宿主后落在那份目录）；harvest 补目的（写路径 E1 燃料）与隐私边界；init_workspace 默认只读、--write-path 显式开启（测试） |
| FB-14 | fixed | Claude/skills/brain-forum-browse/SKILL.md \| Claude/skills/brain-forum-browse/references/write-path/mcp-by-phase.md | 硬性规则 20 条 → 「规则速览」5 行表（规则 / 适用 / 由谁强制）；重复规则并入写路径；「MCP 优先」与「先文件后 MCP」写成一句话消歧（本地只给记忆、事实只来自 MCP）；对抗审查子代理须宿主允许派生，不允许时自审并在合同注明；curator 依赖的 upvote 工具标未注册 |
| FB-15 | fixed | Claude/skills/brain-forum-browse/references/write-path/README.md | 按执行顺序的阶段表 + 历史编号对照（14 步）；L1/L2/L3、Scout、E1–E3、P0–P5 在 README 术语节定义并与全库同形标签消歧 |
| FB-16 | fixed | Claude/skills/brain-forum-browse/references/write-path/README.md | 记忆层 P0–P5 保留为本 skill 内部标签（改名会波及模板与 schema），在 README 逐项命名并声明「与全库其它 P 编号无关」 |
| FB-17 | fixed | Claude/skills/brain-forum-browse/references/write-path/quotas-and-cooldown.md \| Claude/skills/brain-forum-browse/SKILL.md \| Claude/skills/brain-forum-browse/configs/config.example.json | 配额表去重（历史上同一工具多个上限是改名合并残留），读取预算与 config.example.json 一致（测试）；「每轮 ≥1」与「最多 3」不冲突（写操作数 ∈ [1,3]）；recon 的 --max-search-rounds 缺省 8 写明（测试对照代码） |
| FB-18 | fixed | Claude/skills/brain-forum-browse/SKILL.md | 参考资料索引只列现存文件，旧名进 CHANGELOG |

## FE

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FE-01 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 重写：只保留「两条产物路径」——A 节点 = 确定性模板（source=feature_engineering_node，GEM 不注入）/ B agent 人工 = source=manual（注入）；L162「法定输入 / 步 4 必须传 --ideas-file」删；与 RA 步 3「按需、模板产物不注入」一致；description 改为「人工字段理解 → GEM 可摄入 ideas + S1 台账」 |
| FE-02 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 台账 JSON 示例 source 改 manual，并注明「写成 standalone 会被 GEM 静默忽略」；三种模板渲染取值与引擎 TEMPLATE_IDEAS_SOURCES 同口径；测试直接解析该 JSON 示例（占位符替换后）断言 source == manual 且带 ideas_md_path / field_whitelist / concept_count |
| FE-03 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 「S1⇄S2 统一逻辑链」改成 source → 是否注入 对照表（gem.py::is_template_ideas_source 同口径，模板源不注入，manual / s2_nested 且文件存在且非 skeleton 才自动注入，显式 ideas_file 覆盖）；「五闸读此记录」删，改列真实读取方（GEM 节点与 runner / s2_field_validator / campaign 预检）并明写「toolkit 闸 1–5 不读它」——测试断言 gate.py 里没有 s1_ 引用，将来闸读了它会让测试失败提醒改文 |
| FE-04 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 职责边界写明「不选数据集：没有 dataset_id → 回 RA 步 2，不自行挑」；第 1 步改为「锁定数据集」（对 s0_whitelist 校验，不在白名单则报冲突并停）；「基于元数据选择最相关数据集」整段删；输入表 dataset_id 必填 |
| FE-05 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | universe 缺省 = config.REGIONS[<region>][default_universe]，并列出 KOR / AMR TOP600、EUR TOP2500、JPN TOP1600；测试逐区对照 config |
| FE-06 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 第 0 步加裁决序「黑盒 > 半透明 > 透明」（命中任一黑盒判据就按黑盒），并给跨档例：model109 描述覆盖率 ≥ 80% 但 model* 前缀命中黑盒 → 按黑盒 |
| FE-07 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 第 3 步加概念预算（缺省、经验值、非硬闸）：全部 8–12 个（半透明 ≤ 6）/ 每概念 1–2 字段 / 每问 ≤ 2 概念 / 同一字段至多进 2 个概念，并写理由（KOR fundamental17 首波 9.9% 黑名单字段吃 49.4% 预算）；第 4 步给 GEM 摄入契约：Concept / Implementation Example / Expected Exposure（取值取自 pipeline_reports._EXPOSURE_KEYWORDS）；示例块经真实 GEM 解析器解析出 3 块、占位符 = pv1 真实字段后缀、渲染后过规范校验器、窗口全是标准窗口 |
| FE-08 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 产物目录改 data/gem_runs/output_report/manual_<REGION>_delay<D>_<ds>_ideas.md（GEM_REPORT_ROOT，data/ 已 gitignore；不再写与 CWD 有关的 ./output_report/），manual_ 前缀避开 GEM 重跑清理与节点的 fe_ 前缀（测试：run_pipeline 只清 gem_ 名）；主从关系写明：ledger 是事实源、ideas 文档是它指向的载荷；preprocessing 只作记录（测试：全仓只有节点自己 .get 它） |
| FE-09 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md \| Claude/skills/brain-data-feature-engineering/OUTPUT_TEMPLATE.md | 报告提纲（1–5 章 / 3.1–3.8）从 SKILL 删除，只在 OUTPUT_TEMPLATE.md 保留（头部标「唯一提纲」并说明「{字段后缀}」占位约定）；SKILL 里一行指针 |
| FE-10 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 删「本 skill 不应当…」与 5 条泛化原则，硬要求收进第 4 步（概念块契约）/ 第 5 步（落盘与台账）/ 验收 4 项；与节点确定性模板不再互相矛盾（两条路径分表说明） |
| FE-11 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md \| Claude/skills/brain-data-feature-engineering/examples.md | SKILL 内示例换成 pv1 的真实字段（returns / volume / adv20）+ 标准窗口 + 可渲染表达式（真实 GEM 解析器 + 规范校验器实测通过）；examples.md 头部显式标「虚构的教学案例」（BEME 与 book_value 等不是真实字段 id）并指向 SKILL 的真实示例 |
| FE-12 | fixed | Claude/skills/brain-data-feature-engineering/SKILL.md | 「所有字段都被分析」「新颖 / 避开传统思维陷阱」删；验收改 4 项可检产物：分档已写明（档位 + 命中判据）/ 概念块可被解析（Concept + Implementation Example + Expected Exposure、预算内、占位符对得上、标准窗口）/ 台账可读（get_ledger_key 返回 source == manual 且 ideas_md_path 文件存在）/ 无越界（白名单内、blocked 字段不入概念） |
| FE-13 | fixed | tools/sync_gem_embedded_skill.py \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skills/README.md \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skills/brain-data-feature-engineering/GENERATED.md \| tests/unit/test_gem_skill_paths.py | 更正一个更大的事实：这两份内嵌 SKILL.md **从不拼进 LLM prompt**（build_prompt 只把 dfe「是否非空」当真值判断附固定 8 问提示，FI 完全不用；AST 测试钉死），所以「拆 prompt 部分 / 人读部分」不成立。落地的是另外三件：内嵌 dfe 目录加 GENERATED.md 标记；sync_gem_embedded_skill 改成 pairs 制（FI SKILL.md + dfe reference / examples / OUTPUT_TEMPLATE 四个文件，--check / --apply）；test_gem_skill_paths 守护扩到 dfe 三个文件（此前 reference.md 已漂移到 399 行旧稿）。顺带：解析实跑测试此前只认 Windows 的 Scripts/python.exe，在 Linux 永远 skip，现两种 venv 布局都认 |

## FI

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FI-01 | fixed | Claude/skills/brain-feature-implementation/SKILL.md | description 改「排查或手动复现 GEM 渲染时查阅、不是生成表达式的入口」，从触发列表撤出「要求生成 alpha 表达式」 |
| FI-02 | fixed | Claude/skills/brain-feature-implementation/SKILL.md \| Claude/skills/brain-feature-implementation/scripts/fetch_dataset.py | 凭据：标准环境变量 CREDENTIALS_EMAIL/PASSWORD 优先，旧别名仍认，config.json 只在环境变量不全时才需要（此前无论如何都硬要它）；登录不再回显邮箱；文档声明 agent 不读 / 不回显 config.json 与 .env；GEM 内嵌副本同步改（逐字节相同，测试守） |
| FI-03 | fixed | Claude/skills/brain-feature-implementation/SKILL.md | 给确定路径（仓库根相对 & $WQ_PY …/scripts/…，脚本与 CWD 无关，去掉 cd）；写清顶层 vs GEM 内嵌的适用时机与解析顺序（WQB_FI_SKILL_DIR > 安装位 > 仓库 > 内嵌兜底）；两份目录现逐字节相同并有测试；--universe 缺省 TOP3000 只适用部分区域，改指 config.REGIONS[<R>].default_universe；implement_idea 全部真实参数列出（原文「只接受两个」已过期） |
| FI-04 | fixed | Claude/skills/brain-feature-implementation/SKILL.md \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/pipeline_prompts.py | TaskCreate 与 allowed-tools 里的 TaskCreate 删除；核实代码：build_prompt 已不使用 FI 文本（只用 FE 8 问当提示），原「拼进 LLM prompt」的担忧已过时——文档写明并由 AST 测试钉死，将来若又拼进去要同步改文档 |
| FI-05 | fixed | Claude/skills/brain-feature-implementation/SKILL.md | 职责边界写明 final_expressions.json 不是真相源、无下游读取（只有 GEM 节点入库）；想入库走 inspect-raw 或直接用 GEM，不要写 SQL；步骤 5 要求向用户注明「未入库」 |
| FI-06 | fixed | Claude/skills/brain-feature-implementation/SKILL.md | 行为规则（占位符只绑定一次、GROUP 不扩展数值变体）挪进「模板语法」节，删「描述」节 |

## FQ

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FQ-01 | fixed | Claude/skills/brain-alpha-research-field-quality/SKILL.md | §1 分阶段：选方向可用 alphaCount / userCount 作先验，进入造批服从 RA 步 3 §3.3（users 分级、冷门字段占批次预算 ≥ 50%，逐格对照 RA 文档）；饱和数据集不叠加本先验（那是 hypothesis-first 的适用域） |
| FQ-02 | fixed | Claude/skills/brain-alpha-research-field-quality/SKILL.md | 删 jq（Windows 未必有）与散写 SQL，取数改 get_datafields 在对话里按 alphaCount 降序取前 ~30 |
| FQ-03 | fixed | Claude/skills/brain-alpha-research-field-quality/SKILL.md | 「拥挤度阈值：五个数，五条轴」表：离线甜点 / 饱和（webdata_quality）、S0 拥挤罚（score_datasets）、RA 饱和路由（≥ 1 万或连续 2 波）、PPA 硬闸、校准甜区——轴不同不冲突，逐项由测试对照源码 |
| FQ-04 | fixed | Claude/skills/brain-alpha-research-field-quality/SKILL.md \| Claude/skills/brain-alpha-research-field-quality/references/webdatascope-data-quality.md | 26 条规则文档已在本 skill references/（测试守 26 条、无跨 skill 相对链接）；规则 13 补两层口径：理论下限 21d / 63d vs 体检硬门实际执行的代码口径 daily 22 / weekly 52 / monthly 120 / quarterly 252（流量类 daily 5） |
| FQ-05 | fixed | Claude/skills/brain-alpha-research-field-quality/SKILL.md | 范式保留（数据包覆盖 7 区 / 9 组合 / 160 条记录 + 判定顺序 + 免预筛留痕）；「这此区域」笔误随重写消失（测试） |
| FQ-06 | fixed | Claude/skills/brain-alpha-research-field-quality/SKILL.md | §2 判定顺序（在包内 → 预筛；不在 → 改走平台侧并 --source exempt 登记免预筛理由）；§3 首句限定「数据包覆盖的区域」，DEU / IND / GBR / MEA / TWN 不再被要求先跑必空的预筛 |
| FQ-07 | fixed | Claude/skills/brain-alpha-research-field-quality/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | §3「机器自检」写明工具级、未接入 workflow 节点（测试：campaign.py 零引用），待办状态出 SOP；BLOCK 时先预筛或登记豁免，不靠别的 waiver 绕过；RA 步 2 补一段自检指针 |
| FQ-08 | fixed | Claude/skills/brain-alpha-research-field-quality/SKILL.md | 验证清单改产物形式：前 ~30 字段表 / 预筛输出或豁免登记 / prescreen_gate exit 0 + get_ledger_key 可读 |

## FR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| FR-01 | fixed | Claude/skills/brain-forum-browse/references/write-path/modes-and-contract.md | 头注「合并自…」（自己出现两次）删除；标题改四种模式含 recon；原 §2「最低贡献条」并入决策树，删除对 SKILL 的第 N 次复述 |
| FR-02 | fixed | Claude/skills/brain-forum-browse/references/write-path/modes-and-contract.md | Auto-Send E1 的 A1–A8 可检条件清单与自检清单原样保留（全库最可检的范例） |
| FR-03 | fixed | Claude/skills/brain-forum-browse/references/write-path/README.md \| Claude/skills/brain-forum-browse/references/write-path/workspace-and-memory.md | 补 P4（宿主 AI 对话史）作 E1 公开来源的规则：只转述已核实事实、引用须用户同意并脱敏（脱敏清单第 3 条） |
| FR-04 | fixed | Claude/skills/brain-forum-browse/references/write-path/mcp-by-phase.md | 460 行（约一半是空行）压缩到 43 行：每阶段一行工具与参数；改名残留（重复的 get_glossary_terms、try slow、create_forum_* 当现役、user-brain-api）清除，审查子代理的宿主前提写明 |
| FR-05 | fixed | Claude/skills/brain-forum-browse/references/write-path/write-style-zh.md | 归入休眠包；转换脚本命令改 & $WQ_PY 全路径（lint 基线相应删 2 条）；示例表格里的 [文字](url) 是示例，SKILL.md 的链接检查不涉及 |
| FR-06 | fixed | Claude/skills/brain-forum-browse/references/write-path/README.md \| Claude/skills/brain-forum-browse/references/write-path/contribution-and-diversity.md \| Claude/skills/brain-forum-browse/references/write-path/recon-and-gap.md \| Claude/skills/brain-forum-browse/references/write-path/evidence-and-review.md | 其余 references 整体归为休眠（各带横幅）；9 处「合并自 / 参考资料已合并」头注删除；数值阈值（title_sim / self_overlap / gap_threshold）无实测来源也无代码使用——README 明确标为经验启发式、启用前重校准 |
| FR-07 | fixed | Claude/skills/brain-forum-browse/templates/forum_stroll_notes.md \| Claude/skills/brain-forum-browse/templates/session_plan.md \| Claude/skills/brain-forum-browse/scripts/init_workspace.py \| Claude/skills/brain-forum-browse/references/write-path/README.md | 写路径模板移入 templates/write-path/，另写只读版 stroll_notes / session_plan；脚本路径写全并支持 --write-path；写路径专用脚本（init_profile / validate_profile / harvest / md_to_forum_html）列入 write-path README |

## GM

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| GM-01 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 共享产物约定写明「agent 在每次开生成前先跑一次 assemble-priors（与 RA 步 4 同一条；stage 只是标签，路由按 subcommand）」；快照过期只 WARN、不据此认为已确认安全、刷新责任归步 9 |
| GM-02 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 下游改「调一个入口 tools/wave_gate.py（节点 wave_gate；内含闸 1–8、体检硬门、SEM、PF）」，明写 check_batch 已不是门禁，删「check_batch → check_expr_against_inspect → 闸 1–5」三段串联 |
| GM-03 | fixed | Claude/skills/brain-make-some-gem/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step4-generation.md | 原 400 字一段拆成「ideas 注入 / 社区模板 / 预闸 / 两种模式」四条；预闸规则表只在 RA step4-generation.md §4.4 维护，GEM 侧只列自动动作类别并指向它，RA 表补上此前缺的两行（region_invalid_fields / region_vector_ts_forbidden，对照 pipeline_pregate 的四个 reason 与「WQB_GEM_MAX_PER_SKELETON 缺省 12」）；kb_templates --emit-ideas 产物 source = kb_templates.py 且是 JSON，写明不能直接当 ideas_file（测试用真实解析器喂它得 0 块） |
| GM-04 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 铁律 2 保留「默认 DB 快照直读、fail-closed；priors_file 仅覆盖」并注明 RA 旧硬约束「必须带 priors_file」已过期（RA 侧同步）；ideas 注入补限定「source 非模板渲染（manual / s2_nested）且 ideas_md_path 存在且 pipeline_mode ≠ skeleton；显式 ideas_file 覆盖」——与 FE 注入表逐项同口径 |
| GM-05 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 以代码为准重写：引擎实际消费 wins（≤ 6）/ dead_ends（≤ 12）/ region_context（tier / settings_proven / key_notes ≤ 4）/ skeleton_field_matrix（有效 ≤ 6 / 死 ≤ 8 / 正交提示 ≤ 4）/ gate_priors 的 by_operator_count / by_field_family / avoid；by_decay / by_neutralization 不进 prompt；旧「只消费两键」标已更正。测试对 compact_priors_text 源码做切片断言 |
| GM-06 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 铁律 6 统一为 RA 路线 A / 决策表 D3 的态度：不靠加腿修闸；多组件概念每个组件须写明经济角色（条件 / 分组 / 残差 / 同源对偶价差，RA 步 7 §7.7.2 的允许形态），「补它修 sub_universe / 2Y / CW」不是理由，CW 修法看 D6（margin 是数据集属性，补腿修不了）；给反例 add(rank(A), rank(B)) 与 0.4*rank(A)+0.6*rank(B)（闸 5 拦） |
| GM-07 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 铁律 7 三处对齐：语义多样性为准（≥ 3 Expected Exposure / ≥ 3 字段族 / ≥ 2 分组轴 / ≥ 2 时间尺度），同时如实写明闸 6 的批级契约仍在（required_operators + skeleton_quota 由 build-wave 确定性注入、闸 6 强制），所以 GEM 不为算子配额装饰、require_operators / require_count 只是 prompt 软提示（引擎自己写明权威保证是契约骨架注入）；--enhance-diversity 缺省 never 已在 build_wave 与 batch_simulator 两处落地（DEC-33..53 已定） |
| GM-08 | fixed | Claude/skills/brain-make-some-gem/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | 范本保留：铁律 8 明写判死粒度 = 概念、不是数据集；RA 步 7 §7.4 已引用同一口径（想法级 dead_end 须全部变体 RN ≤ 0，并与 GEM 声明的 Expected Exposure 比对） |
| GM-09 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 「mode_b_required = true 怎么办」：它是提示（quality_predict EXPECTED_BLOCK > 0，或 prod_first 且有字段族 prod ≥ 0.7；wave_gate 也用同一预估、只作建议标注、刻度历史上失准）→ 照常进步 5 门禁、不据它丢候选 / 判死 → 原因写进本波 key_findings → 步 7 走 Mode B 想法层（modeb_improve），不做同族参数变体；探针 / 修复批用 wave_gate --batch-type probe\|repair 跳过 qp 标注。测试对节点与 wave_gate 源码逐项核对 |
| GM-10 | fixed | Claude/skills/brain-make-some-gem/SKILL.md \| Claude/skills/brain-make-some-gem/scripts/headless_runner/README.md \| Claude/skills/brain-make-some-gem/scripts/headless_runner/run.py \| Claude/skills/brain-make-some-gem/scripts/headless_runner/config.example.json \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/pipeline_data.py | 直接命令补齐：run_pipeline 收尾自己把表达式写进 expressions（status=gem，wave = s2_<DS>_d<DELAY>）并打 [db] 行，核对 = list_expressions(region, wave) 有行（此前误以为手跑不落库，读源码后更正）；--dry-run 只验证命令构建、验证不了 LLM；不再 cd + 裸 python，改仓库根 ；--priors-from-db 必带区域值；LLM 通道 / 凭据前置表（MOONSHOT_API_KEY / MOONSHOT_BASE_URL / 缺省模型 kimi-k2.6，给了 ideas_file 不需要密钥）。代码：run.py 凭据优先级改「环境变量 > config.json」（此前 config.json 无条件覆盖环境变量），moonshot_api_key 在 --ideas-file 模式不再必填，只报缺失键名不回显值，启动打 [cred] 来源行；新增 config.example.json（全空模板）；README 删把口令写进命令行的示例 |
| GM-11 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 「看实时输出」默认 --watch；--detached --console 明标 **Windows 专有**（DETACHED_PROCESS \| CREATE_NO_WINDOW 下终端天生看不到输出），代价（关窗口 = 杀任务、phased 无断点）保留；测试对 run.py 源码确认 Windows 分支 |
| GM-12 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 行号引用 gem.py:1219 改函数名 _find_final_expressions（测试确认函数存在、行号文本消失）；三段查找路径 + 旧位勿再用于新跑 + 文件不是真相源 全部保留 |
| GM-13 | fixed | Claude/skills/brain-make-some-gem/SKILL.md \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skills/README.md \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/pipeline_paths.py \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py | 范式保留，并把维护警示补上——但按代码更正其前提：这两份 SKILL.md 不是运行时 prompt（旧文与 pipeline_paths / run_pipeline 里「拼进 LLM prompt」「以空内容」两处措辞都写反，已改）；[skill-doc] MISSING / embedded:legacy 的真实含义 = skill 目录解析异常（FI 目录同时承载 ace_lib / validator 脚本）；维护警示：改 scripts/ 须回归 GEM 全链路，validator.py 与 alpha-expression-verifier 权威版四处一起改，漂移由 test_gem_skill_paths 守护 |
| GM-14 | fixed | Claude/skills/brain-make-some-gem/SKILL.md | 失败表新增 402 Insufficient Balance（表现为「no meta.json within 90s」、干跑假绿、不可重试、绕行 = 手写 manual ideas 走 ideas_file）与「LLM 通道不可达」（按 MOONSHOT_RETRIES 退避后抛）两行，401 改「看 [cred] 来源行」；stage 统一写 S2（stage 只是标签，路由按 subcommand，删 stage=S6 写法）；候选不足 → 显式扩容 / 分波 / 换数据集，不补参数变体凑数（与 RA 步 4 选波清单一致） |
| GM-15 | fixed | Claude/skills/brain-make-some-gem/reference.md \| Claude/skills/brain-make-some-gem/examples.md | 两份英文旧稿整体重写为中文并与 SKILL 对齐：reference 只放目录结构 / 模块职责 / workflow_gem 与节点的参数差异表（测试对照两者源码签名与缺省）/ run.py 参数 / 产物路径（data/gem_runs + DB，旧深嵌套位只标历史）/ 环境变量；examples 标准入口 = workflow_gem（此前把 run.py 当标准入口，与 SKILL 倒置），期望行为含落库核对，错误处理表 4 行（config 缺失 / 401 / 402 或 no meta.json / 候选不足）对应 SKILL 失败表的用户可见部分 |

## HF

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| HF-01 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md | 状态节（条件激活 / dormant）+ §1 分支表：目录缺失 → agent 按 §3 起草（干跑校验，闸即批准人，无人工批准点）；起草不出 → 回步 2 换集 / 冷门字段优先；「等假设生成器」与 RA「强制切换」互锁的死锁取消 |
| HF-02 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md | 上游改「RA 步 2 约束 6 路由 + s1_semantic_<ds>」，目录由 agent 按 §3 起草（字段扫描不产假设） |
| HF-03 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md | 切换信号统一为 RA 的两条可测信号（alphaCount ≥ 1 万 / 连续 2 波全灭）；news12 Fitness 0.42 个例与论坛 80 赞帖降为背景，不作触发 |
| HF-04 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md | 取消 data/field_semantics/*.yaml（无代码读、无闸执行，与 s1_semantic_<ds> 是两套互不引用的字段语义）；字段语义 = s1_semantic_<ds>；anchor-only 是纪律（只作条件 / 分母 / group），不是台账字段 |
| HF-05 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md | 示例改标准窗口（5 / 22），四条表达式形状经规范校验器实测通过；control_constant 语义写清（保持同结构、信号项换同集无关字段，不是数值常数；白名单外字段会被闸 2 拦） |
| HF-06 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md \| src/wqb/research/hypothesis_miner.py \| Claude/skills/wq-brain-ra-pipeline/references/concept-taxonomy-map.md | 类别词表单一来源 = hypothesis_miner.HYPOTHESIS_CLASSES：此前代码那份 12 类与 SKILL / 映射表几乎互不重叠且无调用方，现对齐为 SKILL 的 12 类；load_catalog 拒收词表外的类；测试守 SKILL / 代码 / 映射表三处一致 |
| HF-07 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md \| wqb_db_mcp.py | §5 完整回路表：干跑 → 实跑构建 → upsert_expressions(source=hypothesis) → 步 5 门禁 → 步 6 回测 → judge → 步 9 写回；给 judge 的手工命令；验证清单改 4 项产物；upsert_expressions 文档补 hypothesis 来源标签 |
| HF-08 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md \| src/wqb/research/hypothesis_miner.py | 四态 = 假设级结论，与波级 PASS/PARTIAL/FAIL 及数据集级 dead_end 分层；阈值引用代码常量（\|Δ\| ≤ 0.1 / 主 Sharpe < 0.3 / Δ > 0.5 且 fitness > 0.8）并注明是无校准记录的经验值；rejected 不写 registry；顺带修 judge 把「对照比主假设好」误判 partially_supported 的逻辑缺陷 |
| HF-09 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md \| src/wqb/workflow/nodes/hypothesis_round.py \| tests/unit/test_workflow_nodes.py | 台账两层：事实源 = 步 9 wave_results.key_findings；辅助日志 = tracking/hypotheses/ledger.jsonl（gitignore、不作事实源；节点缺省锚仓库根，此前相对 CWD）；data/hypothesis_ledger 从未存在、「元学习取代 bandit」删；顺带修节点单测每次回归往仓库账本追加一行（65 行 t1 垃圾） |
| HF-10 | fixed | Claude/skills/brain-alpha-research-hypothesis-first/SKILL.md | 字段选择与 FQ 反向：饱和集信号字段优先 users 0–9 冷门字段（占批次预算 ≥ 50%），热门字段只作门控 / 锚，alphaCount / userCount 不再作种子排序依据；引用 RA 步 3 §3.3 与 field-quality §1 |

## HP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| HP-01 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | 职责边界改为「只读 + 给出建议路径，不执行」；分流与判死回写归 RA 步 5b / 步 9（seal_dead_end） |
| HP-02 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | §0 三列表：18 个 RA_CHECK_NAMES + SELF / PROD 逐项「平台线 / 内部线（config 键）/ 读哪节」；无专项经验项如实写「暂无专项经验」；数字只在 config，正文只写键名 |
| HP-03 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | 删「配额从 submit 响应读」句；写明配额读取归 submit-alpha / next-move、读配额不得靠 POST submit、预检用 confirm_submit=False（本地放宽预检 + 查状态） |
| HP-04 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md \| Claude/skills/brain-how-to-pass-alpha-test/references/scenarios.md | Fitness 数值例（Sharpe1.6/Returns6%/Turnover 8%→≈1.11 与 12.5% 相同；40%→25%：0.62→0.78）、delay 取 settings.delay 对应列、与 playbook 的 √(505×margin) 互指；Sub-universe 数值例（TOP3000→TOP1000 门槛 0.433 倍，Sharpe1.6→≥0.69）与 NaN 报错对策 |
| HP-05 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md \| Claude/skills/brain-how-to-pass-alpha-test/reference.md \| Claude/skills/wq-brain-alpha-optimization-v1/references/structural-interaction-forms.md | 「分别对流动性/非流动性 decay」的加权相加示例删除，改用 bucket / group_* 写法（形态库 F4）；闸 5 infix_leg_sum / 加权混合会拦相加写法；同一结构两种写法判定相反的问题不再靠示例放行 |
| HP-06 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | CW 要点行直接写「中性化无效、有效手段是时间平滑」；每节标题带平台检查名 |
| HP-07 | fixed | Claude/skills/brain-how-to-pass-alpha-test/references/concentrated-weight-evidence.md \| Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | 证据表移 references/，正文只留合规式样；写明适用范围（IND/TOP500 分析师修正族、n=4）与未验证范围；窗口 10 不在白名单，复用时取 5 或 22；「末端再套 rank 反而 FAIL」标为假设。原始记录无 alpha id，如实标注无从补 |
| HP-08 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | CW=WARNING 计入 Failed RA（引 failed-gates 口径），删重述；「必 FAIL」改「4 例里 2 例 IS 阶段 WARNING 者提交后 FAIL」 |
| HP-09 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md \| Claude/skills/brain-how-to-pass-alpha-test/references/scenarios.md | Fitness 数值例（Sharpe1.6/Returns6%/Turnover 8%→≈1.11 与 12.5% 相同；40%→25%：0.62→0.78）、delay 取 settings.delay 对应列、与 playbook 的 √(505×margin) 互指；Sub-universe 数值例（TOP3000→TOP1000 门槛 0.433 倍，Sharpe1.6→≥0.69）与 NaN 报错对策 |
| HP-10 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | §6 拆 6a SELF（判据、取值途径与盲区、处置）/ 6b PROD（取值指向 prod-corr-avoidance §1，处置只按 D0-P）；「对负相关 alpha 做变换」语义不明已删 |
| HP-11 | fixed | Claude/skills/wq-brain-ra-pipeline/references/prod-corr-avoidance.md \| Claude/skills/brain-how-to-pass-alpha-test/SKILL.md \| Claude/skills/brain-alpha-robustness/SKILL.md | check_correlation 环境事实只写 prod-corr-avoidance §1 一处：阻塞轮询 30s×120、账号级单并发（correlation_busy 带 retry_after）、Redis 只是可选缓存（无 Redis 不缓存）、三种返回处置表、refresh 每决策点至多 1 次且间隔 ≥5 分钟（经验值）；how-to-pass / robustness 改指针 |
| HP-12 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md \| Claude/skills/brain-how-to-pass-alpha-test/reference.md | 决定：本库按单阈值处理，不实现平台「Sharpe 高 10%」豁免（GATES_PLATFORM / submit_queue.LIM 均单阈值）；写明数值例（1.9 vs 1.6 过 / 1.7 vs 1.6 不过）与「平台可能放行、本库先拦」的保守偏差 |
| HP-13 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | 删「TOP3000（USA）」，改引 wqb.config.REGIONS 各区默认 universe；ATOM 写成 判据 / 阈值（只引官方表）/ 适用对象 三项，并说明与 D3 / D11 / D14 跨集路线冲突时主动放弃 ATOM 放宽 |
| HP-14 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | 上游改读 backtest_results 表；下游链补 robustness → submit_verdict，与 INDEX 流水线一致；步号统一 |
| HP-15 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/references/mode-b-qualification.md | FAIL 回流改「建议路径（不执行）」：先做资格判定（主闸 + 旁路 + 判死线），再按 main_gate/bypass → Mode B、no_qualify → 不改不判死、dead_end → 候选级封存（forum_recon → seal_dead_end）；粒度分候选级 / 家族级；salvage 入池宽、动用严 |
| HP-16 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/references/mode-b-qualification.md | FAIL 回流改「建议路径（不执行）」：先做资格判定（主闸 + 旁路 + 判死线），再按 main_gate/bypass → Mode B、no_qualify → 不改不判死、dead_end → 候选级封存（forum_recon → seal_dead_end）；粒度分候选级 / 家族级；salvage 入池宽、动用严 |
| HP-17 | fixed | Claude/skills/brain-how-to-pass-alpha-test/references/two-year-sharpe-playbook.md | 判死范围改 (region, family) 并标 KOR 2022–23 证据出处；rank_by_side 标不在 known_ops、先 get_operators 确认；窗口 250/50/500 标白名单对应值；记 dead_end 的路径写明 forum_recon → seal_dead_end；IS_LADDER 阶梯数字标来源并链到 config 常量 |
| HP-18 | fixed | Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | §0 三列表：18 个 RA_CHECK_NAMES + SELF / PROD 逐项「平台线 / 内部线（config 键）/ 读哪节」；无专项经验项如实写「暂无专项经验」；数字只在 config，正文只写键名 |
| HP-19 | fixed | Claude/skills/brain-how-to-pass-alpha-test/reference.md | 删 63 行想法层通识（idea 来源 / arXiv / ATOM / 6 种字段探测 / 社区模板 / 官方例子），含 scale_down、中缀减法 + 窗口 240 的幽灵 / 非标写法；arXiv 路径问题随之消失 |
| HP-20 | fixed | Claude/skills/brain-how-to-pass-alpha-test/reference.md | 删 63 行想法层通识（idea 来源 / arXiv / ATOM / 6 种字段探测 / 社区模板 / 官方例子），含 scale_down、中缀减法 + 窗口 240 的幽灵 / 非标写法；arXiv 路径问题随之消失 |
| HP-21 | fixed | Claude/skills/brain-how-to-pass-alpha-test/references/scenarios.md | 5 张情景卡：Fitness 不过 / 仅 2Y 不过 / CW=WARNING / Sub-universe 不过 / SELF vs PROD |

## IR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| IR-01 | fixed | Claude/skills/brain-inspect-raw-template-create-setting/SKILL.md | description 重写：说清「外部 / 手写 idea JSON → 核对设置 → 写 expressions 表」，去掉全库无定义的「raw / 增强模板」用语；与 sim-alphas 的触发分开（这里不发起回测） |
| IR-02 | fixed | Claude/skills/brain-inspect-raw-template-create-setting/SKILL.md \| Claude/skills/brain-inspect-raw-template-create-setting/scripts/build_alpha_list.py \| Claude/skills/brain-inspect-raw-template-create-setting/scripts/process_template.py | 交接以 expressions 表为准；alpha_list.json 只有显式 --out 才写并声明「不是交接文件」；过时的「停止并交还 AI」提示同步重写 |
| IR-03 | fixed | Claude/skills/brain-inspect-raw-template-create-setting/SKILL.md \| Claude/skills/brain-inspect-raw-template-create-setting/scripts/process_template.py | 边界与步骤统一为「设置一律来自 settings.json / profile settings_proven / --set；本 skill 不做设置决策」，删「产出设置计划」「选定设置组合」 |
| IR-04 | fixed | Claude/skills/brain-inspect-raw-template-create-setting/SKILL.md | 新增「何时走本通道」三行表：GEM 已入库 → 不走本 skill（互斥）；外部 / 手写 idea → 本 skill（status=pending）；已在库按设置展开 → build_alpha_list.py --from-db（本脚本的参数，不是 pipeline 的） |
| IR-05 | fixed | Claude/skills/brain-inspect-raw-template-create-setting/SKILL.md \| Claude/skills/brain-inspect-raw-template-create-setting/scripts/load_credentials.py | 凭据标准名 CREDENTIALS_* 优先（旧别名 / config.json / ~/secrets 仍认），文档写全顺序；agent 不读 .env |
| IR-06 | fixed | Claude/skills/brain-inspect-raw-template-create-setting/SKILL.md \| Claude/skills/brain-inspect-raw-template-create-setting/scripts/process_template.py \| Claude/skills/brain-inspect-raw-template-create-setting/scripts/_workspace.py | cd 占位删；process_template 新增 --out-dir（缺省仍落 skill 目录 processed_templates/，已 gitignore 且不参与同步）；示例文件名改占位；作者盘符兜底并入 _workspace.py 一份（env > 上溯，无盘符） |
| IR-07 | fixed | Claude/skills/brain-inspect-raw-template-create-setting/SKILL.md \| Claude/skills/brain-inspect-raw-template-create-setting/scripts/build_alpha_list.py | DEC-39：实测战役 settings 的 nanHandling 7 OFF / 6 ON、maxTrade 8 OFF / 5 ON——不统一，所以不改缺省值，改来源透明：新增 --campaign-dir（没给的可选字段取战役 settings.json），并打印每个字段的来源；testPeriod 统一说法（无测试期 P0Y0M0D，P6Y 是真实测试期） |
| IR-08 | fixed | Claude/skills/brain-inspect-raw-template-create-setting/SKILL.md | 两个场景各标适用：生产回测中性化不能为 None（本 skill），字段探测要求 Neutralization: None（datafield-exploration）；情景 IR-B |

## IX

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| IX-01 | fixed | Claude/skills/INDEX.md \| Claude/skills/CONTRACT.md \| Claude/skills/CHANGELOG.md \| docs/env_and_switches.md \| tools/index_tables.py | 拆分：INDEX 只做路由与分层（460 → 约 275 行，其中三块由代码生成的表占大头；未做到 <150 行——闸表 / 逃生口表 / 区域表 / 计数是有意保留的生成物）；契约（frontmatter / 职责边界 / 硬裁定 / 共享产物 / 命名 / 质量门禁）→ 新增 CONTRACT.md；全部 ⚠ 日期条目、迁入记录、改名表、演进注记 → CHANGELOG「更早的历史」；环境变量 / 开关 / 凭据来源 → docs/env_and_switches.md；区域硬事实 → profile；审计叙事删（更正性结论进 CHANGELOG）。INDEX 头部 last_verified 与内容一致（不再有晚于锚点的条目）。守护：INDEX 不得再出现带日期的 ⚠ 变更史 / 迁入记录 / 契约段 |
| IX-02 | fixed | Claude/skills/INDEX.md \| AGENTS.md | 「仓库 = 编辑权威；安装位 = 运行时优先；改完必须 sync_skills 才对 Agent 生效」明写在 INDEX「权威副本与生效方式」，并进 AGENTS.md §8.10 与 skill 修改流程；解析顺序改指 _skill_roots()（不再抄一份）；已归档位置的处置记录移 CHANGELOG |
| IX-03 | fixed | Claude/skills/INDEX.md \| tests/fixtures/skill_lint_baseline.json | $WQ_PY 按平台给三行：Windows Scripts/python.exe、POSIX bin/python、跨平台自动探测（tools/_pyenv.py，顺序由测试对照源码）；INDEX 内裸 python 清零，skill_lint 的 bare-python 基线因此归零（全库 0 条违规）；venv 缺依赖指向 requirements.txt（含 vendored ace_lib 的 tqdm / Jinja2，DEC-57） |
| IX-04 | fixed | Claude/skills/INDEX.md | 持久化铁律只在 INDEX 定义，并补「允许写的文件只有五类」表：A 真相源 DB / B 运行态缓存 / C 静态配置与凭证 / D CLI 临时 @file / E 人读产物（planning-with-files 的三个规划文件、reports/、WAVE_LEDGER 快照归此）；消解「凭证仍用文件」与「禁止读 .env」的并存：凭证文件由脚本读、agent 不读；其余 skill 现为一句引用或各自指向缓存性质 |
| IX-05 | fixed | Claude/skills/INDEX.md \| tools/index_tables.py \| Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md | 区域表改由代码生成（config.REGIONS × profile 的 entry_verdict × tracking/<R>/config/ 目录扫描）并逐字比对：DEU 变 probe-only、AMR 目录 ✓ 两处事实错误随生成消失；entry_verdict 不再双写（表是导出物，冲突以 profile 为准）；TWN 的「缺目录」行为由生成规则给出；AMR 统一为「当前非挖掘区」一句，ALL 补进 contract §4（带日期的平台快照不进 INDEX） |
| IX-06 | fixed | Claude/skills/INDEX.md | 「Ln ≡ Sn」一句话声明，其余编号（步 / 闸 / 关）各自独立、不并用；L-INT 行与迁移史删除 |
| IX-07 | fixed | Claude/skills/INDEX.md \| Claude/skills/CHANGELOG.md | 迁入记录整节移入 CHANGELOG；删除线行、「通用非 WQ 元技能」「历史 .cursor 已移除」并入迁移记录；repair 行按其真实内容改写（配方索引，非改进入口）；不再声称元技能「共用运行环境约定」 |
| IX-08 | fixed | Claude/skills/INDEX.md | ①S5 行改「否决（资格门 + submit_verdict + prod 实测 + 稳健性闸，只能拦）/ 放行（用户确认 + workflow_submit_alpha）」并指向 submit-chain.md，「提交层唯一权威」删；②S3 产物改 backtest_results（alpha_list.json / status CSV 标运行态缓存）；③健康线补第三层「回填带」并说明数字只在 config / decision-table（本文不复写）；④S6 行补「日常回写由 RA 步 9 编排，monitor 只在故障排查 / 盯任务 / 复盘时触发并核验」 |
| IX-09 | fixed | Claude/skills/INDEX.md | 引擎映射表只写「阶段 → 子命令」；七槽填槽 / ThreadPoolExecutor / --max-rounds / linear_mix / 单批在飞串行 / 配额第 3 次重述全删（测试禁止这些实现细节回到 INDEX），细节留 toolkit 与 wqb-concurrency |
| IX-10 | fixed | Claude/skills/INDEX.md \| tools/index_tables.py \| src/wqb/config.py | 闸门阶梯改「按检查名」的生成表（平台线 / 内部线 / 来源常量三列）：IS Sharpe（LOW_SHARPE，Delay-1 / Delay-0 两档）与 2Y Sharpe（LOW_2Y_SHARPE / IS_LADDER_SHARPE）分开，GATES_PLATFORM.sharpe_min 明写取的是 2Y 线；config 侧拆分 PLATFORM_CHECK_LINES 已在此前批次落地，本次让文档由它生成；「层级」并入一句指向 RA 步 5–8 |
| IX-11 | fixed | Claude/skills/INDEX.md \| tests/unit/test_gate_registry_docs.py | 闸表由 gate.py 的 GATE_REGISTRY 生成（此前批次落地），含闸 2b / 2b-2 / 闸 9 与子闸；wave_gate 层的 SEM / PF / 体检 / 区域闸在「闸与逃生口总表」（waiver.GATE_POLICIES 生成）；INDEX 重写后测试仍逐字比对两块 |
| IX-12 | fixed | Claude/skills/INDEX.md \| Claude/skills/CHANGELOG.md | 计数只留现值（一行一项）；7 条 ⚠ 变更史按时间倒序整理后移入 CHANGELOG；补 tools_submit 0 的原因：原生 submit_alpha 工具 2026-09-02 已删、提交统一走 workflow_submit_alpha，所以「MCP 里没有 submit_alpha 工具」成立而 submit_batch 是仿真派发；计数仍由 test_mcp_tool_counts_match_index 守护 |
| IX-13 | fixed | docs/env_and_switches.md \| docs/env_registry.json \| tools/index_tables.py \| Claude/skills/CHANGELOG.md | 新建 docs/env_and_switches.md：变量目录表由代码扫描生成（缺省值与读取方取自源码，用途取自 env_registry.json，102 个变量，含 WQB_GLOBAL_SLOTS / WQB_GEM_MAX_PER_SKELETON 等 09-15 / 09-19 日志里的开关）、CLI 功能开关表、凭据来源登记；测试双向守护（代码读了未登记 / 登记了已不读都红）；两段功能变更日志（15 条）移入 CHANGELOG，INDEX 删 |
| IX-14 | fixed | Claude/skills/INDEX.md \| Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | 「70 / 30」「> 10 种结构才换数据集」删，改指 optimization-v1 的 mode-b-qualification.md（OP-02 已定义可度量的资格与切换判据）；09-01「MCP 直发批也过闸」落地记录移入 toolkit gate-rules.md（写明 create_multi_simulation 的静态门禁与 2–10 条限制） |
| IX-15 | fixed | Claude/skills/INDEX.md \| tests/unit/test_gem_skill_paths.py \| Claude/skills/CHANGELOG.md | 「嵌套副本」改四条可测纪律各配守护：#1 内嵌 scripts 必须在且 validator 与权威版逐字节相同（本次新增测试）、#2 FI SKILL.md 逐字一致、#3 dfe 不得有 SKILL.md 且三个副本一致 + GENERATED.md、#4 GEM 产物根在 skill 树外；审计叙事（含 09-29 对「进 prompt」的再更正）移 CHANGELOG；第 3 行（tracking/KOR/scripts 反斜杠写法的 9 个区域私有脚本）移出权威表，改「待清理」——它们仍在仓库里，README 记载「是否转薄 wrapper 由用户另行决定」，属待用户裁定事项，本轮不动 |
| IX-16 | fixed | Claude/skills/INDEX.md \| Claude/skills/CHANGELOG.md | 「并发口径（演进注记）」一节删：并发参数只留 config.CONCURRENCY 与 wqb-concurrency §8 两处（monitor §6 早已改为不复述）；旧 C=5 → Token-Bucket → 七槽的演进进 CHANGELOG |
| IX-17 | fixed | Claude/skills/INDEX.md \| Claude/skills/CONTRACT.md \| Claude/skills/CHANGELOG.md | 改名表删（保留规则与配套动作，进 CONTRACT §3）；改名清单作为历史进 CHANGELOG（带「旧名 / 迁移」字样，不触发旧名回潮扫描） |
| IX-18 | fixed | Claude/skills/CONTRACT.md \| Claude/skills/brain-alpha-judge/SKILL.md \| tests/unit/test_sf_docs.py | CONTRACT §1 逐字段定义：allowed-tools 可选（缺省继承宿主权限；能力棘轮不得超基线）、hooks 受限（白名单 + 逐条写明 + 危险模式扫描）、user-invocable / version / agent_created 语义；description ≤ 300 字、只写「何时触发 + 范围 + 不做」——全库机检（此前最长 702 字；judge 的中英重复 303 字已删到 ≤ 300） |
| IX-19 | fixed | Claude/skills/CONTRACT.md \| tools/skill_lint.py \| tests/unit/test_skill_lint.py \| tests/fixtures/skill_lint_baseline.json | 把「形式覆盖」补成内容一致性检查的一部分：① CONTRACT §2 写明「边界段『不做』的动作在正文出现须带『仅引用』标记」，并指出实质一致性靠各 skill 的 doc→code 测试（本轮已为报告点名的 6 个矛盾逐个写了）；② 新增 skill_lint 的 const-literal 检查（门槛数字抄写棘轮：数值与 config 相同且未引用常量名 / config.X / 来源标记即违规；现存 29 处登记进基线、新增必红——这是新检查类别的初始基线，不是掩盖新违规）；硬裁定①的权威常量清单补上 PLATFORM_CHECK_LINES / WAIT_THRESHOLDS |
| IX-20 | fixed | docs/ledger_keys.json \| tools/ledger_keys.py \| tests/unit/test_ledger_key_catalog.py \| Claude/skills/CONTRACT.md | 键目录（75 项：键 / 写入方 / 读取方 / 刷新责任 / 状态，含 orphan 与 legacy / deprecated）与「skill 出现的键必须在目录、被读的键必须有写入方」测试均已在此前批次落地；本次把共享产物表迁入 CONTRACT §4 并对齐现状：submit_ready 改「SQL 表单存储、ledger 同名键 legacy」、registry 写入指向 wqb.registry_contract、expressions 写入方写明 run_pipeline 收尾自己写 |
| IX-21 | fixed | Claude/skills/CONTRACT.md \| Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/README.md \| tests/unit/test_gem_skill_paths.py \| tests/unit/test_sf_docs.py | ①已废弃路径：GEM trailSomeAlphas/README.md 里残留的 .qoder/skills 随其重写清掉（该文件是英文旧稿，另有旧深嵌套产物路径、虚构的 MOONSHOT_MODEL 环境变量）；②相对链接 / .py 引用检查递归覆盖 references/**（test_docs_consistency 扫全部 *.md）；③守护输入可指定：_resolve_skills_dir 复用 _skill_roots（WQ_SKILLS_DIR 优先），依赖 gitignore 数据的测试在干净克隆里 skip 并说明原因，「失败于环境 vs 失败于内容」写入 CONTRACT §5；顺带：test_gem_skill_paths 的实跑解析此前在 Linux 永远 skip（DEC-57） |
| IX-22 | fixed | Claude/skills/INDEX.md | 配额只留指针（单一来源 quota-and-tower.md）与一句话模型；日界按 America/New_York 计算，GMT+8 的 12:00 / 13:00 明写「不要写死」（quota_status.py / pipeline 已在此前批次改用 wqb.timeutil）；移除史与 get_submission_quota 叙述删；裸 python 改 $WQ_PY |
| IX-23 | fixed | Claude/skills/INDEX.md \| Claude/skills/CHANGELOG.md \| Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/JPN.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/IND.md | 「2026-09-19 平台区域硬事实」整节移出 INDEX：ALL / AMR 选项 → region-profile-contract §4（带日期、标平台不可达未复核）；JPN 无 pv1 → JPN profile 硬事实 6（此前已在）；IND robust 闸定义与破墙配方 → IND profile（此前已在）；prod 竞速 → ra-pipeline 决策表 D0-P 与 incidents I-2（此前已在）；历史原文进 CHANGELOG |
| IX-24 | fixed | Claude/skills/INDEX.md | 首节新增「任务 → skill 场景路由表」16 行（用户说 / 首选 / 不选谁与为什么），覆盖报告点名的四组歧义：提交（submit-alpha / superalpha / judge）、监控回测（monitor / ra-pipeline 步 9 / batch_track）、修复弱候选（repair / optimization-v1）、相关性（how-to-pass / selfcorr-quick / robustness / prod 墙 D0-P）；测试要求每行点名的 skill 都真实存在 |

## JD

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| JD-01 | fixed | Claude/skills/brain-alpha-judge/SKILL.md | description 收敛为「提交前参考评审（PPA 核对 / trend / 点塔排序）；不判定、不提交」，删「确认后提交」与 MEA 区域状态；user-invocable 在 INDEX 里登记含义 |
| JD-02 | fixed | Claude/skills/brain-alpha-judge/SKILL.md | 边界只留首屏一处；旧「两道硬闸 + 六步 + 确认后提交」骨架、弃用声明、确认规则 / 提交路由整节删除；正文重排为三职能各一节 |
| JD-03 | fixed | Claude/skills/brain-alpha-judge/SKILL.md \| Claude/skills/brain-alpha-judge/scripts/vendor/ace_client.py \| Claude/skills/worldquant-submit-alpha/references/submit-chain.md | 删「提交语义（GBR 旧口径）」整节；vendor get_submit_verdict 只 GET、submit_alpha 只抛错；全库 GET /submit 口径只留 submit-chain（SUPER 的差异见 SP-11 needs-platform） |
| JD-04 | fixed | Claude/skills/brain-alpha-judge/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/submit-chain.md | judge 不再自述翻转延迟 / 二次 POST；唯一提交状态机 = submit-chain §2（REGULAR / SUPER / 补发在同一张表里） |
| JD-05 | fixed | Claude/skills/brain-alpha-judge/SKILL.md | 链按 AGENTS.md：资格门 → robustness → submit_verdict → prod 实测 → 用户确认；judge 标「可选参考、不在必经链上」；删「引用 robustness 结论」（脚本不读）；对照表保留并改口径 |
| JD-06 | fixed | Claude/skills/brain-alpha-judge/SKILL.md | 语料一节改为：静态快照、篇数与生成日期见 index.json（21 篇，2026-04-12）、无更新机制；建库史删除 |
| JD-07 | fixed | Claude/skills/brain-alpha-judge/scripts/vendor/load_credentials.py \| Claude/skills/brain-alpha-judge/configs/config.example.json \| Claude/skills/brain-alpha-judge/scripts/judge_alpha.py \| Claude/skills/brain-alpha-judge/SKILL.md \| tests/unit/test_judge_never_submits.py | 凭据只读进程环境变量 CREDENTIALS_EMAIL/PASSWORD（旧别名保留）；不读 .env / config.json 明文 / ~/secrets；发现明文只在 stderr 提示迁移不打印值；降级运行 verdict 上限 REVIEW、报告首行标降级、JSON 有 degraded 字段；示例配置删 username/password |
| JD-08 | fixed | Claude/skills/brain-alpha-judge/SKILL.md | 「运行与降级」+ 各职能表：每项写输入 / 命令 / 来源；PPA 闸触发条件统一为 type=PPA 或标签含 PowerPoolSelected；删「第 6 步提交」 |
| JD-09 | fixed | Claude/skills/brain-alpha-judge/SKILL.md \| Claude/skills/brain-alpha-judge/scripts/judge_alpha.py \| tests/unit/test_judge_gates_match_config.py | 颜色 PURPLE（脚本不校验，明写）；PPA Sharpe 线 1.0 与平台 LOW_SHARPE value<1 一致（新增一致性测试，脚本注释早已引用却不存在）；WAIT_THEME_ROTATION 明写「没有代码实现」并更正 RA 文档里的错误说法；CW 配方改指 how-to-pass §4（时间平滑），删被禁的加权相加推荐 |
| JD-10 | fixed | Claude/skills/brain-alpha-judge/SKILL.md \| Claude/skills/brain-alpha-judge/scripts/vendor/llm_judge.py \| Claude/skills/brain-alpha-judge/scripts/judge_alpha.py \| Claude/skills/brain-alpha-judge/configs/config.example.json \| tests/unit/test_judge_never_submits.py | LLM 缺省关闭；外发字段白名单写明（表达式原文默认不外发）；密钥只认 BRAIN_JUDGE_LLM_API_KEY（不读配置 api_key、不回落 OPENAI_API_KEY）；LLM 只能收紧确定性判定（stricter_verdict），overall_verdict 上界可复现；删「Agent 模式」的无对象说法；示例与模板一致 |
| JD-11 | fixed | Claude/skills/brain-alpha-judge/SKILL.md | 建议格式 {动作, 对象, 预期, 验收}；证据 id 可选；删「至少 3 条」数量下限与「必须引用语料」 |
| JD-12 | fixed | Claude/skills/brain-alpha-judge/SKILL.md | ATOM 术语区分（judge = SINGLE_DATA_SET 纯度；how-to-pass = 提交标准放宽档）；S_P（宏观多样性）与点亮数（先提哪颗）分工写明；trend delta 标「仅信息、无决策用途」 |
| JD-13 | fixed | Claude/skills/brain-alpha-judge/SKILL.md \| Claude/skills/brain-alpha-judge/scripts/judge_alpha.py \| tests/unit/test_judge_never_submits.py | PowerShell 命令换成 $WQ_PY；补退出码 / 输出位置；证据字段表（字段 → 来源）；--alpha-id 模式自动取平台三段式 description 补 idea_summary / rationale（此前 economic_foundation 天生不过） |
| JD-14 | fixed | Claude/skills/brain-alpha-judge/SKILL.md \| Claude/skills/brain-alpha-judge/scripts/judge_alpha.py \| Claude/skills/brain-alpha-judge/scripts/vendor/ace_client.py \| tests/unit/test_judge_never_submits.py | --confirm-submit 移除（传入报错退出 2）、vendor submit_alpha 只抛错（由测试守）；路由条件改为「submit_verdict ≠ BLOCKED + 用户确认」，READY 是本 skill 词汇；prod 墙只引 D0-P |
| JD-15 | fixed | Claude/skills/brain-alpha-judge/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/quota-and-tower.md | 点塔排序只在 quota-and-tower §2（judge 只链接）；分档更正为「差 1 颗 / 差 2 颗 / 差 3 颗」，「差 1–2 颗一次点亮」的旧错误在该文档 §2.2 修正 |
| JD-16 | fixed | Claude/skills/worldquant-submit-alpha/references/quota-and-tower.md \| Claude/skills/brain-alpha-judge/SKILL.md | UNKNOWN 塔不预测（quota-and-tower §2.3）；_tower_map 审计注记、GET /data-fields 说明随 JD-15 从 judge 删除 |
| JD-17 | fixed | Claude/skills/brain-alpha-judge/references/developer-notes.md \| tests/unit/test_judge_gates_match_config.py | 「独立原则」等开发者规约移到 developer-notes.md；INDEX 的内部闸第 3 份拷贝有一致性测试 |
| JD-18 | fixed | attic/judge_planning_docs_20260929/README.md \| Claude/skills/brain-alpha-judge/references/extra-standard-rubric.md \| Claude/skills/brain-alpha-judge/SKILL.md | improvement-roadmap / future-improvement-guide 归档到 attic；rubric 以 JSON 为机器可读源（英文说明加来源声明）；SKILL 补「证据字段」表 |
| JD-19 | fixed | Claude/skills/brain-alpha-judge/references/scenarios.md | 情景卡 JD-01 PPA 候选（Sharpe 1.2 / PPAC 0.42 / 主题匹配）、JD-02 多候选点塔排序（3 个候选，预期 X > Y > Z）、JD-03 降级运行（输出不能作依据） |

## LB

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| LB-01 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md | 新增「与 REGULAR 流水线的关系」表：Python 轨道 vs FASTEXPR；结论只作线索、不进提交路径；衍生 FASTEXPR 表达式按外部 idea 走 inspect-raw 入库通道；阶段定位统一为「S0 前研究，线索给 S1」 |
| LB-02 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md \| Claude/skills/alpha-template-labs-data-analysis/references/agent-spec.md | 规范文档由 docs/reference 移入 skill 的 references/agent-spec.md（git mv），链接改 skill 相对；同时按引擎实际字段形态与 artifact 键重写 |
| LB-03 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md | 第 4 步显式标【人工 · 在此暂停】并写明对用户的话术与「收到 JSON 前不得继续 / 不得编造」；第 2 步【需用户同意】并定义：新开会话占用账号唯一的交互会话，先问用户 |
| LB-04 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md \| Claude/skills/alpha-template-labs-data-analysis/references/agent-spec.md | labs_output 写明是 Labs 内（Linux）路径，/tmp 正确；ingest_labs_result 只解析不落盘（测试）；一次性分析 JSON 不是战役产物、不入 DB，建议 --output tracking/_scratch/（缺省 tracking/runs 会被 git 跟踪，已警示） |
| LB-05 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md | 第 8 步给固定回报格式与填好的例子（字段 / 形态 / 覆盖 / 诊断 / 接受或拒绝 / 理由 + 机制 + 对 RA 的线索） |
| LB-06 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md | rtk 说明删除；CLI 统一 & $WQ_PY world-quant-brain-mcp/labs_data_analysis_agent.py；子命令表（含文档里原先缺的 screen-os-clues / run-csv）与代码逐个核对 |
| LB-07 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md | 「禁止 VECTOR/GROUP」注明仅 Python 轨道；FASTEXPR 轨道用 vec_* / group_*（RA / GEM） |
| LB-08 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md | 体检数据包写明 WebData_20260219（2026-02-19 打包，逐字节体检覆盖 2012–2021）；check_expr_against_inspect 的调用入口改指 field_inspect_gate.py（wave_gate 内置） |
| LB-09 | fixed | Claude/skills/alpha-template-labs-data-analysis/SKILL.md \| world-quant-brain-mcp/labs_data_analysis_agent.py | 默认示例保留结构（字段 / 角色 / 倾向 / 骨架），但修正一处与引擎相反的内容：imb5_mktcap 是直接市值数据，被引擎的 no-PV / no-direct-market-data 约束排除，只可做相关性诊断，不作上下文；测试用引擎函数断言 |

## ME

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| ME-01 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md | description 改触发句「每波 S6 收尾 / 下一轮选字段前读经验时使用」。allowed-tools 有意不补：补了等于给该 skill 预批准工具（能力基线棘轮要求人审），缺省=无预批准更安全 |
| ME-02 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md \| tests/unit/test_ledger_key_catalog.py | 「s6_verdict_<wave> 回写」改为「upsert_wave_result（含 verdict）」，结尾改「结构化结论不经本 skill 回写：波结论 upsert_wave_result、判死 seal_dead_end」；DEPRECATED_TEACHING_BASELINE 清零（最后一处已改） |
| ME-03 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md | 判死粒度那条保留并放进「主流程连接」（单次失败只约束搭配 + 结构 + 设置） |
| ME-04 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md | --delay 统一写「传本战役的 delay」（只接受 0 / 1，代码 choices） |
| ME-05 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md | 加「核验」一节：命令 Select-String '范围：\|筛选：' + 期望（范围行含区域 / 数据集 / 全部波次 / 去重后 N 条 = rows=N；筛选行与传参一致），并解释并发编辑被拒 |
| ME-06 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md | 新增「文件骨架」（BEGIN/END 块 + ## 人工机制复盘 五个子标题，与工具对新文件的实际写法一致，测试守）；五节各写什么保留；补 post-wave-reading 的纠错复验链接与 README 索引链接 |
| ME-07 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md | 反 cherry-pick 护栏保留（不拼接不同候选最好指标；有测量缺陷的比较不作证据） |
| ME-08 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md \| docs/ledger_keys.json | research_leads_w<W> 已登记进 ledger 键目录（S-D，文档指 post-wave-reading.md），本文引用并指向该页 |
| ME-09 | fixed | Claude/skills/brain-dataset-mining-experience/SKILL.md | 写明 tools/dataset_experience.py 只是薄壳，参数解析与实现在 src/wqb/research/dataset_experience.py |

## NM

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| NM-01 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md | description 加「区域态势 / 哪个区更值得挖 / 该不该转区 / 下一步做什么」触发，并写明只报告不决策 |
| NM-02 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md | 边界改「报告器」：转述 region_status 输出，选区决策归 wqb.region_rotation（region_status --rotate / MCP region_rotation）与 matrix；写明它是 ra-pipeline 的转区出口 + 每 ET 日日报、不是前置；层名统一 L0 |
| NM-03 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md | S0 白名单归属改指 RA 步 2 / 决策表 D4，删 ppa-mining §1.0 的指向 |
| NM-04 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md | §3 固定建议模板（动作 / 依据 / 前置检查 / 预期成本 / 何时复核）+ 三项前置检查（点亮塔 category_lit、跨区弱先验、停波闸 A/B1/B2），命中即改写为替代动作；选塔以「未点亮」为准，不以乘数为准 |
| NM-05 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md | §2.1 定 Alpha 表现取数范围：OS 全量分页 + 新提交；IS 不枚举，只看自上次日报新增 + 可提交队列（get_submit_ready）；单颗深挖限被点名者；IS/OS 词义按 get_user_alphas 文档 |
| NM-06 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md \| tools/region_status.py | 手动口径整段删除，只引用 tools/region_status.py 输出；区域清单改「config.REGIONS（现 14 个）」；判据数值提为 region_status 顶部常量（PASS_SHARPE_MIN 等），文档表由测试钉死 |
| NM-07 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md \| tools/region_status.py \| Claude/skills/wq-brain-campaign-matrix/SKILL.md | 「≥10 且风格同质」拷贝删除：prod_saturation 只认 region_status 的 pass_ge_158 ≥ 10（matrix 同源，测试断言）；probe-only 名单删，改指 profile entry_verdict |
| NM-08 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md \| tools/region_status.py | 输出表加列并写明口径：宽口径 pass_ge_158（只看 Sharpe）与严格口径 ra_clean（get_mining_yield）并列；4 个建议动作各给一条数值判据，与代码逐条对应 |
| NM-09 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step1-inventory.md | entry_verdict 三态默认含义只有 step1-inventory §1.1 一处定义（RA 已补）；本 skill 只引用，并写明「数据侧建议不覆盖 entry_verdict」 |
| NM-10 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md \| tests/unit/test_se_docs.py | 「注册名含大写 S…勿再改」开发者备注删除，改由测试断言文档引用的每个 MCP 工具名在代码里真实存在 |
| NM-11 | fixed | Claude/skills/brain-next-move-analysis/reference.md | reference 改规范体：不再「交接给秘书」，示例日期 / 用户 ID 全部占位；只写各章怎么取数与字段怎么读 |
| NM-12 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md \| Claude/skills/brain-next-move-analysis/reference.md | get_ny_time.py 指令删除（脚本从未存在）；唯一取时方式 = wqb.timeutil.et_now()，命令写入 SKILL §1 且由测试实跑 |
| NM-13 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md \| Claude/skills/brain-next-move-analysis/reference.md | 大纲只在 SKILL 一份（含区域态势章）；reference 各章按「怎么取数 / 字段怎么读」组织，无第二套章节号 |
| NM-14 | fixed | Claude/skills/brain-next-move-analysis/reference.md | 删除「authenticate 提供邮箱和密码」——MCP 的 authenticate 没有参数、凭据由服务端读取（测试绑到签名）；leaderboard 用户 ID 占位；get_events 无参数（删 random_string）；get_messages 与 RA 对齐 limit=30；认证失败请用户在本机登录 |
| NM-15 | fixed | Claude/skills/brain-next-move-analysis/SKILL.md \| Claude/skills/brain-next-move-analysis/reference.md | IS/OS 词义按平台（IS=未提交、OS=已提交），正在回测的归 wq-backtest-monitor；工具清单去重 |
| NM-16 | fixed | Claude/skills/brain-next-move-analysis/reference.md | 论坛默认不查，仅用户点名或公告出现需查证的规则变更时才读；任务清单不指定宿主专有工具名 |
| NM-17 | fixed | Claude/skills/brain-next-move-analysis/reference.md | 错误防范改「常见误读（症状 → 原因 → 防范）」表：达标≠可提交、已点亮塔被推荐、停波区仍建议再开一波、事件章含过期项；GAC 案例保留并写成三段式 |

## NS

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| NS-01 | fixed | Claude/skills/brain-alpha-research-news-sentiment/SKILL.md \| docs/reference/news_bucket_field_map.md | 6 桶表（设计目标 / 优先级 / ● 强适配家族 / ◐ 可选，HIGH = Dispersion / Event-conditioned / Propagation）内联进 SKILL，逐格由测试对照 news_bucket_field_map.md 的矩阵；链接文字改成真实仓库根路径；顺带更正分类器事实（覆盖只有 news12、缓存路径 tracking/taxonomies、novelty 归 attention、is_news_dataset 只认 category==news 与三个前缀） |
| NS-02 | fixed | Claude/skills/brain-alpha-research-news-sentiment/SKILL.md \| docs/reference/news.md | news12 字段码 M → C（旧称 M，SKILL 与 news.md 同改），与 motif M1–M6 不再撞字母；M4 取舍判据：参照预期 / 事件典型值 → Surprise，参照该字段自身历史 → Change（motif 原始定义仓库里没有，只留映射） |
| NS-03 | fixed | Claude/skills/brain-alpha-research-news-sentiment/SKILL.md \| docs/reference/news_dataset_portfolio.md | Tier A 改「候选来源」：路由前三查（判死 / 跨区弱 / lit 塔，读 s0-select 标记），命中任一即不路由；验证清单不再固化「优先路由 Tier A」；Tier A 门槛补 alphaCount/fieldCount ≤ 5 与 typed-catalog 覆盖 |
| NS-04 | fixed | Claude/skills/brain-alpha-research-news-sentiment/SKILL.md \| docs/reference/news_dataset_portfolio.md | wqb news-refresh-portfolio 从未存在：SKILL 与 docs 都删，改指 get_datasets(category=…) 与 S0 recommend_datasets；连带删 news_loop.py / P15_EVENT_CONDITIONED / Beta 桶采样等文档里的不存在实现，6 桶与「每批 ≥ 3 桶」明示为指引、无代码闸 |
| NS-05 | fixed | Claude/skills/brain-alpha-research-news-sentiment/SKILL.md | Tier B 告知之后三个分支：假设优先（缺省，RA 步 2 约束 6）/ 放弃 / 用户坚持则只许高度非对称结构且先做 prod-first（D0-P） |
| NS-06 | fixed | Claude/skills/brain-alpha-research-news-sentiment/SKILL.md \| docs/reference/news_dataset_portfolio.md \| docs/reference/news.md | portfolio 与 news 文档标 2026-04 快照、以 get_datasets / S0 实时读数为准；Tier B α 数写日期；「Hard gates」改「设计目标（无代码闸）」，playbook 幽灵算子表补 neutralize 并由测试钉死 = config.GHOST_OPERATORS |

## OP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| OP-01 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | description 去掉「把 PROD 压到 0.7 以下」的承诺；职责边界写明「不承诺压 PROD，prod 墙只按 D0-P」；本 skill 只承接 D0-P 的「唯一例外」（组合腿救援）与「踩线带 1 次结构性尝试」 |
| OP-02 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | 删「70%/30% 精力」（无可度量含义）；三个上限合并为一条止损阶梯（第 3 个周期救援 / 第 5 个判死 / 累计结构 >10 换数据集）；每步预算改调用数 / 条数，不按分钟 |
| OP-03 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | 删「70%/30% 精力」（无可度量含义）；三个上限合并为一条止损阶梯（第 3 个周期救援 / 第 5 个判死 / 累计结构 >10 换数据集）；每步预算改调用数 / 条数，不按分钟 |
| OP-04 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/arXiv_API_Tool_Manual.md \| tools/sync_skills.py | 写明 arXiv 外发边界（查询词发 arxiv.org、只发通用关键词；--llm 才把公开摘要发第三方 DeepSeek，密钥仅环境变量 / gitignore 的 .arxiv_llm.env）；explain 里的重复脚本删除、全库只留一份；sync_skills 不再复制 *.env |
| OP-05 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | 删 create_multiSim 改错史 |
| OP-06 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/reference.md \| Claude/skills/wq-brain-alpha-optimization-v1/examples.md | Mode A 结果入库（harvest_multisim_alphas → harvest_multisim_results → backtest_results），迭代日志写回复并进 S6 key_findings，不再写自建文本文件；示例 / 提示模式同步改 |
| OP-07 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/reference.md | 算子数 ≤8 标注 PPA-only；REGULAR 无上限，复杂度纪律引 GEM「复杂度预算」与 robustness 软标记；operatorCount 仍以平台返回为准 |
| OP-08 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/reference.md \| Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | Stage A / B 在 reference §6.5 定义（微调闸 Sharpe>1.40 且 Fitness>0.90），SKILL 硬规则 5 指向；注明与 toolkit 探针里的 Stage A/B 不是一回事 |
| OP-09 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/reference.md | 校验层固定三段：verifier → campaign_intel ghost-audit → wave_gate --batch-type repair（写明命令、退出码、validate_expressions 不查幽灵算子）；删「当前项目暴露时使用」的条件式措辞 |
| OP-10 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | 删「陷阱」节：SuperAlpha 构造无关、PROD 闸门并入 D0-P 节；EVENT / winsorize 条并入 B2 一句（闸 8 会拦） |
| OP-11 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/references/mode-b-qualification.md | salvage min_sharpe 由 0.5 改为可选 1.0（与 review_wave combo_sharpe_min 缺省 1.0 同口径；缺省不传）；入池线 / 动用线区别写进资格判定表 §5；触发线改引判定表 |
| OP-12 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/references/structural-interaction-forms.md \| Claude/skills/wq-brain-ra-pipeline/references/step7-diagnose.md | 「一句话说清单一经济信号」换成五类可检的入场方式（条件 / 分组轴 / 残差化 / 协动对象 / 同源价差）；F1 限同源（用户 2026-09-28 spread_signal_ruling，跨数据集 subtract 由闸 5 spread_cross_dataset 拦）；hump 统一为「仍受支持、必须命名参数」（RA D6）；RA §7.7.2 补 ⑦ 协动对象并链到形态库（此前漏列） |
| OP-13 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/references/mode-b-qualification.md | salvage min_sharpe 由 0.5 改为可选 1.0（与 review_wave combo_sharpe_min 缺省 1.0 同口径；缺省不传）；入池线 / 动用线区别写进资格判定表 §5；触发线改引判定表 |
| OP-14 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | 「过拟合与稳健性测试」四项删除，改为指向 brain-alpha-robustness（同库 L4，判据与阈值只有一处）；「外部 Agent 技能」措辞更正 |
| OP-15 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | 「提交层权威判定」改「提交前否决闸；放行须用户确认」，与 GLOSSARY 的否决 / 放行两权威一致 |
| OP-16 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/reference.md | 预期产出 / 完成定义不再手抄 Sharpe / Fitness / 换手区间，改引 wqb.config.GATES_INTERNAL 与 Failed RA==0 |
| OP-17 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | 预期产出改「出现达标候选，或触发止损阶梯（判死回写）」，消除无终止条件的循环 |
| OP-18 | fixed | Claude/skills/wq-brain-alpha-optimization-v1/references/mode-b-qualification.md \| tools/mode_b_qualify.py \| src/wqb/workflow/mode_b_config.py | 资格线单一真相源：判定表（主闸 + 旁路 A–E + 判死线 + 覆盖优先级 + 各入口覆盖范围）；数值 / 动作文案与 _DEFAULT_GLOBAL 逐项对拍，覆盖顺序更正并钉住；只读 CLI 补 judge 节点喂不到的 A/B/D；「未达资格线一律判死」由测试扫全部 skill 文档禁止 |

## PB

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| PB-01 | fixed | Claude/skills/pull-brain-skills/SKILL.md \| Claude/skills/pull-brain-skills/scripts/pull_skills.py | 代码侧（暂存目录 / 静态审查 / 不删除 / 活跃根守卫 / zip-slip）已由 3987274 落地；本轮 SKILL 重写：边界写明「不安装、不执行被导入内容」、审查报告怎么读、导入后清单、出现 hooks / Bash / .env 读取的处置 |
| PB-02 | fixed | Claude/skills/pull-brain-skills/SKILL.md \| Claude/skills/pull-brain-skills/scripts/pull_skills.py | 示例默认不带 --overwrite；--overwrite 只挪到 .backup 不删除（代码已是），文档写明可恢复路径 |
| PB-03 | fixed | Claude/skills/pull-brain-skills/SKILL.md \| tests/unit/test_pull_skills_safety.py | 文档默认目的地改为与代码一致（attic/import_staging/），新增测试断言文档与代码的默认目的地 / 选项一致 |
| PB-04 | fixed | Claude/skills/pull-brain-skills/SKILL.md \| Claude/skills/pull-brain-skills/scripts/pull_skills.py | ZIP 示例改固定 commit SHA（分支头是可变引用）；--branch 只对 Git 生效并在其它源提示；下载加超时（60 s）与大小上限（50 MB） |
| PB-05 | fixed | Claude/skills/pull-brain-skills/scripts/pull_skills.py \| Claude/skills/pull-brain-skills/SKILL.md | 拉取成功但一个都没导入 → 退出码 4（不再 ok:true 退出 0）；新增 --subdir 支持 skills/<name>/ 二级目录（路径不得越出仓库）；「有效 skill」只查 SKILL.md 存在，契约检查放导入后清单 |
| PB-06 | fixed | Claude/skills/pull-brain-skills/SKILL.md | 导入后 7 项清单（看报告 / 归层 / frontmatter / 边界段 / 命名 / 移入并 sync + 测试 / 回滚），命令用 $WQ_PY，含 test_skill_boundaries |
| PB-07 | fixed | Claude/skills/pull-brain-skills/SKILL.md | 三张情景卡：GitHub 仓库导入到审查区并读报告 / 同名更新（diff + 合并）/ 发现 hooks 或读 .env 的拒绝与留痕 |

## PP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| PP-01 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | description 收窄为「开 PPA 战役 / 判断数据集能不能打 PPA」，从触发里撤出「所有 WQ 挖矿 / 开新战役必须先执行 §1.0」；§1 第一屏写明硬门槛只适用 PPA 模式，RA 走决策表 D4 |
| PP-02 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | 删「PPA 主题匹配核查」承诺，边界改为：挖矿期在 ra-pipeline 步 1 §1.6 / ppa-vs-ra §1，提交期在 worldquant-submit-alpha 的 PPA 通道 |
| PP-03 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | §2「体检怎么做（agent 取数路径）」表：每个面板对应命令 / 产物；UI 操作只作人工核对备注；字段级表数值来自体检硬门源码（测试钉死） |
| PP-04 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md \| attic/ppa_mining_20260929/README.md \| Claude/skills/INDEX.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/ASI.md | DEC-46：唯一执行器 = workflow_campaign(stage=S0) + s0-select；dataset_health_check.py（自读 .env 直连、零调用方）归档；127.0.0.1:8876 / --mode direct 等环境细节随之移出；INDEX S0 行、ASI profile、RA 的作废说法表同步 |
| PP-05 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | §1 阈值对照表：PPA / RA / 代码缺省（逐项由测试对照 score_datasets.py）；适用域移到第一屏；alphaCount == 0 改「只做探针」（与 probe-scoring-v2 一致），cov ≥ 0.9 且字段 ≥ 10 才优先 |
| PP-06 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | EUR 32 次回测教训保留，并补后续验证状态：ac = 0 的集多为伪白空间——体检是必要条件不是充分条件 |
| PP-07 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | §4 只留红 / 黄 / 绿判据 + 查询命令（get_dead_ends / get_campaigns / get_cross_region_lessons），快照与 6 组红灯清单删除（registry 才是事实源）；跨区外推统一按 RA 跨区先验规则，单区判死不外推 |
| PP-08 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | §1 三个「最优拥挤度」口径并成一张表：轴（平台 alphaCount vs 离线提交量 count）/ 区间 / 出处，源码逐项核对 |
| PP-09 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | §5.1 中性化：dominant method 只在实测更优且 IS_LADDER 仍达标时采用，否则 D5 禁用 SECTOR / MARKET |
| PP-10 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | 离线包 ★★★ 一节保留（场景 → 规则 → 动作），补「只影响本地分析质量」 |
| PP-11 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | OS 退化量化为 IS − OS > 0.15（webdata_quality 的 degraded 与 field-quality 同阈值） |
| PP-12 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | is_placeholder 删除（非 BRAIN 算子）；缺失 / 偏斜 / 峰度阈值改为体检硬门的真实数值（cr < 0.4、\|skew\| > 2、kurt > 8、频率最小窗口、trade_when 门控） |
| PP-13 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md \| src/wqb/research/evidence.py \| Claude/skills/alpha-expression-verifier/scripts/validator.py | V9 带 0.35 权重的配方删除作配方（标「已删除」并说明违反路线 A）；给合规改写（returns 反转作 trade_when 条件、标准窗口 22/66/252）；核实闸 5 现已拦 X + Y*0.35（infix_leg_sum，实测）；顺带修 subtract 命名参数 filter=true 被本地闸误拒（DEC-48） |
| PP-14 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | 白空间表降为「候选池来源」，必须再过体检与跨区先验；KOR Sentiment 空白 vs 新闻三连死的矛盾写清读法（空白只说明没人试，不说明能出货）；快照移出 |
| PP-15 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | §9 步 6 分「指标补齐」与「质量」；罕见算子须先过闸 5 与语法闸；符号映射表删（解析工具的实现细节） |
| PP-16 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | 删「C = 5」，指向 wqb-concurrency（config 里 slots = 7） |
| PP-17 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | testPeriod：无测试期写 P0Y0M0D，P6Y 是真实 6 年测试期也是平台最大值，两回事写清 |
| PP-18 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | hump 状态统一：仍受支持但必须命名参数 hump(x, hump=k)（决策表 D6；预闸自动改写位置形态）；旧「破坏性勿用」删 |
| PP-19 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | §8 闸门线逐项对齐 config.GATES_PLATFORM / GATES_INTERNAL / PLATFORM_CHECK_LINES（测试）；Margin>5bp / Returns>5% 平台硬线说法删；PPAC 展开为 Power Pool 相关性 |
| PP-20 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | 步 4「加 returns 反转组合」改单信号 / 同源价差 / 辅助腿三式；步 5 删「权重」，参数只在有依据的少数维度内扫并记录理由 |
| PP-21 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | 步 8 改「PPA 由用户在 web UI 提交，agent 出清单 + 主题匹配证据 + ppa_handoff 交接单」；PowerPoolSelected 的 MCP 提交明示会被拦（测试） |
| PP-22 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md \| Claude/skills/wq-brain-ppa-mining/references/region-snapshots-2026-08.md | §8 快照移到 references/region-snapshots-2026-08.md（带日期、失效条件、「不是行动指令」，并写明此后证据反向）；SKILL §10 只留选区方法；倍率差表只留方法与当时数字 |
| PP-23 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | 删「自行实现 _reauth()」「429 退避 min(20+attempt*8,45)」「lavender1203 fork / 端口 8876 / Trust」；改「用 BrainApiClient，429 处置见 wqb-concurrency」；MCP 工具罗列删 |
| PP-24 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | 合法 universe 表删（含已停提的 ILLIQUID_MINVOL1M），改指 get_platform_setting_options 与 config.REGIONS |
| PP-25 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/ppa-mining-experience.md \| Claude/skills/wq-brain-ra-pipeline/references/ppa-vs-ra.md | RA 侧副本早已缩为 39 行（独有实证 + 作废说法表）；本轮把其中对 dataset_health_check 的指向改成「已归档」，方法论只有 ppa-mining 一个家（测试：RA 侧 ≤ 60 行） |
| PP-26 | fixed | Claude/skills/wq-brain-ppa-mining/SKILL.md | §11 六条实测约束改成「症状 → 原因 → 处置」表；合法档位表按 PP-24 处理 |

## PW

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| PW-01 | fixed | Claude/skills/planning-with-files/SKILL.md \| Claude/skills/planning-with-files/scripts/check-complete.sh \| Claude/skills/INDEX.md | Stop 钩子占位符问题已由 3987274 修（内联、无 plan 静默、永远 exit 0）；本轮：PreToolUse 只挂 Write\|Edit 且只回显 20 行（不再每次 Bash 注入 30 行）；正文逐个钩子写明做什么 / 成本；声明 POSIX-only、无 bash 宿主可删 hooks 块；check-complete.sh 标注仅手动；INDEX 定义 hooks 白名单 + 逐条写明的审查规则。PowerShell 等价未实现（如实标注） |
| PW-02 | fixed | Claude/skills/planning-with-files/SKILL.md | 触发口径只剩一个（用户明确要求 / 跨会话 / 无现成状态存储且步数多）；WQ 流水线任务不用；写优先级（用户当次指令 > 领域协议 > 本 skill）；删「没有商量余地」；边界删掉不成立的「共用 $WQ_PY」 |
| PW-03 | fixed | Claude/skills/planning-with-files/SKILL.md | 区分确定性失败（同输入必再败→换方案，3 次协议）与暂时性失败（429 / 空体轮询 / PENDING / 异步补发→按各 skill 协议重试）；定义失败粒度；领域协议优先 |
| PW-04 | fixed | Claude/skills/planning-with-files/SKILL.md \| Claude/skills/INDEX.md | 规划文件固定建在仓库根（已 gitignore；子目录工作也写回仓库根），云端 / 只读会话用 scratchpad；INDEX 持久化铁律加豁免句（规划文件是过程笔记、不是战役产物，结果仍以 DB 为准） |
| PW-05 | fixed | Claude/skills/planning-with-files/SKILL.md | 区分确定性失败（同输入必再败→换方案，3 次协议）与暂时性失败（429 / 空体轮询 / PENDING / 异步补发→按各 skill 协议重试）；定义失败粒度；领域协议优先 |
| PW-06 | fixed | Claude/skills/planning-with-files/SKILL.md | 五问加 WQ 填好示例（RA 步 4 GEM 中断后恢复：五问答案各来自哪个文件 / 台账键，结果以台账为准） |
| PW-07 | fixed | Claude/skills/planning-with-files/references/wq-examples.md \| Claude/skills/planning-with-files/SKILL.md | 新增一次 RA 战役的 task_plan 示例（九步 = 九个 Phase，每阶段写台账检查点，保持 Status 行格式）；bash 脚本要求 Git Bash/WSL 已写明；check-complete 与模板文本耦合已写明。「脚本改 Python / 双实现」未做（维持 bash，如实标注） |
| PW-08 | fixed | Claude/skills/planning-with-files/SKILL.md | 反模式改为「会话内用 Task 工具、跨会话状态用文件 / DB」（互补而非互斥）；WQ 战役结果指向 DB 台账 |
| PW-09 | fixed | Claude/skills/planning-with-files/SKILL.md \| Claude/skills/INDEX.md | 边界加来源注记（外部开源 Manus 风格 skill 的中文化改编，version 为上游版本号）并如实标「上游地址与许可未在仓库内登记——待人补充」（仓库内无法查证）；INDEX 契约补 version / hooks 语义（user-invocable 已定义）。残留：需用户补充上游 URL 与许可 |
| PW-10 | fixed | Claude/skills/planning-with-files/SKILL.md | 三张 WQ 情景卡：一次 RA 战役的计划 / 压缩后恢复（五问 → 台账核对） / 用户说「直接改，别写计划」 |

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
| RA-76 | fixed | attic/toolkit_docs_20260929/README.md \| Claude/skills/wq-brain-campaign-toolkit/SKILL.md | toolkit 的 S2 合规文档同步为「仅提示、不阻断、无 --force」后，S2_COMPLIANCE_* 因 TR-32 整体归档（其「必须调用特征工程」要求已被撤回）；SKILL 子命令表 s2-mark 行写明「可选标记、缺记录只打印提示」 |
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
| RB-01 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | H1 之前的两个引用块删除（「权威性」元说明是 INDEX 的事；「定位声明」并入职责边界） |
| RB-02 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | judge 统一为「可选参考评审」，删「S5 唯一提交评审入口」 |
| RB-03 | fixed | src/wqb/robustness_record.py \| src/wqb/submit_verdict_core.py \| tools/submit_verdict.py \| tools/batch_submit_verdict.py \| world-quant-brain-mcp/tools_ops.py \| docs/ledger_keys.json \| tests/unit/test_submit_verdict_core.py \| Claude/skills/brain-alpha-robustness/SKILL.md | 「必经闸」有了代码落点：判定写台账 robustness_<alpha_id>（agent 经 upsert_ledger_key），submit_verdict 三入口读取——REJECT → BLOCKED，CONDITIONAL / 无记录只提示（fail-open 于缺失、fail-closed 于 REJECT）；键登记进目录并有单测 |
| RB-04 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md \| tools/forum_cache_builder.py \| tests/unit/test_forum_cache_builder_paths.py | Phase A 拆分：闸门只读 references/techniques.md，论坛刷新是独立任务；forum_cache_builder 缓存路径由写死的 ~/.qoder-cn/... 改为仓库内 skill 目录（WQ_ROBUSTNESS_SKILL_DIR 可覆盖）；手工刷新步骤删除，统一 --ensure / --plan |
| RB-05 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md \| Claude/skills/brain-alpha-robustness/references/techniques.md | 论坛新发现只作「提案」追加到 techniques.md 的 E 节，人审后才进 Phase C；删「以新规则为准」 |
| RB-06 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | 删「先经 MCP authenticate（邮箱 / 口令）」：认证由服务端完成，失败即停并请用户处理 |
| RB-07 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | B.0 三行表：Failed > 0 → REJECT 并按 RA 步 7 转 repair 后重新入闸（不是永久判死）；PENDING → 待复查，既不 REJECT 也不 PASS |
| RB-08 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | 体检包路径改为 tracking/mining/field_inspect_<region 小写>_<dataset>.json，给出 tools/field_inspect_gate.py 命令 |
| RB-09 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | 近窗制度写明来源（用户指令 2026-06-20 + 理由）与数值：用户 2Y 线 = PLATFORM_CHECK_LINES[low_2y_sharpe_min]；「每年为正」= sharpe > 0.3，平年 \|sharpe\| < 0.3 |
| RB-10 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | 判定表更正：子宇宙改引平台相对公式与 LOW_SUB_UNIVERSE_SHARPE 结果；算子数 REGULAR 降为软标记（PPA 才有硬上限 ≤ 8）；Margin 标注为论坛经验线（内部严线 10bp 另计）；经济可解释性给判例 |
| RB-11 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | Phase D：台账 robustness_<alpha_id> 是唯一被代码读取的落点；事件与 failure_memory 移出必做项（两模块全仓库无消费方，只写文件），需要时的入口指向源文件；description 软标记改走 submit-alpha 设属性 |
| RB-12 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | Phase E 编号重排为 1–5，无缺号 |
| RB-13 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | PPA 标签 / 颜色澄清：用于记账与识别，web UI 流程里是否仍被要求未复核；颜色是 PURPLE 不是 GREEN |
| RB-14 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | PHANTOM 不再写 alphas.status（非代码状态，且合并写入对 ACTIVE / SUBMITTED / DECOMMISSIONED 不回退）；改为核对报告 / key_findings 留痕，并指明归属 monitor / submit-alpha 而非稳健性闸 |
| RB-15 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | 「提交探测协议」（逐个提交读 prodCorr）删除并写明原因（提交即真实动作）；prod 一律 check_correlation + 决策表 D0-P |
| RB-16 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | 「可通过 skill 参数放宽」改为「放宽入口 = 用户明确指令，留痕于 soft_flags」；skill 无参数机制 |
| RB-17 | fixed | Claude/skills/brain-alpha-robustness/SKILL.md | 验证清单第 2 条的取数知识提为正文「prod 相关性怎么取」；Redis 更正为可选缓存（等死来自 30s×120 次阻塞轮询与账号级单并发）；给合规入口 campaign_intel.py prod-first |

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
| RE-01 | fixed | Claude/skills/brain-alpha-repair/references/repair-recipes.md \| Claude/skills/brain-alpha-repair/SKILL.md \| Claude/skills/INDEX.md | 配方逐项核销：4 项在别处有（字段体检文档 / 代码闸 / RA step5 §5.3 / news_sentiment_playbook）并登记去向，「5 轴旋转」「降相关 6 武器」原文不可恢复（git 内 optimization-v1 从未有）——撤回；INDEX 卖点更正；测试：声明已上移的术语必须能 grep 到 |
| RE-02 | fixed | Claude/skills/brain-alpha-repair/SKILL.md | description 退役触发词，改「配方索引与补充实证，非改进入口」；边界写明与 optimization-v1 的分工 |
| RE-03 | fixed | Claude/skills/brain-alpha-repair/SKILL.md | 写明 REGULAR / PPA 判定方法（PPA 通道 / 标签 CH_PPA / classifications 含 Power Pool Alpha）；failed-count 规则一处定义（failed-gates §1），此处只引用 |
| RE-04 | fixed | Claude/skills/brain-alpha-repair/SKILL.md | 选算子对照 known_ops / ghost_ops 与 ghost-audit，不再要求全量 get_operators |
| RE-05 | fixed | Claude/skills/brain-alpha-repair/references/repair-recipes.md \| Claude/skills/brain-alpha-repair/references/scenarios.md | turnover / coverage / correlation 三类各给可复制模板 + 适用条件 + 预期效果（方向）；库内无实测降幅，如实写「以小样本为准」；模板算子由测试对照 known_ops |
| RE-06 | fixed | Claude/skills/brain-alpha-repair/SKILL.md | news_sentiment_playbook 链接改仓库根形式（链接测试通过） |
| RE-07 | fixed | Claude/skills/brain-alpha-repair/references/repair-recipes.md | GLB emotion 实证拆成 事实表 / 4 条结论 / 适用范围（仅 GLB emotion 族）；结论的处置口径并入 D0-P，不另立学说 |
| RE-08 | fixed | Claude/skills/brain-alpha-repair/references/repair-recipes.md \| Claude/skills/brain-alpha-repair/SKILL.md | 探针改只读 check_correlation，家族首探 = 1 条（删「先 5 探针」与 POST 探测）；删「周额度」过期概念 |
| RE-09 | fixed | Claude/skills/wq-brain-ra-pipeline/references/regions/USA.md \| Claude/skills/brain-alpha-repair/SKILL.md | USA universe 约定迁入 regions/USA.md「步 7 注入」，记录落 wave_result.key_findings（不新造台账键） |
| RE-10 | fixed | Claude/skills/brain-alpha-repair/SKILL.md | 删 trajectory_steps / settings fingerprint 要求（无生产写入方 / 无生成者）；改用现存机制：expressions.fingerprint + settings_json |
| RE-11 | fixed | Claude/skills/brain-alpha-repair/SKILL.md | 验证清单改成可检项（expressions 表有 fingerprint / settings_json、failed-count 为零、算子在 known_ops 且 ghost-audit 0、GLB emotion 有平台 prod 读数） |
| RE-12 | fixed | Claude/skills/brain-alpha-repair/references/scenarios.md | 三张情景卡：降换手（Fitness 演算 0.74→≲17%）/ 覆盖不足 / 降相关（D0-P 判据 + 唯一例外） |

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
| SA-01 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md | description：触发词改「批量回测 / 发起回测」（去「批量提交 alpha」），并发与配额触发让给 wqb-concurrency / toolkit |
| SA-02 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md | 「唯一入口 / 唯一执行者」改入口选用表（workflow_batch_track / pipeline.py / batch_simulator.py 三个入口各管一类场景）；「调用 gate.py 闸」的引擎能力表删除（区分调用与实现）；settings.json 声明「本 skill 不写」 |
| SA-03 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md \| Claude/skills/brain-sim-alphas-in-batch-and-track/reference.md | 长任务规则分两路：MCP / 引擎路径（无 CSV，看 workflow_task_status + backtest_results，卡住 = WAIT_THRESHOLDS 的 60 / 360 分钟）与兼容 CLI 路径（CSV 进度，≥3 分钟无更新 + 进程不可达 = 本地进程死了）；注明两个判据判的是不同层，不是「相差 20 倍」的同一件事 |
| SA-04 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md \| Claude/skills/brain-sim-alphas-in-batch-and-track/README.md \| Claude/skills/brain-sim-alphas-in-batch-and-track/reference.md \| Claude/skills/brain-sim-alphas-in-batch-and-track/examples.md | 警告前置；示例数字换占位 <B> / <C>；裸 python 全换 $WQ_PY（README 的 $env:BRAIN_PASSWORD 示例一并删） |
| SA-05 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/build_wave.py \| Claude/skills/brain-sim-alphas-in-batch-and-track/scripts/batch_simulator.py | DEC-35：两处 --enhance-diversity 缺省改 never（增强会结构变异 / 替换算子 / 追加 novel，与 GEM 铁律冲突；阈值无实证），auto / always 显式 opt-in；测试守缺省 |
| SA-06 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md | 第 3 份「阶段 → 脚本 → 产物」映射表删除，改指 toolkit SKILL §1 分工表与「产物契约」（以 DB 为准） |
| SA-07 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md | 「禁止五数据集同时首探」删，改「填槽内容规则见 RA 步 4 / 步 6」（规则而非数字） |
| SA-08 | fixed | Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md \| Claude/skills/brain-sim-alphas-in-batch-and-track/README.md \| Claude/skills/brain-sim-alphas-in-batch-and-track/scripts/batch_simulator.py | 凭据名统一：标准名 CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD（与 MCP、toolkit 同名），旧别名 BRAIN_* 仍认；解析顺序写成脚本实际顺序（--config → env → 工作区 .env）；agent 不读 .env |

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
| SC-01 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md | 加对照表：MCP check_self_correlation（单个、即时）vs skill.py（批量、Excel）；description 触发词限定为「本地快筛 SELF / PPAC」 |
| SC-02 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md \| Claude/skills/brain-how-to-pass-alpha-test/SKILL.md | SELF 与 PROD 是两个池：本地 SELF>0.7 只推出 SELF 已必然 FAIL，推不出 PROD>0.7；Sharpe 10% 豁免路径写明本库未实现（单阈值 config 常量） |
| SC-03 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/skill.py \| Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md \| Claude/skills/brain-calculate-alpha-selfcorr-quick/reference.md | 脚本输出池最后刷新时间与池大小（终端 + Excel Meta sheet），本地 SELF 最大值 <0.7 自动打印盲区警告；强调符号只留 ★★ |
| SC-04 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md | 删「POST /submit 零成本实测」：全部通过时它就是真提交；写明 confirm_submit=False 只是本地放宽预检（不含平台 SELF/PROD 值）、平台 SELF 值目前只在提交响应里；同族连测改「本地排序 + 用户授权后提交」 |
| SC-05 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/submit-chain.md | GET 恒 404 / PENDING ≠ FAIL / 配额 403 与候选 403 的区分：整段迁指向 submit-alpha 的提交 API 行为表，本页只留链接；删改错史 |
| SC-06 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md \| Claude/skills/worldquant-submit-alpha/references/submit-chain.md | GET 恒 404 / PENDING ≠ FAIL / 配额 403 与候选 403 的区分：整段迁指向 submit-alpha 的提交 API 行为表，本页只留链接；删改错史 |
| SC-07 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/skill.py \| Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md \| Claude/skills/brain-calculate-alpha-selfcorr-quick/reference.md | 补「被测对象是谁」（UNSUBMITTED/IS_FAIL 候选按创建日期区间圈定）；命令统一 $WQ_PY 与仓库相对路径；凭据环境变量优先（--password 兼容但告警）；importlib.metadata 替代 pkg_resources、tqdm 缺失降级、非交互不 input()（此前在 MCP venv 里根本跑不起来） |
| SC-08 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md \| Claude/skills/wq-brain-alpha-optimization-v1/SKILL.md | 链尾改 explain(可选) → robustness → submit_verdict；optimization-v1 下游已回指 selfcorr-quick |
| SC-09 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/reference.md \| Claude/skills/brain-calculate-alpha-selfcorr-quick/scripts/skill.py | reference 重写为中文参数 / 产物 / 依赖表；产物目录固定（$WQ_SELFCORR_OUT_DIR / data/selfcorr_quick，gitignore）；-1.0 阈值 = 实际不过滤；check_status 含义（平台检查无 FAIL 且 long+short>100，非相关性结论） |
| SC-10 | fixed | Claude/skills/brain-calculate-alpha-selfcorr-quick/SKILL.md | 3 行判读决策表（本地 0.23 且同族近期提交→不采信；0.81→直接否决；0.40 且同族近期无提交→可信度中等） |

## SP

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| SP-01 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md | description 只留触发词 + 前置 + 范围；「运行环境」段（含对 SUPER 必 400 的 set_alpha_properties）移除；提交调用不再当固定写法 |
| SP-02 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md | 边界重写：上游 = sa_probe GO + 用户要组 SA（不再写不可达的 SUBMITTABLE）；组件不足 → 输出「区域 / 缺口 N 颗 / 需 prod<0.55 新血」交 ra-pipeline 步 1 起；下游只写 S6 监控一种说法 |
| SP-03 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md \| Claude/skills/wq-brain-superalpha/references/levers-and-evidence.md | 日期快照（USA 133 / EUR 7 …）删除，计数改为 sa_probe 实时命令；区域状态与瓶颈移入各区 profile；规则与证据分开 |
| SP-04 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md | 步 0 组件计数：region= 参数不生效的提醒上移到此；用 sa_probe（MCP / CLI），不手写 requests 翻页 |
| SP-05 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/regions/MEA.md \| Claude/skills/wq-brain-superalpha/references/cases.md | MEA 通道关闭移到 MEA profile 的「SuperAlpha 状态」；SKILL 不再把 MEA 列入组 SA 区域；案例 2 标「存量，不可复制」 |
| SP-06 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md \| world-quant-brain-mcp/tools_alpha.py \| world-quant-brain-mcp/tests/test_mcp_tools_unit.py | 失效脚本指针 logs/_fix_desc_sa4.py 删除；写明「走 CLI 描述自动写入；手工路径只传 selection_description + combo_description，不传 descriptions」；MCP set_alpha_properties 放行 SUPER 只传两段描述（此前缺省 descriptions 一律报错）并加单测 |
| SP-07 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md | 配额模型只留指针（quota-and-tower.md）；删除「硬闸 FAIL 属零成本探测」的泛化说法——SUPER 第一次通过的 POST 就是真提交 |
| SP-08 | needs-platform | ① 在 USA 与另一区各建一颗 SUPER，selection 去掉 (prod_correlation > 0) 子串，看模拟是否报错；② 同池同配方仅把 self_corr 窗口 500 换成 504，比较 SELF / PROD；无差异则统一为 504（标准窗口表） | 已按证据改写：SKILL 给出 super_build 的完整可执行 selection / combo 模板与各参数取值理由；「USA 必须出现 prod_correlation 子串」的来源与后果、以及 500（≈2 年取整，非标准窗口）都在文中标注为未复核 |
| SP-09 | fixed | Claude/skills/wq-brain-superalpha/references/levers-and-evidence.md | 改写为一张双闸决策表：症状 → 已实证有效 → 已实证无效 → 止损线（PROD 饱和 → 停止调参回 RA）；阅读顺序补丁删除，SUBINDUSTRY 降为「USA / GLB 已知最优」 |
| SP-10 | fixed | Claude/skills/wq-brain-superalpha/references/levers-and-evidence.md | V8/V9/V11/V12 变体代号给出定义；「恒」改「在 USA / KOR 观察到」；「prod < 0.6 硬门」零成本探针提到 SKILL 与 levers §3 显著位置 |
| SP-11 | needs-platform | 对同一环境里一颗 UNSUBMITTED 的 SUPER 与一颗 ACTIVE REGULAR 各 GET /alphas/{id}/submit，记录 HTTP 状态与 body；结果按 type 填进 submit-chain.md §3 的行为表 | 两份记录不一致（REGULAR 恒 404；SUPER 2026-09-11 观察为 200 但 SELF/PROD PENDING）且无法在离线环境复核；保守处置：SKILL 与 submit-chain 一律写「无论哪种 type 都不得用 GET /submit 放行，判据只有提交后的 status」 |
| SP-12 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md | 探针统一为 super_build.py probe；注明本地 SELF 对近期新提交孪生体的盲区（selfcorr-quick 实测 0.229 vs 0.8392），近期有同构 SA 时只当下限；run_selection 误区并入步 3「不做」 |
| SP-13 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md \| src/wqb/workflow/nodes/submit_alpha.py \| tests/unit/test_submit_alpha_super_guard.py \| tools/super_build.py \| src/wqb/workflow/nodes/superalpha.py \| tests/unit/test_workflow_nodes.py | 入口表列全（super_build select/status/probe/submit、workflow_superalpha、sa_probe）；submit_alpha 节点代码拒绝 SUPER confirm_submit（force 无效）；不可逆动作块；「预检 = 真提交」的说法删除；workflow_superalpha 的 selection/combo 转发到 super_build select |
| SP-14 | fixed | Claude/skills/wq-brain-superalpha/references/cases.md \| Claude/skills/wq-brain-superalpha/references/levers-and-evidence.md | 规则表（规则 / 证据 / 适用范围）与案例分离；四个案例各 5 行并标是否可复现；案例 3 / 4 标「提交时无 prod 闸，现行需 --allow-prod-above-07」；案例 1 标不可复现 |
| SP-15 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md | 顶部「判定优先级」：平台 result=PASS 且我方 prod<0.7 才提交，后者更严，二者不冲突；「只看 result」只出现一处 |
| SP-16 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md | 淘汰变体按 alpha_properties_spec：RETIRE_<YYYYMMDD> + hidden，不用 RED（RED = 已提交待退役），新前缀须先登记规范 |
| SP-17 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md \| tools/super_build.py \| tests/unit/test_super_build_prod_gate.py | 验证清单改为「需扫描的档位 + 已知最优（区域，日期）」；super_build select --neutralization 必填、无缺省（submit 的描述中性化取自 alpha 详情）；universe / delay 取自 config.REGIONS |
| SP-18 | fixed | Claude/skills/wq-brain-superalpha/SKILL.md | 删除指向不具备该能力的 alpha-expression-verifier；补 SUPER 专属检查名表（SUPER_SUBMISSION / NON_SELF_SUPER_ALPHA / LOW_TURNOVER 0.02 / IND 独有 LOW_ROBUST_UNIVERSE_SHARPE） |
| SP-19 | fixed | Claude/skills/wq-brain-superalpha/references/scenarios.md | 情景卡 SA-01 KOR/IND 从 0 到 SA、SA-02 组件恰好 10 颗（self_gate 0.65→0.70→0.85 与代价）、SA-03 近克隆被拒（同构淘汰法）、SA-04 PROD 饱和止损线 |

## TK

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| TK-01 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| tests/fixtures/skill_capabilities_baseline.json | description 由 702 字功能清单改为 173 字触发场景；闸数只留代码口径；allowed-tools 补 6 个只读 wqb-db 工具（理由已登记，待用户复核） |
| TK-02 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 连续空行与 ledging 笔误清理 |
| TK-03 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 删「唯一正式写入方」；新增 §3 写入矩阵（表 × 校验实现 × 入口 × 适用）：wave_results / registry_empirical / ledger_kv / submit_ready 各写清 |
| TK-04 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | dataset-experience 进 §6 子命令表 |
| TK-05 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 删「唯一权威实现」；§1 加 toolkit vs tools/ 分工表（阶段 → toolkit → tools/），补全 wave_gate / campaign_intel / harvest_multisim / step_funnel 等 |
| TK-06 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | §7「重发安全与异步恢复」独立成节，写成三步恢复顺序（workflow_task_status → 按 multisim_id 查 backtest_results → 两处皆空且任务已死才重发）+ 情景 TK-A |
| TK-07 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| attic/toolkit_docs_20260929/README.md | 删除线行与括号撤回全部清理；§6 只留存在的脚本，已归档清单合成一段并指向 attic 三处；测试逐个核对 scripts/ 里确无这些文件、SKILL 里只在「已归档」行出现 |
| TK-08 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 「使用率分级」整节删除（按 2026-08-31 静态引用扫描的分级与实际流程不符），换成「按阶段选脚本」表 |
| TK-09 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/references/selection-plan.md | 选波数量与状态契约 10 行拷贝删除，只在 selection-plan.md 维护（含 expected-count / source-wave / selection-state / 受保护状态定义） |
| TK-10 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 异步恢复与救援池来源排除拆开：前者进 §7 步骤，后者一段指向 get_salvage_pool / RA 步 7，并写明「数据集不同只证明来源不同」 |
| TK-11 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 「唯一运行时调用方」改「主要调用方」并列出 workflow_campaign / workflow_batch_track 节点 |
| TK-12 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| Claude/skills/INDEX.md | 700 字一行改成「产物契约」表（入口 → DB 落点）；review_wave 写 review_<tag>、workflow S4 节点另写 s4_walls_…，RA 产物表两个键都写明（RA SKILL 的 S4 行同步） |
| TK-13 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/campaign-dir-contract.md | 决策记录换成事实陈述（probe_scoring_v2 刻意缺的原因保留为 schema 事实）；指针去重；新增「缺目录 / 缺 thresholds 时的行为」表（TWN / AMR 情形） |
| TK-14 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 凭据链列出脚本实际顺序（CREDENTIALS_* → WQ_* → BRAIN_CREDENTIALS / ~/.brain_credentials → MCP_CONFIG_FILE），并加红线「agent 不得读取、打印这些文件或 .env」 |
| TK-15 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 开波区域闸 560 字改成 2 行小表（入口 × 缺省 × 命中结果），日期唯一事实源 region_gates.WARN_SUNSET |
| TK-16 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 快速开始改 PowerShell（$WQ_PY / $TK）；标明门禁走 tools/wave_gate.py（含体检硬门 / 闸 SEM / PF / 2b）；补 GEM 一步说明；--submit 旁注「发起回测，不是提交 alpha」，--max-rounds 有说明 |
| TK-17 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 子命令表补全 assemble-priors / diversity-extract / s2-mark / dataset-experience 与 harvest.py / check_ledger_sync.py / neutralization_sweep.py；闸数统一「8 闸 + 可选闸0」；细节文档改链接；campaign.py 文档串同步（8 闸、去重复行、修 \u003e 乱码） |
| TK-18 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| docs/ledger_keys.json | saturated_datasets 的写入口 = campaign_intel.py mark-saturated（DEC-13，已落地）；seat_model 登记 orphan 并在文档写明；饱和相关机制只谈函数名与开关 |
| TK-19 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/references/probe-scoring-v2.md | P0/P2/P3/P5/P6 审计工单号全部改用功能名；probe-scoring 里的「探针 P1–P8」专指模板一组 |
| TK-20 | declined |  | 范本（🟢）：「score=信号强度榜、pyramid_view=点塔战略榜，勿相加或混排」——原样保留在 §8 |
| TK-21 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | §6.y「接线修复落地（审计①③⑥⑦）」变更记录删除（改进 CHANGELOG）；settings prior / region_kb 刷新 / S2-COMPLIANCE 降级 / rn 墙 / 停止规则各在对应章节留一句现行事实，键契约见 campaign-dir-contract |
| TK-22 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | 闸 7 明写「目前只有 WARN，没有任何代码读取 profile 的 longcount_verdict / cw_gate」，小宇宙区域按 FAIL 处理由 agent 依 profile 自行执行；删无出处的「约 17% 死路」；同时更正闸 8 口径（引用 EVENT 字段即拦，平台无 ts_event_*） |
| TK-23 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | fail-fast 指向 docs/experience/fail_fast_rules.md（七信号的量化口径与 FAIL_FAST_THRESHOLDS 一一对应），链接改仓库根形式（skill 同步到别的宿主后不断）；无「priority 65」魔法数 |
| TK-24 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 标题改「开关与入口」并用绝对日期；prod-first 的 top-k 差异写明（pipeline 透传缺省 2，campaign_intel 自身缺省 3） |
| TK-25 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 二分排障合并成一份（§11，保留场景 → 步骤 → 判据的写法，JPN 例）；同步目标统一三处（profile + platform_constraints + pipeline_pregate）；开关表去重；节号重排 |
| TK-26 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | §8 重复项（record_*.py、第二权威、单轨）合并进 §13 纪律；429 退避归 poll-and-quota；旧文件布局（candidates / results / reviews）删 |
| TK-27 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/references/poll-and-quota.md \| Claude/skills/brain-sim-alphas-in-batch-and-track/SKILL.md \| Claude/skills/wqb-concurrency/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py | DEC-36：术语固定 dispatch（发起回测）vs submit（提交 alpha）；核对代码——配额闸缺省关闭（enabled=False），--force 越过的是 universe 判死规则与（区域开了配额闸时的）配额闸，不提交 alpha、不耗额度；help、文档、测试三处同步 |
| TK-28 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | RA 步 4 硬约束的第三份拷贝（含被禁的加权混合范例）整段删除，改一句「见 ra-pipeline 步 4 / 步 6，参数见 config.MINING」 |
| TK-29 | fixed | AGENTS.md \| Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 开发者流程（workflow 节点四处同步 + audit_node_registration）已在 AGENTS.md「变更影响面」，toolkit 只留一行指针 |
| TK-30 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/step9-writeback.md | 回写路径统一为「MCP 可用时 MCP、无 MCP / 批量用 CLI，同一契约」，旧的 results/wave63_results.json 示例改占位 |
| TK-31 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 范本（🟢）：「WAVE_LEDGER.md 是从数据库生成的快照、勿手改」保留为全库口径（RA D8 已一致） |
| TK-32 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md \| wqb_db_mcp.py \| docs/ledger_keys.json \| Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/ledger.py | DEC-33：提交队列唯一事实源 = SQL 表 submit_ready；MCP get_submit_ready 改读表（可按 status 过滤）；ledger 键降 legacy 审计副本，ledger submit-ready 每次打印提示 |
| TK-33 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 15 个 MCP 查询示例删除（属 INDEX 工具表） |
| TK-34 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 「工具化纪律」前移并扩成 §1 的 toolkit vs tools/ 分工表，旧称「提交层判定（403 盲区）」换成 submit_verdict 唯一权威 |
| TK-35 | fixed | Claude/skills/wq-brain-campaign-toolkit/SKILL.md | 文末「2026-09-19 新增」并入 §11 / §12，MCP 工具表故障史（装饰器错挂，N31）删除 |

## TR

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| TR-01 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md \| tests/unit/test_docs_consistency.py | 不再自称「唯一基准」：编号唯一注册表 = gate.py::GATE_REGISTRY（INDEX 表由它生成），wave_gate 层的闸指向 INDEX「闸与逃生口总表」；相应旧测试断言改指 GATE_REGISTRY |
| TR-02 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | 闸 5 列全平台级 8 条（含 4 条结构判定 + 3 条正则 + spread_cross_dataset），每条写「拦什么 / 放行形态」，合规替代三选一；测试逐条核对 platform_constraints |
| TR-03 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | 闸 6 契约过期改写成与代码一致：FAIL-CLOSED（阻断）并自动续约；逃生口留痕键名指向 INDEX 总表 |
| TR-04 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | diversity_slots.py（已归档）指引删除，改「契约就在台账里，照它写」 |
| TR-05 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | 注入算子三种入场方式（事件门控 / 分组 / 单信号几何）与 optimization-v1 的辅助腿入场形态表对齐；group 字段须为该区合法字段（JPN sector 非法，闸 2b）；删「慢腿×快腿」叙事 |
| TR-06 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | build_wave 规则重写为 DB 口径（history_expressions 去重）；linear_mix 澄清为「含 add( / multiply( 表达式的占比上限」，不是配给目标、也不许可拼腿（闸 5 拦）；多样性增强缺省 never |
| TR-07 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/diversity-extract.md \| attic/toolkit_docs_20260929/README.md | diversity_extract 的 5 份文档合并成一页（43 行）；根目录三份归档 |
| TR-08 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | 墙枚举补全：*_UNKNOWN、NO_DATA、CW、RN_EXPOSURE、RA_OTHER，近闸池排除类 ROBUST_STRUCTURAL / RN_EXPOSURE；missing≠fail 保留；prod 类墙指向 prod-first 与 D0-P |
| TR-09 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py | verifier 查找顺序不改（主目录已安装副本先于仓库副本是有意的：那是 agent 实际加载位），改为每个进程 stderr 打印一行所用路径，让验证行为可复现；SYNTAX_UNKNOWN 显式报警保留 |
| TR-10 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/gate-rules.md | 分「agent 需知」与「维护者需知」两部分；闸 3 的 [EVENT] 标签写明是历史遗留（指 VECTOR，与闸 8 无关） |
| TR-11 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/poll-and-quota.md | N=min(5,…) 改 7（代码 n_slots = min(7, n_total)），且该段整体改写为现行七槽 |
| TR-12 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/poll-and-quota.md | 「单批在飞（已废弃）」的删除线原文与历史实证移除，只留现行七槽 + 一句「旧规则已废止」 |
| TR-13 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/poll-and-quota.md | 配额三通道统一（REGULAR 4 + SUPER 1 + PPA 1）；读额度用 pipeline.py quota，勿靠 POST；写明 quota 的 used 数 OS 池当日全部提交、不区分通道（保守上界），精确分通道读数只在提交响应里（needs-platform：需在有账号环境核对）；旧「activities 口径」说法删除（代码只用 OS alphas） |
| TR-14 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/poll-and-quota.md | 「凭证与登录」改「凭证与缓存」，metrics_cache 读穿缓存另起一段 |
| TR-15 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/ledger-schema.md \| tests/unit/test_ledger_key_catalog.py \| Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/ledger.py | wave<N>_verdict / ledger set-verdict 标废止（wave_results.verdict 唯一真相源），CLI 每次打印废止提示；键目录测试的「教废止键」棘轮基线删掉这一项（只减不增） |
| TR-16 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/ledger-schema.md \| docs/ledger_keys.json | submit_ready 的两个家写清：SQL 表 = 队列，ledger 键 = legacy 审计副本 |
| TR-17 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/ledger-schema.md \| docs/ledger_keys.json | 键命名约定表删除，改指 docs/ledger_keys.json（75 键 × 写入方 / 读取方 / 缺失行为 / 刷新，且有「被读的键必有写入方」测试）；只列家族前缀与已废止键 |
| TR-18 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/ledger-schema.md | 原语分「SQLite（现行，单事务）/ JSON（已弃：.bak、atomic_save、双遍重放）」两段 |
| TR-19 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/ledger-schema.md | CLI 标题改通顺，并标出 set 是整值覆盖（共享键用 MCP merge） |
| TR-20 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/campaign-dir-contract.md | 目录布局逐项标 [必需] / [可选] / [历史]（candidates / reviews / results / wave*_exprs.json / ranking / catalog 文件为历史） |
| TR-21 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/campaign-dir-contract.md | 示例 JSON 去掉行内 # 注释（测试解析 json 代码块）；示例中性化改 STATISTICAL 并注明非推荐值、受 D5 约束 |
| TR-22 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/campaign-dir-contract.md | hard_gates 的权威改指 config.py::GATES（GATES_INTERNAL / GATES_PLATFORM） |
| TR-23 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/campaign-dir-contract.md | diversity 行改「signal_floor 与 stop_rules 都有消费方」，并补 stop_rules 全部 8 个键与规则 A / B 语义 |
| TR-24 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/campaign-dir-contract.md | 「上表」指代改明确；区域数量改指 INDEX §区域清单（不再写 11 / 13 / 14 三种数） |
| TR-25 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/selection-plan.md \| Claude/skills/wq-brain-campaign-toolkit/references/post-wave-reading.md \| docs/ledger_keys.json | 拆成「选波」与「波后解读」两篇；定义资格线 / 增强资格 / 受保护状态 / UNITS 警告；research_leads_w<W> 在解读篇给 JSON 样例（键目录 doc 指向随之更新）；纠错复验单模板 + 缺陷白名单（单位警告 / 字段映射 / 对照不匹配，「Sharpe 弱」不算缺陷）；中英文补空格 |
| TR-26 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/probe-scoring-v2.md | tier 分位改代码缺省 P60 / P30、coverage_hard_min 缺省 0.7（旧文 P80 / P55 / 0.65 从未存在于代码），测试从 score_datasets 源码抽缺省值对文档 |
| TR-27 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/probe-scoring-v2.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/score_datasets.py | DEC-38：三灯 action 的拼腿推荐在代码与文档同时改掉（绿灯 → 单信号结构变体；带 CW → 事件门控 / group / 同源价差；黄灯 → 镜像腿与同源价差），测试断言代码里不再出现「跨Category rank加法 / 两两融合」 |
| TR-28 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/probe-scoring-v2.md \| Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | 改「工具不自动执行 calibrate；SOP 要求显式执行」；RA 步 2 的校准段同步加「不要 apply、先查 ac 来源」并指向本处的处置表 |
| TR-29 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/probe-scoring-v2.md \| Claude/skills/wq-brain-campaign-toolkit/config/platform_constraints.json | P 编号只在「探针 P1–P8」这一组（审计工单号已去）；三灯阈值只写引用（参数在 thresholds.probe_scoring_v2 / score_v2），并写明与内部严线 / RN_EXPOSURE 不是同一套；探针 P6 窗口 60 → 66（无实测依据的窗口） |
| TR-30 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/probe-scoring-v2.md \| Claude/skills/wq-brain-ra-pipeline/references/step2-s0.md | 范本（🟢）「审 dry-run 看两处异常 → 怎么办」保留为一张处置表；RA 步 2 校准段改为引用本处并补「怎么办」 |
| TR-31 | fixed | attic/toolkit_docs_20260929/README.md \| Claude/skills/wq-brain-campaign-toolkit/SKILL.md | enhancement-v2.md 整篇移入 attic（其描述的 9 个脚本早已归档，含被禁的混合权重与与 RA 冲突的判死纪律）；仅保留一句原则「预算只花在本地筛过的精英上」 |
| TR-32 | fixed | attic/toolkit_docs_20260929/README.md \| Claude/skills/wq-brain-campaign-toolkit/SKILL.md | S2_COMPLIANCE_* 移入 attic（三条要求均已撤回）；s2-mark 仍是可选标记 |
| TR-33 | fixed | Claude/skills/wq-brain-campaign-toolkit/references/diversity-extract.md \| attic/toolkit_docs_20260929/README.md | DIVERSITY_EXTRACT 三份（546 行）归档，合并为 references/diversity-extract.md（43 行）；L3 窗口收敛为 5 / 22 / 66 / 252（代码同步） |

## WC

| ID | 状态 | 位置 / 依据 | 说明 |
|---|---|---|---|
| WC-01 | fixed | Claude/skills/wqb-concurrency/SKILL.md | description 只写触发场景（122 字）；删「每次挖掘必须执行」「下一波强制以台账为输入」；「提交成功数」改「接受数」 |
| WC-02 | fixed | Claude/skills/wqb-concurrency/SKILL.md | 边界明写「不管台账、复盘与选波」；§8 只留并发部分，台账同步门 / 写波结论 / 台账驱动选波 / 每 10 波评估全部撤回给 RA 步 1 / 步 9 |
| WC-03 | fixed | Claude/skills/wqb-concurrency/SKILL.md \| src/wqb/config.py | 「≤6」与「≤7」两个包络实为两个量：七槽 7（config.CONCURRENCY.slots，代码按 7 同提）与保守档 6 / 批间 ≥45 s（safe_instant_submits / min_batch_interval_sec，当前无代码读取）；SOP 加「批间间隔」规则；测试钉住这两个常量无读取方，一旦接线就逼着改文档 |
| WC-04 | fixed | Claude/skills/wqb-concurrency/SKILL.md | §2 / §3 标「给引擎维护者」，agent 不手写 runner；示例数字改 C=7、引用 config；顶部加读者分层说明 |
| WC-05 | fixed | Claude/skills/wqb-concurrency/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/references/poll-and-quota.md | 退避口径合一：toolkit 传输层 5 s ×2 最多 5 次、MCP 内建 Retry-After，手写 runner 的口径只作原理；429 时降并发用 WQB_GLOBAL_SLOTS（RA 步 6 与本 skill 同一说法） |
| WC-06 | fixed | Claude/skills/wqb-concurrency/SKILL.md | §6 凭据改「agent 不读取 .env」，给脚本作者的 load_dotenv 提示单列 |
| WC-07 | fixed | Claude/skills/wqb-concurrency/SKILL.md | SOP 步 3 改现行工具：harvest_multisim_alphas 一键收批（18 次调用压成 2 次）+ harvest_multisim_results 入库，lookINTO_SimError_message 只用于定位批内 ERROR |
| WC-08 | fixed | Claude/skills/wqb-concurrency/SKILL.md | validate_fields 分场景：验活探针 true（RA 步 3），正式批 false（避免预检超时） |
| WC-09 | fixed | Claude/skills/wqb-concurrency/SKILL.md \| Claude/skills/wq-brain-ra-pipeline/references/decision-table.md | 台账同步门如实定性：check_ledger_sync 两份都是文件时代校验，现行同步门 = 开波三道区域闸 + step_funnel（RA D8 已一致）；「创建批次文件时登记批次表」删 |
| WC-10 | fixed | Claude/skills/wqb-concurrency/SKILL.md | 步 4 的 600 字段落随台账职责一并移出，SOP 改 5 条有序清单 |
| WC-11 | fixed | Claude/skills/wqb-concurrency/SKILL.md \| Claude/skills/wq-brain-campaign-toolkit/references/poll-and-quota.md \| Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py | DEC-36：如实说明——配额闸缺省关闭，回测发起不受提交额度约束（仅区域 submit_quota.enabled=true 才有该闸）；测试钉住缺省 |
| WC-12 | fixed | Claude/skills/wqb-concurrency/SKILL.md | 范本（🟢）「测 C 的 4 步 + 易踩坑 + 反面知识」原样保留在 §1；并补两张情景卡（全 429 / 我该开几个线程） |
