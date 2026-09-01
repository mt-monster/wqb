# -*- coding: utf-8 -*-
"""对候选 SA 做零成本双闸预检（SELF 本地池 + PROD 平台）。

用法: python _sa_check.py <alpha_id> [更多 id...]
"""
import asyncio
import sys
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))


async def main(ids):
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    for aid in ids:
        print(f"\n=== {aid} ===")
        d = await brain.get_alpha_details(aid)
        if d:
            isd = d.get("is") or {}
            print(f"  type={d.get('type')} sharpe={isd.get('sharpe')} fit={isd.get('fitness')} "
                  f"to={isd.get('turnover')} ret={isd.get('returns')} dd={isd.get('drawdown')}")
        try:
            s = await brain.check_self_correlation(aid)
            mx = s.get("max_correlation")
            ok = s.get("passes_check")
            print(f"  [SELF] max={mx} pass={ok}")
            recs = ((s.get("correlation_data") or {}).get("records") or [])[:5]
            for r in recs:
                print(f"        vs {r.get('id')}: {r.get('correlation')}")
        except Exception as e:
            print(f"  [SELF] ERROR {e}")
        try:
            p = await brain.check_correlation(aid, correlation_type="production", threshold=0.7)
            pc = p.get("checks", {}).get("production", {})
            print(f"  [PROD] max={pc.get('max_correlation')} pass={pc.get('passes_check')}")
        except Exception as e:
            print(f"  [PROD] ERROR {e}")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
