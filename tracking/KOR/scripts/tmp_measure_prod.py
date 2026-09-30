# -*- coding: utf-8 -*-
"""对指定 alpha id 列表直轮询 GET /alphas/{id}/correlations/prod 测 prod 真值。
不受提交配额影响（非提交端点）。空体=平台仍在算，非空取 max。
同时本地算 self-corr（与库内 ACTIVE 比对）。
用法: python tmp_measure_prod.py ID1 ID2 ...
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


async def measure(bc, aid, window_s=600, gap=15):
    t0 = time.time()
    while time.time() - t0 < window_s:
        r = await bc._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
        if r.status_code == 200:
            body = r.text.strip()
            if body:
                try:
                    d = r.json()
                except Exception:
                    await asyncio.sleep(gap); continue
                recs = d.get("records") or []
                mx = d.get("max")
                if mx is None and recs:
                    mx = max((r_[2] if len(r_) > 2 else None) for r_ in recs if r_[2] is not None)
                return {"id": aid, "prod_max": mx, "min": d.get("min"), "n": len(recs)}
        await asyncio.sleep(gap)
    return {"id": aid, "prod_max": None, "note": "TIMEOUT"}


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    ids = sys.argv[1:]
    out = []
    for aid in ids:
        res = await measure(brain_client, aid)
        print(f"{aid}: prod_max={res.get('prod_max')} {res.get('note','')}")
        out.append(res)
    p = os.path.join(REPO, "tracking/KOR/candidates/prod_measure_si12.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("SAVED", p)


asyncio.run(main())
