import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave30_p48_verdict'] = {
    'P48_mmp_nlp': {'multisim': '1RMXS5YZ4mFa7T57OdY4XF', 'status': 'COMPLETE',
        'result': '★判弱关闭★ sh∈[-0.32,0.41]; 最佳pos-neg情绪差仅sh0.41/2y0.05; 5式负向(bullish-bearish/目标价/评级多空全反向)',
        'verdict': 'mmp_nlp_sentiment韩国NLP新闻情绪无横截面信号(521字段cov1.0零竞争但信号密度为零), 关闭'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
