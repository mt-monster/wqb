import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_p21_submit_attempt'] = {
    'alpha': 'mL5l7Yj9',
    'expr': 'multiply(rank(short_horizon_hedge3_quantile1_5d_pred),rank(price_volume_quantile1_20d_pred))',
    'result': '提交403: 仅PROD_CORRELATION FAIL(0.8496/0.7); 其余全PASS: CW PASS(战役首次!), SELF_CORR 0.0245, CLUSTER 1.43, SUB_UNIV 1.85, 2y 2.65, DATA_DIVERSITY PASS, REGULAR_SUBMISSION PASS(0/4)',
    'breakthrough': '★CW墙首次被击穿: multiply(rank,rank)乘积结构CW安全(对比KPGZmLMl嵌套add 23+变体全败)',
    'prod_corr_analysis': 'PROD相关0.85: 预测场分位数信号已被生产alpha池捕获, 需差异化: 短窗5d对冲场/季节场/regime场/analyst+embedding场',
    'quota': '403未消耗, 仍3/4',
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
