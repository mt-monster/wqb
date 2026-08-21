import json
import os

def va(f):
    return "vec_avg(" + f + ")"

def rank_ts(f, z=50):
    return "rank(ts_rank(" + va(f) + ", " + str(z) + "))"

def rank_delta(f, d=22):
    return "rank(ts_delta(" + va(f) + ", " + str(d) + "))"

def rank_zs(f, z=126):
    return "rank(ts_zscore(" + va(f) + ", " + str(z) + "))"

BE = "anl44_best_eps"
BU = "anl44_best_eps_4wk_up"
BD = "anl44_best_eps_4wk_dn"
BC = "anl44_best_eps_chg_pct"
BS = "anl44_best_eps_stddev"
BN = "anl44_best_eps_numest"
SA = "anl44_second_en_sales_value"
EB = "anl44_second_en_ebit_value"
RO = "anl44_second_en_roe_value"

cands = [
    {"id": "w35_01", "expr": rank_ts(BE, 50), "note": "best_eps ts_rank 50"},
    {"id": "w35_02", "expr": rank_delta(BE, 22), "note": "best_eps delta 22"},
    {"id": "w35_03", "expr": rank_ts(BC, 50), "note": "chg_pct ts_rank"},
    {"id": "w35_04", "expr": "subtract(" + rank_ts(BU, 22) + ", " + rank_ts(BD, 22) + ")", "note": "net revision up-dn"},
    {"id": "w35_05", "expr": "rank(ts_rank(divide(" + va(BU) + ", add(add(" + va(BU) + ", " + va(BD) + "), 1)), 50))", "note": "revision ratio"},
    {"id": "w35_06", "expr": rank_zs(BS, 126) + " * -1", "note": "low dispersion"},
    {"id": "w35_07", "expr": rank_ts(BN, 50), "note": "analyst coverage"},
    {"id": "w35_08", "expr": rank_ts(SA, 50), "note": "sales ts_rank"},
    {"id": "w35_09", "expr": rank_ts(RO, 50), "note": "roe ts_rank"},
    {"id": "w35_10", "expr": rank_delta(EB, 22), "note": "ebit delta"},
    {"id": "w35_11", "expr": "add(" + rank_ts(BE, 50) + ", subtract(" + rank_ts(BU, 22) + ", " + rank_ts(BD, 22) + "))", "note": "best_eps+netrev"},
    {"id": "w35_12", "expr": "add(" + rank_ts(BE, 50) + ", " + rank_ts(SA, 50) + ")", "note": "best_eps+sales"},
]

settings = {
    "region": "KOR",
    "universe": "TOP600",
    "delay": 1,
    "decay": 16,
    "neutralization": "SECTOR",
    "truncation": 0.04,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "maxTrade": "OFF",
    "maxPosition": "OFF",
    "language": "FASTEXPR",
}

output = {
    "wave": 35,
    "theme": "KOR analyst44 best_eps+revision",
    "region": "KOR",
    "dataset": "analyst44",
    "settings": settings,
    "candidates": cands,
    "avoid_core": "e73Rw8qg: second_en_eps_value + pretaxprofit_down_4w",
}

outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "KOR", "candidates")
os.makedirs(outdir, exist_ok=True)

with open(os.path.join(outdir, "kor_wave35_items.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

exprs = [{"id": c["id"], "expr": c["expr"], "note": c["note"]} for c in cands]
with open(os.path.join(outdir, "kor_wave35_exprs.json"), "w", encoding="utf-8") as f:
    json.dump(exprs, f, indent=2, ensure_ascii=False)

print("Generated " + str(len(cands)) + " candidates")
for c in cands:
    print("  " + c["id"] + ": " + c["note"])
    print("    " + c["expr"][:90])
