import requests
import json
import sys

# 读取 .env 获取凭证
env_path = r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env'
email = None
password = None
with open(env_path) as f:
    for line in f:
        if line.startswith('CREDENTIALS_EMAIL='):
            email = line.strip().split('=',1)[1].strip('"')
        elif line.startswith('CREDENTIALS_PASSWORD='):
            password = line.strip().split('=',1)[1].strip('"')

if not email or not password:
    print("ERROR: Missing credentials")
    sys.exit(1)

# 登录
s = requests.Session()
auth_resp = s.post('https://api.worldquantbrain.com/authentication', json={'email': email, 'password': password})
if auth_resp.status_code != 200:
    print(f"Auth failed: {auth_resp.status_code}")
    sys.exit(1)

# 获取 pattern_scores 字段
url = 'https://api.worldquantbrain.com/data-fields'
params = {
    'instrumentType': 'EQUITY',
    'region': 'GBR',
    'delay': 1,
    'universe': 'TOP700',
    'dataset.id': 'pattern_scores',
    'limit': 50,
    'offset': 0
}
r = s.get(url, params=params)
data = r.json()
print(f"Total fields: {data.get('count', 0)}")
for f in data.get('results', [])[:30]:
    print(f['id'])
