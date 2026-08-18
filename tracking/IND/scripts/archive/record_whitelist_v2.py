import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['dataset_first_strategy_20260815'] = {
    'user_diagnosis': 'KOR/D1贫瘠: 全候选池os_is_sharpe中位数0.2-0.5; 零竞争与高质量互斥(model313 cov0.76但信号弱, other571 cov0.26)。选集锁死上限sh~1.0。数据集问题放首要位置',
    'offline_pkg_evidence': 'WebData包KOR仅含analyst25_TOP600_D1(207字段 cov0.6-0.79 70%季度更新)。analyst25平台alphaCount=3231高竞争→排除',
    'blueocean_batch_verdict': {'multisim': 'hKEkT6ZB50qbjUMJyduxN5', 'result': '8式全灭: best d5ZvoYmx sh1.01/2y0.38(CW过但无信号); model170蓝海域字段无alpha→证实选集是第一瓶颈'},
    'new_whitelist_tier1': [
        {'id': 'behavioral_signals', 'cov': 0.8682, 'fields': 7, 'alpha': 0, 'user': 0, 'mult': 1.7, 'value': 9, 'why': '行为金融外推偏差因子 cov0.87+零竞争+value9 三项全满 首要目标'},
        {'id': 'ai_equity_alpha', 'cov': 1.0, 'fields': 582, 'alpha': 33, 'user': 14, 'mult': 1.7, 'why': 'ML收益预测 cov1.0 低竞争 宽字段库'},
        {'id': 'equity_forum_data', 'cov': 0.8948, 'fields': 6, 'alpha': 0, 'user': 0, 'mult': 1.7, 'value': 10, 'why': '论坛情绪 cov0.89零竞争 value10'},
        {'id': 'price_signal_dl', 'cov': 0.9742, 'fields': 28, 'alpha': 7, 'user': 6, 'mult': 1.7, 'why': 'DL价格信号 cov0.97 近零竞争'},
        {'id': 'model238', 'cov': 0.9945, 'fields': 44, 'alpha': 135, 'user': 64, 'mult': 1.7, 'why': 'SmartHoldings机构持仓预测 cov0.99 中竞争'},
        {'id': 'multi_source_model', 'cov': 0.9298, 'fields': 60, 'alpha': 16, 'user': 12, 'mult': 1.7, 'why': '多源收益预测 cov0.93 低竞争'},
        {'id': 'model242', 'cov': 1.0, 'fields': 5, 'alpha': 23, 'user': 14, 'mult': 1.7, 'why': '短期技术评分 cov1.0'},
    ],
    'tier2_probe': [
        {'id': 'predictive_starmine', 'cov': 0.9434, 'fields': 645, 'alpha': 41, 'why': '分析师关系DL cov0.94'},
        {'id': 'global_seasonal_model', 'cov': 0.9421, 'fields': 681, 'alpha': 132, 'why': '季节ality模型'},
        {'id': 'chart_cnn_alpha', 'cov': 0.8854, 'fields': 1010, 'alpha': 26, 'why': 'CNN图表alpha'},
        {'id': 'model31', 'cov': 0.986, 'fields': 156, 'alpha': 548, 'why': '盈利质量 高竞争备选'},
    ],
    'selection_rule': '双门槛: cov>=0.85 且 alphaCount<=50 (打破零竞争与高质量互斥)。先打behavioral_signals(三项全满)',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
