import json,sys,glob
known={"omERn83n","qMLOooX1","RRE9NkVj","d5Wvpmbx","ZYQ116ln","LLZ6wZO2"}
seen=set(); passers=[]
for p in sorted(glob.glob(sys.argv[1]+"/_pool_*.json")):
    try: raw=open(p,encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    except: continue
    for a in (d.get("results") or []):
        aid=a.get("id")
        if aid in seen: continue
        seen.add(aid)
        m=a.get("metrics") or {}; ra=a.get("ra") or {}
        s=m.get("sharpe"); f=m.get("fitness"); y=m.get("two_year_sharpe"); rf=ra.get("failed_ra_count")
        if s is None: continue
        if s>=1.58 and (f or 0)>=1.0 and (y or 0)>=1.58 and rf==0:
            passers.append((s,f,y,aid,aid in known,(a.get("code") or "")[:60]))
print("total_unique=",len(seen),"full_gate_passers=",len(passers))
for x in sorted(passers,reverse=True): print(x)
