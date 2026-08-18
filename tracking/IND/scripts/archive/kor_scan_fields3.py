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

# 1) malta 模态(不同模型源)高分位
print('=== malta3/maltastar 高分位(未测) ===')
m = [i for i in ids if 'malta' in i and ('q4' in i or 'q5' in i or 'bucket3' in i or 'bucket4' in i)]
for i in m[:20]:
    print(i)

# 2) 5d/短周期 prob class 系列
print()
print('=== 短周期 r5/5d 系列 ===')
s = [i for i in ids if ('_r5_' in i or '_5d' in i or '5dret' in i) and ('q5' in i or 'q4' in i or 'class4' in i or 'prob4' in i)]
for i in s[:20]:
    print(i)

# 3) equity_star6 概率腿 p2/p3 (互补期限)
print()
print('=== probability/confidence 30d star6 系列 ===')
p = [i for i in ids if 'star6' in i and ('next30d' in i)]
for i in p[:20]:
    print(i)
