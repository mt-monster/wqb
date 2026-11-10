import json, sys, re
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or []
ids = sorted(f.get("id") for f in res)
print("total=", len(ids))
key = [i for i in ids if re.search(r"(bullish|bearish|sentiment|total|net)", i)]
print("n_key=", len(key))
for i in key[:120]:
    print(i)
