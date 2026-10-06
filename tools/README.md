# tools/ 通用工具索引

区域无关的战役工具链。约定：
- **退出码**：`0`=PASS/成功，`1`=FAIL/失败（可直接串进 pipeline）
- **网络工具运行环境**：MCP venv（`$WQ_PY` 或 `world-quant-brain-mcp/.venv`），自动 `os.execv` 重启，勿用系统 python
- **skill 依赖路径**：自动解析 `WQ_VALIDATOR_DIR` / `WQ_TOOLKIT_DIR` → `~/.qoder-cn/skills` → `~/.workbuddy/skills`，**禁止硬编码**

## 目录结构与迁移状态（P2-1，2026-10-04）

顶层现在平铺 **142 个脚本**（2026-10-06 实测），主题分类已由本索引的 `## <主题>` 节定义，
部分已落目录。目标结构与逐文件归属固化在 **[`tools/THEMES.json`](THEMES.json)**（19 个主题目录，
kebab-case），另有 4 个区域专属脚本标记为应迁出 `tools/`
（`relocate_out_of_tools` → `tracking/KOR/scripts/`）。

**新脚本一律落主题子目录**，不得再往顶层堆 —— 由 `python tools/audit_structure.py --only s11`
强制（顶层只减不增，新增即 FAIL 阻断提交）。

### 迁移批次记录

| 批次 | 日期 | 文件数 | 落点 |
|---|---|---|---|
| P2-1 止血 | 2026-10-04 | 0 | 只冻基线（S11）+ 出 THEMES.json，全部 `frozen-pending` |
| **第一批下沉** | **2026-10-06** | **10** | `probe/` ×4 · `verdict/` ×3 · `ledger/` ×2 · `data-repair/` ×1 |

> 第一批按本文件「单文件迁移配方」执行，两处与配方的偏差记在此：
> ① 配方第 1 步的工具 **`refs_scan.py` 本身已不在工作区**（属事故丢失的 17 个之一），
> 改用等价 `grep -rn "tools/<stem>.py"` 判命中形态；
> ② 配方第 2 步推荐的 `from wqb.paths import repo_root` **该模块不存在**，故退化为按新层级
> 修正 `dirname` 层数 / `..` 级数（下沉后逐脚本 `--help` 实测通过）。
> 另：被移文件此前均**未被 git 跟踪**，`git mv` 不适用（会报 not under version control），
> 故用文件系统搬移 + `git add` 记录。

### 为什么不当场把 171 个全下沉（实测数据）

下沉一层会**同时**改变两件事，且两者都是运行期才爆：

| 耦合点 | 实测数量 | 后果 |
|---|---|---|
| 全仓 `sys.path.insert(... 'tools')` | **80 处** | 目标模块不在该目录 → ImportError |
| tools 脚本被当**模块 import** | `index_tables`、`migrate_wave_verdict_enum`（含 `run_realenv.py`、3 个测试文件） | 测试与被调脚本同时断 |
| 仓库根推导写法 | 同一主题内 **5 种**：`dirname(dirname(abspath))` / `parents[1]` / `parent.parent` / `os.path.join(f,'..','src')` / `parents[2]` | 层数硬编码 → 根指错，DB/报告/归档全错 |
| CLI 字符串引用 | `tools/<x>.py` 散在 AGENTS.md、docs、`Claude/skills/**`、tests、workflow registry 节点 | 技能运行期找不到脚本 |

一次性批量改在这三条上都无安全网，所以采取：**止血（S11）+ 计划表（THEMES.json）+ 逐主题迁移**。

### 单文件迁移配方（每个主题一批，做完就跑验证）

1. `python tools/refs_scan.py --names <stem> --show-hits` → 人工判别命中形态（import / CLI 串 / ledger key）。
2. 先把该文件的仓库根推导改成**层数无关**写法（新代码直接用 `from wqb.paths import repo_root`；
   不愿依赖安装的脚本写向上探测：逐个 `parent` 找 `pyproject.toml` + `src/wqb`）。
3. `git mv tools/<x>.py tools/<theme>/<x>.py`（保历史，归档而非删除）。
4. 全仓改写字符串引用：`tools/<x>.py` → `tools/<theme>/<x>.py`（AGENTS.md、docs、reports、
   `Claude/skills/**`、`src/wqb/workflow/registry.py` 与节点体里的子进程命令）。
5. 若有 `sys.path.insert(... 'tools')` 的导入方：改成指向新目录，或改走 `wqb` 包导入。
6. `python tools/sync_skills.py`（把 skills 内的路径改动推到 6 个安装位）+ 更新本索引行与
   `THEMES.json` 的 `status`，并把该文件从 `audit_structure_baseline.json` 的
   `s11_tools_top_level` 移出（S11 会点名提醒）。
7. 验证：`python tools/audit_node_registration.py`（若涉节点 argv）→ `python -m pytest tests/ -x`
   → `python tools/audit_structure.py` → 对被移脚本跑一次 `--help`（证 import 与路径自举没断）。

> 参照先例：`tools/wave_gate.py` + `tools/wave_gate_pkg/`（§8.12）是「入口 shim 留原位、
> 实现进包」的已完成样本；改 argparse 时仍须动 shim，`validate_argv` 才解析得到。

## 提交前闸门（构建候选池后、回测前）

| 工具 | 用途 | 取代 |
|---|---|---|
| `wave_gate.py` | 每波门禁编排：语法校验 + 5 闸 + 六维多样性 + 质量预估（EXPECTED_BLOCK 默认标注，`--quality-block` 硬拦截），一键落盘 `cache/gate_wave<N>_<ds>.{json,txt}`。**2026-09-30 包化**：入口为 shim（argparse 契约字面保留，供 `validate_argv` 静态解析），实现 12 个模块在 `tools/wave_gate_pkg/` | `tracking/<R>/scripts/_gate_waveNN.py` 族 |
| `pool_diversity.py` | 候选池表达式结构多样性评估（算子熵/骨架配额/字段集中度/预处理/成对相似度/主导族风险，六维），`--file/--exprs/DB`，`--json` 落盘；已被 `wave_gate.py` 集成调用 | 手写多样性统计脚本 |
| `quality_predict.py` | 候选池质量预估（回测前）：三层先验预估 Sharpe/Fitness + 本地结构代理预估 SELF_CORR 风险，输出 EXPECTED_PASS/REVIEW/EXPECTED_BLOCK；`--status UNSUBMITTED` 直筛存量池，已被 `wave_gate.py` 集成调用 | 手写相关性/质量预判脚本 |
| `legacy/gate.py` | **遗留归档**：通用提交前闸门（5 闸 + 批级多样性）。**权威实现是 skill toolkit 的 `gate.py`**；本文件代码零引用（`wave_gate.py` 走 `_TOOLKIT_CANDIDATES` 加载 toolkit 版），2026-09-20 归档至 `tools/legacy/` | — |
| `legacy/backfill_backtest_dataset.py` | **一次性回填已跑完**（`backtest_results.dataset` 只填空），2026-09-28 按 §6.4 归档至 `tools/legacy/`（三维引用全 0） | — |
| `forum_recon.py` | **问题驱动论坛只读检索（recon，2026-09-28）**：单问题 → 有效文章 → 入库（`KB/community_tpl_kb.forum_recon_entries` 或 ledger `forum_recon_<qkey>`；无解落 `forum_recon_negative_*` 作「论坛无解」判死证据）。额度以查出有效文章为标准（自适应扩关键词，命中即收束）；同问题 7 天缓存；抓取核心复用 `forum_research.py`（不重复 HTTP 实现）；`--dry-run` 零副作用；退出码 0=有货 / 2=**可靠的**无解 / 1=**工具故障**（故障落 `forum_recon_error_*`、不入缓存，**故障 ≠ 无解**，2026-09-29 事故后落地；共享契约 `src/wqb/recon_evidence.py`） | 手写论坛抓取、每次现搜不落库 |
| `forum_recon_wave.py` | **波级默认取证（2026-09-30）**：收批时对本波共同卡住的墙（全灭时为「有无解法」）问一次论坛——本波回测结果机械派生决策问题（`src/wqb/recon_wave.py`），交 `forum_recon.recon()` 执行，落 ledger + 完成标记 `forum_recon_wave_<wave>`；每波 ≤ 1 次（可靠结局占额度，故障不占）；`--force` 重跑、`--dry-run` 只读库零网络零写库；退出码同 `forum_recon`；节点 `forum_recon_wave`、`pipeline.py --forum-recon`（`batch_track` 缺省带上） | 卡墙时靠 Agent 记性想起去查论坛 |
| `shape_quota_check.py` | **模板形状配额机检（2026-09-30）**：一波候选须覆盖 ≥ 3 个形状族、`trade_when` 占比 ≤ 40%（步 4 §4.5.1）；只读、`--verbose` 逐条列族、`--json`；退出码 0=达标或候选不足 3 条 / 1=不达标 / 2=无法检查；不入闸链（闸 6 才是批级多样性权威）。分类规则见 `src/wqb/shape_quota.py` | 人工数一遍算子形状 |
| `expr_lint.py` | 算子签名/字段白名单快速门禁（非战役场景） | — |
| `corr_precheck.py` | 相关性墙预判（设计阶段字段重叠检查） | — |

