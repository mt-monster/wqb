"""Mine a 4th UNRELATED gate-passing alpha (short-interest / fundamental value families)."""
import sys, json
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import start_session, generate_alpha, simulate_single_alpha, get_simulation_result_json, get_check_submission

s = start_session()

# candidate expressions from verified real field names, using proven template structures
C = [
    # short interest family
    ("SI1", "group_rank(ts_zscore(ts_backfill(vec_avg(shrt7_shortlasso1d), 252), 252), industry)",
        dict(region="USA", universe="ILLIQUID_MINVOL1M", decay=0, neutralization="STATISTICAL")),
    ("SI2", "group_rank(vec_avg(shrt7_shortlasso1d), subindustry)",
        dict(region="USA", universe="ILLIQUID_MINVOL1M", decay=0, neutralization="STATISTICAL")),
    ("SI3", "group_rank(ts_zscore(ts_backfill(vec_avg(shrt7_shortlasso1d), 252), 252), subindustry)",
        dict(region="USA", universe="TOP3000", decay=0, neutralization="INDUSTRY")),
    # fundamental value family (EV/EBITDA, cheap=long)
    ("F1", "-group_rank(ts_zscore(ts_backfill(fnd17_3_ev2ebitda_cur, 120), 66), industry)",
        dict(region="USA", universe="ILLIQUID_MINVOL1M", decay=5, neutralization="INDUSTRY")),
    ("F2", "-group_rank(ts_zscore(ts_backfill(fnd17_3_ev2ebitda_cur, 120), 66), industry)",
        dict(region="USA", universe="TOP3000", decay=5, neutralization="INDUSTRY")),
]

results = []
for tag, expr, kw in C:
    sim = generate_alpha(regular=expr, **kw)
    print(f"\n### SIM {tag}: {expr[:70]}...")
    print(f"    universe={kw['universe']} neut={kw['neutralization']} decay={kw['decay']}")
    try:
        out = simulate_single_alpha(s, sim)
    except Exception as e:
        print(f"    SIM ERROR: {e}")
        results.append((tag, None, str(e), None, None))
        continue
    aid = out.get("alpha_id")
    if not aid:
        print("    -> FAILED (no alpha_id; likely unknown variable / error)")
        results.append((tag, None, "no alpha_id", None, None))
        continue
    j = get_simulation_result_json(s, aid)
    sh = (j.get("is") or {}).get("sharpe")
    fit = (j.get("is") or {}).get("fitness")
    print(f"    -> alpha_id={aid}  sharpe={sh}  fitness={fit}")
    # gate + self-corr
    try:
        df = get_check_submission(s, aid)
        sc = df[df["name"] == "SELF_CORRELATION"]
        sc_val = sc.iloc[0]["value"] if len(sc) else None
        sc_res = sc.iloc[0]["result"] if len(sc) else None
        hards = df[df["name"].isin(["LOW_SHARPE","LOW_FITNESS","LOW_SUB_UNIVERSE_SHARPE",
                                    "CLUSTER_TEST","IS_LADDER_SHARPE","LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE"])]
        hard_fail = hards[hards["result"]=="FAIL"]
        print(f"    SELF_CORRELATION: {sc_res} (value={sc_val})")
        print(f"    hard-gate fails: {list(hard_fail['name'])}")
        results.append((tag, aid, f"sh={sh} fit={fit} SC={sc_res}({sc_val})", hard_fail, None))
    except Exception as e:
        print(f"    check err: {e}")
        results.append((tag, aid, f"sh={sh} fit={fit} (check err {e})", None, None))

print("\n===== SUMMARY =====")
for tag, aid, msg, hf, _ in results:
    print(f"  {tag}: aid={aid} | {msg}")
