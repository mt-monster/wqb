"""Tune AOP_z to pass LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE by reducing turnover
via higher decay / longer smoothing. Single sims + full gate checks."""
import sys, time
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import (start_session, generate_alpha, simulate_single_alpha,
                     get_simulation_result_json, get_check_submission)

s = start_session()
def ga(expr, uni, neut, decay):
    return generate_alpha(regular=expr, region="USA", universe=uni,
                          decay=decay, neutralization=neut)
AOP = "aggregate_open_positions_count"
base = f"group_rank(ts_zscore(vec_avg({AOP}), 252), industry)"

# vary decay + smoothing to cut turnover
cands = [
    ("d5",   base, 5),
    ("d10",  base, 10),
    ("d20",  base, 20),
    ("d40",  base, 40),
    ("sm",   f"group_rank(ts_zscore(ts_backfill(vec_avg({AOP}), 252), 252), industry)", 0),
    ("sm_d5",f"group_rank(ts_zscore(ts_backfill(vec_avg({AOP}), 252), 252), industry)", 5),
    ("w504", f"group_rank(ts_zscore(vec_avg({AOP}), 504), industry)", 5),
]

results = {}
for tag, expr, dec in cands:
    try:
        out = simulate_single_alpha(s, ga(expr, "ILLIQUID_MINVOL1M", "STATISTICAL", dec))
        aid = out.get("alpha_id"); results[tag] = aid
        print(f"[SIM] {tag} (decay={dec}) -> {aid}", flush=True)
    except Exception as e:
        print(f"[ERR] {tag}: {e}", flush=True); results[tag] = None
    time.sleep(1)

print("\n=== SUMMARY ===", flush=True)
for tag, aid in results.items():
    if not aid: print(f"  {tag}: NO ALPHA", flush=True); continue
    j = get_simulation_result_json(s, aid); isd = j.get("is") or {}
    print(f"  {tag} ({aid}): sharpe={isd.get('sharpe')} fitness={isd.get('fitness')} subUniv={isd.get('subUniverseSharpe')}", flush=True)

print("\n=== FULL CHECKS ===", flush=True)
for tag, aid in results.items():
    if not aid: continue
    j = get_simulation_result_json(s, aid)
    sh = (j.get("is") or {}).get("sharpe") or 0
    if sh < 1.4:
        print(f"  {tag}: sharpe {sh} < 1.4 skip", flush=True); continue
    try: df = get_check_submission(s, aid)
    except Exception as e: print(f"  {tag}: check err {e}", flush=True); continue
    print(f"\n--- {tag} ({aid}) ---", flush=True)
    if df is not None and len(df):
        for _, r in df.iterrows():
            nm=str(r.get('name')); rs=str(r.get('result'))
            if rs in ("FAIL","WARNING") or "SHARPE" in nm or "CORR" in nm or "FIT" in nm or "TURNOVER" in nm:
                print(f"   {nm:36s} {rs:7s} val={r.get('value')} lim={r.get('limit')}", flush=True)
    else: print("   (empty)", flush=True)
print("\nDONE", flush=True)
