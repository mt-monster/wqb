import json,sys,re
for aid in ["O08kz5Mv","pwvndZJ3","ZY0R0mL8","e73Rw8qg","pwjpKGJ3","0mre68gv"]:
    raw=open(sys.argv[1]+"/_det_"+aid+".json",encoding="utf-8-sig").read()
    try: d=json.loads(raw[raw.find("{"):])
    except: print(aid,"PARSE_FAIL"); continue
    code=d.get("code") or ""; m=d.get("metrics") or {}; ra=d.get("ra") or {}
    toks=set(re.findall(r"[a-z]+[0-9]+_[a-z0-9_]+", code)); prefixes=set(t.split("_")[0] for t in toks)
    ok = (m.get("sharpe") or 0)>=1.58 and (m.get("two_year_sharpe") or 0)>=1.58 and (m.get("fitness") or 0)>=1.0 and ra.get("failed_ra_count")==0
    print(aid,"| status",d.get("status"),"| S",m.get("sharpe"),"| F",m.get("fitness"),"| 2Y",m.get("two_year_sharpe"),"| raF",ra.get("failed_ra_count"),"| prefixes",sorted(prefixes),"| GATES", "PASS" if ok else "FAIL")
