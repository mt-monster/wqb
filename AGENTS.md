# AGENTS.md — wqb（WorldQuant BRAIN Alpha 挖掘工作区）

## 1. 项目概述与模块职责

本工作区用于 WorldQuant BRAIN 平台的 alpha 挖掘、回测、评审与提交，Python 脚本驱动，无统一应用框架；MCP 服务是本项目与编码 Agent 的主要接口。

| 目录 | 职责 | 变更注意 |
|---|---|---|
| `tracking/` | 区域战役追踪（KOR/USA/EUR/IND/GLB/DEU…）：candidates/results/reviews/scripts | `tracking/mining/` 为共享数据湖，勿改动/移动；全量索引见 `tracking/reference/tooling/generate_manifest.py`（`MANIFEST.json` 当前未生成） |
| `tools/` | 工具链（字段解析、质量检查、同步等）；**新脚本一律进这里**，索引见 `tools/README.md` | 被多区域脚本引用，改动前先查调用点 |
| `src/wqb/` | **规范核心包（single source of truth）**：config/expression/research/search/memory；区域/算子/中性化域常量唯一来源（见 `config.py`） | 行为变更须保持根 `tests/` 全绿（数量以 `pytest --collect-only -q \| tail -1` 为准，不在此硬编码） |
| `tests/` | pytest 单元测试（根 `tests/` + MCP 包 `world-quant-brain-mcp/tests/`；数量以 collect-only 为准；根 `tests/` 递归包含 `tests/unit/`，见 §4） | 见 §4 |
| `world-quant-brain-mcp/` | MCP 服务（`wq-brain-http`）：`brain_api.py` 为门面（36 行），方法体 verbatim 拆至 `brain_mixin_transport/auth/simulation/spcread/correlation.py`；模型 `brain_api_models.py`、配置 `brain_config.py`；回测/提交/论坛工具在 `tools_*` | 运行中服务，改 `brain_mixin_*` 需回归 `world-quant-brain-mcp/tests/` |
| `docs/` | 计划、参考、经验文档（**长期规范 / SOP / 速查**，不写一次性结论） | 行为变更需同步相关文档 |
| `reports/` | **人工审计与复盘**报告（结构审计、DB 审计、评审复盘） | 与 `output_report/` 分工判据见 §8.13 |
| `output_report/` | **报告唯一出口**（2026-10-01 组织审计定案）：战役 / ideas / 评审**产物**，含工具直写文件（`archive_submit_ready.py`、`complexity_scan.py`、`run_grouped_tests.py`） | 工具按路径直写，改目录要先查写方 |
| `data/` | 运行期数据与规范库 `data/wqb.db`（只读数据，整体 gitignore） | 备份数受 `test_retention.py` 硬闸（≤ 2），清理走 `tools/retention.py` |
| `attic/` | 隔离归档，**日期化归档包** `<主题>_<YYYYMMDD>/`（现状：`root_clutter_*`/`ppa_mining_*`/`mining_scripts_20261004`/`forum_workbench_20261004`/`brain_api_backup` 等） | 只读归档，勿回迁进活跃代码；除早期存量外不入仓库 |
| `cache/` `logs/` `results/` | 断点 / 日志 / checkpoint 等运行期产物（均已 gitignore） | `results/` 的续跑断点被 `backfill_longcount.py`、`batch_submit_verdict.py`、`prod_blocked_recheck.py` 硬编码引用，**移动会破坏续跑** |
| `research-data/` `extensions/` | 外部数据包与浏览器扩展源（gitignore，只读） | `research-data/operators_platform_*.json` 被 `op_arity.py` 读取，整目录不可动 |

## 2. 核心入口文件

- `world-quant-brain-mcp/main.py` — MCP 服务入口（`.mcp.json` 注册为 `wq-brain-http`；**HTTP 常驻**——缺省 `MCP_TRANSPORT=streamable-http` 监听 `127.0.0.1:8000/mcp`，需先用 `tools/start_wq_mcp.py --all` 把服务起起来；`MCP_TRANSPORT=stdio` 为遗留路径）
- `world-quant-brain-mcp/brain_api.py` — BRAIN API 客户端**门面**（36 行）；方法体 verbatim 拆至 `brain_mixin_transport/auth/simulation/spcread/correlation.py`，保持 `BrainApiClient` 类名与 `brain_client` 单例 + 旧导入路径（`from brain_api import brain_client/BrainApiClient/load_config/SimulationSettings/...`）不变
- `world-quant-brain-mcp/brain_api_models.py` — 纯数据模型（Pydantic）：`AuthCredentials`/`SimulationSettings`/`SimulationData`
- `world-quant-brain-mcp/brain_config.py` — 配置函数：`_resolve_config_path`/`_load_dotenv_into_environ`/`load_config`
- `world-quant-brain-mcp/mcp_core.py` — MCP 工具注册与分发
- `src/wqb/config.py` — **规范域常量**：区域/算子家族/中性化（数据源 `data/operators_verified.json`）；MCP 包与 `pipeline/`/toolkit scripts 共享引用
- `tracking/reference/tooling/generate_manifest.py` — 追踪目录全量索引生成器（产出 `tracking/MANIFEST.json`，当前未生成；注意该脚本会顺带把 >500 KB 文件 zip 归档到 `tracking/archive/large/`）
- `pytest.ini` — 测试配置（验证路由）
- `world-quant-brain-mcp/Makefile` — Docker 部署入口（`make up` / `make down`）

## 3. 变更影响范围指引

- 修改 `world-quant-brain-mcp/` 后需重启 MCP 服务才生效（`.mcp.json` 指向 `main.py`，使用 `world-quant-brain-mcp/.venv`，勿用根环境）。
- 修改 `tracking/<REGION>/config/`（如 `thresholds.json`）影响该区域战役闸门；勿手动编辑 `tracking/mining/` 共享数据湖。
- 修改 `tools/` 中被引用函数前，先用 `rg` 搜索调用点确认影响面。
- **挖掘经验库必读（2026-09-29 建立；索引 = [`docs/experience/README.md`](docs/experience/README.md)）**：平台交互类改动（回测/提交/配额）动手前先按主题读对应篇，遵守并发与配额约束、避免 429，也避免重踩已证伪路径。
  | 你要做的事 | 必读 |
  |---|---|
  | 提交 / 判定闸门 / 配额 / 相关性取数 | [`01_platform_gates.md`](docs/experience/01_platform_gates.md) |
  | 设计或改造信号结构 | [`02_signal_patterns.md`](docs/experience/02_signal_patterns.md)（含组合形态铁律） |
  | 选区 / 选数据集 | [`03_region_dataset.md`](docs/experience/03_region_dataset.md)（含停投结论） |
  | 改工程链路 / skill / DB | [`04_engineering.md`](docs/experience/04_engineering.md) |
  | 复盘 / 准备放弃某方向 | [`05_antipatterns.md`](docs/experience/05_antipatterns.md) |
  ⚠ **双轨同源**：上述 md 给人/Agent 看；**机器消费层是另一套**——`Claude/skills/wq-brain-campaign-toolkit/config/methodology_rules.json`（全局。**实际消费点**：`build_wave.py` 的 `apply_rules("dead_end")` 拦截 + 打印 strategy 提示；`pipeline.py` 的 L1 采集 / L4 证伪 + strategy 提示；`review_wave.py` → `recommend_next_wave` → 通用 `inject_rules`（声明了 `when` / `emit` 的规则条件化命中，其余 active 规则作常驻提示兜底）；`gate.py` **只**消费 `explore_contract` 契约规则，不消费 strategy / diagnosis 规则。旧文写「四处 `RuleStore.query()` 强制注入」不符合实际，2026-10-04 更正）与 `tracking/<REGION>/reference/`（区域，存 DB）。**改一边必须同步另一边**，否则出现"文档写了但流程不认"。守护测试见 `tests/unit/test_experience_kb_refs.py`。
- 凭据位于 `world-quant-brain-mcp/.env`：禁止读取、打印或提交到 git。

## 3.5 Skills 回测标准路径（2026-09-05 单源化）

> **本节只放"入口与边界"。九步流水线的完整正文（每步目的/MCP 调用/产物/失败分支、
> 区域 profile 路由、Artifact 契约、循环停止表、反模式）**唯一权威在**
> [`Claude/skills/wq-brain-ra-pipeline/SKILL.md`](Claude/skills/wq-brain-ra-pipeline/SKILL.md)。
> 2026-09-05 前本节逐字复制了那份 SOP，两边已开始漂移（本节记了 gate_results /
> s4_walls / salvage_pool，SKILL.md 的 Artifact 契约表没有；本节写「brain-make-some-gem
> 强制调用」，SKILL.md 写「workflow_gem 强制调用」）。改流程只改 SKILL.md，不要再复制到这里。

**唯一挖掘编排 SOP**：`wq-brain-ra-pipeline`（九步流水线 S-PRE→S6），三角分工：

| skill | 职责 |
|---|---|
| `wq-brain-ra-pipeline` | when / what / 怎么挖 Regular Alpha（S-PRE→S6） |
| `wq-brain-campaign-matrix` | where = 查表选区选集 |
| `wq-brain-campaign-toolkit` | how = 战役目录内执行引擎 |

**九步骨架（只作索引，细节看 SKILL.md）**：

| 步 | 阶段 | 主入口 |
|---|---|---|
| 1 | S-PRE 查表 | `wq-brain-campaign-matrix` + `mcp__wqb-db__get_*` |
| 2 | S0 数据集体检 | `workflow_campaign(stage="S0")` |
| 3 | S1 字段扫描与理解 | `workflow_campaign(stage="S1")` + `workflow_feature_engineering` |
| 4 | S2 概念优先生成 | `workflow_gem`（强制；引擎 = `brain-make-some-gem` headless_runner） |
| 5 | S2→S3 门禁 | `workflow_execute(node="wave_gate")`（2026-09-11 起有节点）或 CLI `tools/wave_gate.py`（已内置体检硬门 `tools/field_inspect_gate.py`；多样性走 toolkit `gate.py` 闸6） |
| 6 | S3 并发回测 | `workflow_batch_track`（并发参数见 `wqb.config.CONCURRENCY` 与 `wqb-concurrency` §8） |
| 7 | S4 诊断改进 | `workflow_campaign(stage="S4")` + `wq-brain-alpha-optimization-v1` |
| 8 | S4→S5 稳健闸与提交判定 | `brain-alpha-robustness` → `submit_verdict`（**否决权威**：只能拦不能放）→ `check_correlation(refresh=True)` prod 实测 → **用户确认** → `workflow_submit_alpha(confirm_submit=True)`（不可逆） |
| 9 | S6 复盘回写 | `mcp__wqb-db__upsert_wave_result` / `seal_dead_end` / `upsert_registry_empirical`，再跑一次 `assemble-priors`（完成定义见 ra-pipeline `references/step9-writeback.md`） |

整链可用 `mcp__wq-brain-http__workflow_chain`（先 `dry_run=True` 看每步构建出的命令）。
**但提交类节点不入自动链**：`workflow_submit_alpha` / `workflow_superalpha` 的
`confirm_submit=True` 必须由用户在步 8 明确确认后单独调用。这条由代码强制（`wqb.workflow.executor.execute_chain`：
链里出现即整链拒绝、一步都不执行，干跑也拒；`tests/unit/test_workflow_chain_irreversible_guard.py`）。

**几条不在 SKILL.md、属仓库工程约定的补充**：

- **判定与提交的权威划分**：`tools/submit_verdict.py`（MCP `submit_verdict`；实现 `wqb.submit_verdict_core`）是提交判定的**否决权威**——它说 `BLOCKED` 就不提交，
  但它**放行不了**任何东西：放行权威 = 用户明确确认 + `confirm_submit=True` 的 POST（词表见 `Claude/skills/GLOSSARY.md`，链路见 `worldquant-submit-alpha/references/submit-chain.md`）。
  `brain-alpha-judge` / `workflow_judge` 是**参考评审层**，2026-09-05 起代码里已无提交路径。
