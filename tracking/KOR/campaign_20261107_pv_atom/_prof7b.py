
import json, collections
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_dfout_gsm2.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):]); fl = d.get("results") or []
print("n=", len(fl), "count=", d.get("count"))
print("types:", dict(collections.Counter(f.get("type") for f in fl)))
covs=[f.get("coverage") for f in fl if isinstance(f.get("coverage"),(int,float))]
acs=[f.get("alphaCount") for f in fl if isinstance(f.get("alphaCount"),(int,float))]
print("cov med=", sorted(covs)[len(covs)//2] if covs else None, "ac med=", sorted(acs)[len(acs)//2] if acs else None)
for f in fl[:28]:
    print(" ", f["id"], "|", f.get("type"), "| cov=", f.get("coverage"), "| aC=", f.get("alphaCount"), "|", (f.get("description") or "")[:58])
