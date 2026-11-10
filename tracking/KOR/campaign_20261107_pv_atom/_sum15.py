import json,re,collections
def load(k):
    raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_"+k+".json", encoding="utf-8-sig").read()
    return json.loads(raw[raw.find("{"):])["results"]
m262 = load("m262")
pred = [x for x in m262 if x["id"].endswith("_predict")]
madp = [x for x in m262 if x["id"].endswith("_madp")]
print("m262 predict n=",len(pred)," madp n=",len(madp))
for x in pred: print("   P", x["id"], round(x["coverage"],2), x["alphaCount"], "|", (x.get("description") or "")[:50])
print()
m138 = load("m138")
ids = sorted(x["id"] for x in m138)
print("m138 n=",len(ids))
for i in ids[:40]: print("   ", i)