## 回测与状态

字段级经验快照：`dataset_experience.py --region EUR --delay 1` 从 DB 导出每个已回测数据集的
`reports/dataset_experience/eur_<dataset>_campain.md`。支持 `--dataset`、`--waves`、`--dry-run`；
只读数据库，保留人工复盘段。S6 入口为 `workflow_campaign(subcommand="dataset-experience")`。

| 工具 | 用途 | 取代 |
|---|---|---|
| `mcp_7slot_batch.py` | 七槽并发回测（MCP 驱动，`--alpha-json` + `--settings-json` + `--output-csv`）。★ 2026-09-17 修正：此前本表写 `mcp_5slot_batch.py`，**该文件并不存在** | — |
| `batch_status.py` | 批次/子任务状态查询与 `--watch` 轮询（multisim 或单条） | `tracking/_scratch/check_*batch*.py`、`track_mea_super_resume.py` 轮询段 |
| `harvest_multisim.py` | multisim 收批：拉 children → 拉 alpha 详情 → 关联 expressions → 可选 upsert backtest_rows | `tracking/*/scripts/poll_wave*.py`、手写收批脚本 |
| `submit_batch.py` | 批量**派发仿真**（`POST /simulations`；`--spec` 支持逐批不同设置）。⚠ 不是把 alpha 提交上平台——那是不可逆的 `workflow_submit_alpha(confirm_submit=True)` | 31 个 `_submit_*.py` |

## 探针编排（新数据集首探）

S2选波沿用toolkit `build_wave.py`：`--size`为容量；预定实验使用
`--selection-contract-key`读取DB机制/对照清单，按ID与原式核对，不固定8条。
使用说明及延后项审计见[选波实验清单](../Claude/skills/wq-brain-campaign-toolkit/references/selection-plan.md)。

| 工具 | 用途 | 取代 |
|---|---|---|
| `probe_batch_mode.py` | 2+6 探针批模式：L0（2 条）快速判死 → L1（6 条）信号确认，真实回测（入库→pipeline→DB 拉指标） | 手写 8 探针表达式 + 手动判定 |
| `tiered_probe.py` | 三层探针编排器：L0 判死 → L1 确认 → L2 ModeA 变体自动升级；组合腿快腿轮换（fast_pool 多样性）；慢腿预处理轮换（raw/reverse/ts_decay_linear） | 手写 ModeA 变体波 |
| `probe/category_sweep.py` | **L0 类别普查**（2026-10-06 下沉）：指定 region 遍历**全部** category，产出每类字段池。**零回测零 API**；产物是「字段池」不是 ideas，**禁止直接注入 GEM**。边界：只做普查不做判死（判死是 `category_field_triage.py`，其甜点判据 `alpha_count∈[10,50]` 与真实产出矛盾，本工具不复用其判级） | 手写逐 category 查 catalog |
| `probe/category_probe.py` | **L1 苗子探针生成**（2026-10-06 下沉）：为 L0 筛出的类别生成**机制多样**的探针表达式（上游 `probe/category_sweep.py --seed-fields --json <out>`），产物逐行喂 `submit_batch.py --path` 跑 QUICK，收割后 `--classify` 判苗头。★ 铁律：**条数不是首要变量、机制多样性才是**（历史命中率中位 7%；DEU 164 条达标只来自 73 个独立表达式，去重比 2.2x）。**本工具自己不派发仿真**（零配额、可 dry-run） | 手写探针表达式 |

> `wave_gate.py --probe-mode` 只做门禁阶段探针分配标记（结构预判），真实回测判死走 `probe_batch_mode.py` / `tiered_probe.py`。

## SUPER alpha 流水线

| 工具 | 用途 | 取代 |
|---|---|---|
| `sa_probe.py` | 组件池探针：≥10 ACTIVE REGULAR 硬前置，GO/BLOCKED | `probe_kor_sa.py`、`tracking/_scratch/probe_sa2_*.py` |
| `super_build.py` | select / status / probe / submit 四子命令全流程；**submit 内置 prod 闸（2026-09-25）：probe max≥0.7 或超时一律拒提（fail-closed），豁免须 `--allow-prod-above-07`** | `track_mea_super.py` / `_resume` / `_submit` 三件套 |
| `probe/probe_sa_candidates.py` | **SA 候选与组件池盘点**（2026-10-06 下沉；与 `verdict/submit_inventory.py` 互补——后者盘 RA/REGULAR，本脚本盘 SA/SUPER）：组件池 eligibility（GO/BLOCKED）、全部 SUPER alpha、未提交 SA 候选。★ 关键语义：组件 eligibility **只看「已提交且 ACTIVE」的 REGULAR**，IS 阶段 UNSUBMITTED 不计入；SA 可提交的 selection 字段无 sharpe/fitness，只能按 turnover/decay 排。`--save-json` / `--cache-ttl-hours`（env `SA_PROBE_CACHE_TTL_HOURS`，默认 6h） | 手查 SUPER 控制台 |
| `probe/probe_sa_unsubmitted.py` | 对 SA 探针列出的**未提交候选逐颗取真实双闸**（`check_self_correlation` + `check_correlation(production)`），判定是否双双 <0.7。★ 「UNSUBMITTED（已建未提交）」≠「待提交（已验证可交）」——探针文件里这些候选的 prod 恒为 `None`，本工具是**推荐序「余量」列的唯一来源**。★ 处理范围铁律（用户定，勿回退）：**只处理增量数据 + 无 prod 值但业绩已明确记录者**（⛔ 禁 `--all`） | 手写逐颗打相关性 |

## 提交判定

