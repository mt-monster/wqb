import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave32_p63_decay14'] = {
    'multisim': '1D1y455Ll4onbO4KMmBxM9X', 'settings': 'decay=14', 'status': 'COMPLETE',
    'results': {
        'N1bGNeQe': {'expr': '5d rank差', 'sharpe': 2.07, 'fitness': 2.35, 'two_year': 3.02, 'margin_bp': 34.87,
            'tvr': 0.0925, 'ra': 0, 'CW': 'PASS', 'PROD': 0.8379},
        'omNXEoLm': {'expr': '20d prob差', 'sharpe': 1.85, 'fitness': 2.05, 'two_year': 2.59, 'margin_bp': 36.61,
            'ra': 0, 'PROD': 0.8886},
        '0mpLYjXp': {'expr': 'rank(20d回归)', 'sharpe': 1.58, 'fitness': 1.65, 'ra': 0, 'status': '压线过门槛待PROD'},
        '3qpOojX6': {'sharpe': 1.52, 'ra_failed': 1, 'status': '判弱'},
    },
    'decay_gradient': {'d6': 0.8587, 'd10': 0.8469, 'd14': 0.8379, 'conclusion': '边际递减(-0.012/-0.009), 渐近~0.83, decay梯度不足以破0.7'},
    'next': '中性化维度: INDUSTRY批(P64), dl_riskfree未试过',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
