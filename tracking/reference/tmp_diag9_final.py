# -*- coding: utf-8 -*-
"""EUR diag9：判死前的最后覆盖 —— 方向翻转 + 事件门控 + 混合结构。

背景：diag1-8 共 97 种结构，S 可到 1.59（sp_05）但 2Y 恒 0.61~0.76（硬墙）。
假设：近两年效应可能翻转（形态动量取代形态反转）→ 测取反版；
      或需事件门控（只在形态刚形成时交易）→ trade_when。
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
FW = "avg_similarity_falling_wedge_pattern_120"
DIFF = f"subtract(ts_zscore({RW}, 60), ts_zscore({VB}, 60))"
BASE = f"group_zscore({DIFF}, industry)"

EXPRS = [
    # A. 方向翻转（取反）
    ("flip_sp05", f"signed_power(multiply(-1, {BASE}), 0.5)"),
    ("flip_raw", f"multiply(-1, {BASE})"),
    # B. 事件门控（只在形态强时交易）
    ("gate_strong", f"trade_when(ts_zscore({RW}, 60) > 1, {BASE}, -1)"),
    ("gate_weak", f"trade_when(ts_zscore({RW}, 60) < -1, {BASE}, -1)"),
    ("gate_top", f"trade_when({RW} > ts_mean({RW}, 250), {BASE}, -1)"),
    # C. 用形态绝对水平做门（形态刚形成）
    ("gate_lvl", f"trade_when(ts_delta({RW}, 20) > 0, {BASE}, -1)"),
    # D. rank 版 + sp
    ("rank_sp05", f"signed_power(group_rank({DIFF}, industry), 0.5)"),
    # E. 组合更多看跌形态
    ("multi3_sp", f"signed_power(group_zscore(subtract(add(add({RW}, {RW}), {VB}), add({VB}, {FW})), industry), 0.5)"),
    # F. 只做多（不用负腿）
    ("long_only", f"signed_power(group_zscore({RW}, industry), 0.5)"),
    # G. 差异 = 楔形族内部（rising - falling 已测，试 rising 单独 sp）
    ("rw_sp05", f"signed_power(group_zscore({RW}, industry), 0.5)"),
    # H. 加 vol 门控（研究：高波动期注意力溢价更强）
    ("vol_gate", f"trade_when(ts_std_dev(returns, 60) > ts_mean(ts_std_dev(returns, 60), 250), {BASE}, -1)"),
    # I. 极简：纯 diff + sp
    ("diff_sp05", f"signed_power(ts_zscore(subtract({RW}, {VB}), 60), 0.5)"),
]
CKPT = os.path.join(REPO, "tracking/EUR/candidates/probe_eur_diag9_final.json")


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
            is_ = (r3.json().get("is") or {})
            chk = {c["name"]: (c.get("result"), c.get("value")) for c in is_.get("checks", [])}
            rec = {"label": lab, "alpha": aid, "S": is_.get("sharpe"), "F": is_.get("fitness"),
                   "T": is_.get("turnover"), "sub": chk.get("LOW_SUB_UNIVERSE_SHARPE"),
                   "y2": chk.get("LOW_2Y_SHARPE")}
            print(f"  {lab:14s} {aid} S={rec['S']} F={rec['F']} 2Y={rec['y2']} SUB={rec['sub']}", flush=True)
        else:
            rec = {"label": lab, "sim": d.get("status"), "msg": str(d.get("message"))[:110]}
            print(f"  {lab:14s} {d.get('status')} {str(d.get('message'))[:90]}", flush=True)
        st["results"].append(rec); save(st)
        await asyncio.sleep(3)
    ok = [r for r in st["results"] if isinstance(r.get("S"), (int, float))]
    ok.sort(key=lambda x: -(x["S"] or -9))
    print(f"\n=== TOP (el={time.time()-t0:.0f}s) ===")
    for r in ok:
        print(f"  {r['label']:14s} {r['alpha']} S={r['S']} 2Y={r['y2']} SUB={r['sub']}")


asyncio.run(main())
