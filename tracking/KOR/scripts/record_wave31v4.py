import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave31_p58_breakthrough'] = {
    'P58_dl_riskfree_probe': {'multisim': '1K9H0KePl521aTf1clzsh21m', 'status': 'COMPLETE',
        'star': '★★★dl_riskfree_returns爆发★★★ 此前CANCELLED纯属限流误判(对照法误读)',
        'champion': {'alpha': 'vRNbj8ar',
            'expr': 'rank(probability_label4_5quantile_5day_ohlcv_2)-rank(probability_label0_5quantile_5day_ohlcv_2)',
            'sharpe': 2.30, 'fitness': 2.66, 'two_year_sharpe': 3.35, 'turnover': 0.1321, 'margin_bp': 26.85,
            'RN_sharpe': 2.23, 'sub_universe': 2.16, 'ra_failed': 0, 'CW': 'PASS',
            'pyramid': 'KOR/D1/OTHER 1.7x 未点亮',
            'PROD': '0.8587墙(但直方图仅13/7.4万>0.7, 主体0-0.3, 信号族与PROD池整体低相关)'},
        'runner_up': {'alpha': 'wpaAjqX1', 'expr': 'rank(quantile_label_1bucket_5day_ohlcv_2)',
            'sharpe': 1.68, 'fitness': 1.80, 'two_year_sharpe': 2.78, 'margin_bp': 24.08},
        'style': 'CNN图表图像深度学习5d风险中性收益预测(与multi_source_model/gsm完全不同的模型源)'},
    'P59_variants': {'multisim': '4bBXMzeGL55Hc7W17Si8dzgX', 'purpose': 'PROD规避变体: ts_rank持仓结构+20d horizon',
        'exprs': 'ts_rank(5d回归,20) + 20d top-bottom prob差'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
