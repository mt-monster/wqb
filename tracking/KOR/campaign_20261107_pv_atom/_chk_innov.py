import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
res=d.get("results") or []
inn=[f for f in res if "analyst_innovation" in (f.get("id") or "")]
print("n_analyst_innovation=",len(inn))
for f in inn[:40]:
    print(f.get("id"),"|",f.get("type"),"|cov",round(f.get("coverage") or 0,3),"|aC",f.get("alphaCount"))
