"""Mine 4th unrelated alpha v4: aggregate_open_positions_count, fnd110_value, and composites. Full gate checks."""
import sys, json
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import (start_session, generate_alpha, simulate_multi_alpha,
                     get_simulation_result_json, get_check_submission)

s = start_session()
def fa(expr, uni, neut, decay):
    return generate_alpha(regular=expr, region="USA", universe=uni, decay=decay, neutralization=neut)

AOP = "aggregate_open_positions_count"
SI  = "shrt7_shortlasso1d"
FND = "fnd110_value"

cands = [
  ("A1", fa(f"group_rank(ts_zscore(ts_backfill(vec_avg({AOP}),252),252), industry)", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
  ("A2", fa(f"group_rank(ts_zscore(ts_backfill(vec_avg({AOP}),252),252), subindustry)", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
  ("F1", fa(f"-group_rank(ts_zscore(ts_backfill({FND},120),66), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",5)),
  ("C1", fa(f"add(group_rank(ts_zscore(ts_backfill(vec_avg({SI}),252),252), industry), group_rank(ts_zscore(ts_backfill(vec_avg({AOP}),252),252), industry))", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
  ("C2", fa(f"add(group_rank(ts_zscore(ts_backfill(vec_avg({AOP}),252),252), industry), -group_rank(ts_zscore(ts_backfill({FND},120),66), industry))", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
  ("C3", fa(f"add(group_rank(ts_zscore(ts_backfill(vec_avg({SI}),252),252), industry), -group_rank(ts_zscore(ts_backfill({FND},120),66), industry))", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
]

print(f"Launching {len(cands)} sims...")
outs = simulate_multi_alpha(s, [c[1] for c in cands])
idmap = {cands[i][0]: outs[i].get("alpha_id") for i in range(len(cands))}

def full_check(aid):
    j = get_simulation_result_json(s, aid)
    sh=(j.get("is") or {}).get("sharpe"); fit=(j.get("is") or {}).get("fitness")
    df = get_check_submission(s, aid)
    realfail = df[(df["result"]=="FAIL") & (df["name"]!="ALREADY_SUBMITTED")]
    def gv(n):
        r=df[df["name"]==n]; return (r.iloc[0]["result"], r.iloc[0]["value"]) if len(r) else ("?","?")
    pc=gv("PROD_CORRELATION"); y2=gv("LOW_2Y_SHARPE"); sc=gv("SELF_CORRELATION")
    print(f"  -> {aid} sh={sh} fit={fit}")
    print(f"     PROD_CORR={pc} 2Y_SHARPE={y2} SELF_CORR={sc}")
    if len(realfail): print(f"     HARD FAIL: {list(realfail['name'])}")
    else: print(f"     >>> ALL HARD GATES PASS (warns: {list(df[df['result'].isin(['WARNING','WARN'])]['name'])})")
    return len(realfail)==0

for tag,aid in idmap.items():
    print(f"\n[{tag}] aid={aid}")
    if aid: full_check(aid)
    else: print("  FAILED (no alpha_id)")
