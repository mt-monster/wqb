
import json
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_dfout_ipvf.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):]); ids=[f["id"] for f in d["results"]]
for p in ["slippage","skew_","std_","num_","trade_","momentum2_vwap","momentum2_last_trade_price","momentum3_","max_","min_","vwap_"]:
    sel=[i for i in ids if i.startswith(p)]
    print(p, "->", len(sel), sel[:10])
