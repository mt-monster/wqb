import json,collections,re
raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_starmine.json", encoding="utf-8-sig").read()
res = json.loads(raw[raw.find("{"):])["results"]
groups = collections.Counter()
for x in res:
    m = re.match(r"^([a-z]+(?:_[a-z]+)?)", x["id"])
    groups[m.group(1) if m else x["id"][:10]] += 1
print("GROUPS")
for k,v in groups.most_common(40): print("  ", k, v)
print()
sel = [x for x in res if any(t in x["id"] for t in ("arm","surprise","smest","recommendation"))]
print("KEY n=", len(sel))
seen = set()
for x in sel:
    base = re.sub(r"_\d+$","",x["id"])
    if base in seen: continue
    seen.add(base)
    print("  ", x["id"], round(x["coverage"],2), x["alphaCount"], "|", (x.get("description") or "")[:72])
    if len(seen) > 45: break