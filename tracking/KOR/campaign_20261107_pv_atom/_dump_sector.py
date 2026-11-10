import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
res=d.get("results") or []
# SECTOR is index 2
print("SECTOR full:", json.dumps(res[2], ensure_ascii=False)[:900])
