import json, sys
import os
sys.path.insert(0, os.environ.get("WQ_TOOLKIT", os.path.join(os.path.expanduser("~"), ".qoder-cn", "skills", "wq-brain-campaign-toolkit", "scripts")))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from _lib.common import load_credentials
from _lib.api import Api
from _lib.poller import TERMINAL

api = Api()
api.login(*load_credentials())
try:
    d = json.load(api.get("/simulations"))
    sims = d if isinstance(d, list) else d.get("results", [])
    print("total sims listed:", len(sims))
    inflight = [s for s in sims if s.get("status") not in TERMINAL]
    print("non-terminal:", len(inflight))
    for s in inflight[:10]:
        print(" ", s.get("id"), s.get("status"), s.get("progress"), s.get("created"))
except Exception as e:
    print("list err:", e)
