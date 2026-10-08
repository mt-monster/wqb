"""EUR 白名单三重交集：S0 tier1/2 ∩ 未测 ∩ 非 dead_end。"""
import ast
import json
import re
import sqlite3

con = sqlite3.connect("data/wqb.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute("SELECT value FROM ledger_kv WHERE key='s0_ranking' ORDER BY id DESC LIMIT 1")
val = cur.fetchone()["value"]
try:
    data = json.loads(val)
except Exception:
    data = ast.literal_eval(val)
ranking = data.get("ranking") or []

# 已测数据集
cur.execute("SELECT dataset, COUNT(*) n FROM expressions WHERE region='EUR' GROUP BY dataset")
tested = {r["dataset"]: r["n"] for r in cur.fetchall() if r["dataset"]}

# 死路家族文本
cur.execute("SELECT family, payload FROM registry_empirical WHERE region='EUR'")
dead_text = " || ".join(
    f"{r['family'] or ''} {r['payload'] or ''}" for r in cur.fetchall()
).lower()
# 也纳入 dead_datasets
cur.execute("SELECT value FROM ledger_kv WHERE key LIKE '%dead%' AND region='EUR'")
dd = " ".join(str(r["value"]) for r in cur.fetchall()).lower()
dead_all = dead_text + " " + dd

# 死路里出现的 dataset id 集合（按已知 id 匹配）
all_ds_ids = set()
for r in ranking:
    did = r.get("dataset") or r.get("id")
    if did:
        all_ds_ids.add(did)
for k in list(tested):
    all_ds_ids.add(k)

def is_dead(ds):
    return ds.lower() in dead_all

print(f"{'rank':>4} {'tier':6} {'dataset':32s} {'score':>7} {'exprs':>6} dead")
white = []
for i, r in enumerate(ranking, 1):
    ds = r.get("dataset") or r.get("id")
    tier = r.get("tier")
    if tier not in ("tier1", "tier2"):
        continue
    n = tested.get(ds, 0)
    d = is_dead(ds)
    if n == 0 and not d:
        white.append((i, tier, ds, r.get("score"), r.get("category")))
    print(f"{i:>4} {tier:6} {str(ds):32s} {r.get('score'):>7} {n:>6} {'DEAD' if d else ''}")

print("\n===== 白名单（未测 且 非死路）=====")
for i, tier, ds, sc, cat in white:
    print(f"{i:>4} {tier:6} {ds:32s} score={sc} cat={cat}")
