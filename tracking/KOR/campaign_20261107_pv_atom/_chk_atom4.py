import json,sys,re
for aid in ["KPNo2lgl","RRAG0WMb","xAY86Mkl","A1NXddRw"]:
    raw=open(sys.argv[1]+"/_det_"+aid+".json",encoding="utf-8-sig").read()
    try: d=json.loads(raw[raw.find("{"):])
    except: print(aid,"PARSE_FAIL"); continue
    code=d.get("code") or ""
    m=d.get("metrics") or {}; ra=d.get("ra") or {}
    # extract field prefixes (identifiers with underscore that are not operators)
    toks=set(re.findall(r"[a-z]+[0-9]+_[a-z0-9_]+", code))
    prefixes=set(t.split("_")[0] for t in toks)
    print(aid,"| status",d.get("status"),"| S",m.get("sharpe"),"| 2Y",m.get("two_year_sharpe"),"| raF",ra.get("failed_ra_count"),"| prefixes",sorted(prefixes))
    print("   expr:",code[:160])
