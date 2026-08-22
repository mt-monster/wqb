import os, requests, json, base64
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

email = os.environ['CREDENTIALS_EMAIL']
pwd = os.environ['CREDENTIALS_PASSWORD']

def make_session():
    s = requests.Session()
    credentials = f'{email}:{pwd}'
    encoded = base64.b64encode(credentials.encode()).decode()
    headers = {'Authorization': f'Basic {encoded}'}
    r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=60)
    return s

s = make_session()
print('Auth OK')

# 1. Check 9qXP7EMK PROD
print('\n=== 9qXP7EMK PROD ===')
try:
    r2 = s.get('https://api.worldquantbrain.com/alphas/9qXP7EMK/correlations/prod', timeout=120)
    text = r2.text.strip()
    if text:
        d2 = json.loads(text)
        print('PROD max:', d2.get('max', 'N/A'))
    else:
        print('Empty - still computing')
except Exception as e:
    print('Error:', e)

# 2. Check QP7r9YOM SELF
print('\n=== QP7r9YOM SELF ===')
try:
    r3 = s.get('https://api.worldquantbrain.com/alphas/QP7r9YOM/correlations/self', timeout=120)
    text = r3.text.strip()
    if text:
        d3 = json.loads(text)
        print('SELF max:', d3.get('max', 'N/A'))
    else:
        print('Empty - still computing')
except Exception as e:
    print('Error:', e)

# 3. Check QP7r9YOM PROD
print('\n=== QP7r9YOM PROD ===')
try:
    r4 = s.get('https://api.worldquantbrain.com/alphas/QP7r9YOM/correlations/prod', timeout=120)
    text = r4.text.strip()
    if text:
        d4 = json.loads(text)
        print('PROD max:', d4.get('max', 'N/A'))
    else:
        print('Empty - still computing')
except Exception as e:
    print('Error:', e)

# 4. Check fundamental72 POSITIVE batch
print('\n=== fundamental72 POSITIVE batch (1O62BbbzI4QS97tXXVTLFoY) ===')
try:
    r5 = s.get('https://api.worldquantbrain.com/simulations/1O62BbbzI4QS97tXXVTLFoY', timeout=60)
    d5 = r5.json()
    print('Status:', d5.get('status'))
    children = d5.get('children', [])
    print(f'Children: {len(children)}')
    
    for i, cid in enumerate(children):
        try:
            rc = s.get(f'https://api.worldquantbrain.com/simulations/{cid}', timeout=60)
            dc = rc.json()
            alpha_id = dc.get('alpha', None)
            if alpha_id:
                ra = s.get(f'https://api.worldquantbrain.com/alphas/{alpha_id}', timeout=60)
                da = ra.json()
                sharpe = da.get('is', {}).get('sharpe', 'N/A')
                fitness = da.get('is', {}).get('fitness', 'N/A')
                turnover = da.get('is', {}).get('turnover', 'N/A')
                regular = da.get('regular', {})
                expr = regular.get('code', '')[:80] if isinstance(regular, dict) else str(regular)[:80]
                print(f'  [{i+1}/10] {alpha_id}: Sharpe={sharpe}, Fitness={fitness}, TVR={turnover}')
                print(f'    {expr}')
            else:
                print(f'  [{i+1}/10] Sim {cid}: no alpha yet')
        except Exception as e:
            print(f'  [{i+1}/10] Error: {e}')
            s = make_session()
except Exception as e:
    print('Error:', e)
