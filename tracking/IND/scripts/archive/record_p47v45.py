import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave29_p47v4_verdict'] = {
    'P47v4_gsm_confscore': {'multisim': '3PYFvF3f64DPaxrWeWgEune', 'status': 'COMPLETE',
        'result': 'confscore差族同样强: regime_r5 sh1.94/fit1.57/2y2.50, monthqtr sh1.88, calendar sh1.88, r20 sh1.70; 与prob族结构同构',
        'verdict': 'weekly价量模型族(prob/confscore/regression三种表示)全强但预计同撞PROD墙, 不再逐个预筛'},
}
d['wave29_p47v5_submit'] = {
    'P47v5_funda': {'multisim': '2beC2Eey84u8ah33HOsVYKS', 'fixed_bad_batch': '4sJrME36d4zdasEawm8Jzaq(funda_regime_60d_qtile0_prob不存在)',
        'rationale': '★funda基本面源族: PROD池与价量不同, 逃墙概率最高; cov0.975最高覆盖',
        'exprs': 'regime/month_quarter/event/calendar 120d/60d qtile4-0 prob差 + confscore差 + regression×prob乘积'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
