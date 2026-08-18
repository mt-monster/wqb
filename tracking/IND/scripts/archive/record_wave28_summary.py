import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_p46v2_verdict'] = {
    'P46v2_intraday': {'multisim': '3pyssq4yv5cT9slaBX4rxCh', 'status': 'COMPLETE',
        'result': 'vwap_decay10 sh0.78/2y0.70最佳; 深度比族2y1.06-1.09但sh≤0.52; 全CW FAIL; 镜像无效(-0.87/-0.94)',
        'verdict': 'intraday_pv_feats微观结构信号天花板sh0.78+CW结构性, 判弱关闭'},
}
d['wave28_turn_summary'] = {
    'progress': '1/3 可提交alpha(WjAxxZVk ACTIVE), 本轮0突破',
    'batches': 'P41-P46v2共8批全判弱: analyst_consensus目标价/acquisition M&A/论坛情绪/consensus surprise/model262隐含基本面/日内微观结构v1v2',
    'blindspot2_result': '第2轮盲区攻击全军覆没(零竞争≠有信号): 8个新数据集探测, 4个直接判弃(news54全时间戳/analyst_earnings_ibes价量重复/model50全负sharpe/shortinterest38拥挤)',
    'tool_notes': 'get_datafields data_type=MATRIX拆分法固化(绕过超时); search翻页400bug对>100结果必现',
    'remaining_candidates': ['global_seasonal_model(cov0.94/1.7x/ac132, 但与WjAxxZVk seasonal腿互相关风险)', 'MSM confidence族(同数据集不符目标)', 'insider_feats三墙暂挂'],
    'quota_state': '提交配额1/4已用, 回测配额本轮消耗8批',
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
