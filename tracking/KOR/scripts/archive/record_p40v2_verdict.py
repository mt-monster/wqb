import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave27_p40v2_verdict'] = {
    'P40v2_dedup_batch': {'multisim': '1Q6sN65M14RCbJdQRX9FXxc', 'status': 'COMPLETE',
        'best': 'multiply(rank(top5_20d),rank(ts_decay_linear(count_all_60d,10))) alpha=9qp318Nd sh1.82/fit1.95/2y1.34/tvr4.52%/mg63.6bp',
        'pc_result': '9qp318Nd PC0.7968 FAIL; 78zrbvk1(250d腿 2y1.41) PC0.8361 FAIL; kqPM76n8(v1基准) PC0.7854',
        'conclusion': 'ts_decay_smooth仅降PC 0.03-0.04, 双墙仍在: PROD~0.8(生产池拥挤top5字段) + 2y1.34<1.6',
        'next': 'v3换腿top20字段族(竞争更少) 4DpofffiF50YbPGRtvK5pwa轮询中'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
