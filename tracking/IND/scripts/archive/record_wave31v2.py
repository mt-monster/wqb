import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave31_p54_verdict'] = {
    'P54_sentiment23': {'multisim': '2iSYS0dzD4nObLB17O2TF7cY', 'status': '整批CANCELLED',
        'verdict': 'sentiment23判不可回测关闭(sharpe_filter剔154仅剩2字段+cov0.285)'},
    'root_cause': '★CANCELLED根因锁定: 数据集级不可回测★ cov<0.4的集(ai_news_scores 0.373/sentiment23 0.285/news_sentiment_dl 0.259除外)+dl_riskfree_returns(0.91但数据缺失)全CANCELLED; 对照multi_source_model(0.93)与news_sentiment_dl(0.259)COMPLETE打破单一coverage理论→实为字段KOR数据缺失',
    'rule_v1': 'KOR回测预筛: get_datafields后优先coverage≥0.6且sharpe_filter_removed少的数据集; 低coverage集先2式对照再全批',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
