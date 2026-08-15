import json, glob, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
fs = glob.glob(r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\*.txt')
for p in fs:
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception:
        continue
    rs = d.get('results') if isinstance(d, dict) else d
    if not isinstance(rs, list) or not rs or not isinstance(rs[0], dict):
        continue
    keys = set(rs[0].keys())
    if 'pyramidMultiplier' in keys or ('alphaCount' in keys and 'fieldCount' in keys):
        print('DATASET_LIST:', p.split('\\')[-1], 'n=', len(rs))
