import json

# 读取 campaign registry
with open('research-data/campaign_registry.json', encoding='utf-8') as f:
    reg = json.load(f)

# 扩展 ASI 区域
if 'ASI' not in reg.get('regions', {}):
    reg['regions']['ASI'] = {
        'static': {
            'universe': ['TOP3000', 'MINVOL1M'],
            'default_neutralization': 'FAST',
            'notes': 'ASI_1 最佳中性化=FAST(sharpe0.629), 数据质量报告2026-08-19'
        },
        'assets': {
            'datasets': ['analyst94', 'analyst81', 'analyst39', 'analyst44', 'pv1', 'model110', 'fundamental23'],
            'high_priority': ['analyst94', 'analyst81'],
            'notes': '重点关注Analyst数据集(用户要求)'
        },
        'empirical': {
            'campaigns': {
                'analyst94': {'status': 'untried', 'note': 'sharpe0.666最高Analyst数据集'},
                'analyst81': {'status': 'untried', 'note': 'score0.692推荐榜,OS sharpe0.653'}
            },
            'dead_ends': [],
            'wins': [],
            'orphans': []
        }
    }
    # 从 pending_regions 移除
    if 'ASI' in reg.get('pending_regions', []):
        reg['pending_regions'].remove('ASI')
    
    # 原子写
    tmp = 'research-data/campaign_registry.json.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
    import os
    os.replace(tmp, 'research-data/campaign_registry.json')
    print('ASI 区域已扩展到 registry')
else:
    print('ASI 区域已存在')
