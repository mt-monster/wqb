"""Mine 4th unrelated alpha v5: fnd110_value (daily) + composites (safe batch) and aggregate_open_positions_count (event, separate batch). Full checks."""
import sys, json
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import (start_session, generate_alpha, simulate_multi_alpha,
                     get_simulation_result_json, get_check_submission)

s = start_session()
def fa(expr, uni, neut, decay):
    return generate_alpha(regular=expr, region="USA", universe=uni, decay=decay, neutralization=neut)

FND = "fnd110_value"
SI  = "shrt7_shortlasso1d"
AOP = "aggregate_open_positions_count"

safe = [
  ("F1", fa(f"-group_rank(ts_zscore(ts_backfill({FND},120),66), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",5)),
  ("F2", fa(f"-group_rank(ts_zscore(ts_backfill({FND},252),120), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",5)),
  ("CF", fa(f"add(-group_rank(ts_zscore(ts_backfill({FND},120),66), industry), group_rank(ts_zscore(vec_avg({SI}),252), industry))", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
]
event = [
  ("A1", fa(f"group_rank(ts_zscore(ts_backfill({AOP}, 252), 252), industry)", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
  ("A2", fa(f"group_rank(vec_avg({AOP}), industry)", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
  ("CA", fa(f"add(group_rank(ts_zscore(ts_backfill({AOP},252),252), industry), -group_rank(ts_zscore(ts_backfill({FND},120),66), industry))", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
]

def full_check(aid):
    j = get_simulation_result_json(s, aid)
    sh=(j.get("is") or {}).get("sharpe"); fit=(j.get("is") or {}).get("fitness")
    df = get_check_submission(s, aid)
    realfail = df[(df["result"]=="FAIL") & (df["name"]!="ALREADY_SUBMITTED")]
    def gv(n):
        r=df[df["name"]==n]; return (r.iloc[0]["result"], r.iloc[0]["value"]) if len(r) else ("?","?")
    print(f"  -> {aid} sh={sh} fit={fit}")
    print(f"     PROD_CORR={gv('PROD_CORRELATION')} 2Y={gv('LOW_2Y_SHARPE')} SELF={gv('SELF_CORRELATION')}")
    if len(realfail): print(f"     HARD FAIL: {list(realfail['name'])}")
    else: print(f"     >>> ALL HARD GATES PASS (warns: {list(df[df['result'].isin(['WARNING','WARN'])]['name'])})")
    return len(realfail)==0

for bname, grp in [("SAFE", safe), ("EVENT", event)]:
    print(f"\n##### BATCH {bname} #####")
    try:
        outs = simulate_multi_alpha(s, [g[1] for g in grp])
    except Exception as e:
        print(f"  batch error: {e}"); continue
    for i,(tag,_) in enumerate(grp):
        aid = outs[i].get("alpha_id")
        print(f"\n  [{tag}] aid={aid}")
        if aid: full_check(aid)
        else: print("    FAILED (no alpha_id / cancelled)")
