import os
"""Diagnose current stage + RA/PPA gate status of candidate alphas."""
import sys, json
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts")))
from ace_lib import start_session, get_simulation_result_json, get_check_submission

# candidate alphas to inspect
CAND = {
    "YPv8gzdv": "earnings+vader (new, 3-set member)",
    "P0GxGQxM": "earnings+vader (new, redundant)",
    "rK2922Ra": "earnings+vader (new, redundant)",
    "YPv87K0M": "earnings+vader (new, redundant)",
    "vRvg7NzA": "sentiment (account existing)",
    "MPQVZRnk": "ownership (account existing)",
}

s = start_session()
for aid, note in CAND.items():
    try:
        j = get_simulation_result_json(s, aid)
    except Exception as e:
        print(f"{aid}: ERROR {e}")
        continue
    if not j:
        print(f"{aid}: EMPTY response")
        continue
    stage = j.get("stage")
    settings = j.get("settings", {})
    istats = j.get("is", {})
    sharpe = istats.get("sharpe")
    fitness = istats.get("fitness")
    subU = istats.get("subUniverseSharpe")
    print(f"\n=== {aid}  [{note}] ===")
    print(f"  stage      : {stage}")
    print(f"  region     : {settings.get('region')}  universe: {settings.get('universe')}")
    print(f"  IS sharpe  : {sharpe}  fitness: {fitness}  subUniverseSharpe: {subU}")
    # RA checks
    try:
        df = get_check_submission(s, aid)
        fails = df[(df.get("result") == "FAIL")] if "result" in df else df[df.get("result") == "FAIL"]
        pending = df[df.get("result") == "PENDING"] if "result" in df else df
        print(f"  checks total: {len(df)}")
        if "result" in df.columns:
            for _, row in df.iterrows():
                r = row.get("result")
                if r in ("FAIL", "PENDING", "WARN"):
                    print(f"    [{r}] {row.get('name')}: {row.get('msg')}")
    except Exception as e:
        print(f"  check_submission ERROR: {e}")
