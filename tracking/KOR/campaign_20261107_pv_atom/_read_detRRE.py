import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
print("id",d.get("id"),"| status",d.get("status"),"| stage",d.get("stage"),"| dateSubmitted",d.get("dateSubmitted"))
