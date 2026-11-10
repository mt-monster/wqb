
import json, glob, os
rows = {}
for p in [r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_0.json", r"D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_uaout_100.json"]:
    if not os.path.exists(p): continue
    raw = open(p, encoding="utf-8-sig").read()
    d = json.loads(raw[raw.find("{"):])
    for a in (d.get("results") or []):
        rows[a["id"]] = a
print("unique alphas:", len(rows))
delivered = {"omERn83n","qMLOooX1","RRE9NkVj","d5Wvpmbx"}
cands=[]
for aid,a in rows.items():
    m=a.get("metrics") or {}; ra=a.get("ra") or {}
    s=m.get("sharpe"); f=m.get("fitness"); y=m.get("two_year_sharpe"); t=m.get("turnover")
    raf=ra.get("failed_ra_count")
    if s is None: continue
    if s>=1.58 and y is not None and y>=1.58 and f is not None and f>=1.0:
        cands.append((raf, -s, aid, s,f,y,t,(a.get("code") or "")[:80]))
cands.sort()
print("--- 过线候选 (S>=1.58 & 2Y>=1.58 & F>=1.0) ---")
for c in cands:
    print(f"raF={c[0]} S={c[3]:>5} F={c[4]:>5} 2Y={c[5]:>5} TO={c[6]:>6} {'DELIVERED' if c[2] in delivered else 'NEW'} {c[2]} {c[7]}")
print()
print("--- 近线 (S>=1.4 & 2Y>=1.4) ---")
near=[( -((a.get('metrics') or {}).get('sharpe') or 0), a) for a in rows.values() if (a.get('metrics') or {}).get('sharpe') and (a['metrics']['sharpe']>=1.4) and ((a.get('metrics') or {}).get('two_year_sharpe') or 0)>=1.4]
near.sort()
for n,a in near[:25]:
    m=a['metrics']; ra=a.get('ra') or {}
    print(f"raF={ra.get('failed_ra_count')} S={m.get('sharpe'):>5} F={m.get('fitness')} 2Y={m.get('two_year_sharpe')} TO={m.get('turnover')} {a['id']} {(a.get('code') or '')[:80]}")
