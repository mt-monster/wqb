import os, requests, base64, json
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

s = requests.Session()
credentials = os.environ['CREDENTIALS_EMAIL'] + ':' + os.environ['CREDENTIALS_PASSWORD']
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': 'Basic ' + encoded}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
print('Auth:', r.status_code)

# Check RATIO batch progress
print('\n=== RATIO Batch Progress ===')
r2 = s.get('https://api.worldquantbrain.com/simulations/3D0QTR5Dv4NjbjDYx1qyD6b', timeout=120)
print('Progress:', r2.json())

# Check TS batch top performer SELF/PROD
print('\n=== TS Batch Top: zqkwlOWK (Sharpe=0.09) ===')
alpha_id = 'zqkwlOWK'

# SELF
try:
    r3 = s.get(f'https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/self', timeout=120)
    text = r3.text.strip()
    if text:
        d3 = json.loads(text)
        print(f'SELF: {d3.get("max", "N/A")}')
    else:
        print('SELF: computing...')
except Exception as e:
    print(f'SELF Error: {e}')

# PROD
try:
    r4 = s.get(f'https://api.worldquantbrain.com/alphas/{alpha_id}/correlations/prod', timeout=120)
    text = r4.text.strip()
    if text:
        d4 = json.loads(text)
        print(f'PROD: {d4.get("max", "N/A")}')
    else:
        print('PROD: computing...')
except Exception as e:
    print(f'PROD Error: {e}')
