import json
from collections import Counter

d = json.load(open('D:/coding/traeCN_project/wqb/tracking/GBR/reference/gbr_other455_fields.json', encoding='utf-8'))
fields = d['fields']
matrix_fields = [f for f in fields if f['type'] == 'MATRIX']
group_fields = [f for f in fields if f['type'] == 'GROUP']
print(f'Total: {len(fields)}, MATRIX: {len(matrix_fields)}, GROUP: {len(group_fields)}')
print()
print('=== MATRIX fields (usable in expressions) ===')
for f in matrix_fields[:60]:
    print(f"  {f['id']}  cov={f['coverage']:.4f}  alphas={f['alphaCount']}  desc={f['description'][:90]}")
print(f'... total {len(matrix_fields)} MATRIX fields')
print()

# Categorize by prefix
prefixes = Counter()
for f in matrix_fields:
    parts = f['id'].split('_')
    if len(parts) >= 3:
        prefixes['_'.join(parts[1:3])] += 1
    else:
        prefixes[parts[1] if len(parts)>1 else 'unknown'] += 1
print('=== MATRIX field categories (by prefix) ===')
for k, v in prefixes.most_common(30):
    print(f'  {k}: {v}')

# High coverage MATRIX fields
print()
print('=== High coverage (>=0.8) MATRIX fields ===')
high_cov = [f for f in matrix_fields if f['coverage'] >= 0.8]
for f in high_cov[:40]:
    print(f"  {f['id']}  cov={f['coverage']:.4f}  alphas={f['alphaCount']}")
print(f'... total {len(high_cov)} high-cov MATRIX fields')
