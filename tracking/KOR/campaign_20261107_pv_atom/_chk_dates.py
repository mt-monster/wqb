import json,sys
for aid in ["KPNo2lgl","e73Rw8qg","A1NXddRw","pwvndZJ3"]:
    raw=open(sys.argv[1]+"/_det_"+aid+".json",encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
    keys=[k for k in d.keys()]
    ds=d.get("dateSubmitted") or d.get("dateCreated") or d.get("submitted") or ""
    print(aid,"| dateSubmitted",d.get("dateSubmitted"),"| dateCreated",d.get("dateCreated"),"| status",d.get("status"))
