import json
P = r'd:\coding\traeCN_project\wqb\tracking\KOR\kor_d1_campaign_state.json'
d = json.load(open(P, encoding='utf-8-sig'))

d['wave30_p50_verdict'] = {
    'P50_model68': {'multisim': '3EJvnvcU34uVaOvX7mFvJxS', 'status': 'COMPLETE',
        'result': '★判弱关闭★ sh∈[-0.15,0.75]; 252zscore最佳sh0.75/2y0.41; 全CW FAIL; DREAM动量在KOR失效',
        'verdict': 'model68关闭; Tier2带(analyst_consensus/model313/model68/mmp_nlp_sentiment)全部清零'},
}
d['wave30_campaign_milestone'] = {
    'dataset_space': '★KOR/D1数据集空间基本穷尽★ 30+数据集攻击完毕: 1个可提交(WjAxxZVk)+候选池6个(XgoxLn1z/wpaAzd25/ak18P0e1/insider_feats三墙JjGkZ3KA等)',
    'structural_wall': '核心矛盾: 价量/模型预测族信号强但PROD饱和(0.78-0.92); 异源族(NLP/基本面/分析师修正/动量模型)在KOR信号密度为零',
    'next_options': ['等待PROD池变化后重试候选池(44h内配额释放)', '换region重启战役', '用户决策点'],
}

json.dump(d, open(P, 'w', encoding='utf-8-sig'), ensure_ascii=False, indent=1)
print('keys=', len(d))