| 工具 | 用途 | 取代 |
|---|---|---|
| `prod_first_screen.py` | **区域未提交存量的 prod 首筛**（prod-first 纪律的机械执行）：枚举区域内 IS 合格 & 未提交的 alpha → 逐条测 prod（`refresh=true`，服务端计算）+ self（本地）→ **断点续跑**（state 文件，prod 取不到不入 state 下次重试）→ 测得的数值**回写 `alphas.prod_correlation/self_correlation/corr_checked_at`** → 输出「prod<0.7 可提交清单」。★ 背景：全库 370 颗未提交存量里只 97 颗测过 prod、仅 6 颗 <0.7（瓶颈是 prod 不是 IS）；**ASI 95 颗从未测过**故优先。**需 MCP venv 的 Python 跑** | 手工逐条查相关性 |
| `quota_status.py` | **当日提交配额实况（ET 日口径）**：列 `stage=OS` 按 `dateSubmitted` 倒序数**今日（ET）**已提交颗数 → REGULAR 用量/剩余。★ 2026-09-21 事故配套：`GET /users/self/activities/submissions` **只有 yesterday/current/previous/ytd 快照、缺 today**，据此判断当日配额必然误判（实测当日已用 2 个仍显示“昨日 5”）→ 撞 `REGULAR_SUBMISSION(4/4)` 配额墙。**需 MCP venv 的 Python 跑** | 手数控制台提交记录 |
| `submit_verdict.py` | 提交层判定双视图：模拟 checks + `GET /alphas/{id}/submit`（403 盲区拦截，零配额）。★ 出 `SUBMITTABLE` 时**自动把待提交队列该条升级为 `SUBMIT_LAYER_VERIFIED`**（`mark_verified`，2026-09-20） | 手写 GET/POST submit 探针 |
| `os_decay_benchmark.py` | **IS→OS 衰减基准与选品定标**：从 OS 缓存计算保留率分位（ACTIVE / DECOMMISSIONED 双队列）、IS→期望 OS 映射、目标 OS 反推所需 IS，并固化「**IS 对 OS 无预测力**」的决定性检验（n=124：corr(IS,保留率)=+0.001、负 OS 比例恒 ~22%）→ `data/os_decay_benchmark.json`。`--for <IS>` 供选品时查期望 OS 区间 | 口头经验「IS 到 OS 会衰减」 |
| `os_decay_benchmark.py` | **IS→OS 衰减基准与选品定标**：从 OS 缓存计算保留率分位（ACTIVE / DECOMMISSIONED 双队列）、IS→期望 OS 映射、目标 OS 反推所需 IS，并固化「**IS 对 OS 无预测力**」的决定性检验（n=124：corr(IS,保留率)=+0.001、负 OS 比例恒 ~22%）→ `data/os_decay_benchmark.json`。`--for <IS>` 供选品时查期望 OS 区间 | 口头经验「IS 到 OS 会衰减」 |
| `os_report.py` | **已提交 alpha 的 OS（样本外）表现报表**：列表 `stage=OS` 拿全集 → 逐条详情取 `os` 块（`sharpe/sharpe60/sharpe125/returns/drawdown/fitness/osISSharpeRatio`，本地缓存+断点续跑）→ markdown 报表 + CSV。产出「ACTIVE 且 OS Sharpe<0」清单（首要处置对象）、近 60 日恶化榜、Cluster/PowerPool 交叉。★ 知识：**列表端点只带 `osISSharpeRatio`，OS 全量指标只在详情端点**（已验证 `osISSharpeRatio × IS.sharpe = os.sharpe`）。**需 MCP venv 的 Python 跑** | 手查控制台 / 逐条拉详情 |
| `triage_prodcorr_batch.py` | prod_corr 族级抽样（提交层预筛 → 族去重 → 串行抽测，checkpoint 续跑，结果写 `logs/_triage_prodcorr.json`） | 逐条手查 correlations/prod |
| `persist_prod_corr.py` | 把上面的 checkpoint 回填 `alphas` 的 prod/self 相关性（只填 NULL、幂等、默认 dry-run 加 `--apply`；支持 `--source` 溯源与 `--overwrite`）。**运行手册：每轮 S3 批次后跑 triage → 再跑本工具落库**，0.6 预警线才有过程数据 | 手工 UPDATE |
| `query_alpha_metrics.py` | 本地库直查 alpha 全指标（`--coverage` 看填充率；`--region/--max-prod/--max-self/--min-sharpe/--source` 筛候选；`--csv` 导出）。**候选筛选零配额，免打平台 `check_correlation`** | 逐条打平台 correlations API |
| `submit_queue.py` | **待提交候选队列**：把回测过闸的 alpha 持久化到独立表 `submit_ready`，解决"找到可提交项但不当天提交就遗忘"。子命令 `init` / `add`（平台拉指标+相关性）/ `add-many`（离线从 `alphas` 批量导入）/ **`dedup`**（按骨架去重，同区域同骨架只留最优 N 条，其余标 `SUPERSEDED`）/ **`retag`**（按当前规范**重算全队列** `suggested_tags`，规范/解析器升级后回填；`--dry-run`）/ `verify`（相关性时效复检 + **RA 硬闸 + add 混腿**，过期变坏标 EXPIRED/DEAD，开跑前自动退役已 ACTIVE）/ **`sync`**（退役平台已 ACTIVE/已提交的 READY 行，`--offline` 零配额）/ **`regrade`**（离线复判 READY 行：RA 硬闸 / 加权混腿 / prod 兄弟）/ `list`（按优先级排）/ `pick`（取最优先 1 条）/ `retire`（退役）。★ 未过硬闸者自动标 `DEAD` 并从默认视图剔除；★ 2026-09-20 补三坑：RA FAIL（robust/sub-universe/CW/ladder…）不进 READY；加权混腿口径 = gate.py 闸5；同骨架兄弟 prod≥0.7 且本条未测 → `PROD_SIBLING` 判死；SUBMITTED/DEAD 终态粘性（harvest 再入队不复活）+ 排除平台 ACTIVE；`IS_ONLY` 表示 IS 达标但相关性待测，提交前必跑 `verify`。★ 骨架去重复用权威实现 `wqb.expression.skeleton::structural_signature`，`add-many` 默认开启（`--no-dedup` 关，`--max-per-skeleton N` 调） | 手写备忘 / `ledger_kv('submit_ready')` 旧临时队列（**2026-09-20 已归档并删除**，见 `logs/archive_ledger_submit_ready_*.json`） |
| `prod_blocked_recheck.py` | **PROD_BLOCKED 候选的**平台实时**复核器**（`submit_ready` 队列专用）：差分两路径——**A 自家撞墙**（重测自己 prod，跌破 0.7 即复活 READY）与 **B 兄弟带累**（`FAIL:PROD_SIBLING(<id>=<v>)`，本条 prod 从未测过；查**兄弟的实时 prod**，松动才解锁）。★ 动机：`store._prod_wall_sibling` 判定兄弟时读的是**库内存量 prod**，而项目铁律是「库内 prod 会过期→提交前必实测」，故本工具在它之上补实时口径。**同兄弟进程内缓存**（实测 `9qjPxmre` 被 3 行点名，不缓存等于同笔相关性连测三遍，PC 还占平台单并发队列）。`--dry-run` / `--region` / `--limit` / `--fresh`（忽略断点）/ `--sleep`；断点 `results/prod_blocked_recheck_ckpt.json`，**dry-run 不写断点**（否则正式跑会跳过未落库的行）。**需 MCP venv 的 Python 跑** | 手工逐条打平台 correlations 再人工判恢复 |
| `archive_submit_ready.py` | **`submit_ready` 终态残留归档**（移动非删除、可回滚）：把 DEAD/EXPIRED/SUPERSEDED/SUBMITTED 行移入 `submit_ready_archive`（含 `orig_id`/`batch`/`archive_reason`），主表只留活水。三重安全：同一事务 INSERT→DELETE、导出 JSON 快照到 `output_report/archive_submit_ready_<batch>.json`、`--restore <batch>` 完整迁回。**拒不带 `--region` 的整表操作**（须显式 `--all-regions`）。默认 dry-run 友好 | 手写 DELETE / 让终态行无限堆积成坟场 |
| `alpha_properties.py` | **Alpha 属性（name/color/tags）审计与规范化**。规范单一事实源 = `src/wqb/alpha_properties.py`（含平台**实测**的 color 硬枚举 5 值 `GREEN/BLUE/RED/YELLOW/PURPLE`，其余 400），文档 `docs/alpha_properties_spec.md`，审计证据 `reports/alpha_properties_audit_20260920.md`。子命令 `audit`（只读：name 形态/color 分布/tag 合规统计 + 告警清单）· `normalize`（**默认 dry-run**，`--apply` 才写：按 type/`PowerPoolSelected` 判定 `CH_*`、按表达式字段反查补 `SRC_<dataset>`、`--fix-color` 空色→`BLUE`；**不改 name**、**无条件保留 `RETIRE_*` 等已有标签**）。★ 全部 10 区域 ACTIVE(115) 已 `--apply` 规范化 | 手工逐颗改属性 |
| `restore_alpha_props.py` | **事故恢复**：1966 `set_alpha_properties` 全量覆盖曾清空 name / 覆写 description。从 `logs/_os_alphas_raw.json`（事故前转储，221 条）复原 name+regular/selection/combo description。**最小字段 PATCH**（只发要恢复的键，不碰 tags/color）。默认 dry-run，`--apply` 写 | 手工重写描述 |
| `name_missing.py` | 给仍缺 name 的 ACTIVE 补**唯一规范名**（`{REGION}_{R\|S}_{family}_{id尾6位}`；family 由表达式字段反查 SRC 推断）。**必须用 id 短码做后缀**（同族同源会撞名）。默认 dry-run，`--apply` 写 | 手工命名 |
| `finalize_props.py` | **SUPER 命名优化 + 超 5 标签瘦身**（规范化收尾）。SUPER 用 `<REGION>_S_<N>comp_<id6>`（`selectionLimit` 得组件数）；超 5 标签收紧到 ≤5，**必保 `CH_*`/`SRC_*`/`RETIRE_*`/`WAIT_*`**（运维/留痕标记不可砍）。精确 PATCH；默认 dry-run，`--apply` 写 | 手工 |

