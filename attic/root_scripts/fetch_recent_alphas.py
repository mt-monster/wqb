import requests
import json
import time
from datetime import datetime, timedelta

# 从 config.json 读取凭证
config = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\skills\brain-makeSomeGem\scripts\headless_runner\config.json'))
email = config['brain_email']
password = config['brain_password']
auth = (email, password)

# 查询最近 1 小时内创建的 alpha
url = 'https://api.worldquantbrain.com/users/self/alphas'
params = {
    'limit': 100,
    'offset': 0,
    'order': '-dateCreated'
}

print("查询最近创建的 alpha...")

all_alphas = []
offset = 0
limit = 100

while True:
    params['offset'] = offset
    
    try:
        r = requests.get(url, params=params, auth=auth)
        if r.status_code == 200:
            data = r.json()
            alphas = data.get('results', [])
            
            if not alphas:
                break
            
            # 过滤最近 1 小时的 alpha
            recent_alphas = []
            for alpha in alphas:
                created_at = alpha.get('dateCreated', '')
                if created_at:
                    # 解析时间戳
                    try:
                        created_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        if datetime.now(created_time.tzinfo) - created_time < timedelta(hours=1):
                            recent_alphas.append(alpha)
                    except:
                        pass
            
            all_alphas.extend(recent_alphas)
            print(f"  offset={offset}: {len(alphas)} 个 alpha, 其中最近 1 小时 {len(recent_alphas)} 个")
            
            if len(alphas) < limit:
                break
            
            offset += limit
            time.sleep(1)  # 避免 429 错误
        else:
            print(f"  HTTP {r.status_code}")
            break
    except Exception as e:
        print(f"  错误 - {e}")
        break

print(f"\n总共获取 {len(all_alphas)} 个最近 1 小时的 alpha")

# 过滤 pattern_scores 相关的 alpha
pattern_alphas = []
for alpha in all_alphas:
    code = alpha.get('code', '')
    if any(keyword in code for keyword in ['pattern', 'similarity', 'triangle', 'wedge', 'gap', 'reversal']):
        pattern_alphas.append(alpha)

print(f"其中 pattern_scores 相关的有 {len(pattern_alphas)} 个")

# 保存结果
with open('wave6_pattern_alphas.json', 'w') as f:
    json.dump(pattern_alphas, f, indent=2)

print("结果已保存到 wave6_pattern_alphas.json")

# 显示前 5 个结果
if pattern_alphas:
    print("\n前 5 个 pattern_scores alpha:")
    for i, alpha in enumerate(pattern_alphas[:5], 1):
        print(f"\n{i}. Alpha ID: {alpha.get('id')}")
        print(f"   Code: {alpha.get('code', '')[:80]}...")
        print(f"   Sharpe: {alpha.get('is', {}).get('sharpe')}")
        print(f"   Fitness: {alpha.get('is', {}).get('fitness')}")
