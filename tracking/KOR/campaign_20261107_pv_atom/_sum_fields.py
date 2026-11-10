import json,re,collections
def load(key):
    raw = open("tracking/KOR/campaign_20261107_pv_atom/_df_"+key+".json", encoding="utf-8-sig").read()
    return json.loads(raw[raw.find("{"):])["results"]
ids = [x["id"] for x in load("chart")]
fams = ["imgpred_eqstar4_60dret_q5","cnn_predicted_prob_q5_bucket","img_leapstar4b1_50d_qtile5","img_pred_malta3_60d_5bucket","img_maltastar2_20d_qtile5","img_pred_leap_star3_80d_5bucket","img_equity_star1b1_rank60_quantile5"]
for f in fams:
    sel = [i for i in ids if i.startswith(f)]
    if f == "cnn_predicted_prob_q5_bucket":
        sel = [i for i in ids if i.startswith("cnn_predicted_prob_q5_bucket") and i.endswith("_50d_equity2b2")]
    print("##", f, len(sel))
    for i in sel: print("   ", i)
print("## other prefixes with prob")
for i in ids:
    if "prob" in i and i.count("_") <= 5 and i not in ids[:0]: print("   ", i)