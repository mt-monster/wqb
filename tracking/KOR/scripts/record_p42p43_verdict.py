import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_p42p43_verdict'] = {
    'P42_acquisition_model': {'multisim': 'ZOp6k4iz5iH8XhMoNsy5Nb', 'status': 'COMPLETE',
        'result': '判弱: 8式sh∈[-0.49,0.09], M&A标的概率在KOR呈负向(sector似然sh-0.39/mg-22bp)',
        'verdict': 'acquisition_model判弱关闭'},
    'P43_equity_forum_data': {'multisim': '1BHtJ58mZ4Ey9xbxZ3NAAx1', 'status': 'COMPLETE',
        'result': '判弱: 8式sh≤0.23且全CW FAIL; buy-sell差式恒等退化(tvr0); 论坛观点KOR无横截面信号',
        'verdict': 'equity_forum_data判弱关闭'},
    'blindspot2_probe': 'model50判死(54字段全被sharpe_filter移除); ai_factor_transfer=技术指标族降级; other327仅1字段ac13排除; other546 cov0.44-0.67过低后置',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
