import json,collections,re
def load(k):
    raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_"+k+".json", encoding="utf-8-sig").read()
    return json.loads(raw[raw.find("{"):])["results"]
for k in ("mfrp","gsm"):
    try:
        res = load(k)
    except Exception as e:
        print("===", k, "LOADFAIL"); continue
    print("===", k, "n=", len(res), collections.Counter(x["type"] for x in res))
    fam = collections.Counter()
    for x in res:
        p = re.split(r"[_0-9]+", x["id"].lower())
        fam[p[0] if p and p[0] else x["id"][:8]] += 1
    print("  prefix:", fam.most_common(12))
    for x in res[:8]:
        print("   ", x["id"], round(x["coverage"],2), x["alphaCount"], "|", (x.get("description") or "")[:62])