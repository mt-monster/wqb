# AGENTS.md — wqb（WorldQuant BRAIN Alpha 挖掘工作区）

## 1. 项目概述与模块职责

本工作区用于 WorldQuant BRAIN 平台的 alpha 挖掘、回测、评审与提交，Python 脚本驱动，无统一应用框架；MCP 服务是本项目与编码 Agent 的主要接口。

| 目录 | 职责 | 变更注意 |
|---|---|---|
| `world-quant-brain-mcp/` | MCP 服务（`wq-brain-http`）：`brain_api.py` 为门面（36 行），方法体 verbatim 拆至 `brain_mixin_transport/auth/simulation/spcread/correlation.py`；模型 `brain_api_models.py`、配置 `brain_config.py`；回测/提交/论坛工具在 `tools_*` | 运行中服务，改 `brain_mixin_*` 需回归 `world-quant-brain-mcp/tests/` |
| `tracking/` | 区域战役追踪（KOR/USA/EUR/IND/GLB/DEU…）：candidates/results/reviews/scripts | `tracking/mining/` 为共享数据湖，勿改动/移动；全量索引见 `tracking/reference/tooling/generate_manifest.py`（`MANIFEST.json` 当前未生成） |
| `mining/` | 挖掘脚本与归档 | 改动影响战役 pipeline |
| `tools/` | 工具链（字段解析、质量检查、同步等） | 被多区域脚本引用，改动前先查调用点 |
| `reports/` | 报告产物 | — |
| `data/` `data_ref/` | 事件数据与参考字段 | 只读数据 |
| `src/wqb/` | **规范核心包（single source of truth）**：config/expression/research/search/memory；区域/算子/中性化域常量唯一来源（见 `config.py`） | 行为变更须保持根 `tests/` 313 个单测全绿 |
| `tests/` | pytest 单元测试（根 313 + MCP 包 79；根 `tests/` 递归包含 `tests/unit/`，见 §4） | 见 §4 |
| `docs/` | 计划、参考、经验文档 | 行为变更需同步相关文档 |
| `attic/` | 隔离归档（`tools_archive`/`mining_archive`/`root_scripts`/`experience_scripts`）+ `brain_api_backup/`（原码与拆解态备份） | 只读归档，勿回迁进活跃代码 |

## 2. 核心入口文件

- `world-quant-brain-mcp/main.py` — MCP 服务入口（`.mcp.json` 注册为 `wq-brain-http`，stdio 启动）
- `world-quant-brain-mcp/brain_api.py` — BRAIN API 客户端**门面**（36 行）；方法体 verbatim 拆至 `brain_mixin_transport/auth/simulation/spcread/correlation.py`，保持 `BrainApiClient` 类名与 `brain_client` 单例 + 旧导入路径（`from brain_api import brain_client/BrainApiClient/load_config/SimulationSettings/...`）不变
- `world-quant-brain-mcp/brain_api_models.py` — 纯数据模型（Pydantic）：`AuthCredentials`/`SimulationSettings`/`SimulationData`
- `world-quant-brain-mcp/brain_config.py` — 配置函数：`_resolve_config_path`/`_load_dotenv_into_environ`/`load_config`
- `world-quant-brain-mcp/mcp_core.py` — MCP 工具注册与分发
- `src/wqb/config.py` — **规范域常量**：区域/算子家族/中性化（数据源 `data/operators_verified.json`）；MCP 包与 `pipeline/`/`tools/gate.py` 共享引用
- `tracking/reference/tooling/generate_manifest.py` — 追踪目录全量索引生成器（产出 `tracking/MANIFEST.json`，当前未生成；注意该脚本会顺带把 >500 KB 文件 zip 归档到 `tracking/archive/large/`）
- `pytest.ini` — 测试配置（验证路由）
- `world-quant-brain-mcp/Makefile` — Docker 部署入口（`make up` / `make down`）

## 3. 变更影响范围指引

