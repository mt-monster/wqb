import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave30_p49v2_verdict'] = {
    'P49_v2_ac_revision': {'multisim': '1BhMt46BC4Rqb3lrTIAAGyw', 'status': 'COMPLETE',
        'result': '★判弱关闭★ sh∈[-0.27,0.51]; flash-当前差sh0.51最佳但2y0.52; EPS/EBI 3m修正sh0.35-0.42; surprise双负; tvr全极低(1.4-10%)事件稀疏',
        'verdict': 'analyst_consensus revision/surprise/分歧族在KOR无横截面信号(P41目标价+P49修正族全灭), 数据集关闭'},
}
d['wave30_turn_summary'] = {
    'progress': '1/3 可提交alpha(WjAxxZVk), 本轮0提交突破但候选池+3',
    'batches': 'P47v1-v5(gsm五连击: regression/prob/confscore/funda)+P48(mmp_nlp)+P49v1v2(ac revision)共8批',
    'key_finding': '★global_seasonal_model weekly价量模型族极强(sh1.9-2.0/fit1.5-1.6/2y2.4-2.6)但PROD全饱和(0.836-0.921), 三冠入候选池(XgoxLn1z/wpaAzd25/ak18P0e1)',
    'closed': 'global_seasonal_model/mmp_nlp_sentiment/model252(判死)/analyst_consensus',
    'lessons': ['datafields白名单外字段不存在(整批CANCELLED教训)', 'event VECTOR字段需vec_*聚合(固化记忆×2)', '直连API分页绕MCP翻页bug'],
    'remaining': ['model68(Tier2剩)', '候选池待新PROD杠杆', '换region备选'],
    'quota_state': '提交配额3/4剩余; 本轮消耗8批回测',
    'recorded_at': '2026-08-15',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
