# -*- coding: utf-8 -*-
"""prod 直轮询 v2：容错版。每次请求失败（ConnectionError）自动重试，超时不炸。
用法: python tmp_measure_prod2.py ID1 ID2 ...  [--window=600]
结果实时 append 到 prod_measure_v2.jsonl。
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
OUT = os.path.join(REPO, "tracking/KOR/candidates/prod_measure_v2.jsonl")


async def measure(bc, aid, window_s=600, gap=15):
    t0 = time.time()
    last_err = None
    while time.time() - t0 < window_s:
        try:
            r = await bc._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
        except Exception as e:
            last_err = str(e)[:80]
            await asyncio.sleep(gap)
            await bc.ensure_authenticated()
            continue
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
                    mx = max((x[2] if len(x) > 2 else None) for x in recs if x[2] is not None)
                return {"id": aid, "prod_max": mx, "n": len(recs)}
        await asyncio.sleep(gap)
    return {"id": aid, "prod_max": None, "note": "TIMEOUT" + (f" err={last_err}" if last_err else "")}


async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = []
    for aid in ids:
        res = await measure(brain_client, aid)
        print(f"{aid}: prod_max={res.get('prod_max')} {res.get('note','')}", flush=True)
        out.append(res)
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
    print("DONE", OUT)


asyncio.run(main())
