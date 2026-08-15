import json, sys, os, time
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.environ.get('WQ_ACE_LIB', r'C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts'))
import ace_lib
cfg = json.load(open(os.path.join(os.path.dirname(os.environ.get('WQ_ACE_LIB', r'C:/Users/MENGTAO/.workbuddy/skills/brain-simAlphasinBatch-and-track/scripts')), 'configs', 'config.json')))
for k, v in cfg.items():
    os.environ[str(k).upper()] = str(v); os.environ[str(k)] = str(v)
s = ace_lib.start_session()
API = ace_lib.brain_api_url

all_fields = {}
offset = 0
LIMIT = 50
while True:
    r = s.get(API + '/data-fields', params={
        'instrumentType': 'EQUITY', 'region': 'USA', 'delay': 1, 'universe': 'TOP3000',
        'limit': LIMIT, 'offset': offset, 'search': 'mdl177', 'dataset': 'quant_factor_lib'})
    d = r.json()
    res = d.get('results', d) if isinstance(d, dict) else d
    if not res:
        break
    for x in res:
        if isinstance(x, dict) and 'id' in x:
            all_fields[x['id']] = {
                'type': x.get('type'), 'coverage': x.get('coverage'),
                'alphaCount': x.get('alphaCount'), 'userCount': x.get('userCount'),
            }
    print(f"offset={offset} got={len(res)} total={len(all_fields)}", flush=True)
    if len(res) < LIMIT:
        break
    offset += LIMIT
    time.sleep(0.3)

print("TOTAL mdl177 fields:", len(all_fields))
json.dump(all_fields, open(os.path.join(ROOT, 'data_ref', 'mdl177_fields.json'), 'w'), indent=2)
print("saved to mdl177_fields.json")
# show field families (prefix before first '_' after mdl177)
from collections import Counter
fam = Counter()
for fid in all_fields:
    # mdl177[_N]_<family>...
    parts = fid.split('_')
    # parts[0]=mdl177, parts[1]=maybe 2 or family
    if len(parts) >= 3:
        fam['_'.join(parts[:3])] += 1
    else:
        fam[fid] += 1
print("\nTop families (mdl177_X_family):")
for k, v in fam.most_common(40):
    print(f"  {k}: {v}")
