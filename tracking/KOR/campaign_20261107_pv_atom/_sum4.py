import json,collections,re
raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_starmine.json", encoding="utf-8-sig").read()
res = json.loads(raw[raw.find("{"):])["results"]
def dump(tok, lim=14):
    sel = [x for x in res if tok in x["id"]]
    print("##", tok, len(sel))
    seen=set()
    for x in sel:
        b = re.sub(r"_\d+$","",x["id"])
        if b in seen: continue
        seen.add(b)
        print("   ", x["id"], round(x["coverage"],2), x["alphaCount"], "|", (x.get("description") or "")[:64])
        if len(seen)>=lim: break
for tok in ("analyst_upward_count","analyst_downward_count","mean_estimate","iv_projected","smest_growth","rel_val","eq_vr","surprise_pct"):
    dump(tok, 10)