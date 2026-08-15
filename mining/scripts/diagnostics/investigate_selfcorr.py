import os
"""Investigate YPv8gzdv SELF_CORRELATION FAIL: find which submitted alpha it collides with."""
import sys, json
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", r"C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts"))
from ace_lib import start_session

s = start_session()
aid = "YPv8gzdv"

# 1) raw check_submission json
r = s.get("https://api.worldquantbrain.com/alphas/" + aid + "/check")
print("CHECK status:", r.status_code)
j = r.json()
print(json.dumps(j, indent=2, default=str)[:4000])
