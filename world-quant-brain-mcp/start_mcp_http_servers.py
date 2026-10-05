#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动 wq-brain-http (8000) 与 wqb-db (8001) 两个 MCP HTTP 常驻服务。

为什么用 Python 而不是 cmd 的 start：
  - cmd 的 `start` 在本机双击环境不可靠（子进程起不来、且无日志）。
  - 本脚本用 subprocess.Popen(creationflags=DETACHED_PROCESS|CREATE_NO_WINDOW)
    直接拉起服务进程，完全脱离父进程/控制台，关闭本窗口服务继续运行。
  - 每个服务的 stdout/stderr 重定向到 logs/ 下的日志，启动失败可查。
"""
import os
import sys
import time
import socket
import subprocess

MCP_DIR = r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp"
REPO    = r"D:\coding\traeCN_project\wqb"
LOGDIR  = os.path.join(MCP_DIR, "logs")
os.makedirs(LOGDIR, exist_ok=True)

SHARED_ENV = {
    "MCP_TRANSPORT": "streamable-http",
    "MCP_HOST": "127.0.0.1",
    "WQB_ALLOW_ALPHA_SUBMIT": "1",
    "WQB_ASI_UNIVERSE_FIX": "20260916",
    "WQ_TOOLKIT_DIR": os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts"),
    "WQ_VALIDATOR_DIR": os.path.join(REPO, "Claude", "skills", "alpha-expression-verifier", "scripts"),
}

SERVICES = [
    {
        "name": "wq-brain-http", "port": 8000,
        "python": os.path.join(MCP_DIR, ".venv", "Scripts", "python.exe"),
        "script": os.path.join(MCP_DIR, "main.py"),
        "cwd": MCP_DIR,
        "log": os.path.join(LOGDIR, "brain_http_8000.log"),
    },
    {
        "name": "wqb-db", "port": 8001,
        "python": os.path.join(REPO, ".venv", "Scripts", "python.exe"),
        "script": os.path.join(REPO, "wqb_db_mcp.py"),
        "cwd": REPO,
        "log": os.path.join(LOGDIR, "wqb_db_8001.log"),
    },
]

CREATE_NO_WINDOW = 0x08000000   # 不创建控制台窗口
DETACHED_PROCESS = 0x00000008   # 脱离父进程（父退出后服务继续运行）


def main():
    auto = "auto" in sys.argv[1:]

    print("正在启动 MCP HTTP 服务 ...")
    launched = []
    for s in SERVICES:
        env = dict(os.environ)
        env.update(SHARED_ENV)
        env["MCP_PORT"] = str(s["port"])
        try:
            fout = open(s["log"], "w", buffering=1, encoding="utf-8", errors="replace")
            p = subprocess.Popen(
                [s["python"], s["script"]],
                env=env, cwd=s["cwd"], stdout=fout, stderr=subprocess.STDOUT,
                creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS,
                close_fds=True,
            )
            launched.append((s, p.pid))
            print(f"  launched {s['name']} (pid={p.pid}) -> {s['log']}")
        except Exception as e:  # noqa: BLE001
            print(f"  FAILED {s['name']}: {e}")

    print("等待服务绑定端口（约 7 秒）...")
    time.sleep(7)

    print("\n===== 自检（端口监听）=====")
    for s in SERVICES:
        ok = False
        try:
            with socket.create_connection(("127.0.0.1", s["port"]), timeout=2):
                ok = True
        except OSError:
            ok = False
        print(f"  {s['name']} ({s['port']}): {'LISTENING' if ok else 'NOT listening / 启动失败'}")
    print(f"\n日志目录：{LOGDIR}")
    print("若两行均为 LISTENING，服务已在后台常驻（与当前窗口无关）。")
    print("关闭服务：结束对应 python 进程，或运行 stop_mcp_http_servers.bat。")

    if not auto:
        try:
            input("按回车关闭本窗口（服务继续运行）...")
        except EOFError:
            pass


if __name__ == "__main__":
    main()
