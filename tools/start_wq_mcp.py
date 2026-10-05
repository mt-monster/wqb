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
import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVER_DIR = REPO_ROOT / "world-quant-brain-mcp"
VENV_PY = SERVER_DIR / ".venv" / "Scripts" / "python.exe"
# 日志归日志目录（包根不堆运行产物，AGENTS.md §8.13）；MCP/logs/ 已整目录 gitignore
LOG_DIR = REPO_ROOT / "logs"   # 统一放 logs/，与服务日志同处
LOG_PATH = LOG_DIR / "wq-brain-http.log"

DEFAULT_HOST = "127.0.0.1"
#: 兜底端口。**权威值以 `.mcp.json` 的 url 为准**（本文件会读它），
#: 这两个常量只在 .mcp.json 缺失/无 url 时才用。
#: 历史坑（见模块 docstring）：曾硬编码 8876 而 .mcp.json 指8000 → 起得来连不上。
DEFAULT_PORT = 8000          # wq-brain-http
DEFAULT_DB_PORT = 8001       # wqb-db（两者不可相同，否则第二个起不来）
#: 各server 的启动目标：name → (入口脚本相对仓库根的路径, 用哪个解释器)
SERVERS = {
    "wq-brain-http": ("world-quant-brain-mcp/main.py", "world-quant-brain-mcp/.venv"),
    "wqb-db": ("wqb_db_mcp.py", ".venv"),
}


def urls_from_mcp_json():
    """从根 `.mcp.json` 读 `{name: (host, port)}`（HTTP 模式）。

    读不到就返回空dict —— 调用方回落到DEFAULT_PORT / DEFAULT_DB_PORT。
    不抛错：`.mcp.json` 语法错等问题应由 `tools/mcp_ping.py` 报错，这里只做尽力解析。
    """
    cfg_path = REPO_ROOT / ".mcp.json"
    if not cfg_path.is_file():
        return {}
    try:
        servers = json.loads(cfg_path.read_text(encoding="utf-8")).get("mcpServers", {})
        out = {}
        for name, spec in servers.items():
            url = (spec or {}).get("url") or ""
            m = re.match(r"https?://([^:/]+):(\d+)", url)
            if m:
                out[name] = (m.group(1), int(m.group(2)))
        return out
    except Exception:  # noqa: BLE001 — 尽力解析，失败不阻塞启动
        return {}


def port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def start(host: str, port: int, service: str = "wq-brain-http") -> int | None:
    """启动指定 server 的 HTTP 服务（已在监听则由调用方跳过）。"""
    rel_script, rel_venv = SERVERS.get(service, SERVERS["wq-brain-http"])
    script = REPO_ROOT / rel_script
    py = REPO_ROOT / rel_venv / "Scripts" / "python.exe"
    if not script.exists():
        print(f"[start_wq_mcp] 未找到 {script}", file=sys.stderr)
        return None
    if not py.exists():
        py = Path(sys.executable)
    log_path = LOG_PATH.parent / f"{service}.log"
    env = dict(os.environ)
    env.update({"MCP_HOST": host, "MCP_PORT": str(port),
                "MCP_TRANSPORT": "streamable-http", "PYTHONUNBUFFERED": "1"})
    # 关键：stdout/stderr 落文件，绝不接管道（见模块 docstring）
    log_path.parent.mkdir(parents=True, exist_ok=True)   # 干净克隆后 logs/ 尚未创建
    fh = open(log_path, "ab", buffering=0)
    proc = subprocess.Popen(
        [str(py), str(script)], cwd=str(script.parent), env=env,
        stdout=fh, stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0,
    )
    print(f"[start_wq_mcp] {service} 已启动 pid={proc.pid} -> "
          f"http://{host}:{port}/mcp (log: {log_path})")
    return proc.pid


def main() -> int:
    ap = argparse.ArgumentParser(description="确保 wq-brain-http MCP 服务在运行")
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=None,
                    help="显式指定端口（缺省从 .mcp.json 的 url 读；两者都没有才用内置默认）")
    ap.add_argument("--check", action="store_true", help="只报告状态，不启动")
    ap.add_argument("--wait", type=int, default=20, help="启动后最多等待监听的秒数")
    ap.add_argument("--service", default="wq-brain-http",
                    choices=sorted(SERVERS), help="要确保运行的 server")
    ap.add_argument("--all", action="store_true",
                    help="确保 .mcp.json 里的**全部** server 都在跑（端口自动从 .mcp.json 读）")
    a = ap.parse_args()

    # 端口以 .mcp.json 为准（HTTP 模式下客户端按 url 连，端口错就「起得来连不上」）
    urls = urls_from_mcp_json()

    def _resolve(name):
        host, port = urls.get(name, (a.host, DEFAULT_PORT if name == "wq-brain-http" else DEFAULT_DB_PORT))
        # 命令行显式给了 --port 才覆盖
        return (host, a.port) if a.port else (host, port)

    targets = sorted(SERVERS) if a.all else [a.service]
    failed = []
    for name in targets:
        host, port = _resolve(name)
        if port_open(host, port):
            print(f"[start_wq_mcp] {name} 已在运行: http://{host}:{port}/mcp")
            continue
        if a.check:
            print(f"[start_wq_mcp] {name} 未运行: {host}:{port} 无监听")
            failed.append(name)
            continue
        start(host, port, service=name)
        ok = False
        for _ in range(max(1, a.wait)):
            time.sleep(1)
            if port_open(host, port):
                print(f"[start_wq_mcp] ✅ {name} 就绪: http://{host}:{port}/mcp")
                ok = True
                break
        if not ok:
            print(f"[start_wq_mcp] ⚠️ {name} 启动后 {a.wait}s 仍未监听，"
                  f"检查日志: {LOG_DIR / (name + '.log')}", file=sys.stderr)
            failed.append(name)

    if a.check:
        return 1 if failed else 0
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