| `verdict/submit_inventory.py` | **「当前可提交候选清单」一跑即出**（2026-10-06 下沉；每日盘点主力）。⛔ 铁律：**只读平台、只判不提交**——绝不 POST `/alphas/{id}/submit`。判定口径与 `submit_verdict.py` **共用** `wqb.submit_verdict_core.decide`，不另起一套：模拟层 checks → 资格门（WebDataScope Failed-count，唯一权威；本地 `submit_ready.gate` 不可信）→ 相关性（`refresh=True`，>48h 视为过期必重测）。七分类输出 + `--no-csv`（只出 JSON）。★ **只读 `submit_ready` 表 ⇒ 从未入队的候选对它完全隐形**，补扫见 `ledger/scan_backup_ra.py` | 手工逐条查控制台 |
| `verdict/candidate_health_card.py` | **推荐候选「三层体检卡」**（2026-10-06 下沉）：① 闸层（`ra_failed_checks=0` / prod<0.7 / self<0.7 / turnover≤0.30）② 回报层（judge 六指标 + drawdown + 多空均衡）③ 加钱层（VF 三项：单α表现 / 多样性 / 独特性）。★ 补上 `submit_ready` 表**根本没有**的两项：`margin`（官方「好 alpha」线 >4bps）与**约束变体** `is.investabilityConstrained.*` / `is.riskNeutralized.*`（约束后普遍低 31–34%，平台真正扣分的是它们） | 手工拼体检表 |
| `verdict/verify_region_op.py` | **逐区核验平台 ACTIVE 的两种口径**（2026-10-06 下沉）：strict-active = `status=ACTIVE` 且 `osmosisPoints>0`（已分配 OP，排除 DECOMMISSIONED）vs 探针用的宽松 `active`（只看 status）。扫 OS+IS 阶段 `get_user_alphas(alpha_type="REGULAR")` 客户端按区过滤，出 `active_total` / `active_op` / `decom`，并**交叉校验** `active_total` 与探针缓存是否一致（不一致要报警） | 手比控制台与缓存 |

## 存量池卫生（门禁断链 / 积压裁决）

| 工具 | 用途 | 取代 |
|---|---|---|
| `backfill_gate_plan.py` | 无门禁波规划器（只读）：按 catalog 可行性把无 gate_results 的组分成 A 可立即补门禁（`--commands-file` 出逐组 wave_gate 命令）/ B 缺 catalog / C dataset 为 NULL / D 区目录缺失 | 手写 LEFT JOIN 逐区盘 |
| `backfill_catalogs.py` | 补缺失 typed catalog：枚举白名单缺集（scan_fields 走平台 API，**零配额**）→ `--apply` 逐个生成。2026-09-17 实测 JPN 10/10 成功（2m45s） | 手工逐集跑 scan_fields |
| `backfill_skeletons.py` | 为存量表达式回填骨架签名（`structural_signature`；只填 NULL、幂等、dry-run 默认）。写入侧已自动计算，此工具是一次性回填 | — |
| `pick_backlog_representatives.py` | 积压按骨架去重挑代表 → 直接产出 `mcp_7slot_batch.py --alpha-json` 可消费的清单；`--gate-filter` 先用当前门禁全量筛（失败者不回测），`--drop-list` 落盘失败者 id；**`--apply-drop`** 把失败者标 `dropped`（纪律终态）——三守卫：必须配 `--gate-filter` + `--db-backup`、只动 `alpha_id IS NULL` 且状态未变者、分批 rowcount 校验 + ledger 台账留痕 | 手工挑候选 / 手改状态 |

## 战役情报（S0 选集 / 点塔进度 / S4 预筛 / 幽灵算子）

| 工具 | 用途 | 取代 |
|---|---|---|
| `campaign_intel.py s0-select` | S0 选集增强：recommend_datasets（平台真实点塔）× mining_yield（历史产出率）× dead_datasets（判死清单）三方交叉 → 「未点亮塔 × 高产出 × 未判死」候选清单 | Agent 逐个调 MCP 再人工拼结论 |
| `campaign_intel.py pyramid` | 点塔进度快照：各 catalog 点亮状态/乘数/还差几颗（S6 回写时调，输出 `[key_findings]` 单行供直接嵌入 wave_result） | 手工查 pyramid 端点 |
| `campaign_intel.py s4-prescreen` | S4 预筛压缩：批量拉指标 → READY/REVIEW/REJECT 分层，REJECT 直接判死不进 S4 链 | 逐条 get_alpha_details 进 S4 链 |
| `campaign_intel.py ghost-audit` | 幽灵算子硬闸：检测表达式是否含平台不认的算子（S2 产物入库后、wave_gate 前调，防整批 CANCELLED 连坐） | 手写算子比对 |

## 区域态势与轮转（饱和检测 → 转区继续挖）

| 工具 | 用途 | 取代 |
|---|---|---|
| `region_status.py` | 区域状态记分板（本地 DB 驱动、零平台请求）：逐区回测量/sharpe 达标/命中率/ACTIVE/波次/战役 exhausted% + entry_verdict + 建议动作；`--json` 机读 | `brain-next-move-analysis §5.5` 区域饱和手算 |
| `region_status.py --rotate --current <R> --target <N>` | **区域轮转决策**：当前区证实结构性饱和→按证据（产出率/可行库存/prod 墙/战役穷尽/profile）排序推荐下一区并承接目标 N；`--write-ledger` 幂等写 `ledger_kv(<R>,region_rotation)`；`--json` 机读 | 人工逐区查表拼“换哪个区”结论 |

> 轮转判定/打分逻辑的**单一事实源** = `src/wqb/region_rotation.py`（纯函数，`tests/unit/06_wave_pipeline/test_region_rotation.py` 守护）；CLI（`region_status.py --rotate`）与 MCP（`mcp__wqb-db__region_rotation`）同源。关键纪律：`alphas.prod_correlation` 只对做过相关核查的 alpha 有值，**NULL prod ≠ 可行**（会假阳性），可行集/prod 墙仅在 measured 子集上判定，薄样本回 `data_caveat`；仍有未提交可行存量（feasible_unsubmitted≥`feasible_reprieve_min`）则豁免降级为 WATCH。

## 数据修复（一次性回填，幂等）

| 工具 | 用途 | 取代 |
|---|---|---|
| `backfill_expression_dataset.py [--apply]` | 修复 `expressions.dataset` 被写成 region 名（7,434/13,855 行，2026-09-15 审计）与 `backtest_results.dataset` 缺失：waves→datasets / wave 标签 / gate_results 三路解析，未解析者置 NULL；默认干跑，`--apply` 先备份再写 | 手写 UPDATE SQL |
| `migrate_wave_verdict_enum.py [--dry-run]` | `wave_results.verdict` 归一到 PASS/FAIL/PARTIAL（前缀/关键词规则，原文入 key_findings 首条）；写入侧 `mcp__wqb-db__upsert_wave_result` 已同规则强制 | 人工改行 |
| `backfill_check_columns.py [--apply]` | 回填 **checks 派生列**（`cluster_test` / `concentrated_weight` / `sub_universe_sharpe`）。★ 2026-09-19 修复配套：`harvest_multisim._pick_checks` 此前找的 4 条路径全落空（真实位置是**顶层 `is.checks`**）→ `cluster_test` 一度 0/4,926。本工具用平台详情补齐存量：默认 scope=ACTIVE、只填 NULL、幂等、断点续跑（state 文件）、dry-run 默认。**需用 MCP venv 的 Python 跑** | 逐条手查详情 |