- **workflow 节点元数据**：`registry.py` 的 `required_params` / `optional_params` 必须与节点
  `run()` 签名一致（`_context` / `dry_run` 除外）。`workflow_list_nodes` 把它当 API 文档
  暴露给 Agent，漂移即误导。回归由 `tests/unit/test_skill_integrity.py` 守护。
- **新增/修改 workflow 节点 → 五处必须同步（2026-09-18 固化四处，2026-09-29 补第五处）**：注册信息散在五处，
  漏一处测试即红：① `src/wqb/workflow/registry.py`（register + NodeMeta，与 run() 签名逐字一致）
  ② `tests/unit/test_workflow.py::test_registry_lists_all_core_nodes` 期望集合
  ③ `tests/unit/test_skill_integrity.py::_DRY_RUN_CASES` 干跑用例表
  ④ `Claude/skills/INDEX.md` workflow 节点计数
  ⑤ `world-quant-brain-mcp/tests/test_tools_workflow_unit.py` 的 `expected_nodes` 集合。
  ⚠ ⑤ 是 2026-09-29 全量测试转红才暴露的：`forum_recon_wave` 上线时四处全绿、MCP 包测试 20≠19。
  根因是 MCP 包测试与根 `tests/` 是两套路径，只按单文件跑测试会漏掉它。**改节点先跑 `tools/audit_node_registration.py`**（已升级为五处审计）。
  **一次跑完全部检查**：`python tools/audit_node_registration.py`（`--node X` 单节点自检；
  退出码 1 = 有漂移并列出全部缺口）。战例：`alpha_booster` 只做了 ①，②③ 漏同步 +
  NodeMeta 漏 `forum_refresh` → 3 个测试红；`gem` 的 meta 漏 `batch_size` 同被逮到。
- **dry-run 契约**：全部 workflow 节点（含后加的；清单以 `workflow_list_nodes` 与 INDEX 计数基准为准）统一「走完零成本前置 → 构建出命令/请求计划 → 到此为止」，
  不 subprocess、不写库、不建目录。干跑失败必须带得出 `error`（禁止 success=False + error=None）。
- **argv 契约校验（2026-09-06）**：凡是拼子进程命令的节点，构建完必须过
  `_common.validate_argv(cmd)` —— 它静态解析目标脚本（含其本地 import 的辅助模块）的
  `add_argument` / `add_parser`，逮住"脚本压根没声明过的 --flag / 子命令"。
  起因：`batch_track` 给 `pipeline.py run` 拼了个不存在的 `--concurrency 7`，
  argparse exit=2，而 detached 分支不看退出码 → S3 每次都"启动成功"却从未真跑过，
  证据在 `stderr.log` 里躺了 13 天。目标脚本自身零 `add_argument`（纯派发器）时放行。
- **detached 存活握手（2026-09-06）**：后台启动后必须过 `_common.detached_launch_failed()`
  —— 秒退或 stderr 非空即判失败并回传原因。detached 的代价就是没人看退出码，
  「启动即死」不能再被吞成 `success=True`。
- **异步任务查询**：后台任务一律用 `mcp__wq-brain-http__workflow_task_status`
  （`wqb.workflow.tasks`），它同时认两套布局（campaign/fe 的 `<id>.json` 与
  gem/batch_track 的 `<id>/meta.json`）。不要 shell 出去翻 `logs/_async_tasks/`。
  `workflow_chain` 默认 `join_async=True`，异步节点会等到终态再进下一步 ——
  否则下游必然读到上游还没落库的空结果。
- **skill 目录解析**：`_common._skill_roots()` 顺序为 `WQ_SKILLS_DIR` > Claude 安装位
  （`%APPDATA%\Claude\skills` 等）> `~/.claude/skills` > `~/.codex/skills` >
  **Cline 位**（`~/.cline/skills` / `~/.agents/skills`）> 历史 Agent 位
  （qoder-cn / cursor / workbuddy）> 仓库自带 `Claude/skills/`（兜底，保证 clone 即可用）。
  落到历史 Agent 位会打 WARNING：那些是独立物理拷贝。
  **四份必须同序**（改一处必改其余三处，守护测试 `test_docs_consistency.py` 比对镜像顺序）：
  ① `src/wqb/workflow/_common.py::_skill_roots()`（单源）
  ② `Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/skill_roots.py`（`HOST_DIRS`）
  ③ `Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skill_roots.py`（`HOST_DIRS`）
  ④ `tools/skill_paths.py` / `tools/sync_skills.py` 各自的 import 失败兜底。
- **Cline Desktop/CLI 的 skill 入口（2026-10-03 实测登记，别靠猜）**：路径**读自** Cline 自身
  `dist/lib.mjs` 的 `oo` 常量表 + `yYt()`，共 6 个候选（`source` 标注 project / global）：
  | source | 路径 |
  |---|---|
  | project | `.clinerules/skills` → `.cline/skills` → `.claude/skills` → `.agents/skills` |
  | global | `~/.cline/skills`（`Qdp()`）、`~/.agents/skills`（`otu()`） |
  ⚠ **`~/.cline/skills` 不等于 `~/.cline/data/settings/`**：后者放 MCP 配置
  （`cline_mcp_settings.json`），Cline 会自动扫前述 6 个目录，无需在 settings 里登记 skill。
  本工作区 `Claude/skills/` 是源、`~/.cline/skills` 与 `~/.agents/skills` 是派生物；
  **项目级 `.claude/skills` 由 Cline 自行扫描，wqb 侧不为其复制副本**（避免三处重复进 skill 列表）。
- **⚠ 各客户端的 HTTP `type` 取值不通用，照抄会静默失败（2026-10-05 实测）**：
  `.mcp.json` 用 `"type": "http"`，Claude 系与 Qoder 认这个值，Cline 不认。各客户端要各写各的：
  | 客户端 | 配置文件 | HTTP 形态的 `type` |
  |---|---|---|
  | Claude Code / Desktop | `.mcp.json`（权威源）/ `mcp_config.json`（镜像） | `http` |
  | **Qoder CN** | 项目 `.mcp.json` + 用户级 `~/.qoder-cn/mcp.json` | `http`（实测：`wqb-db` 只写在项目 `.mcp.json`，Qoder 按 `type:http` 连上了 8001） |
  | **Cline Desktop/CLI** | `~/.cline/data/settings/cline_mcp_settings.json` | **`streamableHttp`**（驼峰） |
  | **WorkBuddy** | `~/.workbuddy/mcp.json` | `http`（实测：两个 server 已指 8000 / 8001 并连通） |
  | 其他 MCP 客户端 | 按各自 schema | 先查 schema 再写 |
  ⚠ **Qoder：同名 server 以用户级 `~/.qoder-cn/mcp.json` 覆盖项目 `.mcp.json`**。2026-10-05 实测该文件里
  `wq-brain-http` 仍写 stdio（`command` + `env.MCP_TRANSPORT=stdio`），于是 Qoder 自己另拉一份 `main.py`
  子进程 —— 跟 8000 上的常驻 HTTP 服务**并存两个实例、各持一份平台会话**，项目 `.mcp.json` 的 http
  配置对它完全不生效（`wqb-db` 没写进用户级文件，所以那一路是走的 HTTP）。
  判据：`Get-CimInstance Win32_Process -Filter "Name='python.exe'"` 看 `main.py` 的父进程是不是
  `QoderCN.exe`，再看 8000 端口有没有来自 Qoder 的连接。用户级文件已改 `type:http` + `url`
  （原 stdio 版备份 `~/.qoder-cn/mcp.json.bak_stdio_20261005`）；**改完要重载窗口 / 重启 MCP 连接才生效**。
  ⚠ **Cline 核心代码里完全没有 `.mcp.json` 字样**（实测 `index.js` 搜 `.mcp.json` 无命中），
  它只读自己的 settings 文件 ⇒ **改 `.mcp.json` 不会影响 Cline，必须单独改**。
  合法值只有 `stdio` / `sse` / `streamableHttp`（来源：`@cline/core/dist/extensions/mcp/types.d.ts`
  的 `McpServerTransportConfig` + `index.js` 里的 zod `enum(["stdio","sse","streamableHttp"])`）。
  写错时 Cline 抛 `Invalid MCP server "<name>": type: Invalid enum value...`。
  ⚠ **HTTP 模式下 `env` 块整体删除**：客户端不再起进程，没人注入 env。
  服务端已自带兜底 —— `main.py:14-23` 按仓库根 `setdefault` 了 `WQ_TOOLKIT_DIR` /
  `WQ_VALIDATOR_DIR` / `WQB_ALLOW_ALPHA_SUBMIT`（后者是提交闸，缺了会 fail-closed 拦下提交）；
  `wqb_db_mcp.py:40` 的 `DB_PATH` 由 `__file__` 推导仓库根，不依赖 `WQB_DB_PATH`。
  ⚠ **`WQB_ASI_UNIVERSE_FIX` 已无任何代码读取**（`git grep` 仅命中一份历史报告的注释），
  是 stdio 时代遗留，可安全丢弃。**HTTP 模式无认证，只绑回环**（`tools/start_wq_mcp.py` 的 `MCP_HOST`
  缺省 `127.0.0.1`），别改成 `0.0.0.0`——`wq-brain-http` 持平台凭据。
  验证手段：`python tools/mcp_ping.py`（只读探针，走 HTTP 客户端，不起进程）。
- **skill 多目标单向同步（2026-09-10 起；2026-10-03 加 cline/agents 后 6 个安装位）**：仓库 `Claude/skills/` 是源，**全部安装位**是派生物。
  改 skill 只改仓库副本，然后 `python tools/sync_skills.py`（自动枚举全部已存在的安装位：
  claude / codex / **cline / agents** / qoder-cn / cursor / workbuddy，逐个同步 + 逐个校验）；`--check` 模式由
  `tests/unit/test_audit_fixes.py::test_sync_skills_reports_no_drift` 守护（多目标断言）。
  历史教训：① 安装位曾落后仓库两周（make-some-gem 停在 08-22、仓库已 09-05）；
  ② 2026-09-10 审计发现旧版脚本只同步**首个**目标（`resolve_install_root()`），致使
  `~/.codex`、`~/.workbuddy` 反复分叉（ra-pipeline 落后 67 行，缺 09-09 的
  `campaign_intel s0-select` 选集与 `ghost-audit` 幽灵算子硬闸）—— 故改为多目标。
  失效安装器（`install_now.py` / `install_claude_skills.*` / `verify_claude_skills.py` /
  `install_skills_direct.py` / `INSTALLATION_GUIDE.md`）已归档 `attic/install_legacy_20260910/`，
  勿再用它们做更新（`if target.exists(): skip` 永不更新）。
  ⚠ **凭据文件不扩散**：`sync_skills.py::_is_secret_file` 刻意不复制 `.env` / `*.env` / `config.json`，
  故安装位文件数（320）少于仓库（398）是**预期**，不是同步失败（skills 审查 X-15）。
- **MCP 服务器命名**：只能是 `wq-brain-http` 与 `wqb-db` —— 所有 skill 调用的工具前缀是
  `mcp__wq-brain-http__*` / `mcp__wqb-db__*`，改名即全线失配。`.mcp.json` 为准，
  `mcp_config.json` 与安装脚本必须跟随。

### Skill layer 取值表

`SKILL.md` frontmatter 的 `layer` 只表示"在挖掘链条上的位置"，不是优先级：

