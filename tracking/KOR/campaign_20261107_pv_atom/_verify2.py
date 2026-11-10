
import json, re
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_dfout_gsm2.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):]); ids=set(f["id"] for f in d["results"])
cand = ["pv_daily_60d_regression_pred","analyst_regime_120d_regression_pred","pvweekly_60d_regression_pred",
        "analyst_60d_regression_pred","pv_daily_12m_60d_regression_pred","funda_regime_20d_1bucket_pred",
        "pv_daily_60d_5bucket_prob_label_4","pv_daily_60d_5bucket_prob_label_0","pvweekly_60d_1bucket_pred",
        "pv_12m_20d_q5_label4_probability","pv_12m_20d_q5_label0_probability","pv_12m_20d_5bucket_pred"]
for c in cand:
    print(("OK  " if c in ids else "MISS"), c)
print()
print("pv_daily_60d_* :", sorted([i for i in ids if i.startswith("pv_daily_60d")])
)
print("pvweekly_60d_* :", sorted([i for i in ids if i.startswith("pvweekly_60d")])[:15])
