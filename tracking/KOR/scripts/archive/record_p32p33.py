import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave25_p32p33_submit'] = {
    'P32_mmp_nlp_sentiment': {'multisim': '3Kn8gCLO5fR9CIsVJjdEKl',
        'dataset': '★第2alpha主攻★ NLP新闻情感 521字段514零竞争241cov>=0.6全MATRIX(decay6/SECTOR)',
        'style': '事件情感风格(与ML预测完全不同源)',
        'exprs': '正负情感差/bearish分/earnings×buy_rec乘积/analyst_ref_av_diff/buyback-bearish_topic/mild_pos_decay×important/opinion_delta/lvl0×two_pos乘积'},
    'P33_model68': {'multisim': '3uKTdAeZ64BKbRGcMDRK23L',
        'dataset': 'DREAM动量分 4 VECTOR字段 cov0.85近零竞争',
        'style': '风险调整动量风格',
        'exprs': 'rank(score/raw)/score-mktcap差/score×ram乘积/av_diff/delta/decay_linear×raw/ts_rank'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
