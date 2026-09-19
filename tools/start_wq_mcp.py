# -*- coding: utf-8 -*-
"""start_wq_mcp.py — 启动/确保 wq-brain-http MCP 服务在配置端口可用。

背景（2026-09-13 实测）：论坛 MCP 工具「不可用」的根因不是工具缺失，而是
**服务端进程没起 + 端口不匹配**：
  - 服务端 `mcp_core.py` 默认 `MCP_PORT=8000`；
  - `~/.workbuddy/mcp.json` 里 `wq-brain-http` 指向 `http://localhost:8876/mcp`。
两者不一致时，即便进程起来了宿主仍连不上 → 表现为"论坛工具找不到"。

用法：
    python tools/start_wq_mcp.py            # 已在监听则跳过；否则后台启动
    python tools/start_wq_mcp.py --check    # 只报告状态（exit 0=在跑 / 1=未跑）
    python tools/start_wq_mcp.py --wait 30  # 启动后最多等 N 秒确认监听

注意（踩过的坑）：**不要用 `| head -N` 之类的管道承接 stdout** —— 管道提前关闭
会让 Playwright/子进程写出时报 `[Errno 22] Invalid argument`（表现为论坛搜索莫名失败）。
本脚本一律把输出重定向到日志文件。
"""
from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVER_DIR = REPO_ROOT / "world-quant-brain-mcp"
VENV_PY = SERVER_DIR / ".venv" / "Scripts" / "python.exe"
LOG_PATH = SERVER_DIR / "logs_mcp_8876.log"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8876  # 与 ~/.workbuddy/mcp.json 的 wq-brain-http url 保持一致


def port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def start(host: str, port: int) -> int | None:
    py = VENV_PY if VENV_PY.exists() else Path(sys.executable)
    if not (SERVER_DIR / "main.py").exists():
        print(f"[start_wq_mcp] 未找到 {SERVER_DIR / 'main.py'}", file=sys.stderr)
        return None
    env = dict(os.environ)
    env.update({"MCP_HOST": host, "MCP_PORT": str(port),
                "MCP_TRANSPORT": "streamable-http", "PYTHONUNBUFFERED": "1"})
    # 关键：stdout/stderr 落文件，绝不接管道（见模块 docstring）
    fh = open(LOG_PATH, "ab", buffering=0)
    proc = subprocess.Popen(
        [str(py), "main.py"], cwd=str(SERVER_DIR), env=env,
        stdout=fh, stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
    )
    print(f"[start_wq_mcp] 已启动 pid={proc.pid} -> http://{host}:{port}/mcp (log: {LOG_PATH})")
    return proc.pid


def main() -> int:
    ap = argparse.ArgumentParser(description="确保 wq-brain-http MCP 服务在运行")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--check", action="store_true", help="只报告状态，不启动")
    ap.add_argument("--wait", type=int, default=20, help="启动后最多等待监听的秒数")
    a = ap.parse_args()

    if port_open(a.host, a.port):
        print(f"[start_wq_mcp] 已在运行: http://{a.host}:{a.port}/mcp")
        return 0
    if a.check:
        print(f"[start_wq_mcp] 未运行: 端口 {a.port} 无监听")
        return 1

    start(a.host, a.port)
    for _ in range(max(1, a.wait)):
        time.sleep(1)
        if port_open(a.host, a.port):
            print(f"[start_wq_mcp] ✅ 就绪: http://{a.host}:{a.port}/mcp")
            return 0
    print(f"[start_wq_mcp] ⚠️ 启动后 {a.wait}s 仍未监听，检查日志: {LOG_PATH}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
