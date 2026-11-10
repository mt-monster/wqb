import json,re
raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_starmine.json", encoding="utf-8-sig").read()
res = json.loads(raw[raw.find("{"):])["results"]
for tok in ("upward","downward","arm_score_change_7d","arm_global_rank","smest_fy1_earnings","ep_yield_pct_smest_f12m","recommendation_mean"):
    sel = [x for x in res if tok in x["id"]]
    print("##", tok, len(sel))
    seen=set()
    for x in sel:
        b = re.sub(r"_\d+$","",x["id"])
        if b in seen: continue
        seen.add(b)
        print("   ", x["id"], round(x["coverage"],2), x["alphaCount"])
        if len(seen)>=8: break