# -*- coding: utf-8 -*-
"""查 alpha prod 相关性 + 最大桶。用法: python tools/tmp_corr2.py <alpha_id> [...]"""
import asyncio, os, sys, json
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def one(bc, aid):
    url = f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod"
    for attempt in range(8):
        r = await bc._request("GET", url)
        if r.status_code == 200 and r.text.strip():
            d = r.json()
            recs = d.get("records", [])
            total = sum(x[2] for x in recs)
            print(f"[{aid}] buckets={len(recs)} total_prod_alphas={total}")
            for lo, hi, n in recs:
                mark = ""
                if lo >= 0.5: mark = "  <<<"
                if n > 0 or lo >= 0.4:
                    print(f"   [{lo:+.1f},{hi:+.1f}] n={n}{mark}")
            # max bucket with n>0
            nz = [x for x in recs if x[2] > 0]
            if nz:
                mx = max(nz, key=lambda x: x[0])
                print(f"   => MAX occupied bucket: [{mx[0]:+.1f},{mx[1]:+.1f}] n={mx[2]}")
            return
        elif r.status_code == 200:
            await asyncio.sleep(8)
        else:
            print(f"[{aid}] HTTP {r.status_code}: {r.text[:150]}"); return
    print(f"[{aid}] gave up")

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in sys.argv[1:]:
        await one(brain_client, aid)

asyncio.run(main())
