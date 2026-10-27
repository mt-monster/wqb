#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""wqb_tools 兼容 shim —— 只实现 campaign transport 用到的 `dispatch` 子命令。

为什么需要它
------------
`wqb_campaign/config.py` 里 `WQB_TOOLS = <WQB_SCRIPTS>/wqb_tools.py`，
而真实文件已于 **2026-10-26 10:32 被删除**（`~/wqb-scripts/` 目录还在，脚本没了）。

后果链（实测，EUR OTHER+PV 首波）：
    transport.dispatch → subprocess.run([PY, WQB_TOOLS, "dispatch", ...])
    → 文件不存在 → stdout 空 → 正则取不到 sim_id → 返回 (None, tpl, bi)
    → 收割循环 `if not sim_id: continue` 全跳过
    → 该集 0 alpha、verdict=NO_DATA，**日志里连一行 [harvest] 都不出现**（无异常、无报错）
8 个集 × 45 条表达式 = 300 条，实际提交 **0** 条，40 秒「跑完」。

契约（transport.dispatch 传入）
------------------------------
    dispatch <expr_file> --label L --region R --universe U --decay D
             --neutralization N --truncation T --nan-handling ON|OFF
             --max-trade ON|OFF --simulation-mode FULL --force --allow-probe-repeat

输出：stdout 里出现 `"sim_id": "<id>"`（transport 用正则 `"sim_id": "([^"]+)"` 提取）。

实现：转调仓库 `tools/submit_batch.py`（已实测可用），补齐它需要的 `--path` 与 `--delay`。
delay 取 `--delay` / 环境变量 `WQB_DISPATCH_DELAY`，缺省 1（EUR/KOR/GLB 均为 1）。
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")
SUBMIT = os.path.join(ROOT, "tools", "submit_batch.py")


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] != "dispatch":
        sys.stderr.write("[wqb-tools-shim] 只支持 dispatch 子命令，收到: %r\n" % (argv[:2],))
        return 2

    ap = argparse.ArgumentParser(prog="wqb_tools.py dispatch")
    ap.add_argument("path")
    ap.add_argument("--label", default="")
    ap.add_argument("--region", required=True)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--decay", required=True)
    ap.add_argument("--neutralization", required=True)
    ap.add_argument("--truncation", default="0.08")
    ap.add_argument("--nan-handling", default="OFF")
    ap.add_argument("--max-trade", default="OFF")
    ap.add_argument("--simulation-mode", default="FULL")
    ap.add_argument("--delay", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--allow-probe-repeat", action="store_true")
    a = ap.parse_args(argv[1:])

    delay = a.delay or os.environ.get("WQB_DISPATCH_DELAY") or "1"
    cmd = [PY, SUBMIT,
           "--path", a.path,
           "--region", a.region,
           "--universe", a.universe,
           "--delay", str(delay),
           "--decay", str(a.decay),
           "--neutralization", a.neutralization,
           "--truncation", str(a.truncation),
           "--nan-handling", a.nan_handling,
           "--max-trade", a.max_trade,
           "--simulation-mode", a.simulation_mode]

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=540,
                           cwd=ROOT, env=env)
    except subprocess.TimeoutExpired:
        sys.stderr.write("[wqb-tools-shim] submit_batch 超时（540s）: %s\n" % a.path)
        print(json.dumps({"error": "timeout"}))
        return 1

    out = (p.stdout or "") + "\n" + (p.stderr or "")
    m = re.search(r"/simulations/([A-Za-z0-9]+)", out) or \
        re.search(r'"sim_id"\s*:\s*"([^"]+)"', out)
    if not m:
        sys.stderr.write("[wqb-tools-shim] dispatch 失败 rc=%s path=%s\n%s\n"
                         % (p.returncode, os.path.basename(a.path), out[-1500:]))
        print(json.dumps({"error": "dispatch_failed", "rc": p.returncode}, ensure_ascii=False))
        return 1

    print(json.dumps({"sim_id": m.group(1)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
