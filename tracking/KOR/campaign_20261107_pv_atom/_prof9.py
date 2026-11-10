import json, sys, collections, re
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or []
suf = collections.Counter(); metrics = collections.Counter()
for f in res:
    fid = f.get("id") or ""
    parts = fid.split("_")
    suf[parts[-1]] += 1
    if len(parts) >= 2: metrics[parts[1]] += 1
print("suffix=", suf.most_common())
print("n_metrics=", len(metrics))
print("metrics=", sorted(metrics.keys()))
print("--- one metric full family ---")
for f in res:
    if (f.get("id") or "").startswith("oth432_aacr_"):
        print(f.get("id"), "|cov", round(f.get("coverage") or 0,3), "|aC", f.get("alphaCount"), "|", (f.get("description") or "")[:100])
