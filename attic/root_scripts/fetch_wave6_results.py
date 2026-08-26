import requests
import json
import time

# 从 config.json 读取凭证
config = json.load(open(r'C:\Users\MENGTAO\.qoder-cn\skills\brain-makeSomeGem\scripts\headless_runner\config.json'))
email = config['brain_email']
password = config['brain_password']
auth = (email, password)

# Wave 6 的 multisim ID 列表（从 pipeline 输出中获取）
multisim_ids = [
    '2LlUcHgUa4WVcmYbYENHOpS',  # batch4
    '2o4Q7gDA575ar391PzMpV5',  # batch2
    '28mull9114WNcM055NEUYeo',  # batch7
    '4Eu0ppgKh56yaggNAHeHPTr',  # batch3
    '3XNrAH7Ry4tYcDEiIBBCImk',  # batch6
    '3TQ4e99ya4mfcaRszGqVewo',  # batch5
]

print(f"查询 {len(multisim_ids)} 个 multisim 的结果...")

all_alphas = []

for ms_id in multisim_ids:
    url = f'https://api.worldquantbrain.com/multisimulations/{ms_id}'
    
    try:
        r = requests.get(url, auth=auth)
        if r.status_code == 200:
            data = r.json()
            alphas = data.get('alphas', [])
            print(f"  {ms_id}: {len(alphas)} 个 alpha")
            all_alphas.extend(alphas)
        else:
            print(f"  {ms_id}: HTTP {r.status_code}")
    except Exception as e:
        print(f"  {ms_id}: 错误 - {e}")
    
    time.sleep(1)  # 避免 429 错误

print(f"\n总共获取 {len(all_alphas)} 个 alpha")

# 保存结果
with open('wave6_alphas.json', 'w') as f:
    json.dump(all_alphas, f, indent=2)

print("结果已保存到 wave6_alphas.json")
