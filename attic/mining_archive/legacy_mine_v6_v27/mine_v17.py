"""Tune the fundamental EV/EBITDA value factor (and a couple short-interest boosts) to clear the sharpe>=1.58 gate with SC<0.7."""
import sys, json
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import (start_session, generate_alpha, simulate_multi_alpha,
                     get_simulation_result_json, get_check_submission)

s = start_session()

F = "fnd17_3_ev2ebitda_cur"
SI = "shrt7_shortlasso1d"

def fa(expr, uni, neut, decay):
    return generate_alpha(regular=expr, region="USA", universe=uni, decay=decay, neutralization=neut)

# Fundamental value-factor grid (USA/ILLIQUID_MINVOL1M, INDUSTRY)
grid = [
    ("fA", fa(f"-group_rank(ts_zscore(ts_backfill({F},120),66), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
    ("fB", fa(f"-group_rank(ts_zscore(ts_backfill({F},120),66), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",10)),
    ("fC", fa(f"-group_rank(ts_zscore(ts_backfill({F},120),66), subindustry)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
    ("fD", fa(f"-group_rank(ts_zscore(ts_backfill({F},252),120), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",5)),
    ("fE", fa(f"-rank(ts_zscore(ts_backfill({F},120),66))", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
    ("fF", fa(f"-group_rank(ts_backfill({F},120), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
    ("fG", fa(f"-group_rank(ts_zscore(ts_backfill({F},120),66), sector)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
    # short-interest boosts (USA/ILLIQUID_MINVOL1M/STATISTICAL)
    ("sA", fa(f"group_rank(vec_avg({SI}), industry)", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
    ("sB", fa(f"-group_rank(vec_avg({SI}), industry)", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
]

print(f"Launching {len(grid)} simulations in parallel...")
outs = simulate_multi_alpha(s, [g[1] for g in grid])
idmap = {grid[i][0]: outs[i].get("alpha_id") for i in range(len(grid))}
for tag, aid in idmap.items():
    print(f"  {tag} -> {aid}")

print("\n===== RESULTS =====")
for tag, aid in idmap.items():
    if not aid:
        print(f"  {tag}: FAILED (no alpha_id)"); continue
    j = get_simulation_result_json(s, aid)
    sh = (j.get("is") or {}).get("sharpe")
    fit = (j.get("is") or {}).get("fitness")
    sc_v = sc_r = None; hb = []
    try:
        df = get_check_submission(s, aid)
        sc = df[df["name"]=="SELF_CORRELATION"]
        if len(sc): sc_r, sc_v = sc.iloc[0]["result"], sc.iloc[0]["value"]
        hards = df[df["name"].isin(["LOW_SHARPE","LOW_FITNESS","LOW_SUB_UNIVERSE_SHARPE","CLUSTER_TEST","IS_LADDER_SHARPE","LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE"])]
        hb = list(hards[hards["result"]=="FAIL"]["name"])
    except Exception as e:
        print(f"  {tag}: check err {e}")
    gate = "PASS" if not hb else f"FAIL:{hb}"
    ok = (sh is not None and sh>=1.58 and (sc_v is None or sc_v<0.7))
    print(f"  {tag}: aid={aid} sharpe={sh} fit={fit} SC={sc_r}({sc_v}) gate={gate} {'>>> GOOD' if ok else ''}")
