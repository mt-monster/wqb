import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_news54_verdict'] = {
    'news54_key_developments': {'status': '判弃(不回测)',
        'reason': '全量40字段全为时间戳/文本/flag, 唯一数值字段mws54_factor cov0.24过低, 无可用数值信号'},
}
d['wave28_tool_breakthrough'] = {
    'get_datafields_split': 'data_type=MATRIX/VECTOR拆分请求绕过2343字段超时: analyst_consensus MATRIX 18字段成功(targetprice族cov0.80)',
}
d['wave28_p41_submit'] = {
    'P41_analyst_consensus_targetprice': {'multisim': '1UBsX8cug4R1aHz14CP9sDJZ',
        'dataset': '★第2alpha主攻★ 分析师目标价共识 MATRIX18字段 cov0.80 近零竞争',
        'style': '分析师目标价风格(upside/revision/分歧, 与ML预测异源)',
        'exprs': 'upside/upside_delta22/upside×count/upside_decay10/dispersion/upside×dispersion/双平滑/max-min极差'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
