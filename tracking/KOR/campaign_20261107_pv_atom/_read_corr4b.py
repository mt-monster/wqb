import json,sys
for aid in ["KPNo2lgl","e73Rw8qg","A1NXddRw","pwvndZJ3"]:
    raw=open(sys.argv[1]+"/_corr_"+aid+".json",encoding="utf-8-sig").read()
    try: d=json.loads(raw[raw.find("{"):])
    except: print(aid,"PARSE_FAIL"); continue
    ch=d.get("checks") or {}
    p=ch.get("production") or {}; s=ch.get("self") or {}
    print(aid,"| prod",p.get("max_correlation"),"pass",p.get("passes_check"),"| self",s.get("max_correlation"),"pass",s.get("passes_check"),"| all",d.get("all_passed"))
