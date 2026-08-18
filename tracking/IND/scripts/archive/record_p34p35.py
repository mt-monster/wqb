import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave26_p34p35_submit'] = {
    'P34_model37': {'multisim': '1IutcScJz565bnaGm5euOcR',
        'dataset': 'StarMine文本挖掘信用风险 79字段MATRIX cov0.64-0.65 低竞争(decay6/SECTOR)',
        'style': '信用质量/文本风险风格(与ML预测/NLP情感计数异源)',
        'exprs': 'global_rank/structural_grade/global+industry加/global-region差decay/structural×income乘积/country×sector乘积/-pd_pct/global×delta动量乘积'},
    'P35_model307': {'multisim': '1ITjVG2mF59ObwZyxDwkNZb',
        'dataset': '地理销售敞口 15 VECTOR字段 cov0.68 近零竞争(vec_avg, decay6/SECTOR)',
        'style': '地理敞口结构风格(US/中国/日本销售占比)',
        'exprs': 'us/cnax/-jp/us×(-cnax)乘积/axj_decay/us_delta/emea-us差/latam×(-unclass)乘积'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
