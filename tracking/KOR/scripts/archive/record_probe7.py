import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_probe7_verdict'] = {
    'multisim': '3fmIzK1Rx51hbUjm5oh4Qfk',
    'status': 'COMPLETE',
    'result': 'price_signal_dl字段可用: 基础式+rank(normalized_trend_indicator_1)腿 sh1.27; +ts_rank(volume_0,10)腿 sh0.97',
    'conclusion': 'P14毒源不在字段本身, 疑在ts_av_diff(rank(MATRIX),10)包裹顺序; P14v2已改rank(ts_av_diff(x,N))',
}
d['wave23_p14p15_submit']['P14v2'] = {'multisim': 'yfF4mdaF4AH9cW5BEC9TR9', 'design': '去毒重提: rank直用/ts_rank/双腿混合/rank(ts_av_diff)内包/rank乘积'}
d['wave23_p14p15_submit']['P16_model242'] = {'multisim': '48z6SK6A85as8BVKLqzLqLc', 'dataset': 'D1战术评分 cov1.0 sudden_volume_spike_score零竞争', 'exprs': 'rank(1mt/spike/momentum)/双腿混合/rank(ts_av_diff)/ts_rank/动量+季节混合/rank乘积'}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
