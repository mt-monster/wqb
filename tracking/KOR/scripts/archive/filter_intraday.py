import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\8669f9fd.txt', encoding='utf-8'))
rs = d.get('results', [])
print('total', len(rs))
good = [r for r in rs if r.get('coverage', 0) >= 0.8 and r.get('alphaCount', 99) <= 5]
good.sort(key=lambda r: r['alphaCount'])
print('good', len(good))
for r in good[:40]:
    print(r['id'], '|cov', r['coverage'], '|ac', r['alphaCount'], '|', (r['description'] or '')[:70])
