import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave24_p30_verdict'] = {
    'P30_arh_turnover_push': {'multisim': '2CGKxlgz64Tz90CnVYQXm2', 'status': 'COMPLETE',
        'result': '确认跷跷板: ts_delta激活提tvr(10-25%)但sh上限0.67; 慢信号水平式tvr3.9%结构性无解',
        'verdict': 'analyst_revision_horizons判弱关闭(信号真实但双不达标)'},
    'analyst_consensus_block': 'get_datafields 2343字段超时+search翻页400bug复现, 本轮跳过',
}
d['wave24_p31_submit'] = {
    'P31_model313': {'multisim': 'LlapqedF4K3cuF19rz3ZJjw',
        'dataset': '无形资产强度 iai/ico/ick 3数值字段 cov0.67-0.76 ts_backfill decay4'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
