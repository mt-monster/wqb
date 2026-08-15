"""mine_v10.py
基于 9qp8rqbq (earnings_7 单信号, sharpe3.93 但 sub_universe 1.07<1.7 失败) 改进:
在 earnings 信号上并联一个正交的 vader 情绪腿, 复刻 6XpMb0aG (earnings_7+vader, ra_failed:false) 的
提升子宇宙 sharpe 的打法, 但用字段/分组差异做成新 alpha (避免与 6XpMb0aG 完全重复)。

TA(F,G) = ts_decay_linear(signed_power(subtract(group_rank(vec_avg(F), G), 0.5), 5), 90)

设置: 复刻 6XpMb0aG 已验证通过的组合 (ILLIQUID_MINVOL1M/SLOW_AND_FAST/maxTrade OFF);
其中 C1 保留 9qp8rqbq 的原 universe (TOP3000) 以贴合"在其基础上改进"。
"""
import json, sys, time
import os
SKILL_DIR = os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")
sys.path.insert(0, SKILL_DIR)
import ace_lib

def TA(F, G="subindustry"):
    return (f"ts_decay_linear(signed_power(subtract(group_rank(vec_avg({F}), {G}), 0.5), 5), 90)")

SET_ILLIQ = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "ILLIQUID_MINVOL1M",
    "delay": 1, "decay": 6, "neutralization": "SLOW_AND_FAST", "truncation": 0.08,
    "pasteurization": "ON", "unitHandling": "VERIFY", "nanHandling": "ON",
    "maxTrade": "OFF", "language": "FASTEXPR", "visualization": False,
    "startDate": "2014-01-01", "endDate": "2023-12-31",
}
SET_TOP3K = dict(SET_ILLIQ, universe="TOP3000", maxTrade="ON")  # 9qp8rqbq 原设置

# (name, code, settings)
CANDIDATES = [
    # C1: 保留 9qp8rqbq 的 universe(TOP3000), earnings_7 + vader(均 subindustry) -> 与 6XpMb0aG(ILLIQ) 不同 universe, 新
    ("C1_earn7+vader_TOP3k",
     f"add(multiply({TA('historic_earnings_surprise_score_7')}, 0.5), multiply({TA('headline_sentiment_vader_score')}, 0.5))",
     SET_TOP3K),
    # C2: 已验证 universe(ILLIQ), earnings无后缀 + vader(subindustry) -> 与 6XpMb0aG(earnings_7) 字段不同, 新
    ("C2_earn+vader_ILLIQ",
     f"add(multiply({TA('historic_earnings_surprise_score')}, 0.5), multiply({TA('headline_sentiment_vader_score')}, 0.5))",
     SET_ILLIQ),
    # C3: 已验证 universe(ILLIQ), earnings_7 + vader(industry 分组) -> 与 6XpMb0aG(vader subindustry) 分组不同, 新
    ("C3_earn7+vaderInd_ILLIQ",
     f"add(multiply({TA('historic_earnings_surprise_score_7')}, 0.5), multiply({TA('headline_sentiment_vader_score','industry')}, 0.5))",
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
    with open("mine_v10_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n=== DONE ===")
    for r in results:
        print(r["name"], "->", r.get("alpha_id"))

if __name__ == "__main__":
    main()
