# -*- coding: utf-8 -*-
"""并发探针（CONCURRENCY=6）：单条 POST（避免 multi-sim 整批连坐）+ 并发轮询。
用法同上，但吞吐 ~6x。
"""
import argparse, asyncio, json, os, sys, time

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


async def _get(bc, url, tries=4):
    for k in range(tries):
        try:
            return await bc._request("GET", url)
        except Exception:
            if k == tries - 1:
                raise
            await asyncio.sleep(4 * (k + 1))


async def submit_one(bc, expr, cfg, max_429=8):
    """单条 POST。429（CONCURRENT_SIMULATION_LIMIT_EXCEEDED）自身退避重试，
    避免并发拥挤时整条候选被白白丢掉。"""
    payload = {"type": "REGULAR", "settings": {
        "instrumentType": "EQUITY", "region": cfg["region"], "universe": cfg["universe"],
        "delay": cfg["delay"], "decay": cfg["decay"], "neutralization": cfg["neutralization"],
        "truncation": cfg["truncation"], "pasteurization": "ON", "nanHandling": cfg["nanHandling"],
        "unitHandling": "VERIFY", "language": "FASTEXPR", "visualization": False,
        "testPeriod": "P0Y0M"}, "regular": expr}
    for k in range(max_429):
        r = await bc._request("POST", "https://api.worldquantbrain.com/simulations", json=payload)
        if r.status_code == 201:
            loc = r.headers.get("Location") or ""
            return loc.rstrip("/").split("/")[-1], None
        if r.status_code == 429:
            # 并发满：指数退避后重试（15s, 30s, 45s ... 上限 120s）
            await asyncio.sleep(min(15 * (k + 1), 120))
            continue
        return None, f"POST {r.status_code} {r.text[:150]}"
    return None, "POST 429 exhausted retries"


async def poll(bc, sid, max_wait=900):
    t0 = time.time()
    while time.time() - t0 < max_wait:
        await asyncio.sleep(12)
        try:
            r = await _get(bc, f"https://api.worldquantbrain.com/simulations/{sid}")
        except Exception:
            continue
        if r.status_code != 200:
            continue
        d = r.json()
        if d.get("status") in ("COMPLETE", "ERROR", "FAIL", "WARNING"):
            return d
    return {"status": "POLL_TIMEOUT"}


async def run_one(bc, i, lab, expr, cfg, st, cp, sem):
    async with sem:
        sid, err = await submit_one(bc, expr, cfg)
        if err:
            print(f"  [{i}] {lab:24s} SUBMIT_ERR {err[:80]}", flush=True)
            st["results"].append({"label": lab, "err": err})
            save_ckpt(cp, st)
            return
        try:
            d = await poll(bc, sid)
        except Exception as e:
            st["results"].append({"label": lab, "err": f"poll:{str(e)[:60]}"})
            save_ckpt(cp, st)
            return
        aid = d.get("alpha")
        if aid:
            r3 = await _get(bc, f"https://api.worldquantbrain.com/alphas/{aid}")
            aa = r3.json(); is_ = aa.get("is") or {}
            chk = {c["name"]: (c.get("result"), c.get("value")) for c in is_.get("checks", [])}
            rec = {"label": lab, "alpha": aid, "S": is_.get("sharpe"), "F": is_.get("fitness"),
                   "T": is_.get("turnover"), "sub": chk.get("LOW_SUB_UNIVERSE_SHARPE"),
                   "y2": chk.get("LOW_2Y_SHARPE"), "sh_ok": chk.get("LOW_SHARPE"),
                   "fit_ok": chk.get("LOW_FITNESS")}
            print(f"  [{i}] {lab:24s} {aid} S={rec['S']} F={rec['F']} 2Y={rec['y2']} SUB={rec['sub']}", flush=True)
        else:
            rec = {"label": lab, "sim": d.get("status"), "msg": str(d.get("message"))[:150]}
            print(f"  [{i}] {lab:24s} {d.get('status')} {str(d.get('message'))[:100]}", flush=True)
        st["results"].append(rec)
        save_ckpt(cp, st)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="KOR")
    ap.add_argument("--universe", default="TOP600")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--exprs-file", required=True)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--decay", type=int, default=30)
    ap.add_argument("--neutralization", default="STATISTICAL")
    ap.add_argument("--truncation", type=float, default=0.08)
    ap.add_argument("--nan-handling", default="ON")
    ap.add_argument("--conc", type=int, default=6)
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()

    cfg = {"region": a.region, "universe": a.universe, "delay": a.delay, "decay": a.decay,
           "neutralization": a.neutralization, "truncation": a.truncation, "nanHandling": a.nan_handling}
    items = json.load(open(a.exprs_file, encoding="utf-8"))
    cp = ckpt_path(a.region, a.tag)
    st = {"cfg": cfg, "results": []} if a.fresh else load_ckpt(cp)
    st["cfg"] = cfg
    done = {r["label"] for r in st["results"] if r.get("alpha")}
    todo = [(l, e) for l, e in items if l not in done]
    print(f"[conc] tag={a.tag} total={len(items)} done={len(done)} todo={len(todo)} conc={a.conc}", flush=True)

    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    t0 = time.time()
    sem = asyncio.Semaphore(a.conc)
    await asyncio.gather(*[run_one(brain_client, i, l, e, cfg, st, cp, sem)
                           for i, (l, e) in enumerate(todo, 1)])
    ok = [r for r in st["results"] if isinstance(r.get("S"), (int, float))]
    ok.sort(key=lambda x: -(x["S"] or -9))
    print(f"\n=== TOP (el={time.time()-t0:.0f}s) ===")
    for r in ok[:20]:
        print(f"  {r['label']:26s} {r['alpha']} S={r['S']:.3f} F={r['F']} T={r['T']} 2Y={r.get('y2')}")


asyncio.run(main())
