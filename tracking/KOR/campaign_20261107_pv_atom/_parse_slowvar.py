import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
print("submitted=",d.get("submitted"),"total=",d.get("total"))
locs=[]; tags=[]
for r in (d.get("results") or []):
    print(r.get("tag"), r.get("ok"), r.get("simulation_id"), r.get("error",""))
    if r.get("simulation_id"): locs.append("https://api.worldquantbrain.com/simulations/"+r["simulation_id"]); tags.append(r.get("tag"))
json.dump({"locations":locs}, open(sys.argv[1].replace("_slowvar_dispatch.json","_args_LOOK_slowvar.json"),"w"))
json.dump(tags, open(sys.argv[1].replace("_slowvar_dispatch.json","_slowvar_tags.json"),"w"))
