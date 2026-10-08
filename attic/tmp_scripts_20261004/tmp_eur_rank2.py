"""导出 EUR S0 完整 47 榜单（取最新一条 s0_ranking）。"""
import json
import sqlite3
import sys

con = sqlite3.connect("data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("SELECT id, value, updated_at FROM ledger_kv WHERE key='s0_ranking' ORDER BY id DESC LIMIT 1")
row = cur.fetchone()
val = row["value"]
try:
    data = json.loads(val)
except Exception:
    # 可能是 python repr
    import ast

    data = ast.literal_eval(val)
print("updated_at:", row["updated_at"], "type:", type(data))
if isinstance(data, dict):
    print("keys:", list(data.keys())[:20])
    rows = data.get("ranking") or []
else:
    rows = data
print("N=", len(rows))
for i, r in enumerate(rows, 1):
    if isinstance(r, dict):
        print(i, r.get("dataset") or r.get("id"), r.get("tier"), r.get("score"), r.get("category"),
              "ac=", r.get("alpha_count"), "fc=", r.get("field_count"), "cov=", r.get("coverage"))
    else:
        print(i, r)
