"""列出 EUR 的死路家族（registry_empirical.dead_end 层）。"""
import sqlite3
import sys

con = sqlite3.connect("data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("PRAGMA table_info(registry_empirical)")
cols = [r[1] for r in cur.fetchall()]
sys.stderr.write("cols=%s\n" % cols)
q = "SELECT * FROM registry_empirical WHERE region='EUR'"
try:
    cur.execute(q)
except Exception:
    q = "SELECT * FROM registry_empirical WHERE lower(region)='eur'"
    cur.execute(q)
rows = [dict(r) for r in cur.fetchall()]
print("total EUR rows:", len(rows))
for r in rows:
    print("-", r.get("family") or r.get("key"), "|", str(r.get("reason"))[:120])
