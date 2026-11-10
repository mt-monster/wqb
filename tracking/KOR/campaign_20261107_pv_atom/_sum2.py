import json,collections,re
def load(k):
    raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_"+k+".json", encoding="utf-8-sig").read()
    return json.loads(raw[raw.find("{"):])["results"]
for k in ("starmine","intraday"):
    res = load(k)
    print("===", k, "n=", len(res), "types=", collections.Counter(x["type"] for x in res))
    fam = collections.Counter()
    for x in res:
        i = x["id"].lower()
        parts = re.split(r"[_0-9]+", i)
        fam[parts[0] if parts and parts[0] else i[:8]] += 1
    print("  prefix:", fam.most_common(16))
    for x in res[:14]:
        print("   ", x["id"], x["type"], round(x["coverage"],3), x["alphaCount"], "|", (x.get("description") or "")[:70])