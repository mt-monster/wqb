# 🚀 快速开始指南

## 启动MCP服务

```bash
cd world-quant-brain-mcp
python3 main.py
```

✅ 服务启动后，监听地址: `http://localhost:8000/mcp`

> ⚠️ **端口陷阱（2026-09-13 实测）**：服务端默认 `MCP_PORT=8000`，但宿主
> `~/.workbuddy/mcp.json` 的 `wq-brain-http` 指向 **8876**。直接用默认参数启动会表现为
> "论坛工具找不到"。**推荐统一走启动器**：`python tools/start_wq_mcp.py`
> （自动带 `MCP_PORT=8876`，已在监听则跳过，输出落 `logs_mcp_8876.log`）。
> 手工启动请务必：`MCP_PORT=8876 MCP_TRANSPORT=streamable-http .venv/Scripts/python.exe main.py`，
> 且**不要用 `| head -N` 管道承接 stdout**（管道提前关闭会让 Playwright 报 `[Errno 22]`）。

## 在Claude Code中注册

```bash
claude mcp add --transport http brain http://localhost:8000/mcp --scope project
```

## 验证安装

```bash
claude mcp list
```

应看到输出: `brain  │ http://localhost:8000/mcp │ ✓`

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