| `data-repair/backfill_alpha_metrics_from_platform.py` | **从平台补 `alphas` / `submit_ready` 缺失的 IS 指标**（2026-10-06 下沉）：`two_year_sharpe` / `sub_universe_sharpe` / `is_ladder_sharpe`，以及体检卡三层所需的 `margin` 与约束变体指标。★ 全库实测 **1798/11002 行 2Y 为 NULL**（两条成因：`sync_platform_alphas` 曾显式传 `None`；非 harvest 路径从不抽 2Y/sub）。**只补空**（`--overwrite` 才覆盖）、每颗落盘断点续跑、默认 dry-run。★ 其 `extract_is_metrics()` 被 `sync_platform_alphas.py` 复用（跨目录导入，改动路径须同步）；**不改 ingest 逻辑、不改回测** | 手工逐条查平台补库 |

## Cluster Alpha（低门槛区刻意版；依据帖 43562853669655）

| 工具 | 用途 | 取代 |
|---|---|---|
| `build_cluster_variants.py` | 生成**刻意版** cluster 变体：从区域存量信号（默认 `gated`）按骨架去重后套文章配方 —— `cross`=rank(group_mean(SIG,cap,industry))、`equal`=group_normalize 等权行业、`guard`=group_count 防薄行业、`timing`=轮动×择时（区域级）。产出**逐条过当前门禁**（注入 `_region` 触发闸2b），只输出通过者；settings 强制 `neutralization=MARKET`（行业中性化=按构造删掉 cluster 结构）。**JPN 硬拒绝**（闸2b 实测 industry/sector/subindustry 不可用，整批连坐） | 手写 cluster 表达式 |

## 代码体检 / 清理

| 工具 | 用途 | 取代 |
|---|---|---|
| `scan_test_groups.py` | 测试用例扫描与分组：AST 静态分析 + `pytest --collect-only` 取真实 nodeid，按 `tests/unit/NN_xxx` 十个编号域 + `tests` 根级 + MCP 包共 12 组，产物 `cache/test_groups.json`（供 `run_grouped_tests.py` 消费）；`--refresh` 强制重扫 | 仓库根 `wq_test_scan.py`（工作台 UI 已下架） |
| `run_grouped_tests.py` | **全量测试并行跑批器**：按上表 12 组各跑各的 nodeid（`ThreadPoolExecutor`，默认 `--workers 4`），解析 passed/failed/skipped/errors/duration 与失败清单，出 markdown 报告到 `output_report/fulltest_report_<YYYYMMDD_HHMM>.md`。参数与 `pytest tests/ -x` 同口径（`-q --no-header -p no:cacheprovider -ra`）；全量并发跑受 `logs/_slots`/`_dblock` 共享态影响（P8），先看单组绿再信全量 | 仓库根 `wq_fulltest_run.py` |
| `scan_deadcode.py` | 死代码只读扫描：未用 import + 死定义（排除注册式装饰器 @mcp.tool()/@fixture 等反射调用）；支持 `--path` 单文件/子目录、`--out` JSON 报告 | `tracking/_scratch/_scan_deadcode*.py` |
| `code-audit/db_mcp_split.py` | **根入口 `wqb_db_mcp.py` 的拆分生成器**（一次性工具，非通用）：分组表 + 顶层常量按使用点自动归位 + 函数体逐字节搬运（只把 `str(DB_PATH)` 等价换成 `get_db_path()`）+ **写盘前组间 DAG 环硬门**（实测 `mutations ↔ harvest`、`rotation ↔ mutations` 互引成环，拆开就是包内循环 import → 服务启动即挂）。`--plan` 只出报告 / `--apply` 写盘。执行顺位与 26 条待改断言见 `reports/db_mcp_split_20261004.md` | 下次拆分时重新发明分组表与环检测 |
| `code-audit/mcp_surface_diff.py` | **MCP 工具面快照与比对**（拆分/重构的回归凭据）：比对 tool 名集合 / docstring / inputSchema 三项全等，“逐字节搬运不改行为”只能这样机器证明；`--tag before` 建基线 → 改动 → `--tag after` 自动比对（快照落 `cache/mcp_surface_<tag>.json`）；退出码 0=一致 / 1=有回归 / **2=工具故障（与回归区分，导入失败不算回归）** | 靠人眼看 diff 相信“重构没改行为” |
| `refs_scan.py` | **文件级引用核验**（归档前必跑，只读）：token 级匹配且额外按 `.`/`/`/反斜杠切分索引（防 dotted import 漏判），默认排除全仓路径快照件（`py_complexity_scan.json`/`MANIFEST.json` 等，否则任何文件都「被引用」），并标 `__main__` 区分库模块与未登记 CLI；`--dir <目录>` / `--names a,b` / `--show-hits` / `--only-zero` / `--out`。**refs=0 只是必要条件**，仍需人工看命中形态（AGENTS.md §8.5） | 每次归档前重写的 `_tmp_ref_check*.py` 一次性脚本 |
| `fix_bom.py` | BOM(U+FEFF) 剥离修复：默认 `--dry-run` 列出含 BOM 的 .py；`--apply` 才修（备份 + CJK 数量校验 + ast.parse 校验） | `tracking/_scratch/_fix_bom.py`（**已删**） |
| `clean_unused_imports.py` | 清理未用 import：默认 `--dry-run` 列出；`--apply` 才删（**跨文件 re-export 校验**防 SHAPE_CLASSES 误删 + `.bak_imp` 备份 + ast.parse 校验）；可 `--report` 接 scan_deadcode 的 JSON | `tracking/_scratch/_clean_unused_imports.py`（**已删**） |
| `audit_node_registration.py` | **新增/修改 workflow 节点必跑**：审计「四处同步」——① registry.py 注册与 NodeMeta 签名 ② `test_registry_lists_all_core_nodes` 期望集合 ③ `_DRY_RUN_CASES` 用例表 ④ INDEX.md 节点计数。`--node X` 单节点自检；退出码 1 = 有漂移并列出全部缺口 | 改一处跑一次测试的往返 |
| `audit_structure.py` | **仓库结构守护（2026-09-30 新增，已挂 pre-commit）**：S1 sys.path 自举/外挂分类 · S2 src→tools 依赖方向 · S3 tools 与 src 同名模块 · S4 硬编码盘符路径 · S5 reports/ 里的散落脚本 · S6 skills 副本漂移。`--only s1` 跑单项。只读；S1/S2/S4 判 FAIL，S3/S5/S6 判 WARN（存量不阻塞） | 靠 AGENTS.md 文字纪律 |
| `code-audit/repo_governance_check.py` | **未跟踪源码数 = 事故唯一先行指标**（2026-10-06 新增，已挂 pre-commit）：数出「`git ls-files` 之外、且不在运行期/归档目录（`logs`/`cache`/`data`/`attic`…）下的源码类文件」（`.py/.md/.json/.sh/…`）。动机：本仓反复发生「源码从未入库、只以工作区未跟踪文件存在」，`git clean -fd` 一清即**永久**丢失（`tools/` 一次丢 17 个脚本）；`audit_structure.py` 的 S11 只看**顶层脚本数量**，看不见这类缺口。退出码 0=干净 / 1=有未跟踪源码（"下次清理会带走 N 个"）/ 2=无法判定。`--json` / `--quiet` | 事后从 git 里捞不回来的损失 |
| `code-audit/doc_path_refs.py` | **活文档引用的仓库内路径必须真实可达**（2026-10-06 新增，已挂 pre-commit）：把「文档 → 路径」变成可机检断言，分两类 —— **BROKEN**（文档引用了，但 git 未跟踪**且**磁盘不存在 ⇒ 文档腐烂 / 又一批丢失件）与 **UNTRACKED**（磁盘在、git 不在 ⇒ 事故前兆）。范围 = `AGENTS.md`/`README.md`/`CLAUDE.md`/`tools/README.md` + `docs/`（除 `plans/`）+ `Claude/skills/`；`data`/`logs`/`cache`/`attic` 等**按设计不入库**的根、`.gitignore` 命中的路径、以及写明「不存在/已归档/旧文」的行整体豁免（与 `skill_lint.py` 同口径）。**棘轮**：存量违规记 `tests/fixtures/doc_path_refs_baseline.json`，只对**新增**违规 FAIL。与 `skill_lint.py` 的 `path-token` 分工：后者管 skills 目录内的细粒度死指针，本工具补上**非 skills 活文档 + git 索引维度**。`--report`/`--json`/`--update-baseline` | 人工逐个点开文档核对；以及「文档承诺的路径其实早就没了」 |
| `code-audit/audit_destructive_default.py` | **「默认即破坏」守护**（2026-10-06 新增，已挂 pre-commit）：AST 扫模块级（`def`/`class` 之外，即 **import 时就会执行**）的写盘/删除调用（`write_text`/`unlink`/`rmtree`/`open(...,'w')`/`json.dump`/`to_csv`…），若其**前置**没有「提前退出型开关」（`if ...: sys.exit()`，test 提到 `apply`/`dry`/`plan`/`force`/`confirm`）⇒ 报 **DRY-RUN-MISSING**。动机是 2026-10-06 的实测事故：`db_mcp_split.py` 的开关（`--plan`）在破坏性写盘**之后**，跑一次 `--help` 就把被跟踪的 2808 行文件截成 91 行。**已认可的解法**＝把破坏性动作整个收进 `def main()` + `if __name__ == "__main__"` 守卫（工具不进函数体，故不再报）；`__main__` 块**内**的调用归 ADVISORY（不判失败）；`PARSE-FAIL` **只告警不阻断**（编辑中间态居多，硬卡只会训练出 `--no-verify`）。**棘轮**：存量记 `tests/fixtures/destructive_default_baseline.json`（键 `file::kind::detail`，**不含行号**），只拦新增。`--all`/`--json`/`--path`/`--update-baseline` | 靠人记住「默认只读、落盘要 `--apply`」这条文字纪律 |
| `audit_skill_drift.py` | skills 脚本副本漂移检测：A 类（GEM 内嵌快照，设计内）不报，只报 B 类跨 skill 复制（`validator.py` 4 份 / `helpful_functions.py` 4 份 / `ace_lib.py` 2 份）。`--check` 只判退出码，`--json` 机器读 | 手工 md5 对比 |
| `clean_logs.py` | `logs/` 运行期清理：默认 dry-run，`--apply` 才删；`--report-locked` 探测 ACL 锁死目录并打印**需管理员执行**的 takeown/icacls/rmdir 命令（不自行提权——删除纪律要求人工确认） | 手工清 logs |