| layer | 含义 | 例 |
|---|---|---|
| `L-RA` | 唯一编排入口 | `wq-brain-ra-pipeline` |
| `L-RA-R` | RA 的区域分支（区域控制面板 + 区域 × 类别组合文件；**生成物**，改 `tracking/<R>/config/cells.json` 后 `$WQ_PY -m wqb.profiles render --apply`，不手改生成块） | `wq-brain-ra-kor` 等 14 个 `wq-brain-ra-<区域小写>` |
| `L-PRE` | 开战役前的查表选集 | `wq-brain-campaign-matrix` |
| `L-TOOL` | 战役执行引擎（被编排调用） | `wq-brain-campaign-toolkit` |
| `L0` | 战役外的态势/情报 | `brain-next-move-analysis`、`brain-forum-browse`、`wq-brain-ppa-mining` |
| `L1` | 数据集 / 字段研究（S0–S1） | `brain-alpha-research*`、`brain-*-exploration-*` |
| `L2` | 表达式生成与语法校验（S2） | `brain-make-some-gem`、`brain-feature-implementation`、`alpha-expression-verifier` |
| `L3` | 批量回测与并发纪律（S3） | `brain-sim-alphas-in-batch-and-track`、`wqb-concurrency` |
| `L4` | 诊断与改进（S4） | `wq-brain-alpha-optimization-v1`、`brain-alpha-robustness`、`brain-how-to-pass-alpha-test` |
| `L5` | 提交（S5） | `worldquant-submit-alpha`、`wq-brain-superalpha`、`brain-alpha-judge` |
| `L6` | 监控与复盘（S6） | `wq-backtest-monitor` |
| `L7` | 与挖掘无关的通用工具 | `planning-with-files`、`pull-brain-skills` |

### SKILL.md frontmatter 契约（2026-09-10 审计固化；**完整契约在 [`Claude/skills/CONTRACT.md`](Claude/skills/CONTRACT.md)**，本节是摘要，冲突以它为准）

**必需字段**：`name`（== 目录名）、`layer`、`description`、`last_verified`。
**可选字段**：`version`、`user-invocable`、`allowed-tools`、`agent_created`、`hooks`。

- `layer` = 挖掘链条位置（见上表），**不是**版本号；内容版本一律用独立 `version` 字段
  （如 `wq-brain-ra-pipeline: version "2.2"` + `layer: L-RA`）。
- `last_verified` = 最近一次对照平台核实内容正确的日期（`YYYY-MM-DD`）；改正文后应更新。
  2026-09-10 审计已补齐全部 32 个 skill 的该字段（此前 8 个缺失）。
- 守护：`tests/unit/test_skill_integrity.py` 校验 `name` 与目录名一致、frontmatter 完整。

### Skill 命名规范（2026-09-10 审计固化）

- 目录名与 frontmatter `name` **一律纯 kebab-case**（小写字母 + 连字符），禁止驼峰与下划线。
  2026-09-10 已把 7 个历史命名统一：
  `brain-makeSomeGem→brain-make-some-gem`、`brain-simAlphasinBatch-and-track→brain-sim-alphas-in-batch-and-track`、
  `brain-calculate-alpha-selfcorrQuick→brain-calculate-alpha-selfcorr-quick`、
  `brain-how-to-pass-AlphaTest→brain-how-to-pass-alpha-test`、
  `brain-inspectRawTemplate-create-Setting→brain-inspect-raw-template-create-setting`、
  `brain-nextMove-analysis→brain-next-move-analysis`、`pull_BRAINSkill→pull-brain-skills`。
- 前缀语义：`brain-*` = 业务/知识技能；`wq-brain-*` = 流程编排；`wqb-*` = 横切工具（并发等）。
  **新建 skill 必须遵守。**

### 按需调用的知识型 skill（不进自动化 call chain）

以下 skill 不参与 pipeline 自动编排，由 agent 按触发条件按需调用；此处登记触发场景，
避免"存在但无人知何时用"：

| skill | layer | 触发场景 |
|---|---|---|
| `alpha-template-labs-data-analysis` | L0 | 设计 Python alpha **前**做 BRAIN Labs 原始数据分析（USA/TOP3000/D1 MATRIX 覆盖/缺失/频率/离群/相关性） |
| `brain-alpha-repair` | L4 | 弱候选修复的**配方索引**（降 turnover、提覆盖、降相关的修法与实证、修复成功判据）。**配方在本 skill 内**（optimization-v1 里并没有——2026-09-29 审查 RE-01 / P0-6 更正了此前「已上移」的错误说法）；动手改候选走 `wq-brain-alpha-optimization-v1` |
| `brain-datafield-exploration-general` | L1 | 评估单个新 datafield（覆盖率 / 非零值 / 更新频率 / 分布形态） |
| `brain-explain-alphas` | L4 | 解释某个 alpha 表达式 / 字段 / 算子协作 |

## 3.x 单源核心与 brain_api 拆解约定（Direction A）

- **`src/wqb` 为唯一规范核心**（single source of truth）：区域/算子/中性化等域常量只在此定义；MCP 包与 `pipeline/`/toolkit scripts 共享引用，新增域知识只写 `src/wqb`，勿在 `world-quant-brain-mcp/` 重复硬编码。
- **`brain_api` 为稳定 API 客户端，方法逻辑不重写**：`BrainApiClient` 仅继承 5 个 mixin（`TransportMixin`/`AuthMixin`/`SimulationMixin`/`SpcDataMixin`/`CorrelationMixin`），方法体 verbatim 迁移；扩展新端点时**新增 mixin 方法**，勿改动既有方法实现。
- **原码备份（勿依赖 git 之外的临时副本）**：原始 4074 行整文件 `attic/brain_api_backup/original/brain_api.py`；拆解后 7 文件 `attic/brain_api_backup/current_refactored/`（brain_api.py + brain_config.py + brain_api_models.py + 5×brain_mixin_*.py）。
- labs 特性 `labs_data_analysis_agent.py` 由 `labs_functions.emit_labs_script` 经 `read_text()` 整文件读入后粘贴进 BRAIN Labs，**不可拆分**。

## 4. 测试与验证路径

编辑后必须运行验证：

```bash
python -m pytest tests/ -x
```

### 失败诊断纪律（2026-09-18 固化）

面对一批测试失败时，按这个顺序处理——**这套顺序是实测出来的，跳过任一步都会走偏**：

1. **先取完整 traceback**（`--tb=long` / `--tb=short`），不要只看 `-q` 的汇总行。
2. **按根因聚类**，不逐条修。7 个失败往往只是 3–4 个根因。
3. **对行为可疑的失败做端到端最小复现**。★ 最关键的一步：
   2026-09-18 若按"测试期望过时"改掉 `test_auto_coverage_never_injects_no_contract_expressions`，
   就会把 `build_wave.py` 族类配额**静默截断开波**这个真实生产 bug 永久埋掉
   （实测 `--from-db` 下 `--size 3/6/12` 全部只选出 2 条）。复现命令比断言更有说服力。
4. **区分「测试期望过时」与「代码回归」**：前者改测试，后者改代码。判据是复现结果——
   若复现出**与断言不同的真实行为**，先假设代码有问题。
5. **环境/数据类失败先查状态文件**。带 checkpoint/续跑的脚本常见"状态文件陈旧掩盖真实漂移"
   （战例：`normalize_ledger_whitelist.py` 报「已完成，跳过」，加 `--fresh` 才真正重写）。
6. **修复后给回归中的"新失败"定性**：全量回归时冒出的新失败，先确认是不是自己引入的
   （`git stash` 对照 / 检查是否 env 相关），再决定修还是记。
7. **沉淀固化**：同一类漂移出现第二次，就写工具或写测试把它机械拦住，不要靠人记。

- 结果自动写入 `logs/test-results.xml`（JUnit XML，可追溯）。
- 根 `tests/` 全量应全绿（历史数字：2026-09-18 实测 1201 个，2026-09-30 为 2709 个；**今天的数量一律以 `pytest --collect-only -q | tail -1` 为准，此处不再维护**；`src/wqb` 包于 2026-08-16 按 `docs/plans/2026-08-02-wqb-src-reconstruction.md` 重建；仓库根 `conftest.py` **只负责环境耦合测试的 skip 标记**（`needs_operators_verified` 等：依赖被 gitignore 的本机产物，缺失时跳过并写明原因，不是失败）；`sys.path` 由 `tests/conftest.py` 同时把 `src/` 与 `world-quant-brain-mcp/` 注入，`tests/unit/` 继承之）。MCP 包 `world-quant-brain-mcp/tests/` 另有一批测试（需 `.venv`；其 `conftest.py` 只注入 MCP 目录，验证 `brain_api` 拆解不变量与工具注册）。pre-commit 钩子仅跑根 `tests/`，MCP 包测试需单独在 `.venv` 跑。
- **计数口径：根 `tests/` 递归包含 `tests/unit/`，勿把两者相加。** `tests/` 直接子层只有 `test_toolified_cli.py` + `conftest.py`，其余在 `tests/unit/`。故 `pytest tests/` 与 `pytest tests/unit tests` 收集数相同。**新增用例时以 `pytest --collect-only -q | tail -1` 为准，不在此处硬编码逐文件明细**（此处的总数随用例增删会漂，只作量级参考）。
- 依赖声明于根 `requirements.txt` 与 `world-quant-brain-mcp/requirements.txt`，新增依赖需同步相应文件。

### pre-commit 钩子（推荐激活）

提交前自动运行上述 pytest 验证路由，测试失败即阻止提交：

```bash
git config core.hooksPath tools/git-hooks
```

- 钩子脚本：`tools/git-hooks/pre-commit`（调用 `python -m pytest tests/ -x`）。
- 紧急跳过（仅临时）：`git commit --no-verify`。

## 5. Shell 命令规约（根治引号转义事故）

环境为 Windows PowerShell（无 `&&`，用 `;`）。引号经“工具传参→PowerShell→解释器”三层嵌套必出事故，按优先级分层规避：

0. **结构化数据读写首选 wqb-db MCP 工具**（根治层）：MCP 调用传 JSON 参数，不经过 shell，引号问题不存在。读：`get_wave_result`/`get_ledger_key`/`list_expressions`/`get_field_catalog`/`list_*`；写：`upsert_wave_result`/`upsert_ledger_key`/`upsert_registry_empirical`/`upsert_expressions`/`upsert_field_catalog`/`upsert_gate_result`/`upsert_backtest_rows`（幂等）。仅当需要执行逻辑（如批量入库带自动派生）才走 `campaign.py` CLI。**战役产物（expressions/gate/ranking/checkpoint/review/batches）只入库，禁止 Agent `Write`/`Copy-Item` 落 `tracking/*/candidates|cache|results|reviews/*.json|*.csv`。** CLI 临时 `@file.json`（AGENTS.md 引号规避）用完可删，不算战役持久化。
1. **执行逻辑禁止 `python -c "..."` 内联带引号嵌套/中文/JSON 的代码**：一律先写临时脚本 `logs/_tmp_*.py`（UTF-8），执行 `python logs/_tmp_xxx.py`，用完可删。历史惯例 `logs/_*.py` 下划线前缀即临时脚本。
2. **CLI 传中文/JSON/多行参数走 `@file` 文件通道**：先写临时 JSON 再以 `--extra @path.json` / `--candidates @path.json` 形式传入（`campaign.py` 系列已支持）；不要用引号包裹中文直接传参。
3. **路径/含 `$` 的字符串用单引号**：PowerShell 双引号会展开 `$变量` 与反引号转义，路径参数一律 `'...'`。
4. **中文输出乱码是显示层问题**：跑 Python 时加 `-X utf8`（或命令前 `$env:PYTHONUTF8=1`）；乱码不代表逻辑错误，但按规约 0/1 走 MCP 或文件脚本可彻底规避。
5. **长命令拆短**：单条命令超 3 层引号即改写为临时脚本，不要硬凑转义。

## 6. 一次性脚本工具化纪律（2026-08-23 落地，tools/README.md 为索引）

高频同构操作**禁止新建一次性脚本**，必须先查 `tools/README.md` 用对应工具；
缺参数/缺能力就**改工具加参数**（保持 `--help` 自文档），再反复出现即说明工具化不彻底：

