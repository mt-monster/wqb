import json

# 读取 campaign registry
with open('research-data/campaign_registry.json', encoding='utf-8') as f:
    reg = json.load(f)

# 检查 ASI 区域
if 'ASI' in reg.get('regions', {}):
    asi = reg['regions']['ASI']
    print('ASI 区域已存在')
    print('  campaigns:', list(asi.get('empirical', {}).get('campaigns', {}).keys()))
    print('  dead_ends:', len(asi.get('empirical', {}).get('dead_ends', [])))
    print('  wins:', len(asi.get('empirical', {}).get('wins', [])))
else:
    print('ASI 区域不在 registry 中')
    print('  可用区域:', list(reg.get('regions', {}).keys()))
    print('  pending_regions:', reg.get('pending_regions', []))
