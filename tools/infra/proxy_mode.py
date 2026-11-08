#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""proxy_mode - 代理一键切换（终端入口）。

场景（2026-11-07）
=================
代理一关，`HTTP(S)_PROXY` 仍指向死端口 127.0.0.1:7897：
  - 平台 API 无碍（`main.py` 已把 worldquantbrain.com 加进 NO_PROXY，实测直连 401 可达）；
  - 论坛通道会打空（`forum_functions` 回落读 HTTPS_PROXY）。
本命令把「开/关代理」收敛成一个动作：写持久化配置 + 让常驻 MCP 服务**热切换**，
不用手工改环境变量、不用重启服务。

用法
====
    python tools/infra/proxy_mode.py status            # 现状体检（配置+进程env+端口+平台/论坛直连）
    python tools/infra/proxy_mode.py status --no-probe # 只看配置，不联网
    python tools/infra/proxy_mode.py off               # 关代理：论坛直连
    python tools/infra/proxy_mode.py on                # 开代理：论坛走 127.0.0.1:7897
    python tools/infra/proxy_mode.py on --url http://127.0.0.1:7890
    python tools/infra/proxy_mode.py auto              # 不干预（保持进程继承的环境）

    --no-hot   只写配置，不调常驻服务（下次启动才生效）
    --restart  切完后强重启 MCP 服务（改过代理软件端口、或服务假死时用）
    --json     机器可读输出

两个通道分开管
==============
**平台 API 永远直连**（NO_PROXY，实测更稳）；本开关只控制论坛/浏览器通道。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MCP_DIR = REPO / "world-quant-brain-mcp"
VENV_PY = MCP_DIR / ".venv" / "Scripts" / "python.exe"
CALLER = REPO / "tools" / "mcp_http_caller.py"
RESTART_SCRIPT = Path(os.path.expanduser("~")) / "mcp-servers" / "start_mcp_http_servers.py"


def _ensure_venv() -> None:
    """网络/requests 依赖在 MCP venv 里；用系统 python 跑会自动换过去。

    ⚠ 不用 os.execv：Windows 上 execv 是「spawn 后立刻退出」的模拟实现，
    父进程一退出，调用方的管道就被关掉 —— 实测表现为「exit 0 且零输出」。
    改成 subprocess.run 等子进程结束再透传退出码。
    """
    if os.name != "nt" or not VENV_PY.is_file():
        return
    try:
        if Path(sys.prefix).resolve() == VENV_PY.parent.parent.resolve():
            return
    except OSError:
        pass
    proc = subprocess.run([str(VENV_PY), str(Path(__file__).resolve())] + sys.argv[1:])
    raise SystemExit(proc.returncode)


_ensure_venv()
sys.path.insert(0, str(MCP_DIR))

import proxy_mode as pm  # noqa: E402  (MCP 包内核心模块，单一实现)


def _call_mcp(tool: str, args: dict, timeout: int = 120) -> dict:
    """调常驻服务的工具；服务没起/调用失败时返回 {error}，由调用方回落。"""
    if not CALLER.is_file():
        return {"error": f"找不到 {CALLER}"}
    cmd = [sys.executable, str(CALLER), tool, json.dumps(args, ensure_ascii=False),
           "--service", "wq-brain-http", "--timeout", str(timeout)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout + 15)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}
    out = (proc.stdout or "").strip()
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return {"error": (out or proc.stderr or "空输出")[:400]}


def _restart_services() -> str:
    if not RESTART_SCRIPT.is_file():
        return f"跳过：找不到 {RESTART_SCRIPT}"
    try:
        proc = subprocess.run([sys.executable, str(RESTART_SCRIPT), "auto", "force"],
                              capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=180)
        tail = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()][-4:]
        return "已重启：" + " | ".join(tail)
    except Exception as exc:  # noqa: BLE001
        return f"重启失败：{type(exc).__name__}: {exc}"


def _render_status(st: dict) -> str:
    cfg = st.get("config", {})
    env = st.get("process_env", {})
    lines = [
        f"模式        : {cfg.get('mode')}   (配置 {cfg.get('source')})",
        f"代理地址    : {cfg.get('proxy_url')}",
        f"进程代理变量: {env if env else '（空）'}",
        f"论坛直连开关: {st.get('forum_bypass')}   平台 NO_PROXY 绕行: {st.get('platform_bypass')}",
    ]
    port = st.get("proxy_port")
    if port:
        lines.append(f"代理端口    : {port['host']}:{port['port']} "
                     f"{'LISTENING' if port['listening'] else '无监听（代理已关）'}")
    for key, label in (("platform_direct", "平台直连"), ("forum_direct", "论坛直连")):
        res = st.get(key)
        if not res:
            continue
        if res.get("error"):
            lines.append(f"{label}    : ERR {res['error']}")
        else:
            cf = f" cf-mitigated={res['cf_mitigated']}" if res.get("cf_mitigated") else ""
            lines.append(f"{label}    : HTTP {res['status']}{cf}")
    if st.get("hint"):
        lines.append(f"结论        : {st['hint']}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="代理一键切换（论坛通道 + 进程 env；平台永远直连）")
    ap.add_argument("action", nargs="?", default="status",
                    choices=["status", "on", "off", "auto"])
    ap.add_argument("--url", default=None, help="代理地址（mode=on 时用；缺省沿用配置/环境变量）")
    ap.add_argument("--no-probe", action="store_true", help="status 时不联网")
    ap.add_argument("--no-hot", action="store_true", help="只写配置，不调常驻服务热切换")
    ap.add_argument("--restart", action="store_true", help="切完后强重启 MCP 服务")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args(argv)

    if args.action == "status":
        hot = _call_mcp("get_proxy_mode", {"probe": not args.no_probe})
        if "error" in hot:
            st = pm.status(do_probe=not args.no_probe)
            st["_source"] = f"本地（常驻服务不可达：{hot['error'][:120]}）"
        else:
            st = hot
            st["_source"] = "常驻服务"
        if args.json:
            print(json.dumps(st, ensure_ascii=False, indent=2))
        else:
            print(_render_status(st))
            print(f"数据来源    : {st.get('_source')}")
        return 0

    # 先落盘：即便服务没起，下次启动也会按这个模式走
    try:
        cfg = pm.write_config(args.action, args.url)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    report = {"config": cfg, "hot": None, "restart": None}
    if not args.no_hot:
        payload = {"mode": args.action, "verify": False}
        if args.url:
            payload["proxy_url"] = args.url
        report["hot"] = _call_mcp("set_proxy_mode", payload)
    if args.restart:
        report["restart"] = _restart_services()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    mode_cn = {"on": "论坛走代理", "off": "论坛直连", "auto": "不干预"}[args.action]
    print(f"✅ 已切到 {args.action}（{mode_cn}） 配置: {cfg['source']}")
    if report["hot"] is not None:
        hot = report["hot"]
        if "error" in hot:
            print(f"⚠️ 常驻服务热切换失败：{hot['error'][:200]}")
            print("   （配置已落盘，服务下次启动会沿用；要立刻生效可加 --restart）")
        else:
            print("   常驻服务已热切换（无需重启）")
    if report["restart"]:
        print(f"   {report['restart']}")
    print("\n看现状: python tools/infra/proxy_mode.py status")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
