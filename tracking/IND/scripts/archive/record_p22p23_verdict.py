import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_p22_p23_verdict'] = {
    'P22_multi_source_decorrelation': {'multisim': 'oDVyz4z24ir94gl08mL1kW', 'status': 'COMPLETE',
        'result': '★再爆发★ 7式零FAIL: TOP hedge3×seasonal VkGReXWY sh1.80/fit1.56/2y2.01/tvr14.0/mg15.0; hedge3+regime2 ak1gGorv sh1.75; analyst×hedge3 RRmvPNGd sh1.54/fit1.54/mg20bp; regime2×seasonal qMNwVnR2 sh1.51',
        'pc_precheck': '本地check_correlation预筛: VkGReXWY 0.7222(贴线!)/ak1gGorv 0.7846/RRmvPNGd 0.7922/qMNwVnR2 0.862 → 全军未破0.7',
        'verdict': 'hedge3×seasonal贴线0.7222, 进入P24去PC变体批'},
    'P23_event_stock_model': {'multisim': 'FKLkgfoM4gm9NR1e4QuMgAv', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.46且全CW FAIL, 事件评分VECTOR族无信号', 'verdict': '数据集判弱关闭'},
}
d['wave23_p24_submit'] = {
    'P24_dePC_variants': {'multisim': '2Xmz0G3Ql52AalnONPS7mtL',
        'target': 'hedge3×seasonal PC 0.7222→<0.7',
        'exprs': '双腿内细外粗gn(subindustry)/外层gn/三因子乘积(+embedding)/ts_decay_linear(hedge3)/ts_av_diff(hedge3,5)/ts_av_diff(seasonal,10)/ts_delta(seasonal,5)/单腿gn',
        'syntax': 'alpha-expression-verifier 4式抽验全valid'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
