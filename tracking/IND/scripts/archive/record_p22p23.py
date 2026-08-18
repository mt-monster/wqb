import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_p22p23_submit'] = {
    'P22_multi_source_decorrelation': {'multisim': 'oDVyz4z24ir94gl08mL1kW',
        'goal': '避开pv_q1 crowded族(PC0.85), 用seasonal/regime2/hedge3/analyst/event_embedding/long_term场组乘积结构(CW安全模式)',
        'exprs': 'hedge3×seasonal/regime2×seasonal/analyst×hedge3/embedding×seasonal/hedge3+regime2双腿/long×hedge3/analyst×embedding/ts_av_diff(seasonal)'},
    'P23_event_stock_model': {'multisim': 'FKLkgfoM4gm9NR1e4QuMgAv',
        'goal': '盲区B收尾: 事件评分3字段VECTOR族vec_avg聚合(wave21已证路线可用)',
        'exprs': 'rank(corp_structure)/rank(earnings_event)/差式/双腿/ts_av_diff/ts_rank/乘积/event÷市值'},
    'cw_breakthrough_note': '★关键经验: multiply(rank(A),rank(B))乘积结构CW PASS, 是战役首个CW安全骨架; 后续所有批次优先乘积结构',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
