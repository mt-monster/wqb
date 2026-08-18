import json, io, sys
d = json.load(io.open(sys.argv[1], encoding='utf-8-sig'))
fs = d['fields']
hi = [f for f in fs if f['coverage'] >= 0.8]
print('cov>=0.8:', len(hi), '/', len(fs))
seen = {}
for f in sorted(fs, key=lambda x: -x['coverage']):
    parts = f['id'].split('_')
    p = parts[0] + '_' + parts[1] if len(parts) > 1 else f['id']
    if p not in seen:
        seen[p] = f
for k, f in list(seen.items())[:35]:
    print(f"{f['coverage']:.2f} ac={f['alphaCount']:3d} uc={f['userCount']:3d} {f['id']}")
