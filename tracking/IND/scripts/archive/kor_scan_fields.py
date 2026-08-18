import re, os, glob

cache_dir = r'C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7'
txt = ''
for f in glob.glob(os.path.join(cache_dir, '*.txt')):
    try:
        c = open(f, encoding='utf-8', errors='ignore').read()
        if 'cnn_predicted_prob_q5_bucket4_50d_equity2b2' in c:
            txt += c
    except Exception:
        pass

ids = sorted(set(re.findall(r'"id":\s*"([a-z0-9_]{8,})"', txt)))
print('total fields:', len(ids))
known = {
    'cnn_predicted_prob_q5_bucket4_50d_equity2b2',
    'cnn_predicted_prob_q4_bucket2_60d_equity2b2',
    'cnn_predicted_prob_q2_bucket0_60d_equity2b2',
    'img60d_return_quantile5_confscore3',
    'img60d_return_quantile5_confscore4',
    'img200d_return_quintile2_prob_leap1',
    'probability_rank5_next60d_return_p4_equity_star6',
    'cnn_confidence_score3_q5_50d_equity2b2',
}
cand = [i for i in ids if i not in known]
print('candidates:', len(cand))
# 优先: 高分位(q5/quintile5)+高置信(confscore4/star6/p4)+长窗口(50d/60d)
picks = [i for i in cand if ('q5' in i or 'quantile5' in i or 'quintile5' in i or 'rank5' in i)
         and ('confscore4' in i or 'star6' in i or '_p4' in i or 'bucket4' in i)]
print('--- top picks ---')
for i in picks[:40]:
    print(i)
print('--- q5 rest ---')
rest = [i for i in cand if i not in picks and ('q5' in i or 'quantile5' in i or 'rank5' in i)]
for i in rest[:40]:
    print(i)
