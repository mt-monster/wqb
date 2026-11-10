
import json
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_p103.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or []
hit = [a for a in res if "slippage_last_interval" in (a.get("code") or "") or "momentum2_vwap_first_quarter" in (a.get("code") or "")]
print("P103 alphas found:", len(hit))
for a in hit:
    m=a.get("metrics") or {}
    print(f"  S={m.get('sharpe')} 2Y={m.get('two_year_sharpe')} {a['id']} {(a.get('code') or '')[:70]}")
print("total in page:", len(res))
