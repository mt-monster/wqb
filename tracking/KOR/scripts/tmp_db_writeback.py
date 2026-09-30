# -*- coding: utf-8 -*-
"""KOR SI 专项成果落库（region_id=2, dataset_id=1149 shortinterest38）。"""
import sqlite3, os, sys
REPO = r"D:\coding\traeCN_project\wqb"
DB = os.path.join(REPO, "data", "wqb.db")
REGION, DATASET = 2, 1149
NU, UNI, DELAY, TRUNC = "SLOW_AND_FAST", "TOP600", 1, 0.02

ROWS = [
    ("KPNo2lgl", "hump(group_rank(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), sector), hump=0.003)",
     "ACTIVE", 2.57, 2.09, 0.5504, "KOR SI VecSum Ratio Sector Hump3", 30),
    ("omLjG1M5", "group_rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 1260), 5), sector)",
     "ACTIVE", None, None, None, "KOR SI VecSum Ratio ZScore1260 Sector", 30),
    ("E5pjx9q0", "hump(group_rank(divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001)), industry), hump=0.0025)",
     "UNSUBMITTED", 2.50, 1.85, 0.6002, "KOR SI VecAvg Ratio Industry Hump25", 20),
    ("mLmGQEq9", "hump(group_rank(divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001)), sector), hump=0.0025)",
     "UNSUBMITTED", 2.72, 2.12, 0.6011, "KOR SI VecAvg Ratio Sector Hump25", 20),
    ("d5bMPkWY", "hump(group_rank(divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001)), subindustry), hump=0.003)",
     "UNSUBMITTED", 1.71, 1.19, 0.4365, "KOR SI VecAvg Ratio Subindustry Hump3", 30),
    ("JjNAkqbn", "hump(group_rank(ts_decay_linear(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 500), industry), hump=0.0025)",
     "UNSUBMITTED", 2.31, 1.75, 0.6958, "KOR SI Ratio DecayLinear500 Industry", 30),
    ("RRbOoMNg", "hump(group_rank(ts_decay_linear(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 250), sector), hump=0.0025)",
     "UNSUBMITTED", 2.47, 1.94, 0.7682, "KOR SI Ratio DecayLinear250 Sector", 30),
]


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    ins = upd = 0
    for aid, expr, st, sh, fi, prod, name, dec in ROWS:
        ex = cur.execute("SELECT id FROM alphas WHERE alpha_id=?", (aid,)).fetchone()
        if ex:
            cur.execute("""UPDATE alphas SET expression=?, platform_status=?, sharpe=COALESCE(?,sharpe),
                           fitness=COALESCE(?,fitness), prod_correlation=COALESCE(?,prod_correlation),
                           neutralization=?, updated_at=datetime('now') WHERE alpha_id=?""",
                        (expr, st, sh, fi, prod, NU, aid))
            upd += 1
        else:
            cur.execute("""INSERT INTO alphas (alpha_id, expression, region_id, dataset_id, universe, delay,
                           neutralization, sharpe, fitness, turnover, status, platform_status, prod_correlation,
                           alpha_type, created_at, updated_at)
                           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,datetime('now'),datetime('now'))""",
                        (aid, expr, REGION, DATASET, UNI, DELAY, NU, sh, fi, None,
                         "ACTIVE" if st == "ACTIVE" else "UNSUBMITTED", st, prod, "REGULAR"))
            ins += 1
        print(f"  {aid} [{'UPD' if ex else 'INS'}] status={st} prod={prod}")
    con.commit()
    print(f"committed: inserted={ins} updated={upd}")
    con.close()


main()
