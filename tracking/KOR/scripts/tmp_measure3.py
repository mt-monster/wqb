# -*- coding: utf-8 -*-
"""KOR 池 prod 重测 v3（提交后遗留值全部失效，需重测）。
用法: python tmp_measure3.py  + 环境变量 IDS
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
OUT = os.path.join(REPO, "tracking/KOR/candidates/prod_measure_v3.jsonl")

async def measure(bc, aid, window_s=200, gap=12):
    t0 = time.time(); last=None
    while time.time()-t0 < window_s:
        try:
            r = await bc._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
        except Exception as e:
            last=str(e)[:50]; await asyncio.sleep(gap); continue
        if r.status_code==200 and r.text.strip():
            try: d=r.json()
            except Exception: await asyncio.sleep(gap); continue
            mx=d.get("max"); recs=d.get("records") or []
            if mx is None and recs:
                mx=max((x[2] for x in recs if len(x)>2 and x[2] is not None), default=None)
            return {"id":aid,"prod_max":mx}
        await asyncio.sleep(gap)
    return {"id":aid,"prod_max":None,"note":"TIMEOUT"}

async def main():
    ids = os.environ.get("IDS","").split()
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in ids:
        res = await measure(brain_client, aid)
        print(f"{aid}: prod={res.get('prod_max')} {res.get('note','')}", flush=True)
        open(OUT,"a",encoding="utf-8").write(json.dumps(res,ensure_ascii=False)+"\n")

asyncio.run(main())
