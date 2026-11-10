import json,sys
allrows=[]
for off in [0,100]:
    raw=open(sys.argv[1]+"/_pool_"+str(off)+".json",encoding="utf-8-sig").read()
    d=json.loads(raw[raw.find("{"):])
    rows=d.get("results") or d.get("alphas") or []
    if isinstance(rows,dict): rows=rows.get("results") or []
    allrows+=rows
print("total=",len(allrows))
if allrows:
    print("sample_keys=",list(allrows[0].keys()))
def g(a,*ks):
    for k in ks:
        if isinstance(a,dict) and k in a: return a[k]
    m=a.get("metrics") or {} if isinstance(a,dict) else {}
    for k in ks:
        if k in m: return m[k]
    return None
hi=[]
for a in allrows:
    s=g(a,"sharpe"); 
    if s is None: continue
    try: s=float(s)
    except: continue
    if s>=1.4:
        hi.append((s, g(a,"id"), g(a,"fitness"), g(a,"two_year_sharpe"), g(a,"turnover"), (g(a,"code") or g(a,"expression") or "")[:70]))
hi.sort(reverse=True)
print("n_S>=1.4=",len(hi))
for h in hi: print(h)
