import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave28_p45_submit'] = {
    'P45_model262_implied_funda': {'multisim': '47AEEe1vf508aSXS1h8w9xH',
        'dataset': '★第3alpha主攻★ 市场隐含基本面DNN预测 MATRIX cov1.0 ni/fcf/rev/ebt_a/ttm_predict近零竞争',
        'style': '市场隐含基本面动量风格(与ML收益预测/分析师共识异源)',
        'exprs': 'ni_delta63/fcf_delta63/rev_delta63/-cur_mae/ni×rev动量乘积/ebt_av_diff22/fcf双平滑/隐含净利率'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
