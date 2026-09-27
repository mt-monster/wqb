# RA 九步流水线逐阶段展开 · 价值评估 · Dry-Run（沙箱 → P0 修复 → 真实环境复跑 → P1 修复 → 第三轮复跑 → P1 第二批修复 → 第四轮复跑，2026-09-27）

> **对象**：`Claude/skills/wq-brain-ra-pipeline/SKILL.md`（v2.2，last_verified 2026-09-19）定义的唯一挖掘编排 SOP（S-PRE→S6 九步），以及它调用的 workflow 节点、`tools/`、toolkit 脚本与 MCP 函数。
> **代码基线**：`c393bca`（2026-09-25）。
> **前序审计**：`output_report/ra_pipeline_stage_audit_20260916.md`（v2）、`…_v3.md`、`ra_pipeline_remediation_plan_20260917.md`。本报告**不是增量补丁**：九步按"输入 / 处理 / 输出 / 价值"重新完整展开，并对前序结论逐条做代码级复核。
> **附件**（同名目录 `reports/ra_pipeline_stage_review_20260927/`）：`dryrun_transcript.txt`（完整演练实录）、`reproduce.sh` + `run_dryrun.py` / `seed_db.py` / `sbx_guard.py`（一条命令复现）。
> **第二轮（同日更新，见 §14，首读建议从 §14.0 开始）**：按审阅意见先修两个 P0（N1 / N2），再在**真实环境**复跑九步。真实环境 = 真实仓库工作树 + 两个 MCP server 经 stdio 真实启动 + `tracking/KOR` 真实历史经 MCP 导入，并用修复前的原始代码做对照。复跑暴露了 P0-2 的两处残缺（N16 / N17，已一并修复），另记新发现 N18–N27。附件 `realenv/`：`run_realenv.py`、`reproduce_realenv.sh`、`realenv_transcript_p0.txt`（第二轮实录）。
> **第三轮（同日更新，见 §14.8）**：按审阅意见修复四个 P1（R18–R21），用修复后的代码在真实环境把九步完整再跑一遍，每一步打印【阶段小结】（输入 / 处理 / 输出变化 / 价值判定，数字取自本次运行）。首跑又暴露 R19 / R21 的两处残缺（N28 / N29，已一并修复）。实录 `realenv/realenv_transcript_r18_r21.txt`。
> **第四轮（同日更新，见 §14.9）**：按审阅意见修 P1 第二批 R22 / R5 / R12 / R4 / R3，第四轮真实环境复跑，末尾验证清单 8 ✅ + 1 ➖（R4：真实数据无触发样本，靠单测）。验证中顺手修了两处"本批修复让测试走得更远才暴露"的问题，新记 N30（P1，未修）。随后按审阅意见定下 CLI 开波闸灰度截止日：2026-10-11 及以前 warn，2026-10-12 起缺省 enforce（§14.9.7）。实录 `realenv/realenv_transcript.txt`。

**证据等级**（全文每条判断都标注来源，避免"推测记账"）：

| 标记 | 含义 |
|---|---|
| 〔码〕 | 读源码核实（给出 `文件:行`） |
| 〔沙〕 | 在隔离沙箱里实际执行复现（见 §12 与实录） |
| 〔真〕 | 第二轮起：真实环境经 MCP 协议实际执行（见 §14 与 `realenv/` 下各轮实录） |
| 〔史〕 | 引自 SKILL.md / 前序审计记录的生产实证数字——**本环境无生产库，无法复核**，按原文转述并注明出处 |
| 〔推〕 | 依赖平台网络的步骤，按源码静态推演 |

**本环境限制（第一轮）**：云端容器内没有 `data/wqb.db` 生产库；`.mcp.json` 里的两个 MCP 服务（`wq-brain-http` / `wqb-db`）指向 Windows 路径，本会话无法连通。因此 dry-run 在 `git archive HEAD` 副本 + **合成种子库**（region=KOR，虚构数据集 `syn_analyst`）上进行，封网并拦截子进程。沙箱里出现的所有数字都是夹具数字，**不代表生产状况**；它回答的是"这条代码路径在给定输入下会做什么"。

---

## 0. 一页结论

### 0.1 九步总览

| 步 | 阶段 | SOP 主入口 | 核心价值（保留理由） | 判定 | 本轮关键发现 |
|---|---|---|---|---|---|
| 1 | S-PRE 查表 | profile + `get_mining_yield` + 库存盘点 | 先清库存再新挖；conversion/yield 区分"管道问题 vs 标的问题" | **保留深化** | `inventory_scan` 节点未入 SOP；`latest_wave` 对字符串波号排序失效 |
| 2 | S0 体检选集 | `workflow_campaign(S0)` + `s0-select` | 平台真实点塔 × 严格产出率 × 判死；座位可达性 | **保留深化** | dry-run 会写 `settings.json`；节点缓存是死代码 |
| 3 | S1 字段 | `workflow_campaign(S1)` → typed catalog | 类型/覆盖元数据是闸 2/3/8 与 catalog 前置闸的数据源 | **保留** | **Python 3.11 下 S1 恒判"缺 dataset"**；users 分级无工具实现 |
| 4 | S2 生成 | assemble-priors → `workflow_gem` → build_wave | 概念优先 + 生成侧预闸 + 骨架配给 | **保留深化** | **P0：节点路径不写 priors 快照，GEM 只读快照 → S6→S2 回流断开**（✅ 已修，§14.1；第二轮新增的 N18 截断问题 ✅ 已修，§14.8） |
| 5 | S2→S3 门禁 | ghost-audit → `wave_gate` | 零配额拦截整批连坐（语法/元数/字段/VECTOR/毒模式/体检） | **保留，精简展示层** | `[opcat]`/质量预估打印 FAIL 却不参与判定；FAIL 候选仍记 `gated`（✅ 已修，§14.8）；体检规则 1/5 耦合 |
| 5b | prod-first 探针 | `campaign_intel prod-first` | 把 prod 墙判断前移到扩批之前 | **保留** | 网络依赖，未演练 |
| 6 | S3 七槽回测 | `workflow_batch_track` → pipeline.py | 七槽填槽、设置先验、连坐隔离、argv/存活握手 | **保留** | SOP 指定入口 `batch_track` **不跑**停止/天花板/积压三闸（✅ 已修，§14.9） |
| 7 | S4 诊断 | `workflow_campaign(S4)` → review_wave | RN_EXPOSURE / ROBUST_STRUCTURAL 墙、预筛、salvage | **保留深化** | RN_EXPOSURE 行仍进 near/salvage 池（✅ 已修，§14.9；仓库真实数据里无触发样本） |
| 8 | S4→S5 判定 | Failed-count → `submit_verdict` → 用户确认 | 否决权威 + 人工确认门 | **保留，修正定位** | `src/wqb/config.py` 有一份与生产口径相反的 Failed-count 实现（✅ 已收敛为唯一实现，§14.9）；`submit_verdict` 对新候选只能给 UNVERIFIABLE |
| 9 | S6 复盘 | `step_funnel` + `upsert_wave_result` + pyramid | verdict→停止规则 B、region_kb 刷新、判死封存 | **保留** | **P0：只补写 key_findings 会把 verdict 清成 NULL → 停止规则 B 静默失效（全链复现）**（✅ 已修，§14.1；第二轮新增 N20 ✅ 已修，§14.8；N22 ✅ 已修，§14.9；第四轮新记 N30：收批级联绕过写入契约、波号被截成数字，§14.9） |

**总评**：九步骨架本身没有多余的"步"——每一步都承载着至少一个有实证的判别机制。本轮发现的问题集中在**步与步之间的接缝**（写入口契约、快照/文件双载体、节点 vs CLI 两条执行路径语义不一）和**展示层噪声**，而不是"缺步骤"或"步骤无用"。真正该**去除**的是少数已被证明无效或误导的子项（死代码缓存、分叉实现、只打印不判定的伪硬闸），真正该**深化**的是把 SOP 文字规则变成机器可执行的约束（users 分级、区域闸 enforce、verdict 写入契约）。

### 0.2 本轮新发现（按严重度；均为 09-16/17 三份审计未记录的问题；N16–N27 为第二轮真实环境新增，详见 §14.5；N28–N29 为第三轮新增，详见 §14.8；N30 为第四轮新增，详见 §14.9）

