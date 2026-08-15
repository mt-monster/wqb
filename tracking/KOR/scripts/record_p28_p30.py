import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave24_p28p29_verdict'] = {
    'P28_model140': {'multisim': '2ucULxf0G4PIafQ11KxpPMfp', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.2, 通胀敏感度无信号', 'verdict': '数据集判弱关闭'},
    'P29_analyst_revision_horizons': {'multisim': 'pd9N05M04AO9Zovl4SbYkF', 'status': 'COMPLETE',
        'result': '★有信号★ rank(country_percentile_model_score_long) sh0.97/fit0.76/2y1.60/mg38.6bp但tvr仅3.94%结构性低; 乘积式sh0.96/tvr6.11',
        'verdict': '进入P30换手增强轮(decay0+ts_delta激活)'},
}
d['wave24_p30_submit'] = {
    'P30_arh_turnover_push': {'multisim': '2CGKxlgz64Tz90CnVYQXm2',
        'strategy': 'model_score_long主腿+ts_delta(22)/ts_av_diff(10)激活+decay0释放换手',
        'exprs': 'delta主腿/delta×delta乘积/av_diff/主腿×revision_delta/delta差式/decay_linear×rec_delta/revision_delta/delta双腿'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
