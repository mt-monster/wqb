import json, re, collections, sys
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or []
mx = [f for f in res if f.get("type") == "MATRIX"]
print("n_matrix=", len(mx))
pat = re.compile(r"^oth455_(\w+?)_(\w+?)_q(\d+)_w(\d+)_(.*)$")
combos = collections.Counter()
for f in mx:
    fid = f.get("id")
    m = pat.match(fid)
    if m:
        combos[(m.group(1), m.group(3), m.group(4))] += 1
    else:
        print("UNMATCHED", fid)
for k in sorted(combos):
    print(k, combos[k])
print("--- sample matrix ids ---")
for f in mx[:25]:
    print(f.get("id"), "|cov", round(f.get("coverage") or 0,3), "|aC", f.get("alphaCount"))
print("--- group label kinds ---")
gk = collections.Counter()
for f in res:
    if f.get("type") != "GROUP": continue
    fid = f.get("id")
    tail = fid.split("_")
    gk["_".join(tail[-2:]) if tail[-1].isdigit() else tail[-1]] += 1
print(gk.most_common(15))
