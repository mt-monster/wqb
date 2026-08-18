"""Mine 4th unrelated alpha v3: test INTRADAY + ML-image + short-interest-boost families with FULL gate checks (incl PROD_CORRELATION & LOW_2Y_SHARPE)."""
import sys, json
import os
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import (start_session, generate_alpha, simulate_multi_alpha,
                     get_simulation_result_json, get_check_submission)

s = start_session()

def fa(expr, uni, neut, decay):
    return generate_alpha(regular=expr, region="USA", universe=uni, decay=decay, neutralization=neut)

INTR = "mean_last_trade_price_return_30m_pre_close_2"
ML1 = "single_bucket_20day_return_estimate_ohlcv_img_2"
ML2 = "probability_label0_2quantile_20day_ohlcv_img"
SI  = "shrt7_shortlasso1d"

batches = {
  # intraday reversal (different field from proven GLB)
  "INTR": [
    ("I1", fa(f"-group_rank(ts_backfill({INTR}, 66), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
    ("I2", fa(f"-group_rank(ts_decay_linear(ts_backfill({INTR}, 66), 12), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
    ("I3", fa(f"-group_rank(ts_mean(ts_backfill({INTR}, 66), 9), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
  ],
  # ML image fields
  "ML": [
    ("M1", fa(f"group_rank(winsorize(ts_backfill({ML1}, 22), std=4), industry)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
    ("M2", fa(f"-group_rank(ts_mean(ts_backfill({ML2}, 22), 5), sector)", "ILLIQUID_MINVOL1M","INDUSTRY",0)),
  ],
  # short-interest boost (field known valid in USA)
  "SI": [
    ("S1", fa(f"group_rank(ts_zscore(vec_avg({SI}), 252), industry)", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
    ("S2", fa(f"group_rank(ts_zscore(ts_backfill(vec_avg({SI}), 252), 252), subindustry)", "ILLIQUID_MINVOL1M","STATISTICAL",0)),
  ],
}

def full_check(aid):
    j = get_simulation_result_json(s, aid)
    sh = (j.get("is") or {}).get("sharpe"); fit=(j.get("is") or {}).get("fitness")
    df = get_check_submission(s, aid)
    realfail = df[(df["result"]=="FAIL") & (df["name"]!="ALREADY_SUBMITTED")]
    warns = df[df["result"].isin(["WARNING","WARN"])]
    prod = df[df["name"]=="PROD_CORRELATION"]; prod_v = prod.iloc[0]["value"] if len(prod) else None; prod_r = prod.iloc[0]["result"] if len(prod) else None
    y2 = df[df["name"]=="LOW_2Y_SHARPE"]; y2_v = y2.iloc[0]["value"] if len(y2) else None; y2_r = y2.iloc[0]["result"] if len(y2) else None
    sc = df[df["name"]=="SELF_CORRELATION"]; sc_v = sc.iloc[0]["value"] if len(sc) else None; sc_r=sc.iloc[0]["result"] if len(sc) else None
    print(f"  -> {aid} sh={sh} fit={fit}")
    print(f"     PROD_CORR={prod_r}({prod_v}) 2Y_SHARPE={y2_r}({y2_v}) SELF_CORR={sc_r}({sc_v})")
    if len(realfail):
        print(f"     HARD FAIL: {list(realfail['name'])}")
    else:
        print(f"     ALL HARD GATES PASS  >>> GOOD (warns: {list(warns['name'])})")
    return len(realfail)==0

for bname, grp in batches.items():
    print(f"\n##### BATCH {bname} #####")
    try:
        outs = simulate_multi_alpha(s, [g[1] for g in grp])
    except Exception as e:
        print(f"  batch error: {e}"); continue
    for i,(tag,_) in enumerate(grp):
        aid = outs[i].get("alpha_id")
        print(f"\n  [{tag}] aid={aid}")
        if aid: full_check(aid)
        else: print("    FAILED (no alpha_id)")
