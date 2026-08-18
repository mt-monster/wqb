import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave30_p49_error'] = {
    'P49_v1': {'multisim': '4yRWLA2He4xCbEQNN4Tuqd4', 'status': 'ERROR',
        'root_cause': 'analyst_consensus字段是event型VECTOR, rank不支持event输入; 需vec_avg聚合转matrix',
        'lesson': '已固化记忆: event VECTOR字段必须vec_*聚合后再进常规算子'},
    'P49_v2': {'multisim': '1BhMt46BC4Rqb3lrTIAAGyw', 'status': 'RUNNING',
        'fix': '全式套vec_avg: EPS-4w/3m修正/EBI-3m修正/ts_delta20/EPS surprise/NET surprise/-stddev分歧/flash差'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
