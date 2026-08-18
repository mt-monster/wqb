import os
"""Harvest ALL real field tokens from account alphas to build a real-field dictionary,
then identify USA-valid, non-saturated candidates for the 4th alpha."""
import sys, re, json, time, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts")))
from ace_lib import start_session, brain_api_url

s = start_session()
all_expr = []
offset = 0
LIM = 100
while True:
    url = brain_api_url + f"/users/self/alphas?limit={LIM}&offset={offset}"
    r = s.get(url)
    if r.status_code // 100 != 2:
        print("HTTP", r.status_code, r.text[:200]); break
    data = r.json()
    items = data.get("results", data.get("alphas", []))
    if not items: break
    print(f"offset {offset}: {len(items)} alphas", flush=True)
    for a in items:
        reg = a.get("regular") or ""
        if not reg and a.get("type")=="SUPER":
            reg = a.get("combo") or ""
        all_expr.append((a.get("id"), a.get("region"), (a.get("settings") or {}).get("universe"), str(reg)))
    if len(items) < LIM: break
    offset += LIM
    if offset >= 1000: break
    time.sleep(0.3)

print(f"TOTAL alphas with expr: {len(all_expr)}", flush=True)

tok_re = re.compile(r"[a-zA-Z]+(?:_\w+)+")
FNS = {"group_rank","ts_zscore","ts_backfill","vec_avg","rank","ts_delay","ts_decay_linear",
       "signed_power","subtract","winsorize","ts_ir","ts_mean","ts_std_dev","ts_sum","scale",
       "tanh","log","abs","ts_delta","if_else","stddev","mean","correlation","regression",
       "sigmoid","zscore","normalize","div","mul","add","pow","ts_regression","group_neutralize",
       "group_zscore","group_mean","group_stddev","ts_covariance","ts_correlation","decay_linear"}
fields = {}
for aid, region, uni, reg in all_expr:
    for m in tok_re.findall(reg):
        if m.lower() in FNS: continue
        fields.setdefault(m, set()).add((region,uni))

print(f"\n=== UNIQUE FIELD-LIKE TOKENS ({len(fields)}) ===", flush=True)
for f, occ in sorted(fields.items(), key=lambda x:-len(x[1])):
    regs = sorted({r for r,u in occ})
    unis = sorted({u for r,u in occ})
    print(f"  {f:48s} n={len(occ):3d} regions={regs} unis={unis}", flush=True)

with open(os.path.join(ROOT, "data_ref", "all_fields.json"), "w") as f:
    json.dump({k:sorted(list(v)) for k,v in fields.items()}, f, indent=2)
print("\nsaved all_fields.json", flush=True)
