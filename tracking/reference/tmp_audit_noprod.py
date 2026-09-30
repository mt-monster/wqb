# -*- coding: utf-8 -*-
"""筛出：达标 + 无混腿 + prod未测（None）+ 已回测(有alpha) 的候选，按区域/数据集汇总"""
import sqlite3, re, json
from collections import defaultdict

DB = r"D:\coding\traeCN_project\wqb\data\wqb.db"
c = sqlite3.connect(DB)
cur = c.cursor()

MIX_PAT = re.compile(r"add\s*\(\s*multiply|multiply\s*\(\s*0?\.\d|\*\s*0\.\d+\s*\+|\+\s*0\.\d+\s*\*", re.I)

# region 映射
cur.execute("SELECT id, name FROM regions")
RMAP = {r[0]: r[1] for r in cur.fetchall()}

cur.execute("""
  SELECT alpha_id, expression, sharpe, fitness, two_year_sharpe, region_id, dataset_id,
         platform_status, status, prod_correlation, turnover
  FROM alphas
  WHERE sharpe >= 1.58 AND two_year_sharpe >= 1.58 AND fitness >= 1.0
    AND soft_deleted = 0 AND prod_correlation IS NULL
  ORDER BY region_id, sharpe DESC
""")
rows = [r for r in cur.fetchall() if not MIX_PAT.search(r[1] or "") and (r[1] or "").strip()]

print(f"prod未测 + 无混腿 + 达标 = {len(rows)}\n")
buckets = defaultdict(list)
for r in rows:
    buckets[(RMAP.get(r[5], r[5]), r[6])].append(r)

print("=== 按 (region, dataset) 汇总（Top 20 桶）===")
for (reg, ds), lst in sorted(buckets.items(), key=lambda kv: -len(kv[1]))[:20]:
    best = lst[0]
    print(f"  {reg:4s} ds={str(ds):8s} n={len(lst):3d} best_S={best[2]} best_2Y={best[4]} best_F={best[3]}")
    print(f"        {best[0]}: {(best[1] or '')[:150]}")
