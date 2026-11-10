import json, sys, collections, re
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or d.get("datasets") or []
print("n_datasets=", len(res), "count=", d.get("count"))
cat = collections.Counter()
rows = []
for x in res:
    c = (x.get("category") or {}).get("name") if isinstance(x.get("category"), dict) else x.get("category")
    cat[c] += 1
    rows.append((c, x.get("id"), x.get("name"), x.get("fieldCount"), x.get("alphaCount"), x.get("usableFieldCount")))
print("cats=", cat.most_common())
print("--- RISK / INSIDERS ---")
for r in rows:
    if r[0] and r[0].lower() in ("risk","insiders"):
        print(r)
