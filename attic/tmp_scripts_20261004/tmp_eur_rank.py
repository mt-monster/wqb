"""从 ledger_kv 读取 EUR S0 完整榜单 + datasets 表交叉，输出未测/未判死候选。"""
import json
import sqlite3
import sys

con = sqlite3.connect("data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("PRAGMA table_info(ledger_kv)")
sys.stderr.write("ledger_kv cols=%s\n" % [r[1] for r in cur.fetchall()])
cur.execute("SELECT * FROM ledger_kv WHERE key LIKE '%s0_ranking%' OR key LIKE '%EUR%' LIMIT 200")
for r in cur.fetchall():
    k = r["key"]
    v = r["value"]
    print("KEY:", k, "len", len(str(v)))
