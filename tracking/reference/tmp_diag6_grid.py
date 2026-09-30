# -*- coding: utf-8 -*-
"""EUR diag6：对冠军表达式 A1 做 settings 网格扫描（decay × truncation × universe）。

冠军：A1 = group_zscore(subtract(ts_zscore(rw,60), ts_zscore(vb,60)), subindustry)
      EUR/TOP2500/D1/SUBINDUSTRY/decay4/trunc0.02 → S=1.52 F=0.79 T=0.184

目标：跨过 S>=1.58（还差 0.06）。
单变量原则：一次只扫一个维度的变化，但为节省时间做 3×2×2 网格（12 次）。
"""
import asyncio
import json
import os
import sys
import time

REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

A1 = ("group_zscore(subtract(ts_zscore(avg_similarity_rising_wedge_pattern_120, 60), "
      "ts_zscore(avg_similarity_v_reversal_bottom, 60)), subindustry)")

CKPT = os.path.join(REPO, "tracking/EUR/candidates/probe_eur_diag6_grid.json")


def save(obj):
    tmp = CKPT + ".tmp"
    json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, CKPT)


async def submit_one(bc, expr, cfg):
    payload = {"type": "REGULAR", "settings": {
        "instrumentType": "EQUITY", "region": cfg["region"], "universe": cfg["universe"],
        "delay": 1, "decay": cfg["decay"], "neutralization": cfg["neutralization"],
        "truncation": cfg["truncation"], "pasteurization": "ON", "nanHandling": "ON",
        "unitHandling": "VERIFY", "language": "FASTEXPR", "visualization": False,
        "testPeriod": "P0Y0M"}, "regular": expr}
    r = await bc._request("POST", "https://api.worldquantbrain.com/simulations", json=payload)
    if r.status_code != 201:
        return None, f"POST {r.status_code} {r.text[:150]}"
    return (r.headers.get("Location") or "").rstrip("/").split("/")[-1], None


async def poll(bc, sid, max_wait=600):
    t0 = time.time()
    while time.time() - t0 < max_wait:
        await asyncio.sleep(15)
        r = await bc._request("GET", f"https://api.worldquantbrain.com/simulations/{sid}")
        if r.status_code != 200:
            continue
        d = r.json()
        if d.get("status") in ("COMPLETE", "ERROR", "FAIL", "WARNING"):
            return d
    return {"status": "POLL_TIMEOUT"}


async def main():
    # 网格：decay × truncation × universe
    grid = []
    for uni in ("TOP2500", "TOP1200", "TOP800"):
        for dec in (4, 12):
            for tr in (0.02, 0.06):
                grid.append({"region": "EUR", "universe": uni, "decay": dec,
                             "neutralization": "SUBINDUSTRY", "truncation": tr})
    st = {"results": []}
    if os.path.exists(CKPT):
        st = json.load(open(CKPT, encoding="utf-8"))
    done = {r["label"] for r in st["results"] if r.get("alpha")}

    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    t0 = time.time()
    for cfg in grid:
        lab = f"{cfg['universe']}_d{cfg['decay']}_t{cfg['truncation']}"
        if lab in done:
            print(f"  skip {lab}"); continue
        sid, err = await submit_one(brain_client, A1, cfg)
        if err:
            print(f"  {lab:28s} SUBMIT_ERR {err}", flush=True)
            continue
        d = await poll(brain_client, sid)
        aid = d.get("alpha")
        if aid:
            r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
            is_ = (r3.json().get("is") or {})
            rec = {"label": lab, "alpha": aid, "S": is_.get("sharpe"), "F": is_.get("fitness"),
                   "T": is_.get("turnover"), "cfg": cfg}
            print(f"  {lab:28s} {aid} S={rec['S']} F={rec['F']} T={rec['T']}", flush=True)
        else:
            rec = {"label": lab, "sim": d.get("status"), "msg": str(d.get("message"))[:120], "cfg": cfg}
            print(f"  {lab:28s} {d.get('status')} {str(d.get('message'))[:100]}", flush=True)
        st["results"].append(rec)
        save(st)
        await asyncio.sleep(3)
    ok = [r for r in st["results"] if isinstance(r.get("S"), (int, float))]
    ok.sort(key=lambda x: -(x["S"] or -9))
    print(f"\n=== GRID TOP (el={time.time()-t0:.0f}s) ===")
    for r in ok:
        print(f"  {r['label']:28s} {r['alpha']} S={r['S']:.3f} F={r['F']:.3f} T={r['T']}")


asyncio.run(main())
