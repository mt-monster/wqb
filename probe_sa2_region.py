import asyncio, json, sys
from collections import Counter
sys.path.insert(0, 'world-quant-brain-mcp')
from brain_api import BrainApiClient

async def main():
    b = BrainApiClient()
    await b.ensure_authenticated()

    all_regs = []
    for offset in range(0, 400, 100):
        d = await b.get_user_alphas(stage="OS", limit=100, offset=offset, alpha_type="REGULAR", order="-dateSubmitted")
        res = d.get("results", [])
        if not res: break
        all_regs += res
    print("total REGULAR OS fetched:", len(all_regs))

    by_region = Counter()
    mea = []
    for r in all_regs:
        reg = (r.get("settings") or {}).get("region")
        by_region[reg or "UNKNOWN"] += 1
        if (reg or "").upper() == "MEA":
            mea.append({
                "id": r.get("id"),
                "name": r.get("name"),
                "status": r.get("status"),
                "sharpe": (r.get("is") or {}).get("sharpe"),
                "fitness": (r.get("is") or {}).get("fitness"),
                "dateSubmitted": r.get("dateSubmitted"),
            })
    print("by region:", dict(by_region))
    print(f"\nMEA REGULAR OS count: {len(mea)}")
    for m in sorted(mea, key=lambda x: x.get("dateSubmitted") or ""):
        print(f"  {m['id']}  status={m['status']}  sharpe={m['sharpe']}  fitness={m['fitness']}  sub={m['dateSubmitted']}")

asyncio.run(main())
