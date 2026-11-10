import json,sys,re
camp=sys.argv[1]
# exact exprs + settings for the 4 existing
for aid in ["KPNo2lgl","e73Rw8qg","A1NXddRw","pwvndZJ3"]:
    raw=open(camp+"/_det_"+aid+".json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    s=d.get("settings") or {}
    print("==",aid,"| neut",s.get("neutralization"),"decay",s.get("decay"),"trunc",s.get("truncation"),"nan",s.get("nanHandling"))
    print("   ",d.get("code"))
# verify e73Rw8qg fields belong to analyst44
raw=open(camp+"/_dfout_analyst44.json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
ids={f.get("id") for f in (d.get("results") or [])}
for fld in ["anl44_second_en_eps_value","pretaxprofit_estimates_down_4w"]:
    print("analyst44 has",fld,":",fld in ids)
