# 🚀 快速开始指南

## 启动MCP服务

```bash
cd world-quant-brain-mcp
python3 main.py
```

✅ 服务启动后，监听地址: `http://localhost:8000/mcp`

> ⚠️ **端口与启动方式（2026-10-05 更新）**：两个 server 均为 HTTP 常驻 ——
> `wq-brain-http` = `127.0.0.1:8000/mcp`，`wqb-db` = `127.0.0.1:8001/mcp`（端口不可相同，否则第二个起不来）。
> **推荐统一走启动器**：`python tools/start_wq_mcp.py --all`（端口自动读仓库根 `.mcp.json`，已在监听则跳过，
> 输出落 `logs/<服务名>.log`）。历史坑（2026-09-13）：服务端默认 8000而宿主 `~/.workbuddy/mcp.json`
> 曾指 8876 → 表现为“论坛工具找不到”；现在两边都统一 8000。
> 手工启动请务必：`MCP_PORT=8000 MCP_TRANSPORT=streamable-http .venv/Scripts/python.exe main.py`，
> 且**不要用 `| head -N` 管道承接 stdout**（管道提前关闭会让 Playwright 报 `[Errno 22]`）。
> ⚠ 客户端侧的 `type` 取值不通用（Claude / Qoder / WorkBuddy 认 `http`，Cline 认 `streamableHttp`），
> 且部分客户端读自己的用户级配置而非 `.mcp.json` —— 完整对照表见仓库根 AGENTS.md §3.5。

## 在其他客户端注册

服务器名**只能是 `wq-brain-http` / `wqb-db`**（所有 skill 的工具前缀是 `mcp__wq-brain-http__*`，改名即全线失配）：

```bash
claude mcp add --transport http wq-brain-http http://localhost:8000/mcp --scope project
```

## 验证安装

```bash
claude mcp list                 # 应看到：wq-brain-http │ http://localhost:8000/mcp │ ✓
python tools/mcp_ping.py        # 仓库根：只读探针，走 HTTP 客户端，不起进程
```

## 依赖安装

```bash
pip install -r requirements.txt
```

## 环境配置

编辑 `.env` 文件，设置:
```
CREDENTIALS_EMAIL="your_email@example.com"
CREDENTIALS_PASSWORD="your_password"
```

---

**详细文档**: 请查看 MCP_TEST_REPORT.md
