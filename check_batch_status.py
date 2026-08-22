import os, requests, base64, json
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

s = requests.Session()
credentials = os.environ['CREDENTIALS_EMAIL'] + ':' + os.environ['CREDENTIALS_PASSWORD']
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': 'Basic ' + encoded}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
print('Auth:', r.status_code)

# Check RATIO batch with full response
batch_id = '3D0QTR5Dv4NjbjDYx1qyD6b'
r2 = s.get(f'https://api.worldquantbrain.com/simulations/{batch_id}', timeout=120)
print('Status code:', r2.status_code)
print('Response:', json.dumps(r2.json(), indent=2)[:2000])
