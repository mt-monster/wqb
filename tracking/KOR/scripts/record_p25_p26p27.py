import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave24_p25_verdict'] = {
    'P25_ml_factor_proj_latent': {'multisim': 'dTg6v3G44Kdc8F10Z0vt1Db', 'status': 'COMPLETE',
        'result': '判弱: 8式|sh|<=0.73且tvr结构性2.6-3.6%(除timing式), latent族(mean/log_variance_global_feature)慢信号双不达标, 与wave5 rating_revision族同死因', 'verdict': 'latent族关闭, ml_factor_proj最终判弱'},
}
d['wave24_p26p27_submit'] = {
    'P26_model252': {'multisim': '3ewTMo9wQ4At9ySOtoTfLHL',
        'dataset': 'SHIELD风险分 2 VECTOR字段 cov0.90 ac各1', 'exprs': 'rank/差式/乘积/ts_av_diff/ts_delta/ts_rank/decay_linear乘积(vec_avg聚合)'},
    'P27_quant_factor_lib': {'multisim': '4zG6ddc6j4HH9Y51cgZn4PAD',
        'dataset': '★Tier2回填带首攻★ 信用风险32 VECTOR字段 cov0.68-0.88 近零竞争 decay4压tvr',
        'exprs': 'ts_backfill(66/120)强制补偿+ts_delta/ts_av_diff换手增强+cassie×zscore乘积+prelim×longdebt_delta乘积'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
