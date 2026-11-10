import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
tags=["STATISTICAL","MARKET","SECTOR","INDUSTRY","SUBINDUSTRY","SLOW_AND_FAST","FAST","SLOW"]
ids=[]
for i,res in enumerate(d.get("results") or []):
    a=res.get("alpha")
    aid=a if isinstance(a,str) else (a.get("id") if isinstance(a,dict) else None)
    prog=(res.get("raw") or {}).get("progress")
    print(tags[i], "| status", res.get("status"), "| alpha", aid, "| prog", prog)
    if aid: ids.append(aid)
json.dump(ids, open(sys.argv[1].replace("_neutsweep_look.json","_neut_alphaids.json"),"w"))
