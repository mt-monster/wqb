import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave31_p55_p56_verdict'] = {
    'P56_probe': {'multisim': 'ASPgO5ZQ4K48UBzcENV8tU', 'status': 'COMPLETE',
        'result': 'shortinterest6探活OK: global/region rank均sh0.52/fit0.30/2y0.52'},
    'P55c_4expr': {'multisim': 'cV2I7WF4ql9SxY9psGKYd', 'status': 'COMPLETE',
        'result': 'sh∈[0.30,0.52]全弱: screening0.49/delta5_0.40/change0.30(2y-0.58)'},
    'verdict': '★shortinterest6判弱关闭★ SmartHoldings机构持仓预测在KOR信号弱(sh上限0.52); 但shortinterest类金字塔点亮候选失败',
    'batch_size_rule': '★★小批铁律★★ 限流期8式整批CANCELLED而2式/4式COMPLETE; 后续一律≤4式/批串行',
    'multisim_cancelled_chain': 'P55v1(3HV3sy9a94Ofbubj6tVz8mC 8式CANCELLED)→P55v2(21oY9jcAp57ua6tXAuy8CdD 8式CANCELLED)→P55c(4式COMPLETE)',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