| 场景 | 工具（替代的一次性脚本） |
|---|---|
| 每波门禁（gate.py 8 闸 + 体检硬门，一键落盘） | `tools/wave_gate.py --campaign-dir … --dataset … --wave N --candidates <json>`（替代 `tracking/<R>/scripts/_gate_waveNN.py`） |
| 批次/子任务状态查询+轮询 | `tools/batch_status.py --ids … [--watch]`（替代 `tracking/_scratch/check_*batch*.py`） |
| SA 组件池探针（≥10 ACTIVE 硬前置） | `tools/sa_probe.py --region …`（替代 `probe_*sa*.py`） |
| 提交层判定（403 盲区） | `tools/submit_verdict.py --alpha-id …`（替代手写 GET /alphas/{id}/submit） |
| SUPER 组套/提交全流程 | `tools/super_build.py {select|status|probe|submit} …`（替代 `track_mea_super*.py`） |
| 批量派发仿真（dispatch；**不是**把 alpha 提交上平台） | `tools/submit_batch.py`（替代 `_submit_*.py`） |

执行约定：
1. 网络工具一律用 MCP venv（`$WQ_PY` 或 `world-quant-brain-mcp/.venv`）运行，工具已内置自动切换；
   不手写 requests 脚本（429 事故根因之一），统一走 `BrainApiClient`（自带 429 退避）。
2. skill 依赖路径用 `WQ_VALIDATOR_DIR` / `WQ_TOOLKIT_DIR` 或 `skill_roots()`（自动搜索顺序：`~/.claude` → `~/.codex` → 历史位 `.trae-cn`/`.qoder-cn`/`.cursor`/`.workbuddy` → 仓库 `Claude/skills` 兜底），禁止硬编码 `C:\Users\...` 绝对路径。
3. 一次性排障探针（`_inspect_*`/`probe_payment*` 等探索类）仍可写 `tracking/_scratch/`，但结论落地后归档 `attic/`，不留在活跃目录累积。
4. **已跑完的一次性脚本移入 `tools/legacy/`（2026-09-20 落地）**：判据为"类型一次性
   （`backfill_*`/`migrate_*`/`triage_*`/`submit_<alpha_id>*`）+ 全库 refs=0"，用
   `git mv` 移动（保留历史，**不是删除**），索引见 `tools/legacy/README.md`。
   `tracking/_scratch/` 同理，属临时区，用完清空（2026-09-20 已清空 31 个文件）。

## 7. 提交纪律（2026-09-11 固化）

工作区长期存在**多条并行工作流**（战役脚本 / skills 治理 / MCP 改动 / tracking 数据湖），
一次 `git status` 常见 40+ 修改、20+ 未跟踪。踩过的坑：把 A 工作流的半成品混进 B 的提交。

**提交前流程（强制）**：

1. `git status --porcelain` 全量分类，按**主题**切分，**禁止 `git add -A`** / `git add .`。
2. 用**显式路径清单**暂存；跨工作流时优先 `git add -p` 逐块挑选。
3. 只提交"自洽且可验证"的改动：跑 `pytest tests/ -x`；改 skills 后加跑
   `python tools/sync_skills.py --check`（多目标零漂移）。
4. 提交信息写清**范围与验证证据**（例：`chore(skills): … ；验证 pytest 531 passed + sync 4/4 OK`）。
5. 提交前扫硬编码密钥/凭据（`sk-*`、`api_key=`、`password=`、私钥块）；`.env` / `config.json`
   一律不在版本控制内（`.gitignore` 已覆盖，勿 `-f` 强提）。

**并行写入者的注意**：本机可能同时有其他 Agent/会话在改同一棵树（实测发生过
`assemble_priors.py` 被并发改写、`sync_skills.py` 报"已同步 0 个文件"而文件实际已在位）。
因此：① 被漂移断言拦下时**先重跑 `sync_skills.py` 再提交**，不要改测试去迁就；
② 追加共享文件（记忆日志、台账）必须**先读尾部再追加**，禁止整文件覆写。

**归档而非删除**：一次性脚本、旧版本、废弃 skill 一律移入 `attic/<主题>_<YYYYMMDD>/`，
保留可回溯性；安装位孤儿用 `python tools/sync_skills.py --prune-orphans [--apply]`。

## 8. 结构维护约定（2026-09-20 结构审计固化）

### 8.1 gate 门禁分层（**2026-09-20 修正：是分层流水线，不是四份重复实现**）

> **更正**：本节初版误记为"gate 逻辑四重实现、语义重叠"。实测调用链后确认是
> **单一权威 + 包装分层**，并发现 `tools/gate.py` 是代码零引用的遗留文件（已归档）。
> 教训：判定"重复实现"前**必须先读调用链**（`find_script` / `_TOOLKIT_CANDIDATES` 的解析目标），
> 不能只看文件名相同就下结论。

```
unified_gate.py（节点：幽灵算子硬闸 + 转发 wave_gate）
nodes/wave_gate.py（节点：dry-run 契约 + subprocess 包装）
        └─→ tools/wave_gate.py（每波门禁编排器 CLI —— 唯一入口）
                ├─→ toolkit gate.py           （8 闸，经 _TOOLKIT_CANDIDATES，权威实现）
                ├─→ validator.py              （语法，WQ_VALIDATOR_DIR）
                ├─→ wqb.expression.op_arity   （算子元数/命名参数，src/）
                ├─→ _lib/region_gates.py      （区域三道闸：signal_floor/stop_rules/backlog）
                ├─→ field_inspect_gate.py     （体检硬门）
                └─→ pool_diversity.py         （六维多样性）
tools/legacy/gate.py（遗留通用闸门，代码零引用，2026-09-20 归档）
```

| 文件 | 角色 | 关键事实（实测） |
|---|---|---|
| `tools/wave_gate.py` | 每波门禁**编排器 CLI**（唯一入口） | §6 指定工具；`gate_py = find_script(_TOOLKIT_CANDIDATES, "gate.py")`（第 567 行） |
| `Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py` | **8 闸权威实现**（58KB） | 被 wave_gate 子进程调用；测试注入该目录后 `import gate` |
| `src/wqb/workflow/nodes/wave_gate.py` | workflow 节点（包装） | subprocess 调 `tools/wave_gate.py`，带 dry-run 契约 |
| `src/wqb/workflow/nodes/unified_gate.py` | workflow 节点（超集） | = `campaign_intel ghost-audit` + 转发 `tools/wave_gate.py`（第 134 行） |
| `tools/legacy/gate.py` | **遗留**（16KB，2026-09-20 归档） | 代码零引用；曾 `from src.wqb.config import OP_FAMILIES` |

**纪律**：不要新增 gate 实现。要加闸门 → 改 toolkit `gate.py`（8 闸权威）；
要新入口 → 包一层 workflow 节点转发 `tools/wave_gate.py`。

#### 8.1.1 开波区域闸的模式（2026-09-27 定案）

- **两条执行路径**：workflow 节点（`campaign` S2/S3、`batch_track`）一律拦截，只有测试 / 沙箱隔离用的
  `WQB_DISABLE_{SIGNAL_FLOOR,STOP_RULES,BACKLOG}_GATE` 开关；toolkit CLI（`build_wave.py`、`tools/wave_gate.py`）
  按 gate-mode 走。
- **CLI 的 gate-mode**：`--gate-mode` > `WQB_GATE_MODE` > 按日期的缺省。**2026-10-11 及以前 warn，
  2026-10-12 起 enforce。** 唯一事实源是 toolkit `_lib/region_gates.WARN_SUNSET`；改期只改这一处，并同步两份
  SKILL.md、本节与 `tests/unit/test_region_gates_p0p1.py`。依据见报告 §14.9.7。
- **放行**：停波区域要继续开波，写 waiver（§8.1.2；旧键 `stop_rules_override` 仍被识别，新写入用
  `waiver_stop_rules_<region>_all`）。`--gate-mode warn` / `WQB_GATE_MODE=warn` 只作临时回退（灰度期结束后同样需要
  `region_gates` waiver）；非法取值被忽略，不会降级成 warn。
- **退出码**：enforce 拦截 exit 2，与"门禁环境缺失"同码，含义都是"本波没有门禁结论，不是表达式问题"。
- **单测**：结论不能随日历变。`tests/conftest.py` 统一固定 `WQB_GATE_MODE=warn`；要测 enforce 或按日期缺省的用例
  自己 setenv / delenv，或 monkeypatch `region_gates._today`。

#### 8.1.2 放行 / 豁免（waiver）协议（2026-09-29 固化；实现 `src/wqb/waiver.py`，CLI `tools/waiver.py`）

"可显式降级，但必须在台账记因"此前散在 17 处文档、没有键名 / 字段 / 有效期 / 批准人，放行是静默的。现统一：

- **键与字段**：ledger 键 `waiver_<gate>_<region>_<wave|all>`（`wave` 缺省 `all`），值
  `{gate, reason_code, reason, evidence, approved_by, created_at, expires_at}`。**`expires_at` 必填，没有永久 waiver**；
  含当天有效，过期自动失效（闸重新拦截，报错点名「已过期」）。
- **谁能批准 / 最长多久**（`GATE_POLICIES` 为准）：`stop_rules`、`backlog`、`region_gates` 只有 **user**（用户显式指令，
  `reason` 引用原话；30 / 30 / 7 天）；`inspect`、`semantic`（各 7 天）、`diversity`、`prod_family`（各 3 天）
  user 或 agent 均可。`reason_code` 枚举 `USER_INSTRUCTION / REPAIR_BATCH / PROBE_BATCH / NO_INPUT_AVAILABLE /
  PLATFORM_UNAVAILABLE / SUPERSEDED_BY_EVIDENCE`，后三类必须带 `evidence`。
- **写法**：写台账 `waiver_<gate>_<region>_<wave>`——agent 用 `python tools/waiver.py new --gate … --region … --reason-code … --reason … --approved-by … --days N`
  生成并校验，再原样调用它打印的 `mcp__wqb-db__upsert_ledger_key(...)`（**不要手写 JSON**——校验在代码里，手写会绕过）；
  脚本环境加 `--write` 直接写库。`python tools/waiver.py gates|list|check` 查闸清单 / 现存 waiver / 是否生效。
- **哪些逃生口要 waiver**：`--skip-diversity-gate`、`--skip-semantic-gate` / `--semantic-gate off` / `WQB_SEM_MODE=off`、
  `--inspect-mode off`、`--no-prod-family-gate`、灰度期结束后 `--gate-mode warn|off`。`tools/wave_gate.py` 在**首屏**打印每个被跳过的闸
  及其 waiver（或「无 waiver 记录」），并写进报告 `waivers`。`--waiver-mode` / `WQB_WAIVER_MODE`：`warn`（缺省：无 waiver 只告警）/
  `enforce`（无 waiver 即 exit 2）/ `off`（仅测试隔离）。区域闸（`stop_rules` / `backlog`）被 waiver 放行时 `[waiver]` 行会点名批准人与到期日。
- **旧键**：`stop_rules_override` / `backlog_gate_override`（`{reason, until}`）仍被识别，缺 `until` = 永久放行并**告警 NO_EXPIRY**；`until`
  无法解析则 fail closed。读取路径已收成 `wqb.waiver.load` 一处，新代码不得再手写这类 SQL。
- **红线（任何人批准都无效）**：提交 alpha 前的用户明确确认、凭据（`.env` 只在本地，禁止读取 / 打印 / 提交 / 外发）、平台条款与限额。
  `RED_LINES` 里的名字调用 `load` 一律 INVALID；新增红线改 `wqb.waiver.RED_LINES`。
- **新增可豁免的闸**：先在 `GATE_POLICIES` 登记（批准人、最长天数、逃生口），再写文案；`tests/unit/test_waiver.py` 守登记一致。

### 8.2 双 MCP 系统分工（**不要合并，职责不同**）

