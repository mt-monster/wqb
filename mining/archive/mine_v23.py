"""Try AOP (institutional positioning) in TOP3000 universe where after-cost should be positive
(liquid names). Single sims + full gate checks. Target: pass after-cost gate + all hard gates,
keep SC<0.7 and PROD<0.7 vs existing OS alphas."""
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
cands = [
    ("T0",  base, "TOP3000", "INDUSTRY", 0),
    ("T5",  base, "TOP3000", "INDUSTRY", 5),
    ("T10", base, "TOP3000", "INDUSTRY", 10),
    ("smT", f"group_rank(ts_zscore(ts_backfill(vec_avg({AOP}), 252), 252), industry)", "TOP3000", "INDUSTRY", 0),
    ("smT5",f"group_rank(ts_zscore(ts_backfill(vec_avg({AOP}), 252), 252), industry)", "TOP3000", "INDUSTRY", 5),
]
results = {}
for tag, expr, uni, neut, dec in cands:
    try:
        out = simulate_single_alpha(s, ga(expr, uni, neut, dec))
        aid = out.get("alpha_id"); results[tag] = aid
        print(f"[SIM] {tag} -> {aid}", flush=True)
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
            if rs in ("FAIL","WARNING") or "SHARPE" in nm or "CORR" in nm or "FIT" in nm or "TURNOVER" in nm or "COST" in nm:
                print(f"   {nm:40s} {rs:7s} val={r.get('value')} lim={r.get('limit')}", flush=True)
    else: print("   (empty)", flush=True)
print("\nDONE", flush=True)
