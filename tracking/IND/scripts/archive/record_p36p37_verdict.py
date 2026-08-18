import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave26_p36p37_verdict'] = {
    'P36_model243': {'multisim': '2m6iZObso5fTa9H1dgj0QYSN', 'status': 'COMPLETE',
        'result': '判弱: 有真实信号但天花板sh0.89(industry×delta动量乘积,2y1.16/tvr21.5%/mg5.8bp), 距1.58太远; country_rank反向sh-0.77',
        'verdict': 'Combined Alpha Model同行rank信号真实但弱, 数据集判弱关闭'},
    'P37_model144': {'multisim': '36NKOW7p24sZbKEkQLWxqwy', 'status': 'COMPLETE',
        'result': '判弱: sh<=0.74且最佳式2y=0.0, 双向全CW败',
        'verdict': 'StarPerformer深度学习分KOR无信号, 数据集判弱关闭'},
    'campaign_note': '白名单Tier1+盲区B+Tier2带已穷尽(除analyst_consensus工具阻塞/model135技术指标族), 第2alpha需另寻路径',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
