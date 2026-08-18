import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave31_blindspot_audit'] = {
    'audit': '★盲区复查★ get_datasets全量192个 vs 台账diff: hit=83/miss=109; KOR金字塔仅亮analyst=1+model=1, 其余13类0亮',
    'miss_high_value': ['ai_news_scores(5α低竞争)', 'dl_riskfree_returns(657α cov0.91 DL图表族)', 'news_sentiment_dl/nlp(0用户vs9)', 'sentiment23(transformer)', 'shortinterest6(拥挤)', 'other455(1500字段)'],
    'miss_rest': 'analyst10-86系/fundamental17-94系/news3-85系/pv13-70系/risk59-88系多为高竞争饱和集, 暂缓',
}
d['wave31_p51_p52_submit'] = {
    'P51_dl_riskfree': {'multisim': 'Xd9lcIR4uH9kR17UcRSyzP',
        'style': 'CNN图表深度学习预测族(5/20/60d horizon)',
        'exprs': '5d回归rank + 5d top-bottom prob差 + 3q_top ts_av + 20d decay10 + 20d动量(rev) + 5d delta + 60d双top加和 + 60d ts_rank'},
    'P52_ai_news_scores': {'multisim': '1R9Q1O43G5ilaIWoD1u9h8k',
        'style': 'AI新闻情绪(ASI prv2 D1族, cov0.373低竞争)',
        'exprs': 'pos-neg均值差/delta5/decay10/median差/ts_av5/delta1/pos+上界/反向neg-pos'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
