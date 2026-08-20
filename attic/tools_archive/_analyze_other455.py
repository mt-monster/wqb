import json

with open('tracking/GBR/reference/gbr_other455_fields.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

fields = data['fields']
matrix_fields = [f for f in fields if f['type'] == 'MATRIX']

# 按 coverage 排序，取高覆盖的 MATRIX 字段
high_cov = sorted(matrix_fields, key=lambda x: x.get('coverage', 0), reverse=True)[:40]
print('Top 40 MATRIX fields by coverage:')
for f in high_cov:
    print(f"  {f['id']}: cov={f.get('coverage', 0):.4f}, alphas={f.get('alphaCount', 0)}")

print()
print('--- Sample descriptions ---')
for f in high_cov[:10]:
    print(f"{f['id']}:")
    print(f"  {f.get('description', 'N/A')[:100]}")
    print()
