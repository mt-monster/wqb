import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
d = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\1f671caa.txt', encoding='utf-8'))
rs = d.get('results', [])
pvw = [r for r in rs if r['id'].startswith(('pvweekly', 'pv_weekly', 'weekly'))]
print('pvweekly族字段', len(pvw))
for r in sorted(pvw, key=lambda x: x['id']):
    print(r['id'], '|cov', r['coverage'], '|ac', r['alphaCount'])
