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
    r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
    return s

s = make_session()
print('Auth OK')

def check_batch(batch_id, name):
    print(f'\n=== {name} ===')
    try:
        r = s.get(f'https://api.worldquantbrain.com/simulations/{batch_id}', timeout=120)
        d = r.json()
        print('Status:', d.get('status'))
        children = d.get('children', [])
        
        results = []
        for i, cid in enumerate(children):
            try:
                rc = s.get(f'https://api.worldquantbrain.com/simulations/{cid}', timeout=120)
                dc = rc.json()
                status = dc.get('status')
                alpha_id = dc.get('alpha', None)
                
                if status == 'ERROR':
                    msg = dc.get('message', 'N/A')
                    print(f'  [{i+1}] ERROR: {msg[:80]}')
                elif alpha_id:
                    ra = s.get(f'https://api.worldquantbrain.com/alphas/{alpha_id}', timeout=120)
                    da = ra.json()
                    sharpe = da.get('is', {}).get('sharpe', 'N/A')
                    fitness = da.get('is', {}).get('fitness', 'N/A')
                    turnover = da.get('is', {}).get('turnover', 'N/A')
                    regular = da.get('regular', {})
                    expr = regular.get('code', '')[:80] if isinstance(regular, dict) else str(regular)[:80]
                    print(f'  [{i+1}] {alpha_id}: Sharpe={sharpe}, Fitness={fitness}, TVR={turnover}')
                    results.append({'id': alpha_id, 'sharpe': sharpe, 'fitness': fitness, 'tvr': turnover, 'expr': expr})
                else:
                    print(f'  [{i+1}] Sim {cid}: status={status}')
            except Exception as e:
                print(f'  [{i+1}] Error: {str(e)[:50]}')
        return results
    except Exception as e:
        print(f'Error: {e}')
        return []

# Check both batches
r1 = check_batch('3D0QTR5Dv4NjbjDYx1qyD6b', 'RATIO Batch v2')
r2 = check_batch('1hWzELEc4Lfb0QammeyF37', 'TS Batch v2')

# Summary
print('\n=== SUMMARY ===')
print('\nRATIO Batch (sorted by Sharpe):')
for r in sorted(r1, key=lambda x: x.get('sharpe', 0) if isinstance(x.get('sharpe'), (int, float)) else -999, reverse=True):
    print(f"  {r['id']}: Sharpe={r['sharpe']}, Fitness={r['fitness']}, TVR={r['tvr']}")

print('\nTS Batch (sorted by Sharpe):')
for r in sorted(r2, key=lambda x: x.get('sharpe', 0) if isinstance(x.get('sharpe'), (int, float)) else -999, reverse=True):
    print(f"  {r['id']}: Sharpe={r['sharpe']}, Fitness={r['fitness']}, TVR={r['tvr']}")
