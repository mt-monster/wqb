"""Mine 4th unrelated alpha. FIXED event-field wrapping: vec_avg(F) [NO window] -> daily,
then ts_zscore/ts_backfill [WITH window]. Single sims, try/except, full gate checks."""
import sys, json, time
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import (start_session, generate_alpha, simulate_single_alpha,
                     get_simulation_result_json, get_check_submission)

s = start_session()
def ga(expr, uni, neut, decay):
    return generate_alpha(regular=expr, region="USA", universe=uni,
                          decay=decay, neutralization=neut)

AOP = "aggregate_open_positions_count"
FND = "fnd110_value"
SI  = "shrt7_shortlasso1d"
VAD = "headline_sentiment_vader_score"

cands = [
    ("AOP_s",  ga(f"group_rank(vec_avg({AOP}), industry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0)),
    ("AOP_z",  ga(f"group_rank(ts_zscore(vec_avg({AOP}), 252), industry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0)),
    ("AOP_b",  ga(f"group_rank(ts_backfill(vec_avg({AOP}), 252), industry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0)),
    ("FND_z",  ga(f"-group_rank(ts_zscore(vec_avg({FND}), 66), industry)", "ILLIQUID_MINVOL1M", "INDUSTRY", 5)),
    ("FND_b",  ga(f"-group_rank(ts_backfill(vec_avg({FND}), 120), industry)", "ILLIQUID_MINVOL1M", "INDUSTRY", 5)),
    ("SI_z",   ga(f"group_rank(ts_zscore(vec_avg({SI}), 252), subindustry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0)),
    ("SI_vd",  ga(f"group_rank(ts_zscore(vec_avg({SI}), 252) - ts_zscore(vec_avg({VAD}), 252), subindustry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0)),
]

results = {}
for tag, sim in cands:
    try:
        out = simulate_single_alpha(s, sim)
        aid = out.get("alpha_id")
        results[tag] = aid
        print(f"[SIM] {tag} -> {aid}", flush=True)
    except Exception as e:
        print(f"[ERR] {tag}: {e}", flush=True)
        results[tag] = None
    time.sleep(1)

print("\n=== SUMMARY ===", flush=True)
for tag, aid in results.items():
    if not aid:
        print(f"  {tag}: NO ALPHA"); continue
    j = get_simulation_result_json(s, aid)
    isd = j.get("is") or {}
    print(f"  {tag} ({aid}): sharpe={isd.get('sharpe')} fitness={isd.get('fitness')} subUniv={isd.get('subUniverseSharpe')}", flush=True)

print("\n=== FULL CHECKS (sharpe>=1.4) ===", flush=True)
for tag, aid in results.items():
    if not aid: continue
    j = get_simulation_result_json(s, aid)
    sh = (j.get("is") or {}).get("sharpe") or 0
    if sh < 1.4:
        print(f"  {tag}: sharpe {sh} < 1.4 skip", flush=True); continue
    try:
        df = get_check_submission(s, aid)
    except Exception as e:
        print(f"  {tag}: check err {e}", flush=True); continue
    print(f"\n--- {tag} ({aid}) ---", flush=True)
    if df is not None and len(df):
        for _, r in df.iterrows():
            print(f"   {str(r.get('name')):32s} {str(r.get('result')):6s} val={r.get('value')} lim={r.get('limit')}", flush=True)
    else:
        print("   (empty checks)", flush=True)

print("\nDONE", flush=True)
