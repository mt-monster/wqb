# AGENTS.md — wqb（WorldQuant BRAIN Alpha 挖掘工作区）

## 1. 项目概述与模块职责

本工作区用于 WorldQuant BRAIN 平台的 alpha 挖掘、回测、评审与提交，Python 脚本驱动，无统一应用框架；MCP 服务是本项目与编码 Agent 的主要接口。

| 目录 | 职责 | 变更注意 |
|---|---|---|
| `world-quant-brain-mcp/` | MCP 服务（`wq-brain-http`）：`brain_api.py` 为门面（36 行），方法体 verbatim 拆至 `brain_mixin_transport/auth/simulation/spcread/correlation.py`；模型 `brain_api_models.py`、配置 `brain_config.py`；回测/提交/论坛工具在 `tools_*` | 运行中服务，改 `brain_mixin_*` 需回归 `world-quant-brain-mcp/tests/` |
| `tracking/` | 区域战役追踪（KOR/USA/EUR/IND/GLB/DEU…）：candidates/results/reviews/scripts | `tracking/mining/` 为共享数据湖，勿改动/移动；`MANIFEST.json` 为全量索引 |
| `mining/` | 挖掘脚本与归档 | 改动影响战役 pipeline |
| `tools/` | 工具链（字段解析、质量检查、同步等） | 被多区域脚本引用，改动前先查调用点 |
| `reports/` | 报告产物 | — |
| `data/` `data_ref/` | 事件数据与参考字段 | 只读数据 |
| `src/wqb/` | **规范核心包（single source of truth）**：config/expression/research/search/memory；区域/算子/中性化域常量唯一来源（见 `config.py`） | 行为变更须保持根 `tests/` 254 个单测全绿 |
| `tests/` | pytest 单元测试（根 254 + MCP 包 34） | 见 §4 |
| `docs/` | 计划、参考、经验文档 | 行为变更需同步相关文档 |
| `attic/` | 隔离归档（`tools_archive`/`mining_archive`/`root_scripts`/`experience_scripts`）+ `brain_api_backup/`（原码与拆解态备份） | 只读归档，勿回迁进活跃代码 |

## 2. 核心入口文件

- `world-quant-brain-mcp/main.py` — MCP 服务入口（`.mcp.json` 注册为 `wq-brain-http`，stdio 启动）
- `world-quant-brain-mcp/brain_api.py` — BRAIN API 客户端**门面**（36 行）；方法体 verbatim 拆至 `brain_mixin_transport/auth/simulation/spcread/correlation.py`，保持 `BrainApiClient` 类名与 `brain_client` 单例 + 旧导入路径（`from brain_api import brain_client/BrainApiClient/load_config/SimulationSettings/...`）不变
- `world-quant-brain-mcp/brain_api_models.py` — 纯数据模型（Pydantic）：`AuthCredentials`/`SimulationSettings`/`SimulationData`
- `world-quant-brain-mcp/brain_config.py` — 配置函数：`_resolve_config_path`/`_load_dotenv_into_environ`/`load_config`
- `world-quant-brain-mcp/mcp_core.py` — MCP 工具注册与分发
- `src/wqb/config.py` — **规范域常量**：区域/算子家族/中性化（数据源 `data/operators_verified.json`）；MCP 包与 `pipeline/`/`tools/gate.py` 共享引用
- `tracking/MANIFEST.json` — 追踪目录全量索引
- `pytest.ini` — 测试配置（验证路由）
- `world-quant-brain-mcp/Makefile` — Docker 部署入口（`make up` / `make down`）

## 3. 变更影响范围指引

- 修改 `world-quant-brain-mcp/` 后需重启 MCP 服务才生效（`.mcp.json` 指向 `main.py`，使用 `world-quant-brain-mcp/.venv`，勿用根环境）。
- 修改 `tracking/<REGION>/config/`（如 `thresholds.json`）影响该区域战役闸门；勿手动编辑 `tracking/mining/` 共享数据湖。
- 修改 `tools/` 中被引用函数前，先用 `rg` 搜索调用点确认影响面。
- 平台交互类改动（回测/提交/配额）先读 `docs/experience/` 经验文档，遵守并发与配额约束，避免 429。
- 凭据位于 `world-quant-brain-mcp/.env`：禁止读取、打印或提交到 git。

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
- 当前根 `tests/` **254 个测试全部通过**（`src/wqb` 包于 2026-08-16 按 `docs/plans/2026-08-02-wqb-src-reconstruction.md` 重建，`tests/conftest.py` 将 `src/` 注入 `sys.path`）；MCP 包 `world-quant-brain-mcp/tests/` 另含 **34 个测试**（需 `.venv`，验证 `brain_api` 拆解不变量与工具注册）。pre-commit 钩子仅跑根 `tests/`，MCP 包测试需单独在 `.venv` 跑。
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