| # | 级别 | 发现 | 证据 |
|---|---|---|---|
| N1 | **P0** ✅已修（§14.1） | `mcp__wqb-db__upsert_wave_result` 的 UPDATE 分支对未传字段写 NULL（非合并）。按步 9 指引"把 pyramid 的 key_findings 行拷进 upsert_wave_result"只传 key_findings 时，**已有 verdict 被清空** → 规则 B 遇 UNKNOWN 只告警不拦截 → 下一波被放行。该入口还接受 `status=closed` + 空 verdict（toolkit 的 `WaveResultsStore.upsert` 会拒绝，两个写入口契约不一致） | 〔码〕`wqb_db_mcp.py:820-899`、`_lib/wave_results.py:82-85`；〔沙〕实录 步 9 |
| N2 | **P0** ✅已修（§14.1） | `workflow_campaign(subcommand="assemble-priors")` 拼出的命令**不带 `--snapshot-ledger`**，只重写 priors 文件；GEM 默认 `--priors-from-db` **只读 DB 快照** `priors_snapshot_<r>`（缺快照 fail-closed）。SOP 宣称的"S6 回写后下一次 S2 先验自动变新"在指定路径上不成立：新区直接失败，老区静默沿用旧快照 | 〔码〕`campaign.py:444-450`、`assemble_priors.py:474-507`、`headless_runner/run.py:346-371`、SKILL.md:269/281-286；〔沙〕实录 步 4 (b)(c) |
| N3 | P1 ✅已修（§14.9） | Failed-count 资格门有三份实现：`mcp_core.py`（17 项 + WITH_RATIO，非 PASS/PENDING 计失败，**正确**）、`build_gate_prior_from_inventory.py`（同口径副本）、`src/wqb/config.py::compute_webdata_failed_counts`（8 项、只数 FAIL、含不存在的 `HIGH_DRAWDOWN/LOW_SELFCORR/LOW_PNL`）。第三份仅被单测引用，但它位于 AGENTS.md 规定的"唯一事实源"模块，是照规范 `from wqb.config import …` 就会踩中的陷阱。同一组 checks：生产口径 `failed_ra=3`，config 口径 `0` | 〔码〕`config.py:351-383` vs `mcp_core.py:78-95,153-156`；〔沙〕实录 步 8 |
| N4 | P1 ✅已修（§14.9；真实数据无触发样本） | review_wave 的 near 池只排除 `ROBUST_STRUCTURAL`，**不排除 `RN_EXPOSURE`** → 被判"就是暴露本身、禁止调参"的行仍进 near_pool / salvage_pool，可被 Mode A/B 取用 | 〔码〕`review_wave.py:203-215, 297-317`；〔沙〕RN=-0.2 行 `walls=['RN_EXPOSURE'] near=True` |
| N5 | P1 ✅已修（§14.9；CLI 侧灰度 2026-10-11 截止、次日起缺省 enforce，§14.9.7） | 三道零配额开波闸（signal_floor / stop_rules / backlog）只在 `workflow_campaign(stage=S2/S3)` 里 enforce；SOP 步 6 指定的 `workflow_batch_track` 一道都不跑；CLI 入口（build_wave / wave_gate）默认 warn。"发批直接走步 5"的快捷入口全程无 enforce | 〔码〕`batch_track.py:66-225`、`region_gates.py:18-21`；〔沙〕batch_track 干跑 steps 无闸，campaign S3 干跑有三闸 |
| N6 | P1 | `tools/wave_gate.py` 的若干"闸"只打印不判定：`[opcat]` 自称硬闸、打印"FAIL：缺 Group"，质量预估对每条打印 `HARD_REJECT`，但二者都不进 `all_pass` —— 最终 `=> PASS`、exit 0 | 〔码〕`wave_gate.py:749-822, 970-993`；〔沙〕实录 步 5 ⑦ |
| N7 | P1 ✅已修（§14.8） | `--exprs-file` 候选在门禁**之前**以 `status='gated'` 入库，门禁 FAIL 后不回写 → `gated` 同时表示"送过闸"与"过了闸"，积压闸与漏斗把 FAIL 候选计为未消费积压 | 〔码〕`wave_gate.py:572-588`；〔沙〕w5/w6/w7 FAIL 后 19 条仍为 `gated` |
| N8 | P1 | `submit_verdict` 对处女提交（新候选的常态，提交层 404）只能返回 `UNVERIFIABLE`；SOP"是否提交的最终判定以本步为准"对新候选无法给出放行结论——它是**否决权威**，放行依据实际是模拟层 checks + 平台 prod 相关性 + 用户确认 | 〔码〕`tools_ops.py:236-251`、`tools/submit_verdict.py:125-130`；〔推〕判定表 |
| N9 | P2 | `campaign` 节点 S1 必填校验把 `locals().get(p)` 写在列表推导式里：Python 3.11 推导式有独立作用域 → **传了 dataset 也判缺失**。`pyproject.toml` 声明 `>=3.11`；仓库自带 `test_campaign_stage_route_matrix` 在 3.11 下即红（3.12 起因 PEP 709 内联推导式才"碰巧"可用） | 〔码〕`campaign.py:161-170`；〔沙〕实录 步 3 + pytest 复现 |
| N10 | P2 | dry-run 契约（AGENTS.md:90"不 subprocess、不写库、不建目录"）两处破口：`campaign` 节点在 dry-run 前调用 `_ensure_campaign_config`，缺 `settings.json` 时写入一份硬编码默认值（universe=TOP3000/decay=4/SUBINDUSTRY）；`gem` 节点在 dry-run 返回前 `makedirs(logs/_async_tasks)` | 〔码〕`campaign.py:179,1410-1528`、`gem.py:327-331`；〔沙〕AMR 干跑生成 `settings.json`；gem 干跑 FS +2 |
| N11 | P2 | 战役库路径至少 7 套解析口径，其中 3 处硬编码 `D:\coding\traeCN_project\wqb`；`WorkflowExecutor` 用相对路径 `data/wqb.db`，换 cwd 即在当前目录新建空库 | 〔码〕见 §11.1；〔沙〕换 cwd 后生成 `elsewhere/data/wqb.db` |
| N12 | P2 ✅已修（§14.9） | `tools/wave_gate.py` 的 toolkit/validator 解析只认 `WQ_*_DIR`、`~/.qoder-cn`、`~/.cursor`、`~/.workbuddy`，**没有** INDEX.md 所写的 `~/.claude`、`~/.codex` 与仓库兜底；验证器硬依赖 `ply` 但任何 requirements 都未声明，缺失时以 exit 1（=表达式 FAIL）而非 exit 2（=环境 ERROR）退出 | 〔码〕`wave_gate.py:40-51,148,567`、`INDEX.md:27-29`；〔沙〕实录 步 5 ③④a |
| N13 | P2 | 19 个 workflow 节点中 9 个（inventory_scan / field_understanding / gem_wave / unified_gate / auto_harvest / auto_review / auto_pyramid / modeb_improve / structural_reconstruct）**没有任何 skill 引用**；SKILL.md 仍写"registry 注册 8 个""workflow 节点 9"，与 INDEX 的 19 冲突；同类漂移还有 SKILL.md"现有 12 个 profile、JPN 未覆盖"，而 `references/regions/` 实有 13 份（含 09-15 补建的 JPN.md） | 〔码〕grep 结果；SKILL.md:54-56,596,717 vs INDEX.md:65,207-211 |
| N14 | P3 | 体检硬门规则 1（cov<0.4 必须含 ts_backfill）与规则 5（稀疏事件必须 trade_when）对同一字段叠加：真实 320 个体检包 56,235 个字段中 **2,162 个**同时满足两条件，合规的事件门控写法也会被规则 1 判违规 | 〔码〕`webdata_quality.py:344-381`；〔沙〕w6 `trade_when(syn_surprise_evt>0,…)` 被判违规；真实包统计 |
| N15 | P3 | 其它小项：`campaign` 节点 calibrate / assemble-priors 的 ledger 缓存命中条件 `cached.get('value')` 永不成立（死代码）；MCP `upsert_wave_result/get_wave_result` 的 `wave_number: int` 与表结构 TEXT 冲突（✅ 随 P0-1 已修）；`get_campaign_summary.latest_wave` 用 `CAST(wave_number AS INTEGER)` 排序；`submit_alpha` 节点默认给所有提交（含 RA）打 `PowerPoolSelected` 标签；VECTOR 未包裹的报错文案写成 `[EVENT]` | 各节，〔码〕+〔沙〕 |
| N16 | **P1** ✅已修 | S2 开波闸连 assemble-priors 一起拦：区域一停，知识回流即断 | 〔真〕§14.5 |
| N17 | **P1** ✅已修 | P0-2 初版的快照新鲜度检查漏看 registry，且把 UTC / 本地两种时钟混比 | 〔真〕§14.5 |
| N18 | **P1** ✅已修（§14.8） | priors 截断按 entry_id 字母序：新封存的死路进不了 GEM | 〔真〕+〔史〕§14.5 |
| N19 | **P1** ✅已修（§14.8） | `D:\` 默认路径：wave_gate 把候选写进仓库根的杂散库（git 不可见）；assemble-priors 崩溃；干跑 / 单测在默认路径建空库 | 〔真〕§14.5 |
| N20 | **P1** ✅已修（§14.8） | verdict 写入契约只认得 30 条真实历史写法中的 6 条；唯一的 PASS 波不被识别 | 〔真〕§14.5 |
| N21 | **P1** ✅已修（§14.8） | gate 缓存键不含 `--datasets`：漏声明第二腿后补声明仍拿到缓存的 FIELD 失败，跨集赢家被拦 | 〔真〕§14.5 |
| N22–N27 | P2–P3 | 规则 B 窗口按 updated_at（第三轮建议升 P1，§14.8.4；✅ R22 已修，§14.9）；`.mcp.json` 不可移植；孤儿节点 / 工具面缺陷；argv 只校验分发层；fail-open 与静默降级；质量预估刻度失准等 | 〔真〕§14.5 |
| N28 | **P1** ✅已修（§14.8） | `gate.py` 找工作区 `src/` 的解析没随 R19 收敛：`.mcp.json` 原样 env 下 op_arity 不可达，**每条表达式都记 `[ARITY_UNKNOWN]`，静态闸全拦**；仓库自带 4 条单测常红即此因 | 〔真〕§14.8 |
| N29 | P2 ✅已修（§14.8） | R21 逐条回写把"闸门环境缺失"（`[*_UNKNOWN]`）写成 `fail`；这类结论还会进逐条缓存，环境修好后仍被复用 | 〔真〕§14.8 |
| N30 | **P1** 未修 | 收批级联 `wqb_db_mcp._cascade_wave_result`（`harvest_multisim_results` 调用，SOP 步 6 的手动补收入口）绕过 P0-1 写入契约：用 `int(re.search(r"(\d+)", wave))` 取波号（`s2_<ds>_d1` → **2**、`91c` → 91），直接 UPDATE 覆盖已有 verdict（含人写的枚举值）或 INSERT 一条 closed 行 | 〔码〕§14.9.4 |

### 0.3 09-16/17 建议的落地复核（代码核验）

| 前序编号 | 建议 | 09-27 状态 | 证据 |
|---|---|---|---|
| #1 体检包补齐 | 开区硬前置 + fail-closed 档 | 🟡 机制已落地（`--inspect-mode enforce`）；数据源阻塞（本地快照只覆盖 7 区）本环境无法复核 | `wave_gate.py:659-667,985-987` |
| #2 D3 改写 | 删除加权混合方子 | ✅ | `decision-table.md` D3「组合形态铁律」 |
| #3 / P0-2 背压 | 未消费口径（含 gem/selected） | 🟡 已实现，但 `unconsumed_enforce=False`（灰度，只报不拦） | `campaign.py:961-967,1076-1087`；〔沙〕60% 未消费仅 WARN |
| #4 / P0-3 | 0 达标 PARTIAL 计入规则 B | 🟡 未按原方案：只加了可选 `strict_no_pass`（默认关） | `campaign.py:947-951,1229-1234` |
| #13 / P0-3 | 空壳 verdict | 🟡 读侧 UNKNOWN→WARN 已做；**写侧拒绝未做**，且存在 N1 的"部分更新清空"新路径 | `wqb_db_mcp.py:857-899` |
| P0-1 | 闸下沉到 toolkit 入口 | 🟡 已下沉到 build_wave / wave_gate，默认 warn；batch_track 路径无闸（N5） | `region_gates.py`、`build_wave.py:408-439` |
| P0-4 / #14 | s0_whitelist schema 统一 | ✅ `wqb.ledger_whitelist.normalize` 已被 campaign 节点与 region_gates 使用 | `campaign.py:1443`、`region_gates.py:260` |
| #5 | step_metrics 空转表 | ✅ 已下线，`tools/step_funnel.py` 可用 | 〔沙〕漏斗零副作用输出 |
| #7 | 三次 calibrate | ✅ 澄清为"2 必需 + 1 可选" | SKILL.md:188-201 |
| #8 | signal_floor fail-closed | ✅ | `campaign.py:1286-1323` |
| #10 | check_batch 口径收敛 | ✅ 文档收敛 | SKILL.md:312-313 |
| #11 | feature_engineering 收口 | ✅ 正文 + GEM 跳过模板来源 | SKILL.md:215-222、`gem.py:153-166` |
| #12 | priors 键撞名 | ✅ 缓存键改名 | `campaign.py:209-214` |

---

## 1. 评判口径

一个子项被判为：

- **★★★ 保留深化**：有生产实证证明它拦下过真实损失或带来数量级收益，且成本为零或极低（本地、零配额）；深化方向 = 把它从"文字规则"变成"机器约束"。
- **★★ 保留**：有效但收益有限或有替代；维持现状，只修缺陷。
- **★ 按需**：不进主链，需要时调用。
- **✂ 精简/去除**：满足任一：① 代码证明无效（死代码、永不触发）；② 与其它实现重复且口径冲突；③ 只产生噪声（打印 FAIL 却不影响判定）；④ 已被自身文档降级却仍占主链篇幅。每条去除都给替代路径。

判"价值"只看三件事：**是否挡住过真实的配额/时间损失**、**成本（配额 / 时间 / 本地算力）**、**是否与其它机制重复或冲突**。

---

## 2. 步 1（S-PRE）查表

**定位**：回答"这个区值不值得开新挖；先清库存还是新挖"。

**主入口**：`references/regions/<R>.md`（profile）；`mcp__wqb-db__get_campaign_summary / get_dead_ends / get_dead_datasets / get_mining_yield`；库存盘点 `tools/build_gate_prior_from_inventory.py` → `tools/select_ra_basket.py`（workflow 节点 `inventory_scan` 包装二者，但 SOP 未引用）；PPA 主题 `get_messages`；可选 `brain-next-move-analysis`、`brain-forum-browse`。

**输入**

| 类别 | 内容 |
|---|---|
| 驱动参数 | `region`（唯一必填） |
| 静态配置 | profile front-matter：`entry_verdict`（active / probe-only / frozen）、`static`（universe/delay/中性化合法档）、数据集红黄绿榜、`priors`、`gate_overrides`、`loop_policy` |
| 本地库 | `wave_results`、`registry_empirical`（dead_end/win 层）、ledger `*_dead`、`expressions`、`backtest_results`、`alphas` |
| 平台 | `/users/self/alphas`（按 `settings.region` 分区，每区最多翻 1000 条，`build_gate_prior_from_inventory.py` 头注）、`/alphas/{id}` detail、公告 |

**处理过程**

1. 读 profile → 按 `entry_verdict` 裁决（MEA=frozen 即停；无 profile 的 AMR 走处女地模板。注：`references/regions/JPN.md` 已于 09-15 补建，但 SKILL.md:54-56/67 仍写"12 个 profile、未覆盖 AMR/JPN"，属文档漂移）。
2. 库存盘点（先于一切新挖）：枚举账户 IS alpha → 用 WebDataScope 口径复算 failed_ra_count → 按 region ×（中性化 / universe / 算子数 / decay / 字段族）统计过闸率，写 `region_kb.gate_priors`（供步 4 prompt 与步 6 设置先验）→ 候选池 → `select_ra_basket`：去参数网格 → OS 撞车预筛（本地 PnL 互相关，不占平台相关性配额）→ 篮内正交 + 金字塔轮转 → 平台 detail `is.checks` 复核。
3. PPA 主题门禁：解析当期 Power Pool 主题的 region/delay/universe；不匹配的达标候选标 WAIT_THEME_ROTATION。
4. 先验查询：campaign_summary / dead_ends / dead_datasets / mining_yield（全区排名 + 本区按集拆）。
5. 双比率诊断：`conversion = 已回测/已生成`（低→修管道），`yield_rate = ra_clean/已回测`（低→换区换集；2026-09-19 起默认严格口径，要求 `ra_failed_checks` 为空）。

**输出**：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号（不落盘，交给步 2）；库存篮（`cache/basket.json`）；`region_kb.gate_priors`。

**价值评估**

| 子项 | 判定 | 依据 |
|---|---|---|
| 库存盘点 | ★★★ 保留深化 | 〔史〕SKILL.md:77-78：2026-09-07 跨四区 170 次新回测 0 条可提交 vs 一次库存扫描 20 条。成本主要是只读分页与本地互相关。**深化**：SOP 步 1 只给 CLI，`inventory_scan` 节点是孤儿（N13）——要么把节点写进步 1，要么删节点；同时在 SOP 标明平台 1000 条/区的分页上限，库存扫描不是全量 |
| conversion / yield 双比率 | ★★★ 保留 | 唯一能把"S2→S3 断链"与"标的不出货"分开的判据。〔沙〕同一种子库：严格 yield 0.025、宽松 0.0417（2 条带 `LOW_2Y_SHARPE` 的行被严格口径剔除），口径差可见。小瑕疵：停止规则 A 用 `sharpe > 1.58`（有符号），mining_yield 用 `|sharpe| ≥ 1.58`，两处"达标"定义不一致 |
| 判死台账（dead_ends / dead_datasets） | ★★★ 保留 | 零成本、直接避免重复踩死路 |
| PPA 主题门禁 | ★★ 保留，建议后移到步 8 | 只影响 PPA 分支；主题轮换时间不可控，放在 RA 开工前置里只会阻塞主线（v2 已提，仍未调整） |
| `get_campaign_summary.latest_wave` | ✂ 需修 | 〔码〕`wqb_db_mcp.py:487` `ORDER BY CAST(wave_number AS INTEGER)`；〔沙〕3 个 closed 波（w1/w2/w3）返回 `w1`。SOP 把"当前波号"列为本步产物，对 `s2_<ds>_d1`/`W-O` 这类字符串波号不可信；改按 `updated_at` 排序 |
| next-move / forum-browse | ★ 按需 | 不产出配置，只是情报 |

---

## 3. 步 2（S0）数据集体检 + 白名单

**定位**：回答"在哪挖"——锁定本战役的数据集白名单。

**主入口**：`workflow_campaign(stage="S0", calibrate=true)` + `workflow_campaign(stage="S0")` → toolkit `score_datasets.py [--calibrate]`；`tools/campaign_intel.py s0-select`；体检包 `tools/gen_field_inspect_packs.py`；锁白名单 `mcp__wqb-db__upsert_ledger_key(s0_whitelist)`；饱和数据集 → `hypothesis_round`。

**输入**：`settings.json`（region/universe/delay）；`thresholds.json`（category_weight、分位 tier、P0–P6 开关、signal_floor 等）；平台 `get_datasets` 全量、pyramid 端点（`recommend_datasets`）；`get_mining_yield`（严格口径）、`get_dead_datasets`；registry win 层；ledger `saturated_datasets` / `seat_model` / `dataset_empirical_prior`；本地 WebDataScope 快照（体检包数据源）。

**处理过程**

1. `calibrate`：反学 category 权重与拥挤甜区，**只写 `thresholds.json`、不产排名**；
2. `score`：覆盖、拥挤惩罚、字段丰富度、valueScore 加权 → `s0_ranking`（`score` = 信号强度榜，`pyramid_view` = 点塔战略榜，分开排序）；P0 经验先验 / P2 饱和降级 / P3 universe 一致性守卫 / P5 饱和区 model 封顶 / P6 甜区去噪；
3. `s0-select`：未点亮塔 × 历史严格产出率 × 未判死；附跨区负先验、`fields<5` 仅作条件腿、`est_seats` 座位可达性；已点亮塔（当季 ACTIVE≥3）直接剔除；
4. 硬约束：白名单 ≥2 个非 MODEL；category_weight 限 0.9–1.15；`*_dead` 排除；白名单外禁生成；`alphaCount≥1 万` 或连续 2 波模板全灭 → 切 hypothesis-first；白名单集须有体检包（或显式降级并记因）；
5. 锁白名单 → ledger `s0_whitelist`（历史 5 种 schema 由 `wqb.ledger_whitelist.normalize` 容错归一）。

**输出**：ledger `s0_ranking` / `s0_whitelist` / `s0_calibrate_<r>`（缓存标记）/ `*_dead`；更新后的 `thresholds.json`；体检包 `tracking/mining/field_inspect_<r>_<ds>.json`。

**价值评估**

| 子项 | 判定 | 依据 |
|---|---|---|
| `s0-select` 三方交叉 | ★★★ 保留深化 | 把选集依据从"本地 alphaCount 推断"换成"平台 pyramid 实测"，直接服务"主攻未点亮塔"；〔史〕09-19 先验增强前 IND 把结构性弱集推到前排，7 集 197 条回测 0 候选（SKILL.md:166-167） |
| 座位可达性 `est_seats` | ★★★ 保留 | 把"在不够的座位上反复打磨"这一隐性浪费显式化（Σest_seats < target 即报结构性不可达） |
| 已点亮塔不进白名单 | ★★★ 保留 | 用户 09-19 定案；直接落实 CLAUDE.md"点塔要均匀" |
| 饱和路由 → hypothesis-first | ★★★ 保留 | 模板遍历在饱和集上的边际产出接近零 |
| 体检包开区硬前置 | ★★★ 保留 | 见步 5；但数据源边界（本地快照只含 ASI/CHN/EUR/GLB/JPN/KOR/USA，DEU/JPN 白名单 0 集可生成）仍需人工补数据包 |
| calibrate | ★★ 保留（2 必需 + 1 可选） | 必要性已在 09-17 澄清（calibrate 不产排名） |
| 评分公式本身 | ★★ 冻结 | 权重无严格验证，但 tier 兜底 + 六项补丁后可用；不建议再加因子 |
| 节点内 calibrate / assemble-priors 缓存 | ✂ 去除 | 〔码〕`campaign.py:204-231` 命中条件是 `cached.get("value")`，而 `get_ledger` 返回 payload 本体（`_ledger.py:28-37`），节点自己写的 payload 只有 `calibrated_at/region/stdout_tail`；〔沙〕命中条件恒为 `None`。今天它无害，但**没有 TTL**：一旦有人"修好"键名，calibrate 与 priors 组装会变成永不重算的静默缓存 |
| `_ensure_campaign_config` 在 dry-run 下写盘 | ✂ 需修（N10） | 〔沙〕临时移走 `tracking/AMR/config/settings.json` 后干跑 S0，节点**写出**一份新 `settings.json`（universe=TOP3000、decay=4、SUBINDUSTRY、startDate/endDate 固定），违反 dry-run 契约；且这些硬编码默认值绕过了 `src/wqb/config.py` 的"唯一事实源" |

---

## 4. 步 3（S1）字段扫描 + 理解

**定位**：回答"用哪些字段、怎么预处理"。

**主入口**：`workflow_campaign(stage="S1", dataset=…)` → toolkit `scan_fields.py`（`GET /data-fields?dataset.id=…`）；`get_datafields` 做 users 分级；`workflow_feature_engineering`（按需、仅人读、禁注入 GEM）；（孤儿节点 `field_understanding`）。

**输入**：dataset / delay / universe；平台字段元数据（id、type、coverage、userCount、alphaCount、description）。

**处理过程**：扫描落 typed catalog（DB `datasets`/`fields` + ledger `catalog_<ds>`）；按字段类型众数推断数据集 `data_type`；users 分级（≥50 只做方向验证、10–49 提交前必测 prod、0–9 优先且占批次预算 ≥50%）；字段数 <10 退回步 2；VECTOR 比例确认后把 `data_type` 传给步 4。

**输出**：typed catalog（闸 2/3/8 与 catalog 前置闸的数据源）；ledger `s1_<ds>_d<delay>`（`ideas_md_path` + `source`）。

**价值评估**

| 子项 | 判定 | 依据 |
|---|---|---|
| typed catalog | ★★★ 保留 | 类型错配是批级连坐第二大来源（〔史〕MEA fundamental6 标 VECTOR 实为 EVENT → 整批 ERROR）；〔沙〕缺 catalog 的 `syn_news` 被 region_gates 的 catalog 前置闸点名 |
| users 分级 | ★★★ 保留深化 | 在生成之前避开 prod 拥挤区，比生成后靠相关性剪枝便宜得多。**但它只是 SOP 文字**，没有任何工具实现（沙箱里只能按规则手算）；"冷门字段 ≥50% 预算"因此无法被机器执行或审计。深化 = 把分级做成 `s0-select`/`scan_fields` 的输出列或 GEM 候选字段池的排序键 |
| 字段数 <10 守卫 | ★★ 保留 | 薄集撑不起七槽多样性，早拦早换 |
| `workflow_feature_engineering` | ✂ 移出主链 | 09-15 已证实是确定性模板渲染（8 问框架 + `rank(ts_mean({f},66))`），注入 GEM 会让 GEM 不调 LLM；现已"仅人读"。建议从步 3 正文挪到"按需知识型 skill"表，减少主链篇幅 |
| `field_understanding` 节点 | ✂ 待定去留 | SOP 无引用；与 feature_engineering / `brain-datafield-exploration-general` 功能重叠 |
| S1 必填校验（N9） | ✂ 需修 | 〔码〕`campaign.py:161-170` 在推导式里用 `locals().get(p)`；〔沙〕Python 3.11.15 下 `stage=S1, dataset=syn_analyst` 被拒"缺少必填参数: dataset"，仓库自带 `tests/unit/test_workflow_nodes.py::test_campaign_stage_route_matrix` 同样失败。用户机器能跑通说明是 3.12+，属于潜伏的可移植性缺陷；修法一行（改用显式 `{"dataset": dataset}`） |

---

## 5. 步 4（S2）概念优先生成

**定位**：回答"怎么写成表达式"。本步只管生成与选波，门禁在步 5。

**主入口**：`workflow_campaign(stage="S2", subcommand="assemble-priors")` → toolkit `assemble_priors.py`；`workflow_gem(pipeline_mode="phased")` → `headless_runner/run.py` → `run_pipeline`（LLM）→ `pipeline_pregate`；`workflow_campaign(stage="S2", dataset, wave)` → `build_wave.py`；可选 diversity-extract；（孤儿节点 `gem_wave`）。

**输入**：DB 知识库（`GLOBAL/region_kb` 模板与方法论、`<R>/region_kb` 的 win_recipes / dead_patterns / gate_priors、`KB/template_kb` 的 validated / failed）；profile 静态 priors（兜底）；typed catalog 与 `data_type`；候选字段池 `s2_field_pool_<ds>`；非模板来源的 S1 ideas。

**处理过程**

1. **assemble-priors**：wins ≤6、dead_ends ≤12 确定性组装 → 写文件 `<campaign>/priors/<r>_priors.json`；**仅在带 `--snapshot-ledger` 时**再写 DB 快照 `priors_snapshot_<r>`。
2. **GEM**：默认 `--priors-from-db <region>`，从 DB 快照物化 priors（无快照即 fail-closed）→ 机制 → 1–2 个字段 → 实现示例 → phased 分批 LLM。
3. **生成侧预闸 `pipeline_pregate`**：`quantile` 默认 driver 无损归一；`hump` 位置参数改命名参数；`bucket` 缺 range 补齐（非 rank 输入丢弃）；区域非法 group / 字段丢弃；非标窗口归一（20→22、60/63/65→66、250→252…，其余只 WARN）；同骨架换字段封顶 12；加权混合毒模式丢弃 → `expressions(status=gem)`。
4. **build_wave**：全历史去重 → 算子树分桶 → 骨架配给（linear_mix ≤50%）→ near 加权 → 波内字段去重 → `selected`，落选 → `superseded`；经节点调用时前置 signal_floor / stop_rules / backlog 三闸（enforce）。

**输出**：`expressions`（gem → selected / superseded）；priors 文件；（条件性）`priors_snapshot_<r>`；波元数据。

**价值评估**

| 子项 | 判定 | 依据 |
|---|---|---|
| 概念优先 GEM + priors 注入 | ★★★ 保留深化 | 防止"每个字段套一个 rank"的同质化堆；〔史〕KOR wave96–103 八波裸探针 64 条 0 达标 vs 复杂模板首批出 2 RA（决策表 D11） |
| `pipeline_pregate` | ★★★ 保留 | 〔沙〕6 条输入：quantile / hump / bucket / 窗口 20→22 各归一 1 处，加权混合丢弃 1 条，窗口 37 仅 WARN——零成本把闸 4/5 的高频 FAIL（〔史〕quantile 元数 312 次、加权混合 74 次）前移到生成器 |
| gate_priors 分流（表达式层进 prompt、设置层交给步 6） | ★★★ 保留 | 〔史〕GBR decay=14 过闸率 28.3% vs decay=4 3.9%，分流前三波仍跑 decay4 → 0/44 |
| build_wave 选波与骨架配给 | ★★★ 保留 | 槽位纪律直接决定产出 |
| **priors 回流（N2）** | ⚠ **断点，P0** | 〔码〕节点拼出的命令是 `campaign.py … assemble-priors [--dataset][--wave]`（`campaign.py:444-450`），不带 `--snapshot-ledger`；快照唯一写入点在 `assemble_priors.py:500`（仅 `--snapshot-ledger` 分支）；GEM 默认只读快照（`run.py:346-371`，缺快照 `SystemExit`）。〔沙〕(b) 按节点原样命令执行：文件被重写、`priors_snapshot_kor` 不存在；(c) 追加 `--snapshot-ledger` 后快照才出现。SKILL.md:269、281-286 声称该调用"写 DB 快照""S6 回写后下一次 S2 先验自动变新"——在 SOP 指定路径上不成立 |
| diversity-extract | ★ 维持可选 | SOP 自述"不强制、不替代 GEM" |
| `gem_wave` 节点 | ✂ 待定去留 | SOP 无引用；功能 = gem + build_wave 的合并版，与现行两步重叠 |
| gem 节点 dry-run 建目录（N10） | ✂ 需修 | 〔沙〕干跑新增 `logs/`、`logs/_async_tasks/`（`gem.py:327-331` 在 dry-run 返回前 `makedirs`） |
| 其它 | 小 | 节点在缺 `config.json` 时提示"从 config.example.json 复制"，但 `headless_runner/` 下没有该样例文件 |

---

## 6. 步 5（S2→S3）门禁

**定位**：在花任何仿真配额之前，拦下"整批 CANCELLED 连坐"与结构性必败的表达式。

**主入口**：`tools/campaign_intel.py ghost-audit`；`workflow_execute(node="wave_gate")` → `tools/wave_gate.py` → toolkit `gate.py`（8 闸 + 可选闸 0）+ `validator.py` + `op_arity` + `_lib/region_gates` + `field_inspect_gate` + `prod_saturation_gate` + 展示层（`pool_diversity` / `quality_predict` / `[opcat]` / 参数变体聚类）；（孤儿节点 `unified_gate` = ghost-audit + 转发 wave_gate）。

**输入**：候选表达式（`--from-db` 或 `--exprs-file`）；typed catalog；`platform_constraints.json` 与区域生成约束；闸 6 的 explore_contract；体检包；该区历史 alphas（PROD 饱和）。

**处理过程**（按 `wave_gate.py:main` 实际顺序）：区域四闸（catalog 前置 / signal_floor / stop_rules / backlog，默认 warn）→ 可选 GEM / 模板族 / S1 字段校验 → 语法 + 算子元数 → `gate.py` 闸 1–8（含闸 6 契约多样性）→ 体检硬门 → PROD 饱和闸 → 展示层（六维多样性、`[opcat]`、质量预估、参数变体簇）→ 写 `gate_results` → 汇总 `all_pass` → exit 0/1/2。

**输出**：`gate_results(all_pass, report_json)`；ledger `gate_w<wave>_<ds>`、`gate_cache_<ds>`；（`--exprs-file` 时）候选以 `status='gated'` 入库。

**价值评估（逐子闸）**

| 子闸 | 判定 | 依据 |
|---|---|---|
| ghost-audit | ★★★ 保留 | 纯本地、零配额；〔沙〕精确点名 `ts_entropy`（gate.py 只能报成"未验证字段"）；〔史〕ts_entropy 曾致 20 条全 CANCEL |
| 语法 + 算子元数 | ★★★ 保留 | 〔沙〕`hump(x, 0.01)` 被 SYNTAX + ARITY 双拦；〔史〕09-07 该写法曾"语法 8/8 PASS"后整批 CANCEL |
| gate.py 闸 2/3/4/5 | ★★★ 保留 | 〔沙〕10 条样本中 6 条被静态闸拦，原因各不相同且全部正确（未知字段 / VECTOR 未包裹 / `ts_min` 不可访问 / 函数式加权混合 / hump 元数 / 幽灵算子） |
| 闸 6 契约多样性 | ★★ 保留，需审视 | 〔沙〕要求每批 ≥2 个 (算子,字段) 组合使用 `bucket/if_else/ts_corr/ts_kurtosis` 之一，3 条的干净小批也判 FAIL；契约 `issued_at=2026-08-19` 仍在生效。它是探索多样性的强制器，但会把与机制无关的算子塞进批次；repair/probe 有逃生阀 |
| 体检硬门 | ★★★ 保留深化 | 〔沙〕e03 的低覆盖 / 高偏度 / 厚尾三项违规全部命中。**N14**：规则 1 与规则 5 在稀疏事件字段上叠加（真实包 2,162 个字段），建议字段仅出现在 `trade_when` 条件里时豁免规则 1 |
| PROD 饱和闸 | ★★ 保留 | 把 prod 墙判断前移到仿真前；无历史时如实报 unavailable |
| 区域四闸（warn） | ★★ 保留，语义待统一 | 见步 6 / N5 |
| 质量预估 `quality_predict` | ✂ 默认关闭 | 09-17 已判定预估不准并降为"仅标注"（`campaign.py:845-853` 注释）；〔沙〕对每条表达式给出同一个 0.27/0.16 并打印 `HARD_REJECT`，最终仍 PASS——纯噪声，还和 FAIL 语义冲突 |
| `[opcat]` 算子类别覆盖 | ✂ 改为 INFO 或接入判定（N6） | 〔码〕注释写"硬闸"，但不在 `all_pass` 计算里（`wave_gate.py:970-993`）；〔沙〕w8 打印"FAIL：缺 Group 类别"，最终 `=> PASS` exit 0 |
| 六维多样性 / 参数变体簇 | ★ 展示 | 保留为 INFO |
| `--exprs-file` 候选状态（N7） | ✂ 需修 → ✅ 已修（R7 随 R21，§14.8） | 〔沙〕w5/w6/w7 门禁 FAIL 后 19 条候选仍为 `gated`；积压闸把 `gated` 计入 pending+gated 与 unconsumed。〔真〕第三轮：先入 `pending`，按逐条结论回写 `gated` / `fail` |
| 工具解析与依赖（N12） | ✂ 需修 | 〔沙〕未设 `WQ_TOOLKIT_DIR` 时 `FileNotFoundError`（MCP 路径因 `.mcp.json` 设了 env 不受影响）；未装 `ply` 时 exit 1 而非 exit 2 |
| 其它 | 小 | VECTOR 未包裹的报错写成 `[EVENT] 事件型字段必须经 vec_* 聚合`；验证器在其 scripts 目录生成 `parsetab.py`（已 gitignore）；`wave_gate.py` 头部 docstring 仍写"结果落盘 `cache/gate_wave*.json`"，实际已只入库 |

**步 5b prod-first 探针**：★★★ 保留。〔史〕IND intraday_pv_feats 连投 3 波 24 条（IS 全过）后才查 prod = 0.79–0.92 整族报废；族首探 1–2 条即可避免。网络依赖，未演练。

---

## 7. 步 6（S3）七槽回测

**定位**：以账户并发上限（C≈7）把过闸批次送进平台、收回指标。

**主入口**：`workflow_batch_track` → toolkit `pipeline.py run --submit --review --write-ledger --max-rounds 3`；`workflow_task_status`；`harvest_multisim_alphas` + `harvest_multisim_results`；（孤儿节点 `auto_harvest`）。

**输入**：本波 expressions；`settings.json`；`region_kb.gate_priors`（设置先验）；`logs/_slots/` 槽位 token；配额。

**处理过程**：pipeline 内再闸（`gate.check_one` + 闸 6，sha1 缓存）→ 设置先验（`by_decay` / `by_neutralization` 样本 ≥30 且过闸率 ≥ 当前×2 的格子改写本波设置；`--set` 钉住的维度不动）→ 七槽填槽（`n_slots=min(7, 批数)`，多轮即收即补）+ 账户级槽位仲裁（`WQB_GLOBAL_SLOTS`=7）→ 轮询退避 + 挂起熔断 → 连坐隔离（ERROR 批定位坏式回写 `fail`，无辜兄弟重发一次）→ `--review` 收批评审并自动刷新 `region_kb`（recent_waves / gate_priors_local）。

**输出**：`backtest_results`（含 dataset）、`alphas`、`wave_results`（自动）、checkpoint、刷新后的 `region_kb`。

**价值评估**

| 子项 | 判定 | 依据 |
|---|---|---|
| 七槽填槽 + 账户级仲裁 | ★★★ 保留 | 吞吐 ×7 且多流水线并跑不超 C |
| 设置层先验 | ★★★ 保留 | 见步 4 gate_priors 分流 |
| 连坐隔离 | ★★★ 保留 | 〔史〕JPN w7/w8 一条坏式连坐整批，10 批丢 8 批 64 条 |
| argv 契约 + detached 存活握手 | ★★★ 保留 | 〔史〕`--concurrency 7` 让 S3"启动成功却从未真跑"13 天；〔沙〕所有拼子进程命令的节点（campaign / batch_track / gem / wave_gate / feature_engineering 等）干跑均通过 argv 校验 |
| 批次故障协议表 | ★★★ 保留 | 每行都有实证编号 |
| **开波三闸的路径覆盖（N5）** | ⚠ 需统一 | 〔码〕`batch_track.py` 与 toolkit `pipeline.py` 全文均无 signal_floor / stop_rules / backlog / region_gates 引用（grep 为空）；只有 `workflow_campaign(stage="S3")` 调（enforce），CLI 入口默认 warn。〔沙〕batch_track 干跑 steps 里没有任何闸，campaign S3 干跑有三闸。SOP"停止规则闸自动拦截"只对走 campaign 节点的人成立 |
| 积压闸 | ★★ 保留，给出切 enforce 的判据 | 〔沙〕未消费 60% 仅打印"[灰度·未拦截]"；`campaign_intel backlog-drop`（积压波清理）存在但 SOP 未提 |
| S3 前再跑一次 wave_gate | ✂ 精简 | 〔码〕`campaign.py:370-391` `_run_quality_gate` 以 `--from-db` 完整重跑一次 `wave_gate.py`（再写一次 gate_results / ledger），与步 5 重复；pipeline 内部本来就会再闸（`pipeline.py:305-368`） |

---

## 8. 步 7（S4）诊断改进

**定位**：回答"为什么不过闸、下一步改想法还是改参数、哪些族该止损"。

**主入口**：`workflow_campaign(stage="S4", wave=…)` → toolkit `review_wave.py --alphas … --tag … --write-ledger`；`campaign_intel s4-prescreen / prod-first`；`get_salvage_pool`；`wq-brain-alpha-optimization-v1`（Mode B 70% / Mode A 30%）；按需 `brain-calculate-alpha-selfcorr-quick`、`brain-explain-alphas`；（孤儿节点 `auto_review`、`modeb_improve`；`alpha_booster` 仅在 toolkit SKILL 中出现）。

**输入**：本波 alpha_id（按 `backtest_results.wave` 精确匹配，或 `s2_<ds>_d%` 标签）；`metrics_cache` 读穿的平台指标（含 `rn_sharpe`、robust / sub-universe）；`thresholds.review` / `near`。

**处理过程**：`passes()`（sharpe / fitness / 2Y / margin / turnover / failed_checks / RN）→ `walls()` 诊断卡在哪堵墙 → near 池（sharpe 过 near 线且非 `ROBUST_STRUCTURAL`）→ combo 候选 → 规则推荐下一波 → 写 `review_<tag>`、`submit_ready`、`near_pool`、`salvage_pool`、自动 `wave_results`、算子覆盖回写；预筛分 READY/REVIEW/REJECT；prod-first 族级 EXPAND/STOP；Mode B/A 改进（仅结构交互，禁加权混合）。

**输出**：ledger `review_<tag>` / `submit_ready` / `near_pool` / `salvage_pool` / `s4_walls_<r>_<w>`；`alphas.prod_correlation`；改进候选。

**价值评估**

| 子项 | 判定 | 依据 |
|---|---|---|
| RN_EXPOSURE 墙 | ★★★ 保留（判别力最强的一条） | 〔史〕HKG w4 七条里六条 RN 为负而 raw sharpe 非零；约 150 次回测里唯一的真信号 RN≈raw。〔沙〕RN=-0.2 的行 `walls=['RN_EXPOSURE'] passes=False` |
| **RN_EXPOSURE 进 near / salvage 池（N4）** | ⚠ 需修 | 〔码〕`review_wave.py:203-215` 只跳过 `ROBUST_STRUCTURAL`；〔沙〕同一行 `near=True`，会写进 `near_pool` 与 `salvage_pool`（`review_wave.py:297-317`），供 Mode A/B 取用——与 SOP"禁止继续调参"（SKILL.md:488-494）相悖。一行修复 + 单测 |
| ROBUST_STRUCTURAL | ★★★ 保留 | 让停止规则 B 真正可触发（此前"PARTIAL"掩盖全灭波） |
| s4-prescreen | ★★★ 保留 | 〔史〕8 条候选评审压成 1 次预筛，约 8× |
| 收批后 prod-first | ★★★ 保留 | 〔史〕全区绑定约束是 PROD（库存 22/22 撞墙 0.80–0.99） |
| salvage 检索 + 结构交互 | ★★★ 保留 | 〔史〕09-17 探针：7 种加权混合写法全被闸 5 拦、7 种结构交互全 PASS |
| Mode B/A 70/30 | ★★ 保留 | 〔史〕KOR wave96–104 背书 |
| `auto_review` / `modeb_improve` / `alpha_booster` 节点 | ✂ 待定去留 | SOP 未接线；与 review_wave / optimization-v1 功能重叠 |
| campaign S4 解析 alpha_id | ★★ 保留 | 〔沙〕w1 解析出 40 条；不存在的 w9 显式 FAIL 并列出最近波次 |

---

## 9. 步 8（S4→S5）稳健闸与提交判定

**定位**：回答"这一颗能不能交、现在交不交"。

**主入口**：`brain-alpha-robustness`（必经）→ Failed-count 资格门（`mcp_core._slim_checks` 预计算 `ra_failed_count`）→ `mcp__wq-brain-http__submit_verdict` → **用户确认** → `workflow_submit_alpha(confirm_submit=True)` / `submit_batch`；可选 `workflow_judge`（参考层，含 `checklist` / `degraded_gates`）。

**输入**：alpha_id；`is.checks`；`GET /alphas/{id}/submit`；平台 prod / self 相关性；当日配额（REGULAR 4 + SUPER 1 + PPA 1，00:00 ET 重置）。

**处理过程 / 判定表**（〔推〕按 `tools_ops.py:236-251`）：

| 模拟层 FAIL | 硬闸 WARNING | 提交层状态 | verdict |
|---|---|---|---|
| 无 | 无 | 200 | SUBMITTABLE |
| 无 | 无 | **404（处女提交）** | **UNVERIFIABLE** |
| 无 | 有 | 任意 | BLOCKED |
| 无 | 无 | 403 | BLOCKED |

**输出**：判定 + 用户确认 + 提交结果（submission_ledger / alphas.status）。

**价值评估**

| 子项 | 判定 | 依据 |
|---|---|---|
| 用户确认门 | ★★★ 保留（不可自动化） | 〔沙〕`submit_alpha` 未确认时计划只有预检；`confirm_submit=True` 的计划才含 `POST /alphas/{id}/submit` |
| Failed-count 资格门（生产口径） | ★★★ 保留 | 比只看 `result=="FAIL"` 严格（WARNING/ERROR 也计）；〔沙〕合成 checks → `failed_ra=3`（LOW_2Y WARNING、IS_LADDER WARNING、SUB_UNIVERSE FAIL） |
| **`src/wqb/config.py` 的分叉实现（N3）** | ✂ 去除或改为引用生产口径 | 〔沙〕同一组 checks → `failed_ra=0`。名单只有 8 项且含平台不存在的检查名，只数 FAIL——正是 SOP 警告不要用的宽松口径。它只被 `tests/unit/test_config.py` 引用，但处在"唯一事实源"模块里 |
| `submit_verdict` | ★★★ 保留，**修正定位（N8）** | 能可靠"否决"（模拟层 FAIL、硬闸 WARNING、403），但对新候选（404）只能给 UNVERIFIABLE。SKILL.md:516"最终判定以本步为准"应改为"否决权威"；新候选的放行依据写清为：模拟层 checks 全过 + `check_correlation(prod) < 0.7`（决策表 D14 已要求）+ 用户确认 |
| prod 0.60–0.70 当天提交 | ★★★ 保留 | 〔史〕pv103 一小时内被外部同款堵成 1.0 |
| `workflow_judge` | ★ 参考层 | 已降级；`degraded_gates` 非空时 verdict 不可用的规则有价值 |
| `submit_alpha` 默认标签 | ✂ 建议改 | 〔码〕`submit_alpha.py:60-61` 未传 tags 时一律打 `PowerPoolSelected`（含 RA）。平台是否因此改变通道未验证（worldquant-submit-alpha SKILL:220 记载该标签不能让 RA 闸放行 PPA），但语义混淆，RA 默认不应带 PPA 标签 |

---

## 10. 步 9（S6）复盘回写

**定位**：把本波结论写回库，让下一波的选集、先验、停止判定自动变新。"未回写视为本波未完成。"

**主入口**：`tools/step_funnel.py`（只读漏斗）；pipeline `--review` 自动刷新 `region_kb`；`mcp__wqb-db__upsert_wave_result` / `upsert_registry_empirical` / `upsert_ledger_key(s6_verdict_<w>)`；`seal_dead_end`；`campaign_intel pyramid`；`value_factor_trendScore`；`performance_comparison`；`submit_ready_blocked`；（孤儿节点 `auto_pyramid`）。

**输入**：本波 backtest / gate / 提交结果；平台金字塔状态。

**处理过程**：漏斗定位瓶颈 → verdict 三态回写（描述进 key_findings）→ win / dead_end 回写（dead_end 前先 seal，把残值沉降进 salvage）→ 点塔进度写进 key_findings → prod 饱和反馈 S0 → 多样性与 IS→OS 衰减监控。

**输出**：`wave_results.verdict / key_findings`；`registry_empirical`；ledger `s6_verdict_<w>`、`submit_ready_blocked`；`region_kb`。

**价值评估**

| 子项 | 判定 | 依据 |
|---|---|---|
| verdict → 停止规则 B | ★★★ 保留 | 〔沙〕写入 w4=FAIL 后最近 3 个 closed 波为 FAIL/FAIL/FAIL，下一波 `campaign S2` 被拦 |
| **非合并式 UPDATE 清空 verdict（N1）** | ⚠ **P0** | 〔沙〕随后按步 9 指引（SKILL.md:578）只补写 `key_findings=["[pyramid] …"]` → w4 的 verdict 变 NULL → 规则 B 看到 UNKNOWN，只告警不拦截 → 同一个下一波 `campaign S2` 被放行。〔码〕`wqb_db_mcp.py:880-884` UPDATE 对所有列赋值；该入口也允许 closed + 空 verdict，而 toolkit `WaveResultsStore.upsert`（`_lib/wave_results.py:82-85`）会拒绝 |
| region_kb 自动刷新 | ★★★ 保留 | 让步 6 设置先验读到最新值；**注意**它不自动刷新步 4 的 GEM priors（见 N2） |
| `step_funnel` | ★★★ 保留 | 〔沙〕零副作用，给出"S3 回测完成 → 过廉价闸（保留率 0.0417）"的瓶颈定位 |
| seal_dead_end（先沉降再封存） | ★★★ 保留 | 判死不丢残值 |
| 点塔进度回写 | ★★★ 保留 | 与 S0 三方交叉首尾相接；`auto_pyramid` 节点用定向 UPDATE 追加 key_findings，不会清 verdict——比 SOP 当前写法安全 |
| prod 饱和反馈 S0 | ★★★ 保留 | 最接近闭环控制的一条 |
| VF trendScore 监控 | ★★ 保留 | 每 3–5 颗一次 |
| T+1 IS→OS 衰减归因 | ★ 可选 | 无系统执行证据 |
| `wave_number` 类型 | ✂ 需修 | 〔码〕MCP 签名 `wave_number: int`（`wqb_db_mcp.py:82,822`），表结构 TEXT；字符串波号经 MCP 参数校验可能被拒（需在 live MCP 实测确认） |

---

## 11. 横切问题（跨步骤）

### 11.1 战役库路径：7 套解析口径（N11）

| 位置 | 口径 |
|---|---|
| `src/wqb/workflow/_common.resolve_db_path()` | `WQB_DB_PATH` 或仓库推导 |
| `src/wqb/store/_common.default_db_path()` | `WQB_DB_PATH` 或向上找 `data/wqb.db` |
| `WorkflowExecutor.__init__`（`executor.py:89`） | **相对路径** `data/wqb.db`（依赖 cwd） |
| `wqb_db_mcp.DB_PATH` | 模块所在目录 `/data/wqb.db`，忽略 `WQB_DB_PATH` |
| toolkit `_lib/ledger.SqliteLedgerStore`（`ledger.py:109-114`） | `WQB_WORKSPACE`，缺省**硬编码** `D:\coding\traeCN_project\wqb` |
| `tools/wave_gate.py`（:524/576/758/826/923） | `WQB_ROOT`/`WQ_PROJECT_ROOT`，缺省**硬编码** `D:\…` |
| `campaign._ensure_campaign_config` | `REPO_ROOT/data/wqb.db` 硬编码 |

在用户的 Windows 机器上它们恰好都指向同一个库，所以生产没出事；但任何换路径、换机器、做隔离（单测、沙箱、演练）的场景都会读写错库或崩溃。〔沙〕只设 `WQB_DB_PATH`/`WQB_ROOT` 时 assemble-priors 报 `unable to open database file`，必须再设 `WQB_WORKSPACE`；换 cwd 调节点会在当前目录新建空库。AGENTS.md §4 记录的"全套件本地全跑会红"与此同源。

### 11.2 节点孤儿与文档漂移（N13）

- registry 19 个节点，SOP 正文引用 8 个；9 个 09-16~18 新增节点无任何 skill 引用（AGENTS.md 明确反对"存在但无人知何时用"）。
- SKILL.md:596 写"registry 注册 8 个"并称步 1/7/8/9 无节点，附录 SKILL.md:717 写"workflow 节点 9"，INDEX 为 19——三处数字互相矛盾。

### 11.3 dry-run 契约的测试缺口

仓库的 `test_dry_run_reports_error_when_it_fails` 只断言"干跑失败必须带 error"，不断言"干跑零副作用"。本次 N10 的两处破口正是这道护栏的盲区。§12 的 Probe（快照文件树 + 库内容摘要 + 拦截 socket/subprocess）可以原样做成单测。

---

## 12. Dry-Run 演练（沙箱，第一轮；第二轮真实环境复跑见 §14）

### 12.1 环境与方法

| 项 | 设置 |
|---|---|
| 代码 | `git archive HEAD`（c393bca）导出的独立副本 `<SBX>`；真实仓库只读，演练前后 `git status` 均为 0 变更 |
| 数据 | `seed_db.py` 建合成库：KOR；typed catalog `syn_analyst`（7 字段：MATRIX×5、EVENT×1、VECTOR×1）；w1/w2/w3 各 40 条回测（w1 最强 1.935，5 条过廉价闸，其中 2 条带 `LOW_2Y_SHARPE`，1 条 RN=-0.2）；w4 150 条 gem + 30 条 gated；w1 PARTIAL、w2/w3 FAIL；ledger `s0_whitelist`（`syn_analyst` + 无 catalog 的 `syn_news`）/ `s0_ranking` / `region_kb` / `s1_*`；合成体检包 |
| 隔离 | 进程内拦截 `socket.connect`（网络尝试 0 次）与 `subprocess.Popen`；`HOME` 指向空目录（不读任何技能安装位）；每个探针前后比对文件树与库内容 |
| 执行 | workflow 节点一律 `dry_run=True`；标注"沙箱内实跑"的只有纯本地脚本（assemble_priors、ghost-audit、wave_gate、step_funnel）与纯函数（pregate、review_wave 判定函数、Failed-count 计数） |
| 不可演练 | 平台端点（s0-select、scan_fields、GEM LLM、仿真、s4-prescreen、prod-first、submit_verdict）——按源码静态推演 |
| 依赖 | 沙箱本地装 `ply`（验证器依赖，requirements 未声明）与 `msgpack`（已声明）；未装时的行为单独演示 |

### 12.2 逐阶段：输入 → 输出变化 → 价值判定

| 步 | 输入（沙箱） | 实际输出 / 状态变化 | 副作用 | 价值判定 |
|---|---|---|---|---|
| 1 | KOR profile `entry_verdict=active`；种子库 | `mining_yield`: expressions 300 / backtested 120 / conversion 0.40 / passed 5 / ra_clean 3 / **yield 0.025（宽松 0.0417）**；`campaign_summary.latest_wave = w1`（应为 w3）；`inventory_scan` 干跑给出 build_gate_prior → select_ra_basket 计划 | 零 | 双比率有效；latest_wave 排序缺陷复现 |
| 2 | S0 calibrate / score 干跑；缓存探针；AMR 缺 settings | 两条命令构建成功；缓存命中条件 `cached.get('value') → None`；**AMR 干跑写出 `settings.json`**；区域四闸：catalog 命中（`syn_news` 缺 catalog），backlog 未消费 60% 仅灰度 WARN，warn 模式下 `ok=True` | AMR：FS +1 | 缓存 = 死代码；dry-run 契约破口；catalog 前置闸有效 |
| 3 | S1 干跑（有/无 dataset）；FE / field_understanding 干跑 | **有 dataset 也被拒**："缺少必填参数: dataset"（Python 3.11）；FE 与 field_understanding 构建成功；users 分级手算：`syn_num_est`(60)→仅方向，`syn_rec_mean`(15)→提交前测 prod，其余 0–9 优先 | 零 | S1 在 3.11 下不可用；users 分级无工具 |
| 4 | assemble-priors：(a) 仅 `WQB_DB_PATH` (b) +`WQB_WORKSPACE` 按节点原样 (c) +`--snapshot-ledger`；GEM / gem_wave 干跑；pregate 6 条 | (a) `unable to open database file`；(b) 文件重写、**`priors_snapshot_kor` 不存在**；(c) 快照写入（wins=1 dead_ends=1，来自种子 region_kb）；GEM 命令含 `--priors-from-db KOR`；pregate 6→5 条（归一 4 处、丢弃加权混合 1 条、窗口 37 WARN） | (b)(c) 改写 priors 文件；GEM 干跑 FS +2 目录 | **N2 断点复现**；pregate 高价值 |
| 5 | 10 条样本（每条覆盖一类闸）；ghost-audit；wave_gate ③无 toolkit env ④a 无 ply ④b 完整；⑥⑦ 隔离验证 | ghost-audit 精确拦 `ts_entropy`；③ `FileNotFoundError`；④a "需要安装PLY库" exit 1；④b 语法 9/10、gate.py **4/10 通过**（6 条被拦，理由各异且正确）、闸 6 判 FAIL、`=> FAIL`；⑥ 体检硬门拦 e03（三项违规）；⑦ `[opcat] FAIL：缺 Group` + 质量预估 `HARD=3`，**最终 `=> PASS` exit 0**；w5–w8 共 19 条候选全部停在 `gated` | 每次实跑写 gate_results / ledger / expressions；首跑生成 `parsetab.py` | 静态闸 ★★★；展示层噪声；gated 语义缺陷；解析/依赖缺口 |
| 6 | batch_track 干跑；campaign S3 干跑 | batch_track 命令 `pipeline.py … run --dataset syn_analyst --wave w4 --max-rounds 3 --review --write-ledger --submit`，**steps 中无任何区域闸**；campaign S3：signal_floor / stop_rules / backlog 三闸全部执行（放行）后才建命令；backlog 证据 total 300 / unconsumed 180 / `unconsumed_enforced=false` | 零 | N5 复现 |
| 7 | campaign S4（w1 / w9）；review_wave 判定函数（w1 前 5 条）；auto_review / booster / modeb 干跑 | w1 解析 40 个 alpha_id；w9 显式失败；SYNw1039/1038：`LOW_2Y_SHARPE` 墙；**SYNw1037（RN=-0.2）：`RN_EXPOSURE` 墙、passes=False，但 near=True**；1036/1035 通过 | 零 | RN 墙有效；N4 复现 |
| 8 | 合成 is.checks（LOW_2Y WARNING、IS_LADDER WARNING、SUB_UNIVERSE FAIL）；判定表；judge / submit_alpha 干跑 | 生产口径 `failed_ra=3`，**config 口径 `failed_ra=0`**；判定表：404→UNVERIFIABLE、200→SUBMITTABLE、硬闸 WARNING / 403→BLOCKED；submit_alpha 未确认只预检、确认后计划含 POST，默认 tags=`PowerPoolSelected` | 零 | N3、N8 复现 |
| 9 | step_funnel；写 w4=FAIL；只补写 key_findings；auto_pyramid 干跑 | 漏斗瓶颈"回测完成→过廉价闸 0.0417"；写 w4=FAIL → 规则 B `hits=["最近 3 个 closed 波 verdict 全 FAIL"]`，下一波 S2 **被拦**；只补写 key_findings → w4 verdict=NULL → 规则 B 仅 WARN，下一波 S2 **放行**；MCP 签名 `wave_number: int` vs 表 TEXT | 回写改库（预期内） | **N1 全链复现** |

### 12.3 19 个节点 dry-run 契约扫描（仓库自带 `_DRY_RUN_CASES` 参数）

| 结果 | 节点 |
|---|---|
| 成功且零副作用 | alpha_booster、auto_harvest、auto_pyramid、auto_review、batch_track、campaign、feature_engineering、field_understanding、gem*、gem_wave、inventory_scan、judge、modeb_improve、structural_reconstruct、submit_alpha、superalpha、unified_gate、wave_gate |
| 失败（带明确 error，符合契约） | hypothesis_round（测试参数 `dataset_id="_test"` 无假设目录） |
| 条件性副作用 | `campaign`：目标战役目录缺 `settings.json` 时干跑写盘；`gem`*：`logs/_async_tasks` 不存在时干跑建目录（扫描时目录已被前序探针建好，故显示零副作用） |

另：换一个 cwd 调用任意节点，`WorkflowExecutor` 会在该 cwd 下新建 `data/wqb.db`（+wal/shm）——N11。

### 12.4 演练结论

1. 九步的**判别机制本身在代码层面是工作的**：静态闸 6/10 拦截全部正确、体检硬门三项违规命中、RN 墙命中、停止规则 B 在 verdict 完整时正确拦截、漏斗只读。
2. 失效集中在**接缝**：priors 文件↔快照（N2）、两个 wave_results 写入口（N1）、节点↔CLI 的闸语义（N5）、生产↔config 的 Failed-count（N3）。这些都不会在单步测试里暴露，只有沿 S6→S2 或 S2→S6 走一遍才看得见——这也是本次演练最主要的产出。
3. 两个 P0 都属于"安全机制静默失效"：不会报错，只会让下一波在不该开的时候开、用旧知识生成。

---

## 13. 建议清单

### 13.1 P0（修复闭环，成本低）

| # | 建议 | 改法 | 验证 |
|---|---|---|---|
| R1 ✅已实施（§14.1） | 修 `upsert_wave_result`（N1） | UPDATE 改 `COALESCE(?, 列)` 合并语义；`status='closed'` 且 verdict 为空时拒绝（与 `_lib/wave_results.upsert` 同契约）；SKILL.md:578 的 pyramid 回写改为"追加 key_findings"专用入口（或复用 auto_pyramid 的定向 UPDATE） | 复跑实录步 9：补写 key_findings 后规则 B 仍拦截；+2 单测 |
| R2 ✅已实施（§14.1，含 N16 / N17 补充） | 接通 priors 回流（N2） | campaign 节点 assemble-priors 默认追加 `--snapshot-ledger`（或 SOP 显式要求 `extra_args=["--snapshot-ledger"]`）；GEM 物化快照时比较快照 `generated_at` 与 `region_kb.updated_at`，陈旧即 WARN | 复跑实录步 4(b)：快照存在且 wins 反映新 region_kb |

### 13.2 P1（安全/语义）

| # | 建议 | 改法 |
|---|---|---|
| R3 ✅已实施（§14.9） | Failed-count 单一实现（N3） | 把 `mcp_core._RA_CHECK_NAMES/_PPA_CHECK_NAMES/_ra_bad` 迁入 `src/wqb/config.py` 作为唯一事实源，mcp_core 与 build_gate_prior 引用它；删除现有分叉实现并改 `test_config.py` |
| R4 ✅已实施（§14.9；另覆盖组合候选与 pipeline 的 review 阶段） | near 池排除 RN_EXPOSURE（N4） | `review_wave.py` near 循环里 `if "RN_EXPOSURE" in r["walls"]: continue`；+单测 |
| R5 ✅已实施（§14.9；CLI warn 灰度 2026-10-11 截止、次日起缺省 enforce，§14.9.7） | 区域闸语义统一（N5） | `batch_track` 节点接入 `run_region_gates`（与 campaign S3 同为 enforce）；CLI 的 warn 灰度写明截止日期；SOP"快捷入口"注明必须过区域闸 |
| R6 | 去掉门禁展示层噪声（N6） | `[opcat]` 与质量预估改为 INFO（不再出现 FAIL / HARD_REJECT 字样），或真正接入 `all_pass`；质量预估默认关闭，需要时 `--quality` 开 |
| R7 ✅已实施（随 R21，§14.8） | 候选状态语义（N7） | `--exprs-file` 先入 `pending`，按 gate.py 逐条结论回写 `gated`/`fail` |
| R8 | 提交判定定位（N8） | SKILL.md 步 8 改写：submit_verdict = 否决权威；新候选放行 = 模拟层全过 + 平台 prod < 0.7 + 用户确认 |

### 13.3 P2 / P3（可移植性与治理）

| # | 建议 |
|---|---|
| R9 | `campaign.py:161-170` 改显式 dict（N9） |
| R10 | `_ensure_campaign_config` 与 gem 的 `makedirs` 移到 dry-run 判定之后；把 §12 的 Probe 做成"干跑零副作用"单测（N10） |
| R11 ✅已实施（作为 R19，§14.8） | 全部 DB 路径改走 `resolve_db_path()`；`WorkflowExecutor` 默认用它；删除 3 处 `D:\` 硬编码（N11）——第二轮实证后升为 P1，见 R19 |
| R12 ✅已实施（§14.9；覆盖 wave_gate / probe_batch_mode / pre_backtest_filter） | `wave_gate.py` 的解析改用 `skill_roots()`；requirements 增加 `ply`；缺依赖 / 缺脚本时 exit 2（N12） |
| R13 | 删除 campaign 节点缓存死代码（N15） |
| R14 | 9 个孤儿节点逐一定去留：接入 SOP（写清与既有步骤的替代关系）或下线；SKILL.md 的节点计数改为引用 INDEX（N13） |
| R15 | `wave_number` 改 `str`；`latest_wave` 按 `updated_at` 排序（N15） |
| R16 | 体检规则 1 对"仅作 trade_when 条件的稀疏事件字段"豁免（N14） |
| R17 | RA 提交默认不打 `PowerPoolSelected`（先在平台确认影响）（N15） |

### 13.4 汇总：保留深化 / 精简 / 去除

| 类别 | 子项 |
|---|---|
| **保留深化**（判别力所在） | 库存盘点、conversion/yield 双比率、s0-select 三方交叉、座位可达性、已点亮塔剔除、typed catalog、users 分级（做成工具）、概念优先 GEM、pregate、ghost-audit、语法+元数、gate.py 静态闸、体检硬门、prod-first（两处）、七槽+仲裁、设置先验、连坐隔离、RN_EXPOSURE、ROBUST_STRUCTURAL、submit_verdict（否决）、用户确认门、停止规则 B、region_kb 刷新、step_funnel、seal_dead_end |
| **精简** | feature_engineering 移出主链；PPA 主题门禁后移到步 8；质量预估默认关；`[opcat]` 降为 INFO；S3 前重复的 wave_gate 调用；judge 仅作参考 |
| **去除** | campaign 节点缓存分支（死代码）；`src/wqb/config.py` 的 Failed-count 分叉实现（✅ 已替换为唯一实现，§14.9）；`_ensure_campaign_config` 的硬编码默认配置（改为缺配置即报错并给出生成命令）；未被 SOP 采纳的孤儿节点（逐个确认后） |

---

## 14. 修复后真实环境复跑（第二轮，2026-09-27）

> 审阅意见："先修复两个 P0 问题，在真实环境而不是沙箱环境 dry-run，再做一次"。本节是第二轮的全部结果；第一轮（§1–§13）的结论除本节明确修订处外仍然有效。
> 复现：`bash reports/ra_pipeline_stage_review_20260927/realenv/reproduce_realenv.sh`。实录 `realenv/realenv_transcript.txt`，路径已脱敏为 `<repo>` / `<scratch>` / `<base>`。

### 14.0 一页结论

1. **两个 P0 已修复，并在真实 MCP 链路上用修复前 / 修复后对照验证**（§14.4）。
   - **P0-1**：只补写 key_findings 不再清空 verdict。在 KOR 真实历史下，补写前后停止规则 B 都照常拦截；修复前的同一次调用会把 wave 97 的 verdict 清成 NULL，把规则 B 放开。字符串波号可以读写；结案必须带 verdict。
   - **P0-2**：assemble-priors 节点会写 DB 快照；GEM 干跑能看到快照"缺失 / 过期 / 新鲜"三态，按告警重组后恢复安静。
2. **真实环境又暴露 P0-2 的两处残缺，已一并修复。**
   - **N16**：KOR 真实历史命中停止规则 B，SOP 步 4 的 `stage="S2"` 写法被开波闸拦下。知识回流恰好在"区域该停、该换向"时断掉，而 GEM 的过期告警指向的正是这条被拦的命令。
   - **N17**：初版新鲜度检查漏看了 S6 最常见的回写（registry 判死封存 / 登记 win），还把 UTC 与本地两种时钟混在一起比较。
3. **第二轮新发现 N18–N27**，应先处理的四条（P1；✅ 第三轮已全部修复并复跑验证，见 §14.8）：
   - **N18**：priors 截断按 entry_id 字母序。新判死结论进不了 GEM；已入库的 KOR priors 12 条死路全是 `KOR-A*`。
   - **N19**：`D:\` 默认路径在真实环境里把候选静默写进仓库根下一个 git 看不见的杂散库。
   - **N20**：verdict 写入契约只认得 30 条真实历史写法里的 6 条。
   - **N21**：gate 缓存键不含 `--datasets`。漏声明第二腿后补声明重跑，仍拿到被缓存的 FIELD 失败，KOR 唯一出过 ACTIVE 的跨集配方因此被拦。
4. **价值评估修订**（有真实数据支撑，§14.6）。
   - 在真实历史上给出正确判断：按数据集的 yield、相关性代理分、停止规则 B、step_funnel、静态闸（两腿都声明、且绕过缓存时 39/39 正确放行）。
   - **质量预估**把 39 条真实候选全部判 BLOCK，其中包括全部 5 条实测过闸者（2 条是已 ACTIVE 的原式）。它的判定从"精简"改为"**去除 BLOCK 标签 / 重新标定**"。

### 14.1 修复内容

| 项 | 改动 | 文件 |
|---|---|---|
| P0-1 写入契约 | 新模块作为 wave_results 的唯一写实现：<br>• 合并式 upsert：只覆盖显式传入的非 None 列；JSON 列一旦传入即整列替换。<br>• `status='closed'` 必须带 verdict，否则拒绝、不写库。<br>• verdict 归一 / 拒绝规则原样保留。<br>• `wave_number` 一律按字符串存取。<br>status 缺省语义不变：新行 → closed；写了 verdict → closed；只补其它列 → 状态不变 | `src/wqb/wave_results_contract.py`（新） |
| | MCP `upsert_wave_result` / `get_wave_result` 改为 `wave_number: Union[int, str]` 并调用契约；直写兜底 `DirectDBWriter` 走同一实现 | `wqb_db_mcp.py`、`tools/mcp_batch_writer.py` |
| P0-2 快照回流 | campaign 节点的 assemble-priors 默认追加 `--snapshot-ledger`，不再拼 `--dataset/--wave`（修复前拼上它们时，静态 argv 校验放行、实跑 exit 2，见 N25） | `src/wqb/workflow/nodes/campaign.py` |
| | gem 节点新增 `priors_snapshot_check` 步（干跑也走，只告警不阻断）：<br>• 快照缺失 → 预告 GEM 会 fail-closed；<br>• 快照早于任一 KB 源 → 列出过期源并给出修复命令 | `src/wqb/workflow/nodes/gem.py` |
| P0-2 补充（真实环境发现） | N16：`stage="S2"` 路由到 assemble-priors 时，跳过三道开波闸与 S0/S1 产物预检。diversity-extract 会生成候选，仍走闸 | `campaign.py` |
| | N17：新鲜度源改为 assemble-priors 实际读取的四类：`<r>/region_kb`、`KB/template_kb`、`KB/operator_principle_kb`、`registry_empirical`（win / dead_end）；去掉误列的 `GLOBAL/region_kb`。SQLite `datetime('now')`（UTC、空格分隔）先按 UTC 换算成本地时间，再与 Python isoformat（本地、`T` 分隔）比较；registry 的最新时间逐行归一后取最大，不用 SQL 的字符串 MAX | `gem.py` |
| 文档 | SKILL 步 4 / 步 9 注释同步；纠正契约原注释"与 classify 同规则"（不成立，见 N20） | `Claude/skills/wq-brain-ra-pipeline/SKILL.md`、契约模块 |
| 测试 | `tests/unit/test_p0_fixes_20260927.py` 共 21 条：<br>• P0-1 13 条：含停止规则 B 端到端、FastMCP 协议层字符串波号、直写兜底同契约。<br>• P0-2 8 条：含开波闸豁免、registry 过期、东八区时钟换算。<br>`test_workflow_nodes.py` 断言同步 | |

回归结果：
- 根测试 1117 passed / 21 failed。基线为 1096 / 21，多出的 21 条就是新增测试；**失败集合与基线逐条同名**，全部是既有的环境性失败。
- MCP 包 77 / 5，与修复前原始副本一致。其中 4 条 `test_extract_fields_*` 失败即 N26 所述的 operators_catalog 降级。

### 14.2 环境与方法

| 项 | 第一轮（§12，沙箱） | 第二轮（真实环境） |
|---|---|---|
| 代码 | `git archive HEAD` 副本 | **真实仓库工作树**（`d1c7d78` + 本轮修复） |
| MCP 服务 | 函数直调（FastMCP stub） | 按 `.mcp.json` 把路径翻译成本机路径，**`wqb-db` 与 `wq-brain-http` 经 stdio 真实启动**。全部调用走 MCP 协议：pydantic 参数校验、工具注册、启动告警都是真的 |
| 依赖 | `pip --target` 装 ply / msgpack | `world-quant-brain-mcp/.venv`（Python 3.12，`requirements.txt` 全量 + ply） |
| 数据 | 合成种子库（`syn_analyst`） | `tracking/KOR` 已入库的真实历史，**全部经 wqb-db 的 MCP 写工具导入**（导入本身就是一次契约实测）：<br>• 38 个 `wave*_result*.json` → 335 行逐 alpha 指标（其中 247 行带表达式）+ 30 条波级 verdict 原文；<br>• `priors/kor_priors.json` → 反推 DB 侧 KB（2 条 win_recipes、3 条 registry win、12 条 registry dead_end）；<br>• 字段目录：`ml_factor_proj`（333 字段）与 `multi_source_model`（60 字段） |
| 库 | 沙箱库 | 真实默认路径 `data/wqb.db`。演练期间原库临时移开、结束后移回；超过 5MB 的库需显式许可才动 |
| 平台 | 断网 | 容器无 BRAIN 凭据：平台类工具只记录真实失败形态（全部 fail-closed 报错，零平台写入） |
| 修复前对照 | — | 把同一份真实库复制到 `d1c7d78` 的原始副本，起修复前的两个 server，重放同一 P0 调用序列 |
| 仍不可演练 | 平台端点 | 同左；另有 GEM LLM（缺 `headless_runner/config.json`） |

**一启动就看到的环境事实**（步 0）：
- `.mcp.json` 里两个 server 的 command 都是 `D:/coding/traeCN_project/wqb/...` 绝对路径；本会话启动时两者都 ENOENT（N23）。
- `wqb-db` 注册了 45 个工具：其中 `_flatten_platform_alpha` 是私有 helper；另有 7 个 `workflow_*` 没有 `dry_run` 参数（N24）。
- `wq-brain-http` 注册了 69 个工具，启动 stderr 有四条告警：`info_data.bin` 缺失；Redis 不可用；`operators_catalog 不可用 — 字段预检算子过滤降级`（N26）；`No BRAIN credentials`。
- 空库上先调只读工具会报 `no such table: wave_results`，并在默认路径留下一个 0 表的空库文件（N26）。

### 14.3 逐阶段：输入 → 输出变化 → 价值判定（真实环境）

| 步 | 输入（真实） | 实际输出 / 状态变化 | 副作用 | 价值判定（相对第一轮） |
|---|---|---|---|---|
| 导入 | 38 个结果文件、30 条 verdict 原文 | 247/335 行入库（另外 88 行在历史文件里本就没有表达式）。verdict：<br>• **6 条**归一为 closed/FAIL（RED 前缀 / 全灭）；<br>• 24 条被契约拒绝（`no_submit`、`无提交(…)`、`FULL_RED`、`8/8 RED`、`2 GREEN + 6 RED`、`✅ 2 RA 提交成功`），按导入策略以 open 落库；<br>• 8 个文件没有 verdict | 写库（预期内） | 写入契约在真实写法上的覆盖面是新问题（N20） |
| 1 S-PRE | 导入后的 KOR 库 | • `get_mining_yield(strict)`：247 回测 / 5 过闸 / yield 0.0202。<br>• **按数据集：`ml_factor_proj` 5/39 = 0.128，其余全部 0**。<br>• `campaign_summary`：30 波 / 6 closed / 12 dead_ends。<br>• `recommend_datasets` → "Authentication credentials not found"。<br>• `inventory_scan` 干跑给出命令计划（`cache/…` 相对路径）；wqb-db 同名工具没有 dry_run → 真跑 → 平台失败 | 零 | **★★★ 实证**：按数据集的 yield 精确指出了 KOR 唯一的产出集，与 wave91c 的 2 条 ACTIVE 吻合 |
| 2 S0 | calibrate / score 干跑；区域四闸（warn） | 两条命令构建成功。catalog / signal_floor / backlog 放行；**stop_rules 命中 B**（95/96/97 连续"判死"）；warn 模式下 `ok=True` | 零 | 停止规则在真实历史上的判断与团队事后结论一致。warn 灰度 = 看得见、拦不住 |
| 3 S1 | S1 / FE 干跑；typed catalog | 命令构建成功（3.12）；333 字段全 MATRIX；前缀簇 3 个（`change` 253 / `log` 40 / …）。wqb-db `workflow_field_understanding` 真跑 → `no such table: field_catalog`：孤儿节点查的是不存在的表（N24） | 前缀簇写 ledger +1 | typed catalog 保留；孤儿节点再添一证 |
| 4 S2 | assemble-priors（修复后）× GEM 干跑 | • 4.0：修复前的 argv 实跑 exit 2。<br>• 4.1：按 `.mcp.json` 原样 env 真跑，崩溃 rc=1（N19）。<br>• 4.2：缺快照 → 告警。<br>• 4.3：**区域命中规则 B 时照样重组**；快照 wins 5/6、dead_ends 12/12，与已入库 priors 一致（缺的 1 条源自 template_kb，本演练无法反推）。<br>• 4.4：快照新鲜 → 静默。<br>• 4.5：region_kb 追加一条 win → 过期告警。<br>• 4.5b：`seal_dead_end(KOR-MODEL219-DEAD)` → 过期告警同时列出 region_kb 与 registry。<br>• 4.6：重组后恢复静默；新 win 进了快照，**新 dead_end 没进**（13 条按字母序截成 12 条，N18）。<br>• 4.7：GEM 干跑止步于 `check_config`（N27）。<br>• pregate：39 条里有 1 处非标窗口被归一 | 重写已入库的 priors 文件（演练结束 git 复原）；异步任务文件 | P0-2 闭环在真实链路上成立；截断策略成为新瓶颈 |
| 5 S2→S3 | 39 条 `ml_factor_proj` 真实历史表达式，含 5 条实测过廉价闸者，其中 2 条是 ACTIVE 原式 | • ghost-audit：0 个幽灵算子。<br>• ①：按 `.mcp.json` 的 env（无 WQB_ROOT）→ 候选写进仓库根的杂散库，gate.py exit 2（N19）。<br>• ②a：漏声明第二腿 → FIELD 拦下 19 条。**被拦的恰是实测 sharpe 均值 1.29 的一组**（最高 1.91，含全部 5 条赢家）；放行的 20 条均值只有 0.41。<br>• ②b：补声明 `--datasets` 重跑 → **缓存命中 39/39，结论不变**（N21）。<br>• ②c：声明 `--datasets` 并加 `--no-cache` → **静态闸 39/39 全部放行**；all_pass 仍为 false，只因批级多样性闸（3 项）。<br>• 相关性代理分对赢家原式给出 1.00（"疑似撞 88lr21xo / 78jQ29rL"）。<br>• **质量预估 39/39 BLOCK**：赢家预估 0.81–0.88，实测 1.76–1.91，Pearson 0.60。<br>• `[opcat] FAIL：缺 Group` 依然只打印不判定。<br>• 体检硬门因没有 `ml_factor_proj` 体检包而未生效。<br>• `validate_expressions` 无凭据时仍返回 `valid: true`（N26）。<br>• wqb-db `workflow_unified_gate` 真跑时 argv 缺表达式源（N24） | ②：写 expressions / gate_results；三次重跑留下 117 条 `gated`，FAIL 后也不回写（N7 复现），把积压推到 32% 超过 30% 上限，导致后面的下一波 S2 被积压闸拦下。①：杂散库 | 静态闸、prod-sat、相关性代理分 ★★★。"漏声明 + 缓存"的组合对跨集配方代价极高。**质量预估 ✗** |
| 6 S3 | batch_track / campaign S3 干跑 | batch_track：命令含 `--submit`，**不跑任何区域闸**，success。campaign S3：**被规则 B 拦截** | 零 | N5 在真实"应停"区复现：SOP 指定的入口照发 |
| 7 S4 | wave 94；salvage 回填；review_wave × 真实 thresholds | • S4 解析出 9 个 alpha ✓。<br>• `backfill_salvage_pool_batch`：34 个文件 / 6 成功 / 28 跳过；**入池条目的 expression 为空**（历史文件没有式子，无法复用）。<br>• review_wave：5 条过廉价闸的行 `walls=['MARGIN_UNKNOWN']`，却 `passes=False`（N27） | ledger +1 | 墙诊断保留；缺失值口径需统一 |
| 8 S4→S5 | 88lr21xo / 78jQ29rL | • `submit_verdict` → 无凭据报错（fail-closed ✓）。<br>• judge / submit_alpha 干跑只给计划，confirm 与否都不触平台 ✓。<br>• `get_submit_ready` = [] | 零 | 否决链在无凭据时不会误放行 |
| 9 S6 | P0 回放 + 其余 S6 动作 | • P0-1 的全部行为见 §14.4。<br>• 按拒绝提示把 91c 补记为 PASS → 规则 B 窗口变成 `[91c PASS, 97 FAIL, …]` → **规则 B 放行**（N22）。本演练中 S2 随后被积压闸拦下，但那份积压来自步 5 的三次门禁重跑。<br>• `step_funnel` 瓶颈："S3 回测完成 → 过廉价闸 0.0206"；verdict 分布 `(空)=23, FAIL=7, PASS=1`（其中 PASS 即 91c 补记），直接暴露 N20。<br>• auto_pyramid 干跑 ✓ | 写库（预期内） | P0-1 生效；规则 B 的窗口定义是新缺口 |
| 附 A | 19 个节点 × `workflow_execute(dry_run=True)`（经 MCP） | 17 个成功且零副作用。失败两个：`gem`（缺 `config.json`）、`hypothesis_round`（测试参数下没有假设目录） | 零 | 干跑契约在真实服务上成立。第一轮 N10 的两处破口仍在，只是本环境目录已存在，没触发 |

### 14.4 修复前 / 修复后对照（同一份真实库、同一 MCP 调用序列）

| 场景 | 修复前（`d1c7d78` 原样服务） | 修复后 |
|---|---|---|
| 写 / 读字符串波号 `s2_ml_factor_proj_d1` | MCP 参数校验层直接拒绝：`Input should be a valid integer … int_parsing`（写、读都拒） | inserted；读回 verdict=FAIL |
| KOR 真实历史下，下一波 S2 干跑 | 规则 B 拦截（95/96/97 全 FAIL） | 同左 |
| 步 9：只把点塔进度补写进 wave 97 的 key_findings | **verdict 被清空为 NULL**。同一下一波的 S2 干跑 → 窗口 `[UNKNOWN, FAIL, FAIL]` → **放行**（仅 WARN） | verdict 保留 FAIL，`updated_fields=["key_findings"]`；**仍拦截** |
| 新波只写 key_findings（缺 verdict） | 字符串波号先被参数校验拒掉；整数波号会落下一个 closed + NULL 的空壳行（第一轮已证） | 拒绝并提示："结案必须带 verdict；结论未定请传 status='open'"。不写库 |
| assemble-priors 干跑（带 dataset/wave） | 命令尾部是 `assemble-priors --dataset ml_factor_proj --wave p0`，干跑 success；同一 argv 实跑 exit 2 `unrecognized arguments` | `assemble-priors --snapshot-ledger`（S2 与 S6 两种写法一致） |
| assemble-priors 真跑 | 跑通，**但不写快照**（只重写文件）。注：它这次没被规则 B 拦，是因为上一行的 P0-1 缺陷已经把规则 B 放开。修复前代码的 S2 分支对所有调用都先跑三道闸（〔码〕）；本轮第一次真实运行（已加 `--snapshot-ledger`、尚未豁免开波闸）就被规则 B 拦下（N16） | 区域命中规则 B 时照样跑通，**并写快照** |
| GEM 干跑 | 没有快照检查步，静默（真跑时才 fail-closed） | `priors_snapshot_check` 三态可见：缺失 / 过期（列出过期源）/ 新鲜 |

### 14.5 第二轮新发现

| # | 级别 | 发现 | 证据 |
|---|---|---|---|
| N16 | **P1** ✅已修 | **S2 开波闸拦截 assemble-priors。** campaign 节点的 S2 分支对所有调用先跑 signal_floor / stop_rules / backlog 三闸，路由到 assemble-priors 的调用也不例外，而 assemble-priors 零配额、不开波。<br>区域一旦命中停止规则，S6 写下的新死路就再也进不了快照。gem SKILL 的 `stage="S6"` 写法不经闸，两条路径因此不一致 | 〔真〕本轮第一次真实运行步 4.3：`停止规则拦截（KOR）：B: 最近 3 个 closed 波 verdict 全 FAIL`；修复后 4.3 / 4.6 在规则 B 命中时 succeeded。〔码〕`campaign.py` S2 分支；`brain-make-some-gem/SKILL.md:109` |
| N17 | **P1** ✅已修 | **P0-2 初版新鲜度检查源不全、时钟不一**（本轮自身的缺口）。<br>• 没看 registry_empirical 与 `KB/operator_principle_kb`，误列了 `GLOBAL/region_kb`。<br>• toolkit `_lib/registry` 写的是 `datetime('now')`（UTC），与本地时间直接比较，东八区下刚写的行看起来早 8 小时 | 〔码〕`assemble_priors.py:97-130`（实际读取的源）、`_lib/registry.py:87-88`；〔真〕4.5b 修复后同时列出两个过期源 |
| N18 | **P1** | **priors 截断按 entry_id 字母序。** `RegistryStore.list` 按 `ORDER BY layer, entry_id` 排序，assemble-priors 再取 `[:6]` / `[:12]`。哪些死路能进 GEM，取决于 ID 的字母顺序，而不是时效或重要性。<br>S6 新封存的死路只要 ID 排在后面，**快照重组后也进不了 GEM**，这正是 P0-2 要接通的那条知识回流 | 〔码〕`_lib/registry.py:96-107`、`assemble_priors.py:236,278`。〔史〕已入库的 `kor_priors.json` 中 12/12 条 dead_end 全是 `KOR-A*`（推断真实 registry 多于 12 条、后段被截掉；本环境无生产库，无法直接核数）。〔真〕4.6：`registry dead_end 13 条 → 快照 12 条；KOR-MODEL219-DEAD 进快照? False` |
| N19 | **P1** | **`D:\` 默认路径的真实后果**（N11 的实证升级）。<br>(a) `tools/wave_gate.py --exprs-file` 按 `WQB_ROOT or WQ_PROJECT_ROOT or D:\…` 定位写库，而 `.mcp.json` 的 env 不含 WQB_ROOT。结果是在 cwd 下造出一个名为 `D:\coding\traeCN_project\wqb` 的目录和一个新库，39 条候选以 gated 写了进去。gate.py 读的是真库，找不到候选，exit 2 并提示"门禁未跑完…修复环境后重跑"。该目录被 `.gitignore` 的 `data/` 规则吞掉，`git status` 看不见。<br>(b) assemble-priors 在 `.mcp.json` 原样 env 下崩溃 rc=1（`_lib/registry` → `_lib/ledger` 默认 `D:\`）；同一进程里的 `get_store` 却按战役目录上溯找到了正确的库——一次运行两套解析。<br>(c) `_common._platform_category` 用模块常量 `_DB_PATH`（不认 WQB_DB_PATH），而 `sqlite3.connect` 会自动建库：任何一次 GEM 干跑或单测，都会在默认路径留下 0 字节的 `data/wqb.db`。<br>用户本机的仓库恰好在 `D:\coding\traeCN_project\wqb`，(a)(b) 碰巧正确。**但在同机的 worktree 或第二份克隆里，(a) 会把候选静默写进主仓库的生产库** | 〔真〕步 5 ①（杂散库里 `expressions=[('g2', 'gated', 39)]`）、4.1（rc=1）。〔码〕`tools/wave_gate.py:572-583`、`_lib/ledger.py:109-114`、`_lib/wqb_store.py:10-39`、`src/wqb/workflow/_common.py:98-108` |
| N20 | **P1** | **verdict 写入契约 vs 真实写法。** 30 条真实 verdict 原文里，契约只能归一 **6 条**（迁移工具 `classify` 能归一 11 条）。<br>两者都认不出的写法有：`no_submit`、`无提交(…)`（16 条）、`FULL_RED`、`2 GREEN + 6 RED`，以及唯一的 PASS 波 `✅ 2 RA 提交成功`。<br>`classify` 的关键词规则还会把 wave 90（IS 1.79 突破、仅 PPA 硬闸 FAIL）判成 FAIL。写入路径保持保守（拒绝，而不是按关键词猜）是对的，但 SOP 没有告诉 agent 该怎么判 | 〔真〕导入表与覆盖率表。〔码〕`wave_results_contract.normalize_verdict` vs `tools/migrate_wave_verdict_enum.classify:40-77` |
| N21 | **P1** | **gate 缓存键不含 `--datasets`。** `gate.py` 的缓存键是 `sha1(主 dataset + 表达式)`，缓存存在 `gate_cache_<主 dataset>` 下，不含合并后的数据集集合，也不含白名单 / poison 版本。<br>漏声明第二腿 → FIELD 失败被缓存 → agent 补声明重跑时 `cached=39/39`，结论不变；只有加 `--no-cache` 才得到正确的 39/39 放行 | 〔真〕步 5 ②a/②b/②c 与逐条对照。〔码〕`gate.py:517-518,1080-1093` |
| N22 | P2 | **停止规则 B 的窗口按 `updated_at` 取最近 K 个 closed 波。** 给任意旧波补记结论都会把它顶进窗口。按拒绝提示把 91c 补记为 PASS 后，窗口变成 `[91c PASS, 97, …]`，**区域停波被解除**。同理，给旧波补写 findings 也会改变窗口 | 〔真〕步 9 残留演示。〔码〕`_run_stop_rules_gate` 中的 `ORDER BY datetime(COALESCE(updated_at, created_at)) DESC` |
| N23 | P2 | **MCP 配置不可移植。** `.mcp.json`（权威）与 `mcp_config.json`（镜像）提交的都是 Windows 绝对路径，两个 server 还用了不同的 venv。换主机、换克隆路径或用 worktree，两个 server 都会 ENOENT | 〔真〕本会话启动时两个 server 均连接失败。〔码〕`.mcp.json`、`start_mcp_server.py:14-21`（它已按 `__file__` 推导路径，但只写 Windows 布局） |
| N24 | P2 | **孤儿节点与工具面。**<br>• `workflow_unified_gate` 把 `exprs_file` 只传给了 ghost-audit，没有传给 wave_gate，`from_db=False` 时必然失败。<br>• `field_understanding` 读写 `field_catalog` / `field_understanding` 两张不存在的表。<br>• wqb-db 的 7 个 `workflow_*` 没有 `dry_run`（与 wq-brain-http 的同族工具不一致）。<br>• `_flatten_platform_alpha` 被 `@mcp.tool()` 注册成了 MCP 工具 | 〔真〕步 3 / 5 真跑报错、步 0 工具清单。〔码〕`unified_gate.py:104-141`、`field_understanding.py:106,138`、`wqb_db_mcp.py:1172` |
| N25 | P2 | **静态 argv 契约只校验到 `campaign.py` 分发层。** 修复前 assemble-priors 带 dataset/wave 时干跑 success、实跑 exit 2；其它路由子命令也存在同样的盲区 | 〔真〕§14.4 与 4.0。〔码〕`_common.validate_argv`、toolkit `campaign.py:60-90` |
| N26 | P2 | **fail-open 与静默降级。**<br>• `validate_expressions` 字段预检没跑成，仍返回 `valid: true`（只挂一条 warning）。<br>• operators_catalog 的回退链不含仓库里已入库的 `docs/reference/operators_catalog.json`，新环境直接降级为手写清单（MCP 包 4 条 `test_extract_fields_*` 常红即此因）。<br>• 空库上先调只读工具，会建出空库并报 `no such table`。<br>• salvage 回填会接收没有表达式的条目 | 〔真〕步 0 / 5 / 7、MCP 包测试。〔码〕`tools_data.py:240-259` |
| N27 | P3 | **其它小项。**<br>• 质量预估在真实历史上刻度失准：预估值域 [0.72, 0.88]，实测 [−0.12, 1.91]，Pearson 0.60；5 条实测过闸者全被判 BLOCK。<br>• GEM 干跑在命令构建之前就检查含凭据的 `headless_runner/config.json`，没有配置时干跑 success=false、看不到命令（仓库自带的 `test_gem_dry_run_short_circuits` 在无配置环境常红即此因）。<br>• review_wave 的 `passes()` 把缺失的 margin 当 0 判不过，而 `walls()` 标成 `MARGIN_UNKNOWN`"不算败"，两者口径不一 | 〔真〕步 5 对照表、4.7、步 7。〔码〕`review_wave.py:30-44,113-121` |

### 14.6 价值评估的修订（第一轮 → 第二轮真实数据）

| 子项 | 第一轮判定 | 第二轮真实数据 | 修订 |
|---|---|---|---|
| 按数据集的 yield（步 1） | 保留深化 | 精确指出唯一产出集 `ml_factor_proj`（0.128 vs 其余 0） | 维持 ★★★；建议 S0 选集直接引用 |
| 停止规则 B（步 2 / 6 / 9） | 保留 | 命中与团队事后结论一致；但输入受 N20（只认得 6/30）与 N22（窗口）影响 | 保留；修 verdict 契约覆盖面与窗口定义 |
| assemble-priors + 快照（步 4） | 保留深化（P0） | 修复后闭环成立，能复现已入库产物（wins 5/6、dead_ends 12/12） | 保留；改截断策略（N18） |
| 静态闸 gate.py（步 5） | ★★★ | 两腿都声明且不走缓存：39/39 正确放行；漏声明 + 缓存：拦下全部赢家 | 保留；修缓存键（N21），FIELD 报错时点名字段所属的已知数据集 |
| 相关性代理分（步 5） | 未单列 | 对赢家原式给出 1.00，精确识别与 ACTIVE 的重复 | **新列为保留深化** |
| 质量预估（步 5） | 精简（默认关） | 39/39 BLOCK，含全部 5 条实测赢家；只有排序信息（r=0.60） | **去除 BLOCK 标签 / 重新标定**，最多作排序参考 |
| 批级多样性闸（步 5） | 保留 | 4 个历史波并成一批时 3 项不达标（不是真实单批，结论不外推） | 维持 |
| 体检硬门（步 5） | ★★★ | KOR/`ml_factor_proj` 没有体检包 → 未生效 | 保留；需要补包（enforce 档已有） |
| batch_track 作 S3 入口（步 6） | 保留（N5） | 真实"应停"区照发（含 `--submit`） | R5 升为 P1 优先项 |
| `--exprs-file` 入库即 `gated`（步 5） | N7（P1） | 三次重跑留下 117 条 gated，把积压推过 30% 上限，下一波被拦 | R7 维持 P1，并与 R21 一起修 |
| salvage 回填（步 7） | 保留 | 历史回填的条目没有表达式 | 保留；拒收无表达式条目（N26） |
| step_funnel（步 9） | 保留 | 真实瓶颈定位正确（过廉价闸 0.0206），并直接暴露 verdict 空洞 | 维持 |
| submit_verdict（步 8） | 否决权威 | 无凭据时 fail-closed | 维持 |

### 14.7 新增建议

| # | 建议 | 对应 | 优先级 |
|---|---|---|---|
| R18 ✅已实施（§14.8） | assemble-priors 截断前按时效排序（`dead_at` / `updated_at` 倒序，新结论优先），并在 `_meta` 里记录被截的条数与 id；或先按 family 去重再截 | N18 | P1 |
| R19 ✅已实施（§14.8，含 N28 补充） | DB 路径收敛（R11 升为 P1）：<br>• wave_gate / `_lib/ledger` / `_lib/registry` / `_common._platform_category` 统一改走 `resolve_db_path()`，删除 `D:\` 默认值；<br>• 只读路径用 `sqlite3.connect("file:…?mode=ro", uri=True)`，缺库时不新建；<br>• campaign / gem 节点给子进程注入 `WQB_WORKSPACE` / `WQB_ROOT` = REPO_ROOT | N19 | P1 |
| R20 ✅已实施（§14.8；建议值改用判定表规则而非 `classify`，理由见 §14.8.1） | verdict：<br>• SKILL 步 9 给出判定表：有提交 = PASS；有近闸或新基线 = PARTIAL；其余 = FAIL；<br>• 契约拒绝时在错误信息里附上 `classify` 的建议值（不自动采用）；<br>• 历史结果文件导入走同一判定表 | N20 | P1 |
| R21 ✅已实施（§14.8，含 N29 补充） | gate.py 缓存键纳入合并后的数据集集合与白名单 / poison 版本（最简做法：`--datasets` 非空时禁用缓存）；同时落实 R7（FAIL 候选回写，不再留 `gated`） | N21、N7 | P1 |
| R22 ✅已实施（§14.9；按"波的开始时刻"而非结案时刻，理由见 §14.9.1） | 规则 B 的窗口按结案时刻（`created_at`，或新增 `closed_at`）取最近 K 个，而不是按 `updated_at` | N22 | P2 → **建议升 P1**（§14.8.4） |
| R23 | 用 `start_mcp_server.py`（已按 `__file__` 推导路径）按本机生成 `.mcp.json`，仓库只留模板 | N23 | P2 |
| R24 | 孤儿节点与工具面：<br>• unified_gate 把 `exprs_file` 传给 wave_gate（或下线）；<br>• field_understanding 改读 `fields` / catalog（或下线）；<br>• wqb-db 的 `workflow_*` 补 `dry_run`；<br>• 撤掉 `_flatten_platform_alpha` 的 `@mcp.tool()` | N24 | P2 |
| R25 | `validate_argv` 对 `campaign.py <子命令>` 下钻到子脚本的 argparse 校验 | N25 | P2 |
| R26 | • 字段预检未完成时返回 `valid: null`（unverified），而不是 `valid: true`；<br>• operators_catalog 回退到已入库的 `docs/reference/operators_catalog.json`；<br>• 只读工具遇到缺表时报"库未初始化"；<br>• salvage 回填拒收没有表达式的条目 | N26 | P2 |
| R27 | • 质量预估去掉 BLOCK 标签（或按真实回测重新标定后再给标签）；<br>• GEM 干跑把 `check_config` 移到命令构建之后，缺配置只告警；<br>• review_wave 的 `passes()` 与 `walls()` 统一缺失值口径 | N27 | P3 |

### 14.8 P1（R18–R21）修复与第三轮真实环境复跑

> 审阅意见："继续修复 R18–R21 这四个 P1"，并重申第一轮的要求：逐阶段说明输入、输出与处理过程，给出价值评估，对完整流程做一次 dry-run，逐步展示每一阶段的输入输出变化与价值判断。本节是第三轮的全部结果。
> 复现命令同第二轮（附录 A）。第三轮实录现为 `realenv/realenv_transcript_r18_r21.txt`（第四轮时改名，`realenv_transcript.txt` 留给最新一轮）；第二轮实录改名为 `realenv/realenv_transcript_p0.txt`，两份同名步骤可逐行对照。
> 方法与第二轮只有一处不同：两个 server 与所有子进程的 env 一律用 `.mcp.json` 原样。第二轮给主 server 补了 `WQB_WORKSPACE`、给 wave_gate 补了 `WQB_ROOT`；R19 之后不再需要，这本身就是验证。

#### 14.8.0 一页结论

1. **四个 P1 全部修复**，并与第二轮同一调用序列逐条对照（§14.8.2）：
   - **R18**：wave97 的判死结论 `KOR-MODEL219-DEAD` 进了 GEM 快照（排第 1 位）。名额外被截掉的条目（`KOR-ACQ-MODEL-DEAD`，最早登记的那条）写进快照的 `truncated`，assemble-priors 输出里也会打印。
   - **R19**：按 `.mcp.json` 原样 env 运行，assemble-priors 从 rc=1 变成 rc=0；wave_gate 不再造杂散库，候选写进真库。
   - **R20**：真实历史里被拒的 24 条 verdict 写法，拒绝信息全部附上判定表建议（high 5 / medium 11 / low 8）。91c 的"✅ 2 RA 提交成功"得到 PASS/high。
   - **R21**：补声明 `--datasets` 后缓存不再命中（cached 从 39 降到 0），放行从 20/39 变成 39/39，与 `--no-cache` 对照组一致。门禁后逐条回写 gated 20 / fail 19。三次门禁后的积压从 117/364 = 32%（越过 30% 上限）降到 98/364 = 27%。
2. **第三轮首跑又暴露两处残缺，已一并修复**：
   - **N28**（R19 的残缺）：`gate.py` 查找工作区 `src/` 的逻辑没有随 R19 收敛。`.mcp.json` 原样 env 下 op_arity 不可达，首跑三次门禁的 117 条全部记为 `[ARITY_UNKNOWN]`，静态闸 0/39。修复后，仓库自带的 4 条常红单测转绿。
   - **N29**（R21 回写的副作用）：上面这 117 条被逐条回写成了 `fail`，把"没校验"记成了"式子坏"；而且这类结论还会进缓存。
3. **N22 从"被积压闸意外挡住"变成完全暴露。** 第二轮末尾，下一波 S2 被拦下，靠的是 N7 虚高的积压（32%）。修掉 N7 后，积压 27% 不再拦截。此时按 R20 的建议补记旧波 91c=PASS，规则 B 的窗口变成 `[91c PASS, 97, s2_…]`，**KOR 的停波被解除，下一波 S2 放行**。R20 让补记更容易，R22 应随之升为 P1（§14.8.4）。
4. **回归**：根测试 1137 passed / 17 failed（基线 1096 / 21）。失败集合是基线的真子集，没有新增失败；转绿的 4 条正是 N28。MCP 包 77 / 5，与修复前一致。

#### 14.8.1 修复内容

| 项 | 改动 | 文件 |
|---|---|---|
| R18 新登记优先 + 截断可见 | • `RegistryStore.list(newest_first=True)` 按登记先后（id 自增）倒序；默认的字母序保留给 CLI 展示。<br>• assemble-priors 截断前记下名额外的条目，写入 `_meta.truncated` 与快照的 `truncated`。<br>• CLI 打印 `truncated dead_ends: 名额外 N 条未注入（新登记优先保留）`；`restore_from_db` 保留该字段 | `_lib/registry.py`、`assemble_priors.py` |
| R19 库路径收敛 | toolkit 新增 `wqb_store.resolve_db_path(ctx)`，优先级：`WQB_DB_PATH` > 战役目录上溯 > `WQB_WORKSPACE` > `WQB_ROOT` > `WQ_PROJECT_ROOT` > toolkit 自身上溯 > cwd 上溯 > 历史盘符（仅当它真实存在）。<br>`_lib/ledger`、`_lib/registry`、`_lib/wave_results` 与 `get_store` 共用这一解析（此前同一次 assemble-priors 会读两个库）；build_wave / pipeline / review_wave / assemble_priors 改为传 ctx | `_lib/wqb_store.py`、`_lib/ledger.py`、`_lib/registry.py`、`_lib/wave_results.py`、`assemble_priors.py`、`build_wave.py`、`pipeline.py`、`review_wave.py` |
| | `tools/wave_gate.py` 里 7 处 `WQB_ROOT or WQ_PROJECT_ROOT or D:\…` 收敛为 `_wqb_root()` / `_wqb_db_path()`：战役目录上溯优先，并认 `WQB_DB_PATH` | `tools/wave_gate.py` |
| | • `_common._platform_category` 改走 `resolve_db_path()`，以只读 URI 打开（缺库时不再建空库）。<br>• `unbuffered_env` 缺省注入 `WQB_WORKSPACE=REPO_ROOT`（不覆盖已有值）。<br>• `WorkflowExecutor` 的默认库路径改为绝对路径 | `src/wqb/workflow/_common.py`、`executor.py` |
| | **N28 补充**：`gate.py` 的 `_workspace_src_dirs` / `_find_tools_lib` 改用同一套工作区候选（历史变量 `WQB_WORKSPACE_ROOT` 保留为最高优先）；`main()` 拿到战役目录后，再解析一次模块加载时没找到的依赖（op_arity、家族天花板、vector_wrap） | `gate.py` |
| R20 判定表 + 拒绝建议 | • 契约新增 `VERDICT_TABLE`、`verdict_from_counts`、`suggest_verdict`。<br>• 被拒时，错误信息附上判定表与建议（依据 + 置信度），返回体带 `suggestion`。**不自动采用、不写库。**<br>• SKILL 步 9 写入判定表与补记注意事项。<br>建议值用判定表规则，没有照搬 §14.7 所写的 `classify`：`classify` 的关键词规则把 87 / 88 / 90（NEAR、IS 1.79 突破）判成 FAIL，按判定表应是 PARTIAL。<br>"历史结果导入走同一判定表"只提供了 `verdict_from_counts`，**没有改写任何导入工具**：本演练的导入策略仍是"被拒即以 open 落库" | `src/wqb/wave_results_contract.py`、`wqb_db_mcp.py`（docstring）、SKILL.md |
| R21 缓存键 + 逐条回写 | `gate.py` 的缓存键改为 sha1(主 dataset, 闸门签名, 表达式)。签名覆盖数据集集合、合并白名单、字段类型、banned、poison 与平台约束；报告逐条带原式 `expr` | `gate.py` |
| | wave_gate 的 `--exprs-file` 先以 `pending` 入库，再按逐条结论回写 `gated` / `fail`（reason 记闸门原因）；报告新增 `state_writeback` | `tools/wave_gate.py` |
| | **N29 补充**：只因闸门环境缺失而判 FAIL 的条目保持 `pending`，FAIL 行点明"不是表达式问题"；gate.py 不缓存 `[*_UNKNOWN]` 结论 | `tools/wave_gate.py`、`gate.py` |
| 演练脚本 | 每步打印【阶段小结】；server 与子进程的 env 改为 `.mcp.json` 原样；末尾输出 P1 验证清单，与第二轮同名步骤对照 | `realenv/run_realenv.py` |
| 测试 | `tests/unit/test_p1_fixes_20260927.py` 共 16 条：R18 ×3、R19 ×8（含 N28 ×2）、R20 ×3、R21 ×2（含 N29）。其中两条端到端：<br>• wave_gate 配桩 gate.py 回写 gated / fail / pending；<br>• toolkit 按"安装位拷贝"布局真跑 gate.py：无 env 时 `[ARITY_UNKNOWN]` 且不入缓存，有 `WQB_WORKSPACE` 时放行并入缓存 | |

#### 14.8.2 第二轮 vs 第三轮（同一份导入后真实库、同一调用序列）

| 场景 | 第二轮（P0 修复后） | 第三轮（P1 修复后） | 对应 |
|---|---|---|---|
| 4.1 assemble-priors，`.mcp.json` 原样 env | 崩溃 rc=1（`_lib/registry` → `_lib/ledger` 默认走 `D:\`） | rc=0，快照写入 | R19 |
| 4.6 `seal_dead_end(KOR-MODEL219-DEAD)` 后重组快照 | 13 条按字母序截成 12 条，新死路**进不了**快照；截断没有记录 | 进快照（第 1 位）；`truncated={'dead_ends': ['KOR-ACQ-MODEL-DEAD']}`，assemble-priors 打印截断行 | R18 |
| 导入时被拒的 24 条 verdict | 拒绝信息只有"必须是 PASS/FAIL/PARTIAL" | 全部附判定表建议：FAIL/low 8、PARTIAL/medium 10、FAIL/medium 1、PASS/high 2、FAIL/high 3 | R20 |
| 步 5 ①：wave_gate 只声明主集（`.mcp.json` env） | 候选写进仓库根的杂散库，gate.py exit 2 | 写进真库。放行 20/39；FIELD 拦下 19 条（实测均值 1.29，含全部 5 条赢家）。回写 gated 20 / fail 19；没有杂散目录 | R19、R7 |
| 步 5 ②：补声明 `--datasets`（默认缓存） | cached 39/39，放行 20/39 | cached 0/39，放行 39/39 | R21 |
| 步 5 ③：`--no-cache` 对照组 | 39/39 | 39/39 | — |
| 三次门禁后的状态与积压 | 117 条全记 `gated`（其中 38 条是 FIELD 失败）；积压 117/364 = 32% > 30% | gated 98 / fail 19；积压 98/364 = 27% | R7 |
| 步 9：按建议补记 91c=PASS 后的下一波 S2 | 规则 B 放行，但被积压闸拦下（32%） | 规则 B 与积压闸都放行 → **S2 success=True** | N22 暴露（§14.8.4） |

#### 14.8.3 逐阶段：输入 → 处理 → 输出变化 → 价值判定（第三轮）

与实录中每步末尾的【阶段小结】一一对应；数字全部取自该次运行。

| 步 | 输入（真实） | 处理 | 输出变化（第三轮实测） | 价值判定 |
|---|---|---|---|---|
| 0 环境基线 | `.mcp.json` 的两个 server；工作树；默认库路径为空 | 路径翻译后经 stdio 启动（env = `.mcp.json` 原样）；列工具；读启动 stderr | wqb-db 45 个工具 / wq-brain-http 69 个；启动告警 4 条；空库上先调只读工具 → `no such table`，并在默认路径留下空库 | 演练前提，不评星。N23 / N24 / N26 仍在（P2） |
| 导入 | 38 个结果文件（335 行、30 条 verdict 原文）；priors；两份字段目录 | 逐行 `upsert_backtest_rows`；verdict 走写入契约，被拒则以 open 落库；KB 反推 | 247/335 行入库。verdict：6 条 closed/FAIL；24 条被拒，全部附建议；8 个文件没有 verdict | ★★★ 契约 + 建议：不替人猜结论，也不让人卡在"该写什么" |
| 1 S-PRE | 导入后的 KOR 库 | summary / dead_ends / mining_yield（strict、by_dataset）/ dead_datasets / wave_results；inventory_scan；recommend_datasets | 严格 yield 5/247 = 0.0202。按数据集只有 `ml_factor_proj`（5/39）有产出，其余 5 个为 0。30 波 / 6 closed / 12 dead_ends。inventory_scan 真跑与 recommend_datasets 因无凭据失败 | ★★★ 保留深化：按数据集的 yield 一步定位唯一产出集，S0 选集应直接引用；inventory_scan 未入 SOP（N13） |
| 2 S0 | 战役目录 + 库 | S0 calibrate / score 命令构建（干跑）；区域四闸（warn） | 命令构建成功。catalog / signal_floor / backlog 放行，stop_rules 命中 B（95/96/97）；warn 模式下 ok=True | ★★★ 停止规则 B 的判断与团队事后结论一致；warn 灰度看得见、拦不住（R5 待办） |
| 3 S1 | `ml_factor_proj` 的 333 字段目录 | S1 / FE 干跑；typed catalog；前缀聚类；field_understanding | 全部 MATRIX；前缀簇 3 个（change 253 / log 40 / mean 40）；field_understanding 真跑 → `no such table: field_catalog` | ★★ typed catalog 保留；field_understanding ✂ 下线候选（N24） |
| 4 S2 | region_kb（3 条 win，含演练追加的 1 条）+ registry（dead_end 13 / win 3，含新封存的 1 条）+ template_kb | assemble-priors 真跑 3 次；GEM 干跑 5 次；模拟 S6 回写；pregate 预闸 39 条 | • 4.1 rc=0。<br>• GEM 快照检查依次为：缺失 → 新鲜 → 过期（region_kb）→ 过期（region_kb + registry）→ 新鲜。<br>• 4.6 快照含新 win 与 KOR-MODEL219-DEAD，截断 1 条且可见。<br>• pregate 39 → 39（1 处窗口归一） | ★★★ 保留深化：S6→S2 回流闭环，R18 后新判死结论能进 GEM；GEM 真跑仍需 `config.json`（N27） |
| 5 S2→S3 | 39 条真实表达式（含 5 条实测过闸者，其中 2 条是 ACTIVE 原式）；两份字段目录 | ghost-audit → wave_gate 的三种调用（§14.8.2） | ① 20/39，回写 gated 20 / fail 19；② cached 0、39/39；③ 39/39；积压 27%；质量预估 39/39 BLOCK；`[opcat] FAIL` 仍只打印 | 静态闸 ★★★；逐条回写修正了 gated 的语义；质量预估 ✗（R27）；`[opcat]` ✂（R6）；体检硬门缺包、未生效 |
| 6 S3 | 门禁后的 g2；规则 B 命中 | batch_track 干跑 vs campaign S3 干跑 | batch_track 的命令含 `--submit`、没有区域闸，success；campaign S3 被规则 B 拦下 | ★★ 保留；N5 仍在（R5，P1 待办） |
| 7 S4 | wave 94；thresholds；candidates | S4 干跑；按波 / 按 sharpe 检索；salvage 回填；review_wave 判定函数 | 解析出 9 个 alpha；salvage 处理 34 个文件、6 个成功，池内 24 条全都没有表达式；5/6 条 walls 只有 MARGIN_UNKNOWN，却 passes=False | ★★★ 墙诊断保留；N26 / N27 / N4 待办 |
| 8 S4→S5 | 88lr21xo / 78jQ29rL；无凭据 | submit_ready；submit_verdict；judge / submit_alpha 干跑 | submit_ready=[]；submit_verdict 无凭据时 fail-closed；submit_alpha 干跑 submitted=False（确认与否都不触平台） | ★★★ 否决链与确认门保留；N3 / N8 待办 |
| 9 S6 | wave_results（6 closed / 24 open）；规则 B 窗口 97/96/95；91c 的建议 PASS/high | P0-1 回放；assemble-priors + GEM 检查；按建议补记 91c；step_funnel；auto_pyramid | • 只补 key_findings 后 verdict 保持 FAIL，规则 B 仍拦；空壳结案被拒。<br>• 补记 91c 后窗口为 `[91c PASS, 97, s2_…]` → 规则 B 放行，下一波 S2 success=True（积压 27%）。<br>• 漏斗瓶颈："回测完成 → 过廉价闸"，保留率 0.0206 | ★★★ P0-1 契约有效；N22 完全暴露，R22 建议升 P1 |
| 附 A | 19 个节点 × `workflow_execute(dry_run=True)` | 经 MCP 全量扫描 | 17/19 成功且零副作用；失败的是 gem（缺 config.json）与 hypothesis_round（测试参数下没有假设目录） | 干跑契约在真实服务上成立 |

#### 14.8.4 第三轮新发现与残留

| # | 级别 | 发现 | 证据 |
|---|---|---|---|
| N28 | **P1** ✅已修 | **gate.py 查找工作区 `src/` 的逻辑没有随 R19 收敛。** 该目录提供 op_arity 元数检查、家族天花板与 vector_wrap。原先的候选顺序是 `WQB_WORKSPACE_ROOT / WQB_ROOT / WQ_PROJECT_ROOT` > "本目录上溯 5 级" > 硬编码 `D:\`：<br>• "上溯 5 级"在仓库内布局落到仓库的上一级。build_wave 在 09-09 修过同一个 off-by-one，gate.py 没有跟进。<br>• `.mcp.json` 不设这三个变量；节点注入的是 `WQB_WORKSPACE`，gate.py 又不认。<br>结果是 op_arity 不可达，**每条表达式都记 `[ARITY_UNKNOWN]` 并判 FAIL**。第三轮首跑的三次门禁，117 条全部如此，静态闸 0/39。<br>用户本机的仓库恰好在 `D:\…`，所以碰巧正确；worktree、第二份克隆或其它机器上必现。第二轮演练给 wave_gate 补了 `WQB_ROOT`，因此没暴露。<br>仓库自带的 `test_window_whitelist_p4` 3 条与 `test_gem_provenance_p1p2p3::test_window_warning_does_not_block` 常红，就是这个原因：HEAD 上 `check_one` 返回 `[ARITY_UNKNOWN]`，修复后转绿 | 〔真〕第三轮首跑步 5：`passed=0/39`，拦截理由 `{'ARITY_UNKNOWN': 39, 'FIELD': 19}`。〔码〕`gate.py` 的 `_workspace_src_dirs` |
| N29 | P2 ✅已修 | **R21 的逐条回写把环境问题记成表达式问题。** 上面 117 条被写成 `fail`（reason 为 "gate FAIL: [ARITY_UNKNOWN] …"），build_wave / 去重从此不再重选它们。这些结论还进了逐条缓存，环境修好后仍会被复用 | 〔真〕首跑 `[state] 逐条状态回写：gated 0 / fail 39`。〔码〕gate.py 的缓存写入原本无条件 |
| N22 | P2 → **建议升 P1** | **规则 B 的窗口问题完全暴露。** 第二轮末尾下一波 S2 被积压闸拦下，而那份积压来自 N7（FAIL 候选也记 gated）。修掉 N7 后积压 27%，不再拦截。此时按 R20 的建议补记旧波 91c=PASS（91c 早于 92–97），窗口变成 `[91c PASS, 97, s2_…]`，KOR 停波被解除，下一波 S2 放行。<br>R20 让"补记旧波"更容易（SKILL 步 9 已提示补记会改变窗口），R22 应随之升为 P1 | 〔真〕步 9 |
| 仍待办 | — | P1：R3（Failed-count 单一实现）、R4（near 池排除 RN_EXPOSURE）、R5（batch_track 接区域闸）、R6（`[opcat]` 降为 INFO）、R8（提交判定定位），以及建议升级的 R22。其余 P2 / P3 见 §13 / §14.7 | — |

#### 14.8.5 回归与同步

- **根测试**：1137 passed / 17 failed / 21 skipped（基线 1096 / 21）。失败集合是基线的真子集，没有新增失败；转绿的 4 条就是 N28。新增的 16 条 P1 用例已计入。
- **MCP 包**：77 / 5，与修复前一致。
- **pyflakes**：改动文件的告警与 HEAD 逐条相同，都是既有的未用变量 / 无占位 f-string。
- **技能同步**：`tools/sync_skills.py --check` 报 281 个文件 MISSING，因为本容器的 `~/.claude/skills` 不是用户的安装位（基线状态）。toolkit 的 `gate.py`、`assemble_priors.py`、`_lib/*` 都是技能源码，**需要在本机跑 `python tools/sync_skills.py` 同步到安装位后才生效**。
- **SKILL 元数据**：`wq-brain-ra-pipeline/SKILL.md` 的 `last_verified` 已随步 9 的改动更新为 2026-09-27（`test_last_verified_not_older_than_last_commit` 的要求）。
- **第三轮共跑 3 遍**：
  - 第 1 遍暴露 N28 / N29；
  - 第 2 遍（修复后）四项全部达标；
  - 第 3 遍把积压改为"三次门禁后按库统计"，即附件实录。
  - 第 2、3 遍去掉时间戳后比对，差异只剩毫秒与字典键序。

### 14.9 P1 第二批（R22 / R5 / R12 / R4 / R3）修复与第四轮真实环境复跑

> 审阅意见："按建议修 R22、R5、R12、R4、R3"。本节是第四轮的全部结果。
> 复现命令同附录 A。实录 `realenv/realenv_transcript.txt` 是第四轮；第三轮实录改名为 `realenv/realenv_transcript_r18_r21.txt`。第二批各项对照第三轮的同名步骤（步 5–9、附 A），第一批（R18–R21）继续对照第二轮，作为回归护栏。
> 方法同第三轮（env = `.mcp.json` 原样）。新增探针：步 5 ④⑤⑥（R12；写入指到演练库的副本，不改变步 6–9 的区域状态）、步 6（R5）、步 7（R4）、步 8（R3）、步 9 把"旧取法"与"闸的实际窗口"并列打印（R22）。验证清单改为三态：✅ 真实环境验证通过 / ❌ 与预期不符 / ➖ 真实数据无触发样本、靠单测。

#### 14.9.0 一页结论

1. **五项全部修复，真实环境验证清单 8 ✅ + 1 ➖**（第一批 4 项回归无恙）：
   - **R22**：按建议补记旧波 91c=PASS 之后，按 `updated_at` 的旧取法仍是 `[91c, 97, s2_…]`，但闸的实际窗口按波的开始时刻取为 `[s2_…, 97, 96]` → **规则 B 维持拦截，下一波 S2 被拦**。第三轮这里是放行（N22）。
   - **R5**：`workflow_batch_track` 干跑 success=False，闸 `{signal_floor ✓, stop_rules ✗}`，与 campaign S3 同一结果；被拦时仍带回将要执行的命令（含 `--submit`）。附 A 里 batch_track 从"成功"变成"带原因的失败"，全部 3 个失败节点都有 error，没有静默失败。
   - **R12**：env 去掉 `WQ_TOOLKIT_DIR` / `WQ_VALIDATOR_DIR`（= wqb-db server 的 env 形态），wave_gate 自己找到 toolkit 与 verifier，放行 39/39（与对照组一致）、环境缺失标记 0；verifier 缺 ply → exit 2 + `门禁环境缺失`；probe_batch_mode 干跑 exit 0。同一 env 下第三轮代码：前者抛 `FileNotFoundError`（只搜 qoder-cn / cursor / workbuddy）、后者 exit 1，两者都会被读成"表达式不合格"。`ply` 已写进 requirements。
   - **R4**：**仓库真实数据里没有触发样本。** 带 `rn_sharpe` 的真实评审行 119 条（GBR / MEA / USA），其中 35 条 RN_EXPOSURE，raw sharpe 最高 0.51，全部在 near（1.0–1.2）与组合（1.0）线之下——修复前后池子一致，新池里 RN_EXPOSURE 0 条。R4 是防御性修复，效果由单测（构造行）守；真实环境对它给 ➖ 而不是 ✅。
   - **R3**：同一组 N3 checks，mcp_core 仓库布局（`source=wqb.config`）与镜像布局（屏蔽 `wqb` 包，走冻结副本）都得 failed_ra/ppa = 3/1，与 `wqb.config` 相同；修复前副本实测 mcp_core 3/1、`wqb.config` 0/0。
2. **验证中顺手修的两处**（都是本批修复让测试"走得更远"才暴露）：
   - `tools/probe_batch_mode.py::_wqb_store()` 写死 `<repo>/data/wqb.db`、不认 `WQB_DB_PATH`（R19 的漏网）。R12 让 `test_probe_batch_mode_b_distribution_mode` 找得到 toolkit 之后，这条单测会在默认路径上初始化 CampaignStore——在用户本机就是生产库（建表 / 迁移）。改为 `CampaignStore()`（走 `default_db_path()`，`WQB_DB_PATH` 优先），单测指到临时库。
   - S4 的 `_resolve_wave_alpha_ids` 纯读却用 `sqlite3.connect`，缺库时悄悄建空库（dry-run 也走这条路）。改为只读打开，与 R5 的开波闸共用 `connect_db_readonly`。
3. **新记 N30（P1，未修）**：wqb-db 收批级联绕过写入契约、把字符串波号截成数字（§14.9.4）。
4. **回归**：根测试 1239 passed / 13 failed / 15 skipped，失败集合是上一批（17 条）的真子集，没有新增失败。转绿 4 条：N12 的 3 条（R12）+ `test_sync_skills_reports_no_drift`（同步 skills 后）。MCP 包 78 / 5，失败集合与 HEAD 相同（§14.9.6）。

#### 14.9.1 修复内容

| 项 | 改动 | 文件 |
|---|---|---|
| R22 规则 B 窗口按波的开始时刻 | `_recent_closed_waves(conn, region, k)`：closed 波按"开始时刻"倒序取 K 个。<br>• 有表达式的波取 `waves.created_at` 的最早值（按 region 名关联）；<br>• 纯探针 / 只有结论行的波取 `wave_results.created_at`；<br>• 两种写入方的时钟（本地 isoformat 与 SQLite UTC）经 `local_ts` 统一成本地时间再比；同刻按波号数字部分倒序；<br>• 最小库（无 waves / regions 表）退回结论行时间。<br>闸的 evidence 新增 `recent_closed_waves`。补记旧波、补写 findings 都不再改变窗口。<br>**为什么是开始时刻而不是 §14.7 写的"结案时刻"**：补记旧波正是"现在结案一个旧波"，按结案时刻它照样会被顶进窗口；规则 B 问的是"最近 K 次实验是否全灭"，实验的先后由开始时刻决定 | `src/wqb/workflow/nodes/campaign.py`；`_common.py`（`local_ts` 由 gem 节点的快照新鲜度检查提升为公共函数） |
| R5 batch_track 过三道开波闸 | 新公共函数 `run_open_wave_gates(region, dataset, campaign_dir)`：signal_floor → stop_rules → backlog，首个拦截即停；campaign S2/S3 与 batch_track 共用。<br>batch_track 在拼好命令之后、dry-run 返回与真跑之前调用；被拦时返回 success=False + error，并带回命令与闸步骤。<br>三道闸改为只读打开库（`connect_db_readonly`），缺库不再建空库。<br>SOP 的"快捷入口"与步 6 注明 batch_track 同样过闸 | `campaign.py`、`batch_track.py`、`_common.py`、ra-pipeline SKILL.md |
| R12 tools/ 下 CLI 的 skill 解析 + 环境缺失 exit 2 | 新增 `tools/skill_paths.py`：`skill_roots()` 委托 `wqb.workflow._common._skill_roots`，与 workflow 节点同一顺序（WQ_SKILLS_DIR → APPDATA Claude → ~/.claude → ~/.codex → qoder-cn / cursor / workbuddy → 仓库 `Claude/skills`）；wave_gate / probe_batch_mode / pre_backtest_filter 改用它。<br>wave_gate 新增 `env_error_exit`：verifier 找不到或 import 失败（缺 ply 时它打印提示后 `sys.exit(1)`）、gate.py 找不到 → `[done ] ERROR: 门禁环境缺失 …`，exit 2。此前未捕获的 `FileNotFoundError` / `SystemExit` 都是 exit 1。<br>`ply>=3.11,<4.0` 写进 requirements | `tools/skill_paths.py`、`tools/wave_gate.py`、`tools/probe_batch_mode.py`、`tools/pre_backtest_filter.py`、`world-quant-brain-mcp/requirements.txt` |
| R4 near / salvage 排除 RN_EXPOSURE | review_wave 新增 `near_block_wall(r, t, t_near)`（返回 ROBUST_STRUCTURAL / RN_EXPOSURE / None）与 `report_near_exclusions`。near 循环与 `combo_candidate` 都排除 RN_EXPOSURE（组合候选也会进 salvage_pool，§13.2 的原建议只覆盖了 near）；pipeline 的 review 阶段调用同一判据 | toolkit `review_wave.py`、`pipeline.py`；两份 SKILL.md |
| R3 Failed-count 单一实现 | `src/wqb/config.py` 成为唯一实现：RA 18 项 / PPA 7 项名单、`check_counts_as_failed`（非 PASS 且非 PENDING 即计失败）、`compute_webdata_failed_counts`（替换旧的分叉实现：只数 FAIL、名单缺 3 项、含平台不存在的项）。<br>mcp_core 在仓库布局下直接引用；Docker 镜像只打包 MCP 目录，回落到冻结副本，`FAILED_COUNT_SOURCE` 标明来源。build_gate_prior 改为 import | `src/wqb/config.py`、`world-quant-brain-mcp/mcp_core.py`、`tools/build_gate_prior_from_inventory.py` |
| 验证中顺手修 | probe_batch_mode `_wqb_store()` 认 `WQB_DB_PATH`；S4 `_resolve_wave_alpha_ids` 只读打开；`test_probe_batch_mode_b_distribution_mode` 指到临时库 | `tools/probe_batch_mode.py`、`campaign.py`、`tests/unit/test_workflow_nodes.py` |
| 测试 | • `tests/unit/test_p1_batch2_20260927.py` 16 条：R22 ×4（补记旧波、无表达式探针波、UTC / 本地时钟混比、最小库）、R5 ×5（干跑被拦、真跑在 Popen 前被拦、放行时报三闸且与 S2/S3 同一函数、开波闸与 S4 解析都不建库）、R12 ×4、R4 ×3。<br>• `tests/unit/test_r3_failed_count_single_source.py` 12 条：用 AST 执行 mcp_core 的 `except ImportError` 分支，逐项对照冻结副本与 `wqb.config`；N3 回归；build_gate_prior 引用同一对象。<br>• MCP 包 +1：仓库布局下 `FAILED_COUNT_SOURCE == "wqb.config"`。<br>• 两条"顺手修"的用例在修复前均失败（已回退验证） | |
| 演练脚本 | 新增探针（见本节开头）；清单三态；probe_batch_mode 干跑写进 `tracking/KOR/cache/` 的结果文件由演练删除 | `realenv/run_realenv.py`、`reproduce_realenv.sh` |

#### 14.9.2 第三轮 vs 第四轮（同一份导入后真实库、同一调用序列）

| 场景 | 第三轮 | 第四轮 | 对应 |
|---|---|---|---|
| 步 9：按建议补记 91c=PASS 后的下一波 S2 | 窗口（按 updated_at）`[91c PASS, 97, s2_…]` → 规则 B 放行，**S2 success=True** | 旧取法仍是 `[91c, 97, s2_…]`；闸的实际窗口 `[s2_…, 97, 96]` → 规则 B 拦截，S2 success=False（积压闸未执行：首个拦截即停） | R22 |
| 步 6：batch_track 干跑（KOR，规则 B 命中） | success=True，没有区域闸，命令含 `--submit` | success=False，闸 `{signal_floor ✓, stop_rules ✗}`（与 S3 相同），error=停止规则拦截…，仍带回命令 | R5 |
| 附 A：19 节点干跑 | 17/19；batch_track 成功 | 16/19；batch_track 带原因失败；无静默失败、无副作用 | R5 |
| wave_gate，env 无 `WQ_TOOLKIT_DIR` / `WQ_VALIDATOR_DIR` | 第三轮代码（`8921a3a` 导出副本）同 env 实测：`FileNotFoundError: 未找到 validator.py`（已搜 qoder-cn / cursor / workbuddy），exit 1 | 放行 39/39（= 对照组 ③），环境缺失标记 0；exit 1 与 ③ 相同（gate.py 批级多样性闸：这 39 条历史式结构同质，属正常判定） | R12 |
| wave_gate，verifier 缺 ply | 第三轮代码实测：打印"需要安装PLY库"后 exit 1 | exit 2，`[done ] ERROR: 门禁环境缺失 —— … 不是表达式问题` | R12 |
| probe_batch_mode `--dry-run`，env 无 `WQ_TOOLKIT_DIR` | 找不到 toolkit（本机 N12 单测红） | exit 0，DRY_RUN | R12 |
| RN_EXPOSURE 真实行进 near / salvage | 第三轮未实测 | 119 行中 35 条 RN_EXPOSURE，raw sharpe 最高 0.51，修复前后都不进池（无触发样本） | R4 |
| N3 checks 的失败计数 | mcp_core 3/1，`wqb.config` 0/0（口径相反） | 仓库布局 3/1（`wqb.config`）、镜像布局 3/1（冻结副本）、`wqb.config` 3/1 | R3 |

#### 14.9.3 逐阶段：输入 → 处理 → 输出变化 → 价值判定（第四轮）

与实录中每步末尾的【阶段小结】一一对应；步 0–4 与第三轮逐项相同（见 §14.8.3），只列有变化的步骤。

| 步 | 输入（真实） | 处理 | 输出变化（第四轮实测） | 价值判定 |
|---|---|---|---|---|
| 2 S0 | 同第三轮 | 同第三轮 + 打印 CLI 的缺省模式 | 同第三轮：四闸中 stop_rules 命中 B，warn 模式下 ok=True；CLI 缺省 warn（灰度期至 2026-10-11） | ★★★ 不变。toolkit CLI 侧缺省 warn，2026-10-12 起缺省 enforce（§14.9.7）；SOP 的 workflow 入口一律 enforce（R5） |
| 5 S2→S3 | 39 条真实表达式（含 5 条实测过闸者，其中 2 条 ACTIVE 原式）；两份字段目录 | ① ② ③ 同第三轮；R12 探针 ④ 无 `WQ_*` 目录变量、⑤ 假 verifier 缺 ply、⑥ probe_batch_mode 干跑（写入均指到库副本） | ①–③ 与第三轮一致（20/39 → 39/39 → 39/39，积压 27%）；④ 39/39、环境缺失 0；⑤ exit 2；⑥ exit 0 | 静态闸 ★★★；R12 后门禁不再依赖 `WQ_*` 变量，环境问题与表达式问题退出码分开 |
| 6 S3 | 门禁后的 g2；规则 B 命中 | batch_track 干跑 vs campaign S3 干跑 | 两者同被停止规则拦下；batch_track 仍带回命令 | ★★ 保留；N5 已修 |
| 7 S4 | wave 94；thresholds；candidates；R4 探针：119 条带 rn_sharpe 的真实评审行 | 同第三轮 + near / combo 判据新旧对照 | 同第三轮（N26 / N27 仍在）；R4 无触发样本 | ★★★ 墙诊断保留；R4 防御性 |
| 8 S4→S5 | 同第三轮；R3 探针：N3 checks | 同第三轮 + mcp_core 两种布局对照 | 同第三轮；R3 两种布局与 `wqb.config` 同为 3/1 | ★★★ 否决链与确认门保留；N3 已修，N8 仍待办 |
| 9 S6 | wave_results（6 closed / 24 open）；按 updated_at 的最近 3 个 closed 波 97/96/95；91c 建议 PASS/high | 同第三轮 | P0-1 回放同第三轮；补记 91c 后规则 B 维持拦截（实际窗口 `[s2_…, 97, 96]`）；step_funnel verdict 分布 (空)=23 / FAIL=7 / PASS=1 | ★★★ P0-1 契约 + R22：补记不再能解除停波 |
| 附 A | 19 个节点 × `workflow_execute(dry_run=True)` | 经 MCP 全量扫描 | 16/19 成功；失败的 batch_track（停止规则）/ gem（缺 config.json）/ hypothesis_round（测试参数下无假设目录）都带 error；零副作用 | 干跑契约成立；"失败必须带得出原因"成立 |

#### 14.9.4 新发现与残留

| # | 级别 | 发现 | 证据 |
|---|---|---|---|
| N30 | **P1** 未修 | **收批级联绕过写入契约。** `harvest_multisim_results`（ra-pipeline SKILL.md:405 的手动补收入口）收批后调 `_cascade_wave_result`：<br>• 波号用 `int(re.search(r"(\d+)", wave))` 取：`s2_<ds>_d1` → **2**、`91c` → 91。于是 GEM 标签波的收批结果写进"第 2 波"那一行；该行不存在时 INSERT 一条 closed 行，按 R22 它以"现在"为开始时刻进入规则 B 窗口。<br>• verdict 写成 `"N/M 过硬闸, 新高 X"`，直接 UPDATE（覆盖已有 verdict，包括人按判定表写的枚举值），不经 P0-1 契约的归一与合并。<br>• 两个归一器对这种写法不一致：停止闸的 `_normalize_verdict` 给 `3/8 过硬闸` 判 PARTIAL，写入契约的 `normalize_verdict` 判 PASS（`0/8` 两边都是 FAIL）。对规则 B 的结论相同，但同一文本两种枚举。<br>建议：级联改走契约写入口，波号保留原字符串；verdict 用 `verdict_from_counts`（R20）得到枚举值，且只在该波没有 verdict 时填写 | 〔码〕`wqb_db_mcp.py:1454-1525`（`_cascade_wave_result`），调用点 `:1389`；〔码〕两个归一器的实测输出 |
| R22 的边界 | 说明 | 库里从未出现过的旧波（无 `waves` 行、也无旧结论行）第一次补记时，`created_at` 就是"现在"，仍会进窗口。库里没有它的真实开始时刻，只能靠补记方带上（后续可给 `upsert_wave_result` 加 `started_at`）。本演练的 91c 在导入时已有结论行，不受影响 | 〔码〕`_recent_closed_waves` |
| R19 漏网 | P2 | `campaign._ensure_campaign_config` 仍写死 `<repo>/data/wqb.db`，不认 `WQB_DB_PATH`。本批没有测试走到它，未改 | 〔码〕`campaign.py` `_ensure_campaign_config` |
| N11 残留 | P2 | 仍有 49 个文件含 `traeCN_project` 硬编码路径，典型如 `modeb_improve.py` 的 `DB = r'D:\coding\traeCN_project\wqb\data\wqb.db'`、GEM 脚本、`_lib/slots.py`、`tools/campaign_intel.py`、`.mcp.json` | 〔码〕grep |
| 干跑副作用 | P3 | `probe_batch_mode.py --dry-run` 仍把结果写进战役目录 `cache/`（gitignored，所以 Probe 与 `git status` 都看不见） | 〔真〕第四轮步 5 ⑥ |
| 仍待办 | — | P1：R6（`[opcat]` 降为 INFO）、R8（提交判定定位）、N30。R5 里"CLI warn 灰度写明截止日期"一项已定：2026-10-11 截止（§14.9.7）。其余 P2 / P3 见 §13 / §14.7 | — |

#### 14.9.5 价值评估的修订（第二批）

| 项 | 实测价值 | 依据 |
|---|---|---|
| R22 | **高** | 真实历史上"补记一个旧波就解除停波"可复现（第三轮），修复后同一序列维持拦截；规则 B 是 SOP 里唯一的止损机制 |
| R5 | **高** | SOP 指定的发批入口第一次和 S3 同过三闸；KOR 当前正处于规则 B 命中状态，修复前照样发批 |
| R12 | 中高 | 门禁不再依赖 `.mcp.json` 之外的环境变量；环境故障（exit 2）与表达式不合格（exit 1）分开，调用方终于能区分"修环境"与"改式子"；本机 3 条常红单测转绿 |
| R3 | 中 | 生产口径本来就对（mcp_core），修复前的分叉实现只被单测引用；价值在于拆掉"照 AGENTS.md 引用唯一事实源反而踩坑"的陷阱 |
| R4 | 低（本仓库数据） | 真实数据无触发样本：RN_EXPOSURE 行的 raw sharpe 都低于 near / 组合线。改动小、无副作用，作为防御保留；若某区出现"raw 高但 RN≤0"的行（`rn_exposure` 文档里的 HKG w4 实证不在本仓库），它才开始起作用 |

#### 14.9.6 回归与同步

- **根测试**：1239 passed / 13 failed / 15 skipped（上一批记录 1137 / 17 / 21）。
  - 失败集合是上一批的真子集，没有新增失败。13 条都是既有问题：7 条缺 gitignored 的 `data/operators_verified.json`、2 条缺 `attic/`、2 条是本容器自带的非项目 skill 目录（`synced` / `session-start-hook`）、`test_campaign_stage_route_matrix` 需要 USA 回测数据、`test_gem_dry_run_short_circuits`（N27）。
  - 转绿 4 条：N12 的 3 条（R12）与 `test_sync_skills_reports_no_drift`（同步 skills 后）。
  - 少掉的 6 个 skip 现在都跑且通过：`test_wave_gate_terminal_states` 3 条（R12 后找得到 verifier）、`test_wave_verdict_contract` 3 条（安装位有第二份 toolkit 可比）。
  - 同一环境下 HEAD（`8921a3a` 导出副本）收集 1239 条，本批 1267 条，差值正好是新增的 28 条；HEAD 在同一环境下 19 failed，本批的 13 条是其真子集。
- **MCP 包**：78 / 5（新增 1 条），失败集合与 HEAD 相同（4 条缺 `operators_verified.json`、1 条节点计数）。
- **单测隔离**：`test_workflow_nodes.py` 在修复前会在默认路径建库（S4 解析建空库；probe 用例建全 schema 库）。在用户本机，默认路径就是生产库。本批后用审计钩子跟踪全量用例对默认库的 `sqlite3.connect`：**库不存在时以读写方式打开它的只剩一处**——`WorkflowExecutor` 自身的 store（既有行为，`test_audit_fixes` 等用例经 `wqb.workflow.execute()` 触发）；其余读写连接都发生在库已存在之后，其中生产代码的几处（gem 快照检查、toolkit `region_gates`）先判 `isfile`，wqb-db 的 `_conn` 即已知的 N26。
- **pyflakes**：改动文件的告警与 HEAD 相同（既有的未用 import / 无占位 f-string）。
- **技能同步**：改了 toolkit 的 `review_wave.py` / `pipeline.py` 与两份 SKILL.md，本机需要再跑一次 `python tools/sync_skills.py`（容器内已同步，`--check` 通过）。
- **第四轮共跑 4 遍**：
  - 第 1 遍发现 R4 在真实数据上无触发样本（清单改为三态，并如实打印原因），probe_batch_mode 干跑往 `cache/` 写文件（演练改为自清理），另有一处路径未脱敏（sanitize 增加 `~` 规则）；
  - 第 2 遍各项结论与第 3 遍一致；
  - 第 3 遍只改了步 2 的判定文字。第 2、3 遍去掉时间戳后比对，DB Δ 与清单逐行相同。附件实录是 §14.9.7 之后又跑的一遍（第 4 遍）。

#### 14.9.7 R5 收尾：CLI 开波闸灰度截止日

> 审阅意见："按最佳方案定日期"。R5 的第三项（CLI 的 warn 灰度写明截止日期）此前留给人定，现定案并落进代码。

**结论**：toolkit CLI（`build_wave.py`、`tools/wave_gate.py`）的开波闸缺省模式 **2026-10-11 及以前 warn，2026-10-12 起 enforce**（按本机日期）。workflow 节点（campaign S2/S3、batch_track）不受影响，一直是拦截。

**依据**：

| 问题 | 证据 | 取舍 |
|---|---|---|
| 为什么要截止，不能一直 warn | 〔史〕2026-09-17 USA：最近 2 批 max\|sharpe\| 0.88 低于天花板 0.9，近 7 天 582 次回测 0 达标，warn 只告警，照样烧槽位；只能靠战役提示词要求 USA 手动加 `--gate-mode enforce`（`tracking/USA/campaign_prompt_usa_regular_20.md:216-222`）。R5 之后 SOP 的 workflow 入口都已拦截，CLI 的 warn 是剩下的唯一绕行口 | 灰度必须有终点 |
| 为什么不今天就切 | 09-27 闸的输入语义大改：verdict 写入契约（P0-1）、逐条回写（R7 / R21）、规则 B 窗口（R22）。生产库里还有旧数据：R7 之前 FAIL 候选也记 `gated`，会抬高积压；N30 会把收批结果写到错的波上 | 先在新语义下观察真实命中 |
| 观察多久 | 挖掘按周末集中：带日期的 50 个波文件里 29 个在周六（周五 9、周三 6、周二 4、周一 2，周四和周日 0）；08-01 以来 57 个提交有 33 个在周末；KOR 在 W34 一周跑了 38 波。一个活跃周末就是几十次开波判定 | 按周末计，取两个完整周末：10-03/04、10-10/11（约两周） |
| 切在哪天 | 周一在数据里最闲（50 个波文件中 2 个，57 个提交中 3 个） | 10-12（周一）切换：当天波及面最小；若误拦，下个周末前有整整一周处理 |

**机制**（单一事实源 toolkit `_lib/region_gates.py`）：
- `WARN_SUNSET = 2026-10-11`，`default_mode()` 按日期给缺省；`resolve_mode()` 的顺序是 `--gate-mode` > `WQB_GATE_MODE` > 按日期缺省。两个 CLI 都走它（旧版安装位缺 `resolve_mode` 时 wave_gate 沿用旧缺省并提示同步）。
- 每次运行第一行打印 `gate-mode=…（来源；灰度期至 2026-10-11，2026-10-12 起缺省 enforce）`；灰度期内的命中行写明"2026-10-12 起同样命中将阻断开波"。
- 过期后 `--gate-mode warn` / `WQB_GATE_MODE=warn` 可临时回退，并打印"本次是显式回退"；放行停波区域应写台账 `stop_rules_override` 留痕。`WQB_GATE_MODE` 拼错会被忽略并点名，不会降级成 warn；程序调用传入非法 mode 时同样取按日期缺省（此前回落 warn，过期后等于 fail-open）。
- enforce 拦截仍是 exit 2，与 R12 的"门禁环境缺失"同码，含义都是"本波没有门禁结论，不是表达式问题"。
- 文档：两份 SKILL.md（toolkit 调用约定第 7 条、ra-pipeline 快捷入口）与 AGENTS.md §8.1.1。改期只改常量这一处并同步这三处与单测。

**切换前建议核对（10-11 前）**：
1. 翻看灰度期的命中行（`[region-gates] ★ 命中 … 仅告警不阻断（…2026-10-12 起同样命中将阻断开波）`；workflow 异步任务的输出在 `logs/_async_tasks/*.out`），逐区确认是真命中。KOR 的规则 B 与团队事后结论一致，属真命中。
2. 最好先修 N30：否则收批级联可能把结果写到错的波上，再经规则 B 变成误拦或误放。
3. 看各区积压占比：R7 之前的旧 `gated` 行会抬高它（workflow 入口本来就按它拦截，CLI 切换不新增这类风险）。
4. 发现误拦就修闸，或把 `WARN_SUNSET` 往后挪（一处常量）；不要全局设 `WQB_GATE_MODE=warn`，那等于取消截止日。

**时间炸弹排查**：把"今天"模拟成 2026-10-12（常量不动，`_today()` 临时返回该日，安装位同步后跑全量单测），暴露出 5 条悄悄依赖 warn 缺省的用例：`test_build_wave_selection` ×3、`test_wave_gate_missing_ply_exits_2`（开波闸先 exit 2，拿不到"门禁环境缺失"）、非法 mode 回落用例。处理：`tests/conftest.py` 加 autouse 固定 `WQB_GATE_MODE=warn`（单测结论不随日历变），非法 mode 用例改为注入日期。复查：模拟 10-12 与今天各跑一遍全量，失败集合都与基线相同。

**测试**：`tests/unit/test_region_gates_p0p1.py` 新增 6 条：截止日与按日期缺省、解析优先级（含拼错不降级）、过期后缺省与非法 mode 都拦截、输出含来源与倒计时，以及 build_wave / wave_gate 两个 CLI 在进程内走解析器（10-12 缺省 enforce，`--gate-mode warn` 与 `WQB_GATE_MODE=warn` 各自生效）。两条 CLI 用例在改动前的代码上均失败（已回退验证）。

**演练脚本**：步 5 的五次 wave_gate 显式 `--gate-mode warn`（这一步看表达式门禁本身；开波闸拦截在步 2 / 6 / 9 演示），否则 10-12 起 KOR 命中规则 B，①–⑤ 会全停在开波闸，演练不可复现；步 2 打印 CLI 的缺省模式与倒计时。

**回归**：根测试 1245 passed / 13 failed / 15 skipped（新增 6 条），失败集合与 §14.9.6 相同；把"今天"模拟成 2026-10-12 再跑全量，失败集合仍相同。MCP 包 78 / 5，失败集合与 HEAD 相同。

**环境动作（云端容器内）**：
- `python tools/sync_skills.py`：同步了两份 SKILL.md（toolkit 脚本在排查时已同步），`--check` 通过。
- MCP venv 由 uv 创建，里面没有 pip，按等价命令 `uv pip install --python world-quant-brain-mcp/.venv/bin/python -r world-quant-brain-mcp/requirements.txt` 执行：11 项全部已满足（含 ply 3.11），`uv pip check` 无冲突。
- 本机（Windows）拉取 main 后同样要各跑一次：`python tools/sync_skills.py`，以及 `world-quant-brain-mcp\.venv\Scripts\python.exe -m pip install -r world-quant-brain-mcp\requirements.txt`（venv 若由 uv 创建，改用 `uv pip install --python <venv 的 python> -r …`）。

---

## 附录 A：复现

```bash
bash reports/ra_pipeline_stage_review_20260927/reproduce.sh            # 默认在 mktemp 目录
bash reports/ra_pipeline_stage_review_20260927/reproduce.sh /tmp/wqb_dryrun   # 指定工作目录
```

脚本在工作目录里 `git archive HEAD`、建 mcp stub、`pip install --target` 装 `ply`/`msgpack`、播种合成库、跑 `run_dryrun.py`。全程不读写真实仓库与 `data/wqb.db`，不触网。本次在全新目录复跑，关键行（节点结论、退出码、闸判定、Failed-count、快照存在性）与 `dryrun_transcript.txt` 逐行一致。

**第二轮（真实环境）**：

```bash
bash reports/ra_pipeline_stage_review_20260927/realenv/reproduce_realenv.sh
# 可选：REALENV_SCRATCH=<目录>  PRE_FIX_REV=<修复前提交，默认 d1c7d78>  REALENV_ALLOW_DB_SWAP=1（本地库 >5MB 时）
```

前提：`world-quant-brain-mcp/.venv` 已按 `requirements.txt` 安装（第四轮起 `ply` 已写进 requirements；此前需另装）。不需要 BRAIN 凭据，脚本也从不读取 `.env`。

脚本的动作与保护：
- 把两个 MCP server 按 `.mcp.json` 翻译成本机路径后经 stdio 启动。
- 演练期间把 `data/wqb.db` 临时移开，结束（含异常退出）后移回。
- `tracking/KOR/priors/` 有未提交改动时拒跑；演练结束时 git 复原该目录。
- 检测并删除演练中造出的杂散目录（N19）。
- 另起修复前（`PRE_FIX_REV`）原始副本的两个 server 做对照。

本次共跑了 9 遍：
- 前几遍逐步暴露 N16 / N17 / N21，并补齐演练项；
- 第 8 遍起，修复前对照改为从"导入后快照"起步，避免混入步 1–9 的演练写入；
- 第 9 遍（即附件实录）是加入跨平台路径与删除保护后的最终版。

第 2 遍与第 9 遍的关键行逐条比对（去掉时间戳后）完全一致：导入统计、verdict 覆盖率、规则 B 输入、修复前 / 后 P0 回放各行、快照存在性、GEM 检查步。

**第三轮（P1 修复后）**：命令同上。脚本版本已更新：
- 每步打印【阶段小结】（输入 / 处理 / 输出变化 / 价值判定）；
- server 与子进程一律用 `.mcp.json` 原样 env；
- 末尾打印 P1 验证清单，逐项对照第二轮实录 `realenv_transcript_p0.txt`。

附 B 仍以 `PRE_FIX_REV`（默认 `d1c7d78`，P0 修复前）为对照。修复前代码离开 `WQB_WORKSPACE` 时 assemble-priors 会崩溃（N19b），所以附 B 的修复前 server 仍补这一个变量，让 P0 对照只反映 P0。

第三轮共跑 3 遍，经过见 §14.8.5。

**第四轮（P1 第二批修复后）**：命令同上。脚本新增：
- 步 5 ④⑤⑥（R12）：写入指到 `$REALENV_SCRATCH/wqb.db.r12probe`（演练库的副本），不改变步 6–9 的区域状态；
- 步 6（R5）、步 7（R4：读仓库内全部带 `rn_sharpe` 的评审文件）、步 8（R3：mcp_core 两种布局；设了 `BASE_DIR` 时再跑修复前副本）、步 9（R22：旧取法与实际窗口并列）；
- 验证清单三态，第二批对照第三轮实录 `realenv_transcript_r18_r21.txt`。

第四轮共跑 4 遍，经过见 §14.9.6。第 4 遍在 §14.9.7 之后：步 5 的 wave_gate 显式 `--gate-mode warn`，步 2 打印 CLI 的缺省模式；除这两处与时间戳 / 字典键序外，与第 3 遍逐行相同（DB Δ 与验证清单一致）。

## 附录 B：证据索引（主要 `文件:行`）

| 发现 | 位置 |
|---|---|
| N1 | `wqb_db_mcp.py:820-899`；`Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/wave_results.py:71-110`；`src/wqb/workflow/nodes/campaign.py:1228-1240`；SKILL.md:578 |
| N2 | `campaign.py:444-450`；`assemble_priors.py:474-507`；`brain-make-some-gem/scripts/headless_runner/run.py:346-371`；SKILL.md:269,281-286 |
| N3 | `src/wqb/config.py:351-383`；`world-quant-brain-mcp/mcp_core.py:78-98,153-156`；`tools/build_gate_prior_from_inventory.py:60-115` |
| N4 | `review_wave.py:61-76,203-215,297-317`；SKILL.md:488-494 |
| N5 | `src/wqb/workflow/nodes/batch_track.py:66-225`；`_lib/region_gates.py:18-21`；`build_wave.py:408-439`；`tools/wave_gate.py:467-491` |
| N6 | `tools/wave_gate.py:690-866,970-993` |
| N7 | `tools/wave_gate.py:572-588` |
| N8 | `world-quant-brain-mcp/tools_ops.py:236-251`；`tools/submit_verdict.py:125-130`；SKILL.md:516 |
| N9 | `campaign.py:161-170`；`pyproject.toml:19`；`world-quant-brain-mcp/Dockerfile:1`；`tests/unit/test_workflow_nodes.py:229-243` |
| N10 | `campaign.py:179,1410-1528`；`gem.py:327-331`；AGENTS.md:90 |
| N11 | 见 §11.1 |
| N12 | `tools/wave_gate.py:40-58,148,567`；`Claude/skills/INDEX.md:27-29`；`world-quant-brain-mcp/requirements.txt` |
| N13 | `src/wqb/workflow/registry.py:98-451`；SKILL.md:596,717；INDEX.md:207-211 |
| N14 | `tools/webdata_quality.py:334-381` |
| N15 | `campaign.py:204-231`；`src/wqb/store/_ledger.py:28-37`；`wqb_db_mcp.py:82,487,822`；`src/wqb/workflow/nodes/submit_alpha.py:60-61` |
| N16 | `src/wqb/workflow/nodes/campaign.py`（S2 分支，修复后新增 `stage == "S2" and subcommand == "assemble-priors"` 分支）；`Claude/skills/brain-make-some-gem/SKILL.md:109` |
| N17 | `Claude/skills/wq-brain-campaign-toolkit/scripts/assemble_priors.py:97-130`；`_lib/registry.py:87-88`；`src/wqb/workflow/nodes/gem.py`（`_PRIORS_SOURCES` / `_ledger_ts` / `_priors_snapshot_freshness`） |
| N18 | `_lib/registry.py:96-107`；`assemble_priors.py:33-34,236,278`；`tracking/KOR/priors/kor_priors.json` |
| N19 | `tools/wave_gate.py:572-583`；`_lib/ledger.py:109-114`；`_lib/wqb_store.py:10-39`；`src/wqb/workflow/_common.py:98-108` |
| N20 | `src/wqb/wave_results_contract.py`（`normalize_verdict`）；`tools/migrate_wave_verdict_enum.py:40-77`；`tracking/KOR/candidates/wave*_result*.json` |
| N21 | `Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py:165-206,517-518,1070-1093` |
| N22 | `src/wqb/workflow/nodes/campaign.py`（修复前：`_run_stop_rules_gate` 的 `ORDER BY datetime(COALESCE(updated_at, created_at)) DESC`；修复后：`_recent_closed_waves`） |
| N23 | `.mcp.json`；`mcp_config.json`；`start_mcp_server.py:14-21` |
| N24 | `src/wqb/workflow/nodes/unified_gate.py:104-141`；`src/wqb/workflow/nodes/field_understanding.py:106,138`；`wqb_db_mcp.py:1172,1927-2230` |
| N25 | `src/wqb/workflow/_common.py`（`validate_argv`）；`Claude/skills/wq-brain-campaign-toolkit/scripts/campaign.py:60-90` |
| N26 | `world-quant-brain-mcp/tools_data.py:240-259`；`docs/reference/operators_catalog.json`；`wqb_db_mcp.py:53-61`（`_conn` 不建 schema） |
| N27 | `tools/wave_gate.py`（质量预估段）；`src/wqb/workflow/nodes/gem.py`（`check_config` 先于命令构建）；`review_wave.py:30-44,113-121` |
| N28 | `Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py`（`_workspace_src_dirs` / `_load_arity_check` / `_find_tools_lib` / `_resolve_workspace_deps`；修复前的"上溯 5 级"与硬编码盘符）；`build_wave.py:141-168`（09-09 修过的同类问题）；`tests/unit/test_window_whitelist_p4.py`、`test_gem_provenance_p1p2p3.py` |
| N29 | `tools/wave_gate.py`（`_write_back_gate_status` / `_env_unknown_only` / `gate_fail_reasons`）；`gate.py`（`ENV_UNKNOWN_TAGS` / `env_unknown`、逐条缓存写入） |
| N30 | `wqb_db_mcp.py:1389`（`harvest_multisim_results` 调用点）、`:1454-1525`（`_cascade_wave_result`）；`src/wqb/workflow/nodes/campaign.py`（`_normalize_verdict`）vs `src/wqb/wave_results_contract.py`（`normalize_verdict`）；ra-pipeline SKILL.md:405 |
