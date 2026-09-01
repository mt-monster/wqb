# -*- coding: utf-8 -*-
"""查询 KOR registry 现状"""
import sqlite3, json, sys
sys.stdout.reconfigure(encoding="utf-8")
conn = sqlite3.connect(r"d:\coding\traeCN_project\wqb\data\wqb.db")
cur = conn.cursor()
cur.execute("SELECT entry_id, layer, payload FROM registry_empirical WHERE region='KOR' AND layer='campaign'")
for eid, layer, payload in cur.fetchall():
    try:
        p = json.loads(payload)
    except Exception:
        p = {}
    print(f"[campaign] {eid} | status={p.get('status','?')} | {p.get('note','')[:120]}")
print("---dead_ends---")
cur.execute("SELECT entry_id, payload FROM registry_empirical WHERE region='KOR' AND layer='dead_end'")
for eid, payload in cur.fetchall():
    try:
        p = json.loads(payload)
    except Exception:
        p = {}
    print(f"[dead_end] {eid} | rule={p.get('rule','')[:100]} | salvage={p.get('salvage','')[:100]}")
print("---wins---")
cur.execute("SELECT entry_id, payload FROM registry_empirical WHERE region='KOR' AND layer='win'")
for eid, payload in cur.fetchall():
    try:
        p = json.loads(payload)
    except Exception:
        p = {}
    print(f"[win] {eid} | {p.get('key','')[:120]}")
conn.close()
