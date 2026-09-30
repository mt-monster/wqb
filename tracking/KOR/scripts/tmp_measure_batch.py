# -*- coding: utf-8 -*-
"""批量 prod 直轮询（容错 + 断点续跑）。
每颗窗口默认 240s；已测到的 id（prod 非空）跳过；结果 append jsonl。
用法: python tmp_measure_batch.py ID1 ID2 ... [--window=240]
"""
import asyncio, json, sys, os, time
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
OUT = os.path.join(REPO, "tracking/KOR/candidates/prod_measure_v2.jsonl")


def load_done():
    done = {}
    if os.path.exists(OUT):
        for line in open(OUT, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("prod_max") is not None:
                done[r["id"]] = r["prod_max"]
    return done


async def measure(bc, aid, window_s, gap=15):
    t0 = time.time()
    last_err = None
    while time.time() - t0 < window_s:
        try:
            r = await bc._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
        except Exception as e:
            last_err = str(e)[:60]
            await asyncio.sleep(gap)
            try:
                await bc.ensure_authenticated()
            except Exception:
                pass
            continue
        if r.status_code == 200 and r.text.strip():
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
    win = 240
    for a in sys.argv[1:]:
        if a.startswith("--window="):
            win = int(a.split("=")[1])
    ids = [a for a in sys.argv[1:] if not a.startswith("--")]
    done = load_done()
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    todo = [i for i in ids if done.get(i) is None]
    print(f"total={len(ids)} done={len(ids)-len(todo)} todo={len(todo)} window={win}s", flush=True)
    for aid in todo:
        res = await measure(brain_client, aid, win)
        print(f"{aid}: prod_max={res.get('prod_max')} {res.get('note','')}", flush=True)
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
    print("DONE", OUT)


asyncio.run(main())
