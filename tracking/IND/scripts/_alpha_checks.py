"""打印指定 alpha 的全量 checks（非 PASS 项 + limit/value）+ 关键 IS 指标。

用法: python tracking/IND/scripts/_alpha_checks.py <aid> [<aid> ...]
"""
import asyncio
import sys

sys.path.insert(0, "world-quant-brain-mcp")
from brain_api import brain_client as brain  # noqa: E402

FIELD_KEYS = ("sharpe", "fitness", "returns", "turnover", "drawdown", "margin")


async def main():
    await brain.ensure_authenticated()
    for aid in sys.argv[1:]:
        r = await brain._request("GET", f"{brain.base_url}/alphas/{aid}")
        ad = r.json()
        isd = ad.get("is") or {}
        print(f"\n===== {aid}  status={ad.get('status')} =====")
        print("  IS: " + "  ".join(f"{k}={isd.get(k)}" for k in FIELD_KEYS))
        print(f"  L/Sh = {isd.get('longCount')}/{isd.get('shortCount')}")
        print("  code:", (ad.get("regular") or {}).get("code"))
        for c in (isd.get("checks") or []):
            if c.get("result") == "PASS":
                continue
            print(f"  [{c.get('result'):8s}] {c.get('name'):<40} limit={c.get('limit')} value={c.get('value')}")


asyncio.run(main())
