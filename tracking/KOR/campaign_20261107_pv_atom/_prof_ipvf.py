
import json, collections, re
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_dfout_ipvf.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):]); fl = d.get("results") or []
print("n=", len(fl), "count=", d.get("count"))
print("types:", dict(collections.Counter(f.get("type") for f in fl)))
fam = collections.Counter()
for f in fl:
    i=f["id"]
    m = re.match(r"([a-z]+)_", i)
    fam[m.group(1) if m else i]+=1
print("prefix families:", dict(fam))
print()
for f in fl[:35]:
    print(" ", f["id"], "| cov=", f.get("coverage"), "| aC=", f.get("alphaCount"), "|", (f.get("description") or "")[:52])
