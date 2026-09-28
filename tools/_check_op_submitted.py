#!/usr/bin/env python3
"""Fetch expressions for submitted alphas whose local DB expression is empty,
and scan them for a given operator (default ts_max). Resumable via results/op_scan.json."""
import asyncio, json, os, sys

VENV = "D:/coding/traeCN_project/wqb/world-quant-brain-mcp"
sys.path.insert(0, VENV)
sys.path.insert(0, "D:/coding/traeCN_project/wqb/src")
from brain_api import brain_client  # noqa: E402
from wqb.db_conn import connect as db_connect  # noqa: E402

DB = "D:/coding/traeCN_project/wqb/data/wqb.db"
OUT = "D:/coding/traeCN_project/wqb/results/op_scan.json"
OP = sys.argv[1] if len(sys.argv) > 1 else "ts_max"

def log(*a): print(*a, flush=True)

async def robust(fn, *a, tries=6, **kw):
    last = None
    for i in range(tries):
        try:
            return await fn(*a, **kw)
        except Exception as e:
            last = e; m = str(e)
            await asyncio.sleep(20 + i*10 if "429" in m else 4 + i*3)
    raise last

def gap_ids():
    db = db_connect(DB); db.row_factory = sqlite3.Row
    cur = db.execute(
        "SELECT alpha_id, platform_status, alpha_type FROM alphas "
        "WHERE platform_status IN ('ACTIVE','DECOMMISSIONED') "
        "AND (expression IS NULL OR expression='')")
    rows = [dict(r) for r in cur.fetchall()]; db.close(); return rows

def load_state():
    if os.path.exists(OUT):
        try: return json.load(open(OUT))
        except Exception: pass
    return {}

async def main():
    state = load_state()
    gaps = [g for g in gap_ids() if g["alpha_id"] not in state]
    log(f"[init] gap alphas to fetch = {len(gaps)} (op={OP})")
    for g in gaps:
        aid = g["alpha_id"]
        try:
            d = await robust(brain_client.get_alpha_details, aid)
            reg = d.get("regular") or {}
            code = reg.get("code")
            combo = d.get("combo")
            settings = d.get("settings") or {}
            stype = d.get("type")
            blob = " ".join([str(code or ""), json.dumps(combo or "", ensure_ascii=False)])
            state[aid] = {
                "platform_status": d.get("status"), "type": stype,
                "region": settings.get("region"), "has_op": OP in blob,
                "code": code, "combo": combo,
            }
            log(f"  {aid} [{d.get('status')}] type={stype} region={settings.get('region')} has_{OP}={state[aid]['has_op']}")
        except Exception as e:
            log(f"  {aid} FAIL: {e}")
            state[aid] = {"error": str(e)}
        json.dump(state, open(OUT, "w"), ensure_ascii=False, indent=2)
        await asyncio.sleep(1.0)

    hits = [k for k, v in state.items() if isinstance(v, dict) and v.get("has_op")]
    log(f"\n>>> submitted-but-empty-expression alphas containing '{OP}': {len(hits)} {hits}")
    for k in hits:
        v = state[k]
        log(f"   {k} region={v.get('region')} type={v.get('type')}")
        if v.get("code"): log(f"     regular: {v['code'][:300]}")
        if v.get("combo"): log(f"     combo: {json.dumps(v['combo'], ensure_ascii=False)[:300]}")

asyncio.run(main())
