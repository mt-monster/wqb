import os, requests, base64, json
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

s = requests.Session()
credentials = os.environ['CREDENTIALS_EMAIL'] + ':' + os.environ['CREDENTIALS_PASSWORD']
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': 'Basic ' + encoded}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
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
    r2 = s.get('https://api.worldquantbrain.com/data-fields', params=params, timeout=120)
    data = r2.json()
    
    if isinstance(data, dict):
        results = data.get('results', [])
        all_fields.extend(results)
        if len(results) < 50:
            break
        params['offset'] += 50
    elif isinstance(data, list):
        all_fields.extend(data)
        if len(data) < 50:
            break
        params['offset'] += 50
    else:
        break

print(f'\nTotal fields: {len(all_fields)}')

# Filter and print relevant fields
keywords = ['equity', 'rev', 'income', 'ebitda', 'asset', 'liability', 'cash', 'debt', 'retain', 'dividend', 'sh_out', 'borrow']
for kw in keywords:
    matches = []
    for f in all_fields:
        if isinstance(f, dict):
            fid = f.get('id', '')
        else:
            fid = str(f)
        if kw.lower() in fid.lower():
            matches.append(fid)
    if matches:
        print(f'\n=== {kw} ({len(matches)}) ===')
        for m in matches[:10]:
            print(f'  {m}')

# Save all field IDs to file
with open('f72_fields.txt', 'w') as fout:
    for f in all_fields:
        if isinstance(f, dict):
            fout.write(f.get('id', '') + '\n')
        else:
            fout.write(str(f) + '\n')
print('\nSaved to f72_fields.txt')
