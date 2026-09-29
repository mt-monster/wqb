# -*- coding: utf-8 -*-
"""batch_status.py - 回测批次/子任务状态查询与轮询（替代 tracking/_scratch/check_batch*.py 族）。

输入一个或多个仿真 id（multisim 或单条 simulation），输出：
  - multisim：children 列表 + 每个 child 的 status/alpha_id/error（对齐
    lookINTO_SimError_message 的字段语义）
  - 单条 simulation：status/alpha_id/error + 关键指标（sharpe/fitness/turnover，若可得）

--watch 模式下按 interval 轮询直到全部 terminal 或超时（默认 60min），
适合七槽填槽模式下盯一批在飞任务。

用法:
  python tools/batch_status.py --ids 3D0QTR5Dv4NjbjDYx1qyD6b
  python tools/batch_status.py --ids A1b2c3 B4d5e6 --watch --interval 20 --max-waits 60
  python tools/batch_status.py --ids X1 --json tracking/KOR/results/batch_X1.json

退出码: 0=全部 terminal 且无 error, 1=存在 error/未完成
运行环境: 使用 MCP venv（`$WQ_PY` 或 world-quant-brain-mcp/.venv），依赖 brain_api。
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import argparse
import asyncio
import json
import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器/MCP 目录解析（tools/_pyenv.py）


def _mcp_venv_python():
    return _pyenv.venv_python()


def _bootstrap():
    """路径引导：非 MCP venv 解释器时 re-exec 到 venv（Windows 下等待子进程并透传退出码，
    避免 wave31 false-complete）；把 MCP 目录与 src 加入 sys.path（跨平台）。"""
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    from brain_api import BrainApiClient  # noqa: F401
    return str(_pyenv.mcp_dir())


# 2026-09-21 根治：平台 multisim 子任务终态是 COMPLETE（poller.py 早已如此），本工具原集合
# 漏了它 → COMPLETE 子任务永远算"未终态"，--watch 永不退出、all_ok 永假；且 COMPLETE 被当 error 计数。
TERMINAL = {"COMPLETE", "DONE", "WARNING", "ERROR", "CANCELLED", "FAILED", "FAIL"}  # WARNING=已完成但带告警（单位不兼容等），亦为终态；FAIL=平台子模拟裸状态字面量（2026-09-21 ASI psd 批实证：父 ERROR、子全 FAIL，旧集合永远 0/8 terminal）
OK_STATUSES = {"COMPLETE", "DONE"}


def _shape_url(base, loc):
    if loc.startswith("http"):
        return loc
    if loc.startswith("/"):
        return base + loc
    return f"{base}/simulations/{loc}"


async def _get_authed(brain, url):
    """GET，带一次 401 自动重认证（2026-09-21 根治：本工具直接用 brain._request，
    新进程无 JWT 时每条都 HTTP 401，--watch 永远等不到 terminal）。"""
    ensure = getattr(brain, "ensure_authenticated", None)
    if callable(ensure):
        try:
            await ensure()
        except Exception:
            pass
    resp = await brain._request("GET", url)
    if getattr(resp, "status_code", None) == 401 and callable(ensure):
        try:
            brain._auth_validated_until = 0.0
        except Exception:
            pass
        await ensure()
        resp = await brain._request("GET", url)
    return resp


async def fetch_one(brain, loc_full):
    """GET 单条 simulation location → {status, alpha, error, metrics}。"""
    resp = await _get_authed(brain, loc_full)
    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}", "status_code": resp.status_code}
    data = resp.json() if resp.text else {}
    err = brain._simulation_error_message(data)
    if not data.get("alpha") and err == "Unknown error":
        err = ""
    if (data.get("status") or "").upper() in OK_STATUSES and err.strip().upper() in OK_STATUSES:
        err = ""  # 成功终态的 status 字面量不是错误
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
    resp = await _get_authed(brain, loc)
    if resp.status_code != 200:
        return {"batch_id": batch_id, "error": f"HTTP {resp.status_code}"}
    data = resp.json() if resp.text else {}
    children = data.get("children") or []
    if not children:
        # Children not expanded yet: must NOT look like a finished single sim,
        # or --watch exits immediately (EUR wave31 false-complete).
        parent = await fetch_one(brain, loc)
        st = (parent.get("status") or "").upper()
        done = st in TERMINAL
        return {
            "batch_id": batch_id,
            "kind": "multisim",
            "child_count": 0,
            "terminal": 0,
            "errors": 1 if (parent.get("error") or done) else 0,
            "all_terminal": done,
            "children": [],
            "parent_status": parent.get("status"),
            "error": parent.get("error") or (f"parent {st} but children empty" if done else ""),
        }
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


# --watch 连续网络瞬断容忍次数：超过才放弃（每次间隔 interval 秒）
MAX_CONSECUTIVE_NET_FAIL = 10
# 视为"瞬断可重试"的异常：transport 层 raise 的内建 ConnectionError（OSError 子类）、
# 超时、以及 httpx 传输异常（按类名判定，避免硬依赖 httpx）
_TRANSIENT_EXC_NAMES = ("ConnectError", "ReadTimeout", "ConnectTimeout", "WriteTimeout",
                        "PoolTimeout", "RemoteProtocolError", "ReadError", "NetworkError",
                        "TransportError", "TimeoutException")


def _is_transient(exc):
    if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
        return True
    return type(exc).__name__ in _TRANSIENT_EXC_NAMES


async def watch_loop(brain, ids, watch, interval, max_waits, sleep=None,
                     max_net_fail=MAX_CONSECUTIVE_NET_FAIL):
    """轮询直到全部 terminal / 超时；网络瞬断只计一次失败、不终止轮询。

    2026-09-21 根治：一次 `ConnectionError: Failed to connect …`（transport 层重试
    耗尽后抛出）曾直接炸掉整个 --watch（ASI mech_screen 批：两个 multisim 已
    COMPLETE，watcher 却带着 0 收成退出，下游 harvest 收到 0 条）。瞬断只在
    连续 max_net_fail 次后才放弃；--watch 未开启时保持原语义（直接抛出）。
    """
    sleep = sleep or asyncio.sleep
    all_ok = False
    final = None
    t0 = time.time()
    net_fail = 0
    rounds = 1 if not watch else max_waits
    for round_no in range(rounds):
        try:
            final, all_ok = await run_once(brain, ids)
            net_fail = 0
        except Exception as e:  # noqa: BLE001 - 只放行瞬断类
            if not watch or not _is_transient(e):
                raise
            net_fail += 1
            all_ok = False
            print(f"\n[watch] 网络瞬断 {net_fail}/{max_net_fail}（{type(e).__name__}: {str(e)[:120]}）"
                  f"—— 继续轮询", flush=True)
            if net_fail >= max_net_fail:
                raise
        if not watch or all_ok:
            break
        print(f"\n[watch] round {round_no}/{max_waits} 耗时 {time.time() - t0:.0f}s，"
              f"{interval:.0f}s 后再查（Ctrl+C 退出）", flush=True)
        await sleep(interval)
    return final, all_ok


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
    final, all_ok = await watch_loop(brain, ids, watch=a.watch, interval=a.interval,
                                     max_waits=a.max_waits)

    if a.json_out:
        os.makedirs(os.path.dirname(a.json_out) or ".", exist_ok=True)
        json.dump(final, open(a.json_out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        print(f"\n[out] {a.json_out}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    asyncio.run(main())