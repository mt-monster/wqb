import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave33_p65_structure'] = {
    'multisim': 'bWnPA4jH5cyauE1aUBm6geH', 'settings': 'SECTOR decay14 结构重构批', 'status': 'COMPLETE',
    'results': {
        'O0Gj6PqJ': {'expr': 'multiply(rank(prob4_5d),rank(20d回归))', 'sharpe': 2.83, 'fitness': 3.39,
            'two_year': 2.48, 'RN': 2.55, 'sub_universe': 2.57, 'margin_bp': 39.49, 'tvr': 0.0908,
            'ra': 0, 'CW': 'PASS', 'PROD': 0.8211,
            'note': '★★★战役全程最强alpha+族史最低PROD! multiply跨horizon组合双重突破'},
        'QPGAWkqw': {'expr': 'ts_delta动量', 'sharpe': 1.68, 'ra_failed': 1, 'status': '2y差15bp判弱'},
        'JjGk3Emm': {'expr': 'signed_power', 'sharpe': 1.52, 'ra_failed': 1, 'status': '判弱'},
        'j26JVRXj': {'expr': '双horizon叠加', 'sharpe': 1.49, 'ra_failed': 1, 'status': '判弱'},
    },
    'insight': '★multiply(rank,rank)跨horizon组合=PROD规避真杠杆(0.84→0.82)且指标暴涨; P66乘积变体批已发',
    'p66_batch': {'multisim': '1AMw9h14t4nZ98uBNQzkPeW', 'exprs': '3式multiply变体(差×回归/回归×20d差/decay差×回归)'},
    'auth_note': '本轮初遇401, MCP authenticate重登成功',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
