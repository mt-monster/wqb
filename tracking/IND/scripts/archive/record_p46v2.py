import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_p46_verdict'] = {
    'P46v1_intraday': {'multisim': '3dhGY6cg556Oca2vakkHJkj', 'status': 'COMPLETE',
        'result': 'v1判弱但有线索: vwap偏离sh0.64/2y1.05(tvr41%高); bid/ask深度比负向sh-0.55(镜像可做); 全CW FAIL',
        'next': 'v2镜像+decay10平滑压tvr: 3pyssq4yv5cT9slaBX4rxCh'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
