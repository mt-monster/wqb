import json, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

d = json.load(open(r'D:\coding\traeCN_project\wqb\tracking\GBR\reference\gbr_predictive_starmine_fields.json', encoding='utf-8'))
fields = {f['id']: f for f in d.get('fields', [])}

exprs = json.load(open(r'D:\coding\traeCN_project\wqb\tracking\GBR\candidates\gbr_wave17_predictive_starmine_raw_exprs.json', encoding='utf-8'))
ids = set()
for e in exprs:
    for t in re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', e):
        if t in fields:
            ids.add(t)

print('fields used:', len(ids))
for fid in sorted(ids):
    f = fields[fid]
    cov = f.get('coverage') or 0
    tag = 'OK>=0.85' if cov >= 0.85 else 'LOW<0.85'
    print(f"{tag} cov={cov:.3f} uc={f.get('userCount'):>4} ac={f.get('alphaCount'):>4} {fid}")
