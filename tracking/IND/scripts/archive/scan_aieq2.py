import json, re

t = open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\d48cabf4.txt', encoding='utf-8-sig').read()
i = t.find('{')
d = json.loads(t[i:])
rs = d['results']
zero = [r for r in rs if r.get('userCount', 0) == 0 and r.get('coverage', 0) >= 0.95]

pats = ['momentum', 'reversal', 'volatil', 'liquidity', 'volume', 'return', 'price', 'trend', 'oscill', 'beta', 'drawdown', 'risk_prem', 'sentiment', 'flow']
hits = []
for r in zero:
    key = (r['id'] + ' ' + (r.get('description') or '')).lower()
    if any(p in key for p in pats):
        hits.append(r)
print('zero-competition tech/momentum-type fields:', len(hits))
for r in hits[:40]:
    print('%-48s cov=%-5s %s' % (r['id'], r.get('coverage'), (r.get('description') or '')[:70]))
