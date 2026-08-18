import json, sys
d = json.load(open(sys.argv[1], encoding='utf-8'))
rs = d['results']
print('total', len(rs), 'candidates', len(d.get('candidates', [])))
for r in rs:
    print(f"{r['sharpe']:+.2f} fit={r.get('fitness')} 2y={r.get('two_year_sharpe')} mg={r.get('margin_bp')} tvr={r.get('turnover_pct')} rnsh={r.get('rn_sharpe')} rnf={r.get('rn_fitness')} fc={r.get('failed_checks')} :: {r['code'][:55]}")
