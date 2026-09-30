# -*- coding: utf-8 -*-
"""盘点：符合提交四闸 + 无混腿的候选"""
import sqlite3, re, json

DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
c = sqlite3.connect(DB)
cur = c.cursor()

# 混腿检测：add(multiply(...)) 或 显式 0.x* 加权
MIX_PAT = re.compile(r"add\s*\(\s*multiply|multiply\s*\(\s*0?\.\d|\*\s*0\.\d+\s*\+|\+\s*0\.\d+\s*\*", re.I)

cur.execute("""
  SELECT alpha_id, expression, sharpe, fitness, two_year_sharpe, region_id, dataset_id,
         platform_status, status, prod_correlation, turnover, sub_universe_sharpe
  FROM alphas
  WHERE sharpe >= 1.58 AND two_year_sharpe >= 1.58 AND fitness >= 1.0
    AND soft_deleted = 0
  ORDER BY sharpe DESC
""")
rows = cur.fetchall()
print(f"通过 S>=1.58 & 2Y>=1.58 & F>=1.0 的总数: {len(rows)}\n")

clean, mixed = [], []
for r in rows:
    expr = r[1] or ""
    (mixed if MIX_PAT.search(expr) else clean).append(r)

print(f"  其中 无混腿(疑似合规): {len(clean)}")
print(f"       含混腿(违规)    : {len(mixed)}\n")

print("=== 无混腿候选（按 S 降序，Top 30）===")
for r in clean[:30]:
    aid, expr, s, f, y2, reg, ds, pst, st, prod, to, sub = r
    print(f"{aid} S={s} F={f} 2Y={y2} reg={reg} ds={ds} {pst}/{st} prod={prod} TO={to}")
    print(f"    {expr[:190]}")
