import os, requests, base64, json
from dotenv import load_dotenv
load_dotenv(r'D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.env')

s = requests.Session()
credentials = os.environ['CREDENTIALS_EMAIL'] + ':' + os.environ['CREDENTIALS_PASSWORD']
encoded = base64.b64encode(credentials.encode()).decode()
headers = {'Authorization': 'Basic ' + encoded}
r = s.post('https://api.worldquantbrain.com/authentication', headers=headers, timeout=120)
print('Auth:', r.status_code)

all_fields = []
offset = 0
while True:
    url = f'https://api.worldquantbrain.com/data-fields?dataset.id=fundamental72&region=MEA&universe=TOP400&delay=1&instrumentType=EQUITY&limit=50&offset={offset}'
    r2 = s.get(url, timeout=120)
    data = r2.json()
    results = data.get('results', [])
    all_fields.extend(results)
    print(f'Offset {offset}: got {len(results)} fields, total {len(all_fields)}')
    if len(results) < 50:
        break
    offset += 50

print(f'\nTotal fields: {len(all_fields)}')

# Find fields for ratio calculations
keywords = {
    'equity': ['equity', 'common_eq', 'tot_eq', 'shareholder'],
    'revenue': ['revenue', 'rev', 'sales', 'turnover'],
    'net_income': ['net_inc', 'net_income', 'earn_for_common', 'profit'],
    'operating_income': ['oper_inc', 'operating_income', 'ebit'],
    'total_assets': ['tot_asset', 'total_asset'],
    'cash_flow': ['cash_from_oper', 'oper_cash', 'cf_'],
    'ebitda': ['ebitda'],
    'debt': ['debt', 'borrow', 'liability'],
    'retained': ['retain', 'retained'],
    'dividend': ['dividend', 'div_'],
}

for category, kws in keywords.items():
    print(f'\n=== {category} ===')
    found = []
    for f in all_fields:
        fid = f.get('id', '')
        for kw in kws:
            if kw.lower() in fid.lower():
                cov = f.get('coverage', 0)
                found.append((fid, cov))
                break
    # Sort by coverage
    found.sort(key=lambda x: x[1], reverse=True)
    for fid, cov in found[:5]:
        print(f'  {fid} (cov={cov:.3f})')

# Save high coverage fields
high_cov = [f for f in all_fields if f.get('coverage', 0) > 0.7]
print(f'\n=== High coverage fields (>0.7): {len(high_cov)} ===')
for f in high_cov[:30]:
    print(f"  {f.get('id')} (cov={f.get('coverage', 0):.3f})")
