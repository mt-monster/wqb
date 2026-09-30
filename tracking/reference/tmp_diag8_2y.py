# -*- coding: utf-8 -*-
"""EUR diag8：专攻 LOW_2Y_SHARPE（当前瓶颈 0.75 vs 1.58）。

经验库 §4 破 2Y 闸的合规旋钮：换分组轴到 exchange / market / sector / signed_power 压尾。
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
DIFF = f"subtract(ts_zscore({RW}, 60), ts_zscore({VB}, 60))"

EXPRS = [
    # 换分组轴（专攻 2Y）
    ("ax_market", f"group_zscore({DIFF}, market)"),
    ("ax_sector", f"group_zscore({DIFF}, sector)"),
    ("ax_exchange", f"group_zscore({DIFF}, exchange)"),
    ("ax_country", f"group_zscore({DIFF}, country)"),
    # 压尾（signed_power）
    ("sp_05", f"signed_power(group_zscore({DIFF}, industry), 0.5)"),
    ("sp_075", f"signed_power(group_zscore({DIFF}, industry), 0.75)"),
    ("sp_15", f"signed_power(group_zscore({DIFF}, industry), 1.5)"),
    # 截断极值
    ("winsor", f"winsorize(group_zscore({DIFF}, industry), std=4)"),
    # 时序归一（再做一层）
    ("ts_norm", f"group_zscore(ts_zscore({DIFF}, 250), industry)"),
    # rank 版
    ("rank_ind", f"group_rank({DIFF}, industry)"),
    # market 轴 + signed_power
    ("mkt_sp", f"signed_power(group_zscore({DIFF}, market), 0.75)"),
    # 原始 diff（不加 group）
    ("raw_diff", f"ts_zscore({DIFF}, 60)"),
]
CKPT = os.path.join(REPO, "tracking/EUR/candidates/probe_eur_diag8_2y.json")


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
    cfg = {"region": "EUR", "universe": "TOP2500", "decay": 12,
           "neutralization": "SUBINDUSTRY", "truncation": 0.02}
    st = json.load(open(CKPT, encoding="utf-8")) if os.path.exists(CKPT) else {"results": []}
    done = {r["label"] for r in st["results"] if r.get("alpha")}
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    t0 = time.time()
    for lab, expr in EXPRS:
        if lab in done:
            print(f"  skip {lab}"); continue
        sid, err = await submit_one(brain_client, expr, cfg)
        if err:
            print(f"  {lab:14s} SUBMIT_ERR {err}", flush=True); continue
        d = await poll(brain_client, sid)
        aid = d.get("alpha")
        if aid:
            r3 = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
            a = r3.json(); is_ = a.get("is") or {}
            chk = {c["name"]: (c.get("result"), c.get("value")) for c in is_.get("checks", [])}
            rec = {"label": lab, "alpha": aid, "S": is_.get("sharpe"), "F": is_.get("fitness"),
                   "T": is_.get("turnover"), "sub": chk.get("LOW_SUB_UNIVERSE_SHARPE"),
                   "y2": chk.get("LOW_2Y_SHARPE"), "cfg": cfg}
            print(f"  {lab:14s} {aid} S={rec['S']} F={rec['F']} SUB={rec['sub']} 2Y={rec['y2']}", flush=True)
        else:
            rec = {"label": lab, "sim": d.get("status"), "msg": str(d.get("message"))[:110], "cfg": cfg}
            print(f"  {lab:14s} {d.get('status')} {str(d.get('message'))[:90]}", flush=True)
        st["results"].append(rec); save(st)
        await asyncio.sleep(3)
    ok = [r for r in st["results"] if isinstance(r.get("S"), (int, float))]
    ok.sort(key=lambda x: -9)
    print(f"\n=== sorted by 2Y (el={time.time()-t0:.0f}s) ===")
    for r in ok:
        print(f"  {r['label']:14s} {r['alpha']} S={r['S']} 2Y={r['y2']} SUB={r['sub']}")


asyncio.run(main())
