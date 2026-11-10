import json,collections
def load(k):
    raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_"+k+".json", encoding="utf-8-sig").read()
    return json.loads(raw[raw.find("{"):])["results"]
for k in ("f93","fhp","nst"):
    res = load(k)
    print("===", k, "n=", len(res), collections.Counter(x["type"] for x in res))
    for x in res[:16]:
        print("   ", x["id"], x["type"], round(x["coverage"],2), x["alphaCount"], "|", (x.get("description") or "")[:62])