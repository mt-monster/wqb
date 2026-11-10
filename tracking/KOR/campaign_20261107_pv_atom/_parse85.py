import json
raw = open("tracking/KOR/campaign_20261107_pv_atom/_msout_P85.json", encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
items = d.get("alphas") or []
print("n=",len(items),"err=",d.get("error_count"))
rows=[]
for a in items:
    m = a.get("metrics") or {}
    ra = a.get("ra") or a.get("checks") or {}
    f = ra.get("failed_ra_count") if isinstance(ra,dict) else None
    print("%-9s S=%-6s F=%-6s 2Y=%-6s TO=%-6s raF=%-4s | %s" % (a.get("alpha_id"), m.get("sharpe"), m.get("fitness"), m.get("sharpe_2y"), m.get("turnover"), f, str(a.get("expression"))[:84]))
    rows.append(a)
print("--- keys sample:", list(items[0].keys()) if items else None)