- 修改 `world-quant-brain-mcp/` 后需重启 MCP 服务才生效（`.mcp.json` 指向 `main.py`，使用 `world-quant-brain-mcp/.venv`，勿用根环境）。
- 修改 `tracking/<REGION>/config/`（如 `thresholds.json`）影响该区域战役闸门；勿手动编辑 `tracking/mining/` 共享数据湖。
- 修改 `tools/` 中被引用函数前，先用 `rg` 搜索调用点确认影响面。
- 平台交互类改动（回测/提交/配额）先读 `docs/experience/` 经验文档，遵守并发与配额约束，避免 429。
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
| 5 | S2→S3 门禁 | `wave_gate`（已内置体检硬门 `tools/field_inspect_gate.py`；多样性走 toolkit `gate.py` 闸6） |
| 6 | S3 七槽回测 | `workflow_batch_track`（并发纪律权威 = `wqb-concurrency` §8） |
| 7 | S4 诊断改进 | `workflow_campaign(stage="S4")` + `wq-brain-alpha-optimization-v1` |
| 8 | S4→S5 稳健闸与提交判定 | `brain-alpha-robustness` → `submit_verdict`（唯一权威）→ 用户确认 → `workflow_submit_alpha` |
| 9 | S6 复盘回写 | `mcp__wqb-db__upsert_wave_result` / `upsert_registry_empirical` / `upsert_ledger_key` |

整链可用 `mcp__wq-brain-http__workflow_chain`（先 `dry_run=True` 看每步构建出的命令）。
**但提交类节点不入自动链**：`workflow_submit_alpha` / `workflow_superalpha` 的
`confirm_submit=True` 必须由用户在步 8 明确确认后单独调用。

**几条不在 SKILL.md、属仓库工程约定的补充**：

- **判定与提交的权威划分**：提交判定唯一权威 = `tools/submit_verdict.py`（MCP `submit_verdict`）。
  `brain-alpha-judge` / `workflow_judge` 是**参考评审层**，2026-09-05 起代码里已无提交路径。
- **workflow 节点元数据**：`registry.py` 的 `required_params` / `optional_params` 必须与节点
  `run()` 签名一致（`_context` / `dry_run` 除外）。`workflow_list_nodes` 把它当 API 文档
  暴露给 Agent，漂移即误导。回归由 `tests/unit/test_skill_integrity.py` 守护。
- **dry-run 契约**：全部 7 个节点统一「走完零成本前置 → 构建出命令/请求计划 → 到此为止」，
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
  （`%APPDATA%\Claude\skills` 等）> `~/.claude/skills` > `~/.codex/skills` > 历史 Agent 位
  （qoder-cn / cursor / workbuddy）> 仓库自带 `Claude/skills/`（兜底，保证 clone 即可用）。
  落到历史 Agent 位会打 WARNING：那些是独立物理拷贝。
- **skill 多目标单向同步（2026-09-10 起）**：仓库 `Claude/skills/` 是源，**全部安装位**是派生物。
  改 skill 只改仓库副本，然后 `python tools/sync_skills.py`（自动枚举全部已存在的安装位：
  claude / codex / qoder-cn / cursor / workbuddy，逐个同步 + 逐个校验）；`--check` 模式由
  `tests/unit/test_audit_fixes.py::test_sync_skills_reports_no_drift` 守护（多目标断言）。
  历史教训：① 安装位曾落后仓库两周（make-some-gem 停在 08-22、仓库已 09-05）；
  ② 2026-09-10 审计发现旧版脚本只同步**首个**目标（`resolve_install_root()`），致使
  `~/.codex`、`~/.workbuddy` 反复分叉（ra-pipeline 落后 67 行，缺 09-09 的
  `campaign_intel s0-select` 选集与 `ghost-audit` 幽灵算子硬闸）—— 故改为多目标。
  失效安装器（`install_now.py` / `install_claude_skills.*` / `verify_claude_skills.py` /
  `install_skills_direct.py` / `INSTALLATION_GUIDE.md`）已归档 `attic/install_legacy_20260910/`，
  勿再用它们做更新（`if target.exists(): skip` 永不更新）。
- **MCP 服务器命名**：只能是 `wq-brain-http` 与 `wqb-db` —— 所有 skill 调用的工具前缀是
  `mcp__wq-brain-http__*` / `mcp__wqb-db__*`，改名即全线失配。`.mcp.json` 为准，
  `mcp_config.json` 与安装脚本必须跟随。

### Skill layer 取值表

`SKILL.md` frontmatter 的 `layer` 只表示"在挖掘链条上的位置"，不是优先级：

| layer | 含义 | 例 |
|---|---|---|
| `L-RA` | 唯一编排入口 | `wq-brain-ra-pipeline` |
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

### SKILL.md frontmatter 契约（2026-09-10 审计固化）

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
| `brain-alpha-repair` | L4 | 弱候选修复/演化（降 turnover、提覆盖、降相关、失败轨迹恢复）。**配方已上移 `wq-brain-alpha-optimization-v1`**，本 skill 仅保留入口与边界声明 |
| `brain-datafield-exploration-general` | L1 | 评估单个新 datafield（覆盖率 / 非零值 / 更新频率 / 分布形态） |
| `brain-explain-alphas` | L4 | 解释某个 alpha 表达式 / 字段 / 算子协作 |

