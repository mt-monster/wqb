import json

with open(r'D:\coding\traeCN_project\wqb\tracking\GBR\reference\gbr_other455_fields.json', encoding='utf-8') as f:
    data = json.load(f)

matrix_fields = [f for f in data['fields'] if f['type'] == 'MATRIX']
print(f'MATRIX fields count: {len(matrix_fields)}')
for f in matrix_fields:
    print(f"{f['id']} | cov={f['coverage']:.3f} | ac={f['alphaCount']}")
