# -*- coding: utf-8 -*-
"""列出指定 (region, dataset) 的 prod 未测达标候选全量"""
import sqlite3, re, sys
DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
MIX = re.compile(r"add\s*\(\s*multiply|multiply\s*\(\s*0?\.\d|\*\s*0\.\d+\s*\+|\+\s*0\.\d+\s*\*", re.I)
c = sqlite3.connect(DB); cur = c.cursor()
cur.execute("SELECT id,name FROM regions"); RMAP={r[0]:r[1] for r in cur.fetchall()}

targets = [(5,1358),(5,41),(5,1337),(3,1647),(3,1670),(2,21),(10,1902)]
for reg, ds in targets:
    cur.execute("""SELECT alpha_id, expression, sharpe, fitness, two_year_sharpe, turnover, universe, neutralization
      FROM alphas WHERE region_id=? AND dataset_id=? AND sharpe>=1.58 AND two_year_sharpe>=1.58
        AND fitness>=1.0 AND prod_correlation IS NULL AND soft_deleted=0
      ORDER BY sharpe DESC LIMIT 12""", (reg, ds))
    rows=[r for r in cur.fetchall() if (r[1] or '').strip() and not MIX.search(r[1] or '')]
    if not rows: continue
    print(f"\n########## {RMAP.get(reg)} ds={ds}  ({len(rows)} shown) ##########")
    for r in rows:
        print(f"  {r[0]} S={r[2]} F={r[3]} 2Y={r[4]} TO={r[5]:.3f} {r[6]}/{r[7]}")
        print(f"      {(r[1] or '')[:200]}")
