import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_v2_verdicts'] = {
    'P12v2': {'multisim': '2l325z4da4kUcw0UijgiEpQ', 'status': 'COMPLETE',
              'result': 'behavioral_signals判死: 8式全sh<=0.31 行为金融因子在KOR/D1无信号',
              'verdict': '数据集判死不再投入'},
    'P13v2': {'multisim': '4arowLf44JlacCzoonwN7y', 'status': 'COMPLETE',
              'result': 'ai_equity_alpha会计/分析师类8字段弱 sh<=0.52 全CW',
              'verdict': '转攻动量/情绪类字段(P15)'},
}
d['wave23_p14p15_submit'] = {
    'P14_price_signal_dl': {'multisim': '12LCrqg1u4U98LJVrgCEGul',
                            'dataset': 'MATRIX cov0.99 27/28字段零竞争 DL趋势/成交量指标',
                            'exprs': 'rank(trend1/3)/rank(vol0)/双腿混合/ts_av_diff(trend2,10)/ts_rank(vol1,20)/ts_av_diff+rank混合/rank乘积'},
    'P15_aieq_momentum': {'multisim': '2aYEyDf334RaaOb1e5jmQdws',
                          'exprs': 'combined_technical_indicators/target_price_deviation/buzz_trend/sentiment_score_7+混合+ts_av_diff+ts_rank+signed_power'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
