"""打印 EUR 死路的 payload 详情（截断）。"""
import json
import sqlite3
import sys

con = sqlite3.connect("data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
KEY = sys.argv[1] if len(sys.argv) > 1 else None
cur.execute("SELECT family, payload, dead_at FROM registry_empirical WHERE region='EUR'")
for r in cur.fetchall():
    fam = str(r["family"] or "")
    if KEY and KEY.lower() not in fam.lower():
        continue
    print("###", fam, "|", r["dead_at"])
    print(str(r["payload"])[:600])
    print()
