# -*- coding: utf-8 -*-
"""查看 diversity_slots.py 约束 + 本地多样性状态"""
import sys, json, os
sys.path.insert(0, r'C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts')

# 1. diversity 约束文件
con = r'd:\coding\traeCN_project\wqb\tracking\KOR\config\diversity_constraints.json'
if os.path.exists(con):
    print('=== diversity_constraints.json ===')
    print(json.dumps(json.load(open(con, encoding='utf-8')), ensure_ascii=False, indent=1)[:1500])
else:
    print('no diversity_constraints.json, search config dir:')
    cfg = r'd:\coding\traeCN_project\wqb\tracking\KOR\config'
    for f in os.listdir(cfg):
        print(' ', f)

# 2. 参考目录里的约束
ref = r'd:\coding\traeCN_project\wqb\tracking\KOR\reference'
for f in os.listdir(ref):
    if 'divers' in f.lower() or 'slot' in f.lower() or 'method' in f.lower():
        print('REF:', f)
        try:
            print(json.dumps(json.load(open(os.path.join(ref, f), encoding='utf-8')), ensure_ascii=False, indent=1)[:1200])
        except Exception as e:
            print('  err', e)
