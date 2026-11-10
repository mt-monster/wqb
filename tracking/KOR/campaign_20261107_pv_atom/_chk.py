
import json,re
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_dfout_gsm2.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):]); ids=[f["id"] for f in d["results"]]
print("analyst_120d_return_quantile5*:", [i for i in ids if i.startswith("analyst_120d_return_quantile5")])
print()
print("all _20d_return_regression:", [i for i in ids if "_20d_return_regression" in i])
print()
print("any 'quantile5_prob' sample:", [i for i in ids if "quantile5_prob" in i][:20])
