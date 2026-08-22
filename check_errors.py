import os, requests, json, base64
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

email = os.environ['CREDENTIALS_EMAIL']
pwd = os.environ['CREDENTIALS_PASSWORD']

s = requests.Session()
credentials = f'{email}:{pwd}'
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': f'Basic {encoded}'}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
print('Auth:', r.status_code)

# Check error details for RATIO batch
print('\n=== RATIO Batch Errors ===')
r1 = s.get('https://api.worldquantbrain.com/simulations/3JQpoO2yZ4WEajxiEnJSHOi', timeout=120)
d1 = r1.json()
children = d1.get('children', [])

for cid in children[:3]:  # Check first 3
    rc = s.get(f'https://api.worldquantbrain.com/simulations/{cid}', timeout=120)
    dc = rc.json()
    print(f'\nSim {cid}:')
    print(f'  Status: {dc.get("status")}')
    print(f'  Error: {dc.get("error", "N/A")}')
    print(f'  Message: {dc.get("message", "N/A")}')
    # Check full response
    if 'regular' in dc:
        print(f'  Regular: {str(dc["regular"])[:100]}')

# Check error details for TS batch
print('\n=== TS Batch Errors ===')
r2 = s.get('https://api.worldquantbrain.com/simulations/1MJgHEf9B4EjccH1biDAd5nZ', timeout=120)
d2 = r2.json()
children2 = d2.get('children', [])

for cid in children2[:3]:  # Check first 3
    rc = s.get(f'https://api.worldquantbrain.com/simulations/{cid}', timeout=120)
    dc = rc.json()
    print(f'\nSim {cid}:')
    print(f'  Status: {dc.get("status")}')
    print(f'  Error: {dc.get("error", "N/A")}')
    print(f'  Message: {dc.get("message", "N/A")}')
