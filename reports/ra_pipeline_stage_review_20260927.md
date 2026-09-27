# RA 九步流水线逐阶段展开 · 价值评估 · 沙箱 Dry-Run（2026-09-27）

> **对象**：`Claude/skills/wq-brain-ra-pipeline/SKILL.md`（v2.2，last_verified 2026-09-19）定义的唯一挖掘编排 SOP（S-PRE→S6 九步），以及它调用的 workflow 节点、`tools/`、toolkit 脚本与 MCP 函数。
> **代码基线**：`c393bca`（2026-09-25）。
> **前序审计**：`output_report/ra_pipeline_stage_audit_20260916.md`（v2）、`…_v3.md`、`ra_pipeline_remediation_plan_20260917.md`。本报告**不是增量补丁**：九步按"输入 / 处理 / 输出 / 价值"重新完整展开，并对前序结论逐条做代码级复核。
> **附件**（同名目录 `reports/ra_pipeline_stage_review_20260927/`）：`dryrun_transcript.txt`（完整演练实录）、`reproduce.sh` + `run_dryrun.py` / `seed_db.py` / `sbx_guard.py`（一条命令复现）。

**证据等级**（全文每条判断都标注来源，避免"推测记账"）：

| 标记 | 含义 |
|---|---|
| 〔码〕 | 读源码核实（给出 `文件:行`） |
| 〔沙〕 | 在隔离沙箱里实际执行复现（见 §12 与实录） |
| 〔史〕 | 引自 SKILL.md / 前序审计记录的生产实证数字——**本环境无生产库，无法复核**，按原文转述并注明出处 |
| 〔推〕 | 依赖平台网络的步骤，按源码静态推演 |

**本环境限制**：云端容器内没有 `data/wqb.db` 生产库；`.mcp.json` 里的两个 MCP 服务（`wq-brain-http` / `wqb-db`）指向 Windows 路径，本会话无法连通。因此 dry-run 在 `git archive HEAD` 副本 + **合成种子库**（region=KOR，虚构数据集 `syn_analyst`）上进行，封网并拦截子进程。沙箱里出现的所有数字都是夹具数字，**不代表生产状况**；它回答的是"这条代码路径在给定输入下会做什么"。

---

## 0. 一页结论

### 0.1 九步总览

| 步 | 阶段 | SOP 主入口 | 核心价值（保留理由） | 判定 | 本轮关键发现 |
|---|---|---|---|---|---|
| 1 | S-PRE 查表 | profile + `get_mining_yield` + 库存盘点 | 先清库存再新挖；conversion/yield 区分"管道问题 vs 标的问题" | **保留深化** | `inventory_scan` 节点未入 SOP；`latest_wave` 对字符串波号排序失效 |
| 2 | S0 体检选集 | `workflow_campaign(S0)` + `s0-select` | 平台真实点塔 × 严格产出率 × 判死；座位可达性 | **保留深化** | dry-run 会写 `settings.json`；节点缓存是死代码 |
| 3 | S1 字段 | `workflow_campaign(S1)` → typed catalog | 类型/覆盖元数据是闸 2/3/8 与 catalog 前置闸的数据源 | **保留** | **Python 3.11 下 S1 恒判"缺 dataset"**；users 分级无工具实现 |
| 4 | S2 生成 | assemble-priors → `workflow_gem` → build_wave | 概念优先 + 生成侧预闸 + 骨架配给 | **保留深化** | **P0：节点路径不写 priors 快照，GEM 只读快照 → S6→S2 回流断开** |
| 5 | S2→S3 门禁 | ghost-audit → `wave_gate` | 零配额拦截整批连坐（语法/元数/字段/VECTOR/毒模式/体检） | **保留，精简展示层** | `[opcat]`/质量预估打印 FAIL 却不参与判定；FAIL 候选仍记 `gated`；体检规则 1/5 耦合 |
| 5b | prod-first 探针 | `campaign_intel prod-first` | 把 prod 墙判断前移到扩批之前 | **保留** | 网络依赖，未演练 |
| 6 | S3 七槽回测 | `workflow_batch_track` → pipeline.py | 七槽填槽、设置先验、连坐隔离、argv/存活握手 | **保留** | SOP 指定入口 `batch_track` **不跑**停止/天花板/积压三闸 |
| 7 | S4 诊断 | `workflow_campaign(S4)` → review_wave | RN_EXPOSURE / ROBUST_STRUCTURAL 墙、预筛、salvage | **保留深化** | RN_EXPOSURE 行仍进 near/salvage 池 |
| 8 | S4→S5 判定 | Failed-count → `submit_verdict` → 用户确认 | 否决权威 + 人工确认门 | **保留，修正定位** | `src/wqb/config.py` 有一份与生产口径相反的 Failed-count 实现；`submit_verdict` 对新候选只能给 UNVERIFIABLE |
| 9 | S6 复盘 | `step_funnel` + `upsert_wave_result` + pyramid | verdict→停止规则 B、region_kb 刷新、判死封存 | **保留** | **P0：只补写 key_findings 会把 verdict 清成 NULL → 停止规则 B 静默失效（全链复现）** |