> 三者均遵循 dead-code-cleanup skill 红线：**默认只读/dry-run，删除动作必须显式 `--apply`**。原稿已归档 `attic/tools_archive/_2026-08-28_*`。
>
> 另有 skill 资产同步（不属清理类）：
> | 工具 | 用途 | 取代 |
> |---|---|---|
> | `sync_gem_embedded_skill.py` | 同步 GEM 引擎内嵌的两份 skill 副本到顶层权威版：`brain-feature-implementation/SKILL.md` 与 `brain-data-feature-engineering` 的 `reference.md` / `examples.md` / `OUTPUT_TEMPLATE.md`（同名文件不许互相矛盾；**它们不会被拼进 LLM prompt**，2026-09-29 更正，2026-09-26 前内嵌 FI 停在 49 行旧英文稿）。`--check` 只校验（退出码 1 = 漂移）、`--apply` 覆盖写入。**绝不动内嵌 `scripts/`**（`ace_lib`/`validator` 是引擎硬依赖），也不创建 dfe 的 `SKILL.md`。由 `tests/unit/03_gem/test_gem_skill_paths.py` 守护 | 手动复制 |

## MCP 体检

| 工具 | 用途 |
|---|---|
| `mcp_ping.py` | MCP 服务连通性与调用计时；`--service X` 单服务、`--full` 工具清单、`--timeout N` 每次请求写入及响应的等待上限。显式调用：`--call TOOL --args-file args.json` 或 `--calls-file calls.json`（`[{"tool":"...","args":{}}]`）。工具错误退出码 1；超时退出码 2，包含 method/tool/request_id/outcome_unknown/retry_safe=false，废弃连接且停止后续调用。超时不证明远端未执行，先核对任务/DB再决定重试。默认探针只读；显式调用具有所选工具的效果。 |
| `start_wq_mcp.py` | 启动/确保 `wq-brain-http` MCP 服务在 8876 可用（防"论坛工具找不到"） | `--check` / `--wait N` | — |

## 平台台账同步

| 工具 | 用途 |
|---|---|
| `sync_platform_alphas.py` | 把平台 OS 池（已提交 alpha）全量同步进本地 `alphas` 表，含 **OS（样本外）指标**（`os_sharpe`/`os_fitness`/`osISSharpeRatio`/`os_sharpe60-500` 等 15 列）。解决「平台 228 个已提交 vs 本地台账 94」的漏记缺口（2026-09-20 实测漏 134 条）。`--dry-run` 只报告差异、`--baseline` 打印 OS 衰减基线、`--region X` 限定统计视角。走 MCP venv（brain_api），零配额（只读平台） |

| `ledger/scan_backup_ra.py` | **备选 RA 补扫**（2026-10-06 下沉）：把「全闸但未入队」的候选自动补进 `submit_ready`（默认 dry-run，`--apply` 落库）。★ 动机：`verdict/submit_inventory.py` 只读 `submit_ready`，任何「在 `alphas` 里躺着、却从未入队」的达标候选对每日盘点**完全隐形**（典型受害 `WjegEmQO`：EUR S1.94/F1.38/2Y1.59/sub1.96，实测 prod 0.5012/self 0.1616 全过，却连续多轮扫不到）。★ 口径：`2Y/sub` 用 `(x IS NULL OR x >= ?)` 放宽、缺值行进「待核」列，`--apply` 默认跳过待核行（`--apply-pending` 才含） | 手工 SQL 补录 / 让达标候选沉底 |
| `ledger/enqueue_propose.py` | **入队「三层裁决」网关**（2026-10-06 下沉）：L1 策略筛（平台 RA 检查干净 + S/F + 2Y/TO + 非 add_mix + prod/self）→ L2 择优（同族只留代表 + 塔优先 + `--top-per-region`）→ L3 人工确认。★ 政策依据：**入队必须有人工/策略裁决，不做「全闸即自动入队」**——实测全量入队 64% 立即 DEAD（`alphas` 里 S≥1.58/F≥1.0/prod<0.7 的未入队候选 393 条，251 条平台 RA 硬闸已 FAIL）。`--apply --proposal <json> --approved-by <人>` 才落库（校验哈希 + 重跑 L1），缺批准/哈希不符退出码 4；决策留痕 `results/enqueue_decisions.jsonl` | 手工挑候选入队 / 凭 S、F 线拍脑袋 |

## 纪律（AGENTS.md §9）

1. **禁止新建** `_gate_*` / `check_*batch*` / `probe_*sa*` / `_submit_*` / `track_*_super*` 类一次性脚本；先用本索引查工具。
2. 缺参/缺能力 → 改对应工具加参数（保持 `--help` 自文档），不写新脚本。
3. 一次性排障探针仍可写 `tracking/_scratch/`，但完成即归档 `attic/`，不留在活跃目录。

## 相关参考

- 战例权威实现：`~/.qoder-cn/skills/wq-brain-campaign-toolkit/scripts/`（`WQ_TOOLKIT_DIR`）
- 平台 API 封装：`world-quant-brain-mcp/brain_api.py`（`BrainApiClient`，自带 429 退避/Redis 缓存）


## 存量CLI 补登记（2026-10-05）

