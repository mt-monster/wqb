import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_poison_final'] = {
    'poison_expr': 'ts_rank(normalized_volume_indicator_1,20) 或该字段数据缺失',
    'evidence': 'P14/P14v2/probe8三批全灭的共同唯一式; probe9(纯安全式2式)COMPLETE sh2.03排除配额',
    'probe8_multisim': '2V09BngAu4skajzr4He8Qv9',
    'probe9_multisim': '1o1Ny04Qk4zD8NPnLCRuS08',
    'probe9_note': 'KPGZmLMl再现sh2.03仅CW, 指标可复现性确认',
    'p14v3': {'multisim': '1IUwmtb2K4z9cjA1eTrMfrQN', 'design': '剔除volume_indicator_1毒式, 8式全新: trend5/vol3/双腿混合/rank(ts_av_diff trend6)/ts_rank(trend3,20)/ts_rank(vol5)+trend1/乘积/rank(ts_av_diff vol6)'},
}
d['wave23_dataset_kill_list'] = {
    'behavioral_signals': '判死 sh<=0.31',
    'ai_equity_alpha': '判弱 会计/动量/情绪三类字段 sh<=0.52',
    'model242': '判弱 CW全过但sh<=0.39',
    'model170_dividend_fields': '判死 sh<=1.01',
    'price_signal_dl': 'P14v3在飞, probe7示腿sh1.27有潜力',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
