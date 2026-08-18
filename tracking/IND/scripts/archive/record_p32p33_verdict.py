import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave25_p32p33_verdict'] = {
    'P32_mmp_nlp_sentiment': {'multisim': '3Kn8gCLO5fR9CIsVJjdEKl', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.43, 最佳earnings_mention×buy_rec乘积sh0.13/tvr44.8%/mg0.66bp',
        'verdict': 'NLP情感计数在KOR/D1无横截面信号(高tvr低margin), 数据集判弱关闭'},
    'P33_model68': {'multisim': '3uKTdAeZ64BKbRGcMDRK23L', 'status': 'COMPLETE',
        'result': '判弱: 8式sh<=0.36全CW败, DREAM动量分KOR无信号', 'verdict': '数据集判弱关闭'},
    'note': '第2alpha累计P25-P33共9批全判弱; 剩余候选: model37/model307(Tier2 vs7零竞争), MSM confidence族/120d二次挖掘(需注意互相关<0.4)',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