- `world-quant-brain-mcp/`（完整包，`main.py` 入口）= **WQ 平台 API 前端**：仿真 / 相关性 / 提交 /
  论坛 / labs / SP C 读取，server 名 `wq-brain-http`。
- 根 `wqb_db_mcp.py`（2224 行）= **本地 DB 后端**：`data/wqb.db` 台账 / expressions /
  wave_results / registry 读写，server 名 `wqb-db`。
- 两者是**上游/下游关系**，不是重复实现；命名前缀 `mcp__wq-brain-http__*` /
  `mcp__wqb-db__*` 与工具前缀强绑定，改名即全线失配。
- **工具注册**：新函数不要插在某个 `@mcp.tool()` 与它原本装饰的函数之间（2026-09-19 就这样把
  `harvest_multisim_results` 挤出了工具表，N31）；下划线开头的函数不得是工具；SKILL.md 引用的工具必须已注册。
  三条都由 `tests/unit/test_skill_integrity.py` 守护，"已移除工具"白名单只收真正下线的工具。

### 8.3 配置文件权威源

- **MCP 配置**：根 `.mcp.json` 是**唯一权威源**；`mcp_config.json` 是镜像
  （供 Claude Desktop 等客户端读取），env 必须同步。`test_mcp_server_names_are_consistent`
  只校验两边 server 名集合一致（不校验 env），故镜像漂移不会被测试发现——**改 `.mcp.json`
  必须手动同步镜像**。
- **DB 备份**：`data/` 已整体 gitignore，只保留 live 库 + **最新 1 份**备份；
  旧备份用完走回收站（2026-09-20 已回收 326MB）。
- **运行时缓存不入库**：`tracking/hypotheses/`（hypothesis_round 账本）已
  `git rm --cached` + gitignore，磁盘保留。

### 8.4 结构性问题台账（**2026-10-03 更新**）

1. **`world-quant-brain-mcp/config/info_data.bin`（15M）** —— **非问题，无需处理**
   （2026-09-20 核验）。**更正**：初版审计误记"已入库"，实测 `git ls-files` 为空——
   它被**根 `.gitignore:16` 的 `*.bin`** 规则忽略，**从未进版本控制**，是本地运行时缓存
   （源自 WebDataScope 插件的 `data/oth/info_data.bin`，见
   `brain-alpha-research/references/webdatascope-data-quality.md`）。
   `brain_mixin_transport.py:105` 读取它、缺失时优雅降级（关闭 sharpe 过滤）。无需动作。
2. **`src/wqb/` 78 模块未打包** —— ⚠ **2026-09-30 决策已推翻并落地**（详见 8.12）。保留原判断的理由记录：
   当初选「脚本集合 + sys.path 注入」是在没有回归网的前提下做的，代价是 IDE 跳转差、新脚本要贴 `sys.path.insert` 样板。
   2026-09-30 在 **2709 个测试全绿** 的基础上改为正式包。**`tools/` 侧 142 处 `sys.path` 注入仍在**（脚本直跑需要），
   清理是独立任务。`src/wqb` 内的 sys.path 一律是**外挂** `world-quant-brain-mcp/` 与 `tools/` 这两个非 pip 包
   （设计内行为），**不要删**。新脚本直接 `from wqb.store import …`。
3. **文档三分** —— **已处理（2026-09-20）**：`AGENTS.md`（治理规约，权威）、
   `CLAUDE.md`（Claude Code 宿主常驻上下文：alpha 挖掘准则）、`README.md`（项目概述 + 上手）。
   已在 README 顶部「文档分工」与 CLAUDE.md 头部声明三者定位。
   *更正*：初版把 CLAUDE.md 写成"宿主入口、指向 AGENTS.md"——实际它承载挖掘准则、不指向 AGENTS.md。
4. **`tracking/_scratch/` 临时区** —— **已清空（2026-09-20）**，日后仍按 §6 第 3/4 条使用。
5. **代码级结构债与优化项** —— 见独立报告 `reports/code_structure_survey_20260925.md`
   （2026-09-25 全库梳理产出，含 `tools/` 文档覆盖率 38%、默认 zip 路径缺失、
   WebDataScope/info_data.bin 冗余、Skill 嵌套副本等，按优先级 P1–P11 排序）。
   **台账不再重复列举**，避免两处漂移。
   **2026-10-03 更正两项旧结论**（都是当时证据不足，须按此读台账）：
   - ~~僵尸测试：`tools/` 下 2 个 `test_*.py` 从不执行~~ —— **已解决（commit `c393bca`）**。
     二者文件头有 `__test__ = False` 显式自保护，且**非 pytest 用例是正确设计**：
     `test_field_catalog_cache.py` 被 docs 以 CLI 方式调用、非 dry-run 分支会**真打平台 API**；
     `test_gbr_batch_isolation.py` 被 `tools/gbr_pre_submit_check.py` 以子进程调用。
     **不要搬进 `tests/`**（会让 pytest 真去跑它们、打平台）。
   - ~~`data/`、`logs/` 无保留策略~~ —— **已解决（2026-10-03）**，见下一条第 6 项。
6. **`data/` 磁盘复发（第 5 次）** —— **工具已落地，但复发机制已加硬闸**。
   过程：2026-09-20 清到 390M/29M → 09-25 回涨 472M/46M → **10-03 再回涨 1210M + `cache/` 296M**
   （旧报告只盯 `data/`+`logs/`，**漏掉 `cache/`**，这是复发能持续的原因）。
   - **工具**：`tools/retention.py`（2026-10-03 新建，dry-run 默认，`--apply` 才删）。
     三条策略：`data/*.bak*` 只留最新 1 份（live `wqb.db` 与 `-wal`/`-shm` **硬保护，永不删**）；
     `cache/_probe/*.db` 超 7 天回收；`logs/` 过期文件 + pytest 临时目录。
     `_async_tasks`/`_slots`/`_dblock` **在保护名单里**（并发会话 MCP 进程在读写）。
   - **硬闸**：`tests/unit/01_store_db/test_retention.py::test_real_data_dir_backup_count_within_policy`
     断言 `data/` 备份数 ≤ 2。**再堆备份测试即红**，不再依赖"人记得跑清理"。
   - 首轮执行回收 **592 MB**（1210M → 617M）。
   - ⚠ 遗留观察（未处理）：`cache/_probe/probe.db` 单文件 **282.7 MB**，当时仅 4.07 天、
     未超 7 天阈值故未回收。它说明 `cache/` 与 `data/` 一样只增不减，只是阈值尚未到。
7. **`tools/audit_skill_drift.py` 只查"相同"、查不出"分叉"** —— **已解决（2026-10-03）**。
   原理性缺口：`collect()` 按内容哈希分组且只留 `len(v) > 1` → 一旦有人改一份没同步其余，
   各份哈希互异、各自成为长度 1 的组而被过滤 → **完全不可见**。而"改一处漏三处"恰恰就是这个形态
   （历史上 `validator.py` 三份各自演化、缺 hump/bucket/densify 修复即如此漏网）。
   - **补 `collect_diverged()`**：按**文件名**横切，同名 .py 出现在 ≥2 个不同 skill 且内容不同即报。
     首跑即抓到 4 组，其中 `diversity_enhancer.py` 是**真分叉且 sim 侧是旧版**——
     它仍用 3 层上溯找 `src/`，skill 装到 `~/.claude/skills` 时找不到 → ImportError →
     静默降级（多样性增强完全未生效却不报错，2026-09-09 在 toolkit 侧修过，sim 侧漏了）。**已同步修复**。
   - **S6 升 FAIL + 基线棘轮**：存量 B 类 4 组登记进 `tools/audit_structure_baseline.json`
     （键 `文件名@哈希12位`，格式同 `skill_lint` 的 baseline）→ 只 WARN 不阻塞；
     **基线外新增组 → FAIL 阻断提交**；**分叉副本无条件 FAIL、不进基线**（分叉没有"合法存量"形态）。
   - **设计内分叉白名单** `DIVERGED_ALLOWLIST`：`skill_roots.py`（两份 API 不同）、
     `ace_lib.py`（GEM 内嵌 vs 顶层）、`load_credentials.py`（vendor vs 本地适配）——
     每条都写明理由，白名单缺失会让 pre-commit 永久变红。
8. **`region_rotation._campaign_status` 静默吞 DB 异常 → 给出方向相反的转区建议** ——
   **已解决（2026-10-03）**。
   原实现 `except Exception: pass` 后返回全零，而返回值进 `detect_saturation.exhausted_pct`
   与 `rotation_score` 的 `f_headroom`/`f_untried`。失效方向经实测确认是**最坏的那个**：
   `exhausted_pct=None/0 → f_headroom=1.0`（**满分**）、`f_untried=_feat_log(0)=0`
   ——「DB 读不到战役状态」被当成「该区战役很少、空间最大」。而本模块卖点正是
   "零平台请求、零配额"，最该确定的地方反而最不可靠。前科：`.workbuddy/memory/2026-10-01.md`
   记载 310 行无 `status` 的脏 campaign 记录被长期静默忽略。
   - **修法不是塞假数据**（我最初想返回 `in_progress=1` 是错的——那仍是用假数据冒充），
     而是沿用该模块既有的 `data_caveat` 诚实性纪律：
     ① `_campaign_status` 采集失败返回 `None`（**区别于「查到 0 条」**）→
     `gather_region_metrics` 置 `campaigns_available=False` 且 `exhausted_pct=None`；
     ② `detect_saturation` 在不可采信时**禁用** `campaigns_exhausted`/`mined_out`
     两个强信号，并回 `data_caveat`（与 prod 薄样本同一套机制）；
     ③ `rotation_score` 的 `f_headroom`/`f_untried` 未知时取**中性 0.5**，
     与既有"薄样本取中性"纪律一致——旧写法 `or 0.0` 会把 `None` 变 0.0 得满分。
   - **守护**：`tests/unit/06_wave_pipeline/test_region_rotation.py` 新增 7 例
     （用缺 `registry_empirical` 表的真实 sqlite 触发 `OperationalError`，**不 mock**）。
     已验证非空过：`git stash` 掉源码改动后 **5 例立即变红**。
   - ⚠ 扫描发现同类静默吞异常 15+ 处（`except Exception: pass`），**本次只修决策路径上这一处**；
     其余多在采集层且有 `data_caveat` 或更弱的后果，待有具体故障证据再动，别批量改。
