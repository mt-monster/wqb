import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave29_p47v2_verdict'] = {
    'P47v2_gsm': {'multisim': '1wuKaba7S55Ba2BafpiNbBH', 'status': 'COMPLETE',
        'champion': 'XgoxLn1z rank(weekly_pricevol_regime_r5_regression_pred) sh1.90/fit1.55/2y2.43/tvr18.42%/mg13.31bp/RN-sh1.11/ra0/CW全过',
        'runner_up': 'QPGAjVE5 rank(pv_weekly_cal_20d_return_regression) sh1.53/fit1.19/2y2.23',
        'prod_wall': '★PROD墙★ XgoxLn1z PROD0.8607, QPGAjVE5 PROD0.9208, 双双不可提交',
        'mutual_corr': '与WjAxxZVk互相关0.4535/0.486(超0.4标准), 两冠互相关0.8144',
        'verdict': 'weekly价量模型回归预测族PROD饱和(价格信息被生产alpha吃透); v3转攻prob/confscore族(信号结构不同): 2T2U3bdHj5h8ausQGbGQXZ',
        'candidate_pool': 'XgoxLn1z保留(结构极优, 待新杠杆或PROD池变化)'},
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
