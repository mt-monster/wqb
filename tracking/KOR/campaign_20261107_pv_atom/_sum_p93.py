
import json
p = r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_msout_P93.json"
raw = open(p, encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
rows=[]
for a in d["alphas"]:
    m = a.get("metrics") or {}; ra = a.get("ra") or {}
    rows.append((m.get("sharpe"), m.get("fitness"), m.get("two_year_sharpe"), m.get("turnover"),
                 ra.get("failed_ra_count"), a.get("id"), (a.get("code") or "")[:95]))
rows.sort(key=lambda x: (x[0] is None, -(x[0] or -9)))
for r in rows:
    print(f"S={r[0]:>6} F={r[1]:>6} 2Y={r[2]:>6} TO={r[3]:>6} raF={r[4]} {r[5]} {r[6]}")