9. **⚠ 拆 `wqb_db_mcp.py` 入包：已尝试并当场回滚（2026-10-04，P2-2）** —— 结论：**先别拆**，
   除非同时下列三类耦合都处理完。**完整实测与可照做的执行顺位见
   [`reports/db_mcp_split_20261004.md`](../reports/db_mcp_split_20261004.md)**，
   回归凭据工具已入仓：`python tools/code-audit/mcp_surface_diff.py`。
   实测结论一行：拆分本身成功（入口 2792→91 行门面，**MCP 工具面 47=47 逐项一致**），
   失败全部来自耦合面。**两次尝试后测得共 6 类**（数字均为实测，不是估算）：
   ① **17 处**属性式 `DB_PATH` patch → 静默写生产库（✅已消灭，见下）；
   ② **28 个测试文件 66 处**引用入口，其中 **26 条断言**会因拆分变红（响亮）；
   ③ **6 处**测试 patch 入口的**内部符号**（`mod._conn`、`mod._get_ledger_raw`×5）——
     第二危险类：若门面转发了同名对象，patch 打不到实现 → **测试空过（假绿）**，
     所以门面**不得导出 `_*` 私有名**；
   ④ **4 个守护**靠解析入口源码枚举那 47 个工具（`skill_lint`/`test_se_docs`/
     `test_skill_integrity`/`test_docs_consistency`）→ 拆完它们看到 0 个工具；
   ⑤ 1 条连接白名单（✅已验证改法）；⑥ 常量访问（`getattr(mod, "HARVEST_SOURCE")` 等）。
   只有①会写坏数据、③会造假绿；②④⑥ 只会响亮地红 —— 所以它能分批做，
   但也说明入口的**命名空间已是 30 个测试文件的事实 API**，不能当一次性任务推。
   - 入口 2723 行 / 69 个顶层函数 / 47 个 `@mcp.tool()`。生成式拆分（逐字节搬运 + 组间 DAG 环
     检测）本身是成功的：工具面**逐项一致**（47=47，docstring 与入参 schema 零差异，
     入口降到 67 行）。但全量回归从 1 failed 变 6 failed。
   - 根因 = 入口被三类东西直接耦合：
     ① **6 处测试隔离靠 `mod.DB_PATH = tmp` / `monkeypatch.setattr(mod, "DB_PATH", …)`**。拆包后
     该赋值变成一个无人读取的悬空属性 → **不报错，测试直接写进生产 `data/wqb.db`**；
     ② 约 10 处断言直接读根文件的**源码文本**（`test_wave_verdict_enum`〔历史命名，非 `wave<N>_verdict` 废止键〕、`test_se_docs`、
     `test_skill_lint::test_mcp_registry_reads_real_signatures`、`test_ledger_key_catalog`、
     `test_index_tables` 等）；③ `wqb_db_mcp.py` 在 `db_conn.DIRECT_CONNECT_WHITELIST` 名单里。
   - **本次造成的数据污染（待处置，已精确圈定）**：失败那次全量运行在
     `2026-10-04T03:33:3x~4x` 时间窗写进了生产库 —— `registry_empirical` 2 行
     （`KOR-GATE-DEAD`、`KOR-LEGACY-DEAD`，均为测试字面量，可安全删）、
     `wave_results` 12 行 KOR 真实波次被覆盖、`ledger_kv` 5 行。
     复查方法：`SELECT … WHERE updated_at LIKE '2026-10-04T03:33%'`（只读）。
   - **不属于本次的同期变更**（已逐条归属）：非枚举 verdict `KOR/s2_oth466_d33 = MIXED_NO_SUBMIT`、
     裸 `sqlite3.connect`、本机盘符常量，均来自并行会话的 `tools/_kor_d33_writeback.py` 与
     `tools/_tmp_anl69_fields.py`；`test_sync_skills_reports_no_drift` 红是仓库副本新于安装位（
     跑 `python tools/sync_skills.py` 自愈，§8.12）。
   - **可复用的铁律（下次改结构前先过这一问）**：**任何改变模块结构的改动，都要问
     「测试的隔离机制会不会静默失效」**。按属性 patch（`mod.X = tmp`）在拆包/改名/重定位后
     不会报错，只会静默失去作用。正确顺序：**先把隐式 patch 换成显式 hook（如 `set_db_path()`）
     + 加生效断言 + 跑绿，第才能动文件**；顺序反了就是把生产库当测试沙箱。
   - ✅ **安全前置已落地（2026-10-04，同一会话）** —— 拆分现在可做，但仍有约 10 处
     「直接读根文件源码文本」的断言要一并改（见下）。已做的三件事：
     ① `wqb_db_mcp` 新增 `set_db_path()/get_db_path()`，`_store()`/`_conn()`/`get_submit_ready()`
     三个读库点全部改走 getter（**读写同源**：若只 patch getter，那些“patch 完再读
     `mod.DB_PATH` 做校验”的测试会读到陈值 —— 实测踩过）；
     ② **结果层硬闸** `_reject_production_db_under_tests()`：pytest 运行中（`PYTEST_CURRENT_TEST`）
     一旦库指向生产 `data/wqb.db` 就报错。故意只读真库的存量体检测试需显式
     `monkeypatch.setenv('WQB_ALLOW_REAL_DB','1')` 并写明理由（已按此放过
     `test_get_mining_yield_separates_conversion_from_yield`）；
     ③ **17 处**属性式 patch 全量迁到 hook（实际数量不是初估的 6 处），包括
     `monkeypatch.setattr(mod,"DB_PATH",…)` → `mod.set_db_path(…)`；
     另 `_GuardedModule` 只能**条件安装**（`sys.modules.get(__name__)`）—— 测试用
     `spec_from_file_location` 且不注册进 sys.modules 时，`sys.modules[__name__]` 会 KeyError（实测踩过）。
   - ⚠ 拆分仍待处理的**第二类耦合**：约 10 处断言直接读根文件源码文本
     （`test_wave_verdict_enum`〔历史命名，非 `wave<N>_verdict` 废止键〕、`test_se_docs`、`test_skill_lint::test_mcp_registry_reads_real_signatures`、
     `test_ledger_key_catalog`、`test_index_tables` 等）。它们会**响亮地红**（不是静默写库），
     所以风险等级低于 DB_PATH 那一类，但必须同批改。
10. **`tools/` 顶层仍在长（S11 已当场抓到）** —— 2026-10-04 冻结基线（171 个）后，并行会话又往
    顶层丢了 5 个一次性脚本（`_kor_d33_writeback.py`、`_tmp_anl69_fields.py`、`_tmp_build_a69.py`、
    `_tmp_build_afsf.py`、`_tmp_build_an82p.py`），其中 2 个已让 `test_db_write_guards`（裸 sqlite）
    与 `test_sd_portability`（本机盘符）变红。**处置归属**：这些是并行会话的在途工作，
    不要跨会话代删；按 §8.13 它们应落 `logs/_tmp_*.py` 或 `tracking/<REGION>/scripts/`。

### 8.5 审计纠错记录（2026-09-20，**方法论教训**）

本轮结构审计初版有 **3 处结论失实**，全部源于"未精确核验就下结论"：

| 初版结论（错） | 实测事实 | 根因 |
|---|---|---|
| gate 是"四份重复实现" | 是**分层流水线**（1 权威 + 包装 + 1 遗留） | 只看文件名相同，未读调用链（`_TOOLKIT_CANDIDATES`） |
| `CLAUDE.md` 是"宿主入口，指向 AGENTS.md" | 它承载 **alpha 挖掘准则**，不指向 AGENTS.md | 未读文件内容 |
| `info_data.bin` "15M 已入库" | **从未入库**（根 `.gitignore` `*.bin`） | 未跑 `git ls-files` / `git check-ignore` |

**铁律（写入 §4 失败诊断纪律的同源要求）**：结构性结论（"重复实现"/"已入库"/"无人引用"）
必须先用**机器级证据**核验再落笔——`git ls-files`、`git check-ignore`、调用链 grep、
真解析器抽样。这与项目既有"任何违规率/覆盖率数字必须先用真闸校验"是同一条纪律。

#### 第二轮（2026-09-25）：引用分析的两个新坑

再做一次全库"零引用"扫描时又踩两个坑，都是**会直接导致误删代码的那种**：

| 坑 | 错在哪 | 正确做法 |
|---|---|---|
| **子串 grep 高估引用** | `tools/pipeline_integration.py` 被 grep 到，但命中处是 `diversity_extract.py` 里的 **ledger key 字符串** `pipeline_integration_{dataset}`，不是 import；`docs` 里那条还是指向根本不存在的 `test_pipeline_integration.py` | 用**token 级计数**，命中后再人工判别，别把 grep 数字直接当结论 |
| **dotted token 漏票** | 首跑把 `src/wqb/research/selection_contract.py` 判成零引用——因为 `from wqb.research.selection_contract import …` 被整体当成一个 token，**切分后才有 `selection_contract`** | token 同时索引**按 `.` / `/` 切分后的各段**，否则 dotted import 全被误判为死代码 |

**最关键的一条**：**`refs=0` ≠ 死代码**。`tools/*.py` 绝大多数是**命令行工具**，天然
不被任何模块 import（`field_axis.py`、`combo_precheck.py`、`discover_datasets.py`…）。
必须**再看有无 `__main__` / argparse 入口**：有 → 是"未登记的 CLI 工具"（文档缺口，不能删）；
无 → 才是真死代码。本轮按此把疑似项从 22 个收敛到 **6 个**。

#### 全套件在本地全跑会红 —— 不是回归（2026-09-25 实测）

`pytest tests/ -q` 全量出现 25–34 个失败，但**每个失败文件单独跑都全绿**
（`test_build_wave_selection.py` 22/22、`test_db_write_guards.py` 14/14）。
根因两条：

1. **共享状态争用**：`logs/_slots`、`logs/_dblock`、`logs/_async_tasks` 是**进程级**共享状态，
   运行中的 MCP 服务与 pytest 抢同一把锁；
2. **沙箱 safe-delete 守卫**：守卫会截获对 `logs/_dblock/dbwrite.lock.json` 的删除，
   把守卫文本混进 subprocess stdout → `assert 'xxx' in out` 型断言失败，
   失败文本里能看到 `[safe-delete][SAFE_DELETE_BULK_CONFIRM_REQUIRED]`。

**判价顺序**：先看失败文件单独跑绿不绿 → 绿就不是回归。**别急于 revert**。
pre-commit 钩子已绕过第 2 条（见下一节：唯一 basetemp + TMPDIR 重定向）。


### 8.6 wave_results 写入单入口（2026-09-27 P0-1 / N30 固化）

`wave_results` 是停止规则 B（`campaign._run_stop_rules_gate`）的唯一输入，写错一行就是误停区或误放行。

- **只经写入契约写**：`src/wqb/wave_results_contract.upsert_wave_result`（合并式：只写传入的列；结案必带
  PASS/FAIL/PARTIAL；`created_at` 首写后不变）。现有写入方全部走它：wqb-db `upsert_wave_result`、
  `tools/mcp_batch_writer` 直写兜底、收批级联 `wqb_db_mcp._cascade_wave_result`、toolkit `_lib/wave_results`
  （review_wave / pipeline / `campaign.py wave upsert`）、`auto_pyramid` 点塔回写。**新增写入方禁止直写 SQL /
  `INSERT OR REPLACE`**（一次性迁移工具 `tools/migrate_*` 除外，须人工复核）。
- **波号一律原字符串**：`97`、`91c`、`s2_<ds>_d1` 原样入库，与 `backtest_results.wave` / `waves.wave_number`
  同键。禁止"取第一个数字"之类的派生（N30：`s2_<ds>_d1` 被写进第 2 波，评审顺延出的 105 撞上另一个真实波）。
- **结论归属**：评审（`source_file=pipeline:auto`）覆盖收批级联的暂定结论（`harvest:auto`）；级联不覆盖评审 /
  人工结论，不动显式 open 的行。各写入方只替换自己前缀的 key_findings 行（`[harvest]`、评审的
  `GREEN:`/`YELLOW:`/`RED:` 等、`[pyramid]`），其余保留。
- **verdict 归一只有一张表**：`wave_results_contract.normalize_verdict`；停止闸的 `_normalize_verdict` 委托它，
  不另写规则。

### 8.7 backtest_results.ra_failed_checks 口径（2026-09-28 第 4 项固化）

严格产出率（`get_mining_yield` / `campaign_intel`）、prod-first 选探针、toolkit `region_kb` 的本地闸门先验、
提交队列的 RA 闸都读这一列，都把"空"当作"平台 RA 硬闸全过"。

- **这一列只装 RA 资格门失败项**，定义只有一份：`wqb.config.compute_webdata_failed_counts`（R3）——18 项 RA check
  里 result 既不是 PASS 也不是 PENDING 的（WARNING / ERROR 也算）。空 / NULL = RA 全过。
- **唯一写入方** `CampaignStore.upsert_backtest_rows` 经 `wqb.store._backtest.ra_failed_names(row)` 取值：行里给了
  `ra_failed_checks` 就用它（只留 RA 项名；空列表 = 全过）→ 否则从完整 `checks` 现算 → 否则 `failed_checks ∩ RA`
  （旧缓存行，看不到 RA 项的 WARNING / ERROR）。
