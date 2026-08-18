import json, sys

for w in sys.argv[1:] or ["15"]:
    r = json.load(open(f"d:/coding/traeCN_project/wqb/tracking/GBR/reviews/gbr_review_{w}.json", encoding="utf-8"))
    print(f"=== wave {w}: total={len(r['all'])} candidates={len(r.get('candidates', []))} near={len(r.get('near', []))}")
    for a in r["all"][:8]:
        print(f"  {a.get('code','')[:58]:<58} sh={a.get('sharpe') or 0:.2f} fit={a.get('fitness') or 0:.2f} 2y={a.get('two_year_sharpe') or 0:.2f} mg={a.get('margin_bp') or 0:.1f}bp tvr={a.get('turnover_pct') or 0:.1f}%")
