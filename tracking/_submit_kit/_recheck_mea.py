# -*- coding: utf-8 -*-
"""MEA 7 颗低 PROD 候选的零成本双闸预检（再评估用，不提交）。

SELF = 本地 OS PnL 池（秒级，无锁）；PROD = 平台生产池（单并发锁 ~30s/颗）。
"""
import asyncio
import json
import sys
import time
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

OUT = WQ_ROOT / "research-data" / "mea_recheck_20260831.json"

MEA_CANDS = ["qMjLYVVP", "Jj7ee6nO", "omqEE1pn", "E5l6mmqJ",
             "Xg79vj7a", "58lEQMo1", "ak7KQoXv"]
PROD_ONLY = ["qMjLYVVP", "Jj7ee6nO", "omqEE1pn"]  # 3 颗最优先，逐颗 PROD


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    report = {}
    t0 = time.time()

    # SELF 预检（本地池，全部）
    print("=== SELF 预检（本地 OS PnL 池）===")
    for aid in MEA_CANDS:
        try:
            s = await brain.check_self_correlation(aid)
            mx = s.get("max_correlation")
            ok = s.get("passes_check")
            report.setdefault("self", {})[aid] = {"max": mx, "pass": ok}
            print(f"  {aid}: max={mx} pass={ok}")
        except Exception as e:
            report.setdefault("self", {})[aid] = {"error": str(e)}
            print(f"  {aid}: ERROR {e}")

    # PROD 预检（平台，仅前 3 颗）
    print("\n=== PROD 预检（平台生产池）===")
    for aid in PROD_ONLY:
        try:
            p = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
            pc = p.get("checks", {}).get("production", {})
            mx = pc.get("max_correlation")
            ok = pc.get("passes_check")
            report.setdefault("prod", {})[aid] = {"max": mx, "pass": ok,
                                                  "detail": p.get("checks")}
            print(f"  {aid}: max={mx} pass={ok}")
        except Exception as e:
            report.setdefault("prod", {})[aid] = {"error": str(e)}
            print(f"  {aid}: ERROR {e}")

    report["elapsed_sec"] = round(time.time() - t0, 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[elapsed] {report['elapsed_sec']}s  [saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
