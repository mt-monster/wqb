
import json, os
rows = {}
for p in [r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_0.json", r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_100.json"]:
    if not os.path.exists(p): continue
    raw = open(p, encoding="utf-8-sig").read()
    d = json.loads(raw[raw.find("{"):])
    for a in (d.get("results") or []):
        rows[a["id"]] = a
near=[]
for aid,a in rows.items():
    m=a.get("metrics") or {}
    s=m.get("sharpe"); y=m.get("two_year_sharpe"); f=m.get("fitness")
    if s is None or y is None: continue
    if s>=1.35 and y>=1.35:
        near.append((-(s or 0), aid, s, f, y, m.get("turnover"), (a.get("ra") or {}).get("failed_ra_count"), (a.get("code") or "")[:78]))
near.sort(key=lambda x: x[0])
print("近线 (S>=1.35 & 2Y>=1.35):", len(near))
for n in near:
    print(f"raF={n[6]} S={n[2]:>5} F={n[3]:>5} 2Y={n[4]:>5} TO={n[5]:>6} {n[1]} {n[7]}")
print()
# distribution
import collections
sc=[ (a.get('metrics') or {}).get('sharpe') for a in rows.values() ]
sc=[x for x in sc if isinstance(x,(int,float))]
sc.sort()
print("sharpe percentiles:", {p: round(sc[int(len(sc)*p/100)-1],2) for p in [50,75,90,95,99]}, "max", sc[-1])
