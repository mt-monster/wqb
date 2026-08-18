import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave27_p40v3_verdict'] = {
    'P40v3_top20_leg_batch': {'multisim': '4DpofffiF50YbPGRtvK5pwa', 'status': 'COMPLETE',
        'result': '8式全强sh1.64-1.79/fit1.65-1.92/margin43-84bp零FAIL; 最佳2y: JjGkZ3KA双平滑sh1.77/2y1.46',
        'pc_audit': '9qp3LG0V基准PC0.7815 / JjGkZ3KA双平滑PC0.8301 / v2系0.7968-0.8361 → 全FAIL',
        'walls': '①PROD地板0.78-0.83字段级拥挤(生产池大量insider买卖比alpha), 平滑/换腿/换地平线均无效; ②2y墙1.46<1.6',
        'tvr_note': 'v3多数tvr<5%(3.6-6.4%), 亦不达标',
        'verdict': 'insider_feats信号极强但三墙(PROD/2y/tvr)结构性, 暂挂: 候选池保留JjGkZ3KA/9qp318Nd/kqPM76n8, 待新PC杠杆(异源场混合)再攻'},
}
d['wave27_turn_summary'] = {
    'progress': '1/3 可提交alpha(WjAxxZVk ACTIVE)',
    'this_turn_batches': 'P32-P40v3共9批: mmp_nlp/model68/model37/model307/model243/model144/other545/fund_holdings判弱; insider_feats爆发但三墙',
    'key_findings': ['盲区复查再发现3个未攻数据集(other545/fund_holdings/insider_feats)', 'insider_feats乘积骨架KOR爆发sh1.8+零FAIL', 'insider字段族PROD地板0.78+表达式无杠杆', 'get_datafields翻页400bug阻塞analyst_consensus/multifactor_return_pred'],
    'remaining_candidates': ['global_seasonal_model(cov0.94/ac132拥挤)', 'analyst_consensus(需绕工具)', 'news54 Key Developments(cov0.69)', 'MSM confidence族(同数据集不符目标)'],
    'quota_state': '提交配额1/4已用, 回测配额消耗较大',
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
