import json
raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_fhp.json", encoding="utf-8-sig").read()
res = json.loads(raw[raw.find("{"):])["results"]
for x in res: print("   %-48s %-7s cov=%.2f aC=%-3s | %s" % (x["id"], x["type"], x["coverage"], x["alphaCount"], (x.get("description") or "")[:54]))