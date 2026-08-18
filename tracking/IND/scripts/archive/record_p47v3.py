import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave29_p47v3_error'] = {
    'P47v3_gsm': {'multisim': '2T2U3bdHj5h8ausQGbGQXZ', 'status': 'ERROR',
        'root_cause': 'pv_weekly_event_20d_return_quantile0_prob不存在(sharpe_filter只展示存活字段, 缺失字段≠可用); 一个坏字段导致整批CANCELLED',
        'fix': 'v3b全部改用1f671caa缓存白名单字段: 19prH610v4Bl92l12tvbuSyd',
        'lesson': '构造表达式必须逐字段核对get_datafields返回白名单, 禁止按命名规律推断字段存在'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
