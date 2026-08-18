import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave27_p38p39_verdict'] = {
    'P38_other545': {'multisim': '150gHUadS4Vh9yez427nm8E', 'status': 'COMPLETE',
        'result': '判弱: 8式sh<=0.38, NEMO网络动量KOR无信号', 'verdict': '数据集判弱关闭'},
    'P39_fund_holdings_panel': {'multisim': '4kTfi61VA521aBAPCYUdkT9', 'status': 'COMPLETE',
        'result': '判弱: 持仓水平式sh<=0.38且tvr2-3%跷跷板(margin22-35bp达标); 交易流式全负',
        'verdict': '机构持仓拥挤度KOR无可用信号, 数据集判弱关闭'},
}
d['wave27_p40_breakout'] = {
    'P40_insider_feats': {'multisim': '1SGpic4i64uGaRk7tqF3w3g',
        'best': 'multiply(rank(buy_sell_ratio_top5_20d_filled),rank(buy_sell_tx_count_ratio_all_60d_filled))',
        'alpha_id': 'kqPM76n8',
        'metrics': '★sh1.70/fit1.82/2y1.33/tvr5.42%/margin52.5bp/零FAIL',
        'yearly': '10年全正(2014-2023 sh 1.76/3.16/2.13/2.27/0.73/0.84/1.17/2.94/2.04/0.81)近3年均1.94',
        'walls': '2y1.33<1.6 + PROD0.7854>0.7双墙',
        'sibling_strong': ['ts_decay(top20_60d,10) sh1.67/2y1.40/tvr3.1%', 'backfill(all_250d,120) sh1.48/2y1.27']},
    'P40v2_dedup_batch': {'multisim': '1Q6sN65M14RCbJdQRX9FXxc',
        'strategy': 'ts_decay_linear(10/20)单双腿平滑+250d地平线换腿+av_diff+top5_60d换腿 8式降PC修2y'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
