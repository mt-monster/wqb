import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave30_p48_submit'] = {
    'mmp_nlp_probe': 'MATRIX 521字段 cov1.0 全零竞争; NLP新闻情绪/评级/主题计数族(异源, 非价量非模型预测)',
    'P48_mmp_nlp': {'multisim': '1RMXS5YZ4mFa7T57OdY4XF',
        'style': '★NLP新闻情绪多空对差风格★(完全异源于WjAxxZVk模型金字塔)',
        'exprs': 'bullish-bearish/pos-neg/buy-sell推荐/目标价上调-下调/极强情绪计数/overweight-downgrade/outperform/情绪净zscore'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
