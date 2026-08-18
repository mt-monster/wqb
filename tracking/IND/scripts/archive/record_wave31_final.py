import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave31_p59_verdict'] = {
    'P59_v1': {'multisim': '4bBXMzeGL55Hc7W17Si8dzgX', 'status': 'CANCELLED'},
    'P59_v2': {'multisim': 's3PfU6eS4A1awcDiP2QYlM', 'status': 'CANCELLED'},
    'note': '限流升级: 2式也CANCELLED; 按铁律停止提交(连续2批串行CANCELLED)',
    'pending_exprs': ['rank(ts_rank(quantile_label_1bucket_5day_ohlcv_2,20))',
        'rank(probability_label3_4quantile_20day_ohlcv)-rank(probability_label0_4quantile_20day_ohlcv)'],
}
d['wave31_turn_summary'] = {
    'progress': '1/3可提交(WjAxxZVk) + ★候选池新增2个全门槛过冠军(vRNbj8ar sh2.30/wpaAjqX1 sh1.68, dl_riskfree_returns)★',
    'blindspot_audit': '192集diff出109漏网; 攻4个: news_sentiment_dl判弱/sentiment23不可回测/shortinterest6判弱(6式sh≤0.52)/dl_riskfree爆发',
    'key_breakthrough': '★dl_riskfree_returns=CNN图表图像DL族, KOR/D1/OTHER金字塔1.7x未亮; vRNbj8ar sh2.30/fit2.66/2y3.35/RN2.23/margin26.85bp/tvr13.2%全过, 仅PROD0.8587墙(直方图13/7.4万>0.7族整体低相关)',
    'cancelled_root_cause': '平台限流: 8式整批CANCELLED→4式可过→后期2式也CANCELLED; 串行+小批铁律固化(记忆df1d0607)',
    'candidate_pool': ['WjAxxZVk(已提交ACTIVE)', 'vRNbj8ar(PROD0.86)', 'wpaAjqX1(待PROD核)', 'XgoxLn1z/wpaAzd25/ak18P0e1(gsm PROD0.84-0.86)', 'insider_feats三墙×3'],
    'next_actions': ['限流解除后跑P59变体(ts_rank/20d)避PROD', 'wpaAjqX1 PROD核', 'other455(1500字段)待攻', 'ai_equity_alpha(582字段)待攻'],
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
