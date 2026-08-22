import os, requests, json, base64, time
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
    print('Auth:', r.status_code)
    return s

s = make_session()

# 1. fundamental72 batch results
print('\n=== fundamental72 batch results ===')
r1 = s.get('https://api.worldquantbrain.com/simulations/3YSELyfnE4UZcvW9OeSghHF', timeout=60)
d1 = r1.json()
children = d1.get('children', [])
print(f'Children: {len(children)}')

results = []
for i, cid in enumerate(children):
    try:
        rc = s.get(f'https://api.worldquantbrain.com/simulations/{cid}', timeout=60)
        dc = rc.json()
        status = dc.get('status', 'N/A')
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
            results.append({'id': alpha_id, 'sharpe': sharpe, 'fitness': fitness, 'tvr': turnover, 'expr': expr})
        else:
            print(f'  [{i+1}/10] Sim {cid}: status={status}, no alpha yet')
    except Exception as e:
        print(f'  [{i+1}/10] Error: {e}')
        # Re-auth and continue
        try:
            s = make_session()
        except:
            pass

# 2. Check 9qXP7EMK PROD
print('\n=== 9qXP7EMK PROD ===')
try:
    r2 = s.get('https://api.worldquantbrain.com/alphas/9qXP7EMK/correlations/prod', timeout=120)
    print('Status:', r2.status_code)
    text = r2.text.strip()
    if text:
        d2 = json.loads(text)
        print('PROD max:', d2.get('max', 'N/A'))
    else:
        print('Empty - still computing')
except Exception as e:
    print('Error:', e)

# 3. Check QP7r9YOM SELF
print('\n=== QP7r9YOM SELF ===')
try:
    r3 = s.get('https://api.worldquantbrain.com/alphas/QP7r9YOM/correlations/self', timeout=120)
    print('Status:', r3.status_code)
    text = r3.text.strip()
    if text:
        d3 = json.loads(text)
        print('SELF max:', d3.get('max', 'N/A'))
    else:
        print('Empty - still computing')
except Exception as e:
    print('Error:', e)

# 4. Check QP7r9YOM PROD
print('\n=== QP7r9YOM PROD ===')
try:
    r4 = s.get('https://api.worldquantbrain.com/alphas/QP7r9YOM/correlations/prod', timeout=120)
    print('Status:', r4.status_code)
    text = r4.text.strip()
    if text:
        d4 = json.loads(text)
        print('PROD max:', d4.get('max', 'N/A'))
    else:
        print('Empty - still computing')
except Exception as e:
    print('Error:', e)

# Summary
print('\n=== SUMMARY ===')
for r in results:
    print(f'{r["id"]}: Sharpe={r["sharpe"]}, Fitness={r["fitness"]}, TVR={r["tvr"]}')
