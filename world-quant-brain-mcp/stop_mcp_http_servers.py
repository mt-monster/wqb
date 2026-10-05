#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
停止 wq-brain-http (8000) 与 wqb-db (8001) 两个 MCP HTTP 常驻服务。

思路（与启动对称，同样不依赖 cmd 的 start / for 循环）：
  1) netstat -ano 找出监听 8000/8001 的 PID → taskkill /F /PID
  2) 兜底清扫：PowerShell CIM 找出命令行命中本仓库服务脚本的 python 进程
     （覆盖"已启动但端口被别的占、没绑上"这类游离进程）
  3) 复检端口是否已释放并打印结果

带 --dry-run：只探测、不杀进程，用于安全验证探测逻辑是否正确。
"""
import json
import os
import subprocess
import sys
import time
import socket

REPO = r"D:\coding\traeCN_project\wqb"
PORTS = [8000, 8001]

# 本仓库两个服务脚本（用于兜底清扫时精确匹配，避免误杀其它仓库的同名脚本）
SERVICE_SCRIPTS = [
    os.path.join(REPO, "world-quant-brain-mcp", "main.py"),
    os.path.join(REPO, "wqb_db_mcp.py"),
]


def listening_pids(port):
    """返回正在监听该端口的 PID 列表。"""
    pids = []
    try:
        # ⚠ 中文 Windows 的 netstat 输出含 GBK 中文，不能用 text=True（会
        # UnicodeDecodeError 且 stdout 变 None）。按字节捕获 + ignore 解码，
        # 只取需要的 ASCII 部分（地址 / LISTENING / PID）。
        res = subprocess.run(["netstat", "-ano"], capture_output=True, timeout=20)
        out = (res.stdout or b"").decode("utf-8", errors="ignore")
    except Exception:
        return pids
    suffix = f":{port}"
    for line in out.splitlines():
        if "LISTENING" not in line:
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        local = parts[1]
        # 兼容 IPv4 (127.0.0.1:8000) 与 IPv6 ([::]:8000)
        if not local.endswith(suffix):
            continue
        try:
            pids.append(int(parts[-1]))
        except ValueError:
            pass
    return pids


def python_processes():
    """返回 [{'ProcessId':int,'CommandLine':str}]，失败返回 []。"""
    ps = (
        "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
        "Select-Object ProcessId,CommandLine | ConvertTo-Json"
    )
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
            capture_output=True, timeout=40,
        )
        raw = (res.stdout or b"").decode("utf-8", errors="ignore").strip()
        if not raw:
            return []
        data = json.loads(raw)
        if isinstance(data, dict):
            data = [data]
        return [
            {"ProcessId": int(d["ProcessId"]), "CommandLine": d.get("CommandLine") or ""}
            for d in data if d.get("ProcessId") is not None
        ]
    except Exception:
        return []


def stray_service_pids():
    """兜底：命令行命中本仓库服务脚本的 python 进程 PID。"""
    pids = []
    repo_l = REPO.lower()
    scripts_l = [s.lower() for s in SERVICE_SCRIPTS]
    for p in python_processes():
        cmd = p["CommandLine"].replace("/", "\\").lower()
        if repo_l in cmd and any(s in cmd for s in scripts_l):
            pids.append(p["ProcessId"])
    return pids


def kill(pid):
    # 不加 text=True：中文 Windows 的 taskkill 输出是 GBK，按 UTF-8 解码会抛
    # UnicodeDecodeError（虽不影响终止结果，但会在 stderr 刷 traceback）。
    subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True)


def port_open(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def main():
    dry = "--dry-run" in sys.argv[1:]
    print(f"停止 MCP HTTP 服务 (8000 / 8001){'  [DRY-RUN 只探测不结束]' if dry else ''}")
    print("-" * 46)

    targets = {}   # pid -> 来源说明
    for port in PORTS:
        for pid in listening_pids(port):
            targets.setdefault(pid, f"监听端口 {port}")
    for pid in stray_service_pids():
        targets.setdefault(pid, "服务脚本进程（兜底清扫）")

    if not targets:
        print("未发现运行中的 MCP 服务进程。")
        return

    for pid, why in targets.items():
        print(f"  发现 PID={pid}  {why}")

    if dry:
        print("\n[DRY-RUN] 以上进程不会被结束。")
        return

    print("")
    killed = []
    for pid in targets:
        kill(pid)
        killed.append(pid)
        print(f"  已结束 PID={pid}")

    time.sleep(1)
    print("\n===== 结果 =====")
    for port in PORTS:
        print(f"  {port}: {'仍在监听（未完全停止）' if port_open(port) else '已停止'}")
    print(f"  共结束 {len(killed)} 个进程。")


if __name__ == "__main__":
    main()
