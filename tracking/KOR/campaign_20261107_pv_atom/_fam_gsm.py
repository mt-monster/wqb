
import json, re
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_dfout_gsm2.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):]); ids=[f["id"] for f in d["results"]]
pats = ["_5bucket_pred","_5bucket_prob_label_","_5bucket_confidence_score_","_q5_label","_forward_return","regime_","pvdaily12m","_regression_pred","_1bucket_pred"]
for p in pats:
    sel=[i for i in ids if p in i]
    print(p, "->", len(sel), sel[:8])
