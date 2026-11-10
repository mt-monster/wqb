import json, sys
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
for f in (d.get("results") or []):
    print(f.get("id"), "|cov", round(f.get("coverage") or 0,3), "|aC", f.get("alphaCount"), "|", (f.get("description") or "")[:95])
