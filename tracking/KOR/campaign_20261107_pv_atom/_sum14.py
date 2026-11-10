import json,collections,re
def load(k):
    raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_"+k+".json", encoding="utf-8-sig").read()
    return json.loads(raw[raw.find("{"):])["results"]
for k in ("m262","m138"):
    try: res = load(k)
    except Exception: print("===",k,"LOADFAIL"); continue
    print("===", k, "n=", len(res), collections.Counter(x["type"] for x in res))
    for x in res[:10]:
        print("   ", x["id"], round(x["coverage"],2), x["alphaCount"], "|", (x.get("description") or "")[:66])