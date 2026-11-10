import json,collections,re
raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_intraday.json", encoding="utf-8-sig").read()
res = json.loads(raw[raw.find("{"):])["results"]
groups = collections.Counter()
for x in res:
    m = re.match(r"^([a-z]+(?:\_[a-z]+)?)", x["id"])
    groups[m.group(1) if m else x["id"][:10]] += 1
for k,v in groups.most_common(25): print("  ", k, v)
print()
for tok in ("momentum","corr","skew","kurtosis","vwap","bid_size","ask_size","high","low","last_price"):
    sel = [x for x in res if tok in x["id"]]
    print("##", tok, len(sel))
    seen=set()
    for x in sel:
        b = re.sub(r"\_\d+$","",x["id"])
        if b in seen: continue
        seen.add(b)
        print("   ", x["id"], round(x["coverage"],2), x["alphaCount"], "|", (x.get("description") or "")[:58])
        if len(seen)>=6: break