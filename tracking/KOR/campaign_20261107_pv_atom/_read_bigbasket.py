import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
print("n_ids=",len(d.get("alpha_ids") or []),"missing_pnl=",d.get("missing_pnl"))
print("max_subset_size=",d.get("max_mutually_below_subset_size"),"exact=",d.get("max_subset_exact"))
print("max_subset=",d.get("max_mutually_below_subset"))
print("pairs_over=",len(d.get("pairs_over_threshold") or []))
