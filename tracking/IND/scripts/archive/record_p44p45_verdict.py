import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_p44p45_verdict'] = {
    'P44_analyst_base_ref_surprise': {'multisim': '3LxbRtbsf51x8CB6F5YArzJ', 'status': 'COMPLETE',
        'result': '判弱: 8式sh∈[-0.56,0.19]且全CW FAIL; consensus surprise快照在KOR无横截面信号',
        'verdict': 'analyst_base_ref判弱关闭'},
    'P45_model262_implied_funda': {'multisim': '47AEEe1vf508aSXS1h8w9xH', 'status': 'COMPLETE',
        'result': '判弱: 最佳-cur_mae sh0.67/ebt_av_diff sh0.49, 距1.58太远',
        'verdict': 'model262市场隐含基本面KOR信号弱, 判弱关闭'},
    'wave28_streak': 'P41-P45连续5批判弱: analyst_consensus/acquisition/forum/surprise/implied_funda',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
