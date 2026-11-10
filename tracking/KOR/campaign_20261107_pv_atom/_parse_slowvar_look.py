import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
tags=json.load(open(sys.argv[2],encoding="utf-8"))
ids=[]
for i,res in enumerate(d.get("results") or []):
    a=res.get("alpha"); aid=a if isinstance(a,str) else None
    prog=(res.get("raw") or {}).get("progress")
    print(tags[i] if i<len(tags) else i,"| status",res.get("status"),"| alpha",aid,"| prog",prog)
    if aid: ids.append(aid)
json.dump(ids, open(sys.argv[1].replace("_slowvar_look.json","_slowvar_alphaids.json"),"w"))
