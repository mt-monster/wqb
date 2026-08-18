import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave24_p31_verdict'] = {
    'P31_model313': {'multisim': 'LlapqedF4K3cuF19rz3ZJjw', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.48且tvr结构性1.4%, 无形资产强度无信号', 'verdict': '数据集判弱关闭'},
}
d['wave24_turn_summary'] = {
    'milestone': '★战役首个提交成功alpha: WjAxxZVk ACTIVE (multi_source_model, KOR/D1/MODEL金字塔点亮)',
    'progress': '1/3 可提交alpha',
    'datasets_closed_this_turn': ['ml_factor_proj(含latent族)', 'pattern_scores', 'event_stock_model', 'model252', 'quant_factor_lib', 'model140', 'analyst_revision_horizons(信号真实但tvr结构性3.9%)', 'model313', 'continuation_score(同族跳过)'],
    'key_learnings': ['multiply(rank,rank)乘积骨架CW安全(战役首破)', 'ts_decay_linear是降PC辅助杠杆(0.7222→0.6999)', 'check_correlation本地免费预筛省配额', '慢信号sh/tvr跷跷板: 水平式高sh低tvr, delta激活后sh上限0.67'],
    'next_candidates': ['mmp_nlp_sentiment(Tier2 cov0.62/vs7/521字段)', 'model68(cov0.85/ac2/vs7)', 'model37/model307', 'analyst_consensus(需绕get_datafields超时)', 'multi_source_model confidence族/120d地平线二次挖掘'],
    'quota_state': '提交配额已用1/4(WjAxxZVk), 回测配额正常',
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
