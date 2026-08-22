import os, requests, base64
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

s = requests.Session()
credentials = os.environ['CREDENTIALS_EMAIL'] + ':' + os.environ['CREDENTIALS_PASSWORD']
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': 'Basic ' + encoded}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
print('Auth:', r.status_code)

# Search for fields
for search_term in ['equity', 'revenue', 'net_income', 'income', 'bs_tot', 'is_q']:
    params = {
        'dataset.id': 'fundamental72',
        'region': 'MEA',
        'universe': 'TOP400',
        'delay': 1,
        'limit': 10,
        'search': search_term
    }
    r2 = s.get('https://api.worldquantbrain.com/data-fields', params=params, timeout=120)
    data = r2.json()
    print(f'\n=== {search_term} ===')
    if isinstance(data, list):
        for f in data[:8]:
            if isinstance(f, dict):
                fid = f.get('id', 'N/A')
                print(f'  {fid}')
            else:
                print(f'  {f}')
    else:
        print(f'  Response: {type(data)}')
