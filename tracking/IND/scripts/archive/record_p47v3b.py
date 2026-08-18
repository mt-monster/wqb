import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave29_p47v3b_verdict'] = {
    'P47v3b_gsm_prob': {'multisim': '19prH610v4Bl92l12tvbuSyd', 'status': 'COMPLETE',
        'champion': 'wpaAzd25 regime_r5 quantile4-0 prob差 sh1.99/fit1.64/2y2.62/tvr18.5%/mg13.67bp/RN-sh1.16/ra0/CW全过',
        'others': 'ak18P0e1 monthqtr sh1.93; YPvOkVJv r20 sh1.75; YPvOkVzv multiply sh1.63; VkGLlrZA sh1.43; 8式中6过门槛',
        'prod_wall': '★wpaAzd25 PROD0.8363墙, 不可提交★ (ak18P0e1/YPvOkVJv预计同样撞墙, 不耗预筛)',
        'verdict': 'prob差结构比regression更强但PROD墙同构; v4最后尝试confscore族: 3PYFvF3f64DPaxrWeWgEune',
        'candidate_pool': 'wpaAzd25/ak18P0e1保留(结构极优待新杠杆)'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
