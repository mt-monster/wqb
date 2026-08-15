"""mine_v11.py
补挖第 3 个可提交 alpha (完成"3 个"目标)。
沿用 v10 已验证公式: ILLIQUID_MINVOL1M + SLOW_AND_FAST + maxTrade OFF + earnings+vader 两正交信号组合。
通过换分组/换 decay 与既有 C2(YPv8gzdv)/C3(P0GxGQxM) 差异化。
TA(F,G,D)=ts_decay_linear(signed_power(subtract(group_rank(vec_avg(F),G),0.5),5),D)
"""
import json, sys, time
import os
SKILL_DIR = os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")
sys.path.insert(0, SKILL_DIR)
import ace_lib

def TA(F, G="subindustry", D=90):
    return (f"ts_decay_linear(signed_power(subtract(group_rank(vec_avg({F}), {G}), 0.5), 5), {D})")

SET_ILLIQ = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "ILLIQUID_MINVOL1M",
    "delay": 1, "decay": 6, "neutralization": "SLOW_AND_FAST", "truncation": 0.08,
    "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
    "maxTrade": "OFF", "language": "FASTEXPR", "visualization": False,
    "startDate": "2014-01-01", "endDate": "2023-12-31",
}

CANDIDATES = [
    # C4: earnings无后缀 + vader(industry) -> 与 C2(vader subindustry)/C3(earnings_7) 都不同, 新
    ("C4_earn+vaderInd_ILLIQ",
     f"add(multiply({TA('historic_earnings_surprise_score')}, 0.5), multiply({TA('headline_sentiment_vader_score','industry')}, 0.5))",
     SET_ILLIQ),
    # C5: earnings_7 + vader(subindustry) decay=60 -> 与 6XpMb0aG(=此但 decay90) 仅 decay 不同, 新
    ("C5_earn7+vader_d60_ILLIQ",
     f"add(multiply({TA('historic_earnings_surprise_score_7')}, 0.5), multiply({TA('headline_sentiment_vader_score','subindustry',60)}, 0.5))",
     SET_ILLIQ),
]

def main():
    s = ace_lib.start_session()
    results = []
    for name, code, settings in CANDIDATES:
        sim = {"type": "REGULAR", "settings": settings, "regular": code}
        print(f"\n=== {name}\n  {code}", flush=True)
        try:
            r = ace_lib.simulate_single_alpha(s, sim)
            aid = r.get("alpha_id")
            print(f"  -> alpha_id={aid}", flush=True)
            results.append({"name": name, "code": code, "alpha_id": aid})
        except Exception as e:
            print(f"  -> ERROR: {e}", flush=True)
            results.append({"name": name, "code": code, "alpha_id": None, "error": str(e)})
        time.sleep(2)
    with open("mine_v11_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n=== DONE ===")
    for r in results:
        print(r["name"], "->", r.get("alpha_id"))

if __name__ == "__main__":
    main()
