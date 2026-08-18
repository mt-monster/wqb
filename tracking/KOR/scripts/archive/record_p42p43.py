import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_p41_verdict'] = {
    'P41_analyst_consensus_targetprice': {'multisim': '1UBsX8cug4R1aHz14CP9sDJZ', 'status': 'COMPLETE',
        'result': '判弱: 8式sh∈[-0.18,0.33], 目标价upside/分歧/revision在KOR/D1无横截面信号',
        'verdict': 'analyst_consensus targetprice族判弱关闭(VECTOR部分工具阻塞但主信号族已证伪)'},
}
d['wave28_blindspot2_discovery'] = {
    'finding': '★192全量复查第2轮盲区: acquisition_model/equity_forum_data从未攻击(1.7x倍率近零竞争)',
    'analyst_earnings_ibes': '判弃: 字段实为OHLCV价量重复(closing/return/volume dlr1/dlr2), 非真实IBES预测',
    'P42_acquisition_model': {'multisim': 'ZOp6k4iz5iH8XhMoNsy5Nb',
        'dataset': 'M&A标的概率模型 15字段VECTOR cov0.9937 12/15零竞争',
        'style': '并购标的概率风格(事件预测, 与ML收益预测/NLP情感异源)',
        'exprs': 'country/industry/sector似然/country×text乘积/country-size差/delta22/industry_decay/region_text×fundamental乘积'},
    'P43_equity_forum_data': {'multisim': '1BHtJ58mZ4Ey9xbxZ3NAAx1',
        'dataset': '散户论坛情绪 6字段VECTOR cov0.8948 全零alpha竞争 valueScore10',
        'style': '散户关注度/观点风格(行为金融, 完全异源)',
        'exprs': 'buy-sell观点差/纯buy/buy×参与人数/buy_delta5/人均评论强度/buy_decay/评论量×观点/参与人数delta10'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
