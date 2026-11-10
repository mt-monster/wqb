import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
print("keys=",list(d.keys()))
for a in (d.get("alphas") or []):
    print({k:v for k,v in a.items() if k in ("location","simulation_location","sim_location","alpha_id","error","status")})
