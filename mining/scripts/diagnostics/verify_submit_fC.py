import os
"""Verify fC (mL5d17Z9) full RA checks, then submit to platform."""
import sys, json
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts")))
from ace_lib import start_session, get_check_submission, submit_alpha, get_simulation_result_json

s = start_session()
aid = "mL5d17Z9"
print(f"=== FULL CHECK for {aid} ===")
df = get_check_submission(s, aid)
for _, r in df.iterrows():
    print(f"  [{r['result']}] {r['name']}  value={r.get('value')} limit={r.get('limit')}")

# decide
fails = df[(df['result']=='FAIL') & (~df['name'].isin(['ALREADY_SUBMITTED']))]
pending = df[df['result']=='PENDING']
print(f"\nHard FAILs: {list(fails['name'])}")
print(f"PENDING (expected PROD_CORRELATION): {list(pending['name'])}")

if len(fails)==0:
    print("\n>>> All hard gates pass. Submitting...")
    ok = submit_alpha(s, aid)
    print(f">>> submit_alpha returned: {ok}")
    # re-check stage
    import time
    for _ in range(10):
        j = get_simulation_result_json(s, aid)
        st = j.get("stage")
        print(f"    stage now: {st}")
        if st in ("SUBMITTED","OS","PENDING"): break
        time.sleep(5)
else:
    print("\n>>> Hard gates NOT all passed; NOT submitting.")
