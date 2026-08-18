import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_gate_audit_v2'] = {
    'trigger': '用户质疑双门槛科学性, 重扫192数据集实证确有盲区',
    'blindspot_A_backfill_band': 'cov0.65-0.85被硬门槛排除但低竞争高valueScore: model313(cov0.83/ac7/vs6), model68(cov0.85/ac2/vs7), other545(cov0.84/ac28/vs6), quant_factor_lib(cov0.77/ac3/vs7), model140(cov0.79/ac1/vs6), model135(cov0.85/ac39), analyst_revision_horizons(cov0.66/ac27/vs7/1026字段), analyst_consensus(cov0.69/ac22/2343字段), mmp_nlp_sentiment(cov0.62/ac6/vs7/521字段), model37(cov0.62/ac5/vs7), model307(cov0.67/ac1/vs7)',
    'blindspot_B_unattacked_passed': '过门槛但此前未攻击: acquisition_model(cov0.99/ac6/vs7/15字段), equity_forum_data(cov0.89/ac=0/vs10/6字段), ml_factor_proj(cov1.0/ac13/vs7/333字段), analyst_earnings_ibes(cov1.0/ac6/28字段), ai_factor_transfer(cov1.0/ac9/20字段), event_stock_model(cov0.92/ac1/vs6), model252(cov0.90/ac3/vs6), multi_source_model(cov0.93/ac16/60字段), pattern_scores(cov1.0/ac41/504字段), continuation_score(cov1.0/ac49/560字段), model144(cov0.86/ac6), model243(cov1.0/ac32)',
    'gate_v2_rules': {
        'tier1': 'cov>=0.85 & alphaCount<=50 直接攻',
        'tier2': '0.65<=cov<0.85 & alphaCount<=50 & valueScore>=6 → 强制ts_backfill(66/120)补偿',
        'tier3': 'dataset级cov低但get_datafields个别字段cov高 → 字段级救援',
        'sharpe_filter': 'get_datafields默认filter_sharpe=true已滤OS/IS负sharpe字段, 返回即可信候选',
        'alphaCount_note': '平台级统计不分region, 用userCount辅助判局部竞争',
    },
    'attack_order': 'P17 acquisition_model + P18 equity_forum_data先行(vs10零竞争+vs7零竞争), 后续ml_factor_proj/analyst_earnings_ibes/tier2带',
}
d['wave23_p17p18_submit'] = {
    'P17_acquisition_model': {'multisim': 'f93Qb6lJ5cIcbqPS3iMuE9', 'dataset': 'M&A目标概率模型 cov0.99 15字段全VECTOR 大部分字段ac=0', 'exprs': 'rank(country/global likelihood)/sector+credit双腿/fundamental+valuation双腿/ts_av_diff/ts_rank/industry+text双腿/credit×sector乘积'},
    'P18_equity_forum_data': {'multisim': '3blFaL2oy57U8T2hDIdRAWV', 'dataset': '国际股票论坛活跃度 cov0.89 6字段全ac=0 valueScore10', 'exprs': 'rank(buy)/buy-sell差/ts_av_diff(comment)/buy+comment混合/rank(participants)/ts_rank(comment,20)/buy+participants加权/buy×comment乘积'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
