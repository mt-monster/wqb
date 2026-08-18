import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave27_p39p40_submit'] = {
    'P39_fund_holdings_panel': {'multisim': '4kTfi61VA521aBAPCYUdkT9',
        'dataset': '★机构基金持仓/交易流 30字段 cov0.955(MATRIX)/0.887(VECTOR) 大量零竞争(decay6/SECTOR)',
        'style': '机构拥挤度/资金流风格(与ML预测完全异源)',
        'exprs': 'boundary_usd/holding_value/holder_count/top_weighted×mean_weight乘积/tx_decay/tx_delta/-herfindahl集中度反向/stable_boundary×-tx_concentration乘积'},
    'P40_insider_feats': {'multisim': '1SGpic4i64uGaRk7tqF3w3g',
        'dataset': '内部人买卖特征 31 MATRIX字段 cov0.6757(Tier2, ts_backfill补偿)',
        'style': '事件驱动内部人交易风格',
        'exprs': 'top20_20d/all250_backfill120/top5×count60乘积/top20_60_decay/all20_delta/top5-all250差/top20_decay×delta动量/top20_volume10'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
