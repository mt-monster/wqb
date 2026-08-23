# -*- coding: utf-8 -*-
"""batch_status.py - 回测批次/子任务状态查询与轮询（替代 tracking/_scratch/check_batch*.py 族）。

输入一个或多个仿真 id（multisim 或单条 simulation），输出：
  - multisim：children 列表 + 每个 child 的 status/alpha_id/error（对齐
    lookINTO_SimError_message 的字段语义）
  - 单条 simulation：status/alpha_id/error + 关键指标（sharpe/fitness/turnover，若可得）

--watch 模式下按 interval 轮询直到全部 terminal 或超时（默认 60min），
适合五槽填槽模式下盯一批在飞任务。

用法:
  python tools/batch_status.py --ids 3D0QTR5Dv4NjbjDYx1qyD6b
  python tools/batch_status.py --ids A1b2c3 B4d5e6 --watch --interval 20 --max-waits 60
  python tools/batch_status.py --ids X1 --json tracking/KOR/results/batch_X1.json

退出码: 0=全部 terminal 且无 error, 1=存在 error/未完成
运行环境: 使用 MCP venv（`$WQ_PY` 或 world-quant-brain-mcp/.venv），依赖 brain_api。
"""
import argparse
import asyncio
import json
import os
import sys
import time


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe"]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _bootstrap():
    """路径引导：优先 MCP venv 解释器重启，否则把工作区 MCP 包加入 sys.path。"""
    py = _mcp_venv_python()
    if py and os.path.abspath(py) != os.path.abspath(sys.executable):
        os.execv(py, [py] + sys.argv)
    mcp = os.environ.get("WQ_MCP_DIR", r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp")
    sys.path.insert(0, mcp)
    from brain_api import BrainApiClient  # noqa: F401
    return mcp


TERMINAL = {"DONE", "ERROR", "CANCELLED", "FAILED"}


def _shape_url(base, loc):
    if loc.startswith("http"):
        return loc
    if loc.startswith("/"):
        return base + loc
    return f"{base}/simulations/{loc}"


async def fetch_one(brain, loc_full):
    """GET 单条 simulation location → {status, alpha, error, metrics}。"""
    resp = await brain._request("GET", loc_full)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "status_code": resp.status_code}
    data = resp.json() if resp.text else {}
    err = brain._simulation_error_message(data)
    if not data.get("alpha") and err == "Unknown error":
        err = ""
    is_ = data.get("is") or {}
    m = is_.get("metrics") or {}
    return {
        "status": data.get("status"),
        "alpha": data.get("alpha"),
        "error": err,
        "sharpe": is_.get("sharpe") or m.get("sharpe"),
        "fitness": is_.get("fitness") or m.get("fitness"),
        "turnover": is_.get("turnover") or m.get("turnover"),
    }


async def fetch_batch(brain, batch_id):
    """fetch one batch (multisim or single) → summary dict。"""
    base = brain.base_url
    loc = _shape_url(base, batch_id)
    resp = await brain._request("GET", loc)
    if resp.status_code != 200:
        return {"batch_id": batch_id, "error": f"HTTP {resp.status_code}"}
    data = resp.json() if resp.text else {}
    children = data.get("children") or []
    if not children:
        return {"batch_id": batch_id, **await fetch_one(brain, loc)}
    out_children = []
    for c in children:
        cloc = _shape_url(base, c if isinstance(c, str) else c.get("location"))
        child = await fetch_one(brain, cloc)
        child["location"] = cloc.rsplit("/", 1)[-1]
        out_children.append(child)
    term = [c for c in out_children if (c.get("status") or "").upper() in TERMINAL]
    errs = [c for c in out_children if c.get("error") and c["error"] != "HTTP 404"]
    return {
        "batch_id": batch_id,
        "kind": "multisim",
        "child_count": len(out_children),
        "terminal": len(term),
        "errors": len(errs),
        "all_terminal": len(term) == len(out_children) if out_children else False,
        "children": out_children,
    }


def _print_summary(b):
    if b.get("kind") == "multisim":
        print(f"\n=== {b['batch_id']} (multisim) {b['terminal']}/{b['child_count']} terminal ===")
        for c in b["children"]:
            mark = "✓" if (c.get("status") or "").upper() in TERMINAL else "…"
            print(f"  {mark} {c['location']}  status={c.get('status')}  alpha={c.get('alpha')} "
                  f"sh={c.get('sharpe')} fit={c.get('fitness')}"
                  + (f"  ERR: {c.get('error')[:120]}" if c.get("error") else ""))
    else:
        print(f"\n=== {b['batch_id']} status={b.get('status')} alpha={b.get('alpha')} "
              f"sh={b.get('sharpe')} fit={b.get('fitness')}"
              + (f"  ERR: {b.get('error')[:160]}" if b.get('error') else "") + " ===")


async def run_once(brain, ids):
    batches = [await fetch_batch(brain, i) for i in ids]
    for b in batches:
        _print_summary(b)
    bad = [b for b in batches if b.get("error") or (b.get("kind") == "multisim" and not b.get("all_terminal"))]
    return batches, not bad


async def main():
    ap = argparse.ArgumentParser(description="回测批次/子任务状态查询与轮询")
    ap.add_argument("--ids", nargs="+", required=True, help="simulation/multisim id（可多个）")
    ap.add_argument("--watch", action="store_true", help="轮询直到全部 terminal 或超时")
    ap.add_argument("--interval", type=float, default=20.0, help="轮询间隔秒（默认 20）")
    ap.add_argument("--max-waits", type=int, default=180, help="最大轮询次数（默认 180≈60min）")
    ap.add_argument("--json", dest="json_out", help="结果落盘 JSON 路径")
    a = ap.parse_args()

    _bootstrap()
    from brain_api import BrainApiClient  # noqa: F402
    brain = BrainApiClient()

    ids = [i.replace(f"{brain.base_url}/simulations/", "") for i in a.ids]
    all_ok = True
    final = None
    t0 = time.time()
    for round_no in range(1 if not a.watch else a.max_waits):
        final, all_ok = await run_once(brain, ids)
        if not a.watch or all_ok:
            break
        print(f"\n[watch] round {round_no}/{a.max_waits} 耗时 {time.time() - t0:.0f}s，"
              f"{a.interval:.0f}s 后再查（Ctrl+C 退出）")
        await asyncio.sleep(a.interval)

    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump(final, open(a.json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        print(f"\n[out] {a.json_out}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    asyncio.run(main())