import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_FIRST_SUBMITTED_ALPHA'] = {
    'alpha': 'WjAxxZVk', 'status': 'ACTIVE/OS',
    'expr': 'multiply(rank(ts_decay_linear(short_horizon_hedge3_quantile1_5d_pred,10)),rank(short_term_seasonal_quantile1_20d_pred))',
    'dataset': 'multi_source_model', 'pyramid': 'KOR/D1/MODEL(1.7x)已点亮',
    'metrics': 'sh1.72/fit1.54/2y1.92/tvr11.24%/mg17.94bp/CLUSTER1.22/SUB_UNIV1.41/RN_sh1.02',
    'submission': '2026-08-15T06:33 全PASS: CW PASS+PROD_CORR 0.6999 PASS+SELF 0.0+DATA_DIVERSITY PASS+ra_failed=0',
    'properties': 'name=0.6999 color=GREEN tags=[PowerPoolSelected] 三段式英文描述已设',
    'key_path': '三层门槛v2盲区B命中→P21爆发→P22乘积骨架CW首破→P24 ts_decay_linear去PC(0.7222→0.6999)',
    'overfit_check': '年检6年全正(2018-2023 sh 1.41/2.04/0.49/2.71/3.23/0.85)无单年依赖',
    'progress': '1/3 可提交alpha达成',
    'recorded_at': '2026-08-15',
}
d['wave23_p24_verdict'] = {
    'P24_dePC_variants': {'multisim': '2Xmz0G3Ql52AalnONPS7mtL', 'status': 'COMPLETE',
        'result': '7式零FAIL: ts_delta变体sh1.90/1.86但PC 0.72-0.73未过; ★ts_decay_linear(hedge3,10)×seasonal WjAxxZVk sh1.72/fit1.54/2y1.92 PC0.6999全过★; 内细外粗gn双腿sh1.24(洗edge)',
        'lesson': 'ts_decay_linear平滑是降PC真杠杆之一(0.7222→0.6999)且不毁fitness; ts_delta/ts_av_diff提sh但PC不降'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