**总评**：九步骨架本身没有多余的"步"——每一步都承载着至少一个有实证的判别机制。本轮发现的问题集中在**步与步之间的接缝**（写入口契约、快照/文件双载体、节点 vs CLI 两条执行路径语义不一）和**展示层噪声**，而不是"缺步骤"或"步骤无用"。真正该**去除**的是少数已被证明无效或误导的子项（死代码缓存、分叉实现、只打印不判定的伪硬闸），真正该**深化**的是把 SOP 文字规则变成机器可执行的约束（users 分级、区域闸 enforce、verdict 写入契约）。

### 0.2 本轮新发现（按严重度；均为 09-16/17 三份审计未记录的问题）

| # | 级别 | 发现 | 证据 |
|---|---|---|---|
| N1 | **P0** | `mcp__wqb-db__upsert_wave_result` 的 UPDATE 分支对未传字段写 NULL（非合并）。按步 9 指引"把 pyramid 的 key_findings 行拷进 upsert_wave_result"只传 key_findings 时，**已有 verdict 被清空** → 规则 B 遇 UNKNOWN 只告警不拦截 → 下一波被放行。该入口还接受 `status=closed` + 空 verdict（toolkit 的 `WaveResultsStore.upsert` 会拒绝，两个写入口契约不一致） | 〔码〕`wqb_db_mcp.py:820-899`、`_lib/wave_results.py:82-85`；〔沙〕实录 步 9 |
| N2 | **P0** | `workflow_campaign(subcommand="assemble-priors")` 拼出的命令**不带 `--snapshot-ledger`**，只重写 priors 文件；GEM 默认 `--priors-from-db` **只读 DB 快照** `priors_snapshot_<r>`（缺快照 fail-closed）。SOP 宣称的"S6 回写后下一次 S2 先验自动变新"在指定路径上不成立：新区直接失败，老区静默沿用旧快照 | 〔码〕`campaign.py:444-450`、`assemble_priors.py:474-507`、`headless_runner/run.py:346-371`、SKILL.md:269/281-286；〔沙〕实录 步 4 (b)(c) |
| N3 | P1 | Failed-count 资格门有三份实现：`mcp_core.py`（17 项 + WITH_RATIO，非 PASS/PENDING 计失败，**正确**）、`build_gate_prior_from_inventory.py`（同口径副本）、`src/wqb/config.py::compute_webdata_failed_counts`（8 项、只数 FAIL、含不存在的 `HIGH_DRAWDOWN/LOW_SELFCORR/LOW_PNL`）。第三份仅被单测引用，但它位于 AGENTS.md 规定的"唯一事实源"模块，是照规范 `from wqb.config import …` 就会踩中的陷阱。同一组 checks：生产口径 `failed_ra=3`，config 口径 `0` | 〔码〕`config.py:351-383` vs `mcp_core.py:78-95,153-156`；〔沙〕实录 步 8 |
| N4 | P1 | review_wave 的 near 池只排除 `ROBUST_STRUCTURAL`，**不排除 `RN_EXPOSURE`** → 被判"就是暴露本身、禁止调参"的行仍进 near_pool / salvage_pool，可被 Mode A/B 取用 | 〔码〕`review_wave.py:203-215, 297-317`；〔沙〕RN=-0.2 行 `walls=['RN_EXPOSURE'] near=True` |
| N5 | P1 | 三道零配额开波闸（signal_floor / stop_rules / backlog）只在 `workflow_campaign(stage=S2/S3)` 里 enforce；SOP 步 6 指定的 `workflow_batch_track` 一道都不跑；CLI 入口（build_wave / wave_gate）默认 warn。"发批直接走步 5"的快捷入口全程无 enforce | 〔码〕`batch_track.py:66-225`、`region_gates.py:18-21`；〔沙〕batch_track 干跑 steps 无闸，campaign S3 干跑有三闸 |
| N6 | P1 | `tools/wave_gate.py` 的若干"闸"只打印不判定：`[opcat]` 自称硬闸、打印"FAIL：缺 Group"，质量预估对每条打印 `HARD_REJECT`，但二者都不进 `all_pass` —— 最终 `=> PASS`、exit 0 | 〔码〕`wave_gate.py:749-822, 970-993`；〔沙〕实录 步 5 ⑦ |
| N7 | P1 | `--exprs-file` 候选在门禁**之前**以 `status='gated'` 入库，门禁 FAIL 后不回写 → `gated` 同时表示"送过闸"与"过了闸"，积压闸与漏斗把 FAIL 候选计为未消费积压 | 〔码〕`wave_gate.py:572-588`；〔沙〕w5/w6/w7 FAIL 后 19 条仍为 `gated` |
| N8 | P1 | `submit_verdict` 对处女提交（新候选的常态，提交层 404）只能返回 `UNVERIFIABLE`；SOP"是否提交的最终判定以本步为准"对新候选无法给出放行结论——它是**否决权威**，放行依据实际是模拟层 checks + 平台 prod 相关性 + 用户确认 | 〔码〕`tools_ops.py:236-251`、`tools/submit_verdict.py:125-130`；〔推〕判定表 |
| N9 | P2 | `campaign` 节点 S1 必填校验把 `locals().get(p)` 写在列表推导式里：Python 3.11 推导式有独立作用域 → **传了 dataset 也判缺失**。`pyproject.toml` 声明 `>=3.11`；仓库自带 `test_campaign_stage_route_matrix` 在 3.11 下即红（3.12 起因 PEP 709 内联推导式才"碰巧"可用） | 〔码〕`campaign.py:161-170`；〔沙〕实录 步 3 + pytest 复现 |
| N10 | P2 | dry-run 契约（AGENTS.md:90"不 subprocess、不写库、不建目录"）两处破口：`campaign` 节点在 dry-run 前调用 `_ensure_campaign_config`，缺 `settings.json` 时写入一份硬编码默认值（universe=TOP3000/decay=4/SUBINDUSTRY）；`gem` 节点在 dry-run 返回前 `makedirs(logs/_async_tasks)` | 〔码〕`campaign.py:179,1410-1528`、`gem.py:327-331`；〔沙〕AMR 干跑生成 `settings.json`；gem 干跑 FS +2 |
| N11 | P2 | 战役库路径至少 7 套解析口径，其中 3 处硬编码 `D:\coding\traeCN_project\wqb`；`WorkflowExecutor` 用相对路径 `data/wqb.db`，换 cwd 即在当前目录新建空库 | 〔码〕见 §11.1；〔沙〕换 cwd 后生成 `elsewhere/data/wqb.db` |
| N12 | P2 | `tools/wave_gate.py` 的 toolkit/validator 解析只认 `WQ_*_DIR`、`~/.qoder-cn`、`~/.cursor`、`~/.workbuddy`，**没有** INDEX.md 所写的 `~/.claude`、`~/.codex` 与仓库兜底；验证器硬依赖 `ply` 但任何 requirements 都未声明，缺失时以 exit 1（=表达式 FAIL）而非 exit 2（=环境 ERROR）退出 | 〔码〕`wave_gate.py:40-51,148,567`、`INDEX.md:27-29`；〔沙〕实录 步 5 ③④a |
| N13 | P2 | 19 个 workflow 节点中 9 个（inventory_scan / field_understanding / gem_wave / unified_gate / auto_harvest / auto_review / auto_pyramid / modeb_improve / structural_reconstruct）**没有任何 skill 引用**；SKILL.md 仍写"registry 注册 8 个""workflow 节点 9"，与 INDEX 的 19 冲突；同类漂移还有 SKILL.md"现有 12 个 profile、JPN 未覆盖"，而 `references/regions/` 实有 13 份（含 09-15 补建的 JPN.md） | 〔码〕grep 结果；SKILL.md:54-56,596,717 vs INDEX.md:65,207-211 |
| N14 | P3 | 体检硬门规则 1（cov<0.4 必须含 ts_backfill）与规则 5（稀疏事件必须 trade_when）对同一字段叠加：真实 320 个体检包 56,235 个字段中 **2,162 个**同时满足两条件，合规的事件门控写法也会被规则 1 判违规 | 〔码〕`webdata_quality.py:344-381`；〔沙〕w6 `trade_when(syn_surprise_evt>0,…)` 被判违规；真实包统计 |
| N15 | P3 | 其它小项：`campaign` 节点 calibrate / assemble-priors 的 ledger 缓存命中条件 `cached.get('value')` 永不成立（死代码）；MCP `upsert_wave_result/get_wave_result` 的 `wave_number: int` 与表结构 TEXT 冲突；`get_campaign_summary.latest_wave` 用 `CAST(wave_number AS INTEGER)` 排序；`submit_alpha` 节点默认给所有提交（含 RA）打 `PowerPoolSelected` 标签；VECTOR 未包裹的报错文案写成 `[EVENT]` | 各节，〔码〕+〔沙〕 |

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
| `--exprs-file` 候选状态（N7） | ✂ 需修 | 〔沙〕w5/w6/w7 门禁 FAIL 后 19 条候选仍为 `gated`；积压闸把 `gated` 计入 pending+gated 与 unconsumed |
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

