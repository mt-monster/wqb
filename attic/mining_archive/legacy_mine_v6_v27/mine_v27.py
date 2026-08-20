"""Mine 4th UNRELATED alpha: probe 4 genuinely distinct USA families with full gate checks.
Template (universal, handles daily+event): group_rank(ts_zscore(vec_avg(F),252), industry)"""
import sys, json, time
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import start_session, generate_alpha, simulate_single_alpha, get_simulation_result_json, get_check_submission

s = start_session()

def mk(expr, uni, neut, decay):
    return generate_alpha(regular=expr, region="USA", universe=uni, decay=decay, neutralization=neut)

# (tag, expr, universe, neutralization, decay)
C = [
    ("OPT_A", "group_rank(ts_zscore(vec_avg(opt6_ivetfratio),252), industry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0),
    ("OPT_B", "group_rank(ts_zscore(vec_avg(opt6_ivhvxernratio),252), industry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0),
    ("OPT_C", "group_rank(ts_zscore(vec_avg(opt6_20div),252), industry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0),
    ("ES_A",  "group_rank(ts_zscore(vec_avg(historic_earnings_surprise_score_7),252), industry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0),
    ("ANL_A", "group_rank(ts_zscore(vec_avg(analyst_earnings_revision_score),252), industry)", "TOP3000", "INDUSTRY", 0),
    ("MOM_A", "group_rank(ts_zscore(vec_avg(momentum_strength_index),252), industry)", "ILLIQUID_MINVOL1M", "STATISTICAL", 0),
]

KEY = ["LOW_SHARPE","LOW_FITNESS","LOW_SUB_UNIVERSE_SHARPE","CLUSTER_TEST","IS_LADDER_SHARPE",
       "LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE","LOW_AFTER_COST_UNIVERSE_SHARPE","LOW_2Y_SHARPE",
       "PROD_CORRELATION","SELF_CORRELATION","SUB_TEST","OSMOSIS_ALLOCATION","MATCHES_THEMES"]

def full_check(aid):
    j = get_simulation_result_json(s, aid)
    isd = j.get("is") or {}
    sh = isd.get("sharpe"); fit = isd.get("fitness")
    df = get_check_submission(s, aid)
    print(f"    sharpe={sh} fitness={fit}")
    fails = df[df["result"]=="FAIL"]
    for n in KEY:
        r = df[df["name"]==n]
        if len(r):
            row = r.iloc[0]
            print(f"    {n:42s} {row['result']:5s} v={row['value']}")
    realfail = fails[fails["name"]!="ALREADY_SUBMITTED"]
    print(f"    >>> REAL FAIL GATES: {list(realfail['name'])}")
    return sh, fit, list(realfail["name"])

results = []
for tag, expr, uni, neut, decay in C:
    sim = mk(expr, uni, neut, decay)
    print(f"\n### SIM {tag}: {expr[:60]}... [{uni}/{neut}/d{decay}]")
    try:
        out = simulate_single_alpha(s, sim)
    except Exception as e:
        print(f"    SIM ERROR: {e}")
        results.append((tag, None, str(e)[:120]))
        continue
    aid = out.get("alpha_id")
    if not aid:
        print("    -> FAILED (no alpha_id; unknown variable / parse error)")
        results.append((tag, None, "no alpha_id"))
        continue
    print(f"    -> alpha_id={aid}")
    try:
        full_check(aid)
    except Exception as e:
        print(f"    check err: {e}")
    results.append((tag, aid, "ok"))

print("\n===== SUMMARY =====")
for tag, aid, msg in results:
    print(f"  {tag}: aid={aid} | {msg}")
