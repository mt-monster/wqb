import os
"""Verify pairwise correlation + gate status of the 6 OS alphas to confirm a 3-unrelated gate-passing set."""
import sys, json
import pandas as pd
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts")))
from ace_lib import start_session, get_alpha_daily_pnl, get_check_submission, get_simulation_result_json

s = start_session()
OS = {
    "6XpMb0aG": "earnings+vader",
    "vRvg7NzA": "sentiment",
    "MPQVZRnk": "ownership",
    "KPGvRMg1": "combo/selfcorr",
    "gJ8eVmNM": "combo",
    "QPGvgO2G": "IND fundamental",
}

# 1) gate checks (FAIL/PENDING/WARN) for the 3 family reps
print("=== GATE CHECKS (only non-PASS) ===")
for aid in ["6XpMb0aG", "vRvg7NzA", "MPQVZRnk"]:
    try:
        df = get_check_submission(s, aid)
        nonpass = df[df["result"].isin(["FAIL", "PENDING", "WARNING", "WARN"])]
        print(f"\n{aid} ({OS[aid]}):")
        for _, r in nonpass.iterrows():
            print(f"   [{r['result']}] {r['name']}")
    except Exception as e:
        print(f"{aid} check err: {e}")

# 2) pairwise daily-PnL correlation
print("\n=== PAIRWISE DAILY-PnL CORRELATION ===")
pnls = {}
for aid in OS:
    try:
        d = get_alpha_daily_pnl(s, aid)
        col = [c for c in d.columns if "pnl" in c.lower()][0]
        ser = d[col]
        ser.index = pd.to_datetime(ser.index)
        pnls[aid] = ser
    except Exception as e:
        print(f"  pnl err {aid}: {e}")

ids = list(pnls.keys())
print("        " + " ".join(f"{i[:6]:>8}" for i in ids))
for a in ids:
    row = []
    for b in ids:
        if a in pnls and b in pnls:
            c = pd.concat([pnls[a], pnls[b]], axis=1).dropna()
            corr = c.iloc[:,0].corr(c.iloc[:,1])
            row.append(f"{corr:8.3f}")
        else:
            row.append("    NA")
    print(f"{a[:6]:>6}: " + " ".join(row))
