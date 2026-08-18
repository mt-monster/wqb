import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave29_p47v5_verdict'] = {
    'P47v5_funda': {'multisim': '2beC2Eey84u8ah33HOsVYKS', 'status': 'COMPLETE',
        'result': 'funda基本面族全弱: 最佳confscore差sh0.85/2y1.66, prob差sh0.83; 全FAIL(LOW_SHARPE/FITNESS)',
        'verdict': '基本面模型预测在KOR无足够横截面信号'},
}
d['wave29_gsm_final'] = {
    'global_seasonal_model_final': '★关闭★ weekly价量模型族(regression/prob/confscore三表示)极强sh1.9-2.0/2y2.5+但PROD全饱和(0.836-0.921); funda/analyst族弱; 候选池: XgoxLn1z/wpaAzd25/ak18P0e1(结构极优待新杠杆)',
    'campaign_state': '1/3可提交(WjAxxZVk); 数据集空间基本穷尽: 25+数据集攻击, 仅剩异源盲区未探',
    'next_direction': ['model252/Tier2回填带(todo nextWave)', 'analyst_consensus剩余字段族', 'mmp_nlp_sentiment', 'PROD墙规避: 找非价量非模型预测的异源信号'],
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
