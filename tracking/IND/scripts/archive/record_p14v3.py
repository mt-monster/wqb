import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_p14v3_verdict'] = {
    'multisim': '1IUwmtb2K4z9cjA1eTrMfrQN',
    'status': 'ERROR',
    'result': '8子模拟全ERROR(错误信息为空): 剔除vol1毒式后仍全灭, price_signal_dl内存在多个毒字段或数据质量问题',
    'next': '二分隔离: bisectA(8jiEx8DL4UiaYjKjdYJwnH=trend5/vol3/ts_av_diff(trend6)/ts_rank(trend3)) bisectB(1lBcVoema4Ou8AKcxpiWtea=trend3+vol0混合/vol5+trend1/trend2xvol4/ts_av_diff(vol6))',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
