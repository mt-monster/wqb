import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave32_p60_ai_equity_alpha'] = {
    'multisim': 'aqGrnc5F4WfbIj1ebSO73OD', 'status': 'COMPLETE',
    'pyramid': 'KOR/D1/MODEL 1.7x(与已亮的model同格)',
    'results': {
        'A1G26awR': {'expr': 'rank(vec_avg(alpha_excess_return_forecast))', 'sharpe': -0.19, 'status': '负向'},
        'VkGLdarw': {'expr': 'rank(vec_avg(forecasted_alpha_ranking))', 'sharpe': 0.60, 'tvr': 0.797, 'status': '弱+高换'},
        'wpaA9ZdQ': {'expr': 'rank(vec_avg(pure_alpha_generation_metric))', 'sharpe': -0.75, 'status': '负向'},
        'omNXoLbb': {'expr': 'rank(vec_avg(alpha_score))', 'sharpe': 0.80, 'status': '最强但远不达标'},
    },
    'verdict': '初攻4式sh∈[-0.75,0.80]+CONCENTRATED_WEIGHT失败(VECTOR稀疏单股支配), 信号面弱; 待翻转/聚合变体二轮定终判',
}

d['wave32_turn_summary'] = {
    'major_findings': [
        '★CANCELLED疑案终极破解: 批内ERROR式(坏字段/坏算子)连坐取消兄弟任务, lookINTO_SimError_message下钻可定位; 此前"限流"诊断部分误判',
        '★字段名陷阱: KOR dl_riskfree label3_4quantile_20day带_2而label0不带; ts_av不存在(用ts_mean)',
        'P59修正批COMPLETE: E5GMpmAP sh2.01/fit2.31/2y2.80全过但PROD0.91墙(第3冠军入池); KPGpNVex sh1.65 PROD0.88墙',
        'P61结构变体: E5GMVW90(原始差)sh1.64全过但PROD0.91墙; decay/ts_delta式判弱',
        'P60 ai_equity_alpha初攻判弱(sh≤0.80, MODEL金字塔)',
    ],
    'candidate_pool': ['WjAxxZVk(已提交ACTIVE)', 'vRNbj8ar(PROD0.86)', 'E5GMpmAP(PROD0.91)', 'E5GMVW90(PROD0.91)',
        'KPGpNVex(PROD0.88)', 'wpaAjqX1(PROD0.92)', 'XgoxLn1z等gsm三冠(PROD0.84-0.86)', 'insider_feats三墙×3'],
    'structural_conclusion': 'dl_riskfree族6个全门槛过alpha全撞PROD墙0.86-0.92, 但墙极薄(>0.7仅20/7.9万); 剩余规避手段: decay设置/中性化切换/跨horizon组合',
    'next_actions': ['P60二轮(翻转+组合变体)定终判', 'dl_riskfree设置空间规避PROD(decay/neutralization变体)', 'other455(1500字段)待攻'],
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
