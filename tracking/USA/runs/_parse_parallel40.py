# 解析 5 并行批 40 条回测结果的闸门评估（一次性脚本）
import json

p = r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-080\78ec0fd8.txt'
d = json.load(open(p, encoding='utf-8'))
new40 = {
    'omN0Ebz2', 'A1G8Vpaw', 'QPGpvxlW', 'MPGNYE5M', 'blQ16mWM', 'zqNn3xJO', 'QPGpvx5W', 'e73Z5Ydl',
    'QPGp01mw', 'ak19ar2x', '1YpAWqVM', '1YpAWq16', 'WjA2lEnG', 'leWPaLkA', 'blQ1aYVK', 'omN0a1vm',
    'gJ8VeN0O', 'kqP6NpYK', 'E5GP6n2L', 'E5GP6nM1', 'WjA2OrRG', 'GrG5WjNx', 'd5ZrWJrX', 'e73Z5MZz',
    'N1blNZae', 'mL5WovmE', 'QPGpv8Kr', 'rK2MRxej', 'e73Z5jQE', '78zRLpoO', 'QPGpv8YG', 'leWPAmMn',
    '78zRL5Nv', '1YpAN8Zk', '6XpLdWKP', 'MPGNYE3k', 'mL5WoG61', 'O0GXALJ1', 'xANprL1w', '3qpvoKjz',
}
rows = []
for a in d['results']:
    if a['id'] not in new40:
        continue
    m = a['metrics']; ra = a.get('ra', {})
    sh = m['sharpe']; fit = m['fitness']; tv = m['turnover']; mg = m['margin']
    y2 = m['two_year_sharpe']; rn = m.get('risk_neutralized_sharpe'); su = m.get('sub_universe_sharpe')
    ok = (sh > 1.58 and fit > 1 and y2 > 1.6 and mg > 0.0005 and 0.05 < tv < 0.30
          and rn is not None and rn > 1 and not ra.get('ra_failed'))
    rows.append((sh, a['id'], a['settings']['decay'], a['settings']['neutralization'][:3],
                 fit, tv, round(mg * 1e4, 1), y2, rn, su, int(ra.get('failed_ra_count', 0)), ok, a['code'][:62]))
rows.sort(reverse=True)
hdr = ('sharpe', 'id', 'dc', 'neu', 'fit', 'tv%', 'm_bp', '2y', 'RN', 'subU', 'raF', 'OK', 'expr')
print(f'{hdr[0]:>6} {hdr[1]:>9} {hdr[2]:>2} {hdr[3]:>3} {hdr[4]:>5} {hdr[5]:>5} {hdr[6]:>4} {hdr[7]:>5} {hdr[8]:>5} {hdr[9]:>5} {hdr[10]:>3} {hdr[11]:>4} {hdr[12]}')
for r in rows:
    rn = r[8] if r[8] is not None else -99.0
    su = r[9] if r[9] is not None else -99.0
    tag = 'PASS' if r[11] else ''
    print(f'{r[0]:>6.2f} {r[1]:>9} {r[2]:>2} {r[3]:>3} {r[4]:>5.2f} {r[5]*100:>5.1f} {r[6]:>4.1f} '
          f'{r[7]:>5.2f} {rn:>5.2f} {su:>5.2f} {r[10]:>3} {tag:>4} {r[12]}')
print('found', len(rows), 'of 40; PASS =', sum(1 for r in rows if r[11]))
