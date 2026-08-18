import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave32_p61_verdict'] = {
    'p61_v1': {'multisim': '1fNdEJ3UI4sl9ipq9g3bqXO', 'status': 'ERROR', 'cause': 'ts_av算子不存在→连坐取消3兄弟'},
    'p61_v2': {'multisim': '3Kq7m74EN4FZ8Y75rJImWjI', 'status': 'ERROR', 'cause': 'probability_label0_4quantile_20day_ohlcv_2不存在(label0无_2后缀,label3有)→连坐'},
    'p61_v3': {'multisim': 'CIS5i81Z4l18MRjDFMN1Ru', 'status': 'COMPLETE', 'note': '全验证字段批,连坐理论确证'},
    'results': {
        'E5GMVW90': {'expr': 'rank(prob4_5quantile_5day-prob0_5quantile_5day)原始差', 'sharpe': 1.64, 'fitness': 1.76,
            'two_year': 2.69, 'RN': 1.94, 'margin_bp': 24.38, 'ra': 0, 'CW': 'PASS', 'PROD': 0.9099, 'status': 'PROD墙候选池'},
        'MPGn0Rrz': {'expr': 'ts_decay_linear(差,8)', 'sharpe': 1.41, 'ra_failed': 1, 'status': '判弱(decay过度)'},
        'LLGw5a09': {'expr': 'ts_delta(20d回归,5)', 'sharpe': 1.37, 'ra_failed': 3, 'status': '判弱'},
    },
    'key_insight': '★CANCELLED真根因=批内ERROR式连坐取消兄弟(非限流)! lookINTO_SimError_message下钻可见; dl_riskfree全结构变体PROD墙0.86-0.91(墙薄>0.7仅20/7.9万)',
    'field_suffix_rule': 'KOR dl_riskfree: label3_4quantile_20day带_2, label0_4quantile_20day不带; ts_av不存在用ts_mean',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
