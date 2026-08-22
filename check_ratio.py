import os, requests, base64
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

s = requests.Session()
credentials = os.environ['CREDENTIALS_EMAIL'] + ':' + os.environ['CREDENTIALS_PASSWORD']
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': 'Basic ' + encoded}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
print('Auth:', r.status_code)

# Check RATIO batch
r2 = s.get('https://api.worldquantbrain.com/simulations/3D0QTR5Dv4NjbjDYx1qyD6b', timeout=120)
d = r2.json()
print('Status:', d.get('status'))
children = d.get('children', [])
print('Children:', len(children))

for i, cid in enumerate(children):
    rc = s.get(f'https://api.worldquantbrain.com/simulations/{cid}', timeout=120)
    dc = rc.json()
    status = dc.get('status')
    alpha_id = dc.get('alpha', None)
    msg = dc.get('message', '')
    
    if status == 'ERROR':
        print(f'  [{i+1}] ERROR: {msg[:80]}')
    elif alpha_id:
        ra = s.get(f'https://api.worldquantbrain.com/alphas/{alpha_id}', timeout=120)
        da = ra.json()
        sharpe = da.get('is', {}).get('sharpe', 'N/A')
        fitness = da.get('is', {}).get('fitness', 'N/A')
        turnover = da.get('is', {}).get('turnover', 'N/A')
        print(f'  [{i+1}] {alpha_id}: Sharpe={sharpe}, Fitness={fitness}, TVR={turnover}')
    else:
        print(f'  [{i+1}] status={status}, alpha={alpha_id}')
