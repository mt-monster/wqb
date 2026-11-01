# -*- coding: utf-8 -*-
"""GBR: 逐数据集回测次数审计 —— 找出真正零回测的数据集。"""
import sqlite3, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DB = r"D:/coding/traeCN_project/wqb/data/wqb.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("=== tables ===")
for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print(" ", r["name"])

print("\n=== expressions columns ===")
cols = [r[1] for r in cur.execute("PRAGMA table_info(expressions)")]
print(" ", cols)

print("\n=== backtest_results columns ===")
cols2 = [r[1] for r in cur.execute("PRAGMA table_info(backtest_results)")]
print(" ", cols2)

# GBR 各数据集：expressions 条数 + 已回测条数
print("\n=== GBR per-dataset expression counts ===")
q = """
SELECT dataset,
       COUNT(*) AS n_expr,
       SUM(CASE WHEN alpha_id IS NOT NULL AND alpha_id <> '' THEN 1 ELSE 0 END) AS n_simmed
FROM expressions
WHERE region = 'GBR'
GROUP BY dataset
ORDER BY n_simmed DESC, n_expr DESC
"""
rows = list(cur.execute(q))
print(f"{'dataset':<34}{'expr':>8}{'simmed':>8}")
for r in rows:
    print(f"{(r['dataset'] or '?'):<34}{r['n_expr']:>8}{r['n_simmed']:>8}")
print(f"\n合计 {len(rows)} 个数据集 / {sum(r['n_expr'] for r in rows)} 条表达式")

# GBR 各数据集：backtest_results 行数
print("\n=== GBR per-dataset backtest_results row counts ===")
q2 = """
SELECT e.dataset AS dataset, COUNT(*) AS n_rows
FROM backtest_results b
JOIN expressions e ON e.id = b.expression_id
WHERE e.region = 'GBR'
GROUP BY e.dataset
ORDER BY n_rows DESC
"""
rows2 = list(cur.execute(q2))
for r in rows2:
    print(f"{(r['dataset'] or '?'):<34}{r['n_rows']:>8}")
print(f"\n合计 {len(rows2)} 个数据集 / {sum(r['n_rows'] for r in rows2)} 行")

con.close()
