import json,re,collections
raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_mfrp.json", encoding="utf-8-sig").read()
res = json.loads(raw[raw.find("{"):])["results"]
ids = [x["id"] for x in res]
longs = [i for i in ids if i.startswith("long")]
shorts = [i for i in ids if i.startswith("short")]
print("LONG", len(longs)); 
for i in longs[:24]: print("   ", i)
print("SHORT", len(shorts))
for i in shorts[:16]: print("   ", i)
print("--- families by (root, horizon)")
def root(i):
    m = re.match(r"^(.*?)_(\d+)d_(q\d|confidence_score|signal.*)$", i)
    return (m.group(1), m.group(2)) if m else (i[:24], "?")
c = collections.Counter(root(i) for i in ids)
for k,v in c.most_common(24): print("   ", k, v)