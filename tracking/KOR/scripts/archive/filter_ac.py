import json, io, sys, re
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'd:\coding\traeCN_project\wqb\tracking\KOR\ac_fields.json', encoding='utf-8'))
rs = d.get('results', [])
print('total', len(rs))
good = [r for r in rs if r.get('coverage', 0) >= 0.8 and r.get('alphaCount', 99) <= 3]
print('good(cov>=0.8,ac<=3)', len(good))
# 按族分组展示代表字段
seen = Counter()
for r in sorted(good, key=lambda x: (x['alphaCount'], x['id'])):
    fam = '_'.join(r['id'].split('_')[:3])
    if seen[fam] < 4:
        seen[fam] += 1
        print(r['id'], '|cov', r['coverage'], '|ac', r['alphaCount'], '|', (r.get('description') or '')[:55])
