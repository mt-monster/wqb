import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave32_p59fix_verdict'] = {
    'multisim': '3NDxpu3545908XPt6rOHIi0', 'status': 'COMPLETE(字段名修正后首战全通)',
    'E5GMpmAP': {'expr': 'rank(probability_label3_4quantile_20day_ohlcv_2)-rank(probability_label0_4quantile_20day_ohlcv)',
        'sharpe': 2.01, 'fitness': 2.31, 'two_year_sharpe': 2.80, 'RN': 2.11, 'sub_universe': 1.87,
        'margin_bp': 27.13, 'tvr': 0.1214, 'ra_failed': 0, 'CW': 'PASS',
        'PROD': 0.9096, 'PROD_hist': '20/7.9万>0.7, 主体0-0.3', 'status': '★第3冠军, PROD墙, 候选池'},
    'KPGpNVex': {'expr': 'rank(ts_rank(quantile_label_1bucket_5day_ohlcv_2,20))',
        'sharpe': 1.65, 'fitness': 1.04, 'two_year_sharpe': 1.74, 'RN': 1.46, 'margin_bp': 7.96,
        'ra_failed': 0, 'PROD': 0.8762, 'PROD_hist': '仅3/7.9万>0.7 墙极薄', 'status': 'PROD规避候选'},
    'O0GjN6e1': {'expr': 'rank(ts_rank(winsorize(quantile_label_1bucket_20day_ohlcv),20))',
        'sharpe': 1.41, 'ra_failed': 3, 'status': '判弱'},
    'conclusion': 'dl_riskfree族第4次PROD墙复现但墙极薄(>0.7仅个位数), 深层结构变体规避空间真实',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
