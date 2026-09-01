# -*- coding: utf-8 -*-
"""对 Jj7aRNKm / 2rlVPwdw 做零成本双闸预检（SELF 本地 + PROD 平台）。
只为预估能否过闸，不提交。"""
import asyncio
import json
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))

TARGETS = ["Jj7aRNKm", "2rlVPwdw"]
OUT = WQ_ROOT / "research-data" / "submit3_precheck.json"


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    res = {}
    for aid in TARGETS:
        print(f"\n=== {aid} ===")
        row = {}

        # SELF（本地 OS PnL 池，无锁，便宜）
        try:
            s = await brain.check_self_correlation(aid)
            row["self"] = s
            print(f"  [SELF] {json.dumps(s, ensure_ascii=False)[:500]}")
        except Exception as e:
            row["self"] = {"error": str(e)}
            print(f"  [SELF] ERROR {e}")

        # PROD（平台计算，单并发锁）
        try:
            p = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
            row["prod"] = p
            print(f"  [PROD] {json.dumps(p, ensure_ascii=False)[:500]}")
        except Exception as e:
            row["prod"] = {"error": str(e)}
            print(f"  [PROD] ERROR {e}")

        res[aid] = row

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
