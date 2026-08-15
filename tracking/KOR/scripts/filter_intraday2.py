import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\8669f9fd.txt', encoding='utf-8'))
rs = d.get('results', [])
good = [r for r in rs if r.get('coverage', 0) >= 0.8 and r.get('alphaCount', 99) <= 3]
# 信号类：相关性/偏离/不对称/深度比
sig = [r for r in good if any(k in r['id'] for k in ('corr_', 'skew', 'ratio', 'dev', 'diff', 'spread', 'imb', 'asym', 'conc', 'entropy'))]
print('sig_fields', len(sig))
for r in sig[:60]:
    print(r['id'], '|cov', r['coverage'], '|ac', r['alphaCount'], '|', (r['description'] or '')[:65])
