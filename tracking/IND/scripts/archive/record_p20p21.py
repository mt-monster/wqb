import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_p20p21_submit'] = {
    'P20_pattern_scores': {'multisim': 'COPtgDQ4DA94IC9eeKEHu',
        'dataset': '图表形态相似度 cov1.0 504字段全MATRIX 474零竞争 风格=技术形态(与此前评分类完全不同)',
        'exprs': 'rank(rising_wedge/falling_wedge)/楔形多空差/rank(upward_gap)/breakaway多空双腿/ts_av_diff(asc_triangle)/ts_rank(wedge,20)/support+breakaway双腿',
        'field_check': '8字段全部在get_datafields返回中验证存在'},
    'P21_multi_source_model': {'multisim': '4grMpN88r4VP9Gd10KKcDaAq',
        'dataset': '多源收益预测 cov0.93 60字段 MATRIX 分位数/regime/季节/hedge信号',
        'exprs': 'rank(short_term_q1_20d)/rank(pv_q1_20d)/regime2+short双腿/seasonal/long q1-q5价差/ts_av_diff/analyst+event_embedding双腿/hedge×pv乘积'},
    'analyst_earnings_ibes_skip': '28字段实为价格/成交量region分片复制品(pv1重复), 无增量信息, 跳过',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
