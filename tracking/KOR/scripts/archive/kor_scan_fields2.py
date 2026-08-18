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

# 做空方向候选: q1/q0 低分位 bucket0/bucket1 (做空高估)
print('=== 低分位(做空腿) ===')
low = [i for i in ids if ('q1_' in i or 'q0_' in i or 'bucket0_' in i or 'bucket1_' in i or 'quantile1' in i or 'quintile1' in i)
       and ('equity2b2' in i or 'confscore' in i or 'star' in i)]
for i in low[:30]:
    print(i)

print()
print('=== 100d/200d 长窗口高分位 ===')
lng = [i for i in ids if ('100d' in i or '200d' in i) and ('q5' in i or 'quantile5' in i or 'quintile5' in i or 'rank5' in i)]
for i in lng[:25]:
    print(i)

print()
print('=== img200d / img20d 系列全貌 ===')
img = [i for i in ids if i.startswith('img2') ]
for i in img[:30]:
    print(i)
