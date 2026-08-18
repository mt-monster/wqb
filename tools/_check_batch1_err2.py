import json, sys
sys.path.insert(0, r"C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts")
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from _lib.common import load_credentials
from _lib.api import Api

api = Api()
api.login(*load_credentials())
msid = "4jBXadf6V4D9byznuMUQ51L"
ms = json.load(api.get(f"/simulations/{msid}"))
for c in ms.get("children", []):
    try:
        sim = json.load(api.get(f"/simulations/{c}"))
        if sim.get("status") in ("ERROR", "CANCELLED"):
            print("==== child", c, sim.get("status"))
            print(json.dumps(sim, ensure_ascii=False, indent=1)[:1200])
    except Exception as e:
        print(c, "fetch err", e)
