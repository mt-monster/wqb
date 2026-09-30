# -*- coding: utf-8 -*-
"""直接从平台拉取候选 alpha 的 pyramids（权威塔归属）+ 完整 IS checks。

输入: JSON list of alpha ids
输出: tracking/prod_probe/pyramid_<tag>.json
"""
import sys, os, asyncio, json, argparse
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
from brain_api import brain_client


def ckpt(tag):
    d = os.path.join(REPO, "tracking", "prod_probe")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"pyramid_{tag}.json")


def save(p, o):
    t = p + ".tmp"
    json.dump(o, open(t, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(t, p)


def load(p):
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    return {"results": {}}


async def one(bc, aid, sem, st, cp):
    async with sem:
        try:
            r = await bc._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        except Exception as e:
            st["results"][aid] = {"err": repr(e)}; save(cp, st); return
        if r.status_code != 200:
            st["results"][aid] = {"err": f"HTTP {r.status_code}"}; save(cp, st); return
        d = r.json()
        isd = d.get("is") or {}
        checks = {}
        pyramids = []
        for cc in isd.get("checks", []):
            checks[cc.get("name")] = {"result": cc.get("result"), "value": cc.get("value"), "limit": cc.get("limit")}
            if cc.get("name") == "MATCHES_PYRAMID":
                for p in (cc.get("pyramids") or []):
                    pyramids.append(p.get("name"))
        st["results"][aid] = {
            "status": d.get("status"),
            "checks": checks,
            "pyramids": pyramids,
            "settings": d.get("settings"),
        }
        save(cp, st)
        fails = [k for k, v in checks.items() if v.get("result") == "FAIL"]
        print(f"  {aid} pyr={pyramids} FAILS={fails}", flush=True)


async def go():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids-file", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--conc", type=int, default=3)
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()
    ids = json.load(open(a.ids_file, encoding="utf-8"))
    cp = ckpt(a.tag)
    st = {"results": {}} if a.fresh else load(cp)
    todo = [i for i in ids if i not in st["results"]]
    print(f"[pyr] tag={a.tag} total={len(ids)} todo={len(todo)}")
    await brain_client.ensure_authenticated()
    sem = asyncio.Semaphore(a.conc)
    await asyncio.gather(*[one(brain_client, i, sem, st, cp) for i in todo])

    # 汇总
    from collections import Counter
    cnt = Counter()
    clean = []
    for aid, v in st["results"].items():
        for p in (v.get("pyramids") or ["<none>"]):
            cnt[p] += 1
        fails = [k for k, c in (v.get("checks") or {}).items() if c.get("result") == "FAIL"]
        if not fails:
            clean.append(aid)
    print("\n=== 塔分布 ===")
    for k, v in cnt.most_common():
        print(f"  {k:24} {v}")
    print(f"\n=== 无 FAIL 的候选 ({len(clean)}) ===")
    print(" ", clean)


asyncio.run(go())
