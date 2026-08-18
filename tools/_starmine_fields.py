import json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

d = json.load(open(r'D:\coding\traeCN_project\wqb\tracking\GBR\reference\gbr_predictive_starmine_fields.json', encoding='utf-8'))
fields = d.get('fields', [])
print('total fields:', len(fields))
print('data_type:', d.get('data_type'))

def cov(f):
    return f.get('coverage') or 0

fields.sort(key=lambda f: -cov(f))
print('\n== top 40 by coverage ==')
for f in fields[:40]:
    print(f"cov={cov(f):.3f} uc={f.get('userCount'):>4} ac={f.get('alphaCount'):>4} {f['id']:45s} {f.get('description','')[:60]}")

print('\n== ep_yield family ==')
for f in fields:
    if 'ep_yield' in f['id'] or 'starmine' in f['id'] or 'smest' in f['id']:
        print(f"cov={cov(f):.3f} uc={f.get('userCount'):>4} ac={f.get('alphaCount'):>4} {f['id']:45s} {f.get('description','')[:60]}")

print('\n== ar_m/arm family (analyst revision model) ==')
for f in fields:
    if f['id'].startswith('ar_m') or f['id'].startswith('arm_') or '_arm_' in f['id']:
        print(f"cov={cov(f):.3f} uc={f.get('userCount'):>4} ac={f.get('alphaCount'):>4} {f['id']:45s} {f.get('description','')[:60]}")
