import os, requests, json, base64, time
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

email = os.environ['CREDENTIALS_EMAIL']
pwd = os.environ['CREDENTIALS_PASSWORD']

s = requests.Session()
credentials = f'{email}:{pwd}'
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': f'Basic {encoded}'}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=60)
print('Auth:', r.status_code)

# 1. Check fundamental72 batch - get children simulation results
print('\n=== fundamental72 batch results ===')
r1 = s.get('https://api.worldquantbrain.com/simulations/3YSELyfnE4UZcvW9OeSghHF', timeout=60)
d1 = r1.json()
print('Status:', d1.get('status'))
children = d1.get('children', [])
print('Children count:', len(children))

for cid in children:
    # GET each child simulation
    rc = s.get(f'https://api.worldquantbrain.com/simulations/{cid}', timeout=60)
    dc = rc.json()
    status = dc.get('status', 'N/A')
    alpha_id = dc.get('alpha', 'N/A')
    
    if alpha_id and alpha_id != 'N/A':
        # Get alpha details
        ra = s.get(f'https://api.worldquantbrain.com/alphas/{alpha_id}', timeout=60)
        da = ra.json()
        sharpe = da.get('is', {}).get('sharpe', 'N/A')
        fitness = da.get('is', {}).get('fitness', 'N/A')
        turnover = da.get('is', {}).get('turnover', 'N/A')
        regular = da.get('regular', {})
        expr = regular.get('code', '')[:100] if isinstance(regular, dict) else str(regular)[:100]
        print(f'  {alpha_id}: Sharpe={sharpe}, Fitness={fitness}, TVR={turnover}')
        print(f'    Expr: {expr}...')
    else:
        print(f'  Sim {cid}: status={status}, alpha={alpha_id}')

# 2. Check 9qXP7EMK PROD (GET not POST)
print('\n=== 9qXP7EMK PROD ===')
try:
    r2 = s.get('https://api.worldquantbrain.com/alphas/9qXP7EMK/correlations/prod', timeout=120)
    print('Status:', r2.status_code)
    if r2.status_code == 200:
        text = r2.text.strip()
        if text:
            d2 = r2.json()
            print('PROD max:', d2.get('max', 'N/A'))
        else:
            print('Empty response - still computing')
    else:
        print(r2.text[:300])
except Exception as e:
    print('Error:', e)

# 3. Check QP7r9YOM SELF (GET not POST)
print('\n=== QP7r9YOM SELF ===')
try:
    r3 = s.get('https://api.worldquantbrain.com/alphas/QP7r9YOM/correlations/self', timeout=120)
    print('Status:', r3.status_code)
    if r3.status_code == 200:
        text = r3.text.strip()
        if text:
            d3 = r3.json()
            print('SELF max:', d3.get('max', 'N/A'))
        else:
            print('Empty response - still computing')
    else:
        print(r3.text[:300])
except Exception as e:
    print('Error:', e)

# 4. Check QP7r9YOM PROD
print('\n=== QP7r9YOM PROD ===')
try:
    r4 = s.get('https://api.worldquantbrain.com/alphas/QP7r9YOM/correlations/prod', timeout=120)
    print('Status:', r4.status_code)
    if r4.status_code == 200:
        text = r4.text.strip()
        if text:
            d4 = r4.json()
            print('PROD max:', d4.get('max', 'N/A'))
        else:
            print('Empty response - still computing')
    else:
        print(r4.text[:300])
except Exception as e:
    print('Error:', e)
