import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_p46_submit'] = {
    'shortinterest38_excluded': '韩国投资者买卖: 核心净买字段ac40-209极拥挤, 排除',
    'P46_intraday_pv_feats': {'multisim': '3dhGY6cg556Oca2vakkHJkj',
        'dataset': '★第2alpha主攻★ 日内微观结构 MATRIX574字段 cov0.99 568零竞争 223信号类字段',
        'style': '订单簿深度/微观结构风格(完全异源, 1.4x倍率)',
        'exprs': 'bid/ask深度比/-量价相关/vwap偏离/深度比delta5/深度比×vwap乘积/-slippage相关/综合深度比/vwap_av_diff5(decay4)'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
