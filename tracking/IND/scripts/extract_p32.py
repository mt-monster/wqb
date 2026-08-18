import json, os, sys
P = os.path.join(os.environ['TEMP'], sys.argv[1] if len(sys.argv) > 1 else 'p32.json')
d = json.load(open(P, encoding='utf-8-sig'))
ms = d[0]['metrics'] if isinstance(d, list) and d and isinstance(d[0], dict) and 'metrics' in d[0] else d
for m in ms:
    print('==', m.get('code', '')[:95])
    for k in ('sharpe', 'fitness', 'two_year_sharpe', 'turnover_pct', 'margin_bp'):
        if k in m:
            print('   ', k, '=', m[k])
    fc = m.get('failed_checks') or []
    if fc:
        print('    FAIL:', fc)
