import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for r in d['results'][:n]:
    print(f"sh={r['sharpe']} fit={r['fitness']} 2y={r['two_year_sharpe']} mg={r['margin_bp']} tvr={r['turnover_pct']} decay={r.get('decay')} rnsh={r.get('rn_sharpe')} rnf={r.get('rn_fitness')}")
    print(f"   {r['code']}")
