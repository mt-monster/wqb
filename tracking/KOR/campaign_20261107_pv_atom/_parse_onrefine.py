import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
locs=[]; tags=[]
for x in (d.get("results") or []):
    if x.get("simulation_id"): locs.append("https://api.worldquantbrain.com/simulations/"+x["simulation_id"]); tags.append(x.get("tag"))
json.dump({"locations":locs}, open(sys.argv[1].replace("_onrefine_dispatch.json","_args_LOOK_onrefine.json"),"w"))
json.dump(tags, open(sys.argv[1].replace("_onrefine_dispatch.json","_onrefine_tags.json"),"w"))
print("n_locs",len(locs))
