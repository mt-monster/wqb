# -*- coding: utf-8 -*-
"""EUR 形态相似度 串行探针（单条 POST → 轮询 → 收割），可靠优先。

用法:
  python tmp_probe_serial.py --exprs-file <json> --tag <tag> \
      --region EUR --universe TOP2500 --neutralization SUBINDUSTRY --decay 4
断点续跑：tracking/<region>/candidates/probe_<tag>.json
"""
import argparse
import asyncio
import json
import os
import sys
import time

REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))


def ckpt_path(region, tag):
    d = os.path.join(REPO, "tracking", region, "candidates")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"probe_{tag}.json")


def load_ckpt(p):
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:
            pass
    return {"results": []}


def save_ckpt(p, obj):
    tmp = p + ".tmp"
    json.dump(obj, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, p)


async def submit_one(bc, expr, cfg):
    payload = {"type": "REGULAR", "settings": {
        "instrumentType": "EQUITY", "region": cfg["region"], "universe": cfg["universe"],
        "delay": cfg["delay"], "decay": cfg["decay"], "neutralization": cfg["neutralization"],
        "truncation": cfg["truncation"], "pasteurization": "ON", "nanHandling": cfg["nanHandling"],
        "unitHandling": "VERIFY", "language": "FASTEXPR", "visualization": False,
        "testPeriod": "P0Y0M"}, "regular": expr}
    r = await bc._request("POST", "https://api.worldquantbrain.com/simulations", json=payload)
    if r.status_code != 201:
        return None, f"POST {r.status_code} {r.text[:180]}"
    loc = r.headers.get("Location") or ""
    sid = loc.rstrip("/").split("/")[-1]
    return sid, None


async def poll(bc, sid, max_wait=600):
    t0 = time.time()
    while time.time() - t0 < max_wait:
        await asyncio.sleep(15)
        r = await bc._request("GET", f"https://api.worldquantbrain.com/simulations/{sid}")
        if r.status_code != 200:
            continue
        d = r.json()
        st = d.get("status")
        if st in ("COMPLETE", "ERROR", "FAIL", "WARNING"):
            return d
    return {"status": "POLL_TIMEOUT"}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--universe", default="TOP2500")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--exprs-file", required=True)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--decay", type=int, default=4)
    ap.add_argument("--neutralization", default="SUBINDUSTRY")
    ap.add_argument("--truncation", type=float, default=0.02)
    ap.add_argument("--nan-handling", default="ON")
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()

    cfg = {"region": a.region, "universe": a.universe, "delay": a.delay, "decay": a.decay,
           "neutralization": a.neutralization, "truncation": a.truncation,
           "nanHandling": a.nan_handling}
    items = json.load(open(a.exprs_file, encoding="utf-8"))
    cp = ckpt_path(a.region, a.tag)
    st = {"cfg": cfg, "results": []} if a.fresh else load_ckpt(cp)
    st["cfg"] = cfg
    done = {r["label"] for r in st["results"] if r.get("alpha")}
    todo = [(l, e) for l, e in items if l not in done]
    print(f"[serial] tag={a.tag} total={len(items)} done={len(done)} todo={len(todo)}", flush=True)

    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    t0 = time.time()
    for i, (lab, expr) in enumerate(todo, 1):
        sid, err = await submit_one(brain_client, expr, cfg)
        if err:
            print(f"  [{i}] {lab:22s} SUBMIT_ERR {err}", flush=True)
            st["results"].append({"label": lab, "err": err})
            save_ckpt(cp, st)
            continue
        d = await poll(brain_client, sid)
        aid = d.get("alpha")
        if aid:
            r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
            aa = r3.json(); is_ = aa.get("is") or {}
            rec = {"label": lab, "alpha": aid, "S": is_.get("sharpe"), "F": is_.get("fitness"),
                   "T": is_.get("turnover")}
            print(f"  [{i}] {lab:22s} {aid} S={rec['S']} F={rec['F']} T={rec['T']}", flush=True)
        else:
            rec = {"label": lab, "sim": d.get("status"), "msg": str(d.get("message"))[:160]}
            print(f"  [{i}] {lab:22s} {d.get('status')} {str(d.get('message'))[:110]}", flush=True)
        st["results"].append(rec)
        save_ckpt(cp, st)
        await asyncio.sleep(3)
    ok = [r for r in st["results"] if isinstance(r.get("S"), (int, float))]
    ok.sort(key=lambda x: -(x["S"] or -9))
    print(f"\n=== TOP (el={time.time()-t0:.0f}s) ===")
    for r in ok[:15]:
        print(f"  {r['label']:24s} {r['alpha']} S={r['S']:.3f} F={r['F']} T={r['T']}")


asyncio.run(main())
