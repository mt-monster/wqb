import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
tags=json.load(open(sys.argv[2],encoding="utf-8")); ids=[]
for i,res in enumerate(d.get("results") or []):
    a=res.get("alpha"); aid=a if isinstance(a,str) else None
    print(tags[i],"| status",res.get("status"),"| alpha",aid,"| prog",(res.get("raw") or {}).get("progress"))
    if aid: ids.append(aid)
json.dump(ids, open(sys.argv[1].replace("_slowgeo_look.json","_slowgeo_alphaids.json"),"w"))
