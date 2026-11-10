import json,glob
def parse(k):
    raw = open("tracking/KOR/campaign_20261107_pv_atom/_msout_"+k+".json", encoding="utf-8-sig").read()
    d = json.loads(raw[raw.find("{"):])
    items = d.get("alphas") or d.get("results") or []
    print("=== "+k+" n="+str(len(items))+" topkeys="+str(list(d.keys())[:8]))
    rows=[]
    for a in items:
        if not isinstance(a, dict): continue
        m = a.get("metrics") or (a.get("is") or {}).get("metrics") or {}
        ra = a.get("ra") or a.get("checks") or {}
        aid = a.get("alpha_id") or a.get("id") or a.get("alphaId")
        rows.append((aid, m, ra, a.get("expression") or a.get("regular") or ""))
    for aid,m,ra,ex in rows:
        fails = None
        if isinstance(ra,dict):
            fails = ra.get("failed_ra_count", ra.get("failed_count"))
        print("  %-10s S=%-6s F=%-6s 2Y=%-6s TO=%-6s raF=%-4s | %s" % (
            str(aid), m.get("sharpe"), m.get("fitness"), m.get("sharpe_2y") or m.get("long_count"),
            m.get("turnover"), fails, str(ex)[:88]))
for k in ("P84A","P84B"):
    parse(k)