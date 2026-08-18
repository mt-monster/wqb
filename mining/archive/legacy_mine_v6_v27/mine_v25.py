"""Tune C1 (AOP - SI combo) to lift LOW_FITNESS above 1.0 while keeping PROD_CORR<0.7,
sharpe>=1.58, SC<0.7. Higher decay / AOP-weighted. Single sims + full checks."""
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
SI  = "shrt7_shortlasso1d"

def c1(w=1.0):
    return f"group_rank(ts_zscore(vec_avg({AOP}),252) - {w}*ts_zscore(vec_avg({SI}),252), industry)"

cands = [
    ("C1_d5",  c1(1.0), "TOP3000", "INDUSTRY", 5),
    ("C1_d10", c1(1.0), "TOP3000", "INDUSTRY", 10),
    ("C1_A2",  c1(0.5), "TOP3000", "INDUSTRY", 0),
    ("C1_A2d5",c1(0.5), "TOP3000", "INDUSTRY", 5),
    ("C1_sub", f"group_rank(ts_zscore(vec_avg({AOP}),252) - ts_zscore(vec_avg({SI}),252), subindustry)", "TOP3000", "INDUSTRY", 0),
    ("C1_d20", c1(1.0), "TOP3000", "INDUSTRY", 20),
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
            if rs in ("FAIL","WARNING") or "SHARPE" in nm or "CORR" in nm or "FIT" in nm or "TURNOVER" in nm or "COST" in nm or "WEIGHT" in nm or "2Y" in nm:
                print(f"   {nm:40s} {rs:7s} val={r.get('value')} lim={r.get('limit')}", flush=True)
    else: print("   (empty)", flush=True)
print("\nDONE", flush=True)
