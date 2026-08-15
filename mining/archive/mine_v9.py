"""mine_v9.py
Mine NEW ra_failed:false alphas by applying transform VARIANTS of the proven
T_A earnings/sentiment template to the 3 usable event-type fields:
  - historic_earnings_surprise_score        (xAdL5vmN used this exact template -> sharpe 4.51)
  - historic_earnings_surprise_score_7      (6XpMb0aG combined w/ vader -> 4.32)
  - headline_sentiment_vader_score          (used inside 6XpMb0aG via vec_avg)

T_A base template:
  ts_decay_linear(signed_power(subtract(group_rank(vec_avg(F), GROUP), 0.5), POWER), DECAY)

Settings copied EXACTLY from xAdL5vmN (ra_failed:false, sharpe 4.51):
  EQUITY/USA/TOP3000/delay1/decay6/neutralization=SLOW_AND_FAST/trunc0.08/
  pasteur ON/unit VERIFY/nan ON/maxTrade ON/FASTEXPR/2014-2023
"""
import json
import sys
import os
import time

# ace_lib lives in the skill scripts dir
import os
SKILL_DIR = os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")
sys.path.insert(0, SKILL_DIR)
import ace_lib

SETTINGS = {
    "instrumentType": "EQUITY",
    "region": "USA",
    "universe": "TOP3000",
    "delay": 1,
    "decay": 6,
    "neutralization": "SLOW_AND_FAST",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "ON",
    "maxTrade": "ON",
    "language": "FASTEXPR",
    "visualization": False,
    "startDate": "2014-01-01",
    "endDate": "2023-12-31",
}

def ta(field, group="subindustry", decay=90, power=5):
    return (f"ts_decay_linear(signed_power(subtract(group_rank(vec_avg({field}), {group}), 0.5), {power}), {decay})")

# Candidate variants: each differs from existing alphas (xAdL5vmN / 6XpMb0aG)
CANDIDATES = [
    # name, field, group, decay, power
    ("earn7_sub90",   "historic_earnings_surprise_score_7",      "subindustry", 90, 5),  # proven component alone
    ("earn_ind90",    "historic_earnings_surprise_score",        "industry",    90, 5),  # group change
    ("earn_sub60",    "historic_earnings_surprise_score",        "subindustry", 60, 5),  # decay change
    ("earn_sub3",     "historic_earnings_surprise_score",        "subindustry", 90, 3),  # power change
    ("earn7_ind90",   "historic_earnings_surprise_score_7",      "industry",    90, 5),
    ("earn7_sub120",  "historic_earnings_surprise_score_7",      "subindustry", 120, 5),
    ("vader_sub90",   "headline_sentiment_vader_score",          "subindustry", 90, 5),  # different field
    ("earn_sec90",    "historic_earnings_surprise_score",        "sector",      90, 5),
]

def main():
    s = ace_lib.start_session()
    results = []
    for name, field, group, decay, power in CANDIDATES:
        code = ta(field, group, decay, power)
        sim_data = {"type": "REGULAR", "settings": SETTINGS, "regular": code}
        print(f"\n=== {name}: {code}", flush=True)
        try:
            r = ace_lib.simulate_single_alpha(s, sim_data)
            aid = r.get("alpha_id")
            print(f"  -> alpha_id={aid}", flush=True)
            results.append({"name": name, "code": code, "alpha_id": aid})
        except Exception as e:
            print(f"  -> ERROR: {e}", flush=True)
            results.append({"name": name, "code": code, "alpha_id": None, "error": str(e)})
        time.sleep(2)
    with open("mine_v9_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n=== DONE. Saved mine_v9_results.json ===")
    for r in results:
        print(r["name"], "->", r.get("alpha_id"))

if __name__ == "__main__":
    main()
