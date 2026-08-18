import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave29_p47_verdict'] = {
    'P47_gsm': {'multisim': '2tk0vG56d4l38A8U0W4XJxz', 'status': 'COMPLETE',
        'result': '★突破★ pv_weekly_monthqtr_60d_return_regression sh1.25/fit0.93/2y2.04/tvr15.38%/mg11.09bp 仅LOW_SHARPE; funda_regime_120d sh0.96次之; analyst族sh0.83-0.87; 5d族近零',
        'next': 'v2主攻pvweekly族+算子杠杆: 1wuKaba7S55Ba2BafpiNbBH'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
