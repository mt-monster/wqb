import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
print("n=",len(d.get("alpha_ids") or []),"all_below=",d.get("all_below_threshold"),"subset_size=",d.get("max_mutually_below_subset_size"),"exact=",d.get("max_subset_exact"))
print("max_pair=",d.get("max_pair"))
print("pairs_over=",d.get("pairs_over_threshold"))
