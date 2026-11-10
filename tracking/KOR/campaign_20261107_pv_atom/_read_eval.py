import json,sys
for th in ["0.5","0.7"]:
    raw=open(sys.argv[1]+"/_mc_eval"+th+".json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    print("th",th,"| subset_size",d.get("max_mutually_below_subset_size"),"| exact",d.get("max_subset_exact"),"| max_pair",d.get("max_pair",{}).get("correlation"))
    print("   subset:",d.get("max_mutually_below_subset"))
    print("   pairs_over:",[(p['a'],p['b'],p['correlation']) for p in (d.get("pairs_over_threshold") or [])])
