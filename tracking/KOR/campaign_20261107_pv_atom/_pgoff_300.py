
import json
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_300.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
print("count=", d.get("count"), "server_count=", d.get("server_count"), "n=", len(d.get("results") or []), "next=", bool(d.get("next")))
