import json,sys
raw=open(sys.argv[1],encoding="utf-8-sig").read(); d=json.loads(raw[raw.find("{"):])
recs=d.get("recommendations") or []
rows=[]
for x in recs:
    rows.append((x.get("os_is_sharpe"), x.get("dataset_id"), x.get("category"), x.get("quality_score"), x.get("os_is_count"), x.get("dataset_alpha_count"), x.get("dataset_user_count"), x.get("category_lit")))
rows.sort(key=lambda r:(r[0] is None, -(r[0] or 0)))
print("os_is_sharpe | dataset | cat | quality | os_is_n | aC | uC | lit")
for r in rows: print(r)
print("total_scored",d.get("total_datasets_scored"),"candidate",d.get("total_candidate_datasets"),"available",d.get("total_available_datasets"))
