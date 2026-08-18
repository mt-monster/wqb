import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_p14_bisect_final'] = {
    'bisectA': {'multisim': '8jiEx8DL4UiaYjKjdYJwnH', 'status': 'ERROR全灭',
                'exprs': 'rank(trend5)/rank(vol3)/rank(ts_av_diff(trend6,10))/ts_rank(trend3,20)',
                'note': '毒在trend3/5/6/vol3至少一个数据缺失'},
    'bisectB': {'multisim': '1lBcVoema4Ou8AKcxpiWtea', 'status': 'COMPLETE',
                'result': '全弱: ts_av_diff(vol6) sh0.22; trend2xvol4 sh-0.07; vol5+trend1 sh-0.13; trend3+vol0 sh-0.52'},
    'probe10': {'multisim': '4cZ77egUr4w6bRf3C4OQyPg', 'status': 'COMPLETE',
                'note': 'rank(returns)/ts_rank(close,10)纯安全式跑通, 配额正常实锤'},
    'price_signal_dl_final_verdict': '判弃: 可跑式全弱|sh|<=0.52(probe7腿1.27为孤例), 多字段数据缺失(vol1+trend系), 数据质量不过关',
}
d['wave23_cw_settings_space'] = {
    'design': 'CW突破最后变量空间: 此前17+变体全为表达式结构(SECTOR decay6固定), 现扫设置参数',
    'S1_INDUSTRY': {'multisim': '2EuQuo9Gn56K99Seszq9syd', 'exprs': 'KPGZmLMl原式 + 均匀权重0.25x4'},
    'S2_MARKET': {'multisim': '3neu2E4U94w99sZwOjxzzPG', 'exprs': 'KPGZmLMl原式 + PV腿加重0.4'},
    'S3_SECTOR_decay10': {'multisim': '3Oq8s63wR4l59ggyd7EnFDV', 'exprs': 'KPGZmLMl原式 + EM腿ts_decay_linear10平滑'},
    'kpgzmlml_code': 'add(add(add(multiply(rank(vec_avg(recent_earnings_momentum_score)),0.24),multiply(rank(ts_av_diff(vec_avg(annual_price_peak),10)),0.3)),multiply(rank(divide(vec_avg(latest_implied_valuation_price),vec_avg(prior_close_price))),0.26)),multiply(rank(ts_av_diff(ts_mean(pv106_spreadbp,5),110)),0.2))',
}
d['wave23_dataset_kill_list']['price_signal_dl'] = '判弃: bisectB可跑式全弱sh<=0.22 + trend系字段数据缺失(probe10证配额正常)'

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
