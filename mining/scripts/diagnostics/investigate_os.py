import os
"""Find all OS/submitted alphas in account + inspect 6XpMb0aG (the collision target)."""
import sys, json
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts")))
from ace_lib import start_session, get_simulation_result_json

s = start_session()
BASE = "https://api.worldquantbrain.com"

# paginate all user alphas, print only non-IS (submitted) ones
all_ids = []
offset = 0
while True:
    r = s.get(BASE + f"/users/self/alphas?limit=100&offset={offset}")
    if r.status_code != 200:
        print("err", r.status_code, r.text[:200]); break
    data = r.json()
    items = data.get("results", [])
    if not items: break
    for it in items:
        all_ids.append((it.get("id"), it.get("stage"), (it.get("is") or {}).get("sharpe"), (it.get("is") or {}).get("fitness")))
    if not data.get("next"): break
    offset += 100
    if offset > 500: break

print(f"TOTAL alphas: {len(all_ids)}")
print("Non-IS (submitted/OS) alphas:")
for aid, stage, sh, fit in all_ids:
    if stage != "IS":
        print(f"  {aid} | stage={stage} | sharpe={sh} | fitness={fit}")

# Inspect 6XpMb0aG directly
print("\n=== 6XpMb0aG detail ===")
j = get_simulation_result_json(s, "6XpMb0aG")
if j:
    print("  stage:", j.get("stage"))
    print("  region/uni:", j.get("settings",{}).get("region"), j.get("settings",{}).get("universe"))
    print("  IS sharpe:", (j.get("is") or {}).get("sharpe"), "fitness:", (j.get("is") or {}).get("fitness"))
    print("  name:", j.get("name"))
else:
    print("  NOT FOUND (maybe not owned by this user)")
