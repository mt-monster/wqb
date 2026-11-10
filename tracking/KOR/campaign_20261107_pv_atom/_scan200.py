
import json
raw = open(r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_200.json", encoding="utf-8-sig").read()
try:
    d = json.loads(raw[raw.find("{"):])
except Exception as e:
    print("ERR", raw[:300]); raise SystemExit
res = d.get("results") or []
print("n=", len(res), "count=", d.get("count"))
near=[]
for a in res:
    m=a.get("metrics") or {}
    s=m.get("sharpe"); y=m.get("two_year_sharpe")
    if isinstance(s,(int,float)) and isinstance(y,(int,float)) and s>=1.35 and y>=1.35:
        near.append((-(s), a["id"], s, m.get("fitness"), y, m.get("turnover"), (a.get("ra") or {}).get("failed_ra_count"), (a.get("code") or "")[:70]))
near.sort()
print("near-line:", len(near))
for n in near[:20]:
    print(f"raF={n[6]} S={n[2]:>5} F={n[3]:>5} 2Y={n[4]:>5} TO={n[5]:>6} {n[1]} {n[7]}")
