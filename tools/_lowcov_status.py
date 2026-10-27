# -*- coding: utf-8 -*-
"""看低覆盖波（26 集）已完成部分的判定与指标。"""
import collections
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOW = ("model25,multifactor_return_pred,other296,pv29,other335,behavioral_signals,"
       "stock_alpha_model,model138,model135,analyst_base_ref,model68,event_stock_model,"
       "analyst_factor_signals,insider_feats,other545,other315,other327,analyst15,"
       "fundamental1,model140,earningscall_sentiment,pv87,fundamental6,analyst14,"
       "fundamental28,analyst7").split(",")

res = json.load(open(os.path.join(ROOT, "results",
                                  "full_template_campaign_results.json"),
                     encoding="utf-8")).get("results") or {}
con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
cat = {d: (c or "?").upper() for d, c in
       con.execute("select dataset, category from dataset_profile where region='EUR'")}
con.close()

rows = []
for ds in LOW:
    v = res.get(ds) or {}
    if v.get("verdict"):
        rows.append((ds, cat.get(ds, "?"), v.get("verdict"), v.get("max_s"),
                     v.get("max_2y"), v.get("n_alphas"), v.get("prod_top")))

print("低覆盖波已完成 {}/26".format(len(rows)))
print("判定:", dict(collections.Counter(r[2] for r in rows)))
print()
rows.sort(key=lambda r: -(r[3] or -9))
for r in rows:
    print("  {:<24}{:<13}{:<22}S={} 2Y={} a={} prod={}".format(
        r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
