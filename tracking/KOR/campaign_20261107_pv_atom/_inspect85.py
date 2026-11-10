import json
raw = open("tracking/KOR/campaign_20261107_pv_atom/_msout_P85.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
a = d["alphas"][7]
print("METRICS:", json.dumps(a.get("metrics"), ensure_ascii=False)[:900])
print("RA:", json.dumps(a.get("ra"), ensure_ascii=False)[:600])
print("CHECKS:", json.dumps(a.get("checks"), ensure_ascii=False)[:900])