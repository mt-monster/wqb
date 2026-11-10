import json,sys,glob
hits=[]
for p in sorted(glob.glob(sys.argv[1]+"/_pool_*.json")):
    try: raw=open(p,encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    except: continue
    for a in (d.get("results") or []):
        code=a.get("code") or ""
        if "net_buy_amt" in code or "oth466" in code or "invactnet_buy" in code:
            m=a.get("metrics") or {}; ra=a.get("ra") or {}
            hits.append((a.get("id"),m.get("sharpe"),m.get("fitness"),m.get("two_year_sharpe"),ra.get("failed_ra_count"),code[:75]))
seen=set(); uniq=[]
for h in hits:
    if h[0] in seen: continue
    seen.add(h[0]); uniq.append(h)
print("n_hits=",len(uniq))
for h in sorted(uniq,key=lambda x:-(x[1] or 0)): print(h)
