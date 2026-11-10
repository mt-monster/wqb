
import json, re, collections
for name in ["fundamental89","other78","model238"]:
    raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_dfout_" + name + ".json", encoding="utf-8-sig").read()
    d = json.loads(raw[raw.find("{"):])
    fl = d.get("results") or []
    print("="*70)
    print(name, "fields=", len(fl), "total=", d.get("count"))
    types = collections.Counter(f.get("type") for f in fl)
    covs = [f.get("coverage") for f in fl if isinstance(f.get("coverage"), (int,float))]
    acs  = [f.get("alphaCount") for f in fl if isinstance(f.get("alphaCount"), (int,float))]
    print("  types:", dict(types), "cov_med=", sorted(covs)[len(covs)//2] if covs else None,
          "ac_med=", sorted(acs)[len(acs)//2] if acs else None)
    for f in fl[:40]:
        print("   ", f.get("id"), "|", f.get("type"), "| cov=", f.get("coverage"), "| aC=", f.get("alphaCount"), "|", (f.get("description") or "")[:70])
