import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
recs=d.get("recommendations") or d.get("datasets") or []
print("n=",len(recs), "| topkeys", list(d.keys()))
for x in recs[:30]:
    print(x.get("dataset_id") or x.get("id"),"|",x.get("category") or x.get("pyramid"),"| score",x.get("score"),"| fields",x.get("fieldCount"),"| aC",x.get("alphaCount"),"| lit",x.get("pyramid_status") or x.get("lit"))
