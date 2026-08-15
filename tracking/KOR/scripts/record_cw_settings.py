import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave23_cw_settings_verdict'] = {
    'S1_INDUSTRY': {'multisim': '2EuQuo9Gn56K99Seszq9syd', 'result': 'sh2.02/1.88 全CW+IS_LADDER失败'},
    'S2_MARKET': {'multisim': '3neu2E4U94w99sZwOjxzzPG', 'result': 'sh1.87/1.42 全CW+IS_LADDER失败'},
    'S3_SECTOR_decay10': {'multisim': '3Oq8s63wR4l59ggyd7EnFDV', 'result': 'sh1.98/1.90 全CW失败'},
    'final': '设置空间(INDUSTRY/MARKET/decay10)亦全CW失败。CW攻坚共计23+变体(结构17++设置6)全败, model170四腿CW墙判定为结构性不可修, KPGZmLMl留档sh2.03/2y2.09仅CW',
}
d['campaign_status_20260815_day']['submit_ready_count'] = 0
d['campaign_status_20260815_day']['blocked_by'] = 'KOR/D1市场级贫瘠+model170 CW结构墙: 5个零竞争数据集全判死/弱, 唯一强信号KPGZmLMl卡CW(23+变体全败), 需用户决策(region扩展 or 接受0/3)'

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
