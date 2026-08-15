import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave22P10_verdict'] = {
    'batchA': {
        'multisim': '3MSuF6adO56TbhYe9MGZn2f',
        'status': 'COMPLETE',
        'results': 'group_rank(sector) sh1.88/fit1.35; signed_power0.7 sh1.80/fit1.30; PV跨Category腿 sh1.71/fit1.15; ts_decay_linear60 sh1.62/fit1.15(IS_LADDER过) -> 全部CW失败',
        'conclusion': '手册算子修复法(平滑/摊权/压尾/跨Category)对model170 CW全无效。按手册终局建议更换alpha思路: 转蓝海字段批',
    },
    'batchB': {
        'multisim': '274sCj6wq4iqbnH7cCyuyTs',
        'status': 'ERROR(批内毒表达式致整批CANCELLED,再次验证记忆库规则)',
        'poison': '定位在 6腿扩散(slippage44/tcm44)/ts_mean10/ts_weighted_delay 三者之一, 拆分批B2(4qQQXh5wX4NV8FqQHPzp7bM)验证中',
    },
    'densify_status': '批A去掉densify后跑通,但densify未被单独对照100%洗清',
    'model170_CW_final': '17+变体(参数/平滑/摊权/压尾/跨Category/稀释腿)全部CW失败, model170的CW判定为结构性不可修(KPGZmLMl留档sh2.03/2y2.09)',
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
