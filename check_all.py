import os, requests, json, base64
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

email = os.environ['CREDENTIALS_EMAIL']
pwd = os.environ['CREDENTIALS_PASSWORD']

s = requests.Session()
credentials = f'{email}:{pwd}'
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': f'Basic {encoded}'}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=30)
print('Auth:', r.status_code)

# 1. Check fundamental72 batch status
print('\n=== fundamental72 batch (3YSELyfnE4UZcvW9OeSghHF) ===')
r1 = s.get('https://api.worldquantbrain.com/simulations/3YSELyfnE4UZcvW9OeSghHF', timeout=30)
d1 = r1.json()
print('Status:', d1.get('status'))
children = d1.get('children', [])
print('Children count:', len(children))
for c in children:
    print(f'  {c}')

# Get children details
if children:
    print('\n--- Children details ---')
    for cid in children:
        rc = s.get(f'https://api.worldquantbrain.com/alphas/{cid}', timeout=30)
        dc = rc.json()
        sharpe = dc.get('is', {}).get('sharpe', 'N/A')
        fitness = dc.get('is', {}).get('fitness', 'N/A')
        turnover = dc.get('is', {}).get('turnover', 'N/A')
        status = dc.get('status', 'N/A')
        expr = dc.get('regular', '')[:80]
        print(f'  {cid}: Sharpe={sharpe}, Fitness={fitness}, TVR={turnover}, Status={status}')
        print(f'    Expr: {expr}...')

# 2. Check 9qXP7EMK PROD
print('\n=== 9qXP7EMK PROD ===')
try:
    r2 = s.post('https://api.worldquantbrain.com/alphas/9qXP7EMK/correlations/prod', timeout=60)
    print('Status:', r2.status_code)
    if r2.status_code == 200:
        d2 = r2.json()
        print('PROD:', d2.get('max', 'N/A'))
    else:
        print(r2.text[:300])
except Exception as e:
    print('Error:', e)

# 3. Check QP7r9YOM SELF
print('\n=== QP7r9YOM SELF ===')
try:
    r3 = s.post('https://api.worldquantbrain.com/alphas/QP7r9YOM/correlations/self', timeout=60)
    print('Status:', r3.status_code)
    if r3.status_code == 200:
        d3 = r3.json()
        print('SELF:', d3.get('max', 'N/A'))
    else:
        print(r3.text[:300])
except Exception as e:
    print('Error:', e)
