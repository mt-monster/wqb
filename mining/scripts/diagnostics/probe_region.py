import os
import sys, json
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import start_session

s = start_session()
BASE = "https://api.worldquantbrain.com"

# find a USA alpha to inspect JSON structure (region key)
for offset in [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]:
    r = s.get(BASE + f"/users/self/alphas?limit=100&offset={offset}")
    if r.status_code != 200:
        print("GET fail", r.status_code, r.text[:200]); break
    items = r.json().get("results", [])
    if not items: break
    for a in items:
        st = a.get("settings") or {}
        if st.get("region") == "USA":
            print("FOUND USA alpha id=", a.get("id"))
            print("KEYS:", list(a.keys()))
            print("  region=", st.get("region"), "uni=", st.get("universe"), "type=", a.get("type"))
            reg = a.get("regular") or a.get("combo") or ""
            if isinstance(reg, dict): reg = reg.get("code","")
            print("  expr=", str(reg)[:200])
            sys.exit(0)
    print(f"offset {offset}: scanned 100, no USA yet")
print("no USA alpha found in first 1000")