本节收录**顶层有 `__main__`（真命令行入口）但既不在上文各功能节、也无其他文档提及**的脚本。
它们不是死代码：`git grep` 显示零引用只说明「没人从代码里 import 它」，
命令行工具本就靠人敲。按 AGENTS.md §8.5 判据（有 CLI 入口 → 未登记的 CLI → 文档缺口，不能删），
此处补登记。**引用为零不代表该删**——要判断是否还有用，看模块 docstring 与 `--help`。

| 工具 | 用途（模块 docstring 首句） | 调用形态 |
|---|---|---|
| `atom_labeler.py` | WorldQuant BRAIN "atom / combined" 信号分类器（CLI + 批量回写）。 | 需参数 |
| `audit_dead_code.py` | 高置信度死代码侦察（只读，不删任何东西）。 | 无参直跑 |
| `audit_file_sizes.py` | 全量扫描项目内 Python 文件：行数 / 函数类规模 / 圈复杂度 / 职责数量。 | 无参直跑 |
| `combo_precheck.py` | 组合预检串联工作流（P1-C + P1-D，2026-08-31）。 | 需参数 |
| `db_maintenance.py` | wqb.db 维护工具（2026-09-20 L4）。 | 需参数 |
| `demo_layered_mining.py` | 层层推进挖掘策略演示 | 无参直跑 |
| `field_axis.py` | 字段信息轴自动识别（P0-B，2026-08-31）。 | 需参数 |
| `field_quality_scorer_v2.py` | 8 维字段质量评分器. | 需参数 |
| `field_signal_mine.py` | L0 零回测选基：从 backtest_results 的表达式文本挖【字段级】与【字段对】历史信号先验。 | 需参数 |
| `five_slot_executor.py` | 五槽并发执行器 (Five-Slot Executor) | 无参直跑 |
| `fix_db_residuals.py` | 数据修复脚本：同步 expressions 指标 + 清理残留 + 删旧表 + 补 campaign_state。 | 需参数 |
| `fix_wave_backfill.py` | 波级低覆盖字段 ts_backfill 修复器（幂等）。 | 需参数 |
| `fix_wave_vectors.py` | 波级 VECTOR 字段 vec_* 包裹修复器（幂等）。 | 需参数 |
| `gem_validator.py` | GEM 候选池强制校验。 | 需参数 |
| `kor_ledger_write.py` | KOR 台账写入（wqb-db MCP 未连接时的降级写库）。 | 无参直跑 |
| `operator_diversity_analyzer.py` | 算子多样性分析器. | 需参数 |
| `pipeline_integration.py` | （无模块 docstring） | 需参数 |
| `populate_external_fields.py` | 灌 external_fields 表。 | 需参数 |
| `pre_backtest_filter.py` | 回测前快筛闭环（self/PPAC + 关键闸）。 | 需参数 |
| `role_cluster.py` | 职责聚类 + 跨文件重复逻辑检测（只读）。 | 无参直跑 |
| `s0_enhanced_screening.py` | S0 数据集体检增强预筛（WebDataScope 零成本预筛）。 | 需参数 |
| `seed_region_priors.py` | 区域 priors 自动装配器（evidence-driven，不手写、不编造）。 | 需参数 |
| `skeleton_origin_report.py` | 骨架来源过闸率报告：forum（论坛来源） vs native（原生）对比。 | 需参数 |
| `step_event_log.py` | 步级评估 T2 事件台账 CLI（2026-09-30 方案 B）。 | 需参数 |
| `success_formula_engine.py` | 成功配方推广引擎。 | 需参数 |
| `three_dataset_probe.py` | 3 数据集组合边界探索计划生成（P2-3，2026-08-31）。 | 需参数 |
| `validate_fields_batch.py` | 批量字段可用性验证器（区域无关）。 | 需参数 |

## 全量 CLI 索引（机器生成，2026-10-05）

本节由 `tools/` 顶层**有 `__main__`（真命令行入口）但正文各节未提及**的脚本汇总而成，
按「谁在用它」标注首个引用点。生成口径与工具链治理见 `tools/THEMES.json`。

