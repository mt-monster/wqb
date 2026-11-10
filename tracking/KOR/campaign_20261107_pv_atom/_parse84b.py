import json
for k in ("P84A","P84B"):
    raw = open("tracking/KOR/campaign_20261107_pv_atom/_msout_"+k+".json", encoding="utf-8-sig").read()
    d = json.loads(raw[raw.find("{"):])
    print("===",k)
    for a in d["alphas"]:
        m = a.get("metrics") or {}
        ra = a.get("ra") or {}
        print("  %-9s S=%-5s F=%-5s 2Y=%-5s TO=%-6s raF=%-3s %s | %s" % (a.get("alpha_id"), m.get("sharpe"), m.get("fitness"), m.get("two_year_sharpe"), m.get("turnover"), ra.get("failed_ra_count"), ",".join(ra.get("ra_failed_checks") or []), str(a.get("expression"))[:60]))