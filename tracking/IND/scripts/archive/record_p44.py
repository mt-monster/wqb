import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_p44_submit'] = {
    'P44_analyst_base_ref_surprise': {'multisim': '3LxbRtbsf51x8CB6F5YArzJ',
        'dataset': '★第2alpha主攻★ 分析师共识快照 surprise族 cov0.6683 近零竞争(surprise_pct/diff/high-low全ac0)',
        'style': '盈利surprise风格(与ML预测完全异源)',
        'exprs': 'surprise_pct/surprise_av_diff66/surprise×est_count/vs_actual_diff/surprise_decay10/surprise_delta66/high-low极差/surprise×delta动量乘积'},
    'other553_deprioritized': '金融观点挖掘: est/sal族cov0.74有竞争(ac4-10), rec/ptg族cov0.48-0.58过低, 降级',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