## 12. Dry-Run 演练（沙箱）

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
| R1 | 修 `upsert_wave_result`（N1） | UPDATE 改 `COALESCE(?, 列)` 合并语义；`status='closed'` 且 verdict 为空时拒绝（与 `_lib/wave_results.upsert` 同契约）；SKILL.md:578 的 pyramid 回写改为"追加 key_findings"专用入口（或复用 auto_pyramid 的定向 UPDATE） | 复跑实录步 9：补写 key_findings 后规则 B 仍拦截；+2 单测 |
| R2 | 接通 priors 回流（N2） | campaign 节点 assemble-priors 默认追加 `--snapshot-ledger`（或 SOP 显式要求 `extra_args=["--snapshot-ledger"]`）；GEM 物化快照时比较快照 `generated_at` 与 `region_kb.updated_at`，陈旧即 WARN | 复跑实录步 4(b)：快照存在且 wins 反映新 region_kb |

### 13.2 P1（安全/语义）

| # | 建议 | 改法 |
|---|---|---|
| R3 | Failed-count 单一实现（N3） | 把 `mcp_core._RA_CHECK_NAMES/_PPA_CHECK_NAMES/_ra_bad` 迁入 `src/wqb/config.py` 作为唯一事实源，mcp_core 与 build_gate_prior 引用它；删除现有分叉实现并改 `test_config.py` |
| R4 | near 池排除 RN_EXPOSURE（N4） | `review_wave.py` near 循环里 `if "RN_EXPOSURE" in r["walls"]: continue`；+单测 |
| R5 | 区域闸语义统一（N5） | `batch_track` 节点接入 `run_region_gates`（与 campaign S3 同为 enforce）；CLI 的 warn 灰度写明截止日期；SOP"快捷入口"注明必须过区域闸 |
| R6 | 去掉门禁展示层噪声（N6） | `[opcat]` 与质量预估改为 INFO（不再出现 FAIL / HARD_REJECT 字样），或真正接入 `all_pass`；质量预估默认关闭，需要时 `--quality` 开 |
| R7 | 候选状态语义（N7） | `--exprs-file` 先入 `pending`，按 gate.py 逐条结论回写 `gated`/`fail` |
| R8 | 提交判定定位（N8） | SKILL.md 步 8 改写：submit_verdict = 否决权威；新候选放行 = 模拟层全过 + 平台 prod < 0.7 + 用户确认 |

