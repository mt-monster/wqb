import os
"""Harvest real field names from account alphas (OS + high-sharpe IS) to pick a 4th-family field."""
import sys, re
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts")))
from ace_lib import start_session, get_simulation_result_json

s = start_session()
BASE = "https://api.worldquantbrain.com"

# Get all user alphas with stage + sharpe, select interesting ones
targets = []
offset = 0
while True:
    r = s.get(BASE + f"/users/self/alphas?limit=100&offset={offset}")
    if r.status_code != 200: break
    data = r.json()
    for it in data.get("results", []):
        sh = (it.get("is") or {}).get("sharpe")
        targets.append((it.get("id"), it.get("stage"), sh, it.get("settings",{}).get("region"), it.get("settings",{}).get("universe")))
    if not data.get("next"): break
    offset += 100
    if offset > 600: break

# also force-include the 6 OS ids (may not be in list)
os_ids = ["6XpMb0aG","vRvg7NzA","MPQVZRnk","KPGvRMg1","gJ8eVmNM","QPGvgO2G"]
seen=set()
sel=[]
for aid,stage,sh,reg,uni in targets:
    if aid in os_ids or (stage=="IS" and sh is not None and sh>=2.0):
        sel.append(aid); seen.add(aid)
for aid in os_ids:
    if aid not in seen: sel.append(aid)

print(f"Harvesting {len(sel)} alphas' expressions...\n")
WQOPS = set("""ts group rank zscore backfill vec_avg signed_power subtract multiply add scale decay
stddev mean corr divide minus log power abs winsorize ts_zscore ts_backfill ts_avg ts_mean
ts_std_dev ts_rank ts_delta ts_covariance ts_decay_linear ts_arg_max ts_arg_min if_else
where normalize quantile bucket rank power square sqrt exp sign _ """.split())
fields=set()
for aid in sel:
    j=get_simulation_result_json(s,aid)
    if not j: continue
    code=""
    for k in ("regular","combo","selection"):
        v=j.get(k)
        if isinstance(v,dict): code+=" "+(v.get("code") or "")
        elif isinstance(v,str): code+=" "+v
    toks=re.findall(r"[a-z][a-z0-9_]+", code)
    real=[t for t in toks if t not in WQOPS and "_" in t and not t.startswith("ts_") and len(t)>3]
    for t in real: fields.add(t)
    print(f"{aid} [{j.get('stage')}] {j.get('settings',{}).get('region')}/{j.get('settings',{}).get('universe')} sharpe={(j.get('is') or {}).get('sharpe')}")
    print(f"   {code.strip()[:160]}")

print("\n=== CANDIDATE REAL FIELDS (with underscore, not WQ operator) ===")
for f in sorted(fields):
    print("  ", f)
