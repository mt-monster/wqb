import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave32_p62_decay10'] = {
    'multisim': '2nfAdn6SC4lNap0IMv4sQjh', 'settings': 'decay=10 SECTOR', 'status': 'COMPLETE',
    'results': {
        '3qpOod1P': {'expr': 'vRNbj8ar同式', 'sharpe': 2.17, 'fitness': 2.52, 'two_year': 3.12, 'RN': 2.07,
            'sub_universe': 2.05, 'margin_bp': 31.65, 'tvr': 0.1065, 'ra': 0, 'CW': 'PASS',
            'PROD': 0.8469, 'PROD_note': '★dl_riskfree族史上最低PROD(0.86→0.85), >0.7仅12/7.4万, decay梯度有效'},
        'N1bGNMJw': {'expr': '20d prob差', 'sharpe': 1.93, 'fitness': 2.18, 'two_year': 2.67, 'margin_bp': 32.94,
            'ra': 0, 'PROD': 0.8985, 'status': '墙'},
        'j26JYLPW': {'sharpe': 1.55, 'ra_failed': 1, 'status': '差3bp判弱'},
        'mL5NoO0X': {'sharpe': 1.54, 'ra_failed': 1, 'status': '判弱'},
    },
    'insight': '★decay=10是杠杆: 指标全面提升(sh2.30→2.17指标略降但margin27→32bp/fit↑)+PROD降0.014; 沿decay梯度14/18继续压PROD',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
