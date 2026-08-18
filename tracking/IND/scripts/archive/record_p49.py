import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave30_model252_dead'] = {
    'model252': '判死不回测: 仅3 VECTOR字段(mdl252_shield/shield2风险分+firm_market_value), 1个已被sharpe_filter移除',
    'tool_fix': '直连API分页拉取脚本fetch_ac_fields.py固化(绕MCP get_datafields翻页400bug+limit上限50); analyst_consensus 2343字段全量落盘ac_fields.json',
}
d['wave30_p49_submit'] = {
    'P49_ac_revision': {'multisim': '4yRWLA2He4xCbEQNN4Tuqd4',
        'style': '★分析师预测修正(revision)动量风格★ EPS/EBI共识当前vs4周前/3月前差值+surprise+分歧度',
        'exprs': 'EPS-4w修正/EPS-3m修正/EBI-3m修正/EPS ts_delta20/EPS surprise/NET surprise/-stddev分歧/flash-当前差'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
