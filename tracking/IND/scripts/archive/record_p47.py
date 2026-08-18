import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave29_gsm_probe'] = {
    'global_seasonal_model': 'MATRIX 681字段 cov0.93-0.975 几乎全零竞争; 实际为模型预测族(analyst/pvweekly/funda × calendar/event/monthquarter/regime上下文)',
    'key_fields': 'funda_regime 60d/120d regression(cov0.975 ac1最强); analyst_event/monthquarter regression(ac0); regime_5d_return_regression; pv_weekly_monthqtr_60d',
    'risk_note': '与WjAxxZVk(multi_source_model)同为模型预测族, 出信号需compute_mutual_correlation验证<0.4',
}
d['wave29_p47_submit'] = {
    'P47_gsm': {'multisim': '2tk0vG56d4l38A8U0W4XJxz',
        'style': '全局季节/上下文模型回归预测rank(慢信号decay6)',
        'exprs': 'funda_regime_60d/120d, analyst_event_60d/120d, analyst_monthquarter_60d, pv_weekly_monthqtr_60d, regime_5d, event_5d 各rank'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
