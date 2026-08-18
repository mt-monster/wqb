# AGENTS.md — wqb（WorldQuant BRAIN Alpha 挖掘工作区）

## 1. 项目概述与模块职责

本工作区用于 WorldQuant BRAIN 平台的 alpha 挖掘、回测、评审与提交，Python 脚本驱动，无统一应用框架；MCP 服务是本项目与编码 Agent 的主要接口。

| 目录 | 职责 | 变更注意 |
|---|---|---|
| `world-quant-brain-mcp/` | MCP 服务（`wqb-mcp`）：BRAIN API 客户端、回测/提交/论坛工具 | 运行中服务，改动需回归验证 |
| `tracking/` | 区域战役追踪（KOR/USA/EUR/IND/GLB/DEU…）：candidates/results/reviews/scripts | `tracking/mining/` 为共享数据湖，勿改动/移动；`MANIFEST.json` 为全量索引 |
| `mining/` | 挖掘脚本与归档 | 改动影响战役 pipeline |
| `tools/` | 工具链（字段解析、质量检查、同步等） | 被多区域脚本引用，改动前先查调用点 |
| `reports/` | 报告产物 | — |
| `data/` `data_ref/` | 事件数据与参考字段 | 只读数据 |
| `src/wqb/` | 核心包：config/expression/research/search/memory（测试契约见 `tests/unit/`） | 行为变更须保持 223 个单测全绿 |
| `tests/` | pytest 单元测试 | 见 §4 |
| `docs/` | 计划、参考、经验文档 | 行为变更需同步相关文档 |

## 2. 核心入口文件

- `world-quant-brain-mcp/main.py` — MCP 服务入口（`.mcp.json` 注册为 `wqb-mcp`，stdio 启动）
- `world-quant-brain-mcp/brain_api.py` — BRAIN API 客户端核心
- `world-quant-brain-mcp/mcp_core.py` — MCP 工具注册与分发
- `src/wqb/config.py` — 区域配置/算子家族/幽灵算子黑名单（数据源 `data/operators_verified.json`）
- `tracking/MANIFEST.json` — 追踪目录全量索引
- `pytest.ini` — 测试配置（验证路由）
- `world-quant-brain-mcp/Makefile` — Docker 部署入口（`make up` / `make down`）

## 3. 变更影响范围指引

- 修改 `world-quant-brain-mcp/` 后需重启 MCP 服务才生效（`.mcp.json` 指向 `main.py`，使用 `world-quant-brain-mcp/.venv`，勿用根环境）。
- 修改 `tracking/<REGION>/config/`（如 `thresholds.json`）影响该区域战役闸门；勿手动编辑 `tracking/mining/` 共享数据湖。
- 修改 `tools/` 中被引用函数前，先用 `rg` 搜索调用点确认影响面。
- 平台交互类改动（回测/提交/配额）先读 `docs/experience/` 经验文档，遵守并发与配额约束，避免 429。
- 凭据位于 `world-quant-brain-mcp/.env`：禁止读取、打印或提交到 git。

## 4. 测试与验证路径

编辑后必须运行验证：

```bash
python -m pytest tests/ -x
```

- 结果自动写入 `logs/test-results.xml`（JUnit XML，可追溯）。
- 当前 223 个测试全部可运行且通过（13 个测试文件全量收集；`src/wqb` 包已于 2026-08-16 按 `docs/plans/2026-08-02-wqb-src-reconstruction.md` 重建完成，`tests/conftest.py` 将 `src/` 注入 `sys.path`）。
- 依赖声明于根 `requirements.txt` 与 `world-quant-brain-mcp/requirements.txt`，新增依赖需同步相应文件。

### pre-commit 钩子（推荐激活）

提交前自动运行上述 pytest 验证路由，测试失败即阻止提交：

```bash
git config core.hooksPath tools/git-hooks
```

- 钩子脚本：`tools/git-hooks/pre-commit`（调用 `python -m pytest tests/ -x`）。
- 紧急跳过（仅临时）：`git commit --no-verify`。
