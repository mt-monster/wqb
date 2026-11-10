
import json, os
rows={}
for p in [r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_0.json", r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_100.json"]:
    raw = open(p, encoding="utf-8-sig").read()
    d = json.loads(raw[raw.find("{"):])
    for a in (d.get("results") or []): rows[a["id"]]=a
for aid in ["npvr2qow","wpQWLOQx","9qxk9OQ1","E56xEz00","3qoJ9MxP"]:
    a=rows.get(aid)
    if not a: print(aid,"missing"); continue
    m=a.get("metrics") or {}; s=a.get("settings") or {}; ra=a.get("ra") or {}
    print("="*80)
    print(aid, "S=",m.get("sharpe"),"F=",m.get("fitness"),"2Y=",m.get("two_year_sharpe"))
    print("  code:", a.get("code"))
    print("  settings:", {k:s.get(k) for k in ["neutralization","decay","truncation","nanHandling","universe","delay"]})
    print("  ra_failed:", ra.get("ra_failed_checks"))
