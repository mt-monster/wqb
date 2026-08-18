import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave26_p38_submit'] = {
    'P38_other545': {'multisim': '150gHUadS4Vh9yez427nm8E',
        'dataset': 'NEMO2.0关联公司网络动量 4 VECTOR字段 cov0.8393 ac28(Tier2, ts_backfill补偿, decay6/SECTOR)',
        'style': '网络动量风格(文本链路NLP动量+价格动量合成, 与ML收益预测异源)',
        'exprs': 'score/-mpd双向/pln_omen×mpd乘积/score_decay/score×delta动量/backfill66/pln-mpd差/-mktcap×score乘积'},
    'field_discovery': '全量192数据集复查: other545/multifactor_return_pred从未攻击; chart_cnn(wave11判)/predictive_starmine(判死)已排除',
    'multifactor_return_pred_block': 'search=hedge/quantile1均>100条触发翻页400; 且与MSM同源架构(互相关风险>0.4), 降级',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
