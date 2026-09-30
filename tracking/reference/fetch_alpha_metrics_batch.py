# -*- coding: utf-8 -*-
"""批量补取 alpha 指标（走 list 端点，避开 /alphas/{id} 的 429 限流）。

背景：2026-09-29 ASI 探针后，`/alphas/{id}` 单条详情端点持续 429
（"API rate limit exceeded"，全局限流，非并发占用），但
`/users/self/alphas` 列表端点正常 → 用列表端点 + 精确 id 过滤补取。

用法:
  python tracking/reference/fetch_alpha_metrics_batch.py A1 A2 A3 ...
  python tracking/reference/fetch_alpha_metrics_batch.py --file ids.txt
  python tracking/reference/fetch_alpha_metrics_batch.py --update-ckpt tracking/ASI/candidates/probe_asi_w2_sector.json
"""
import argparse
import asyncio
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

API = "https://api.worldquantbrain.com"


async def fetch(bc, ids):
    """拉多页列表，收集目标 id 的指标。"""
    want = set(ids)
    got = {}
    url = f"{API}/users/self/alphas?limit=100&order=-dateCreated"
    for _ in range(60):  # 最多 6000 条
        r = await bc._request("GET", url)
        if r.status_code != 200:
            print(f"  [warn] list {r.status_code}", flush=True)
            break
        d = r.json()
        for a in d.get("results", []):
            aid = a.get("id")
            if aid in want:
                is_ = a.get("is") or {}
                chk = {c["name"]: (c.get("result"), c.get("value"))
                       for c in is_.get("checks", [])}
                got[aid] = {
                    "label": None,
                    "alpha": aid,
                    "S": is_.get("sharpe"),
                    "F": is_.get("fitness"),
                    "T": is_.get("turnover"),
                    "sub": chk.get("LOW_SUB_UNIVERSE_SHARPE"),
                    "y2": chk.get("LOW_2Y_SHARPE"),
                    "sh_ok": chk.get("LOW_SHARPE"),
                    "fit_ok": chk.get("LOW_FITNESS"),
                    "created": a.get("dateCreated"),
                    "status": a.get("status"),
                    "region": (a.get("settings") or {}).get("region"),
                    "code": (a.get("regular") or {}).get("code"),
                }
        if len(got) >= len(want):
            break
        nxt = d.get("next")
        if not nxt:
            break
        url = nxt
        await asyncio.sleep(1)
    return got


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--update-ckpt")
    ap.add_argument("--out")
    a = ap.parse_args()

    ids = list(a.ids)
    if a.file:
        ids += [l.strip() for l in open(a.file, encoding="utf-8") if l.strip()]

    if a.update_ckpt:
        ck = json.load(open(a.update_ckpt, encoding="utf-8"))
        ids += [r["alpha"] for r in ck.get("results", []) if r.get("alpha")]
    ids = list(dict.fromkeys(ids))
    if not ids:
        print("no ids")
        return

    import brain_api
    bc = brain_api.brain_client
    await bc.ensure_authenticated()
    got = await fetch(bc, ids)

    print(f"\n=== fetched {len(got)}/{len(ids)} ===")
    for aid in ids:
        g = got.get(aid)
        if not g:
            print(f"  {aid}  <not found in list>")
            continue
        print(f"  {aid}  S={g['S']} F={g['F']} T={g['T']} 2Y={g['y2']} SUB={g['sub']} "
              f"({g['region']})")

    if a.update_ckpt:
        ck = json.load(open(a.update_ckpt, encoding="utf-8"))
        for r in ck.get("results", []):
            aid = r.get("alpha")
            g = got.get(aid)
            if not g:
                continue
            kv = {k: g[k] for k in ("S", "F", "T", "sub", "y2", "sh_ok", "fit_ok")}
            r.update({k: v for k, v in kv.items() if r.get(k) is None and v is not None})
            r.pop("sim", None)
            r.pop("msg", None)
        tmp = a.update_ckpt + ".tmp"
        json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.replace(tmp, a.update_ckpt)
        print(f"\n[ok] updated {a.update_ckpt}")

    if a.out:
        json.dump(got, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[ok] wrote {a.out}")


asyncio.run(main())
