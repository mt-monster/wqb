# -*- coding: utf-8 -*-
"""批量探测 alpha 的 prod correlation（GET /alphas/{id}/correlations/prod）。
平台单账号单并发，空体=平台在算需重试。落盘 checkpoint 支持续跑。
用法: python tmp_probe_prod.py --ids-file <json> --tag <tag> [--fresh]
"""
import argparse, asyncio, json, os, sys, time

REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


def ckpt_path(tag):
    d = os.path.join(REPO, "tracking", "prod_probe")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"prod_{tag}.json")


def load(p):
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    return {"results": {}}


def save(p, obj):
    tmp = p + ".tmp"
    json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, p)


async def probe_one(bc, aid, sem, st, cp, max_wait=900):
    async with sem:
        t0 = time.time()
        while time.time() - t0 < max_wait:
            try:
                r = await bc._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}/correlations/prod")
            except Exception as e:
                await asyncio.sleep(15); continue
            if r.status_code != 200:
                await asyncio.sleep(15); continue
            body = r.text.strip()
            if not body:
                await asyncio.sleep(20); continue
            try:
                d = r.json()
            except Exception:
                await asyncio.sleep(20); continue
            mx = d.get("max")
            st["results"][aid] = {"prod_max": mx, "min": d.get("min"),
                                  "n_records": len(d.get("records") or []), "el": round(time.time() - t0)}
            save(cp, st)
            verdict = "PASS" if (mx is not None and mx < 0.7) else "REJECT"
            print(f"  {aid} prod_max={mx} -> {verdict}  ({time.time()-t0:.0f}s)", flush=True)
            return
        st["results"][aid] = {"prod_max": None, "err": "TIMEOUT"}
        save(cp, st)
        print(f"  {aid} TIMEOUT", flush=True)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids-file", required=True, help="JSON list of alpha ids")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--conc", type=int, default=2)
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()

    ids = json.load(open(a.ids_file, encoding="utf-8"))
    cp = ckpt_path(a.tag)
    st = {"results": {}} if a.fresh else load(cp)
    todo = [i for i in ids if i not in st["results"] or st["results"][i].get("prod_max") is None]
    print(f"[prod] tag={a.tag} total={len(ids)} todo={len(todo)} conc={a.conc}", flush=True)

    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    sem = asyncio.Semaphore(a.conc)
    await asyncio.gather(*[probe_one(brain_client, i, sem, st, cp) for i in todo])

    ok = [(k, v) for k, v in st["results"].items() if v.get("prod_max") is not None]
    ok.sort(key=lambda kv: kv[1]["prod_max"])
    print("\n=== prod 排序（低→高）===")
    for k, v in ok:
        print(f"  {k} prod={v['prod_max']}")


asyncio.run(main())