### 13.3 P2 / P3（可移植性与治理）

| # | 建议 |
|---|---|
| R9 | `campaign.py:161-170` 改显式 dict（N9） |
| R10 | `_ensure_campaign_config` 与 gem 的 `makedirs` 移到 dry-run 判定之后；把 §12 的 Probe 做成"干跑零副作用"单测（N10） |
| R11 | 全部 DB 路径改走 `resolve_db_path()`；`WorkflowExecutor` 默认用它；删除 3 处 `D:\` 硬编码（N11） |
| R12 | `wave_gate.py` 的解析改用 `skill_roots()`；requirements 增加 `ply`；缺依赖 / 缺脚本时 exit 2（N12） |
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
| **去除** | campaign 节点缓存分支（死代码）；`src/wqb/config.py` 的 Failed-count 分叉实现；`_ensure_campaign_config` 的硬编码默认配置（改为缺配置即报错并给出生成命令）；未被 SOP 采纳的孤儿节点（逐个确认后） |

---

## 附录 A：复现

```bash
bash reports/ra_pipeline_stage_review_20260927/reproduce.sh            # 默认在 mktemp 目录
bash reports/ra_pipeline_stage_review_20260927/reproduce.sh /tmp/wqb_dryrun   # 指定工作目录
```

脚本在工作目录里 `git archive HEAD`、建 mcp stub、`pip install --target` 装 `ply`/`msgpack`、播种合成库、跑 `run_dryrun.py`。全程不读写真实仓库与 `data/wqb.db`，不触网。本次在全新目录复跑，关键行（节点结论、退出码、闸判定、Failed-count、快照存在性）与 `dryrun_transcript.txt` 逐行一致。

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
