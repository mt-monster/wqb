import json, sys
raw = open(sys.argv[1], encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or []
# high coverage + low crowding, prefer ratio/score-like
cand = [f for f in res if (f.get("coverage") or 0) >= 0.85 and (f.get("alphaCount") or 0) <= 30 and f.get("type")=="MATRIX"]
cand.sort(key=lambda f: (f.get("alphaCount") or 0))
print("n_candidates=", len(cand))
for f in cand[:45]:
    print(f.get("id"), "|cov", round(f.get("coverage") or 0,3), "|aC", f.get("alphaCount"), "|", (f.get("description") or "")[:75])
