import json

with open(r'D:\coding\traeCN_project\wqb\tracking\GBR\reference\gbr_model264_fields.json', encoding='utf-8') as f:
    data = json.load(f)

# 查看 2l 字段的描述
print("=== mdl264_2l_* fields ===")
l2_fields = [f for f in data['fields'] if f['id'].startswith('mdl264_2l_')][:5]
for f in l2_fields:
    print(f['id'])
    desc = f.get('description', 'N/A')
    print(f"  desc: {desc[:100]}")
    print()

# 查看 3l 字段的描述
print("=== mdl264_3l_* fields ===")
l3_fields = [f for f in data['fields'] if f['id'].startswith('mdl264_3l_')][:5]
for f in l3_fields:
    print(f['id'])
    desc = f.get('description', 'N/A')
    print(f"  desc: {desc[:100]}")
    print()