- **写入方手里有完整 checks，就按定义给 `ra_failed_checks`**：`compute_webdata_failed_counts(checks)["ra_failed_names"]`，
  或平台精简结构 `ra` 块里预算好的名单（RA 全过时不带名单键，按空列表处理）。不要自己数 FAIL。
- **`failed_checks` = 全部 FAIL 项名**（评审 / 诊断用），照旧留在行里与 `payload_json`。相关性等非 RA 失败读它，
  或读 `alphas.prod_correlation` / `self_correlation` 的数值（提交队列的相关性闸就看数值），不要从这一列推断。

### 8.8 alphas / backtest_results 写入是合并式（2026-09-28 N35 固化）

同一个 alpha 会被多条路径反复写入：收批（wqb-db `harvest_multisim_results`、`tools/harvest_multisim.py`）、
toolkit 评审（pipeline stage_review）、平台同步（`tools/sync_platform_alphas`）、相关性落库。
每次写入都只带它自己知道的那几列。

- **只经 CampaignStore 写**：
  - `upsert_backtest_rows` 写回测行，并同步 alphas；
  - `upsert_alpha_from_platform` 写平台详情；
  - 两者写 alphas 行时共用 `_write_alpha_row`；
  - 相关性单独落库走 `persist_correlation`。

  新增写入方不要自己拼整行覆盖的 `UPDATE alphas SET …`。一次性修数工具除外，但须人工复核。
- **没带不等于清空**：行里没有、或值为 None 的列保留原值，alphas 与 backtest_results 都是这样。
  `backtest_results.ra_failed_checks` 只在这一行说得清时才改。空列表表示 RA 全过，照样会覆盖旧名单。
- **生命周期不回退**：
  - `status` / `platform_status` 一旦是 ACTIVE / SUBMITTED / DECOMMISSIONED，就不会再被 UNSUBMITTED / COMPLETE 之类的值改回去；
  - `stage` 一旦是 OS，就不会再被 IS 改回去。

  已提交态之间可以互相变化，比如 ACTIVE 变 DECOMMISSIONED。
- **数据集归属**：
  - 调用方点名了数据集，才改归属；
  - 没点名（缺省为 `_unknown`），不动；
  - 字段投票这类推断，只补 `_unknown` 的行。
- **相关性**：写入时同时记 `prod_corr_source` 与 `corr_checked_at`。[0,1] 以外的值不算数。
- `backtest_results.payload_json` 仍是最近一次入库的原始行。需要"历次入库的并集"时读列，不要读 payload。

### 8.9 ledger 键目录 / 时间炸弹登记 / skill 文档棘轮（2026-09-29 固化）

- **ledger 键目录** `docs/ledger_keys.json` 是全库 `ledger_kv` 键的单一真相源（用途 / 写入方 / 读取方 / 缺失行为 / 刷新责任 / 状态）。
  `tools/ledger_keys.py` 从代码（AST + SQL 字面量）与文档抽取实际出现的键，`tests/unit/test_ledger_key_catalog.py` 守：**新增或改名一个
  ledger 键必须先登记**；被读取的键必须有写入方（已知缺口登记 `orphan` 并指向审查条目，缺口补上后必须删登记）；登记的代码引用必须真实存在；
  已废止的键（`wave<N>_verdict` 等）只能出现在带「废止 / 历史」字样的行。`python tools/ledger_keys.py` 打印差异，`--print-table` 生成文档表。
- **时间炸弹登记** `docs/time_bombs.json`：凡「到某日会自动改变行为或让文案失效」（灰度截止、到期放行、夏令时……）先登记再写文案。
  `tests/unit/test_time_bombs.py` 守：证据文件 / 测试真实存在、人工项过期未办完即红、文档里出现的**未来日期**必须已登记。
- **skill 文档「内容为真」棘轮** `tools/skill_lint.py`：命令 / 子命令 / 必填参数（argparse AST）、MCP 工具签名、表达式过闸、`.env` 读取、裸 `python`。
  现存违规登记在 `tests/fixtures/skill_lint_baseline.json`，**新增必红、修复必须从基线移除**；反例段落用 `<!-- lint:counterexample -->` 豁免。

### 8.10 INDEX 拆分 / 生成表 / 环境变量与凭据登记（2026-09-29 固化，skills 审查 IX-01…24）

- **INDEX 只做路由与分层**。契约（frontmatter / 职责边界 / 命名 / 共享产物 / 质量门禁）在 `Claude/skills/CONTRACT.md`；术语与状态词表在 `GLOSSARY.md`；
  变更历史与迁移记录在 `Claude/skills/CHANGELOG.md`（带日期的 ⚠ 条目**不得**再写进 INDEX，`tests/unit/test_index_tables.py` 守）；
  环境变量、开关、凭据来源在 `docs/env_and_switches.md`。用户意图 → skill 的**场景路由表**在 INDEX 首节。
- **可由代码导出的表由代码生成并嵌入文档**：区域清单（`config.REGIONS` × profile × `tracking/<R>/config/`）、闸门阶梯（`config` 的 `GATES_*` / `PLATFORM_CHECK_LINES`）、
  环境变量目录（代码扫描 + `docs/env_registry.json` 的用途）。生成器 `python tools/index_tables.py {regions|ladder|env}`；`--apply` 覆盖嵌入块、`--check` 比对。
  **改 profile / 目录 / config 常量 / 读取了新环境变量后必须重新 `--apply`**，不要手改表。
