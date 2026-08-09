# -*- coding: utf-8 -*-
"""查询 task1 的 4 条 alpha 在平台上的真实状态,避免重提。"""
import sys, os, json, pickle, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glb_pipeline as gp
from glb_machine_lib import login

BLOCKED = gp._load_blocked_fields()
DONE = gp._load_done_expressions("glb_first")
FO = pickle.load(open(os.path.join(gp.CACHE, "stage1_first_order.pkl"), "rb"))
TASK1 = [x[0] for x in FO if x[0] not in BLOCKED and x[0] not in DONE][:4]
print("task1 expressions:", flush=True)
for e in TASK1:
    print(" ", e, flush=True)

s = login()
# search for recently created alphas containing these field names
import datetime
today = datetime.date.today()
ds = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
de = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

for expr in TASK1:
    field = expr.split("ts_backfill(", 1)[1].split(",", 1)[0] if "ts_backfill(" in expr else expr[:30]
    print(f"\n=== searching field={field} ===", flush=True)
    url = (
        f"https://api.worldquantbrain.com/users/self/alphas?limit=50&offset=0"
        f"&dateCreated>={ds}T00:00:00-04:00"
        f"&dateCreated<{de}T00:00:00-04:00"
        f"&settings.region={gp.REGION}&hidden=false"
    )
    resp = s.get(url, timeout=30)
    if resp.status_code != 200:
        print(f"  HTTP {resp.status_code}", resp.text[:200])
        continue
    data = resp.json()
    hits = [a for a in data.get("results", []) if field in a.get("regular", {}).get("code", "")]
    print(f"  recent hits for {field}: {len(hits)}")
    for h in hits[:5]:
        is_ = h.get("is", {})
        print(f"    id={h.get('id')} status={h.get('status')} sharpe={is_.get('sharpe')} turnover={is_.get('turnover')} created={h.get('dateCreated')}")
        print(f"      code={h.get('regular', {}).get('code', '')[:80]}")
