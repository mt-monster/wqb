import json, sys
sys.path.insert(0, r"C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts")
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from _lib.common import load_credentials
from _lib.api import Api

api = Api()
api.login(*load_credentials())
msid = "4jBXadf6V4D9byznuMUQ51L"
ms = json.load(api.get(f"/simulations/{msid}"))
print("ms status:", ms.get("status"))
print("error:", str(ms.get("error"))[:200])
print("children:", len(ms.get("children", [])))
for c in ms.get("children", []):
    try:
        sim = json.load(api.get(f"/simulations/{c}"))
        reg = sim.get("regular", {})
        code = reg.get("expression", "") if isinstance(reg, dict) else str(reg)
        print("-", c, sim.get("status"), "|", code[:70], "| err:", str(sim.get("error"))[:150])
    except Exception as e:
        print("-", c, "fetch err", e)
