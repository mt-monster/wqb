import os
import sys, json, re, time
sys.path.insert(0, os.environ.get("WQ_ACE_LIB", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills", "brain-simAlphasinBatch-and-track", "scripts")))
from ace_lib import start_session

s = start_session()
BASE = "https://api.worldquantbrain.com"

# operators/function names to exclude (not data fields)
FUNCS = set("""ts_rank ts_zscore ts_backfill vec_avg group_rank rank decay_linear ts_decay_linear
ts_mean ts_std_dev ts_ir ts_corr ts_covariance ts_product ts_sum ts_delta ts_arg_max ts_arg_min
ts_min ts_max ts_scale ts_sign ts_log ts_sqrt signed_power power subtract add multiply divide
abs winsorize ffill scale normalize if_else lag correlation row_constant identity
sigmoid tanh clip percentile quantile bucket between reverse sign norm improve made date shift
where is_nan nan_to_zero rank_dense rank_percentile vector_neutralize group_neutralize
ts_av_diff ts_av_diff_abs if is_null null_to_zero""".split())

TOKEN = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

usa_exprs = []
offset = 0
LIM = 100
while offset < 2000:
    r = s.get(BASE + f"/users/self/alphas?limit={LIM}&offset={offset}")
    if r.status_code != 200:
        print("GET fail", r.status_code, r.text[:150]); break
    items = r.json().get("results", [])
    if not items: break
    cnt_usa = 0
    for a in items:
        st = a.get("settings") or {}
        if st.get("region") != "USA": continue
        cnt_usa += 1
        reg = a.get("regular") or a.get("combo") or ""
        if isinstance(reg, dict): reg = reg.get("code", "")
        reg = str(reg)
        if reg:
            usa_exprs.append((a.get("id"), st.get("universe"), reg))
    print(f"offset {offset}: {len(items)} alphas, {cnt_usa} USA")
    if len(items) < LIM: break
    offset += LIM
    time.sleep(0.2)

print("TOTAL USA exprs:", len(usa_exprs))

# extract field-like tokens with universe context
from collections import defaultdict
field_uni = defaultdict(set)
field_count = defaultdict(int)
for aid, uni, reg in usa_exprs:
    toks = set(TOKEN.findall(reg))
    for t in toks:
        if t in FUNCS: continue
        if t in ("x","y","a","b","c","d","e","f","g","i","j","k","n","w","t","p","s","u","v","z"): continue
        field_uni[t].add(uni)
        field_count[t] += 1

# sort by usage count
rows = sorted(field_count.items(), key=lambda kv: -kv[1])
print("\n=== USA FIELD TOKENS (%d) ===" % len(rows))
for t, c in rows:
    print(f"  {t:55s} n={c:3d} unis={sorted(field_uni[t])}")
