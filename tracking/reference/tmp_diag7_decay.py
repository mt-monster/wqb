# -*- coding: utf-8 -*-
"""EUR diag7：decay 深扫 × {A1, B2} 两个最强表达式。

已知：A1 decay4→S1.52/F0.79；A1 decay12→S1.53/F0.95（F 大涨，S 微升）
      B2  decay4→S1.42/F0.80
假设：decay 继续增大可再推 S；B2 的 F 基础更高，可能率先 F>1.0。
"""
import asyncio
import json
import os
import sys
import time

REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

RW = "avg_similarity_rising_wedge_pattern_120"
VB = "avg_similarity_v_reversal_bottom"
EXPRS = {
    "A1_zsub": f"group_zscore(subtract(ts_zscore({RW}, 60), ts_zscore({VB}, 60)), subindustry)",
    "B2_ztsr": f"group_zscore(ts_rank(subtract({RW}, {VB}), 250), subindustry)",
    "A1b_zsub_ind": f"group_zscore(subtract(ts_zscore({RW}, 60), ts_zscore({VB}, 60)), industry)",
}
CKPT = os.path.join(REPO, "tracking/EUR/candidates/probe_eur_diag7_decay.json")


def save(o):
    tmp = CKPT + ".tmp"; json.dump(o, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(tmp, CKPT)


async def submit_one(bc, expr, cfg):
    payload = {"type": "REGULAR", "settings": {
        "instrumentType": "EQUITY", "region": cfg["region"], "universe": cfg["universe"],
        "delay": 1, "decay": cfg["decay"], "neutralization": cfg["neutralization"],
        "truncation": cfg["truncation"], "pasteurization": "ON", "nanHandling": "ON",
        "unitHandling": "VERIFY", "language": "FASTEXPR", "visualization": False,
        "testPeriod": "P0Y0M"}, "regular": expr}
    r = await bc._request("POST", "https://api.worldquantbrain.com/simulations", json=payload)
    if r.status_code != 201:
        return None, f"POST {r.status_code} {r.text[:130]}"
    return (r.headers.get("Location") or "").rstrip("/").split("/")[-1], None


async def poll(bc, sid, mw=600):
    t0 = time.time()
    while time.time() - t0 < mw:
        await asyncio.sleep(15)
        r = await bc._request("GET", f"https://api.worldquantbrain.com/simulations/{sid}")
        if r.status_code != 200:
            continue
        d = r.json()
        if d.get("status") in ("COMPLETE", "ERROR", "FAIL", "WARNING"):
            return d
    return {"status": "POLL_TIMEOUT"}


async def main():
    grid = []
    for name in ("A1_zsub", "B2_ztsr"):
        for dec in (20, 30, 60):
            grid.append((f"{name}_d{dec}", EXPRS[name],
                         {"region": "EUR", "universe": "TOP2500", "decay": dec,
                          "neutralization": "SUBINDUSTRY", "truncation": 0.02}))
    # 加一组 industry 轴对比（隔离 inter-industry）
    for dec in (4, 12, 30):
        grid.append((f"A1b_ind_d{dec}", EXPRS["A1b_zsub_ind"],
                     {"region": "EUR", "universe": "TOP2500", "decay": dec,
                      "neutralization": "SUBINDUSTRY", "truncation": 0.02}))

    st = json.load(open(CKPT, encoding="utf-8")) if os.path.exists(CKPT) else {"results": []}
    done = {r["label"] for r in st["results"] if r.get("alpha")}
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    t0 = time.time()
    for lab, expr, cfg in grid:
        if lab in done:
            print(f"  skip {lab}"); continue
        sid, err = await submit_one(brain_client, expr, cfg)
        if err:
            print(f"  {lab:20s} SUBMIT_ERR {err}", flush=True); continue
        d = await poll(brain_client, sid)
        aid = d.get("alpha")
        if aid:
            r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
            is_ = (r3.json().get("is") or {})
            rec = {"label": lab, "alpha": aid, "S": is_.get("sharpe"), "F": is_.get("fitness"),
                   "T": is_.get("turnover"), "cfg": cfg}
            print(f"  {lab:20s} {aid} S={rec['S']} F={rec['F']} T={rec['T']}", flush=True)
        else:
            rec = {"label": lab, "sim": d.get("status"), "msg": str(d.get("message"))[:110], "cfg": cfg}
            print(f"  {lab:20s} {d.get('status')} {str(d.get('message'))[:90]}", flush=True)
        st["results"].append(rec); save(st)
        await asyncio.sleep(3)
    ok = [r for r in st["results"] if isinstance(r.get("S"), (int, float))]
    ok.sort(key=lambda x: -(x["S"] or -9))
    print(f"\n=== TOP (el={time.time()-t0:.0f}s) ===")
    for r in ok:
        print(f"  {r['label']:20s} {r['alpha']} S={r['S']:.3f} F={r['F']:.3f} T={r['T']}")


asyncio.run(main())
