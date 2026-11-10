import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
res=d.get("results") or []
for f in res:
    fid=f.get("id") or ""
    if any(k in fid for k in ["salrevise","prerevise","salinnovate","salnormal","preinnovate","prenormal","dpsrevise","preinnovation","salinnovation"]):
        print(fid,"|",f.get("type"),"|cov",round(f.get("coverage") or 0,3),"|aC",f.get("alphaCount"),"|",(f.get("description") or "")[:55])
