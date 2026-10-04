"""列当前账号在飞仿真（占槽检查）。"""
import json
import os
import sys

ROOT = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts"))
from _lib.api import Api, api_call  # noqa: E402
from _lib.common import load_credentials  # noqa: E402

api = Api()
api.login(*load_credentials())
try:
    d = json.load(api.get("/simulations?status=RUNNING&limit=20"))
except Exception as e:
    print("ERR", e)
    raise SystemExit(1)
rows = d.get("results") or d.get("simulations") or []
if isinstance(rows, dict):
    rows = [rows]
print("RUNNING:", len(rows))
for r in rows:
    print(" ", r.get("id"), r.get("status"), str(r.get("progress"))[:20], (r.get("alpha") or "-"))
