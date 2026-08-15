import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_p19_p21_verdict'] = {
    'P19_ml_factor_proj': {'multisim': 'ksEQk3W051ocvHp97zRX3K', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.74, 最佳rank(change_6m_rating_revision) sh0.74/2y1.88但tvr仅3.37%衰减信号', 'verdict': '数据集判弱'},
    'P20_pattern_scores': {'multisim': 'COPtgDQ4DA94IC9eeKEHu', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.53, 图表形态相似度在KOR/D1无信号', 'verdict': '数据集判弱'},
    'P21_multi_source_model': {'multisim': '4grMpN88r4VP9Gd10KKcDaAq', 'status': 'COMPLETE',
        'result': '★爆发★ 4式零FAIL过首门: TOP multiply(rank(short_horizon_hedge3_quantile1_5d_pred),rank(price_volume_quantile1_20d_pred)) sh2.11/fit1.98/2y2.65/tvr15.39/mg17.67bp; rank(pv_q1_20d) sh1.61/fit1.35/2y2.35; regime2+short双腿 sh1.51; seasonal sh1.50',
        'verdict': '进入CW预审轮'},
    'note': 'P21是三层门槛v2盲区B(过门槛未攻清单)命中, 验证用户"会不会漏掉信号"质疑正确',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
