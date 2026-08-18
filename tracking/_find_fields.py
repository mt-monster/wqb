import json, io, sys
d = json.load(io.open(sys.argv[1], encoding='utf-8-sig'))
fs = d['fields']
keys = sys.argv[2].split(',')
for f in sorted(fs, key=lambda x: -x['coverage']):
    if any(k in f['id'] for k in keys):
        print(f"{f['coverage']:.2f} ac={f['alphaCount']} uc={f['userCount']} {f['id']}")
