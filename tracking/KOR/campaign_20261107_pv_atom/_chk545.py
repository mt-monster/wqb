import json,sys
raw=open(sys.argv[1]+"/_dfout_other545.json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
for f in (d.get("results") or []): print(f.get("id"),f.get("type"),round(f.get("coverage") or 0,3))
used=set(json.load(open(sys.argv[1]+"/_all_used_identifiers.json",encoding="utf-8")))
print("oth545 ever dispatched:", [u for u in used if u.startswith("oth545")] or "NONE")