| 工具 | 一句话用途 | 首个引用点 |
|---|---|---|
| `_pyenv.py` | tools/_pyenv.py — 工具脚本共用的解释器 / MCP 目录解析（跨平台）。 | `Claude/skills/CHANGELOG.md` |
| `ab_test_framework.py` | ab_test_framework.py — 多维骨架标签对比实验框架 | `docs/reference/multidim_ab_test_report_template.md` |
| `authority_claims.py` | authority_claims.py — SKILL.md / INDEX.md 里「唯一权威 / 唯一事实源 / 唯一入口…」宣称的计数（棘轮基线维护） | `Claude/skills/CONTRACT.md` |
| `backfill_longcount.py` | backfill_longcount.py — 从平台补回 is 段持仓广度指标（longCount/shortCount/pnl/bookSize）。 | `docs/env_and_switches.md` |
| `backfill_prod_corr.py` | backfill_prod_corr.py — 补测 pc_null alpha 的平台 prod_correlation（2026-09-02）。 | `docs/env_and_switches.md` |
| `batch_submit_verdict.py` | batch_submit_verdict.py - 对 submit_ready 表中 IS_ONLY 的候选批量跑提交层相关性校验。 | `docs/plans/2026-09-23-dryrun-audit-optimization-plan.md` |
| `build_field_index.py` | build_field_index.py — 构建/补齐「平台级字段→数据集索引」（降低 atom 判定的 unknown）。 | `tests/unit/01_store_db/test_build_field_index.py` |
| `build_gate_prior_from_inventory.py` | build_gate_prior_from_inventory.py — 用账户历史 alpha 库存反哺 GEM 先验。 | `Claude/skills/CHANGELOG.md` |
| `category_field_triage.py` | category_field_triage.py — 一个 region×category 下所有数据集的「字段分诊」总表。 | `Claude/skills/wq-brain-campaign-toolkit/scripts/scan_fields.py` |
| `cleanup_async_tasks.py` | logs/_async_tasks TTL 归档清理工具（2026-09-25 结构优化目标 D）。 | `src/wqb/workflow/_common.py` |
| `closure_ledger.py` | closure_ledger.py — skills 审查（reports/skills_review_20260929.md）条目的「处置登记」（评审 → | `docs/skills_review_closure.json` |
| `concept_overlap.py` | concept_overlap.py — 概念重叠检查（skills 审查 EX-01 / EX-10）。 | `Claude/skills/CHANGELOG.md` |
| `db_lock_audit.py` | db_lock_audit.py - wqb.db 写锁探针（2026-09-20 L2）。 | `tests/unit/01_store_db/test_db_write_guards.py` |
| `diag_forum_read.py` | forum_recon 读帖链路最小诊断（只读、零回测配额）。 | `Claude/skills/brain-alpha-research/SKILL.md` |
| `discover_datasets.py` | discover_datasets.py - 数据集发现（灌 datasets 表）。 | `Claude/skills/INDEX.md` |
| `dryrun_multidim.py` | dryrun_multidim.py — 多维骨架标签 dry-run 验证脚本 | `docs/reference/multidim_production_deployment.md` |
| `dynamic_recipe_weighter.py` | dynamic_recipe_weighter.py - 成功配方动态权重. | `docs/design/skills_review_decisions.md` |
| `economic_mechanism_kb.py` | economic_mechanism_kb.py - 经济机制知识库. | `Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skeletons.py` |
| `economic_mechanism_templates.py` | economic_mechanism_templates.py - 经济学机制模板库. | `Claude/skills/brain-forum-browse/SKILL.md` |
| `export_wave_ledger_md.py` | export_wave_ledger_md.py - 从数据库生成 WAVE_LEDGER.md 快照（单轨 DB 模式）。 | `Claude/skills/wq-brain-campaign-toolkit/SKILL.md` |
| `fetch_dataset_assets.py` | fetch_dataset_assets.py - 全 Region 数据集资产拉取（**直连入库**，不落 JSON）。 | `Claude/skills/INDEX.md` |
| `field_catalog_cache_manager.py` | field_catalog_cache_manager.py - S1 字段扫描缓存管理工具。 | `docs/S1_FIELD_CATALOG_CACHE_GUIDE.md` |
| `field_inspect_gate.py` | 体检→表达式硬门（S2→S3 第二道硬门）的可执行接线。 | `Claude/skills/INDEX.md` |
| `field_pool_ab.py` | field_pool_ab.py — 字段分类→GEM 机制 A/B 评估器（2026-09-26 落地）。 | `docs/ledger_keys.json` |
| `field_profile_backfill.py` | field_profile_backfill.py - 从 WebDataScope zip 解析字段画像并回填 data/wqb.db。 | `Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/pipeline_kb.py` |
| `field_profile_from_labs.py` | field_profile_from_labs.py - 把 BRAIN Labs 批量画像 JSON 入库 field_profile 表。 | `docs/ledger_keys.json` |
| `field_quality_scorer.py` | field_quality_scorer.py - 字段质量预筛器. | `Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skeletons.py` |
| `field_semantic_classify.py` | field_semantic_classify.py — 数据集字段的经济含义归类（S1 补做环节）。 | `Claude/skills/CHANGELOG.md` |
| `forum_cache_builder.py` | Forum post cache builder for brain-alpha-robustness Phase A. | `Claude/skills/CHANGELOG.md` |
| `gen_field_inspect_packs.py` | 从 WebDataScope 数据包生成体检硬门用的按数据集分文件体检包。 | `Claude/skills/CHANGELOG.md` |
| `gen_inspect_from_db.py` | 从 wqb.db fields 表生成降级版体检包（P1-4 HKG 解锁，2026-09-07）。 | `tests/unit/10_toolkit_scripts/test_inspect_degraded_pack_marking.py` |
| `ind_sim_submit.py` | IND 战役专用：按精确 settings 直连 POST /simulations（multi-sim），绕开 CLI 固定档。 | `Claude/skills/CHANGELOG.md` |
| `ingest_dataset_assets.py` | ingest_dataset_assets.py - 把 fetch_dataset_assets.py 拉取的 JSON 批量写入 wqb.db。 | `docs/skills_review_closure.json` |
| `kb_templates.py` | KB 社区模板库读取/过滤/导出工具（P1-5：让 59KB 社区模板回流生成端）。 | `Claude/skills/brain-alpha-research/SKILL.md` |
| `tracking/KOR/scripts/kor_opportunity_scan.py` | KOR 机会空间穷举扫描（S-PRE 用，2026-09-28；2026-10-05 由 tools/ 迁出，区域专属）。 | `docs/experience/03_region_dataset.md` |
| `ledger_keys.py` | ledger_keys.py — 台账（ledger_kv）键目录：扫描器 + 目录读取 + 文档表生成（库 + CLI）。 | `Claude/skills/CHANGELOG.md` |
| `market_regime_adapter.py` | market_regime_adapter.py - 市场状态适配器. | `Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skeletons.py` |
| `migrate_phase2.py` | migrate_phase2.py - Phase 2 迁移：registry 实证层 + wave 结果台账 + 跨区教训入 SQLite。 | `docs/skills_review_closure.json` |
| `migrate_priors_cache_key.py` | migrate_priors_cache_key.py — 消除 priors 快照的大小写撞键（2026-09-17 P2-12）。 | `docs/ledger_keys.json` |
| `migrate_profile_datasets.py` | 一次性迁移：14 个 region profile 的 datasets 块 → 精确化结构形态（2026-10-01）。 | `Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md` |
| `mode_b_qualify.py` | mode_b_qualify.py — Mode B 资格判定的 CLI 入口（skills 审查 OP-18 / HP-15 / X-16）。 | `Claude/skills/CHANGELOG.md` |
| `modeb_improvement_pipeline.py` | Mode B Idea Layer Improvement Pipeline - Integrated Workflow. | `docs/design/submit_queue_design.md` |
| `neut_cache.py` | neut_cache.py - 中性化×数据集缓存表（P1-1，2026-08-31）。 | `Claude/skills/wq-brain-campaign-toolkit/scripts/pipeline.py` |
| `normalize_ledger_whitelist.py` | normalize_ledger_whitelist.py — 把 `s0_whitelist` 归一为统一契约（2026-09-17 P0-4）。 | `docs/experience/04_engineering.md` |
| `normalize_wave_ids.py` | normalize_wave_ids.py — 回填裸时间戳波号（2026-09-17 P2-6）。 | `src/wqb/wave_id.py` |
| `ppa_handoff.py` | ppa_handoff.py — PPA（Power Pool）人工提交通道的交接单与回写（skills 审查 SB-22）。 | `Claude/skills/worldquant-submit-alpha/SKILL.md` |
| `preflight_wave.py` | preflight_wave.py - 波次前置条件预检与自动修复（区域无关，通用）。 | `Claude/skills/wq-brain-ra-pipeline/references/step5-gates.md` |
| `prescreen_gate.py` | 区域切换预筛门禁（P1-7：把 field-quality 的强制纪律机器化）。 | `Claude/skills/brain-alpha-research-field-quality/SKILL.md` |
| `prod_saturation_gate.py` | PROD 饱和闸（S2 生成层前移，2026-09-07 P1-1）。 | `Claude/skills/wq-brain-campaign-toolkit/SKILL.md` |
| `profile_drift_check.py` | 区域 profile 漂移体检（profile green/red 精确层 ↔ DB 实证）。 | `Claude/skills/wq-brain-ra-pipeline/references/region-profile-contract.md` |
| `quality_control_engine.py` | （无模块docstring） | `docs/reference/quality_control_landing_summary.md` |
| `refresh_operator_catalog.py` | 把 ``get_operators`` 的实时输出刷进 docs/reference/operators_catalog.json。 | `docs/reference/operators_catalog.json` |
| `retention.py` | retention.py — data/ cache/ logs/ 运行期保留策略（2026-10-03 立项） | `tests/unit/01_store_db/test_retention.py` |
| `s2_field_validator.py` | s2_field_validator.py - S2 表达式字段强制校验器 | `Claude/skills/brain-data-feature-engineering/SKILL.md` |
| `select_ra_basket.py` | select_ra_basket.py — 从过闸候选池选出 N 条互不相关、可提交的 RA 篮子。 | `Claude/skills/CHANGELOG.md` |
| `skeleton_tags.py` | skeleton_tags.py — 多维骨架标签提取器（经济学构造链感知） | `docs/reference/multidim_ab_test_report_template.md` |
| `skill_lint.py` | skill_lint.py — skill 文档「内容为真」的机械检查（库 + CLI）。 | `Claude/skills/CHANGELOG.md` |
| `step9_audit.py` | step9_audit.py — 步 9（S6）完成定义只读校验器（2026-10-02 新增）。 | `Claude/skills/wq-brain-ra-pipeline/SKILL.md` |
| `step_funnel.py` | step_funnel.py — 步级漏斗（S2→S6）只读推导，单一事实源（2026-09-17 新增）。 | `Claude/skills/CHANGELOG.md` |
| `structural_reconstruct_cli.py` | structural_reconstruct_cli.py - 结构重构命令行工具. | `docs/design/structural_reconstruction.md` |
| `test_field_catalog_cache.py` | test_field_catalog_cache.py - S1 字段扫描缓存功能**手动校验脚本**。 | `docs/S1_FIELD_CATALOG_CACHE_GUIDE.md` |
| `update_operator_stats.py` | 工具：统计区域算子使用频率并写入 region_kb（供 assemble_priors 注入 GEM）。 | `docs/experience/field_operator_pattern.md` |
| `waiver.py` | waiver.py — 闸「放行 / 豁免」台账协议的命令行（实现见 src/wqb/waiver.py）。 | `Claude/skills/GLOSSARY.md` |
| `wave_results_writer.py` | wave_results_writer.py - wave 结果台账入库工具（单轨 DB 模式，DirectDBWriter 优化版）。 | `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/wave_results.py` |
| `webdata_quality.py` | WebDataScope 数据包 → 数据集/字段/中性化/预处理全景分析。 | `Claude/skills/alpha-template-labs-data-analysis/SKILL.md` |
