import json, sys
p = sys.argv[1]
raw = open(p, encoding="utf-8-sig").read()
d = json.loads(raw[raw.find("{"):])
alphas = d.get("alphas") or []
print("n_alphas=", len(alphas))
for a in alphas:
    m = a.get("metrics") or {}
    ra = a.get("ra") or {}
    print("|".join(str(x) for x in [
        a.get("id"),
        m.get("sharpe"), m.get("fitness"), m.get("two_year_sharpe"),
        m.get("turnover"), m.get("longCount"), m.get("shortCount"),
        ra.get("failed_ra_count"), ra.get("ra_failed_checks"),
    ]))
    print("   EXPR:", (a.get("code") or "")[:400])
