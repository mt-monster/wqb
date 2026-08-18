import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave32_iso_test_verdict'] = {
    'iso_batch': {'multisim': '4grmlgbNj52QaZl1hxIouiho', 'status': 'ERROR',
        'child1_5day_known_good': '4sViGoK75jsalBigMbwA7n -> CANCELLED (限流再证)',
        'child2_20d_suspect': '1HbkBMcXH5ge9PxwGzoIo3v -> ERROR: unknown variable probability_label3_4quantile_20day_ohlcv'},
    'root_cause': '★字段名错误! KOR实际字段带_2后缀: probability_label3_4quantile_20day_ohlcv_2 (get_datafields确认存在,cov0.91). '
                  '此前P51v1/v2+P59v1-v4共6批CANCELLED疑案破解: unknown variable错误+限流连坐复合根因',
    'tool_discovery': '★lookINTO_SimError_message工具可深挖子任务error详情(message字段), 此前CANCELLED排查盲区关闭',
    'p59_fixed_batch': {'multisim': '3NDxpu3545908XPt6rOHIi0', 'exprs': [
        'rank(probability_label3_4quantile_20day_ohlcv_2)-rank(probability_label0_4quantile_20day_ohlcv)',
        'rank(ts_rank(winsorize(quantile_label_1bucket_20day_ohlcv),20))',
        'rank(ts_rank(quantile_label_1bucket_5day_ohlcv_2,20))'],
        'purpose': '20d horizon新信号面+ts_rank持仓结构, 攻PROD<0.7规避'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
