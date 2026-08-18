# JJ/KK 闸门评估 (一次性脚本)
import json, sys

p = r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-080\6dffc0ad.txt'
d = json.load(open(p, encoding='utf-8'))

files = [
    r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_news_batch_jj.txt',
    r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_snt22_batch_kk.txt',
    r'd:\coding\traeCN_project\wqb\tracking\USA\runs\usa_snt22_batch_ll.txt',
]
want = set()
for f in files:
    try:
        for ln in open(f, encoding='utf-8'):
            ln = ln.strip()
            if ln:
                want.add(ln)
    except FileNotFoundError:
        pass

rows = []
seen = set()
for a in d['results']:
    code = a.get('code', '').strip()
    if code not in want or code in seen:
        continue
    seen.add(code)
    m = a['metrics']; ra = a.get('ra', {})
    sh = m['sharpe']; fit = m['fitness']; tv = m['turnover']; mg = m['margin']
    y2 = m['two_year_sharpe']; rn = m.get('risk_neutralized_sharpe'); su = m.get('sub_universe_sharpe')
    ok = (sh > 1.58 and fit > 1 and y2 > 1.6 and mg > 0.0005 and 0.05 < tv < 0.30
          and rn is not None and rn > 1 and not ra.get('ra_failed'))
    rows.append((sh, a['id'], a['settings']['decay'], a['settings']['neutralization'][:3],
                 fit, tv, round(mg * 1e4, 1), y2, rn, su, int(ra.get('failed_ra_count', 0)), ok, code[:70]))
rows.sort(reverse=True)
hdr = ('sharpe', 'id', 'dc', 'neu', 'fit', 'tv%', 'm_bp', '2y', 'RN', 'subU', 'raF', 'OK', 'expr')
print(f'{hdr[0]:>6} {hdr[1]:>9} {hdr[2]:>2} {hdr[3]:>3} {hdr[4]:>5} {hdr[5]:>6} {hdr[6]:>5} {hdr[7]:>5} {hdr[8]:>5} {hdr[9]:>5} {hdr[10]:>3} {hdr[11]:>4} {hdr[12]}')
for r in rows:
    rn = r[8] if r[8] is not None else -99.0
    su = r[9] if r[9] is not None else -99.0
    tag = 'PASS' if r[11] else ''
    print(f'{r[0]:>6.2f} {r[1]:>9} {r[2]:>2} {r[3]:>3} {r[4]:>5.2f} {r[5]*100:>6.1f} {r[6]:>5.1f} '
          f'{r[7]:>5.2f} {rn:>5.2f} {su:>5.2f} {r[10]:>3} {tag:>4} {r[12]}')
print(f'matched {len(rows)} of {len(want)} wanted; PASS =', sum(1 for r in rows if r[11]))
