import json

d = json.load(open('D:/coding/traeCN_project/wqb/tracking/GBR/reference/gbr_dl_riskfree_returns_fields.json', encoding='utf-8'))
fields = d['fields']
print(f'Total fields: {len(fields)}')

# High coverage fields
high_cov = [f for f in fields if f['coverage'] >= 0.9]
print(f'\n=== High coverage (>=0.9) fields: {len(high_cov)} ===')
for f in high_cov:
    print(f"  {f['id']}  cov={f['coverage']:.4f}  alphas={f['alphaCount']}  desc={f['description'][:100]}")

# Categorize
from collections import Counter
cats = Counter()
for f in high_cov:
    fid = f['id']
    if '2quantile' in fid: cats['2quantile'] += 1
    elif '3quantile' in fid: cats['3quantile'] += 1
    elif '4quantile' in fid: cats['4quantile'] += 1
    elif '5quantile' in fid: cats['5quantile'] += 1
    else: cats['other'] += 1

print('\n=== Quantile categories (high cov) ===')
for k, v in cats.most_common():
    print(f'  {k}: {v}')

# Horizon
horizons = Counter()
for f in high_cov:
    fid = f['id']
    for h in ['5day', '10day', '20day', '40day', '50day', '60day']:
        if h in fid:
            horizons[h] += 1
            break
    else:
        horizons['unknown'] += 1

print('\n=== Horizons (high cov) ===')
for k, v in horizons.most_common():
    print(f'  {k}: {v}')
