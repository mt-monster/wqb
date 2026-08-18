import json, io, sys, re
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\a8b910e1.txt', encoding='utf-8'))
rs = d.get('results', [])
print('total', len(rs), 'removed_by_filter', d.get('sharpe_filter_removed'))
fams = Counter(re.sub(r'\d+$', '', r['id']) for r in rs)
print('--- families(top25) ---')
for f, c in fams.most_common(25):
    print(c, f)
print('--- good: cov>=0.7 & ac<=10 ---')
good = [r for r in rs if r.get('coverage', 0) >= 0.7 and r.get('alphaCount', 99) <= 10]
good.sort(key=lambda r: (r['alphaCount'], -r['coverage']))
print('good', len(good))
for r in good[:45]:
    print(r['id'], '|cov', r['coverage'], '|ac', r['alphaCount'], '|', (r['description'] or '')[:60])
