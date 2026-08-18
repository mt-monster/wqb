import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave32_p64_industry'] = {
    'multisim': '3uGj2O8Gy5a38N9nxao9eqx', 'settings': 'INDUSTRY decay10', 'status': 'COMPLETE',
    'results': {
        'O0GjWqeY': {'expr': '5d rank差', 'sharpe': 2.44, 'fitness': 2.85, 'two_year': 2.89, 'RN': 2.23,
            'sub_universe': 2.31, 'margin_bp': 31.34, 'tvr': 0.1088, 'ra': 0, 'CW': 'PASS',
            'PROD': 0.8778, 'note': '★★战役全程指标最强alpha, INDUSTRY中性化大幅提指标但不破PROD'},
        'j26JaWLo': {'expr': '20d prob差', 'sharpe': 2.17, 'fitness': 2.46, 'PROD': 0.8538},
        'KPGpgqx8': {'expr': 'rank(5d回归)', 'sharpe': 1.80, 'fitness': 1.89, 'PROD': '待核'},
        '2rpx5QQ8': {'expr': 'rank(20d回归)', 'sharpe': 1.86, 'fitness': 1.97, 'PROD': '待核'},
    },
}

d['wave32_final_summary'] = {
    'settings_space_map': {
        'decay_gradient_SECTOR': {'d6': 'PROD0.8587 sh2.30', 'd10': 'PROD0.8469 sh2.17', 'd14': 'PROD0.8379 sh2.07', 'trend': '边际递减渐近~0.83'},
        'INDUSTRY_d10': 'sh2.44战役最强指标但PROD0.8778反弹',
        'conclusion': 'dl_riskfree族PROD墙0.84-0.92结构性(墙极薄>0.7仅11-20/7.4万), 设置空间无法破0.7; 剩余手段仅结构重构(组合/差分/非线性)或等待PROD池更新',
    },
    'campaign_best_alphas': [
        'O0GjWqeY sh2.44/fit2.85 (INDUSTRY d10) PROD0.8778',
        'vRNbj8ar sh2.30 (SECTOR d6) PROD0.8587',
        '3qpOod1P sh2.17 (SECTOR d10) PROD0.8469',
        'N1bGNeQe sh2.07 (SECTOR d14) PROD0.8379族史最低',
    ],
    'deliverables_this_turn': [
        '★CANCELLED疑案终极破解+lookINTO_SimError_message工具发现(记忆df1d0607已修正)',
        '★字段名后缀陷阱固化(label3带_2/label0不带; ts_av不存在)',
        'dl_riskfree族新增6个全门槛过冠军(候选池累计14+)',
        'ai_equity_alpha初攻判弱(MODEL金字塔, sh≤0.80)',
    ],
    'progress': '1/3可提交(WjAxxZVk ACTIVE); dl_riskfree=第2数据集已穷尽设置空间待PROD突破; 第3数据集待攻(other455/ai_news_scores等)',
    'next_actions': ['dl_riskfree结构重构批(跨horizon组合/signed_power)攻PROD', 'other455(1500字段)攻击', 'P60二轮ai_equity_alpha变体'],
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