## 3.x 单源核心与 brain_api 拆解约定（Direction A）

- **`src/wqb` 为唯一规范核心**（single source of truth）：区域/算子/中性化等域常量只在此定义；MCP 包与 `pipeline/`/`tools/gate.py` 共享引用，新增域知识只写 `src/wqb`，勿在 `world-quant-brain-mcp/` 重复硬编码。
- **`brain_api` 为稳定 API 客户端，方法逻辑不重写**：`BrainApiClient` 仅继承 5 个 mixin（`TransportMixin`/`AuthMixin`/`SimulationMixin`/`SpcDataMixin`/`CorrelationMixin`），方法体 verbatim 迁移；扩展新端点时**新增 mixin 方法**，勿改动既有方法实现。
- **原码备份（勿依赖 git 之外的临时副本）**：原始 4074 行整文件 `attic/brain_api_backup/original/brain_api.py`；拆解后 7 文件 `attic/brain_api_backup/current_refactored/`（brain_api.py + brain_config.py + brain_api_models.py + 5×brain_mixin_*.py）。
- labs 特性 `labs_data_analysis_agent.py` 由 `labs_functions.emit_labs_script` 经 `read_text()` 整文件读入后粘贴进 BRAIN Labs，**不可拆分**。

## 4. 测试与验证路径

编辑后必须运行验证：

```bash
python -m pytest tests/ -x
```

- 结果自动写入 `logs/test-results.xml`（JUnit XML，可追溯）。
- 当前根 `tests/` **313 个测试全部通过**（`src/wqb` 包于 2026-08-16 按 `docs/plans/2026-08-02-wqb-src-reconstruction.md` 重建；仓库根**没有** `conftest.py`，由 `tests/conftest.py` 同时把 `src/` 与 `world-quant-brain-mcp/` 注入 `sys.path`，`tests/unit/` 继承之）。MCP 包 `world-quant-brain-mcp/tests/` 另含 **79 个测试**（需 `.venv`；其 `conftest.py` 只注入 MCP 目录，验证 `brain_api` 拆解不变量与工具注册）。pre-commit 钩子仅跑根 `tests/`，MCP 包测试需单独在 `.venv` 跑。
- **计数口径：根 `tests/` 递归包含 `tests/unit/`，勿把两者相加。** `tests/` 直接子层只有 `test_toolified_cli.py`（10 个）+ `conftest.py`；`tests/unit/` 含 `__init__.py` 与 15 个 `test_*.py`（303 个）。故 `313 = 10 + 303`，且 `pytest tests/` 与 `pytest tests/unit tests` 收集数相同（均为 313）。新增用例时以 `pytest --collect-only -q | tail -1` 为准，不在此处硬编码逐文件明细。
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
| 每波门禁（语法+5 闸+多样性，一键落盘） | `tools/wave_gate.py --campaign-dir … --dataset … --wave N --candidates <json>`（替代 `tracking/<R>/scripts/_gate_waveNN.py`） |
| 批次/子任务状态查询+轮询 | `tools/batch_status.py --ids … [--watch]`（替代 `tracking/_scratch/check_*batch*.py`） |
| SA 组件池探针（≥10 ACTIVE 硬前置） | `tools/sa_probe.py --region …`（替代 `probe_*sa*.py`） |
| 提交层判定（403 盲区） | `tools/submit_verdict.py --alpha-id …`（替代手写 GET /alphas/{id}/submit） |
| SUPER 组套/提交全流程 | `tools/super_build.py {select|status|probe|submit} …`（替代 `track_mea_super*.py`） |
| 批量提交 | `tools/submit_batch.py`（替代 `_submit_*.py`） |

执行约定：
1. 网络工具一律用 MCP venv（`$WQ_PY` 或 `world-quant-brain-mcp/.venv`）运行，工具已内置自动切换；
   不手写 requests 脚本（429 事故根因之一），统一走 `BrainApiClient`（自带 429 退避）。
2. skill 依赖路径用 `WQ_VALIDATOR_DIR` / `WQ_TOOLKIT_DIR` 或自动搜索 `.qoder-cn`/`.workbuddy`/`.cursor`，禁止硬编码 `C:\Users\...` 绝对路径。
3. 一次性排障探针（`_inspect_*`/`probe_payment*` 等探索类）仍可写 `tracking/_scratch/`，但结论落地后归档 `attic/`，不留在活跃目录累积。
