"""查 EUR expressions 里 risk62 / risk70 / risk88 / risk59 的历史探测。"""
import sqlite3
import sys

con = sqlite3.connect("data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
ds = sys.argv[1] if len(sys.argv) > 1 else "risk62"
cur.execute(
    "SELECT expression, alpha_id, sharpe, fitness, status FROM expressions "
    "WHERE region='EUR' AND dataset=? ORDER BY sharpe DESC",
    (ds,),
)
for r in cur.fetchall():
    print(f"[{r['alpha_id'] or '-'}] S={r['sharpe']} F={r['fitness']} {r['status']}")
    print("   ", r["expression"][:200])