- **环境变量登记**：代码里新读一个环境变量 = 先在 `docs/env_registry.json` 登记（类别 + 用途）再 `--apply`；登记的变量不再被读取时必须删除。
  **凭据只登记名字与来源，不登记值**；标准名 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`，新增凭据消费者必须先认标准名，并在 `docs/env_and_switches.md` §1 登记来源顺序与是否落盘。
  vendored `ace_lib.get_credentials()` 会把口令**明文写进** `~/secrets/platform-brain.json`——任何调用 `ace_lib.start_session()` 的脚本必须先覆盖它（`tests/unit/test_sf_docs.py` 守）。
- **改 skill 的生效流程**：仓库 `Claude/skills/` 是编辑权威，各安装位是运行时优先——**改完必须 `$WQ_PY tools/sync_skills.py`（`--check` 零漂移）才对 Agent 生效**。
  `description` ≤ 300 字且只写触发条件（`test_sf_docs.py` 守）。

### 8.11 论坛取证证据契约 / 判死闸 / 波级默认取证 / 形状配额（2026-09-30 落地）

- **故障 ≠ 无解（2026-09-29 事故：5 条 recon 记录里 2 条是工具故障，被记成 `found=false` 当判死证据）**。取证只有三种结局：`ok`（`found=true`）/ `no_result`（`found=false`，检索**可靠**完成）/ `error`（`found=null`，工具故障）。
  **单一实现 = `src/wqb/recon_evidence.py`**（`forum_recon_*` 键名、记录分类、判死闸判定）：写入方 `tools/forum_recon.py` / `tools/forum_recon_wave.py`、判死闸 `wqb_db_mcp.seal_dead_end`、
  统计方 `tools/step_funnel.py` 都从它取——**不要在别处再拼 `forum_recon_*` 键或再判一遍 `found`**。故障绝不落 `forum_recon_negative_*`、不入 7 天缓存；旧版遗留的「`found=false` + `error`」记录按故障处理。
- **`seal_dead_end` 取证闸是 fail-closed**：按 `question_key` 回 ledger 核对，只放行可靠的「论坛无解」；拒绝时**不沉降、不写库**。绕过只有 `force_seal=True` / `require_forum_recon=False`，**必须人工确认**，都留痕在 `payload.forum_recon_gate`。
  ⚠ **闸只在 `seal_dead_end` 上**：`campaign.py registry add-dead-end`（CLI 备选）与 `upsert_registry_empirical(layer="dead_end")`（低层写入口）不经闸——判死统一走 `seal_dead_end`；闸不核对证据的相关性、不给证据龄设上限（留痕的 `question` / `searched_at` 供人复核）。
- **波级默认取证**：`tools/forum_recon_wave.py` = 节点 `forum_recon_wave` = `pipeline.py --forum-recon`（`batch_track` 缺省带上，`forum_recon=False` 关）。问题由本波回测行机械派生（`src/wqb/recon_wave.py`），每波 ≤ 1 次，
  可靠结局占额度、故障不占。**墙词表必须与 `config.RA_CHECK_NAMES` 一一对应**（`tests/unit/test_recon_wave.py` 守）——config 新增一项 RA 闸而这里没给它墙，测试即红。
- **形状配额**：`tools/shape_quota_check.py`（分类规则 `src/wqb/shape_quota.py`，启发式；阈值 ≥ 3 个形状族、`trade_when` ≤ 40% 来自步 4 §4.5.1 准则）只读、不入闸链，闸 6 才是批级多样性的权威。
- **live 论坛路径没有端到端实测过**（无凭据 / 无出口）：测试覆盖到假 session / 假检索轮；首次真跑先 `--dry-run`。此前该路径**从未跑通过**（`load_creds(None)` 永远 TypeError），所有真实调用都落进了「鉴权失败 → 记成无解」。

### 8.12 仓库结构守护与可安装包（2026-09-30 落地）

- **`src/wqb` 已改为正式可安装包**（推翻 8.4 第 2 条的旧决策）：`pyproject.toml` 声明
  `[tool.setuptools.packages.find] where=["src"] include=["wqb*"]`，`pip install -e .` 后
  `import wqb` 在**任意工作目录**可用（实测从仓库外目录导入成功，14 个区域正常加载）。
  依据是当时 2709 个测试全绿，回归网足够。
- **`tools/audit_structure.py` 是结构守护，已挂 pre-commit**（`core.hooksPath = tools/git-hooks`）：
  S1 sys.path 自举/外挂分类 · S2 src→tools 依赖方向 · S3 跨层同名 · S4 硬编码盘符 ·
  S5 reports/ 散落脚本 · S6 skills 副本漂移 · **S7 根目录白名单 · S8 根↔子目录同名分叉 ·
  S9 文档声明目录存在性 · S10 区域子目录完整性 · S11 tools/ 顶层冻结 ·
  **S12 已下架路径不得复活**
  （2026-10-04 新增，后六条是为根目录第 5 次污染、`tools/` 上帝目录、与
  “归档后又被恢复”三件事补的闸）。
  **FAIL 阻断：S1/S2/S4/S7/S8/S9/S10/S11/S12**（S8 分叉、S11 新增顶层、S12 复活
  都不进基线豁免：分叉没有合法存量形态，顶层只减不增，已下架不得回来）；
  **WARN 不阻塞：S3/S5/S6**（存量已登记）。
  单项自查：`python tools/audit_structure.py --only s7`。S11 基线 = 171 个顶层脚本，
  建/重置用 `--freeze-tools-top`；S12 清单在基线的 `retired_paths`。
- **S3「同名」不是缺陷**：`tools/x.py` 与 `src/wqb/**/x.py` 分属脚本与包两套命名空间，import 不会撞
  （实测 `import wave_gate` 报 ModuleNotFoundError，它只以 `wqb.workflow.nodes.wave_gate` 存在）。**勿改名。**
- **`wave_gate` 包化收尾（2026-09-30）**：`tools/wave_gate.py` = 入口 shim（~140 行：argparse 契约字面 +
  `parser_factory()` + 历史符号全量重导出）；实现 12 模块在 `tools/wave_gate_pkg/`（编排 `cli.py`，
  各闸 `gates_*`，waiver 在 `gates_waiver.py`）。**改 flag/argparse 动 shim，且勿把 add_argument 挪进包**
  （`wqb.workflow._common.validate_argv` 的静态解析会 fail-open）；改闸逻辑动包内模块。
  `monkeypatch.setattr(wave_gate, ...)` 的测试契约由 `_compat` 晚绑定保住。
- **pre-commit 钩子的解释器**：钩子由 git 自带的 sh 执行，PATH 与交互式 shell 不同（实测会把 `python`
  解析到无 pytest 的 LobsterAI 运行时，导致钩子每次提交都误报失败）。钩子已改为**优先用
  `<repo>/.venv/Scripts/python.exe`**，无 venv 才退回 PATH。手写 shell 调用时注意同一问题。
- **`tools/audit_skill_drift.py` 管仓库内 skill 之间的副本漂移**（区别于 `sync_skills.py` 的仓库→安装位同步）：
  A 类（GEM 内嵌快照，由 `sync_gem_embedded_skill.py` 同步，设计内保留）不报，只报 B 类跨 skill 复制。
  当前 B=3 组：`validator.py`（4 份）/ `helpful_functions.py`（4 份）/ `ace_lib.py`（2 份）。
  **改这些文件时四处一起覆盖**——历史上曾三份 validator 各自演化、缺 hump/bucket/densify 修复。
- **`tools/clean_logs.py` 管 logs/ 运行期清理**：默认 dry-run，`--apply` 才删。
  `--report-locked` 探测 ACL 锁死目录并打印**需管理员执行**的 takeown/icacls/rmdir 命令——
  **不自行提权**（删除纪律要求人工确认）。非提权进程删不掉锁死目录，不要反复重试。
- **归档一律用 `tools/legacy/`（产物脚本）或各目录自带的 `archive/`**（区域探针，如
  `tracking/KOR/scripts/archive/`），且**必须先核 refs=0**（`git grep -w <name>`）。
  `reports/` 下带日期前缀的 .py 看着像一次性产物，实际常是审查结论的**可重跑证据**
  （报告里写着「可复现：`python reports/xxx.py`」），`audit_structure` 的 `S5_EXEMPT_PREFIXES`
  已登记豁免。判据全文见 `tools/legacy/README.md`。
- **skills 目录禁止放明文凭据**：`Claude/skills/**/config.json` 已 gitignore（GEM 内嵌副本是引擎硬依赖，
  凭据落这里等于交给任何能跑引擎的进程）。2026-09-30 曾在内嵌 `brain-feature-implementation/config.json`
  发现明文 email+password（未入库，已移出）。
- **测试的两个环境前提**（Windows）：符号链接需开发者模式/管理员，否则 `test_pull_skills_safety`
  的链接识别用例 skip；`test_sync_skills_reports_no_drift` 会因「仓库已改 / 安装位未同步」的时序差失败，
  跑一次 `python tools/sync_skills.py` 即自愈——**判断回归归属前先看 `git status` 有没有你改过该文件**。

### 8.13 目录归属与命名规范（2026-10-04 结构治理固化）

新增文件先问「放哪」，只有一条路（机器守卫：`audit_structure` S7 白名单 + S8 分叉 + S9 声明存在性）：

| 你要放的东西 | 唯一去处 | 反例（都曾真实发生过） |
|---|---|---|
| 可复用 CLI | `tools/`，并在 `tools/README.md` 登记一行 | 6 个「论坛工作台」脚本散落仓库根 → 与 `tools/` 副本分叉成**互为超集**的两份 |
| 一次性/会话草稿脚本 | `logs/_tmp_*.py`（用完即删） | `cache/` 里 22 个 `_gen_*/_log_*.py` 固化成无人管的资产 |
| 区域专属探针 | `tracking/<REGION>/scripts/`，用完进 `scripts/archive/` | `tracking/reference/` 积了 54 个 `tmp_*` + 37 个 `gen_*` |
| 战役/评审**产物**报告 | `output_report/`（2026-10-01 定案的**报告唯一出口**） | `reports/` 与 `output_report/` 两头分流，检索靠运气 |
| 人工审计与复盘 | `reports/<主题>_<YYYYMMDD>.md` | 同一份 review 在两个目录各留一版 |
| 长期规范 / SOP / 速查 | `docs/`（`docs/README.md` 索引必须与实际目录一致） | `docs/README.md` 索引着不存在的 `architecture/` |
| 运行期产物 | `cache/`（断点）`logs/`（日志）`results/`（续跑 checkpoint） | `sa_*.log`、`dump.rdb`、`0` 落在根 |
| 归档 | `attic/<主题>_<YYYYMMDD>/`（**归档而非删除**，§7） | `mining/` 14 个脚本被工作树清空却仍留在 git 索引 |

**命名规范**（新建即守，存量不强制回改）：

- **目录**：小写 kebab-case；`_` 前缀 = 同层内部/横切；第三方源码只进 `vendor/`
  （下一份 WebDataScope 副本放这里，别再往 `research-data/` 与 `extensions/` 各拷一份）。
  例外：`tracking/<REGION>` 三字母大写是**平台数据标识**，不属目录命名；`Claude/`、`output_report/`
  为历史名，保留但不新增此类风格。
  ⚠ `tracking/` 同层的 `FORUM`/`PPA_USA`/`prod_probe`/`hypotheses`/`mining` **都不是区域**，
  新 Agent 极易当成区域读；现有五个搬迁代价 > 收益，**只做约定**：再增非区域目录一律 `_` 前缀。
- **文件**：纯 snake_case；包内私有实现 `_` 前缀（`store/_alphas.py` 已是范式）。
- **活探针禁止 `test_` 前缀**：用 `probe_*` / `*_live`。`test_` 名字 + 不在 `testpaths` 内
  = 既不被收集又骗人（`world-quant-brain-mcp/probe_direct_auth.py`、`probe_labs_live.py` 即此形态，
  2026-10-04 改名）。处置纪律 = **改名，不搬家**：搬进 `tests/` 会让 pytest 真去跑平台 API
  （与 §8.4 第 4 条对 `tools/test_*.py` 的结论同一）。
- **日期**：产物与报告一律 `YYYYMMDD` **作后缀**（`skills_review_20261003.md`）；
  `docs/plans/` 保持 `YYYY-MM-DD-<主题>.md` **前缀**（该目录已成型，同目录内不混用）。
  停止 `2026-10-02_xxx.md` 这种前缀带杠写法。
- **路径一律纯 ASCII**，不含空格/中文/Windows 保留名（`nul`/`con`/`0`/`-`）。非 ASCII 名会让
  `git` 需 `core.quotepath=false`、脚本处理与跨平台同步都出摩擦；中文放正文，别放文件名。
- **仓库根推导一律层数无关**（2026-10-04 P2-1 新增）：新代码用 `from wqb.paths import repo_root`
  （向上探测 `pyproject.toml` + `src/wqb` 双标记，解析失败**显式报错**不猜根）；
  脚本里写 `find_repo_root(__file__)` 即可与自身深度解耦。
  **禁止新增** `parents[1]` / `dirname(dirname())` 这类层数硬编码——实测仓库内有 5 种同义写法并存，
  文件一旦移动一层就静默指错目录（DB 路径/报告输出/归档全错）。存量不强制回改，
  但按 `tools/README.md` 「单文件迁移配方」在每次实际移动该文件时顺手换掉。

**tools/ 主题下沉（P2-1，2026-10-04）**：顶层 171 个脚本的目标结构与逐文件归属已固化到
`tools/THEMES.json`（19 个 kebab 主题目录，171/171 已归属；另 4 个区域专属脚本标记应迁出至
`tracking/KOR/scripts/`）。**当场全量下沉已评估并否定**：实测全仓 80 处 `sys.path.insert(...'tools')`、
`index_tables`/`migrate_wave_verdict_enum`〔历史命名，非 `wave<N>_verdict` 废止键〕等被当模块 import、仓库根推导 5 种写法——下沉一层同时改变
import 解析与路径层数，且都在运行期才爆。因此采用 S11 冻结顶层（新增即 FAIL）+ 按主题逐批迁移，
配方与实测耦合数据见 `tools/README.md` 「目录结构与迁移状态」。

**本轮定案**（作为 §8.4 台账的补充，两边不得重复描述）：

1. **`output_report/` 仍是报告唯一出口**。上一轮结构建议里「把 `output_report/` 并入 `reports/`」的方向
   **已作废**（与 2026-10-01 定案冲突）；同样作废的还有「`info_data.bin` 外迁」与
   「`tools/test_field_catalog_cache.py` 搬进 `tests/`」——它们都是已结案项（§8.4 第 1/4 条）。
2. **论坛/工作台整端下架** `attic/forum_workbench_20261004/`：UI 模板 `wq_workbench.html`
   **从未入库且全盘不存在** → 部署/托管链路不可运行；论坛读取能力由 MCP
   `search_forum_posts`/`read_forum_post` + `tools/forum_recon.py` + `brain-forum-browse` 承接；
   滚动清理由 `tools/retention.py`（§8.4 第 6 项）承接。不依赖 UI 的测试跑批半段**转正为工具**：
   `tools/scan_test_groups.py` + `tools/run_grouped_tests.py`（产物 `cache/test_groups.json`）。
   ⚠ 指向 `tools/forum_workbench/wq_daily_refresh.py` 的每晚 21:30 自动化必须停用（否则每晚 exit≠0）。
3. **`mining/` 幽灵索引已摘**：15 个文件从 HEAD 恢复后归档 `attic/mining_scripts_20261004/`；
   §1 职责表不再声明 `mining/` 与 `data_ref/`（两者磁盘均不存在），S9 会持续校这一点。
4. `world-quant-brain-mcp/downloads/`（`brain_mixin_correlation.py:72` 的 `cache_dir`）与
   `config/info_data.bin`（`brain_mixin_transport.py:105`）**不是冗余**，是代码硬编码的运行时位，勿外迁。

### 8.14 区域 × 类别控制层（2026-10-04 落地；方案与落地记录 `docs/plans/2026-10-04-ra-region-category-split.md`）

- **区域差异写数据，不写代码分支**：回测设置在 `tracking/<R>/config/settings.json`，阈值在 `thresholds.json`，
  「区域 × 类别」组合的覆盖在 `cells.json`（只存覆盖，每条带 `_evidence`），跨区类别知识在
  `src/wqb/profiles/category_cards.json`（只收 ≥ 2 区复现的结论），单国 / 多国口径在 `config.REGION_COUNTRY_SCOPE`。
  棘轮 `tests/unit/07_docs_skills/test_region_control_ratchets.py`：代码里新增按区域代码字面量的分支 / 查表即红，
  `thresholds.json` 新增没人读取的键即红；两份基线（`tests/fixtures/region_literal_baseline.json`、
  `threshold_unread_keys_baseline.json`）只许减，修掉一条就删一条。
- **解析单入口**：`wqb.profiles.resolve()`，人读用 `$WQ_PY -m wqb.profiles explain --region <R> --dataset <ds>`（每个生效值带来源层）。
  消费方：`workflow_batch_track` 把组合回测覆盖以 `--set` 钉住；toolkit `CampaignContext.bind_cell` 让直跑 `pipeline.py` 同样生效
  （设置先验不改被钉住的维度）；`mode_b_config.load_mode_b_config(store, region, category)` 读组合的 `mode_b.*`。
- **锁定表**（`src/wqb/profiles/locked.py`）任何层都不能覆盖：禁混信号、Mode B 主闸下限（GLOBAL `mode_b_qualification`，只许收紧——
  `mode_b_config` 加载时钳制并在 `_clamped_from` 留档，`mode_b_adaptive` 写库前钳制）、D0-P、平台线、窗口白名单、
  已点亮塔不作主数据集、truncation 不作扫描维度、提交前用户确认。
- **区域 skill 是生成物**：`Claude/skills/wq-brain-ra-<区域小写>/`（layer `L-RA-R`）的生成块只由
  `$WQ_PY -m wqb.profiles render --apply` 写，手写内容只放 `profiles:manual` 块（重渲原样保留）。改了 `cells.json` /
  profile / 类别卡之后：`render --apply` → `tools/sync_skills.py --apply` → `$WQ_PY -m wqb.profiles check`（测试守面板与 settings.json 一致、无孤儿文件）。
  判死 / 胜绩刷新用 `sync-cells --region <R> --apply`（只写文件、不写库，保留人写字段）。
