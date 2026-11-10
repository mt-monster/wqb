import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
recs=d.get("recommendations") or []
print("rec0 keys:", list(recs[0].keys()) if recs else "none")
print("category_summary:", json.dumps(d.get("category_summary"),ensure_ascii=False)[:400])
for x in recs:
    did=x.get("dataset_id") or x.get("id")
    if did in ["other571","other475","other315","news59","news66","news17","news48","news29","news20","news18"]:
        print(json.dumps(x,ensure_ascii=False)[:350])
