import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave31_prod_check'] = {
    'vRNbj8ar': {'PROD': 0.8587, 'hist': '仅13/7.4万>0.7, 主体0-0.3', 'status': '墙但族整体低相关, P59变体待跑'},
    'wpaAjqX1': {'PROD': 0.9171, 'hist': '20/7.9万>0.7', 'status': '墙更高, 候选池保留'},
    'conclusion': 'dl_riskfree双冠全撞PROD墙, 与gsm三冠同构——KOR强信号族PROD饱和的结构性矛盾第4次复现',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
