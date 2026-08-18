import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave30_p50_submit'] = {
    'model68_probe': 'DREAM动量模型 4 VECTOR字段 cov0.85: mdl68_score(主推)/ram(风险调整)/raw(原始)/mktcap; 信号字段全零竞争',
    'P50_model68': {'multisim': '3EJvnvcU34uVaOvX7mFvJxS',
        'style': '模型动量风格(vec_avg聚合)',
        'exprs': 'score/ram/raw rank + 252zscore + delta20 + decay10 + score-raw差 + score×ram乘积'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
