# -*- coding: utf-8 -*-
"""对可提交候选做双闸预检 + 配额核对（只读）。

SELF = 本地 OS PnL 池（秒级，无锁）；PROD = 平台生产池（~30s/颗，单并发锁）。
同时读 /users/self/activities/submissions 推算 48h 滚动窗口内的已用配额。
"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "submittable_precheck_20260901.json"

# 从 submittable_scan 结果里按 fitness 取 top，逐区域均衡取样
SELF_TARGETS = [
    "JjGnYeGO", "lejwlpbe", "0mwZMK96", "mLjaYKQ5", "KP7A9LXp",
    "KP7M0Lok", "1YmJPkYz", "ZY7vP52n", "e72L9vq6", "N17EGMl7",
    "kqjppmaK", "6XqzlA5K", "vRzdk99Q", "QP9XRGjp", "e7zYRwGE",
]
PROD_TARGETS = [
    "JjGnYeGO", "lejwlpbe", "mLjaYKQ5", "KP7A9LXp", "1YmJPkYz", "ZY7vP52n",
]


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    report = {}

    # --- 配额 / 提交活动 ---
    print("=== 提交活动（推算 48h 滚动窗口） ===")
    try:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/activities/submissions",
            params={"grouping": "SUBMISSION"},
        )
        j = r.json()
        recs = ((j.get("records") or {}).get("records") or [])
        recent = [x for x in recs if x[0] >= "2026-08-28"]
        print(f"  最近提交记录：{recent}")
        report["recent_submissions"] = recent
        print(f"  yesterday({j.get('yesterday', {}).get('start')}) = "
              f"{j.get('yesterday', {}).get('value')}")
        print(f"  current({j.get('current', {}).get('start')}~"
              f"{j.get('current', {}).get('end')}) = {j.get('current', {}).get('value')}")
        report["activities"] = {
            "yesterday": j.get("yesterday"), "current": j.get("current"),
        }
    except Exception as e:
        print(f"  ERR {e}")

    # --- SELF 预检 ---
    print("\n=== SELF 预检（本地 OS PnL 池） ===")
    for aid in SELF_TARGETS:
        try:
            s = await brain.check_self_correlation(aid)
            mx, ok = s.get("max_correlation"), s.get("passes_check")
            report.setdefault("self", {})[aid] = {"max": mx, "pass": ok}
            flag = "OK " if ok else "FAIL"
            print(f"  {aid}: {flag} max={mx}")
        except Exception as e:
            report.setdefault("self", {})[aid] = {"error": str(e)[:100]}
            print(f"  {aid}: ERR {str(e)[:60]}")

    # --- PROD 预检 ---
    print("\n=== PROD 预检（平台生产池） ===")
    for aid in PROD_TARGETS:
        try:
            p = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
            pc = p.get("checks", {}).get("production", {})
            mx, ok = pc.get("max_correlation"), pc.get("passes_check")
            report.setdefault("prod", {})[aid] = {"max": mx, "pass": ok}
            flag = "OK " if ok else "FAIL"
            print(f"  {aid}: {flag} max={mx}")
        except Exception as e:
            report.setdefault("prod", {})[aid] = {"error": str(e)[:100]}
            print(f"  {aid}: ERR {str(e)[:60]}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
