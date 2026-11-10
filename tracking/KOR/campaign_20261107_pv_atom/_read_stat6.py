import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
for x in (d.get("results") or []):
    print(x.get("alpha_id"),"| status",x.get("status"),"| S",x.get("sharpe"),"| dateSubmitted",x.get("dateSubmitted"))
