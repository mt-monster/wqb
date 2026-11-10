
import json
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_ua2_out.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
res = d.get("results") or []
f89 = [a for a in res if "fnd89" in (a.get("code") or "")]
f89.sort(key=lambda a: -((a.get("metrics") or {}).get("sharpe") or -9))
for a in f89:
    m=a.get("metrics") or {}; ra=a.get("ra") or {}
    print(f"S={m.get('sharpe'):>6} F={m.get('fitness'):>6} 2Y={m.get('two_year_sharpe'):>6} TO={m.get('turnover'):>6} raF={ra.get('failed_ra_count')} {a['id']} {(a.get('code') or '')[:95]}")
print("total fnd89:", len(f89), "of", len(res))
