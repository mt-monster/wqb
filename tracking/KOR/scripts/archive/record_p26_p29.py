import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave24_p26p27_verdict'] = {
    'P26_model252': {'multisim': '3ewTMo9wQ4At9ySOtoTfLHL', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.58全CW FAIL, SHIELD风险分无信号', 'verdict': '数据集判弱关闭'},
    'P27_quant_factor_lib': {'multisim': '4zG6ddc6j4HH9Y51cgZn4PAD', 'status': 'COMPLETE',
        'result': '判弱: Tier2回填带ts_backfill后8式|sh|<=0.56, 信用风险因子KOR/D1无信号', 'verdict': '数据集判弱关闭'},
    'continuation_score_skip': '560字段与pattern_scores同属图表形态相似度族(P20已判弱sh<=0.53), 跳过不浪费配额',
}
d['wave24_p28p29_submit'] = {
    'P28_model140': {'multisim': '2ucULxf0G4PIafQ11KxpPMfp',
        'dataset': '通胀敏感度3 MATRIX字段 cov0.79零竞争 Tier2 ts_backfill(66/120) decay4'},
    'P29_analyst_revision_horizons': {'multisim': 'pd9N05M04AO9Zovl4SbYkF',
        'dataset': '★Tier2大头★ 1026字段951零竞争571cov>=0.66, 选TOP10 cov1.0百分位/成分字段',
        'exprs': 'rank(model_score_long/short_term4)/乘积/差式/decay_linear乘积/ts_av_diff/双腿/三乘积'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
