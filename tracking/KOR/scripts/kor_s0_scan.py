"""KOR S0 dataset scan: score every KOR/TOP600 dataset for mining potential.

Excludes datasets already 'lit' (>=3 submitted REGULAR alphas) and previously
triaged/dead ones. Writes whitelist to <repo>/logs/_kor_s0_whitelist.json.

用法（仓库根下执行）：
  $WQ_PY tracking/KOR/scripts/kor_s0_scan.py

⚠ 下面的 `DS` 清单是 **2026-10-15 `get_datasets` 的一次性快照**（不是实时拉取）。
  平台数据集会上下架、alphaCount 会涨，所以：换轮战役先重拉一次 `get_datasets`
  再评分，别把这份表当现状 —— 本仓已有「本地库含已下架数据集」的实证
  （`ml_factor_proj` 本地 333 字段 vs 平台 0 字段）。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _repo_path import REPO as _REPO_PATH  # noqa: E402

REPO = str(_REPO_PATH)

# KOR/TOP600 dataset inventory (get_datasets, 2026-10-15)
# id, category, coverage, fieldCount, userCount, alphaCount, valueScore
DS = [
    ("acquisition_model", "other", 0.9937, 15, 62, 106, 5.0),
    ("ai_news_scores", "other", 0.373, 103, 26, 36, 6.0),
    ("continuation_score", "pv", 1.0, 560, 240, 444, 4.0),
    ("dl_riskfree_returns", "other", 0.9095, 57, 1111, 7026, 2.0),
    ("earnings3", "earnings", 0.6603, 8, 635, 2599, 1.0),
    ("equity_forum_data", "other", 0.8948, 6, 9, 13, 6.0),
    ("event_relation", "other", 0.3392, 3, 3, 3, 6.0),
    ("fund_holdings_panel", "institutions", 0.8093, 30, 108, 210, 4.0),
    ("fundamental17", "fundamental", 0.8896, 373, 1130, 4568, 2.0),
    ("fundamental21", "fundamental", 0.6444, 153, 206, 445, 4.0),
    ("fundamental23", "fundamental", 0.7092, 381, 1272, 7572, 2.0),
    ("fundamental28", "fundamental", 0.5, 535, 668, 3202, 2.0),
    ("fundamental4", "fundamental", 0.332, 1, 5, 5, 5.0),
    ("fundamental44", "fundamental", 0.8984, 12, 140, 505, 3.0),
    ("fundamental6", "fundamental", 0.5, 259, 473, 2037, 2.0),
    ("fundamental86", "fundamental", 0.8345, 10, 65, 118, 3.0),
    ("fundamental89", "fundamental", 0.742, 368, 80, 148, 4.0),
    ("fundamental90", "fundamental", 0.7202, 59, 98, 153, 5.0),
    ("fundamental93", "fundamental", 0.7552, 46, 40, 63, 4.0),
    ("fundamental94", "fundamental", 0.8558, 215, 532, 1381, 2.0),
    ("imbalance5", "imbalance", 0.8559, 2, 473, 1332, 1.0),
    ("insider_feats", "other", 0.6636, 31, 417, 1692, 3.0),
    ("insiders1", "insiders", 0.3526, 9, 198, 544, 3.0),
    ("insiders5", "insiders", 0.8918, 53, 785, 4874, 2.0),
    ("institutions6", "institutions", 0.9996, 11, 301, 975, 2.0),
    ("intraday_pv_feats", "pv", 0.9925, 574, 389, 1141, 3.0),
    ("macro63", "macro", 1.0, 1, 80, 188, 3.0),
    ("mmp_nlp_sentiment", "other", 0.6187, 521, 40, 68, 6.0),
    ("model56", "fundamental", 0.8257, 9, 70, 158, 3.0),
    ("news_sentiment_dl", "other", 0.2588, 22, 2, 2, 7.0),
    ("news_sentiment_nlp", "other", 0.2767, 23, 4, 4, 7.0),
    ("news_sentiment_transfer", "sentiment", 0.9654, 23, 116, 209, 4.0),
    ("other100", "socialmedia", 1.0, 1, 154, 398, 2.0),
    ("other106", "macro", 0.4038, 15, 116, 302, 4.0),
    ("other315", "other", 0.4022, 32, 155, 471, 4.0),
    ("other323", "other", 1.0, 11, 276, 1035, 3.0),
    ("other327", "other", 0.7866, 3, 25, 31, 5.0),
    ("other335", "other", 0.59, 10, 377, 1039, 2.0),
    ("other395", "fundamental", 0.5317, 368, 74, 146, 5.0),
    ("other401", "fundamental", 0.6058, 57, 73, 356, 4.0),
    ("other424", "other", 0.5919, 3, 30, 43, 5.0),
    ("other436", "other", 0.57, 3, 12, 15, 6.0),
    ("other452", "fundamental", 0.5751, 46, 24, 40, 5.0),
    ("other455", "other", 0.8973, 1500, 135, 547, 5.0),
    ("other466", "fundamental", 0.8269, 177, 884, 5583, 1.0),
    ("other475", "other", 0.357, 1, 217, 602, 2.0),
    ("other496", "other", 0.8006, 104, 231, 840, 4.0),
    ("other532", "other", 0.9956, 8, 462, 1852, 3.0),
    ("other545", "other", 0.8393, 4, 26, 43, 5.0),
    ("other546", "other", 0.5632, 10, 7, 8, 7.0),
    ("other553", "sentiment", 0.6243, 21, 62, 88, 5.0),
    ("other567", "other", 0.2571, 2, 12, 16, 6.0),
    ("other571", "other", 0.2649, 23, 49, 62, 5.0),
    ("other635", "other", 0.3011, 6, 3, 5, 6.0),
    ("other695", "other", 0.4886, 3, 76, 158, 4.0),
    ("other78", "other", 0.7925, 11, 27, 68, 6.0),
    ("pattern_scores", "pv", 1.0, 504, 161, 299, 4.0),
    ("pv1", "pv", 1.0, 24, 3265, 87050, 1.0),
    ("pv103", "pv", 1.0, 7, 95, 160, 3.0),
    ("pv106", "pv", 1.0, 29, 339, 969, 2.0),
    ("pv109", "pv", 0.222, 25, 4, 8, 5.0),
    ("pv13", "pv", 0.8191, 36, 267, 1025, 2.0),
    ("pv14", "pv", 0.8911, 2, 64, 116, 2.0),
    ("pv149", "pv", 1.0, 2, 2, 3, 6.0),
    ("pv173", "pv", 0.1993, 21, 6, 6, 5.0),
    ("pv20", "pv", 1.0, 6, 26, 37, 4.0),
    ("pv29", "pv", 0.6678, 40, 329, 6212, 1.0),
    ("pv30", "pv", 0.9418, 690, 268, 4290, 2.0),
    ("pv37", "pv", 0.734, 873, 590, 2326, 2.0),
    ("pv47", "pv", 0.9456, 5, 98, 158, 2.0),
    ("pv70", "pv", 0.1906, 33, 6, 15, 6.0),
    ("risk59", "risk", 0.9806, 16, 217, 556, 2.0),
    ("risk60", "risk", 1.0, 5, 80, 208, 3.0),
    ("risk68", "risk", 0.9914, 5, 329, 732, 2.0),
    ("risk70", "risk", 0.9798, 96, 1194, 7884, 1.0),
    ("risk71", "risk", 0.6658, 7, 145, 334, 2.0),
    ("risk72", "risk", 0.6246, 5, 160, 395, 2.0),
    ("risk88", "risk", 0.9727, 64, 482, 1391, 2.0),
    ("sentiment21", "sentiment", 0.3812, 138, 53, 93, 6.0),
    ("sentiment23", "sentiment", 0.2648, 156, 34, 51, 6.0),
    ("sentiment26", "sentiment", 0.357, 19, 27, 46, 5.0),
    ("sentiment27", "sentiment", 0.3989, 29, 435, 1863, 2.0),
    ("shortinterest3", "shortinterest", 0.9238, 56, 318, 1422, 3.0),
    ("shortinterest38", "shortinterest", 0.9953, 88, 674, 2656, 3.0),
    ("shortinterest5", "shortinterest", 1.0, 3, 36, 73, 5.0),
    ("socialmedia39", "socialmedia", 1.0, 1, 179, 572, 1.0),
    ("univ1", "pv", 1.0, 1, 3, 16, 4.0),
]

LIT = {"shortinterest38": 5, "other466": 5}  # >=3 submitted REGULAR

DEAD = {
    "pv29": "pyramid duplicate of fundamentals",
    "macro63": "1 field, index membership only",
    "other106": "KOSPI index membership, near-static (cov 0.404)",
    "shortinterest5": "CN/HK price limit, not KOR applicable -> constants",
    "fundamental4": "HK-only, 1 field",
    "imbalance5": "2 fields, identifier mapping",
    "other100": "1 field co-search",
    "socialmedia39": "1 field co-search",
    "univ1": "1 field",
    "pv14": "2 fields",
    "pv149": "2 fields holiday calendar",
    "pv1": "87050 alphas - fully saturated",
    "pv30": "PCA industry labels, no signal",
    "pattern_scores": "chart pattern family triple-dead (RULES G)",
    "continuation_score": "chart pattern family triple-dead (RULES G)",
    "risk70": "7884 alphas, saturated",
    "pv37": "interval data low TO",
    "insiders5": "TO<0.31 near-static in KOR",
    "fund_holdings_panel": "TO<0.1 in KOR",
    "sentiment27": "1863 alphas + website rank; dual-window product killed S",
    "earnings3": "8 fields identifier mapping",
    "institutions6": "ownership levels only",
}


def score(d):
    _, cat, cov, nf, uc, ac, vs = d
    s = vs * 2.0
    if cov < 0.30:
        s -= 3.0
    elif cov < 0.45:
        s -= 0.5
    elif cov > 0.97:
        s -= 0.5
    else:
        s += 1.5
    if nf < 3:
        s -= 2.5
    elif nf >= 20:
        s += 2.0
    elif nf >= 8:
        s += 1.5
    if ac <= 20:
        s += 4.0
    elif ac <= 200:
        s += 3.0
    elif ac <= 600:
        s += 1.5
    elif ac <= 1500:
        s += 0.5
    elif ac <= 3000:
        s -= 1.0
    else:
        s -= 3.0
    if uc <= 10:
        s += 2.0
    elif uc <= 60:
        s += 1.5
    elif uc <= 300:
        s += 0.5
    else:
        s -= 1.0
    return round(s, 2)


def main():
    rows = []
    for d in DS:
        did = d[0]
        if did in LIT:
            rows.append((did, d[1], score(d), d[3], d[5], d[6], "LIT-EXCLUDED"))
        elif did in DEAD:
            rows.append((did, d[1], score(d), d[3], d[5], d[6], "DEAD: " + DEAD[did]))
        else:
            rows.append((did, d[1], score(d), d[3], d[5], d[6], "candidate"))
    cand = sorted([r for r in rows if r[6] == "candidate"], key=lambda r: -r[2])
    ndead = len([r for r in rows if r[6].startswith("DEAD")])
    print(f"KOR total={len(DS)}  lit={len(LIT)}  dead/triaged={ndead}  candidates={len(cand)}\n")
    print(f"{'rank':<5}{'dataset':<26}{'cat':<14}{'score':>6}{'nfld':>6}{'aCnt':>7}{'vS':>5}")
    for i, r in enumerate(cand, 1):
        print(f"{i:<5}{r[0]:<26}{r[1]:<14}{r[2]:>6}{r[3]:>6}{r[4]:>7}{r[5]:>5}")
    out = os.path.join(REPO, "logs", "_kor_s0_whitelist.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(
            [{"dataset": r[0], "category": r[1], "score": r[2], "nfields": r[3],
              "alphaCount": r[4], "valueScore": r[5]} for r in cand],
            f, ensure_ascii=False, indent=1)
    print(f"\nwhitelist -> {out}")


if __name__ == "__main__":
    main()