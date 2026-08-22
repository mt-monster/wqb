import os, requests, base64, json
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

s = requests.Session()
credentials = os.environ['CREDENTIALS_EMAIL'] + ':' + os.environ['CREDENTIALS_PASSWORD']
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': 'Basic ' + encoded}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=60)
print('Auth:', r.status_code)

# Get all fundamental72 fields
params = {
    'dataset.id': 'fundamental72',
    'region': 'MEA',
    'universe': 'TOP400',
    'delay': 1,
    'limit': 50,
    'offset': 0
}

all_fields = []
while True:
    r2 = s.get('https://api.worldquantbrain.com/data-fields', params=params, timeout=60)
    data = r2.json()
    if isinstance(data, list):
        all_fields.extend(data)
        if len(data) < 50:
            break
        params['offset'] += 50
    else:
        print('Unexpected response:', type(data))
        break

print(f'Total fields: {len(all_fields)}')

# Search for specific patterns
patterns = ['common_eq', 'tot_eq', 'rev', 'net_inc', 'oper_inc', 'ebitda', 'cash_from_oper', 'retain']
for pat in patterns:
    matches = [f['id'] for f in all_fields if pat in f.get('id', '').lower()]
    print(f'\n{pat}: {len(matches)} matches')
    for m in matches[:5]:
        print(f'  {m}')
