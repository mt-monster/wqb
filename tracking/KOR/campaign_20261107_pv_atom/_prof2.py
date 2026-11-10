import json, sys, collections
p = sys.argv[1]
raw = open(p, encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or d.get("datafields") or d
if isinstance(res, dict):
    res = res.get("results") or []
print("n_fields=", len(res), "count=", d.get("count"))
covs = [f.get("coverage") for f in res if isinstance(f.get("coverage"), (int,float))]
if covs:
    covs.sort()
    print("coverage min/med/max=", round(covs[0],3), round(covs[len(covs)//2],3), round(covs[-1],3))
fam = collections.Counter()
for f in res:
    fid = f.get("id") or ""
    parts = fid.split("_")
    key = parts[1] if len(parts) > 1 else fid
    fam[key] += 1
print("fam_top=", fam.most_common(30))
print("types=", collections.Counter(f.get("type") for f in res).most_common())
ac = [f.get("alphaCount") for f in res if isinstance(f.get("alphaCount"), (int,float))]
if ac:
    ac.sort(); print("alphaCount min/med/max=", ac[0], ac[len(ac)//2], ac[-1])
for f in res[:800]:
    print(f.get("id"), "|", f.get("type"), "|", round(f.get("coverage") or 0,3), "|aC", f.get("alphaCount"), "|", (f.get("description") or "")[:70])
