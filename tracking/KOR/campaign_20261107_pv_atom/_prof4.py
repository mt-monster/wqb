import json, collections, re, sys
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or []
tri = collections.defaultdict(dict)
for f in res:
    if f.get("type") != "VECTOR": continue
    fid = f.get("id") or ""
    m = re.match(r"^anl44_(\d+)_(.+)$", fid)
    if not m: continue
    grp, rest = m.group(1), m.group(2)
    parts = rest.split("_")
    kind = parts[-1]
    metric = "_".join(parts[:-1])
    if kind in ("value","prevalue","lastactvalue","coveredby","lastactccy"):
        tri[(grp, metric)][kind] = round((f.get("coverage") or 0),3)
full = {k:v for k,v in tri.items() if "value" in v and "prevalue" in v}
print("n_metrics_with_value_and_prevalue=", len(full))
for k in sorted(full, key=lambda x: -(full[x].get("value") or 0)):
    print(k, full[k])
