import json
t = open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\d48cabf4.txt', encoding='utf-8-sig').read()
i = t.find('{')
d = json.loads(t[i:])
rs = d['results']
print('total fields:', len(rs))
zero = [r for r in rs if r.get('userCount', 0) == 0]
print('userCount=0:', len(zero))
types = {}
for r in rs:
    types[r.get('type')] = types.get(r.get('type'), 0) + 1
print('types:', types)
cands = sorted(zero, key=lambda r: -r.get('coverage', 0))[:25]
for r in cands:
    print('%-46s cov=%-6s type=%-7s %s' % (r['id'], r.get('coverage'), r.get('type'), (r.get('description') or '')[:60]))
