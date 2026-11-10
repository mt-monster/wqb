import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
res=d.get("results") or []
rt=[f for f in res if "_rt_" in (f.get("id") or "") and (f.get("coverage") or 0)>=0.8]
print("n_rt_highcov=",len(rt))
for f in rt[:25]: print(f.get("id"),"|cov",round(f.get("coverage") or 0,3),"|aC",f.get("alphaCount"),"|",(f.get("description") or "")[:55])
