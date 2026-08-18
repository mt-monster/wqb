import json, io, sys, re
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\1f671caa.txt', encoding='utf-8'))
rs = d.get('results', [])
print('total', len(rs), 'removed_by_filter', d.get('sharpe_filter_removed'))
# 字段族统计(去掉尾部数字)
fams = Counter(re.sub(r'\d+$', '', r['id']) for r in rs)
print('--- families(top30) ---')
for f, c in fams.most_common(30):
    print(c, f)
print('--- good: cov>=0.8 & ac<=5 ---')
good = [r for r in rs if r.get('coverage', 0) >= 0.8 and r.get('alphaCount', 99) <= 5]
good.sort(key=lambda r: r['alphaCount'])
print('good', len(good))
for r in good[:50]:
    print(r['id'], '|cov', r['coverage'], '|ac', r['alphaCount'], '|', (r['description'] or '')[:70])
print('--- seasonal关键字字段 ---')
for r in rs:
    if 'season' in r['id'].lower() and r.get('coverage', 0) >= 0.8:
        print(r['id'], '|cov', r['coverage'], '|ac', r['alphaCount'], '|', (r['description'] or '')[:70])
print('--- 前缀大类(source×context) ---')
pfx = Counter()
for r in rs:
    m = re.match(r'^(analyst|pv_daily|pvdaily12m|pvweekly)(_[a-z]+)?', r['id'])
    pfx[m.group(0) if m else r['id'].split('_')[0]] += 1
for f, c in pfx.most_common(40):
    print(c, f)
print('--- 回归直出字段(regression, 连续值最可做) ---')
for r in rs:
    if 'regression' in r['id'] and r.get('coverage', 0) >= 0.8 and r.get('alphaCount', 99) <= 5:
        print(r['id'], '|cov', r['coverage'], '|ac', r['alphaCount'])
