import sys, json
sys.path.insert(0, r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts")
from ace_lib import start_session, brain_api_url

s = start_session()
BASE = brain_api_url
aid = "KPGvRMg1"
r = s.get(BASE + f"/alphas/{aid}")
print("GET status:", r.status_code)
if r.status_code != 200:
    print(r.text[:300]); sys.exit()
a = r.json()
st = a.get("settings") or {}
print("id:", a.get("id"))
print("stage:", a.get("stage"), "| status:", a.get("status"))
print("region:", st.get("region"), "| universe:", st.get("universe"), "| type:", a.get("type"))
isd = a.get("is") or {}
print("IS sharpe:", isd.get("sharpe"), "| fitness:", isd.get("fitness"))
reg = a.get("regular") or a.get("combo") or ""
if isinstance(reg, dict): reg = reg.get("code","")
print("expr:", str(reg)[:200])
