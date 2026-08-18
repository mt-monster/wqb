import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave31_p53_verdict'] = {
    'P53_news_sentiment_dl': {'multisim': '2o6Inv2bF4M9cE313QJvl3E', 'status': 'COMPLETE',
        'result': '★判弱关闭★ sh∈[-0.59,0.18]全负向; perplexity最佳sh0.18/2y-0.77; tvr76-83%失控; margin全<2bp; inferess族在KOR无信号',
        'verdict': 'news_sentiment_dl关闭(0用户vs9但cov0.259+全VECTOR+信号为零)'},
}
d['wave31_cancelled_anomaly'] = {
    'P51_dl_riskfree': {'multisim_v1': 'Xd9lcIR4uH9kR17UcRSyzP', 'multisim_v2': '4dJer765z4vuaCIKXyQxoMJ', 'status': '两度整批CANCELLED(错误字段为空)'},
    'P52_ai_news_scores': {'multisim': '1R9Q1O43G5ilaIWoD1u9h8k', 'status': '整批CANCELLED'},
    'control_test': {'multisim': '4zUY7T2OL5hWbUR1c2cjQ9us', 'exprs': 'multi_source_model已知可用字段2式对照', 'purpose': '区分数据集级CANCELLED vs 账户级配额'},
    'notes': 'P53(news_sentiment_dl)同期COMPLETE排除并发理论; 重发429后等90s仍CANCELLED; 记忆df1d0607已录串行铁律',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
