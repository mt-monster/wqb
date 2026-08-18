import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_p17p18_verdict'] = {
    'P17_acquisition_model': {'multisim': 'f93Qb6lJ5cIcbqPS3iMuE9', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.48, M&A目标概率在KOR/D1无可用信号', 'verdict': '数据集判弱'},
    'P18_equity_forum_data': {'multisim': '3blFaL2oy57U8T2hDIdRAWV', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.59(buy-sell差式tvr=0退化), 零竞争valueScore10也弱', 'verdict': '数据集判弱'},
    'implication': '盲区候选补攻后仍弱, 市场级贫瘠结论强化: 连平台标注最高价值(vs10)的零竞争数据集在KOR/D1上限也仅0.6',
}
d['wave23_p19_submit'] = {
    'P19_ml_factor_proj': {'multisim': 'ksEQk3W051ocvHp97zRX3K',
        'dataset': 'ML因子投影 cov1.0 333字段全MATRIX 几乎全零竞争 valueScore7',
        'exprs': 'rank(12m_alpha/6m_rating_revision/real_earnings_surprise)/fy2_revision+动量双腿/ts_av_diff(1y_eps_growth)/ts_rank(50_200d)/rating+FF动量双腿/alpha×surprise乘积'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
