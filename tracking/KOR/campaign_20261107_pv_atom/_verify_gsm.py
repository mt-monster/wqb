
import json, re
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_dfout_gsm2.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):]); ids=set(f["id"] for f in d["results"])
exprs = [
 "group_rank(analyst_60d_return_regression, industry)",
 "group_rank(pv_daily_20d_return_regression, industry)",
 "subtract(group_rank(analyst_60d_return_regression, industry), group_rank(analyst_120d_return_regression, industry))",
 "subtract(group_rank(analyst_60d_return_regression, industry), group_rank(pv_weekly_monthqtr_60d_return_regression, industry))",
 "group_rank(ts_delta(analyst_60d_return_regression, 22), industry)",
 "subtract(0.5, group_rank(ts_std_dev(analyst_60d_return_regression, 252), industry))",
 "subtract(group_rank(analyst_60d_return_quantile5_prob4, industry), group_rank(analyst_60d_return_quantile5_prob1, industry))",
 "signed_power(group_rank(analyst_60d_return_regression, industry), 2)",
 "group_rank(funda_regime_120d_return_regression, industry)",
 "multiply(group_rank(analyst_60d_return_regression, industry), group_rank(pv_daily_20d_return_regression, industry))"
]
KNOWN_OPS={"group_rank","subtract","group_scale","ts_mean","ts_delta","ts_std_dev","signed_power","multiply","vec_avg","rank","winsorize","ts_rank","ts_zscore","ts_av_diff","divide","add","group_zscore","ts_target_tvr_decay","vector_neut"}
bad=[]
for e in exprs:
    toks=set(re.findall(r"[a-z_][a-z0-9_]{2,}", e))
    for t in toks:
        if t in KNOWN_OPS: continue
        if t in {"industry","sector","subindustry","country","market"}: continue
        if t not in ids: bad.append((e[:40], t))
print("invalid tokens:", bad if bad else "NONE - all fields valid")
