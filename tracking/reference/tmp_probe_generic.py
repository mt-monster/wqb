# -*- coding: utf-8 -*-
"""通用多结构 probe v2（可复用 / 支持断点续跑 / checkpoint）。

用法:
  python tmp_probe_generic.py --region EUR --universe TOP2500 --ds pattern_scores \
      --fields-file <path> --batch 8 --tag eur_pattern
  python tmp_probe_generic.py ... --fresh      # 忽略 checkpoint 全量重跑

纪律（2026-09-29 固化）:
  - 发批期间**禁止任何并行平台请求**（否则 multi-sim 子任务 CONCURRENT_... 整批 FAIL）
  - 每批 2~10 条；FAIL 无 message 先怀疑并发，再怀疑语法
  - checkpoint 落 tracking/<region>/candidates/probe_<tag>.json
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
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"results": []}
    return {"results": []}


def save_ckpt(p, obj):
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, p)


async def run_batch(brain_client, exprs, labels, cfg):
    from tools_sim import create_multi_simulation
    r = await create_multi_simulation(
        exprs, region=cfg["region"], universe=cfg["universe"], delay=cfg["delay"],
        decay=cfg["decay"], neutralization=cfg["neutralization"], truncation=cfg["truncation"],
        nan_handling="ON", test_period="P0Y0M")
    if isinstance(r, dict) and r.get("error"):
        return None, [{"label": l, "err": str(r.get("error"))[:200]} for l in labels]
    pid = r.get("multisimulation_id") or (r.get("location") or "").rstrip("/").split("/")[-1]
    out = []
    for i in range(30):
        await asyncio.sleep(20)
        rr = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{pid}")
        d = rr.json()
        st = d.get("status")
        if st in ("COMPLETE", "ERROR", "FAIL"):
            ch = d.get("children") or []
            for j, sid in enumerate(ch):
                r2 = await brain_client._request("GET", f"https://api.worldquantbrain.com/simulations/{sid}")
                dd = r2.json()
                aid = dd.get("alpha")
                lab = labels[j] if j < len(labels) else f"idx{j}"
                if aid:
                    r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
                    a = r3.json(); is_ = a.get("is") or {}
                    out.append({"label": lab, "alpha": aid, "S": is_.get("sharpe"),
                                "F": is_.get("fitness"), "T": is_.get("turnover")})
                else:
                    out.append({"label": lab, "sim": dd.get("status"),
                                "msg": str(dd.get("message"))[:150]})
            return pid, out
        if i >= 29:
            return pid, [{"label": l, "err": "POLL_TIMEOUT"} for l in labels]
    return pid, [{"label": l, "err": "POLL_TIMEOUT"} for l in labels]


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--exprs-file", required=True, help="json: [[label, expr], ...]")
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--decay", type=int, default=30)
    ap.add_argument("--neutralization", default="SUBINDUSTRY")
    ap.add_argument("--truncation", type=float, default=0.02)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()

    with open(a.exprs_file, "r", encoding="utf-8") as f:
        items = json.load(f)
    cfg = {"region": a.region, "universe": a.universe, "delay": a.delay, "decay": a.decay,
           "neutralization": a.neutralization, "truncation": a.truncation}

    cp = ckpt_path(a.region, a.tag)
    st = {"cfg": cfg, "results": []} if a.fresh else load_ckpt(cp)
    st["cfg"] = cfg
    done = {r["label"] for r in st["results"] if r.get("alpha")}
    todo = [(l, e) for l, e in items if l not in done]
    print(f"[probe] tag={a.tag} total={len(items)} done={len(done)} todo={len(todo)}", flush=True)
    if not todo:
        print("nothing to do"); return

    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    t0 = time.time()
    for i in range(0, len(todo), a.batch):
        chunk = todo[i:i + a.batch]
        labs = [c[0] for c in chunk]
        exps = [c[1] for c in chunk]
        pid, res = await run_batch(brain_client, exps, labs, cfg)
        for r in res:
            st["results"].append(r)
            s = r.get("S")
            print(f"   {r['label']:34s} {r.get('alpha') or r.get('sim') or r.get('err')} "
                  f"S={s} F={r.get('F')} T={r.get('T')}", flush=True)
        save_ckpt(cp, st)
        print(f"  [batch {i//a.batch+1}] pid={pid} el={time.time()-t0:.0f}s", flush=True)
    ok = [r for r in st["results"] if isinstance(r.get("S"), (int, float))]
    ok.sort(key=lambda x: -(x["S"] or -9))
    print("\n=== TOP by Sharpe ===")
    for r in ok[:12]:
        print(f"  {r['label']:34s} {r['alpha']} S={r['S']:.2f} F={r['F']} T={r['T']}")


asyncio.run(main())
