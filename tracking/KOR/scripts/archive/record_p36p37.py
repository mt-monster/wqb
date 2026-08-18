import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave26_p34p35_verdict'] = {
    'P34_model37': {'multisim': '1IutcScJz565bnaGm5euOcR', 'status': 'COMPLETE',
        'result': '判弱: 8式sh<=0.45且tvr结构性2.2%(慢信号跷跷板), margin29bp但sh不达标',
        'verdict': 'StarMine信用文本风险KOR无可用信号, 数据集判弱关闭'},
    'P35_model307': {'multisim': '1ITjVG2mF59ObwZyxDwkNZb', 'status': 'COMPLETE',
        'result': '判弱: 8式sh<=0.37全CW败, emea-us差2y1.11但sh仅0.37',
        'verdict': '地理销售敞口季度静态数据KOR无横截面信号, 数据集判弱关闭'},
}
d['wave26_p36p37_submit'] = {
    'note': '门槛审计盲区清单复查: model135/model144/model243此前仅入清单未攻击, 本轮补攻',
    'P36_model243': {'multisim': '2m6iZObso5fTa9H1dgj0QYSN',
        'dataset': 'Combined Alpha Model分位rank 4 VECTOR字段 cov1.0(vec_avg, decay6/SECTOR)',
        'style': '综合模型同行相对强弱风格',
        'exprs': 'industry/-country/sector×industry乘积/industry-sector差decay/region_decay/industry×delta动量/country-region差/-country×sector_decay乘积'},
    'P37_model144': {'multisim': '36NKOW7p24sZbKEkQLWxqwy',
        'dataset': 'StarPerformer(wolfe_star)深度学习分 2字段 cov0.8586(decay6/SECTOR)',
        'style': '深度学习star performer风格',
        'exprs': 'score双向/predict双向/score_decay/score×delta动量/predict_delta/predict-score差'},
    'model135_deprioritized': '技术指标库137字段仅1个过sharpe_filter, 与价量族高相关, 后置',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
