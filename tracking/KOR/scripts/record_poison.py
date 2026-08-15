import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['poison_nested_add_finding'] = {
    'killed_batches': ['P12 1W63Cc1u4Dxbanw25SJqWY', 'P13 Pcf7WaKU4D99i2MbGT4MUV', 'probe6 3Edt0p3mF4xSb9d11wOUkIaQ', '早前batchB 274sCj6wq4iqbnH7cCyuyTs同构'],
    'poison_pattern': 'add(multiply(rank(x),0.4),add(multiply(rank(y),0.3),multiply(rank(z),0.3))) 嵌套三腿add -> 整批CANCELLED',
    'bisect_evidence': [
        'probe2对照(安全式)COMPLETE sh1.9 -> 配额正常',
        'probe3替换腿批4式COMPLETE -> behavioral/aieq字段vec_avg直用与ts_backfill都合法',
        'probe4 4式COMPLETE -> ts_av_diff(rank)/ts_decay_linear(vec_avg)/multiply(rank,rank)无毒',
        'probe5 2式COMPLETE -> signed_power(rank,0.7)/ts_decay_linear(rank,20)无毒',
        'probe6 2式全为嵌套三腿add -> 整批CANCELLED实锤',
    ],
    'rule': 'FASTEXPR中add(multiply(rank(x),a),add(multiply(rank(y),b),multiply(rank(z),c)))嵌套结构高度疑似致CANCELLED; 三腿混合优先写成add(add(a,b),c)左结合',
    'counter_example': '蓝海批hKEkT6ZB50qbjUMJyduxN5的嵌套三腿式(含ts_rank(close,90) PV腿)曾COMPLETE; 差异可能在三腿同数据集rank相关性退化, 待P12v2/P13v2验证',
    'resubmit': {'P12v2': '2l325z4da4kUcw0UijgiEpQ', 'P13v2': '4arowLf44JlacCzoonwN7y'},
}

d['wave23_newfront_submit']['P12_behavioral']['status'] = 'CANCELLED(嵌套add毒),v2重提2l325z4da4kUcw0UijgiEpQ'
d['wave23_newfront_submit']['P13_aieq']['status'] = 'CANCELLED(嵌套add毒),v2重提4arowLf44JlacCzoonwN7y'

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
