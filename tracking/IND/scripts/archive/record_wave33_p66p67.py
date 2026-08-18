import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave33_p66_p67_verdict'] = {
    'p66_multiply_variants': {'multisim': '1AMw9h14t4nZ98uBNQzkPeW', 'status': 'COMPLETE 全判弱',
        'MPGng72k': 'sh1.50', 'qMNp5jwO': 'sh1.47', 'LLGw872v': 'sh1.36'},
    'p67_group_neutralize': {'multisim': 'gOWP27Ah4NCam185agaZcd', 'status': 'COMPLETE 双过门槛但PROD墙',
        '6XpQGjJK': {'expr': 'multiply(rank(gn(prob4_5d,subind)),rank(20d回归))', 'sharpe': 2.71, 'fitness': 3.06,
            'two_year': 2.76, 'RN': 2.45, 'margin_bp': 35.87, 'ra': 0, 'CW': 'PASS', 'PROD': 0.8631},
        '1YpRGXPJ': {'expr': 'rank(gn(multiply(...),subind))', 'sharpe': 2.45, 'fitness': 2.50, 'two_year': 2.46,
            'ra': 0, 'PROD': 0.8251},
        'conclusion': '二次中性化提指标但PROD不降(0.82-0.86), 与记忆c097335f论坛案例不同——dl_riskfree墙为信号本身与PROD池重叠'},
    'parallel_ok': '双批并行全COMPLETE, 限流理论进一步证伪(连坐理论成立)',
    'dl_riskfree_closure': '17+全门槛过alpha, PROD全0.82-0.92, 结构/设置/中性化三维空间穷尽; 数据集判定: 强但PROD饱和, 候选池封存待PROD池更新',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
