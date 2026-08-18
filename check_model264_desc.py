import json

with open(r'D:\coding\traeCN_project\wqb\tracking\GBR\reference\gbr_model264_fields.json', encoding='utf-8') as f:
    data = json.load(f)

# 查看 class 字段的描述
class_fields = [f for f in data['fields'] if '_class' in f['id']][:10]
for f in class_fields:
    print(f['id'])
    desc = f.get('description', 'N/A')
    print(f"  desc: {desc[:100]}")
    print()

# 查看 1l 字段的描述
print("=== mdl264_1l_* fields ===")
l1_fields = [f for f in data['fields'] if f['id'].startswith('mdl264_1l_')][:10]
for f in l1_fields:
    print(f['id'])
    desc = f.get('description', 'N/A')
    print(f"  desc: {desc[:100]}")
    print()
