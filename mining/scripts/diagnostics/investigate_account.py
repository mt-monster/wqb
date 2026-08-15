import os
"""List account's alphas and inspect 6XpMb0aG to understand the full submission picture."""
import sys, json
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import start_session

s = start_session()
BASE = "https://api.worldquantbrain.com"

# Try to list user's own alphas (submitted ones = stage OS or SUBMITTED)
for url in [
    BASE + "/users/self/alphas?limit=100&offset=0",
    BASE + "/alphas?limit=100&offset=0&stage=SUBMITTED",
]:
    r = s.get(url)
    print("GET", url, "->", r.status_code)
    if r.status_code == 200:
        try:
            data = r.json()
            print("  keys:", list(data.keys()))
            items = data.get("results", data.get("alphas", []))
            print("  count:", len(items))
            for it in items[:60]:
                print("   ", it.get("id"), "| stage:", it.get("stage"), "| region:", it.get("settings",{}).get("region"), "| uni:", it.get("settings",{}).get("universe"), "| sharpe:", (it.get("is") or {}).get("sharpe"), "| fitness:", (it.get("is") or {}).get("fitness"))
        except Exception as e:
            print("  parse err", e, r.text[:300])
